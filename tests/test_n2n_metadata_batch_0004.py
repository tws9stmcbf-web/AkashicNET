import copy
import shutil
import tempfile
import unittest
from pathlib import Path
from tools.stage_n2n_metadata_batch import PINS, ROOT, build, encode, validate
from tools.search_reddit import load_records


class FourthBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batches = [build(batch_number=n) for n in (1, 2, 3, 4)]

    def test_all_four_reproduce_without_overlap(self):
        ids = []
        for number, batch in enumerate(self.batches, 1):
            self.assertEqual((ROOT / f'references/community/n2n-metadata-batch-{number:04d}.json').read_text(), encode(batch))
            ids.extend(r['post_id'] for r in batch['records'])
        self.assertEqual(len(ids), 4000)
        self.assertEqual(len(set(ids)), 4000)
        expected = sorted((r for r in load_records() if not r['metadata']),
                          key=lambda r: (not bool(r['historical_annotations']), r['post_id']))[3000:4000]
        third = self.batches[3]
        self.assertEqual([r['post_id'] for r in third['records']], [r['post_id'] for r in expected])
        self.assertEqual(third['counts']['remaining_uncurated_outside_all_batches'], 3396)
        self.assertEqual(third['distribution']['selected_archive_row_references'], 1000)
        self.assertEqual(third['distribution']['selected_historical_annotation_values'], 0)
        for r in third['records']:
            self.assertEqual(r['metadata'], {})
            self.assertTrue(all(r[f] is None for f in ('title', 'author', 'current_flair', 'evidence_status', 'rights_status')))

    def test_overlap_with_either_previous_batch_and_gate_changes_rejected(self):
        for number in (0, 1, 2):
            bad = copy.deepcopy(self.batches[3])
            bad['records'][0] = self.batches[number]['records'][0]
            with self.subTest(prior=number + 1), self.assertRaises(ValueError):
                validate(bad, batch_number=4)
        bad = copy.deepcopy(self.batches[3])
        bad['boundaries']['publication_gate'] = 'OPEN'
        with self.assertRaises(ValueError):
            validate(bad, batch_number=4)

    def test_missing_or_changed_third_batch_blocks_fourth(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path in [*PINS, 'references/community/n2n-metadata-batch-0001.json', 'references/community/n2n-metadata-batch-0002.json']:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, root / path)
            with self.assertRaises(FileNotFoundError):
                build(root, 4)
            bad = copy.deepcopy(self.batches[2])
            bad['records'][0]['title'] = 'invented'
            (root / 'references/community/n2n-metadata-batch-0003.json').write_text(encode(bad))
            with self.assertRaises(ValueError):
                build(root, 4)


if __name__ == '__main__':
    unittest.main()
