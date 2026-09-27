import copy
import json
import shutil
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

    def validate(self, tamper=None):
        # Run the real CLI against an isolated copy; never modify the census.
        with tempfile.TemporaryDirectory() as directory:
            for relative in (
                "references/community/reddit-semantic-index.csv",
                "references/consciousness/interbrain-telepathy-mayim-bialik-source-crawl-v0.1.json",
            ):
                fixture = Path(directory) / relative
                fixture.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / relative, fixture)
                if relative == tamper:
                    fixture.write_bytes(fixture.read_bytes() + b"\n")
            path = Path(directory) / ARTIFACT
            path.parent.mkdir(parents=True, exist_ok=True)
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


    def assert_rejected(self):
        result = self.validate()
        self.assertNotEqual(result.returncode, 0, result.stdout)

    def test_vocabulary_and_normalization_drift_fail(self):
        original = copy.deepcopy(self.data)
        for field, value in (("normalization", "substring"), ("matching", "any substring"),
                             ("seed_post_ids", {}), ("supplemental_metadata", [])):
            with self.subTest(field=field):
                self.data = copy.deepcopy(original)
                self.data["method"]["discovery"][field] = value
                self.assert_rejected()
        self.data = copy.deepcopy(original)
        self.data["method"]["discovery"]["vocabulary"]["CHN"].append("channel")
        self.assert_rejected()

    def test_counts_and_discovery_membership_drift_fail(self):
        original = copy.deepcopy(self.data)
        for field in ("matched_manifestations", "provisional_unique_source_lineages"):
            with self.subTest(field=field):
                self.data = copy.deepcopy(original)
                self.data["lanes"]["TEL"][field] += 1
                self.assert_rejected()
        self.data = copy.deepcopy(original)
        block = self.data["lanes"]["TEL"]
        block["records"].pop(0)
        block["matched_manifestations"] -= 1
        block["provisional_unique_source_lineages"] -= 1
        self.assert_rejected()  # Internally consistent counts cannot hide an omission.

    def test_unlisted_bare_channel_record_fails(self):
        block = self.data["lanes"]["CHN"]
        record = copy.deepcopy(block["records"][0])
        record.update(post_id="1ln91sj", title_slug="howto_channel_consciousnesses_jun_2025",
                      reddit_url="https://www.reddit.com/r/NeuronsToNirvana/comments/1ln91sj/howto_channel_consciousnesses_jun_2025/",
                      source_lineage_id="RSL-1LN91SJ")
        block["records"].append(record)
        block["matched_manifestations"] += 1
        block["provisional_unique_source_lineages"] += 1
        self.assert_rejected()

    def test_unsupported_governed_mappings_fail(self):
        original = copy.deepcopy(self.data)
        for lane in ("TEL", "CHN", "PK"):
            with self.subTest(lane=lane):
                self.data = copy.deepcopy(original)
                block = self.data["lanes"][lane]
                selected = block["selected_for_full_provenance_review"]
                record = next(r for r in block["records"] if r["post_id"] == selected["post_id"])
                record["lineage_basis"] = selected["lineage_basis"] = "GOVERNED_SOURCE_MAPPING"
                self.assert_rejected()

    def test_provisional_review_state_and_source_url_cannot_be_elevated(self):
        original = copy.deepcopy(self.data)
        for key, value in (("review_state", "VERIFIED_OFFICIAL_SECONDARY"),
                           ("underlying_source_urls", ["https://example.org/unverified"])):
            with self.subTest(key=key):
                self.data = copy.deepcopy(original)
                block = self.data["lanes"]["TEL"]
                selected = block["selected_for_full_provenance_review"]
                record = next(r for r in block["records"] if r["post_id"] == selected["post_id"])
                record[key] = selected[key] = value
                self.assert_rejected()

    def test_governed_locator_and_hash_are_required(self):
        original = copy.deepcopy(self.data)
        for field in ("path", "git_blob_sha", "pre_existing_commit", "json_pointer"):
            with self.subTest(field=field):
                self.data = copy.deepcopy(original)
                record = next(r for r in self.data["lanes"]["PSI-PERSON"]["records"] if r["post_id"] == "1oyi2qp")
                record["repository_provenance"][field] = "fabricated"
                self.assert_rejected()
        self.data = copy.deepcopy(original)
        record = next(r for r in self.data["lanes"]["PSI-PERSON"]["records"] if r["post_id"] == "1oyi2qp")
        del record["repository_provenance"]
        self.assert_rejected()

    def test_fabricated_or_altered_selections_fail(self):
        original = copy.deepcopy(self.data)
        selected = original["lanes"]["TEL"]["selected_for_full_provenance_review"]
        record = next(r for r in original["lanes"]["TEL"]["records"] if r["post_id"] == selected["post_id"])
        for field, value in record.items():
            with self.subTest(field=field):
                self.data = copy.deepcopy(original)
                self.data["lanes"]["TEL"]["selected_for_full_provenance_review"][field] = "altered"
                self.assert_rejected()
            with self.subTest(missing=field):
                self.data = copy.deepcopy(original)
                del self.data["lanes"]["TEL"]["selected_for_full_provenance_review"][field]
                self.assert_rejected()

    def test_selection_from_another_lane_fails(self):
        self.data["lanes"]["TEL"]["selected_for_full_provenance_review"] = copy.deepcopy(
            self.data["lanes"]["PRE"]["selected_for_full_provenance_review"])
        self.data["lanes"]["TEL"]["selected_for_full_provenance_review"]["lane"] = "TEL"
        self.assert_rejected()

    def test_duplicate_lane_record_fails(self):
        block = self.data["lanes"]["TEL"]
        block["records"].append(copy.deepcopy(block["records"][0]))
        block["matched_manifestations"] += 1
        self.assert_rejected()

    def test_changed_repository_blob_bytes_fail(self):
        for path in (
            "references/community/reddit-semantic-index.csv",
            "references/consciousness/interbrain-telepathy-mayim-bialik-source-crawl-v0.1.json",
        ):
            with self.subTest(path=path):
                result = self.validate(tamper=path)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("pinned blob mismatch", result.stderr)

    def test_shared_lineage_order_does_not_change_membership(self):
        self.data["cross_lane_lineages"].reverse()
        for summary in self.data["cross_lane_lineages"]:
            summary["manifestations"].reverse()
            summary["lanes"].reverse()
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_or_duplicate_shared_lineages_fail(self):
        original = copy.deepcopy(self.data)
        for mutation in ("empty", "omitted", "duplicate"):
            with self.subTest(mutation=mutation):
                self.data = copy.deepcopy(original)
                summaries = self.data["cross_lane_lineages"]
                if mutation == "empty":
                    summaries.clear()
                elif mutation == "omitted":
                    summaries.pop()
                else:
                    summaries.append(copy.deepcopy(summaries[0]))
                self.assert_rejected()

    def test_altered_shared_lineage_fields_fail(self):
        original = copy.deepcopy(self.data)
        mutations = (
            ("source_lineage_id", "RSL-FABRICATED"),
            ("manifestations", ["https://example.org/fabricated"]),
            ("manifestations", []),
            ("lanes", ["PK"]),
            ("lanes", []),
            ("evidence_transfer_allowed", True),
            ("independent_corroboration", True),
        )
        for field, value in mutations:
            with self.subTest(field=field, value=value):
                self.data = copy.deepcopy(original)
                self.data["cross_lane_lineages"][0][field] = value
                self.assert_rejected()
        for field in original["cross_lane_lineages"][0]:
            with self.subTest(missing=field):
                self.data = copy.deepcopy(original)
                del self.data["cross_lane_lineages"][0][field]
                self.assert_rejected()

    def test_duplicate_summary_members_and_unshared_lineage_fail(self):
        original = copy.deepcopy(self.data)
        for field in ("manifestations", "lanes"):
            with self.subTest(field=field):
                self.data = copy.deepcopy(original)
                values = self.data["cross_lane_lineages"][0][field]
                values.append(values[0])
                self.assert_rejected()
        self.data = copy.deepcopy(original)
        # A real record is insufficient: this lineage is not shared.
        record = self.data["lanes"]["TEL"]["records"][0]
        self.data["cross_lane_lineages"].insert(0, {
            "source_lineage_id": record["source_lineage_id"],
            "manifestations": [record["reddit_url"]],
            "lanes": [record["lane"]],
            "evidence_transfer_allowed": False,
            "independent_corroboration": False,
        })
        self.assert_rejected()

    def test_index_pin_drift_fails(self):
        self.data["source_surface"]["git_blob_sha"] = "0" * 40
        self.assert_rejected()


if __name__ == "__main__":
    unittest.main()

