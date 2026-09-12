# SPDX-License-Identifier: AGPL-3.0-only
"""Validaciones independientes de las bibliotecas de inferencia."""
import hashlib
import math
from pathlib import Path

MODEL_SHA256 = "543c913aa621eb58d9db88b8a3123c4fd3820f163acdda32c4c05e681d1d5c99"


def verify_model(path):
    """Exigir el checkpoint local conocido antes de deserializarlo.

    El hash detecta sustituciones; no certifica que un checkpoint sea inocuo.
    Un atacante que modifique este código también puede cambiar el hash.
    """
    model = Path(path).expanduser().resolve(strict=True)
    if not model.is_file() or model.suffix.lower() != ".pt":
        raise ValueError("Se requiere un archivo local .pt")
    digest = hashlib.sha256()
    with model.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    if digest.hexdigest() != MODEL_SHA256:
        raise ValueError("Modelo rechazado: SHA-256 diferente del checkpoint del proyecto")
    return model


def direction(center_x, width, mirror=False):
    if not math.isfinite(width) or width <= 0:
        raise ValueError("Ancho de imagen inválido")
    if not math.isfinite(center_x) or not 0 <= center_x <= width:
        raise ValueError("Centro de objeto fuera de la imagen")
    offset = center_x - width / 2
    if abs(offset) < width * 50 / 640:
        return "centro"
    left = offset < 0
    if mirror:
        left = not left
    return "izquierda" if left else "derecha"
