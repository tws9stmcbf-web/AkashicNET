#!/usr/bin/env python3
"""Fail when private Drive corpus metadata enters the public repository."""

from __future__ import annotations

import csv
import fnmatch
import json
import re
import subprocess
from pathlib import Path


PRIVATE_PATH_PATTERNS = (
    "references/akashic-library/*.csv",
    "references/akashic-library/AKASHIC_LIBRARY_INDEX.md",
    "references/community/drive-*.csv",
    "references/community/hash-verification-*.csv",
    "references/community/canonical-graph-promotions-*.csv",
    "references/community/canonical-promotion-decisions-*.csv",
    "references/community/canonical-work-registry-*.csv",
    "references/community/canonical-review-queue-*.csv",
    "references/community/canonical-review-plan-*.md",
    "references/community/*manifestation*review*.csv",
    "data/knowledge-graph-v0.*.json",
    "data/dedup-retrieval-view-v0.*.json",
)

SENSITIVE_CSV_COLUMNS = {
    "drive_id",
    "drive_ids",
    "parent_drive_id",
    "drive_object_id",
    "source_drive_id",
    "target_drive_id",
    "drive_url",
    "drive_folder_url",
}
SENSITIVE_JSON_ID_KEYS = {
    "drive_id",
    "drive_ids",
    "parent_drive_id",
    "drive_object_id",
    "source_drive_id",
    "target_drive_id",
}

LIVE_DRIVE_URL = re.compile(
    r"https://(?:drive\.google\.com/(?:drive/(?:u/\d+/)?folders|file/d)|"
    r"docs\.google\.com/[^/]+/d)/[A-Za-z0-9_-]{20,}"
)
EMBEDDED_DRIVE_ID = re.compile(r"drive:(?:file|folder):[A-Za-z0-9_-]{20,}")
OPAQUE_PROVIDER_ID = re.compile(r"^[A-Za-z0-9_-]{20,}$")


def tracked_files() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files", "-z"])
    return [Path(item) for item in output.decode().split("\0") if item and Path(item).is_file()]


def _contains_opaque_provider_id(value: object) -> bool:
    if isinstance(value, str):
        return bool(OPAQUE_PROVIDER_ID.fullmatch(value.strip()))
    if isinstance(value, list):
        return any(_contains_opaque_provider_id(item) for item in value)
    return False


def _find_sensitive_json_ids(value: object, path: str = "$") -> list[str]:
    findings: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            child = f"{path}.{key}"
            if key in SENSITIVE_JSON_ID_KEYS and _contains_opaque_provider_id(item):
                findings.append(child)
            findings.extend(_find_sensitive_json_ids(item, child))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            findings.extend(_find_sensitive_json_ids(item, f"{path}[{index}]"))
    return findings


def validate_entry(name: str, text: str | None) -> list[str]:
    """Return privacy-boundary violations for one tracked repository entry.

    `text=None` is allowed so path-level rules can still fail closed for binary or
    unreadable files. Tests use this callable surface with synthetic, non-secret
    fixtures rather than private corpus material.
    """
    violations: list[str] = []

    if any(fnmatch.fnmatch(name, pattern) for pattern in PRIVATE_PATH_PATTERNS):
        return [f"private data path is tracked: {name}"]

    if text is None:
        return violations

    if LIVE_DRIVE_URL.search(text):
        violations.append(f"live Drive URL found: {name}")
    if EMBEDDED_DRIVE_ID.search(text):
        violations.append(f"embedded Drive ID found: {name}")

    if name.lower().endswith(".json"):
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            payload = None
        if payload is not None:
            findings = _find_sensitive_json_ids(payload)
            if findings:
                violations.append(f"opaque Drive object ID found in JSON fields {findings}: {name}")

    if name.lower().endswith(".csv"):
        try:
            header = next(csv.reader(text.splitlines()), [])
        except csv.Error:
            header = []
        exposed = SENSITIVE_CSV_COLUMNS.intersection(cell.strip() for cell in header)
        if exposed:
            violations.append(f"sensitive CSV columns {sorted(exposed)} found: {name}")
        if name == "references/community/akashic-master-index.csv":
            for line_number, row in enumerate(csv.DictReader(text.splitlines()), 2):
                if row.get("source", "").strip().lower() == "google drive":
                    violations.append(f"Drive-derived master-index row found: {name}:{line_number}")
                    break

    return violations


def validate_entries(entries: list[tuple[str, str | None]]) -> list[str]:
    violations: list[str] = []
    for name, text in entries:
        violations.extend(validate_entry(name, text))
    return violations


def main() -> int:
    entries: list[tuple[str, str | None]] = []

    for path in tracked_files():
        name = path.as_posix()
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            text = None
        entries.append((name, text))

    violations = validate_entries(entries)
    if violations:
        print("PUBLIC DATA BOUNDARY: FAIL")
        for violation in violations:
            print(f"- {violation}")
        return 1

    print("PUBLIC DATA BOUNDARY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
