import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from scripts.prepare_semantic_link_candidates_v020 import (
    DEFAULT_INPUT, V021_OUTPUT, build_packet, validate_packet,
)


def endpoint(endpoint_id, endpoint_type, label, artifact, record, independence):
    return {"endpoint_id": endpoint_id, "endpoint_type": endpoint_type, "label": label,
            "provenance": {"artifact_id": artifact, "record_id": record, "independence_key": independence, "public_safe": True}}


class TestSemanticLinkCandidates(unittest.TestCase):
    def packet(self):
        registry = {"endpoints": [
            endpoint("endpoint:topic:consciousness", "TOPIC", "Consciousness", "artifact:topics", "consciousness", "source:topics"),
            endpoint("endpoint:evidence:alpha", "EVIDENCE_RECORD", "A study of consciousness", "artifact:evidence", "alpha", "source:evidence:alpha"),
            endpoint("endpoint:evidence:art", "EVIDENCE_RECORD", "S-ART framework", "artifact:evidence", "art", "source:evidence:art"),
            endpoint("endpoint:topic:art", "TOPIC", "Art", "artifact:topics", "art", "source:topics"),
        ]}
        return build_packet((json.dumps(registry, sort_keys=True) + "\n").encode())

    def test_exact_whole_term_proposes_one_review_candidate(self):
        packet = self.packet()
        self.assertEqual(validate_packet(packet), [])
        self.assertEqual(packet["summary"]["candidate_count"], 1)
        candidate = packet["proposed_candidates"][0]
        self.assertEqual(candidate["assertion_class"], "INFERRED_CANDIDATE")
        self.assertEqual(candidate["review_state"], "REVIEW_REQUIRED")
        self.assertFalse(candidate["accepted_edge"])

    def test_short_acronym_topic_is_excluded(self):
        self.assertNotIn("endpoint:topic:art", [c["target_topic"]["endpoint_id"] for c in self.packet()["proposed_candidates"]])

    def mutate(self, change):
        packet = self.packet(); change(packet); self.assertTrue(validate_packet(packet))

    def test_truth_inference_fails_closed(self): self.mutate(lambda p: p["boundaries"].__setitem__("automated_truth_inference_allowed", True))
    def test_acceptance_fails_closed(self): self.mutate(lambda p: p["proposed_candidates"][0].__setitem__("accepted_edge", True))
    def test_edge_creation_fails_closed(self): self.mutate(lambda p: p["accepted_edges"].append({"edge_id": "forbidden"}))
    def test_graph_signal_fails_closed(self): self.mutate(lambda p: p["proposed_candidates"][0]["signal_controls"].__setitem__("graph_derived", True))
    def test_transitive_inference_fails_closed(self): self.mutate(lambda p: p["proposed_candidates"][0]["signal_controls"].__setitem__("transitive_inference", True))
    def test_representation_signal_fails_closed(self): self.mutate(lambda p: p["proposed_candidates"][0]["signal_controls"].__setitem__("representation_count_used", True))
    def test_private_metadata_fails_closed(self): self.mutate(lambda p: p.__setitem__("drive_id", "private"))
    def test_anchor_tampering_fails_closed(self): self.mutate(lambda p: p["proposed_candidates"][0]["anchor_evidence"].__setitem__("source_token_start", 0))
    def test_same_artifact_fails_closed(self): self.mutate(lambda p: p["proposed_candidates"][0]["target_topic"]["provenance"].__setitem__("artifact_id", "artifact:evidence"))
    def test_summary_fails_closed(self): self.mutate(lambda p: p["summary"].__setitem__("candidate_count", 99))

    def test_current_registry_reproduces_v021_packet_exactly(self):
        packet = build_packet(DEFAULT_INPUT.read_bytes(), "0.2.1")
        self.assertEqual(validate_packet(packet, "0.2.1"), [])
        self.assertEqual(json.dumps(packet, indent=2, ensure_ascii=False) + "\n",
                         V021_OUTPUT.read_text(encoding="utf-8"))
        self.assertEqual(packet["summary"]["accepted_edges"], 0)
        self.assertTrue(all(c["review_state"] == "REVIEW_REQUIRED"
                            for c in packet["proposed_candidates"]))

    def test_v021_version_and_boundary_mutations_fail_closed(self):
        packet = build_packet(DEFAULT_INPUT.read_bytes(), "0.2.1")
        self.assertIn("version or mode", validate_packet(packet, "0.2.0"))
        packet["proposed_candidates"][0]["accepted_edge"] = True
        self.assertIn("review gate", validate_packet(packet, "0.2.1"))

    def test_preparation_workflow_preserves_historical_packet(self):
        root = DEFAULT_INPUT.parents[2]
        workflow = (root / ".github/workflows/prepare-semantic-link-candidates.yml").read_text()
        command = next(line.strip() for line in workflow.splitlines()
                       if line.strip().startswith("python scripts/prepare_semantic_link_candidates_v020.py"))
        with tempfile.TemporaryDirectory() as directory:
            sandbox = Path(directory)
            for relative in ("scripts/prepare_semantic_link_candidates_v020.py",
                             "references/community/public-safe-semantic-endpoint-registry-v0.1.9.json",
                             "references/community/semantic-link-candidates-v0.2.0.json"):
                target = sandbox / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(root / relative, target)
            historical = sandbox / "references/community/semantic-link-candidates-v0.2.0.json"
            before = historical.read_bytes()
            subprocess.run([sys.executable, *command.split()[1:]], cwd=sandbox,
                           check=True, capture_output=True, text=True)
            self.assertEqual(historical.read_bytes(), before)
            current = sandbox / V021_OUTPUT.relative_to(root)
            self.assertEqual(current.read_bytes(), V021_OUTPUT.read_bytes())
            packet = json.loads(current.read_bytes())
            self.assertEqual(validate_packet(packet, "0.2.1"), [])


if __name__ == "__main__":
    unittest.main()
