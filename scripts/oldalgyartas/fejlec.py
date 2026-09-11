#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fejléc — kontaktsáv + HÁROMSZINTŰ megamenü, minden oldalra.

╔══════════════════════════════════════════════════════════════════════════════╗
║  FIGYELEM — EZ A SZKRIPT JELENLEG NEM FUTTATHATÓ BIZTONSÁGOSAN.              ║
║                                                                              ║
║  A `_web/` fejlécei két ponton ELŐBBRE JÁRNAK, mint az itteni adatok, mert   ║
║  kézzel lettek átvezetve:                                                    ║
║                                                                              ║
║   · TUDÁSTÁR és EREDMÉNYEK panel — a holt menütételek élesítve lettek        ║
║     (élő hivatkozások a megvalósult projektekre, az EN 12566 cikkre), itt    ║
║     viszont még a `KESZUL` helykitöltő lista áll;                            ║
║   · RÓLUNK kategória — a hatodik fül a webhelyen már megvan, a `MENU`-ben    ║
║     még nincs. 2026-09-11 óta a HÍREK tétel is benne áll a webhely RÓLUNK    ║
║     paneljében (`okotech-home/hirek/`, `icon-nav-hirek` ikonnal), mind a     ║
║     186 menüs lapon — a `MENU` ezt sem tartalmazza.                          ║
║                                                                              ║
║  Amíg ez a három nincs átvezetve, a szkript futtatása VISSZAÍRNÁ a régi      ║
║  állapotot mind a 186 oldalon. Az eltérés ellenőrzése (0 sor = futtatható):  ║
║                                                                              ║
║      python3 - <<\'EOF\'                                                      ║
║      import importlib.util, pathlib, re, difflib                             ║
║      sp = importlib.util.spec_from_file_location('f', 'scripts/oldalgyartas/fejlec.py')
║      m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)       ║
║      web = re.search(r'<a class="skip-link".*?</header>',                    ║
║          pathlib.Path('_web/index.html').read_text(encoding='utf-8'), re.S).group(0)
║      print('\\n'.join(difflib.unified_diff(web.splitlines(),                  ║
║          m.epit('').splitlines(), 'web', 'gen', lineterm='', n=0)))          ║
║      EOF                                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝

A 2026-09-08-i fejléc-átdolgozás (nyilak elhagyása, CTA-kapszula, tematikus
Megoldások-hasábok, rövidített hub-feliratok) ITT MÁR BENNE VAN.


MIÉRT KELL EZ A SZKRIPT. A fejléc 120 oldalon duplikálódik, és eddig a
`sablon.py` egy meglévő aloldalból emelte ki — tehát a szerkezete csak úgy volt
módosítható, ha valaki kézzel átírja az egyik oldalt, majd mindent újragenerál.
Innentől a menü szerkezete ITT, adatként él, és ez a szkript írja be minden
oldalba — ugyanúgy, ahogy a `lablec.py` a láblécet.

MI VÁLTOZOTT A KORÁBBI MENÜHÖZ KÉPEST. A panel eddig csak a HUB szintet
mutatta: a látogató a menüből nem látta, hogy egy hub alatt hét aloldal van, és
hogy azok alatt még egy termékcsalád is. Most a hub alatt ott a saját
aloldallistája, a termékcsaládok pedig külön oszlopot kapnak.

A PANEL ELHELYEZÉSE. A panel rögzített, 48rem szélességű, három hasábbal, és a
NAVIGÁCIÓS BLOKKHOZ igazodik, nem az egyes menüponthoz: 1280 képpontos ablakban
a középső menüponthoz kötve se balra, se jobbra nem férne el. Így viszont
minden menüpontnál ugyanott nyílik, és a nyitó gombon ülő csúcs mondja meg,
melyikből. A rendezés az app.css 5.12b szakaszában él.

