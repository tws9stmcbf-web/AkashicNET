#!/usr/bin/env python3
"""Quality-filter N2N slug topic candidates.
Regenerates candidates from tracked historical URLs so CI is self-contained.
Outputs REVIEW candidates only; never promotes canonical topics.
"""
import csv,json,re,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; SRC=ROOT/'references/community/reddit-uri-index.csv'; OUT=ROOT/'artifacts'
RX=re.compile(r'/r/NeuronsToNirvana/comments/([A-Za-z0-9]+)/([^/?#,]+)',re.I)
STOP=set('a an and are as at be been but by can could did do does for from had has have how i if in into is it its may might more most my no not of on one or our out over should so than that the their them then there these they this those to too up us was we were what when where which who why will with would you your'.split())
NOISE=set('amp comments comment reddit post posts crosspost original research source sources link links video videos image images article articles discussion question questions update updates part day days today new first second third'.split())
GENERIC=set('good great best better interesting important possible really much many things thing something anyone everyone people person time way look looking thought thoughts think know says said'.split())
def norm(s):
 s=re.sub(r'[_-]+',' ',s.lower()); s=re.sub(r'[^a-z0-9 ]+',' ',s); return ' '.join(s.split())
def main():
 ids={}
 for r in csv.DictReader(SRC.open(encoding='utf-8-sig',newline='')):
  m=RX.search(r.get('reddit_url',''))
  if m: ids.setdefault(m.group(1).lower(),norm(m.group(2)))
 tok=collections.Counter(); phr=collections.Counter()
 for slug in ids.values():
  ws=[w for w in slug.split() if len(w)>=3 and w not in STOP and not w.isdigit()]
  tok.update(set(ws));
  for n in (2,3): phr.update(set(' '.join(ws[i:i+n]) for i in range(len(ws)-n+1)))
 review=[]; rejected=collections.Counter()
 for kind,counter,min_df in [('slug_token',tok,5),('slug_phrase',phr,3)]:
  for term,df in counter.items():
   words=term.split(); reason=None
   if any(w in NOISE for w in words): reason='platform_or_format_noise'
   elif kind=='slug_token' and term in GENERIC: reason='generic_language'
   elif len(term)<4: reason='too_short'
   elif re.fullmatch(r'[0-9a-f]{6,}',term): reason='identifier_like'
   elif df<min_df: reason='low_document_frequency'
   if reason: rejected[reason]+=1; continue
   review.append({'candidate':term,'document_frequency':df,'candidate_type':kind,'status':'review_candidate','provenance':'historical_reddit_url_slug'})
 review.sort(key=lambda x:(-x['document_frequency'],x['candidate']))
 OUT.mkdir(exist_ok=True)
 fields=['candidate','document_frequency','candidate_type','status','provenance']
 with (OUT/'n2n-topic-review-candidates-v0.1.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(review)
 summary={'version':'0.1','network_access_performed':False,'drive_crawl_performed':False,'historical_n2n_ids_with_slugs':len(ids),'review_candidate_rows':len(review),'review_token_candidates':sum(x['candidate_type']=='slug_token' for x in review),'review_phrase_candidates':sum(x['candidate_type']=='slug_phrase' for x in review),'rejected_reason_counts':dict(sorted(rejected.items())),'status':'review_candidate','warning':'Review candidates are lexical signals only. They are not canonical topics and must be matched/deduplicated/adjudicated before census inclusion.'}
 (OUT/'n2n-topic-review-candidates-v0.1.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8'); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
