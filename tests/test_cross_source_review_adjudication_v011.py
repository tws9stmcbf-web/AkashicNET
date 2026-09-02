from __future__ import annotations

import copy
import json
import unittest

from scripts.validate_cross_source_review_adjudication_v011 import DATA, validate_adjudication


def load() -> dict:
    return json.loads(DATA.read_text(encoding="utf-8"))


class CrossSourceReviewAdjudicationV011Tests(unittest.TestCase):
    def test_baseline_rejects_three_and_accepts_zero(self) -> None:
        data = load()
        self.assertEqual(validate_adjudication(data), [])
        self.assertEqual(sum(e["review_state"] == "REJECTED" for e in data["edges"]), 3)
        self.assertFalse(any(e["accepted_edge"] for e in data["edges"]))

    def test_rejection_cannot_be_promoted(self) -> None:
        data = load()
        data["edges"][3]["accepted_edge"] = True
        self.assertTrue(any("accept zero edges" in e for e in validate_adjudication(data)))

    def test_decision_requires_candidate_parent(self) -> None:
        data = load()
        data["edges"][3]["parent_edge_ids"] = []
        self.assertTrue(any("candidate parent" in e for e in validate_adjudication(data)))

    def test_decision_endpoint_drift_is_rejected(self) -> None:
        data = load()
        data["edges"][3]["target"]["record_id"] = "OTHER"
        self.assertTrue(any("endpoints drifted" in e for e in validate_adjudication(data)))

    def test_decision_relationship_drift_is_rejected(self) -> None:
        data = load()
        data["edges"][3]["relationship"] = "NEGATIVE_EVIDENCE"
        self.assertTrue(any("relationship drifted" in e for e in validate_adjudication(data)))

    def test_missing_adjudication_reference_is_rejected(self) -> None:
        data = load()
        del data["edges"][3]["adjudication_ref"]
        self.assertTrue(any("adjudication_ref" in e or "decision reference" in e for e in validate_adjudication(data)))

    def test_duplicate_review_independence_is_rejected(self) -> None:
        data = load()
        data["artifacts"][2]["independence_key"] = data["artifacts"][0]["independence_key"]
        decision = data["edges"][3]
        decision["confidence_source_artifact_ids"].append(data["artifacts"][0]["artifact_id"])
        self.assertTrue(any("duplicate independence_key" in e for e in validate_adjudication(data)))

    def test_lineage_cycle_is_rejected(self) -> None:
        data = load()
        data["edges"][0]["parent_edge_ids"] = [data["edges"][3]["edge_id"]]
        self.assertTrue(any("cyclic edge lineage" in e for e in validate_adjudication(data)))

    def test_policy_cannot_enable_truth_inference(self) -> None:
        data = load()
        data["policy"]["truth_inference_allowed"] = True
        self.assertTrue(any("truth_inference_allowed" in e or "policy" in e for e in validate_adjudication(data)))


if __name__ == "__main__":
    unittest.main()
