import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("maturity_validator", ROOT / "scripts/validate_big_question_maturity_v01.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BigQuestionMaturityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ladder = json.loads((ROOT / "references/big-questions/research-maturity-ladder-v0.1.json").read_text())
        cls.registry = json.loads((ROOT / "references/big-questions/maturity-assessments-v0.1.json").read_text())

    def test_canonical_state_passes(self):
        module.validate(self.ladder, self.registry, [("page", "BQ001 · Level 6/10\nBQ002 · Level 4/10")])

    def test_nonconsecutive_completion_fails_closed(self):
        candidate = copy.deepcopy(self.registry)
        candidate["assessments"][0]["completed_stages"] = [1, 2, 3, 4, 6]
        with self.assertRaises(ValueError):
            module.validate(self.ladder, candidate)

    def test_file_overstatement_fails_closed(self):
        with self.assertRaises(ValueError):
            module.validate(self.ladder, self.registry, [("candidate.json", "BQ001 remains Level 8/10")])

    def test_pr_body_overstatement_fails_closed(self):
        with self.assertRaises(ValueError):
            module.validate(self.ladder, self.registry, pr_body="BQ001: UNRESOLVED, Level 8/10")

    def test_promotion_gate_fails_closed(self):
        candidate = copy.deepcopy(self.registry)
        candidate["governance"]["website_promotion_allowed"] = True
        with self.assertRaises(ValueError):
            module.validate(self.ladder, candidate)


if __name__ == "__main__":
    unittest.main()
