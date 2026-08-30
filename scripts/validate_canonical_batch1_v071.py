#!/usr/bin/env python3

"""Batch-specific checks for canonical adjudication batch 1 v0.7.1."""

from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED_IDS = {
    "work:alice-a-bailey-discipleship-new-age-vol-1",
    "work:alice-a-bailey-discipleship-new-age-vol-2",
    "work:franz-bardon-golden-book-of-wisdom",
}


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_canonical_batch1_v071.py <json-file>", file=sys.stderr)
        return 2

    try:
        payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        records = payload.get("records", [])
        if payload.get("batch_version") != "0.7.1":
            fail("batch_version must be 0.7.1")
        if len(records) != 3:
            fail("batch must contain exactly three records")
        ids = {record.get("candidate_id") for record in records}
        if ids != EXPECTED_IDS:
            fail("unexpected candidate set")
        for record in records:
            if record.get("decision") != "ACCEPT":
                fail("all batch-1 records must be ACCEPT")
            if record.get("relationship") != "REPRESENTS_WORK":
                fail("all batch-1 records must be REPRESENTS_WORK")
            if record.get("evidence_class") != "INDEPENDENT_PUBLIC_BIBLIOGRAPHY":
                fail("all batch-1 records require independent public bibliography")
            if record.get("contradictory_evidence_checked") is not True:
                fail("contradictory evidence check must be explicit")
            provenance = record.get("provenance", [])
            if not provenance or not all(str(p.get("reference", "")).startswith("https://") for p in provenance):
                fail("public HTTPS provenance is required")
            for field in (
                "rights_promoted",
                "public_release_promoted",
                "scientific_evidence_promoted",
                "safety_or_efficacy_promoted",
            ):
                if record.get(field) is not False:
                    fail(f"{field} must remain false")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"CANONICAL BATCH 1 FAIL: {exc}", file=sys.stderr)
        return 1

    print("CANONICAL BATCH 1 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
