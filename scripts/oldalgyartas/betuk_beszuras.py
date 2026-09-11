#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""betuk_beszuras.py — a Google Fonts hivatkozás cseréje a saját fájlokra.

A `betuk.py` letölti a betűket és megírja a `betuk.css`-t; ez a szkript a
lapokon cseréli le a hivatkozást. Három sor megy ki és három jön be:

    KI   preconnect fonts.googleapis.com        ← nincs többé idegen kapcsolat
    KI   preconnect fonts.gstatic.com
    KI   stylesheet fonts.googleapis.com/css2   ← renderelést blokkolt

    BE   preload  zilla-slab-600-latin.woff2    ← a címsorok betűje
    BE   preload  ibm-plex-sans-400-latin.woff2 ← a törzsszöveg betűje
    BE   stylesheet /assets/css/betuk.css

A KÉT ELŐTÖLTÉS SZÁNDÉKOSAN CSAK KETTŐ, és mindkettő `latin`. Ezek kellenek
biztosan minden lapon, az első képernyőn. A `latin-ext` (magyar ő és ű) és a
többi vastagság a `betuk.css` `unicode-range`-ei szerint jön, amikor kell —
előtöltve csak fölösleges sávszélesség volna azon, aki le sem görget.

A `crossorigin` A SAJÁT FÁJLNÁL IS KELL. A betűket a böngésző anonim CORS
móddal kéri le akkor is, ha egy eredetről jönnek; `crossorigin` nélkül az
előtöltés MÁSIK kérésnek számít, és a fájl kétszer jön le. Ez a némán dupla
letöltés a `preload` leggyakoribb hibája.

FUTTATÁS:  python3 scripts/oldalgyartas/betuk_beszuras.py [verzió]
"""
import pathlib
import re
import sys

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'

REGI = re.compile(
    r'[ \t]*<link rel="preconnect" href="https://fonts\.googleapis\.com">\n'
    r'[ \t]*<link rel="preconnect" href="https://fonts\.gstatic\.com" crossorigin>\n'
    r'[ \t]*<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2[^"]*">\n')

UJ = ('<!-- A betűk SAJÁT KISZOLGÁLÓRÓL jönnek. A Google Fontsról betöltve a\n'
      '     stíluslap renderelést blokkolna két idegen kézfogás után, és a\n'
      '     látogató IP-címe minden lapmegtekintéskor a Google-höz kerülne.\n'
      '     Lásd assets/css/betuk.css és scripts/oldalgyartas/betuk.py. -->\n'
      '<link rel="stylesheet" href="/assets/css/betuk.css?v={v}">\n')


def main() -> int:
    v = sys.argv[1] if len(sys.argv) > 1 else '1'
    uj = UJ.format(v=v)
    csere = mar = kihagy = 0
    for p in sorted(WEB.rglob('*.html')):
        s = p.read_text(encoding='utf-8')
        if 'assets/css/betuk.css' in s:
            s2 = re.sub(r'assets/css/betuk\.css\?v=\d+',
                        f'assets/css/betuk.css?v={v}', s)
            if s2 != s:
                p.write_text(s2, encoding='utf-8')
            mar += 1
            continue
        s2, n = REGI.subn(uj, s, count=1)
        if not n:
            kihagy += 1
            print(f'  ! nincs Google Fonts sor: {p.relative_to(WEB)}')
            continue
        p.write_text(s2, encoding='utf-8')
        csere += 1
    print(f'betűhivatkozás cserélve: {csere} lapon · már saját: {mar} · '
          f'kihagyva: {kihagy}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
