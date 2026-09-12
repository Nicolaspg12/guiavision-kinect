# SPDX-License-Identifier: AGPL-3.0-only
"""Síntesis local y reproducción estéreo con temporales aislados."""
from pathlib import Path
import queue
import tempfile
import threading
import time
import logging
import pygame.mixer
import pyttsx3
import pythoncom


class AudioProcessing:
    def __init__(self):
        self.audio_activado = True
        self.audio_queue = queue.Queue(maxsize=1)
        self.tiempo_ultimo_anuncio = 0.0
        self.anuncio_intervalo = 3.0
        self._stop = threading.Event()
        pygame.mixer.init(frequency=44100, size=-16, channels=2)
        self.audio_thread = threading.Thread(target=self._worker, daemon=True)
        self.audio_thread.start()

    def puede_anunciar(self):
        return (self.audio_activado and not self._stop.is_set()
                and time.time() - self.tiempo_ultimo_anuncio >= self.anuncio_intervalo)

    def anunciar_deteccion(self, mensaje, direccion):
        if not self.puede_anunciar() or not mensaje.strip():
            return False
        try:
            self.audio_queue.get_nowait()
        except queue.Empty:
            pass
        try:
            self.audio_queue.put_nowait((mensaje, direccion, time.monotonic()))
        except queue.Full:
            return False
        self.tiempo_ultimo_anuncio = time.time()
        return True

    def _worker(self):
        pythoncom.CoInitialize()
        engine = None
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            # Preferir una voz española instalada; nunca descargar voces.
            for voice in engine.getProperty('voices'):
                if any(token in str(voice).lower() for token in ('spanish', 'es-es', 'es-mx')):
                    engine.setProperty('voice', voice.id)
                    break
            while not self._stop.is_set():
                try:
                    mensaje, direccion, created = self.audio_queue.get(timeout=0.1)
                except queue.Empty:
                    continue
                if not self.audio_activado or time.monotonic() - created > 3:
                    continue
                try:
                    with tempfile.TemporaryDirectory(prefix='guiavision-') as directory:
                        wav = Path(directory) / 'speech.wav'
                        engine.save_to_file(mensaje, str(wav))
                        engine.runAndWait()
                        if self._stop.is_set() or not self.audio_activado:
                            continue
                        sound = pygame.mixer.Sound(str(wav))
                        channel = pygame.mixer.Channel(0)
                        channel.set_volume(*{'izquierda': (1, 0), 'derecha': (0, 1)}.get(direccion, (1, 1)))
                        channel.play(sound)
                        while channel.get_busy() and not self._stop.wait(0.05):
                            if not self.audio_activado:
                                channel.stop()
                        channel.stop()
                except Exception:
                    logging.exception('No se pudo reproducir el aviso de voz')
        except Exception:
            logging.exception('Audio no disponible; revisar voces y dispositivo de salida')
        finally:
            if engine is not None:
                engine.stop()
            pythoncom.CoUninitialize()

    def close(self):
        self._stop.set()
        self.audio_thread.join(timeout=5)
        if self.audio_thread.is_alive():
            logging.warning('La síntesis de voz no terminó en cinco segundos')
        else:
            pygame.mixer.quit()
