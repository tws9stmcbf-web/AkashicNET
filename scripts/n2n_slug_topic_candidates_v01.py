#!/usr/bin/env python3
"""Extract conservative topic *candidates* from historical N2N URL slugs.
No network/Drive access. Output is lexical discovery only, never canonical truth.
"""
import csv,json,re,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'references/community/reddit-uri-index.csv'; OUT=ROOT/'artifacts'
RX=re.compile(r'/r/NeuronsToNirvana/comments/([A-Za-z0-9]+)/([^/?#,]+)',re.I)
STOP=set('a an and are as at be by for from has have how i in is it its of on or our that the their this to was we what when where which who why with you your'.split())
def norm(slug):
 s=re.sub(r'[_-]+',' ',slug.lower()); s=re.sub(r'[^a-z0-9 ]+',' ',s); return ' '.join(s.split())
def main():
 rows=list(csv.DictReader(SRC.open(encoding='utf-8-sig',newline=''))); ids={}; tokens=collections.Counter(); phrases=collections.Counter()
 for r in rows:
  m=RX.search(r.get('reddit_url',''))
  if not m: continue
  pid,slug=m.group(1).lower(),norm(m.group(2)); ids.setdefault(pid,slug)
 for slug in ids.values():
  words=[w for w in slug.split() if len(w)>=3 and w not in STOP and not w.isdigit()]
  tokens.update(set(words))
  for n in (2,3): phrases.update(set(' '.join(words[i:i+n]) for i in range(len(words)-n+1)))
 cand=[{'candidate':k,'document_frequency':v,'candidate_type':'slug_token','status':'candidate_topic','provenance':'historical_reddit_url_slug'} for k,v in tokens.most_common() if v>=3]
 cand += [{'candidate':k,'document_frequency':v,'candidate_type':'slug_phrase','status':'candidate_topic','provenance':'historical_reddit_url_slug'} for k,v in phrases.most_common() if v>=2]
 cand.sort(key=lambda x:(-x['document_frequency'],x['candidate']))
 OUT.mkdir(exist_ok=True)
 fields=['candidate','document_frequency','candidate_type','status','provenance']
 with (OUT/'n2n-slug-topic-candidates-v0.1.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(cand)
 summary={'version':'0.1','network_access_performed':False,'drive_crawl_performed':False,'canonical_n2n_ids_with_slugs':len(ids),'candidate_rows':len(cand),'token_candidates':sum(x['candidate_type']=='slug_token' for x in cand),'phrase_candidates':sum(x['candidate_type']=='slug_phrase' for x in cand),'status':'candidate_topic','warning':'Lexical candidates are not canonical topics and require deduplication/adjudication before Topic Census inclusion.'}
 (OUT/'n2n-slug-topic-candidates-v0.1.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8'); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
