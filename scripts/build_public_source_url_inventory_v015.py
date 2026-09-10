#!/usr/bin/env python3
from __future__ import annotations

import argparse, hashlib, json, re, subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references/community/public-source-url-inventory-v0.15.json"
SHARD_DIR = ROOT / "references/community/source-url-inventory-v0.15"
URL_RE = re.compile(r"https?://[^\s<>'\"\x60\\]+")
SHARDS = "0123456789abcdef"

def canonical(data): return json.dumps(data, indent=2, ensure_ascii=False) + "\n"
def git_blob_sha(text):
    raw=text.encode(); return hashlib.sha1(f"blob {len(raw)}\0".encode()+raw).hexdigest()
def git_head():
    try: value=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True,stderr=subprocess.DEVNULL).strip()
    except (OSError,subprocess.CalledProcessError): return None
    return value if re.fullmatch(r"[0-9a-f]{40}",value) else None
def clean(value): return value.split(",",1)[0].rstrip(".,;:!?)]}\\")
def normalize(url):
    p=urlsplit(url); scheme=p.scheme.lower(); host=(p.hostname or "").lower(); port=p.port
    netloc=host if not port or (scheme,port) in {("http",80),("https",443)} else f"{host}:{port}"
    path=p.path or "/"
    if path!="/": path=path.rstrip("/")
    return urlunsplit((scheme,netloc,path,p.query,""))
def external(url,scope):
    host=(urlsplit(url).hostname or "").lower()
    return host not in set(scope["first_party_hosts"]) and not any(url.startswith(x) for x in scope["internal_github_prefixes"])
def source_role(url,scope):
    host=(urlsplit(url).hostname or "").lower()
    if url in set(scope.get("derivative_endpoint_urls", [])): return "DERIVATIVE_ACCESS_ENDPOINT"
    if host in set(scope.get("deployment_alias_hosts", [])): return "DEPLOYMENT_ALIAS"
    return None
def files(scope):
    suffixes=set(scope["included_suffixes"]); excluded=set(scope["excluded_paths"]); prefixes=tuple(scope.get("excluded_path_prefixes",[]))
    for root_name in scope["include_roots"]:
        root=ROOT/root_name
        if not root.exists(): continue
        for path in sorted(p for p in root.rglob("*") if p.is_file()):
            rel=path.relative_to(ROOT).as_posix()
            if rel not in excluded and not rel.startswith(prefixes) and path.suffix.lower() in suffixes: yield path,rel
def prior():
    out={}
    for path in sorted(SHARD_DIR.glob("shard-*.json")):
        for entry in json.loads(path.read_text()).get("entries",[]): out[entry["source_id"]]=entry
    return out
def build_entries(scope):
    grouped={}
    for path,rel in files(scope):
        for line_no,line in enumerate(path.read_text(encoding="utf-8",errors="replace").splitlines(),1):
            for match in URL_RE.finditer(line):
                original=clean(match.group(0))
                if not external(original,scope): continue
                normalized=normalize(original); sid="URL-"+hashlib.sha256(normalized.encode()).hexdigest()[:16]
                item=grouped.setdefault(normalized,{"source_id":sid,"normalized_url":normalized,"host":(urlsplit(normalized).hostname or "").lower(),"original_urls":set(),"occurrences":defaultdict(list)})
                item["original_urls"].add(original); item["occurrences"][rel].append(line_no)
    old=prior(); result=[]
    for item in grouped.values():
        previous=old.get(item["source_id"],{})
        occurrences=[{"repository_path":p,"lines":lines} for p,lines in sorted(item["occurrences"].items())]
        entry={"source_id":item["source_id"],"normalized_url":item["normalized_url"],"host":item["host"],"original_urls":sorted(item["original_urls"]),"occurrence_count":sum(len(x["lines"]) for x in occurrences),"occurrences":occurrences,"retrieval_status":previous.get("retrieval_status","UNASSESSED"),"retrieved_on":previous.get("retrieved_on"),"redirect_target":previous.get("redirect_target"),"observed_title":previous.get("observed_title"),"retraction_status":previous.get("retraction_status","UNCHECKED"),"truth_status_changed":False,"repair_candidate":previous.get("repair_candidate")}
        role=previous.get("source_role") or source_role(item["normalized_url"],scope)
        if role: entry["source_role"]=role
        result.append(entry)
    return sorted(result,key=lambda x:x["source_id"])
def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--check",action="store_true"); args=parser.parse_args()
    manifest=json.loads(MANIFEST.read_text()); entries=build_entries(manifest["scope"])
    source_commit=manifest["source_commit"] if args.check else git_head()
    groups={k:[] for k in SHARDS}
    for entry in entries: groups[entry["source_id"][4]].append(entry)
    metadata=[]
    for key in SHARDS:
        rows=groups[key]; data={"inventory_version":"0.1.0","target_release":"0.15.0","source_commit":source_commit,"shard":key,"entry_count":len(rows),"occurrence_count":sum(x["occurrence_count"] for x in rows),"entries":rows}
        rendered=canonical(data); path=SHARD_DIR/f"shard-{key}.json"
        metadata.append({"content_sha":git_blob_sha(rendered),"entry_count":data["entry_count"],"occurrence_count":data["occurrence_count"],"path":path.relative_to(ROOT).as_posix(),"shard":key})
        if args.check:
            if not path.exists() or path.read_text()!=rendered: raise SystemExit(f"FAIL: stale inventory shard {key}")
        else: path.parent.mkdir(parents=True,exist_ok=True); path.write_text(rendered)
    assessed={x["source_id"] for x in entries if x["retrieval_status"]!="UNASSESSED"}
    manifest.update({"state":"ASSESSED" if len(assessed)==len(entries) else "GENERATED_UNASSESSED","generated_at":manifest["generated_at"] if args.check else date.today().isoformat(),"source_commit":source_commit,"summary":{"external_url_occurrences":sum(x["occurrence_count"] for x in entries),"unique_normalized_external_urls":len(entries),"assessed_unique_urls":len(assessed),"unassessed_unique_urls":len(entries)-len(assessed),"shard_count":16},"shards":metadata})
    manifest.pop("entries",None); rendered_manifest=canonical(manifest)
    if args.check:
        if MANIFEST.read_text()!=rendered_manifest: raise SystemExit("FAIL: stale inventory manifest")
        print("PASS: sharded public source URL inventory is deterministic and current")
    else: MANIFEST.write_text(rendered_manifest); print(f"GENERATED: {len(entries)} unique URLs across 16 shards; {len(entries)-len(assessed)} UNASSESSED")
    return 0
if __name__=="__main__": raise SystemExit(main())
