#!/usr/bin/env python3
"""Validate the human-reviewed disposition of held Reddit topic cells."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "references" / "community" / "n2n-index.csv"

EXPECTED = [
    "Consciousness discourse mapping",
    "Akashic archive, codex, symbolic memory",
    "Unity, ego, multiple paths, meaning-making",
]


def main() -> int:
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        cells = [row["topic"] for row in csv.DictReader(handle)]
    if cells != EXPECTED:
        raise SystemExit(f"held Reddit topic cells drifted: {cells}")

    result = {
        "version": "0.7.9",
        "status": "CANONICAL_REVIEW_ONLY",
        "sealed_public_top_level_topic_count": 71,
        "recommended_candidate_count": 73,
        "recommended_new_top_level_topics": ["meaning-making", "unity"],
        "recommended_child_relationships": {
            "selfhood": ["ego"],
            "cognition": ["symbolic memory"],
        },
        "not_top_level_topics": {
            "consciousness discourse mapping": "mapping method or framework",
            "akashic archive": "project/archive descriptor",
            "codex": "document form",
            "multiple paths": "relational pathway descriptor",
        },
        "promotion_state": "NOT_PROMOTED",
        "required_next_gate": "explicit approval of Unity and Meaning-making as top-level topics",
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
