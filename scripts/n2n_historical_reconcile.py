#!/usr/bin/env python3
"""Reconcile the tracked historical Reddit URI archive into a canonical N2N corpus.

Repository-data only. No Drive access, Reddit API calls, or network crawling.
Public-web corroboration is joined only when already materialised in tracked seed files.
"""
from __future__ import annotations
import csv, glob, json, re
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'references/community/reddit-uri-index.csv'
OUT=ROOT/'artifacts'
POST_RE=re.compile(r'/r/([^/]+)/comments/([A-Za-z0-9]+)(?:/([^/?#]*))?',re.I)
KNOWN_ANNOTATIONS={'original','research','hieratic','qmm','what'}

def clean(raw):
 """Strip one or more trailing known annotation tokens without altering the URL.

 Historical rows can end in composite suffixes such as `,HIERATIC,What` and
 `,QMM,What`.  Parsing from the right preserves the base URL and captures every
 known suffix token deterministically.
 """
 value=(raw or '').strip()
 annotations=[]
 while ',' in value:
  base,tail=value.rsplit(',',1)
  token=tail.strip()
  if token.casefold() not in KNOWN_ANNOTATIONS:
   break
  annotations.insert(0,token)
  value=base.rstrip()
 return value.rstrip('/'),annotations

def canonical(url):
 m=POST_RE.search(url)
 if not m:return None
 sub,pid,slug=m.groups(); slug=(slug or '').strip('/')
 base=f'https://www.reddit.com/r/{sub}/comments/{pid.lower()}'
 return (base+(f'/{slug}' if slug else ''),sub,pid.lower(),slug)

def suspicious_ids(ids):
 # Conservative v0.2-compatible structural heuristic: numeric base36 +1 runs >=4.
 vals=sorted({(int(x,36),x) for x in ids})
 flagged=set(); run=[]; prev=None
 for val,pid in vals:
  if prev is not None and val==prev+1: run.append(pid)
  else:
   if len(run)>=4: flagged.update(run)
   run=[pid]
  prev=val
 if len(run)>=4: flagged.update(run)
 return flagged

def corroborated_ids():
 out=set()
 for p in glob.glob(str(ROOT/'references/community/reddit-corroboration-seed-v0.*.json')):
  try:d=json.loads(Path(p).read_text(encoding='utf-8'))
  except Exception:continue
  recs=d.get('records',d if isinstance(d,list) else [])
  if isinstance(recs,dict): recs=recs.get('records',[])
  for r in recs:
   if isinstance(r,str): out.add(r.lower()); continue
   pid=r.get('post_id') or r.get('reddit_post_id') or ''
   if pid:out.add(str(pid).lower())
 return out

def main():
 rows=list(csv.DictReader(SRC.open(encoding='utf-8-sig',newline='')))
 by_id={}; annotation_rows=0; annotation_tokens=0; nonposts=0
 for i,r in enumerate(rows,2):
  raw=r.get('reddit_url',''); url,annotations=clean(raw)
  if annotations:
   annotation_rows+=1
   annotation_tokens+=len(annotations)
  c=canonical(url)
  if not c: nonposts+=1; continue
  can,sub,pid,slug=c
  rec=by_id.setdefault(pid,{'post_id':pid,'subreddit':sub,'canonical_url':can,'slug':slug,'source_rows':0,'annotations':set()})
  rec['source_rows']+=1
  rec['annotations'].update(annotations)
 # Only N2N records form this output; other subreddit records stay visible in summary.
 n2n={pid:r for pid,r in by_id.items() if r['subreddit'].casefold()=='neuronstonirvana'}
 suspicious=suspicious_ids(n2n)
 corr=corroborated_ids()
 outrows=[]
 for pid,r in sorted(n2n.items(),key=lambda x:int(x[0],36)):
  status='public_web_corroborated' if pid in corr else ('suspicious_pattern' if pid in suspicious else 'structural_candidate')
  outrows.append({**r,'annotations':'|'.join(sorted(r['annotations'],key=str.casefold)),'evidence_status':status,'public_web_corroborated':str(pid in corr).lower(),'api_verified':'false','origin_status':'origin_unresolved'})
 OUT.mkdir(exist_ok=True)
 csvpath=OUT/'n2n-historical-reconciled.csv'
 fields=['post_id','subreddit','canonical_url','slug','source_rows','annotations','evidence_status','public_web_corroborated','api_verified','origin_status']
 with csvpath.open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(outrows)
 counts=Counter(r['evidence_status'] for r in outrows)
 summary={'version':'0.2','network_access_performed':False,'drive_crawl_performed':False,'source_rows':len(rows),'annotation_rows':annotation_rows,'annotation_tokens':annotation_tokens,'non_post_rows':nonposts,'unique_post_ids_all_subreddits':len(by_id),'unique_n2n_post_ids':len(n2n),'n2n_suspicious_pattern_ids':len(suspicious),'tracked_public_web_corroborated_n2n_ids':counts['public_web_corroborated'],'n2n_structural_candidates':counts['structural_candidate'],'evidence_status_counts':dict(counts),'warning':'Structural candidates and suspicious patterns are not API verification. suspicious_pattern does not mean fabricated.'}
 (OUT/'n2n-historical-reconciliation-summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
