#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""partnerek.py — Rólunk → Partnerek (`/okotech-home/partnerek`).

MIÉRT. A 90-es issue („2026. 09. 015. Partnerek") négy partnert sorol fel
logóval; Bela kérése szerint kapjanak saját lapot és egy logósávot a főoldal
alján. A logók használatára van engedély (Bela, 2026-09-18).

A SZÖVEG CSAK AZT MONDJA, AMI AZ ISSUE-BAN ÁLL: cégnév, székhely, tevékenység.
Közös projektet, tagságot vagy bármilyen minősítést nem állítunk — ilyet nem
kaptunk forrásként. A honlapcímek ELLENŐRIZVE: a lap címe és székhelye egyezik
(hidrofilt.com — Nagykanizsa; sunikft.hu és esoviz.net — Suni Kft.;
maszesz.hu — MASZESZ). A HD Rotatec Kft.-hez nem találtunk működő honlapot,
ezért ott nincs hivatkozás.

A LOGÓK FEHÉR LAPON ÁLLNAK mindkét témában: az eredeti fájlok fehér hátterű
raszterek, sötét felületen kivágatlanul csúnyák lennének — a fehér kártya
egyben a logó „védőterülete" is.

A lap kerete (fejléc, lábléc, szkriptek) a `palyazatok.html`-ből jön.

FUTTATÁS:  python3 scripts/oldalgyartas/partnerek.py
"""
import html as _html
import json
import pathlib
import re

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
DOMAIN = 'https://okotechhome.hu'
UT = 'okotech-home/partnerek'
LAP = WEB / 'okotech-home' / 'partnerek.html'
MINTA_LAP = WEB / 'okotech-home' / 'palyazatok.html'

CIM = 'Partnereink — akikkel a víz körül együtt dolgozunk | ÖkoTech Home'
LEIRAS = ('Vízkezelés, esővízhasznosítás, víztározás és szakmai szövetség: ezekkel a '
          'partnerekkel dolgozunk együtt a szennyvíztisztításon túl.')
H1 = 'Partnereink'
LEAD = ('A szennyvíztisztítás ritkán áll önmagában: a víz útja a kúttól a kertig tart. '
        'Az alábbi cégekkel és szakmai szervezettel dolgozunk együtt.')

# (szlug, név, székhely, tevékenység, leírás, honlap, logó szélessége)
PARTNEREK = [
    ('hidrofilt', 'Hidrofilt Kft.', 'Nagykanizsa', 'Vízkezelés',
     'Vízkezelést tervező és kivitelező cég. Ott kapcsolódik a mi munkánkhoz, ahol az ivóvíz '
     'vagy a technológiai víz minősége külön kezelést kíván.',
     'https://hidrofilt.com', 680),
    ('suni', 'Suni Kft.', 'Budapest', 'Esővízhasznosítás',
     'Esővízgyűjtés és -hasznosítás: ciszternák, tartályok, szikkasztás. A tisztított szennyvíz '
     'elhelyezése és az esővíz kezelése ugyanazt a kérdést teszi fel — hova kerül a víz a telken.',
     'https://sunikft.hu', 231),
    ('hd-rotatec', 'HD Rotatec Kft.', 'Dabas', 'Víztározás, vízelosztás',
     'Víztározás és vízelosztás. Nagyobb kapacitású és közösségi projekteknél a tározás és a '
     'továbbítás önálló tervezési feladat.',
     None, 615),
    ('maszesz', 'MaSzeSz', 'Magyar Víz- és Szennyvíztechnikai Szövetség', 'Szakmai szövetség',
     'A hazai víz- és szennyvíztechnikai szakma szövetsége: konferenciák, szakmai kiadványok, '
     'közös gondolkodás a decentralizált szennyvízkezelésről is.',
     'https://maszesz.hu', 873),
]

NL = chr(10)


def esc(s):
    return _html.escape(str(s), quote=False)


def logo(szlug, nev, szel, elotag='../'):
    return (f'<img src="{elotag}assets/img/partnerek/{szlug}.webp?v=1" width="{szel}" height="160"\n'
            f'             alt="{_html.escape(nev, quote=True)} logója" loading="lazy" decoding="async">')


def kartyak():
    ki = []
    for szlug, nev, hely, terulet, leiras, honlap, szel in PARTNEREK:
        link = (f'{NL}          <p class="partner-link"><a class="text-link" href="{honlap}" '
                f'target="_blank" rel="noopener noreferrer"><span class="link-label">'
                f'{honlap.replace("https://", "")}<span class="action-arrow-end" aria-hidden="true">&rarr;</span>'
                f'</span></a></p>') if honlap else ''
        ki.append(f'''        <li class="card partner-kartya">
          <figure class="partner-logo">{logo(szlug, nev, szel)}</figure>
          <h3 class="type-ui-card-title partner-nev">{esc(nev)}</h3>
          <p class="type-ui-caption partner-adat">{esc(hely)} · {esc(terulet)}</p>
          <p class="type-ui-body card-text">{esc(leiras)}</p>{link}
        </li>''')
    return NL.join(ki)


def jsonld():
    szervezet = {'@type': 'Organization', 'name': 'ÖkoTech-Home Kft.', 'url': f'{DOMAIN}/'}
    graf = {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'WebPage', 'name': H1, 'description': LEIRAS, 'inLanguage': 'hu-HU',
             'url': f'{DOMAIN}/{UT}', 'publisher': szervezet,
             'mainEntity': {'@type': 'ItemList', 'itemListElement': [
                 {'@type': 'ListItem', 'position': i,
                  'item': {k: v for k, v in (('@type', 'Organization'), ('name', nev),
                                             ('url', honlap)) if v}}
                 for i, (_, nev, _, _, _, honlap, _) in enumerate(PARTNEREK, 1)]}},
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Főoldal', 'item': f'{DOMAIN}/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'ÖkoTech-Home',
                 'item': f'{DOMAIN}/okotech-home/'},
                {'@type': 'ListItem', 'position': 3, 'name': 'Partnerek', 'item': f'{DOMAIN}/{UT}'},
            ]},
        ],
    }
    return ('<script type="application/ld+json">' + NL
            + json.dumps(graf, ensure_ascii=False, indent=2) + NL + '</script>')


def epit(minta):
    t = minta
    kep = re.search(r'    <figure class="hero-media page-hero-media">.*?</figure>', t, re.S).group(0)
    fo = f'''<main id="fotartalom">

  <section class="hero page-hero" aria-labelledby="oldal-cim">
    <div class="hero-inner">
      <div class="hero-copy">
        <nav class="breadcrumb" aria-label="Morzsamenü">
          <ol class="breadcrumb-list type-ui-caption" role="list">
            <li><a href="../">Főoldal</a></li>
            <li><a href="./">ÖkoTech-Home</a></li>
            <li aria-current="page">Partnerek</li>
          </ol>
        </nav>
        <h1 class="type-display-page-title hero-title" id="oldal-cim">{esc(H1)}</h1>
        <p class="type-ui-body-strong hero-lead">{esc(LEAD)}</p>
      </div>
    </div>
{kep}
  </section>

  <section class="section" id="partnerek" aria-labelledby="partnerek-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Együttműködés</p>
        <h2 class="type-display-section-title section-title" id="partnerek-cim">Akikkel együtt dolgozunk</h2>
      </header>
      <ul class="card-grid partner-racs" role="list">
{kartyak()}
      </ul>
      <div class="folyoszoveg">
        <p class="type-ui-body">A saját területünk a szennyvíz helyben tartása és kezelése: a
          <a href="../megoldasok/">szennyvíztisztító rendszer</a> három része — a kezelés, a
          <a href="../projekt-elokeszites/tisztitomezo">vízelhelyezés</a> és az üzemeltetés.
          Ahol ezen túlmutató kérdés merül fel, ott érdemes a megfelelő szakmához fordulni.</p>
      </div>
    </div>
  </section>

  <section class="section section-alt" aria-labelledby="partner-cta-cim">
    <div class="section-inner">
      <aside class="panel-dark" aria-labelledby="partner-cta-cim">
        <div class="panel-dark-head">
          <p class="type-data-eyebrow panel-dark-eyebrow">Együttműködés</p>
          <h2 class="type-display-highlight-title panel-dark-title" id="partner-cta-cim">Dolgozna velünk?</h2>
        </div>
        <div class="panel-dark-body">
          <p class="type-ui-body panel-dark-text">Kivitelezőként, tervezőként vagy szakmai partnerként keres minket? Írja meg, milyen együttműködésre gondol, és felvesszük Önnel a kapcsolatot.</p>
          <p class="panel-dark-actions"><a class="btn btn-inverse" href="../kapcsolat">Kapcsolatfelvétel</a></p>
          <p class="type-ui-body panel-dark-text">Telefonon: <a href="tel:+3633200211">+36 33 200 211</a>.</p>
        </div>
      </aside>
    </div>
  </section>
</main>'''
    u = re.sub(r'<main id="fotartalom">.*?</main>', lambda _: fo, t, count=1, flags=re.S)
    cserek = [
        (r'<title>.*?</title>', f'<title>{esc(CIM)}</title>'),
        (r'<meta name="description" content="[^"]*">',
         f'<meta name="description" content="{_html.escape(LEIRAS)}">'),
        (r'<link rel="canonical" href="[^"]*">',
         f'<link rel="canonical" href="{DOMAIN}/{UT}">'),
        (r'<meta property="og:title" content="[^"]*">',
         f'<meta property="og:title" content="{_html.escape(H1)}">'),
        (r'<meta property="og:description" content="[^"]*">',
         f'<meta property="og:description" content="{_html.escape(LEIRAS)}">'),
        (r'<meta property="og:url" content="[^"]*">',
         f'<meta property="og:url" content="{DOMAIN}/{UT}">'),
        (r'<meta property="og:image:alt" content="[^"]*">',
         '<meta property="og:image:alt" content="Partnereink">'),
    ]
    for minta_re, uj in cserek:
        u, n = re.subn(minta_re, lambda _: uj, u, count=1)
        assert n == 1, minta_re
    u, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda _: jsonld(), u,
                   count=1, flags=re.S)
    assert n == 1
    return u


def main():
    # Meglévő lapot frissítünk, ha van; különben a mintából építünk újat.
    alap = LAP.read_text(encoding='utf-8') if LAP.exists() else MINTA_LAP.read_text(encoding='utf-8')
    LAP.write_text(epit(alap), encoding='utf-8')
    print(f'{LAP.relative_to(GYOKER)}: {LAP.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
