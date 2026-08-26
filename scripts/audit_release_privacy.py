#!/usr/bin/env python3
"""Audit a release directory or ZIP against a strict file allowlist and leak rules."""

from __future__ import annotations

import argparse
import re
import stat
import zipfile
from pathlib import Path, PurePosixPath


MANIFEST_NAME = "release-files.txt"
DEFAULT_MAX_FILE_BYTES = 1_000_000
DEFAULT_MAX_TOTAL_BYTES = 5_000_000
MAX_COMPRESSION_RATIO = 200


CONTENT_RULES = (
    ("file URI to a home path", re.compile(r"file:/+(?:Users|home)/[A-Za-z0-9._-]+/", re.I)),
    ("macOS home path", re.compile(r"/Users/[A-Za-z0-9._-]+/")),
    ("Linux home path", re.compile(r"/home/[A-Za-z0-9._-]+/")),
    ("mounted-volume path", re.compile(r"/Vol" r"umes/[^/\s]+/")),
    ("Windows home path", re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+", re.I)),
    ("UNC path", re.compile(r"\\\\[^\\\s]+\\[^\\\s]+")),
    ("email address", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    ("DOI record", re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)),
    ("SHA-256-like record", re.compile(r"(?<![A-F0-9])[A-F0-9]{64}(?![A-F0-9])", re.I)),
    ("OpenAI-style secret", re.compile(r"\bsk-(?:proj-|svcacct-)?[A-Za-z0-9_-]{16,}\b")),
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("Slack token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{16,}\b")),
    (
        "assigned secret",
        re.compile(
            r"(?im)^\s*(?:api[_-]?key|access[_-]?token|auth[_-]?token|password|secret)"
            r"\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}"
        ),
    ),
    ("private key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("embedded paper hash marker", re.compile(r"paper[-_ ]sha256\s*:", re.I)),
    ("BibTeX record", re.compile(r"(?im)^\s*@(article|book|inproceedings|misc)\s*\{")),
    ("RIS journal record", re.compile(r"(?m)^TY  - JOUR\s*$")),
    ("embedded PDF full-text section", re.compile(r"(?im)^#{1,4}\s+PDF\s+(?:full\s*text|全文)\s*$")),
)


def scan_text(location: str, text: str) -> list[str]:
    findings: list[str] = []
    for label, pattern in CONTENT_RULES:
        match = pattern.search(text)
        if match:
            line = text.count("\n", 0, match.start()) + 1
            findings.append(f"{label}: {location}:{line}")
    bad_controls = [char for char in text if ord(char) < 32 and char not in "\n\r\t"]
    if bad_controls:
        findings.append(f"unexpected control character: {location}")
    return findings


def parse_manifest_text(text: str, location: str) -> tuple[list[str], list[str]]:
    entries: list[str] = []
    findings: list[str] = []
    seen: set[str] = set()
    for line_number, raw in enumerate(text.splitlines(), 1):
        entry = raw.strip()
        if not entry or entry.startswith("#"):
            continue
        path = PurePosixPath(entry)
        if path.is_absolute() or ".." in path.parts or "\\" in entry or entry.endswith("/"):
            findings.append(f"unsafe allowlist entry: {location}:{line_number}")
            continue
        normalized = path.as_posix()
        if normalized in seen:
            findings.append(f"duplicate allowlist entry: {location}:{line_number}")
            continue
        seen.add(normalized)
        entries.append(normalized)
    if MANIFEST_NAME not in seen:
        findings.append(f"allowlist must include itself: {location}")
    return entries, findings


def decode_and_scan(location: str, data: bytes) -> list[str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return [f"non-UTF-8 or binary release file: {location}"]
    return scan_text(location, text)


def audit_directory(
    root: Path,
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES,
) -> list[str]:
    root = root.resolve()
    findings: list[str] = []
    manifest = root / MANIFEST_NAME
    if not manifest.is_file() or manifest.is_symlink():
        return [f"missing regular allowlist file: {MANIFEST_NAME}"]
    try:
        manifest_text = manifest.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"cannot read allowlist: {type(exc).__name__}"]
    allowed, manifest_findings = parse_manifest_text(manifest_text, MANIFEST_NAME)
    findings.extend(manifest_findings)

    actual_files: set[str] = set()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        findings.extend(scan_text(f"filename:{relative}", relative))
        if path.is_symlink():
            findings.append(f"symbolic link is not allowed: {relative}")
        elif path.is_file():
            actual_files.add(relative)

    expected = set(allowed)
    for missing in sorted(expected - actual_files):
        findings.append(f"allowlisted file is missing: {missing}")
    for extra in sorted(actual_files - expected):
        findings.append(f"unlisted file: {extra}")

    total = 0
    for relative in sorted(expected & actual_files):
        path = root / relative
        if path.is_symlink():
            continue
        try:
            data = path.read_bytes()
        except OSError as exc:
            findings.append(f"cannot read release file: {relative} ({type(exc).__name__})")
            continue
        size = len(data)
        total += size
        if size > max_file_bytes:
            findings.append(f"file exceeds size limit ({size} bytes): {relative}")
        findings.extend(decode_and_scan(relative, data))
    if total > max_total_bytes:
        findings.append(f"release exceeds total size limit ({total} bytes)")
    return findings


def _unsafe_zip_name(name: str) -> bool:
    path = PurePosixPath(name)
    return path.is_absolute() or ".." in path.parts or "\\" in name or name.startswith("/")


def _zip_is_symlink(info: zipfile.ZipInfo) -> bool:
    return stat.S_IFMT(info.external_attr >> 16) == stat.S_IFLNK


def audit_zip(
    archive: Path,
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES,
) -> list[str]:
    findings: list[str] = []
    try:
        handle = zipfile.ZipFile(archive, "r")
    except (OSError, zipfile.BadZipFile) as exc:
        return [f"cannot open ZIP: {type(exc).__name__}"]

    with handle:
        if handle.comment:
            findings.append("ZIP comment is not allowed")
        infos = handle.infolist()
        names: set[str] = set()
        file_infos: dict[str, zipfile.ZipInfo] = {}
        for info in infos:
            name = info.filename
            findings.extend(scan_text(f"filename:{name}", name))
            if name in names:
                findings.append(f"duplicate ZIP entry: {name}")
            names.add(name)
            if _unsafe_zip_name(name):
                findings.append(f"unsafe ZIP path: {name}")
            if info.flag_bits & 0x1:
                findings.append(f"encrypted ZIP entry: {name}")
            if _zip_is_symlink(info):
                findings.append(f"symbolic-link ZIP entry: {name}")
            if info.extra:
                findings.append(f"ZIP extra metadata is not allowed: {name}")
            if not info.is_dir():
                file_infos[name] = info

        manifest_candidates = [name for name in file_infos if name.endswith("/" + MANIFEST_NAME)]
        if len(manifest_candidates) != 1:
            findings.append("ZIP must contain exactly one top-level release-files.txt")
            return findings
        manifest_name = manifest_candidates[0]
        root_name = manifest_name[: -len("/" + MANIFEST_NAME)]
        if not root_name or "/" in root_name:
            findings.append("ZIP must contain one top-level package directory")
            return findings
        try:
            manifest_data = handle.read(manifest_name)
            manifest_text = manifest_data.decode("utf-8")
        except (KeyError, UnicodeDecodeError, RuntimeError) as exc:
            findings.append(f"cannot read ZIP allowlist: {type(exc).__name__}")
            return findings
        allowed, manifest_findings = parse_manifest_text(manifest_text, manifest_name)
        findings.extend(manifest_findings)
        expected = {f"{root_name}/{relative}" for relative in allowed}
        actual = set(file_infos)
        for missing in sorted(expected - actual):
            findings.append(f"allowlisted ZIP file is missing: {missing}")
        for extra in sorted(actual - expected):
            findings.append(f"unlisted ZIP file: {extra}")

        total = 0
        for name in sorted(expected & actual):
            info = file_infos[name]
            total += info.file_size
            if info.file_size > max_file_bytes:
                findings.append(f"ZIP file exceeds size limit ({info.file_size} bytes): {name}")
            if info.compress_size and info.file_size > 100_000:
                ratio = info.file_size / info.compress_size
                if ratio > MAX_COMPRESSION_RATIO:
                    findings.append(f"suspicious ZIP compression ratio ({ratio:.1f}): {name}")
            try:
                data = handle.read(info)
            except (RuntimeError, zipfile.BadZipFile) as exc:
                findings.append(f"cannot read ZIP entry: {name} ({type(exc).__name__})")
                continue
            findings.extend(decode_and_scan(name, data))
        if total > max_total_bytes:
            findings.append(f"ZIP exceeds total size limit ({total} bytes)")
        bad_member = handle.testzip()
        if bad_member:
            findings.append(f"ZIP CRC failure: {bad_member}")
    return findings


def audit_target(
    target: Path,
    max_file_bytes: int = DEFAULT_MAX_FILE_BYTES,
    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES,
) -> list[str]:
    if target.is_dir():
        return audit_directory(target, max_file_bytes, max_total_bytes)
    if target.is_file() and target.suffix.casefold() == ".zip":
        return audit_zip(target, max_file_bytes, max_total_bytes)
    return ["target must be a release directory or ZIP file"]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit an allowlisted skill directory or final ZIP for configured leak patterns."
    )
    parser.add_argument("target", nargs="?", default=".", type=Path)
    parser.add_argument("--max-file-bytes", type=int, default=DEFAULT_MAX_FILE_BYTES)
    parser.add_argument("--max-total-bytes", type=int, default=DEFAULT_MAX_TOTAL_BYTES)
    args = parser.parse_args()
    if args.max_file_bytes < 1 or args.max_total_bytes < 1:
        parser.error("size limits must be positive")

    findings = audit_target(args.target, args.max_file_bytes, args.max_total_bytes)
    if findings:
        print("RELEASE AUDIT: FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("RELEASE AUDIT: PASS")
    print("The allowlist, archive structure, and configured leak checks passed.")
    print("This heuristic audit does not prove that arbitrary content is non-sensitive.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
