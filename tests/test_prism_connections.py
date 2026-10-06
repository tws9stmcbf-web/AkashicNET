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
                if lane == 'traditional_knowledge':
                    record['perspectives'][0]['cultural_authority'] = {
                        'community_or_lineage': None, 'speaker_position': None,
                        'authority_to_share': 'unknown',
                    }
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
            record['governance'].update(privacy_disposition='cleared', cultural_review_status='cleared')
            record['governance']['publication_status'] = 'review_candidate'
            self.assertFalse(validator.VALIDATOR.is_valid(record))
            self.assertTrue(validator.validate(record))

    def test_source_free_exception_cannot_hide_behind_sourced_connection(self):
        record = self.record
        record['connections'].append(copy.deepcopy(record['connections'][0]))
        record['connections'][1]['connection_id'] = 'CONN-SECOND'
        record['connections'][1]['source_ids'] = []
        record['governance'].update(privacy_disposition='cleared', cultural_review_status='cleared')
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

    def independent_pair(self):
        network = self.record['source_network']
        first = network['nodes'][0]
        first.update(provenance_state='verified', work_id='WORK-A')
        second = copy.deepcopy(first)
        second.update(source_id='SRC-SECOND', work_id='WORK-B', locator='urn:synthetic:second')
        network['nodes'].append(second)
        network['edges'] = [dict(edge_id='EDGE-TEST', from_source_id='SRC-TEST',
                                 to_source_id='SRC-SECOND', relation='supports',
                                 independent_evidence=True)]
        network['counting_boundary']['independent_evidence_sources'] = 2
        return network

    def test_unresolved_or_empty_network_cannot_claim_evidence(self):
        for count in (1, 999, True, 0.0):
            record = copy.deepcopy(self.record)
            record['source_network']['counting_boundary']['independent_evidence_sources'] = count
            self.assertTrue(validator.validate(record))
        self.record['source_network']['nodes'] = []
        self.record['connections'] = []
        self.assertEqual(validator.validate(self.record), [])
        self.record['source_network']['counting_boundary']['independent_evidence_sources'] = 1
        self.assertTrue(validator.validate(self.record))

    def test_independent_work_count_is_recomputed(self):
        network = self.independent_pair()
        self.assertEqual(validator.validate(self.record), [])
        network['edges'].append(dict(network['edges'][0], edge_id='EDGE-REPEAT'))
        self.assertEqual(validator.validate(self.record), [])
        for count in (0, 1, 3):
            network['counting_boundary']['independent_evidence_sources'] = count
            self.assertTrue(validator.validate(self.record))

    def test_unverified_unlocated_or_unidentified_work_rejected(self):
        self.independent_pair()
        for field, value in [('provenance_state', 'unresolved'), ('work_id', None),
                             ('work_id', '  '), ('locator', '  ')]:
            record = copy.deepcopy(self.record)
            record['source_network']['nodes'][1][field] = value
            self.assertTrue(validator.validate(record), field)
        self.record['source_network']['edges'][0]['to_source_id'] = 'SRC-MISSING'
        self.assertTrue(validator.validate(self.record))

    def test_duplicate_work_aliases_and_derivation_are_not_independent(self):
        self.independent_pair()
        for field, value in [('work_id', 'WORK-SAME'), ('doi', '10.1234/same'),
                             ('locator', 'urn:same'), ('post_id', 'same')]:
            record = copy.deepcopy(self.record)
            for node in record['source_network']['nodes']:
                node[field] = value
            self.assertTrue(validator.validate(record), field)
        for relation in ('same_work_as', 'derived_from'):
            record = copy.deepcopy(self.record)
            record['source_network']['edges'].append(dict(
                record['source_network']['edges'][0], edge_id='EDGE-ALIAS',
                relation=relation, independent_evidence=False))
            self.assertTrue(validator.validate(record), relation)
        self.record['source_network']['nodes'].append(
            copy.deepcopy(self.record['source_network']['nodes'][0]))
        self.assertTrue(validator.validate(self.record))

    def test_null_or_false_independence_does_not_count(self):
        network = self.independent_pair()
        for value in (False, None):
            network['edges'][0]['independent_evidence'] = value
            network['counting_boundary']['independent_evidence_sources'] = 0
            self.assertEqual(validator.validate(self.record), [])
            network['counting_boundary']['independent_evidence_sources'] = 2
            self.assertTrue(validator.validate(self.record))

    def test_doi_identity_aliases_cannot_inflate_independent_count(self):
        self.independent_pair()
        for left_field, right_field, left, right in (
                ('doi', 'doi', '10.1234/Same', '10.1234/same'),
                ('doi', 'locator', '10.1234/same', 'https://doi.org/10.1234/same'),
                ('locator', 'locator', 'https://doi.org/10.1234/same',
                 'http://dx.doi.org/10.1234/same'),
                ('locator', 'locator', 'https://doi.org/10.1234/same',
                 'https://doi.org/10.1234/%73ame?utm_source=copy#abstract')):
            with self.subTest(left=left, right=right):
                record = copy.deepcopy(self.record)
                record['source_network']['nodes'][0][left_field] = left
                record['source_network']['nodes'][1][right_field] = right
                self.assertTrue(validator.VALIDATOR.is_valid(record))
                self.assertIn('independence conflicts', ' '.join(validator.validate(record)))

    def test_valid_distinct_dois_do_not_fail_the_schema(self):
        network = self.independent_pair()
        network['nodes'][0]['doi'] = '10.1234/first'
        network['nodes'][1]['doi'] = '10.1234/second'
        self.assertEqual(validator.validate(self.record), [])

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
