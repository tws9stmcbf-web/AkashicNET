import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_bq002_level5_evidence_atlas.py"
spec = importlib.util.spec_from_file_location("bq002_level5_validator", VALIDATOR)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BQ002Level5EvidenceAtlasTests(unittest.TestCase):
    def setUp(self):
        self.atlas = json.loads(module.ATLAS.read_text(encoding="utf-8"))
        self.spec = json.loads(module.SPEC.read_text(encoding="utf-8"))

    def validate(self, atlas=None):
        module.validate(atlas or self.atlas, self.spec)

    def test_candidate_passes(self):
        self.validate()

    def test_level_cannot_be_applied_before_review(self):
        candidate = copy.deepcopy(self.atlas)
        candidate["maturity"]["candidate_level_applied"] = True
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_source_count_cannot_advance_level(self):
        candidate = copy.deepcopy(self.atlas)
        candidate["scope"]["source_count_advances_level"] = True
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_established_label_cannot_be_applied_to_hypothesis(self):
        candidate = copy.deepcopy(self.atlas)
        claim = next(x for x in candidate["claims"] if x["claim_id"] == "CLAIM-BQ002-ATLAS-PREDICTIVE-01")
        claim["evidence_label"] = "Established Evidence"
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_counter_source_removal_rejected(self):
        candidate = copy.deepcopy(self.atlas)
        for claim in candidate["claims"]:
            claim["counter_source_ids"] = [x for x in claim["counter_source_ids"] if x != "SRC-BQ002-BRUINEBERG-2018"]
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_model_support_rejected(self):
        candidate = copy.deepcopy(self.atlas)
        candidate["claims"][0]["supports_models"] = ["MODEL-BQ002-COGNITIVE-GENERATION"]
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_domain_omission_rejected(self):
        candidate = copy.deepcopy(self.atlas)
        candidate["coverage"].pop()
        with self.assertRaises(ValueError):
            self.validate(candidate)

    def test_promotion_and_boundary_mutations_rejected(self):
        paths = [
            ("question_status", "RESOLVED"),
            ("public_beta_gate", True),
            ("accepted_canonical_edges", 1),
            ("supports_models", ["MODEL-BQ002-COGNITIVE-GENERATION"]),
            ("canonical_promotion_applied", True),
            ("evidence_promotion_applied", True),
            ("public_synthesis_updated", True),
            ("website_updated", True),
            ("truth_inference_allowed", True),
            ("transpersonal_claim_promoted", True),
            ("rights_promotion_allowed", True),
        ]
        for key, value in paths:
            with self.subTest(key=key):
                candidate = copy.deepcopy(self.atlas)
                candidate["governance"][key] = value
                with self.assertRaises(ValueError):
                    self.validate(candidate)


if __name__ == "__main__":
    unittest.main()
