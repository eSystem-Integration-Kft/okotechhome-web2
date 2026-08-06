#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Megoldások hub — a sitemap szerinti négy döntéstámogató aloldal.

A tartalmi brief alapján. Két szabály végig érvényes, mert a brief maga is
ezeket hangsúlyozza:

1. NINCS „jobb–rosszabb" minősítés. A technológiák FELTÉTELEKKEL és
   kompromisszumokkal írhatók le, nem rangsorral. A cél nem az A.B. Clear
   mindenáron való kiválasztása, hanem a rossz technológiaválasztás megelőzése.

2. NINCS kitalált adat. Ahol a brief belső ÖkoTech-adatot ír elő (karbantartási
   ciklus, kizárási mátrix, telekigény, ürítési intervallum, energiafogyasztás),
   ott ADATHIÁNY-jelölés áll, nem becslés. A 147/2010. Korm. rendeletre
   hivatkozó állítások JOGI ELLENŐRZÉS jelölést kapnak, mert a brief publikálás
   előtti friss ellenőrzést ír elő — a jogszabály változhat, és a téves
   értelmezés a látogatót rossz döntéshez vezetné.

Konkrét ár sehol nem szerepel: csak költségKATEGÓRIA és -logika.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import sec_numbered, sec_split, sec_prose, sec_cta, sec_faq

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

JOGI = ('<!-- JOGI ELLENŐRZÉS PUBLIKÁLÁS ELŐTT: a 147/2010. (IV. 29.) Korm. rendeletre\n'
        '     hivatkozó állítás. A brief előírja a friss ellenőrzést minden kiadás előtt,\n'
        '     mert a jogszabály és a hatósági gyakorlat változhat. -->')


def adathiany(mi, honnan):
    return f'<!-- ADATHIÁNY: {mi}\n     Forrás: {honnan}. Addig ez a rész nem publikálható konkrét értékkel. -->'


# =========================================================== 1. összehasonlítás
DIMENZIOK = [
    ('Mit csinál a szennyvízzel',
     'gyűjti és tárolja',
     'oldómedencében előkezel, a tisztítás nagy része a tisztítómezőben, a talajban zajlik',
     'energiabevitellel biológiai tisztítást végez'),
    ('Villamos energia', 'nem igényel', 'nem igényel', 'folyamatos ellátást igényel'),
    ('Állandó használat', 'működik, de a gyűjtött mennyiséggel a szállítási igény is nő',
     'működik, ha a tisztítómező mérete és a talaj ezt engedi', 'erre a terhelésre való'),
    ('Időszakos használat', 'működik', 'működik',
     'a biológiai közösséget rendszeres terhelés tartja fenn; hosszú szünet után az '
     'újraindulás időt vesz igénybe'),
    ('Hosszabb távollét', 'nincs biológiai folyamat, amit fenn kellene tartani',
     'a talajban zajló folyamat lassabban reagál a szünetre',
     'a hatásfok átmenetileg csökken; a berendezés élettartamát nem érinti'),
    ('Területigény', 'a tartály helyigénye',
     'a tartály MELLETT tisztítómező is kell — ez a nagyobb tétel',
     'a tartály helyigénye, plusz a kezelt víz elhelyezése'),
    ('A talaj szerepe', 'nincs szerepe, a szennyvíz nem jut a talajba',
     'meghatározó: a tisztítás egy része itt történik',
     'a kezelt víz elhelyezésénél számít, a tisztításban nem'),
    ('Talajvíz-érzékenység', 'a tartály beépítési mélységét érinti',
     'meghatározó: magas talajvíz a tisztítómező működését korlátozza',
     'a beépítést és a kezelt víz elhelyezését érinti'),
    ('A víz további sorsa', 'elszállítás',
     'a talajba szivárog a tisztítómezőn keresztül',
     'elszivárogtatás, felszíni befogadó vagy — feltételekkel — hasznosítás'),
    ('Elszállítási igény', 'a teljes szennyvízmennyiség rendszeres szippantása',
     'időszakos iszapeltávolítás', 'időszakos iszapkezelés'),
    ('Adalékanyag', 'nem értelmezhető',
     'egyes forgalmazók rendszeres baktériumadalékot írnak elő',
     'az A.B. Clear rendszerben a baktériumkultúrát a beérkező szennyvíz táplálja'),
    ('Felhasználói ellenőrzés', 'az ürítési szint követése',
     'a rendszer és a tisztítómező időszakos átnézése',
     'rendszeres, de kis munkaigényű ellenőrzés'),
    ('Mozgó és elektromos alkatrész', 'nincs', 'nincs',
     'kompresszor és membrán — ezek kopó elemek'),
    ('Bővíthetőség', 'a tartály cseréjével', 'a tisztítómező bővítésével',
     'egységek összekapcsolásával'),
]

