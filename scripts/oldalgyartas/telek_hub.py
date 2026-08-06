#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helyzetem → Telekvásárlás vagy új építés — a sitemap szerinti öt aloldal.

A brief három ponton KIFEJEZETTEN FELÜLÍR korábbi állításokat:

1. „Nem feltétlenül szükséges helyszíni felmérés — elég, ha tudja a telek
   adatait." Ez így félrevezető. Helyette döntési tábla kell: mikor elég
   dokumentum és fotó, mikor indokolt a felmérés, és mikor kell más szakértő.

2. A tartály telepíthetősége és a kezelt víz elhelyezhetősége KÉT KÜLÖN
   döntés. Attól, hogy a tartály magasabb talajvíznél is rögzíthető, még nem
   következik, hogy a víz helyben szikkasztható. A régi tartalom ezt egybemosta.

3. A felmérés eredménye nem „személyre szabott ajánlat", hanem strukturált
   telekbrief — javasolt rendszerhely, csatlakozási szintek, vízelhelyezési
   irány, kockázatok, hiányzó szakértői adatok.

Szolgáltatási ár SEHOL nem szerepel, a felmérésé sem.
Az ellenőrzőlista NEM kér kapcsolati adatot a használatához.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import sec_numbered, sec_split, sec_prose, sec_cta, sec_faq

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'
JOGI = ('<!-- JOGI ELLENŐRZÉS PUBLIKÁLÁS ELŐTT. Érintett: 147/2010. Korm. rendelet ·\n'
        '     27/2004. KvVM rendelet érzékenységi besorolása (a mellékletét 2026-ban is\n'
        '     módosították) · 219/2004. Korm. rendelet a felszín alatti vizek védelméről ·\n'
        '     281/2024. Korm. rendelet és módosításai. Mind gyorsan avuló tartalom. -->')


def hiany(mi, honnan):
    return f'<!-- ADATHIÁNY: {mi}\n     Forrás: {honnan}. Addig konkrét értékkel nem publikálható. -->'


# =========================================================== 4. ellenőrzőlista
CHECKLIST = [
    ('Alap', [
        ('Település, cím, helyrajzi szám', 'kötelező', 'tulajdoni lap, hirdetés'),
        ('Közcsatorna helyzete', 'kötelező', 'víziközmű-szolgáltató, önkormányzat'),
        ('Telek mérete', 'kötelező', 'tulajdoni lap, térképmásolat'),
    ]),
    ('Elrendezés', [
        ('A ház tervezett helye', 'kötelező', 'építész, helyszínrajz'),
        ('Szabad, beépíthető terület', 'kötelező', 'helyszínrajz, bejárás'),
        ('Tervezett lakosszám', 'kötelező', 'Ön tudja'),
        ('Megközelíthetőség géppel', 'hasznos', 'bejárás, fotó'),
    ]),
    ('Műszaki', [
        ('A szennyvízcső kilépési helye', 'kötelező új építésnél', 'gépész tervező'),
        ('A csőkilépés mélysége', 'kötelező új építésnél', 'gépész tervező, terv'),
        ('Tereplejtés', 'kötelező', 'bejárás, terepszintrajz'),
        ('Talajtípus', 'kötelező', 'talajmechanikai szakvélemény, szomszédok'),
        ('Talajvízszint — ismert-e', 'kötelező', 'szakvélemény, fúrt kút adatlapja'),
        ('A talajvíz-információ forrása és időpontja', 'kötelező, ha ismert', 'a dokumentumon'),
        ('Kút helye — sajátja és szomszédoké', 'kötelező', 'bejárás, kút adatlapja'),
        ('A kezelt víz tervezett elhelyezése', 'kötelező', 'bejárás + helyi előírások'),
    ]),
    ('Dokumentum', [
        ('Helyszínrajz', 'hasznos', 'építész'),
        ('Fotók a telekről', 'hasznos', 'Ön készíti'),
        ('Korábbi közműnyilatkozat vagy engedély', 'speciális esetben', 'saját irattár'),
    ]),
]

