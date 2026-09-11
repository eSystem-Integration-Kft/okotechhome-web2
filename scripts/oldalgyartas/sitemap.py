#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sitemap.xml — a webhely térképe a keresőknek.

MIÉRT KELL. A kereső magától is bejárja a lapot, de a térkép két dolgot ad,
amit a bejárás nem: megmondja, MI LÉTEZIK (a mélyen fekvő lapok is, amikre
kevés belső hivatkozás mutat), és megmondja, MIKOR VÁLTOZOTT. Egy
száznegyvenhét lapos webhelynél ez nem formaság — a hírarchívum és a
tudástár nagy része három kattintásra van a főoldaltól.

MI KERÜL BELE. Minden kiszolgált, indexelhető lap. NEM kerül bele:

  · a hibaoldalak (401/403/404/500) — nincs mit indexelni rajtuk;
  · a `noindex` lapok — a térkép és a metasor nem mondhat mást;
  · az eredménylapok (`eredmeny`, `jelentes`) — ügyazonosítóval működnek,
    üresen semmit nem érnek;
  · az `oth-titkok/` és az `api/`.

A `lastmod` a FÁJL módosítási ideje. Nem kitalált dátum: a kereső a
hitelességét abból méri, hogy a bejelentett változás valódi-e.

A `priority` és a `changefreq` SZÁNDÉKOSAN NINCS BENNE. A Google 2023 óta
figyelmen kívül hagyja mindkettőt, és a Bing is a `lastmod`-ra támaszkodik —
ami nem számít, azt ne állítsuk be, mert a karbantartása csak félrevezetne.

FUTTATÁS:  python3 scripts/oldalgyartas/sitemap.py
"""
import datetime
import pathlib
import re

GYOKER = pathlib.Path(__file__).resolve().parents[2]
DOMAIN = 'https://okotechhome.hu'

# A TÉRKÉP AZ ÉLES FÁBÓL KÉSZÜL, nem a `_web/`-ből. A `_web/` minden lapja
# `noindex` (teszt üzemmód), tehát onnan a térkép szükségszerűen ÜRES lenne —
# és ha mégsem szűrnénk, akkor olyan lapokat jelentene be, amiket ugyanaz a
# lap a metasorában letilt. A `prod-epit.sh` hívja meg, a noindex eltávolítása
# UTÁN; első argumentumként a fa útját adja át.

# Amit nem jelentünk be. A hibaoldalak és a paraméterrel működő lapok.
KIHAGY = {
    '401', '403', '404', '500',
    'eredmeny',     # mentett ügy — ügyazonosító nélkül üres
    'jelentes',     # ajánlat-összehasonlítási jelentés — ugyanígy
}
KIHAGY_MAPPA = {'api', 'oth-titkok', 'assets'}


def utvonal(f: pathlib.Path) -> str:
    """Fájl → kiszolgált URL-útvonal. A `.html` lemarad, az `index` a mappa.

    A GYÖKÉR KÜLÖN ESET. Az `index.html` útvonala `/`, nem `//` — a listából
    kivett `index` után üres marad a rész-lista, és a záró perjel hozzáfűzése
    megduplázta volna a kezdőt. A kanonikus alak a `.htaccess`-szel is így
    egyezik (az `/index.html` 301-gyel a gyökérre megy).
    """
    rel = f.relative_to(WEB).with_suffix('')
    reszek = list(rel.parts)
    mappa_index = reszek[-1] == 'index'
    if mappa_index:
        reszek.pop()
    if not reszek:
        return '/'
    return '/' + '/'.join(reszek) + ('/' if mappa_index else '')


def gyujt():
    lapok = []
    for f in sorted(WEB.rglob('*.html')):
        rel = f.relative_to(WEB)
        if set(rel.parts) & KIHAGY_MAPPA:
            continue
        if rel.with_suffix('').as_posix() in KIHAGY or rel.stem in KIHAGY:
            continue
        szoveg = f.read_text(encoding='utf-8', errors='replace')
        # A TÉRKÉP ÉS A METASOR NEM MONDHAT MÁST. Ha a lap `noindex`, akkor a
        # bejelentése ellentmondás — a kereső ezt hibaként naplózza.
        if re.search(r'<meta name="robots"[^>]*content="[^"]*noindex', szoveg):
            continue
        mod = datetime.datetime.fromtimestamp(f.stat().st_mtime)
        lapok.append((utvonal(f), mod.strftime('%Y-%m-%d')))
    return lapok


def epit(lapok):
    sorok = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<!--',
        '  ÖkoTech Home — webhelytérkép.',
        '  GENERÁLT FÁJL: scripts/oldalgyartas/sitemap.py. Kézzel ne szerkeszd.',
        f'  Épült: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")} · {len(lapok)} lap.',
        '-->',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for ut, mod in lapok:
        sorok += ['  <url>',
                  f'    <loc>{DOMAIN}{ut}</loc>',
                  f'    <lastmod>{mod}</lastmod>',
                  '  </url>']
    sorok.append('</urlset>')
    return '\n'.join(sorok) + '\n'


if __name__ == '__main__':
    import sys
    WEB = (pathlib.Path(sys.argv[1]) if len(sys.argv) > 1
           else GYOKER / '_web_prod').resolve()
    if not WEB.is_dir():
        sys.exit(f'Nincs meg a fa: {WEB} — előbb: scripts/prod-epit.sh')
    lapok = gyujt()
    ki = WEB / 'sitemap.xml'
    ki.write_text(epit(lapok), encoding='utf-8')
    try:
        nev = ki.relative_to(GYOKER)
    except ValueError:                     # a fa a repón kívül is lehet
        nev = ki
    print(f'{nev}: {len(lapok)} lap')
    for ut, _ in lapok[:3]:
        print(f'  {DOMAIN}{ut}')
    print('  …')
