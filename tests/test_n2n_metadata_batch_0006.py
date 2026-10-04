import copy
import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from tools.stage_n2n_metadata_batch import PINS, ROOT, build, encode, validate
from tools.search_reddit import load_records


class SixthBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sixth = build(batch_number=6)
        cls.batches = [json.loads((ROOT / f'references/community/n2n-metadata-batch-{n:04d}.json').read_text()) for n in range(1, 7)]

    def test_exact_selection_cumulative_counts_and_reproduction(self):
        self.assertEqual(encode(self.sixth), encode(self.batches[5]))
        ids = [r['post_id'] for b in self.batches for r in b['records']]
        self.assertEqual(len(ids), 6000)
        self.assertEqual(len(set(ids)), 6000)
        expected = sorted((r for r in load_records() if not r['metadata']),
                          key=lambda r: (not bool(r['historical_annotations']), r['post_id']))[5000:6000]
        self.assertEqual([r['post_id'] for r in self.sixth['records']], [r['post_id'] for r in expected])
        self.assertEqual(self.sixth['counts']['remaining_uncurated_outside_all_batches'], 1396)
        self.assertEqual(self.sixth['distribution']['selected_archive_row_references'], 1000)
        self.assertEqual(self.sixth['distribution']['selected_historical_annotation_values'], 0)
        self.assertEqual(self.sixth['boundaries'], self.batches[0]['boundaries'])

    def test_all_sixth_batch_provenance_matches_raw_csv(self):
        with (ROOT / 'references/community/reddit-uri-index.csv').open(newline='', encoding='utf-8-sig') as handle:
            raw = list(csv.reader(handle))
        for r in self.sixth['records']:
            for ref in r['archive_provenance']:
                self.assertEqual(raw[ref['csv_record_ordinal'] - 1][0], ref['raw_value'])
            self.assertTrue(all(r[f] is None for f in ('title', 'author', 'current_flair', 'evidence_status', 'rights_status')))
            self.assertEqual(r['metadata'], {})

    def test_prior_overlap_rejected(self):
        bad = copy.deepcopy(self.sixth)
        bad['records'][0] = self.batches[4]['records'][0]
        with self.assertRaises(ValueError):
            validate(bad, batch_number=6)

    def test_missing_fifth_batch_blocks_generation(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path in [*PINS, *(f'references/community/n2n-metadata-batch-{n:04d}.json' for n in (1, 2, 3, 4))]:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, root / path)
            with self.assertRaises(FileNotFoundError):
                build(root, 6)


if __name__ == '__main__':
    unittest.main()
