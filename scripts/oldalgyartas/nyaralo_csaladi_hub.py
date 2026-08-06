#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helyzetem → Nyaraló/szezonális (5) és Családi ház (5) — tíz aloldal.

NÉGY ÁLLÍTÁS, AMIT A BRIEFEK SZERINT NEM SZABAD ÁTVENNI VÁLTOZTATÁS NÉLKÜL —
mindegyik jelölve van, és egyik sincs feloldva a saját szakállunkra:

1. „Nyaraló = oldómedence." A webhely az aktív rendszert életvitelszerű
   használathoz köti, DE az A.B. Clear kezelési dokumentációja szabadságüzemmódot
   tartalmaz. Ez valószínűleg nem valódi ellentmondás — a rövid távollét és a
   tartós szezonális nulla terhelés más —, de a látogató számára nem derül ki.
   A briefek szerint ennek tisztázása az ág legértékesebb szakmai hozzájárulása.
   EZT BELSŐ MŰSZAKI DÖNTÉSSEL KELL RENDEZNI, nem tartalomírással.

2. Az EPURECO baktériumadalék-ajánlása GYÁRTÓI ÜZEMELTETÉSI ELŐÍRÁS, nem
   univerzális biológiai tény. Így is szerepel.

3. A „150%-os rövid túlterhelés" modellenként, vizsgálattal validálandó.
   Az elv (a rövid vendégcsúcs nem feltétlenül indokol nagyobb berendezést)
   megmarad, a SZÁM nem.

4. A „zéró szippantás" mellé oda kell tenni, milyen iszapzsák-kezelési feladat
   marad a tulajdonosnál. Ez nem gyengíti az értékajánlatot: előre láthatóvá
   teszi a valódi üzemeltetési modellt.

Konkrét ár sehol. A telepítésszám (3500+ / 3800+) továbbra sem megerősített.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import sec_numbered, sec_split, sec_prose, sec_cta, sec_faq

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'


def hiany(mi, honnan):
    return f'<!-- ADATHIÁNY: {mi}\n     Forrás: {honnan}. Addig konkrét értékkel nem publikálható. -->'


TISZTAZANDO = ('<!-- BELSŐ MŰSZAKI DÖNTÉSRE VÁR — a hub legfontosabb nyitott kérdése:\n'
               '     PONTOSAN milyen hosszú és milyen gyakori kihagyást kezel az A.B. Clear\n'
               '     biztonságosan, és milyen beállítás mellett? A webhely az aktív rendszert\n'
               '     életvitelszerű használathoz köti, a kezelési dokumentáció viszont\n'
               '     szabadságüzemmódot tartalmaz. A kettő valószínűleg nem mond ellent\n'
               '     egymásnak, de amíg nincs jóváhagyott határérték, konkrét időtartamot\n'
               '     NEM írunk ki. A nyilvános A.B. Clear PDF verziója V4_2019.02.27. —\n'
               '     ellenőrizni kell, van-e frissebb belső változat. -->')

