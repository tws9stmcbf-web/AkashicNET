#!/usr/bin/env python3
"""Promote explicitly approved Reddit-derived top-level topics."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "references" / "community" / "reddit-topic-canonical-review-v0.7.9.json"


def main() -> int:
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    if review["sealed_public_top_level_topic_count"] != 71:
        raise SystemExit("review baseline drift")
    if review["recommended_new_top_level_topics"] != ["meaning-making", "unity"]:
        raise SystemExit("review candidate drift")

    result = {
        "version": "0.7.10",
        "status": "PROMOTED_PUBLIC_CHECKPOINT",
        "previous_public_top_level_topic_count": 71,
        "audited_public_top_level_topic_count": 73,
        "promoted_top_level_topics": ["meaning-making", "unity"],
        "canonical_child_relationships": {
            "selfhood": ["ego"],
            "cognition": ["symbolic memory"],
        },
        "promotion_state": "PROMOTED",
        "approval_date": "2026-09-03",
        "guardrails": {
            "comma_token_auto_promotion": False,
            "semantic_similarity_auto_merge": False,
            "url_slug_inference": False,
            "truth_inference": False,
            "rights_promotion": False,
            "scientific_evidence_promotion": False,
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
