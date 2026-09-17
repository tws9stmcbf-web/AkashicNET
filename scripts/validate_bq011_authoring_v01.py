#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "references/big-questions/BQ011/spec-v0.1.json"
ASSESSMENT = ROOT / "references/big-questions/BQ011/progress-assessment-v0.1.json"
AGENDA = ROOT / "references/big-questions/BQ011/research-agenda-v0.1.json"
ARCH = ROOT / "references/big-questions/architecture-v0.1.json"

EXPECTED_CHAIN = [
    "TRANSFORMATIVE_EXPERIENCE",
    "SELF_AND_VALUE_CHANGE",
    "DURABLE_COMPASSIONATE_BEHAVIOR",
    "COMMUNITY_AND_INSTITUTIONAL_CHANGE",
    "HUMAN_AND_ECOLOGICAL_FLOURISHING",
]
EXPECTED_MODELS = {
    "MODEL-BQ011-TRANSIENT-STATE",
    "MODEL-BQ011-INTEGRATION",
    "MODEL-BQ011-SOCIAL-REINFORCEMENT",
    "MODEL-BQ011-STRUCTURAL-CONSTRAINT",
    "MODEL-BQ011-MULTILEVEL",
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
EXPECTED_PRIORITIES = [f"BQ011-P{i:02d}" for i in range(1, 13)]
EXPECTED_CULTURAL_GOVERNANCE = {
    "indigenous_and_lineage_knowledge_is_not_generic_evidence",
    "community_authority_permission_and_care_required",
    "restricted_knowledge_must_remain_restricted",
    "benefit_sharing_and_non_extractive_research_required",
    "traditions_must_not_be_collapsed_into_one_path",
}
EXPECTED_PROMOTION_GUARDS = {
    "testimony_may_not_auto_promote_to_established_evidence": True,
    "transformative_state_may_not_be_presented_as_durable_trait": True,
    "compassionate_intention_may_not_be_presented_as_observed_benefit": True,
    "individual_change_may_not_be_presented_as_system_change": True,
    "correlation_may_not_be_presented_as_causation": True,
    "source_count_may_not_upgrade_evidence": True,
    "semantic_similarity_may_not_upgrade_evidence": True,
    "ai_synthesis_may_not_be_primary_source": True,
    "rights_promotion_allowed": False,
    "scientific_truth_inference_allowed": False,
}
EXPECTED_METHOD_REQUIREMENTS = [
    "Prospective and longitudinal designs where feasible.",
    "Preregistered outcomes and transparent deviations.",
    "Behavioural, third-party, institutional or ecological measures alongside self-report.",
    "Null results, adverse effects and heterogeneous responses retained.",
    "Selection, expectancy, demand-characteristic and social-desirability alternatives assessed.",
    "No metaphysical conclusion inferred from psychological or social outcomes.",
    "Community-led cultural governance, permission and benefit sharing where applicable.",
    "No individual-level change presented as institutional or planetary change without direct measurement.",
]
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
    if spec.get("id") != "BQ011" or spec.get("status") != "UNRESOLVED":
        fail("BQ011 identity/status changed")
    if spec.get("authoring_status") != "REVIEW_CANDIDATE" or spec.get("public_beta_gate") is not False:
        fail("BQ011 must remain a gated review candidate")
    if spec.get("causal_chain") != EXPECTED_CHAIN:
        fail("BQ011 causal chain changed")

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
    claims = spec.get("claims")
    if not isinstance(claims, list) or len(claims) != 1:
        fail("BQ011 must retain exactly one project-state claim")
    claim = claims[0]
    if (
        claim.get("claim_id") != "CLAIM-BQ011-FRAMEWORK-001"
        or claim.get("claim_type") != "PROJECT_STATE"
        or claim.get("scope") != "project_state_only"
        or claim.get("text") != "BQ011 currently has no adjudicated substantive answer or accepted evidence batch."
        or claim.get("uncertainty") != "No causal, clinical, social or metaphysical conclusion is implied."
        or claim.get("source_ids") != []
        or claim.get("supports_models") != []
    ):
        fail("BQ011 project-state claim or no-support boundary changed")

    outcomes = spec.get("outcome_families", [])
    if set(outcomes) != EXPECTED_OUTCOMES or len(outcomes) != len(EXPECTED_OUTCOMES):
        fail("outcome family set changed")

    for key in ("truth_inference_allowed", "edge_state_may_upgrade_evidence"):
        if spec.get("graph", {}).get(key) is not False:
            fail(f"BQ011 graph guard weakened: {key}")
    guards = spec.get("promotion_guards")
    if guards != EXPECTED_PROMOTION_GUARDS:
        fail("BQ011 promotion guards changed or weakened")

    cultural = spec.get("cultural_governance")
    if not isinstance(cultural, dict) or set(cultural) != EXPECTED_CULTURAL_GOVERNANCE:
        fail("BQ011 cultural governance requirements changed")
    if any(cultural.get(key) is not True for key in EXPECTED_CULTURAL_GOVERNANCE):
        fail("BQ011 cultural governance must remain fail-closed")

    if assessment.get("assessment_id") != "BQ011-PROGRESS-ASSESSMENT-V0.1":
        fail("assessment artifact identity changed")
    if assessment.get("status") != "REVIEW_CANDIDATE" or assessment.get("question_id") != "BQ011":
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

    if agenda.get("agenda_id") != "BQ011-RESEARCH-AGENDA-V0.1":
        fail("agenda artifact identity changed")
    if agenda.get("status") != "REVIEW_CANDIDATE" or agenda.get("question_id") != "BQ011":
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
    if agenda.get("methodological_requirements") != EXPECTED_METHOD_REQUIREMENTS:
        fail("research methodology boundaries changed")
    community = agenda.get("community_role")
    if not isinstance(community, dict) or set(community) != {"n2n_function", "evidence_boundary", "consent_boundary"}:
        fail("community role boundaries changed")
    if "cannot establish causation" not in community["evidence_boundary"]:
        fail("community evidence boundary weakened")
    if "without permission" not in community["consent_boundary"]:
        fail("community consent boundary weakened")
    require_false(agenda.get("governance"), FALSE_GUARDS | {"accepted_evidence_batch"}, "research agenda guard")

    if "BQ011" in architecture.get("questions", {}):
        fail("BQ011 must not enter the canonical questions registry without an accepted evidence batch")
    reg = architecture.get("authoring_candidates", {}).get("BQ011", {})
    if reg.get("registration_status") != "REVIEW_CANDIDATE" or reg.get("public_beta_gate") is not False:
        fail("BQ011 authoring-candidate gate changed")
    if reg.get("canonical_registration_applied") is not False or reg.get("accepted_evidence_batches") != []:
        fail("BQ011 canonical acceptance must remain unapplied")
    if reg.get("candidate_path") != "references/big-questions/BQ011":
        fail("BQ011 candidate path changed")
    if reg.get("spec") != "references/big-questions/BQ011/spec-v0.1.json":
        fail("BQ011 spec registration changed")
    if reg.get("review_candidates") != [
        "references/big-questions/BQ011/progress-assessment-v0.1.json",
        "references/big-questions/BQ011/research-agenda-v0.1.json",
    ]:
        fail("BQ011 review-candidate registry changed")


def main():
    try:
        validate(
            json.loads(SPEC.read_text(encoding="utf-8")),
            json.loads(ASSESSMENT.read_text(encoding="utf-8")),
            json.loads(AGENDA.read_text(encoding="utf-8")),
            json.loads(ARCH.read_text(encoding="utf-8")),
        )
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ011 AUTHORING FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ011 AUTHORING PASS: Level 3 review candidate; causal chain documented; no evidence accepted")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
