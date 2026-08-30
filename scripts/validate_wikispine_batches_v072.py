#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REF=ROOT/'references'/'community'

def load(name): return json.loads((REF/name).read_text(encoding='utf-8'))

pilot=load('wikispine-seed-v0.7.0.json')['records']
a=load('wikispine-batch-a-v0.7.1.json')['records']
b=load('wikispine-batch-b-v0.7.1.json')['records']
updates=load('wikispine-resolution-updates-v0.7.2.json')['records']
c=load('wikispine-batch-c-v0.7.2.json')['records']
d=load('wikispine-batch-d-v0.7.2.json')['records']
cp=load('wikispine-expansion-checkpoint-v0.7.2.json')

state={r['akashic_concept']:dict(r) for r in pilot+a+b}
assert len(state)==20
for r in updates:
    assert r['akashic_concept'] in state
    assert state[r['akashic_concept']]['resolution_state']=='PENDING_API_RESOLUTION'
    state[r['akashic_concept']]=dict(r)
for r in c+d:
    assert r['akashic_concept'] not in state
    state[r['akashic_concept']]=dict(r)

assert len(state)==cp['unique_seeds']==33
resolved=[r for r in state.values() if r['resolution_state']=='RESOLVED_HIGH_PRECISION']
pending=[r for r in state.values() if r['resolution_state']!='RESOLVED_HIGH_PRECISION']
assert len(resolved)==cp['resolved_high_precision']==30
assert len(pending)==cp['pending_resolution_or_disambiguation']==3
assert len(updates)==cp['resolution_updates_applied']==3

qids=[r['wikidata_qid'] for r in resolved]
assert all(q and q.startswith('Q') and q[1:].isdigit() for q in qids)
assert len(set(qids))==len(qids)
assert cp['duplicate_resolved_qids']==0
assert all(r.get('wikidata_qid') is None for r in pending)

assert cp['reference_class']=='REFERENCE_ENCYCLOPEDIA'
assert cp['max_hops']==2
assert cp['arbitrary_recursive_crawl'] is False
assert cp['full_article_body_ingestion_default'] is False
assert cp['candidate_edges_default']=='HOLD'
assert cp['truth_inference_allowed'] is False
assert cp['rights_promotion_allowed'] is False
assert cp['scientific_evidence_promotion_allowed'] is False
assert cp['drive_access_performed'] is False

print('AKASHICNET v0.7.2 WIKISPINE BATCH PASS', {
 'unique_seeds':len(state), 'resolved_high_precision':len(resolved),
 'pending':len(pending), 'resolution_updates':len(updates),
 'duplicate_resolved_qids':0, 'max_hops':2, 'drive_access_performed':False})
