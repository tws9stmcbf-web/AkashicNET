#!/usr/bin/env python3
"""Stage-1 canonical corpus resolver for the live Drive census.

This script is deliberately conservative. It assigns stable manifestation IDs,
creates exact-metadata duplicate candidate families, preserves deterministic
technical exclusions, and leaves canonical_work_id blank until equivalence is
actually proven by later review or stronger evidence (for example hashing,
ISBN/edition metadata, or manual adjudication).
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

INPUT = Path("references/community/drive-live-full-object-census.csv")
LEDGER = Path("references/community/drive-canonical-resolution-ledger-v0.5.1.csv")
FAMILIES = Path("references/community/drive-canonical-candidate-families-v0.5.1.csv")
SUMMARY = Path("references/community/drive-canonical-resolution-summary-v0.5.1.json")


def stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16].upper()
    return f"{prefix}-{digest}"


def technical_reason(name: str, size: str) -> str:
    lower = name.lower()
    if name == ".DS_Store":
        return "DS_STORE"
    if lower.endswith(".crdownload"):
        return "PARTIAL_DOWNLOAD"
    try:
        if int(size or 0) == 0:
            return "ZERO_BYTE"
    except ValueError:
        pass
    return ""


def main() -> int:
    if not INPUT.exists():
        raise SystemExit(f"Missing input: {INPUT}")

    with INPUT.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise SystemExit("Live object census is empty")

    drive_ids = [r["drive_id"] for r in rows]
    if len(drive_ids) != len(set(drive_ids)):
        raise SystemExit("Duplicate Drive IDs in live object census")

    exact_groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        exact_groups[(row.get("name", ""), row.get("size", ""))].append(row)

    candidate_keys = {k for k, members in exact_groups.items() if len(members) > 1}
    family_id_by_key = {
        key: stable_id("AKCF", f"{key[0]}\n{key[1]}") for key in sorted(candidate_keys)
    }

    ledger_rows = []
    technical_count = 0
    candidate_object_count = 0

    for row in sorted(rows, key=lambda r: r["drive_id"]):
        key = (row.get("name", ""), row.get("size", ""))
        tech = technical_reason(row.get("name", ""), row.get("size", ""))
        family_id = family_id_by_key.get(key, "")

        if tech:
            resolution_status = "TECHNICAL_EXCLUSION"
            technical_count += 1
        elif family_id:
            resolution_status = "EXACT_METADATA_DUPLICATE_CANDIDATE"
            candidate_object_count += 1
        else:
            resolution_status = "SINGLETON_UNRESOLVED"

        ledger_rows.append({
            "manifestation_id": stable_id("AKM", f"drive:{row['drive_id']}"),
            "drive_id": row["drive_id"],
            "root_title": row.get("root_title", ""),
            "parent_path": row.get("parent_path", ""),
            "name": row.get("name", ""),
            "mime_type": row.get("mime_type", ""),
            "size": row.get("size", ""),
            "candidate_family_id": family_id,
            "canonical_work_id": "",
            "resolution_status": resolution_status,
            "technical_exclusion_reason": tech,
            "equivalence_assertion": "NONE",
            "review_required": "true" if not tech else "false",
        })

    family_rows = []
    for key in sorted(candidate_keys):
        members = exact_groups[key]
        family_rows.append({
            "candidate_family_id": family_id_by_key[key],
            "name": key[0],
            "size": key[1],
            "member_count": len(members),
            "member_drive_ids": "|".join(sorted(r["drive_id"] for r in members)),
            "status": "REVIEW_REQUIRED",
            "equivalence_assertion": "NONE",
            "byte_identity_verified": "false",
            "canonical_work_id": "",
        })

    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(ledger_rows[0].keys()))
        writer.writeheader()
        writer.writerows(ledger_rows)

    with FAMILIES.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(family_rows[0].keys()) if family_rows else [
            "candidate_family_id", "name", "size", "member_count", "member_drive_ids",
            "status", "equivalence_assertion", "byte_identity_verified", "canonical_work_id"
        ])
        writer.writeheader()
        writer.writerows(family_rows)

    summary = {
        "version": "v0.5.1-stage1",
        "input_objects": len(rows),
        "unique_manifestation_ids": len({r["manifestation_id"] for r in ledger_rows}),
        "technical_exclusions": technical_count,
        "exact_metadata_candidate_families": len(family_rows),
        "candidate_objects": candidate_object_count,
        "canonical_work_ids_assigned": 0,
        "unsupported_equivalence_assertions": 0,
        "policy": "fail-closed; metadata similarity creates review candidates only",
    }
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
