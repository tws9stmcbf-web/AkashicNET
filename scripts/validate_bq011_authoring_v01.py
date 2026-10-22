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
# Independent contracts pinned from the reviewed v0.1 candidate.
# Do not derive these expectations from the documents being validated at runtime.
EXPECTED_MODELS = {
    "MODEL-BQ011-TRANSIENT-STATE": {
        "model_id": "MODEL-BQ011-TRANSIENT-STATE",
        "name": "transient_state_model",
        "position": "Experiences of interconnection may be meaningful yet fade without producing durable behavioural or institutional change.",
        "status": "UNRESOLVED"
    },
    "MODEL-BQ011-INTEGRATION": {
        "model_id": "MODEL-BQ011-INTEGRATION",
        "name": "integration_and_practice_model",
        "position": "Durable change depends on repeated practice, psychological integration, supportive relationships and opportunities for action.",
        "status": "UNRESOLVED"
    },
    "MODEL-BQ011-SOCIAL-REINFORCEMENT": {
        "model_id": "MODEL-BQ011-SOCIAL-REINFORCEMENT",
        "name": "social_reinforcement_model",
        "position": "Communities and social norms determine whether compassionate intentions become stable habits or dissipate.",
        "status": "UNRESOLVED"
    },
    "MODEL-BQ011-STRUCTURAL-CONSTRAINT": {
        "model_id": "MODEL-BQ011-STRUCTURAL-CONSTRAINT",
        "name": "structural_constraint_model",
        "position": "Institutional incentives, inequality and material conditions may dominate individual intentions and limit compassionate outcomes.",
        "status": "UNRESOLVED"
    },
    "MODEL-BQ011-MULTILEVEL": {
        "model_id": "MODEL-BQ011-MULTILEVEL",
        "name": "multilevel_transformation_model",
        "position": "Lasting planetary benefit may require interacting individual, relational, institutional and ecological changes rather than a single intervention.",
        "status": "UNRESOLVED"
    }
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
EXPECTED_AXIS_BOUNDARIES = {
    "inner_experience_to_self_change": "Candidate mechanisms are framed, but no evidence batch has been accepted.",
    "self_change_to_observable_behavior": "Self-report must remain separate from observed helping, nonviolence, generosity or stewardship.",
    "behavior_to_community_change": "No reviewed causal pathway from individual change to community outcomes is established.",
    "community_to_institutional_change": "No reviewed evidence shows that transformative experiences alter durable institutional incentives or policy.",
    "institutional_to_ecological_flourishing": "Planetary and ecological outcomes remain an untested research horizon.",
    "harms_equity_and_cultural_governance": "Risks and governance requirements are named but require source-led review and affected-community participation.",
}
EXPECTED_PROJECT_CLAIM = {
    "claim_id": "CLAIM-BQ011-FRAMEWORK-001",
    "claim_type": "PROJECT_STATE",
    "text": "BQ011 currently has no adjudicated substantive answer or accepted evidence batch.",
    "domain": "flourishing_measurement_and_long_term_follow_up",
    "evidence_label": "Established Evidence",
    "provenance": ["references/big-questions/BQ011/spec-v0.1.json"],
    "source_ids": [],
    "reviewed_support": True,
    "scope": "project_state_only",
    "uncertainty": "No causal, clinical, social or metaphysical conclusion is implied.",
    "supports_models": [],
}
EXPECTED_COMMUNITY_ROLE = {
    "n2n_function": "Generate questions, lived-experience signals, counterexamples and candidate patterns for formal review.",
    "evidence_boundary": "Community recurrence and testimony can motivate research but cannot establish causation, efficacy or universal truth.",
    "consent_boundary": "Do not extract personal narratives, cultural material or identifying information without permission.",
}
EXPECTED_OVERALL_PROGRESS = {
    "level": 3,
    "maximum": 10,
    "label": "COMPETING_MODELS_AND_CAUSAL_CHAIN_DOCUMENTED",
    "meaning": "The problem, causal chain, competing models, outcome families and research priorities are documented. This level does not estimate whether any intervention works or whether planetary transformation will occur.",
}
EXPECTED_SCALE = [
    {"level": 1, "label": "QUESTION_FRAMED"},
    {"level": 2, "label": "OUTCOMES_OPERATIONALISED"},
    {"level": 3, "label": "COMPETING_MODELS_AND_CAUSAL_CHAIN_DOCUMENTED"},
    {"level": 4, "label": "BOUNDED_EVIDENCE_BATCH_REVIEWED"},
    {"level": 5, "label": "PROSPECTIVE_MULTI_METHOD_SIGNAL"},
    {"level": 6, "label": "INDEPENDENT_REPLICATION"},
    {"level": 7, "label": "CROSS_CULTURAL_AND_LONGITUDINAL_ROBUSTNESS"},
    {"level": 8, "label": "CAUSAL_AND_IMPLEMENTATION_EVIDENCE"},
    {"level": 9, "label": "INSTITUTIONAL_AND_ECOLOGICAL_OUTCOMES_REPLICATED"},
    {"level": 10, "label": "DURABLE_BENEFIT_WITH_KNOWN_LIMITS"},
]
EXPECTED_ADVANCEMENT_REQUIREMENTS = {
    "level_4": [
        "Review at least one bounded evidence batch for each major transition in the causal chain.",
        "Separate self-report, observed behavior, community indicators, institutional change and ecological outcomes.",
        "Record null findings, adverse effects, spiritual bypassing, coercion and moral licensing."
    ],
    "level_5": [
        "Use prospective designs with preregistered outcomes and follow-up beyond the immediate experience.",
        "Include behavioural and third-party measures alongside self-report.",
        "Measure mediators, moderators and baseline differences."
    ],
    "level_6": [
        "Achieve independent replication across research groups and intervention contexts.",
        "Replicate benefits and harms with adequate power and transparent exclusions."
    ],
    "level_7": [
        "Test cross-cultural validity with community-led governance and measurement adaptation.",
        "Demonstrate durability across months or years and across socioeconomic settings."
    ],
    "level_8": [
        "Use designs capable of distinguishing intervention effects from selection, expectancy and social reinforcement.",
        "Evaluate implementation fidelity, access, equity and unintended consequences."
    ],
    "level_9": [
        "Replicate community, institutional or ecological outcomes rather than inferring them from individual reports.",
        "Show that benefits do not depend on exploitation, cultural extraction or displaced harms."
    ],
    "level_10": [
        "Demonstrate durable net benefit with clearly bounded generalisability and known failure modes.",
        "Preserve uncertainty and monitoring rather than declaring a final universal solution."
    ]
}
EXPECTED_PRIORITIES = [
    {
        "priority_id": "BQ011-P01",
        "rank": 1,
        "title": "Compassion at scale",
        "question": "Which practices reliably convert empathy, compassion or metta into sustained helping, generosity and nonviolence?",
        "required_outcomes": [
            "observed_behavior",
            "durability",
            "harms"
        ]
    },
    {
        "priority_id": "BQ011-P02",
        "rank": 2,
        "title": "States into traits into service",
        "question": "When do psychedelic, contemplative, mystical or collective experiences produce lasting humility, care and ethical action?",
        "required_outcomes": [
            "self_report",
            "observed_behavior",
            "longitudinal_follow_up"
        ]
    },
    {
        "priority_id": "BQ011-P03",
        "rank": 3,
        "title": "Flexible selfhood and prejudice",
        "question": "Does safely loosening rigid self-models reduce dehumanisation, prejudice and tribal hostility?",
        "required_outcomes": [
            "validated_attitudes",
            "observed_intergroup_behavior",
            "adverse_effects"
        ]
    },
    {
        "priority_id": "BQ011-P04",
        "rank": 4,
        "title": "Ecological connectedness",
        "question": "Does felt connection with nature predict or cause measurable stewardship and lower-impact behaviour?",
        "required_outcomes": [
            "observed_ecological_behavior",
            "material_footprint",
            "durability"
        ]
    },
    {
        "priority_id": "BQ011-P05",
        "rank": 5,
        "title": "Collective synchrony without metaphysical assumptions",
        "question": "How do music, dance, ritual and shared attention affect trust, cooperation and belonging?",
        "required_outcomes": [
            "behavioral_cooperation",
            "inclusion_and_exclusion",
            "physiological_or_temporal_synchrony"
        ]
    },
    {
        "priority_id": "BQ011-P06",
        "rank": 6,
        "title": "Trauma and intergenerational repair",
        "question": "Which combinations of therapy, embodiment, community and meaning-making interrupt cycles of harm safely?",
        "required_outcomes": [
            "clinical_and_functional_change",
            "relationship_outcomes",
            "adverse_events"
        ]
    },
    {
        "priority_id": "BQ011-P07",
        "rank": 7,
        "title": "Death awareness and compassionate priorities",
        "question": "Can death contemplation or end-of-life engagement reduce fear and increase care without requiring survival beliefs?",
        "required_outcomes": [
            "death_anxiety",
            "prosocial_behavior",
            "worldview_coercion_checks"
        ]
    },
    {
        "priority_id": "BQ011-P08",
        "rank": 8,
        "title": "Wisdom across cultures",
        "question": "Which ethical insights recur across traditions, and which meanings must remain culturally and lineage specific?",
        "required_outcomes": [
            "community_authority",
            "attribution",
            "non_extractive_benefit"
        ]
    },
    {
        "priority_id": "BQ011-P09",
        "rank": 9,
        "title": "Community care and mutual witnessing",
        "question": "Which forms of listening and moderated experience-sharing improve belonging without amplifying dogma, delusion or misinformation?",
        "required_outcomes": [
            "belonging",
            "epistemic_humility",
            "safety_incidents"
        ]
    },
    {
        "priority_id": "BQ011-P10",
        "rank": 10,
        "title": "Attention and information ecology",
        "question": "How do platforms, algorithms and AI alter agency, empathy and collective reality formation?",
        "required_outcomes": [
            "attention_and_agency",
            "polarisation",
            "wellbeing",
            "manipulation_risk"
        ]
    },
    {
        "priority_id": "BQ011-P11",
        "rank": 11,
        "title": "Institutions of care",
        "question": "Which organisational, educational and economic structures reward cooperation, sufficiency and stewardship rather than extraction?",
        "required_outcomes": [
            "policy_and_incentive_change",
            "distributional_effects",
            "implementation_durability"
        ]
    },
    {
        "priority_id": "BQ011-P12",
        "rank": 12,
        "title": "Measuring flourishing",
        "question": "Which indicators capture meaning, belonging, compassion, justice and ecological health beyond narrow economic output?",
        "required_outcomes": [
            "cross_cultural_validity",
            "distributional_equity",
            "ecological_indicators"
        ]
    }
]
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
    if spec.get("conclusion_policy") != "UNDETERMINED_AT_INGESTION":
        fail("BQ011 conclusion policy changed")
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

    model_items = spec.get("models")
    if not isinstance(model_items, list) or any(not isinstance(item, dict) for item in model_items):
        fail("competing models must be a list of records")
    if {item.get("model_id") for item in model_items} != set(EXPECTED_MODELS) or len(model_items) != len(EXPECTED_MODELS):
        fail("competing model set changed")
    for item in model_items:
        if item != EXPECTED_MODELS[item["model_id"]]:
            fail(f"competing model payload changed: {item['model_id']}")
    claims = spec.get("claims")
    if not isinstance(claims, list) or len(claims) != 1:
        fail("BQ011 must retain exactly one project-state claim")
    claim = claims[0]
    if claim != EXPECTED_PROJECT_CLAIM or claim.get("reviewed_support") is not True:
        fail("BQ011 project-state claim or no-support boundary changed")

    outcomes = spec.get("outcome_families", [])
    if set(outcomes) != EXPECTED_OUTCOMES or len(outcomes) != len(EXPECTED_OUTCOMES):
        fail("outcome family set changed")

    for key in ("truth_inference_allowed", "edge_state_may_upgrade_evidence"):
        if spec.get("graph", {}).get(key) is not False:
            fail(f"BQ011 graph guard weakened: {key}")
    guards = spec.get("promotion_guards")
    if not isinstance(guards, dict) or set(guards) != set(EXPECTED_PROMOTION_GUARDS):
        fail("BQ011 promotion guards changed or weakened")
    if any(guards.get(key) is not expected for key, expected in EXPECTED_PROMOTION_GUARDS.items()):
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
    if (
        progress != EXPECTED_OVERALL_PROGRESS
        or type(progress.get("level")) is not int
        or type(progress.get("maximum")) is not int
    ):
        fail("overall progress contract changed")
    scale = assessment.get("scale")
    if scale != EXPECTED_SCALE or any(type(item.get("level")) is not int for item in scale or []):
        fail("assessment scale contract changed")

    axes = assessment.get("axis_assessments", [])
    axis_map = {item.get("axis"): item for item in axes}
    if set(axis_map) != set(EXPECTED_AXES) or len(axis_map) != len(axes):
        fail("assessment axis set changed")
    for axis, level in EXPECTED_AXES.items():
        if (
            type(axis_map[axis].get("level")) is not int
            or type(axis_map[axis].get("maximum")) is not int
            or axis_map[axis].get("level") != level
            or axis_map[axis].get("maximum") != 10
        ):
            fail(f"assessment axis changed: {axis}")
        if axis_map[axis].get("boundary") != EXPECTED_AXIS_BOUNDARIES[axis]:
            fail(f"assessment boundary changed: {axis}")
    if assessment.get("advancement_requirements") != EXPECTED_ADVANCEMENT_REQUIREMENTS:
        fail("advancement requirements changed or weakened")
    require_false(assessment.get("governance"), FALSE_GUARDS | {"model_edges_upgrade_evidence"}, "assessment guard")

    if agenda.get("agenda_id") != "BQ011-RESEARCH-AGENDA-V0.1":
        fail("agenda artifact identity changed")
    if agenda.get("status") != "REVIEW_CANDIDATE" or agenda.get("question_id") != "BQ011":
        fail("research agenda identity/status changed")
    if agenda.get("question_status") != "UNRESOLVED":
        fail("research agenda must remain unresolved")
    priority_items = agenda.get("priorities")
    if not isinstance(priority_items, list) or any(not isinstance(item, dict) for item in priority_items):
        fail("research priorities must be a list of records")
    if any(type(item.get("rank")) is not int for item in priority_items):
        fail("research priority ranks must be integers")
    if any(not isinstance(item.get("required_outcomes"), list) for item in priority_items):
        fail("research priority outcomes must be lists")
    if priority_items != EXPECTED_PRIORITIES:
        fail("research priority payloads changed")
    if agenda.get("methodological_requirements") != EXPECTED_METHOD_REQUIREMENTS:
        fail("research methodology boundaries changed")
    community = agenda.get("community_role")
    if community != EXPECTED_COMMUNITY_ROLE:
        fail("community role boundaries changed or weakened")
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
