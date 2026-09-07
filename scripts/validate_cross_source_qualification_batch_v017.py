#!/usr/bin/env python3
"""Fail-closed validator for audited cross-source qualification Batch 4 v0.1.7."""
import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REPORT=ROOT/"references/community/cross-source-qualification-batch-v0.1.7.json"
TYPES={"TOPIC","PUBLICATION","FRAMEWORK","QUESTION","SOURCE_RECORD","EVIDENCE_RECORD"}
FALSE={"automated_truth_inference_allowed","automated_acceptance_allowed","rights_promotion_allowed","scientific_evidence_promotion_allowed","canonical_identity_promotion_allowed","circular_confidence_allowed","private_drive_metadata_allowed"}
OLD={"https://www.reddit.com/r/NeuronsToNirvana/comments/1t4mza9/wisdom_traditions_as_cognitive_maps/","https://www.reddit.com/r/NeuronsToNirvana/comments/1udv3su/visual_symbolism_and_the_sacred/","https://www.reddit.com/r/NeuronsToNirvana/comments/1u6dq0s/hieratic_as_interpretive_scaffolding/"}
ENDPOINT_ID=re.compile(r"endpoint:[a-z0-9][a-z0-9:-]+")
SHA256=re.compile(r"[0-9a-f]{64}")
SOURCE_ARTIFACTS={
 "artifact:reddit-n2n-test-batch-25:2026-09-02":{"sha256":"9e7f1b1036bee1f48e399ba5f9bec0a9b509626602b6ebc09de5eb8b6b7b514c","independence_key":"source:reddit-index:n2n-test-batch-25"},
 "artifact:drive-knowledge-graph-seed:0.1":{"sha256":"2ff59b08c528c92f4161ddb153f990ed56486c2a9cf8c475fe9351cc65e596ab","independence_key":"source:drive-public-seed:stage-b-v0.1"},
}
FORBIDDEN_KEYS={"drive_id","drive_file_id","drive_object_id","file_id","filename","file_name","path","parent_id","parent_path","parents","private_path","object_hash"}
FORBIDDEN_VALUES=("/My Drive/","drive.google.com/open?id=")

def walk(v):
 if isinstance(v,dict):
  for k,x in v.items():
   yield k,x
   yield from walk(x)
 elif isinstance(v,list):
  for x in v: yield from walk(x)

def validate(d):
 e=[]
 if (d.get("schema_version"),d.get("policy_version"),d.get("endpoint_registry_version"),d.get("anchor_evidence_version"))!=("0.1.7","0.1.2","0.1.4","0.1.6"): e.append("version")
 if d.get("defaults")!={"assertion_class":"INFERRED_CANDIDATE","review_state":"REVIEW_REQUIRED","accepted_edge":False}: e.append("defaults")
 if set(d.get("boundaries",{}))!=FALSE or any(d.get("boundaries",{}).values()): e.append("boundaries")
 if d.get("edges",[])!=[]: e.append("accepted edges prohibited")
 sources=d.get("source_artifacts")
 if not isinstance(sources,list) or not sources:
  e.append("source artifacts")
  declared={}
 else:
  declared={}
  for source in sources:
   if not isinstance(source,dict) or set(source)!={"artifact_id","sha256","independence_key","public_safe"}:
    e.append("source artifacts"); continue
   artifact_id=source.get("artifact_id")
   if not all(isinstance(source.get(k),str) and source[k] for k in ("artifact_id","sha256","independence_key")) or source.get("public_safe") is not True:
    e.append("source artifacts"); continue
   if artifact_id in declared: e.append("source artifacts")
   declared[artifact_id]=source
   expected=SOURCE_ARTIFACTS.get(artifact_id)
   if expected is None or source.get("sha256")!=expected["sha256"] or source.get("independence_key")!=expected["independence_key"] or not SHA256.fullmatch(source.get("sha256","")):
    e.append("source artifacts")
 if set(declared)!=set(SOURCE_ARTIFACTS): e.append("source artifacts")
 q=d.get("qualified_candidates",[]); r=d.get("rejected_candidates",[]); allc=q+r
 if q: e.append("unaudited qualification")
 for c in allc:
  if c.get("accepted_edge") is not None: e.append("accepted edges prohibited")
  if c.get("source_endpoint",{}).get("provenance",{}).get("record_id") in OLD: e.append("reused Batch 3 pair")
  for n in ("source_endpoint","target_endpoint"):
   x=c.get(n,{})
   if x.get("endpoint_type") not in TYPES or not isinstance(x.get("endpoint_id"),str) or not ENDPOINT_ID.fullmatch(x["endpoint_id"]): e.append("endpoint")
   p=x.get("provenance",{})
   if set(p)!={"artifact_id","record_id","independence_key","public_safe"} or p.get("public_safe") is not True or not all(isinstance(p.get(k),str) and p[k] for k in ("artifact_id","record_id","independence_key")):
    e.append("provenance")
   else:
    source=declared.get(p["artifact_id"])
    if source is None or p["independence_key"]!=source.get("independence_key"): e.append("provenance")
  if c.get("anchor_evidence")!=[]: e.append("unvalidated anchor")
  if not c.get("observed_nonqualifying_signals"): e.append("signal explanation")
  if c.get("decision")!="REJECTED_QUALIFICATION": e.append("decision")
 ids=[x.get("candidate_id") for x in allc]
 if None in ids or len(ids)!=len(set(ids)): e.append("IDs")
 if d.get("summary")!={"screened":len(allc),"qualified":len(q),"rejected":len(r),"accepted_edges":0}: e.append("summary")
 if d.get("rejection_is_not_negative_evidence") is not True: e.append("disclaimer")
 for k,v in walk(d):
  if str(k).lower() in FORBIDDEN_KEYS or isinstance(v,str) and any(marker in v for marker in FORBIDDEN_VALUES): e.append("private metadata")
 return sorted(set(e))

def main():
 d=json.loads(REPORT.read_text()); e=validate(d); print(json.dumps(d["summary"],sort_keys=True))
 for x in e: print("ERROR:",x)
 if not e: print("AKASHICNET AUDITED CROSS-SOURCE BATCH v0.1.7 PASS")
 return bool(e)
if __name__=="__main__": raise SystemExit(main())
