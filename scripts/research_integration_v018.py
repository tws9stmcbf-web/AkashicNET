"""Bounded offline PRISM -> manual OMNI queue -> metadata projection. No network."""
import argparse
import copy
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'schemas/research-integration-v0.18.schema.json'
LOCK = ROOT / 'references/integration/v018/input-lock.json'
PERSPECTIVES = ['AWAKEN', 'HIERATIC', 'HOMESENSE', 'ADAPT', 'REGENERATE',
                'TRANSCEND', '#METAD', 'ACTC', 'CUT Past', 'CUT Present', 'CUT Future', 'UMASC']
CATEGORIES = {'access', 'cultural_authority', 'privacy', 'provenance', 'rights'}
GUARDS = dict.fromkeys(['truth', 'evidence', 'rights', 'identity', 'edge_acceptance'], False)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(rows, keys):
    seen = set()
    for row in rows:
        key = tuple(row[k] for k in keys)
        require(None not in key and key not in seen, 'duplicate or null primary key')
        seen.add(key)


def validate_packet(packet, contracts):
    """Validate all exported tables, including compound SQLite foreign keys."""
    require(packet['schema'] == 'akashicprism.framework-input.v1', 'packet schema')
    require(packet['table_contracts'] == contracts, 'table contracts differ from lock')
    tables = packet['collections']
    require(set(tables) == set(contracts), 'missing or extra tables')
    for name, c in contracts.items():
        rows = tables[name]
        require(len(rows) == c['row_count'] and digest(rows) == c['sha256'], 'table digest/count')
        if c['primary_key']:
            unique(rows, c['primary_key'])
        groups = {}
        for fk in c['foreign_keys']:
            groups.setdefault(fk['id'], []).append(fk)
        for group in groups.values():
            group.sort(key=lambda f: f['seq'])
            target = {tuple(r[f['to']] for f in group) for r in tables[group[0]['table']]}
            for row in rows:
                key = tuple(row[f['from']] for f in group)
                require(None in key or key in target, 'foreign key violation')
    assessments = tables['assessments']
    by_id = {a['assessment_id']: a for a in assessments}
    children = set()
    for a in assessments:
        prev = a['supersedes']
        if prev is not None:
            require(prev not in children, 'forked assessment history')
            children.add(prev)
        visited = set()
        node = a
        while node['supersedes'] is not None:
            require(node['assessment_id'] not in visited, 'cyclic assessment history')
            visited.add(node['assessment_id'])
            node = by_id[node['supersedes']]
            require(node['record_id'] == a['record_id'], 'cross-record correction')
    expected_current = {a['assessment_id'] for a in assessments} - children
    current = tables['current_assessments']
    require({a['assessment_id'] for a in current} == expected_current, 'current assessment mismatch')
    require(all(a == by_id[a['assessment_id']] for a in current), 'current assessment changed')


def observation(source_id, row, restrictions, packet_hash, path, depth):
    return {
        'observation_id': 'obs-' + digest([source_id, row, restrictions])[:24],
        'supersedes': None, 'observed_at': row.get('observed_at', row.get('assessment_date')),
        'retrieved_at': None,  # observation and retrieval dates are not interchangeable
        'url': row.get('source_url', row.get('canonical_url')),
        'reading_depth': depth, 'evidence_status': row.get('evidence_status', 'unassessed'),
        'access_scope': row.get('access_scope', row.get('scope', 'metadata only')),
        'provenance': row.get('provenance', 'PRISM record metadata'),
        'input_sha256': packet_hash, 'input_path': path,
        'upstream_assessment_id': row.get('assessment_id'),
        'rationale': row.get('rationale'), 'uncertainty': row.get('uncertainty'),
        'upstream_integration_status': row.get('integration_status'),
        'restrictions': restrictions, 'correction_reason': None,
    }


def verify_foundations(lock):
    for path, pin in lock.get('foundation_pins', {}).items():
        data = (ROOT / path).read_bytes()
        require(hashlib.sha256(data).hexdigest() == pin['sha256'], 'foundation changed: ' + path)
        require(hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                == pin['git_blob_sha'], 'foundation blob mismatch')