DOKUMENTUMOK = [
    ('Amit az építtető gyűjt össze', [
        'a telek címe és helyrajzi száma',
        'tulajdoni lap és térképmásolat',
        'fotók a telekről és a megközelítésről',
        'a tervezett lakosszám, és ha ismert, a vízfogyasztás',
        'korábbi közműnyilatkozat vagy engedély, ha van',
    ]),
    ('Amit a tervezőtől érdemes kérni', [
        'helyszínrajz az épület és a telek elrendezésével',
        'a szennyvízcső tervezett kilépési pontja és <strong>mélysége</strong>',
        'terepszintek és lejtésviszonyok',
        'a kezelt víz elhelyezésére szánt terület kijelölése',
        'talajmechanikai szakvélemény, ha az építéshez amúgy is készül',
    ]),
    ('Amit az ÖkoTech használ', [
        'a fenti adatok a méretezéshez és a telepítés megtervezéséhez',
        'a berendezés műszaki adatlapja',
        'teljesítménynyilatkozat, ahol az eljárás megkívánja',
    ]),
    ('Amit hatóság vagy szakértő kérhet', [
        'a projekt helyétől, méretétől, a vízelhelyezés módjától és a terület '
        'érzékenységi besorolásától függ',
        'ezért <strong>univerzális dokumentumlista nincs</strong> — az eljárást minden '
        'esetben az adott projektre kell tisztázni',
    ]),
]


