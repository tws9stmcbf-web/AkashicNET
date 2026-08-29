#!/usr/bin/env python3
from __future__ import annotations
import csv,json
from pathlib import Path

SRC=Path('data/knowledge-graph-v0.13.json')
LEDGER=Path('references/community/drive-manifestation-provenance-v0.14.csv')
OUT=Path('data/knowledge-graph-v0.14.json')

def main():
    g=json.load(SRC.open(encoding='utf-8'))
    rows=list(csv.DictReader(LEDGER.open(encoding='utf-8',newline='')))
    nodes=g.setdefault('nodes',[]); edges=g.setdefault('edges',[])
    family_ids={n.get('family_id'):n.get('node_id') for n in nodes if n.get('family_id')}
    collection_ids={n.get('collection_path'):n.get('node_id') for n in nodes if n.get('collection_path')}
    seen_manifest=set(); seen_drive=set(); unresolved=[]
    for r in rows:
        mid=r['manifestation_id']; fid=r['family_id']; cpath=r['collection_path']; did=r['drive_object_id']
        fam_node=family_ids.get(fid); coll_node=collection_ids.get(cpath)
        if not fam_node or not coll_node:
            unresolved.append({'manifestation_id':mid,'family_id':fid,'collection_path':cpath,'missing_family':not bool(fam_node),'missing_collection':not bool(coll_node)})
            continue
        if mid in seen_manifest or did in seen_drive:
            raise SystemExit(f'duplicate manifestation or drive object: {mid} {did}')
        seen_manifest.add(mid); seen_drive.add(did)
        nodes.append({
            'node_id':f'manifestation:{mid}', 'node_type':'manifestation', 'manifestation_id':mid,
            'family_id':fid, 'label':r['logical_work'], 'filename':r['filename'],
            'source_drive_object_id':did, 'size_bytes':int(r['size_bytes']),
            'manifestation_class':r['manifestation_class'], 'identity_status':r['identity_status'],
            'evidence_basis':r['evidence_basis'], 'rights_state':r['rights_state'],
            'content_hydrated':False, 'embeddings_generated':False,
            'not_truth_claim':True, 'not_byte_identity_claim':True
        })
        edges.append({'source':fam_node,'relationship':'HAS_MANIFESTATION','target':f'manifestation:{mid}','basis':'live Drive metadata v0.14','review_state':'accepted','not_truth_claim':True})
        edges.append({'source':f'manifestation:{mid}','relationship':'OBSERVED_IN_COLLECTION','target':coll_node,'basis':'exact Drive parent collection + immutable object ID','review_state':'accepted','not_document_body_read':True})
    same_size_groups={}
    for r in rows:
        if r['manifestation_class']=='duplicate_copy_candidate':
            key=(r['family_id'],r['logical_work'],r['size_bytes'])
            same_size_groups.setdefault(key,[]).append(r['manifestation_id'])
    duplicate_candidate_groups=[{'family_id':k[0],'logical_work':k[1],'size_bytes':int(k[2]),'manifestations':v,'hash_status':'NOT_COMPUTED','byte_identity_asserted':False} for k,v in same_size_groups.items() if len(v)>1]
    meta={
        'version':'0.14','scope':'manifestation-level Drive metadata provenance; no document bodies or hashes',
        'manifestations_added':len(seen_manifest),'unique_drive_document_ids':len(seen_drive),
        'families_refined':len({r['family_id'] for r in rows}),
        'duplicate_candidate_groups':len(duplicate_candidate_groups),
        'unresolved_rows':unresolved,'hashes_computed':0,'byte_identity_assertions':0,
        'truth_inference_allowed':False,'rights_promotion_allowed':False,'scientific_evidence_promotion_allowed':False,
        'integrity_pass':len(seen_manifest)==len(rows) and len(unresolved)==0 and len(seen_drive)==len(rows)
    }
    g['schema_version']='0.14'; g['manifestation_provenance_v014']=meta; g['duplicate_candidate_groups_v014']=duplicate_candidate_groups
    g.setdefault('integrity',{})['release_integrity_pass']=bool(g.get('integrity',{}).get('release_integrity_pass',True) and meta['integrity_pass'])
    OUT.parent.mkdir(parents=True,exist_ok=True); json.dump(g,OUT.open('w',encoding='utf-8'),ensure_ascii=False,indent=2)
    print(json.dumps(meta,sort_keys=True))
    if not meta['integrity_pass']: raise SystemExit(2)

if __name__=='__main__': main()
