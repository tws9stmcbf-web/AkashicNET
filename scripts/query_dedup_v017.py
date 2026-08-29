#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

VIEW=Path('data/dedup-retrieval-view-v0.17.json')

p=argparse.ArgumentParser()
p.add_argument('query')
a=p.parse_args()
q=a.query.lower()
d=json.load(VIEW.open(encoding='utf-8'))
results=[]
for u in d['retrieval_units']:
    hay=' '.join(u['labels']+u['family_ids']+[m['filename'] for m in u['manifestations']]).lower()
    if q not in hay:
        continue
    results.append(u)
print(json.dumps({
    'version':'0.17',
    'query':a.query,
    'result_count':len(results),
    'physical_manifestation_count':sum(r['physical_manifestation_count'] for r in results),
    'collapse_policy':d['metadata']['collapse_policy'],
    'truth_inference_allowed':False,
    'rights_promotion_allowed':False,
    'scientific_evidence_promotion_allowed':False,
    'results':results,
},ensure_ascii=False,indent=2))
