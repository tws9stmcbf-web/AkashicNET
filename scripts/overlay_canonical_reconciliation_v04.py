#!/usr/bin/env python3
"""Overlay the reconciled 29-family canonicalisation ledger onto graph v0.3."""
from __future__ import annotations
import csv, json
from pathlib import Path

BASE=Path('data/knowledge-graph-v0.3.json')
LEDGER=Path('references/community/drive-canonicalisation-reconciliation-v0.1.csv')
OUT=Path('data/knowledge-graph-v0.4.json')
EXPECTED=29

with BASE.open(encoding='utf-8') as f:
    graph=json.load(f)
with LEDGER.open(encoding='utf-8-sig', newline='') as f:
    rows=list(csv.DictReader(f))

assert len(rows)==EXPECTED, f'expected {EXPECTED} canonical rows, got {len(rows)}'
ids=[r['family_id'] for r in rows]
assert len(ids)==len(set(ids)), 'duplicate canonical family IDs'

nodes=graph['nodes']
edges=graph['edges']
for r in rows:
    nid='canonical:'+r['family_id']
    nodes.append({
        'node_id':nid,
        'node_type':'canonical_candidate_family',
        'family_id':r['family_id'],
        'label':r['canonical_label'],
        'legacy_status':r['legacy_status'],
        'reconciled_status':r['reconciled_status'],
        'authoritative_disposition':r['authoritative_disposition'],
        'confidence':r['confidence'].lower(),
        'basis':r['basis'],
        'notes':r['notes'],
        'review_state': ('unresolved' if r['reconciled_status']=='UNRESOLVED_PROVENANCE' else 'provisional' if r['reconciled_status']=='REVIEW_REQUIRED' else 'accepted'),
        'rights_status':'UNKNOWN_UNVERIFIED'
    })

counts={}
for r in rows:
    counts[r['reconciled_status']]=counts.get(r['reconciled_status'],0)+1

node_ids=[n['node_id'] for n in nodes]
graph['schema_version']='0.4'
graph['canonical_reconciliation']={
    'candidate_families':len(rows),
    'status_counts':counts,
    'accepted_or_advanced':sum(v for k,v in counts.items() if k in {'STAGE_B_ADVANCED','REVIEWED_RETAINED'}),
    'unresolved_provenance':counts.get('UNRESOLVED_PROVENANCE',0),
    'review_required':counts.get('REVIEW_REQUIRED',0),
    'integrity_pass':(
        len(rows)==29 and
        counts.get('UNRESOLVED_PROVENANCE',0)==1 and
        counts.get('REVIEW_REQUIRED',0)==1 and
        len(node_ids)==len(set(node_ids))
    )
}
graph['policy']['canonical_review_is_not_hash_identity']=True
graph['integrity']['release_integrity_pass']=bool(graph['integrity'].get('release_integrity_pass')) and graph['canonical_reconciliation']['integrity_pass']
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(graph['canonical_reconciliation'],sort_keys=True))
raise SystemExit(0 if graph['integrity']['release_integrity_pass'] else 2)
