#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Előkészítés → Telekalkalmasság — hub és a brief szerinti kilenc aloldal.

A brief HÁROM ponton kifejezetten felülírja a jelenlegi ÖkoTech-kommunikációt:

1. „Nem feltétlenül szükséges helyszíni felmérés — elég, ha tudja a telek
   adatait." Ez önmagában félrevezető: attól függ, MELYIK adatot ismeri, és
   milyen minőségben. Helyette adatminőségi feltétel kell — becsült, dokumentált
   vagy mért —, és ehhez kötött továbblépés.

2. A tartály telepíthetősége és a tisztított víz elhelyezhetősége KÉT KÜLÖN
   döntés, sőt a második maga is kettéválik műszaki és jogi kérdésre. Magas
   talajvíznél a tartály rögzíthető lehet, ettől a szikkasztás még nem válik
   megfelelővé. A jelenlegi tartalom ezt egybemossa.

3. Az eredmény ne „alkalmas / nem alkalmas" legyen, hanem négy állapot:
   standard · feltételes · vizsgálandó · jelenleg nem igazolt.

AMIT EZ AZ OLDALCSOPORT SZÁNDÉKOSAN NEM KÖZÖL:
 · egyetlen univerzális védőtávolságot a kúttól — az a kút típusától, jogi
   státuszától, a vízbázisvédelmi helyzettől és a tényleges elhelyezési ponttól
   függ, tehát egy szám itt megtévesztő lenne;
 · univerzális minimális telekméretet — technológiánként, terhelésenként és
   talajonként más;
 · konkrét szikkasztó-méretezési darabszámot — a jelenlegi cikkek számai csak
   belső műszaki validálás után publikálhatók (lásd `hiany()` megjegyzések);
 · árat, engedélyezhetőségi ígéretet, garantált méretezést mérés nélkül.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import (sec_numbered, sec_split, sec_prose, sec_situations,
                    sec_cta, sec_faq)

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

JOGI = ('<!-- JOGI ELLENŐRZÉS PUBLIKÁLÁS ELŐTT. Érintett: 147/2010. Korm. rendelet ·\n'
        '     27/2004. KvVM rendelet érzékenységi besorolása (mellékletét 2026-ban is\n'
        '     módosították) · 123/1997. Korm. rendelet a vízbázisok védőterületeiről ·\n'
        '     219/2004. Korm. rendelet a felszín alatti vizek védelméről · helyi HÉSZ.\n'
        '     Mind gyorsan avuló tartalom, dátumozott felülvizsgálat kell hozzá. -->')


def hiany(mi, honnan):
    return (f'<!-- ADATHIÁNY: {mi}\n'
            f'     Forrás: {honnan}. Addig konkrét értékkel nem publikálható. -->')


HOME = ('Főoldal', '../')
ELO = ('Előkészítés', './')
CRUMB = [HOME, ELO]
HUB = [HOME, ELO, ('Telekalkalmasság', 'telekalkalmassag')]


