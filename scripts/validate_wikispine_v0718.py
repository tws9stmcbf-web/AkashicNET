#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"
BATCH = COMMUNITY / "wikispine-batch-s-works-v0.7.18.json"
PREV = COMMUNITY / "wikispine-entity-aggregate-v0.7.17.json"
AGG = COMMUNITY / "wikispine-entity-aggregate-v0.7.18.json"

EXPECTED_ENTITY = "The Psychedelic Experience"
EXPECTED_QID = "Q4382913"


def validate(batch: dict, prev: dict, agg: dict) -> bool:
    assert batch["version"] == "0.7.18"
    records = batch["records"]
    assert len(records) == 1
    record = records[0]
    assert record["akashic_entity"] == EXPECTED_ENTITY
    assert record["entity_type"] == "WORK"
    assert record["wikidata_qid"] == EXPECTED_QID
    assert record["wikipedia_title"] == EXPECTED_ENTITY
    assert record["resolution_state"] == "RESOLVED_HIGH_PRECISION"
    assert record["reference_class"] == "REFERENCE_ENCYCLOPEDIA"
    assert record["semantic_decision"] == "REFERENCE_IDENTITY_ONLY"
    assert record["truth_inference"] is False
    assert record["scientific_evidence"] is False

    for guards in (batch["guardrails"], agg["guardrails"]):
        assert guards["candidate_edges_default"] == "HOLD"
        assert guards["entity_count_is_topic_count"] is False
        assert guards["rights_promotion_allowed"] is False
        assert guards["scientific_evidence_promotion_allowed"] is False
        assert guards["truth_inference_allowed"] is False
        assert guards["drive_access_performed"] is False

    assert prev["resolved_high_precision"] == 72
    assert prev["resolved_by_type"] == {"PERSON": 60, "WORK": 12}
    assert prev["pending_resolution"] == len(prev["pending_entities"]) == 1
    assert prev["pending_entities"][0]["akashic_entity"] == EXPECTED_ENTITY
    assert prev["pending_entities"][0]["entity_type"] == "WORK"
    assert "wikidata_qid" not in prev["pending_entities"][0]

    assert agg["version"] == "0.7.18"
    assert agg["resolved_high_precision"] == 73
    assert agg["resolved_by_type"] == {"PERSON": 60, "WORK": 13}
    assert sum(agg["resolved_by_type"].values()) == agg["resolved_high_precision"]
    assert agg["resolved_high_precision"] == prev["resolved_high_precision"] + 1
    assert agg["resolved_by_type"]["WORK"] == prev["resolved_by_type"]["WORK"] + 1
    assert agg["resolved_by_type"]["PERSON"] == prev["resolved_by_type"]["PERSON"]
    assert agg["pending_resolution"] == 0
    assert agg["pending_entities"] == []
    assert "wikispine-batch-s-works-v0.7.18.json" in agg["source_batches"]
    return True


def main() -> int:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    prev = json.loads(PREV.read_text(encoding="utf-8"))
    agg = json.loads(AGG.read_text(encoding="utf-8"))
    validate(batch, prev, agg)
    print("AKASHICNET v0.7.18 WIKISPINE PASS", {"new_works": 1, "resolved_high_precision": 73, "pending": 0})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
