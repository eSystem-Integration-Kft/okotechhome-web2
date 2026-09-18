# -*- coding: utf-8 -*-
"""A „Biológiai szennyvíztisztító" lap ábrái.

1. ÍGY TISZTÍT — négy lépés, négy kis rajz. A lépések szövege HTML (nem az
   SVG-ben él): telefonon a rajzok egymás alá kerülnek, a szöveg pedig a
   lap betűméretén marad olvasható. Egyetlen széles SVG 360 px-en a felére
   zsugorodna, és a feliratai olvashatatlanok lennének.
   A lépések a főoldal „A tisztítási folyamat" négy lépését követik — nem
   új műszaki állítás, hanem ugyanannak a képi változata.

2. ÉVES ÜZEMELTETÉSI KÖLTSÉG — két üzemmód, halmozott sávban. A sáv SVG,
   `preserveAspectRatio="none"`-nal: a geometria a konténerrel nyúlik, a
   feliratok HTML-ben vannak. A téglalapok szélessége ATTRIBÚTUM, nem
   `style` — az éles CSP a soron belüli stílust eldobja.

A SZÍNEK TOKENBŐL JÖNNEK (`--abra-*`), mint az SBR- és MBBR-ábrákon, így a
rajz témát vált a lappal. A mozgás az app.css `motion` rétegében él,
`prefers-reduced-motion` mögött; mozgás nélkül is teljes a rajz.
"""
import html as _html


def _esc(s):
    return _html.escape(str(s), quote=True)


def _svg(tartalom, cim):
    # Dekoratív kísérőrajz: a jelentést a mellette álló HTML-szöveg hordozza,
    # ezért a képernyőolvasó elől rejtve — kétszer ne olvassa fel ugyanazt.
    # `<title>` NINCS benne: rejtett rajzban haszontalan, a SEO-ellenőrzők
    # viszont „több title elem" hibának jelzik. A `cim` a forrás olvasójának
    # szól, megjegyzésként marad a rajz előtt.
    return (f'<!-- {_esc(cim)} -->'
            f'<svg class="hub-lepes-rajz" viewBox="0 0 120 84" aria-hidden="true" focusable="false">'
            f'{tartalom}</svg>')


def _buborekok(x0, szel, y, db, r0=2.2):
    ki = []
    for i in range(db):
        cx = x0 + szel * (i + 1) / (db + 1)
        ki.append(f'<circle class="abra-bub abra-i{i}" cx="{cx:.1f}" cy="{y}" '
                  f'r="{r0 + (i % 3) * 0.5:.1f}" fill="var(--abra-kiemeles)"/>')
    return ''.join(ki)


def rajz_beerkezes():
    """A ház szennyvize a csövön a berendezésbe folyik."""
    return _svg(
        # ház
        '<path d="M8 44 L28 27 L48 44 V66 H8 Z" fill="none" stroke="var(--abra-keret)" '
        'stroke-width="2.2" stroke-linejoin="round"/>'
        '<rect x="22" y="52" width="10" height="14" rx="1.5" fill="none" stroke="var(--abra-keret)" stroke-width="1.8"/>'
        # talajvonal
        '<path d="M2 70 H118" stroke="var(--abra-jel)" stroke-width="1.2" stroke-dasharray="3 3"/>'
        # cső és benne a haladó víz
        '<path d="M48 60 H84 Q92 60 92 68 V78" fill="none" stroke="var(--abra-keret)" '
        'stroke-width="7" stroke-linecap="round"/>'
        '<path class="abra-ciklus" d="M48 60 H84 Q92 60 92 68 V78" fill="none" stroke="var(--abra-viz)" '
        'stroke-width="3.4" stroke-linecap="round" stroke-dasharray="7 4"/>'
        # a tartály pereme
        '<path d="M80 80 V76 H104 V80" fill="none" stroke="var(--abra-kiemeles)" stroke-width="2.2"/>',
        'A ház szennyvize a berendezésbe folyik')


