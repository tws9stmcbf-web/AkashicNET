#!/usr/bin/env python3
import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = ROOT / "website/app/page.tsx"
PROGRESS = ROOT / "website/app/development-progress/page.tsx"
PUBLIC_APP = ROOT / "website/app"


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


for path in (HOME, PROGRESS):
    if not path.is_file():
        fail(f"missing required surface: {path.relative_to(ROOT)}")

home = HOME.read_text()
progress = PROGRESS.read_text()

for token in (
    "v0.15",
    "SEALED BASELINE",
    "v0.16.0-beta.2",
    "GOVERNED CANDIDATE",
    "v0.16.7",
    "SITE CHECKPOINT",
    "BQ001 remains UNRESOLVED",
):
    if token not in progress:
        fail(f"development record missing governed status token: {token}")

for token in (
    "Public Beta",
    "v0.15 sealed",
    "v0.16.0-beta.2 governed candidate",
    "v0.14.0-beta.1",
    "Automation & Reproducibility Beta",
    "READY / SEALED",
    "2 September 2026",
    "Historical sealed release checkpoint",
):
    if token not in home:
        fail(f"homepage missing required current-or-historical token: {token}")

# Inspect text across inline JSX tags, while keeping separate source lines apart.
# This is a bounded status-copy guard, not a general JSX or natural-language parser.
def status_text(source: str) -> str:
    return unescape(re.sub(r"<[^>]*>", " ", source)).replace("’", "'")


product_status = re.compile(
    r"\bAkashicNET\b(?:'s)?"
    # Accept ordinary connective words, but stop at independently versioned names.
    r"(?:[ \t,·:–—-]+(?!(?:METAD|ACTC|UMASC|MultidimensionalCUT|AkashicOMNI|BQ\d+)\b)[a-z]+)*"
    r"[ \t,·:–—-]*(?:Pre-alpha|Public Beta|v\d+\.\d+(?:\.\d+)?(?:-[\w.]+)?)\b|"
    r"(?:Pre-alpha|Public Beta)[ \t,·:–—-]*AkashicNET\b|"
    r"\bv\d+\.\d+(?:\.\d+)?(?:-[\w.]+)?[ \t]+(?:is[ \t]+)?"
    r"(?:AkashicNET(?:'s)?[ \t]+(?:current[ \t]+)?(?:product[ \t]+)?version\b|"
    r"(?:the[ \t]+)?(?:current[ \t]+)?(?:product[ \t]+)?version[ \t]+of[ \t]+AkashicNET\b)",
    re.IGNORECASE,
)
pre_alpha = re.compile(
    r"\bAkashicNET[^\n<]{0,40}Pre-alpha|"
    r"Pre-alpha[^\n<]{0,40}AkashicNET\b",
    re.IGNORECASE,
)
allowed_product_status_surfaces = {HOME.resolve(), PROGRESS.resolve()}
for surface in PUBLIC_APP.rglob("*.tsx"):
    visible = status_text(surface.read_text())
    if pre_alpha.search(visible):
        fail(f"contradictory current Pre-alpha status: {surface.relative_to(ROOT)}")
    if surface.resolve() not in allowed_product_status_surfaces:
        if product_status.search(visible):
            fail(
                "product status must remain centralised on the homepage checkpoint "
                f"and development record: {surface.relative_to(ROOT)}"
            )

# The homepage has one linked current-product label; the sealed snapshot is historical.
links = re.findall(r'<a\b[^>]*href="/development-progress"[^>]*>(.*?)</a>', home, re.S)
current_label = "Public Beta · v0.15 sealed · v0.16.0-beta.2 governed candidate"
if len(links) != 1 or current_label not in status_text(links[0]):
    fail("homepage must have one linked current-product checkpoint")
if (home.count("Public Beta") != 1 or home.count("v0.16.0-beta.2") != 1
        or "v0.16.7" in home):
    fail("duplicate current-product homepage status")

# Enforce status and limitation together in the governed checkpoint records.
for version, status, limitation in (
    ("v0.16.0-beta.2", "GOVERNED CANDIDATE", "not a sealed release"),
    ("v0.16.7", "SITE CHECKPOINT", "not a release"),
):
    record = re.search(
        r'\["' + re.escape(version) + r'",\s*"' + status + r'",\s*"([^"\n]+)"\]',
        progress,
    )
    if not record or limitation not in record.group(1):
        fail(f"missing candidate/checkpoint limitation: {version}")
