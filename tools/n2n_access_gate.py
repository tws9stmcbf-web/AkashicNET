"""Decide whether another web-reader batch is justified; never fetch or retry."""
import argparse
import json
from pathlib import Path


def decision(results):
    if not results:
        raise ValueError('access evidence is required')
    if any(r.get('http_status') == 429 for r in results):
        return {'action': 'STOP_WEB_READER', 'reason': 'RATE_LIMIT_429',
                'next_step': 'Honor any Retry-After value; use approved API access or an authorized offline export. Do not automatically retry.'}
    if any(r.get('http_status') in (401, 403) for r in results):
        return {'action': 'STOP_WEB_READER', 'reason': 'ACCESS_DENIED',
                'next_step': 'Resolve authorized access before further requests.'}
    new = [r for r in results if r.get('role') != 'control']
    if new and all(r.get('error') == 'DisabledError' for r in new):
        return {'action': 'STOP_WEB_READER', 'reason': 'NO_READABLE_NEW_RECORDS',
                'next_step': 'Use approved API access or an authorized offline export. A readable cached control does not authorize another blind batch.'}
    return {'action': 'BOUNDED_DIAGNOSTIC_ONLY', 'max_requests': 5,
            'reason': 'NO_BULK_ACCESS_ESTABLISHED',
            'next_step': 'Use only source-discovered URLs whose post IDs match the pinned archive. Capture returned metadata separately.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    args = parser.parse_args()
    print(json.dumps(decision(json.loads(args.receipt.read_text())['records']), indent=2))
