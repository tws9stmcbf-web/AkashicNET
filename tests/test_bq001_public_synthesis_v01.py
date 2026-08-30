import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_bq001_public_synthesis_v01.py"
SYNTHESIS = ROOT / "references" / "big-questions" / "BQ001" / "public-synthesis-v0.1.json"

spec = importlib.util.spec_from_file_location("validate_bq001_public_synthesis_v01", VALIDATOR)
module = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(module)


def payload():
    return json.loads(SYNTHESIS.read_text(encoding="utf-8"))


class BQ001PublicSynthesisTests(unittest.TestCase):
    def test_valid_synthesis_passes(self):
        module.validate(payload(), ROOT)

    def test_resolved_conclusion_fails(self):
        p = payload()
        p["status"] = "RESOLVED"
        p["conclusion"]["status"] = "RESOLVED"
        with self.assertRaises(ValueError):
            module.validate(p, ROOT)

    def test_unknown_claim_fails(self):
        p = payload()
        p["sections"][0]["claim_ids"].append("CLAIM-BQ001-INVENTED")
        with self.assertRaises(ValueError):
            module.validate(p, ROOT)

    def test_unknown_source_fails(self):
        p = payload()
        p["sections"][0]["source_ids"].append("SRC-BQ001-INVENTED")
        with self.assertRaises(ValueError):
            module.validate(p, ROOT)

    def test_evidence_label_upgrade_fails(self):
        p = payload()
        p["sections"][2]["evidence_label"] = "Established Evidence"
        with self.assertRaises(ValueError):
            module.validate(p, ROOT)

    def test_missing_boundary_fails(self):
        p = payload()
        p["sections"][0]["boundary"] = ""
        with self.assertRaises(ValueError):
            module.validate(p, ROOT)

    def test_model_vote_guard_must_remain_false(self):
        p = payload()
        p["promotion_guards"]["model_vote_counting_allowed"] = True
        with self.assertRaises(ValueError):
            module.validate(p, ROOT)

    def test_single_score_guard_must_remain_false(self):
        p = payload()
        p["promotion_guards"]["single_score_allowed"] = True
        with self.assertRaises(ValueError):
            module.validate(p, ROOT)


if __name__ == "__main__":
    unittest.main()
