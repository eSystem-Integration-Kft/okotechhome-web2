#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Jogi oldalak — a lábléc öt hivatkozása, a webgyökérben.

FORRÁSOK. Az adatkezelési tájékoztató, az ÁSZF és a cégadatok az ÖkoTech-Home
jelenlegi, élő webhelyéről (okotechhome.hu) származnak: a cég saját, meglévő
dokumentumai. A cookie-tájékoztató és az akadálymentességi nyilatkozat ÚJ —
ezek a régi webhelyen nem szerepeltek önálló oldalként.

KÉT ELLENTMONDÁS, AMIT NEM LEHET ELDÖNTENI KÍVÜLRŐL:

1. CÍM. A cégadatok szerint a SZÉKHELY 2500 Esztergom, Csendesvölgy utca 27.
   Az új webhely mindenhol 2509 Esztergom, Strázsa u. 12. címet közöl. A kettő
   más — jellemzően székhely kontra telephely/ügyfélszolgálat. Itt MINDKETTŐ
   szerepel, külön megnevezve, mert a jogi oldalakon a székhely a kötelező adat,
   a kapcsolattartási cím pedig a használható. Ha a székhely azóta megváltozott,
   EZT KELL ELŐSZÖR JAVÍTANI.

2. HATÁLY. A régi ÁSZF webshopos szerkezetű: futárszolgálat, csomagátvétel,
   14 napos elállás távollévők közötti szerződésre. Az új webhelyen NINCS
   webshop — ajánlatkérés és szolgáltatás van. Az ÁSZF ezért itt a szolgáltatási
   és adásvételi szerződésre koncentrál; a webshopos részek megtartva, de a
   hatály elején kimondva, mikor melyik alkalmazandó.

AMI AZ ÚJ WEBHELYEN VAN, ÉS A RÉGI TÁJÉKOZTATÓBAN NEM SZEREPELHETETT:
 · a kapcsolati és ajánlatkérő űrlapok saját SMTP-n futnak,
 · az ajánlat-összehasonlító a FELTÖLTÖTT DOKUMENTUMOT AI-szolgáltatóhoz küldi,
 · a kapcsolat oldal Google Térkép-beágyazást tölt be.
Mindhárom új adatkezelés, és mindhárom bekerült.

