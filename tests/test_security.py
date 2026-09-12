import tempfile
import unittest
from pathlib import Path
from guiavision.security import direction, verify_model


class SecurityTests(unittest.TestCase):
    def test_bundled_model_integrity(self):
        model = Path(__file__).resolve().parents[1] / 'models/best.pt'
        self.assertEqual(verify_model(model), model.resolve())

    def test_tampered_checkpoint_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'untrusted.pt'
            path.write_bytes(b'not the trusted checkpoint')
            with self.assertRaisesRegex(ValueError, 'SHA-256'):
                verify_model(path)

    def test_remote_or_missing_model_is_not_downloaded(self):
        with self.assertRaises((OSError, ValueError)):
            verify_model('https://example.invalid/model.pt')

    def test_default_and_mirrored_directions(self):
        self.assertEqual(direction(100, 640), 'izquierda')
        self.assertEqual(direction(540, 640), 'derecha')
        self.assertEqual(direction(100, 640, True), 'derecha')
        self.assertEqual(direction(540, 640, True), 'izquierda')
        for mirror in (False, True):
            self.assertEqual(direction(320, 640, mirror), 'centro')

    def test_resolution_independence(self):
        self.assertEqual(direction(640, 1280), 'centro')
        self.assertEqual(direction(200, 1280), 'izquierda')

    def test_invalid_coordinates(self):
        for x, width in ((-1, 640), (641, 640), (0, 0), (float('nan'), 640), (1, float('inf'))):
            with self.assertRaises(ValueError):
                direction(x, width)


if __name__ == '__main__':
    unittest.main()
