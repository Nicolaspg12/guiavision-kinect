# SPDX-License-Identifier: AGPL-3.0-only
# Autoria academica (2025): Alvaro Mauricio Molina Guamanga y Nicolas Santiago Pantoja Garcia

import cv2
import numpy as np
import time
from .yolo_segmentation import YoloSegmentation
from .kinect_v1 import KinectV1
from .audio_processing import AudioProcessing

class KinectParaCiegos:
    def __init__(self, model_path, redist_path, mirror=False):
        self.kinect = KinectV1(redist_path)
        self.yolo = YoloSegmentation(model_path)
        self.mirror = mirror
        self.audio = AudioProcessing()
        self.running = True
        self.fps_counter = 0
        self.fps_time = time.time()
        self.avg_fps = 0
        self.frame_count = 0
        self.camara_tapada = False
        self.frame_center_x = 320
        self.direction_threshold = 50
        self.profundidad_maxima = 2.5
        self.ultimas_detecciones = {}
        self.umbral_cambio_distancia = 0.2
        self.max_repeticiones = 3
        print("Sistema configurado para usar CPU")
        print(f"DETECCIÓN LIMITADA A: 0.3-{self.profundidad_maxima} metros")
        print("Máximo 1 mensaje en cola de audio")
        print(f"Anuncia cambios > {self.umbral_cambio_distancia}m")

    def obtener_direccion(self, x_centro):
        from .security import direction
        return direction(x_centro, self.frame_center_x * 2, self.mirror)

    def verificar_camara_tapada(self, frame_color):
        """Verificar si la cámara está tapada optimizado"""
        if frame_color is None:
            return True
        sample = frame_color[::20, ::20]
        gray = np.dot(sample[..., :3], [0.114, 0.587, 0.299]).astype(np.uint8)
        brillo_promedio = np.mean(gray)
        if brillo_promedio < 10:
            if not self.camara_tapada:
                self.camara_tapada = True
            return True
        else:
            if self.camara_tapada:
                self.camara_tapada = False
            return False

    def deberia_anunciar_deteccion(self, nombre_clase, profundidad):
        """Determinar si se debe anunciar una detección"""
        tiempo_actual = time.time()
        if nombre_clase not in self.ultimas_detecciones:
            self.ultimas_detecciones[nombre_clase] = {
                'profundidad': profundidad,
                'contador': 1,
                'timestamp': tiempo_actual,
                'ultimo_anuncio': tiempo_actual
            }
            return True
        deteccion_anterior = self.ultimas_detecciones[nombre_clase]
        profundidad_anterior = deteccion_anterior['profundidad']
        contador_anterior = deteccion_anterior['contador']
        cambio_significativo = abs(profundidad - profundidad_anterior) > self.umbral_cambio_distancia
        if cambio_significativo:
            self.ultimas_detecciones[nombre_clase] = {
                'profundidad': profundidad,
                'contador': 1,
                'timestamp': tiempo_actual,
                'ultimo_anuncio': tiempo_actual
            }
            print(f"Cambio significativo detectado: {nombre_clase} {profundidad_anterior:.1f}m -> {profundidad:.1f}m")
            return True
        if contador_anterior < self.max_repeticiones:
            if tiempo_actual - deteccion_anterior['ultimo_anuncio'] > self.audio.anuncio_intervalo:
                self.ultimas_detecciones[nombre_clase]['contador'] += 1
                self.ultimas_detecciones[nombre_clase]['ultimo_anuncio'] = tiempo_actual
                print(f"Repetición {self.ultimas_detecciones[nombre_clase]['contador']} de {nombre_clase}")
                return True
        self.ultimas_detecciones[nombre_clase]['timestamp'] = tiempo_actual
        return False

    def anunciar_detecciones_constantes(self, detecciones_audio):
        """Anunciar detecciones optimizado"""
        if not detecciones_audio:
            self.ultimas_detecciones.clear()
            if time.time() - self.audio.tiempo_ultimo_anuncio > 10.0:
                self.audio.anunciar_deteccion("Explorando entorno", "centro")
            return
        if not self.audio.puede_anunciar():
            return
        detecciones_audio.sort(key=lambda x: x['profundidad'])
        for deteccion in detecciones_audio:
            nombre_clase = deteccion['nombre_clase']
            profundidad = deteccion['profundidad']
            direccion = deteccion['direccion']
            if self.deberia_anunciar_deteccion(nombre_clase, profundidad):
                mensaje = f"{nombre_clase} a {profundidad:.1f} metros"
                self.audio.anunciar_deteccion(mensaje, direccion)
                break

    def crear_visualizacion_profundidad_rapida(self, profundidad_metros):
        """Crear visualización de profundidad ultra rápida para CPU"""
        profundidad_visual = cv2.convertScaleAbs(profundidad_metros * (255 / self.profundidad_maxima))
        profundidad_visual = cv2.applyColorMap(profundidad_visual, cv2.COLORMAP_JET)
        cv2.putText(profundidad_visual, f"Rango: 0.3-{self.profundidad_maxima}m", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(profundidad_visual, "        Objetos >2.5m ignorados", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        return profundidad_visual

    def ejecutar_bucle_cpu_optimizado(self):
        """Bucle principal optimizado para CPU"""
        print("Iniciando bucle principal para CPU...")
        print(f"DETECCIÓN LIMITADA A: 0.3-{self.profundidad_maxima} metros")
        print("Objetos más allá de 2.5m serán ignorados")
        last_profundidad_time = time.time()
        last_segmentacion_time = time.time()
        segmentacion_intervalo = 0.1
        detecciones_audio = []
        while self.running:
            try:
                frame_color, frame_depth = self.kinect.obtener_frames()
                if frame_color is None or frame_depth is None:
                    raise RuntimeError("Se perdió la lectura del sensor")
                profundidad_metros = self.kinect.procesar_frame_profundidad(frame_depth)
                if profundidad_metros is None:
                    raise RuntimeError("Se perdió la lectura del sensor")
                self.frame_center_x = frame_color.shape[1] / 2
                current_time = time.time()
                if current_time - last_segmentacion_time >= segmentacion_intervalo:
                    frame_segmentado, detecciones_audio = self.yolo.aplicar_segmentacion_cpu(
                        frame_color, profundidad_metros, self.verificar_camara_tapada, self.obtener_direccion)
                    self.anunciar_detecciones_constantes(detecciones_audio)
                    last_segmentacion_time = current_time
                else:
                    if 'frame_segmentado' not in locals():
                        frame_segmentado = frame_color.copy()
                self.frame_count += 1
                current_time = time.time()
                if current_time - self.fps_time >= 0.5:
                    self.avg_fps = self.fps_counter / (current_time - self.fps_time)
                    self.fps_counter = 0
                    self.fps_time = current_time
                else:
                    self.fps_counter += 1
                cv2.putText(frame_segmentado, f"FPS: {self.avg_fps:.1f}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame_segmentado, f"Detecciones: {len(detecciones_audio)}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame_segmentado, f"Límite: {self.profundidad_maxima}m", (10, 90),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                if current_time - last_profundidad_time > 0.3:
                    profundidad_visual = self.crear_visualizacion_profundidad_rapida(profundidad_metros)
                    cv2.putText(profundidad_visual, f"FPS: {self.avg_fps:.1f}", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                    cv2.imshow('Mapa de Profundidad', profundidad_visual)
                    last_profundidad_time = current_time
                cv2.imshow(f'Segmentación (0.3-{self.profundidad_maxima}m)', frame_segmentado)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('a'):
                    self.audio.audio_activado = not self.audio.audio_activado
                    print(f"Audio {'activado' if self.audio.audio_activado else 'desactivado'}")
            except Exception as e:
                print(f"Error en bucle principal: {e}")
                raise
        self.running = False
