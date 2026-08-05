#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helyzetem kategória — oldaltartalom.

A szekciók a sitemap 3. szintjét követik; a szerkezet a skill „Helyzet-oldal"
sablonja. Szám, ár és műszaki érték nincs benne — azok gyártói adatlapból
jönnek, addig ADATHIÁNY-jelölést kap a hely.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sablon import (build, sec_numbered, sec_split, sec_prose,
                           sec_situations, sec_cta, sec_faq)

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'
HOME = ('Főoldal', '../')
HELY = ('Helyzetem', './')
HELY_UP = ('Helyzetem', '../helyzetem/')

PAGES = []

# ===========================================================================
# 1) Áttekintő
# ===========================================================================
PAGES.append(dict(
    file='helyzetem/index.html', url='helyzetem/', img='helyzetem',
    title='Miben keres megoldást? — helyzetek és belépési pontok | ÖkoTech Home',
    desc='Hét tipikus ingatlanhelyzet, és hogy melyikben mit kell először tisztázni: csatorna nélküli telek, új építés, emésztő kiváltása, nyaraló, családi ház, vállalkozás, meglévő rendszer.',
    h1='Miben keres megoldást?',
    alt='Magyar falu széle naplementében: különböző korú családi házak földút mentén, az egyik gyepben tisztítóakna fedlapja',
    lead='A szennyvízkezelés kérdése ritkán önmagában érkezik — mindig egy konkrét élethelyzethez kapcsolódik. Alább hét tipikus helyzet szerepel. Válassza ki azt, amelyik a legközelebb áll az Önéhez: mindegyiknél azzal kezdünk, mit kell először tisztázni, és csak utána jön a megoldás.',
    crumbs=[HOME],
    sections=[
        sec_situations(
            'Helyzetek', 'Melyik áll a legközelebb az Ön helyzetéhez?',
            'A helyzetek átfedhetik egymást. Ha kettő is illik Önre, kezdje azzal, amelyik időben előbb van — a telek kérdései például megelőzik a berendezés kiválasztását.',
            [
                ('nav-kozcsatorna', 'Nincs elérhető közcsatorna',
                 'Az ingatlan nem köthető rá a közműhálózatra, és nem világos, milyen megoldások jöhetnek egyáltalán szóba.',
                 'nincs-elerheto-kozcsatorna', 'Nincs közcsatorna'),
                ('telek', 'Telekvásárlás vagy új építés előtt állok',
                 'A szennyvízkezelés a telek alkalmasságán múlik. Ezt vásárlás vagy tervezés előtt érdemes tisztázni, nem utána.',
                 'telekvasarlas-vagy-uj-epites-elott-allok', 'Telek és új építés'),
                ('emeszto', 'Meglévő emésztőt szeretnék kiváltani',
                 'A szippantási költség nő, vagy a rendszer nem felel meg. A csere csak akkor indokolt, ha a felmérés is ezt támasztja alá.',
                 'meglevo-emesztot-szeretnek-kivaltani', 'Emésztő kiváltása'),
                ('nyaralo', 'Nyaraló vagy szezonálisan használt ingatlan',
                 'A hosszú távollét más követelményt támaszt, mint az állandó lakhatás. Nem minden technológia bírja jól.',
                 'nyaralo-vagy-szezonalisan-hasznalt-ingatlan', 'Nyaraló, szezonális'),
                ('epitkezes', 'Családi házhoz keresek rendszert',
                 'Adott a ház és a háztartás létszáma; a kérdés a megoldástípus, a kapacitás és a telepíthetőség.',
                 'csaladi-hazhoz-keresek-rendszert', 'Családi ház'),
                ('nav-vallalkozas', 'Vállalkozás vagy intézmény számára keresek megoldást',
                 'Panzió, étterem, iskola, kemping vagy üzem: itt a csúcsterhelés és a szennyvíz összetétele dönt, nem a létszám önmagában.',
                 'vallalkozas-vagy-intezmeny-szamara-keresek-megoldast', 'Vállalkozás, intézmény'),
                ('nav-szerviz', 'Már van rendszerem, segítségre van szükségem',
                 'Üzemeltetési kérdés, hibajelenség, alkatrész vagy szerviz: ezek az Ügyféltámogatás területére tartoznak.',
                 'mar-van-rendszerem-segitsegre-van-szuksegem', 'Már van rendszerem'),
            ]),
        sec_numbered(
            'Közös vonás', 'Ami mind a hét helyzetben ugyanaz',
            'Bármelyik ágon indul el, ugyanaz a négy kérdés dönti el, mi valósítható meg. Ezért kérjük ugyanazokat az adatokat minden esetben.',
            ['<strong>Mennyi szennyvíz keletkezik és milyen ütemben.</strong> Nem a ház mérete számít, hanem a tényleges terhelés és annak ingadozása — az állandó és az időszakos használat két különböző feladat.',
             '<strong>Hová kerül a kezelt víz.</strong> Ez a legtöbb projektben a szűk keresztmetszet: talajba szikkasztás, felszíni befogadó vagy öntözési hasznosítás — mindegyiknek más a feltétele.',
             '<strong>Mit enged a telek.</strong> Talajszerkezet, talajvízszint, lejtés, beépítettség, meglévő közművek és a szomszédos kutak helyzete együtt szűkíti a lehetőségeket.',
             '<strong>Milyen engedélyezési feltételek vonatkoznak a területre.</strong> Ez településenként eltér, és felülírhat minden más szempontot — például vízbázisvédelmi területen.']),
        sec_cta('Nem találja a sajátját', 'Ha egyik helyzet sem illik pontosan',
                ['Az eddigi projektekben visszatérő élethelyzeteket gyűjtöttük össze, de a felsorolás nem teljes. Az összetettebb esetekhez — több épület, vegyes használat, meglévő és új rendszer együtt — nincs sablon, ezekhez felmérés kell.',
                 'Írja le a helyzetét néhány mondatban, és megmondjuk, melyik irány jöhet szóba — akkor is, ha a válasz az, hogy nem a mi rendszerünk a megoldás.'],
                'Kapcsolatfelvétel', '../kapcsolat'),
        sec_faq([
            ('Melyik helyzettel kezdjem, ha több is illik rám?',
             'Azzal, amelyik időben előbb van. A telek alkalmassága például megelőzi a berendezés kiválasztását: ha a telek nem enged talajba jutást, a megoldástípusok fele eleve kiesik.'),
            ('Muszáj minden adatot előre összeszednem?',
             'Nem. A tájékozódáshoz elég a település neve, az ingatlan használati módja és a háztartás létszáma. A részletes adatokra csak a méretezésnél és az ajánlatnál lesz szükség.'),
            ('Meg tudják mondani előre, mennyibe fog kerülni?',
             'Nagyságrendet igen, végleges árat nem. A végösszeget a telepítési körülmények mozgatják leginkább — a földmunka, a bekötés mélysége és a kezelt víz elhelyezésének módja. Ezeket helyszíni felmérés nélkül nem lehet felelősen megmondani.'),
        ]),
    ]))

