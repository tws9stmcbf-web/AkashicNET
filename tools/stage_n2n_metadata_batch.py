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


def build(root=ROOT):
    for path, digest in PINS.items():
        if hashlib.sha256((root / path).read_bytes()).hexdigest() != digest:
            raise ValueError(f'pinned source drift: {path}')
    records = load_records(root / URI, root / META)
    eligible = [r for r in records if not r['metadata']]
    selected = sorted(eligible, key=lambda r: (not bool(r['historical_annotations']), r['post_id']))[:1000]
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
    if list(counts.values()) != [7399, 3, 7396, 1000, 997, 3, 6396, 0, 3]:
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
    return {
        'schema': 'akashicnet.n2n.metadata-review-batch.v1', 'batch_id': 'N2N-METADATA-0001',
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


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n'


def validate(value, root=ROOT):
    # Canonical byte-level comparison also rejects extra keys, null substitutions,
    # bool/int confusion, changes in order, provenance, fields or closed gates.
    if encode(value) != encode(build(root)):
        raise ValueError('batch differs from pinned deterministic review queue')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    expected = build()
    path = ROOT / BATCH
    if args.write:
        path.write_text(encode(expected), encoding='utf-8')
    validate(json.loads(path.read_text(encoding='utf-8')))
    print(json.dumps({'validation': 'PASS', **expected['counts'], **expected['distribution']}, indent=2))


if __name__ == '__main__':
    main()
