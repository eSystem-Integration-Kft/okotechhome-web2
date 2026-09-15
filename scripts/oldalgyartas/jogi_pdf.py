#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jogi_pdf.py — a jogi lapokból csatolható PDF.

MIRE KELL. A visszaigazoló levelek mellé megy az adatkezelési tájékoztató és az
ÁSZF. Hivatkozás helyett csatolmány: így bizonyítható, hogy a beküldés
pillanatában MI volt a szöveg — a weboldal változhat, a levél nem.

MIÉRT NEM A LAPOT NYOMTATJUK KI. Mérve: a `/adatkezelesi-tajekoztato` teljes
lapja Chrome-mal 857 KB, 352 beágyazott képpel — mert egy weboldal képe, nem
dokumentum. Ebből a szkriptből 232 KB lesz, hét oldalon, mert csak a szöveg
kerül bele, dokumentumtipográfiával. Egy ajánlatkérés visszaigazolása nem
hordozhat több megabájtot.

MIÉRT NEM A `prod-epit.sh` RÉSZE. Chrome kell hozzá, ami a telepítő gépen nem
feltétlenül van meg — egy build, ami a fejlesztő gépétől függ, előbb-utóbb
elromlik valaki másnál. Ez kézzel futtatandó, amikor a jogi szöveg változik; az
`ellenorzes.sh` figyelmeztet, ha a HTML frissebb a PDF-nél.

FUTTATÁS
    python3 scripts/oldalgyartas/jogi_pdf.py [alap-url]
    (alapértelmezett: https://okotechhome.hu)
"""
import html as H
import pathlib
import re
import subprocess
import sys
import tempfile
import urllib.request

GYOKER = pathlib.Path(__file__).resolve().parents[2]
CEL = GYOKER / '_web' / 'assets' / 'dok'

# lap → a csatolmány fájlneve. Ami ide kerül, azt a levelek csatolhatják.
LAPOK = {
    'adatkezelesi-tajekoztato': 'okotechhome-adatkezelesi-tajekoztato.pdf',
    'aszf':                     'okotechhome-aszf.pdf',
}

CHROME_JELOLTEK = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
]

# A dokumentum saját tipográfiája. RENDSZERBETŰ: a márkabetűt a PDF beágyazná,
# és papíron úgysincs dolga — egy adatkezelési tájékoztatót nem a betűtípusa
# miatt olvas el valaki.
STILUS = """
  @page { size:A4; margin:18mm 16mm; }
  body { font:11pt/1.5 Georgia,'Times New Roman',serif; color:#1a1a1a; margin:0; }
  h1 { font-size:19pt; margin:0 0 4mm; }
  h2 { font-size:13pt; margin:7mm 0 2mm; break-after:avoid; }
  h3 { font-size:11.5pt; margin:5mm 0 1.5mm; break-after:avoid; }
  p, li { margin:0 0 2.5mm; }
  ul, ol { margin:0 0 3mm; padding-left:6mm; }
  table { width:100%; border-collapse:collapse; font-size:9.5pt; margin:3mm 0; }
  th, td { border:1px solid #bbb; padding:1.6mm 2.2mm; text-align:left; vertical-align:top; }
  th { background:#f0efec; }
  a { color:inherit; text-decoration:none; }
  section, tr, li, table { break-inside:avoid; }
  .fejlec { border-bottom:1.5pt solid #2f4f2f; padding-bottom:3mm; margin-bottom:6mm;
            font-size:9pt; letter-spacing:.06em; text-transform:uppercase; }
"""

# Amit a dokumentumból ki kell venni: navigáció, gombok, ikonok, szkriptek.
# Ezek a KÉPERNYŐHÖZ tartoznak; papíron zaj, és a PDF méretét is ők viszik.
KIVAG = [
    r'<nav\b.*?</nav>',
    r'<button\b.*?</button>',
    r'<script\b.*?</script>',
    r'<svg\b.*?</svg>',
    r'<span class="icon[^"]*"[^>]*></span>',
    r'<span class="mega-ico"[^>]*>.*?</span>',
    r'<span class="sugo"[^>]*>.*?</span>',
    # A KÉPEK KÉTSZERESEN IS ROSSZAK ITT. Egy jogi dokumentumba a díszkép nem
    # való, és az ideiglenes fájlból a relatív URL-jük úgysem oldódik fel —
    # a Chrome ilyenkor az `alt` szöveget rakja a lapra, ami a PDF-ben
    # mondat közepén álló képleírásként jelenik meg. (Mérve: az ÁSZF első
    # oldalán ott állt a hero-kép teljes alt-szövege.)
    r'<picture\b.*?</picture>',
    r'<figure\b.*?</figure>',
    r'<img\b[^>]*>',
]


def chrome() -> str:
    for u in CHROME_JELOLTEK:
        if pathlib.Path(u).is_file():
            return u
    sys.exit('Nincs meg a Chrome. A PDF-generálás fejlesztői gépen fut — '
             'lásd a fájl fejlécét.')


def letolt(url: str) -> str:
    keres = urllib.request.Request(url, headers={'User-Agent': 'oth-jogi-pdf'})
    with urllib.request.urlopen(keres, timeout=30) as v:
        return v.read().decode('utf-8')


def dokumentum(lap_html: str, cegnev: str) -> str:
    m = re.search(r'<main[^>]*>(.*?)</main>', lap_html, re.S)
    if not m:
        raise SystemExit('Nincs <main> a lapon — a sablon megváltozott.')
    torzs = m.group(1)
    for minta in KIVAG:
        torzs = re.sub(minta, '', torzs, flags=re.S)

    cim = re.search(r'<title>([^<]*)</title>', lap_html).group(1).split('|')[0].strip()
    return (f'<!doctype html><html lang="hu"><meta charset="utf-8">'
            f'<title>{H.escape(cim)}</title><style>{STILUS}</style>'
            f'<p class="fejlec">{H.escape(cegnev)}</p>{torzs}</html>')


def main() -> int:
    alap = (sys.argv[1] if len(sys.argv) > 1 else 'https://okotechhome.hu').rstrip('/')
    CEL.mkdir(parents=True, exist_ok=True)
    ch = chrome()

    for szlug, fajl in LAPOK.items():
        lap = letolt(f'{alap}/{szlug}')
        doc = dokumentum(lap, 'ÖkoTech-Home Kft. · okotechhome.hu')

        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False,
                                         encoding='utf-8') as t:
            t.write(doc)
            atmeneti = t.name

        ki = CEL / fajl
        subprocess.run(
            [ch, '--headless', '--disable-gpu', '--no-sandbox',
             '--no-pdf-header-footer', f'--print-to-pdf={ki}',
             f'file://{atmeneti}'],
            check=True, capture_output=True, timeout=120,
        )
        pathlib.Path(atmeneti).unlink(missing_ok=True)
        print(f'  {fajl}: {ki.stat().st_size / 1024:.0f} KB')

    print(f'{len(LAPOK)} dokumentum kész — {CEL.relative_to(GYOKER)}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
