#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"
BATCH = COMMUNITY / "wikispine-batch-r-works-v0.7.17.json"
PREV = COMMUNITY / "wikispine-entity-aggregate-v0.7.16.json"
AGG = COMMUNITY / "wikispine-entity-aggregate-v0.7.17.json"

EXPECTED_ENTITY = "Wholeness and the Implicate Order"
EXPECTED_QID = "Q17094352"
EXPECTED_PENDING = "The Psychedelic Experience"


def validate(batch: dict, prev: dict, agg: dict) -> bool:
    assert batch["version"] == "0.7.17"
    records = batch["records"]
    assert len(records) == 1
    r = records[0]
    assert r["akashic_entity"] == EXPECTED_ENTITY
    assert r["entity_type"] == "WORK"
    assert r["wikidata_qid"] == EXPECTED_QID
    assert r["wikipedia_title"] == EXPECTED_ENTITY
    assert r["resolution_state"] == "RESOLVED_HIGH_PRECISION"
    assert r["reference_class"] == "REFERENCE_ENCYCLOPEDIA"
    assert r["semantic_decision"] == "REFERENCE_IDENTITY_ONLY"
    assert r["truth_inference"] is False
    assert r["scientific_evidence"] is False

    for guards in (batch["guardrails"], agg["guardrails"]):
        assert guards["candidate_edges_default"] == "HOLD"
        assert guards["entity_count_is_topic_count"] is False
        assert guards["rights_promotion_allowed"] is False
        assert guards["scientific_evidence_promotion_allowed"] is False
        assert guards["truth_inference_allowed"] is False
        assert guards["drive_access_performed"] is False

    assert prev["resolved_high_precision"] == 71
    assert prev["resolved_by_type"] == {"PERSON": 60, "WORK": 11}
    assert prev["pending_resolution"] == 2
    assert {p["akashic_entity"] for p in prev["pending_entities"]} == {
        EXPECTED_ENTITY,
        EXPECTED_PENDING,
    }

    assert agg["version"] == "0.7.17"
    assert agg["resolved_high_precision"] == 72
    assert agg["resolved_by_type"] == {"PERSON": 60, "WORK": 12}
    assert sum(agg["resolved_by_type"].values()) == agg["resolved_high_precision"]
    assert agg["resolved_high_precision"] == prev["resolved_high_precision"] + 1
    assert agg["resolved_by_type"]["WORK"] == prev["resolved_by_type"]["WORK"] + 1
    assert agg["resolved_by_type"]["PERSON"] == prev["resolved_by_type"]["PERSON"]
    assert agg["pending_resolution"] == len(agg["pending_entities"]) == 1
    pending = agg["pending_entities"][0]
    assert pending == {
        "akashic_entity": EXPECTED_PENDING,
        "entity_type": "WORK",
        "resolution_state": "PENDING_VERIFIED_QID",
    }
    assert "wikidata_qid" not in pending
    assert "wikispine-batch-r-works-v0.7.17.json" in agg["source_batches"]
    return True


def main() -> int:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    prev = json.loads(PREV.read_text(encoding="utf-8"))
    agg = json.loads(AGG.read_text(encoding="utf-8"))
    validate(batch, prev, agg)
    print("AKASHICNET v0.7.17 WIKISPINE PASS", {"new_works": 1, "resolved_high_precision": 72, "pending": 1})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
