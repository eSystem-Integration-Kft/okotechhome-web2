#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helyzetem → Nincs elérhető közcsatorna — a sitemap szerinti négy aloldal.

A tartalmi brief alapján. Négy szabály végig érvényes:

1. NINCS KONKRÉT ÁR. Csak költségTÍPUS és összehasonlítási logika. A régi oldal
   havi költség- és megtérülési számai NEM kerülnek át.
2. A „NEM TUDOM" ÉRVÉNYES VÁLASZ. Az adatlapnál minden tételnél szerepel, hogy
   honnan tudható meg, becsülhető-e vagy mérni kell, és mi a teendő, ha hiányzik.
3. AZ AJÁNLATKÉRÉS NEM MINDEN OLDAL VÉGPONTJA. Legitim eredmény a további
   adatgyűjtés, a telekellenőrzés, a helyszíni felmérés — vagy más megoldás.
4. A JOGI TARTALOM AVUL. A „Közcsatorna vagy egyedi rendszer?" a hub
   leggyorsabban avuló oldala: dátumozás és szakmai tartalomgazda nélkül nem
   publikálható. Ezt az oldal maga is kiírja.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import sec_numbered, sec_split, sec_prose, sec_cta, sec_faq

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'
JOGI = ('<!-- JOGI ELLENŐRZÉS PUBLIKÁLÁS ELŐTT: a 147/2010. (IV. 29.) Korm. rendeletre\n'
        '     hivatkozó állítás. A brief kötelező friss ellenőrzést ír elő minden kiadás\n'
        '     előtt, és ehhez az oldalhoz szakmai tartalomgazdát is. -->')


def hiany(mi, honnan):
    return f'<!-- ADATHIÁNY: {mi}\n     Forrás: {honnan}. Addig konkrét értékkel nem publikálható. -->'


# ---------------------------------------------------- 2. adatok összegyűjtése
ADATOK = [
    ('Ingatlan és használat', [
        ('Ingatlantípus és projektfázis',
         'Ez dönti el, milyen kérdések relevánsak. Telekvásárlás előtt más adat áll '
         'rendelkezésre, mint kész háznál.', 'Ön tudja', 'megadható'),
        ('Állandó vagy időszakos használat',
         'A biológiai tisztítás rendszeres terhelést kíván; a hosszú szünet a '
         'technológiaválasztást írja felül.', 'Ön tudja', 'megadható'),
        ('Normál és maximális létszám',
         'A méretezés a mértékadó terhelésre készül, nem az átlagra.',
         'Ön tudja', 'megadható'),
        ('Vízfogyasztás, ha ismert',
         'A számlából kiolvasva pontosabb alap, mint a létszámból becsült érték.',
         'vízszámla vagy szolgáltatói kimutatás', 'dokumentumból'),
        ('Várható bővítés',
         'Az utólagos bővítés lényegesen drágább, mint az induláskor eggyel nagyobb kapacitás.',
         'Ön tudja', 'megadható'),
    ]),
    ('Közmű és jogi alaphelyzet', [
        ('Település és pontos cím',
         'A helyi előírások és a védettségi besorolás ettől függ.', 'Ön tudja', 'megadható'),
        ('A közcsatorna tényleges elérhetősége',
         'Nem az a kérdés, van-e cső az utcában, hanem hogy műszakilag elérhető-e, és van-e '
         'hozzá tisztítótelepi kapacitás.',
         'a területi víziközmű-szolgáltató és az önkormányzat', 'hivatalos tájékoztatás kell'),
        ('Szolgáltatói nyilatkozat, ha van',
         'Ez az egyetlen dokumentum, ami a közcsatornahelyzetet bizonyítja.',
         'víziközmű-szolgáltató', 'dokumentumból'),
    ]),
    ('Telek', [
        ('Telekméret és szabad terület',
         'A tisztítómező és a kezelt víz elhelyezése ezen múlik.',
         'tulajdoni lap, térképmásolat vagy helyszínrajz', 'dokumentumból'),
        ('Lejtésviszonyok',
         'A gravitációs levezetés lehetőségét dönti el.', 'a telken megfigyelhető', 'becsülhető'),
        ('Ásott és fúrt kutak — a sajátja és a szomszédoké',
         'A védőtávolságok szűkítik a beépíthető sávot.',
         'helyszíni bejárás, szomszédok, kút adatlapja', 'megfigyelhető'),
        ('Gépi megközelíthetőség',
         'A telepítéshez gép, a későbbi iszapelszállításhoz szippantóautó kell.',
         'a telken megfigyelhető', 'megfigyelhető'),
    ]),
    ('Műszaki adatok', [
        ('A szennyvízcső kilépési helye és mélysége',
         'Ez dönti el, gravitációsan megoldható-e a bekötés, vagy átemelő is kell. '
         'Meglévő háznál ez a leggyakrabban hiányzó adat.',
         'kiásással vagy tervrajzból', 'mérendő'),
        ('Talajvízszint',
         'Nem az aktuális, hanem a mértékadó, évszakos maximum számít.',
         'talajmechanikai szakvélemény, fúrt kút adatlapja, szomszédok tapasztalata',
         'mérendő'),
        ('Talajtípus és vízáteresztő képesség',
         'A szikkasztás lehetőségét és a szükséges területet határozza meg.',
         'talajmechanikai szakvélemény', 'mérendő'),
        ('A kezelt víz tervezett elhelyezése',
         'A projekt leggyakoribb szűk keresztmetszete. Talajba szikkasztás, felszíni befogadó '
         'vagy hasznosítás — legalább az egyiknek működnie kell.',
         'helyszíni bejárás és a helyi előírások', 'vizsgálandó'),
    ]),
    ('Dokumentumok', [
        ('Helyszínrajz vagy tervrajz', 'A telepítés helyének kijelöléséhez.',
         'tervező, korábbi építési dokumentáció', 'dokumentumból'),
        ('Fotók a telekről', 'Sok kérdést kivált — a megközelíthetőséget és a terepviszonyokat '
         'képen gyorsabb megmutatni, mint leírni.', 'Ön készíti', 'megadható'),
        ('Meglévő rendszer adatai', 'Kiváltásnál a régi műtárgy típusa, mérete és mélysége.',
         'saját dokumentáció vagy helyszíni megnézés', 'megfigyelhető'),
        ('Korábbi engedély vagy közműnyilatkozat', 'Ha van, jelentősen gyorsítja az eljárást.',
         'saját irattár', 'dokumentumból'),
    ]),
]


