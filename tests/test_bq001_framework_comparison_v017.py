import copy
import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/validate_bq001_framework_comparison_v017.py"
SPEC = importlib.util.spec_from_file_location("comparison_validator", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class FrameworkComparisonValidationTests(unittest.TestCase):
    def setUp(self):
        self.packet = validator.load_json(validator.PACKET)

    def validate(self, packet):
        validator.validate(packet, verify_git=False)

    def mutate(self, change, pattern=None):
        candidate = copy.deepcopy(self.packet)
        change(candidate)
        context = self.assertRaisesRegex(Exception, pattern) if pattern else self.assertRaises(Exception)
        with context:
            self.validate(candidate)

    def test_reviewed_packet_passes(self):
        self.validate(self.packet)

    def test_core_review_only_boundaries_are_closed(self):
        self.mutate(lambda d: d.update(question_status="RESOLVED"))
        self.mutate(lambda d: d.update(accepted_edges=1))
        self.mutate(lambda d: d.update(mode="PUBLIC_SYNTHESIS"))
        self.mutate(lambda d: d["operational_boundaries"].update(reddit_live_access="LIVE"))
        self.mutate(lambda d: d["promotion_guards"].update(truth_inference_allowed=True))

    def test_adjudicative_fields_fail_closed(self):
        self.mutate(lambda d: d["comparison_rows"][0].update(score=0.9))
        with self.assertRaisesRegex(ValueError, "adjudicative key rejected"):
            validator.scan_safety({"winner": "synthetic"})

    def test_inventory_projection_cannot_drift(self):
        self.mutate(lambda d: d["comparison_rows"][2].update(canonical_name="Synthetic"), "inventory projection drift")
        self.mutate(lambda d: d["comparison_rows"][2]["linked_record_ids"].pop(), "inventory projection drift")
        self.mutate(lambda d: d["comparison_rows"][0].update(comparison_state="INTERPRETIVE_FRAMEWORK_NOT_EMPIRICAL_ADJUDICATION"), "comparison state drift")

    def test_counter_inferences_and_research_gaps_are_preserved(self):
        self.mutate(lambda d: d["counter_inferences"].pop())
        self.mutate(lambda d: d["research_gaps"].pop())

    def test_shared_source_is_not_double_counted(self):
        self.mutate(lambda d: d["shared_ancestry_groups"][0]["inventory_item_ids"].pop())
        self.mutate(lambda d: d["comparison_rows"][-1].update(independence_state="UNASSESSED_REVIEW_REQUIRED"), "inventory projection drift")

    def test_correction_record_is_preserved(self):
        self.mutate(lambda d: d["correction_records"][0].update(evidence_label_changed=True))
        self.mutate(lambda d: d["correction_records"].clear())

    def test_input_commit_and_blobs_are_pinned(self):
        self.mutate(lambda d: d.update(input_commit="0" * 40))
        self.mutate(lambda d: d["input_anchors"][0].update(git_blob_sha="0" * 40), "input anchor mapping drift")

    def test_private_drive_markers_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "private Drive/Docs marker rejected"):
            validator.scan_safety("https://drive.google.com/file/d/private")

    def test_duplicate_keys_and_nonfinite_json_fail_closed(self):
        for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                validator.load_json(raw)


if __name__ == "__main__":
    unittest.main()
