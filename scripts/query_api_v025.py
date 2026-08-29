#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess

API_NAME='AKASHICNET_RETRIEVAL_API'
API_VERSION='0.25'
SCHEMA_ID='akashicnet://schemas/retrieval/v0.25'


def main():
    p=argparse.ArgumentParser(description='AkashicNET stable retrieval API v0.25')
    p.add_argument('query')
    p.add_argument('--domain',choices=['all','reddit','library'],default='all')
    p.add_argument('--state',choices=['all','accepted','hold'],default='all')
    p.add_argument('--limit',type=int,default=100)
    a=p.parse_args()
    if a.limit < 1:
        p.error('--limit must be >= 1')

    cmd=['python','scripts/query_unified_v024.py',a.query,'--domain',a.domain,'--state',a.state,'--limit',str(a.limit)]
    upstream=json.loads(subprocess.check_output(cmd,text=True))

    out={
        'api':API_NAME,
        'api_version':API_VERSION,
        'schema_id':SCHEMA_ID,
        'request':upstream['request'],
        'policy':upstream['policy'],
        'summary':upstream['summary'],
        'results':upstream['results'],
        'compatibility':{
            'source_contract':upstream['contract'],
            'source_contract_version':upstream['version'],
            'semantic_decisions_preserved':True,
            'provenance_ranking_preserved':True,
            'consumer_contract_is_versioned':True,
        },
    }
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