# ===========================================================================
# 2) Nincs elérhető közcsatorna
# ===========================================================================
PAGES.append(dict(
    file='helyzetem/nincs-elerheto-kozcsatorna.html',
    url='helyzetem/nincs-elerheto-kozcsatorna', img='kozcsatorna',
    title='Nincs elérhető közcsatorna — milyen megoldások jöhetnek szóba | ÖkoTech Home',
    desc='Ha az ingatlan nem köthető rá a közcsatornára: milyen megoldási lehetőségek vannak, mikor érdemes kivárni a hálózat kiépítését, és milyen adatokat kell először összegyűjteni.',
    h1='Nincs elérhető közcsatorna',
    alt='Magyar falusi utca, ahol az aszfalt és az utolsó csatornaakna véget ér, tovább földút és bekötés nélküli családi házak',
    lead='Magyarországon a lakott ingatlanok egy részénél nincs és belátható időn belül nem is lesz közcsatorna. Ilyenkor a szennyvizet a telken belül kell megoldani — de nem mindegy, hogyan. Ez az oldal végigveszi, mely megoldások jöhetnek szóba, melyik mikor esik ki, és mit kell hozzá tisztázni.',
    crumbs=[HOME, HELY],
    sections=[
        sec_numbered(
            'Lehetőségek', 'Milyen megoldási lehetőségek vannak?',
            'Négy irány létezik. A választást nem az ár dönti el elsőként, hanem az, hogy hová kerülhet a kezelt víz, és mit enged a helyi szabályozás.',
            ['<strong>Biológiai szennyvíztisztító berendezés.</strong> A szennyvizet a telken belül megtisztítja, a kezelt víz szikkasztható vagy — a feltételek teljesülése esetén — hasznosítható. Állandó lakhatásnál ez a leggyakoribb megoldás. Áram kell hozzá, és rendszeres, de kis munkaigényű üzemeltetést igényel.',
             '<strong>Oldómedencés rendszer szikkasztással.</strong> Egyszerűbb, áramigény nélküli megoldás. Csak ott működik, ahol a talaj vízáteresztő képessége megfelelő és a talajvízszint elég mély — és a szikkasztómező területigénye is jelentős.',
             '<strong>Zárt szennyvíztároló.</strong> Nem kezel, csak gyűjt: a szennyvizet rendszeresen el kell szállíttatni. Ott van a helye, ahol a helyi adottságok semmilyen talajba jutást nem engednek. <strong>Ezt a megoldást nem mi gyártjuk</strong>, de megmondjuk, ha ez a helyzet.',
             '<strong>A közcsatorna kivárása.</strong> Ha az önkormányzatnak konkrét, ütemezett fejlesztési terve van, és a bekötés belátható időn belül elérhető, érdemes lehet átmeneti megoldással kivárni. Ígéret és ütemterv azonban nem ugyanaz.']),
        sec_split(
            'Összevetés', 'Közcsatorna vagy egyedi rendszer?',
            'Az egyedi rendszer felé billen, ha…',
            ['<strong>nincs konkrét fejlesztési ütemterv</strong> — az önkormányzat nem tud kötelező érvényű időpontot mondani;',
             '<strong>a bekötési pont messze van</strong>, és a telken belüli vezetékszakasz költsége önmagában jelentős;',
             '<strong>a telek alkalmas</strong> a kezelt víz elhelyezésére, tehát a rendszer a telken belül lezárható;',
             '<strong>hosszú távra tervez</strong>: a rendszer élettartama alatt a szolgáltatási díj is elmarad.'],
            'A közcsatorna felé billen, ha…',
            ['<strong>a hálózat épül, és a bekötés dátuma ismert</strong> — ilyenkor egy párhuzamos beruházás nehezen indokolható;',
             '<strong>a telek nem enged talajba jutást</strong>, és a kezelt víznek nincs más elhelyezési módja;',
             '<strong>a telekhatár közvetlen közelében van a gerincvezeték</strong>, tehát a bekötés műszakilag egyszerű;',
             '<strong>az ingatlant rövid távon értékesítenék</strong> — ott a közműrákötés önmagában is érték.']),
        sec_numbered(
            'Előkészítés', 'Milyen adatokat kell először összegyűjteni?',
            'Ezekkel a válaszokkal már meg tudjuk mondani, mely megoldások jönnek szóba, és melyik esik ki — mindezt helyszíni kiszállás előtt.',
            ['<strong>Az ingatlan pontos helye és a helyi szabályozás.</strong> A település neve és a helyrajzi szám elég ahhoz, hogy kiderüljön, vonatkozik-e a területre vízbázisvédelmi vagy más korlátozás.',
             '<strong>A használat módja és a létszám.</strong> Állandó lakhatás vagy időszakos használat, hány fő, és van-e a terhelésben kiszámítható csúcs (például hétvégi vendégek).',
             '<strong>A telek adottságai.</strong> Terület, lejtésviszonyok, a beépített rész elhelyezkedése, és hogy hol van szabad, gépjárművel megközelíthető felület a berendezésnek.',
             '<strong>Talaj és talajvíz.</strong> Ha van korábbi talajmechanikai szakvélemény vagy fúrt kút adatlapja, az sokat segít. Ha nincs, a szomszédos ingatlanok tapasztalata is támpont.',
             '<strong>A kezelt víz tervezett sorsa.</strong> Van-e a közelben felszíni befogadó (árok, patak), tervez-e öntözési hasznosítást, és hol vannak a környező ásott vagy fúrt kutak.']),
        sec_numbered(
            'Buktatók', 'Tipikus hibák ebben a helyzetben', None,
            ['<strong>A berendezés kiválasztása a telek vizsgálata előtt.</strong> A leggyakoribb sorrendi hiba. Egy jó berendezés is működésképtelen, ha a kezelt vizet nincs hová elhelyezni.',
             '<strong>Ígéretre alapozott várakozás.</strong> „Néhány éven belül kiépül" — ütemterv és forrás nélkül ez nem tervezhető adat. Közben a szippantási költség folyamatosan fut.',
             '<strong>A szomszédos kutak figyelmen kívül hagyása.</strong> A védőtávolságok nemcsak a saját, hanem a szomszédos ingatlanok vízkivételi helyeire is vonatkoznak.',
             '<strong>Csak a beruházási költség számolása.</strong> A teljes kép az üzemeltetéssel együtt áll össze: áramfogyasztás, iszapelszállítás, karbantartás — ezek nélkül a megoldások nem hasonlíthatók össze.']),
        sec_cta('Következő lépés', 'Kezdje a helyzetfelméréssel',
                ['Ha a fenti adatok nagyjából megvannak, a döntéstámogató modul néhány kérdés alapján megmutatja, mely megoldástípusok jöhetnek szóba az Ön esetében, és melyik esik ki — nagyságrendi költségtartománnyal együtt.',
                 'Az eredmény tájékoztató jellegű: a végleges megoldást és árat helyszíni felmérés után adjuk meg.'],
                'Döntéstámogató kitöltése', '../#dontestamogato',
                alt=('Vagy nézze meg előbb a megoldástípusok összehasonlítását', '../megoldasok/')),
        sec_faq([
            ('Kötelező rákötni a közcsatornára, ha kiépül?',
             'A rákötési kötelezettség és annak határideje helyi rendelet kérdése, és településenként eltér. Ezt az illetékes önkormányzatnál vagy a szolgáltatónál érdemes tisztázni még a beruházás megkezdése előtt, mert befolyásolja a megtérülési számítást.'),
            ('Mennyi ideig tart egy egyedi rendszer telepítése?',
             'A telepítés maga rendszerint néhány nap, de a teljes átfutást az engedélyezés és a földmunka határozza meg. A reális ütemtervet a felmérés után tudjuk megadni, mert a bekötés mélysége és a talajviszonyok jelentősen befolyásolják.'),
            ('Mi történik, ha később mégis kiépül a csatorna?',
             'A telepített rendszer nem válik értéktelenné: a kezelt víz hasznosítása és az elmaradó szolgáltatási díj továbbra is előny lehet. A rákötés és a meglévő rendszer sorsa azonban helyi szabályozás kérdése, ezért ezt előre érdemes tisztázni.'),
        ]),
    ]))

