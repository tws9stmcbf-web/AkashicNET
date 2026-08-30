#!/usr/bin/env python3
"""Exact lexical matching of canonical WikiSpine labels against historical N2N slugs.
No semantic inference, network access or Drive crawl. Exact/alias lexical evidence only.
"""
import csv,json,re,collections
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
URI=ROOT/'references/community/reddit-uri-index.csv'
WIKI=ROOT/'references/topics/wikispine-topic-identities-v0.7.4.json'
OUT=ROOT/'artifacts'
RX=re.compile(r'/r/NeuronsToNirvana/comments/([A-Za-z0-9]+)/([^/?#,]+)',re.I)
ALIASES={
 'qabbalah':['qabbalah','kabbalah'],
 'non duality':['non duality','nonduality'],
 'near death experience':['near death experience','nde','ndes'],
 'dimethyltryptamine':['dimethyltryptamine','dmt'],
 '5 meo dmt':['5 meo dmt','5meodmt','5 meo dmt'],
 'lsd':['lsd'],
 'dna':['dna'],
}
def norm(s):
 s=s.lower().replace('&',' and ')
 s=re.sub(r'[_-]+',' ',s); s=re.sub(r'[^a-z0-9 ]+',' ',s)
 return ' '.join(s.split())
def contains_phrase(text,phrase):
 return re.search(r'(?<![a-z0-9])'+re.escape(phrase)+r'(?![a-z0-9])',text) is not None
def main():
 data=json.loads(WIKI.read_text(encoding='utf-8'))
 seeds=[{'label':r[0],'qid':r[1],'identity_status':r[2]} for r in data['records']]
 slugs={}
 for row in csv.DictReader(URI.open(encoding='utf-8-sig',newline='')):
  m=RX.search(row.get('reddit_url',''))
  if m: slugs.setdefault(m.group(1).lower(),norm(m.group(2)))
 rows=[]; matched_posts=set()
 for seed in seeds:
  label_norm=norm(seed['label']); aliases=ALIASES.get(label_norm,[label_norm]); hits=[]
  for pid,slug in slugs.items():
   if any(contains_phrase(slug,a) for a in aliases): hits.append(pid)
  matched_posts.update(hits)
  rows.append({'wikispine_label':seed['label'],'qid':seed['qid'] or '', 'identity_status':seed['identity_status'],'matched_post_count':len(hits),'lexical_status':'exact_or_curated_alias_match' if hits else 'no_exact_lexical_match'})
 rows.sort(key=lambda x:(-x['matched_post_count'],x['wikispine_label'].lower()))
 OUT.mkdir(exist_ok=True)
 fields=['wikispine_label','qid','identity_status','matched_post_count','lexical_status']
 with (OUT/'n2n-wikispine-match-v0.1.csv').open('w',encoding='utf-8',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
 summary={'version':'0.1','network_access_performed':False,'drive_crawl_performed':False,'historical_n2n_ids_with_slugs':len(slugs),'wikispine_identities_examined':len(seeds),'wikispine_identities_with_lexical_hits':sum(r['matched_post_count']>0 for r in rows),'wikispine_identities_without_lexical_hits':sum(r['matched_post_count']==0 for r in rows),'unique_n2n_posts_matching_at_least_one_wikispine_identity':len(matched_posts),'warning':'Matches are exact lexical or explicitly curated aliases only. They indicate vocabulary overlap, not claim/evidence/truth relationships.'}
 (OUT/'n2n-wikispine-match-v0.1.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8'); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
