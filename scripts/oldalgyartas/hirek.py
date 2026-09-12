#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hírek — gyűjtőlap és hírrészletek generátora.

MIÉRT GENERÁLT. Negyvenkét hírrészlet és egy gyűjtőlap: kézzel írva a fejléc,
a lábléc, a morzsamenü és a strukturált adat negyvenháromszor duplikálódna, és
az első javításnál szétcsúszna. A TARTALOM nem itt él, hanem a
`hirek-forras.json`-ban — ez a fájl csak a HTML-t rakja össze belőle.

EGY HÍR TÖRLÉSE: vedd ki a bejegyzését a `hirek-forras.json`-ból, futtasd újra
ezt a szkriptet, és töröld a hozzá tartozó `.html`-t meg a képeit. A szkript
nem takarít maga után — azt szándékosan nem bízzuk rá, mert egy elgépelt szlug
így nem törölne le fájlokat.

FEJLÉC ÉS LÁBLÉC. Egy meglévő lapból emeljük ki (`okotech-home/cegunkrol.html`),
ahogy a `sablon.py` is teszi: amíg nincs build-lépés, ez az egyetlen mód, hogy
a menü ne tudjon szétcsúszni. A hírrészletek EGGYEL MÉLYEBBEN vannak, ezért
ott a relatív útvonalak egy szinttel hosszabbak.

