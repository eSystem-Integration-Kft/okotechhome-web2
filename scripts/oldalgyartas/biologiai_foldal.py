#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""biologiai_foldal.py — Megoldások → Biológiai szennyvíztisztítás (a hub lapja).

MIÉRT ÚJ GENERÁTOR. A lap 2026-09-16-án új szöveget kapott Belától, SEO-
blokkal együtt: fókusz a „biológiai szennyvíztisztító", másodlagosan a
„bio emésztő" (és a „bio emésztő tartály", „… ár" változatok). A korábbi
szöveg a `biologiai_hub.py`-ból jött; azóta a kiadott HTML-t többször kézzel
is javítottuk, így annak újrafuttatása mindkettőt felülírná. Ez a generátor
csak a `<main>`-t, a fej címét/leírását/OG-sorait és a JSON-LD-t cseréli —
a fejléc, a lábléc és minden szkript a kiadott lapból marad.

A SZÖVEG BELÁÉ, nem az enyém. Négy ponton a webhely saját forrásaihoz
igazítva (2026-09-16, tételes ellenőrzés után):
  1. „2 év jótállás" → kimaradt a szám. Az ÁSZF 1 évet, a megrendelő 2 évet
     ír, és a 151/2003. Korm. rendelet 2026. márciusi módosítása óta
     250 000 Ft fölött 3 év a kötelező — lásd
     `_files/jogi-hivatkozas-ellenorzes-2026-09-14.md`, A pont.
  2. „2004 óta gyártja az A.B. Clear-t" → a cég 2004 óta foglalkozik a
     területtel; a saját berendezés fejlesztése a cégtörténet szerint 2010-ben
     indult (`okotech-home/tortenetunk`).
  3. „gyökérzónás öntözés" → „gyökérzónás elhelyezés": a webhely szabálya
     szerint ez elhelyezés, nem öntözés (`projekt-elokeszites/gyokerzonas-elhelyezes`).
  4. „CE-tanúsítás" → „CE-jelölés", ahogy a fogalomtár és a többi lap mondja.
  +  „több mint 3800 rendszer működik" → „valósítottunk meg", a főoldallal
     egyezően (a működő rendszerek száma nincs dokumentálva).

AZ ÁR. Az ágon termék- és projektár nem jelenik meg (`biologiai_hub.py`).
Az üzemeltetési példaszámítás más: 2026-09-10-én döntés alapján került ki,
és ugyanezek a számok a főoldalon is állnak.

