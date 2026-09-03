#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references/community/public-sync-observability-beta-release-manifest-v0.15.json"
V014 = "7b6cfd89de570c4b945d574dad570c37825645fe"
V015 = "ea46629558ff57970f6efd2485a7e9a288dc55f2"
READY_META = "392205a17f2d6187b91c1ee6524df00d829b468a"

if not MANIFEST.is_file():
    raise SystemExit("FAIL: missing v0.15 manifest")
m = json.loads(MANIFEST.read_text())
if m.get("target_version") != "0.15.0-beta.1": raise SystemExit("FAIL: wrong target version")
if m.get("target_name") != "Public Sync & Observability Beta": raise SystemExit("FAIL: wrong target name")
if m.get("state") != "SEALED": raise SystemExit("FAIL: v0.15 must be SEALED")
if m.get("baseline", {}).get("validated_release_commit") != V014: raise SystemExit("FAIL: v0.14 baseline retargeted")
if m.get("baseline", {}).get("retarget_allowed") is not False: raise SystemExit("FAIL: v0.14 baseline became retargetable")
p = m.get("promotion", {})
if p.get("ready") is not True or p.get("sealed") is not True: raise SystemExit("FAIL: promotion flags incomplete")
if p.get("validated_release_commit") != V015: raise SystemExit("FAIL: v0.15 validated release commit retargeted")
if p.get("seal_metadata_commit") != READY_META: raise SystemExit("FAIL: wrong READY metadata provenance")
if m.get("live_site_verification_issue") != 242 or m.get("live_site_verification_state") != "COMPLETED": raise SystemExit("FAIL: live-site prerequisite missing")
for key, value in m.get("invariants", {}).items():
    if value is not False: raise SystemExit(f"FAIL: invariant must remain false: {key}")

r = subprocess.run([sys.executable, "scripts/validate_v015_readiness.py"], cwd=ROOT)
if r.returncode != 0: raise SystemExit("FAIL: v0.15 readiness regression")
print("PASS: v0.15.0-beta.1 is sealed without retargeting validated release state")
