import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_bq001_batch2_v01.py"
DATA_PATH = ROOT / "references" / "big-questions" / "BQ001" / "evidence-batch2-v0.1.json"

spec = importlib.util.spec_from_file_location("validate_bq001_batch2_v01", VALIDATOR_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def payload():
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


class BQ001Batch2Tests(unittest.TestCase):
    def test_seed_passes(self):
        module.validate(payload())

    def test_forced_resolution_fails(self):
        p = payload()
        p["question_status"] = "RESOLVED"
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_missing_limitations_fails(self):
        p = payload()
        p["sources"][0]["limitations"] = []
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_review_cannot_be_primary_established_evidence(self):
        p = payload()
        c = copy.deepcopy(p["claims"][1])
        c["claim_id"] = "CLAIM-BQ001-NEG-REVIEW-PROMOTION"
        c["claim_type"] = "OBSERVATION"
        c["evidence_label"] = "Established Evidence"
        p["claims"][1] = c
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_interpretation_cannot_be_established_evidence(self):
        p = payload()
        p["claims"][3]["evidence_label"] = "Established Evidence"
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_metaphysical_identity_guard_cannot_flip(self):
        p = payload()
        p["promotion_guards"]["psychological_self_continuity_equals_metaphysical_identity"] = True
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_neuroscientific_model_completeness_guard_cannot_flip(self):
        p = payload()
        p["promotion_guards"]["neuroscientific_model_proves_complete_explanation"] = True
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_model_edges_cannot_upgrade_evidence(self):
        p = payload()
        p["promotion_guards"]["model_support_edges_upgrade_evidence"] = True
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_forbidden_non_survival_conclusion_fails(self):
        p = payload()
        p["batch_conclusion"]["statement"] = "This batch proves non-survival."
        with self.assertRaises(ValueError):
            module.validate(p)


if __name__ == "__main__":
    unittest.main()
