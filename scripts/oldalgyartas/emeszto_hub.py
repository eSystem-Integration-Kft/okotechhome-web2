#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helyzetem → Meglévő emésztő kiváltása — a sitemap szerinti öt aloldal.

A brief négy dolgot köt ki, és mindegyik érvényes végig:

1. A „NÉGY ÉV KÖRÜLI MEGTÉRÜLÉS" NEM VIHETŐ TOVÁBB általános állításként.
   Egy 2023-as szippantási díjból és egy háromfős példából származik. Helyette
   5/10/15 éves forgatókönyv és érzékenységi vizsgálat — az eredmény nem
   „X év alatt megtérül", hanem költségtartomány + a legfontosabb bizonytalanságok.

2. A ZÁRT TÁROLÓ NEM HIBÁS TECHNOLÓGIA. Jogszabályilag létező megoldás, amelynek
   logikája az összegyűjtés és a rendszeres ártalmatlanítás. A csere indoka mindig
   az adott ingatlanból következik, nem a technológia elítéléséből.

3. A MEGTARTÁS ÉS A KIVÁRÁS LEGITIM EREDMÉNY. Alacsony használat, rövid tervezett
   ingatlanhasználat vagy várható közcsatorna esetén racionális döntés lehet.

4. SZERKEZETI ÁLLAPOTOT NEM DIAGNOSZTIZÁLUNK WEBES KÉRDŐÍVVEL. A tulajdonosnak
   nem kell megítélnie a vízzáróságot vagy a szerkezeti hibát — és nem ígérjük,
   hogy a régi tartály vagy csövezés újrahasználható.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import sec_numbered, sec_split, sec_prose, sec_cta, sec_faq

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'
JOGI = ('<!-- JOGI ELLENŐRZÉS PUBLIKÁLÁS ELŐTT: 147/2010. Korm. rendelet (a zárt\n'
        '     szennyvíztároló fogalma és az ártalmatlanítási kötelezettség) + a helyi,\n'
        '     nem közművel összegyűjtött háztartási szennyvízre vonatkozó önkormányzati\n'
        '     rendelet. Mindkettő gyorsan avuló tartalom. -->')
DIJ = ('<!-- DÍJADAT: helyi szippantási díj, energiaár és kivitelezési költség NEM\n'
       '     égethető statikus szövegbe — településenként eltér és gyorsan avul.\n'
       '     Az ügyfél a saját számlájából adja meg; mi nem használunk országos átlagot. -->')


def hiany(mi, honnan):
    return f'<!-- ADATHIÁNY: {mi}\n     Forrás: {honnan}. Addig konkrét értékkel nem publikálható. -->'


KOLTSEG = [
    ('Meglévő rendszer', [
        ('Szippantás gyakorisága', 'a saját számláiból', 'ez a legnagyobb tétel'),
        ('Helyi szolgáltatási feltételek', 'a szolgáltatótól', 'településenként eltér'),
        ('Kiszállási vagy hozzáférési többlet', 'a szolgáltatótól', 'nehéz megközelítésnél'),
        ('Javítás és karbantartás', 'saját tapasztalat', 'ha volt'),
        ('Hátralévő használati idő', 'Ön tudja', 'ez dönti el az időtávot'),
    ]),
    ('Az új rendszer beruházása', [
        ('Berendezés és szállítás', 'ajánlatból', 'ritkán a legnagyobb tétel'),
        ('Földmunka', 'felmérésből', 'a talaj kötöttsége mozgatja'),
        ('Csövezés és elektromos előkészítés', 'felmérésből', 'a távolságtól függ'),
        ('A kezelt víz elhelyezése', 'felmérésből', 'gyakran a legnagyobb tétel'),
        ('Átemelő, magasítás, betonozás', 'felmérésből', 'csak ha a csőszint megkívánja'),
        ('A régi rendszer kezelése', 'felmérésből', 'kiürítés, megszüntetés'),
        ('Beüzemelés és dokumentáció', 'ajánlatból', ''),
    ]),
    ('Üzemeltetés', [
        ('Energia', 'a berendezés adatlapjából', 'csak aktív rendszernél'),
        ('Rendszeres feladatok', 'a kezelési útmutatóból', ''),
        ('Fogyóeszköz és alkatrész', 'szervizlistából', 'membrán, kompresszor'),
        ('Iszapkezelés', 'a kezelési útmutatóból', ''),
    ]),
]


