#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'
batch = json.loads((REF / 'wikispine-batch-e-science-v0.7.3.json').read_text(encoding='utf-8'))
agg = json.loads((REF / 'wikispine-aggregate-v0.7.3.json').read_text(encoding='utf-8'))

assert batch['version'] == '0.7.3'
assert batch['batch'] == 'E_SCIENCE_CONSCIOUSNESS_COSMOLOGY'
records = batch['records']
assert len(records) == 10
assert len({r['akashic_concept'] for r in records}) == 10
assert len({r['wikidata_qid'] for r in records}) == 10
assert all(r['wikidata_qid'].startswith('Q') and r['wikidata_qid'][1:].isdigit() for r in records)

expected = {
    'Physics':'Q413',
    'Quantum mechanics':'Q944',
    'Cosmology':'Q338',
    'Astronomy':'Q333',
    'Astrophysics':'Q37547',
    'Biology':'Q420',
    'Evolution':'Q1063',
    'Dark matter':'Q79925',
    'Dark energy':'Q18343',
    'Universe':'Q1',
}
assert {r['akashic_concept']: r['wikidata_qid'] for r in records} == expected

defaults = batch['record_defaults']
assert defaults['resolution_state'] == 'RESOLVED_HIGH_PRECISION'
assert defaults['reference_class'] == 'REFERENCE_ENCYCLOPEDIA'
assert defaults['semantic_decision'] == 'REFERENCE_IDENTITY_ONLY'
assert defaults['truth_inference'] is False
assert defaults['scientific_evidence'] is False

for p in (batch['guardrails'], agg['policies']):
    assert p['candidate_edges_default'] == 'HOLD'
    assert p['max_hops'] == 2
    assert p['arbitrary_recursive_crawl'] is False
    assert p['full_article_body_ingestion_default'] is False
    assert p['truth_inference_allowed'] is False
    assert p['rights_promotion_allowed'] is False
    assert p['scientific_evidence_promotion_allowed'] is False
    assert p['drive_access_performed'] is False

assert agg['previous_total_seeds'] == 33
assert agg['new_batch_seeds'] == 10
assert agg['total_unique_seeds'] == 43
assert agg['resolved_high_precision'] == 40
assert agg['pending_resolution'] == 3
assert agg['duplicate_resolved_qids'] == 0
assert len(agg['pending_preserved_from_v0_7_2']) == 3

print('AKASHICNET v0.7.3 WIKISPINE PASS', {
    'total_unique_seeds': 43,
    'resolved_high_precision': 40,
    'pending_resolution': 3,
    'new_science_cosmology_seeds': 10,
    'candidate_edges_default': 'HOLD',
    'truth_inference': False,
    'rights_promotion': False,
    'scientific_evidence_promotion': False,
    'drive_access': False,
})
