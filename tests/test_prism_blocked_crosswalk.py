"""Regression cases for fabricated reads, promotion and checkpoint drift."""
import copy
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/validate_prism_blocked_crosswalk.py'
SPEC = importlib.util.spec_from_file_location('crosswalk_validator', SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class CrosswalkTests(unittest.TestCase):
    def setUp(self):
        self.data = validator.load_crosswalk(validator.DEFAULT_PATH)

    def test_current_checkpoint_passes(self):
        self.assertEqual(validator.validate(self.data), [])

    def test_record_order_does_not_change_membership(self):
        self.data['records'].reverse()
        self.assertEqual(validator.validate(self.data), [])

    def test_unread_cannot_become_not_applicable_or_verified(self):
        for status in ('NOT_APPLICABLE', 'VERIFIED', None):
            with self.subTest(status=status):
                self.data['records'][0]['paper_link_resolution']['status'] = status
                self.assertTrue(validator.validate(self.data))

    def test_fabricated_source_metadata_is_rejected(self):
        for field, value in {'primary_doi': '10.1234/fabricated',
                             'additional_dois': ['10.1234/other'],
                             'paper_title': 'Unverified title',
                             'paper_authors': ['Unverified author'],
                             'checked_on': '2026-09-23',
                             'verification_depth': 'FULL_TEXT',
                             'relationship_to_post': 'VERIFIED',
                             'link_found_in': 'post',
                             'link_evidence_locator': 'invented'}.items():
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data['records'][0]['paper_link_resolution'][field] = value
                self.assertTrue(validator.validate(data))

    def test_missing_and_unknown_resolution_fields_fail(self):
        for field in self.data['records'][0]['paper_link_resolution']:
            data = copy.deepcopy(self.data)
            del data['records'][0]['paper_link_resolution'][field]
            self.assertTrue(validator.validate(data), field)
        self.data['records'][0]['paper_link_resolution']['approved'] = True
        self.assertTrue(validator.validate(self.data))

    def test_all_permissions_require_explicit_false(self):
        for permission in self.data['records'][0]['promotion_permissions']:
            for value in (True, 0, None, 'false'):
                data = copy.deepcopy(self.data)
                data['records'][0]['promotion_permissions'][permission] = value
                self.assertTrue(validator.validate(data), (permission, value))
            data = copy.deepcopy(self.data)
            del data['records'][0]['promotion_permissions'][permission]
            self.assertTrue(validator.validate(data), permission)

    def test_membership_drift_fails_even_with_same_total(self):
        self.data['records'][1] = copy.deepcopy(self.data['records'][0])
        self.assertTrue(validator.validate(self.data))

    def test_missing_record_and_adjusted_total_fail(self):
        self.data['records'].pop()
        self.data['assessment_summary']['source_records'] = 40
        self.assertTrue(validator.validate(self.data))

    def test_pin_and_metadata_provenance_tampering_fail(self):
        for path, field in [('source_checkpoint', 'head_commit'),
                            ('source_checkpoint', 'blob_sha')]:
            data = copy.deepcopy(self.data)
            data[path][field] = '0' * 40
            self.assertTrue(validator.validate(data))
        self.data['doi_enrichment_followup']['metadata_check']['source_blob'] = '0' * 40
        self.assertTrue(validator.validate(self.data))

    def test_count_and_gate_changes_fail(self):
        for field in ('source_records', 'original_blocked', 'original_complete',
                      'prism_registered_metadata_only', 'publication_eligible'):
            data = copy.deepcopy(self.data)
            data['assessment_summary'][field] += 1
            self.assertTrue(validator.validate(data), field)
        for field, value in [('reddit_live_access', 'OPEN'), ('publication', 'OPEN'),
                             ('accepted_canonical_edges', 1), ('big_questions', 'RESOLVED')]:
            data = copy.deepcopy(self.data)
            data['safeguards'][field] = value
            self.assertTrue(validator.validate(data), field)

    def test_malformed_shapes_report_errors(self):
        for value in (None, [], 'record'):
            data = copy.deepcopy(self.data)
            data['records'][0] = value
            self.assertTrue(validator.validate(data))
        self.assertTrue(validator.validate([]))

    def test_cli_rejects_invalid_json_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'bad.json'
            for content in ('{', '{"records": [], "records": []}', '{"value": NaN}'):
                path.write_text(content)
                result = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertIn('ERROR:', result.stdout)
                self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