def rajz_tisztitas():
    """Levegőztetett tér: a kompresszor levegője buborékokban száll fel,
    közöttük az eleveniszap pelyhei."""
    pelyhek = ''.join(
        f'<circle class="abra-lebeg abra-i{i}" cx="{x}" cy="{y}" r="2.6" fill="var(--abra-iszap)" '
        f'stroke="var(--abra-keret)" stroke-width=".8"/>'
        for i, (x, y) in enumerate([(52, 44), (70, 52), (86, 40), (62, 62), (94, 58)]))
    return _svg(
        # kompresszor
        '<rect x="4" y="8" width="24" height="16" rx="3" fill="var(--abra-badge)" '
        'stroke="var(--abra-kiemeles)" stroke-width="1.8"/>'
        '<path d="M10 16 H22" stroke="var(--abra-kiemeles)" stroke-width="1.6" stroke-linecap="round"/>'
        # légvezeték a tartály aljáig
        '<path d="M16 24 V74 H44" fill="none" stroke="var(--abra-kiemeles)" stroke-width="1.8"/>'
        # tartály víztérrel
        '<rect x="38" y="18" width="72" height="62" rx="6" fill="none" stroke="var(--abra-keret)" stroke-width="2.2"/>'
        '<rect x="40" y="30" width="68" height="48" rx="4" fill="var(--abra-viz)"/>'
        # diffúzor
        '<path d="M46 74 H102" stroke="var(--abra-kiemeles)" stroke-width="2.4" stroke-linecap="round" '
        'stroke-dasharray="2 3"/>'
        + pelyhek + _buborekok(44, 60, 70, 6),
        'Levegőztetett tér buborékokkal és eleveniszap-pelyhekkel')


def rajz_iszap():
    """A fölösiszap az iszapzsákba kerül, és ott víztelenedik."""
    cseppek = ''.join(
        f'<circle class="hub-hullo abra-i{i}" cx="{x}" cy="70" r="1.6" fill="var(--abra-viz)"/>'
        for i, x in enumerate((50, 60, 70)))
    return _svg(
        # kosár
        '<path d="M30 20 H90 L84 66 H36 Z" fill="none" stroke="var(--abra-keret)" stroke-width="2.2" '
        'stroke-linejoin="round"/>'
        + ''.join(f'<circle cx="{x}" cy="{y}" r="1" fill="var(--abra-jel)"/>'
                  for y in (32, 44, 56) for x in range(42, 82, 8)) +
        # zsák benne, az iszappal
        '<path d="M40 14 Q60 8 80 14 L76 58 Q60 64 44 58 Z" fill="var(--surface)" '
        'stroke="var(--abra-kiemeles)" stroke-width="1.8"/>'
        '<path d="M45 34 Q60 30 75 34 L73 56 Q60 61 47 56 Z" fill="var(--abra-iszap)"/>'
        '<path d="M52 12 Q60 18 68 12" fill="none" stroke="var(--abra-kiemeles)" stroke-width="1.6"/>'
        + cseppek,
        'Iszapzsák a kosárban, alóla kicsepegő víz')


