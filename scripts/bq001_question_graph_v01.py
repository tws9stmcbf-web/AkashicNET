#!/usr/bin/env python3
"""Deterministic, review-only retrieval over the governed BQ001 graph.

Generation is separate from readiness. A safe changed upstream fixture can be
projected for review, but validation/retrieval require the audited input pin.
"""
import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validate_knowledge_graph_beta_v016 import validate as validate_upstream
from scripts.build_knowledge_graph_beta_fixture_v016 import SOURCE_SPECS

INPUT = ROOT / 'references/big-questions/BQ001/knowledge-graph-beta-fixture-v0.16.json'
OUTPUT = ROOT / 'references/big-questions/BQ001/question-graph-v0.1.json'
SCHEMA = ROOT / 'schemas/bq001-question-graph-v0.1.schema.json'
INPUT_SHA256 = 'bb501c962b54c88b581ca6911e6377cdd0e18e12c34d0bd04ffcaa0dcae5cca3'
GUARDS = {
    key: False for key in (
        'truth_inference', 'scientific_evidence_promotion', 'rights_inference',
        'public_status_inference', 'identity_promotion', 'safety_efficacy_promotion',
        'edge_acceptance', 'ranking_promotion', 'private_drive_data',
    )
}
FORBIDDEN_KEYS = {
    'driveid', 'drivefileid', 'driveobjectid', 'fileid', 'objectid',
    'filename', 'filepath', 'privatepath', 'parentid', 'objecthash',
    'objectsha256', 'md5checksum', 'sha256checksum', 'privatedriveid',
}


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, indent=2, allow_nan=False) + '\n'


def load_json(raw):
    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate JSON key')
            result[key] = value
        return result
    def reject_constant(_):
        raise ValueError('non-finite JSON number')
    return json.loads(raw, object_pairs_hook=unique_pairs, parse_constant=reject_constant)


def privacy_check(value):
    """Check keys and values; diagnostics never echo rejected private content."""
    def check_string(text, is_key=False):
        decoded = text
        for _ in range(32):
            new = unquote(decoded)
            if new == decoded:
                break
            decoded = new
        else:
            raise ValueError('encoding did not stabilize')
        unescaped = decoded
        decoded = decoded.casefold().replace('\\', '/')
        if any(marker in decoded for marker in (
            'drive.google.com', 'docs.google.com', '/my drive/', 'akm-',
            'file://', 'gdrive://',
        )):
            raise ValueError('private metadata rejected')
        # Digests are allowed only in typed artifact/baseline slots below.
        if not is_key and re.search(r'(?<![a-f0-9])[a-f0-9]{32,64}(?![a-f0-9])', decoded):
            raise ValueError('unscoped digest rejected')
        if not is_key:
            for token in re.findall(r'(?<![A-Za-z0-9_-])[A-Za-z0-9_-]{25,}(?![A-Za-z0-9_-])', unescaped):
                if re.search(r'[a-z]', token) and re.search(r'[A-Z]', token) and re.search(r'[0-9]', token):
                    raise ValueError('opaque identifier rejected')
    if isinstance(value, dict):
        for key, child in value.items():
            check_string(key, is_key=True)
            if re.sub(r'[^a-z0-9]', '', key.casefold()) in FORBIDDEN_KEYS:
                raise ValueError('private metadata rejected')
            if key == 'sha256' and value.get('repository_path') in {
                str(INPUT.relative_to(ROOT)),
                *(s['repository_path'] for s in SOURCE_SPECS.values()),
            } and isinstance(child, str) and re.fullmatch(r'[a-f0-9]{64}', child):
                continue  # Repository artifact digest; never a Drive object slot.
            if key in {'v0.14', 'v0.15_release', 'v0.15_seal'} and isinstance(child, str) and re.fullmatch(r'[a-f0-9]{40}', child):
                continue  # Exact lock values are checked by schema and projection.
            privacy_check(child)
    elif isinstance(value, list):
        for child in value:
            privacy_check(child)
    elif isinstance(value, str):
        check_string(value)


