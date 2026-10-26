# Safety and security

**This is experimental source code, not automotive safety software.**

## Risks

- Some original scripts transmit CAN frames or attempt to change throttle mapping, drive modes and motor-related values.
- Wrong message IDs, counters, checksums or timing may cause unpredictable results in vehicle networks.
- Unsupported hardware and software versions can behave differently.
- A serial connection working does not prove that a CAN write action is safe or effective.

Do not run CAN transmission, torque, pedal, or drive-control experiments on an occupied or road-going vehicle. Limit development to simulated traffic, offline recordings or suitable isolated bench setups with proper protections. This software has not been validated to satisfy functional-safety requirements.

## Local web dashboards

`tools/dashboard_server.py`, `tools/drive_recorder.py`, `tools/ghost3d.py` and `tools/ghost_ui.py` start a local web server. The upstream versions listened on every network interface without authentication, sent `Access-Control-Allow-Origin: *`, accepted control requests from any website the browser visited, and `ghost3d.py` served any file on the disk (`GET /../../etc/passwd`). They now share `tools/local_web_guard.py`:

- they listen on `127.0.0.1` only; `--bind 0.0.0.0` exposes them to the network deliberately, with a warning;
- each start prints a URL with a random token; the browser keeps it in an `HttpOnly`, `SameSite=Strict` cookie and every request without it gets HTTP 403;
- cross-site and cross-origin POST requests are refused, no CORS headers are sent, and POST bodies must be small JSON objects;
- only the dashboard pages and their JSON API are served, with `no-store`, `nosniff` and anti-framing headers.

Never expose these servers to the internet or to an untrusted network.

## Reporting

If you find exposed credentials or security flaws, do not include sensitive details in public issues. Use GitHub's private vulnerability reporting (Security → Report a vulnerability) or contact the repository maintainer privately using their public GitHub profile.
