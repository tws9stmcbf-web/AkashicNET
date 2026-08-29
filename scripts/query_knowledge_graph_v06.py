#!/usr/bin/env python3
"""Provenance-aware retrieval over AkashicNET knowledge graph v0.5.

This is a controlled metadata-only retrieval layer. It does not hydrate document
bodies, infer truth, or change rights states. Results expose their graph node,
review state, relationship disposition, confidence score, and source evidence.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

GRAPH=Path('data/knowledge-graph-v0.5.json')


def norm(text: str) -> str:
    return re.sub(r'[^a-z0-9]+',' ',(text or '').lower()).strip()


def searchable_text(node: dict) -> str:
    parts=[
        node.get('node_id',''), node.get('label',''), node.get('family_id',''),
        node.get('collection_path',''), node.get('parent_root',''),
        node.get('authoritative_disposition',''), node.get('stage_b_disposition',''),
        node.get('basis',''), node.get('notes',''), node.get('reconciled_status',''),
    ]
    return norm(' '.join(str(x) for x in parts if x is not None))


def provenance_path(node: dict) -> list[dict]:
    path=[]
    if node.get('node_type')=='canonical_candidate_family':
        ep=node.get('evidence_provenance',{})
        path.append({'kind':'canonical_family','id':node.get('family_id'),'label':node.get('label')})
        path.append({'kind':'reconciliation_status','value':node.get('reconciled_status')})
        path.append({'kind':'relationship_disposition','value':node.get('authoritative_disposition')})
        path.append({'kind':'evidence_basis','value':ep.get('basis') or node.get('basis')})
        path.append({'kind':'source_ledger','value':ep.get('source_ledger')})
    elif node.get('node_type')=='drive_object':
        path.append({'kind':'drive_object','id':node.get('drive_id'),'label':node.get('label')})
        path.append({'kind':'collection_path','value':node.get('collection_path')})
        path.append({'kind':'parent_root','value':node.get('parent_root')})
        obs=node.get('provenance_observations') or []
        for o in obs:
            path.append({'kind':'census_observation','source_file':o.get('source_file'),'count_status':o.get('count_status')})
    elif node.get('node_type')=='canonical_family':
        path.append({'kind':'stage_b_family','id':node.get('family_id'),'label':node.get('label')})
        path.append({'kind':'relationship_disposition','value':node.get('stage_b_disposition')})
        path.append({'kind':'provenance','value':node.get('provenance')})
    else:
        path.append({'kind':node.get('node_type','node'),'id':node.get('node_id'),'label':node.get('label')})
    return path


def result_record(node: dict, rank: int) -> dict:
    ep=node.get('evidence_provenance',{})
    return {
        'rank':rank,
        'node_id':node.get('node_id'),
        'node_type':node.get('node_type'),
        'label':node.get('label'),
        'family_id':node.get('family_id'),
        'relationship':node.get('authoritative_disposition') or node.get('stage_b_disposition'),
        'review_state':node.get('review_state'),
        'reconciled_status':node.get('reconciled_status'),
        'confidence':node.get('confidence'),
        'evidence_score':ep.get('score'),
        'evidence_tier':ep.get('tier'),
        'score_scope':ep.get('scope'),
        'rights_status':node.get('rights_status'),
        'provenance_path':provenance_path(node),
        'not_truth_claim':True,
        'not_rights_clearance':node.get('rights_status')!='PUBLIC_VERIFIED',
    }


def query(graph: dict, text: str, limit: int=10, node_type: str|None=None) -> dict:
    terms=[t for t in norm(text).split() if t]
    scored=[]
    for node in graph.get('nodes',[]):
        if node_type and node.get('node_type')!=node_type:
            continue
        hay=searchable_text(node)
        if not terms:
            score=0
        else:
            hits=sum(1 for t in terms if t in hay)
            if hits==0:
                continue
            score=hits/len(terms)
            if norm(node.get('label',''))==norm(text): score+=1.0
            if norm(node.get('family_id',''))==norm(text): score+=1.0
        scored.append((score,node))
    scored.sort(key=lambda x:(-x[0],-(x[1].get('evidence_provenance',{}).get('score') or -1),x[1].get('label','')))
    results=[result_record(n,i+1) for i,(_,n) in enumerate(scored[:limit])]
    return {
        'query':text,
        'result_count':len(results),
        'retrieval_scope':'metadata_graph_only',
        'truth_inference_allowed':False,
        'rights_promotion_allowed':False,
        'results':results,
    }


def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument('query')
    p.add_argument('--graph',default=str(GRAPH))
    p.add_argument('--limit',type=int,default=10)
    p.add_argument('--node-type')
    args=p.parse_args()
    graph=json.load(open(args.graph,encoding='utf-8'))
    out=query(graph,args.query,args.limit,args.node_type)
    print(json.dumps(out,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
