#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from html.parser import HTMLParser
from http.client import HTTPException, parse_headers
from io import BytesIO
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "references/community/public-infrastructure-observability-v0.15.json"
STATUS = ROOT / "references/community/public-status-v0.14.json"
V014 = "7b6cfd89de570c4b945d574dad570c37825645fe"


def fail(msg):
    raise SystemExit(f"FAIL: {msg}")


def load_contract():
    if not CONTRACT.is_file(): fail("missing infrastructure observability contract")
    if not STATUS.is_file(): fail("missing canonical public status")
    c = json.loads(CONTRACT.read_text())
    s = json.loads(STATUS.read_text())
    if c.get("target_version") != "0.15.0-beta.1": fail("wrong target version")
    if c.get("status") != "IN_DEVELOPMENT": fail("v0.15 must remain IN_DEVELOPMENT")
    base = c.get("baseline", {})
    if base.get("validated_release_commit") != V014 or base.get("retarget_allowed") is not False:
        fail("immutable v0.14 baseline not preserved")
    if s.get("validated_release_commit") != V014 or s.get("state") != "SEALED":
        fail("canonical public status does not preserve sealed v0.14")
    site = c.get("site", {})
    if site.get("canonical_origin") != "https://akashicnet.org": fail("canonical origin changed")
    if site.get("alternate_origin") != "https://www.akashicnet.org": fail("alternate origin changed")
    if site.get("http_origin") != "http://akashicnet.org" or site.get("http_www_origin") != "http://www.akashicnet.org":
        fail("HTTP origins changed")
    paths = c.get("paths", {})
    for k in ("robots", "sitemap", "public_status_surface"):
        if not isinstance(paths.get(k), str) or not paths[k].startswith("/"): fail(f"invalid path: {k}")
        path = urlsplit(paths[k])
        decoded = unquote(path.path).casefold()
        if path.netloc or path.query or path.fragment or ".." in decoded.split("/") or decoded.startswith("//"):
            fail(f"invalid public probe path: {k}")
        if private_path(decoded):
            fail(f"restricted probe path: {k}")
    checks = c.get("required_live_checks", {})
    for k, v in checks.items():
        if v is not True: fail(f"required live check must be true: {k}")
    uptime = c.get("uptime_semantics", {})
    for k in ("probe_is_operational_telemetry_not_evidence", "release_readiness_requires_successful_live_probe"):
        if uptime.get(k) is not True: fail(f"uptime semantic must be true: {k}")
    for k in ("single_probe_failure_means_source_is_false", "single_probe_failure_means_site_is_permanently_down"):
        if uptime.get(k) is not False: fail(f"uptime semantic must be false: {k}")
    if not isinstance(uptime.get("retry_count"), int) or uptime["retry_count"] < 1: fail("invalid retry count")
    if not isinstance(uptime.get("timeout_seconds"), int) or uptime["timeout_seconds"] < 1: fail("invalid timeout")
    for k, v in c.get("invariants", {}).items():
        if v is not False: fail(f"invariant must remain false: {k}")
    return c


ARTICLE_TITLES = {
    "/homesense887": "one humanity",
    "/awaken/the-serpent-and-the-lotus": "the serpent and the lotus",
}
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
REDIRECTS = {301, 302, 303, 307, 308}


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title = []
        self.in_heading = False
        self.headings = []
        self.canonicals = []
        self.robots = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "h1":
            self.in_heading = True
        if tag == "meta" and (values.get("name") or "").casefold() in ("robots", "googlebot"):
            self.robots.append(values.get("content") or "")
        if tag == "link" and "canonical" in (values.get("rel") or "").lower().split():
            self.canonicals.append(values.get("href"))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "h1":
            self.in_heading = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)
        if self.in_heading:
            self.headings.append(data)


def private_path(path):
    return any(path == prefix or path.startswith(prefix + "/")
               for prefix in ("/sandbox", "/private", "/unlisted", "/contact-inbox", "/api"))


def check_sitemap(body, expected_origin):
    root = ElementTree.fromstring(body)
    entries = {SITEMAP_NS + "urlset": "url", SITEMAP_NS + "sitemapindex": "sitemap"}
    if root.tag not in entries or not len(root):
        raise ValueError("expected a nonempty namespaced sitemap")
    seen = set()
    for entry in root:
        elements = entry.findall(SITEMAP_NS + "loc")
        if entry.tag != SITEMAP_NS + entries[root.tag] or len(elements) != 1:
            raise ValueError("invalid sitemap entry")
        loc = (elements[0].text or "").strip()
        url = urlsplit(loc)
        if (url.scheme, url.netloc) != (expected_origin.scheme, expected_origin.netloc) or url.fragment:
            raise ValueError("sitemap location has unexpected origin or fragment")
        decoded_path = unquote(url.path).casefold()
        if private_path(decoded_path):
            raise ValueError("sitemap includes a protected location")
        if loc in seen:
            raise ValueError("duplicate sitemap location")
        seen.add(loc)
    if root.tag == SITEMAP_NS + "urlset":
        if any(urljoin(expected_origin.geturl(), path) not in seen for path in ARTICLE_TITLES):
            raise ValueError("sitemap is missing a published article control")


