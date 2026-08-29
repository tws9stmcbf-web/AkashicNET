#!/usr/bin/env python3
from __future__ import annotations
import argparse,json
from pathlib import Path

DATA=Path('data/concept-layer-v0.11.json')

def main():
 p=argparse.ArgumentParser()
 p.add_argument('query')
 p.add_argument('--accepted-only',action='store_true')
 a=p.parse_args()
 d=json.load(DATA.open(encoding='utf-8'))
 q=a.query.lower()
 concepts={c['node_id']:c for c in d['concept_nodes']}
 matched={cid for cid,c in concepts.items() if q in c['label'].lower() or q in c['definition'].lower() or q==cid.lower()}
 rows=[]
 for domain,key in [('reddit','reddit_edges'),('library','library_edges')]:
  for e in d[key]:
   if e['target_concept'] not in matched: continue
   if a.accepted_only and not e['accepted_edge']: continue
   rows.append({
    'domain':domain,'source_ref':e['source_ref'],'concept_id':e['target_concept'],
    'concept':concepts[e['target_concept']]['label'],'relationship':e['relationship'],
    'decision':e['v011_decision'],'review_state':e['review_state'],
    'basis':e['basis'],'matched_terms':e.get('matched_terms',[]),
    'not_truth_claim':True,'not_scientific_evidence':True if domain=='reddit' else None
   })
 print(json.dumps({'query':a.query,'matched_concepts':sorted(matched),'result_count':len(rows),'results':rows},ensure_ascii=False,indent=2))

if __name__=='__main__': main()
