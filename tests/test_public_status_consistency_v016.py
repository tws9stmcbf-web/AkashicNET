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

    def test_adverbial_release_assertions_rejected(self):
        for version in ("v0.16.0-beta.2", "v0.16.7"):
            for wording in ("is now the latest release", "is currently the release",
                            "has now been released", "is now a sealed release"):
                with self.subTest(version=version, wording=wording):
                    self.assert_rejected(
                        reason="unsealed candidate or site checkpoint presented as a release",
                        progress=lambda text, v=version, w=wording: text + f"<p>{v} {w}</p>",
                    )

    def test_shipped_assertions_rejected_with_disclaimers_intact(self):
        for version in ("v0.16.0-beta.2", "v0.16.7"):
            for wording in ("has shipped", "has now shipped", "shipped", "is shipped"):
                with self.subTest(version=version, wording=wording):
                    self.assert_rejected(
                        reason="unsealed candidate or site checkpoint presented as a release",
                        progress=lambda text, v=version, w=wording: text + f"<p>{v} {w}</p>",
                    )

    def test_negative_release_constructions_pass(self):
        for version in ("v0.16.0-beta.2", "v0.16.7"):
            for wording in (
                "has yet to be released", "has yet to ship", "has not shipped",
                "cannot be released", "can not be released", "can't be released",
                "is neither released nor sealed", "remains without a release",
                "is far from released", "has yet to be shipped",
            ):
                with self.subTest(version=version, wording=wording):
                    result = self.run_case(progress=lambda text, v=version, w=wording:
                                           text + f"<p>{v} {w}</p>")
                    self.assertEqual(result.returncode, 0, result.stderr)

    def test_negative_resolution_constructions_pass(self):
        for wording in (
            "remains far from RESOLVED", "has yet to be RESOLVED",
            "cannot be RESOLVED", "can not be RESOLVED", "can't be RESOLVED",
            "is neither settled nor RESOLVED", "remains without a RESOLVED status",
        ):
            for surface in ("home", "progress"):
                with self.subTest(wording=wording, surface=surface):
                    result = self.run_case(**{surface: lambda text, w=wording:
                                            text + f"<p>BQ001 {w}</p>"})
                    self.assertEqual(result.returncode, 0, result.stderr)

    def test_negative_copy_does_not_hide_separate_affirmative_claims(self):
        for separator in (". ", "; ", "</p><p>", "\n"):
            with self.subTest(separator=separator):
                self.assert_rejected(
                    reason="unsealed candidate or site checkpoint presented as a release",
                    progress=lambda text, s=separator: text + (
                        f"<p>v0.16.7 has yet to be released{s}v0.16.7 has shipped</p>"),
                )
                self.assert_rejected(
                    reason="public status surface contradicts BQ001 UNRESOLVED",
                    progress=lambda text, s=separator: text + (
                        f"<p>BQ001 remains far from RESOLVED{s}BQ001 is RESOLVED</p>"),
                )

    def test_possessive_product_labels_rejected(self):
        for possessive in ("'s", "’s", "&apos;s", "&#39;s", "&#x2019;s"):
            with self.subTest(possessive=possessive):
                self.assert_rejected(
                    reason="product status must remain centralised",
                    extra=f"<p>AkashicNET{possessive} current version is v0.16.7</p>",
                )

    def test_adverbial_resolution_assertions_rejected(self):
        for wording in ("has now been", "has finally been", "has been definitively", "is now"):
            for surface in ("home", "progress"):
                with self.subTest(wording=wording, surface=surface):
                    self.assert_rejected(
                        reason="public status surface contradicts BQ001 UNRESOLVED",
                        **{surface: lambda text, w=wording: text + f"<p>BQ001 {w} RESOLVED</p>"},
                    )

    def test_adverbial_negatives_and_possessive_frameworks_pass(self):
        result = self.run_case(
            progress=lambda text: text + (
                "<p>v0.16.7 is currently not the latest release.</p>"
                "<p>v0.16.0-beta.2 has never been released.</p>"
                "<p>BQ001 has not yet been RESOLVED.</p>"
                "<p>BQ001 has never been definitively RESOLVED.</p>"
            ),
            extra="<p>AkashicNET’s METAD v2.1</p><p>AkashicNET's AkashicOMNI v0.3.0</p>",
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_historical_homepage_context_required(self):
        self.assert_rejected(home=lambda text:
            text.replace("Historical sealed release checkpoint", "Current release"))

    def test_bq001_and_no_promotion_boundaries_required(self):
        self.assert_rejected(progress=lambda text:
            text + "<p>BQ001 is RESOLVED</p>")
        self.assert_rejected(progress=lambda text: text + "truth inference enabled")


if __name__ == "__main__":
    unittest.main()
