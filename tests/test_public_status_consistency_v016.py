"""Typed status, generated rendering, and editorial-boundary regression tests."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('status', ROOT / 'scripts/validate_public_status_consistency_v016.py')
status = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(status)

class PublicStatusTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        paths = [status.DATA, status.MANIFEST, *status.SURFACES]
        paths += [source for source, _ in status.SURFACES.values()]
        for name in paths:
            dest = self.root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)

    def mutate_data(self, change):
        data = copy.deepcopy(status.EXPECTED)
        change(data)
        (self.root / status.DATA).write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'contract drift'):
            status.check(self.root)

    def test_current_pages_and_deterministic_replay(self):
        status.check(self.root)
        before = status.render(self.root)
        status.check(self.root, write=True)
        self.assertEqual(before, status.render(self.root))
        status.check(self.root)

    def test_no_release_or_resolution_promotion(self):
        changes = [
            lambda d: d['candidate'].update(sealed=True),
            lambda d: d['site_checkpoint'].update(is_release=True),
            lambda d: d['target']['github_release'].update(prerelease=False),
            lambda d: d['bq001'].update(status='RESOLVED'),
            lambda d: d['bq001'].update(accepted_edges=1),
            lambda d: d.update(reddit_live_access='LIVE'),
            lambda d: d.update(promotion_allowed=True),
        ]
        for change in changes:
            with self.subTest(change=change): self.mutate_data(change)

    def test_readiness_and_publication_are_independently_pinned(self):
        for field in ('readiness', 'github_release'):
            for key in status.EXPECTED['target'][field]:
                with self.subTest(field=field, key=key, mutation='delete'):
                    self.mutate_data(lambda d: d['target'][field].pop(key))
                with self.subTest(field=field, key=key, mutation='contradict'):
                    self.mutate_data(lambda d: d['target'][field].update({key: 'unverified'}))
        for change in (
            lambda d: d['target'].update(status='NEXT_MINOR'),
            lambda d: d['target'].update(released=False),
            lambda d: d['target'].pop('readiness'),
            lambda d: d['target'].pop('github_release'),
            lambda d: d['target']['readiness'].update(commit='2ab380827fd0ac0a1f89484867e10c26977a7c86'),
            lambda d: d['target']['github_release'].update(prerelease=1),
        ):
            self.mutate_data(change)

    def test_rendered_readiness_does_not_approve_main_or_deployment(self):
        page = status.render(self.root)['website/app/development-progress/page.tsx']
        for text in ('06:01:56 Europe/Berlin', '06:06:55 Europe/Berlin',
                     'Approval does not extend to later main changes.',
                     'GitHub publication does not establish website deployment.',
                     status.EXPECTED['target']['readiness']['commit'],
                     status.EXPECTED['target']['github_release']['url']):
            self.assertIn(text, page)
        self.assertNotIn('progress toward v0.17.0', page)
        self.assertNotIn('NEXT MINOR', page)

    def test_published_github_release_must_be_non_draft(self):
        for mutation in (
            lambda d: d['target']['github_release'].pop('draft'),
            lambda d: d['target']['github_release'].update(draft=True),
        ):
            with self.subTest(mutation=mutation):
                self.mutate_data(mutation)

    def test_homepage_ready_label_is_bounded_to_approved_commit(self):
        homepage = status.render(self.root)['website/app/page.tsx']
        commit = status.EXPECTED['target']['readiness']['commit']
        self.assertIn('v0.17.0 READY · bounded review only · ' + commit, homepage)

    def test_types_unknown_fields_and_missing_fields_fail(self):
        for change in (lambda d: d['candidate'].update(sealed=0),
                       lambda d: d['bq001'].update(accepted_edges=False),
                       lambda d: d.update(schema_version=True),
                       lambda d: d.update(label='Released'),
                       lambda d: d.pop('candidate')):
            with self.subTest(change=change): self.mutate_data(change)

    def test_duplicate_json_keys_rejected(self):
        path = self.root / status.DATA
        path.write_text(path.read_text().replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1'))
        with self.assertRaisesRegex(ValueError, 'duplicate JSON key'): status.check(self.root)

    def test_manifest_disagreement_rejected(self):
        original = status.read_json(self.root / status.MANIFEST)
        for key, value in (('schema_version', '0.17.0'), ('artifact_status', 'RELEASED'),
                           ('promotion_boundaries', {'truth': True})):
            with self.subTest(key=key):
                data = copy.deepcopy(original); data[key] = value
                (self.root / status.MANIFEST).write_text(json.dumps(data))
                with self.assertRaises(ValueError): status.check(self.root)

    def test_manifest_candidate_iteration_matches_rendered_ordinal(self):
        original = status.read_json(self.root / status.MANIFEST)
        for value in (None, 3, True, 2.0, '2'):
            with self.subTest(value=value):
                data = copy.deepcopy(original)
                if value is None:
                    del data['candidate_iteration']
                else:
                    data['candidate_iteration'] = value
                (self.root / status.MANIFEST).write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, 'candidate iteration'):
                    status.check(self.root, write=True)

    def test_manifest_pending_release_requirements(self):
        original = status.read_json(self.root / status.MANIFEST)
        for key, values in (
            ('release_decision', (None, 'READY', 'RELEASED', False)),
            ('exact_head_ci_required', (None, False, 1, 'true')),
        ):
            for value in values:
                with self.subTest(key=key, value=value):
                    data = copy.deepcopy(original)
                    if value is None:
                        del data[key]
                    else:
                        data[key] = value
                    (self.root / status.MANIFEST).write_text(json.dumps(data))
                    before = {path: (self.root / path).read_bytes() for path in status.SURFACES}
                    with self.assertRaisesRegex(ValueError, 'pending exact-head CI and review'):
                        status.check(self.root, write=True)
                    self.assertEqual(before, {path: (self.root / path).read_bytes() for path in status.SURFACES})

    def test_manifest_question_identity_is_required(self):
        original = status.read_json(self.root / status.MANIFEST)
        for question_id in (None, 'BQ002'):
            with self.subTest(question_id=question_id):
                data = copy.deepcopy(original)
                if question_id is None:
                    del data['candidate_summary']['question_id']
                else:
                    data['candidate_summary']['question_id'] = question_id
                (self.root / status.MANIFEST).write_text(json.dumps(data))
                with self.assertRaisesRegex(ValueError, 'BQ001 boundaries drift'):
                    status.check(self.root)

    def test_rendered_labels_cannot_be_changed_by_hand(self):
        for output in status.SURFACES:
            with self.subTest(output=output):
                path = self.root / output; old = path.read_text()
                path.write_text(old.replace('READY', 'STABLE RELEASE'))
                with self.assertRaisesRegex(ValueError, 'surface drift'): status.check(self.root)
                path.write_text(old)

    def test_required_slots_cannot_be_removed_or_duplicated(self):
        for source, tokens in status.SURFACES.values():
            path = self.root / source; original = path.read_text()
            for token in tokens:
                for replacement in ('', ('@@' + token + '@@') * 2):
                    with self.subTest(token=token, replacement=replacement):
                        marker = '@@' + token + '@@'
                        path.write_text(original.replace(marker, replacement))
                        with self.assertRaises(ValueError): status.check(self.root)
            path.write_text(original)

    def test_dependency_versions_and_disclaimers_are_editorial_copy(self):
        # These examples are accepted as template prose, never used as status data.
        path = self.root / 'website/status-templates/home.tsx.in'
        for text in ("AkashicNET, built with React v19.0", "v0.16.7 is not to be released",
                     "v0.16.7 has not been released, sealed, or shipped"):
            path.write_text(path.read_text() + '\n// Editorial example: ' + text + '\n')
        status.check(self.root, write=True)
        status.check(self.root)
        self.assertFalse(status.read_json(self.root / status.DATA)['candidate']['sealed'])

    def test_free_prose_does_not_set_authoritative_status(self):
        # Semantic review is explicitly outside this validator's contract.
        path = self.root / 'website/status-templates/home.tsx.in'
        path.write_text(path.read_text() + '\n// Review fixture: Official release is v0.16.7\n')
        status.check(self.root, write=True)
        self.assertFalse(status.read_json(self.root / status.DATA)['site_checkpoint']['is_release'])

if __name__ == '__main__': unittest.main()

