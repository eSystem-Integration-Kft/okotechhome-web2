#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jelentes.html — az ajánlat-összehasonlítási jelentés önálló oldala.

MIÉRT VAN SZÜKSÉG KÜLÖN OLDALRA. A jelentés nyomtatható és letölthető, a
nyomtatáshoz pedig valódi, azonos eredetű oldal kell: egy `blob:` URL-en
megnyitott dokumentum a létrehozó lap CSP-jét örökli, a webhelyé viszont
`style-src 'self'`, tehát a beágyazott stílusblokkot kiszűrné, és a jelentés
formázás nélkül jelenne meg. Ez az oldal külső stíluslapot hivatkozik, így a
szabály nem sérül.

AZ ADAT NEM AZ OLDALON ÉL. A jelentés tartalmát a 11. szekció adja át
`sessionStorage`-ban. Ez szándékos: az ajánlatok a látogató dokumentumaiból
származnak, tehát semmi nem kerül a szerverre és semmi nem marad a böngészőben
a lap bezárása után. Ha nincs adat (valaki közvetlenül nyitja meg a címet), az
oldal ezt megmondja, és visszairányít az összehasonlítóhoz.

A `?nyomtat=1` paraméterrel érkezve a lap magától megnyitja a nyomtatási
párbeszédet — innen menthető PDF-be.
"""
import pathlib, re

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'
CSS_V = 'v=82'

OLDAL = f'''<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<!-- TESZT ÜZEMMÓD: az oldal fejlesztés alatt áll. ÉLESÍTÉSKOR ezt a sort
     minden oldalról törölni kell (a .htaccess X-Robots-Tag blokkjával együtt). -->
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Ajánlat-összehasonlítási jelentés | ÖkoTech Home</title>
<meta name="description" content="A feltöltött ajánlatokból készült összehasonlítás nyomtatható és letölthető jelentésként.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@400;500;600;700&amp;family=IBM+Plex+Sans:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;display=swap">
<link rel="stylesheet" href="assets/css/app.css?{CSS_V}">
<link rel="stylesheet" href="assets/css/jelentes.css?v=1">
</head>
<body>

<a class="skip-link" href="#fotartalom">Ugrás a tartalomra</a>
<header class="site-header"></header>

<main id="fotartalom">

  <section class="section jelentes-lap" aria-labelledby="jelentes-cim">
    <div class="section-inner">

      <!-- Az eszköztár csak képernyőn látszik: a nyomtatott lapon értelmetlen
           volna, és elvinné a helyet a tartalom elől (jelentes.css @media print). -->
      <div class="jelentes-eszkoztar" data-jelentes-eszkoztar hidden>
        <p class="type-ui-caption jelentes-eszkoztar-cim" id="jelentes-cim">Ajánlat-összehasonlítási jelentés</p>
        <div class="jelentes-gombok">
          <button type="button" class="btn btn-primary" data-jelentes-nyomtat>Nyomtatás / PDF</button>
          <button type="button" class="btn btn-secondary" data-jelentes-letolt>HTML letöltése</button>
          <a class="btn btn-secondary" href="./#ajanlat-osszehasonlito">Vissza az összehasonlítóhoz</a>
        </div>
      </div>

      <article class="jel" data-jelentes-torzs hidden></article>

      <div class="jelentes-ures" data-jelentes-ures hidden>
        <h1 class="type-display-section-title">Ehhez a nézethez még nincs összehasonlítás</h1>
        <p class="type-ui-body jelentes-ures-szoveg">
          A jelentés abból az összehasonlításból készül, amit a főoldali ajánlat-összehasonlítóban
          futtat le. Töltsön fel 2–3 ajánlatot, indítsa el az elemzést, és onnan nyissa meg ezt a
          nézetet — az adatok nem kerülnek a szerverre, ezért egy közvetlenül megnyitott cím
          üresen marad.
        </p>
        <p class="jelentes-ures-gomb">
          <a class="btn btn-primary" href="./#ajanlat-osszehasonlito">Ugrás az összehasonlítóhoz</a>
        </p>
      </div>

    </div>
  </section>

</main>

<script src="assets/js/site.js?v=3" defer></script>
<script src="assets/js/jelentes.js?v=2" defer></script>
<script src="assets/js/jelentes-oldal.js?v=1" defer></script>

</body>
</html>
'''


if __name__ == '__main__':
    p = WEB / 'jelentes.html'
    regi = p.read_text(encoding='utf-8') if p.exists() else ''
    uj = OLDAL
    # A fejlécet és a láblécet a saját generátoraik írják be; ha már megvoltak,
    # átmentjük őket, hogy ez a szkript önmagában is teljes oldalt hagyjon hátra.
    fej = re.search(r'<a class="skip-link".*?</header>', regi, re.S)
    if fej:
        uj = re.sub(r'<a class="skip-link".*?</header>', lambda _: fej.group(), uj, flags=re.S)
    lab = re.search(r'\n<!-- =+\n     LÁBLÉC.*?\n</footer>\n', regi, re.S)
    if lab:
        uj = uj.replace('\n<script src="assets/js/site.js', lab.group() + '\n<script src="assets/js/site.js', 1)
    p.write_text(uj, encoding='utf-8')
    print('jelentes.html kiírva — futtasd utána a fejlec.py és a lablec.py szkriptet')
