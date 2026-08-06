#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lábléc — egy sorban, minden oldalra.

A minta kétsoros volt (a hasábok két sávban álltak); itt EGY sor: a márkablokk
és öt hasáb egymás mellett. Nyolc főkategória van, de nyolc hasáb egy sorban
olvashatatlanul keskeny lenne, ezért a három másodlagos kategória a márkablokk
alá, illetve a záró sávba került — ugyanoda, ahová a fejlécben is.

HELYŐRZŐK: a cégadatok (cégjegyzékszám, adószám, székhely) nincsenek meg a
repóban. Kitalálni nem lehet őket — cégadat, amit tévesen közölni jogi kockázat.
Ezért `data-helyorzo` attribútummal jelölt, láthatóan ideiglenes mezőként
szerepelnek, és a CSS is megjelöli őket. Egyetlen kereséssel megtalálhatók.
"""
import pathlib, re

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

HASABOK = [
    ('Helyzetem', 'helyzetem/', [
        ('Nincs elérhető közcsatorna', 'helyzetem/nincs-elerheto-kozcsatorna'),
        ('Telekvásárlás, új építés', 'helyzetem/telekvasarlas-vagy-uj-epites-elott-allok'),
        ('Emésztő kiváltása', 'helyzetem/meglevo-emesztot-szeretnek-kivaltani'),
        ('Nyaraló, szezonális', 'helyzetem/nyaralo-vagy-szezonalisan-hasznalt-ingatlan'),
        ('Családi ház', 'helyzetem/csaladi-hazhoz-keresek-rendszert'),
        ('Vállalkozás, intézmény', 'helyzetem/vallalkozas-vagy-intezmeny-szamara-keresek-megoldast'),
    ]),
    ('Megoldások', 'megoldasok/', [
        ('Biológiai szennyvíztisztítás', 'megoldasok/biologiai-szennyviztisztitas'),
        ('Oldómedencés rendszer', 'megoldasok/oldomedences-rendszer'),
        ('Nagyobb és közösségi', 'megoldasok/nagyobb-es-kozossegi-rendszerek'),
        ('Alternatívák', 'megoldasok/alternativak'),
        ('Megoldástípusok összevetése', 'megoldasok/megoldastipusok-osszehasonlitasa'),
        ('Kizáró feltételek', 'megoldasok/kizaro-es-korlatozo-feltetelek'),
    ]),
    ('Előkészítés', 'projekt-elokeszites/', [
        ('Telekalkalmasság', 'projekt-elokeszites/telekalkalmassag'),
        ('Terhelés és kapacitás', 'projekt-elokeszites/terheles-es-kapacitas'),
        ('Tisztított víz elhelyezése', 'projekt-elokeszites/tisztitott-viz-elhelyezese'),
        ('Engedélyezés', 'projekt-elokeszites/engedelyezes-es-dokumentumok'),
        ('Helyszíni felmérés', 'projekt-elokeszites/helyszini-felmeres'),
        ('Költségek és ajánlatok', 'projekt-elokeszites/koltsegek-es-ajanlatok'),
    ]),
    ('Tudástár', 'tudastar/', [
        ('Telek, talaj és víz', 'tudastar/telek-talaj-es-viz'),
        ('Terhelés és méretezés', 'tudastar/terheles-es-meretezes'),
        ('Engedélyezés', 'tudastar/engedelyezes-es-megfeleloseg'),
        ('Üzemeltetés', 'tudastar/uzemeltetes-es-hibamegelozes'),
        ('Költség és megvalósítás', 'tudastar/koltseg-es-megvalositas'),
        ('Fogalomtár', 'tudastar/fogalomtar'),
    ]),
    ('Eredmények', 'eredmenyek/', [
        ('Csikvánd — 128 berendezés', 'eredmenyek/csikvand'),
        ('Bakonypéterd — központi telep', 'eredmenyek/bakonypeterd'),
        ('Diósberény — 90 berendezés', 'eredmenyek/diosbereny'),
        ('Óbudavár — a kezdet', 'eredmenyek/obudavar'),
        ('Esettanulmányok', 'eredmenyek/esettanulmanyok'),
        ('Tanúsítványok', 'eredmenyek/tanusitvanyok-es-dokumentumok'),
    ]),
]

MASODLAGOS = [
    ('Ügyféltámogatás', 'ugyfeltamogatas/'),
    ('Partnereknek', 'partnereknek/'),
    ('ÖkoTech-Home', 'okotech-home/'),
    ('Kapcsolat', 'kapcsolat'),
]

JOGI = [
    ('Adatkezelési tájékoztató', 'adatkezelesi-tajekoztato'),
    ('Cookie-tájékoztató', 'cookie-tajekoztato'),
    ('Jogi nyilatkozat', 'jogi-nyilatkozat'),
    ('ÁSZF', 'aszf'),
    ('Akadálymentesség', 'akadalymentessegi-nyilatkozat'),
]


def epit(elo=''):
    """`elo` az útvonal-előtag: '' a gyökérben, '../' az aloldalakon."""

    hasabok = ''
    for cim, cel, tetelek in HASABOK:
        li = '\n'.join(
            f'          <li><a class="lablec-link" href="{elo}{h}">{t}</a></li>'
            for t, h in tetelek)
        hasabok += f'''
      <nav class="lablec-hasab" aria-labelledby="lf-{cel.strip('/').replace('/', '-')}">
        <h2 class="type-data-eyebrow lablec-cim" id="lf-{cel.strip('/').replace('/', '-')}">
          <a class="lablec-cim-link" href="{elo}{cel}">{cim}</a>
        </h2>
        <ul class="lablec-lista" role="list">
{li}
        </ul>
      </nav>'''

    masodlagos = ' '.join(
        f'<a class="lablec-link" href="{elo}{h}">{t}</a>' for t, h in MASODLAGOS)
    jogi = '\n'.join(
        f'        <li><a class="lablec-jogi-link" href="{elo}{h}">{t}</a></li>'
        for t, h in JOGI)

    return f'''
<!-- ==========================================================================
     LÁBLÉC — egy sorban: márkablokk + öt hasáb.
     A `data-helyorzo` mezők cégadatot várnak (cégjegyzékszám, adószám,
     székhely). Ezeket nem lehet kitalálni: tévesen közölt cégadat jogi
     kockázat. Élesítés előtt kereséssel mind megtalálható.
=========================================================================== -->
<footer class="lablec">
  <div class="lablec-inner">

    <div class="lablec-marka">
      <a class="lablec-logo" href="{elo or './'}" aria-label="ÖkoTech Home — főoldal">
        <img src="{elo}assets/img/logo-email.png" width="220" height="69"
             alt="ÖkoTech Home" loading="lazy" decoding="async">
      </a>
      <p class="type-ui-body lablec-lead">
        Biológiai szennyvíztisztítás közcsatorna nélküli ingatlanokhoz — a telek
        felmérésétől az üzemeltetésig, egy kézben.
      </p>
      <ul class="lablec-kapcsolat" role="list">
        <li><a class="lablec-link" href="mailto:kapcsolat@okotechhome.hu">kapcsolat@okotechhome.hu</a></li>
        <li><a class="lablec-link" href="tel:+3633200211">+36 33 200 211</a></li>
        <li class="lablec-halvany">2509 Esztergom, Strázsa u. 12.</li>
      </ul>
      <p class="lablec-masodlagos">{masodlagos}</p>
    </div>
{hasabok}

  </div>

  <div class="lablec-zaro">
    <div class="lablec-inner lablec-zaro-inner">
      <p class="type-ui-caption lablec-ceg">
        © 2026 ÖkoTech-Home Kft. Minden jog fenntartva.
        <span class="lablec-helyorzo" data-helyorzo="cegjegyzekszam">Cégjegyzékszám: #####</span>
        <span class="lablec-helyorzo" data-helyorzo="adoszam">Adószám: #####</span>
      </p>
      <ul class="lablec-jogi" role="list">
{jogi}
      </ul>
    </div>
  </div>
</footer>
'''


if __name__ == '__main__':
    n = 0
    for p in sorted(WEB.rglob('*.html')):
        if p.name in ('401.html', '403.html', '404.html', '500.html'):
            continue                      # a hibaoldalak önhordók, saját láblécük van
        s = p.read_text(encoding='utf-8')
        elo = '' if p.parent == WEB else '../'
        uj = epit(elo)
        if '<footer class="lablec">' in s:
            s = re.sub(r'\n<!-- =+\n     LÁBLÉC.*?\n</footer>\n', uj, s, flags=re.S)
        elif '\n<script src=' in s:
            # A lábléc a betöltött szkriptek ELÉ kerül — a szkriptek maradjanak
            # a törzs végén, hogy ne blokkolják a megjelenítést.
            s = s.replace('\n<script src=', uj + '\n<script src=', 1)
        elif '</body>' in s:
            # Ha az oldal nem tölt be külső szkriptet (a kapcsolat oldal utolsó
            # eleme például egy beágyazott JSON-LD blokk), a fenti minta nem
            # illeszkedik. Enélkül az oldal NÉMÁN lábléc nélkül maradt.
            s = s.replace('\n</body>', uj + '\n</body>', 1)
        else:
            print(f'  ! nem találtam beszúrási pontot: {p.relative_to(WEB)}')
            continue
        p.write_text(s, encoding='utf-8')
        n += 1
    print(f'lábléc beírva: {n} oldal')