def epit_lehetosegek():
    return [
        sec_prose('A döntési tér', 'Négy irány, nem egy termék', [
            'Ha az ingatlan nem köthető közcsatornára, a szennyvizet helyben kell megoldani — '
            'de ez nem egyetlen megoldást jelent. Négy irány létezik, és mindegyiknek más a '
            'feltétele.',
            'A választást nem a berendezés dönti el, hanem az ingatlan használata, a várható '
            'terhelés, a telek, a talaj- és talajvízviszonyok, a kezelt víz elhelyezése és a '
            'helyi szabályozás — együtt.']),
        sec_numbered('Lehetőségek', 'Mi jöhet szóba, és mi a feltétele',
                     'A sorrend nem rangsor. Mindegyiknél az szerepel, mit csinál, és mi kell '
                     'hozzá, hogy egyáltalán szóba jöjjön.',
                     ['<strong>Aktív biológiai szennyvíztisztító.</strong> Energiabevitellel '
                      'ténylegesen megtisztítja a szennyvizet. Feltétele a folyamatos '
                      'áramellátás, a rendszeres terhelés és a kezelt víz elhelyezhetősége. '
                      'Rendszeres, de kis munkaigényű üzemeltetést kíván.',
                      '<strong>Tisztítómezővel működő oldómedencés rendszer.</strong> Az '
                      'oldómedence előkezel, a tisztítás nagy része a talajban zajlik. Áram nem '
                      'kell hozzá, viszont a tisztítómező területigénye jelentős, és a talaj '
                      'vízáteresztő képessége meghatározó.',
                      '<strong>Zárt szennyvíztároló.</strong> Nem kezel, csak gyűjt: a teljes '
                      'mennyiséget el kell szállíttatni. Ott van a helye, ahol a helyi adottságok '
                      'semmilyen talajba jutást nem engednek. <strong>Ezt nem mi gyártjuk</strong>, '
                      'de megmondjuk, ha ez a helyzet.',
                      '<strong>A közcsatorna újbóli ellenőrzése vagy a kivárás.</strong> Ha a '
                      'hálózat műszakilag mégis elérhető, vagy a kiépítése ütemezett és a dátum '
                      'ismert, egy párhuzamos beruházás nehezen indokolható.']),
        sec_split('Használat', 'Mi billenti az egyik vagy a másik irányba',
                  'Az aktív biológiai irány felé billen, ha…',
                  ['<strong>életvitelszerű a használat</strong>, tehát a terhelés rendszeres;',
                   '<strong>korlátozott a szabad terület</strong> — a tisztítómező itt nem férne el;',
                   '<strong>van folyamatos áramellátás</strong> a telken;',
                   '<strong>a kezelt vizet hasznosítaná</strong>, például öntözésre.'],
                  'Az oldómedencés irány felé billen, ha…',
                  ['<strong>időszakos a használat</strong>, hosszú, terhelés nélküli szakaszokkal;',
                   '<strong>nincs vagy bizonytalan az áramellátás</strong>;',
                   '<strong>jó a talaj vízáteresztő képessége</strong>, és van hely a tisztítómezőnek;',
                   '<strong>a lehető legkevesebb üzemeltetést</strong> szeretné, és elfogadja a '
                   'nagyobb területigényt.']),
        sec_numbered('Költség', 'Mit érdemes összehasonlítani — konkrét ár nélkül',
                     'Végleges árat felmérés nélkül nem lehet felelősen mondani. Az alábbi '
                     'kategóriák viszont mindegyik iránynál összevethetők.',
                     ['<strong>Beruházás.</strong> A berendezés ára mellett a földmunka, a bekötés '
                      'mélysége és a kezelt víz elhelyezése — utóbbiak gyakran nagyobb tételek.',
                      '<strong>Energia.</strong> Az aktív rendszernél folyamatos, a másik kettőnél '
                      'nincs.',
                      '<strong>Elszállítás.</strong> Zárt tárolónál a teljes mennyiség rendszeres '
                      'szippantása; a másik kettőnél időszakos iszapkezelés.',
                      '<strong>Karbantartás és kopó alkatrész.</strong> Az aktív rendszernél '
                      'kompresszor és membrán; a passzívnál nincs mozgó alkatrész.']),
        sec_cta('Következő lépés', 'Egyáltalán választható-e egyedi rendszer?',
                ['Mielőtt technológiát választ, egy kérdést tisztázni kell: a közcsatorna '
                 'ténylegesen elérhetetlen-e. Ez nem az utcában lévő cső kérdése, és nem '
                 'vélemény dolga — hivatalos tájékoztatás dönti el.'],
                'Közcsatorna vagy egyedi rendszer?', 'kozcsatorna-vagy-egyedi-rendszer',
                alt=('Vagy nézze meg, milyen adat kell a döntéshez',
                     'milyen-adatokat-kell-osszegyujteni')),
    ]