# ===========================================================================
# 3) Telekvásárlás vagy új építés
# ===========================================================================
PAGES.append(dict(
    file='helyzetem/telekvasarlas-vagy-uj-epites-elott-allok.html',
    url='helyzetem/telekvasarlas-vagy-uj-epites-elott-allok', img='telekvasarlas',
    title='Telekvásárlás vagy új építés előtt — alkalmas-e a telek | ÖkoTech Home',
    desc='Mit érdemes a szennyvízkezelésről tudni telekvásárlás vagy tervezés előtt: talaj, talajvíz, vízelhelyezés, szükséges dokumentumok és telekadat-ellenőrzőlista.',
    h1='Telekvásárlás vagy új építés előtt állok',
    alt='Üres füves építési telek kitűzőcövekekkel és zsinórral, előtérben nyitott talajvizsgálati gödör a rétegekkel',
    lead='Ez az a pont, ahol a legtöbbet lehet nyerni — és a legtöbbet veszíteni. A szennyvízkezelés feltételei a telekben vannak kódolva: ha ezeket vásárlás vagy tervezés előtt tisztázza, a megoldás beépíthető a tervbe. Ha utólag derülnek ki, a korrekció mindig drágább.',
    crumbs=[HOME, HELY],
    sections=[
        sec_numbered(
            'Alkalmasság', 'Alkalmas lehet-e a telek?',
            'Öt tényező dönti el, mi valósítható meg. Egyik sem látszik a hirdetésből, de mindegyik kideríthető vásárlás előtt.',
            ['<strong>Talajszerkezet.</strong> A vízáteresztő képesség határozza meg, szikkasztható-e egyáltalán a kezelt víz, és ha igen, mekkora területen. Kötött agyagos talajon a szikkasztás nem vagy csak jelentős területigénnyel működik.',
             '<strong>Talajvízszint.</strong> A magas, illetve erősen ingadozó talajvízszint két dolgot érint: a berendezés elhelyezhetőségét és a szikkasztás lehetőségét. Az évszakos maximumot kell nézni, nem az aktuális értéket.',
             '<strong>A kezelt víz elhelyezése.</strong> Talajba szikkasztás, felszíni befogadó vagy hasznosítás — ha egyik sem áll rendelkezésre, a megoldások köre a zárt tárolóra szűkül.',
             '<strong>Védőtávolságok.</strong> Ásott és fúrt kutak, vízbázisvédelmi terület, telekhatárok és épületek: ezek együtt jelölik ki, hol helyezhető el a berendezés és a szikkasztómező.',
             '<strong>Megközelíthetőség.</strong> A telepítéshez gép kell, a későbbi iszapelszállításhoz pedig szippantóautó. Ha a berendezés helye nem megközelíthető, az az üzemeltetést drágítja évtizedeken át.']),
        sec_prose(
            'Talajvizsgálat', 'Talaj, talajvíz és vízelhelyezés',
            ['A talaj és a talajvíz nem egy technikai részletkérdés, hanem a projekt legfontosabb bemenő adata. A vízáteresztő képesség és a mértékadó talajvízszint együtt dönti el, hogy a kezelt víz elhelyezhető-e a telken belül, és ha igen, mekkora felületen.',
             'Vásárlás előtt ehhez nem kell teljes talajmechanikai szakvélemény: sokat elárul a szomszédos ingatlanok tapasztalata, a környékbeli fúrt kutak adatlapja, valamint az, hogy tavasszal áll-e meg víz a telken. A pontos méretezéshez azonban a beruházás megkezdése előtt már mérésre lesz szükség.',
             'Ha az építkezéshez amúgy is készül talajmechanikai szakvélemény, kérje meg a szakértőt, hogy a szennyvízkezelés szempontjait is vegye bele — így egy vizsgálatból két kérdésre kap választ.']),
        sec_numbered(
            'Dokumentumok', 'Milyen dokumentumokra lehet szükség?',
            'A pontos lista településenként és megoldástípusonként eltér. Az alábbiak azok, amelyek a legtöbb projektben előkerülnek — érdemes már a tervezésnél számolni velük.',
            ['<strong>Tulajdoni lap és térképmásolat.</strong> A telek jogi helyzete, terhei és pontos határai — vásárlás előtt önmagában is szükséges.',
             '<strong>Helyi építési szabályzat vonatkozó része.</strong> Beépíthetőség, közműellátottsági előírások és az esetleges helyi korlátozások.',
             '<strong>Talajmechanikai szakvélemény.</strong> Az építéshez általában készül; a szennyvízkezelés méretezéséhez a vízáteresztő képesség és a talajvízszint adatai kellenek belőle.',
             '<strong>Vízjogi engedélyezési dokumentáció.</strong> A megoldástípustól és a helyi előírásoktól függ, hogy szükséges-e, és milyen mélységben. Ezt a felmérés után tudjuk pontosan megmondani.',
             '<strong>A berendezés teljesítménynyilatkozata.</strong> A gyártói dokumentáció része; az engedélyezésnél és az átadásnál egyaránt kérhetik.']),
        sec_numbered(
            'Ellenőrzőlista', 'Telekadat-ellenőrzőlista vásárlás előtt',
            'Ha ezekre a kérdésekre már a vételi döntés előtt tudja a választ, nem érheti meglepetés. Mindegyik megválaszolható a telek megtekintésével, az önkormányzatnál és a szomszédokkal beszélve.',
            ['<strong>Van-e közcsatorna a telek előtt, és ha nincs, tervezik-e?</strong> Kérjen ütemtervet, ne szóbeli tájékoztatást.',
             '<strong>Milyen a talaj, és tavasszal áll-e meg víz a telken?</strong> A tartós pangó víz magas talajvízszintre vagy rossz vízáteresztésre utal.',
             '<strong>Hol vannak a környező ásott és fúrt kutak?</strong> Ezek védőtávolsága szűkíti a beépíthető területet.',
             '<strong>Van-e a közelben felszíni befogadó?</strong> Árok, patak vagy csatorna — és ki a kezelője.',
             '<strong>Vízbázisvédelmi vagy más védett területen fekszik-e a telek?</strong> Ez felülír minden más szempontot, ezért ezzel érdemes kezdeni.',
             '<strong>Megközelíthető-e a telek hátsó része géppel?</strong> A telepítés és a későbbi iszapelszállítás egyaránt igényli.']),
        sec_cta('Következő lépés', 'Helyszíni felmérés a döntés előtt',
                ['Ha a telek szóba jöhet, de a fenti kérdések egy részére nincs válasz, a helyszíni felmérés a leggyorsabb út. A felmérésen a telepítés lehetséges helyét, a vízelhelyezés módját és a megközelíthetőséget nézzük meg — vagyis pontosan azt, amiből az ár és a megvalósíthatóság következik.',
                 'Vásárlás előtt is érdemes: ha kiderül, hogy a telek nem alkalmas, azt jobb a szerződés előtt megtudni.'],
                'Felmérés kérése', '../kapcsolat',
                alt=('Vagy nézze meg, milyen megoldások jöhetnek szóba', '../megoldasok/')),
        sec_faq([
            ('Vásárlás előtt is tudnak felmérést végezni?',
             'Igen. A telek adottságait a tulajdonos hozzájárulásával a vétel előtt is meg lehet nézni. Ez a leggyakoribb kérés azoktól, akik csatorna nélküli területen vásárolnának, és nem szeretnének utólag szembesülni a korlátokkal.'),
            ('Mennyivel drágább, ha a szennyvízkezelést csak a ház tervezése után nézzük meg?',
             'A különbséget nem a berendezés ára okozza, hanem a kényszermegoldások: hosszabb vezetékszakasz, mélyebb bekötés, átemelő beépítése vagy a szikkasztómező kedvezőtlen elhelyezése. Ezek együtt jelentős tételt tesznek ki, és utólag nehezen javíthatók.'),
            ('Mit tegyek, ha a talaj nem alkalmas szikkasztásra?',
             'Ilyenkor a kezelt víz elhelyezésének más módját kell megvizsgálni: felszíni befogadót vagy hasznosítást. Ha egyik sem lehetséges, a zárt tároló marad — ezt akkor is megmondjuk, ha nem a mi rendszerünk következik belőle.'),
        ]),
    ]))