# ─────────────────────────────────────────────────────────── NYARALÓ
def n_terheles():
    return [
        sec_prose('A valódi kérdés', 'Nem az, hányan használják', [
            'Egy négyfős nyaraló háromféle dolgot jelenthet: minden hétvégén használt házat, '
            'júniustól augusztusig folyamatosan lakott ingatlant, vagy évi néhány alkalommal '
            'felkeresett vadászházat. <strong>Ugyanaz a létszám, három különböző műszaki '
            'feladat.</strong>',
            'A terhelést ezért nem a személyszám írja le, hanem a <strong>használati '
            'mintázat</strong>: mikor, milyen gyakran és mennyi ideig keletkezik szennyvíz — '
            'és mekkora a leghosszabb teljes szünet.']),
        sec_numbered('Amit rögzíteni kell', 'Hat adat, amiből terhelési profil lesz',
                     'Ezek együtt többet mondanak, mint a létszám önmagában.',
                     ['<strong>Mely hónapokban használják</strong> az ingatlant.',
                      '<strong>Milyen gyakran térnek vissza</strong> — hetente, havonta, évente '
                      'néhányszor.',
                      '<strong>Egy tartózkodás átlagos hossza</strong>, és a leghosszabb '
                      'összefüggő használat.',
                      '<strong>A leghosszabb teljes kihagyás</strong> — ez a technológiaválasztás '
                      'legerősebb szűrője.',
                      '<strong>Jellemző és maximális létszám</strong>, és hogy a maximum milyen '
                      'gyakran fordul elő.',
                      '<strong>Van-e áram a távollét alatt</strong>, és téliesítik-e az épületet.']),
        sec_split('Két különböző dolog', 'Az alulterhelés nem ugyanaz, mint a nulla terhelés',
                  'Alulterhelés — kevés, de rendszeres szennyvíz',
                  ['a biológiai közösség kap táplálékot, csak keveset;',
                   'a rendszer működik, a hatásfok jellemzően tartható;',
                   '<strong>rendszeres hétvégi használat</strong> jellemzően ide tartozik.'],
                  'Nulla terhelés — hetekig semmi',
                  ['a biológiai közösség aktivitása visszaesik;',
                   'az újraindulás időt vesz igénybe;',
                   '<strong>a hosszú szezonális szünet</strong> ide tartozik — és ez az, ami a '
                   'technológiaválasztást felülírhatja.']),
        f'''
  <section class="section" aria-labelledby="hatar-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Nyitott kérdés</p>
        <h2 class="type-display-section-title section-title" id="hatar-cim">
          Hol a határ pontosan?
        </h2>
      </header>
      {TISZTAZANDO}
      <p class="type-ui-body section-lead">
        Azt, hogy <strong>meddig</strong> tekinthető a kihagyás rövidnek és hol kezdődik a
        tartós szünet, konkrét időtartamban nem írjuk ki, amíg a saját műszaki adataink ezt
        nem támasztják alá. Egy tévesen megadott határérték rossz technológiaválasztáshoz
        vezetne — és ez évtizedes döntés.
      </p>
      <p class="type-ui-body section-lead">
        A felmérésen viszont az Ön konkrét használati mintájára meg tudjuk mondani.
      </p>
      {hiany('a „rövid”, „közepes” és „hosszú” kihagyás műszaki definíciója; milyen profilnál választanak A.B. Cleart, milyennél EPURECO-t; mely esetben egyik sem megfelelő standard konfigurációban; valós szezonális ügyfelek éves használati mintái.', 'ÖkoTech műszaki vezetés')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'A profilból következik a technológia',
                ['Ha a használati mintázat megvan, a két irány feltételei összevethetők — és az '
                 'is kiderül, ha a telek írja felül a döntést.'],
                'Biológiai rendszer vagy oldómedence?', 'biologiai-rendszer-vagy-oldomedence',
                alt=('Vagy állítsa össze a használati profilját', 'hasznalati-profil')),
    ]


def n_valasztas():
    return [
        sec_prose('Nem szabály, hanem feltétel', 'A „nyaraló = oldómedence" túl egyszerű', [
            'Az EPURECO oldómedencés rendszert kifejezetten időszakosan használt ingatlanokhoz '
            'ajánljuk, mert passzív működésű és nem igényel folyamatos áramot. Ebből azonban '
            '<strong>nem lesz automatikus szabály</strong>: a tisztítómező területigénye, a '
            'talaj és a talajvíz ugyanúgy dönt.',
            'Az aktív biológiai rendszer viszont nem zárható ki pusztán azért, mert az ingatlan '
            'nem lakott folyamatosan — a kritikus változó a <strong>kihagyás hossza és '
            'ismétlődése</strong>, nem maga a szezonalitás.']),
        sec_split('Irányok', 'Mi billenti melyik felé',
                  'Az oldómedencés irány felé billen, ha…',
                  ['<strong>hosszúak és ismétlődőek a szünetek</strong> — évi néhány alkalom, '
                   'hónapos kihagyásokkal;',
                   '<strong>nincs áram a távollét alatt</strong>, vagy télre lekapcsolják;',
                   '<strong>jó a talaj vízáteresztő képessége</strong>, és van hely a '
                   'tisztítómezőnek;',
                   '<strong>a lehető legkevesebb üzemeltetést</strong> szeretné.'],
                  'Az aktív biológiai irány felé billen, ha…',
                  ['<strong>rendszeres a használat</strong> a szezonban — például hetente;',
                   '<strong>korlátozott a szabad terület</strong>, a tisztítómező nem férne el;',
                   '<strong>kötött a talaj vagy magas a talajvíz</strong>;',
                   '<strong>hosszabb távon állandó lakhatásra</strong> is gondol.']),
        sec_numbered('Üzemeltetés', 'Amit a két irány másképp kér', None,
                     ['<strong>Áram.</strong> Az aktív rendszer folyamatos ellátást igényel; '
                      'az oldómedence nem.',
                      '<strong>Iszapkezelés.</strong> Mindkettőnél van, de más ritmusban és más '
                      'módon.',
                      '<strong>Adalékanyag.</strong> Az A.B. Clear rendszerben a baktériumkultúrát '
                      'a beérkező szennyvíz táplálja. Az EPURECO-nál hosszabb kihagyás után '
                      '<strong>a gyártó frissítő adalékot javasol</strong> — ez üzemeltetési '
                      'előírás, nem általános biológiai szabály.',
                      '<strong>Ellenőrzés távollétben.</strong> Szezonális ingatlannál számít, '
                      'van-e valaki, aki időnként ránéz a rendszerre.']),
        f'''
  <section class="section" aria-labelledby="nyitott-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Amit még pontosítunk</p>
        <h2 class="type-display-section-title section-title" id="nyitott-cim">
          Konkrét időtartamot itt nem adunk
        </h2>
      </header>
      {TISZTAZANDO}
      <p class="type-ui-body section-lead">
        Az A.B. Clear vezérlése tartalmaz <strong>szabadságüzemmódot</strong> a tervezett
        távollétre. Azt viszont, hogy ez pontosan mekkora kihagyásra szolgál, csak jóváhagyott
        műszaki adat alapján írjuk ki — addig a felmérésen mondjuk meg, az Ön használati
        mintájára.
      </p>
      {hiany('az A.B. Clear és az EPURECO alkalmazási mátrixa; a szabadságüzemmód célja és időkorlátja; az újraindítás szükségessége és körülményei; az EPURECO adalék adagolása és bizonyítéka; a tényleges szippantási intervallumok használati profil szerint.', 'gyártói dokumentáció + ÖkoTech műszaki vezetés')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'Mi történik a hosszú szünet alatt?',
                ['A távolléti működés és az újrahasználat feltételei a legtöbb kérdést itt '
                 'vetik fel — érdemes vásárlás előtt tisztán látni.'],
                'Hosszabb távollét és újraindítás', 'hosszabb-tavollet-es-ujrainditas',
                alt=('Vagy nézze meg a szezonális eseteket', 'szezonalis-esettanulmanyok')),
    ]


