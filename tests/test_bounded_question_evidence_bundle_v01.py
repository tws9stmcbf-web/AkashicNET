#!/usr/bin/env python3
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_bounded_question_evidence_bundle_v01.py"
FIXTURE = ROOT / "references" / "community" / "bq001-scientific-baseline-batch1.json"

spec = importlib.util.spec_from_file_location("bq_validator", MODULE_PATH)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def load_fixture():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def expect_failure(data, tmp_path):
    path = tmp_path / "bundle.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    try:
        validator.validate(path)
    except AssertionError:
        return
    raise AssertionError("expected fail-closed validation failure")


def test_current_bq001_bundle_passes():
    validator.validate(FIXTURE)


def test_rejects_unknown_epistemic_label(tmp_path):
    data = load_fixture()
    data["epistemic_annotations"][0]["label"] = "Proven Fact"
    expect_failure(data, tmp_path)


def test_rejects_missing_source_provenance(tmp_path):
    data = load_fixture()
    data["evidence_core"]["claims"][0]["provenance"]["source_ids"] = ["MISSING-SOURCE"]
    expect_failure(data, tmp_path)


def test_rejects_model_edge_promotion(tmp_path):
    data = load_fixture()
    data["model_implications"]["model_edges_upgrade_epistemic_label"] = True
    expect_failure(data, tmp_path)


def test_rejects_truth_inference(tmp_path):
    data = load_fixture()
    data["release_invariants"]["truth_inference_allowed"] = True
    expect_failure(data, tmp_path)
