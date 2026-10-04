#!/usr/bin/env python3
"""Validate PRISM schema, connection references and candidate event gates.

This does not conduct privacy or cultural review, nor grant rights or publication
approval. Locators are checked locally; no source is fetched or deemed read.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / 'schemas/akashic-prism-v0.1.schema.json').read_text())
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA)


def doi_identity(value):
    """Resolve syntactic DOI aliases locally; never infer real independence."""
    if not isinstance(value, str):
        return None
    value = value.strip()
    if value.casefold().startswith('doi:'):
        value = value[4:].strip()
    try:
        parsed = urlsplit(value)
    except ValueError:
        return None
    if parsed.scheme.casefold() in ('http', 'https') and parsed.hostname in (
            'doi.org', 'dx.doi.org'):
        value = unquote(parsed.path.lstrip('/'))
    return value.casefold() if re.fullmatch(r'10\.[0-9]{4,9}/\S+', value) else None


def validate(record):
    errors = [f'{list(error.absolute_path)}: {error.message}'
              for error in VALIDATOR.iter_errors(record)]
    if errors:
        return errors
    nodes = defaultdict(list)
    for node in record['source_network']['nodes']:
        nodes[node['source_id']].append(node)
    for section in ('connections', 'perspectives', 'practice_outcomes',
                    'state_observations', 'comparative_correspondences',
                    'assessment_history'):
        for index, item in enumerate(record.get(section, [])):
            for source_id in item.get('source_ids', []):
                matches = nodes.get(source_id, [])
                if len(matches) != 1:
                    errors.append(f'{section}[{index}]: {source_id} must resolve '
                                  'to exactly one source_network node')
                elif not matches[0]['locator'].strip():
                    errors.append(f'{section}[{index}]: {source_id} requires '
                                  'a nonblank locator')
    # Count only explicitly independent, verified work identities. Equivalence
    # and derivation links (plus repeated identity fields) collapse aliases.
    parent = {source_id: source_id for source_id in nodes}

    def find(source_id):
        while parent[source_id] != source_id:
            source_id = parent[source_id]
        return source_id

    def union(left, right):
        parent[find(left)] = find(right)

    identities = {}
    for source_id, matches in nodes.items():
        if len(matches) != 1:
            errors.append(f'source_network: ambiguous source identity {source_id}')
        for node in matches:
            for field in ('doi', 'locator'):
                doi = doi_identity(node.get(field))
                if doi:
                    key = ('canonical_doi', doi)
                    if key in identities:
                        union(source_id, identities[key])
                    identities[key] = source_id
            for field in ('work_id', 'doi', 'post_id', 'locator'):
                value = node.get(field)
                if isinstance(value, str) and value.strip():
                    key = (field, value.strip().casefold())
                    if key in identities:
                        union(source_id, identities[key])
                    identities[key] = source_id
    edges = record['source_network']['edges']
    resolved_edges = []
    for edge in edges:
        left, right = edge['from_source_id'], edge['to_source_id']
        if left not in nodes or right not in nodes:
            errors.append('source_network: edge has unresolved source identity')
            continue
        resolved_edges.append(edge)
        if edge['relation'] in ('same_work_as', 'derived_from'):
            union(left, right)
    independent = set()
    for edge in resolved_edges:
        if edge['independent_evidence'] is not True:
            continue
        source_ids = (edge['from_source_id'], edge['to_source_id'])
        if (edge['relation'] not in ('supports', 'contradicts')
                or find(source_ids[0]) == find(source_ids[1])):
            errors.append('source_network: independence conflicts with relationship or work identity')
            continue
        eligible = all(len(nodes[sid]) == 1 and
                       nodes[sid][0]['provenance_state'] == 'verified' and
                       nodes[sid][0]['locator'].strip() and
                       isinstance(nodes[sid][0].get('work_id'), str) and
                       nodes[sid][0]['work_id'].strip() for sid in source_ids)
        if not eligible:
            errors.append('source_network: independent evidence requires verified, located work identities')
            continue
        independent.update(find(sid) for sid in source_ids)
    expected = len(independent)
    actual = record['source_network']['counting_boundary']['independent_evidence_sources']
    if type(actual) is not int or actual != expected:
        errors.append(f'counting_boundary.independent_evidence_sources: expected {expected}')
    if record['governance']['publication_status'] == 'review_candidate':
        history = record.get('assessment_history', [])
        successors = {event['supersedes_event_id']: event for event in history
                      if event.get('supersedes_event_id')}
        seen = set()
        valid_chain = len(successors) == sum(
            bool(event.get('supersedes_event_id')) for event in history)
        for event in history:
            event_id = event['assessment_event_id']
            predecessor = event.get('supersedes_event_id')
            if event_id in seen or (predecessor and predecessor not in seen):
                valid_chain = False
            seen.add(event_id)
        if not valid_chain:
            errors.append('assessment_history: ambiguous event supersession')
        else:
            for event in history:
                pending = set(event.get('gates_pending', [])) & {
                    'privacy', 'cultural_authority'}
                successor = successors.get(event['assessment_event_id'])
                # A clearance only resolves gates for the same affected reference.
                if successor and successor['affected_ref'] == event['affected_ref']:
                    pending -= set(successor.get('gates_passed', []))
                if pending:
                    errors.append('assessment_history: event '
                                  f"{event['assessment_event_id']} has unresolved "
                                  f"{', '.join(sorted(pending))} gate")
    return errors


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f'invalid JSON constant: {value}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path)
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text(), object_pairs_hook=unique_object,
                            parse_constant=reject_constant)
        errors = validate(record)
    except (OSError, ValueError) as error:
        errors = [str(error)]
    for error in errors:
        print(f'ERROR: {error}')
    if not errors:
        print('PASS: schema, connection traceability and candidate event gates; no gate approval')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
