#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helyzetem → Vállalkozás vagy intézmény számára keresek megoldást — hub és hat
aloldal, plusz a szakmai projektbrief funkcionális oldal.

Ez a hub NEM technológiai oldal, hanem BELÉPÉSI PONT: a látogató a saját
létesítménytípusából indul ki, és a hub kategorizálja a projektjét. A műszaki
mélység a `megoldasok/nagyobb-*` ágon van — ide csak annyi kerül, amennyi a
helyes irányba tereléshez kell. A kettő KERESZTHIVATKOZIK, nem duplikál.

A brief KÉT ponton kifejezetten felülír:

1. A kapacitáshatárok rendezetlenek: a lakossági ág 1–50 főig kommunikál, az
   50 fő feletti érdeklődőt a nagytelepi oldalra küldi, az viszont 100 LE
   feletti, kb. 75–750 fős rendszereket ír le. A 147/2010. szerinti egyedi
   kategória felső határa 50 LE. A férőhely és az alkalmazotti létszám üzleti
   és intézményi terhelésnél KÜLÖNÖSEN félrevezető.

2. Az ipari állításokhoz (vágóhíd, tejüzem, borászat) bizonyíték kell:
   projekt, iparág, bemeneti szennyvízjellemző, előkezelés, technológia,
   kibocsátási követelmény, laboreredmény, működési időtáv. Enélkül a helyes
   megfogalmazás: „speciális terhelések egyedi mérnöki vizsgálat alapján".

ÁR NEM JELENIK MEG; ársáv is csak tisztázott projektparaméterek után.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import (sec_numbered, sec_split, sec_prose, sec_situations,
                    sec_cta, sec_faq)

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

JOGI = ('<!-- JOGI ELLENŐRZÉS PUBLIKÁLÁS ELŐTT ÉS PROJEKTENKÉNT. Érintett: 147/2010.\n'
        '     Korm. rendelet (1–50 LE egyedi kategória, üzemeltetési és mintavételi\n'
        '     követelmények) · 220/2004. Korm. rendelet (termelési és szolgáltatási\n'
        '     tevékenységből származó szennyvíz, kibocsátás, engedélyezési dokumentáció)\n'
        '     · 28/2004. KvVM rendelet (technológiai és területi kibocsátási\n'
        '     határértékek, előtisztítás). Iparág-specifikus követelmények projektenként. -->')


def hiany(mi, honnan):
    return (f'<!-- ADATHIÁNY: {mi}\n'
            f'     Forrás: {honnan}. Addig konkrét értékkel nem publikálható. -->')


HOME = ('Főoldal', '../')
HELY = ('Helyzetem', './')
CRUMB = [HOME, HELY]
HUB = [HOME, HELY,
       ('Vállalkozás vagy intézmény', 'vallalkozas-vagy-intezmeny-szamara-keresek-megoldast')]


