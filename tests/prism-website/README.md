# PRISM review-only website harness

`npm ci --prefix tests/prism-website --ignore-scripts --no-audit --no-fund`

`tests/prism-website/node_modules/.bin/playwright install --with-deps chromium`

`npm run check --prefix tests/prism-website`

This harness copies the repository snapshot into a temporary directory, builds
and type-checks the six PR surfaces (home, About, OMNI, FAQ and both PRISM
articles) using pinned Next/React/TypeScript dependencies, then serves the result
only on loopback. It runs Chromium checks on FAQ and the two PRISM articles at
1440, 821, 768 and 390 pixels: page overflow, runtime errors, heading/landmark
counts, accessible ID references, images, internal links and fragments, FAQ
keyboard expansion, diagram keyboard scrolling and its text equivalent. It
blocks browser requests outside loopback. No deployment or artifact upload runs.

Built destinations receive HTTP and rendered-fragment checks. Unchanged routes
outside the six-page build receive repository route/fragment existence checks.
This is bounded automated coverage, not a complete accessibility audit, source
read, cultural review, evidence adjudication, gate approval or release check.

The snapshot lacks its imported vendored stylesheet. The harness supplies
`shadcn@4.13.0`'s `dist/tailwind.css` and MIT license in the temporary directory;
both match the npm tarball byte-for-byte. CSS SHA-256:
`bc7d83425702955b4cb67cb14ede9d603f9d912376d57a2d81d661094d2a782a`.
Tailwind and animation packages are pinned in the lockfile. Production source is
not substituted or edited during the test.

The existing toroidal logo is manifest-only and absent from this repository;
that one known inherited missing binary is excluded from the asset check. New
PRISM assets must resolve. No external logo or withheld artwork is recovered or
published by this harness.

A whole-snapshot build was attempted during reconciliation and failed on two
unchanged routes: a nonlocal `*` selector in
`app/akashic-symbiosis/symbiosis.module.css` and a duplicate `ResonanceCipher`
import in `app/metta-awareness/page.tsx`. These remain outside PR #379's bounded
surface verification; this harness does not claim a full-site build passes.
