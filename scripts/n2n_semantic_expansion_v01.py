#!/usr/bin/env python3
"""N2N semantic expansion v0.1.
Join the 1,000-record semantic pilot to canonical IDs reconstructed from the historical URI archive.
No network or Drive access. Missing metadata remains missing; nothing is inferred.
"""
import csv,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; C=ROOT/'references'/'community'; O=ROOT/'artifacts'
RE=re.compile(r'/comments/([A-Za-z0-9]+)',re.I)
def pid(url):
 m=RE.search(url or ''); return m.group(1).lower() if m else ''
def main():
 pilot=list(csv.DictReader((C/'n2n-pilot-index.csv').open(encoding='utf-8-sig',newline='')))
 archive=list(csv.DictReader((C/'reddit-uri-index.csv').open(encoding='utf-8-sig',newline='')))
 n2n_ids=set()
 for r in archive:
  u=r.get('reddit_url','')
  if '/r/NeuronsToNirvana/comments/' in u:
   x=pid(u)
   if x:n2n_ids.add(x)
 mapped={}; outside=[]
 for r in pilot:
  x=pid(r.get('reddit_url',''))
  if x and x in n2n_ids:mapped[x]=r
  else:outside.append(x or '(missing-id)')
 cats={r.get('category','').strip() for r in mapped.values() if r.get('category','').strip()}
 frameworks={r.get('toolkit_framework','').strip() for r in mapped.values() if r.get('toolkit_framework','').strip()}
 edges={(r.get('category','').strip(),r.get('toolkit_framework','').strip()) for r in mapped.values() if r.get('category','').strip() and r.get('toolkit_framework','').strip()}
 report={'version':'0.1','network_access_performed':False,'drive_crawl_performed':False,'canonical_historical_n2n_ids':len(n2n_ids),'pilot_records_examined':len(pilot),'pilot_records_joined_to_historical_n2n':len(mapped),'pilot_records_outside_or_unmatched':len(outside),'historical_n2n_with_semantic_pilot_metadata':len(mapped),'historical_n2n_without_semantic_pilot_metadata':len(n2n_ids)-len(mapped),'semantic_coverage_percent':round(100*len(mapped)/len(n2n_ids),4) if n2n_ids else 0,'unique_categories_in_join':len(cats),'unique_frameworks_in_join':len(frameworks),'category_framework_edges_in_join':len(edges),'unmatched_pilot_ids':outside,'warning':'Unmapped historical records receive no inferred category, framework, title, author, date or evidence status.'}
 O.mkdir(exist_ok=True); (O/'n2n-semantic-expansion-v0.1.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8'); print(json.dumps(report,indent=2))
if __name__=='__main__':main()
