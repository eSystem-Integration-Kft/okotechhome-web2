#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Szippantási díj kalkulátor — `/szippantasi-dij-kalkulator`.

Modul-oldal (oldaltípus 6.): a látogató a SAJÁT díjszabásából számol éves
szippantási költséget, közben pedig épül a települési díjadatbázis.

MIÉRT GENERÁTOR. A fejléc (kontaktsáv + háromszintű megamenü) és a lábléc ma
minden lapon duplikálódik. Amíg nincs build-lépés, a másolás egyetlen
megengedett módja az, hogy egy MEGLÉVŐ lapból emeljük ki — így nem tud
szétcsúszni. A gyökérben álló `kapcsolat.html` a forrás, mert annak a
hivatkozásai már gyökér-relatívak (nincs bennük `../`), akárcsak ezen a lapon.

ADATFORRÁS. Sem díj, sem településnév nem áll ebben a fájlban: a kalkulátor a
`_web/assets/data/szippantas-konfig.js` fájlból dolgozik. A briefben szereplő
példaértékek is oda kerültek, „példa" jelöléssel.

    python3 scripts/oldalgyartas/szippantasi_kalkulator.py
"""
import pathlib
import re

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'
FORRAS = WEB / 'kapcsolat.html'
CEL = WEB / 'szippantasi-dij-kalkulator.html'

URL = 'szippantasi-dij-kalkulator'
H1 = 'Szippantási díj kalkulátor'
CIM = 'Szippantási díj kalkulátor — mennyibe kerül egy évben? | ÖkoTech Home'
LEIRAS = ('Számolja ki, mennyibe kerül évente a szippantás: kiszállási díj, '
          'köbméter-alapú ürítési díj és minimumdíj együtt. A minimumdíjban '
          'foglalt mennyiség is beleszámít.')
LEAD = ('A szippantás díja településenként más, és ritkán áll egyetlen számból: '
        'kiszállási díj, köbméter-alapú ürítési díj és sok helyen minimumdíj is '
        'szerepel a számlán. Ez a kalkulátor a saját díjszabásából számol éves '
        'költséget — és megmutatja, mennyit fizet ki olyan mennyiségért, amit el '
        'sem visznek.')

# A fejléckép a `megoldasok/oldomedence-szippantas-es-karbantartas` lapé.
# Megosztott kép, mert a két lap TÉNYLEGESEN ugyanarról szól (szippantás) —
# a designrendszer 11.4 szabálya szerint ilyenkor az `alt` is azonos.
KEP = 'szippantas'
KEP_V = '?v=2'
ALT = ('Nyitott aknafedlap a gyepben, belőle szippantótömlő vezet a bekötőúton '
       'álló szippantóautóhoz')

CSS_V = 137          # az app.css hivatkozásának verziója (cache-busting)
KONFIG_V = 1
JS_V = 1

# --------------------------------------------------------------------------
# GYIK — a látható szövegből épül a FAQPage jelölés is, hogy a kettő ne
# tudjon elcsúszni (a Google szerint az eltérés önmagában szabálysértés).
# --------------------------------------------------------------------------
GYIK = [
    ('Miért nem írják ki, mennyi a szippantás díja a településemen?',
     'Mert nem tudjuk. A nem közművel elvezetett háztartási szennyvíz begyűjtése '
     'közszolgáltatás: a díjat a közszolgáltató és az önkormányzat állapítja meg, '
     'településenként külön, és nincs róla nyilvános, összesített nyilvántartás. '
     'Kitalált vagy „nagyjából ennyi" értéket pedig nem írunk ki — az rosszabb a '
     'semminél, mert a látogató elhinné. Ezért kéri be a kalkulátor a díjakat, és '
     'ezért gyűjtjük őket településenként.'),
    ('Mit jelent az, hogy a minimumdíj tartalmaz x m³-t?',
     'Azt, hogy a minimumdíjért cserébe a szolgáltató egy adott mennyiség '
     'elszállítását vállalja — és ha ennél kevesebbet vitet el, akkor is ennyit '
     'fizet ki. Ha ez a mennyiség megegyezik a szippantóautó űrtartalmával, akkor a '
     'teljes kocsit kifizeti akkor is, ha egyetlen köbmétert szállíttat el. A '
     'kalkulátorban ezért külön mező a „minimumdíjban foglalt mennyiség": nullától a '
     'kocsi űrtartalmáig bármi lehet.'),
    ('Mi van, ha nincs kiszállási díj?',
     'Akkor írjon a mezőbe nullát. A kiszállási díj nem minden szolgáltatónál külön '
     'tétel — van, ahol a mennyiségalapú díjba vagy a minimumdíjba van beépítve. A '
     'kalkulátor a nullát valódi értékként kezeli, és a költségsávban nem is jelenik '
     'meg ilyenkor ez a szelet.'),
    ('Bruttó vagy nettó értéket írjak be?',
     'Amelyik a számláján szerepel — a kalkulátor nem számol áfát, csak összead és '
     'szoroz. Lakossági számlán ez jellemzően bruttó érték. Ha nettó díjakkal dolgozik, '
     'az eredmény is nettó lesz; a kettőt viszont ne keverje egy számításon belül.'),
    ('Honnan tudom meg a saját településem díjszabását?',
     'Három helyről: a legutóbbi szippantási számláról, a közszolgáltató '
     'ártáblázatából, illetve az önkormányzat hulladékgazdálkodási vagy '
     'szennyvízszállítási rendeletéből. Ha bármelyik megvan, az űrlapon beküldheti — '
     'a következő érdeklődő már azt fogja látni a térképen.'),
    ('Milyen gyakran kell szippantatni?',
     'Erre a kalkulátor nem ad választ, mert ez nem díjkérdés: az iszapszint a '
     'mérvadó, nem a naptár, és a gyakoriságot a tartály mérete, a használói létszám '
     'és a használat intenzitása határozza meg. A gyakoriságot Ön adja meg a '
     'kalkulátorban — mi nem becsüljük meg Ön helyett.'),
]


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _reszek():
    """A fejléc és a lábléc kiemelése a kapcsolat oldalból."""
    src = FORRAS.read_text(encoding='utf-8')
    fejlec = re.search(r'(<a class="skip-link".*?</header>)', src, re.S)
    lablec = re.search(r'(<!-- =+\n     LÁBLÉC.*?</footer>)', src, re.S)
    if not fejlec or not lablec:
        raise SystemExit('! nem találom a fejlécet vagy a láblécet a kapcsolat.html-ben')
    return fejlec.group(1), lablec.group(1)


# ==========================================================================
# SZEKCIÓK
# ==========================================================================

MIT_AD = '''
  <section class="section" aria-labelledby="mit-ad-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Mit ad ez az oldal</p>
        <h2 class="type-display-section-title section-title" id="mit-ad-cim">Mit mutat meg — és mit nem</h2>
        <p class="type-ui-body section-lead">A szippantás nem a mi szolgáltatásunk, és nem a mi árunk. Ez a kalkulátor
          azért van, hogy a saját díjszabásából átlátható legyen, mennyibe kerül ez évente, és min múlik.</p>
      </header>
      <div class="split">
        <div class="split-card">
          <h3 class="type-ui-card-title split-title">Amit megmutat</h3>
          <ul class="fit-list" role="list">
            <li class="type-ui-body"><span class="fit-mark fit-yes" aria-hidden="true"></span><span class="fit-text">Az alkalmankénti és az éves díjat a megadott díjszabás alapján</span></li>
            <li class="type-ui-body"><span class="fit-mark fit-yes" aria-hidden="true"></span><span class="fit-text">Hogy miből áll össze az összeg — tételről tételre</span></li>
            <li class="type-ui-body"><span class="fit-mark fit-yes" aria-hidden="true"></span><span class="fit-text">Mennyit fizet ki olyan mennyiségért, amit nem visznek el</span></li>
            <li class="type-ui-body"><span class="fit-mark fit-yes" aria-hidden="true"></span><span class="fit-text">Hogyan változik a fajlagos díj, ha ritkábban, teltebb tartállyal szippantat</span></li>
            <li class="type-ui-body"><span class="fit-mark fit-yes" aria-hidden="true"></span><span class="fit-text">Hol tartunk a települési díjadatbázis építésével</span></li>
          </ul>
        </div>
        <div class="split-card">
          <h3 class="type-ui-card-title split-title">Amit nem tud megmondani</h3>
          <ul class="fit-list" role="list">
            <li class="type-ui-body"><span class="fit-mark fit-no" aria-hidden="true"></span><span class="fit-text">Nem árlista: nem ismerjük minden település díjszabását, és nem is találjuk ki</span></li>
            <li class="type-ui-body"><span class="fit-mark fit-no" aria-hidden="true"></span><span class="fit-text">Nem helyettesíti a közszolgáltató árajánlatát vagy az önkormányzati rendeletet</span></li>
            <li class="type-ui-body"><span class="fit-mark fit-no" aria-hidden="true"></span><span class="fit-text">Nem mondja meg, milyen gyakran kell szippantatni — azt az iszapszint dönti el</span></li>
            <li class="type-ui-body"><span class="fit-mark fit-no" aria-hidden="true"></span><span class="fit-text">Nem számol áfát: azt írja be, ami a számláján szerepel</span></li>
            <li class="type-ui-body"><span class="fit-mark fit-no" aria-hidden="true"></span><span class="fit-text">Nem küld semmit sehova — a számítás a böngészőjében fut, adat nélkül</span></li>
          </ul>
        </div>
      </div>
    </div>
  </section>
'''

HOGYAN = '''
  <section class="section section-alt" aria-labelledby="hogyan-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">A képlet</p>
        <h2 class="type-display-section-title section-title" id="hogyan-cim">Hogyan számol</h2>
        <p class="type-ui-body section-lead">Öt lépés, és mindegyik ellenőrizhető papíron is. A kalkulátor nem tartalmaz
          rejtett szorzót vagy „tapasztalati" korrekciót.</p>
      </header>
      <ul class="numbered-grid" role="list">
        <li class="card">
          <span class="card-badge type-data-value" aria-hidden="true">01</span>
          <p class="type-ui-body card-text"><strong>Elszámolt mennyiség.</strong> A díj alapja nem mindig az, amennyit
            ténylegesen elvisznek. Ha a minimumdíj tartalmaz egy adott mennyiséget, akkor az elszámolt mennyiség az
            elszállított és a foglalt mennyiség közül a <strong>nagyobbik</strong>.</p>
        </li>
        <li class="card">
          <span class="card-badge type-data-value" aria-hidden="true">02</span>
          <p class="type-ui-body card-text"><strong>Alapdíj.</strong> Az ürítési díj szorozva az elszámolt mennyiséggel —
            de legalább a minimumdíj. A minimumdíj alsó korlát: ha a mennyiségalapú összeg kisebb nála, a minimumdíj lép
            a helyébe.</p>
        </li>
        <li class="card">
          <span class="card-badge type-data-value" aria-hidden="true">03</span>
          <p class="type-ui-body card-text"><strong>Kiszállási díj.</strong> Alkalmanként egyszer, a mennyiségtől
            függetlenül. Nem minden szolgáltatónál külön tétel — ilyenkor nulla kerül a mezőbe, és a költségsávban meg
            sem jelenik.</p>
        </li>
        <li class="card">
          <span class="card-badge type-data-value" aria-hidden="true">04</span>
          <p class="type-ui-body card-text"><strong>További tételek.</strong> Távolságarányos díj (Ft/km szorozva a
            megteendő kilométerrel) és minden egyéb alkalmankénti tétel, ami a számláján szerepel. Mindkettő
            elhagyható.</p>
        </li>
        <li class="card">
          <span class="card-badge type-data-value" aria-hidden="true">05</span>
          <p class="type-ui-body card-text"><strong>Éves költség.</strong> Az alkalmankénti díj szorozva az éves
            alkalomszámmal. A gyakoriságot Ön adja meg — azt a kalkulátor nem becsüli meg, mert az az iszapszinttől és a
            használattól függ, nem a díjszabástól.</p>
        </li>
      </ul>
    </div>
  </section>
'''


def _mezo(nev, cimke, egyseg, hint='', tipus='number', lepes='1', maxi='',
          pelda=False, szeles=False):
    """Egy számmező a kalkulátorban.

    A mértékegység a CÍMKE része, nem külön elem: a képernyőolvasó így együtt
    mondja ki a mező nevével, és nem marad ki a felolvasásból.
    """
    azon = 'k-' + nev.lower()
    peldajel = (f'<span class="type-data-value szip-pelda-jel" '
                f'data-szip-pelda="{nev}">példa</span>' if pelda else '')
    hintsor = (f'\n            <span class="type-ui-caption szip-egyseg" '
               f'id="{azon}-sugo">{hint}</span>' if hint else '')
    leiras = f' aria-describedby="{azon}-sugo"' if hint else ''
    maxattr = f' max="{maxi}"' if maxi else ''
    return f'''          <p class="urlap-mezo{' szip-mezo-szeles' if szeles else ''}">
            <label class="type-ui-caption urlap-cimke" for="{azon}">{cimke}
              <span class="szip-egyseg">({egyseg})</span>{peldajel}</label>
            <input class="urlap-input" type="{tipus}" id="{azon}" name="{nev}"
                   inputmode="decimal" min="0"{maxattr} step="{lepes}"{leiras}>{hintsor}
          </p>'''


# --------------------------------------------------------------------------
# A SZIPPANTÓAUTÓ RAJZA
# --------------------------------------------------------------------------
# Egyetlen geometria, két felhasználás: a fejlécben illusztrációként (sötét
# felületen, betöltéskor behajtó járművel és felfutó töltéssel), a kalkulátorban
# élőben (világos felületen, a mezőkhöz kötve). A megjelenést a `.szip-rajz-hero`
# / `.szip-rajz-muszer` változatosztály állítja, a rajz maga ugyanaz — a látogató
# a fejlécben látott ábrát ismeri fel a kalkulátorban.
#
# Koordináták (viewBox 0 0 560 300):
#   tartály        x=150…450, y=96…200, rx=52   → a töltés x=150-től skálázódik
#   búvónyílás     x=280…334, y=80…98
#   vezetőfülke    x=26…142,  y=128…212
#   alváz          x=40…510,  y=210…222
#   kerekek        cy=232, r=26 · első cx=78 · hátsó tandem cx=330 és 392
#   talajvonal     y=257
#
# A töltésréteg CSS `transform: scaleX()`, nem SVG `width`: az SVG geometriai
# tulajdonságok CSS-ből való állítása nem egyformán támogatott, a `transform`
# viszont mindenhol animálódik.
# --------------------------------------------------------------------------
import math

TANK_X, TANK_SZ = 150, 300
TANK_Y, TANK_M = 96, 104


def _kullo(cx, cy, r1, r2, fokok):
    """Küllők egy tengely körül. A gumi és a felni körén a forgás nem látszana;
    a küllő az egyetlen elem, amin igen."""
    ki = []
    for fok in fokok:
        a = math.radians(fok)
        dx, dy = math.cos(a), math.sin(a)
        ki.append(
            '          <line class="szip-rajz-kullo" '
            'x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"></line>'
            % (cx + r1 * dx, cy + r1 * dy, cx + r2 * dx, cy + r2 * dy))
        ki.append(
            '          <line class="szip-rajz-kullo" '
            'x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"></line>'
            % (cx - r1 * dx, cy - r1 * dy, cx - r2 * dx, cy - r2 * dy))
    return '\n'.join(ki)


def _kerek(cx, cy=232):
    return ('        <g class="szip-rajz-kerek">\n'
            '          <circle class="szip-rajz-gumi" cx="%d" cy="%d" r="26"></circle>\n'
            '          <circle class="szip-rajz-felni" cx="%d" cy="%d" r="15"></circle>\n'
            % (cx, cy, cx, cy)
            + _kullo(cx, cy, 7, 13.5, (12, 57, 102, 147)) + '\n'
            '          <circle class="szip-rajz-kupak" cx="%d" cy="%d" r="5"></circle>\n'
            '        </g>' % (cx, cy))


def _allo_skala():
    """A fejléc ábrájának állandó, nyolcosztásos szintbeosztása."""
    return '\n' + '\n'.join(
        '            <line class="szip-rajz-osztas%s" x1="%.1f" x2="%.1f" y1="98" y2="%d"></line>'
        % (' szip-rajz-osztas-fo' if i == 4 else '',
           150 + 300 * i / 8, 150 + 300 * i / 8, 114 if i == 4 else 107)
        for i in range(1, 8)) + '\n          '


def _sebessegvonalak():
    """Behajtáskor a jármű mögött elhúzó vonalak. A megérkezés után eltűnnek —
    nem dekoráció, hanem a mozgás iránya."""
    return '\n' + '\n'.join(
        '        <line class="szip-rajz-sebesseg" x1="%d" y1="%d" x2="%d" y2="%d"></line>'
        % (-30 - i * 14, y, 26 - i * 16, y)
        for i, y in enumerate((152, 186, 220))) + '\n'


def _bordak():
    """Bordázat enyhén domború ívekkel — egyenes vonal lapos hengert adna."""
    return '\n'.join(
        '        <path class="szip-rajz-borda" d="M%d 101 C %d 130 %d 166 %d 195"></path>'
        % (x, x - 5, x - 5, x) for x in (236, 296, 356))


def rajz(hero):
    """`hero=True`: fejléc-illusztráció feliratozott jelölőkkel.
    `False`: a kalkulátor élő mérőműszere — ott a feliratokat a HTML adja."""
    uid = 'sza' if hero else 'szt'
    valtozat = 'szip-rajz-hero' if hero else 'szip-rajz-muszer'
    # A műszer nézete felül szűkebb, mert nála csak EGY jelölő van felirattal —
    # de a gombostűnek és az értéknek így is kell hely, különben a viewBox
    # levágja őket (ez történt 62-nél).
    nezet = '0 0 560 300' if hero else '0 38 560 260'
    horgony = '' if hero else ' data-szip-tank'
    felirat = ('Szippantóautó tartálya. Az elszállított és a kiszámlázott mennyiség '
               'a minimumdíj miatt eltérhet egymástól.') if hero else \
              'Szippantóautó tartálya'

    if hero:
        jelolok = '''
      <!-- A két jelölő a töltésrétegek élén áll, és velük együtt mozdul. -->
      <g class="szip-rajz-jelolo szip-rajz-jelolo-toltes">
        <line class="szip-rajz-jelvonal-halo" x1="150" y1="44" x2="150" y2="208"></line>
        <line class="szip-rajz-jelvonal" x1="150" y1="44" x2="150" y2="208"></line>
        <path class="szip-rajz-jelpont" d="M144 32 L156 32 L150 44 Z"></path>
        <text class="szip-rajz-cimke" x="150" y="24" text-anchor="middle">ELVISZIK</text>
      </g>
      <g class="szip-rajz-jelolo szip-rajz-jelolo-fizetett">
        <line class="szip-rajz-jelvonal-halo" x1="150" y1="68" x2="150" y2="208"></line>
        <line class="szip-rajz-jelvonal" x1="150" y1="68" x2="150" y2="208"></line>
        <path class="szip-rajz-jelpont" d="M144 56 L156 56 L150 68 Z"></path>
        <text class="szip-rajz-cimke" x="150" y="48" text-anchor="middle">KIFIZETI</text>
      </g>'''
    else:
        jelolok = '''
      <!-- A MINIMUMDÍJBAN FOGLALT MENNYISÉG jelölése. Két vonal egymáson: alul
           tömör, a felület színével, fölötte a sötét szaggatott. Így a jelölés a
           töltött (arany) és az üres (halvány) tartályrészen is olvasható —
           egyetlen vonallal az egyik oldalon mindig elveszett.
           A csoportot a JS elrejti, ha a foglalt mennyiség nulla: ott a vonal a
           tartály bal szélén állna, és nem jelölne semmit. -->
      <g class="szip-rajz-jelolo szip-rajz-jelolo-minimum" data-szip-minimum-jel>
        <line class="szip-rajz-jelvonal-halo" x1="150" y1="74" x2="150" y2="208"></line>
        <line class="szip-rajz-jelvonal" x1="150" y1="74" x2="150" y2="208"></line>
        <path class="szip-rajz-jelpont" d="M144 62 L156 62 L150 74 Z"></path>
        <text class="szip-rajz-cimke szip-rajz-jelcimke" x="150" y="54"
              text-anchor="middle" data-szip-minimum-cimke></text>
      </g>'''

    return SVG_SABLON.format(
        valtozat=valtozat, nezet=nezet, horgony=horgony, felirat=felirat,
        uid=uid, jelolok=jelolok,
        dob_kullok=_kullo(506, 132, 7, 20, (0, 60, 120)),
        bordak=_bordak(),
        kerek1=_kerek(78), kerek2=_kerek(330), kerek3=_kerek(392),
        allo_skala=_allo_skala() if hero else '',
        sebessegvonalak=_sebessegvonalak() if hero else '',
        tx=TANK_X, ty=TANK_Y, tsz=TANK_SZ, tm=TANK_M,
        tx8=TANK_X + 8, tsz16=TANK_SZ - 16, txm2=TANK_X - 2, tym4=TANK_Y - 4, tm8=TANK_M + 8)


SVG_SABLON = '''<svg class="szip-rajz {valtozat}" viewBox="{nezet}" role="img"{horgony}
             aria-label="{felirat}">
      <defs>
        <clipPath id="{uid}-tank">
          <rect x="{tx}" y="{ty}" width="{tsz}" height="{tm}" rx="52"></rect>
        </clipPath>
        <!-- A gradiensszínek `stop-color` CSS-tulajdonságból jönnek
             (osztályonként), hogy a témaváltást ezek is kövessék. -->
        <radialGradient id="{uid}-arny" cx="50%" cy="50%" r="50%">
          <stop class="szip-rajz-arny-0" offset="0%"></stop>
          <stop class="szip-rajz-arny-1" offset="100%"></stop>
        </radialGradient>
        <linearGradient id="{uid}-talaj" x1="0%" x2="100%">
          <stop class="szip-rajz-talaj-0" offset="0%"></stop>
          <stop class="szip-rajz-talaj-1" offset="50%"></stop>
          <stop class="szip-rajz-talaj-0" offset="100%"></stop>
        </linearGradient>
        <linearGradient id="{uid}-melyseg" x1="0%" y1="0%" x2="0%" y2="100%">
          <stop class="szip-rajz-melyseg-0" offset="0%"></stop>
          <stop class="szip-rajz-melyseg-1" offset="100%"></stop>
        </linearGradient>
        <linearGradient id="{uid}-paszma" x1="0%" x2="100%">
          <stop class="szip-rajz-paszma-0" offset="0%"></stop>
          <stop class="szip-rajz-paszma-1" offset="50%"></stop>
          <stop class="szip-rajz-paszma-0" offset="100%"></stop>
        </linearGradient>
      </defs>

      <g class="szip-rajz-jarmu">{sebessegvonalak}
        <!-- Talajra vetett árnyék: kifelé nullába halványuló gradiens, nem
             tömör ellipszis — így nincs éle. -->
        <ellipse class="szip-rajz-arny" cx="288" cy="258" rx="252" ry="10"
                 fill="url(#{uid}-arny)"></ellipse>

        <!-- Alváz. Erősebb tónus, mint a burkolati elemeké: ez köti össze a
             fülkét és a tartályt, e nélkül a rajz különálló darabokra esik. -->
        <rect class="szip-rajz-vaz" x="40" y="210" width="470" height="12" rx="5"></rect>
        <rect class="szip-rajz-test" x="46" y="222" width="458" height="5" rx="2"></rect>

        <!-- tartálybölcsők: a tartály nem lebeg, hanem nyeregben ül -->
        <path class="szip-rajz-vaz" d="M198 196 L232 196 L227 211 L203 211 Z"></path>
        <path class="szip-rajz-vaz" d="M366 196 L400 196 L395 211 L371 211 Z"></path>

        <!-- Vezetőfülke: ferde szélvédő, ajtóvonal, kilincs, tükör, lökhárító.
             SAJÁT CSOPORT, mert az űrtartalommal a TARTÁLY nyúlik, a fülke nem:
             ez a csoport visszaskálázza magát, hogy megtartsa az arányait. -->
        <g class="szip-rajz-fulke">
          <path class="szip-rajz-test" d="M48 128 L126 128 Q142 128 142 144 L142 212 L26 212 L26 176 Q26 158 36 148 Z"></path>
          <path class="szip-rajz-ur" d="M56 138 L120 138 Q130 138 130 148 L130 171 L42 171 L42 167 Q42 156 50 148 Z"></path>
          <path class="szip-rajz-korvonal" d="M48 128 L126 128 Q142 128 142 144 L142 212 L26 212 L26 176 Q26 158 36 148 Z"></path>
          <line class="szip-rajz-vonal" x1="106" y1="176" x2="106" y2="212"></line>
          <line class="szip-rajz-vonal" x1="93" y1="185" x2="101" y2="185"></line>
          <path class="szip-rajz-vonal" d="M143 150 L151 146"></path>
          <rect class="szip-rajz-test" x="18" y="199" width="10" height="15" rx="3"></rect>
        </g>

        <!-- Hátsó szerelvény: vákuumpumpa-ház és tömlődob. Ugyanezért külön
             csoport — a dob kör marad, nem lapul ellipszissé. -->
        <g class="szip-rajz-hatso">
          <rect class="szip-rajz-test" x="452" y="170" width="44" height="42" rx="8"></rect>
          <rect class="szip-rajz-korvonal-r" x="452" y="170" width="44" height="42" rx="8"></rect>
          <line class="szip-rajz-vonal" x1="460" y1="180" x2="488" y2="180"></line>
          <line class="szip-rajz-vonal" x1="460" y1="189" x2="488" y2="189"></line>
          <g class="szip-rajz-dob">
            <circle class="szip-rajz-test" cx="506" cy="132" r="30"></circle>
            <circle class="szip-rajz-korvonal" cx="506" cy="132" r="30"></circle>
            <circle class="szip-rajz-korvonal-r" cx="506" cy="132" r="20"></circle>
{dob_kullok}
            <circle class="szip-rajz-kupak" cx="506" cy="132" r="6"></circle>
          </g>
          <path class="szip-rajz-tomlo" d="M506 162 C 506 208 526 226 542 252"></path>
        </g>

        <!-- ============================== TARTÁLY ============================== -->
        <rect class="szip-rajz-ur" x="{tx}" y="{ty}" width="{tsz}" height="{tm}" rx="52"></rect>
        <g clip-path="url(#{uid}-tank)">
          <rect class="szip-rajz-fizetett" x="{tx}" y="{ty}" width="{tsz}" height="{tm}"></rect>
          <rect class="szip-rajz-toltes" x="{tx}" y="{ty}" width="{tsz}" height="{tm}"></rect>
          <!-- A henger térbelisége: alul mélyülő árnyék, felül keskeny csillanás. -->
          <rect class="szip-rajz-belso-arny" x="{tx}" y="148" width="{tsz}" height="52"
                fill="url(#{uid}-melyseg)"></rect>
          <rect class="szip-rajz-belso-feny" x="{tx8}" y="104" width="{tsz16}" height="10" rx="5"></rect>
          <!-- A töltésrétegek éle: vékony világos sáv, mint a folyadék meniszkusza. -->
          <rect class="szip-rajz-el szip-rajz-el-fizetett" x="{txm2}" y="{ty}" width="3" height="{tm}"></rect>
          <rect class="szip-rajz-el szip-rajz-el-toltes" x="{txm2}" y="{ty}" width="3" height="{tm}"></rect>
          <!-- Végigfutó fénypászma — csak a fejlécben, hurokban. -->
          <rect class="szip-rajz-paszma" x="-140" y="{tym4}" width="140" height="{tm8}"
                fill="url(#{uid}-paszma)"></rect>
          <!-- SZINTBEOSZTÁS. A műszer-változatban a vonalkákat a JS rajzolja,
               mert a számuk a megadott űrtartalomtól függ (egy 4 m³-es kocsin
               négy osztás van, egy 11 m³-esen tizenegy). A fejléc ábráján
               állandó, nyolcosztásos skála áll: ott illusztráció, nem mérés. -->
          <g class="szip-rajz-skala" data-szip-skala aria-hidden="true">{allo_skala}</g>
        </g>
        <!-- Domború hátsó véglap: ettől henger a tartály, nem kapszula. -->
        <ellipse class="szip-rajz-veglap" cx="424" cy="148" rx="24" ry="51"></ellipse>
{bordak}
        <rect class="szip-rajz-korvonal" x="{tx}" y="{ty}" width="{tsz}" height="{tm}" rx="52"></rect>

        <!-- Búvónyílás és szellőzőszelep a tartály ELEJÉN. Korábban középen
             állt, és pont a „KIFIZETI" felirat alá esett — a kettő takarta
             egymást. Elöl a töltésjelölők soha nem érik el. -->
        <rect class="szip-rajz-test" x="196" y="80" width="52" height="18" rx="7"></rect>
        <rect class="szip-rajz-korvonal-r" x="196" y="80" width="52" height="18" rx="7"></rect>
        <line class="szip-rajz-vonal" x1="208" y1="75" x2="236" y2="75"></line>
        <circle class="szip-rajz-test" cx="172" cy="90" r="8"></circle>
        <circle class="szip-rajz-korvonal-r" cx="172" cy="90" r="8"></circle>
        <line class="szip-rajz-vonal" x1="172" y1="81" x2="172" y2="99"></line>

        <!-- alsó ürítőcsonk a tartály és a szivattyúház között -->
        <path class="szip-rajz-tomlo" d="M410 198 L452 198"></path>

        <!-- Sárvédők. A tartály alsó éle y=200; az ív csúcsa ezért 204 —
             korábban 187-nél volt, és keresztbe vágta a tartályt. -->
        <path class="szip-rajz-korvonal-r" d="M52 226 Q54 206 78 206 Q102 206 104 226"></path>
        <path class="szip-rajz-korvonal-r" d="M298 226 Q300 204 361 204 Q422 204 424 226"></path>

        <!-- kerekek -->
{kerek1}
{kerek2}
{kerek3}

        <!-- Talajvonal: a két vége nullába halványul, nincs levágott éle. -->
        <rect class="szip-rajz-talaj" x="16" y="257" width="528" height="2"
              fill="url(#{uid}-talaj)"></rect>
      </g>
{jelolok}
    </svg>'''


HERO_ABRA = rajz(hero=True)


TANK_SVG = '''
      <!-- A JÁRMŰ: méretválasztó és ábra EGY blokkban.
           Külön állva a két dolog nem beszélt egymással — a látogató átállította
           a járműméretet, és nem látta, mit csinál. Így a választó mellett ott a
           rajz: a tartály hossza és a köbméter-beosztása is követi a választást. -->
      <fieldset class="szip-csoport szip-jarmu">
        <legend class="type-ui-card-title szip-csoport-cim">A jármű és a tartály</legend>
        <div class="szip-jarmu-racs">
          <figure class="szip-jarmu-abra">
            ''' + rajz(hero=False) + '''
            <figcaption class="type-ui-caption szip-egyseg">A tartály tetején minden vonalka egy köbméter.
              A szaggatott jelölés a minimumdíjban foglalt mennyiséget mutatja: ami e között és az elszállított
              mennyiség között van, azt kifizeti, de nem viszik el.</figcaption>
          </figure>

          <div class="szip-jarmu-vezerlo">
            <p class="urlap-mezo">
              <label class="type-ui-caption urlap-cimke" for="k-kocsim3">A szippantóautó űrtartalma
                <span class="szip-egyseg">(m³)</span>
                <span class="type-data-value szip-pelda-jel" data-szip-pelda="kocsiM3">példa</span></label>
              <input class="urlap-input" type="number" id="k-kocsim3" name="kocsiM3"
                     inputmode="decimal" min="1" max="20" step="0.5">
            </p>
            <div class="szip-kocsi-valaszto">
              <p class="type-ui-caption urlap-cimke" id="k-kocsi-cimke">Gyakori járműméretek</p>
              <div class="szip-kocsi-sor" data-szip-kocsi-sor role="group" aria-labelledby="k-kocsi-cimke"></div>
            </div>

            <ul class="szip-tank-cimkek" role="list">
              <li class="szip-tank-cimke">
                <span class="type-ui-caption szip-tank-cimke-nev">
                  <span class="szip-jm-folt" data-szip-folt="urites" aria-hidden="true"></span>
                  Amit elvisznek</span>
                <span class="type-ui-body-strong szip-tank-cimke-ertek" data-szip-tank-cimke="m3">—</span>
              </li>
              <li class="szip-tank-cimke">
                <span class="type-ui-caption szip-tank-cimke-nev">
                  <span class="szip-jm-folt" data-szip-folt="minimum" aria-hidden="true"></span>
                  Amit kiszámláznak</span>
                <span class="type-ui-body-strong szip-tank-cimke-ertek" data-szip-tank-cimke="fizetett">—</span>
              </li>
              <li class="szip-tank-cimke">
                <span class="type-ui-caption szip-tank-cimke-nev">Tartálykihasználás</span>
                <span class="type-ui-body-strong szip-tank-cimke-ertek" data-szip-tank-cimke="kihasznalas">—</span>
              </li>
            </ul>
          </div>
        </div>

        <p class="type-ui-caption szip-egyseg">A járműméret <strong>önmagában nem változtatja a díjat</strong>:
          azt a foglalt mennyiség és az ürítési díj adja. Két helyen számít mégis. Egy: ha a szolgáltató a
          <strong>teljes kocsit</strong> számlázza, akkor a foglalt mennyiséghez ugyanezt az értéket írja be —
          onnantól minden járműméret más díjat ad. Kettő: a <strong>tartálykihasználás</strong> az, ami a fajlagos
          díjat lenyomja, mert a kiszállási díj és a minimumdíj több köbméterre oszlik el.</p>
      </fieldset>
'''

def kalkulator():
    m = _mezo
    hol = '\n'.join([
        m('alkalom', 'Évente hány alkalommal szippantat?', 'alkalom/év',
          'Ha nem tudja pontosan, a legutóbbi két szippantás közti idővel számoljon.',
          lepes='1', maxi='52', pelda=True),
        m('m3', 'Alkalmanként hány m³-t szállítanak el?', 'm³/alkalom',
          'A számlán szereplő mennyiség. Ha a szolgáltató a kocsi térfogatát írja ki, azt adja meg.',
          lepes='0.5', maxi='50', pelda=True),
    ])
    dijak = '\n'.join([
        m('kiszallas', 'Kiszállási / alapdíj', 'Ft/alkalom',
          'Lehet nulla is — nem minden szolgáltatónál külön tétel.', maxi='1000000', pelda=True),
        m('uritesM3', 'Ürítési díj', 'Ft/m³', '', maxi='500000', pelda=True),
        m('minimumDij', 'Minimumdíj', 'Ft/alkalom',
          'Ha nincs minimumdíj, írjon nullát.', maxi='2000000', pelda=True),
        m('minimumM3', 'Ebből mennyi elszállítását tartalmazza?', 'm³',
          'Nullától a kocsi űrtartalmáig. Ha a teljes kocsit ki kell fizetni, '
          'ide ugyanaz kerül, mint az űrtartalomhoz.',
          lepes='0.5', maxi='50', pelda=True),
    ])
    tovabbi = '\n'.join([
        m('kmDij', 'Távolságarányos díj', 'Ft/km',
          'Csak ha a számlán külön szerepel.', maxi='50000'),
        m('tavolsagKm', 'Megteendő távolság', 'km',
          'Ahogy a szolgáltató számolja — oda-vissza vagy csak oda.', lepes='1', maxi='2000'),
        m('egyeb', 'Egyéb tétel alkalmanként', 'Ft', '', maxi='1000000'),
    ])

    jelmagyarazat = '\n'.join(
        f'''            <li class="szip-jm-sor">
              <span class="szip-jm-folt" data-szip-folt="{k}" aria-hidden="true"></span>
              <span class="type-ui-caption szip-jm-nev">{nev}</span>
              <span class="type-data-value szip-jm-ertek" data-szip-tetel="{k}">—</span>
            </li>'''
        for k, nev in [
            ('kiszallas', 'Kiszállási díj'),
            ('urites', 'Ürítés — amit elvisznek'),
            ('minimum', 'Minimum-felár — amit nem visznek el'),
            ('km', 'Távolsági díj'),
            ('egyeb', 'Egyéb'),
        ])
    savok = '\n'.join(
        f'              <span class="szip-sav-elem" data-szip-sav-elem="{k}" hidden></span>'
        for k in ['kiszallas', 'urites', 'minimum', 'km', 'egyeb'])

    return f'''
  <section class="section" id="kalkulator" aria-labelledby="kalkulator-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Kalkulátor</p>
        <h2 class="type-display-section-title section-title" id="kalkulator-cim">Számolja ki a saját éves szippantási költségét</h2>
        <p class="type-ui-body section-lead">A díjmezők működő <strong>példaértékekkel</strong> indulnak, hogy legyen mit
          nézni — ezek nem egy konkrét település díjai. Írja felül őket a saját számláján szereplő értékekkel: a
          példajelzés minden mezőről lekerül, amint hozzányúl.</p>
      </header>

      <div class="szip-racs" data-szip-vart>
        <div class="szip-bemenet">

          <fieldset class="szip-csoport">
            <legend class="type-ui-card-title szip-csoport-cim">Hol és mennyit</legend>
            <p class="urlap-mezo">
              <label class="type-ui-caption urlap-cimke" for="k-megye">Vármegye</label>
              <select class="urlap-input" id="k-megye" name="megye">
                <option value="">Válasszon vármegyét…</option>
              </select>
            </p>
            <p class="urlap-mezo">
              <label class="type-ui-caption urlap-cimke" for="k-telepules">Település</label>
              <input class="urlap-input" type="text" id="k-telepules" name="telepules"
                     list="szip-telepulesek" maxlength="120" autocomplete="off"
                     placeholder="ahol az ingatlan van">
              <!-- A javaslatlista KIZÁRÓLAG azokat a helyeket kínálja fel,
                   amelyekről tényleg van adatunk. Teljes településlista azt
                   sugallná, hogy mindegyikhez tartozik díjszabás. -->
              <datalist id="szip-telepulesek"></datalist>
            </p>
            <p class="type-ui-caption szip-talalat" data-szip-talalat hidden></p>
            <p class="urlap-akcio">
              <button class="btn btn-secondary btn-kicsi" type="button" data-szip-betolt hidden>
                Az ismert díjak betöltése
              </button>
            </p>
            <div class="szip-mezosor">
{hol}
            </div>
          </fieldset>

          <fieldset class="szip-csoport">
            <legend class="type-ui-card-title szip-csoport-cim">A település díjszabása</legend>
            <p class="type-ui-caption szip-csoport-lead">Ezek nem a mi áraink. A nem közművel elvezetett háztartási
              szennyvíz begyűjtése közszolgáltatás — a díjat a közszolgáltató és az önkormányzat állapítja meg. Azt írja
              be, ami a számláján szerepel.</p>
            <div class="szip-mezosor">
{dijak}
            </div>
          </fieldset>

          <fieldset class="szip-csoport">
            <legend class="type-ui-card-title szip-csoport-cim">További költségek — ha a számlán szerepelnek</legend>
            <p class="type-ui-caption szip-csoport-lead">Mindhárom mező elhagyható. Üresen hagyva nem kerülnek be a
              számításba, és a költségsávban sem jelennek meg.</p>
            <div class="szip-mezosor-harmas">
{tovabbi}
            </div>
          </fieldset>

        </div>

        <aside class="szip-eredmeny" aria-labelledby="eredmeny-cim">
          <div class="szip-fo">
            <p class="type-data-eyebrow szip-fo-cimke" id="eredmeny-cim">Éves szippantási költség</p>
            <p class="type-display-page-title szip-fo-ertek" data-szip-ki="ev">—</p>
          </div>
          <div class="szip-fo">
            <p class="type-ui-caption szip-fo-cimke">Alkalmanként</p>
            <p class="type-display-section-title szip-fo-ertek" data-szip-ki="alkalom">—</p>
          </div>

          <div class="szip-sav" data-szip-sav role="img" aria-label="Az alkalmankénti díj összetétele">
{savok}
          </div>
          <ul class="szip-jelmagyarazat" role="list">
{jelmagyarazat}
          </ul>

          <div class="szip-mellek">
            <p class="szip-mellek-tetel">
              <span class="szip-mellek-cimke type-ui-caption">Fajlagos díj arra, amit elvisznek</span>
              <span class="szip-mellek-ertek type-ui-body-strong" data-szip-ki="fajlagos">—</span></p>
            <p class="szip-mellek-tetel">
              <span class="szip-mellek-cimke type-ui-caption">Elszámolt mennyiség alkalmanként</span>
              <span class="szip-mellek-ertek type-ui-body-strong" data-szip-ki="elszamolt">—</span></p>
          </div>

          <p class="type-ui-caption szip-talalat" data-szip-pelda-sav hidden>
            Példaértékekkel számol. Írja felül a díjmezőket a saját számlája alapján.</p>
          <!-- EGYETLEN élő régió az egész kalkulátorra, késleltetve. A látható
               számokon szándékosan NINCS `aria-live`: gépelés közben minden
               leütésnél újra felolvasnák magukat, és a felület használhatatlan
               lenne képernyőolvasóval. -->
          <p class="visually-hidden" role="status" aria-live="polite" data-szip-elo></p>
          <p class="urlap-akcio">
            <button class="btn btn-secondary btn-kicsi" type="button" data-szip-pelda-gomb>
              Példaértékek visszaállítása
            </button>
          </p>
        </aside>
      </div>

{TANK_SVG}
      <!-- A modul legfontosabb állítása. Korábban egyetlen tömött bekezdés
           volt benne négy számmal — olvashatatlan. Most cím + négy adatcella:
           a látogató ránézésre látja, mennyiről van szó. -->
      <aside class="szip-jelzes" data-szip-jelzes hidden>
        <p class="type-ui-card-title szip-jelzes-cim">Fizet olyan mennyiségért, amit nem visznek el</p>
        <ul class="szip-jelzes-adatok" role="list">
          <li class="szip-jelzes-tetel">
            <span class="type-ui-caption szip-jelzes-nev">Amit kifizet, de nem visznek el</span>
            <span class="type-ui-body-strong szip-jelzes-ertek" data-szip-jelzes-ertek="nemVitt">—</span>
          </li>
          <li class="szip-jelzes-tetel">
            <span class="type-ui-caption szip-jelzes-nev">Ez alkalmanként</span>
            <span class="type-ui-body-strong szip-jelzes-ertek" data-szip-jelzes-ertek="alkalom">—</span>
          </li>
          <li class="szip-jelzes-tetel">
            <span class="type-ui-caption szip-jelzes-nev">Egy évben</span>
            <span class="type-ui-body-strong szip-jelzes-ertek" data-szip-jelzes-ertek="ev">—</span>
          </li>
          <li class="szip-jelzes-tetel">
            <span class="type-ui-caption szip-jelzes-nev">Fajlagos díj teltebb tartállyal</span>
            <span class="type-ui-body-strong szip-jelzes-ertek" data-szip-jelzes-ertek="teli">—</span>
          </li>
        </ul>
        <p class="type-ui-caption szip-jelzes-labjegyzet">Ha ritkábban hívja ki, de teltebb tartállyal,
          ugyanannyi szennyvízre kevesebbet fizet — a kiszállási díj és a minimumdíj ilyenkor több
          köbméterre oszlik el.</p>
      </aside>

      <noscript>
        <div class="szip-jelzes type-ui-body">
          <p>A kalkulátor JavaScript nélkül nem tud számolni — a képlet viszont papíron is elvégezhető:</p>
          <p><strong>elszámolt mennyiség</strong> = a nagyobbik az elszállított és a minimumdíjban foglalt mennyiség
            közül · <strong>alkalmankénti díj</strong> = kiszállási díj + a nagyobbik a minimumdíj és az
            (ürítési díj × elszámolt mennyiség) közül + további tételek ·
            <strong>éves díj</strong> = alkalmankénti díj × az éves alkalomszám.</p>
          <p>Ha inkább megbeszélné: <a href="tel:+3633200211">+36 33 200 211</a> vagy
            <a href="mailto:kapcsolat@okotechhome.hu">kapcsolat@okotechhome.hu</a>.</p>
        </div>
      </noscript>
    </div>
  </section>
'''


TERKEP = '''
  <section class="section section-alt" id="adatbazis" aria-labelledby="adatbazis-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Adatbázis</p>
        <h2 class="type-display-section-title section-title" id="adatbazis-cim">Hol tartunk a települési díjakkal</h2>
        <p class="type-ui-body section-lead">A szippantási díj településenként és szolgáltatónként más, és nincs róla
          nyilvános, összesített nyilvántartás. Ezt az adatbázist a beküldésekből építjük — kizárólag olyan sorral,
          amelyet számla, szolgáltatói ártáblázat vagy önkormányzati rendelet igazol. Amíg egy településről nincs
          igazolt adatunk, addig a térképen sem lesz.</p>
      </header>

      <div class="szip-terkep-doboz" data-szip-vart>
        <div class="szip-terkep-oszlop">
          <p class="type-ui-body-strong szip-terkep-osszeg" data-szip-terkep-osszeg></p>
          <ul class="szip-terkep-jelmagyarazat" role="list">
            <li class="szip-terkep-jm type-ui-caption">
              <span class="szip-terkep-jm-folt" data-allapot="van" aria-hidden="true"></span>Van igazolt díjadatunk</li>
            <li class="szip-terkep-jm type-ui-caption">
              <span class="szip-terkep-jm-folt" data-allapot="nincs" aria-hidden="true"></span>Még nincs — gyűjtés alatt</li>
          </ul>
          <p class="type-ui-body szip-terkep-reszlet" data-szip-terkep-reszlet role="status" aria-live="polite"></p>
          <p class="type-ui-caption szip-egyseg">A térkép csempékből áll, nem határvonalakból: minden vármegye azonos
            méretű mezőt kap, a helyük a valós kelet–nyugati és észak–déli sorrendet követi. Pontos határvonalat
            szándékosan nem rajzolunk — arra nincs hiteles térképi forrásunk.</p>
          <p><a class="text-link" href="#bekuldes"><span class="link-label">Küldje be a saját települését<span class="action-arrow-end" aria-hidden="true">&rarr;</span></span></a></p>
        </div>
        <div class="szip-terkep-gorgo">
          <div data-szip-terkep></div>
        </div>
      </div>

      <noscript>
        <p class="type-ui-body">A vármegyei áttekintő JavaScript nélkül nem jelenik meg. Az adatbázis jelenlegi
          állásáról és egy adott település díjszabásáról telefonon is tudunk tájékoztatást adni:
          <a href="tel:+3633200211">+36 33 200 211</a>.</p>
      </noscript>
    </div>
  </section>
'''


def bekuldo():
    forrasok = '\n'.join(
        f'                <option value="{k}">{v}</option>' for k, v in [
            ('szamla', 'Saját szippantási számla'),
            ('artablazat', 'Szolgáltatói ártáblázat vagy weboldal'),
            ('rendelet', 'Önkormányzati rendelet'),
            ('telefon', 'Telefonos tájékoztatás a szolgáltatótól'),
            ('egyeb', 'Egyéb'),
        ])

    def um(nev, cimke, egyseg, lepes='1', maxi=''):
        azon = 'b-' + nev.lower()
        maxattr = f' max="{maxi}"' if maxi else ''
        return f'''          <p class="urlap-mezo">
            <label class="type-ui-caption urlap-cimke" for="{azon}">{cimke}
              <span class="szip-egyseg">({egyseg})</span></label>
            <input class="urlap-input" type="number" id="{azon}" name="{nev}"
                   inputmode="decimal" min="0"{maxattr} step="{lepes}">
          </p>'''

    return f'''
  <section class="section" id="bekuldes" aria-labelledby="bekuldes-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Adatbeküldés</p>
        <h2 class="type-display-section-title section-title" id="bekuldes-cim">Ismeri a saját településén érvényes díjakat?</h2>
        <p class="type-ui-body section-lead">Küldje be — és a következő érdeklődő már készen kapja. Csak olyan sort
          veszünk fel, amelyhez forrás is tartozik, és minden beküldést emberi ellenőrzés után rögzítünk, ezért az adat
          nem jelenik meg azonnal a térképen. Nevet és e-mail-címet nem kérünk; e-mailt csak akkor adjon meg, ha
          szeretné, hogy visszajelezzünk.</p>
      </header>

      <p class="urlap-akcio">
        <button class="btn btn-secondary btn-kicsi" type="button" data-szip-atmasol>
          A kalkulátorban megadott értékek átemelése
        </button>
      </p>

      <!-- Az űrlap JS NÉLKÜL is működik: sima POST az api/szippantasi-dij
           végpontra, amely ilyenkor JSON-t ad vissza. Az `urlap.js` csak annyit
           tesz, hogy a választ helyben jeleníti meg. -->
      <form class="urlap" method="post" action="api/szippantasi-dij" data-urlap data-szip-urlap>
        <p class="szip-atmasolva type-ui-body" data-szip-atmasolva role="status" aria-live="polite" hidden></p>

        <div class="urlap-sor">
          <p class="urlap-mezo">
            <label class="type-ui-caption urlap-cimke" for="b-megye">Vármegye <span aria-hidden="true">*</span></label>
            <select class="urlap-input" id="b-megye" name="megye" required>
              <option value="">Válasszon vármegyét…</option>
            </select>
          </p>
          <p class="urlap-mezo">
            <label class="type-ui-caption urlap-cimke" for="b-telepules">Település <span aria-hidden="true">*</span></label>
            <input class="urlap-input" type="text" id="b-telepules" name="telepules" required maxlength="120">
          </p>
        </div>

        <p class="urlap-mezo">
          <label class="type-ui-caption urlap-cimke" for="b-szolgaltato">Közszolgáltató neve</label>
          <input class="urlap-input" type="text" id="b-szolgaltato" name="szolgaltato" maxlength="160"
                 placeholder="ha szerepel a számlán">
        </p>

        <div class="szip-mezosor-harmas">
{um('kiszallas', 'Kiszállási / alapdíj', 'Ft/alkalom', maxi='1000000')}
{um('uritesM3', 'Ürítési díj', 'Ft/m³', maxi='500000')}
{um('minimumDij', 'Minimumdíj', 'Ft/alkalom', maxi='2000000')}
        </div>
        <div class="szip-mezosor-harmas">
{um('minimumM3', 'Ebben foglalt mennyiség', 'm³', lepes='0.5', maxi='50')}
{um('kocsiM3', 'Kocsi űrtartalma', 'm³', lepes='0.5', maxi='50')}
{um('kmDij', 'Távolságarányos díj', 'Ft/km', maxi='50000')}
        </div>
        <p class="type-ui-caption szip-egyseg">Amelyik tételt nem ismeri, hagyja üresen — az üres mező azt jelenti,
          hogy nem tudjuk, a nulla viszont valódi érték (például: nincs kiszállási díj). A kettőt nem cseréljük fel.</p>

        <div class="urlap-sor">
          <p class="urlap-mezo">
            <label class="type-ui-caption urlap-cimke" for="b-ervenyes">Mikortól érvényes</label>
            <input class="urlap-input" type="text" id="b-ervenyes" name="ervenyes" maxlength="40"
                   placeholder="például: 2026. január">
          </p>
          <p class="urlap-mezo">
            <label class="type-ui-caption urlap-cimke" for="b-forras">Honnan tudja? <span aria-hidden="true">*</span></label>
            <select class="urlap-input" id="b-forras" name="forras" required>
              <option value="">Válasszon forrást…</option>
{forrasok}
            </select>
          </p>
        </div>

        <p class="urlap-mezo">
          <label class="type-ui-caption urlap-cimke" for="b-megjegyzes">Megjegyzés</label>
          <textarea class="urlap-input urlap-terulet" id="b-megjegyzes" name="megjegyzes" rows="4" maxlength="1500"
                    placeholder="Bármi, ami a díjszabás megértéséhez kell — például hogy a szolgáltató a teljes kocsit számlázza."></textarea>
        </p>

        <p class="urlap-mezo">
          <label class="type-ui-caption urlap-cimke" for="b-email">E-mail-cím — csak ha visszajelzést kér</label>
          <input class="urlap-input" type="email" id="b-email" name="email" maxlength="254" autocomplete="email">
        </p>

        <p class="urlap-jelolo">
          <input type="checkbox" id="b-hozzajarul" name="hozzajarul" value="1">
          <label class="type-ui-subtitle" for="b-hozzajarul">Ha megadta az e-mail-címét: hozzájárulok, hogy azt a
            beküldés visszajelzéséhez kezeljék.
            <a href="adatkezelesi-tajekoztato">Adatkezelési tájékoztató</a></label>
        </p>

        <!-- Mézesbödön: a robotok kitöltik, ember nem látja. A `nyitva` mező a
             megnyitás időpontja — a túl gyors beküldés is robotra utal. -->
        <p class="urlap-csapda" aria-hidden="true">
          <label for="b-weboldal">Weboldal</label>
          <input type="text" id="b-weboldal" name="weboldal" tabindex="-1" autocomplete="off">
        </p>
        <input type="hidden" name="nyitva" value="" data-urlap-ido>

        <p class="urlap-akcio">
          <button class="btn btn-primary" type="submit">Díjadat beküldése</button>
        </p>
        <p class="type-ui-caption urlap-jog">A <span aria-hidden="true">*</span>-gal jelölt mezők kitöltése kötelező.
          A díjszabás önmagában nem személyes adat; e-mail-címet csak akkor kérünk, ha visszajelzést szeretne.</p>

        <p class="urlap-valasz type-ui-body" role="status" aria-live="polite" data-urlap-valasz hidden></p>
      </form>
    </div>
  </section>
'''


TIPUSOK = '''
  <section class="section section-alt" aria-labelledby="tipusok-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Díjszabás-típusok</p>
        <h2 class="type-display-section-title section-title" id="tipusok-cim">Három szerkezet, amivel találkozni fog</h2>
        <p class="type-ui-body section-lead">Mindhárom ugyanabból a három tételből épül fel — a különbség az, mi
          történik <strong>kis mennyiségnél</strong>. A kalkulátor mindhármat ugyanazzal a képlettel kezeli; Önnek csak
          a mezőket kell helyesen kitöltenie.</p>
      </header>
      <div class="compare-scroll" role="region" aria-labelledby="tipusok-cim" tabindex="0">
        <table class="compare-table">
          <thead>
            <tr>
              <th scope="col">Szempont</th>
              <th scope="col">Csak mennyiség szerint</th>
              <th scope="col">Minimumdíj alsó korlátként</th>
              <th scope="col">A minimumdíj mennyiséget tartalmaz</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row" class="type-ui-subtitle">Mi szerepel a számlán</th>
              <td class="type-ui-subtitle">kiszállási díj (ha van) és ürítési díj köbméterenként</td>
              <td class="type-ui-subtitle">ugyanez, plusz egy legkisebb számlázható összeg</td>
              <td class="type-ui-subtitle">egy alapösszeg, amiért adott mennyiséget elvisznek, és e fölött köbméterár</td>
            </tr>
            <tr>
              <th scope="row" class="type-ui-subtitle">Mit fizet, ha keveset szippantat</th>
              <td class="type-ui-subtitle">arányosan keveset</td>
              <td class="type-ui-subtitle">a minimumdíjat, akkor is, ha a mennyiségalapú összeg kisebb volna</td>
              <td class="type-ui-subtitle">a foglalt mennyiség árát — a különbözetet nem viszik el</td>
            </tr>
            <tr>
              <th scope="row" class="type-ui-subtitle">Mit fizet, ha megtelik a tartály</th>
              <td class="type-ui-subtitle">a tényleges mennyiség árát</td>
              <td class="type-ui-subtitle">a tényleges mennyiség árát — a minimum ilyenkor nem köt</td>
              <td class="type-ui-subtitle">a foglalt mennyiséget, plusz a fölötte lévő köbmétereket</td>
            </tr>
            <tr>
              <th scope="row" class="type-ui-subtitle">Számít-e, hogy teltebb tartállyal hívja ki</th>
              <td class="type-ui-subtitle">csak a kiszállási díj miatt</td>
              <td class="type-ui-subtitle">igen, amíg a minimumdíj alatt jár</td>
              <td class="type-ui-subtitle">igen, ez a legerősebb hatás — a foglalt mennyiséget mindenképp kifizeti</td>
            </tr>
            <tr>
              <th scope="row" class="type-ui-subtitle">Mit írjon a kalkulátorba</th>
              <td class="type-ui-subtitle">minimumdíj: 0 · foglalt mennyiség: 0</td>
              <td class="type-ui-subtitle">minimumdíj: a számla szerint · foglalt mennyiség: 0</td>
              <td class="type-ui-subtitle">minimumdíj és foglalt mennyiség is a számla szerint</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="type-ui-body">Van, ahol a szolgáltató a <strong>teljes kocsit</strong> számlázza akkor is, ha egyetlen
        köbmétert visz el. Ez a harmadik eset szélső változata: a foglalt mennyiséghez a kocsi űrtartalmát írja be.</p>
    </div>
  </section>
'''


CTA = '''
  <section class="section" aria-labelledby="kovetkezo-cim">
    <div class="section-inner">
      <aside class="panel-dark" aria-labelledby="kovetkezo-cim">
        <div class="panel-dark-head">
          <p class="type-data-eyebrow panel-dark-eyebrow">Következő lépés</p>
          <h2 class="type-display-highlight-title panel-dark-title" id="kovetkezo-cim">A szippantás mennyisége technológiafüggő</h2>
        </div>
        <div class="panel-dark-body">
          <p class="type-ui-body panel-dark-text">Ez a kalkulátor a díjszabást bontja szét — azt, hogy mennyit és
            milyen gyakran kell elszállíttatni, a telepített rendszer dönti el. Zárt tárolónál a teljes szennyvíz
            elszállítás tárgya; oldómedencés rendszernél az iszap; aktív biológiai berendezésnél megint más az
            üzemeltetési profil. Melyik mit jelent, azt a megoldásoldalak írják le.</p>
          <p class="type-ui-body panel-dark-text"><a href="megoldasok/oldomedence-szippantas-es-karbantartas">Szippantás és karbantartás oldómedencés rendszernél</a> ·
            <a href="megoldasok/megoldastipusok-osszehasonlitasa">Megoldástípusok összehasonlítása</a></p>
          <p class="panel-dark-actions"><a class="btn btn-inverse" href="konzultacio">Konzultációt kérek</a></p>
        </div>
      </aside>

      <p class="type-ui-caption szip-egyseg">A kalkulátor eredménye <strong>tájékoztató jellegű</strong>: a megadott
        értékekből számol, és nem minősül árajánlatnak. A szippantás nem az ÖkoTech-Home szolgáltatása — a díjat a
        területileg illetékes közszolgáltató és az önkormányzat állapítja meg, és az időben változik. Kötelező érvényű
        adatért a közszolgáltatóhoz vagy az önkormányzathoz forduljon. A számítás a böngészőjében fut: a beírt értékek
        nem kerülnek szerverre, amíg Ön nem küldi be őket az adatbeküldő űrlapon.</p>
    </div>
  </section>
'''


def gyik_szekcio():
    tetelek = '\n'.join(f'''        <details class="faq-item">
          <summary class="faq-q type-ui-card-title">{esc(q)}</summary>
          <div class="faq-a"><p class="type-ui-body">{esc(a)}</p></div>
        </details>''' for q, a in GYIK)
    return f'''
  <section class="section section-alt" aria-labelledby="gyik-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Gyakori kérdések</p>
        <h2 class="type-display-section-title section-title" id="gyik-cim">Amit a leggyakrabban kérdeznek</h2>
      </header>
      <div class="faq">
{tetelek}
      </div>
    </div>
  </section>
'''


def json_ld():
    import json
    faq = ',\n'.join(
        '        {"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False))
        for q, a in GYIK)
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{"@type":"ListItem","position":1,"name":"Főoldal","item":"https://okoth.hu/"}},
        {{"@type":"ListItem","position":2,"name":"{H1}","item":"https://okoth.hu/{URL}"}}
      ]
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
{faq}
      ]
    }}
  ]
}}
</script>'''


def epit():
    fejlec, lablec = _reszek()
    # A modul GYÖKERE a kalkulátort és a csempetérképet fogja össze: a
    # `szippantas.js` minden lekérdezése erre a fára szűkül. A BEKÜLDŐ ŰRLAP
    # szándékosan kívül marad — annak ugyanolyan nevű mezői vannak (`megye`,
    # `telepules`), és ha a gyökéren belülre kerülne, a kitöltése átírná a
    # kalkulátor állapotát.
    modul = ('\n<div class="szip-modul" data-szip>\n'
             + kalkulator() + TERKEP
             + '</div>\n')
    body = (MIT_AD + HOGYAN + modul + bekuldo()
            + TIPUSOK + CTA + gyik_szekcio())

    return f'''<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<!-- TESZT ÜZEMMÓD: az oldal fejlesztés alatt áll. ÉLESÍTÉSKOR ezt a sort
     minden oldalról törölni kell (a .htaccess X-Robots-Tag blokkjával együtt). -->
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{CIM}</title>
<meta name="description" content="{esc(LEIRAS)}">
<link rel="canonical" href="https://okoth.hu/{URL}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(H1)}">
<meta property="og:description" content="{esc(LEIRAS)}">
<meta property="og:image" content="https://okoth.hu/assets/img/oldalak/hero-{KEP}.webp{KEP_V}">
<meta property="og:locale" content="hu_HU">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/css/app.css?v={CSS_V}">
<!-- A témát a `data-theme` hordozza; ez a szkript írja ki, még a törzs
     feldolgozása előtt — így nincs villanás. Lásd assets/js/tema.js. -->
<script src="assets/js/tema.js?v=1"></script>
<!-- Fejlécképet ez a lap NEM tölt be: a fejléc rajzolt (lásd app.css 5.22).
     Az LCP-elem így a főcím, tehát nincs mit előre tölteni. Az `og:image`
     viszont marad — a megosztási kártyához kell egy felvétel. -->
</head>
<body>

{fejlec}

<main id="fotartalom">

  <!-- MODUL-HERO — jelzett eltérés a fényképes `.page-hero`-tól.
       Indoklás: app.css 5.22 és COMPONENTS.md 21. -->
  <section class="szip-hero" aria-labelledby="oldal-cim">
    <div class="szip-hero-inner">
      <div class="szip-hero-copy">
        <nav class="breadcrumb szip-hero-morzsa" aria-label="Morzsamenü">
          <ol class="breadcrumb-list type-ui-caption" role="list">
            <li><a href="./">Főoldal</a></li>
            <li aria-current="page">{H1}</li>
          </ol>
        </nav>
        <p class="type-data-eyebrow szip-hero-eyebrow">
          <span class="szip-hero-pont" aria-hidden="true"></span>Költségkalkulátor
        </p>
        <h1 class="type-display-hero szip-hero-cim" id="oldal-cim">{H1}</h1>
        <p class="type-ui-body szip-hero-lead">{LEAD}</p>
        <ul class="szip-hero-chipek" role="list">
          <li class="type-data-value szip-hero-chip">
            <span class="szip-hero-chip-folt" data-szip-folt="kiszallas" aria-hidden="true"></span>Kiszállási díj</li>
          <li class="type-data-value szip-hero-chip">
            <span class="szip-hero-chip-folt" data-szip-folt="urites" aria-hidden="true"></span>Ürítési díj Ft/m³</li>
          <li class="type-data-value szip-hero-chip">
            <span class="szip-hero-chip-folt" data-szip-folt="minimum" aria-hidden="true"></span>Minimumdíj</li>
        </ul>
        <p class="szip-hero-akciok">
          <a class="btn btn-primary" href="#kalkulator">Számoljuk ki</a>
          <a class="text-link" href="#adatbazis"><span class="link-label">A települési adatbázis<span class="action-arrow-end" aria-hidden="true">&rarr;</span></span></a>
        </p>
      </div>
      <div class="szip-hero-abra">
        {HERO_ABRA}
      </div>
    </div>
  </section>
{body}
</main>

{lablec}

<!-- A KONFIG a modul ELŐTT tölt be, halasztás nélkül: a `szippantas.js` az
     induláskor olvassa a `window.OTH_SZIPPANTAS` objektumot. Ha megfordulna a
     sorrend, a modul példaértékek és vármegyelista nélkül indulna. -->
<script src="assets/data/szippantas-konfig.js?v={KONFIG_V}"></script>
<script src="assets/js/site.js?v=3" defer></script>
<script src="assets/js/kalauz.js?v=32" defer></script>
<script src="assets/js/urlap.js?v=1" defer></script>
<script src="assets/js/szippantas.js?v={JS_V}" defer></script>
{json_ld()}

</body>
</html>
'''


if __name__ == '__main__':
    CEL.write_text(epit(), encoding='utf-8')
    print(f'kész: {CEL.relative_to(WEB.parent)} ({len(epit().splitlines())} sor)')
