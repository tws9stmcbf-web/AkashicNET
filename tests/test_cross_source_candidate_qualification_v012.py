from __future__ import annotations

import copy
import json
import unittest

from scripts.validate_cross_source_candidate_qualification_v012 import POLICY, qualifies, validate


def load() -> dict:
    return json.loads(POLICY.read_text(encoding="utf-8"))


class CrossSourceCandidateQualificationV012Tests(unittest.TestCase):
    def test_baseline_policy_passes(self) -> None:
        self.assertEqual(validate(load()), [])

    def test_exact_full_title_qualifies_for_review_only(self) -> None:
        policy = load()
        self.assertTrue(qualifies(policy, [{"type": "EXACT_FULL_TITLE", "normalized_value": "key to the true qabbalah"}]))
        self.assertFalse(policy["candidate_defaults"]["accepted_edge"])

    def test_two_distinct_corroborating_anchors_qualify(self) -> None:
        anchors = [
            {"type": "DISTINCTIVE_NAMED_ENTITY", "normalized_value": "vivekananda"},
            {"type": "DISTINCTIVE_MULTI_TOKEN_PHRASE", "normalized_value": "raja yoga"},
        ]
        self.assertTrue(qualifies(load(), anchors))

    def test_one_corroborating_anchor_fails(self) -> None:
        self.assertFalse(qualifies(load(), [{"type": "DISTINCTIVE_NAMED_ENTITY", "normalized_value": "vivekananda"}]))

    def test_duplicate_corroborating_anchor_fails(self) -> None:
        anchor = {"type": "DISTINCTIVE_NAMED_ENTITY", "normalized_value": "vivekananda"}
        self.assertFalse(qualifies(load(), [anchor, copy.deepcopy(anchor)]))

    def test_generic_token_fails(self) -> None:
        self.assertFalse(qualifies(load(), [{"type": "GENERIC_TERM", "normalized_value": "sacred"}]))

    def test_graph_derived_anchor_fails(self) -> None:
        anchors = [{"type": "EXPLICIT_IDENTIFIER", "normalized_value": "VIVEKANANDA-001", "graph_derived": True}]
        self.assertFalse(qualifies(load(), anchors))

    def test_representation_only_anchor_fails(self) -> None:
        anchors = [{"type": "EXPLICIT_IDENTIFIER", "normalized_value": "VIVEKANANDA-001", "representation_only": True}]
        self.assertFalse(qualifies(load(), anchors))

    def test_automatic_acceptance_cannot_be_enabled(self) -> None:
        policy = load()
        policy["boundaries"]["automated_acceptance_allowed"] = True
        self.assertTrue(any("automated_acceptance_allowed" in error for error in validate(policy)))

    def test_truth_inference_cannot_be_enabled(self) -> None:
        policy = load()
        policy["boundaries"]["automated_truth_inference_allowed"] = True
        self.assertTrue(any("automated_truth_inference_allowed" in error for error in validate(policy)))

    def test_threshold_cannot_be_weakened(self) -> None:
        policy = load()
        policy["qualification"]["corroborating_anchor_minimum"] = 1
        self.assertTrue(any("two corroborating anchors" in error for error in validate(policy)))

    def test_generic_denylist_cannot_be_weakened(self) -> None:
        policy = load()
        policy["qualification"]["generic_terms"].remove("sacred")
        self.assertTrue(any("denylist was weakened" in error for error in validate(policy)))


if __name__ == "__main__":
    unittest.main()
