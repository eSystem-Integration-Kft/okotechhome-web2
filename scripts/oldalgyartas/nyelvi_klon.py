# -*- coding: utf-8 -*-
"""Angol lapváz készítése egy magyar lapból.

Amit elvégez, hogy kézzel ne kelljen 119-szer:
  · `<html lang="en" data-gyoker="…">` a mélységnek megfelelő gyökérelőtaggal,
  · az eszközhivatkozások (`assets/…`) átírása a helyes mélységre,
  · a belső laphivatkozások átirányítása: ha a célnak MÁR VAN angol változata,
    oda mutat; ha nincs, a magyar lapra `hreflang="hu"` jelöléssel,
  · a fejléc és a lábléc átemelése a kész angol nyitólapról — OSZTÁLYRA
    illesztve (`<footer class="lablec">`), mert a véleménykártyák szerzőblokkja
    szintén `<footer`, és az első előfordulásra illesztés korábban a lábléc
    helyére egy vélemény aláírását tette,
  · kölcsönös `hreflang` mindkét lapon, és a nyelvváltó a lap saját párjára.

A SZÖVEGET NEM FORDÍTJA. A váz elkészül, a tartalom fordítása külön lépés —
így a gépies és az ítéletet igénylő munka nem keveredik.

Használat:  python3 scripts/oldalgyartas/nyelvi_klon.py helyzetem/telekalkalmassag [...]
            python3 scripts/oldalgyartas/nyelvi_klon.py --mind
"""
import os, re, sys

GYOKER = os.path.join(os.path.dirname(__file__), '..', '..')
WEB = os.path.normpath(os.path.join(GYOKER, '_web'))
sys.path.insert(0, os.path.dirname(__file__))
from nyelvek import SZLUG


def elotag(relut: str) -> str:
    """A WEBGYÖKÉRIG vezető előtag egy `en/…` lapról.

    A `+1` az `en/` könyvtár maga: az `en/contact.html` a `_web/en`-ben ül,
    tehát az `assets/` egy szinttel FÖLÖTTE van. Enélkül a nulla mélységű
    angol lapok `en/assets/…`-t kértek volna, ami nincs.
    """
    return '../' * (relut.count('/') + 1)


def kivag(t: str, kezd: str, veg: str) -> str:
    i = t.index(kezd); j = t.index(veg, i) + len(veg)
    return t[i:j]


