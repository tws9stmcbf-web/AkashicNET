#!/usr/bin/env python3

import json
import sys
from pathlib import Path

EXPECTED_BATCHES = [
    "references/big-questions/BQ001/evidence-batch1-v0.1.json",
    "references/big-questions/BQ001/evidence-batch2-v0.1.json",
    "references/big-questions/BQ001/evidence-batch3-v0.1.json",
    "references/big-questions/BQ001/evidence-batch4-v0.1.json",
    "references/big-questions/BQ001/evidence-batch5-v0.1.json",
    "references/big-questions/BQ001/evidence-batch6-v0.1.json",
]
EXPECTED_MODELS = {"MODEL-BQ001-BIOLOGICAL-DEPENDENCE", "MODEL-BQ001-CONTINUITY"}
EXPECTED_LABELS = {
    "Established Evidence",
    "Interpretation",
    "Lived Experience/Testimony",
    "Hypothesis",
    "Speculation",
}
REQUIRED_FALSE_GUARDS = {
    "single_score_allowed",
    "model_vote_counting_allowed",
    "unsupported_claims_allowed",
    "resolved_metaphysical_conclusion_allowed",
    "testimony_or_anomaly_proves_survival",
    "brain_dependence_proves_non_survival",
    "philosophical_position_counts_as_empirical_verdict",
}


def fail(message):
    raise ValueError(message)


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def validate(payload, repo_root=Path(".")):
    if payload.get("synthesis_id") != "BQ001-PUBLIC-SYNTHESIS":
        fail("unexpected synthesis_id")
    if payload.get("question_id") != "BQ001":
        fail("question_id must be BQ001")
    if payload.get("status") != "UNRESOLVED":
        fail("public synthesis must remain UNRESOLVED")
    if payload.get("source_batches") != EXPECTED_BATCHES:
        fail("public synthesis must reference exactly the six validated BQ001 batches")

    claims = {}
    sources = {}
    for rel in EXPECTED_BATCHES:
        batch = load_json(repo_root / rel)
        if batch.get("question_id") != "BQ001" or batch.get("question_status") != "UNRESOLVED":
            fail(f"invalid or resolved source batch: {rel}")
        for claim in batch.get("claims", []):
            cid = claim.get("claim_id")
            if not cid or cid in claims:
                fail(f"missing or duplicate claim id across batches: {cid}")
            claims[cid] = claim
        for source in batch.get("sources", []):
            sid = source.get("source_id")
            if not sid:
                fail(f"source without id in {rel}")
            sources[sid] = source

    sections = payload.get("sections")
    if not isinstance(sections, list) or len(sections) < 6:
        fail("public synthesis requires multiple evidence-domain sections")
    seen = set()
    for section in sections:
        section_id = section.get("id")
        if not section_id or section_id in seen:
            fail("section ids must be present and unique")
        seen.add(section_id)
        label = section.get("evidence_label")
        if label not in EXPECTED_LABELS:
            fail(f"{section_id}: invalid evidence label")
        claim_ids = section.get("claim_ids")
        source_ids = section.get("source_ids")
        if not claim_ids or not source_ids:
            fail(f"{section_id}: claim_ids and source_ids are required")
        for cid in claim_ids:
            if cid not in claims:
                fail(f"{section_id}: unsupported claim id {cid}")
            if claims[cid].get("evidence_label") != label:
                fail(f"{section_id}: synthesis evidence label does not match {cid}")
        for sid in source_ids:
            if sid not in sources:
                fail(f"{section_id}: unsupported source id {sid}")
        claim_source_ids = {sid for cid in claim_ids for sid in claims[cid].get("source_ids", [])}
        if not set(source_ids).issubset(claim_source_ids):
            fail(f"{section_id}: source ids must be traceable through the cited claims")
        boundary = section.get("boundary", "")
        if not isinstance(boundary, str) or len(boundary.strip()) < 20:
            fail(f"{section_id}: explicit evidence boundary is required")

    models = payload.get("competing_models")
    if not isinstance(models, list) or {m.get("model_id") for m in models} != EXPECTED_MODELS:
        fail("both competing BQ001 models must remain visible")
    if any(m.get("status") != "UNRESOLVED" for m in models):
        fail("competing models must remain UNRESOLVED")

    conclusion = payload.get("conclusion", {})
    if conclusion.get("status") != "UNRESOLVED":
        fail("conclusion must remain UNRESOLVED")
    statement = conclusion.get("statement", "").lower()
    if "surviving irreversible death" not in statement or "impossibility" not in statement:
        fail("conclusion must explicitly preserve both survival and non-survival uncertainty")

    counter = payload.get("counter_inferences", [])
    joined = " ".join(counter).lower()
    required_phrases = ["does not prove non-survival", "do not prove consciousness", "does not prove reincarnation", "not votes"]
    if any(phrase not in joined for phrase in required_phrases):
        fail("required counter-inference boundaries are missing")

    guards = payload.get("promotion_guards", {})
    for key in REQUIRED_FALSE_GUARDS:
        if guards.get(key) is not False:
            fail(f"promotion guard must remain false: {key}")

    if len(payload.get("open_questions", [])) < 4:
        fail("open questions must remain first-class data")


def main():
    if len(sys.argv) != 2:
        print("usage: validate_bq001_public_synthesis_v01.py <public-synthesis.json>", file=sys.stderr)
        return 2
    try:
        payload = load_json(sys.argv[1])
        validate(payload, Path("."))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"BQ001 PUBLIC SYNTHESIS FAIL: {exc}", file=sys.stderr)
        return 1
    print("BQ001 PUBLIC SYNTHESIS PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
