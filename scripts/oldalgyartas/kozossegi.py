#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kozossegi.py — a megosztási kártya hiányzó metaadatai.

MI HIÁNYZOTT ÉS MIÉRT SZÁMÍT. A lapokon megvolt az `og:title`, `og:description`,
`og:image`, `og:type` és `og:locale`, de öt dolog nem:

  · `og:url` .......... a megosztás kanonikus címe. Enélkül a Facebook és a
                        LinkedIn azt az URL-t jegyzi meg, AMIN a megosztó
                        éppen állt — `?gclid=…`, `?fbclid=…` farokkal együtt.
                        Ugyanannak a lapnak így több „megosztási identitása"
                        lesz, és a lájkok/megosztások szétszóródnak rajtuk.
  · `og:site_name` .... a márkanév a kártya fejlécében. Enélkül a domain áll ott.
  · `og:image:width`
    `og:image:height` . AZ ELSŐ MEGOSZTÁS MIATT. Méret nélkül a gyűjtő előbb
                        letölti a képet, hogy megmérje — és amíg ez nem kész,
                        a kártya kép nélkül jelenik meg. Az első megosztás a
                        legfontosabb, és épp az romlik el.
  · `og:image:alt` .... a kép leírása a kártyán, képernyőolvasónak.
  · `twitter:card` .... ez dönti el, hogy nagy képes vagy apró bélyeges
                        kártya lesz-e. Az X a többi mezőt az `og:`-ból veszi,
                        EZT viszont nem — ezért ez az egyetlen `twitter:` sor,
                        amit kiteszünk.

AMIT SZÁNDÉKOSAN NEM TESZÜNK KI: `twitter:title`, `twitter:description`,
`twitter:image`. Az X ezeket az `og:` megfelelőikből veszi, ha hiányoznak —
kiírva csak ugyanaz a szöveg állna kétszer minden lapon, és két helyen kellene
karbantartani. Ami két helyen áll, az előbb-utóbb két különbözőt mond.

A KÉPMÉRET A FÁJLBÓL JÖN, nem kézzel beírt számból: az `og:image` URL-jét
visszafejtjük a helyi fájlra, és megmérjük. Ha a kép cserélődik, a szám a
következő futtatáskor magától követi.

FUTTATÁS:  python3 scripts/oldalgyartas/kozossegi.py
"""
import pathlib
import re
import subprocess
import sys

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
DOMAIN = 'https://okotechhome.hu'
MARKA = 'ÖkoTech Home'

_meret_gyorsito = {}   # URL → (szélesség, magasság) vagy None


def kepmeret(url: str):
    """Az `og:image` URL-jéből a helyi fájl mérete. None, ha nem mérhető."""
    if url in _meret_gyorsito:
        return _meret_gyorsito[url]
    ut = url.split('?')[0]
    if not ut.startswith(DOMAIN + '/'):
        _meret_gyorsito[url] = None
        return None
    f = WEB / ut[len(DOMAIN) + 1:]
    if not f.is_file():
        _meret_gyorsito[url] = None
        return None
    try:
        ki = subprocess.run(['identify', '-format', '%w %h', str(f) + '[0]'],
                            capture_output=True, text=True, timeout=20)
        w, h = ki.stdout.strip().split()
        meret = (int(w), int(h))
    except Exception:
        meret = None
    _meret_gyorsito[url] = meret
    return meret


def elso(minta: str, szoveg: str):
    m = re.search(minta, szoveg)
    return m.group(1) if m else None


def main() -> int:
    bovitett = kihagyott = 0
    meret_nelkul = []

    for p in sorted(WEB.rglob('*.html')):
        s = p.read_text(encoding='utf-8')
        nev = p.relative_to(WEB).as_posix()

        # Ahol nincs `og:image`, ott nincs megosztási kártya sem — a
        # hibaoldalakat nem osztja meg senki.
        kep = elso(r'<meta property="og:image" content="([^"]+)">', s)
        kanon = elso(r'<link rel="canonical" href="([^"]+)">', s)
        if not kep or not kanon:
            kihagyott += 1
            continue
        if 'og:site_name' in s and 'twitter:card' in s and 'og:url' in s:
            continue

        sorok = []
        if 'og:url' not in s:
            sorok.append(f'<meta property="og:url" content="{kanon}">')
        if 'og:site_name' not in s:
            sorok.append(f'<meta property="og:site_name" content="{MARKA}">')
        if 'og:image:width' not in s:
            m = kepmeret(kep)
            if m:
                sorok.append(f'<meta property="og:image:width" content="{m[0]}">')
                sorok.append(f'<meta property="og:image:height" content="{m[1]}">')
            else:
                meret_nelkul.append(nev)
        if 'og:image:alt' not in s:
            # A lap CÍME a kép legpontosabb leírása, ami rendelkezésre áll: a
            # hero-kép mindig a lap tárgyát ábrázolja. Kitalálni nem fogunk.
            cim = elso(r'<meta property="og:title" content="([^"]+)">', s)
            if cim:
                sorok.append(f'<meta property="og:image:alt" content="{cim}">')
        if 'twitter:card' not in s:
            sorok.append('<meta name="twitter:card" content="summary_large_image">')

        if not sorok:
            continue

        # Az `og:image` sor UTÁN szúrunk be: a képhez tartozó kiegészítők
        # maradjanak a kép mellett, ne szóródjanak szét a fejlécben.
        horgony = f'<meta property="og:image" content="{kep}">'
        s = s.replace(horgony, horgony + '\n' + '\n'.join(sorok), 1)
        p.write_text(s, encoding='utf-8')
        bovitett += 1

    print(f'közösségi metaadatok: {bovitett} lap bővítve · {kihagyott} kihagyva '
          '(nincs og:image vagy canonical)')
    if meret_nelkul:
        print(f'  ! {len(meret_nelkul)} lapon nem volt mérhető a kép:')
        for n in meret_nelkul[:5]:
            print(f'      {n}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
