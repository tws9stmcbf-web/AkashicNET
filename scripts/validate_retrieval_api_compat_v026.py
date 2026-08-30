#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'

REQUIRED_POLICY_PHRASES = (
    'remove a required top-level field',
    'reinterpret `DIRECT_METADATA_LOOKUP` as semantic `ACCEPT`',
    'make provenance ranking alter semantic decisions',
    'turn HOLD into ACCEPT without an explicit reviewed/adjudicated change',
    'treat provenance tier as truth, scientific evidence, rights, safety, or efficacy',
    'promote inaccessible/unverified Drive material into a public redistribution manifest',
    'collapse physical manifestations without verified byte identity',
    '`DIRECT_METADATA_LOOKUP is not semantic acceptance`',
)


def validate(policy_text, schema, fixtures):
    for phrase in REQUIRED_POLICY_PHRASES:
        assert phrase.lower() in policy_text.lower(), f'missing compatibility boundary: {phrase}'

    assert schema['properties']['api']['const'] == 'AKASHICNET_RETRIEVAL_API'
    assert schema['properties']['api_version']['const'] == '0.25'
    assert schema['properties']['schema_id']['const'] == 'akashicnet://schemas/retrieval/v0.25'

    top_required = set(schema['required'])
    for key in {'api', 'api_version', 'schema_id', 'request', 'policy', 'summary', 'results', 'compatibility'}:
        assert key in top_required, f'missing stable top-level field: {key}'

    decisions = set(schema['properties']['results']['items']['properties']['semantic_decision']['enum'])
    assert {'ACCEPT', 'HOLD', 'DIRECT_METADATA_LOOKUP'}.issubset(decisions)

    invariants = fixtures['invariants']
    assert invariants['truth_inference_allowed'] is False
    assert invariants['rights_promotion_allowed'] is False
    assert invariants['scientific_evidence_promotion_allowed'] is False
    assert invariants['ranking_changes_semantic_decision'] is False
    assert invariants['direct_metadata_lookup_is_not_semantic_acceptance'] is True
    assert invariants['hold_results_are_explicitly_addressable'] is True

    return True


def main():
    policy = (REF / 'retrieval-api-compatibility-policy-v0.26.md').read_text(encoding='utf-8')
    schema = json.loads((REF / 'unified-retrieval-schema-v0.25.json').read_text(encoding='utf-8'))
    fixtures = json.loads((REF / 'retrieval-fixtures-v0.25.json').read_text(encoding='utf-8'))
    validate(policy, schema, fixtures)
    print('AKASHICNET RETRIEVAL API COMPATIBILITY v0.26 PASS', {'api_version': '0.25', 'truth_inference': False, 'rights_promotion': False, 'scientific_evidence_promotion': False})


if __name__ == '__main__':
    main()
