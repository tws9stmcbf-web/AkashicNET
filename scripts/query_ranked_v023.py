#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path

DEDUP=Path('data/dedup-retrieval-view-v0.17.json')
LEVELS={
    'P0_TOPICAL_CANDIDATE':0,
    'P1_REVIEWED_TOPICAL':1,
    'P2_MANIFESTATION_PROVENANCE':2,
    'P3_SHA256_IDENTITY_PROVENANCE':3,
}

def profile(result):
    accepted=(result.get('concept_hop') or {}).get('review_state')=='ACCEPTED'
    direct=result.get('query_path')=='canonical_family_label'
    units=result.get('logical_retrieval_units',[])
    sha_units=[u for u in units if u.get('collapse_basis')=='SHA256_MATCH_VERIFIED']
    if sha_units:
        level='P3_SHA256_IDENTITY_PROVENANCE'
        basis='manifestation provenance includes SHA-256 verified byte-identity group(s)'
    elif units:
        level='P2_MANIFESTATION_PROVENANCE'
        basis='physical manifestation provenance is available'
    elif accepted:
        level='P1_REVIEWED_TOPICAL'
        basis='reviewed topical relation; no manifestation provenance attached in current view'
    else:
        level='P0_TOPICAL_CANDIDATE'
        basis='unaccepted topical candidate or direct metadata-only lookup'
    return {
        'provenance_rank':LEVELS[level],
        'provenance_tier':level,
        'ranking_basis':basis,
        'direct_canonical_lookup':direct,
        'logical_unit_count':len(units),
        'physical_manifestation_count':sum(u.get('physical_manifestation_count',0) for u in units),
        'sha256_verified_logical_units':len(sha_units),
        'not_truth_score':True,
        'not_scientific_evidence_score':True,
        'not_rights_score':True,
        'not_safety_or_efficacy_score':True,
    }

def main():
    p=argparse.ArgumentParser(); p.add_argument('query'); p.add_argument('--accepted-only',action='store_true'); a=p.parse_args()
    cmd=['python','scripts/query_multihop_v022.py',a.query]
    if a.accepted_only: cmd.append('--accepted-only')
    base=json.loads(subprocess.check_output(cmd,text=True))
    ranked=[]; seen=set()
    for r in base['results']:
        x=dict(r); x['evidence_profile']=profile(r); ranked.append(x)
        src=x.get('source',{}); seen.add((x.get('domain'),src.get('family_id') or src.get('ref'),x.get('concept')))

    # Direct canonical-family / manifestation fallback is retrieval only. It does
    # not create a semantic concept edge and therefore cannot increase topical evidence.
    dedup=json.load(DEDUP.open(encoding='utf-8'))
    q=a.query.lower().strip()
    for u in dedup['retrieval_units']:
        labels=' '.join(u.get('labels',[])).lower()
        fams=' '.join(u.get('family_ids',[])).lower()
        if not q or (q not in labels and q not in fams):
            continue
        r={
            'domain':'library','query_path':'canonical_family_label','concept':None,
            'source':{'type':'canonical_family','family_id':u.get('family_ids',[None])[0],'label':u.get('labels',[None])[0]},
            'logical_retrieval_units':[u],
            'retrieval_resolution':'DEDUP_LOGICAL_UNITS_RESOLVED',
            'not_semantic_inference':True,
        }
        key=('library',r['source']['family_id'],None,u['retrieval_unit_id'])
        if key in seen: continue
        seen.add(key); r['evidence_profile']=profile(r); ranked.append(r)

    ranked.sort(key=lambda r:(-r['evidence_profile']['provenance_rank'], r.get('domain',''), str(r.get('source',{}))))
    out={
        'version':'0.23','query':a.query,'accepted_only':a.accepted_only,'matched_concepts':base['matched_concepts'],
        'result_count':len(ranked),'ranking_scope':'provenance and retrieval support only',
        'ranking_order':['P3_SHA256_IDENTITY_PROVENANCE','P2_MANIFESTATION_PROVENANCE','P1_REVIEWED_TOPICAL','P0_TOPICAL_CANDIDATE'],
        'truth_inference_allowed':False,'rights_promotion_allowed':False,'scientific_evidence_promotion_allowed':False,
        'ranking_must_not_be_interpreted_as_truth_evidence_safety_efficacy_or_rights':True,
        'semantic_decisions_changed_by_ranking':False,
        'results':ranked,
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
