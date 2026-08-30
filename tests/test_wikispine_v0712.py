import copy
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_wikispine_v0712.py"
spec = importlib.util.spec_from_file_location("wikispine_v0712", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

BATCH = json.loads((ROOT / "references" / "community" / "wikispine-batch-m-consciousness-researchers-v0.7.12.json").read_text(encoding="utf-8"))
AGG = json.loads((ROOT / "references" / "community" / "wikispine-entity-aggregate-v0.7.12.json").read_text(encoding="utf-8"))


def test_current_contract_passes():
    assert mod.validate(BATCH, AGG)


@pytest.mark.parametrize("key,value", [
    ("candidate_edges_default", "ACCEPT"),
    ("entity_count_is_topic_count", True),
    ("rights_promotion_allowed", True),
    ("scientific_evidence_promotion_allowed", True),
    ("truth_inference_allowed", True),
    ("drive_access_performed", True),
])
def test_batch_guardrails_fail_closed(key, value):
    batch = copy.deepcopy(BATCH)
    batch["guardrails"][key] = value
    with pytest.raises(AssertionError):
        mod.validate(batch, AGG)


@pytest.mark.parametrize("field,value", [
    ("semantic_decision", "ACCEPT"),
    ("truth_inference", True),
    ("scientific_evidence", True),
    ("resolution_state", "PROVISIONAL"),
])
def test_record_promotion_mutations_fail_closed(field, value):
    batch = copy.deepcopy(BATCH)
    batch["records"][0][field] = value
    with pytest.raises(AssertionError):
        mod.validate(batch, AGG)


def test_duplicate_qid_fails_closed():
    batch = copy.deepcopy(BATCH)
    batch["records"][1]["wikidata_qid"] = batch["records"][0]["wikidata_qid"]
    with pytest.raises(AssertionError):
        mod.validate(batch, AGG)


def test_aggregate_count_drift_fails_closed():
    agg = copy.deepcopy(AGG)
    agg["resolved_high_precision"] = 52
    with pytest.raises(AssertionError):
        mod.validate(BATCH, agg)


def test_pending_record_cannot_carry_unverified_qid():
    agg = copy.deepcopy(AGG)
    agg["pending_entities"][0]["wikidata_qid"] = "Q999999999"
    with pytest.raises(AssertionError):
        mod.validate(BATCH, agg)


@pytest.mark.parametrize("key,value", [
    ("entity_identity_is_truth", True),
    ("entity_count_is_topic_count", True),
    ("candidate_edges_default", "ACCEPT"),
    ("rights_promotion_allowed", True),
    ("scientific_evidence_promotion_allowed", True),
    ("truth_inference_allowed", True),
    ("drive_access_performed", True),
])
def test_aggregate_guardrails_fail_closed(key, value):
    agg = copy.deepcopy(AGG)
    agg["guardrails"][key] = value
    with pytest.raises(AssertionError):
        mod.validate(BATCH, agg)
