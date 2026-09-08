import json
import tempfile
import unittest
from pathlib import Path

from scripts.reddit_crawler import (
    RedditAPIError,
    canonical_post_url,
    fetch_post,
    is_post_removed,
    load_seen_ids,
    normalize_post,
    normalize_post_id,
    normalize_post_v2,
    read_checkpoint,
    reconcile_post,
    reconcile_records,
    tombstone_record,
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


class RedditMinimizedSchemaV2Tests(unittest.TestCase):
    _SAMPLE_CHILD = {
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

    def test_v1_schema_is_untouched_by_v2_addition(self):
        record = normalize_post(self._SAMPLE_CHILD, '2026-08-29T06:00:00Z')
        self.assertEqual(record['schema_version'], 'akashicnet.reddit.post.v1')
        self.assertIn('score', record)
        self.assertIn('num_comments', record)
        self.assertIn('upvote_ratio', record)

    def test_v2_schema_excludes_engagement_fields(self):
        record = normalize_post_v2(self._SAMPLE_CHILD, '2026-08-29T06:00:00Z')
        self.assertEqual(record['schema_version'], 'akashicnet.reddit.post.v2')
        for field in ('score', 'num_comments', 'upvote_ratio', 'stickied', 'locked', 'is_self'):
            self.assertNotIn(field, record)

    def test_v2_schema_excludes_body_comments_and_usernames(self):
        record = normalize_post_v2(self._SAMPLE_CHILD, '2026-08-29T06:00:00Z')
        self.assertNotIn('author', record)
        self.assertNotIn('selftext', record)
        self.assertNotIn('comments', record)

    def test_v2_schema_retains_justified_fields(self):
        record = normalize_post_v2(self._SAMPLE_CHILD, '2026-08-29T06:00:00Z')
        self.assertEqual(record['reddit_id'], 'abc123')
        self.assertEqual(record['canonical_url'], 'https://www.reddit.com/r/NeuronsToNirvana/comments/abc123/example/')
        self.assertEqual(record['created_utc'], 123.0)
        self.assertIn('over_18', record)
        self.assertTrue(record['provenance']['metadata_only'])


class RedditDeletionReconciliationTests(unittest.TestCase):
    def test_is_post_removed_detects_markers(self):
        self.assertTrue(is_post_removed(None))
        self.assertTrue(is_post_removed({'title': '[deleted]'}))
        self.assertTrue(is_post_removed({'title': '[removed]'}))
        self.assertTrue(is_post_removed({'removed_by_category': 'moderator'}))
        self.assertTrue(is_post_removed({'is_self': True, 'selftext': '[removed]'}))
        self.assertFalse(is_post_removed({'title': 'Still here'}))

    def test_tombstone_record_has_only_minimal_non_content_fields(self):
        record = tombstone_record('abc123', '2026-09-01T00:00:00Z', status='removed')
        self.assertEqual(
            set(record.keys()),
            {'schema_version', 'record_type', 'reddit_id', 'status', 'checked_at'},
        )
        self.assertEqual(record['record_type'], 'post_metadata_removed')
        self.assertEqual(record['status'], 'removed')

    def test_reconcile_post_tombstones_removed_post(self):
        class RemovedClient:
            def get_json(self, path, params=None):
                return {
                    'data': {
                        'children': [{
                            'data': {
                                'id': 'abc123',
                                'title': '[removed]',
                                'removed_by_category': 'moderator',
                            }
                        }]
                    }
                }, {}

        record = reconcile_post(RemovedClient(), 'abc123')
        self.assertEqual(record['record_type'], 'post_metadata_removed')
        self.assertEqual(record['status'], 'removed')
        self.assertNotIn('title', record)
        self.assertNotIn('canonical_url', record)

    def test_reconcile_post_tombstones_unavailable_post(self):
        class MissingClient:
            def get_json(self, path, params=None):
                return {'data': {'children': []}}, {}

        record = reconcile_post(MissingClient(), 'abc123')
        self.assertEqual(record['status'], 'unavailable')
        self.assertEqual(record['reddit_id'], 'abc123')

    def test_reconcile_post_refreshes_present_post_as_v2(self):
        class PresentClient:
            def get_json(self, path, params=None):
                return {
                    'data': {
                        'children': [{
                            'data': {
                                'id': 'abc123',
                                'title': 'Still here',
                                'permalink': '/r/NeuronsToNirvana/comments/abc123/example/',
                            }
                        }]
                    }
                }, {}

        record = reconcile_post(PresentClient(), 'abc123')
        self.assertEqual(record['schema_version'], 'akashicnet.reddit.post.v2')
        self.assertEqual(record['title'], 'Still here')

    def test_reconcile_records_removes_content_only_for_deleted_entries(self):
        class MixedClient:
            def get_json(self, path, params=None):
                post_id = params['id'].split('_', 1)[1]
                if post_id == 'gone1':
                    return {'data': {'children': []}}, {}
                return {
                    'data': {
                        'children': [{
                            'data': {'id': post_id, 'title': 'Still here'}
                        }]
                    }
                }, {}

        cached = [
            {'reddit_id': 'gone1', 'title': 'Old cached title'},
            {'reddit_id': 'live1', 'title': 'Old cached title'},
        ]
        reconciled = reconcile_records(MixedClient(), cached)
        by_id = {record['reddit_id']: record for record in reconciled}
        self.assertEqual(by_id['gone1']['record_type'], 'post_metadata_removed')
        self.assertNotIn('title', by_id['gone1'])
        self.assertEqual(by_id['live1']['title'], 'Still here')

    def test_reconcile_records_passes_through_existing_tombstones(self):
        cached = [{'reddit_id': 'gone1', 'record_type': 'post_metadata_removed', 'status': 'removed'}]

        class UnusedClient:
            def get_json(self, path, params=None):
                raise AssertionError('should not be called for existing tombstones')

        reconciled = reconcile_records(UnusedClient(), cached)
        self.assertEqual(reconciled, cached)


if __name__ == '__main__':
    unittest.main()
