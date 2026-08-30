#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "references" / "community"
BATCH = COMMUNITY / "wikispine-batch-m-consciousness-researchers-v0.7.12.json"
AGG = COMMUNITY / "wikispine-entity-aggregate-v0.7.12.json"

EXPECTED = {
    "Anil Seth": "Q22087352",
    "Christof Koch": "Q1084303",
    "Giulio Tononi": "Q1080557",
    "Michael Pollan": "Q1138996",
    "Rick Strassman": "Q4354666",
}


def validate(batch: dict, agg: dict) -> bool:
    assert batch["version"] == "0.7.12"
    records = batch["records"]
    assert len(records) == 5
    assert {r["akashic_entity"]: r["wikidata_qid"] for r in records} == EXPECTED
    assert len({r["wikidata_qid"] for r in records}) == len(records)
    for r in records:
        assert r["entity_type"] == "PERSON"
        assert r["resolution_state"] == "RESOLVED_HIGH_PRECISION"
        assert r["reference_class"] == "REFERENCE_ENCYCLOPEDIA"
        assert r["semantic_decision"] == "REFERENCE_IDENTITY_ONLY"
        assert r["truth_inference"] is False
        assert r["scientific_evidence"] is False

    g = batch["guardrails"]
    assert g["candidate_edges_default"] == "HOLD"
    assert g["entity_count_is_topic_count"] is False
    assert g["rights_promotion_allowed"] is False
    assert g["scientific_evidence_promotion_allowed"] is False
    assert g["truth_inference_allowed"] is False
    assert g["drive_access_performed"] is False

    assert agg["version"] == "0.7.12"
    assert agg["resolved_high_precision"] == 51
    assert agg["resolved_by_type"] == {"PERSON": 40, "WORK": 11}
    assert agg["resolved_by_type"]["PERSON"] + agg["resolved_by_type"]["WORK"] == agg["resolved_high_precision"]
    assert agg["pending_resolution"] == len(agg["pending_entities"]) == 2
    for pending in agg["pending_entities"]:
        assert pending["resolution_state"] == "PENDING_VERIFIED_QID"
        assert "wikidata_qid" not in pending

    ag = agg["guardrails"]
    assert ag["entity_identity_is_truth"] is False
    assert ag["entity_count_is_topic_count"] is False
    assert ag["candidate_edges_default"] == "HOLD"
    assert ag["rights_promotion_allowed"] is False
    assert ag["scientific_evidence_promotion_allowed"] is False
    assert ag["truth_inference_allowed"] is False
    assert ag["drive_access_performed"] is False
    return True


def main() -> int:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    agg = json.loads(AGG.read_text(encoding="utf-8"))
    validate(batch, agg)
    print("AKASHICNET v0.7.12 WIKISPINE PASS", {"new_persons": 5, "resolved_high_precision": 51, "pending": 2})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
