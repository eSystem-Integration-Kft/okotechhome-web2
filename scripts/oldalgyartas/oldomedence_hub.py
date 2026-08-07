#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Megoldások → Oldómedencés rendszer — hub, hat aloldal, és alatta az EPURECO
termékcsalád alhub öt aloldallal.

A brief HÉT ponton pontosít:

1. A jelenlegi „az oldómedence csak tárolja és ülepíti" állítás pontatlan a
   TELJES RENDSZERRE. A jogszabály és a gyártó is kétlépcsős rendszert ír le:
   oldómedence = első, ANAEROB előkezelési lépcső · tisztítómező = második
   kezelési/elhelyezési lépcső · a kettő EGYÜTT = oldómedencés rendszer.

2. A szippantási gyakoriság ellentmondásos: az EPURECO oldal kétévente, a
   2023-as összehasonlítás 1,5 évente írja. Ezt nem „1,5–2 évre" kell átírni,
   hanem gyártói útmutatóból és saját üzemeltetési adatból rendezni — a
   végleges tartalom valószínűleg feltételhez kötött intervallum lesz.

3. Az EPURECO modellrendszert a gyártóhoz kell igazítani. A GRAF jelenlegi
   nyilvános kínálata EPURECO 4 (2100 l), 6 (2700 l) és 7 (3400 l).

4. A tanúsítványokat aktuális gyártói dokumentumhoz kell kötni, nem régi
   szabványszámhoz: modell → aktuális DoP → alkalmazott szabvány → vizsgáló
   szervezet → dokumentum dátuma.

5. A baktériumadalék VALÓS üzemeltetési feladat — lényeges különbség az
   A.B.Clear önfenntartó kultúrájához képest, és nyíltan meg kell jelennie.

6. A fő döntési korlát nem a tartály, hanem a TISZTÍTÓMEZŐ. A konverziós
   logika ezért nem „hány fő → modell → ajánlat", hanem
   „használati profil → alkalmasság → telek és szivárgás → modell + mező".

7. ÁR EZEN AZ ÁGON SEM JELENIK MEG.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import (sec_numbered, sec_split, sec_prose, sec_situations,
                    sec_cta, sec_faq)

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

JOGI = ('<!-- JOGI ÉS GYÁRTÓI ELLENŐRZÉS PUBLIKÁLÁS ELŐTT. Érintett: 147/2010. Korm.\n'
        '     rendelet (tisztítómezővel ellátott oldómedencés létesítmény definíciója,\n'
        '     méretezési és üzemeltetési feltételek, hulladékkezelési dokumentáció) ·\n'
        '     EN 12566-1 aktuális változata · GRAF aktuális EPURECO termék- és\n'
        '     telepítési dokumentáció. Gyorsan avuló tartalom. -->')


def hiany(mi, honnan):
    return (f'<!-- ADATHIÁNY: {mi}\n'
            f'     Forrás: {honnan}. Addig konkrét értékkel nem publikálható. -->')


HOME = ('Főoldal', '../')
MEG = ('Megoldások', './')
CRUMB = [HOME, MEG]
HUB = [HOME, MEG, ('Oldómedencés rendszer', 'oldomedences-rendszer')]
EPU = HUB + [('EPURECO termékcsalád', 'epureco')]