SORREND: a lablec.py után is futtatható, a kettő nem érinti egymást. A
`sablon.py` a fejlécet egy meglévő oldalból emeli ki, ezért ha ITT módosítasz,
előbb EZT futtasd, és csak utána az oldalgenerátorokat.
"""
import pathlib, re

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

# ---------------------------------------------------------------------------
# A MENÜ SZERKEZETE. Kategóriánként: (menüfelirat, kategória URL, hubok).
# Hub: (ikon, felirat, URL vagy None, aloldalak). Aloldal: (felirat, URL) —
# vagy (felirat, URL, [alaloldalak]) a termékcsaládoknál.
#
# A `None` URL azt jelenti, hogy a hubnak nincs saját oldala; ilyenkor a
# felirat nem hivatkozás, csak oszlopcím.
#
# A TERMÉKCSALÁDOK a fában a technológia ALATT vannak (Biológiai → A.B.Clear).
# A panelen a SZÜLŐJÜK ALATT állnak, behúzva (`mega-csoport-gyerek`) — korábban
# saját hasábot kaptak egy `↳` nyíllal, de a rács sorfolytonos kiosztása miatt a
# szomszédjuk lehetett egy másik technológia is, és az A.B.Clear úgy festett,
# mintha az EPURECO testvére volna. A hovatartozást a GYEREK halmaz mondja meg.
# ---------------------------------------------------------------------------
# Azok a hubok, amelyek az ELŐTTÜK álló hub gyerekei (termékcsalád).
GYEREK = {'megoldasok/ab-clear', 'megoldasok/epureco'}

# Ahol gyerek is van, ott a hasábok TEMATIKUSAK: egy hasáb több csoportot tart,
# és a gyerek a szülője alatt marad. A többi kategóriában maradt a régi kiosztás
# (egy hub = egy hasáb), mert ott nincs mit összetartani.
HASAB_TEMAK = {
    'Megoldások': [['megoldasok/', 'megoldasok/nagyobb-es-kozossegi-rendszerek',
                    'megoldasok/alternativak'],
                   ['megoldasok/biologiai-szennyviztisztitas', 'megoldasok/ab-clear'],
                   ['megoldasok/oldomedences-rendszer', 'megoldasok/epureco']],
}
# ---------------------------------------------------------------------------
MENU = [
    ('Kiindulópont', 'helyzetem/', [
        ('nav-kozcsatorna', 'Nincs közcsatorna',
         'helyzetem/nincs-elerheto-kozcsatorna', [
             ('Milyen megoldási lehetőségek vannak?', 'helyzetem/milyen-megoldasi-lehetosegek-vannak'),
             ('Közcsatorna vagy egyedi rendszer?', 'helyzetem/kozcsatorna-vagy-egyedi-rendszer'),
             ('Milyen adatokat kell összegyűjteni?', 'helyzetem/milyen-adatokat-kell-osszegyujteni'),
             ('Projektindító / helyzetfelmérő', 'helyzetem/projektindito'),
         ]),
        ('telek', 'Telekvásárlás, új építés',
         'helyzetem/telekvasarlas-vagy-uj-epites-elott-allok', [
             ('Alkalmas lehet-e a telek?', 'helyzetem/alkalmas-lehet-e-a-telek'),
             ('Talaj, talajvíz és vízelhelyezés', 'helyzetem/talaj-talajviz-es-vizelhelyezes'),
             ('Milyen dokumentumokra lehet szükség?', 'helyzetem/milyen-dokumentumokra-lehet-szukseg'),
             ('Telekadat-ellenőrzőlista', 'helyzetem/telekadat-ellenorzolista'),
             ('Helyszíni felmérés', 'helyzetem/helyszini-felmeres'),
         ]),
        ('emeszto', 'Emésztő kiváltása',
         'helyzetem/meglevo-emesztot-szeretnek-kivaltani', [
             ('Mikor indokolt a csere?', 'helyzetem/mikor-indokolt-a-csere'),
             ('Emésztő, oldómedence vagy biológiai?', 'helyzetem/emeszto-oldomedence-vagy-biologiai'),
             ('Teljes költség és megtérülés', 'helyzetem/teljes-koltseg-es-megterules'),
             ('Meglévő rendszer felmérése', 'helyzetem/meglevo-rendszer-felmerese'),
             ('Költség- és projektbrief', 'helyzetem/koltseg-es-projektbrief'),
         ]),
        ('nyaralo', 'Nyaraló, szezonális ház',
         'helyzetem/nyaralo-vagy-szezonalisan-hasznalt-ingatlan', [
             ('Mit jelent az időszakos terhelés?', 'helyzetem/mit-jelent-az-idoszakos-terheles'),
             ('Biológiai rendszer vagy oldómedence?', 'helyzetem/biologiai-rendszer-vagy-oldomedence'),
             ('Hosszabb távollét és újraindítás', 'helyzetem/hosszabb-tavollet-es-ujrainditas'),
             ('Szezonális esettanulmányok', 'helyzetem/szezonalis-esettanulmanyok'),
             ('Használati profil elkészítése', 'helyzetem/hasznalati-profil'),
         ]),
        ('epitkezes', 'Családi ház',
         'helyzetem/csaladi-hazhoz-keresek-rendszert', [
             ('Megoldástípus kiválasztása', 'helyzetem/megoldastipus-kivalasztasa'),
             ('Telekalkalmasság', 'helyzetem/telekalkalmassag'),
             ('Kapacitás és létszám', 'helyzetem/kapacitas-es-letszam'),
             ('Költség és telepítés', 'helyzetem/koltseg-es-telepites'),
             ('Ajánlatkérési készültség', 'helyzetem/ajanlatkeresi-keszultseg'),
         ]),
        ('nav-vallalkozas', 'Vállalkozás, intézmény',
         'helyzetem/vallalkozas-vagy-intezmeny-szamara-keresek-megoldast', [
             ('Panziók és szálláshelyek', 'helyzetem/vallalkozas-panziok-es-szallashelyek'),
             ('Éttermek és nagykonyhák', 'helyzetem/vallalkozas-ettermek-es-nagykonyhak'),
             ('Iskolák és intézmények', 'helyzetem/vallalkozas-iskolak-es-intezmenyek'),
             ('Kempingek és közösségi létesítmények', 'helyzetem/vallalkozas-kempingek-es-kozossegi'),
             ('Üzemek és speciális terhelések', 'helyzetem/vallalkozas-uzemek-es-specialis-terhelesek'),
             ('Szakmai projektbrief', 'helyzetem/vallalkozas-szakmai-projektbrief'),
         ]),
        ('nav-szerviz', 'Már van rendszerem',
         'helyzetem/mar-van-rendszerem-segitsegre-van-szuksegem', []),
    ]),

    ('Megoldások', 'megoldasok/', [
        ('nav-attekintes', 'Áttekintés', 'megoldasok/', [
            ('Megoldástípusok összehasonlítása', 'megoldasok/megoldastipusok-osszehasonlitasa'),
            ('Melyik megoldás mikor megfelelő?', 'megoldasok/melyik-megoldas-mikor-megfelelo'),
            ('Kizáró és korlátozó feltételek', 'megoldasok/kizaro-es-korlatozo-feltetelek'),
            ('Megoldástípus-előszűrő', 'megoldasok/megoldastipus-eloszuro'),
        ]),
        ('nav-biologiai', 'Biológiai tisztítás',
         'megoldasok/biologiai-szennyviztisztitas', [
             ('Hogyan működik?', 'megoldasok/biologiai-hogyan-mukodik'),
             ('Kinek megfelelő?', 'megoldasok/biologiai-kinek-megfelelo'),
             ('Mikor nem megfelelő?', 'megoldasok/biologiai-mikor-nem-megfelelo'),
             ('Telek- és terhelési feltételek', 'megoldasok/biologiai-telek-es-terhelesi-feltetelek'),
             ('Üzemeltetés és karbantartás', 'megoldasok/biologiai-uzemeltetes-es-karbantartas'),
             ('Költségtényezők', 'megoldasok/biologiai-koltsegtenyezok'),
             ('Kapcsolódó esettanulmányok', 'megoldasok/biologiai-esettanulmanyok'),
         ]),
        ('biologiai', 'A.B.Clear', 'megoldasok/ab-clear', [
            ('Modellek és kapacitások', 'megoldasok/ab-clear-modellek-es-kapacitasok'),
            ('Műszaki adatok', 'megoldasok/ab-clear-muszaki-adatok'),
            ('Iszapzsákos technológia', 'megoldasok/ab-clear-iszapzsakos-technologia'),
            ('Telepítési feltételek', 'megoldasok/ab-clear-telepitesi-feltetelek'),
            ('Dokumentumok és tanúsítványok', 'megoldasok/ab-clear-dokumentumok'),
            ('Kapcsolódó referenciák', 'megoldasok/ab-clear-referenciak'),
        ]),
        ('nav-mukodes', 'Oldómedencés rendszer', 'megoldasok/oldomedences-rendszer', [
            ('Hogyan működik?', 'megoldasok/oldomedence-hogyan-mukodik'),
            ('Kinek megfelelő?', 'megoldasok/oldomedence-kinek-megfelelo'),
            ('Mikor nem megfelelő?', 'megoldasok/oldomedence-mikor-nem-megfelelo'),
            ('Tisztítómező és területigény', 'megoldasok/oldomedence-tisztitomezo'),
            ('Szippantás és karbantartás', 'megoldasok/oldomedence-szippantas-es-karbantartas'),
            ('Kapcsolódó esettanulmányok', 'megoldasok/oldomedence-esettanulmanyok'),
        ]),
        ('oldomedence', 'EPURECO', 'megoldasok/epureco', [
            ('Modellek és kapacitások', 'megoldasok/epureco-modellek-es-kapacitasok'),
            ('Műszaki adatok', 'megoldasok/epureco-muszaki-adatok'),
            ('Telepítési feltételek', 'megoldasok/epureco-telepitesi-feltetelek'),
            ('Dokumentumok', 'megoldasok/epureco-dokumentumok'),
        ]),
        ('nav-kozossegi', 'Nagyobb rendszerek',
         'megoldasok/nagyobb-es-kozossegi-rendszerek', [
             ('Kapacitási és projektkategóriák', 'megoldasok/nagyobb-kapacitasi-kategoriak'),
             ('Terhelési profil', 'megoldasok/nagyobb-terhelesi-profil'),
             ('Előkezelés és kiegészítők', 'megoldasok/nagyobb-elokezeles-es-kiegeszitok'),
             ('Monitoring és üzemeltetés', 'megoldasok/nagyobb-monitoring-es-uzemeltetes'),
             ('Engedélyezés', 'megoldasok/nagyobb-engedelyezes'),
             ('Intézményi esettanulmányok', 'megoldasok/nagyobb-esettanulmanyok'),
             ('Szakmai konzultáció', 'megoldasok/nagyobb-szakmai-konzultacio'),
         ]),
        ('nav-alternativak', 'Alternatívák', 'megoldasok/alternativak', []),
    ]),

    ('Előkészítés', 'projekt-elokeszites/', [
        ('nav-talaj', 'Telekalkalmasság', 'projekt-elokeszites/telekalkalmassag', [
            ('Telekalkalmasság áttekintése', 'projekt-elokeszites/telekalkalmassag-attekintese'),
            ('Talaj és szivárgóképesség', 'projekt-elokeszites/talaj-es-szivargokepesseg'),
            ('Talajvíz', 'projekt-elokeszites/talajviz'),
            ('Kút és védőtávolság', 'projekt-elokeszites/kut-es-vedotavolsag'),
            ('Telekméret és rendelkezésre álló terület', 'projekt-elokeszites/telekmeret-es-szabad-terulet'),
            ('Lejtés és csőmélység', 'projekt-elokeszites/lejtes-es-csomelyseg'),
            ('Járműterhelés és hozzáférés', 'projekt-elokeszites/jarmuterheles-es-hozzaferes'),
            ('Hogyan gyűjtsem össze a telekadatokat?', 'projekt-elokeszites/telekadatok-osszegyujtese'),
            ('Telek- és vízelhelyezési előszűrő', 'projekt-elokeszites/telek-es-vizelhelyezesi-eloszuro'),
        ]),
        ('nav-vizelvezetes', 'Víz elhelyezése',
         'projekt-elokeszites/tisztitott-viz-elhelyezese', [
             ('Elszivárogtatás', 'projekt-elokeszites/elszivarogtatas'),
             ('Tisztítómező', 'projekt-elokeszites/tisztitomezo'),
             ('Gyökérzónás elhelyezés', 'projekt-elokeszites/gyokerzonas-elhelyezes'),
             ('Magas talajvízi helyzetek', 'projekt-elokeszites/magas-talajvizi-helyzetek'),
             ('Szivárogtatási vizsgálat', 'projekt-elokeszites/szivarogtatasi-vizsgalat'),
             ('Mikor szükséges szakértő?', 'projekt-elokeszites/mikor-szukseges-szakerto'),
         ]),
        ('nav-terheles', 'Terhelés és kapacitás',
         'projekt-elokeszites/terheles-es-kapacitas', [
             ('Lakosegyenérték', 'projekt-elokeszites/lakosegyenertek'),
             ('Személyszám és vízfogyasztás', 'projekt-elokeszites/szemelyszam-es-vizfogyasztas'),
             ('Átlag- és csúcsterhelés', 'projekt-elokeszites/atlag-es-csucsterheles'),
             ('Szezonális használat', 'projekt-elokeszites/szezonalis-hasznalat'),
             ('Panziók és vendéglátás', 'projekt-elokeszites/panziok-es-vendeglatas'),
             ('Intézményi terhelés', 'projekt-elokeszites/intezmenyi-terheles'),
             ('Speciális vagy ipari szennyvíz', 'projekt-elokeszites/specialis-vagy-ipari-szennyviz'),
             ('Terhelési profil és előminősítő', 'projekt-elokeszites/terhelesi-profil-eloszuro'),
         ]),
    ]),
]

# Az a három kategória, amelynek még nincs tartalma — a menüben szerepelnek,
# mert a sitemap tartalmazza őket, de a panel csak a tervezett hubokat sorolja
# fel, hivatkozás nélkül. Így a látogató látja a szerkezetet, de nem fut 404-re.
KESZUL = [
    ('Tudástár', ['Tudástár kezdőoldal', 'Megoldások és működés', 'Telek, talaj és víz',
                  'Terhelés és méretezés', 'Engedélyezés és megfelelőség',
                  'Költség és megvalósítás', 'Üzemeltetés és hibamegelőzés',
                  'Vízminőség és iszap', 'Fogalomtár', 'Gyakorlati útmutatók',
                  'Kereshető GYIK']),
    ('Eredmények', ['Eredmények áttekintése', 'Esettanulmányok', 'Projektadatbázis',
                    'Műszaki bizonyítékok', 'Tanúsítványok és dokumentumok',
                    'Ügyféltapasztalatok']),
]

# A három másodlagos kategória a sitemapban szerepel, de MÉG NEM ÉPÜLT MEG.
# Ezért felirat, nem hivatkozás: a látogató látja a szerkezetet, de nem fut
# 404-re. Amint elkészül egy szakasz, ide kerül az URL-je a None helyére.
MASODLAGOS = [('Ügyféltámogatás', None),
              ('Partnereknek', None),
              ('ÖkoTech-Home', None)]

TEL, TEL_HREF = '+36 33 200 211', 'tel:+3633200211'
MAIL = 'kapcsolat@okotechhome.hu'
CIM = '2509 Esztergom, Strázsa u. 12.'


def slug(s):
    return re.sub(r'[^a-z]+', '-', s.lower()
                  .translate(str.maketrans('áéíóöőúüű', 'aeiooouuu'))).strip('-')


def epit(elo=''):
    """`elo` az útvonal-előtag: '' a gyökérben, '../' az aloldalakon."""

    def h(u):
        return f'{elo}{u}'

    menuk = []
    for cim, katurl, hubok in MENU:
        az = slug(cim)
        # Hubonként egy csoport (fejléc + aloldallista), URL szerint elérhetően.
        csoportok = {}
        burok_nelkul = {}
        sorrend = []
        for ikon, hcim, hurl, alok in hubok:
            fej = (f'<a class="mega-link" href="{h(hurl)}">'
                   f'<span class="mega-ico" aria-hidden="true">'
                   f'<span class="icon icon-inline icon-inline-lg icon-{ikon}"></span></span>'
                   f'<span class="mega-label type-ui-body">{hcim}</span></a>'
                   ) if hurl else (
                   f'<p class="mega-link mega-link-passziv">'
                   f'<span class="mega-ico" aria-hidden="true">'
                   f'<span class="icon icon-inline icon-inline-lg icon-{ikon}"></span></span>'
                   f'<span class="mega-label type-ui-body">{hcim}</span></p>')
            alista = ''
            if alok:
                li = '\n'.join(
                    f'                        <li><a class="mega-alink type-ui-caption" '
                    f'href="{h(u)}">{c}</a></li>' for c, u in alok)
                alista = ('\n                      <ul class="mega-alista" role="list">\n'
                          f'{li}\n                      </ul>')
            oszt = 'mega-csoport mega-csoport-gyerek' if hurl in GYEREK else 'mega-csoport'
            kulcs = hurl or hcim
            # A csoport-burok CSAK a tematikus hasábokhoz kell; ahol egy hub =
            # egy hasáb, ott fölösleges elem volna a fában, ezért két alakot
            # tartunk el ugyanabból.
            csoportok[kulcs] = ('                    <div class="' + oszt + '">\n'
                                f'                      {fej}{alista}\n'
                                '                    </div>')
            burok_nelkul[kulcs] = ('                    ' + fej
                                   + alista.replace('\n                      ', '\n                    ')
                                           .replace('\n                        ', '\n                      '))
            sorrend.append(kulcs)

        temak = HASAB_TEMAK.get(cim)
        if temak:
            # Tematikus hasábok: egy hasáb több csoportot tart.
            oszlopok = ['                  <li class="mega-oszlop">\n'
                        + '\n'.join(csoportok[k] for k in hasab)
                        + '\n                  </li>' for hasab in temak]
        else:
            # Régi kiosztás: egy hub = egy hasáb, a rács tölti sorfolytonosan.
            oszlopok = ['                  <li class="mega-oszlop">\n'
                        + burok_nelkul[k]
                        + '\n                  </li>' for k in sorrend]
        menuk.append(f'''          <li class="nav-item">
            <button type="button" class="nav-link nav-trigger type-ui-nav"
                    aria-expanded="false" aria-controls="mega-{az}">
              {cim}
            </button>
            <div class="mega" id="mega-{az}" hidden>
              <div class="mega-inner">
                <div class="mega-fej">
                  <p class="type-data-eyebrow mega-eyebrow">{cim}</p>
                  <a class="text-link mega-attekintes" href="{h(katurl)}"><span class="link-label">Áttekintés<span class="action-arrow-end" aria-hidden="true">&rarr;</span></span></a>
                </div>
                <ul class="mega-oszlopok" role="list">
{chr(10).join(oszlopok)}
                </ul>
              </div>
            </div>
          </li>''')

    for cim, tervek in KESZUL:
        az = slug(cim)
        li = '\n'.join(
            f'                      <li><span class="mega-alink mega-alink-passziv '
            f'type-ui-caption">{t}</span></li>' for t in tervek)
        menuk.append(f'''          <li class="nav-item">
            <button type="button" class="nav-link nav-trigger type-ui-nav"
                    aria-expanded="false" aria-controls="mega-{az}">
              {cim}
            </button>
            <div class="mega" id="mega-{az}" hidden>
              <div class="mega-inner">
                <div class="mega-fej">
                  <p class="type-data-eyebrow mega-eyebrow">{cim}</p>
                  <span class="type-ui-caption mega-keszul">Ez a szakasz még készül. Kérdésével addig is fordulhat hozzánk.</span>
                </div>
                <ul class="mega-oszlopok" role="list">
                  <li class="mega-oszlop">
                    <p class="mega-link mega-link-passziv"><span class="mega-label type-ui-body">A szakasz készül</span></p>
                    <ul class="mega-alista" role="list">
{li}
                    </ul>
                  </li>
                </ul>
              </div>
            </div>
          </li>''')

    def masod(c, u):
        return (f'<a class="topbar-link type-ui-label" href="{h(u)}">{c}</a>' if u
                else f'<span class="topbar-link topbar-link-passziv type-ui-label">{c}</span>')
    masodlagos = '\n'.join(
        f'        <li>{masod(c, u)}</li>'
        + ('\n        <li aria-hidden="true" class="topbar-sep">|</li>'
           if (c, u) != MASODLAGOS[-1] else '')
        for c, u in MASODLAGOS)

    return f'''<a class="skip-link" href="#fotartalom">Ugrás a tartalomra</a>

<!-- ==========================================================================
     OLDALFEJLÉC — kontaktsáv + HÁROMSZINTŰ megamenü
     A navigáció natív `details`/`summary`: szűk nézetben lenyitható panel,
     asztali nézetben a lenyitó gomb elrejtve, a lista nyitva. JS csak annyit
     tesz, hogy szűk nézetben becsukja az alapból nyitott panelt.

     A menü SZERKEZETE a scripts/oldalgyartas/fejlec.py fájlban él, és onnan
     kerül minden oldalba. NE ITT szerkeszd — a következő futtatás felülírja.
     ========================================================================== -->
<header class="site-header">

  <div class="topbar">
    <div class="topbar-inner">
      <ul class="topbar-list" role="list">
        <li class="topbar-item type-ui-label topbar-hide-narrow">
          <span class="icon icon-inline icon-helyszin topbar-icon" aria-hidden="true"></span>
          {CIM}
        </li>
        <li>
          <a class="topbar-link type-ui-label" href="mailto:{MAIL}">
            <span class="icon icon-inline icon-email topbar-icon" aria-hidden="true"></span>
            {MAIL}
          </a>
        </li>
        <li>
          <a class="topbar-link type-ui-label" href="{TEL_HREF}">
            <span class="icon icon-inline icon-telefon topbar-icon" aria-hidden="true"></span>
            {TEL}
          </a>
        </li>
      </ul>

      <!-- A sitemap nyolc főkategóriájából a három másodlagos itt kap helyet:
           a fő sávban nyolc nagybetűs menüpont nem fér el a logó és a CTA mellett. -->
      <ul class="topbar-list topbar-hide-narrow" role="list">
{masodlagos}
      </ul>
    </div>
  </div>

  <!-- A kontaktsáv elgörög, a fő sáv tapad (sticky), finom árnyékkal. -->
  <div class="header-main">
  <div class="header-inner">
    <!-- Két rajz, a téma választ: az `img`-ként betöltött SVG nem látja a
         dokumentum `data-theme` attribútumát, ezért a szóvédjegy színe nem
         tudná követni a váltást. Az `alt` csak az egyiken van kitöltve, a
         másik `alt=""` — különben a képernyőolvasó kétszer mondaná ki a
         cégnevet, hiszen a hivatkozásnak már van `aria-label`-je. -->
    <a class="site-logo" href="{elo or './'}" aria-label="ÖkoTech Home — főoldal">
      <img class="site-logo-vilagos" src="{elo}assets/img/logo-okotechhome.svg"
           width="928" height="290" alt="ÖkoTech Home" decoding="async">
      <img class="site-logo-sotet" src="{elo}assets/img/logo-okotechhome-sotet.svg"
           width="928" height="290" alt="" decoding="async">
    </a>

    <details class="nav-drawer" open>
      <summary class="nav-toggle type-ui-nav">Menü</summary>
      <nav class="site-nav" aria-label="Fő navigáció">
        <ul class="nav-list" role="list">
{chr(10).join(menuk)}
        </ul>
      </nav>
    </details>

    <!-- TÉMAVÁLTÓ. `role="switch"`: a gomb NEVE állandó („Sötét téma"), az
         állapotot az `aria-checked` hordozza — ez a kapcsolók ARIA-mintája. A
         lebegő súgó a MŰVELETET mondja ki, és `aria-hidden`, hogy a
         képernyőolvasó ne ismételje meg ugyanazt más szavakkal.
         A gomb csak akkor látszik, ha a tema.js lefutott (app.css 5.12c). -->
    <div class="tema-doboz">
      <button type="button" class="tema-valto" role="switch" aria-checked="false"
              data-tema-valto>
        <span class="visually-hidden">Sötét téma</span>
        <span class="tema-sin" aria-hidden="true">
          <span class="icon icon-inline icon-tema-nap tema-jel"></span>
          <span class="icon icon-inline icon-tema-hold tema-jel"></span>
          <span class="tema-fogo">
            <span class="icon icon-inline icon-tema-nap tema-jel"></span>
            <span class="icon icon-inline icon-tema-hold tema-jel"></span>
          </span>
        </span>
      </button>
      <span class="tema-tipp type-ui-caption" aria-hidden="true"
            data-tema-tipp>Váltás sötét témára</span>
    </div>

    <!-- CTA-KAPSZULA. Három lépés egyetlen sínben, a döntés sorrendjében:
         konzultáció → ajánlat → megrendelés. A csúszó jelölő díszítés, ezért
         `aria-hidden`; a helyzetét CSS mondja meg (app.css 5.12d). -->
    <div class="cta-kapszula" role="group" aria-label="Kapcsolatfelvétel">
      <span class="cta-jelolo" aria-hidden="true"></span>
      <a class="cta-szegmens" href="{h('konzultacio')}">Konzultáció</a>
      <a class="cta-szegmens" href="{h('ajanlat')}">Ajánlat</a>
      <a class="cta-szegmens" href="{h('megrendeles')}">Megrendelés</a>
    </div>
  </div>
  </div>

</header>'''


def temaszkript(s: str, elo: str) -> str:
    """A témaváltó szkriptjét a `<head>`-be teszi, a stíluslap után.

    HALASZTÁS NÉLKÜL töltődik, szemben az összes többi szkripttel: a témát a
    `<html>` `data-theme` attribútuma hordozza, és ha ez a törzs végén dőlne
    el, minden oldalbetöltéskor felvillanna a világos oldal, mielőtt sötétre
    vált. Néhány sorról van szó, közvetlenül a stíluslap után.
    """
    if 'assets/js/tema.js' in s:
        return s
    minta = re.compile(r'(<link rel="stylesheet" href="[^"]*assets/css/app\.css[^"]*">)')
    if not minta.search(s):
        return s
    return minta.sub(
        r'\1\n<!-- A témát a `data-theme` hordozza; ez a szkript írja ki, még a törzs\n'
        '     feldolgozása előtt — így nincs villanás. Lásd assets/js/tema.js. -->\n'
        f'<script src="{elo}assets/js/tema.js?v=1"></script>', s, count=1)


# A nyelvi alkönyvtárak fejlécét EZ A SZKRIPT NEM ÍRJA. A `MENU` magyar
# feliratokat tartalmaz, és a hivatkozásai a magyar szlugokra mutatnak — egy
# futtatás visszaírná a magyar fejlécet az angol lapra, némán.
#
# AMIKOR AZ ANGOL FA MEGNŐ, itt a teendő: a `MENU` szerkezetét nyelvenkénti
# táblává kell bontani (felirat + szlug párokkal), és az `epit()`-nek nyelvet
# is át kell adni. Amíg csak a nyitólap van meg angolul, ez a kihagyás az
# olcsóbb és biztonságosabb megoldás — a kézzel fordított fejléc megmarad.
NYELVI_KONYVTARAK = {'en'}


if __name__ == '__main__':
    minta = re.compile(r'<a class="skip-link".*?</header>', re.S)
    n, sz = 0, 0
    for p in sorted(WEB.rglob('*.html')):
        if p.name in ('401.html', '403.html', '404.html', '500.html'):
            continue                      # a hibaoldalak önhordók, saját fejlécük van
        if p.relative_to(WEB).parts[0] in NYELVI_KONYVTARAK:
            continue                      # idegen nyelvű fa — lásd a megjegyzést fent
        s = p.read_text(encoding='utf-8')
        if not minta.search(s):
            print(f'  ! nincs fejléc: {p.relative_to(WEB)}')
            continue
        elo = '' if p.parent == WEB else '../'
        uj = minta.sub(lambda _: epit(elo), s, count=1)
        elotte = uj
        uj = temaszkript(uj, elo)
        sz += uj != elotte
        p.write_text(uj, encoding='utf-8')
        n += 1
    print(f'témaszkript beszúrva: {sz} oldalon')
    print(f'fejléc beírva: {n} oldal')
