"""Offline provenance checks; no retrieval, evidence appraisal or promotion."""

import copy
import json
from pathlib import Path
import unittest
from urllib.parse import parse_qs, urlencode, urlsplit


PILOT = Path(__file__).resolve().parents[1] / "references/psi/reincarnation-bibliographic-pilot-2026-10-02.json"


def validate_pubmed(record):
    pubmed = record["pubmed"]
    returned = pubmed["records"]
    endpoint = pubmed["summary_endpoint"]
    if pubmed["lookup"] == "EXACT_DOI_QUERY":
        search = urlsplit(pubmed["search_endpoint"])
        assert (search.scheme, search.netloc, search.path) == (
            "https", "eutils.ncbi.nlm.nih.gov", "/entrez/eutils/esearch.fcgi"
        ), "Invalid PubMed search endpoint"
        try:
            search_query = parse_qs(search.query, keep_blank_values=True, strict_parsing=True)
        except ValueError as exc:
            raise AssertionError("Malformed PubMed search query") from exc
        # Extra filters/history can manufacture a null result for an indexed DOI.
        assert set(search_query) <= {"db", "term", "retmode", "tool", "retmax"}, "Unsupported PubMed search parameters"
        assert all(len(values) == 1 and values[0].strip() for values in search_query.values()), "Search parameters must be single nonblank values"
        assert search_query.get("db") == ["pubmed"], "Search endpoint must query PubMed"
        assert [term.strip().lower() for term in search_query.get("term", [])] == [
            record["doi"].strip().lower() + "[doi]"
        ], "Search DOI must match source DOI"
    if pubmed["match_status"] == "NO_MATCH_RETURNED_FOR_EXACT_DOI_QUERY":
        assert pubmed["lookup"] == "EXACT_DOI_QUERY", "No-match result requires an exact DOI query"
        assert returned == [], "No-match result must have no returned records"
        assert pubmed["search_count"] == 0, "No-match result must have zero search count"
    if not returned:
        assert endpoint is None, "Empty PubMed result must have a null summary endpoint"
        assert pubmed["match_status"] == "NO_MATCH_RETURNED_FOR_EXACT_DOI_QUERY", "Empty PubMed result cannot claim a DOI match"
        return
    assert pubmed["match_status"] == "EXACT_NORMALIZED_DOI", "Returned records require verified DOI matches"
    assert isinstance(endpoint, str), "Returned records require a summary endpoint"
    url = urlsplit(endpoint)
    assert (url.scheme, url.netloc, url.path) == (
        "https", "eutils.ncbi.nlm.nih.gov", "/entrez/eutils/esummary.fcgi"
    ), "Invalid PubMed summary endpoint"
    query = parse_qs(url.query)
    assert query.get("db") == ["pubmed"], "Summary endpoint must query PubMed"
    assert len(query.get("id", [])) == 1, "Summary endpoint requires one PMID list"
    ids = query["id"][0].split(",")
    uids = [item["uid"] for item in returned]
    assert all(isinstance(uid, str) and uid.isdigit() for uid in uids), "Invalid returned PMID"
    assert len(ids) == len(uids) and set(ids) == set(uids), "Summary PMIDs must equal returned record PMIDs"
    for item in returned:
        assert item["doi"].strip().lower() == record["doi"].strip().lower(), "Returned DOI must match source DOI"


class PubMedProvenanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = json.loads(PILOT.read_text(encoding="utf-8"))["records"]

    def test_current_pilot(self):
        for record in self.records:
            with self.subTest(doi=record["doi"]):
                validate_pubmed(record)

    def test_original_unrelated_endpoints_are_rejected(self):
        no_matches = [r for r in self.records if not r["pubmed"]["records"]]
        self.assertEqual(len(no_matches), 2)
        for record in no_matches:
            with self.subTest(doi=record["doi"]):
                broken = copy.deepcopy(record)
                broken["pubmed"]["summary_endpoint"] = self.records[-1]["pubmed"]["summary_endpoint"]
                with self.assertRaisesRegex(AssertionError, "null summary endpoint"):
                    validate_pubmed(broken)

    def test_empty_result_cannot_bypass_guard_by_changing_match_status(self):
        broken = copy.deepcopy(self.records[1])
        broken["pubmed"]["match_status"] = "EXACT_NORMALIZED_DOI"
        broken["pubmed"]["summary_endpoint"] = self.records[-1]["pubmed"]["summary_endpoint"]
        with self.assertRaisesRegex(AssertionError, "null summary endpoint"):
            validate_pubmed(broken)

    def test_empty_result_with_null_endpoint_cannot_claim_a_match(self):
        for record in self.records:
            if record["pubmed"]["records"]:
                continue
            with self.subTest(doi=record["doi"]):
                broken = copy.deepcopy(record)
                broken["pubmed"]["match_status"] = "EXACT_NORMALIZED_DOI"
                with self.assertRaisesRegex(AssertionError, "cannot claim a DOI match"):
                    validate_pubmed(broken)

    def test_exact_search_cannot_query_another_publication(self):
        for record in self.records:
            if record["pubmed"]["lookup"] != "EXACT_DOI_QUERY":
                continue
            with self.subTest(doi=record["doi"]):
                broken = copy.deepcopy(record)
                other = next(r for r in self.records if r["doi"] != record["doi"]
                             and r["pubmed"]["lookup"] == "EXACT_DOI_QUERY")
                broken["pubmed"]["search_endpoint"] = other["pubmed"]["search_endpoint"]
                with self.assertRaisesRegex(AssertionError, "Search DOI"):
                    validate_pubmed(broken)

    def test_no_match_requires_exact_query_provenance(self):
        broken = copy.deepcopy(self.records[1])
        broken["pubmed"]["lookup"] = "KNOWN_PMID_ESUMMARY"
        with self.assertRaisesRegex(AssertionError, "requires an exact DOI query"):
            validate_pubmed(broken)

    def test_exact_search_rejects_filters_and_malformed_parameters(self):
        suffixes = (
            "&mindate=1900&maxdate=1901&datetype=pdat",
            "&reldate=1",
            "&query_key=1&WebEnv=other_search&usehistory=y",
            "&db=", "&term=", "&db", "&term",
            "&db=pubmed", "&term=unrelated",
            "&retmode=", "&retmax=", "&tool=",
            "&unexpected=value", "&",
        )
        for record in self.records:
            if record["pubmed"]["lookup"] != "EXACT_DOI_QUERY":
                continue
            for suffix in suffixes:
                with self.subTest(doi=record["doi"], suffix=suffix):
                    broken = copy.deepcopy(record)
                    broken["pubmed"]["search_endpoint"] += suffix
                    with self.assertRaises(AssertionError):
                        validate_pubmed(broken)

    def test_exact_search_accepts_equivalent_query_encoding(self):
        for record in self.records:
            if record["pubmed"]["lookup"] != "EXACT_DOI_QUERY":
                continue
            with self.subTest(doi=record["doi"]):
                equivalent = copy.deepcopy(record)
                search = urlsplit(equivalent["pubmed"]["search_endpoint"])
                query = parse_qs(search.query)
                query["term"] = [" " + record["doi"].upper() + "[doi] "]
                equivalent["pubmed"]["search_endpoint"] = search._replace(
                    query=urlencode(list(reversed(list(query.items()))), doseq=True)
                ).geturl()
                validate_pubmed(equivalent)

    def test_matched_record_cannot_use_another_publications_summary(self):
        broken = copy.deepcopy(self.records[0])
        broken["pubmed"]["summary_endpoint"] = self.records[-1]["pubmed"]["summary_endpoint"]
        with self.assertRaisesRegex(AssertionError, "Summary PMIDs"):
            validate_pubmed(broken)

    def test_matched_record_requires_source_doi(self):
        broken = copy.deepcopy(self.records[0])
        broken["pubmed"]["records"][0]["doi"] = self.records[-1]["doi"]
        with self.assertRaisesRegex(AssertionError, "Returned DOI"):
            validate_pubmed(broken)

    def test_no_match_cannot_carry_returned_records(self):
        broken = copy.deepcopy(self.records[1])
        broken["pubmed"]["records"] = copy.deepcopy(self.records[-1]["pubmed"]["records"])
        with self.assertRaisesRegex(AssertionError, "no returned records"):
            validate_pubmed(broken)


if __name__ == "__main__":
    unittest.main()
