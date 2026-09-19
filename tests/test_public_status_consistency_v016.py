"""Mutation checks for current naming; sealed validators are never modified."""

from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "scripts/validate_public_status_consistency_v016.py"
HOME = "website/app/page.tsx"
PROGRESS = "website/app/development-progress/page.tsx"


class CurrentPublicStatusTests(unittest.TestCase):
    def run_case(self, *, home=None, progress=None, extra=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in (SCRIPT, HOME, PROGRESS):
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / name, target)
            for name, transform in ((HOME, home), (PROGRESS, progress)):
                if transform:
                    target = root / name
                    target.write_text(transform(target.read_text()))
            if extra is not None:
                (root / "website/app/ordinary.tsx").write_text(extra)
            return subprocess.run(
                [sys.executable, str(root / SCRIPT)],
                text=True, capture_output=True, check=False,
            )

    def assert_rejected(self, *, reason=None, **changes):
        result = self.run_case(**changes)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("FAIL:", result.stderr)
        if reason:
            self.assertIn(reason, result.stderr)

    def test_current_copy_and_independent_framework_versions_pass(self):
        result = self.run_case(extra=(
            '<p>AkashicNET analysis: METAD v2.1, ACTC v2.0, UMASC v7.2</p>'
            '<p>BQ001 · Public synthesis v0.1.1 · Page iteration 04</p>'
        ))
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_pre_alpha_rejected_on_both_allowed_surfaces(self):
        for surface in ("home", "progress"):
            with self.subTest(surface=surface):
                self.assert_rejected(**{surface: lambda text:
                    text + '<p>AkashicNET <span>engine · Pre-alpha</span></p>'})

    def test_ordinary_product_labels_rejected(self):
        for label in (
            "AkashicNET engine · Pre-alpha", "AkashicNET v0.16.7",
            "AkashicNET · Public Beta", "Public Beta · AkashicNET",
            "AkashicNET <span>v0.16.0-beta.2</span>",
            "AkashicNET is v0.16.7", "AkashicNET release: v0.16.7",
            "AkashicNET currently runs v0.16.7",
            "AkashicNET now uses version v0.16.0-beta.2",
            "AkashicNET currently <strong>runs</strong> v0.16.7",
        ):
            with self.subTest(label=label):
                self.assert_rejected(extra=f"<p>{label}</p>")

    def test_duplicate_current_homepage_status_rejected(self):
        self.assert_rejected(home=lambda text: text + "<p>Public Beta</p>")
        self.assert_rejected(home=lambda text: text + "<p>v0.16.0-beta.2</p>")
        self.assert_rejected(home=lambda text: text + "<p>v0.16.7</p>")

    def test_checkpoint_must_link_to_development_record(self):
        self.assert_rejected(home=lambda text:
            text.replace('href="/development-progress"', 'href="/"'))

    def test_affirmative_release_claims_rejected(self):
        for version in ("v0.16.0-beta.2", "v0.16.7"):
            for claim in (
                f"{version} is a sealed release",
                f"{version} is the current release",
                f"{version} READY / SEALED",
                f"Released {version}",
            ):
                for surface in ("home", "progress"):
                    with self.subTest(claim=claim, surface=surface):
                        self.assert_rejected(**{surface: lambda text, claim=claim:
                            text + f"<p>{claim}</p>"})

    def test_candidate_and_checkpoint_disclaimers_required(self):
        for disclaimer in ("not a sealed release", "not a release"):
            with self.subTest(disclaimer=disclaimer):
                self.assert_rejected(progress=lambda text, phrase=disclaimer:
                    text.replace(phrase, "a completed release"))

    def test_latest_release_claim_rejected_with_disclaimer_intact(self):
        for version in ("v0.16.0-beta.2", "v0.16.7"):
            with self.subTest(version=version):
                self.assert_rejected(
                    reason="unsealed candidate or site checkpoint presented as a release",
                    progress=lambda text, version=version:
                        text + f"<p>{version} is the latest release</p>",
                )
                self.assert_rejected(home=lambda text, version=version:
                    text + f"<p>{version} is the latest release</p>")

    def test_perfect_tense_resolution_rejected_with_unresolved_intact(self):
        for surface in ("home", "progress"):
            with self.subTest(surface=surface):
                self.assert_rejected(
                    reason="public status surface contradicts BQ001 UNRESOLVED",
                    **{surface: lambda text:
                        text + "<p>BQ001 has been RESOLVED</p>"},
                )

    def test_negative_claims_and_framework_versions_remain_allowed(self):
        result = self.run_case(
            progress=lambda text: text + (
                "<p>v0.16.0-beta.2 is not the latest release.</p>"
                "<p>v0.16.7 is not a release.</p>"
                "<p>BQ001 has not been RESOLVED.</p>"
            ),
            extra=("<p>AkashicNET uses METAD v2.1</p>"
                   "<p>AkashicNET uses MultidimensionalCUT v4.0.0</p>"
                   "<p>AkashicNET uses AkashicOMNI v0.3.0</p>"),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_checkpoint_direction_required(self):
        self.assert_rejected(progress=lambda text:
            text.replace("progress toward v0.17.0", "completed development"))

    def test_historical_homepage_context_required(self):
        self.assert_rejected(home=lambda text:
            text.replace("Historical sealed release checkpoint", "Current release"))

    def test_bq001_and_no_promotion_boundaries_required(self):
        self.assert_rejected(progress=lambda text:
            text + "<p>BQ001 is RESOLVED</p>")
        self.assert_rejected(progress=lambda text: text + "truth inference enabled")


if __name__ == "__main__":
    unittest.main()
