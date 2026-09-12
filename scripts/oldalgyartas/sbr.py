#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sbr.py — Tudástár: SBR szennyvíztisztító.

MIÉRT KELL EZ A LAP. A kulcsszókutatás (DataForSEO, 2026-09-04) HU-klaszterében
ott az „eleveniszapos / SBR / MBBR szennyvíztisztító”, és a top vásárlói
kérdések nyolcadika szó szerint: „SBR vagy MBBR vagy eleveniszapos — mi a
különbség?”. A webhelyen eddig EGYETLEN GYIK-válasz érintette; a versenytársak
viszont ezekkel a betűszavakkal hirdetnek.

A SZÖVEG BELÁÉTÓL VAN, nem tőlem. Szakmai állítást — évszámot, technológiai
elvet, terméktulajdonságot — nem írok emlékezetből; ez a lap a cég saját,
átadott anyagából készült, a webhely szerkezetébe illesztve.

AZ ÁBRA A CIKK KÖZPONTI GONDOLATÁT rajzolja meg: „amit az egyik konstrukció
elsősorban időben és vezérléssel választ szét, azt a másik jelentős részben
térben, a tartály kialakításával oldja meg”. Két külön SVG, mert keskenyen
egymás alá kell kerülniük — egyetlen széles rajz telefonon olvashatatlan.
Lásd `sbr_abra.py`.

