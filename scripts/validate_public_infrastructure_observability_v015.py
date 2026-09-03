#!/usr/bin/env python3
import argparse
import json
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, build_opener, HTTPRedirectHandler

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
    paths = c.get("paths", {})
    for k in ("robots", "sitemap", "public_status_surface"):
        if not isinstance(paths.get(k), str) or not paths[k].startswith("/"): fail(f"invalid path: {k}")
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


def get(url, timeout, retries):
    opener = build_opener(HTTPRedirectHandler())
    last = None
    for i in range(retries):
        try:
            req = Request(url, headers={"User-Agent": "AkashicNET-v0.15-observability/1.0"})
            with opener.open(req, timeout=timeout) as r:
                body = r.read(1024 * 1024).decode("utf-8", errors="replace")
                return {"requested": url, "final": r.geturl(), "status": r.status, "body": body}
        except (HTTPError, URLError, TimeoutError) as e:
            last = e
            if i + 1 < retries:
                time.sleep(1 + i)
    raise RuntimeError(f"probe failed for {url}: {last}")


def origin(url):
    m = re.match(r"^(https?://[^/]+)", url)
    return m.group(1).lower() if m else ""


def live_probe(c):
    site, paths, uptime = c["site"], c["paths"], c["uptime_semantics"]
    timeout, retries = uptime["timeout_seconds"], uptime["retry_count"]
    canonical = site["canonical_origin"]
    results = {}
    for key, url in {
        "canonical": canonical + "/",
        "http": site["http_origin"] + "/",
        "alternate": site["alternate_origin"] + "/",
        "http_www": site["http_www_origin"] + "/",
        "robots": canonical + paths["robots"],
        "sitemap": canonical + paths["sitemap"],
        "status": canonical + paths["public_status_surface"],
    }.items():
        results[key] = get(url, timeout, retries)

    if results["canonical"]["status"] < 200 or results["canonical"]["status"] >= 400:
        fail("canonical HTTPS site is not reachable")
    if origin(results["http"]["final"]) != canonical or not results["http"]["final"].startswith("https://"):
        fail("apex HTTP does not converge to canonical HTTPS origin")
    if origin(results["http_www"]["final"]) != canonical or not results["http_www"]["final"].startswith("https://"):
        fail("www HTTP does not converge to canonical HTTPS origin")
    if origin(results["alternate"]["final"]) != canonical:
        fail("alternate HTTPS host does not converge to canonical origin")
    if results["robots"]["status"] != 200:
        fail("robots.txt is not reachable")
    robots = results["robots"]["body"].lower()
    if re.search(r"user-agent\s*:\s*\*[^#]*?disallow\s*:\s*/\s*(?:\n|$)", robots, re.S):
        fail("robots.txt globally disallows indexing")
    if results["sitemap"]["status"] != 200:
        fail("sitemap is not reachable")
    if results["status"]["status"] < 200 or results["status"]["status"] >= 400:
        fail("public status surface is not reachable")
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
