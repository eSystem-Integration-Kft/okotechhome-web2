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

# A gyökérben a fejléc-hivatkozások nem ../-rel kezdődnek.
HEADER = re.sub(r'href="\.\./', 'href="', G.HEADER)
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
          válaszolni. Ha sürgős, a telefon a gyorsabb út.</p>
      </header>

      <!-- ADATHIÁNY: az űrlap küldési végpontja még nincs beállítva. Amíg nincs,
           az űrlap NEM tesz úgy, mintha elküldte volna az üzenetet: a gomb helyett
           a közvetlen elérhetőségek állnak itt. A végpontot ugyanoda kell felvenni,
           ahol a döntéstámogató modulé is van: assets/data/aidt-konfig.js -> endpoint. -->
      <div class="panel">
        <p class="type-ui-body"><strong>Az online űrlap még nem éles.</strong> Amíg a küldési
          végpont nincs beállítva, nem teszünk ki olyan űrlapot, amelyik látszólag elküldi az
          üzenetet, valójában nem. Addig a közvetlen elérhetőségek működnek:</p>
        <ul class="fit-list" role="list">
          <li class="type-ui-body"><span class="fit-mark fit-yes" aria-hidden="true"></span><span class="fit-text"><strong>Telefon:</strong> <a href="{tel_href}">{tel}</a> — munkanapokon</span></li>
          <li class="type-ui-body"><span class="fit-mark fit-yes" aria-hidden="true"></span><span class="fit-text"><strong>E-mail:</strong> <a href="mailto:{mail}">{mail}</a></span></li>
          <li class="type-ui-body"><span class="fit-mark fit-yes" aria-hidden="true"></span><span class="fit-text"><strong>Cím:</strong> {cim}</span></li>
        </ul>
      </div>
    </div>
  </section>
'''.format(tel_href=TEL_HREF, tel=TEL, mail=MAIL, cim=CIM)

SECTIONS.append(FORM)
SECTIONS.append(sec_prose(
    'Elérhetőség', 'Elérhetőség és megközelítés',
    [f'<strong>ÖkoTech Home</strong> — {CIM}',
     f'Telefon: <a href="{TEL_HREF}">{TEL}</a> · E-mail: <a href="mailto:{MAIL}">{MAIL}</a>',
     'A helyszíni felmérésre az ország egész területén vállalkozunk. A látogatás időpontját '
     'előre egyeztetjük, és előtte átküldjük, mit érdemes hozzá előkészíteni.',
     '<!-- ADATHIÁNY: nyitvatartás, cégadatok (adószám, cégjegyzékszám) és beágyazott térkép '
     '— ügyféltől kérendő. A térkép beágyazása csak cookie-hozzájárulás után történhet. -->']))
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
    out = WEB / PAGE['file']
    out.write_text(html, encoding='utf-8')
    print(f"{PAGE['file']}  {len(html)//1024} KB")
