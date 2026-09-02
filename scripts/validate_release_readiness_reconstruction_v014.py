#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references/community/release-readiness-reconstruction-v0.14.json"
LEDGER = ROOT / "references/community/release-ledger-v0.14.json"

REQUIRED_INPUTS = [
    "references/community/release-ledger-v0.14.json",
    "references/community/public-knowledge-beta-release-manifest-v0.13.json",
    "references/community/public-knowledge-beta-readiness-v0.13.json",
    "references/community/integration-beta-readiness-v0.12.json",
    "references/big-questions/architecture-v0.1.json",
]
REQUIRED_VALIDATORS = [
    "scripts/validate_release_ledger_v014.py",
    "scripts/audit_public_knowledge_beta_readiness_v013.py",
    "scripts/validate_public_knowledge_release_manifest_v013.py",
    "scripts/validate_public_route_qa_v013.py",
    "scripts/validate_support_evidence_boundary_v013.py",
    "scripts/validate_public_knowledge_link_integrity_v013.py",
    "scripts/audit_integration_beta_readiness_v012.py",
    "scripts/validate_big_question_architecture_v01.py",
    "scripts/validate_actions_immutable_refs.py",
    "scripts/check_public_data_boundary.py",
]
V013 = "fbb7b6f539947f528383ca13a01639a04471b594"
SEAL = "98e551d5fe257c6e7aa991812b0d56f0dc0bf0a7"


def fail(msg):
    raise SystemExit(f"FAIL: {msg}")

if not MANIFEST.is_file():
    fail("missing reconstruction manifest")
if not LEDGER.is_file():
    fail("missing release ledger")

m = json.loads(MANIFEST.read_text())
l = json.loads(LEDGER.read_text())

if m.get("reconstruction_policy") != "repository_state_and_ci_only_fail_closed":
    fail("reconstruction policy is not fail-closed")
if m.get("status") != "IN_DEVELOPMENT":
    fail("v0.14 must remain IN_DEVELOPMENT until final release gate")

for p in REQUIRED_INPUTS:
    if p not in m.get("authoritative_inputs", []):
        fail(f"manifest missing authoritative input: {p}")
    if not (ROOT / p).is_file():
        fail(f"repository missing authoritative input: {p}")

for p in REQUIRED_VALIDATORS:
    if p not in m.get("required_validators", []):
        fail(f"manifest missing validator: {p}")
    if not (ROOT / p).is_file():
        fail(f"repository missing validator: {p}")

base = m.get("historical_baseline", {})
if base.get("v0.13_validated_release_commit") != V013:
    fail("v0.13 validated target changed")
if base.get("v0.13_seal_metadata_commit") != SEAL:
    fail("v0.13 seal metadata changed")
if base.get("retarget_allowed") is not False:
    fail("historical retargeting is not disabled")

r13 = next((r for r in l.get("releases", []) if r.get("version") == "0.13.0-beta.1"), None)
if not r13:
    fail("v0.13 missing from release ledger")
if r13.get("validated_release_commit") != V013:
    fail("ledger v0.13 validated target changed")
if r13.get("seal_metadata_commit") != SEAL:
    fail("ledger v0.13 seal metadata changed")
if r13.get("retargetable") is not False:
    fail("ledger allows v0.13 retargeting")

assertions = m.get("reconstruction_assertions", {})
for key in [
    "historical_release_targets_resolve_from_ledger",
    "dependent_release_manifests_are_repository_addressable",
    "dependent_validators_are_repository_addressable",
    "ci_is_required_for_readiness_claim",
    "missing_input_fails_closed",
    "missing_validator_fails_closed",
]:
    if assertions.get(key) is not True:
        fail(f"required reconstruction assertion not true: {key}")
if assertions.get("requires_conversational_state") is not False:
    fail("conversational state must not be required")
if assertions.get("requires_manual_memory") is not False:
    fail("manual memory must not be required")

inv = m.get("invariants", {})
for key in [
    "truth_inference",
    "rights_promotion",
    "scientific_evidence_promotion",
    "private_drive_promotion",
    "api_unverified_reddit_as_verified",
    "cross_source_candidates_are_truth_claims",
]:
    if inv.get(key) is not False:
        fail(f"invariant must remain false: {key}")

print("PASS: v0.14 release readiness is reconstructable from repository state and CI inputs")
