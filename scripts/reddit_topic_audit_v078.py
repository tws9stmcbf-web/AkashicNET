#!/usr/bin/env python3
"""Audit Reddit CSVs for explicit topic-bearing fields without URL inference."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"

URI = COMMUNITY / "reddit-uri-index.csv"
SEMANTIC = COMMUNITY / "reddit-semantic-index.csv"
PILOT = COMMUNITY / "n2n-pilot-index.csv"
CURATED = COMMUNITY / "n2n-index.csv"

EXPECTED_CATEGORIES = {
    "Art", "Community", "Consciousness", "Frameworks", "Future / Speculation",
    "Humour", "Indigenous / Cultural Knowledge", "Music", "Nature / Ecology",
    "Personal Experience", "Philosophy", "Psychedelics", "Research", "Stories",
    "Wisdom Traditions",
}


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> int:
    uri = rows(URI)
    semantic = rows(SEMANTIC)
    pilot = rows(PILOT)
    curated = rows(CURATED)

    if len(uri) != 9502 or len({r["reddit_url"] for r in uri}) != 9502:
        raise SystemExit("reddit URI census drift")
    if len(semantic) != 9401 or len({r["reddit_url"] for r in semantic}) != 9401:
        raise SystemExit("reddit semantic URL census drift")
    if {r["subreddit"] for r in semantic} != {"NeuronsToNirvana", "TribalGathering", "microdosing"}:
        raise SystemExit("reddit semantic subreddit drift")
    if len(pilot) != 1000 or {r["category"] for r in pilot} != EXPECTED_CATEGORIES:
        raise SystemExit("N2N pilot category census drift")
    if len(curated) != 3:
        raise SystemExit("curated N2N topic-row drift")

    structural_headers = {
        "reddit_uri_index": list(uri[0]),
        "reddit_semantic_index": list(semantic[0]),
    }
    if structural_headers["reddit_uri_index"] != ["reddit_url"]:
        raise SystemExit("URI index unexpectedly gained a topic-bearing field")
    if any(x in structural_headers["reddit_semantic_index"] for x in ("topic", "category", "flair")):
        raise SystemExit("semantic index unexpectedly gained a topic-bearing field")

    result = {
        "version": "0.7.8",
        "status": "REDDIT_TOPIC_SOURCE_AUDIT",
        "sealed_public_top_level_topic_count": 71,
        "automatically_promotable_topics_from_uri_and_semantic_indexes": 0,
        "source_counts": {
            "reddit_uri_rows": len(uri),
            "reddit_uri_unique_values": len({r["reddit_url"] for r in uri}),
            "reddit_semantic_rows": len(semantic),
            "reddit_semantic_unique_urls": len({r["reddit_url"] for r in semantic}),
            "reddit_semantic_unique_post_ids": len({r["post_id"] for r in semantic if r["post_id"]}),
            "reddit_semantic_subreddits": sorted({r["subreddit"] for r in semantic}),
            "n2n_pilot_rows": len(pilot),
            "n2n_pilot_categories": len(EXPECTED_CATEGORIES),
        },
        "held_explicit_topic_cells": [r["topic"] for r in curated],
        "hold_reason": "free-text multi-concept cells require canonical review; URL slugs are not topic labels",
        "promotion_state": "NO_COUNT_CHANGE",
        "guardrails": {
            "url_is_topic": False,
            "url_slug_inference": False,
            "title_inference": False,
            "free_text_token_auto_promotion": False,
            "semantic_similarity_auto_merge": False,
            "private_data_included": False,
            "truth_inference": False,
            "rights_promotion": False,
            "scientific_evidence_promotion": False,
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
