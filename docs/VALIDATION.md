# Validación antes de una demostración

## Comprobaciones automatizadas

Seis pruebas de biblioteca estándar: hash del checkpoint, rechazo de archivo alterado, rechazo de URL/archivo ausente, direcciones normales e invertidas, escalado de resolución y coordenadas inválidas. También se comprueba la sintaxis Python. No requieren cargar `best.pt`.

## Resultados previos y comprobación de esta edición

El informe de investigación documenta resultados satisfactorios de precisión, audio y recorridos reales, detallados en [RESULTS.md](RESULTS.md). La siguiente lista corresponde a la verificación de las modificaciones y a la reproducción en otros equipos; no sustituye ni invalida los ensayos del trabajo original.

1. Registrar Windows, Python, versiones resueltas de dependencias, OpenNI2 y controlador del Kinect.
2. Confirmar color RGB y profundidad en milímetros con igual resolución. El código conserva los modos por defecto del controlador original; no configura automáticamente el registro ni la sincronización.
3. Comparar máscaras y bordes de profundidad con objetos conocidos; verificar alineación a varias distancias. Corregir la configuración o calibración antes de interpretar las distancias si no coinciden.
4. Medir error de distancia frente a una referencia independiente, con varias superficies e iluminaciones. Evaluar especialmente el límite inferior configurado de 0,3 m, que puede estar fuera del rango fiable del dispositivo.
5. Comprobar izquierda, centro y derecha con el montaje real y auriculares colocados correctamente; se mantiene la inversión original y `--no-mirror` permite desactivarla si corresponde.
6. Validar la voz instalada, balance estéreo, cola de avisos, silenciamiento con A y cierre con Q.
7. Probar desconexión, cámara tapada, iluminación insuficiente, ausencia de audio, modelo incorrecto y salida repetida. Verificar que no se anuncien datos antiguos tras un fallo.
8. Evaluar falsos positivos y negativos para las cinco clases y objetos no contemplados. Medir latencia de inferencia y audio, no solo el contador visual de FPS.

Documentar resultados y condiciones en un informe separado. No usar personas con discapacidad visual como primera prueba de seguridad ni hacer pruebas de movilidad sin un protocolo y supervisión adecuados.

## Limitaciones conocidas

- No hay seguimiento con identidad de objetos: el historial de avisos se agrupa por clase.
- El contador de FPS visual refleja iteraciones del bucle, no necesariamente inferencias por segundo.
- La heurística de brillo puede confundir oscuridad con cámara tapada.
- Los avisos de voz pueden retrasarse mientras habla el sintetizador; no proporcionan respuesta garantizada en tiempo real.
- Se dispone de resultados académicos de entrenamiento y validación técnica en campo; no de una evaluación con usuarios con discapacidad visual ni de validación clínica.
