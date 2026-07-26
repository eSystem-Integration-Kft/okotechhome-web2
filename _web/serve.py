#!/usr/bin/env python3
"""
serve.py — lokális preview szerver az ÖkoTech Home Test2 oldalhoz.

Miért kell: az oldal kiterjesztés nélküli útvonalakat használ (/uj-epitkezes),
amit élesben a .htaccess rewrite old meg. A sima `python3 -m http.server`
ezekre 404-et adna, így a linkek helyben nem lennének kipróbálhatók.

Ez a szerver a .htaccess viselkedését emulálja:
  /uj-epitkezes       -> uj-epitkezes.html
  /uj-epitkezes.html  -> 301 a tiszta URL-re
  /uj-epitkezes/      -> 301 a záró perjel nélküli alakra
  nem létező útvonal  -> 404.html (ha van), 404-es státusszal

Használat:
    python3 serve.py            # http://localhost:8849
    python3 serve.py 9000       # egyedi port
"""

import http.server
import os
import posixpath
import socketserver
import sys
from urllib.parse import unquote, urlparse

DEFAULT_PORT = 8849
ROOT = os.path.dirname(os.path.abspath(__file__))


class CleanURLHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def send_head(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        query = f"?{parsed.query}" if parsed.query else ""

        # /index.html  ->  301  /   (a főoldal egyetlen kanonikus URL-en éljen)
        if path.endswith("/index.html"):
            self.send_response(301)
            self.send_header("Location", path[: -len("index.html")] + query)
            self.end_headers()
            return None

        # /valami.html  ->  301  /valami
        if path.endswith(".html"):
            self.send_response(301)
            self.send_header("Location", path[: -len(".html")] + query)
            self.end_headers()
            return None

        # /valami/  ->  301  /valami   (a gyökeret nem bántjuk)
        if len(path) > 1 and path.endswith("/"):
            candidate = self._fs_path(path.rstrip("/"))
            if not os.path.isdir(candidate):
                self.send_response(301)
                self.send_header("Location", path.rstrip("/") + query)
                self.end_headers()
                return None

        # /valami  ->  valami.html, ha nincs ilyen nevű fájl vagy könyvtár
        fs = self._fs_path(path)
        if not os.path.isdir(fs) and not os.path.isfile(fs):
            if os.path.isfile(fs + ".html"):
                self.path = path + ".html" + query

        return super().send_head()

    def _fs_path(self, url_path):
        rel = posixpath.normpath(url_path).lstrip("/")
        return os.path.join(ROOT, rel.replace("/", os.sep))

    def send_error(self, code, message=None, explain=None):
        """404-nél az egyedi hibaoldalt adjuk vissza, megtartva a 404 státuszt."""
        if code == 404:
            custom = os.path.join(ROOT, "404.html")
            if os.path.isfile(custom):
                with open(custom, "rb") as fh:
                    body = fh.read()
                self.send_response(404, message)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(body)
                return
        super().send_error(code, message, explain)

    def end_headers(self):
        # A .htaccess biztonsági fejléceinek helyi tükre, hogy a fejlesztés
        # közben is ugyanaz a viselkedés érvényesüljön.
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main():
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Érvénytelen port: {sys.argv[1]}", file=sys.stderr)
            return 1

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", port), CleanURLHandler) as httpd:
        print(f"ÖkoTech Home Test2 — preview:  http://localhost:{port}")
        print(f"Gyökér: {ROOT}")
        print("Leállítás: Ctrl+C")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nLeállítva.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
