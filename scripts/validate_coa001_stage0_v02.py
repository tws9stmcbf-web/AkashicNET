#!/usr/bin/env python3
"""Static COA-001/INT-001 v0.2 draft guards; never operational authorisation.

This is a deliberately versioned subset validator, not a clinical-data schema,
access-control implementation, scientific appraisal or proof of prose coherence.
Future governed progression requires explicit review of these Stage-0 guards.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STUDY = ROOT / "references/big-questions/BQ001/studies/COA-001"
CONTRACT = STUDY / "protocol-synopsis-v0.1.json"
MANUAL = "BLINDED-INTERVIEW-MANUAL-v0.2.md"
ORDER = [
    "orientation_and_permission", "uninterrupted_free_narrative",
    "N0_source_boundary", "participant_defined_temporal_map",
    "participant_led_clarification", "open_environmental_recall",
    "contamination_and_exposure_audit", "primary_closing",
    "L1_verified_primary_lock",
]
CLOSED_PATHS = [
    "parent_question/truth_inference",
    "parent_question/scientific_evidence_promotion",
    "parent_question/rights_public_synthesis", "parent_question/website_promotion",
    "interview_manual/recruitment_authorized",
    "interview_manual/operational_use_authorized",
    "interview_manual/live_participant_data_processing_authorized",
    "interview_manual/secondary_supplement/may_modify_primary",
    "interview_manual/recognition/execution_authorized",
    "interview_manual/recognition/primary_endpoint_inclusion",
    "interview_manual/primary_source_compatibility/source_eligibility_frozen",
    "scoring_and_decoy_manual/recruitment_authorized",
    "scoring_and_decoy_manual/operational_use_authorized",
    "statistical_analysis_plan/preregistered",
    "statistical_analysis_plan/recruitment_authorized",
    "statistical_analysis_plan/operational_use_authorized",
    "ethics_and_data_protection/ethics_approval",
    "ethics_and_data_protection/legal_authorization",
    "ethics_and_data_protection/recruitment_authorized",
    "ethics_and_data_protection/live_participant_data_processing_authorized",
    "data_flow_and_leakage/recruitment_authorized",
    "data_flow_and_leakage/live_participant_data_processing_authorized",
    "falsification_stopping_and_classification/recruitment_authorized",
    "falsification_stopping_and_classification/operational_use_authorized",
    "falsification_stopping_and_classification/automatic_BQ001_update",
    "interview_manual/flow_accounting/lock_success_required_for_completed_denominator",
    "interview_manual/flow_accounting/later_interview_may_replace_failed_primary",
    "interview_manual/flow_accounting/unknown_blinding_is_clean",
    "interview_manual/flow_accounting/zero_denominator_may_pass",
]


class ContractError(ValueError):
    """A required draft invariant is missing, malformed or contradicted."""


def fail(message: str) -> None:
    raise ContractError(message)


def lookup(document: Any, pointer: str) -> Any:
    value = document
    for key in pointer.split("/"):
        if not isinstance(value, dict) or key not in value:
            fail(f"/{pointer}: missing required field or malformed parent")
        value = value[key]
    return value


def require(document: Any, pointer: str, expected: Any) -> None:
    value = lookup(document, pointer)
    # bool is an int subclass: False/0 and True/1 must not be interchangeable.
    if type(value) is not type(expected) or value != expected:
        fail(f"/{pointer}: expected {expected!r}, got {value!r}")


def require_items(document: Any, pointer: str, items: list[str]) -> None:
    value = lookup(document, pointer)
    if not isinstance(value, list) or any(type(v) is not str for v in value):
        fail(f"/{pointer}: expected string list")
    if len(value) != len(set(value)) or not set(items).issubset(value):
        fail(f"/{pointer}: missing or duplicate required boundary")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_contract(path: Path) -> dict[str, Any]:
    def reject_constant(value: str) -> None:
        fail(f"non-finite JSON number: {value}")
    return json.loads(path.read_text(encoding="utf-8"),
                      object_pairs_hook=unique_object, parse_constant=reject_constant)


def validate(document: Any, study_dir: Path) -> None:
    require(document, "schema_version", "0.1")
    require(document, "version", "0.1")
    require(document, "study_id", "COA-001")
    require(document, "state", "DRAFT_STAGE_0_METHOD_DEVELOPMENT")
    require(document, "parent_question/id", "BQ001")
    require(document, "parent_question/status", "UNRESOLVED")
    require(document, "parent_question/depth_level", "6/10")
    require(document, "parent_question/accepted_canonical_edges", 0)
    require(document, "parent_question/supports_models", [])
    for pointer in CLOSED_PATHS:
        require(document, pointer, False)

    stages = lookup(document, "stages")
    if not isinstance(stages, list) or len(stages) != 3:
        fail("/stages: require the three distinct programme stage definitions")
    stage_ids = [s.get("id") if isinstance(s, dict) else None for s in stages]
    if any(type(v) is not int for v in stage_ids) or set(stage_ids) != {0, 1, 2}:
        fail("/stages: missing, duplicate or malformed stage identity")
    stage0 = next(s for s in stages if s["id"] == 0)
    require(stage0, "label", "protocol_construction")
    require(stage0, "participant_recruitment", False)
    require(stage0, "truth_inference", False)

    require(document, "interview_manual/id", "INT-001")
    require(document, "interview_manual/version", "0.2")
    require(document, "interview_manual/path", MANUAL)
    require(document, "interview_manual/state", "PROVISIONAL_NOT_CLINICALLY_OR_ETHICALLY_APPROVED")
    require(document, "interview_manual/revision_state", "DRAFT_STAGE_0_NOT_VALIDATED")
    require(document, "interview_manual/order", ORDER)
    require(document, "interview_manual/primary_interview",
            "chronologically_first_completed_primary_interview_within_frozen_window_independent_of_lock_success_or_outcome")
    require(document, "analysis_population_definitions/ALL_INTERVIEWED",
            "eligible participant-events with a completed primary protocol interview, regardless of transcript-lock success; lock and data-use states recorded separately")
    require(document, "interview_manual/secondary_supplement/after", "L1")
    require(document, "interview_manual/secondary_supplement/lock", "L2")
    require(document, "interview_manual/recognition/access_route", "NOT_DEFINED_OR_AUTHORIZED")
    require(document, "interview_manual/primary_source_compatibility/status", "HOLD_PENDING_INDEPENDENT_REVIEW")
    require_items(document, "interview_manual/required_boundaries", [
        "L1_before_structured_supplement_target_prompts_or_candidate_exposure",
        "C1_before_primary_scorer_candidate_access",
        "recognition_blocked_pending_coordinated_access_and_analysis_review",
        "append_only_post_lock_amendments", "primary_interview_not_replaced_by_later_interview",
    ])
    require_items(document, "scoring_and_decoy_manual/required_boundaries", [
        "claim_set_locked_without_candidate_access", "L1_only_primary_source",
        "L2_and_recognition_excluded_from_primary_packet",
        "candidate_set_manifest_committed_before_scorer_access",
    ])
    require_items(document, "statistical_analysis_plan/freeze_requires", [
        "independent_statistical_review", "independent_simulation_reproduction",
        "INT_001_v0_2_primary_source_and_failed_lock_compatibility_review",
    ])
    require(document, "data_flow_and_leakage/permitted_flow_count", 17)
    require_items(document, "data_flow_and_leakage/invariants", [
        "no_direct_target_or_truth_route_to_participant_facing_staff",
        "claim_and_score_locks_precede_truth_release",
        "truth_release_requires_machine_prerequisites_and_dual_control",
        "participant_recognition_route_not_defined_or_authorized",
    ])

    # Review blockers: guard the planning unit, the sole zero-use exception,
    # and the non-recursive signing contract. These remain static draft checks.
    require(document, "stage_2_primary_hypothesis/information_target_unit",
            "unique_TARGET_EXPOSED_participant")
    require(document, "stage_2_primary_hypothesis/provisional_information_target_target_exposed", 132)
    require(document, "stage_2_primary_hypothesis/repeated_events_increment_information_count", False)
    stopping = "statistical_analysis_plan/accrual_stopping_rule"
    for key, value in {
        "information_unit": "unique_TARGET_EXPOSED_participant",
        "provisional_minimum_unique_participants": 132,
        "final_unique_participant_target": None,
        "freeze_before_recruitment": "blinded_stage_1_simulation_of_participant_weighted_endpoint_and_independent_review",
        "repeated_events_increment_count": False,
        "ethical_cap_stop_below_target": "UNDERPOWERED_OR_INFEASIBLE_NOT_INFORMATION_TARGET_MET",
    }.items():
        require(document, f"{stopping}/{key}", value)
    require(document, "operating_characteristics/calculation_unit",
            "independent_rank_contribution_not_repeated_participant_event")

    gates = lookup(document, "feasibility_gates")
    if not isinstance(gates, list) or any(not isinstance(g, dict) for g in gates):
        fail("/feasibility_gates: expected gate objects")
    interpreter = [g for g in gates if g.get("id") == "INTERPRETER_CONFIDENTIALITY_COMPLIANCE"]
    if len(interpreter) != 1:
        fail("INTERPRETER_CONFIDENTIALITY_COMPLIANCE: require exactly one gate")
    for key, value in {
        "denominator": "all_interpreted_interviews", "threshold": "100%", "mandatory": True,
        "zero_denominator": "PASS_ONLY_IF_VERIFIED_NO_INTERPRETER_USE",
        "zero_denominator_pass_reason": "NOT_APPLICABLE_NO_INTERPRETER_USE",
        "zero_denominator_requires": [
            "complete_interview_ledger", "at_least_one_completed_interview",
            "explicit_no_interpreter_use_for_every_interview_in_scope",
            "verification_recorded_by_site_and_pooled", "no_incident_hold_waived",
        ],
        "empty_missing_or_unknown_use": "NOT_EVALUABLE",
        "unknown_compliance_with_interpreter_use": "FAIL",
    }.items():
        require(interpreter[0], key, value)
    require(document, "feasibility_gate_common_rules/zero_denominator", "NOT_EVALUABLE")
    require(document, "feasibility_gate_common_rules/zero_denominator_exception",
            "INTERPRETER_CONFIDENTIALITY_COMPLIANCE_only_under_its_verified_no_use_rule")

    for key, value in {
        "unsigned_payload_excludes": ["current_record_digest", "digital_signature"],
        "unsigned_payload_includes": ["prior_record_digest"],
        "digest_input": "canonicalize_unsigned_payload",
        "signature_input": "current_record_digest",
        "verification": "recompute_digest_compare_verify_signature_and_prior_link",
        "closing_digest": "immediately_preceding_record_digest",
        "closing_count": "preceding_records_only", "profile_freeze_required": True,
    }.items():
        require(document, f"target_record_integrity/{key}", value)

    ref = lookup(document, "module_references/blinded_interview_manual")
    for key, value in [("id", "INT-001"), ("version", "0.2"), ("path", MANUAL),
                       ("state", "PROVISIONAL_NOT_CLINICALLY_OR_ETHICALLY_APPROVED")]:
        require(ref, key, value)
    target = study_dir / MANUAL
    if target.is_symlink() or not target.is_file():
        fail("INT-001 v0.2 manual missing or symlinked")
    # Bound file resolution before inspection; no paths supplied by the JSON are followed.
    if not target.resolve().is_relative_to(study_dir.resolve()):
        fail("INT-001 manual escaped its study directory")
    text = target.read_text(encoding="utf-8")
    for marker in ["**Module:** INT-001", "**Version:** 0.2 working draft",
                   "**State:** DRAFT / STAGE-0 METHOD DEVELOPMENT"]:
        if marker not in text:
            fail(f"INT-001 manual header mismatch: {marker}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", nargs="?", type=Path, default=CONTRACT)
    args = parser.parse_args(argv)
    try:
        validate(load_contract(args.contract), args.contract.parent)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"COA-001 STAGE-0 CONTRACT FAIL: {error}")
        return 1
    print("COA-001 STAGE-0 CONTRACT PASS: static draft guards only; no research or promotion authorised")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

