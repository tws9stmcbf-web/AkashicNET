#!/usr/bin/env python3

"""Focused validator for canonical adjudication batch 2 v0.7.2."""

from __future__ import annotations

import json
import sys
from pathlib import Path

EXPECTED_IDS = {
    "CANON-B2-ABRAMELIN",
    "CANON-B2-FORBIDDEN-HISTORY",
    "CANON-B2-AGRIPPA",
    "CANON-B2-BARDON-VARIANTS",
    "CANON-B2-RAMAYANA",
    "CANON-B2-VIVEKANANDA",
}


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_canonical_batch2_v072.py <json-file>", file=sys.stderr)
        return 2

    try:
        payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        if payload.get("contract_version") != "0.7.0":
            fail("contract_version must remain 0.7.0")
        records = payload.get("records")
        if not isinstance(records, list) or len(records) != 6:
            fail("batch 2 must contain exactly six records")
        ids = {r.get("candidate_id") for r in records}
        if ids != EXPECTED_IDS:
            fail("unexpected or missing batch 2 candidate IDs")
        if any(r.get("decision") != "HOLD" for r in records):
            fail("all batch 2 decisions must remain HOLD")
        if sum(1 for r in records if r.get("relationship") == "REPRESENTS_EDITION") != 1:
            fail("exactly one batch 2 record must test edition identity")
        for i, record in enumerate(records):
            if not record.get("rationale"):
                fail(f"record {i}: HOLD rationale required in this batch")
            for field in (
                "rights_promoted",
                "public_release_promoted",
                "scientific_evidence_promoted",
                "safety_or_efficacy_promoted",
            ):
                if record.get(field) is not False:
                    fail(f"record {i}: {field} must remain false")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"CANONICAL BATCH 2 FAIL: {exc}", file=sys.stderr)
        return 1

    print("CANONICAL BATCH 2 PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
