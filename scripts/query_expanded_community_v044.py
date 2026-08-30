#!/usr/bin/env python3
from __future__ import annotations

import argparse,base64,hashlib,json,re
from pathlib import Path
import csv

INDEX=Path('data/n2n-expanded-index-v0.40.csv')
VERSION='0.44'
MAX_PAGE=100


def tokens(s:str)->list[str]:
    return [x for x in re.findall(r'[a-z0-9]+',(s or '').lower()) if len(x)>=2]


def score(row:dict,query:str)->tuple[int,dict]:
    q=(query or '').strip().lower(); qt=tokens(q)
    title=(row.get('title') or '').lower(); topics=(row.get('topics') or '').lower()
    title_tokens=set(tokens(title)); topic_tokens=set(tokens(topics))
    exact_title=bool(q and q in title)
    title_hits=sum(t in title_tokens for t in qt)
    topic_hits=sum(t in topic_tokens for t in qt)
    value=(100 if exact_title else 0)+(10*title_hits)+topic_hits
    return value,{'exact_title_phrase':exact_title,'title_token_hits':title_hits,'topic_token_hits':topic_hits}


def fp(query:str)->str:
    return hashlib.sha256(query.strip().lower().encode()).hexdigest()[:20]


def enc(fingerprint:str,offset:int)->str:
    raw=json.dumps({'f':fingerprint,'o':offset},separators=(',',':')).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip('=')


def dec(cursor:str,fingerprint:str)->int:
    try:
        raw=base64.urlsafe_b64decode(cursor+'='*((4-len(cursor)%4)%4)); obj=json.loads(raw)
        if obj.get('f')!=fingerprint: raise ValueError
        o=int(obj['o']); assert o>=0; return o
    except Exception as exc: raise ValueError('invalid cursor for this query') from exc


def main():
    p=argparse.ArgumentParser(description='AkashicNET expanded community metadata search v0.44')
    p.add_argument('query'); p.add_argument('--page-size',type=int,default=20); p.add_argument('--cursor',default='')
    a=p.parse_args()
    if not a.query.strip(): p.error('query is required')
    if not 1<=a.page_size<=MAX_PAGE: p.error('--page-size must be 1..100')
    rows=list(csv.DictReader(INDEX.open(encoding='utf-8',newline='')))
    ranked=[]
    for r in rows:
        s,why=score(r,a.query)
        if s<=0: continue
        ranked.append((s,r,why))
    ranked.sort(key=lambda x:(-x[0],x[1]['community_id']))
    fingerprint=fp(a.query); offset=dec(a.cursor,fingerprint) if a.cursor else 0
    page=ranked[offset:offset+a.page_size]; next_offset=offset+len(page)
    results=[]
    for s,r,why in page:
        results.append({
            'result_id':r['community_id'],'canonical_url':r['canonical_url'],'title':r['title'],
            'author':r['author'],'topics':r['topics'],'source_type':r['source_type'],
            'relevance_score':s,'ranking_basis':why,
            'review_state':'unreviewed','semantic_status':'UNADJUDICATED',
            'rights_status':'UNKNOWN_UNVERIFIED','scientific_evidence_status':'NOT_EVALUATED',
        })
    out={
        'service':'AKASHICNET_EXPANDED_COMMUNITY_SEARCH','version':VERSION,
        'visibility':'internal_metadata_research','query':a.query,
        'pagination':{'offset':offset,'page_size':a.page_size,'total_matches':len(ranked),'returned':len(results),'next_cursor':enc(fingerprint,next_offset) if next_offset<len(ranked) else None},
        'ranking_policy':{'title_phrase_weight':100,'title_token_weight':10,'topic_token_weight':1,'ranking_is_truth_score':False,'ranking_is_evidence_score':False},
        'results':results,
        'guardrails':{'body_reads':0,'embeddings':0,'semantic_auto_acceptance':False,'truth_inference':False,'rights_promotion':False,'scientific_evidence_promotion':False},
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
