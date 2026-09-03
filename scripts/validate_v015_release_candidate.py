#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references/community/public-sync-observability-beta-release-manifest-v0.15.json"
V014 = "7b6cfd89de570c4b945d574dad570c37825645fe"
READINESS_MERGE = "3537d5725b45c8ff856a3aa0897d10245812aa72"

if not MANIFEST.is_file():
    raise SystemExit("FAIL: missing v0.15 release candidate manifest")
m = json.loads(MANIFEST.read_text())
if m.get("target_version") != "0.15.0-beta.1": raise SystemExit("FAIL: wrong target version")
if m.get("target_name") != "Public Sync & Observability Beta": raise SystemExit("FAIL: wrong target name")
if m.get("state") != "READY_CANDIDATE": raise SystemExit("FAIL: candidate must not self-declare sealed")
if m.get("baseline", {}).get("validated_release_commit") != V014: raise SystemExit("FAIL: v0.14 baseline changed")
if m.get("baseline", {}).get("retarget_allowed") is not False: raise SystemExit("FAIL: v0.14 baseline became retargetable")
if m.get("repository_readiness_merge") != READINESS_MERGE: raise SystemExit("FAIL: wrong repository readiness merge")
if m.get("live_site_verification_issue") != 242 or m.get("live_site_verification_state") != "COMPLETED": raise SystemExit("FAIL: live verification prerequisite not recorded complete")
p = m.get("promotion", {})
if p.get("ready") is not False or p.get("sealed") is not False or p.get("validated_release_commit") is not None: raise SystemExit("FAIL: candidate prematurely promoted")
for key, value in m.get("invariants", {}).items():
    if value is not False: raise SystemExit(f"FAIL: invariant must remain false: {key}")

r = subprocess.run([sys.executable, "scripts/validate_v015_readiness.py"], cwd=ROOT)
if r.returncode != 0: raise SystemExit("FAIL: composed v0.15 readiness gate failed")
print("PASS: v0.15 release candidate is ready for exact-head CI review; promotion remains false until reviewed")