def epit_kozcsatorna():
    return [
        f'''
  <section class="section" aria-labelledby="figyelem-cim">
    <div class="section-inner">
      <aside class="panel" aria-labelledby="figyelem-cim">
        <h2 class="type-ui-card-title" id="figyelem-cim">Ez az oldal jogi kérdést érint</h2>
        <p class="type-ui-body">Az alábbi tájékoztatás általános, és a szabályozás változhat.
          A saját ingatlanára vonatkozó választ <strong>a területi víziközmű-szolgáltatótól és
          az illetékes önkormányzattól</strong> kell megkérnie — ezt semmilyen weboldal nem
          helyettesíti, a miénk sem.</p>
      </aside>
      {JOGI}
      {hiany('a hivatkozott jogszabályhelyek pontos megjelölése, a hatályos szöveg és a helyi engedélyezési gyakorlat. Az oldal dátumozás és nevesített szakmai tartalomgazda nélkül nem publikálható.', 'jogi ellenőrzés')}
    </div>
  </section>
''',
        sec_prose('A valódi kérdés', 'Nem az, hogy van-e cső az utcában', [
            'A köznyelvben a „van csatorna" azt jelenti, hogy látszik egy akna a közelben. '
            'A szabályozás viszont más fogalommal dolgozik: a szennyvízelvezető mű '
            '<strong>műszaki elérhetősége</strong> és a megfelelő <strong>tisztítótelepi '
            'kapacitás</strong> együtt számít.',
            'Ez a különbség gyakorlati következménnyel jár: ha mindkettő fennáll, új egyedi '
            'szennyvízkezelő berendezés telepítése nem járható út — nem preferencia kérdése. '
            'Ha viszont nem áll fenn, az egyedi rendszer útja nyitva van.',
            'Ezért a helyes sorrend: <strong>előbb a közcsatornahelyzet tisztázása, utána a '
            'technológiaválasztás.</strong> Fordítva a projekt közepén derül ki, hogy nem '
            'megvalósítható.']),
        sec_numbered('Mit ellenőrizzen', 'Négy kérdés, és kitől kérdezze',
                     'Ezekre hivatalos választ kell kapnia. A szomszéd tapasztalata és a '
                     'hirdetés szövege nem elég.',
                     ['<strong>Műszakilag elérhető-e a szennyvízelvezető mű</strong> az ingatlant '
                      'határoló közterületen? <em>Kérdezze:</em> a területi víziközmű-szolgáltatót.',
                      '<strong>Van-e megfelelő tisztítótelepi kapacitás?</strong> Ez akkor is '
                      'lehet korlát, ha a vezeték fizikailag ott van. <em>Kérdezze:</em> a '
                      'szolgáltatót.',
                      '<strong>Tervezik-e a hálózat kiépítését, és mikor?</strong> Kötelező '
                      'érvényű ütemtervet kérjen, ne szóbeli tájékoztatást. <em>Kérdezze:</em> '
                      'az önkormányzatot.',
                      '<strong>Vonatkozik-e a területre vízbázisvédelmi vagy más korlátozás?</strong> '
                      'Ez minden más szempontot felülírhat. <em>Kérdezze:</em> az illetékes '
                      'hatóságot vagy az önkormányzatot.']),
        sec_numbered('Eredmények', 'Négy kimenet — mindegyik érvényes', None,
                     ['<strong>A közcsatorna nem elérhető.</strong> Az egyedi rendszer útja '
                      'nyitva; a következő feladat a telek és a terhelés adatainak összegyűjtése.',
                      '<strong>A közcsatorna elérhető.</strong> Ilyenkor a rákötés az út. Ezt '
                      'akkor is megmondjuk, ha ez azt jelenti, hogy nem tőlünk vásárol.',
                      '<strong>A kiépítés ütemezett, a dátum ismert.</strong> Érdemes összevetni '
                      'a bekötési és szolgáltatási költséget az egyedi rendszer teljes '
                      'életciklus-költségével. A kivárás legitim döntés.',
                      '<strong>Nincs egyértelmű válasz.</strong> Ez a leggyakoribb kimenet. '
                      'Ilyenkor a következő feladat a hivatalos tájékoztatás beszerzése — '
                      'ebben tudunk segíteni.']),
        sec_numbered('Költség', 'Mit érdemes összevetni — konkrét ár nélkül', None,
                     ['<strong>Közcsatorna oldalán:</strong> bekötési díj, a telken belüli '
                      'vezetékszakasz kiépítése, és a folyamatos szolgáltatási díj.',
                      '<strong>Egyedi rendszer oldalán:</strong> beruházás, földmunka, energia, '
                      'iszapkezelés és karbantartás.',
                      '<strong>Az időtáv dönt.</strong> A szolgáltatási díj évtizedeken át fut; '
                      'az egyedi rendszernél ez elmarad, cserébe üzemeltetési feladat marad. '
                      'A két oldal csak azonos időtávon vethető össze.']),
        sec_cta('Következő lépés', 'Ha az egyedi rendszer útja nyitva',
                ['A következő feladat a saját helyzetének adatait összegyűjteni. Nem kell '
                 'mindent tudnia — az oldal megmutatja, melyik adat honnan szerezhető meg, '
                 'melyik becsülhető, és melyiknél a „nem tudom" is elfogadható válasz.'],
                'Milyen adatokat kell összegyűjteni?', 'milyen-adatokat-kell-osszegyujteni',
                alt=('Vagy beszéljünk róla', '../kapcsolat')),
    ]


