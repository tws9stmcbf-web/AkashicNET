#!/usr/bin/env python3
"""Seal the governed Reddit topic census across checkpoints v0.7.8-v0.7.17."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = ROOT / "references" / "community" / "reddit-topic-census-seal-v0.7.18.json"
CHECKPOINTS = {
    "0.7.8": "references/community/reddit-topic-source-audit-v0.7.8.json",
    "0.7.9": "references/community/reddit-topic-canonical-review-v0.7.9.json",
    "0.7.10": "references/community/reddit-topic-promotion-v0.7.10.json",
    "0.7.11": "references/community/reddit-csv-topic-closure-v0.7.11.json",
    "0.7.12": "references/community/reddit-jsonl-metadata-audit-v0.7.12.json",
    "0.7.13": "references/community/reddit-source-registry-topic-audit-v0.7.13.json",
    "0.7.14": "references/community/reddit-canonical-delta-topic-audit-v0.7.14.json",
    "0.7.15": "references/community/reddit-corroboration-topic-audit-v0.7.15.json",
    "0.7.16": "references/community/reddit-structural-unified-topic-audit-v0.7.16.json",
    "0.7.17": "references/community/reddit-markdown-topic-closure-v0.7.17.json",
}
EXPECTED_STATUSES = {
    "0.7.8": "REDDIT_TOPIC_SOURCE_AUDIT",
    "0.7.9": "CANONICAL_REVIEW_ONLY",
    "0.7.10": "PROMOTED_PUBLIC_CHECKPOINT",
    "0.7.11": "REDDIT_CSV_TOPIC_COVERAGE_CLOSED",
    "0.7.12": "REDDIT_JSONL_METADATA_BATCH_1_AUDITED",
    "0.7.13": "REDDIT_SOURCE_REGISTRY_TOPIC_AUDITED",
    "0.7.14": "REDDIT_CANONICAL_DELTA_TOPIC_AUDITED",
    "0.7.15": "REDDIT_CORROBORATION_TOPIC_AUDITED",
    "0.7.16": "REDDIT_STRUCTURAL_UNIFIED_TOPIC_AUDITED",
    "0.7.17": "REDDIT_MARKDOWN_TOPIC_COVERAGE_CLOSED",
}
REQUIRED_FALSE_GUARDRAILS = (
    "truth_inference",
    "rights_promotion",
    "scientific_evidence_promotion",
)


def load_documents():
    documents = {}
    for version, relative_path in CHECKPOINTS.items():
        path = ROOT / relative_path
        if not path.is_file():
            raise ValueError(f"missing checkpoint: {relative_path}")
        documents[version] = json.loads(path.read_text(encoding="utf-8"))
    return documents


def validate_chain(documents):
    if set(documents) != set(CHECKPOINTS):
        raise ValueError("checkpoint version set differs from the governed chain")

    for version in CHECKPOINTS:
        document = documents[version]
        if document.get("version") != version:
            raise ValueError(f"version mismatch at {version}")
        if document.get("status") != EXPECTED_STATUSES[version]:
            raise ValueError(f"status mismatch at {version}")
        guardrails = document.get("guardrails", {})
        for key in REQUIRED_FALSE_GUARDRAILS:
            if guardrails.get(key) is not False:
                raise ValueError(f"{key} must remain false at {version}")

    source_audit = documents["0.7.8"]
    if source_audit.get("sealed_public_top_level_topic_count") != 71:
        raise ValueError("v0.7.8 must seal 71 topics")
    if source_audit.get("automatically_promotable_topics_from_uri_and_semantic_indexes") != 0:
        raise ValueError("URI and semantic indexes must not auto-promote topics")

    review = documents["0.7.9"]
    if review.get("sealed_public_top_level_topic_count") != 71:
        raise ValueError("v0.7.9 must preserve the 71-topic seal")
    if review.get("recommended_candidate_count") != 73:
        raise ValueError("v0.7.9 candidate count must be 73")
    if review.get("promotion_state") != "NOT_PROMOTED":
        raise ValueError("v0.7.9 must remain review-only")

    promotion = documents["0.7.10"]
    if promotion.get("previous_public_top_level_topic_count") != 71:
        raise ValueError("v0.7.10 previous count must be 71")
    if promotion.get("audited_public_top_level_topic_count") != 73:
        raise ValueError("v0.7.10 promoted count must be 73")
    if promotion.get("promoted_top_level_topics") != ["meaning-making", "unity"]:
        raise ValueError("v0.7.10 promoted topics differ from approval")
    if promotion.get("promotion_state") != "PROMOTED":
        raise ValueError("v0.7.10 must record the approved promotion")

    no_change_versions = list(CHECKPOINTS)[3:]
    for version in no_change_versions:
        document = documents[version]
        if document.get("audited_public_top_level_topic_count") != 73:
            raise ValueError(f"topic count drift at {version}")
        if document.get("new_top_level_topics") != []:
            raise ValueError(f"unexpected topic promotion at {version}")
        if document.get("promotion_state") != "NO_COUNT_CHANGE":
            raise ValueError(f"promotion state mismatch at {version}")

    if documents["0.7.17"].get("coverage", {}).get("markdown_explicit_topic_audit") != "complete":
        raise ValueError("Markdown explicit-topic coverage is not complete")

    return {
        "version": "0.7.18",
        "status": "REDDIT_TOPIC_CENSUS_SEALED",
        "previous_sealed_public_top_level_topic_count": 71,
        "audited_public_top_level_topic_count": 73,
        "promotion_checkpoint": "0.7.10",
        "promoted_top_level_topics": ["meaning-making", "unity"],
        "subsequent_no_change_checkpoints": no_change_versions,
        "checkpoint_chain": [
            {"version": version, "path": CHECKPOINTS[version], "status": EXPECTED_STATUSES[version]}
            for version in CHECKPOINTS
        ],
        "coverage": {
            "checkpoint_count": len(CHECKPOINTS),
            "first_checkpoint": "0.7.8",
            "last_checkpoint": "0.7.17",
            "explicit_topic_coverage": "complete_for_current_governed_reddit_sources",
            "surfaces": [
                "URI and semantic indexes",
                "canonical review and explicit promotion",
                "CSV",
                "JSONL",
                "source registry",
                "canonical delta JSON",
                "corroboration JSON",
                "structural and unified index",
                "source-bearing Markdown",
            ],
        },
        "decision": "The current governed Reddit source surfaces are reconciled. Only meaning-making and unity were explicitly approved for promotion; every later checkpoint preserves the public-safe count of 73.",
        "guardrails": {
            "new_source_requires_reaudit": True,
            "title_inference": False,
            "url_inference": False,
            "subreddit_name_inference": False,
            "semantic_similarity_auto_merge": False,
            "truth_inference": False,
            "rights_promotion": False,
            "scientific_evidence_promotion": False,
        },
    }


def main():
    result = validate_chain(load_documents())
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    if result != checkpoint:
        raise SystemExit("generated census seal differs from checked-in checkpoint")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
