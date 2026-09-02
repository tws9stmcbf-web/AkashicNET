#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references/community/automation-reproducibility-beta-release-manifest-v0.14.json"
V013 = "fbb7b6f539947f528383ca13a01639a04471b594"
V013_SEAL = "98e551d5fe257c6e7aa991812b0d56f0dc0bf0a7"
V014 = "7b6cfd89de570c4b945d574dad570c37825645fe"
V014_SEAL = "24c7d3d214e31a8de1357edaf02fe191b12872f5"
REQUIRED_GATES = {
    "historical_release_ledger",
    "repository_state_readiness_reconstruction",
    "complete_source_denominator",
    "source_integrity_provenance_guards",
    "cross_source_candidate_separation",
    "big_questions_registry_and_architecture",
    "public_data_privacy_boundary",
    "immutable_actions_refs",
    "v0.13_public_knowledge_readiness",
    "v0.12_integration_readiness",
}


def fail(msg):
    raise SystemExit(f"FAIL: {msg}")

if not MANIFEST.is_file():
    fail("v0.14 release manifest missing")
m = json.loads(MANIFEST.read_text())
if m.get("target_version") != "0.14.0-beta.1":
    fail("wrong target version")
if m.get("target_name") != "Automation & Reproducibility Beta":
    fail("wrong target name")
if m.get("state") not in {"CANDIDATE", "READY", "SEALED"}:
    fail("invalid release state")
if m.get("release_policy") != "exact_commit_fail_closed":
    fail("release policy is not exact-commit fail-closed")

base = m.get("historical_baseline", {})
if base.get("v0.13_validated_release_commit") != V013 or base.get("v0.13_seal_metadata_commit") != V013_SEAL:
    fail("historical v0.13 baseline changed")
if base.get("must_not_retarget") is not True:
    fail("historical retargeting guard missing")

if set(m.get("required_gates", [])) != REQUIRED_GATES:
    fail("required gate set changed")
for rel in m.get("required_artifacts", []):
    if not (ROOT / rel).is_file():
        fail(f"required artifact missing: {rel}")

coverage = m.get("source_coverage", {})
if coverage.get("status") != "COMPLETE_FAIL_CLOSED":
    fail("source coverage is not complete/fail-closed")
if not isinstance(coverage.get("derived_external_url_count"), int) or coverage["derived_external_url_count"] <= 0:
    fail("source coverage count invalid")
sha = coverage.get("derived_inventory_sha256_at_source_coverage_candidate")
if not isinstance(sha, str) or len(sha) != 64:
    fail("source coverage digest invalid")

inv = m.get("invariants", {})
for key in [
    "truth_inference", "rights_promotion", "scientific_evidence_promotion",
    "private_drive_promotion", "api_unverified_reddit_as_verified",
    "cross_source_candidates_are_truth_claims", "circular_confidence_amplification",
    "unavailable_or_changed_means_false", "bq001_forced_resolution",
]:
    if inv.get(key) is not False:
        fail(f"invariant must remain false: {key}")

state = m.get("state")
if state == "CANDIDATE":
    if m.get("validated_release_commit") is not None or m.get("seal_metadata_commit") is not None:
        fail("candidate must not predeclare release or seal commit")
elif state == "READY":
    if m.get("validated_release_commit") != V014:
        fail("READY state does not preserve exact validated v0.14 target")
    if m.get("seal_metadata_commit") is not None:
        fail("READY state must not predeclare seal metadata commit")
else:
    if m.get("validated_release_commit") != V014:
        fail("SEALED state retargeted v0.14")
    if m.get("seal_metadata_commit") != V014_SEAL:
        fail("SEALED state does not preserve exact v0.14 seal metadata provenance")

print(f"PASS: v0.14 Automation & Reproducibility Beta manifest validates in state {state}")
