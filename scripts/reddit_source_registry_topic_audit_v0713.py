#!/usr/bin/env python3
"""Audit the Reddit source registry for explicit post-level topic evidence."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references" / "community" / "reddit-source-registry.json"
CHECKPOINT = ROOT / "references" / "community" / "reddit-source-registry-topic-audit-v0.7.13.json"


def main() -> int:
    registry = json.loads(SOURCE.read_text(encoding="utf-8"))
    sources = registry["sources"]
    expected = {"NeuronsToNirvana", "TribalGathering", "microdosing", "microDJPanPSYchic"}
    if {s["subreddit"] for s in sources} != expected:
        raise SystemExit("Reddit source registry drift")
    if any(s["platform"] != "reddit" or s["kind"] != "subreddit" for s in sources):
        raise SystemExit("Unexpected source type")
    post_topic_fields = {"topic", "category", "flair", "link_flair_text"}
    observed = sorted(post_topic_fields.intersection({k for s in sources for k in s}))
    if observed:
        raise SystemExit(f"unexpected post topic fields: {observed}")

    result = {
        "version": "0.7.13",
        "status": "REDDIT_SOURCE_REGISTRY_TOPIC_AUDITED",
        "audited_public_top_level_topic_count": 73,
        "new_top_level_topics": [],
        "promotion_state": "NO_COUNT_CHANGE",
        "registry": {
            "source_count": len(sources),
            "subreddits": sorted(expected, key=str.casefold),
            "enabled_sources": sum(bool(s["enabled"]) for s in sources),
            "access_modes": sorted({s["access_mode"] for s in sources}),
            "classification_profiles": sorted({s["classification_profile"] for s in sources}),
            "post_level_topic_or_flair_fields": observed,
        },
        "decision": "Classification profiles configure source handling; they are not post-level Reddit topics or flairs and cannot change the topic census.",
        "guardrails": {
            "classification_profile_is_topic": False,
            "subreddit_name_is_topic": False,
            "url_inference": False,
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
