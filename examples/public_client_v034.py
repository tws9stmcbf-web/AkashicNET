#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.parse
import urllib.request

CLIENT='AKASHICNET_PUBLIC_CLIENT'
CLIENT_VERSION='0.34'
ALLOWED_PUBLIC_FIELDS={
    'result_id','source_type','title','label','canonical_family_id','concept_id','concept_label',
    'semantic_decision','review_state','query_path','provenance_tier','provenance_rank',
    'logical_unit_count','physical_manifestation_count','sha256_verified_logical_units',
    'public_status','rights_state'
}


def _pick(row: dict) -> dict:
    out={k:row[k] for k in ALLOWED_PUBLIC_FIELDS if k in row}
    out.setdefault('public_status', row.get('rights_state','PUBLIC_VERIFIED'))
    return out


def query(base_url: str, text: str, domain: str='all', state: str='all', limit: int=20) -> dict:
    params=urllib.parse.urlencode({
        'q':text,
        'domain':domain,
        'state':state,
        'limit':limit,
        'visibility':'public',
    })
    url=base_url.rstrip('/')+'/v1/retrieve?'+params
    with urllib.request.urlopen(url, timeout=15) as r:
        payload=json.load(r)
    if payload.get('visibility') != 'public':
        raise RuntimeError('server did not enforce public visibility')
    upstream=payload.get('upstream',{})
    gate=upstream.get('public_retrieval_gate',{})
    if gate.get('required_status') != 'PUBLIC_VERIFIED':
        raise RuntimeError('PUBLIC_VERIFIED gate missing')
    rows=[]
    for row in upstream.get('results',[]):
        public_status=row.get('public_status') or row.get('rights_state')
        if public_status and public_status != 'PUBLIC_VERIFIED':
            raise RuntimeError('non-public result crossed public gate')
        rows.append(_pick(row))
    return {
        'client':CLIENT,
        'client_version':CLIENT_VERSION,
        'visibility':'public',
        'required_public_status':'PUBLIC_VERIFIED',
        'query':text,
        'result_count':len(rows),
        'results':rows,
        'suppressed_count':upstream.get('summary',{}).get('public_gate_suppressed_count',0),
        'epistemic_notice':'Topical relevance and provenance strength do not imply truth, scientific validation, safety, efficacy, or rights beyond explicit PUBLIC_VERIFIED status.',
    }


def main() -> None:
    p=argparse.ArgumentParser(description='Minimal public-only AkashicNET client v0.34')
    p.add_argument('query')
    p.add_argument('--base-url', default='http://127.0.0.1:8787')
    p.add_argument('--domain', choices=['all','reddit','library'], default='all')
    p.add_argument('--state', choices=['all','accepted','hold'], default='all')
    p.add_argument('--limit', type=int, default=20)
    a=p.parse_args()
    if a.limit < 1 or a.limit > 100:
        p.error('--limit must be between 1 and 100')
    print(json.dumps(query(a.base_url,a.query,a.domain,a.state,a.limit),ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