def adapt(packet_bytes, lock):
    """Use native source_url/record_id, retaining full selected assessment history."""
    verify_foundations(lock)
    packet_hash = hashlib.sha256(packet_bytes).hexdigest()
    require(packet_hash == lock['packet_sha256'], 'packet checksum mismatch')
    packet = json.loads(packet_bytes)
    require(packet['dataset_revision'] == lock['dataset_revision'], 'dataset revision mismatch')
    validate_packet(packet, lock['table_contracts'])
    if lock.get('foundation_pins'):
        import sys
        sys.path.insert(0, str(ROOT))
        from tools.search_reddit import load_records
        archive_id = lock['selection']['community_id'].removeprefix('PRISM-REDDIT-')
        require(any(r['post_id'] == archive_id for r in load_records()), 'community absent from pinned N2N archive')
    tables = packet['collections']
    selection = lock['selection']
    primary = next((r for r in tables['source_metadata'] if r['source_url'] == selection['primary_id']), None)
    community = next((r for r in tables['records'] if r['record_id'] == selection['community_id']), None)
    require(primary is not None and community is not None, 'selected source missing')
    require(any(r['source_url'] == selection['primary_id'] and r['question_id'] == 'BQ001'
                for r in tables['bq_discovery_links']), 'missing BQ001 discovery link')
    context = [r for r in tables['record_context'] if r['record_id'] == selection['community_id']]
    require(len(context) == 1, 'missing/duplicate record context')
    assessments = [a for a in tables['assessments'] if a['record_id'] == selection['community_id']]
    require(assessments, 'missing assessments')
    primary_restrictions = [dict(category=k, status='unknown', scope='No scope-specific clearance recorded')
                            for k in sorted(CATEGORIES)]
    primary_restrictions = copy.deepcopy(primary_restrictions)
    next(r for r in primary_restrictions if r['category'] == 'rights')['status'] = primary['rights_status']
    sources = [dict(source_id=primary['source_url'], kind='primary_research', visibility='unknown',
                    work_family=None, relationships=[], observations=[observation(
                        primary['source_url'], primary, primary_restrictions, packet_hash,
                        'collections.source_metadata', 'metadata_only')])]
    observations = []
    # Topological order, not assessment number or array order.
    previous = None
    while len(observations) < len(assessments):
        candidates = [a for a in assessments if a['supersedes'] == previous]
        require(len(candidates) == 1, 'ambiguous assessment history')
        a = candidates[0]
        restrictions = [r for r in tables['restrictions'] if r['assessment_id'] == a['assessment_id']]
        require({r['category'] for r in restrictions} == CATEGORIES, 'incomplete restrictions')
        safe_restrictions = [{k: r[k] for k in ['category', 'status', 'scope']} for r in restrictions]
        row = dict(a, canonical_url=community['canonical_url'])
        o = observation(community['record_id'], row, safe_restrictions, packet_hash,
                        'collections.assessments', a['review_depth'])
        o['supersedes'] = observations[-1]['observation_id'] if observations else None
        o['correction_reason'] = 'Upstream superseding assessment' if observations else None
        observations.append(o)
        previous = a['assessment_id']
    sources.append(dict(source_id=community['record_id'], kind='community_citation',
                        visibility=context[0]['visibility'], work_family=None,
                        relationships=[], observations=observations))
    document = dict(contract_version='0.18.0-pilot.1', fixture_kind='REAL_PRIVATE_INPUT',
                    dataset_revision=packet['dataset_revision'], input_sha256=packet_hash,
                    collection_release_policy='DEPRECATED_AMBIGUOUS_NOT_A_RELEASE',
                    question_id='BQ001', question_status='UNRESOLVED', promotion_guards=dict(GUARDS),
                    sources=sources, reviews=[])
    document['reviews'] = [pending_review(document)]
    validate(document)
    return document


def bindings(document):
    return {s['source_id']: digest(s) for s in document['sources']}


def pending_review(document, review_id='OMNI-BQ001-PILOT-1'):
    return dict(review_id=review_id, supersedes=None, recorded_at='2026-10-22',
                method='OMNI-0.5.0-manual-reference', state='PENDING_HUMAN_REVIEW',
                reviewer=None, source_bindings=bindings(document),
                perspectives={p: 'INSUFFICIENT_INFORMATION' for p in PERSPECTIVES},
                direct_evidence=[], interpretation=[], synthesis=[], hypothesis=[],
                counter_evidence=[], missing_information=['Original source appraisal, contrary evidence, rights and human review pending'],
                uncertainty=['No BQ001 inference is justified by metadata integration'],
                disclosures=[])


