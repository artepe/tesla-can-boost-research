"""Hardware-free checks for tools/local_web_guard.py.

Run from the repository root: python -m unittest discover -s tests -v
"""

import http.client
import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import ClassVar

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import local_web_guard as guard


class Handler(guard.GuardedHandlerMixin, BaseHTTPRequestHandler):
    calls: ClassVar[list] = []

    def do_GET(self):
        if not self.admit():
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok": true}')

    def do_POST(self):
        if not self.admit():
            return
        body = self.read_json()
        if body is None:
            return
        self.calls.append(body)
        self.send_response(200)
        self.end_headers()

    def log_message(self, *_args):
        pass


class GuardTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=cls.httpd.serve_forever, daemon=True).start()
        cls.port = cls.httpd.server_port
        cls.cookie = {"Cookie": f"can_toolkit_token_{cls.port}={guard.TOKEN}"}

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def request(self, method, path, headers=None, body=None):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=5)
        conn.request(method, path, body=body, headers=headers or {})
        response = conn.getresponse()
        response.read()
        conn.close()
        return response.status, {k.lower(): v for k, v in response.getheaders()}

    def setUp(self):
        Handler.calls.clear()

    def test_requests_without_token_are_refused(self):
        self.assertEqual(self.request("GET", "/")[0], 403)
        self.assertEqual(self.request("GET", "/?token=wrong")[0], 403)

    def test_token_url_sets_strict_cookie_and_hides_token(self):
        status, headers = self.request("GET", f"/?token={guard.TOKEN}")
        self.assertEqual(status, 303)
        self.assertEqual(headers["location"], "/")
        self.assertIn("SameSite=Strict", headers["set-cookie"])
        self.assertIn("HttpOnly", headers["set-cookie"])

    def test_cookie_allows_access_with_security_headers_and_no_cors(self):
        status, headers = self.request("GET", "/api/state", self.cookie)
        self.assertEqual(status, 200)
        self.assertEqual(headers["x-frame-options"], "DENY")
        self.assertEqual(headers["x-content-type-options"], "nosniff")
        self.assertEqual(headers["cache-control"], "no-store")
        self.assertNotIn("access-control-allow-origin", headers)

    def test_cross_site_and_malformed_posts_are_refused(self):
        json_headers = {**self.cookie, "Content-Type": "application/json"}
        body = json.dumps({"mode": "off"})
        self.assertEqual(self.request("POST", "/", {"Content-Type": "application/json"}, body)[0], 403)
        self.assertEqual(self.request("POST", "/", {**json_headers, "Origin": "http://evil.example"}, body)[0], 403)
        self.assertEqual(self.request("POST", "/", {**json_headers, "Sec-Fetch-Site": "cross-site"}, body)[0], 403)
        self.assertEqual(self.request("POST", "/", {**self.cookie, "Content-Type": "text/plain"}, body)[0], 415)
        self.assertEqual(self.request("POST", "/", json_headers, "x" * (guard.MAX_BODY + 1))[0], 413)
        self.assertEqual(self.request("POST", "/", json_headers, "[1]")[0], 400)
        self.assertEqual(Handler.calls, [])

    def test_same_origin_post_is_accepted(self):
        headers = {**self.cookie, "Content-Type": "application/json", "Origin": f"http://127.0.0.1:{self.port}"}
        self.assertEqual(self.request("POST", "/", headers, json.dumps({"mode": "off"}))[0], 200)
        self.assertEqual(Handler.calls, [{"mode": "off"}])

    def test_head_and_preflight_are_refused(self):
        self.assertEqual(self.request("HEAD", "/", self.cookie)[0], 405)
        status, headers = self.request("OPTIONS", "/", {"Origin": "http://evil.example"})
        self.assertEqual(status, 405)
        self.assertNotIn("access-control-allow-origin", headers)

    def test_default_bind_is_loopback(self):
        import argparse

        parser = argparse.ArgumentParser()
        guard.add_bind_argument(parser)
        self.assertEqual(parser.parse_args([]).bind, "127.0.0.1")


if __name__ == "__main__":
    unittest.main()
