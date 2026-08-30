#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / 'references' / 'community' / 'wikispine-seed-v0.7.0.json'
s = json.loads(P.read_text(encoding='utf-8'))

assert s['version'] == '0.7.0'
assert s['milestone'] == 'WIKISPINE_REFERENCE_BACKBONE_PILOT'
records = s['records']
assert len(records) == 5

qids = []
concepts = []
for r in records:
    qid = r['wikidata_qid']
    assert re.fullmatch(r'Q[1-9][0-9]*', qid), qid
    assert r['wikidata_url'].endswith('/' + qid)
    assert r['wikipedia_url'].startswith('https://en.wikipedia.org/wiki/')
    assert r['resolution_state'] == 'RESOLVED_HIGH_PRECISION'
    assert r['reference_class'] == 'REFERENCE_ENCYCLOPEDIA'
    assert r['semantic_decision'] == 'REFERENCE_IDENTITY_ONLY'
    assert r['truth_inference'] is False
    assert r['scientific_evidence'] is False
    qids.append(qid)
    concepts.append(r['akashic_concept'])

assert len(set(qids)) == len(qids)
assert len(set(concepts)) == len(concepts)
assert set(concepts) == {'Consciousness','Buddhism','Hinduism','Alchemy','Mysticism'}

policy = s['expansion_policy']
assert policy['max_hops'] == 2
assert policy['arbitrary_recursive_crawl'] is False
assert policy['full_article_body_ingestion_default'] is False
assert policy['wikidata_first'] is True
assert policy['candidate_edges_default'] == 'HOLD'
assert policy['revision_provenance_required_for_article_snapshots'] is True
assert policy['rights_promotion_allowed'] is False
assert policy['scientific_evidence_promotion_allowed'] is False
assert policy['truth_inference_allowed'] is False

print('AKASHICNET v0.7.0 WIKISPINE PASS', {
    'resolved_seeds': len(records),
    'unique_qids': len(set(qids)),
    'max_hops': policy['max_hops'],
    'recursive_crawl': policy['arbitrary_recursive_crawl'],
    'full_body_default': policy['full_article_body_ingestion_default'],
    'candidate_edges_default': policy['candidate_edges_default'],
    'truth_inference': policy['truth_inference_allowed'],
    'rights_promotion': policy['rights_promotion_allowed'],
    'scientific_evidence_promotion': policy['scientific_evidence_promotion_allowed'],
})