JOGI FELÜLVIZSGÁLAT KÖTELEZŐ ÉLESÍTÉS ELŐTT. Ez a tartalom a meglévő
dokumentumok átvétele és kiegészítése, nem ügyvédi munka.
"""
import pathlib, sys, re
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import sec_faq, slug_id, esc

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

# A gyökérben a fejléc-hivatkozások nem ../-rel kezdődnek — ugyanaz a kezelés,
# mint a kapcsolat oldalon. A csupasz `../`-ból üres href lenne, ami az AKTUÁLIS
# oldalra mutat: a logóra kattintva nem történne semmi.
HEADER = G.HEADER.replace('href="../"', 'href="./"')
HEADER = re.sub(r'href="\.\./', 'href="', HEADER)
HEADER = HEADER.replace('src="../assets/', 'src="assets/')

FRISSITVE = '2026. augusztus 7'

CEG = {
    'nev': 'ÖkoTech-Home Kft.',
    'szekhely': '2500 Esztergom, Csendesvölgy utca 27.',
    'telephely': '2509 Esztergom, Strázsa u. 12.',
    'cegjegyzek': '11-09-008852',
    'adoszam': '12268687-2-11',
    'cegbirosag': 'Tatabányai Törvényszék Cégbírósága',
    'email': 'kapcsolat@okotechhome.hu',
    'tel': '+36 33 200 211',
    'tel2': '+36 33 400 387',
    'bank': 'CIB Bank — 10700268-70877618-51100005',
    'iban': 'HU80 1070 0268 7087 7618 5110 0005',
}

NAIH = ('Nemzeti Adatvédelmi és Információszabadság Hatóság (NAIH) · '
        '1055 Budapest, Falk Miksa utca 9–11. · postacím: 1363 Budapest, Pf. 9. · '
        '+36 1 391 1400 · ugyfelszolgalat@naih.hu · naih.hu')

JOGI_MEGJ = ('<!-- JOGI FELÜLVIZSGÁLAT KÖTELEZŐ ÉLESÍTÉS ELŐTT. Ez a tartalom a cég\n'
             '     meglévő dokumentumainak átvétele és kiegészítése, NEM ügyvédi munka.\n'
             '     Külön ellenőrizendő: a székhely (lásd a generátor fejlécét), az\n'
             '     adatfeldolgozói lista aktualitása, és minden jogszabályi hivatkozás. -->')


# --- saját szekció-építők a jogi szöveghez -------------------------------

def sec_jogi(eyebrow, title, blokkok, kiemelt=None):
    """h2 + tetszőleges számú (h3, [bekezdés vagy lista]) blokk.

    A blokk lehet: ('alcim', 'Szöveg') · ('p', 'bekezdés') ·
    ('ul', [tételek]) · ('ol', [tételek]) · ('kiemelt', 'szöveg').
    """
    sid = slug_id(title) + '-cim'
    ki = ''
    if kiemelt:
        ki = f'\n      <div class="jogi-kiemelt type-ui-body"><p>{kiemelt}</p></div>'
    darabok = []
    for tipus, tartalom in blokkok:
        if tipus == 'alcim':
            darabok.append(
                f'        <h3 class="type-ui-card-title jogi-alcim">{tartalom}</h3>')
        elif tipus == 'p':
            darabok.append(f'        <p class="type-ui-body">{tartalom}</p>')
        elif tipus in ('ul', 'ol'):
            li = '\n'.join(f'          <li class="type-ui-body">{t}</li>'
                           for t in tartalom)
            darabok.append(f'        <{tipus} class="jogi-lista">\n{li}\n        </{tipus}>')
        elif tipus == 'kiemelt':
            darabok.append(
                f'        <div class="jogi-kiemelt type-ui-body"><p>{tartalom}</p></div>')
    return f'''
  <section class="section" aria-labelledby="{sid}">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">{eyebrow}</p>
        <h2 class="type-display-section-title section-title" id="{sid}">{title}</h2>
      </header>{ki}
      <div class="jogi-szoveg">
{chr(10).join(darabok)}
      </div>
    </div>
  </section>
'''


def sec_tabla(eyebrow, title, lead, fejlec, sorok):
    """Adattábla — adatkezelési célok, adatfeldolgozók, sütik."""
    sid = slug_id(title) + '-cim'
    th = '\n'.join(f'              <th scope="col">{h}</th>' for h in fejlec)
    tr = []
    for sor in sorok:
        cellak = [f'          <th scope="row">{sor[0]}</th>']
        cellak += [f'          <td class="type-ui-body">{c}</td>' for c in sor[1:]]
        tr.append('        <tr>\n' + '\n'.join(cellak) + '\n        </tr>')
    return f'''
  <section class="section" aria-labelledby="{sid}">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">{eyebrow}</p>
        <h2 class="type-display-section-title section-title" id="{sid}">{title}</h2>
        <p class="type-ui-body section-lead">{lead}</p>
      </header>
      <div class="compare-scroll" tabindex="0" role="region" aria-labelledby="{sid}">
        <table class="compare-table compare-table-start">
          <caption class="visually-hidden">{esc(title)}</caption>
          <thead>
            <tr>
{th}
            </tr>
          </thead>
          <tbody>
{chr(10).join(tr)}
          </tbody>
        </table>
      </div>
    </div>
  </section>
'''


# ===========================================================================
# 1) Adatkezelési tájékoztató
# ===========================================================================
def epit_adatkezeles():
    return [
        sec_jogi('Bevezetés', 'Ki kezeli az adatait, és mire',
                 [('p', f'Ez a tájékoztató azt írja le, hogy az <strong>{CEG["nev"]}</strong> '
                        'milyen személyes adatokat kezel az okoth.hu webhelyen keresztül '
                        'és az ahhoz kapcsolódó szolgáltatások során, milyen célból és '
                        'milyen jogalapon, meddig őrzi meg őket, kinek adja át, és Önnek '
                        'milyen jogai vannak mindezzel kapcsolatban.'),
                  ('alcim', 'Az adatkezelő'),
                  ('ul', [f'<strong>Cégnév:</strong> {CEG["nev"]}',
                          f'<strong>Székhely:</strong> {CEG["szekhely"]}',
                          f'<strong>Ügyfélszolgálat és telephely:</strong> {CEG["telephely"]}',
                          f'<strong>Cégjegyzékszám:</strong> {CEG["cegjegyzek"]} '
                          f'({CEG["cegbirosag"]})',
                          f'<strong>Adószám:</strong> {CEG["adoszam"]}',
                          f'<strong>E-mail:</strong> <a href="mailto:{CEG["email"]}">{CEG["email"]}</a>',
                          f'<strong>Telefon:</strong> {CEG["tel"]}, {CEG["tel2"]}']),
                  ('alcim', 'Adatvédelmi tisztviselő'),
                  ('p', 'A társaság tevékenysége alapján adatvédelmi tisztviselő '
                        'kijelölése nem kötelező, ezért nem jelöltünk ki. Az '
                        'adatvédelemmel kapcsolatos megkereséseket a fenti e-mail címen '
                        'fogadjuk.'),
                  ('alcim', 'Alapelvek'),
                  ('p', 'Személyes adatot kizárólag meghatározott célból, a cél '
                        'eléréséhez szükséges mértékben és ideig kezelünk. Csak olyan '
                        'adatot kérünk, amely a cél megvalósulásához elengedhetetlen, és '
                        'amelyre a cél elérésére alkalmas. Az adatkezelés minden '
                        'szakaszában megfelel a célnak.')],
                 kiemelt=f'Utolsó frissítés: <strong>{FRISSITVE}</strong>. A tájékoztatót '
                         'a jogszabályi környezet vagy a szolgáltatásaink változása esetén '
                         'módosítjuk; a mindenkori hatályos szöveg ezen az oldalon érhető el.'),

        sec_tabla('Adatkezelések', 'Mit, miért, milyen jogalapon és meddig',
                  'Minden adatkezelést külön soron kezelünk. A megőrzési idő letelte után '
                  'az adatokat töröljük vagy visszaállíthatatlanul anonimizáljuk.',
                  ['Adatkezelés', 'Kezelt adatok', 'Jogalap', 'Megőrzési idő'],
                  [
                      ('Kapcsolatfelvétel, ajánlatkérés',
                       'Név, e-mail, telefonszám, település, az üzenet tartalma és '
                       'minden, amit Ön az üzenetben megad',
                       'GDPR 6. cikk (1) b) — a szerződés megkötését megelőző lépések '
                       'az érintett kérésére',
                       'A megkeresés lezárásától számított 1 év; ha szerződés jön létre, '
                       'a szerződéses adatkezelés szerint'),
                      ('Szerződés teljesítése',
                       'Név, számlázási és telepítési cím, telefonszám, e-mail, a '
                       'megrendelés paraméterei, bankszámlaszám',
                       'GDPR 6. cikk (1) b) — szerződés teljesítése',
                       'A szerződés megszűnésétől számított 5 év (általános elévülési idő)'),
                      ('Számlázás, számviteli bizonylat',
                       'Név, cím, adószám, adózási státusz, a bizonylat adatai',
                       'GDPR 6. cikk (1) c) — jogi kötelezettség (Számv. tv., ÁFA tv.)',
                       '8 év'),
                      ('Kapcsolattartói adatok üzleti partnereknél',
                       'Név, beosztás, munkahelyi telefonszám és e-mail cím',
                       'GDPR 6. cikk (1) f) — jogos érdek a szerződés teljesítéséhez '
                       'szükséges kapcsolattartásban',
                       'A kapcsolattartói minőség megszűnésétől számított 5 év'),
                      ('Ajánlat-összehasonlító — feltöltött dokumentumok',
                       'A feltöltött ajánlatok tartalma és minden személyes adat, amit '
                       'azok tartalmaznak',
                       'GDPR 6. cikk (1) a) — hozzájárulás, amelyet a feltöltéssel ad meg',
                       'A feldolgozás után azonnal törlődik; nálunk nem tárolódik '
                       '(lásd az „AI-alapú ajánlat-összehasonlítás” szakaszt)'),
                      ('Panaszkezelés',
                       'Név, elérhetőség, a panasz tartalma, a válasz',
                       'GDPR 6. cikk (1) c) — jogi kötelezettség (Fgytv.)',
                       '5 év (a fogyasztóvédelmi törvény szerint)'),
                      ('Webhely működése — technikai naplók',
                       'IP-cím, böngésző- és eszközadatok, a lekért oldal, időbélyeg',
                       'GDPR 6. cikk (1) f) — jogos érdek a szolgáltatás biztonságos '
                       'üzemeltetésében és a visszaélések megelőzésében',
                       'Legfeljebb 30 nap'),
                      ('Sütik',
                       'Lásd a Cookie-tájékoztatót',
                       'Működéshez szükséges: Elkertv. 13/A. § · minden más: '
                       'GDPR 6. cikk (1) a) — hozzájárulás',
                       'Süti típusonként eltérő — lásd a Cookie-tájékoztatót'),
                  ]),

        sec_jogi('Új szolgáltatás', 'AI-alapú ajánlat-összehasonlítás',
                 [('p', 'A webhelyen elérhető ajánlat-összehasonlító modul a feltöltött '
                        'dokumentumokat <strong>mesterséges intelligencia szolgáltatóhoz '
                        'továbbítja</strong> feldolgozásra. Ezt külön kiemeljük, mert ez '
                        'a webhely egyetlen olyan funkciója, amely az Ön dokumentumát '
                        'harmadik félhez küldi.'),
                  ('alcim', 'Hogyan működik'),
                  ('ol', ['Ön feltölt egy vagy több ajánlatot a saját eszközéről.',
                          'A dokumentumból szöveget nyerünk ki a saját szerverünkön.',
                          'A kinyert szöveget elküldjük az AI-szolgáltatónak elemzésre.',
                          'Az elemzés eredményét megjelenítjük Önnek a böngészőben.',
                          'A feltöltött fájlt és a kinyert szöveget a feldolgozás után '
                          'töröljük. Nálunk nem tárolódik, adatbázisba nem kerül.']),
                  ('alcim', 'Mire figyeljen'),
                  ('p', 'Az ajánlatok személyes adatokat is tartalmazhatnak — nevet, '
                        'címet, telefonszámot. Ha ezeket nem szeretné továbbítani, '
                        'a feltöltés előtt takarja ki őket a dokumentumban. '
                        'A modul az összehasonlításhoz nem igényli a személyes adatokat.'),
                  ('kiemelt', 'A feltöltéssel Ön kifejezetten hozzájárul ahhoz, hogy a '
                              'dokumentum tartalmát az elemzés céljából AI-szolgáltatónak '
                              'továbbítsuk. A hozzájárulás megtagadásának egyetlen '
                              'következménye az, hogy a modul nem használható — a webhely '
                              'többi funkciója változatlanul elérhető.')],
                 kiemelt='<strong>ADATHIÁNY — élesítés előtt pótolandó:</strong> az '
                         'AI-szolgáltató pontos megnevezése, székhelye, a szerződéses '
                         'garanciák (adatfeldolgozói szerződés, EU-n kívüli továbbítás '
                         'esetén az általános szerződési feltételek), valamint az, hogy '
                         'a szolgáltató a beküldött adatot tanításra használja-e. '
                         'Enélkül ez a szakasz nem teljes.'),

        sec_tabla('Címzettek', 'Kinek adjuk át az adatait',
                  'Adatfeldolgozóink a mi utasításunkra, a mi nevünkben járnak el. '
                  'Az alábbi lista a régi webhelyről átvett állapot — a felülvizsgálata '
                  'élesítés előtt kötelező.',
                  ['Funkció', 'Adatfeldolgozó', 'Székhely'],
                  [
                      ('Webtárhely', 'A tárhelyszolgáltató megnevezése — pótolandó',
                       'Pótolandó'),
                      ('Levélküldés (SMTP)', 'Saját levelezőszerver (mail.okoth.hu)',
                       'Magyarország'),
                      ('Könyvelés, adózás', 'Bázis Könyvelő Iroda Kft.',
                       '2900 Komárom, Laktanya köz 30/A.'),
                      ('Könyvvizsgálat', 'Audit Assistance Kft.',
                       '1042 Budapest, Árpád út 51–53.'),
                      ('IT-üzemeltetés', 'PC-Ház-Terv Bt.',
                       '2500 Esztergom, Mikszáth K. u. 8.'),
                      ('Ügyfélnyilvántartás', 'Starsoft International Kft.',
                       '2517 Kesztölc, Esztergomi u. 89.'),
                      ('Szállítás', 'GLS General Logistics Systems Hungary Kft.',
                       '2351 Alsónémedi, GLS Európa u. 2.'),
                      ('Térképszolgáltatás', 'Google Ireland Limited',
                       'Gordon House, Barrow Street, Dublin 4, Írország'),
                      ('AI-elemzés', 'Az AI-szolgáltató megnevezése — pótolandó',
                       'Pótolandó'),
                  ]),

        sec_jogi('Harmadik ország', 'Adattovábbítás az Európai Gazdasági Térségen kívülre',
                 [('p', 'A Google Térkép beágyazása és — a szolgáltató megnevezésétől '
                        'függően — az AI-elemzés adattovábbítást jelenthet az EGT-n '
                        'kívülre. Ilyenkor a továbbítás jogszerűségét az Európai Bizottság '
                        'megfelelőségi határozata vagy az általános szerződési feltételek '
                        '(SCC) biztosítják.'),
                  ('kiemelt', '<strong>ADATHIÁNY:</strong> a konkrét garanciák '
                              '(megfelelőségi határozat vagy SCC) megnevezése '
                              'szolgáltatónként pótolandó élesítés előtt.')]),

        sec_jogi('Az Ön jogai', 'Mit kérhet tőlünk',
                 [('p', 'Az alábbi jogokat bármikor gyakorolhatja. Kérését a '
                        f'<a href="mailto:{CEG["email"]}">{CEG["email"]}</a> címen vagy '
                        'postai úton a székhelyünkre küldve terjesztheti elő.'),
                  ('ul', ['<strong>Hozzáférés.</strong> Tájékoztatást kérhet arról, '
                          'kezelünk-e Önről adatot, és ha igen, milyet, milyen célból, '
                          'meddig, és kinek adjuk át. Másolatot is kérhet.',
                          '<strong>Helyesbítés.</strong> Kérheti a pontatlan adat '
                          'javítását és a hiányos adat kiegészítését.',
                          '<strong>Törlés.</strong> Kérheti az adatai törlését, ha az '
                          'adatkezelés célja megszűnt, ha visszavonja a hozzájárulását, '
                          'vagy ha az adatkezelés jogellenes. A törlés nem érvényesíthető, '
                          'ha jogszabály kötelez a megőrzésre — például számviteli '
                          'bizonylatnál.',
                          '<strong>Az adatkezelés korlátozása.</strong> Kérheti, hogy az '
                          'adatait csak tároljuk, de ne kezeljük tovább — például amíg a '
                          'pontosságukat vitatja.',
                          '<strong>Adathordozhatóság.</strong> A hozzájáruláson vagy '
                          'szerződésen alapuló, automatizáltan kezelt adatait tagolt, '
                          'géppel olvasható formában kérheti, és kérheti másik '
                          'adatkezelőhöz továbbításukat.',
                          '<strong>Tiltakozás.</strong> Tiltakozhat a jogos érdeken '
                          'alapuló adatkezelés ellen. Ilyenkor csak akkor folytatjuk, ha '
                          'kényszerítő erejű jogos okot tudunk igazolni.',
                          '<strong>A hozzájárulás visszavonása.</strong> A '
                          'hozzájáruláson alapuló adatkezelésnél a hozzájárulást bármikor '
                          'visszavonhatja, ugyanolyan egyszerűen, ahogy megadta. '
                          'A visszavonás a korábbi adatkezelés jogszerűségét nem érinti.']),
                  ('alcim', 'Válaszadási határidő'),
                  ('p', 'A kérésre indokolatlan késedelem nélkül, de legkésőbb '
                        '<strong>egy hónapon belül</strong> válaszolunk. Ez a határidő '
                        'a kérelem összetettségére tekintettel két hónappal '
                        'meghosszabbítható; a hosszabbításról a kérelem kézhezvételétől '
                        'számított egy hónapon belül tájékoztatjuk.'),
                  ('alcim', 'Automatizált döntéshozatal'),
                  ('p', 'Nem hozunk Önre nézve joghatással járó, kizárólag automatizált '
                        'adatkezelésen alapuló döntést, és nem végzünk profilalkotást. '
                        'Az ajánlat-összehasonlító és az előszűrő modulok kimenete '
                        'tájékoztatás, nem döntés — a tényleges műszaki és üzleti '
                        'döntéseket ember hozza meg.')]),

        sec_jogi('Jogorvoslat', 'Ha nem ért egyet azzal, ahogy az adatait kezeljük',
                 [('p', 'Először forduljon hozzánk — a legtöbb kérdés így oldódik meg a '
                        'leggyorsabban. Ha nem jár eredménnyel, az alábbi lehetőségei '
                        'vannak.'),
                  ('alcim', 'Panasz a felügyeleti hatóságnál'),
                  ('p', NAIH),
                  ('alcim', 'Bírósági jogorvoslat'),
                  ('p', 'Az adatkezelővel vagy az adatfeldolgozóval szemben bírósághoz '
                        'fordulhat. A per — az Ön választása szerint — a lakóhelye vagy '
                        'tartózkodási helye szerinti törvényszék előtt is megindítható. '
                        'A törvényszékek illetékessége és elérhetősége a birosag.hu '
                        'oldalon található.'),
                  ('alcim', 'Adatvédelmi incidens'),
                  ('p', 'Ha olyan adatvédelmi incidens történik, amely valószínűsíthetően '
                        'magas kockázattal jár az Ön jogaira nézve, indokolatlan '
                        'késedelem nélkül tájékoztatjuk. A felügyeleti hatóság felé az '
                        'incidenst az arról való tudomásszerzéstől számított 72 órán '
                        'belül jelentjük be.')]),

        sec_faq([
            ('Kötelező megadnom az adataimat?',
             'Nem. A megadás önkéntes — de bizonyos adatok nélkül nem tudunk válaszolni. '
             'Ajánlathoz például szükségünk van elérhetőségre és a projekt alapadataira. '
             'Az űrlapokon jelöljük, mely mező kötelező, és miért.'),
            ('Küldenek hírlevelet?',
             'A megkeresésre adott válasz nem hírlevél. Marketingcélú megkeresést csak '
             'külön, kifejezett hozzájárulással küldünk, és minden ilyen levélben '
             'egyszerű leiratkozási lehetőséget biztosítunk.'),
            ('Mi történik a feltöltött ajánlataimmal?',
             'A dokumentumból szöveget nyerünk ki, azt elemzésre elküldjük az '
             'AI-szolgáltatónak, majd az eredményt megjelenítjük. A fájl és a kinyert '
             'szöveg a feldolgozás után törlődik — nálunk nem tárolódik. Ha a '
             'dokumentum személyes adatot tartalmaz, a feltöltés előtt kitakarhatja.'),
            ('Meddig őrzik meg az adataimat?',
             'Adatkezelésenként eltér — a fenti táblázat minden sornál megadja. '
             'A leghosszabb a számviteli bizonylatok 8 éves megőrzése, amit jogszabály '
             'ír elő; ezt kérésre sem tudjuk lerövidíteni.'),
        ]),
        JOGI_MEGJ,
    ]


# ===========================================================================
# 2) Cookie-tájékoztató
# ===========================================================================
def epit_cookie():
    return [
        sec_jogi('Bevezetés', 'Mik azok a sütik, és miért használunk ilyet',
                 [('p', 'A süti (cookie) kis adatfájl, amelyet a webhely az Ön '
                        'eszközére helyez el, és amelyet a böngésző a későbbi '
                        'látogatásoknál visszaküld. Van, amelyik a működéshez kell, van, '
                        'amelyik kényelmi célt szolgál, és van, amelyik mérésre vagy '
                        'hirdetésre való.'),
                  ('p', 'A működéshez feltétlenül szükséges sütikhez nem kell '
                        'hozzájárulás, de tájékoztatnunk kell róluk. Minden más sütihez '
                        '<strong>előzetes hozzájárulás</strong> szükséges, amit bármikor, '
                        'ugyanolyan egyszerűen visszavonhat, ahogy megadta.')],
                 kiemelt=f'Utolsó frissítés: <strong>{FRISSITVE}</strong>.'),

        sec_tabla('Sütikategóriák', 'Milyen sütiket használunk',
                  'A kategóriánkénti beállítást a süti-beállítások felületén bármikor '
                  'módosíthatja.',
                  ['Kategória', 'Mire való', 'Jogalap', 'Élettartam'],
                  [
                      ('Működéshez szükséges',
                       'A webhely alapvető működése: munkamenet-azonosítás, a '
                       'süti-beállítás megjegyzése, biztonsági funkciók. Enélkül a '
                       'webhely nem használható.',
                       'Elkertv. 13/A. § — hozzájárulás nem szükséges',
                       'Munkamenet végéig, illetve a beállítás megjegyzésénél '
                       'legfeljebb 12 hónap'),
                      ('Beállításokat megjegyző',
                       'Az Ön választásainak megjegyzése — például a világos vagy sötét '
                       'megjelenítés.',
                       'GDPR 6. cikk (1) a) — hozzájárulás',
                       'Legfeljebb 12 hónap'),
                      ('Statisztikai',
                       'A látogatottság mérése összesített formában: mely oldalak '
                       'népszerűek, hol akadnak el a látogatók.',
                       'GDPR 6. cikk (1) a) — hozzájárulás',
                       'A mérőeszköz beállítása szerint'),
                      ('Beágyazott térkép',
                       'A Kapcsolat oldalon a Google Térkép beágyazása. A megjelenítéssel '
                       'a Google sütiket helyezhet el és megkapja az Ön IP-címét.',
                       'GDPR 6. cikk (1) a) — hozzájárulás',
                       'A Google beállítása szerint'),
                  ]),

        sec_jogi('Harmadik fél', 'A Google Térkép beágyazása',
                 [('p', 'A Kapcsolat oldalon Google Térképet ágyazunk be, hogy a '
                        'telephelyünk megközelítése egyszerűbb legyen. A beágyazás '
                        'harmadik fél szolgáltatása.'),
                  ('ul', ['<strong>Szolgáltató:</strong> Google Ireland Limited '
                          '(Gordon House, Barrow Street, Dublin 4, Írország)',
                          '<strong>Mit kap meg:</strong> az Ön IP-címét, a böngésző- és '
                          'eszközadatokat, és a Google-fiókjához kapcsolódó adatokat, ha '
                          'be van jelentkezve',
                          '<strong>Mire használja:</strong> a térkép megjelenítésére, '
                          'valamint a Google saját adatkezelési tájékoztatójában '
                          'meghatározott célokra',
                          '<strong>Adattovábbítás:</strong> a Google az adatokat az '
                          'EGT-n kívülre is továbbíthatja']),
                  ('p', 'A Google adatkezeléséről a Google saját adatvédelmi '
                        'irányelveiben tájékozódhat. Ha nem járul hozzá a beágyazáshoz, '
                        'a térkép nem töltődik be — a cím és az útvonaltervezési '
                        'hivatkozás ettől függetlenül elérhető marad az oldalon.')],
                 kiemelt='<strong>MEGFELELŐSÉGI NYITOTT PONT — élesítés előtt rendezendő:</strong> '
                         'a Google Térkép jelenleg <em>alapértelmezésben</em> betöltődik, '
                         'hozzájárulás bekérése nélkül. Az ePrivacy és a GDPR szerint ehhez '
                         'előzetes hozzájárulás szükséges. Élesítés előtt vagy a '
                         'süti-hozzájárulási felületet kell bevezetni a térkép betöltése '
                         'elé, vagy a beágyazást kattintásra kell tölteni. '
                         'A beágyazás helye: <code>kapcsolat.html</code>, '
                         '<code>.terkep</code> szekció.'),

        sec_jogi('Beállítás', 'Hogyan módosíthatja a hozzájárulását',
                 [('alcim', 'A webhelyen'),
                  ('p', 'A süti-beállítások felületén kategóriánként engedélyezheti vagy '
                        'tilthatja a nem szükséges sütiket. A visszavonás ugyanolyan '
                        'egyszerű, mint a hozzájárulás megadása, és a visszavonás nem '
                        'érinti a korábbi adatkezelés jogszerűségét.'),
                  ('kiemelt', '<strong>ADATHIÁNY:</strong> a süti-hozzájárulási felület '
                              '(banner és beállításkezelő) még nem került be a webhelyre. '
                              'Amíg nincs, a hozzájáruláshoz kötött sütik nem '
                              'helyezhetők el jogszerűen. Élesítés előtt pótolandó.'),
                  ('alcim', 'A böngészőben'),
                  ('p', 'Minden elterjedt böngésző lehetővé teszi a sütik megtekintését, '
                        'törlését és blokkolását. A beállítás jellemzően az '
                        '„Adatvédelem” vagy „Beállítások” menüpont alatt található. '
                        'Ha az összes sütit blokkolja, a webhely egyes funkciói nem '
                        'fognak működni.'),
                  ('alcim', 'A hozzájárulás nyilvántartása'),
                  ('p', 'A hozzájárulását és annak időpontját a bizonyíthatóság érdekében '
                        'rögzítjük. Ez maga is a működéshez szükséges adatkezelés, '
                        'amelynek jogalapja a jogi kötelezettségeink teljesítése.')]),

        sec_faq([
            ('Mi történik, ha nem fogadom el a sütiket?',
             'A webhely működni fog. A működéshez szükséges sütik enélkül is elhelyezésre '
             'kerülnek — ehhez nem kell hozzájárulás —, a többi viszont nem. Ennek '
             'egyetlen látható következménye, hogy a beágyazott térkép nem töltődik be, '
             'és nem mérjük a látogatását.'),
            ('Nyomon követnek hirdetési célból?',
             'Jelenleg nem használunk hirdetési vagy remarketing sütit. Ha ez '
             'megváltozik, ez a tájékoztató frissül, és a hozzájárulást külön '
             'kategóriaként kérjük majd.'),
            ('Meddig érvényes a hozzájárulásom?',
             'A süti-beállítást legfeljebb 12 hónapig őrizzük meg, utána újra '
             'megkérdezzük. Természetesen bármikor korábban is módosíthatja.'),
        ]),
        JOGI_MEGJ,
    ]


# ===========================================================================
# 3) ÁSZF
# ===========================================================================
def epit_aszf():
    return [
        sec_jogi('Hatály', 'Mire vonatkoznak ezek a feltételek',
                 [('p', f'Ezek az Általános Szerződési Feltételek (ÁSZF) az '
                        f'<strong>{CEG["nev"]}</strong> mint Eladó és a Megrendelő '
                        'között létrejövő adásvételi és szolgáltatási szerződésekre '
                        'vonatkoznak.'),
                  ('alcim', 'Amire vonatkozik'),
                  ('ul', ['szennyvíztisztító berendezés és kapcsolódó termékek '
                          'adásvétele',
                          'telepítés, beüzemelés és kapcsolódó kivitelezési '
                          'szolgáltatások',
                          'helyszíni felmérés és műszaki tanácsadás',
                          'karbantartás és szerviz']),
                  ('alcim', 'Amire nem vonatkozik'),
                  ('p', 'Ez a webhely <strong>nem webáruház</strong>: itt közvetlenül '
                        'nem lehet terméket megvásárolni. A webhelyen ajánlatot kérhet, '
                        'a szerződés pedig az ajánlat elfogadásával, külön jön létre. '
                        'A távollévők között kötött szerződésekre vonatkozó szabályokat '
                        '— így a fogyasztói elállási jogot — akkor kell alkalmazni, ha a '
                        'szerződés ténylegesen távollévők között jött létre.'),
                  ('alcim', 'Fogyasztó és vállalkozás'),
                  ('p', 'A Polgári Törvénykönyv szerint <strong>fogyasztó</strong> a '
                        'szakmája, önálló foglalkozása vagy üzleti tevékenysége körén '
                        'kívül eljáró természetes személy. Több rendelkezés — az '
                        'elállási jog, a jótállás, a kellékszavatosság határideje — '
                        'eltér aszerint, hogy Ön fogyasztóként vagy vállalkozásként köt '
                        'szerződést. Ezt minden érintett pontban külön jelöljük.')],
                 kiemelt=f'Hatályos: <strong>{FRISSITVE}</strong>-tól. Az ÁSZF-et '
                         'egyoldalúan módosíthatjuk; a módosítás a közzététellel lép '
                         'hatályba, és a már megkötött szerződéseket nem érinti.'),

        sec_jogi('Az Eladó', 'Szerződő fél adatai',
                 [('ul', [f'<strong>Cégnév:</strong> {CEG["nev"]}',
                          f'<strong>Székhely:</strong> {CEG["szekhely"]}',
                          f'<strong>Ügyfélszolgálat és telephely:</strong> {CEG["telephely"]}',
                          f'<strong>Cégjegyzékszám:</strong> {CEG["cegjegyzek"]} '
                          f'({CEG["cegbirosag"]})',
                          f'<strong>Adószám:</strong> {CEG["adoszam"]}',
                          f'<strong>Bankszámlaszám:</strong> {CEG["bank"]}',
                          f'<strong>IBAN:</strong> {CEG["iban"]}',
                          f'<strong>E-mail:</strong> <a href="mailto:{CEG["email"]}">{CEG["email"]}</a>',
                          f'<strong>Telefon:</strong> {CEG["tel"]}, {CEG["tel2"]}'])]),

        sec_jogi('A szerződés', 'Hogyan jön létre, és mi a tartalma',
                 [('alcim', 'Az ajánlatkérés és az ajánlat'),
                  ('ol', ['A Megrendelő ajánlatot kér — a webhely űrlapján, e-mailben, '
                          'telefonon vagy személyesen.',
                          'Az Eladó az ajánlatot a kérés beérkezésétől számított '
                          '<strong>48 órán belül</strong> megküldi, munkanapokon.',
                          'A Megrendelő az ajánlatot annak megküldésétől számított '
                          '<strong>48 órán belül</strong> fogadhatja el; ezt követően az '
                          'ajánlat kötöttsége megszűnik.',
                          'A szerződés az ajánlat elfogadásának az Eladóhoz való '
                          'megérkezésével jön létre.']),
                  ('alcim', 'Az Eladó kötelezettségei'),
                  ('ul', ['a termék tulajdonjogának átruházása és átadása a '
                          'szerződésben meghatározott mennyiségben, minőségben és '
                          'leírás szerint',
                          'külön megrendelés esetén a telepítés elvégzése',
                          'műszaki átadás-átvételi eljárás lefolytatása',
                          'a berendezés működésének bemutatása, illetve a használati '
                          'útmutató átadása']),
                  ('alcim', 'A Megrendelő kötelezettségei'),
                  ('ul', ['a vételár megfizetése a szállítást megelőzően, illetve az '
                          'átadáskor',
                          'a termék átvételkori megvizsgálása',
                          'a munkavégzéshez szükséges villamos energia biztosítása',
                          'a munkaterület megközelíthetőségének biztosítása',
                          'az építési törmelék elszállításáról való gondoskodás, ha a '
                          'szerződés másként nem rendelkezik'])]),

        sec_jogi('Teljesítés', 'Szállítás, telepítés, átadás',
                 [('alcim', 'Szállítás'),
                  ('p', 'A termék a visszaigazolásban megjelölt határidőn belül kerül '
                        'kiszállításra; a határidő a teljes vételár beérkezését követő '
                        'naptól számít. Konkrét órára történő kiszállítást csak külön '
                        'megállapodás esetén tudunk vállalni.'),
                  ('alcim', 'Átvétel és megvizsgálás'),
                  ('p', 'A Megrendelő az átvételkor köteles a küldemény tartalmát '
                        'megvizsgálni és az átvételt igazolni. Szállításból eredő '
                        'sérülést az átvételkor, a fuvarozónál kell jelezni; az így '
                        'keletkezett kárért az Eladó nem felel.'),
                  ('alcim', 'Telepítés és műszaki átadás'),
                  ('p', 'A telepítést az Eladó biztonságosan, szakszerűen, gazdaságosan '
                        'és határidőben végzi el. Az időjárás a teljesítést késleltetheti. '
                        'Az Eladó a Megrendelő utasítása szerint jár el, de köteles '
                        'figyelmeztetni, ha az utasítás célszerűtlen vagy jogszabályba '
                        'ütközik. A teljesítést a dokumentált műszaki átadás-átvétel '
                        'igazolja; ha a Megrendelő az átadáson nem vesz részt, a tényleges '
                        'birtokbavétel váltja ki a teljesítés joghatásait.'),
                  ('alcim', 'Raktározás'),
                  ('p', 'Ha a kiszállítás a teljes vételár megfizetésétől számított egy '
                        'hónapon túl történik, az Eladó a terméket a megállapodott '
                        'kiszállítási időpontig díjmentesen tárolja. Az ezt követő '
                        'időszakra napi 3 000 Ft + áfa tárolási díj számítható fel.'),
                  ('alcim', 'Időpont-egyeztetés és lemondás'),
                  ('ul', ['az egyeztetett időpontot az Eladó e-mailben visszaigazolja; '
                          'a Megrendelő visszaigazolása nélkül az időpont nem foglalt',
                          'az első időpontmódosítás díjmentes',
                          'ismételt lemondás vagy módosítás esetén 15 000 Ft + áfa '
                          'adminisztrációs díj számítható fel',
                          'a szolgáltatás napját megelőző második munkanap 16:00 óráig a '
                          'lemondás díjmentes; ezt követően a kiszállási díj '
                          'felszámítható'])]),

        sec_jogi('Fizetés', 'Fizetési feltételek',
                 [('p', 'A Megrendelő a vételárat a visszaigazolást követően banki '
                        'átutalással vagy bankkártyával fizeti meg. Az Eladó a számlát '
                        'elektronikusan, a megadott e-mail címre küldi meg; a Megrendelő '
                        'az elektronikus számlát elfogadja, kivéve, ha ettől eltérően '
                        'nyilatkozik.'),
                  ('p', 'Késedelmes fizetés esetén az Eladó a Polgári Törvénykönyv '
                        'szerinti késedelmi kamatot számíthatja fel a késedelem '
                        'napjától. A behajtással kapcsolatos költségek a Megrendelőt '
                        'terhelik. Lejárt tartozás esetén az Eladó a további '
                        'szolgáltatást a rendezésig felfüggesztheti.')]),

        sec_jogi('Fogyasztói jogok', 'Elállási jog távollévők között kötött szerződésnél',
                 [('p', 'Ha a szerződés fogyasztóval, távollévők között jött létre, a '
                        'fogyasztót a 45/2014. (II. 26.) Korm. rendelet alapján '
                        '<strong>14 napon belül indokolás nélküli elállási jog</strong> '
                        'illeti meg.'),
                  ('alcim', 'A határidő'),
                  ('p', 'A 14 nap attól a naptól kezdődik, amelyen a fogyasztó vagy az '
                        'általa megjelölt, a fuvarozótól eltérő harmadik személy a '
                        'terméket átveszi. Több tétel esetén az utoljára átvett terméktől '
                        'számít. Szolgáltatásra irányuló szerződésnél a szerződés '
                        'megkötésének napjától.'),
                  ('alcim', 'Hogyan gyakorolható'),
                  ('p', 'Egyértelmű nyilatkozattal — postai úton, e-mailben vagy a '
                        '45/2014. Korm. rendelet 2. melléklete szerinti nyilatkozatminta '
                        'felhasználásával. A határidő betartottnak minősül, ha a '
                        'nyilatkozatot a határidő lejárta előtt elküldi.'),
                  ('alcim', 'A termék visszaküldése'),
                  ('p', 'A terméket indokolatlan késedelem nélkül, de legkésőbb az '
                        'elállás közlésétől számított 14 napon belül vissza kell '
                        'küldeni. A visszaküldés közvetlen költsége a fogyasztót '
                        'terheli. A fogyasztó a termék jellegének, tulajdonságainak '
                        'megállapításához szükséges használatot meghaladó használatból '
                        'eredő értékcsökkenésért felel.'),
                  ('alcim', 'Visszatérítés'),
                  ('p', 'Az Eladó az elállásról való tudomásszerzéstől számított 14 '
                        'napon belül téríti vissza a fogyasztó által megfizetett '
                        'összeget, ideértve a kiszállítás költségét is — kivéve a '
                        'legkevésbé költséges szokásos fuvarozási módtól eltérő '
                        'választásból eredő többletköltséget. A visszatérítés az eredeti '
                        'fizetési móddal történik. Az Eladó a visszatérítést '
                        'visszatarthatja, amíg a terméket vissza nem kapta, vagy amíg a '
                        'fogyasztó nem igazolta a visszaküldést.'),
                  ('alcim', 'Mikor nem gyakorolható'),
                  ('ul', ['a szolgáltatás egészének teljesítése után, ha a fogyasztó '
                          'előzetesen kifejezetten hozzájárult a teljesítés '
                          'megkezdéséhez és tudomásul vette az elállási jog elvesztését',
                          'nem előre gyártott, a fogyasztó utasítása alapján vagy '
                          'kifejezett kérésére előállított, illetve egyértelműen a '
                          'fogyasztó személyére szabott termék esetén',
                          'a fogyasztó kifejezett kérésére végzett sürgős javítási vagy '
                          'karbantartási munkánál',
                          'a jogszabályban meghatározott további esetekben']),
                  ('kiemelt', 'Szolgáltatásra irányuló szerződésnél a 14 napon túli '
                              'lemondás esetén a megrendelés szerinti díj 30%-a '
                              'meghiúsulási kötbérként számítható fel.')]),

        sec_jogi('Hibás teljesítés', 'Kellékszavatosság, termékszavatosság, jótállás',
                 [('alcim', 'Kellékszavatosság'),
                  ('p', 'Hibás teljesítés esetén a Megrendelő kijavítást vagy kicserélést '
                        'kérhet, kivéve, ha az lehetetlen vagy aránytalan többletköltséget '
                        'jelentene. Ha erre nincs mód vagy az Eladó nem vállalta, a '
                        'Megrendelő arányos árleszállítást igényelhet, a hibát az Eladó '
                        'költségére maga kijavíthatja, vagy — végső esetben — elállhat a '
                        'szerződéstől. Jelentéktelen hiba miatt elállásnak nincs helye.'),
                  ('p', 'A hibát a felfedezéstől számított <strong>két hónapon belül</strong> '
                        'közölni kell. Az igény a teljesítéstől számított '
                        '<strong>két év</strong> — vállalkozás esetén egy év — alatt évül '
                        'el. A teljesítéstől számított hat hónapon belül a hiba közlésén '
                        'túl nincs más feltétel; hat hónap után a Megrendelőnek kell '
                        'bizonyítania, hogy a hiba már a teljesítéskor megvolt.'),
                  ('alcim', 'Termékszavatosság'),
                  ('p', 'Ingó dolog hibája esetén a fogyasztó a gyártótól vagy '
                        'forgalmazótól kijavítást vagy kicserélést kérhet. A termék '
                        'akkor hibás, ha nem felel meg a forgalomba hozatalakor hatályos '
                        'minőségi követelményeknek, vagy nem rendelkezik a gyártó által '
                        'megadott tulajdonságokkal. Az igény a forgalomba hozataltól '
                        'számított <strong>két éven belül</strong> érvényesíthető. '
                        'Ugyanazon hiba miatt kellékszavatossági és termékszavatossági '
                        'igény egyszerre nem érvényesíthető.'),
                  ('alcim', 'Jótállás'),
                  ('p', 'Fogyasztói szerződés esetén az Eladó a berendezésre az átadástól '
                        'vagy a telepítéstől számított <strong>egy év</strong> jótállást '
                        'vállal. A jótállás a tartályszerkezetre és a beépített '
                        'egységekre — légbefúvó, elosztók, csővezetékek — terjed ki, '
                        'amennyiben a szállítást és a telepítést az Eladó végezte.'),
                  ('alcim', 'A jótállás nem terjed ki'),
                  ('ul', ['a rendeltetésszerű használat melletti természetes '
                          'elhasználódásra',
                          'a nem rendeltetésszerű használatból, a karbantartás '
                          'elmulasztásából vagy jogosulatlan átalakításból eredő hibára',
                          'a nem az Eladó által végzett telepítésből eredő hibára',
                          'a szállítás során keletkezett sérülésre, ha a szállítást nem '
                          'az Eladó végezte',
                          'a baktériumkultúra teljesítményére — annak állapotát a '
                          'rendszerbe juttatott vegyszerek és anyagok érdemben '
                          'befolyásolják, ez a Megrendelő ellenőrzése alatt áll']),
                  ('p', 'A jótállás érvényesítésének feltétele a rendeltetésszerű '
                        'használat és a karbantartás dokumentált igazolása. Ha a '
                        'Megrendelő a karbantartást nem tudja igazolni, az a jótállási '
                        'igényt korlátozhatja vagy kizárhatja.')]),

        sec_jogi('Felelősség', 'A felelősség korlátai',
                 [('p', 'Az Eladó a hibás teljesítésért való felelősségét a teljesítés '
                        'során részére megfizetett nettó díj 50%-áig korlátozza. Ez a '
                        'korlátozás nem terjed ki a szándékosan okozott, továbbá az '
                        'emberi életet, testi épséget vagy egészséget megkárosító '
                        'szerződésszegésre — ezekre a korlátozás jogszabály erejénél '
                        'fogva sem alkalmazható.'),
                  ('p', 'Az Eladó nem felel a következményi károkért — így az elmaradt '
                        'haszonért vagy a jóhírnév sérelméért —, továbbá mentesül, ha a '
                        'teljesítés elmaradása az ellenőrzési körén kívül eső, '
                        'előre nem látható körülmény (vis maior) következménye.')]),

        sec_jogi('Panasz', 'Panaszkezelés és jogorvoslat',
                 [('alcim', 'Panasz bejelentése'),
                  ('p', 'Panaszát szóban — személyesen vagy telefonon — és írásban is '
                        'előterjesztheti: postai úton a székhelyre, vagy e-mailben a '
                        f'<a href="mailto:{CEG["email"]}">{CEG["email"]}</a> címre. '
                        'A szóbeli panaszt lehetőség szerint azonnal orvosoljuk; ha ez '
                        'nem lehetséges, jegyzőkönyvet veszünk fel, amelynek másolatát '
                        'átadjuk vagy megküldjük.'),
                  ('alcim', 'Válaszadási határidő'),
                  ('p', 'Az írásbeli panaszra a beérkezéstől számított '
                        '<strong>30 napon belül</strong> érdemben, indokolással ellátva, '
                        'írásban válaszolunk. A panaszt elutasító álláspontunkat '
                        'megindokoljuk, és tájékoztatjuk a jogorvoslati lehetőségekről. '
                        'A panaszról felvett jegyzőkönyvet és a válasz másolatát '
                        'öt évig megőrizzük.'),
                  ('alcim', 'Békéltető testület'),
                  ('p', 'Fogyasztói jogvita esetén a fogyasztó a lakóhelye vagy '
                        'tartózkodási helye szerinti békéltető testülethez fordulhat. '
                        'Az Eladó székhelye szerint illetékes: <strong>Komárom-Esztergom '
                        'Vármegyei Békéltető Testület</strong> — 2800 Tatabánya, Fő tér '
                        '36. · +36 34 513 010 · '
                        '<a href="mailto:bekeltetes@kemkik.hu">bekeltetes@kemkik.hu</a>. '
                        'Az Eladót a békéltető testületi eljárásban együttműködési '
                        'kötelezettség terheli.'),
                  ('alcim', 'Fogyasztóvédelmi hatóság'),
                  ('p', 'A fogyasztó a lakóhelye szerint illetékes fogyasztóvédelmi '
                        'hatósághoz is fordulhat. A hatósági feladatokat a fővárosi és '
                        'vármegyei kormányhivatalok látják el; elérhetőségük a '
                        'kormanyhivatal.hu oldalon található.'),
                  ('alcim', 'Online vitarendezés'),
                  ('p', 'Online megkötött szerződéssel összefüggő jogvita esetén a '
                        'fogyasztó az Európai Bizottság online vitarendezési platformját '
                        'is igénybe veheti.'),
                  ('kiemelt', '<strong>ELLENŐRIZENDŐ ÉLESÍTÉS ELŐTT:</strong> az EU '
                              'online vitarendezési (ODR) platformjának működése és '
                              'elérhetősége megváltozott. Publikálás előtt ellenőrizni '
                              'kell az aktuális állapotot, és ennek megfelelően kell '
                              'megadni vagy elhagyni a hivatkozást.')]),

        sec_jogi('Záró rendelkezések', '',
                 [('p', 'Az ÁSZF valamely rendelkezésének érvénytelensége a többi '
                        'rendelkezés érvényességét nem érinti. Az itt nem szabályozott '
                        'kérdésekben a magyar jog — különösen a Polgári Törvénykönyvről '
                        'szóló 2013. évi V. törvény és a 45/2014. (II. 26.) Korm. '
                        'rendelet — az irányadó.'),
                  ('p', 'A webhely tartalma — szöveg, kép, szerkezet — szerzői jogi '
                        'védelem alatt áll. A webhely használata nem keletkeztet jogot a '
                        'tartalom felhasználására.')]),

        sec_faq([
            ('Ez a webhely webáruház?',
             'Nem. Itt ajánlatot kérhet, de közvetlenül nem vásárolhat. A szerződés az '
             'ajánlat elfogadásával, külön jön létre — ezért az ÁSZF is elsősorban az '
             'adásvételi és szolgáltatási szerződésre vonatkozik.'),
            ('Meddig érvényes az ajánlatuk?',
             'Az ajánlat megküldésétől számított 48 óráig. Ez rövidnek tűnhet, de az '
             'ajánlat összeállításához használt árak és kapacitások ennyi ideig '
             'tarthatók. Ha több időre van szüksége, jelezze — jellemzően meg tudjuk '
             'hosszabbítani.'),
            ('Mennyi a jótállás?',
             'Fogyasztói szerződés esetén egy év az átadástól vagy a telepítéstől. '
             'A kellékszavatossági igény ettől függetlenül két évig érvényesíthető. '
             'A jótállás feltétele a dokumentált, rendeltetésszerű használat és '
             'karbantartás.'),
            ('A baktériumkultúrára is jár jótállás?',
             'Nem. A baktériumkultúra állapotát érdemben befolyásolja, hogy milyen '
             'anyagok kerülnek a rendszerbe — ez a használat során a Megrendelő '
             'ellenőrzése alatt áll. Ezért erre a jótállás nem terjed ki. '
             'Az üzemeltetési oldalon részletesen leírjuk, mit nem szabad a rendszerbe '
             'juttatni.'),
        ]),
        JOGI_MEGJ,
    ]


# ===========================================================================
# 4) Jogi nyilatkozat / impresszum
# ===========================================================================
def epit_jogi_nyilatkozat():
    return [
        sec_jogi('Impresszum', 'A szolgáltató adatai',
                 [('ul', [f'<strong>Cégnév:</strong> {CEG["nev"]}',
                          f'<strong>Székhely:</strong> {CEG["szekhely"]}',
                          f'<strong>Ügyfélszolgálat és telephely:</strong> {CEG["telephely"]}',
                          f'<strong>Cégjegyzékszám:</strong> {CEG["cegjegyzek"]}',
                          f'<strong>Nyilvántartó cégbíróság:</strong> {CEG["cegbirosag"]}',
                          f'<strong>Adószám:</strong> {CEG["adoszam"]}',
                          f'<strong>Bankszámlaszám:</strong> {CEG["bank"]}',
                          f'<strong>IBAN:</strong> {CEG["iban"]}',
                          f'<strong>E-mail:</strong> <a href="mailto:{CEG["email"]}">{CEG["email"]}</a>',
                          f'<strong>Telefon:</strong> {CEG["tel"]}, {CEG["tel2"]}']),
                  ('kiemelt', '<strong>ADATHIÁNY — élesítés előtt pótolandó:</strong> '
                              'a képviselő (ügyvezető) neve, valamint a '
                              'tárhelyszolgáltató neve, székhelye és elérhetősége. '
                              'Az elektronikus kereskedelmi szolgáltatásokról szóló '
                              'törvény mindkettőt megköveteli.')]),

        sec_jogi('Szerzői jog', 'A webhely tartalmának felhasználása',
                 [('p', 'A webhelyen megjelenő tartalom — szöveg, ábra, fénykép, '
                        'grafika, logó, szerkezeti felépítés és forráskód — szerzői jogi '
                        'védelem alatt áll. A jogosult a szolgáltató, illetve az egyes '
                        'műveknél megjelölt jogtulajdonos.'),
                  ('p', 'A tartalom bármilyen formában történő átvétele, többszörözése, '
                        'terjesztése vagy más módon való felhasználása kizárólag a '
                        'jogosult előzetes írásbeli engedélyével lehetséges. Ez alól '
                        'kivétel a szerzői jogi törvény szerinti szabad felhasználás — '
                        'így a forrás megjelölésével történő idézés.'),
                  ('p', 'A webhelyre mutató hivatkozás elhelyezése engedély nélkül is '
                        'megengedett, feltéve, hogy az nem kelt megtévesztő látszatot a '
                        'szolgáltatóval fennálló kapcsolatról.')]),

        sec_jogi('Felelősség', 'A tartalom pontossága és a hivatkozások',
                 [('alcim', 'A közölt információk'),
                  ('p', 'A webhely tartalmát a lehető legnagyobb gondossággal állítjuk '
                        'össze, de az itt közölt információk <strong>tájékoztató '
                        'jellegűek</strong>. Nem minősülnek ajánlattételnek, műszaki '
                        'tervnek, hatósági állásfoglalásnak vagy jogi tanácsadásnak.'),
                  ('p', 'A műszaki tartalom — a méretezési, telekalkalmassági és '
                        'kapacitási útmutatók, valamint az előszűrő modulok kimenete — '
                        'tájékozódásra szolgál. Konkrét projektre vonatkozó döntést '
                        'kizárólag a helyszín és a rendelkezésre álló adatok ismeretében, '
                        'szakemberrel egyeztetve hozzon.'),
                  ('alcim', 'Jogszabályi hivatkozások'),
                  ('p', 'A webhelyen szereplő jogszabályi hivatkozások a közzététel '
                        'időpontjában hatályos állapotot tükrözik. A jogszabályi környezet '
                        'változhat; a mindenkori hatályos szöveg a Nemzeti Jogszabálytárban '
                        '(njt.hu) érhető el. Engedélyezési és hatósági kérdésben mindig az '
                        'illetékes hatóság aktuális tájékoztatása az irányadó.'),
                  ('alcim', 'Külső hivatkozások'),
                  ('p', 'A webhelyről más webhelyekre mutató hivatkozások tartalmáért nem '
                        'vállalunk felelősséget. A hivatkozott oldalak adatkezelésére a '
                        'saját tájékoztatójuk vonatkozik.'),
                  ('alcim', 'Elérhetőség'),
                  ('p', 'Törekszünk a webhely folyamatos elérhetőségére, de a '
                        'megszakításmentes működésért felelősséget nem vállalunk. '
                        'Karbantartás, üzemzavar vagy a szolgáltatói hálózat hibája miatt '
                        'a szolgáltatás átmenetileg szünetelhet.')]),

        sec_jogi('Kapcsolódó dokumentumok', '',
                 [('ul', ['<a href="adatkezelesi-tajekoztato">Adatkezelési tájékoztató</a> '
                          '— milyen személyes adatot kezelünk, miért és meddig',
                          '<a href="cookie-tajekoztato">Cookie-tájékoztató</a> — milyen '
                          'sütiket használunk, és hogyan állíthatja be őket',
                          '<a href="aszf">Általános Szerződési Feltételek</a> — a '
                          'szerződéskötés és a teljesítés szabályai',
                          '<a href="akadalymentessegi-nyilatkozat">Akadálymentességi '
                          'nyilatkozat</a> — a webhely akadálymentességi állapota'])]),
        JOGI_MEGJ,
    ]


# ===========================================================================
# 5) Akadálymentességi nyilatkozat
# ===========================================================================
def epit_akadalymentesseg():
    return [
        sec_jogi('Elköteleződés', 'Mit vállalunk',
                 [('p', f'Az <strong>{CEG["nev"]}</strong> arra törekszik, hogy az '
                        'okoth.hu webhely mindenki számára használható legyen, '
                        'függetlenül attól, milyen eszközzel vagy segítő technológiával '
                        'böngészi.'),
                  ('p', 'A webhelyet a <strong>WCAG 2.2 AA</strong> szintű '
                        'követelményekhez igazítjuk. Ez az a szint, amelyet az '
                        'akadálymentesítési irányelveket átültető magyar szabályozás is '
                        'alapul vesz.')],
                 kiemelt=f'A nyilatkozat elkészítésének és utolsó felülvizsgálatának '
                         f'időpontja: <strong>{FRISSITVE}</strong>. A nyilatkozat '
                         'önértékelésen alapul.'),

        sec_jogi('Állapot', 'Amit megvalósítottunk',
                 [('alcim', 'Szerkezet és navigáció'),
                  ('ul', ['minden oldal szemantikus HTML-lel épül: fejléc, főtartalom, '
                          'lábléc, valódi címsorhierarchia',
                          'a főtartalomra ugró hivatkozás („Ugrás a tartalomra”) minden '
                          'oldal első eleme',
                          'a navigáció billentyűzettel teljes egészében bejárható',
                          'a morzsamenü minden aloldalon jelzi az oldal helyét a '
                          'szerkezetben',
                          'a lenyíló menük natív HTML-elemekre épülnek, és JavaScript '
                          'nélkül is működnek']),
                  ('alcim', 'Megjelenés'),
                  ('ul', ['a szövegek kontrasztaránya megfelel a WCAG 2.2 AA '
                          'követelményének — normál szövegnél legalább 4,5:1',
                          'a fókusz minden interaktív elemen láthatóan jelölt',
                          'az információt nem kizárólag szín hordozza',
                          'a szövegméret a böngészőben nagyítható a tartalom '
                          'elvesztése nélkül',
                          'az érintőcélpontok legalább 44×44 képpont méretűek',
                          'a `prefers-reduced-motion` beállítást tiszteletben tartjuk: '
                          'aki csökkentett mozgást kér, annál az animációk leállnak']),
                  ('alcim', 'Tartalom'),
                  ('ul', ['minden érdemi kép szöveges alternatívával rendelkezik; a '
                          'díszítő elemek a segítő technológia elől el vannak rejtve',
                          'az űrlapmezők címkével rendelkeznek, a hibaüzenetek '
                          'szövegesek és a mezőhöz kapcsoltak',
                          'a dinamikus visszajelzéseket `aria-live` régió közli, így a '
                          'képernyőolvasó is megkapja őket',
                          'a táblázatok fejléccel és összefoglalóval rendelkeznek',
                          'a nyelv `lang` attribútummal jelölt']),
                  ('alcim', 'Működés JavaScript nélkül'),
                  ('p', 'A webhely minden érdemi funkciója működik JavaScript nélkül is. '
                        'Az űrlapok szerveroldali feldolgozással is elküldhetők, a '
                        'lenyíló tartalmak natív HTML-elemek, és a szkript csak '
                        'kiegészíti, nem helyettesíti a működést.')]),

        sec_jogi('Korlátok', 'Amit még nem, vagy nem teljesen tudunk biztosítani',
                 [('p', 'Az őszinteség többet ér, mint a teljes megfelelés állítása. '
                        'Az alábbiak jelenleg nem, vagy nem teljesen felelnek meg a '
                        'követelményeknek.'),
                  ('ul', ['<strong>Beágyazott térkép.</strong> A Kapcsolat oldalon '
                          'megjelenő Google Térkép harmadik fél szolgáltatása, amelynek '
                          'akadálymentességére nincs ráhatásunk. Ezért a cím szövegesen '
                          'is szerepel az oldalon, és útvonaltervezési hivatkozást is '
                          'adunk.',
                          '<strong>Mozgóképes háttér.</strong> Ahol a nyitóképen '
                          'mozgókép szerepel, a változó háttér miatt a szövegkontraszt '
                          'nem garantálható minden képkockán. A csökkentett mozgást kérő '
                          'beállításnál a mozgókép nem töltődik be.',
                          '<strong>Letölthető dokumentumok.</strong> A későbbiekben '
                          'közzétett PDF-dokumentumok akadálymentessége nem minden '
                          'esetben biztosított. Kérésre elérhetővé tesszük az adott '
                          'tartalmat akadálymentes formában.',
                          '<strong>Külső hivatkozások.</strong> A más webhelyekre mutató '
                          'hivatkozások célpontjának akadálymentességéért nem tudunk '
                          'felelősséget vállalni.']),
                  ('kiemelt', '<strong>ADATHIÁNY — élesítés előtt pótolandó:</strong> a '
                              'nyilatkozat jelenleg önértékelésen alapul. Élesítés előtt '
                              'javasolt független akadálymentességi vizsgálat, és annak '
                              'eredményét — a vizsgálat módszerét, dátumát és a vizsgáló '
                              'megnevezését — ide kell átvezetni.')]),

        sec_jogi('Visszajelzés', 'Ha akadályba ütközik',
                 [('p', 'Ha a webhely valamely tartalma vagy funkciója nem érhető el az '
                        'Ön számára, kérjük, jelezze. Igyekszünk a lehető leggyorsabban '
                        'orvosolni, és ha az adott tartalom azonnal nem javítható, '
                        'akadálymentes formában bocsátjuk a rendelkezésére.'),
                  ('ul', [f'<strong>E-mail:</strong> <a href="mailto:{CEG["email"]}">{CEG["email"]}</a>',
                          f'<strong>Telefon:</strong> {CEG["tel"]}',
                          f'<strong>Postai cím:</strong> {CEG["szekhely"]}']),
                  ('p', 'Kérjük, jelezze, melyik oldalról van szó, mit szeretett volna '
                        'megtenni, és milyen eszközt vagy segítő technológiát használ. '
                        'A visszajelzésre a beérkezéstől számított 30 napon belül '
                        'válaszolunk.'),
                  ('alcim', 'Ha nem elégedett a válasszal'),
                  ('p', 'Ha a bejelentésére nem kapott választ, vagy a választ nem '
                        'tartja kielégítőnek, panasszal fordulhat a fogyasztóvédelmi '
                        'hatósághoz. A hatósági feladatokat a fővárosi és vármegyei '
                        'kormányhivatalok látják el.')]),

        sec_faq([
            ('Milyen segítő technológiákkal használható a webhely?',
             'A webhely szemantikus HTML-re épül, ezért az elterjedt képernyőolvasókkal '
             'és a billentyűzetes navigációval használható. Ha valamelyik segítő '
             'technológiával mégis akadályba ütközik, kérjük, jelezze — a konkrét eset '
             'többet segít, mint az általános tesztelés.'),
            ('Nagyíthatom a szöveget?',
             'Igen. A webhely relatív méretegységeket használ, ezért a böngésző '
             'nagyítása és a beállított nagyobb alapbetűméret is működik, a tartalom '
             'elvesztése nélkül.'),
            ('Ki tudom kapcsolni az animációkat?',
             'A rendszerszintű „csökkentett mozgás” beállítást a webhely tiszteletben '
             'tartja: ilyenkor az animációk leállnak, és a mozgóképes háttér sem '
             'töltődik be. A beállítás az operációs rendszer kisegítő lehetőségei között '
             'található.'),
        ]),
        JOGI_MEGJ,
    ]


# ===========================================================================
HOME = ('Főoldal', './')

OLDALAK = [
    dict(file='adatkezelesi-tajekoztato.html', url='adatkezelesi-tajekoztato',
         img='kapcsolat',
         title='Adatkezelési tájékoztató | ÖkoTech Home',
         desc='Milyen személyes adatot kezelünk, milyen célból és jogalapon, meddig '
              'őrizzük meg, kinek adjuk át — és Önnek milyen jogai vannak.',
         h1='Adatkezelési tájékoztató',
         alt='Iratrendezőben sorakozó dokumentumok egy irodai polcon',
         lead='Ez a tájékoztató azt írja le, hogyan kezeljük a személyes adatait — '
              'célonként, jogalappal és konkrét megőrzési idővel.',
         crumbs=[HOME], sections=epit_adatkezeles()),

    dict(file='cookie-tajekoztato.html', url='cookie-tajekoztato', img='helyzetem',
         title='Cookie-tájékoztató | ÖkoTech Home',
         desc='Milyen sütiket használ a webhely, milyen jogalapon, meddig — és hogyan '
              'módosíthatja vagy vonhatja vissza a hozzájárulását.',
         h1='Cookie-tájékoztató',
         alt='Laptop képernyője egy webhely beállítási felületével',
         lead='Van süti, amely a működéshez kell, és van, amelyhez az Ön hozzájárulása. '
              'Itt kategóriánként leírjuk, melyik melyik.',
         crumbs=[HOME], sections=epit_cookie()),

    dict(file='aszf.html', url='aszf', img='attekintes',
         title='Általános Szerződési Feltételek | ÖkoTech Home',
         desc='A szerződéskötés menete, teljesítés, fizetés, fogyasztói elállási jog, '
              'jótállás és szavatosság, panaszkezelés és jogorvoslat.',
         h1='Általános Szerződési Feltételek',
         alt='Aláírásra előkészített szerződés és toll egy asztalon',
         lead='A szerződéskötés és a teljesítés szabályai. Ahol a fogyasztókra és a '
              'vállalkozásokra eltérő szabály vonatkozik, azt külön jelöljük.',
         crumbs=[HOME], sections=epit_aszf()),

    dict(file='jogi-nyilatkozat.html', url='jogi-nyilatkozat', img='alternativak',
         title='Jogi nyilatkozat és impresszum | ÖkoTech Home',
         desc='A szolgáltató adatai, a webhely tartalmának szerzői jogi védelme, és a '
              'közölt információk felhasználásának korlátai.',
         h1='Jogi nyilatkozat',
         alt='Céges dokumentumok és bélyegző egy íróasztalon',
         lead='A szolgáltató adatai, a tartalom felhasználásának szabályai, és annak '
              'kimondása, hogy a webhely műszaki tartalma tájékoztató jellegű.',
         crumbs=[HOME], sections=epit_jogi_nyilatkozat()),

    dict(file='akadalymentessegi-nyilatkozat.html',
         url='akadalymentessegi-nyilatkozat', img='mar-van-rendszerem',
         title='Akadálymentességi nyilatkozat | ÖkoTech Home',
         desc='A webhely akadálymentességi állapota a WCAG 2.2 AA szinthez mérve — '
              'amit megvalósítottunk, és amit még nem.',
         h1='Akadálymentességi nyilatkozat',
         alt='Billentyűzet és képernyőolvasót használó személy keze a munkaasztalon',
         lead='Az őszinteség többet ér, mint a teljes megfelelés állítása: itt szerepel '
              'az is, amit megvalósítottunk, és az is, amit még nem.',
         crumbs=[HOME], sections=epit_akadalymentesseg()),
]

if __name__ == '__main__':
    for o in OLDALAK:
        html = G.build(o)
        # Gyökérszint: a fejléc és az eszközhivatkozások ../ nélkül állnak.
        html = html.replace(G.HEADER, HEADER)
        html = re.sub(r'(href|src|imagesrcset|srcset)="\.\./', r'\1="', html)
        html = html.replace('../assets/', 'assets/')
        out = WEB / o['file']
        out.write_text(html, encoding='utf-8')
        print(f"  {o['file']:40s} {len(out.read_text(encoding='utf-8'))//1024} KB")
