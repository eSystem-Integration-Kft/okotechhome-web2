#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mbbr.py — Tudástár: MBBR és Fixed Bed — a biofilm a szennyvíztisztításban.

MIÉRT KELL EZ A LAP. A kulcsszókutatás (DataForSEO, 2026-09-04) HU-klaszterében
az „eleveniszapos / SBR / MBBR szennyvíztisztító" hármas együtt szerepel, és a
top vásárlói kérdések nyolcadika szó szerint: „SBR vagy MBBR vagy eleveniszapos
— mi a különbség?". Az SBR-lap ebből kettőt fed le; ez a harmadikat. A
versenytársak ezekkel a betűszavakkal hirdetnek, és a látogató a prospektusból
nem tudja eldönteni, mit jelentenek.

A SZÖVEG BELÁÉTÓL VAN, nem tőlem. Szakmai állítást — technológiai elvet,
terméktulajdonságot, mikrobiológiai folyamatot — nem írok emlékezetből; ez a
lap a cég saját, átadott anyagából készült, a webhely szerkezetébe illesztve.

A KÉT ÁBRA a cikk két legnehezebben elmondható állítását rajzolja meg:
  · HOL ÉL A BIOMASSZA — Fixed Bed, MBBR és eleveniszap egymás mellett;
  · A BIOFILM METSZETE — miért nem homogén néhány milliméteren belül sem.
Lásd `mbbr_abra.py`.

A LAP SBR-PÁRJA: `sbr.py`. A kettő egymásra hivatkozik, és mindkettő a
Fogalomtárra mutat — az AI-kereső és a látogató is így látja a szerkezetet.

