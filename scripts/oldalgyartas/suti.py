#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""suti.py — a süti-hozzájárulás szkriptjét minden lapra beteszi.

MIÉRT KÜLÖN SZKRIPT ÉS NEM A SABLONBAN. A hozzájárulási sávot a `suti.js`
építi föl futásidőben, tehát a lapokba EGYETLEN sor kell. Ezt a sort harminc
oldalgyártó szkriptbe külön beírni annyi, mint harminc helyen elrontani —
és amelyikből kimarad, ott a sáv némán nem jelenik meg, miközben a mérés
esetleg fut. Egy bejáró szkript ezt kizárja: vagy minden lapon ott van, vagy
egyiken sem, és a futás kiírja a számot.

ROOT-RELATÍV ÚTVONAL (`/assets/...`), nem `../`-os. A webhely lapjai három
mélységben állnak (gyökér, `tudastar/…`, `okotech-home/hirek/…`), és a
mélységfüggő előtag pontosan az a hibaforrás, amit itt nem akarunk: egy
elrontott `../` néma 404, a sáv pedig nem jön föl. Mindkét környezet a
domain gyökeréből szolgál ki (mérve: tst és éles egyaránt 200-at ad a
`/assets/css/app.css`-re), tehát a root-relatív alak mindenhol jó.

A MÉRÉST EZ A SZKRIPT NEM TESZI BE. A `meres.js` hivatkozása csak az ÉLES
fába kerül, a `prod-epit.sh` rétegeként — a tesztoldal forgalma nem
szennyezheti be a GA4 adatait.

FUTTATÁS:  python3 scripts/oldalgyartas/suti.py
"""
import pathlib
import re
import sys

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'

SOR = ('<!-- Süti-hozzájárulás: a sávot és a beállításkezelőt a szkript építi.\n'
       '     Szkript nélkül nem marad a lapon árva, néma sáv. -->\n'
       '<script src="/assets/js/suti.js?v={v}" defer></script>\n')

MINTA = re.compile(r'<script src="/assets/js/suti\.js\?v=\d+" defer></script>')


def main() -> int:
    v = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    sor = SOR.format(v=v)
    beszurt = frissitett = kihagyott = 0

    for p in sorted(WEB.rglob('*.html')):
        s = p.read_text(encoding='utf-8')
        if '</head>' not in s:
            print(f'  ! nincs </head>: {p.relative_to(WEB)}')
            kihagyott += 1
            continue
        if MINTA.search(s):
            uj = MINTA.sub(f'<script src="/assets/js/suti.js?v={v}" defer></script>', s)
            if uj != s:
                p.write_text(uj, encoding='utf-8')
                frissitett += 1
            continue
        p.write_text(s.replace('</head>', sor + '</head>', 1), encoding='utf-8')
        beszurt += 1

    print(f'süti-szkript beszúrva: {beszurt} lapon · '
          f'verzió frissítve: {frissitett} · kihagyva: {kihagyott}')
    return 1 if kihagyott else 0


if __name__ == '__main__':
    raise SystemExit(main())
