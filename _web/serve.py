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
import json
import os
import posixpath
import socketserver
import sys
from urllib.parse import unquote, urlparse

DEFAULT_PORT = 8849
ROOT = os.path.dirname(os.path.abspath(__file__))



class RangeMixin:
    """Részleges (206) válasz támogatása.

    A `SimpleHTTPRequestHandler` mindig a teljes fájlt küldi. Videónál ez azt
    jelenti, hogy a böngésző minden tekeréskor/újraindításkor az egészet
    letölti — hosszú munkamenetben ez fölösleges forgalom és memória. Élesben
    az Apache ezt magától megoldja; ez a helyi kiszolgálót hozza szintre."""

    def send_head(self):
        rng = self.headers.get('Range')
        if not rng or not rng.startswith('bytes='):
            return super().send_head()
        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return super().send_head()
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404)
            return None
        size = os.fstat(f.fileno()).st_size
        try:
            first, last = rng.split('=', 1)[1].split('-', 1)
            start = int(first) if first else 0
            end = int(last) if last else size - 1
        except ValueError:
            f.close()
            return super().send_head()
        end = min(end, size - 1)
        if start > end:
            f.close()
            self.send_error(416)
            return None
        self.send_response(206)
        self.send_header('Content-Type', self.guess_type(path))
        self.send_header('Accept-Ranges', 'bytes')
        self.send_header('Content-Range', f'bytes {start}-{end}/{size}')
        self.send_header('Content-Length', str(end - start + 1))
        self.end_headers()
        f.seek(start)
        self.wfile.write(f.read(end - start + 1))
        f.close()
        return None

class CleanURLHandler(RangeMixin, http.server.SimpleHTTPRequestHandler):
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


    def do_POST(self):
        """A /api/ végpontok PHP-t igényelnek — ez a kiszolgáló nem futtat PHP-t.

        Miért kell mégis kezelni: POST-ra a BaseHTTPRequestHandler 501-et küld,
        de a kérés TÖRZSÉT nem olvassa ki. Nagyobb feltöltésnél a böngésző a
        küldés közben blokkol, a fetch sosem tér vissza, és a gomb a végtelenségig
        pörög — ami hibának látszik a weboldalon, holott a kiszolgáló hiánya.

        Ezért itt kiolvassuk a törzset, és beszédes JSON-t adunk vissza.
        """
        hossz = int(self.headers.get("Content-Length") or 0)
        maradek = hossz
        while maradek > 0:                      # a törzset EL KELL olvasni
            maradek -= len(self.rfile.read(min(65536, maradek)) or b"")

        if self.path.startswith("/api/"):
            uzenet = ("Ez a fejlesztői kiszolgáló nem futtat PHP-t, ezért az /api/ "
                      "végpontok itt nem működnek. Próbálja PHP-s kiszolgálón: "
                      "php -S 127.0.0.1:8910 -t . — vagy a teszt-szerveren.")
            kod = 501
        else:
            uzenet = "Ez a kiszolgáló csak statikus fájlokat ad ki."
            kod = 405

        torzs = json.dumps({"ok": False, "uzenet": uzenet}, ensure_ascii=False).encode("utf-8")
        self.send_response(kod)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(torzs)))
        self.end_headers()
        self.wfile.write(torzs)

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
        #
        # A CSP-t azért is küldjük, mert enélkül egy egész hibaosztály csak
        # ÉLESBEN derül ki: a `style-src` itt NEM tartalmaz 'unsafe-inline'-t,
        # ezért minden beágyazott <style> és style="" attribútum eldobódik —
        # helyben viszont, CSP nélkül, tökéletesnek látszana. (Pontosan ez
        # történt a hibaoldalakkal: formázatlanul jelentek meg a szerveren.)
        # HA EZT A SORT MÓDOSÍTOD, a .htaccess CSP-jét is át kell írni.
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; base-uri 'self'; form-action 'self'; "
            "frame-ancestors 'none'; object-src 'none'; img-src 'self' data:; "
            "style-src 'self' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; script-src 'self'",
        )
        # A teszt üzemmód robotkizárása is, hogy a két környezet ne térjen el.
        self.send_header(
            "X-Robots-Tag",
            "noindex, nofollow, noarchive, nosnippet, noimageindex, notranslate",
        )
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
