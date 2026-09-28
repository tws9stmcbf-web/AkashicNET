"""Mutation checks plus synthetic reviewer fixtures; no real review is claimed."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('omni', ROOT / 'scripts/validate_akashicomni_claim_review_v050.py')
omni = importlib.util.module_from_spec(spec)
spec.loader.exec_module(omni)


class ClaimReviewTests(unittest.TestCase):
    def setUp(self):
        self.packet = json.loads(omni.PILOT.read_text())

    def test_pilot_is_valid_but_unreleased(self):
        self.assertEqual(omni.validate(self.packet), [])
        self.assertEqual(self.packet['release_status'], 'UNRELEASED')
        self.assertTrue(all(not c['assessments'] for c in self.packet['claims']))

    def test_each_required_field_is_required(self):
        containers = [self.packet, self.packet['claims'][0], self.packet['sources'][0], self.packet['promotion_allowed']]
        for container in containers:
            for key in list(container):
                with self.subTest(key=key):
                    value = container.pop(key)
                    self.assertTrue(omni.validate(self.packet))
                    container[key] = value

    def test_promotions_and_unknown_fields_fail_closed(self):
        mutations = [('release_status','RELEASED'), ('review_state','APPROVED'),
                     ('independent_review_status','COMPLETE'), ('framework_baseline','0.5.0'),
                     ('supports_models',['MODEL-1']), ('accepted_edges',['EDGE-1']),
                     ('bq_id','BQ011'), ('truth_score',0.9)]
        for key, value in mutations:
            with self.subTest(key=key):
                p = copy.deepcopy(self.packet); p[key] = value
                self.assertTrue(omni.validate(p))
        for key in self.packet['promotion_allowed']:
            p = copy.deepcopy(self.packet); p['promotion_allowed'][key] = True
            self.assertTrue(omni.validate(p))

    def test_claim_resolution_rejected(self):
        for key,value in [('status','RESOLVED'),('decision','ACCEPTED'),('kind','ESTABLISHED_FACT')]:
            p=copy.deepcopy(self.packet); p['claims'][0][key]=value
            self.assertTrue(omni.validate(p))

    def test_duplicate_and_missing_source(self):
        p=copy.deepcopy(self.packet); p['claims'].append(copy.deepcopy(p['claims'][0]))
        self.assertTrue(omni.validate(p))
        p=copy.deepcopy(self.packet); p['sources'].append(copy.deepcopy(p['sources'][0]))
        self.assertTrue(omni.validate(p))
        self.packet['claims'][0]['source_ids']=['SOURCE-ABSENT']
        self.assertTrue(omni.validate(self.packet))

    def test_missing_evidence_cannot_become_support(self):
        self.packet['claims'][0]['supporting_observations']=['Uninspected source supposedly confirms it.']
        self.assertTrue(omni.validate(self.packet))
        self.packet['claims'][0]['supporting_observations']=[]
        self.packet['claims'][0]['missing_evidence']=[]
        self.assertTrue(omni.validate(self.packet))

    def test_revision_date_and_sequence(self):
        revision=self.packet['claims'][0]['revision_history'][0]
        revision['revision']=2
        self.assertTrue(omni.validate(self.packet))
        revision['revision']=1; revision['date']='2026-02-30'
        self.assertTrue(omni.validate(self.packet))

    @staticmethod
    def verification():
        return {'status':'HUMAN_VERIFIED', 'verified_by':'TEST-VERIFIER',
                'record_url':'https://example.invalid/test-only-verification'}

    def test_synthetic_humans_never_qualify_or_validate(self):
        c = self.add_simulated_verified_reviews()
        for a in c['assessments']:
            a['provenance'] = 'SYNTHETIC_FIXTURE'
        self.assertEqual(omni.compare_assessments(c['assessments'], self.packet, c), [])
        self.assertTrue(any('synthetic fixtures' in e for e in omni.validate(self.packet)))
        c['comparison'] = {'status':'PENDING','pairs':[],'agreements':[],'disagreements':[]}
        for a in c['assessments']:
            a['reviewer_verification'] = None
        self.assertTrue(any('synthetic fixtures' in e for e in omni.validate(self.packet)))

    def test_missing_or_unverified_reviewer_provenance_fails_closed(self):
        c = self.add_simulated_verified_reviews()
        c['assessments'][0]['reviewer_verification'] = None
        self.assertEqual(omni.compare_assessments(c['assessments'], self.packet, c), [])
        self.assertTrue(omni.validate(self.packet))
        del c['assessments'][0]['provenance']
        self.assertEqual(omni.compare_assessments(c['assessments'], self.packet, c), [])
        self.assertTrue(omni.validate(self.packet))

    def test_self_verified_independence_rejected(self):
        c = self.add_simulated_verified_reviews()
        a = c['assessments'][0]
        a['reviewer_verification']['verified_by'] = a['reviewer_id']
        self.assertTrue(any('self-verify' in e for e in omni.validate(self.packet)))

    def test_support_requires_all_sources_inspected_and_human_verified(self):
        self.add_simulated_verified_reviews()
        baseline = copy.deepcopy(self.packet)
        for i in range(len(baseline['sources'])):
            for access in ('NOT_REINSPECTED', 'ABSTRACT_ONLY', 'FULL_TEXT_INSPECTED'):
                with self.subTest(source=i, access=access):
                    self.packet = copy.deepcopy(baseline)
                    source = self.packet['sources'][i]
                    source['access_status'] = access
                    source['inspection_verification'] = None
                    self.assertTrue(any('SUPPORT requires' in e for e in omni.validate(self.packet)))
        self.packet = baseline
        self.mock_trusted_records()
        self.assertEqual(omni.validate(self.packet), [])

    def test_inspection_attestation_cannot_override_uninspected_status(self):
        self.add_simulated_verified_reviews()
        self.packet['sources'][0]['access_status'] = 'NOT_REINSPECTED'
        self.assertTrue(any('SUPPORT requires' in e for e in omni.validate(self.packet)))

    def test_privacy_and_cultural_authority_required_false(self):
        for key in ('privacy', 'cultural_authority'):
            for mutation in ('missing', 'enabled'):
                with self.subTest(gate=key, mutation=mutation):
                    p = copy.deepcopy(self.packet)
                    if mutation == 'missing':
                        del p['promotion_allowed'][key]
                    else:
                        p['promotion_allowed'][key] = True
                    self.assertTrue(omni.validate(p))

    def test_lineage_must_resolve_to_editorial_artifact(self):
        for value in ('SOURCE-ABSENT', 'SOURCE-HAGELIN-1999'):
            p = copy.deepcopy(self.packet)
            p['claims'][0]['lineage_source_id'] = value
            self.assertTrue(any('lineage must reference' in e for e in omni.validate(p)))
        self.packet['sources'].pop()
        self.assertTrue(omni.validate(self.packet))

    def test_editorial_artifact_missing_or_tampered_rejected(self):
        editorial = self.packet['sources'][1]
        for key in ('repository_path', 'sha256'):
            with self.subTest(missing=key):
                value = editorial['artifact'].pop(key)
                self.assertTrue(omni.validate(self.packet))
                editorial['artifact'][key] = value
        p = copy.deepcopy(self.packet)
        p['sources'][1]['artifact']['repository_path'] = 'references/akashicomni/missing.md'
        self.assertTrue(any('missing' in e for e in omni.validate(p)))
        p = copy.deepcopy(self.packet)
        p['sources'][1]['artifact']['sha256'] = '0' * 64
        self.assertTrue(any('digest mismatch' in e for e in omni.validate(p)))
        original = Path.read_bytes
        def tamper(path):
            return original(path) + b' altered editorial input'
        with patch.object(Path, 'read_bytes', tamper):
            self.assertTrue(any('digest mismatch' in e for e in omni.validate(self.packet)))

    def add_simulated_verified_reviews(self):
        """Fabricate packet labels only; these MUST fail against the real registry."""
        for source in self.packet["sources"]:
            source["access_status"] = "FULL_TEXT_INSPECTED"
            source["inspection_verification"] = self.verification()
        c=self.packet['claims'][0]
        c['assessments']=[{'assessment_id':'TEST-A'+str(i),'reviewer_id':'TEST-R'+str(i),
            'reviewer_type':'HUMAN','independence':'DECLARED_INDEPENDENT',
            'provenance':'REAL_REVIEW', 'reviewer_verification':self.verification(),
            'independence_note':'Synthetic test fixture only.', 'decision':d,
            'rationale':'Synthetic rationale, not a scientific assessment.',
            'source_locations':['Synthetic test locator.']}
            for i,d in enumerate(['SUPPORT','CHALLENGE'])]
        c['comparison']={'status':'RECORDED','pairs':[{'assessment_ids':['TEST-A0','TEST-A1'], 'decision_agreement':False}],
                         'agreements':[], 'disagreements':['The synthetic decisions differ.']}
        return c

    def mock_trusted_records(self):
        """Isolated positive control, never a production registry or real review."""
        records = {
            'reviewer_attestations': [omni.verification_record(self.packet, claim=c, assessment=a)
                for c in self.packet['claims'] for a in c['assessments']],
            'source_inspections': [omni.verification_record(self.packet, source=s)
                for s in self.packet['sources']],
        }
        mocked = patch.object(omni, 'load_verifications', return_value=records)
        mocked.start()
        self.addCleanup(mocked.stop)
        return records

    def test_relabeled_synthetic_reviewers_cannot_qualify(self):
        c = self.add_simulated_verified_reviews()
        # Isolate reviewer authentication from the source SUPPORT gate.
        for a in c['assessments']:
            a['decision'] = 'CHALLENGE'
        for source in self.packet['sources']:
            source['inspection_verification'] = None
        self.assertEqual(omni.compare_assessments(c['assessments'], self.packet, c), [])
        for status in ('RECORDED', 'PENDING'):
            c['comparison'] = {'status':status, 'pairs':[], 'agreements':[], 'disagreements':[]}
            self.assertTrue(any('reviewer attestation is not repository-trusted' in e
                                for e in omni.validate(self.packet)))

    def test_relabeled_source_inspections_cannot_enable_support(self):
        c = self.add_simulated_verified_reviews()
        c['assessments'] = c['assessments'][:1]
        c['assessments'][0]['reviewer_verification'] = None
        c['comparison'] = {'status':'PENDING', 'pairs':[], 'agreements':[], 'disagreements':[]}
        self.assertTrue(any('SUPPORT requires' in e for e in omni.validate(self.packet)))
        self.assertTrue(any('inspection attestation is not repository-trusted' in e
                            for e in omni.validate(self.packet)))

    def test_trusted_records_cannot_be_replayed_on_changed_subjects(self):
        c = self.add_simulated_verified_reviews()
        self.mock_trusted_records()
        baseline = copy.deepcopy(self.packet)
        mutations = [
            lambda p: p.update(packet_id='OTHER-PACKET'),
            lambda p: p['claims'][0].update(wording='A different claim.'),
            lambda p: p['claims'][0]['assessments'][0].update(reviewer_id='OTHER-REVIEWER'),
            lambda p: p['claims'][0]['assessments'][0].update(decision='CHALLENGE'),
            lambda p: p['claims'][0]['assessments'][0]['reviewer_verification'].update(
                verified_by='OTHER-VERIFIER'),
            lambda p: p['sources'][0].update(url='https://example.invalid/other-source'),
            lambda p: p['sources'][0].update(location='Other pages.'),
            lambda p: p['sources'][1]['artifact'].update(sha256='0' * 64),
        ]
        for mutate in mutations:
            p = copy.deepcopy(baseline)
            mutate(p)
            self.assertTrue(any('not repository-trusted' in e for e in omni.validate(p)))

    def test_missing_or_malformed_registry_fails_closed(self):
        c = self.add_simulated_verified_reviews()
        for contents in ('{}', '[]', 'not json', '{"reviewer_attestations":{},"source_inspections":[]}'):
            with patch.object(Path, 'read_text', return_value=contents):
                with self.assertRaises(ValueError):
                    omni.load_verifications()
                self.assertEqual(omni.compare_assessments(c['assessments'], self.packet, c), [])
        with patch.object(omni, 'VERIFICATIONS', ROOT / 'missing-registry.json'):
            self.assertTrue(any('trusted verification registry' in e for e in omni.validate(self.packet)))
            self.assertEqual(omni.compare_assessments(c['assessments'], self.packet, c), [])

    def test_comparison_preserves_disagreement(self):
        c=self.add_simulated_verified_reviews()
        self.mock_trusted_records()
        self.assertEqual(omni.validate(self.packet),[])
        c['comparison']['disagreements']=[]
        self.assertTrue(omni.validate(self.packet))

    def test_forged_agreement_and_reference_rejected(self):
        c=self.add_simulated_verified_reviews(); self.mock_trusted_records()
        c['comparison']['pairs'][0]['decision_agreement']=True
        self.assertTrue(omni.validate(self.packet))
        c['comparison']['pairs']=omni.compare_assessments(c['assessments'], self.packet, c)
        c['comparison']['pairs'][0]['assessment_ids'][0]='TEST-MISSING'
        self.assertTrue(omni.validate(self.packet))

    def test_same_reviewer_or_ai_does_not_supply_independence(self):
        c=self.add_simulated_verified_reviews(); c['assessments'][1]['reviewer_id']='TEST-R0'
        self.assertTrue(omni.validate(self.packet))
        c['assessments'][1]['reviewer_id']='TEST-R1'; c['assessments'][1]['reviewer_type']='AI'
        self.assertTrue(omni.validate(self.packet))
        c['assessments'][1]['independence']='NOT_ESTABLISHED'
        self.assertTrue(omni.validate(self.packet))

    def test_pending_comparison_cannot_contain_results(self):
        c=self.add_simulated_verified_reviews(); c['comparison']['status']='PENDING'
        self.assertTrue(omni.validate(self.packet))

    def test_agreement_is_not_framework_release(self):
        c=self.add_simulated_verified_reviews(); c['assessments'][1]['decision']='SUPPORT'
        self.mock_trusted_records()
        c['comparison']={'status':'RECORDED','pairs':omni.compare_assessments(c['assessments'], self.packet, c),
                         'agreements':['Synthetic decisions agree.'],'disagreements':[]}
        self.assertEqual(omni.validate(self.packet),[])
        self.packet['release_status']='RELEASED'
        self.assertTrue(omni.validate(self.packet))


if __name__ == '__main__':
    unittest.main()
