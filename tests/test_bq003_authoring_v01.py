import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_bq003_authoring_v01.py"
spec = importlib.util.spec_from_file_location("bq003_validator", VALIDATOR)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class BQ003AuthoringTests(unittest.TestCase):
    def setUp(self):
        self.spec = json.loads(module.SPEC.read_text(encoding="utf-8"))
        self.assessment = json.loads(module.ASSESSMENT.read_text(encoding="utf-8"))
        self.bridge = json.loads(module.BRIDGE.read_text(encoding="utf-8"))
        self.aghor = json.loads(module.AGHOR.read_text(encoding="utf-8"))
        self.architecture = json.loads(module.ARCH.read_text(encoding="utf-8"))

    def validate(self, spec=None, assessment=None, bridge=None, aghor=None, architecture=None):
        module.validate(
            spec or self.spec,
            assessment or self.assessment,
            bridge or self.bridge,
            aghor or self.aghor,
            architecture or self.architecture,
        )

    def test_aghori_full_text_hold_removal_rejected(self):
        candidate = copy.deepcopy(self.aghor)
        source = next(x for x in candidate["sources"] if x["source_id"] == "SRC-BQ003-GUPTA-KINA-RAMI-1993")
        source["review_disposition"] = "ACCEPTED"
        with self.assertRaises(ValueError):
            self.validate(aghor=candidate)

    def test_aghori_model_support_promotion_rejected(self):
        candidate = copy.deepcopy(self.aghor)
        candidate["bounded_claims"][0]["supports_models"] = ["MODEL-BQ003-LOVE-FIELD"]
        with self.assertRaises(ValueError):
            self.validate(aghor=candidate)

    def test_aghori_canonical_acceptance_rejected(self):
        candidate = copy.deepcopy(self.aghor)
        candidate["governance"]["accepted_evidence_batch"] = True
        with self.assertRaises(ValueError):
            self.validate(aghor=candidate)

    def test_candidate_passes(self):
        self.validate()

    def test_renewed_review_guards_reject_promotion_and_removal(self):
        cases = [
            ("aghor", ("governance", "canonical_promotion_applied"), True),
            ("aghor", ("governance", "public_synthesis_updated"), True),
            ("aghor", ("governance", "website_updated"), True),
            ("aghor", ("governance", "question_status"), "RESOLVED"),
            ("spec", ("graph", "truth_inference_allowed"), True),
            ("spec", ("graph", "edge_state_may_upgrade_evidence"), True),
            ("assessment", ("status",), "ACCEPTED"),
        ]
        for document, path, promoted in cases:
            for remove in (False, True):
                with self.subTest(document=document, path=path, remove=remove):
                    candidate = copy.deepcopy(getattr(self, document))
                    parent = candidate
                    for key in path[:-1]:
                        parent = parent[key]
                    if remove:
                        del parent[path[-1]]
                    else:
                        parent[path[-1]] = promoted
                    with self.assertRaises(ValueError):
                        self.validate(**{document: candidate})

    def test_aghor_interpretations_cannot_be_retyped_as_observations(self):
        for index, claim in enumerate(self.aghor["bounded_claims"]):
            if claim["claim_type"] != "INTERPRETATION":
                continue
            with self.subTest(claim=claim["claim_id"]):
                candidate = copy.deepcopy(self.aghor)
                candidate["bounded_claims"][index]["claim_type"] = "OBSERVATION"
                candidate["bounded_claims"][index]["evidence_label"] = "Established Evidence"
                with self.assertRaises(ValueError):
                    self.validate(aghor=candidate)

    def test_aghor_claim_source_swap_rejected(self):
        candidate = copy.deepcopy(self.aghor)
        first, second = candidate["bounded_claims"][:2]
        first["source_ids"], second["source_ids"] = second["source_ids"], first["source_ids"]
        with self.assertRaises(ValueError):
            self.validate(aghor=candidate)

    def test_aghor_claim_identity_changes_rejected(self):
        for replacement in (None, "UNKNOWN", self.aghor["bounded_claims"][0]["claim_id"]):
            with self.subTest(replacement=replacement):
                candidate = copy.deepcopy(self.aghor)
                if replacement is None:
                    del candidate["bounded_claims"][1]["claim_id"]
                else:
                    candidate["bounded_claims"][1]["claim_id"] = replacement
                with self.assertRaises(ValueError):
                    self.validate(aghor=candidate)

    def test_assessment_promotion_flags_rejected(self):
        for key in (
            "canonical_promotion_applied",
            "public_synthesis_updated",
            "website_updated",
            "model_edges_upgrade_evidence",
        ):
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.assessment)
                candidate["governance"][key] = True
                with self.assertRaises(ValueError):
                    self.validate(assessment=candidate)

    def test_cultural_governance_key_removal_rejected(self):
        candidate = copy.deepcopy(self.spec)
        del candidate["cultural_governance"]["restricted_knowledge_must_remain_restricted"]
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_competing_model_status_promotion_rejected(self):
        candidate = copy.deepcopy(self.spec)
        candidate["models"][0]["status"] = "ESTABLISHED"
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_interpretation_evidence_promotion_rejected(self):
        candidate = copy.deepcopy(self.aghor)
        claim = next(x for x in candidate["bounded_claims"] if x["claim_type"] == "INTERPRETATION")
        claim["evidence_label"] = "Established Evidence"
        with self.assertRaises(ValueError):
            self.validate(aghor=candidate)

    def test_bridge_question_pair_change_rejected(self):
        for questions in (["BQ004", "BQ005"], ["BQ001"], ["BQ003", "BQ001"]):
            with self.subTest(questions=questions):
                candidate = copy.deepcopy(self.bridge)
                candidate["questions"] = questions
                with self.assertRaises(ValueError):
                    self.validate(bridge=candidate)

    def test_bridge_competing_model_removal_rejected(self):
        candidate = copy.deepcopy(self.bridge)
        candidate["candidate_models"].pop()
        with self.assertRaises(ValueError):
            self.validate(bridge=candidate)

    def test_governed_execution_begins_at_stage_8(self):
        stage_7 = " ".join(self.assessment["advancement_requirements"]["stage_7"]).lower()
        stage_8 = " ".join(self.assessment["advancement_requirements"]["stage_8"]).lower()
        self.assertNotIn("run governed tests", stage_7)
        self.assertIn("run governed tests", stage_8)

    def test_aghori_field_of_love_overattribution_rejected(self):
        candidate = copy.deepcopy(self.spec)
        lens = candidate["culturally_situated_interpretive_lenses"][0]
        lens["attribution_boundary"] = "All Aghoris teach that the field is full of love."
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_aghori_lens_evidence_promotion_rejected(self):
        candidate = copy.deepcopy(self.spec)
        candidate["culturally_situated_interpretive_lenses"][0]["evidence_label"] = "Established Evidence"
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_field_creation_misstatement_rejected(self):
        candidate = copy.deepcopy(self.spec)
        candidate["hypothesis_boundary"]["excluded_claim"] = "No exclusion."
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_ontology_promotion_rejected(self):
        candidate = copy.deepcopy(self.spec)
        candidate["hypothesis_boundary"]["ontology_status"] = "ESTABLISHED"
        with self.assertRaises(ValueError):
            self.validate(spec=candidate)

    def test_progress_truth_promotion_rejected(self):
        candidate = copy.deepcopy(self.assessment)
        candidate["overall_progress"]["meaning"] = "The field probably exists."
        with self.assertRaises(ValueError):
            self.validate(assessment=candidate)

    def test_axis_maturity_fields_rejected_on_every_axis(self):
        for field, value in (("level", 9), ("label", "FINDINGS_TRIANGULATED")):
            with self.subTest(field=field):
                candidate = copy.deepcopy(self.assessment)
                candidate["axis_assessments"][0][field] = value
                with self.assertRaises(ValueError):
                    self.validate(assessment=candidate)

    def test_unverified_synchrony_replication_promotion_rejected(self):
        candidate = copy.deepcopy(self.assessment)
        axis = next(x for x in candidate["axis_assessments"] if x["axis"] == "interpersonal_harmony")
        axis["evidence_state"] = "INDEPENDENT_REPLICATION_ACHIEVED"
        with self.assertRaises(ValueError):
            self.validate(assessment=candidate)

    def test_cosmic_axis_promotion_rejected(self):
        candidate = copy.deepcopy(self.assessment)
        cosmic = next(x for x in candidate["axis_assessments"] if x["axis"] == "literal_cosmic_ontology")
        cosmic["evidence_state"] = "RELEVANT_EVIDENCE_MAPPED"
        with self.assertRaises(ValueError):
            self.validate(assessment=candidate)

    def test_reincarnation_without_continuity_boundary_rejected(self):
        candidate = copy.deepcopy(self.bridge)
        candidate["named_hypothesis"]["decisive_boundary"] = "Universal awareness is reincarnation."
        with self.assertRaises(ValueError):
            self.validate(bridge=candidate)

    def test_meta_awareness_hypothesis_promotion_rejected(self):
        candidate = copy.deepcopy(self.bridge)
        candidate["named_hypothesis"]["evidence_label"] = "Established Evidence"
        with self.assertRaises(ValueError):
            self.validate(bridge=candidate)

    def test_panpsychism_model_support_rejected(self):
        candidate = copy.deepcopy(self.bridge)
        candidate["governance"]["supports_models"] = ["BRIDGE-MODEL-PANPSYCHIC"]
        with self.assertRaises(ValueError):
            self.validate(bridge=candidate)

    def test_personal_and_meta_awareness_cannot_collapse(self):
        candidate = copy.deepcopy(self.bridge)
        candidate["distinctions"] = [
            x for x in candidate["distinctions"]
            if x["continuity_type"] != "PERSONAL_IDENTITY_CONTINUITY"
        ]
        with self.assertRaises(ValueError):
            self.validate(bridge=candidate)

    def test_canonical_registration_without_evidence_rejected(self):
        candidate = copy.deepcopy(self.architecture)
        candidate["questions"]["BQ003"] = {
            "canonical_path": "references/big-questions/BQ003",
            "spec": "references/big-questions/BQ003/spec-v0.1.json",
            "evidence_batches": [],
        }
        with self.assertRaises(ValueError):
            self.validate(architecture=candidate)

    def test_public_gate_rejected(self):
        candidate = copy.deepcopy(self.architecture)
        candidate["authoring_candidates"]["BQ003"]["public_beta_gate"] = True
        with self.assertRaises(ValueError):
            self.validate(architecture=candidate)

if __name__ == "__main__":
    unittest.main()
