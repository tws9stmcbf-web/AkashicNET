#!/usr/bin/env python3
"""Validate review-only records; structural success never releases the framework."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / 'schemas/akashicomni-claim-review-v0.5.0.schema.json'
PILOT = ROOT / 'data/akashicomni/meditation-crime-pilot-v0.5.0.json'
VERIFICATIONS = ROOT / 'references/akashicomni/trusted-verifications-v0.5.0.json'


def load_verifications():
    """Repository policy input, never a packet-selected file or remote URL."""
    records = json.loads(VERIFICATIONS.read_text(encoding='utf-8'))
    if (not isinstance(records, dict)
            or set(records) != {'reviewer_attestations', 'source_inspections'}
            or any(not isinstance(v, list) or any(not isinstance(r, dict) for r in v)
                   for v in records.values())):
        raise ValueError('invalid trusted verification registry')
    return records


def verification_record(packet, *, source=None, claim=None, assessment=None):
    """Bind attestations to exact content; a URL or reviewer label is not trust."""
    if source is not None:
        subject = source
        verification = source['inspection_verification']
    else:
        subject = {
            'claim': {k: v for k, v in claim.items() if k not in ('assessments', 'comparison')},
            'sources': packet['sources'],
            'assessment': assessment,
        }
        verification = assessment['reviewer_verification']
    digest = hashlib.sha256(json.dumps(subject, sort_keys=True, ensure_ascii=True,
                                       separators=(',', ':')).encode('utf-8')).hexdigest()
    return {'packet_id': packet['packet_id'], 'subject_sha256': digest,
            'verification': verification}


def trusted_verification(packet, kind, **subject):
    record = verification_record(packet, **subject)
    if not record['verification'] or record['verification'].get('status') != 'HUMAN_VERIFIED':
        return False
    try:
        return record in load_verifications()[kind]
    except (OSError, ValueError):
        return False


def compare_assessments(assessments, packet=None, claim=None):
    """Compare real, human-verified independent reviewers; never test personas."""
    if packet is None or claim is None:
        return []
    eligible = sorted((a for a in assessments
                       if a['reviewer_type'] == 'HUMAN'
                       and a['independence'] == 'DECLARED_INDEPENDENT'
                       and a.get('provenance') == 'REAL_REVIEW'
                       and a.get('reviewer_verification')
                       and a['reviewer_verification'].get('verified_by') != a['reviewer_id']
                       and trusted_verification(packet, 'reviewer_attestations',
                                                claim=claim, assessment=a)),
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
    try:
        load_verifications()
    except (OSError, ValueError) as exc:
        return [f'trusted verification registry: {exc}']

    def unique(values, label):
        if len(values) != len(set(values)):
            errors.append(f'{label}: duplicate identifiers')

    unique([s['source_id'] for s in packet['sources']], 'sources')
    unique([c['claim_id'] for c in packet['claims']], 'claims')
    sources = {s['source_id']: s for s in packet['sources']}
    for source in packet['sources']:
        if source['inspection_verification'] and not trusted_verification(
                packet, 'source_inspections', source=source):
            errors.append(f"{source['source_id']}: inspection attestation is not repository-trusted")
        if source['inspection_verification'] and source['access_status'] != 'FULL_TEXT_INSPECTED':
            errors.append(f"{source['source_id']}: inspection verification requires full-text inspection")
        if 'artifact' in source:
            artifact = source['artifact']
            path = (ROOT / artifact['repository_path']).resolve()
            try:
                if not path.is_relative_to(ROOT) or not path.is_file():
                    raise ValueError('missing or non-repository artifact')
                if hashlib.sha256(path.read_bytes()).hexdigest() != artifact['sha256']:
                    raise ValueError('artifact digest mismatch')
            except (OSError, ValueError) as exc:
                errors.append(f"{source['source_id']}: {exc}")
    for claim in packet['claims']:
        cid = claim['claim_id']
        refs = claim['source_ids']
        lineage = sources.get(claim['lineage_source_id'])
        if (claim['lineage_source_id'] not in refs or not lineage
                or lineage['source_kind'] != 'EDITORIAL_DRAFT'):
            errors.append(f'{cid}: lineage must reference a registered editorial artifact in source_ids')
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
            if a['provenance'] == 'SYNTHETIC_FIXTURE':
                errors.append(f'{cid}: synthetic fixtures are forbidden in governed packets')
            if a['reviewer_verification']:
                if not trusted_verification(packet, 'reviewer_attestations', claim=claim, assessment=a):
                    errors.append(f'{cid}: reviewer attestation is not repository-trusted')
                if a['reviewer_type'] != 'HUMAN' or a['provenance'] != 'REAL_REVIEW':
                    errors.append(f'{cid}: only real humans may carry reviewer verification')
                if a['reviewer_verification']['verified_by'] == a['reviewer_id']:
                    errors.append(f'{cid}: reviewer cannot self-verify independence')
            if a['decision'] == 'SUPPORT' and any(
                    s not in sources or sources[s]['access_status'] != 'FULL_TEXT_INSPECTED'
                    or not trusted_verification(packet, 'source_inspections', source=sources[s])
                    for s in refs):
                errors.append(f'{cid}: SUPPORT requires human-verified full-text inspection of every source')
            if a['reviewer_type'] == 'AI' and a['independence'] != 'NOT_ESTABLISHED':
                errors.append(f'{cid}: AI output cannot declare independent human review')
        comparison = claim['comparison']
        expected = compare_assessments(assessments, packet, claim)
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
