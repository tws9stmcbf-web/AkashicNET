#!/usr/bin/env python3
"""Validate a private SHA-256 duplicate-adjudication batch without exposing row data.

The validator is intentionally generic. Private manifests should live under an ignored
path such as references/private/ and must never be committed to the public repo.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import re
from collections import Counter, defaultdict
from pathlib import Path

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
REQUIRED = {
    "candidate_family_id",
    "drive_id",
    "size_bytes",
    "sha256",
    "family_result",
    "work_identity_status",
    "rights_state",
    "scientific_evidence_state",
}


def validate_rows(rows, expected_families=None, expected_objects=None, expected_verified=None):
    if not rows:
        raise AssertionError("hash batch is empty")
    missing = REQUIRED - set(rows[0])
    if missing:
        raise AssertionError(f"missing required columns: {sorted(missing)}")

    by_family = defaultdict(list)
    seen_objects = set()
    for row in rows:
        fid = row["candidate_family_id"].strip()
        oid = row["drive_id"].strip()
        digest = row["sha256"].strip().lower()
        if not fid or not oid:
            raise AssertionError("blank family/object identifier")
        if oid in seen_objects:
            raise AssertionError("duplicate physical-object identifier in batch")
        seen_objects.add(oid)
        if not SHA256_RE.fullmatch(digest):
            raise AssertionError("invalid SHA-256 digest")
        if int(row["size_bytes"]) < 0:
            raise AssertionError("negative object size")
        if row["work_identity_status"] != "HOLD_PENDING_WORK_ADJUDICATION":
            raise AssertionError("hash batch must not promote work identity")
        if row["rights_state"] != "UNKNOWN_UNVERIFIED":
            raise AssertionError("hash batch must not promote rights state")
        if row["scientific_evidence_state"] != "NOT_EVALUATED":
            raise AssertionError("hash batch must not promote scientific-evidence state")
        by_family[fid].append(row)

    family_states = Counter()
    for group in by_family.values():
        stated = {r["family_result"] for r in group}
        if len(stated) != 1:
            raise AssertionError("inconsistent family result")
        state = next(iter(stated))
        digests = {r["sha256"].lower() for r in group}
        if state == "BYTE_IDENTICAL_VERIFIED":
            if len(group) < 2 or len(digests) != 1:
                raise AssertionError("verified family lacks complete SHA-256 agreement")
        elif state == "NOT_BYTE_IDENTICAL":
            if len(digests) < 2:
                raise AssertionError("mismatch family does not contain differing hashes")
        else:
            raise AssertionError("unsupported family result")
        family_states[state] += 1

    if expected_families is not None and len(by_family) != expected_families:
        raise AssertionError("unexpected family count")
    if expected_objects is not None and len(rows) != expected_objects:
        raise AssertionError("unexpected object count")
    if expected_verified is not None and family_states["BYTE_IDENTICAL_VERIFIED"] != expected_verified:
        raise AssertionError("unexpected verified-family count")

    return {
        "families": len(by_family),
        "objects": len(rows),
        "bytes": sum(int(r["size_bytes"]) for r in rows),
        "verified": family_states["BYTE_IDENTICAL_VERIFIED"],
        "mismatched": family_states["NOT_BYTE_IDENTICAL"],
    }


def self_test():
    digest_a = hashlib.sha256(b"same bytes").hexdigest()
    digest_b = hashlib.sha256(b"different bytes").hexdigest()
    data = f"""candidate_family_id,drive_id,size_bytes,sha256,family_result,work_identity_status,rights_state,scientific_evidence_state
SYNTH-1,OBJ-1,10,{digest_a},BYTE_IDENTICAL_VERIFIED,HOLD_PENDING_WORK_ADJUDICATION,UNKNOWN_UNVERIFIED,NOT_EVALUATED
SYNTH-1,OBJ-2,10,{digest_a},BYTE_IDENTICAL_VERIFIED,HOLD_PENDING_WORK_ADJUDICATION,UNKNOWN_UNVERIFIED,NOT_EVALUATED
SYNTH-2,OBJ-3,10,{digest_a},NOT_BYTE_IDENTICAL,HOLD_PENDING_WORK_ADJUDICATION,UNKNOWN_UNVERIFIED,NOT_EVALUATED
SYNTH-2,OBJ-4,10,{digest_b},NOT_BYTE_IDENTICAL,HOLD_PENDING_WORK_ADJUDICATION,UNKNOWN_UNVERIFIED,NOT_EVALUATED
"""
    rows = list(csv.DictReader(io.StringIO(data)))
    result = validate_rows(rows, expected_families=2, expected_objects=4, expected_verified=1)
    assert result == {"families": 2, "objects": 4, "bytes": 40, "verified": 1, "mismatched": 1}
    print("private hash batch validator self-test PASS")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="?", type=Path)
    ap.add_argument("--expected-families", type=int)
    ap.add_argument("--expected-objects", type=int)
    ap.add_argument("--expected-verified", type=int)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        return 0
    if not args.csv:
        ap.error("csv path is required unless --self-test is used")

    with args.csv.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    result = validate_rows(rows, args.expected_families, args.expected_objects, args.expected_verified)
    # Print aggregates only; never echo identifiers, filenames, paths or digests.
    print("private hash batch validation PASS")
    print("families={families} objects={objects} bytes={bytes} verified={verified} mismatched={mismatched}".format(**result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
