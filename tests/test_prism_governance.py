"""Synthetic gate regressions; dispositions below are not real approvals."""
import copy
import itertools
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_prism_connections import ROOT, SCRIPT, validator

FIXTURE = ROOT / 'tests/fixtures/prism/cultural-privacy-hold.json'


class GovernanceTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(FIXTURE.read_text())

    def assert_validity(self, record, expected):
        self.assertEqual(validator.VALIDATOR.is_valid(record), expected)
        self.assertEqual(not validator.validate(record), expected)

    def candidate(self):
        record = copy.deepcopy(self.record)
        record['governance'].update(publication_status='review_candidate',
                                    privacy_disposition='cleared',
                                    cultural_review_status='cleared')
        record['perspectives'][0]['cultural_authority'].update(
            community_or_lineage='Synthetic community, not a real attribution',
            speaker_position='Synthetic test role', authority_to_share='confirmed')
        return record

    def pending_event(self, gate, event_id='ASSESS-TEST'):
        return {
            'assessment_event_id': event_id,
            'recorded_at': '2026-09-27T07:00:00Z',
            'affected_ref': 'EPI-TEST',
            'input_type': 'cultural_authority_review' if gate == 'cultural_authority'
                          else 'other',
            'independence_status': 'unknown',
            'prior_evidence_lane': None,
            'new_evidence_lane': 'interpretation',
            'effect': 'no_change',
            'rationale': 'Synthetic pending gate.',
            'uncertainty': 'Test fixture only.',
            'reviewer_role': 'synthetic',
            'source_ids': [],
            'gates_pending': [gate],
        }

    def test_current_event_gate_overrides_cleared_aggregate(self):
        for gate in ('privacy', 'cultural_authority'):
            with self.subTest(gate=gate):
                record = self.candidate()
                record['assessment_history'] = [self.pending_event(gate)]
                self.assertTrue(validator.VALIDATOR.is_valid(record))
                self.assertIn(gate, ' '.join(validator.validate(record)))
                record['governance']['publication_status'] = 'hold'
                self.assertEqual(validator.validate(record), [])

    def test_superseded_pending_event_requires_current_clearance(self):
        for gate in ('privacy', 'cultural_authority'):
            with self.subTest(gate=gate):
                record = self.candidate()
                successor = self.pending_event(gate, 'ASSESS-CLEAR')
                successor['gates_pending'] = []
                successor['gates_passed'] = [gate]
                successor['supersedes_event_id'] = 'ASSESS-TEST'
                record['assessment_history'] = [self.pending_event(gate), successor]
                self.assertEqual(validator.validate(record), [])
                del successor['gates_passed']
                self.assertIn(gate, ' '.join(validator.validate(record)))
                successor['gates_passed'] = [gate]
                record['assessment_history'].reverse()
                self.assertIn('ambiguous event supersession',
                              ' '.join(validator.validate(record)))

    def test_supersession_cannot_clear_another_reference(self):
        for gate in ('privacy', 'cultural_authority'):
            with self.subTest(gate=gate):
                record = self.candidate()
                other = copy.deepcopy(record['perspectives'][0])
                other['perspective_id'] = 'EPI-SECOND'
                record['perspectives'].append(other)
                pending = self.pending_event(gate)
                successor = self.pending_event(gate, 'ASSESS-CLEAR')
                successor.update(affected_ref='EPI-SECOND', gates_pending=[],
                                 gates_passed=[gate],
                                 supersedes_event_id=pending['assessment_event_id'])
                record['assessment_history'] = [pending, successor]
                before = copy.deepcopy(record)
                self.assertTrue(validator.VALIDATOR.is_valid(record))
                self.assertIn(gate, ' '.join(validator.validate(record)))
                self.assertEqual(record, before)
                with tempfile.TemporaryDirectory() as directory:
                    path = Path(directory) / 'cross-reference.json'
                    path.write_text(json.dumps(record))
                    result = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                                            capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn(gate, result.stdout)
                    self.assertNotIn('Traceback', result.stderr)
                # HOLD retains the unresolved history without granting clearance.
                record['governance']['publication_status'] = 'hold'
                self.assertEqual(validator.validate(record), [])
                # Clearance for the original reference remains structurally valid.
                record['governance']['publication_status'] = 'review_candidate'
                successor['affected_ref'] = pending['affected_ref']
                self.assertEqual(validator.validate(record), [])

    def test_pending_fixture_is_valid_without_mutation(self):
        before = copy.deepcopy(self.record)
        self.assert_validity(self.record, True)
        self.assertEqual(self.record, before)

    def test_privacy_disposition_required_even_without_cultural_scope(self):
        for value in ('missing', None, '', 'unknown', 'approved', False):
            record = self.candidate()
            record['perspectives'][0]['lens'] = 'philosophical'
            del record['perspectives'][0]['cultural_authority']
            record['governance']['cultural_review_required'] = False
            del record['governance']['cultural_review_status']
            if value == 'missing':
                del record['governance']['privacy_disposition']
            else:
                record['governance']['privacy_disposition'] = value
            self.assert_validity(record, False)

    def test_privacy_and_cultural_disposition_matrix(self):
        for publication, privacy, culture in itertools.product(
                ('hold', 'review_candidate'),
                ('review_required', 'restricted', 'cleared'),
                ('review_required', 'restricted', 'cleared')):
            with self.subTest(publication=publication, privacy=privacy, culture=culture):
                record = self.candidate()
                record['governance'].update(publication_status=publication,
                                            privacy_disposition=privacy,
                                            cultural_review_status=culture)
                self.assert_validity(record, publication == 'hold' or
                                     (privacy == culture == 'cleared'))

    def test_each_perspective_scope_requires_own_authority_and_review(self):
        scopes = [('lens', value) for value in ('cultural', 'shamanic', 'lineage')]
        scopes += [('evidence_lane', 'traditional_knowledge'),
                   ('claim_scope', 'communal_meaning'),
                   ('interpretive_modes', ['cultural_teaching'])]
        scopes += [('epistemic_basis', [value]) for value in
                   ('lineage_transmission', 'community_attestation', 'traditional_text')]
        for key, value in scopes:
            with self.subTest(key=key, value=value):
                record = copy.deepcopy(self.record)
                record['perspectives'][0]['lens'] = 'philosophical'
                record['perspectives'][0][key] = value
                self.assert_validity(record, True)
                for authority in ('missing', None, {}, {'authority_to_share': 'unknown'}):
                    bad = copy.deepcopy(record)
                    if authority == 'missing':
                        del bad['perspectives'][0]['cultural_authority']
                    else:
                        bad['perspectives'][0]['cultural_authority'] = authority
                    # A second attributed perspective cannot mask this omission.
                    other = copy.deepcopy(record['perspectives'][0])
                    other['perspective_id'] = 'EPI-SECOND'
                    bad['perspectives'].append(other)
                    self.assert_validity(bad, False)
                bad = copy.deepcopy(record)
                bad['governance']['cultural_review_required'] = False
                self.assert_validity(bad, False)
                del record['governance']['cultural_review_status']
                self.assert_validity(record, False)

    def test_record_scope_cannot_bypass_cultural_review(self):
        for scope in ('investigation', 'source', 'connection_lane', 'connection_domain',
                      'correspondence', 'state'):
            with self.subTest(scope=scope):
                record = copy.deepcopy(self.record)
                record['perspectives'][0]['lens'] = 'philosophical'
                if scope == 'investigation':
                    record['investigation']['classification'] = 'cultural_or_traditional_claim'
                elif scope == 'source':
                    record['source_network']['nodes'][0]['source_type'] = 'traditional_teaching'
                elif scope == 'connection_lane':
                    record['connections'][0]['evidence_lane'] = 'traditional_knowledge'
                elif scope == 'connection_domain':
                    record['connections'][0]['domains'] = ['indigenous_or_traditional']
                elif scope == 'correspondence':
                    record['comparative_correspondences'] = [{
                        'correspondence_id': 'CORR-TEST',
                        'terms': [{'term': 'A', 'context': 'Synthetic A'},
                                  {'term': 'B', 'context': 'Synthetic B'}],
                        'relation': 'hypothesised_correspondence', 'status': 'unresolved',
                        'cultural_authority_status': 'unknown',
                        'non_equivalence_note': 'Not equivalent.', 'source_ids': ['SRC-TEST'],
                    }]
                else:
                    record['state_observations'] = [{
                        'state_observation_id': 'STATE-TEST', 'state': 'ritual_trance',
                        'report_basis': 'traditional_teaching', 'phenomenology': ['Synthetic'],
                        'source_ids': ['SRC-TEST'], 'uncertainty': 'Unresolved.',
                    }]
                self.assert_validity(record, True)
                bad = copy.deepcopy(record)
                bad['governance']['cultural_review_required'] = False
                self.assert_validity(bad, False)
                del record['perspectives'][0]['cultural_authority']
                self.assert_validity(record, False)

    def test_authority_matrix_and_unknown_context_prevent_advancement(self):
        for status, publication in itertools.product(
                ('confirmed', 'public_with_attribution', 'review_required', 'restricted', 'unknown'),
                ('hold', 'review_candidate')):
            record = self.candidate()
            record['governance']['publication_status'] = publication
            record['perspectives'][0]['cultural_authority']['authority_to_share'] = status
            self.assert_validity(record, publication == 'hold' or
                                 status in ('confirmed', 'public_with_attribution'))
        for field in ('community_or_lineage', 'speaker_position', 'authority_to_share'):
            for value in ('missing', None, '', ' \t'):
                record = self.candidate()
                if value == 'missing':
                    del record['perspectives'][0]['cultural_authority'][field]
                else:
                    record['perspectives'][0]['cultural_authority'][field] = value
                self.assert_validity(record, False)

    def test_non_cultural_candidate_does_not_require_invented_authority(self):
        record = self.candidate()
        record['perspectives'][0]['lens'] = 'philosophical'
        del record['perspectives'][0]['cultural_authority']
        record['governance']['cultural_review_required'] = False
        del record['governance']['cultural_review_status']
        self.assert_validity(record, True)
        record['governance']['privacy_disposition'] = 'review_required'
        self.assert_validity(record, False)

    def test_explicit_authority_also_requires_cultural_review(self):
        record = self.candidate()
        record['perspectives'][0]['lens'] = 'philosophical'
        record['governance']['cultural_review_required'] = False
        self.assert_validity(record, False)

    def test_cli_accepts_hold_and_rejects_pending_candidate(self):
        result = subprocess.run([sys.executable, str(SCRIPT), str(FIXTURE)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.record['governance']['publication_status'] = 'review_candidate'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'invalid.json'
            path.write_text(json.dumps(self.record))
            result = subprocess.run([sys.executable, str(SCRIPT), str(path)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn('ERROR:', result.stdout)
            self.assertNotIn('Traceback', result.stderr)


if __name__ == '__main__':
    unittest.main()
