import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_bq001_batch1_v01.py"
BATCH_PATH = ROOT / "references" / "big-questions" / "BQ001" / "evidence-batch1-v0.1.json"

spec = importlib.util.spec_from_file_location("validate_bq001_batch1_v01", VALIDATOR_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def payload():
    return json.loads(BATCH_PATH.read_text(encoding="utf-8"))


class BQ001Batch1Tests(unittest.TestCase):
    def test_seed_batch_passes(self):
        module.validate(payload())

    def test_forced_resolution_fails(self):
        p = payload()
        p["question_status"] = "PROVEN_CONTINUITY"
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_interpretation_cannot_be_established_evidence(self):
        p = payload()
        p["claims"][-1]["evidence_label"] = "Established Evidence"
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_unknown_source_fails(self):
        p = payload()
        p["claims"][0]["source_ids"] = ["SRC-DOES-NOT-EXIST"]
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_missing_uncertainty_fails(self):
        p = payload()
        p["claims"][0]["uncertainty"] = ""
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_survival_overclaim_fails(self):
        p = payload()
        c = copy.deepcopy(p["claims"][1])
        c["claim_id"] = "CLAIM-BQ001-NEGATIVE-OVERCLAIM"
        c["text"] = "This proves consciousness after death."
        p["claims"].append(c)
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_non_survival_overclaim_fails(self):
        p = payload()
        c = copy.deepcopy(p["claims"][3])
        c["claim_id"] = "CLAIM-BQ001-NEGATIVE-NONSURVIVAL"
        c["text"] = "This proves non-survival."
        p["claims"].append(c)
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_guard_cannot_be_enabled(self):
        p = payload()
        p["promotion_guards"]["model_support_edges_upgrade_evidence"] = True
        with self.assertRaises(ValueError):
            module.validate(p)


if __name__ == "__main__":
    unittest.main()
