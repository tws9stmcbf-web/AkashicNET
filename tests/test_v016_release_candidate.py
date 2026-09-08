"""Mutation tests for the v0.16 composite release candidate."""

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_v016_release_candidate import validate_manifest

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads(
    (ROOT / "manifests/v0.16-release-candidate.json").read_text(encoding="utf-8")
)


class ReleaseCandidateTests(unittest.TestCase):
    def errors_after(self, mutation):
        data = copy.deepcopy(DATA)
        mutation(data)
        return validate_manifest(data)

    def test_candidate_manifest_passes(self):
        self.assertEqual(validate_manifest(copy.deepcopy(DATA)), [])

    def test_candidate_base_must_be_exact(self):
        errors = self.errors_after(
            lambda data: data.__setitem__("candidate_base_commit", "0" * 40)
        )
        self.assertIn("candidate base commit", errors)

    def test_sealed_baseline_drift_fails(self):
        errors = self.errors_after(
            lambda data: data["baseline_locks"].__setitem__("v0.15_seal", "0" * 40)
        )
        self.assertIn("sealed baseline lock drift", errors)

    def test_missing_gate_fails(self):
        errors = self.errors_after(lambda data: data["required_gates"].pop())
        self.assertIn("ten-gate composition", errors)

    def test_enabled_promotion_fails(self):
        errors = self.errors_after(
            lambda data: data["promotion_boundaries"].__setitem__("truth", True)
        )
        self.assertIn("promotion boundary", errors)

    def test_premature_ready_decision_fails(self):
        errors = self.errors_after(
            lambda data: data.__setitem__("release_decision", "READY")
        )
        self.assertIn("premature release decision", errors)

    def test_unpinned_artifact_fails(self):
        errors = self.errors_after(
            lambda data: data["governed_artifacts"][0].__setitem__(
                "git_blob_sha", "not-a-sha"
            )
        )
        self.assertIn("artifact pin", errors)

    def test_artifact_drift_fails(self):
        errors = self.errors_after(
            lambda data: data["governed_artifacts"][0].__setitem__(
                "git_blob_sha", "0" * 40
            )
        )
        self.assertIn("governed artifact drift", errors)

    def test_duplicate_artifact_path_fails(self):
        def mutate(data):
            data["governed_artifacts"][1]["path"] = data["governed_artifacts"][0]["path"]

        errors = self.errors_after(mutate)
        self.assertIn("duplicate artifact path", errors)

    def test_observed_retraction_claim_cannot_be_fabricated(self):
        errors = self.errors_after(
            lambda data: data["candidate_summary"].__setitem__(
                "observed_retraction_claim_count", 1
            )
        )
        self.assertIn("candidate summary", errors)

    def test_accepted_edge_count_must_remain_zero(self):
        errors = self.errors_after(
            lambda data: data["candidate_summary"].__setitem__(
                "accepted_edge_count", 1
            )
        )
        self.assertIn("candidate summary", errors)


if __name__ == "__main__":
    unittest.main()
