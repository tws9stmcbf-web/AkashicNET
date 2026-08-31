#!/usr/bin/env python3
import json
import re
from pathlib import Path

P = Path('references/community/drive-p1-small-batch5-hash-summary-v0.6.15.json')
TOTAL_REVIEW_FAMILIES = 126
FORBIDDEN_PUBLIC_KEYS = {
    'drive_id', 'drive_ids', 'file_id', 'file_ids', 'filename', 'filenames',
    'path', 'paths', 'timestamp', 'timestamps', 'object_sha256',
    'object_sha256s', 'per_object_sha256', 'per_object_digests'
}


def fail(msg):
    raise ValueError(msg)


def _walk_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield str(key).lower()
            yield from _walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk_keys(child)


def validate(d):
    expected = {
        'version': '0.6.15',
        'tranche': 'P1_SMALL_BATCH5_OVERALL_ROWS_77_81',
        'acquisition_route': 'CONNECTED_GOOGLE_DRIVE_RAW_DOWNLOAD',
        'families': 5,
        'objects': 10,
        'bytes_hashed': 38013254,
        'hash_failures': 0,
        'private_rows_tracked_in_public_repo': False,
        'authoritative_unique_families_before': 76,
        'authoritative_unique_families_after': 81,
        'unresolved_before': 50,
        'unresolved_after': 45,
        'work_ids_promoted': 0,
        'edition_ids_promoted': 0,
        'rights_promoted': 0,
        'scientific_evidence_promoted': 0,
    }
    for k, v in expected.items():
        if d.get(k) != v:
            fail(f'{k}: expected {v!r}, got {d.get(k)!r}')

    fr = d.get('family_results')
    if not isinstance(fr, dict):
        fail('family_results missing or malformed')
    if set(fr) != {'BYTE_IDENTICAL_VERIFIED', 'NOT_BYTE_IDENTICAL'}:
        fail('family_results contains unexpected keys')
    if fr.get('BYTE_IDENTICAL_VERIFIED') != 5 or fr.get('NOT_BYTE_IDENTICAL') != 0:
        fail('family result counts incorrect')
    if sum(fr.values()) != d['families']:
        fail('family result counts do not sum to families')

    digest = d.get('private_batch_sha256', '')
    if not re.fullmatch(r'[0-9a-f]{64}', digest):
        fail('private batch digest malformed')

    if d['authoritative_unique_families_before'] + d['unresolved_before'] != TOTAL_REVIEW_FAMILIES:
        fail('pre-batch denominator arithmetic does not equal 126')
    if d['authoritative_unique_families_after'] + d['unresolved_after'] != TOTAL_REVIEW_FAMILIES:
        fail('post-batch denominator arithmetic does not equal 126')
    if d['authoritative_unique_families_after'] - d['authoritative_unique_families_before'] != d['families']:
        fail('authoritative family delta does not equal batch families')
    if d['unresolved_before'] - d['unresolved_after'] != d['families']:
        fail('unresolved family delta does not equal batch families')

    guardrail = d.get('guardrail', '')
    required_guardrail_fragments = (
        'physical byte identity only',
        'canonical work identity',
        'edition identity',
        'rights/public status',
        'truth',
        'scientific-evidence status',
    )
    for fragment in required_guardrail_fragments:
        if fragment not in guardrail:
            fail(f'guardrail missing required boundary: {fragment}')

    forbidden = FORBIDDEN_PUBLIC_KEYS.intersection(_walk_keys(d))
    if forbidden:
        fail(f'private object-level keys must not appear in public summary: {sorted(forbidden)}')

    return True


def main():
    if not P.exists():
        raise SystemExit('FAIL: summary missing')
    try:
        d = json.loads(P.read_text())
        validate(d)
    except (ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f'FAIL: {exc}')
    print('PASS: P1 small batch5 v0.6.15 aggregate is valid')


if __name__ == '__main__':
    main()
