#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Megoldások → Nagyobb és közösségi rendszerek — hub és nyolc aloldal.

A brief HÉT ponton pontosít:

1. AZ 50–100 LE KÖZÖTTI ÚT RENDEZETLEN. A lakossági oldal 1–50 főig
   kommunikál, majd 50 fő felett a nagytelepi oldalra irányít — az viszont
   100 LE feletti, kb. 75–750 fős rendszerekről szól. A közte lévő sáv nincs
   lefedve, és a 147/2010. szerinti „egyedi szennyvíztisztítás" felső határa
   50 LE, tehát ez valódi szabályozási választóvonal is.

2. A „lakosegyenérték = 135 liter/fő/nap" itt is javítandó:
   LE = szerves terhelés · m³/nap = hidraulikai terhelés · fő = közelítő adat.

3. Az engedélyezési szöveg elavult hatóságot nevez meg. Ezt nem szabad
   átvinni; az aktuális eljárást és illetékes szervet publikáláskor és
   rendszeresen újra kell ellenőrizni.

4. A „víz újrahasznosítása" projektspecifikus: elszikkasztás, felszíni
   befogadó és hasznosítás külön ág, eltérő vízminőségi, monitoring- és
   engedélyezési feltételekkel.

5. Az ipari alkalmassági állításokat referenciával és laboradattal kell
   igazolni. Enélkül a helyes megfogalmazás: „speciális terhelések egyedi
   mérnöki vizsgálat alapján".

6. A monitoring nem opcionális utógondolat, hanem az ajánlat előtt tisztázandó.

7. ÁR EZEN AZ ÁGON SEM JELENIK MEG.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import (sec_numbered, sec_split, sec_prose, sec_situations,
                    sec_cta, sec_faq)

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

JOGI = ('<!-- JOGI ELLENŐRZÉS PUBLIKÁLÁS ELŐTT ÉS RENDSZERESEN. Érintett: 147/2010.\n'
        '     Korm. rendelet (1–50 LE egyedi kategória) · 220/2004. Korm. rendelet\n'
        '     (engedélykérő dokumentáció, üzemnapló, önellenőrzés) · 28/2004. KvVM\n'
        '     rendelet (kibocsátási határértékek, előtisztítás) · 27/2005. KvVM rendelet\n'
        '     (mintavétel és ellenőrzés). AZ ILLETÉKES HATÓSÁG MEGNEVEZÉSE gyorsan\n'
        '     avul — a korábbi szövegünk már nem létező szervezetet nevezett meg. -->')


def hiany(mi, honnan):
    return (f'<!-- ADATHIÁNY: {mi}\n'
            f'     Forrás: {honnan}. Addig konkrét értékkel nem publikálható. -->')


HOME = ('Főoldal', '../')
MEG = ('Megoldások', './')
CRUMB = [HOME, MEG]
HUB = [HOME, MEG, ('Nagyobb és közösségi rendszerek', 'nagyobb-es-kozossegi-rendszerek')]


