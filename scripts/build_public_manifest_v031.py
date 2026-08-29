#!/usr/bin/env python3
import csv, json
from pathlib import Path

ledger_path = Path('references/community/drive-rights-provenance-ledger.csv')
fixture_path = Path('references/community/rights-verification-fixtures-v0.30.csv')
out_path = Path('data/public-manifest-v0.31.json')

with ledger_path.open(encoding='utf-8', newline='') as f:
    ledger = list(csv.DictReader(f))
with fixture_path.open(encoding='utf-8', newline='') as f:
    fixtures = list(csv.DictReader(f))

entries = []
excluded = []
for row in ledger:
    eligible = row.get('public_status') == 'PUBLIC_VERIFIED' and row.get('public_manifest_eligible','').upper() == 'YES'
    if eligible:
        entries.append({
            'audit_id': row['audit_id'],
            'scope': row['scope'],
            'public_status': row['public_status'],
            'rights_basis': row['rights_basis'],
            'licence_evidence': row['licence_evidence'],
            'provenance_evidence': row['provenance_evidence'],
        })
    else:
        excluded.append({'record_id': row['audit_id'], 'source': 'production_rights_ledger', 'reason': 'PUBLIC_VERIFIED_AND_MANIFEST_ELIGIBLE_REQUIRED'})

for row in fixtures:
    excluded.append({'record_id': row['fixture_id'], 'source': 'fixture_only', 'reason': 'FIXTURE_NEVER_PRODUCTION_MANIFEST_ELIGIBLE'})

payload = {
    'manifest': 'AKASHICNET_PUBLIC_MANIFEST',
    'version': '0.31',
    'policy': {
        'required_public_status': 'PUBLIC_VERIFIED',
        'requires_manifest_eligible': True,
        'fixtures_allowed': False,
        'unknown_unverified_allowed': False,
        'rights_inference_allowed': False,
        'truth_inference_allowed': False,
        'scientific_evidence_promotion_allowed': False,
    },
    'counts': {
        'production_rights_records_examined': len(ledger),
        'fixture_records_examined_for_exclusion': len(fixtures),
        'public_manifest_entries': len(entries),
        'excluded_records': len(excluded),
    },
    'entries': entries,
    'excluded_audit': excluded,
}
assert all(x['public_status'] == 'PUBLIC_VERIFIED' for x in entries)
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(payload['counts'], sort_keys=True))
