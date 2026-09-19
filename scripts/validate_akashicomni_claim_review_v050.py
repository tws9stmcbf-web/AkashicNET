#!/usr/bin/env python3
"""Validate review-only records; structural success never releases the framework."""
import argparse
import itertools
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'schemas/akashicomni-claim-review-v0.5.0.schema.json'
PILOT = ROOT / 'data/akashicomni/meditation-crime-pilot-v0.5.0.json'


def compare_assessments(assessments):
    """Compare declared-independent human decisions, not truth or rationale quality."""
    eligible = sorted((a for a in assessments
                       if a['reviewer_type'] == 'HUMAN'
                       and a['independence'] == 'DECLARED_INDEPENDENT'),
                      key=lambda a: a['assessment_id'])
    return [{'assessment_ids': [a['assessment_id'], b['assessment_id']],
             'decision_agreement': a['decision'] == b['decision']}
            for a, b in itertools.combinations(eligible, 2)
            if a['reviewer_id'] != b['reviewer_id']]


def validate(packet):
    schema = json.loads(SCHEMA.read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    errors = [f"{'/'.join(map(str, e.absolute_path))}: {e.message}"
              for e in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(packet)]
    if errors:
        return errors

    def unique(values, label):
        if len(values) != len(set(values)):
            errors.append(f'{label}: duplicate identifiers')

    unique([s['source_id'] for s in packet['sources']], 'sources')
    unique([c['claim_id'] for c in packet['claims']], 'claims')
    sources = {s['source_id']: s for s in packet['sources']}
    for claim in packet['claims']:
        cid = claim['claim_id']
        refs = claim['source_ids']
        if not set(refs) <= sources.keys():
            errors.append(f'{cid}: unknown source reference')
        elif any(sources[s]['access_status'] == 'NOT_REINSPECTED' for s in refs):
            if not claim['missing_evidence']:
                errors.append(f'{cid}: uninspected sources require a missing-evidence entry')
            if claim['supporting_observations']:
                errors.append(f'{cid}: reinspect sources before entering supporting observations')
        revisions = claim['revision_history']
        if [r['revision'] for r in revisions] != list(range(1, len(revisions) + 1)):
            errors.append(f'{cid}: revisions must be sequential from 1')
        if [r['date'] for r in revisions] != sorted(r['date'] for r in revisions):
            errors.append(f'{cid}: revision dates must not move backwards')
        assessments = claim['assessments']
        unique([a['assessment_id'] for a in assessments], f'{cid} assessments')
        unique([a['reviewer_id'] for a in assessments], f'{cid} current reviewers')
        for a in assessments:
            if a['reviewer_type'] == 'AI' and a['independence'] != 'NOT_ESTABLISHED':
                errors.append(f'{cid}: AI output cannot declare independent human review')
        comparison = claim['comparison']
        expected = compare_assessments(assessments)
        if comparison['status'] == 'PENDING':
            if any(comparison[k] for k in ('pairs', 'agreements', 'disagreements')):
                errors.append(f'{cid}: pending comparison must not invent results')
        else:
            if not expected or comparison['pairs'] != expected:
                errors.append(f'{cid}: comparison must contain all computed independent-human pairs')
            if any(p['decision_agreement'] for p in expected) and not comparison['agreements']:
                errors.append(f'{cid}: explain recorded decision agreement')
            if any(not p['decision_agreement'] for p in expected) and not comparison['disagreements']:
                errors.append(f'{cid}: preserve recorded decision disagreement')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet', nargs='?', type=Path, default=PILOT)
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.packet.read_text(encoding='utf-8')))
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    if errors:
        print('AkashicOMNI draft contract: FAIL\n' + '\n'.join(errors))
        return 1
    print('AkashicOMNI draft contract: PASS; UNRELEASED; independent review PENDING')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
