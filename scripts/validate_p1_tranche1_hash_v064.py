#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUMMARY_PATH = ROOT / 'references' / 'community' / 'drive-p1-tranche1-hash-summary-v0.6.4.json'
summary = json.loads(SUMMARY_PATH.read_text(encoding='utf-8'))

assert summary['families'] == 10
assert summary['objects'] == 20
assert summary['bytes_hashed'] == 2522992
assert summary['family_results'] == {'BYTE_IDENTICAL_VERIFIED': 10}
assert summary['work_ids_promoted'] == 0
assert summary['edition_ids_promoted'] == 0
assert summary['rights_promoted'] == 0
assert summary['scientific_evidence_promoted'] == 0
assert summary['private_rows_tracked_in_public_repo'] is False
assert summary['acquisition_route'] == 'CONNECTED_GOOGLE_DRIVE_RAW_DOWNLOAD'
assert re.fullmatch(r'[0-9a-f]{64}', summary['private_batch_sha256'])

print('P1 tranche 1 public aggregate proof v0.6.4 validation PASS')
print('families=10 objects=20 bytes=2522992 byte_identical_verified=10 private_rows_tracked=false')
