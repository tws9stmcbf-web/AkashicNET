#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path

PRODUCTION=Path('references/community/drive-rights-provenance-ledger.csv')
TRIAGE=Path('references/community/rights-candidate-triage-v0.37.csv')


def load(path):
    with path.open(encoding='utf-8',newline='') as f: return list(csv.DictReader(f))


def next_action(row):
    state=row.get('public_status','UNKNOWN_UNVERIFIED')
    if state=='PUBLIC_VERIFIED': return 'REVERIFY_R4_AND_EXPIRY'
    if row.get('provisional_ladder_state')=='R1_WORK_LEVEL_CANDIDATE': return 'ESTABLISH_EXACT_MANIFESTATION_R2'
    return 'GATHER_RIGHTS_EVIDENCE'


def main():
    p=argparse.ArgumentParser(description='AkashicNET read-only rights review console v0.38')
    p.add_argument('--status',default='all',choices=['all','UNKNOWN_UNVERIFIED','PUBLIC_VERIFIED'])
    a=p.parse_args()
    prod=load(PRODUCTION); triage=load(TRIAGE)
    queue=[]
    for r in prod:
        item={
            'record_type':'production_scope','id':r['audit_id'],'label':r['scope'],
            'public_status':r['public_status'],'manifest_eligible':r['public_manifest_eligible'],
            'rights_basis':r['rights_basis'],'provenance_evidence':r['provenance_evidence'],
            'next_action':next_action(r),'can_auto_promote':False,
        }
        queue.append(item)
    for r in triage:
        item={
            'record_type':'real_candidate','id':r['candidate_id'],'family_id':r['family_id'],'label':r['canonical_label'],
            'provisional_ladder_state':r['provisional_ladder_state'],'public_status':r['public_status'],
            'manifest_eligible':r['public_manifest_eligible'],'manifestation_identified':r['manifestation_identified'],
            'blocker':r['blocker'],'next_action':next_action(r),'can_auto_promote':False,
        }
        queue.append(item)
    if a.status!='all': queue=[x for x in queue if x['public_status']==a.status]
    out={
        'console':'AKASHICNET_RIGHTS_REVIEW','version':'0.38','read_only':True,
        'promotion_requires_explicit_review':True,'automatic_rights_promotion':False,
        'summary':{
            'records':len(queue),'public_verified':sum(x['public_status']=='PUBLIC_VERIFIED' for x in queue),
            'unknown_unverified':sum(x['public_status']=='UNKNOWN_UNVERIFIED' for x in queue),
            'r1_candidates':sum(x.get('provisional_ladder_state')=='R1_WORK_LEVEL_CANDIDATE' for x in queue),
            'manifest_eligible':sum(x['manifest_eligible']=='YES' for x in queue),
        },
        'review_queue':queue,
        'guardrails':{'truth_inference':False,'scientific_evidence_promotion':False,'rights_from_accessibility':False,'rights_from_provenance_strength':False},
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