def permits(rules, path):
    matches = []
    for directive, pattern in rules:
        if not pattern:
            continue
        anchored = pattern.endswith("$")
        literal = pattern[:-1] if anchored else pattern
        expression = re.escape(literal).replace(r"\*", ".*") + ("$" if anchored else "")
        if re.match(expression, path):
            matches.append((len(literal.replace("*", "")), directive == "allow"))
    # Longest matching rule wins; Allow wins ties.
    return max(matches, default=(0, True))[1]


def check_robots(body, sitemap):
    agents, rules, groups, maps = [], [], [], []
    for line in body.decode("utf-8-sig").splitlines():
        key, _, value = line.split("#", 1)[0].partition(":")
        key, value = key.strip().lower(), value.strip()
        if key == "user-agent":
            if rules:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(value.lower())
        elif agents and key in ("allow", "disallow"):
            rules.append((key, value))
        elif key == "sitemap":
            maps.append(value)
    groups.append((agents, rules))
    if sitemap not in maps or not any("*" in agents for agents, _ in groups):
        raise ValueError("robots lacks wildcard policy or canonical sitemap")
    for agent in ("*", "googlebot"):
        matching = [rules for agents, rules in groups if agent in agents]
        if not matching:
            continue  # Googlebot inherits the wildcard group.
        combined = [rule for rules in matching for rule in rules]
        if any(key == "disallow" and value in ("/", "/*") for key, value in combined):
            raise ValueError("global Disallow for public crawlers")
        if not all(permits(combined, path) for path in ("/", *ARTICLE_TITLES, "/sitemap.xml")):
            raise ValueError("robots blocks a public control")
        # These synthetic paths are evaluated in memory and never requested.
        if any(permits(combined, path) for path in ("/sandbox/check", "/private/check",
                                                   "/api/filofax", "/api/filofax-photo")):
            raise ValueError("robots omits an existing protected exclusion")


def check_content(kind, url, content_type, body, contract, robots_header=""):
    canonical = contract["site"]["canonical_origin"]
    paths = contract["paths"]
    if kind == "robots":
        if content_type != "text/plain":
            raise ValueError("robots response is not text/plain")
        check_robots(body, canonical + paths["sitemap"])
    elif kind == "sitemap":
        if content_type not in {"text/xml", "application/xml"}:
            raise ValueError("sitemap response is not XML")
        check_sitemap(body, urlsplit(canonical))
    else:
        if content_type != "text/html":
            raise ValueError("expected HTML page")
        page = Page()
        page.feed(body.decode("utf-8"))
        page.close()
        path = urlsplit(url).path
        marker = ARTICLE_TITLES.get(path, "akashicnet")
        if marker not in "".join(page.title).casefold() or marker not in " ".join(page.headings).casefold():
            raise ValueError("title or heading does not identify the expected page")
        if any(re.search(r"\b(?:noindex|none)\b", directive, re.I)
               for directive in [*page.robots, robots_header]):
            raise ValueError("public page has an indexing exclusion")
        if page.canonicals != [canonical + path]:
            raise ValueError("missing or unexpected page canonical")


@dataclass
class Hop:
    status: int | None
    headers: dict
    body: bytes
    error: str | None = None


def fetch(url, remaining):
    # --max-time covers DNS, TLS and all body reads, including a slow stream.
    # Redirects are followed by the caller within the same monotonic deadline.
    with tempfile.TemporaryDirectory() as temp:
        headers, body = Path(temp, "headers"), Path(temp, "body")
        cmd = ["curl", "--disable", "--silent", "--show-error", "--compressed",
               "--proto", "=http,https", "--max-time", f"{remaining:.6f}",
               "--max-filesize", "52428800", "--suppress-connect-headers",
               "--user-agent", "AkashicNET-v0.15-observability/1.1",
               "--dump-header", str(headers), "--output", str(body), url]
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=remaining)
            code = result.returncode
        except subprocess.TimeoutExpired:
            code = 28
        except OSError as error:
            return Hop(None, {}, b"", f"transport: {error.strerror}")
        status, fields = None, {}
        if headers.exists():
            # Skip any HTTP 1xx block and keep the final response (even on timeout).
            for block in headers.read_bytes().split(b"\r\n\r\n"):
                first, _, rest = block.partition(b"\r\n")
                match = re.match(rb"^HTTP/\S+ (\d{3})(?: |$)", first)
                if match and int(match[1]) >= 200:
                    status = int(match[1])
                    try:
                        parsed = parse_headers(BytesIO(rest))
                        fields = {name.lower(): val for name, val in parsed.items()}
                        if "x-robots-tag" in fields:
                            fields["x-robots-tag"] = ", ".join(parsed.get_all("X-Robots-Tag"))
                    except HTTPException:
                        return Hop(status, {}, b"", "transport: malformed response headers")
        if code:
            failure = "timeout" if code == 28 else f"transport: curl exit {code}"
            return Hop(status, fields, b"", failure)
        return Hop(status, fields, body.read_bytes() if body.exists() else b"")


