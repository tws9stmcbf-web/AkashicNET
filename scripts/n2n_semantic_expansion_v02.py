#!/usr/bin/env python3
"""N2N semantic expansion v0.2.
Measures how much additional tracked metadata can be joined from reddit-semantic-index.csv
onto the canonical historical N2N ID set. Repository data only; no network or Drive crawl.
"""
import csv,json,re
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]; C=ROOT/'references'/'community'; O=ROOT/'artifacts'
RX=re.compile(r'/comments/([A-Za-z0-9]+)',re.I)
def extract_id(row):
    for k,v in row.items():
        if not v: continue
        lk=(k or '').lower()
        if lk in {'post_id','reddit_post_id','id'} and re.fullmatch(r'[A-Za-z0-9]+',v.strip()): return v.strip().lower()
        if 'url' in lk or 'link' in lk:
            m=RX.search(v)
            if m:return m.group(1).lower()
    return ''
def canonical_ids():
    out=set()
    with (C/'reddit-uri-index.csv').open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            u=r.get('reddit_url','')
            if '/r/NeuronsToNirvana/comments/' in u:
                m=RX.search(u)
                if m:out.add(m.group(1).lower())
    return out
def load(path):
    with path.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
def main():
    ids=canonical_ids(); semantic=load(C/'reddit-semantic-index.csv'); pilot=load(C/'n2n-pilot-index.csv')
    sem_join={}; pilot_join={}
    field_nonempty=Counter()
    for r in semantic:
        x=extract_id(r)
        if x in ids:
            sem_join[x]=r
            for k,v in r.items():
                if v and v.strip():field_nonempty[k]+=1
    for r in pilot:
        x=extract_id(r)
        if x in ids:pilot_join[x]=r
    union=set(sem_join)|set(pilot_join)
    additive=set(sem_join)-set(pilot_join)
    report={
      'version':'0.2','network_access_performed':False,'drive_crawl_performed':False,
      'canonical_historical_n2n_ids':len(ids),'reddit_semantic_index_records_examined':len(semantic),
      'reddit_semantic_index_joined_n2n_ids':len(sem_join),'pilot_joined_n2n_ids':len(pilot_join),
      'semantic_union_joined_n2n_ids':len(union),'semantic_index_additive_beyond_pilot':len(additive),
      'remaining_without_tracked_semantic_metadata':len(ids)-len(union),
      'semantic_union_coverage_percent':round(100*len(union)/len(ids),4) if ids else 0,
      'semantic_index_columns':list(semantic[0].keys()) if semantic else [],
      'nonempty_joined_values_by_column':dict(field_nonempty),
      'warning':'Coverage means metadata is present in tracked repository indexes, not that Reddit API existence has been verified.'}
    O.mkdir(exist_ok=True); (O/'n2n-semantic-expansion-v0.2.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8'); print(json.dumps(report,indent=2))
if __name__=='__main__':main()
