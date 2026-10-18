#!/usr/bin/env python3
"""Read-only structural checks for a separate OMNI coverage record, never acceptance."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'schemas/akashicomni-perspective-coverage-v0.1.schema.json'
spec = importlib.util.spec_from_file_location(
    'omni_claim_review', ROOT / 'scripts/validate_akashicomni_claim_review_v050.py')
claim_review = importlib.util.module_from_spec(spec)
spec.loader.exec_module(claim_review)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def _invalid_constant(value):
    raise ValueError(f'non-finite JSON value: {value}')


def read_json(raw):
    """Reject ambiguous JSON; packet hashing always uses the unmodified bytes."""
    return json.loads(raw.decode('utf-8'), object_pairs_hook=_unique_object,
                      parse_constant=_invalid_constant)


def validate(record, packet_bytes):
    """Return structural errors. Never fetch sources, mutate records or grant gates."""
    try:
        schema = read_json(SCHEMA.read_bytes())
        Draft202012Validator.check_schema(schema)
        errors = [f"{'/'.join(map(str, e.absolute_path))}: {e.message}"
                  for e in Draft202012Validator(
                      schema, format_checker=FormatChecker()).iter_errors(record)]
        if errors:
            return errors
        packet = read_json(packet_bytes)
        packet_errors = claim_review.validate(packet)
    except (OSError, ValueError) as exc:
        return [f'input or policy: {exc}']
    if packet_errors:
        return [f'claim packet: {e}' for e in packet_errors]

    binding = record['packet_binding']
    if binding['sha256'] != hashlib.sha256(packet_bytes).hexdigest():
        errors.append('packet binding: SHA-256 mismatch (exact file bytes required)')
    if binding['packet_id'] != packet['packet_id']:
        errors.append('packet binding: packet ID mismatch')
    claims = {c['claim_id']: c for c in packet['claims']}
    selected = set(record['scope']['claim_ids'])
    if not selected <= claims.keys():
        return errors + ['scope: unknown claim reference']
    source_ids = {sid for cid in selected for sid in claims[cid]['source_ids']}
    contexts = record['source_context']
    context_ids = [s['source_id'] for s in contexts]
    if len(context_ids) != len(set(context_ids)):
        errors.append('source context: duplicate source IDs')
    if set(context_ids) != source_ids:
        errors.append('source context: must cover exactly the selected claims\' sources')
    sources = {s['source_id']: s for s in packet['sources']}
    for context in contexts:
        sid = context['source_id']
        if sid not in source_ids:
            continue
        if context['access_status'] != sources[sid]['access_status']:
            errors.append(f'{sid}: access status must match the bound packet')

    # Identifier spellings match the pinned PRISM compatibility vocabulary;
    # their use here is coverage metadata, not PRISM interchange or execution.
    expected = set(schema['properties']['coverage']['items']['properties'][
        'perspective_id']['enum'])
    entries = record['coverage']
    included = [e['perspective_id'] for e in entries]
    excluded = [e['perspective_id'] for e in record['scope']['excluded_perspectives']]
    if len(included) != len(set(included)) or len(excluded) != len(set(excluded)):
        errors.append('coverage: duplicate included or excluded perspective')
    if set(included) & set(excluded):
        errors.append('coverage: included and excluded perspectives overlap')
    if set(included) | set(excluded) != expected:
        errors.append('coverage: baseline perspectives must all be accounted for')
    if record['scope']['mode'] == 'FULL' and excluded:
        errors.append('coverage: FULL scope cannot exclude a perspective')
    if record['scope']['mode'] == 'NARROW' and not excluded:
        errors.append('coverage: NARROW scope must disclose excluded perspectives')
    for entry in entries:
        refs = set(entry['source_ids'])
        if not refs <= source_ids:
            errors.append(f"{entry['perspective_id']}: unknown or out-of-scope source")
            continue
        if entry['state'] == 'APPLIED' and not any(
                sources[sid]['access_status'] != 'NOT_REINSPECTED' for sid in refs):
            errors.append(f"{entry['perspective_id']}: APPLIED requires an inspected source")
        if entry['state'] == 'NOT_RELEVANT' and any(
                sources[sid]['access_status'] == 'NOT_REINSPECTED' for sid in refs):
            errors.append(f"{entry['perspective_id']}: unavailable material is not irrelevance")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('record', type=Path, help='Separate coverage JSON file')
    parser.add_argument('packet', type=Path, help='Explicit local claim packet, never a record-selected path')
    args = parser.parse_args(argv)
    try:
        record = read_json(args.record.read_bytes())
        errors = validate(record, args.packet.read_bytes())
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    if errors:
        print('OMNI coverage structure: FAIL\n' + '\n'.join(errors))
        return 1
    print(f"OMNI coverage structure: PASS; {record['record_provenance']}; UNRELEASED; REVIEW_REQUIRED")
    print('Manual checks remain PENDING: source-access accuracy, relevance/reasons, '
          'synthesis adequacy, human verification and M01–M12 acceptance.')
    print('No independent review, evidence promotion, publication or release is established.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
