#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""12. szekció — Dokumentált projektek és használói tapasztalatok,
   valamint a hozzá tartozó négy esettanulmány-oldal.

A szöveg a végleges szövegdokumentum 12. szekciójából való, szó szerint.
Ezek VALÓDI, megvalósult projektek — a számokat és az évszámokat nem
kerekítjük és nem szépítjük.
"""
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import sec_numbered, sec_split, sec_prose, sec_cta, sec_faq

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

# ---------------------------------------------------------------- projektek
PROJEKTEK = [
    dict(
        slug='csikvand', kep='csikvand', kiemelt=True,
        cim='Csikvánd — 128 egyedi berendezés egy egész faluban',
        rovid='Csikvánd', ev='2017–2018', hely='Győr-Moson-Sopron megye',
        szam='128 berendezés', szamalatt='országos elsőség',
        alt='Légifelvétel egy kisalföldi magyar faluról: cserepes tetők kertek és gyümölcsösök között, körben szántóföld',
        szoveg='Csikvándon nem épült ki közcsatorna, így az egész település szennyvízkezelését '
               'kellett megoldani, ingatlanonként telepített egyedi berendezésekkel. 2017 és 2018 '
               'során 128 A.B. Clear berendezést telepítettünk és üzemeltünk be, házanként. Ez volt '
               'Magyarországon az elsőként lezárt, elkészült szennyvíztisztítási projekt a '
               'Vidékfejlesztési Program pályázati keretében.',
        lead='Egy egész falu szennyvízkezelése közcsatorna nélkül, ingatlanonként telepített '
             'berendezésekkel — és az ország első lezárt projektje a Vidékfejlesztési Program '
             'keretében.',
        adatok=[('Helyszín', 'Csikvánd, Győr-Moson-Sopron megye'),
                ('Kivitelezés éve', '2017–2018'),
                ('Megoldás', 'ingatlanonkénti egyedi berendezés'),
                ('Darabszám', '128 db A.B. Clear'),
                ('Finanszírozás', 'Vidékfejlesztési Program pályázati keret')],
        miert=[
            '<strong>Nem volt közcsatorna, és nem is épült.</strong> A településen a hálózat '
            'kiépítése nem volt reális, ezért a szennyvízkezelést ingatlanonként kellett megoldani.',
            '<strong>Százhuszonnyolc külön telek, százhuszonnyolc külön adottság.</strong> Minden '
            'ingatlanon külön kellett megnézni a csőkivezetés mélységét, a talajt és a kezelt víz '
            'elhelyezését — ez a projekt legnagyobb szervezési feladata.',
            '<strong>Pályázati keret, kötött határidővel.</strong> A Vidékfejlesztési Program '
            'elszámolási rendje pontos ütemezést kívánt; a projekt az országban elsőként zárult le.'],
    ),
    dict(
        slug='bakonypeterd', kep='bakonypeterd', kiemelt=False,
        cim='Bakonypéterd — központi telep, amelyet ma a közműszolgáltató üzemeltet',
        rovid='Bakonypéterd', ev='2018', hely='központi telep',
        szam='4 × 50 fős egység', szamalatt='közműszolgáltató üzemelteti',
        alt='Kisméretű szennyvíztisztító telep egy magyar falu szélén: négy összekötött hengeres egység betonalapon, kerítés mögött',
        szoveg='Bakonypéterd nem ingatlanonkénti berendezéseket, hanem központi szennyvíztisztítót '
               'kapott — a tervezéstől a működő telepig. A telep négy darab 50 fős berendezés '
               'összekötésével működik, teljesen elektronikus vezérlésű, távüzemben irányítható. '
               'A tervezést is mi vállaltuk, a próbaüzemet mi folytattuk le. A telepet azóta a '
               'területi közműszolgáltató, a Pannon-Víz Zrt. üzemelteti.',
        lead='Nem ingatlanonkénti berendezések, hanem központi telep — a tervezéstől a működő '
             'üzemig. Ma a területi közműszolgáltató üzemelteti.',
        adatok=[('Helyszín', 'Bakonypéterd'),
                ('Kivitelezés éve', '2018'),
                ('Megoldás', 'központi szennyvíztisztító telep'),
                ('Kapacitás', '4 db 50 fős berendezés összekötve'),
                ('Vezérlés', 'teljesen elektronikus, távüzemben irányítható'),
                ('Üzemeltető', 'Pannon-Víz Zrt. (területi közműszolgáltató)')],
        miert=[
            '<strong>Központi telep, nem házankénti berendezés.</strong> A település szerkezete és '
            'a terhelés eloszlása ezt tette ésszerűvé; a szennyvíz egy ponton kezelődik.',
            '<strong>A tervezés is a feladat része volt.</strong> Nem kész tervhez szállítottunk '
            'berendezést: a méretezéstől a próbaüzemig végigvittük a projektet.',
            '<strong>Az átadás után közműszolgáltatóhoz került.</strong> A telepet ma a Pannon-Víz '
            'Zrt. üzemelteti — ez önmagában is minősíti a kialakítást, mert a szolgáltató a saját '
            'üzemeltetési rendjébe illesztette.'],
    ),
    dict(
        slug='diosbereny', kep='diosbereny', kiemelt=False,
        cim='Diósberény — 90 egyedi berendezés, saját csapattal',
        rovid='Diósberény', ev='2022', hely='Tolna megye',
        szam='90 berendezés', szamalatt='',
        alt='Magyar falusi utca dombos Tolna megyei tájban: előkertes házak az út mentén, a domboldalon szőlők',
        szoveg='Diósberényben szintén településszintű, ingatlanonkénti egyedi szennyvízkezelésre '
               'volt szükség. 2022-ben 90 A.B. Clear berendezést adtunk át, saját csapattal '
               'telepítve és beüzemelve. A rendszerek a lakosok megelégedésére működnek.',
        lead='Településszintű, ingatlanonkénti szennyvízkezelés: kilencven berendezés, saját '
             'csapattal telepítve és beüzemelve.',
        adatok=[('Helyszín', 'Diósberény, Tolna megye'),
                ('Kivitelezés éve', '2022'),
                ('Megoldás', 'ingatlanonkénti egyedi berendezés'),
                ('Darabszám', '90 db A.B. Clear'),
                ('Telepítés', 'saját csapattal')],
        miert=[
            '<strong>Ugyanaz a feladat, mint Csikvándon — négy évvel később.</strong> A '
            'közcsatorna hiánya itt is településszintű megoldást kívánt.',
            '<strong>Saját csapat, alvállalkozó nélkül.</strong> A telepítést és a beüzemelést '
            'végig a saját munkatársaink végezték; ez a kivitelezés egységességén látszik.',
            '<strong>A visszajelzés a lakosoktól jön.</strong> A rendszerek azóta is a lakosok '
            'megelégedésére működnek.'],
    ),
    dict(
        slug='obudavar', kep='obudavar', kiemelt=False,
        cim='Óbudavár — ahol elkezdődött',
        rovid='Óbudavár', ev='2011', hely='Balaton-felvidék',
        szam='minisztériumi mintaprojekt', szamalatt='a kezdet',
        alt='Apró dombtetői magyar falu a Balaton-felvidéken: fehérre meszelt házak szőlők és gyümölcsösök között, háttérben bazalthegyek',
        szoveg='2011-ben, minisztériumi mintaprojekt keretében egy egész kistelepülés '
               'szennyvízkezelését kellett megoldani. A telepítést és beüzemelést saját '
               'munkatársainkkal végeztük, alvállalkozót kizárólag a négy monitoringkút '
               'létesítéséhez vontunk be.',
        idezet=('Ami nálam működik, az tökéletes. Csendes, és szinte hihetetlen, hogy az ilyen '
                'anyagoknak nincs szaga. A faluban bevált a rendszer.',
                'Bodor Antal', 'Óbudavár polgármestere'),
        lead='Minisztériumi mintaprojekt 2011-ben — az első településszintű munkánk, és az az '
             'alap, amire minden későbbi projekt épült.',
        adatok=[('Helyszín', 'Óbudavár, Balaton-felvidék'),
                ('Kivitelezés éve', '2011'),
                ('Keret', 'minisztériumi mintaprojekt'),
                ('Megoldás', 'településszintű szennyvízkezelés'),
                ('Alvállalkozó', 'kizárólag a négy monitoringkút létesítéséhez')],
        miert=[
            '<strong>Mintaprojekt volt, tehát mérték.</strong> A minisztériumi keret együtt járt '
            'a monitorozással: négy monitoringkút létesült a hatás követésére.',
            '<strong>Ez volt az első településszintű munkánk.</strong> Amit itt tanultunk a '
            'szervezésről és a telepítésről, az minden későbbi projektben visszaköszön.',
            '<strong>Tizenöt év távlatából is működik.</strong> A polgármester visszajelzése nem '
            'az átadáskor született, hanem évekkel később.'],
    ),
]

# ------------------------------------------------------------ visszajelzések
VISSZAJELZESEK = [
    ('Végre nincs szag, és nincs több szippantás-szervezés',
     'A tisztítóberendezés hibátlanul, szagtalanul és csendben üzemel. A tisztított víz '
     'kristálytiszta. A berendezés karbantartási igénye minimális. Mindenkinek ajánlom!',
     'Windberg Péter', 'Zebegény'),
    ('Végre nincs szag, és nincs több szippantás-szervezés',
     'Megszabadultunk a szippantással járó kellemetlen szagoktól, költségektől és szervezési '
     'feladatoktól. Az utcánkban mi vagyunk a harmadik család, aki a berendezés előnyeit élvezi.',
     'Sz. Csaba', 'Vác'),
    ('A tisztított vizet tényleg használom a kertben',
     'Oly mértékben megtisztítja a szennyvizet, hogy locsolóvíznek tudjuk használni a kertünkben, '
     'az elválasztott iszap pedig kiválóan komposztálható. Nálunk közel négy éve kifogástalanul '
     'működik.', 'Szücsi Frigyes', 'Bakonykúti'),
    ('A tisztított vizet tényleg használom a kertben',
     'Jó alternatív megoldás, öntözésre nagyon jól fel tudom használni a tisztított szennyvizet.',
     'K. János', 'Nagydorog'),
    ('Nem bántuk meg — és a cég ott volt utána is',
     'Nem csak a berendezés üzembehelyezésekor kaptunk szakszerű figyelmet, hanem az utánkövetés '
     'is folyamatos!', 'Édes Orsolya', 'Budakeszi'),
    ('Nem bántuk meg — és a cég ott volt utána is',
     'Amennyiben kérdésem-kérésem volt, arra haladéktalanul korrekt választ kaptam. Két év '
     'használat után kijelenthetem, hogy nem csak környezetkímélő, hanem költséghatékony is.',
     'L. László', 'Dunabogdány'),
    ('Nem bántuk meg — és a cég ott volt utána is',
     'Nagyon jó döntés volt az ÖkoTech-et választanom a sok versenytárssal szemben. A rendszer '
     'tökéletesen működik, tudja mindazt, amit ígértek.', 'Bősz Ákos', 'Lovasberény'),
    ('Nem bántuk meg — és a cég ott volt utána is',
     'Rengeteg ötlettel, tapasztalattal segített nekünk abban, hogy a szennyvízkezelőt hibák '
     'nélkül tudjuk üzemeltetni. Az Önök cégét mindenkinek csak ajánlani tudom.',
     'Kenéz Mihály', 'turisztikai egységvezető, Balaton-felvidéki Nemzeti Park Igazgatóság'),
]


def esc(s):
    import html as h
    return h.escape(s, quote=False)


# =========================================================== főoldali szekció
def szekcio():
    kiemelt = PROJEKTEK[0]
    tobbi = PROJEKTEK[1:]

    def chip(p):
        alatt = (f'<span class="projekt-chip-alatt type-ui-caption">{esc(p["szamalatt"])}</span>'
                 if p['szamalatt'] else '')
        return (f'<p class="projekt-chip"><span class="projekt-chip-szam type-ui-card-title">'
                f'{esc(p["szam"])}</span>{alatt}</p>')

    kartyak = '\n'.join(f'''        <li class="projekt">
          <figure class="projekt-media">
            <img src="assets/img/projektek/{p['kep']}.webp" width="900" height="600"
                 alt="{esc(p['alt'])}" loading="lazy" decoding="async">
          </figure>
          <h3 class="type-ui-card-title projekt-cim">{esc(p['cim'])}</h3>
          <p class="type-ui-caption projekt-meta">
            <span class="projekt-ev type-data-value">{esc(p['ev'])}</span>
            <span aria-hidden="true">·</span> {esc(p['hely'])}
          </p>
          <p class="type-ui-body projekt-szoveg">{esc(p['szoveg'])}</p>
          {chip(p)}
          <a class="text-link projekt-link" href="eredmenyek/{p['slug']}"><span class="link-label">Megnyitom a projektet<span class="action-arrow-end" aria-hidden="true">&rarr;</span></span></a>
        </li>''' for p in tobbi)

    slide = '\n'.join(f'''          <li class="velemeny" data-velemeny{'' if i else ' data-aktiv'}{'' if i == 0 else ' hidden'}>
            <p class="type-ui-card-title velemeny-tema">{esc(t)}</p>
            <blockquote class="velemeny-idezet">
              <p class="type-display-highlight-title velemeny-szoveg">{esc(q)}</p>
              <footer class="type-ui-subtitle velemeny-nev">— {esc(n)}, {esc(h)}</footer>
            </blockquote>
          </li>''' for i, (t, q, n, h) in enumerate(VISSZAJELZESEK))

    return f'''
  <!-- ==========================================================================
       12. SZEKCIÓ — DOKUMENTÁLT PROJEKTEK ÉS HASZNÁLÓI TAPASZTALATOK
       Valódi, megvalósult projektek: a számok és az évszámok a végleges
       szövegdokumentumból valók, kerekítés nélkül. Mind a négyhez tartozik
       esettanulmány-oldal az eredmenyek/ alatt.
  =========================================================================== -->
  <section class="section" aria-labelledby="projektek-cim">
    <div class="section-inner">

      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Projektek és tapasztalatok</p>
        <h2 class="type-display-section-title section-title" id="projektek-cim">
          Nem csak családi házak — egész települések szennyvízkezelése
        </h2>
        <p class="type-ui-body section-lead">
          A legnagyobb számban családi házakhoz telepítünk, de több egész település
          szennyvízkezelését is megoldottuk, ingatlanonkénti egyedi berendezésekkel vagy
          központi teleppel.
        </p>
      </header>

      <article class="projekt-kiemelt">
        <figure class="projekt-media projekt-media-nagy">
          <img src="assets/img/projektek/{kiemelt['kep']}.webp" width="1400" height="933"
               alt="{esc(kiemelt['alt'])}" loading="lazy" decoding="async">
        </figure>
        <div class="projekt-kiemelt-torzs">
          <p class="type-data-eyebrow projekt-eyebrow">Kiemelt projekt</p>
          <h3 class="type-display-highlight-title projekt-kiemelt-cim">{esc(kiemelt['cim'])}</h3>
          <p class="type-ui-caption projekt-meta">
            <span class="projekt-ev type-data-value">{esc(kiemelt['ev'])}</span>
            <span aria-hidden="true">·</span> {esc(kiemelt['hely'])}
          </p>
          <p class="type-ui-body projekt-szoveg">{esc(kiemelt['szoveg'])}</p>
          <div class="projekt-kiemelt-alj">
            {chip(kiemelt)}
            <a class="text-link projekt-link" href="eredmenyek/{kiemelt['slug']}"><span class="link-label">Megnyitom a projektet<span class="action-arrow-end" aria-hidden="true">&rarr;</span></span></a>
          </div>
        </div>
      </article>

      <ul class="projekt-racs" role="list">
{kartyak}
      </ul>

      <p class="section-actions">
        <a class="btn btn-primary" href="eredmenyek/">További esettanulmányok</a>
      </p>

    </div>
  </section>

  <!-- Visszajelzések. A léptetés natív gombokkal megy; JS nélkül MINDEN
       vélemény látszik egymás alatt (a `hidden` attribútumot a JS teszi rá),
       tehát a tartalom sosem vész el. -->
  <section class="section" aria-labelledby="velemenyek-cim">
    <div class="section-inner">
      <div class="velemeny-keret">

        <header class="section-head section-head-start velemeny-fej">
          <h2 class="type-display-section-title section-title" id="velemenyek-cim">
            Amit a mindennapokban jelent
          </h2>
          <p class="type-ui-body section-lead">
            A projektek a számokat mutatják. Az alábbi visszajelzések azt, milyen együtt élni
            a rendszerrel — évek távlatából.
          </p>
        </header>

        <div class="velemeny-doboz" data-velemeny-doboz>
          <ul class="velemeny-lista" role="list">
{slide}
          </ul>
          <p class="velemeny-lepteto">
            <button type="button" class="velemeny-gomb" data-velemeny-elozo aria-label="Előző vélemény">
              <span aria-hidden="true">&#8249;</span>
            </button>
            <span class="type-data-value velemeny-szamlalo" data-velemeny-szamlalo
                  role="status" aria-live="polite">1 / {len(VISSZAJELZESEK)}</span>
            <button type="button" class="velemeny-gomb" data-velemeny-kovetkezo aria-label="Következő vélemény">
              <span aria-hidden="true">&#8250;</span>
            </button>
          </p>
        </div>

      </div>
    </div>
  </section>
'''


# ====================================================== esettanulmány-oldalak
def oldal(p):
    idezet = ''
    if p.get('idezet'):
        q, n, h = p['idezet']
        idezet = f'''
  <section class="section" aria-labelledby="idezet-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Visszajelzés</p>
        <h2 class="type-display-section-title section-title" id="idezet-cim">Amit a település mond</h2>
      </header>
      <blockquote class="velemeny-idezet velemeny-idezet-onallo">
        <p class="type-display-highlight-title velemeny-szoveg">{esc(q)}</p>
        <footer class="type-ui-subtitle velemeny-nev">— {esc(n)}, {esc(h)}</footer>
      </blockquote>
    </div>
  </section>
'''

    adatsorok = '\n'.join(
        f'          <tr><th scope="row" class="type-ui-subtitle">{esc(k)}</th>'
        f'<td class="type-ui-subtitle">{esc(v)}</td></tr>' for k, v in p['adatok'])

    return dict(
        file=f"eredmenyek/{p['slug']}.html",
        url=f"eredmenyek/{p['slug']}", img=p['kep'],
        title=f"{p['rovid']} — esettanulmány | ÖkoTech Home",
        desc=p['lead'],
        h1=p['cim'], alt=p['alt'], lead=p['lead'],
        crumbs=[('Főoldal', '../'), ('Eredmények', './')],
        sections=[
            f'''
  <section class="section" aria-labelledby="adatok-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Projektadatok</p>
        <h2 class="type-display-section-title section-title" id="adatok-cim">A projekt egy lapon</h2>
      </header>
      <div class="compare-scroll" role="region" aria-labelledby="adatok-cim" tabindex="0">
        <table class="compare-table">
          <tbody>
{adatsorok}
          </tbody>
        </table>
      </div>
    </div>
  </section>
''',
            sec_prose('A feladat', 'Mit kellett megoldani', [esc(p['szoveg'])]),
            sec_numbered('Háttér', 'Miért így oldottuk meg', None, p['miert']),
            idezet,
            sec_cta('Hasonló helyzet', 'Az Ön településén is ez a kérdés?',
                    ['Településszintű szennyvízkezelésnél a megoldás nem a berendezésen múlik '
                     'elsősorban, hanem azon, hogy ingatlanonkénti vagy központi kialakítás illik-e '
                     'a település szerkezetéhez, és mit enged a helyi szabályozás.',
                     'Ezt felmérés nélkül nem lehet megmondani — de az első beszélgetés '
                     'elköteleződés nélkül zajlik.'],
                    'Kapcsolatfelvétel', '../kapcsolat',
                    alt=('Vagy nézze meg a nagyobb és közösségi rendszereket',
                         '../megoldasok/nagyobb-es-kozossegi-rendszerek')),
            sec_faq([
                ('Meddig tart egy ilyen projekt?',
                 'A településméret és a kialakítás dönti el. Az ingatlanonkénti telepítés '
                 'ütemezhető, a központi telep egy összefüggő beruházás. A reális ütemtervet '
                 'a felmérés és az engedélyezési feltételek ismeretében tudjuk megadni.'),
                ('Ki üzemelteti a rendszert az átadás után?',
                 'Ingatlanonkénti kialakításnál a tulajdonos, a mi szervizhátterünkkel. Központi '
                 'telepnél az üzemeltető lehet az önkormányzat vagy a területi közműszolgáltató — '
                 'Bakonypéterden például a Pannon-Víz Zrt. vette át.'),
                ('Van pályázati lehetőség ilyen projektre?',
                 'Volt és lehet — a csikvándi projekt a Vidékfejlesztési Program keretében '
                 'valósult meg. A mindenkori kiírásokat az önkormányzatnál és a pályázati '
                 'portálokon érdemes követni; a műszaki tartalom összeállításában tudunk segíteni.'),
            ]),
        ])


if __name__ == '__main__':
    # 1) a szekció beírása a főoldalba
    p = WEB / 'index.html'
    s = p.read_text(encoding='utf-8')
    sec = szekcio()
    if 'projektek-cim' in s:
        s = re.sub(r'\n  <!-- =+\n       12\. SZEKCIÓ.*?\n  </section>\n(?=\n</main>)', sec, s, flags=re.S)
    else:
        s = s.replace('\n</main>', sec + '\n</main>', 1)
    if 'js/velemeny.js' not in s:
        s = s.replace('<script src="assets/js/ofc.js?v=1" defer></script>',
                      '<script src="assets/js/ofc.js?v=1" defer></script>\n'
                      '<script src="assets/js/velemeny.js?v=1" defer></script>')
    p.write_text(s, encoding='utf-8')
    print('index.html — 12. szekció beírva')

    # 2) a négy esettanulmány-oldal
    for pr in PROJEKTEK:
        o = oldal(pr)
        out = WEB / o['file']
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:44s} {len(out.read_text(encoding='utf-8'))//1024} KB")
