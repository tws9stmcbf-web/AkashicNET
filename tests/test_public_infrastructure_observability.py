import io
import json
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock, patch

from scripts import validate_public_infrastructure_observability_v015 as monitor


CONTRACT = monitor.load_contract()
ORIGIN = CONTRACT["site"]["canonical_origin"]
WILDCARD = """User-agent: *
Allow: /
Disallow: /sandbox
Disallow: /private/
Disallow: /api/filofax
Sitemap: https://akashicnet.org/sitemap.xml
"""
XML = ('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
       "".join(f"<url><loc>{ORIGIN}{path}</loc></url>" for path in ("/", *monitor.ARTICLE_TITLES)) +
       "</urlset>").encode()


def page(path, title):
    html = '<title>' + title + '</title><link rel="canonical" href="' + ORIGIN + path + '"><h1>' + title + '</h1>'
    return monitor.Hop(200, {"content-type": "text/html"}, html.encode())


def normal(url, remaining):
    source = monitor.urlsplit(url)
    if source.scheme == "http":
        return monitor.Hop(302, {"location": url.replace("http:", "https:", 1)}, b"")
    if source.netloc.startswith("www."):
        return monitor.Hop(308, {"location": url.replace("//www.", "//", 1)}, b"")
    if source.path == "/robots.txt":
        return monitor.Hop(200, {"content-type": "text/plain"}, WILDCARD.encode())
    if source.path == "/sitemap.xml":
        return monitor.Hop(200, {"content-type": "application/xml"}, XML)
    return page(source.path, monitor.ARTICLE_TITLES.get(source.path, "AkashicNET"))


