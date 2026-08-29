#!/usr/bin/env python3
"""Szövegkivonat a teljes oldalról, a menürendszer szerint rendezve.

A megépült oldalak `<main>` tartalmából kinyeri a látható szöveget —
címeket, bevezetőket, bekezdéseket, felsorolásokat, kártyákat, GYIK-et,
táblázatokat, gombfeliratokat, képaláírásokat és űrlapcímkéket —, és a
`fejlec.py` menüfája szerinti sorrendben három kimenetet ír:

  _files/szoveg-kivonat.html   — olvasónézet: bal oldalt a menürendszer,
                                 kereső, szűrés, nyomtatás → PDF
  _files/szoveg-kivonat.md     — lineáris szöveg, továbbküldhető
  _files/szoveg-kivonat.pdf    — csak a --pdf kapcsolóval (Chrome headless)

A navigáció, a lábléc és a morzsamenü szándékosan kimarad: minden oldalon
ugyanaz, átnézésre zaj. A HTML önhordó, a betűtípusok base64-ben ágyazva.

Futtatás a repó gyökeréből:
    python3 scripts/oldalgyartas/szoveg_kivonat.py
    python3 scripts/oldalgyartas/szoveg_kivonat.py --pdf
"""
from __future__ import annotations

import base64
import html as htmlmod
import json
import os
import pathlib
import re
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
from html.parser import HTMLParser

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / "_web"
KIMENET = GYOKER / "_files"
sys.path.insert(0, str(GYOKER / "scripts" / "oldalgyartas"))

import fejlec  # noqa: E402

VERZIO = (GYOKER / "VERSION").read_text().strip()

CHROME = pathlib.Path(
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

# A láblécből elérhető rendszer- és jogi oldalak — a főmenüben nem szerepelnek.
JOGI = [
    ("Kapcsolat", "kapcsolat"),
    ("Konzultáció", "konzultacio"),
    ("Adatkezelési tájékoztató", "adatkezelesi-tajekoztato"),
    ("Cookie-tájékoztató", "cookie-tajekoztato"),
    ("Általános Szerződési Feltételek", "aszf"),
    ("Jogi nyilatkozat", "jogi-nyilatkozat"),
    ("Akadálymentességi nyilatkozat", "akadalymentessegi-nyilatkozat"),
]

# Nem tartalomoldalak: hibaoldalak és belső jelentés.
KIHAGY = {"401.html", "403.html", "404.html", "500.html", "jelentes.html"}

VOID = {"img", "br", "hr", "input", "meta", "link", "source", "area",
        "base", "col", "embed", "param", "track", "wbr"}
ATUGOR = {"svg", "script", "style", "noscript", "source", "template"}
BLOKKSZERU = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "div",
              "section", "header", "footer", "figcaption", "summary",
              "td", "th", "tr", "dt", "dd", "blockquote", "aside"}

EYEBROW = {"section-eyebrow", "panel-dark-eyebrow", "type-data-eyebrow",
           "hero-eyebrow", "eyebrow"}
CIMKE_CIM = {"card-title", "split-title", "situation-title", "faq-q",
             "type-ui-card-title", "panel-dark-title", "step-title"}


# ------------------------------------------------------------------ 1. DOM
class Elem:
    __slots__ = ("tag", "attrs", "gyerekek")

    def __init__(self, tag: str, attrs: dict | None = None):
        self.tag = tag
        self.attrs = attrs or {}
        self.gyerekek: list = []

    @property
    def osztaly(self) -> set[str]:
        return set(self.attrs.get("class", "").split())


