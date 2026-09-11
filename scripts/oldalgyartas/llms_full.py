#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""llms-full.txt — a webhely TELJES szövege egy fájlban, az AI-keresőknek.

A KETTŐ KÜLÖNBSÉGE. Az `llms.txt` a TÉRKÉP: megmondja, milyen lapok vannak és
melyik miről szól — a modell ebből dönti el, MIT nyisson meg. Az
`llms-full.txt` maga a TARTALOM: minden lap szövege egyben, letisztítva.
Amelyik modell nem tud (vagy nem akar) száznyolcvan lapot végigjárni, annak
ez az egy fájl elég.

MIÉRT SZÁMÍT EZ A WEBHELYNÉL. A tartalom itt műszaki válaszgyűjtemény:
határértékek, szabványhivatkozások, „mikor NEM megfelelő" szakaszok. Pont az
a fajta anyag, amit az AI-válaszgeneráló idézni szokott — ha hozzáfér.

MIT TARTALMAZ. A `<main>` szövege, Markdownná alakítva: címsorok, bekezdések,
felsorolások, táblázatok és idézetek. Ami KIMARAD: a fejléc, a lábléc, a
navigáció, a `<script>`, a `<style>`, a képek, az űrlapok és a gombok — azok
a felület részei, nem a mondanivalóé.

MIBŐL KÉSZÜL. Az ÉLES fából (`_web_prod/`), a `sitemap.py`-hoz és az
`llms.py`-hoz hasonlóan: ott már nincs `noindex`, és ami a térképen szerepel,
annak itt is szerepelnie kell. A `prod-epit.sh` hívja.

