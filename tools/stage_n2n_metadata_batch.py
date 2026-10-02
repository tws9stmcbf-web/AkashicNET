"""Reproduce the offline review queue pinned to PR #376; never fetch Reddit."""
import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.reddit_corpus_census import canonicalise
from tools.search_reddit import load_records

HEAD = '808564658800a1ab230bbb837aa3b228911d671f'
BATCH = 'references/community/n2n-metadata-batch-0001.json'
PINS = {
    'references/community/reddit-uri-index.csv': '3a6a702061cff7ae9e8d555b1de32b17cba9401f59451fce739f7f8411804b80',
    'references/community/n2n-index.csv': '6d6ea88cbeda0a14b281246201e9cc711d74b28898531951da57dcdfdd36595a',
    'scripts/reddit_corpus_census.py': '5377d0454e8f22c4684becd611a6136549ddba8e1c21be7d75dfce5d1b5e3845',
    'tools/search_reddit.py': '1e8286abff822f2edfc34f180aa5c0bf7b88eaa5df85bd1e8d6857208330f8d4',
}
URI, META = list(PINS)[:2]


def build(root=ROOT, batch_number=1):
    if type(batch_number) is not int or batch_number not in (1, 2, 3, 4, 5, 6, 7):
        raise ValueError("only reviewed batches 1 through 7 are supported")
    previous = None
    earlier = []
    if batch_number > 1:
        for number in range(1, batch_number):
            prior_path = f'references/community/n2n-metadata-batch-{number:04d}.json'
            prior = json.loads((root / prior_path).read_text(encoding='utf-8'))
            validate(prior, root, number)
            earlier.append(prior)
        previous = earlier[-1]
    for path, digest in PINS.items():
        if hashlib.sha256((root / path).read_bytes()).hexdigest() != digest:
            raise ValueError(f'pinned source drift: {path}')
    records = load_records(root / URI, root / META)
    eligible = [r for r in records if not r['metadata']]
    selected = sorted(eligible, key=lambda r: (not bool(r['historical_annotations']), r['post_id']))[(batch_number - 1) * 1000:batch_number * 1000]
    provenance = defaultdict(list)
    statuses = Counter()
    with (root / URI).open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.reader(handle)
        next(reader)
        for ordinal, row in enumerate(reader, 2):
            if not row:
                continue
            parsed = canonicalise(row[0])
            statuses[parsed['status']] += 1
            if parsed.get('subreddit', '').casefold() == 'neuronstonirvana' and parsed.get('post_id'):
                provenance[parsed['post_id']].append({'csv_record_ordinal': ordinal, 'raw_value': row[0]})
    counts = {
        'archive_unique_n2n_records': len(records),
        'curated_before': sum(bool(r['metadata']) for r in records),
        'eligible_uncurated': len(eligible),
        'selected': len(selected),
        'selected_with_historical_annotations': sum(bool(r['historical_annotations']) for r in selected),
        'selected_without_historical_annotations': sum(not r['historical_annotations'] for r in selected),
        'remaining_uncurated_outside_batch': len(eligible) - len(selected),
        'new_curated_records': 0, 'curated_after': 3,
    }
    expected_annotations = 997 if batch_number == 1 else 0
    if list(counts.values()) != [7399, 3, 7396, 1000, expected_annotations, 1000 - expected_annotations, 6396, 0, 3]:
        raise ValueError(f'count drift: {counts}')
    result = []
    for rank, r in enumerate(selected, 1):
        result.append({
            'rank': rank, 'post_id': r['post_id'], 'archived_url': r['Reddit URL'],
            'source_locations': r['source_locations'],
            'historical_annotations': r['historical_annotations'],
            'archive_provenance': provenance[r['post_id']],
            'record_kind': 'ARCHIVED_URL_ONLY', 'stage': 'QUEUED_FOR_OFFLINE_METADATA_REVIEW',
            'title': None, 'current_flair': None, 'author': None,
            'evidence_status': None, 'rights_status': None, 'metadata': {},
        })
    manifest = {
        'schema': 'akashicnet.n2n.metadata-review-batch.v1', 'batch_id': f'N2N-METADATA-{batch_number:04d}',
        'source_boundary': {'repository': 'tws9stmcbf-web/AkashicNET', 'pull_request': 376,
                            'head': HEAD, 'sha256': PINS},
        'selection_rule': 'Exclude records with curated metadata; sort annotated records first, then lowercase post_id in ascending lexical order; take first 1000. No chronological, evidential or representative-sample claim.',
        'counts': counts,
        'distribution': {
            'archive_csv_status_counts': dict(sorted(statuses.items())),
            'archive_annotation_count_histogram': dict(sorted(Counter(str(len(r['historical_annotations'])) for r in records).items())),
            'curated_post_ids_excluded': sorted(r['post_id'] for r in records if r['metadata']),
            'selected_archive_row_references': sum(len(r['archive_provenance']) for r in result),
            'selected_historical_annotation_values': sum(len(r['historical_annotations']) for r in result),
        },
        'boundaries': {'live_reddit_access': 'HOLD', 'source_bodies_ingested': 0,
            'comments_ingested': 0, 'media_ingested': 0, 'accepted_canonical_edges': 0,
            'supports_models': [], 'rights_gate': 'CLOSED', 'evidence_gate': 'CLOSED',
            'privacy_gate': 'CLOSED', 'publication_gate': 'CLOSED', 'promotion_gate': 'CLOSED',
            'truth_inference': False, 'website_updated': False,
            'post_existence_verified': False, 'archive_wide_authorship_verified': False},
        'records': result,
    }

    if previous is not None:
        prior_ids = {r['post_id'] for prior in earlier for r in prior['records']}
        selected_ids = {r['post_id'] for r in result}
        if prior_ids & selected_ids or len(prior_ids | selected_ids) != batch_number * 1000:
            raise ValueError('cross-batch overlap or count drift')
        manifest['selection_rule'] = 'Use the same eligible ordering as batch 0001; exclude its 1000 validated IDs and take the next 1000 (global eligible ranks 1001-2000). No chronological, evidential or representative-sample claim.' if batch_number == 2 else 'Use the same eligible ordering as batch 0001; exclude all 2000 validated IDs in batches 0001 and 0002 and take the next 1000 (global eligible ranks 2001-3000). No chronological, evidential or representative-sample claim.'
        if batch_number == 4:
            manifest['selection_rule'] = 'Use the same eligible ordering as batch 0001; exclude all 3000 validated IDs in batches 0001 through 0003 and take the next 1000 (global eligible ranks 3001-4000). No chronological, evidential or representative-sample claim.'
        if batch_number == 5:
            manifest['selection_rule'] = 'Use the same eligible ordering as batch 0001; exclude all 4000 validated IDs in batches 0001 through 0004 and take the next 1000 (global eligible ranks 4001-5000). No chronological, evidential or representative-sample claim.'
        if batch_number == 6:
            manifest['selection_rule'] = 'Use the same eligible ordering as batch 0001; exclude all 5000 validated IDs in batches 0001 through 0005 and take the next 1000 (global eligible ranks 5001-6000). No chronological, evidential or representative-sample claim.'
        if batch_number == 7:
            manifest['selection_rule'] = 'Use the same eligible ordering as batch 0001; exclude all 6000 validated IDs in batches 0001 through 0006 and take the next 1000 (global eligible ranks 6001-7000). No chronological, evidential or representative-sample claim.'
        prior_path = f'references/community/n2n-metadata-batch-{batch_number - 1:04d}.json'
        manifest['previous_batch'] = {'path': prior_path, 'sha256': hashlib.sha256((root / prior_path).read_bytes()).hexdigest()}
        manifest['counts'].update(previously_staged=len(prior_ids), overlap_with_previous=0,
                                  cumulative_staged_unique=len(prior_ids | selected_ids),
                                  remaining_uncurated_outside_all_batches=len(eligible) - len(prior_ids | selected_ids))
    return manifest


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n'


def validate(value, root=ROOT, batch_number=1):
    # Canonical byte-level comparison also rejects extra keys, null substitutions,
    # bool/int confusion, changes in order, provenance, fields or closed gates.
    if encode(value) != encode(build(root, batch_number)):
        raise ValueError('batch differs from pinned deterministic review queue')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--batch', type=int, choices=(1, 2, 3, 4, 5, 6, 7), default=1)
    args = parser.parse_args()
    expected = build(batch_number=args.batch)
    path = ROOT / f'references/community/n2n-metadata-batch-{args.batch:04d}.json'
    if args.write:
        path.write_text(encode(expected), encoding='utf-8')
    validate(json.loads(path.read_text(encoding='utf-8')), batch_number=args.batch)
    print(json.dumps({'validation': 'PASS', **expected['counts'], **expected['distribution']}, indent=2))


if __name__ == '__main__':
    main()
