#!/usr/bin/env python3
"""Federated metadata-only retrieval over AkashicNET Drive + N2N graph v0.7."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

GRAPH=Path('data/knowledge-graph-v0.7.json')

def norm(text:str)->str:
    return re.sub(r'[^a-z0-9]+',' ',(text or '').lower()).strip()

def searchable(node:dict)->str:
    fields=['node_id','label','family_id','collection_path','parent_root','authoritative_disposition','stage_b_disposition','basis','notes','reconciled_status','category','short_summary','toolkit_framework','research_question_potential','canonical_url','evidence_status','source_type']
    return norm(' '.join(str(node.get(k,'')) for k in fields))

def query(graph:dict,text:str,limit:int=12)->dict:
    terms=norm(text).split()
    scored=[]
    for n in graph.get('nodes',[]):
        hay=searchable(n)
        hits=sum(1 for t in terms if t in hay)
        if terms and hits==0: continue
        score=(hits/len(terms)) if terms else 0
        if norm(n.get('label',''))==norm(text): score+=1
        if norm(n.get('family_id',''))==norm(text): score+=1
        scored.append((score,n))
    scored.sort(key=lambda x:(-x[0],-(x[1].get('evidence_provenance',{}).get('score') or -1),x[1].get('label','')))
    selected=[n for _,n in scored[:limit]]
    ids={n['node_id'] for n in selected}
    related=[]
    for e in graph.get('edges',[]):
        if e.get('source') in ids or e.get('target') in ids:
            related.append(e)
    by_id={n['node_id']:n for n in graph.get('nodes',[])}
    results=[]
    for rank,n in enumerate(selected,1):
        ep=n.get('evidence_provenance',{})
        links=[]
        for e in related:
            if e.get('source')==n['node_id'] or e.get('target')==n['node_id']:
                other=e['target'] if e['source']==n['node_id'] else e['source']
                o=by_id.get(other,{})
                links.append({
                    'relationship':e.get('relationship'),
                    'direction':'out' if e['source']==n['node_id'] else 'in',
                    'other_node_id':other,
                    'other_node_type':o.get('node_type'),
                    'other_label':o.get('label'),
                    'confidence':e.get('confidence'),
                    'basis':e.get('basis'),
                    'review_state':e.get('review_state'),
                })
        results.append({
            'rank':rank,
            'node_id':n.get('node_id'),
            'node_type':n.get('node_type'),
            'source_domain':n.get('source_domain') or ('drive' if n.get('node_type')=='drive_object' else 'akashicnet'),
            'label':n.get('label'),
            'canonical_url':n.get('canonical_url'),
            'family_id':n.get('family_id'),
            'collection_path':n.get('collection_path'),
            'relationship':n.get('authoritative_disposition') or n.get('stage_b_disposition'),
            'review_state':n.get('review_state'),
            'evidence_status':n.get('evidence_status'),
            'evidence_score':ep.get('score'),
            'evidence_tier':ep.get('tier'),
            'rights_status':n.get('rights_status'),
            'graph_links':links,
            'not_truth_claim':True,
        })
    return {
        'query':text,
        'result_count':len(results),
        'retrieval_scope':'cross_source_metadata_graph_only',
        'source_boundaries_explicit':True,
        'truth_inference_allowed':False,
        'rights_promotion_allowed':False,
        'results':results,
    }

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument('query')
    p.add_argument('--graph',default=str(GRAPH))
    p.add_argument('--limit',type=int,default=12)
    a=p.parse_args()
    g=json.load(open(a.graph,encoding='utf-8'))
    print(json.dumps(query(g,a.query,a.limit),ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