def epit_mikor():
    return [
        sec_prose('Előbb tisztázzuk', 'A zárt tároló nem hibás technológia', [
            'A köznyelvi „emésztő" nem műszaki fogalom. Először azt kell tudni, mi van '
            'ténylegesen a földben: <strong>zárt, vízzáró szennyvíztároló</strong>, '
            '<strong>oldómedencés rendszer</strong>, vagy valamilyen régebbi, más elven '
            'kialakított műtárgy.',
            'A zárt tároló <strong>jogszabályilag létező, szabályos megoldás</strong>: a logikája '
            'az összegyűjtés és a rendszeres ártalmatlanítás. Nem attól kell lecserélni, mert '
            'rossz technológia — hanem attól, ha az adott ingatlanon a használat, a költség vagy '
            'a műszaki állapot ezt indokolja.',
            'Ezért a csere indoka mindig a saját helyzetéből következik, nem egy általános '
            'állításból.']),
        sec_split('Indokok', 'Mi szól a csere mellett, és mi ellene',
                  'A csere mellett szól, ha…',
                  ['<strong>gyakori a szippantás</strong>, és a szervezése is terhet jelent;',
                   '<strong>a tartály kapacitása kevés</strong> a mostani használathoz;',
                   '<strong>szag, túlfolyás vagy visszaduzzadás</strong> jelentkezik;',
                   '<strong>nőtt vagy nőni fog a háztartás</strong>;',
                   '<strong>amúgy is felújítás vagy kertátalakítás készül</strong> — ilyenkor a '
                   'földmunka egy része megosztható;',
                   '<strong>hosszú távon tervez</strong> az ingatlannal.'],
                  'A megtartás vagy a kivárás is racionális, ha…',
                  ['<strong>alacsony a használat</strong>, és a szippantás ritka;',
                   '<strong>rövid ideig tervezi még használni</strong> az ingatlant;',
                   '<strong>a közcsatorna kiépítése ütemezett</strong>, és a dátum ismert;',
                   '<strong>a rendszer zárt és ép</strong>, az ürítési gyakoriság évek óta '
                   'egyenletes;',
                   '<strong>a probléma egyetlen elemre szűkíthető</strong> — például a fedlapra '
                   'vagy a bekötővezetékre.']),
        f'''
  <section class="section" aria-labelledby="diag-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Amit nem tudunk innen eldönteni</p>
        <h2 class="type-display-section-title section-title" id="diag-cim">
          Szerkezeti állapotot nem diagnosztizálunk kérdőívvel
        </h2>
      </header>
      <p class="type-ui-body section-lead">
        Ha a gyanú <strong>szivárgás, vízzáróság-hiány vagy szerkezeti hiba</strong>, azt sem
        Ön, sem mi nem tudjuk online megítélni. Ehhez helyszíni vizsgálat kell — és ez nem
        udvariassági formula, hanem a felelős válasz határa.
      </p>
      <p class="type-ui-body section-lead">
        Önnek nem kell megítélnie a tartály vízzáróságát vagy szerkezeti állapotát. Amit
        össze tud gyűjteni: fotók, korábbi dokumentumok, a szippantási előzmény és a
        tapasztalt tünetek. A többi a felmérés dolga.
      </p>
      {JOGI}
    </div>
  </section>
''',
        sec_numbered('Eredmény', 'Négyféle következtetés — és egyik sem „vegyen berendezést"',
                     None,
                     ['<strong>Érdemes tovább vizsgálni.</strong> Az indokok megvannak; a '
                      'következő kérdés az, milyen rendszer jöhet helyette.',
                      '<strong>Előbb műszaki felmérés kell.</strong> A tünetek szerkezeti okra '
                      'utalnak, amit a helyszínen kell megnézni.',
                      '<strong>Előbb költséget kell összevetni.</strong> A csere gazdaságilag '
                      'nem egyértelmű — a teljes költséget kell megnézni, nem a szippantási díjat.',
                      '<strong>A csere jelenleg nem egyértelműen indokolt.</strong> Ez is '
                      'érvényes eredmény, és megmondjuk, ha ez a helyzet.']),
        sec_cta('Következő lépés', 'Ha a csere indokolt: mi jöhet helyette?',
                ['Három működési modell közül lehet választani, és nem az ár dönt köztük, hanem '
                 'a használat, a telek és a vállalható üzemeltetés.'],
                'Emésztő, oldómedence vagy biológiai?', 'emeszto-oldomedence-vagy-biologiai',
                alt=('Vagy nézze meg a teljes költséget', 'teljes-koltseg-es-megterules')),
    ]


