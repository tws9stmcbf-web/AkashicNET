#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "references/big-questions/BQ004/spec-v0.1.json"
ASSESSMENT = ROOT / "references/big-questions/BQ004/progress-assessment-v0.1.json"
AGENDA = ROOT / "references/big-questions/BQ004/research-agenda-v0.1.json"
ARCH = ROOT / "references/big-questions/architecture-v0.1.json"

EXPECTED_CHAIN = [
    "TRANSFORMATIVE_EXPERIENCE",
    "SELF_AND_VALUE_CHANGE",
    "DURABLE_COMPASSIONATE_BEHAVIOR",
    "COMMUNITY_AND_INSTITUTIONAL_CHANGE",
    "HUMAN_AND_ECOLOGICAL_FLOURISHING",
]
EXPECTED_MODELS = {
    "MODEL-BQ004-TRANSIENT-STATE",
    "MODEL-BQ004-INTEGRATION",
    "MODEL-BQ004-SOCIAL-REINFORCEMENT",
    "MODEL-BQ004-STRUCTURAL-CONSTRAINT",
    "MODEL-BQ004-MULTILEVEL",
}
EXPECTED_OUTCOMES = {
    "observable_helping_and_generosity",
    "nonviolence_and_conflict_reduction",
    "prejudice_and_dehumanization_reduction",
    "community_care_and_belonging",
    "ecological_stewardship_behavior",
    "institutional_policy_and_incentive_change",
    "durability_and_adverse_effects",
}
EXPECTED_AXES = {
    "inner_experience_to_self_change": 2,
    "self_change_to_observable_behavior": 2,
    "behavior_to_community_change": 1,
    "community_to_institutional_change": 1,
    "institutional_to_ecological_flourishing": 1,
    "harms_equity_and_cultural_governance": 2,
}
EXPECTED_PRIORITIES = [f"BQ004-P{i:02d}" for i in range(1, 13)]
EXPECTED_CULTURAL_GOVERNANCE = {
    "indigenous_and_lineage_knowledge_is_not_generic_evidence",
    "community_authority_permission_and_care_required",
    "restricted_knowledge_must_remain_restricted",
    "benefit_sharing_and_non_extractive_research_required",
    "traditions_must_not_be_collapsed_into_one_path",
}
FALSE_GUARDS = {
    "canonical_promotion_applied",
    "public_synthesis_updated",
    "website_updated",
    "truth_inference_allowed",
    "scientific_evidence_promotion_allowed",
    "rights_promotion_allowed",
}


def fail(message):
    raise ValueError(message)


def require_false(mapping, keys, label):
    if not isinstance(mapping, dict):
        fail(f"{label} missing")
    for key in keys:
        if mapping.get(key) is not False:
            fail(f"{label} weakened: {key}")


