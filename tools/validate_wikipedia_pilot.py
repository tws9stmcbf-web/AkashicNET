#!/usr/bin/env python3
"""Fail-closed integrity/privacy validation for the public Wikipedia metadata pilot.

This validates discovery/reference metadata only. Passing this check does not promote
work identity, edition identity, rights/public status, truth, scientific-evidence,
safety, or efficacy state.
"""

from __future__ import annotations

import csv
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

PILOT = Path("references/community/wikipedia-akashic-pilot.csv")
EXPECTED_FIELDS = [
    "source",
    "page_id",
    "title",
    "topic_seed",
    "url",
    "retrieved_utc",
]
ALLOWED_TOPICS = {
    "consciousness",
    "neuroscience",
    "meditation",
    "psychedelics",
    "panpsychism",
    "philosophy of mind",
    "quantum physics",
    "cosmology",
    "archaeology",
    "anthropology",
    "mycology",
    "artificial intelligence",
}
FORBIDDEN_FIELDS = {
    "drive_id",
    "file_id",
    "filename",
    "path",
    "sha256",
    "digest",
    "created_time",
    "modified_time",
    "mime_type",
    "size_bytes",
}
EXPECTED_ROWS = 100


def fail(message: str) -> None:
    raise ValueError(message)


def validate(path: Path = PILOT) -> int:
    if not path.is_file():
        fail(f"missing pilot CSV: {path}")

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != EXPECTED_FIELDS:
            fail(f"unexpected columns: {reader.fieldnames!r}")
        if FORBIDDEN_FIELDS.intersection(reader.fieldnames or []):
            fail("private/object-level metadata column present")
        rows = list(reader)

    if len(rows) != EXPECTED_ROWS:
        fail(f"expected {EXPECTED_ROWS} rows, found {len(rows)}")

    seen_page_ids: set[str] = set()
    seen_urls: set[str] = set()

    for line_no, row in enumerate(rows, start=2):
        if any(value is None or not value.strip() for value in row.values()):
            fail(f"line {line_no}: blank value")
        if row["source"] != "Wikipedia":
            fail(f"line {line_no}: unexpected source")
        if not row["page_id"].isdigit() or int(row["page_id"]) <= 0:
            fail(f"line {line_no}: invalid public Wikipedia page_id")
        if row["page_id"] in seen_page_ids:
            fail(f"line {line_no}: duplicate page_id")
        seen_page_ids.add(row["page_id"])

        if row["topic_seed"] not in ALLOWED_TOPICS:
            fail(f"line {line_no}: unexpected topic_seed")

        parsed = urlparse(row["url"])
        if parsed.scheme != "https" or parsed.netloc != "en.wikipedia.org":
            fail(f"line {line_no}: non-English-Wikipedia URL")
        if not parsed.path.startswith("/wiki/") or not parsed.path.removeprefix("/wiki/"):
            fail(f"line {line_no}: invalid article URL path")
        if parsed.params or parsed.query or parsed.fragment:
            fail(f"line {line_no}: URL must be canonical article form")
        if row["url"] in seen_urls:
            fail(f"line {line_no}: duplicate URL")
        seen_urls.add(row["url"])

        try:
            timestamp = datetime.fromisoformat(row["retrieved_utc"].replace("Z", "+00:00"))
        except ValueError as exc:
            fail(f"line {line_no}: invalid retrieved_utc: {exc}")
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            fail(f"line {line_no}: retrieved_utc must be timezone-aware")

    return len(rows)


def main() -> int:
    try:
        count = validate()
    except (OSError, ValueError) as exc:
        print(f"Wikipedia pilot validation FAILED: {exc}", file=sys.stderr)
        return 1

    print(f"Wikipedia pilot validation passed: {count} public reference rows")
    print("Epistemic status unchanged: discovery/reference metadata only")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