def epit_alkalmassag():
    return [
        sec_prose('A valódi kérdés', 'Nem az, hogy elfér-e a tartály', [
            'A telek alkalmassága nem geometriai kérdés. A tartály szinte mindig elfér valahol — '
            'a rendszer viszont csak akkor működik, ha a <strong>kezelt víznek is van hová '
            'mennie</strong>, és a bekötés gravitációsan vagy átemelővel megoldható.',
            'Ezért a vizsgálat együtt nézi a közcsatornahelyzetet, a várható terhelést, a ház és '
            'a rendszer egymáshoz viszonyított helyét, a csőszintet, a szabad területet, a '
            'talajt, a talajvizet és a víz végső elhelyezését.',
            '<strong>Cím és telekméret alapján senki nem adhat „alkalmas" minősítést</strong> — '
            'a miénk sem. Ez előszűrés, nem műszaki engedély.']),
        sec_numbered('Állapotok', 'Háromféle eredmény lehet',
                     'Az előszűrés nem igen/nem választ ad, hanem azt, hogy mennyi bizonytalanság '
                     'maradt — és mit kell tenni vele.',
                     ['<strong>Standard helyzet.</strong> Az adatok ismertek, és nem mutatnak '
                      'kockázatot. A projekt a szokásos úton vihető tovább.',
                      '<strong>További adat szükséges.</strong> Egy vagy több kritikus adat '
                      'hiányzik — jellemzően a talajvíz, a talaj vagy a csőkilépés mélysége. '
                      'Ez a leggyakoribb kimenet, és nem rossz hír.',
                      '<strong>Szakértői felmérés szükséges.</strong> A telek műszakilag nem '
                      'standard: mély csőkilépés, kevés szabad terület, bizonytalan vízelhelyezés '
                      'vagy ellentmondó adatok. Itt a helyszín dönt, nem a dokumentum.']),
        sec_split('Kockázat', 'Mi az, ami módosít — és mi az, ami kizár',
                  'Módosítja a kialakítást, de nem zárja ki',
                  ['<strong>magas vagy ingadozó talajvíz</strong> — eltérő beépítési mód jöhet szóba;',
                   '<strong>mély szennyvízcső-kilépés</strong> — átemelő beépítése oldhatja meg;',
                   '<strong>kötött, rosszul szivárgó talaj</strong> — a vízelhelyezés módját írja felül;',
                   '<strong>erős lejtés</strong> — a rendszer helyét és a szintviszonyokat érinti;',
                   '<strong>szűk megközelítés</strong> — a telepítés és a későbbi szerviz drágul.'],
                  'Kizárhatja a helyben történő megoldást',
                  ['<strong>a kezelt víznek nincs hová mennie</strong> — sem szikkasztás, sem '
                   'befogadó, sem hasznosítás;',
                   '<strong>a közcsatorna műszakilag elérhető</strong>, és a kapacitás is megvan;',
                   '<strong>vízbázisvédelmi vagy fokozottan érzékeny terület</strong>, ahol külön '
                   'feltétel vonatkozik a telepítésre;',
                   '<strong>nincs elegendő szabad terület</strong> sem a rendszernek, sem a víz '
                   'elhelyezésének.']),
        f'''
  <section class="section" aria-labelledby="jog-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Jogi keret</p>
        <h2 class="type-display-section-title section-title" id="jog-cim">Amit a szabályozás is nevesít</h2>
      </header>
      {JOGI}
      <p class="type-ui-body section-lead">
        Az egyedi szennyvíztisztító létesítmény méretezésénél és létesítésénél a szabályozás
        kifejezetten nevesíti a <strong>talaj adottságait</strong>, a <strong>felszín alatti víz
        mélységét</strong> és a <strong>szennyvíz mennyiségét</strong>. Ezek tehát nem műszaki
        részletkérdések, hanem a jogszabály által is elismert döntési tényezők.
      </p>
      <p class="type-ui-body section-lead">
        Érzékeny vagy magas talajvízállású területen további feltételek állhatnak fenn.
        A területre vonatkozó besorolást és a helyi előírásokat minden esetben az illetékes
        hatóságnál kell tisztázni.
      </p>
      {hiany('a hivatkozott jogszabályhelyek pontos megjelölése és a hatályos szöveg; a település érzékenységi besorolása.', 'jogi ellenőrzés + illetékes hatóság')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'Értse meg, mi mit befolyásol',
                ['A talaj, a talajvíz és a vízelhelyezés összefügg — és a legtöbb félreértés '
                 'abból ered, hogy a tartály telepíthetőségét és a víz elhelyezhetőségét egy '
                 'kérdésnek nézik. Pedig két külön döntés.'],
                'Talaj, talajvíz és vízelhelyezés', 'talaj-talajviz-es-vizelhelyezes',
                alt=('Vagy gyűjtse össze a telek adatait', 'telekadat-ellenorzolista')),
    ]


def epit_talaj():
    return [
        sec_prose('A leggyakoribb félreértés', 'Két külön döntés, nem egy', [
            'A tartály telepíthetősége és a kezelt víz elhelyezhetősége <strong>két külön '
            'kérdés</strong>. Attól, hogy a tartály magasabb talajvíznél is műszakilag '
            'rögzíthető — például betonmedencés beépítéssel —, még <strong>nem következik</strong>, '
            'hogy a víz helyben szikkasztható.',
            'Ez a különbségtétel a legfontosabb, amit erről az oldalról érdemes elvinni. Sok '
            'projekt azért akad el, mert a kettőt egy kérdésnek vették.']),
        sec_numbered('Talaj', 'Nem a talaj neve számít, hanem a vízáteresztő képessége', None,
                     ['<strong>Laza, homokos talaj</strong> jól ereszti a vizet: a szikkasztás '
                      'kisebb felületen is működhet.',
                      '<strong>Kötött, agyagos talaj</strong> rosszul ereszti: a szikkasztás vagy '
                      'jelentős területet kíván, vagy nem járható út.',
                      '<strong>A talajtípus neve önmagában kevés.</strong> Ugyanaz az elnevezés '
                      'eltérő vízáteresztő képességet takarhat; a méretezéshez mérés kell.',
                      '<strong>A rétegződés is számít.</strong> A felszíni réteg alatt lehet '
                      'záróréteg, ami a szikkasztást megakadályozza.']),
        sec_numbered('Talajvíz', 'Az évszakos maximum számít, nem a mai szint',
                     'Ez a leggyakrabban félreértett adat. Egy nyári méréssel megállapított '
                     'alacsony szint nem mond semmit a tavaszi maximumról.',
                     ['<strong>A mértékadó szint a döntő.</strong> A tartály beépítését és a '
                      'szikkasztás lehetőségét is az évszakos maximum korlátozza.',
                      '<strong>A tartályra hatása:</strong> magas talajvíznél a felúszás ellen '
                      'külön műszaki védelem kell.',
                      '<strong>A szikkasztásra hatása:</strong> a kezelt víznek elegendő '
                      'talajréteg kell a talajvíz felett; ez független attól, hogy a tartály '
                      'beépíthető-e.',
                      '<strong>Honnan tudható meg:</strong> talajmechanikai szakvélemény, fúrt '
                      'kút adatlapja, a szomszédok tapasztalata, és hogy tavasszal áll-e meg víz '
                      'a telken.']),
        sec_numbered('Vízelhelyezés', 'Hová mehet a kezelt víz', None,
                     ['<strong>Talajba szikkasztás.</strong> A leggyakoribb megoldás, de a talaj '
                      'vízáteresztő képességétől és a talajvízszinttől függ. A szikkasztómező '
                      'területigénye jelentős.',
                      '<strong>Felszíni befogadó.</strong> Árok, patak vagy csatorna — ha van a '
                      'közelben, és a kezelője hozzájárul.',
                      '<strong>Hasznosítás.</strong> Például öntözésre, a feltételek '
                      'teljesülése esetén.',
                      '<strong>Ha egyik sem lehetséges</strong>, a zárt tároló marad — ezt '
                      'akkor is megmondjuk, ha nem a mi rendszerünk következik belőle.']),
        sec_split('Adatszerzés', 'Mihez elég a tájékozódás, és mihez kell mérés',
                  'Tájékozódó adatnak elég',
                  ['<strong>szomszédok tapasztalata</strong> a tavaszi vízállásról;',
                   '<strong>a telek megfigyelése</strong> — áll-e meg víz, hol a mélypont;',
                   '<strong>közeli fúrt kutak adatlapja</strong>, ha hozzáférhető;',
                   '<strong>a talaj felszíni jellege</strong> ásónyomnyi mélységben.'],
                  'Méréssel állapítható meg csak',
                  ['<strong>a mértékadó talajvízszint</strong> — ehhez szakvélemény kell;',
                   '<strong>a vízáteresztő képesség</strong> számszerű értéke;',
                   '<strong>a rétegződés</strong> a szikkasztás mélységéig;',
                   '<strong>a szikkasztómező méretezése</strong> — ez a fentiekből számított érték.']),
        f'''
  <section class="section" aria-labelledby="szakerto-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Mikor kell szakértő</p>
        <h2 class="type-display-section-title section-title" id="szakerto-cim">
          Van, amit nem lehet megbecsülni
        </h2>
      </header>
      <p class="type-ui-body section-lead">
        Hidrogeológus vagy geotechnikus bevonása indokolt, ha a talajvíz ismeretlen vagy
        ellentmondó, ha a telek vízbázisvédelmi vagy fokozottan érzékeny területen fekszik,
        vagy ha a szikkasztás lehetősége a méretezés szempontjából határeset.
      </p>
      {JOGI}
      {hiany('az ÖkoTech által alkalmazott valós telepítési és vízelhelyezési küszöbértékek; milyen talajhelyzethez milyen szikkasztómegoldás; a magas talajvíznél használt műszaki megoldások; mely esetben utasítják el a helyben történő vízelhelyezést.', 'ÖkoTech műszaki vezetés')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'Gyűjtse össze, amit tud',
                ['Az ellenőrzőlista végigveszi a telek adatait, és minden tételnél elfogadja a '
                 '„nem tudom" választ — mellé téve, honnan szerezhető meg.'],
                'Telekadat-ellenőrzőlista', 'telekadat-ellenorzolista',
                alt=('Vagy nézze meg, milyen dokumentum kell', 'milyen-dokumentumokra-lehet-szukseg')),
    ]


