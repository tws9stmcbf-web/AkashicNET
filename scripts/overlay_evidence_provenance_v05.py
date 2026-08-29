#!/usr/bin/env python3
"""Add metadata-only evidence/provenance scores to knowledge graph v0.4."""
from __future__ import annotations
import csv, json
from pathlib import Path

BASE=Path('data/knowledge-graph-v0.4.json')
LEDGER=Path('references/community/drive-canonicalisation-reconciliation-v0.1.csv')
OUT=Path('data/knowledge-graph-v0.5.json')
EXPECTED=29

STATUS_POINTS={
    'STAGE_B_ADVANCED':40,
    'REVIEWED_RETAINED':30,
    'REVIEW_REQUIRED':15,
    'UNRESOLVED_PROVENANCE':10,
}
CONF_POINTS={'HIGH':40,'MEDIUM_HIGH':30,'MEDIUM':20}


def basis_points(text:str)->int:
    t=text.lower()
    if 'stage-b' in t:
        return 20
    if 'title+size' in t or 'size evidence' in t:
        return 15
    if 'canonicalisation candidate ledger' in t:
        return 10
    return 5


def tier(score:int)->str:
    if score>=85: return 'E3_STRONG_METADATA_RELATIONSHIP'
    if score>=70: return 'E2_REVIEWED_METADATA_RELATIONSHIP'
    if score>=50: return 'E1_PROVISIONAL_METADATA_RELATIONSHIP'
    return 'E0_UNRESOLVED_OR_WEAK'

with BASE.open(encoding='utf-8') as f:
    graph=json.load(f)
with LEDGER.open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))
assert len(rows)==EXPECTED

by_family={r['family_id']:r for r in rows}
scored=[]
for node in graph['nodes']:
    if node.get('node_type')!='canonical_candidate_family':
        continue
    fid=node['family_id']
    r=by_family[fid]
    raw=(STATUS_POINTS.get(r['reconciled_status'],0)+
         CONF_POINTS.get(r['confidence'],10)+
         basis_points(r['basis']))
    cap=100
    if r['reconciled_status']=='UNRESOLVED_PROVENANCE': cap=45
    if r['reconciled_status']=='REVIEW_REQUIRED': cap=55
    score=min(raw,cap)
    record={
        'score':score,
        'tier':tier(score),
        'scope':'canonical_provenance_relationship_only',
        'status_component':STATUS_POINTS.get(r['reconciled_status'],0),
        'confidence_component':CONF_POINTS.get(r['confidence'],10),
        'basis_component':basis_points(r['basis']),
        'uncertainty_cap':cap,
        'basis':r['basis'],
        'source_ledger':str(LEDGER),
        'not_truth_score':True,
        'not_rights_score':True,
    }
    node['evidence_provenance']=record
    scored.append((fid,r['reconciled_status'],score,record['tier']))

assert len(scored)==EXPECTED, f'expected {EXPECTED} scored families, got {len(scored)}'
assert all(score<=45 for _,status,score,_ in scored if status=='UNRESOLVED_PROVENANCE')
assert all(score<=55 for _,status,score,_ in scored if status=='REVIEW_REQUIRED')
assert all(n.get('rights_status')=='UNKNOWN_UNVERIFIED' for n in graph['nodes'] if n.get('node_type')=='canonical_candidate_family')

counts={}
for _,_,_,t in scored: counts[t]=counts.get(t,0)+1

graph['schema_version']='0.5'
graph['evidence_provenance_scoring']={
    'scored_canonical_families':len(scored),
    'tier_counts':counts,
    'score_scope':'canonical/provenance relationship confidence only',
    'truth_inference_allowed':False,
    'rights_promotion_allowed':False,
    'integrity_pass':len(scored)==29,
}
graph['policy']['evidence_score_is_not_truth_score']=True
graph['policy']['evidence_score_does_not_change_rights']=True
graph['integrity']['release_integrity_pass']=bool(graph['integrity'].get('release_integrity_pass')) and graph['evidence_provenance_scoring']['integrity_pass']
OUT.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(graph['evidence_provenance_scoring'],sort_keys=True))
raise SystemExit(0 if graph['integrity']['release_integrity_pass'] else 2)
