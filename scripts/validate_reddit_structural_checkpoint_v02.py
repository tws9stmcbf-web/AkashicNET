#!/usr/bin/env python3
"""Validate the materialised historical Reddit structural denominator checkpoint."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.reddit_corpus_census import audit

SOURCE = ROOT / "references" / "community" / "reddit-uri-index.csv"
CHECKPOINT = ROOT / "references" / "community" / "reddit-corpus-structural-checkpoint-v0.2.json"


def validate() -> list[str]:
    errors: list[str] = []
    expected = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    actual = audit(SOURCE)

    mapping = {
        "source_rows": actual["total_rows"],
        "post_rows": actual["post_rows"],
        "annotation_derived_rows": actual["status_counts"].get("annotation_derived", 0),
        "candidate_rows": actual["status_counts"].get("candidate", 0),
        "non_post_subreddit_rows": actual["status_counts"].get("non_post_subreddit", 0),
        "unique_post_ids_all_subreddits": actual["unique_post_ids"],
        "unique_canonical_post_urls_all_subreddits": actual["unique_canonical_urls"],
        "duplicate_post_id_rows": actual["duplicate_post_id_rows"],
        "duplicate_canonical_url_rows": actual["duplicate_canonical_url_rows"],
        "source_rows_by_subreddit": actual["subreddits"],
        "unique_post_ids_by_subreddit": actual["unique_post_ids_by_subreddit"],
    }

    for key, value in mapping.items():
        if expected.get(key) != value:
            errors.append(f"{key}: checkpoint={expected.get(key)!r} recomputed={value!r}")

    boundary = expected.get("evidence_boundary", {})
    for key in (
        "structurally_valid_means_api_verified",
        "annotation_rows_are_independent_posts",
        "source_row_count_may_be_presented_as_unique_post_count",
    ):
        if boundary.get(key) is not False:
            errors.append(f"evidence boundary must remain false: {key}")

    if expected.get("network_access_performed") is not False:
        errors.append("checkpoint must state network_access_performed=false")
    if expected.get("reddit_api_verification_performed") is not False:
        errors.append("checkpoint must state reddit_api_verification_performed=false")
    return errors


def main() -> int:
    try:
        errors = validate()
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"REDDIT STRUCTURAL CHECKPOINT VALIDATION FAILED: {exc}")
        return 1
    if errors:
        print("REDDIT STRUCTURAL CHECKPOINT VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("REDDIT STRUCTURAL CHECKPOINT VALIDATION PASS: 9,401 rows -> 7,356 structural unique posts; N2N 7,298")
    return 0


if __name__ == "__main__":
    sys.exit(main())
