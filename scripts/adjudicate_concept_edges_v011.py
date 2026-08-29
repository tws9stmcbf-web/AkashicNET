#!/usr/bin/env python3
from __future__ import annotations
import csv,json,re
from pathlib import Path

IN=Path('data/concept-layer-v0.10.json')
PILOT=Path('references/community/n2n-pilot-index.csv')
OUT=Path('data/concept-layer-v0.11.json')

# High-precision terms may support an ABOUT edge when explicitly present in a title.
# Broad bridge terms remain HOLD even when explicit.
HIGH_PRECISION={
 'CONCEPT-0003':{'non-duality','nonduality','non-dual','nondual'},
 'CONCEPT-0004':{'psychedelic','psychedelics','psilocybin','lsd','dmt','ayahuasca','ibogaine'},
 'CONCEPT-0005':{'buddhism','buddhist','buddha','dharma'},
 'CONCEPT-0006':{'hinduism','hindu','vedanta','upanishad','ramayana'},
 'CONCEPT-0007':{'shamanism','shamanic','shaman'},
 'CONCEPT-0008':{'alchemy','alchemical','alchemist'},
 'CONCEPT-0009':{'mysticism','mystical','mystic'},
 'CONCEPT-0010':{'meditation','contemplative','contemplation','mindfulness'},
}
BROAD={'CONCEPT-0001','CONCEPT-0002'}

def has_term(text,terms):
 t=(text or '').lower()
 return any(re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',t) for x in terms)

def main():
 d=json.load(IN.open(encoding='utf-8'))
 posts={r.get('reddit_url'):r for r in csv.DictReader(PILOT.open(encoding='utf-8',newline=''))}
 out_edges=[]
 counts={'ACCEPT':0,'HOLD':0,'REJECT':0}
 for e in d['reddit_edges']:
  cid=e['target_concept']; p=posts.get(e['source_ref'],{}); title=p.get('title','')
  if cid in BROAD:
   decision='HOLD'; reason='Broad bridge concept requires human contextual review; explicit token alone is insufficient.'
  elif cid in HIGH_PRECISION and has_term(title,HIGH_PRECISION[cid]):
   decision='ACCEPT'; reason='High-precision reviewed alias occurs explicitly in Reddit title; promotes topical ABOUT edge only.'
  else:
   decision='HOLD'; reason='Alias occurs only outside the title or is insufficiently specific for automatic topical promotion.'
  counts[decision]+=1
  out_edges.append({**e,'relationship':'ABOUT' if decision=='ACCEPT' else 'ABOUT_CANDIDATE','v011_decision':decision,'review_state':'ACCEPTED' if decision=='ACCEPT' else 'HOLD','accepted_edge':decision=='ACCEPT','adjudication_reason':reason})
 library=[]
 for e in d['library_edges']:
  cid=e['target_concept']
  if cid in BROAD:
   decision='HOLD'; reason='Broad bridge concept requires contextual review beyond canonical label token match.'
  else:
   decision='ACCEPT'; reason='High-precision reviewed concept alias occurs explicitly in canonical-family label; topical ABOUT edge only.'
  counts[decision]+=1
  library.append({**e,'relationship':'ABOUT' if decision=='ACCEPT' else 'ABOUT_CANDIDATE','v011_decision':decision,'review_state':'ACCEPTED' if decision=='ACCEPT' else 'HOLD','accepted_edge':decision=='ACCEPT','adjudication_reason':reason})
 out={
  'version':'0.11','scope':'concept-topical-adjudication-not-truth-or-evidence-validation',
  'concept_count':d['concept_count'],'reddit_records_examined':d['reddit_records_examined'],
  'candidate_count':len(out_edges)+len(library),'decision_counts':counts,
  'accepted_edge_count':counts['ACCEPT'],'truth_inference_allowed':False,
  'rights_promotion_allowed':False,'scientific_evidence_promotion_allowed':False,
  'concept_nodes':d['concept_nodes'],'reddit_edges':out_edges,'library_edges':library}
 OUT.parent.mkdir(parents=True,exist_ok=True)
 json.dump(out,OUT.open('w',encoding='utf-8'),ensure_ascii=False,indent=2)
 print(json.dumps({k:v for k,v in out.items() if k not in {'concept_nodes','reddit_edges','library_edges'}},sort_keys=True))

if __name__=='__main__': main()