def epit_dokumentumok():
    blokkok = ''
    # Az azonosító SORSZÁMBÓL képződik, nem a címből: két szerepkör címe is
    # „Amit az…" kezdetű, és a szóból képzett kulcs ütközött volna.
    for i, (cim, tetelek) in enumerate(DOKUMENTUMOK, 1):
        li = '\n'.join(f'          <li class="type-ui-body">{t}</li>' for t in tetelek)
        aid = str(i)
        blokkok += f'''
        <div class="split-card">
          <h3 class="type-ui-card-title split-title" id="dok-{aid}">{cim}</h3>
          <ul class="dok-lista" role="list">
{li}
          </ul>
        </div>'''

    return [
        sec_prose('Előbb tisztázzuk', 'Nem minden dokumentum kell minden projekthez', [
            'Három különböző dolog keveredik gyakran össze: az <strong>épület építésügyi '
            'dokumentációja</strong>, a <strong>szennyvízrendszer műszaki előkészítéséhez '
            'használt tervanyag</strong>, és az <strong>egyedi szennyvízkezelés esetleges '
            'hatósági dokumentációja</strong>. Ezek más funkciót töltenek be, és nem ugyanaz a '
            'kör kéri őket.',
            'Ezért nem adunk univerzális dokumentumlistát. Az alábbi felosztás szerepkör szerint '
            'rendezi, mit érdemes honnan beszerezni.']),
        f'''
  <section class="section" aria-labelledby="szerep-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Szerepkörök</p>
        <h2 class="type-display-section-title section-title" id="szerep-cim">Ki mit ad hozzá</h2>
      </header>
      <div class="split split-4">
{blokkok}
      </div>
    </div>
  </section>
''',
        f'''
  <section class="section" aria-labelledby="hatosag-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Hatósági eljárás</p>
        <h2 class="type-display-section-title section-title" id="hatosag-cim">
          Miért nem adunk kész eljárási mintát
        </h2>
      </header>
      {JOGI}
      <p class="type-ui-body section-lead">
        A szükséges eljárást a projekt helye, mérete, a kezelt víz elhelyezésének módja és a
        terület érzékenységi besorolása együtt határozza meg. Ugyanaz a berendezés két
        településen eltérő eljárást kívánhat.
      </p>
      <p class="type-ui-body section-lead">
        Korábbi engedélypéldáink szemléltetésre alkalmasak, de <strong>nem automatikusan
        alkalmazható minták</strong>: mindegyik egy adott időpontban, adott településen, adott
        projekttípusra született. Ha ilyet adunk ki, dátummal, településsel és projekttípussal
        együtt adjuk, épp azért, hogy ne lehessen sablonként használni.
      </p>
      <p class="type-ui-body section-lead">
        Új lakóépületnél az építésügyi dokumentáció követelményeit minden esetben az
        <strong>aktuális</strong> építésügyi szabályok alapján kell ellenőrizni; ez a terület
        gyakran változik.
      </p>
      {hiany('az ÖkoTech „miből tudunk ajánlatot készíteni" és „miből lehet kivitelezni" minimumcsomagja; a modellek aktuális műszaki dokumentumai; az engedélypéldák pontos kontextusa; a leggyakrabban hiányzó dokumentumok listája.', 'ÖkoTech értékesítés és műszaki vezetés')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'Vezesse végig a saját telkét',
                ['Az ellenőrzőlista a fenti adatokat gyakorlati sorrendben kéri, és megjelöli, '
                 'melyik kell a következő döntéshez, melyik hasznos, és melyik csak speciális '
                 'esetben szükséges.'],
                'Telekadat-ellenőrzőlista', 'telekadat-ellenorzolista'),
    ]


def epit_checklist():
    blokkok = ''
    for cim, tetelek in CHECKLIST:
        sorok = '\n'.join(
            f'''            <tr>
              <th scope="row" class="type-ui-subtitle">{n}</th>
              <td class="type-ui-subtitle">{sz}</td>
              <td class="type-ui-subtitle">{h}</td>
            </tr>''' for n, sz, h in tetelek)
        aid = cim.lower().replace('ő', 'o').replace('é', 'e')
        blokkok += f'''
  <section class="section" aria-labelledby="cl-{aid}-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">{cim}</p>
        <h2 class="type-display-section-title section-title" id="cl-{aid}-cim">{cim}adatok</h2>
      </header>
      <div class="compare-scroll" role="region" aria-labelledby="cl-{aid}-cim" tabindex="0">
        <table class="compare-table">
          <thead>
            <tr>
              <th scope="col">Adat</th>
              <th scope="col">Mennyire szükséges</th>
              <th scope="col">Honnan szerezhető meg</th>
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
        sec_prose('Hogyan használja', 'Nem kér Öntől semmit', [
            'Ez a lista <strong>nem űrlap</strong>: nem kér kapcsolati adatot, és nem feltételezi, '
            'hogy ajánlatot szeretne. Végigmehet rajta magának, és a végén látni fogja, mi van meg '
            'és mi hiányzik.',
            'Minden adatnál négy válasz lehetséges: <strong>tudom · becsülöm · nem tudom · mérni '
            'kell</strong>. A becsült, a dokumentumból származó és a ténylegesen megmért adat nem '
            'azonos megbízhatóságú — ezért másra elég. Ha később ajánlatot kér, ez a különbség '
            'számít.',
            'A „nem tudom" nem hiba. Minden tételnél ott áll, honnan szerezhető meg.']),
    ] + [blokkok] + [
        sec_numbered('Az eredmény', 'Mi következik abból, ami hiányzik', None,
                     ['<strong>Minden kötelező adat megvan.</strong> A projekt továbbvihető: '
                      'jöhet a tervezői egyeztetés vagy az ajánlat-előkészítés.',
                      '<strong>A talajvíz vagy a talaj hiányzik.</strong> Ez a leggyakoribb eset. '
                      'A következő lépés szakvélemény beszerzése — vagy ha az építkezéshez amúgy '
                      'is készül, annak kiterjesztése erre a kérdésre.',
                      '<strong>A csőkilépés mélysége nem ismert.</strong> Új építésnél a gépész '
                      'tervezőtől kérhető; meglévő háznál kiásással állapítható meg.',
                      '<strong>A vízelhelyezés bizonytalan.</strong> Ez az a pont, ahol a '
                      'helyszíni felmérés a leggyorsabb út — dokumentumból nem dönthető el.']),
        f'''
  <section class="section" aria-labelledby="mento-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Mentés</p>
        <h2 class="type-display-section-title section-title" id="mento-cim">Kitölthető változat</h2>
      </header>
      <aside class="panel">
        <p class="type-ui-body"><strong>A kitölthető, menthető változat még készül.</strong>
          Addig a fenti táblázatok kinyomtathatók vagy lementhetők a böngészőből, és úgy is
          használhatók egyeztetésen.</p>
      </aside>
      {hiany('a menthető/PDF-be exportálható telekbrief formátuma és mezőkészlete; mely adatból következik ténylegesen konfigurációváltozás.', 'ÖkoTech felmérési munkalap + értékesítési adatlap')}
    </div>
  </section>
''',
        sec_cta('Következő lépés', 'Ha maradt nyitott kérdés',
                ['A helyszíni felmérés akkor ad értéket, ha konkrét bizonytalanságot zár le — '
                 'nem értékesítési rituálé. A következő oldal megmutatja, mikor indokolt, és '
                 'mikor elég a dokumentum és a fotó.'],
                'Helyszíni felmérés', 'helyszini-felmeres'),
    ]


