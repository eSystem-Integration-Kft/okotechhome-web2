#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""megoldasok_foldal.py — a Megoldások hub lapja (`/megoldasok/`).

MIÉRT. A lap a „szennyvíztisztító rendszer" kifejezésre a 4. helyről a 20.-ra
esett vissza (Bela SEO-blokkja, 2026-09-18). A klaszter ≈320 keresés/hó:
szennyvíztisztító rendszer 140 · szikkasztó rendszer(ek) 60 · házi
szennyvíztisztító rendszer 50 · … ár(ak) 50 · bio szennyvíztisztító rendszer 20.
A lap eddig 417 szó volt, három szakasszal; most ez a klaszter teljes,
kalauzoló lapja.

A SZÖVEG BELÁÉ. Két ponton a webhely saját szóhasználatához igazítva, ahogy a
biológiai lapon is (0.51.00): „2004 óta foglalkozik biológiai
szennyvíztisztítással; saját fejlesztésű A.B. Clear berendezéseit Esztergomban
gyártja" (a cégtörténet szerint a saját fejlesztés 2010-ben indult), és
„CE-jelölés", nem „CE-tanúsítás" (fogalomtár).

A H2-K A MENÜPONTOK. Szándékosan azonos a szövegezés, és a horgony az aloldal
szlugja (`#megoldastipusok-osszehasonlitasa`, `#kizaro-es-korlatozo-feltetelek`,
`#megoldastipus-eloszuro`) — a megamenüből is ide lehet ugrani, és a szerkezet
a keresőnek is egyértelmű.

EZ A LAP OSZTJA SZÉT A BELSŐ LINKERŐT: minden szakaszból megy tovább
hivatkozás a megoldásoldalakra, a HELYZETEM lapokra, a szivárogtatási
vizsgálatra, a közcsatorna-lapra, a tisztítómezőre és az üzemeltetésre.

Szerkezete és készlete a biológiai lapé (`hub-*`, lásd `_web/COMPONENTS.md`).
A fejléc, a lábléc és a szkriptek a kiadott lapból maradnak.

