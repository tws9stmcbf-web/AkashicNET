import copy
import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from tools.stage_n2n_metadata_batch import PINS, ROOT, build, encode, validate
from tools.search_reddit import load_records


class FifthBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fifth = build(batch_number=5)
        cls.batches = [json.loads((ROOT / f'references/community/n2n-metadata-batch-{n:04d}.json').read_text()) for n in range(1, 6)]

    def test_exact_selection_cumulative_counts_and_reproduction(self):
        self.assertEqual(encode(self.fifth), encode(self.batches[4]))
        ids = [r['post_id'] for b in self.batches for r in b['records']]
        self.assertEqual(len(ids), 5000)
        self.assertEqual(len(set(ids)), 5000)
        expected = sorted((r for r in load_records() if not r['metadata']),
                          key=lambda r: (not bool(r['historical_annotations']), r['post_id']))[4000:5000]
        self.assertEqual([r['post_id'] for r in self.fifth['records']], [r['post_id'] for r in expected])
        self.assertEqual(self.fifth['counts']['remaining_uncurated_outside_all_batches'], 2396)
        self.assertEqual(self.fifth['distribution']['selected_archive_row_references'], 1000)
        self.assertEqual(self.fifth['distribution']['selected_historical_annotation_values'], 0)
        self.assertEqual(self.fifth['boundaries'], self.batches[0]['boundaries'])

    def test_all_fifth_batch_provenance_matches_raw_csv(self):
        with (ROOT / 'references/community/reddit-uri-index.csv').open(newline='', encoding='utf-8-sig') as handle:
            raw = list(csv.reader(handle))
        for r in self.fifth['records']:
            for ref in r['archive_provenance']:
                self.assertEqual(raw[ref['csv_record_ordinal'] - 1][0], ref['raw_value'])
            self.assertTrue(all(r[f] is None for f in ('title', 'author', 'current_flair', 'evidence_status', 'rights_status')))
            self.assertEqual(r['metadata'], {})

    def test_prior_overlap_rejected(self):
        bad = copy.deepcopy(self.fifth)
        bad['records'][0] = self.batches[3]['records'][0]
        with self.assertRaises(ValueError):
            validate(bad, batch_number=5)

    def test_missing_fourth_batch_blocks_generation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path in [*PINS, *(f'references/community/n2n-metadata-batch-{n:04d}.json' for n in (1, 2, 3))]:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, root / path)
            with self.assertRaises(FileNotFoundError):
                build(root, 5)


if __name__ == '__main__':
    unittest.main()
