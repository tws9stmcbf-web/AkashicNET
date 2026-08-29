#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import subprocess

EXPECTED_API = 'AKASHICNET_RETRIEVAL_API'
EXPECTED_SCHEMA = 'akashicnet://schemas/retrieval/v0.25'
REQUIRED_TOP_LEVEL = {
    'api','api_version','schema_id','request','policy','summary','results','compatibility'
}


def retrieve(query: str, domain: str = 'all', state: str = 'all', limit: int = 20) -> dict:
    cmd = [
        'python', 'scripts/query_api_v025.py', query,
        '--domain', domain, '--state', state, '--limit', str(limit),
    ]
    payload = json.loads(subprocess.check_output(cmd, text=True))
    missing = REQUIRED_TOP_LEVEL - set(payload)
    if missing:
        raise RuntimeError(f'missing stable API fields: {sorted(missing)}')
    if payload['api'] != EXPECTED_API:
        raise RuntimeError(f"unexpected API name: {payload['api']}")
    if payload['schema_id'] != EXPECTED_SCHEMA:
        raise RuntimeError(f"unsupported schema: {payload['schema_id']}")
    return payload


def main() -> None:
    p = argparse.ArgumentParser(description='Minimal AkashicNET retrieval API consumer')
    p.add_argument('query')
    p.add_argument('--domain', choices=['all','reddit','library'], default='all')
    p.add_argument('--state', choices=['all','accepted','hold'], default='all')
    p.add_argument('--limit', type=int, default=20)
    a = p.parse_args()

    data = retrieve(a.query, a.domain, a.state, a.limit)
    compact = {
        'api_version': data['api_version'],
        'schema_id': data['schema_id'],
        'query': data['request']['query'],
        'results_returned': data['summary']['results_returned'],
        'results': [
            {
                'domain': r.get('domain'),
                'semantic_decision': r.get('semantic_decision'),
                'provenance_tier': (r.get('evidence_profile') or {}).get('provenance_tier'),
                'label': r.get('label') or r.get('title') or r.get('canonical_family_label'),
            }
            for r in data['results']
        ],
    }
    print(json.dumps(compact, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
