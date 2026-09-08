from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_source_status_v016",
    ROOT / "scripts/validate_source_status_v016.py",
)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)

FIXTURE = json.loads(
    (ROOT / "references/source-status-fixture-v0.16.json").read_text(encoding="utf-8")
)
SLICE2 = json.loads(
    (ROOT / "references/source-status-fixture-v0.16-slice2.json").read_text(encoding="utf-8")
)
SYNTHETIC = json.loads(
    (ROOT / "references/source-status-fixture-v0.16-synthetic.json").read_text(encoding="utf-8")
)


def mutated() -> dict:
    return copy.deepcopy(FIXTURE)


def event(data: dict, status: str) -> dict:
    return next(item for item in data["events"] if item["status"] == status)


def test_fixture_passes() -> None:
    validator.validate(mutated())


def test_original_url_mutation_fails() -> None:
    data = mutated()
    event(data, "AVAILABLE")["original_url"] = "https://example.org/replacement"
    with pytest.raises(AssertionError, match="original URL changed"):
        validator.validate(data)


def test_locator_binding_mutation_fails() -> None:
    data = mutated()
    event(data, "CORRECTED")["source_node_id"] = "SRC-NOT-IN-GRAPH"
    with pytest.raises(AssertionError, match="unbound source node"):
        validator.validate(data)


def test_redirect_cannot_replace_original() -> None:
    data = mutated()
    event(data, "REDIRECTED")["transition"]["replacement_applied"] = True
    with pytest.raises(AssertionError, match="replaced original URL"):
        validator.validate(data)


def test_redirect_requires_distinct_endpoint() -> None:
    data = mutated()
    redirect = event(data, "REDIRECTED")
    redirect["transition"]["to_url"] = redirect["transition"]["from_url"]
    with pytest.raises(AssertionError, match="target is unchanged"):
        validator.validate(data)


def test_correction_cannot_become_unverified_retraction() -> None:
    data = mutated()
    corrected = event(data, "CORRECTED")
    corrected["status"] = "RETRACTED"
    data["coverage"]["implemented_statuses"] = [
        "AVAILABLE", "REDIRECTED", "RETRACTED", "UNAVAILABLE_INDETERMINATE"
    ]
    data["coverage"]["verified_gaps"] = [
        "TITLE_CHANGED", "CORRECTED", "DELETED",
        "DUPLICATE_REFERENCE_CANDIDATE", "PROVENANCE_INCOMPLETE"
    ]
    with pytest.raises(AssertionError, match="retraction evidence is not explicit"):
        validator.validate(data)


@pytest.mark.parametrize("guard", ["truth", "evidence", "rights", "identity", "edge_acceptance"])
def test_no_automatic_promotion(guard: str) -> None:
    data = mutated()
    data["promotion_guards"][guard] = True
    with pytest.raises(AssertionError, match="promotion guards"):
        validator.validate(data)


def test_slice2_fixture_passes() -> None:
    validator.validate(copy.deepcopy(SLICE2))


def test_duplicate_candidate_cannot_imply_merge() -> None:
    data = copy.deepcopy(SLICE2)
    duplicate = event(data, "DUPLICATE_REFERENCE_CANDIDATE")
    duplicate["evidence"]["observation"] = "Records were merged automatically."
    with pytest.raises(AssertionError, match="non-merge boundary"):
        validator.validate(data)


def test_provenance_gap_must_remain_explicit() -> None:
    data = copy.deepcopy(SLICE2)
    incomplete = event(data, "PROVENANCE_INCOMPLETE")
    incomplete["evidence"]["observation"] = "All provenance is complete."
    with pytest.raises(AssertionError, match="incomplete provenance"):
        validator.validate(data)


def test_synthetic_terminal_status_fixture_passes() -> None:
    validator.validate(copy.deepcopy(SYNTHETIC))


def test_synthetic_fixture_cannot_use_real_url() -> None:
    data = copy.deepcopy(SYNTHETIC)
    data["source_nodes"][0]["original_url"] = "https://example.com/real"
    with pytest.raises(AssertionError, match="reserved URL"):
        validator.validate(data)


def test_synthetic_fixture_cannot_appear_reviewed() -> None:
    data = copy.deepcopy(SYNTHETIC)
    data["events"][0]["human_review_state"] = "REVIEWED_NO_PROMOTION"
    with pytest.raises(AssertionError, match="cannot be marked reviewed"):
        validator.validate(data)


def test_synthetic_retraction_cannot_infer_falsity() -> None:
    data = copy.deepcopy(SYNTHETIC)
    event(data, "RETRACTED")["truth_inference"] = "FALSE"
    with pytest.raises(AssertionError, match="automatic inference"):
        validator.validate(data)


def test_synthetic_disclaimer_is_required() -> None:
    data = copy.deepcopy(SYNTHETIC)
    data["synthetic_disclaimer"] = "Test data."
    with pytest.raises(AssertionError, match="non-observational disclaimer"):
        validator.validate(data)