class InfrastructureTests(unittest.TestCase):
    def run_probe(self, get, expect_failure=False):
        output = io.StringIO()
        with redirect_stdout(output):
            if expect_failure:
                with self.assertRaisesRegex(SystemExit, "live probe failed"):
                    monitor.live_probe(CONTRACT, get=get, pause=lambda _: None)
            else:
                monitor.live_probe(CONTRACT, get=get, pause=lambda _: None)
        return {row["check"]: row for line in output.getvalue().splitlines()
                if line.startswith("{") for row in [json.loads(line)]}

    def test_success_and_recovered_attempt_records(self):
        first = True

        def flaky(url, remaining):
            nonlocal first
            self.assertLessEqual(remaining, 15)
            if url == ORIGIN + "/" and first:
                first = False
                return monitor.Hop(503, {"cf-ray": "test-edge"}, b"")
            return normal(url, remaining)

        rows = self.run_probe(flaky)
        self.assertEqual(rows["status"]["same_as"], "canonical")
        self.assertEqual(rows["canonical"]["result"], "recovered")
        attempts = rows["canonical"]["attempts"]
        self.assertEqual([a["hops"][0]["status"] for a in attempts], [503, 200])
        self.assertEqual(attempts[0]["hops"][0]["cf-ray"], "test-edge")
        self.assertEqual([h["status"] for h in rows["http_www"]["attempts"][0]["hops"]], [302, 308, 200])
        hops = rows["alternate_article_query"]["attempts"][0]["hops"]
        self.assertEqual(hops[0]["location"], ORIGIN + "/homesense887?ref=qr")
        self.assertEqual(hops[-1]["url"], hops[0]["location"])

    def test_exhaustion_preserves_other_endpoint_results(self):
        def failing(url, remaining):
            if url.endswith("/robots.txt"):
                return monitor.Hop(503, {}, b"")
            return normal(url, remaining)
        rows = self.run_probe(failing, expect_failure=True)
        self.assertEqual(rows["robots"]["result"], "failed")
        attempts = rows["robots"]["attempts"]
        self.assertEqual([a["attempt"] for a in attempts], [1, 2, 3, 4])
        self.assertEqual([a["outcome"] for a in attempts], ["http_error"] * 4)
        self.assertEqual(rows["sitemap"]["result"], "pass")
        self.assertEqual(rows["/awaken/the-serpent-and-the-lotus"]["result"], "pass")

    def attempt(self, kind, start, *responses):
        get = Mock(side_effect=responses)
        record = monitor.probe_attempt(kind, start, CONTRACT, get, lambda: 0)
        self.assertEqual(get.call_count, len(responses))
        return record

    def test_timeout_preserves_partial_status_and_is_not_http_error(self):
        for status in (None, 200):
            record = self.attempt("canonical", ORIGIN + "/", monitor.Hop(status, {}, b"", "timeout"))
            self.assertEqual(record["outcome"], "timeout")
            self.assertEqual(record["hops"][0]["status"], status)
        result = self.attempt("canonical", ORIGIN + "/", monitor.Hop(None, {}, b"", "transport: curl exit 6"))
        self.assertEqual(result["outcome"], "transport_error")

    def test_same_deadline_across_redirects(self):
        ticks = iter((0, 0, 8, 8, 16, 16))
        get = Mock(side_effect=[monitor.Hop(302, {"location": ORIGIN + "/"}, b""),
                                page("/", "AkashicNET")])
        record = monitor.probe_attempt("http", "http://akashicnet.org/", CONTRACT, get, lambda: next(ticks))
        self.assertEqual([call.args[1] for call in get.call_args_list], [15, 7])
        self.assertEqual(record["outcome"], "timeout")

    def test_wrong_content_is_a_failed_check_even_with_200(self):
        for kind, path, mime in (("robots", "/robots.txt", "text/plain"), ("sitemap", "/sitemap.xml", "application/xml")):
            for content_type in (mime, "text/html"):
                with self.subTest(kind=kind, content_type=content_type):
                    response = monitor.Hop(200, {"content-type": content_type}, b"<html>oops</html>")
                    self.assertEqual(self.attempt(kind, ORIGIN + path, response)["outcome"], "content_or_redirect_error")
        response = page("/", "AkashicNET")
        self.assertEqual(self.attempt("article", ORIGIN + "/homesense887", response)["outcome"], "content_or_redirect_error")

    def test_article_requires_heading_and_indexable_response(self):
        response = page("/homesense887", "One Humanity")
        for extra, headers in ((b'<meta name="googlebot" content="noindex">', {}),
                               (b"", {"x-robots-tag": "noindex, nofollow"}),
                               (b"", None)):
            with self.subTest(extra=extra, headers=headers):
                body = response.body + extra
                if headers is None:
                    body = body[:body.index(b"<h1>")]
                hop = monitor.Hop(200, {**response.headers, **(headers or {})}, body)
                row = self.attempt("article", ORIGIN + "/homesense887", hop)
                self.assertEqual(row["outcome"], "content_or_redirect_error")

    def test_urlset_requires_published_controls(self):
        for path in monitor.ARTICLE_TITLES:
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, "published article control"):
                monitor.check_sitemap(XML.replace(path.encode(), b"/alternate-control"), monitor.urlsplit(ORIGIN))

    def test_robots_groups_and_private_rules(self):
        for extra in ("Disallow: /\n", "Disallow: /homesense887\n", "Allow: /sandbox/check\n",
                      "User-agent: Googlebot\nDisallow: /\n"):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                monitor.check_robots((WILDCARD + extra).encode(), ORIGIN + "/sitemap.xml")
        monitor.check_robots((WILDCARD + "User-agent: OtherBot\nDisallow: /\n").encode(), ORIGIN + "/sitemap.xml")

    def test_sitemap_rejects_invalid_and_restricted_entries(self):
        for xml in (b"<urlset/>", XML.replace(b".org/</loc>", b".org/sandbox/demo</loc>"),
                    XML.replace(b"akashicnet.org", b"www.akashicnet.org"),
                    XML.replace(b"<loc>", b"<loc>oops</loc><loc>")):
            with self.subTest(xml=xml), self.assertRaises(ValueError):
                monitor.check_sitemap(xml, monitor.urlsplit(ORIGIN))

    def test_no_changed_path_host_query_or_redirect_loop(self):
        start = "https://www.akashicnet.org/homesense887?ref=qr"
        for dest in (start, ORIGIN + "/homesense887", ORIGIN + "/sandbox/fixture", "https://example.org/"):
            record = self.attempt("alternate_article_query", start, monitor.Hop(308, {"location": dest}, b""))
            self.assertEqual(record["outcome"], "content_or_redirect_error")
            self.assertEqual(len(record["hops"]), 1)

    def test_curl_propagates_status_headers_when_body_times_out(self):
        def timeout(cmd, **kwargs):
            index = cmd.index("--dump-header")
            monitor.Path(cmd[index + 1]).write_bytes(b"HTTP/2 200\r\ncf-ray: test-id\r\n\r\n")
            raise monitor.subprocess.TimeoutExpired(cmd, kwargs["timeout"])
        with patch.object(monitor.subprocess, "run", side_effect=timeout):
            hop = monitor.fetch(ORIGIN + "/", 0.1)
        self.assertEqual((hop.status, hop.headers, hop.error), (200, {"cf-ray": "test-id"}, "timeout"))


if __name__ == "__main__":
    unittest.main()