class Fa(HTMLParser):
    """Elnéző DOM-építő: a lezáratlan tageket a verem visszatekerése zárja."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.gyoker = Elem("#gyoker")
        self.verem = [self.gyoker]

    def handle_starttag(self, tag, attrs):
        e = Elem(tag, {k: (v or "") for k, v in attrs})
        self.verem[-1].gyerekek.append(e)
        if tag not in VOID:
            self.verem.append(e)

    def handle_startendtag(self, tag, attrs):
        self.verem[-1].gyerekek.append(Elem(tag, {k: (v or "") for k, v in attrs}))

    def handle_endtag(self, tag):
        for i in range(len(self.verem) - 1, 0, -1):
            if self.verem[i].tag == tag:
                del self.verem[i:]
                return

    def handle_data(self, data):
        self.verem[-1].gyerekek.append(data)


def elemez(reszlet: str) -> Elem:
    p = Fa()
    p.feed(reszlet)
    p.close()
    return p.gyoker


def szoveg(e: Elem, kizar: set[str] | None = None) -> str:
    """A részfa látható szövege, az eredeti szóközöket megtartva.

    A `kizar` osztálynevekkel jelölt elemek (pl. sorszámbadge, pipa)
    kimaradnak — azokat a hívó külön, jelként teszi a szöveg elé.
    """
    darabok: list[str] = []

    def bejar(n):
        if isinstance(n, str):
            darabok.append(n)
            return
        if n.tag in ATUGOR:
            return
        if kizar and n.osztaly & kizar:
            return
        blokk = n.tag in BLOKKSZERU or n.tag == "br"
        if blokk:
            darabok.append(" ")
        for gy in n.gyerekek:
            bejar(gy)
        if blokk:
            darabok.append(" ")

    bejar(e)
    return re.sub(r"\s+", " ", "".join(darabok)).strip()


def keres(e: Elem, tag: str) -> list[Elem]:
    ki = []

    def bejar(n):
        if isinstance(n, str):
            return
        if n.tag == tag:
            ki.append(n)
        for gy in n.gyerekek:
            bejar(gy)

    bejar(e)
    return ki


# -------------------------------------------------------------- 2. BLOKKOK
def blokkok(fo: Elem) -> list[tuple[str, str]]:
    """A `<main>` tartalma (tipus, szöveg) párok sorozataként."""
    ki: list[tuple[str, str]] = []

    def hozzaad(tipus: str, sz: str):
        if sz:
            ki.append((tipus, sz))

    def bejar(e: Elem):
        for gy in e.gyerekek:
            if isinstance(gy, str):
                continue
            t, cl = gy.tag, gy.osztaly
            if t in ATUGOR:
                continue
            if t == "nav" and "breadcrumb" in cl:
                continue
            if "vizualisan-rejtett" in cl or "sr-only" in cl:
                continue

            if t == "details":
                fejek = [x for x in gy.gyerekek
                         if isinstance(x, Elem) and x.tag == "summary"]
                for f in fejek:
                    hozzaad("kerdes", szoveg(f))
                for x in gy.gyerekek:
                    if isinstance(x, Elem) and x.tag != "summary":
                        hozzaad("valasz", szoveg(x))
            elif t == "table":
                for sor in keres(gy, "tr"):
                    cellak = [szoveg(c) for c in sor.gyerekek
                              if isinstance(c, Elem) and c.tag in ("th", "td")]
                    hozzaad("tabla", " | ".join(cellak))
            elif t == "img":
                alt = gy.attrs.get("alt", "").strip()
                hozzaad("kep", alt)
            elif t == "figcaption":
                hozzaad("kep", szoveg(gy))
            elif t == "h1":
                hozzaad("h1", szoveg(gy))
            elif t == "h2":
                hozzaad("h2", szoveg(gy))
            elif t in ("h3", "h4", "h5", "h6"):
                hozzaad("h3", szoveg(gy))
            elif t == "li":
                li_blokk(gy)
            elif t == "p":
                gombok = ([x for x in keres(gy, "a") if "btn" in x.osztaly]
                          + keres(gy, "button"))
                gombszoveg = " ".join(szoveg(g) for g in gombok).strip()
                if gombok and len(szoveg(gy)) <= len(gombszoveg) + 4:
                    for g in gombok:
                        hozzaad("cta", szoveg(g))
                    continue
                if cl & EYEBROW:
                    tipus = "eyebrow"
                elif "hero-lead" in cl:
                    tipus = "lead"
                elif "section-lead" in cl:
                    tipus = "szakaszlead"
                else:
                    tipus = "p"
                hozzaad(tipus, szoveg(gy))
            elif t == "button" or (t == "a" and "btn" in cl):
                hozzaad("cta", szoveg(gy))
            elif t == "label":
                hozzaad("mezo", szoveg(gy))
            elif t == "select":
                opciok = [szoveg(o) for o in keres(gy, "option")]
                hozzaad("mezo", "választható: " + ", ".join(x for x in opciok if x))
            elif t == "span" and cl & EYEBROW:
                hozzaad("eyebrow", szoveg(gy))
            else:
                bejar(gy)

    def li_blokk(li: Elem):
        """Kártya vagy felsoroláselem — a címet és a törzset külön tartva."""
        cl = li.osztaly
        beagyazott = [x for x in li.gyerekek
                      if isinstance(x, Elem) and x.tag in ("ul", "ol", "details")]
        jel = ""
        for sp in keres(li, "span"):
            k = sp.osztaly
            if "fit-mark" in k:
                jel = "✓ " if "fit-yes" in k else "✗ "
            elif "card-badge" in k:
                jel = szoveg(sp) + ". "

        cimek = [x for x in keres(li, "h3") + keres(li, "h4")]
        cimek += [x for x in keres(li, "p") + keres(li, "span")
                  if x.osztaly & CIMKE_CIM]
        cimszoveg = " ".join(szoveg(c) for c in cimek).strip()

        forras = li
        if beagyazott:
            forras = Elem(li.tag, li.attrs)
            forras.gyerekek = [x for x in li.gyerekek if x not in beagyazott]
        # a sorszám és a pipa jelként kerül a szöveg elé, nem a törzsbe
        teljes = szoveg(forras, kizar={"card-badge", "fit-mark"})

        if cimszoveg and teljes.startswith(cimszoveg) and len(teljes) > len(cimszoveg):
            hozzaad("li-cim", jel + cimszoveg)
            hozzaad("li", teljes[len(cimszoveg):].strip())
        else:
            hozzaad("li", jel + teljes)

        for b in beagyazott:
            bejar_egy(b)

    def bejar_egy(e: Elem):
        burok = Elem("#burok")
        burok.gyerekek = [e]
        bejar(burok)

    bejar(fo)

    # ismétlődő szomszédos blokkok kiszűrése (pl. kép alt + figcaption)
    tiszta: list[tuple[str, str]] = []
    for b in ki:
        if tiszta and tiszta[-1] == b:
            continue
        tiszta.append(b)
    return tiszta


# ---------------------------------------------------------------- 3. OLDAL
def utvonal(url: str) -> str:
    return "/" + url if url else "/"


def fajl(url: str) -> pathlib.Path:
    u = url or ""
    rel = (u + "index.html") if (u == "" or u.endswith("/")) else u + ".html"
    return WEB / rel


def van(url: str | None) -> bool:
    return url is not None and fajl(url).exists()


def oldal(url: str) -> dict:
    forras = fajl(url).read_text(errors="replace")
    i = forras.find("<main")
    j = forras.find("</main>")
    fo = elemez(forras[i:j] if i >= 0 and j > i else forras)

    cimke = re.search(r"<title>(.*?)</title>", forras, re.S)
    bl = blokkok(fo)
    cim = next((s for t, s in bl if t == "h1"), None)
    if not cim and cimke:
        cim = htmlmod.unescape(cimke.group(1)).split("—")[0].strip()

    torzs = [b for b in bl if b[0] != "h1"]
    szavak = sum(len(s.split()) for _t, s in torzs)
    return {"cim": cim or url, "utvonal": utvonal(url), "fajl": str(
        fajl(url).relative_to(GYOKER)), "blokkok": torzs, "szavak": szavak}


# ------------------------------------------------------------------- 4. FA
def menufa() -> list[dict]:
    """Főmenüpont › hub › aloldal, csak a megépült oldalakkal."""
    ki: list[dict] = []
    latott: set[str] = set()

    def felvesz(cim: str, url: str | None, szint: int, csoport: list):
        if not van(url) or url in latott:
            return
        latott.add(url)
        csoport.append({"cim": cim, "url": url, "szint": szint})

    fooldal: list[dict] = []
    felvesz("Főoldal", "", 1, fooldal)
    if fooldal:
        ki.append({"kat": "Főoldal", "tetelek": fooldal})

    for kat, katurl, hubok in fejlec.MENU:
        tetelek: list[dict] = []
        felvesz(f"{kat} — áttekintés", katurl, 1, tetelek)
        for _ikon, hcim, hurl, alok in hubok:
            felvesz(hcim.lstrip("↳ "), hurl, 1, tetelek)
            for acim, aurl in alok:
                felvesz(acim, aurl, 2, tetelek)
        if tetelek:
            ki.append({"kat": kat, "tetelek": tetelek})

    masodlagos: list[dict] = []
    for cim, url in getattr(fejlec, "MASODLAGOS", []):
        felvesz(cim, url, 1, masodlagos)
    if masodlagos:
        ki.append({"kat": "További oldalak", "tetelek": masodlagos})

    jogi: list[dict] = []
    for cim, url in JOGI:
        felvesz(cim, url, 1, jogi)
    if jogi:
        ki.append({"kat": "Rendszer- és jogi oldalak", "tetelek": jogi})

    # ami egyik listában sem szerepelt, de létező tartalomoldal
    egyeb: list[dict] = []
    for f in sorted(WEB.rglob("*.html")):
        if f.name in KIHAGY:
            continue
        rel = f.relative_to(WEB).as_posix()
        url = rel[:-len("index.html")] if rel.endswith("index.html") else rel[:-5]
        if url in latott:
            continue
        latott.add(url)
        egyeb.append({"cim": url, "url": url, "szint": 1})
    if egyeb:
        ki.append({"kat": "Menün kívüli oldalak", "tetelek": egyeb})
    return ki


# ------------------------------------------------------------ 5. MARKDOWN
MD_ELO = {"eyebrow": "**", "h2": "## ", "h3": "### ", "lead": "*",
          "kerdes": "**K:** ", "valasz": "**V:** ", "kep": "> _kép:_ ",
          "cta": "→ ", "mezo": "▢ ", "tabla": "| ", "li-cim": "- **",
          "li": "- ", "p": ""}


def markdown(fa: list[dict], oldalak: dict, ossz: dict) -> str:
    s = ["# ÖkoTech Home — szövegkivonat",
         "",
         f"Verzió {VERZIO} · {ossz['oldal']} oldal · "
         f"{ossz['szavak']:,} szó".replace(",", " "),
         "",
         "A fejléc, a morzsamenü és a lábléc kimarad — minden oldalon azonos.",
         "", "---", ""]
    for csoport in fa:
        s += [f"# {csoport['kat']}", ""]
        for t in csoport["tetelek"]:
            o = oldalak[t["url"]]
            s += [f"## {o['cim']}", "",
                  f"`{o['utvonal']}` · {o['szavak']} szó", ""]
            for tip, sz in o["blokkok"]:
                if tip == "eyebrow":
                    s.append(f"**{sz.upper()}**")
                elif tip == "h2":
                    s.append(f"### {sz}")
                elif tip == "h3":
                    s.append(f"#### {sz}")
                elif tip == "lead":
                    s.append(f"> {sz}")
                elif tip == "szakaszlead":
                    s.append(sz)
                elif tip == "li-cim":
                    s.append(f"- **{sz}**")
                elif tip == "li":
                    s.append(f"  {sz}" if s and s[-1].startswith("- **") else f"- {sz}")
                elif tip == "kerdes":
                    s.append(f"**K: {sz}**")
                elif tip == "valasz":
                    s.append(f"V: {sz}")
                elif tip == "tabla":
                    s.append(f"| {sz} |")
                elif tip == "kep":
                    s.append(f"> _kép:_ {sz}")
                elif tip == "cta":
                    s.append(f"→ _{sz}_")
                elif tip == "mezo":
                    s.append(f"▢ {sz}")
                else:
                    s.append(sz)
                s.append("")
            s += ["---", ""]
    return "\n".join(s)


# ---------------------------------------------------------------- 6. HTML
def h(sz: str) -> str:
    return htmlmod.escape(sz, quote=True)


def html_doc(fa: list[dict], oldalak: dict, ossz: dict) -> str:
    fontfajl = GYOKER / "scripts" / "oldalgyartas" / "_fonts.css"
    fontcss = fontfajl.read_text() if fontfajl.exists() else ""

    menu, torzs, toc = [], [], []
    n = 0
    for ci, csoport in enumerate(fa):
        kid = f"k{ci}"
        elemek = []
        for t in csoport["tetelek"]:
            n += 1
            o = oldalak[t["url"]]
            aid = f"o{n}"
            szint = "m2" if t["szint"] == 2 else "m1"
            elemek.append(
                f'<li class="{szint}"><a href="#{aid}" data-cel="{aid}">'
                f'<span class="m-cim">{h(o["cim"])}</span>'
                f'<span class="m-szo">{o["szavak"]}</span></a></li>')
            toc.append(f'<li class="{szint}"><span class="toc-cim">{h(o["cim"])}</span>'
                       f'<code>{h(o["utvonal"])}</code></li>')

            sorok = []
            for tip, sz in o["blokkok"]:
                e = h(sz)
                if tip == "eyebrow":
                    sorok.append(f'<p class="b-eyebrow">{e}</p>')
                elif tip == "h2":
                    sorok.append(f'<h3 class="b-h2">{e}</h3>')
                elif tip == "h3":
                    sorok.append(f'<h4 class="b-h3">{e}</h4>')
                elif tip == "lead":
                    sorok.append(f'<p class="b-lead b-lead-fo">{e}</p>')
                elif tip == "szakaszlead":
                    sorok.append(f'<p class="b-lead">{e}</p>')
                elif tip == "li-cim":
                    sorok.append(f'<p class="b-li b-li-cim">{e}</p>')
                elif tip == "li":
                    sorok.append(f'<p class="b-li">{e}</p>')
                elif tip == "kerdes":
                    sorok.append(f'<p class="b-kerdes">{e}</p>')
                elif tip == "valasz":
                    sorok.append(f'<p class="b-valasz">{e}</p>')
                elif tip == "tabla":
                    sorok.append(f'<p class="b-tabla">{e}</p>')
                elif tip == "kep":
                    sorok.append(f'<p class="b-kep">{e}</p>')
                elif tip == "cta":
                    sorok.append(f'<p class="b-cta">{e}</p>')
                elif tip == "mezo":
                    sorok.append(f'<p class="b-mezo">{e}</p>')
                else:
                    sorok.append(f'<p class="b-p">{e}</p>')

            kereso = h(" ".join(s for _t, s in o["blokkok"])[:6000].lower()
                       + " " + o["cim"].lower() + " " + o["utvonal"].lower())
            torzs.append(
                f'<article class="oldal" id="{aid}" data-kat="{kid}" '
                f'data-kereso="{kereso}">'
                f'<header class="o-fej">'
                f'<p class="o-kat">{h(csoport["kat"])}</p>'
                f'<h2 class="o-cim">{h(o["cim"])}</h2>'
                f'<p class="o-meta"><code>{h(o["utvonal"])}</code>'
                f'<span>{o["szavak"]} szó</span></p></header>'
                f'<div class="o-torzs">{"".join(sorok)}</div></article>')

        menu.append(
            f'<section class="m-csoport" data-kat="{kid}">'
            f'<h2 class="m-kat">{h(csoport["kat"])}'
            f'<span class="m-db">{len(csoport["tetelek"])}</span></h2>'
            f'<ul class="m-lista">{"".join(elemek)}</ul></section>')

    chipek = "".join(
        f'<button class="chip" data-szur="k{ci}">{h(c["kat"])}</button>'
        for ci, c in enumerate(fa))

    return (TPL
            .replace("/*FONTCSS*/", fontcss)
            .replace("{{VERZIO}}", h(VERZIO))
            .replace("{{OLDAL}}", str(ossz["oldal"]))
            .replace("{{SZAVAK}}", f"{ossz['szavak']:,}".replace(",", " "))
            .replace("{{KARAKTER}}", f"{ossz['karakter']:,}".replace(",", " "))
            .replace("{{MENU}}", "".join(menu))
            .replace("{{CHIPEK}}", chipek)
            .replace("{{TOC}}", "".join(toc))
            .replace("{{TORZS}}", "".join(torzs)))


TPL = """<meta charset="utf-8">
<title>ÖkoTech Home — szövegkivonat</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
/*FONTCSS*/

