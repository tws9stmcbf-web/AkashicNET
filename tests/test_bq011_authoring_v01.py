import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_bq011_authoring_v01.py"
spec = importlib.util.spec_from_file_location("bq011_validator", VALIDATOR)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BQ011AuthoringTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads(module.SPEC.read_text(encoding="utf-8"))
        self.assessment = json.loads(module.ASSESSMENT.read_text(encoding="utf-8"))
        self.agenda = json.loads(module.AGENDA.read_text(encoding="utf-8"))
        self.architecture = json.loads(module.ARCH.read_text(encoding="utf-8"))

    def validate(self, spec=None, assessment=None, agenda=None, architecture=None):
        module.validate(
            self.spec if spec is None else spec,
            self.assessment if assessment is None else assessment,
            self.agenda if agenda is None else agenda,
            self.architecture if architecture is None else architecture,
        )

    def test_existing_question_ids_cannot_be_reused(self):
        snapshot = json.loads((ROOT / "references/big-questions/gold-nuggets-cross-question-synthesis-v0.1.json").read_text(encoding="utf-8"))
        existing_ids = {item["question_id"] for item in snapshot["question_movements"]}
        self.assertNotIn(self.spec["id"], existing_ids)
        for question_id in existing_ids:
            with self.subTest(question_id=question_id):
                candidate = copy.deepcopy(self.spec)
                candidate["id"] = question_id
                with self.assertRaises(ValueError):
                    self.validate(spec=candidate)

    def test_artifact_identity_change_and_removal_rejected(self):
        for argument, original, key in (
            ("assessment", self.assessment, "assessment_id"),
            ("agenda", self.agenda, "agenda_id"),
        ):
            for value in (original[key].replace("BQ011", "BQ004"), "", None):
                with self.subTest(argument=argument, value=value):
                    candidate = copy.deepcopy(original)
                    candidate[key] = value
                    with self.assertRaises(ValueError):
                        self.validate(**{argument: candidate})
            with self.subTest(argument=argument, removed=True):
                candidate = copy.deepcopy(original)
                del candidate[key]
                with self.assertRaises(ValueError):
                    self.validate(**{argument: candidate})

    def test_candidate_passes(self):
        self.validate()

    def test_causal_boundary_promotion_and_removal_rejected(self):
        for key in self.spec["causal_boundary"]:
            for remove in (False, True):
                with self.subTest(key=key, remove=remove):
                    candidate = copy.deepcopy(self.spec)
                    if remove:
                        del candidate["causal_boundary"][key]
                    else:
                        candidate["causal_boundary"][key] = True
                    with self.assertRaises(ValueError):
                        self.validate(spec=candidate)

    def test_causal_chain_change_rejected(self):
        candidate = copy.deepcopy(self.spec)
        candidate["causal_chain"].pop()
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_model_promotion_rejected(self):
        candidate = copy.deepcopy(self.spec)
        candidate["models"][0]["status"] = "ESTABLISHED"
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_model_support_promotion_rejected(self):
        candidate = copy.deepcopy(self.spec)
        candidate["claims"][0]["supports_models"] = ["MODEL-BQ011-MULTILEVEL"]
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_project_state_claim_removal_rejected(self):
        candidate = copy.deepcopy(self.spec)
        candidate["claims"] = []
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_project_state_payload_change_and_removal_rejected(self):
        replacements = {
            "text": "Transformative experiences cause enduring planetary flourishing.",
            "uncertainty": "The causal conclusion is established without uncertainty.",
        }
        for key, replacement in replacements.items():
            for value in (replacement, "", None):
                with self.subTest(key=key, value=value):
                    candidate = copy.deepcopy(self.spec)
                    candidate["claims"][0][key] = value
                    with self.assertRaises(ValueError):
                        self.validate(spec=candidate)
            with self.subTest(key=key, removed=True):
                candidate = copy.deepcopy(self.spec)
                del candidate["claims"][0][key]
                with self.assertRaises(ValueError):
                    self.validate(spec=candidate)

    def test_promotion_guard_change_and_removal_rejected(self):
        for key, value in module.EXPECTED_PROMOTION_GUARDS.items():
            for remove in (False, True):
                with self.subTest(key=key, remove=remove):
                    candidate = copy.deepcopy(self.spec)
                    if remove:
                        del candidate["promotion_guards"][key]
                    else:
                        candidate["promotion_guards"][key] = not value
                    with self.assertRaises(ValueError):
                        self.validate(spec=candidate)

    def test_outcome_family_drift_rejected(self):
        candidate = copy.deepcopy(self.spec)
        candidate["outcome_families"][0] = "self_report_only"
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_graph_gate_promotion_rejected(self):
        for key in ("truth_inference_allowed", "edge_state_may_upgrade_evidence"):
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.spec)
                candidate["graph"][key] = True
                with self.assertRaises(ValueError):
                    self.validate(spec=candidate)

    def test_cultural_governance_removal_rejected(self):
        candidate = copy.deepcopy(self.spec)
        del candidate["cultural_governance"]["benefit_sharing_and_non_extractive_research_required"]
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_progress_promotion_rejected(self):
        candidate = copy.deepcopy(self.assessment)
        candidate["overall_progress"]["level"] = 8
        with self.assertRaises(ValueError):
            self.validate(assessment=candidate)

    def test_assessment_axis_promotion_rejected(self):
        candidate = copy.deepcopy(self.assessment)
        axis = next(x for x in candidate["axis_assessments"] if x["axis"] == "community_to_institutional_change")
        axis["level"] = 6
        with self.assertRaises(ValueError):
            self.validate(assessment=candidate)

    def test_assessment_guard_promotion_and_removal_rejected(self):
        for key in module.FALSE_GUARDS | {"model_edges_upgrade_evidence"}:
            for remove in (False, True):
                with self.subTest(key=key, remove=remove):
                    candidate = copy.deepcopy(self.assessment)
                    if remove:
                        del candidate["governance"][key]
                    else:
                        candidate["governance"][key] = True
                    with self.assertRaises(ValueError):
                        self.validate(assessment=candidate)

    def test_research_priority_identity_and_order_rejected(self):
        candidate = copy.deepcopy(self.agenda)
        candidate["priorities"][0], candidate["priorities"][1] = candidate["priorities"][1], candidate["priorities"][0]
        with self.assertRaises(ValueError):
            self.validate(agenda=candidate)

    def test_research_priority_without_outcomes_rejected(self):
        candidate = copy.deepcopy(self.agenda)
        candidate["priorities"][0]["required_outcomes"] = []
        with self.assertRaises(ValueError):
            self.validate(agenda=candidate)

    def test_methodology_and_community_consent_removal_rejected(self):
        candidate = copy.deepcopy(self.agenda)
        candidate["methodological_requirements"].pop()
        with self.assertRaises(ValueError):
            self.validate(agenda=candidate)

        candidate = copy.deepcopy(self.agenda)
        del candidate["community_role"]["consent_boundary"]
        with self.assertRaises(ValueError):
            self.validate(agenda=candidate)

    def test_agenda_guard_promotion_and_removal_rejected(self):
        for key in module.FALSE_GUARDS | {"accepted_evidence_batch"}:
            for remove in (False, True):
                with self.subTest(key=key, remove=remove):
                    candidate = copy.deepcopy(self.agenda)
                    if remove:
                        del candidate["governance"][key]
                    else:
                        candidate["governance"][key] = True
                    with self.assertRaises(ValueError):
                        self.validate(agenda=candidate)

    def test_canonical_registration_rejected(self):
        candidate = copy.deepcopy(self.architecture)
        candidate["questions"]["BQ011"] = {
            "canonical_path": "references/big-questions/BQ011",
            "spec": "references/big-questions/BQ011/spec-v0.1.json",
            "evidence_batches": [],
        }
        with self.assertRaises(ValueError):
            self.validate(architecture=candidate)

    def test_authoring_registration_drift_rejected(self):
        candidate = copy.deepcopy(self.architecture)
        candidate["authoring_candidates"]["BQ011"]["public_beta_gate"] = True
        with self.assertRaises(ValueError):
            self.validate(architecture=candidate)

        candidate = copy.deepcopy(self.architecture)
        candidate["authoring_candidates"]["BQ011"]["candidate_path"] = "references/public/BQ011"
        with self.assertRaises(ValueError):
            self.validate(architecture=candidate)


if __name__ == "__main__":
    unittest.main()