def klon(hu_ut: str, felulir: bool = False) -> str:
    """A vázat elkészíti. LÉTEZŐ lapot alapból NEM ír felül: a kész fordítás
    elvesztése sokkal drágább, mint egy kihagyott váz. Felülíráshoz `--felulir`."""
    en_ut = SZLUG[hu_ut]
    forras = os.path.join(WEB, hu_ut + '.html')
    cel = os.path.join(WEB, 'en', en_ut + '.html')
    if os.path.exists(cel) and not felulir:
        return ''
    os.makedirs(os.path.dirname(cel), exist_ok=True)
    s = open(forras, encoding='utf-8').read()

    fel = elotag(en_ut)          # az angol lap saját mélysége
    gyoker = fel or './'

    # 1) nyelv és gyökérjelölés
    s = re.sub(r'<html lang="hu"[^>]*>', f'<html lang="en" data-gyoker="{gyoker}">', s, count=1)

    # 2) eszközök
    s = re.sub(r'\b(href|src|data-video-webm|data-video-mp4)="((?:\.\./)*)(assets/)',
               lambda m: f'{m.group(1)}="{fel}{m.group(3)}', s)
    s = re.sub(r'\b(srcset|imagesrcset)="([^"]*)"',
               lambda m: f'{m.group(1)}="' + re.sub(r'(^|,\s*)((?:\.\./)*)(assets/)',
                                                    lambda k: k.group(1) + fel + k.group(3), m.group(2)) + '"', s)
    for f in ('favicon.ico', 'site.webmanifest'):
        s = re.sub(r'href="((?:\.\./)*)' + re.escape(f) + '"', f'href="{fel}{f}"', s)

    # 3) laphivatkozások — kész angol lapra, különben a magyarra jelölve
    hu_konyvtar = os.path.dirname(hu_ut)

    def hivatkozas(m):
        egesz, cim = m.group(0), m.group(1)
        if cim.startswith(('#', 'http', 'mailto:', 'tel:')):
            return egesz
        # a magyar lap útvonalához képest oldjuk fel
        cel_hu = os.path.normpath(os.path.join(hu_konyvtar, cim.rstrip('/') or 'index'))
        cel_hu = cel_hu.replace(os.sep, '/')
        if cel_hu in ('.', ''):
            cel_hu = 'index'
        if cel_hu.endswith('/'):
            cel_hu += 'index'
        if cel_hu in SZLUG and os.path.exists(os.path.join(WEB, 'en', SZLUG[cel_hu] + '.html')):
            uj = os.path.relpath(SZLUG[cel_hu], os.path.dirname(en_ut) or '.').replace(os.sep, '/')
            return egesz.replace(f'href="{cim}"', f'href="{uj}"')
        # Nincs még angol változat: a MAGYAR lapra megy, jelölve. Az utat
        # KISZÁMOLJUK, nem toldalékoljuk — a magyar hivatkozás a magyar lap
        # könyvtárához képest relatív, az angol lap viszont máshol ül, és a
        # naiv előtagolás emiatt `en/`-en belülre mutatott.
        uj = os.path.relpath(cel_hu, os.path.join('en', os.path.dirname(en_ut))).replace(os.sep, '/')
        return egesz.replace(f'href="{cim}"', f'href="{uj}" hreflang="hu"')

    s = re.sub(r'<a\b[^>]*?href="([^"]+)"[^>]*>', hivatkozas, s)

    # 4) fejléc és lábléc a kész angol nyitólapról — OSZTÁLYRA illesztve
    nyito = open(os.path.join(WEB, 'en', 'index.html'), encoding='utf-8').read()
    en_konyvtar = os.path.dirname(en_ut) or '.'
    en_haza = os.path.relpath('.', en_konyvtar).replace(os.sep, '/')
    en_haza = './' if en_haza == '.' else en_haza + '/'

    def blokk_hivatkozas(m):
        """A nyitólapról átemelt fejléc/lábléc hivatkozásai a NYITÓLAP mélységéhez
        készültek. Egy mélyebben ülő lapon ugyanaz a cím máshova mutat — a
        `../adatkezelesi-tajekoztato` a gyökérből a magyar lapra visz, egy
        alkönyvtárból viszont `en/adatkezelesi-tajekoztato`-ra, ami nincs.
        Ezért minden hivatkozást újraszámolunk erre a lapra."""
        egesz, cim = m.group(0), m.group(1)
        if cim.startswith(('#', 'http', 'mailto:', 'tel:')):
            return egesz
        if cim.startswith('../'):                      # magyar fa
            uj_cim = fel + cim[3:]
        elif cim in ('./', ''):                        # angol nyitólap
            uj_cim = en_haza
        else:                                          # angol fa, gyökérszinten
            uj_cim = os.path.relpath(cim, en_konyvtar).replace(os.sep, '/')
        return egesz.replace(f'href="{cim}"', f'href="{uj_cim}"')

    for kezd, veg in (('<a class="skip-link"', '</header>'), ('<footer class="lablec">', '</footer>')):
        if kezd in s and kezd in nyito:
            blokk = kivag(nyito, kezd, veg)
            blokk = blokk.replace('="../assets/', f'="{fel}assets/')
            blokk = re.sub(r'href="([^"]*)"', blokk_hivatkozas, blokk)
            s = s.replace(kivag(s, kezd, veg), blokk)

    open(cel, 'w', encoding='utf-8').write(s)
    return cel


if __name__ == '__main__':
    arg = [a for a in sys.argv[1:] if a != '--felulir']
    felulir = '--felulir' in sys.argv
    utak = sorted(SZLUG) if arg == ['--mind'] else arg
    uj = kihagy = 0
    for u in utak:
        if u not in SZLUG:
            print(f'  ! nincs a szlugtáblában: {u}'); continue
        cel = klon(u, felulir)
        if cel:
            uj += 1
        else:
            kihagy += 1
    print(f'{uj} lapváz elkészült, {kihagy} kihagyva (már létezik)')