# ===========================================================================
# HUB
# ===========================================================================
def epit_hub():
    return [
        sec_prose('A kiinduló kérdés', 'A „hány fő?” itt különösen félrevezető', [
            'Vállalkozási vagy intézményi szennyvízkezelésnél a „hányan használják?” '
            'önmagában nem elegendő méretezési információ. A napi vízmennyiség, a '
            'csúcsterhelés, a kihasználtság időbeli változása és maga a szennyvíz '
            '<strong>eredete</strong> legalább ilyen fontos.',
            'Egy húszférőhelyes panzió, egy háromszáz fős iskola és egy ötven '
            'alkalmazottat foglalkoztató üzem mind mondhatja ugyanazt a számot — és '
            'három teljesen különböző projekt lesz belőle.',
            'Ezért ez az oldal nem terméket ajánl első lépésként. A célja az, hogy '
            'a projektet <strong>kategorizálja</strong>: standard kommunális jellegű '
            'terhelésként kezelhető-e, vagy egyedi mérnöki, előkezelési, labor-, '
            'engedélyezési és üzemeltetési tervezést igényel.',
        ]),

        sec_split('Az első szétválasztás', 'Milyen eredetű a szennyvíz?',
                  'Kommunális jellegű',
                  ['Fürdőszoba, WC, kézmosó, tisztálkodás',
                   'Összetétele a háztartásihoz hasonló',
                   'A terhelés a használói létszámmal arányos',
                   'A szokásos biológiai tisztítás alkalmazható',
                   'Laborvizsgálat jellemzően nem előfeltétel',
                   'Szálláshely, iroda, iskola nagy része ide tartozik'],
                  'Technológiai vagy nagykonyhai',
                  ['Termelési folyamatból vagy főzőkonyhából ered',
                   'Összetétele a tevékenységtől függ',
                   'Nem vezethető le személyszámból',
                   'Előkezelést igényelhet',
                   'Laborvizsgálat jellemzően elkerülhetetlen',
                   'Iparág-specifikus kibocsátási követelmények élhetnek']),

        sec_situations('Melyik létesítmény?', 'Válassza ki a legközelebbit',
                       'A terhelési logika létesítménytípusonként eltér — ezért '
                       'kezeljük őket külön, nem egyetlen „B2B” kategóriaként.',
                       [
                           ('nav-vallalkozas', 'Panziók és szálláshelyek',
                            'A férőhely nem terhelés. Kihasználtság, csúcshétvégék, '
                            'szezon, mosoda, wellness — és a szezonon kívüli üzem.',
                            'vallalkozas-panziok-es-szallashelyek', 'Panzió, szálláshely'),
                           ('nav-vizminoseg', 'Éttermek és nagykonyhák',
                            'A konyhai szennyvíz nem kezelhető ugyanúgy, mint egy '
                            'azonos létszámú lakóingatlané. Előkezelés és laboradat.',
                            'vallalkozas-ettermek-es-nagykonyhak', 'Étterem, konyha'),
                           ('nav-kozossegi', 'Iskolák és intézmények',
                            'Erős napi ritmus, hétvégi visszaesés, hosszú szünetek — '
                            'és szervezeti kérdés, ki lesz a felelős üzemeltető.',
                            'vallalkozas-iskolak-es-intezmenyek', 'Iskola, intézmény'),
                           ('nyaralo', 'Kempingek és közösségi létesítmények',
                            'Szélsőségesen változó terhelés, több felhasználói pont és '
                            'közös üzemeltetési felelősség.',
                            'vallalkozas-kempingek-es-kozossegi', 'Kemping, közösségi'),
                           ('nav-adatbazis', 'Üzemek és speciális terhelések',
                            'Az „üzem” nem méretezési kategória. Kommunális és '
                            'technológiai vízáram szétválasztása, laboradat.',
                            'vallalkozas-uzemek-es-specialis-terhelesek', 'Üzem, ipari'),
                           ('nav-iranytu', 'Szakmai projektbrief',
                            'Strukturált adatcsomag, amiből eldönthető, standard '
                            'konfiguráció vagy mérnöki tervezés következik.',
                            'vallalkozas-szakmai-projektbrief', 'Projektbrief'),
                       ]),

        sec_numbered('Amit minden projektnél tisztázni kell', 'Hét kérdés, sorrendben',
                     'Ezek a válaszok együtt adják meg, hogy standard vagy egyedi '
                     'projektről van szó.',
                     ['<strong>Mi a létesítmény, és mi a szennyvíz eredete?</strong> '
                      'Ez a legfontosabb egyetlen kérdés — ebből következik minden '
                      'további.',
                      '<strong>Mennyi a tényleges terhelés?</strong> Átlagos napi '
                      'vízmennyiség, csúcs, szezonalitás. Meglévő létesítménynél a '
                      'vízszámla a legjobb kiindulás.',
                      '<strong>Van-e speciális vízhasználat?</strong> Konyha, mosoda, '
                      'wellness, technológiai mosás — mindegyik külön vízáram.',
                      '<strong>Melyik kapacitási kategóriába esik?</strong> A jogi '
                      'határ 50 LE — e fölött más tervezési és engedélyezési út '
                      'következik.',
                      '<strong>Hová kerül a tisztított víz?</strong> Talajba, felszíni '
                      'befogadóba, vagy hasznosításra — mindhárom külön ág.',
                      '<strong>Ki lesz a felelős üzemeltető?</strong> Ez üzleti '
                      'projektben szervezeti kérdés, nem csak műszaki.',
                      '<strong>Milyen bővítés várható?</strong> Ha a létesítmény nő, '
                      'azt most kell figyelembe venni.']),

        hiany('a kapacitási határaink. A lakossági ág 1–50 főig kommunikál és 50 fő '
              'felett a nagytelepi oldalra irányít; az viszont 100 LE feletti, kb. '
              '75–750 fős rendszereket ír le. Az 50–100 LE közötti tényleges ajánlati '
              'logika nincs rögzítve',
              'ÖkoTech műszaki és értékesítési workshop. Ugyanez a hiány szerepel a '
              'megoldasok/nagyobb-kapacitasi-kategoriak oldalon is — egy helyen kell '
              'rendezni, és mindkét helyen átvezetni'),

        sec_prose('Amit ez a hub nem tesz', '', [
            'Nem ad árat, és nem ígér engedélyezhetőséget. Üzleti és intézményi '
            'projektnél a kapacitás vagy a férőhely alapján közölt ár különösen '
            'félrevezető lenne — a teljes projekt- és életciklusköltséget a '
            'rendszerarchitektúra, az előkezelés, a telepítés, a monitoring és az '
            'üzemeltetés együtt határozza meg.',
            'És nem helyettesíti a mérnöki döntést. Ahol a szennyvíz nem kommunális '
            'jellegű, ott laboradat és megvalósíthatósági vizsgálat előzi meg az '
            'ajánlatot — nem fordítva.',
        ]),

        sec_cta('Következő lépés', 'Válasszon létesítménytípust',
                ['A fenti hat oldal mindegyike a saját logikája szerint kérdez. Ha nem '
                 'találja a sajátját, kezdje a projektbriefnél — az minden '
                 'létesítménytípust kezel.'],
                'Szakmai projektbrief', 'vallalkozas-szakmai-projektbrief',
                alt=('Nagyobb és közösségi rendszerek',
                     '../megoldasok/nagyobb-es-kozossegi-rendszerek')),

        sec_faq([
            ('Elég, ha megmondom, hányan dolgozunk?',
             'Belépő adatnak jó, de nem elegendő. Üzleti és intézményi terhelésnél a '
             'létszám különösen félrevezető: az számít, mennyi vizet használnak, mikor, '
             'és hogy a szennyvíz kommunális jellegű-e. Meglévő létesítménynél a '
             'vízszámla a legjobb kiindulás.'),
            ('Vágóhídi vagy tejüzemi szennyvizet kezelnek?',
             'Speciális terheléseket egyedi mérnöki vizsgálat alapján kezelünk. Ez nem '
             'automatikus alkalmasság: mintavétel, laboradat és megvalósíthatósági '
             'vizsgálat előzi meg. Egy standard telep nem alkalmas automatikusan '
             'bármilyen ipari szennyvízre — ezt előre megmondjuk.'),
            ('Mennyi idő, míg ajánlatot kapok?',
             'Attól függ, milyen adatok állnak rendelkezésre. Tisztán kommunális '
             'terhelésnél, ismert vízfogyasztással gyorsan. Technológiai szennyvíznél '
             'laborvizsgálat és megvalósíthatósági vizsgálat előzi meg — ott az első '
             'lépés a mintavétel, nem az ajánlat.'),
            ('Kell hozzá engedély?',
             'Üzleti és intézményi projektnél jellemzően igen, és az eljárás a '
             'kapacitástól, a szennyvíz eredetétől és a befogadótól függ. Az '
             'engedélyezési kérdéseket a Megoldások szakasz nagyobb rendszerekről szóló '
             'oldala tárgyalja részletesen.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 1) Panziók és szálláshelyek
# ===========================================================================
def epit_panzio():
    return [
        sec_prose('A férőhely nem terhelés', '', [
            'Egy húszférőhelyes panzió nem azonos terhelési helyzet akkor, ha '
            'folyamatosan 70–80%-os kihasználtsággal működik, és akkor, ha csak nyári '
            'hétvégéken telik meg.',
            'A terhelés meghatározásához a férőhely mellett szükséges a valós vagy '
            'tervezett <strong>kihasználtság</strong>, az éves nyitvatartás, a '
            'csúcsszezon hossza, a rövid idejű teljes telítettség, és lehetőség szerint '
            'a <strong>tényleges vízfogyasztási adat</strong>.',
        ]),

        sec_numbered('Amit meg kell adni', 'A szálláshelyi terhelési profil', '',
                     ['<strong>Férőhely és átlagos éves kihasználtság.</strong> A kettő '
                      'együtt adja a reális átlagot.',
                      '<strong>Csúcskihasználtság.</strong> Mikor telt ház, mennyi ideig, '
                      'és évente hányszor.',
                      '<strong>Nyitvatartási hónapok.</strong> Egész évben vagy '
                      'szezonálisan üzemel. Ez a technológiaválasztást is befolyásolja.',
                      '<strong>Hétvégi és hétköznapi különbség.</strong> Városi és '
                      'üdülőhelyi szálláshelynél ez ellentétes lehet.',
                      '<strong>Személyzet létszáma.</strong> Ők a nyitvatartás teljes '
                      'idejében terhelést jelentenek.',
                      '<strong>Étkeztetés.</strong> Csak reggeli vagy teljes étterem. '
                      'Ha van konyha, az külön ág — lásd az éttermek oldalt.',
                      '<strong>Mosoda.</strong> Helyben mosnak, vagy külső szolgáltató. '
                      'A saját mosoda jelentős, koncentrált vízhasználat.',
                      '<strong>Wellness.</strong> Medence, jacuzzi, szauna — a '
                      'medencevíz-csere külön, nagy egyszeri vízmennyiség.',
                      '<strong>Tényleges vízfogyasztás.</strong> Meglévő szálláshelynél '
                      'ez mindent felülír — a vízszámla a legjobb adat.']),

        sec_split('Két szélsőség', 'Ugyanaz a férőhely, más rendszer',
                  'Egész évben, egyenletesen',
                  ['Kiszámítható átlagterhelés',
                   'A biológia folyamatos terhelést kap',
                   'Kisebb szórás, kisebb tartalék kell',
                   'Aktív biológiai rendszer jellemzően jó választás',
                   'A csúcs kezelhető rövid túlterhelésként'],
                  'Csak szezonban, csúcsokkal',
                  ['Hosszú alacsony vagy nulla terhelés',
                   'Hirtelen visszatérő teljes telítettség',
                   'A szezonnyitás külön üzemeltetési feladat',
                   'A technológiaválasztás is kérdés, nem csak a méret',
                   'Nagyobb tartalék és más üzemmód kell']),

        sec_prose('Szezonon kívül', 'Ami a leggyakrabban kimarad a tervezésből', [
            'Erősen szezonális szálláshelynél külön kell vizsgálni, hogyan működik a '
            'rendszer az alulterhelt vagy kihagyásos időszakban, és milyen üzemeltetői '
            'beavatkozás szükséges a szezon elején és végén.',
            'Ez nem műszaki apróság: az aktív biológiai rendszer baktériumközössége '
            'folyamatos tápanyagot igényel, és a hosszú szünet után az újraindulás időt '
            'vesz igénybe. A szezonnyitáskor érkező első teljes ház nem ideális pillanat '
            'arra, hogy a biológia még épp épül.',
            'Ezért kérdezzük meg a szezonon kívüli állapotot is — nem udvariasságból.',
        ]),

        hiany('a szálláshelyi referenciaadatok: panzió, hotel és apartman projektek '
              'férőhely és valós vízfogyasztás összevetésével, éves kihasználtsági '
              'profilok, csúcsterhelési tapasztalat, szezonális leállás és újraindítás, '
              'vendéglátással rendelkező és anélküli projektek külön, szerviz- és '
              'karbantartási adatok, többéves kifolyóvíz-mérési eredmények',
              'ÖkoTech projektarchívum. A döntéshez hasonló férőhelyű ÉS hasonló '
              'használati profilú működő szálláshely kell — nem telepítési fotó'),

        sec_cta('Következő lépés', 'Ha étterem is van',
                ['Saját étterem vagy főzőkonyha esetén a konyhai szennyvíz külön ág: '
                 'eltérő terheléssel és jellemzően előkezelési igénnyel.'],
                'Éttermek és nagykonyhák', 'vallalkozas-ettermek-es-nagykonyhak',
                alt=('Szakmai projektbrief', 'vallalkozas-szakmai-projektbrief')),

        sec_faq([
            ('Húsz férőhelyes a panzióm. Húsz fős rendszer kell?',
             'Valószínűleg nem. A férőhely a maximumot mutatja, a méretezés viszont az '
             'átlagos kihasználtságból és a rendszeres csúcsokból indul. Adja meg az '
             'éves kihasználtságot és a csúcshétvégék számát — abból lényegesen '
             'pontosabb kép áll össze.'),
            ('Rendezvényeket is tartunk.',
             'A rendezvény rövid, nagyon nagy csúcs, amit jellemzően nem érdemes a '
             'berendezés méretével kezelni — az az év többi napján túlméretezést '
             'jelentene. Adja meg a gyakoriságot és a nagyságrendet, és megnézzük, mi a '
             'helyes megközelítés.'),
            ('Van medencénk. Az beleszámít?',
             'A medence feltöltése és a víz cseréje nagy, egyszeri vízmennyiség — ezt '
             'külön kell jelezni, mert ha a szennyvízrendszerbe kerül, hidraulikai '
             'sokkot okozhat. Sok esetben megoldható a külön kezelése.'),
            ('Szezonálisan üzemelünk. Melyik technológia jobb?',
             'Ez éppen az a helyzet, ahol a technológiaválasztás is kérdés, nem csak a '
             'méret. Adja meg a nyitvatartási hónapokat és a leghosszabb szünetet — '
             'ebből derül ki, hogy az aktív rendszer külön üzemmóddal, vagy a passzív '
             'megoldás a relevánsabb.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 2) Éttermek és nagykonyhák
# ===========================================================================
def epit_etterem():
    return [
        sec_prose('Az első üzenet', 'A vendégszám itt kevés', [
            'Egy étterem vagy nagykonyha méretezésénél a vendégszám önmagában nem elég, '
            'mert a konyhai tevékenységből származó használt víz <strong>összetétele '
            'eltérhet</strong> a tisztán kommunális szennyvíztől.',
            'A jogszabály is külön kezeli a termelési és szolgáltatási tevékenységből '
            'eredő szennyvizet: az adott kibocsátásra jellemző szennyező anyagokat, a '
            'technológiai határértékeket és a szükséges előtisztítást külön kell '
            'vizsgálni.',
            'Ezért itt a projekt korán mérnöki kérdéssé válik — és ez nem bonyolítás, '
            'hanem a működő rendszer feltétele.',
        ]),

        sec_split('Két külön szennyvízáram', 'Amit érdemes szétválasztani',
                  'Szociális — vendégek és személyzet',
                  ['Mosdó, WC, kézmosó',
                   'Összetétele kommunális jellegű',
                   'A vendégszámmal arányos',
                   'A szokásos biológiai tisztítás kezeli',
                   'Jellemzően nem igényel előkezelést'],
                  'Konyhai — a főzés és mosogatás vize',
                  ['Mosogatás, előkészítés, takarítás',
                   'Magasabb szerves-, zsír- és olajterhelés',
                   'Az étkezésszámmal és a konyha üzemidejével arányos',
                   'Rövid, intenzív csúcsokkal',
                   'Előkezelést igényelhet — jellemzően zsírleválasztást']),

        sec_numbered('Amit meg kell adni', 'A konyhai terhelési adatlap', '',
                     ['<strong>A létesítmény típusa.</strong> Étterem, vendéglő, büfé, '
                      'rendezvényhelyszín, szálláshelyi vagy intézményi konyha.',
                      '<strong>Napi átlagos és maximális vendégszám.</strong> '
                      'Vagy intézményi konyhánál a napi adagszám.',
                      '<strong>Nyitvatartás és a konyha üzemideje.</strong> A konyhai '
                      'csúcs jellemzően rövidebb és intenzívebb, mint a vendégforgalom.',
                      '<strong>Rendezvény- vagy szezonális csúcs.</strong> Mekkora, '
                      'milyen gyakori, meddig tart.',
                      '<strong>Az ételkészítés típusa.</strong> Zsíros, sült ételek, '
                      'nagy mennyiségű előkészítés — más terhelést jelent.',
                      '<strong>A mosogatási technológia.</strong> Kézi, gépi, '
                      'alagútmosogató — eltérő vízmennyiség és vegyszerhasználat.',
                      '<strong>Meglévő zsírleválasztó.</strong> Ha van: típus, méret, '
                      'a karbantartás gyakorisága.',
                      '<strong>Tényleges vízfogyasztás.</strong> Meglévő üzemnél ez a '
                      'legmegbízhatóbb adat.']),

        sec_prose('A zsírleválasztásról', 'Amit nem állítunk általánosan', [
            'A nagy konyhai zsírterhelés valóban jellemző ok az előkezelésre, és a '
            'jogszabály bizonyos tevékenységek szennyvizénél elő is írja az '
            'előtisztítást.',
            'Azt viszont <strong>nem</strong> állítjuk, hogy minden étteremre ugyanaz a '
            'zsírfogó-követelmény vonatkozik. Hogy szükséges-e, milyen méretben és '
            'milyen kialakításban, azt az adott konyha működéséből és — ahol van — a '
            'mérési adatokból kell levezetni.',
            'A zsír egyébként nem elméleti probléma: a felszínen filmréteget képez és '
            'rontja az oxigénbevitelt, tehát közvetlenül a biológiai fokozat hatásfokát '
            'csökkenti. Ezért nem érdemes „majd meglátjuk” alapon halasztani.',
        ]),

        hiany('a konyhai és éttermi projektek adatai: milyen konyhai adatokból '
              'méretezünk, a laboreredmények, az alkalmazott előkezelési konfigurációk, '
              'a zsírleválasztóval kapcsolatos belső műszaki szabály, a meghibásodási és '
              'karbantartási tapasztalat, valamint a szálláshely + étterem kombinált '
              'rendszerek',
              'ÖkoTech projektarchívum és műszaki csapat. Iparág- és tevékenységfüggő '
              'kibocsátási követelmények projektenként frissen ellenőrizendők'),

        sec_cta('Következő lépés', 'A konyhai adatokkal induljunk',
                ['A konyhai terhelés méretezéséhez korán érdemes szakértőt bevonni. '
                 'A projektbrief összegyűjti, amit ehhez tudni kell.'],
                'Szakmai projektbrief', 'vallalkozas-szakmai-projektbrief',
                alt=('Előkezelés és kiegészítők',
                     '../megoldasok/nagyobb-elokezeles-es-kiegeszitok')),

        sec_faq([
            ('Kötelező a zsírfogó?',
             'Nem állítjuk általánosan. A jogszabály bizonyos tevékenységek szennyvizénél '
             'előtisztítást ír elő, és a konyhai zsírterhelés jellemző ok — de hogy az '
             'Ön üzemében szükséges-e és milyen méretben, azt a konyha működéséből kell '
             'levezetni. A konkrét projektnél ezt megvizsgáljuk.'),
            ('Szétválasztható a konyhai és a vendégek szennyvize?',
             'Sok üzemben igen, és gyakran ez a legolcsóbb megoldás: a szociális ág a '
             'szokásos módon kezelhető, a konyhai pedig külön előkezelést kap. Érdemes '
             'ezt már a tervezéskor megvizsgálni — utólag lényegesen nehezebb.'),
            ('Kell laborvizsgálat?',
             'Nagyobb konyhai terhelésnél jellemzően igen. Enélkül a méretezés '
             'feltételezésen alapulna, és éppen a legkockázatosabb tételnél. A vizsgálat '
             'költsége töredéke annak, amibe egy alulméretezett rendszer helyreállítása '
             'kerül.'),
            ('Vendéglátás melletti szálláshelyünk van.',
             'Akkor két terhelési profil áll össze: a szálláshelyi és a konyhai. Ezeket '
             'külön kell megadni, és a méretezésnél is külön kezelni — a kettő nem '
             'egyszerűen összeadódik.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 3) Iskolák és intézmények
# ===========================================================================
def epit_intezmeny():
    return [
        sec_prose('Más ritmus', 'Az intézmény terhelése nem lakóépület-jellegű', [
            'Egy iskola vagy intézmény terhelése másképp változik, mint egy családi házé '
            'vagy egy szálláshelyé: erős hétköznapi nappali csúcs, hétvégi visszaesés és '
            'hosszabb szünetek egyaránt jelentkeznek.',
            'A névleges tanulói vagy dolgozói létszám ezért önmagában félrevezető. '
            'A 300 fő nem egyszerre, nem egész nap és nem egész évben használja a '
            'létesítményt.',
        ]),

        sec_numbered('Amit meg kell adni', 'Az intézményi működési profil', '',
                     ['<strong>Intézménytípus.</strong> Iskola, óvoda, iroda, szociális '
                      'intézmény, közösségi épület, sportlétesítmény.',
                      '<strong>Névleges és tényleges létszám.</strong> Hányan vannak '
                      'nyilvántartva, és jellemzően hányan vannak jelen.',
                      '<strong>Napi használati idő.</strong> Hány órát töltenek bent. '
                      'A négy órát bent töltő óvodás nem ugyanaz a terhelés, mint egy '
                      'bentlakó.',
                      '<strong>Hétvégi használat.</strong> Van-e, és milyen mértékű.',
                      '<strong>Szünetek és éves üzemnapok.</strong> Nyári és téli '
                      'szünet — ezek hosszú alulterhelési időszakok.',
                      '<strong>Étkeztetés.</strong> Van-e főzőkonyha, hány adag, milyen '
                      'üzemidőben. Ha van, az külön ág.',
                      '<strong>Sport, rendezvény, bentlakás.</strong> Tornaterem '
                      'zuhanyzóval, esti rendezvények, kollégium — mind külön terhelési '
                      'ablak.',
                      '<strong>Tényleges vízfogyasztás.</strong> Meglévő intézménynél ez '
                      'megvan, és lényegesen pontosabb minden becslésnél.']),

        sec_prose('A nagykonyháról', 'Nem olvasztható be a személyszámba', [
            'Ha az intézményben főzőkonyha működik, annak szennyvizét külön '
            '<strong>nagykonyhai terhelési ágként</strong> kell kezelni — nem egyszerűen '
            'hozzáadni a személyszámhoz.',
            'Eltérő az összetétele, más az időbeli eloszlása, és előkezelést igényelhet. '
            'Egy konyhás és egy konyha nélküli, azonos létszámú iskola két különböző '
            'projekt.',
        ]),

        sec_prose('Az üzemeltetés szervezeti kérdés', 'Nem elég, hogy „bárki elsajátítja”', [
            'Intézményi méretben az üzemeltetés nem melléktevékenység. A jogszabály az '
            'egyedi rendszereknél is rendszeres ellenőrzést, üzemnapló vezetését, '
            'karbantartást és bizonyos esetekben mintavételt ír elő — nagyobb projektnél '
            'pedig még egyértelműbb felelős üzemeltetési rend szükséges.',
            'Ezért az intézményi projektnél előre tisztázandó: <strong>ki</strong> a '
            'nevesített felelős, milyen betanítást kap, ki helyettesíti szünetben és '
            'szabadság idején, ki vezeti a dokumentációt, és milyen szervizkonstrukció '
            'tartozik hozzá.',
            'Ez fenntartói döntés, nem műszaki részletkérdés — és jellemzően ezen szokott '
            'elakadni egy egyébként jól megtervezett intézményi rendszer.',
        ]),

        hiany('az intézményi referenciák: iskolai és más intézményi projektek névleges '
              'létszámmal és valós m³/nap adattal, a tanítási szünet alatti működés '
              'tapasztalatai, a konyhával rendelkező intézmények külön, üzemeltetési '
              'naplók, laboreredmények, szervizterhelés, valamint az intézményi '
              'betanítás és támogatás tartalma',
              'ÖkoTech projektarchívum. Lakossági ügyfélvélemény itt nem elég '
              'bizonyíték — hasonló létszámú, hasonló napi ritmusú, többéves intézményi '
              'referencia kell'),

        sec_cta('Következő lépés', 'Az üzemeltetési modellt is tisztázzuk',
                ['Intézményi rendszernél a monitoring és az üzemeltetés az ajánlat '
                 'előtti kérdés. A Megoldások szakasz erről szóló oldala részletesen '
                 'végigveszi.'],
                'Monitoring és üzemeltetés',
                '../megoldasok/nagyobb-monitoring-es-uzemeltetes',
                alt=('Szakmai projektbrief', 'vallalkozas-szakmai-projektbrief')),

        sec_faq([
            ('Az iskola 300 fős. Milyen rendszer kell?',
             'Ebből az egy adatból nem megállapítható. Kell hozzá a tényleges napi '
             'jelenlét, a bent töltött idő, az éves üzemnapok, a szünetek és az, hogy van-e '
             'főzőkonyha. Meglévő intézménynél a vízfogyasztás mindezt jól közelíti — '
             'azzal érdemes kezdeni.'),
            ('Mi történik a nyári szünetben?',
             'Hosszú alulterhelési időszak keletkezik, amit kezelni kell. Ez üzemmód- és '
             'technológiaválasztási kérdés, és a méretezésnél is számít: a rendszernek a '
             'szüneti állapotot is bírnia kell, nem csak a tanítási időszakot.'),
            ('Ki üzemelteti majd?',
             'Ezt a fenntartónak kell eldöntenie, és érdemes a tervezéskor. Nevesített '
             'felelős kell, betanítással, helyettesítéssel és dokumentációs renddel. '
             'Ez gyakran szervezeti kérdés, nem műszaki.'),
            ('Közbeszerzési eljárásban vagyunk.',
             'Ilyenkor a műszaki tartalom pontos meghatározása különösen fontos, mert az '
             'ajánlatok összehasonlíthatósága ezen múlik. Szívesen segítünk a műszaki '
             'leírás összeállításában — írja meg, hol tart az eljárás.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 4) Kempingek és közösségi létesítmények
# ===========================================================================
def epit_kemping():
    return [
        sec_prose('A legszélsőségesebb terhelés', '', [
            'Kempingeknél és közösségi rendszereknél a terhelés gyakran sokkal '
            'szélsőségesebben változik, mint egy állandó lakóingatlanban: hosszú '
            'alacsony kihasználtság, majd rövid idő alatt teljes kapacitás.',
            'Ezért a tervezéshez nem a maximális személyszám kell, hanem a '
            '<strong>szezonális kihasználtsági görbe</strong>, a napi csúcsok, a '
            'vizesblokkok száma, az esetleges vendéglátás — és az, hogy több épületből '
            'vagy közös gyűjtőrendszerből érkezik-e a szennyvíz.',
        ]),

        sec_numbered('Amit meg kell adni', 'A szezonális és közösségi profil', '',
                     ['<strong>A létesítmény típusa.</strong> Kemping, üdülőtábor, '
                      'közösségi szállás, házcsoport, több ingatlan közös rendszere, '
                      'kisebb településrész.',
                      '<strong>Maximális és átlagos létszám.</strong> A kettő közötti '
                      'különbség itt a legnagyobb.',
                      '<strong>Havi vagy szezonális kihasználtság.</strong> Hónapos '
                      'bontásban — ez a legfontosabb egyetlen adatsor.',
                      '<strong>Csúcsnapok.</strong> Hosszú hétvégék, ünnepek, '
                      'rendezvények.',
                      '<strong>Vizesblokkok száma és elhelyezkedése.</strong> Több '
                      'csatlakozási pont eltérő hálózati kialakítást igényel.',
                      '<strong>Étterem, konyha, mosoda.</strong> Külön vízáramok.',
                      '<strong>Szezonon kívüli állapot.</strong> Teljesen zárva, '
                      'minimális őrszemélyzet, vagy részleges üzem.',
                      '<strong>A belső csatornahálózat kialakítása.</strong> Több '
                      'épületnél ez önálló tervezési feladat.']),

        sec_prose('A közös üzemeltetés', 'Ami nem műszaki kérdés', [
            'Közösségi rendszernél — házcsoport, több ingatlan közös megoldása, '
            'településrész — a tulajdonosi és üzemeltetői felelősség önálló tartalmi '
            'kérdés, és jellemzően ezen múlik a projekt hosszú távú sikere.',
            'Előre tisztázandó: <strong>ki vezeti a naplót</strong>, ki végzi a '
            'rendszeres ellenőrzést, ki hív szervizt, és <strong>milyen módon oszlik meg '
            'az üzemeltetési költség</strong>.',
            'A jogszabály programszerű telepítésnél felelős szolgáltatói és '
            'monitoringkövetelményeket is megfogalmaz — ezért a közösségi projekt nem '
            'kezelhető úgy, mintha több családi ház összeadása lenne.',
        ]),

        sec_split('Két szezonális kockázat', 'Amit külön kell kezelni',
                  'Hosszú alacsony terhelés',
                  ['A biológia tápanyag nélkül marad',
                   'Az aktív rendszernél külön üzemmód vagy leállítás kell',
                   'A szezonzárás tervezett folyamat',
                   'Az áramellátás a szünetben is kérdés',
                   'A passzív rendszer ezt jobban tűri'],
                  'Hirtelen visszatérő csúcs',
                  ['A szezonnyitás első hétvégéje gyakran azonnal telt ház',
                   'A biológia újraindulása időt vesz igénybe',
                   'A szezonnyitást előre kell ütemezni',
                   'Ez üzemeltetési feladat, nem magától megy',
                   'A méretezésnek a visszatérési csúcsot is bírnia kell']),

        hiany('a kemping- és közösségi projektek adatai: szezonális terhelési görbék, a '
              'maximális és minimális működési terhelés, az indítási és leállítási '
              'protokoll, a közösségi üzemeltetési modellek, szerviz- és laboradat, a '
              'többépületes hálózatok tapasztalatai, valamint a települési projektek '
              'működési tapasztalatai',
              'ÖkoTech projektarchívum. Külön frissen ellenőrizendő: a programszerű '
              'telepítés aktuális jogi fogalma és feltételei, a felelős szolgáltatói és '
              'monitoringkövetelmények'),

        sec_cta('Következő lépés', 'A rendszerforma is kérdés',
                ['Több épület, több csatlakozási pont és bővíthetőség esetén a '
                 'moduláris kialakítás jöhet szóba. A Megoldások szakasz áttekintő '
                 'oldala ezt veszi végig.'],
                'Megoldások áttekintése', '../megoldasok/nagyobb-megoldasok-attekintese',
                alt=('Szakmai projektbrief', 'vallalkozas-szakmai-projektbrief')),

        sec_faq([
            ('A maximális kapacitásra kell méretezni?',
             'Nem feltétlenül — de a szezonális csúcsot nem lehet figyelmen kívül hagyni. '
             'A helyes megközelítés a szezonális görbéből indul: mennyi ideig tart a '
             'csúcs, milyen gyakran, és mekkora az alatta lévő átlag.'),
            ('Több épületből érkezik a szennyvíz.',
             'Ilyenkor a belső gyűjtőhálózat kialakítása önálló tervezési feladat, és a '
             'rendszerforma is kérdés: egy központi telep vagy több elosztott egység. '
             'Ez a projekt egyik korai döntése.'),
            ('Ki lesz a felelős egy közös rendszernél?',
             'Ezt a tulajdonosi körnek kell eldöntenie, és érdemes írásban rögzíteni: '
             'ki üzemeltet, ki vezeti a dokumentációt, és hogyan oszlik meg a költség. '
             'Sok közösségi projekt nem műszaki, hanem éppen ezen a ponton akad el.'),
            ('Télen nem üzemelünk. Mi legyen a rendszerrel?',
             'Ez tervezett szezonzárási és -nyitási eljárást igényel. A pontos lépések '
             'technológiafüggők — és éppen ezért a szezonalitás a technológiaválasztás '
             'egyik bemenete, nem utólagos kérdés.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 5) Üzemek és speciális terhelések
# ===========================================================================
def epit_uzem():
    return [
        sec_prose('Az „üzem” nem méretezési kategória', '', [
            'Teljesen más projekt egy iroda dolgozóinak kommunális szennyvize és egy '
            'termelési technológiából származó szennyvíz kezelése — akkor is, ha a '
            'létszám azonos.',
            'A jogszabály is önálló szennyvízkategóriaként kezeli a termelési és '
            'szolgáltatási tevékenység során keletkező használt vizet, és iparág- '
            'illetve szennyezőanyag-specifikus kibocsátási határértékeket állapíthat meg. '
            'Ezért a szennyvíz összetétele nem vezethető le a személyszámból vagy a '
            'napi vízmennyiségből.',
        ]),

        sec_numbered('Az első lépés', 'Válassza szét a két vízáramot',
                     'Ez a legfontosabb egyetlen döntés ezen az oldalon — és sok '
                     'esetben ez a legolcsóbb megoldás is.',
                     ['<strong>Szociális, kommunális ág.</strong> A dolgozók mosdója, '
                      'öltözője, konyhája. Összetétele háztartási jellegű, a szokásos '
                      'módon kezelhető.',
                      '<strong>Technológiai ág.</strong> A gyártásból, mosásból, '
                      'öblítésből származó víz. Összetételét a technológia határozza '
                      'meg, és jellemzően előkezelést igényel.',
                      '<strong>Miért érdemes szétválasztani.</strong> A kommunális ág '
                      'egyszerűen kezelhető; a technológiai ág külön előkezelést kap, '
                      'a méretének megfelelően. Együtt kezelve a teljes mennyiséget '
                      'a szigorúbb követelményhez kell tervezni.']),

        sec_numbered('Amit meg kell adni', 'A technológiai adatlap', '',
                     ['<strong>A telephely tevékenysége.</strong> Mi készül, milyen '
                      'folyamatokkal.',
                      '<strong>Alap- és segédanyagok.</strong> Ami a vízbe kerülhet.',
                      '<strong>Műszakok száma és éves üzemnapok.</strong>',
                      '<strong>Idényjelleg.</strong> A borászat szüret idején egészen '
                      'mást termel, mint télen — az idényjelleg a csúcsterhelést '
                      'határozza meg.',
                      '<strong>Napi és maximális vízmennyiség.</strong> Átlagos és '
                      'csúcs m³/nap, valamint az órás vagy műszakonkénti csúcs.',
                      '<strong>Technológiai mosó- és öblítővizek.</strong> Mikor, '
                      'mennyi, milyen összetétellel.',
                      '<strong>Használt vegyszerek.</strong> Tisztító-, fertőtlenítő- '
                      'és technológiai szerek.',
                      '<strong>Szennyvízhőmérséklet.</strong> Ahol releváns — a '
                      'biológiai folyamatot befolyásolja.',
                      '<strong>Laboreredmények.</strong> BOI5, KOI, lebegőanyag; '
                      'iparágtól függően zsír és olaj, nitrogén, foszfor, pH és egyéb '
                      'komponensek. A pontos listát a technológia határozza meg.',
                      '<strong>Meglévő előkezelés.</strong> Rács, zsírfogó, ülepítő, '
                      'kiegyenlítő medence.']),

        sec_prose('Amit erről az oldalról nem kap', 'És miért nem', [
            'Nincs itt kapacitástáblázat és nincs modellajánlás. Ahol nincs '
            'reprezentatív laboradat, ott a weboldal nem próbál automatikus '
            'rendszerjavaslatot adni — a természetes következő lépés a '
            '<strong>mintavétel és szakértői megvalósíthatósági vizsgálat</strong>.',
            'A korábbi tájékoztatásunk vágóhídi, tejüzemi és borászati szennyvíz '
            'biológiai tisztítását is megoldhatóként említette. Ez a szakmai képesség '
            'létezhet, de weboldalon nem lehet belőle automatikus méretezés: a bemeneti '
            'vízminőség és a szükséges előkezelés projektenként más.',
            'Amíg nincs bemutatható projekt bemeneti szennyvízjellemzővel, előkezeléssel, '
            'technológiával, kibocsátási követelménnyel, laboreredménnyel és működési '
            'időtávval, a helyes megfogalmazás ez: <strong>speciális terhelések egyedi '
            'mérnöki vizsgálat és tervezés alapján kezelhetők</strong>.',
            'Ez nem óvatoskodás. Egy rosszul méretezett ipari rendszer nem a beruházó '
            'pénzét pazarolja el először, hanem a kibocsátási követelmények teljesítését '
            'teszi lehetetlenné — és azt utólag lényegesen nehezebb korrigálni.',
        ]),

        hiany('az ipari referenciák: vágóhídi, tejüzemi, borászati és egyéb ipari '
              'projektek bemeneti és kimeneti laboreredményekkel, az alkalmazott '
              'előkezelés, a névleges és csúcsterhelés, a működési időtáv, a szerviz- és '
              'meghibásodási adatok, a projekttervező szakértők — és külön: MIT NEM '
              'VÁLLAL az ÖkoTech',
              'ÖkoTech mérnöki csapat. Az iparági hitelesség kizárólag megvalósult '
              'projekten és laboradaton alapulhat; enélkül ez az oldal a folyamatot írja '
              'le, nem a képességet'),

        sec_cta('Következő lépés', 'Kezdjük a technológiával',
                ['Írja meg, mi a tevékenység, hány műszakban, milyen éves ritmusban, és '
                 'hogy van-e már laboreredmény. Ebből meg tudjuk mondani, elegendő-e a '
                 'meglévő adat, vagy mintavétellel kell kezdeni.'],
                'Szakmai projektbrief', 'vallalkozas-szakmai-projektbrief',
                alt=('Speciális vagy ipari szennyvíz',
                     '../projekt-elokeszites/specialis-vagy-ipari-szennyviz')),

        sec_faq([
            ('Nincs laboreredményünk. Így is lehet ajánlatot kérni?',
             'Ajánlatot felelősen nem, megvalósíthatósági egyeztetést viszont igen. '
             'A technológia, a munkarend és a vízhozam alapján meg tudjuk mondani, '
             'milyen vizsgálat szükséges és milyen nagyságrendről van szó. '
             'A méretezéshez a laboradat elkerülhetetlen.'),
            ('Milyen laborparaméterek kellenek?',
             'A minimum jellemzően BOI5, KOI és lebegőanyag; ezen felül iparágtól '
             'függően zsír és olaj, nitrogén, foszfor, pH és hőmérséklet. A pontos '
             'listát a technológia határozza meg — ezért kérdezünk rá először a '
             'gyártási folyamatra.'),
            ('Van olyan, amit nem vállalnak?',
             'Igen, és ezt előre megmondjuk. Vannak technológiai szennyvizek, amelyek '
             'biológiai úton nem vagy csak jelentős előkezeléssel kezelhetők. Ha ez a '
             'helyzet, azt a megvalósíthatósági vizsgálat során jelezzük — nem az '
             'ajánlat után.'),
            ('Külön kezelhető a dolgozói szennyvíz?',
             'Sok üzemben igen, és gyakran ez a legolcsóbb megoldás. Érdemes már a '
             'tervezéskor megvizsgálni, mert utólag a hálózat szétválasztása jelentős '
             'munka.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 6) Szakmai projektbrief
# ===========================================================================
def epit_brief():
    return [
        sec_prose('Több, mint ajánlatkérő', '', [
            'Egy intézmény vagy vállalkozás szennyvízterhelése nem írható le néhány '
            'személyszám- és telekmezővel. Ezért ez az oldal nem általános ajánlatkérő, '
            'hanem strukturált <strong>projektadat-csomag</strong>.',
            'Ebből eldönthető, hogy a projekt standard konfiguráció, részletes mérnöki '
            'méretezés, helyszíni felmérés, laborvizsgálat vagy külön megvalósíthatósági '
            'vizsgálat irányába megy.',
            'A cél az, hogy a szakértőnk strukturált döntési helyzetet kapjon, ne egy '
            '„200 fős szállodához kérek árat” típusú nyers megkeresést — és hogy Ön se '
            'azt hallja vissza, hogy „ehhez több adat kell”.',
        ]),

        sec_numbered('Amit a brief rögzít', 'Hat adatcsoport', '',
                     ['<strong>Projektazonosítás.</strong> Létesítménytípus, település, '
                      'projektfázis, tervezett üzembe helyezés, új vagy meglévő rendszer.',
                      '<strong>Terhelés.</strong> Névleges létszám vagy férőhely, '
                      'átlagos napi létszám, csúcslétszám, m³/nap átlag és maximum, '
                      'működési napok, szezonális görbe, műszakok.',
                      '<strong>A szennyvíz jellege.</strong> Tisztán kommunális, '
                      'nagykonyhai, technológiai vagy több eredetű elegy; meglévő '
                      'laboreredmény; meglévő előkezelés.',
                      '<strong>Telek és befogadó.</strong> Rendelkezésre álló terület, '
                      'csőszintek, talaj és talajvíz, befogadó, közcsatorna, meglévő '
                      'hálózat.',
                      '<strong>Műszaki készültség.</strong> Meglévő tervek, technológiai '
                      'vízáramok, bővítési tartalék, monitoringigény, redundanciaigény.',
                      '<strong>Üzemeltetés.</strong> Felelős üzemeltető, karbantartási '
                      'modell, szervizelvárás, dokumentáció, naplózás, beszerzési '
                      'folyamat.']),

        sec_split('A kimenet', 'Mit ad vissza, és mit nem',
                  'Ezt kapja',
                  ['Projektkategória — melyik ágra esik',
                   'Adatkomplettség: mi van meg, mi hiányzik',
                   'A szükséges labor- vagy felmérési feladatok',
                   'Melyik szakértő bevonása indokolt',
                   'Konzultációs napirend',
                   'Ajánlatkészültségi állapot'],
                  'Ezt nem kapja',
                  ['Automatikus konkrét árat',
                   'Ársávot tisztázatlan projektterjedelemre',
                   'Garantált kapacitást hiányos adatokból',
                   'Automatikus ipari méretezést laboradat nélkül',
                   'Jogi engedélyezhetőségi ígéretet',
                   'Végleges termékmodellt']),

        sec_numbered('Amit érdemes csatolni', 'Dokumentumok',
                     'Ezekkel lényegesen gyorsabban jutunk műszaki irányig. Az adataikat '
                     'kizárólag a megkeresés megválaszolására használjuk.',
                     ['Helyszínrajz',
                      'Gépészeti terv',
                      'Fogyasztási adatsor — vízszámla vagy mérőóra-adatok',
                      'Laboreredmény, ha van',
                      'Korábbi terv vagy engedély',
                      'Meglévő ajánlat, ha összehasonlítást szeretne']),

        sec_prose('Ipari szennyvíznél', 'Egy külön szabály', [
            'Technológiai szennyvíznél laboreredmény vagy reprezentatív mintavétel '
            'nélkül a brief <strong>nem ad</strong> ajánlott terméket vagy méretet. '
            'Az eredmény ilyenkor „szakértői vizsgálat szükséges” — és ez nem elutasítás, '
            'hanem a helyes első lépés.',
            'Ez azért fontos, mert az ipari projektben a legdrágább hiba nem a rosszul '
            'megválasztott berendezés, hanem az, ha a kibocsátási követelmény nem '
            'teljesíthető. Azt utólag lényegesen nehezebb korrigálni.',
        ]),

        hiany('a brief belső rendje: milyen mezőket kér ma a nagyprojektes értékesítő, '
              'milyen adatot kér vissza rendszeresen, milyen dokumentum kell indikatív '
              'és milyen végleges műszaki ajánlathoz, mely projekttípusnál kell labor és '
              'milyen paraméterekkel, mikor kötelező a helyszíni felmérés, mikor kell '
              'külső tervező, ki végzi az engedélyezést, és mit vállal az ÖkoTech a '
              'tervezésből, telepítésből és üzemeltetésből',
              'ÖkoTech értékesítés és műszaki vezetés — közös workshop. A modul addig a '
              'brief SZERKEZETÉT írja le; az űrlap élesítése ezután következik'),

        sec_cta('Addig is', 'Vegyük végig együtt',
                ['Amíg a strukturált brief nem üzemel, ugyanezt élőben végigvesszük. '
                 'Írja meg a létesítmény típusát, a nagyságrendet, a működési profilt és '
                 'azt, hol tart a projekt — a többit megkérdezzük.',
                 'Ha vannak dokumentumai — helyszínrajz, vízszámla, laboreredmény, '
                 'korábbi terv —, csatolja: azokkal sokkal gyorsabban jutunk műszaki '
                 'irányig.'],
                'Kapcsolatfelvétel', '../kapcsolat',
                alt=('Szakmai konzultáció', '../megoldasok/nagyobb-szakmai-konzultacio')),

        sec_faq([
            ('Miért nem kapok azonnal árat?',
             'Mert üzleti és intézményi projektnél a kapacitás vagy a férőhely alapján '
             'közölt ár félrevezető lenne. A teljes projekt- és életciklusköltséget a '
             'rendszerarchitektúra, az előkezelés, a telepítés, a monitoring és az '
             'üzemeltetés együtt határozza meg. Tisztázott projektterjedelemnél viszont '
             'adható ársáv.'),
            ('Mennyi adat kell a megkereséshez?',
             'A beszélgetéshez elég a létesítmény típusa és a nagyságrend. Ahhoz, hogy '
             'műszaki irányt tudjunk mondani, kell a terhelési profil és a szennyvíz '
             'jellege. Ajánlathoz ezeken felül a telek, a befogadó és az üzemeltetési '
             'modell is.'),
            ('Beszerzési eljárásban vagyunk, műszaki leírás kell.',
             'Ebben szívesen segítünk. A pontos műszaki tartalom éppen azért fontos, '
             'mert az ajánlatok összehasonlíthatósága ezen múlik — és hiányos leírásból '
             'nem összevethető ajánlatok születnek.'),
        ]),
        JOGI,
    ]


# ===========================================================================
OLDALAK = [
    dict(file='helyzetem/vallalkozas-vagy-intezmeny-szamara-keresek-megoldast.html',
         url='helyzetem/vallalkozas-vagy-intezmeny-szamara-keresek-megoldast',
         img='vallalkozas',
         title='Vállalkozás vagy intézmény számára keresek megoldást | ÖkoTech Home',
         desc='Panzió, étterem, iskola, kemping, üzem. Miért nem elég a létszám, és '
              'hogyan kategorizálható a projekt a terhelés és a szennyvíz eredete szerint.',
         h1='Vállalkozás vagy intézmény számára keresek megoldást',
         alt='Vidéki panzió és melléképületei madártávlatból, körülöttük parkoló és kert',
         lead='A „hányan használják?” itt különösen félrevezető. Egy panzió, egy iskola és '
              'egy üzem mondhatja ugyanazt a számot — és három teljesen különböző projekt '
              'lesz belőle.',
         crumbs=CRUMB, sections=epit_hub()),

    dict(file='helyzetem/vallalkozas-panziok-es-szallashelyek.html',
         url='helyzetem/vallalkozas-panziok-es-szallashelyek', img='telepek',
         title='Panziók és szálláshelyek — terhelési profil | ÖkoTech Home',
         desc='A férőhely nem terhelés. Kihasználtság, csúcshétvégék, szezon, mosoda, '
              'wellness — és ami a szezonon kívüli üzemben történik.',
         h1='Panziók és szálláshelyek',
         alt='Panzió reggeliző terasza megterített asztalokkal, háttérben a szálláshely',
         lead='Egy húszférőhelyes panzió nem azonos terhelés akkor, ha egész évben '
              'működik, és akkor, ha csak nyári hétvégéken telik meg.',
         crumbs=HUB, sections=epit_panzio()),

    dict(file='helyzetem/vallalkozas-ettermek-es-nagykonyhak.html',
         url='helyzetem/vallalkozas-ettermek-es-nagykonyhak', img='alternativak',
         title='Éttermek és nagykonyhák — konyhai terhelés | ÖkoTech Home',
         desc='A konyhai szennyvíz nem kezelhető ugyanúgy, mint egy azonos létszámú '
              'lakóingatlané. Előkezelés, laboradat, és amit nem állítunk általánosan.',
         h1='Éttermek és nagykonyhák',
         alt='Nagykonyha rozsdamentes munkapultokkal és mosogatórendszerrel',
         lead='A vendégszám itt kevés. A konyhai víz összetétele eltér a kommunálistól — '
              'és éppen ez határozza meg, mi kerül a biológiai fokozat elé.',
         crumbs=HUB, sections=epit_etterem()),

    dict(file='helyzetem/vallalkozas-iskolak-es-intezmenyek.html',
         url='helyzetem/vallalkozas-iskolak-es-intezmenyek', img='kozcsatorna',
         title='Iskolák és intézmények — működési profil | ÖkoTech Home',
         desc='Erős napi ritmus, hétvégi visszaesés, hosszú szünetek. És a kérdés, ami '
              'szervezeti: ki lesz a felelős üzemeltető.',
         h1='Iskolák és intézmények',
         alt='Iskolaépület udvara szünetben, háttérben tornaterem',
         lead='A 300 fő nem egyszerre, nem egész nap és nem egész évben használja a '
              'létesítményt. A névleges létszám ezért önmagában félrevezető.',
         crumbs=HUB, sections=epit_intezmeny()),

    dict(file='helyzetem/vallalkozas-kempingek-es-kozossegi.html',
         url='helyzetem/vallalkozas-kempingek-es-kozossegi', img='nyaralo',
         title='Kempingek és közösségi létesítmények | ÖkoTech Home',
         desc='Szélsőségesen változó terhelés, több felhasználói pont, közös '
              'üzemeltetési felelősség — és a szezonnyitás mint tervezett folyamat.',
         h1='Kempingek és közösségi létesítmények',
         alt='Kemping vizesblokkja és sátorhelyek fák között nyáron',
         lead='Hosszú alacsony kihasználtság, majd rövid idő alatt teljes kapacitás. '
              'A tervezéshez nem a maximum kell, hanem a szezonális görbe.',
         crumbs=HUB, sections=epit_kemping()),

    dict(file='helyzetem/vallalkozas-uzemek-es-specialis-terhelesek.html',
         url='helyzetem/vallalkozas-uzemek-es-specialis-terhelesek', img='emeszto-csere',
         title='Üzemek és speciális terhelések | ÖkoTech Home',
         desc='Az „üzem” nem méretezési kategória. Kommunális és technológiai vízáram '
              'szétválasztása, technológiai adatlap, laboradat.',
         h1='Üzemek és speciális terhelések',
         alt='Élelmiszeripari üzem csarnoka rozsdamentes tartályokkal és vezetékekkel',
         lead='Egy iroda dolgozóinak szennyvize és egy termelési technológiából származó '
              'szennyvíz nem ugyanaz a feladat — akkor sem, ha a létszám azonos.',
         crumbs=HUB, sections=epit_uzem()),

    dict(file='helyzetem/vallalkozas-szakmai-projektbrief.html',
         url='helyzetem/vallalkozas-szakmai-projektbrief', img='kapcsolat',
         title='Szakmai projektbrief — üzleti és intézményi projektekhez | ÖkoTech Home',
         desc='Strukturált projektadat-csomag: kategória, adatkomplettség, hiánylista, '
              'szükséges vizsgálatok és konzultációs napirend.',
         h1='Szakmai projektbrief',
         alt='Tárgyalóasztal műszaki rajzokkal, laptoppal és jegyzetekkel',
         lead='Nem általános ajánlatkérő. A cél az, hogy a szakértőnk strukturált '
              'döntési helyzetet kapjon — és Ön se azt hallja vissza, hogy „ehhez több '
              'adat kell”.',
         crumbs=HUB, sections=epit_brief()),
]

if __name__ == '__main__':
    for o in OLDALAK:
        out = WEB / o['file']
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:60s} {len(out.read_text(encoding='utf-8'))//1024} KB")
