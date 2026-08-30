#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'references/community/sanitized-topic-label-schema-v0.7.6.json'
FIXTURE = ROOT / 'tests/fixtures/sanitized-topic-label-v0.7.6.json'
FORBIDDEN = {'drive_id','parent_drive_id','collection_path','filename','object_name','document_body','email','user_name','private_url'}
ALLOWED = {'topic_label','source_class','review_state'}

schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
data = json.loads(FIXTURE.read_text(encoding='utf-8'))

assert schema['$id'] == 'akashicnet://schemas/sanitized-topic-label/v0.7.6'
assert data['schema_version'] == '0.7.6'
assert data['fixture_only'] is True
assert isinstance(data['records'], list) and data['records']

for row in data['records']:
    assert set(row) == ALLOWED
    assert not (set(row) & FORBIDDEN)
    assert row['topic_label'].strip()
    assert row['source_class'] in {'DRIVE_COLLECTION_LABEL','OTHER_SANITIZED_METADATA'}
    assert row['review_state'] in {'REVIEWED','HOLD'}

# Deliberately hostile synthetic row must fail the boundary.
hostile = {'topic_label':'Synthetic','source_class':'DRIVE_COLLECTION_LABEL','review_state':'REVIEWED','drive_id':'FORBIDDEN'}
assert set(hostile) != ALLOWED
assert set(hostile) & FORBIDDEN

print('AKASHICNET v0.7.6 SANITIZED TOPIC BRIDGE PASS', {
    'fixture_records': len(data['records']),
    'fixture_only': True,
    'forbidden_fields': len(FORBIDDEN),
    'drive_access_performed': False,
    'production_snapshot_present': False,
    'truth_inference': False,
    'rights_promotion': False,
    'scientific_evidence_promotion': False,
})
