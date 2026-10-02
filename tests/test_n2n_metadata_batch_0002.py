import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from tools.stage_n2n_metadata_batch import BATCH, PINS, ROOT, build, encode, validate
from tools.search_reddit import load_records


class SecondBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.first = build()
        cls.second = build(batch_number=2)

    def test_reproduction_and_exact_nonoverlap(self):
        actual = self.second['records']
        self.assertEqual((ROOT / 'references/community/n2n-metadata-batch-0002.json').read_text(), encode(self.second))
        expected = sorted((r for r in load_records() if not r['metadata']),
                          key=lambda r: (not bool(r['historical_annotations']), r['post_id']))[1000:2000]
        self.assertEqual([r['post_id'] for r in actual], [r['post_id'] for r in expected])
        a = {r['post_id'] for r in self.first['records']}
        b = {r['post_id'] for r in actual}
        self.assertEqual(len(a | b), 2000)
        self.assertFalse(a & b)
        self.assertEqual(sum(len(r['archive_provenance']) for r in actual), 1000)
        self.assertTrue(all(r['historical_annotations'] == [] for r in actual))
        self.assertEqual(self.second['counts']['remaining_uncurated_outside_all_batches'], 5396)
        self.assertEqual(self.second['boundaries'], self.first['boundaries'])

    def test_rejects_overlap_inventions_and_open_gate(self):
        mutations = [
            lambda b: b['records'].__setitem__(0, self.first['records'][0]),
            lambda b: b['records'][0].update(title='Inferred title'),
            lambda b: b['records'][0].update(current_flair='Research'),
            lambda b: b['records'][0].update(author='Assumed author'),
            lambda b: b['records'][0].update(rights_status='Cleared', evidence_status='Established'),
            lambda b: b['records'][0]['archive_provenance'][0].update(raw_value='invented'),
            lambda b: b['boundaries'].update(live_reddit_access='OPEN'),
            lambda b: b['counts'].update(cumulative_staged_unique=3000),
            lambda b: b['previous_batch'].update(sha256='wrong'),
        ]
        for index, mutate in enumerate(mutations):
            with self.subTest(mutation=index):
                bad = copy.deepcopy(self.second)
                mutate(bad)
                with self.assertRaises(ValueError):
                    validate(bad, batch_number=2)

    def test_previous_batch_required_and_validated(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path in PINS:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, root / path)
            with self.assertRaises(FileNotFoundError):
                build(root, 2)
            damaged = copy.deepcopy(self.first)
            damaged['records'].pop()
            (root / BATCH).write_text(encode(damaged))
            with self.assertRaises(ValueError):
                build(root, 2)

    def test_batch_one_unchanged_and_unreviewed_batches_rejected(self):
        self.assertEqual((ROOT / BATCH).read_text(), encode(self.first))
        for number in (0, 7, -1, True, 1.0):
            with self.subTest(number=number), self.assertRaises(ValueError):
                build(batch_number=number)


if __name__ == '__main__':
    unittest.main()
