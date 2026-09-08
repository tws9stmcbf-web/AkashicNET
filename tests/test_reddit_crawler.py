import json
import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.reddit_crawler import (
    RedditAPIError,
    canonical_post_url,
    crawl_post,
    fetch_post,
    is_post_removed,
    iter_subreddit_posts,
    load_seen_ids,
    main,
    normalize_post,
    normalize_post_id,
    normalize_post_v2,
    read_checkpoint,
    reconcile_file,
    reconcile_post,
    reconcile_records,
    replace_exact_post_record,
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
        self.assertEqual(record['schema_version'], 'akashicnet.reddit.post.v2')
        self.assertEqual(record['provenance']['endpoint'], 'post_info')
        self.assertTrue(record['provenance']['metadata_only'])
        self.assertNotIn('score', record)
        self.assertNotIn('num_comments', record)
        self.assertNotIn('upvote_ratio', record)

    def test_fetch_post_tombstones_removed_post_immediately(self):
        class RemovedClient:
            def get_json(self, path, params=None):
                return {
                    'data': {
                        'children': [{
                            'data': {
                                'id': 'abc123',
                                'title': '[removed]',
                                'removed_by_category': 'moderator',
                                'permalink': '/r/NeuronsToNirvana/comments/abc123/removed/',
                            }
                        }]
                    }
                }, {}

        record = fetch_post(RemovedClient(), 'abc123')
        self.assertEqual(record['record_type'], 'post_metadata_removed')
        self.assertEqual(record['status'], 'removed')
        self.assertEqual(record['provenance']['endpoint'], 'post_info')
        for field in ('title', 'canonical_url', 'external_url', 'subreddit', 'created_utc', 'retrieved_at'):
            self.assertNotIn(field, record)

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

    def test_iter_subreddit_posts_emits_v2_without_engagement_fields(self):
        class ListingClient:
            def get_json(self, path, params=None):
                return {
                    'data': {
                        'children': [{
                            'data': {
                                'id': 'abc123',
                                'title': 'Example title',
                                'permalink': '/r/NeuronsToNirvana/comments/abc123/example/',
                                'score': 47,
                                'num_comments': 7,
                                'upvote_ratio': 0.93,
                                'author': 'should_not_be_stored',
                                'selftext': 'should_not_be_stored',
                            }
                        }],
                        'after': None,
                    }
                }, {}

        records = [record for record, _ in iter_subreddit_posts(ListingClient(), 'NeuronsToNirvana', max_posts=1)]
        self.assertEqual(len(records), 1)
        record = records[0]
        self.assertEqual(record['schema_version'], 'akashicnet.reddit.post.v2')
        for field in ('score', 'num_comments', 'upvote_ratio', 'author', 'selftext'):
            self.assertNotIn(field, record)

    def test_iter_subreddit_posts_tombstones_removed_children_immediately(self):
        class MixedListingClient:
            def get_json(self, path, params=None):
                return {
                    'data': {
                        'children': [
                            {
                                'data': {
                                    'id': 'gone1',
                                    'title': '[removed]',
                                    'removed_by_category': 'moderator',
                                    'permalink': '/r/NeuronsToNirvana/comments/gone1/was_here/',
                                }
                            },
                            {
                                'data': {
                                    'id': 'live1',
                                    'title': 'Still here',
                                    'permalink': '/r/NeuronsToNirvana/comments/live1/still_here/',
                                    'score': 12,
                                }
                            },
                        ],
                        'after': None,
                    }
                }, {}

        records = [record for record, _ in iter_subreddit_posts(MixedListingClient(), 'NeuronsToNirvana', max_posts=2)]
        self.assertEqual(len(records), 2)
        by_id = {record['reddit_id']: record for record in records}

        removed = by_id['gone1']
        self.assertEqual(removed['record_type'], 'post_metadata_removed')
        self.assertEqual(removed['status'], 'removed')
        self.assertEqual(removed['provenance']['endpoint'], 'subreddit_listing')
        for content_field in ('title', 'canonical_url', 'external_url', 'subreddit', 'created_utc', 'score'):
            self.assertNotIn(content_field, removed)

        live = by_id['live1']
        self.assertEqual(live['schema_version'], 'akashicnet.reddit.post.v2')
        self.assertEqual(live['title'], 'Still here')
        self.assertNotIn('score', live)


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
            {'schema_version', 'source', 'record_type', 'reddit_id', 'status', 'checked_at', 'provenance'},
        )
        self.assertEqual(record['record_type'], 'post_metadata_removed')
        self.assertEqual(record['status'], 'removed')
        self.assertEqual(record['source'], 'reddit')
        self.assertTrue(record['provenance']['metadata_only'])
        for content_field in ('title', 'canonical_url', 'external_url', 'subreddit', 'created_utc', 'retrieved_at'):
            self.assertNotIn(content_field, record)

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

    def test_reconcile_post_honors_rate_limit_headers(self):
        class LimitedClient:
            def get_json(self, path, params=None):
                return {
                    'data': {
                        'children': [{'data': {'id': 'abc123', 'title': 'Still here'}}]
                    }
                }, {'x-ratelimit-remaining': '0', 'x-ratelimit-reset': '2'}

        with patch('scripts.reddit_crawler.time.sleep') as sleep:
            record = reconcile_post(LimitedClient(), 'abc123')

        self.assertEqual(record['record_type'], 'post_metadata')
        sleep.assert_called_once_with(3.0)

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

    def test_reconcile_records_retries_unavailable_tombstones(self):
        class NowLiveClient:
            def get_json(self, path, params=None):
                return {
                    'data': {
                        'children': [{
                            'data': {'id': 'wasgone', 'title': 'Back again'}
                        }]
                    }
                }, {}

        cached = [{
            'reddit_id': 'wasgone',
            'record_type': 'post_metadata_removed',
            'status': 'unavailable',
            'checked_at': '2026-09-01T00:00:00Z',
        }]
        reconciled = reconcile_records(NowLiveClient(), cached)
        self.assertEqual(reconciled[0]['schema_version'], 'akashicnet.reddit.post.v2')
        self.assertEqual(reconciled[0]['title'], 'Back again')

    def test_reconcile_records_does_not_retry_confirmed_removed(self):
        class ShouldNotBeCalledClient:
            def get_json(self, path, params=None):
                raise AssertionError('confirmed removed tombstones must not be retried')

        cached = [{
            'reddit_id': 'gone_forever',
            'record_type': 'post_metadata_removed',
            'status': 'removed',
            'checked_at': '2026-09-01T00:00:00Z',
        }]
        reconciled = reconcile_records(ShouldNotBeCalledClient(), cached)
        self.assertEqual(reconciled, cached)


