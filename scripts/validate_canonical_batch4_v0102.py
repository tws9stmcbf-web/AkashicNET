#!/usr/bin/env python3
import json
from pathlib import Path

PATH = Path("references/community/canonical-adjudication-batch4-v0.10.2.json")
data = json.loads(PATH.read_text(encoding="utf-8"))
records = data.get("records", [])
expected = {"CANON-B2-FORBIDDEN-HISTORY", "CANON-B2-BARDON-VARIANTS", "CANON-B2-RAMAYANA"}
assert data.get("contract_version") == "0.7.0"
assert data.get("batch_version") == "0.10.2"
assert len(records) == 3
assert {r.get("candidate_id") for r in records} == expected
for r in records:
    assert r.get("decision") == "HOLD"
    assert r.get("relationship") in {"REPRESENTS_WORK", "REPRESENTS_EDITION"}
    assert r.get("evidence_class")
    assert r.get("rationale")
    assert r.get("contradiction_check")
    for flag in ("rights_promoted", "public_release_promoted", "scientific_evidence_promoted", "safety_or_efficacy_promoted"):
        assert r.get(flag) is False
summary = data.get("summary", {})
assert summary.get("records") == 3
assert summary.get("accept") == 0
assert summary.get("hold") == 3
assert summary.get("reject") == 0
print("CANONICAL BATCH 4 PASS: 3 unresolved families remain HOLD; all side-effect promotions false")
