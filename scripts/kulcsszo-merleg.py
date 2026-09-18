#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kulcsszo-merleg.py — hol tart a webhely a kulcsszókutatáshoz képest.

MIÉRT. A 2026-09-04-i DataForSEO-kutatás 317 kifejezést adott; a 2026-09-16-i
kézi mérés óta több új lap készült (Megoldások hub, Biológiai szennyvíztisztító,
Házi szennyvíztisztító, Partnerek), és a kánon is átírta a szövegeket. Ez a
szkript ÚJRAMÉRI a lefedettséget, hogy a következő döntés adatra épüljön, ne
emlékezetre.

A SZINTEK a kutatás jelöléseit követik:
  A — a kifejezés a `<title>`-ben vagy a `<h1>`-ben áll (a legerősebb jel)
  B — alcímben (h2/h3) vagy a meta leírásban
  C — csak a folyó szövegben
  – — sehol

EGYEZTETÉS. A magyar ragozás miatt nem szó szerint keresünk: a kifejezés
szavainak TŐVÉGÉT levágjuk (a magyar toldalék hátul van), és a szavaknak
egymáshoz közel, sorrendben kell állniuk. Az egybe- és különírás („szennyvíz
tartály" / „szennyvíztartály") ugyanannak számít, ezért a szóközöket a minta
opcionálissá teszi.

FUTTATÁS:  python3 scripts/kulcsszo-merleg.py [--csak-hianyzo]
"""
import html
import json
import pathlib
import re
import sys

GYOKER = pathlib.Path(__file__).resolve().parents[1]
# A KIADOTT változatot mérjük: a `_web/` tesztüzemben noindex, a
# `_web_prod/` az, ami a keresőbe kerül.
WEB = GYOKER / '_web_prod'
KULCSSZAVAK = GYOKER / '_files' / 'kulcsszavak.json'

# A magyar toldalék hátul van, ezért a szó végét szabadon hagyjuk. Négy
# karakternél rövidebb szónál nem vágunk: abból csonk lenne, nem tő.
def to(szo):
    return re.escape(szo[:-1]) if len(szo) > 4 else re.escape(szo)


def minta(kifejezes):
    # Minden szó után jöhet toldalék (`\w*`), a szavak közé pedig szóköz vagy
    # kötőjel — vagy semmi, mert a „szennyvíz tartály” egybeírva ugyanaz.
    szavak = [to(sz) for sz in kifejezes.split()]
    return re.compile(r'\w*[\s\-]*'.join(szavak) + r'\w*', re.I)


def szoveg(t):
    t = re.sub(r'<(script|style|svg)\b.*?</\1>', ' ', t, flags=re.S | re.I)
    return html.unescape(re.sub(r'<[^>]+>', ' ', t))


def reszek(t):
    """A lap három rétege: A-jelölt, B-jelölt és a többi szöveg."""
    cim = ' '.join(re.findall(r'<title>(.*?)</title>', t, re.S)
                   + re.findall(r'<h1[^>]*>(.*?)</h1>', t, re.S))
    alcim = ' '.join(re.findall(r'<h[23][^>]*>(.*?)</h[23]>', t, re.S)
                     + re.findall(r'<meta name="description" content="([^"]*)"', t))
    return szoveg(cim), szoveg(alcim), szoveg(t)


def main():
    csak_hianyzo = '--csak-hianyzo' in sys.argv
    lapok = []
    for p in sorted(WEB.rglob('*.html')):
        if any(r in p.parts for r in ('_tst',)):
            continue
        t = p.read_text(encoding='utf-8', errors='ignore')
        if 'name="robots" content="noindex' in t:
            continue
        lapok.append(('/' + str(p.relative_to(WEB)).removesuffix('.html').removesuffix('/index'),
                      *reszek(t)))
    print(f'{len(lapok)} indexelhető lap\n')

    adat = json.loads(KULCSSZAVAK.read_text(encoding='utf-8'))
    eredmeny = []
    for k in adat:
        if k['celpiac'] != 'igen':
            continue
        m = minta(k['kulcsszo'])
        szint, hol = '–', []
        for url, cim, alcim, egesz in lapok:
            if m.search(cim):
                szint, hol = 'A', hol + [url]
            elif m.search(alcim):
                if szint != 'A':
                    szint = 'B'
                hol.append(url)
            elif m.search(egesz):
                if szint == '–':
                    szint = 'C'
                hol.append(url)
        eredmeny.append({**k, 'szint': szint, 'lapok': hol[:3], 'hany': len(hol)})

    rang = {'A': 0, 'B': 1, 'C': 2, '–': 3}
    eredmeny.sort(key=lambda x: (rang[x['szint']], -x['volumen']))

    osszeg = {s: 0 for s in rang}
    for e in eredmeny:
        osszeg[e['szint']] += e['volumen']
    print('KERESÉSI VOLUMEN SZINTENKÉNT (célpiac)')
    for s in 'ABC–':
        print(f'  {s}: {osszeg[s]:>6} /hó')
    print(f'  összesen: {sum(osszeg.values())} /hó\n')

    print('A LEGNAGYOBB HIÁNYOK (nincs a webhelyen, volumen szerint)')
    for e in eredmeny:
        if e['szint'] == '–' and e['volumen'] >= 90:
            print(f"  {e['volumen']:>5} · {e['kulcsszo']:<38} [{e['klaszter']}]")
    if csak_hianyzo:
        return

    print('\nAMI JAVULT a 09-16-i méréshez képest')
    for e in eredmeny:
        regi = e['regi_szint'][:1] if e['regi_szint'] else '–'
        if rang[e['szint']] < rang.get(regi, 3):
            print(f"  {regi} → {e['szint']}  {e['volumen']:>5} · {e['kulcsszo']:<36} {e['lapok'][0] if e['lapok'] else ''}")

    print('\nAMI ROMLOTT')
    for e in eredmeny:
        regi = e['regi_szint'][:1] if e['regi_szint'] else '–'
        if rang[e['szint']] > rang.get(regi, 3):
            print(f"  {regi} → {e['szint']}  {e['volumen']:>5} · {e['kulcsszo']}")


if __name__ == '__main__':
    main()
