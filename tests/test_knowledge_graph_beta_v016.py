import copy
import hashlib
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.build_knowledge_graph_beta_fixture_v016 import OUTPUT, SOURCE_SPECS, build
from scripts.validate_knowledge_graph_beta_v016 import validate

DATA = json.loads(OUTPUT.read_text())


class TestKnowledgeGraphBetaV016(unittest.TestCase):
    def mutate(self, operation, expected=None):
        data = copy.deepcopy(DATA)
        operation(data)
        errors = validate(data)
        self.assertTrue(errors)
        if expected:
            self.assertIn(expected, errors)

    def test_baseline(self):
        self.assertEqual(validate(DATA), [])

    def test_generation_is_deterministic(self):
        self.assertEqual(build(), DATA)
        self.assertEqual(build(), build())

    def test_review_generation_survives_source_digest_drift(self):
        original = Path.read_bytes

        def drifted(path):
            raw = original(path)
            if str(path).endswith("spec-v0.1.json"):
                return raw + b"\n"
            return raw

        with patch.object(Path, "read_bytes", autospec=True, side_effect=drifted):
            generated = build()
            self.assertNotEqual(
                generated["source_artifacts"][0]["sha256"],
                SOURCE_SPECS["artifact:bq001-spec:0.1"]["sha256"],
            )
            self.assertIn("source artifacts", validate(generated))

    def test_sealed_baseline_lock(self):
        self.mutate(lambda d: d["baseline_locks"].__setitem__("v0.14", "0" * 40), "sealed baseline locks")

    def test_question_remains_unresolved(self):
        self.mutate(lambda d: d.__setitem__("question_status", "RESOLVED"), "question status")

    def test_truth_inference_stays_off(self):
        self.mutate(lambda d: d["boundaries"].__setitem__("automated_truth_inference_allowed", True), "unsafe boundaries")

    def test_source_declaration_cannot_move(self):
        self.mutate(lambda d: d["source_artifacts"][0].__setitem__("sha256", "0" * 64), "source artifacts")

    def test_source_bytes_and_declaration_cannot_move_together(self):
        data = copy.deepcopy(DATA)
        tampered = json.dumps({"valid": "but not the governed source"}).encode()
        moved = hashlib.sha256(tampered).hexdigest()
        data["source_artifacts"][0]["sha256"] = moved
        for node in data["nodes"]:
            if node["provenance"]["artifact_id"] == data["source_artifacts"][0]["artifact_id"]:
                node["provenance"]["sha256"] = moved
        for edge in data["edges"]:
            if edge["provenance"]["artifact_id"] == data["source_artifacts"][0]["artifact_id"]:
                edge["provenance"]["sha256"] = moved
        with patch.object(Path, "read_bytes", return_value=tampered):
            self.assertTrue(validate(data))

    def test_duplicate_node_id(self):
        self.mutate(lambda d: d["nodes"][1].__setitem__("node_id", d["nodes"][0]["node_id"]), "node IDs")

    def test_invalid_node_type(self):
        self.mutate(lambda d: d["nodes"][0].__setitem__("node_type", "TRUTH"), "nodes")

    def test_node_id_cannot_use_edge_namespace(self):
        self.mutate(lambda d: d["nodes"][0].__setitem__("node_id", "edge:question:BQ001"), "nodes")

    def test_missing_endpoint(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("target_node_id", "node:missing"), "edge endpoints")

    def test_self_edge(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("target_node_id", d["edges"][0]["source_node_id"]), "self edge")

    def test_unknown_relationship(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("relationship_type", "PROVES"), "edges")

    def test_edge_id_cannot_use_node_namespace(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("edge_id", "node:not-an-edge"), "edges")

    def test_no_edge_is_accepted(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("accepted_edge", True), "accepted edges prohibited")

    def test_inferred_candidate_requires_review(self):
        self.mutate(lambda d: d["edges"][1].__setitem__("review_state", "SOURCE_ASSERTED"), "inferred review boundary")

    def test_direct_metadata_requires_direct_provenance(self):
        self.mutate(lambda d: d["edges"][0]["provenance"].__setitem__("derivation_method", "HUMAN_REVIEW_CANDIDATE"), "direct metadata boundary")

    def test_correction_not_mislabeled_retracted(self):
        self.mutate(lambda d: d["edges"][3].__setitem__("edge_state", "RETRACTED"), "correction state")

    def test_competing_models_remain_review_only(self):
        self.mutate(lambda d: d["edges"][2].__setitem__("edge_state", "ACTIVE"), "contradiction state")

    def test_duplicate_independence_key_rejected(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("evidence_independence_keys", [d["edges"][0]["evidence_independence_keys"][0]] * 2), "evidence independence")

    def test_unknown_independence_key_rejected(self):
        self.mutate(lambda d: d["edges"][0].__setitem__("evidence_independence_keys", ["source:invented"]), "evidence independence")

    def test_missing_record_locator(self):
        self.mutate(lambda d: d["nodes"][0]["provenance"].__setitem__("record_locator", "/missing"), "record locator")

    def test_unknown_parent_edge(self):
        self.mutate(lambda d: d["edges"][0]["parent_edge_ids"].append("edge:missing"), "edge ancestry")

    def test_circular_parent_lineage(self):
        def cycle(data):
            data["edges"][0]["parent_edge_ids"] = [data["edges"][1]["edge_id"]]
            data["edges"][1]["parent_edge_ids"] = [data["edges"][0]["edge_id"]]
        self.mutate(cycle, "circular ancestry")

    def test_private_key_rejected(self):
        self.mutate(lambda d: d.__setitem__("drive_id", "private"), "private metadata")

    def test_private_marker_nested_in_array_rejected(self):
        self.mutate(lambda d: d["edges"][0]["evidence_independence_keys"].append("copy_AKM-001234.pdf"), "private metadata")

    def test_private_path_nested_in_array_rejected(self):
        self.mutate(lambda d: d["edges"][0]["parent_edge_ids"].append("/My Drive/private.pdf"), "private metadata")

    def test_summary_is_derived(self):
        self.mutate(lambda d: d["summary"].__setitem__("accepted_edge_count", 1), "summary")


if __name__ == "__main__":
    unittest.main()
