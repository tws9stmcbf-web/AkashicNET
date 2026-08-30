#!/usr/bin/env python3
from __future__ import annotations

import csv,json,re
from pathlib import Path

BASE=Path('data/knowledge-graph-v0.5.json')
INDEX=Path('data/n2n-expanded-index-v0.40.csv')
OUT=Path('data/knowledge-graph-v0.41.json')
EXPECTED=9340


def post_id(url:str)->str|None:
    m=re.search(r'/comments/([a-z0-9]+)/',url or '',re.I)
    return m.group(1).lower() if m else None


def main():
    graph=json.loads(BASE.read_text(encoding='utf-8'))
    with INDEX.open(encoding='utf-8',newline='') as f:
        rows=list(csv.DictReader(f))
    assert len(rows)==EXPECTED, f'expected {EXPECTED} expanded N2N records, got {len(rows)}'
    urls=[r['canonical_url'] for r in rows]
    ids=[r['community_id'] for r in rows]
    assert len(set(urls))==EXPECTED and len(set(ids))==EXPECTED

    node_ids={n['node_id'] for n in graph['nodes']}
    added=[]
    for r in rows:
        nid='community:'+r['community_id']
        assert nid not in node_ids, nid
        node_ids.add(nid)
        added.append({
            'node_id':nid,
            'node_type':'community_post',
            'source_domain':'reddit',
            'community':'r/NeuronsToNirvana',
            'reddit_post_id':post_id(r['canonical_url']),
            'canonical_url':r['canonical_url'],
            'label':r['title'],
            'author':r['author'],
            'topics':r['topics'],
            'source_type':r['source_type'],
            'source_record_count':int(r['source_row_count']),
            'source_record_ids':r['source_record_ids'].split('|') if r['source_record_ids'] else [],
            'source_licence_status':r['licence_status'],
            'source_reuse_decision':r['reuse_decision'],
            'source_provenance_status':r['provenance_status'],
            'rights_status':'UNKNOWN_UNVERIFIED',
            'review_state':'unreviewed',
            'semantic_status':'UNADJUDICATED',
            'not_scientific_evidence_by_default':True,
            'topics_are_navigation_not_validation':True,
        })

    graph['nodes'].extend(added)
    all_ids={n['node_id'] for n in graph['nodes']}
    orphan=[e for e in graph['edges'] if e['source'] not in all_ids or e['target'] not in all_ids]
    graph['schema_version']='0.41'
    graph['expanded_community']={
        'source_index_version':'0.40',
        'community':'r/NeuronsToNirvana',
        'canonical_records':len(added),
        'historical_curated_pilot_records':1000,
        'historical_pilot_preserved':True,
        'review_state':'unreviewed',
        'automatic_cross_source_identity_links':0,
        'automatic_semantic_edges':0,
        'archive_mode':'metadata_and_links_only',
        'reddit_body_hydration':False,
        'embeddings_created':0,
        'scientific_evidence_default':False,
        'truth_inference_allowed':False,
        'rights_promotion_allowed':False,
        'integrity_pass':len(added)==EXPECTED and not orphan,
    }
    graph['policy']['reddit_is_canonical_source']=True
    graph['policy']['reddit_body_hydration']=False
    graph['policy']['cross_source_links_are_not_truth_claims']=True
    graph['policy']['expanded_community_review_required_before_semantic_acceptance']=True
    graph['integrity']['release_integrity_pass']=bool(graph['integrity'].get('release_integrity_pass')) and graph['expanded_community']['integrity_pass']
    OUT.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(graph['expanded_community'],sort_keys=True))
    raise SystemExit(0 if graph['integrity']['release_integrity_pass'] else 2)

if __name__=='__main__': main()
