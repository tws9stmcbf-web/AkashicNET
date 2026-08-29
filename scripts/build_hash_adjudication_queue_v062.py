#!/usr/bin/env python3
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'
OUT = REF / 'hash-adjudication-queue-v0.6.2.csv'


def read_csv(name):
    with (REF / name).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

families = read_csv('drive-canonical-family-review-v0.6.0.csv')
objects = read_csv('drive-canonical-object-ledger-v0.6.0.csv')

members = defaultdict(list)
for obj in objects:
    fid = obj['candidate_family_id']
    if fid:
        members[fid].append(obj)

review = [f for f in families if f['review_state'] == 'REVIEW_REQUIRED']
assert len(families) == 127, f'expected 127 exact name+size families, got {len(families)}'
assert len(review) == 126, f'expected 126 review families, got {len(review)}'
assert sum(int(f['object_count']) for f in review) == 258, 'expected 258 objects in review families'

queue = []
for family in review:
    fid = family['candidate_family_id']
    group = members[fid]
    expected = int(family['object_count'])
    assert len(group) == expected, f'{fid}: ledger members {len(group)} != family count {expected}'
    assert len({o['name'] for o in group}) == 1, f'{fid}: names differ'
    assert len({o['size'] for o in group}) == 1, f'{fid}: sizes differ'
    member_size = int(family['size'])
    total_bytes = member_size * expected
    if expected >= 3:
        priority = 'P0_MULTIPLICITY'
    elif total_bytes <= 10 * 1024 * 1024:
        priority = 'P1_LOW_COST'
    elif total_bytes <= 100 * 1024 * 1024:
        priority = 'P2_MEDIUM_COST'
    else:
        priority = 'P3_HIGH_COST'
    queue.append({
        'candidate_family_id': fid,
        'priority': priority,
        'name': family['name'],
        'member_size_bytes': member_size,
        'object_count': expected,
        'total_bytes_to_hash': total_bytes,
        'drive_ids': ';'.join(sorted(o['drive_id'] for o in group)),
        'parent_paths': ';'.join(sorted({o['parent_path'] for o in group})),
        'action': 'COMPUTE_SHA256_ALL_MEMBERS',
        'byte_identity_rule': 'ALL_HASHES_EQUAL=>BYTE_IDENTICAL_VERIFIED;ELSE=>NOT_BYTE_IDENTICAL',
        'canonical_rule': 'HASH_RESULT_IS_NOT_AUTOMATIC_WORK_IDENTITY',
        'status': 'QUEUED',
    })

rank = {'P0_MULTIPLICITY': 0, 'P1_LOW_COST': 1, 'P2_MEDIUM_COST': 2, 'P3_HIGH_COST': 3}
queue.sort(key=lambda r: (rank[r['priority']], int(r['total_bytes_to_hash']), r['candidate_family_id']))

fields = list(queue[0].keys())
with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(queue)

assert len(queue) == 126
assert sum(int(r['object_count']) for r in queue) == 258
assert len({r['candidate_family_id'] for r in queue}) == 126
print(f'wrote {OUT}')
print('families=126 objects=258')
for p in rank:
    subset = [r for r in queue if r['priority'] == p]
    print(f'{p}: families={len(subset)} objects={sum(int(r["object_count"]) for r in subset)} bytes={sum(int(r["total_bytes_to_hash"]) for r in subset)}')