def probe_attempt(kind, start, contract, get, clock):
    site = contract["site"]
    began = clock()
    limit = contract["uptime_semantics"]["timeout_seconds"]
    source = urlsplit(start)
    suffix = source.path + ("?" + source.query if source.query else "")
    expected = site["canonical_origin"] + suffix
    allowed = {expected, site["alternate_origin"] + suffix}
    url = start
    hops = []
    record = {"utc": datetime.now(timezone.utc).isoformat(), "hops": hops}
    try:
        while True:
            remaining = limit - (clock() - began)
            if remaining <= 0:
                raise TimeoutError()
            response = get(url, remaining)
            hop = {"url": url, "status": response.status}
            for field in ("content-type", "cf-ray"):
                if field in response.headers:
                    hop[field] = response.headers[field]
            hops.append(hop)
            if response.error == "timeout" or clock() - began >= limit:
                raise TimeoutError()
            if response.error:
                record.update(outcome="transport_error", error=response.error)
                break
            if response.status in REDIRECTS:
                location = response.headers.get("location")
                if not location:
                    raise ValueError("redirect without Location")
                target = urljoin(url, location)
                # Never follow a changed path/query, private route, new host or downgrade.
                if target not in allowed:
                    raise ValueError("redirect outside the allowed public URLs")
                hop["location"] = target
                if any(previous["url"] == target for previous in hops):
                    raise ValueError("redirect loop")
                url = target
                continue
            if response.status != 200:
                record["outcome"] = "http_error" if response.status else "transport_error"
                break
            if url != expected:
                raise ValueError("request did not converge on canonical HTTPS URL")
            mime = response.headers.get("content-type", "").partition(";")[0].strip().lower()
            check_content(kind, url, mime, response.body, contract, response.headers.get("x-robots-tag", ""))
            record["outcome"] = "pass"
            break
    except TimeoutError:
        record["outcome"] = "timeout"
    except (ValueError, ElementTree.ParseError) as error:
        record.update(outcome="content_or_redirect_error", error=str(error))
    record["seconds"] = round(clock() - began, 3)
    return record


def live_probe(c, get=fetch, pause=time.sleep, clock=time.monotonic):
    site, paths = c["site"], c["paths"]
    canonical = site["canonical_origin"]
    targets = {
        "canonical": canonical + "/", "http": site["http_origin"] + "/",
        "alternate": site["alternate_origin"] + "/", "http_www": site["http_www_origin"] + "/",
        "robots": canonical + paths["robots"], "sitemap": canonical + paths["sitemap"],
        "status": canonical + paths["public_status_surface"],
        **{path: canonical + path for path in ARTICLE_TITLES},
        "alternate_article_query": site["alternate_origin"] + "/homesense887?ref=qr",
    }
    failures = []
    results = {}
    for kind, url in targets.items():
        # The status surface is currently the homepage; count that request once.
        if url in results:
            original, outcome = results[url]
            print(json.dumps({"check": kind, "url": url, "same_as": original, "result": outcome}))
            if outcome == "failed":
                failures.append(kind)
            continue
        attempts = []
        for index in range(c["uptime_semantics"]["retry_count"] + 1):
            if index:
                pause(index)
            attempt = probe_attempt(kind, url, c, get, clock)
            attempts.append({"attempt": index + 1, **attempt})
            if attempt["outcome"] == "pass":
                break
        outcome = "recovered" if len(attempts) > 1 else "pass"
        if attempts[-1]["outcome"] != "pass":
            outcome = "failed"
            failures.append(kind)
        results[url] = (kind, outcome)
        print(json.dumps({"check": kind, "url": url, "result": outcome, "attempts": attempts}), flush=True)
    if failures:
        fail("live probe failed: " + ", ".join(failures))
    print("PASS: live v0.15 infrastructure probe: HTTPS/redirects/indexing/public manifests")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--live", action="store_true", help="also probe the public site over the network")
    args = ap.parse_args()
    c = load_contract()
    print("PASS: v0.15 infrastructure observability contract validates")
    if args.live:
        live_probe(c)


if __name__ == "__main__":
    main()
