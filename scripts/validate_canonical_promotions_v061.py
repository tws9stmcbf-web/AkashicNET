#!/usr/bin/env python3
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / 'references' / 'community'


def rows(name):
    with (REF / name).open(newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))

hashes = rows('hash-verification-results-v0.16.csv')
manifests = rows('drive-manifestation-provenance-v0.14.csv')
decisions = rows('canonical-promotion-decisions-v0.6.1.csv')
works = rows('canonical-work-registry-v0.6.1.csv')
edges = rows('canonical-graph-promotions-v0.6.1.csv')

hash_by_id = {r['hash_record_id']: r for r in hashes}
manifest_ids = {'manifestation:' + r['manifestation_id'] for r in manifests}
decision_by_id = {r['decision_id']: r for r in decisions}
work_ids = {r['work_id'] for r in works}

assert len(decisions) == 15, f'expected 15 decisions, got {len(decisions)}'
accepted = [r for r in decisions if r['decision'] == 'ACCEPT']
holds = [r for r in decisions if r['decision'] == 'HOLD']
assert len(accepted) == 3, f'expected 3 accepts, got {len(accepted)}'
assert len(holds) == 12, f'expected 12 holds, got {len(holds)}'
assert len(works) == 3, f'expected 3 promoted works, got {len(works)}'
assert len(edges) == 9, f'expected 9 accepted edges, got {len(edges)}'
assert len({r['edge_id'] for r in edges}) == 9, 'duplicate edge IDs'
assert len({r['work_id'] for r in works}) == 3, 'duplicate work IDs'
assert not any(r['edition_id'] for r in accepted), 'no edition ID is supported in v0.6.1'

for decision in accepted:
    evidence = decision['evidence_ids']
    assert evidence in hash_by_id, f"missing hash evidence {evidence}"
    h = hash_by_id[evidence]
    assert h['comparison_result'] == 'MATCH', f'{evidence} is not MATCH'
    assert h['byte_identity_status'] == 'BYTE_IDENTICAL_VERIFIED', f'{evidence} lacks verified byte identity'
    assert h['sha256_a'] == h['sha256_b'], f'{evidence} hash mismatch'
    assert decision['work_id'] in work_ids, f"missing work {decision['work_id']}"

for edge in edges:
    assert edge['status'] == 'ACCEPT', f"non-accepted edge {edge['edge_id']}"
    assert edge['promotion_decision_id'] in decision_by_id, f"unknown decision {edge['promotion_decision_id']}"
    decision = decision_by_id[edge['promotion_decision_id']]
    assert decision['decision'] == 'ACCEPT', f"edge from HOLD {edge['edge_id']}"
    assert edge['evidence_id'] in hash_by_id, f"unknown evidence {edge['evidence_id']}"
    assert edge['source_id'] in manifest_ids, f"unknown source manifestation {edge['source_id']}"
    if edge['relation'] == 'REPRESENTS':
        assert edge['target_id'] in work_ids, f"unknown target work {edge['target_id']}"
    elif edge['relation'] == 'DUPLICATE_OF':
        assert edge['target_id'] in manifest_ids, f"unknown target manifestation {edge['target_id']}"
    else:
        raise AssertionError(f"unsupported relation {edge['relation']}")

for work in works:
    assert work['rights_state'] == 'UNKNOWN_UNVERIFIED', 'canonical promotion must not promote rights state'
    assert work['scientific_evidence_state'] == 'NOT_EVALUATED', 'canonical promotion must not promote scientific evidence state'
    assert work['edition_status'] == 'NOT_ASSIGNED', 'edition IDs are intentionally not promoted in v0.6.1'

print('canonical promotion v0.6.1 validation PASS')
print(f'decisions={len(decisions)} accepts={len(accepted)} holds={len(holds)} works={len(works)} edges={len(edges)}')
