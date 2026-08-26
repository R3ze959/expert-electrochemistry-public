from __future__ import annotations

import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "audit_release_privacy.py"
SPEC = importlib.util.spec_from_file_location("audit_release_privacy", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)


def labels(text: str) -> list[str]:
    return MODULE.scan_text("probe", text)


class PrivacyRuleTests(unittest.TestCase):
    def test_home_and_volume_paths(self) -> None:
        probes = [
            "/" + "Users" + "/example/private/file.txt",
            "/" + "home" + "/example/private/file.txt",
            "/" + "Volumes" + "/LabDrive/private/file.txt",
            "C:" + "\\" + "Users" + "\\" + "example" + "\\" + "private.txt",
            "\\" + "\\" + "server" + "\\" + "share" + "\\" + "private.txt",
            "file:" + "///" + "Users" + "/example/private/file.txt",
        ]
        for probe in probes:
            with self.subTest(probe=probe):
                self.assertTrue(labels(probe))

    def test_identifiers_and_secrets(self) -> None:
        probes = [
            "person" + "@" + "example.org",
            "10." + "1234" + "/fictional.record",
            "a" * 64,
            "ghp" + "_" + "A" * 24,
            "AKIA" + "A" * 16,
            "api_" + "key=" + "A" * 20,
            "-----BEGIN " + "PRIVATE KEY-----",
        ]
        for probe in probes:
            with self.subTest(probe=probe[:12]):
                self.assertTrue(labels(probe))

    def test_clean_allowlisted_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "release-files.txt").write_text(
                "release-files.txt\nsafe.txt\n", encoding="utf-8"
            )
            (root / "safe.txt").write_text("synthetic safe content\n", encoding="utf-8")
            self.assertEqual(MODULE.audit_directory(root), [])

    def test_unlisted_and_cache_files_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "release-files.txt").write_text(
                "release-files.txt\nsafe.txt\n", encoding="utf-8"
            )
            (root / "safe.txt").write_text("safe\n", encoding="utf-8")
            cache = root / "__pycache__"
            cache.mkdir()
            (cache / "module.pyc").write_bytes(b"binary")
            findings = MODULE.audit_directory(root)
            self.assertTrue(any("unlisted file" in finding for finding in findings))

    def test_filename_is_scanned(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            sensitive_name = "person" + "@" + "example.org"
            (root / "release-files.txt").write_text(
                f"release-files.txt\n{sensitive_name}\n", encoding="utf-8"
            )
            (root / sensitive_name).write_text("safe body\n", encoding="utf-8")
            findings = MODULE.audit_directory(root)
            self.assertTrue(any("email address" in finding for finding in findings))

    def test_unsafe_zip_path_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "unsafe.zip"
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr("../outside.txt", "unsafe")
            findings = MODULE.audit_zip(archive)
            self.assertTrue(any("unsafe ZIP path" in finding for finding in findings))


if __name__ == "__main__":
    unittest.main()
