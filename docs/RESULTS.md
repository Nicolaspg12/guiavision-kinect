# Resultados experimentales del proyecto original

Esta página resume el informe de investigación de **Alvaro Mauricio Molina Guamanga y Nicolas Santiago Pantoja García (2025)**, *Algoritmo de segmentación semántica para facilitar la movilidad de personas con discapacidad visual en las instalaciones de la Universidad Mariana*, Ingeniería Mecatrónica, Universidad Mariana. Asesor: Carlos Armando Patiño Terán.

La fuente es el PDF de 88 páginas suministrado por Nicolas Pantoja. Los números de página siguientes corresponden a ese documento. Se reproducen sus resultados reportados, sin presentarlos como mediciones nuevas de esta edición del código. El PDF completo y las imágenes de personas no se redistribuyen en este repositorio.

## Pruebas funcionales en la Universidad Mariana

Se realizaron diez recorridos a baja velocidad en cada escenario, con cinco obstáculos por recorrido y cambio de posiciones cada dos recorridos. Son **100 oportunidades de detección**, no 100 obstáculos independientes ni 100 participantes. Fuente: sección 2.3.5, tabla 7, página 64.

| Escenario | Condición | Recorridos | Oportunidades | Alertas correctas | Éxito reportado |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | Iluminación estable, 7 × 6 m | 10 | 50 | 42 | 84 % |
| 2 | Contraste de iluminación, 2,8 × 6 m | 10 | 50 | 39 | 78 % |
| **Total** | **Dos espacios reales** | **20** | **100** | **81** | **81 %** |

El 81 % expresa la tasa de alertas correctas del ensayo funcional; no equivale a mAP ni a una garantía de detección en otros entornos.

## Medición de distancia con Kinect v1

El informe comparó lecturas con cinta métrica, con diez muestras por objeto y distancias de referencia entre 1 y 2,5 m, en posiciones izquierda, centro y derecha. El texto principal reporta estos errores promedio (páginas 59 y 72; anexo 2, páginas 83–85):

| Objeto | Error promedio reportado |
| --- | ---: |
| Silla | 0,81 % |
| Persona | 0,83 % |
| Planta | 1,05 % |
| Cono | 1,09 % |

Todos se sitúan por debajo del 2 % **en las mediciones descritas**. El anexo indica 1,02 % para planta, frente a 1,05 % en el texto principal; se conserva aquí el dato del texto y se deja constancia de la discrepancia. No se ha recalculado ni certificado estadísticamente cada tabla. Estas pruebas no acreditan precisión de distancia para la clase carro ni para todo el rango configurado desde 0,3 m.

## Audio direccional

Las secciones 2.3.4 y 3.3.2 (páginas 62–63 y 72) documentan reproducción correcta por los canales izquierdo, derecho o ambos, sincronización con las detecciones, ausencia de solapamientos y separación mínima de tres segundos. El sistema usa pyttsx3 y pygame.mixer, con avisos de tipo, distancia y posición. Es un resultado funcional documentado; el informe no aporta un porcentaje independiente de acierto del audio.

## Evaluación de los modelos

El **modelo 5** fue seleccionado para las fases experimentales. La tabla 8 del anexo 1, página 83, informa resultados de validación posterior con un conjunto externo:

| Métrica reportada | Modelo 5 |
| --- | ---: |
| mAP@50 | 0,8155 |
| mAP@50–95 | 0,5522 |
| Precisión | 0,8385 |
| Recall | 0,7482 |
| F1-score | 0,7813 |

Se transcriben los valores del informe sin inferir el método de agregación. No se dispone aquí del conjunto externo ni de los registros para recalcularlos. Tampoco se ha establecido una correspondencia verificable entre el identificador «modelo 5» y el hash del checkpoint distribuido.

La tabla 5 de la página 45 presenta otra evaluación: YOLOv8n-seg entrenado para **silla**, con 74 imágenes de entrenamiento y 18 de validación. Allí se reportan precisión 1,0000, recall 0,8757, F1 0,9337, mAP@50 0,9320 y mAP@50–95 0,8110. Estos resultados de una clase **no se atribuyen al sistema final de cinco clases**. Los 96,1 ms de CPU ONNX citados en la página 44 proceden de una comparación de Ultralytics; no son una medición de latencia integral de GuíaVisión.

## Alcance de la evidencia

El informe concluye que se obtuvo un prototipo funcional y exitoso (página 75). También documenta fallos con contraluz, superposición de objetos, falsas clasificaciones de escaleras y latencia (páginas 64–65 y 73–77).

La página 73 aclara que se trató de validación técnica y **no se realizaron pruebas con usuarios con discapacidad visual**. Por tanto, el proyecto demuestra viabilidad técnica en los ensayos descritos, sin acreditar todavía una ayuda autónoma de movilidad validada con su población destinataria.

Las mejoras de empaquetado y seguridad publicadas aquí deben pasar una comprobación de regresión con el hardware original. El éxito documentado del trabajo original y esa comprobación pendiente son aspectos distintos.
