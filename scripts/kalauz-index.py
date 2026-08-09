#!/usr/bin/env python3
"""Tartalomindex Ökónak — a webhely lapjaiból, a lapokból magukból.

MIÉRT A LAPOKBÓL. Külön karbantartott témalista elavulna: a sitemap már ma sem
egyezik minden ponton a valósággal. Az index a KIADOTT HTML-ből készül, tehát
azt tükrözi, ami tényleg fent van — ha egy lap megszűnik, kiesik innen is.

MI KERÜL BE. Lapon: az útvonal, a cím, a leíró meta, és a szakaszcímek a
horgonyaikkal. A szakaszcím a lényeg: Öko nem csak azt tudja megmondani, MELYIK
lapon van a válasz, hanem azt is, hogy a lap MELYIK részében — és a horgonnyal
oda is tud görgetni.

FUTTATÁS:  python3 scripts/kalauz-index.py
KIMENET:   _web/api/kalauz-index.json
"""
import json
import pathlib
import re

GYOKER = pathlib.Path(__file__).resolve().parent.parent / '_web'
KIMENET = GYOKER / 'api' / 'kalauz-index.json'

# Ezekre nem irányítunk: jogi szövegek, hibaoldalak, eszközlapok.
KIHAGY = {
    '404.html', '401.html', '403.html', '500.html',
    'jelentes.html',            # csak saját eredménnyel értelmes
}

cim_re   = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S)
desc_re  = re.compile(r'<meta name="description" content="([^"]*)"')
# Szakaszcím a horgonyával: a lapokon a <section> hordozza az id-t.
szakasz_re = re.compile(
    r'<section[^>]*\bid="([^"]+)"[^>]*>.*?<h2[^>]*>(.*?)</h2>', re.S)
# Ahol a section-nek nincs id-je, az aria-labelledby mutat a címre.
h2_re = re.compile(r'<h2[^>]*\bid="([^"]+)"[^>]*>(.*?)</h2>', re.S)


def tiszta(s: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()


def lapok():
    for p in sorted(GYOKER.rglob('*.html')):
        rel = p.relative_to(GYOKER)
        if rel.name in KIHAGY or str(rel).startswith('assets/'):
            continue
        t = p.read_text(encoding='utf-8')
        if 'noindex' in t and rel.name in ('adatkezelesi-tajekoztato.html',):
            pass  # a jogi lapokat bevesszük: gyakori kérdés, hol van
        cim = cim_re.search(t)
        if not cim:
            continue

        # A kiterjesztés nélküli útvonal a valódi URL (lásd .htaccess).
        url = str(rel).removesuffix('.html')
        if url.endswith('/index'):
            url = url.removesuffix('index')
        elif url == 'index':
            url = ''

        szakaszok = []
        for hid, h2 in h2_re.findall(t):
            szoveg = tiszta(h2)
            if szoveg and len(szakaszok) < 8:
                szakaszok.append({'cim': szoveg, 'horgony': '#' + hid})

        d = desc_re.search(t)
        yield {
            'url': '/' + url if url else '/',
            'cim': tiszta(cim.group(1)),
            'leiras': tiszta(d.group(1)) if d else '',
            'szakaszok': szakaszok,
        }


def main() -> None:
    adat = list(lapok())
    KIMENET.write_text(
        json.dumps({'lapok': adat}, ensure_ascii=False, separators=(',', ':')),
        encoding='utf-8')
    meret = KIMENET.stat().st_size
    szakasz = sum(len(l['szakaszok']) for l in adat)
    print(f'{len(adat)} lap, {szakasz} szakasz — {KIMENET.name} {meret // 1024} KB')


if __name__ == '__main__':
    main()
