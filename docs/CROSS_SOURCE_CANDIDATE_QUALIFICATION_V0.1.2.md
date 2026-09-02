# Cross-Source Candidate Qualification v0.1.2

Status: review candidate for Issue #207

## Why this gate exists

The first provenance-compliant review batch correctly rejected all three proposals. That outcome showed that broad thematic proximity and generic words create review noise. Batch 2 must therefore use a stricter admission gate.

## Qualification rule

A proposed cross-source relationship may enter a review batch only when it has:

1. at least one direct anchor: an explicit stable identifier, exact full title, or explicit citation; **or**
2. at least two distinct corroborating anchors, such as a distinctive named entity plus a distinctive multi-token phrase.

Passing this gate never accepts a relationship. Every output remains an `INFERRED_CANDIDATE` with `REVIEW_REQUIRED` and `accepted_edge: false`.

## Signals that cannot qualify a candidate

- a single generic term such as “sacred,” “wisdom,” “consciousness,” “meaning,” or “magic”
- record or representation count
- a reverse edge
- a parent, descendant, or other graph-derived relationship
- private Drive identifiers, paths, filenames, or document-body content

## Epistemic boundary

Qualification means only “specific enough to review.” It does not mean true, scientifically supported, rights-cleared, canonically identical, or relevant after contextual review.

Automated truth inference, automatic acceptance, rights promotion, scientific-evidence promotion, canonical-identity promotion, and circular confidence amplification remain off.

## Batch 2 gate

Do not generate Batch 2 until this policy and its mutation tests pass review. If no records meet the threshold, the correct output is an empty candidate batch rather than weaker matching.