class RedditApprovalGateTests(unittest.TestCase):
    def _run_main_without_network(self, env, argv=('NeuronsToNirvana',)):
        with patch.dict(os.environ, env, clear=True):
            return main(list(argv))

    def test_unset_approval_blocks_before_credentials(self):
        rc = self._run_main_without_network({})
        self.assertEqual(rc, 3)

    def test_false_approval_blocks(self):
        rc = self._run_main_without_network({'REDDIT_API_APPROVED': 'false'})
        self.assertEqual(rc, 3)

    def test_mixed_case_approval_blocks(self):
        for value in ('True', 'TRUE', 'tRuE', ' true', 'true '):
            with self.subTest(value=value):
                rc = self._run_main_without_network({'REDDIT_API_APPROVED': value})
                self.assertEqual(rc, 3)

    def test_approval_even_with_credentials_present_does_not_bypass_gate(self):
        rc = self._run_main_without_network({
            'REDDIT_API_APPROVED': 'false',
            'REDDIT_CLIENT_ID': 'id',
            'REDDIT_CLIENT_SECRET': 'secret',
        })
        self.assertEqual(rc, 3)

    def test_exact_true_passes_gate_and_reaches_credential_check(self):
        # No REDDIT_CLIENT_ID/SECRET set, so this proves the gate let
        # execution proceed (rc=2 for missing credentials) without ever
        # attempting a network call.
        rc = self._run_main_without_network({'REDDIT_API_APPROVED': 'true'})
        self.assertEqual(rc, 2)


