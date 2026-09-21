import csv
import tempfile
import unittest
from pathlib import Path
from tools.search_reddit import load_records, search


class ArchiveSearchTests(unittest.TestCase):
    def test_full_archive_coverage(self):
        records = load_records()
        self.assertEqual(len(records), 7399)
        self.assertEqual(len({r['post_id'] for r in records}), 7399)
        self.assertEqual(sum(bool(r['metadata']) for r in records), 3)
        self.assertEqual(len(search(records, '')), 7399)
        self.assertTrue(search(records, 'HOMESENSE'))

    def test_annotations_deduplicate_and_metadata_enriches(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            uri = root / 'urls.csv'
            with uri.open('w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['reddit_url'])
                writer.writerows([[u] for u in [
                    'https://reddit.com/r/NeuronsToNirvana/comments/abc/example/',
                    'https://reddit.com/r/NeuronsToNirvana/comments/abc/example/,HIERATIC,What',
                    'https://reddit.com/r/Other/comments/def/other/',
                    'https://example.com/r/NeuronsToNirvana/comments/ghi/no/',
                    'https://reddit.com/r/NeuronsToNirvana/',
                ]])
            metadata = root / 'metadata.csv'
            with metadata.open('w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Reddit URL', 'title'])
                writer.writerow(['https://reddit.com/r/NeuronsToNirvana/comments/abc/new_slug/', 'Known title'])
            records = load_records(uri, metadata)
        self.assertEqual(len(records), 1)
        self.assertEqual(len(search(records, 'hieratic')), 1)
        self.assertEqual(len(search(records, 'known title')), 1)
        self.assertEqual(records[0]['claim_review'], 'NOT_ASSESSED_BY_THIS_TOOL')


if __name__ == '__main__':
    unittest.main()
