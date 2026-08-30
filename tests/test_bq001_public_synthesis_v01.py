import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_bq001_public_synthesis_v01.py"
spec = importlib.util.spec_from_file_location("validator", MODULE_PATH)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

BASE = json.loads((ROOT / "references" / "big-questions" / "BQ001" / "public-synthesis-v0.1.json").read_text(encoding="utf-8"))


def assert_fails(payload):
    try:
        validator.validate(payload)
    except (AssertionError, KeyError, TypeError):
        return
    raise AssertionError("payload unexpectedly passed validation")


def test_valid_payload_passes():
    validator.validate(copy.deepcopy(BASE))


def test_resolved_status_fails():
    payload = copy.deepcopy(BASE)
    payload["status"] = "RESOLVED"
    assert_fails(payload)


def test_unknown_claim_fails():
    payload = copy.deepcopy(BASE)
    payload["sections"][0]["claim_ids"][0] = "CLAIM-BQ001-INVENTED"
    assert_fails(payload)


def test_unknown_source_fails():
    payload = copy.deepcopy(BASE)
    payload["sections"][0]["source_ids"][0] = "SRC-BQ001-INVENTED"
    assert_fails(payload)


def test_untraced_source_fails():
    payload = copy.deepcopy(BASE)
    payload["sections"][0]["source_ids"] = ["SRC-BQ001-ALLAN-2025"]
    assert_fails(payload)


def test_guard_promotion_fails():
    payload = copy.deepcopy(BASE)
    payload["guards"]["question_resolved"] = True
    assert_fails(payload)
