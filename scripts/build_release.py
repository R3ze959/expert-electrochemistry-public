#!/usr/bin/env python3
"""Build a deterministic, allowlisted skill ZIP and audit the final archive."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
import zipfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import audit_release_privacy as release_audit  # noqa: E402


FIXED_ZIP_TIME = (2026, 1, 1, 0, 0, 0)


def load_allowlist(root: Path) -> list[str]:
    manifest = root / release_audit.MANIFEST_NAME
    try:
        text = manifest.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise SystemExit(f"Cannot read release allowlist: {type(exc).__name__}") from exc
    entries, findings = release_audit.parse_manifest_text(text, release_audit.MANIFEST_NAME)
    if findings:
        raise SystemExit("Invalid release allowlist:\n- " + "\n- ".join(findings))
    return entries


def build_release(root: Path, output: Path) -> Path:
    root = root.resolve()
    output = output.resolve()
    if not root.is_dir():
        raise SystemExit("Skill root is not a directory.")
    if root == output.parent or root in output.parents:
        raise SystemExit("Release ZIP must be written outside the skill root.")
    if output.exists():
        raise SystemExit("Output already exists; choose a new versioned path.")

    findings = release_audit.audit_directory(root)
    if findings:
        raise SystemExit("Source release audit failed:\n- " + "\n- ".join(findings))
    entries = load_allowlist(root)
    output.parent.mkdir(parents=True, exist_ok=True)

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=output.name + ".", suffix=".tmp", dir=output.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        with zipfile.ZipFile(
            temporary,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
            strict_timestamps=True,
        ) as archive:
            for relative in sorted(entries):
                data = (root / relative).read_bytes()
                info = zipfile.ZipInfo(f"{root.name}/{relative}", FIXED_ZIP_TIME)
                info.create_system = 3
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                info.extra = b""
                archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        zip_findings = release_audit.audit_zip(temporary)
        if zip_findings:
            raise SystemExit("Final ZIP audit failed:\n- " + "\n- ".join(zip_findings))
        os.replace(temporary, output)
    finally:
        if temporary.exists():
            temporary.unlink()
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic allowlisted skill ZIP.")
    parser.add_argument(
        "--root", type=Path, default=SCRIPT_DIR.parent, help="Skill root; defaults to this skill."
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    built = build_release(args.root, args.output)
    print(f"Built and audited: {built}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
