#!/usr/bin/env python3
import json
from pathlib import Path

PATH = Path("references/community/canonical-adjudication-batch3-v0.7.3.json")
PRIOR = Path("references/community/canonical-adjudication-public-bibliography-v0.10.1.json")
EXPECTED = {"CANON-B3-ABRAMELIN", "CANON-B3-AGRIPPA", "CANON-B3-VIVEKANANDA"}
EXPECTED_PRIOR = {
    "CANON-B2-ABRAMELIN": "ACCEPT",
    "CANON-B2-AGRIPPA": "HOLD",
    "CANON-B2-VIVEKANANDA": "HOLD",
}
FORBIDDEN_PROMOTIONS = (
    "rights_promoted",
    "public_release_promoted",
    "scientific_evidence_promoted",
    "safety_or_efficacy_promoted",
)


def main() -> int:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    prior = json.loads(PRIOR.read_text(encoding="utf-8"))
    assert data["contract_version"] == "0.7.0"
    assert data["batch_version"] == "0.7.3"
    assert data["supersedes_checkpoint"] == PRIOR.name
    records = data["records"]
    assert len(records) == 3
    assert {r["logical_id"] for r in records} == EXPECTED

    prior_decisions = {r["candidate_id"]: r["decision"] for r in prior["records"]}
    for candidate_id, decision in EXPECTED_PRIOR.items():
        assert prior_decisions[candidate_id] == decision

    mapped = {r["supersedes_candidate_id"] for r in records}
    assert mapped == set(EXPECTED_PRIOR)

    for record in records:
        assert record["relationship"] == "REPRESENTS_WORK"
        assert record["decision"] == "ACCEPT"
        assert record["evidence_class"] == "INDEPENDENT_PUBLIC_BIBLIOGRAPHY"
        assert "PUBLIC_BIBLIOGRAPHIC_AUTHORITY" in record["signals"]
        assert record["provenance"] and len(record["provenance"]) >= 2
        assert record["rationale"].strip()
        assert record["contradiction_check"].strip()
        for field in FORBIDDEN_PROMOTIONS:
            assert record[field] is False

    print("CANONICAL BATCH 3 PASS: prior decisions reconciled; 3 work identities ACCEPT; all side-effect promotions false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
