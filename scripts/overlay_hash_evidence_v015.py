#!/usr/bin/env python3
import csv,json
from pathlib import Path

IN=Path('data/knowledge-graph-v0.14.json')
QUEUE=Path('references/community/hash-verification-queue-v0.15.csv')
OUT=Path('data/knowledge-graph-v0.15.json')

g=json.load(IN.open(encoding='utf-8'))
existing={n.get('node_id') or n.get('id') for n in g['nodes'] if (n.get('node_id') or n.get('id'))}
records=list(csv.DictReader(QUEUE.open(encoding='utf-8')))
added=0
for r in records:
    node_id=f"hash_evidence:{r['hash_record_id']}"
    manifests=[x.strip() for x in r['manifestation_node_ids'].split(';') if x.strip()]
    assert all(m in existing for m in manifests), (r['hash_record_id'], manifests)
    node={
        'node_id':node_id,
        'node_type':'hash_evidence',
        'hash_record_id':r['hash_record_id'],
        'family_id':r['family_id'],
        'canonical_label':r['canonical_label'],
        'algorithm':r['algorithm'],
        'hash_execution_state':r['hash_execution_state'],
        'comparison_state':r['comparison_state'],
        'evidence_scope':r['evidence_scope'],
        'review_state':r['review_state'],
        'manifestation_node_ids':manifests,
        'hashes':[],
        'not_byte_identity_claim':True,
        'not_truth_claim':True,
        'rights_promotion_allowed':False,
        'scientific_evidence_promotion_allowed':False,
    }
    g['nodes'].append(node); existing.add(node_id); added+=1
    for m in manifests:
        g['edges'].append({
            'source':node_id,'target':m,'relationship':'HASH_CHECK_QUEUED_FOR',
            'review_state':'REVIEW_REQUIRED','hash_execution_state':'NOT_AUTHORISED',
            'comparison_state':'NOT_COMPARED','not_byte_identity_claim':True,
            'not_truth_claim':True
        })

g['schema_version']='0.15'
g['hash_evidence_v015']={
    'queue_records':len(records),
    'hash_evidence_nodes_added':added,
    'hashes_computed':0,
    'byte_identity_assertions':0,
    'execution_policy':'NOT_AUTHORISED',
    'truth_inference_allowed':False,
    'rights_promotion_allowed':False,
    'scientific_evidence_promotion_allowed':False,
    'integrity_pass': added==3 and all(r['hash_execution_state']=='NOT_AUTHORISED' and r['comparison_state']=='NOT_COMPARED' for r in records)
}
g['integrity']['release_integrity_pass']=bool(g['integrity'].get('release_integrity_pass')) and g['hash_evidence_v015']['integrity_pass']
json.dump(g,OUT.open('w',encoding='utf-8'),ensure_ascii=False,indent=2,sort_keys=True)
print(json.dumps(g['hash_evidence_v015'],sort_keys=True))
raise SystemExit(0 if g['integrity']['release_integrity_pass'] else 2)
