import copy
import csv
import json
import unittest
from tools.build_n2n_provenance_pilot import ROOT, FEEDS, build, encode, output_path, validate

class ProvenanceCompletionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.value = build(batch_number=3)

    def test_exact_coverage_and_unchanged_pilots(self):
        values = [build(batch_number=n) for n in (1, 2)] + [self.value]
        for n, value in enumerate(values, 1):
            self.assertEqual((ROOT / output_path(n)).read_text(), encode(value))
        ids = [r['post_id'] for v in values for r in v['records']]
        expected = set()
        for path in FEEDS:
            with (ROOT / path).open(newline='', encoding='utf-8-sig') as handle:
                expected.update(r['reddit_post_id'] for r in csv.DictReader(handle) if r['subreddit'].casefold() == 'neuronstonirvana')
        self.assertEqual([len(v['records']) for v in values], [25,25,75])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(set(ids), expected)
        self.assertEqual(len(expected),125)
        self.assertEqual(ids, sorted(ids))

    def test_receipt_fidelity_and_queue_membership(self):
        queue = {r['post_id']: r for n in range(1,9) for r in json.loads((ROOT / f'references/community/n2n-metadata-batch-{n:04d}.json').read_text())['records']}
        for row in self.value['records']:
            self.assertEqual(row['archived_url'], queue[row['post_id']]['archived_url'])
            for receipt in row['historical_observation_receipts']:
                with (ROOT / receipt['source_path']).open(newline='', encoding='utf-8-sig') as handle:
                    raw = list(csv.DictReader(handle))[receipt['csv_record_ordinal']-2]
                self.assertEqual(receipt['historical_observation'],raw)
                self.assertEqual(raw['reddit_post_id'],row['post_id'])
            for field in ('title','author','current_flair','evidence_status','rights_status'):
                self.assertIsNone(row[field])
            self.assertEqual(row['current_verification'],'NOT_PERFORMED')
            self.assertFalse(row['canonical_metadata_write'])

    def test_promotion_overlap_and_omission_rejected(self):
        for mutation in ('title','boundary','overlap','omission'):
            bad = copy.deepcopy(self.value)
            if mutation == 'title': bad['records'][0]['title']='Invented'
            elif mutation == 'boundary': bad['boundaries']={}
            elif mutation == 'overlap': bad['records'][0]=build()['records'][0]
            else: bad['records'].pop()
            with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                validate(bad,batch_number=3)
