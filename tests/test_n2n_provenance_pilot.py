import copy
import csv
import json
import tempfile
import unittest
from pathlib import Path
from tools.build_n2n_provenance_pilot import ROOT, PINS, OUTPUT, build, validate, encode


class ProvenancePilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pilot = build()

    def test_reproduction_counts_and_every_receipt(self):
        self.assertEqual((ROOT / OUTPUT).read_text(), encode(self.pilot))
        self.assertEqual(len({r['post_id'] for r in self.pilot['records']}), 25)
        for record in self.pilot['records']:
            for receipt in record['historical_observation_receipts']:
                with (ROOT / receipt['source_path']).open(newline='') as handle:
                    rows = list(csv.DictReader(handle))
                self.assertEqual(receipt['historical_observation'], rows[receipt['csv_record_ordinal'] - 2])
                self.assertEqual(receipt['historical_observation']['reddit_post_id'], record['post_id'])
                self.assertEqual(receipt['historical_observation']['observed_at'], '2026-09-01')
            self.assertIsNone(record['title'])
            self.assertIsNone(record['author'])
            self.assertFalse(record['canonical_metadata_write'])
        self.assertEqual(self.pilot['counts']['selected_staging_overlap'], 0)

    def test_inventions_temporal_promotion_and_gate_mutations_rejected(self):
        mutations = [
            lambda x: x['records'][0].update(title='Unverified pilot title'),
            lambda x: x['records'][0].update(current_verification='PUBLIC_VERIFIED'),
            lambda x: x['records'][0]['historical_observation_receipts'][0]['historical_observation'].update(observed_at='2026-10-02'),
            lambda x: x['records'][0].update(canonical_metadata_write=True),
            lambda x: x['boundaries'].update(rights_gate='OPEN'),
            lambda x: x['counts'].update(curated_unchanged=28),
        ]
        for i, mutate in enumerate(mutations):
            with self.subTest(mutation=i):
                bad = copy.deepcopy(self.pilot)
                mutate(bad)
                with self.assertRaises(ValueError):
                    validate(bad)

    def test_each_new_pinned_source_drift_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path in PINS:
                (root / path).parent.mkdir(parents=True, exist_ok=True)
                (root / path).write_bytes((ROOT / path).read_bytes())
            for path in PINS:
                original = (root / path).read_bytes()
                (root / path).write_bytes(original + b'\n')
                with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'pinned input drift'):
                    build(root)
                (root / path).write_bytes(original)


if __name__ == '__main__':
    unittest.main()
