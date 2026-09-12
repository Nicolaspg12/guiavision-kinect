# SPDX-License-Identifier: AGPL-3.0-only
# Autoria academica (2025): Alvaro Mauricio Molina Guamanga y Nicolas Santiago Pantoja Garcia

import os
import numpy as np
from primesense import openni2

class KinectV1:
    def __init__(self, redist_path=r"C:\Program Files\OpenNI2\Redist"):
        self.openni2_redist = redist_path
        self.initialized = False
        self.device = None
        self.depth_stream = None
        self.color_stream = None
        self.profundidad_metros = np.zeros((480, 640), dtype=np.float32)

    def inicializar_kinect(self):
        """Inicializar el dispositivo Kinect"""
        try:
            os.environ['OPENNI2_REDIST'] = self.openni2_redist
            openni2.initialize(self.openni2_redist)
            self.initialized = True
            self.device = openni2.Device.open_any()
            print("Kinect inicializado correctamente")
            return True
        except Exception as e:
            print(f"Error al inicializar Kinect: {e}")
            return False

    def configurar_streams(self):
        """Configurar los streams de profundidad y color"""
        try:
            self.depth_stream = self.device.create_depth_stream()
            self.depth_stream.start()
            self.color_stream = self.device.create_color_stream()
            self.color_stream.start()
            print("Streams configurados correctamente")
            return True
        except Exception as e:
            print(f"Error al configurar streams: {e}")
            return False

    def obtener_frames(self):
        """Obtener frames de color y profundidad optimizado"""
        try:
            frame_color = self.color_stream.read_frame()
            frame_color_data = frame_color.get_buffer_as_uint8()
            color_array = np.frombuffer(frame_color_data, dtype=np.uint8)
            color_array = color_array.reshape(frame_color.height, frame_color.width, 3)
            color_array = color_array[:, :, [2, 1, 0]]
            frame_depth = self.depth_stream.read_frame()
            frame_depth_data = frame_depth.get_buffer_as_uint16()
            depth_array = np.frombuffer(frame_depth_data, dtype=np.uint16)
            depth_array = depth_array.reshape(frame_depth.height, frame_depth.width)
            return color_array, depth_array
        except Exception as e:
            print(f"Error obteniendo frames: {e}")
            return None, None

    def procesar_frame_profundidad(self, frame_profundidad, profundidad_maxima=2.5):
        """Procesar frame de profundidad optimizado para CPU"""
        try:
            self.profundidad_metros = frame_profundidad.astype(np.float32) / 1000.0
            self.profundidad_metros[self.profundidad_metros > profundidad_maxima] = 0
            self.profundidad_metros[self.profundidad_metros < 0.3] = 0
            return self.profundidad_metros
        except Exception as e:
            print(f"Error procesando profundidad: {e}")
            return None

    def cerrar_streams(self):
        """Cerrar los streams de Kinect"""
        for stream in (self.depth_stream, self.color_stream):
            if stream:
                try:
                    stream.stop()
                except Exception:
                    pass
        if self.initialized:
            openni2.unload()
            self.initialized = False
