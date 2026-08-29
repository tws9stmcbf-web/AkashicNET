#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path

I=Path('data/cross-source-candidates-v0.8.json')
O=Path('data/cross-source-adjudication-v0.9.json')

def norm(s):
    return re.sub(r'[^a-z0-9]+',' ',(s or '').lower()).strip()

def decide(c):
    label=norm(c.get('family_label'))
    title=norm(c.get('reddit_title'))
    score=float(c.get('candidate_score') or 0)
    exact_in_title=bool(label and label in title)
    if exact_in_title and score >= 60:
        return 'ACCEPT','Exact normalised canonical-family label occurs in curated Reddit title; metadata-only cross-source relationship accepted after rule-based review.'
    if score < 50:
        return 'REJECT','Lexical overlap is too weak for a defensible cross-source relationship.'
    return 'HOLD','Candidate has non-trivial lexical overlap but lacks exact title-level canonical-family evidence; requires human/context review.'

def main():
    d=json.load(I.open(encoding='utf-8'))
    rows=[]
    counts={'ACCEPT':0,'REJECT':0,'HOLD':0}
    for c in d['candidates']:
        decision,reason=decide(c)
        counts[decision]+=1
        rows.append({**c,'v09_decision':decision,'v09_reason':reason,
                     'accepted_edge':decision=='ACCEPT',
                     'reviewed_by':'deterministic_metadata_rule_v0.9',
                     'truth_inference_allowed':False,
                     'scientific_evidence_promotion_allowed':False,
                     'rights_promotion_allowed':False})
    out={'version':'0.9','scope':'metadata-only candidate adjudication',
         'candidate_count':len(rows),'decision_counts':counts,
         'accepted_edge_count':counts['ACCEPT'],
         'truth_inference_allowed':False,
         'scientific_evidence_promotion_allowed':False,
         'rights_promotion_allowed':False,
         'adjudications':rows}
    O.parent.mkdir(parents=True,exist_ok=True)
    json.dump(out,O.open('w',encoding='utf-8'),ensure_ascii=False,indent=2)
    print(json.dumps({k:v for k,v in out.items() if k!='adjudications'},sort_keys=True))
    for r in rows:
        print(f"{r['candidate_id']}\t{r['v09_decision']}\t{r['candidate_score']}\t{r['family_id']}\t{r['reddit_title']}")

if __name__=='__main__': main()