# ===========================================================================
# 4) Meglévő emésztő kiváltása
# ===========================================================================
PAGES.append(dict(
    file='helyzetem/meglevo-emesztot-szeretnek-kivaltani.html',
    url='helyzetem/meglevo-emesztot-szeretnek-kivaltani', img='emeszto-csere',
    title='Meglévő emésztő kiváltása — mikor indokolt a csere | ÖkoTech Home',
    desc='Mikor indokolt a régi emésztő kiváltása, mi a különbség emésztő, oldómedence és biológiai rendszer között, és hogyan áll össze a teljes költség és megtérülés.',
    h1='Meglévő emésztőt szeretnék kiváltani',
    alt='Régi repedt betonemésztő nyitva a talajban egy idősebb családi ház mellett, mellette friss kiásott gödör az új tartálynak',
    lead='A kiváltás akkor jó döntés, ha a felmérés is alátámasztja. Van, amikor a régi rendszer még évekig üzemeltethető, és van, amikor a csere évek óta halasztott, elkerülhetetlen lépés. Ezen az oldalon végigvesszük, mi alapján lehet ezt eldönteni — a szippantási számlán túl.',
    crumbs=[HOME, HELY],
    sections=[
        sec_split(
            'Döntés', 'Mikor indokolt a csere?',
            'A csere mellett szól, ha…',
            ['<strong>a szippantás gyakorisága nő</strong>, vagy a költsége már összemérhető egy beruházás törlesztésével;',
             '<strong>a rendszer szagol, visszaduzzad vagy elfolyik</strong> — ezek nem üzemeltetési apróságok, hanem szerkezeti vagy kapacitásbeli problémára utalnak;',
             '<strong>az emésztő szikkasztó kialakítású</strong>, tehát a kezeletlen szennyvíz a talajba jut — ez ma a legtöbb helyen nem tartható állapot;',
             '<strong>bővítés vagy felújítás készül</strong>, és a terhelés növekedni fog;',
             '<strong>a betonszerkezet elöregedett</strong>: repedés, süllyedés, beomlott fedlap.'],
            'Nem sürgős a csere, ha…',
            ['<strong>a rendszer zárt és ép</strong>, és az ürítési gyakoriság évek óta egyenletes;',
             '<strong>a közcsatorna kiépítése ütemezett</strong>, és a bekötés belátható időn belül megtörténik;',
             '<strong>az ingatlant ritkán használják</strong>, és a terhelés töredéke az állandó lakhatásénak;',
             '<strong>a probléma egyetlen elemre szűkíthető</strong> — például a fedlapra vagy a bekötővezetékre —, mert akkor javítás is elég lehet.']),
        sec_numbered(
            'Fogalmak', 'Emésztő, oldómedence vagy biológiai rendszer?',
            'A három nem ugyanannak a dolognak három változata. Más a működésük, más a kimenetük, és más feltételekhez kötöttek.',
            ['<strong>Emésztő (zárt tároló).</strong> Nem kezel, csak gyűjt. A szennyvíz teljes mennyiségét el kell szállíttatni, így az üzemeltetési költség a vízfogyasztással arányosan nő. A régi, szikkasztó kialakítású emésztők ráadásul a kezeletlen szennyvizet a talajba engedik.',
             '<strong>Oldómedence szikkasztással.</strong> Mechanikai előkezelést végez, majd a részben tisztított víz szikkasztómezőre kerül. Áram nem kell hozzá, de a talaj vízáteresztő képessége és a talajvízszint korlátozza, és a szikkasztómező jelentős területet igényel.',
             '<strong>Biológiai szennyvíztisztító berendezés.</strong> A szennyvizet ténylegesen megtisztítja, a kezelt víz elhelyezése így lényegesen kisebb területen megoldható, és kedvező esetben hasznosítható is. Áramigénye van, és rendszeres — de kis munkaigényű — üzemeltetést kíván.']),
        sec_prose(
            'Költség', 'Teljes költség és megtérülés',
            ['A két megoldás csak akkor hasonlítható össze, ha mindkettőnél a teljes költséget nézzük. A meglévő emésztőnél ez elsősorban a rendszeres szippantás díja, amely a háztartás vízfogyasztásával együtt nő, és a szolgáltatói díjakkal együtt emelkedik.',
             'A biológiai rendszernél a beruházási költség mellett az áramfogyasztás, az időszakos iszapelszállítás és a karbantartás jelenik meg — ezek együtt jelentősen alacsonyabbak a folyamatos szippantásnál, de nem nulla tételek. A megtérülés ezért nem általánosan, hanem a konkrét háztartás fogyasztási adataiból számolható.',
             'A beruházási oldalon a berendezés ára gyakran nem a legnagyobb tétel: a földmunka, a bekötés mélysége, a régi emésztő megszüntetése és a kezelt víz elhelyezésének módja együtt jelentősen mozgatja a végösszeget. Ezért adunk sávot ajánlat helyett, amíg nem volt felmérés.',
             '<!-- ADATHIÁNY: konkrét üzemeltetési költségtáblázat (kompresszor energiafogyasztás W, iszapürítési gyakoriság, szippantási átlagdíj) — gyártói szervizlista és aktuális szolgáltatói díjak kellenek hozzá. -->']),
        sec_numbered(
            'Felmérés', 'A meglévő rendszer felmérése',
            'A csere előtt a régi rendszert is meg kell nézni — nemcsak azért, hogy kiderüljön, indokolt-e, hanem mert a megszüntetése is a projekt része.',
            ['<strong>A meglévő műtárgy típusa és állapota.</strong> Zárt vagy szikkasztó kialakítású, milyen anyagból van, ép-e a szerkezet, és milyen mély.',
             '<strong>A tényleges terhelés.</strong> A vízfogyasztási adatok és a szippantási gyakoriság együtt megmutatja, mekkora kapacitásra van valójában szükség.',
             '<strong>A bekötővezeték nyomvonala és mélysége.</strong> Ez dönti el, hogy az új berendezés a régi helyére kerülhet-e, vagy szükség van-e átemelőre.',
             '<strong>A régi emésztő sorsa.</strong> A megszüntetés módja — kiürítés, esetleg betömedékelés vagy elbontás — engedélyezési kérdés is, és költségtétel.',
             '<strong>A kezelt víz elhelyezése.</strong> Az új rendszer kimenetét el kell tudni helyezni; ez a felmérés legfontosabb pontja, mert enélkül a csere nem tervezhető.']),
        sec_cta('Következő lépés', 'Költség- és projektbrief a cseréhez',
                ['A döntéstámogató modul néhány kérdés alapján megmutatja, indokolt-e a csere az Ön esetében, mely megoldástípusok jönnek szóba, és milyen nagyságrendű költséggel érdemes számolni.',
                 'A modul nem ad árajánlatot: az eredmény tájékoztató jellegű, és a helyszíni felmérés adatai felülírhatják.'],
                'Döntéstámogató kitöltése', '../#dontestamogato',
                alt=('Vagy olvassa el, hogyan működik a biológiai tisztítás', '../megoldasok/biologiai-szennyviztisztitas')),
        sec_faq([
            ('Az új berendezés a régi emésztő helyére kerülhet?',
             'Néha igen, de ez nem alapeset. A régi műtárgy mérete, mélysége és állapota, valamint a bekötővezeték nyomvonala dönti el. A felmérésen ezt konkrétan megnézzük, mert a válasz jelentősen befolyásolja a földmunka költségét.'),
            ('Mi lesz a régi emésztővel?',
             'Ki kell üríteni, és a további sorsáról — betömedékelés vagy elbontás — a helyi előírások és a telepítés adottságai döntenek. Ez a projekt része és költségtétel, ezért az ajánlatban külön szerepel.'),
            ('Mennyi ideig tart a csere, és lakható-e közben az ingatlan?',
             'A telepítés maga általában néhány nap. Az ingatlan használata rövid ideig korlátozott, elsősorban a bekötés átvezetése alatt. A pontos ütemtervet a felmérés után adjuk meg, mert a földmunka mennyisége határozza meg.'),
        ]),
    ]))