:root {
  --forest:#133216; --oliveleaf:#56642B; --fern:#80A640; --lime:#E5EBBB;
  --drizzle:#F3F2EC; --stardust:#FAFAFA; --amber:#C98A1D;

  --ground:var(--drizzle); --surface:var(--stardust); --sunken:#EBEAE1;
  --ink:var(--forest); --ink-2:var(--oliveleaf); --ink-3:#7C8560;
  --vonal:#DDDCCF; --vonal-halk:#E8E7DC;
  --el:var(--fern); --kiemel:#FFF3C4;
  --font-fej:'Zilla Slab',Georgia,serif;
  --font-torzs:'IBM Plex Sans',system-ui,sans-serif;
  --font-adat:'IBM Plex Mono',ui-monospace,monospace;
  --menu-w:22rem;
}
@media (prefers-color-scheme:dark) {
  :root:not([data-tema="vilagos"]) {
    --ground:#0E2612; --surface:#16331A; --sunken:#1C3D20;
    --ink:#EDF2E2; --ink-2:#B9C99A; --ink-3:#8B9C6E;
    --vonal:#2A4A2C; --vonal-halk:#213C24;
    --el:#9CC258; --kiemel:#4A431A;
  }
}
:root[data-tema="sotet"] {
  --ground:#0E2612; --surface:#16331A; --sunken:#1C3D20;
  --ink:#EDF2E2; --ink-2:#B9C99A; --ink-3:#8B9C6E;
  --vonal:#2A4A2C; --vonal-halk:#213C24;
  --el:#9CC258; --kiemel:#4A431A;
}