def validate(document):
    schema = json.loads(SCHEMA.read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(document)
    sources = document['sources']
    unique(sources, ['source_id'])
    require(len(sources) == 2 and {s['kind'] for s in sources} == {'primary_research', 'community_citation'}, 'bounded source pair')
    ids = {s['source_id'] for s in sources}
    for source in sources:
        observations = source['observations']
        unique(observations, ['observation_id'])
        previous = None
        previous_date = ''
        for o in observations:
            require(o['supersedes'] == previous, 'broken correction chain')
            require(o['observed_at'] >= previous_date, 'correction chronology')
            require(previous is None or bool(o['correction_reason']), 'correction reason required')
            unique(o['restrictions'], ['category'])
            require({r['category'] for r in o['restrictions']} == CATEGORIES, 'missing restriction category')
            previous, previous_date = o['observation_id'], o['observed_at']
        for rel in source['relationships']:
            require(rel['target_id'] in ids, 'dangling source relationship')
        # A locator match flags a candidate; it never merges source/study identity.
        for o in observations:
            url = urlsplit(o['url'])
            require(url.scheme == 'https' and bool(url.hostname) and not url.username and not url.password
                    and not url.query and not url.fragment, 'unsafe source URL')
    reviews = document['reviews']
    unique(reviews, ['review_id'])
    previous = None
    date = ''
    for review in reviews:
        require(review['supersedes'] == previous and review['recorded_at'] >= date, 'broken review correction chain')
        require(set(review['source_bindings']) == ids, 'review source referential integrity')
        require(set(review['perspectives']) == set(PERSPECTIVES), 'twelve perspective dispositions required')
        if review['state'] == 'HUMAN_REVIEWED':
            require(review['reviewer'] and document['fixture_kind'] == 'REAL_PRIVATE_INPUT', 'human identity required')
        if review['state'] == 'SIMULATED_REVIEW':
            require(document['fixture_kind'] == 'SYNTHETIC', 'simulated review is fixture-only')
        unique(review['disclosures'], ['source_id'])
        for disclosure in review['disclosures']:
            require(disclosure['source_id'] in ids, 'dangling disclosure')
        previous, date = review['review_id'], review['recorded_at']
    return document


def project(document):
    """Fresh allowlist only. HOLD reveals no source IDs, counts, text or failure reasons."""
    validate(document)
    review = document['reviews'][-1]
    approved_state = ('SIMULATED_REVIEW' if document['fixture_kind'] == 'SYNTHETIC' else 'HUMAN_REVIEWED')
    permitted = review['state'] == approved_state and review['source_bindings'] == bindings(document)
    for source in document['sources']:
        o = source['observations'][-1]
        permission = next((d for d in review['disclosures'] if d['source_id'] == source['source_id']), None)
        permitted = permitted and source['visibility'] == 'public' and permission is not None
        permitted = permitted and all(r['status'] == 'cleared_for_scope' for r in o['restrictions'])
        if permission is not None:
            permitted = permitted and permission['observation_sha256'] == digest(o)
    result = dict(contract_version=document['contract_version'], question_id='BQ001', question_status='UNRESOLVED',
                  status='HOLD', promotion_guards=dict(GUARDS), sources=[], review=None,
                  limitations=['Metadata integration is not scientific validation; release approval is separate'])
    if not permitted:
        return validate_projection(result)
    result.update(status=('SYNTHETIC_NOT_FOR_PUBLICATION' if document['fixture_kind'] == 'SYNTHETIC'
                          else 'HUMAN_CLEARED_METADATA_PREVIEW_NOT_PUBLISHED'),
                  input_revision=document['dataset_revision'], input_sha256=document['input_sha256'],
                  review=dict(review_id=review['review_id'], state=review['state'], recorded_at=review['recorded_at'],
                              review_sha256=digest(review)))
    for source in sorted(document['sources'], key=lambda s: s['source_id']):
        o = source['observations'][-1]
        result['sources'].append(dict(source_id=source['source_id'], original_url=source['observations'][0]['url'],
            current_url=o['url'], kind=source['kind'], reading_depth=o['reading_depth'],
            evidence_status=o['evidence_status'], observation_sha256=digest(o),
            corrections=[dict(observation_id=p['observation_id'], supersedes=p['supersedes'],
                              observed_at=p['observed_at'], observation_sha256=digest(p))
                         for p in source['observations']]))
    return validate_projection(result)


def validate_projection(result):
    schema = json.loads((ROOT / 'schemas/research-integration-public-v0.18.schema.json').read_text())
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--packet', type=Path)
    group.add_argument('--contract', type=Path)
    parser.add_argument('--private-out', type=Path)
    parser.add_argument('--public-out', type=Path, required=True)
    args = parser.parse_args()
    # Remove stale approved projection before a failing validation can leave it available.
    paths = [p.resolve() for p in [args.packet, args.contract, args.private_out, args.public_out] if p]
    require(len(paths) == len(set(paths)), 'input/private/public paths must differ')
    require(not any(p.is_relative_to(ROOT) for p in paths[-(2 if args.private_out else 1):]),
            'runtime outputs must stay outside the repository')
    args.public_out.unlink(missing_ok=True)
    document = (adapt(args.packet.read_bytes(), json.loads(LOCK.read_text())) if args.packet
                else validate(json.loads(args.contract.read_text())))
    result = project(document)
    if args.private_out:
        import os
        fd = os.open(args.private_out, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, 'w') as handle:
            handle.write(json.dumps(document, indent=2, ensure_ascii=False) + '\n')
    args.public_out.write_bytes(canonical(result) + b'\n')
    print(result['status'])


if __name__ == '__main__':
    import sys
    from jsonschema import ValidationError
    try:
        main()
    except (ValueError, ValidationError, KeyError, OSError, TypeError):
        print('HOLD: validation failed; no public source output. Inspect inputs privately.', file=sys.stderr)
        sys.exit(2)
