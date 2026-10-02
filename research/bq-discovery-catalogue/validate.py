"""Validate the metadata snapshot; does not validate scientific claims."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def normalise(value):
    return re.sub(r'[^a-z0-9]', '', (value or '').lower())

def validate():
    data = json.loads((ROOT / 'catalogue.json').read_text())
    records = data['records']
    assert len(records) == data['totals']['unique_source_records'] == 91
    assert len({r['record_id'] for r in records}) == len(records)
    for key in ('doi', 'source_url', 'title'):
        values = [normalise(r[key]) for r in records if r.get(key)]
        assert len(values) == len(set(values)), f'Duplicate {key}'
    for r in records:
        assert r['title'] and r['source_url'].startswith('https://')
        assert r.get('supports_models', []) == []
        assert r.get('independent_studies_added', 0) == 0
        assert r.get('accepted_edges_added', 0) == 0
        assert r.get('evidence_assessed', False) is False
        assert r.get('article_text_retained', False) is False
        assert r.get('raw_data_collected', False) is False
        assert all(not edge.get('accepted', False) for edge in r.get('suggested_relations', []))
    gates = data['governance']
    assert gates['independent_studies_added'] == gates['accepted_edges_added'] == 0
    for key in ('bq_evidence_status_changed', 'website_updated', 'canonical_evidence_ingested', 'blanket_source_reuse_permission'):
        assert gates[key] is False
    for number, count in ((13, 7), (14, 20), (15, 6), (16, 5)):
        batch = json.loads((ROOT / f'batch-{number:02}.json').read_text())
        batch_records = batch['records']
        assert len(batch_records) == count
        for item in batch_records:
            match = next(r for r in records if r['record_id'] == item['record_id'])
            assert match['title'] == item['title'] and match['doi'] == item['doi']
    return {'passed': True, 'records': len(records), 'duplicate_ids_titles_dois_urls': 0,
            'independent_studies_promoted': 0, 'accepted_edges': 0,
            'website_updated': False, 'scientific_claims_validated': False,
            'checks': ['count and identifiers', 'batch snapshot membership', 'evidence and rights governance', 'no article text or raw data']}

if __name__ == '__main__':
    print(json.dumps(validate(), indent=2))