FUTTATÁS:  python3 scripts/oldalgyartas/hirek.py
"""
import html as _html
import json
import pathlib
import re

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
FORRAS = pathlib.Path(__file__).resolve().parent / 'hirek-forras.json'

CSS_V = 237          # süti-hozzájárulás: sáv és beállításkezelő
JS_SITE_V = 12
JS_KALAUZ_V = 45
JS_HIREK_V = 3      # a szűrő csak a kártyákat veszi
KEP_V = 1            # az assets/img/hirek/ első kiadása

DOMAIN = 'https://okotechhome.hu'
SZAKASZ_URL = 'okotech-home/hirek'

HONAP = ['január', 'február', 'március', 'április', 'május', 'június',
         'július', 'augusztus', 'szeptember', 'október', 'november', 'december']
# Az idővonalon az ÉV a tengelyen áll, ezért az eseménynél csak hónap és nap
# kell. Rövidítve, mert a hasáb 13,5rem széles.
HONAP_ROVID = ['jan.', 'febr.', 'márc.', 'ápr.', 'máj.', 'jún.',
               'júl.', 'aug.', 'szept.', 'okt.', 'nov.', 'dec.']

# Rovatonként egy ikon — a kép nélküli hírek keretében ez áll a fénykép
# helyett. A rajzolatok a meglévő készletből valók, nem újak.
ROVAT_IKON = {
    'vallalati-hirek': 'icon-nav-hirek',
    'kiallitasok-es-esemenyek': 'icon-nav-kozossegi',
    'palyazatok-es-fejlesztesek': 'icon-nav-bizonyitek',
}

# ---------------------------------------------------------------------------
# Fejléc és lábléc egy meglévő lapból
# ---------------------------------------------------------------------------
MINTA = (WEB / 'okotech-home' / 'cegunkrol.html').read_text(encoding='utf-8')
FEJLEC = re.search(r'(<a class="skip-link".*?</header>)', MINTA, re.S).group(1)
LABLEC = re.search(r'(<!-- =+\n     LÁBLÉC.*?</footer>)', MINTA, re.S).group(1)


def melyebb(s):
    """Egy szinttel mélyebbre tolt relatív útvonalak (`../` → `../../`)."""
    return s.replace('="../', '="../../').replace(' ../assets/', ' ../../assets/')


def esc(s):
    return _html.escape(s, quote=False)


def attr(s):
    return _html.escape(s, quote=True)


def jso(s):
    return json.dumps(s, ensure_ascii=False)


def szoveg(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()


def datum_hu(iso):
    ev, ho, nap = iso.split('-')
    return f'{ev}. {HONAP[int(ho) - 1]} {int(nap)}.'


def datum_rovid(iso):
    _, ho, nap = iso.split('-')
    return f'{HONAP_ROVID[int(ho) - 1]} {int(nap)}.'


def kep_ut(elo, fajl):
    return f'{elo}assets/img/hirek/{fajl}.webp?v={KEP_V}'


# ---------------------------------------------------------------------------
# Törzsblokkok → HTML
# ---------------------------------------------------------------------------
def torzs_html(darabok, elo, behuzas='        '):
    ki = []
    b = behuzas
    for d in darabok:
        t = d['tipus']
        if t == 'bekezdes':
            ki.append(f'{b}<p class="type-ui-body">{d["szoveg"]}</p>')
        elif t == 'cim':
            ki.append(f'{b}<h2 class="type-display-section-title">{esc(d["szoveg"])}</h2>')
        elif t == 'lista':
            tag = 'ol' if d.get('rendezett') else 'ul'
            pontok = '\n'.join(f'{b}  <li class="type-ui-body">{p}</li>'
                               for p in d['pontok'])
            ki.append(f'{b}<{tag} role="list">\n{pontok}\n{b}</{tag}>')
        elif t == 'idezet':
            ki.append(f'{b}<blockquote class="type-ui-body-strong">'
                      f'<p>{d["szoveg"]}</p></blockquote>')
        elif t == 'kep':
            ki.append(
                f'{b}<figure class="hir-figura">\n'
                f'{b}  <img src="{kep_ut(elo, d["fajl"])}" width="{d["w"]}" height="{d["h"]}"\n'
                f'{b}       alt="{attr(d["alt"])}" loading="lazy" decoding="async">\n'
                f'{b}</figure>')
        elif t == 'video':
            # A beágyazás a `youtube-nocookie.com`-ra megy: a lap SAJÁT
            # sütijein kívül semmit nem tesz le a látogatónál addig, amíg el
            # nem indítja a videót. A cookie-tájékoztató ezt így ígéri.
            cim = d['cim'] if d['cim'] and d['cim'] != 'YouTube video player' \
                else 'Videó az ÖkoTech-Home-ról'
            ki.append(
                f'{b}<div class="hir-video">\n'
                f'{b}  <iframe src="https://www.youtube-nocookie.com/embed/{d["azonosito"]}"\n'
                f'{b}          title="{attr(cim)}" loading="lazy"\n'
                f'{b}          allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"\n'
                f'{b}          allowfullscreen></iframe>\n'
                f'{b}</div>')
    return '\n'.join(ki)


# ---------------------------------------------------------------------------
# Kártya a rácsba
# ---------------------------------------------------------------------------
def kartya(h, kat_nev, elo, hir_elo):
    bor = h['borito']
    if bor:
        keret = 'card-media-foto' if bor['mod'] == 'foto' else 'card-media-dok'
        # A borító két méretben áll rendelkezésre: a kártya asztali nézetben
        # ~370px széles, tehát az 1x-es eszköznek a kisebb is elég.
        media = (
            f'            <figure class="card-media {keret}">\n'
            f'              <img src="{kep_ut(elo, bor["fajl"] + "-600")}"\n'
            f'                   srcset="{kep_ut(elo, bor["fajl"] + "-600")} 600w, {kep_ut(elo, bor["fajl"])} 1200w"\n'
            f'                   sizes="(min-width: 1025px) 360px, (min-width: 641px) 45vw, 90vw"\n'
            f'                   width="{bor["w"]}" height="{bor["h"]}"\n'
            f'                   alt="{attr(bor["alt"])}" loading="lazy" decoding="async">\n'
            f'            </figure>')
    else:
        # Nincs kép ehhez a hírhez. Nem teszünk oda odaillőnek látszó
        # felvételt: a rovat jele áll a helyén, `aria-hidden`, mert nem hordoz
        # olyan információt, amit a kártya szövege ne mondana ki.
        media = (
            f'            <div class="card-media card-media-jel" aria-hidden="true">\n'
            f'              <span class="icon {ROVAT_IKON[h["kategoria"]]}"></span>\n'
            f'            </div>')
    return f'''        <li class="card-item" data-rovat="{h['kategoria']}">
          <article class="card">
{media}
            <p class="hir-meta">
              <span class="card-tag type-ui-label">{esc(kat_nev)}</span>
              <time class="type-data-value hir-datum" datetime="{h['datum']}">{datum_hu(h['datum'])}</time>
            </p>
            <h3 class="type-ui-card-title card-title">
              <a class="hir-cim-link" href="{hir_elo}{h['szlug']}">{esc(h['cim'])}</a>
            </h3>
            <p class="type-ui-body card-text">{esc(h['lead'])}</p>
          </article>
        </li>'''


# ---------------------------------------------------------------------------
# Vízszintes idővonal
# ---------------------------------------------------------------------------
def idovonal(hirek, hir_elo):
    """A hírek NÖVEKVŐ időrendben — balról jobbra halad az idő.

    A rácsban a legfrissebb áll elöl (ott az a kérdés, „mi újság"), az
    idővonalon viszont a kezdet: ott a történet a tárgy, nem a hírérték.
    Az évszám csak ÉVVÁLTÁSNÁL jelenik meg — így a tengely magától tagolódik,
    és nem kell minden ponthoz kiírni ugyanazt az évet.
    """
    sorrend = sorted(hirek, key=lambda h: h['datum'])
    elemek, elozo_ev = [], None
    for i, h in enumerate(sorrend):
        ev = h['datum'][:4]
        valt = ev != elozo_ev
        elozo_ev = ev
        # Felváltva a tengely fölé és alá. A hely a SORSZÁMBÓL adódik, nem az
        # évből: így a ritmus egyenletes marad akkor is, ha egy évre több hír
        # jut, és az egymáshoz közeli dátumok szövege nem ér össze.
        hely = 'fent' if i % 2 == 0 else 'lent'
        ev_jel = ('\n            <span class="type-data-eyebrow hir-idovonal-ev">'
                  f'{ev}</span>' if valt else '')
        elemek.append(
            f'        <li class="hir-idovonal-elem" data-hely="{hely}"'
            f'{" data-evvaltas" if valt else ""}>\n'
            f'{ev_jel}\n'
            f'          <a class="hir-idovonal-link" href="{hir_elo}{h["szlug"]}">\n'
            f'            <time class="type-data-value hir-idovonal-datum" '
            f'datetime="{h["datum"]}">{datum_rovid(h["datum"])}</time>\n'
            f'            <span class="type-ui-subtitle hir-idovonal-cim">{esc(h["cim"])}</span>\n'
            f'          </a>\n'
            f'        </li>')
    sor = '\n'.join(elemek)
    return (
        '      <div class="hir-idovonal">\n'
        '        <div class="hir-idovonal-fej">\n'
        '          <h2 class="type-data-eyebrow section-eyebrow" id="idovonal-cim">'
        f'Idővonal · {sorrend[0]["datum"][:4]}–{sorrend[-1]["datum"][:4]}</h2>\n'
        '          <p class="type-ui-caption hir-idovonal-sug">'
        'Kattintson egy pontra a hírhez</p>\n'
        '          <div class="hir-idovonal-vezerlok"></div>\n'
        '        </div>\n'
        '        <div class="hir-idovonal-keret">\n'
        '          <div class="hir-idovonal-palya" tabindex="0" role="group"\n'
        '               aria-labelledby="idovonal-cim">\n'
        '            <ol class="hir-idovonal-sor">\n'
        f'{sor}\n'
        '            </ol>\n'
        '          </div>\n'
        '        </div>\n'
        '      </div>')


def leiras_forras(h) -> str:
    """A kivonat NYERSANYAGA: a lead, és ha az kevés, a törzs eleje is.

    Három hírnél a lead egyetlen felkiáltás („Felépült!", „Kedves
    Felhasználóink!") — kilenc, illetve negyvenegy karakter. Az kivonatnak
    semmit nem mond: a találati listában a cím alatt egy üres sor hatását
    kelti, és a kereső ilyenkor magától szemez ki valamit a lapból, jellemzően
    rosszabbul, mint ahogy mi tennénk.

    Ezért amíg a szöveg rövid, HOZZÁVESSZÜK a következő bekezdéseket. A
    `leiras_vag()` utána úgyis levágja mondathatáron — tehát a hozzáfűzés nem
    tesz hosszúvá semmit, csak az üres eseteket tölti fel.
    """
    reszek = [szoveg(h['lead']).strip()]
    if len(reszek[0]) < 110:
        for b in h.get('torzs', []):
            if b.get('tipus') != 'bekezdes':
                continue
            t = szoveg(str(b.get('szoveg', ''))).strip()
            # A lead gyakran SZÓ SZERINT az első bekezdés — azt ne kétszer.
            if not t or t in reszek[0]:
                continue
            reszek.append(t)
            if len(' '.join(reszek)) >= 110:
                break
    return ' '.join(reszek).strip()


def leiras_vag(t: str, max_hossz: int = 158, cim: str = '') -> str:
    """A `meta description` a KERESŐ KIVONATÁNAK nyersanyaga, nem a lead.

    A Google az asztali találatban 155-160 karakter körül vág. A háromszáz
    karakteres nyers lead ezért a felénél elharapódik — és nem ott, ahol mi
    akarnánk, hanem szó közepén, három ponttal. A hírek leadjei mind hosszabbak
    ennél (mérve: 210-220 karakter), tehát ez MINDEGYIKET érintette.

    A vágás SORRENDJE: előbb mondathatár, aztán szóhatár. Egy egész mondat
    mindig jobb kivonat, mint egy csonka — és ha az első mondat önmagában
    elfér, az pontosan az, amit a szerző első mondatnak szánt.
    """
    t = t.strip()
    # AZONOS LEADŰ ÉVES HÍREK. A Dun & Bradstreet tanúsítványról négy éven át
    # ugyanazzal a szöveggel számoltunk be (2022-2025) — a négy lap így
    # ugyanazt a leírást viselte, és a kereső számára megkülönböztethetetlen
    # volt. Amelyik címben évszám áll, ott az évszám elé kerül: ez tényszerű,
    # és pontosan azt mondja, ami a négy lapot elválasztja.
    ev = re.search(r'\b(20\d\d)\b', cim)
    if ev and ev.group(1) not in t:
        t = f'{ev.group(1)}: {t}'
    if len(t) <= max_hossz:
        return t
    # 1) az utolsó mondatvég a korláton belül — de csak ha nem túl korán van:
    #    egy nyolcvan karakteres töredék már nem mond eleget.
    vag = max(t.rfind(j, 0, max_hossz + 1) for j in ('. ', '! ', '? '))
    if vag >= max_hossz * 0.55:
        return t[:vag + 1].strip()
    # 2) különben szóhatár, három ponttal — a csonka szó rosszabb, mint a jelölt
    #    rövidítés.
    vag = t.rfind(' ', 0, max_hossz - 1)
    return (t[:vag] if vag > 0 else t[:max_hossz - 1]).rstrip(' ,;:–—-') + '…'


# ---------------------------------------------------------------------------
# Lapváz
# ---------------------------------------------------------------------------
def lap(*, elo, cim, leiras, url, og_kep, torzs, ld, fejlec, lablec,
        hirek_js=False):
    kep_meta = (f'<meta property="og:image" content="{DOMAIN}/{og_kep}">\n'
                if og_kep else '')
    js_hirek = (f'<script src="{elo}assets/js/hirek.js?v={JS_HIREK_V}" defer></script>\n'
                if hirek_js else '')
    return f'''<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<!-- TESZT ÜZEMMÓD: a robot LETÖLTHETI a lapot (a robots.txt engedi), de nem
     indexelheti, nem archiválhatja és nem idézhet belőle — ugyanezt küldi a
     .htaccess X-Robots-Tag fejléce is. ÉLESÍTÉSKOR a lenti sor tartalmát
     "index, follow"-ra kell cserélni, minden oldalon. -->
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex, notranslate, max-snippet:0, max-image-preview:none, max-video-preview:0, noai, noimageai">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(cim)}</title>
<meta name="description" content="{attr(leiras)}">
<link rel="canonical" href="{DOMAIN}/{url}">
<meta property="og:type" content="article">
<meta property="og:title" content="{attr(cim)}">
<meta property="og:description" content="{attr(leiras)}">
{kep_meta}<meta property="og:locale" content="hu_HU">
<!-- A betűk SAJÁT KISZOLGÁLÓRÓL jönnek. A Google Fontsról betöltve a
     stíluslap renderelést blokkolna két idegen kézfogás után, és a
     látogató IP-címe minden lapmegtekintéskor a Google-höz kerülne.

     ELŐTÖLTÉS SZÁNDÉKOSAN NINCS. A `preload as="font"` MAGAS prioritású —
     ugyanaz, mint a hero-képé —, és mobilhálózaton 57 KB betű állt volna a
     86 KB-os LCP-kép elé. Amit cserébe adott volna, az egy rövid
     betűcsere-villanás megspórolása; a `font-display: swap` viszont a
     szöveget így is azonnal kirakja tartalék betűvel. A villanásért nem
     adjuk oda az LCP-t.
     Lásd assets/css/betuk.css és scripts/oldalgyartas/betuk.py. -->
<link rel="stylesheet" href="/assets/css/betuk.css?v=1">
<link rel="stylesheet" href="{elo}assets/css/app.css?v={CSS_V}">
<!-- A témát a `data-theme` hordozza; ez a szkript írja ki, még a törzs
     feldolgozása előtt — így nincs villanás. Lásd assets/js/tema.js. -->
<script src="{elo}assets/js/tema.js?v=1"></script>
</head>
<body>

{fejlec}

<main id="fotartalom">
{torzs}
</main>

{lablec}

<script src="{elo}assets/js/site.js?v={JS_SITE_V}" defer></script>
<script src="{elo}assets/js/kalauz.js?v={JS_KALAUZ_V}" defer></script>
{js_hirek}<script type="application/ld+json">
{ld}
</script>

</body>
</html>
'''


def morzsa_ld(elemek):
    sorok = ',\n'.join(
        '        {\n'
        f'          "@type": "ListItem",\n'
        f'          "position": {i},\n'
        f'          "name": {jso(nev)}'
        + (f',\n          "item": "{DOMAIN}/{ut}"' if ut else '')
        + '\n        }'
        for i, (nev, ut) in enumerate(elemek, 1))
    return ('    {\n      "@type": "BreadcrumbList",\n'
            '      "itemListElement": [\n' + sorok + '\n      ]\n    }')


# ---------------------------------------------------------------------------
# Gyűjtőlap
# ---------------------------------------------------------------------------
def gyujtolap(adat):
    hirek, kategoriak = adat['hirek'], adat['kategoriak']
    nev = {k['szlug']: k['nev'] for k in kategoriak}
    elso = hirek[0]

    chipek = [
        '          <button type="button" class="hir-chip type-ui-button"\n'
        '                  data-rovat="mind" aria-pressed="true">Mind\n'
        f'            <span class="hir-chip-db type-data-value">{len(hirek)}</span>\n'
        '          </button>'
    ]
    for k in kategoriak:
        db = sum(1 for h in hirek if h['kategoria'] == k['szlug'])
        if not db:
            continue
        chipek.append(
            '          <button type="button" class="hir-chip type-ui-button"\n'
            f'                  data-rovat="{k["szlug"]}" aria-pressed="false">{esc(k["nev"])}\n'
            f'            <span class="hir-chip-db type-data-value">{db}</span>\n'
            '          </button>')

    # A RÁCS MINDEN HÍRT TARTALMAZ, a legfrissebbet is. Korábban kimaradt
    # belőle, mert fölötte külön panelben áll — csakhogy a szűrőgombon álló
    # darabszám a TELJES rovatot mondja, és a rács eggyel kevesebbet mutatott:
    # „Pályázatok és fejlesztések 8", alatta hét kártya. A kiemelés hangsúly,
    # nem kivétel; a szakasz címe pedig „Minden hír".
    kartyak = '\n'.join(kartya(h, nev[h['kategoria']], '../../', '')
                        for h in hirek)

    bor = elso['borito']
    if bor:
        # Fényképnél a bélyeg keretét KI kell tölteni, tanúsítványnál viszont
        # egészben kell látszania — ugyanaz a kétféle bánásmód, mint a
        # kártyaborítóknál.
        kiemelt_media = (
            f'        <figure class="hir-kiemelt-media" data-mod="{bor["mod"]}">\n'
            f'          <img src="{kep_ut("../../", bor["fajl"] + "-600")}"\n'
            f'               width="{bor["w"]}" height="{bor["h"]}" alt="{attr(bor["alt"])}"\n'
            f'               decoding="async">\n'
            f'        </figure>')
    else:
        kiemelt_media = (
            f'        <div class="hir-kiemelt-media" aria-hidden="true">\n'
            f'          <span class="icon {ROVAT_IKON[elso["kategoria"]]}"></span>\n'
            f'        </div>')

    ev_tol = min(h['datum'][:4] for h in hirek)
    ev_ig = max(h['datum'][:4] for h in hirek)

    torzs = f'''
  <!-- ==========================================================================
       FEJLÉC — fejléckép NÉLKÜL. Lásd az app.css „HÍREK" szakaszának jelzett
       eltérését: a hírek képanyagán a cím kontrasztja nem tartható. A vizuális
       súlyt az IDŐVONAL viszi: az mondja el egy pillantásra, hogy ez
       {ev_tol} óta tartó, folyamatos történet — és egyben navigáció is,
       mert minden pontja hivatkozás.
       ========================================================================== -->
  <section class="hero page-hero" aria-labelledby="oldal-cim">
    <div class="hero-inner">
      <div class="hero-copy">
        <nav class="breadcrumb" aria-label="Morzsamenü">
          <ol class="breadcrumb-list type-ui-caption" role="list">
            <li><a href="../../">Főoldal</a></li>
            <li><a href="../">ÖkoTech-Home</a></li>
            <li aria-current="page">Hírek</li>
          </ol>
        </nav>
        <h1 class="type-display-page-title hero-title" id="oldal-cim">Hírek</h1>
        <p class="type-ui-body-strong hero-lead">Ami {ev_tol} óta történt velünk: fejlesztések, átadott
          projektek, kiállítások, tanúsítványok és pályázatok — időrendben, egy helyen.</p>
      </div>

{idovonal(hirek, '')}
    </div>
  </section>

  <section class="section section-tomor" aria-labelledby="kiemelt-cim">
    <div class="section-inner">
      <p class="type-data-eyebrow section-eyebrow">Legfrissebb hírünk</p>
      <article class="hir-kiemelt">
{kiemelt_media}
        <div class="hir-kiemelt-torzs">
          <p class="hir-meta">
            <span class="card-tag type-ui-label">{esc(nev[elso['kategoria']])}</span>
            <time class="type-data-value hir-datum" datetime="{elso['datum']}">{datum_hu(elso['datum'])}</time>
          </p>
          <h2 class="type-ui-card-title" id="kiemelt-cim">
            <a class="hir-cim-link" href="{elso['szlug']}">{esc(elso['cim'])}</a>
          </h2>
          <p class="type-ui-subtitle card-text">{esc(elso['lead'])}</p>
        </div>
      </article>
    </div>
  </section>

  <!-- ==========================================================================
       MINDEN HÍR. A lista TELJES EGÉSZÉBEN itt van; a rovatszűrő (hirek.js)
       csak elrejt belőle. Szkript nélkül tehát minden hír olvasható, és a
       szűrősor akkor sem hazudik: a chipek melletti darabszám statikus adat.
       ========================================================================== -->
  <section class="section" aria-labelledby="lista-cim" data-hirek>
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Archívum · {ev_tol}–{ev_ig}</p>
        <h2 class="type-display-section-title section-title" id="lista-cim">Minden hír</h2>
        <p class="type-ui-body section-lead">A régi webhely blogjának teljes anyaga átkerült ide.
          A rovatokra szűkítéshez válasszon a gombok közül.</p>
      </header>

      <div class="hir-szuro" role="group" aria-label="Szűrés rovatra">
{chr(10).join(chipek)}
        <p class="type-ui-subtitle hir-talalat" data-hir-talalat hidden></p>
      </div>

      <ul class="card-grid" data-cols="3" role="list">
{kartyak}
      </ul>

      <p class="type-ui-body" data-hir-ures hidden>Ebben a rovatban jelenleg nincs hír.</p>
    </div>
  </section>

  <section class="section" aria-labelledby="tovabb-cim">
    <div class="section-inner">
      <aside class="panel-dark" aria-labelledby="tovabb-cim">
        <div class="panel-dark-head">
          <p class="type-data-eyebrow panel-dark-eyebrow">A cégről</p>
          <h2 class="type-display-highlight-title panel-dark-title" id="tovabb-cim">Kik vagyunk?</h2>
        </div>
        <div class="panel-dark-body">
          <p class="type-ui-body panel-dark-text">Az ÖkoTech-Home Kft. 2004 óta gyárt biológiai
            szennyvíztisztító berendezéseket Esztergomban, több mint 3800 telepítéssel.</p>
          <p class="type-ui-body panel-dark-text"><a href="../palyazatok">Pályázati tájékoztatás</a></p>
          <p class="panel-dark-actions"><a class="btn btn-inverse" href="../tortenetunk">Történetünk</a></p>
        </div>
      </aside>
    </div>
  </section>
'''

    lista_ld = ',\n'.join(
        '        {\n'
        f'          "@type": "ListItem",\n          "position": {i},\n'
        f'          "url": "{DOMAIN}/{SZAKASZ_URL}/{h["szlug"]}",\n'
        f'          "name": {jso(h["cim"])}\n        }}'
        for i, h in enumerate(hirek, 1))
    ld = f'''{{
  "@context": "https://schema.org",
  "@graph": [
{morzsa_ld([('Főoldal', ''), ('ÖkoTech-Home', 'okotech-home/'), ('Hírek', None)])},
    {{
      "@type": "ItemList",
      "name": "ÖkoTech-Home hírek",
      "numberOfItems": {len(hirek)},
      "itemListElement": [
{lista_ld}
      ]
    }}
  ]
}}'''

    return lap(elo='../../', cim='Hírek — ÖkoTech-Home',
               leiras='Az ÖkoTech-Home Kft. hírei 2014 óta: fejlesztések, átadott '
                      'projektek, kiállítások, tanúsítványok és pályázatok.',
               url=SZAKASZ_URL + '/',
               # BORÍTÓ NÉLKÜLI HÍRNÉL A MÁRKAKÉP a tartalék. Hat régi
               # bejegyzésnek nincs képe, és kép nélkül a Facebook/LinkedIn
               # csupasz szöveges kártyát rajzol — az a hírfolyamban
               # gyakorlatilag láthatatlan. A márkakép nem hazudik: a lap
               # tényleg az ÖkoTech Home híre.
               og_kep=(f'assets/img/hirek/{bor["fajl"]}.webp' if bor
                       else 'assets/img/hero-rendszer-allokep.webp'),
               torzs=torzs, ld=ld, fejlec=melyebb(FEJLEC), lablec=melyebb(LABLEC),
               hirek_js=True)


# ---------------------------------------------------------------------------
# Hírrészlet
# ---------------------------------------------------------------------------
def reszletlap(h, i, adat):
    hirek, kategoriak = adat['hirek'], adat['kategoriak']
    nev = {k['szlug']: k['nev'] for k in kategoriak}
    elo = '../../'
    ujabb = hirek[i - 1] if i > 0 else None          # a lista időrendben csökken
    regebbi = hirek[i + 1] if i + 1 < len(hirek) else None

    bor = h['borito']
    if bor:
        # A RÉSZLETLAP A TELJES KÉPET KAPJA, nem a kártyák 3:2-es kivágását.
        # A kivágás a RÁCSNAK szól: ott az egységes arány tartja együtt a sort.
        # Itt viszont a kép maga a tartalom — egy álló gyerekrajz teteje-alja a
        # vízszintes kivágásban elveszne, és sehol nem maradna meg egészben.
        t = bor.get('teljes')
        if t:
            borito_html = f'''
      <figure class="hir-figura">
        <img src="{kep_ut(elo, t['fajl'])}" width="{t['w']}" height="{t['h']}"
             alt="{attr(bor['alt'])}" fetchpriority="high" decoding="async">
      </figure>
'''
        else:
            borito_html = f'''
      <figure class="hir-figura">
        <img src="{kep_ut(elo, bor['fajl'])}" width="{bor['w']}" height="{bor['h']}"
             alt="{attr(bor['alt'])}" fetchpriority="high" decoding="async">
      </figure>
'''
    else:
        borito_html = ''

    lepteto = []
    if regebbi:
        lepteto.append(
            '        <div class="hir-lepteto-elem" data-irany="elozo">\n'
            '          <span class="type-ui-caption hir-lepteto-cimke">Korábbi hír</span>\n'
            f'          <a class="text-link" href="{regebbi["szlug"]}">'
            f'<span class="link-label">{esc(regebbi["cim"])}</span></a>\n'
            '        </div>')
    if ujabb:
        lepteto.append(
            '        <div class="hir-lepteto-elem" data-irany="kovetkezo">\n'
            '          <span class="type-ui-caption hir-lepteto-cimke">Újabb hír</span>\n'
            f'          <a class="text-link" href="{ujabb["szlug"]}">'
            f'<span class="link-label">{esc(ujabb["cim"])}</span></a>\n'
            '        </div>')
    lepteto_html = ''
    if lepteto:
        lepteto_html = ('\n      <nav class="hir-lepteto" aria-label="Léptetés a hírek között">\n'
                        + '\n'.join(lepteto) + '\n      </nav>\n')

    # Kapcsolódó: ugyanabból a rovatból a három legközelebbi.
    rokon = [x for x in hirek if x['kategoria'] == h['kategoria'] and x is not h][:3]
    rokon_html = ''
    if rokon:
        rokon_html = f'''
  <section class="section" aria-labelledby="rokon-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Ugyanebből a rovatból</p>
        <h2 class="type-display-section-title section-title" id="rokon-cim">{esc(nev[h['kategoria']])}</h2>
      </header>
      <ul class="card-grid" data-cols="3" role="list">
{chr(10).join(kartya(x, nev[x['kategoria']], elo, '') for x in rokon)}
      </ul>
    </div>
  </section>
'''

    torzs = f'''
  <section class="hero page-hero" aria-labelledby="oldal-cim">
    <div class="hero-inner">
      <div class="hero-copy">
        <nav class="breadcrumb" aria-label="Morzsamenü">
          <ol class="breadcrumb-list type-ui-caption" role="list">
            <li><a href="{elo}">Főoldal</a></li>
            <li><a href="../">ÖkoTech-Home</a></li>
            <li><a href="./">Hírek</a></li>
            <li aria-current="page">{esc(h['cim'])}</li>
          </ol>
        </nav>
        <p class="hir-meta">
          <span class="card-tag type-ui-label">{esc(nev[h['kategoria']])}</span>
          <time class="type-data-value hir-datum" datetime="{h['datum']}">{datum_hu(h['datum'])}</time>
        </p>
        <h1 class="type-display-page-title hero-title" id="oldal-cim">{esc(h['cim'])}</h1>
      </div>
    </div>
  </section>

  <section class="section" aria-labelledby="oldal-cim">
    <div class="section-inner">
{borito_html}      <div class="hir-cikk">
{torzs_html(h['torzs'], elo)}
      </div>
{lepteto_html}    </div>
  </section>
{rokon_html}
  <section class="section" aria-labelledby="kapcsolat-cim">
    <div class="section-inner">
      <aside class="panel-dark" aria-labelledby="kapcsolat-cim">
        <div class="panel-dark-head">
          <p class="type-data-eyebrow panel-dark-eyebrow">Kérdése van?</p>
          <h2 class="type-display-highlight-title panel-dark-title" id="kapcsolat-cim">Beszéljük meg a helyzetét</h2>
        </div>
        <div class="panel-dark-body">
          <p class="type-ui-body panel-dark-text">Ha az ingatlanán nincs közcsatorna, egy rövid
            konzultáción tisztázzuk, milyen megoldás jöhet szóba — és mi az, ami nem.</p>
          <p class="type-ui-body panel-dark-text"><a href="./">Vissza a hírekhez</a></p>
          <p class="panel-dark-actions"><a class="btn btn-inverse" href="{elo}konzultacio">Konzultáció kérése</a></p>
        </div>
      </aside>
    </div>
  </section>
'''

    kep_url = f'assets/img/hirek/{bor["fajl"]}.webp' if bor else None
    cikk_ld = ('    {\n      "@type": "NewsArticle",\n'
               f'      "headline": {jso(h["cim"])},\n'
               f'      "datePublished": "{h["datum"]}",\n'
               f'      "articleSection": {jso(nev[h["kategoria"]])},\n'
               f'      "description": {jso(szoveg(h["lead"]))},\n'
               + (f'      "image": "{DOMAIN}/{kep_url}",\n' if kep_url else '')
               + f'      "mainEntityOfPage": "{DOMAIN}/{SZAKASZ_URL}/{h["szlug"]}",\n'
               '      "publisher": {\n'
               '        "@type": "Organization",\n'
               '        "name": "ÖkoTech-Home Kft.",\n'
               f'        "url": "{DOMAIN}/"\n'
               '      }\n    }')
    ld = f'''{{
  "@context": "https://schema.org",
  "@graph": [
{morzsa_ld([('Főoldal', ''), ('ÖkoTech-Home', 'okotech-home/'),
            ('Hírek', SZAKASZ_URL + '/'), (h['cim'], None)])},
{cikk_ld}
  ]
}}'''

    # A `hirek.js` a RÉSZLETLAPRA IS kell: a nagyított képnézet onnan indul.
    # A modul három egymástól független részből áll, és mindegyik kilép, ha a
    # saját elemét nem találja — a szűrő és az idővonal itt egyszerűen nem fut.
    return lap(elo=elo, cim=f'{h["cim"]} — Hírek | ÖkoTech Home',
               leiras=leiras_vag(leiras_forras(h), cim=h['cim']) or h['cim'],
               url=f'{SZAKASZ_URL}/{h["szlug"]}',
               # A MEGOSZTÁSI KÉP ÉS A CIKK KÉPE NEM UGYANAZ. A `kep_url` a
               # cikk SAJÁT képe, és a JSON-LD `image` mezőjébe csak az
               # kerülhet — borító híján ott a hiány az igazság. Az `og:image`
               # viszont a megosztási kártyáé: kép nélkül a Facebook és a
               # LinkedIn csupasz szöveges kártyát rajzol, ami a hírfolyamban
               # gyakorlatilag láthatatlan. Hat régi bejegyzésnek nincs
               # borítója; azoknak a márkakép a tartaléka.
               og_kep=kep_url or 'assets/img/hero-rendszer-allokep.webp',
               torzs=torzs, ld=ld,
               fejlec=melyebb(FEJLEC), lablec=melyebb(LABLEC),
               hirek_js=True)


def fut():
    adat = json.load(open(FORRAS, encoding='utf-8'))
    adat['hirek'].sort(key=lambda h: h['datum'], reverse=True)

    mappa = WEB / 'okotech-home' / 'hirek'
    mappa.mkdir(exist_ok=True)
    (mappa / 'index.html').write_text(gyujtolap(adat), encoding='utf-8')
    for i, h in enumerate(adat['hirek']):
        (mappa / f'{h["szlug"]}.html').write_text(
            reszletlap(h, i, adat), encoding='utf-8')
    print(f'kész: 1 gyűjtőlap + {len(adat["hirek"])} hírrészlet')


if __name__ == '__main__':
    fut()
