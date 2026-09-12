#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aria-ellenor.py — ARIA-attribútum a NEM MEGFELELŐ szerepen.

MIÉRT VAN ERRE SZÜKSÉG. Az `aria-selected="true"` egy szerep nélküli
`<button>`-on nem hibaüzenetet ad, hanem SEMMIT: a képernyőolvasó egyszerűen
figyelmen kívül hagyja, és az állapot némán elveszik. A lap ettől működik, jól
néz ki, és a hiba csak egy külső auditból derül ki (Lighthouse:
„Elements must only use supported ARIA attributes"). Épp ezért való gépi
ellenőrzésbe: amit a szem nem lát, azt ellenőrizni kell.

MIT NÉZ. Azokat az ARIA-attribútumokat, amelyek CSAK meghatározott szerepeken
értelmesek. A szerep jöhet kiírva (`role="tab"`) vagy az elem alapértelmezett
szerepéből (`<option>` → option, `<th>` → columnheader/rowheader).

MIT NEM NÉZ. Az `aria-label`, `aria-hidden`, `aria-describedby` és társaik
globálisak — azok bármely elemen állhatnak. Ez a szkript nem teljes ARIA-
validátor, hanem épp azt a hibaosztályt fogja meg, amibe egyszer beleestünk.
"""
import pathlib
import re
import sys

# attribútum → mely szerepeken értelmes (üres halmaz = csak kiírt szerep kell)
KOTOTT = {
    'aria-selected':  {'option', 'tab', 'row', 'gridcell', 'columnheader', 'rowheader', 'treeitem'},
    'aria-checked':   {'checkbox', 'radio', 'menuitemcheckbox', 'menuitemradio', 'option', 'switch', 'treeitem'},
    'aria-posinset':  {'article', 'listitem', 'menuitem', 'option', 'radio', 'tab', 'treeitem', 'comment', 'row'},
    'aria-setsize':   {'article', 'listitem', 'menuitem', 'option', 'radio', 'tab', 'treeitem', 'comment', 'row'},
    'aria-level':     {'heading', 'listitem', 'row', 'treeitem', 'comment'},
    'aria-sort':      {'columnheader', 'rowheader'},
    'aria-multiselectable': {'grid', 'listbox', 'tablist', 'tree', 'treegrid'},
    'aria-required':  {'combobox', 'gridcell', 'listbox', 'radiogroup', 'spinbutton',
                       'textbox', 'tree', 'columnheader', 'rowheader', 'checkbox', 'switch'},
}

# az elemek SAJÁT (implicit) szerepe, ahol ez számít
SAJAT_SZEREP = {
    'option': 'option', 'th': 'columnheader', 'td': 'gridcell', 'tr': 'row',
    'li': 'listitem', 'h1': 'heading', 'h2': 'heading', 'h3': 'heading',
    'h4': 'heading', 'h5': 'heading', 'h6': 'heading',
    'input': None,      # a típusától függ — az `input`-ot kihagyjuk
    'select': 'listbox',
}

ELEM = re.compile(r'<([a-z][a-z0-9]*)\b([^>]*)>', re.I)


def ellenoriz(szoveg: str):
    hibak = []
    for m in ELEM.finditer(szoveg):
        tag, attrok = m.group(1).lower(), m.group(2)
        if 'aria-' not in attrok:
            continue
        r = re.search(r'\brole="([^"]+)"', attrok)
        szerep = r.group(1).split()[0] if r else SAJAT_SZEREP.get(tag, '')
        if tag == 'input':
            continue
        for attr, engedett in KOTOTT.items():
            if re.search(rf'\b{attr}=', attrok) and szerep not in engedett:
                hibak.append((attr, szerep or '(nincs)', tag,
                              m.group(0)[:100].replace('\n', ' ')))
    return hibak


def main() -> int:
    gyoker = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '_web')
    osszes, rossz = 0, 0
    latott = set()
    for f in sorted(gyoker.rglob('*.html')):
        osszes += 1
        for attr, szerep, tag, minta in ellenoriz(f.read_text(encoding='utf-8')):
            rossz += 1
            kulcs = (attr, szerep, tag)
            if kulcs not in latott:
                latott.add(kulcs)
                print(f'  ✕ {attr} a(z) <{tag}> elemen, szerep: {szerep}')
                print(f'      {minta}')
                print(f'      először itt: {f.relative_to(gyoker)}')
    if rossz:
        print(f'\n  {rossz} előfordulás {len(latott)} különböző alakban, {osszes} lapon')
        return 1
    print(f'  ✓ {osszes} lapon nincs szerephez nem illő ARIA-attribútum')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