def epit_adatok():
    blokkok = ''
    for cim, tetelek in ADATOK:
        sorok = '\n'.join(
            f'''            <tr>
              <th scope="row" class="type-ui-subtitle">{n}</th>
              <td class="type-ui-subtitle">{m}</td>
              <td class="type-ui-subtitle">{h}</td>
              <td class="type-ui-subtitle">{t}</td>
            </tr>''' for n, m, h, t in tetelek)
        aid = cim.lower().replace(' ', '-').replace('é', 'e').replace('á', 'a').replace('í', 'i').replace('ó', 'o').replace('ö', 'o').replace('ű', 'u').replace('ú', 'u').replace('ü', 'u')
        blokkok += f'''
  <section class="section" aria-labelledby="{aid}-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Adatcsoport</p>
        <h2 class="type-display-section-title section-title" id="{aid}-cim">{cim}</h2>
      </header>
      <div class="compare-scroll" role="region" aria-labelledby="{aid}-cim" tabindex="0">
        <table class="compare-table">
          <thead>
            <tr>
              <th scope="col">Adat</th>
              <th scope="col">Miért számít</th>
              <th scope="col">Honnan tudható meg</th>
              <th scope="col">Becsülhető vagy mérendő</th>
            </tr>
          </thead>
          <tbody>
{sorok}
          </tbody>
        </table>
      </div>
    </div>
  </section>
'''
    return [
        sec_prose('Hogyan használja', 'A „nem tudom" is érvényes válasz', [
            'Ez a lista nem vizsga. Az alábbi táblázatokban minden adatnál szerepel, '
            '<strong>miért számít</strong>, <strong>honnan tudható meg</strong>, és hogy '
            '<strong>becsülhető-e vagy mérni kell</strong>.',
            'Ha valamit nem tud, az nem hiba, hanem információ: megmutatja, hogy a következő '
            'lépés dokumentum beszerzése, helyszíni felmérés vagy szakértő bevonása. '
            'A becsült, a dokumentumból származó és a ténylegesen megmért adat nem azonos '
            'megbízhatóságú — ezért másra elég.',
            'A tájékozódáshoz elég a település neve, a használat módja és a létszám. '
            'A többi a méretezésnél és az ajánlatnál válik szükségessé.']),
    ] + [blokkok] + [
        sec_cta('Következő lépés', 'Vigye tovább, amit összeszedett',
                ['Ha az adatok egy része megvan, a helyzetfelmérő végigveszi Önnel, mi az, '
                 'ami már elég a döntéshez, és mi hiányzik még.',
                 'Ha inkább beszélne róla, írja le a helyzetét néhány mondatban — ugyanoda jut.'],
                'Projektindító / helyzetfelmérő', 'projektindito',
                alt=('Vagy írjon nekünk', '../kapcsolat')),
        sec_faq([
            ('Mi van, ha a talajvizet nem ismerem?',
             'Ez a leggyakoribb hiányzó adat, és nem akadály a tájékozódásban. A mértékadó '
             'talajvízszint méréssel állapítható meg; ha az építkezéshez amúgy is készül '
             'talajmechanikai szakvélemény, érdemes kérni, hogy a szennyvízkezelés szempontjait '
             'is vegye bele — egy vizsgálatból két kérdésre kap választ.'),
            ('Meddig érdemes adatot gyűjteni, mielőtt megkeresem Önöket?',
             'Nem kell megvárnia, amíg minden megvan. A település neve, a használat módja és a '
             'létszám elég ahhoz, hogy megmondjuk, mely irányok jöhetnek szóba. A részletes '
             'adatokra a méretezésnél lesz szükség.'),
            ('A becsült adat elég az ajánlathoz?',
             'Nagyságrendi tájékoztatáshoz igen, végleges ajánlathoz nem. A telepítési '
             'körülmények — földmunka, bekötési mélység, vízelhelyezés — mozgatják leginkább a '
             'végösszeget, és ezeket mérni kell, nem becsülni.'),
        ]),
    ]


