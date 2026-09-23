import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts/validate_psi_subreddit_census_v01.py"
ARTIFACT = Path("references/psi/subreddit-psi-metadata-census-v0.1.json")


class PsiSubredditCensusReviewStateTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / ARTIFACT).read_text(encoding="utf-8"))

    def validate(self):
        # Run the real CLI against an isolated copy; never modify the census.
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / ARTIFACT
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(self.data), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(VALIDATOR)], cwd=directory,
                capture_output=True, text=True, check=False,
            )

    def test_review_required_passes(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_other_review_states_fail(self):
        for state in ("APPROVED", "PROMOTED", "", "review_required", None, False):
            with self.subTest(state=state):
                self.data["governance"]["review_state"] = state
                result = self.validate()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("AssertionError", result.stderr)

    def test_missing_review_state_fails(self):
        del self.data["governance"]["review_state"]
        result = self.validate()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("KeyError: 'review_state'", result.stderr)


if __name__ == "__main__":
    unittest.main()
