#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hazi_szennyviztisztito.py — Megoldások → Házi szennyvíztisztító.

MIÉRT. A „házi szennyvíztisztító" (390 keresés/hó) és klasztere — hátrányai 90,
legjobb 70, egyedi szennyvíztisztító kisberendezés 70, szennyvíztisztító
házilag 70, legolcsóbb 50, rendszer 50, engedélyezése 40, házi biológiai 30,
vélemények 20, pályázat 20, kisberendezés 20 — eddig nem kapott saját lapot.
Bela szövege, 2026-09-18.

SZÁNDÉK ÉS KANNIBALIZÁCIÓ. A főoldal címe („Biológiai házi szennyvíztisztító
közcsatorna nélkül") és a fogalmi tudástár-lap ugyanerre a kifejezésre megy.
Ez a lap ezért DÖNTÉSI szándékú: melyik rendszer való Önnek, mik a hátrányok,
mi az engedélyezés menete, mi a költség — nem fogalommagyarázat, és nem
márkabemutató. A fogalmakra a tudástár-lapra, a technológiára a biológiai
lapra visz tovább.

A KÁNON SZERINT (Bela, 2026-09-18): engedélyezés (1), legkisebb kapacitás (2),
oxigénellátás (3), kétféle költségadat kiírva (4), garancia (5), kibocsátás (6),
iszap hasznosítása (7), 767 000 m³ becslésként (9), írásmód (10).

A SZÖVEG BELÁÉ, öt ponton a webhely saját forrásaihoz tompítva:
  · a tisztítószerek „nagy mennyiségben" károsíthatják a biológiát (a webhely
    sehol nem mondja, hogy a rendszeres használat felborítja) — `tudastar/tisztitoszerek`;
  · a tisztítómező fölött gyep és sekély gyökérzetű növény lehet, burkolat, fa
    és járműforgalom nem — `projekt-elokeszites/tisztitomezo`;
  · a talajterhelési díjnál a webhely a fizetési KÖTELEZETTSÉG feltételét írja
    le (2003. évi LXXXIX. tv.); „mentesség" állításra nincs forrás;
  · a szivárogtatási próba útmutatóját a `tudastar/elszivarogtatas` ígéri, a
    kapcsolati lapra mutatva — „k tényezőről szóló oldal" nincs;
  · Csikvánd: „Vidékfejlesztési Program"; Bakonypéterd: a telepet ma a
    Pannon-Víz Zrt. üzemelteti.

