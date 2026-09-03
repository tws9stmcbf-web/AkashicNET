#!/usr/bin/env python3
"""Audit the first 25 Reddit JSONL metadata records without topic inference."""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSONL = ROOT / "tools" / "n2n" / "dryrun" / "25_post_test.jsonl"
CSV = ROOT / "references" / "community" / "n2n-test-batch-25.csv"

EXPECTED_CATEGORIES = {
    "art": 1,
    "community": 1,
    "consciousness": 2,
    "frameworks": 10,
    "humour": 1,
    "lived experience": 2,
    "music": 1,
    "nature": 1,
    "philosophy": 2,
    "psychedelics": 1,
    "stories": 1,
    "wisdom": 2,
}


def main() -> int:
    with JSONL.open(encoding="utf-8") as handle:
        records = [json.loads(line) for line in handle if line.strip()]
    with CSV.open(newline="", encoding="utf-8") as handle:
        csv_rows = list(csv.DictReader(handle))

    if len(records) != 25 or len({r["reddit_post_id"] for r in records}) != 25:
        raise SystemExit("JSONL record or post-ID drift")
    if Counter(r["category"] for r in records) != Counter(EXPECTED_CATEGORIES):
        raise SystemExit("JSONL category drift")
    if {r["reddit_url"] for r in records} != {r["reddit_url"] for r in csv_rows}:
        raise SystemExit("JSONL is no longer the same 25-record lineage as the audited CSV")
    if any(r.get("import_mode") != "dry_run" for r in records):
        raise SystemExit("JSONL lineage is no longer uniformly dry-run")
    forbidden = {"topic", "flair", "link_flair_text", "link_flair_template_id"}
    observed_native_fields = sorted(forbidden.intersection({k for r in records for k in r}))
    if observed_native_fields:
        raise SystemExit(f"unexpected Reddit-native topic/flair fields: {observed_native_fields}")

    result = {
        "version": "0.7.12",
        "status": "REDDIT_JSONL_METADATA_BATCH_1_AUDITED",
        "audited_public_top_level_topic_count": 73,
        "new_top_level_topics": [],
        "promotion_state": "NO_COUNT_CHANGE",
        "batch": {
            "path": "tools/n2n/dryrun/25_post_test.jsonl",
            "records": len(records),
            "unique_reddit_post_ids": len({r["reddit_post_id"] for r in records}),
            "distinct_normalized_categories": len(EXPECTED_CATEGORIES),
            "normalized_category_counts": dict(sorted(EXPECTED_CATEGORIES.items())),
            "reddit_native_topic_or_flair_fields": observed_native_fields,
        },
        "lineage": {
            "source_csv": "references/community/n2n-test-batch-25.csv",
            "same_reddit_url_set": True,
            "import_mode": "dry_run",
            "independent_topic_evidence": False,
        },
        "decision": "The category field is normalized project metadata from an already-audited CSV lineage, not a Reddit-native flair. It adds no independent top-level topic evidence.",
        "guardrails": {
            "url_slug_inference": False,
            "title_inference": False,
            "summary_inference": False,
            "framework_is_topic": False,
            "normalized_category_auto_promotion": False,
            "truth_inference": False,
            "rights_promotion": False,
            "scientific_evidence_promotion": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
