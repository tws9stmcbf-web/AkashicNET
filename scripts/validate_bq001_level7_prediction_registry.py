#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "references/big-questions/BQ001/prediction-registry-level7-review-candidate-v0.1.json"
SPEC = ROOT / "references/big-questions/BQ001/spec-v0.1.json"
BATCH1 = ROOT / "references/big-questions/BQ001/evidence-batch1-v0.1.json"
BATCH3 = ROOT / "references/big-questions/BQ001/evidence-batch3-v0.1.json"

EXPECTED_MODELS = {"MODEL-BQ001-BIOLOGICAL-DEPENDENCE", "MODEL-BQ001-CONTINUITY"}
EXPECTED_TESTS = {
    "TEST-BQ001-RESUSCITATION-TIMELOCK",
    "TEST-BQ001-PASTLIFE-PROSPECTIVE",
    "TEST-BQ001-INDEPENDENT-REPLICATION",
}
EXPECTED_SAFEGUARDS = {
    "guardian_consent_required",
    "child_assent_when_developmentally_possible",
    "data_minimisation_required",
    "public_identification_forbidden",
    "family_contact_pressure_forbidden",
    "culturally_situated_interpretation_required",
}
EXPECTED_CANONICAL_INPUTS = {
    "references/big-questions/BQ001/spec-v0.1.json",
    "references/big-questions/BQ001/evidence-batch1-v0.1.json",
    "references/big-questions/BQ001/evidence-batch3-v0.1.json",
    "references/big-questions/BQ001/public-synthesis-v0.1.json",
}
EXPECTED_MATURITY_MEANING = (
    "Research-method maturity only; not truth probability, evidence strength, model support, "
    "or readiness for canonical or public promotion."
)
FALSE_GUARDS = {
    "canonical_promotion_applied",
    "evidence_promotion_applied",
    "public_synthesis_updated",
    "website_updated",
    "truth_inference_allowed",
    "scientific_evidence_promotion_allowed",
    "rights_promotion_allowed",
    "privacy_posture_changed",
    "cultural_safeguarding_relaxed",
}


def fail(message):
    raise ValueError(message)


def nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def validate(registry, spec, batch1, batch3):
    if registry.get("status") != "REVIEW_CANDIDATE":
        fail("prediction registry must remain a review candidate")
    if registry.get("question_id") != "BQ001" or registry.get("question_status") != "UNRESOLVED":
        fail("BQ001 must remain UNRESOLVED")

    maturity = registry.get("maturity", {})
    if (
        maturity.get("current_level") != 6
        or maturity.get("candidate_level") != 7
        or maturity.get("candidate_level_name") != "PREDICTIONS_DEFINED"
    ):
        fail("registry must describe the bounded Level 6 to Level 7 transition")
    if maturity.get("candidate_level_applied") is not False:
        fail("Level 7 may not be applied before review")
    if maturity.get("meaning") != EXPECTED_MATURITY_MEANING:
        fail("maturity meaning must deny truth, evidence, model-support and promotion inferences")

    spec_models = {item.get("model_id") for item in spec.get("models", [])}
    models = registry.get("models", [])
    if spec_models != EXPECTED_MODELS or {item.get("model_id") for item in models} != EXPECTED_MODELS:
        fail("competing model identities changed")
    if len(models) != 2:
        fail("exactly two competing models required")
    all_prediction_ids = []
    all_challenge_ids = []
    for model in models:
        if not nonempty_string(model.get("operational_scope")):
            fail("every model requires a substantive operational scope")
        if model.get("status") != "UNRESOLVED" or model.get("supports_models") != []:
            fail("model status or support boundary promoted")
        predictions = model.get("predictions", [])
        challenges = model.get("potential_disconfirming_observations", [])
        if len(predictions) < 2 or len(challenges) < 2:
            fail("each model requires predictions and potential disconfirming observations")
        prediction_ids = [item.get("prediction_id") for item in predictions]
        if len(set(prediction_ids)) != len(prediction_ids) or any(
            not nonempty_string(item.get(key))
            for item in predictions
            for key in ("prediction_id", "statement", "boundary")
        ):
            fail("predictions require unique IDs and substantive statements and boundaries")
        all_prediction_ids.extend(prediction_ids)
        challenge_ids = [item.get("observation_id") for item in challenges]
        if len(set(challenge_ids)) != len(challenge_ids) or any(
            not nonempty_string(item.get(key))
            for item in challenges
            for key in ("observation_id", "statement")
        ):
            fail("potential disconfirming observations require unique IDs and substantive statements")
        all_challenge_ids.extend(challenge_ids)
        if any(item.get("not_decisive_alone") is not True for item in challenges):
            fail("disconfirming observations must preserve auxiliary-assumption caution")
    if len(set(all_prediction_ids)) != len(all_prediction_ids) or len(set(all_challenge_ids)) != len(all_challenge_ids):
        fail("prediction and challenge IDs must be unique across all models")

    combined_record_ids = all_prediction_ids + all_challenge_ids
    if len(set(combined_record_ids)) != len(combined_record_ids):
        fail("IDs must be unique across prediction and challenge record kinds")

    tests = registry.get("discriminating_tests", [])
    if {item.get("test_id") for item in tests} != EXPECTED_TESTS or len(tests) != 3:
        fail("discriminating test set changed")
    for test in tests:
        if not nonempty_string(test.get("domain")) or not nonempty_string(test.get("design")):
            fail("each discriminating test requires a substantive domain and design")
        rules = test.get("outcome_rules", {})
        if set(rules) != {"biological_dependence_strengthened", "continuity_strengthened", "neutral_or_ambiguous"}:
            fail("each test requires symmetric and neutral outcome rules")
        if any(not nonempty_string(value) for value in rules.values()):
            fail("outcome rules must contain substantive symmetric and neutral statements")
        if len({" ".join(value.split()).casefold() for value in rules.values()}) != 3:
            fail("outcome rule statements must be distinct")
    past_life = next(item for item in tests if item.get("test_id") == "TEST-BQ001-PASTLIFE-PROSPECTIVE")
    safeguards = past_life.get("safeguards", {})
    if set(safeguards) != EXPECTED_SAFEGUARDS or any(value is not True for value in safeguards.values()):
        fail("child privacy and cultural safeguards must remain enabled")

    source_scope = registry.get("source_scope", {})
    canonical_inputs = set(source_scope.get("canonical_inputs", []))
    if canonical_inputs != EXPECTED_CANONICAL_INPUTS or any(not (ROOT / path).is_file() for path in canonical_inputs):
        fail("canonical provenance inputs changed or do not exist")
    known_ids = {item.get("source_id") for item in batch1.get("sources", []) + batch3.get("sources", [])}
    used_ids = set(source_scope.get("source_ids_used_for_design_context_only", []))
    if not used_ids or not used_ids.issubset(known_ids):
        fail("design-context source provenance is invalid")
    if source_scope.get("new_evidence_added") is not False:
        fail("prediction registry cannot silently add evidence")
    if source_scope.get("design_context_does_not_create_model_support") is not True:
        fail("design context must not create model support")

    methods = registry.get("method_rules", {})
    required_true = {
        "null_results_retained", "misses_retained", "protocol_deviations_retained",
        "exploratory_analyses_labelled", "absence_of_explanation_is_not_positive_evidence",
        "failure_of_one_model_does_not_prove_another", "anomaly_is_not_identity_continuity",
        "source_count_does_not_advance_level",
    }
    if any(methods.get(key) is not True for key in required_true):
        fail("methodological guard missing or weakened")

    rights = registry.get("rights", {})
    if rights.get("record_type") != "methodology_metadata_and_bounded_summary":
        fail("rights scope changed")
    for key in ("full_text_republished", "audio_or_transcript_republished", "quotations_republished"):
        if rights.get(key) is not False:
            fail("rights boundary weakened")

    governance = registry.get("governance", {})
    if governance.get("question_status") != "UNRESOLVED":
        fail("governed question status changed")
    if governance.get("accepted_canonical_edges") != 0 or governance.get("supports_models") != []:
        fail("canonical/model edges must remain empty")
    for key in FALSE_GUARDS:
        if governance.get(key) is not False:
            fail(f"governance guard weakened: {key}")


def main():
    try:
        validate(
            json.loads(REGISTRY.read_text(encoding="utf-8")),
            json.loads(SPEC.read_text(encoding="utf-8")),
            json.loads(BATCH1.read_text(encoding="utf-8")),
            json.loads(BATCH3.read_text(encoding="utf-8")),
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ001 LEVEL 7 PREDICTION REGISTRY FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ001 LEVEL 7 PREDICTION REGISTRY PASS: review candidate; BQ001 UNRESOLVED; accepted edges 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
