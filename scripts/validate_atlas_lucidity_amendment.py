#!/usr/bin/env python3
"""Validate the bounded PR412 metadata amendment; no scientific reanalysis.

Requires the amendment's recorded baseline commit in the local Git history.
DOI ownership is checked in research/reference JSON, not across every external
publication or unrelated branch. Repeated citations with the same owner are OK.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = "references/research-atlas/review-candidates-2026-10-22-grief-lucidity.json"
BASE = "fe130ec0df56f72decaf8c7aa026cb9bee7c0af3"
AUDIT_BASE = "5879b6daedf1096beabf2a168f474f5fb504bfe6"
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
    require(record["version"] in {"0.1.2", "0.1.3"}, "Unexpected amendment version")
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
    mutable = {"sample", "reviewed_on", "assessment_added", "next_review_action", "access_scope", "data_code_preregistration", "limitations"}
    for key, value in prior.items():
        if key not in mutable:
            require(original[key] == value, f"Original field unexpectedly changed: {key}")
    require(all(original["sample"][k] == v for k, v in prior["sample"].items()), "Original denominators overwritten")
    require(original["limitations"][:len(prior["limitations"])] == prior["limitations"], "Original limitations erased")
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
    receipts = [item for item in record["review_updates"] if "resolves_lead" in item]
    require(len(receipts) == 1, "Expected exactly one lead-resolution receipt")
    receipt = receipts[0]
    require(receipt["source_id"] == SECONDARY and receipt["related_source_id"] == ORIGINAL, "Receipt source mismatch")
    require(receipt["resolves_lead"]["url"] == history[0]["discovery_lead"]["url"], "Lead resolution mismatch")
    require((ROOT / receipt["appraisal_ref"]).is_file(), "Appraisal link missing")
    require(record["correction_check_updates"][-1]["dois"] == [original["doi"], secondary["doi"]], "Correction update identities invalid")
    require(record["amendment_provenance"]["source_identity_checks"] == [{"source_id": row["source_id"], "doi": row["doi"], "pmid": row["pmid"], "pmcid": row["pmcid"], "verified_against": row["references"]} for row in (original, secondary)], "Identity receipt mismatch")


def validate_main_text_audit(record, prior):
    require(record["review_updates"][:len(prior["review_updates"])] == prior["review_updates"], "Earlier review receipts changed")
    require(record["correction_check_updates"][:len(prior["correction_check_updates"])] == prior["correction_check_updates"], "Earlier correction receipts changed")
    require(record["amendment_provenance"] == prior["amendment_provenance"], "Initial amendment provenance changed")
    for current, previous in zip(record["sources"], prior["sources"]):
        require(current["limitations"][:len(previous["limitations"])] == previous["limitations"], "Prior limitations removed")
        require(current["sample"] == previous["sample"], "Audit changed cohort/segment denominators")
    audit = record["methods_audit"]
    require(audit["base_commit"] == AUDIT_BASE, "Audit baseline changed")
    require(audit["access"] == {"original_main_manuscript_read": True, "secondary_main_manuscript_read": True, "publisher_version_compared": False, "supplement_read": False, "code_audited": False, "participant_data_accessed": False}, "Access scope overstated or participant data accessed")
    require(audit["independent_review_status"] == "REQUIRED_NOT_COMPLETED" and audit["scientific_evidence_promotion"] is False, "Audit bypassed review/promotion gate")
    questions = audit["denominator_questions"]
    require(len(questions) == 1 and questions[0]["source_id"] == ORIGINAL, "Denominator question source invalid")
    require((questions[0]["audiovisual_observations"], questions[0]["power_analysis_days_reported"], questions[0]["status"]) == (539, 556, "OPEN_MAPPING_NOT_ESTABLISHED"), "Distinct denominator mapping silently resolved")
    snapshots = audit["source_snapshots"]
    require(len(snapshots) == 5 and len({item["url"] for item in snapshots}) == 5, "Source receipt count/URL uniqueness invalid")
    for item in snapshots:
        require(re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) and item["bytes"] > 0, "Invalid source fingerprint")
    checks = audit["source_identity_and_notice_checks"]
    require([item["source_id"] for item in checks] == [ORIGINAL, SECONDARY], "Notice source identities invalid")
    for item, row in zip(checks, record["sources"][2:4]):
        require(item["doi"] == row["doi"] and item["pmc_version"] == row["pmcid"] + ".1", "Notice/version identity mismatch")
        require(item["pubmed_comments_corrections_count"] == 0 and item["crossref_relation"] == {} and item["crossref_update_to"] == [] and item["crossref_updated_by"] == [], "Notice fields differ; requires fresh audit")


def validate_source_cache(record, cache):
    names = ["pubmed-records.xml", "pmc-original.xml", "pmc-secondary.xml", "crossref-original.json", "crossref-secondary.json"]
    snapshots = record["methods_audit"]["source_snapshots"]
    for name, receipt in zip(names, snapshots):
        raw = (cache / name).read_bytes()
        require(len(raw) == receipt["bytes"] and hashlib.sha256(raw).hexdigest() == receipt["sha256"], f"Source response changed: {name}")
    pubmed = ET.fromstring((cache / names[0]).read_bytes())
    for label, check, row in zip(["original", "secondary"], record["methods_audit"]["source_identity_and_notice_checks"], record["sources"][2:4]):
        articles = [article for article in pubmed.findall("PubmedArticle") if article.findtext("./MedlineCitation/PMID") == row["pmid"]]
        require(len(articles) == 1, "Missing or duplicate article PMID")
        article = articles[0]
        # Only the article's IDs: .//ArticleId would also include cited works.
        ids = {item.attrib["IdType"]: item.text for item in article.findall("./PubmedData/ArticleIdList/ArticleId")}
        require((ids["pubmed"], ids["pmc"], ids["doi"]) == (row["pmid"], row["pmcid"], row["doi"]), "PubMed article identity mismatch")
        notices = article.findall("./MedlineCitation/CommentsCorrectionsList/CommentsCorrections")
        require(len(notices) == check["pubmed_comments_corrections_count"], "PubMed notice fields changed")
        pmc = ET.fromstring((cache / f"pmc-{label}.xml").read_bytes())
        ids = {item.attrib["pub-id-type"]: item.text for item in pmc.findall("./article/front/article-meta/article-id")}
        require((ids["pmid"], ids["pmcid"], ids["doi"], ids["pmcid-ver"]) == (row["pmid"], row["pmcid"], row["doi"], check["pmc_version"]), "PMC article identity/version mismatch")
        crossref = parse((cache / f"crossref-{label}.json").read_text())["message"]
        require(crossref["DOI"].lower() == row["doi"].lower(), "Crossref DOI mismatch")
        for key, receipt_key, default in [("relation", "crossref_relation", {}), ("update-to", "crossref_update_to", []), ("updated-by", "crossref_updated_by", [])]:
            require(crossref.get(key, default) == check[receipt_key], f"Crossref {key} changed")
    print("PASS: 5 source-cache fingerprints; article-level PMID/PMCID/DOI/version and inspected notice fields match")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-cache", type=Path, help="Check five saved public source responses against the audit receipts")
    args = parser.parse_args()
    record = parse((ROOT / RECORD).read_text())
    baseline = parse(git("show", f"{BASE}:{RECORD}"))
    validate(record, baseline)
    if record["version"] == "0.1.3":
        prior = parse(git("show", f"{AUDIT_BASE}:{RECORD}"))
        validate_main_text_audit(record, prior)
        if args.source_cache:
            validate_source_cache(record, args.source_cache)
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
    except (ValueError, KeyError, TypeError, OSError, ET.ParseError, subprocess.CalledProcessError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        sys.exit(1)
