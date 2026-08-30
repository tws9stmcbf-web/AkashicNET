#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / 'references' / 'community'
FILES = [
    COMMUNITY / 'wikispine-batch-g-people-v0.7.7.json',
    COMMUNITY / 'wikispine-batch-h-works-v0.7.7.json',
]
ALLOWED_TYPES = {'PERSON', 'WORK'}


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> int:
    resolved = []
    pending = []
    for path in FILES:
        obj = load(path)
        assert obj['version'] == '0.7.7'
        g = obj['guardrails']
        assert g['candidate_edges_default'] == 'HOLD'
        assert g['max_hops'] == 2
        assert g['arbitrary_recursive_crawl'] is False
        assert g['full_article_body_ingestion_default'] is False
        assert g['rights_promotion_allowed'] is False
        assert g['scientific_evidence_promotion_allowed'] is False
        assert g['truth_inference_allowed'] is False
        assert g['drive_access_performed'] is False
        for r in obj.get('records', []):
            assert r['entity_type'] in ALLOWED_TYPES
            assert r['resolution_state'] == 'RESOLVED_HIGH_PRECISION'
            assert r['wikidata_qid'].startswith('Q') and r['wikidata_qid'][1:].isdigit()
            assert r['reference_class'] == 'REFERENCE_ENCYCLOPEDIA'
            assert r['semantic_decision'] == 'REFERENCE_IDENTITY_ONLY'
            assert r['truth_inference'] is False
            assert r['scientific_evidence'] is False
            resolved.append(r)
        for r in obj.get('pending_records', []):
            assert r['entity_type'] in ALLOWED_TYPES
            assert r['resolution_state'].startswith('PENDING_')
            assert 'wikidata_qid' not in r
            pending.append(r)

    labels = [r['akashic_entity'].casefold() for r in resolved]
    qids = [r['wikidata_qid'] for r in resolved]
    assert len(labels) == len(set(labels)), 'duplicate resolved entity labels'
    assert len(qids) == len(set(qids)), 'duplicate resolved QIDs'
    assert len(resolved) == 13
    assert len(pending) == 2
    assert sum(r['entity_type'] == 'PERSON' for r in resolved) == 10
    assert sum(r['entity_type'] == 'WORK' for r in resolved) == 3
    print('AKASHICNET v0.7.7 WIKISPINE ENTITY BATCH PASS', {
        'resolved_high_precision': len(resolved),
        'persons': 10,
        'works': 3,
        'pending': len(pending),
        'truth_inference': False,
        'rights_promotion': False,
        'scientific_evidence_promotion': False,
        'drive_access': False,
    })
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
