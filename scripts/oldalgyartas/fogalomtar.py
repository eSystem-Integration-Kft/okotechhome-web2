#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fogalomtar.py — a Tudástár fogalomtára.

MIÉRT ÉPÜL MEG. Két okból, és mindkettő mérhető.

1. A LÁBLÉCBEN MIND A 186 LAPON OTT VOLT A HIVATKOZÁS — és 404-re mutatott.
   A sitemap régóta tervezi (`tudastar/fogalomtar`), csak nem készült el.

2. Bela kulcsszókutatása (DataForSEO, 2026-09-04) az 5. teendőként nevezi meg:
   „Fogalomtár a 9 PAA fogalmi kérdésre — ez az AI Overview-ba bekerülés
   legolcsóbb útja. 6 kulcsszóból 5-nél már ott az AI-válasz." A kilenc kérdés
   szó szerint bekerült a GYIK-be, mert azokat teszi fel a kereső.

HONNAN JÖN A TARTALOM. A `fogalomtar-forras.json`-ból, és ott minden
meghatározás mögött forrás áll: vagy a webhely SAJÁT szövege (a `lap` mező
mutatja, hova vezet tovább), vagy a projekt szakmai referenciái — a
háromnyelvű glosszárium (EN/DE megfelelők) és a jogszabályi összeállítás.
Amire nem volt forrás, az NINCS benne; a forrásfájl fel is sorolja, mi az.

MIÉRT NEM A `sablon.py`-BÓL ÉPÜL. Az a sablon még `https://okoth.hu/`-t ír a
kanonikusba és a morzsákba; egy futtatás visszahozná a régi domaint. Ez a
szkript a `hirek.py` bevált módszerét követi: a fejlécet és a láblécet egy
MEGLÉVŐ, azonos mélységű lapból emeli át, tehát a menü mindig az aktuális.

