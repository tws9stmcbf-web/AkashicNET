#!/usr/bin/env python3
"""Validate PRISM schema and connection source references, without promotion.

This is not an evidence-independence, privacy, rights or publication approval
validator. Locators are checked locally; no source is fetched or deemed read.
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
        print('PASS: schema and connection source traceability only; no gate approval')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
