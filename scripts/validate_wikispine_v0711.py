#!/usr/bin/env python3
"""Validate WikiSpine v0.7.11 foundations expansion and fail-closed boundaries."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"
BATCH = COMMUNITY / "wikispine-batch-l-foundations-v0.7.11.json"
AGG = COMMUNITY / "wikispine-entity-aggregate-v0.7.11.json"
PREV = COMMUNITY / "wikispine-entity-aggregate-v0.7.10.json"

EXPECTED_PENDING = {
    ("The Psychedelic Experience", "WORK", "PENDING_VERIFIED_QID"),
    ("Wholeness and the Implicate Order", "WORK", "PENDING_VERIFIED_QID"),
}


def main() -> int:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    agg = json.loads(AGG.read_text(encoding="utf-8"))
    prev = json.loads(PREV.read_text(encoding="utf-8"))

    records = batch["records"]
    assert batch["version"] == "0.7.11"
    assert len(records) == 5
    assert all(r["entity_type"] == "PERSON" for r in records)
    assert len({r["akashic_entity"] for r in records}) == 5
    assert len({r["wikidata_qid"] for r in records}) == 5
    assert all(r["resolution_state"] == "RESOLVED_HIGH_PRECISION" for r in records)
    assert all(r["reference_class"] == "REFERENCE_ENCYCLOPEDIA" for r in records)
    assert all(r["semantic_decision"] == "REFERENCE_IDENTITY_ONLY" for r in records)
    assert all(r["truth_inference"] is False for r in records)
    assert all(r["scientific_evidence"] is False for r in records)

    guard = batch["guardrails"]
    assert guard["candidate_edges_default"] == "HOLD"
    assert guard["max_hops"] == 2
    assert guard["arbitrary_recursive_crawl"] is False
    assert guard["full_article_body_ingestion_default"] is False
    assert guard["rights_promotion_allowed"] is False
    assert guard["scientific_evidence_promotion_allowed"] is False
    assert guard["truth_inference_allowed"] is False
    assert guard["drive_access_performed"] is False

    assert prev["resolved_high_precision"] == 41
    assert prev["resolved_by_type"] == {"PERSON": 30, "WORK": 11}
    assert agg["resolved_high_precision"] == 46
    assert agg["resolved_by_type"] == {"PERSON": 35, "WORK": 11}
    assert agg["pending_resolution"] == 2
    pending = {(x["akashic_entity"], x["entity_type"], x["resolution_state"]) for x in agg["pending_entities"]}
    assert pending == EXPECTED_PENDING
    assert agg["source_batches"][-1] == BATCH.name

    ag = agg["guardrails"]
    assert ag["entity_identity_is_truth"] is False
    assert ag["entity_count_is_topic_count"] is False
    assert ag["candidate_edges_default"] == "HOLD"
    assert ag["rights_promotion_allowed"] is False
    assert ag["scientific_evidence_promotion_allowed"] is False
    assert ag["truth_inference_allowed"] is False
    assert ag["drive_access_performed"] is False

    print("AKASHICNET WikiSpine v0.7.11 PASS", {
        "new_person_identities": 5,
        "resolved_high_precision": 46,
        "person": 35,
        "work": 11,
        "pending": 2,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
