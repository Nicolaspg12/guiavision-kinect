# Arquitectura y procedencia

La base es la implementación modular original de cuatro archivos en `codigo final`, dentro del proyecto Kinect v1. Se mantiene su diseño de inferencia CPU, clases personalizadas y avisos de proximidad. Los scripts exploratorios y variantes monolíticas no se publican como puntos de entrada adicionales.

| Módulo | Responsabilidad |
| --- | --- |
| `__main__.py` | Parámetros, validación previa, arranque y cierre |
| `security.py` | Integridad del checkpoint y dirección relativa |
| `kinect_v1.py` | OpenNI2, streams RGB-D y profundidad en metros |
| `yolo_segmentation.py` | Inferencia, máscara, promedio de profundidad y anotación |
| `main.py` | Bucle, visualización y selección de avisos |
| `audio_processing.py` | Síntesis local, temporales y canal estéreo |

## Cambios de preparación

Se añadió una entrada de paquete, validación SHA-256 y comprobación de clases. Se corrigió el uso de detecciones antes de su inicialización, se hicieron las máscaras dependientes del tamaño de imagen y se evitó oscurecer toda la imagen por cada objeto. Se conserva el promedio de distancia de la versión original que el autor reporta como satisfactoria.

Se conserva por defecto la orientación invertida original; `--no-mirror` permite ajustarla a otro montaje. Los streams mantienen la configuración del controlador original y presuponen profundidad en milímetros y alineación RGB-D. Se añadió cierre de audio y runtime, aislamiento de WAV temporales y detención ante fallos de lectura o inferencia.

Estos cambios tienen comprobaciones estáticas y unitarias parciales; no deben describirse como validados en hardware hasta completar el protocolo.