*,*::before,*::after { box-sizing:border-box }
html { scroll-behavior:smooth; scroll-padding-top:1rem }
body {
  margin:0; background:var(--ground); color:var(--ink);
  font-family:var(--font-torzs); font-size:16px; line-height:1.6;
  -webkit-font-smoothing:antialiased;
}

/* ---------- elrendezés ---------- */
.keret { display:grid; grid-template-columns:var(--menu-w) minmax(0,1fr) }
.menu {
  position:sticky; top:0; height:100vh; overflow-y:auto;
  background:var(--surface); border-right:1px solid var(--vonal);
  padding:1.25rem 1rem 4rem;
}
.tartalom { padding:2.5rem clamp(1rem,4vw,3.5rem) 6rem; max-width:56rem }

/* ---------- menü ---------- */
.m-fej { position:sticky; top:0; background:var(--surface); padding-bottom:.75rem;
  margin:-1.25rem -1rem .5rem; padding:1.25rem 1rem .75rem;
  border-bottom:1px solid var(--vonal-halk); z-index:5 }
.m-logo { font-family:var(--font-adat); font-size:10px; letter-spacing:.18em;
  text-transform:uppercase; color:var(--ink-3); margin:0 0 .5rem }
.m-cimke { font-family:var(--font-fej); font-size:1.25rem; font-weight:600;
  margin:0 0 .75rem; line-height:1.2 }
