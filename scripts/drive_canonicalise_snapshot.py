#!/usr/bin/env python3
"""Build a conservative object-level canonicalisation baseline from a frozen Drive census.

This script deliberately does not infer canonical-work or byte identity from metadata.
Exact filename + size is only a review signal.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

EXPECTED_OBJECTS = 2459


def technical_reason(row: dict[str, str]) -> str:
    name = row["name"].casefold()
    try:
        size = int(row.get("size") or 0)
    except ValueError:
        size = 0
    if size == 0:
        return "ZERO_BYTE"
    if name == ".ds_store":
        return "DS_STORE"
    if name.endswith(".crdownload"):
        return "CRDOWNLOAD"
    return ""


def family_id(name: str, size: str) -> str:
    digest = hashlib.sha256((name + "\0" + str(size)).encode("utf-8")).hexdigest()[:12]
    return "DUP-" + digest.upper()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("references/community"))
    args = parser.parse_args()

    with args.input_csv.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    required = {"root_title", "parent_path", "parent_drive_id", "drive_id", "name", "mime_type", "size"}
    if not rows or not required.issubset(rows[0]):
        raise SystemExit("Input is not the v0.5.0 live object census")
    if len(rows) != EXPECTED_OBJECTS:
        raise SystemExit(f"Frozen snapshot mismatch: expected {EXPECTED_OBJECTS}, got {len(rows)}")
    if len({row["drive_id"] for row in rows}) != EXPECTED_OBJECTS:
        raise SystemExit("Drive IDs are not unique across the frozen snapshot")

    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[(row["name"], row["size"])].append(row)

    duplicate_groups = {key: members for key, members in groups.items() if len(members) > 1}
    family_ids = {key: family_id(*key) for key in duplicate_groups}

    ledger = []
    for row in rows:
        reason = technical_reason(row)
        fid = family_ids.get((row["name"], row["size"]), "")
        if reason:
            disposition = "TECHNICAL_EXCLUSION"
            review_state = "CLOSED"
            decision_basis = reason
        elif fid:
            disposition = "REVIEW_REQUIRED"
            review_state = "OPEN"
            decision_basis = "EXACT_NAME_SIZE_CANDIDATE_ONLY"
        else:
            disposition = "UNIQUE_CANDIDATE"
            review_state = "OPEN"
            decision_basis = "NO_EXACT_NAME_SIZE_PEER"

        ledger.append({
            "manifestation_id": "drive:file:" + row["drive_id"],
            "drive_id": row["drive_id"],
            "parent_path": row["parent_path"],
            "name": row["name"],
            "size": row["size"],
            "disposition": disposition,
            "candidate_family_id": fid,
            "review_state": review_state,
            "canonical_work_id": "",
            "edition_id": "",
            "decision_basis": decision_basis,
        })

    families = []
    for (name, size), members in sorted(duplicate_groups.items(), key=lambda item: (-len(item[1]), item[0][0])):
        all_technical = all(bool(technical_reason(member)) for member in members)
        families.append({
            "candidate_family_id": family_ids[(name, size)],
            "name": name,
            "size": size,
            "object_count": len(members),
            "review_state": "CLOSED_TECHNICAL" if all_technical else "REVIEW_REQUIRED",
            "promotion_status": "NONE",
            "evidence_basis": "exact filename + size only",
            "notes": "Technical artefact family." if all_technical else "No byte identity or same-work assertion without stronger evidence.",
        })

    args.out_dir.mkdir(parents=True, exist_ok=True)
    ledger_path = args.out_dir / "drive-canonical-object-ledger-v0.6.0.csv"
    family_path = args.out_dir / "drive-canonical-family-review-v0.6.0.csv"
    summary_path = args.out_dir / "drive-canonical-baseline-v0.6.0.json"

    with ledger_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=ledger[0].keys())
        writer.writeheader()
        writer.writerows(ledger)

    with family_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=families[0].keys())
        writer.writeheader()
        writer.writerows(families)

    summary = {
        "schema_version": "0.6.0",
        "source_snapshot_objects": len(rows),
        "unique_drive_ids": len({row["drive_id"] for row in rows}),
        "dispositions": dict(Counter(item["disposition"] for item in ledger)),
        "technical_reasons": dict(Counter(technical_reason(row) for row in rows if technical_reason(row))),
        "exact_name_size_families": len(families),
        "objects_in_exact_name_size_families": sum(int(item["object_count"]) for item in families),
        "nontechnical_review_families": sum(item["review_state"] == "REVIEW_REQUIRED" for item in families),
        "canonical_work_ids_promoted": 0,
        "edition_ids_promoted": 0,
        "guardrail": "Metadata similarity is a review signal, not proof of byte identity or canonical-work identity.",
    }
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    assert summary["dispositions"] == {
        "UNIQUE_CANDIDATE": 2173,
        "TECHNICAL_EXCLUSION": 28,
        "REVIEW_REQUIRED": 258,
    }
    assert summary["technical_reasons"] == {"DS_STORE": 11, "ZERO_BYTE": 16, "CRDOWNLOAD": 1}
    assert summary["exact_name_size_families"] == 127
    assert summary["objects_in_exact_name_size_families"] == 269
    assert summary["nontechnical_review_families"] == 126

    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
