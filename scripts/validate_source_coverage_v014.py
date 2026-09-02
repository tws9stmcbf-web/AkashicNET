#!/usr/bin/env python3
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references/community/source-coverage-v0.14.json"
ALLOWED = {"AVAILABLE", "REDIRECTED", "UNAVAILABLE", "RATE_LIMITED", "UNCHECKED"}
URL_RE = re.compile(r"https?://[^\s<>\"'`]+")
TRAILING = ".,;:!?)]}"


def fail(msg):
    raise SystemExit(f"FAIL: {msg}")


def clean_url(raw):
    return raw.rstrip(TRAILING)


def is_repository_self(url, contract):
    p = urlparse(url)
    host = (p.hostname or "").lower()
    if host in set(contract.get("first_party_hosts_excluded", [])):
        return True
    self_hosts = set(contract.get("repository_self_hosts_excluded", []))
    if host not in self_hosts:
        return False
    prefix = contract.get("repository_self_path_prefix", "").strip("/").lower()
    path = p.path.strip("/").lower()
    if host == "github.com":
        return path.startswith(prefix)
    if host == "api.github.com":
        return path.startswith("repos/" + prefix)
    if host == "raw.githubusercontent.com":
        return path.startswith(prefix)
    return False


if not MANIFEST.is_file():
    fail("missing v0.14 source coverage manifest")
m = json.loads(MANIFEST.read_text())
if m.get("target_version") != "0.14.0-beta.1":
    fail("wrong target version")
if m.get("status") != "COMPLETE_FAIL_CLOSED":
    fail("coverage manifest is not COMPLETE_FAIL_CLOSED")
if m.get("coverage_complete") is not True:
    fail("coverage denominator is not declared complete")
if m.get("release_ready") is not False:
    fail("source coverage contract must not itself declare release readiness")
if set(m.get("allowed_statuses", [])) != ALLOWED:
    fail("allowed source statuses changed")

contract = m.get("denominator_contract", {})
if contract.get("mode") != "repository_derived_recursive_scan":
    fail("unsupported denominator mode")
if contract.get("default_status") != "UNCHECKED":
    fail("default status must remain UNCHECKED")
suffixes = set(contract.get("included_suffixes", []))
if not suffixes:
    fail("included suffixes missing")
excluded = set(contract.get("excluded_paths", []))
files = []
for root_name in contract.get("roots", []):
    root = ROOT / root_name
    if not root.is_dir():
        fail(f"missing release-boundary root: {root_name}")
    for p in root.rglob("*"):
        if p.is_file() and p.suffix.lower() in suffixes:
            rel = p.relative_to(ROOT).as_posix()
            if rel not in excluded:
                files.append(p)
for rel in contract.get("root_files", []):
    p = ROOT / rel
    if not p.is_file():
        fail(f"missing release-boundary root file: {rel}")
    files.append(p)

contexts = {}
for p in sorted(set(files), key=lambda x: x.as_posix()):
    rel = p.relative_to(ROOT).as_posix()
    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fail(f"release-boundary file is not UTF-8: {rel}")
    for raw in URL_RE.findall(text):
        url = clean_url(raw)
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            fail(f"unrepresentable URL in {rel}: {url}")
        if is_repository_self(url, contract):
            continue
        contexts.setdefault(url, set()).add(rel)

reviewed = {}
for rec in m.get("reviewed_overrides", []):
    sid = rec.get("source_id")
    url = rec.get("original_url")
    status = rec.get("status")
    review = rec.get("review_record")
    if not sid or not isinstance(url, str) or status not in ALLOWED or not review:
        fail("malformed reviewed override")
    if url in reviewed:
        fail(f"duplicate reviewed override: {url}")
    rp = ROOT / review
    if not rp.is_file():
        fail(f"missing review record: {review}")
    robj = json.loads(rp.read_text())
    source = robj.get("source", {})
    if source.get("source_id") != sid or source.get("original_url") != url or source.get("live_status") != status:
        fail(f"review override does not match source record: {review}")
    if url not in contexts:
        fail(f"reviewed URL is outside derived release denominator: {url}")
    reviewed[url] = rec

records = []
for url in sorted(contexts):
    override = reviewed.get(url)
    record = {
        "source_id": override["source_id"] if override else "SRC-" + hashlib.sha256(url.encode()).hexdigest()[:16],
        "original_url": url,
        "status": override["status"] if override else "UNCHECKED",
        "contexts": sorted(contexts[url]),
    }
    if override:
        record["review_record"] = override["review_record"]
    records.append(record)

payload = {
    "schema_version": "0.1",
    "target_version": "0.14.0-beta.1",
    "denominator_mode": contract["mode"],
    "record_count": len(records),
    "records": records,
    "invariants": m.get("invariants", {}),
}
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
digest = hashlib.sha256(canonical).hexdigest()
payload["sha256"] = digest
out = ROOT / contract.get("generated_inventory_path", "artifacts/source-coverage-v0.14.generated.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

inv = m.get("invariants", {})
for key in ["original_url_preserved", "provenance_contexts_preserved"]:
    if inv.get(key) is not True:
        fail(f"invariant must be true: {key}")
for key in ["silent_replacement", "unavailable_or_changed_means_false", "truth_inference", "scientific_evidence_promotion", "rights_promotion", "private_drive_promotion"]:
    if inv.get(key) is not False:
        fail(f"invariant must be false: {key}")

print(f"PASS: v0.14 complete source denominator enumerates {len(records)} external URLs; sha256={digest}")
