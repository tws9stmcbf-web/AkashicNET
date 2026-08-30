#!/usr/bin/env python3
import json
from pathlib import Path

PATH = Path("references/community/canonical-adjudication-batch3-v0.7.3.json")
EXPECTED = {"CANON-B3-ABRAMELIN", "CANON-B3-AGRIPPA", "CANON-B3-VIVEKANANDA"}
FORBIDDEN_PROMOTIONS = (
    "rights_promoted",
    "public_release_promoted",
    "scientific_evidence_promoted",
    "safety_or_efficacy_promoted",
)


def main() -> int:
    data = json.loads(PATH.read_text(encoding="utf-8"))
    assert data["contract_version"] == "0.7.0"
    assert data["batch_version"] == "0.7.3"
    records = data["records"]
    assert len(records) == 3
    assert {r["logical_id"] for r in records} == EXPECTED

    for record in records:
        assert record["relationship"] == "REPRESENTS_WORK"
        assert record["decision"] == "ACCEPT"
        assert "PUBLIC_LIBRARY_CATALOGUE" in record["evidence_class"]
        assert record["provenance"] and len(record["provenance"]) >= 2
        assert record["rationale"].strip()
        assert record["contradiction_check"].strip()
        for field in FORBIDDEN_PROMOTIONS:
            assert record[field] is False

    print("CANONICAL BATCH 3 PASS: 3 work identities ACCEPT; all side-effect promotions false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
