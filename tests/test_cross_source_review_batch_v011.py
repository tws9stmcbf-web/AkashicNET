from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_cross_source_review_batch_v011 import (
    BATCH,
    DRIVE_ARTIFACT,
    REDDIT_ARTIFACT,
    validate_batch,
)


def load() -> dict:
    return json.loads(Path(BATCH).read_text(encoding="utf-8"))


class CrossSourceReviewBatchV011Tests(unittest.TestCase):
    def test_baseline_passes_with_zero_accepted_edges(self) -> None:
        data = load()
        self.assertEqual(validate_batch(data), [])
        self.assertEqual(sum(e["accepted_edge"] is True for e in data["edges"]), 0)

    def test_candidate_cannot_self_accept(self) -> None:
        data = load()
        data["edges"][0]["accepted_edge"] = True
        self.assertTrue(any("accepted_edge must be False" in e for e in validate_batch(data)))

    def test_candidate_cannot_claim_accepted_review_state(self) -> None:
        data = load()
        data["edges"][0]["review_state"] = "ACCEPTED"
        self.assertTrue(any("review_state must be 'REVIEW_REQUIRED'" in e for e in validate_batch(data)))

    def test_truth_inference_switch_fails_closed(self) -> None:
        data = load()
        data["policy"]["truth_inference_allowed"] = True
        self.assertTrue(any("truth_inference_allowed" in e or "policy" in e for e in validate_batch(data)))

    def test_source_digest_drift_is_rejected(self) -> None:
        data = load()
        data["artifacts"][0]["sha256"] = "0" * 64
        self.assertTrue(any("source digest mismatch" in e for e in validate_batch(data)))

    def test_duplicate_independence_key_is_rejected(self) -> None:
        data = load()
        data["artifacts"][1]["independence_key"] = data["artifacts"][0]["independence_key"]
        self.assertTrue(any("duplicate independence_key" in e for e in validate_batch(data)))

    def test_graph_parent_amplification_is_rejected(self) -> None:
        data = load()
        data["edges"][1]["parent_edge_ids"] = [data["edges"][0]["edge_id"]]
        self.assertTrue(any("no graph-derived parents" in e for e in validate_batch(data)))

    def test_missing_confidence_source_is_rejected(self) -> None:
        data = load()
        data["edges"][0]["confidence_source_artifact_ids"] = [REDDIT_ARTIFACT]
        self.assertTrue(any("confidence sources must cite both inputs" in e for e in validate_batch(data)))

    def test_reversed_domains_are_rejected(self) -> None:
        data = load()
        data["edges"][0]["source"]["artifact_id"] = DRIVE_ARTIFACT
        data["edges"][0]["target"]["artifact_id"] = REDDIT_ARTIFACT
        errors = validate_batch(data)
        self.assertTrue(any("Reddit source" in e for e in errors))
        self.assertTrue(any("Drive public-family target" in e for e in errors))

    def test_private_drive_identifier_key_is_rejected(self) -> None:
        data = load()
        data["edges"][0]["drive_object_id"] = "private-object"
        self.assertTrue(any("private-boundary key prohibited" in e for e in validate_batch(data)))

    def test_batch_size_cannot_expand_silently(self) -> None:
        data = load()
        extra = copy.deepcopy(data["edges"][0])
        extra["edge_id"] = "edge:review-batch-0004"
        data["edges"].append(extra)
        self.assertTrue(any("exactly 3 edges" in e for e in validate_batch(data)))


if __name__ == "__main__":
    unittest.main()