def n_tavollet():
    return [
        sec_prose('Három különböző helyzet', 'A „hosszabb távollét" nem egyetlen állapot', [
            'Más következménye van egy kéthetes nyári szünetnek, egy három hónapos téli '
            'leállásnak, és annak, ha az ingatlan egész évben csak havonta egy hétvégén lakott.',
            'A cél az, hogy <strong>vásárlás előtt</strong> tudja, milyen teendővel jár a '
            'választott rendszer — ne a használati útmutatóból derüljön ki később.']),
        sec_numbered('Az utolsó használati nap', 'Amit távozás előtt érdemes megtenni',
                     'Az alábbiak általános elvek. A konkrét lépéseket mindig a berendezés '
                     'saját, aktuális kezelési utasítása írja elő — modellenként eltérhet.',
                     ['<strong>A rendszert nem kell leüríteni.</strong> A tartályban maradó víz '
                      'védi a szerkezetet, és megőrzi a biológiai közösséget.',
                      '<strong>Aktív rendszernél a levegőztetés teljes kikapcsolása kerülendő.</strong> '
                      'A vezérlés tervezett távollétre <strong>szabadságüzemmódot</strong> kínál — '
                      'ennek beállítását a kezelési utasítás írja le.',
                      '<strong>Ne juttasson a rendszerbe</strong> a szokásostól eltérő anyagot az '
                      'utolsó napokban — fertőtlenítőt, festéket, nagy mennyiségű zsírt.',
                      '<strong>Ellenőrizze a fedlapot és a szellőzést</strong>, mielőtt hosszabb '
                      'időre magára hagyja.']),
        sec_numbered('Az első visszatérési nap', 'Amit érkezéskor érdemes végignézni', None,
                     ['<strong>Áram és kompresszor.</strong> Aktív rendszernél az első ellenőrzés: '
                      'van-e áram, és halkan, egyenletesen jár-e a kompresszor.',
                      '<strong>Adjon időt a rendszernek.</strong> A teljes tisztítási hatásfok nem '
                      'az első nap áll vissza; ez alatt a kimenő víz minősége átmenetileg gyengébb.',
                      '<strong>Kerülje a hirtelen csúcsterhelést</strong> az első napokban — a '
                      'nagy vendégsereget ne közvetlenül a szezonnyitásra időzítse.',
                      '<strong>Oldómedencés rendszernél</strong> a gyártó hosszabb kihagyás után '
                      'frissítő baktériumadalékot javasolhat; ezt az adott termék előírása szerint.',
                      '<strong>Szag, habzás vagy zavarosság esetén</strong> ne várjon: ezek '
                      'jelzések, nem beszokási tünetek.']),
        sec_split('Ki mit intéz', 'A tulajdonos feladata és a szakemberé',
                  'Amit Ön elvégezhet',
                  ['a szabadságüzemmód beállítása a kezelési utasítás szerint;',
                   'szemrevételezés: fedlap, szellőzés, kompresszor hangja;',
                   'az adalék adagolása, ahol a gyártó előírja;',
                   'a használati napló vezetése — távollétnél különösen hasznos.'],
                  'Amihez szakember kell',
                  ['tartós szag vagy vízminőségi eltérés az újraindulás után;',
                   'hibajelzés a vezérlésen;',
                   'a rendszer teljes leállása után az újraindítás;',
                   'fagykár gyanúja téliesített ingatlannál.'],
                  ),
        f'''
  <section class="section" aria-labelledby="dok-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Forrás</p>
        <h2 class="type-display-section-title section-title" id="dok-cim">
          A konkrét utasítás mindig a berendezésé
        </h2>
      </header>
      {TISZTAZANDO}
      <p class="type-ui-body section-lead">
        Ez az oldal az elveket írja le. A beállítások, időtartamok és lépések a berendezés
        <strong>saját, aktuális kezelési és karbantartási utasításából</strong> következnek,
        modell- és verziószám szerint — nem általános szabályból.
      </p>
      {hiany('az A.B. Clear aktuális kezelési dokumentációja (a nyilvános PDF V4_2019.02.27.); a szabadságüzemmód hivatalos időtartama és beállítási logikája; a szezonális szerviztapasztalatok; az újraindítás tényleges gyakorisága és oka; a téli és fagyvédelmi protokoll; a szezonnyitási ellenőrzőlista.', 'ÖkoTech műszaki vezetés + gyártói dokumentáció')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'Hasonló helyzetek a gyakorlatban',
                ['A szezonális ingatlannál a vásárlási kockázat éppen a többéves működés — '
                 'ezért a hasonló használati mintájú esetek mondják a legtöbbet.'],
                'Szezonális esettanulmányok', 'szezonalis-esettanulmanyok'),
    ]


def n_esetek():
    return [
        sec_prose('Miért nem fotógaléria', 'A használati ritmus a bizonyíték', [
            'Szezonális ingatlannál nem az a kérdés, hogy szép-e a telepítés, hanem hogy '
            '<strong>évek óta működik-e ugyanolyan használati mintázat mellett</strong>, mint '
            'amilyet Ön tervez.',
            'Ezért minden esethez az ingatlan típusa, az éves használati minta, a leghosszabb '
            'távollét, a telek adottságai, a választott rendszer, a választás indoka és a '
            'telepítés éve tartozik — nem csak egy kép és egy idézet.']),
        f'''
  <section class="section" aria-labelledby="esetek-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Esetek</p>
        <h2 class="type-display-section-title section-title" id="esetek-cim">
          Szezonális esettanulmányok
        </h2>
      </header>
      <aside class="panel">
        <p class="type-ui-body"><strong>Az esettár összeállítás alatt van.</strong> Szezonális
          ingatlanhoz nem közlünk esetet addig, amíg a többéves működési adat — szezonnyitási
          teendők, szervizigény, tényleges karbantartás — nem áll rendelkezésre hozzá.
          Egy fotó és egy idézet ezen a területen nem bizonyíték.</p>
        <p class="type-ui-body">Az időszakos használatú ingatlanok az eddigi projektek jelentős
          részét teszik ki. Ha hasonló helyzetről szeretne hallani, írjon —
          <a href="../kapcsolat">elmondjuk, mit tapasztaltunk</a>.</p>
      </aside>
      {hiany('szezonális referenciák használati profil szerint: ingatlantípus, telepítési év, rendszer és kapacitás, használati hónapok és gyakoriság, normál és maximum létszám, leghosszabb távollét, talaj és talajvíz, vízelhelyezés, a választás indoka, a kizárt alternatívák, szezonnyitási teendők, valós karbantartás, szervizesemények, működési időtáv. Ügyfél-hozzájárulás és anonimizálás szükséges; olyan következtetés nem szerepelhet, amelyet az esetadat nem bizonyít.', 'ÖkoTech projekt- és szerviznyilvántartás')}
    </div>
  </section>
''',
        sec_cta('Addig is', 'Készítse el a saját profilját',
                ['A használati profil néhány kérdés alapján megmutatja, mely irányok maradnak '
                 'relevánsak az Ön mintázatához, és mit kell még tisztázni.'],
                'Használati profil elkészítése', 'hasznalati-profil'),
    ]


def n_profil():
    return [
        sec_prose('Mire jó', 'A „nyaraló, 4 fő" túl kevés', [
            'Ez az eszköz nem terméket választ. Az éves használati mintázatból <strong>terhelési '
            'profilt</strong> készít, amiből eldönthető, mely technológiai irányok maradnak '
            'relevánsak — és milyen telek- vagy műszaki adat hiányzik még.',
            'Minden kérdésnél elfogadható a „nem tudom", és minden kérdésnél ott áll, hogy '
            'befolyásolja-e a technológiát, vagy csak a méretezést.']),
        sec_numbered('Amit kérdez', 'Négy csoport', None,
                     ['<strong>Használati naptár.</strong> Mely hónapokban, milyen gyakran, '
                      'meddig — és mekkora a leghosszabb kihagyás.',
                      '<strong>Létszám.</strong> Jellemző és maximális, és hogy a maximum milyen '
                      'gyakran fordul elő.',
                      '<strong>Terhelés.</strong> Vízfogyasztás, ha ismert; mosógép, '
                      'mosogatógép; vendégcsúcs; bérbeadás.',
                      '<strong>Távolléti feltételek.</strong> Marad-e áram, téliesítik-e az '
                      'épületet, van-e időszakos felügyelet.']),
        f'''
  <section class="section" aria-labelledby="modul-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">A modul</p>
        <h2 class="type-display-section-title section-title" id="modul-cim">A profilkészítő</h2>
      </header>
      <aside class="panel">
        <p class="type-ui-body"><strong>A profilkészítő még nem él.</strong> A szabályait — melyik
          válasz melyik irányt zárja ki vagy nyitja meg — nem lehet megírni addig, amíg a
          kihagyási határértékek nincsenek jóváhagyva. Ez ugyanaz a nyitott kérdés, amit ez a
          hub végig jelöl.</p>
        <p class="type-ui-body">Addig írja le a használati mintáját néhány mondatban, és
          átvesszük Önnel: <a href="../kapcsolat">Kapcsolatfelvétel</a>.</p>
      </aside>
      {TISZTAZANDO}
      {hiany('a műszaki csapat által jóváhagyott terhelésiprofil-szabályok; melyik válasz változtat technológiát és melyik csak kapacitást; mi vált ki szakértői egyeztetést; milyen kihagyási idő kritikus az A.B. Clear szempontjából; az EPURECO felső terhelési korlátai; felhasználói teszt arról, hogy az ügyfelek meg tudják-e adni ezt az információt.', 'ÖkoTech műszaki vezetés')}
    </div>
  </section>
''',
        sec_cta('Addig is', 'Beszéljünk a használatáról',
                ['Írja meg, mely hónapokban és milyen gyakran használják az ingatlant, és mekkora '
                 'a leghosszabb szünet — ennyi már elég ahhoz, hogy megmondjuk, melyik irány '
                 'jöhet szóba.'],
                'Kapcsolatfelvétel', '../kapcsolat'),
    ]


# ─────────────────────────────────────────────────────── CSALÁDI HÁZ
def cs_megoldas():
    return [
        sec_prose('A kiindulópont', 'Az állandó használat még nem elég a döntéshez', [
            'Életvitelszerűen lakott családi háznál az aktív biológiai irány természetes '
            'kiindulópont — de <strong>nem automatikus végkövetkeztetés</strong>. A telek '
            'helyigénye, a talaj, a talajvíz, az áramellátás, a kezelt víz elhelyezése és a '
            'vállalható üzemeltetés együtt írhatja felül.',
            'A választás sorrendje: előbb a kezelt víz elhelyezése, aztán a technológia, '
            'végül a kapacitás. Fordítva a projekt közepén derül ki, hogy nem megvalósítható.']),
        sec_numbered('Amit a használó ténylegesen érzékel', 'Öt különbség', None,
                     ['<strong>Kell-e áram.</strong> Az aktív rendszernél folyamatosan; a '
                      'passzívaknál nem.',
                      '<strong>Mennyi hely kell.</strong> Nem a tartály, hanem a kezelt víz '
                      'elhelyezése a nagyobb tétel — oldómedencénél a tisztítómező.',
                      '<strong>Milyen rendszeres feladat van.</strong> Aktív rendszernél '
                      'ellenőrzés és kopó alkatrész; passzívnál kevesebb, de nem nulla.',
                      '<strong>Hogyan kezelődik az iszap.</strong> Zárt tárolónál a teljes '
                      'mennyiség elszállítása; a másik kettőnél időszakos iszapkezelés.',
                      '<strong>Hová megy a víz.</strong> Ez dönti el, hogy egyáltalán melyik '
                      'irány jöhet szóba.']),
        sec_numbered('Mikor nem megfelelő', 'Mindhárom megoldásnak van ilyen helyzete', None,
                     ['<strong>A zárt tároló nem jó,</strong> ha az állandó használat mellett a '
                      'szippantás gyakorisága vagy szervezése tarthatatlan.',
                      '<strong>Az oldómedencés rendszer nem jó,</strong> ha nincs elég terület a '
                      'tisztítómezőnek, kötött a talaj vagy magas a talajvíz.',
                      '<strong>Az aktív biológiai rendszer nem jó,</strong> ha nincs folyamatos '
                      'áram, vagy ha az ingatlant hosszú szünetekkel használják.']),
        sec_cta('Következő lépés', 'Elhelyezhető-e a telken?',
                ['A technológia csak akkor releváns, ha a telek engedi. A csőszint, a talajvíz és '
                 'a vízelhelyezés együtt dönti el, mi valósítható meg.'],
                'Telekalkalmasság', 'telekalkalmassag',
                alt=('Vagy a kapacitás kérdése', 'kapacitas-es-letszam')),
    ]


def cs_telek():
    return [
        sec_prose('A valódi kérdés', 'Nem az, hogy elfér-e', [
            'A telekalkalmasság nem geometria. A házból érkező szennyvízvezeték <strong>szintje</strong>, '
            'a tereplejtés, a talaj, a talajvíz, a rendelkezésre álló hely és a kezelt víz '
            'elhelyezése <strong>összefüggő</strong> műszaki feltétel — egyiket sem lehet a '
            'többi nélkül eldönteni.',
            'És egy fontos különbség: a <strong>telekalkalmasság nem termékalkalmasság</strong>. '
            'Attól, hogy a telek elvileg megfelel, még nem következik, hogy bármelyik konkrét '
            'berendezés beépíthető rá változtatás nélkül.']),
        sec_numbered('Ami leggyakrabban módosít', 'Négy adottság, amelyik konfigurációt változtat',
                     'Ezek jellemzően nem zárnak ki — de eltérő kialakítást kívánnak, ami a '
                     'költséget is mozgatja.',
                     ['<strong>A befolyó cső mélysége.</strong> Ha a szennyvízvezeték mélyebben '
                      'érkezik, mint amit a berendezés fogadószintje enged, magasítás vagy '
                      'átemelő válhat szükségessé. Ezt már a ház tervezésénél érdemes tisztázni.',
                      '<strong>Magas vagy ingadozó talajvíz.</strong> Nem igen/nem kérdés: '
                      'módosíthatja a tartály beépítési kialakítását, és <strong>külön kell '
                      'vizsgálni</strong> a kezelt víz elhelyezhetőségét — a kettő nem ugyanaz.',
                      '<strong>Járműterhelés.</strong> Ha a fedlap fölött autó áll vagy közlekedik, '
                      'az a kialakítást érinti.',
                      '<strong>Szerelési és szervizhozzáférés.</strong> Ami a telepítéskor szűk, '
                      'az a későbbi karbantartásnál is az marad.']),
        sec_numbered('Négy eredmény', 'Az előszűrés nem ad „alkalmas" pecsétet', None,
                     ['<strong>Standard.</strong> Az adatok ismertek, kockázatot nem mutatnak.',
                      '<strong>Feltételes.</strong> Megvalósítható, de eltérő kialakítással.',
                      '<strong>További adat szükséges.</strong> Jellemzően a talajvíz vagy a '
                      'csőszint hiányzik. Ez a leggyakoribb, és nem rossz hír.',
                      '<strong>Helyszíni felmérés kell.</strong> Az adatok ellentmondanak, vagy a '
                      'telek műszakilag nem standard.']),
        f'''
  <section class="section" aria-labelledby="nemtudom-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Ha nem tudja</p>
        <h2 class="type-display-section-title section-title" id="nemtudom-cim">
          Ismeretlen talajvízre nem adunk „alkalmas" eredményt
        </h2>
      </header>
      <p class="type-ui-body section-lead">
        Ha a talajvíz vagy a kezelt víz elhelyezése nem ismert, abból nem lesz alkalmassági
        minősítés — sem igen, sem nem. Ilyenkor az a helyes válasz, hogy <strong>mit kell
        megszerezni</strong>, és honnan.
      </p>
      <p class="type-ui-body section-lead">
        Ugyanakkor nem minden nem standard telek kizárt: a mély csőkilépés, a magas talajvíz és
        a lejtés egy része kezelhető eltérő telepítési kialakítással.
      </p>
      {hiany('az A.B. Clear típusonkénti csőszint- és magasítási határai; az átemelős és a magas talajvizes telepítések tapasztalata; a valós szikkasztási konfigurációk; az elutasított telekhelyzetek; a pótköltséget okozó leggyakoribb adottságok.', 'ÖkoTech telekfelmérési jegyzőkönyvek')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'Mekkora rendszer kell?',
                ['A kapacitás nem a lakók számából következik egyenesen — a vízfogyasztás, a '
                 'csúcsok és a várható változás is számít.'],
                'Kapacitás és létszám', 'kapacitas-es-letszam',
                alt=('Vagy a teljes projekt költsége', 'koltseg-es-telepites')),
    ]