# ===========================================================================
# HUB
# ===========================================================================
def epit_hub():
    return [
        sec_prose('Az első tisztázandó', 'Nem tartály — rendszer', [
            'Az oldómedencés rendszer nem egyszerűen egy földbe helyezett tartály. '
            'A hatályos szabályozás szerint <strong>oldómedencéből és tisztítómezőből '
            'álló vízilétesítmény</strong>, amely energiabevitel nélkül végzi a '
            'szennyezőanyagok lebontását és a szennyvíz helyi elhelyezését.',
            'A folyamat kétlépcsős. Az <strong>oldómedencében</strong> ülepedés és '
            'anaerob — oxigén nélküli — előkezelés történik. Az előkezelt víz ezután a '
            '<strong>tisztítómezőbe</strong> kerül, ahol a talajban folytatódik az aerob '
            'kezelés. A tisztítás tehát nem fejeződik be a tartályban.',
            'Ezt azért mondjuk ki így, mert a korábbi tájékoztatásunk egy helyen úgy '
            'fogalmazott, hogy az oldómedence „csak tárolja és ülepíti” a szennyvizet. '
            'Ez magára a tartályra részben igaz, de a teljes rendszer leírásaként '
            'pontatlan — és éppen a lényeget hagyja ki.',
        ]),

        sec_split('Két lépcső', 'Mi történik hol',
                  'Oldómedence — első lépcső',
                  ['A szilárdabb részek leülepednek a fenékre',
                   'A könnyebb anyagok felúsznak, úszó réteget képeznek',
                   'Oxigénszegény környezetben anaerob bontás indul',
                   'A víz szűrőn keresztül halad tovább',
                   'Az iszap itt halmozódik fel — ezért kell időnként szippantani',
                   'Nem igényel villamos energiát'],
                  'Tisztítómező — második lépcső',
                  ['Az előkezelt víz elosztó rendszeren át jut a talajba',
                   'A talaj felső, levegős rétegében aerob folyamat zajlik',
                   'A tisztítás jelentős része ITT történik',
                   'Ezért a mező nem elvezetés, hanem technológiai elem',
                   'Területigénye jellemzően nagyobb, mint egy szikkasztóé',
                   'A mérete a talajtól és a terheléstől függ']),

        sec_prose('A fő előny — és a feltétele', 'Árammentes működés', [
            'A technológia legfontosabb előnye, hogy <strong>nem igényel villamos '
            'energiát</strong>. Nincs kompresszor, nincs levegőztetés, nincs vezérlés — '
            'és nincs olyan élő baktériumkultúra, amelyet folyamatos terheléssel kellene '
            'életben tartani.',
            'Ez különösen releváns nagy kihagyásokkal használt nyaralókban, hétvégi '
            'házakban és vadászházakban. Ott, ahol az aktív rendszer hosszú téli szünete '
            'külön eljárást igényelne, ez a technológia elnézőbb.',
            'Ebből viszont nem következik, hogy „nyaraló = oldómedence”. A tisztítómező '
            'megfelelő működéséhez elegendő terület, megfelelő talaj, kedvező talajvízi '
            'helyzet és szakszerű méretezés is kell. A 147/2010. Korm. rendelet maga is '
            'ezek figyelembevételéhez köti a létesítmény méretezését.',
        ]),

        sec_situations('A szakasz oldalai', 'Mit érdemes megnézni?',
                       'A sorrend a döntés logikáját követi: működés, alkalmasság, '
                       'kizárás, majd a telek és az üzemeltetés.',
                       [
                           ('nav-mukodes', 'Hogyan működik?',
                            'A szennyvíz útja az oldómedencétől a tisztítómezőn '
                            'keresztül a talajba. Két lépcső, egy rendszer.',
                            'oldomedence-hogyan-mukodik', 'Működés'),
                           ('nyaralo', 'Kinek megfelelő?',
                            'Nyaraló, hétvégi ház, vadászház — és az a négy feltétel, '
                            'amit az ingatlantípuson túl ellenőrizni kell.',
                            'oldomedence-kinek-megfelelo', 'Kinek megfelelő'),
                           ('nav-alternativak', 'Mikor nem megfelelő?',
                            'Az árammentesség önmagában nem teszi minden ingatlanhoz '
                            'megfelelővé. Kizárás és feltételes alkalmasság.',
                            'oldomedence-mikor-nem-megfelelo', 'Mikor nem'),
                           ('nav-talaj', 'Tisztítómező és területigény',
                            'A fő döntési korlát nem a tartály, hanem a mező. Mennyi '
                            'hely kell, és mitől függ.',
                            'oldomedence-tisztitomezo', 'Tisztítómező'),
                           ('nav-szerviz', 'Szippantás és karbantartás',
                            'Árammentes nem jelent karbantartásmentest: szippantás, '
                            'baktériumadalék, szűrő és a mező ellenőrzése.',
                            'oldomedence-szippantas-es-karbantartas', 'Karbantartás'),
                           ('nav-esettanulmany', 'Kapcsolódó esettanulmányok',
                            'Használati profil szerint: hétvégi ház, nyári nyaraló, '
                            'vadászház, hosszú téli távollét.',
                            'oldomedence-esettanulmanyok', 'Esettanulmányok'),
                       ]),

        sec_numbered('Amit vállalni kell', 'A rendszeres feladatok',
                     'Az árammentesség nem jelent teendőmentességet. Ezeket előre '
                     'érdemes átgondolni.',
                     ['<strong>Időszakos szippantás.</strong> A tartályban felhalmozódó '
                      'fenékiszapot és úszó réteget el kell távolítani. A gyakoriságról '
                      'lásd az alábbi megjegyzést — jelenleg ellentmondásos adataink '
                      'vannak, ezért nem közlünk számot.',
                      '<strong>Baktériumadalék.</strong> A jelenlegi tájékoztatásunk '
                      'rendszeres baktériumfrissítőt javasol, hosszabb kihagyás után '
                      'ismételt adagolással. Ez valós, visszatérő feladat és '
                      'fogyóeszköz-költség — lényeges különbség az aktív rendszerhez '
                      'képest, ahol a kultúra önfenntartó.',
                      '<strong>A szűrő ellenőrzése.</strong> Az oldómedence kimenetén '
                      'lévő szűrő eltömődhet; állapotát ellenőrizni kell.',
                      '<strong>A tisztítómező figyelése.</strong> Szag, nedvesedés a '
                      'felszínen vagy visszaduzzadás mind a mező telítődésének jele '
                      'lehet.',
                      '<strong>Dokumentáció.</strong> A jogszabály a keletkező hulladék '
                      'szabályos elhelyezéséhez kapcsolódó dokumentumok megőrzését is '
                      'előírja — a szippantási bizonylatokat érdemes megtartani.']),

        hiany('a szippantás tényleges gyakorisága. Két saját forrásunk ELTÉRŐEN '
              'fogalmaz: az EPURECO oldal kétévente, a 2023-as összehasonlítás 1,5 '
              'évente írja. Ezt nem szabad „átlagosan 1,5–2 évre" átírni',
              'GRAF aktuális ürítési kritériuma + ÖkoTech valós EPURECO ügyféladatok. '
              'Tisztázandó: milyen iszapszintig engedhető a tartály feltöltődése, és '
              'hogyan változik az intervallum a létszámmal. A végleges tartalom '
              'valószínűleg feltételhez kötött intervallumot vagy ellenőrzési szabályt '
              'igényel, nem fix számot'),

        sec_cta('Következő lépés', 'Előbb a működés',
                ['Ha érti a két lépcsőt, a többi kérdés — a területigény, a szippantás, '
                 'a baktériumadalék — magától adódik. Utána jön az, hogy illik-e az Ön '
                 'használatához.'],
                'Hogyan működik?', 'oldomedence-hogyan-mukodik',
                alt=('EPURECO termékcsalád', 'epureco')),

        sec_faq([
            ('Ez ugyanaz, mint az emésztő?',
             'Nem. Az emésztő jellemzően szigetelés és tisztítómező nélküli, gyakran '
             'szivárgó tároló. Az oldómedencés rendszer szigetelt tartályból és '
             'megfelelően méretezett tisztítómezőből álló, engedélyezhető vízilétesítmény, '
             'amelyben tényleges kezelés történik.'),
            ('Tényleg nem kell hozzá áram?',
             'Nem kell. Ez a technológia egyik fő előnye. Cserébe nagyobb területet '
             'igényel, rendszeres szippantást és baktériumadalékot kér, és a kilépő víz '
             'minősége nehezebben dokumentálható, mint egy aktív rendszernél.'),
            ('Mekkora területet igényel?',
             'Erre nem adunk egyetlen számot, mert a mező mérete a talaj mért '
             'szivárgóképességétől, a napi terheléstől és a talajvíztől függ. Ugyanaz a '
             'háztartás az egyik talajon jóval kisebb, a másikon többszörös felületet '
             'igényel — ezért kell mérés.'),
            ('Nyaralóhoz mindig ez a jó választás?',
             'Gyakran ez a relevánsabb irány, de nem automatikusan. A tisztítómező '
             'helyigénye, a talaj és a talajvíz ugyanúgy feltétel — és van olyan '
             'nyaraló, ahol éppen ezek miatt nem valósítható meg.'),
            ('Szagol?',
             'Rendeltetésszerű működésnél és megfelelő szellőzés mellett nem jellemző. '
             'A szag jelzés: telítődő tartály, eltömődött szűrő vagy telítődő '
             'tisztítómező egyaránt okozhatja — ilyenkor ellenőrzés szükséges.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 1) Hogyan működik?
# ===========================================================================
def epit_mukodes():
    return [
        sec_numbered('A folyamat', 'A szennyvíz útja lépésenként', '',
                     ['<strong>Beérkezés az oldómedencébe.</strong> A háztartási '
                      'szennyvíz gravitációsan érkezik a tartályba.',
                      '<strong>Ülepedés és úszó réteg.</strong> A nehezebb szilárd rész '
                      'a fenékre süllyed, a könnyebb — zsír, olaj — a felszínen úszó '
                      'réteget képez. A kettő között marad a viszonylag tisztább '
                      'folyadékfázis.',
                      '<strong>Anaerob bontás.</strong> Az oxigénszegény környezetben '
                      'baktériumok bontják a szerves anyagot. Ez lassabb folyamat, mint '
                      'az aerob, és nem is végzi el a teljes tisztítást.',
                      '<strong>Szűrés.</strong> A kilépő oldalon szűrő tartja vissza a '
                      'továbbhaladó szilárd részecskéket. Ez védi a tisztítómezőt az '
                      'eltömődéstől — ezért kell rendszeresen ellenőrizni.',
                      '<strong>A tisztítómező.</strong> Az előkezelt víz elosztó '
                      'rendszeren keresztül, egyenletesen jut a talajba. Itt zajlik a '
                      'rendszer második kezelési szakasza.',
                      '<strong>Aerob kezelés a talajban.</strong> A mező felső, levegős '
                      'rétegében élő mikroorganizmusok bontják tovább a szerves anyagot. '
                      'Ehhez oxigén kell — ezért kritikus, hogy a réteg ne tömörödjön be.',
                      '<strong>Elhelyezés a talajban.</strong> A megtisztított víz a '
                      'mélyebb rétegekbe szivárog.']),

        sec_prose('Miért nem elég a tartály', 'A leggyakoribb félreértés', [
            'Az oldómedence önmagában előkezel: ülepít és anaerob módon bont. '
            'A <em>tisztítás</em> érdemi része viszont a tisztítómezőben, a talaj felső, '
            'levegős rétegében történik — ott, ahol oxigén áll rendelkezésre.',
            'Ezért nem lehet a mezőt elhagyni, kisebbre venni vagy „majd később '
            'megcsináljuk” alapon halasztani. Tisztítómező nélkül nem oldómedencés '
            'rendszerről beszélünk, hanem egy szigetelt tárolóról, ami előbb-utóbb '
            'megtelik.',
            'És ezért nem lehet a mezőt szabadon áthelyezni sem: a helye, mérete és '
            'kialakítása a technológia része, nem elrendezési kérdés.',
        ]),

        sec_split('Mi kell hozzá, és mi nem', 'A működés feltételei',
                  'Nem kell hozzá',
                  ['Villamos energia',
                   'Kompresszor, levegőztetés',
                   'Vezérlés, automatika',
                   'Folyamatos terhelés a biológia fenntartásához',
                   'Rendszeres áramfogyasztás'],
                  'Kell hozzá',
                  ['Gravitációs vagy műszakilag kialakított vízvezetés',
                   'Megfelelő szellőzés',
                   'Megfelelően MÉRETEZETT tisztítómező',
                   'Alkalmas talaj és kedvező talajvízi helyzet',
                   'Elegendő szabad terület',
                   'Időszakos szippantás és baktériumadalék']),

        hiany('az ÖkoTech által ténylegesen telepített konfiguráció metszete: a szűrő '
              'típusa, a szellőző kialakítása, a tisztítómező típusa, valamint a '
              'gravitációs és szivattyús változatok',
              'ÖkoTech műszaki dokumentáció + GRAF telepítési útmutató. Egy sematikus '
              'metszeti ábra ezen az oldalon többet érne, mint bármelyik bekezdés'),

        sec_cta('Következő lépés', 'Illik ez az Ön használatához?',
                ['A működés megértése után jön a kérdés, hogy a saját használati '
                 'helyzete illeszkedik-e hozzá — és hogy a telek elbírja-e a '
                 'tisztítómezőt.'],
                'Kinek megfelelő?', 'oldomedence-kinek-megfelelo',
                alt=('Tisztítómező és területigény', 'oldomedence-tisztitomezo')),

        sec_faq([
            ('Miért kell szippantani, ha a baktériumok lebontják?',
             'Mert az anaerob bontás nem tünteti el a szilárd anyagot, csak részben '
             'bontja. Ami marad — a nem bomló rész és a bomlás melléktermékei — a fenéken '
             'halmozódik fel. Ezt időnként el kell távolítani, különben elszűkíti a '
             'tartályt és a szűrőt is terheli.'),
            ('Mi történik télen?',
             'A folyamat lassul, de nem áll le. A tartály a talajban van, ami '
             'hőmérsékleti szempontból kedvező. Éppen a téli, alacsony terhelésű időszakot '
             'tűri jól ez a technológia — ezért releváns szezonális ingatlanoknál.'),
            ('Mennyi ideig működik egy ilyen rendszer?',
             'A tartály hosszú élettartamú, de a tisztítómező élettartama a '
             'terheléstől, a talajtól és a karbantartástól függ. Az eltömődött vagy '
             'telítődött mező felújítása jelentős munka — ezért fontos a helyes méretezés '
             'és a mező fölötti terület védelme.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 2) Kinek megfelelő?
# ===========================================================================
def epit_kinek():
    return [
        sec_prose('Az elsődleges helyzet', 'Időszakosan használt ingatlan', [
            'A technológia elsődleges alkalmazási területe a <strong>nem folyamatosan '
            'használt ingatlan</strong>: nyaraló, hétvégi ház, vadászház, hétvégi telek.',
            'Ezekben a helyzetekben az árammentes működés valódi előny. Nem kell '
            'elektromos üzemet fenntartani egy hónapokig üres ingatlanon, és nincs élő '
            'baktériumkultúra, amelyet a hosszú távollét megviselne. A rendszer '
            'egyszerűen vár.',
            'Ez viszont nem automatikus szabály. Az alkalmasságot nem az ingatlantípus '
            'dönti el, hanem négy feltétel — és mind a négynek teljesülnie kell.',
        ]),

        sec_numbered('A négy feltétel', 'Amit az ingatlantípuson túl ellenőrizni kell', '',
                     ['<strong>Kommunális jellegű szennyvíz.</strong> Konyha, '
                      'fürdőszoba, WC. Jelentős konyhai, technológiai vagy ipari terhelés '
                      'esetén a rendszer nem méretezhető pusztán a személyszámból.',
                      '<strong>Alkalmas talaj.</strong> A tisztítómező működéséhez a '
                      'talajnak be kell fogadnia a vizet. Ezt mérni kell — a talaj neve '
                      'nem elegendő adat.',
                      '<strong>Kedvező talajvízi helyzet.</strong> A mezőnek a talajvíz '
                      'fölött, levegős rétegben kell működnie. Magas talajvíznél ez '
                      'korlát lehet.',
                      '<strong>Elegendő terület.</strong> A tisztítómező helyigénye a '
                      'legnagyobb tényleges korlát — nagyobb, mint egy aktív rendszer '
                      'szikkasztójáé. Ezt a ház, a kút, a behajtó és a tervezett '
                      'építmények után maradó területen kell elhelyezni.']),

        sec_split('Tipikus helyzetek', 'Hol jó választás, és hol kell vizsgálat',
                  'Jellemzően jó választás',
                  ['Csak nyáron használt nyaraló',
                   'Hétvégi ház, hosszabb szünetekkel',
                   'Vadászház, szezonális használattal',
                   'Ingatlan, ahol nincs vagy bizonytalan az áramellátás',
                   'Nagy telek, ahol elfér a tisztítómező',
                   'Jó vízáteresztő talaj, alacsony talajvíz'],
                  'Itt külön vizsgálat kell',
                  ['Életvitelszerűen lakott családi ház',
                   'Kis vagy erősen beépített telek',
                   'Kötött, agyagos talaj',
                   'Magas vagy szezonálisan magas talajvíz',
                   'Kút közelsége, vízbázisvédelmi helyzet',
                   'Nagykonyhai vagy nem kommunális terhelés']),

        sec_prose('Állandó lakhatásnál', 'Miért javasoljuk inkább az aktív rendszert', [
            'Életvitelszerűen használt családi háznál jellemzően az aktív biológiai '
            'rendszert javasoljuk. Ott a folyamatos terhelés éppen az, amire az a '
            'technológia való, a kilépő víz minősége mérhetően jobb, és a helyigény '
            'kisebb.',
            'Ez nem azt jelenti, hogy állandó lakhatásnál kizárt az oldómedencés '
            'rendszer — inkább azt, hogy ott a nagyobb tisztítómező és a rendszeres '
            'szippantás olyan ár, amiért cserébe nem kapunk annyit, mint egy '
            'szezonális ingatlanon.',
            'Ha mégis ez az irány — például mert nincs áram —, a telek adottságait '
            'különösen alaposan meg kell nézni, mert az állandó használat nagyobb '
            'terhelést és nagyobb mezőt jelent.',
        ]),

        hiany('az EPURECO-projektek megoszlása használati gyakoriság szerint, a nyaralók '
              'téli üzemének tapasztalatai, hogy mennyi kihagyás után milyen teendőt '
              'javasol az ÖkoTech, valamint az állandó használatú projektek száma és '
              'tapasztalata',
              'ÖkoTech projektarchívum és szerviz. Külön ellenőrizendő az az állítás, '
              'hogy a baktériumok szennyvíz nélkül is életben maradnak — ezt gyártói '
              'dokumentáció alapján kell pontosítani, nem általános biológiai tényként '
              'kommunikálni'),

        sec_cta('Következő lépés', 'A telek dönt',
                ['Az alkalmasság érdemi része a tisztítómezőn múlik: elfér-e a szükséges '
                 'felület, és befogadja-e a talaj a napi vízmennyiséget.'],
                'Tisztítómező és területigény', 'oldomedence-tisztitomezo',
                alt=('Mikor nem megfelelő?', 'oldomedence-mikor-nem-megfelelo')),

        sec_faq([
            ('Nyaralóhoz ez a legjobb megoldás?',
             'Gyakran a relevánsabb irány, különösen hosszú téli kihagyásnál vagy ha '
             'nincs áram. De nem automatikus: a tisztítómező helyigénye, a talaj és a '
             'talajvíz ugyanúgy feltétel. Van olyan nyaraló, ahol éppen ezek miatt nem '
             'valósítható meg.'),
            ('Családi házba is jó?',
             'Életvitelszerű használatnál jellemzően az aktív biológiai rendszert '
             'javasoljuk — jobb kilépővíz-minőség, kisebb helyigény. Az oldómedencés '
             'rendszer ott elsősorban akkor jön szóba, ha nincs vagy bizonytalan az '
             'áramellátás, és a telek elbírja a nagyobb mezőt.'),
            ('Mi van, ha évekig nem használjuk?',
             'A rendszer tűri a hosszú szünetet — ez az egyik fő előnye. Hosszabb '
             'kihagyás után baktériumadalék adagolása javasolt az újraindításhoz. '
             'A pontos eljárást a berendezés dokumentációja rögzíti.'),
            ('Kell hozzá szippantás nyaralónál is?',
             'Igen, csak ritkábban, mert kevesebb a terhelés. A gyakoriság a tartály '
             'méretétől, a létszámtól és a használat intenzitásától függ — ezért nem '
             'közlünk fix intervallumot.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 3) Mikor nem megfelelő?
# ===========================================================================
def epit_mikor_nem():
    return [
        sec_prose('Az árammentesség nem mindenre válasz', '', [
            'Az oldómedencés rendszer egyszerű és nem igényel villamos energiát. Ettől '
            'viszont még nem lesz minden közcsatorna nélküli ingatlan számára megfelelő — '
            'és a leggyakoribb korlát nem is a tartály, hanem a tisztítómező.',
            'Ez az oldal külön kezeli azt, ami <strong>kizárás</strong>, és azt, ami '
            '<strong>további vizsgálattal megfelelő</strong> lehet. A kettő nem ugyanaz, '
            'és a következmény sem.',
        ]),

        sec_split('Két súlyosság', 'Kizárás és feltételes alkalmasság',
                  'Jellemzően kizárás',
                  ['Nincs elegendő terület a megfelelő méretű tisztítómezőnek',
                   'A talaj szivárgási képessége nem elegendő, és nem javítható',
                   'Az egyedi rendszer jogi alkalmazhatósága nem igazolt az adott helyen',
                   'Nem kommunális, technológiai eredetű szennyvíz vizsgálat nélkül',
                   'Jelentős nagykonyhai vagy ipari terhelés előkezelés nélkül'],
                  'Külön vizsgálattal megfelelő lehet',
                  ['Magas talajvíz — a mező elhelyezése módosítható',
                   'Kötött talaj — nagyobb mező vagy más kialakítás',
                   'Kisebb telek — az elrendezés dönt, nem a négyzetméter',
                   'Kút közelsége — a mező helye áthelyezhető',
                   'Életvitelszerű használat — nagyobb mező, gyakoribb szippantás',
                   'Ezekben mérés és szakértői vélemény zárja le a kérdést']),

        sec_prose('Ami nem műszaki kizárás', 'A vállalhatóság kérdése', [
            'Van, amikor a rendszer műszakilag megvalósítható, de a tulajdonos nem '
            'vállalja, ami vele jár. Ez teljesen legitim döntés — csak nem műszaki '
            'kizárás, hanem használati ellenérv, és ezért külön kategória.',
            'Ide tartozik a <strong>rendszeres szippantás</strong> megszervezése és '
            'költsége, valamint a <strong>baktériumadalék</strong> rendszeres adagolása. '
            'Egyik sem nagy feladat, de mindkettő visszatérő, és ha valaki ezeket '
            'eleve nem akarja, akkor nem fog jól működni a rendszer.',
            'Ilyenkor érdemes megnézni, mit ad cserébe az aktív biológiai rendszer: '
            'ott nincs rendszeres szippantás és nincs adalékolás, viszont villamos '
            'energia és rendszeres ellenőrzés kell hozzá.',
        ]),

        sec_numbered('Az eredmény', 'Négy lehetséges kimenet', '',
                     ['<strong>Nem javasolt.</strong> Az ismert körülmények alapján a '
                      'technológia nem alkalmas — jellemzően a tisztítómező helyigénye '
                      'vagy a talaj miatt.',
                      '<strong>Telekvizsgálat szükséges.</strong> Nem a technológia a '
                      'kérdés, hanem a telek adottságai. Szivárogtatási vizsgálat és a '
                      'talajvíz tisztázása következik.',
                      '<strong>Biológiai rendszer vizsgálandó.</strong> A használati '
                      'profil vagy a helyszűke miatt az aktív rendszer lehet '
                      'kedvezőbb — érdemes a kettőt egymás mellett megnézni.',
                      '<strong>Más megoldás szükséges.</strong> Ha sem a helyi '
                      'elhelyezés, sem a biológiai rendszer nem jön szóba, a zárt '
                      'tároló vagy más irány marad.']),

        hiany('a tényleges EPURECO-elutasítások okai, a technológiaváltások esetei, a '
              'talaj és talajvíz miatt meghiúsult projektek, a maximális standard '
              'terhelési szabály és a nem kommunális terhelésre vonatkozó kizárás',
              'ÖkoTech értékesítés és műszaki csapat'),

        sec_cta('Következő lépés', 'Nézze meg a másik irányt is',
                ['Ha a helyszűke vagy az életvitelszerű használat miatt bizonytalan, '
                 'érdemes a két technológiát egymás mellett megnézni ugyanazon '
                 'szempontok szerint.'],
                'Megoldástípusok összehasonlítása', 'megoldastipusok-osszehasonlitasa',
                alt=('Biológiai szennyvíztisztítás', 'biologiai-szennyviztisztitas')),

        sec_faq([
            ('Kis telken kizárt?',
             'Nem automatikusan, de ez a leggyakoribb korlát. A tisztítómező helyigénye '
             'jellemzően nagyobb, mint egy aktív rendszer szikkasztójáé — ezért kis '
             'telken gyakran az aktív rendszer marad reális. A döntéshez mérés kell, nem '
             'becslés.'),
            ('Agyagos talajon működik?',
             'Nehezebben, nagyobb mezővel, és van, ahol nem. Ezt szivárogtatási '
             'vizsgálat dönti el. Ha a talaj nem fogadja be a napi vízmennyiséget, a '
             'technológiaváltás önmagában nem segít — mert az aktív rendszer '
             'szikkasztójának is be kell fogadnia a vizet.'),
            ('Nem akarok szippantással foglalkozni.',
             'Ez érvényes szempont, és nem kell szégyellni. Ilyenkor érdemes az aktív '
             'biológiai rendszert megnézni: ott nincs rendszeres szippantás, viszont '
             'villamos energia és rendszeres ellenőrzés kell hozzá. A két rendszer más '
             'terhet ró a tulajdonosra.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 4) Tisztítómező és területigény
# ===========================================================================
def epit_tisztitomezo():
    return [
        sec_prose('A központi állítás', 'A mező a rendszer része, nem kiegészítő', [
            'Az oldómedencés rendszer nem a földbe helyezett tartály, hanem a '
            'megfelelően kialakított <strong>tisztítómezővel együtt működő rendszer</strong>. '
            'A tartály az első, mechanikai és anaerob kezelési lépcső; a második kezelési '
            'szakasz a mezőben történik.',
            'Ebből következik a legfontosabb gyakorlati szabály: a lebontási folyamat '
            'nagy része a tisztítómezőben zajlik, ezért annak megfelelő mérete '
            'meghatározó jelentőségű. Nem az a kérdés, hogy elfér-e a tartály — hanem '
            'hogy elfér-e a mező.',
        ]),

        sec_numbered('Mitől függ a szükséges terület', 'Öt tényező együtt',
                     'Ezért nem adható fix négyzetméter/fő szabály: egyetlen tényező '
                     'megváltozása többszörösére növelheti a szükséges felületet.',
                     ['<strong>A talaj MÉRT szivárgóképessége.</strong> Nem a talaj neve, '
                      'hanem a szivárogtatási vizsgálat eredménye. Ez a legerősebben ható '
                      'tényező.',
                      '<strong>A napi szennyvízmennyiség.</strong> A háztartás '
                      'terheléséből adódik. Nagyobb terhelés arányosan nagyobb mezőt '
                      'igényel.',
                      '<strong>A talajvíz.</strong> A mezőnek a talajvíz fölött, levegős '
                      'rétegben kell működnie — a szezonális maximumon is.',
                      '<strong>A mező kialakítása.</strong> Perforált drén, szikkasztó '
                      'kamra vagy más elosztóelem eltérő felületigénnyel dolgozik.',
                      '<strong>A gyártói méretezési szabály.</strong> A konkrét '
                      'termékrendszerhez tartozó előírás, amely a fentieket összeköti.']),

        sec_split('A mező fölött', 'Mit lehet, és mit nem',
                  'Jellemzően megengedett',
                  ['Gyep és sekély gyökérzetű növényzet',
                   'Alkalmi gyalogos használat',
                   'Szabadon hagyott, gondozott zöldfelület',
                   'A mező nyomvonalának ismerete és megjelölése'],
                  'Nem javasolt vagy tiltott',
                  ['Burkolás, betonozás, tömörítés',
                   'Mély gyökérzetű fa és cserje telepítése',
                   'Csapadékvíz rávezetése — a mező többletterhelést kap',
                   'Építmény elhelyezése a mező fölé vagy közvetlen mellé',
                   'A terület megbontása az elosztás nyomvonalának ismerete nélkül']),

        hiany('a járműterhelhető kialakítás pontos feltételei. A jelenlegi '
              'tájékoztatásunk azt állítja, hogy megfelelő földtakarással gépkocsibeálló '
              'alatt is kialakítható a mező — ezt konkrét terméktípusra, fedési és '
              'terhelési feltételekre kell visszavezetni, nem általános ígéretként '
              'használni',
              'GRAF aktuális tervezési útmutató + ÖkoTech által alkalmazott rétegrend. '
              'Szintén hiányzik: az ÖkoTech által használt tisztítómező-elemek köre, a '
              'méretezési algoritmus, a szivárogtatási eredmény → mezőméret megfeleltetés '
              'és az eliszapolódott mezők tapasztalatai'),

        sec_numbered('Helyszínrajz', 'Mit jelöljön be a területellenőrzéshez?',
                     'Kézzel rajzolt, méretarányos vázlat is megfelel.',
                     ['A ház körvonala és a szennyvízcső kilépési pontja',
                      'A tervezett oldómedence helye',
                      'A tisztítómezőnek szánt terület',
                      'A kút vagy kutak helye — a szomszédos telkeken lévőkkel együtt',
                      'Behajtó, gépkocsibeálló, burkolt felületek',
                      'Ismert közművek nyomvonala',
                      'Nagy fák és megtartandó növényzet',
                      'A tereplejtés iránya',
                      'A későbbre tervezett építmények — ez marad ki a leggyakrabban']),

        sec_cta('Következő lépés', 'A mező méretéhez mérés kell',
                ['A tisztítómező méretezésének bemenete a talaj mért szivárgóképessége. '
                 'Enélkül minden méret becslés — és a rosszul méretezett mező '
                 'helyreállítása jelentős munka.'],
                'Szivárogtatási vizsgálat',
                '../projekt-elokeszites/szivarogtatasi-vizsgalat',
                alt=('Telekalkalmasság', '../projekt-elokeszites/telekalkalmassag')),

        sec_faq([
            ('Hány négyzetméter kell?',
             'Erre szándékosan nem adunk számot, mert a talaj mért szivárgóképessége '
             'nélkül nem lenne megalapozott. Ugyanaz a háztartás az egyik talajon '
             'jóval kisebb, a másikon többszörös felületet igényel. A mérés a bemenet.'),
            ('Lehet a mező fölé parkolót építeni?',
             'A jelenlegi tájékoztatásunk említ ilyen lehetőséget megfelelő '
             'földtakarással, de ezt konkrét terméktípusra és rétegrendre kell '
             'visszavezetni. Amíg ez nincs dokumentálva, nem ígérjük meg — kérdezze meg '
             'a konkrét projektnél.'),
            ('Mi történik, ha eltömődik a mező?',
             'A víz nem szivárog el elég gyorsan, visszaduzzad, a felszínen nedvesedés '
             'jelentkezhet, és a tisztítás hatásfoka romlik. Az okok között tömörítés, '
             'túlterhelés, csapadékvíz rávezetése és elmaradt szippantás egyaránt lehet. '
             'A helyreállítás jellemzően a mező részleges vagy teljes újraépítése.'),
            ('Bővíthető később a mező?',
             'Elvileg igen, ha van hová. Ezért érdemes már a tervezéskor számolni a '
             'bővítés lehetőségével — és nem beépíteni a mellette lévő területet.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 5) Szippantás és karbantartás
# ===========================================================================
def epit_karbantartas():
    return [
        sec_prose('Árammentes ≠ karbantartásmentes', '', [
            'Az, hogy a rendszer nem igényel villamos energiát, nem jelenti azt, hogy nem '
            'igényel figyelmet. Az oldómedencében felhalmozódó fenékiszapot és úszó '
            'réteget időszakosan el kell távolítani, a szűrő és a tisztítómező állapotát '
            'pedig ellenőrizni kell.',
            'Ehhez jön a <strong>baktériumadalék</strong> rendszeres adagolása, ami '
            'lényeges különbség az aktív biológiai rendszerhez képest — ott a kultúra '
            'önfenntartó. Ez visszatérő feladat és fogyóeszköz-költség.',
            'Egyik sem nagy teher, de mindkettő rendszeres. Aki ezeket előre tudja, nem '
            'fog csalódni.',
        ]),

        sec_numbered('Szippantás', 'Miért, mikor és mi alapján', '',
                     ['<strong>Miért.</strong> Az anaerob bontás nem tünteti el a szilárd '
                      'anyagot. Ami marad, a fenéken halmozódik fel, és idővel elszűkíti '
                      'a tartályt, terheli a szűrőt és a tisztítómezőt.',
                      '<strong>Mi alapján.</strong> Az iszapszint a mérvadó, nem a '
                      'naptár. A tartály feltöltöttségét ellenőrizni kell — a naptári '
                      'ciklus csak durva iránymutatás.',
                      '<strong>Mi befolyásolja.</strong> A tartály mérete, a használói '
                      'létszám, a használat intenzitása és a felhalmozódott iszap '
                      'mennyisége. Egy ritkán használt nyaralónál lényegesen ritkább, '
                      'mint egy állandóan lakott háznál.',
                      '<strong>Dokumentáció.</strong> A jogszabály a keletkező hulladék '
                      'szabályos elhelyezéséhez kapcsolódó dokumentumok megőrzését is '
                      'előírja. A szippantási bizonylatokat tehát érdemes megtartani.']),

        hiany('a szippantás tényleges gyakorisága. Két saját forrásunk eltérően '
              'fogalmaz: az EPURECO oldal kétévente, a 2023-as összehasonlítás 1,5 '
              'évente. Ezt NEM „1,5–2 évre" kell átírni',
              'GRAF hivatalos ürítési kritériuma (milyen iszapszintig engedhető a '
              'feltöltődés) + ÖkoTech valós EPURECO szippantási adatok létszám szerint. '
              'A végleges tartalom valószínűleg feltételhez kötött intervallum vagy '
              'ellenőrzési szabály lesz, nem fix szám'),

        sec_split('Ki mit csinál', 'Felelősségi megosztás',
                  'A tulajdonos feladata',
                  ['Az iszapszint időszakos ellenőrzése',
                   'A szűrő állapotának ellenőrzése, szükség szerinti tisztítása',
                   'A baktériumadalék rendszeres adagolása',
                   'A tisztítómező feletti terület védelme',
                   'A szippantás megszervezése és a bizonylatok megőrzése',
                   'Szag, nedvesedés vagy visszaduzzadás esetén jelzés'],
                  'Szolgáltató vagy szakember',
                  ['A szippantás elvégzése — engedéllyel rendelkező szolgáltató',
                   'A hulladék szabályos elhelyezése és igazolása',
                   'Szag, visszaduzzadás vagy eliszapolódás kivizsgálása',
                   'A tisztítómező állapotának szakmai megítélése',
                   'Meghibásodás vagy telítődés esetén helyreállítás',
                   'Hosszabb kihagyás utáni újraindítás tanácsadása']),

        sec_numbered('Figyelmeztető jelek', 'Mikor kell szakember?',
                     'Ezek mindegyike arra utal, hogy valami nem a tervezett módon '
                     'működik — és minél előbb derül ki, annál egyszerűbb kezelni.',
                     ['Szag a tartály vagy a mező környékén, tartósan',
                      'Nedvesedés vagy pangó víz a tisztítómező fölött',
                      'Visszaduzzadás a házban — lassan folyó lefolyó, gurgulázás',
                      'A tartály a vártnál gyorsabban telik',
                      'A szűrő gyakran eltömődik',
                      'Szokatlanul buja növényzet a mező fölött — a telítődés jele lehet']),

        sec_cta('Következő lépés', 'Nézzen meg működő példákat',
                ['Az esettanulmányok használati profil szerint mutatják a valós '
                 'szippantási előzményt, adalékhasználatot és a mező állapotát — ez '
                 'többet mond, mint bármelyik általános szabály.'],
                'Kapcsolódó esettanulmányok', 'oldomedence-esettanulmanyok',
                alt=('EPURECO termékcsalád', 'epureco')),

        sec_faq([
            ('Milyen gyakran kell szippantani?',
             'Erre most nem adunk számot, mert két saját forrásunk eltérően fogalmaz, és '
             'ezt gyártói útmutató és valós üzemeltetési adat alapján kell rendezni. Ami '
             'biztos: az iszapszint a mérvadó, nem a naptár, és a gyakoriságot a tartály '
             'mérete és a használat intenzitása határozza meg.'),
            ('Mennyibe kerül a szippantás?',
             'Konkrét összeget nem közlünk: a szippantási díjak helyenként és időben is '
             'eltérnek. Ami tervezhető: hogy ez visszatérő üzemeltetési költség, és a '
             'ritkábban használt ingatlanoknál lényegesen kevesebbszer jelentkezik.'),
            ('Tényleg kell baktériumadalék?',
             'A jelenlegi tájékoztatásunk rendszeres adagolást javasol, hosszabb kihagyás '
             'után ismételt frissítést. Ezt a berendezéshez tartozó gyártói útmutató '
             'rögzíti pontosan — a konkrét terméknél ezt kérje el.'),
            ('Mit tegyek, ha szagot érzek?',
             'Először ellenőrizze a szellőzést és a szűrőt. Ha a szag tartós, vagy a mező '
             'fölött nedvesedés is van, az telítődésre utalhat — ilyenkor érdemes '
             'szakemberrel megnézetni, mielőtt a mező tartósan károsodik.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 6) Kapcsolódó esettanulmányok
# ===========================================================================
def epit_esettanulmanyok():
    return [
        sec_prose('Mit keresünk egy esettanulmányban', '', [
            'Ez az oldal kizárólag olyan projekteket mutat, ahol dokumentáltan '
            'oldómedencés rendszer készült — nem keveredik össze a más technológiájú '
            'referenciákkal.',
            'A rendezés elve a <strong>használati profil</strong>: hétvégi ház, csak '
            'nyáron használt nyaraló, vadászház, hosszú téli távollét, illetve olyan '
            'helyzet, ahol az árammentes működés volt a technológiaválasztás fő oka.',
            'Ez azért fontos, mert a technológia alkalmassága éppen a használati '
            'mintától függ — nem az ingatlan méretétől vagy típusától.',
        ]),

        sec_numbered('Amit minden esethez tudni érdemes', 'A hasznos esetlap adatai',
                     'Ezek nélkül a referencia illusztráció, nem bizonyíték.',
                     ['Az ingatlan típusa és a telepítés éve',
                      'A tartálymodell és a névleges kapacitás',
                      'Átlagos és maximális létszám',
                      'Használati hónapok és a leghosszabb kihagyás',
                      'A talaj és a talajvízi helyzet',
                      'A tisztítómező mérete és típusa',
                      'A technológiaválasztás indoka',
                      'Tényleges szippantási előzmény — mikor, milyen gyakran',
                      'Baktériumadalék használata',
                      'A szűrő karbantartása és a mező állapota',
                      'Szervizesemény, ha volt',
                      'Mit bizonyít az eset — és mit nem']),

        sec_prose('Amit ezeknek az eseteknek igazolniuk kell', '', [
            'A jelenlegi tájékoztatásunk erős általános állításokat tesz: hogy a rendszer '
            'jól tűri a szezonális használatot, hogy a szippantás ritkán szükséges, és '
            'hogy a karbantartás minimális.',
            'Éppen ezeket a pontokat kell valós projektadatokkal igazolni. Egy több éve '
            'működő nyaralós rendszer szippantási előzménye, adalékhasználata és a mező '
            'állapota közvetlenül bizonyítja vagy cáfolja ezeket az állításokat.',
            'Ha ilyen adat nincs, akkor az állítás sem szerepelhet erős formában. Ez a '
            'rend — nem fordítva.',
        ]),

        hiany('maga az esettanulmány-tár. Az EPURECO telepítési adatbázis, a '
              'megrendelések modellazonosítással, helyszínrajzok, telepítési fotók, '
              'szerviz- és szippantási adatok, ügyfél-visszajelzések, valamint a több '
              'mint 3–5 éve működő rendszerek adatai',
              'ÖkoTech projektarchívum. Ha nincs elegendő oldómedencés esettanulmány, '
              'azt belső archívumból kell felépíteni — NEM más technológiájú '
              'referenciával kitölteni'),

        sec_cta('Következő lépés', 'A saját helyzetéhez keresünk hasonlót',
                ['Írja meg, hogyan használják az ingatlant — hány hónapban, hányan, '
                 'mennyi a leghosszabb kihagyás —, és megnézzük, van-e dokumentált, '
                 'hasonló projektünk.'],
                'Kapcsolatfelvétel', '../kapcsolat',
                alt=('Kinek megfelelő?', 'oldomedence-kinek-megfelelo')),

        sec_faq([
            ('Miért nincs itt sok esettanulmány?',
             'Mert csak olyat mutatunk, ahol ténylegesen oldómedencés rendszer működik, '
             'és ahol a döntéshez szükséges adatok is rendelkezésre állnak. Ezek '
             'összegyűjtésén dolgozunk — inkább kevesebb, de használható eset, mint sok '
             'fotó adat nélkül.'),
            ('Beszélhetek egy meglévő tulajdonossal?',
             'Ez az ügyfél hozzájárulásán múlik, de több esetben megoldható. Egy több éve '
             'működő rendszer tulajdonosa jellemzően pontosabban tud mesélni a '
             'szippantásról és a mindennapokról, mint bármelyik adatlap.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# ALHUB — EPURECO termékcsalád
# ===========================================================================
def epit_epu_hub():
    return [
        sec_prose('Itt már a termékről van szó', '', [
            'Az eddigi oldalak az oldómedencés technológiáról szóltak. Ez az oldal arról, '
            'hogy az ÖkoTech milyen konkrét rendszert kínál — és hogyan áll össze belőle '
            'a teljes megoldás.',
            'Az EPURECO tartályokat a <strong>GRAF</strong> gyártja. A gyártói leírás '
            'szerint a tartály a házi szennyvízkezelés <strong>anaerob első '
            'szakasza</strong>; a második kezelési lépcső a tisztítómezőben történik. '
            'A tartály tehát nem önálló kész megoldás.',
        ]),

        sec_numbered('A választás logikája', 'Négy lépés, ebben a sorrendben',
                     'Ez a sorrend szándékos. A modell kiválasztása nem az első lépés, '
                     'hanem a harmadik — mert rossz tisztítómezővel a megfelelő méretű '
                     'tartály sem alkot megfelelő rendszert.',
                     ['<strong>Használati profil.</strong> Hogyan használják az '
                      'ingatlant: hány hónapban, hányan, mennyi a leghosszabb kihagyás.',
                      '<strong>Telek és szivárgási képesség.</strong> Befogadja-e a talaj '
                      'a napi vízmennyiséget, és elfér-e a szükséges mező.',
                      '<strong>Tartálymodell.</strong> A használói kapacitás alapján, '
                      'a névleges térfogattal együtt.',
                      '<strong>Tisztítómező.</strong> A mért szivárgás és a napi terhelés '
                      'alapján méretezve. Ez zárja le a rendszert.']),

        sec_numbered('A jelenlegi gyártói kínálat', 'Három tartályméret',
                     'A modellnévben lévő szám a névleges használói kapacitásra utal, a '
                     'hozzá tartozó térfogat pedig a tartály mérete. Ezek a GRAF nyilvános '
                     'adatai — hogy közülük az ÖkoTech ma pontosan melyeket forgalmazza '
                     'Magyarországon, belső termékadatból egyértelműsítendő.',
                     ['<strong>EPURECO 4</strong> — 2100 liter névleges térfogat',
                      '<strong>EPURECO 6</strong> — 2700 liter névleges térfogat',
                      '<strong>EPURECO 7</strong> — 3400 liter névleges térfogat']),

        sec_prose('Amit a modellnév nem mond meg', 'A tartály önmagában nem rendszer',
                  ['A modellnévben szereplő személyszám <strong>csak a tartály '
                   'kiválasztásának egyik bemenete</strong>. A teljes rendszer '
                   'alkalmasságához külön kell méretezni a tisztítómezőt a telek és a '
                   'használat alapján.',
                   'Ezért nincs ezen az oldalon „kiválasztom és megrendelem" logika: '
                   'rossz mezővel a megfelelő méretű tartály sem alkot megfelelő '
                   'rendszert. A döntő kérdés az, mekkora felület kell, elfér-e a telken, '
                   'és befogadja-e a talaj a napi vízmennyiséget.']),

        sec_situations('A termékcsalád oldalai', 'Mit szeretne megnézni?', '',
                       [
                           ('nav-terheles', 'Modellek és kapacitások',
                            'Névleges kapacitás, tartálytérfogat, méretek — egységes '
                            'adatstruktúrában.',
                            'epureco-modellek-es-kapacitasok', 'Modellek'),
                           ('nav-biologiai', 'Műszaki adatok',
                            'Tartályadatok, szűrő, be- és kifolyó, telepítési '
                            'paraméterek, CE és EN 12566-1.',
                            'epureco-muszaki-adatok', 'Műszaki adatok'),
                           ('nav-telepites', 'Telepítési feltételek',
                            'A tartály és a tisztítómező együtt — földmunka, talajvíz, '
                            'szellőzés, hozzáférés.',
                            'epureco-telepitesi-feltetelek', 'Telepítés'),
                           ('nav-tanusitvany', 'Dokumentumok',
                            'Adatlap, teljesítménynyilatkozat, telepítési és '
                            'üzemeltetési utasítás — verzióval és dátummal.',
                            'epureco-dokumentumok', 'Dokumentumok'),
                       ]),

        hiany('pontosan mely EPURECO modelleket forgalmazza ma az ÖkoTech '
              'Magyarországon, van-e eltérés a GRAF aktuális kínálatához képest, milyen '
              'tisztítómező-csomagokat kínálunk hozzájuk, valamint az aktuális garancia- '
              'és szállítási feltételek',
              'ÖkoTech értékesítés + GRAF aktuális terméklista. A régi vagy külföldi '
              'kereskedői katalógus alapján NEM szabad modellt hozzáadni'),

        sec_cta('Következő lépés', 'Előbb a használati profil',
                ['A modellválasztás bemenete az, hogyan használják az ingatlant, és mit '
                 'bír a telek. Ha ez megvan, a tartály kérdése egyszerű.'],
                'Modellek és kapacitások', 'epureco-modellek-es-kapacitasok',
                alt=('Tisztítómező és területigény', 'oldomedence-tisztitomezo')),

        sec_faq([
            ('Mennyibe kerül egy EPURECO?',
             'Konkrét termékárat nem publikálunk. A projekt költségét a tartály mellett a '
             'tisztítómező mérete, a földmunka, a telepítés és a kivitelezési terjedelem '
             'is meghatározza — ezek nélkül egy közölt szám félrevezetne.'),
            ('A tartály önmagában megvásárolható?',
             'Fizikailag igen, de nem javasoljuk így gondolkodni: tisztítómező nélkül a '
             'tartály nem alkot működő rendszert, csak egy szigetelt tárolót. A '
             'méretezésnek a kettőre együtt kell vonatkoznia.'),
            ('Ki gyártja?',
             'Az EPURECO tartályokat a GRAF gyártja. Az ÖkoTech a magyarországi '
             'értékesítést, a rendszertervezést és a telepítést végzi — a tisztítómező '
             'méretezésével együtt.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# EPURECO 2) Modellek és kapacitások
# ===========================================================================
def epit_epu_modellek():
    return [
        sec_prose('Mire jó ez az oldal', 'Egységes adatstruktúra', [
            'Ez az oldal az ÖkoTechnél ténylegesen rendelhető EPURECO modellek '
            'kapacitását, névleges tartálytérfogatát és fizikai méreteit gyűjti egy '
            'táblázatba — hogy tervező és kivitelező is dolgozni tudjon vele.',
            'Egy dolgot fontos érteni hozzá: a <strong>tartály mérete az anaerob '
            'előkezeléshez</strong> kapcsolódik. A teljes rendszer kapacitását a '
            'megfelelően méretezett tisztítómezővel együtt kell értelmezni.',
        ]),

        sec_numbered('Milyen adatok kellenek modellenként', 'A táblázat oszlopai',
                     'Ez a lista egyben a hiányzó adatok listája is.',
                     ['Modellnév és magyar termékkód',
                      'Névleges használói kapacitás',
                      'Névleges tartálytérfogat, literben',
                      'Hosszúság, szélesség, magasság',
                      'Tömeg',
                      'Be- és kifolyási szintek',
                      'A beépített szűrő típusa',
                      'Az adat forrása és verziója']),

        hiany('a magyar értékesítéshez használt aktuális terméklap adatai. A GRAF '
              'nyilvános kínálatában EPURECO 4 (2100 l), 6 (2700 l) és 7 (3400 l) '
              'szerepel, 100, 110 és 120 kg körüli gyártói tömeggel — ezeket a magyar '
              'terméklappal kell egyeztetni, mielőtt termékadatként megjelennek. '
              'Ha az ÖkoTech ezeken kívül más konfigurációt is forgalmaz, azt belső '
              'termékadatból kell egyértelműsíteni',
              'ÖkoTech értékesítés + GRAF aktuális adatlapok. Régi vagy külföldi '
              'kereskedői katalógus alapján modellt hozzáadni NEM szabad'),

        sec_split('Két külön méretezés', 'Amit nem szabad összevonni',
                  'A tartály mérete',
                  ['A névleges használói kapacitáshoz igazodik',
                   'Az anaerob előkezelés és az ülepítés térfogata',
                   'Ez határozza meg a szippantás gyakoriságát is',
                   'Gyártói adat, katalógusból választható'],
                  'A tisztítómező mérete',
                  ['A talaj MÉRT szivárgóképességétől függ',
                   'A napi szennyvízmennyiségtől',
                   'A talajvíz helyzetétől',
                   'Telekspecifikus — nem katalógusadat',
                   'Ehhez mérés kell, nem választás']),

        sec_prose('Időszakos használatnál', 'Nem elég a „hány fős nyaraló”', [
            'Szezonálisan használt ingatlannál a tulajdonos által megadott „hány fős '
            'nyaraló” önmagában félrevezető lehet. Külön kell rögzíteni a '
            '<strong>jellemző</strong> és a <strong>maximális</strong> létszámot, '
            'valamint a használati ritmust.',
            'Egy négy férőhelyes nyaraló, amelyet nyáron folyamatosan nyolcan használnak '
            'hétvégenként, egészen más terhelés, mint amelyben négyen töltenek évi két '
            'hetet. A tartály és a mező méretezése is ettől függ.',
        ]),

        sec_cta('Következő lépés', 'A mező méretezéséhez adat kell',
                ['A tisztítómező méretezéséhez a talaj, a talajvíz, a szivárgási próba '
                 'eredménye, a napi terhelés és a rendelkezésre álló terület szükséges.'],
                'Tisztítómező és területigény', 'oldomedence-tisztitomezo',
                alt=('Műszaki adatok', 'epureco-muszaki-adatok')),

        sec_faq([
            ('Miért nincs itt kész táblázat?',
             'Mert a gyártói adatokat a magyar értékesítéshez használt aktuális '
             'terméklappal kell egyeztetni, és tisztázni kell, mely modellek '
             'rendelhetők ténylegesen. Inkább megmondjuk, mi hiányzik, mint hogy '
             'egyeztetetlen adatot tegyünk ki.'),
            ('A nagyobb tartály ritkább szippantást jelent?',
             'Jellemzően igen, mert lassabban telik. A pontos összefüggést viszont a '
             'gyártói ürítési kritérium adja meg — és ez az egyik olyan adat, amit '
             'jelenleg rendezünk.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# EPURECO 3) Műszaki adatok
# ===========================================================================
def epit_epu_muszaki():
    return [
        sec_prose('Egyetlen forráspont', '', [
            'Ez az oldal az EPURECO termékcsalád műszaki adatainak egyetlen, naprakész '
            'forráspontja a webhelyünkön. Minden adat mellett szerepelnie kell a '
            'modellnek és a forrásverziónak.',
            'Az adatok elsődleges forrása a gyártó, a GRAF. Ahol az ÖkoTech saját '
            'kiegészítést vagy konfigurációt alkalmaz, azt külön jelöljük.',
        ]),

        sec_numbered('Amit ennek az oldalnak tartalmaznia kell', 'A teljes specifikáció',
                     '',
                     ['Tartálytérfogat és fizikai méretek',
                      'Tömeg és termékkód',
                      'A tartály anyaga',
                      'Be- és kifolyási szintek',
                      'A beépített szűrő típusa és adatai',
                      'Fedlap és terhelhetőség',
                      'Megengedett földtakarás',
                      'Talajvízi telepítési korlátozás',
                      'Kompatibilis tisztítómező-elemek',
                      'CE-jelölés és az alkalmazott szabvány',
                      'Teljesítménynyilatkozat',
                      'Dokumentumverzió és dátum']),

        sec_prose('A szabványhivatkozásról', 'Amit rendezni kell', [
            'A jelenlegi tájékoztatásunk konkrét szabványverziókra és egy vizsgálati '
            'azonosítóra hivatkozik. A gyártó aktuális termékoldala CE-jelölést jelez az '
            '<strong>EN 12566-1</strong> szerinti megfelelőség alapján, és modellenként '
            'kínál teljesítménynyilatkozatot.',
            'A régi szabványszám nem lehet önálló marketingelem. A helyes lánc: '
            '<strong>modell → aktuális teljesítménynyilatkozat → alkalmazott szabvány → '
            'vizsgáló szervezet → a dokumentum dátuma</strong>.',
            'Ha az aktuális dokumentum más hivatkozásokat tartalmaz, mint a régi '
            'szövegünk, akkor a régi szöveget felül kell írni — nem fordítva.',
        ]),

        hiany('az aktuális magyar nyelvű adatlap, a modellenkénti teljesítménynyilatkozat, '
              'a telepítési útmutató, a szűrő adatlapja és a ténylegesen alkalmazott '
              'tisztítómező-elemek műszaki dokumentációja',
              'GRAF aktuális dokumentumok + ÖkoTech kiegészítések. KÜLÖN ELLENŐRZENDŐ: a '
              'jelenlegi „gépjárműbeálló alatt is használható" állítás — ez csak az adott '
              'elosztóelem és rétegrend igazolt terhelhetőségével együtt közölhető műszaki '
              'paraméterként'),

        sec_split('Két külön adatlap', 'Miért nem egy',
                  'A tartály adatlapja',
                  ['Gyártói adat, katalógusból',
                   'Méret, térfogat, tömeg, csatlakozások',
                   'Modellenként azonos minden telepítésnél',
                   'CE és teljesítménynyilatkozat tartozik hozzá'],
                  'A tisztítómező adatai',
                  ['Telekspecifikus — nem katalógusadat',
                   'A mért szivárgás és a terhelés függvénye',
                   'Az alkalmazott elosztóelem típusától is függ',
                   'Minden projektnél újra kell méretezni']),

        sec_cta('Következő lépés', 'A telepítés feltételei',
                ['A műszaki adatok után a kivitelezés kérdései jönnek: földmunka, '
                 'ágyazat, talajvíz, szellőzés és a mező elhelyezése.'],
                'Telepítési feltételek', 'epureco-telepitesi-feltetelek',
                alt=('Dokumentumok', 'epureco-dokumentumok')),

        sec_faq([
            ('Ráállhat autó a tartályra?',
             'A jelenlegi tájékoztatásunk említ ilyen lehetőséget megfelelő '
             'földtakarással, de ezt az adott elosztóelem és rétegrend igazolt '
             'terhelhetőségével együtt kell megadni. Amíg ez nincs dokumentálva, nem '
             'ígérjük meg — a konkrét projektnél egyeztetve mondjuk meg.'),
            ('Megkaphatom a teljesítménynyilatkozatot?',
             'Igen. Írja meg, melyik modell érdekli, és megküldjük a gyártó aktuális '
             'dokumentumát. Tervezéshez és engedélyezési eljáráshoz ez gyakran '
             'szükséges is.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# EPURECO 4) Telepítési feltételek
# ===========================================================================
def epit_epu_telepites():
    return [
        sec_prose('A teljes rendszer telepítése', 'Nem csak a gödörméret', [
            'A projekt sikerét nem a tartály gödre dönti el, hanem az, hogy a '
            '<strong>tisztítómező</strong> is a helyére kerül-e a megfelelő méretben. '
            'Ezért ez az oldal a teljes rendszer telepítési feltételeit tárgyalja.',
            'A jogszabály szerint a tisztítómezővel ellátott oldómedencés rendszert a '
            'talajadottságok, a felszín alatti víz mélysége és a szennyvízmennyiség '
            'figyelembevételével kell méretezni. Magas talajvízi vagy fokozottan '
            'érzékeny területen további feltételek lehetnek.',
        ]),

        sec_numbered('A tartály telepítése', 'Amit a gyártói előírás határoz meg', '',
                     ['<strong>Földmunka és gödörméret.</strong> A tartály méretéhez és a '
                      'talajviszonyokhoz igazodva.',
                      '<strong>Ágyazat.</strong> A tartály alá kerülő réteg anyaga és '
                      'vastagsága — ez a szerkezeti stabilitás alapja.',
                      '<strong>Visszatöltés.</strong> Az anyaga és a tömörítés módja '
                      'gyártói előírás szerint.',
                      '<strong>Fedés és földtakarás.</strong> Mennyi föld kerülhet a '
                      'tartályra, és mi a felette megengedett használat.',
                      '<strong>Be- és kifolyó csőmagasságok.</strong> Ezek határozzák meg, '
                      'kell-e magasító elem.',
                      '<strong>Talajvízi rögzítés.</strong> Magas talajvíznél a felúszás '
                      'elleni megoldás.',
                      '<strong>Szellőzés.</strong> A rendszer megfelelő működéséhez '
                      'szükséges.']),

        sec_numbered('A tisztítómező telepítése', 'Amit a telek határoz meg',
                     'Ezeket a tartálytól függetlenül, a telek adottságai alapján kell '
                     'meghatározni.',
                     ['A talaj mért szivárgóképessége — szivárogtatási vizsgálatból',
                      'A szezonálisan legmagasabb talajvízszint',
                      'A rendelkezésre álló, ténylegesen szabad terület',
                      'A tereplejtés és a gravitációs vízvezetés lehetősége',
                      'A kút vagy kutak helye, a szomszédos telkeken lévőkkel együtt',
                      'A mező fölötti terület tervezett, későbbi használata',
                      'Az alkalmazott elosztóelem típusa és a hozzá tartozó rétegrend']),

        hiany('az ÖkoTech magyarországi telepítési gyakorlata: az alkalmazott rétegrend, '
              'a magas talajvízi megoldás, az ajánlott tisztítómező-rendszer, a '
              'munkagép- és hozzáférési feltételek, valamint az, hogy a gyártó '
              'perforált drénnel és szikkasztókamrával is mutat konfigurációt — '
              'egyértelműsíteni kell, melyiket értékesíti és méretezi az ÖkoTech',
              'ÖkoTech kivitelezési csapat + GRAF telepítési útmutató'),

        sec_split('Ki végzi', 'Felelősségi megosztás',
                  'Lehet a megrendelő vagy saját kivitelezője',
                  ['Földmunka, gödör kiemelése',
                   'Ágyazat és visszatöltés a gyártói előírás szerint',
                   'Csővezeték fektetése a háztól',
                   'A tisztítómező kivitelezése',
                   'Szállítás'],
                  'ÖkoTech-szolgáltatásként kérhető',
                  ['Szállítás a helyszínre',
                   'A rendszer méretezése — tartály és mező együtt',
                   'Telepítés és beüzemelés',
                   'Átadás és a tulajdonos betanítása',
                   'Ezek külön szolgáltatási elemek']),

        sec_prose('Mikor elég a dokumentum, és mikor kell felmérés', '', [
            'Ha a telek adatai — talajtípus, korábbi talajvizsgálat, a talajvíz ismert '
            'szintje, a szabad terület mérete — dokumentumból rendelkezésre állnak, sok '
            'esetben elegendő ezek megadása.',
            'Ha viszont a talaj szivárgóképessége nincs mérve, a talajvíz csak becslés, '
            'vagy a szabad terület szűkös, akkor szivárogtatási vizsgálat, illetve '
            'helyszíni felmérés szükséges. Ezt a projekt elején érdemes eldönteni — '
            'nem a kivitelezés hetében.',
        ]),

        sec_cta('Következő lépés', 'A telekadatokkal kezdje',
                ['A tisztítómező méretezéséhez a talaj és a talajvíz adatai kellenek. '
                 'A telekalkalmassági szakasz végigvezeti, mit kell megszereznie.'],
                'Telekalkalmasság', '../projekt-elokeszites/telekalkalmassag',
                alt=('Dokumentumok', 'epureco-dokumentumok')),

        sec_faq([
            ('Saját kivitelezővel is telepíthető?',
             'A földmunka, az ágyazat, a visszatöltés és a csövezés végezhető saját '
             'kivitelezővel, a gyártói előírások betartásával. A rendszer méretezését — '
             'különösen a tisztítómezőt — viszont érdemes ránk bízni, mert ott a '
             'hibának hosszú távú következménye van.'),
            ('Kell hozzá engedély?',
             'Ez projekt- és helyszínfüggő, és az eljárási szabályok időről időre '
             'változnak. A projekt-előkészítés szakasz foglalkozik ezzel, aktuális '
             'forrásokkal.'),
            ('Mennyi idő a telepítés?',
             'A tartály elhelyezése önmagában rövid folyamat. A teljes kivitelezés — a '
             'tisztítómezővel együtt — jellemzően több nap, és erősen függ a mező '
             'méretétől és a talajviszonyoktól.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# EPURECO 5) Dokumentumok
# ===========================================================================
def epit_epu_dokumentumok():
    return [
        sec_prose('Mi lesz ez az oldal', 'Egyetlen verziózott dokumentumközpont', [
            'A cél az, hogy az ÖkoTech által forgalmazott EPURECO modellek gyártói és '
            'projekt-előkészítéshez szükséges dokumentumai egy helyen, naprakészen '
            'legyenek elérhetők.',
            'A gyártó modellenként kínál adatlapot és teljesítménynyilatkozatot, valamint '
            'közös telepítési és üzemeltetési dokumentációt a termékcsaládhoz. Ezeket '
            'kell magyar nyelven, verziózva összegyűjteni.',
        ]),

        sec_numbered('A dokumentumtár tartalma', 'Mi tartozik ide',
                     'Minden fájl mellett: modell, dokumentumtípus, gyártó, verzió vagy '
                     'kiadási dátum, és „aktuális / archív” státusz.',
                     ['Modellenkénti termékadatlap',
                      'Modellenkénti teljesítménynyilatkozat',
                      'CE-jelöléshez tartozó szabványhivatkozás',
                      'Telepítési utasítás',
                      'Üzemeltetési utasítás',
                      'A beépített szűrő dokumentációja',
                      'A ténylegesen alkalmazott tisztítómező-elemek adatlapjai',
                      'ÖkoTech magyar telepítési checklist',
                      'Garanciafeltételek']),

        sec_prose('Amit külön kell kezelni', 'A jogszabályi tartalom', [
            'A jogi és engedélyezési információ <strong>nem való statikus PDF-be</strong>. '
            'Erre jó példa a webhelyünkön jelenleg is megtalálható, 2012-ben frissített '
            'jogszabály-összefoglaló: több mint egy évtizede áll ott, miközben a '
            'hivatkozott szabályozás azóta többször módosult.',
            'Ezért a jogi tartalom külön, rendszeresen frissített rendszerben kezelendő, '
            'nem a termékdokumentumok között. A régi összefoglalót archiválni kell — nem '
            'törölni, de egyértelműen dátumozva és „archív” megjelöléssel.',
        ]),

        hiany('a dokumentumaudit. Tisztázandó: mely GRAF modelleket értékesíti jelenleg '
              'az ÖkoTech, melyek az aktuális magyar nyelvű gyártói dokumentumok, mely '
              'teljesítménynyilatkozatok érvényesek, mik a garanciafeltételek, milyen '
              'tisztítómező-elemek adatlapjai tartoznak ide, és mely régi EPURECO '
              'dokumentumok archiválandók',
              'ÖkoTech műszaki felelős + GRAF. KÜLÖN ELLENŐRZENDŐ: a jelenlegi '
              'szövegünkben szereplő szabványverziók és vizsgálati azonosító csak akkor '
              'maradhatnak, ha az aktuális teljesítménynyilatkozat is ezeket tartalmazza'),

        sec_cta('Addig is', 'Kérje el, amire szüksége van',
                ['Amíg a dokumentumtár nem áll össze, a szükséges iratokat közvetlenül '
                 'megküldjük. Írja meg, melyik modellről és milyen dokumentumról van szó, '
                 'és milyen célra kell.'],
                'Kapcsolatfelvétel', '../kapcsolat',
                alt=('Műszaki adatok', 'epureco-muszaki-adatok')),

        sec_faq([
            ('Magyar nyelven is elérhetők a dokumentumok?',
             'A gyártói dokumentumok egy része magyar nyelven is rendelkezésre áll. '
             'Ennek pontos körét jelenleg tisztázzuk — kérdezze meg a konkrét modellnél, '
             'és megküldjük, ami elérhető.'),
            ('A régi berendezésemhez hol találok dokumentációt?',
             'Adja meg a típust és a telepítés hozzávetőleges évét — az akkori '
             'dokumentációt keressük ki. Egy régebbi EPURECO-hoz nem feltétlenül a mai '
             'adatlap tartozik.'),
        ]),
        JOGI,
    ]


# ===========================================================================
OLDALAK = [
    dict(file='megoldasok/oldomedences-rendszer.html',
         url='megoldasok/oldomedences-rendszer', img='oldomedence',
         title='Oldómedencés rendszer — árammentes helyi szennyvízkezelés | ÖkoTech Home',
         desc='Oldómedence és tisztítómező együtt alkot rendszert. Kinek való, mit igényel, '
              'és miért a tisztítómező a fő döntési korlát.',
         h1='Oldómedencés rendszer',
         alt='Rétegzett talajmetszet oldómedencével és a mögötte húzódó, elosztócsövekkel '
             'ellátott tisztítómezővel',
         lead='Nem egyszerűen egy földbe helyezett tartály: oldómedencéből és '
              'tisztítómezőből álló rendszer, amely villamos energia nélkül működik. '
              'A tisztítás jelentős része a talajban történik.',
         crumbs=CRUMB, sections=epit_hub()),

    dict(file='megoldasok/oldomedence-hogyan-mukodik.html',
         url='megoldasok/oldomedence-hogyan-mukodik', img='biologiai',
         title='Hogyan működik az oldómedencés rendszer? | ÖkoTech Home',
         desc='A szennyvíz útja a tartálytól a tisztítómezőn át a talajba. Két kezelési '
              'lépcső, és miért nem elég a tartály önmagában.',
         h1='Hogyan működik?',
         alt='Talajmetszet: oldómedence, szűrő és az elosztócsövekkel ellátott '
             'tisztítómező',
         lead='A folyamat kétlépcsős. A tartályban anaerob előkezelés történik, a '
              'tisztítás érdemi része viszont a talajban, a tisztítómezőben.',
         crumbs=HUB, sections=epit_mukodes()),

    dict(file='megoldasok/oldomedence-kinek-megfelelo.html',
         url='megoldasok/oldomedence-kinek-megfelelo', img='nyaralo',
         title='Kinek megfelelő az oldómedencés rendszer? | ÖkoTech Home',
         desc='Nyaraló, hétvégi ház, vadászház — és az a négy feltétel, amit az '
              'ingatlantípuson túl ellenőrizni kell.',
         h1='Kinek megfelelő?',
         alt='Fák között álló nyaraló nyáron, előtte gondozott gyepfelület',
         lead='Az árammentes működés hosszú kihagyásoknál valódi előny. De az '
              'alkalmasságot nem az ingatlantípus dönti el — négy feltétel van, és '
              'mind a négynek teljesülnie kell.',
         crumbs=HUB, sections=epit_kinek()),

    dict(file='megoldasok/oldomedence-mikor-nem-megfelelo.html',
         url='megoldasok/oldomedence-mikor-nem-megfelelo', img='alternativak',
         title='Mikor nem megfelelő az oldómedencés rendszer? | ÖkoTech Home',
         desc='Kizárás és feltételes alkalmasság. A leggyakoribb korlát nem a tartály, '
              'hanem a tisztítómező helyigénye.',
         h1='Mikor nem megfelelő?',
         alt='Szűk, beépített telek kis szabad zöldfelülettel',
         lead='Az árammentesség és az egyszerűség önmagában nem teszi minden '
              'ingatlanhoz megfelelővé. És van, ami nem műszaki kizárás, hanem '
              'vállalhatósági kérdés.',
         crumbs=HUB, sections=epit_mikor_nem()),

    dict(file='megoldasok/oldomedence-tisztitomezo.html',
         url='megoldasok/oldomedence-tisztitomezo', img='telekvasarlas',
         title='Tisztítómező és területigény — a fő döntési korlát | ÖkoTech Home',
         desc='A mező a technológia része, nem kiegészítő. Mitől függ a mérete, mit '
              'lehet fölötte, és miért nincs fix négyzetméter/fő szabály.',
         h1='Tisztítómező és területigény',
         alt='Frissen kiásott árokrendszer egy kertben, előkészítve az elosztócsövek '
             'fektetéséhez',
         lead='Nem az a kérdés, hogy elfér-e a tartály — hanem hogy elfér-e a mező. '
              'A lebontás nagy része ott zajlik, ezért a mérete meghatározó.',
         crumbs=HUB, sections=epit_tisztitomezo()),

    dict(file='megoldasok/oldomedence-szippantas-es-karbantartas.html',
         url='megoldasok/oldomedence-szippantas-es-karbantartas', img='mar-van-rendszerem',
         title='Szippantás és karbantartás — oldómedencés rendszer | ÖkoTech Home',
         desc='Árammentes nem jelent karbantartásmentest. Szippantás, baktériumadalék, '
              'szűrő és a tisztítómező ellenőrzése.',
         h1='Szippantás és karbantartás',
         alt='Aknafedlap egy kertben, mellette szerszámok és mérőrúd',
         lead='Az, hogy nem kell hozzá áram, nem jelenti, hogy nem kell hozzá figyelem. '
              'Egyik feladat sem nagy — de mindegyik rendszeres.',
         crumbs=HUB, sections=epit_karbantartas()),

    dict(file='megoldasok/oldomedence-esettanulmanyok.html',
         url='megoldasok/oldomedence-esettanulmanyok', img='obudavar',
         title='Kapcsolódó esettanulmányok — oldómedencés rendszer | ÖkoTech Home',
         desc='Használati profil szerint rendezve: hétvégi ház, nyári nyaraló, vadászház. '
              'Szippantási előzmény, adalékhasználat, a mező állapota.',
         h1='Kapcsolódó esettanulmányok',
         alt='Hétvégi házak sora egy domboldalon, gondozott kertekkel',
         lead='Az általános állításokat — szezonális használat, ritka szippantás, '
              'minimális karbantartás — éppen valós projektadatoknak kell igazolniuk.',
         crumbs=HUB, sections=epit_esettanulmanyok()),

    # --- EPURECO alhub -----------------------------------------------------
    dict(file='megoldasok/epureco.html',
         url='megoldasok/epureco', img='oldomedence',
         title='EPURECO termékcsalád — oldómedencés rendszer | ÖkoTech Home',
         desc='GRAF gyártmányú EPURECO tartályok és a hozzájuk méretezett tisztítómező. '
              'Modellek, műszaki adatok, telepítés és dokumentumok.',
         h1='EPURECO termékcsalád',
         alt='EPURECO tartály a telepítés előtt egy telken, mellette a fedlap',
         lead='A tartályt a GRAF gyártja, és a házi szennyvízkezelés anaerob első '
              'szakasza. A rendszert a hozzá méretezett tisztítómezővel együtt alkotja.',
         crumbs=HUB, sections=epit_epu_hub()),

    dict(file='megoldasok/epureco-modellek-es-kapacitasok.html',
         url='megoldasok/epureco-modellek-es-kapacitasok', img='csaladi-haz',
         title='EPURECO modellek és kapacitások | ÖkoTech Home',
         desc='Névleges kapacitás, tartálytérfogat, méretek — és miért kell külön '
              'méretezni a tartályt és a tisztítómezőt.',
         h1='Modellek és kapacitások',
         alt='Műszaki adatlapok és mérőszalag egy asztalon, háttérben tartály',
         lead='A tartály mérete az anaerob előkezeléshez kapcsolódik. A teljes rendszer '
              'kapacitását a megfelelően méretezett tisztítómezővel együtt kell '
              'értelmezni.',
         crumbs=EPU, sections=epit_epu_modellek()),

    dict(file='megoldasok/epureco-muszaki-adatok.html',
         url='megoldasok/epureco-muszaki-adatok', img='kozcsatorna',
         title='EPURECO műszaki adatok | ÖkoTech Home',
         desc='Tartályadatok, szűrő, csatlakozási szintek, földtakarás, CE és '
              'EN 12566-1 — modellenként, forrásverzióval.',
         h1='Műszaki adatok',
         alt='Gyártói műszaki rajz és adatlap egy asztalon, mellette mérőeszközök',
         lead='Egyetlen naprakész forráspont, minden adat mellett a modellel és a '
              'forrásverzióval. Az elsődleges forrás a gyártó.',
         crumbs=EPU, sections=epit_epu_muszaki()),

    dict(file='megoldasok/epureco-telepitesi-feltetelek.html',
         url='megoldasok/epureco-telepitesi-feltetelek', img='kapcsolat',
         title='EPURECO telepítési feltételek | ÖkoTech Home',
         desc='A tartály és a tisztítómező együtt: földmunka, ágyazat, talajvíz, '
              'szellőzés, hozzáférés — és melyik munkát ki végzi.',
         h1='Telepítési feltételek',
         alt='Munkagödör oldómedencéhez, mellett kitermelt föld és az előkészített ágyazat',
         lead='A projekt sikerét nem a tartály gödre dönti el, hanem az, hogy a '
              'tisztítómező is a helyére kerül-e a megfelelő méretben.',
         crumbs=EPU, sections=epit_epu_telepites()),

    dict(file='megoldasok/epureco-dokumentumok.html',
         url='megoldasok/epureco-dokumentumok', img='helyzetem',
         title='EPURECO dokumentumok | ÖkoTech Home',
         desc='Adatlap, teljesítménynyilatkozat, telepítési és üzemeltetési utasítás — '
              'modellenként, verzióval és érvényességi státusszal.',
         h1='Dokumentumok',
         alt='Iratrendezőben sorakozó gyártói adatlapok és megfelelőségi dokumentumok',
         lead='A gyártó modellenként kínál adatlapot és teljesítménynyilatkozatot. '
              'Ezeket kell magyar nyelven, verziózva összegyűjteni.',
         crumbs=EPU, sections=epit_epu_dokumentumok()),
]

if __name__ == '__main__':
    for o in OLDALAK:
        out = WEB / o['file']
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:56s} {len(out.read_text(encoding='utf-8'))//1024} KB")
