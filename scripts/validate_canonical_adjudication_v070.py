#!/usr/bin/env python3

"""Fail-closed validator for AkashicNET canonical adjudication records v0.7.0."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ALLOWED_STATES = {"ACCEPT", "HOLD", "REJECT"}
ALLOWED_RELATIONSHIPS = {
    "REPRESENTS_WORK",
    "REPRESENTS_EDITION",
    "DUPLICATE_COPY_OF",
    "TRANSLATION_OF",
    "DERIVED_FROM",
}
FORBIDDEN_PRIVATE_FIELDS = {
    "drive_id",
    "file_id",
    "private_filename",
    "private_path",
    "private_timestamp",
    "private_size",
    "sha256",
    "object_hash",
    "access_token",
}
INDEPENDENT_PROMOTIONS = {
    "rights_promoted",
    "public_release_promoted",
    "scientific_evidence_promoted",
    "safety_or_efficacy_promoted",
}


def fail(message: str) -> None:
    raise ValueError(message)


def validate_record(record: dict, index: int) -> None:
    if not isinstance(record, dict):
        fail(f"record {index}: expected object")

    forbidden = FORBIDDEN_PRIVATE_FIELDS.intersection(record)
    if forbidden:
        fail(f"record {index}: forbidden private fields: {sorted(forbidden)}")

    state = record.get("decision")
    if state not in ALLOWED_STATES:
        fail(f"record {index}: invalid decision {state!r}")

    relationship = record.get("relationship")
    if relationship not in ALLOWED_RELATIONSHIPS:
        fail(f"record {index}: invalid relationship {relationship!r}")

    rationale = record.get("rationale")
    if state in {"ACCEPT", "REJECT"} and not isinstance(rationale, str):
        fail(f"record {index}: {state} requires rationale")
    if state in {"ACCEPT", "REJECT"} and not rationale.strip():
        fail(f"record {index}: {state} rationale must not be empty")

    evidence_class = record.get("evidence_class")
    if state in {"ACCEPT", "REJECT"} and not isinstance(evidence_class, str):
        fail(f"record {index}: {state} requires evidence_class")
    if state in {"ACCEPT", "REJECT"} and not evidence_class.strip():
        fail(f"record {index}: {state} evidence_class must not be empty")

    for field in INDEPENDENT_PROMOTIONS:
        value = record.get(field, False)
        if value is not False:
            fail(f"record {index}: {field} must remain false in canonical adjudication")

    signals = set(record.get("signals", []))
    if state == "ACCEPT" and signals and signals.issubset(
        {"SHA256_EQUAL", "FILENAME", "PATH", "SIZE", "TIMESTAMP", "LEXICAL_OVERLAP", "SEMANTIC_SIMILARITY"}
    ):
        fail(f"record {index}: ACCEPT cannot rely only on nomination/byte-identity signals")

    if state == "ACCEPT":
        provenance = record.get("provenance")
        if not isinstance(provenance, list) or not provenance:
            fail(f"record {index}: ACCEPT requires non-empty provenance")


def validate_payload(payload: dict) -> None:
    if not isinstance(payload, dict):
        fail("top-level payload must be an object")
    if payload.get("contract_version") != "0.7.0":
        fail("contract_version must be 0.7.0")
    records = payload.get("records")
    if not isinstance(records, list):
        fail("records must be a list")
    for index, record in enumerate(records):
        validate_record(record, index)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_canonical_adjudication_v070.py <json-file>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        validate_payload(payload)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"CANONICAL ADJUDICATION FAIL: {exc}", file=sys.stderr)
        return 1

    print("CANONICAL ADJUDICATION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
