#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dokumentumtar.py — a visszaállított régi dokumentumok bekötése a lapokba.

MIÉRT. A régi webhely `/wp-content/uploads/` mappájának fájljai évi 600-nál több
organikus kattintást hoztak, és az átállás után mind 404 lett. A fájlok a
`/_Backup/20260903/oko-wp-mentes.zip` mentésből visszakerültek az EREDETI
címükre — átirányítás nélkül, mert egy PDF-et lapra irányítani „soft 404".

Ez a szkript a MÁSIK felét végzi el: hivatkozást ad rájuk a témába vágó lapról,
hogy ne csak a régi találatokból legyenek elérhetők. A fájlnevek ékezetesek; a
`href`-ben százalékjeles kódolással állnak, mert a régi cím ilyen volt, és az
marad az indexben.

MEGJELENÍTÉS — KÁRTYA, NEM FELSOROLÁS. Huszonöt engedélyminta listaként azt
ismételte huszonötször, ami mindegyikben közös („Mintaengedély —"), és azt
mondta egyszer, kicsiben, ami megkülönbözteti őket. A kártyán a TELEPÜLÉS a
címsor, az év és a fájlméret a metasor, a közös rész pedig a szakasz címében
áll egyszer.

FUTTATÁS:  python3 scripts/oldalgyartas/dokumentumtar.py
"""
import html as H
import pathlib
import urllib.parse

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
UPL = 'wp-content/uploads'

# Behajtott sarkú lap. Dekoráció: a jelentést a „PDF" felirat hordozza.
LAPJEL = ('<svg class="dok-jel" viewBox="0 0 24 32" aria-hidden="true" focusable="false">'
          '<path d="M3 1h12l6 6v24H3z" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linejoin="round"/>'
          '<path d="M15 1v6h6" fill="none" stroke="currentColor" stroke-width="2" '
          'stroke-linejoin="round"/></svg>')


def meret(ut):
    b = (WEB / ut).stat().st_size
    return f'{b / 1048576:.1f} MB' if b >= 1048576 else f'{(b + 512) // 1024} KB'


def kartya(ut, cim, meta, elotag):
    """A fájlnév ékezetes; a cím a miénk, a href a régi, kódolt útvonal."""
    assert (WEB / ut).exists(), ut
    href = elotag + urllib.parse.quote(ut)
    sorok = [
        '          <li>',
        f'            <a class="dok" href="{href}" download>',
        f'              {LAPJEL}',
        '              <span class="dok-szoveg">',
        f'                <span class="type-ui-card-title dok-cim">{H.escape(cim)}</span>',
        f'                <span class="type-ui-caption dok-meta">{H.escape(meta)} · PDF, {meret(ut)}</span>',
        '              </span>',
        '            </a>',
        '          </li>',
    ]
    return '\n'.join(sorok)


def lista(tetelek, elotag):
    """A tétel (útvonal, cím) vagy (útvonal, cím, meta) alakú."""
    return '\n'.join(kartya(x[0], x[1], x[2] if len(x) > 2 else 'Letöltés', elotag)
                     for x in tetelek)


def szakasz(azon, cimke, cim, bevezeto, tetelek, elotag, alt=False):
    return f'''<section class="section{' section-alt' if alt else ''}" aria-labelledby="{azon}-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">{cimke}</p>
        <h2 class="type-display-section-title section-title" id="{azon}-cim">{cim}</h2>
        <p class="type-ui-body section-lead">{bevezeto}</p>
      </header>
      <ul class="dok-racs" role="list">
{lista(tetelek, elotag)}
      </ul>
    </div>
  </section>

  '''


# (útvonal, a kártya címe, a metasor)
UZEMELTETES = [
    (f'{UPL}/2020/05/2.1.1_A.B.Clear_használati-és-karbantartási-utasítás.pdf',
     'Használati és karbantartási utasítás', 'A.B. Clear'),
    (f'{UPL}/2020/05/2.1.0_A-B-Clear-berendezések-működése.pdf',
     'A berendezések működése', 'A.B. Clear'),
    (f'{UPL}/2020/05/2.1.2_A.B.Clear_kamrák-elnevezése.pdf',
     'A kamrák elnevezése', 'A.B. Clear'),
    (f'{UPL}/2020/05/4_2_1_Telepítés-lépésről-lépésre.pdf',
     'Telepítés lépésről lépésre', 'Kivitelezés'),
    (f'{UPL}/2020/05/4.2.2_Szikkasztóalagutakból-álló-szikkasztórendszer-telepítése.pdf',
     'Szikkasztórendszer telepítése', 'Kivitelezés'),
    (f'{UPL}/2020/05/5.2.1_Levegőelosztó-csapsor-beállítása.pdf',
     'A levegőelosztó csapsor beállítása', 'Beállítás'),
    (f'{UPL}/2020/05/5.2.2_Levegőztetés-átállítása-szaghatás-esetén.pdf',
     'Levegőztetés átállítása szaghatásnál', 'Beállítás'),
    (f'{UPL}/2020/05/5.3.1_Fölösiszap-kipumpálása-az-Iszapsűrítő-kamrából.pdf',
     'Fölösiszap kipumpálása', 'Iszapkezelés'),
    (f'{UPL}/2020/05/5.3.1_Iszapkipumpálás-vezérlés-nélküli-berendezésen.pdf',
     'Iszapkipumpálás vezérlés nélkül', 'Iszapkezelés'),
    (f'{UPL}/2020/05/5.3.2_Iszapelvételi-könyök-beállítása-az-iszapszinthez-igazodva.pdf',
     'Az iszapelvételi könyök beállítása', 'Iszapkezelés'),
    (f'{UPL}/2020/05/5.3.3_Iszapkipumpálás-beállítása-digitális-vezérlésen.pdf',
     'Iszapkipumpálás digitális vezérlésen', 'Iszapkezelés'),
    (f'{UPL}/2020/05/6.1.2._Dugult-iszapelvételi-könyök-kitisztítása-dugulásának-elhárítása.pdf',
     'Dugult iszapelvételi könyök', 'Hibaelhárítás'),
]

# A határozatok KITAKARVA kerültek ki annak idején: sem név, sem cím, sem
# helyrajzi szám nem olvasható bennük. Ezért közölhetők tovább.
ENGEDELYEK_REGI = [
    ('01', 'alsoors_2013_05_31', 'Alsóörs', '2013'),
    ('02', 'balatonfured_2015_04_30', 'Balatonfüred', '2015'),
    ('03', 'belapatfalva_2014_08_04', 'Bélapátfalva', '2014'),
    ('04', 'budakeszi_2015_10_15', 'Budakeszi', '2015'),
    ('05', 'dombovar_nodate_noname', 'Dombóvár', 'Dátum nélkül'),
    ('06', 'dunabogdany_2016_09_08', 'Dunabogdány', '2016'),
    ('07', 'kerta_2015_05_13', 'Kerta', '2015'),
    ('08', 'koszeg_2016_03_10', 'Kőszeg', '2016'),
    ('09', 'nogradsap_2013_05_02', 'Nógrádsáp', '2013'),
    ('10', 'nyirgyulaj_2013_06_13', 'Nyírgyulaj', '2013'),
    ('11', 'penzesgyor_2014_08_15', 'Pénzesgyőr', '2014'),
    ('12', 'piliscsev_2013_11_04', 'Piliscsév', '2013'),
    ('13', 'szolad_2014_08_19', 'Szólád', '2014'),
    ('14', 'telki_2014_06_26', 'Telki', '2014'),
    ('15', 'ujlengyel_2016_12_07', 'Újlengyel', '2016'),
]

ENGEDELYEK_UJ = [
    ('Biatorbágy_2020_08_24_', 'Biatorbágy', '2020'),
    ('Buj_2020_02_03', 'Buj', '2020'),
    ('Csapod_2020_05_13', 'Csapod', '2020'),
    ('Kiskunfélegyháza_2020_02_17', 'Kiskunfélegyháza', '2020'),
    ('Nyúl_2020_10_16', 'Nyúl', '2020'),
    ('Sopron_2020_09_10', 'Sopron', '2020'),
    ('Verőce_2020_12_11', 'Verőce', '2020'),
    ('Zalakomár_2020_10_15', 'Zalakomár', '2020'),
    ('Zebegény_2020_05_29', 'Zebegény', '2020'),
]

# A lap → (horgony, blokk) — a beszúrás helye a lapon.
GYIK_HORGONY = '<section class="section" aria-labelledby="gyik-cim">'


def beszur(lap, horgony, blokk):
    p = WEB / lap
    t = p.read_text(encoding='utf-8')
    if 'class="dok-racs"' in t:
        print(f'  – már bekötve: {lap}')
        return
    i = t.index(horgony)
    p.write_text(t[:i] + blokk + t[i:], encoding='utf-8')
    print(f'  ✓ {lap}')


def main():
    beszur('megoldasok/ab-clear-dokumentumok.html', GYIK_HORGONY, szakasz(
        'letoltheto', 'Dokumentumtár', 'Letölthető üzemeltetési dokumentumok',
        'A berendezés használati és karbantartási utasítása, a telepítés leírása és a '
        'leggyakoribb beállítások lépésről lépésre.',
        UZEMELTETES, '../', alt=True))

    engedelyek = (
        [(f'{UPL}/2017/04/{n}-mintaengedely-szennyviztisztito-telepitesre-{f}.pdf', c, ev)
         for n, f, c, ev in ENGEDELYEK_REGI]
        + [(f'{UPL}/2021/03/{f}.pdf', c, ev) for f, c, ev in ENGEDELYEK_UJ]
        + [(f'{UPL}/2017/04/5-telepulesszintu-engedely-obudavar.pdf',
            'Óbudavár', 'Településszintű')])
    beszur('eredmenyek/tanusitvanyok-es-dokumentumok.html',
           '<section class="section" aria-labelledby="tovabb-cim"', szakasz(
               'mintaengedelyek', 'Mintaengedélyek', 'Huszonöt kiadott engedély',
               'Jegyzői és vízügyi határozatok az ország különböző pontjairól, 2013 és 2020 '
               'között. A dokumentumokban a név, a cím és a helyrajzi szám kitakarva '
               'szerepel. Nem jogi minta, hanem annak bizonyítéka, hogy az eljárás '
               'lefolytatható.',
               engedelyek, '../', alt=True))

    beszur('tudastar/elszivarogtatas.html', GYIK_HORGONY, szakasz(
        'telepitesi-utmutato', 'Kivitelezés', 'A szikkasztórendszer telepítési útmutatója',
        'A saját kivitelezési útmutatónk: árokméret alagútszámonként, kavicsmennyiség, '
        'lejtés, geotextília és földtakarás — táblázatokkal.',
        [(f'{UPL}/2020/05/4.2.2_Szikkasztóalagutakból-álló-szikkasztórendszer-telepítése.pdf',
          'Szikkasztórendszer telepítése', 'Kivitelezés')], '../', alt=True))

    beszur('tudastar/telepites-lepesrol-lepesre.html',
           '<section class="section" aria-labelledby="kapcsolodo-cim"', szakasz(
               'telepitesi-dok', 'Dokumentum', 'A telepítés saját leírása',
               'Ugyanez a folyamat dokumentumban, a helyszínen is használható formában.',
               [(f'{UPL}/2020/05/4_2_1_Telepítés-lépésről-lépésre.pdf',
                 'Telepítés lépésről lépésre', 'Kivitelezés'),
                (f'{UPL}/2020/05/2.1.2_A.B.Clear_kamrák-elnevezése.pdf',
                 'A kamrák elnevezése', 'A.B. Clear')], '../', alt=True))

    beszur('megoldasok/biologiai-uzemeltetes-es-karbantartas.html', GYIK_HORGONY, szakasz(
        'uzemeltetesi-dok', 'Dokumentum', 'Üzemeltetési útmutatók',
        'A használati és karbantartási utasítás, és a leggyakoribb beavatkozások '
        'lépésről lépésre.',
        UZEMELTETES[:1] + UZEMELTETES[5:], '../', alt=True))


if __name__ == '__main__':
    main()
