#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess

PUBLIC_VERIFIED = 'PUBLIC_VERIFIED'
UNKNOWN_UNVERIFIED = 'UNKNOWN_UNVERIFIED'


def result_public_status(row: dict) -> str:
    """Return only an explicit result-level public status.

    No promotion is inferred from source accessibility, provenance strength,
    SHA-256 identity, authorship, collection membership, or nested metadata.
    """
    for key in ('public_status', 'rights_state'):
        value = row.get(key)
        if isinstance(value, str) and value:
            return value
    rights = row.get('rights_record')
    if isinstance(rights, dict):
        value = rights.get('public_status')
        if isinstance(value, str) and value:
            return value
    return UNKNOWN_UNVERIFIED


def apply_public_gate(payload: dict, visibility: str) -> dict:
    if visibility not in {'internal', 'public'}:
        raise ValueError('visibility must be one of: internal, public')

    rows = list(payload.get('results', []))
    if visibility == 'internal':
        kept = rows
        suppressed = []
    else:
        kept = []
        suppressed = []
        for row in rows:
            status = result_public_status(row)
            if status == PUBLIC_VERIFIED:
                kept.append(row)
            else:
                suppressed.append({
                    'result_id': row.get('result_id') or row.get('source_ref') or row.get('canonical_family_id'),
                    'public_status': status,
                    'reason': 'PUBLIC_VERIFIED_REQUIRED',
                })

    out = dict(payload)
    out['results'] = kept
    summary = dict(payload.get('summary', {}))
    summary['visibility'] = visibility
    summary['results_before_public_gate'] = len(rows)
    summary['results_after_public_gate'] = len(kept)
    summary['public_gate_suppressed_count'] = len(suppressed)
    out['summary'] = summary
    out['public_retrieval_gate'] = {
        'visibility': visibility,
        'required_status': PUBLIC_VERIFIED if visibility == 'public' else None,
        'default_missing_status': UNKNOWN_UNVERIFIED,
        'rights_inference_allowed': False,
        'source_accessibility_implies_public_permission': False,
        'provenance_strength_implies_public_permission': False,
        'sha256_identity_implies_public_permission': False,
        'suppressed': suppressed,
    }
    return out


def main() -> None:
    p = argparse.ArgumentParser(description='AkashicNET public/private retrieval gate v0.29')
    p.add_argument('query')
    p.add_argument('--domain', choices=['all', 'reddit', 'library'], default='all')
    p.add_argument('--state', choices=['all', 'accepted', 'hold'], default='all')
    p.add_argument('--limit', type=int, default=100)
    p.add_argument('--visibility', choices=['internal', 'public'], default='internal')
    a = p.parse_args()

    cmd = [
        'python', 'scripts/query_api_v025.py', a.query,
        '--domain', a.domain,
        '--state', a.state,
        '--limit', str(a.limit),
    ]
    payload = json.loads(subprocess.check_output(cmd, text=True))
    print(json.dumps(apply_public_gate(payload, a.visibility), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