OSSZEHAS = dict(
    file='megoldasok/megoldastipusok-osszehasonlitasa.html',
    url='megoldasok/megoldastipusok-osszehasonlitasa', img='attekintes',
    title='Megoldástípusok összehasonlítása — zárt tároló, oldómedence, biológiai | ÖkoTech Home',
    desc='A három megoldástípus ugyanazon szempontok szerint: mit csinál a szennyvízzel, '
         'mit igényel a telektől és a használattól, és milyen feladatot hagy a tulajdonosnál.',
    h1='Megoldástípusok összehasonlítása',
    alt='Talajmetszet egy kerti tisztítórendszerrel: ülepítő, biológiai egység és kavicságyas '
        'elszivárogtatás egymás után',
    lead='Ez a táblázat nem rangsor. A három megoldástípus más feladatra való, ezért nem az a '
         'kérdés, melyik a „jobb", hanem hogy melyik feltételeit tudja teljesíteni az Ön '
         'ingatlana — és melyik üzemeltetési feladatot vállalja el.',
    crumbs=[('Főoldal', '../'), ('Megoldások', './')],
)

# ====================================================== 2. melyik mikor megfelelő
HELYZETEK = [
    ('Életvitelszerűen használt családi ház',
     'Aktív biológiai rendszer vizsgálata',
     'Az állandó, egyenletes terhelés az a működési feltétel, amire a biológiai tisztítás '
     'épül. A telek adottságai és a kezelt víz elhelyezése azonban felülírhatják ezt.',
     'nincs folyamatos áram · a kezelt víz nem helyezhető el · a telek nem közelíthető meg géppel'),
    ('Nyaraló, hétvégi ház, hosszú szezonális szünet',
     'Oldómedencés irány vizsgálata',
     'A hosszú, terhelés nélküli szakaszok a biológiai közösséget megviselik. A talajban zajló '
     'folyamat kevésbé érzékeny a szünetre — ha a tisztítómezőnek van elég helye, és a talaj '
     'engedi.',
     'kötött talaj · magas talajvíz · nincs elég terület a tisztítómezőnek'),
    ('Meglévő emésztő kiváltása',
     'Először a meglévő rendszer felmérése',
     'A csere nem technológiaválasztással kezdődik. A régi műtárgy állapota, mélysége és a '
     'bekötővezeték nyomvonala határozza meg, mi telepíthető a helyére és milyen földmunkával.',
     'a régi rendszer megszüntetése engedélyezési kérdés is'),
    ('Kis vagy nehezen szikkasztó telek',
     'Aktív biológiai rendszer vagy zárt tároló',
     'A tisztítómező területigénye itt a szűk keresztmetszet. Ha nincs rá hely, az oldómedencés '
     'irány kiesik — nem műszaki preferenciából, hanem geometriából.',
     'ha a kezelt víz sem helyezhető el, a zárt tároló marad'),
    ('Magas vagy erősen ingadozó talajvíz',
     'Előbb talajvíz-vizsgálat, csak utána technológia',
     'A mértékadó talajvízszint a beépítést és a vízelhelyezést egyaránt érinti. Ez nem '
     'feltétlenül kizáró ok, de külön műszaki kialakítást igényelhet.',
     'a döntéshez mérés kell, nem becslés'),
    ('Nincs villamos energia a telken',
     'Oldómedencés irány vagy zárt tároló',
     'Az aktív biológiai rendszer folyamatos áramellátást igényel. Áram nélkül ez az irány '
     'kiesik, függetlenül minden más adottságtól.',
     'ideiglenes áramellátás nem elég a folyamatos üzemhez'),
    ('Panzió, étterem, intézmény, kemping',
     'Méretezett rendszer, nem házi berendezés',
     'Itt a csúcsterhelés és a szennyvíz összetétele dönt, nem a létszám önmagában. '
     'A technológia a méretezés után következik.',
     'konyhai szennyvíznél előkezelés is kell'),
    ('Nem kommunális, ipari vagy technológiai szennyvíz',
     'Laboratóriumi vizsgálat, szakértői út',
     'A biológiai tisztítás kommunális szennyvízre való. Eltérő összetételnél a standard '
     'ajánlati út megszakad, és vizsgálat dönt.',
     'ez nem online eldönthető kérdés'),
    ('A közcsatorna kiépítése belátható időn belül várható',
     'Először a fejlesztési ütemterv ellenőrzése',
     'Ha a bekötés ütemezett és a dátum ismert, egy párhuzamos beruházás nehezen indokolható. '
     'Ígéret és ütemterv azonban nem ugyanaz.',
     'kérjen kötelező érvényű időpontot az önkormányzattól'),
]

