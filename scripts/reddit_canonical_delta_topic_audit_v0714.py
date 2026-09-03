#!/usr/bin/env python3
"""Audit the 101-record canonical Reddit delta for explicit topic metadata."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references" / "community" / "reddit-canonical-delta-import-2026-09-02.json"
CHECKPOINT = ROOT / "references" / "community" / "reddit-canonical-delta-topic-audit-v0.7.14.json"
EXPECTED_FIELDS = {
    "canonical_url", "import_status", "live_verification_status",
    "observed_at", "reddit_post_id", "source_batch",
}
EXPECTED_BATCHES = {
    "reddit-manual-delta-batch-0002.csv": 25,
    "reddit-manual-delta-batch-0003.csv": 25,
    "reddit-manual-delta-batch-0004.csv": 25,
    "reddit-manual-delta-batch-0005.csv": 25,
    "reddit-manual-delta-batch-0006.csv": 1,
}
TOPIC_FIELDS = {
    "topic", "topics", "category", "categories", "flair",
    "link_flair_text", "link_flair_template_id",
}


def main() -> int:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    records = source["records"]
    observed_fields = {key for record in records for key in record}
    if len(records) != 101:
        raise SystemExit("canonical delta record-count drift")
    if len({r["reddit_post_id"] for r in records}) != 101:
        raise SystemExit("canonical delta post-ID uniqueness drift")
    if len({r["canonical_url"] for r in records}) != 101:
        raise SystemExit("canonical delta URL uniqueness drift")
    if observed_fields != EXPECTED_FIELDS:
        raise SystemExit(f"canonical delta record-field drift: {sorted(observed_fields)}")
    batches = dict(sorted(Counter(r["source_batch"] for r in records).items()))
    if batches != EXPECTED_BATCHES:
        raise SystemExit(f"canonical delta batch drift: {batches}")
    observed_topic_fields = sorted(TOPIC_FIELDS.intersection(observed_fields))
    if observed_topic_fields:
        raise SystemExit(f"unexpected topic-bearing fields: {observed_topic_fields}")

    result = {
        "version": "0.7.14",
        "status": "REDDIT_CANONICAL_DELTA_TOPIC_AUDITED",
        "audited_public_top_level_topic_count": 73,
        "new_top_level_topics": [],
        "promotion_state": "NO_COUNT_CHANGE",
        "batch": {
            "path": "references/community/reddit-canonical-delta-import-2026-09-02.json",
            "records": len(records),
            "unique_reddit_post_ids": len({r["reddit_post_id"] for r in records}),
            "unique_canonical_urls": len({r["canonical_url"] for r in records}),
            "source_batch_counts": batches,
            "record_fields": sorted(observed_fields),
            "explicit_topic_category_or_flair_fields": observed_topic_fields,
        },
        "decision": "The canonical delta stores structural import and observation metadata only. It contains no explicit topic, category, or Reddit flair evidence.",
        "guardrails": {
            "title_inference": False,
            "url_inference": False,
            "post_id_inference": False,
            "subreddit_is_topic": False,
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