def epit_technologia():
    return [
        sec_prose('Fogalmak', 'Három működési modell, nem három termék', [
            'A hétköznapi „emésztő" mögött három, jogilag is külön kezelt megoldás áll: a '
            '<strong>zárt szennyvíztároló</strong> összegyűjt és időszakosan elszállíttat; az '
            '<strong>oldómedencés rendszer</strong> energiabevitel nélkül előkezel, és a '
            'tisztítás nagy része a tisztítómezőben zajlik; az <strong>aktív biológiai '
            'szennyvíztisztító</strong> levegőztetett folyamattal ténylegesen megtisztít.',
            'A választás nem a berendezés árából indul, hanem abból, hogy melyik feltételeit '
            'tudja teljesíteni az Ön ingatlana — és melyik üzemeltetési feladatot vállalja el.']),
        sec_numbered('Amit mérlegelni kell', 'Nyolc szempont, mindhárom megoldásra', None,
                     ['<strong>Használat.</strong> Életvitelszerű vagy időszakos — ez a '
                      'legerősebb szűrő.',
                      '<strong>Áramellátás.</strong> Az aktív rendszer folyamatos áramot igényel; '
                      'a másik kettő nem.',
                      '<strong>Telek és talaj.</strong> Az oldómedencés rendszer tisztítómezője '
                      'jelentős területet és megfelelő vízáteresztő képességet kíván.',
                      '<strong>Talajvíz.</strong> A beépítést és a vízelhelyezést egyaránt érinti.',
                      '<strong>A kezelt víz sorsa.</strong> Ha nincs hová mennie, a megoldások '
                      'köre a zárt tárolóra szűkül.',
                      '<strong>Szippantás elfogadhatósága.</strong> Zárt tárolónál ez a működés '
                      'része, nem hiba.',
                      '<strong>Vállalható karbantartás.</strong> Az aktív rendszernél kompresszor '
                      'és membrán kopó elem.',
                      '<strong>Meghibásodási pontok.</strong> Mozgó alkatrész csak az aktív '
                      'rendszerben van.']),
        sec_numbered('Mikor NEM való', 'Minden megoldásnak van olyan helyzet, ahol nem jó', None,
                     ['<strong>A zárt tároló nem jó,</strong> ha a használat intenzív és a '
                      'szippantás gyakorisága vagy szervezése tarthatatlan.',
                      '<strong>Az oldómedencés rendszer nem jó,</strong> ha nincs elég terület a '
                      'tisztítómezőnek, kötött a talaj vagy magas a talajvíz.',
                      '<strong>Az aktív biológiai rendszer nem jó,</strong> ha nincs folyamatos '
                      'áram, vagy ha az ingatlan évente csak néhány alkalommal, hosszú szünetekkel '
                      'használt.']),
        f'''
  <section class="section" aria-labelledby="sajat-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Amit bizonyítanunk kell</p>
        <h2 class="type-display-section-title section-title" id="sajat-cim">
          Az alkalmazási határokat saját adattal támasztjuk alá
        </h2>
      </header>
      <p class="type-ui-body section-lead">
        Ezen a piacon az alkalmazási határokat gyártónként eltérően kommunikálják — ugyanazt a
        technológiát az egyik szereplő szezonális, a másik állandó használatra ajánlja. Ezért a
        saját szabályainkat saját projektadatokkal kell alátámasztanunk, nem versenytársi vagy
        marketingállítással.
      </p>
      {hiany('az A.B. Clear és az EPURECO saját alkalmazási mátrixa; az éves és idényjellegű használati határok; a tényleges szippantási gyakoriságok; a telepítésenkénti szikkasztó-területigény; a karbantartási feladatok és időráfordítás; azok a projektek, ahol az ügyfél eredeti technológiaválasztását megváltoztattuk.', 'ÖkoTech műszaki vezetés + projektnyilvántartás')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'A teljes költség, nem a berendezés ára',
                ['A csere gazdasági döntése nem a szippantási díj és a berendezés vételárának '
                 'összevetése. A következő oldal megmutatja, mi tartozik még hozzá — és hogy '
                 'miért nem adunk „X év alatt megtérül" ígéretet.'],
                'Teljes költség és megtérülés', 'teljes-koltseg-es-megterules',
                alt=('Vagy nézzük meg, mi van most a földben', 'meglevo-rendszer-felmerese')),
    ]


def epit_koltseg():
    blokkok = ''
    for cim, tetelek in KOLTSEG:
        sorok = '\n'.join(
            f'''            <tr>
              <th scope="row" class="type-ui-subtitle">{n}</th>
              <td class="type-ui-subtitle">{h}</td>
              <td class="type-ui-subtitle">{m}</td>
            </tr>''' for n, h, m in tetelek)
        aid = cim.split()[0].lower().replace('é', 'e').replace('ü', 'u').replace('ő', 'o')
        blokkok += f'''
  <section class="section" aria-labelledby="k-{aid}-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Költségoldal</p>
        <h2 class="type-display-section-title section-title" id="k-{aid}-cim">{cim}</h2>
      </header>
      <div class="compare-scroll" role="region" aria-labelledby="k-{aid}-cim" tabindex="0">
        <table class="compare-table">
          <thead>
            <tr>
              <th scope="col">Tétel</th>
              <th scope="col">Honnan derül ki</th>
              <th scope="col">Megjegyzés</th>
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
        f'''
  <section class="section" aria-labelledby="nincs-cim">
    <div class="section-inner">
      <aside class="panel" aria-labelledby="nincs-cim">
        <h2 class="type-ui-card-title" id="nincs-cim">Miért nem mondunk megtérülési évszámot</h2>
        <p class="type-ui-body">Egy „négy év alatt megtérül" típusú állítás mindig egy konkrét
          háztartásra, egy adott évi szippantási díjra és egy adott telepítési helyzetre
          érvényes. Általános ígéretként megtévesztő: a szippantási díj településenként eltér és
          évente változik, a telepítési költséget pedig a földmunka és a vízelhelyezés mozgatja.</p>
        <p class="type-ui-body">Ezért itt <strong>költségtartományt és bizonytalanságokat</strong>
          mutatunk, nem megtérülési évszámot — és megnevezzük azokat az adatokat, amelyek nélkül
          még nem lehet felelős gazdasági következtetést levonni.</p>
      </aside>
      {DIJ}
    </div>
  </section>
''',
        sec_prose('A módszer', 'Teljes életciklus, nem beruházási ár', [
            'A csere pénzügyi döntése nem a régi rendszer éves szippantási díjának és az új '
            'berendezés vételárának összevetése. Mindkét oldalon több tétel van — és a '
            'legnagyobbak nem ott vannak, ahol elsőre keresnénk.',
            'A helyes megközelítés <strong>5, 10 és 15 éves forgatókönyv</strong>, '
            'érzékenységi vizsgálattal: mi történik az eredménnyel, ha a szippantás gyakorisága, '
            'az energiaár, a háztartás létszáma vagy a szükséges kiegészítő munka változik.',
            'A <strong>hátralévő használati idő</strong> is bemenet: aki öt évig tervez még az '
            'ingatlannal, más eredményt kap, mint aki huszonötig.']),
    ] + [blokkok] + [
        sec_numbered('Az eredmény', 'Mit adhat egy ilyen számítás — és mit nem', None,
                     ['<strong>Költségtartomány</strong>, nem egyetlen szám.',
                      '<strong>A legfontosabb bizonytalanságok megnevezve</strong> — jellemzően '
                      'a földmunka mennyisége és a vízelhelyezés módja.',
                      '<strong>A hiányzó adatok listája</strong>, amelyek nélkül a következtetés '
                      'nem felelős.',
                      '<strong>Nincs garantált megtérülés.</strong> Ha valaki évszámot ígér az '
                      'Ön adatainak ismerete nélkül, azt érdemes fenntartással kezelni.']),
        sec_cta('Következő lépés', 'A számokhoz adat kell',
                ['A költségtartomány pontossága a telek- és műszaki adatok minőségén múlik. '
                 'A következő lépés a meglévő rendszer és a telek felmérése.'],
                'Meglévő rendszer felmérése', 'meglevo-rendszer-felmerese',
                alt=('Vagy állítsa össze a projektbriefet', 'koltseg-es-projektbrief')),
    ]


