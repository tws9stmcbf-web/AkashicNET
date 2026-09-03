#!/usr/bin/env python3
"""Close the explicit-topic audit over the remaining Reddit CSV sources."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"
TEST = COMMUNITY / "n2n-test-batch-25.csv"
DELTAS = [COMMUNITY / f"reddit-manual-delta-batch-{i:04d}.csv" for i in range(1, 7)]

EXPECTED_TEST_CATEGORIES = {
    "Art", "Community", "Consciousness", "Frameworks", "Humour",
    "Indigenous / Cultural Knowledge", "Music", "Nature / Ecology",
    "Personal Experience", "Philosophy", "Psychedelics", "Stories",
    "Wisdom Traditions",
}


def read(path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader), reader.fieldnames or []


def main() -> int:
    test_rows, test_fields = read(TEST)
    delta_data = [read(path) for path in DELTAS]
    delta_counts = [len(rows) for rows, _ in delta_data]
    delta_fields = [fields for _, fields in delta_data]

    if len(test_rows) != 25:
        raise SystemExit("N2N test batch row drift")
    if {row["category"] for row in test_rows} != EXPECTED_TEST_CATEGORIES:
        raise SystemExit("N2N test category drift")
    if delta_counts != [7, 25, 25, 25, 25, 25]:
        raise SystemExit(f"manual delta row drift: {delta_counts}")
    if any(any(name in fields for name in ("topic", "category", "flair")) for fields in delta_fields):
        raise SystemExit("manual delta unexpectedly gained a topic-bearing field")

    result = {
        "version": "0.7.11",
        "status": "REDDIT_CSV_TOPIC_COVERAGE_CLOSED",
        "audited_public_top_level_topic_count": 73,
        "new_top_level_topics": [],
        "promotion_state": "NO_COUNT_CHANGE",
        "remaining_source_counts": {
            "n2n_test_batch_rows": len(test_rows),
            "n2n_test_batch_distinct_categories": len(EXPECTED_TEST_CATEGORIES),
            "manual_delta_batches": len(DELTAS),
            "manual_delta_rows": sum(delta_counts),
        },
        "coverage": {
            "n2n_test_categories": "all already represented",
            "manual_delta_rows": "structural provenance only",
            "toolkit_frameworks": "not counted as topics",
            "reddit_csv_explicit_topic_audit": "complete",
        },
        "guardrails": {
            "url_slug_inference": False,
            "title_inference": False,
            "framework_is_topic": False,
            "semantic_similarity_auto_merge": False,
            "truth_inference": False,
            "rights_promotion": False,
            "scientific_evidence_promotion": False,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
