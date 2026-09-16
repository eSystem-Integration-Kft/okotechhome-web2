#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""szkript_kesleltetes.py — a lap alatti widgetek szkriptjei az első kirajzolás után.

A lapokon a widget-szkriptek `defer`-rel álltak; ez a szkript helyőrzővé
alakítja őket (`<script type="text/plain" data-kesleltetett src=…>`), és
beteszi mellé az `assets/js/betolto.js`-t, amely a kirajzolás után tölti be
őket. A miértet és a mérést lásd a `betolto.js` fejében.

MI KÉSLELTETHETŐ. Ami a lap alsó részén, felhasználói műveletre dolgozik
(KESLELTETHETO). NEM kerül ide, ami az első képet alakítja (`site.js`: a
menüsor sűrűsége), ami hozzájárulást vagy mérést kezel (`suti.js`,
`meres.js`, `kampany.js`), és ami az űrlap első lépésétől működik.

A FÜGGŐSÉGEK. Egy késleltetett szkriptre nem támaszkodhat olyan, ami nem
késik — különben az a futásakor még nem találná meg. Laponként ezért
kimarad a késleltetésből:
  · `ugy.js`, ha a lapon `eredmeny-oldal.js` vagy `urlap.js` is van (OthUgy),
  · `jelentes.js`, ha `jelentes-oldal.js` is van (OthJelentes),
  · `kalauz.js`, ha `konzultacio.js` is van: az a betöltéskor jelzi a kísérőnek
    az első lapot (`konzv:lap` esemény), és egy később induló kalauz ezt
    elmulasztaná.

Idempotens; új vagy újragyártott lap után futtasd le újra — az
`ellenorzes.sh` 4. kapuja jelzi, ha egy lapon kimaradt.

FUTTATÁS:  python3 scripts/oldalgyartas/szkript_kesleltetes.py
"""
import pathlib
import re

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'
BETOLTO_V = 1

KESLELTETHETO = {'galeria', 'kalauz', 'ugy', 'ajanlo-konfig', 'ajanlo', 'aidt-konfig',
                 'ai-advisor', 'jelentes', 'ofc', 'folyamat', 'gyik'}
KIVETEL = {
    'ugy': {'eredmeny-oldal', 'urlap'},
    'jelentes': {'jelentes-oldal'},
    'kalauz': {'konzultacio'},
}

TAG = re.compile(r'<script (?:type="text/plain" data-kesleltetett )?src="(?P<src>[^"]*?/(?P<nev>[a-z-]+)\.js[^"]*)"'
                 r'(?: defer)?></script>')


def kesleltetendo(nevek):
    return {n for n in nevek & KESLELTETHETO if not (KIVETEL.get(n, set()) & nevek)}


def lapot_atir(t):
    nevek = {m['nev'] for m in TAG.finditer(t)}
    kesik = kesleltetendo(nevek)

    def csere(m):
        helyorzo = m.group(0).startswith('<script type="text/plain"')
        if m['nev'] in kesik:
            return f'<script type="text/plain" data-kesleltetett src="{m["src"]}"></script>'
        if helyorzo:
            # Korábban késleltettük, de a lapon azóta függő szkript áll.
            return f'<script src="{m["src"]}" defer></script>'
        return m.group(0)          # a többihez nem nyúlunk

    u = TAG.sub(csere, t)
    u = re.sub(r'<script src="[^"]*assets/js/betolto\.js[^"]*" defer></script>\n?', '', u)
    if kesik:
        elso = re.search(r'<script type="text/plain" data-kesleltetett src="(?P<elotag>[^"]*?)assets/js/', u)
        betolto = f'<script src="{elso["elotag"]}assets/js/betolto.js?v={BETOLTO_V}" defer></script>'
        u = u[:elso.start()] + betolto + '\n' + u[elso.start():]
    return u, len(kesik)


def main():
    atirt = 0
    for f in sorted(WEB.rglob('*.html')):
        t = f.read_text(encoding='utf-8')
        u, _ = lapot_atir(t)
        if u != t:
            f.write_text(u, encoding='utf-8')
            atirt += 1
    print(f'átírt lap: {atirt}')


if __name__ == '__main__':
    main()