def epit_projektindito():
    return [
        sec_prose('Mit ad és mit nem', 'Helyzetértékelést ad, nem árajánlatot', [
            'A helyzetfelmérő az általános tudást a saját ingatlanára fordítja le. '
            '<strong>Nem</strong> hoz végleges műszaki döntést, és <strong>nem ad árat</strong>.',
            'Amit ad: mely adatok vannak meg, melyek hiányoznak, mik a fő kockázatok, és mi a '
            'következő értelmes lépés. Az eredmény akkor is hasznos, ha az derül ki, hogy még '
            'nem áll készen az ajánlatkérésre — sőt, főleg akkor.']),
        sec_numbered('Ahogy kérdez', 'Alkalmazkodik ahhoz, amit már tud',
                     'Egy nyaralótulajdonos más kérdéseket kap, mint egy telekvásárló. '
                     'Aki még nem vette meg a telket, nem kap olyan kérdést, amire nem lehet '
                     'válasza.',
                     ['<strong>Hol tart a projektben.</strong> Tájékozódik, telket néz, tervez, '
                      'vagy már ajánlatot kér.',
                      '<strong>Milyen az ingatlan és a használat.</strong> Típus, állandó vagy '
                      'időszakos használat, létszám, csúcsterhelés.',
                      '<strong>Mi a jelenlegi helyzet.</strong> Van-e már rendszer a telken, és '
                      'mit tud a közcsatornáról.',
                      '<strong>Mit tud a telekről.</strong> Terület, talaj, talajvíz, a kezelt '
                      'víz elhelyezése, a cső mélysége — amennyit tud.',
                      '<strong>Amit nem tud.</strong> A „nem tudom" külön válasz, nem üresen '
                      'hagyott mező: ebből lesz a hiányzó adatok listája.']),
        sec_numbered('Az eredmény', 'Öt kimenet, és mindegyik értelmes folytatás', None,
                     ['<strong>Gyűjtse össze ezt az adatot</strong> — konkrét lista arról, mi '
                      'hiányzik és honnan szerezhető meg.',
                      '<strong>Ellenőrizze a telekalkalmasságot</strong> — a telek adottságai '
                      'döntik el, mi valósítható meg.',
                      '<strong>Kérjen helyszíni felmérést</strong> — ha a nyitott kérdésekre csak '
                      'a helyszínen van válasz.',
                      '<strong>Egyeztessen szakértővel</strong> — összetett vagy nem kommunális '
                      'helyzetben.',
                      '<strong>Készen áll az ajánlatkérésre</strong> — ez csak akkor jelenik meg, '
                      'ha tényleg megvan hozzá minden.']),
        f'''
  <section class="section" aria-labelledby="modul-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">A modul</p>
        <h2 class="type-display-section-title section-title" id="modul-cim">A helyzetfelmérő</h2>
      </header>
      <aside class="panel">
        <p class="type-ui-body"><strong>A helyzetfelmérő még nem él.</strong> A döntési
          szabályokat — melyik válasz melyik következő lépést váltja ki, és mikor kell emberi
          szakértő — a cég szakmai vezetésének kell jóváhagynia. Addig nem teszünk ki olyan
          felületet, amely eredményt sugall.</p>
        <p class="type-ui-body">Amíg elkészül, írja le a helyzetét néhány mondatban, és
          ugyanazt átvesszük Önnel: <a href="../kapcsolat">Kapcsolatfelvétel</a>.</p>
      </aside>
      {hiany('a teljes előminősítési döntési fa; mely válaszok változtatják meg ténylegesen a rendszerválasztást; mely válaszok váltják ki a helyszíni felmérést; mi a minimális input egy felelős ajánlathoz; mikor kell tervező, hidrogeológus vagy más szakértő; a jóváhagyott kizárási szabályok. A szabályokat 50–100 korábbi ajánlatkérésen vissza kell tesztelni.', 'ÖkoTech szakmai vezetés + korábbi ajánlatkérések elemzése')}
    </div>
  </section>
''',
        sec_cta('Addig is', 'Beszéljünk a helyzetéről',
                ['Nem kell megvárnia, amíg minden adat megvan. Írja le, hol van az ingatlan, '
                 'hogyan használják, és mit tud a telekről — megmondjuk, mi a következő '
                 'értelmes lépés.',
                 'Akkor is, ha a válasz az, hogy nem a mi rendszerünk a megoldás.'],
                'Kapcsolatfelvétel', '../kapcsolat'),
    ]


