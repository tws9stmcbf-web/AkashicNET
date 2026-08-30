#!/usr/bin/env python3
import json
from pathlib import Path

p = Path('references/community/wikispine-batch-g1-people-v0.7.7.json')
d = json.loads(p.read_text(encoding='utf-8'))
assert d['version'] == '0.7.7'
assert d['batch'] == 'G1_PEOPLE_01'
records = d['records']
assert len(records) == 5
assert all(r['entity_type'] == 'PERSON' for r in records)
assert all(r['resolution_state'] == 'RESOLVED_HIGH_PRECISION' for r in records)
assert all(r['reference_class'] == 'REFERENCE_ENCYCLOPEDIA' for r in records)
assert all(r['semantic_decision'] == 'REFERENCE_IDENTITY_ONLY' for r in records)
assert all(r['wikidata_qid'].startswith('Q') and r['wikidata_qid'][1:].isdigit() for r in records)
assert len({r['wikidata_qid'] for r in records}) == 5
assert len({r['akashic_entity'].casefold() for r in records}) == 5
assert all(r['truth_inference'] is False for r in records)
assert all(r['scientific_evidence'] is False for r in records)
g = d['guardrails']
assert g['batch_size'] == 5
assert g['candidate_edges_default'] == 'HOLD'
assert g['max_hops'] == 2
assert g['arbitrary_recursive_crawl'] is False
assert g['full_article_body_ingestion_default'] is False
assert g['rights_promotion_allowed'] is False
assert g['scientific_evidence_promotion_allowed'] is False
assert g['truth_inference_allowed'] is False
assert g['drive_access_performed'] is False
print('AKASHICNET v0.7.7 SMALL PEOPLE BATCH PASS', {'resolved': 5, 'entity_type': 'PERSON'})
