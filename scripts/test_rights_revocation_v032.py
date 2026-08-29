#!/usr/bin/env python3
from __future__ import annotations

import csv
import copy
import json
from pathlib import Path
import sys

sys.path.insert(0, 'scripts')
from validate_rights_v030 import rung
from public_retrieval_gate_v029 import apply_public_gate

FIXTURES = Path('references/community/rights-verification-fixtures-v0.30.csv')
SCENARIOS = Path('references/community/rights-revocation-scenarios-v0.32.csv')
OUTPUT = Path('data/rights-revocation-regression-v0.32.json')


def effective_row(base: dict, scenario: dict) -> dict:
    row = copy.deepcopy(base)
    auth_state = scenario['authoritative_evidence_state']
    corr_state = scenario['corroborating_evidence_state']
    scope_state = scenario['scope_state']
    review_state = scenario['review_state']

    if auth_state != 'ACTIVE':
        row['authoritative_evidence'] = ''
        row['corroborating_evidence'] = ''
    elif corr_state != 'ACTIVE':
        row['corroborating_evidence'] = ''

    if scope_state != 'VALID':
        row['jurisdiction_or_scope'] = ''

    if review_state != 'APPROVED':
        row['review_decision'] = 'REVIEW_REQUIRED'

    return row


def main() -> None:
    fixtures = list(csv.DictReader(FIXTURES.open(encoding='utf-8', newline='')))
    scenarios = list(csv.DictReader(SCENARIOS.open(encoding='utf-8', newline='')))
    by_id = {row['fixture_id']: row for row in fixtures}
    results = []

    for scenario in scenarios:
        base = by_id[scenario['base_fixture']]
        row = effective_row(base, scenario)
        effective_rung = rung(row)
        public_status = 'PUBLIC_VERIFIED' if effective_rung == 'R4' else 'UNKNOWN_UNVERIFIED'
        payload = {
            'results': [{
                'result_id': row['manifestation_id'],
                'public_status': public_status,
                'semantic_decision': 'DIRECT_METADATA_LOOKUP',
                'provenance_tier': 'P3_SHA256_IDENTITY_PROVENANCE',
            }],
            'summary': {},
        }
        gated = apply_public_gate(payload, 'public')
        observed_gate_results = len(gated['results'])
        assert effective_rung == scenario['expected_effective_rung'], (scenario['scenario_id'], effective_rung)
        assert public_status == scenario['expected_public_status'], (scenario['scenario_id'], public_status)
        assert observed_gate_results == int(scenario['expected_public_gate_results'])
        results.append({
            'scenario_id': scenario['scenario_id'],
            'effective_rung': effective_rung,
            'public_status': public_status,
            'public_gate_results': observed_gate_results,
            'semantic_decision_preserved': True,
            'provenance_tier_preserved': True,
        })

    baseline = [r for r in results if r['scenario_id'] == 'REV-032-BASELINE'][0]
    downgraded = [r for r in results if r['scenario_id'] != 'REV-032-BASELINE']
    assert baseline['public_gate_results'] == 1
    assert all(r['public_gate_results'] == 0 for r in downgraded)
    assert all(r['public_status'] == 'UNKNOWN_UNVERIFIED' for r in downgraded)

    out = {
        'version': '0.32',
        'scope': 'synthetic-rights-revocation-regression-only',
        'policy': {
            'rights_status_recomputed_from_current_evidence': True,
            'public_visibility_revocable': True,
            'semantic_status_independent_of_rights': True,
            'provenance_strength_independent_of_rights': True,
            'truth_inference_allowed': False,
            'scientific_evidence_promotion_allowed': False,
            'real_corpus_promotions': 0,
        },
        'counts': {
            'scenarios': len(results),
            'baseline_public': baseline['public_gate_results'],
            'downgrade_scenarios': len(downgraded),
            'downgraded_public_results': sum(r['public_gate_results'] for r in downgraded),
        },
        'results': results,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(out['counts'], sort_keys=True))


if __name__ == '__main__':
    main()