FUTTATÁS:  python3 scripts/oldalgyartas/hazi_szennyviztisztito.py
"""
import html as _html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import hazi_abra as abra  # noqa: E402

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
DOMAIN = 'https://okotechhome.hu'
UT = 'megoldasok/hazi-szennyviztisztito'
LAP = WEB / 'megoldasok' / 'hazi-szennyviztisztito.html'
MINTA_LAP = WEB / 'megoldasok' / 'biologiai-szennyviztisztitas.html'
FRISSITVE = ('2026-09-18', '2026-09', '2026. szeptember')

CIM = 'Házi szennyvíztisztító: melyik rendszer való Önnek?'
LEIRAS = ('Melyik házi szennyvíztisztító való az Ön ingatlanára? Döntési szempontok, őszinte '
          'hátrányok, engedélyezés és költségek — magyar gyártótól.')
H1 = 'Házi szennyvíztisztító: melyik rendszer való az Ön ingatlanára?'
LEAD = ('A házi szennyvíztisztító olyan kisberendezés, amely egy ingatlan szennyvizét a keletkezés '
        'helyén kezeli — ott, ahol nincs közcsatorna, vagy a rákötés nem megoldható. A jogszabályok '
        'ezt egyedi szennyvíztisztító berendezésnek nevezik.')

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


def foto(kep, alt, felirat, mappa='galeria'):
    return f'''      <figure class="hub-foto">
        <img src="../assets/img/{mappa}/{kep}.webp?v=1" width="1200" height="800"
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
    ('melyik-valo', 'Melyik rendszer való Önnek?'),
    ('hogyan-mukodik', 'Hogyan működik?'),
    ('legjobb', 'Melyik a legjobb?'),
    ('hatranyok', 'A hátrányai'),
    ('hazilag', 'Lehet házilag?'),
    ('koltseg', 'Mennyibe kerül?'),
    ('engedelyezes', 'Engedélyezés'),
    ('kinek-a-berendezese', 'Kinek a berendezését?'),
    ('gyik', 'Gyakori kérdések'),
]


def bevezeto():
    linkek = NL.join(f'            <li><a class="hub-tartalom-link" href="#{a}">{esc(c)}</a></li>'
                     for a, c in TARTALOM)
    return f'''
  <section class="section" aria-labelledby="lenyeg-cim">
    <div class="section-inner hub-bevezeto">
      <div class="hub-bevezeto-szoveg">
        <p class="type-ui-body-strong">Ez az oldal nem a fogalmakat magyarázza, hanem a döntéshez ad támpontot: melyik rendszer való az Ön ingatlanára, mire számíthat az üzemeltetésnél, mik a valódi hátrányok, és milyen hatósági eljárással kell számolni.</p>
        <p class="type-ui-body">Ha a bioemésztő, ökoemésztő és oldómedence kifejezések között szeretne előbb rendet tenni, azt a <a href="../tudastar/bioemeszto-okoemeszto-hazi-szennyviztisztito">fogalmi oldalunkon</a> tettük meg.</p>
        <nav class="hub-tartalom" aria-label="Az oldal tartalma">
          <p class="type-data-eyebrow hub-tartalom-cim">Az oldalon</p>
          <ol class="hub-tartalom-lista" role="list">
{linkek}
          </ol>
        </nav>
      </div>
      <aside class="hub-lenyeg" aria-labelledby="lenyeg-cim">
        <h2 class="type-display-highlight-title hub-lenyeg-cim" id="lenyeg-cim">A lényeg röviden</h2>
        <p class="type-ui-body">Nincs egyetlen „legjobb” házi szennyvíztisztító. A választást a használat jellege dönti el, a megvalósítás feltételeit pedig a telek. Egész évben lakott háznál az aktív biológiai tisztítás az elsődleges irány; erősen szezonális használatnál az oldómedencés rendszer is szóba jön, de nagyobb méretű tisztítómezőt igényelhet.</p>
        <dl class="hub-kulcsadatok">
          <div class="hub-kulcsadat"><dt class="type-ui-caption">Legkisebb szabványos berendezés</dt><dd class="type-data-value">6&nbsp;LE</dd></div>
          <div class="hub-kulcsadat"><dt class="type-ui-caption">A termékcsalád felső határa</dt><dd class="type-data-value">50&nbsp;LE</dd></div>
          <div class="hub-kulcsadat"><dt class="type-ui-caption">Villamos energia havonta</dt><dd class="type-data-value">1000–1500&nbsp;Ft</dd></div>
          <div class="hub-kulcsadat"><dt class="type-ui-caption">Rendszeres szippantás</dt><dd class="type-data-value">nincs</dd></div>
        </dl>
        <p class="type-ui-caption hub-lenyeg-jegyzet">Az A.B. Clear 6 adatai; a havi összeg <strong>csak a villamos energia</strong>, 36&nbsp;Ft/kWh példaárral. A teljes üzemeltetés — árammal, iszapzsákkal és évesített membráncserével — nagyjából 22&nbsp;700–27&nbsp;500&nbsp;Ft évente.</p>
      </aside>
    </div>
  </section>'''


HELYZET_TABLA = [
    ('Egész évben lakott családi ház', '<a href="biologiai-szennyviztisztitas">Aktív biológiai szennyvíztisztító</a>',
     'A napi terhelés kiszámítható, a biológia folyamatosan tápanyagot kap.'),
    ('Nyaraló, hétvégi ház', 'Biológiai vagy <a href="oldomedences-rendszer">oldómedencés</a>',
     'Egy 2–3 hetes kihagyás egyik technológiánál sem okoz gondot; erősen szezonális '
     'használatnál az oldómedence is szóba jön.'),
    ('Meglévő emésztő kiváltása', '<a href="biologiai-szennyviztisztitas">Aktív biológiai szennyvíztisztító</a>',
     'A régi akna kitisztítás és vízzáróvá tétel után például esővízgyűjtőként hasznosítható tovább.'),
    ('Panzió, étterem, intézmény', '<a href="nagyobb-es-kozossegi-rendszerek">Kapacitás szerint méretezett rendszer</a>',
     'Itt a terhelési profil és a csúcsidőszakok döntenek, nem az épület funkciója.'),
]


def melyik_valo():
    sorok = NL.join(
        f'            <tr><th scope="row" class="type-ui-body-strong">{a}</th>'
        f'<td class="type-ui-body">{b}</td><td class="type-ui-body">{c}</td></tr>'
        for a, b, c in HELYZET_TABLA)
    torzs = NL.join([
        abra.helyzet_abra('helyzet-abra-cim'),
        f'''      <div class="compare-scroll hub-tabla-keret" tabindex="0" role="region" aria-labelledby="helyzet-tabla-cim">
        <table class="compare-table compare-table-start hub-tabla">
          <caption class="type-ui-card-title" id="helyzet-tabla-cim">Az Ön helyzete és a javasolt irány</caption>
          <thead><tr><th scope="col">Az Ön helyzete</th><th scope="col">Melyik irány?</th><th scope="col">Miért?</th></tr></thead>
          <tbody>
{sorok}
          </tbody>
        </table>
      </div>''',
        folyo(p('Ezután következik a telek: a '
                '<a href="../projekt-elokeszites/talaj-es-szivargokepesseg">talaj vízáteresztő '
                'képessége</a>, a <a href="../projekt-elokeszites/talajviz">talajvízszint</a>, a '
                '<a href="../projekt-elokeszites/lejtes-es-csomelyseg">lejtés</a> és a '
                '<a href="../projekt-elokeszites/telekmeret-es-szabad-terulet">rendelkezésre álló '
                'szabad terület</a>. Ezek nem írják felül a technológiaválasztást, hanem azt '
                'határozzák meg, milyen műszaki kialakítással és milyen költséggel valósítható meg.')),
        tovabb('megoldastipus-eloszuro', 'Megoldástípus-előszűrő — öt kérdés'),
    ])
    return szekcio('melyik-valo', 'Döntés', 'Melyik házi szennyvíztisztító való Önnek?', torzs)


def hogyan_mukodik():
    torzs = NL.join([
        folyo(
            p('Az aktív biológiai tisztításban baktériumok bontják le a szennyvíz szerves '
              'anyagtartalmát — ez a lebontás maga a tisztítás. A biológiai folyamathoz szükséges '
              'oxigénellátást kompresszor biztosítja; az <a href="ab-clear-modellek-es-kapacitasok">A.B. '
              'Clear 6</a> berendezésben <strong>50&nbsp;W</strong> teljesítményű kompresszor működik.'),
            p('A tisztítás végén az utóülepítőben válik el a tisztított víz az iszaptól. Ezt a '
              'megtisztított vizet ezután el kell helyezni: jellemzően '
              '<a href="../projekt-elokeszites/elszivarogtatas">szivárogtatómezőn</a> keresztül, '
              'megfelelő feltételek mellett a növények gyökérzónájában hasznosulva.'),
            p('A technológia részleteit — a mérhető kibocsátási értékekkel együtt — a '
              '<a href="biologiai-szennyviztisztitas">biológiai szennyvíztisztítás</a> oldalunkon '
              'írtuk le.'),
        ),
        '      <div class="hub-foto-par">',
        foto('berendezes-belso', 'Nyitott tartály belseje: válaszfalak, levegőztető csövek, tömlő.',
             'A berendezés belseje: válaszfalak és a levegőztetés csövei.'),
        foto('berendezes-kompresszor', 'Kék burkolatú membrános légszivattyú, a berendezés kompresszora.',
             'A kompresszor adja az oxigént — a rendszer egyetlen mozgó alkatrésze.'),
        '      </div>',
    ])
    return szekcio('hogyan-mukodik', 'Működés', 'Hogyan működik egy házi szennyvíztisztító?', torzs, alt=True)


OSSZEHASONLITAS = [
    ('Van-e mért adat a kibocsátásról?',
     'Vagyis nem gyártói ígéret, hanem független vizsgálati eredmény. Az A.B. Clear berendezések '
     'VITUKI vizsgálati zárójegyzőkönyv szerinti értékei: KOI(Cr) 55, BOI₅ 15, lebegőanyag 18, '
     'N-NH₄ 9, összes nitrogén 20, összes foszfor 5&nbsp;mg/l.'),
    ('Megvan-e a szabványi megfelelés?',
     'Rendelkezik-e a berendezés az <a href="../tudastar/en-12566-1-vagy-en-12566-3">EN&nbsp;12566-3</a> '
     'szabvány szerinti CE-tanúsítással?'),
    ('Mi történik az iszappal?',
     'Ez dönti el, kell-e rendszeres szippantás, vagy sem — lásd az '
     '<a href="ab-clear-iszapzsakos-technologia">iszapzsákos technológiát</a>.'),
    ('Ki végzi a szervizt, és honnan jön?',
     'Egy berendezés élettartama évtizedekben mérhető, a karbantartás pedig jogszabályi előírás is.'),
    ('Mekkora a valódi helyigény?',
     'A legtöbb telken nem a tartály, hanem a '
     '<a href="../projekt-elokeszites/tisztitomezo">tisztítómező</a> mérete szab határt.'),
]


def legjobb():
    torzs = NL.join([
        folyo(
            p('Erre a kérdésre az őszinte válasz az, hogy <strong>nincs egyetlen legjobb</strong>, '
              'mert a helyzetek is különböznek. Ugyanaz a berendezés kiváló egy állandóan lakott '
              'háznál, viszont rossz választás egy évente néhány hetet használt nyaralóban.'),
            p('Amit viszont érdemes összehasonlítani, az öt konkrét dolog:'),
        ),
        kartyak(OSSZEHASONLITAS, 'hub-feltetelek'),
        folyo(
            p('Ez az öt kérdés többet mond egy berendezésről, mint bármilyen rangsor.'),
            p('Egy konkrét projekt kibocsátási megfelelőségét mindig az adott befogadó, az '
              'alkalmazandó határértékek és a hatósági előírások alapján kell megítélni.'),
        ),
        tovabb('ab-clear-muszaki-adatok', 'A.B. Clear műszaki adatok'),
        tovabb('../eredmenyek/tanusitvanyok-es-dokumentumok', 'Tanúsítványok és dokumentumok'),
    ])
    return szekcio('legjobb', 'Összehasonlítás', 'Melyik a legjobb házi szennyvíztisztító?', torzs)


HATRANYOK = [
    ('Folyamatos villamosenergia-ellátást igényel.',
     'Az aktív biológiai tisztítás oxigénellátás nélkül nem működik. Gyenge vagy időszakos '
     'betáplálású ingatlanon ezt előre tisztázni kell.'),
    ('Helyet kér — de nem ott, ahol gondolná.',
     'A berendezés maga viszonylag kis helyet foglal. A tisztított víz elhelyezéséhez viszont '
     'összefüggő, beépítetlen terület kell, és a legtöbb telken ez ütközik korlátba előbb. A '
     '<a href="../projekt-elokeszites/tisztitomezo">tisztítómező</a> a föld alatt van: fölötte '
     'gyep és sekély gyökérzetű növényzet lehet, burkolat, mély gyökérzetű fa és járműforgalom nem.'),
    ('Élő rendszer, tehát érzékeny.',
     'Ami fertőtlenítésre készült, az a rendszerben lévő baktériumokat is fertőtleníti. A hipó, a '
     'klóros és fertőtlenítő tisztítószerek, valamint a lefolyóba öntött sütőolaj <strong>nagy '
     'mennyiségben</strong> károsíthatja a biológiát — a szokásos háztartási mennyiség rendben van. '
     'Részletesen a <a href="../tudastar/tisztitoszerek">tisztítószerekről</a> szóló lapon.'),
    ('Nem felejthető el.',
     'A rendszer rendszeres ellenőrzést és karbantartást igényel: a 147/2010. (IV.&nbsp;29.) Korm. '
     'rendelet a tulajdonosra ellenőrzési, karbantartási és dokumentálási kötelezettséget ró.'),
    ('Nem minden telken valósítható meg ugyanúgy.',
     'A helyi építési szabályzat korlátozhatja az egyedi szennyvízkezelést, fokozottan érzékeny '
     'vagy vízbázisvédelmi területen pedig további korlátozások vonatkozhatnak a tisztított víz '
     'talajba juttatására — lásd a '
     '<a href="kizaro-es-korlatozo-feltetelek">kizáró és korlátozó feltételeket</a>.'),
]


def hatranyok():
    torzs = NL.join([
        folyo(p('Ezeket ritkán írják le a gyártók, pedig a döntéshez hozzátartoznak. Öt valódi '
                'korlát van.')),
        kartyak(HATRANYOK),
        folyo(p('Ezek egyike sem kizáró ok önmagában. Viszont mind olyan kérdés, amit a megrendelés '
                '<strong>előtt</strong> kell tisztázni, nem utána.')),
        foto('kesz_kertek-gyep',
             'Nyírt gyep, kavicsos szárazpatak és sziklaágyás egy kertben; a gyepen egyetlen kerek fedlap látszik.',
             'A tisztítómező és a tartály a föld alatt: a felszínen a fedlap marad.'),
    ])
    return szekcio('hatranyok', 'Őszintén', 'A házi szennyvíztisztító hátrányai', torzs, alt=True)


def hazilag():
    torzs = NL.join([
        folyo(
            p('Sokan keresnek rá arra, hogyan lehet szennyvíztisztítót vagy szikkasztót házilag '
              'építeni. A válasz árnyalt.'),
            p('<strong>Amit házilag érdemes elvégezni: a szivárogtatási próbát.</strong> A helyszíni '
              'próba egyszerű módja annak, hogy közvetlen információt kapjunk a tervezett '
              'szivárogtató helyén a talaj vízbefogadó képességéről; ez a méretezés legfontosabb '
              'telekspecifikus bemeneti adata. Az útmutatót '
              '<a href="../kapcsolat">kérésre elküldjük</a>, a módszert pedig az '
              '<a href="../tudastar/elszivarogtatas">elszivárogtatásról</a> és a '
              '<a href="../projekt-elokeszites/szivarogtatasi-vizsgalat">szivárogtatási '
              'vizsgálatról</a> szóló lapunkon írtuk le.'),
            p('<strong>Amit nem érdemes: magát a tisztítóberendezést.</strong> Három okból. Egyrészt '
              'az engedélyezési eljárásban a berendezés megfelelőségét igazolni kell. Másrészt a '
              'biológiai tisztítás méretezése a napi terheléstől, az oxigénellátás teljesítményétől '
              'és az iszapkezeléstől együtt függ, nem külön-külön. Ha pedig a rendszer nem tisztít '
              'megfelelően, az a tisztítómezőt tömíti el — ez a legdrágább javítás az egész '
              'rendszerben.'),
            p('A házilag épített szikkasztónál ugyanez a helyzet: a szerkezet egyszerű, a '
              'méretezése viszont nem az.'),
        ),
    ])
    return szekcio('hazilag', 'Barkács', 'Lehet szennyvizet tisztítani házilag?', torzs)


def koltseg():
    torzs = NL.join([
        folyo(
            p('A végösszeget nem a tartály ára dönti el, hanem a tisztítómező mérete, a földmunka és '
              'a telek adottságai. Ezért ugyanaz a berendezés két szomszédos telken is eltérő '
              'beruházási költséget jelenthet.'),
            p('A „legolcsóbb házi szennyvíztisztító” keresésre is érdemes egy őszinte válasz: a '
              'legolcsóbb beruházás és a legolcsóbb megoldás ritkán ugyanaz. Egy zárt tároló '
              'beszerzése olcsóbb, az üzemeltetése viszont évről évre ismétlődő költség, és a '
              'háztartás méretével meg a szolgáltatási díjakkal együtt nő. A valódi költség később '
              'jelentkezik, ráadásul egy alulméretezett tisztítómező néhány év múlva kerül igazán '
              'sokba.'),
            p('Az üzemeltetési oldalon a háztartási A.B. Clear 6 rendszer '
              '<strong>villamosenergia-költsége</strong> üzemmódtól függően nagyjából '
              '<strong>1000–1500 forint havonta</strong>, 36&nbsp;Ft/kWh példaárral számolva. A '
              '<strong>teljes üzemeltetés</strong> — a villamos energiával, az iszapzsákkal és az '
              'évesített membráncserével együtt — nagyjából <strong>22&nbsp;700–27&nbsp;500 forint '
              'évente</strong>; a karbantartási szerződés díja ebben nincs benne. Szippantással '
              'normál üzemeltetés mellett nem kell számolni: a fölösiszap az iszapzsákban gyűlik.'),
        ),
        tovabb('biologiai-koltsegtenyezok', 'Költségtényezők — mi mozgatja a végösszeget'),
        tovabb('../tudastar/uzemeltetes-teendok-es-koltsegek', 'Üzemeltetési költségek tételesen'),
    ])
    return szekcio('koltseg', 'Költség', 'Mennyibe kerül egy házi szennyvíztisztító?', torzs, alt=True)


def engedelyezes():
    torzs = NL.join([
        folyo(
            p('A szükséges hatósági eljárás attól függ, milyen berendezést telepítenek, hogyan '
              'történik a tisztított víz elhelyezése, és milyenek a helyszín adottságai. A '
              'CE-tanúsítással rendelkező szennyvízkezelő berendezésekre és a tisztított víz '
              'elszivárogtatására nem azonos szabályok vonatkoznak, ezért az alkalmazandó eljárást '
              'minden esetben az adott projekt alapján tisztázzuk.'),
            p('A kialakításnál a <strong>147/2010. (IV.&nbsp;29.) Korm. rendelet</strong> a talaj '
              'adottságainak, a felszín alatti víz mélységének és a szennyvíz mennyiségének '
              'együttes figyelembevételét írja elő.'),
            p('Egy dolgot érdemes külön kiemelni: ha a műszakilag rendelkezésre álló közcsatornára '
              'nem történt rákötés, felmerülhet a <strong>talajterhelési díj</strong>. A fizetési '
              'kötelezettség feltételeit a 2003. évi LXXXIX. törvény szabja meg — a részleteket az '
              '<a href="../helyzetem/meglevo-emesztot-szeretnek-kivaltani">emésztő kiváltása</a> '
              'oldalon foglaltuk össze.'),
        ),
        tovabb('../helyzetem/kozcsatorna-vagy-egyedi-rendszer', 'Közcsatorna vagy egyedi rendszer'),
    ])
    return szekcio('engedelyezes', 'Hatósági eljárás', 'Házi szennyvíztisztító engedélyezése', torzs)


PROJEKTEK = [
    ('Óbudavár, 2011', 'minisztériumi mintaprojekt a Balaton-felvidéken.', '../eredmenyek/obudavar'),
    ('Csikvánd, 2017–2018', '128 darab A.B. Clear egység — Magyarországon elsőként lezárt projekt a '
     'Vidékfejlesztési Program keretében.', '../eredmenyek/csikvand'),
    ('Bakonypéterd, 2018', 'négy darab 50 fős berendezésből álló, távüzemben irányítható központi '
     'telep; ma a Pannon-Víz Zrt. üzemelteti.', '../eredmenyek/bakonypeterd'),
    ('Diósberény, 2022', '90 darab A.B. Clear egység, saját csapattal telepítve.',
     '../eredmenyek/diosbereny'),
    ('Balaton-felvidéki Nemzeti Park Igazgatóság', 'intézményi telepítés.',
     '../eredmenyek/ugyfeltapasztalatok'),
]


def kinek_a_berendezese():
    elemek = NL.join(
        f'          <div class="hub-jogi-tetel"><dt class="type-ui-body-strong">{cim}</dt>'
        f'<dd class="type-ui-body">{szov} <a href="{h}">Részletek</a></dd></div>'
        for cim, szov, h in PROJEKTEK)
    bizalom = [
        ('2004 óta', 'gyártunk biológiai szennyvíztisztító berendezéseket Esztergomban.'),
        ('3&nbsp;800+', 'telepített rendszer országszerte.'),
        ('EP 2766313', 'európai szabadalom az A.B. Clear műszaki megoldására.'),
        ('ISO 9001', 'minőségirányítási rendszerben folyó gyártás.'),
    ]
    bizalom_html = NL.join(f'''        <li class="trust-item">
          <p class="type-ui-card-title trust-title trust-title-data">{a}</p>
          <p class="type-ui-subtitle trust-text">{b}</p>
        </li>''' for a, b in bizalom)
    torzs = NL.join([
        folyo(
            p('A „vélemények” keresés mögött egy egyszerű kérdés áll: kiben lehet megbízni '
              'évtizedes távon?'),
            p('Amit mi fel tudunk mutatni: 2004 óta gyártunk biológiai szennyvíztisztító '
              'berendezéseket Esztergomban, és több mint 3800 rendszert telepítettünk országszerte. '
              'Becslésünk szerint berendezéseink évente mintegy 767&nbsp;000&nbsp;m³ szennyvizet '
              'tisztítanak meg.'),
        ),
        f'''      <ul class="trust-grid hub-bizalom" role="list">
{bizalom_html}
      </ul>''',
        folyo(p('Intézményi és települési léptékben ezek a lezárt projektjeink:')),
        f'''      <dl class="hub-jogi">
{elemek}
      </dl>''',
        folyo(
            p('Az A.B. Clearben alkalmazott műszaki megoldás saját fejlesztésünk, amelyre '
              'nemzetközi szabadalmi eljárást követően <strong>európai szabadalmat</strong> '
              'szereztünk (EP&nbsp;2766313). A gyártás <strong>ISO&nbsp;9001</strong> '
              'minőségirányítási rendszerben folyik. A berendezésre a mindenkor hatályos '
              'jogszabályok szerinti jótállás, <strong>2&nbsp;év</strong> vonatkozik; az általunk '
              'kiszállított és szakszerűen telepített tartály stabilitására <strong>15&nbsp;év</strong> '
              'garanciát vállalunk.'),
        ),
        tovabb('../eredmenyek/ugyfeltapasztalatok', 'Ügyféltapasztalatok'),
        tovabb('../eredmenyek/esettanulmanyok', 'Megvalósult projektek'),
    ])
    return szekcio('kinek-a-berendezese', 'Bizalom', 'Kinek a berendezését érdemes választani?',
                   torzs, alt=True)


GYIK = [
    ('Mi az a házi szennyvíztisztító?',
     'A házi szennyvíztisztító olyan kisberendezés, amely egy ingatlan szennyvizét a keletkezés '
     'helyén kezeli. A jogszabályok egyedi szennyvíztisztító berendezésnek vagy egyedi '
     'szennyvíztisztító kisberendezésnek nevezik.'),
    ('Melyik a legjobb házi szennyvíztisztító?',
     'Nincs egyetlen legjobb, mert a választást a használat jellege dönti el. Érdemes viszont '
     'megnézni, van-e független mért adat a kibocsátásról, rendelkezik-e a berendezés '
     'EN 12566-3 szabvány szerinti CE-tanúsítással, mi történik az iszappal, ki végzi a szervizt, '
     'és mekkora a tisztított víz elhelyezésének helyigénye.'),
    ('Mik a házi szennyvíztisztító hátrányai?',
     'Folyamatos villamosenergia-ellátást igényel, a tisztított víz elhelyezéséhez szabad területre '
     'van szükség, a biológiát a fertőtlenítő tisztítószerek nagy mennyiségben károsíthatják, '
     'rendszeres karbantartást kíván, és nem minden telken valósítható meg ugyanúgy.'),
    ('Milyen hatósági eljárás szükséges a telepítéshez?',
     'Ez attól függ, milyen berendezést telepítenek, hogyan történik a tisztított víz elhelyezése, '
     'és milyenek a helyszín adottságai. A CE-tanúsítással rendelkező berendezésekre és a '
     'tisztított víz elszivárogtatására nem azonos szabályok vonatkoznak, ezért az alkalmazandó '
     'eljárást az adott projekt alapján tisztázzuk.'),
    ('Kell-e szippantás a berendezés mellé?',
     'Normál üzemeltetés mellett nincs szükség rendszeres szippantásra: az iszapzsákos '
     'technológiánál a fölösiszap a zsákban gyűlik. A rendszer állapotát ugyanakkor érdemes '
     'rendszeresen ellenőrizni.'),
    ('Van-e pályázati lehetőség házi szennyvíztisztítóra?',
     'Volt már rá példa: Csikvándon 2017–2018-ban 128 A.B. Clear egység telepítése valósult meg a '
     'Vidékfejlesztési Program keretében. Hogy éppen most van-e az Ön esetére alkalmazható kiírás, '
     'azt érdemes az ajánlatkéréskor megkérdezni.'),
    ('Mekkora a legkisebb berendezés?',
     'Az A.B. Clear legkisebb szabványos berendezése 6 lakosegyenérték névleges kapacitású; a '
     'termékcsalád 50 lakosegyenértékig kínál megoldást.'),
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
          <p class="type-ui-body panel-dark-text">A választáshoz nem kell helyszíni felmérés, és nem jár elköteleződéssel sem. Elég a telek helye, a rendszeresen jelen lévő létszám, és annyi, amennyit a talajról, a talajvízről és a szabad területről tud.</p>
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
        <p class="type-ui-body">Az oldalt az <strong>ÖkoTech-Home Kft.</strong> szakmai csapata állította össze, amely 2004 óta gyárt biológiai szennyvíztisztító berendezéseket Esztergomban, és eddig több mint 3800 rendszert telepített országszerte.</p>
        <p class="type-ui-caption hub-szerzo-datum">Utolsó szakmai frissítés: <time datetime="{FRISSITVE[1]}">{FRISSITVE[2]}</time></p>
      </aside>
    </div>
  </section>'''


def jsonld():
    szervezet = {'@type': 'Organization', 'name': 'ÖkoTech-Home Kft.', 'url': f'{DOMAIN}/'}
    graf = {
        '@context': 'https://schema.org',
        '@graph': [
            {'@type': 'Article', 'headline': H1, 'description': LEIRAS, 'inLanguage': 'hu-HU',
             'image': f'{DOMAIN}/assets/img/oldalak/hero-biologiai.webp?v=2',
             'dateModified': FRISSITVE[0],
             'about': [{'@type': 'Thing', 'name': 'házi szennyvíztisztító',
                        'alternateName': ['egyedi szennyvíztisztító berendezés',
                                          'egyedi szennyvíztisztító kisberendezés',
                                          'házi biológiai szennyvíztisztító',
                                          'házi szennyvíztisztító rendszer']}],
             'author': szervezet, 'publisher': szervezet,
             'mainEntityOfPage': f'{DOMAIN}/{UT}'},
            {'@type': 'BreadcrumbList', 'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Főoldal', 'item': f'{DOMAIN}/'},
                {'@type': 'ListItem', 'position': 2, 'name': 'Megoldások',
                 'item': f'{DOMAIN}/megoldasok/'},
                {'@type': 'ListItem', 'position': 3, 'name': 'Házi szennyvíztisztító',
                 'item': f'{DOMAIN}/{UT}'}]},
            {'@type': 'FAQPage', 'mainEntity': [
                {'@type': 'Question', 'name': szoveg(k),
                 'acceptedAnswer': {'@type': 'Answer', 'text': szoveg(v)}} for k, v in GYIK]},
        ],
    }
    return ('<script type="application/ld+json">' + NL
            + json.dumps(graf, ensure_ascii=False, indent=2) + NL + '</script>')


def epit(alap):
    t = alap
    kep = re.search(r'    <figure class="hero-media page-hero-media">.*?</figure>', t, re.S).group(0)
    fo = f'''<main id="fotartalom">

  <section class="hero page-hero" aria-labelledby="oldal-cim">
    <div class="hero-inner">
      <div class="hero-copy">
        <nav class="breadcrumb" aria-label="Morzsamenü">
          <ol class="breadcrumb-list type-ui-caption" role="list">
            <li><a href="../">Főoldal</a></li>
            <li><a href="./">Megoldások</a></li>
            <li aria-current="page">Házi szennyvíztisztító</li>
          </ol>
        </nav>
        <h1 class="type-display-page-title hero-title" id="oldal-cim">{esc(H1)}</h1>
        <p class="type-ui-body-strong hero-lead">{esc(LEAD)}</p>
      </div>
    </div>
{kep}
  </section>
{bevezeto()}
{melyik_valo()}
{hogyan_mukodik()}
{legjobb()}
{hatranyok()}
{hazilag()}
{koltseg()}
{engedelyezes()}
{kinek_a_berendezese()}
{gyik()}
{cta()}
{szerzo()}
</main>'''
    u = re.sub(r'<main id="fotartalom">.*?</main>', lambda _: fo, t, count=1, flags=re.S)
    cserek = [
        (r'<title>.*?</title>', f'<title>{esc(CIM)}</title>'),   # a megadott 50 karakteres cím, márkanév nélkül
        (r'<meta name="description" content="[^"]*">',
         f'<meta name="description" content="{_html.escape(LEIRAS)}">'),
        (r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{DOMAIN}/{UT}">'),
        (r'<meta property="og:title" content="[^"]*">',
         f'<meta property="og:title" content="{_html.escape(CIM)}">'),
        (r'<meta property="og:description" content="[^"]*">',
         f'<meta property="og:description" content="{_html.escape(LEIRAS)}">'),
        (r'<meta property="og:url" content="[^"]*">',
         f'<meta property="og:url" content="{DOMAIN}/{UT}">'),
        (r'<meta property="og:image:alt" content="[^"]*">',
         '<meta property="og:image:alt" content="Házi szennyvíztisztító">'),
    ]
    for minta, uj in cserek:
        u, n = re.subn(minta, lambda _: uj, u, count=1)
        assert n == 1, minta
    u, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda _: jsonld(), u,
                   count=1, flags=re.S)
    assert n == 1
    return u


def main():
    alap = LAP.read_text(encoding='utf-8') if LAP.exists() else MINTA_LAP.read_text(encoding='utf-8')
    LAP.write_text(epit(alap), encoding='utf-8')
    szavak = len(re.sub(r'<[^>]+>', ' ', re.search(r'<main.*?</main>', LAP.read_text(encoding='utf-8'), re.S).group(0)).split())
    print(f'{LAP.relative_to(GYOKER)}: {LAP.stat().st_size // 1024} KB, ~{szavak} szó a <main>-ben')


if __name__ == '__main__':
    main()
