import copy
import unittest

from scripts.prepare_audited_cross_source_review import build_packet, validate_packet


CSV_HEADER = "title,reddit_url,short_summary,toolkit_framework,research_question_potential\n"
DRIVE = b"""| family_id | canonical work | disposition | confidence |
|---|---|---|---|
| ALPHA-001 | Exact Alpha Title | SAME_LOGICAL_WORK_FAMILY | HIGH |
"""


class TestAuditedCrossSourceOrchestrator(unittest.TestCase):
    def packet(self, title="Exact Alpha Title", summary="", framework=""):
        row = f"{title},https://www.reddit.com/r/example/comments/abc123/example/,{summary},{framework},question\n"
        return build_packet((CSV_HEADER + row).encode(), DRIVE)

    def test_exact_title_proposes_review_candidate(self):
        packet = self.packet()
        self.assertEqual(validate_packet(packet), [])
        self.assertEqual(packet["summary"]["exact_anchor_candidates"], 1)
        candidate = packet["proposed_candidates"][0]
        self.assertEqual(candidate["review_state"], "REVIEW_REQUIRED")
        self.assertFalse(candidate["accepted_edge"])
        self.assertEqual(candidate["anchor_evidence"][0]["anchor_type"], "EXACT_FULL_TITLE")

    def test_explicit_identifier_proposes_review_candidate(self):
        packet = self.packet(title="Different", summary="Explicit ALPHA-001 reference")
        self.assertEqual(validate_packet(packet), [])
        self.assertEqual(packet["proposed_candidates"][0]["anchor_evidence"][0]["anchor_type"], "EXPLICIT_IDENTIFIER")

    def test_thematic_similarity_does_not_propose(self):
        packet = self.packet(title="Alpha reflections", summary="Similar themes only")
        self.assertEqual(validate_packet(packet), [])
        self.assertEqual(packet["proposed_candidates"], [])

    def mutate(self, change):
        packet = self.packet()
        change(packet)
        self.assertTrue(validate_packet(packet))

    def test_truth_inference_fails_closed(self):
        self.mutate(lambda p: p["boundaries"].__setitem__("automated_truth_inference_allowed", True))

    def test_acceptance_fails_closed(self):
        self.mutate(lambda p: p["proposed_candidates"][0].__setitem__("accepted_edge", True))

    def test_edge_creation_fails_closed(self):
        self.mutate(lambda p: p["accepted_edges"].append({"edge_id": "forbidden"}))

    def test_graph_signal_fails_closed(self):
        self.mutate(lambda p: p["proposed_candidates"][0]["anchor_evidence"][0].__setitem__("graph_derived", True))

    def test_private_metadata_fails_closed(self):
        self.mutate(lambda p: p.__setitem__("drive_id", "private"))

    def test_missing_anchor_fails_closed(self):
        self.mutate(lambda p: p["proposed_candidates"][0].__setitem__("anchor_evidence", []))


if __name__ == "__main__":
    unittest.main()
