"""Mutation tests for the v0.16 composite release candidate."""

import copy
import json
import os
import subprocess
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from scripts.validate_v016_release_candidate import (
    validate_manifest,
    validate_repository_binding,
)

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

    def test_candidate_iteration_must_be_exact(self):
        errors = self.errors_after(
            lambda data: data.__setitem__("candidate_iteration", 1)
        )
        self.assertIn("candidate iteration", errors)

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

    def test_role_cannot_be_reassigned_to_another_governed_path(self):
        def mutate(data):
            first = data["governed_artifacts"][0]
            second = data["governed_artifacts"][1]
            first["role"], second["role"] = second["role"], first["role"]

        errors = self.errors_after(mutate)
        self.assertIn("governed artifact mapping", errors)

    def test_extra_source_status_fixture_fails_closed(self):
        governed = {
            artifact["path"]
            for artifact in DATA["governed_artifacts"]
            if artifact["path"].startswith("references/source-status-fixture-v0.16")
        }
        discovered = governed | {"references/source-status-fixture-v0.16-extra.json"}
        with mock.patch(
            "scripts.validate_v016_release_candidate.discovered_source_status_fixture_paths",
            return_value=discovered,
        ):
            errors = validate_manifest(copy.deepcopy(DATA))
        self.assertIn("ungoverned source-status fixture", errors)

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


class RepositoryBindingTests(unittest.TestCase):
    """Exercise real Git ancestry, including main advancing after a green head."""

    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Validator test")
        self.git("config", "user.email", "validator@example.invalid")
        self.git("commit", "--allow-empty", "-qm", "base")
        self.base = self.git("rev-parse", "HEAD")
        self.git("update-ref", "refs/remotes/origin/main", self.base)
        self.git("commit", "--allow-empty", "-qm", "candidate")
        self.head = self.git("rev-parse", "HEAD")

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.root, check=True,
            text=True, capture_output=True,
        ).stdout.strip()

    def errors(self, *, base=None, head=None):
        with mock.patch("scripts.validate_v016_release_candidate.ROOT", self.root), \
             mock.patch("scripts.validate_v016_release_candidate.EXPECTED_BASE_COMMIT", base or self.base), \
             mock.patch.dict(os.environ, {"CANDIDATE_HEAD_SHA": head or self.head}):
            return validate_repository_binding()

    def advance_main(self):
        tree = self.git("rev-parse", f"{self.base}^{{tree}}")
        advanced = self.git("commit-tree", tree, "-p", self.base, "-m", "new main")
        self.git("update-ref", "refs/remotes/origin/main", advanced)
        return advanced

    def test_current_main_ancestor_passes(self):
        self.assertEqual(self.errors(), [])

    def test_main_advancement_fails_even_when_old_merge_base_is_unchanged(self):
        self.advance_main()
        self.assertEqual(self.git("merge-base", "HEAD", "origin/main"), self.base)
        self.assertIn("candidate must contain current origin/main", self.errors())
        self.assertIn("actual candidate base commit", self.errors())

    def test_repinning_without_integrating_main_fails(self):
        advanced = self.advance_main()
        self.assertIn("candidate must contain current origin/main", self.errors(base=advanced))

    def test_integrated_and_rebound_main_passes(self):
        advanced = self.advance_main()
        self.git("merge", "--no-ff", "-m", "integrate main", "origin/main")
        head = self.git("rev-parse", "HEAD")
        self.assertEqual(self.errors(base=advanced, head=head), [])

    def test_wrong_exact_head_fails(self):
        self.assertIn("exact candidate head checkout", self.errors(head=self.base))

    def test_missing_main_fails_closed(self):
        self.git("update-ref", "-d", "refs/remotes/origin/main")
        self.assertIn("candidate repository binding", self.errors())


if __name__ == "__main__":
    unittest.main()
