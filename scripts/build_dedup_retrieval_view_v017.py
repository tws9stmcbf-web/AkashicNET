#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

SRC=Path('data/knowledge-graph-v0.16.json')
OUT=Path('data/dedup-retrieval-view-v0.17.json')

g=json.load(SRC.open(encoding='utf-8'))
manifestations=[n for n in g['nodes'] if n.get('node_type')=='manifestation']

# Collapse only manifestations whose byte identity was verified by matching SHA-256.
# Every other physical manifestation remains an independent retrieval unit.
groups={}
for m in manifestations:
    if m.get('identity_status')=='SHA256_MATCH_VERIFIED' and m.get('sha256'):
        key='sha256:'+m['sha256']
        collapse_basis='SHA256_MATCH_VERIFIED'
    else:
        key='manifestation:'+m['manifestation_id']
        collapse_basis='NOT_COLLAPSED_NO_HASH_IDENTITY'
    grp=groups.setdefault(key,{
        'retrieval_unit_id':key,
        'collapse_basis':collapse_basis,
        'sha256':m.get('sha256') if collapse_basis=='SHA256_MATCH_VERIFIED' else None,
        'family_ids':set(),
        'labels':set(),
        'manifestations':[],
        'rights_states':set(),
        'not_truth_claim':True,
        'rights_promotion_allowed':False,
        'scientific_evidence_promotion_allowed':False,
    })
    grp['family_ids'].add(m.get('family_id'))
    grp['labels'].add(m.get('label'))
    grp['rights_states'].add(m.get('rights_state','UNKNOWN_UNVERIFIED'))
    grp['manifestations'].append({
        'manifestation_node_id':m['node_id'],
        'manifestation_id':m['manifestation_id'],
        'drive_object_id':m['source_drive_object_id'],
        'filename':m['filename'],
        'size_bytes':m['size_bytes'],
        'identity_status':m['identity_status'],
        'sha256':m.get('sha256'),
    })

units=[]
for grp in groups.values():
    grp['family_ids']=sorted(x for x in grp['family_ids'] if x)
    grp['labels']=sorted(x for x in grp['labels'] if x)
    grp['rights_states']=sorted(grp['rights_states'])
    grp['physical_manifestation_count']=len(grp['manifestations'])
    grp['deduplicated']=grp['collapse_basis']=='SHA256_MATCH_VERIFIED' and len(grp['manifestations'])>1
    units.append(grp)
units.sort(key=lambda x:(x['labels'][0] if x['labels'] else '',x['retrieval_unit_id']))

verified_groups=[u for u in units if u['deduplicated']]
singletons=[u for u in units if not u['deduplicated']]
meta={
    'version':'0.17',
    'scope':'deduplication-aware retrieval view over v0.16 manifestation provenance',
    'physical_manifestations':len(manifestations),
    'logical_retrieval_units':len(units),
    'sha256_verified_dedup_groups':len(verified_groups),
    'physical_manifestations_in_dedup_groups':sum(u['physical_manifestation_count'] for u in verified_groups),
    'uncollapsed_units':len(singletons),
    'collapse_policy':'matching SHA-256 only',
    'raw_content_retained':False,
    'truth_inference_allowed':False,
    'rights_promotion_allowed':False,
    'scientific_evidence_promotion_allowed':False,
    'integrity_pass':(
        len(manifestations)==13 and len(units)==10 and len(verified_groups)==3 and
        sum(u['physical_manifestation_count'] for u in units)==13 and
        all(u['physical_manifestation_count']==2 for u in verified_groups)
    )
}
out={'schema_version':'0.17','metadata':meta,'retrieval_units':units}
OUT.parent.mkdir(parents=True,exist_ok=True)
json.dump(out,OUT.open('w',encoding='utf-8'),ensure_ascii=False,indent=2,sort_keys=True)
print(json.dumps(meta,sort_keys=True))
raise SystemExit(0 if meta['integrity_pass'] else 2)
