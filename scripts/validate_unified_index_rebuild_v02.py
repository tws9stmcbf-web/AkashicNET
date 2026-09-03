#!/usr/bin/env python3
"""Validate the count-only AkashicNET unified-index rebuild checkpoint.

This script performs no network access and does not crawl Drive or Reddit. It
reconciles the committed Reddit URI ledger with the last completed non-dry-run
Drive intake count, then verifies the privacy-safe aggregate checkpoint.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REDDIT = ROOT / "references" / "community" / "reddit-uri-index.csv"
DRIVE_AUDIT = ROOT / "tools" / "akashic-library" / "state" / "audit.jsonl"
CHECKPOINT = ROOT / "references" / "community" / "unified-index-rebuild-v0.2.json"

PREVIOUS_REDDIT_ROWS = 9401
PREVIOUS_UNIFIED_RECORDS = 12058
EXPECTED_REDDIT_ROWS = 9502
EXPECTED_DRIVE_RECORDS = 2657


def reddit_rows() -> int:
    with REDDIT.open(newline="", encoding="utf-8") as handle:
        return sum(1 for _ in csv.DictReader(handle))


def drive_records() -> int:
    completed = []
    with DRIVE_AUDIT.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            event = json.loads(line)
            if event.get("event") == "run_complete" and event.get("dry_run") is False:
                completed.append(int(event["count"]))
    if not completed:
        raise SystemExit("no completed non-dry-run Drive intake count found")
    return completed[-1]


def expected_checkpoint() -> dict:
    reddit = reddit_rows()
    drive = drive_records()
    total = reddit + drive
    return {
        "schema": "akashicnet.unified-index-rebuild.v0.2",
        "rebuild_date": "2026-09-03",
        "status": "INDEX_ONLY_REBUILD_VALIDATED",
        "mode": "count_only_privacy_safe",
        "network_access_performed": False,
        "crawler_runs_performed": False,
        "sources": {
            "reddit": {
                "path": "references/community/reddit-uri-index.csv",
                "records": reddit,
                "previous_records": PREVIOUS_REDDIT_ROWS,
            },
            "drive": {
                "path": "tools/akashic-library/state/audit.jsonl",
                "records": drive,
                "selection": "latest run_complete where dry_run is false",
            },
        },
        "recount": {
            "previous_unified_index_records": PREVIOUS_UNIFIED_RECORDS,
            "current_unified_index_records": total,
            "net_change": total - PREVIOUS_UNIFIED_RECORDS,
        },
        "gates": {
            "reddit_source_count_matches": reddit == EXPECTED_REDDIT_ROWS,
            "drive_source_count_matches": drive == EXPECTED_DRIVE_RECORDS,
            "recount_arithmetic_matches": total == 12159,
            "raw_drive_rows_materialized": False,
            "usernames_stored": False,
            "post_bodies_stored": False,
            "comments_stored": False,
            "truth_inference": False,
            "rights_promotion": False,
            "scientific_evidence_promotion": False,
        },
        "limitations": [
            "This rebuild reconciles aggregate record counts; it does not expose private Drive rows.",
            "Reddit API verification remains pending and is not implied by structural inclusion.",
            "Structural inclusion does not establish authorship, permanence, reuse rights, or scientific validity.",
        ],
    }


def main() -> int:
    expected = expected_checkpoint()
    actual = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    if actual != expected:
        raise SystemExit("unified-index checkpoint drift")
    failed = [name for name, passed in actual["gates"].items() if isinstance(passed, bool) and name.endswith("_matches") and not passed]
    if failed:
        raise SystemExit(f"unified-index gates failed: {failed}")
    print(json.dumps(actual, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