FUTTATÁS:  python3 scripts/oldalgyartas/biologiai_foldal.py
"""
import html as _html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import biologiai_abra as abra  # noqa: E402

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
DOMAIN = 'https://okotechhome.hu'
UT = 'megoldasok/biologiai-szennyviztisztitas'
LAP = WEB / f'{UT}.html'
FRISSITVE = ('2026-09-17', '2026-09', '2026. szeptember')

CIM = 'Biológiai szennyvíztisztító (bio emésztő) — hogyan működik?'
LEIRAS = ('Hogyan működik a biológiai szennyvíztisztító, amit sokan bio emésztőnek hívnak? '
          'Működés, mért értékek, üzemeltetési költség és telepítési feltételek.')
H1 = 'Biológiai szennyvíztisztító: hogyan működik, és Önnek való-e?'
LEAD = ('A biológiai szennyvíztisztító olyan berendezés, amely élő mikroorganizmusok '
        'segítségével bontja le a háztartási szennyvíz szennyezőanyagait. A köznyelvben '
        'sokan bio emésztőnek vagy ökoemésztőnek nevezik — a berendezés viszont nem tárolja '
        'a szennyvizet, hanem megtisztítja.')

NL = chr(10)


def esc(s):
    return _html.escape(str(s), quote=False)


def szoveg(s):
    """HTML-ből sima szöveg a JSON-LD-hez."""
    return _html.unescape(re.sub(r'<[^>]+>', '', s)).replace(' ', ' ')


def p(s, osztaly='type-ui-body'):
    return f'        <p class="{osztaly}">{s}</p>'


def tovabb(href, felirat):
    return (f'        <p class="bio-tovabb"><a class="text-link" href="{href}"><span class="link-label">'
            f'{felirat}<span class="action-arrow-end" aria-hidden="true">&rarr;</span></span></a></p>')


def szekcio(azon, eyebrow, cim, torzs, alt=False):
    hatter = ' section-alt' if alt else ''
    return f'''
  <section class="section{hatter}" id="{azon}" aria-labelledby="{azon}-cim">
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


def foto(kep, szel, mag, alt, felirat, osztaly='bio-foto'):
    return f'''      <figure class="{osztaly}">
        <img src="../assets/img/galeria/{kep}.webp?v=1" width="{szel}" height="{mag}"
             alt="{_html.escape(alt, quote=True)}" loading="lazy" decoding="async">
        <figcaption class="type-ui-caption bio-foto-felirat">{felirat}</figcaption>
      </figure>'''


# ================================================================ TARTALOM
TARTALOM = [
    ('hogyan-mukodik', 'Hogyan működik?'),
    ('bio-emeszto', 'Bio emésztő, ökoemésztő'),
    ('mert-adatok', 'Mérhető adatok'),
    ('kinek-valo', 'Kinek megfelelő?'),
    ('uzemeltetes-koltseg', 'Üzemeltetés és költség'),
    ('telek-feltetelek', 'Telek- és terhelési feltételek'),
    ('mikor-mast', 'Mikor javasolunk mást?'),
    ('telepitesek', 'Megvalósult telepítések'),
    ('gyik', 'Gyakori kérdések'),
]


def bevezeto():
    linkek = NL.join(f'            <li><a class="bio-tartalom-link" href="#{a}">{esc(c)}</a></li>'
                     for a, c in TARTALOM)
    return f'''
  <section class="section" aria-labelledby="lenyeg-cim">
    <div class="section-inner bio-bevezeto">
      <div class="bio-bevezeto-szoveg">
        <p class="type-ui-body-strong">Ez a különbség dönt el minden mást: nincs szippantás, a megtisztított víz pedig a telken belül hasznosul.</p>
        <p class="type-ui-body">Ezen az oldalon végigmegyünk azon, hogyan működik a rendszer, kinek való, mit kell tudni az üzemeltetéséről, és mennyibe kerül fenntartani egy évben. A végén azt is megmondjuk, mikor javasolunk inkább mást.</p>
        <nav class="bio-tartalom" aria-label="Az oldal tartalma">
          <p class="type-data-eyebrow bio-tartalom-cim">Az oldalon</p>
          <ol class="bio-tartalom-lista" role="list">
{linkek}
          </ol>
        </nav>
      </div>
      <aside class="bio-lenyeg" aria-labelledby="lenyeg-cim">
        <h2 class="type-display-highlight-title bio-lenyeg-cim" id="lenyeg-cim">A lényeg röviden</h2>
        <p class="type-ui-body">A tisztítást élő mikroorganizmusok végzik, a szükséges oxigénellátást pedig kompresszor biztosítja. Mivel a keletkező fölösiszap iszapzsákba kerül, rendszeres szippantásra nincs szükség.</p>
        <dl class="bio-kulcsadatok">
          <div class="bio-kulcsadat"><dt class="type-ui-caption">Legkisebb szabványos berendezés</dt><dd class="type-data-value">6&nbsp;LE</dd></div>
          <div class="bio-kulcsadat"><dt class="type-ui-caption">A termékcsalád felső határa</dt><dd class="type-data-value">50&nbsp;LE</dd></div>
          <div class="bio-kulcsadat"><dt class="type-ui-caption">Teljes üzemeltetés évente</dt><dd class="type-data-value">22&nbsp;700–27&nbsp;500&nbsp;Ft</dd></div>
          <div class="bio-kulcsadat"><dt class="type-ui-caption">Rendszeres szippantás</dt><dd class="type-data-value">nincs</dd></div>
        </dl>
        <p class="type-ui-caption bio-lenyeg-jegyzet">Az A.B. Clear adatai. Az üzemeltetési költség árammal, iszapzsákkal és évesített membráncserével együtt értendő; <abbr title="lakosegyenérték">LE</abbr> = <a href="../tudastar/fogalomtar#f-lakosegyenertek-le">lakosegyenérték</a>.</p>
      </aside>
    </div>
  </section>'''


def mukodes():
    torzs = NL.join([
        abra.folyamat_abra('folyamat-abra-cim'),
        folyo(
            p('Egy biológiai szennyvíztisztító belsejében élő baktériumkultúra dolgozik. Ezek a '
              'mikroorganizmusok bontják le és alakítják át a szennyvíz szennyezőanyagait; a '
              'berendezés feladata pedig az, hogy biztosítsa ehhez a megfelelő körülményeket — '
              'mindenekelőtt az oxigénellátást, amelyet kompresszor ad.'),
            p('Ez az alapvető különbség a tárolós megoldásokhoz képest. Egy emésztő vagy zárt '
              'tároló összegyűjti a szennyvizet, és ami belekerül, azt előbb-utóbb el kell '
              'szállíttatni. A biológiai szennyvíztisztító ezzel szemben elvégzi a munkát a '
              'helyszínen.'),
            p('A folyamat során fölösiszap keletkezik. Ez iszapzsákba kerül, ahol tovább '
              'víztelenedik és szárad — négy fő szennyvize mellett ez nagyjából évi '
              '0,5&nbsp;köbméter iszapot jelent. Éppen ezért nincs szükség rendszeres szippantásra.'),
            p('A megtisztított víz pedig megfelelő kialakítás és az adott ingatlanra vonatkozó '
              'feltételek mellett a telken belül marad, és '
              '<a href="../projekt-elokeszites/gyokerzonas-elhelyezes">gyökérzónás elhelyezéssel</a> '
              'hasznosul.'),
        ),
        '      <div class="bio-foto-par">',
        foto('berendezes-kompresszor', 1200, 800,
             'Kék burkolatú membrános légszivattyú, a berendezés kompresszora.',
             'A membrános légszivattyú adja az oxigént — a rendszer egyetlen mozgó alkatrésze.'),
        foto('iszapkezeles-zsak_kosarban', 1200, 800,
             'Fehér szűrőzsák a perforált kosárban, benne sötét, víztelenedett iszap.',
             'A szűrőzsák a kosárban, a kiemelés pillanatában — a fölösiszap itt gyűlik össze.'),
        '      </div>',
        tovabb('biologiai-hogyan-mukodik', 'Lépésről lépésre: mi történik a tartályban'),
    ])
    return szekcio('hogyan-mukodik', 'Működés', 'Hogyan működik a biológiai szennyvíztisztító?', torzs)


def bio_emeszto():
    sorok = [
        ('Mit csinál a szennyvízzel?', 'Helyben megtisztítja', 'Előkezeli', 'Csak gyűjti'),
        ('Hol történik a tisztítás?', 'Túlnyomórészt a berendezésben',
         'Nagy része a talajban folytatódik', 'Sehol — nem tisztít'),
        ('Mi lesz a szennyvízzel?', 'Kezelt vízként a telken marad',
         'Előkezelten a talajba jut, ott tisztul tovább', 'Rendszeres szippantással elszállítják'),
    ]
    tabla_sorok = NL.join(
        f'            <tr><th scope="row" class="type-ui-body-strong">{a}</th>'
        f'<td class="type-ui-body">{b}</td><td class="type-ui-body">{c}</td><td class="type-ui-body">{d}</td></tr>'
        for a, b, c, d in sorok)
    torzs = NL.join([
        folyo(
            p('A bio emésztő nem szabványos szakkifejezés, hanem a kereskedelmi és a köznyelvi '
              'szóhasználatból jött. Aki erre keres, jellemzően olyan megoldást szeretne, amely a '
              'szennyvizet nem csak gyűjti, hanem helyben meg is tisztítja — vagyis a gyakorlatban '
              'éppen azt, amit ezen az oldalon bemutatunk.'),
            p('Érdemes viszont tudni, hogy a bio emésztő tartály megnevezést a piacon többféle '
              'termékre használják. Előfordul, hogy egy egyszerű oldómedencét, máskor egy pusztán '
              'gyűjtésre szolgáló tartályt hirdetnek így. A kettő között pedig lényeges különbség '
              'van: az aktív biológiai tisztításból már kezelt víz távozik, az oldómedence után '
              'viszont a tisztítás nagy része a talajban folytatódik.'),
        ),
        f'''      <div class="compare-scroll" tabindex="0" role="region" aria-labelledby="bio-emeszto-tabla-cim">
        <table class="compare-table compare-table-start bio-tabla">
          <caption class="type-ui-card-title" id="bio-emeszto-tabla-cim">Mit takarhat a „bio emésztő” név?</caption>
          <thead>
            <tr><th scope="col"><span class="visually-hidden">Kérdés</span></th><th scope="col">Aktív biológiai szennyvíztisztító</th><th scope="col">Oldómedence</th><th scope="col">Gyűjtő (zárt) tartály</th></tr>
          </thead>
          <tbody>
{tabla_sorok}
          </tbody>
        </table>
      </div>''',
        '''      <aside class="panel bio-kerdes-panel" aria-labelledby="bio-kerdesek-cim">
        <h3 class="type-ui-card-title" id="bio-kerdesek-cim">Ajánlatkérésnél ezt kérdezze meg</h3>
        <ul class="fit-list" role="list">
          <li class="type-ui-body"><span class="fit-mark fit-yes" aria-hidden="true"></span><span class="fit-text">Rendelkezik-e a berendezés <strong>EN&nbsp;12566-3</strong> szabvány szerinti <strong>CE-jelöléssel</strong>?</span></li>
          <li class="type-ui-body"><span class="fit-mark fit-yes" aria-hidden="true"></span><span class="fit-text">Van-e <strong>mért adat</strong> a kibocsátásáról?</span></li>
        </ul>
      </aside>''',
        folyo(p('Ha a bio emésztő kifejezés mögötti fogalmakban szeretne előbb rendet tenni, azt '
                '<a href="../tudastar/bioemeszto-okoemeszto-hazi-szennyviztisztito">külön oldalunkon</a> '
                'tettük meg.')),
    ])
    return szekcio('bio-emeszto', 'Elnevezések',
                   'Bio emésztő, ökoemésztő — ugyanaz, mint a biológiai szennyvíztisztító?', torzs, alt=True)


def mert_adatok():
    ertekek = [
        ('<a href="../tudastar/fogalomtar#f-koi">KOI</a><sub>Cr</sub>', '55'),
        ('<a href="../tudastar/fogalomtar#f-boi">BOI</a><sub>5</sub>', '15'),
        ('Lebegőanyag', '18'),
        ('N-NH<sub>4</sub>', '9'),
        ('Összes nitrogén', '20'),
        ('Összes foszfor', '5'),
    ]
    sorok = NL.join(f'            <tr><th scope="row" class="type-ui-body">{a}</th>'
                    f'<td class="type-data-value bio-ertek">{b}&nbsp;mg/l</td></tr>' for a, b in ertekek)
    bizalom = [
        ('EN 12566-3 · CE-jelölés', 'A berendezések az európai kisberendezés-szabvány szerint CE-jelölést viselnek.'),
        ('ISO 9001', 'A gyártás ISO 9001 minőségirányítási rendszerben folyik.'),
        ('15 év', 'Garancia az általunk kiszállított és szakszerűen telepített tartály stabilitására.'),
        ('VITUKI', 'A fenti kibocsátási értékek a VITUKI vizsgálati zárójegyzőkönyvéből.'),
    ]
    bizalom_html = NL.join(
        f'''        <li class="trust-item">
          <p class="type-ui-card-title trust-title trust-title-data">{a}</p>
          <p class="type-ui-subtitle trust-text">{b}</p>
        </li>''' for a, b in bizalom)
    torzs = NL.join([
        folyo(p('Az ÖkoTech-Home Kft. A.B. Clear berendezéseinek mért kibocsátási értékei a '
                '<strong>VITUKI</strong> vizsgálati zárójegyzőkönyve szerint:')),
        f'''      <div class="compare-scroll bio-adat-keret" tabindex="0" role="region" aria-labelledby="vituki-cim">
        <table class="compare-table compare-table-start bio-adat-tabla">
          <caption class="visually-hidden" id="vituki-cim">A VITUKI által mért kibocsátási értékek</caption>
          <thead><tr><th scope="col">Paraméter</th><th scope="col">Mért érték</th></tr></thead>
          <tbody>
{sorok}
          </tbody>
        </table>
      </div>''',
        folyo(
            p('Ezek a VITUKI vizsgálati eredményei. Egy konkrét projekt kibocsátási megfelelőségét '
              'viszont mindig az adott befogadó, az alkalmazandó határértékek és a hatósági '
              'előírások alapján kell megítélni.'),
            p('A berendezések <strong>CE-jelöléssel</strong> rendelkeznek az EN&nbsp;12566-3 szabvány '
              'szerint, a gyártás pedig <strong>ISO&nbsp;9001</strong> minőségirányítási rendszerben '
              'folyik. A berendezésre a mindenkor hatályos jogszabályok szerinti jótállás vonatkozik; '
              'az általunk kiszállított és szakszerűen telepített tartály stabilitására '
              '<strong>15&nbsp;év</strong> garanciát vállalunk.'),
        ),
        f'''      <ul class="trust-grid bio-bizalom" role="list">
{bizalom_html}
      </ul>''',
        tovabb('ab-clear-muszaki-adatok', 'Az A.B. Clear műszaki adatai'),
        tovabb('../eredmenyek/tanusitvanyok-es-dokumentumok', 'Tanúsítványok és dokumentumok'),
    ])
    return szekcio('mert-adatok', 'Bizonyíték', 'Mit ad a rendszer? Mérhető adatok', torzs)


def kinek():
    feltetelek = [
        ('Rendszeres terhelés.', 'A baktériumkultúra a beérkező szennyvízből él, ezért folyamatos '
         'utánpótlásra van szüksége. Egy egész évben, életvitelszerűen lakott háznál ez adott.'),
        ('Van hova elhelyezni a tisztított vizet.', 'A szivárogtatóhoz vagy a gyökérzónás '
         'elhelyezéshez szabad terület kell a telken.'),
        ('Folyamatos villamosenergia-ellátás biztosított.', 'Az oxigénellátáshoz szükséges '
         'kompresszor működéséhez erre szükség van.'),
        ('A terhelés 50 lakosegyenérték alatt van.', 'Az A.B. Clear legkisebb szabványos '
         'berendezése 6 lakosegyenérték névleges kapacitású, a termékcsalád pedig 50 '
         'lakosegyenértékig kínál megoldást. E fölött egyedileg méretezett szennyvíztisztító '
         'telepet tervezünk.'),
    ]
    kartyak = NL.join(f'''        <li class="card">
          <span class="card-badge type-data-value" aria-hidden="true">{i:02d}</span>
          <p class="type-ui-body card-text"><strong>{a}</strong> {b}</p>
        </li>''' for i, (a, b) in enumerate(feltetelek, 1))
    helyek = ['családi házak', 'tanyák', 'vadászházak', 'irodák', 'társasházak',
              'házcsoportok közös szennyvíztisztítása']
    cimkek = ''.join(f'<li class="card-tag type-ui-caption">{h}</li>' for h in helyek)
    torzs = NL.join([
        folyo(p('Négy feltétel teljesülése esetén ez a legjobb választás, és a négy közül a '
                'legfontosabb az első.')),
        f'''      <ol class="numbered-grid bio-feltetelek" role="list">
{kartyak}
      </ol>''',
        folyo(p('Ha ez a négy adott, akkor jellemzően családi házaknál, tanyákon, vadászházaknál, '
                'irodáknál, társasházaknál, sőt házcsoportok közös szennyvíztisztításánál is ez a '
                'megoldás jön szóba.')),
        f'      <ul class="bio-cimkek" role="list" aria-label="Jellemző felhasználási helyek">{cimkek}</ul>',
        folyo(p('A legtöbben azért választják, mert <strong>megszűnik a szippantás</strong>. A '
                'második ok pedig rendszerint az, hogy a szennyvíz nem áll heteken át a tartályban '
                'az elszállításig.')),
        foto('kesz_kertek-gyep', 1200, 800,
             'Nyírt gyep, kavicsos szárazpatak és sziklaágyás egy kertben; a gyepen egyetlen kerek fedlap látszik.',
             'Egy működő rendszer fölött: nyírt gyep, kavicsos szárazpatak, sziklaágyás — és egyetlen fedlap.',
             'bio-foto bio-foto-szeles'),
        tovabb('biologiai-kinek-megfelelo', 'Kinek megfelelő — részletesen'),
    ])
    return szekcio('kinek-valo', 'Alkalmasság', 'Kinek megfelelő a biológiai szennyvíztisztító?',
                   torzs, alt=True)


def uzemeltetes():
    tetelek = [
        ('Villamos energia folyamatos üzemben', 'kb. 15&nbsp;800&nbsp;Ft/év'),
        ('Villamos energia 7/3 perces üzemmódban', 'kb. 11&nbsp;000&nbsp;Ft/év'),
        ('Iszapzsákok éves költsége', 'legfeljebb kb. 1&nbsp;200&nbsp;Ft/év'),
        ('Membráncsere 3–4 évente, évesítve', 'kb. 10&nbsp;500&nbsp;Ft/év'),
    ]
    lista = NL.join(f'          <div class="bio-tetel"><dt class="type-ui-body">{a}</dt>'
                    f'<dd class="type-data-value">{b}</dd></div>' for a, b in tetelek)
    torzs = NL.join([
        folyo(
            p('Egy biológiai szennyvíztisztító üzemeltetése tételesen kiszámolható, és itt jön ki '
              'az igazi különbség a tárolós megoldásokhoz képest.'),
            p('A berendezés oxigénellátását <strong>50&nbsp;watt</strong> teljesítményű kompresszor '
              'biztosítja. Megszakítás nélküli üzemben ez <strong>438&nbsp;kWh</strong> évente. '
              'Megfelelő terhelés mellett sok rendszer 7 perc működés és 3 perc szünet '
              'váltakozásával üzemel. Ilyenkor a kompresszor az idő 70&nbsp;százalékában jár, ami '
              'körülbelül <strong>307&nbsp;kWh</strong> évente. A szakaszos üzem nem minden '
              'üzemállapotban alkalmazható — a folyamatos működés is teljesen normális, a '
              'beállítást a rendszer terhelése és üzemi állapota határozza meg.'),
        ),
        abra.utem_abra('utem-abra-cim'),
        f'''      <div class="bio-szamitas">
        <h3 class="type-ui-card-title">Példaszámítás 36&nbsp;Ft/kWh lakossági áramárral</h3>
        <dl class="bio-tetelek">
{lista}
        </dl>
      </div>''',
        abra.koltseg_abra('koltseg-abra-cim'),
        folyo(
            p('A teljes üzemeltetés — árammal, iszapzsákkal és évesített membráncserével együtt — '
              'így nagyjából <strong>22&nbsp;700–27&nbsp;500&nbsp;forint</strong> évente. Ebből maga '
              'az áramköltség üzemmódtól függően körülbelül 1000–1500&nbsp;forint havonta. Ehhez '
              'érdemes hozzátenni, hogy szippantásra ebben az összegben nincs szükség — miközben '
              'egy zárt tárolónál gyakran ennyibe kerül egyetlen ürítés. A forintösszegek '
              'példaszámítások, a tényleges villamosenergia-költség az Ön tarifájától függ.'),
            p('Külön, választható szolgáltatásként <strong>negyedéves karbantartási szerződés</strong> '
              'köthető; ennek díja a fenti összegben nincs benne. Az értéke nem pusztán az évi négy '
              'ellenőrzés: a rendszeres felülvizsgálaton időben észrevehetők azok az eltérések, '
              'amelyek beavatkozás nélkül később a biológiai működést is befolyásolnák.'),
            p('A beruházás oldalán a berendezés ára mellett a földmunka, a szivárogtató '
              'kialakítása, az elektromos bekötés és az engedélyeztetés jelent költséget. Emésztő '
              'kiváltásánál ehhez jön a régi akna megszüntetése is. A konkrét ajánlat a telek '
              'adottságaitól függ, ezért árat itt nem adunk meg; a részleteket a '
              '<a href="biologiai-koltsegtenyezok">költségek oldalon</a> foglaltuk össze.'),
        ),
        tovabb('biologiai-uzemeltetes-es-karbantartas', 'Üzemeltetés és karbantartás: a teendők listája'),
        tovabb('../tudastar/uzemeltetes-teendok-es-koltsegek', 'Üzemeltetési költségek tételesen'),
    ])
    return szekcio('uzemeltetes-koltseg', 'Költség', 'Üzemeltetés és költségtényezők', torzs)


def telek():
    torzs = NL.join([
        '''      <aside class="panel bio-elv" aria-label="Fontos elv">
        <p class="type-ui-body-strong">Fontos elv: a telek adottságai nem a technológiát döntik el, hanem a kivitelezés módját.</p>
      </aside>''',
        folyo(
            p('Magas talajvízállásnál vagy nehéz, kötött agyagtalajnál jellemzően kiemelt '
              'szivárogtató kialakítására van szükség, magas talajvíznél emellett a tartály '
              'felúszás elleni rögzítése is szempont. A telek lejtése és a házból kilépő '
              'szennyvízcső mélysége szintén befolyásolhatja a megoldást.'),
            p('A szükséges szivárogtató mérete a várható terheléstől, a talaj szerkezetétől és a '
              'talajvízszinttől függ, ezért felelősen nem lehet előre négyzetmétert mondani. Ezt '
              'minden esetben a konkrét telek alapján határozzuk meg.'),
            p('A kút helye minden esetben tisztázandó kérdés, akkor is, ha a szomszéd telkén van. '
              'Ezt az elhelyezés tervezésénél kell figyelembe venni.'),
        ),
        tovabb('biologiai-telek-es-terhelesi-feltetelek', 'Telek- és terhelési feltételek — részletesen'),
    ])
    return szekcio('telek-feltetelek', 'Feltételek', 'Telek- és terhelési feltételek', torzs, alt=True)


def mikor_mast():
    esetek = [
        ('Időszakos vagy szezonális használatnál',
         'Ha az ingatlan hetekig üresen áll, a biológiai szennyvíztisztító alulterhelt lesz, és a '
         'baktériumkultúra legyengül. Ilyenkor az oldómedencés rendszer a stabilabb választás, még '
         'akkor is, ha a tisztítás nagy része a talajban történik, alacsonyabb tisztítási '
         'teljesítménnyel.',
         'oldomedences-rendszer', 'Oldómedencés rendszer'),
        ('Kevés a szabad terület a vízelhelyezésre',
         'Ilyenkor nincs „kisebb helyigényű” szennyvíztisztító: ha nincs hova elhelyezni a kezelt '
         'vizet, a zárt tároló marad a járható irány.',
         'megoldastipusok-osszehasonlitasa', 'Megoldástípusok összehasonlítása'),
        ('50 fő feletti kapacitásnál',
         'Ekkor nem háztartási berendezésről, hanem szennyvíztisztító telepről beszélünk.',
         'nagyobb-es-kozossegi-rendszerek', 'Nagyobb és közösségi rendszerek'),
        ('Ha rendelkezésre áll a közcsatorna',
         'Ha van elérhető közcsatorna, főszabály szerint arra kell csatlakozni; új berendezés '
         'létesítését a 147/2010. (IV.&nbsp;29.) Korm. rendelet is korlátozza, ha a '
         'szennyvízelvezető mű az ingatlant határoló közterületen műszakilag rendelkezésre áll, és '
         'van megfelelő telepi kapacitás. Ha azonban a rákötés gazdaságtalan, és ezt '
         'gazdaságossági számítással igazolni lehet, felmentés kérhető a rákötési kötelezettség alól.',
         '../helyzetem/kozcsatorna-vagy-egyedi-rendszer', 'Közcsatorna vagy egyedi rendszer'),
    ]
    kartyak = NL.join(f'''        <li class="situation bio-eset">
          <h3 class="type-ui-card-title situation-title">{a}</h3>
          <p class="type-ui-body situation-text">{b}</p>
          <p class="bio-eset-link"><a class="text-link" href="{h}"><span class="link-label">{f}<span class="action-arrow-end" aria-hidden="true">&rarr;</span></span></a></p>
        </li>''' for a, b, h, f in esetek)
    torzs = NL.join([
        folyo(p('Nem minden helyzetben ez a jó válasz. Négy esetben mást ajánlunk — és ezek közül '
                'háromra szintén van megoldásunk.')),
        f'''      <ul class="situation-grid bio-esetek" data-cols="4" role="list">
{kartyak}
      </ul>''',
        tovabb('biologiai-mikor-nem-megfelelo', 'Mikor nem megfelelő — részletesen'),
    ])
    return szekcio('mikor-mast', 'Őszintén', 'Mikor javasolunk mást?', torzs)


def telepitesek():
    kepek = NL.join([
        foto('telepites-munkagodor', 1200, 800,
             'Egyenes falú munkagödör agyagos talajban, tömörített aljjal.',
             'Munkagödör agyagos talajban: a gödör egyenes falú, az alja tömörítve.', 'bio-foto'),
        foto('telepites-beemeles', 1200, 800,
             'Világos színű tartály a munkagödörben, mellette a narancssárga bekötőcső.',
             'A tartály a gödörben, a bekötőcső csatlakoztatása előtt.', 'bio-foto'),
        foto('telepites-kesz', 1200, 800,
             'Elkészült telepítés: gyepes kert, amelyben egyetlen fedlap látszik.',
             'A kész állapot: a gyepben egyetlen fedlap marad látható.', 'bio-foto'),
    ])
    statok = [
        ('2004 óta', 'foglalkozunk biológiai szennyvíztisztítással.'),
        ('3&nbsp;800+', 'megvalósított rendszer országszerte.'),
        ('~767&nbsp;000&nbsp;m³', 'szennyvizet tisztítanak meg évente — becslésünk szerint.'),
    ]
    stat_html = NL.join(f'''        <li class="trust-item">
          <p class="type-ui-card-title trust-title trust-title-data">{a}</p>
          <p class="type-ui-subtitle trust-text">{b}</p>
        </li>''' for a, b in statok)
    torzs = NL.join([
        f'''      <div class="bio-foto-sor">
{kepek}
      </div>''',
        folyo(
            p('Az ÖkoTech-Home Kft. 2004 óta foglalkozik biológiai szennyvíztisztítással; saját '
              'fejlesztésű A.B. Clear berendezéseit Esztergomban gyártja és telepíti. '
              'Országszerte több mint 3800 rendszert valósítottunk meg, amelyek becslésünk szerint '
              'évente mintegy 767&nbsp;000 köbméter szennyvizet tisztítanak meg.'),
            p('Konkrét eseteket — kiindulási helyzettel, választott megoldással és eredménnyel — az '
              '<a href="../eredmenyek/esettanulmanyok">esettanulmányok</a> között talál.'),
        ),
        f'''      <ul class="trust-grid bio-bizalom" role="list">
{stat_html}
      </ul>''',
        tovabb('biologiai-esettanulmanyok', 'Kapcsolódó esettanulmányok'),
    ])
    return szekcio('telepitesek', 'Tapasztalat', 'Megvalósult telepítések', torzs, alt=True)


GYIK = [
    (None, [
        ('Mi az a bio emésztő?',
         'A bio emésztő köznyelvi elnevezés, amellyel jellemzően olyan berendezést jelölnek, amely '
         'a háztartási szennyvizet helyben, biológiai úton tisztítja meg. Szakmailag ez az egyedi '
         'szennyvíztisztító berendezés, más néven biológiai szennyvíztisztító.'),
        ('Mennyibe kerül egy bio emésztő tartály?',
         'A végösszeget nem a tartály ára dönti el, hanem a kapacitás, a tisztítómező mérete, a '
         'földmunka és a telek adottságai. A telek adatai alapján e-mailben küldünk tételes '
         'ajánlatot.'),
        ('Megszűnik teljesen a szippantás?',
         'Egy biológiai szennyvíztisztítónál normál üzemeltetésben nincs szükség rendszeres '
         'szippantásra, mert a fölösiszap az iszapzsákba kerül. A teljes rendszer kiszippantása nem '
         'időszakos karbantartási feladat: arra rendkívüli helyzetben, például súlyosan károsodott '
         'biológiai állapot és teljes újraindítás esetén lehet szükség.'),
        ('Kell-e baktériumot vagy vegyszert adagolni?',
         'A normál működéshez nincs szükség rendszeres technológiai vegyszeradagolásra. A '
         'háztartásban a szokásos tisztító- és mosószerek normál mennyiségben használhatók; az '
         'viszont nem mindegy, ha agresszív vegyszerből egyszerre nagy mennyiség kerül a '
         'szennyvízbe.'),
    ]),
    ('Üzemeltetés és karbantartás', [
        ('Büdös lesz a kertben?',
         'Egy megfelelően működő rendszer nem jár az emésztőkhöz társított rothadásszaggal, mert a '
         'rendszeres levegőztetés miatt a szennyvíz nem indul rothadásnak. Tartós, szokatlan szag '
         'esetén az okát érdemes megvizsgálni.'),
        ('Mennyi áramot fogyaszt egy biológiai szennyvíztisztító?',
         'Egy 50 wattos kompresszorral működő biológiai szennyvíztisztító megszakítás nélküli '
         'üzemben körülbelül 438&nbsp;kWh áramot fogyaszt évente, illetve 307&nbsp;kWh-t, ha '
         'szakaszos üzemmódban jár. Ez 36&nbsp;Ft/kWh példaárral nagyjából 15&nbsp;800, illetve '
         '11&nbsp;000 forint egy évben.'),
        ('Mi történik áramszünetkor?',
         'Áramszünetben a biológiai szennyvíztisztító kompresszora és ezzel az oxigénellátás leáll. '
         'Egy rövidebb áramszünet önmagában nem jelenti a rendszer elvesztését, hosszabb kimaradás '
         'azonban már kedvezőtlenül befolyásolhatja a biológiai folyamatokat. Általános „ennyi '
         'napot biztosan kibír” ígéretet szándékosan nem adunk.'),
        ('Mi van, ha két hétre elutazunk?',
         'Egy két-három hetes szabadság nem viseli meg a rendszert, és nem is minősül időszakos '
         'használatnak. A rendszeres, hetekig tartó kihagyás az, ami a technológiaválasztást '
         'befolyásolja.'),
    ]),
    ('Engedélyezés', [
        ('Kell-e hozzá engedély?',
         'A szükséges hatósági eljárás attól függ, milyen berendezést telepítenek, hogyan történik '
         'a tisztított víz elhelyezése, és milyenek a helyszín adottságai. A CE-jelöléssel '
         'rendelkező szennyvízkezelő berendezésekre és a tisztított víz elszivárogtatására nem '
         'azonos szabályok vonatkoznak, ezért az alkalmazandó eljárást az adott projekt alapján '
         'tisztázzuk.'),
    ]),
]


def gyik():
    csoportok = []
    for cim, kerdesek in GYIK:
        elemek = NL.join(f'''          <details class="faq-item">
            <summary class="faq-q type-ui-card-title">{k}</summary>
            <div class="faq-a"><p class="type-ui-body">{v}</p></div>
          </details>''' for k, v in kerdesek)
        fej = f'        <h3 class="type-ui-subtitle gyik-csoport-cim">{cim}</h3>{NL}' if cim else ''
        csoportok.append(f'''      <div class="gyik-csoport">
{fej}        <div class="faq">
{elemek}
        </div>
      </div>''')
    return szekcio('gyik', 'Gyakori kérdések', 'Gyakori kérdések', NL.join(csoportok))


def cta():
    return '''
  <section class="section" aria-labelledby="telek-cta-cim">
    <div class="section-inner">
      <aside class="panel-dark" aria-labelledby="telek-cta-cim">
        <div class="panel-dark-head">
          <p class="type-data-eyebrow panel-dark-eyebrow">Következő lépés</p>
          <h2 class="type-display-highlight-title panel-dark-title" id="telek-cta-cim">Nézzük meg, az Ön telkére mi való</h2>
        </div>
        <div class="panel-dark-body">
          <p class="type-ui-body panel-dark-text">Ehhez nem kell helyszíni felmérés. Elég, ha ismeri a telek adatait, a szennyvízcső mélységét és azt, hányan laknak majd a házban.</p>
          <p class="type-ui-body panel-dark-text">Küldje el a telek adatait, és megmondjuk, hogy az Ön ingatlanán milyen biológiai szennyvíztisztító jöhet szóba.</p>
          <p class="panel-dark-actions"><a class="btn btn-inverse" href="../ajanlat#urlap">Telekadatok elküldése</a></p>
          <p class="type-ui-body panel-dark-text"><a href="../helyzetem/milyen-adatokat-kell-osszegyujteni">Milyen adatokat érdemes összegyűjteni?</a></p>
        </div>
      </aside>
    </div>
  </section>'''


JOGSZABALYOK = [
    ('28/2004. (XII.&nbsp;25.) KvVM rendelet',
     'a vízszennyező anyagok kibocsátásaira vonatkozó határértékekről; az alkalmazandó határértéket '
     'az adott befogadó és a terület besorolása határozza meg.'),
    ('147/2010. (IV.&nbsp;29.) Korm. rendelet',
     'az egyedi szennyvíztisztító létesítményekre vonatkozó általános szabályok.'),
    ('72/1996. (V.&nbsp;22.) Korm. rendelet', 'a vízgazdálkodási hatósági jogkör gyakorlásáról.'),
    ('1995. évi LVII. törvény', 'a vízgazdálkodásról — a vízilétesítmények törvényi háttere.'),
    ('MSZ EN 12566-3', 'a legfeljebb 50 lakosegyenértékű szennyvíztisztító kisberendezésekre '
     'vonatkozó európai szabvány; berendezéseink CE-jelölése ezen alapul.'),
]


def jogi():
    elemek = NL.join(f'          <div class="bio-jogi-tetel"><dt class="type-ui-body-strong">{a}</dt>'
                     f'<dd class="type-ui-body">{b}</dd></div>' for a, b in JOGSZABALYOK)
    torzs = NL.join([
        f'''      <dl class="bio-jogi">
{elemek}
      </dl>''',
        folyo(p('Mivel a jogszabályok és a helyi előírások változhatnak, a konkrét ingatlanra '
                'vonatkozó eljárást mindig az aktuálisan hatályos szabályok alapján kell '
                'meghatározni. Ezért ha bizonytalan, inkább kérdezzen rá.')),
        f'''      <aside class="bio-szerzo" aria-label="Az oldal szerzője">
        <p class="type-ui-body">Az oldalt az <strong>ÖkoTech-Home Kft.</strong> szakmai csapata állította össze. A vállalkozás 2004 óta foglalkozik biológiai szennyvíztisztító berendezésekkel, saját A.B. Clear berendezéseit Esztergomban gyártja — az itt leírtak tehát saját gyártói és telepítési tapasztalaton alapulnak.</p>
        <p class="type-ui-caption bio-szerzo-datum">Utolsó szakmai frissítés: <time datetime="{FRISSITVE[1]}">{FRISSITVE[2]}</time></p>
      </aside>''',
    ])
    return szekcio('jogszabalyok', 'Háttér', 'Jogszabályi és szabványi háttér', torzs)


# ================================================================ LAP
def jsonld(tartalom_html):
    faq = []
    for _, kerdesek in GYIK:
        for k, v in kerdesek:
            faq.append({'@type': 'Question', 'name': szoveg(k),
                        'acceptedAnswer': {'@type': 'Answer', 'text': szoveg(v)}})
    szervezet = {'@type': 'Organization', 'name': 'ÖkoTech-Home Kft.', 'url': f'{DOMAIN}/'}
    graf = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'Article',
                'headline': H1,
                'description': LEIRAS,
                'inLanguage': 'hu-HU',
                'image': f'{DOMAIN}/assets/img/oldalak/hero-biologiai.webp?v=2',
                'dateModified': FRISSITVE[0],
                'about': [
                    {'@type': 'Thing', 'name': 'biológiai szennyvíztisztító',
                     'alternateName': ['bio emésztő', 'ökoemésztő', 'bio emésztő tartály',
                                       'egyedi szennyvíztisztító berendezés',
                                       'házi szennyvíztisztító']},
                ],
                'author': szervezet,
                'publisher': szervezet,
                'mainEntityOfPage': f'{DOMAIN}/{UT}',
            },
            {
                '@type': 'Service',
                'name': 'Biológiai szennyvíztisztítás',
                'description': LEIRAS,
                'serviceType': 'Decentralizált szennyvízkezelés',
                'provider': szervezet,
                'areaServed': {'@type': 'Country', 'name': 'Magyarország'},
                'url': f'{DOMAIN}/{UT}',
            },
            {
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': 1, 'name': 'Főoldal', 'item': f'{DOMAIN}/'},
                    {'@type': 'ListItem', 'position': 2, 'name': 'Megoldások',
                     'item': f'{DOMAIN}/megoldasok/'},
                    {'@type': 'ListItem', 'position': 3, 'name': 'Biológiai szennyvíztisztítás',
                     'item': f'{DOMAIN}/{UT}'},
                ],
            },
            {'@type': 'FAQPage', 'mainEntity': faq},
        ],
    }
    return ('<script type="application/ld+json">' + NL
            + json.dumps(graf, ensure_ascii=False, indent=2) + NL + '</script>')


def epit(t):
    # A HERO KÉPE és a SZAKASZ OLDALAINAK listája a kiadott lapból marad — a
    # kép jelölését a hero_avif.py tartja karban, a lista a megamenüvel él.
    kep = re.search(r'    <figure class="hero-media page-hero-media">.*?</figure>', t, re.S).group(0)
    szakasz = re.search(r'  <section class="section" aria-labelledby="mit-erdemes-megnezni-cim">.*?</section>',
                        t, re.S).group(0)
    fo = f'''<main id="fotartalom">

  <section class="hero page-hero" aria-labelledby="oldal-cim">
    <div class="hero-inner">
      <div class="hero-copy">
        <nav class="breadcrumb" aria-label="Morzsamenü">
          <ol class="breadcrumb-list type-ui-caption" role="list">
            <li><a href="../">Főoldal</a></li>
            <li><a href="./">Megoldások</a></li>
            <li aria-current="page">Biológiai szennyvíztisztítás</li>
          </ol>
        </nav>
        <h1 class="type-display-page-title hero-title" id="oldal-cim">{esc(H1)}</h1>
        <p class="type-ui-body-strong hero-lead">{esc(LEAD)}</p>
      </div>
    </div>
{kep}
  </section>
{bevezeto()}
{mukodes()}
{bio_emeszto()}
{mert_adatok()}
{kinek()}
{uzemeltetes()}
{telek()}
{mikor_mast()}
{telepitesek()}
{gyik()}
{cta()}
{jogi()}

{szakasz}
</main>'''
    u = re.sub(r'<main id="fotartalom">.*?</main>', lambda _: fo, t, count=1, flags=re.S)
    cserek = [
        (r'<title>.*?</title>', f'<title>{esc(CIM)}</title>'),
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{_html.escape(LEIRAS)}">'),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{_html.escape(CIM)}">'),
        (r'<meta property="og:description" content="[^"]*">',
         f'<meta property="og:description" content="{_html.escape(LEIRAS)}">'),
        (r'<meta property="og:image:alt" content="[^"]*">',
         '<meta property="og:image:alt" content="Talajmetszet egy családi ház kertjében: '
         'A.B.Clear biológiai tisztítótartály kavicságyon">'),
    ]
    for minta, uj in cserek:
        u, n = re.subn(minta, lambda _: uj, u, count=1)
        assert n == 1, minta
    u, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda _: jsonld(fo), u,
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
