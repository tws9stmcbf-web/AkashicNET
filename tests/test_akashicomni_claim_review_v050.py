"""Mutation checks plus synthetic reviewer fixtures; no real review is claimed."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

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

    def add_synthetic_reviews(self):
        c=self.packet['claims'][0]
        c['assessments']=[{'assessment_id':'TEST-A'+str(i),'reviewer_id':'TEST-R'+str(i),
            'reviewer_type':'HUMAN','independence':'DECLARED_INDEPENDENT',
            'independence_note':'Synthetic test fixture only.', 'decision':d,
            'rationale':'Synthetic rationale, not a scientific assessment.',
            'source_locations':['Synthetic test locator.']}
            for i,d in enumerate(['SUPPORT','CHALLENGE'])]
        c['comparison']={'status':'RECORDED','pairs':omni.compare_assessments(c['assessments']),
                         'agreements':[], 'disagreements':['The synthetic decisions differ.']}
        return c

    def test_comparison_preserves_disagreement(self):
        c=self.add_synthetic_reviews()
        self.assertEqual(omni.validate(self.packet),[])
        c['comparison']['disagreements']=[]
        self.assertTrue(omni.validate(self.packet))

    def test_forged_agreement_and_reference_rejected(self):
        c=self.add_synthetic_reviews(); c['comparison']['pairs'][0]['decision_agreement']=True
        self.assertTrue(omni.validate(self.packet))
        c['comparison']['pairs']=omni.compare_assessments(c['assessments'])
        c['comparison']['pairs'][0]['assessment_ids'][0]='TEST-MISSING'
        self.assertTrue(omni.validate(self.packet))

    def test_same_reviewer_or_ai_does_not_supply_independence(self):
        c=self.add_synthetic_reviews(); c['assessments'][1]['reviewer_id']='TEST-R0'
        self.assertTrue(omni.validate(self.packet))
        c['assessments'][1]['reviewer_id']='TEST-R1'; c['assessments'][1]['reviewer_type']='AI'
        self.assertTrue(omni.validate(self.packet))
        c['assessments'][1]['independence']='NOT_ESTABLISHED'
        self.assertTrue(omni.validate(self.packet))

    def test_pending_comparison_cannot_contain_results(self):
        c=self.add_synthetic_reviews(); c['comparison']['status']='PENDING'
        self.assertTrue(omni.validate(self.packet))

    def test_agreement_is_not_framework_release(self):
        c=self.add_synthetic_reviews(); c['assessments'][1]['decision']='SUPPORT'
        c['comparison']={'status':'RECORDED','pairs':omni.compare_assessments(c['assessments']),
                         'agreements':['Synthetic decisions agree.'],'disagreements':[]}
        self.assertEqual(omni.validate(self.packet),[])
        self.packet['release_status']='RELEASED'
        self.assertTrue(omni.validate(self.packet))


if __name__ == '__main__':
    unittest.main()
