import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_bq001_v01.py"
SPEC_PATH = ROOT / "references" / "big-questions" / "BQ001" / "spec-v0.1.json"

spec = importlib.util.spec_from_file_location("validate_bq001_v01", VALIDATOR_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def payload():
    return json.loads(SPEC_PATH.read_text(encoding="utf-8"))


def test_seed_passes():
    module.validate(payload())


def test_forced_conclusion_fails_closed():
    p = payload()
    p["status"] = "PROVEN_CONTINUITY"
    with pytest.raises(ValueError):
        module.validate(p)


def test_single_model_fails():
    p = payload()
    p["models"] = p["models"][:1]
    with pytest.raises(ValueError):
        module.validate(p)


def test_claim_without_provenance_fails():
    p = payload()
    p["claims"][0]["provenance"] = []
    with pytest.raises(ValueError):
        module.validate(p)


def test_testimony_cannot_be_universalised():
    p = payload()
    c = copy.deepcopy(p["claims"][0])
    c.update({
        "claim_id": "CLAIM-BQ001-TESTIMONY-NEGATIVE",
        "text": "A reported experience proves a universal survival claim.",
        "evidence_label": "Lived Experience/Testimony",
        "reviewed_support": False,
        "universalised": True,
    })
    p["claims"].append(c)
    with pytest.raises(ValueError):
        module.validate(p)


def test_placeholder_cannot_support_established_evidence():
    p = payload()
    p["claims"][0]["source_ids"] = ["SRC-BQ001-SEED-001"]
    with pytest.raises(ValueError):
        module.validate(p)


def test_graph_truth_inference_fails():
    p = payload()
    p["graph"]["truth_inference_allowed"] = True
    with pytest.raises(ValueError):
        module.validate(p)