FUTTATÁS:  python3 scripts/oldalgyartas/sbr.py
"""
import html as _html
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import sbr_abra  # noqa: E402

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
DOMAIN = 'https://okotechhome.hu'
UT = 'tudastar/sbr-szennyviztisztito'
CSS_V = 236
SUTI_V = 2

MINTA = (WEB / 'tudastar' / 'elszivarogtatas.html').read_text(encoding='utf-8')
FEJLEC = re.search(r'(<a class="skip-link".*?</header>)', MINTA, re.S).group(1)
LABLEC = re.search(r'(<!-- =+\n     LÁBLÉC.*?</footer>)', MINTA, re.S).group(1)


def esc(s):
    return _html.escape(str(s), quote=False)


def attr(s):
    return _html.escape(str(s), quote=True)


def jso(s):
    return json.dumps(str(s), ensure_ascii=False)


# A SORTÖRÉS KONSTANS, nem irodalom. A Python 3.9 f-stringjében a kifejezés
# nem tartalmazhat fordított perjelet, a szekciók törzsét viszont `\n`-nel
# fűzzük össze — így a `NL` néven hivatkozunk rá, és az f-string tiszta marad.
NL = chr(10)


def p(sz):
    return f'        <p class="type-ui-body">{sz}</p>'


def szekcio(azon, eyebrow, cim, torzs):
    return f'''
  <section class="section" id="{azon}" aria-labelledby="{azon}-cim">
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
    ('Mit jelent az SBR a szennyvíztisztításban?',
     'Az SBR a Sequencing Batch Reactor, vagyis szakaszos üzemű biológiai reaktor '
     'rövidítése. A lényege, hogy a tisztítás több technológiai fázisa — feltöltés, '
     'levegőztetés, ülepítés, elvezetés — ugyanabban a reaktortérben, de különböző '
     'időpontokban történik.'),
    ('Mi a különbség az SBR és a folyamatos átfolyású eleveniszapos rendszer között?',
     'Az SBR a tisztítás fázisait elsősorban IDŐBEN választja szét, vezérléssel. A '
     'folyamatos átfolyású, többkamrás rendszer ugyanezt jelentős részben TÉRBEN oldja '
     'meg: a szennyvíz egymást követő, különböző funkciójú tereken halad keresztül, és '
     'az elkülönítést maga a tartály kialakítása biztosítja.'),
    ('Új technológia az SBR?',
     'Nem. A szakaszos feltöltésen és ürítésen alapuló eleveniszapos rendszerek elődei '
     'már a XX. század elején megjelentek. Az elterjedéséhez az kellett, ami akkor még '
     'nem állt rendelkezésre a mai formájában: megbízható automatizálás és '
     'vezérléstechnika.'),
    ('Mi történik egy SBR-berendezéssel áramszünet esetén?',
     'Elektromos energia nélkül minden levegőztetett biológiai tisztítóban leáll a '
     'levegőztetés. Az SBR-nél azonban az időben egymásra épülő ciklus végrehajtása is '
     'a vezérléstől függ, ezért hosszabb áramszünetnél lényeges kérdés, mit tesz a '
     'berendezés az áram visszatérésekor: folytatja a megszakított ciklust, újat kezd, '
     'vagy felismeri, melyik fázisban állt le.'),
    ('SBR-rendszer az A.B. Clear?',
     'Nem. Az A.B. Clear szintén eleveniszapos biológiai tisztítást alkalmaz, de '
     'folyamatos átfolyású, többkamrás technológiával: a különböző folyamatok '
     'elkülönítését a többkamrás kialakítás biztosítja, nem az időzítés.'),
    ('Melyik a jobb technológia, az SBR vagy a folyamatos átfolyású?',
     'Önmagában a technológia nevéből erre nem lehet értelmes választ adni. Mindkettő '
     'évtizedek óta bizonyított alapokon működik. Egy családi háznál az a kérdés, hány '
     'aktív gépészeti alkatrész kell a működéshez, mekkora az energiaigény, hogyan '
     'történik az iszapkezelés, hogyan viseli a rendszer a változó terhelést, és mi '
     'történik hosszabb távollét vagy áramszünet után.'),
]


# A CIKK SZAKASZAI ADATSZERKEZETBEN, nem beágyazott füzérekben. Az első
# nekifutás f-stringbe ágyazott hármas idézőjelekkel épült, és az nem fordul:
# a Python 3.9 f-stringje sem fordított perjelet, sem beágyazott `'''`-t nem
# tűr a kifejezésében. Adatként a szöveg olvasható marad, és a formázás
# egyetlen helyen, a `szekcio()`-ban dől el.
#
# Egy elem: ('bekezdes', szöveg) vagy ('lista', [tételek]) vagy
# ('szamozott', [tételek]).
SZAKASZOK = [
    ('mi-az-sbr', 'Röviden', 'Mi az SBR, és mióta létezik?', [
        ('bekezdes', 'Az SBR ma az egyik ismert technológiai megoldás a biológiai '
         'szennyvíztisztításban. A rövidítés a <strong>Sequencing Batch Reactor</strong>, '
         'vagyis szakaszos üzemű biológiai reaktor elnevezésből származik.'),
        ('bekezdes', 'Bár korszerű technológiaként szokás beszélni róla, maga az alapelv '
         'egyáltalán nem új. A szakaszos feltöltésen és ürítésen alapuló eleveniszapos '
         'rendszerek elődei már a XX. század elején megjelentek. Az SBR későbbi '
         'elterjedéséhez azonban kellett valami, ami az első berendezések idején még nem '
         'állt rendelkezésre a mai formájában: <strong>megbízható automatizálás és '
         'vezérléstechnika</strong>.'),
        ('bekezdes', 'Amikor a 2000-es években a müncheni IFAT szakkiállításon jártunk, az '
         'SBR Nyugat-Európában már korántsem számított újdonságnak: kiforrott, széles körben '
         'alkalmazott szennyvíztisztítási technológia volt.'),
    ]),
    ('ciklus', 'A folyamat', 'Mi történik egy ciklus alatt?', [
        ('bekezdes', 'Egy biológiai szennyvíztisztítóban több, egymástól eltérő folyamatnak '
         'kell végbemennie. A szennyvizet fogadni kell, a szerves szennyező anyagokat '
         'mikroorganizmusok segítségével le kell bontani, ehhez megfelelő körülményeket — '
         'többek között oxigént — kell biztosítani, majd a kezelt víztől el kell választani '
         'a biológiai iszapot.'),
        ('bekezdes', 'Az SBR egyik lényeges ötlete, hogy ezek közül több folyamat '
         '<strong>ugyanabban a reaktortérben, de különböző időpontokban</strong> történik.'),
        ('szamozott', [
            '<strong>Feltöltés</strong> — a szennyvíz beérkezik a reaktorba',
            '<strong>Biológiai kezelés és levegőztetés</strong>',
            '<strong>Ülepítés</strong> — a levegőztetés leáll, az eleveniszap leülepszik',
            '<strong>Elvezetés</strong> — a fölötte kialakuló tisztított vízréteg egy részét '
            'a rendszer elvezeti',
        ]),
        ('bekezdes', 'Ezután kezdődhet a következő ciklus.'),
    ]),
    ('miert-terjedt-el', 'A háttér', 'Miért lett ennyire népszerű az SBR?', [
        ('bekezdes', 'Az SBR elterjedésének megértéséhez nem elég csak a szennyvízbiológiát '
         'vizsgálni. A <strong>gyártás gazdaságosságát</strong> is érdemes figyelembe venni.'),
        ('bekezdes', 'Egy többkamrás tartály elkészítése több belső szerkezeti elemet, '
         'válaszfalat, illesztést és — az alkalmazott anyagtól és gyártástechnológiától '
         'függően — jelentős kézi szerelési vagy hegesztési munkát igényelhet. Ezeknek a '
         'műveleteknek egy része nehezebben automatizálható, mint egy egyszerűbb geometriájú '
         'tartály nagy sorozatú előállítása.'),
        ('bekezdes', 'Ez különösen fontossá vált Nyugat-Európában, ahol a magas munkaerőköltség '
         'miatt a sok élőmunkát igénylő gyártás egyre drágábbá vált. Kézenfekvő mérnöki és '
         'gazdasági irány volt tehát az egyszerűbben sorozatgyártható tartályok alkalmazása, '
         'miközben a technológiai feladatok egy részét a mechanikai kialakítás helyett '
         'automatika, időprogramok és működtetett gépészeti elemek vették át.'),
        ('bekezdes', 'Az SBR ebből a szempontból elegáns megoldás: nem szükséges minden egyes '
         'technológiai fázishoz önálló teret kialakítani, ha ugyanaz a reaktortér megfelelő '
         'vezérléssel egymás után több feladatot is el tud látni.'),
        ('bekezdes', '<strong>Csakhogy ezzel a technológiai feladat nem tűnik el.</strong> '
         'Részben átköltözik a tartályból a vezérlésbe.'),
    ]),
    ('vezerles', 'Amit érdemes tudni', 'Az SBR lelke a vezérlés', [
        ('bekezdes', 'Ha egy rendszernek előre meghatározott időrendben kell levegőztetnie, '
         'ülepítenie, vizet továbbítania vagy elvezetnie, akkor az ehhez szükséges vezérlés a '
         'technológia szerves része.'),
        ('bekezdes', 'A vezérlőelektronika, a kompresszor, illetve az adott konstrukciótól '
         'függően alkalmazott szivattyúk, elektromosan működtetett szelepek és egyéb gépészeti '
         'elemek mind azért dolgoznak, hogy a megfelelő folyamat a megfelelő pillanatban '
         'történjen. Ez jól működő automatika mellett nagy előny: a rendszer képes önállóan '
         'végrehajtani az előre meghatározott technológiai ciklusokat.'),
        ('bekezdes', 'Ugyanakkor érdemes a másik oldalát is látni. <strong>Minden aktív '
         'gépészeti és elektromos alkatrész energiafogyasztó, karbantartást igényelhet, és '
         'egyben lehetséges meghibásodási pont is.</strong> Ezért egy szennyvíztisztító '
         'összehasonlításakor önmagában az, hogy „SBR-technológiás”, még nem mondja meg, '
         'mennyire egyszerű vagy összetett maga a berendezés.'),
    ]),
    ('aramszunet', 'Rendellenes üzem', 'És mi történik áramszünet esetén?', [
        ('bekezdes', 'Ez különösen érdekes kérdés, mert jól megmutatja a különböző '
         'konstrukciók közötti eltérést. Elektromos energia nélkül egy levegőztetett '
         'biológiai szennyvíztisztítóban természetesen a levegőztetés is leáll — ebben az '
         'értelemben az áramszünet egyik rendszernek sem kedvez.'),
        ('bekezdes', 'Az SBR esetében azonban az áramellátás nemcsak az oxigénbevitel miatt '
         'fontos. <strong>Az időben egymásra épülő technológiai ciklus végrehajtása is a '
         'vezérléstől függ.</strong>'),
        ('bekezdes', 'Hosszabb áramszünetnél ezért lényeges kérdés, hogy az adott berendezés '
         'mit tesz az áram visszatérésekor. Folytatja a megszakított ciklust? Újat kezd? '
         'Felismeri, hogy melyik technológiai fázisban történt a leállás? Milyen állapotban '
         'van ekkor a reaktor, és szükséges-e valamilyen beavatkozás?'),
        ('bekezdes', 'Ezek nem az SBR-technológia „hibái”. Egyszerűen következnek abból, hogy '
         'a technológiai folyamatok egy részének elkülönítését az időzített működés '
         'biztosítja. Ezért vásárlás előtt nemcsak azt érdemes megkérdezni, hogy egy '
         'berendezés milyen tisztítási technológiát használ, hanem azt is, hogy <strong>mi '
         'történik vele rendellenes üzemi helyzetekben</strong>.'),
    ]),
    ('ab-clear', 'A mi megoldásunk', 'Az A.B. Clear más utat követ', [
        ('bekezdes', 'Az A.B. Clear szennyvíztisztító szintén eleveniszapos biológiai '
         'tisztítást alkalmaz, de <strong>nem SBR-rendszer</strong>. Folyamatos átfolyású, '
         'többkamrás eleveniszapos technológiáról van szó, amelyben a szennyvíz meghatározott '
         'útvonalon, egymást követő funkcionális tereken halad keresztül. A különböző '
         'biológiai és fizikai folyamatok jelentős részének elkülönítését így maga a '
         'többkamrás kialakítás biztosítja.'),
        ('bekezdes', 'Ez természetesen nem jelenti azt, hogy az A.B. Clearnek nincs szüksége '
         'elektromos energiára. Az aerob biológiai folyamatokhoz levegőt kell biztosítani, '
         'ehhez kompresszor működik. A tervezési filozófia azonban az volt, hogy minél több '
         'feladatot maga a hidraulikai és tartálykialakítás oldjon meg, és minél kevesebb, a '
         'működéshez nélkülözhetetlen gépészeti alkatrészre legyen szükség.'),
        ('bekezdes', 'Ehhez kapcsolódik az <a href="../megoldasok/ab-clear-iszapzsakos-technologia">'
         'A.B. Clear iszapkezelése</a> is. A rendszerben keletkező fölösiszap az iszapzsákba '
         'kerül, ahol a víztartalom jelentős része eltávozhat és visszakerülhet a rendszerbe, '
         'miközben a szilárdabb iszap a zsákban marad. Ez a megoldás a rendszer stabil '
         'iszapszintjének fenntartását és az üzemeltetés egyszerűsítését szolgálja.'),
    ]),
    ('melyik-jobb', 'A döntés', 'Melyik technológia a jobb?', [
        ('bekezdes', 'Erre önmagában az „SBR” vagy az „eleveniszapos” kifejezés alapján nem '
         'lehet értelmes választ adni. Az SBR egy régóta ismert, kiforrott '
         'szennyvíztisztítási technológia. A folyamatos átfolyású eleveniszapos rendszerek '
         'szintén évtizedek óta bizonyított technológiai alapokon működnek.'),
        ('bekezdes', 'Egy családi háznál ezért sokkal érdekesebb kérdések következnek:'),
        ('lista', [
            'Mennyi aktív gépészeti alkatrész szükséges a működéshez?',
            'Mekkora az energiaigény?',
            'Hogyan történik az iszap kezelése?',
            'Hogyan viseli a rendszer a változó terhelést?',
            'Mi történik hosszabb távollét vagy áramszünet után?',
            'Milyen rendszeres karbantartást igényel?',
            'Egy meghibásodás esetén van-e hozzá alkatrész és szakember?',
        ]),
        ('bekezdes', 'És van még egy szempont, amelyet egy prospektusból nehéz megítélni: '
         '<strong>ki foglalkozik a berendezéssel öt vagy tíz év múlva?</strong>'),
    ]),
    ('szerviz', 'Hosszú távon', 'Egy szennyvíztisztító nem egyszeri vásárlás', [
        ('bekezdes', 'A biológiai szennyvíztisztító hosszú éveken keresztül működő műszaki és '
         'biológiai rendszer. Ezért az üzemeltetés és a szerviz legalább annyira fontos, mint '
         'maga a tartály.'),
        ('bekezdes', 'Az A.B. Clearhez ezért <strong>negyedéves karbantartási lehetőséget</strong> '
         'is biztosítunk. A rendszeres felülvizsgálat során ellenőrizhető a berendezés '
         'általános műszaki állapota és az iszapkezelés, tisztítható a kompresszor szűrője, '
         'szükség esetén korrigálható a levegőelosztás és a vezérlés beállítása, valamint még '
         'időben felismerhetők és javíthatók a kialakuló hibák.'),
        ('bekezdes', 'Egy jól megtervezett rendszer célja ugyanis nem pusztán az, hogy '
         'megfelelő körülmények között képes legyen szennyvizet tisztítani. Az igazi kérdés '
         'az, hogy ezt <strong>mennyire egyszerűen, kiszámíthatóan és üzembiztosan</strong> '
         'képes megtenni hosszú éveken keresztül, egy valódi háztartás mindennapi '
         'körülményei között.'),
    ]),
]


# ---------------------------------------------------------------------------
# SABLONOK. Nem f-string: `.format()` és `.replace()` tölti ki őket. A Python
# 3.9 f-stringje sem fordított perjelet, sem beágyazott hármas idézőjelet nem
# tűr a kifejezésében — az első nekifutás pontosan ezen bukott el.
# ---------------------------------------------------------------------------
HERO = """
  <section class="hero page-hero" aria-labelledby="oldal-cim">
    <div class="hero-inner">
      <div class="hero-copy">
        <nav class="breadcrumb" aria-label="Morzsamenü">
          <ol class="breadcrumb-list type-ui-caption" role="list">
            <li><a href="../">Főoldal</a></li>
            <li><a href="../tudastar/">Tudástár</a></li>
            <li aria-current="page">SBR szennyvíztisztító</li>
          </ol>
        </nav>
        <h1 class="type-display-page-title hero-title" id="oldal-cim">SBR szennyvíztisztító:
        hogyan működik, és miért terjedt el?</h1>
        <p class="type-ui-body-strong hero-lead">Az SBR a tisztítás fázisait időben
        választja szét, a folyamatos átfolyású rendszer térben. Ebből az egy különbségből
        következik szinte minden más — az alkatrészszám, az energiaigény és az is, mi
        történik áramszünet után.</p>
      </div>
    </div>
  </section>"""

ABRA_VAZ = """
  <section class="section section-alt" id="ido-vagy-ter" aria-labelledby="ido-vagy-ter-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Az alapvető különbség</p>
        <h2 class="type-display-section-title section-title" id="ido-vagy-ter-cim">Idő vagy tér</h2>
        <p class="type-ui-body section-lead">Amit az egyik konstrukció elsősorban időben és
        vezérléssel választ szét, azt a másik jelentős részben térben, a tartály
        kialakításával oldja meg.</p>
      </header>
      <div class="abra-parok">
        <figure class="abra">
          {SBR}
          <figcaption class="abra-felirat type-ui-caption"><strong>SBR — időben.</strong>
          Ugyanaz a reaktortér, egymás után négy fázis. A sorrendet és az időzítést a
          vezérlés adja.</figcaption>
        </figure>
        <figure class="abra">
          {ATFOLYO}
          <figcaption class="abra-felirat type-ui-caption"><strong>Folyamatos átfolyás — térben.</strong>
          A szennyvíz egymást követő, különböző funkciójú tereken halad át. Az elkülönítést
          a tartály kialakítása biztosítja.</figcaption>
        </figure>
      </div>
      <div class="folyoszoveg">
        <p class="type-ui-body">A valóságban természetesen ennél összetettebb rendszerek is
        léteznek, és az egyes technológiai elvek kombinálhatók. A különbség mégis jól
        érzékelteti a két tervezési filozófiát.</p>
      </div>
    </div>
  </section>"""

GYIK_SZEKCIO = """
  <section class="section section-alt" id="gyik" aria-labelledby="gyik-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Gyakori kérdések</p>
        <h2 class="type-display-section-title section-title" id="gyik-cim">Amit az SBR-ről a leggyakrabban kérdeznek</h2>
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
        <p class="type-ui-body section-lead">A technológia nevénél többet mond, hogy mi van
        a telken és hogyan használják. Írja meg — a többit mi mondjuk meg.</p>
      </header>
      <p class="type-ui-body">
        <a class="btn btn-primary type-ui-button" href="../konzultacio">Konzultációt kérek</a>
        <a class="btn btn-secondary type-ui-button" href="../megoldasok/megoldastipusok-osszehasonlitasa">Megoldástípusok összehasonlítása</a>
        <a class="btn btn-secondary type-ui-button" href="../tudastar/fogalomtar">Fogalomtár</a>
      </p>
    </div>
  </section>"""

LD_VAZ = """{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Article",
      "headline": "SBR szennyvíztisztító: hogyan működik, és miért terjedt el?",
      "description": {LEIRAS},
      "inLanguage": "hu-HU",
      "author": { "@type": "Organization", "name": "ÖkoTech-Home Kft.", "url": "https://okotechhome.hu/" },
      "publisher": { "@type": "Organization", "name": "ÖkoTech-Home Kft.", "url": "https://okotechhome.hu/" },
      "mainEntityOfPage": "https://okotechhome.hu/tudastar/sbr-szennyviztisztito"
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
        {"@type":"ListItem","position":3,"name":"SBR szennyvíztisztító","item":"https://okotechhome.hu/tudastar/sbr-szennyviztisztito"}
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
<meta property="og:locale" content="hu_HU">
<link rel="stylesheet" href="/assets/css/betuk.css?v=1">
<link rel="stylesheet" href="../assets/css/app.css?v={css}">
<script src="../assets/js/tema.js?v=1"></script>
<script src="/assets/js/suti.js?v={suti}" defer></script>
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


def abra_szekcio():
    """A két technológiai elv egymás mellett — a cikk központi gondolata képben."""
    return ABRA_VAZ.replace('{SBR}', sbr_abra.sbr_svg()).replace(
        '{ATFOLYO}', sbr_abra.atfolyo_svg())


def elem_html(tipus, tartalom):
    if tipus == 'bekezdes':
        return f'        <p class="type-ui-body">{tartalom}</p>'
    cimke = 'ol class="folyamat-lepesek"' if tipus == 'szamozott' else 'ul class="jogi-lista"'
    zaro = 'ol' if tipus == 'szamozott' else 'ul'
    sorok = NL.join(f'          <li class="type-ui-body">{t}</li>' for t in tartalom)
    return f'        <{cimke} role="list">{NL}{sorok}{NL}        </{zaro}>'


def epit():
    darabok = [szekcio(azon, eyebrow, cim,
                       NL.join(elem_html(t, x) for t, x in elemek))
               for azon, eyebrow, cim, elemek in SZAKASZOK]
    # AZ ÁBRA A MÁSODIK HELYRE KERÜL: a „mi az SBR” után, a ciklus
    # részletezése előtt. Ott mondja el képben, amit a cikk mondatban —
    # hogy időben vagy térben válik szét a folyamat.
    darabok.insert(1, abra_szekcio())
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

    cim = 'SBR szennyvíztisztító: hogyan működik, és miért terjedt el? | ÖkoTech Home'
    leiras = ('Az SBR a tisztítás fázisait időben választja szét, a folyamatos átfolyású '
              'rendszer térben. Mit jelent ez a gyakorlatban, és mi történik áramszünet után?')

    torzs = (HERO + NL + szakaszok + NL
             + GYIK_SZEKCIO.replace('{GYIK}', gyik_html) + NL + CTA_SZEKCIO)
    ld = (LD_VAZ.replace('{LEIRAS}', jso(leiras)).replace('{GYIK_LD}', gyik_ld))
    return LAP.format(cim=esc(cim), cim_attr=attr(cim), leiras=attr(leiras),
                      css=CSS_V, suti=SUTI_V, fejlec=FEJLEC, lablec=LABLEC,
                      torzs=torzs, ld=ld, domain=DOMAIN, ut=UT)


if __name__ == '__main__':
    cel = WEB / 'tudastar' / 'sbr-szennyviztisztito.html'
    sz = epit()
    cel.write_text(sz, encoding='utf-8')
    print(f'{cel.relative_to(GYOKER)}: {len(GYIK)} kérdés, {len(sz):,} bájt'.replace(',', ' '))
