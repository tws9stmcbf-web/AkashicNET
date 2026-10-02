"""Validate the larger fetch tranche against the pinned archive, not URL slugs."""
import json
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.search_reddit import load_records

class FetchBatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.batch = json.loads((ROOT / 'references/community/n2n-metadata-fetch-batch-0006.json').read_text())
        cls.archive = {r['post_id']: r for r in load_records()}

    def test_deterministic_selection_and_exact_count(self):
        excluded = {k for k, r in self.archive.items() if r['metadata']}
        for path in (ROOT / 'references/community').glob('n2n-web-metadata-pilot-*.json'):
            prior = json.loads(path.read_text())
            excluded.update(r['post_id'] for r in prior['records'])
            excluded.update(r['post_id'] for r in prior.get('unresolved_fetches', []))
        expected = sorted(k for k in self.archive if k not in excluded)[:100]
        self.assertEqual([r['post_id'] for r in self.batch['records']], expected)
        self.assertEqual(len(set(expected)), 100)

    def test_urls_provenance_and_annotations_preserved(self):
        for r in self.batch['records']:
            source = self.archive[r['post_id']]
            self.assertEqual(r['archived_url'], source['Reddit URL'])
            self.assertEqual(r['source_locations'], source['source_locations'])
            self.assertEqual(r['historical_annotations'], source['historical_annotations'])
            self.assertRegex(r['tool_reference'], r'^turn[0-9]+view[0-9]+$')
            self.assertEqual(r['retrieved_on'], '2026-10-02')

    def test_no_metadata_inferred_from_failures(self):
        self.assertEqual(self.batch['counts'], {
            'selected': 100, 'attempted': 100, 'metadata_observed': 0, 'fetch_failed': 100,
            'new_field_values': 0, 'cumulative_observed_records': 22,
            'cumulative_observed_field_values': 66, 'canonical_curated_records': 3})
        for r in self.batch['records']:
            self.assertEqual(r['status'], 'FETCH_FAILED')
            self.assertEqual(r['error'], 'DisabledError')
            self.assertEqual(r['observed_metadata'], {})
            for field in ('current_flair', 'authorship_verified', 'rights_status', 'evidence_status'):
                self.assertIsNone(r[field])
            self.assertNotIn('title', r)
            self.assertNotIn('body', r)
            self.assertNotIn('comments', r)
            self.assertNotIn('media', r)

if __name__ == '__main__':
    unittest.main()
