import importlib.util
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_canonical_adjudication_v070.py"
spec = importlib.util.spec_from_file_location("canonical_validator", MODULE_PATH)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


def base_record():
    return {
        "relationship": "REPRESENTS_WORK",
        "decision": "HOLD",
        "signals": ["SHA256_EQUAL"],
        "evidence_class": "BYTE_IDENTITY_ONLY",
        "rationale": "Insufficient evidence.",
        "provenance": [],
        "rights_promoted": False,
        "public_release_promoted": False,
        "scientific_evidence_promoted": False,
        "safety_or_efficacy_promoted": False,
    }


def test_hold_byte_identity_is_allowed():
    validator.validate_record(base_record(), 0)


def test_accept_byte_identity_only_fails():
    record = base_record()
    record.update({"decision": "ACCEPT", "provenance": [{"source_class": "HASH"}]})
    with pytest.raises(ValueError):
        validator.validate_record(record, 0)


def test_accept_independent_public_evidence_passes():
    record = base_record()
    record.update(
        {
            "decision": "ACCEPT",
            "signals": ["PUBLIC_BIBLIOGRAPHIC_IDENTITY"],
            "evidence_class": "INDEPENDENT_PUBLIC_BIBLIOGRAPHY",
            "rationale": "Public bibliographic evidence explicitly identifies the work.",
            "provenance": [{"source_class": "PUBLIC_BIBLIOGRAPHIC_REFERENCE"}],
        }
    )
    validator.validate_record(record, 0)


def test_private_field_fails():
    record = base_record()
    record["drive_id"] = "private"
    with pytest.raises(ValueError):
        validator.validate_record(record, 0)


def test_side_effect_promotion_fails():
    record = base_record()
    record["rights_promoted"] = True
    with pytest.raises(ValueError):
        validator.validate_record(record, 0)
