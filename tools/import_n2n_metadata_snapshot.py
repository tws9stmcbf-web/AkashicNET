"""Validate a metadata-only snapshot and emit an unreviewed offline overlay."""
import argparse
import csv
import hashlib
import io
import json
from datetime import datetime
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.stage_n2n_metadata_batch import HEAD, PINS, URI, META
from tools.search_reddit import load_records

COLUMNS = ['post_id', 'source_url', 'title', 'created_at', 'author', 'flair_at_capture', 'outbound_url']
FIELDS = COLUMNS[2:]
BOUNDARIES = {'live_reddit_access': 'NOT_USED_BY_OFFLINE_IMPORTER', 'rights_gate': 'CLOSED', 'evidence_gate': 'CLOSED',
              'privacy_gate': 'CLOSED', 'publication_gate': 'CLOSED', 'promotion_gate': 'CLOSED',
              'canonical_metadata_write': False, 'website_updated': False,
              'source_bodies_ingested': 0, 'comments_ingested': 0, 'media_ingested': 0}


def timestamp(value):
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if dt.utcoffset() is None:
            raise ValueError('timezone required')
        return dt
    except (ValueError, TypeError, AttributeError) as exc:
        raise ValueError('expected an ISO timestamp with timezone') from exc


def url(value):
    p = urlsplit(value)
    if p.scheme not in ('https', 'http') or not p.hostname or p.username or p.password:
        raise ValueError('expected an HTTP(S) URL without credentials')
    return p


def candidates(snapshot, receipt, root=ROOT, limit=1000):
    if isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 1000:
        raise ValueError('batch limit must be an integer from 1 to 1000')
    required = {'schema', 'source_head', 'snapshot_sha256', 'captured_at', 'source_description', 'acquisition_method'}
    if not isinstance(receipt, dict) or set(receipt) != required:
        raise ValueError('receipt fields differ from contract')
    if receipt['schema'] != 'akashicnet.n2n.snapshot-receipt.v1' or receipt['source_head'] != HEAD:
        raise ValueError('receipt schema or archive boundary mismatch')
    if receipt['acquisition_method'] not in ('existing_export', 'saved_metadata_snapshot'):
        raise ValueError('only existing offline sources supported')
    if not isinstance(receipt['source_description'], str) or not receipt['source_description'].strip():
        raise ValueError('attributable source description required')
    capture = timestamp(receipt['captured_at'])
    digest = hashlib.sha256(snapshot).hexdigest()
    if receipt['snapshot_sha256'] != digest:
        raise ValueError('snapshot hash mismatch')
    for path, expected in PINS.items():
        if hashlib.sha256((root / path).read_bytes()).hexdigest() != expected:
            raise ValueError('archive input drift: ' + path)
    archive = {r['post_id']: r for r in load_records(root / URI, root / META)}
    reader = csv.DictReader(io.StringIO(snapshot.decode('utf-8-sig'), newline=''))
    if reader.fieldnames != COLUMNS:
        raise ValueError('exact metadata-only CSV columns required')
    records, seen = [], set()
    for ordinal, row in enumerate(reader, 2):
        if len(records) == limit:
            raise ValueError('snapshot exceeds the bounded batch limit')
        if None in row or any(v is None for v in row.values()):
            raise ValueError('malformed CSV row')
        ident = row['post_id']
        if not re.fullmatch('[a-z0-9]+', ident) or ident in seen or ident not in archive:
            raise ValueError('unknown, duplicate or malformed post ID')
        seen.add(ident)
        original = archive[ident]
        if original['metadata']:
            raise ValueError('curated records require separate conflict review')
        p = url(row['source_url'])
        if p.hostname not in ('reddit.com', 'www.reddit.com', 'old.reddit.com') or not re.match(r'^/r/NeuronsToNirvana/comments/' + re.escape(ident) + r'(?:/|$)', p.path, re.I):
            raise ValueError('source URL does not identify the N2N post')
        if row['created_at'] and timestamp(row['created_at']) > capture:
            raise ValueError('creation date is after capture date')
        if row['outbound_url']:
            url(row['outbound_url'])
        values = {}
        for field in FIELDS:
            value = row[field]
            if value:
                if not value.strip():
                    raise ValueError('whitespace-only value is not metadata')
                values[field] = {'value': value, 'snapshot_sha256': digest,
                                 'csv_record_ordinal': ordinal, 'source_column': field,
                                 'source_url': row['source_url'], 'captured_at': receipt['captured_at']}
        if not values:
            raise ValueError('record has no descriptive values')
        records.append({'post_id': ident, 'archived_url': original['Reddit URL'],
                        'source_locations': original['source_locations'],
                        'candidate_metadata': values, 'review_status': 'UNREVIEWED_SOURCE_ASSERTION',
                        'current_verification': 'NOT_PERFORMED', 'current_flair': None,
                        'rights_status': None, 'evidence_status': None})
    if not records:
        raise ValueError('empty pilot')
    return {'schema': 'akashicnet.n2n.snapshot-candidates.v1', 'source_head': HEAD,
            'archive_sha256': PINS, 'receipt': receipt, 'boundaries': BOUNDARIES.copy(),
            'counts': {'candidate_records': len(records), 'candidate_field_values': sum(len(r['candidate_metadata']) for r in records),
                       'new_verified_records': 0, 'new_curated_records': 0},
            'records': sorted(records, key=lambda r: r['post_id'])}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot', type=Path)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('--limit', type=int, default=1000)
    args = parser.parse_args()
    print(json.dumps(candidates(args.snapshot.read_bytes(), json.loads(args.receipt.read_text()), limit=args.limit), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