# ===========================================================================
# HUB
# ===========================================================================
def epit_hub():
    return [
        sec_prose('Az alapállítás', 'Nem egy nagyobb családi berendezés', [
            'A nagyobb szennyvíztisztító projekt nem egy családi berendezés nagyobb '
            'változata. Terhelési, technológiai, üzemeltetési és engedélyezési '
            'szempontból <strong>önálló projektkategória</strong>, más tervezési úttal '
            'és más felelősségi rendszerrel.',
            'A leggyakoribb hiba az, hogy a projekt lakossági logikával indul el: '
            'megkérdezik, hány fő, kiválasztanak egy méretet, és a monitoring, az '
            'előkezelés meg az üzemeltetés csak a végén kerül elő. Nagyobb rendszernél '
            'ezek nem részletkérdések — a projekt szerkezetét határozzák meg.',
            'Ez a szakasz ezért nem terméket ajánl, hanem <strong>kategorizál</strong>: '
            'standardizálható kommunális terhelésű, moduláris közösségi vagy teljesen '
            'egyedi mérnöki rendszerről van-e szó.',
        ]),

        sec_split('Három fogalom', 'Amit nem szabad összevonni',
                  'LE — lakosegyenérték',
                  ['A biológiailag bontható SZERVES terhelés egysége',
                   '1 LE = napi 60 g BOI5',
                   'Ez határozza meg a jogi kategóriát is (1–50 LE)',
                   'Laborvizsgálattal mérhető',
                   'NEM azonos a napi vízmennyiséggel'],
                  'm³/nap és „fő”',
                  ['m³/nap = HIDRAULIKAI terhelés, a beérkező vízmennyiség',
                   'A vízóráról leolvasható, meglévő létesítménynél mért adat',
                   '„Fő” = használati közelítő adat, nem méretezési egység',
                   'Intézménynél és üzemnél a fő különösen félrevezető',
                   'A három adatot külön kell megadni']),

        sec_prose('Egy korrekció', 'Az „1 LE = 135 liter/fő/nap” állítás téves', [
            'A korábbi tájékoztatásunk egy helyen úgy fogalmazott, hogy 1 lakosegyenérték '
            'napi 135 liter/fő vízfogyasztást jelent. Ezt pontosítjuk: a lakosegyenérték '
            '<strong>szervesanyag-terhelési egység</strong>, nem vízmennyiség.',
            'A 135 liter/fő/nap érték legfeljebb saját <strong>hidraulikai tervezési '
            'alapértékként</strong> maradhat meg — ha a műszaki csapat továbbra is ezzel '
            'számol és dokumentálni tudja. De a két fogalmat terminológiailag szét kell '
            'választani.',
            'Nagyobb projektnél ez nem szőrszálhasogatás: egy nagykonyhás intézmény '
            'vízfogyasztása és szerves terhelése egészen máshogy arányulnak egymáshoz, '
            'mint egy lakóépületé.',
        ]),

        sec_numbered('Négy rendszerforma', 'Milyen szerkezetű megoldás jöhet szóba?',
                     'Nem terméknevekkel dolgozunk, hanem rendszerarchitektúrával: milyen '
                     'felépítésű megoldás illik a létesítményhez. A konkrét berendezés '
                     'ebből következik, nem fordítva.',
                     ['<strong>Moduláris — több standard egység összekapcsolva.</strong> '
                      'Fokozatos kapacitásépítés, leválasztható egységek. Saját példánk a '
                      'Bakonypéterd-projekt: négy darab 50 fős berendezésből kialakított '
                      'központi telep.',
                      '<strong>Célzott nagy kapacitású tartályos telep.</strong> Kör '
                      'keresztmetszetű, nagyobb kapacitásra gyártott rendszer, egységes '
                      'technológiai és vezérlési felépítéssel.',
                      '<strong>Konténeres kialakítás.</strong> Ahol a telepítési '
                      'körülmények vagy az áthelyezhetőség ezt indokolja.',
                      '<strong>Egyedi mérnöki technológia.</strong> Speciális, nem '
                      'kommunális szennyvíznél. Itt a fő kérdés már nem a tartályforma, '
                      'hanem hogy milyen előkezelés vagy technológiai módosítás kell a '
                      'biológiai fokozat elé.']),

        hiany('a rendszerformák valós műszaki szabályai: a moduláris rendszerek '
              'összekapcsolási feltételei, a minimális és maximális egységszám, a '
              'vezérlési architektúra, a tartályos és konténeres termékváltozatok, '
              'valamint a standard és egyedi megoldások közötti határ',
              'ÖkoTech műszaki csapat. A fenti tagolás addig általános szakmai logika; '
              'ÖkoTech-specifikus előnyként vagy korlátként csak belső szabály alapján '
              'publikálható'),

        sec_situations('A szakasz oldalai', 'Hol tart a projektben?',
                       'A sorrend a projekt logikáját követi: kategória, terhelés, '
                       'technológia, majd az üzemeltetés és az engedélyezés.',
                       [
                           ('nav-terheles', 'Kapacitási és projektkategóriák',
                            'A jogi, a műszaki és a kereskedelmi kategória nem ugyanaz. '
                            'Hol húzódnak a határok — és hol van rés.',
                            'nagyobb-kapacitasi-kategoriak', 'Kategóriák'),
                           ('nav-mukodes', 'Terhelési profil',
                            'A névleges létszámból méretezhető adatsor: átlag, csúcs, '
                            'szezonalitás, szennyvízjelleg.',
                            'nagyobb-terhelesi-profil', 'Terhelési profil'),
                           ('nav-vizminoseg', 'Előkezelés és kiegészítők',
                            'A biológiai reaktor csak egy elem. Zsírfogó, kiegyenlítés, '
                            'átemelő, tisztítottvíz-tartály — mikor melyik.',
                            'nagyobb-elokezeles-es-kiegeszitok', 'Előkezelés'),
                           ('nav-szerviz', 'Monitoring és üzemeltetés',
                            'Az átadás nem a projekt vége. Üzemnapló, mintavétel, '
                            'riasztás, szerviz — és ki a felelős üzemeltető.',
                            'nagyobb-monitoring-es-uzemeltetes', 'Üzemeltetés'),
                           ('nav-engedely', 'Engedélyezés',
                            'Az út a kapacitástól, a szennyvíz eredetétől és a '
                            'befogadótól függ. Nincs egyetlen lépéssor.',
                            'nagyobb-engedelyezes', 'Engedélyezés'),
                           ('nav-kozossegi', 'Intézményi esettanulmányok',
                            'Működő közösségi és intézményi rendszerek — terheléssel, '
                            'monitoringgal, üzemeltetési modellel.',
                            'nagyobb-esettanulmanyok', 'Esettanulmányok'),
                           ('nav-iranytu', 'Szakmai konzultáció',
                            'Nem ajánlatkérő űrlap: strukturált projektbrief, '
                            'kategóriával, hiánylistával és napirenddel.',
                            'nagyobb-szakmai-konzultacio', 'Konzultáció'),
                       ]),

        hiany('a kapacitási határok. A jelenlegi kommunikáció ELLENTMONDÁSOS: a '
              'nagytelepi oldal címe 50 fő feletti rendszerekről szól, a törzsszöveg '
              'viszont 100 LE feletti, kb. 75–750 fős telepeket említ — miközben a '
              'lakossági ág 1–50 főig tart. Az 50–100 LE közötti sáv így nincs lefedve',
              'ÖkoTech műszaki workshop. Tisztázandó: a standard A.B.Clear felső '
              'műszaki határa · az 50–100 LE ajánlati folyamat · a moduláris rendszerek '
              'összekapcsolási szabályai · a nagytelepi termékcsalád aktuális minimum- és '
              'maximumkapacitása · és hogy LE-ben vagy m³/nap-ban kommunikálunk-e'),

        sec_prose('Amit ez a szakasz nem tesz', '', [
            'Nem ad automatikus termékjavaslatot és nem ad árat. Nagyobb rendszernél '
            'a kapacitás vagy a személyszám alapján közölt ár különösen félrevezető '
            'lenne: a projektköltséget a rendszerarchitektúra, az előkezelés, a '
            'földmunka, a vezérlés és monitoring, a vízelhelyezés, a tervezés és az '
            'üzemeltetés együtt határozza meg.',
            'És nem ígér engedélyezhetőséget. Az engedélyezési út projektfüggő, a '
            'hatósági rendszer pedig időről időre változik — ezt aktuális forrásból kell '
            'ellenőrizni, nem egy weboldalról.',
        ]),

        sec_cta('Következő lépés', 'Kezdje a kategóriával',
                ['Az első kérdés nem az, hogy melyik berendezés, hanem hogy milyen '
                 'projektről van szó. Ebből következik a tervezési szint, az '
                 'engedélyezési út és az üzemeltetési modell is.'],
                'Kapacitási és projektkategóriák', 'nagyobb-kapacitasi-kategoriak',
                alt=('Szakmai konzultáció', 'nagyobb-szakmai-konzultacio')),

        sec_faq([
            ('50 fő fölött mi változik?',
             'A 147/2010. Korm. rendelet szerinti egyedi szennyvíztisztítás kategóriája '
             '1–50 LE terhelésig terjed. E fölött a projekt más szabályozási és '
             'engedélyezési úton halad, a méretezés jogosult tervező feladata lesz, és a '
             'monitoring meg az üzemeltetési felelősség is más szinten jelenik meg.'),
            ('Több kisebb berendezés vagy egy nagy?',
             'Mindkettő létező út, és a választás projektfüggő. A moduláris kialakítás '
             'fokozatos kapacitásépítést és leválasztható egységeket tesz lehetővé; a '
             'célzott nagytelep egységesebb technológiai és vezérlési rendszerként '
             'tervezhető. Az áttekintő oldal ezt veszi végig.'),
            ('Vágóhídi vagy tejüzemi szennyvíz kezelhető?',
             'Speciális terhelések egyedi mérnöki vizsgálat alapján kezelhetők. Ez nem '
             'automatikus alkalmasság: mintavétel, laboradat és megvalósíthatósági '
             'vizsgálat előzi meg. Egy standard telep nem alkalmas automatikusan '
             'bármilyen ipari szennyvízre.'),
            ('Ki fogja üzemeltetni?',
             'Ezt az ajánlat előtt kell tisztázni, nem az átadáskor. Nagyobb rendszernél '
             'nevesített felelős üzemeltető, rendszeres ellenőrzés, üzemnapló és '
             'jellemzően mintavétel is szükséges.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 2) Kapacitási és projektkategóriák
# ===========================================================================
def epit_kategoriak():
    return [
        sec_prose('Három külön kategória', 'Amit a webhelyünk eddig összemosott', [
            'A kapacitásról három különböző dolog szokott szó lenni, és ezek nem '
            'ugyanazok: a <strong>jogszabályi kategória</strong>, az ÖkoTech '
            '<strong>termékcsaládjainak határa</strong>, és a projekt '
            '<strong>tényleges terhelése</strong>.',
            'A jogszabályi határ egyértelmű: a 147/2010. Korm. rendelet szerinti egyedi '
            'szennyvíztisztítás legfeljebb 50 lakosegyenértékig tart. Ez valódi '
            'szabályozási választóvonal — e fölött más tervezési és engedélyezési út '
            'következik.',
            'A termékhatár és a tényleges terhelés viszont nem esik egybe ezzel, és '
            'jelenleg a saját kommunikációnk sem egységes ebben. Ezt itt kimondjuk, '
            'nem elfedjük.',
        ]),

        hiany('a saját kapacitási határaink. A jelenlegi állapot: a lakossági oldal '
              '1–50 főig kommunikál A.B.Clear berendezéseket, és 50 fő felett a '
              'nagytelepi oldalra irányít; az viszont 100 LE feletti, kb. 75–750 fős '
              'kapacitást nevez meg. Az 50–100 LE közötti projektút így nem egyértelmű',
              'ÖkoTech műszaki workshop. Tisztázandó: a standard A.B.Clear tartomány · '
              'a többegységes, moduláris átmeneti tartomány · a nagytelepi termékcsalád '
              'aktuális minimuma és maximuma · az egyedi ipari projektág belépési pontja'),

        sec_numbered('A kategóriák', 'Négy sáv, négy különböző projektút',
                     'A határok pontos számai belső validáció után kerülnek ide. '
                     'A kategóriák szerkezete viszont már most használható.',
                     ['<strong>Standard egyedi tartomány.</strong> Kommunális jellegű '
                      'terhelés, katalógusmodell, szokásos kialakítás. A jogi kategória '
                      'is ez, 50 LE-ig.',
                      '<strong>Moduláris átmeneti tartomány.</strong> Több standard '
                      'egység összekapcsolása. A terhelés meghaladja az egyedi '
                      'kategóriát, de a technológia még ismert elemekből épül.',
                      '<strong>Nagytelepi termékcsalád.</strong> Célzottan nagy '
                      'kapacitásra gyártott tartályos vagy konténeres rendszer, egységes '
                      'vezérléssel.',
                      '<strong>Egyedi ipari projektág.</strong> Nem kommunális '
                      'szennyvíz. Itt a kapacitás önmagában nem kategorizál — a '
                      'technológia és a laboradat dönt.']),

        sec_split('Mi változik a határ átlépésével', 'Nem csak a méret',
                  '50 LE alatt',
                  ['A 147/2010. szerinti egyedi szennyvíztisztítás kategóriája',
                   'Katalógusmodell választható',
                   'Egyszerűbb tervezési út',
                   'A tulajdonos maga is lehet üzemeltető',
                   'Az ellenőrzési és dokumentációs kötelezettség egyszerűbb'],
                  '50 LE fölött',
                  ['Kikerül az egyedi kategóriából',
                   'Jogosult tervező méretezi',
                   'Más engedélyezési út, más dokumentáció',
                   'Nevesített felelős üzemeltető szükséges',
                   'Üzemnapló, önellenőrzés, jellemzően mintavétel is',
                   'A kibocsátási követelmények külön vizsgálandók']),

        sec_prose('A „fő” mint kommunikációs adat', 'Meddig használható', [
            'A „hány fő?” kérdés felhasználóbarát, és kommunális jellegű, ismert '
            'használatnál jó közelítés. Nem véletlenül ezzel kezdi a piac nagy része.',
            'Panziónál, intézménynél vagy üzemben viszont a férőhely és az alkalmazotti '
            'létszám <strong>különösen félrevezető</strong>: ugyanannyi „fő” egészen más '
            'vízmennyiséget és szervesanyag-terhelést jelenthet. Ott LE, m³/nap, '
            'csúcsterhelés és szükség esetén laboradat alapján kell kategorizálni.',
            'Ezért használjuk a „fő”-t belépő adatként, és kérünk mellé mást is.',
        ]),

        sec_cta('Következő lépés', 'A kategóriához terhelési adat kell',
                ['A kategorizálás bemenete a terhelési profil: átlag, csúcs, '
                 'szezonalitás és a szennyvíz eredete. Enélkül a besorolás becslés '
                 'marad.'],
                'Terhelési profil', 'nagyobb-terhelesi-profil',
                alt=('Terhelési profil', 'nagyobb-terhelesi-profil')),

        sec_faq([
            ('Hol tart pontosan az A.B.Clear termékcsalád?',
             'Erre most nem adunk pontos számot, mert a saját anyagaink nem egységesek '
             'ebben, és inkább megmondjuk, hogy rendezzük, mint hogy egy bizonytalan '
             'határt közöljünk. A konkrét projektnél a műszaki kollégáink pontos választ '
             'adnak.'),
            ('60 fős intézményhez mi tartozik?',
             'Ez pontosan az a sáv, amit rendezünk. Ilyenkor jellemzően moduláris '
             'megoldás vagy a nagytelepi ág alsó tartománya jön szóba — de a válaszhoz '
             'a tényleges terhelés kell, nem a létszám. Írja meg a vízfogyasztást és a '
             'működési profilt, és megmondjuk.'),
            ('Miért nem elég a férőhely?',
             'Mert a férőhely a maximumot mutatja, nem a terhelést. Egy húszférőhelyes '
             'panzió éves átlagban működhet nyolc vendéggel — a méretezés az átlagból '
             'és a rendszeres csúcsból indul, nem a névleges kapacitásból.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 3) Terhelési profil
# ===========================================================================
def epit_profil():
    return [
        sec_prose('Amiből méretezni lehet', 'A névleges létszám csak egy adat', [
            'Nagyobb rendszernél a névleges személyszám vagy férőhely önmagában nem '
            'elegendő. A tervezéshez a szennyvíz <strong>időbeli és minőségi terhelési '
            'profilja</strong> kell.',
            'A profil legalább ezeket tartalmazza: az átlagos napi vízmennyiséget, a '
            'maximális napi és rövidebb idejű hidraulikai csúcsot, a működési napokat, a '
            'szezonális változást és a szennyvíz eredetét.',
            'Ez nem bürokrácia. Ebből derül ki, hogy a rendszer a valós működés alatt is '
            'stabilan tud-e üzemelni — vagy csak az átlagos napokon.',
        ]),

        sec_numbered('Létesítménytípusonként más', 'Melyik adat a meghatározó?',
                     'Ugyanaz a kapacitáskommunikáció nem használható lakóépületre, '
                     'iskolára, étteremre és üzemre.',
                     ['<strong>Panzió, szálláshely.</strong> A kihasználtság és a '
                      'csúcshétvégék határozzák meg a méretezési helyzetet — nem a '
                      'férőhely.',
                      '<strong>Iskola, intézmény.</strong> A nappali terhelési ablak, a '
                      'hétvégi visszaesés és a hosszabb szünetek. Erős napi ritmus, '
                      'jelentős alulterhelési időszakokkal.',
                      '<strong>Kemping, üdülőtábor.</strong> A szezonális maximum és a '
                      'szezonon kívüli közel nulla terhelés. Szélsőséges görbe.',
                      '<strong>Étterem, nagykonyha.</strong> A konyha üzemideje és a napi '
                      'étkezésszám. Itt a szerves terhelés lehet a szűk keresztmetszet, '
                      'nem a vízmennyiség.',
                      '<strong>Üzem, telephely.</strong> A műszakok és a technológiai '
                      'vízáramok. A dolgozói létszám csak a szociális ágra vonatkozik.']),

        sec_split('Két külön terhelés', 'Külön kell mérni és külön méretezni',
                  'Hidraulikai — mennyi VÍZ érkezik',
                  ['Átlagos m³/nap',
                   'Maximális m³/nap',
                   'Órás vagy műszakos csúcs, ahol releváns',
                   'A vízóráról leolvasható, meglévő létesítménynél mért',
                   'A berendezés átfolyási kapacitása a korlát'],
                  'Szerves — mennyi ANYAGOT kell lebontani',
                  ['BOI5, KOI és lebegőanyag',
                   'Nagykonyhánál és üzemnél laborvizsgálatot igényel',
                   'Nem olvasható le a vízórán',
                   'Ugyanakkora vízmennyiség mellett is nagyon eltérhet',
                   'A biológiai fokozat méretezésének alapja']),

        sec_numbered('Adatminőség', 'Négy szint, és mind számít',
                     'Ahol nincs megbízható adat, ott ne becsüljünk — hanem jelöljük a '
                     'bizonytalanságot, és indítsunk adatgyűjtést.',
                     ['<strong>Mért.</strong> Vízóra-adat, laboreredmény, üzemnapló. '
                      'Ez terhelhető.',
                      '<strong>Dokumentált.</strong> Korábbi terv, engedély, kihasználtsági '
                      'kimutatás. Jó, de ellenőrizendő, hogy aktuális-e.',
                      '<strong>Becsült.</strong> Tulajdonosi ismeret, tapasztalat. '
                      'Előszűrésre elegendő, méretezéshez nem.',
                      '<strong>Ismeretlen.</strong> Nem hiba, hanem feladat: mérés, '
                      'mintavétel vagy szakértői adatgyűjtés következik belőle.']),

        hiany('a nagyprojektes méretezési adatlap, a panziós, iskolai, kempingi és '
              'települési fogyasztási profilok, a befolyó laboreredmények, a csúcs- és '
              'alulterhelési tesztek, a működő telepek napló- és monitoringadatai, '
              'valamint az alkalmazott tervezési biztonsági tartalék',
              'ÖkoTech műszaki csapat + működő telepek adatai. Országos vízfogyasztási '
              'benchmark csak másodlagos támpont lehet, méretezési alap nem'),

        sec_cta('Következő lépés', 'A profil után az előkezelés',
                ['Ha a terhelés összeállt, a következő kérdés az, hogy kell-e valami a '
                 'biológiai fokozat elé — zsírfogó, kiegyenlítés, átemelő.'],
                'Előkezelés és kiegészítők', 'nagyobb-elokezeles-es-kiegeszitok',
                alt=('Kapacitási és projektkategóriák', 'nagyobb-kapacitasi-kategoriak')),

        sec_faq([
            ('Nincs vízfogyasztási adatunk, még nem épült meg a létesítmény.',
             'Új létesítménynél becslés szükséges: a tervezett kapacitásból, a működési '
             'rendből és hasonló üzemek adataiból. Ilyenkor a bizonytalanságot külön '
             'jelöljük, és a tervezésbe nagyobb tartalékot kell beépíteni.'),
            ('Kell laborvizsgálat?',
             'Tisztán kommunális terhelésnél jellemzően nem előfeltétel. Nagykonyhánál, '
             'jelentős zsírterhelésnél és minden technológiai eredetű szennyvíznél '
             'viszont igen — enélkül a méretezés feltételezésen alapulna.'),
            ('Mi az a terhelési görbe?',
             'A terhelés időbeli lefutása: hogyan változik a napi vízmennyiség a hét, a '
             'hónap és az év során. Ebből látszik, mekkora a szórás az átlag körül — és '
             'éppen ez határozza meg, mekkora tartalék kell.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 4) Előkezelés és kiegészítők
# ===========================================================================
def epit_elokezeles():
    return [
        sec_prose('A reaktor csak egy elem', '', [
            'Nagyobb vagy összetettebb projektben a biológiai tisztítóegység <strong>előtt '
            'és után</strong> további műszaki elemekre lehet szükség a stabil működéshez. '
            'Ezek nem extrák, hanem sokszor a működés feltételei.',
            'Fontos viszont, hogy egyik sem automatikus kiegészítő. Mindegyiket a '
            'szennyvíz eredete, összetétele, hőmérséklete és terhelése alapján kell '
            'megítélni — projektadatból, nem sablonból.',
        ]),

        sec_numbered('Ami a biológiai fokozatot VÉDI', 'Bemeneti oldal',
                     'Ezek nélkül a biológia sérülhet, eltömődhet vagy elveszítheti a '
                     'hatásfokát.',
                     ['<strong>Mechanikai előkezelés, rács.</strong> A durvább szilárd '
                      'részek visszatartása, ahol a beérkező szennyvíz ezt indokolja.',
                      '<strong>Zsírleválasztó vagy zsírfogó.</strong> Nagy mennyiségű '
                      'konyhai szennyvíznél. A zsír a felszínen filmréteget képez és '
                      'rontja az oxigénbevitelt — de hogy szükséges-e, azt a konkrét '
                      'konyhából kell levezetni, nem általános szabályból.',
                      '<strong>Homok- vagy üledékleválasztás.</strong> Projektfüggően, '
                      'ahol a beérkező szennyvíz ezt indokolja.',
                      '<strong>Olaj- és szénhidrogén-leválasztás.</strong> Kizárólag '
                      'releváns tevékenységnél — nem általános kiegészítő.',
                      '<strong>Kiegyenlítő tér.</strong> Nagy csúcsingadozásnál. '
                      'A hirtelen érkező nagy vízmennyiséget elosztja időben, így a '
                      'biológiai fokozat egyenletesebb terhelést kap.']),

        sec_numbered('Ami a hidraulikát oldja meg', 'És ami a kimeneti oldalon áll', '',
                     ['<strong>Szennyvízátemelő.</strong> Kedvezőtlen csőszinteknél, '
                      'vagy ha több beérkező ág van különböző szinteken.',
                      '<strong>Vész- vagy tartaléktérfogat.</strong> Ahol az üzembiztonság '
                      'ezt indokolja — például ha a kiesés következménye súlyos.',
                      '<strong>Tisztítottvíz-tartály.</strong> Ha a kilépő vizet '
                      'hasznosítják, vagy ha az elhelyezés időben elosztva történik.',
                      '<strong>Utókezelés vagy fertőtlenítés.</strong> Ha a befogadó vagy '
                      'a felhasználás ezt megköveteli. Ez már kibocsátási kérdés.',
                      '<strong>Mintavételi pont.</strong> A monitoring előfeltétele — '
                      'a helyét a tervezéskor kell kijelölni, nem utólag megoldani.',
                      '<strong>Szagkezelés és szellőzés.</strong> Ahol a telepítés helye '
                      'ezt indokolja.',
                      '<strong>Automatika és riasztás.</strong> Hibajelzés, szintjelzés — '
                      'nagyobb rendszernél ez nem extra.']),

        sec_split('Minden elemnél', 'Négy lehetséges minősítés',
                  'Így minősítünk',
                  ['Szükséges — a működés feltétele',
                   'Feltételesen szükséges — adott körülmények mellett',
                   'Nem indokolt — az adott projektben nem kell',
                   'Labor vagy tervezői vizsgálat kell a döntéshez'],
                  'Amiből ez következik',
                  ['A szennyvíz eredete és összetétele',
                   'A napi és csúcsterhelés',
                   'A meglévő előkezelés, ha van',
                   'A befogadó és a kibocsátási követelmény',
                   'A telepítés helye és körülményei']),

        hiany('az ÖkoTech által kínált előkezelő és kiegészítő elemek köre: '
              'zsírfogó- és leválasztó megoldások, átemelő aknák és szivattyúk, '
              'kiegyenlítő kialakítás, tisztítottvíz-tárolók, monitoring- és '
              'mintavételi egységek, valamint az előkezelési döntési mátrix — mely '
              'bemeneti adatnál mi szükséges',
              'ÖkoTech műszaki csapat és beszállítói kínálat. Külön értékes lenne: '
              'mely meghibásodásokat okozta hiányzó előkezelés'),

        sec_cta('Következő lépés', 'És ki figyeli majd?',
                ['A mintavételi pont, a riasztás és a vezérlés már az üzemeltetés '
                 'kérdése — és azt az ajánlat előtt kell tisztázni, nem az átadáskor.'],
                'Monitoring és üzemeltetés', 'nagyobb-monitoring-es-uzemeltetes',
                alt=('Terhelési profil', 'nagyobb-terhelesi-profil')),

        sec_faq([
            ('Minden étteremhez kell zsírfogó?',
             'Nem állítjuk általánosan. A jogszabály bizonyos tevékenységek szennyvizénél '
             'előtisztítást ír elő, és a nagy konyhai zsírterhelés valóban jellemző ok — '
             'de hogy az adott üzemben szükséges-e és milyen méretben, azt a konyha '
             'működéséből és a mérési adatokból kell levezetni.'),
            ('Mi az a kiegyenlítő tér?',
             'Egy pufferként működő térfogat a biológiai fokozat előtt. Ha rövid idő '
             'alatt nagy vízmennyiség érkezik — például egy rendezvény után —, ez '
             'elosztja időben, így a biológia nem kap hirtelen sokkot.'),
            ('Utólag beépíthető egy kiegészítő?',
             'Sok esetben igen, de jellemzően drágábban és nehezebben, mint a tervezéskor. '
             'Különösen igaz ez a mintavételi pontra és a kiegyenlítő térre — ezeket '
             'érdemes az első körben megtervezni.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 5) Monitoring és üzemeltetés
# ===========================================================================
def epit_monitoring():
    return [
        sec_prose('Az átadás nem a vég', '', [
            'Nagyobb szennyvíztisztító telepnél az átadás nem a projekt vége, hanem egy '
            '<strong>szabályozott üzemeltetési folyamat kezdete</strong>. Ezt már az '
            'ajánlat előtt tisztázni kell, mert a technológia kiválasztását is '
            'befolyásolja.',
            'Meg kell nevezni a felelős üzemeltetőt, az ellenőrzések gyakoriságát, az '
            'üzemnapló tartalmát, a mintavételi és laborfeladatokat, a riasztások '
            'kezelését és a szerviz reakcióidejét.',
            'A jogszabály sem tekinti ezt opcionálisnak: a hatóság ellenőrizheti az '
            'üzemnapló vezetését, az önellenőrzési eredmények megfelelését és a '
            'kibocsátási határértékek betartását — a mintavétel és a vizsgálat részletes '
            'szabályai külön rendeletben állnak.',
        ]),

        sec_split('Ki mit csinál', 'Felelősségi megosztás',
                  'A helyszíni üzemeltető',
                  ['Napi és heti szemrevételezés',
                   'Üzemnapló vezetése',
                   'Vízhozam- és terheléskövetés',
                   'Riasztás esetén első reagálás és jelzés',
                   'A mintavételi pont hozzáférhetőségének biztosítása',
                   'Fogyóanyagok kezelése'],
                  'Az ÖkoTech és a labor',
                  ['Preventív karbantartás és időszakos átvizsgálás',
                   'Alkatrészcsere, gépészeti javítás',
                   'A vezérlés ellenőrzése és beállítása',
                   'Eszkalált hibák elhárítása',
                   'Akkreditált labor: mintavétel és vizsgálat',
                   'Az eredmények értékelése és a riport']),

        sec_numbered('A rendszeres feladatok', 'Napi, heti, havi, éves',
                     'A konkrét ütemezés projektfüggő, és az engedélyben előírtakhoz is '
                     'igazodik. A szerkezet viszont minden nagyobb telepnél hasonló.',
                     ['<strong>Napi vagy heti.</strong> Szemrevételezés, a vezérlés '
                      'állapotának ellenőrzése, üzemnapló-bejegyzés, a beérkező vízhozam '
                      'követése.',
                      '<strong>Havi.</strong> Részletesebb átnézés, a fogyóanyagok '
                      'ellenőrzése, a terhelési adatok összesítése.',
                      '<strong>Az engedélyben előírt gyakorisággal.</strong> Mintavétel '
                      'és laborvizsgálat, az eredmények összevetése a kibocsátási '
                      'követelményekkel.',
                      '<strong>Éves.</strong> Teljes átvizsgálás, preventív karbantartás, '
                      'alkatrészcserék, a dokumentáció összesítése és riport.',
                      '<strong>Eseti.</strong> Riasztás, túlterhelés, vízminőségi '
                      'eltérés — ezekre előre meghatározott eszkalációs rend kell.']),

        sec_numbered('Amit előre el kell dönteni', 'Az ajánlat előtt, nem utána', '',
                     ['Ki a nevesített felelős üzemeltető, és milyen kompetenciával',
                      'Milyen betanítást kap, és mikor',
                      'Ki helyettesíti szabadság és ünnep idején',
                      'Milyen adatokat mérnek, és milyen gyakorisággal',
                      'Ki végzi a mintavételt, és melyik labor vizsgálja',
                      'Ki értékeli az eredményt, és kinek jelent',
                      'Mi történik hiba esetén — kit hívnak, milyen határidővel',
                      'Van-e távfelügyelet, és ha igen, ki nézi',
                      'Milyen szerviz-reakcióidőt vállalunk, és milyen konstrukcióban',
                      'Hol és meddig őrzik a dokumentációt']),

        hiany('a nagytelepi üzemeltetési modell: üzemeltetési kézibook, a távfelügyeleti '
              'és riasztási funkciók, a vezérlőrendszer képességei, az üzemeltetői '
              'betanítás tartalma, a szerviz-SLA és reakcióidő, a mintavételi protokoll, '
              'a karbantartási csomagok, a tipikus hibák és elhárításuk, valamint az '
              'ügyfél és az ÖkoTech közötti felelősségi mátrix',
              'ÖkoTech szerviz és műszaki vezetés. Ez lehet az egyik legerősebb '
              'különbség a pusztán berendezést értékesítő piaci kommunikációhoz képest — '
              'de csak akkor, ha van mögötte dokumentált modell'),

        sec_cta('Következő lépés', 'Az engedély is meghatározza',
                ['A monitoring gyakoriságát és tartalmát részben az engedély írja elő. '
                 'Ezért érdemes az engedélyezési utat is korán megnézni.'],
                'Engedélyezés', 'nagyobb-engedelyezes',
                alt=('Előkezelés és kiegészítők', 'nagyobb-elokezeles-es-kiegeszitok')),

        sec_faq([
            ('Kell hozzá szakképzett üzemeltető?',
             'A követelmény projektfüggő, és az engedély is meghatározhatja. Ami biztos: '
             'nevesített felelős kell, betanítással, és a feladat nem melléktevékenység. '
             'A pontos kompetenciaszintet a konkrét projektnél egyeztetjük.'),
            ('Van távfelügyelet?',
             'A vezérlés képességeit és a távfelügyeleti lehetőséget jelenleg '
             'dokumentáljuk. A konkrét projektnél megmondjuk, mi érhető el — inkább '
             'pontosan, mint általánosságban.'),
            ('Mennyi idő alatt jön ki a szerviz?',
             'Konkrét reakcióidőt itt nem ígérünk, mert ez szerződéses kérdés, és a '
             'konstrukciótól függ. Nagyobb rendszernél viszont éppen ezt érdemes az '
             'ajánlatban rögzíteni — kérdezze meg, és megállapodunk benne.'),
            ('Mi történik, ha eltér a kibocsátási határértéktől?',
             'Ilyenkor okfeltárás következik: terhelés, előkezelés, biológia állapota, '
             'üzemeltetési eltérés. A hatósági következményeket az engedély és a '
             'jogszabály határozza meg — ezért fontos, hogy az önellenőrzés időben '
             'jelezze az eltérést.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 6) Engedélyezés
# ===========================================================================
def epit_engedelyezes():
    return [
        sec_prose('Nincs egyetlen lépéssor', '', [
            'Nagyobb és közösségi szennyvíztisztító telepnél az engedélyezési út a '
            '<strong>kapacitástól</strong>, a <strong>szennyvíz eredetétől</strong>, a '
            '<strong>befogadótól</strong>, a <strong>kibocsátás módjától</strong> és a '
            '<strong>helyszíntől</strong> függ. Ezért nem írható le egyetlen, minden '
            'projektre érvényes lépéssorral — és aki mégis ezt ígéri, az egyszerűsít.',
            'Amit ez az oldal ad: döntési térkép arról, mely projektadatok, szakági '
            'tervek és szakértők szükségesek, és hol ágazik el az út.',
        ]),

        sec_prose('Egy javítás', 'Az illetékes hatóság megnevezése elavult', [
            'A korábbi tájékoztatásunk egy már nem létező szervezeti megnevezésű '
            'felügyelőséghez irányította az érdeklődőt. Ezt nem vittük át erre az '
            'oldalra.',
            'Az illetékes vízügyi és vízvédelmi hatóság megnevezése és az eljárási rend '
            'időről időre változik. Ezért itt szándékosan <strong>nem nevezünk meg '
            'konkrét szervezetet</strong>: a projekt indításakor aktuális forrásból kell '
            'ellenőrizni, és mi is így járunk el.',
        ]),

        sec_numbered('Négy elágazás', 'A kibocsátás módja határozza meg az utat', '',
                     ['<strong>Talajba, földtani közegbe történő elhelyezés.</strong> '
                      'A talaj, a talajvíz és a területi érzékenységi besorolás a '
                      'meghatározó. A telekalkalmassági kérdések itt közvetlenül '
                      'engedélyezési kérdéssé válnak.',
                      '<strong>Felszíni befogadóba vezetés.</strong> Vízjogi engedélyt és '
                      'a kibocsátási követelmények teljesítését igényli. A befogadó '
                      'állapota és az arra megállapított követelmények döntenek.',
                      '<strong>Közcsatornába vagy közös üzemi rendszerbe.</strong> '
                      'Ahol ez egyáltalán szóba jön, a szolgáltatói feltételek és az '
                      'esetleges előtisztítási követelmény a meghatározó.',
                      '<strong>A tisztított víz további hasznosítása.</strong> Külön ág, '
                      'saját vízminőségi, monitoring- és engedélyezési feltételekkel. '
                      'Nem kezelhető a helyi elhelyezés egyszerű változataként.']),

        sec_numbered('Milyen adat és dokumentum kell', 'Az engedélyezési csomag elemei',
                     'A konkrét követelményeket az engedély és a befogadó helyzete '
                     'határozza meg. Ez a lista a jellemző elemeket mutatja.',
                     ['Projektkapacitás LE-ben és m³/nap-ban',
                      'A szennyvíz eredete és jellege, laboradattal ahol szükséges',
                      'Technológiai leírás',
                      'Terhelési adatok — átlag, csúcs, szezonalitás',
                      'Helyszínrajz és a vízáramok bemutatása',
                      'A kibocsátás vagy elhelyezés módja és helye',
                      'Monitoringterv',
                      'Üzemeltetési terv és a felelős üzemeltető',
                      'Az alkalmazott előkezelés',
                      'Jogosult tervező által készített dokumentáció']),

        hiany('a saját engedélyezési gyakorlatunk: a nagytelepi engedélyezési '
              'projektlista, a benyújtott technológiai dokumentációk, a szakági '
              'tervezőpartnerek, hogy mely dokumentumot készíti az ÖkoTech és melyiket '
              'külső tervező, a visszatérő hiánypótlások és hatósági kérdések, valamint '
              'a sikeres és meghiúsult engedélyezések tanulságai',
              'ÖkoTech projektarchívum. GYORSAN AVUL, minden publikálás előtt '
              'ellenőrizendő: a hatósági szervezetrendszer, az eljárási rend, a '
              'formanyomtatványok, a jogszabályok és a monitoringkövetelmények'),

        sec_prose('A régi engedélypéldákról', 'Miért nem útmutatók', [
            'Vannak korábbi projektjeinkhez tartozó engedélydokumentumaink. Ezek '
            'hasznosak lehetnek példaként — megmutatják, milyen adatokat tartalmazott egy '
            'ilyen eljárás —, de <strong>dátumozott esettanulmányként</strong>, nem mai '
            'eljárási útmutatóként.',
            'Egy néhány évvel ezelőtti engedély nem bizonyítja a mai automatikus '
            'engedélyezhetőséget, és nem írja le a mai eljárást. Ezért ha ilyet mutatunk, '
            'mindig a dátumával és ezzel a megjegyzéssel együtt tesszük.',
        ]),

        sec_cta('Következő lépés', 'Készítsünk projektbriefet',
                ['Az engedélyezési készültséghez ugyanazok az adatok kellenek, mint a '
                 'műszaki tervezéshez. A szakmai konzultáció oldal ezeket gyűjti össze '
                 'strukturáltan.'],
                'Szakmai konzultáció', 'nagyobb-szakmai-konzultacio',
                alt=('Monitoring és üzemeltetés', 'nagyobb-monitoring-es-uzemeltetes')),

        sec_faq([
            ('Vállalják az engedélyezést?',
             'Azt, hogy pontosan mit vállalunk az engedélyezésből és mit készít külső '
             'jogosult tervező, projektfüggően egyeztetjük — és ezt a belső '
             'felelősségi rendet éppen most rögzítjük. Amit biztosan adunk: a '
             'technológiai leírást és a berendezés dokumentációját.'),
            ('Mennyi idő az engedélyezés?',
             'Erre nem adunk általános választ, mert az eljárás típusától, a befogadótól '
             'és a hatóság ügyintézésétől függ. Amit érdemes tudni: a hiánypótlás a '
             'leggyakoribb időveszteség, és ez jórészt az előkészítés minőségén múlik.'),
            ('Melyik hatósághoz kell fordulni?',
             'Szándékosan nem nevezünk meg konkrét szervezetet, mert a hatósági rendszer '
             'időről időre változik — a korábbi szövegünk éppen emiatt lett elavult. '
             'A projekt indításakor ezt aktuális forrásból ellenőrizzük.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 7) Intézményi esettanulmányok
# ===========================================================================
def epit_esettanulmanyok():
    return [
        sec_prose('Mit keresünk egy nagyprojektes referenciában', '', [
            'Ez az oldal kizárólag intézményi, közösségi vagy nagyobb kapacitású '
            'rendszereket mutat — nem keveredik össze a családi házas referenciákkal, '
            'mert azok más kérdésre válaszolnak.',
            'A telepítési fotón túl az számít, hogy a projekt <strong>hogyan jutott el '
            'az adatoktól a működő telepig</strong>: milyen terhelésre tervezték, mi lett '
            'a valós működési profil, hogyan oldották meg a vízelhelyezést, mi került a '
            'biológiai fokozat elé, és ki üzemelteti.',
        ]),

        sec_situations('Működő projektek', 'Közösségi és nagyobb rendszerek',
                       'Dokumentált projektjeink, amelyek a nagyobb léptékű '
                       'alkalmazhatóságot mutatják.',
                       [
                           ('nav-kozossegi', 'Bakonypéterd — központi telep',
                            'Négy darab 50 fős berendezés összekapcsolásával kialakított '
                            'központi tisztítótelep, saját tervezéssel. A moduláris '
                            'megközelítés élő példája.',
                            '../eredmenyek/bakonypeterd', 'Bakonypéterd'),
                           ('nav-kozossegi', 'Csikvánd — 128 berendezés',
                            'Egész községet lefedő, egyedi berendezésekre épülő '
                            'megoldás. Más architektúra ugyanarra a léptékre.',
                            '../eredmenyek/csikvand', 'Csikvánd'),
                           ('nav-kozossegi', 'Diósberény — 90 berendezés',
                            'Hasonló léptékű települési projekt, évek óta üzemelő '
                            'rendszerekkel.',
                            '../eredmenyek/diosbereny', 'Diósberény'),
                           ('nav-esettanulmany', 'Óbudavár — a kezdet',
                            'A legkorábbi dokumentált projektek egyike. A hosszú '
                            'működési idő önmagában is bizonyíték.',
                            '../eredmenyek/obudavar', 'Óbudavár'),
                       ]),

        sec_numbered('Amit egy nagyprojektes esetlapnak tartalmaznia kell',
                     'A döntéshez szükséges adatok', '',
                     ['Projekt- és létesítménytípus, helyszín, telepítés éve',
                      'Tervezési LE és m³/nap',
                      'A valós átlag- és csúcsterhelés a működés során',
                      'A szennyvíz eredete',
                      'A rendszerarchitektúra és a berendezések száma',
                      'Az alkalmazott előkezelés és kiegészítők',
                      'A befogadó vagy a vízelhelyezés módja',
                      'Az engedélyezési út és annak tanulságai',
                      'Kivitelezési sajátosság',
                      'A monitoring rendje és az üzemeltető',
                      'Laboreredmény, ahol publikálható',
                      'Szerviz- és karbantartási tapasztalat',
                      'Bővítés, ha volt',
                      'Mit bizonyít a referencia — és mit nem']),

        hiany('a strukturált nagyprojektes esetlapok adattartalma: CRM- és projektlista, '
              'szerződések és műszaki specifikációk, tervezési dokumentáció, engedélyek, '
              'telepítési és üzembe helyezési jegyzőkönyvek, üzemnaplók, laboreredmények, '
              'szerviztörténet, fotók, valamint az ügyfél- és fenntartói hozzájárulások',
              'ÖkoTech projektarchívum. Ez az oldal döntően saját projektadatból épülhet '
              'fel — a lakossági telepítésszám itt nem elég erős bizonyíték'),

        sec_prose('Az ipari állításokról', 'Amit csak referenciával mondunk ki', [
            'A korábbi tájékoztatásunk vágóhídi, tejüzemi és borászati szennyvíz '
            'biológiai tisztítását is vállalhatóként említette. Ez üzletileg értékes '
            'állítás — de csak akkor erős, ha bemutatható hozzá konkrét projekt, '
            'bemeneti szennyvízjellemző, előkezelés, alkalmazott technológia, '
            'kibocsátási követelmény, laboreredmény és működési időtáv.',
            'Amíg ezek nincsenek együtt, a helyes megfogalmazás: <em>speciális '
            'terhelések egyedi mérnöki vizsgálat és tervezés alapján kezelhetők</em>. '
            'Ez nem gyengébb állítás, csak pontosabb — és nem kelti azt a benyomást, '
            'hogy egy standard telep automatikusan alkalmas bármilyen ipari szennyvízre.',
        ]),

        sec_cta('Következő lépés', 'Keressünk hasonlót',
                ['Írja meg, milyen létesítményről és milyen nagyságrendről van szó, és '
                 'megnézzük, van-e dokumentált, összevethető projektünk. Ha nincs, azt '
                 'is megmondjuk.'],
                'Szakmai konzultáció', 'nagyobb-szakmai-konzultacio',
                alt=('Bakonypéterd — központi telep', '../eredmenyek/bakonypeterd')),

        sec_faq([
            ('Meglátogatható egy működő telep?',
             'Az üzemeltető hozzájárulásán múlik, de intézményi és települési '
             'projekteknél több esetben megoldható. Kérdezze meg — egy működő telep '
             'megnézése többet mond, mint bármelyik dokumentum.'),
            ('Van iparági referenciájuk?',
             'Írja meg, melyik iparágról van szó, és megnézzük, van-e összevethető '
             'projektünk laboreredménnyel együtt. Ha nincs, azt megmondjuk — és akkor a '
             'projekt megvalósíthatósági vizsgálattal indul, nem referenciával.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 8) Szakmai konzultáció
# ===========================================================================
def epit_konzultacio():
    return [
        sec_prose('Nem ajánlatkérő űrlap', '', [
            'Ez az oldal a nagyobb projekt előzetes szakmai minősítésének lezárása, nem '
            'egy név–telefon–üzenet mező. A cél az, hogy a konzultáció előtt '
            '<strong>mindkét fél</strong> rendelkezzen a szükséges alapadatokkal.',
            'Így a szakértőnk nem egy „200 fős szállodához kérek árat” típusú nyers '
            'megkeresést kap, hanem strukturált döntési helyzetet — és Ön sem azt hallja '
            'vissza, hogy „ehhez több adat kell”.',
        ]),

        sec_numbered('Amit a brief rögzít', 'Öt adatcsoport', '',
                     ['<strong>Projektazonosítás.</strong> Létesítménytípus, projektgazda '
                      'vagy fenntartó, helyszín, projektfázis, tervezett üzembe helyezés, '
                      'új vagy meglévő rendszer.',
                      '<strong>Terhelés.</strong> Névleges létszám vagy férőhely, '
                      'átlagos napi létszám, csúcslétszám, m³/nap átlag és maximum, '
                      'működési napok, szezonális görbe, műszakok, bővítési terv.',
                      '<strong>A szennyvíz jellege.</strong> Tisztán kommunális, '
                      'nagykonyhai, technológiai vagy vegyes; meglévő laboreredmény; '
                      'meglévő előkezelés.',
                      '<strong>Telek és kibocsátás.</strong> Rendelkezésre álló terület, '
                      'csőszintek, talaj és talajvíz, befogadó, vízelhelyezés, meglévő '
                      'hálózat.',
                      '<strong>Projektkészültség és üzemeltetés.</strong> Meglévő tervek, '
                      'engedélyezési állapot, monitoringigény, a felelős üzemeltető, '
                      'karbantartási modell, szervizelvárás, beszerzési folyamat.']),

        sec_split('Mit ad vissza', 'A brief kimenete',
                  'Ezt kapja',
                  ['Projektkategória — melyik ágra esik',
                   'Adatkomplettség: mi van meg, mi hiányzik',
                   'A szükséges vizsgálatok listája',
                   'Melyik szakértő bevonása indokolt',
                   'Konzultációs napirend',
                   'A következő felelős és lépés'],
                  'Ezt nem kapja',
                  ['Automatikus konkrét árat',
                   'Ársávot tisztázatlan projektterjedelemre',
                   'Garantált kapacitást hiányos adatokból',
                   'Automatikus ipari méretezést laboradat nélkül',
                   'Engedélyezhetőségi ígéretet',
                   'Végleges termékmodellt']),

        sec_numbered('A lehetséges kimenetek', 'Öt eredmény, öt út', '',
                     ['<strong>Standard kommunális projekt.</strong> Az adatok elegendők, '
                      'a terhelés kommunális jellegű. A tervezés folytatható.',
                      '<strong>Moduláris közösségi rendszer.</strong> A terhelés '
                      'meghaladja az egyedi kategóriát, de ismert elemekből építhető.',
                      '<strong>Nagytelepi tervezés.</strong> Célzott nagy kapacitású '
                      'rendszer, jogosult tervezővel.',
                      '<strong>Speciális vagy ipari vizsgálat.</strong> Nem kommunális '
                      'szennyvíz. Mintavétel és megvalósíthatósági vizsgálat következik, '
                      'nem kapacitásbecslés.',
                      '<strong>További adatgyűjtés szükséges.</strong> Nem a projekt a '
                      'korlát, hanem az információ. A brief megmondja, melyik adat és '
                      'honnan.']),

        sec_prose('Amit érdemes csatolni', '', [
            'Ha van, csatolja: helyszínrajzot, gépészeti tervet, fogyasztási adatsort, '
            'korábbi tervet vagy engedélyt, laboreredményt, és — ha már van — meglévő '
            'ajánlatot.',
            'Ezekkel lényegesen gyorsabban jutunk műszaki irányig, és a konzultáción '
            'már a döntésekről lehet beszélni, nem az adatok összegyűjtéséről.',
            'Az adatkezelésről a kapcsolatfelvételi oldalon tájékoztatunk; a csatolt '
            'dokumentumokat kizárólag a megkeresés megválaszolására használjuk.',
        ]),

        hiany('a konzultációs folyamat belső rendje: milyen mezőket kér ma a '
              'nagyprojektes értékesítő, milyen adatot kér vissza rendszeresen, milyen '
              'dokumentum kell indikatív és milyen végleges műszaki ajánlathoz, ki vesz '
              'részt a konzultáción, mikor kell külső tervező vagy labor, mikor kötelező '
              'a helyszíni felmérés, és milyen a válaszadási folyamat',
              'ÖkoTech értékesítés és műszaki vezetés — közös workshop. A modul addig a '
              'brief SZERKEZETÉT írja le; az űrlap élesítése ezután következik'),

        sec_cta('Addig is', 'Vegyük végig együtt',
                ['Amíg a strukturált brief nem üzemel, ugyanezt élőben végigvesszük. '
                 'Írja meg a létesítmény típusát, a nagyságrendet, a működési profilt és '
                 'azt, hol tart a projekt — a többit megkérdezzük.'],
                'Kapcsolatfelvétel', '../kapcsolat',
                alt=('Intézményi esettanulmányok', 'nagyobb-esettanulmanyok')),

        sec_faq([
            ('Miért nem kapok azonnal árat?',
             'Mert nagyobb rendszernél a kapacitás vagy a személyszám alapján közölt ár '
             'félrevezető lenne. A projektköltséget a rendszerarchitektúra, az '
             'előkezelés, a földmunka, a vezérlés, a vízelhelyezés, a tervezés és az '
             'üzemeltetés együtt határozza meg. Tisztázott projektterjedelemnél viszont '
             'adható ársáv.'),
            ('Mennyi adat kell a konzultációhoz?',
             'A beszéléshez elég a létesítmény típusa és a nagyságrend. Ahhoz, hogy '
             'műszaki irányt tudjunk mondani, kell a terhelési profil és a szennyvíz '
             'jellege. Ajánlathoz ezeken felül a telek, a befogadó és az üzemeltetési '
             'modell is.'),
            ('Ki vesz részt a konzultáción?',
             'A projekt jellegétől függ. Standard kommunális projektnél műszaki '
             'kollégánk; nagyobb vagy speciális projektnél tervező, esetenként külső '
             'szakértő is. A brief eredménye éppen ezt is megmondja.'),
        ]),
        JOGI,
    ]


# ===========================================================================
OLDALAK = [
    dict(file='megoldasok/nagyobb-es-kozossegi-rendszerek.html',
         url='megoldasok/nagyobb-es-kozossegi-rendszerek', img='telepek',
         title='Nagyobb és közösségi rendszerek — projektkategóriák | ÖkoTech Home',
         desc='Panzió, intézmény, kemping, üzem, településrész. Miért önálló '
              'projektkategória, és hogyan kell kategorizálni a terhelés alapján.',
         h1='Nagyobb és közösségi rendszerek',
         alt='Nagyobb kapacitású szennyvíztisztító telep tartályai egy telephelyen',
         lead='Nem egy családi berendezés nagyobb változata. Terhelési, technológiai, '
              'üzemeltetési és engedélyezési szempontból önálló projektkategória — '
              'más tervezési úttal.',
         crumbs=CRUMB, sections=epit_hub()),

    dict(file='megoldasok/nagyobb-kapacitasi-kategoriak.html',
         url='megoldasok/nagyobb-kapacitasi-kategoriak', img='vallalkozas',
         title='Kapacitási és projektkategóriák — hol húzódnak a határok | ÖkoTech Home',
         desc='A jogi, a műszaki és a kereskedelmi kategória nem ugyanaz. Az 50 LE-s '
              'határ, és ami fölötte változik.',
         h1='Kapacitási és projektkategóriák',
         alt='Műszaki dokumentumok és kapacitástáblázatok egy tárgyalóasztalon',
         lead='Három különböző dolgot szoktak összemosni: a jogszabályi kategóriát, a '
              'termékcsalád határát és a projekt tényleges terhelését.',
         crumbs=HUB, sections=epit_kategoriak()),

    dict(file='megoldasok/nagyobb-terhelesi-profil.html',
         url='megoldasok/nagyobb-terhelesi-profil', img='biologiai',
         title='Terhelési profil — nagyobb és közösségi rendszerek | ÖkoTech Home',
         desc='Átlag, csúcs, szezonalitás és a szennyvíz eredete. Létesítménytípusonként '
              'más adat a meghatározó.',
         h1='Terhelési profil',
         alt='Vízhozammérő és adatrögzítő egység egy gépészeti helyiségben',
         lead='A névleges létszám csak egy adat. A tervezéshez a szennyvíz időbeli és '
              'minőségi terhelési profilja kell — és az létesítménytípusonként más.',
         crumbs=HUB, sections=epit_profil()),

    dict(file='megoldasok/nagyobb-elokezeles-es-kiegeszitok.html',
         url='megoldasok/nagyobb-elokezeles-es-kiegeszitok', img='alternativak',
         title='Előkezelés és kiegészítők — nagyobb rendszerek | ÖkoTech Home',
         desc='Zsírfogó, kiegyenlítés, átemelő, tisztítottvíz-tartály, mintavételi pont — '
              'mikor melyik, és milyen bemeneti adatból következik.',
         h1='Előkezelés és kiegészítők',
         alt='Gépészeti előkezelő egységek egy tisztítótelep bejáratánál',
         lead='A biológiai reaktor csak a teljes rendszer egyik eleme. Ami elé és mögé '
              'kerül, sokszor a stabil működés feltétele — de egyik sem automatikus.',
         crumbs=HUB, sections=epit_elokezeles()),

    dict(file='megoldasok/nagyobb-monitoring-es-uzemeltetes.html',
         url='megoldasok/nagyobb-monitoring-es-uzemeltetes', img='mar-van-rendszerem',
         title='Monitoring és üzemeltetés — nagyobb rendszerek | ÖkoTech Home',
         desc='Üzemnapló, mintavétel, riasztás, szerviz — és ki a nevesített felelős '
              'üzemeltető. Az ajánlat előtt tisztázandó, nem az átadáskor.',
         h1='Monitoring és üzemeltetés',
         alt='Vezérlőszekrény és kijelző egy szennyvíztisztító telep gépházában',
         lead='Az átadás nem a projekt vége, hanem egy szabályozott üzemeltetési '
              'folyamat kezdete. És ezt már a technológiaválasztásnál tudni kell.',
         crumbs=HUB, sections=epit_monitoring()),

    dict(file='megoldasok/nagyobb-engedelyezes.html',
         url='megoldasok/nagyobb-engedelyezes', img='kozcsatorna',
         title='Engedélyezés — nagyobb és közösségi rendszerek | ÖkoTech Home',
         desc='Az út a kapacitástól, a szennyvíz eredetétől és a befogadótól függ. '
              'Nincs egyetlen lépéssor — de van döntési térkép.',
         h1='Engedélyezés',
         alt='Engedélyezési tervdokumentáció és helyszínrajz egy asztalon',
         lead='Négy elágazás a kibocsátás módja szerint, és egy dolog, amit nem '
              'ígérünk: hogy a weboldalról megtudja, melyik hatósághoz kell fordulnia.',
         crumbs=HUB, sections=epit_engedelyezes()),

    dict(file='megoldasok/nagyobb-esettanulmanyok.html',
         url='megoldasok/nagyobb-esettanulmanyok', img='bakonypeterd',
         title='Intézményi esettanulmányok — nagyobb rendszerek | ÖkoTech Home',
         desc='Működő közösségi és intézményi rendszerek terheléssel, monitoringgal és '
              'üzemeltetési modellel — nem galéria.',
         h1='Intézményi esettanulmányok',
         alt='Községi szennyvíztisztító telep madártávlatból, körülötte mezőgazdasági '
             'terület',
         lead='A telepítési fotón túl az számít, hogyan jutott el a projekt az adatoktól '
              'a működő telepig — és ki üzemelteti azóta.',
         crumbs=HUB, sections=epit_esettanulmanyok()),

    dict(file='megoldasok/nagyobb-szakmai-konzultacio.html',
         url='megoldasok/nagyobb-szakmai-konzultacio', img='kapcsolat',
         title='Szakmai konzultáció — nagyobb projektekhez | ÖkoTech Home',
         desc='Strukturált projektbrief: kategória, adatkomplettség, hiánylista, '
              'szükséges vizsgálatok és konzultációs napirend. Nem ajánlatkérő űrlap.',
         h1='Szakmai konzultáció',
         alt='Tárgyalás közben: műszaki rajzok, laptop és jegyzetek az asztalon',
         lead='A cél az, hogy a konzultáció előtt mindkét fél rendelkezzen a szükséges '
              'alapadatokkal — így a beszélgetés a döntésekről szól, nem az '
              'adatgyűjtésről.',
         crumbs=HUB, sections=epit_konzultacio()),
]

if __name__ == '__main__':
    for o in OLDALAK:
        out = WEB / o['file']
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:56s} {len(out.read_text(encoding='utf-8'))//1024} KB")
