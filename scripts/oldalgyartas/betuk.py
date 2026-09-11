#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""betuk.py — a betűkészletek letöltése a Google Fontsról, saját kiszolgálóra.

KÉT OKBÓL CSINÁLJUK, és mindkettő önmagában is elég volna.

1. SEBESSÉG. A Google Fonts stíluslapja RENDERELÉST BLOKKOL, és két IDEGEN
   kiszolgálóhoz kell hozzá kapcsolódni (`fonts.googleapis.com`, majd
   `fonts.gstatic.com`). Mindkettő külön DNS + TCP + TLS kézfogás; lassú
   mobilhálózaton ez egyenként 400-800 ms, és a lap addig nem rajzolódik ki.
   Saját kiszolgálóról a betűk a MÁR NYITOTT kapcsolaton jönnek.

2. ADATVÉDELEM. A Google Fonts betöltése a látogató IP-címét minden
   lapmegtekintéskor elküldi a Google-nek, hozzájárulás nélkül — a müncheni
   LG 2022-es ítélete (3 O 17493/20) ezt GDPR-sértésnek mondta ki. A webhely
   Cookie-tájékoztatója a hozzájárulást kategóriánként ígéri; egy mindig
   lefutó, harmadik feles kérés ezzel nem fér össze. Saját fájlból nincs
   külső kérés, tehát nincs mihez hozzájárulni.

CSAK A `latin` ÉS A `latin-ext` RÉSZHALMAZ kell. A magyar ékezetek közül az
á é í ó ö ú ü a `latin`-ban van, az ő (U+0151) és az ű (U+0171) viszont a
`latin-ext`-ben — ezért kell mind a kettő. A cirill, a görög és a vietnami
kimarad: harminchat fájlból így tizennyolc lesz.

A `unicode-range` MEGMARAD minden szabályban. Ez mondja meg a böngészőnek,
melyik fájlra van szüksége — enélkül mind a tizennyolcat letöltené, holott
egy magyar lapon jellemzően a felére sincs szükség.

FUTTATÁS:  python3 scripts/oldalgyartas/betuk.py
"""
import pathlib
import re
import subprocess
import sys

GYOKER = pathlib.Path(__file__).resolve().parents[2]
FONTOK = GYOKER / '_web' / 'assets' / 'fonts'
KI = GYOKER / '_web' / 'assets' / 'css' / 'betuk.css'

CSS_URL = ('https://fonts.googleapis.com/css2'
           '?family=Zilla+Slab:wght@400;500;600;700'
           '&family=IBM+Plex+Sans:wght@400;500;600'
           '&family=IBM+Plex+Mono:wght@400;500'
           '&display=swap')

# A böngésző-azonosító DÖNTI EL, MILYEN FORMÁTUMOT KAPUNK. Régi azonosítóval a
# Google `ttf`-et küld; ezzel a modernnel `woff2`-t, ami feleakkora.
UA = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 '
      '(KHTML, like Gecko) Version/17.0 Safari/605.1.15')

KELL = {'latin', 'latin-ext'}


def hoz(url: str) -> bytes:
    k = subprocess.run(['curl', '-sS', '-m', '40', '-A', UA, url],
                       capture_output=True)
    if k.returncode != 0 or not k.stdout:
        sys.exit(f'Nem tölthető le: {url}\n{k.stderr.decode()[:200]}')
    return k.stdout


def main() -> int:
    FONTOK.mkdir(parents=True, exist_ok=True)
    css = hoz(CSS_URL).decode('utf-8')

    # A Google a részhalmaz nevét MEGJEGYZÉSBEN írja a blokk elé:
    #     /* latin-ext */
    #     @font-face { … }
    blokkok = re.findall(r'/\*\s*([a-z0-9-]+)\s*\*/\s*(@font-face\s*\{.*?\})',
                         css, re.S)
    if not blokkok:
        sys.exit('A Google Fonts válasza nem a várt szerkezetű — a szkriptet '
                 'hozzá kell igazítani.')

    sorok = [
        '/* ==========================================================================',
        '   BETŰKÉSZLETEK — saját kiszolgálóról',
        '   --------------------------------------------------------------------------',
        '   GENERÁLT FÁJL: scripts/oldalgyartas/betuk.py. Kézzel ne szerkeszd.',
        '',
        '   Miért nem a Google Fontsról: a stíluslapja renderelést blokkol és két',
        '   idegen kiszolgálóhoz kell kapcsolódni hozzá (mobilhálózaton egyenként',
        '   400-800 ms), a betöltése pedig a látogató IP-címét minden',
        '   lapmegtekintéskor elküldi a Google-nek. Innen semmi külső kérés nincs.',
        '',
        '   Csak a `latin` és a `latin-ext` részhalmaz van meg: a magyar ő és ű a',
        '   `latin-ext`-ben él, a cirill és a görög viszont sosem kell.',
        '   ========================================================================== */',
        '',
    ]

    letoltve = 0
    for reszhalmaz, blokk in blokkok:
        if reszhalmaz not in KELL:
            continue
        csalad = re.search(r"font-family:\s*'([^']+)'", blokk).group(1)
        suly = re.search(r'font-weight:\s*(\d+)', blokk).group(1)
        url = re.search(r'url\((https://[^)]+)\)', blokk).group(1)
        nev = (csalad.lower().replace(' ', '-') + f'-{suly}-{reszhalmaz}.woff2')
        cel = FONTOK / nev
        if not cel.exists():
            cel.write_bytes(hoz(url))
            letoltve += 1
        uj = blokk.replace(url, f'../fonts/{nev}')
        # A `font-display: swap` már benne van (a lekérésben kértük): a szöveg
        # a tartalék betűvel AZONNAL látszik, és a saját betű cseréli le.
        sorok.append(f'/* {csalad} {suly} · {reszhalmaz} */')
        sorok.append(re.sub(r'\s*\n\s*', ' ', uj).strip())
        sorok.append('')

    KI.write_text('\n'.join(sorok), encoding='utf-8')
    meret = sum(f.stat().st_size for f in FONTOK.glob('*.woff2'))
    print(f'betűfájl: {len(list(FONTOK.glob("*.woff2")))} db '
          f'({meret / 1024:.0f} KB), ebből most letöltve: {letoltve}')
    print(f'{KI.relative_to(GYOKER)}: {len(KI.read_text(encoding="utf-8"))} bájt')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
