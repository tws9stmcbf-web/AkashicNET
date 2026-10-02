import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from tools.stage_n2n_metadata_batch import BATCH, PINS, ROOT, build, encode, validate
from tools.search_reddit import load_records


class MetadataBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batch = build()

    def test_checked_in_batch_reproduces(self):
        self.assertEqual((ROOT / BATCH).read_text(), encode(self.batch))
        self.assertEqual(encode(build()), encode(self.batch))

    def test_exact_selection_and_preserved_source_values(self):
        archive = load_records()
        expected = sorted((r for r in archive if not r['metadata']),
                          key=lambda r: (not bool(r['historical_annotations']), r['post_id']))[:1000]
        actual = self.batch['records']
        self.assertEqual([r['post_id'] for r in actual], [r['post_id'] for r in expected])
        self.assertEqual(len({r['post_id'] for r in actual}), 1000)
        self.assertEqual(sum(bool(r['historical_annotations']) for r in actual), 997)
        self.assertEqual(sum(len(r['archive_provenance']) for r in actual), 3033)
        for r, source in zip(actual, expected):
            self.assertEqual(r['source_locations'], source['source_locations'])
            self.assertEqual(r['historical_annotations'], source['historical_annotations'])
            self.assertEqual(r['archived_url'], source['Reddit URL'])
            for field in ('title', 'author', 'current_flair', 'rights_status', 'evidence_status'):
                self.assertIsNone(r[field])

    def test_rejects_inventions_and_provenance_damage(self):
        mutations = [
            lambda b: b['records'][0].update(title='Title inferred from slug'),
            lambda b: b['records'][0].update(current_flair='Original'),
            lambda b: b['records'][0].update(author='Assumed owner'),
            lambda b: b['records'][0].update(evidence_status='Established'),
            lambda b: b['records'][0].update(rights_status='Cleared'),
            lambda b: b['records'][0].update(body='Source text'),
            lambda b: b['records'][0]['archive_provenance'][0].update(csv_record_ordinal=1),
            lambda b: b['records'][0]['source_locations'].clear(),
            lambda b: b['records'].reverse(),
            lambda b: b['records'].__setitem__(1, b['records'][0]),
            lambda b: b['records'].pop(),
        ]
        for i, mutate in enumerate(mutations):
            with self.subTest(mutation=i):
                bad = copy.deepcopy(self.batch)
                mutate(bad)
                with self.assertRaises(ValueError):
                    validate(bad)

    def test_rejects_every_boundary_change(self):
        for key, value in self.batch['boundaries'].items():
            with self.subTest(boundary=key):
                bad = copy.deepcopy(self.batch)
                bad['boundaries'][key] = 'OPEN' if isinstance(value, str) else ['promoted']
                with self.assertRaises(ValueError):
                    validate(bad)

    def test_rejects_each_pinned_source_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path in PINS:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / path, root / path)
            for path in PINS:
                with self.subTest(source=path):
                    original = (root / path).read_bytes()
                    (root / path).write_bytes(original + b'\n')
                    with self.assertRaisesRegex(ValueError, 'pinned source drift'):
                        build(root)
                    (root / path).write_bytes(original)


if __name__ == '__main__':
    unittest.main()