def epit_felmeres():
    return [
        sec_prose('Mikor ad értéket', 'Nem minden projekthez kell', [
            'A helyszíni felmérés nem kötelező lépés és nem értékesítési rituálé. Akkor ad '
            'értéket, ha <strong>konkrét bizonytalanságot zár le</strong> — olyat, amire '
            'dokumentumból nincs válasz.',
            'Ha a telek adatai ismertek és nem mutatnak kockázatot, a projekt fotókkal és '
            'dokumentumokkal is előkészíthető. Ha viszont a kritikus adatok hiányoznak vagy '
            'ellentmondóak, a felmérés a leggyorsabb út.']),
        sec_numbered('Döntési tábla', 'Mikor mi elég', None,
                     ['<strong>Elég a dokumentum és a fotó,</strong> ha a talajvíz ismert, a '
                      'vízelhelyezés tisztázott, a csőkilépés mélysége adott, és van elegendő '
                      'szabad terület.',
                      '<strong>Indokolt a felmérés,</strong> ha a talajvíz vagy a vízelhelyezés '
                      'nem ismert, a lejtés problémás, mély a szennyvízcső, kevés a szabad '
                      'terület, vagy bizonytalan a rendszer helye.',
                      '<strong>Gyakorlatilag elengedhetetlen,</strong> ha több műszaki kialakítás '
                      'között kell választani, vagy ha az adatok ellentmondanak egymásnak.',
                      '<strong>Más szakértő kell,</strong> ha a kérdés hidrogeológiai vagy '
                      'geotechnikai — a felmérés ezt nem helyettesíti.']),
        sec_split('A helyszínen', 'Mit vizsgálunk — és mit nem',
                  'Amit megnézünk',
                  ['<strong>a szennyvízcső helye és mélysége</strong>;',
                   '<strong>a tereplejtés</strong> és a szintviszonyok;',
                   '<strong>a talaj felszíni jellege</strong> és a látható vízviszonyok;',
                   '<strong>a szabad terület</strong> és a rendszer lehetséges helye;',
                   '<strong>a kezelt víz elhelyezésének iránya</strong>;',
                   '<strong>a megközelíthetőség</strong> telepítéshez és későbbi szervizhez;',
                   '<strong>szükséges-e kiegészítő műszaki elem</strong> — például átemelő.'],
                  'Amit NEM állapít meg',
                  ['<strong>a mértékadó talajvízszintet</strong> — ehhez szakvélemény kell;',
                   '<strong>a talaj számszerű vízáteresztő képességét</strong>;',
                   '<strong>az engedélyezhetőséget</strong> — az hatósági kérdés;',
                   '<strong>a végleges árat</strong> — az a tisztázott adatokból következik.']),
        sec_numbered('Az eredmény', 'Amit kézhez kap',
                     'Nem „személyre szabott ajánlat", hanem strukturált telekbrief — ez akkor is '
                     'használható, ha végül nem tőlünk vásárol.',
                     ['<strong>A rendszer javasolt helye</strong> a telken.',
                      '<strong>Csatlakozási szintek</strong> — gravitációs vagy átemelős megoldás.',
                      '<strong>A kezelt víz elhelyezésének javasolt iránya.</strong>',
                      '<strong>A kritikus kockázatok</strong> megnevezve.',
                      '<strong>A szükséges kiegészítő műszaki elemek.</strong>',
                      '<strong>Ami még hiányzik</strong> — és melyik szakértőtől szerezhető meg.']),
        f'''
  <section class="section" aria-labelledby="tovabb-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Az építésszel és a gépésszel</p>
        <h2 class="type-display-section-title section-title" id="tovabb-cim">
          A brief tervezési inputként is használható
        </h2>
      </header>
      <p class="type-ui-body section-lead">
        A csatlakozási szintek és a rendszer helye olyan adatok, amelyekre az építésznek és a
        gépész tervezőnek szüksége van. Ha ezek a tervezés korai szakaszában rendelkezésre
        állnak, elkerülhető a későbbi magasítás, átemelő beépítése vagy más pótlólagos megoldás.
      </p>
      {hiany('a felmérési protokoll: mit mérnek ténylegesen és mit csak megfigyelnek; kap-e az ügyfél írásos eredményt és milyen formában; a felmérés földrajzi lefedettsége és szolgáltatási feltételei; mely esetben elegendő távoli dokumentációs egyeztetés.', 'ÖkoTech felmérési gyakorlat')}
    </div>
  </section>
''',
        sec_cta('Felmérés', 'Kérjen helyszíni felmérést',
                ['Írja meg, hol van az ingatlan és mit tud róla — visszajelezzük, hogy a '
                 'felmérés indokolt-e, vagy az adatok alapján enélkül is továbbléphet.',
                 'Ha inkább önállóan gyűjtené össze az adatokat, az ellenőrzőlista végigvezeti.'],
                'Felmérés kérése', '../kapcsolat',
                alt=('Vagy előbb a telekadat-ellenőrzőlista', 'telekadat-ellenorzolista')),
    ]


