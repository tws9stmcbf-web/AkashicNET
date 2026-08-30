import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_bq001_batch4_v01.py"
BATCH_PATH = ROOT / "references" / "big-questions" / "BQ001" / "evidence-batch4-v0.1.json"

spec = importlib.util.spec_from_file_location("validate_bq001_batch4_v01", VALIDATOR_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def payload():
    return json.loads(BATCH_PATH.read_text(encoding="utf-8"))


class BQ001Batch4Tests(unittest.TestCase):
    def test_batch_passes(self):
        module.validate(payload())

    def test_question_cannot_be_resolved(self):
        p = payload()
        p["question_status"] = "RESOLVED"
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_philosophy_reference_cannot_be_established_evidence(self):
        p = payload()
        p["claims"][3]["evidence_label"] = "Established Evidence"
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_tradition_longevity_cannot_upgrade(self):
        p = payload()
        p["promotion_guards"]["tradition_longevity_upgrades_evidence"] = True
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_panpsychism_cannot_entail_personal_survival(self):
        p = payload()
        p["promotion_guards"]["panpsychism_entails_personal_survival"] = True
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_model_edges_cannot_upgrade_evidence(self):
        p = payload()
        p["promotion_guards"]["model_support_edges_upgrade_evidence"] = True
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_missing_uncertainty_fails(self):
        p = payload()
        p["claims"][0]["uncertainty"] = ""
        with self.assertRaises(ValueError):
            module.validate(p)


if __name__ == "__main__":
    unittest.main()
