#!/usr/bin/env python3
import csv,json
from pathlib import Path

IN=Path('data/knowledge-graph-v0.15.json')
RESULTS=Path('references/community/hash-verification-results-v0.16.csv')
OUT=Path('data/knowledge-graph-v0.16.json')

g=json.load(IN.open(encoding='utf-8'))
rows=list(csv.DictReader(RESULTS.open(encoding='utf-8',newline='')))
node_by_id={n.get('node_id') or n.get('id'):n for n in g['nodes']}
hash_nodes={n.get('hash_record_id'):n for n in g['nodes'] if n.get('node_type')=='hash_evidence'}
verified_pairs=0
for r in rows:
    assert r['comparison_result']=='MATCH'
    assert r['sha256_a']==r['sha256_b']
    assert len(r['sha256_a'])==64
    a=r['manifestation_a']; b=r['manifestation_b']
    assert a in node_by_id and b in node_by_id
    for mid,digest in [(a,r['sha256_a']),(b,r['sha256_b'])]:
        m=node_by_id[mid]
        m['identity_status']='SHA256_MATCH_VERIFIED'
        m['sha256']=digest
        m['not_byte_identity_claim']=False
        m['byte_identity_scope']='verified pair only'
    hn=hash_nodes[r['hash_record_id']]
    hn['hash_execution_state']='COMPLETED'
    hn['comparison_state']='MATCH'
    hn['hashes']=[{'manifestation_node_id':a,'sha256':r['sha256_a']},{'manifestation_node_id':b,'sha256':r['sha256_b']}]
    hn['not_byte_identity_claim']=False
    hn['byte_identity_status']='BYTE_IDENTICAL_VERIFIED'
    g['edges'].append({'source':a,'relationship':'BYTE_IDENTICAL_TO','target':b,'basis':'matching SHA-256 under explicit v0.16 authorisation','review_state':'accepted','not_truth_claim':True,'rights_promotion_allowed':False,'scientific_evidence_promotion_allowed':False})
    verified_pairs+=1

g['schema_version']='0.16'
g['hash_evidence_v016']={
    'authorised_raw_files_hashed':6,
    'verification_pairs':len(rows),
    'matching_pairs':verified_pairs,
    'mismatching_pairs':sum(1 for r in rows if r['comparison_result']!='MATCH'),
    'byte_identity_assertions':verified_pairs,
    'hash_algorithm':'SHA-256',
    'raw_content_retained_in_graph':False,
    'digest_only_persistence':True,
    'scope':'six explicitly authorised queued Drive files only',
    'truth_inference_allowed':False,
    'rights_promotion_allowed':False,
    'scientific_evidence_promotion_allowed':False,
    'integrity_pass':len(rows)==3 and verified_pairs==3
}
g.setdefault('integrity',{})['release_integrity_pass']=bool(g['integrity'].get('release_integrity_pass',True) and g['hash_evidence_v016']['integrity_pass'])
json.dump(g,OUT.open('w',encoding='utf-8'),ensure_ascii=False,indent=2,sort_keys=True)
print(json.dumps(g['hash_evidence_v016'],sort_keys=True))
raise SystemExit(0 if g['integrity']['release_integrity_pass'] else 2)
