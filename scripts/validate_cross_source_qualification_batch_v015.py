#!/usr/bin/env python3
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"references/community/cross-source-qualification-batch-v0.1.5.json"
TYPES={"TOPIC","PUBLICATION","FRAMEWORK","QUESTION","SOURCE_RECORD","EVIDENCE_RECORD"}
FALSE={"automated_truth_inference_allowed","automated_acceptance_allowed","rights_promotion_allowed","scientific_evidence_promotion_allowed","canonical_identity_promotion_allowed","circular_confidence_allowed","private_drive_metadata_allowed"}
DIRECT={"EXPLICIT_IDENTIFIER","EXACT_FULL_TITLE","EXPLICIT_CITATION"}
CORR={"DISTINCTIVE_NAMED_ENTITY","DISTINCTIVE_MULTI_TOKEN_PHRASE","EXPLICIT_FRAMEWORK_REFERENCE","EXPLICIT_QUESTION_REFERENCE"}
def qualifies(a):
 u=[x for x in a if not x.get("graph_derived") and not x.get("representation_only")]
 return any(x.get("type") in DIRECT for x in u) or len({(x.get("type"),x.get("normalized_value")) for x in u if x.get("type") in CORR and x.get("normalized_value")})>=2
def validate(d):
 e=[]
 if (d.get("schema_version"),d.get("policy_version"),d.get("endpoint_registry_version"))!=("0.1.5","0.1.2","0.1.4"): e.append("version mismatch")
 if d.get("defaults")!={"assertion_class":"INFERRED_CANDIDATE","review_state":"REVIEW_REQUIRED","accepted_edge":False}: e.append("unsafe defaults")
 if set(d.get("boundaries",{}))!=FALSE or any(d.get("boundaries",{}).values()): e.append("unsafe boundaries")
 q=d.get("qualified_candidates",[]); r=d.get("rejected_candidates",[]); allc=q+r
 for c in allc:
  for n in ("source_endpoint","target_endpoint"):
   x=c.get(n,{})
   if x.get("endpoint_type") not in TYPES or not str(x.get("endpoint_id","")).startswith("endpoint:"): e.append("invalid endpoint")
   p=x.get("provenance",{})
   if set(p)!={"artifact_id","record_id","independence_key","public_safe"} or p.get("public_safe") is not True: e.append("invalid provenance")
 if any(not qualifies(x.get("anchors",[])) for x in q): e.append("unqualified candidate")
 if any(qualifies(x.get("anchors",[])) or x.get("decision")!="REJECTED_QUALIFICATION" for x in r): e.append("invalid rejection")
 ids=[x.get("candidate_id") for x in allc]
 if None in ids or len(ids)!=len(set(ids)): e.append("candidate IDs")
 if d.get("summary")!={"screened":len(allc),"qualified":len(q),"rejected":len(r),"accepted_edges":0}: e.append("summary mismatch")
 if d.get("rejection_is_not_negative_evidence") is not True: e.append("disclaimer missing")
 s=json.dumps(d)
 if any(k in s for k in ('"drive_id"','"filename"','"private_path"','/My Drive/')): e.append("private metadata")
 return sorted(set(e))
def main():
 d=json.loads(REPORT.read_text()); e=validate(d); print(json.dumps(d["summary"],sort_keys=True))
 for x in e: print("ERROR:",x)
 if not e: print("AKASHICNET TYPED CROSS-SOURCE BATCH v0.1.5 PASS")
 return bool(e)
if __name__=="__main__": raise SystemExit(main())
