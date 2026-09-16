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
kimarad; a Plex Sans változó betű, egy fájl részhalmazonként — így tizennégy
fájl marad.

A `unicode-range` MEGMARAD minden szabályban. Ez mondja meg a böngészőnek,
melyik fájlra van szüksége — enélkül mind a tizennégyet letöltené, holott
egy magyar lapon jellemzően a felére sincs szükség.

FUTTATÁS:  python3 scripts/oldalgyartas/betuk.py
"""
import pathlib
import re
import subprocess
import sys

GYOKER = pathlib.Path(__file__).resolve().parents[2]
FONTOK = GYOKER / '_web' / 'assets' / 'fonts'
# A @font-face szabályok AZ app.css JELÖLT RÉGIÓJÁBA kerülnek, nem külön
# fájlba: külön stíluslapként egy renderelést blokkoló kérés volt (mérve
# 190 ms 1,8 KiB-ért). A jelölők közti tartalmat ez a szkript írja újra.
KI = GYOKER / '_web' / 'assets' / 'css' / 'app.css'
KEZDET = '/* ===== BETŰK-KEZDET'
VEGE   = '/* ===== BETŰK-VÉGE'

# AZ IBM PLEX SANS VÁLTOZÓ BETŰ, ezért TARTOMÁNNYAL kérjük (`400..600`), nem
# súlyonként. Súlyonként kérve a Google ugyanazt a fájlt adta háromszor, három
# `@font-face`-ben — mi pedig három néven mentettük (`-400-`, `-500-`, `-600-`,
# bájtra azonos tartalommal). A böngésző az eltérő URL miatt mindet külön
# töltötte le: mérve 2026-09-16-án a főoldal 12 betűkéréséből 6 volt Plex Sans,
# 204 KB, holott két fájl (68 KB) elég. Tartománnyal EGY szabály jön,
# `font-weight: 400 600`-zal, és részhalmazonként egy fájl.
#
# A Zilla Slab és a Plex Mono NEM változó betű: náluk a Google a tartományt
# visszautasítja, ott a súlyonkénti fájl a valódi.
CSS_URL = ('https://fonts.googleapis.com/css2'
           '?family=Zilla+Slab:wght@400;500;600;700'
           '&family=IBM+Plex+Sans:wght@400..600'
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

    # A régió FEJLÉCE az app.css-ben marad (a jelölő után); ide csak a
    # szabályok jönnek, üres sor nélkül — a fájl egy évig gyorsítótárban ül,
    # de minden lapbetöltés első letöltésekor ezek is bájtok.
    sorok = []

    letoltve = 0
    for reszhalmaz, blokk in blokkok:
        if reszhalmaz not in KELL:
            continue
        csalad = re.search(r"font-family:\s*'([^']+)'", blokk).group(1)
        # Változó betűnél a súly TARTOMÁNY (`font-weight: 400 600`) — a
        # fájlnévben kötőjellel áll, hogy ne látszódjon egyetlen súlynak.
        suly = '-'.join(re.search(r'font-weight:\s*(\d+)(?:\s+(\d+))?', blokk)
                        .groups(default='')).strip('-')
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

    # BESZÚRÁS A JELÖLŐK KÖZÉ. A fájl többi része érintetlen marad — az
    # app.css kézzel karbantartott, csak ez az egy régió generált.
    teljes = KI.read_text(encoding='utf-8')
    i = teljes.index(KEZDET)
    j = teljes.index(VEGE, i)
    fejvege = teljes.index('*/\n', i) + 3          # a régió fejléckommentje marad
    KI.write_text(teljes[:fejvege] + '\n'.join(sorok) + '\n' + teljes[j:],
                  encoding='utf-8')
    meret = sum(f.stat().st_size for f in FONTOK.glob('*.woff2'))
    print(f'betűfájl: {len(list(FONTOK.glob("*.woff2")))} db '
          f'({meret / 1024:.0f} KB), ebből most letöltve: {letoltve}')
    print(f'{KI.relative_to(GYOKER)}: a BETŰK régió frissítve '
          f'({len(sorok)} sor, {len(KI.read_text(encoding="utf-8"))} bájt a teljes fájl)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
