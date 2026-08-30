#!/usr/bin/env python3
from __future__ import annotations
import csv,json
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit,urlunsplit

PATH=Path('references/community/akashic-master-index.csv')
N2N_PREFIX='/r/neuronstonirvana/'


def canonical_url(url:str)->str:
    try:
        p=urlsplit((url or '').strip())
        host=p.netloc.lower()
        if host.startswith('www.'): host=host[4:]
        if host.startswith('old.'): host=host[4:]
        path=p.path.rstrip('/') or '/'
        return urlunsplit(('https',host,path,'',''))
    except Exception:
        return (url or '').strip()


def main():
    with PATH.open(encoding='utf-8-sig',newline='') as f:
        reader=csv.DictReader(f)
        fields=list(reader.fieldnames or [])
        total=0; reddit_rows=0; n2n_rows=0
        reddit_urls=set(); n2n_urls=set(); source_values=Counter()
        explicit_url_fields=[x for x in fields if 'url' in x.lower() or 'link' in x.lower()]
        source_fields=[x for x in fields if any(k in x.lower() for k in ('source','subreddit','community','type'))]
        for row in reader:
            total+=1
            source=(row.get('source') or '').strip()
            url=canonical_url(row.get('url') or '')
            parts=urlsplit(url) if url else None
            if source.lower()=='reddit' and parts and parts.netloc=='reddit.com':
                reddit_rows+=1
                reddit_urls.add(url)
                if N2N_PREFIX in parts.path.lower():
                    n2n_rows+=1
                    n2n_urls.add(url)
            for k in source_fields:
                v=(row.get(k) or '').strip()
                if v: source_values[(k,v)]+=1
    out={
        'audit':'AKASHICNET_MASTER_INDEX_AUDIT','version':'0.40',
        'count_basis':'explicit tracked source + url columns; canonical URL strips host variants, query, fragment and trailing slash',
        'columns':fields,'explicit_url_fields':explicit_url_fields,'source_like_fields':source_fields,
        'total_rows':total,'reddit_rows':reddit_rows,'unique_reddit_urls':len(reddit_urls),
        'n2n_rows':n2n_rows,'unique_n2n_urls':len(n2n_urls),
        'n2n_expansion_over_1000':len(n2n_urls)>1000,
        'top_source_values':[{'field':k[0],'value':k[1],'count':v} for k,v in source_values.most_common(12)],
        'content_mode':'metadata_and_links_only','drive_body_reads':0,'embeddings_created':0,
        'truth_inference_allowed':False,'rights_promotion_allowed':False,'scientific_evidence_promotion_allowed':False,
    }
    print(json.dumps(out,ensure_ascii=False,sort_keys=True))

if __name__=='__main__': main()