CRUMB = [('Főoldal', '../'), ('Helyzetem', './'),
         ('Telekvásárlás vagy új építés', 'telekvasarlas-vagy-uj-epites-elott-allok')]

OLDALAK = [
    dict(file='helyzetem/alkalmas-lehet-e-a-telek.html', url='helyzetem/alkalmas-lehet-e-a-telek',
         img='telekvasarlas',
         title='Alkalmas lehet-e a telek? — előzetes alkalmassági szempontok | ÖkoTech Home',
         desc='Nem az a kérdés, elfér-e a tartály. A kezelt víz elhelyezése, a csőszint, a talaj '
              'és a talajvíz együtt dönti el, mi valósítható meg a telken.',
         h1='Alkalmas lehet-e a telek?',
         alt='Üres füves építési telek kitűzőcövekekkel és zsinórral, előtérben nyitott '
             'talajvizsgálati gödör a rétegekkel',
         lead='A tartály szinte mindig elfér valahol. A rendszer viszont csak akkor működik, ha a '
              'kezelt víznek is van hová mennie, és a bekötés megoldható. Ez előszűrés, nem '
              'műszaki engedély.',
         crumbs=CRUMB, sections=epit_alkalmassag()),
    dict(file='helyzetem/talaj-talajviz-es-vizelhelyezes.html',
         url='helyzetem/talaj-talajviz-es-vizelhelyezes', img='oldomedence',
         title='Talaj, talajvíz és vízelhelyezés — mi mit befolyásol | ÖkoTech Home',
         desc='A tartály telepíthetősége és a kezelt víz elhelyezhetősége két külön kérdés. '
              'Mit jelent a vízáteresztő képesség, miért az évszakos maximum számít, és mikor kell mérés.',
         h1='Talaj, talajvíz és vízelhelyezés',
         alt='Talajmetszet egy erdőszéli ház előtt: oldómedence és kavicsos elszivárogtató mező',
         lead='A legtöbb félreértés abból ered, hogy a tartály telepíthetőségét és a kezelt víz '
              'elhelyezhetőségét egy kérdésnek nézik. Pedig két külön döntés — és a második a '
              'nehezebb.',
         crumbs=CRUMB, sections=epit_talaj()),
    dict(file='helyzetem/milyen-dokumentumokra-lehet-szukseg.html',
         url='helyzetem/milyen-dokumentumokra-lehet-szukseg', img='biologiai',
         title='Milyen dokumentumokra lehet szükség? — szerepkörök szerint | ÖkoTech Home',
         desc='Építési dokumentáció, műszaki tervanyag és hatósági dokumentum — három különböző '
              'dolog. Ki mit ad hozzá, és miért nincs univerzális lista.',
         h1='Milyen dokumentumokra lehet szükség?',
         alt='Talajmetszet egy családi ház kertje alatt: hengeres biológiai tisztítótartály '
             'belső terekkel és aknafedlapokkal',
         lead='Nem minden dokumentum kell minden projekthez. Az épület építésügyi dokumentációja, '
              'a műszaki tervanyag és az esetleges hatósági dokumentáció más funkciót tölt be — '
              'és nem ugyanaz a kör kéri őket.',
         crumbs=CRUMB, sections=epit_dokumentumok()),
    dict(file='helyzetem/telekadat-ellenorzolista.html', url='helyzetem/telekadat-ellenorzolista',
         img='csaladi-haz',
         title='Telekadat-ellenőrzőlista — mi van meg, mi hiányzik | ÖkoTech Home',
         desc='Végigveheti a telek adatait: melyik kell a következő döntéshez, melyik hasznos, '
              'és honnan szerezhető meg. Nem kér kapcsolati adatot.',
         h1='Telekadat-ellenőrzőlista',
         alt='Modern földszintes családi ház gondozott kerttel, a gyepben két diszkrét aknafedlap',
         lead='Ez nem űrlap: nem kér kapcsolati adatot, és nem feltételezi, hogy ajánlatot '
              'szeretne. Végigmehet rajta magának, és a végén látni fogja, mi van meg és mi '
              'hiányzik — a „nem tudom" is érvényes válasz.',
         crumbs=CRUMB, sections=epit_checklist()),
    dict(file='helyzetem/helyszini-felmeres.html', url='helyzetem/helyszini-felmeres',
         img='kapcsolat',
         title='Helyszíni felmérés — mikor indokolt és mit ad | ÖkoTech Home',
         desc='A felmérés akkor ad értéket, ha konkrét bizonytalanságot zár le. Mikor elég a '
              'dokumentum, mikor indokolt a kiszállás, és milyen telekbriefet kap kézhez.',
         h1='Helyszíni felmérés',
         alt='Helyszíni felmérés eszközei egy jármű raktere mellett: összehajtott műszaki rajz, '
             'jegyzetfüzet, colstok és talajmintavevő zacskó',
         lead='A felmérés nem értékesítési rituálé, hanem műszaki szolgáltatás: konkrét '
              'bizonytalanságokat zár le. Ha a telek adatai ismertek, enélkül is továbbléphet — '
              'és ezt megmondjuk.',
         crumbs=CRUMB, sections=epit_felmeres()),
]

if __name__ == '__main__':
    for o in OLDALAK:
        out = WEB / o['file']
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:52s} {len(out.read_text(encoding='utf-8'))//1024} KB")