#kereso {
  width:100%; padding:.6rem .75rem; font:inherit; font-size:.9rem;
  color:var(--ink); background:var(--ground);
  border:1px solid var(--vonal); border-radius:.4rem;
}
#kereso:focus-visible { outline:2px solid var(--el); outline-offset:1px }
.talalat { font-family:var(--font-adat); font-size:11px; color:var(--ink-3);
  margin:.5rem 0 0; min-height:1.2em }
.chipek { display:flex; flex-wrap:wrap; gap:.3rem; margin:.6rem 0 0 }
.chip {
  font:inherit; font-size:.72rem; padding:.22rem .55rem; cursor:pointer;
  background:var(--ground); color:var(--ink-2);
  border:1px solid var(--vonal); border-radius:1rem;
}
.chip:hover { border-color:var(--el); color:var(--ink) }
.chip[aria-pressed="true"] { background:var(--el); border-color:var(--el); color:#fff }

.m-csoport { margin:1.5rem 0 0 }
.m-kat {
  font-family:var(--font-adat); font-size:10.5px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-3);
  margin:0 0 .4rem; display:flex; justify-content:space-between; gap:.5rem;
  border-bottom:1px solid var(--vonal-halk); padding-bottom:.35rem;
}
.m-db { color:var(--ink-3) }
.m-lista { list-style:none; margin:0; padding:0 }
.m-lista a {
  display:flex; justify-content:space-between; gap:.6rem; align-items:baseline;
  padding:.3rem .45rem; border-radius:.3rem; text-decoration:none;
  color:var(--ink-2); font-size:.875rem; line-height:1.35;
}
.m-lista a:hover { background:var(--sunken); color:var(--ink) }
.m-lista a:focus-visible { outline:2px solid var(--el); outline-offset:1px }
.m-lista .m2 a { padding-left:1.15rem; font-size:.82rem; color:var(--ink-3) }
.m-lista .m2 a::before { content:"└ "; color:var(--vonal) }
.m-szo { font-family:var(--font-adat); font-size:10px; color:var(--ink-3);
  flex:none; opacity:.7 }
.m-lista a.aktiv { background:var(--sunken); color:var(--ink); font-weight:600;
  box-shadow:inset 2px 0 0 var(--el) }

/* ---------- fejléc ---------- */
.fej { border-bottom:2px solid var(--ink); padding-bottom:1.5rem; margin-bottom:2.5rem }
.fej-kicsi { font-family:var(--font-adat); font-size:11px; letter-spacing:.16em;
  text-transform:uppercase; color:var(--ink-2); margin:0 0 .75rem }
.fej-cim { font-family:var(--font-fej); font-weight:600;
  font-size:clamp(1.9rem,4vw,2.75rem); line-height:1.08; margin:0;
  letter-spacing:-.01em }
.fej-alcim { margin:.85rem 0 0; max-width:58ch; color:var(--ink-2) }
.szamok { display:flex; flex-wrap:wrap; gap:1.5rem; margin:1.5rem 0 0 }
.szam-ertek { font-family:var(--font-adat); font-size:1.35rem; color:var(--ink) }
.szam-cimke { font-family:var(--font-adat); font-size:10px; letter-spacing:.12em;
  text-transform:uppercase; color:var(--ink-3) }
.nyomtat {
  font:inherit; font-size:.85rem; margin-top:1.5rem; cursor:pointer;
  padding:.5rem 1rem; border-radius:.35rem;
  background:var(--ink); color:var(--ground); border:1px solid var(--ink);
}
.nyomtat:hover { background:transparent; color:var(--ink) }

/* ---------- oldal ---------- */
.oldal { padding:2rem 0 2.5rem; border-bottom:1px solid var(--vonal) }
.oldal[hidden] { display:none }
.o-fej { margin:0 0 1.25rem }
.o-kat { font-family:var(--font-adat); font-size:10px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-3); margin:0 0 .35rem }
.o-cim { font-family:var(--font-fej); font-weight:600; font-size:1.75rem;
  line-height:1.15; margin:0; letter-spacing:-.01em }
.o-meta { display:flex; gap:1rem; align-items:baseline; margin:.5rem 0 0;
  font-family:var(--font-adat); font-size:11px; color:var(--ink-3) }
.o-meta code { color:var(--ink-2) }

.o-torzs > * { margin:0 0 .85rem }
.b-eyebrow { font-family:var(--font-adat); font-size:10.5px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-3); margin-top:2rem }
.b-h2 { font-family:var(--font-fej); font-size:1.3rem; font-weight:600;
  line-height:1.25; margin:.35rem 0 .75rem }
.b-eyebrow + .b-h2 { margin-top:0 }
.b-h3 { font-family:var(--font-fej); font-size:1.05rem; font-weight:600;
  margin:1.25rem 0 .5rem }
.b-lead { color:var(--ink-2); font-size:1.05rem; max-width:70ch }
.b-lead-fo { font-size:1.15rem; color:var(--ink); border-left:3px solid var(--el);
  padding-left:.9rem }
.b-p { max-width:70ch }
.b-li { max-width:70ch; padding-left:1.1rem; position:relative; color:var(--ink-2) }
.b-li::before { content:"·"; position:absolute; left:.25rem; color:var(--el);
  font-weight:700 }
