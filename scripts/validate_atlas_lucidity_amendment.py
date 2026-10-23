#!/usr/bin/env python3
"""Validate the bounded PR412 metadata amendment; no scientific reanalysis.

Requires the amendment's recorded baseline commit in the local Git history.
DOI ownership is checked in research/reference JSON, not across every external
publication or unrelated branch. Repeated citations with the same owner are OK.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = "references/research-atlas/review-candidates-2026-10-22-grief-lucidity.json"
BASE = "fe130ec0df56f72decaf8c7aa026cb9bee7c0af3"
ORIGINAL = "SRC-ATLAS-LUCIDITY-GNAF178-2025"
SECONDARY = "SRC-ATLAS-LUCIDITY-LCA-2026"
ALLOWED = {
    RECORD,
    "research/atlas-grief-lucidity-review-2026-10-22.md",
    "research/atlas-lucidity-secondary-analysis-2026-10-23.md",
    "scripts/validate_atlas_lucidity_amendment.py",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def parse(text):
    return json.loads(text, object_pairs_hook=unique_keys)


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True)


def normalise_doi(value):
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", value.strip(), flags=re.I).lower()


def objects(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def validate(record, baseline):
    require(record["amendment_provenance"]["base_commit"] == BASE, "Baseline changed")
    require(record["version"] == "0.1.2", "Unexpected amendment version")
    require(record["status"] == "REVIEW_CANDIDATE", "Batch promoted")
    require(record["question_status"] == baseline["question_status"] == "UNRESOLVED", "BQ status changed")
    require(record["governance"] == baseline["governance"], "Governance changed")
    require(record["deduplication"] == baseline["deduplication"], "Prior duplicate receipt changed")
    require(record["correction_check"] == baseline["correction_check"], "Prior correction scope overwritten")
    history = baseline["review_updates"]
    require(record["review_updates"][:len(history)] == history, "Review history overwritten")
    require(len(record["review_updates"]) > len(history), "No appended review receipt")
    require(record["sources"][:2] == baseline["sources"][:2], "Unrelated grief records changed")

    rows = record["sources"]
    ids = [row["source_id"] for row in rows]
    dois = [normalise_doi(row["doi"]) for row in rows]
    require(len(ids) == len(set(ids)) == 4, "Duplicate or unexpected source IDs")
    require(len(dois) == len(set(dois)), "Duplicate normalised DOI in batch")
    by_id = {row["source_id"]: row for row in rows}
    expected = {
        ORIGINAL: ("10.1093/geront/gnaf178", "40748700", "PMC12871080"),
        SECONDARY: ("10.1177/13872877261445464", "42081117", "PMC13225770"),
    }
    for sid, identity in expected.items():
        row = by_id[sid]
        require((row["doi"], row["pmid"], row["pmcid"]) == identity, f"Identity mismatch: {sid}")
        for url in (f"https://doi.org/{identity[0]}", f"https://pubmed.ncbi.nlm.nih.gov/{identity[1]}/", f"https://pmc.ncbi.nlm.nih.gov/articles/{identity[2]}/"):
            require(url in row["references"], f"Identifier URL missing: {url}")
    for row in rows:
        require(row["supports_models"] == [], "Support edge added")
        require(row["public_integration"] is False, "Public integration enabled")
        require(row["canonical_evidence_status"] == "NOT_PROMOTED", "Evidence promoted")
        require(row["status"] == "REVIEW_CANDIDATE", "Source promoted")

    original, secondary = by_id[ORIGINAL], by_id[SECONDARY]
    prior = baseline["sources"][2]
    mutable = {"sample", "reviewed_on", "assessment_added", "next_review_action"}
    for key, value in prior.items():
        if key not in mutable:
            require(original[key] == value, f"Original field unexpectedly changed: {key}")
    require(all(original["sample"][k] == v for k, v in prior["sample"].items()), "Original denominators overwritten")
    require(original["sample"]["enrolled_participants"] == 20, "Enrolled denominator changed")
    require(original["sample"]["participants_with_audiovisual_observations"] == 19, "Recorded denominator changed")
    require(secondary["sample"] == {"participants": 3, "audiovisual_segments": 1283, "newly_recruited_participants": 0}, "Secondary denominators or recruitment changed")
    require(secondary["replication_status"] == "NOT_INDEPENDENT_REPLICATION_SAME_COHORT", "False replication credit")
    require(secondary["independent_review_status"] == "REQUIRED_NOT_COMPLETED", "Independent review bypassed")
    require(record["amendment_provenance"]["independent_review_status"] == "REQUIRED_NOT_COMPLETED", "Review provenance changed")
    require(secondary["original_date"] == "2026-05-04" and secondary["issue_date"] == "2026-06", "Publication dates conflated")

    groups = record["cohort_groups"]
    require(len(groups) == 1, "Unexpected cohort count")
    group = groups[0]
    require(original["cohort_id"] == secondary["cohort_id"] == group["cohort_id"], "Cohort identity mismatch")
    require(group["source_ids"] == [ORIGINAL, SECONDARY] and group["primary_source_id"] == ORIGINAL, "Cohort source references invalid")
    for key, value in {"enrolled_unique_participants": 20, "participants_with_audiovisual_observations": 19, "secondary_analysis_subset_participants": 3, "new_participants_from_secondary_analysis": 0, "independent_cohorts": 1}.items():
        require(group[key] == value, f"Cohort double counting: {key}")
    for row, target, relation in [(original, SECONDARY, "HAS_SECONDARY_ANALYSIS"), (secondary, ORIGINAL, "SECONDARY_ANALYSIS_OF")]:
        require(row["related_publications"] == [{"source_id": target, "relationship": relation, "same_cohort": True}], "Nonreciprocal publication relationship")
    receipt = record["review_updates"][-1]
    require(receipt["source_id"] == SECONDARY and receipt["related_source_id"] == ORIGINAL, "Receipt source mismatch")
    require(receipt["resolves_lead"]["url"] == history[0]["discovery_lead"]["url"], "Lead resolution mismatch")
    require((ROOT / receipt["appraisal_ref"]).is_file(), "Appraisal link missing")
    require(record["correction_check_updates"][-1]["dois"] == [original["doi"], secondary["doi"]], "Correction update identities invalid")
    require(record["amendment_provenance"]["source_identity_checks"] == [{"source_id": row["source_id"], "doi": row["doi"], "pmid": row["pmid"], "pmcid": row["pmcid"], "verified_against": row["references"]} for row in (original, secondary)], "Identity receipt mismatch")


def main():
    record = parse((ROOT / RECORD).read_text())
    baseline = parse(git("show", f"{BASE}:{RECORD}"))
    validate(record, baseline)
    ownership = {}
    for directory in ("references", "research"):
        for path in (ROOT / directory).rglob("*.json"):
            for obj in objects(parse(path.read_text())):
                if isinstance(obj.get("source_id"), str) and isinstance(obj.get("doi"), str):
                    doi = normalise_doi(obj["doi"])
                    require(re.fullmatch(r"10\.\d{4,9}/\S+", doi), f"Invalid DOI in {path}")
                    ownership.setdefault(doi, set()).add(obj["source_id"])
    for sid in (ORIGINAL, SECONDARY):
        doi = next(row["doi"] for row in record["sources"] if row["source_id"] == sid)
        require(ownership[doi] == {sid}, f"Conflicting DOI ownership: {doi}: {ownership[doi]}")
    changed = set(git("diff", "--name-only", BASE, "--").splitlines())
    changed.update(git("ls-files", "--others", "--exclude-standard").splitlines())
    require(changed <= ALLOWED, f"Changes outside bounded amendment: {sorted(changed - ALLOWED)}")
    print("PASS: 4 unique source IDs/DOIs; reciprocal same-cohort links; 20 enrolled/19 recorded/3 reused/0 new; history and safeguards preserved")
    print("PASS: lucidity DOI ownership in reference/research JSON; bounded changed paths; independent review still required")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