def rajz_elvezetes():
    """A tisztított víz a gyökérzónában hasznosul."""
    cseppek = ''.join(
        f'<circle class="hub-hullo abra-i{i}" cx="{x}" cy="{50}" r="1.7" fill="var(--abra-viz)"/>'
        for i, x in enumerate((30, 48, 66, 84, 102)))
    novenyek = ''.join(
        f'<path d="M{x} 24 V12 M{x} 18 Q{x - 7} 12 {x - 9} 6 M{x} 16 Q{x + 7} 10 {x + 9} 5" fill="none" '
        f'stroke="var(--abra-kiemeles)" stroke-width="1.8" stroke-linecap="round"/>'
        f'<path d="M{x} 24 Q{x - 4} 36 {x - 10} 44 M{x} 26 Q{x + 3} 38 {x + 8} 46" fill="none" '
        f'stroke="var(--abra-jel)" stroke-width="1.1" stroke-linecap="round"/>'
        for x in (24, 60, 96))
    return _svg(
        # talajfelszín és talaj
        '<rect x="2" y="24" width="116" height="58" rx="3" fill="var(--abra-iszap)" opacity=".45"/>'
        '<path d="M2 24 H118" stroke="var(--abra-kiemeles)" stroke-width="2.4"/>'
        + novenyek +
        # perforált szivárogtató cső
        '<rect x="14" y="40" width="96" height="8" rx="4" fill="var(--surface)" '
        'stroke="var(--abra-keret)" stroke-width="1.8"/>'
        + ''.join(f'<circle cx="{x}" cy="46" r="1" fill="var(--abra-keret)"/>' for x in range(22, 106, 10))
        + cseppek,
        'Szivárogtató cső a talajban, a növények gyökérzónájában')


LEPESEK = [
    (rajz_beerkezes, 'Beérkezik',
     'A ház teljes szennyvize — a WC-ből érkező feketevíz és a konyha, fürdő, mosás szürkevize — '
     'a berendezésbe folyik.'),
    (rajz_tisztitas, 'Élő baktériumok tisztítják',
     'Az eleveniszap baktériumai bontják le a szennyezőanyagokat. Az oxigént a kompresszor adja; '
     'levegőztetett és ülepítő szakaszok váltakoznak.'),
    (rajz_iszap, 'A fölösiszap zsákba kerül',
     'A keletkező fölösiszap az iszapzsákban víztelenedik és szárad — négy fő mellett nagyjából '
     'évi 0,5 m³. Rendszeres szippantás nincs.'),
    (rajz_elvezetes, 'A tisztított víz a kertben marad',
     'Megfelelő kialakítással a megtisztított víz a telken belül, gyökérzónás elhelyezéssel '
     'hasznosul.'),
]


def folyamat_abra(azon):
    lepesek = []
    for n, (rajz, cim, szoveg) in enumerate(LEPESEK, 1):
        lepesek.append(f'''          <li class="hub-lepes">
            {rajz()}
            <p class="type-data-eyebrow hub-lepes-szam"><span class="visually-hidden">Lépés </span>{n:02d}</p>
            <h3 class="type-ui-card-title hub-lepes-cim">{_html.escape(cim)}</h3>
            <p class="type-ui-body hub-lepes-szoveg">{_html.escape(szoveg)}</p>
          </li>''')
    nl = '\n'
    return f'''      <figure class="hub-folyamat" aria-labelledby="{azon}">
        <figcaption class="hub-folyamat-fej">
          <p class="type-data-eyebrow section-eyebrow">Infografika</p>
          <p class="type-display-highlight-title hub-folyamat-cim" id="{azon}">Így tisztít — négy lépésben</p>
        </figcaption>
        <ol class="hub-lepesek" role="list">
{nl.join(lepesek)}
        </ol>
        <p class="type-ui-caption hub-folyamat-jegyzet">Egyszerűsített ábra. A kamrák száma és elrendezése modellenként eltérhet.</p>
      </figure>'''


# ------------------------------------------------------------ KÖLTSÉG
# Forrás: a megrendelő szövege (2026-09-16), a főoldal üzemeltetési
# kártyájával egyezően: 50 W, 36 Ft/kWh, iszapzsák legfeljebb 4 × 300 Ft,
# membráncsere 3–4 évente, évesítve 10 500 Ft.
TETELEK = [
    # (osztály, felirat)
    ('hub-sav-aram', 'Villamos energia'),
    ('hub-sav-zsak', 'Iszapzsák'),
    ('hub-sav-membran', 'Membráncsere, évesítve'),
]
UZEMMODOK = [
    # (név, részlet, [áram, zsák, membrán])
    ('Folyamatos üzem', '438 kWh/év', [15_800, 1_200, 10_500]),
    ('Szakaszos üzem, 7 perc működés / 3 perc szünet', 'kb. 307 kWh/év', [11_000, 1_200, 10_500]),
]
SKALA = 27_500