FUTTATÁS:  python3 scripts/oldalgyartas/megoldasok_foldal.py
"""
import html as _html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import megoldasok_abra as abra  # noqa: E402

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
DOMAIN = 'https://okotechhome.hu'
UT = 'megoldasok/'
LAP = WEB / 'megoldasok' / 'index.html'
FRISSITVE = ('2026-09-18', '2026-09', '2026. szeptember')

CIM = 'Szennyvíztisztító rendszer: melyik megoldás való Önnek?'
LEIRAS = ('Miből áll egy szennyvíztisztító rendszer, és melyik megoldástípus mikor megfelelő? '
          'Összehasonlítás, kizáró feltételek és előszűrő kérdések egy helyen.')
H1 = 'Szennyvíztisztító rendszer: melyik megoldás való az Ön ingatlanára?'
LEAD = ('A szennyvíztisztító rendszer nem egyetlen berendezés, hanem három, egymásra épülő rész: '
        'a szennyvizet kezelő műtárgy, a megtisztított víz elhelyezése, és az üzemeltetés. '
        'A legtöbb rossz döntés abból születik, hogy csak az elsőt nézik.')

NL = chr(10)


def esc(s):
    return _html.escape(str(s), quote=False)


def szoveg(s):
    return _html.unescape(re.sub(r'<[^>]+>', '', s)).replace(' ', ' ')


def p(s, osztaly='type-ui-body'):
    return f'        <p class="{osztaly}">{s}</p>'


def tovabb(href, felirat):
    return (f'        <p class="hub-tovabb"><a class="text-link" href="{href}"><span class="link-label">'
            f'{felirat}<span class="action-arrow-end" aria-hidden="true">&rarr;</span></span></a></p>')


def szekcio(azon, eyebrow, cim, torzs, alt=False):
    return f'''
  <section class="section{' section-alt' if alt else ''}" id="{azon}" aria-labelledby="{azon}-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">{esc(eyebrow)}</p>
        <h2 class="type-display-section-title section-title" id="{azon}-cim">{esc(cim)}</h2>
      </header>
{torzs}
    </div>
  </section>'''


def folyo(*bekezdesek):
    return '      <div class="folyoszoveg">' + NL + NL.join(bekezdesek) + NL + '      </div>'


def foto(kep, alt, felirat):
    return f'''      <figure class="hub-foto">
        <img src="../assets/img/galeria/{kep}.webp?v=1" width="1200" height="800"
             alt="{_html.escape(alt, quote=True)}" loading="lazy" decoding="async">
        <figcaption class="type-ui-caption hub-foto-felirat">{felirat}</figcaption>
      </figure>'''


def kartyak(tetelek, osztaly='hub-feltetelek'):
    elemek = NL.join(f'''        <li class="card">
          <span class="card-badge type-data-value" aria-hidden="true">{i:02d}</span>
          <p class="type-ui-body card-text"><strong>{cim}</strong> {szov}</p>
        </li>''' for i, (cim, szov) in enumerate(tetelek, 1))
    return f'''      <ol class="numbered-grid {osztaly}" role="list">
{elemek}
      </ol>'''


TARTALOM = [
    ('rendszer', 'Mi az a szennyvíztisztító rendszer?'),
    ('megoldastipusok-osszehasonlitasa', 'Megoldástípusok összehasonlítása'),
    ('kizaro-es-korlatozo-feltetelek', 'Kizáró és korlátozó feltételek'),
    ('megoldastipus-eloszuro', 'Megoldástípus-előszűrő'),
    ('tisztitomezo-es-uzemeltetes', 'Amit még tervezni kell'),
    ('miert-mi', 'Miért érdemes minket választani?'),
    ('gyik', 'Gyakori kérdések'),
]


def bevezeto():
    linkek = NL.join(f'            <li><a class="hub-tartalom-link" href="#{a}">{esc(c)}</a></li>'
                     for a, c in TARTALOM)
    return f'''
  <section class="section" aria-labelledby="lenyeg-cim">
    <div class="section-inner hub-bevezeto">
      <div class="hub-bevezeto-szoveg">
        <p class="type-ui-body-strong">Ez az oldal a teljes képet adja: milyen megoldástípusok léteznek, melyik mikor megfelelő, mi zárja ki valamelyiket, és néhány kérdés alapján merre érdemes elindulni.</p>
        <nav class="hub-tartalom" aria-label="Az oldal tartalma">
          <p class="type-data-eyebrow hub-tartalom-cim">Az oldalon</p>
          <ol class="hub-tartalom-lista" role="list">
{linkek}
          </ol>
        </nav>
      </div>
      <aside class="hub-lenyeg" aria-labelledby="lenyeg-cim">
        <h2 class="type-display-highlight-title hub-lenyeg-cim" id="lenyeg-cim">A lényeg röviden</h2>
        <p class="type-ui-body">A technológiát a használat jellege dönti el, a megvalósítás feltételeit pedig a telek. A legtöbb ingatlanon nem a berendezés mérete a korlát, hanem az, hogy hova kerül a megtisztított víz.</p>
        <dl class="hub-kulcsadatok">
          <div class="hub-kulcsadat"><dt class="type-ui-caption">A rendszer részei</dt><dd class="type-data-value">3</dd></div>
          <div class="hub-kulcsadat"><dt class="type-ui-caption">Megoldástípus</dt><dd class="type-data-value">3</dd></div>
          <div class="hub-kulcsadat"><dt class="type-ui-caption">Kizáró és korlátozó feltétel</dt><dd class="type-data-value">5</dd></div>
          <div class="hub-kulcsadat"><dt class="type-ui-caption">Előszűrő kérdés</dt><dd class="type-data-value">5</dd></div>
        </dl>
        <p class="type-ui-caption hub-lenyeg-jegyzet">A leggyakoribb valódi korlát a <a href="../projekt-elokeszites/tisztitomezo">tisztítómező</a> helyigénye, nem a berendezés mérete.</p>
      </aside>
    </div>
  </section>'''


def rendszer():
    torzs = NL.join([
        abra.rendszer_abra('rendszer-abra-cim'),
        folyo(
            p('Egy működő szennyvíztisztító rendszer három elemből áll, és mindháromnak rendben '
              'kell lennie.'),
            p('<strong>1 · A kezelés.</strong> Ez az a műtárgy, amely a szennyvizet fogadja: zárt '
              'tároló, <a href="oldomedences-rendszer">oldómedence</a> vagy aktív '
              '<a href="biologiai-szennyviztisztitas">biológiai szennyvíztisztító</a>. Ebben dől '
              'el, milyen minőségű víz megy tovább.'),
            p('<strong>2 · A vízelhelyezés.</strong> A tisztított víznek el kell tudnia távozni — '
              'jellemzően <a href="../projekt-elokeszites/elszivarogtatas">szivárogtatómezőn</a> '
              'keresztül, a talajba. Ez a rész igényli a legtöbb szabad területet, és itt akad el '
              'a legtöbb terv.'),
            p('<strong>3 · Az üzemeltetés.</strong> Rendszeres ellenőrzés, karbantartás, és a '
              'szennyvíztisztító rendszer típusától függően szippantás vagy iszapzsákcsere.'),
            p('Aki csak a berendezést választja ki, az a rendszernek <strong>egyharmadát</strong> '
              'tervezte meg.'),
        ),
    ])
    return szekcio('rendszer', 'Alapfogalom', 'Mi az a szennyvíztisztító rendszer?', torzs)


OSSZEHASONLITAS = [
    ('Mit csinál?', 'Csak gyűjt', 'Előkezel; a tisztítás nagy része a talajban',
     'Helyben megtisztítja a vizet'),
    ('Áram', 'Nem kell', 'Nem kell', 'Kell, a kompresszorhoz'),
    ('Rendszeres teendő', 'Szippantás évente többször',
     'Ürítés legalább kétévente, baktériumkészítmény-adagolás', 'Iszapzsákcsere, ellenőrzés'),
    ('Helyigény a víz elhelyezéséhez', 'Nincs (elszállítják)', 'Nagyobb tisztítómező',
     'Kisebb helyigény'),
    ('Használati ritmus', 'Bármilyen', 'Jól tűri a hosszabb szüneteket',
     'Rendszeres terhelést igényel'),
    ('Üzemeltetési költség', 'Évről évre nő a háztartás méretével és a díjakkal', 'Alacsony',
     'Kiszámítható, szippantás nélkül'),
]


def osszehasonlitas():
    sorok = NL.join(
        f'            <tr><th scope="row" class="type-ui-body-strong">{a}</th>'
        f'<td class="type-ui-body">{b}</td><td class="type-ui-body">{c}</td>'
        f'<td class="type-ui-body">{d}</td></tr>' for a, b, c, d in OSSZEHASONLITAS)
    torzs = NL.join([
        folyo(p('Három megoldástípus létezik, és a különbség nem fokozat kérdése.')),
        f'''      <div class="compare-scroll hub-tabla-keret" tabindex="0" role="region" aria-labelledby="osszehasonlitas-tabla-cim">
        <table class="compare-table compare-table-start hub-tabla">
          <caption class="type-ui-card-title" id="osszehasonlitas-tabla-cim">A három megoldástípus egymás mellett</caption>
          <thead>
            <tr><th scope="col"><span class="visually-hidden">Szempont</span></th>
            <th scope="col">Zárt szennyvíztároló</th>
            <th scope="col"><a href="oldomedences-rendszer">Oldómedencés rendszer</a></th>
            <th scope="col"><a href="biologiai-szennyviztisztitas">Biológiai szennyvíztisztító</a></th></tr>
          </thead>
          <tbody>
{sorok}
          </tbody>
        </table>
      </div>''',
        folyo(p('Ezután jön a telek: a '
                '<a href="../projekt-elokeszites/talaj-es-szivargokepesseg">talaj vízáteresztő '
                'képessége</a>, a <a href="../projekt-elokeszites/talajviz">talajvízszint</a>, a '
                '<a href="../projekt-elokeszites/lejtes-es-csomelyseg">lejtés</a> és a '
                '<a href="../projekt-elokeszites/telekmeret-es-szabad-terulet">szabad terület</a>. '
                'Ezek nem írják felül a technológiaválasztást, hanem azt határozzák meg, milyen '
                'műszaki kialakítással és milyen költséggel valósítható meg.')),
        tovabb('megoldastipusok-osszehasonlitasa', 'Megoldástípusok összehasonlítása — részletesen'),
        tovabb('melyik-megoldas-mikor-megfelelo', 'Melyik megoldás mikor megfelelő?'),
    ])
    return szekcio('megoldastipusok-osszehasonlitasa', 'Áttekintés', 'Megoldástípusok összehasonlítása',
                   torzs, alt=True)


KIZARO = [
    ('Nincs elég szabad terület a vízelhelyezésre.',
     'Ez a leggyakoribb valódi korlát. Ilyenkor nincs „kisebb helyigényű” szennyvíztisztító '
     'rendszer: ha nincs hova elhelyezni a kezelt vizet, a zárt tároló marad. Lásd a '
     '<a href="../projekt-elokeszites/telekmeret-es-szabad-terulet">szabad terület</a> lapot.'),
    ('Rendelkezésre álló közcsatorna.',
     'Ha van elérhető közcsatorna, főszabály szerint arra kell csatlakozni. Ha azonban a rákötés '
     'gazdaságtalan, és ezt gazdaságossági számítással igazolni lehet, felmentés kérhető a '
     'rákötési kötelezettség alól — lásd '
     '<a href="../helyzetem/kozcsatorna-vagy-egyedi-rendszer">Közcsatorna vagy egyedi rendszer</a>.'),
    ('Helyi szabályozás.',
     'A település helyi építési szabályzata korlátozhatja vagy kizárhatja az egyedi '
     'szennyvízkezelést, illetve a tisztított víz telken belüli elhelyezését.'),
    ('Vízvédelmi besorolás.',
     'Fokozottan érzékeny vagy vízbázisvédelmi területen a tisztított víz talajba juttatására '
     'további korlátozások vonatkozhatnak; a '
     '<a href="../projekt-elokeszites/kut-es-vedotavolsag">kút és a védőtávolság</a> is ide '
     'tartozik.'),
    ('Gyenge vagy hiányzó áramellátás.',
     'Aktív biológiai tisztításnál a kompresszor működéséhez folyamatos '
     'villamosenergia-ellátás kell.'),
]


def kizaro():
    torzs = NL.join([
        folyo(p('Öt dolog van, amelyik érdemben szűkíti a lehetőségeket. Egyik sem derül ki '
                'magától — mindet a megrendelés előtt érdemes tisztázni.')),
        kartyak(KIZARO),
        '''      <aside class="hub-elv" aria-label="Ami nem kizáró ok">
        <p class="type-ui-body-strong">A magas talajvíz, az agyagos talaj és a kedvezőtlen lejtés nem kizáró ok, csak kivitelezési feltétel: kiemelt szivárogtató, felúszás elleni rögzítés, külön megoldás a gravitációs továbbításra.</p>
      </aside>''',
        tovabb('kizaro-es-korlatozo-feltetelek', 'Kizáró és korlátozó feltételek — részletesen'),
        tovabb('../projekt-elokeszites/magas-talajvizi-helyzetek', 'Magas talajvízi helyzetek'),
    ])
    return szekcio('kizaro-es-korlatozo-feltetelek', 'Ami szűkít', 'Kizáró és korlátozó feltételek', torzs)


ELOSZURO = [
    ('Van műszakilag elérhető közcsatorna az ingatlant határoló közterületen?',
     'Ha igen, először ezt kell tisztázni, mert minden más erre épül.',
     '../helyzetem/nincs-elerheto-kozcsatorna', 'Nincs elérhető közcsatorna'),
    ('Az év hány hónapjában keletkezik szennyvíz az ingatlanon?',
     'Egész évben → biológiai irány. Néhány hónapban, vagy hosszú kihagyásokkal → az oldómedence '
     'is szóba jön.',
     '../projekt-elokeszites/szezonalis-hasznalat', 'Szezonális használat'),
    ('Hányan használják rendszeresen, és mennyi az éves vízfogyasztás?',
     'A vízszámla adata pontosabb minden becslésnél. A méretezési számításokban fejenként '
     '135 liter napi vízfelhasználással dolgozunk.',
     '../projekt-elokeszites/szemelyszam-es-vizfogyasztas', 'Személyszám és vízfogyasztás'),
    ('Mekkora összefüggő, beépítetlen terület áll rendelkezésre?',
     'Ez dönti el, elfér-e a tisztítómező — és ez a leggyakoribb korlát.',
     '../projekt-elokeszites/tisztitomezo', 'A tisztítómező helyigénye'),
    ('Milyen a talaj, és hol van a talajvíz?',
     'Ha nem tudja, az sem baj. A tervezett helyen a szivárogtatási próba ad közvetlen '
     'információt a talaj vízbefogadó képességéről.',
     '../projekt-elokeszites/szivarogtatasi-vizsgalat', 'Szivárogtatási vizsgálat'),
]


def eloszuro():
    elemek = NL.join(f'''        <li class="card hub-kerdes">
          <span class="card-badge type-data-value" aria-hidden="true">{i}</span>
          <h3 class="type-ui-card-title hub-kerdes-cim">{esc(k)}</h3>
          <p class="type-ui-body card-text">{v}</p>
          <p class="hub-kerdes-link"><a class="text-link" href="{h}"><span class="link-label">{f}<span class="action-arrow-end" aria-hidden="true">&rarr;</span></span></a></p>
        </li>''' for i, (k, v, h, f) in enumerate(ELOSZURO, 1))
    torzs = NL.join([
        folyo(p('Öt kérdés, és nagyjából megvan az irány. Érdemes leírni a válaszokat — ezek '
                'kellenek az ajánlathoz is.')),
        f'''      <ol class="numbered-grid hub-kerdesek" role="list">
{elemek}
      </ol>''',
        folyo(p('Ha mind az ötre tud válaszolni, helyszíni felmérés nélkül is tudunk konkrét '
                'javaslatot adni.')),
        tovabb('megoldastipus-eloszuro', 'Megoldástípus-előszűrő — az egész kérdéssor'),
        tovabb('../helyzetem/milyen-adatokat-kell-osszegyujteni', 'Milyen adatokat érdemes összegyűjteni?'),
    ])
    return szekcio('megoldastipus-eloszuro', 'Merre induljon', 'Megoldástípus-előszűrő', torzs, alt=True)


def tervezni():
    torzs = NL.join([
        folyo(
            p('Két olyan elem van, amit a legtöbben csak a kivitelezésnél vesznek észre.'),
            p('<strong>A tisztítómező.</strong> A tisztított víz mennyisége megegyezik a keletkező '
              'szennyvíz mennyiségével — a tisztítás nem tünteti el a vizet, csak megtisztítja. A '
              'szükséges felület a napi vízmennyiségtől, a talaj vízáteresztő képességétől és a '
              'talajvízszinttől függ, ezért általános négyzetméterszám felelősen nem adható meg.'),
            p('<strong>Az üzemeltetés.</strong> Az <a href="ab-clear">A.B. Clear</a> '
              'berendezéseknél a fölösiszap az iszapzsákba kerül, ezért normál üzemeltetés mellett '
              'rendszeres szippantásra nincs szükség. A rendszer állapotát ugyanakkor érdemes '
              'rendszeresen ellenőrizni: a 147/2010. (IV.&nbsp;29.) Korm. rendelet a tulajdonosra '
              'ellenőrzési, karbantartási és dokumentálási kötelezettséget ró.'),
            p('A két elem összefügg: rosszul működő berendezés esetén a tisztítómező fizeti meg a '
              'számlát, és annak javítása lényegesen drágább.'),
        ),
        '      <div class="hub-foto-sor">',
        foto('szivarogtatas-arok', 'Kiásott, egyenes falú árok a kertben, a szivárogtató számára.',
             'A szivárogtató árka — a tisztítómező ezt a szabad területet igényli.'),
        foto('szivarogtatas-alagut', 'Fekete, bordázott szivárogtató alagútelemek a kavicságyon, narancs csővezetékkel.',
             'Szivárogtató alagútelemek a kavicságyon, a bekötéssel.'),
        foto('szivarogtatas-elkeszult', 'Visszatemetett, elkészült szivárogtató a gyepes kertben.',
             'A kész állapot: a felszínen már semmi nem látszik belőle.'),
        '      </div>',
        tovabb('../projekt-elokeszites/tisztitomezo', 'A tisztítómező méretezése'),
        tovabb('../tudastar/uzemeltetes-teendok-es-koltsegek', 'Üzemeltetés: teendők és költségek'),
    ])
    return szekcio('tisztitomezo-es-uzemeltetes', 'Amit sokan kihagynak',
                   'Amit a berendezésen kívül még tervezni kell', torzs)


VITUKI = [('KOI<sub>Cr</sub>', '55'), ('BOI<sub>5</sub>', '15'), ('Lebegőanyag', '18'),
          ('N-NH<sub>4</sub>', '9'), ('Összes nitrogén', '20'), ('Összes foszfor', '5')]

BIZALOM = [
    ('2004 óta', 'foglalkozunk biológiai szennyvíztisztítással; a berendezéseket Esztergomban gyártjuk.'),
    ('3&nbsp;800+', 'megvalósított rendszer országszerte.'),
    ('EP 2766313', 'európai szabadalom az A.B. Clear műszaki megoldására.'),
    ('EN 12566-3 · CE-jelölés', 'a gyártás ISO 9001 minőségirányítási rendszerben folyik.'),
]


def miert_mi():
    sorok = NL.join(f'            <tr><th scope="row" class="type-ui-body">{a}</th>'
                    f'<td class="type-data-value hub-ertek">{b}&nbsp;mg/l</td></tr>' for a, b in VITUKI)
    bizalom = NL.join(f'''        <li class="trust-item">
          <p class="type-ui-card-title trust-title trust-title-data">{a}</p>
          <p class="type-ui-subtitle trust-text">{b}</p>
        </li>''' for a, b in BIZALOM)
    torzs = NL.join([
        folyo(
            p('Az ÖkoTech-Home Kft. 2004 óta foglalkozik biológiai szennyvíztisztítással; saját '
              'fejlesztésű A.B. Clear berendezéseit Esztergomban gyártja, és eddig több mint '
              '3800 rendszert valósított meg országszerte.'),
            p('Az A.B. Clearben alkalmazott műszaki megoldás saját fejlesztésünk, amelyre '
              'nemzetközi szabadalmi eljárást követően <strong>európai szabadalmat</strong> '
              'szereztünk (EP&nbsp;2766313). A berendezések <strong>CE-jelöléssel</strong> '
              'rendelkeznek az EN&nbsp;12566-3 szabvány szerint, a gyártás '
              '<strong>ISO&nbsp;9001</strong> minőségirányítási rendszerben folyik.'),
        ),
        f'''      <ul class="trust-grid hub-bizalom" role="list">
{bizalom}
      </ul>''',
        folyo(p('Mért adataink a <strong>VITUKI</strong> vizsgálati zárójegyzőkönyvéből:')),
        f'''      <div class="compare-scroll hub-adat-keret" tabindex="0" role="region" aria-labelledby="vituki-cim">
        <table class="compare-table compare-table-start hub-adat-tabla">
          <caption class="visually-hidden" id="vituki-cim">A VITUKI által mért kibocsátási értékek</caption>
          <thead><tr><th scope="col">Paraméter</th><th scope="col">Mért érték</th></tr></thead>
          <tbody>
{sorok}
          </tbody>
        </table>
      </div>''',
        folyo(p('Egy konkrét projekt kibocsátási megfelelőségét viszont mindig az adott befogadó és '
                'az alkalmazandó határértékek alapján kell megítélni.')),
        tovabb('ab-clear-muszaki-adatok', 'Az A.B. Clear műszaki adatai'),
        tovabb('../eredmenyek/esettanulmanyok', 'Megvalósult projektek'),
    ])
    return szekcio('miert-mi', 'Rólunk', 'Miért érdemes minket választani?', torzs, alt=True)


GYIK = [
    ('Mi az a szennyvíztisztító rendszer?',
     'A szennyvíztisztító rendszer három részből áll: a szennyvizet kezelő műtárgyból, a '
     'megtisztított víz elhelyezéséből és az üzemeltetésből. A kezelést zárt tároló, oldómedence '
     'vagy aktív biológiai szennyvíztisztító végezheti.'),
    ('Melyik szennyvíztisztító rendszer a legjobb?',
     'Nincs egyetlen legjobb, mert a választást a használat jellege dönti el. Egész évben lakott '
     'háznál az aktív biológiai tisztítás az elsődleges irány; erősen szezonális használatnál az '
     'oldómedencés rendszer is szóba jön.'),
    ('Mennyibe kerül egy szennyvíztisztító rendszer?',
     'A végösszeget nem a tartály ára dönti el, hanem a kapacitás, a tisztítómező mérete, a '
     'földmunka és a telek adottságai. Ezért ugyanaz a berendezés két szomszédos telken is eltérő '
     'beruházási költséget jelenthet.'),
    ('Mekkora a legkisebb berendezés?',
     'Az A.B. Clear termékcsalád legkisebb szabványos berendezése 6 lakosegyenérték névleges '
     'kapacitású, és ennél kisebb szabványos berendezés nincs a termékcsaládban. A termékcsalád '
     '50 lakosegyenértékig kínál megoldást.'),
    ('Milyen hatósági eljárás szükséges?',
     'Ez attól függ, milyen berendezést telepítenek, hogyan történik a tisztított víz elhelyezése, '
     'és milyenek a helyszín adottságai. A CE-jelöléssel rendelkező berendezésekre és a tisztított '
     'víz elszivárogtatására nem azonos szabályok vonatkoznak, ezért az alkalmazandó eljárást az '
     'adott projekt alapján tisztázzuk.'),
    ('Mi a legfontosabb, amit előre tisztázni kell?',
     'Az, hogy hova kerül a megtisztított víz. A legtöbb terv nem a berendezésen, hanem a '
     'tisztítómező helyigényén akad el.'),
]


def gyik():
    elemek = NL.join(f'''          <details class="faq-item">
            <summary class="faq-q type-ui-card-title">{k}</summary>
            <div class="faq-a"><p class="type-ui-body">{v}</p></div>
          </details>''' for k, v in GYIK)
    return szekcio('gyik', 'Gyakori kérdések', 'Gyakori kérdések', f'''      <div class="faq">
{elemek}
      </div>''')


def cta():
    return '''
  <section class="section" aria-labelledby="ingatlan-cta-cim">
    <div class="section-inner">
      <aside class="panel-dark" aria-labelledby="ingatlan-cta-cim">
        <div class="panel-dark-head">
          <p class="type-data-eyebrow panel-dark-eyebrow">Következő lépés</p>
          <h2 class="type-display-highlight-title panel-dark-title" id="ingatlan-cta-cim">Nézzük meg, az Ön ingatlanára mi való</h2>
        </div>
        <div class="panel-dark-body">
          <p class="type-ui-body panel-dark-text">Nem kell helyszíni felmérés, és nem jár elköteleződéssel. Elég a telek helye, a rendszeresen jelen lévő létszám, és annyi, amennyit a talajról, a talajvízről és a szabad területről tud.</p>
          <p class="panel-dark-actions"><a class="btn btn-inverse" href="../ajanlat#urlap">Kérem a személyre szabott javaslatot</a></p>
          <p class="type-ui-body panel-dark-text">Ha inkább telefonon beszélne, hívjon minket: <a href="tel:+3633200211">+36 33 200 211</a>.</p>
        </div>
      </aside>
    </div>
  </section>'''


def szerzo():
    return f'''
  <section class="section" aria-labelledby="szerzo-cim">
    <div class="section-inner">
      <aside class="hub-szerzo" aria-labelledby="szerzo-cim">
        <h2 class="type-ui-card-title" id="szerzo-cim">Az oldalról</h2>
        <p class="type-ui-body">Az oldalt az <strong>ÖkoTech-Home Kft.</strong> szakmai csapata állította össze. A vállalkozás 2004 óta foglalkozik biológiai szennyvíztisztítással, saját A.B. Clear berendezéseit Esztergomban gyártja, és eddig több mint 3800 rendszert valósított meg országszerte.</p>
        <p class="type-ui-caption hub-szerzo-datum">Utolsó szakmai frissítés: <time datetime="{FRISSITVE[1]}">{FRISSITVE[2]}</time></p>
      </aside>
    </div>
  </section>'''


def jsonld():
    szervezet = {'@type': 'Organization', 'name': 'ÖkoTech-Home Kft.', 'url': f'{DOMAIN}/'}
    graf = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'Article',
                'headline': H1,
                'description': LEIRAS,
                'inLanguage': 'hu-HU',
                'image': f'{DOMAIN}/assets/img/oldalak/hero-attekintes.webp?v=3',
                'dateModified': FRISSITVE[0],
                'about': [{'@type': 'Thing', 'name': 'szennyvíztisztító rendszer',
                           'alternateName': ['házi szennyvíztisztító rendszer', 'szikkasztó rendszer',
                                             'bio szennyvíztisztító rendszer',
                                             'egyedi szennyvízkezelés']}],
                'author': szervezet, 'publisher': szervezet,
                'mainEntityOfPage': f'{DOMAIN}/{UT}',
            },
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Főoldal', 'item': f'{DOMAIN}/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Megoldások', 'item': f'{DOMAIN}/{UT}'},
            ]},
            {'@type': 'FAQPage', 'mainEntity': [
                {'@type': 'Question', 'name': szoveg(k),
                 'acceptedAnswer': {'@type': 'Answer', 'text': szoveg(v)}} for k, v in GYIK]},
        ],
    }
    return ('<script type="application/ld+json">' + NL
            + json.dumps(graf, ensure_ascii=False, indent=2) + NL + '</script>')


def epit(t):
    kep = re.search(r'    <figure class="hero-media page-hero-media">.*?</figure>', t, re.S).group(0)
    fo = f'''<main id="fotartalom">

  <section class="hero page-hero" aria-labelledby="oldal-cim">
    <div class="hero-inner">
      <div class="hero-copy">
        <nav class="breadcrumb" aria-label="Morzsamenü">
          <ol class="breadcrumb-list type-ui-caption" role="list">
            <li><a href="../">Főoldal</a></li>
            <li aria-current="page">Megoldások</li>
          </ol>
        </nav>
        <h1 class="type-display-page-title hero-title" id="oldal-cim">{esc(H1)}</h1>
        <p class="type-ui-body-strong hero-lead">{esc(LEAD)}</p>
      </div>
    </div>
{kep}
  </section>
{bevezeto()}
{rendszer()}
{osszehasonlitas()}
{kizaro()}
{eloszuro()}
{tervezni()}
{miert_mi()}
{gyik()}
{cta()}
{szerzo()}
</main>'''
    u = re.sub(r'<main id="fotartalom">.*?</main>', lambda _: fo, t, count=1, flags=re.S)
    cserek = [
        (r'<title>.*?</title>', f'<title>{esc(CIM)}</title>'),
        (r'<meta name="description" content="[^"]*">',
         f'<meta name="description" content="{_html.escape(LEIRAS)}">'),
        (r'<meta property="og:title" content="[^"]*">',
         f'<meta property="og:title" content="{_html.escape(CIM)}">'),
        (r'<meta property="og:description" content="[^"]*">',
         f'<meta property="og:description" content="{_html.escape(LEIRAS)}">'),
    ]
    for minta, uj in cserek:
        u, n = re.subn(minta, lambda _: uj, u, count=1)
        assert n == 1, minta
    u, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda _: jsonld(), u,
                   count=1, flags=re.S)
    assert n == 1
    return u


def main():
    t = LAP.read_text(encoding='utf-8')
    u = epit(t)
    LAP.write_text(u, encoding='utf-8')
    szavak = len(re.sub(r'<[^>]+>', ' ', re.search(r'<main.*?</main>', u, re.S).group(0)).split())
    print(f'{LAP.relative_to(GYOKER)}: {len(u) // 1024} KB, ~{szavak} szó a <main>-ben')


if __name__ == '__main__':
    main()
