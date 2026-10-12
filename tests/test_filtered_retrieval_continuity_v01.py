"""Synthetic backend-independent continuity contract; NOT production retrieval.

The SQLite exact-reference adapter is test infrastructure, not an ANN backend,
API v0.25 extension, or certification of query_api_v025. Its max-dot ranking is
deliberately separate from production provenance-tier ranking. Future adapters
can implement the same lifecycle surface and reuse the frozen fixture/oracle.
Only synthetic metadata is persisted, exclusively under pytest temporary paths.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import math
from pathlib import Path
import random
import sqlite3
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_PATH = ROOT / "tests/fixtures/filtered-retrieval-continuity-v0.1.json"
FIXTURE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
SOURCES = {"library", "reddit"}
EVIDENCE = {"SOURCE_CLASSIFICATION_ONLY", "UNASSESSED"}
DECISIONS = {"ACCEPT", "HOLD", "DIRECT_METADATA_LOOKUP"}
REQUIRED_INDEXES = {
    "continuity_public": ("objects", ("public_safe", "metadata_eligible")),
    "continuity_source": ("objects", ("source",)),
    "continuity_evidence": ("objects", ("evidence",)),
    "continuity_concept": ("objects", ("concept",)),
    "continuity_vectors": ("vectors", ("object_id",)),
}
PUBLIC_FIELDS = (
    "id", "label", "source", "evidence", "concept", "semantic_decision",
    "rights_state", "provenance",
)


class ContractError(ValueError):
    """Only fixed, payload-free messages may cross the public boundary."""


class MissingRequiredIndex(ContractError):
    pass


def synthetic_records():
    records = []
    specs = copy.deepcopy(FIXTURE["records"])
    distractors = FIXTURE["distractors"]
    for number in range(distractors["count"]):
        specs.append({
            "id": f'{distractors["id_prefix"]}{number:02d}',
            **{key: distractors[key] for key in ("source", "evidence", "vectors")},
        })
    for spec in specs:
        record = copy.deepcopy(FIXTURE["defaults"])
        record.update(spec)
        record["provenance"]["record_id"] = record["id"]
        record["provenance"]["independence_key"] = "synthetic:" + record["source"]
        records.append(record)
    return records


def public_projection(record):
    return {key: copy.deepcopy(record[key]) for key in PUBLIC_FIELDS}


class ExactReferenceAdapter:
    """Small transactional oracle target, with no network or production imports."""

    def __init__(self, path):
        self.path = Path(path)
        # Reopen must not create a new empty store or silently rebuild indexes.
        self.db = sqlite3.connect(self.path.as_uri() + "?mode=rw", uri=True)
        self.db.execute("PRAGMA foreign_keys=ON")

    @classmethod
    def create(cls, path):
        path = Path(path)
        if path.exists():
            raise ContractError("store already exists")
        db = sqlite3.connect(path)
        try:
            with db:
                db.execute("CREATE TABLE objects (id TEXT PRIMARY KEY, public_safe INTEGER, "
                           "metadata_eligible INTEGER, source TEXT, evidence TEXT, concept TEXT, "
                           "decision TEXT, payload TEXT NOT NULL)")
                db.execute("CREATE TABLE vectors (object_id TEXT REFERENCES objects(id), "
                           "ordinal INTEGER, x REAL, y REAL, PRIMARY KEY(object_id, ordinal))")
                db.execute("CREATE TABLE protected (id INTEGER PRIMARY KEY, payload TEXT NOT NULL)")
                db.execute("INSERT INTO protected VALUES (1, ?)", (json.dumps({
                    "policy": FIXTURE["policy"], "edges": FIXTURE["protected_edges"],
                }, sort_keys=True),))
                for name, (table, columns) in REQUIRED_INDEXES.items():
                    db.execute(f"CREATE INDEX {name} ON {table} ({','.join(columns)})")
        finally:
            db.close()
        return cls(path)

    def close(self):
        self.db.close()

    def _require_indexes(self):
        for name, (table, columns) in REQUIRED_INDEXES.items():
            row = self.db.execute("SELECT tbl_name FROM sqlite_master "
                                  "WHERE type='index' AND name=?", (name,)).fetchone()
            actual = tuple(item[2] for item in self.db.execute(f"PRAGMA index_info({name})"))
            index = next((item for item in self.db.execute(f"PRAGMA index_list({table})")
                          if item[1] == name), None)
            if row != (table,) or actual != columns or index is None or index[4] != 0:
                raise MissingRequiredIndex("required retrieval index unavailable")

    @staticmethod
    def _validate_record(record):
        try:
            vectors = record["vectors"]
            valid = (
                isinstance(record["id"], str) and record["id"].startswith("synthetic:")
                and all(key in record for key in PUBLIC_FIELDS)
                and record["source"] in SOURCES and record["evidence"] in EVIDENCE
                and record["semantic_decision"] in DECISIONS
                and isinstance(record["provenance"], dict)
                and isinstance(vectors, list) and bool(vectors)
                and all(isinstance(v, list) and len(v) == 2 for v in vectors)
                and all(type(x) in (int, float) and math.isfinite(x) for v in vectors for x in v)
            )
            if not valid:
                raise ContractError("invalid synthetic record")
        except (KeyError, TypeError):
            raise ContractError("invalid synthetic record") from None

    def _insert_vectors(self, record):
        self.db.executemany("INSERT INTO vectors VALUES (?, ?, ?, ?)", [
            (record["id"], ordinal, *vector)
            for ordinal, vector in enumerate(record["vectors"])
        ])

    def insert_batch(self, records):
        # BEGIN IMMEDIATE prevents a competing schema writer between preflight
        # and commit. Validate every record before the first durable object write.
        try:
            with self.db:
                self.db.execute("BEGIN IMMEDIATE")
                self._require_indexes()
                for record in records:
                    self._validate_record(record)
                for record in records:
                    self.db.execute("INSERT INTO objects VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (
                        record["id"], int(record.get("public_safe") is True),
                        int(record.get("metadata_eligible") is True), record["source"],
                        record["evidence"], record["concept"], record["semantic_decision"],
                        json.dumps(record, sort_keys=True),
                    ))
                    self._insert_vectors(record)
        except sqlite3.Error:
            raise ContractError("synthetic storage write failed") from None

    def query(self, vector, filters, limit=100):
        if (not isinstance(filters, dict)
                or set(filters) - {"source", "evidence", "concept", "state"}
                or type(limit) is not int or limit < 1
                or not isinstance(vector, list) or len(vector) != 2
                or any(type(x) not in (int, float) or not math.isfinite(x) for x in vector)):
            raise ContractError("invalid retrieval request")
        for key, allowed in (("source", SOURCES), ("evidence", EVIDENCE),
                             ("state", {"all", "accepted", "hold"})):
            if key in filters and (not isinstance(filters[key], str) or filters[key] not in allowed):
                raise ContractError("unsupported filter value")
        if "concept" in filters and (not isinstance(filters["concept"], str) or not filters["concept"]):
            raise ContractError("unsupported filter value")
        where, parameters = ["public_safe=1", "metadata_eligible=1"], []
        for key in ("source", "evidence", "concept"):
            if key in filters:
                where.append(f"{key}=?")
                parameters.append(filters[key])
        state = filters.get("state", "all")
        if state == "accepted":
            where.append("decision IN ('ACCEPT','DIRECT_METADATA_LOOKUP')")
        elif state == "hold":
            where.append("decision='HOLD'")
        with self.db:
            self.db.execute("BEGIN")
            self._require_indexes()
            rows = self.db.execute("SELECT payload FROM objects WHERE " + " AND ".join(where), parameters)
            ranked = []
            for (payload,) in rows:
                record = json.loads(payload)
                if (record["provenance"].get("public_safe") is not True
                        or record["rights_state"] != "METADATA_LINK_ONLY"):
                    continue
                vectors = self.db.execute("SELECT x, y FROM vectors WHERE object_id=?", (record["id"],)).fetchall()
                if not vectors:
                    raise ContractError("retrieval vector data unavailable")
                score = max(sum(x * y for x, y in zip(vector, candidate)) for candidate in vectors)
                ranked.append((score, record["id"], public_projection(record)))
            ranked.sort(key=lambda item: (-item[0], item[1]))
            policy = json.loads(self.db.execute("SELECT payload FROM protected WHERE id=1").fetchone()[0])["policy"]
            return {"policy": policy, "summary": {"eligible_count": len(ranked)},
                    "results": [item[2] for item in ranked[:limit]]}

    def rebuild_index(self):
        # Rebuild derived vectors only; never infer or update semantic/evidence state.
        with self.db:
            self.db.execute("BEGIN IMMEDIATE")
            self._require_indexes()
            records = [json.loads(row[0]) for row in self.db.execute("SELECT payload FROM objects ORDER BY id")]
            self.db.execute("DELETE FROM vectors")
            for record in records:
                self._insert_vectors(record)

    def inspect_state(self):
        """Privileged test-only diagnostics: never returned from public query."""
        return {
            "objects": self.db.execute("SELECT * FROM objects ORDER BY id").fetchall(),
            "vectors": self.db.execute("SELECT * FROM vectors ORDER BY object_id, ordinal").fetchall(),
            "protected": self.db.execute("SELECT * FROM protected ORDER BY id").fetchall(),
        }

    def drop_index(self, name):
        assert name in REQUIRED_INDEXES
        with self.db:
            self.db.execute(f"DROP INDEX {name}")


def assert_response(response, case, records=None, limit=100):
    """Frozen ID expectations, not the adapter predicate, define success."""
    records = synthetic_records() if records is None else records
    by_id = {record["id"]: record for record in records}
    assert set(response) == {"policy", "summary", "results"}
    assert response["policy"] == FIXTURE["policy"]
    assert response["summary"] == {"eligible_count": len(case["expected_ids"])}
    assert [record["id"] for record in response["results"]] == case["expected_ids"][:limit]
    assert response["results"] == [public_projection(by_id[key]) for key in case["expected_ids"][:limit]]
    serialized = json.dumps(response, sort_keys=True)
    for record in records:
        if record.get("public_safe") is not True or record.get("metadata_eligible") is not True:
            assert record["id"] not in serialized
            assert record["label"] not in serialized


def assert_cases(adapter):
    before = adapter.inspect_state()
    for case in FIXTURE["cases"]:
        assert_response(adapter.query(FIXTURE["query_vector"], case["filters"]), case)
        assert adapter.inspect_state() == before


@pytest.fixture
def store(tmp_path):
    adapter = ExactReferenceAdapter.create(tmp_path / "synthetic.sqlite")
    adapter.insert_batch(synthetic_records())
    yield adapter
    adapter.close()


@pytest.mark.parametrize("order", ["forward", "reverse", "seed-7", "seed-19"])
def test_lifecycle_exact_targets_and_protected_state(tmp_path, order):
    records = synthetic_records()
    if order == "reverse":
        records.reverse()
    elif order.startswith("seed-"):
        random.Random(int(order.split("-")[1])).shuffle(records)
    path = tmp_path / "synthetic.sqlite"
    adapter = ExactReferenceAdapter.create(path)
    try:
        adapter.insert_batch(records)
        before = adapter.inspect_state()
        assert_cases(adapter)
        adapter.rebuild_index()
        assert adapter.inspect_state() == before
        assert_cases(adapter)
    finally:
        adapter.close()
    # A genuinely separate process cannot rely on the parent's open connection/cache.
    worker = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--reopen", str(path)],
                            check=True, capture_output=True, text=True, timeout=30)
    assert worker.stderr == ""
    outputs = json.loads(worker.stdout)
    assert len(outputs) == len(FIXTURE["cases"])
    for response, case in zip(outputs, FIXTURE["cases"]):
        assert_response(response, case)
    reopened = ExactReferenceAdapter(path)
    try:
        assert reopened.inspect_state() == before
        assert_cases(reopened)
    finally:
        reopened.close()


def test_multivector_retrieved_once_and_bounded_top_k(store):
    case = FIXTURE["cases"][0]
    response = store.query(FIXTURE["query_vector"], case["filters"], limit=1)
    assert_response(response, case, limit=1)
    assert response["results"][0]["id"] == "synthetic:multivector"


def test_fixture_defeats_unfiltered_candidate_window():
    records = synthetic_records()
    raw = sorted(records, key=lambda r: (-max(v[0] for v in r["vectors"]), r["id"]))
    raw_ids = {r["id"] for r in raw[:FIXTURE["raw_candidate_window"]]}
    assert raw_ids.isdisjoint(FIXTURE["cases"][0]["expected_ids"])


@pytest.mark.parametrize("name", sorted(REQUIRED_INDEXES))
def test_missing_index_fails_before_any_object_write_and_survives_reopen(store, name):
    store.drop_index(name)
    before = store.inspect_state()
    attempted = synthetic_records()[:2]
    for record in attempted:
        record["id"] += ":attempted"
    statements = []
    store.db.set_trace_callback(statements.append)
    with pytest.raises(MissingRequiredIndex, match="^required retrieval index unavailable$"):
        store.insert_batch(attempted)
    store.db.set_trace_callback(None)
    assert not any(sql.lstrip().upper().startswith("INSERT") for sql in statements)
    assert store.inspect_state() == before
    for operation in (lambda: store.query([1, 0], {}), store.rebuild_index):
        with pytest.raises(MissingRequiredIndex):
            operation()
        assert store.inspect_state() == before
    reopened = ExactReferenceAdapter(store.path)
    try:
        assert reopened.inspect_state() == before
        with pytest.raises(MissingRequiredIndex):
            reopened.query([1, 0], {})
    finally:
        reopened.close()
    worker = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--check-missing", str(store.path)],
                            check=True, capture_output=True, text=True, timeout=30)
    assert worker.stdout.strip() == "required retrieval index unavailable"
    assert worker.stderr == ""
    assert store.inspect_state() == before


def test_named_but_wrong_index_fails_closed(store):
    store.drop_index("continuity_source")
    with store.db:
        store.db.execute("CREATE INDEX continuity_source ON objects(evidence)")
    before = store.inspect_state()
    with pytest.raises(MissingRequiredIndex):
        store.insert_batch(synthetic_records()[:1])
    assert store.inspect_state() == before


def test_named_partial_index_fails_closed(store):
    store.drop_index("continuity_source")
    with store.db:
        store.db.execute("CREATE INDEX continuity_source ON objects(source) WHERE public_safe=0")
    before = store.inspect_state()
    with pytest.raises(MissingRequiredIndex):
        store.insert_batch(synthetic_records()[:1])
    with pytest.raises(MissingRequiredIndex):
        store.query([1, 0], {})
    assert store.inspect_state() == before


def test_vector_order_and_multiplicity_do_not_change_results_or_semantics(tmp_path):
    records = synthetic_records()
    multivector = next(record for record in records if record["id"] == "synthetic:multivector")
    multivector["vectors"] = list(reversed(multivector["vectors"])) * 3
    adapter = ExactReferenceAdapter.create(tmp_path / "multiplicity.sqlite")
    try:
        adapter.insert_batch(records)
        assert_cases(adapter)
    finally:
        adapter.close()


def test_mid_batch_vector_failure_rolls_back_objects_and_vectors(store, monkeypatch):
    before = store.inspect_state()
    records = synthetic_records()[:2]
    for record in records:
        record["id"] += ":attempted"
    original = store._insert_vectors
    calls = []

    def fail_second(record):
        calls.append(record["id"])
        if len(calls) == 2:
            raise sqlite3.OperationalError("SYNTHETIC_PRIVATE_CANARY_PAYLOAD")
        original(record)

    monkeypatch.setattr(store, "_insert_vectors", fail_second)
    with pytest.raises(ContractError, match="^synthetic storage write failed$"):
        store.insert_batch(records)
    assert len(calls) == 2
    assert store.inspect_state() == before
    reopened = ExactReferenceAdapter(store.path)
    try:
        assert reopened.inspect_state() == before
    finally:
        reopened.close()


def test_invalid_late_record_is_rejected_before_first_write(store):
    records = synthetic_records()[:2]
    records[1]["vectors"] = [[float("nan"), 0]]
    statements = []
    store.db.set_trace_callback(statements.append)
    with pytest.raises(ContractError, match="^invalid synthetic record$"):
        store.insert_batch(records)
    store.db.set_trace_callback(None)
    assert not any(sql.lstrip().upper().startswith("INSERT") for sql in statements)


@pytest.mark.parametrize("field", ["public_safe", "metadata_eligible"])
@pytest.mark.parametrize("value", ["absent", None, False, "true", 1])
def test_absent_null_and_non_boolean_eligibility_fail_closed(tmp_path, field, value):
    record = synthetic_records()[0]
    record["id"] = "synthetic:denied-canary"
    record["label"] = "SYNTHETIC_DENIED_CANARY_PAYLOAD"
    if value == "absent":
        record.pop(field)
    else:
        record[field] = value
    adapter = ExactReferenceAdapter.create(tmp_path / "denied.sqlite")
    try:
        adapter.insert_batch([record])
        response = adapter.query([1, 0], {})
        assert response["results"] == []
        assert response["summary"] == {"eligible_count": 0}
        assert "CANARY" not in json.dumps(response)
    finally:
        adapter.close()


@pytest.mark.parametrize("gate", ["provenance", "rights"])
def test_independent_provenance_and_rights_gate(tmp_path, gate):
    record = synthetic_records()[0]
    if gate == "provenance":
        record["provenance"]["public_safe"] = False
    else:
        record["rights_state"] = "METADATA_WITHHELD"
    adapter = ExactReferenceAdapter.create(tmp_path / "gate.sqlite")
    try:
        adapter.insert_batch([record])
        response = adapter.query([1, 0], {})
        assert response["results"] == []
        assert response["summary"] == {"eligible_count": 0}
    finally:
        adapter.close()


@pytest.mark.parametrize("value", ["absent", None])
def test_missing_or_null_rights_never_become_eligible(tmp_path, value):
    record = synthetic_records()[0]
    if value == "absent":
        record.pop("rights_state")
    else:
        record["rights_state"] = value
    adapter = ExactReferenceAdapter.create(tmp_path / "rights.sqlite")
    try:
        if value == "absent":
            before = adapter.inspect_state()
            with pytest.raises(ContractError, match="^invalid synthetic record$"):
                adapter.insert_batch([record])
            assert adapter.inspect_state() == before
        else:
            adapter.insert_batch([record])
        assert adapter.query([1, 0], {})["results"] == []
    finally:
        adapter.close()


@pytest.mark.parametrize("value", ["absent", None, "true", 1])
def test_missing_or_non_boolean_public_provenance_is_denied(tmp_path, value):
    record = synthetic_records()[0]
    if value == "absent":
        record["provenance"].pop("public_safe")
    else:
        record["provenance"]["public_safe"] = value
    adapter = ExactReferenceAdapter.create(tmp_path / "provenance.sqlite")
    try:
        adapter.insert_batch([record])
        assert adapter.query([1, 0], {})["results"] == []
    finally:
        adapter.close()


@pytest.mark.parametrize("filters", [
    {"source; DROP TABLE objects;--": "SYNTHETIC_PRIVATE_CANARY_PAYLOAD"},
    {"source": "library' OR 1=1--"}, {"source": None}, {"evidence": None},
    {"evidence": "PROVEN_TRUTH"}, {"state": "promote"}, {"concept": None},
])
def test_unknown_or_malicious_filters_fail_closed_without_payload(store, filters):
    before = store.inspect_state()
    with pytest.raises(ContractError) as caught:
        store.query([1, 0], filters)
    assert str(caught.value) in {"invalid retrieval request", "unsupported filter value"}
    assert store.inspect_state() == before


@pytest.mark.parametrize("limit", [0, -1, True, 1.5])
def test_invalid_limits_fail_closed(store, limit):
    with pytest.raises(ContractError):
        store.query([1, 0], {}, limit)


@pytest.mark.parametrize("omitted", ["source", "evidence", "concept", "state"])
def test_negative_control_omitting_one_filter_is_detected(store, omitted):
    case = FIXTURE["cases"][0]
    weakened = dict(case["filters"])
    weakened.pop(omitted)
    with pytest.raises(AssertionError):
        assert_response(store.query([1, 0], weakened), case)


@pytest.mark.parametrize("mutation", [
    "lost-target", "duplicate", "private-result", "leaked-summary", "changed-evidence",
    "changed-rights", "changed-provenance", "promoted-direct", "truth", "rights-promotion",
    "evidence-promotion", "automated-acceptance",
])
def test_negative_control_response_corruption_is_detected(store, mutation):
    case = FIXTURE["cases"][0]
    response = store.query([1, 0], case["filters"])
    if mutation == "lost-target":
        response["results"].pop()
    elif mutation == "duplicate":
        response["results"].append(copy.deepcopy(response["results"][0]))
    elif mutation == "private-result":
        response["results"].append(public_projection(next(r for r in synthetic_records() if r["id"] == "synthetic:private")))
    elif mutation == "leaked-summary":
        response["summary"]["debug"] = "SYNTHETIC_PRIVATE_CANARY_PAYLOAD"
    elif mutation == "changed-evidence":
        response["results"][0]["evidence"] = "PROVEN_TRUTH"
    elif mutation == "changed-rights":
        response["results"][0]["rights_state"] = "UNRESTRICTED"
    elif mutation == "changed-provenance":
        response["results"][0]["provenance"]["record_id"] = "synthetic:wrong"
    elif mutation == "promoted-direct":
        response["results"][-1]["semantic_decision"] = "ACCEPT"
    else:
        key = {"truth": "truth_inference_allowed", "rights-promotion": "rights_promotion_allowed",
               "evidence-promotion": "scientific_evidence_promotion_allowed",
               "automated-acceptance": "automated_acceptance_allowed"}[mutation]
        response["policy"][key] = True
    with pytest.raises(AssertionError):
        assert_response(response, case)


def test_negative_control_second_vector_loss_is_detected(store):
    with store.db:
        store.db.execute("DELETE FROM vectors WHERE object_id=? AND ordinal=1", ("synthetic:multivector",))
    case = FIXTURE["cases"][0]
    with pytest.raises(AssertionError):
        assert_response(store.query([1, 0], case["filters"]), case)


def test_negative_control_edge_mutation_is_detected(store):
    before = store.inspect_state()
    protected = json.loads(before["protected"][0][1])
    assert protected["edges"][0]["accepted_edge"] is True
    assert protected["edges"][1]["accepted_edge"] is False
    protected["edges"][1]["accepted_edge"] = True
    with store.db:
        store.db.execute("UPDATE protected SET payload=? WHERE id=1", (json.dumps(protected),))
    with pytest.raises(AssertionError):
        assert store.inspect_state() == before


@pytest.mark.parametrize("relative", [
    "tests/fixtures/filtered-retrieval-continuity-v0.1.json",
    "tests/test_filtered_retrieval_continuity_v01.py",
    ".github/workflows/validate-retrieval-evidence-bridge-v078.yml",
])
def test_changed_files_pass_public_data_boundary(relative):
    spec = importlib.util.spec_from_file_location("continuity_boundary", ROOT / "scripts/check_public_data_boundary.py")
    boundary = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(boundary)
    assert boundary.validate_entry(relative, (ROOT / relative).read_text(encoding="utf-8")) == []


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in {"--reopen", "--check-missing"}:
        raise SystemExit("usage: test module --reopen|--check-missing SYNTHETIC_STORE")
    adapter = ExactReferenceAdapter(Path(sys.argv[2]))
    try:
        if sys.argv[1] == "--check-missing":
            try:
                adapter.query([1, 0], {})
            except MissingRequiredIndex as error:
                print(str(error))
            else:
                raise SystemExit("missing-index gate unexpectedly allowed retrieval")
        else:
            print(json.dumps([adapter.query(FIXTURE["query_vector"], case["filters"])
                              for case in FIXTURE["cases"]], sort_keys=True))
    finally:
        adapter.close()
