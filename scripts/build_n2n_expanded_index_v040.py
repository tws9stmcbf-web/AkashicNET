#!/usr/bin/env python3
from __future__ import annotations

import csv,hashlib,json
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit

SOURCE=Path('references/community/akashic-master-index.csv')
OUTPUT=Path('data/n2n-expanded-index-v0.40.csv')
N2N_PREFIX='/r/neuronstonirvana/'
FIELDS=[
    'community_id','canonical_url','title','author','topics','source_type',
    'licence_status','reuse_decision','provenance_status','source_row_count','source_record_ids'
]


def canonical_url(url:str)->str:
    p=urlsplit((url or '').strip())
    host=p.netloc.lower()
    if host.startswith('www.'): host=host[4:]
    if host.startswith('old.'): host=host[4:]
    path=p.path.rstrip('/') or '/'
    return urlunsplit(('https',host,path,'',''))


def community_id(url:str)->str:
    return 'reddit_'+hashlib.sha256(url.encode()).hexdigest()[:24]


def main():
    groups=defaultdict(list)
    source_rows=0
    with SOURCE.open(encoding='utf-8-sig',newline='') as f:
        for row in csv.DictReader(f):
            if (row.get('source') or '').strip().lower()!='reddit':
                continue
            url=canonical_url(row.get('url') or '')
            if not url or urlsplit(url).netloc!='reddit.com' or N2N_PREFIX not in urlsplit(url).path.lower():
                continue
            source_rows+=1
            groups[url].append(row)

    OUTPUT.parent.mkdir(parents=True,exist_ok=True)
    with OUTPUT.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
        for url in sorted(groups):
            rows=groups[url]
            rows.sort(key=lambda r:((r.get('record_id') or ''),(r.get('title') or '')))
            representative=rows[0]
            record_ids=sorted({(r.get('record_id') or '').strip() for r in rows if (r.get('record_id') or '').strip()})
            w.writerow({
                'community_id':community_id(url),
                'canonical_url':url,
                'title':representative.get('title') or '',
                'author':representative.get('author') or '',
                'topics':representative.get('topics') or '',
                'source_type':representative.get('source_type') or '',
                'licence_status':representative.get('licence_status') or '',
                'reuse_decision':representative.get('reuse_decision') or '',
                'provenance_status':representative.get('provenance_status') or '',
                'source_row_count':len(rows),
                'source_record_ids':'|'.join(record_ids),
            })

    duplicate_source_rows=source_rows-len(groups)
    report={
        'index':'AKASHICNET_N2N_EXPANDED_INDEX','version':'0.40',
        'source_master_rows':source_rows,'canonical_records':len(groups),
        'duplicate_source_rows_collapsed':duplicate_source_rows,
        'pilot_checkpoint_records':1000,'pilot_preserved':True,
        'expansion_factor_vs_pilot':round(len(groups)/1000,3),
        'identity_basis':'normalized canonical Reddit URL',
        'metadata_and_links_only':True,'document_bodies_read':0,'embeddings_created':0,
        'scientific_evidence_default':False,'truth_inference_allowed':False,'rights_promotion_allowed':False,
        'automatic_cross_source_identity_links':False,
        'output':str(OUTPUT),
    }
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__': main()