FUTTATÁS:  python3 scripts/oldalgyartas/llms_full.py [fa]
"""
import html
import pathlib
import re
import sys

GYOKER = pathlib.Path(__file__).resolve().parents[2]
DOMAIN = 'https://okotechhome.hu'

KIHAGY_MAPPA = {'api', 'assets', 'oth-titkok'}
KIHAGY_LAP = {'401', '403', '404', '500', 'eredmeny', 'jelentes'}

# A tartalmi szakaszok sorrendje — ugyanaz, mint az `llms.txt`-ben, hogy a
# két fájl együtt olvasva ne mondjon más szerkezetet.
SORREND = ['helyzetem', 'megoldasok', 'projekt-elokeszites', 'tudastar',
           'eredmenyek', 'okotech-home']


def szoveggé(h: str) -> str:
    """A `<main>` HTML-jéből Markdown. Csak a tartalmi elemeket tartja meg."""
    # 1) Ami sosem tartalom.
    h = re.sub(r'<(script|style|svg|form|nav|noscript)\b.*?</\1>', ' ', h, flags=re.S | re.I)
    h = re.sub(r'<button\b.*?</button>', ' ', h, flags=re.S | re.I)
    # A SZEKCIÓK FÖLÖTTI CÍMKESZÓ („Bevezetés", „Röviden", „1. lépés") a
    # tipográfia eszköze: a szemnek jelzi, hol tart az olvasó. Szövegfolyamban
    # árva szóként áll a címsor előtt, és a modell külön állításnak nézheti.
    h = re.sub(r'<p[^>]*class="[^"]*(?:eyebrow)[^"]*"[^>]*>.*?</p>', ' ', h,
               flags=re.S | re.I)
    # 2) Táblázat: soronként egy „a | b | c" — a cellahatár így megmarad.
    h = re.sub(r'</t[hd]>\s*<t[hd][^>]*>', ' | ', h, flags=re.I)
    h = re.sub(r'</tr>', '\n', h, flags=re.I)
    # 3) Címsorok Markdown-szintre. A lap `<h1>`-e a fájlban `##` lesz, mert a
    #    `#` a dokumentum egészéé.
    for n, jel in ((1, '##'), (2, '###'), (3, '####'), (4, '#####')):
        h = re.sub(rf'<h{n}\b[^>]*>(.*?)</h{n}>', rf'\n\n{jel} \1\n', h, flags=re.S | re.I)
    # 4) Felsorolás és bekezdés.
    h = re.sub(r'<li\b[^>]*>', '\n- ', h, flags=re.I)
    h = re.sub(r'<(p|div|section|article|tr|dt|dd|figcaption|blockquote)\b[^>]*>',
               '\n', h, flags=re.I)
    h = re.sub(r'</(p|div|section|article|li|ul|ol|dl|table|blockquote)>', '\n', h, flags=re.I)
    h = re.sub(r'<br\s*/?>', '\n', h, flags=re.I)
    # 5) A maradék jelölés el.
    h = re.sub(r'<[^>]+>', '', h)
    h = html.unescape(h)
    # 6) Térköz rendezése: legfeljebb egy üres sor, sorvégi szóköz nélkül.
    h = re.sub(r'[ \t]+', ' ', h)
    h = re.sub(r' *\n *', '\n', h)
    h = re.sub(r'\n{3,}', '\n\n', h)
    return h.strip()


def ut(f: pathlib.Path, web: pathlib.Path) -> str:
    rel = f.relative_to(web).with_suffix('')
    reszek = list(rel.parts)
    mappa = reszek[-1] == 'index'
    if mappa:
        reszek.pop()
    return '/' if not reszek else '/' + '/'.join(reszek) + ('/' if mappa else '')


def rendez(f: pathlib.Path, web: pathlib.Path):
    """A gyökér elöl, utána a szakaszok a megadott sorrendben."""
    r = f.relative_to(web)
    elso = r.parts[0] if len(r.parts) > 1 else ''
    return (SORREND.index(elso) + 1 if elso in SORREND else (0 if not elso else 99),
            r.as_posix())


def main() -> int:
    web = (pathlib.Path(sys.argv[1]) if len(sys.argv) > 1
           else GYOKER / '_web_prod').resolve()
    if not web.is_dir():
        sys.exit(f'Nincs meg a fa: {web} — előbb: scripts/prod-epit.sh')

    lapok = []
    for f in sorted(web.rglob('*.html')):
        rel = f.relative_to(web)
        if set(rel.parts) & KIHAGY_MAPPA or rel.stem in KIHAGY_LAP:
            continue
        t = f.read_text(encoding='utf-8', errors='replace')
        if re.search(r'<meta name="robots"[^>]*content="[^"]*noindex', t):
            continue
        m = re.search(r'<main\b.*?</main>', t, re.S | re.I)
        if not m:
            continue
        torzs = szoveggé(m.group(0))
        if len(torzs) < 200:          # üres vagy csak felület
            continue
        c = re.search(r'<title>(.*?)</title>', t, re.S)
        cim = html.unescape(c.group(1)).strip() if c else f.stem
        cim = re.sub(r'\s*[—|]\s*ÖkoTech[- ]Home\s*$', '', cim).strip()
        # A LAP CÍME KÉTSZER. A fájl minden laphoz kiír egy `## <cím>` sort, a
        # lap `<h1>`-e pedig ugyanazt a szöveget hozza — a modell így két
        # azonos címsort lát egymás alatt. Ha egyeznek, a törzsbelit vesszük ki.
        elso = torzs.split('\n', 1)
        if elso[0].lstrip('# ').strip() == cim:
            torzs = elso[1].lstrip('\n') if len(elso) > 1 else ''
        lapok.append((f, cim, torzs))

    lapok.sort(key=lambda x: rendez(x[0], web))

    ki = ['# ÖkoTech-Home Kft. — a webhely teljes szövege',
          '',
          'Ez a fájl a webhely MINDEN indexelhető lapjának szövegét tartalmazza,',
          'egyben, Markdown formában. A lapok listája és egymondatos leírása',
          f'külön: {DOMAIN}/llms.txt — a teljes URL-lista: {DOMAIN}/sitemap.xml',
          '',
          'Számot, határértéket és jogszabályi hivatkozást kérjük az adott lapról',
          'idézni, a forrás URL-jével együtt. A lapok címe alatt ott az URL.',
          '',
          f'Lapok száma: {len(lapok)}',
          '',
          '---',
          '']
    for f, cim, torzs in lapok:
        ki += [f'## {cim}', '', f'URL: {DOMAIN}{ut(f, web)}', '', torzs, '', '---', '']

    szoveg = '\n'.join(ki)
    cel = web / 'llms-full.txt'
    cel.write_text(szoveg, encoding='utf-8')
    print(f'llms-full.txt: {len(lapok)} lap · {len(szoveg):,} karakter '
          f'({len(szoveg.encode("utf-8")) / 1024:.0f} KB)'.replace(',', ' '))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
