# SPDX-License-Identifier: AGPL-3.0-only
# Autoria academica (2025): Alvaro Mauricio Molina Guamanga y Nicolas Santiago Pantoja Garcia

import cv2
import numpy as np
from .security import verify_model

class YoloSegmentation:
    def __init__(self, model_path):
        self.model = None
        self.model_path = model_path
        self.target_classes = {
            0: {'name': 'carro', 'color': (0, 0, 255)},
            1: {'name': 'silla', 'color': (255, 0, 0)},
            2: {'name': 'cono', 'color': (0, 165, 255)},
            3: {'name': 'persona', 'color': (0, 255, 0)},
            4: {'name': 'planta', 'color': (128, 0, 128)}
        }
        self.mascara_objeto = np.zeros((480, 640), dtype=np.uint8)
        self.overlay = np.zeros((480, 640, 3), dtype=np.uint8)

    def cargar_modelo_yolo(self):
        """Cargar el modelo YOLO optimizado para CPU"""
        try:
            verified = verify_model(self.model_path)
            from ultralytics import YOLO
            self.model = YOLO(str(verified), task='segment')
            expected = {0: 'car', 1: 'chair', 2: 'cone', 3: 'person', 4: 'potted plant'}
            if self.model.names != expected:
                raise ValueError('Las etiquetas del modelo no coinciden con las cinco clases esperadas')
            print("Calentando modelo para CPU...")
            for size in [320, 224]:
                dummy_input = np.zeros((size, size, 3), dtype=np.uint8)
                self.model(dummy_input, imgsz=size, verbose=False, device='cpu')
            print("Modelo YOLO cargado y optimizado para CPU")
            return True
        except Exception as e:
            print(f"Error al cargar modelo YOLO: {e}")
            return False

    def aplicar_segmentacion_cpu(self, frame_color, profundidad_metros, verificar_camara_tapada, obtener_direccion, profundidad_maxima=2.5):
        """Aplicar segmentación YOLO optimizada para CPU con límite de 2.5m"""
        if frame_color.shape[:2] != profundidad_metros.shape:
            raise ValueError('Color y profundidad deben estar registrados y tener igual resolución')
        self.mascara_objeto = np.zeros(profundidad_metros.shape, dtype=np.uint8)
        self.overlay = np.zeros_like(frame_color)
        frame_segmentado = frame_color.copy()
        info_detecciones = []
        detecciones_audio = []
        if verificar_camara_tapada(frame_color):
            return frame_segmentado, info_detecciones
        if self.model:
            try:
                resultados = self.model(frame_color,
                                      imgsz=320,
                                      conf=0.4,
                                      iou=0.4,
                                      device='cpu',
                                      verbose=False,
                                      max_det=8,
                                      half=False,
                                      augment=False)
                for resultado in resultados:
                    if hasattr(resultado, 'boxes') and resultado.boxes is not None:
                        for i in range(len(resultado.boxes)):
                            if resultado.masks is not None and i < len(resultado.masks):
                                mascara = resultado.masks[i].xy[0]
                                caja = resultado.boxes[i]
                                clase = resultado.boxes.cls[i]
                                id_clase = int(clase)
                                confianza = float(caja.conf[0])
                                if id_clase in self.target_classes and confianza > 0.4:
                                    info_clase = self.target_classes[id_clase]
                                    color = info_clase['color']
                                    if len(mascara) < 3 or not np.isfinite(mascara).all():
                                        continue
                                    puntos = np.array(mascara, dtype=np.int32)
                                    self.mascara_objeto.fill(0)
                                    cv2.fillPoly(self.mascara_objeto, [puntos], 1)
                                    objeto_profundidad = profundidad_metros * self.mascara_objeto
                                    mascara_valida = (objeto_profundidad > 0.3) & (objeto_profundidad <= profundidad_maxima)
                                    profundidades_validas = objeto_profundidad[mascara_valida]
                                    if len(profundidades_validas) > 10:
                                        profundidad_promedio = np.mean(profundidades_validas)
                                        if 0.3 <= profundidad_promedio <= profundidad_maxima:
                                            x1, y1, x2, y2 = map(int, caja.xyxy[0])
                                            x_centro = (x1 + x2) // 2
                                            direccion = obtener_direccion(x_centro)
                                            self.overlay[:] = frame_segmentado
                                            cv2.fillPoly(self.overlay, [puntos], color)
                                            cv2.addWeighted(self.overlay, 0.3, frame_segmentado, 0.7, 0, frame_segmentado)
                                            cv2.polylines(frame_segmentado, [puntos], True, color, 2)
                                            cv2.rectangle(frame_segmentado, (x1, y1), (x2, y2), color, 2)
                                            etiqueta = f"{info_clase['name']} {profundidad_promedio:.1f}m"
                                            cv2.putText(frame_segmentado, etiqueta, (x1, y1-10),
                                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
                                            info_detecciones.append({
                                                'puntos': puntos,
                                                'color': color,
                                                'etiqueta': etiqueta,
                                                'profundidad': profundidad_promedio,
                                                'direccion': direccion,
                                                'nombre_clase': info_clase['name'],
                                                'confianza': confianza,
                                                'bbox': (x1, y1, x2, y2)
                                            })
                                            detecciones_audio.append({
                                                'nombre_clase': info_clase['name'],
                                                'profundidad': profundidad_promedio,
                                                'direccion': direccion
                                            })
                                        else:
                                            print(f"Objeto {info_clase['name']} fuera de rango: {profundidad_promedio:.1f}m")
            except Exception as e:
                raise RuntimeError("Falló la segmentación; se detiene la aplicación") from e
        return frame_segmentado, detecciones_audio
