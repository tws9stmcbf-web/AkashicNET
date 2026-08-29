#!/usr/bin/env python3
from __future__ import annotations
import csv,json,re
from pathlib import Path

BASE=Path('data/concept-layer-v0.20.json')
GRAPH=Path('data/knowledge-graph-v0.16.json')
PILOT=Path('references/community/n2n-pilot-index.csv')
OUT=Path('data/concept-layer-v0.21.json')

ALIASES={
 'CONCEPT-0011':['hermeticism','hermetic'],
 'CONCEPT-0012':['qabbalah','kabbalah','cabala','quabbalah','qabalistic','qabbalistic','kabbalistic'],
 'CONCEPT-0013':['ceremonial magic','ritual magic'],
 'CONCEPT-0014':['esotericism','esoteric','occult'],
 'CONCEPT-0015':['theosophy','theosophical'],
}

def hits(text,terms):
 t=(text or '').lower()
 return sorted({x for x in terms if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',t)})

def main():
 base=json.load(BASE.open(encoding='utf-8'))
 graph=json.load(GRAPH.open(encoding='utf-8'))
 posts=list(csv.DictReader(PILOT.open(encoding='utf-8',newline='')))
 reddit=list(base['reddit_edges']); library=list(base['library_edges'])
 existing_r={(e['source_ref'],e['target_concept']) for e in reddit}
 existing_l={(e['source_ref'],e['target_concept']) for e in library}
 decisions={'ACCEPT':0,'HOLD':0,'REJECT':0}; new_r=[]; new_l=[]
 for p in posts:
  title=p.get('title',''); summary=p.get('short_summary','')
  for cid,terms in ALIASES.items():
   ht=hits(title,terms); hs=hits(summary,terms)
   if not (ht or hs) or (p.get('reddit_url'),cid) in existing_r: continue
   decision='ACCEPT' if ht else 'HOLD'; decisions[decision]+=1
   e={'source_type':'reddit_record','source_ref':p.get('reddit_url'),'relationship':'ABOUT' if decision=='ACCEPT' else 'ABOUT_CANDIDATE','target_concept':cid,'basis':'explicit expanded-ontology alias in curated title' if ht else 'expanded-ontology alias occurs only in short_summary','matched_terms':sorted(set(ht+hs)),'matched_field':'title' if ht else 'short_summary','review_state':'ACCEPTED' if decision=='ACCEPT' else 'HOLD','accepted_edge':decision=='ACCEPT','v021_decision':decision,'not_truth_claim':True,'not_scientific_evidence':True,'rights_promotion_allowed':False}
   reddit.append(e); new_r.append(e); existing_r.add((p.get('reddit_url'),cid))
 for n in graph.get('nodes',[]):
  if n.get('node_type') not in {'canonical_family','canonical_candidate_family'}: continue
  ref=n.get('family_id') or n.get('node_id'); label=n.get('label','')
  for cid,terms in ALIASES.items():
   hl=hits(label,terms)
   if not hl or (ref,cid) in existing_l: continue
   decisions['ACCEPT']+=1
   e={'source_type':'canonical_family','source_ref':ref,'relationship':'ABOUT','target_concept':cid,'basis':'explicit expanded-ontology alias in canonical family label','matched_terms':hl,'matched_field':'canonical_label','review_state':'ACCEPTED','accepted_edge':True,'v021_decision':'ACCEPT','not_truth_claim':True,'rights_promotion_allowed':False,'scientific_evidence_promotion_allowed':False}
   library.append(e); new_l.append(e); existing_l.add((ref,cid))
 out={**base,'version':'0.21','scope':'expanded reviewed ontology indexed across N2N pilot and canonical-family metadata','candidate_count':base['candidate_count']+len(new_r)+len(new_l),'accepted_edge_count':base['accepted_edge_count']+sum(1 for e in new_r+new_l if e['accepted_edge']),'v021_new_reddit_candidates':len(new_r),'v021_new_library_candidates':len(new_l),'v021_decision_counts':decisions,'truth_inference_allowed':False,'rights_promotion_allowed':False,'scientific_evidence_promotion_allowed':False,'reddit_edges':reddit,'library_edges':library}
 OUT.parent.mkdir(parents=True,exist_ok=True); json.dump(out,OUT.open('w',encoding='utf-8'),ensure_ascii=False,indent=2)
 print(json.dumps({k:out[k] for k in ['version','concept_count','reddit_records_examined','v021_new_reddit_candidates','v021_new_library_candidates','v021_decision_counts','accepted_edge_count']},sort_keys=True))

if __name__=='__main__': main()
