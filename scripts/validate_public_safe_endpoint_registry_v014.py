#!/usr/bin/env python3
"""Fail-closed validator for typed public-safe endpoint registry v0.1.4."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/"references/community/public-safe-endpoint-registry-fixture-v0.1.4.json"
TYPES={"TOPIC","PUBLICATION","FRAMEWORK","QUESTION","SOURCE_RECORD","EVIDENCE_RECORD"}
FALSE={"automated_truth_inference_allowed","automated_acceptance_allowed","canonical_identity_promotion_allowed","circular_confidence_allowed","private_drive_metadata_allowed"}
FORBIDDEN_KEYS={"drive_id","drive_object_id","file_id","filename","path","parent_path","private_path","object_hash"}
def walk(v):
    if isinstance(v,dict):
        for k,x in v.items(): yield k,x; yield from walk(x)
    elif isinstance(v,list):
        for x in v: yield from walk(x)
def validate(d):
    e=[]
    if d.get("schema_version")!="0.1.4": e.append("schema version")
    p=d.get("policy",{})
    if set(p)!=FALSE or any(p.values()): e.append("policy boundaries must exist and remain false")
    xs=d.get("endpoints",[])
    if {x.get("endpoint_type") for x in xs}!=TYPES: e.append("all six endpoint types required")
    ids=[x.get("endpoint_id") for x in xs]
    if len(ids)!=len(set(ids)) or any(not isinstance(x,str) or not re.fullmatch(r"endpoint:[a-z0-9][a-z0-9:-]+",x) for x in ids): e.append("stable unique endpoint IDs required")
    for x in xs:
        if x.get("assertion_class") not in {"ASSERTED_SOURCE_METADATA","CURATED_PUBLIC_LABEL","SYNTHETIC_FIXTURE"}: e.append("invalid assertion class")
        if x.get("evidence_status") not in {"NOT_APPLICABLE","UNASSESSED","SOURCE_CLASSIFICATION_ONLY"}: e.append("invalid evidence status")
        if x.get("identity_state") not in {"DISTINCT","UNRESOLVED"}: e.append("invalid identity state")
        q=x.get("provenance",{})
        if set(q)!={"artifact_id","record_id","independence_key","public_safe"} or q.get("public_safe") is not True or not all(q.get(k) for k in ("artifact_id","record_id","independence_key")): e.append("invalid provenance")
    if d.get("edges")!=[]: e.append("endpoint registry cannot contain edges")
    for k,v in walk(d):
        if str(k).lower() in FORBIDDEN_KEYS or isinstance(v,str) and any(m in v for m in ("/My Drive/","drive.google.com/open?id=","AKM-")): e.append("private Drive metadata prohibited")
    return sorted(set(e))
def main():
    d=json.loads(FIXTURE.read_text()); e=validate(d)
    print(json.dumps({"endpoint_count":len(d.get("endpoints",[])),"endpoint_types":sorted({x.get("endpoint_type") for x in d.get("endpoints",[])}),"edge_count":len(d.get("edges",[]))},sort_keys=True))
    for x in e: print("ERROR:",x)
    if not e: print("AKASHICNET PUBLIC-SAFE ENDPOINT REGISTRY v0.1.4 PASS")
    return bool(e)
if __name__=="__main__": raise SystemExit(main())
