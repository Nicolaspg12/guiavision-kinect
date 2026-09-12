# SPDX-License-Identifier: AGPL-3.0-only
"""Entrada local: python -m guiavision --help."""
import argparse
import os
from pathlib import Path
from .security import verify_model


def main():
    parser = argparse.ArgumentParser(description="GuíaVisión | Prototipo RGB-D con Kinect v1")
    parser.add_argument("--model", type=Path, default=Path(__file__).resolve().parents[1] / "models/best.pt")
    parser.add_argument("--openni-redist", type=Path,
                        default=Path(os.environ.get("OPENNI2_REDIST", r"C:\Program Files\OpenNI2\Redist")))
    parser.add_argument("--mirror", action=argparse.BooleanOptionalAction, default=True,
                        help="Invertir izquierda/derecha como en el montaje original; --no-mirror desactiva la inversión")
    parser.add_argument("--verify-model", action="store_true", help="Verificar integridad sin cargar el modelo ni abrir el sensor")
    args = parser.parse_args()
    try:
        model = verify_model(args.model)
    except (OSError, ValueError) as error:
        parser.exit(1, f"No se puede utilizar el modelo: {error}\n")
    if args.verify_model:
        print("SHA-256 correcto. No se ha deserializado el modelo.")
        return
    if not args.openni_redist.is_dir():
        parser.error("No existe la carpeta OpenNI2. Usa --openni-redist con una instalación de confianza.")
    print("Prototipo experimental: requiere calibración y supervisión; no es una ayuda de movilidad validada.")
    import cv2
    from .main import KinectParaCiegos
    sistema = None
    try:
        sistema = KinectParaCiegos(model, str(args.openni_redist.resolve()), args.mirror)
        if not sistema.yolo.cargar_modelo_yolo():
            raise RuntimeError("No se pudo cargar el modelo")
        if not sistema.kinect.inicializar_kinect() or not sistema.kinect.configurar_streams():
            raise RuntimeError("No se pudo iniciar el sensor RGB-D")
        print("Q: salir | A: activar/desactivar audio")
        sistema.ejecutar_bucle_cpu_optimizado()
    finally:
        if sistema is not None:
            sistema.running = False
            try:
                sistema.audio.close()
            finally:
                sistema.kinect.cerrar_streams()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
