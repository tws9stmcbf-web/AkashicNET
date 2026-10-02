import csv
import hashlib
import io
import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.import_n2n_metadata_snapshot import candidates, COLUMNS, HEAD
from tools.n2n_access_gate import decision


def fixture(rows=None, columns=COLUMNS):
    handle = io.StringIO(newline='')
    writer = csv.writer(handle)
    writer.writerow(columns)
    writer.writerows(rows or [['10a8yeh', 'https://www.reddit.com/r/NeuronsToNirvana/comments/10a8yeh/', 'Source-supplied test title', '', '', '', '']])
    snapshot = handle.getvalue().encode()
    receipt = {'schema': 'akashicnet.n2n.snapshot-receipt.v1', 'source_head': HEAD,
               'snapshot_sha256': hashlib.sha256(snapshot).hexdigest(),
               'captured_at': '2026-10-02T04:40:00Z', 'source_description': 'Test fixture only; no real metadata assertion',
               'acquisition_method': 'saved_metadata_snapshot'}
    return snapshot, receipt


class MetadataImportTests(unittest.TestCase):
    def test_preserves_missing_fields_and_unverified_status(self):
        out = candidates(*fixture())
        self.assertEqual(out['counts']['candidate_records'], 1)
        self.assertEqual(out['counts']['candidate_field_values'], 1)
        record = out['records'][0]
        self.assertEqual(set(record['candidate_metadata']), {'title'})
        self.assertEqual(record['review_status'], 'UNREVIEWED_SOURCE_ASSERTION')
        self.assertIsNone(record['current_flair'])
        self.assertIsNone(record['rights_status'])
        self.assertIsNone(record['evidence_status'])
        self.assertFalse(out['boundaries']['canonical_metadata_write'])

    def test_rejects_tampering_extra_body_columns_and_duplicates(self):
        raw, receipt = fixture()
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            candidates(raw + b'\n', receipt)
        with self.assertRaisesRegex(ValueError, 'columns'):
            candidates(*fixture(columns=COLUMNS + ['body']))
        row = ['10a8yeh', 'https://www.reddit.com/r/NeuronsToNirvana/comments/10a8yeh/', 'Fixture', '', '', '', '']
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            candidates(*fixture([row, row]))

    def test_rejects_wrong_post_and_future_creation_time(self):
        row = ['10a8yeh', 'https://www.reddit.com/r/NeuronsToNirvana/comments/otherid/', 'Fixture', '', '', '', '']
        with self.assertRaisesRegex(ValueError, 'does not identify'):
            candidates(*fixture([row]))
        row[1] = 'https://www.reddit.com/r/NeuronsToNirvana/comments/10a8yeh/'
        row[3] = '2026-10-03T00:00:00Z'
        with self.assertRaisesRegex(ValueError, 'after capture'):
            candidates(*fixture([row]))

    def test_enforces_bounded_limit(self):
        for limit in [0, 1001, True]:
            with self.assertRaises(ValueError):
                candidates(*fixture(), limit=limit)
        rows = [[id, f'https://www.reddit.com/r/NeuronsToNirvana/comments/{id}/', 'Fixture', '', '', '', ''] for id in ['100080', '100081']]
        with self.assertRaisesRegex(ValueError, 'exceeds'):
            candidates(*fixture(rows), limit=1)

    def test_accepts_exactly_1000_and_rejects_1001(self):
        from tools.search_reddit import load_records
        eligible = [r for r in load_records() if not r['metadata']][:1001]
        rows = [[r['post_id'], r['Reddit URL'], 'Fixture title only', '', '', '', ''] for r in eligible]
        out = candidates(*fixture(rows[:1000]))
        self.assertEqual(out['counts']['candidate_records'], 1000)
        self.assertEqual(out['counts']['candidate_field_values'], 1000)
        self.assertEqual(out['counts']['new_verified_records'], 0)
        with self.assertRaisesRegex(ValueError, 'exceeds'):
            candidates(*fixture(rows))

    def test_cached_control_does_not_override_disabled_new_urls(self):
        self.assertEqual(decision([{'role': 'control', 'status': 'READABLE_RETURNED_COPY'}, {'role': 'unread', 'error': 'DisabledError'}])['action'], 'STOP_WEB_READER')

    def test_429_and_denied_access_stop_without_automatic_retry(self):
        self.assertEqual(decision([{'http_status': 429}])['reason'], 'RATE_LIMIT_429')
        self.assertEqual(decision([{'http_status': 403}])['action'], 'STOP_WEB_READER')
        self.assertEqual(decision([{'status': 'READABLE_RETURNED_COPY'}])['max_requests'], 5)


if __name__ == '__main__':
    unittest.main()
