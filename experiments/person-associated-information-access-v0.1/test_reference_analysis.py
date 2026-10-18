"""Scientific-computing checks on synthetic examples, never human trials."""
import copy
import itertools
import unittest
from reference_analysis import (
    analyze_synthetic, binomial_tail, planning, synthetic_fixture,
    validate_synthetic, score
)


class ReferenceChecks(unittest.TestCase):
    def setUp(self):
        self.data = synthetic_fixture()

    def test_tail_matches_exhaustive_four_symbol_assignments(self):
        # Independent finite enumeration, not another call to the same formula.
        targets = list(itertools.product(range(4), repeat=4))
        for k in range(6):
            expected = sum(sum(t == 0 for t in seq) >= k for seq in targets)/256
            self.assertAlmostEqual(binomial_tail(4, k), expected, places=14)

    def test_discrete_planning_boundary(self):
        p = planning()
        self.assertEqual(p["critical_hits"], 61)
        self.assertGreater(binomial_tail(192, 60), .025)
        self.assertLessEqual(binomial_tail(192, 61), .025)

    def test_equal_cluster_fixture_has_no_arm_difference(self):
        r = analyze_synthetic(self.data, permutation_draws=199, bootstrap_draws=199)
        self.assertEqual(r["h2"]["clusters"], 48)
        self.assertEqual(r["h2"]["p_value"], 1)
        self.assertEqual(r["h2"]["difference"], 0)
        self.assertEqual(r["h1"]["hits"], 48)
        self.assertEqual(r["participant_intervals"]["intervals"]["MT"], [.25, .25])
        for cell in r["cells"].values():
            self.assertEqual(cell["planned"], 192)

    def test_missing_and_wrong_answers_retain_denominator(self):
        row = self.data["trials"][0]
        row.update(status="timeout", choice=None)
        self.assertEqual(score(row), 0)
        r = analyze_synthetic(self.data, permutation_draws=19, bootstrap_draws=19)
        self.assertEqual(r["h1"]["n"], 192)
        self.assertEqual(r["h1"]["hits"], 47)
        self.assertEqual(r["cells"]["MT"]["zero_scored_statuses"], {"timeout": 1})
        self.assertEqual(r["cells"]["MT"]["missing_bounds"], [47/192, 48/192])

    def test_integrity_failure_never_scores_a_hit(self):
        row = self.data["trials"][0]
        self.assertEqual(row["choice"], row["target"])
        row["status"] = "integrity_failure"
        self.assertEqual(score(row), 0)

    def test_duplicate_missing_and_invalid_codes_rejected(self):
        for mutate in (
            lambda d: d["trials"].pop(),
            lambda d: d["trials"].__setitem__(1, copy.deepcopy(d["trials"][0])),
            lambda d: d["trials"][0].update(choice=[0, 1]),
            lambda d: d["trials"][0].update(choice=True),
            lambda d: d["trials"][0].update(target=4),
            lambda d: d["trials"][0].update(status="excluded_for_low_score"),
            lambda d: d["trials"][0].update(familiarity="U"),
            lambda d: d["trials"][0].update(person_id="F02"),
        ):
            d = copy.deepcopy(self.data)
            mutate(d)
            with self.assertRaises(ValueError):
                validate_synthetic(d)

    def test_early_open_or_late_commit_rejected(self):
        for fields in (
            {"target_opened_at": 0},
            {"target_committed_at": 2},
            {"response_locked_at": float("nan")},
        ):
            d = copy.deepcopy(self.data)
            d["trials"][0].update(fields)
            with self.assertRaises(ValueError):
                validate_synthetic(d)

    def test_real_data_and_imbalanced_allocation_rejected(self):
        d = copy.deepcopy(self.data)
        d["data_kind"] = "REAL"
        with self.assertRaises(ValueError):
            validate_synthetic(d)
        self.data["participants"][0]["arm"] = "R"
        with self.assertRaises(ValueError):
            validate_synthetic(self.data)

    def test_permutation_detects_extreme_synthetic_separation(self):
        for row in self.data["trials"]:
            row["choice"] = 0 if int(row["participant_id"][1:]) < 24 else 1
        r = analyze_synthetic(self.data, permutation_draws=999, bootstrap_draws=99)
        self.assertEqual(r["h2"]["difference"], 1)
        self.assertEqual(r["h2"]["p_value"], 1/1000)
        self.assertEqual(r["scientific_interpretation"], "NONE: synthetic software check only")


if __name__ == "__main__":
    unittest.main()

