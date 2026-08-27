# Multidimensional Framework Registry

`framework-registry.json` is the canonical, machine-readable catalogue of named
frameworks, models, methodologies, protocols and meta-frameworks in AkashicNET.
The initial file is a **curated seed**, not a complete archive-derived inventory.
Its record count must not be interpreted as confirmation of any provisional
estimate for the wider ecosystem.

## Model

- `frameworks` contain stable IDs, descriptive metadata, zero or more explicitly
  documented versions, aliases, extensible domains, provenance references and an
  overall evidence-confidence classification.
- `relationships` are first-class, independently sourced records. Supported types
  are `derived_from`, `supersedes`, `superseded_by`, `fork_of`, `merged_from`,
  `inspired_by`, `overlaps_with`, `supports`, `contradicts`, `depends_on`, and
  `part_of`. The validator never infers inverse relationships.
- `source_records` distinguish `reddit_archive`, `google_drive_metadata`,
  `research_evidence_layer`, `manual_akashicnet_record`, and extensible `other`
  provenance. A locator identifies the record without claiming that unreviewed
  archive material supports a framework.
- `claims` reserve claim-level confidence and provenance inside each framework.
  Claims can therefore be classified separately as the registry is enriched.

`first_seen_date` and `latest_version` may be `null`. Unknown dates and versions
must remain unknown rather than being guessed. Aliases remain aliases and versions
remain explicit version records; neither is silently merged into a canonical item.

## Epistemic boundary

Allowed confidence values are `strong`, `moderate`, `emerging`, and `speculative`.
Confidence applies only to the record or claim where it appears. In particular,
personal experience, synchronicity, visionary accounts, symbolic material and
community observations are not automatically scientific evidence. A strong
confidence that a project is documented does not establish every proposition
catalogued by that project.

Domains are free-form strings so future curation can add or refine domains without
a schema migration. Validators enforce structure and references, not a fixed
domain vocabulary.

## Validation

Run:

```bash
python -m tools.framework_registry.validate
```

The validator reports all detected errors, including duplicate stable IDs,
cross-record name/short-name/alias collisions, malformed dates, invalid enum
values, unresolved provenance or relationship references, self-relationships,
unrepresented latest versions, duplicate versions and count drift. It returns a
non-zero status on failure.

## Curation workflow

1. Establish a source record without fabricating authorship, dates or evidence.
2. Add a framework using a stable lowercase `fw-...` ID. Leave unknown values null.
3. Add versions and aliases explicitly rather than rewriting older identity.
4. Add only relationships supported by cited source records.
5. Classify each record, relationship and later each claim on its own evidence.
6. Run the validator and tests before review.

Discovery and archive-wide counting are future work. `generated_count` currently
checks internal seed-file consistency only; `count_status` makes that limitation
machine-readable.