# ================================================================ 3. kizárás
KAPUK = [
    ('Kizárt',
     'Van olyan feltétel, ami az adott megoldást jogilag vagy műszakilag kizárja. '
     'Ilyenkor nincs konfiguráció, amivel megoldható lenne.'),
    ('Csak külön feltételekkel',
     'A megoldás megvalósítható, de eltérő műszaki kialakítást igényel — például '
     'átemelőt, betonmedencés beépítést vagy nagyobb tisztítómezőt.'),
    ('További adat szükséges',
     'A rendelkezésre álló információból nem dönthető el. Jellemzően talajvíz-, '
     'talaj- vagy vízelhelyezési adat hiányzik.'),
    ('Szakértői vizsgálat kell',
     'A helyzet túlmutat a standard eseteken: nem kommunális szennyvíz, nagyobb '
     'kapacitás vagy összetett telekhelyzet.'),
    ('Más megoldás vizsgálandó',
     'Az adott irány nem alkalmas, de van másik. Ezt megmondjuk akkor is, ha a '
     'másik nem a mi rendszerünk.'),
]


def epit_osszehasonlitas():
    fejek = ['Szempont', 'Zárt tároló', 'Oldómedencés rendszer', 'Aktív biológiai']
    ths = '\n'.join(f'              <th scope="col">{h}</th>' for h in fejek[1:])
    sorok = '\n'.join(
        f'''            <tr>
              <th scope="row" class="type-ui-subtitle">{d[0]}</th>
              <td class="type-ui-subtitle">{d[1]}</td>
              <td class="type-ui-subtitle">{d[2]}</td>
              <td class="type-ui-subtitle">{d[3]}</td>
            </tr>''' for d in DIMENZIOK)

    tabla = f'''
  <section class="section" aria-labelledby="tabla-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Szempontok</p>
        <h2 class="type-display-section-title section-title" id="tabla-cim">
          Ugyanazok a kérdések mindhárom megoldáshoz
        </h2>
        <p class="type-ui-body section-lead">
          A sorok nem tulajdonságok, hanem döntési szempontok. Egy megoldás akkor jön szóba,
          ha minden sorban teljesíthető, amit az Ön ingatlana megkíván.
        </p>
      </header>
      <div class="compare-scroll" role="region" aria-labelledby="tabla-cim" tabindex="0">
        <table class="compare-table">
          <thead>
            <tr>
              <th scope="col">Szempont</th>
{ths}
            </tr>
          </thead>
          <tbody>
{sorok}
          </tbody>
        </table>
      </div>
      {adathiany('energiafogyasztás modellenként, valós karbantartási ciklus, iszapzsák-kezelési gyakoriság, EPURECO ürítési intervallum, technológiánkénti tényleges telek- és szikkasztóigény.', 'technológus által jóváhagyott összehasonlító adatlap')}
    </div>
  </section>
'''

    return [
        sec_prose('Mi alapján hasonlítunk', 'Nem az előnylisták hossza dönt', [
            'Három megoldástípus áll szemben egymással, és a legfontosabb különbség köztük nem '
            'egy tulajdonság, hanem a <strong>funkció</strong>: az egyik gyűjti a szennyvizet, a '
            'másik előkezeli és a talajra bízza a tisztítás nagy részét, a harmadik energiabevitellel '
            'ténylegesen megtisztítja.',
            'Ezért nem lehet őket egyetlen sorrendbe állítani. Az összehasonlítás akkor hasznos, ha '
            'ugyanazokat a kérdéseket teszi fel mindháromnak — és a válaszból az derül ki, melyiknek '
            'a feltételeit tudja teljesíteni az adott ingatlan.',
            JOGI + '\n      A hatályos szabályozás is külön fogalomként kezeli a három megoldást; '
            'a besorolás nem marketingkérdés, hanem jogi kategória.']),
        tabla,
        sec_numbered('Költség', 'Költségkategóriák — konkrét ár nélkül',
                     'Végleges árat felmérés nélkül nem lehet felelősen mondani. Az alábbi '
                     'kategóriák viszont mindhárom megoldásnál összevethetők.',
                     ['<strong>Beruházás.</strong> A berendezés ára ritkán a legnagyobb tétel; a '
                      'földmunka, a bekötés mélysége és a kezelt víz elhelyezése mozgatja a végösszeget.',
                      '<strong>Energia.</strong> Az aktív rendszernél folyamatos áramfogyasztás, a '
                      'másik kettőnél nincs.',
                      '<strong>Elszállítás.</strong> Zárt tárolónál a teljes szennyvízmennyiség '
                      'rendszeres szippantása; a másik kettőnél időszakos iszapkezelés.',
                      '<strong>Adalékanyag.</strong> Ahol a forgalmazó előírja, ez visszatérő tétel.',
                      '<strong>Karbantartás és kopó alkatrész.</strong> Az aktív rendszernél '
                      'kompresszor és membrán; a passzív megoldásoknál nincs mozgó alkatrész.']),
        sec_cta('Következő lépés', 'Melyik illik az Ön helyzetéhez?',
                ['A táblázat megmutatja a különbségeket, de a döntést a saját ingatlana adottságai '
                 'hozzák meg. A következő oldal tipikus helyzetekből indul, nem technológiából.'],
                'Melyik megoldás mikor megfelelő?', 'melyik-megoldas-mikor-megfelelo',
                alt=('Vagy nézze meg, mi zárhat ki egy megoldást', 'kizaro-es-korlatozo-feltetelek')),
    ]


