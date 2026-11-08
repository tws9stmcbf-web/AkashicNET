"""Adversarial checks of the review-only IONS sample; no scientific validation."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('omni_ions', ROOT / 'scripts/validate_akashicomni_claim_review_v050.py')
omni = importlib.util.module_from_spec(spec)
spec.loader.exec_module(omni)
PACKET = ROOT / 'data/akashicomni/ions-public-claims-demo-v0.5.0.json'


class IonsDemoTests(unittest.TestCase):
    def setUp(self):
        self.packet = json.loads(PACKET.read_text(encoding='utf-8'))

    def test_real_packet_passes_without_reviews(self):
        self.assertEqual(omni.validate(self.packet), [])
        self.assertTrue(all(not c['assessments'] for c in self.packet['claims']))
        self.assertTrue(all(s['inspection_verification'] is None for s in self.packet['sources']))

    def test_each_promotion_stays_closed(self):
        for gate in self.packet['promotion_allowed']:
            with self.subTest(gate=gate):
                p = copy.deepcopy(self.packet)
                p['promotion_allowed'][gate] = True
                self.assertTrue(omni.validate(p))

    def test_release_and_evidence_state_mutations_fail(self):
        for key, value in [('release_status', 'RELEASED'), ('review_state', 'APPROVED'),
                           ('independent_review_status', 'COMPLETE'),
                           ('accepted_edges', ['EDGE-TELEPATHY']),
                           ('supports_models', ['NONLOCAL-MIND']), ('bq_id', 'BQ001')]:
            with self.subTest(key=key):
                p = copy.deepcopy(self.packet); p[key] = value
                self.assertTrue(omni.validate(p))

    def test_forged_source_attestation_fails_with_real_registry(self):
        self.packet['sources'][0]['access_status'] = 'FULL_TEXT_INSPECTED'
        self.packet['sources'][0]['inspection_verification'] = {
            'status': 'HUMAN_VERIFIED', 'verified_by': 'REVIEWER-FAKE',
            'record_url': 'https://example.org/not-a-review'}
        self.assertTrue(any('not repository-trusted' in e for e in omni.validate(self.packet)))

    def test_support_cannot_be_added_to_abstract_only_sources(self):
        self.packet['claims'][0]['assessments'] = [{
            'assessment_id': 'ASSESSMENT-TEST', 'reviewer_id': 'REVIEWER-TEST',
            'reviewer_type': 'AI', 'independence': 'NOT_ESTABLISHED',
            'independence_note': 'Adversarial in-memory mutation; not a real review.',
            'decision': 'SUPPORT', 'rationale': 'Invalid support mutation.',
            'source_locations': ['SOURCE-TSC2026'], 'provenance': 'REAL_REVIEW',
            'reviewer_verification': None}]
        self.assertTrue(any('SUPPORT requires' in e for e in omni.validate(self.packet)))

    def test_invented_comparison_fails(self):
        self.packet['claims'][0]['comparison']['status'] = 'RECORDED'
        self.assertTrue(any('independent-human pairs' in e for e in omni.validate(self.packet)))

    def test_wrong_editorial_digest_fails(self):
        self.packet['sources'][-1]['artifact']['sha256'] = '0' * 64
        self.assertTrue(any('digest mismatch' in e for e in omni.validate(self.packet)))

    def test_primary_source_cannot_replace_editorial_lineage(self):
        self.packet['claims'][0]['lineage_source_id'] = 'SOURCE-TSC2026'
        self.assertTrue(any('lineage' in e for e in omni.validate(self.packet)))

    def test_dangling_source_reference_fails(self):
        self.packet['claims'][0]['source_ids'].append('SOURCE-NOT-FOUND')
        self.assertTrue(any('unknown source reference' in e for e in omni.validate(self.packet)))

    def test_uninspected_source_cannot_keep_supporting_observations(self):
        self.packet['sources'][0]['access_status'] = 'NOT_REINSPECTED'
        self.assertTrue(any('reinspect sources' in e for e in omni.validate(self.packet)))

    def test_private_row_payload_is_outside_contract(self):
        self.packet['participant_observations'] = [{'participant_id': 'TEST-ONLY'}]
        self.assertTrue(omni.validate(self.packet))

    def test_unknown_mechanism_proof_field_fails(self):
        self.packet['claims'][0]['mechanism_verified'] = True
        self.assertTrue(omni.validate(self.packet))


if __name__ == '__main__':
    unittest.main()
