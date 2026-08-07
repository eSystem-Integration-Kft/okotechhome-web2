#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Előkészítés — a szakasz áttekintő oldala (`projekt-elokeszites/index.html`).

A fejléc megamenüje tíz belépési pontot sorol fel ebben a kategóriában, de a
tartalom hubonként készül el. Ez az oldal ezért KÉT listát vezet: a `KESZ`
elemek hivatkozásként jelennek meg, a `TERVEZETT` elemek csak felsorolásként.

Miért nem linkeljük mindet: a nem létező oldalra mutató hivatkozás a
látogatónak 404, a keresőnek pedig hibás jelzés. Amint egy hub elkészül, itt
kell átemelni a `KESZ` listába — ez az egyetlen hely, ahol nyilván van tartva.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import sec_prose, sec_situations, sec_numbered, sec_cta, sec_faq

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

# ikon, cím, leírás, útvonal, gomb felirata
KESZ = [
    ('nav-talaj', 'Telekalkalmasság',
     'Talaj, talajvíz, szabad terület, csőszint, kút és hozzáférés — mi dönti el, hogy '
     'megvalósítható-e a rendszer, és milyen kialakítással.',
     'telekalkalmassag', 'Telekalkalmasság'),
    ('nav-vizelvezetes', 'Tisztított víz elhelyezése',
     'Elszivárogtatás, tisztítómező, gyökérzónás elhelyezés — hová kerül a naponta kilépő '
     'vízmennyiség, és mitől függ, melyik irány jöhet szóba.',
     'tisztitott-viz-elhelyezese', 'Vízelhelyezés'),
    ('nav-terheles', 'Terhelés és kapacitás',
     'A „hány fő?” csak az első kérdés. Vízmennyiség, szerves terhelés, csúcsok és '
     'időbeli eloszlás — ebből áll össze a terhelési profil.',
     'terheles-es-kapacitas', 'Terhelés és kapacitás'),
]

TERVEZETT = [
    'Engedélyezés és dokumentumok — mit kell bejelenteni, és mikor',
    'Helyszíni felmérés — mikor indokolt, és mit ad',
    'Költségek és ajánlatok — mi befolyásolja az árat',
    'Telepítés és beüzemelés — mi történik a helyszínen',
    'Projektkészültségi ellenőrzés — készen áll-e a projekt',
]


def epit():
    tervezett = '\n'.join(
        f'        <li class="card">\n'
        f'          <span class="card-badge type-data-value" aria-hidden="true">{i:02d}</span>\n'
        f'          <p class="type-ui-body card-text">{t}</p>\n'
        f'        </li>' for i, t in enumerate(TERVEZETT, len(KESZ) + 1))

    return [
        sec_prose('Miről szól ez a szakasz', 'A döntés előtti munka', [
            'A szennyvízrendszer kiválasztása nem a berendezésnél kezdődik. Előbb ki kell '
            'derülnie, hogy mi valósítható meg a telken, hová kerül a tisztított víz, '
            'mekkora terhelésre kell méretezni, és milyen dokumentumok szükségesek.',
            'Ez a szakasz ezt a munkát bontja lépésekre. Nem terméket ajánl: azt mutatja meg, '
            'milyen kérdésekre kell választ találni, honnan szerezhetők meg az adatok, és '
            'mikor elég a saját tájékozódás — illetve mikor kell mérés vagy szakértő.',
            'A sorrend nem kötelező, de van logikája. A telek adottságai a legtöbb továbbit '
            'meghatározzák, ezért érdemes ott kezdeni.',
        ]),

        sec_situations('Elérhető szakaszok', 'Hol tart most?',
                       'Ami már elkészült. A többi hamarosan követi — alább felsorolva.',
                       KESZ),

        sec_numbered('Ami készül', 'A szakasz további részei',
                     'Ezek a témák a fejléc menüjében már szerepelnek, de a tartalmuk még '
                     'készül. Amíg nem érhetők el, a kérdéseivel közvetlenül is fordulhat '
                     'hozzánk.',
                     TERVEZETT) if TERVEZETT else '',

        sec_cta('Ha most kell válasz', 'Beszéljünk a konkrét projektről',
                ['Ha a szakasz még nem tartalmazza, amit keres, írja meg a település nevét, '
                 'a háztartás létszámát és amit a telekről tud — a többit megkérdezzük.'],
                'Kapcsolatfelvétel', '../kapcsolat'),

        sec_faq([
            ('Hol kezdjem, ha még semmit nem tudok?',
             'A telekalkalmasságnál. Az ott vizsgált adatok — talaj, talajvíz, szabad terület, '
             'csőszint — a későbbi döntések nagy részét meghatározzák, és többségük '
             'megszerezhető anélkül, hogy bárkit ki kellene hívni.'),
            ('Kell ehhez ajánlatot kérnem?',
             'Nem. A szakasz oldalai tájékozódásra készültek, és az előszűrők sem kérnek '
             'kapcsolati adatot a használatukhoz. Ajánlatkérésnek akkor van értelme, ha a '
             'telek és a terhelés kérdései már tisztázottak.'),
        ]),
    ]


OLDAL = dict(
    file='projekt-elokeszites/index.html', url='projekt-elokeszites/', img='attekintes',
    title='Projekt-előkészítés — mit kell tisztázni a döntés előtt | ÖkoTech Home',
    desc='Telekalkalmasság, vízelhelyezés, terhelés, engedélyezés és felmérés — a '
         'szennyvízrendszer kiválasztása előtti munka lépésekre bontva.',
    h1='Projekt-előkészítés',
    alt='Kiterített műszaki rajzok és jegyzetfüzet egy asztalon, mellette mérőszalag és '
        'ceruza',
    lead='A rendszer kiválasztása nem a berendezésnél kezdődik. Előbb az derül ki, mi '
         'valósítható meg a telken, hová kerül a tisztított víz, és mekkora terhelésre kell '
         'méretezni. Ez a szakasz ebben vezet végig.',
    crumbs=[('Főoldal', '../')],
    sections=[s for s in epit() if s],
)

if __name__ == '__main__':
    (WEB / 'projekt-elokeszites').mkdir(exist_ok=True)
    out = WEB / OLDAL['file']
    out.write_text(G.build(OLDAL), encoding='utf-8')
    print(f"  {OLDAL['file']:60s} {len(out.read_text(encoding='utf-8'))//1024} KB")
