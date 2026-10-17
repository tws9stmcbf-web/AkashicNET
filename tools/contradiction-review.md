# Contradiction review tool

Status: experimental research utility; not scientifically validated.

Use this tool to triage explicitly nominated pairs of research claims. It produces
a bounded review queue with source passages, study context and proposed next tests.
It does not discover contradictions automatically, verify sources, update the
knowledge graph, or publish results.

## Run from the repository root

Python 3.10+; standard library only; no network, API key or package installation.

```bash
python scripts/review_contradictions.py examples/contradiction_review_input.json --budget 5
python -m unittest discover -s tests -p 'test_contradiction_review.py' -v
```

The example is synthetic. Output goes to stdout; redirect it to a local working
file if needed. Retain private source material locally. The output includes the
input claims and passages and is not automatically safe to publish.

## Input contract

- `claims`: unique nonempty `id`, `text`, optional `sources` list of objects with
  `ref` and exact `passage`, optional `scope` object.
- Scope fields: `population`, `conditions`, `definition`, `time`. Missing or empty
  fields remain unknown. Use a documented `not_applicable` label only when justified.
- `pairs`: two distinct known claim IDs under `claims`, plus optional `next_test`.
  Nominate pairs deliberately; duplicate pairs, including reversed pairs, fail.
- `--budget`: nonnegative integer limiting emitted review items. It does not bound
  externally performed research or parsing of the supplied file.

The tool prioritizes missing source anchors, differing scope, missing context, then
candidate conflicts. IDs break ties deterministically. Reordering claims/pairs
does not change the queue. `deferred` reports items beyond the budget.

Matching scope labels only permits semantic review; it does not prove contradiction.
Different study populations or definitions may explain a disagreement. Compare
methods, estimates and uncertainty before treating findings as incompatible.
The helper checks field presence, not source authenticity, evidence strength,
independence or quotation accuracy. It assigns no confidence or truth scores.

## Research workflow

1. Extract claims with original passages and contextual labels.
2. Nominate apparently conflicting pairs and run the bounded queue.
3. Verify sources and resolve missing context before interpreting disagreement.
4. Record a prediction and specify what outcomes would favor each explanation.
5. Perform one discriminating test within a stated action budget.
6. Preserve unresolved alternatives, with evidence-based differences in support.
   Stop when no new information is available or the budget is exhausted.

Output uses `REVIEW_PACKET_ONLY`; automated acceptance, truth promotion, rights
promotion, scientific evidence promotion and publication are disabled. These fields
describe this utility's boundary; they are not evidence of rights clearance or a
replacement for existing AkashicNET validators and human adjudication. No direct
graph/retrieval ingestion or production website integration is provided.

## Optional quantum cognition illustration

```bash
python scripts/quantum_order_demo.py --state 0 --a 0 --b 45
```

This isolated two-dimensional projective probability example compares A-then-B
with B-then-A, aligning both joint tables to A rows and B columns. Angles are in
degrees. It reports total variation and a QQ residual, not significance or accuracy.
It is opt-in and never feeds the review queue or evidence ranking.

Quantum cognition models contextual judgments mathematically. This example does
not establish a physical quantum mechanism, consciousness, or benefit to AkashicNET.
Before using it predictively, compare held-out order-counterbalanced data against
classical context-sensitive models under matched complexity. Holding several
hypotheses open is not, by itself, quantum cognition.

## Provenance and evaluation

Independently authored following Jennifer Prendki's TSC 2026 presentation and the
AkashicNET framework discussion; no Dyssonance code copied and no CRUU implementation
claimed. The review workflow has deterministic software tests, not empirical proof
of improved scientific reasoning.

- Talk: https://tsc2026.org/abstracts_html/jennifer-prendki.html
- Quantum question-order research: Wang et al. (2014),
  https://doi.org/10.1073/pnas.1407756111
  (successive questions without intervening new information are an assumption).

Evaluate on a fixed, independently reviewed claim set using matched sources and
research budgets: source fidelity, genuine/apparent contradiction discrimination,
appropriate uncertainty, useful next tests and cost. Treat improved internal
consistency separately from improved factual accuracy.