def cs_kapacitas():
    return [
        sec_prose('A gyakori félreértés', '„Négyen lakunk, tehát négyszemélyes kell"', [
            'A kapacitás nem a lakók számából következik egyenesen. A méretezés a '
            '<strong>mértékadó terhelésre</strong> történik, amit a tényleges vízfogyasztás, a '
            'használati intenzitás és a várható változás együtt ad.',
            'Ezért négy dolgot külön kell kezelni: az <strong>állandó lakók</strong> számát, a '
            '<strong>rendszeresen jelen lévő</strong> személyeket, az <strong>alkalmi '
            'vendégcsúcsot</strong>, és a <strong>jövőben várható tartós bővülést</strong>.']),
        sec_split('Két hiba', 'Az alul- és a túlméretezés is kockázat',
                  'Ha tartósan alulméretezett',
                  ['a rendszer nem tudja tartani a tisztítási hatásfokot;',
                   'a terhelés a berendezést is jobban igénybe veszi;',
                   '<strong>az utólagos bővítés lényegesen drágább</strong>, mint az induláskor '
                   'egy fokozattal nagyobb kapacitás.'],
                  'Ha indokolatlanul túlméretezett',
                  ['a biológiai folyamat a tényleges terheléshez igazodik;',
                   'a tartósan alacsony terhelés a hatásfokot is befolyásolja;',
                   '<strong>a beruházás és a helyigény</strong> fölöslegesen nő.']),
        f'''
  <section class="section" aria-labelledby="csucs-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Vendégcsúcs</p>
        <h2 class="type-display-section-title section-title" id="csucs-cim">
          A karácsonyi vendégsereg nem feltétlenül méretezési alap
        </h2>
      </header>
      <p class="type-ui-body section-lead">
        Egy néhány napos vendégterhelés nem feltétlenül indokol a maximális pillanatnyi
        létszámra választott nagyobb berendezést. A rendszerek elviselnek rövid ideig tartó
        többletterhelést — <strong>a mértéket és az időtartamot azonban modellenként kell
        megadni</strong>, nem általános szabályként.
      </p>
      <!-- SZAKMAI VALIDÁCIÓRA VÁR: a jelenlegi GYIK 2–3 napig 150%-os terhelést
           kommunikál általánosan. Az ELV megmarad (a rövid csúcs nem feltétlenül
           indokol nagyobb berendezést), a SZÁM nem publikálható addig, amíg
           modellenként, vizsgálattal vagy üzemi tapasztalattal nincs alátámasztva.
           Egy téves méretezési szabály évtizedes döntést ront el. -->
      <p class="type-ui-body section-lead">
        Az Ön esetére a méretezésnél mondjuk meg, mennyi csúcsot bír el a szóba jövő
        konfiguráció.
      </p>
      {hiany('az A.B. Clear aktuális modell- és kapacitásmátrixa; minden modell névleges terhelési határa; a rövid túlterhelés validált mértéke és időtartama; az alulterhelési működés; a családi házak valós fogyasztási adatai; mikor választanak egy mérettel nagyobb rendszert; a szakértői méretezési döntési szabályok.', 'ÖkoTech műszaki vezetés + vizsgálati adat')}
    </div>
  </section>
''',
        sec_numbered('Adatforrás', 'Meglévő háznál mérhető, új építésnél becsülni kell', None,
                     ['<strong>Meglévő háznál</strong> a vízszámla éves vagy havi fogyasztása '
                      'sokkal jobb alap, mint a névleges létszám — ez tényleges adat.',
                      '<strong>Új építésnél</strong> nincs fogyasztási előzmény: a háztartás '
                      'összetételét, a tervezett használatot és a várható bővülést kell '
                      'strukturáltan rögzíteni.',
                      '<strong>A home office nem létszám</strong>, hanem használati intenzitás — '
                      'a napközbeni jelenlét a fogyasztást növeli.',
                      '<strong>Az eredmény tartomány, nem modell.</strong> A végleges '
                      'konfigurációt jóváhagyott méretezés adja, határhelyzetben szakértői '
                      'ellenőrzéssel.']),
        sec_cta('Következő lépés', 'Miből áll a teljes projekt?',
                ['A berendezés ára ritkán a legnagyobb tétel. A következő oldal végigveszi, mi '
                 'tartozik még hozzá, és ki mit vállal.'],
                'Költség és telepítés', 'koltseg-es-telepites'),
    ]


