import csv
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from tools.search_reddit import load_records, main, search


class ArchiveSearchTests(unittest.TestCase):
    def run_cli(self, records, *args):
        output = io.StringIO()
        with patch('tools.search_reddit.load_records', return_value=records), \
                patch('sys.argv', ['search_reddit.py', *args]), redirect_stdout(output):
            main()
        return output.getvalue()

    def test_text_explains_annotation_match_without_inventing_metadata(self):
        record = {
            'post_id': 'abc', 'Reddit URL': 'https://www.reddit.com/r/NeuronsToNirvana/comments/abc/',
            'source_locations': [], 'historical_annotations': ['HOMESENSE,What'],
            'metadata': {}, 'record_kind': 'ARCHIVED_URL_ONLY',
            'claim_review': 'NOT_ASSESSED_BY_THIS_TOOL',
        }
        output = self.run_cli([record], ' homesense ')
        self.assertIn('1 matches', output)
        self.assertIn('HISTORICAL ANNOTATION (not current flair): HOMESENSE,What', output)
        self.assertIn('TITLE: [Title not captured]', output)
        self.assertNotIn('CURATED ', output)
        self.assertNotIn('HISTORICAL ANNOTATION', self.run_cli([record], 'HOMESENSE', '-n', '0'))
        result = json.loads(self.run_cli([record], 'HOMESENSE', '--json'))
        self.assertEqual(result['records'], [record])

    def test_text_explains_each_curated_field_match(self):
        metadata = {
            'title': 'Known title', 'topic': 'Unique topic', 'category': 'Unique category',
            'author': 'Captured author', 'related Toolkit framework': 'Framework label',
            'short summary': 'Summary text', 'external source URL': 'https://example.org/source',
            'date': '', 'post type': None,
        }
        record = {
            'post_id': 'abc', 'Reddit URL': 'https://www.reddit.com/r/NeuronsToNirvana/comments/abc/',
            'source_locations': [], 'historical_annotations': [], 'metadata': metadata,
            'record_kind': 'ARCHIVED_URL_WITH_CURATED_METADATA',
        }
        for field, value in metadata.items():
            if field == 'title' or not value:
                continue
            with self.subTest(field=field):
                output = self.run_cli([record], value.upper())
                self.assertIn('1 matches', output)
                self.assertIn(f'CURATED {field}: {value}', output)
                self.assertNotIn('CURATED date:', output)
                self.assertNotIn('CURATED post type:', output)
                self.assertNotIn('HISTORICAL ANNOTATION', output)

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
