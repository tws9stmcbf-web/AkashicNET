#!/usr/bin/env python3
"""Complete conservative collection-level provenance for canonical candidates.

v0.13 policy:
- Use only collection paths explicitly recorded in drive-canonicalisation-candidates.csv.
- Resolve only exact collection_path matches against the reconciled 195-folder graph.
- Do not imply document/manifestation identity from a collection-level link.
- Preserve Stage-B provenance edges unchanged.
- Do not alter rights, truth, or scientific-evidence status.
"""
from __future__ import annotations
import csv,json
from pathlib import Path

BASE=Path('data/knowledge-graph-v0.7.json')
CANDIDATES=Path('references/community/drive-canonicalisation-candidates.csv')
OUT=Path('data/knowledge-graph-v0.13.json')
EXPECTED_DRIVE_NODES=195
EXPECTED_CANDIDATES=29


def main():
    graph=json.load(BASE.open(encoding='utf-8'))
    rows=list(csv.DictReader(CANDIDATES.open(encoding='utf-8-sig',newline='')))
    assert len(rows)==EXPECTED_CANDIDATES

    drive_by_path={
        n.get('collection_path'):n for n in graph['nodes']
        if n.get('node_type')=='drive_object' and n.get('collection_path')
    }
    assert len(drive_by_path)==EXPECTED_DRIVE_NODES

    candidate_nodes={
        n.get('family_id'):n for n in graph['nodes']
        if n.get('node_type')=='canonical_candidate_family' and n.get('family_id')
    }

    existing={(e.get('source'),e.get('target'),e.get('relationship')) for e in graph['edges']}
    added=[]
    family_status=[]
    unresolved=[]

    for r in rows:
        fid=r['family_id']
        cnode=candidate_nodes.get(fid)
        declared=[p.strip() for p in (r.get('collections') or '').split(';') if p.strip()]
        matched=[]
        missing=[]
        if not cnode:
            unresolved.append({'family_id':fid,'reason':'canonical_candidate_node_missing','declared_collections':declared})
            family_status.append({'family_id':fid,'status':'HOLD','matched_collection_paths':[],'missing_collection_paths':declared})
            continue
        for path in declared:
            drive=drive_by_path.get(path)
            if not drive:
                missing.append(path)
                continue
            key=(cnode['node_id'],drive['node_id'],'PROVENANCE_RECORDED_IN_COLLECTION')
            if key not in existing:
                edge={
                    'edge_id':f'v013_collection_provenance:{fid}:{drive["drive_id"]}',
                    'source':cnode['node_id'],
                    'target':drive['node_id'],
                    'relationship':'PROVENANCE_RECORDED_IN_COLLECTION',
                    'confidence':'high',
                    'basis':'exact collection_path match from reviewed canonicalisation candidate ledger',
                    'review_state':'accepted' if r.get('status')=='REVIEWED' else 'provisional',
                    'provenance_level':'collection_only',
                    'not_document_identity':True,
                    'not_truth_claim':True,
                    'rights_promotion_allowed':False,
                }
                graph['edges'].append(edge); added.append(edge); existing.add(key)
            matched.append(path)
        status='RESOLVED_COLLECTION_PROVENANCE' if matched and not missing else 'PARTIAL_COLLECTION_PROVENANCE' if matched else 'HOLD'
        family_status.append({'family_id':fid,'status':status,'matched_collection_paths':matched,'missing_collection_paths':missing})
        if missing or not matched:
            unresolved.append({'family_id':fid,'reason':'one_or_more_declared_collection_paths_unmatched','declared_collections':declared,'matched':matched,'missing':missing})

    node_ids={n['node_id'] for n in graph['nodes']}
    orphan=[e for e in graph['edges'] if e['source'] not in node_ids or e['target'] not in node_ids]
    fully=sum(1 for x in family_status if x['status']=='RESOLVED_COLLECTION_PROVENANCE')
    partial=sum(1 for x in family_status if x['status']=='PARTIAL_COLLECTION_PROVENANCE')
    holds=sum(1 for x in family_status if x['status']=='HOLD')

    graph['schema_version']='0.13'
    graph['provenance_completion_v013']={
        'candidate_families_examined':len(rows),
        'exact_collection_edges_added':len(added),
        'fully_resolved_collection_provenance':fully,
        'partial_collection_provenance':partial,
        'holds':holds,
        'family_status':family_status,
        'unresolved':unresolved,
        'policy':'exact reviewed-ledger collection_path match only; collection provenance is not document identity',
        'truth_inference_allowed':False,
        'rights_promotion_allowed':False,
        'scientific_evidence_promotion_allowed':False,
        'integrity_pass':len(drive_by_path)==EXPECTED_DRIVE_NODES and len(rows)==EXPECTED_CANDIDATES and not orphan,
    }
    graph['integrity']['v013_provenance_integrity_pass']=graph['provenance_completion_v013']['integrity_pass']
    graph['integrity']['release_integrity_pass']=bool(graph['integrity'].get('release_integrity_pass')) and graph['provenance_completion_v013']['integrity_pass']
    OUT.write_text(json.dumps(graph,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in graph['provenance_completion_v013'].items() if k not in {'family_status','unresolved'}},sort_keys=True))
    print(json.dumps({'unresolved':unresolved},sort_keys=True))
    raise SystemExit(0 if graph['integrity']['release_integrity_pass'] else 2)

if __name__=='__main__': main()
