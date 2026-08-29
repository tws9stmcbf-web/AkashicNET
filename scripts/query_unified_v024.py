#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess

VALID_DOMAINS={'all','reddit','library'}
VALID_STATES={'all','accepted','hold'}


def decision_of(r):
    hop=r.get('concept_hop') or {}
    d=hop.get('decision') or hop.get('review_state')
    if d in {'ACCEPT','ACCEPTED'}: return 'ACCEPT'
    if d in {'HOLD','REVIEW_REQUIRED','PROVISIONAL'}: return 'HOLD'
    if d=='REJECT': return 'REJECT'
    if r.get('query_path')=='canonical_family_label': return 'DIRECT_METADATA_LOOKUP'
    return 'UNSPECIFIED'


def main():
    p=argparse.ArgumentParser(description='AkashicNET unified retrieval contract v0.24')
    p.add_argument('query')
    p.add_argument('--domain',choices=sorted(VALID_DOMAINS),default='all')
    p.add_argument('--state',choices=sorted(VALID_STATES),default='all',help='semantic edge state; direct metadata lookups remain visible unless --state hold')
    p.add_argument('--limit',type=int,default=100)
    a=p.parse_args()
    if a.limit < 1: p.error('--limit must be >= 1')

    base=json.loads(subprocess.check_output(['python','scripts/query_ranked_v023.py',a.query],text=True))
    rows=[]
    for r in base['results']:
        decision=decision_of(r)
        if a.domain!='all' and r.get('domain')!=a.domain: continue
        if a.state=='accepted' and decision not in {'ACCEPT','DIRECT_METADATA_LOOKUP'}: continue
        if a.state=='hold' and decision!='HOLD': continue
        x=dict(r)
        x['semantic_decision']=decision
        x['contract_guards']={
            'ranking_changes_semantic_decision':False,
            'not_truth_claim':True,
            'not_scientific_evidence_claim':True,
            'not_rights_clearance_claim':True,
            'not_safety_or_efficacy_claim':True,
        }
        rows.append(x)

    total_before_limit=len(rows)
    rows=rows[:a.limit]
    counts={}
    tiers={}
    domains={}
    for r in rows:
        counts[r['semantic_decision']]=counts.get(r['semantic_decision'],0)+1
        t=r['evidence_profile']['provenance_tier']; tiers[t]=tiers.get(t,0)+1
        d=r.get('domain','unknown'); domains[d]=domains.get(d,0)+1

    out={
        'contract':'AKASHICNET_UNIFIED_RETRIEVAL','version':'0.24',
        'request':{'query':a.query,'domain':a.domain,'state':a.state,'limit':a.limit},
        'policy':{
            'archive_mode':'metadata_and_links_only',
            'truth_inference_allowed':False,
            'rights_promotion_allowed':False,
            'scientific_evidence_promotion_allowed':False,
            'ranking_scope':'provenance and retrieval support only',
            'ranking_changes_semantic_decision':False,
            'direct_metadata_lookup_is_not_semantic_acceptance':True,
            'hold_results_are_explicitly_addressable':True,
        },
        'summary':{
            'matched_concepts':base.get('matched_concepts',[]),
            'results_before_limit':total_before_limit,
            'results_returned':len(rows),
            'semantic_decision_counts':counts,
            'provenance_tier_counts':tiers,
            'domain_counts':domains,
        },
        'result_schema':{
            'semantic_decision':'ACCEPT | HOLD | REJECT | DIRECT_METADATA_LOOKUP | UNSPECIFIED',
            'provenance_tier':'P3_SHA256_IDENTITY_PROVENANCE | P2_MANIFESTATION_PROVENANCE | P1_REVIEWED_TOPICAL | P0_TOPICAL_CANDIDATE',
            'result_order':'descending provenance tier; deterministic tie-break inherited from v0.23',
        },
        'results':rows,
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
