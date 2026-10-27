# OMNI v0.5.0 provenance for the bounded v0.18 pilot

Recorded 22 October 2026, America/Los_Angeles. Reviewed against draft PR #413 at
`9382394d0a0ab5aa896613a1b8c7b5409bd22eea`; implementation checks must be rerun on
each later exact head. This is a first-party source-provenance review, not an
independent scientific assessment or release approval.

## Authority and version comparison

The authoritative public method is the publisher's
[v0.5.0 Public Review Specification](https://akashicnet.org/akashicomni/v0-5-0),
with its [overview](https://akashicnet.org/akashicomni) and
[researcher kit](https://akashicnet.org/akashicomni/research-kit). It names candidate
rc.4 A, publication on 1 October, method clarification on 2 October, availability
clarification on 7 October and a worked-example clarification on 12 October. The
served footer records a page-file change on 13 October. These are dated changes
within v0.5.0, not evidence of v0.5.1 or a software release.

| Baseline repository reference | Current inspected manual | Pilot consequence |
| --- | --- | --- |
| `docs/AKASHICOMNI_V050_PUBLIC_STATUS.md`, verified 7 October | Same method version, with later dated manual-use clarifications | Keep the document as a dated status reference, not the complete current specification. Its original foundation checksum is unchanged. |
| Twelve perspective identifiers in `scripts/research_integration_v018.py` | Same twelve identifiers; typographic separators differ for CUT | All names match after explicit separator normalization. This establishes identity mapping, not completed perspective appraisal. |
| `website/lib/akashicomni-method.ts`: ACTC described through agency, context, temporal order and candidate causes | ACTC described through conceptual coherence and explanatory relationships | Texts differ. Do not substitute the older repository role for the current component specification or infer equivalence. |
| Earlier retrieved-text SHA-256 `31de87154185e932b4c4205ae1e8c920d4f9263097f5644fccecfc0884d3ecd8` | Original served HTML independently captured and hashed | Preserve both representation identifiers. Earlier text bytes are unavailable for equivalence checking; a different hash is not evidence of semantic drift. |
| Pending twelve-perspective worksheet | DISCERN + DEEPEN, synthesis, coverage reasons, claim/source/revision records, counter-evidence and optional prompts/modules | The worksheet queues manual work. It does not execute the complete method, authenticate reviewers or establish scientific conclusions. |

The full-reading requirement remains twelve analytical dispositions with reasons;
synthesis is an output. Optional DARK, QM/MM/PP and inquiry prompts do not silently
change the baseline. Unavailable component material is insufficient information,
not evidence of irrelevance. Internal convergence is not independent evidence.

## Verified representations

[`method-provenance.json`](../references/integration/v018/omni/method-provenance.json)
contains the URLs, retrieval timestamps, HTTP status, response representation,
byte lengths and SHA-256 values for **11 original first-party HTTP bodies**:
the manual, overview, researcher kit, three starter downloads, AWAKEN, ADAPT001,
REGENERATE000, TRANSCEND001 and HIERATIC Book I editorial edition 1.1 PDF.
Requests were unauthenticated and requested identity content encoding. All returned
200 at their declared URL. No error body was accepted as a manual.

The original manual body is 110,871 bytes, SHA-256
`dca4484d7572ff81050a7da21eb16eecbf84fe2d3684478f38fcb797784d3953`.
It and the three starter downloads are bundled under the same `omni/` directory.
The HTML retains the original served bytes, including shared page markup. It is
not a normalized-text export or a complete, offline-renderable website bundle.
The other seven HTTP bodies are described by their pins but are not vendored.

All **15 selected source-blob pins** from the earlier source-pin review were
independently retrieved through an authorized Sites source checkout and rehashed.
The manifest records Git blob SHA, SHA-256 and byte length. The selected blobs are
identical at source commits `79f1087bdcda4f3f832f0e76b7a694f4e47fcf7a` (saved version
1087) and `afa553074bf4552684564cbd3aeea0bd33b7f2c7` (saved version 1090).
The latter version's deployment receipt reports success. This is a source-to-version
association; it is not a claim that TSX and served HTML have identical bytes.
The archive hash remains explicitly provider-reported, not recomputed.

The source pins cover the manual/overview, method/release descriptions, researcher
kit/content, three starter files, four component entry pages, TRANSCEND content
JSON and HIERATIC PDF. The three HTTP starter files and PDF match their respective
source-blob SHA-256 values exactly. Selected source pins are not a full dependency
or build lock. Public visibility and byte identity do not confer publication rights
over the pilot's research sources.

## Component specifications still requiring original bytes

The captured manual's component register supplies these versioned reference
bundles. Exact original and addendum URLs are retained in the manifest and checked
against the captured HTML; none was fetched live from Reddit.

| Component | Original | Recorded clarification | Original/addendum byte status |
| --- | --- | --- | --- |
| ACTC | v2.0 | v2.0.1 | Both pending authorized archived bytes |
| METAD | v2.1 | v2.1.1 | Both pending authorized archived bytes |
| UMASC | v7.2 | v7.2.1 | Both pending authorized archived bytes |
| CUT | v4.0.3 | v4.0.4 | Both pending authorized archived bytes |
| HOMESENSE700 | Working Draft v1.1 | Working Draft v1.1.1 | Both pending authorized archived bytes |
| PP | v1.0 nested draft | v1.0.1 within ACTC addendum | Both pending authorized archived bytes |
| QMM | Community interpretation | Dated attribution correction | Both pending authorized archived bytes |

Seven rows contain fourteen reference entries and **thirteen distinct URLs**;
ACTC and PP share one addendum URL. The manual reports six clarification
publication units. This is publication history, not fresh verification of live
comments or fourteen independent sources. Neither archive URL metadata nor a site
entry page substitutes for the missing original/addendum representation.
HOMESENSE809 does not replace the HOMESENSE700 charter. A book edition, phase
number or series number is not one version identifier for a whole framework.

To complete these pins, obtain authorized archived post/comment representations;
record their original URL/comment ID, capture date, access scope, exact bytes and
checksum. Preserve their status as archived representations. Do not assert that
they establish current live content or silently lift live Reddit HOLD. Reconcile
the inspected component versions and passages with the declared manual before
requesting human acceptance of the method-pin gate.

## Reproduce without publication or deployment

From the exact GitHub PR checkout:

```bash
python scripts/verify_omni_method_pins_v018.py
python -m pytest -q tests/test_research_integration_v018.py tests/test_search_reddit_archive.py tests/test_bq001_public_status_boundary.py tests/test_omni_method_pins_v018.py
```

Default verification is offline: it verifies the lock-to-manifest checksum, four
bundled bodies, the component register and the twelve perspective identities.
Its output distinguishes described external pins from bytes actually rechecked
in that invocation. No method/research/release gate becomes complete.

To verify the 15 source blobs, use an independently authorized checkout containing
the recorded commit and its blobs. No credentials belong in this repository:

```bash
python scripts/verify_omni_method_pins_v018.py --sites-checkout /path/to/authorized/sites-checkout
```

The verifier uses `git show` at the manifest's exact commit, never the checkout's
current HEAD. Missing objects, changed bytes or a missing repository fail. It does
not mint credentials, change refs, commit, push or deploy.

Optional public refetch checks must be explicit and outside offline CI. Run the
offline verifier first, then capture only the listed first-party URLs into a new
directory outside the checkout. This example refuses differing bytes and never
fetches a registered Reddit URL:

```bash
python - /tmp/omni-v050-captures <<'PY'
import hashlib, json, pathlib, sys, urllib.request
root = pathlib.Path(sys.argv[1]); root.mkdir(parents=True, exist_ok=False)
m = json.loads(pathlib.Path('references/integration/v018/omni/method-provenance.json').read_text())
for pin in m['http_assets']:
    assert pin['url'].startswith('https://akashicnet.org/')
    request = urllib.request.Request(pin['url'], headers={'Accept-Encoding': 'identity'})
    with urllib.request.urlopen(request, timeout=30) as response:
        assert response.status == 200 and response.url == pin['url']
        raw = response.read()
    assert len(raw) == pin['size_bytes'], pin['id']
    assert hashlib.sha256(raw).hexdigest() == pin['sha256'], pin['id']
    (root / pin['capture_filename']).write_bytes(raw)
PY
python scripts/verify_omni_method_pins_v018.py --capture-directory /tmp/omni-v050-captures
```

URLs are mutable. Shared markup may change even when the method prose does not.
A failed refetch is recorded as access failure or representation drift; retain
the old pin and investigate. Never accept an error page, normalize away a mismatch
or automatically replace the expected hash. A fresh capture needs a dated,
reviewable inventory update. Historical text equivalence, complete original
component bundles and full dependency/build reproduction remain separate gaps.

The baseline 74 tests were rerun against files verified from `9382394…`.
The follow-up adds 14 adversarial provenance cases and byte verification of all
11 public captures and 15 selected source blobs. Current-head CI evidence belongs
in PR #413 and issue #411; old successful checks do not validate a new commit.

## Release-readiness consequence

Only the original HTML snapshot pin is now complete. The aggregate method and
component-pin gates remain incomplete. PR #413 remains draft, BQ001 remains
UNRESOLVED, its real projection remains HOLD with no cleared source records or
review content, and v0.18 remains PLANNED / not release-ready. Full primary access,
scope-specific rights/cultural decisions, genuine human appraisal, authenticated
review, independent review and separate release approval remain outstanding.
No merge, tag, deployment, accepted edge or promotion control changes here.

## Component Archive Follow-Up · 27 October 2026

PR #413 was still draft and unchanged at `9ed741ced3fdf4338abdd988367368df6bd238c8`
when this follow-up began. The earlier 88-test/16-check receipt remains historical.
The integration adapter, pinned packet, foundation pins, original manual and
starter bytes were not changed by this follow-up.

[`component-archive-review.json`](../references/integration/v018/omni/component-archive-review.json)
records a bounded search of preserved first-party audit/publication packages,
the candidate specification, the larger Reddit metadata archive, connected Drive
and two public search indexes. No direct live Reddit or Reddit API retrieval was
performed. No complete original or clarification representation was recovered.
Internet Archive CDX requests for all six original post URL prefixes were
inaccessible through available retrieval; capture existence remains unknown.
Other archive providers and authorised private backups were not exhausted.
This is not an exhaustive census of every possible archive.

One package contains `patches-pinned-20260928.jpg`: a **partial** ACTC v2.0.1
screenshot, 132,193 bytes, SHA-256
`17f0c45efac072e1d9b9611357c5be8d9c8db6475e760a7cadab13a9757c17fe`.
The heading and visible QM/MM/QMM distinctions are consistent with the manual's
scoped naming and non-equivalence rules. This does not establish the unseen
remainder or PP clarification. The URL is not visible, the bottom is cut off and
there is no EXIF or absolute capture time. Its attribution to the shared ACTC/PP
locator depends on the accompanying narrative receipt. The filename's September
date, ZIP member's 1 October local timestamp and provider's 1 October package
creation metadata are different kinds of evidence; none independently
authenticates the source's capture time, publication time or edit history.

The package's SHA-256 is
`31f67efa8c24900abaf4d5d0342609cb30632b7c9169bd0c901fae812bd62d4b`.
The review records exact byte lengths and checksums for this container, its
partial image, the rc.4 A candidate, the applied-addendum receipt, the earlier
component audit and the larger metadata archive. These are **supporting artifact
pins, not original Reddit source pins**. The archive has six matching original
post IDs, all with null stored titles and summaries, and no post/comment bodies.
The prior reports describe publication and inspection but do not preserve the
complete published source representations. Prepared draft wording is not proof
of what was published.

### Exact Outstanding Dependencies

The machine-readable inventory deduplicates the shared comment while retaining
both component/version bindings. All rows below remain
`PENDING_AUTHORIZED_ARCHIVED_BYTES`, with null original-source checksums.

| Dependency | Component / Declared Version | Preserved Support / Missing Source |
| --- | --- | --- |
| `t3_1uld5ws` | ACTC v2.0 | Candidate and metadata only; full original absent |
| `t1_pcjwo7y` | ACTC v2.0.1 and PP v1.0.1 | Partial ACTC screenshot and receipt; complete shared comment including PP absent |
| `t3_1ukdnzu` | METAD v2.1 | Candidate and metadata only; full original absent |
| `t1_pcjx6eb` | METAD v2.1.1 | Narrative receipt only; full addendum absent |
| `t3_1uk9qdp` | UMASC v7.2 | Candidate and metadata only; full original absent |
| `t1_pck0cro` | UMASC v7.2.1 | Narrative receipt only; full addendum absent |
| `t3_1nlqn3o` | CUT v4.0.3 | Candidate and metadata only; full original absent |
| `t1_pck0jk6` | CUT v4.0.4 | Narrative receipt only; full addendum absent |
| `t3_1ul49l9` | HOMESENSE700 Working Draft v1.1 | Candidate and metadata only; full charter absent |
| `t1_pck09dt` | HOMESENSE700 Working Draft v1.1.1 | Narrative receipt only; full addendum absent |
| `t1_ovc6qyw` | PP v1.0 nested draft | Candidate/receipt context only; full nested comment absent |
| `t3_1peyo0j` | QMM community interpretation | Candidate and metadata only; full interpretation absent |
| `t1_pck0vdo` | QMM dated attribution correction | Narrative receipt only; full correction absent |

For **each** dependency, the outstanding input is a legitimately retained,
complete representation tied to the exact post/comment, with capture time and
version evidence, reproducible checksum, scope-specific permission and a
retention/deletion/suppression plan. Do not recover material from an unauthorised
copy or bypass a deletion. A current capture, if separately authorised, would be
a new representation with its own date and rights review, not historical proof.
Do not infer ownership or perpetual storage rights from moderator access,
public visibility, a previous receipt or a checksum. If deletion or a retention
restriction is established, suppress the affected representation and invalidate
dependent verification; an immutable Git copy cannot implement that lifecycle.
Raw copies and the screenshot are therefore **not added to public Git**.

All fourteen declared version/URL bindings and seven scope labels were reconciled
with the unchanged manual register and earlier rc.4 A candidate. Complete source
semantics remain unverified for all seven components. ACTC remains conceptual
axioms, METAD architecture/attribution and UMASC classification without empirical
equivalence. CUT's three temporal views remain a subset; HOMESENSE700 remains
charter context distinct from Phase 8; PP remains optional; QMM has no established
PP bridge. This is consistency of the declared integration contract, not a full
component compatibility pass or independent scientific appraisal.

### Reproduce The Follow-Up

The existing offline verifier now checks the checksum chain from input lock to
method manifest to archive review, all thirteen dependency identities and fourteen
bindings, partial-capture boundaries and unchanged HOLD classifications. It also
rejects attempted source/rights/time/independence promotion and source payloads
inserted into dependency records. CI needs no private source content or network.

The optional command below rechecks the five supporting artifact bodies and
the partial image directly within its ZIP. The directory must be outside the
checkout and contain the exact filenames listed in the review. Missing or changed
bytes fail; nothing is fetched, copied, written or promoted by this check:

```bash
python scripts/verify_omni_method_pins_v018.py
python scripts/verify_omni_method_pins_v018.py --private-component-evidence-directory /path/to/authorised/preserved-artifacts
python -m pytest -q tests/test_research_integration_v018.py tests/test_search_reddit_archive.py tests/test_bq001_public_status_boundary.py tests/test_omni_method_pins_v018.py
```

An offline run reports zero supporting bodies rechecked; the optional private
run reports five. Both report **zero complete original component references**,
thirteen pending dependencies and incomplete component/method gates. Input
permission for task inspection does not grant redistribution or new permanent
retention. Existing private artifacts remain subject to their own lifecycle;
this verifier is not a deletion monitor or retention service.

The follow-up adds 22 regression cases to the inherited 88 tests (110 total).
Validation applies to the exact changed files and later CI head reported in the
draft PR; it does not reopen or repeat the completed integration implementation.
Human appraisal, rights/cultural decisions, independent review and separate
release approval remain outstanding. BQ001 stays UNRESOLVED, public output HOLD,
v0.18 PLANNED / not release-ready and PR #413 draft and unmerged.