FUTTATÁS:  python3 scripts/oldalgyartas/mbbr.py
"""
import html as _html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mbbr_abra  # noqa: E402

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
DOMAIN = 'https://okotechhome.hu'
UT = 'tudastar/mbbr-es-fixed-bed-biofilm'
SUTI_V = 2
SITE_V = 12      # a megamenü szkriptje
KALAUZ_V = 45    # az Öko kalauz

MINTA = (WEB / 'tudastar' / 'elszivarogtatas.html').read_text(encoding='utf-8')

# A STÍLUSLAP VERZIÓJA A MINTALAPBÓL JÖN, nem beégetve. Beégetve ez visszatérő
# csapda: az `app.css?v=NN` emelésekor a 188 kiadott lap frissül, a generátorok
# viszont a régi számot írták vissza a következő futáskor — az `ellenorzes.sh`
# 3. pontja ilyenkor „többféle app.css verzió" hibát jelez. A mintalap mindig a
# jelenlegi állapotot hordozza, tehát ez magától követi.
CSS_V = int(re.search(r'app\.css\?v=(\d+)', MINTA).group(1))

FEJLEC = re.search(r'(<a class="skip-link".*?</header>)', MINTA, re.S).group(1)
LABLEC = re.search(r'(<!-- =+\n     LÁBLÉC.*?</footer>)', MINTA, re.S).group(1)

CIM = 'MBBR és Fixed Bed: hogyan dolgozik a biofilm a szennyvíztisztításban?'
LEIRAS = ('A biofilm nem mesterséges találmány: a mikroorganizmusok felületeken '
          'telepednek meg. Mi a különbség a Fixed Bed és az MBBR között, és mit '
          'jelent mindez egy családi szennyvíztisztítónál?')


def esc(s):
    return _html.escape(str(s), quote=False)


def attr(s):
    return _html.escape(str(s), quote=True)


def jso(s):
    return json.dumps(str(s), ensure_ascii=False)


# A SORTÖRÉS KONSTANS, nem irodalom: a Python 3.9 f-stringjében a kifejezés
# nem tartalmazhat fordított perjelet. Lásd `sbr.py` ugyanitt.
NL = chr(10)


def szekcio(azon, eyebrow, cim, torzs, alt=False):
    o = ' section-alt' if alt else ''
    return f'''
  <section class="section{o}" id="{azon}" aria-labelledby="{azon}-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">{esc(eyebrow)}</p>
        <h2 class="type-display-section-title section-title" id="{azon}-cim">{esc(cim)}</h2>
      </header>
      <div class="folyoszoveg">
{torzs}
      </div>
    </div>
  </section>'''


GYIK = [
    ('Mit jelent az MBBR a szennyvíztisztításban?',
     'Az MBBR a Moving Bed Biofilm Reactor, vagyis mozgóágyas biofilmreaktor rövidítése. '
     'A reaktortérben szabadon mozgó hordozóelemek felületén biofilm alakul ki, és az '
     'ebben élő mikroorganizmusok vesznek részt a szennyező anyagok lebontásában.'),
    ('Mi a különbség az MBBR és a Fixed Bed között?',
     'Az alapelv mindkettőben ugyanaz: felületet biztosítunk a mikroorganizmusoknak. A '
     'különbség az, hogy a Fixed Bed rendszerben a hordozó meghatározott helyen marad a '
     'reaktorban, az MBBR-ben viszont a hordozóelemek szabadon mozognak a számukra '
     'kialakított térben.'),
    ('Mi az a biofilm?',
     'A biofilm a felületeken megtelepedő mikroorganizmusok összetett közössége. '
     'Természetes vizekben is megfigyelhető: a tartósan víz alatt lévő kövek és növényi '
     'részek idővel benépesülnek. A szennyvíztisztítás ezt a természetes jelenséget '
     'használja fel ellenőrzött körülmények között.'),
    ('A biofilmhordozó mindig műanyag?',
     'Nem. Az MBBR-ről készült fényképeken gyakran apró műanyag elemeket látunk, de '
     'számos anyag alkalmas lehet erre a célra: léteznek szivacsos, kerámia-, ásványi, '
     'aktívszén-alapú és kompozit hordozók is. Önmagában az alapanyag keveset árul el egy '
     'biofilmes rendszer teljesítményéről.'),
    ('Mindig a nagyobb fajlagos felületű hordozó a jobb?',
     'Nem. A biofilmnek kapcsolatban kell maradnia a kezelendő szennyvízzel: a szükséges '
     'anyagoknak el kell jutniuk hozzá, aerob folyamatoknál pedig megfelelő oxigénellátásra '
     'is szükség van. Ezért a hordozó geometriája, átjárhatósága és a víz áramlása legalább '
     'olyan fontos lehet, mint a névleges fajlagos felület.'),
    ('MBBR-rendszer az A.B. Clear?',
     'Nem. Az A.B. Clear nem MBBR- és nem Fixed Bed-rendszer: folyamatos átfolyású, '
     'többkamrás eleveniszapos technológiát alkalmaz. A biológiai tisztításban részt vevő '
     'mikroorganizmusok jelentős része eleveniszap formájában van jelen, a technológiai '
     'funkciók elkülönítésében pedig a többkamrás kialakítás és a szennyvíz meghatározott '
     'áramlási útja kap fontos szerepet.'),
    ('Melyik a jobb, a Fixed Bed vagy az MBBR?',
     'Erre nincs általános válasz. Mindkét technológia ugyanazt a biológiai lehetőséget '
     'használja ki, csak másképp. Jól méretezve és megfelelően üzemeltetve mindkét elv '
     'hatékonyan alkalmazható biológiai szennyvíztisztításra — a különbségeik nem '
     'feltétlenül hátrányok, hanem az adott technológiából következő mérnöki feladatok.'),
    ('Mire figyeljek egy családi szennyvíztisztító választásakor?',
     'A technológia neve mellett érdemes a teljes konstrukciót megvizsgálni: hogyan '
     'történik a levegőztetés, hogyan kezeli a rendszer a keletkező biomasszát, milyen '
     'gépészeti elemek szükségesek a működéshez, mekkora az energiaigény, hogyan férhet '
     'hozzá a szerviz, és milyen rendszeres karbantartást igényel. Ezekre nincs olyan '
     'válasz, hogy „MBBR", „Fixed Bed" vagy „eleveniszapos" — ezekre mindig az adott '
     'berendezés konstrukciója ad választ.'),
]


# A CIKK SZAKASZAI ADATSZERKEZETBEN — lásd `sbr.py` ugyanezt a megjegyzést.
# Egy elem: ('bekezdes', szöveg) vagy ('lista', [tételek]).
SZAKASZOK = [
    ('mi-a-biofilm', 'Az alapjelenség', 'Mi az a biofilm?', False, [
        ('bekezdes', 'Az MBBR, a Fixed Bed, a biofilm és a baktériumhordozó kifejezésekkel '
         'gyakran találkozhatunk a biológiai szennyvíztisztítók műszaki leírásában. Elsőre '
         'meglehetősen bonyolultnak tűnhetnek, pedig <strong>egy könnyen érthető biológiai '
         'jelenség áll mögöttük</strong>.'),
        ('bekezdes', 'A mikroorganizmusok megfelelő körülmények között szívesen telepednek meg '
         'különböző felületeken. Ha pedig megfelelő felületet biztosítunk számukra egy '
         'szennyvíztisztítóban, az ott kialakuló élő közösség részt vesz a szennyező anyagok '
         'lebontásában. Erre épülnek a biofilmes szennyvíztisztítási technológiák.'),
        ('bekezdes', 'A biofilm egyáltalán nem mesterséges találmány. Természetes vizekben is '
         'megfigyelhető, hogy a tartósan víz alatt lévő kövek, növényi részek és más felületek '
         'idővel benépesülnek mikroorganizmusokkal, amelyek összetett közösséget alkotnak a '
         'felületen. A szennyvíztisztítás ezt a természetes jelenséget használja fel '
         'ellenőrzött körülmények között.'),
        ('kiemeles', 'Fontos különbséget tenni: <strong>nem maga a hordozóanyag tisztítja meg a '
         'szennyvizet.</strong> A hordozó megfelelő életteret biztosít a tisztításban részt '
         'vevő mikroorganizmusoknak.'),
    ]),
    ('hordozo', 'A hordozóanyag', 'A baktériumhordozó nem feltétlenül műanyag', False, [
        ('bekezdes', 'Az MBBR-ről készült fényképeken gyakran apró műanyag hordozóelemeket '
         'látunk, ezért könnyű azt gondolni, hogy a biofilmhordozó szükségszerűen műanyagból '
         'készül. Pedig számos anyag alkalmas lehet erre a célra: léteznek különféle műanyag, '
         'szivacsos, kerámia-, ásványi, aktívszén-alapú és kompozit hordozók is. Az '
         'alkalmazható anyagok köre folyamatos fejlesztések tárgya.'),
        ('bekezdes', 'A megfelelő hordozó kiválasztásánál több tulajdonságot kell egyszerre '
         'figyelembe venni:'),
        ('lista', [
            'a rendelkezésre álló felületet',
            'a biofilm megtapadását',
            'a víz átjárhatóságát',
            'az anyag tartósságát',
            'és azt is, hogyan viselkedik a hordozó a reaktor tényleges üzemi körülményei között',
        ]),
        ('bekezdes', 'Ezért <strong>önmagában az alapanyag még keveset árul el egy biofilmes '
         'rendszer teljesítményéről</strong>.'),
    ]),
    ('felulet', 'A fajlagos felület', 'Miért fontos a hordozó felülete?', True, [
        ('bekezdes', 'Minél több megfelelő felület áll rendelkezésre, annál több helyet '
         'biztosíthatunk a biofilm kialakulásához. Ezért a biofilmhordozók egyik jellemző '
         'műszaki adata a <strong>fajlagos felület</strong>, amelyet rendszerint '
         'négyzetméter/köbméterben adnak meg.'),
        ('bekezdes', 'Ez azonban nem egyszerű verseny, amelyben automatikusan a legnagyobb szám '
         'győz. A biofilmnek kapcsolatban kell maradnia a kezelendő szennyvízzel: a '
         'mikroorganizmusok számára szükséges anyagoknak el kell jutniuk hozzájuk, aerob '
         'folyamatoknál pedig megfelelő oxigénellátásra is szükség van.'),
        ('bekezdes', 'Ezért a hordozó geometriája, átjárhatósága és a víz áramlása legalább '
         'olyan fontos lehet, mint a névleges fajlagos felület. A biofilm ráadásul maga is '
         'változik: növekszik, egyes részei leválnak, majd új biomassza alakul ki.'),
        ('kiemeles', 'A jó hordozó tehát nem egyszerűen sok felületet biztosít, hanem olyan '
         'felületet, amely <strong>a technológiai folyamat számára valóban hasznosítható</strong>.'),
    ]),
    ('fixed-bed', 'Az egyik elv', 'Fixed Bed: amikor a biofilmhordozó rögzített', False, [
        ('bekezdes', 'A Fixed Bed — vagyis rögzített ágyas biofilmes — technológiában a hordozó '
         'meghatározott helyen marad a reaktorban. A szennyvíz a hordozó mellett vagy annak '
         'szerkezetén keresztül áramlik, így kapcsolatba kerül a felületén kialakult '
         'biofilmmel.'),
        ('bekezdes', 'Ennek a megoldásnak az egyik előnye, hogy viszonylag nagy biofilmes felület '
         'alakítható ki egy meghatározott reaktortérben úgy, hogy maga a hordozó nem mozog.'),
        ('bekezdes', 'A Fixed Bed kialakításánál ezért különösen fontos a <strong>megfelelő '
         'hidraulika</strong>. A szennyvizet úgy kell vezetni, hogy a hordozófelület megfelelően '
         'részt vegyen a folyamatban, és a rendszer hosszú távon is jól átjárható maradjon. A '
         'biofilm természetes módon növekszik és megújul, ezért a megfelelően megtervezett '
         'rendszernek a biomassza változásával és leválásával is számolnia kell.'),
        ('bekezdes', 'Ez nem a Fixed Bed sajátos „hibája", hanem a biofilmes technológia '
         'tervezésének egyik alapvető feladata.'),
    ]),
    ('mbbr', 'A másik elv', 'MBBR: amikor a hordozó együtt mozog a vízzel', False, [
        ('bekezdes', 'Az MBBR az angol <strong>Moving Bed Biofilm Reactor</strong>, vagyis '
         'mozgóágyas biofilmreaktor rövidítése. Az alapelv ugyanaz: felületet biztosítunk a '
         'mikroorganizmusok számára. A különbség az, hogy az MBBR-ben a hordozóelemek szabadon '
         'mozognak a számukra kialakított reaktortérben.'),
        ('bekezdes', 'Aerob MBBR-rendszerekben a levegőztetés egyszerre biztosít oxigént a '
         'biológiai folyamatokhoz, valamint hozzájárul a hordozók és a szennyvíz keveredéséhez. '
         'Ennek komoly technológiai előnye van: a mozgó hordozók folyamatosan érintkeznek a '
         'kezelendő szennyvízzel, a mozgás és a kialakuló nyíróerők pedig a biofilm megújulását '
         'is segítik. A leváló, elöregedett biomassza helyén új biofilm fejlődhet.'),
        ('bekezdes', 'Az MBBR-hordozók feladata, hogy mozogjanak — <strong>de csak ott, ahol '
         'szükség van rájuk</strong>. Ezért a reaktor kialakításának biztosítania kell, hogy a '
         'víz továbbhaladhasson, miközben a hordozóelemek a számukra kijelölt térben maradnak. '
         'Erre különböző műszaki megoldások alkalmazhatók.'),
        ('kiemeles', 'A megfelelően megtervezett MBBR-rendszerben egymással összhangban működik '
         'a hordozóanyag, a levegőztetés, a keveredés, a víz áramlása és a hordozók '
         'visszatartása. Éppen ezért <strong>az MBBR jóval több annál, mint hogy műanyag '
         'elemeket helyeznek egy levegőztetett tartályba</strong>.'),
    ]),
    ('melyik-jobb', 'Az összevetés', 'Fixed Bed vagy MBBR — melyik a jobb?', True, [
        ('bekezdes', '<strong>Erre nincs általános válasz.</strong> Mindkét technológia ugyanazt '
         'a biológiai lehetőséget használja ki: felületet biztosít a biofilm számára. Abban '
         'különböznek, hogyan teszik ezt.'),
        ('lista', [
            'A <strong>Fixed Bed</strong>ben a hordozó rögzített. A megfelelő átáramlás és a '
            'hordozó hosszú távú átjárhatósága fontos tervezési kérdés.',
            'Az <strong>MBBR</strong>-ben a hordozó mozog. A hordozók megfelelő mozgását, a '
            'szükséges levegőztetést és a hordozók reaktorban tartását kell biztosítani.',
        ]),
        ('bekezdes', 'Ezek nem feltétlenül hátrányok, hanem az adott technológiából következő '
         'mérnöki feladatok. Jól méretezve és megfelelően üzemeltetve mindkét elv hatékonyan '
         'alkalmazható biológiai szennyvíztisztításra.'),
    ]),
    ('eleveniszap', 'A harmadik elv', 'És miben különbözik mindez az eleveniszapos technológiától?', False, [
        ('bekezdes', 'A hagyományos eleveniszapos tisztításnál a mikroorganizmusok jelentős része '
         'nem mesterséges hordozófelületen, hanem <strong>a vízben lebegő iszappelyhekben</strong> '
         'van jelen. A biofilmes rendszerek ezzel szemben lehetőséget adnak arra, hogy a '
         'biomassza jelentős részét egy hordozófelülethez kötve tartsuk a biológiai rendszerben.'),
        ('bekezdes', 'Ez bizonyos alkalmazásokban jelentős előny. Egy adott reaktortérben nagy '
         'mennyiségű aktív biomassza tartható fenn, ezért biofilmes technológiával meglévő '
         'szennyvíztisztító rendszerek biológiai kapacitása is növelhető anélkül, hogy '
         'feltétlenül ugyanilyen arányban kellene növelni a medencetérfogatot.'),
        ('bekezdes', 'A két technológiai világ ráadásul <strong>nem válik el élesen</strong> '
         'egymástól. Biofilm és lebegő eleveniszap ugyanabban a rendszerben is jelen lehet: '
         'léteznek olyan hibrid technológiák, amelyek tudatosan használják ki mindkét '
         'biomasszaforma tulajdonságait.'),
        ('bekezdes', 'Ezért egy berendezés működéséről sokkal többet kell tudnunk annál, mint '
         'hogy a műszaki leírásban szerepel-e az MBBR rövidítés.'),
    ]),
    ('nagy-telepek', 'A nagyüzem', 'Miért alkalmaznak biofilmes technológiákat nagy szennyvíztisztítókban is?', False, [
        ('bekezdes', 'A rendelkezésre álló tér a nagy szennyvíztisztító telepeken is érték. Ha egy '
         'meglévő biológiai medencében több aktív biomassza tartható fenn, az lehetőséget '
         'teremthet a tisztítási kapacitás növelésére vagy bizonyos tisztítási folyamatok '
         'intenzívebbé tételére anélkül, hogy minden esetben újabb nagy medencéket kellene '
         'építeni.'),
        ('bekezdes', 'Ez az MBBR és más biofilmes technológiák egyik fontos alkalmazási területe. '
         'A technológia tehát nem valamiféle marketingújdonság, hanem <strong>komoly mérnöki és '
         'mikrobiológiai alapokon nyugvó szennyvíztisztítási eljárás</strong>.'),
    ]),
    ('csaladi-haz', 'A családi ház', 'Családi szennyvíztisztítónál a teljes rendszert érdemes nézni', True, [
        ('bekezdes', 'Egy családi háznál természetesen ugyanazok a biológiai törvényszerűségek '
         'érvényesek, mint egy nagy szennyvíztisztító telepen. A gyakorlati követelmények azonban '
         'eltérhetnek.'),
        ('bekezdes', 'Egy háztartás szennyvízterhelése napszakonként és időszakonként jelentősen '
         'változhat. Előfordulhat többnapos távollét, hirtelen nagyobb vízhasználat, áramszünet '
         'vagy olyan háztartási vegyszer használata, amely átmenetileg befolyásolja a biológiai '
         'folyamatokat.'),
        ('bekezdes', 'Ezért családi szennyvíztisztító választásakor a technológia neve mellett '
         'érdemes megvizsgálni a teljes konstrukciót is:'),
        ('lista', [
            'Hogyan történik a levegőztetés?',
            'Hogyan kezeli a rendszer a keletkező biomasszát?',
            'Milyen gépészeti elemek szükségesek a működéshez?',
            'Mekkora az energiaigény?',
            'Hogyan férhet hozzá a szerviz a berendezéshez?',
            'Milyen rendszeres karbantartást igényel?',
        ]),
        ('kiemeles', 'Ezekre nincs olyan válasz, hogy „MBBR", „Fixed Bed" vagy „eleveniszapos". '
         '<strong>Ezekre mindig az adott berendezés konstrukciója ad választ.</strong>'),
    ]),
    ('ab-clear', 'A mi választásunk', 'Az A.B. Clear egy másik bevált biológiai elvet alkalmaz', False, [
        ('bekezdes', 'Az A.B. Clear <strong>nem MBBR- és nem Fixed Bed-rendszer</strong>. '
         'Folyamatos átfolyású, többkamrás eleveniszapos technológiát alkalmaz. Ebben a '
         'rendszerben a biológiai tisztításban részt vevő mikroorganizmusok jelentős része '
         'eleveniszap formájában van jelen, a technológiai funkciók elkülönítésében pedig fontos '
         'szerepet kap a többkamrás kialakítás és a szennyvíz meghatározott áramlási útja.'),
        ('bekezdes', 'Ez <strong>nem jobb vagy rosszabb biológiai alapelv, hanem más mérnöki '
         'megközelítés</strong>. A mi választásunknál fontos szempont volt, hogy családi házas '
         'alkalmazásban a teljes rendszer hosszú távon egyszerűen üzemeltethető, ellenőrizhető '
         'és javítható legyen.'),
        ('bekezdes', 'És itt ér össze minden szennyvíztisztítási technológia egyik legfontosabb '
         'kérdése: <strong>a megfelelő működés nemcsak a tervezésen, hanem az üzemeltetésen is '
         'múlik</strong>. A rendszeres felülvizsgálat lehetőséget ad arra, hogy ellenőrizzük a '
         'biológiai és műszaki működés szempontjából fontos állapotokat, elvégezzük a szükséges '
         'beállításokat, és egy kialakuló hibát lehetőség szerint még azelőtt felismerjünk és '
         'javítsunk, hogy komolyabb üzemzavart okozna.'),
    ]),
    ('zaras', 'Összegzés', 'Nem technológiai rövidítést, hanem működő rendszert választunk', False, [
        ('bekezdes', 'Az MBBR, a Fixed Bed és az eleveniszapos technológia egyaránt régóta ismert '
         'eszköz a biológiai szennyvíztisztításban. Mindegyiknek megvan a maga működési logikája, '
         'alkalmazási területe és tervezési követelménye. Ezért egyiket sem érdemes pusztán a '
         'neve alapján jobbnak vagy rosszabbnak tekinteni.'),
        ('bekezdes', 'Egy családi szennyvíztisztítónál végül az számít, hogyan áll össze a teljes '
         'rendszer: megfelelően méretezték-e az adott terheléshez, hogyan kezeli a biomasszát, '
         'mennyi gépészetet igényel, hogyan karbantartható, és milyen műszaki háttér áll mögötte '
         'hosszú távon.'),
        ('kiemeles', 'Ha ezeket megértjük, az MBBR, a Fixed Bed vagy az eleveniszapos technológia '
         'már nem hangzatos rövidítés egy prospektusban. Hanem az, ami valójában: '
         '<strong>különböző mérnöki megoldás ugyanarra a feladatra</strong> — a szennyvíz '
         'biológiai megtisztítására.'),
    ]),
]

HERO = """
  <section class="hero page-hero" aria-labelledby="oldal-cim">
    <div class="hero-inner">
      <div class="hero-copy">
        <nav class="breadcrumb" aria-label="Morzsamenü">
          <ol class="breadcrumb-list type-ui-caption" role="list">
            <li><a href="../">Főoldal</a></li>
            <li><a href="../tudastar/">Tudástár</a></li>
            <li aria-current="page">MBBR és Fixed Bed</li>
          </ol>
        </nav>
        <h1 class="type-display-page-title hero-title" id="oldal-cim">MBBR és Fixed Bed:
        hogyan dolgozik a biofilm a szennyvíztisztításban?</h1>
        <p class="type-ui-body-strong hero-lead">A mikroorganizmusok szívesen telepednek meg
        felületeken — a biofilmes technológiák ezt a természetes jelenséget használják
        ellenőrzött körülmények között. A hordozó nem tisztít: életteret ad.</p>
      </div>
    </div>
  </section>"""

ABRA_ELVEK = """
  <section class="section section-alt" id="harom-elv" aria-labelledby="harom-elv-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Egy pillantásra</p>
        <h2 class="type-display-section-title section-title" id="harom-elv-cim">Hol él a biomassza?</h2>
        <p class="type-ui-body section-lead">Mindhárom megoldás ugyanazt a biológiai lehetőséget
        használja. A különbség az, hogyan biztosít helyet a mikroorganizmusoknak.</p>
      </header>
      <div class="abra-egy">
        <figure class="abra">
          {SVG}
          <figcaption class="abra-felirat type-ui-caption"><strong>Ugyanaz a biológia, három
          elrendezés.</strong> A Fixed Bed rögzített hordozón tartja a biofilmet; az MBBR-ben a
          hordozók a vízzel együtt mozognak; az eleveniszapos technológiában nincs mesterséges
          hordozófelület. Mindháromnál a levegőztetés adja az oxigént.</figcaption>
        </figure>
      </div>
    </div>
  </section>"""

ABRA_BIOFILM = """
  <section class="section" id="biofilm-belseje" aria-labelledby="biofilm-belseje-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">A rétegen belül</p>
        <h2 class="type-display-section-title section-title" id="biofilm-belseje-cim">Mi történik a biofilm belsejében?</h2>
        <p class="type-ui-body section-lead">A biofilm egyik legérdekesebb tulajdonsága, hogy
        nem feltétlenül homogén.</p>
      </header>
      <div class="abra-egy">
        <figure class="abra">
          {SVG}
          <figcaption class="abra-felirat type-ui-caption"><strong>Néhány milliméter, többféle
          környezet.</strong> Az oxigén a biofilm belseje felé haladva fogy, ezért ugyanazon a
          vékony biológiai rétegen belül különböző mikrobiológiai folyamatok számára kedvező
          környezet jöhet létre.</figcaption>
        </figure>
      </div>
      <div class="folyoszoveg">
        <p class="type-ui-body">A vízzel érintkező külső réteg és a hordozóhoz közelebbi belső
        területek között eltérő körülmények alakulhatnak ki. Ez az egyik oka annak, hogy a
        biofilmes technológiák a szennyvíztisztításban ennyire érdekesek:
        <strong>egy apró hordozóelem felületén valójában összetett mikrobiológiai ökoszisztéma
        működhet</strong>.</p>
      </div>
    </div>
  </section>"""

GYIK_SZEKCIO = """
  <section class="section section-alt" id="gyik" aria-labelledby="gyik-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Gyakori kérdések</p>
        <h2 class="type-display-section-title section-title" id="gyik-cim">Amit a biofilmes technológiákról a leggyakrabban kérdeznek</h2>
      </header>
      <div class="fogalom-gyik">
{GYIK}
      </div>
    </div>
  </section>"""

CTA_SZEKCIO = """
  <section class="section" aria-labelledby="tovabb-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Tovább</p>
        <h2 class="type-display-section-title section-title" id="tovabb-cim">Ha a saját helyzete érdekli</h2>
        <p class="type-ui-body section-lead">A technológia nevénél többet mond, hogy mi van a
        telken és hogyan használják. Írja meg — a többit mi mondjuk meg.</p>
      </header>
      <p class="type-ui-body">
        <a class="btn btn-primary type-ui-button" href="../konzultacio">Konzultációt kérek</a>
        <a class="btn btn-secondary type-ui-button" href="sbr-szennyviztisztito">SBR szennyvíztisztító</a>
        <a class="btn btn-secondary type-ui-button" href="../megoldasok/megoldastipusok-osszehasonlitasa">Megoldástípusok összehasonlítása</a>
        <a class="btn btn-secondary type-ui-button" href="fogalomtar">Fogalomtár</a>
      </p>
    </div>
  </section>"""

LD_VAZ = """{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": {CIM},
      "description": {LEIRAS},
      "inLanguage": "hu-HU",
      "about": [
        {"@type":"Thing","name":"MBBR","alternateName":["Moving Bed Biofilm Reactor","mozgóágyas biofilmreaktor"]},
        {"@type":"Thing","name":"Fixed Bed","alternateName":["rögzített ágyas biofilmes technológia"]},
        {"@type":"Thing","name":"biofilm"},
        {"@type":"Thing","name":"eleveniszapos szennyvíztisztítás"}
      ],
      "author": { "@type": "Organization", "name": "ÖkoTech-Home Kft.", "url": "https://okotechhome.hu/" },
      "publisher": { "@type": "Organization", "name": "ÖkoTech-Home Kft.", "url": "https://okotechhome.hu/" },
      "mainEntityOfPage": "https://okotechhome.hu/{UT}"
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
{GYIK_LD}
      ]
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        {"@type":"ListItem","position":1,"name":"Főoldal","item":"https://okotechhome.hu/"},
        {"@type":"ListItem","position":2,"name":"Tudástár","item":"https://okotechhome.hu/tudastar/"},
        {"@type":"ListItem","position":3,"name":"MBBR és Fixed Bed","item":"https://okotechhome.hu/{UT}"}
      ]
    }
  ]
}"""

LAP = """<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<!-- TESZT ÜZEMMÓD: élesítéskor a `prod-epit.sh` 1. rétege cseréli. -->
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex, notranslate, max-snippet:0, max-image-preview:none, max-video-preview:0, noai, noimageai">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cim}</title>
<meta name="description" content="{leiras}">
<link rel="canonical" href="{domain}/{ut}">
<meta property="og:type" content="article">
<meta property="og:title" content="{cim_attr}">
<meta property="og:description" content="{leiras}">
<meta property="og:image" content="https://okotechhome.hu/assets/img/oldalak/hero-labor.webp?v=2">
<meta property="og:image:width" content="1800">
<meta property="og:image:height" content="764">
<meta property="og:image:alt" content="Laborvizsgálat az ÖkoTech-Home berendezéseihez">
<meta property="og:url" content="{domain}/{ut}">
<meta property="og:site_name" content="ÖkoTech Home">
<meta name="twitter:card" content="summary_large_image">
<meta property="og:locale" content="hu_HU">
<link rel="stylesheet" href="../assets/css/app.css?v={css}">
<script src="../assets/js/tema.js?v=1"></script>
<script src="/assets/js/suti.js?v={suti}" defer></script>
<!-- A MEGAMENÜT A `site.js` MŰKÖDTETI, az Ökót a `kalauz.js`. A fejléc
     MARKUPJA önmagában néma: a panelek nyitása, a billentyűzetes kezelés és a
     mobil fiók mind innen jön. Az SBR-lap első kiadásából ez kimaradt, és a
     megamenü emiatt nem nyílt — lásd `sbr.py` ugyanezt a megjegyzést. -->
