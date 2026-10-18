import copy
import math
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.review_contradictions import build_queue
from scripts.quantum_order_demo import compare


def fixture():
    scope = dict(population="adults", conditions="trial", definition="outcome", time="week4")
    return {"claims": [{"id": i, "text": text, "scope": dict(scope),
                        "sources": [{"ref": "source-"+i, "passage": text}]}
                       for i, text in [("A", "effect"), ("B", "no effect"), ("C", "uncertain")]],
            "pairs": [{"claims": ["A", "B"]}, {"claims": ["B", "C"]}]}


class QueueTests(unittest.TestCase):
    def test_malformed_contract_rejected(self):
        for data in ([], {}, {"claims": {}, "pairs": []},
                     {"claims": [None], "pairs": []},
                     {"claims": [], "pairs": [None]}):
            with self.assertRaises(ValueError): build_queue(data)

    def test_unknown_scope_never_classified_as_conflict(self):
        d = fixture()
        for c in d["claims"]: c["scope"] = {}
        self.assertTrue(all(r["state"] == "needs_context" for r in build_queue(d)["queue"]))

    def test_missing_source_precedes_conflict_and_budget_defers(self):
        d = fixture(); d["claims"][2]["sources"] = []
        q = build_queue(d, 1)
        self.assertEqual(q["queue"][0]["state"], "needs_source")
        self.assertEqual(q["deferred"], 1)
        self.assertFalse(q["truth_promotion"])
        self.assertFalse(q["publication_allowed"])
        self.assertFalse(q["scientific_evidence_promotion_allowed"])
        self.assertEqual(q["claims"], d["claims"])

    def test_scope_difference_retained(self):
        d = fixture(); d["claims"][0]["scope"]["population"] = "children"
        self.assertEqual(build_queue(d)["queue"][0]["different_scope"], ["population"])

    def test_input_order_invariance_and_no_mutation(self):
        d = fixture(); before = copy.deepcopy(d); expected = build_queue(d)
        self.assertEqual(d, before)
        d["claims"].reverse(); d["pairs"].reverse()
        for p in d["pairs"]: p["claims"].reverse()
        self.assertEqual(build_queue(d), expected)

    def test_duplicate_unknown_and_invalid_budget_rejected(self):
        d = fixture(); d["pairs"].append({"claims": ["B", "A"]})
        with self.assertRaises(ValueError): build_queue(d)
        d = fixture(); d["pairs"][0]["claims"][0] = "missing"
        with self.assertRaises(ValueError): build_queue(d)
        for b in (-1, True, 1.5):
            with self.assertRaises(ValueError): build_queue(fixture(), b)

    def test_zero_budget_and_human_gate(self):
        q = build_queue(fixture(), 0)
        self.assertEqual(q["queue"], [])
        self.assertEqual(q["deferred"], 2)
        self.assertTrue(q["requires_researcher_adjudication"])


class QuantumTests(unittest.TestCase):
    def test_known_noncommuting_case(self):
        q = compare(0, 0, 45)
        self.assertAlmostEqual(q["AB"][0][0], 0.5)
        self.assertAlmostEqual(q["BA_aligned"][0][0], 0.25)
        self.assertAlmostEqual(q["total_variation"], 0.5)
        self.assertAlmostEqual(q["qq_residual"], 0)

    def test_commuting_and_normalization(self):
        for state in (0, 17, 90):
            for a, b in ((0, 0), (0, 90), (13, 53)):
                q = compare(state, a, b)
                for k in ("AB", "BA_aligned"):
                    self.assertAlmostEqual(sum(map(sum, q[k])), 1)
                    self.assertTrue(all(0 <= v <= 1 for row in q[k] for v in row))
                self.assertAlmostEqual(q["qq_residual"], 0)
                if (a, b) in ((0, 0), (0, 90)):
                    self.assertAlmostEqual(q["total_variation"], 0)

    def test_nonfinite_rejected(self):
        for x in (math.nan, math.inf):
            with self.assertRaises(ValueError): compare(x, 0, 45)


if __name__ == "__main__":
    unittest.main()