def cs_koltseg():
    return [
        sec_prose('A kérdés átfogalmazása', '„Mennyibe kerül a szennyvíztisztító?"', [
            'Erre nincs egyetlen szám, mert a projekt nem azonos a berendezéssel. A telek '
            'adottságai és az igényelt szolgáltatási kör több további elemet hoznak magukkal — '
            'és ezek gyakran nagyobb tételek, mint maga a tartály.',
            'Ezért itt <strong>költségszerkezetet</strong> mutatunk, nem árat: azt, hogy mely '
            'tételeket kell az ajánlatban keresnie, és melyik telekadaton múlik még a pontos '
            'összeg.']),
        sec_numbered('Költségszerkezet', 'Amiből a projekt összeáll', None,
                     ['<strong>Berendezés és szállítás.</strong>',
                      '<strong>Földmunka és beemelés.</strong> A talaj kötöttsége és a kitermelt '
                      'föld elhelyezése mozgatja.',
                      '<strong>Csővezetékek és elektromos előkészítés.</strong>',
                      '<strong>Magasítás vagy átemelő</strong>, ha a csőszint megkívánja.',
                      '<strong>A kezelt víz elhelyezése.</strong> Szikkasztómező vagy a befogadóig '
                      'vezető szakasz — talajtípustól és távolságtól függően eltérő nagyságrend.',
                      '<strong>Beüzemelés és dokumentáció.</strong>',
                      '<strong>A régi rendszer kezelése</strong>, ha van ilyen a telken.',
                      '<strong>Üzemeltetés.</strong> Áram, karbantartás, kopó alkatrész — ezek '
                      'nélkül két ajánlat nem hasonlítható össze.']),
        sec_split('Felelősség', 'Ki mit végez',
                  'Amit tőlünk kérhet',
                  ['a berendezés szállítása és beemelése;',
                   'a telepítés és a csatlakozások kialakítása;',
                   'a beüzemelés és az átadás;',
                   'a műszaki dokumentáció;',
                   'a későbbi szervizháttér.'],
                  'Amit saját kivitelezővel is elvégeztethet',
                  ['a földmunka;',
                   'az elektromos előkészítés;',
                   'a helyszín előkészítése a szállítás napjára;',
                   '<strong>ilyenkor a felelősségi határokat előre tisztázni kell</strong> — '
                   'ez utólag a leggyakoribb vitaforrás.']),
        f'''
  <section class="section" aria-labelledby="uzem-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Üzemeltetés</p>
        <h2 class="type-display-section-title section-title" id="uzem-cim">
          Ami a tulajdonosnál marad
        </h2>
      </header>
      <p class="type-ui-body section-lead">
        Az iszapzsákos technológiánál <strong>nincs rendszeres szippantás</strong> — ez valós
        előny. Ettől azonban nem lesz „nincs vele teendő" rendszer, és jobb ezt vásárlás előtt
        tudni, mint utána.
      </p>
      <p class="type-ui-body section-lead">
        Marad: az <strong>iszapzsák kezelése</strong> és a fölösiszap komposztálása, a
        <strong>rendszeres ellenőrzés</strong>, a <strong>membrán és a kompresszor</strong>
        mint kopó elem, és a <strong>szellőzés átnézése</strong>. Rendkívüli helyzetben —
        például tartós túlterhelés vagy meghibásodás után — külső beavatkozás is szükséges lehet.
      </p>
      {hiany('az iszapzsák kezelésének tényleges gyakorisága és időráfordítása; a membrán és a kompresszor valós cseregyakorisága; mely rendkívüli helyzetekben van szükség külső beavatkozásra; a családi házas projektek tényleges teljes költségsávjai; az ajánlat és a végszámla eltérésének okai.', 'ÖkoTech szerviz- és ajánlati nyilvántartás')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'Készen áll az ajánlatkérésre?',
                ['Nem a tartalom elolvasása teszi a projektet ajánlatkérésre késszé, hanem az '
                 'adatok. A következő oldal ezt ellenőrzi.'],
                'Ajánlatkérési készültség', 'ajanlatkeresi-keszultseg'),
    ]


def cs_keszultseg():
    return [
        sec_prose('Mit ellenőriz', 'Előbb az adatok, utána a kapcsolatfelvétel', [
            'Ez nem ajánlatkérő űrlap. Azt nézi meg, hogy rendelkezik-e olyan adatcsomaggal, '
            'amelyből <strong>személyre szabott és összehasonlítható</strong> ajánlat készíthető.',
            'Kapcsolati adatot csak az eredmény után kérünk — és amit addig megadott, azzal '
            'együtt jut el a szakértőhöz, hogy ne kelljen ugyanazt telefonon újra összeszedni.']),
        sec_numbered('A minimális adatcsomag', 'Amiből felelős ajánlat készíthető', None,
                     ['<strong>Új vagy meglévő családi ház</strong>, és a település.',
                      '<strong>Közcsatornahelyzet</strong> — hivatalos tájékoztatás alapján.',
                      '<strong>Állandó létszám és vendégcsúcs</strong>, illetve a vízfogyasztás, '
                      'ha ismert.',
                      '<strong>Talaj és talajvíz</strong> — vagy annak jelzése, hogy nem ismert.',
                      '<strong>A szennyvízcső kilépési mélysége.</strong> Új építésnél a gépész '
                      'tervezőtől; meglévő háznál kiásással.',
                      '<strong>A kezelt víz tervezett elhelyezése</strong> és a telepítés '
                      'lehetséges helye.',
                      '<strong>Kivitelezési igény</strong> — mit kér tőlünk, mit végez saját '
                      'kivitelező.']),
        sec_numbered('Három eredmény', 'És mindegyik értelmes folytatás', None,
                     ['<strong>Ajánlatkérésre kész.</strong> A kritikus adatok megvannak.',
                      '<strong>Néhány adat még hiányzik.</strong> Megnevezzük, melyik, és honnan '
                      'szerezhető meg. Ez a leggyakoribb eredmény.',
                      '<strong>Helyszíni vagy szakértői felmérés szükséges.</strong> Egy vagy '
                      'több kérdésre csak a helyszínen van válasz.']),
        f'''
  <section class="section" aria-labelledby="modul-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">A modul</p>
        <h2 class="type-display-section-title section-title" id="modul-cim">A készültség-ellenőrző</h2>
      </header>
      <aside class="panel">
        <p class="type-ui-body"><strong>Az ellenőrző még nem él.</strong> Azt, hogy mely adat
          nélkül nem készíthető felelős ajánlat, korábbi ajánlatkérések elemzéséből kell
          megállapítani — nem feltevésből.</p>
        <p class="type-ui-body">Addig írja le a helyzetét, és megmondjuk, mi hiányzik:
          <a href="../kapcsolat">Kapcsolatfelvétel</a>.</p>
      </aside>
      {hiany('100–200 korábbi családi házas ajánlatkérés elemzése; az első válasz előtti visszakérdezések; mely mező hiányzik a leggyakrabban; mely adat nélkül nem készíthető felelős ajánlat; mikor kötelező helyszíni felmérés; melyik input dönti el a konfigurációt és melyik csak a költséget módosítja.', 'ÖkoTech ajánlati archívum')}
    </div>
  </section>
''',
        sec_cta('Addig is', 'Nem kell mindent tudnia',
                ['A település neve, a háztartás létszáma és az, amit a telekről tud — ennyivel '
                 'már értelmes beszélgetést tudunk kezdeni.',
                 'Ha kiderül, hogy még korai az ajánlatkérés, azt is megmondjuk.'],
                'Kapcsolatfelvétel', '../kapcsolat'),
    ]


NY = [('Nyaraló, szezonális', 'nyaralo-vagy-szezonalisan-hasznalt-ingatlan')]
CS = [('Családi ház', 'csaladi-hazhoz-keresek-rendszert')]
ALAP = [('Főoldal', '../'), ('Helyzetem', './')]

OLDALAK = [
    ('mit-jelent-az-idoszakos-terheles', 'Mit jelent az időszakos terhelés?', 'nyaralo',
     'Ugyanaz a létszám háromféle terhelést jelenthet. A használati mintázat írja le, nem a '
     'személyszám — és a leghosszabb kihagyás a legerősebb szűrő.',
     'Bezárt magyar hétvégi ház késő ősszel, csukott zsalukkal, a nyíratlan gyepben látszó '
     'aknafedlappal', NY, n_terheles),
    ('biologiai-rendszer-vagy-oldomedence', 'Biológiai rendszer vagy oldómedence?', 'attekintes',
     'A „nyaraló = oldómedence" túl egyszerű. A kritikus változó a kihagyás hossza és '
     'ismétlődése — nem maga a szezonalitás.',
     'Talajmetszet egy kerti tisztítórendszerrel: ülepítő, biológiai egység és kavicságyas '
     'elszivárogtatás egymás után', NY, n_valasztas),
    ('hosszabb-tavollet-es-ujrainditas', 'Hosszabb távollét és újraindítás', 'oldomedence',
     'Mit tegyen az utolsó használati napon és az elsőn, amikor visszatér — és mi az, amihez '
     'már szakember kell.',
     'Talajmetszet egy erdőszéli ház előtt: oldómedence és kavicsos elszivárogtató mező',
     NY, n_tavollet),
    ('szezonalis-esettanulmanyok', 'Szezonális esettanulmányok', 'helyzetem',
     'Szezonális ingatlannál a vásárlási kockázat a többéves működés. Ezért a hasonló használati '
     'mintájú, dokumentált esetek mondják a legtöbbet — nem a fotók.',
     'Magyar falu széle naplementében: különböző korú családi házak földút mentén, az egyik '
     'gyepben tisztítóakna fedlapja', NY, n_esetek),
    ('hasznalati-profil', 'Használati profil elkészítése', 'nyaralo',
     'A „nyaraló, 4 fő" túl kevés a döntéshez. Az éves használati mintázatból terhelési profil '
     'lesz — abból pedig kiderül, mely irányok maradnak relevánsak.',
     'Bezárt magyar hétvégi ház késő ősszel, csukott zsalukkal, a nyíratlan gyepben látszó '
     'aknafedlappal', NY, n_profil),

    ('megoldastipus-kivalasztasa', 'Megoldástípus kiválasztása', 'biologiai',
     'Az állandó használat mellett az aktív biológiai irány természetes kiindulópont — de nem '
     'automatikus végkövetkeztetés. A telek felülírhatja.',
     'Talajmetszet egy családi ház kertje alatt: hengeres biológiai tisztítótartály belső '
     'terekkel és aknafedlapokkal', CS, cs_megoldas),
    ('telekalkalmassag', 'Telekalkalmasság', 'telekvasarlas',
     'A csőszint, a talajvíz és a vízelhelyezés összefüggő feltétel. És a telekalkalmasság nem '
     'termékalkalmasság — a kettő nem ugyanaz.',
     'Üres füves építési telek kitűzőcövekekkel és zsinórral, előtérben nyitott talajvizsgálati '
     'gödör a rétegekkel', CS, cs_telek),
    ('kapacitas-es-letszam', 'Kapacitás és létszám', 'csaladi-haz',
     'A kapacitás nem a lakók számából következik egyenesen. Az alul- és a túlméretezés is '
     'kockázat, és a vendégcsúcs nem feltétlenül méretezési alap.',
     'Modern földszintes családi ház gondozott kerttel, a gyepben két diszkrét aknafedlap',
     CS, cs_kapacitas),
    ('koltseg-es-telepites', 'Költség és telepítés', 'kapcsolat',
     'A projekt nem azonos a berendezéssel. Költségszerkezet, felelősségi határok — és az, ami '
     'az iszapzsákos rendszernél is a tulajdonosnál marad.',
     'Helyszíni felmérés eszközei egy jármű raktere mellett: összehajtott műszaki rajz, '
     'jegyzetfüzet, colstok és talajmintavevő zacskó', CS, cs_koltseg),
    ('ajanlatkeresi-keszultseg', 'Ajánlatkérési készültség', 'mar-van-rendszerem',
     'Nem a tartalom elolvasása teszi a projektet ajánlatkérésre késszé, hanem az adatok. '
     'Kapcsolati adatot csak az eredmény után kérünk.',
     'Szervizre nyitott biológiai tisztító akna gondozott kertben, mellette kompresszorszekrény '
     'és kiterített szerszámok', CS, cs_keszultseg),
]

if __name__ == '__main__':
    for slug, cim, kep, lead, alt, szulo, epito in OLDALAK:
        o = dict(
            file=f'helyzetem/{slug}.html', url=f'helyzetem/{slug}', img=kep,
            title=f'{cim} | ÖkoTech Home', desc=lead, h1=cim, alt=alt, lead=lead,
            crumbs=ALAP + [szulo[0]], sections=epito())
        out = WEB / o['file']
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:52s} {len(out.read_text(encoding='utf-8'))//1024} KB")
