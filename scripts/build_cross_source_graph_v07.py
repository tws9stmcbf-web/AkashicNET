#!/usr/bin/env python3
"""Overlay the curated N2N pilot index onto AkashicNET knowledge graph v0.5.

Policy:
- Reddit remains the canonical source of record.
- Only curated metadata already present in n2n-pilot-index.csv is imported.
- No Reddit post bodies, comments, images, or media are fetched.
- Source domains remain explicit.
- Cross-source work links are created only when a canonical work/family label is
  explicitly present in curated Reddit metadata after conservative normalisation.
"""
from __future__ import annotations
import csv, json, re
from pathlib import Path
from urllib.parse import urlparse

BASE=Path('data/knowledge-graph-v0.5.json')
N2N=Path('references/community/n2n-pilot-index.csv')
OUT=Path('data/knowledge-graph-v0.7.json')
EXPECTED_REDDIT=1000


def norm(s:str)->str:
    return re.sub(r'[^a-z0-9]+',' ',(s or '').lower()).strip()


def reddit_id(url:str)->str:
    m=re.search(r'/comments/([a-z0-9]+)/',url or '',re.I)
    return m.group(1).lower() if m else ''

with BASE.open(encoding='utf-8') as f:
    graph=json.load(f)
with N2N.open(encoding='utf-8-sig',newline='') as f:
    rows=list(csv.DictReader(f))

assert len(rows)==EXPECTED_REDDIT, f'expected {EXPECTED_REDDIT} N2N records, got {len(rows)}'
urls=[r['reddit_url'].strip() for r in rows]
assert len(urls)==len(set(urls)), 'duplicate reddit_url in N2N pilot'

nodes=graph['nodes']
edges=graph['edges']
node_ids={n['node_id'] for n in nodes}

canonical=[n for n in nodes if n.get('node_type')=='canonical_candidate_family']
source_nodes={}
reddit_nodes=0
cross_links=0

for r in rows:
    url=r['reddit_url'].strip()
    rid=reddit_id(url) or norm(url).replace(' ','_')
    nid=f'reddit:{rid}'
    assert nid not in node_ids, f'duplicate graph node id {nid}'
    node_ids.add(nid)
    nodes.append({
        'node_id':nid,
        'node_type':'reddit_post',
        'source_domain':'reddit',
        'reddit_post_id':reddit_id(url) or None,
        'canonical_url':url,
        'label':r.get('title',''),
        'author':r.get('author',''),
        'date':r.get('date',''),
        'source_type':r.get('source_type',''),
        'category':r.get('category',''),
        'short_summary':r.get('short_summary',''),
        'toolkit_framework':r.get('toolkit_framework',''),
        'research_question_potential':r.get('research_question_potential',''),
        'evidence_status':r.get('evidence_status',''),
        'provenance_status':r.get('provenance_status',''),
        'rights_status':'LINK_ONLY_METADATA',
        'review_state':'accepted',
        'not_scientific_evidence_by_default':True,
    })
    reddit_nodes+=1

    ext=(r.get('external_source_url') or '').strip()
    if ext and ext!=url:
        sid='external:'+re.sub(r'[^a-zA-Z0-9]+','_',ext).strip('_')[:180]
        if sid not in source_nodes:
            source_nodes[sid]={
                'node_id':sid,
                'node_type':'external_source',
                'source_domain':urlparse(ext).netloc.lower(),
                'canonical_url':ext,
                'label':ext,
                'rights_status':'UNKNOWN_UNVERIFIED',
                'review_state':'provisional',
            }
        edges.append({
            'edge_id':f'reddit_external:{rid}:{sid}',
            'source':nid,
            'target':sid,
            'relationship':'LINKS_TO_EXTERNAL_SOURCE',
            'confidence':'high',
            'basis':'curated_external_source_url',
            'review_state':'accepted',
        })

    hay=norm(' '.join([r.get('title',''),r.get('short_summary','')]))
    for c in canonical:
        label=norm(c.get('label',''))
        # Conservative explicit mention gate; avoid short/ambiguous labels.
        if len(label)>=12 and label in hay:
            edges.append({
                'edge_id':f'cross_source:{rid}:{c["family_id"]}',
                'source':nid,
                'target':c['node_id'],
                'relationship':'CURATED_METADATA_MENTIONS_CANONICAL_FAMILY',
                'confidence':'medium',
                'basis':'explicit_normalised_label_mention_in_curated_title_or_summary',
                'review_state':'provisional',
                'not_truth_claim':True,
            })
            cross_links+=1

nodes.extend(source_nodes.values())
all_ids={n['node_id'] for n in nodes}
orphan=[e for e in edges if e['source'] not in all_ids or e['target'] not in all_ids]

graph['schema_version']='0.7'
graph['cross_source']={
    'reddit_records':reddit_nodes,
    'external_source_nodes':len(source_nodes),
    'explicit_canonical_cross_links':cross_links,
    'reddit_canonical_source':'Reddit',
    'archive_mode':'metadata_and_links_only',
    'scientific_evidence_default':False,
    'cross_link_policy':'explicit canonical label mention in curated title/summary only; provisional until reviewed',
    'integrity_pass':reddit_nodes==EXPECTED_REDDIT and not orphan,
}
graph['policy']['reddit_is_canonical_source']=True
graph['policy']['reddit_body_hydration']=False
graph['policy']['cross_source_links_are_not_truth_claims']=True
graph['integrity']['release_integrity_pass']=bool(graph['integrity'].get('release_integrity_pass')) and graph['cross_source']['integrity_pass']
OUT.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(graph['cross_source'],sort_keys=True))
raise SystemExit(0 if graph['integrity']['release_integrity_pass'] else 2)