# ===========================================================================
# 5) Nyaraló / szezonális
# ===========================================================================
PAGES.append(dict(
    file='helyzetem/nyaralo-vagy-szezonalisan-hasznalt-ingatlan.html',
    url='helyzetem/nyaralo-vagy-szezonalisan-hasznalt-ingatlan', img='nyaralo',
    title='Nyaraló vagy szezonálisan használt ingatlan — időszakos terhelés | ÖkoTech Home',
    desc='Mit jelent az időszakos terhelés a szennyvízkezelésben, mikor jobb az oldómedence a biológiai rendszernél, és mi történik hosszabb távollét után az újraindításkor.',
    h1='Nyaraló vagy szezonálisan használt ingatlan',
    alt='Bezárt magyar hétvégi ház késő ősszel, csukott zsalukkal, a nyíratlan gyepben látszó aknafedlappal',
    lead='Az időszakos használat nem „kevesebb" az állandó lakhatásnál, hanem más feladat. A biológiai tisztítás élő folyamat: hosszú távollét alatt a rendszer működése lelassul, és az újraindulásnak időre van szüksége. Ezt a technológia kiválasztásánál kell figyelembe venni, nem utólag.',
    crumbs=[HOME, HELY],
    sections=[
        sec_prose(
            'Terhelés', 'Mit jelent az időszakos terhelés?',
            ['A biológiai szennyvíztisztítás lényege, hogy mikroorganizmusok bontják le a szennyezőanyagot. Ez a folyamat folyamatos táplálékellátást feltételez: ha hetekig nem érkezik szennyvíz, a biológiai közösség aktivitása visszaesik.',
             'A szezonális használatnál ez kétféle problémát okoz. Egyrészt a hosszú szünet után a rendszer nem azonnal éri el a teljes tisztítási hatásfokot. Másrészt az újraindulás után gyakran hirtelen, nagy terhelés érkezik — egy hétvégi vendégsereg lényegesen több szennyvizet termel, mint amennyire a rendszer épp fel van készülve.',
             'Ezért a szezonális ingatlanoknál nem az a kérdés, hány fő használja, hanem hogy milyen a használati mintázat: hetente néhány nap, havonta egy hétvége, vagy egy összefüggő nyári időszak — ezek különböző megoldásokat kívánnak.']),
        sec_split(
            'Választás', 'Biológiai rendszer vagy oldómedence?',
            'A biológiai rendszer felé billen, ha…',
            ['<strong>a használat rendszeres</strong> — például hetente vagy kéthetente van terhelés a szezonban;',
             '<strong>a telek nem enged nagy szikkasztómezőt</strong>, mert a terület korlátozott vagy a talaj kötött;',
             '<strong>a kezelt vizet hasznosítaná</strong>, például öntözésre a szezonban;',
             '<strong>hosszabb távon állandó lakhatásra</strong> is gondol — a nyaralókból gyakran lesz állandó otthon.'],
            'Az oldómedence felé billen, ha…',
            ['<strong>a használat ritka és kiszámíthatatlan</strong> — évente néhány alkalom, hosszú, több hónapos szünetekkel;',
             '<strong>nincs megbízható áramellátás</strong>, vagy a téli időszakra lekapcsolják az ingatlant;',
             '<strong>a talaj vízáteresztő képessége jó</strong>, és a szikkasztómezőnek van elegendő szabad területe;',
             '<strong>a lehető legkevesebb üzemeltetést szeretné</strong>, és elfogadja a nagyobb területigényt.']),
        sec_numbered(
            'Üzemeltetés', 'Hosszabb távollét és újraindítás',
            'Ha biológiai rendszer mellett dönt szezonális ingatlanhoz, néhány üzemeltetési szabály betartásával a hatásfok gyorsan helyreáll.',
            ['<strong>A rendszert nem kell leüríteni a szezon végén.</strong> A tartályban maradó víz és az iszap tartalmazza azt a biológiai közösséget, amely a következő szezon indulásakor újraéled.',
             '<strong>A levegőztetést nem célszerű teljesen kikapcsolni</strong>, ha erre van mód. A csökkentett üzem lényegesen rövidebb újraindulást eredményez, mint a teljes leállítás.',
             '<strong>Az újraindulás után adjon időt a rendszernek.</strong> A teljes tisztítási hatásfok nem az első nap áll vissza; ez alatt az időszak alatt a kimenő víz minősége átmenetileg gyengébb.',
             '<strong>Kerülje a hirtelen csúcsterhelést az indulás első napjaiban.</strong> Ha lehet, a nagy vendégsereget ne közvetlenül a szezonnyitásra időzítse.',
             '<strong>A szezon előtti átnézés érdemes lépés.</strong> A kompresszor, a membrán és a fedlap állapotának ellenőrzése megelőzi a szezon közbeni leállást.']),
        sec_prose(
            'Referenciák', 'Szezonális esettanulmányok',
            ['Az időszakos használatú ingatlanok az eddigi projektek jelentős részét teszik ki: hétvégi házak, horgásztanyák és nyaralók, ahol a terhelés a szezonban koncentrálódik.',
             '<!-- ADATHIÁNY: konkrét szezonális esettanulmányok (helyszín, kapacitás, használati mintázat, telepítés éve, tapasztalatok) — ügyfél-hozzájárulással a cégnyilvántartásból. Addig ez a szekció nem publikálható konkrét referenciákkal. -->',
             'A konkrét esettanulmányokat az Eredmények területen tesszük közzé, ügyfél-hozzájárulás után.']),
        sec_cta('Következő lépés', 'Kezdje a használati profil rögzítésével',
                ['Szezonális ingatlannál a méretezés a használati mintázatból indul: hány alkalommal, hány fővel és milyen hosszan használják az ingatlant az év során. Ez a néhány adat többet mond, mint az ingatlan mérete.',
                 'A döntéstámogató modul ezt figyelembe veszi, és megmutatja, melyik technológia illik jobban az Ön használati módjához.'],
                'Döntéstámogató kitöltése', '../#dontestamogato',
                alt=('Vagy hasonlítsa össze a két technológiát', '../megoldasok/')),
        sec_faq([
            ('Télre le kell üríteni a rendszert?',
             'Nem. A tartályban maradó víz védi a szerkezetet és megőrzi a biológiai közösséget, amely a következő szezonban újraindul. A leürítés inkább árt: a rendszer üresen fagykárt szenvedhet, és az újraindulás is hosszabb lesz.'),
            ('Mi történik, ha egy évig egyáltalán nem használjuk az ingatlant?',
             'A biológiai aktivitás ilyenkor jelentősen visszaesik, és az újraindulás hosszabb időt vesz igénybe. Ilyen használati mintázatnál érdemes megvizsgálni, hogy nem az oldómedencés megoldás illik-e jobban — ezt a felmérésen konkrétan meg tudjuk mondani.'),
            ('Egy hétvégi vendégsereg megterheli a rendszert?',
             'Az alkalmi csúcsterhelést a berendezések elviselik, de a kiválasztásnál számolni kell vele. A méretezés ezért nem az átlagos, hanem a mértékadó terhelésre történik — a csúcsot előre meg kell adni, nem utólag kiderülni.'),
        ]),
    ]))

