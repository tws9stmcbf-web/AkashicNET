#!/usr/bin/env python3
"""Validate PRISM schema, connection references and candidate event gates.

This does not conduct privacy or cultural review, nor grant rights or publication
approval. Locators are checked locally; no source is fetched or deemed read.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / 'schemas/akashic-prism-v0.1.schema.json').read_text())
Draft202012Validator.check_schema(SCHEMA)
VALIDATOR = Draft202012Validator(SCHEMA)


def validate(record):
    errors = [f'{list(error.absolute_path)}: {error.message}'
              for error in VALIDATOR.iter_errors(record)]
    if errors:
        return errors
    nodes = defaultdict(list)
    for node in record['source_network']['nodes']:
        nodes[node['source_id']].append(node)
    for index, connection in enumerate(record.get('connections', [])):
        for source_id in connection.get('source_ids', []):
            matches = nodes[source_id]
            if len(matches) != 1:
                errors.append(f'connections[{index}]: {source_id} must resolve '
                              'to exactly one source_network node')
            elif not matches[0]['locator'].strip():
                errors.append(f'connections[{index}]: {source_id} requires '
                              'a nonblank locator')
    if record['governance']['publication_status'] == 'review_candidate':
        history = record.get('assessment_history', [])
        superseded = [event.get('supersedes_event_id') for event in history
                      if event.get('supersedes_event_id')]
        seen = set()
        valid_chain = True
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
                if event['assessment_event_id'] not in superseded:
                    pending = set(event.get('gates_pending', [])) & {
                        'privacy', 'cultural_authority'}
                    if pending:
                        errors.append('assessment_history: current event '
                                      f"{event['assessment_event_id']} has pending "
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
