#!/usr/bin/env python3
from __future__ import annotations

import argparse,base64,hashlib,json,subprocess

API_NAME='AKASHICNET_RETRIEVAL_API'
API_VERSION='0.36'
SCHEMA_ID='akashicnet://schemas/retrieval/v0.36'
MAX_PAGE_SIZE=100
MAX_SCAN=1000


def logical_identity(row:dict)->dict:
    return {
        'domain':row.get('domain'),
        'canonical_family_id':row.get('canonical_family_id'),
        'logical_unit_id':row.get('logical_unit_id'),
        'source_ref':row.get('source_ref'),
        'concept_id':row.get('concept_id'),
        'query_path':row.get('query_path'),
        'title':row.get('title'),
        'label':row.get('label'),
    }


def stable_id(row:dict)->str:
    raw=json.dumps(logical_identity(row),sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
    return 'akn_'+hashlib.sha256(raw).hexdigest()[:24]


def sort_key(row:dict):
    profile=row.get('evidence_profile') or {}
    rank=profile.get('provenance_rank')
    if rank is None:
        tier=profile.get('provenance_tier','')
        rank={'P3_SHA256_IDENTITY_PROVENANCE':3,'P2_MANIFESTATION_PROVENANCE':2,'P1_REVIEWED_TOPICAL':1,'P0_TOPICAL_CANDIDATE':0}.get(tier,0)
    decision_order={'DIRECT_METADATA_LOOKUP':0,'ACCEPT':1,'HOLD':2,'REJECT':3,'UNSPECIFIED':4}
    return (-int(rank),decision_order.get(row.get('semantic_decision'),9),row.get('domain') or '',stable_id(row))


def fingerprint(query:str,domain:str,state:str)->str:
    raw=json.dumps({'q':query,'domain':domain,'state':state},sort_keys=True,separators=(',',':')).encode()
    return hashlib.sha256(raw).hexdigest()[:20]


def encode_cursor(fp:str,offset:int)->str:
    raw=json.dumps({'f':fp,'o':offset},separators=(',',':')).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip('=')


def decode_cursor(value:str,expected_fp:str)->int:
    try:
        raw=base64.urlsafe_b64decode(value+'='*((4-len(value)%4)%4))
        obj=json.loads(raw)
        if obj.get('f')!=expected_fp: raise ValueError
        offset=int(obj['o'])
        if offset<0: raise ValueError
        return offset
    except Exception as exc:
        raise ValueError('invalid cursor for this query') from exc


def main():
    p=argparse.ArgumentParser(description='AkashicNET retrieval API v0.36 with stable IDs and pagination')
    p.add_argument('query')
    p.add_argument('--domain',choices=['all','reddit','library'],default='all')
    p.add_argument('--state',choices=['all','accepted','hold'],default='all')
    p.add_argument('--page-size',type=int,default=20)
    p.add_argument('--cursor',default='')
    a=p.parse_args()
    if not 1<=a.page_size<=MAX_PAGE_SIZE: p.error('--page-size must be between 1 and 100')

    cmd=['python','scripts/query_api_v025.py',a.query,'--domain',a.domain,'--state',a.state,'--limit',str(MAX_SCAN)]
    upstream=json.loads(subprocess.check_output(cmd,text=True))
    rows=[dict(r) for r in upstream['results']]
    for r in rows: r['result_id']=stable_id(r)
    rows.sort(key=sort_key)

    fp=fingerprint(a.query,a.domain,a.state)
    offset=decode_cursor(a.cursor,fp) if a.cursor else 0
    page=rows[offset:offset+a.page_size]
    next_offset=offset+len(page)
    next_cursor=encode_cursor(fp,next_offset) if next_offset<len(rows) else None

    out={
        'api':API_NAME,'api_version':API_VERSION,'schema_id':SCHEMA_ID,
        'request':{'query':a.query,'domain':a.domain,'state':a.state,'page_size':a.page_size,'cursor':a.cursor or None},
        'policy':dict(upstream['policy']),
        'pagination':{
            'stable_result_ids':True,
            'stable_sorting':True,
            'cursor_bound_to_query':True,
            'offset':offset,
            'page_size':a.page_size,
            'total_results':len(rows),
            'returned':len(page),
            'next_cursor':next_cursor,
        },
        'result_identity':{
            'basis':'logical result identity fields; independent of current rank and list position',
            'not_content_hash':True,
            'not_rights_claim':True,
            'not_truth_claim':True,
        },
        'results':page,
        'compatibility':{
            'source_api':'0.25','semantic_decisions_preserved':True,'provenance_ranking_preserved':True,
            'rights_promotion_allowed':False,'truth_inference_allowed':False,'scientific_evidence_promotion_allowed':False,
        },
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