# ===========================================================================
# HUB — Telekalkalmasság
# ===========================================================================
def epit_hub():
    return [
        sec_prose('Miről dönt ez a szakasz', 'A telekalkalmasság nem egyetlen adat', [
            'Egy szennyvíztisztító rendszer telekalkalmassága nem egyetlen kérdésre adott '
            'válasz. A talaj, a talajvíz, a rendelkezésre álló terület, a házból érkező '
            'szennyvízcső szintje, a terepviszonyok, a kút és más érzékeny objektumok, '
            'valamint a tisztított víz elhelyezésének lehetősége <strong>együtt</strong> '
            'határozza meg, hogy mi valósítható meg a telken — és milyen kialakítással.',
            'A 147/2010. Korm. rendelet maga is előírja, hogy az oldómedencés és az egyedi '
            'biológiai rendszereket a talaj adottságainak, a felszín alatti víz mélységének '
            'és a szennyvízmennyiségnek a figyelembevételével kell méretezni. Magas '
            'talajvízállású és fokozottan érzékeny területeken további feltételek '
            'érvényesek. Ezért nem elég egyetlen adatot ismerni.',
            'Ez a szakasz nem terméket ajánl. A célja az, hogy végigvezesse a kritikus '
            'telekfeltételeken, megmutassa, melyik adatot honnan szerezheti meg, és a '
            'végén látható legyen, hol tart: elegendő-e a meglévő adat az előszűréshez, '
            'vagy mérés, illetve szakértői vizsgálat szükséges.',
        ]),

        sec_split('Két külön döntés', 'A tartály elfér — a víznek is kell hová mennie',
                  'A tartály telepíthetősége',
                  ['A berendezés fizikai elhelyezése a telken',
                   'Elegendő hely a tartálynak és a gépészetnek',
                   'A szennyvízcső szintje és a fogadószint viszonya',
                   'Talajvíznél külön szerkezeti megoldás — rögzítés, betonmedence',
                   'Munkagép behajtása és a tartály beemelése',
                   'Későbbi szervizhozzáférés'],
                  'A tisztított víz elhelyezése',
                  ['Hová kerül a naponta kilépő vízmennyiség',
                   'A talaj MÉRT vízbefogadó képessége, nem a neve',
                   'A szezonálisan legmagasabb talajvízállás',
                   'A szikkasztó helyigénye a terhelés függvényében',
                   'Kút, vízbázisvédelem, területi érzékenységi besorolás',
                   'Ahol a talajba szikkasztás nem megfelelő: más elhelyezési irány']),

        sec_prose('Miért fontos ez a különbségtétel', 'A második kérdés a nehezebb', [
            'A leggyakoribb félreértés az, hogy a két kérdést egynek nézik. Attól, hogy a '
            'tartály magasabb talajvíznél is biztonságosan rögzíthető — az ÖkoTech ilyenkor '
            'a műanyag tartály köré betonmedencés kialakítást alkalmaz —, még nem '
            'következik, hogy ugyanazon a telken a tisztított víz talajba szikkasztása is '
            'megfelelő.',
            'A vízelhelyezés ráadásul maga is két kérdés: <strong>műszakilag</strong> '
            'lehetséges-e (befogadja-e a talaj a napi vízmennyiséget), és '
            '<strong>jogilag, környezetvédelmi szempontból</strong> alkalmazható-e az adott '
            'helyen. Bármelyik megállíthatja vagy módosíthatja a projektet.',
            'A gyakorlati következmény: ha a vízelhelyezés iránya nincs tisztázva, a projekt '
            'nem ajánlatkész — akkor sem, ha a tartály helye már megvan.',
        ]),

        sec_situations(
            'A vizsgálandó tényezők', 'Mi határozza meg a telek alkalmasságát?',
            'Hét témakör, mindegyik önálló oldalon. A sorrend nem kötelező, de van logikája: '
            'a talaj és a talajvíz a legtöbb továbbit befolyásolja, a hozzáférés pedig a '
            'legkésőbb derül ki, ha nem nézik meg időben.',
            [
                ('nav-talaj', 'Talaj és szivárgóképesség',
                 'A talaj neve — homokos, agyagos — önmagában nem méretezési adat. '
                 'A kérdés az, milyen sebességgel képes a helyszíni talaj a vizet befogadni.',
                 'talaj-es-szivargokepesseg', 'Talaj és szivárgás'),
                ('nav-vizelvezetes', 'Talajvíz',
                 'Nem a mai vízállás számít, hanem a szezonálisan előforduló legmagasabb. '
                 'A tartály rögzítése és a szikkasztás két külön kérdés.',
                 'talajviz', 'Talajvíz'),
                ('nav-vizminoseg', 'Kút és védőtávolság',
                 'A zárt tartály és az a pont, ahol a víz ténylegesen a talajba kerül, '
                 'vízvédelmi szempontból nem ugyanaz az objektum.',
                 'kut-es-vedotavolsag', 'Kút és védelem'),
                ('telek', 'Telekméret és rendelkezésre álló terület',
                 'Nem a telek négyzetmétere a kérdés, hanem a ház, kút, behajtó és '
                 'közművek után ténylegesen használható terület.',
                 'telekmeret-es-szabad-terulet', 'Telekméret'),
                ('nav-telepites', 'Lejtés és csőmélység',
                 'A házból kilépő cső magassága meghatározza, milyen mélyre kerülhet a '
                 'berendezés befolyója — és hogy kell-e átemelő.',
                 'lejtes-es-csomelyseg', 'Lejtés és csőmélység'),
                ('nav-felmeres', 'Járműterhelés és hozzáférés',
                 'A tartály fölött nem vezethető gépjárműforgalom külön kialakítás nélkül, '
                 'és a rendszernek később is hozzáférhetőnek kell maradnia.',
                 'jarmuterheles-es-hozzaferes', 'Terhelés és hozzáférés'),
                ('nav-adatbazis', 'Hogyan gyűjtsem össze az adatokat?',
                 'Adatforrásonként: honnan szerezhető meg, ki tudja megadni, és melyiknél '
                 'nem elegendő a becslés.',
                 'telekadatok-osszegyujtese', 'Adatgyűjtés'),
            ]),

        sec_numbered('Négy lehetséges állapot', 'Nem „alkalmas" vagy „nem alkalmas"',
                     'A telekalkalmasság ritkán bináris. A vizsgálat végén ezek '
                     'valamelyikébe sorolható a telek — és mindegyikhez más következő '
                     'lépés tartozik.',
                     ['<strong>Standard.</strong> Az ismert adatok alapján nincs azonosított '
                      'kritikus akadály, a szokásos kialakítás valószínű. Ez nem engedély '
                      'és nem végleges méretezés — a tervezés a szokásos úton folytatható.',
                      '<strong>Feltételes.</strong> A telepítés megvalósítható, de külön '
                      'műszaki elem szükséges: tartályrögzítés, magasítás, átemelő, '
                      'betonakna vagy nagyobb szikkasztó. Ezek a projekt költségét és '
                      'kivitelezési idejét is befolyásolják.',
                      '<strong>Vizsgálandó.</strong> Egy vagy több kritikus adat hiányzik, '
                      'vagy csak becslés áll rendelkezésre. Itt nem a telek a probléma, '
                      'hanem az adat: mérés, dokumentum vagy helyszíni felmérés zárja le.',
                      '<strong>Jelenleg nem igazolt.</strong> Az ismert körülmények alapján '
                      'a tervezett megoldás nem támasztható alá — jellemzően vízvédelmi '
                      'vagy talajvíz-okból. Ilyenkor más vízelhelyezési irány, más '
                      'technológia vagy szakértői vizsgálat következik.']),

        sec_cta('Következő lépés', 'Nézzük meg, hol tart a telekkel',
                ['Ha még nem tudja, melyik adatot kell tisztáznia, kezdje az áttekintéssel: '
                 'rövid térkép arról, mit kell megvizsgálni és milyen sorrendben.',
                 'Ha már vannak adatai, az előszűrő végigveszi őket, megmondja, mi hiányzik, '
                 'és melyik továbblépés indokolt. Nem kér kapcsolati adatot a használatához, '
                 'és nem ad engedélyezhetőségi nyilatkozatot.'],
                'Telekalkalmasság áttekintése', 'telekalkalmassag-attekintese',
                alt=('Telek- és vízelhelyezési előszűrő', 'telek-es-vizelhelyezesi-eloszuro')),

        sec_faq([
            ('Elég, ha megadom a telek adatait, vagy ki kell jönniük?',
             'Attól függ, melyik adatot ismeri és milyen minőségben. Ha a kritikus adatok — '
             'talaj, talajvíz, szabad terület, csőkilépési szint — dokumentumból vagy '
             'mérésből ismertek, sok esetben elegendő a távoli előszűrés. Ha ezek egy része '
             'csak becslés, a felmérés nem formalitás, hanem az egyetlen mód a lezárásukra. '
             'Ezt minden témakörnél külön jelezzük.'),
            ('Mi van, ha valamelyik adatot egyszerűen nem tudom?',
             'A „nem tudom” érvényes válasz, és nem jelent kizárást. Adatbeszerzési útvonal '
             'következik belőle: megmondjuk, honnan szerezhető meg, ki tudja megadni, és '
             'hogy elegendő-e hozzá dokumentum, vagy mérés kell.'),
            ('A szomszéd tapasztalata elfogadható adatnak?',
             'Előzetes jelzésnek hasznos — különösen a szezonális talajvízről —, de nem '
             'azonos értékű egy mérési eredménnyel vagy hivatalos dokumentummal. Az '
             'előszűrésben külön jelöljük, hogy egy adat becsült, dokumentált vagy mért, '
             'mert a továbblépés ettől függ.'),
            ('Magas talajvíznél eleve kizárt a rendszer?',
             'Nem. Két külön kérdésre bomlik: a tartály biztonságos telepítése és a '
             'tisztított víz elhelyezhetősége. Az elsőre gyakran van műszaki megoldás. '
             'A második viszont a talajvíz mellett vízvédelmi és területi besorolástól is '
             'függ, ezért külön vizsgálatot igényelhet.'),
            ('Kap-e engedélyt vagy hivatalos igazolást az előszűrésből?',
             'Nem. Az előszűrés műszaki tájékozódás: megmutatja, mi látszik akadálynak és '
             'milyen adat hiányzik. Engedélyezhetőségről hatóság, méretezésről jogosult '
             'tervező, hidrogeológiai kérdésről szakértő nyilatkozik.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 1) Telekalkalmasság áttekintése
# ===========================================================================
def epit_attekintes():
    return [
        sec_prose('Mire jó ez az oldal', 'Térkép, nem részletes útmutató', [
            'Ez az oldal röviden végigveszi, milyen kérdésekre kell választ találni ahhoz, '
            'hogy felelősen lehessen rendszerelhelyezést és vízelhelyezési irányt javasolni. '
            'Minden témakörnél csak annyi szerepel, hogy <em>miért számít</em>, <em>mit kell '
            'tudnia róla</em>, és <em>hová léphet tovább</em>. A részletek a saját oldalaikon '
            'vannak.',
            'A sorrend nem véletlen. Az első kérdés a közcsatorna helyzete és a telek '
            'területi besorolása, mert jogi vagy vízvédelmi körülmény már a műszaki részletek '
            'előtt befolyásolhatja, hogy egyedi rendszer egyáltalán szóba jöhet-e.',
        ]),

        sec_numbered('A vizsgálat sorrendje', 'Mit érdemes elsőként tisztázni?',
                     'Ha korlátozott ideje van, ebben a sorrendben haladjon: a korábbi '
                     'pontok a későbbiek értelmét is meghatározzák.',
                     ['<strong>Közcsatorna és jogi alaphelyzet.</strong> Van-e elérhető '
                      'közcsatorna, és milyen a település érzékenységi besorolása. Ha a telek '
                      'kijelölt vízbázisvédelmi területen fekszik, az minden továbbit '
                      'befolyásol.',
                      '<strong>Talaj és tényleges szivárgóképesség.</strong> Nem a talaj neve, '
                      'hanem a mért vízbefogadó képesség. Ez határozza meg, hogy a tisztított '
                      'víz helyben elhelyezhető-e, és mekkora felületen.',
                      '<strong>Talajvíz.</strong> A szezonálisan előforduló legmagasabb '
                      'vízállás. Külön hat a tartály telepítésére és külön a szikkasztásra.',
                      '<strong>Kút és más vízvédelmi objektum.</strong> A saját és a szomszédos '
                      'kutak helye, típusa, használata. A zárt tartály és a szikkasztó itt '
                      'külön elbírálás alá esik.',
                      '<strong>Ténylegesen szabad terület.</strong> Ami a ház, melléképület, '
                      'behajtó, közművek és fák után marad — és amit később sem építenek be.',
                      '<strong>Csőkilépési szint és tereplejtés.</strong> A házból érkező cső '
                      'magassága meghatározza a berendezés fogadószintjét; a lejtés azt, hogy '
                      'gravitációsan megoldható-e a vízvezetés.',
                      '<strong>Járműterhelés és hozzáférés.</strong> Behajtás a telepítéshez, '
                      'és tartós hozzáférés a szervizhez. Ez derül ki a legkésőbb, ha nem '
                      'nézik meg időben.']),

        sec_split('Adatminőség', 'Melyik adat becsülhető, és melyiket kell mérni?',
                  'Jellemzően elegendő dokumentumból vagy tulajdonosi ismeretből',
                  ['Cím, helyrajzi szám, telekméret — tulajdoni lap, térképmásolat',
                   'Közcsatorna helyzete — víziközmű-szolgáltató, önkormányzat',
                   'A ház helye és a szabad terület — helyszínrajz',
                   'Tereplejtés iránya — bejárás, fotó',
                   'Kút helye és használata — bejárás',
                   'Behajtási szélesség, munkagép útvonala — mérés helyben, fotó',
                   'Későbbi kert- és építési tervek — Ön tudja'],
                  'Ehhez mérés vagy dokumentált vizsgálat szükséges',
                  ['A talaj tényleges szivárgóképessége — szivárogtatási vizsgálat',
                   'Talajmechanikai rétegződés — szakvélemény',
                   'A szezonálisan legmagasabb talajvízszint — mérés vagy szakvélemény',
                   'A csőkilépés pontos folyásfenék-mélysége — terv vagy szintezés',
                   'Vízbázisvédelmi besorolás — hivatalos forrás',
                   'Kút mélysége és rétegvíz-viszonyai — kút dokumentációja',
                   'Fokozottan érzékeny területen a szikkasztás megengedettsége — hatóság']),

        sec_prose('Mit módosít, és mit állít meg', 'Nem minden probléma egyforma súlyú', [
            'A telekadottságok egy része csak a <strong>kialakítást</strong> módosítja: '
            'magasabb talajvíznél szerkezeti megoldás, mély csőkilépésnél átemelő, '
            'járműterhelésnél betonakna, gyengébb szivárgásnál nagyobb szikkasztó felület. '
            'Ezek költséget és kivitelezési időt jelentenek, nem kizárást.',
            'Más része viszont <strong>külön szakértőt</strong> igényel: bizonytalan vagy '
            'kijelölt vízbázisvédelmi helyzet, fokozottan érzékeny terület, ismeretlen '
            'rétegviszonyok, felszíni befogadóba vezetés terve. Ezekben nem a berendezés '
            'gyártója, hanem hidrogeológus, jogosult tervező vagy hatóság dönt.',
            'Az áttekintés célja pontosan ez a szétválasztás: mielőtt bárki ajánlatot ad, '
            'legyen látható, melyik kategóriába esik a telek.',
        ]),

        sec_cta('Következő lépés', 'Kezdje a legtöbbet befolyásoló adattal',
                ['A talaj tényleges szivárgóképessége és a szezonális talajvízszint a két '
                 'olyan adat, amely a legtöbb továbbit meghatározza. Ha csak egyet tud '
                 'megszerezni, ezekkel kezdje.'],
                'Talaj és szivárgóképesség', 'talaj-es-szivargokepesseg',
                alt=('Vissza a Telekalkalmasság áttekintéséhez', 'telekalkalmassag')),

        sec_faq([
            ('Meddig jutok el ezekkel az adatokkal ajánlatkérés nélkül?',
             'Az előszűrő megmondja, van-e látható műszaki vagy vízvédelmi kockázat, és mi '
             'hiányzik még. Nem ad árat, végleges modellt és engedélyezhetőségi nyilatkozatot '
             '— ezekhez ember és további adat kell.'),
            ('Mi az az érzékenységi besorolás?',
             'A települések felszín alatti víz szempontjából vett érzékenységi besorolása '
             'hivatalos jegyzékben szerepel, és befolyásolja, milyen feltételekkel helyezhető '
             'el tisztított szennyvíz a földtani közegbe. A besorolás időről időre változik, '
             'ezért mindig aktuális forrásból kell ellenőrizni.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 2) Talaj és szivárgóképesség
# ===========================================================================
def epit_talaj():
    return [
        sec_prose('A legfontosabb különbség', 'A talaj neve nem méretezési adat', [
            'A „homokos”, „agyagos” vagy „kötött” megnevezés önmagában nem elegendő egy '
            'szikkasztórendszer méretezéséhez. A lényegi kérdés az, hogy a <strong>helyszíni '
            'talaj milyen sebességgel és milyen körülmények között képes a vizet '
            'befogadni</strong> — ez a szivárgóképesség, és mérni kell, nem megnevezni.',
            'Két egymás melletti telek talaja ugyanúgy nevezhető homokosnak, miközben a '
            'rétegződésük, tömörödöttségük vagy egy közbeékelődő agyagréteg miatt egészen '
            'másképp viselkednek. A 147/2010. Korm. rendelet ezért teszi a talaj adottságait '
            'az egyedi rendszer méretezésének egyik alapfeltételévé — nem a talaj nevét.',
            'A megfelelő szivárgóképesség önmagában szintén nem elegendő: a talajvíz, a '
            'rendelkezésre álló terület, a kezelt víz mennyisége és a környezeti '
            'korlátozások együtt határozzák meg a vízelhelyezési megoldást.',
        ]),

        sec_numbered('Amit meg lehet tudni', 'Honnan származhat talajinformáció?',
                     'A források nem egyenértékűek. Az alábbi sorrend nagyjából a '
                     'megbízhatóságot is követi — alulról felfelé.',
                     ['<strong>Szomszédi vagy környékbeli tapasztalat.</strong> Hasznos '
                      'előzetes jelzés, de nem mérési adat: a rétegződés telkenként eltérhet. '
                      'Előszűrésre jó, méretezésre nem.',
                      '<strong>Korábbi földmunka megfigyelése.</strong> Alapásás, medence, '
                      'kerti gödör — sokat elmond a rétegekről, és fotóval dokumentálható. '
                      'A vízbefogadó képességet viszont nem méri.',
                      '<strong>Korábbi talajmechanikai szakvélemény.</strong> Ha az épület '
                      'tervezéséhez készült, gyakran megvan. Ellenőrizni kell a készítés '
                      'dátumát és azt, hogy a szikkasztó tervezett helyére vonatkozik-e.',
                      '<strong>Szivárogtatási vizsgálat.</strong> Ez méri közvetlenül azt, '
                      'ami a méretezéshez kell: a talaj tényleges vízbefogadó képességét, a '
                      'szikkasztó tervezett helyén és mélységében.']),

        sec_split('Mit befolyásol a talaj', 'Két külön hatás',
                  'A talaj típusa és rétegződése hat…',
                  ['A földmunka nehézségére és költségére',
                   'A munkagödör állékonyságára, a dúcolás szükségességére',
                   'A tartály körüli visszatöltés minőségére',
                   'Feltöltött talajnál a teherbírásra és a süllyedésre',
                   'Arra, hogy szükséges-e talajmechanikai szakvélemény'],
                  'A MÉRT szivárgóképesség hat…',
                  ['Arra, hogy a víz helyben elhelyezhető-e egyáltalán',
                   'A szikkasztó szükséges felületére és térfogatára',
                   'Arra, hogy elfér-e a szükséges felület a szabad területen',
                   'A hosszú távú megbízhatóságra — eliszapolódás, visszaduzzadás',
                   'Arra, hogy más vízelhelyezési irányt kell-e vizsgálni']),

        sec_prose('Amit külön kezelni kell', 'Feltöltött talaj és rétegzett talaj', [
            'A <strong>feltöltött talaj</strong> külön eset: a feltöltés anyaga, kora, '
            'tömörítettsége és vastagsága ismeretlen lehet, és a felszíni benyomás '
            'megtévesztő. Feltöltésen sem a teherbírás, sem a szivárgás nem becsülhető '
            'a talajtípus alapján — itt a vizsgálat nem opció.',
            'A <strong>rétegzett talaj</strong> szintén: jó vízáteresztő felső réteg alatt '
            'záró agyagréteg is lehet, amely a vizet megfogja. Ilyenkor a szikkasztó a '
            'tervezett mélységben egészen máshogy viselkedik, mint amit a felszín ígér. '
            'Ezért kell a vizsgálatot a tervezett szikkasztó helyén és mélységében végezni, '
            'nem a telek egy tetszőleges pontján.',
        ]),

        sec_numbered('Az eredmény', 'Négy lehetséges kimenet — nem „jó” vagy „rossz” talaj',
                     '',
                     ['<strong>Tájékoztató adat áll rendelkezésre.</strong> Van információ, '
                      'de becslés vagy régi dokumentum. Előszűrésre elég, méretezésre nem.',
                      '<strong>Mérés szükséges.</strong> A meglévő adat nem elegendő vagy nem '
                      'a szikkasztó helyére vonatkozik. Szivárogtatási vizsgálat következik.',
                      '<strong>Szivárogtatás tervezhető.</strong> A mért érték alapján a '
                      'helyben történő elhelyezés reális; a szükséges felület a napi '
                      'vízmennyiséggel együtt számolható.',
                      '<strong>Alternatív vízelhelyezés vizsgálandó.</strong> A talaj nem '
                      'fogadja be a szükséges vízmennyiséget, vagy a szükséges felület nem '
                      'fér el. Ilyenkor más elhelyezési irányt kell megvizsgálni.']),

        hiany('a szikkasztóalagút darabszáma adott terhelésre és talajra, valamint a '
              'dréncső-egyenérték',
              'ÖkoTech belső méretezési szabály + a beépített alagútmodell aktuális '
              'gyártói adatlapja. A jelenlegi cikkben szereplő számok alkalmazási feltétele, '
              'biztonsági tényezője és talajvízmélység-korlátja nincs dokumentálva'),

        sec_cta('Következő lépés', 'A talajvíz nélkül a talajadat sem elég',
                ['Jó vízbefogadó talaj sem elegendő, ha a szezonális talajvíz a szikkasztó '
                 'szintjéig felér, vagy ha vízvédelmi korlátozás áll fenn. A két adatot '
                 'együtt kell megnézni.'],
                'Talajvíz', 'talajviz',
                alt=('Telekalkalmasság áttekintése', 'telekalkalmassag-attekintese')),

        sec_faq([
            ('Elég, ha a szomszédnál jól szikkad a víz?',
             'Előzetes jelzésnek jó, de nem elég a méretezéshez. A rétegződés telken belül is '
             'változhat, és a szomszéd szikkasztója más mélységben, más terheléssel működhet. '
             'A vizsgálatot a saját telkén, a tervezett helyen és mélységben kell elvégezni.'),
            ('Mit mér pontosan a szivárogtatási vizsgálat?',
             'Azt, hogy a talaj a tervezett mélységben milyen sebességgel nyeli el a vizet. '
             'Ez az érték a napi elhelyezendő vízmennyiséggel együtt adja meg a szükséges '
             'szikkasztófelületet. Talajtípus-megnevezésből ez nem vezethető le.'),
            ('Van már talajmechanikai szakvéleményem az építkezéshez. Az elég?',
             'Sokszor jó kiindulás, de két dolgot ellenőrizni kell: mikor készült, és a telek '
             'melyik pontjára és milyen mélységre vonatkozik. Az alapozáshoz készült feltárás '
             'nem feltétlenül a szikkasztó tervezett helyén és mélységében történt.'),
            ('Agyagos talajon lehetetlen a helyi elhelyezés?',
             'Nem automatikusan, de nehezebb és nagyobb felületet igényel — és van, ahol nem '
             'oldható meg. Ezt mérés dönti el, nem a talaj megnevezése. Ha a helyi elhelyezés '
             'nem megoldható, más vízelhelyezési irányt kell vizsgálni.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 3) Talajvíz
# ===========================================================================
def epit_talajviz():
    return [
        sec_prose('Két külön kérdés', 'A tartály és a víz nem ugyanaz a probléma', [
            'Magas talajvíznél két dolgot kell külön megvizsgálni: '
            '<strong>telepíthető-e biztonságosan a tartály</strong>, és '
            '<strong>elhelyezhető-e a tisztított víz</strong> ugyanazon a helyszínen. '
            'A kettő gyakran összemosódik, pedig más a megoldásuk és más a korlátjuk.',
            'A tartály telepítése szerkezeti kérdés. Az ÖkoTech magas talajvíznél a műanyag '
            'tartály köré betonmedencés kialakítást alkalmaz, ami megakadályozza a '
            'felúszást. Ez tehát bizonyos vízállásig kezelhető külön műszaki megoldással.',
            'A víz elhelyezése viszont nem szerkezeti, hanem befogadási és jogi kérdés. '
            'A 147/2010. Korm. rendelet a magas talajvízállású és a fokozottan érzékeny '
            'területeken külön feltételeket ír elő a földtani közegbe történő bevezetésre. '
            'Attól tehát, hogy a tartály elhelyezhető, a szikkasztás még nem lesz megfelelő.',
        ]),

        sec_prose('Melyik vízszint számít?', 'Nem a mai — a szezonálisan legmagasabb', [
            'A talajvízszint az év során jelentősen változhat. Egy nyár végi mérés a '
            'legkedvezőbb állapotot mutathatja, miközben tavasszal vagy hosszabb csapadékos '
            'időszakban a víz méterekkel magasabban állhat. A méretezéshez és a telepítési '
            'döntéshez a <strong>szezonálisan előforduló legmagasabb jellemző vízállás</strong> '
            'a mértékadó.',
            'Ez a gyakorlatban azt jelenti, hogy egyetlen pillanatnyi mérés önmagában ritkán '
            'elegendő. Vagy hosszabb megfigyelés, vagy olyan dokumentum kell, amely a '
            'szezonális maximumot is tartalmazza, vagy szakértői becslés a helyi '
            'rétegviszonyok alapján.',
        ]),

        sec_numbered('Adatforrások', 'Honnan tudható meg a talajvízszint?',
                     'Alulról felfelé nő a megbízhatóság. Az első kettő előszűrésre jó, '
                     'méretezéshez a többi kell.',
                     ['<strong>Környékbeli tapasztalat.</strong> Pince beázása, tavaszi '
                      'vízállás a kertben, korábbi földmunka. Jelzésértékű, és sokszor ez az '
                      'egyetlen, ami rögtön rendelkezésre áll.',
                      '<strong>Saját megfigyelés.</strong> Ásott kút vízszintje, korábbi '
                      'gödör vízbetörése, a kert vízállásos foltjai. Érdemes dátumozni és '
                      'fotózni — a megfigyelés időpontja itt legalább annyit ér, mint maga '
                      'az adat.',
                      '<strong>Kút dokumentációja.</strong> Fúrt kútnál a rétegsor és a '
                      'nyugalmi vízszint szerepelhet benne. Figyelni kell, hogy talajvízről '
                      'vagy mélyebb rétegvízről szól-e — a kettő nem ugyanaz.',
                      '<strong>Talajmechanikai vagy hidrogeológiai szakvélemény.</strong> '
                      'Ez ad mérési adatot és értelmezést is. Bizonytalan helyzetben, '
                      'fokozottan érzékeny területen vagy vízbázisvédelmi közelségben '
                      'ez az egyetlen elfogadható forrás.']),

        sec_split('Mire hat a talajvíz', 'Ugyanaz az adat, két külön következmény',
                  'A tartály telepítésére',
                  ['Felúszási kockázat üres vagy részben töltött tartálynál',
                   'Betonmedencés vagy más rögzítéses kialakítás szükségessége',
                   'A munkagödör víztelenítése a kivitelezés alatt',
                   'A gödör állékonysága, dúcolás',
                   'Többlet földmunka és többletköltség',
                   'A telepítés időzítése — szárazabb időszak'],
                  'A tisztított víz elhelyezésére',
                  ['A szikkasztó és a talajvíz közötti szükséges távolság',
                   'A talaj tényleges befogadóképessége magas vízállásnál',
                   'A 147/2010. szerinti külön feltételek magas talajvízállású területen',
                   'Fokozottan érzékeny területen a szikkasztás megengedettsége',
                   'Az esetleg szükséges más vízelhelyezési irány',
                   'Hidrogeológiai vagy hatósági ellenőrzés szükségessége']),

        hiany('az ÖkoTech által vállalt maximális talajvízszint a standard, illetve a '
              'betonmedencés kialakításnál — méterben, terepszinthez viszonyítva',
              'ÖkoTech műszaki csapat + a betonmedencés kialakítás aktuális műszaki terve. '
              'Enélkül a látogató nem tudja megítélni, az ő esete melyik kategóriába esik'),

        sec_numbered('Az eredmény', 'Négy lehetséges kimenet', '',
                     ['<strong>Normál telepítés.</strong> A talajvíz a tartály és a szikkasztó '
                      'szintje alatt marad a szezonális maximumon is. A szokásos kialakítás '
                      'valószínű.',
                      '<strong>Külön tartályrögzítés vagy magasítás vizsgálandó.</strong> '
                      'A tartály elhelyezhető, de szerkezeti megoldással. Ez a projekt '
                      'költségét és kivitelezési idejét is befolyásolja.',
                      '<strong>A vízelhelyezés külön vizsgálandó.</strong> A tartály '
                      'kérdése rendezhető, de a szikkasztás megfelelősége nem igazolt. '
                      'Szivárogtatási vizsgálat, esetleg más elhelyezési irány következik.',
                      '<strong>Szakértői vagy hatósági ellenőrzés szükséges.</strong> '
                      'Fokozottan érzékeny terület, vízbázisvédelmi közelség vagy ismeretlen '
                      'rétegviszonyok esetén hidrogeológus, illetve hatóság dönt.']),

        sec_cta('Következő lépés', 'Ha van kút a telken, az külön kérdés',
                ['A kút jelenléte nem zárja ki a rendszert, de a zárt tartály és a szikkasztó '
                 'vízvédelmi szempontból külön elbírálás alá esik. Egyetlen univerzális '
                 'védőtávolság nem adható meg — a következő oldal megmutatja, mi határozza meg.'],
                'Kút és védőtávolság', 'kut-es-vedotavolsag',
                alt=('Telekalkalmasság áttekintése', 'telekalkalmassag-attekintese')),

        sec_faq([
            ('Tavasszal a kertben megáll a víz. Ez magas talajvizet jelent?',
             'Jelzés, de nem bizonyíték. A felszínen megálló víz származhat záró agyagrétegből, '
             'rossz felszíni vízelvezetésből vagy tömörödött talajból is, nem feltétlenül a '
             'talajvízszintből. Ugyanakkor pontosan az a fajta megfigyelés, amit érdemes '
             'jelezni — dátummal és fotóval —, mert vizsgálatot indokol.'),
            ('Ha a tartály rögzíthető, akkor a víz is elszikkasztható?',
             'Nem következik egyikből a másik. A rögzítés szerkezeti megoldás a felúszás ellen. '
             'A szikkasztás megfelelősége viszont attól függ, befogadja-e a talaj a napi '
             'vízmennyiséget a magas vízállás mellett is, és hogy a terület besorolása '
             'megengedi-e. Ez a két legfontosabb külön kérdés.'),
            ('Nem tudom a talajvízszintet. Ez kizárja a projektet?',
             'Nem. Ez „vizsgálandó” állapot, nem elutasítás. Az adat megszerezhető: kút '
             'dokumentációjából, korábbi szakvéleményből, megfigyeléssel vagy szakértői '
             'méréssel. Az előszűrő megmutatja, melyik út a legrövidebb az Ön esetében.'),
            ('Mit jelent a fokozottan érzékeny terület?',
             'A települések felszín alatti víz szempontjából vett érzékenységi besorolása '
             'hivatalos jegyzékben szerepel, és a fokozottan érzékeny kategóriában szigorúbb '
             'feltételek vonatkoznak a tisztított szennyvíz földtani közegbe juttatására. '
             'A besorolás időről időre módosul, ezért mindig aktuális forrásból kell '
             'ellenőrizni.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 4) Kút és védőtávolság
# ===========================================================================
def epit_kut():
    return [
        sec_prose('Az első tisztázandó', 'A tartály és a szikkasztó két külön objektum', [
            'Vízvédelmi szempontból nem ugyanaz a <strong>zárt szennyvíztisztító '
            'tartály</strong> helye és az a pont, ahol a tisztított vagy előkezelt víz '
            '<strong>ténylegesen a talajba kerül</strong>. A tartály zárt szerkezet; a '
            'szikkasztó viszont pontosan az az objektum, ahol a víz a földtani közegbe jut. '
            'A kúttal kapcsolatos kérdés elsősorban az utóbbira vonatkozik.',
            'Ez a különbségtétel az ÖkoTech jelenlegi tájékoztatásában is megjelenik, és '
            'helyes kiindulás. Nem következik belőle azonban, hogy bármely kúttípus és '
            'bármely területi besorolás mellett ugyanaz érvényes.',
        ]),

        sec_prose('Miért nem adunk egyetlen számot', 'A „hány méterre?” kérdésre nincs '
                                                     'univerzális válasz', [
            'Kézenfekvő lenne egyetlen védőtávolságot megadni. Az viszont megtévesztő lenne, '
            'mert a válasz több körülménytől függ egyszerre: a kút <strong>típusától</strong> '
            '(ásott, fúrt, mélységi), <strong>jogi státuszától</strong>, a '
            '<strong>vízbázisvédelmi helyzettől</strong>, a felszín alatti víz '
            '<strong>áramlási irányától</strong>, a talajvízszinttől és a tényleges '
            'vízelhelyezési pont helyétől.',
            'A 147/2010. Korm. rendelet a fokozottan érzékeny területeknél kifejezetten a '
            'vízbázisvédelmi szabályokhoz köti a tisztított szennyvíz szikkasztásának '
            'lehetőségét, a 123/1997. Korm. rendelet pedig a vízbázisokhoz védőidomokat és '
            'védőövezeteket rendel. Ezek nem egyetlen méterszámot jelentenek, hanem '
            'helyfüggő geometriát.',
            'Ha valaki egyetlen általános számot mond, az vagy egy konkrét helyzetre '
            'vonatkozik, vagy nem elég pontos. Ezért itt inkább azt mutatjuk meg, milyen '
            'adatokból áll össze a válasz.',
        ]),

        sec_numbered('Amit meg kell adni', 'Milyen adat kell a kútról?',
                     'Minél több ismert ezekből, annál kevesebb szakértői kör szükséges. '
                     'A saját és a szomszédos kutakat is számba kell venni.',
                     ['<strong>A kút típusa.</strong> Ásott, fúrt vagy mélységi. Az ásott kút '
                      'jellemzően a talajvizet csapolja meg, a mélyebb fúrt kút más '
                      'vízadó réteget — a kockázati kép ezért eltérő.',
                      '<strong>Használata.</strong> Ivóvíz, öntözés, állatitatás vagy nem '
                      'használt. Az ivóvízcélú használat lényegesen szigorúbb megítélés alá '
                      'esik.',
                      '<strong>Pontos helye.</strong> A telekhatárhoz és a tervezett '
                      'szikkasztóhoz viszonyítva, helyszínrajzon megjelölve. A szomszédos '
                      'telkek kútjait is beleértve.',
                      '<strong>Mélysége és rétegsora, ha ismert.</strong> Fúrt kútnál a '
                      'kútdokumentáció tartalmazhatja. Ebből derül ki, melyik vízadó réteget '
                      'érinti.',
                      '<strong>Dokumentáció és jogi státusz.</strong> Van-e engedélye vagy '
                      'bejelentése. Ez nem a szennyvízprojekt kérdése, de a szakértői '
                      'megítélést befolyásolja.',
                      '<strong>Kijelölt vízbázisvédelmi terület.</strong> Érint-e a telket '
                      'védőidom vagy védőövezet. Ezt hivatalos forrásból kell ellenőrizni, '
                      'nem becsülni.']),

        sec_numbered('Az eredmény', 'Négy lehetséges kimenet', '',
                     ['<strong>Nincs nyilvánvaló konfliktus.</strong> Az ismert adatok alapján '
                      'a tervezett elrendezés nem ütközik látható akadályba. Ez nem hatósági '
                      'igazolás, hanem előszűrési eredmény.',
                      '<strong>További kútadat szükséges.</strong> A kút típusa, mélysége vagy '
                      'dokumentációja hiányzik. Ezek nélkül a megítélés nem megalapozott.',
                      '<strong>Vízbázisvédelmi ellenőrzés szükséges.</strong> A telek '
                      'kijelölt védőterületet érinthet, vagy a besorolás bizonytalan. '
                      'Hivatalos forrásból kell tisztázni a szikkasztás megengedettségét.',
                      '<strong>A szikkasztó helyét módosítani kell.</strong> Az elrendezés '
                      'átalakítható úgy, hogy az elhelyezési pont távolabb, más irányba vagy '
                      'a felszín alatti víz áramlásához képest kedvezőbb helyzetbe kerüljön.']),

        hiany('az ÖkoTech saját belső ellenőrzési eljárása kút esetén: milyen adatot kér, '
              'mikor módosítja a szikkasztó helyét, mikor küldi hidrogeológushoz, és volt-e '
              'kút vagy vízbázis miatt elutasított projekt',
              'ÖkoTech műszaki és értékesítési csapat. A publikus tartalom nem előzheti meg '
              'a belső szabályt'),

        sec_cta('Következő lépés', 'Ha a szikkasztót át kell helyezni, kell hozzá hely',
                ['A kút miatti áthelyezés csak akkor megoldás, ha van hová. A következő oldal '
                 'a ténylegesen szabad területről szól — arról, ami a ház, a behajtó és a '
                 'közművek után marad.'],
                'Telekméret és rendelkezésre álló terület', 'telekmeret-es-szabad-terulet',
                alt=('Telekalkalmasság áttekintése', 'telekalkalmassag-attekintese')),

        sec_faq([
            ('A kút miatt eleve nem telepíthető a rendszer?',
             'Önmagában nem. A zárt tartály és a tisztított víz elhelyezési pontja külön '
             'objektum, és jellemzően az utóbbi elhelyezése az érdemi kérdés. A megítéléshez '
             'viszont ismerni kell a kút típusát, használatát, helyét és a terület '
             'vízbázisvédelmi helyzetét.'),
            ('Miért nem mondják meg, hány méter kell a kúttól?',
             'Mert egyetlen szám nem lenne igaz minden helyzetre. A távolság megítélése függ a '
             'kút típusától és mélységétől, a talajvíz áramlási irányától, a terület '
             'érzékenységi besorolásától és attól, hogy kijelölt vízbázisvédelmi területet '
             'érint-e. Egy általános szám itt inkább félrevezetne, mint segítene.'),
            ('A szomszéd kútját is figyelembe kell venni?',
             'Igen. A vízvédelmi megítélés szempontjából nem a telekhatár a döntő, hanem a '
             'kút és az elhelyezési pont tényleges viszonya. Ezért érdemes a szomszédos '
             'kutakat is feltüntetni a helyszínrajzon.'),
            ('Nem használt, régi kút van a telken. Számít?',
             'Számíthat. A nem használt, de le nem zárt kút a felszín alatti víz felé nyitott '
             'útvonal maradhat. Érdemes jelezni a helyét és állapotát, mert a szakértői '
             'megítélést befolyásolja.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 5) Telekméret és rendelkezésre álló terület
# ===========================================================================
def epit_terulet():
    return [
        sec_prose('A rossz kérdés', 'Nem a telek mérete a döntő', [
            'A telek teljes négyzetmétere önmagában kevéssé használható adat. Ami számít, az '
            'a <strong>ténylegesen felhasználható terület</strong>: ami a ház, melléképület, '
            'kút, gépkocsibeálló, fák, közművek és a tervezett kertfunkciók után megmarad — '
            'és amit később sem építenek be.',
            'Egy 1500 m²-es telken is lehet szűkös a helyzet, ha a ház középen áll, a hátsó '
            'harmadot fák foglalják el, és a maradék az egyetlen behajtási útvonal. '
            'Egy 600 m²-esen viszont lehet elegendő hely, ha az elrendezés jól tervezett.',
        ]),

        sec_numbered('Mihez kell hely', 'Négy külön helyigény',
                     'Ezek nem ugyanazon a helyen vannak, és nem is válthatók ki egymással.',
                     ['<strong>A tartály és a gépészet.</strong> Maga a berendezés, valamint '
                      'a hozzá tartozó gépészeti elemek. Ez a legkisebb helyigényű elem, és '
                      'jellemzően ez okozza a legkevesebb gondot.',
                      '<strong>A tisztított víz elhelyezése.</strong> A szikkasztó felülete a '
                      'napi vízmennyiség és a mért szivárgóképesség függvénye. Ez tipikusan '
                      'sokkal nagyobb terület, mint a tartályé — és ezt szokták alábecsülni.',
                      '<strong>A szervizhozzáférés.</strong> A fedlapnak nyithatónak, a '
                      'berendezésnek ellenőrizhetőnek és karbantarthatónak kell maradnia. '
                      'Nem elég annyi hely, amennyibe a tartály fizikailag befér.',
                      '<strong>A kivitelezés helyigénye.</strong> Munkagép mozgástere, a '
                      'kitermelt föld ideiglenes helye, a tartály beemelési útvonala. Ez '
                      'átmeneti, de a telepítés napján nélkülözhetetlen.']),

        sec_prose('Technológiánként más', 'Az oldómedencés rendszer nagyobb területet kér', [
            'A területigény nem ugyanaz a két fő megoldástípusnál. Az aktív biológiai '
            'rendszernél a tisztítás túlnyomó része a berendezésben történik, és a szikkasztó '
            'elsősorban a kilépő víz elhelyezésére szolgál.',
            'Az oldómedencés rendszernél viszont a talajban kialakított tisztítómező maga is '
            'a technológia része: a tisztítás jelentős hányada ott zajlik. Emiatt a '
            'területigénye rendszerint nagyobb, és a mező helye nem tekinthető szabadon '
            'áthelyezhető kiegészítőnek.',
            'Ezért fordulhat elő, hogy ugyanazon a telken az egyik megoldástípus elfér, a '
            'másik nem — és ez a telekméret önmagában nem mutatja meg.',
        ]),

        sec_numbered('Helyszínrajz', 'Mit jelöljön be?',
                     'Egy kézzel rajzolt, méretarányos vázlat is tökéletesen megfelel. '
                     'Nem kell tervezői rajz — a viszonyok a fontosak.',
                     ['A ház körvonala és a szennyvízcső kilépési pontja',
                      'Melléképületek, terasz, medence — meglévő és tervezett egyaránt',
                      'A kút vagy kutak helye, a szomszédos telkeken lévőkkel együtt',
                      'Behajtó, gépkocsibeálló, burkolt felületek',
                      'Ismert közművek nyomvonala — víz, gáz, elektromos, telekom',
                      'Nagy fák és megtartandó növényzet, a lombkorona kiterjedésével',
                      'Az északi irány, a telekhatárok és a tereplejtés iránya',
                      'A későbbre tervezett építmények — ez a leggyakrabban kimaradó adat']),

        hiany('a modell- és terhelésspecifikus helyigény: mekkora terület kell a tartálynak, '
              'a gépészetnek és a szervizhozzáférésnek modellenként, és mekkora a '
              'legkisebb sikeresen megvalósított telek',
              'ÖkoTech aktuális termékméretek + megvalósult projektek. A jelenlegi 2–10 '
              'méteres épülettávolság gyártói és üzemeltetési ajánlás, NEM jogi védőtávolság '
              '— így is kell kommunikálni'),

        sec_prose('Amit a szikkasztó fölött nem lehet', 'A terület használata utána is számít', [
            'A szikkasztó fölötti és körüli terület nem használható korlátlanul. A '
            'tömörítés, a burkolás, a járműforgalom és a mély gyökérzetű növényzet mind '
            'befolyásolhatja a működést. Ezt a tervezéskor kell tisztázni, nem akkor, amikor '
            'két év múlva medence vagy parkoló kerülne ugyanoda.',
            'Ezért kérdezünk rá a <strong>későbbi</strong> kert- és építési tervekre is. '
            'Ha tudható, hogy a hátsó kertbe medence kerül, akkor a szikkasztó nem oda '
            'tervezendő — akkor sem, ha ma az a legkényelmesebb hely.',
        ]),

        sec_cta('Következő lépés', 'A hely megvan — milyen mélyen?',
                ['A vízszintes elrendezés után a magassági viszonyok jönnek: a házból kilépő '
                 'cső mélysége és a terep lejtése határozza meg, hogy gravitációsan '
                 'megoldható-e a rendszer, vagy átemelő kell hozzá.'],
                'Lejtés és csőmélység', 'lejtes-es-csomelyseg',
                alt=('Telekalkalmasság áttekintése', 'telekalkalmassag-attekintese')),

        sec_faq([
            ('Mekkora telek kell egy házi szennyvíztisztítóhoz?',
             'Erre szándékosan nem adunk egyetlen számot, mert nem lenne igaz. A szükséges '
             'terület függ a megoldástípustól, a háztartás létszámától és a talaj mért '
             'szivárgóképességétől — ugyanaz a telek egyik esetben elegendő, másikban nem. '
             'Az elrendezés a döntő, nem a négyzetméter.'),
            ('Milyen messze kell lennie a tartálynak a háztól?',
             'A 2–10 méteres távolság gyártói és üzemeltetési ajánlás, nem jogszabályi '
             'védőtávolság. A tényleges elhelyezést a csőkilépési szint, a lejtés, a '
             'szervizhozzáférés és a telek adottságai együtt határozzák meg.'),
            ('A szikkasztó fölé lehet később teraszt vagy medencét építeni?',
             'Általában nem célszerű, és bizonyos esetekben nem is megengedhető: a tömörítés '
             'és a burkolás rontja a működést. Ha ilyen terve van, azt a tervezéskor jelezze '
             '— akkor a szikkasztó eleve máshová kerül.'),
            ('Beépített, kicsi telken van esély?',
             'Sok esetben igen, de ott számít igazán az elrendezés és a mért szivárgóképesség. '
             'Kis telken gyakran a tisztított víz elhelyezése a szűk keresztmetszet, nem a '
             'tartály. Ilyenkor érdemes korán helyszínrajzot készíteni.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 6) Lejtés és csőmélység
# ===========================================================================
def epit_lejtes():
    return [
        sec_prose('Miért most, és nem a kivitelezéskor', 'A magassági adat a legdrágább '
                                                          'meglepetés', [
            'A házból kilépő szennyvízcső magassága meghatározza, milyen mélyre kerülhet a '
            'berendezés befolyó pontja. A terep lejtése pedig azt, hogy a szennyvíz és '
            'később a tisztított víz <strong>gravitációsan</strong> vezethető-e, vagy '
            'szivattyús megoldás kell hozzá.',
            'Ez az a telekadat, amely a leggyakrabban csak a kivitelezéskor derül ki — és '
            'akkor már a legdrágább kezelni. A magasító elem, az átemelő akna vagy a '
            'többlet földmunka mind olyan tétel, amely a tervezéskor még átgondolható, '
            'a gödör szélén állva viszont már nem.',
        ]),

        sec_numbered('A négy magassági pont', 'Mit kell megmérni?',
                     'Mindegyik a terepszinthez viszonyítva értendő. Egy egyszerű '
                     'vízszintezés és mérőszalag elegendő hozzá.',
                     ['<strong>A cső kilépési helye a házból.</strong> A ház melyik oldalán '
                      'és pontosan hol lép ki a szennyvízcső. Új építésnél ez tervezői '
                      'döntés — érdemes az elhelyezéssel együtt eldönteni.',
                      '<strong>A folyásfenék mélysége.</strong> Nem a cső teteje, hanem az '
                      'alja: ez határozza meg, milyen szintre kell a berendezés befolyójának '
                      'kerülnie. Ez a legfontosabb egyetlen szám ezen az oldalon.',
                      '<strong>A tartály tervezett helyének terepszintje.</strong> Ha az '
                      'magasabban vagy alacsonyabban van, mint a ház melletti terep, az '
                      'közvetlenül módosítja a beépítési mélységet.',
                      '<strong>A tisztított víz elhelyezésének szintje.</strong> Ha a '
                      'szikkasztó magasabban van, mint a berendezés kifolyója, szivattyú '
                      'nélkül nem működik. Sík terepen ez gyakoribb, mint gondolnánk.']),

        sec_split('A lejtés nem jó vagy rossz', 'Iránytól függ',
                  'Kedvező helyzet',
                  ['A ház felől a szikkasztó felé lejt a terep',
                   'A berendezés a ház és a szikkasztó között, közbenső szinten helyezhető el',
                   'Gravitációs befolyás és gravitációs kifolyás egyaránt megoldható',
                   'Nincs szükség átemelőre, se szivattyúra',
                   'Kevesebb földmunka, egyszerűbb kivitelezés'],
                  'Külön megoldást igényel',
                  ['A szikkasztó a berendezés kifolyójánál magasabban van',
                   'A csőkilépés a terepszinthez képest szokatlanul mély',
                   'A terep a ház felé lejt, a szabad terület felfelé esik',
                   'Sík terep, ahol nincs elegendő esés a szikkasztóig',
                   'Ilyenkor magasítás, átemelő akna vagy szivattyús vízvezetés jön szóba']),

        hiany('a jelenlegi 30 cm-es magasító-korlát érvényessége az AKTUÁLIS A.B.Clear '
              'modellekre, valamint a modellenkénti pontos befolyási és kifolyási méretek',
              'ÖkoTech műszaki dokumentáció + aktuális termékadatlapok. A megrendelőlapon '
              'szereplő szabály régebbi; modellenként ellenőrizni kell, mielőtt általános '
              'tervezési szabályként megjelenik'),

        sec_prose('Új építésnél és meglévő háznál más a feladat', '', [
            '<strong>Új építésnél</strong> a csőkilépés helye és mélysége még '
            'befolyásolható. Ez a legolcsóbb pillanat: a gépész tervezővel egyeztetve a '
            'kilépési pont odakerülhet, ahol a berendezés is elfér, és olyan mélységbe, '
            'amely magasító és átemelő nélkül megoldható. Érdemes a szennyvízrendszert még '
            'a kiviteli terv véglegesítése előtt átbeszélni.',
            '<strong>Meglévő háznál</strong> a csőkilépés adott, tehát mérni kell. A '
            'legmegbízhatóbb, ha megbontják vagy megkeresik a meglévő aknát, és a '
            'folyásfeneket a terepszinthez viszonyítva lemérik. Ha ez nem megoldható, a '
            'helyszíni felmérés része lehet.',
        ]),

        sec_numbered('Az eredmény', 'Négy lehetséges kimenet', '',
                     ['<strong>Gravitációs kialakítás valószínű.</strong> A szintek '
                      'megfelelnek, szivattyú és magasítás nélkül megoldható.',
                      '<strong>Magasítás vizsgálandó.</strong> A berendezés a szokásosnál '
                      'mélyebbre kerülne; magasító elemmel kezelhető lehet, de a '
                      'megengedett mértéket modellenként kell ellenőrizni.',
                      '<strong>Átemelés valószínű.</strong> A mélység vagy a szikkasztó '
                      'szintje szivattyús megoldást tesz szükségessé. Ez a beruházási '
                      'költséget és az üzemeltetést is befolyásolja.',
                      '<strong>Helyszíni szintezés szükséges.</strong> A magassági adatok '
                      'nem ismertek megbízhatóan. Ezt mérés zárja le — becsléssel nem '
                      'tervezhető.']),

        sec_cta('Következő lépés', 'A gép is bejut? És a szerviz?',
                ['A magassági viszonyok után a hozzáférés a következő. Két külön kérdés: '
                 'a telepítéshez szükséges munkagép behajtása, és a rendszer tartós '
                 'hozzáférhetősége az üzemeltetés alatt.'],
                'Járműterhelés és hozzáférés', 'jarmuterheles-es-hozzaferes',
                alt=('Telekalkalmasság áttekintése', 'telekalkalmassag-attekintese')),

        sec_faq([
            ('Mi az a folyásfenék?',
             'A cső belsejének legalsó pontja — ahol a víz ténylegesen folyik. A méretezéshez '
             'nem a cső teteje vagy a földfelszín számít, hanem ez. Ezért kérünk mindig '
             'folyásfenék-mélységet, terepszinthez viszonyítva.'),
            ('Sík telken nincs gond a lejtéssel?',
             'Nem feltétlenül. Sík terepen fordulhat elő leggyakrabban, hogy a berendezés '
             'kifolyója a szikkasztó szintje alá kerül, és emiatt szivattyú válik '
             'szükségessé. A sík terep nem azonos a problémamentes szintviszonnyal.'),
            ('Mennyivel drágább az átemelős megoldás?',
             'Konkrét árat itt nem adunk, mert az a berendezéstől, a szükséges emelési '
             'magasságtól és a kivitelezési körülményektől függ. Ami biztosan igaz: az '
             'átemelő beruházási költséget, áramfogyasztást és egy további karbantartandó '
             'gépészeti elemet jelent. Ezért érdemes új építésnél a szintekkel elkerülni.'),
            ('Új házat tervezünk. Mikor kell ezt eldönteni?',
             'A kiviteli terv véglegesítése előtt. Ekkor még szabadon megválasztható a '
             'szennyvízcső kilépési helye és mélysége, ami a legolcsóbb módja annak, hogy '
             'a rendszer magasító és átemelő nélkül működjön.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 7) Járműterhelés és hozzáférés
# ===========================================================================
def epit_hozzaferes():
    return [
        sec_prose('Két külön hozzáférés', 'A telepítés és az üzemeltetés mást igényel', [
            'Az egyik kérdés az, hogyan jutnak be a telepítéshez szükséges gépek a telekre, '
            'és hogyan kerül a helyére a tartály. Ez egyszeri, de a telepítés napján nincs '
            'rá alternatíva.',
            'A másik az, hogyan marad a rendszer elérhető a használat és a szerviz során. '
            'Ez tartós követelmény: a fedlapnak nyithatónak, a berendezésnek '
            'ellenőrizhetőnek és karbantarthatónak kell maradnia — évek múlva is.',
        ]),

        sec_prose('A legfontosabb korlát', 'A tartály fölött nem vezethető járműforgalom', [
            'A standard műanyag tartály fölött <strong>nem vezethető közvetlenül '
            'gépjárműforgalom</strong>, és úttest vagy járda sem építhető fölé egyszerűen. '
            'Ez termékspecifikus szerkezeti korlát, nem óvatoskodás.',
            'Ha a járműterhelés elkerülhetetlen — mert például csak a behajtó alatt van hely —, '
            'akkor külön, megfelelően méretezett betonakna és előzetes műszaki egyeztetés '
            'szükséges. Ez megoldható, de tervezési döntés és költségtétel, nem utólagos '
            'apróság.',
            'Ugyanez vonatkozik a szikkasztó fölötti területre: a tömörítés és a burkolás ott '
            'a működést rontja, nem a szerkezetet veszélyezteti — de a következmény ugyanúgy '
            'meghibásodás.',
        ]),

        sec_numbered('A telepítés hozzáférése', 'Mit kell ellenőrizni a kivitelezés előtt?',
                     'Ezek nagy része fotóval előre tisztázható, kiszállás nélkül.',
                     ['<strong>Kapuszélesség és -magasság.</strong> A behajtó legszűkebb '
                      'pontja, a kapuoszlopok közötti tényleges méret.',
                      '<strong>A behajtó teherbírása.</strong> Puha talaj, frissen feltöltött '
                      'terület vagy rézsű mellett a munkagép nem feltétlenül jut be.',
                      '<strong>Belógó akadályok.</strong> Elektromos légvezeték, faágak, '
                      'előtető — a magasság éppúgy korlát, mint a szélesség.',
                      '<strong>A tartály beemelési útvonala.</strong> A tartály nem gurul: '
                      'oda kell emelni. A gép állásának helye és a beemelés útvonala '
                      'előre tisztázandó.',
                      '<strong>A kitermelt föld helye.</strong> A munkagödörből kikerülő föld '
                      'jelentős térfogatot foglal. Ha nincs hová tenni, elszállítás — '
                      'költség és többlet forgalom.',
                      '<strong>Megtartandó növényzet és burkolat.</strong> Mit nem szabad '
                      'megbontani, és mit lehet helyreállítani utána.']),

        sec_numbered('A szerviz hozzáférése', 'Mi kell tartósan?',
                     'Ez a rész marad ki a leggyakrabban a tervezésből — és ez okoz a '
                     'legtöbb bosszúságot évekkel később.',
                     ['A fedlap szabadon nyitható legyen: ne kerüljön rá burkolat, ágyás, '
                      'tárolt anyag vagy parkoló autó',
                      'A berendezés körül legyen elegendő hely a munkavégzéshez',
                      'A szikkasztó fölötti terület maradjon ellenőrizhető',
                      'Az áramellátás és a vezérlés hozzáférhető legyen',
                      'A szippantás — ahol szükséges — megközelíthető legyen tehergépjárművel',
                      'A növényzet ne nőjön rá: a mély gyökérzetű fa a fedlaphoz közel '
                      'később problémát okoz']),

        hiany('az A.B.Clear fedlap és tartály hivatalos terhelési adatai, a járműterhelésre '
              'jóváhagyott betonakna kialakítása, valamint a kivitelezéshez szükséges '
              'minimális behajtási szélesség és géppark-méretek',
              'ÖkoTech kivitelezési csapat + aktuális termékdokumentáció. Amíg nincs meg, '
              'a látogató nem tudja előre eldönteni, elfér-e a gép'),

        sec_cta('Következő lépés', 'Most már tudja, mit kell megszereznie',
                ['Végigment a hét témakörön. A következő oldal adatforrásonként mutatja meg, '
                 'honnan és milyen megbízhatósággal szerezhető meg mindaz, amire szükség van — '
                 'és mi a teendő azzal, amit nem tud.'],
                'Hogyan gyűjtsem össze a telekadatokat?', 'telekadatok-osszegyujtese',
                alt=('Telekalkalmasság áttekintése', 'telekalkalmassag-attekintese')),

        sec_faq([
            ('A behajtó alá kerülhet a tartály?',
             'Csak külön, megfelelően méretezett betonaknával és előzetes műszaki '
             'egyeztetéssel. A standard műanyag tartály fölött közvetlen gépjárműforgalom '
             'nem vezethető. Ha nincs más hely, ezt a tervezéskor kell tisztázni, mert '
             'költség- és kivitelezési következménye van.'),
            ('Mi történik, ha később burkolatot építenék a fedlap fölé?',
             'A fedlapnak nyithatónak és hozzáférhetőnek kell maradnia, különben az '
             'ellenőrzés és a karbantartás ellehetetlenül. Ha burkolást tervez, azt előre '
             'jelezze — akkor az elhelyezés eleve máshová kerül, vagy a burkolat kap '
             'nyitható részt.'),
            ('Fotóval elő lehet szűrni a hozzáférést?',
             'A legtöbb kérdést igen. A behajtó legszűkebb pontja, a kapu, a belógó '
             'vezetékek, a tervezett hely és a környezete fotón jól megítélhető. Ha ezekből '
             'bizonytalanság marad, akkor indokolt a helyszíni felmérés.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 8) Hogyan gyűjtsem össze a telekadatokat?
# ===========================================================================
ADATOK = [
    ('Alaphelyzet', [
        ('Cím, helyrajzi szám', 'Tulajdoni lap, térképmásolat, hirdetés',
         'dokumentum', 'Enélkül a területi besorolás nem ellenőrizhető'),
        ('Közcsatorna helyzete', 'Víziközmű-szolgáltató, önkormányzat',
         'dokumentum', 'Ez dönti el, hogy egyedi rendszer egyáltalán szóba jön-e'),
        ('Érzékenységi besorolás', 'Hivatalos jegyzék, aktuális állapot',
         'dokumentum', 'Fokozottan érzékeny területen külön feltételek élnek'),
        ('Vízbázisvédelmi terület', 'Hivatalos forrás, hatóság',
         'dokumentum', 'Kút közelében és bizonytalan helyzetben nem hagyható ki'),
    ]),
    ('Elrendezés', [
        ('Telekméret', 'Tulajdoni lap', 'dokumentum',
         'Önmagában nem elég — a szabad terület a lényeg'),
        ('Helyszínrajz a ház helyével', 'Építési terv vagy kézi vázlat',
         'becsülhető', 'Kézzel rajzolt, méretarányos vázlat is megfelel'),
        ('Ténylegesen szabad terület', 'Bejárás, helyszínrajz', 'becsülhető',
         'A fákkal, közművekkel és tervezett építményekkel együtt'),
        ('Kút helye és típusa', 'Bejárás, kút dokumentációja', 'becsülhető',
         'A szomszédos telkek kútjait is jelölje'),
        ('Behajtási szélesség', 'Mérés helyben, fotó', 'becsülhető',
         'A legszűkebb pont számít, nem a kapu névleges mérete'),
    ]),
    ('Magassági adatok', [
        ('A csőkilépés helye', 'Gépész terv vagy bejárás', 'becsülhető',
         'Új építésnél még befolyásolható'),
        ('Folyásfenék-mélység', 'Terv, vagy szintezés helyben', 'mérni kell',
         'A cső alja, terepszinthez viszonyítva — nem a cső teteje'),
        ('Tereplejtés iránya és mértéke', 'Bejárás, terepszintrajz', 'becsülhető',
         'Az irány gyakran fontosabb, mint a pontos százalék'),
        ('A szikkasztó tervezett szintje', 'Helyszínrajz + szintezés', 'mérni kell',
         'Ha a kifolyónál magasabban van, szivattyú kell'),
    ]),
    ('Talaj és víz', [
        ('Talajtípus és rétegződés', 'Talajmechanikai szakvélemény, korábbi földmunka',
         'becsülhető', 'Előszűrésre elég, méretezésre nem'),
        ('MÉRT szivárgóképesség', 'Szivárogtatási vizsgálat', 'mérni kell',
         'A szikkasztó tervezett helyén és mélységében'),
        ('Szezonális legmagasabb talajvíz', 'Szakvélemény, kút adatlapja, megfigyelés',
         'mérni kell', 'Nem a mai vízállás — az évszakos maximum'),
        ('A talajvíz-adat forrása és dátuma', 'A dokumentumon', 'dokumentum',
         'Egy adat kora önmagában is információ'),
    ]),
]


def epit_adatgyujtes():
    sorok = []
    for csoport, tetelek in ADATOK:
        sorok.append(f'''        <tr>
          <th class="compare-group" colspan="4" scope="colgroup">{csoport}</th>
        </tr>''')
        for mi, honnan, minoseg, megj in tetelek:
            sorok.append(f'''        <tr>
          <th scope="row">{mi}</th>
          <td class="type-ui-body">{honnan}</td>
          <td class="type-ui-body">{minoseg}</td>
          <td class="type-ui-body">{megj}</td>
        </tr>''')
    tabla = f'''
  <section class="section" aria-labelledby="adatlap-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Adatforrások</p>
        <h2 class="type-display-section-title section-title" id="adatlap-cim">Melyik adat honnan szerezhető meg?</h2>
        <p class="type-ui-body section-lead">A harmadik oszlop a lényeg: van, amit elég
          megbecsülni, van, amit dokumentumból kell kiolvasni, és van, amit mérni kell.
          Ez dönti el, hogy elegendő-e a távoli előszűrés.</p>
      </header>
      <div class="compare-scroll" tabindex="0" role="region" aria-labelledby="adatlap-cim">
        <table class="compare-table compare-table-start">
          <caption class="visually-hidden">Telekadatok, forrásuk és a szükséges adatminőség</caption>
          <thead>
            <tr>
              <th scope="col">Adat</th>
              <th scope="col">Honnan</th>
              <th scope="col">Minőség</th>
              <th scope="col">Megjegyzés</th>
            </tr>
          </thead>
          <tbody>
{chr(10).join(sorok)}
          </tbody>
        </table>
      </div>
    </div>
  </section>
'''
    return [
        sec_prose('Mire jó ez az oldal', 'Nem újabb lista — adatforrások', [
            'A korábbi oldalak megmutatták, <em>milyen</em> adatokra van szükség. Ez az oldal '
            'azt mutatja meg, <em>honnan</em> szerezhetők meg, és milyen megbízhatósággal.',
            'Minden adatnál három dolog számít: miért kell, hol találja meg, és mi a teendő, '
            'ha nem áll rendelkezésre. A „nem tudom” itt sem hiba — adatbeszerzési feladat.',
        ]),
        tabla,
        sec_numbered('Fotók', 'Mit érdemes lefotózni, és milyen szögből?',
                     'A fotó sokszor többet mond, mint a leírás — de csak akkor, ha látszik '
                     'rajta a viszonyítás. Érdemes mindegyikre ráállítani valami ismert '
                     'méretű tárgyat, például egy colstokot.',
                     ['<strong>A tervezett hely a ház felől.</strong> Legyen rajta a ház fala '
                      'és a szabad terület is, hogy a távolság megítélhető legyen.',
                      '<strong>Ugyanaz a hely a telek vége felől.</strong> A két ellentétes '
                      'nézet együtt megmutatja a terep lejtését is.',
                      '<strong>A behajtó a kapuval.</strong> A legszűkebb pontnál állva, '
                      'befelé nézve. Ha van belógó vezeték vagy faág, az is legyen rajta.',
                      '<strong>A szennyvízcső kilépési pontja vagy a meglévő akna.</strong> '
                      'Ha megbontható, a folyásfenék is lássék, mérőszalaggal.',
                      '<strong>A kút és környezete.</strong> A kút fedele, és a mögötte lévő '
                      'terület a tájékozódáshoz.',
                      '<strong>Bármi szokatlan.</strong> Vízállásos folt, feltöltés nyoma, '
                      'rézsű, korábbi földmunka helye.']),

        sec_split('Az adat kora', 'Mikortól nem használható egy régi adat?',
                  'Jellemzően tartós',
                  ['A telek mérete és határai',
                   'A ház és a melléképületek helye',
                   'A csőkilépés helye és mélysége meglévő háznál',
                   'A tereplejtés iránya',
                   'A talaj rétegződése'],
                  'Elavulhat — ellenőrizni kell',
                  ['A település érzékenységi besorolása',
                   'A vízbázisvédelmi terület kijelölése',
                   'A közcsatorna elérhetősége és a fejlesztési tervek',
                   'A helyi építési szabályzat előírásai',
                   'A talajvízszint — évszakosan és évek között is változik']),

        sec_cta('Következő lépés', 'Nézzük meg, mi jön ki belőle',
                ['Ha összegyűlt, ami megszerezhető volt, az előszűrő végigveszi: megmondja, '
                 'van-e látható műszaki vagy vízvédelmi kockázat, mi hiányzik még, és melyik '
                 'továbblépés indokolt. Nem kér kapcsolati adatot a használatához.'],
                'Telek- és vízelhelyezési előszűrő', 'telek-es-vizelhelyezesi-eloszuro',
                alt=('Telekalkalmasság áttekintése', 'telekalkalmassag-attekintese')),

        sec_faq([
            ('Mennyi adat kell ahhoz, hogy egyáltalán elinduljunk?',
             'A beszélgetéshez elég a település, a használat módja és a háztartás létszáma. '
             'Ahhoz viszont, hogy műszaki irányt tudjunk mondani, kell a szabad terület, a '
             'csőkilépési szint és legalább egy tájékoztató talaj- és talajvízadat. '
             'A méretezéshez ezeken felül mérés is szükséges.'),
            ('Kell fizetnem az adatok beszerzéséért?',
             'Egy részük ingyenes vagy már megvan: tulajdoni lap, építési terv, saját '
             'megfigyelés, fotó. A szivárogtatási vizsgálat és a talajmechanikai szakvélemény '
             'viszont szolgáltatás, aminek költsége van. Hogy szükséges-e, éppen az '
             'előszűrésből derül ki — nem érdemes vele kezdeni.'),
            ('Feltölthetek tervet vagy fotót?',
             'Igen, és érdemes: a helyszínrajz, a metszet és néhány fotó sokkal gyorsabbá '
             'teszi a szakmai egyeztetést, mint a szöveges leírás. A dokumentumokat a '
             'kapcsolatfelvételnél tudja csatolni.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 9) Telek- és vízelhelyezési előszűrő
# ===========================================================================
def epit_eloszuro():
    return [
        sec_prose('Mi ez, és mi nem', 'Előszűrés, nem alkalmassági igazolás', [
            'Ez a modul a megadott telekadatokat szabályalapon értékeli: megmutatja, van-e '
            'látható műszaki vagy vízvédelmi kockázat, mely adatok hiányoznak, és melyik '
            'továbblépés indokolt. Nem kér kapcsolati adatot a használatához.',
            'Amit <strong>nem</strong> ad: engedélyezhetőségi nyilatkozatot, végleges '
            'termékmodellt, konkrét árat és mérés nélküli, garantált szikkasztó-méretezést. '
            'Ezek egyike sem dönthető el űrlapról — hatóság, jogosult tervező, illetve '
            'mérési eredmény kell hozzájuk.',
            'A modul megkülönbözteti a <strong>valódi negatív feltételt</strong> és az '
            '<strong>egyszerűen hiányzó adatot</strong>. A kettő nem ugyanaz: az első a telek '
            'tulajdonsága, a második a tájékozottságé — és csak az elsőből következik '
            'korlátozás.',
        ]),

        sec_numbered('A vizsgálat menete', 'Milyen sorrendben halad?',
                     'A kemény kapukkal kezd: ha ott elakad, a részletkérdéseket fölösleges '
                     'végigvenni.',
                     ['<strong>Kemény kapuk.</strong> Közcsatorna helyzete, a projekt jellege '
                      'és nagyságrendje, a település érzékenységi besorolása, ismert '
                      'vízbázisvédelmi körülmény. Nem kommunális jellegű vagy nagyobb '
                      'kapacitású projekt itt külön szakértői ágra kerül.',
                      '<strong>Talaj és víz.</strong> Talajtípus, mért szivárgóképesség, '
                      'szezonális talajvíz, kút és a tisztított víz tervezett elhelyezése.',
                      '<strong>Elrendezés.</strong> Telekméret, ténylegesen szabad terület, '
                      'csőkilépési szint, tereplejtés.',
                      '<strong>Hozzáférés.</strong> Behajtás, járműterhelés, szervizterület.',
                      '<strong>Adatminőség.</strong> Minden válasznál külön rögzül, hogy '
                      'becsült, dokumentumból ismert vagy mért. Ez határozza meg, hogy az '
                      'eredmény mennyire terhelhető.']),

        sec_split('Az eredmény', 'Mit mond meg, és mit nem',
                  'Ezt megmondja',
                  ['Van-e azonosított kritikus akadály',
                   'Melyik kritikus adat hiányzik, és mivel pótolható',
                   'Valószínű-e külön műszaki elem — rögzítés, magasítás, átemelő, betonakna',
                   'Igazolt-e a vízelhelyezés iránya, vagy még vizsgálandó',
                   'Indokolt-e a helyszíni felmérés, és mit zárna le',
                   'Kell-e hidrogeológiai vagy jogi ellenőrzés'],
                  'Ezt nem mondja meg',
                  ['Hogy a projekt engedélyezhető-e',
                   'Hogy melyik konkrét berendezésmodell lesz a megfelelő',
                   'Hogy mennyibe kerül',
                   'A szikkasztó pontos méretét mérési adat nélkül',
                   'A megtérülést vagy az üzemeltetési költséget',
                   'Bármit, ami jogosult tervező vagy hatóság hatásköre']),

        sec_numbered('A lehetséges kimenetek', 'Öt eredmény, öt különböző következő lépés', '',
                     ['<strong>Nincs látható akadály.</strong> Az ismert adatok alapján a '
                      'szokásos kialakítás valószínű. A tervezés a szokásos úton folytatható.',
                      '<strong>Feltételesen alkalmas.</strong> Megvalósítható, de külön '
                      'műszaki elemmel. Az érintett elemeket az eredmény nevesíti.',
                      '<strong>Hiányzó kritikus adat.</strong> Nem a telek a korlát, hanem az '
                      'információ. Az eredmény megmondja, melyik adat és honnan szerezhető meg.',
                      '<strong>Helyszíni felmérés indokolt.</strong> Több bizonytalanság '
                      'együtt, vagy olyan kérdés, amit csak a helyszínen lehet lezárni.',
                      '<strong>Szakértői vagy hatósági vizsgálat szükséges.</strong> '
                      'Vízvédelmi, hidrogeológiai vagy jogi kérdés, amiben nem a berendezés '
                      'szállítója dönt.']),

        hiany('maga a szabálymotor: a telekalkalmassági döntési fa, a talajvíz–konstrukció '
              'megfeleltetés, a szivárgási eredmény értelmezési küszöbei, a csőmélység–'
              'magasítás–átemelés szabály és a kötelező felmérés esetei',
              'ÖkoTech műszaki workshop, majd legalább 50–100 korábbi projekt visszatesztelése '
              'az előszűrőn. A modul addig nem kapcsolható élesre — a jelen oldal a szerkezetet '
              'és a kimeneteket írja le'),

        sec_cta('Addig is', 'Beszéljünk a konkrét telekről',
                ['Amíg az előszűrő nem üzemel, ugyanezt élőben végigvesszük. Írja meg a '
                 'település nevét, a háztartás létszámát, és amit a telekről tud — a többit '
                 'megkérdezzük.',
                 'Ha vannak dokumentumai — helyszínrajz, metszet, talajmechanikai '
                 'szakvélemény, kút adatlapja —, csatolja: azokkal sokkal gyorsabban jutunk '
                 'műszaki irányig.'],
                'Kapcsolatfelvétel', '../kapcsolat',
                alt=('Telekalkalmasság áttekintése', 'telekalkalmassag-attekintese')),

        sec_faq([
            ('Miért nem ad az előszűrő egyértelmű „igen” vagy „nem” választ?',
             'Mert a telekalkalmasság több olyan tényezőt tartalmaz, amely csak mérésből, '
             'hivatalos adatból vagy szakértői vizsgálatból dönthető el. Egy egyértelmű '
             'válasz ezek nélkül nem lenne megalapozott — legfeljebb magabiztosnak hangzana.'),
            ('Elmentheti valaki az eredményt?',
             'Igen, a kimenet egy menthető telekbrief: mit tudunk, mi hiányzik, és mi a '
             'javasolt következő lépés. Ez továbbadható a műszaki kollégának, a helyszíni '
             'felmérésnek vagy a tervezőnek.'),
            ('Ha az eredmény „nem igazolt”, akkor vége?',
             'Nem. Az azt jelenti, hogy az ismert körülmények alapján a tervezett megoldás '
             'nem támasztható alá — jellemzően a vízelhelyezés miatt. Ilyenkor más '
             'elhelyezési irány, más technológia vagy szakértői vizsgálat következik, '
             'nem a projekt lezárása.'),
        ]),
        JOGI,
    ]


# ===========================================================================
OLDALAK = [
    dict(file='projekt-elokeszites/telekalkalmassag.html',
         url='projekt-elokeszites/telekalkalmassag', img='telekvasarlas',
         title='Telekalkalmasság — mi dönti el, hogy megvalósítható-e | ÖkoTech Home',
         desc='A talaj, a talajvíz, a szabad terület, a csőszint, a kút és a vízelhelyezés '
              'együtt dönti el, mi valósítható meg a telken. Négy állapot, nem igen-nem.',
         h1='Telekalkalmasság',
         alt='Beépítetlen telek felmérés közben: kitűzőkarók, mérőszalag és talajminta-gödör '
             'a gyepen',
         lead='A tartály szinte mindig elfér valahol. A rendszer viszont csak akkor működik, '
              'ha a tisztított víznek is van hová mennie — és ez a nehezebb kérdés. '
              'Itt végigvesszük, mi dönti el.',
         crumbs=CRUMB, sections=epit_hub()),

    dict(file='projekt-elokeszites/telekalkalmassag-attekintese.html',
         url='projekt-elokeszites/telekalkalmassag-attekintese', img='attekintes',
         title='Telekalkalmasság áttekintése — mit kell megvizsgálni | ÖkoTech Home',
         desc='Rövid döntési térkép: milyen kérdésekre kell választ találni, milyen '
              'sorrendben, és melyik adatot lehet becsülni, melyiket kell mérni.',
         h1='Telekalkalmasság áttekintése',
         alt='Kiterített helyszínrajz egy telekről, rajta ceruzával bejelölt ház, kút és '
             'tervezett rendszerhely',
         lead='Ez nem részletes útmutató, hanem térkép: mit kell megvizsgálni, milyen '
              'sorrendben, és hová vezet tovább. A részletek a saját oldalaikon vannak.',
         crumbs=HUB, sections=epit_attekintes()),

    dict(file='projekt-elokeszites/talaj-es-szivargokepesseg.html',
         url='projekt-elokeszites/talaj-es-szivargokepesseg', img='oldomedence',
         title='Talaj és szivárgóképesség — mit kell mérni | ÖkoTech Home',
         desc='A talaj neve nem méretezési adat. Mi a szivárgóképesség, mikor kell '
              'szivárogtatási vizsgálat, és mit nem lehet a szomszéd tapasztalatából tudni.',
         h1='Talaj és szivárgóképesség',
         alt='Talajmetszet réteges szerkezettel: humusz, homokos és agyagos rétegek egy '
             'feltárási gödör falában',
         lead='A „homokos” vagy „agyagos” megnevezés önmagában nem elég. A kérdés az, milyen '
              'sebességgel képes a helyszíni talaj a vizet befogadni — és ezt mérni kell, '
              'nem megnevezni.',
         crumbs=HUB, sections=epit_talaj()),

    dict(file='projekt-elokeszites/talajviz.html',
         url='projekt-elokeszites/talajviz', img='kozcsatorna',
         title='Talajvíz — a tartály és a vízelhelyezés két külön kérdés | ÖkoTech Home',
         desc='Nem a mai vízállás számít, hanem a szezonális maximum. Mit old meg a '
              'tartályrögzítés, és miért külön kérdés a szikkasztás megfelelősége.',
         h1='Talajvíz',
         alt='Talajmetszet magas talajvízszinttel: a vízszint fölött homokos réteg, alatta '
             'vízzel telített zóna',
         lead='Magas talajvíznél két külön kérdés van: telepíthető-e a tartály, és '
              'elhelyezhető-e a tisztított víz. Az elsőre gyakran van műszaki megoldás — '
              'a második nem következik belőle.',
         crumbs=HUB, sections=epit_talajviz()),

    dict(file='projekt-elokeszites/kut-es-vedotavolsag.html',
         url='projekt-elokeszites/kut-es-vedotavolsag', img='alternativak',
         title='Kút és védőtávolság — miért nincs egyetlen szám | ÖkoTech Home',
         desc='A zárt tartály és a szikkasztó vízvédelmi szempontból két külön objektum. '
              'Milyen kútadat kell, és mikor szükséges vízbázisvédelmi ellenőrzés.',
         h1='Kút és védőtávolság',
         alt='Ásott kút betongyűrűs kávája egy kert szélén, mögötte gondozott gyepfelület',
         lead='Kézenfekvő lenne egyetlen védőtávolságot megadni. Az viszont megtévesztő '
              'lenne: a válasz a kút típusától, a vízbázisvédelmi helyzettől és a tényleges '
              'elhelyezési ponttól függ.',
         crumbs=HUB, sections=epit_kut()),

    dict(file='projekt-elokeszites/telekmeret-es-szabad-terulet.html',
         # A SZLUG rövidebb marad, mint a megjelenített név: a sitemap oldalakat
         # nevez meg, nem URL-eket, és a szakaszban másutt is rövidített szlug áll
         # (pl. „Hogyan gyűjtsem össze a telekadatokat?" → telekadatok-osszegyujtese).
         url='projekt-elokeszites/telekmeret-es-szabad-terulet', img='csaladi-haz',
         title='Telekméret és rendelkezésre álló terület — mennyi hely kell valójában | ÖkoTech Home',
         desc='Nem a telek négyzetmétere a kérdés, hanem ami a ház, a kút, a behajtó és a '
              'közművek után marad. Mihez kell hely, és mit nem lehet a szikkasztó fölé építeni.',
         h1='Telekméret és rendelkezésre álló terület',
         alt='Családi ház kertje felülnézetből: gyep, behajtó, néhány fa és egy szabadon '
             'hagyott zöldfelület',
         lead='Egy nagy telken is lehet szűkös a helyzet, egy kisebben pedig elegendő — '
              'az elrendezés dönt, nem a négyzetméter. Univerzális minimális telekméret '
              'ezért nincs.',
         crumbs=HUB, sections=epit_terulet()),

    dict(file='projekt-elokeszites/lejtes-es-csomelyseg.html',
         url='projekt-elokeszites/lejtes-es-csomelyseg', img='biologiai',
         title='Lejtés és csőmélység — mikor kell magasítás vagy átemelő | ÖkoTech Home',
         desc='A folyásfenék mélysége és a terep lejtése dönti el, hogy gravitációsan '
              'megoldható-e a rendszer. Mit mérjen meg, és miért a tervezéskor a legolcsóbb.',
         h1='Lejtés és csőmélység',
         alt='Lejtős telek metszete: a házból kilépő szennyvízcső, a tartály és az alacsonyabb '
             'szinten elhelyezett szikkasztó',
         lead='Ez az a telekadat, amely a leggyakrabban csak a kivitelezéskor derül ki — és '
              'akkor a legdrágább kezelni. Négy magassági pont, és minden eldől.',
         crumbs=HUB, sections=epit_lejtes()),

    dict(file='projekt-elokeszites/jarmuterheles-es-hozzaferes.html',
         url='projekt-elokeszites/jarmuterheles-es-hozzaferes', img='kapcsolat',
         title='Járműterhelés és hozzáférés — telepítés és szerviz | ÖkoTech Home',
         desc='A tartály fölött nem vezethető gépjárműforgalom külön kialakítás nélkül. '
              'Behajtás, beemelés, és a rendszer tartós hozzáférhetősége.',
         h1='Járműterhelés és hozzáférés',
         alt='Munkagép egy telek behajtójánál, mellette földkupac és frissen kiásott munkagödör',
         lead='Két külön kérdés: bejut-e a gép a telepítéshez, és marad-e hozzáférés a '
              'szervizhez. A második marad ki a leggyakrabban — és az okoz gondot évekkel '
              'később.',
         crumbs=HUB, sections=epit_hozzaferes()),

    dict(file='projekt-elokeszites/telekadatok-osszegyujtese.html',
         url='projekt-elokeszites/telekadatok-osszegyujtese', img='helyzetem',
         title='Hogyan gyűjtsem össze a telekadatokat? — források és minőség | ÖkoTech Home',
         desc='Adatforrásonként: honnan szerezhető meg, ki tudja megadni, becsülhető vagy '
              'mérni kell — és mit érdemes lefotózni.',
         h1='Hogyan gyűjtsem össze a telekadatokat?',
         alt='Asztalon szétterített dokumentumok: tulajdoni lap, helyszínrajz, mérőszalag és '
             'jegyzetfüzet',
         lead='A korábbi oldalak megmutatták, milyen adatokra van szükség. Ez megmutatja, '
              'honnan szerezhetők meg — és mit tegyen azzal, amit nem tud.',
         crumbs=HUB, sections=epit_adatgyujtes()),

    dict(file='projekt-elokeszites/telek-es-vizelhelyezesi-eloszuro.html',
         url='projekt-elokeszites/telek-es-vizelhelyezesi-eloszuro', img='mar-van-rendszerem',
         title='Telek- és vízelhelyezési előszűrő — mi látszik akadálynak | ÖkoTech Home',
         desc='Szabályalapú előértékelés: van-e látható műszaki vagy vízvédelmi kockázat, '
              'mi hiányzik, és melyik továbblépés indokolt. Nem engedélyezhetőségi nyilatkozat.',
         h1='Telek- és vízelhelyezési előszűrő',
         alt='Táblagép egy telek helyszínrajzával, mellette mérőszalag és talajminta-zacskó',
         lead='Előszűrés, nem alkalmassági igazolás. Megmutatja, mi látszik akadálynak, mi '
              'hiányzik, és mi a következő lépés — kapcsolati adat kérése nélkül.',
         crumbs=HUB, sections=epit_eloszuro()),
]

if __name__ == '__main__':
    (WEB / 'projekt-elokeszites').mkdir(exist_ok=True)
    for o in OLDALAK:
        out = WEB / o['file']
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:60s} {len(out.read_text(encoding='utf-8'))//1024} KB")
