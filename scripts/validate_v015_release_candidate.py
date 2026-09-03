#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references/community/public-sync-observability-beta-release-manifest-v0.15.json"
V014 = "7b6cfd89de570c4b945d574dad570c37825645fe"
READINESS_MERGE = "3537d5725b45c8ff856a3aa0897d10245812aa72"
V015 = "ea46629558ff57970f6efd2485a7e9a288dc55f2"  # exact candidate head with all required checks green
EXPECTED_RELEASE_POLICY = "exact_commit_fail_closed"
EXPECTED_VALIDATORS = [
    "scripts/validate_v015_readiness.py",
    "scripts/validate_release_ledger_v014.py",
    "scripts/validate_public_observability_contract_v015.py",
    "scripts/validate_public_infrastructure_observability_v015.py",
    "scripts/validate_public_status_consistency_v015.py",
]
EXPECTED_INVARIANTS = {
    "truth_inference": False,
    "rights_promotion": False,
    "scientific_evidence_promotion": False,
    "private_drive_promotion": False,
    "api_unverified_reddit_as_verified": False,
    "circular_confidence_amplification": False,
    "bq001_forced_resolution": False,
}
EXPECTED_CANDIDATE_PROMOTION = {
    "ready": False,
    "sealed": False,
    "validated_release_commit": None,
    "seal_metadata_commit": None,
}
READY_METADATA = "5ba6989aade68461c8f3953c4a82cc0e158b0730"
EXPECTED_READY_PROMOTION = {
    "ready": True,
    "sealed": False,
    "validated_release_commit": V015,
    "seal_metadata_commit": None,
}
EXPECTED_SEALED_PROMOTION = {
    "ready": True,
    "sealed": True,
    "validated_release_commit": V015,
    "seal_metadata_commit": READY_METADATA,
}

if not MANIFEST.is_file():
    raise SystemExit("FAIL: missing v0.15 release candidate manifest")
m = json.loads(MANIFEST.read_text())
if m.get("target_version") != "0.15.0-beta.1":
    raise SystemExit("FAIL: wrong target version")
if m.get("target_name") != "Public Sync & Observability Beta":
    raise SystemExit("FAIL: wrong target name")
state = m.get("state")
if state not in {"READY_CANDIDATE", "READY", "SEALED"}:
    raise SystemExit("FAIL: v0.15 release state must be READY_CANDIDATE, READY or SEALED")
if m.get("release_policy") != EXPECTED_RELEASE_POLICY:
    raise SystemExit("FAIL: release policy must remain exact_commit_fail_closed")
if m.get("baseline", {}).get("validated_release_commit") != V014:
    raise SystemExit("FAIL: v0.14 baseline changed")
if m.get("baseline", {}).get("retarget_allowed") is not False:
    raise SystemExit("FAIL: v0.14 baseline became retargetable")
if m.get("repository_readiness_merge") != READINESS_MERGE:
    raise SystemExit("FAIL: wrong repository readiness merge")
if m.get("live_site_verification_issue") != 242 or m.get("live_site_verification_state") != "COMPLETED":
    raise SystemExit("FAIL: live verification prerequisite not recorded complete")
if m.get("required_validators") != EXPECTED_VALIDATORS:
    raise SystemExit("FAIL: required validator set changed")
promotion = m.get("promotion")
if state == "READY_CANDIDATE":
    if promotion != EXPECTED_CANDIDATE_PROMOTION:
        raise SystemExit("FAIL: candidate promotion metadata must remain entirely unset")
elif state == "READY":
    if promotion != EXPECTED_READY_PROMOTION:
        raise SystemExit("FAIL: READY promotion must preserve the exact validated v0.15 target and defer sealing")
elif promotion != EXPECTED_SEALED_PROMOTION:
    raise SystemExit("FAIL: SEALED promotion must preserve the exact v0.15 target and READY metadata provenance")
if m.get("invariants") != EXPECTED_INVARIANTS:
    raise SystemExit("FAIL: complete fail-closed invariant set must be preserved")

r = subprocess.run([sys.executable, "scripts/validate_v015_readiness.py"], cwd=ROOT)
if r.returncode != 0:
    raise SystemExit("FAIL: composed v0.15 readiness gate failed")
print(f"PASS: v0.15 release manifest validates in state {state}; exact target and fail-closed invariants are preserved")
