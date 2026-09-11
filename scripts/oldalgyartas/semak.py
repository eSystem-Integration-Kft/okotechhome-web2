#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""semak.py — a hiányzó JSON-LD típusok beszúrása a meglévő `@graph`-ba.

MI VOLT MEG ÉS MI HIÁNYZOTT. A lapokon ott volt az `Organization`, a `WebSite`,
a `LocalBusiness`, a `BreadcrumbList` és a `FAQPage`. Ami nem:

    Article ..... a Tudástár lapjai valódi szakcikkek, de a kereső és az
                  AI-válaszgeneráló számára ez sehol nem volt kimondva.
                  Épp ez a típus mondja meg, hogy a lap ÁLLÍTÁSOKAT tartalmaz
                  egy témáról — egy idézhető forrás, nem egy termékoldal.
    Service ..... a Megoldások lapjai szolgáltatást írnak le (méretezés,
                  telepítés, üzemeltetés), és megmondják, HOL: ez a
                  `areaServed` a helyi keresésnél számít.
    Product ..... az A.B. Clear és az EPURECO fizikai termék. A gyártó és a
                  márka géppel olvashatóan eddig nem volt sehol.

MIÉRT BESZÚRÓ SZKRIPT ÉS NEM A SABLON. A `sablon.py` sablonja még
`https://okoth.hu/`-t ír a kanonikusba és a morzsákba; a kiadott lapokon ez
már `okotechhome.hu` (a v0.25.00 átírta). Egy újragyártás tehát VISSZAHOZNÁ a
régi domaint 786 helyen. Amíg a sablon nincs átállítva, a HTML-t utólag
egészítjük ki — ugyanúgy, mint a süti-szkriptnél és a közösségi metáknál.

AMIT SZÁNDÉKOSAN NEM TESZÜNK BELE:

  · `aggregateRating` — ahhoz valódi, ellenőrizhető értékelések kellenek.
    Kitalált csillagszám a strukturált adatban megtévesztés, és a Google
    kézi büntetéssel sújtja.
  · `offers` / `price` — a webhely szándékosan nem közöl árat (a méretezés
    dönti el). Ár nélküli `offers` érvénytelen, kitalált ár pedig hazugság.
  · `datePublished` — ezekhez a lapokhoz nincs megbízható első kiadási
    dátumunk. A fájl módosítási ideje NEM ugyanaz, és minden újragyártáskor
    változna: a kereső a hitelességet épp abból méri, hogy a bejelentett
    dátum valódi-e.

FUTTATÁS:  python3 scripts/oldalgyartas/semak.py [--proba]
"""
import html
import json
import pathlib
import re
import sys

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
DOMAIN = 'https://okotechhome.hu'

CEG = {
    '@type': 'Organization',
    'name': 'ÖkoTech-Home Kft.',
    'url': DOMAIN + '/',
}

# A TERMÉKLAPOK. Két saját berendezéscsalád; a többi megoldáslap szolgáltatást
# vagy döntéstámogatást ír le, nem terméket.
# Az EPURECO lapján MÁR VAN gazdag `Product` séma (márka, tanúsítványok,
# modellenkénti méretek) — azt nem bántjuk. Csak az A.B. Clear hiányzott.
#
# MODELLVÁLTOZATOK NINCSENEK BENNE, és ez nem hanyagság: a
# `ab-clear-modellek-es-kapacitasok` lap KÜLÖN MEGINDOKOLJA, miért nem közöl
# táblázatot („Miért nem szerepelnek a táblázatban"). Ami a lapon nem
# állítás, az a strukturált adatban sem lehet az — a séma a lap tartalmának
# géppel olvasható mása, nem egy második, bővebb adatlap.
TERMEKEK = {
    'megoldasok/ab-clear.html': {
        'nev': 'A.B. Clear biológiai szennyvíztisztító',
        'kategoria': 'Biológiai szennyvíztisztító berendezés',
        'tanusitvany': ['CE — EN 12566-3'],
    },
}

CIMKE = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S)
LEIRAS = re.compile(r'<meta name="description" content="(.*?)">', re.S)
KEP = re.compile(r'<meta property="og:image" content="(.*?)">', re.S)
KANON = re.compile(r'<link rel="canonical" href="(.*?)">', re.S)
GRAPH = re.compile(r'("@graph": \[\n)', re.S)


def tiszta(s):
    return html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s))).strip()


def mezo(minta, t):
    m = minta.search(t)
    return tiszta(m.group(1)) if m else ''


def csomopont(nev, t):
    """A laphoz illő séma — vagy None, ha ehhez a laphoz nem tartozik ilyen."""
    cim = mezo(CIMKE, t)
    leiras = mezo(LEIRAS, t)
    kep = mezo(KEP, t)
    url = mezo(KANON, t)
    if not (cim and url):
        return None

    if nev in TERMEKEK:
        p = TERMEKEK[nev]
        d = {
            '@type': 'Product',
            'name': p['nev'],
            'category': p['kategoria'],
            'description': leiras,
            'brand': {'@type': 'Brand', 'name': 'ÖkoTech-Home'},
            'manufacturer': CEG,
            'url': url,
        }
        if p.get('tanusitvany'):
            d['hasCertification'] = [{'@type': 'Certification', 'name': n}
                                     for n in p['tanusitvany']]
        if kep:
            d['image'] = kep
        return d

    if nev.startswith('tudastar/') and not nev.endswith('/index.html'):
        d = {
            '@type': 'Article',
            'headline': cim,
            'description': leiras,
            'inLanguage': 'hu-HU',
            'author': CEG,
            'publisher': CEG,
            'mainEntityOfPage': url,
        }
        if kep:
            d['image'] = kep
        return d

    if nev.startswith('megoldasok/') and not nev.endswith('/index.html'):
        return {
            '@type': 'Service',
            'name': cim,
            'description': leiras,
            'serviceType': 'Decentralizált szennyvízkezelés',
            'provider': CEG,
            'areaServed': {'@type': 'Country', 'name': 'Magyarország'},
            'url': url,
        }
    return None


def main() -> int:
    proba = '--proba' in sys.argv
    szamlalo = {}
    kihagy = 0

    for p in sorted(WEB.rglob('*.html')):
        nev = p.relative_to(WEB).as_posix()
        t = p.read_text(encoding='utf-8')
        d = csomopont(nev, t)
        if d is None:
            continue
        if f'"@type": "{d["@type"]}"' in t or f'"@type":"{d["@type"]}"' in t:
            continue
        if not GRAPH.search(t):
            print(f'  ! nincs @graph: {nev}')
            kihagy += 1
            continue
        # A `@graph` ELEJÉRE tesszük: a lap fő entitása álljon elöl, a
        # morzsa és a GYIK utána. A feldolgozók sorrendfüggetlenek, de aki
        # elolvassa a forrást, annak így mond valamit a szerkezet.
        blokk = json.dumps(d, ensure_ascii=False, indent=2)
        blokk = '    ' + blokk.replace('\n', '\n    ') + ',\n'
        if not proba:
            p.write_text(GRAPH.sub(lambda m: m.group(1) + blokk, t, count=1),
                         encoding='utf-8')
        szamlalo[d['@type']] = szamlalo.get(d['@type'], 0) + 1

    for k, v in sorted(szamlalo.items()):
        print(f'  {k:<10} {v} lapon')
    if kihagy:
        print(f'  ! {kihagy} lap kihagyva')
    if proba:
        print('  (PRÓBAMENET — semmi nem íródott)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
