import json
import tempfile
import unittest
from pathlib import Path

from scripts.reddit_crawler import (
    RedditAPIError,
    canonical_post_url,
    fetch_post,
    load_seen_ids,
    normalize_post,
    normalize_post_id,
    read_checkpoint,
    write_checkpoint,
)


class RedditCrawlerTests(unittest.TestCase):
    def test_canonical_post_url_strips_query_and_adds_slash(self):
        self.assertEqual(
            canonical_post_url('/r/NeuronsToNirvana/comments/abc123/example/?utm_source=test'),
            'https://www.reddit.com/r/NeuronsToNirvana/comments/abc123/example/',
        )

    def test_normalize_post_is_metadata_only(self):
        child = {
            'data': {
                'id': 'abc123',
                'name': 't3_abc123',
                'subreddit': 'NeuronsToNirvana',
                'title': 'Example title',
                'permalink': '/r/NeuronsToNirvana/comments/abc123/example/',
                'url': 'https://example.org/source',
                'created_utc': 123.0,
                'score': 47,
                'num_comments': 7,
                'upvote_ratio': 0.93,
                'over_18': False,
                'stickied': False,
                'locked': False,
                'is_self': False,
                'author': 'should_not_be_stored',
                'selftext': 'should_not_be_stored',
            }
        }
        record = normalize_post(child, '2026-08-29T06:00:00Z')
        self.assertEqual(record['reddit_id'], 'abc123')
        self.assertEqual(record['canonical_url'], 'https://www.reddit.com/r/NeuronsToNirvana/comments/abc123/example/')
        self.assertTrue(record['provenance']['metadata_only'])
        self.assertNotIn('author', record)
        self.assertNotIn('selftext', record)

    def test_normalize_post_id_accepts_fullname_prefix(self):
        self.assertEqual(normalize_post_id('t3_1UEPVP1'), '1uepvp1')
        with self.assertRaises(ValueError):
            normalize_post_id('not/a/post')

    def test_fetch_post_uses_exact_info_endpoint(self):
        class FakeClient:
            def get_json(self, path, params=None):
                self.path = path
                self.params = params
                return {
                    'data': {
                        'children': [{
                            'data': {
                                'id': '1uepvp1',
                                'name': 't3_1uepvp1',
                                'subreddit': 'NeuronsToNirvana',
                                'title': 'Storytelling as an epistemic tool',
                                'permalink': '/r/NeuronsToNirvana/comments/1uepvp1/storytelling_as_an_epistemic_tool/',
                            }
                        }]
                    }
                }, {}

        client = FakeClient()
        record = fetch_post(client, 't3_1UEPVP1')
        self.assertEqual(client.path, '/api/info')
        self.assertEqual(client.params['id'], 't3_1uepvp1')
        self.assertEqual(record['reddit_id'], '1uepvp1')
        self.assertEqual(record['provenance']['endpoint'], 'post_info')
        self.assertTrue(record['provenance']['metadata_only'])

    def test_fetch_post_keeps_absence_indeterminate(self):
        class EmptyClient:
            def get_json(self, path, params=None):
                return {'data': {'children': []}}, {}

        with self.assertRaisesRegex(RedditAPIError, 'availability remains indeterminate'):
            fetch_post(EmptyClient(), '1uepvp1')

    def test_seen_ids_and_checkpoint_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            output = root / 'posts.jsonl'
            output.write_text(
                json.dumps({'reddit_id': 'a'}) + '\n' +
                'not-json\n' +
                json.dumps({'reddit_id': 'b'}) + '\n',
                encoding='utf-8',
            )
            self.assertEqual(load_seen_ids(output), {'a', 'b'})

            checkpoint = root / 'checkpoint.json'
            write_checkpoint(checkpoint, subreddit='NeuronsToNirvana', after='t3_xyz')
            data = read_checkpoint(checkpoint)
            self.assertEqual(data['subreddit'], 'NeuronsToNirvana')
            self.assertEqual(data['after'], 't3_xyz')
            self.assertIn('updated_at', data)


if __name__ == '__main__':
    unittest.main()
