#!/usr/bin/env python3
"""AkashicNET topic census v0.3: active metadata + materialised WikiSpine identities."""
from __future__ import annotations
import csv, json, re, unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; C=ROOT/'references'/'community'; T=ROOT/'references'/'topics'
ALIASES={'catholocism':'catholicism','rosicurcianism':'rosicrucianism','qabbalah':'kabbalah'}
NON={'pdf','uncategorized','textbooks','reference','biographies','fiction'}
def norm(v):
 v=unicodedata.normalize('NFKC',v or '').strip(); v=re.sub(r'\s+',' ',v).casefold(); return ALIASES.get(v,v)
def rows(p):
 if not p.exists(): return []
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def root_topics():
 rs=rows(C/'drive-metadata-root-census.csv'); out=set()
 for r in rs:
  raw=next((r.get(k,'') for k in ('root_name','name','folder_name','collection','label','topic') if r.get(k)), '')
  if not raw:
   raw=next((str(v).strip() for v in r.values() if v and not str(v).strip().isdigit() and '/' not in str(v)), '')
  n=norm(raw)
  if n and n not in NON: out.add(n)
 return out,len(rs)
def n2n():
 rs=rows(C/'n2n-pilot-index.csv'); c=set(); f=set(); e=set()
 for r in rs:
  a=norm(r.get('category','')); b=norm(r.get('toolkit_framework',''))
  if a:c.add(a)
  if b:f.add(b)
  if a and b:e.add((a,b))
 return c,f,e,len(rs)
def expansion():
 rs=rows(T/'topic-expansion-cross-source-v0.1.csv'); s={norm(r.get('canonical_topic','')) for r in rs if norm(r.get('adjudication',''))=='accept' and norm(r.get('provisional_additive',''))=='yes'}
 return {x for x in s if x},len(rs)
def wiki():
 p=T/'wikispine-topic-identities-v0.7.4.json'; d=json.loads(p.read_text(encoding='utf-8')); rec=d['records']; labels={norm(x[0]) for x in rec}; qids={x[1] for x in rec if x[1]}; pending=[x[0] for x in rec if x[2] != 'RESOLVED_HIGH_PRECISION']; return labels,qids,pending,len(rec)
def main():
 roots,nr=root_topics(); cats,frames,edges,nn=n2n(); exp,ne=expansion(); wik,qids,pending,nw=wiki()
 base=roots|cats|frames|exp; overlap=base&wik; additive=wik-base; union=base|wik
 report={'version':'0.3','method':'identity_aware_explicit_label_union','external_crawl_performed':False,'records_examined':nr+nn+ne+nw,'drive_root_records':nr,'n2n_records':nn,'expansion_records':ne,'wikispine_records':nw,'active_v02_union':len(base),'wikispine_unique_labels':len(wik),'wikispine_resolved_qids':len(qids),'wikispine_pending_labels':pending,'wikispine_overlap_with_v02':len(overlap),'wikispine_additive_to_v02':len(additive),'canonical_explicit_label_union_v03':len(union),'overlap_labels':sorted(overlap),'additive_wikispine_labels':sorted(additive),'n2n_category_framework_edges':len(edges),'audited_333_reached':len(union)>=333,'warning':'This is an explicit-label census. Descendant metadata and ontology layers are not yet fully integrated; do not present it as the final AkashicNET topic count.'}
 out=ROOT/'artifacts'/'akashicnet-topic-census-v0.3.json';out.parent.mkdir(exist_ok=True);out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8');print(json.dumps(report,indent=2,ensure_ascii=False))
if __name__=='__main__':main()
