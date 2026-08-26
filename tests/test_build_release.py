from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
SCRIPT = ROOT / "scripts" / "build_release.py"


def environment() -> dict[str, str]:
    values = dict(os.environ)
    values["PYTHONDONTWRITEBYTECODE"] = "1"
    return values


class BuildReleaseTests(unittest.TestCase):
    def test_build_is_reproducible_and_audited(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.zip"
            second = Path(temporary) / "second.zip"
            for output in (first, second):
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), "--root", str(ROOT), "--output", str(output)],
                    capture_output=True,
                    text=True,
                    env=environment(),
                )
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
            self.assertEqual(
                hashlib.sha256(first.read_bytes()).digest(),
                hashlib.sha256(second.read_bytes()).digest(),
            )

    def test_unlisted_file_blocks_build(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "synthetic-skill"
            root.mkdir()
            (root / "release-files.txt").write_text(
                "release-files.txt\nsafe.txt\n", encoding="utf-8"
            )
            (root / "safe.txt").write_text("safe\n", encoding="utf-8")
            (root / "unexpected.txt").write_text("not allowlisted\n", encoding="utf-8")
            output = Path(temporary) / "blocked.zip"
            result = subprocess.run(
                [sys.executable, str(SCRIPT), "--root", str(root), "--output", str(output)],
                capture_output=True,
                text=True,
                env=environment(),
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unlisted file", result.stderr + result.stdout)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