# ===========================================================================
# 6) Családi ház
# ===========================================================================
PAGES.append(dict(
    file='helyzetem/csaladi-hazhoz-keresek-rendszert.html',
    url='helyzetem/csaladi-hazhoz-keresek-rendszert', img='csaladi-haz',
    title='Családi házhoz keresek rendszert — megoldástípus, kapacitás, telepítés | ÖkoTech Home',
    desc='Családi házhoz választandó szennyvízkezelés: megoldástípus kiválasztása, telekalkalmasság, kapacitás és létszám, költség és telepítés, ajánlatkérési készültség.',
    h1='Családi házhoz keresek rendszert',
    alt='Modern földszintes családi ház gondozott kerttel, a gyepben két diszkrét aknafedlap jelzi a föld alatti tisztítórendszert',
    lead='Ez a leggyakoribb helyzet: adott a ház, ismert a háztartás létszáma, és a kérdés az, melyik megoldás való ide. A választást négy dolog dönti el — a telek, a terhelés, a kezelt víz sorsa és az engedélyezési feltételek. Ezeket vesszük végig sorrendben.',
    crumbs=[HOME, HELY],
    sections=[
        sec_numbered(
            'Választás', 'Megoldástípus kiválasztása',
            'A sorrend nem tetszőleges: a telek adottságai szűkítik a kört, és csak azon belül van értelme technológiát választani.',
            ['<strong>Először a kezelt víz elhelyezése.</strong> Ha nincs hová elhelyezni a tisztított vizet, a berendezés kiválasztása értelmetlen. Talajba szikkasztás, felszíni befogadó vagy hasznosítás — legalább az egyiknek működnie kell.',
             '<strong>Utána a technológia.</strong> Állandó lakhatásnál a biológiai berendezés a leggyakoribb választás, mert kisebb területen és jobb kimeneti minőséggel dolgozik. Az oldómedence ott jön szóba, ahol jó vízáteresztő talajon van elég hely a szikkasztómezőnek.',
             '<strong>Végül a kapacitás.</strong> A méretezés a mértékadó terhelésre történik, nem az átlagra — a bejelentett létszám és a várható csúcs együtt adja meg.',
             '<strong>És minden lépésnél az engedélyezési feltételek.</strong> Ezek településenként eltérnek, és felülírhatják a műszakilag egyébként jó megoldást.']),
        sec_numbered(
            'Telek', 'Telekalkalmasság',
            'Meglévő háznál a telek egy része már beépített, ezért a szabad felület elhelyezkedése is korlát. Négy dolgot érdemes megnézni.',
            ['<strong>Szabad, megközelíthető felület.</strong> A berendezés telepítéséhez gép kell, a későbbi iszapelszállításhoz szippantóautó. Ha a kiszemelt hely nem megközelíthető, az évtizedekre megdrágítja az üzemeltetést.',
             '<strong>Talaj és talajvíz.</strong> A vízáteresztő képesség és a mértékadó talajvízszint dönti el a vízelhelyezés módját és a szükséges területet.',
             '<strong>Védőtávolságok.</strong> Ásott és fúrt kutak — a sajátja és a szomszédoké is —, telekhatárok és épületek együtt jelölik ki a beépíthető sávot.',
             '<strong>A meglévő bekötés nyomvonala és mélysége.</strong> Ez dönti el, hogy gravitációsan megoldható-e a bekötés, vagy átemelő is kell hozzá.']),
        sec_prose(
            'Méretezés', 'Kapacitás és létszám',
            ['A kapacitás nem a ház alapterületéből, hanem a tényleges terhelésből következik. A méretezés alapja a háztartás létszáma és a fajlagos vízfogyasztás, kiegészítve a várható ingadozással.',
             'Érdemes előre gondolni: ha a család bővülhet, vagy rendszeresen fogadnak vendéget, azt a méretezésnél kell figyelembe venni. Az utólagos bővítés lényegesen drágább, mint az induláskor egy fokozattal nagyobb kapacitás.',
             'Ugyanakkor a jelentősen túlméretezett rendszer sem előnyös: a biológiai folyamat a tényleges terheléshez igazodik, és a tartósan alacsony terhelés a hatásfokot is befolyásolja. A cél nem a legnagyobb, hanem a mértékadó terheléshez illő berendezés.',
             '<!-- ADATHIÁNY: A.B. Clear és EPURECO modelltábla (típusjel, LE-kapacitás, névleges napi terhelés, tartályméret) — gyártói adatlapból. Ide egy .compare-table kerül, amint az adatok megvannak. -->']),
        sec_numbered(
            'Költség', 'Költség és telepítés',
            'A végösszeget ritkán a berendezés ára mozgatja leginkább. Az alábbi tételekkel érdemes számolni, mert ezek adják a különbséget két látszólag azonos projekt között.',
            ['<strong>Földmunka.</strong> A gödör mérete, a talaj kötöttsége és a kitermelt föld elhelyezése — sziklás vagy nagyon kötött talajon ez jelentős tétel.',
             '<strong>A bekötés mélysége és hossza.</strong> Mély bekötésnél átemelőre lehet szükség, ami beruházási és üzemeltetési költséget is jelent.',
             '<strong>A kezelt víz elhelyezése.</strong> A szikkasztómező kiépítése vagy a befogadóig vezető szakasz — talajtípustól és távolságtól függően eltérő nagyságrend.',
             '<strong>Elektromos bekötés.</strong> A berendezéshez áram kell; ha a telepítés helye messze van az elosztótól, a kábelezés is költség.',
             '<strong>Engedélyezés és dokumentáció.</strong> Mértéke a megoldástípustól és a helyi előírásoktól függ.',
             '<strong>Üzemeltetés.</strong> Áramfogyasztás, időszakos iszapelszállítás és karbantartás — ezek nélkül a megoldások nem hasonlíthatók össze.']),
        sec_cta('Következő lépés', 'Mikor áll készen az ajánlatkérésre?',
                ['Akkor, ha tudja a háztartás létszámát, a telek nagyjából szabad felületét, és van elképzelése arról, hová kerülhet a kezelt víz. Ennyivel már értelmes ajánlatot lehet kérni — a többit a felmérés tisztázza.',
                 'A döntéstámogató modul néhány kérdés alapján megmutatja, melyik megoldástípus jön szóba, és milyen költségtartománnyal érdemes számolni. Az eredmény tájékoztató jellegű.'],
                'Döntéstámogató kitöltése', '../#dontestamogato',
                alt=('Vagy kérjen helyszíni felmérést', '../kapcsolat')),
        sec_faq([
            ('Mekkora helyet foglal el a berendezés a kertben?',
             'A berendezés maga a föld alá kerül, a felszínen csak az aknafedlapok látszanak, így a kert használható marad. A területigényt nem a tartály, hanem a kezelt víz elhelyezése határozza meg — szikkasztómezőnél ez lényegesen nagyobb felület.'),
            ('Hallható vagy szagol a rendszer?',
             'Rendeltetésszerű üzemben nem. A levegőztetést végző kompresszor halk, és jellemzően védett helyre kerül. A szag mindig jelzés: eltömődésre, elmaradt iszapürítésre vagy meghibásodásra utal, ezért ilyenkor szervizt kell hívni.'),
            ('Mennyi az áramfogyasztása?',
             'A folyamatosan üzemelő kompresszor fogyasztása adja, ami a berendezés méretétől függ. A konkrét értéket a kiválasztott modell adatlapja tartalmazza; ezt az ajánlatban a várható éves üzemeltetési költséggel együtt adjuk meg.'),
        ]),
    ]))

