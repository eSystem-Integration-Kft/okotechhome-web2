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

FUTTATÁS:  python3 scripts/oldalgyartas/dokumentumtar.py
"""
import html as H
import pathlib
import re
import urllib.parse

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
UPL = 'wp-content/uploads'


def meret(ut):
    b = (WEB / ut).stat().st_size
    return f'{b / 1048576:.1f} MB' if b >= 1048576 else f'{(b + 512) // 1024} KB'


def link(ut, cim, elotag):
    """A fájlnév ékezetes; a cím a miénk, a href a régi, kódolt útvonal."""
    assert (WEB / ut).exists(), ut
    href = elotag + urllib.parse.quote(ut)
    return (f'<a class="text-link" href="{href}"><span class="link-label">{H.escape(cim)}'
            f'<span class="action-arrow-end" aria-hidden="true">&darr;</span></span></a>'
            f' <span class="type-ui-caption">PDF, {meret(ut)}</span>')


def lista(tetelek, elotag):
    return '\n'.join(f'          <li class="type-ui-body">{link(u, c, elotag)}</li>'
                     for u, c in tetelek)


def szakasz(azon, cimke, cim, bevezeto, tetelek, elotag, alt=False):
    return f'''<section class="section{' section-alt' if alt else ''}" aria-labelledby="{azon}-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">{cimke}</p>
        <h2 class="type-display-section-title section-title" id="{azon}-cim">{cim}</h2>
        <p class="type-ui-body section-lead">{bevezeto}</p>
      </header>
      <div class="jogi-szoveg">
        <ul class="jogi-lista">
{lista(tetelek, elotag)}
        </ul>
      </div>
    </div>
  </section>

  '''


UZEMELTETES = [
    (f'{UPL}/2020/05/2.1.1_A.B.Clear_használati-és-karbantartási-utasítás.pdf',
     'A.B. Clear használati és karbantartási utasítás'),
    (f'{UPL}/2020/05/2.1.0_A-B-Clear-berendezések-működése.pdf',
     'Az A.B. Clear berendezések működése'),
    (f'{UPL}/2020/05/2.1.2_A.B.Clear_kamrák-elnevezése.pdf',
     'A kamrák elnevezése'),
    (f'{UPL}/2020/05/4_2_1_Telepítés-lépésről-lépésre.pdf',
     'Telepítés lépésről lépésre'),
    (f'{UPL}/2020/05/4.2.2_Szikkasztóalagutakból-álló-szikkasztórendszer-telepítése.pdf',
     'Szikkasztóalagutakból álló szikkasztórendszer telepítése'),
    (f'{UPL}/2020/05/5.2.1_Levegőelosztó-csapsor-beállítása.pdf',
     'A levegőelosztó csapsor beállítása'),
    (f'{UPL}/2020/05/5.2.2_Levegőztetés-átállítása-szaghatás-esetén.pdf',
     'A levegőztetés átállítása szaghatás esetén'),
    (f'{UPL}/2020/05/5.3.1_Fölösiszap-kipumpálása-az-Iszapsűrítő-kamrából.pdf',
     'Fölösiszap kipumpálása az iszapsűrítő kamrából'),
    (f'{UPL}/2020/05/5.3.1_Iszapkipumpálás-vezérlés-nélküli-berendezésen.pdf',
     'Iszapkipumpálás vezérlés nélküli berendezésen'),
    (f'{UPL}/2020/05/5.3.2_Iszapelvételi-könyök-beállítása-az-iszapszinthez-igazodva.pdf',
     'Az iszapelvételi könyök beállítása'),
    (f'{UPL}/2020/05/5.3.3_Iszapkipumpálás-beállítása-digitális-vezérlésen.pdf',
     'Iszapkipumpálás beállítása digitális vezérlésen'),
    (f'{UPL}/2020/05/6.1.2._Dugult-iszapelvételi-könyök-kitisztítása-dugulásának-elhárítása.pdf',
     'Dugult iszapelvételi könyök kitisztítása'),
]

# A határozatok KITAKARVA kerültek ki annak idején: sem név, sem cím, sem
# helyrajzi szám nem olvasható bennük. Ezért közölhetők tovább.
ENGEDELYEK_REGI = [
    ('01', 'alsoors_2013_05_31', 'Alsóörs, 2013'),
    ('02', 'balatonfured_2015_04_30', 'Balatonfüred, 2015'),
    ('03', 'belapatfalva_2014_08_04', 'Bélapátfalva, 2014'),
    ('04', 'budakeszi_2015_10_15', 'Budakeszi, 2015'),
    ('05', 'dombovar_nodate_noname', 'Dombóvár'),
    ('06', 'dunabogdany_2016_09_08', 'Dunabogdány, 2016'),
    ('07', 'kerta_2015_05_13', 'Kerta, 2015'),
    ('08', 'koszeg_2016_03_10', 'Kőszeg, 2016'),
    ('09', 'nogradsap_2013_05_02', 'Nógrádsáp, 2013'),
    ('10', 'nyirgyulaj_2013_06_13', 'Nyírgyulaj, 2013'),
    ('11', 'penzesgyor_2014_08_15', 'Pénzesgyőr, 2014'),
    ('12', 'piliscsev_2013_11_04', 'Piliscsév, 2013'),
    ('13', 'szolad_2014_08_19', 'Szólád, 2014'),
    ('14', 'telki_2014_06_26', 'Telki, 2014'),
    ('15', 'ujlengyel_2016_12_07', 'Újlengyel, 2016'),
]

ENGEDELYEK_UJ = [
    ('Biatorbágy_2020_08_24_', 'Biatorbágy, 2020'),
    ('Buj_2020_02_03', 'Buj, 2020'),
    ('Csapod_2020_05_13', 'Csapod, 2020'),
    ('Kiskunfélegyháza_2020_02_17', 'Kiskunfélegyháza, 2020'),
    ('Nyúl_2020_10_16', 'Nyúl, 2020'),
    ('Sopron_2020_09_10', 'Sopron, 2020'),
    ('Verőce_2020_12_11', 'Verőce, 2020'),
    ('Zalakomár_2020_10_15', 'Zalakomár, 2020'),
    ('Zebegény_2020_05_29', 'Zebegény, 2020'),
]


def beszur(lap, horgony, blokk):
    p = WEB / lap
    t = p.read_text(encoding='utf-8')
    if 'wp-content/uploads' in t:
        print(f'  – már bekötve: {lap}')
        return
    i = t.index(horgony)
    p.write_text(t[:i] + blokk + t[i:], encoding='utf-8')
    print(f'  ✓ {lap}')


def main():
    gyik = '<section class="section" aria-labelledby="gyik-cim">'

    beszur('megoldasok/ab-clear-dokumentumok.html', gyik, szakasz(
        'letoltheto', 'Dokumentumtár', 'Letölthető üzemeltetési dokumentumok',
        'A berendezés használati és karbantartási utasítása, a telepítés leírása és a '
        'leggyakoribb beállítások lépésről lépésre.',
        UZEMELTETES, '../', alt=True))

    engedelyek = ([(f'{UPL}/2017/04/{n}-mintaengedely-szennyviztisztito-telepitesre-{f}.pdf',
                    f'Mintaengedély — {c}') for n, f, c in ENGEDELYEK_REGI]
                  + [(f'{UPL}/2021/03/{f}.pdf', f'Mintaengedély — {c}')
                     for f, c in ENGEDELYEK_UJ]
                  + [(f'{UPL}/2017/04/5-telepulesszintu-engedely-obudavar.pdf',
                      'Településszintű engedély — Óbudavár')])
    beszur('eredmenyek/tanusitvanyok-es-dokumentumok.html',
           '<section class="section" aria-labelledby="tovabb-cim"', szakasz(
        'mintaengedelyek', 'Mintaengedélyek', 'Kiadott engedélyek — huszonöt példa',
        'Jegyzői és vízügyi határozatok az ország különböző pontjairól, 2013 és 2020 '
        'között. A dokumentumokban a név, a cím és a helyrajzi szám kitakarva szerepel. '
        'Nem jogi minta, hanem annak bizonyítéka, hogy az eljárás lefolytatható.',
        engedelyek, '../', alt=True))

    beszur('tudastar/elszivarogtatas.html', gyik, szakasz(
        'telepitesi-utmutato', 'Kivitelezés', 'A szikkasztórendszer telepítési útmutatója',
        'A saját kivitelezési útmutatónk: árokméret alagútszámonként, kavicsmennyiség, '
        'lejtés, geotextília és földtakarás — táblázatokkal.',
        [(f'{UPL}/2020/05/4.2.2_Szikkasztóalagutakból-álló-szikkasztórendszer-telepítése.pdf',
          'Szikkasztóalagutakból álló szikkasztórendszer telepítése')], '../', alt=True))

    beszur('tudastar/telepites-lepesrol-lepesre.html',
           '<section class="section" aria-labelledby="kapcsolodo-cim"', szakasz(
        'telepitesi-dok', 'Dokumentum', 'A telepítés saját leírása',
        'Ugyanez a folyamat dokumentumban, a helyszínen is használható formában.',
        [(f'{UPL}/2020/05/4_2_1_Telepítés-lépésről-lépésre.pdf',
          'Telepítés lépésről lépésre'),
         (f'{UPL}/2020/05/2.1.2_A.B.Clear_kamrák-elnevezése.pdf',
          'A kamrák elnevezése')], '../', alt=True))

    beszur('megoldasok/biologiai-uzemeltetes-es-karbantartas.html', gyik, szakasz(
        'uzemeltetesi-dok', 'Dokumentum', 'Üzemeltetési útmutatók',
        'A használati és karbantartási utasítás, és a leggyakoribb beavatkozások '
        'lépésről lépésre.',
        UZEMELTETES[:1] + UZEMELTETES[5:], '../', alt=True))


if __name__ == '__main__':
    main()
