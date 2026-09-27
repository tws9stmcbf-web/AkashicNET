"""Mutation regressions for unsafe changes to the current Stage-0 draft."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_coa001_stage0_v02.py"
SPEC = importlib.util.spec_from_file_location("coa001_guard", SCRIPT)
guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)
BASELINE = json.loads(guard.CONTRACT.read_text(encoding="utf-8"))


class StageZeroRegressionTests(unittest.TestCase):
    def setUp(self):
        self.document = copy.deepcopy(BASELINE)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.study = Path(self.tmp.name)
        self.manual = self.study / "BLINDED-INTERVIEW-MANUAL-v0.2.md"
        self.manual.write_text((guard.STUDY / self.manual.name).read_text(), encoding="utf-8")

    def reject(self, fragment):
        with self.assertRaisesRegex(guard.ContractError, fragment):
            guard.validate(self.document, self.study)

    def test_current_contract_and_manual(self):
        guard.validate(self.document, self.study)

    def test_participant_event_stopping_regression_is_rejected(self):
        rule = self.document["statistical_analysis_plan"]["accrual_stopping_rule"]
        for key, value in [
            ("information_unit", "TARGET_EXPOSED_participant_event"),
            ("repeated_events_increment_count", True),
            ("provisional_minimum_unique_participants", 131),
            ("final_unique_participant_target", 132),
            ("freeze_before_recruitment", "not_required"),
            ("ethical_cap_stop_below_target", "INFORMATION_TARGET_MET"),
        ]:
            with self.subTest(key=key):
                original = rule[key]
                rule[key] = value
                self.reject(key)
                rule[key] = original

    def test_primary_target_and_simulation_units_cannot_drift(self):
        self.document["stage_2_primary_hypothesis"]["information_target_unit"] = "participant_event"
        self.reject("information_target_unit")
        self.document = copy.deepcopy(BASELINE)
        self.document["operating_characteristics"]["calculation_unit"] = "repeated_event"
        self.reject("calculation_unit")

    def test_zero_interpreter_use_exception_is_conditional(self):
        gate = next(g for g in self.document["feasibility_gates"]
                    if g["id"] == "INTERPRETER_CONFIDENTIALITY_COMPLIANCE")
        for key, value in [
            ("zero_denominator", "NOT_EVALUABLE"),
            ("zero_denominator", "PASS"),
            ("zero_denominator_requires", []),
            ("empty_missing_or_unknown_use", "PASS"),
            ("unknown_compliance_with_interpreter_use", "PASS"),
            ("threshold", ">=95%"),
        ]:
            with self.subTest(key=key, value=value):
                original = gate[key]
                gate[key] = value
                self.reject(key)
                gate[key] = original
        # Each prerequisite is necessary; zero use cannot hide missingness or holds.
        requirements = gate["zero_denominator_requires"][:]
        for requirement in requirements:
            with self.subTest(requirement=requirement):
                gate["zero_denominator_requires"] = [r for r in requirements if r != requirement]
                self.reject("zero_denominator_requires")
        gate["zero_denominator_requires"] = requirements
        guard.validate(self.document, self.study)

    def test_zero_interpreter_exception_does_not_relax_other_gates(self):
        self.document["feasibility_gate_common_rules"]["zero_denominator"] = "PASS"
        self.reject("zero_denominator")

    def test_missing_or_duplicate_interpreter_gate_is_rejected(self):
        gates = self.document["feasibility_gates"]
        gate = next(g for g in gates if g["id"] == "INTERPRETER_CONFIDENTIALITY_COMPLIANCE")
        gates.remove(gate)
        self.reject("require exactly one gate")
        gates.extend([gate, copy.deepcopy(gate)])
        self.reject("require exactly one gate")

    def test_recursive_hash_or_signature_inputs_are_rejected(self):
        integrity = self.document["target_record_integrity"]
        for key, value in [
            ("unsigned_payload_excludes", []),
            ("unsigned_payload_excludes", ["digital_signature"]),
            ("unsigned_payload_excludes", ["current_record_digest"]),
            ("unsigned_payload_includes", []),
            ("digest_input", "canonicalize_stored_record_envelope"),
            ("signature_input", "stored_record_envelope"),
            ("closing_digest", "current_record_digest"),
            ("closing_count", "including_current_record"),
            ("verification", "trust_attached_digest"),
        ]:
            with self.subTest(key=key, value=value):
                original = integrity[key]
                integrity[key] = value
                self.reject(key)
                integrity[key] = original

    def test_recruitment_permission_is_blocked(self):
        self.document["interview_manual"]["recruitment_authorized"] = True
        self.reject("recruitment_authorized")

    def test_gate_type_coercion_is_blocked(self):
        for value in [0, "false", None, [], {}]:
            with self.subTest(value=value):
                self.document["interview_manual"]["recruitment_authorized"] = value
                self.reject("recruitment_authorized")

    def test_missing_gate_is_not_closed_by_default(self):
        del self.document["ethics_and_data_protection"]["live_participant_data_processing_authorized"]
        self.reject("missing required field")

    def test_malformed_gate_parent_is_blocked(self):
        self.document["ethics_and_data_protection"] = []
        self.reject("malformed parent")

    def test_operational_permission_is_blocked(self):
        self.document["scoring_and_decoy_manual"]["operational_use_authorized"] = True
        self.reject("operational_use_authorized")

    def test_promotion_is_blocked(self):
        for key in ["truth_inference", "scientific_evidence_promotion", "rights_public_synthesis", "website_promotion"]:
            with self.subTest(key=key):
                self.document = copy.deepcopy(BASELINE)
                self.document["parent_question"][key] = True
                self.reject(key)

    def test_edges_and_models_cannot_be_accepted(self):
        self.document["parent_question"]["accepted_canonical_edges"] = 1
        self.reject("accepted_canonical_edges")
        self.document = copy.deepcopy(BASELINE)
        self.document["parent_question"]["supports_models"] = ["example-model"]
        self.reject("supports_models")

    def test_boolean_is_not_an_edge_count(self):
        self.document["parent_question"]["accepted_canonical_edges"] = False
        self.reject("accepted_canonical_edges")

    def test_maturity_inflation_and_resolution_are_blocked(self):
        self.document["parent_question"]["depth_level"] = "8/10"
        self.reject("depth_level")
        self.document = copy.deepcopy(BASELINE)
        self.document["parent_question"]["status"] = "RESOLVED"
        self.reject("status")

    def test_stage_zero_cannot_be_replaced(self):
        self.document["state"] = "STAGE_1_ACTIVE"
        self.reject("state")

    def test_stage_zero_identity_and_permission_cannot_be_hidden(self):
        self.document["stages"][0]["id"] = False
        self.reject("stage identity")
        self.document = copy.deepcopy(BASELINE)
        self.document["stages"].append(copy.deepcopy(self.document["stages"][0]))
        self.reject("three distinct")
        self.document = copy.deepcopy(BASELINE)
        self.document["stages"][0]["participant_recruitment"] = True
        self.reject("participant_recruitment")

    def test_restoring_recognition_before_lock_is_blocked(self):
        self.document["interview_manual"]["order"].insert(-1, "forced_choice_recognition")
        self.reject("order")

    def test_audit_after_lock_is_blocked(self):
        order = self.document["interview_manual"]["order"]
        order.remove("contamination_and_exposure_audit")
        order.append("contamination_and_exposure_audit")
        self.reject("order")

    def test_recognition_permission_and_primary_inclusion_are_blocked(self):
        for key in ["execution_authorized", "primary_endpoint_inclusion"]:
            with self.subTest(key=key):
                self.document = copy.deepcopy(BASELINE)
                self.document["interview_manual"]["recognition"][key] = True
                self.reject(key)

    def test_later_material_cannot_rewrite_primary(self):
        self.document["interview_manual"]["secondary_supplement"]["may_modify_primary"] = True
        self.reject("may_modify_primary")

    def test_primary_source_cannot_be_frozen_silently(self):
        self.document["interview_manual"]["primary_source_compatibility"]["source_eligibility_frozen"] = True
        self.reject("source_eligibility_frozen")

    def test_failed_locks_remain_in_denominator(self):
        self.document["interview_manual"]["flow_accounting"]["lock_success_required_for_completed_denominator"] = True
        self.reject("lock_success_required")

    def test_restored_lock_filtered_population_is_rejected(self):
        self.document["analysis_population_definitions"]["ALL_INTERVIEWED"] = "completed and successfully locked interviews only"
        self.reject("ALL_INTERVIEWED")

    def test_reference_cannot_claim_approval(self):
        self.document["module_references"]["blinded_interview_manual"]["state"] = "APPROVED"
        self.reject("state")

    def test_clean_later_interview_cannot_replace_failed_primary(self):
        self.document["interview_manual"]["flow_accounting"]["later_interview_may_replace_failed_primary"] = True
        self.reject("later_interview")

    def test_unknown_and_empty_denominators_cannot_pass(self):
        for key in ["unknown_blinding_is_clean", "zero_denominator_may_pass"]:
            with self.subTest(key=key):
                self.document = copy.deepcopy(BASELINE)
                self.document["interview_manual"]["flow_accounting"][key] = True
                self.reject(key)

    def test_required_claim_lock_boundary_cannot_be_removed(self):
        self.document["scoring_and_decoy_manual"]["required_boundaries"].remove("claim_set_locked_without_candidate_access")
        self.reject("required_boundaries")

    def test_review_requirement_cannot_be_removed(self):
        self.document["statistical_analysis_plan"]["freeze_requires"].remove("independent_statistical_review")
        self.reject("freeze_requires")

    def test_duplicate_boundary_is_rejected(self):
        values = self.document["data_flow_and_leakage"]["invariants"]
        values.append(values[0])
        self.reject("duplicate")

    def test_registration_or_automatic_bq_update_cannot_be_asserted(self):
        self.document["statistical_analysis_plan"]["preregistered"] = True
        self.reject("preregistered")
        self.document = copy.deepcopy(BASELINE)
        self.document["falsification_stopping_and_classification"]["automatic_BQ001_update"] = True
        self.reject("automatic_BQ001_update")

    def test_stale_module_reference_is_rejected(self):
        self.document["module_references"]["blinded_interview_manual"]["version"] = "0.1"
        self.reject("version")

    def test_path_escape_and_missing_manual_are_rejected(self):
        self.document["interview_manual"]["path"] = "../outside.md"
        self.reject("path")
        self.document = copy.deepcopy(BASELINE)
        self.manual.unlink()
        self.reject("manual missing")

    def test_symlinked_manual_is_rejected(self):
        self.manual.unlink()
        self.manual.symlink_to(guard.STUDY / self.manual.name)
        self.reject("symlinked")

    def test_manual_version_mismatch_is_rejected(self):
        self.manual.write_text(self.manual.read_text().replace("**Version:** 0.2 working draft", "**Version:** 0.1"))
        self.reject("header mismatch")

    def test_invalid_duplicate_and_nonfinite_json_fail_cli(self):
        path = self.study / "contract.json"
        for text in ['{', '{"gate": false, "gate": true}', '{"value": NaN}', '[]']:
            with self.subTest(text=text):
                path.write_text(text)
                result = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertIn("CONTRACT FAIL", result.stdout)
                self.assertNotIn("Traceback", result.stderr)

    def test_guards_remain_active_with_python_optimization(self):
        self.document["interview_manual"]["recognition"]["execution_authorized"] = True
        path = self.study / "contract.json"
        path.write_text(json.dumps(self.document))
        result = subprocess.run([sys.executable, "-O", str(SCRIPT), str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("execution_authorized", result.stdout)


if __name__ == "__main__":
    unittest.main()