def epit_mikor():
    kartyak = '\n'.join(f'''        <li class="situation">
          <h3 class="type-ui-card-title situation-title">{h}</h3>
          <p class="type-ui-body-strong helyzet-irany">{irany}</p>
          <p class="type-ui-body situation-text">{miert}</p>
          <p class="type-ui-caption helyzet-kizar"><strong>Ami módosíthatja:</strong> {kizar}</p>
        </li>''' for h, irany, miert, kizar in HELYZETEK)

    return [
        sec_prose('Hogyan olvassa', 'Vizsgálati irány, nem termékajánlás', [
            'Az alábbi helyzetek nem termék-hozzárendelések. Mindegyiknél az szerepel, melyik '
            'irányt <strong>érdemes először megvizsgálni</strong>, és mi az, ami ezt felülírhatja.',
            'Van olyan helyzet is, ahol a következő feladat nem technológiaválasztás, hanem '
            'adatgyűjtés: közcsatorna-ellenőrzés, talajvíz-vizsgálat vagy laboradat beszerzése.']),
        f'''
  <section class="section" aria-labelledby="helyzetek-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Helyzetek</p>
        <h2 class="type-display-section-title section-title" id="helyzetek-cim">
          Kilenc tipikus helyzet, és hogy melyikben mit érdemes először megnézni
        </h2>
      </header>
      <ul class="situation-grid" data-cols="3" role="list">
{kartyak}
      </ul>
      {adathiany('az értékesítési döntési gyakorlat, az elutasított projektek és az átirányítások mintázata; milyen telekhelyzet és használati profil változtatja meg a választást.', 'ÖkoTech belső projektnyilvántartás')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'Van olyan feltétel, ami kizárja?',
                ['Mielőtt egy irány mellett dönt, érdemes megnézni a kizáró és korlátozó '
                 'feltételeket. Van, amit jogszabály zár ki, van, ami csak eltérő műszaki '
                 'kialakítást igényel — a kettő nem ugyanaz.'],
                'Kizáró és korlátozó feltételek', 'kizaro-es-korlatozo-feltetelek',
                alt=('Vagy szűrje elő a saját helyzetét', 'megoldastipus-eloszuro')),
    ]


def epit_kizaras():
    kat = '\n'.join(f'''        <li class="card">
          <h3 class="type-ui-card-title card-title">{c}</h3>
          <p class="type-ui-body card-text">{t}</p>
        </li>''' for c, t in KAPUK)

    return [
        sec_prose('Miért van külön oldala', 'A „nem" is válasz — és időben jobb', [
            'Ez az oldal azért van, hogy a rossz döntés és a fölösleges ajánlatkérés elkerülhető '
            'legyen. Három dolgot élesen elválasztunk egymástól: mi a <strong>jogi kapu</strong>, '
            'mi a <strong>termékspecifikus korlát</strong>, és mi az, ami csak eltérő műszaki '
            'kialakítást igényel.',
            'Ez a különbségtétel a lényeg. Egy jogi kizárást nem lehet konfigurációval megoldani; '
            'egy mély bejövő csövet viszont igen — átemelővel.']),
        f'''
  <section class="section" aria-labelledby="kategoriak-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Eredménykategóriák</p>
        <h2 class="type-display-section-title section-title" id="kategoriak-cim">
          Ötféle válasz létezik — és csak az egyik jelenti azt, hogy „nem"
        </h2>
      </header>
      <ul class="numbered-grid" role="list">
{kat}
      </ul>
    </div>
  </section>
''',
        sec_split('Jogi és műszaki', 'Mi zárja ki, és mi csak módosítja',
                  'Jogi vagy területi kapu — ezen nem lehet átkonfigurálni',
                  ['<strong>a közcsatorna műszakilag elérhető</strong> az ingatlant határoló '
                   'közterületen, és a tisztítótelepi kapacitás is megvan;',
                   '<strong>vízbázisvédelmi vagy fokozottan érzékeny terület</strong>, ahol külön '
                   'feltétel vagy települési program vonatkozik a telepítésre;',
                   '<strong>a projekt kapacitási kategóriája</strong> más eljárást kíván;',
                   '<strong>nem kommunális szennyvíz</strong> — a standard út itt megszakad, '
                   'és vizsgálat dönt.'],
                  'Műszaki vagy használati korlát — konfigurációval kezelhető lehet',
                  ['<strong>túl mély bejövő cső</strong> — átemelő beépítése oldhatja meg;',
                   '<strong>magas talajvíz</strong> — eltérő beépítési mód jöhet szóba;',
                   '<strong>kevés terület a tisztítómezőnek</strong> — más technológia felé mutat;',
                   '<strong>nincs folyamatos áram</strong> — az aktív irányt zárja ki, a passzívat nem;',
                   '<strong>hosszú, terhelés nélküli szakaszok</strong> — a technológiaválasztást '
                   'módosítják, nem a megvalósíthatóságot;',
                   '<strong>a tulajdonos nem vállalja</strong> az előírt ellenőrzést és karbantartást.']),
        f'''
  <section class="section" aria-labelledby="jogi-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Jogi háttér</p>
        <h2 class="type-display-section-title section-title" id="jogi-cim">A jogszabályi keretről</h2>
      </header>
      {JOGI}
      <p class="type-ui-body section-lead">
        Az egyedi szennyvízkezelés jogi kereteit a vonatkozó kormányrendelet határozza meg: ez
        rögzíti a rendszerkategóriákat, a telepítési feltételeket, valamint a tulajdonost terhelő
        ellenőrzési, karbantartási és dokumentálási kötelezettségeket.
      </p>
      <p class="type-ui-body section-lead">
        A konkrét hivatkozásokat és a jelenleg hatályos szöveget publikálás előtt minden esetben
        ellenőrizni kell, mert a szabályozás és a hatósági gyakorlat is változhat. Az Ön
        településén érvényes feltételeket az illetékes hatóságnál érdemes tisztázni.
      </p>
      {adathiany('a hatályos jogszabályhelyek pontos megjelölése, a helyi engedélyezési gyakorlat és a vízbázisvédelmi besorolások.', 'jogi ellenőrzés + illetékes hatóság')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'Nézzük meg az Ön helyzetére',
                ['Az előszűrő néhány kérdés alapján megmutatja, mely irányok jöhetnek szóba, '
                 'mi esik ki, és milyen adat hiányzik még a döntéshez.',
                 'Az eredmény tájékoztató jellegű: telekalkalmasságot és engedélyezhetőséget nem '
                 'állapít meg.'],
                'Megoldástípus-előszűrő', 'megoldastipus-eloszuro',
                alt=('Vagy kérjen helyszíni felmérést', '../kapcsolat')),
    ]