.b-li-cim { color:var(--ink); font-weight:600; margin-bottom:.15rem }
.b-li-cim + .b-li { margin-top:0 }
.b-li-cim + .b-li::before { content:none }
.vizualisan-rejtett {
  position:absolute; width:1px; height:1px; margin:-1px; padding:0;
  overflow:hidden; clip:rect(0 0 0 0); clip-path:inset(50%); white-space:nowrap;
}
.b-kerdes { font-weight:600; margin-top:1.25rem; padding-left:1.6rem;
  position:relative }
.b-kerdes::before { content:"K"; position:absolute; left:0;
  font-family:var(--font-adat); font-size:11px; color:var(--el) }
.b-valasz { color:var(--ink-2); padding-left:1.6rem; position:relative;
  max-width:70ch }
.b-valasz::before { content:"V"; position:absolute; left:0;
  font-family:var(--font-adat); font-size:11px; color:var(--ink-3) }
.b-tabla { font-family:var(--font-adat); font-size:.8rem; color:var(--ink-2);
  background:var(--sunken); padding:.35rem .6rem; margin-bottom:1px }
.b-kep { font-size:.85rem; color:var(--ink-3); font-style:italic;
  border-left:2px solid var(--vonal); padding-left:.75rem }
.b-cta { font-family:var(--font-adat); font-size:.8rem; color:var(--el);
  text-transform:uppercase; letter-spacing:.06em }
.b-cta::before { content:"→ " }
.b-mezo { font-family:var(--font-adat); font-size:.8rem; color:var(--ink-3) }
.b-mezo::before { content:"▢ " }
mark { background:var(--kiemel); color:inherit; padding:0 .1em }

.ures { padding:3rem 0; color:var(--ink-3); font-style:italic }
.toc { display:none }

