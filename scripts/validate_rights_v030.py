#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path

INPUT = Path('references/community/rights-verification-fixtures-v0.30.csv')
OUTPUT = Path('data/rights-verification-v0.30.json')
VALID_BASES = {'PUBLIC_DOMAIN', 'EXPLICIT_LICENCE', 'OWNER_AUTHORISED'}


def rung(row: dict) -> str:
    if not row.get('source_provenance'):
        return 'R0'
    if not row.get('rights_basis'):
        return 'R0'
    if not row.get('manifestation_description'):
        return 'R1'
    if not row.get('authoritative_evidence') or not row.get('jurisdiction_or_scope'):
        return 'R2'
    if not row.get('corroborating_evidence'):
        return 'R3'
    if row.get('corroborating_evidence') == row.get('authoritative_evidence'):
        return 'R3'
    if row.get('review_decision') != 'APPROVE_R4' or not row.get('reviewed_at'):
        return 'R3'
    if row.get('rights_basis') not in VALID_BASES:
        return 'R3'
    return 'R4'


def main() -> None:
    rows = list(csv.DictReader(INPUT.open(encoding='utf-8')))
    evaluated = []
    for row in rows:
        computed = rung(row)
        public_status = 'PUBLIC_VERIFIED' if computed == 'R4' else 'UNKNOWN_UNVERIFIED'
        evaluated.append({
            'fixture_id': row['fixture_id'],
            'manifestation_id': row['manifestation_id'],
            'fixture_only': row['fixture_only'] == 'YES',
            'corpus_item': row['corpus_item'] == 'YES',
            'computed_rung': computed,
            'declared_rung': row['declared_rung'],
            'computed_public_status': public_status,
            'declared_public_status': row['declared_public_status'],
            'production_manifest_eligible': row['production_manifest_eligible'] == 'YES',
            'rights_basis': row['rights_basis'],
            'authoritative_evidence': row['authoritative_evidence'],
            'corroborating_evidence': row['corroborating_evidence'],
            'jurisdiction_or_scope': row['jurisdiction_or_scope'],
            'review_decision': row['review_decision'],
        })

    assert rows, 'fixture ledger must not be empty'
    assert all(x['computed_rung'] == x['declared_rung'] for x in evaluated)
    assert all(x['computed_public_status'] == x['declared_public_status'] for x in evaluated)
    r4 = [x for x in evaluated if x['computed_rung'] == 'R4']
    assert len(r4) == 1
    assert r4[0]['computed_public_status'] == 'PUBLIC_VERIFIED'
    assert r4[0]['fixture_only'] is True
    assert r4[0]['corpus_item'] is False
    assert r4[0]['production_manifest_eligible'] is False

    out = {
        'version': '0.30',
        'policy': {
            'public_verified_requires_r4': True,
            'rights_inference_allowed': False,
            'fixture_r4_may_enter_test_gate': True,
            'fixture_r4_may_enter_production_manifest': False,
            'truth_inference_allowed': False,
            'scientific_evidence_promotion_allowed': False,
        },
        'counts': {
            'fixtures': len(evaluated),
            'r4': len(r4),
            'public_verified': sum(x['computed_public_status'] == 'PUBLIC_VERIFIED' for x in evaluated),
            'production_manifest_eligible': sum(x['production_manifest_eligible'] for x in evaluated),
        },
        'records': evaluated,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(out['counts'], sort_keys=True))


if __name__ == '__main__':
    main()
