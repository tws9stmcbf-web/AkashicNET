#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / 'references' / 'community'
BATCH = COMMUNITY / 'wikispine-batch-k-historical-figures-v0.7.10.json'
AGG = COMMUNITY / 'wikispine-entity-aggregate-v0.7.10.json'


def main() -> int:
    batch = json.loads(BATCH.read_text(encoding='utf-8'))
    agg = json.loads(AGG.read_text(encoding='utf-8'))
    assert batch['version'] == '0.7.10'
    rows = batch['records']
    assert len(rows) == 10
    qids = []
    labels = []
    for r in rows:
        assert r['entity_type'] == 'PERSON'
        assert r['resolution_state'] == 'RESOLVED_HIGH_PRECISION'
        assert r['wikidata_qid'].startswith('Q') and r['wikidata_qid'][1:].isdigit()
        assert r['reference_class'] == 'REFERENCE_ENCYCLOPEDIA'
        assert r['semantic_decision'] == 'REFERENCE_IDENTITY_ONLY'
        assert r['truth_inference'] is False
        assert r['scientific_evidence'] is False
        qids.append(r['wikidata_qid'])
        labels.append(r['akashic_entity'].casefold())
    assert len(qids) == len(set(qids))
    assert len(labels) == len(set(labels))
    g = batch['guardrails']
    assert g['candidate_edges_default'] == 'HOLD'
    assert g['max_hops'] == 2
    assert g['arbitrary_recursive_crawl'] is False
    assert g['full_article_body_ingestion_default'] is False
    assert g['rights_promotion_allowed'] is False
    assert g['scientific_evidence_promotion_allowed'] is False
    assert g['truth_inference_allowed'] is False
    assert g['drive_access_performed'] is False

    assert agg['resolved_high_precision'] == 41
    assert agg['resolved_by_type'] == {'PERSON': 30, 'WORK': 11}
    assert agg['pending_resolution'] == 2
    assert len(agg['source_batches']) == 5
    ag = agg['guardrails']
    assert ag['entity_identity_is_truth'] is False
    assert ag['candidate_edges_default'] == 'HOLD'
    assert ag['rights_promotion_allowed'] is False
    assert ag['scientific_evidence_promotion_allowed'] is False
    assert ag['truth_inference_allowed'] is False
    assert ag['drive_access_performed'] is False
    print('AKASHICNET v0.7.10 WIKISPINE HISTORICAL FIGURES PASS', {
        'new_person_identities': 10,
        'typed_entity_resolved_total': 41,
        'persons_total': 30,
        'works_total': 11,
        'pending': 2,
    })
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
