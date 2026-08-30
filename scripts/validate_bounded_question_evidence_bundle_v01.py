#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAXONOMY = ROOT / "references" / "community" / "evidence-taxonomy-v0.10.json"
CORE_SCHEMA = ROOT / "data" / "evidence_claim_v01.schema.json"
CANONICAL_LABELS = {
    "Established Evidence",
    "Interpretation",
    "Lived Experience/Testimony",
    "Hypothesis",
    "Speculation",
}
FALSE_GUARDS = {
    "truth_inference_allowed",
    "scientific_evidence_promotion_allowed",
    "rights_promotion_allowed",
    "privacy_posture_changed",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path: Path) -> None:
    data = load(path)
    taxonomy = load(TAXONOMY)
    core_schema = load(CORE_SCHEMA)

    assert data["question_id"].startswith("BQ")
    assert data["question"].strip()
    assert data["question_status"] in {"UNRESOLVED", "PARTIALLY_RESOLVED", "RESOLVED"}
    assert data["public_epistemic_taxonomy"] == "references/community/evidence-taxonomy-v0.10.json"
    assert data["core_evidence_contract"] == "data/evidence_claim_v01.schema.json"
    assert set(taxonomy["canonical_labels"]) == CANONICAL_LABELS
    assert core_schema["title"] == "AkashicNET Evidence Claim v0.1"

    sources = data["sources"]
    assert sources
    source_ids = set()
    for source in sources:
        sid = source["source_id"]
        assert sid and sid not in source_ids
        source_ids.add(sid)
        assert source["type"].strip()
        assert source["title"].strip()
        assert isinstance(source["year"], int)
        assert source["url"].startswith("https://")
        assert source.get("doi") or source.get("pmid") or source["url"], "source must be reproducibly addressable"

    core = data["evidence_core"]
    assert core["evidence_model_version"] == "0.1"
    claims = core["claims"]
    links = core["evidence_links"]
    assert claims and links

    claim_ids = set()
    for claim in claims:
        cid = claim["claim_id"]
        assert cid and cid not in claim_ids
        claim_ids.add(cid)
        assert claim["statement"].strip()
        assert claim["provenance"]
        prov_ids = claim["provenance"].get("source_ids", [])
        assert prov_ids
        assert set(prov_ids) <= source_ids

    annotations = data["epistemic_annotations"]
    assert len(annotations) == len(claims)
    annotated_ids = set()
    for annotation in annotations:
        cid = annotation["claim_id"]
        assert cid in claim_ids
        assert cid not in annotated_ids
        annotated_ids.add(cid)
        assert annotation["label"] in CANONICAL_LABELS
    assert annotated_ids == claim_ids

    linked_claims = set()
    for link in links:
        assert link["claim_id"] in claim_ids
        assert link["source_id"] in source_ids
        linked_claims.add(link["claim_id"])
    assert linked_claims == claim_ids

    limitations = data["material_limitations"]
    assert limitations and all(item.strip() for item in limitations)

    implications = data["model_implications"]
    assert implications["model_edges_upgrade_epistemic_label"] is False

    invariants = data["release_invariants"]
    for key in FALSE_GUARDS:
        assert invariants[key] is False, f"guard must remain false: {key}"
    for key, value in invariants.items():
        if key.endswith("_allowed") or key.endswith("_promoted") or key.endswith("_changed"):
            assert value is False, f"fail-closed invariant must remain false: {key}"


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit("usage: validate_bounded_question_evidence_bundle_v01.py <bundle.json>")
    path = Path(sys.argv[1])
    if not path.is_absolute():
        path = ROOT / path
    validate(path)
    print(f"BOUNDED QUESTION EVIDENCE BUNDLE v0.1 PASS: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