FUTTATÁS:  python3 scripts/oldalgyartas/fogalomtar.py
"""
import html as _html
import json
import pathlib
import re

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
FORRAS = pathlib.Path(__file__).resolve().parent / 'fogalomtar-forras.json'
DOMAIN = 'https://okotechhome.hu'
UT = 'tudastar/fogalomtar'
CSS_V = 238
SUTI_V = 2
SITE_V = 12      # a megamenü szkriptje
KALAUZ_V = 45    # az Öko kalauz

# A FEJLÉC ÉS A LÁBLÉC EGY AZONOS MÉLYSÉGŰ LAPBÓL jön (`tudastar/…`), ezért a
# benne álló `../` előtagok változtatás nélkül helyesek. A `hirek.py`-nak azért
# kell `melyebb()`, mert az ő lapjai egy szinttel lejjebb ülnek.
MINTA = (WEB / 'tudastar' / 'elszivarogtatas.html').read_text(encoding='utf-8')
FEJLEC = re.search(r'(<a class="skip-link".*?</header>)', MINTA, re.S).group(1)
LABLEC = re.search(r'(<!-- =+\n     LÁBLÉC.*?</footer>)', MINTA, re.S).group(1)


def esc(s):
    return _html.escape(str(s), quote=False)


def attr(s):
    return _html.escape(str(s), quote=True)


def jso(s):
    return json.dumps(str(s), ensure_ascii=False)


def horgony(s):
    """Ékezet nélküli, URL-be való azonosító a fogalom nevéből."""
    t = str(s).lower()
    for a, b in zip('áéíóöőúüű', 'aeiooouuu'):
        t = t.replace(a, b)
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    return t[:48]


def fogalom_html(f):
    nev = esc(f['nev'])
    mas = (f'\n            <span class="fogalom-masnev type-ui-caption">{esc(f["masnev"])}</span>'
           if f.get('masnev') else '')
    # AZ IDEGEN MEGFELELŐK A SZÓTÁRBÓL jönnek, és nem díszek: aki külföldi
    # adatlapot vagy szabványt olvas, ezekkel találkozik.
    nyelvek = []
    if f.get('en'):
        nyelvek.append(f'<span class="fogalom-nyelv"><abbr title="angolul">EN</abbr> {esc(f["en"])}</span>')
    if f.get('de'):
        nyelvek.append(f'<span class="fogalom-nyelv"><abbr title="németül">DE</abbr> {esc(f["de"])}</span>')
    nyelv_html = (f'\n            <span class="fogalom-nyelvek type-ui-caption">{" ".join(nyelvek)}</span>'
                  if nyelvek else '')
    tovabb = (f'\n            <span class="fogalom-tovabb type-ui-caption">'
              f'<a href="../{f["lap"]}">Részletesen →</a></span>'
              if f.get('lap') else '')
    # A MEGLÉVŐ `.fogalomtar` KOMPONENS SZERKEZETE: `<dl>` alapú definíciós
    # lista, `<dt>` a név, `<dd>` a magyarázat. Három másik lap is ezt
    # használja — újat építeni helyette azt jelentette volna, hogy két
    # fogalomtár-komponens él egymás mellett, és az egyik felülírja a másikat.
    # (Egyszer már megtörtént: a saját `.fogalom` szabályaim elrontották
    # azt a hármat, amíg ki nem derült, hogy a komponens régóta létezik.)
    return f'''        <div class="fogalom" id="f-{horgony(f['nev'])}">
          <dt class="type-ui-subtitle fogalom-nev">{nev}{mas}</dt>
          <dd class="type-ui-body fogalom-leiras">{esc(f['mit'])}{nyelv_html}{tovabb}</dd>
        </div>'''


def csoport_html(cs):
    fogalmak = '\n'.join(fogalom_html(f) for f in cs['fogalmak'])
    return f'''
  <section class="section" id="{cs['azon']}" aria-labelledby="{cs['azon']}-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Fogalmak</p>
        <h2 class="type-display-section-title section-title" id="{cs['azon']}-cim">{esc(cs['cim'])}</h2>
        <p class="type-ui-body section-lead">{esc(cs['bevezeto'])}</p>
      </header>
      <dl class="fogalomtar">
{fogalmak}
      </dl>
    </div>
  </section>'''


def epit():
    adat = json.loads(FORRAS.read_text(encoding='utf-8'))
    csoportok = adat['csoportok']
    gyik = adat['gyik']

    ugras = '\n'.join(
        f'          <li><a class="fogalom-ugras-link type-ui-button" href="#{c["azon"]}">'
        f'{esc(c["cim"].split(" — ")[0])}</a></li>' for c in csoportok)

    gyik_html = '\n'.join(f'''          <div class="fogalom-gyik-tetel">
            <h3 class="type-ui-card-title">{esc(q['k'])}</h3>
            <p class="type-ui-body">{esc(q['v'])}</p>
          </div>''' for q in gyik)

    torzs = f'''
  <section class="hero page-hero" aria-labelledby="oldal-cim">
    <div class="hero-inner">
      <div class="hero-copy">
        <nav class="breadcrumb" aria-label="Morzsamenü">
          <ol class="breadcrumb-list type-ui-caption" role="list">
            <li><a href="../">Főoldal</a></li>
            <li><a href="../tudastar/">Tudástár</a></li>
            <li aria-current="page">Fogalomtár</li>
          </ol>
        </nav>
        <h1 class="type-display-page-title hero-title" id="oldal-cim">Fogalomtár</h1>
        <p class="type-ui-body-strong hero-lead">Ugyanarra a három technológiára tíz név is
        használatban van, és a hatósági papír megint mást ír, mint a hirdetés. Itt egy helyen
        megtalálja, melyik szó mit takar — és hol olvashat róla bővebben.</p>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="ugras-cim">
    <div class="section-inner">
      <h2 class="visually-hidden" id="ugras-cim">Ugrás a fogalomcsoportokhoz</h2>
      <nav class="fogalom-ugras" aria-label="Fogalomcsoportok">
        <ul class="fogalom-ugras-lista" role="list">
{ugras}
        </ul>
      </nav>
    </div>
  </section>
{''.join(csoport_html(c) for c in csoportok)}

  <section class="section section-alt" id="gyik" aria-labelledby="gyik-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Gyakori kérdések</p>
        <h2 class="type-display-section-title section-title" id="gyik-cim">Amit a fogalmakról a leggyakrabban kérdeznek</h2>
      </header>
      <div class="fogalom-gyik">
{gyik_html}
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="tovabb-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Tovább</p>
        <h2 class="type-display-section-title section-title" id="tovabb-cim">Ha a nevek helyett a helyzete érdekli</h2>
        <p class="type-ui-body section-lead">A nevekkel nem kell bajlódnia. Írja meg, mi van most az
        ingatlanon és hogyan használják — a technológia nevét mi mondjuk meg, és azt is, hogy melyik
        illik oda.</p>
      </header>
      <p class="type-ui-body">
        <a class="btn btn-primary type-ui-button" href="../konzultacio">Konzultációt kérek</a>
        <a class="btn btn-secondary type-ui-button" href="../tudastar/">Vissza a Tudástárba</a>
      </p>
    </div>
  </section>'''

    # ---- strukturált adat ------------------------------------------------
    # A `DefinedTermSet` mondja ki géppel olvashatóan, hogy ez SZÓTÁR, nem
    # cikk; a `FAQPage` pedig a kilenc kérdést adja az AI-válaszgenerálónak.
    termek = ',\n'.join(
        f'''      {{
        "@type": "DefinedTerm",
        "name": {jso(f['nev'])},
        "description": {jso(f['mit'])},
        "inDefinedTermSet": "{DOMAIN}/{UT}"
      }}''' for c in csoportok for f in c['fogalmak'])
    kerdesek = ',\n'.join(
        f'''      {{
        "@type": "Question",
        "name": {jso(q['k'])},
        "acceptedAnswer": {{ "@type": "Answer", "text": {jso(q['v'])} }}
      }}''' for q in gyik)

    ld = f'''{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "DefinedTermSet",
      "name": "ÖkoTech Home fogalomtár — szennyvízkezelés",
      "description": "A decentralizált szennyvízkezelés fogalmai magyarul, angol és német megfelelőkkel.",
      "url": "{DOMAIN}/{UT}",
      "inLanguage": "hu-HU",
      "hasDefinedTerm": [
{termek}
      ]
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
{kerdesek}
      ]
    }},
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type":"ListItem","position":1,"name":"Főoldal","item":"{DOMAIN}/"}},
        {{"@type":"ListItem","position":2,"name":"Tudástár","item":"{DOMAIN}/tudastar/"}},
        {{"@type":"ListItem","position":3,"name":"Fogalomtár","item":"{DOMAIN}/{UT}"}}
      ]
    }}
  ]
}}'''

    cim = 'Fogalomtár — szennyvízkezelési fogalmak egyszerűen | ÖkoTech Home'
    leiras = ('Emésztő, oldómedence, szikkasztó, bioemésztő, lakosegyenérték — '
              'melyik szó mit takar, és melyik nem pontos műszaki megnevezés.')

    return f'''<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<!-- TESZT ÜZEMMÓD: élesítéskor a `prod-epit.sh` 1. rétege cseréli
     „index, follow"-ra. A `_web/` minden lapja noindex. -->
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex, notranslate, max-snippet:0, max-image-preview:none, max-video-preview:0, noai, noimageai">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(cim)}</title>
<meta name="description" content="{attr(leiras)}">
<link rel="canonical" href="{DOMAIN}/{UT}">
<meta property="og:type" content="article">
<meta property="og:title" content="{attr(cim)}">
<meta property="og:description" content="{attr(leiras)}">
<meta property="og:locale" content="hu_HU">
<!-- A betűk SAJÁT KISZOLGÁLÓRÓL jönnek; előtöltés szándékosan nincs (magas
     prioritással a hero-kép elé állna). Lásd assets/css/betuk.css. -->
<link rel="stylesheet" href="/assets/css/betuk.css?v=1">
<link rel="stylesheet" href="../assets/css/app.css?v={CSS_V}">
<!-- A témát a `data-theme` hordozza; ez a szkript írja ki, még a törzs
     feldolgozása előtt — így nincs villanás. -->
<script src="../assets/js/tema.js?v=1"></script>
<!-- Süti-hozzájárulás: a sávot és a beállításkezelőt a szkript építi. -->
<script src="/assets/js/suti.js?v={SUTI_V}" defer></script>
<!-- A MEGAMENÜT A `site.js` MŰKÖDTETI, az Ökót a `kalauz.js`. Mindkettő
     hiányzott az első kiadásból, és a lapokon emiatt nem nyílt a menü — a
     fejlécet átemeltem egy meglévő lapból, a hozzá tartozó szkripteket
     viszont nem. A fejléc MARKUPJA önmagában néma: a panelek nyitása,
     a billentyűzetes kezelés és a mobil fiók mind innen jön. -->
<script src="../assets/js/site.js?v={SITE_V}" defer></script>
<script src="../assets/js/kalauz.js?v={KALAUZ_V}" defer></script>
</head>
<body>

{FEJLEC}

<main id="fotartalom">
{torzs}
</main>

{LABLEC}

<script type="application/ld+json">
{ld}
</script>

</body>
</html>
'''


if __name__ == '__main__':
    cel = WEB / 'tudastar' / 'fogalomtar.html'
    szoveg = epit()
    cel.write_text(szoveg, encoding='utf-8')
    adat = json.loads(FORRAS.read_text(encoding='utf-8'))
    n = sum(len(c['fogalmak']) for c in adat['csoportok'])
    print(f'{cel.relative_to(GYOKER)}: {n} fogalom, {len(adat["gyik"])} kérdés, '
          f'{len(szoveg):,} bájt'.replace(',', ' '))
