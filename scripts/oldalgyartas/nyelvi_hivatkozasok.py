# -*- coding: utf-8 -*-
"""Az angol fa hivatkozásait az ANGOL lapokra irányítja.

A lapvázak akkor készültek, amikor még egyetlen angol lap sem volt, ezért minden
belső hivatkozás a magyar lapra mutatott, `hreflang="hu"` jelöléssel. Azóta
mind a 121 angol lap létezik fájlként — a menü tehát már most az angol fára
mutathat, függetlenül attól, hogy egy-egy lap tartalma még magyar-e.

Ez a szkript ÚJRAFUTTATHATÓ, és csak oda-vissza konzisztens irányba ír:
  · magyar célra mutató hivatkozás → az angol párja, ha az létezik fájlként,
  · a `hreflang="hu"` jelölés lekerül, mert a cél már az angol fában van.

Ami NEM kap angol párt (nincs a szlugtáblában — például a sitemapban szereplő,
még meg nem épített lapok), az marad a magyar fán, jelöléssel. Ez szándékos: a
törött hivatkozás rosszabb, mint a nyelvváltás.
"""
import os, re, sys, glob

ITT = os.path.dirname(__file__)
WEB = os.path.normpath(os.path.join(ITT, '..', '..', '_web'))
sys.path.insert(0, ITT)
from nyelvek import SZLUG


def atir(fajl: str) -> int:
    en_rel = os.path.relpath(fajl, os.path.join(WEB, 'en'))[:-5]
    en_dir = os.path.dirname(en_rel) or '.'
    s = open(fajl, encoding='utf-8').read()
    n = 0

    def csere(m):
        nonlocal n
        egesz, cim = m.group(0), m.group(1)
        # a magyar fára mutató hivatkozások: `../…`, esetleg több szinttel
        cel = os.path.normpath(os.path.join('en', en_dir, cim.split('#')[0].split('?')[0]))
        if cel.startswith('en' + os.sep) or cel == 'en':
            return egesz                      # már az angol fában van
        cel = cel.replace(os.sep, '/').rstrip('/')
        if cel in ('', '.'):
            cel = 'index'
        if os.path.isdir(os.path.join(WEB, cel)):
            cel += '/index'
        if cel not in SZLUG:
            return egesz                      # nincs angol párja — marad
        uj = os.path.relpath(SZLUG[cel], en_dir).replace(os.sep, '/')
        if uj.endswith('/index'):
            uj = uj[:-5]
        elif uj == 'index':
            uj = './'
        toldalek = cim[len(cim.split('#')[0].split('?')[0]):]
        n += 1
        return (egesz.replace(f'href="{cim}"', f'href="{uj}{toldalek}"')
                     .replace(' hreflang="hu"', ''))

    s = re.sub(r'<a\b[^>]*?href="((?!https?:|#|mailto:|tel:)[^"]+)"[^>]*>', csere, s)
    if n:
        open(fajl, 'w', encoding='utf-8').write(s)
    return n


if __name__ == '__main__':
    ossz = lap = 0
    for f in sorted(glob.glob(os.path.join(WEB, 'en', '**', '*.html'), recursive=True)):
        k = atir(f)
        if k:
            ossz += k; lap += 1
    print(f'{ossz} hivatkozás átirányítva az angol fára, {lap} lapon')