# ===========================================================================
# 7) Vállalkozás / intézmény
# ===========================================================================
PAGES.append(dict(
    file='helyzetem/vallalkozas-vagy-intezmeny-szamara-keresek-megoldast.html',
    url='helyzetem/vallalkozas-vagy-intezmeny-szamara-keresek-megoldast', img='vallalkozas',
    title='Vállalkozás vagy intézmény — panzió, étterem, iskola, kemping, üzem | ÖkoTech Home',
    desc='Panziók, éttermek, iskolák, kempingek és üzemek szennyvízkezelése: miben más a vállalkozói terhelés, mit jelent a csúcsterhelés, és mit tartalmaz a szakmai projektbrief.',
    h1='Vállalkozás vagy intézmény számára keresek megoldást',
    alt='Vidéki panzió és kisüzemi telephely szervizudvarral, a parkoló mellett kompakt szennyvíztisztító berendezés vezérlőszekrénnyel',
    lead='Vállalkozásnál és intézménynél nem a létszám a méretezés alapja, hanem a terhelés jellege és időbeli eloszlása. Egy étterem konyhai szennyvize más feladat, mint egy iskoláé, és egy kemping nyári csúcsa más, mint egy panzió egyenletesebb foglaltsága. Ezért itt minden projekt egyedi méretezéssel indul.',
    crumbs=[HOME, HELY],
    sections=[
        sec_situations(
            'Területek', 'Melyik létesítménytípusról van szó?',
            'A tipikus feladatok az alábbi öt csoportba sorolhatók. Mindegyiknél más a szűk keresztmetszet, ezért a felmérés is másra kérdez rá.',
            [('nav-vallalkozas', 'Panziók és szálláshelyek',
              'A terhelés a foglaltsággal ingadozik, és a csúcs jellemzően a reggeli és esti órákra esik. A méretezésnél a szezonális ingadozás és a napi csúcs együtt számít.',
              '#szakmai-brief', 'Projektbrief'),
             ('nav-terheles', 'Éttermek és nagykonyhák',
              'A konyhai szennyvíz zsír- és szervesanyag-tartalma miatt előkezelés is szükséges lehet. A biológiai fokozat elé kerülő zsírfogó itt nem opció, hanem feltétel.',
              '#szakmai-brief', 'Projektbrief'),
             ('nav-kozossegi', 'Iskolák és intézmények',
              'Erősen ciklikus terhelés: napközbeni csúcs, hétvégi és szünidei szünet. A rendszernek a hosszabb leállásokat is jól kell viselnie.',
              '#szakmai-brief', 'Projektbrief'),
             ('nyaralo', 'Kempingek és közösségi létesítmények',
              'Rövid, koncentrált szezon, nagy csúcsterheléssel. A méretezés a szezonális maximumra készül, de a szezonon kívüli üzemet is kezelnie kell.',
              '#szakmai-brief', 'Projektbrief'),
             ('nav-mukodes', 'Üzemek és speciális terhelések',
              'Ha a szennyvíz összetétele eltér a kommunálistól, előzetes vizsgálat kell. Van, amikor a válasz az, hogy a feladat nem biológiai tisztítással oldható meg — ezt megmondjuk.',
              '#szakmai-brief', 'Projektbrief'),
             ]),
        sec_numbered(
            'Eltérések', 'Miben más ez a lakossági feladatnál?',
            'Négy különbség van, és mindegyik a méretezést érinti. Ezért nem lehet lakossági berendezést egyszerűen felnagyítani.',
            ['<strong>A csúcsterhelés dominál, nem az átlag.</strong> A rendszernek a legterheltebb órát kell kiszolgálnia. Az átlagos napi mennyiség önmagában félrevezető méretezési alap.',
             '<strong>A szennyvíz összetétele eltérhet.</strong> Konyhai zsír, mosodai vegyszer vagy technológiai szennyvíz esetén előkezelésre lehet szükség, különben a biológiai fokozat nem működik megfelelően.',
             '<strong>Az engedélyezés összetettebb.</strong> Nagyobb kapacitásnál a vízjogi engedélyezés és a kibocsátási feltételek részletesebb dokumentációt kívánnak.',
             '<strong>Az üzemeltetés felelőssége nevesített.</strong> Intézménynél és vállalkozásnál az üzemeltetés, a mintavétel és a dokumentálás rendje is a rendszer része — ezt a tervezésnél kell tisztázni.']),
        sec_split(
            'Buktatók', 'Mire figyeljen a tervezésnél',
            'Jó irányba indul, ha…',
            ['<strong>a tényleges csúcsterhelést méri vagy becsli</strong>, nem a névleges befogadóképességből indul;',
             '<strong>a szennyvíz összetételét is megvizsgálja</strong>, ha a tevékenység eltér az általános kommunálistól;',
             '<strong>az üzemeltetést a beruházással együtt tervezi</strong> — ki felel érte, milyen rendszerességgel, milyen dokumentálással;',
             '<strong>a bővítést előre beszámítja</strong>, ha a létesítmény kapacitása nőhet.'],
            'Kockázatot vállal, ha…',
            ['<strong>lakossági berendezést méretez fel</strong> vállalkozói terhelésre — a technológia nem skálázódik egyszerű szorzással;',
             '<strong>a konyhai szennyvizet előkezelés nélkül</strong> vezeti a biológiai fokozatra;',
             '<strong>a szezonon kívüli üzemmel nem számol</strong> — a hosszú leállás a biológiai rendszert érinti;',
             '<strong>az engedélyezést a beruházás végére hagyja</strong> — a kibocsátási feltételek visszahathatnak a műszaki megoldásra.']),
        sec_cta('Következő lépés', 'Szakmai projektbrief',
                ['Vállalkozói és intézményi projekteknél az első lépés a terhelési adatok összegyűjtése: létesítménytípus, kapacitás, üzemidő, szezonalitás és a szennyvíz jellege. Ezekből készül a méretezési alap.',
                 'Nagyobb kapacitásnál nem házi berendezést választunk, hanem méretezett rendszert tervezünk — több egység összekapcsolásával is. Referenciáink között szerepel <strong>Bakonypéterd központi szennyvíztisztító telepe</strong>, négy darab 50 fős berendezés összekapcsolásával.'],
                'Kapcsolatfelvétel', '../kapcsolat',
                alt=('Vagy nézze meg a nagyobb és közösségi rendszereket', '../megoldasok/nagyobb-es-kozossegi-rendszerek')),
        sec_faq([
            ('Mekkora kapacitástól számít nem lakossági feladatnak?',
             'Nem a határérték a lényeg, hanem a terhelés jellege. Egy nagy létszámú, de egyenletes terhelésű létesítmény kezelhető lehet sorozatgyártott berendezéssel is, míg egy kisebb étterem konyhai szennyvize már egyedi megoldást kíván. A besorolást a felmérés adja meg.'),
            ('Össze lehet kapcsolni több berendezést?',
             'Igen, ez bevett megoldás nagyobb kapacitásnál. Az egységek párhuzamos üzeme rugalmasabb is: részterhelésnél nem kell a teljes rendszert járatni. Bakonypéterden négy darab 50 fős berendezés alkotja a központi telepet.'),
            ('Kell-e külön üzemeltetői képzettség?',
             'A napi kezelés nem igényel szakképzettséget, de a felelősségi rend, a mintavétel és a dokumentálás rendje intézményi és vállalkozói üzemeltetésnél nevesített feladat. Ezt az átadáskor rögzítjük, és a szervizháttér is ehhez igazodik.'),
        ]),
    ]))

