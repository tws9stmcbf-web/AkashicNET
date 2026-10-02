"""Offline historical receipt overlay; no current verification or curated promotion."""
import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.stage_n2n_metadata_batch import build as build_first, encode, HEAD
from tools.search_reddit import load_records
PINS = {'references/community/reddit-manual-delta-batch-0002.csv': 'd97011b3ab2bd7e542f62ff17da0b2545f983decd3450871ca87d7f76be05193', 'references/community/reddit-manual-delta-batch-0003.csv': 'cd314cc22775a98c1d3e1423671c964b09ab6b5fa287a918658a7b3552f0b61b', 'references/community/reddit-manual-delta-batch-0004.csv': 'e39b755c86b38c61b678300406354bc7aeb78482a487d65ccc5e8031fa0aadd5', 'references/community/reddit-manual-delta-batch-0005.csv': '5ea83c66119a31df795143a6ecaecfc984bd5e7f10589a36302808b503bb8997', 'references/community/reddit-manual-delta-batch-0006.csv': '08172bf3cda9264f3c49b66a8ef1a7661c847bf5576e1cb7e0949085184d59b6', 'references/community/REDDIT_HISTORICAL_PROVENANCE_AUDIT_V0.7.md': '9fcfce2e31ecafddefe69c388017d71d2c4d02887ed9ef7262f95aab8f4b653b', 'references/community/n2n-metadata-batch-0001.json': '23bcb5a4cceec77a123946174ad068a93474aaa5e342e21c6a66f0ef9b8ead57', 'references/community/n2n-metadata-batch-0002.json': 'f8c982e63c8cf7bd52803d6dad8b275a7afaec4b47f98800d5fe93c578f23893', 'references/community/n2n-metadata-batch-0003.json': 'dd1401ea856f4a4ebb99e02713c0711807eaac38a4455877e69f2f8265419e28', 'references/community/n2n-metadata-batch-0004.json': '8f2f3e076e35235fb7ac9baca00b8dba851ff779e23169321e50b61b1d3cee2c', 'references/community/n2n-metadata-batch-0005.json': 'c9e44a7bc50c185de9c10f54c2688fdccfaeb57e37be4876f07f6beecebba9b7'}
OUTPUT = 'references/community/n2n-historical-observation-pilot-0025.json'
FEEDS = [f'references/community/reddit-manual-delta-batch-{n:04d}.csv' for n in range(2, 7)]
BATCHES = [f'references/community/n2n-metadata-batch-{n:04d}.json' for n in range(1, 6)]


def build(root=ROOT, batch_number=1):
    if type(batch_number) is not int or batch_number not in (1, 2):
        raise ValueError('only provenance pilot batches 1 and 2 are enabled')
    prior = None
    if batch_number == 2:
        prior = json.loads((root / OUTPUT).read_text())
        validate(prior, root)
    for path, digest in PINS.items():
        if hashlib.sha256((root / path).read_bytes()).hexdigest() != digest:
            raise ValueError(f'pinned input drift: {path}')
    first = build_first(root)
    archive = {r['post_id']: r for r in load_records(root / 'references/community/reddit-uri-index.csv', root / 'references/community/n2n-index.csv')}
    staged = {r['post_id'] for path in BATCHES for r in json.loads((root / path).read_text())['records']}
    receipts = defaultdict(list)
    for path in FEEDS:
        with (root / path).open(newline='', encoding='utf-8-sig') as handle:
            for ordinal, row in enumerate(csv.DictReader(handle), 2):
                if row['subreddit'].casefold() == 'neuronstonirvana':
                    receipts[row['reddit_post_id']].append({'source_path': path, 'csv_record_ordinal': ordinal, 'historical_observation': row})
    eligible = sorted(i for i in receipts if i in archive and not archive[i]['metadata'])
    if len(eligible) != 125 or len(staged) != 5000 or set(eligible) & staged:
        raise ValueError('historical receipt population drift')
    rows = []
    for i in eligible[(batch_number - 1) * 25:batch_number * 25]:
        rows.append({'post_id': i, 'archived_url': archive[i]['Reddit URL'],
                     'source_locations': archive[i]['source_locations'],
                     'historical_observation_receipts': receipts[i],
                     'observation_interpretation': 'Repository-recorded past observation only; not reverified now.',
                     'current_verification': 'NOT_PERFORMED', 'title': None, 'author': None,
                     'current_flair': None, 'evidence_status': None, 'rights_status': None,
                     'canonical_metadata_write': False})
    result = {'schema': 'akashicnet.n2n.historical-observation-pilot.v1',
            'source_head': HEAD,
            'source_sha256': PINS,
            'selection_rule': 'First 25 lowercase post IDs in lexical order from uncurated archive records with a historical N2N feed observation in manual delta batches 0002-0006. Separate provenance review overlay; not a sixth staging batch.',
            'counts': {'historical_feed_ids':125, 'selected':len(rows), 'selected_staging_overlap':0,
                       'staging_queue_unchanged':5000, 'curated_unchanged':3,
                       'new_curated_titles':0, 'new_authorship_verifications':0,
                       'current_reddit_requests':0},
            'boundaries': first['boundaries'],
            'limitations': ['Historical observation status is not a current public-visibility or API verification claim.',
                           'Unverified pilot CSV titles/summaries are not imported.',
                           'Archive origin remains unresolved in the pinned provenance audit; structural counts do not establish authenticity.',
                           'No public search/index integration or evidence, rights or maturity promotion.'],
            'records': rows}

    if prior is not None:
        ids = {r['post_id'] for r in rows}
        prior_ids = {r['post_id'] for r in prior['records']}
        if ids & prior_ids or len(ids | prior_ids) != 50:
            raise ValueError('pilot overlap or cumulative count drift')
        result['selection_rule'] = 'Next 25 lowercase post IDs in lexical order after excluding the first validated historical-observation pilot; eligible ranks 26-50. Separate provenance overlay, not a staging batch.'
        result['previous_pilot'] = {'path': OUTPUT, 'sha256': hashlib.sha256((root / OUTPUT).read_bytes()).hexdigest()}
        result['counts'].update(previous_provenance_records=25, overlap_with_previous=0,
                                cumulative_provenance_records=50, remaining_historical_feed_candidates=75)
    return result


def output_path(batch_number):
    return OUTPUT if batch_number == 1 else 'references/community/n2n-historical-observation-pilot-0025-batch-0002.json'


def validate(value, root=ROOT, batch_number=1):
    if encode(value) != encode(build(root, batch_number)):
        raise ValueError('pilot differs from pinned historical receipts')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write', action='store_true')
    p.add_argument('--batch', type=int, choices=(1, 2), default=1)
    args = p.parse_args()
    expected = build(batch_number=args.batch)
    destination = ROOT / output_path(args.batch)
    if args.write:
        destination.write_text(encode(expected))
    validate(json.loads(destination.read_text()), batch_number=args.batch)
    print(json.dumps({'validation':'PASS', **expected['counts']}, indent=2))


if __name__ == '__main__':
    main()
