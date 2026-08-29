#!/usr/bin/env python3
"""Hash the six P0 canonical-review families directly from Google Drive.

Safety boundaries:
- only families selected as P0_MULTIPLICITY are downloaded;
- SHA-256 equality establishes byte identity for the compared Drive objects only;
- no canonical work, edition, rights, or scientific-evidence promotion occurs here;
- authentication exception bodies are never persisted or printed.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references" / "community"
FAMILY_LEDGER = REF / "drive-canonical-family-review-v0.6.0.csv"
OBJECT_LEDGER = REF / "drive-canonical-object-ledger-v0.6.0.csv"
RESULTS = REF / "drive-p0-hash-results-v0.6.3.csv"
SUMMARY = REF / "drive-p0-hash-summary-v0.6.3.json"

EXPECTED_FAMILIES = 6
EXPECTED_OBJECTS = 18
EXPECTED_BYTES = 14838834


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def download_and_hash(token: str, drive_id: str) -> tuple[str, int]:
    params = urllib.parse.urlencode({"alt": "media", "supportsAllDrives": "true"})
    url = f"https://www.googleapis.com/drive/v3/files/{urllib.parse.quote(drive_id, safe='')}?{params}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    h = hashlib.sha256()
    n = 0
    with urllib.request.urlopen(req, timeout=90) as resp:
        while True:
            chunk = resp.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
            n += len(chunk)
    return h.hexdigest(), n


def main() -> int:
    token = os.environ.get("GOOGLE_DRIVE_ACCESS_TOKEN")
    if not token:
        print("GOOGLE_DRIVE_ACCESS_TOKEN is required", file=sys.stderr)
        return 2

    families = read_csv(FAMILY_LEDGER)
    objects = read_csv(OBJECT_LEDGER)
    members = defaultdict(list)
    for obj in objects:
        fid = obj.get("candidate_family_id", "")
        if fid:
            members[fid].append(obj)

    p0 = []
    for fam in families:
        if fam.get("review_state") != "REVIEW_REQUIRED":
            continue
        count = int(fam["object_count"])
        if count >= 3:
            p0.append(fam)

    assert len(p0) == EXPECTED_FAMILIES, f"expected {EXPECTED_FAMILIES} P0 families, got {len(p0)}"
    assert sum(int(f["object_count"]) for f in p0) == EXPECTED_OBJECTS
    assert sum(int(f["size"]) * int(f["object_count"]) for f in p0) == EXPECTED_BYTES

    rows = []
    family_hashes = defaultdict(list)
    failures = 0

    for fam in sorted(p0, key=lambda r: (int(r["size"]) * int(r["object_count"]), r["candidate_family_id"])):
        fid = fam["candidate_family_id"]
        group = sorted(members[fid], key=lambda r: r["drive_id"])
        assert len(group) == int(fam["object_count"])
        for obj in group:
            expected_size = int(obj["size"])
            try:
                digest, actual_size = download_and_hash(token, obj["drive_id"])
                status = "HASHED" if actual_size == expected_size else "SIZE_MISMATCH"
                if status != "HASHED":
                    failures += 1
                family_hashes[fid].append(digest)
            except Exception as exc:
                # Do not expose OAuth/provider response bodies in logs or artifacts.
                digest = ""
                actual_size = 0
                status = f"ERROR_{type(exc).__name__}"
                failures += 1
            rows.append({
                "candidate_family_id": fid,
                "name": fam["name"],
                "drive_id": obj["drive_id"],
                "parent_path": obj["parent_path"],
                "expected_size_bytes": expected_size,
                "downloaded_size_bytes": actual_size,
                "sha256": digest,
                "hash_status": status,
            })

    family_results = {}
    for fam in p0:
        fid = fam["candidate_family_id"]
        hashes = family_hashes.get(fid, [])
        expected = int(fam["object_count"])
        if len(hashes) != expected or any(not h for h in hashes):
            result = "UNRESOLVED_HASH_ERROR"
        elif len(set(hashes)) == 1:
            result = "BYTE_IDENTICAL_VERIFIED"
        else:
            result = "NOT_BYTE_IDENTICAL"
        family_results[fid] = result

    for row in rows:
        row["family_byte_identity_status"] = family_results[row["candidate_family_id"]]
        row["canonical_promotion_status"] = "HOLD_PENDING_WORK_ADJUDICATION"
        row["rights_state"] = "UNKNOWN_UNVERIFIED"
        row["scientific_evidence_state"] = "NOT_EVALUATED"

    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "candidate_family_id", "name", "drive_id", "parent_path",
        "expected_size_bytes", "downloaded_size_bytes", "sha256", "hash_status",
        "family_byte_identity_status", "canonical_promotion_status",
        "rights_state", "scientific_evidence_state",
    ]
    with RESULTS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    counts = defaultdict(int)
    for result in family_results.values():
        counts[result] += 1
    summary = {
        "version": "0.6.3",
        "p0_families": len(p0),
        "p0_objects": len(rows),
        "expected_bytes": EXPECTED_BYTES,
        "hash_failures": failures,
        "family_results": dict(sorted(counts.items())),
        "work_ids_promoted": 0,
        "edition_ids_promoted": 0,
        "rights_promoted": 0,
        "scientific_evidence_promoted": 0,
        "guardrail": "SHA-256 equality proves byte identity for compared objects only; canonical work identity remains separately adjudicated.",
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
