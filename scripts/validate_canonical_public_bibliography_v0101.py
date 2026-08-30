#!/usr/bin/env python3

"""Validate the single-candidate public-bibliography adjudication for Issue #69."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

EXPECTED_IDS = [
    "CANON-B2-ABRAMELIN",
    "CANON-B2-FORBIDDEN-HISTORY",
    "CANON-B2-AGRIPPA",
    "CANON-B2-BARDON-VARIANTS",
    "CANON-B2-RAMAYANA",
    "CANON-B2-VIVEKANANDA",
]
FORBIDDEN_PRIVATE_FIELDS = {
    "drive_id", "file_id", "private_filename", "private_path",
    "private_timestamp", "private_size", "sha256", "object_hash", "access_token",
}
NON_PROMOTIONS = (
    "rights_promoted", "public_release_promoted",
    "scientific_evidence_promoted", "safety_or_efficacy_promoted",
)


def fail(message: str) -> None:
    raise ValueError(message)


def walk_forbidden(value, path="root") -> None:
    if isinstance(value, dict):
        forbidden = FORBIDDEN_PRIVATE_FIELDS.intersection(value)
        if forbidden:
            fail(f"{path}: forbidden private fields: {sorted(forbidden)}")
        for key, child in value.items():
            walk_forbidden(child, f"{path}.{key}")
    elif isinstance(value, list):
        for i, child in enumerate(value):
            walk_forbidden(child, f"{path}[{i}]")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_canonical_public_bibliography_v0101.py <json-file>", file=sys.stderr)
        return 2

    try:
        payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
        walk_forbidden(payload)

        if payload.get("contract_version") != "0.7.0":
            fail("contract_version must remain 0.7.0")
        if payload.get("checkpoint_version") != "0.10.1":
            fail("checkpoint_version must be 0.10.1")
        rule = payload.get("selection_rule", "")
        if "first candidate" not in rule or "CANON-B2-ABRAMELIN" not in rule:
            fail("deterministic selection rule must select the first HOLD: CANON-B2-ABRAMELIN")

        records = payload.get("records")
        if not isinstance(records, list) or len(records) != 6:
            fail("checkpoint must contain exactly six batch-2 records")
        if [r.get("candidate_id") for r in records] != EXPECTED_IDS:
            fail("candidate order/identity must remain identical to batch 2")

        accepts = [r for r in records if r.get("decision") == "ACCEPT"]
        holds = [r for r in records if r.get("decision") == "HOLD"]
        if len(accepts) != 1 or len(holds) != 5:
            fail("checkpoint must contain exactly one ACCEPT and five HOLD decisions")

        record = accepts[0]
        if record.get("candidate_id") != "CANON-B2-ABRAMELIN":
            fail("only CANON-B2-ABRAMELIN may be promoted")
        if record.get("relationship") != "REPRESENTS_WORK":
            fail("Abramelin promotion is scoped only to REPRESENTS_WORK")
        tested = record.get("tested_relationship", "")
        for required in ("Mathers", "Dehn", "Guth", "distinct translations/editions/manifestations"):
            if required not in tested:
                fail(f"tested relationship must preserve scope marker: {required}")
        if record.get("evidence_class") != "REPRODUCIBLE_PUBLIC_BIBLIOGRAPHY":
            fail("Abramelin ACCEPT must use reproducible public bibliography")

        provenance = record.get("provenance")
        if not isinstance(provenance, list) or len(provenance) < 2:
            fail("Abramelin ACCEPT requires at least two public bibliographic sources")
        authorities = {p.get("authority") for p in provenance}
        if len(authorities) < 2:
            fail("bibliographic sources must come from at least two independent authorities")
        for source in provenance:
            if not source.get("record_id") or not source.get("bibliographic_fact"):
                fail("every source requires record_id and bibliographic_fact")
            parsed = urlparse(source.get("url", ""))
            if parsed.scheme != "https" or not parsed.netloc:
                fail("every source must have a stable public HTTPS URL")

        for i, item in enumerate(records):
            for field in NON_PROMOTIONS:
                if item.get(field) is not False:
                    fail(f"record {i}: {field} must remain false")

        if any(r.get("decision") != "HOLD" for r in records[1:]):
            fail("the other five batch-2 candidates must remain HOLD")

    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"CANONICAL PUBLIC BIBLIOGRAPHY FAIL: {exc}", file=sys.stderr)
        return 1

    print("CANONICAL PUBLIC BIBLIOGRAPHY PASS: 1 ACCEPT, 5 HOLD; semantic promotions remain off")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
