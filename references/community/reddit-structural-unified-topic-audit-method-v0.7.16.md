# Reddit structural and unified-index topic audit — v0.7.16

The Reddit corpus structural checkpoint and unified-index rebuild were cross-audited at every JSON nesting level.

Validated arithmetic:

- 9,502 Reddit source rows + 2,657 Drive rows = 12,159 unified records.
- 9,401 previous Reddit rows + 2,657 Drive rows = 12,058 previous unified records.
- Both views reconcile to a net increase of 101.
- The structural checkpoint separately reports 7,457 unique Reddit post IDs and canonical post URLs after annotation-aware deduplication.

No topic, category, flair, `link_flair_text`, or `link_flair_template_id` key appears at any level.

**Decision:** aggregate counts and provenance metadata are not topic evidence. No topic is promoted; the public-safe top-level count remains **73**. Truth, rights, and scientific-evidence promotion remain off.