def validate(spec, assessment, agenda, architecture):
    if spec.get("id") != "BQ004" or spec.get("status") != "UNRESOLVED":
        fail("BQ004 identity/status changed")
    if spec.get("authoring_status") != "REVIEW_CANDIDATE" or spec.get("public_beta_gate") is not False:
        fail("BQ004 must remain a gated review candidate")
    if spec.get("causal_chain") != EXPECTED_CHAIN:
        fail("BQ004 causal chain changed")

    boundary = spec.get("causal_boundary")
    if not isinstance(boundary, dict) or set(boundary) != {
        "transformative_experience_is_sufficient_cause",
        "correlation_implies_transformation",
        "self_report_is_behavioral_outcome",
        "individual_change_implies_institutional_change",
        "compassionate_intention_guarantees_benefit",
    }:
        fail("causal boundary changed")
    if any(value is not False for value in boundary.values()):
        fail("causal boundary must remain fail-closed")

    model_items = spec.get("models", [])
    if {item.get("model_id") for item in model_items} != EXPECTED_MODELS or len(model_items) != len(EXPECTED_MODELS):
        fail("competing model set changed")
    if any(item.get("status") != "UNRESOLVED" for item in model_items):
        fail("competing models must remain unresolved")
    if any(claim.get("supports_models") != [] for claim in spec.get("claims", [])):
        fail("BQ004 model support promotion")

    outcomes = spec.get("outcome_families", [])
    if set(outcomes) != EXPECTED_OUTCOMES or len(outcomes) != len(EXPECTED_OUTCOMES):
        fail("outcome family set changed")

    for key in ("truth_inference_allowed", "edge_state_may_upgrade_evidence"):
        if spec.get("graph", {}).get(key) is not False:
            fail(f"BQ004 graph guard weakened: {key}")
    guards = spec.get("promotion_guards", {})
    if guards.get("rights_promotion_allowed") is not False or guards.get("scientific_truth_inference_allowed") is not False:
        fail("BQ004 promotion guards weakened")

    cultural = spec.get("cultural_governance")
    if not isinstance(cultural, dict) or set(cultural) != EXPECTED_CULTURAL_GOVERNANCE:
        fail("BQ004 cultural governance requirements changed")
    if any(cultural.get(key) is not True for key in EXPECTED_CULTURAL_GOVERNANCE):
        fail("BQ004 cultural governance must remain fail-closed")

    if assessment.get("status") != "REVIEW_CANDIDATE" or assessment.get("question_id") != "BQ004":
        fail("assessment identity/status changed")
    if assessment.get("question_status") != "UNRESOLVED":
        fail("assessment must remain unresolved")
    progress = assessment.get("overall_progress", {})
    if progress.get("level") != 3 or progress.get("maximum") != 10:
        fail("overall progress must remain Level 3/10")
    meaning = progress.get("meaning", "").lower()
    if "does not estimate" not in meaning or "planetary transformation" not in meaning:
        fail("progress-is-not-truth boundary missing")

    axes = assessment.get("axis_assessments", [])
    axis_map = {item.get("axis"): item for item in axes}
    if set(axis_map) != set(EXPECTED_AXES) or len(axis_map) != len(axes):
        fail("assessment axis set changed")
    for axis, level in EXPECTED_AXES.items():
        if axis_map[axis].get("level") != level or axis_map[axis].get("maximum") != 10:
            fail(f"assessment axis changed: {axis}")
    require_false(assessment.get("governance"), FALSE_GUARDS | {"model_edges_upgrade_evidence"}, "assessment guard")

    if agenda.get("status") != "REVIEW_CANDIDATE" or agenda.get("question_id") != "BQ004":
        fail("research agenda identity/status changed")
    if agenda.get("question_status") != "UNRESOLVED":
        fail("research agenda must remain unresolved")
    priority_items = agenda.get("priorities", [])
    if [item.get("priority_id") for item in priority_items] != EXPECTED_PRIORITIES:
        fail("research priority identity/order changed")
    if [item.get("rank") for item in priority_items] != list(range(1, 13)):
        fail("research priority ranks changed")
    if any(not item.get("required_outcomes") for item in priority_items):
        fail("research priorities require measurable outcomes")
    community = agenda.get("community_role", {})
    if "cannot establish causation" not in community.get("evidence_boundary", ""):
        fail("community evidence boundary weakened")
    require_false(agenda.get("governance"), FALSE_GUARDS | {"accepted_evidence_batch"}, "research agenda guard")

    if "BQ004" in architecture.get("questions", {}):
        fail("BQ004 must not enter the canonical questions registry without an accepted evidence batch")
    reg = architecture.get("authoring_candidates", {}).get("BQ004", {})
    if reg.get("registration_status") != "REVIEW_CANDIDATE" or reg.get("public_beta_gate") is not False:
        fail("BQ004 authoring-candidate gate changed")
    if reg.get("canonical_registration_applied") is not False or reg.get("accepted_evidence_batches") != []:
        fail("BQ004 canonical acceptance must remain unapplied")
    if reg.get("spec") != "references/big-questions/BQ004/spec-v0.1.json":
        fail("BQ004 spec registration changed")
    if reg.get("review_candidates") != [
        "references/big-questions/BQ004/progress-assessment-v0.1.json",
        "references/big-questions/BQ004/research-agenda-v0.1.json",
    ]:
        fail("BQ004 review-candidate registry changed")


def main():
    try:
        validate(
            json.loads(SPEC.read_text(encoding="utf-8")),
            json.loads(ASSESSMENT.read_text(encoding="utf-8")),
            json.loads(AGENDA.read_text(encoding="utf-8")),
            json.loads(ARCH.read_text(encoding="utf-8")),
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ004 AUTHORING FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ004 AUTHORING PASS: Level 3 review candidate; causal chain documented; no evidence accepted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
