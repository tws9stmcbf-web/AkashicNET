# Semantic link candidates v0.2.0

This stage proposes a small, review-only set of literal links between approved public-safe endpoints and audited topic endpoints.

The generator recognizes only one relationship: `LABEL_CONTAINS_EXACT_TOPIC_TERM`. It means that a publication, framework, question, or evidence-record label contains a topic label as an exact normalized token sequence. It does not mean the source is broadly about the topic, supports the topic, or proves any claim.

## Permanent controls

- Every proposal is `INFERRED_CANDIDATE`, `REVIEW_REQUIRED`, and `accepted_edge: false`.
- `accepted_edges` remains empty.
- Topic terms shorter than four characters are excluded to avoid acronym collisions such as `Art` in `S-ART`.
- More than 25 candidates fails closed instead of truncating or silently expanding review scope.
- Fuzzy similarity, embeddings, graph proximity, transitive inference, representation counts, confidence aggregation, and prior candidate output are prohibited.
- Source and topic endpoints must originate from different public-safe artifacts.
- Automated truth inference and acceptance remain off.
- Scientific-evidence, rights, and canonical-identity promotion remain off.
- Private Drive metadata and circular confidence remain prohibited.

The generated packet is committed only through a draft, packet-only pull request. The repository owner must review every proposal and apply `human-reviewed`; this approves only mechanical storage of the proposal packet and does not accept any graph edge.
