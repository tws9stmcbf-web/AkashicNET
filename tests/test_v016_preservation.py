"""Real Git controls for historical preservation without candidate rebinding."""

import contextlib
import io
import os
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import validate_v016_preservation as preservation
from scripts import validate_v016_release_candidate as historical


class PreservationBindingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Preservation test")
        self.git("config", "user.email", "preservation@example.invalid")
        self.git("commit", "--allow-empty", "-qm", "historical base")
        self.anchor = self.git("rev-parse", "HEAD")
        self.git("commit", "--allow-empty", "-qm", "advanced main")
        self.current_main = self.git("rev-parse", "HEAD")
        self.git("update-ref", "refs/remotes/origin/main", self.current_main)
        self.git("commit", "--allow-empty", "-qm", "candidate")
        self.head = self.git("rev-parse", "HEAD")
        for target, value in (
            ("scripts.validate_v016_preservation.ROOT", self.root),
            ("scripts.validate_v016_preservation.HISTORICAL_BASE_COMMIT", self.anchor),
            ("scripts.validate_v016_release_candidate.ROOT", self.root),
            ("scripts.validate_v016_release_candidate.EXPECTED_BASE_COMMIT", self.anchor),
        ):
            patcher = mock.patch(target, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        patcher = mock.patch.dict(os.environ, {"CANDIDATE_HEAD_SHA": self.head})
        patcher.start()
        self.addCleanup(patcher.stop)

    def git(self, *args):
        return subprocess.run(
            ["git", *args], cwd=self.root, check=True,
            text=True, capture_output=True,
        ).stdout.strip()

    def new_commit(self, *parents):
        tree = self.git("rev-parse", "HEAD^{tree}")
        parent_args = [arg for parent in parents for arg in ("-p", parent)]
        return self.git("commit-tree", tree, *parent_args, "-m", "alternate history")

    def test_integrated_descendant_passes_without_rebinding_historical_base(self):
        self.assertEqual(preservation.validate_repository_binding(), [])
        self.assertEqual(
            historical.validate_repository_binding(), ["actual candidate base commit"]
        )

    def test_original_base_position_also_passes(self):
        self.git("update-ref", "refs/remotes/origin/main", self.anchor)
        self.assertEqual(preservation.validate_repository_binding(), [])
        self.assertEqual(historical.validate_repository_binding(), [])

    def test_main_advancing_beyond_candidate_fails(self):
        self.git("update-ref", "refs/remotes/origin/main", self.new_commit(self.head))
        self.assertIn("candidate must contain current origin/main",
                      preservation.validate_repository_binding())

    def test_diverged_main_fails_with_same_historical_merge_base(self):
        self.git("update-ref", "refs/remotes/origin/main", self.new_commit(self.anchor))
        self.assertEqual(self.git("merge-base", "HEAD", "origin/main"), self.anchor)
        self.assertIn("candidate must contain current origin/main",
                      preservation.validate_repository_binding())

    def test_integrating_advanced_main_passes_without_repin(self):
        advanced = self.new_commit(self.current_main)
        self.git("update-ref", "refs/remotes/origin/main", advanced)
        self.git("merge", "--no-ff", "-m", "integrate main", "origin/main")
        os.environ["CANDIDATE_HEAD_SHA"] = self.git("rev-parse", "HEAD")
        self.assertEqual(preservation.validate_repository_binding(), [])

    def test_anchor_outside_main_fails_even_if_head_contains_both(self):
        unrelated = self.new_commit()
        merged = self.new_commit(self.head, unrelated)
        self.git("update-ref", "refs/remotes/origin/main", unrelated)
        self.git("checkout", "--detach", merged)
        os.environ["CANDIDATE_HEAD_SHA"] = merged
        self.assertEqual(preservation.validate_repository_binding(),
                         ["historical base must be an ancestor of current origin/main"])

    def test_head_outside_anchor_and_main_fails(self):
        unrelated = self.new_commit()
        self.git("checkout", "--detach", unrelated)
        os.environ["CANDIDATE_HEAD_SHA"] = unrelated
        errors = preservation.validate_repository_binding()
        self.assertIn("historical base must be an ancestor of candidate head", errors)
        self.assertIn("candidate must contain current origin/main", errors)

    def test_missing_main_fails_closed(self):
        self.git("update-ref", "-d", "refs/remotes/origin/main")
        self.assertIn("candidate repository binding", preservation.validate_repository_binding())

    def test_missing_anchor_fails_closed(self):
        with mock.patch.object(preservation, "HISTORICAL_BASE_COMMIT", "0" * 40):
            self.assertIn("candidate repository binding", preservation.validate_repository_binding())

    def test_rebinding_historical_validator_is_rejected(self):
        with mock.patch.object(historical, "EXPECTED_BASE_COMMIT", self.current_main):
            self.assertIn("historical candidate base identity changed",
                          preservation.validate_repository_binding())

    def test_wrong_exact_head_fails(self):
        os.environ["CANDIDATE_HEAD_SHA"] = self.current_main
        self.assertIn("exact candidate head checkout", preservation.validate_repository_binding())

    def test_missing_or_abbreviated_exact_head_fails(self):
        for value in ("", self.head[:7], "HEAD"):
            with self.subTest(value=value):
                os.environ["CANDIDATE_HEAD_SHA"] = value
                self.assertIn("full exact candidate head SHA required",
                              preservation.validate_repository_binding())


class PreservationEntryPointTests(unittest.TestCase):
    def test_production_anchor_keeps_exact_historical_identity(self):
        self.assertEqual(preservation.HISTORICAL_BASE_COMMIT,
                         "5fb99152524b57948aa10662a1467944fea706c6")
        self.assertEqual(preservation.HISTORICAL_BASE_COMMIT, historical.EXPECTED_BASE_COMMIT)

    def test_manifest_and_dependency_failures_cannot_be_bypassed(self):
        with mock.patch.object(preservation, "validate_repository_binding", return_value=[]), \
             mock.patch.object(preservation, "git_commit", return_value="0" * 40), \
             mock.patch.object(historical, "validate_manifest", return_value=["governed artifact drift"]), \
             mock.patch.object(historical, "run_dependencies") as dependencies, \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(preservation.main(), 1)
            dependencies.assert_not_called()
        with mock.patch.object(preservation, "validate_repository_binding", return_value=[]), \
             mock.patch.object(preservation, "git_commit", return_value="0" * 40), \
             mock.patch.object(historical, "run_dependencies", side_effect=AssertionError("dependency failed")), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(preservation.main(), 1)


if __name__ == "__main__":
    unittest.main()