<script src="../assets/js/site.js?v={site}" defer></script>
<script src="../assets/js/kalauz.js?v={kalauz}" defer></script>
</head>
<body>

{fejlec}

<main id="fotartalom">
{torzs}
</main>

{lablec}

<script type="application/ld+json">
{ld}
</script>

</body>
</html>
"""


def elem_html(tipus, tartalom):
    if tipus == 'bekezdes':
        return f'        <p class="type-ui-body">{tartalom}</p>'
    if tipus == 'kiemeles':
        # A MEGLÉVŐ `.jogi-kiemelt` komponens, amit a Tudástár többi lapja is
        # használ (`elszivarogtatas.html`, `bioemeszto-…`). Először írtam hozzá
        # egy `.folyoszoveg-kiemeles` osztályt — az lett volna a második
        # `.fogalom`-hiba: új komponens ott, ahol már van jó.
        return (f'        <div class="jogi-kiemelt">{NL}'
                f'          <p class="type-ui-body">{tartalom}</p>{NL}'
                f'        </div>')
    sorok = NL.join(f'          <li class="type-ui-body">{t}</li>' for t in tartalom)
    return f'        <ul class="jogi-lista" role="list">{NL}{sorok}{NL}        </ul>'


def epit():
    darabok = [szekcio(azon, eyebrow, cim,
                       NL.join(elem_html(t, x) for t, x in elemek), alt)
               for azon, eyebrow, cim, alt, elemek in SZAKASZOK]

    # AZ ELVEK ÁBRÁJA a „mi a biofilm" és a „hordozóanyag" közé: a látogató
    # ekkor már tudja, mi a biofilm, de még nem tudja, hányféleképpen lehet
    # helyet adni neki. A BIOFILM METSZETE a Fixed Bed / MBBR pár UTÁN áll,
    # mert az a szakasz már a rétegről szól, nem az elrendezésről.
    darabok.insert(1, ABRA_ELVEK.replace('{SVG}', mbbr_abra.harom_elv_svg()))
    darabok.insert(7, ABRA_BIOFILM.replace('{SVG}', mbbr_abra.biofilm_metszet_svg()))
    szakaszok = NL.join(darabok)

    gyik_ld = (',' + NL).join(
        '      {' + NL
        + f'        "@type": "Question",{NL}'
        + f'        "name": {jso(k)},{NL}'
        + '        "acceptedAnswer": { "@type": "Answer", "text": ' + jso(v) + ' }' + NL
        + '      }' for k, v in GYIK)

    gyik_html = NL.join(
        f'          <div class="fogalom-gyik-tetel">{NL}'
        f'            <h3 class="type-ui-card-title">{esc(k)}</h3>{NL}'
        f'            <p class="type-ui-body">{esc(v)}</p>{NL}'
        f'          </div>' for k, v in GYIK)

    cim = CIM + ' | ÖkoTech Home'
    torzs = (HERO + NL + szakaszok + NL
             + GYIK_SZEKCIO.replace('{GYIK}', gyik_html) + NL + CTA_SZEKCIO)
    ld = (LD_VAZ.replace('{CIM}', jso(CIM)).replace('{LEIRAS}', jso(LEIRAS))
          .replace('{GYIK_LD}', gyik_ld).replace('{UT}', UT))
    return LAP.format(cim=esc(cim), cim_attr=attr(cim), leiras=attr(LEIRAS),
                      css=CSS_V, suti=SUTI_V, site=SITE_V, kalauz=KALAUZ_V,
                      fejlec=FEJLEC, lablec=LABLEC,
                      torzs=torzs, ld=ld, domain=DOMAIN, ut=UT)


if __name__ == '__main__':
    cel = WEB / 'tudastar' / 'mbbr-es-fixed-bed-biofilm.html'
    sz = epit()
    cel.write_text(sz, encoding='utf-8')
    print(f'{cel.relative_to(GYOKER)}: {len(SZAKASZOK)} szakasz, {len(GYIK)} kérdés, '
          f'{len(sz):,} bájt'.replace(',', ' '))