CRUMB = [('Főoldal', '../'), ('Helyzetem', './'),
         ('Nincs elérhető közcsatorna', 'nincs-elerheto-kozcsatorna')]

OLDALAK = [
    dict(file='helyzetem/milyen-megoldasi-lehetosegek-vannak.html',
         url='helyzetem/milyen-megoldasi-lehetosegek-vannak', img='attekintes',
         title='Milyen megoldási lehetőségek vannak? — közcsatorna nélküli ingatlan | ÖkoTech Home',
         desc='Négy irány közcsatorna nélküli ingatlanon: aktív biológiai rendszer, oldómedence '
              'tisztítómezővel, zárt tároló, vagy a közcsatorna kivárása — feltételekkel együtt.',
         h1='Milyen megoldási lehetőségek vannak?',
         alt='Talajmetszet egy kerti tisztítórendszerrel: ülepítő, biológiai egység és kavicságyas '
             'elszivárogtatás egymás után',
         lead='Ha nincs közcsatorna, a szennyvizet helyben kell megoldani — de ez nem egyetlen '
              'megoldást jelent. Négy irány létezik, és a választást nem a berendezés dönti el, '
              'hanem az ingatlan, a telek és a helyi szabályozás együtt.',
         crumbs=CRUMB, sections=epit_lehetosegek()),
    dict(file='helyzetem/kozcsatorna-vagy-egyedi-rendszer.html',
         url='helyzetem/kozcsatorna-vagy-egyedi-rendszer', img='kozcsatorna',
         title='Közcsatorna vagy egyedi rendszer? — mit kell előbb tisztázni | ÖkoTech Home',
         desc='Nem az a kérdés, van-e cső az utcában. A műszaki elérhetőség és a tisztítótelepi '
              'kapacitás dönti el, választható-e egyedi rendszer — és kitől kérdezze meg.',
         h1='Közcsatorna vagy egyedi rendszer?',
         alt='Magyar falusi utca, ahol az aszfalt és az utolsó csatornaakna véget ér, tovább '
             'földút és bekötés nélküli családi házak',
         lead='Ezt a kérdést a technológiaválasztás ELŐTT kell tisztázni. Nem vélemény dolga, és '
              'nem az utcában lévő cső dönti el — hivatalos tájékoztatás. Fordított sorrendben a '
              'projekt közepén derül ki, hogy nem megvalósítható.',
         crumbs=CRUMB, sections=epit_kozcsatorna()),
    dict(file='helyzetem/milyen-adatokat-kell-osszegyujteni.html',
         url='helyzetem/milyen-adatokat-kell-osszegyujteni', img='telekvasarlas',
         title='Milyen adatokat kell először összegyűjteni? — ellenőrzőlista | ÖkoTech Home',
         desc='Öt adatcsoport, és mindegyik tételnél: miért számít, honnan tudható meg, '
              'becsülhető-e vagy mérni kell — és mi a teendő, ha nem tudja.',
         h1='Milyen adatokat kell először összegyűjteni?',
         alt='Üres füves építési telek kitűzőcövekekkel és zsinórral, előtérben nyitott '
             'talajvizsgálati gödör a rétegekkel',
         lead='Ez a lista nem vizsga. Minden adatnál szerepel, miért számít, honnan tudható meg, '
              'és hogy becsülhető-e vagy mérni kell. Ha valamit nem tud, az nem hiba — megmutatja, '
              'mi a következő lépés.',
         crumbs=CRUMB, sections=epit_adatok()),
    dict(file='helyzetem/projektindito.html',
         url='helyzetem/projektindito', img='helyzetem',
         title='Projektindító / helyzetfelmérő — mi a következő lépés | ÖkoTech Home',
         desc='Az általános tudás alkalmazása a saját ingatlanra: mi van meg, mi hiányzik, '
              'mik a kockázatok, és mi a következő értelmes lépés. Ár nélkül.',
         h1='Projektindító / helyzetfelmérő',
         alt='Magyar falu széle naplementében: különböző korú családi házak földút mentén, '
             'az egyik gyepben tisztítóakna fedlapja',
         lead='A hub gyakorlati végpontja. Nem hoz végleges műszaki döntést, és nem ad árat — '
              'azt mutatja meg, mi van meg, mi hiányzik, és mi a következő értelmes lépés. '
              'Az is érvényes eredmény, ha még nem áll készen az ajánlatkérésre.',
         crumbs=CRUMB, sections=epit_projektindito()),
]

if __name__ == '__main__':
    for o in OLDALAK:
        out = WEB / o['file']
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:50s} {len(out.read_text(encoding='utf-8'))//1024} KB")