if "progress toward v0.17.0" not in status_text(progress):
    fail("site checkpoint must describe progress toward v0.17.0")

# Check each predicate separately so negation of an unrelated noun or earlier
# predicate cannot hide a later affirmative assertion. This remains a bounded
# status-copy guard, not a general natural-language parser.
negative_words = r"(?:not|never|no|cannot|can't|neither|nor|without|far[ \t]+from|yet[ \t]+to)\b"
negative_modifiers = r"(?:yet|be|been|a|an|the|its|latest|current|official|public|final|sealed|officially|publicly|formally|definitively)"


def predicate_is_negated(prefix: str) -> bool:
    # "not released or shipped" negates both predicates. An adversative or a
    # fresh affirmative verb ("but is shipped") must not inherit that negation.
    prefix = re.sub(
        r"(?:\b(?:release|released|shipped|sealed|resolved)[ \t]+(?:or|nor)[ \t]+)+$",
        "", prefix, flags=re.IGNORECASE,
    )
    return bool(re.search(
        r"\b" + negative_words + r"(?:[ \t]+" + negative_modifiers
        + r"){0,6}[ \t]+$", prefix, re.IGNORECASE,
    ))


def has_affirmative_claim(text: str, subject: str, predicate: str) -> bool:
    for match in re.finditer(subject, text, re.IGNORECASE):
        # Stop at a sentence, block boundary, or another version identifier.
        tail = re.match(r"[ \t,·:–—/a-z'-]*", text[match.end():], re.IGNORECASE).group()
        for claim in re.finditer(predicate, tail, re.IGNORECASE):
            if not predicate_is_negated(tail[:claim.start()]):
                return True
    return False

# Mask only a directly qualified pending release noun phrase. A later shipped
# or released predicate must still be checked, and BQ001 uses no pending barrier.
release_text = re.sub(
    r"\b(?:pending|awaiting)[ \t]+(?:(?:a|the|its)[ \t]+)?"
    r"(?:(?:final|official|public|sealed)[ \t]+){0,3}release\b",
    "pendingevent", status_text(home + "\n" + progress), flags=re.IGNORECASE,
)
if has_affirmative_claim(
    release_text, r"\bv0\.16\.(?:0-beta\.2|7)\b",
    r"\b(?:release|released|shipped|sealed|READY[ \t]*/[ \t]*SEALED)\b",
):
    fail("unsealed candidate or site checkpoint presented as a release")

if has_affirmative_claim(status_text(home + "\n" + progress), r"\bBQ001\b", r"\bRESOLVED\b"):
    fail("public status surface contradicts BQ001 UNRESOLVED")

# Predicate-first headings need their own negation check. Keep block and
# sentence boundaries so a preceding disclaimer cannot hide a later heading.
reverse_claim = re.compile(
    r"\b(?:(?:sealed|official|public|final)[ \t]+release|release|released|shipped)[ \t,·:–—-]*"
    r"(?:(?:version|status)[ \t,·:–—-]+){0,2}v0\.16\.(?:0-beta\.2|7)\b|"
    r"\bRESOLVED(?:[ \t]+(?:status|research|question|for|of)){0,4}[ \t,·:–—-]+BQ001\b",
    re.IGNORECASE,
)
block_text = re.sub(r"</?(?:p|div|li|h[1-6])\b[^>]*>", "\n", home + "\n" + progress)
for clause in re.split(r"[\n;!?]|\.(?=\s)", status_text(block_text)):
    for match in reverse_claim.finditer(clause):
        prefix = clause[:match.start()]
        pending_release = (
            not match.group().lower().startswith("resolved")
            and re.search(r"\b(?:pending|awaiting)[ \t]+$", prefix, re.IGNORECASE)
        )
        if not pending_release and not predicate_is_negated(prefix):
            fail("predicate-first status contradicts unreleased/BQ001 boundaries")

for forbidden in (
    "truth inference enabled",
    "scientifically confirmed",
    "canonical public integration complete",
):
    if forbidden.lower() in (home + "\n" + progress).lower():
        fail(f"public status surface contains forbidden promotion: {forbidden}")

print(
    "PASS: v0.16 public status is centralised; sealed v0.15 assertions and "
    "BQ001/no-promotion boundaries remain explicit"
)