def epit_eloszuro():
    return [
        sec_prose('Mit ad és mit nem', 'Vizsgálati irányt ad, nem terméket választ', [
            'Az előszűrő <strong>nem</strong> mondja meg, melyik berendezést vegye meg. Azt mutatja '
            'meg, mely megoldástípusok jöhetnek egyáltalán szóba az Ön helyzetében, melyik esik ki, '
            'és milyen adat hiányzik még a döntéshez.',
            'A kemény szabályokat — jogi kizárás, nem kommunális szennyvíz, kritikus telekhelyzet — '
            'nem bízzuk nyelvi modellre: ezek rögzített elágazások, és szükség esetén emberi '
            'megkeresésre irányítanak.']),
        sec_numbered('Amit kérdez', 'Négy szint, és mindegyik módosíthatja az irányt', None,
                     ['<strong>Alaphelyzet.</strong> Van-e közcsatorna, milyen ingatlanról van szó, '
                      'új rendszer vagy meglévő kiváltása, lakossági vagy üzleti a használat.',
                      '<strong>Használat.</strong> Állandó vagy időszakos, hány fő, mekkora a '
                      'csúcs, milyen hosszúak a szünetek.',
                      '<strong>Telek.</strong> Szabad terület, talaj, talajvíz, közeli kutak, a '
                      'kezelt víz elhelyezése, a bejövő cső mélysége, ha ismert.',
                      '<strong>Üzemeltetés.</strong> Van-e folyamatos áram, elfogadható-e a '
                      'szippantás, milyen karbantartást vállal a tulajdonos.']),
        sec_numbered('Amit ad', 'Az eredmény öt válasz egyike lehet',
                     'Minden eredményhez tartozik indoklás, ellenérv, a hiányzó adat megjelölése '
                     'és a következő feladat.',
                     ['<strong>Aktív biológiai irány vizsgálata indokolt.</strong>',
                      '<strong>Oldómedencés irány valószínűbb.</strong>',
                      '<strong>Zárt tároló vagy átmeneti megoldás is vizsgálandó.</strong>',
                      '<strong>Jelenleg nincs elég adat</strong> — ez is érvényes eredmény.',
                      '<strong>Szakértői vizsgálat szükséges.</strong>']),
        f'''
  <section class="section" aria-labelledby="modul-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">A modul</p>
        <h2 class="type-display-section-title section-title" id="modul-cim">Az előszűrő</h2>
      </header>
      <aside class="panel">
        <p class="type-ui-body"><strong>Az előszűrő még nem él.</strong> A döntési szabályokat
          — melyik válasz melyik irányt zárja ki vagy nyitja meg — a cég szakmai vezetésének kell
          jóváhagynia, mielőtt bárkinek eredményt mutatunk. Addig nem teszünk ki olyan felületet,
          amely döntést sugall.</p>
        <p class="type-ui-body">Amíg elkészül, a <a href="../#ai-dontestamogato">döntéstámogató
          modul</a> ad nagyságrendi eligazítást, vagy írjon nekünk, és átvesszük Önnel.</p>
      </aside>
      {adathiany('a teljes megoldásválasztási döntési fa; az A.B. Clear és az EPURECO alkalmassági és kizárási szabályai; a zárt tároló javaslati helyzetei; a távollét és a szezonalitás pontos határai; mikor kötelező helyszíni felmérés, jogi ellenőrzés vagy mérnöki szakértő; az 50 LE feletti átadás logikája; a nem kommunális szennyvíz eszkalációja. A szabályokat legalább 100 korábbi ajánlati eseten vissza kell tesztelni.', 'ÖkoTech szakmai vezetés + belső projektnyilvántartás')}
    </div>
  </section>
''',
        sec_cta('Addig is', 'Beszéljünk róla',
                ['Ha most szeretne eligazodni, írja le a helyzetét néhány mondatban: hol van az '
                 'ingatlan, hogyan használják, és mit tud a telekről. Megmondjuk, melyik irány '
                 'jöhet szóba — akkor is, ha a válasz az, hogy nem a mi rendszerünk.'],
                'Kapcsolatfelvétel', '../kapcsolat'),
    ]


