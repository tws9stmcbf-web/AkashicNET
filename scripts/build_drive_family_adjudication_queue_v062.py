#!/usr/bin/env python3
"""Persist a fail-closed decision for every unresolved live Drive family."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "references" / "community"
FAMILIES = REF / "drive-canonical-family-review-v0.6.0.csv"
BASELINE = REF / "drive-canonical-object-ledger-v0.6.0.csv"
WORKS = REF / "canonical-work-registry-v0.6.1.csv"
EDGES = REF / "canonical-graph-promotions-v0.6.1.csv"
HASHES = REF / "hash-verification-results-v0.16.csv"
DEFAULT_QUEUE = REF / "drive-canonical-family-decisions-v0.6.2.csv"
DEFAULT_SUMMARY = REF / "drive-canonical-completion-v0.6.2.json"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    args = parser.parse_args()

    families = rows(FAMILIES)
    baseline = rows(BASELINE)
    works = rows(WORKS)
    edges = rows(EDGES)
    hashes = rows(HASHES)
    unresolved = [row for row in families if row["review_state"] == "REVIEW_REQUIRED"]

    decisions = []
    for row in sorted(unresolved, key=lambda item: item["candidate_family_id"]):
        decisions.append({
            "decision_id": "hold:" + row["candidate_family_id"].casefold(),
            "candidate_family_id": row["candidate_family_id"],
            "object_count": row["object_count"],
            "disposition": "REVIEW_REQUIRED",
            "review_state": "HOLD",
            "decision_basis": "TITLE;SIZE",
            "confidence": "0.35",
            "work_id": "",
            "edition_id": "",
            "evidence_ref": "drive-canonical-family-review-v0.6.0.csv:" + row["candidate_family_id"],
            "notes": "Exact filename and size are candidate signals only; no identity relationship promoted.",
        })

    args.queue.parent.mkdir(parents=True, exist_ok=True)
    with args.queue.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=decisions[0].keys())
        writer.writeheader()
        writer.writerows(decisions)

    verified_hashes = [row for row in hashes if row["byte_identity_status"] == "BYTE_IDENTICAL_VERIFIED"]
    dispositions: dict[str, int] = {}
    for row in baseline:
        dispositions[row["disposition"]] = dispositions.get(row["disposition"], 0) + 1

    summary = {
        "version": "0.6.2",
        "contract_version": "0.1",
        "live_objects": len(baseline),
        "object_disposition_coverage": len({row["drive_id"] for row in baseline}),
        "baseline_dispositions": dict(sorted(dispositions.items())),
        "candidate_families_total": len(families),
        "technical_candidate_families": sum(row["review_state"] == "CLOSED_TECHNICAL" for row in families),
        "unresolved_family_decisions": len(decisions),
        "unresolved_objects": sum(int(row["object_count"]) for row in decisions),
        "confirmed_works": len(works),
        "confirmed_editions": 0,
        "confirmed_translations": 0,
        "verified_duplicate_pairs": len(verified_hashes),
        "verified_duplicate_objects": len(verified_hashes) * 2,
        "technical_exclusions": dispositions.get("TECHNICAL_EXCLUSION", 0),
        "accepted_graph_edges": len(edges),
        "truth_inference_allowed": False,
        "rights_promotion_allowed": False,
        "scientific_evidence_promotion_allowed": False,
        "reddit_bridge_enabled": False,
    }
    summary["integrity_pass"] = (
        summary["live_objects"] == 2459
        and summary["object_disposition_coverage"] == 2459
        and summary["candidate_families_total"] == 127
        and summary["technical_candidate_families"] == 1
        and summary["unresolved_family_decisions"] == 126
        and summary["unresolved_objects"] == 258
        and summary["confirmed_works"] == 3
        and summary["confirmed_editions"] == 0
        and summary["verified_duplicate_pairs"] == 3
        and summary["technical_exclusions"] == 28
        and summary["accepted_graph_edges"] == 9
    )
    args.summary.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(summary, sort_keys=True))
    return 0 if summary["integrity_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
