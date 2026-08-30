#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'

SCHEMA = json.loads((REF / 'unified-retrieval-schema-v0.25.json').read_text(encoding='utf-8'))
FIXTURES = json.loads((REF / 'retrieval-fixtures-v0.25.json').read_text(encoding='utf-8'))
EVIDENCE = (ROOT / 'docs' / 'canonical-evidence-v01.md').read_text(encoding='utf-8')

policy_required = set(SCHEMA['properties']['policy']['required'])
for key in {
    'truth_inference_allowed',
    'rights_promotion_allowed',
    'scientific_evidence_promotion_allowed',
    'ranking_changes_semantic_decision',
    'direct_metadata_lookup_is_not_semantic_acceptance',
}:
    assert key in policy_required, f'missing retrieval policy guard: {key}'

result_required = set(SCHEMA['properties']['results']['items']['properties']['contract_guards']['required'])
for key in {
    'ranking_changes_semantic_decision',
    'not_truth_claim',
    'not_scientific_evidence_claim',
    'not_rights_clearance_claim',
    'not_safety_or_efficacy_claim',
}:
    assert key in result_required, f'missing per-result guard: {key}'

invariants = FIXTURES['invariants']
assert invariants['truth_inference_allowed'] is False
assert invariants['rights_promotion_allowed'] is False
assert invariants['scientific_evidence_promotion_allowed'] is False
assert invariants['ranking_changes_semantic_decision'] is False
assert invariants['direct_metadata_lookup_is_not_semantic_acceptance'] is True

# Retrieval provenance is ranking/traceability metadata, not evidence status.
for phrase in [
    'Provenance is not evidence',
    'Semantic connection is not scientific evidence',
    'Archive inclusion is not endorsement',
]:
    assert phrase.lower() in EVIDENCE.lower(), f'missing evidence boundary: {phrase}'

# P3 SHA provenance is the highest retrieval provenance tier but remains identity provenance only.
tier_enum = SCHEMA['properties']['results']['items']['properties']['evidence_profile']['properties']['provenance_tier']['enum']
assert 'P3_SHA256_IDENTITY_PROVENANCE' in tier_enum

print('AKASHICNET v0.7.8 RETRIEVAL EVIDENCE BRIDGE PASS', {
    'retrieval_schema_version': '0.25',
    'truth_inference': False,
    'rights_promotion': False,
    'scientific_evidence_promotion': False,
    'ranking_changes_semantic_decision': False,
    'provenance_is_evidence': False,
})
