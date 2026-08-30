#!/usr/bin/env python3
import json
from pathlib import Path
p=Path('references/community/drive-p1-wave20-reconciliation-v0.6.9.json')
d=json.loads(p.read_text())
assert d['version']=='0.6.9'
assert d['queue_slice']=='rows_31_50'
assert d['families']==20 and d['objects']==40
assert d['deterministic_queue_bytes']==33041612
assert d['authoritative_source']['pr']==40
assert d['authoritative_source']['bytes_hashed']==d['deterministic_queue_bytes']
assert d['authoritative_source']['byte_identical_verified_families']==20
assert d['invalidated_overlap']['pr']==44
assert d['invalidated_overlap']['bytes_hashed']!=d['deterministic_queue_bytes']
assert d['invalidated_overlap']['byte_total_delta']==d['invalidated_overlap']['bytes_hashed']-d['deterministic_queue_bytes']
assert d['incremental_families_resolved_by_pr44']==0
assert d['unresolved_surface_after_authoritative_wave']==75
assert any('physical byte identity only' in x.lower() for x in d['guardrails'])
print('P1 wave20 reconciliation v0.6.9 PASS')
