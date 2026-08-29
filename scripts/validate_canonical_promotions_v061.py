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
manifest_by_id = {'manifestation:' + r['manifestation_id']: r for r in manifests}
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
    assert len(bytes.fromhex(h['sha256_a'])) == 32, f'{evidence} is not a valid SHA-256 digest'
    assert decision['work_id'] in work_ids, f"missing work {decision['work_id']}"
    for suffix in ('a', 'b'):
        manifest_id = h[f'manifestation_{suffix}']
        assert manifest_id in manifest_by_id, f'{evidence} references unknown manifestation {manifest_id}'
        manifest = manifest_by_id[manifest_id]
        assert h[f'drive_id_{suffix}'] == manifest['drive_object_id'], f'{evidence} Drive ID does not match {manifest_id}'
        assert h[f'size_{suffix}'] == manifest['size_bytes'], f'{evidence} size does not match {manifest_id}'
        assert manifest['family_id'] == decision['family_id'], f'{evidence} family does not match {manifest_id}'

for edge in edges:
    assert edge['status'] == 'ACCEPT', f"non-accepted edge {edge['edge_id']}"
    assert edge['promotion_decision_id'] in decision_by_id, f"unknown decision {edge['promotion_decision_id']}"
    decision = decision_by_id[edge['promotion_decision_id']]
    assert decision['decision'] == 'ACCEPT', f"edge from HOLD {edge['edge_id']}"
    assert edge['evidence_id'] == decision['evidence_ids'], f"edge evidence does not match decision {edge['edge_id']}"
    assert edge['evidence_id'] in hash_by_id, f"unknown evidence {edge['evidence_id']}"
    hash_record = hash_by_id[edge['evidence_id']]
    expected_manifests = {hash_record['manifestation_a'], hash_record['manifestation_b']}
    assert edge['source_id'] in manifest_ids, f"unknown source manifestation {edge['source_id']}"
    if edge['relation'] == 'REPRESENTS':
        assert edge['source_id'] in expected_manifests, f"source not covered by hash evidence {edge['edge_id']}"
        assert edge['target_id'] == decision['work_id'], f"target does not match decision work {edge['edge_id']}"
    elif edge['relation'] == 'DUPLICATE_OF':
        assert {edge['source_id'], edge['target_id']} == expected_manifests, f"duplicate pair not covered by hash evidence {edge['edge_id']}"
    else:
        raise AssertionError(f"unsupported relation {edge['relation']}")

for decision in accepted:
    decision_edges = [edge for edge in edges if edge['promotion_decision_id'] == decision['decision_id']]
    assert sum(edge['relation'] == 'REPRESENTS' for edge in decision_edges) == 2, f"expected two REPRESENTS edges for {decision['decision_id']}"
    assert sum(edge['relation'] == 'DUPLICATE_OF' for edge in decision_edges) == 1, f"expected one DUPLICATE_OF edge for {decision['decision_id']}"

for work in works:
    assert work['rights_state'] == 'UNKNOWN_UNVERIFIED', 'canonical promotion must not promote rights state'
    assert work['scientific_evidence_state'] == 'NOT_EVALUATED', 'canonical promotion must not promote scientific evidence state'
    assert work['edition_status'] == 'NOT_ASSIGNED', 'edition IDs are intentionally not promoted in v0.6.1'

print('canonical promotion v0.6.1 validation PASS')
print(f'decisions={len(decisions)} accepts={len(accepted)} holds={len(holds)} works={len(works)} edges={len(edges)}')
