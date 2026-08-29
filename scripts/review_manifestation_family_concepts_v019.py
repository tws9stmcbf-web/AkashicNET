#!/usr/bin/env python3
from __future__ import annotations
import csv,json
from pathlib import Path

REVIEW=Path('references/community/manifestation-family-concept-review-v0.19.csv')
CONCEPT=Path('data/concept-layer-v0.11.json')
DEDUP=Path('data/dedup-retrieval-view-v0.17.json')
OUT=Path('data/manifestation-family-concept-review-v0.19.json')

rows=list(csv.DictReader(REVIEW.open(encoding='utf-8',newline='')))
concept=json.load(CONCEPT.open(encoding='utf-8'))
dedup=json.load(DEDUP.open(encoding='utf-8'))
concept_ids={c['node_id'] for c in concept['concept_nodes']}
family_ids={fid for u in dedup['retrieval_units'] for fid in u.get('family_ids',[])}

assert len(rows)==5
assert all(r['family_id'] in family_ids for r in rows)
assert all(r['candidate_concept_id'] in concept_ids for r in rows)
assert all(r['decision'] in {'ACCEPT','HOLD','REJECT'} for r in rows)

accepted=[r for r in rows if r['decision']=='ACCEPT']
holds=[r for r in rows if r['decision']=='HOLD']
rejected=[r for r in rows if r['decision']=='REJECT']

out={
    'version':'0.19',
    'scope':'metadata-only reviewed manifestation-family to concept adjudication',
    'families_reviewed':len(rows),
    'decision_counts':{'ACCEPT':len(accepted),'HOLD':len(holds),'REJECT':len(rejected)},
    'accepted_about_edges_added':0,
    'metadata_only':True,
    'document_bodies_read':False,
    'truth_inference_allowed':False,
    'rights_promotion_allowed':False,
    'scientific_evidence_promotion_allowed':False,
    'review_records':rows,
    'integrity_pass':(
        len(rows)==5 and len(accepted)==0 and len(holds)==5 and len(rejected)==0 and
        all(r['truth_inference_allowed']=='false' for r in rows) and
        all(r['rights_promotion_allowed']=='false' for r in rows) and
        all(r['scientific_evidence_promotion_allowed']=='false' for r in rows)
    )
}
OUT.parent.mkdir(parents=True,exist_ok=True)
json.dump(out,OUT.open('w',encoding='utf-8'),ensure_ascii=False,indent=2,sort_keys=True)
print(json.dumps({k:v for k,v in out.items() if k!='review_records'},sort_keys=True))
raise SystemExit(0 if out['integrity_pass'] else 2)
