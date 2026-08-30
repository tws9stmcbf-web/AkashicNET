#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'
BATCH = json.loads((REF / 'wikispine-batch-f-v0.7.4.json').read_text(encoding='utf-8'))
CHECK = json.loads((REF / 'wikispine-checkpoint-v0.7.4.json').read_text(encoding='utf-8'))

assert BATCH['version'] == '0.7.4'
assert BATCH['batch'] == 'F_BRAIN_COGNITION_BIOLOGY'
records = BATCH['records']
assert len(records) == 10
assert len({r['akashic_concept'] for r in records}) == 10
assert len({r['wikidata_qid'] for r in records}) == 10
for r in records:
    assert r['wikidata_qid'].startswith('Q') and r['wikidata_qid'][1:].isdigit()
    assert r['resolution_state'] == 'RESOLVED_HIGH_PRECISION'
    assert r['reference_class'] == 'REFERENCE_ENCYCLOPEDIA'
    assert r['semantic_decision'] == 'REFERENCE_IDENTITY_ONLY'
    assert r['truth_inference'] is False
    assert r['scientific_evidence'] is False

g = BATCH['guardrails']
assert g['candidate_edges_default'] == 'HOLD'
assert g['max_hops'] == 2
assert g['arbitrary_recursive_crawl'] is False
assert g['full_article_body_ingestion_default'] is False
assert g['rights_promotion_allowed'] is False
assert g['scientific_evidence_promotion_allowed'] is False
assert g['truth_inference_allowed'] is False
assert g['drive_access_performed'] is False

assert CHECK['previous_unique_seeds'] == 43
assert CHECK['new_batch_records'] == 10
assert CHECK['unique_seeds'] == 53
assert CHECK['resolved_high_precision'] == 50
assert CHECK['pending'] == 3
assert CHECK['new_duplicate_concepts'] == 0
assert CHECK['new_duplicate_resolved_qids'] == 0
assert CHECK['candidate_edges_default'] == 'HOLD'
assert CHECK['max_hops'] == 2
assert CHECK['arbitrary_recursive_crawl'] is False
assert CHECK['full_article_body_ingestion_default'] is False
assert CHECK['truth_inference_allowed'] is False
assert CHECK['rights_promotion_allowed'] is False
assert CHECK['scientific_evidence_promotion_allowed'] is False
assert CHECK['drive_access_performed'] is False

print('AKASHICNET v0.7.4 WIKISPINE PASS', {
    'new_records': len(records),
    'unique_seeds': CHECK['unique_seeds'],
    'resolved_high_precision': CHECK['resolved_high_precision'],
    'pending': CHECK['pending'],
    'truth_inference': False,
    'rights_promotion': False,
    'scientific_evidence_promotion': False,
    'drive_access': False,
})
