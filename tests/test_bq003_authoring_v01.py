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
        self.architecture = json.loads(module.ARCH.read_text(encoding="utf-8"))

    def validate(self, spec=None, assessment=None, bridge=None, architecture=None):
        module.validate(
            spec or self.spec,
            assessment or self.assessment,
            bridge or self.bridge,
            architecture or self.architecture,
        )

    def test_candidate_passes(self):
        self.validate()

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

    def test_unverified_synchrony_replication_promotion_rejected(self):
        candidate = copy.deepcopy(self.assessment)
        axis = next(x for x in candidate["axis_assessments"] if x["axis"] == "interpersonal_harmony")
        axis["level"] = 6
        with self.assertRaises(ValueError):
            self.validate(assessment=candidate)

    def test_cosmic_axis_promotion_rejected(self):
        candidate = copy.deepcopy(self.assessment)
        cosmic = next(x for x in candidate["axis_assessments"] if x["axis"] == "literal_cosmic_ontology")
        cosmic["level"] = 5
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
