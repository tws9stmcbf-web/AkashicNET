#!/usr/bin/env python3
from __future__ import annotations

import csv,json,re
from collections import Counter
from pathlib import Path

INDEX=Path('data/n2n-expanded-index-v0.40.csv')
CONCEPTS=Path('references/community/concept-seed-v0.20.csv')
OUT=Path('data/expanded-concept-candidates-v0.42.json')

ALIASES={
 'CONCEPT-0001':{'consciousness','conscious','awareness'},
 'CONCEPT-0002':{'selfhood','self','ego'},
 'CONCEPT-0003':{'non-duality','nonduality','non-dual','nondual'},
 'CONCEPT-0004':{'psychedelic','psychedelics','psilocybin','lsd','dmt','ayahuasca','ibogaine'},
 'CONCEPT-0005':{'buddhism','buddhist','buddha','dharma'},
 'CONCEPT-0006':{'hinduism','hindu','vedanta','upanishad','ramayana'},
 'CONCEPT-0007':{'shamanism','shamanic','shaman'},
 'CONCEPT-0008':{'alchemy','alchemical','alchemist'},
 'CONCEPT-0009':{'mysticism','mystical','mystic'},
 'CONCEPT-0010':{'meditation','contemplative','contemplation','mindfulness'},
 'CONCEPT-0011':{'hermeticism','hermetic'},
 'CONCEPT-0012':{'qabbalah','kabbalah','cabala','quabbalah','qabalistic','kabbalistic'},
 'CONCEPT-0013':{'ceremonial magic','ritual magic'},
 'CONCEPT-0014':{'esotericism','esoteric','occult'},
 'CONCEPT-0015':{'theosophy','theosophical'},
}
BROAD={'CONCEPT-0001','CONCEPT-0002'}


def matched(text:str,terms:set[str])->list[str]:
    t=(text or '').lower()
    return sorted(x for x in terms if re.search(r'(?<![a-z0-9])'+re.escape(x)+r'(?![a-z0-9])',t))


def main():
    concepts={r['concept_id']:r for r in csv.DictReader(CONCEPTS.open(encoding='utf-8',newline=''))}
    rows=list(csv.DictReader(INDEX.open(encoding='utf-8',newline='')))
    candidates=[]; by_concept=Counter(); basis_counts=Counter()
    for row in rows:
        title=row.get('title',''); topics=row.get('topics','')
        for cid,terms in ALIASES.items():
            mt=matched(title,terms); mp=matched(topics,terms)
            if not mt and not mp: continue
            if mt and cid in BROAD:
                basis='BROAD_TITLE_MATCH'
            elif mt:
                basis='HIGH_PRECISION_TITLE_MATCH'
            else:
                basis='TOPICS_METADATA_MATCH'
            candidates.append({
                'candidate_id':f"EXP042:{row['community_id']}:{cid}",
                'source_ref':row['community_id'],'canonical_url':row['canonical_url'],
                'source_title':title,'target_concept':cid,'concept_label':concepts[cid]['label'],
                'matched_title_terms':mt,'matched_topic_terms':mp,
                'basis':basis,'decision':'HOLD','review_state':'HOLD',
                'accepted_edge':False,
                'reason':'Expanded-corpus alias match is candidate discovery only; review required before topical ABOUT acceptance.',
                'not_truth_claim':True,'not_scientific_evidence_claim':True,'rights_promotion_allowed':False,
            })
            by_concept[cid]+=1; basis_counts[basis]+=1
    out={
        'version':'0.42','scope':'expanded-community-concept-candidate-discovery-only',
        'community_records_examined':len(rows),'concept_count':len(concepts),
        'candidate_count':len(candidates),'decision_counts':{'ACCEPT':0,'HOLD':len(candidates),'REJECT':0},
        'basis_counts':dict(sorted(basis_counts.items())),
        'candidate_counts_by_concept':{cid:{'label':concepts[cid]['label'],'count':by_concept[cid]} for cid in sorted(concepts)},
        'automatic_acceptance_allowed':False,'truth_inference_allowed':False,
        'scientific_evidence_promotion_allowed':False,'rights_promotion_allowed':False,
        'embeddings_created':0,'reddit_body_hydration':False,
        'candidates':candidates,
    }
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in out.items() if k!='candidates'},sort_keys=True))

if __name__=='__main__': main()