# ===========================================================================
# 8) Már van rendszerem
# ===========================================================================
PAGES.append(dict(
    file='helyzetem/mar-van-rendszerem-segitsegre-van-szuksegem.html',
    url='helyzetem/mar-van-rendszerem-segitsegre-van-szuksegem', img='mar-van-rendszerem',
    title='Már van rendszerem, segítségre van szükségem — szerviz és üzemeltetés | ÖkoTech Home',
    desc='Meglévő szennyvíztisztító rendszerhez üzemeltetési segítség, hibajelenség azonosítása, alkatrész és szerviz — az Ügyféltámogatás belépési pontja.',
    h1='Már van rendszerem, segítségre van szükségem',
    alt='Szervizre nyitott biológiai tisztító akna gondozott kertben, mellette kompresszorszekrény és kiterített szerszámok',
    lead='Ha a rendszer már működik, a kérdés nem a választás, hanem az üzemeltetés. Az alábbi belépési pontok az Ügyféltámogatás területére vezetnek: hibajelenség, karbantartás, alkatrész és szerviz. Nem tőlünk származó berendezéssel is fordulhat hozzánk — megmondjuk, ha nem tudunk segíteni.',
    crumbs=[HOME, HELY],
    sections=[
        sec_situations(
            'Támogatás', 'Miben tudunk segíteni?', None,
            [('nav-szerviz', 'Hibajelenség azonosítása',
              'Szag, visszaduzzadás, szokatlan zaj vagy leállt kompresszor: az első lépés annak eldöntése, üzemeltetési vagy műszaki okról van-e szó.',
              '../ugyfeltamogatas/', 'Hibajelenségek'),
             ('nav-mukodes', 'Rendszeres karbantartás',
              'Az iszapszint ellenőrzése, a membrán és a kompresszor átnézése, valamint az időszakos iszapelszállítás — ezek adják a rendszer élettartamát.',
              '../ugyfeltamogatas/', 'Karbantartás'),
             ('nav-telepites', 'Alkatrész és csere',
              'Kompresszor, membrán, fedlap és egyéb kopó elemek. A pontos típus a berendezés adattáblájáról olvasható le.',
              '../ugyfeltamogatas/', 'Alkatrészek'),
             ('nav-felmeres', 'Meglévő rendszer felmérése',
              'Ha nem tudja, milyen rendszer van a telken, vagy régóta nem volt átnézve: a felmérés megmutatja az állapotát és a további teendőket.',
              '../kapcsolat', 'Felmérés kérése'),
             ]),
        sec_numbered(
            'Első lépések', 'Mit érdemes megnézni, mielőtt szervizt hív',
            'Az esetek egy részében a probléma üzemeltetési okra vezethető vissza, és néhány perces ellenőrzéssel tisztázható. Ez a lista nem helyettesíti a szervizt, de segít pontosabban leírni a helyzetet.',
            ['<strong>Van-e áram a berendezésen?</strong> Kioldott kismegszakító vagy kihúzott csatlakozó a leggyakoribb ok a kompresszor leállása mögött.',
             '<strong>Működik-e a kompresszor?</strong> Halk, egyenletes hang normális. A teljes csend vagy a szokatlanul hangos, egyenetlen működés egyaránt jelzés.',
             '<strong>Mikor volt utoljára iszapelszállítás?</strong> Az elmaradt iszapürítés a leggyakoribb oka a hatásfokromlásnak és a szagnak.',
             '<strong>Változott-e a terhelés?</strong> Több lakó, hosszabb vendégség vagy éppen több hetes távollét egyaránt hatással van a rendszer működésére.',
             '<strong>Került-e a rendszerbe olyasmi, ami nem oda való?</strong> Nedves törlőkendő, zsír, festék, gyógyszer vagy fertőtlenítőszer nagy mennyiségben mind kárt tesz a biológiai folyamatban.']),
        sec_cta('Ügyféltámogatás', 'Lépjen tovább a támogatási területre',
                ['A hibajelenségek, a karbantartási teendők, az alkatrészek és a szervizkérés részletesen az Ügyféltámogatás területen szerepelnek.',
                 'Ha a berendezés nem tőlünk származik, akkor is írjon: megnézzük, tudunk-e segíteni, és megmondjuk, ha nem — ilyenkor igyekszünk megmondani, kihez érdemes fordulni.'],
                'Ügyféltámogatás', '../ugyfeltamogatas/',
                alt=('Vagy írjon közvetlenül a szerviznek', '../kapcsolat')),
        sec_faq([
            ('Nem tőletek van a berendezés — tudtok segíteni?',
             'Sok esetben igen, különösen üzemeltetési kérdésekben és felmérésnél. Alkatrésznél a típus dönt: ha az adott gyártó eleme nem beszerezhető, azt megmondjuk, ahelyett hogy alkalmatlan helyettesítőt javasolnánk.'),
            ('Milyen gyakran kell iszapot elszállíttatni?',
             'Ez a terheléstől és a berendezés típusától függ, ezért nem adható meg általánosan. Az iszapszint ellenőrzése a rendszeres karbantartás része, és abból következik az ürítés időpontja — nem naptári alapon érdemes tervezni.'),
            ('Mit jelent, ha szagot érzek a rendszer közelében?',
             'A szag mindig jelzés, nem normál üzemállapot. Leggyakoribb oka az elmaradt iszapürítés, a levegőztetés kiesése vagy a szellőzés eltömődése. Ha az áramellátás és a kompresszor rendben van, érdemes szervizt hívni.'),
        ]),
    ]))


# ===========================================================================
if __name__ == '__main__':
    for p in PAGES:
        out = WEB / p['file']
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(build(p), encoding='utf-8')
        print(f"{p['file']:70s} {len(out.read_text(encoding='utf-8')) // 1024:3d} KB")
