#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'

pilot = json.loads((REF / 'wikispine-seed-v0.7.0.json').read_text(encoding='utf-8'))
a = json.loads((REF / 'wikispine-batch-a-v0.7.1.json').read_text(encoding='utf-8'))
b = json.loads((REF / 'wikispine-batch-b-v0.7.1.json').read_text(encoding='utf-8'))
cp = json.loads((REF / 'wikispine-expansion-checkpoint-v0.7.1.json').read_text(encoding='utf-8'))

records = list(pilot['records']) + list(a['records']) + list(b['records'])
assert len(records) == cp['total_seeds'] == 20

concepts = [r['akashic_concept'] for r in records]
assert len(set(concepts)) == len(concepts)

resolved = [r for r in records if r['resolution_state'] == 'RESOLVED_HIGH_PRECISION']
pending = [r for r in records if r['resolution_state'] == 'PENDING_API_RESOLUTION']
assert len(resolved) == cp['resolved_high_precision'] == 17
assert len(pending) == cp['pending_api_resolution'] == 3

qids = [r.get('wikidata_qid') for r in resolved]
assert all(q and q.startswith('Q') and q[1:].isdigit() for q in qids)
assert len(set(qids)) == len(qids)
assert all(r.get('wikidata_qid') is None for r in pending)

for doc in (a, b):
    d = doc['defaults']
    assert d['reference_class'] == 'REFERENCE_ENCYCLOPEDIA'
    assert d['semantic_decision'] == 'REFERENCE_IDENTITY_ONLY'
    assert d['candidate_edges_default'] == 'HOLD'
    assert d['truth_inference'] is False
    assert d['scientific_evidence'] is False
    assert d['rights_promotion'] is False
    assert d['full_article_body_ingestion'] is False

policy = pilot['expansion_policy']
assert policy['max_hops'] == cp['max_hops'] == 2
assert policy['arbitrary_recursive_crawl'] is cp['arbitrary_recursive_crawl'] is False
assert policy['full_article_body_ingestion_default'] is cp['full_article_body_ingestion_default'] is False
assert policy['candidate_edges_default'] == cp['candidate_edges_default'] == 'HOLD'
assert cp['truth_inference_allowed'] is False
assert cp['rights_promotion_allowed'] is False
assert cp['scientific_evidence_promotion_allowed'] is False
assert cp['drive_access_performed'] is False

print('AKASHICNET v0.7.1 WIKISPINE BATCH PASS', {
    'total_seeds': len(records),
    'resolved_high_precision': len(resolved),
    'pending_api_resolution': len(pending),
    'duplicate_concepts': 0,
    'duplicate_resolved_qids': 0,
    'max_hops': 2,
    'candidate_edges_default': 'HOLD',
    'drive_access_performed': False,
})