OLDALAK = [
    dict(OSSZEHAS, sections=epit_osszehasonlitas()),
    dict(file='megoldasok/melyik-megoldas-mikor-megfelelo.html',
         url='megoldasok/melyik-megoldas-mikor-megfelelo', img='oldomedence',
         title='Melyik megoldás mikor megfelelő? — helyzet szerinti eligazítás | ÖkoTech Home',
         desc='Kilenc tipikus ingatlanhelyzet, és hogy melyikben melyik megoldástípust érdemes '
              'először megvizsgálni — a kizáró körülményekkel együtt.',
         h1='Melyik megoldás mikor megfelelő?',
         alt='Talajmetszet egy erdőszéli ház előtt: oldómedence és kavicsos elszivárogtató mező',
         lead='A technológiai különbségeket ismerve a következő kérdés az, hogyan alkalmazhatók a '
              'saját helyzetére. Ez az oldal helyzetekből indul, nem termékekből — és van, ahol a '
              'válasz az, hogy előbb adatot kell gyűjteni.',
         crumbs=[('Főoldal', '../'), ('Megoldások', './')],
         sections=epit_mikor()),
    dict(file='megoldasok/kizaro-es-korlatozo-feltetelek.html',
         url='megoldasok/kizaro-es-korlatozo-feltetelek', img='alternativak',
         title='Kizáró és korlátozó feltételek — mikor nem telepíthető | ÖkoTech Home',
         desc='Mi zár ki jogilag egy megoldást, mi csak eltérő műszaki kialakítást igényel, és '
              'mikor kell további adat vagy szakértői vizsgálat.',
         h1='Kizáró és korlátozó feltételek',
         alt='Talajmetszet zárt betontárolóval egy vidéki ingatlan mellett, a bekötőúton '
             'szippantóautóval',
         lead='Nem minden ingatlanon telepíthető minden megoldás. Van, amit jogszabály zár ki, van, '
              'ami csak más műszaki kialakítást igényel, és van, ami csak további adatot kíván. '
              'A háromnak nem ugyanaz a következménye.',
         crumbs=[('Főoldal', '../'), ('Megoldások', './')],
         sections=epit_kizaras()),
    dict(file='megoldasok/megoldastipus-eloszuro.html',
         url='megoldasok/megoldastipus-eloszuro', img='biologiai',
         title='Megoldástípus-előszűrő — mely irányok jöhetnek szóba | ÖkoTech Home',
         desc='Néhány kérdés alapján megmutatja, mely megoldástípusok jöhetnek szóba az Ön '
              'ingatlanán, melyik esik ki, és milyen adat hiányzik még a döntéshez.',
         h1='Megoldástípus-előszűrő',
         alt='Talajmetszet egy családi ház kertje alatt: hengeres biológiai tisztítótartály '
             'belső terekkel és aknafedlapokkal',
         lead='Az általános döntési tudás akkor ér valamit, ha a saját ingatlanára alkalmazza. '
              'Ez az eszköz nem terméket ajánl, hanem leszűkíti a reálisan szóba jövő irányokat — '
              'és megmondja, mi hiányzik még a döntéshez.',
         crumbs=[('Főoldal', '../'), ('Megoldások', './')],
         sections=epit_eloszuro()),
]

if __name__ == '__main__':
    for o in OLDALAK:
        out = WEB / o['file']
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:52s} {len(out.read_text(encoding='utf-8'))//1024} KB")