def project(upstream, digest):
    privacy_check(upstream)
    # A changed fixture can be reviewed, but its structure, transitive source
    # pins and record identities must remain governed. Only byte reproduction
    # against the existing fixture is deliberately non-blocking here.
    errors = validate_upstream(upstream)
    if any(error != 'deterministic artifact' for error in errors):
        raise ValueError('upstream graph governance violation')
    # Runtime schema and deterministic validation reject unknown metadata.
    nodes = sorted(copy.deepcopy(upstream['nodes']), key=lambda n: n['node_id'])
    edges = sorted(copy.deepcopy(upstream['edges']), key=lambda e: e['edge_id'])
    result = {
        'schema_version': 'akashicnet.bq001.question-graph.v0.1',
        'mode': 'REVIEW_ONLY',
        'question_id': 'BQ001',
        'question_status': 'UNRESOLVED',
        'finality': 'NEVER_FINAL',
        'baseline_locks': copy.deepcopy(upstream['baseline_locks']),
        'guards': dict(GUARDS),
        'input': {'repository_path': str(INPUT.relative_to(ROOT)), 'sha256': digest},
        'source_artifacts': sorted(copy.deepcopy(upstream['source_artifacts']), key=lambda a: a['artifact_id']),
        'nodes': nodes,
        'edges': edges,
        'curated_edge_ids': [e['edge_id'] for e in edges if e['assertion_class'] == 'DIRECT_SOURCE_METADATA'],
        'inferred_edge_ids': [e['edge_id'] for e in edges if e['assertion_class'] == 'INFERRED_CANDIDATE'],
        'coverage': {
            'scope': 'EXISTING_SIX_NODE_FOUR_EDGE_REVIEW_FIXTURE',
            'exhaustive': False,
            'counter_evidence': 'COMPETING_MODEL_CANDIDATE_ONLY',
            'observed_retractions': 0,
            'accepted_edges': 0,
        },
    }
    # Review generation may carry a changed repository digest, but it must
    # still obey the closed schema, typed provenance and no-promotion fields.
    from jsonschema import Draft202012Validator
    schema = load_json(SCHEMA.read_bytes())
    schema['properties']['input']['properties']['sha256'] = {
        'type': 'string', 'pattern': '^[a-f0-9]{64}$',
    }
    if not Draft202012Validator(schema).is_valid(result):
        raise ValueError('unsafe review projection')
    return result


def load_input_bytes():
    return INPUT.read_bytes()


def build():
    raw = load_input_bytes()
    upstream = load_json(raw)
    return project(upstream, hashlib.sha256(raw).hexdigest())


def validate(data):
    from jsonschema import Draft202012Validator
    privacy_check(data)
    schema = load_json(SCHEMA.read_bytes())
    Draft202012Validator.check_schema(schema)
    if not Draft202012Validator(schema).is_valid(data):
        raise ValueError('question graph schema violation')
    raw = load_input_bytes()
    if hashlib.sha256(raw).hexdigest() != INPUT_SHA256:
        raise ValueError('question graph input drift')
    upstream = load_json(raw)
    if validate_upstream(upstream):
        raise ValueError('upstream graph governance violation')
    if canonical(data) != canonical(project(upstream, INPUT_SHA256)):
        raise ValueError('question graph deterministic projection mismatch')


def retrieve(data, node_id='node:question:BQ001', view='all'):
    """Question returns the bounded fixture; other IDs return incident edges.

    No recursive traversal, ranking, evidence voting, or implicit acceptance.
    Curated means selected direct metadata, never adjudicated scientific truth.
    """
    validate(data)
    if view not in {'all', 'curated', 'inferred'}:
        raise ValueError('unknown graph view')
    nodes = {n['node_id']: n for n in data['nodes']}
    if node_id not in nodes:
        raise ValueError('unknown graph node')
    selected = set(data['curated_edge_ids'] if view == 'curated' else data['inferred_edge_ids'] if view == 'inferred' else [e['edge_id'] for e in data['edges']])
    edges = [e for e in data['edges'] if e['edge_id'] in selected and (
        node_id == 'node:question:BQ001' or node_id in {e['source_node_id'], e['target_node_id']}
    )]
    visible = {node_id} | {e[k] for e in edges for k in ('source_node_id', 'target_node_id')}
    result = {
        'schema_version': 'akashicnet.bq001.question-graph-result.v0.1',
        'question_id': 'BQ001', 'question_status': 'UNRESOLVED', 'finality': 'NEVER_FINAL',
        'mode': 'REVIEW_ONLY', 'node_id': node_id, 'view': view,
        'guards': dict(GUARDS), 'baseline_locks': data['baseline_locks'],
        'input': data['input'], 'source_artifacts': data['source_artifacts'],
        'coverage': data['coverage'],
        'nodes': [nodes[key] for key in sorted(visible)],
        'curated_edges': [e for e in edges if e['edge_id'] in data['curated_edge_ids']],
        'inferred_candidates': [e for e in edges if e['edge_id'] in data['inferred_edge_ids']],
    }
    return copy.deepcopy(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'validate', 'query'])
    parser.add_argument('--node', default='node:question:BQ001')
    parser.add_argument('--view', choices=['all', 'curated', 'inferred'], default='all')
    args = parser.parse_args()
    try:
        if args.command == 'build':
            OUTPUT.write_text(canonical(build()), encoding='utf-8')
            print('BQ001 Question Graph v0.1 generated for review')
        else:
            data = load_json(OUTPUT.read_bytes())
            if args.command == 'validate':
                validate(data)
                if OUTPUT.read_text(encoding='utf-8') != canonical(data):
                    raise ValueError('noncanonical serialization')
                print('BQ001 Question Graph v0.1 PASS; unresolved; zero accepted edges')
            else:
                print(canonical(retrieve(data, args.node, args.view)), end='')
    except (ValueError, TypeError, KeyError, OSError, IndexError, AttributeError):
        print('BQ001 Question Graph FAIL; no retrieval or promotion', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
