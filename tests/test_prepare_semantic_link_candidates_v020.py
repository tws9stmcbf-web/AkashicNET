import copy
import json
import unittest

from scripts.prepare_semantic_link_candidates_v020 import build_packet, validate_packet


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


if __name__ == "__main__":
    unittest.main()