def ft(n):
    return f'{n:,}'.replace(',', ' ') + ' Ft'


def koltseg_abra(azon):
    sorok = []
    for nev, reszlet, ertekek in UZEMMODOK:
        x = 0
        teglalapok = []
        for (osztaly, _), ertek in zip(TETELEK, ertekek):
            teglalapok.append(f'<rect class="{osztaly}" x="{x}" y="0" width="{ertek}" height="10"/>')
            x += ertek
        osszeg = sum(ertekek)
        bontas = ' + '.join(f'{felirat.lower()} {ft(e)}' for (_, felirat), e in zip(TETELEK, ertekek))
        sorok.append(f'''          <li class="hub-koltseg-sor">
            <p class="type-ui-body hub-koltseg-nev"><strong>{_html.escape(nev)}</strong> <span class="hub-koltseg-reszlet">{reszlet}</span></p>
            <p class="type-data-value hub-koltseg-osszeg">≈ {ft(osszeg)}<span class="hub-koltseg-egyseg">/év</span></p>
            <svg class="hub-koltseg-sav" viewBox="0 0 {SKALA} 10" preserveAspectRatio="none" aria-hidden="true" focusable="false">{''.join(teglalapok)}</svg>
            <p class="visually-hidden">{bontas}</p>
          </li>''')
    jelek = ''.join(
        f'<li class="type-ui-caption hub-jel"><span class="hub-jel-minta {osztaly}" aria-hidden="true"></span>{felirat}</li>'
        for osztaly, felirat in TETELEK)
    nl = '\n'
    return f'''      <figure class="abra hub-koltseg" aria-labelledby="{azon}">
        <figcaption>
          <p class="type-ui-card-title hub-koltseg-cim" id="{azon}">Éves üzemeltetési költség, két üzemmódban</p>
          <p class="type-ui-caption abra-felirat">Példaszámítás 36&nbsp;Ft/kWh lakossági áramárral. Szippantás nincs benne, mert nincs rá szükség.</p>
        </figcaption>
        <ul class="hub-koltseg-sorok" role="list">
{nl.join(sorok)}
        </ul>
        <ul class="hub-jelek" role="list">{jelek}</ul>
      </figure>'''


def utem_abra(azon):
    """A kompresszor szakaszos ütemezése: tíz percből hét működés."""
    return f'''      <figure class="abra hub-utem" aria-labelledby="{azon}">
        <figcaption>
          <p class="type-ui-card-title hub-koltseg-cim" id="{azon}">A kompresszor szakaszos üzemben</p>
          <p class="type-ui-caption abra-felirat">Egy tízperces ciklus. A folyamatos üzem is teljesen normális — a beállítást a terhelés és az üzemállapot határozza meg.</p>
        </figcaption>
        <div class="hub-utem-sav" aria-hidden="true">
          <span class="hub-utem-be"></span><span class="hub-utem-ki"></span>
        </div>
        <ul class="hub-utem-skala" role="list">
          <li class="type-ui-caption"><strong>7 perc működés</strong> · az idő 70%-a</li>
          <li class="type-ui-caption"><strong>3 perc szünet</strong></li>
        </ul>
        <dl class="hub-utem-adatok">
          <div><dt class="type-ui-caption">Folyamatos üzem</dt><dd class="type-data-value">438&nbsp;kWh/év</dd></div>
          <div><dt class="type-ui-caption">Szakaszos üzem</dt><dd class="type-data-value">kb. 307&nbsp;kWh/év</dd></div>
          <div><dt class="type-ui-caption">Kompresszor</dt><dd class="type-data-value">50&nbsp;W</dd></div>
        </dl>
      </figure>'''
