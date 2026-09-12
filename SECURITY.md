# Seguridad

## Medidas de esta edición

- Se exige un checkpoint `.pt` local con SHA-256 conocido antes de importar el cargador YOLO. No se aceptan URLs ni descargas automáticas de modelos desde la opción `--model`.
- Se detiene el arranque si falla el modelo o el sensor; los errores de inferencia detienen el bucle. La alineación RGB-D requiere comprobación física.
- Los WAV de voz se crean en un directorio temporal exclusivo y se limpian al finalizar cada aviso, incluso al producirse errores ordinarios.
- Las capturas, secretos habituales, entornos y registros están excluidos mediante `.gitignore`.
- El workflow de comprobaciones tiene acceso de solo lectura y fija la acción externa a un commit. Dependabot propone actualizaciones.

Estas medidas reducen riesgos concretos; no constituyen una auditoría completa ni una garantía contra ataques. `.gitignore` no detecta secretos ya incluidos en un archivo rastreado.

## Modelos y dependencias

Los checkpoints PyTorch pueden contener objetos serializados capaces de ejecutar código durante la carga. El hash solo permite comprobar que los bytes coinciden con el archivo distribuido: **no prueba que el modelo sea seguro**, ni protege frente a alguien que cambie simultáneamente código y modelo. Mantén permisos de escritura restringidos y no reemplaces archivos mientras se ejecuta la aplicación.

El checkpoint se inspeccionó estáticamente; no se ejecutó para preparar esta publicación. No cargues modelos de terceros desconocidos. No ejecutes el prototipo como administrador. Las DLL del runtime OpenNI2 también deben proceder de una instalación de confianza.

El código de la aplicación no envía capturas a servicios remotos ni incluye un servidor de red. No se ha auditado el tráfico de todas las dependencias; no se promete aislamiento de red. `requirements.txt` no es un lockfile ni certifica ausencia de vulnerabilidades.

## Reportar un problema

Si GitHub ofrece **Security → Report a vulnerability**, utiliza ese canal privado. Si no está disponible, abre una issue solicitando un canal privado **sin** incluir credenciales, datos personales ni detalles de explotación. No publiques capturas de personas sin autorización.

## Seguridad de uso

No interpretes el silencio como ausencia de obstáculos. El sistema es experimental y requiere pruebas supervisadas. Consulta `docs/VALIDATION.md`.

Referencia: [Advertencia de torch.load](https://docs.pytorch.org/docs/stable/generated/torch.load).
