import copy
import json
import tempfile
import unittest
from pathlib import Path
from tools.build_n2n_provenance_pilot import ROOT, OUTPUT, build, validate, encode, output_path


class SecondProvenancePilotTests(unittest.TestCase):
    def test_reproduction_and_cumulative_nonoverlap(self):
        first = build()
        second = build(batch_number=2)
        self.assertEqual((ROOT / OUTPUT).read_text(), encode(first))
        self.assertEqual((ROOT / output_path(2)).read_text(), encode(second))
        ids = [r['post_id'] for b in (first, second) for r in b['records']]
        self.assertEqual(len(ids), 50)
        self.assertEqual(len(set(ids)), 50)
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(second['counts']['remaining_historical_feed_candidates'], 75)
        self.assertEqual(second['boundaries'], first['boundaries'])
        self.assertTrue(all(r['title'] is None and r['author'] is None for r in second['records']))

    def test_overlap_and_current_verification_rejected(self):
        first = build()
        second = build(batch_number=2)
        bad = copy.deepcopy(second)
        bad['records'][0] = first['records'][0]
        with self.assertRaises(ValueError):
            validate(bad, batch_number=2)
        second['records'][0]['current_verification'] = 'VERIFIED'
        with self.assertRaises(ValueError):
            validate(second, batch_number=2)

    def test_missing_previous_and_unreviewed_batch_rejected(self):
        with tempfile.TemporaryDirectory() as temp, self.assertRaises(FileNotFoundError):
            build(Path(temp), 2)
        for n in (0, 3, True, 1.0):
            with self.subTest(n=n), self.assertRaises(ValueError):
                build(batch_number=n)


if __name__ == '__main__':
    unittest.main()