def epit_felmeres():
    return [
        sec_prose('Miért más ez, mint egy új építés', 'Már van valami a földben', [
            'Az emésztőkiváltás nem ugyanaz a projekt, mint egy új házhoz telepített rendszer. '
            'Itt már van egy <strong>részben vagy egyáltalán nem ismert föld alatti '
            'rendszer</strong>, meglévő csőhálózat és kialakult telekhasználat — és ezek '
            'mindegyike befolyásolja a kivitelezést.',
            'A felmérés célja ezért nem csak az új rendszer megtervezése, hanem a <strong>kiinduló '
            'állapot rögzítése</strong>: mi ismert, mi bizonytalan, és mi az, amit a helyszínen '
            'kell megnézni.']),
        sec_split('Előkészítés', 'Mit gyűjthet össze Ön — és mit ne ítéljen meg',
                  'Amit Ön elő tud készíteni',
                  ['<strong>fotók</strong> a fedlapról, a környezetéről és a megközelítésről;',
                   '<strong>korábbi dokumentumok</strong>, ha vannak;',
                   '<strong>szippantási előzmény</strong> — milyen gyakran és ki végzi;',
                   '<strong>a tapasztalt tünetek</strong>: szag, túlfolyás, visszaduzzadás;',
                   '<strong>egy egyszerű helyszínrajz</strong> — hol van a műtárgy és a ház;',
                   '<strong>a telepítés becsült éve</strong>, ha tudja.'],
                  'Amit NE Önnek kelljen megítélnie',
                  ['<strong>a szerkezeti állapot</strong> — repedés, süllyedés, elöregedés;',
                   '<strong>a vízzáróság</strong> — ez vizsgálat kérdése;',
                   '<strong>a környezetvédelmi megfelelőség</strong>;',
                   '<strong>hogy megtartható-e bármely elem</strong> az új kialakításban;',
                   '<strong>a tartály belseje</strong> — a régi aknák megnyitása veszélyes, '
                   'ne másszon bele és ne hajoljon fölé.']),
        sec_numbered('A helyszínen', 'Mit nézünk meg', None,
                     ['<strong>A meglévő műtárgy</strong> típusa, anyaga, becsült mérete, helye '
                      'és hozzáférhetősége.',
                      '<strong>A házból érkező cső szintje.</strong> Ez határozza meg az új '
                      'berendezés elhelyezési mélységét, és azt, kell-e magasítás vagy átemelő.',
                      '<strong>A rendelkezésre álló terület</strong> az új tartálynak és a kezelt '
                      'víz elhelyezésének.',
                      '<strong>A talaj és a látható vízviszonyok.</strong>',
                      '<strong>A megközelíthetőség</strong> telepítéshez és későbbi szervizhez.',
                      '<strong>Az átállás menete</strong> — hogyan marad használható az ingatlan '
                      'a munka alatt.']),
        f'''
  <section class="section" aria-labelledby="regi-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">A régi rendszer sorsa</p>
        <h2 class="type-display-section-title section-title" id="regi-cim">
          Nem ígérjük, hogy bármi újrahasználható
        </h2>
      </header>
      <p class="type-ui-body section-lead">
        Előfordul, hogy a meglévő csőhálózat egy része vagy maga a műtárgy más funkcióban
        megtartható — de ezt <strong>csak a tényleges állapot ismeretében</strong> lehet
        eldönteni. Amíg nem láttuk, nem ígérjük.
      </p>
      <p class="type-ui-body section-lead">
        A régi műtárgy megszüntetése a projekt része és költségtétel: a kiürítés, a
        betömedékelés vagy az elbontás módja engedélyezési kérdés is lehet.
      </p>
      {JOGI}
      {hiany('a felmérési jegyzőkönyvek gyakorlata: mit mérnek és mit csak megfigyelnek; milyen régi rendszereket találnak leggyakrabban; mi tartható meg és mi nem; a régi rendszer kezelésének belső műszaki protokollja; a tipikus átállási forgatókönyvek; a gyakori rejtett költségokok; a biztonsági szabályok régi aknák vizsgálatánál.', 'ÖkoTech felmérési gyakorlat')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'Rakjuk össze, ami megvan',
                ['A projektbrief összegyűjti a meglévő rendszer, a telek és a használat adatait — '
                 'ebből már meghatározható a műszaki irány és a költséget mozgató tényezők köre.'],
                'Költség- és projektbrief', 'koltseg-es-projektbrief',
                alt=('Vagy kérjen felmérést', '../kapcsolat')),
    ]


def epit_brief():
    return [
        sec_prose('Mire jó', 'Nem árajánlatkérő', [
            'Ez a brief az előző négy oldal gyakorlati összefoglalója. Nem magyaráz újra semmit — '
            'azokat az adatokat gyűjti össze, amelyekből <strong>felelősen meghatározható a '
            'műszaki irány</strong>, és később a projekt költségtartománya.',
            'Az ajánlatkérés így nem a feltárás kezdete, hanem az összegyűjtött projektadat '
            'természetes következő állapota.']),
        sec_numbered('Amit kérünk', 'Öt blokk — a meglévő rendszerrel kezdve', None,
                     ['<strong>A meglévő rendszer.</strong> Típus, becsült életkor és méret, '
                      'anyag, hely, szippantási gyakoriság, tapasztalt problémák, '
                      'megközelíthetőség.',
                      '<strong>A használat.</strong> Életvitelszerű vagy időszakos, normál és '
                      'maximális létszám, és ha ismert, a vízfogyasztás.',
                      '<strong>A telek.</strong> Helyszín, közcsatornahelyzet, talaj, talajvíz, '
                      'rendelkezésre álló terület, kút, lejtés.',
                      '<strong>A csatlakozás.</strong> A szennyvízcső helye és kifolyási mélysége '
                      '— ez a leggyakrabban hiányzó, de a költséget leginkább mozgató adat.',
                      '<strong>A projekt.</strong> Mikorra tervezi, milyen munkát kér tőlünk, '
                      'van-e saját kivitelezője, és tud-e dokumentumot vagy fotót csatolni.']),
        f'''
  <section class="section" aria-labelledby="minoseg-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Adatminőség</p>
        <h2 class="type-display-section-title section-title" id="minoseg-cim">
          Minden adat háromféle lehet
        </h2>
      </header>
      <p class="type-ui-body section-lead">
        Minden tételnél külön jelöljük, hogy az adat <strong>ismert</strong>,
        <strong>becsült</strong>, vagy <strong>nem tudom</strong>. Ez nem formaság: a
        költségtartomány pontossága közvetlenül ezen múlik.
      </p>
      <p class="type-ui-body section-lead">
        A jelenlegi szippantási terhet is Öntől kérjük — a <strong>saját számlájából</strong>,
        nem országos átlagból. Egy átlagszám ezen a területen félrevezető, mert a díj
        településenként eltér.
      </p>
      {DIJ}
    </div>
  </section>
''',
        sec_numbered('Az eredmény', 'Négy lehetséges kimenet', None,
                     ['<strong>Ajánlatra kész.</strong> A kritikus adatok megvannak, a projekt '
                      'ajánlatba fordítható.',
                      '<strong>Helyszíni felmérést igényel.</strong> Egy vagy több kérdésre csak '
                      'a helyszínen van válasz.',
                      '<strong>További adat szükséges.</strong> Megnevezzük, melyik, és honnan '
                      'szerezhető meg.',
                      '<strong>Más megoldási irányt is érdemes vizsgálni.</strong> Ez is '
                      'eredmény — és megmondjuk, ha ez a helyzet.']),
        f'''
  <section class="section" aria-labelledby="modul-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">A modul</p>
        <h2 class="type-display-section-title section-title" id="modul-cim">A projektbrief</h2>
      </header>
      <aside class="panel">
        <p class="type-ui-body"><strong>A kitölthető brief még készül.</strong> Automatikus
          ársávot csak akkor épít bele értelmesen, ha mögötte van elég saját projektadat —
          addig az ilyen becslés inkább félrevezet, mint segít.</p>
        <p class="type-ui-body">Amíg elkészül, írja meg a helyzetét, és ugyanezeket átvesszük
          Önnel: <a href="../kapcsolat">Kapcsolatfelvétel</a>.</p>
      </aside>
      {hiany('legalább 50–100 korábbi emésztőkiváltási ajánlat elemzése; az ajánlat és a végleges projektköltség eltérései; mely inputok mozgatják legjobban a költségsávot; mely adatok hiányoznak a leggyakrabban; a felmérés után felmerülő póttételek; milyen pontosságú inputtól adható értelmes ársáv; mely esetben nem adható távoli becslés.', 'ÖkoTech ajánlati archívum')}
    </div>
  </section>
''',
        sec_cta('Addig is', 'Beszéljünk a rendszeréről',
                ['Nem kell megvárnia, amíg minden adat megvan. Írja le, mi van most a telken, '
                 'milyen gyakran szippantanak, és mit tapasztal — megmondjuk, mi a következő '
                 'értelmes lépés.',
                 'Azt is, ha az derül ki, hogy a csere még nem indokolt.'],
                'Kapcsolatfelvétel', '../kapcsolat'),
    ]


CRUMB = [('Főoldal', '../'), ('Helyzetem', './'),
         ('Emésztő kiváltása', 'meglevo-emesztot-szeretnek-kivaltani')]

OLDALAK = [
    dict(file='helyzetem/mikor-indokolt-a-csere.html', url='helyzetem/mikor-indokolt-a-csere',
         img='emeszto-csere',
         title='Mikor indokolt a csere? — emésztő kiváltása | ÖkoTech Home',
         desc='A zárt tároló nem hibás technológia. A csere indoka mindig az adott ingatlanból '
              'következik — és a megtartás vagy a kivárás is racionális lehet.',
         h1='Mikor indokolt a csere?',
         alt='Régi repedt betonemésztő nyitva a talajban egy idősebb családi ház mellett, '
             'mellette friss kiásott gödör az új tartálynak',
         lead='A zárt tároló jogszabályilag létező, szabályos megoldás — nem attól kell '
              'lecserélni, mert rossz technológia. A csere indoka mindig a saját helyzetéből '
              'következik, és a megtartás is legitim eredmény.',
         crumbs=CRUMB, sections=epit_mikor()),
    dict(file='helyzetem/emeszto-oldomedence-vagy-biologiai.html',
         url='helyzetem/emeszto-oldomedence-vagy-biologiai', img='attekintes',
         title='Emésztő, oldómedence vagy biológiai rendszer? | ÖkoTech Home',
         desc='Három működési modell feltételes összehasonlítása: használat, áram, telek, '
              'talajvíz, vízelhelyezés, szippantás és vállalható karbantartás szerint.',
         h1='Emésztő, oldómedence vagy biológiai rendszer?',
         alt='Talajmetszet egy kerti tisztítórendszerrel: ülepítő, biológiai egység és '
             'kavicságyas elszivárogtatás egymás után',
         lead='A hétköznapi „emésztő" mögött három, jogilag is külön kezelt megoldás áll. '
              'A választás nem az árból indul, hanem abból, melyik feltételeit tudja teljesíteni '
              'az Ön ingatlana.',
         crumbs=CRUMB, sections=epit_technologia()),
    dict(file='helyzetem/teljes-koltseg-es-megterules.html',
         url='helyzetem/teljes-koltseg-es-megterules', img='csaladi-haz',
         title='Teljes költség és megtérülés — miért nem mondunk évszámot | ÖkoTech Home',
         desc='A csere pénzügyi döntése nem a szippantási díj és a vételár összevetése. '
              '5/10/15 éves forgatókönyv, érzékenységi vizsgálat — költségtartomány, nem ígéret.',
         h1='Teljes költség és megtérülés',
         alt='Modern földszintes családi ház gondozott kerttel, a gyepben két diszkrét aknafedlap',
         lead='Egy „négy év alatt megtérül" típusú állítás mindig egy konkrét háztartásra és egy '
              'adott évi díjra érvényes. Általános ígéretként megtévesztő — ezért itt '
              'költségtartományt és bizonytalanságokat mutatunk.',
         crumbs=CRUMB, sections=epit_koltseg()),
    dict(file='helyzetem/meglevo-rendszer-felmerese.html',
         url='helyzetem/meglevo-rendszer-felmerese', img='mar-van-rendszerem',
         title='Meglévő rendszer felmérése — mi van most a földben | ÖkoTech Home',
         desc='Az emésztőkiváltás nem új építés: van egy részben ismert föld alatti rendszer. '
              'Mit gyűjthet össze Ön, és mit ne kelljen megítélnie.',
         h1='Meglévő rendszer felmérése',
         alt='Szervizre nyitott biológiai tisztító akna gondozott kertben, mellette '
             'kompresszorszekrény és kiterített szerszámok',
         lead='Itt már van valami a földben — részben vagy egyáltalán nem ismert. A felmérés '
              'célja a kiinduló állapot rögzítése: mi ismert, mi bizonytalan, és mit kell a '
              'helyszínen megnézni.',
         crumbs=CRUMB, sections=epit_felmeres()),
    dict(file='helyzetem/koltseg-es-projektbrief.html',
         url='helyzetem/koltseg-es-projektbrief', img='helyzetem',
         title='Költség- és projektbrief — emésztőkiváltáshoz | ÖkoTech Home',
         desc='Az adatok, amelyekből felelősen meghatározható a műszaki irány és a '
              'költségtartomány. Nem árajánlatkérő, és nem használ országos átlagdíjat.',
         h1='Költség- és projektbrief',
         alt='Magyar falu széle naplementében: különböző korú családi házak földút mentén, '
             'az egyik gyepben tisztítóakna fedlapja',
         lead='Az előző négy oldal gyakorlati összefoglalója. Az ajánlatkérés így nem a feltárás '
              'kezdete, hanem az összegyűjtött projektadat természetes következő állapota.',
         crumbs=CRUMB, sections=epit_brief()),
]

if __name__ == '__main__':
    for o in OLDALAK:
        out = WEB / o['file']
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:48s} {len(out.read_text(encoding='utf-8'))//1024} KB")
