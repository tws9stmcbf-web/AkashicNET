from __future__ import annotations

import copy
import importlib.util
import json
import time
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
@pytest.mark.parametrize("denial", ["never occurred", "has, apparently, not occurred", "has, for now, not occurred", "has, so far, not occurred", "has, for the moment, not occurred", "has, for a little while, not occurred", "failed to occur", "failure to occur", "without confirmation", "has no confirmation"])
def test_all_post_concept_negators_and_comma_modifiers(status, concept, denial):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = f"A {concept} notice says the {concept} {denial}."
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


@pytest.mark.parametrize("seeking", ["finding any evidence", "finding credible evidence", "detecting independent evidence", "detecting unusually credible evidence"])
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
@pytest.mark.parametrize("coordinator", ["but", "and"])
def test_coordinating_comma_starts_separate_clause(status, affirmative, ordering, coordinator):
    data = copy.deepcopy(SYNTHETIC)
    if ordering == "status_first":
        observation = f"{affirmative}, {coordinator} its claims were not deemed false."
    else:
        observation = f"Claims were not deemed false, {coordinator} {affirmative.lower()}."
    event(data, status)["evidence"]["observation"] = observation
    validator.validate(data)


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("TITLE_CHANGED", "An explicit title-change was recorded, but the archive reported its claims never warranted reclassification."),
        ("RETRACTED", "A retraction notice confirms the work was retracted, but the archive confirmed its claims never warranted reclassification."),
        ("DELETED", "The source was deleted, but the archive confirmed its claims never warranted reclassification."),
    ],
)
def test_past_tense_reporting_clause_preserves_affirmative_status(status, observation):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    validator.validate(data)


@pytest.mark.parametrize("status,concept", [
    ("TITLE_CHANGED", "title-change"), ("RETRACTED", "retraction"), ("DELETED", "deletion"),
])
@pytest.mark.parametrize("modifier", ["as-yet", "up-to-now"])
def test_hyphenated_same_clause_negation_is_rejected(status, concept, modifier):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = (
        f"A {concept} notice says the {concept} has, {modifier}, not occurred."
    )
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("TITLE_CHANGED", "The title-change was recorded and no claims were automatically promoted."),
        ("RETRACTED", "A retraction notice confirms the work was retracted with no automatic falsity inference."),
        ("DELETED", "The source was deleted and no claims were automatically promoted."),
    ],
)
def test_unpunctuated_no_promotion_disclaimer_remains_affirmative(status, observation):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    validator.validate(data)


@pytest.mark.parametrize("status,concept", [
    ("TITLE_CHANGED", "title-change"), ("RETRACTED", "retraction"), ("DELETED", "deletion"),
])
def test_terminal_status_yet_to_occur_is_rejected(status, concept):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = (
        f"A {concept} notice confirms the {concept} has yet to occur."
    )
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("TITLE_CHANGED", "The title-change was not only observed but independently verified."),
        ("RETRACTED", "A retraction notice confirms the work was not only retracted but independently verified."),
        ("DELETED", "The source deletion was not only observed but independently verified."),
    ],
)
def test_not_only_focus_construction_remains_affirmative(status, observation):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    validator.validate(data)


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("DELETED", "The source was deleted, not merely made unavailable."),
        ("RETRACTED", "A retraction notice confirms the work was retracted, not merely corrected."),
        ("DELETED", "The source was deleted, not just made unavailable."),
    ],
)
def test_not_merely_and_not_just_focus_constructions_remain_affirmative(status, observation):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    validator.validate(data)



@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("TITLE_CHANGED", "A title-change check found no change in the title."),
        ("RETRACTED", "A retraction notice says the retraction cannot be confirmed."),
        ("DELETED", "A deletion notice says the deletion cannot be verified."),
        ("RETRACTED", "A retraction notice says the retraction remains unverified."),
        ("DELETED", "A deletion notice says the deletion remains unconfirmed."),
        ("RETRACTED", "A retraction notice says the work was neither retracted nor withdrawn."),
        ("DELETED", "A deletion notice says the source was neither deleted nor removed."),
    ],
)
def test_reverse_title_and_modal_nonconfirmation_are_rejected(status, observation):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("DELETED", "The source was deleted while its provenance remains unconfirmed."),
        ("RETRACTED", "A retraction notice confirms the work was retracted while its original provenance remains unverified."),
    ],
)
def test_unrelated_nonconfirmation_does_not_negate_terminal_status(status, observation):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    validator.validate(data)


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("TITLE_CHANGED", "The title-change was recorded and its claims were not automatically promoted."),
        ("RETRACTED", "A retraction notice confirms the work was retracted and its claims were not automatically promoted."),
        ("DELETED", "The source was deleted and its claims were not automatically promoted."),
    ],
)
def test_unpunctuated_not_promotion_disclaimer_remains_affirmative(status, observation):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    validator.validate(data)


def test_terminal_negation_scan_is_linear_on_long_whitespace() -> None:
    start = time.monotonic()
    assert not validator.terminal_evidence_is_negated(
        "DELETED", "deletion" + " " * 25 + "x"
    )
    assert time.monotonic() - start < 1.0


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("TITLE_CHANGED", "A title-change notice says the title-change was by no means confirmed."),
        ("RETRACTED", "A retraction notice says the retraction was in no way verified."),
        ("DELETED", "A deletion notice says the deletion was by no means confirmed."),
    ],
)
def test_idiomatic_direct_nonconfirmation_is_rejected(status, observation):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("TITLE_CHANGED", "The title-change was recorded after the archive failed to preserve its metadata."),
        ("RETRACTED", "A retraction notice confirms the work was retracted although the archive failed to preserve its metadata."),
        ("DELETED", "The source was deleted after the archive failed to preserve its metadata."),
    ],
)
def test_subordinate_negation_does_not_negate_terminal_status(status, observation):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    validator.validate(data)


def test_unable_to_confirm_rejects_deletion():
    data = copy.deepcopy(SYNTHETIC)
    event(data, "DELETED")["evidence"]["observation"] = (
        "A deletion notice says the archive was unable to confirm the source was deleted."
    )
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


def test_no_doubt_phrase_remains_affirmative():
    data = copy.deepcopy(SYNTHETIC)
    event(data, "DELETED")["evidence"]["observation"] = (
        "A deletion notice says there is no doubt the source was deleted."
    )
    validator.validate(data)


def test_neither_reviewer_phrase_does_not_negate_terminal_status():
    data = copy.deepcopy(SYNTHETIC)
    event(data, "RETRACTED")["evidence"]["observation"] = (
        "A retraction notice confirms the work was retracted; neither reviewer disputed retraction."
    )
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


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("TITLE_CHANGED", "A title-change check confirmed that the title was unchanged."),
        ("RETRACTED", "A retraction notice says the work remains unretracted."),
        ("DELETED", "A deletion notice says the source remains undeleted."),
    ],
)
def test_morphologically_negated_terminal_predicates_are_rejected(status, observation):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    with pytest.raises(AssertionError, match="evidence is negated"):
        validator.validate(data)


@pytest.mark.parametrize(
    ("status", "observation"),
    [
        ("TITLE_CHANGED", "The title-change was not disputed and was independently verified."),
        ("RETRACTED", "A retraction notice confirms the work was retracted; the retraction was not disputed and was independently verified."),
        ("DELETED", "The source deletion was not disputed and was independently verified."),
    ],
)
def test_not_on_unrelated_predicate_does_not_negate_terminal_status(status, observation):
    data = copy.deepcopy(SYNTHETIC)
    event(data, status)["evidence"]["observation"] = observation
    validator.validate(data)
