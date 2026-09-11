#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""leirasok.py — az ISMÉTLŐDŐ `meta description`-ök kijavítása.

MI VOLT A BAJ. Kilenc, egymással nem rokon lap ugyanazt a leírást viselte:

    eredmenyek/index · okotech-home/index · tudastar/index ·
    tudastar/tisztitoszerek · tudastar/elszivarogtatas ·
    tudastar/hogyan-tisztul-meg-a-szennyviz · tudastar/uzemeltetes-… ·
    tudastar/bioemeszto-… · tudastar/mikrobiologiai-ujjlenyomat

Mind a kilencen a mikrobiológiai ujjlenyomat lapjának szövege állt. Ez nem
szépséghiba: a kereső a leírásból dönti el, mit ígér a találat, és kilenc
azonos ígéret közül nyolc HAMIS. A Search Console külön jelenti („Duplicate
meta descriptions"), és a nem illő kivonat rontja az átkattintást azon a
nyolcon, amelyik nem erről szól.

AMIT NEM CSINÁLUNK: nem írunk új marketingszöveget. A leírás a lap SAJÁT
címéből (`<h1>`) és bevezetőjéből áll össze — abból, amit a lap amúgy is
mond. Így nem tud elcsúszni a tartalomtól, és nem kell külön karbantartani.

A HOSSZ. A Google az asztali találatban 155-160 karakter körül vág, ezért
158-nál mondathatáron, annak híján szóhatáron vágunk. Egy egész mondat mindig
jobb kivonat, mint egy csonka.

FUTTATÁS:  python3 scripts/oldalgyartas/leirasok.py [--proba]
"""
import collections
import html
import pathlib
import re
import sys

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
MAX = 158

LEIRAS = re.compile(r'<meta name="description" content="(.*?)">', re.S)
H1 = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S)
LEAD = re.compile(r'<p class="[^"]*(?:hero-lead|type-lead|section-lead)[^"]*"[^>]*>(.*?)</p>', re.S)


def tiszta(s: str) -> str:
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))).strip()


def vag(t: str, max_hossz: int = MAX) -> str:
    t = t.strip()
    if len(t) <= max_hossz:
        return t
    pont = max(t.rfind(j, 0, max_hossz + 1) for j in ('. ', '! ', '? '))
    if pont >= max_hossz * 0.55:
        return t[:pont + 1].strip()
    szo = t.rfind(' ', 0, max_hossz - 1)
    return (t[:szo] if szo > 0 else t[:max_hossz - 1]).rstrip(' ,;:–—-') + '…'


def sajat_leiras(t: str):
    """A lap saját címéből és bevezetőjéből. None, ha egyik sincs meg."""
    h = H1.search(t)
    l = LEAD.search(t)
    cim = tiszta(h.group(1)) if h else ''
    lead = tiszta(l.group(1)) if l else ''
    if not lead:
        return None
    # A CÍM CSAK AKKOR KERÜL ELÉ, ha a bevezető magában kevés. Egy jó bevezető
    # önmagában pontosabb kivonat, mint a cím megismétlése előtte.
    if len(lead) >= 110 or not cim:
        return vag(lead)
    if lead.startswith(cim):
        return vag(lead)
    # KÉT GONDOLATJEL EGY MONDATBAN elmossa, melyik mit választ el. Ha a
    # bevezetőben már van, a cím kettősponttal kapcsolódik.
    kotes = ': ' if '—' in lead else ' — '
    return vag(cim + kotes + lead[0].lower() + lead[1:] if kotes == ': ' else cim + kotes + lead)


def main() -> int:
    proba = '--proba' in sys.argv
    d2p = collections.defaultdict(list)
    for p in sorted(WEB.rglob('*.html')):
        m = LEIRAS.search(p.read_text(encoding='utf-8'))
        if m:
            d2p[tiszta(m.group(1))].append(p)

    ismetlodo = {d: ps for d, ps in d2p.items() if len(ps) > 1}
    if not ismetlodo:
        print('nincs ismétlődő leírás')
        return 0

    javitott = hagyott = 0
    for d, lapok in sorted(ismetlodo.items(), key=lambda x: -len(x[1])):
        print(f'\n{len(lapok)} lap viseli: „{d[:80]}…"')
        # A SAJÁT GAZDÁJA MEGTARTJA. Amelyik lap bevezetője egyezik a
        # leírással, azé a szöveg jog szerint — a többiről került rá.
        for p in lapok:
            t = p.read_text(encoding='utf-8')
            nev = p.relative_to(WEB).as_posix()
            l = LEAD.search(t)
            if l and tiszta(l.group(1))[:60] == d[:60]:
                print(f'   = {nev}  (ez a gazdája, marad)')
                hagyott += 1
                continue
            uj = sajat_leiras(t)
            if not uj or uj == d:
                print(f'   ! {nev}  — nincs miből leírást építeni, KÉZI munka')
                hagyott += 1
                continue
            print(f'   → {nev}\n       „{uj}"')
            if not proba:
                p.write_text(LEIRAS.sub(
                    lambda _: f'<meta name="description" content="{html.escape(uj, quote=True)}">',
                    t, count=1), encoding='utf-8')
            javitott += 1

    print(f'\n{javitott} lap leírása újraírva · {hagyott} változatlan'
          + ('   (PRÓBAMENET — semmi nem íródott)' if proba else ''))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
