# Modelo de GuíaVisión

| Campo | Valor |
| --- | --- |
| Archivo | `best.pt` |
| Tamaño | 6.903.715 bytes |
| Tipo | Checkpoint YOLOv8 con cabeza de segmentación |
| Clases | 0: car; 1: chair; 2: cone; 3: person; 4: potted plant |
| Uso previsto | Investigación y demostración supervisada |
| Procedencia | Archivo suministrado con el proyecto Kinect v1 de Nicolas Pantoja |
| Licencia de publicación | AGPL-3.0-only; sujeto a los derechos de los componentes de terceros |

SHA-256:

```text
543c913aa621eb58d9db88b8a3123c4fd3820f163acdda32c4c05e681d1d5c99
```

La inspección estática confirmó las cinco etiquetas y una cabeza `Segment`. No se deserializó el checkpoint durante la preparación. Sus metadatos contienen rutas históricas de entrenamiento; no son rutas requeridas para ejecutar el proyecto.

El informe académico suministrado documenta entrenamiento y resultados de evaluación, resumidos en [docs/RESULTS.md](../docs/RESULTS.md). No se proporcionaron los archivos del dataset, scripts de entrenamiento ni registros para reproducirlos. No se ha verificado que este hash corresponda exactamente al «modelo 5» del informe. La licencia del código no certifica los derechos del dataset original.

No sustituir este modelo por `yolov8n-seg.pt`: el modelo genérico emplea otra taxonomía y produciría nombres incorrectos con el mapeo del proyecto. Para introducir un nuevo modelo se debe revisar su procedencia, taxonomía, hash y rendimiento mediante un cambio de código revisado.
