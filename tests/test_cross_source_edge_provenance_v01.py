from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from scripts.validate_cross_source_edge_provenance_v01 import validate

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "references" / "community" / "cross-source-edge-provenance-fixtures-v0.1.json"


def load() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class CrossSourceEdgeProvenanceTests(unittest.TestCase):
    def test_baseline_fixture_passes_and_promotes_nothing(self) -> None:
        data = load()
        self.assertEqual(validate(data), [])
        self.assertEqual(sum(edge["accepted_edge"] is True for edge in data["edges"]), 0)

    def test_missing_generator_fails_closed(self) -> None:
        data = load()
        del data["edges"][1]["generator"]
        self.assertTrue(any("lacks generator provenance" in error for error in validate(data)))

    def test_self_cycle_fails_closed(self) -> None:
        data = load()
        data["edges"][1]["parent_edge_ids"] = [data["edges"][1]["edge_id"]]
        self.assertTrue(any("cycle" in error for error in validate(data)))

    def test_multi_edge_cycle_fails_closed(self) -> None:
        data = load()
        data["edges"][1]["parent_edge_ids"] = ["edge:hold:0001"]
        self.assertTrue(any("cyclic edge lineage" in error for error in validate(data)))

    def test_reverse_edge_feedback_fails_closed(self) -> None:
        data = load()
        reverse = copy.deepcopy(data["edges"][0])
        reverse["edge_id"] = "edge:reverse:0001"
        reverse["source"], reverse["target"] = reverse["target"], reverse["source"]
        reverse["parent_edge_ids"] = ["edge:direct:0001"]
        data["edges"].append(reverse)
        self.assertTrue(any("reverse-edge feedback loop" in error for error in validate(data)))

    def test_unadjudicated_promotion_fails_closed(self) -> None:
        data = load()
        data["edges"][1]["accepted_edge"] = True
        data["edges"][1]["review_state"] = "ACCEPTED"
        self.assertTrue(any("promoted without explicit accepted adjudication" in error for error in validate(data)))

    def test_representation_count_cannot_increase_strength(self) -> None:
        data = load()
        data["edges"][1]["representation_count"] = 20
        self.assertTrue(any("representation_count cannot contribute" in error for error in validate(data)))

    def test_unknown_source_artifact_fails_closed(self) -> None:
        data = load()
        data["edges"][0]["source"]["artifact_id"] = "artifact:missing"
        self.assertTrue(any("unresolvable source reference" in error for error in validate(data)))

    def test_policy_cannot_enable_truth_inference(self) -> None:
        data = load()
        data["policy"]["truth_inference_allowed"] = True
        self.assertTrue(any("policy must remain false: truth_inference_allowed" in error for error in validate(data)))


if __name__ == "__main__":
    unittest.main()
