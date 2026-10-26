"""Access guard for the toolkit's local web dashboards.

The dashboards show live vehicle data and, in the inherited Ghost3D
experiments, can start CAN frame transmission. They must therefore not be
usable by other devices on the network or by unrelated web pages:

* servers listen on 127.0.0.1 unless ``--bind`` is given explicitly;
* every request needs a random per-run token. It is printed once in the
  terminal URL and then kept in a ``SameSite=Strict`` HttpOnly cookie, so
  other websites (CSRF, DNS rebinding) and LAN users cannot drive the API;
* cross-site and cross-origin POSTs are rejected, no CORS headers are sent,
  and every response carries no-store / nosniff / anti-framing headers;
* POST bodies must be small JSON objects.
"""

from __future__ import annotations

import hmac
import json
import secrets
import socket
from http.cookies import CookieError, SimpleCookie
from urllib.parse import parse_qs, urlsplit

TOKEN = secrets.token_urlsafe(24)
MAX_BODY = 4096
LOOPBACK = {"127.0.0.1", "localhost", "::1"}


def add_bind_argument(parser) -> None:
    parser.add_argument(
        "--bind",
        default="127.0.0.1",
        help="listen address (default 127.0.0.1 = this computer only; "
        "use 0.0.0.0 only on a trusted private network)",
    )


def _lan_ip() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("192.0.2.1", 9))  # UDP connect sends no packet
        return sock.getsockname()[0]
    except OSError:
        return "<this-computer-ip>"
    finally:
        sock.close()


def print_access(bind: str, port: int) -> None:
    """Print the one-time URLs that carry the access token."""
    print(f"Open in this computer's browser: http://127.0.0.1:{port}/?token={TOKEN}")
    if bind not in LOOPBACK:
        host = _lan_ip() if bind in ("0.0.0.0", "::", "") else bind
        print(f"From another device:            http://{host}:{port}/?token={TOKEN}")
        print("WARNING: listening on the network. Anyone with this token URL can use the dashboard.")
    print("The token changes every time the program starts. Do not share it.")


class GuardedHandlerMixin:
    """Mix into a BaseHTTPRequestHandler subclass, listed before the base class."""

    def _cookie_name(self) -> str:
        # Cookies are not port-specific; include the port so two dashboards
        # running at the same time do not overwrite each other's token.
        return f"can_toolkit_token_{self.server.server_port}"

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Content-Security-Policy", "frame-ancestors 'none'")
        self.send_header("Referrer-Policy", "no-referrer")
        super().end_headers()

    def path_only(self) -> str:
        return urlsplit(self.path).path

    def _deny(self, status: int, message: str) -> None:
        body = message.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _cookie_token(self) -> str:
        jar = SimpleCookie()
        try:
            jar.load(self.headers.get("Cookie", ""))
        except CookieError:
            return ""
        morsel = jar.get(self._cookie_name())
        return morsel.value if morsel else ""

    def admit(self) -> bool:
        """Return True when the request may proceed; otherwise a response was sent."""
        query = parse_qs(urlsplit(self.path).query).get("token", [""])[0]
        if self.command == "GET" and query and hmac.compare_digest(query, TOKEN):
            # Move the token into a strict cookie and drop it from the address bar.
            self.send_response(303)
            self.send_header(
                "Set-Cookie",
                f"{self._cookie_name()}={TOKEN}; Path=/; HttpOnly; SameSite=Strict",
            )
            self.send_header("Location", self.path_only() or "/")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return False
        cookie = self._cookie_token()
        if not cookie or not hmac.compare_digest(cookie, TOKEN):
            self._deny(403, "Forbidden: open the token URL printed in the terminal.")
            return False
        if self.command == "POST":
            fetch_site = self.headers.get("Sec-Fetch-Site")
            if fetch_site not in (None, "same-origin", "none"):
                self._deny(403, "Forbidden: cross-site request.")
                return False
            origin = self.headers.get("Origin")
            if origin and urlsplit(origin).netloc != self.headers.get("Host", ""):
                self._deny(403, "Forbidden: cross-origin request.")
                return False
        return True

    def read_json(self):
        """Return a small JSON object body ({} when empty) or None after an error response."""
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = -1
        if length == 0:
            return {}
        if not 0 < length <= MAX_BODY:
            self._deny(413, "Invalid request size.")
            return None
        if self.headers.get("Content-Type", "").split(";", 1)[0].strip() != "application/json":
            self._deny(415, "Use a JSON request.")
            return None
        try:
            body = json.loads(self.rfile.read(length))
        except (ValueError, UnicodeError):
            body = None
        if not isinstance(body, dict):
            self._deny(400, "Invalid JSON object.")
            return None
        return body

    def do_HEAD(self):
        self._deny(405, "Method not allowed.")

    def do_OPTIONS(self):
        # No CORS: never answer preflights with permissive headers.
        self._deny(405, "Method not allowed.")
