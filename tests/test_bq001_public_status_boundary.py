import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_bq001_public_status_boundary.py"
spec = importlib.util.spec_from_file_location("bq001_status", SCRIPT)
bq001_status = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bq001_status)

PAGE_TEXT = (ROOT / "website" / "app" / "big-questions" / "bq001" / "page.tsx").read_text(encoding="utf-8")
SYNTHESIS = json.loads(
    (ROOT / "references" / "big-questions" / "BQ001" / "public-synthesis-v0.1.json").read_text(encoding="utf-8")
)


def test_current_page_matches_canonical_synthesis():
    assert bq001_status.validate(PAGE_TEXT, SYNTHESIS)


@pytest.mark.parametrize("required", bq001_status.REQUIRED)
def test_required_boundaries_fail_closed(required):
    mutated = PAGE_TEXT.replace(required, "REMOVED_BOUNDARY", 1)
    with pytest.raises(AssertionError):
        bq001_status.validate(mutated, SYNTHESIS)


@pytest.mark.parametrize("forbidden", bq001_status.FORBIDDEN)
def test_forbidden_status_phrases_fail_closed(forbidden):
    mutated = PAGE_TEXT + f"\n{forbidden}\n"
    with pytest.raises(AssertionError):
        bq001_status.validate(mutated, SYNTHESIS)


def test_page_status_cannot_drift_from_synthesis():
    mutated = PAGE_TEXT.replace("CURRENT STATUS · UNRESOLVED", "CURRENT STATUS · OPEN", 1)
    with pytest.raises(AssertionError, match="page status must match"):
        bq001_status.validate(mutated, SYNTHESIS)


def test_page_conclusion_cannot_drift_from_synthesis():
    mutated = PAGE_TEXT.replace("CURRENT CONCLUSION · UNRESOLVED", "CURRENT CONCLUSION · OPEN", 1)
    with pytest.raises(AssertionError, match="page conclusion must match"):
        bq001_status.validate(mutated, SYNTHESIS)


def test_synthesis_status_and_conclusion_must_agree():
    mutated = copy.deepcopy(SYNTHESIS)
    mutated["conclusion"]["status"] = "OPEN"
    with pytest.raises(AssertionError, match="status and conclusion must agree"):
        bq001_status.validate(PAGE_TEXT, mutated)


def test_each_competing_model_requires_status():
    mutated = copy.deepcopy(SYNTHESIS)
    mutated["competing_models"][0].pop("status")
    with pytest.raises(AssertionError, match="each BQ001 model requires status"):
        bq001_status.validate(PAGE_TEXT, mutated)


def test_page_model_statuses_cannot_drift_from_synthesis():
    mutated = copy.deepcopy(SYNTHESIS)
    mutated["competing_models"][0]["status"] = "OPEN"
    with pytest.raises(AssertionError, match="competing-model statuses must match"):
        bq001_status.validate(PAGE_TEXT, mutated)


def test_bq001_identity_is_required():
    mutated = copy.deepcopy(SYNTHESIS)
    mutated["question_id"] = "BQ999"
    with pytest.raises(AssertionError, match="must identify BQ001"):
        bq001_status.validate(PAGE_TEXT, mutated)
