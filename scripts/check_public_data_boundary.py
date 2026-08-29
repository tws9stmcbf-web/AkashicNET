#!/usr/bin/env python3
"""Fail when private Drive corpus metadata enters the public repository."""

from __future__ import annotations

import csv
import fnmatch
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

LIVE_DRIVE_URL = re.compile(
    r"https://(?:drive\.google\.com/(?:drive/(?:u/\d+/)?folders|file/d)|"
    r"docs\.google\.com/[^/]+/d)/[A-Za-z0-9_-]{20,}"
)
EMBEDDED_DRIVE_ID = re.compile(r"drive:(?:file|folder):[A-Za-z0-9_-]{20,}")


def tracked_files() -> list[Path]:
    output = subprocess.check_output(["git", "ls-files", "-z"])
    return [Path(item) for item in output.decode().split("\0") if item and Path(item).is_file()]


def main() -> int:
    violations: list[str] = []

    for path in tracked_files():
        name = path.as_posix()
        if any(fnmatch.fnmatch(name, pattern) for pattern in PRIVATE_PATH_PATTERNS):
            violations.append(f"private data path is tracked: {name}")
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue

        if LIVE_DRIVE_URL.search(text):
            violations.append(f"live Drive URL found: {name}")
        if EMBEDDED_DRIVE_ID.search(text):
            violations.append(f"embedded Drive ID found: {name}")

        if path.suffix.lower() == ".csv":
            try:
                header = next(csv.reader(text.splitlines()), [])
            except csv.Error:
                header = []
            exposed = SENSITIVE_CSV_COLUMNS.intersection(cell.strip() for cell in header)
            if exposed:
                violations.append(
                    f"sensitive CSV columns {sorted(exposed)} found: {name}"
                )
            if name == "references/community/akashic-master-index.csv":
                for line_number, row in enumerate(csv.DictReader(text.splitlines()), 2):
                    if row.get("source", "").strip().lower() == "google drive":
                        violations.append(
                            f"Drive-derived master-index row found: {name}:{line_number}"
                        )
                        break

    if violations:
        print("PUBLIC DATA BOUNDARY: FAIL")
        for violation in violations:
            print(f"- {violation}")
        return 1

    print("PUBLIC DATA BOUNDARY: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
