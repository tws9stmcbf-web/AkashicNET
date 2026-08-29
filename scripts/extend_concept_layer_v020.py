#!/usr/bin/env python3
from __future__ import annotations
import csv,json
from pathlib import Path

BASE=Path('data/concept-layer-v0.11.json')
CONCEPTS=Path('references/community/concept-seed-v0.20.csv')
REVIEWS=Path('references/community/family-concept-review-v0.20.csv')
OUT=Path('data/concept-layer-v0.20.json')


def main():
    base=json.load(BASE.open(encoding='utf-8'))
    concepts=list(csv.DictReader(CONCEPTS.open(encoding='utf-8',newline='')))
    reviews=list(csv.DictReader(REVIEWS.open(encoding='utf-8',newline='')))

    concept_nodes=[{
        'node_id':c['concept_id'],'node_type':'concept','label':c['label'],
        'definition':c['definition'],'review_state':c['review_state'],'notes':c['notes']
    } for c in concepts]

    library_edges=list(base['library_edges'])
    added=[]
    for r in reviews:
        if r['decision']!='ACCEPT':
            continue
        edge={
            'source_type':'canonical_family','source_ref':r['family_id'],
            'relationship':'ABOUT','target_concept':r['concept_id'],
            'basis':r['basis'],'matched_terms':[r['concept_label']],
            'review_state':'ACCEPTED','accepted_edge':True,'v020_decision':'ACCEPT',
            'review_id':r['review_id'],'not_truth_claim':True,
            'rights_promotion_allowed':False,'scientific_evidence_promotion_allowed':False
        }
        library_edges.append(edge); added.append(edge)

    counts={d:sum(1 for r in reviews if r['decision']==d) for d in ['ACCEPT','HOLD','REJECT']}
    out={
        'version':'0.20','scope':'reviewed ontology expansion plus metadata-only family concept re-review',
        'concept_count':len(concept_nodes),'base_concept_count':base['concept_count'],
        'new_concept_count':len(concept_nodes)-base['concept_count'],
        'reddit_records_examined':base['reddit_records_examined'],
        'candidate_count':base['candidate_count']+len(reviews),
        'review_decision_counts':counts,'new_accepted_family_edges':len(added),
        'accepted_edge_count':base['accepted_edge_count']+len(added),
        'truth_inference_allowed':False,'rights_promotion_allowed':False,
        'scientific_evidence_promotion_allowed':False,
        'concept_nodes':concept_nodes,'reddit_edges':base['reddit_edges'],'library_edges':library_edges,
        'v020_reviews':reviews
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    json.dump(out,OUT.open('w',encoding='utf-8'),ensure_ascii=False,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k not in {'concept_nodes','reddit_edges','library_edges','v020_reviews'}},sort_keys=True))

if __name__=='__main__':
    main()
