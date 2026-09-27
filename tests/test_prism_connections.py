"""Synthetic source-traceability regressions; no evidence or gate approvals."""
import copy
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/validate_prism_connections.py'
FIXTURE = ROOT / 'tests/fixtures/prism/connection-traceability.json'
SPEC = importlib.util.spec_from_file_location('prism_connections', SCRIPT)
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ConnectionTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(FIXTURE.read_text())

    def test_traceable_fixture_passes_without_mutation(self):
        before = copy.deepcopy(self.record)
        self.assertEqual(validator.validate(self.record), [])
        self.assertEqual(self.record, before)

    def test_all_lane_strength_and_source_presence_combinations(self):
        properties = validator.SCHEMA['properties']['connections']['items']['properties']
        for lane, strength, sources in itertools.product(
                properties['evidence_lane']['enum'],
                properties['current_strength']['enum'], (None, [], ['SRC-TEST'])):
            with self.subTest(lane=lane, strength=strength, sources=sources):
                record = copy.deepcopy(self.record)
                connection = record['connections'][0]
                connection.update(evidence_lane=lane, current_strength=strength)
                if sources is None:
                    del connection['source_ids']
                else:
                    connection['source_ids'] = sources
                allowed = bool(sources) or (
                    lane != 'established_evidence'
                    and strength in ('descriptive_only', 'unresolved'))
                self.assertEqual(validator.VALIDATOR.is_valid(record), allowed)
                self.assertEqual(not validator.validate(record), allowed)

    def test_source_free_exceptions_require_hold(self):
        for strength, sources in itertools.product(
                ('descriptive_only', 'unresolved'), (None, [])):
            record = copy.deepcopy(self.record)
            record['connections'][0]['current_strength'] = strength
            if sources is None:
                del record['connections'][0]['source_ids']
            else:
                record['connections'][0]['source_ids'] = sources
            record['source_network']['nodes'] = []
            self.assertEqual(validator.validate(record), [])
            record['governance']['publication_status'] = 'review_candidate'
            self.assertFalse(validator.VALIDATOR.is_valid(record))
            self.assertTrue(validator.validate(record))

    def test_source_free_exception_cannot_hide_behind_sourced_connection(self):
        record = self.record
        record['connections'].append(copy.deepcopy(record['connections'][0]))
        record['connections'][1]['connection_id'] = 'CONN-SECOND'
        record['connections'][1]['source_ids'] = []
        record['governance']['publication_status'] = 'review_candidate'
        self.assertTrue(validator.validate(record))

    def test_unknown_ambiguous_and_blank_locator_sources_fail(self):
        for strength in ('descriptive_only', 'well_supported'):
            for mutation in ('unknown', 'duplicate', 'blank'):
                with self.subTest(strength=strength, mutation=mutation):
                    record = copy.deepcopy(self.record)
                    record['connections'][0]['current_strength'] = strength
                    nodes = record['source_network']['nodes']
                    if mutation == 'unknown':
                        record['connections'][0]['source_ids'].append('SRC-MISSING')
                    elif mutation == 'duplicate':
                        nodes.append(copy.deepcopy(nodes[0]))
                    else:
                        nodes[0]['locator'] = ' \t\n'
                    self.assertTrue(validator.VALIDATOR.is_valid(record))
                    self.assertTrue(validator.validate(record))

    def test_invalid_source_values_fail(self):
        for sources in (None, '', [''], ['bad-id'], ['SRC-TEST', 'SRC-TEST'], [None]):
            record = copy.deepcopy(self.record)
            record['connections'][0]['source_ids'] = sources
            self.assertTrue(validator.validate(record), repr(sources))

    def test_no_promotion_constants_still_fail_closed(self):
        for field in ('truth_inference_allowed', 'testimony_auto_promotion_allowed',
                      'tradition_auto_promotion_allowed'):
            record = copy.deepcopy(self.record)
            record['governance'][field] = True
            self.assertTrue(validator.validate(record), field)

    def test_optional_connections_remain_optional(self):
        del self.record['connections']
        self.assertEqual(validator.validate(self.record), [])

    def test_cli_rejects_unsupported_and_malformed_records(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(FIXTURE)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.record['connections'][0].update(
            evidence_lane='established_evidence', current_strength='well_supported')
        del self.record['connections'][0]['source_ids']
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid.json'
            for content in (json.dumps(self.record), '{', '{"x": 1, "x": 2}',
                            '{"x": NaN}', '[]'):
                path.write_text(content)
                result = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 1)
                self.assertIn('ERROR:', result.stdout)
                self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
