# Reddit corroboration topic audit — v0.7.15

The complete corroboration seed series v0.3–v0.6 was audited record by record.

Every record contains exactly two fields: `subreddit` and `post_id`. There are no topic, category, flair, `link_flair_text`, or `link_flair_template_id` fields.

Lineage is cumulative through v0.5: 20 → 29 → 38 records. Version 0.6 contains 39 records but is a replacement transition, adding five IDs and removing four. This distinction is now tested rather than describing v0.6 as a one-record append.

**Decision:** public-presence corroboration is not topic evidence. No topic is promoted and the public-safe top-level count remains **73**. Truth, rights, and scientific-evidence promotion remain off.
