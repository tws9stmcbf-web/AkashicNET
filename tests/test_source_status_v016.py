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
    with pytest.raises(AssertionError, match="reserved hostname"):
        validator.validate(data)


def test_synthetic_fixture_rejects_reserved_text_on_real_hostname() -> None:
    data = copy.deepcopy(SYNTHETIC)
    data["source_nodes"][0]["original_url"] = "https://example.com/.example.invalid/real"
    with pytest.raises(AssertionError, match="reserved hostname"):
        validator.validate(data)


def test_synthetic_evidence_url_must_be_reserved() -> None:
    data = copy.deepcopy(SYNTHETIC)
    event(data, "RETRACTED")["evidence"]["notice_url"] = "https://example.com/retraction"
    with pytest.raises(AssertionError, match="reserved hostname"):
        validator.validate(data)


@pytest.mark.parametrize("status", ["TITLE_CHANGED", "RETRACTED", "DELETED"])
def test_synthetic_terminal_status_requires_structured_confirmation(status: str) -> None:
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observed_status"] = "DELETED" if status != "DELETED" else "TITLE_CHANGED"
    with pytest.raises(AssertionError, match="affirmative structured evidence"):
        validator.validate(data)


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("TITLE_CHANGED", "No title-change occurred."),
        ("RETRACTED", "The work was not retracted."),
        ("DELETED", "The source was not deleted."),
    ],
)
def test_synthetic_terminal_status_rejects_negated_evidence(status: str, observation: str) -> None:
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("TITLE_CHANGED", "The title-change wasn't observed."),
        ("TITLE_CHANGED", "The title didn’t change."),
        ("RETRACTED", "The work hasn't been retracted."),
        ("DELETED", "The source wasn't deleted."),
        ("TITLE_CHANGED", "The title-change hasn't occurred."),
        ("RETRACTED", "A retraction notice says the work hasn't undergone retraction."),
        ("DELETED", "Deletion hasn't occurred."),
        ("RETRACTED", "A retraction notice says the work hadn't undergone retraction."),
        ("DELETED", "The source haven’t been deleted."),
        ("TITLE_CHANGED", "The title-change has explicitly not occurred."),
    ],
)
def test_synthetic_terminal_status_rejects_negation_contractions(
    status: str, observation: str
) -> None:
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


def test_synthetic_fixture_cannot_appear_reviewed() -> None:
    data = copy.deepcopy(SYNTHETIC)
    data["events"][0]["human_review_state"] = "REVIEWED_NO_PROMOTION"
    with pytest.raises(AssertionError, match="cannot be marked reviewed"):
        validator.validate(data)


@pytest.mark.parametrize("separator", [";", ".", ":"])
@pytest.mark.parametrize("status,affirmative", [
    ("TITLE_CHANGED", "An explicit title-change was recorded"),
    ("RETRACTED", "A retraction notice confirms the work was retracted"),
    ("DELETED", "The source was deleted"),
])
def test_affirmative_status_preserves_separate_safety_disclaimer(status, affirmative, separator):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = (
        f"{affirmative}{separator} its claims were not automatically deemed false."
    )
    validator.validate(data)


@pytest.mark.parametrize("status,concept", [
    ("TITLE_CHANGED", "title-change"), ("RETRACTED", "retraction"), ("DELETED", "deletion"),
])
@pytest.mark.parametrize("spacing", [" ", "\n", "\t"])
def test_same_clause_adverb_negation_still_rejected(status, concept, spacing):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = f"The {concept} has{spacing}explicitly not occurred."
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


@pytest.mark.parametrize("observation", [
    "A title-change check found the title did not actually change.",
    "A title-change check found the title had not actually changed.",
    "A title-change check found the title has never actually changed.",
    "A title-change check found that the title failed to change.",
    "A title-change check found that the title failure to change was recorded.",
    "A title-change check found the title's failure to change.",
    "A title-change check found the title’s failure to change.",
])
def test_split_title_change_denial_rejected(observation):
    data = copy.deepcopy(SYNTHETIC)
    event(data, "TITLE_CHANGED")["evidence"]["observation"] = observation
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


@pytest.mark.parametrize("separator", [";", ".", ":"])
@pytest.mark.parametrize("status,affirmative", [
    ("TITLE_CHANGED", "title-change occurred"),
    ("RETRACTED", "a retraction notice confirms the work was retracted"),
    ("DELETED", "deletion occurred"),
])
def test_leading_safety_disclaimer_does_not_negate_status(status, affirmative, separator):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = f"Claims are not deemed false{separator} {affirmative}."
    validator.validate(data)


@pytest.mark.parametrize("status,concept", [
    ("TITLE_CHANGED", "title-change"), ("RETRACTED", "retraction"), ("DELETED", "deletion"),
])
@pytest.mark.parametrize("denial", ["never occurred", "has, apparently, not occurred", "has, for now, not occurred", "has, so far, not occurred", "failed to occur", "failure to occur", "without confirmation", "has no confirmation"])
def test_all_post_concept_negators_and_comma_modifiers(status, concept, denial):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = f"A {concept} notice says the {concept} {denial}."
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


@pytest.mark.parametrize("seeking", ["finding any evidence", "detecting independent evidence"])
def test_without_evidence_seeking_negates_terminal_status(seeking):
    data = copy.deepcopy(SYNTHETIC)
    event(data, "RETRACTED")["evidence"]["observation"] = (
        f"A retraction notice was filed without {seeking} that the work was retracted."
    )
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        (
            "TITLE_CHANGED",
            "An explicit title-change was recorded without altering the original URL.",
        ),
        (
            "RETRACTED",
            "A retraction notice confirms the work was retracted without automatically deeming its claims false.",
        ),
        (
            "RETRACTED",
            "A retraction notice confirms the work was retracted without deleting supporting evidence.",
        ),
        (
            "DELETED",
            "The source was deleted without removing its preserved provenance.",
        ),
    ],
)
def test_affirmative_status_allows_benign_without_consequences(
    status: str, observation: str
) -> None:
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    validator.validate(data)


@pytest.mark.parametrize("status,affirmative", [
    ("TITLE_CHANGED", "An explicit title-change was recorded"),
    ("RETRACTED", "A retraction notice confirms the work was retracted"),
    ("DELETED", "The source was deleted"),
])
@pytest.mark.parametrize("ordering", ["status_first", "disclaimer_first"])
def test_coordinating_comma_starts_separate_clause(status, affirmative, ordering):
    data = copy.deepcopy(SYNTHETIC)
    if ordering == "status_first":
        observation = f"{affirmative}, but its claims were not deemed false."
    else:
        observation = f"Claims were not deemed false, but {affirmative.lower()}."
    event(data, status)["evidence"]["observation"] = observation
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
