import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path
from tools.stage_n2n_metadata_batch import ROOT, build, encode, validate
from tools.search_reddit import load_records


class FinalBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batches = [json.loads((ROOT / f'references/community/n2n-metadata-batch-{n:04d}.json').read_text()) for n in range(1, 9)]

    def test_full_queue_plus_curated_exactly_covers_archive(self):
        archive = load_records()
        queued = [r['post_id'] for b in self.batches for r in b['records']]
        curated = {r['post_id'] for r in archive if r['metadata']}
        self.assertEqual(len(queued), 7396)
        self.assertEqual(len(set(queued)), 7396)
        self.assertFalse(set(queued) & curated)
        self.assertEqual(set(queued) | curated, {r['post_id'] for r in archive})
        ordered = sorted((r for r in archive if not r['metadata']), key=lambda r: (not bool(r['historical_annotations']), r['post_id']))
        self.assertEqual([r['post_id'] for r in self.batches[-1]['records']], [r['post_id'] for r in ordered[7000:]])
        self.assertEqual(len(self.batches[-1]['records']), 396)
        self.assertEqual(self.batches[-1]['counts']['remaining_uncurated_outside_all_batches'], 0)
        self.assertEqual(self.batches[-1]['boundaries'], self.batches[0]['boundaries'])

    def test_final_batch_reproduces_and_revalidates_prior_chain(self):
        self.assertEqual(encode(build(batch_number=8)), encode(self.batches[-1]))

    def test_all_final_rows_retain_original_provenance_and_null_fields(self):
        with (ROOT / 'references/community/reddit-uri-index.csv').open(newline='', encoding='utf-8-sig') as f:
            raw = list(csv.reader(f))
        self.assertEqual(sum(len(r['archive_provenance']) for r in self.batches[-1]['records']), 396)
        for r in self.batches[-1]['records']:
            for ref in r['archive_provenance']:
                self.assertEqual(ref['raw_value'], raw[ref['csv_record_ordinal'] - 1][0])
            self.assertTrue(all(r[field] is None for field in ('title', 'author', 'current_flair', 'evidence_status', 'rights_status')))
            self.assertEqual(r['metadata'], {})

    def test_missing_prior_and_unreviewed_batches_rejected(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(FileNotFoundError):
            build(Path(tmp), 8)
        for n in (0, 9, True, 8.0):
            with self.subTest(n=n), self.assertRaises(ValueError):
                build(batch_number=n)

    def test_prior_overlap_rejected(self):
        bad = copy.deepcopy(self.batches[-1])
        bad['records'][0] = self.batches[6]['records'][0]
        with self.assertRaises(ValueError):
            validate(bad, batch_number=8)


if __name__ == '__main__':
    unittest.main()
