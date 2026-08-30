import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "validate_bq001_batch3_v01.py"
BATCH_PATH = ROOT / "references" / "big-questions" / "BQ001" / "evidence-batch3-v0.1.json"

spec = importlib.util.spec_from_file_location("validate_bq001_batch3_v01", VALIDATOR_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def payload():
    return json.loads(BATCH_PATH.read_text(encoding="utf-8"))


class BQ001Batch3Tests(unittest.TestCase):
    def test_batch_passes(self):
        module.validate(payload())

    def test_forced_resolution_fails(self):
        p = payload()
        p["question_status"] = "PROVEN_REINCARNATION"
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_case_match_proof_guard_fails_open(self):
        p = payload()
        p["promotion_guards"]["case_match_proves_reincarnation"] = True
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_interpretation_cannot_be_established_evidence(self):
        p = payload()
        c = next(c for c in p["claims"] if c["claim_type"] == "INTERPRETATION")
        c["evidence_label"] = "Established Evidence"
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_claim_without_methodological_risks_fails(self):
        p = payload()
        p["claims"][0]["methodological_risks"] = []
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_unknown_source_fails(self):
        p = payload()
        p["claims"][0]["source_ids"] = ["SRC-NOT-REAL"]
        with self.assertRaises(ValueError):
            module.validate(p)

    def test_explicit_proof_language_fails(self):
        p = payload()
        p["claims"][0]["text"] = "This case proves reincarnation."
        with self.assertRaises(ValueError):
            module.validate(p)


if __name__ == "__main__":
    unittest.main()
