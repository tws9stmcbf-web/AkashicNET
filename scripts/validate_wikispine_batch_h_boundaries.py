#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'references' / 'community' / 'wikispine-batch-h-works-v0.7.7.json'


def validate(payload):
    assert payload['batch'] == 'H_CANONICAL_WORKS'
    guardrails = payload['guardrails']
    assert guardrails['candidate_edges_default'] == 'HOLD'
    assert guardrails['arbitrary_recursive_crawl'] is False
    assert guardrails['full_article_body_ingestion_default'] is False
    assert guardrails['rights_promotion_allowed'] is False
    assert guardrails['scientific_evidence_promotion_allowed'] is False
    assert guardrails['truth_inference_allowed'] is False
    assert guardrails['drive_access_performed'] is False

    for record in payload['records']:
        assert record['resolution_state'] == 'RESOLVED_HIGH_PRECISION'
        assert record['semantic_decision'] == 'REFERENCE_IDENTITY_ONLY'
        assert record['truth_inference'] is False
        assert record['scientific_evidence'] is False
        qid = record.get('wikidata_qid', '')
        assert qid.startswith('Q') and qid[1:].isdigit(), f'invalid verified QID: {qid}'

    for record in payload['pending_records']:
        assert record['resolution_state'] == 'PENDING_VERIFIED_QID'
        assert 'wikidata_qid' not in record, 'pending record must not carry an unverified QID'
        assert record.get('reason'), 'pending record requires an explicit reason'

    resolved_names = {r['akashic_entity'] for r in payload['records']}
    pending_names = {r['akashic_entity'] for r in payload['pending_records']}
    assert resolved_names.isdisjoint(pending_names), 'work cannot be both resolved and pending'
    return True


def main():
    payload = json.loads(DATA.read_text(encoding='utf-8'))
    validate(payload)
    print('AKASHICNET WIKISPINE BATCH H BOUNDARY PASS', {'resolved': len(payload['records']), 'pending': len(payload['pending_records']), 'truth_inference': False, 'drive_access': False})


if __name__ == '__main__':
    main()
