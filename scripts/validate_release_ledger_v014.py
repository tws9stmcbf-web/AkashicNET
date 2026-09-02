#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "references/community/release-ledger-v0.14.json"
V013_MANIFEST = ROOT / "references/community/public-knowledge-beta-release-manifest-v0.13.json"
V014_MANIFEST = ROOT / "references/community/automation-reproducibility-beta-release-manifest-v0.14.json"

EXPECTED = {
    "0.10.0-prealpha": "5dc9a6ccf872e57a98bb3b6d999b5e32f841f0c9",
    "0.11.0-beta.1": "818ad224f47da78194c31a817161365f50202d4d",
    "0.12.0-beta.1": "c986cf14d91edf2274cfd9351a7d330edcff620c",
    "0.13.0-beta.1": "fbb7b6f539947f528383ca13a01639a04471b594",
    "0.14.0-beta.1": "7b6cfd89de570c4b945d574dad570c37825645fe",
}
EXPECTED_V013_SEAL = "98e551d5fe257c6e7aa991812b0d56f0dc0bf0a7"
EXPECTED_V014_SEAL = "24c7d3d214e31a8de1357edaf02fe191b12872f5"


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
    if versions != ["0.10.0-prealpha", "0.11.0-beta.1", "0.12.0-beta.1", "0.13.0-beta.1", "0.14.0-beta.1"]:
        fail("release ledger order or append-only sequence changed")

    by_version = {r.get("version"): r for r in releases}
    for version, sha in EXPECTED.items():
        record = by_version.get(version)
        if record is None:
            fail(f"missing release {version}")
        if record.get("validated_release_commit") != sha:
            fail(f"validated target changed for {version}")
        if record.get("retargetable") is not False:
            fail(f"release {version} must be non-retargetable")

    v013 = by_version["0.13.0-beta.1"]
    if v013.get("state") != "SEALED" or v013.get("seal_metadata_commit") != EXPECTED_V013_SEAL:
        fail("v0.13 seal metadata changed")

    v014 = by_version["0.14.0-beta.1"]
    if v014.get("name") != "Automation & Reproducibility Beta":
        fail("v0.14 release name changed")
    if v014.get("state") != "SEALED":
        fail("v0.14 ledger entry is not SEALED")
    if v014.get("seal_metadata_commit") != EXPECTED_V014_SEAL:
        fail("v0.14 seal metadata commit changed")
    if v014.get("manifest") != "references/community/automation-reproducibility-beta-release-manifest-v0.14.json":
        fail("v0.14 manifest path changed")

    m13 = json.loads(V013_MANIFEST.read_text())
    if m13.get("validated_release_commit") != EXPECTED["0.13.0-beta.1"] or m13.get("state") != "SEALED":
        fail("v0.13 manifest differs from ledger")

    m14 = json.loads(V014_MANIFEST.read_text())
    if m14.get("validated_release_commit") != EXPECTED["0.14.0-beta.1"]:
        fail("v0.14 manifest target differs from ledger")
    if m14.get("seal_metadata_commit") != EXPECTED_V014_SEAL:
        fail("v0.14 manifest seal metadata differs from ledger")
    if m14.get("state") != "SEALED":
        fail("v0.14 manifest is not SEALED")

    inv = data.get("invariants", {})
    for key in ["truth_inference", "rights_promotion", "scientific_evidence_promotion", "private_drive_promotion"]:
        if inv.get(key) is not False:
            fail(f"invariant {key} must remain false")
    if inv.get("historical_targets_are_immutable") is not True:
        fail("historical target immutability not asserted")
    if inv.get("later_seal_commits_do_not_retarget") is not True:
        fail("seal non-retargeting invariant not asserted")

    print("PASS: release ledger preserves v0.10-v0.14 exact targets and sealed v0.14 metadata")


if __name__ == "__main__":
    main()
