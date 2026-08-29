# Drive pagination audit discrepancies — 2026-08-29

Workflow run: `33246765815`
Job: `99085478537`
Head SHA: `a99d21c8e395f750a07bd51be508ac5dbaad6d82`

## Result

The credential-backed raw Google Drive API audit executed against the frozen **195-node** denominator.

- audited nodes: **195**
- unique Drive IDs: **195**
- PASS: **178**
- FAIL: **17**
- ERROR: **0**

Therefore `PAGINATION_AND_TERMINALITY_AUDIT` remains **0 / 2**. The gate must not be awarded until the discrepancies below are reconciled and a subsequent full audit returns 195 PASS / 0 FAIL / 0 ERROR.

## Discrepancies

| Scope | Collection | Expected docs | Observed docs | Expected child folders | Observed child folders |
|---|---|---:|---:|---:|---:|
| root | Aura + Astral Bodies | 5 | 6 | 0 | 0 |
| root | Metaphysics | 100 | 127 | 2 | 2 |
| root | Occultism | 6 | 6 | 0 | 3 |
| root | Buddhism | 100 | 357 | 15 | 16 |
| descendant | Hinduism/Supermundane – The Inner Life | 0 | 1 | 0 | 0 |
| descendant | Ancient Religions/Sacred Texts | 10 | 11 | 0 | 0 |
| descendant | PDF/Aleister Crowley | 10 | 11 | 0 | 0 |
| descendant | PDF/Alice A. Bailey | 26 | 27 | 0 | 0 |
| descendant | PDF/Montalk | 13 | 6 | 1 | 1 |
| descendant | PDF/Author Avalon/Reference Material | 0 | 1 | 0 | 0 |
| descendant | Islam/In The Shade Of The Qur’an | 14 | 15 | 0 | 0 |
| descendant | Magick/Ceremonial Beginners | 22 | 20 | 2 | 2 |
| descendant | Alchemy/Jean Dubuis | 2 | 3 | 3 | 3 |
| descendant | Alchemy/Jean Dubuis/Mineral Alchemy | 4 | 5 | 0 | 0 |
| descendant | Theosophy/Annie Besant | 3 | 4 | 0 | 0 |
| descendant | Theosophy/Blavatsky | 8 | 9 | 0 | 0 |
| descendant | Theosophy/Leadbeater | 6 | 7 | 0 | 0 |

## Interpretation

This run proves that the access token and raw API execution path are functioning. The remaining failures are census/content discrepancies, not authentication or denominator failures.

Several one-object increases may be non-document technical artefacts because the raw audit currently counts every non-folder child as a document. These require MIME-aware reconciliation before changing the authoritative document denominator.

Two results are structurally significant and must not be explained away by technical exclusions without evidence:

- `Metaphysics`: 127 non-folder children observed versus 100 in the frozen census.
- `Buddhism`: 357 non-folder children and 16 child folders observed versus 100 documents and 15 folders in the frozen census.
- `Occultism`: three child folders observed where none were recorded.

`PDF/Montalk` also confirms that the historical parent direct-document count of 13 is inconsistent with the raw audit observation of 6 direct non-folder children plus one child folder, reinforcing the earlier Montalk double-count correction.

## Next reconciliation step

For each failed node, enumerate direct children with `id`, `name`, and `mimeType`, classify folder versus usable document versus technical artefact, and persist the corrected counts. New child folders must be traversed recursively and added to the topology before the frozen denominator can be re-established.

After reconciliation, rerun the full raw API audit. Only a result of **195/195 PASS, 0 FAIL, 0 ERROR** (or a formally revised, evidence-backed denominator if new nodes are confirmed) may earn Gate 3.