class RedditReconcileFileTests(unittest.TestCase):
    def test_reconcile_file_atomically_rewrites_on_success(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / 'posts.jsonl'
            path.write_text(
                json.dumps({'reddit_id': 'gone1', 'title': 'Old cached title'}) + '\n' +
                json.dumps({'reddit_id': 'live1', 'title': 'Old cached title'}) + '\n',
                encoding='utf-8',
            )

            class MixedClient:
                def get_json(self, path, params=None):
                    post_id = params['id'].split('_', 1)[1]
                    if post_id == 'gone1':
                        return {'data': {'children': []}}, {}
                    return {
                        'data': {'children': [{'data': {'id': post_id, 'title': 'Refreshed title'}}]}
                    }, {}

            total, changed = reconcile_file(MixedClient(), path)
            self.assertEqual(total, 2)
            self.assertEqual(changed, 1)

            lines = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
            by_id = {record['reddit_id']: record for record in lines}
            self.assertEqual(by_id['gone1']['record_type'], 'post_metadata_removed')
            self.assertNotIn('title', by_id['gone1'])
            self.assertEqual(by_id['live1']['title'], 'Refreshed title')

            # No stray temp file left behind after a successful atomic replace.
            self.assertFalse((Path(tmpdir) / 'posts.jsonl.reconcile.tmp').exists())

    def test_reconcile_file_leaves_original_untouched_on_partial_api_failure(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / 'posts.jsonl'
            original_text = (
                json.dumps({'reddit_id': 'live1', 'title': 'Old cached title'}) + '\n' +
                json.dumps({'reddit_id': 'boom', 'title': 'Old cached title'}) + '\n'
            )
            path.write_text(original_text, encoding='utf-8')

            class FailingClient:
                def get_json(self, path, params=None):
                    post_id = params['id'].split('_', 1)[1]
                    if post_id == 'boom':
                        raise RedditAPIError('simulated API failure')
                    return {
                        'data': {'children': [{'data': {'id': post_id, 'title': 'Refreshed title'}}]}
                    }, {}

            with self.assertRaises(RedditAPIError):
                reconcile_file(FailingClient(), path)

            self.assertEqual(path.read_text(encoding='utf-8'), original_text)
            self.assertFalse((Path(tmpdir) / 'posts.jsonl.reconcile.tmp').exists())

    def test_reconcile_file_missing_input_raises_without_writing(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / 'missing.jsonl'

            class UnusedClient:
                def get_json(self, path, params=None):
                    raise AssertionError('should not be called when input file is missing')

            with self.assertRaises(FileNotFoundError):
                reconcile_file(UnusedClient(), path)
            self.assertFalse(path.exists())


_WORKFLOW_STEP_START_RE = re.compile(r'^      - ')


def _load_workflow_step_blocks(text):
    """Split a GitHub Actions workflow's job ``steps:`` list into blocks.

    Dependency-free (stdlib ``re``/text only, no PyYAML): relies on this
    repository's fixed 2-space-per-level indentation, where each step in
    the (single) ``crawl`` job begins with a line matching exactly six
    leading spaces followed by ``- `` and every following line belonging
    to that step is indented further (or blank), until the next step
    starts.
    """
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == 'steps:':
            start = i + 1
            break
    if start is None:
        raise AssertionError("workflow has no 'steps:' key")

    blocks = []
    current = None
    for line in lines[start:]:
        if _WORKFLOW_STEP_START_RE.match(line):
            if current is not None:
                blocks.append(current)
            current = [line]
        elif current is not None and (line.strip() == '' or line.startswith(' ')):
            current.append(line)
        else:
            break
    if current is not None:
        blocks.append(current)
    return blocks


def _workflow_step_name(block):
    match = re.match(r'^\s*-\s*name:\s*(.*)$', block[0])
    return match.group(1).strip() if match else None


def _workflow_step_env(block):
    """Extract the ``env:`` mapping scoped to a single step block only."""
    env = {}
    in_env = False
    env_indent = None
    for line in block[1:]:
        if not in_env:
            match = re.match(r'^(\s*)env:\s*$', line)
            if match:
                in_env = True
                env_indent = len(match.group(1))
            continue
        if line.strip() == '':
            continue
        indent = len(line) - len(line.lstrip(' '))
        if indent <= env_indent:
            break
        match = re.match(r'^\s*([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$', line)
        if match:
            env[match.group(1)] = match.group(2).strip()
    return env


def _workflow_step_if(block):
    for line in block:
        match = re.match(r'^\s*if:\s*(.*)$', line)
        if match:
            return match.group(1).strip()
    return None


def _workflow_step_run_text(block):
    collecting = False
    run_indent = None
    out = []
    for line in block:
        if not collecting:
            match = re.match(r'^(\s*)run:\s*\|\s*$', line)
            if match:
                collecting = True
                run_indent = len(match.group(1))
                continue
            inline = re.match(r'^\s*run:\s*(.+)$', line)
            if inline:
                return inline.group(1).strip()
            continue
        if line.strip():
            indent = len(line) - len(line.lstrip(' '))
            if indent <= run_indent:
                break
        out.append(line)
    return '\n'.join(out)


class RedditExactFetchReplacementTests(unittest.TestCase):
    """Exact --post-id refresh must replace, not merely append, on removal."""

    @staticmethod
    def _removed_client(reddit_id='abc123'):
        class RemovedClient:
            def get_json(self, path, params=None):
                return {
                    'data': {
                        'children': [{
                            'data': {
                                'id': reddit_id,
                                'title': '[removed]',
                                'removed_by_category': 'moderator',
                            }
                        }]
                    }
                }, {}

        return RemovedClient()

    @staticmethod
    def _live_client(reddit_id='abc123', title='Refreshed live title'):
        class LiveClient:
            def get_json(self, path, params=None):
                return {
                    'data': {
                        'children': [{
                            'data': {
                                'id': reddit_id,
                                'title': title,
                                'permalink': f'/r/NeuronsToNirvana/comments/{reddit_id}/example/',
                            }
                        }]
                    }
                }, {}

        return LiveClient()

    def test_exact_removed_post_replaces_existing_cached_content_atomically(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'posts.jsonl'
            stale = {
                'schema_version': 'akashicnet.reddit.post.v2',
                'source': 'reddit',
                'record_type': 'post_metadata',
                'reddit_id': 'abc123',
                'subreddit': 'NeuronsToNirvana',
                'title': 'Stale cached title',
                'canonical_url': 'https://www.reddit.com/r/NeuronsToNirvana/comments/abc123/example/',
                'external_url': 'https://example.org/source',
                'created_utc': 123.0,
                'retrieved_at': '2026-08-01T00:00:00Z',
                'provenance': {'api': 'reddit-data-api', 'endpoint': 'subreddit_listing', 'metadata_only': True},
            }
            other = {'reddit_id': 'other1', 'title': 'Unrelated kept record'}
            output.write_text(
                json.dumps(stale) + '\n' + json.dumps(other) + '\n',
                encoding='utf-8',
            )

            written, skipped = crawl_post(self._removed_client('abc123'), 'abc123', output)
            self.assertEqual((written, skipped), (1, 0))

            lines = [json.loads(line) for line in output.read_text(encoding='utf-8').splitlines()]
            by_id = {record['reddit_id']: record for record in lines}
            self.assertEqual(len(lines), 2)
            self.assertEqual(by_id['other1'], other)

            tombstone = by_id['abc123']
            self.assertEqual(tombstone['record_type'], 'post_metadata_removed')
            self.assertEqual(tombstone['status'], 'removed')
            self.assertEqual(tombstone['provenance']['endpoint'], 'post_info')
            for content_field in (
                'title', 'canonical_url', 'external_url', 'subreddit',
                'created_utc', 'retrieved_at', 'score', 'num_comments',
                'upvote_ratio', 'author', 'selftext',
            ):
                self.assertNotIn(content_field, tombstone)

            # Exactly one record survives for abc123 anywhere in the file.
            self.assertEqual(sum(1 for r in lines if r.get('reddit_id') == 'abc123'), 1)
            self.assertFalse((Path(tmpdir) / 'posts.jsonl.exactfetch.tmp').exists())

    def test_exact_removed_post_with_no_prior_record_writes_one_tombstone(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'posts.jsonl'
            written, skipped = crawl_post(self._removed_client('abc123'), 'abc123', output)
            self.assertEqual((written, skipped), (1, 0))

            lines = [json.loads(line) for line in output.read_text(encoding='utf-8').splitlines()]
            self.assertEqual(len(lines), 1)
            self.assertEqual(lines[0]['record_type'], 'post_metadata_removed')
            self.assertEqual(lines[0]['reddit_id'], 'abc123')
            self.assertEqual(lines[0]['provenance']['endpoint'], 'post_info')

    def test_exact_live_refetch_of_existing_id_is_still_treated_as_duplicate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'posts.jsonl'
            output.write_text(json.dumps({'reddit_id': 'abc123', 'title': 'Old'}) + '\n', encoding='utf-8')

            written, skipped = crawl_post(self._live_client('abc123'), 'abc123', output)
            self.assertEqual((written, skipped), (0, 1))
            lines = output.read_text(encoding='utf-8').splitlines()
            self.assertEqual(len(lines), 1)
            self.assertEqual(json.loads(lines[0])['title'], 'Old')

    def test_replace_exact_post_record_failure_preserves_original_artifact(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / 'posts.jsonl'
            original_text = (
                json.dumps({'reddit_id': 'abc123', 'title': 'Stale cached title'}) + '\n' +
                'not-valid-json\n'
            )
            output.write_text(original_text, encoding='utf-8')

            tombstone = tombstone_record('abc123', '2026-09-08T00:00:00Z', status='removed', endpoint='post_info')
            with self.assertRaises(json.JSONDecodeError):
                replace_exact_post_record(tombstone, output)

            self.assertEqual(output.read_text(encoding='utf-8'), original_text)
            self.assertFalse((Path(tmpdir) / 'posts.jsonl.exactfetch.tmp').exists())


class RedditPilotWorkflowGateWiringTests(unittest.TestCase):
    """Deterministic validation of the reddit-pilot.yml approval wiring.

    scripts/reddit_crawler.py's main() now enforces
    ``os.getenv("REDDIT_API_APPROVED") == "true"`` as a fail-closed local
    gate. Any workflow step that runs the crawler must therefore also
    receive REDDIT_API_APPROVED in its step ``env``, or an otherwise
    correctly-approved CI run would exit 3 before ever reaching Reddit.

    This validation is intentionally dependency-free (stdlib ``re``/text
    parsing only, no PyYAML): reddit-pilot.yml runs
    ``python -m unittest tests.test_reddit_crawler -v`` without installing
    PyYAML, so this test module must not require it.
    """

    WORKFLOW_PATH = Path(__file__).resolve().parents[1] / '.github' / 'workflows' / 'reddit-pilot.yml'

    @classmethod
    def setUpClass(cls):
        text = cls.WORKFLOW_PATH.read_text(encoding='utf-8')
        cls.steps = _load_workflow_step_blocks(text)

    def _step(self, name):
        for block in self.steps:
            if _workflow_step_name(block) == name:
                return block
        raise AssertionError(f'workflow step not found: {name}')

    def test_gate_step_receives_repository_variable_via_env(self):
        gate = self._step('Reddit API approval gate')
        env = _workflow_step_env(gate)
        self.assertEqual(env.get('REDDIT_API_APPROVED'), '${{ vars.REDDIT_API_APPROVED }}')
        # Exact-string comparison against a quoted shell variable, not an
        # inline template interpolated directly into shell source.
        run_text = _workflow_step_run_text(gate)
        self.assertIn('if [ "$REDDIT_API_APPROVED" = "true" ]', run_text)
        self.assertNotIn('${{ vars.REDDIT_API_APPROVED }}', run_text)

    def test_crawler_pilot_step_also_receives_repository_variable_via_env(self):
        pilot = self._step('Run crawler pilot')
        env = _workflow_step_env(pilot)
        self.assertEqual(
            env.get('REDDIT_API_APPROVED'),
            '${{ vars.REDDIT_API_APPROVED }}',
            'Run crawler pilot step must forward REDDIT_API_APPROVED so scripts/reddit_crawler.py '
            'main() does not exit 3 before an otherwise-approved pilot run reaches Reddit.',
        )

    def test_gate_step_env_is_distinct_from_crawler_step_env(self):
        # Proves the parser (and the workflow) scope env per-step: the gate
        # step's env must not be conflated with, or substitute for, the
        # crawler pilot step's own env mapping. This fails if the
        # crawler-step REDDIT_API_APPROVED mapping is removed while the
        # gate step's mapping remains untouched.
        gate_env = _workflow_step_env(self._step('Reddit API approval gate'))
        pilot_env = _workflow_step_env(self._step('Run crawler pilot'))
        self.assertEqual(set(gate_env), {'REDDIT_API_APPROVED'})
        self.assertIn('REDDIT_API_APPROVED', pilot_env)
        self.assertIn('REDDIT_CLIENT_ID', pilot_env)
        self.assertNotIn('REDDIT_CLIENT_ID', gate_env)

    def test_crawler_pilot_step_condition_and_credential_isolation_unchanged(self):
        pilot = self._step('Run crawler pilot')
        expected_condition = (
            "${{ steps.gate.outputs.approved == 'true' && "
            "(github.event_name == 'workflow_dispatch' || "
            "contains(github.event.head_commit.message, '[reddit-smoke]')) }}"
        )
        self.assertEqual(_workflow_step_if(pilot), expected_condition)
        env = _workflow_step_env(pilot)
        self.assertEqual(env.get('REDDIT_CLIENT_ID'), '${{ secrets.REDDIT_CLIENT_ID }}')
        self.assertEqual(env.get('REDDIT_CLIENT_SECRET'), '${{ secrets.REDDIT_CLIENT_SECRET }}')

    def test_simulated_env_resolution_when_repository_variable_is_exactly_true(self):
        """Simulate GitHub Actions env resolution for the approved case.

        Confirms that when the repository variable REDDIT_API_APPROVED is
        exactly 'true', the templated env mapping for the crawler pilot
        step resolves to a REDDIT_API_APPROVED value that satisfies
        scripts/reddit_crawler.py's local gate, without invoking any
        network access.
        """
        pilot = self._step('Run crawler pilot')
        template = _workflow_step_env(pilot)['REDDIT_API_APPROVED']
        simulated_vars = {'REDDIT_API_APPROVED': 'true'}
        resolved = template.replace('${{ vars.REDDIT_API_APPROVED }}', simulated_vars['REDDIT_API_APPROVED'])
        self.assertEqual(resolved, 'true')

        with patch.dict(os.environ, {'REDDIT_API_APPROVED': resolved}, clear=True):
            # Gate check alone must pass; missing credentials should be the
            # very next failure, proving the approval gate is satisfied.
            rc = main(['NeuronsToNirvana'])
            self.assertEqual(rc, 2)


if __name__ == '__main__':
    unittest.main()
