#!/usr/bin/env python3
from __future__ import annotations

import csv,hashlib,json
from collections import Counter
from pathlib import Path

SOURCE=Path('references/community/akashic-master-index.csv')
OUT=Path('data/evidence-classification-v0.43.csv')
FIELDS=['evidence_record_id','source_record_id','source','source_type','canonical_url','evidence_class','classification_basis','scientific_evidence_status','review_state']

CLASS_MAP={
    'post':'COMMUNITY_POST',
    'subreddit':'COMMUNITY_COLLECTION',
    'book':'BOOK_OR_LONGFORM_METADATA',
    'article':'ARTICLE_UNRESOLVED',
    'unknown':'UNKNOWN',
}


def stable_id(row:dict)->str:
    raw='|'.join([(row.get('record_id') or ''),(row.get('source') or ''),(row.get('url') or '')])
    return 'evidence_'+hashlib.sha256(raw.encode()).hexdigest()[:24]


def main():
    rows=list(csv.DictReader(SOURCE.open(encoding='utf-8-sig',newline='')))
    counts=Counter()
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS); w.writeheader()
        for r in rows:
            st=(r.get('source_type') or 'unknown').strip().lower() or 'unknown'
            cls=CLASS_MAP.get(st,'UNKNOWN')
            counts[cls]+=1
            w.writerow({
                'evidence_record_id':stable_id(r),
                'source_record_id':r.get('record_id') or '',
                'source':r.get('source') or '',
                'source_type':r.get('source_type') or '',
                'canonical_url':r.get('url') or '',
                'evidence_class':cls,
                'classification_basis':'explicit source_type metadata only',
                'scientific_evidence_status':'NOT_EVALUATED',
                'review_state':'UNREVIEWED' if cls in {'ARTICLE_UNRESOLVED','UNKNOWN'} else 'METADATA_CLASSIFIED',
            })
    report={
        'version':'0.43','records':len(rows),'counts':dict(sorted(counts.items())),
        'classification_scope':'source-form metadata only',
        'article_is_scientific_evidence':False,'scientific_evidence_evaluated':0,
        'truth_inference_allowed':False,'rights_promotion_allowed':False,
        'body_reads':0,'embeddings_created':0,'output':str(OUT),
    }
    print(json.dumps(report,sort_keys=True))

if __name__=='__main__': main()
