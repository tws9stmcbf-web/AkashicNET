#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "references/community/release-ledger-v0.14.json"
V013 = ROOT / "references/community/public-knowledge-beta-release-manifest-v0.13.json"

EXPECTED = {
    "0.10.0-prealpha": "5dc9a6ccf872e57a98bb3b6d999b5e32f841f0c9",
    "0.11.0-beta.1": "818ad224f47da78194c31a817161365f50202d4d",
    "0.12.0-beta.1": "c986cf14d91edf2274cfd9351a7d330edcff620c",
    "0.13.0-beta.1": "fbb7b6f539947f528383ca13a01639a04471b594",
}
EXPECTED_V013_SEAL = "98e551d5fe257c6e7aa991812b0d56f0dc0bf0a7"


def fail(msg: str) -> None:
    raise SystemExit(f"FAIL: {msg}")


def main() -> None:
    if not LEDGER.exists():
        fail("release ledger missing")
    data = json.loads(LEDGER.read_text())
    if data.get("policy") != "append_only_exact_commit_fail_closed":
        fail("ledger policy must be append_only_exact_commit_fail_closed")

    releases = data.get("releases")
    if not isinstance(releases, list):
        fail("releases must be a list")
    versions = [r.get("version") for r in releases]
    if len(versions) != len(set(versions)):
        fail("duplicate release versions")

    by_version = {r.get("version"): r for r in releases}
    for version, sha in EXPECTED.items():
        record = by_version.get(version)
        if record is None:
            fail(f"missing historical release {version}")
        if record.get("validated_release_commit") != sha:
            fail(f"historical target changed for {version}")
        if record.get("retargetable") is not False:
            fail(f"historical release {version} must be non-retargetable")

    v013 = by_version["0.13.0-beta.1"]
    if v013.get("state") != "SEALED":
        fail("v0.13 must remain SEALED")
    if v013.get("seal_metadata_commit") != EXPECTED_V013_SEAL:
        fail("v0.13 seal metadata commit changed")

    manifest = json.loads(V013.read_text())
    if manifest.get("validated_release_commit") != EXPECTED["0.13.0-beta.1"]:
        fail("v0.13 manifest target differs from ledger")
    if manifest.get("state") != "SEALED":
        fail("v0.13 manifest is not SEALED")

    inv = data.get("invariants", {})
    required_false = [
        "truth_inference",
        "rights_promotion",
        "scientific_evidence_promotion",
        "private_drive_promotion",
    ]
    for key in required_false:
        if inv.get(key) is not False:
            fail(f"invariant {key} must remain false")
    if inv.get("historical_targets_are_immutable") is not True:
        fail("historical target immutability not asserted")
    if inv.get("later_seal_commits_do_not_retarget") is not True:
        fail("seal non-retargeting invariant not asserted")

    print("PASS: v0.14 release ledger preserves historical validated targets")


if __name__ == "__main__":
    main()
