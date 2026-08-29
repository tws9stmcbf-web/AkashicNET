#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

CONCEPT=Path('data/concept-layer-v0.21.json')
GRAPH=Path('data/knowledge-graph-v0.16.json')
OUT=Path('data/concept-layer-v0.22.json')


def main():
    d=json.load(CONCEPT.open(encoding='utf-8'))
    g=json.load(GRAPH.open(encoding='utf-8'))

    # Resolve every graph representation to one logical canonical family id.
    logical_by_ref={}
    repr_meta={}
    for n in g.get('nodes',[]):
        if n.get('node_type') not in {'canonical_family','canonical_candidate_family'}:
            continue
        ref=n.get('node_id')
        logical=n.get('family_id') or ref
        logical_by_ref[ref]=logical
        logical_by_ref[logical]=logical
        repr_meta[ref]={
            'node_id':ref,
            'node_type':n.get('node_type'),
            'family_id':logical,
            'label':n.get('label') or n.get('canonical_label'),
        }

    grouped={}
    for e in d['library_edges']:
        raw=e['source_ref']
        logical=logical_by_ref.get(raw,raw)
        key=(logical,e['target_concept'])
        rec=grouped.setdefault(key,{
            'source_type':'canonical_family',
            'source_ref':logical,
            'logical_family_id':logical,
            'relationship':'ABOUT' if e.get('accepted_edge') else 'ABOUT_CANDIDATE',
            'target_concept':e['target_concept'],
            'review_state':'ACCEPTED' if e.get('accepted_edge') else e.get('review_state','HOLD'),
            'accepted_edge':bool(e.get('accepted_edge')),
            'basis_set':set(),
            'matched_terms':set(),
            'representation_sources':[],
            'not_truth_claim':True,
            'rights_promotion_allowed':False,
            'scientific_evidence_promotion_allowed':False,
        })
        if e.get('accepted_edge'):
            rec['relationship']='ABOUT'; rec['review_state']='ACCEPTED'; rec['accepted_edge']=True
        if e.get('basis'): rec['basis_set'].add(e['basis'])
        rec['matched_terms'].update(e.get('matched_terms') or [])
        rep=repr_meta.get(raw,{'node_id':raw,'family_id':logical})
        rep={**rep,
             'original_source_ref':raw,
             'relationship':e.get('relationship'),
             'review_state':e.get('review_state'),
             'accepted_edge':bool(e.get('accepted_edge')),
             'matched_field':e.get('matched_field'),
             'review_id':e.get('review_id'),
             'v011_decision':e.get('v011_decision'),
             'v020_decision':e.get('v020_decision'),
             'v021_decision':e.get('v021_decision')}
        # Prevent exact representation duplicates in provenance list.
        sig=json.dumps(rep,sort_keys=True,ensure_ascii=False)
        if all(json.dumps(x,sort_keys=True,ensure_ascii=False)!=sig for x in rec['representation_sources']):
            rec['representation_sources'].append(rep)

    norm=[]
    for rec in grouped.values():
        rec['basis_set']=sorted(rec['basis_set'])
        rec['matched_terms']=sorted(rec['matched_terms'])
        rec['representation_count']=len(rec['representation_sources'])
        rec['representation_multiplicity_not_semantic_strength']=True
        norm.append(rec)
    norm.sort(key=lambda x:(x['logical_family_id'],x['target_concept']))

    accepted=sum(1 for e in norm if e['accepted_edge'])
    multi=[e for e in norm if e['representation_count']>1]
    out={
        **d,
        'version':'0.22',
        'scope':'semantic representation normalisation; one logical family-concept edge with representation provenance retained',
        'library_edges_pre_normalisation':len(d['library_edges']),
        'library_edges_post_normalisation':len(norm),
        'logical_library_accepted_edges':accepted,
        'multi_representation_logical_edges':len(multi),
        'representation_provenance_records':sum(e['representation_count'] for e in norm),
        'semantic_strength_from_representation_count':False,
        'truth_inference_allowed':False,
        'rights_promotion_allowed':False,
        'scientific_evidence_promotion_allowed':False,
        'library_edges':norm,
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    json.dump(out,OUT.open('w',encoding='utf-8'),ensure_ascii=False,indent=2)
    print(json.dumps({k:out[k] for k in ['version','library_edges_pre_normalisation','library_edges_post_normalisation','logical_library_accepted_edges','multi_representation_logical_edges','representation_provenance_records']},sort_keys=True))

if __name__=='__main__': main()
