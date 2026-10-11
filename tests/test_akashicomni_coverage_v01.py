"""Coverage records must never bypass packet validation or acceptance gates."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/validate_akashicomni_coverage_v01.py'
spec = importlib.util.spec_from_file_location('coverage_validator', SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
PACKET = ROOT / 'data/akashicomni/meditation-crime-pilot-v0.5.0.json'
FIXTURE = ROOT / 'tests/fixtures/akashicomni/coverage-synthetic-v0.1.json'


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(FIXTURE.read_text())
        self.packet = PACKET.read_bytes()

    def errors(self):
        return validator.validate(self.record, self.packet)

    def test_full_synthetic_structure(self):
        self.assertEqual(self.errors(), [])

    def test_narrow_discloses_exclusion(self):
        entry = self.record['coverage'].pop()
        self.record['scope']['mode'] = 'NARROW'
        self.record['scope']['excluded_perspectives'] = [
            {'perspective_id': entry['perspective_id'], 'reason': 'Synthetic scope exclusion.'}]
        self.assertEqual(self.errors(), [])

    def test_missing_duplicate_unknown_and_overlapping_perspectives(self):
        original = copy.deepcopy(self.record)
        for kind in ('missing', 'duplicate', 'unknown', 'overlap', 'narrow_without_exclusions'):
            with self.subTest(kind=kind):
                self.record = copy.deepcopy(original)
                if kind == 'missing':
                    self.record['coverage'].pop()
                elif kind == 'duplicate':
                    self.record['coverage'].append(copy.deepcopy(self.record['coverage'][0]))
                elif kind == 'unknown':
                    self.record['coverage'][0]['perspective_id'] = 'INVENTED'
                elif kind == 'overlap':
                    self.record['scope']['excluded_perspectives'] = [
                        {'perspective_id': self.record['coverage'][0]['perspective_id'], 'reason': 'Excluded'}]
                else:
                    self.record['scope']['mode'] = 'NARROW'
                self.assertTrue(self.errors())

    def test_exact_packet_binding(self):
        self.packet += b'\n'
        self.assertTrue(self.errors())
        self.record['packet_binding']['sha256'] = hashlib.sha256(self.packet).hexdigest()
        self.assertEqual(self.errors(), [])
        self.record['packet_binding']['packet_id'] = 'WRONG-PACKET'
        self.assertTrue(self.errors())

    def test_rehash_does_not_bypass_packet_gates(self):
        packet = json.loads(self.packet)
        packet['promotion_allowed']['truth'] = True
        self.packet = json.dumps(packet).encode()
        self.record['packet_binding']['sha256'] = hashlib.sha256(self.packet).hexdigest()
        self.assertTrue(self.errors())

    def test_unknown_claim(self):
        self.record['scope']['claim_ids'] = ['UNKNOWN-CLAIM']
        self.assertTrue(self.errors())

    def test_source_context_exact_and_nonpromoting(self):
        original = copy.deepcopy(self.record)
        for kind in ('missing', 'duplicate', 'unknown', 'upgraded'):
            with self.subTest(kind=kind):
                self.record = copy.deepcopy(original)
                if kind == 'missing':
                    self.record['source_context'].pop()
                elif kind == 'duplicate':
                    self.record['source_context'].append(copy.deepcopy(self.record['source_context'][0]))
                elif kind == 'unknown':
                    self.record['source_context'][0]['source_id'] = 'UNKNOWN-SOURCE'
                else:
                    self.record['source_context'][0]['access_status'] = 'FULL_TEXT_INSPECTED'
                    self.record['source_context'][0]['inspected_scope'] = 'Unsupported upgrade'
                self.assertTrue(self.errors())

    def test_applied_requires_inspected_source_and_contribution(self):
        entry = self.record['coverage'][0]
        entry.update(state='APPLIED', contribution='Synthetic contribution.', source_ids=['SOURCE-HAGELIN-1999'])
        self.assertTrue(self.errors())
        entry['source_ids'] = ['SOURCE-EDITORIAL-20260919']
        self.assertEqual(self.errors(), [])
        entry['contribution'] = None
        self.assertTrue(self.errors())

    def test_unavailable_source_is_not_irrelevance(self):
        self.record['coverage'][0]['state'] = 'NOT_RELEVANT'
        self.assertTrue(self.errors())

    def test_out_of_scope_source(self):
        self.record['coverage'][0]['source_ids'] = ['UNKNOWN-SOURCE']
        self.assertTrue(self.errors())

    def test_recorded_requires_separate_synthesis(self):
        self.record['synthesis'] = None
        self.assertTrue(self.errors())
        self.record['reading_status'] = 'IN_PROGRESS'
        self.assertEqual(self.errors(), [])

    def test_gates_cannot_be_granted(self):
        original = copy.deepcopy(self.record)
        for group in ('promotion_allowed', 'manual_gates'):
            for key in original[group]:
                with self.subTest(group=group, key=key):
                    self.record = copy.deepcopy(original)
                    self.record[group][key] = True if group == 'promotion_allowed' else 'PASS'
                    self.assertTrue(self.errors())
        for key, value in [('release_status', 'RELEASED'), ('review_state', 'ACCEPTED'),
                           ('independent_review_status', 'COMPLETE'), ('accepted_edges', ['EDGE']),
                           ('supports_models', ['MODEL'])]:
            with self.subTest(key=key):
                self.record = copy.deepcopy(original)
                self.record[key] = value
                self.assertTrue(self.errors())

    def test_attribution_is_not_authenticated(self):
        self.record['record_provenance'] = 'REAL_RECORD'
        self.record['author']['author_type'] = 'HUMAN'
        self.assertEqual(self.errors(), [])  # Labels never authenticate a person.
        self.record['author']['attribution_status'] = 'VERIFIED'
        self.assertTrue(self.errors())

    def test_closed_contract(self):
        self.record['assessments'] = []
        self.assertTrue(self.errors())

    def test_ambiguous_json_rejected(self):
        for raw in (b'{"a":1,"a":2}', b'{"a":NaN}', b'{"a":Infinity}', b'bad', b'\xff'):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                validator.read_json(raw)

    def test_cli_is_read_only_on_success_and_failure(self):
        protected = [PACKET, FIXTURE, ROOT / 'references/akashicomni/trusted-verifications-v0.5.0.json']
        before = {p: p.read_bytes() for p in protected}
        with tempfile.TemporaryDirectory() as directory:
            record = Path(directory) / 'record.json'
            record.write_bytes(FIXTURE.read_bytes())
            for valid in (True, False):
                if not valid:
                    record.write_text('{"invalid":true}')
                saved = record.read_bytes()
                result = subprocess.run([sys.executable, str(SCRIPT), str(record), str(PACKET)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0 if valid else 1, result.stdout + result.stderr)
                if valid:
                    self.assertIn('UNRELEASED; REVIEW_REQUIRED', result.stdout)
                    self.assertIn('remain PENDING', result.stdout)
                self.assertEqual(record.read_bytes(), saved)
        self.assertEqual({p: p.read_bytes() for p in protected}, before)


if __name__ == '__main__':
    unittest.main()
