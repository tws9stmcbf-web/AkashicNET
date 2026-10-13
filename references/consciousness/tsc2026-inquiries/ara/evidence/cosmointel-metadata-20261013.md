# Cosmointel Metadata Inspection
Checked 13 October 2026. Bounded inspection, not a site-wide crawl or study validation.

## Raw HTML: homepage and founder page
Sources: https://cosmointel.com/ and https://cosmointel.com/about-founder/
Extracted from publicly returned HTML using a standard-library HTML parser.

- JSON-LD types on both pages: Organization, WebPage, WebSite, BreadcrumbList.
- Organisation name: Cosmointel inc.; description: Sciencefact Research Center.
- Canonical URLs match the two source URLs.
- Languages advertised by hreflang: English and Persian.
- X/Twitter metadata: @cosmo_intel.
- sameAs: https://www.facebook.com/cosmointel/ ; https://twitter.com/cosmo_intel ; https://www.instagram.com/cosmo.intel/ ; https://www.youtube.com/c/MohammadAliTaheriOfficial
- RSS discovery: https://cosmointel.com/feed/
- Public JSON page endpoints advertised: https://cosmointel.com/wp-json/wp/v2/pages/6138 and https://cosmointel.com/wp-json/wp/v2/pages/5576 . Endpoints discovered, not tested.
- Open Graph image: https://89a70ac4.delivery.rocketcdn.me/wp-content/uploads/2020/05/share2.jpg ; advertised dimensions 600 × 314. Image rights not determined.
- Homepage JSON-LD datePublished: 2019-03-08T21:25:53+08:00; dateModified: 2026-06-03T16:54:38+08:00.
- Founder JSON-LD datePublished: 2020-02-23T07:51:14+08:00; Open Graph article:published_time: 2020-02-23T07:51:14+00:00. These disagree by eight hours; retain both.
- Founder JSON-LD dateModified: 2026-03-12T20:13:54+08:00; Open Graph article:modified_time: 2026-03-12T12:13:54+00:00. These are the same instant.
- HTTP Last-Modified: homepage Tue, 13 Oct 2026 02:15:28 GMT; founder Tue, 13 Oct 2026 07:04:33 GMT. These headers may describe generated/cached representations and should not replace editorial dates.
- WordPress and SEO/page-builder generator tags are present. No Person or ScholarlyArticle node observed in these two pages' JSON-LD. This does not describe the rest of the site.

## Public organisational and research metadata
Contact page https://cosmointel.com/contact/ lists a Vaughan, Ontario, Canada office.
AI Search page https://cosmointel.com/cosmointel-ai-search/ advertises discovery across its articles, papers, concepts and pages with links to original sources. Search effectiveness was not tested.

Current OJS About page https://journalofcosmointel.com/index.php/journalofcosmointel/about states establishment in 2022, ISSN 2817-6995, and internal committee review rather than traditional peer review. The same policy appears at https://www.journalofcosmointel.com/en/about/ . This is the journal's own policy disclosure, not an independent assessment of any paper.

Example article: https://journalofcosmointel.com/index.php/journalofcosmointel/article/view/218
Title: Differential Effects of the Faradarmani Consciousness Field on Cell Cycle Progression of Lymphoma Raji Cells Under Clinostat-Simulated Microgravity and Earth Gravity Conditions.
Authors: Mohammad Ali Taheri, Sara Torabi, Zahra Hajebrahimi, Farid Semsarha.
DOI: 10.61450/joci.v4i18.218; article date: 2025-09-25; volume 4, issue 18, pages 11–19.
Issue page https://journalofcosmointel.com/index.php/journalofcosmointel/issue/view/39 gives 2025-09-27. Main-site announcement gives 2025-10-10. These are different publication events, not automatically inconsistent.
Only article metadata and abstract were read; no full-paper methods or data audit.

Submission policies https://journalofcosmointel.com/index.php/journalofcosmointel/about/submissions assert restrictive republication rights. Free reading does not establish a reuse licence.

## Candidate integration
Capture source URLs, exact metadata strings, source-reported timestamps, organisation/account identities and per-article DOI/author records. Keep internal review, independent replication and source reliability as separate fields. No scheduler created, no research evidence promoted, no journal figures or papers republished.
