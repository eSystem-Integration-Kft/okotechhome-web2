#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kapcsolat oldal — a webhely egyetemes CTA-célpontja.

A sitemap az ÖkoTech-Home kategória alá sorolja, de a gyökérben áll: minden
szekció és minden aloldal ide mutat, és a fejléc CTA-ja is ez. Ha később a
sitemap szerinti helyre kerül, 301-gyel átirányítható.

A megszólítás-blokkok a sitemap 3. szintjét követik: Új érdeklődők · Meglévő
ügyfelek · Szakmai partnerek · Sajtó · Elérhetőség.
"""
import sys, pathlib, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import sec_numbered, sec_situations, sec_prose, sec_faq

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

# A gyökérben a fejléc-hivatkozások nem ../-rel kezdődnek. A CSUPASZ `../`-t
# külön kell kezelni: abból üres href lenne, ami az AKTUÁLIS oldalra mutat —
# a logóra kattintva nem történne semmi. Ezért az lesz './'.
HEADER = G.HEADER.replace('href="../"', 'href="./"')
HEADER = re.sub(r'href="\.\./', 'href="', HEADER)
HEADER = HEADER.replace('src="../assets/', 'src="assets/')

TEL_HREF, TEL = 'tel:+3633200211', '+36 33 200 211'
MAIL = 'kapcsolat@okotechhome.hu'
CIM = '2509 Esztergom, Strázsa u. 12.'

SECTIONS = [
    sec_situations(
        'Megkeresés típusa', 'Kihez kerül a megkeresése?',
        'Négy külön útvonal, mert négy különböző kérdésről van szó. Válassza azt, '
        'amelyik a helyzetére illik — így rögtön ahhoz jut, aki válaszolni tud.',
        [('nav-inditas', 'Új érdeklődő vagyok',
          'Még nincs rendszer, és azt szeretné tudni, mi jöhet szóba az ingatlanán. '
          'Ehhez a település neve, a használat módja és a háztartás létszáma elég a kezdéshez.',
          '#urlap', 'Írjon nekünk'),
         ('nav-szerviz', 'Meglévő ügyfél vagyok',
          'Üzemeltetési kérdés, hibajelenség, alkatrész vagy szervizkérés. '
          'Adja meg a berendezés típusát és a telepítés helyét — az adattábláról leolvasható.',
          'helyzetem/mar-van-rendszerem-segitsegre-van-szuksegem', 'Már van rendszerem'),
         ('nav-vallalkozas', 'Szakmai partner vagyok',
          'Tervező, kivitelező, önkormányzat vagy viszonteladó. Műszaki dokumentációt, '
          'méretezési segítséget és együttműködési feltételeket egyaránt tudunk küldeni.',
          '#urlap', 'Szakmai megkeresés'),
         ('nav-tudastar', 'Sajtó vagy egyéb megkeresés',
          'Szakmai anyag, interjú vagy egyéb kérdés. Írja meg a határidőt is, '
          'hogy tudjunk hozzá igazodni.',
          '#urlap', 'Egyéb megkeresés'),
         ]),
    sec_numbered(
        'Előkészítés', 'Mit írjon meg, hogy érdemi választ tudjunk adni?',
        'Nem kell mindent tudnia — de minél több szerepel az alábbiakból, annál '
        'pontosabb választ tudunk küldeni kiszállás előtt.',
        ['<strong>Az ingatlan helye.</strong> A település neve elég a kezdéshez; a helyrajzi '
         'számmal a helyi szabályozás is ellenőrizhető.',
         '<strong>A használat módja és a létszám.</strong> Állandó lakhatás vagy időszakos '
         'használat, hány fő, és van-e kiszámítható csúcs a terhelésben.',
         '<strong>A jelenlegi helyzet.</strong> Van-e már valamilyen rendszer a telken, és ha '
         'igen, milyen — emésztő, oldómedence vagy tisztítóberendezés.',
         '<strong>Mit tud a telekről.</strong> Talaj, tavaszi vízállás, közeli kutak, '
         'megközelíthetőség — amennyit tud, annyit.',
         '<strong>Hol tart a projektben.</strong> Tájékozódik, telket néz, tervez, vagy már '
         'ajánlatot kér. Ez határozza meg, mivel tudunk a leginkább segíteni.']),
]

FORM = '''
  <section class="section" id="urlap" aria-labelledby="urlap-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Üzenet</p>
        <h2 class="type-display-section-title section-title" id="urlap-cim">Írjon nekünk</h2>
        <p class="type-ui-body section-lead">Munkanapokon igyekszünk egy munkanapon belül
          válaszolni. Ha sürgős, a telefon a gyorsabb út:
          <a href="{tel_href}">{tel}</a>.</p>
      </header>

      <!-- Az űrlap JS NÉLKÜL is működik: sima POST az api/kapcsolat végpontra,
           amely ilyenkor JSON-t ad vissza. A JS ezt fogja el, és helyben
           jeleníti meg a választ — de a küldés nem függ tőle. -->
      <form class="urlap" method="post" action="api/kapcsolat" data-urlap>
        <div class="urlap-sor">
          <p class="urlap-mezo">
            <label class="type-ui-caption urlap-cimke" for="f-nev">Név <span aria-hidden="true">*</span></label>
            <input class="urlap-input" type="text" id="f-nev" name="nev" required
                   autocomplete="name" maxlength="120">
          </p>
          <p class="urlap-mezo">
            <label class="type-ui-caption urlap-cimke" for="f-email">E-mail <span aria-hidden="true">*</span></label>
            <input class="urlap-input" type="email" id="f-email" name="email" required
                   autocomplete="email" maxlength="254">
          </p>
        </div>

        <div class="urlap-sor">
          <p class="urlap-mezo">
            <label class="type-ui-caption urlap-cimke" for="f-tel">Telefon</label>
            <input class="urlap-input" type="tel" id="f-tel" name="telefon"
                   autocomplete="tel" maxlength="40" placeholder="+36 30 123 4567">
          </p>
          <p class="urlap-mezo">
            <label class="type-ui-caption urlap-cimke" for="f-telepules">Település</label>
            <input class="urlap-input" type="text" id="f-telepules" name="telepules"
                   maxlength="120" placeholder="ahol az ingatlan van">
          </p>
        </div>

        <p class="urlap-mezo">
          <label class="type-ui-caption urlap-cimke" for="f-tema">Megkeresés típusa</label>
          <select class="urlap-input" id="f-tema" name="tema">
            <option value="uj">Új érdeklődő vagyok</option>
            <option value="ugyfel">Meglévő ügyfél vagyok</option>
            <option value="partner">Szakmai partner vagyok</option>
            <option value="sajto">Sajtó vagy egyéb megkeresés</option>
          </select>
        </p>

        <p class="urlap-mezo">
          <label class="type-ui-caption urlap-cimke" for="f-uzenet">Üzenet <span aria-hidden="true">*</span></label>
          <textarea class="urlap-input urlap-terulet" id="f-uzenet" name="uzenet" required
                    rows="6" maxlength="5000"
                    placeholder="Írja le néhány mondatban a helyzetét: hol van az ingatlan, hogyan használják, és mi a kérdése."></textarea>
        </p>

        <p class="urlap-jelolo">
          <input type="checkbox" id="f-hozzajarul" name="hozzajarul" value="1" required>
          <label class="type-ui-subtitle" for="f-hozzajarul">Hozzájárulok, hogy a megadott adataimat
            a megkeresés megválaszolása céljából kezeljék.
            <a href="adatkezelesi-tajekoztato">Adatkezelési tájékoztató</a> <span aria-hidden="true">*</span></label>
        </p>

        <!-- Mézesbödön: a robotok kitöltik, ember nem látja. A `nyitva` mező a
             megnyitás időpontja — a túl gyors beküldés is robotra utal. -->
        <p class="urlap-csapda" aria-hidden="true">
          <label for="f-weboldal">Weboldal</label>
          <input type="text" id="f-weboldal" name="weboldal" tabindex="-1" autocomplete="off">
        </p>
        <input type="hidden" name="nyitva" value="" data-urlap-ido>

        <p class="urlap-akcio">
          <button class="btn btn-primary" type="submit">Üzenet küldése</button>
        </p>
        <p class="type-ui-caption urlap-jog">A <span aria-hidden="true">*</span>-gal jelölt mezők
          kitöltése kötelező. Az adatait kizárólag a megkeresés megválaszolására használjuk.</p>

        <!-- A visszajelzés helye. `aria-live`: a képernyőolvasó felolvassa,
             amint megjelenik — enélkül a nem látó felhasználó nem tudná meg,
             sikerült-e a küldés. -->
        <p class="urlap-valasz type-ui-body" role="status" aria-live="polite" data-urlap-valasz hidden></p>
      </form>

      <p class="type-ui-body urlap-kozvetlen">Vagy közvetlenül:
        <a href="{tel_href}">{tel}</a> ·
        <a href="mailto:{mail}">{mail}</a> ·
        {cim}</p>
    </div>
  </section>
'''.format(tel_href=TEL_HREF, tel=TEL, mail=MAIL, cim=CIM)

SECTIONS.append(FORM)
TERKEP = '''
  <section class="section" aria-labelledby="terkep-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Elérhetőség</p>
        <h2 class="type-display-section-title section-title" id="terkep-cim">Elérhetőség és megközelítés</h2>
      </header>
      <p class="type-ui-body section-lead"><strong>ÖkoTech Home</strong> — {cim}</p>
      <p class="type-ui-body section-lead">Telefon: <a href="{tel_href}">{tel}</a> ·
        E-mail: <a href="mailto:{mail}">{mail}</a></p>
      <p class="type-ui-body section-lead">A helyszíni felmérésre az ország egész területén
        vállalkozunk. A látogatás időpontját előre egyeztetjük, és előtte átküldjük, mit
        érdemes hozzá előkészíteni.</p>
    </div>
  </section>

  <!-- A térkép TELJES SZÉLESSÉGŰ, a két széle a lap hátterébe fakul.
       Alapból a saját, kiszolgált állókép látszik: így a betöltés nem küld
       adatot harmadik félnek. A Google Térkép csak KATTINTÁSRA töltődik be —
       az iframe hozzájárulás nélkül sütit tenne le és elküldené a látogató
       IP-jét, ami hozzájárulás nélkül nem jogszerű. -->
  <section class="terkep" aria-labelledby="terkep-cim" data-terkep>
    <figure class="terkep-kep">
      <picture>
        <source media="(max-width: 1024px)" srcset="assets/img/terkep-esztergom-1200.webp" width="1144" height="300">
        <img src="assets/img/terkep-esztergom.webp" width="2288" height="600"
             alt="Térképrészlet Esztergomról, a Strázsa utcai telephely környékével"
             loading="lazy" decoding="async">
      </picture>
    </figure>

    <span class="terkep-jelolo" aria-hidden="true">
      <svg viewBox="0 0 48 60" role="img">
        <path class="terkep-jelolo-test" d="M24 2c-9.4 0-17 7.6-17 17 0 12.4 17 39 17 39s17-26.6 17-39c0-9.4-7.6-17-17-17z"/>
        <circle class="terkep-jelolo-mag" cx="24" cy="19" r="7.5"/>
      </svg>
      <span class="terkep-jelolo-gyuru"></span>
    </span>

    <p class="terkep-cimke type-ui-card-title">ÖkoTech Home<span class="type-ui-caption terkep-cimke-alatt">{cim}</span></p>

    <p class="terkep-akcio">
      <button type="button" class="btn btn-secondary" data-terkep-betolt>Google Térkép megnyitása itt</button>
      <a class="text-link terkep-uj" href="https://www.google.com/maps/search/?api=1&amp;query=2509+Esztergom%2C+Str%C3%A1zsa+u.+12."
         target="_blank" rel="noopener noreferrer"><span class="link-label">Megnyitom új lapon<span class="action-arrow-end" aria-hidden="true">&rarr;</span></span></a>
    </p>

    <p class="type-ui-caption terkep-jog">A térképrészlet forrása az OpenStreetMap
      (© OpenStreetMap közreműködői). A Google Térkép betöltésekor a Google adatokat kaphat
      Önről — ezért csak az Ön kattintására töltjük be.</p>
  </section>
'''.format(tel_href=TEL_HREF, tel=TEL, mail=MAIL, cim=CIM)
SECTIONS.append(TERKEP)
SECTIONS.append(sec_faq([
    ('Mennyi idő alatt kapok választ?',
     'Munkanapokon egy munkanapon belül igyekszünk válaszolni. Ha a kérdés felmérést igényel, '
     'a válaszban időpontot is javasolunk.'),
    ('A felmérés fizetős?',
     'A felmérés feltételeit a helyszín és a feladat összetettsége határozza meg; ezt a '
     'megkeresésre adott válaszban előre és egyértelműen megírjuk, hogy ne érje meglepetés.'),
    ('Az egész országban vállalnak munkát?',
     'Igen, a felmérést és a telepítést az ország egész területén végezzük. A távolság a '
     'kiszállásban jelenhet meg költségtételként, ezt az ajánlat tartalmazza.'),
]))

PAGE = dict(
    file='kapcsolat.html', url='kapcsolat', img='kapcsolat',
    title='Kapcsolat — felmérés, ajánlat, szerviz | ÖkoTech Home',
    desc=('Írjon vagy telefonáljon: új érdeklődőként, meglévő ügyfélként, szakmai partnerként '
          'vagy sajtómegkeresésként. Elérhetőség, és amit érdemes a megkereséshez előkészíteni.'),
    h1='Kapcsolat',
    alt=('Helyszíni felmérés eszközei egy jármű raktere mellett: összehajtott műszaki rajz, '
         'jegyzetfüzet, colstok és talajmintavevő zacskó, a háttérben aknafedlap a gyepen'),
    lead=('Négy különböző okból szokás írni: valaki most tájékozódik, valakinek már van '
          'rendszere, valaki szakmai partnerként keres, és van, aki sajtóként. Alább '
          'kiválaszthatja, melyik illik Önre — a válasz így gyorsabb és pontosabb lesz.'),
    crumbs=[('Főoldal', './')],
    sections=SECTIONS,
)

if __name__ == '__main__':
    html = G.build(PAGE)
    # Gyökérszint: a fejléc és az eszközhivatkozások ../ nélkül állnak.
    html = html.replace(G.HEADER, HEADER)
    html = re.sub(r'(href|src|imagesrcset|srcset)="\.\./', r'\1="', html)
    html = html.replace('../assets/', 'assets/')
    html = html.replace('<script src="assets/js/site.js?v=3" defer></script>',
                        '<script src="assets/js/site.js?v=3" defer></script>\n'
                        '<script src="assets/js/urlap.js?v=1" defer></script>\n'
                        '<script src="assets/js/terkep.js?v=1" defer></script>')
    out = WEB / PAGE['file']
    out.write_text(html, encoding='utf-8')
    print(f"{PAGE['file']}  {len(html)//1024} KB")
