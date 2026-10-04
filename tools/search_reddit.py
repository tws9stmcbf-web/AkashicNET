"""Search archived source locations and curated metadata without network access."""
import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.reddit_corpus_census import canonicalise

INDEX = ROOT / 'references/community/n2n-index.csv'
URI_INDEX = ROOT / 'references/community/reddit-uri-index.csv'


def load_records(uri_index=URI_INDEX, metadata_index=INDEX):
    records = {}
    with uri_index.open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.reader(handle)
        next(reader, None)
        for row in reader:
            if not row:
                continue
            source = canonicalise(row[0])
            if source['status'] not in {'candidate', 'annotation_derived'}:
                continue
            if source['subreddit'].casefold() != 'neuronstonirvana':
                continue
            key = source['post_id']
            record = records.setdefault(key, {
                'post_id': key, 'Reddit URL': source['canonical_url'],
                'record_kind': 'ARCHIVED_URL_ONLY', 'source_locations': [],
                'historical_annotations': [], 'metadata': {},
                'claim_review': 'NOT_ASSESSED_BY_THIS_TOOL',
            })
            if source['canonical_url'] not in record['source_locations']:
                record['source_locations'].append(source['canonical_url'])
            if source.get('annotation') and source['annotation'] not in record['historical_annotations']:
                record['historical_annotations'].append(source['annotation'])
    if metadata_index.exists():
        with metadata_index.open(encoding='utf-8-sig', newline='') as handle:
            for row in csv.DictReader(handle):
                source = canonicalise(row.get('Reddit URL', ''))
                if source.get('subreddit', '').casefold() != 'neuronstonirvana':
                    continue
                record = records.get(source.get('post_id'))
                if record is not None:
                    record['metadata'] = row
                    record['record_kind'] = 'ARCHIVED_URL_WITH_CURATED_METADATA'
    return list(records.values())


def search(records, query):
    query = query.casefold().strip()
    return [r for r in records if query in ' '.join([
        r['post_id'], *r['source_locations'], *r['historical_annotations'],
        *(str(v) for v in r['metadata'].values()),
    ]).casefold()]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('-n', '--limit', type=int, default=20)
    parser.add_argument('--json', action='store_true', help='Return bounded search results as JSON')
    args = parser.parse_args()
    if args.limit < 0:
        parser.error('--limit must be nonnegative')
    records = load_records()
    matches = search(records, args.query)
    result = {
        'archive_records': len(records), 'matching_records': len(matches),
        'returned_records': min(args.limit, len(matches)),
        'boundary': 'Archived locations and curated metadata only; no live access, full-text review, authorship verification, rights or evidence promotion. Presence in the archive or search output does not establish current public visibility or PUBLIC_VERIFIED/ELIGIBLE status; publication requires the existing sensitivity, rights and public-manifest reviews.',
        'records': matches[:args.limit],
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Archive: {len(records)} unique N2N records; {len(matches)} matches")
        print(result['boundary'])
        for record in matches[:args.limit]:
            print('\nTITLE:', record['metadata'].get('title') or '[Title not captured]')
            print('KIND:', record['record_kind'])
            print('URL:', record['Reddit URL'])
            for annotation in record['historical_annotations']:
                print('HISTORICAL ANNOTATION (not current flair):', annotation)
            for field, value in record['metadata'].items():
                if field != 'title' and value:
                    print(f'CURATED {field}:', value)
        if len(matches) > args.limit:
            print(f'Showing first {args.limit} of {len(matches)} matches.')


if __name__ == '__main__':
    main()
