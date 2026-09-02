#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
READINESS=ROOT/"references/community/provenance-integrity-beta-readiness-v0.14.json"
INVENTORY=ROOT/"references/community/public-source-url-inventory-v0.14.json"
V013=ROOT/"references/community/public-knowledge-beta-release-manifest-v0.13.json"
CRITERIA=[f"V014-C{i}" for i in range(1,11)]
ALLOWED={"PASS","PARTIAL","BLOCKED","PENDING","REVALIDATION_REQUIRED"}
def blob_sha(raw): return hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--require-ready",action="store_true"); args=parser.parse_args()
    readiness=json.loads(READINESS.read_text()); inventory=json.loads(INVENTORY.read_text()); v013=json.loads(V013.read_text())
    assert readiness["target_version"]=="0.14.0-beta.1" and readiness["target_name"]=="Provenance Integrity Beta"
    assert readiness["readiness_policy"]=="exact_commit_fail_closed" and readiness["status"]=="CANDIDATE_BLOCKED" and readiness["v014_declared"] is False
    assert v013["target_version"]=="0.13.0-beta.1" and v013["state"]=="SEALED"
    assert v013["validated_release_commit"]==readiness["immutable_baseline"]["validated_release_commit"] and readiness["immutable_baseline"]["retargetable"] is False
    keys=list(readiness["criteria"]); assert [x.split("_",1)[0] for x in keys]==CRITERIA
    assert all(x in ALLOWED for x in readiness["criteria"].values()) and all(x is False for x in readiness["fixed_invariants"].values())
    guards=inventory["guards"]; assert guards["original_urls_preserved"] is True and guards["unavailability_changes_truth_status"] is False and guards["automatic_source_replacement"] is False and guards["automatic_evidence_promotion"] is False
    entries=[]; occurrences=0; shard_keys=[]
    for meta in inventory["shards"]:
        path=ROOT/meta["path"]; raw=path.read_bytes(); assert blob_sha(raw)==meta["content_sha"]
        shard=json.loads(raw); assert shard["shard"]==meta["shard"] and shard["entry_count"]==meta["entry_count"]==len(shard["entries"])
        assert shard["occurrence_count"]==meta["occurrence_count"]==sum(x["occurrence_count"] for x in shard["entries"])
        shard_keys.append(shard["shard"]); occurrences+=shard["occurrence_count"]; entries.extend(shard["entries"])
    assert shard_keys==list("0123456789abcdef") and inventory["summary"]["shard_count"]==16
    assert inventory["summary"]["external_url_occurrences"]==occurrences and inventory["summary"]["unique_normalized_external_urls"]==len(entries)
    assert len({x["source_id"] for x in entries})==len(entries)
    for entry in entries:
        assert re.fullmatch(r"URL-[0-9a-f]{16}",entry["source_id"]) and entry["normalized_url"].startswith(("http://","https://")) and entry["original_urls"] and entry["truth_status_changed"] is False
    assessed={x["source_id"] for x in entries if x["retrieval_status"]!="UNASSESSED"}
    assert inventory["summary"]["assessed_unique_urls"]==len(assessed) and inventory["summary"]["unassessed_unique_urls"]==len(entries)-len(assessed)
    ready=inventory["state"]=="ASSESSED" and bool(entries) and not inventory["summary"]["unassessed_unique_urls"] and all(x=="PASS" for x in readiness["criteria"].values()) and not readiness["release_blockers"] and readiness["v014_declared"] is True
    if args.require_ready and not ready: raise SystemExit("BLOCKED: v0.14 readiness conditions are not all satisfied")
    print(f"VALID: 16 shards, {len(entries)} unique URLs; release_ready={ready}; blockers={len(readiness['release_blockers'])}")
    return 0
if __name__=="__main__": raise SystemExit(main())