/* ---------- nyomtatás ---------- */
@page { size:A4; margin:16mm 15mm }
@media print {
  :root { --ground:#fff; --surface:#fff; --sunken:#f4f4ef;
          --ink:#111; --ink-2:#333; --ink-3:#666; --vonal:#ccc; --el:#4a6b1f }
  body { font-size:10.5pt; line-height:1.45 }
  .menu, .nyomtat, .chipek, #kereso, .talalat, .m-fej { display:none !important }
  .keret { display:block }
  .tartalom { padding:0; max-width:none }
  .toc { display:block; break-after:page; margin:2rem 0 0 }
  .toc h2 { font-family:var(--font-fej); font-size:1.2rem; margin:0 0 .75rem }
  .toc ul { list-style:none; margin:0; padding:0; columns:2; column-gap:2rem;
            font-size:8.5pt }
  .toc li { break-inside:avoid; margin:0 0 .2rem; display:flex; gap:.4rem;
            justify-content:space-between }
  .toc li.m2 .toc-cim { padding-left:.8rem; color:#444 }
  .toc code { font-family:var(--font-adat); font-size:7.5pt; color:#777 }
  .oldal { break-before:page; border-bottom:0; padding:0 }
  .o-cim, .b-h2, .b-h3, .b-kerdes { break-after:avoid }
  .b-p, .b-li, .b-lead, .b-valasz { orphans:2; widows:2 }
  a { color:inherit; text-decoration:none }
}

@media (max-width:900px) {
  .keret { grid-template-columns:1fr }
  .menu { position:static; height:auto; max-height:60vh; border-right:0;
          border-bottom:1px solid var(--vonal) }
}
</style>

<div class="keret">
  <aside class="menu" aria-label="Menürendszer">
    <div class="m-fej">
      <p class="m-logo">ÖkoTech Home · v{{VERZIO}}</p>
      <p class="m-cimke">Szövegkivonat</p>
      <label class="vizualisan-rejtett" for="kereso">Keresés a szövegben</label>
      <input id="kereso" type="search" placeholder="Keresés a szövegben…"
             autocomplete="off" spellcheck="false">
      <p class="talalat" id="talalat" role="status"></p>
      <div class="chipek">{{CHIPEK}}</div>
    </div>
    <nav id="menufa">{{MENU}}</nav>
  </aside>

  <main class="tartalom">
    <header class="fej">
      <p class="fej-kicsi">Verzió {{VERZIO}} · a menürendszer sorrendjében</p>
      <h1 class="fej-cim">Az oldal teljes szöveges tartalma</h1>
      <p class="fej-alcim">Minden megépült oldal látható szövege, a fejléc,
        a morzsamenü és a lábléc nélkül — azok minden oldalon azonosak.
        Bal oldalt a menürendszer, fölötte kereső. A nyomtatás PDF-be
        mentve tartalomjegyzékkel, oldalanként új lapon adja ugyanezt.</p>
      <div class="szamok">
        <div><div class="szam-ertek">{{OLDAL}}</div>
             <div class="szam-cimke">oldal</div></div>
        <div><div class="szam-ertek">{{SZAVAK}}</div>
             <div class="szam-cimke">szó</div></div>
        <div><div class="szam-ertek">{{KARAKTER}}</div>
             <div class="szam-cimke">karakter</div></div>
      </div>
      <button class="nyomtat" type="button" onclick="window.print()">
        Nyomtatás / mentés PDF-be</button>
    </header>

    <nav class="toc" aria-label="Tartalomjegyzék">
      <h2>Tartalom</h2>
      <ul>{{TOC}}</ul>
    </nav>

    <div id="torzs">{{TORZS}}</div>
    <p class="ures" id="ures" hidden>Nincs találat erre a keresésre.</p>
  </main>
</div>

<script>
(function () {
  var kereso = document.getElementById('kereso');
  var talalat = document.getElementById('talalat');
  var ures = document.getElementById('ures');
  var oldalak = Array.prototype.slice.call(
    document.querySelectorAll('.oldal'));
  var linkek = Array.prototype.slice.call(
    document.querySelectorAll('.m-lista a'));
  var chipek = Array.prototype.slice.call(document.querySelectorAll('.chip'));
  var szurtKat = null;

  function ekezet(s) {
    return s.toLowerCase()
      .replace(/[áà]/g, 'a').replace(/[éè]/g, 'e').replace(/[íì]/g, 'i')
      .replace(/[óöő]/g, 'o').replace(/[úüű]/g, 'u');
  }

  function frissit() {
    var q = ekezet(kereso.value.trim());
    var db = 0;
    oldalak.forEach(function (o) {
      var katOk = !szurtKat || o.dataset.kat === szurtKat;
      var szovegOk = !q || ekezet(o.dataset.kereso).indexOf(q) >= 0;
      var lathato = katOk && szovegOk;
      o.hidden = !lathato;
      if (lathato) db++;
    });
    linkek.forEach(function (a) {
      var cel = document.getElementById(a.dataset.cel);
      a.parentNode.hidden = cel ? cel.hidden : false;
    });
    document.querySelectorAll('.m-csoport').forEach(function (cs) {
      var van = cs.querySelector('li:not([hidden])');
      cs.hidden = !van;
    });
    ures.hidden = db > 0;
    talalat.textContent = (q || szurtKat)
      ? db + ' / ' + oldalak.length + ' oldal'
      : '';
    kiemel(q);
  }

  var kiemeltek = [];
  function kiemel(q) {
    kiemeltek.forEach(function (m) {
      var sz = document.createTextNode(m.textContent);
      m.parentNode.replaceChild(sz, m);
    });
    kiemeltek = [];
    if (q.length < 3) return;
    oldalak.filter(function (o) { return !o.hidden; })
      .slice(0, 40).forEach(function (o) {
      var seta = document.createTreeWalker(o, NodeFilter.SHOW_TEXT);
      var csomok = [], cs;
      while ((cs = seta.nextNode())) { csomok.push(cs); }
      csomok.forEach(function (n) {
        var i = ekezet(n.nodeValue).indexOf(q);
        if (i < 0 || !n.parentNode) return;
        var kozep = n.splitText(i);
        kozep.splitText(q.length);
        var m = document.createElement('mark');
        m.textContent = kozep.nodeValue;
        kozep.parentNode.replaceChild(m, kozep);
        kiemeltek.push(m);
      });
    });
  }

  var ido;
  kereso.addEventListener('input', function () {
    clearTimeout(ido);
    ido = setTimeout(frissit, 160);
  });

  chipek.forEach(function (c) {
    c.addEventListener('click', function () {
      var kat = c.dataset.szur;
      szurtKat = (szurtKat === kat) ? null : kat;
      chipek.forEach(function (x) {
        x.setAttribute('aria-pressed', String(x.dataset.szur === szurtKat));
      });
      frissit();
    });
  });

  document.addEventListener('keydown', function (e) {
    if ((e.metaKey || e.ctrlKey) && e.key === 'f') {
      e.preventDefault(); kereso.focus(); kereso.select();
    }
    if (e.key === 'Escape' && document.activeElement === kereso) {
      kereso.value = ''; frissit(); kereso.blur();
    }
  });

  if ('IntersectionObserver' in window) {
    var terkep = {};
    linkek.forEach(function (a) { terkep[a.dataset.cel] = a; });
    var figyelo = new IntersectionObserver(function (bejegyzesek) {
      bejegyzesek.forEach(function (b) {
        var a = terkep[b.target.id];
        if (!a) return;
        if (b.isIntersecting) {
          linkek.forEach(function (x) { x.classList.remove('aktiv'); });
          a.classList.add('aktiv');
          if (a.scrollIntoViewIfNeeded) { a.scrollIntoViewIfNeeded(); }
        }
      });
    }, { rootMargin: '0px 0px -75% 0px', threshold: 0 });
    oldalak.forEach(function (o) { figyelo.observe(o); });
  }
})();
</script>
"""


# ------------------------------------------------------------------ 7. PDF
# A Chrome headless nyomtatója hívásonként legfeljebb 8 oldalt ad vissza
# (151-es verzió). A dokumentumot ezért egyszer töltjük be, és `pageRanges`
# szerinti nyolcas darabokban kérjük le, majd összefűzzük — így a tördelés
# ugyanaz, mintha egyben nyomtatnánk, és nem veszhet el tartalom.
ADAG = 8


class CDP:
    """Minimál DevTools-protokoll kliens (WebSocket, csak stdlib)."""

    def __init__(self, ws_url: str):
        m = re.match(r"ws://([^:/]+):(\d+)(/.*)", ws_url)
        self.s = socket.create_connection((m.group(1), int(m.group(2))),
                                          timeout=180)
        kulcs = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall(
            (f"GET {m.group(3)} HTTP/1.1\r\nHost: {m.group(1)}:{m.group(2)}\r\n"
             "Upgrade: websocket\r\nConnection: Upgrade\r\n"
             f"Sec-WebSocket-Key: {kulcs}\r\n"
             "Sec-WebSocket-Version: 13\r\n\r\n").encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.s.recv(4096)
        self.buf = bytearray(buf.split(b"\r\n\r\n", 1)[1])
        self.azon = 0

    def _kell(self, n: int):
        while len(self.buf) < n:
            r = self.s.recv(1 << 20)
            if not r:
                raise ConnectionError("a Chrome lezárta a kapcsolatot")
            self.buf += r

    def _uzenet(self) -> str:
        darabok = []
        while True:
            self._kell(2)
            fin, op = self.buf[0] & 0x80, self.buf[0] & 0x0F
            hossz, eltol = self.buf[1] & 0x7F, 2
            if hossz == 126:
                self._kell(4)
                hossz = struct.unpack(">H", bytes(self.buf[2:4]))[0]
                eltol = 4
            elif hossz == 127:
                self._kell(10)
                hossz = struct.unpack(">Q", bytes(self.buf[2:10]))[0]
                eltol = 10
            self._kell(eltol + hossz)
            adat = bytes(self.buf[eltol:eltol + hossz])
            del self.buf[:eltol + hossz]
            if op == 0x8:
                raise ConnectionError("a Chrome bontotta a kapcsolatot")
            if op == 0x9:
                continue
            darabok.append(adat)
            if fin:
                return b"".join(darabok).decode()

    def _kuld(self, adat: str):
        d = adat.encode()
        fej = bytearray([0x81])
        n = len(d)
        if n < 126:
            fej.append(0x80 | n)
        elif n < 65536:
            fej.append(0x80 | 126)
            fej += struct.pack(">H", n)
        else:
            fej.append(0x80 | 127)
            fej += struct.pack(">Q", n)
        maszk = os.urandom(4)
        fej += maszk
        self.s.sendall(bytes(fej) + bytes(b ^ maszk[i % 4]
                                          for i, b in enumerate(d)))

    def hivas(self, metodus: str, param: dict | None = None) -> dict:
        self.azon += 1
        sajat = self.azon
        self._kuld(json.dumps({"id": sajat, "method": metodus,
                               "params": param or {}}))
        while True:
            v = json.loads(self._uzenet())
            if v.get("id") == sajat:
                return v

    def varj(self, esemeny: str, mp: float = 30):
        hatarido = time.time() + mp
        while time.time() < hatarido:
            self.s.settimeout(max(1.0, hatarido - time.time()))
            try:
                v = json.loads(self._uzenet())
            except socket.timeout:
                return
            if v.get("method") == esemeny:
                return


def pdf(forras: pathlib.Path, cel: pathlib.Path) -> bool:
    if not CHROME.exists():
        print("  PDF kihagyva: a Chrome nem található.", file=sys.stderr)
        return False
    if not shutil.which("pdfunite"):
        print("  PDF kihagyva: a pdfunite hiányzik (brew install poppler).\n"
              "  A HTML-ből a Cmd+P → „Mentés PDF-ként” ugyanezt adja.",
              file=sys.stderr)
        return False

    profil = tempfile.mkdtemp(prefix="okotech-pdf-")
    folyamat = subprocess.Popen(
        [str(CHROME), "--headless=new", "--disable-gpu",
         "--remote-debugging-port=0", f"--user-data-dir={profil}",
         "about:blank"],
        stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)
    darabok: list[pathlib.Path] = []
    try:
        port = None
        hatarido = time.time() + 30
        while time.time() < hatarido:
            sor = folyamat.stderr.readline().decode(errors="replace")
            m = re.search(r"ws://127\.0\.0\.1:(\d+)/", sor)
            if m:
                port = m.group(1)
                break
        if not port:
            print("  PDF hiba: a Chrome nem indult el.", file=sys.stderr)
            return False

        lapok = json.load(urllib.request.urlopen(
            f"http://127.0.0.1:{port}/json/list", timeout=20))
        lap = next(x for x in lapok if x["type"] == "page")
        cdp = CDP(lap["webSocketDebuggerUrl"])
        cdp.hivas("Page.enable")
        cdp.hivas("Page.navigate", {"url": forras.as_uri()})
        cdp.varj("Page.loadEventFired", 60)
        time.sleep(1.5)  # a beágyazott betűtípusok kirajzolása

        elso = 1
        while True:
            v = cdp.hivas("Page.printToPDF", {
                "printBackground": True, "preferCSSPageSize": True,
                "pageRanges": f"{elso}-{elso + ADAG - 1}"})
            if "result" not in v:
                if "exceeds page count" in json.dumps(v):
                    break
                print(f"  PDF hiba: {json.dumps(v)[:300]}", file=sys.stderr)
                return False
            adat = base64.b64decode(v["result"]["data"])
            d = pathlib.Path(profil) / f"resz-{elso:04d}.pdf"
            d.write_bytes(adat)
            darabok.append(d)
            db = len(re.findall(rb"/Type\s*/Page[^s]", adat))
            if db < ADAG:
                break
            elso += ADAG

        if not darabok:
            return False
        e = subprocess.run(["pdfunite", *[str(x) for x in darabok], str(cel)],
                           capture_output=True, text=True)
        if e.returncode != 0 or not cel.exists():
            print(f"  PDF hiba az összefűzésnél: {e.stderr[-300:]}",
                  file=sys.stderr)
            return False
        return True
    finally:
        folyamat.kill()
        folyamat.wait(timeout=10)
        shutil.rmtree(profil, ignore_errors=True)


# ----------------------------------------------------------------- 8. MAIN
def main() -> None:
    fa = menufa()
    oldalak: dict[str, dict] = {}
    for csoport in fa:
        for t in csoport["tetelek"]:
            oldalak[t["url"]] = oldal(t["url"])

    ossz = {
        "oldal": len(oldalak),
        "szavak": sum(o["szavak"] for o in oldalak.values()),
        "karakter": sum(len(s) for o in oldalak.values()
                        for _t, s in o["blokkok"]),
    }

    KIMENET.mkdir(exist_ok=True)
    md_ut = KIMENET / "szoveg-kivonat.md"
    html_ut = KIMENET / "szoveg-kivonat.html"
    md_ut.write_text(markdown(fa, oldalak, ossz))
    html_ut.write_text(html_doc(fa, oldalak, ossz))

    print(f"  {md_ut.relative_to(GYOKER)}  ({md_ut.stat().st_size // 1024} KB)")
    print(f"  {html_ut.relative_to(GYOKER)}  ({html_ut.stat().st_size // 1024} KB)")
    print(f"  {ossz['oldal']} oldal · {ossz['szavak']} szó · "
          f"{ossz['karakter']} karakter")

    if "--pdf" in sys.argv:
        pdf_ut = KIMENET / "szoveg-kivonat.pdf"
        if pdf(html_ut, pdf_ut):
            print(f"  {pdf_ut.relative_to(GYOKER)}  "
                  f"({pdf_ut.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
