#!/usr/bin/env python3
"""Cross-audit Reddit structural and unified-index metadata for topic fields."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"
STRUCTURAL = COMMUNITY / "reddit-corpus-structural-checkpoint-v0.2.json"
UNIFIED = COMMUNITY / "unified-index-rebuild-v0.2.json"
CHECKPOINT = COMMUNITY / "reddit-structural-unified-topic-audit-v0.7.16.json"
TOPIC_FIELDS = {
    "topic", "topics", "category", "categories", "flair",
    "link_flair_text", "link_flair_template_id",
}


def keys_recursive(value):
    keys = set()
    if isinstance(value, dict):
        for key, child in value.items():
            keys.add(key)
            keys.update(keys_recursive(child))
    elif isinstance(value, list):
        for child in value:
            keys.update(keys_recursive(child))
    return keys


def main() -> int:
    structural = json.loads(STRUCTURAL.read_text(encoding="utf-8"))
    unified = json.loads(UNIFIED.read_text(encoding="utf-8"))

    reddit_rows = structural["source_rows"]
    unified_reddit = unified["sources"]["reddit"]["records"]
    drive_rows = unified["sources"]["drive"]["records"]
    current = unified["recount"]["current_unified_index_records"]
    previous_reddit = unified["sources"]["reddit"]["previous_records"]
    previous = unified["recount"]["previous_unified_index_records"]
    net_change = unified["recount"]["net_change"]

    if reddit_rows != 9502 or unified_reddit != reddit_rows:
        raise SystemExit("Reddit source-count reconciliation drift")
    if drive_rows != 2657 or current != reddit_rows + drive_rows:
        raise SystemExit("current unified-index arithmetic drift")
    if previous != previous_reddit + drive_rows:
        raise SystemExit("previous unified-index arithmetic drift")
    if net_change != reddit_rows - previous_reddit or net_change != current - previous:
        raise SystemExit("unified-index net-change drift")
    if structural["unique_post_ids_all_subreddits"] != 7457:
        raise SystemExit("structural unique-post count drift")
    if structural["unique_canonical_post_urls_all_subreddits"] != 7457:
        raise SystemExit("structural unique-URL count drift")

    observed_topic_fields = sorted(TOPIC_FIELDS.intersection(
        keys_recursive(structural) | keys_recursive(unified)
    ))
    if observed_topic_fields:
        raise SystemExit(f"unexpected topic-bearing fields: {observed_topic_fields}")

    result = {
        "version": "0.7.16",
        "status": "REDDIT_STRUCTURAL_UNIFIED_TOPIC_AUDITED",
        "audited_public_top_level_topic_count": 73,
        "new_top_level_topics": [],
        "promotion_state": "NO_COUNT_CHANGE",
        "reconciliation": {
            "reddit_source_rows": reddit_rows,
            "drive_source_rows": drive_rows,
            "current_unified_index_records": current,
            "previous_reddit_source_rows": previous_reddit,
            "previous_unified_index_records": previous,
            "net_change": net_change,
            "unique_reddit_post_ids_all_subreddits": structural["unique_post_ids_all_subreddits"],
            "unique_reddit_urls_all_subreddits": structural["unique_canonical_post_urls_all_subreddits"],
            "arithmetic_valid": True,
            "explicit_topic_category_or_flair_fields": observed_topic_fields,
        },
        "decision": "The structural checkpoint and unified rebuild contain aggregate provenance and count metadata only; they contain no explicit topic, category, or Reddit flair evidence.",
        "guardrails": {
            "counts_are_topics": False,
            "subreddit_is_topic": False,
            "path_inference": False,
            "note_text_inference": False,
            "truth_inference": False,
            "rights_promotion": False,
            "scientific_evidence_promotion": False,
        },
    }
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    if result != checkpoint:
        raise SystemExit("generated audit differs from checked-in checkpoint")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
