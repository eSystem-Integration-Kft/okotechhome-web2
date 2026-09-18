#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aszf_oldalak.py — a két ÁSZF a webhelyen.

MIÉRT KETTŐ. A magyar jog a FOGYASZTÓRA kötelező szabályokat ír elő, amelyek a
vállalkozásra nem vonatkoznak: 14 napos elállási jog (45/2014. Korm. r.),
kötelező jótállás (151/2003. Korm. r.), termékszavatosság, békéltető testület.
Ezért két külön szerződés van, és ezért hosszabb a fogyasztói 2,3-szor. A
jótállás is emiatt tér el: fogyasztónak 3 év, vállalkozásnak 1 év — a tartályra
mindkettőben 15 év, feltétellel.

    /aszf                    Fogyasztók részére
    /aszf-vallalkozasoknak   Fogyasztónak nem minősülő vásárlók részére

A SZÖVEG SZÓ SZERINT KERÜL ÁT. Jogi dokumentum: nem rövidítjük, nem fogalmazzuk
át, nem hagyunk ki belőle. A generátor dolga a TAGOLÁS — fejezet, alcím,
felsorolás, táblázat —, hogy olvasható legyen. A forrás a `.docx`, és ha a
jogász újat küld, elég a fájlt cserélni és ezt újrafuttatni.

AMI A FORRÁSDOKUMENTUMBAN ELAVULT (2026-09-18-án jelezve Belának, a szövegen NEM
változtattunk, mert jogi tartalom):
  · a preambulum a `okotechhome.hu/formok/megrendel.php` címre hivatkozik (ma 301),
  · „Biológiai szennyvíztisztítók 1-től 50 főig" — a kánon szerint 6–50 LE,
  · regisztrációhoz kötött megrendelést ír le, ami az új webhelyen nincs,
  · „Ökotech-Home Kft." írásmód a kánon ÖkoTech-Home alakja helyett.

FUTTATÁS:  python3 scripts/oldalgyartas/aszf_oldalak.py
"""
import html as H
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from aszf_forras import szakaszok
from jogi_oldalak import HEADER, sec_jogi, sec_tabla
from sablon import sec_faq

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
FORRAS = pathlib.Path.home() / 'Desktop'
HOME = ('Főoldal', './')

# fejezetcím → a szakasz fölötti kis címke. Ami nincs benne, az „Szerződés".
CIMKE = {
    'PREAMBULUM': 'Bevezetés',
    '1. ELADÓ ADATAI': 'Szerződő fél',
    'ELADÓ KÖTELEZETTSÉGEI': 'Kötelezettségek',
    'MEGRENDELŐ KÖTELEZETTSÉGEI': 'Kötelezettségek',
    'SZÁLLÍTÁSI ÉS FIZETÉSI FELTÉTELEK': 'Szállítás',
    'A MEGRENDELÉS FOLYAMATA': 'Megrendelés',
    'A SZERZŐDÉS TELJESÍTÉSE': 'Teljesítés',
    'RAKTÁROZÁSI MEGÁLLAPODÁS': 'Raktározás',
    'IDŐPONTEGYEZTETÉS, LEMONDÁSOK KEZELÉSE': 'Időpont',
    'FIZETÉSI FELTÉTELEK': 'Fizetés',
    'SZELLEMI TULAJDON': 'Szerzői jog',
    'FELELŐSSÉG': 'Felelősség',
    'JÓTÁLLÁS, SZAVATOSSÁG': 'Jótállás',
    'JÓTÁLLÁS': 'Jótállás',
    'ELÁLLÁS, FELMONDÁS': 'Elállás',
    'ELÁLLÁSI JOG GYAKORLÁSÁNAK A MENETE': 'Elállás',
    'AZ ÁSZF KÖZZÉTÉTELE ÉS MÓDOSÍTÁSA': 'Hatály',
    'ZÁRÓ RENDELKEZÉSEK': 'Záró rész',
    'PANASZ': 'Panasz',
    '1. számú melléklet': 'Melléklet',
    '2. számú melléklet': 'Melléklet',
}

# A csupa nagybetűs fejezetcím a lapon mondatkezdő alakban áll — kiabálás
# helyett olvasható címsor. A rövidítések nagybetűsek maradnak.
ROVIDITES = {'ÁSZF', 'GDPR'}


def cimke_alak(cim):
    cim = cim.rstrip(':').strip()
    # A MELLÉKLET SORSZÁMA A CÍM RÉSZE — a fejezetek elején álló számozás
    # viszont a Word automatikus listája, azt levágjuk.
    if not re.match(r'^\d+\. számú melléklet$', cim):
        cim = re.sub(r'^\d+\.\s*', '', cim)
    else:
        return cim
    szavak = []
    for i, sz in enumerate(cim.split()):
        tiszta = sz.strip(',.')
        if tiszta in ROVIDITES:
            szavak.append(sz)
        elif i == 0:
            szavak.append(sz[0] + sz[1:].lower())
        else:
            szavak.append(sz.lower())
    return ' '.join(szavak)


MEGYE = re.compile(r'^(Budapest|[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]+(-[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]+)?)'
                   r'\s+(megye|megyei)?\s*$', re.U)


def bekeltetok(blokkok, kezdo):
    """A békéltető testületek felsorolásából táblázat.

    Húsz megye, mindegyik öt-hat soron: megnevezés, cím, telefon, e-mail, web.
    Bekezdésfolyamként olvashatatlan; táblázatban egy pillantás.
    """
    sorok, aktualis = [], None
    vege = kezdo
    for i in range(kezdo, len(blokkok)):
        tipus, tartalom = blokkok[i]
        if tipus != 'p':
            break
        vege = i + 1
        if MEGYE.match(tartalom):
            aktualis = [tartalom.strip(), [], []]
            sorok.append(aktualis)
        elif aktualis is None:
            break
        elif tartalom.lower().startswith(('e-mail', 'web', 'fax', '(+36')) or tartalom[:1] == '+':
            aktualis[2].append(tartalom)
        else:
            aktualis[1].append(tartalom)
    tabla = [(nev, '<br>'.join(H.escape(x) for x in cim),
              '<br>'.join(H.escape(x) for x in elerheto)) for nev, cim, elerheto in sorok]
    return tabla, vege


def szakasz_html(cim, blokkok):
    """Egy fejezet a lapon. A listaelemként érkező alcímeket kiemeljük."""
    ki, lista = [], []

    def zar():
        if lista:
            ki.append(('ol', [H.escape(x) for x in lista]))
            lista.clear()

    i = 0
    while i < len(blokkok):
        tipus, tartalom = blokkok[i]
        if tipus == 'ul':
            for t in tartalom:
                t = re.sub(r'^\.\s*', '', t).strip()
                if len(t) <= 70 and t.endswith(':'):
                    zar()
                    ki.append(('alcim', H.escape(t.rstrip(':'))))
                elif t:
                    lista.append(t)
        elif tipus == 'alcim':
            zar()
            ki.append(('alcim', H.escape(tartalom)))
            if 'békéltető testületek elérhetőségei' in tartalom:
                tabla, i = bekeltetok(blokkok, i + 1)
                if tabla:
                    ki.append(('tabla', tabla))
                continue
        else:
            zar()
            ki.append(('p', H.escape(tartalom)))
        i += 1
    zar()
    return ki


def epit(ut):
    """A dokumentum szakaszai a lapon, EREDETI SORRENDBEN.

    A táblázat ott áll, ahol a dokumentumban: a szöveg kettéválik előtte és
    utána. Korábban a végére került, és a keltezés meg a mellékletek elé
    csúsztak.
    """
    ki = []
    for cim, blokkok in szakaszok(ut):
        if cim is None:            # a dokumentum saját címlapja — a lap h1-e viszi
            continue
        cimke = CIMKE.get(cim.rstrip(':'), 'Szerződés')
        nev = cimke_alak(cim)
        resz = []
        for tipus, tartalom in szakasz_html(cim, blokkok):
            if tipus == 'tabla':
                if resz:
                    ki.append(sec_jogi(cimke, nev, resz)); resz = []
                ki.append(sec_tabla('Jogorvoslat', 'Békéltető testületek',
                                    'Megyénként, a kamarák mellett működő független szervezetek.',
                                    ['Megye', 'Cím', 'Elérhetőség'], tartalom))
                cimke, nev = cimke, nev + ' — folytatás'
            else:
                resz.append((tipus, tartalom))
        if resz:
            ki.append(sec_jogi(cimke, nev, resz))
    return ki


HATALY = re.compile(r'Jelen ÁSZF (\d{4})\. (\w+) (\d{1,2})\. napján lép hatályba')


def hatalyos(ut):
    """A szerződés hatálybalépése — a lap fejlécében és a sémában is ez áll."""
    for _, blokkok in szakaszok(ut):
        for _, tartalom in blokkok:
            for s in ([tartalom] if isinstance(tartalom, str) else tartalom):
                m = HATALY.search(s)
                if m:
                    honap = ['január', 'február', 'március', 'április', 'május', 'június',
                             'július', 'augusztus', 'szeptember', 'október', 'november',
                             'december'].index(m.group(2)) + 1
                    return f'{m.group(1)}. {m.group(2)} {m.group(3)}.', \
                           f'{m.group(1)}-{honap:02d}-{int(m.group(3)):02d}'
    return None, None


def valaszto(masik_url, masik_cim, itt, hatalyos_nap):
    """A lap tetején: melyik dokumentum vonatkozik Önre."""
    return f'''
  <section class="section" aria-labelledby="valaszto-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Melyik vonatkozik Önre</p>
        <h2 class="type-display-section-title section-title" id="valaszto-cim">Két szerződés, két vásárlói kör</h2>
      </header>
      <div class="jogi-szoveg">
        <p class="type-ui-body">A magyar jog a fogyasztóra olyan kötelező szabályokat ír elő — 14 napos
          elállási jog, kötelező jótállás, termékszavatosság, békéltető testület —, amelyek a
          vállalkozásokra nem vonatkoznak. Ezért két külön szerződésünk van.</p>
        <ul class="jogi-lista">
          <li class="type-ui-body"><strong>Ezt a lapot olvassa</strong>, ha {itt}</li>
          <li class="type-ui-body">A másik dokumentum a <a href="{masik_url}">{masik_cim}</a>.</li>
          <li class="type-ui-body"><strong>Hatályos:</strong> {hatalyos_nap}</li>
        </ul>
      </div>
    </div>
  </section>
'''


def letoltes(fajl, cim):
    return f'''
  <section class="section section-alt" aria-labelledby="letoltes-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Letöltés</p>
        <h2 class="type-display-section-title section-title" id="letoltes-cim">A dokumentum PDF-ben</h2>
      </header>
      <div class="jogi-szoveg">
        <p class="type-ui-body">Ugyanez a szöveg letölthető és nyomtatható formában. Az űrlapok
          visszaigazoló levele is ezt csatolja, hogy utólag is bizonyítható legyen, mi állt itt a
          beküldés pillanatában.</p>
        <p><a class="btn btn-secondary" href="assets/dok/{fajl}" download>{cim} (PDF)</a></p>
      </div>
    </div>
  </section>
'''



# A `sablon.py` KERETE ELAVULT: csak a `site.js` régi változatát emeli be, és
# hiányzik belőle a témabetöltő, a süti-hozzájárulás, a kampánykód és a
# késleltetett kalauz. Mérve 2026-09-18-án: a frissen gyártott lap `meres.js`-t
# kapott `suti.js` nélkül — vagyis hozzájárulás nélküli mérést. Ezért a keretet
# nem a sablonból vesszük, hanem egy KIADOTT jogi lapról: ami ott áll, az a
# webhely mindenkori állapota.
MINTA_LAP = WEB / 'adatkezelesi-tajekoztato.html'

FEJ_MINTA = re.compile(
    r'<link rel="preload" as="font"[^>]*>'
    r'|<script>\(\(\)=>\{try\{var t=localStorage.*?</script>'
    r'|<script src="[^"]*(?:tema|suti|kampany)\.js[^"]*"[^>]*></script>', re.S)


def keret_szinkron(html):
    minta = MINTA_LAP.read_text(encoding='utf-8')
    fej = minta[:minta.index('</head>')]
    for m in FEJ_MINTA.finditer(fej):
        if m.group(0) not in html:
            html = html.replace('</head>', m.group(0) + '\n</head>', 1)
    # A záró szkriptsor egyben cserélődik: a sorrend is számít (a `betolto.js`
    # a késleltetett szkripteket a `site.js` után indítja).
    veg = minta[minta.rindex('</footer>') + len('</footer>'):]
    sorok = re.findall(r'<script[^>]*src="[^"]*"[^>]*></script>', veg)
    regi = re.search(r'<script[^>]*src="[^"]*site\.js[^"]*"[^>]*></script>', html)
    if regi and sorok:
        html = html[:regi.start()] + '\n'.join(sorok) + html[regi.end():]
    return html


# A GYIK A KORÁBBI ÁSZF-LAPRÓL MARAD — ez az egyetlen rész, amely nem a
# dokumentumból jön. A szerződés szövege pontos, de nem válaszol arra, amit egy
# érdeklődő ténylegesen kérdez; ezért a lap végén ott a négy leggyakoribb.
GYIK_FOGYASZTO = [
    ('Ez a webhely webáruház?',
     'Nem. Itt ajánlatot kérhet, de közvetlenül nem vásárolhat. A szerződés az ajánlat '
     'elfogadásával, külön jön létre — ezért az ÁSZF is elsősorban az adásvételi és '
     'szolgáltatási szerződésre vonatkozik.'),
    ('Meddig érvényes az ajánlatuk?',
     'Az ajánlat megküldésétől számított 48 óráig. Ez rövidnek tűnhet, de az ajánlat '
     'összeállításához használt árak és kapacitások ennyi ideig tarthatók. Ha több időre van '
     'szüksége, jelezze — jellemzően meg tudjuk hosszabbítani.'),
    ('Mennyi a jótállás?',
     'Fogyasztóként <strong>3 év</strong> a berendezésre és annak elektronikai részére, a '
     'műanyag tartályra pedig <strong>15 év</strong> kiterjesztett jótállás. A 15 év feltétele, '
     'hogy a kiszállítást, a szakszerű beszerelést és az éves karbantartást is mi végezzük — '
     'ellenkező esetben a tartályra is 3 év vonatkozik.'),
    ('A baktériumkultúrára is jár jótállás?',
     'Nem. A baktériumkultúra állapotát érdemben befolyásolja, hogy milyen anyagok kerülnek a '
     'rendszerbe — ez a használat során a Megrendelő ellenőrzése alatt áll. Az '
     '<a href="megoldasok/biologiai-uzemeltetes-es-karbantartas">üzemeltetési oldalon</a> '
     'részletesen leírjuk, mit nem szabad a rendszerbe engedni.'),
]

GYIK_VALLALKOZAS = [
    ('Miért más ez a szerződés, mint a fogyasztói?',
     'Mert a fogyasztóra kötelező szabályok — 14 napos elállási jog, kötelező jótállás, '
     'termékszavatosság, békéltető testület — a vállalkozásokra nem vonatkoznak. Ami ezen a '
     'lapon áll, az a felek megállapodása.'),
    ('Mennyi a jótállás vállalkozásként?',
     '<strong>1 év</strong> a berendezésre és annak elektronikai részére, a műanyag tartályra '
     'pedig összesen <strong>15 év</strong> kiterjesztett jótállás. A 15 év feltétele, hogy a '
     'kiszállítást, a szakszerű beszerelést és az éves karbantartást is mi végezzük — ellenkező '
     'esetben a tartályra is 1 év vonatkozik.'),
    ('Melyik szerződés vonatkozik egyéni vállalkozóra?',
     'Ez, ha a megrendelés a szakmája, önálló foglalkozása vagy üzleti tevékenysége körébe '
     'esik. Ha magánszemélyként, ettől függetlenül rendel, a '
     '<a href="aszf">fogyasztói ÁSZF</a> az irányadó.'),
]


def webpage_sema(html, o, nap_iso):
    """A jogi lap sémája eddig csak morzsát és GYIK-et adott.

    A `WebPage` csomópont mondja meg, MI ez a lap, KI adja ki és MIKORTÓL
    hatályos — ez az, amit egy nyelvi modellnek tudnia kell, ha valaki a
    jótállásról vagy az elállási jogról kérdez.
    """
    csomopont = json.dumps({
        '@type': 'WebPage',
        'name': o['h1'],
        'description': o['desc'],
        'url': f"{G.DOMAIN.rstrip('/')}/{o['url']}",
        'inLanguage': 'hu-HU',
        'datePublished': nap_iso,
        'dateModified': nap_iso,
        'publisher': {'@type': 'Organization', 'name': 'ÖkoTech-Home Kft.',
                      'url': G.DOMAIN.rstrip('/') + '/'},
    }, ensure_ascii=False, indent=6)
    return html.replace('"@graph": [\n', '"@graph": [\n    ' + csomopont + ',\n', 1)

FOGYASZTO = FORRAS / '2026-09-18_ASZF_fogyasztok.docx'
VALLALKOZAS = FORRAS / '2026-09-18_ASZF_fogyasztonak_nem_minosulo.docx'
NAP, NAP_ISO = hatalyos(FOGYASZTO)

OLDALAK = [
    dict(file='aszf.html', url='aszf', img='aszf',
         title='ÁSZF — Általános Szerződési Feltételek | ÖkoTech Home',
         desc='A fogyasztókra vonatkozó szerződési feltételek: megrendelés, teljesítés, '
              'fizetés, 14 napos elállási jog, jótállás és szavatosság, panaszkezelés.',
         h1='Általános Szerződési Feltételek',
         alt='Aláírásra előkészített szerződés és toll egy asztalon',
         lead='Fogyasztók részére. Ha cégként vagy intézményként rendel, a vállalkozásoknak '
              'szóló változat vonatkozik Önre.',
         crumbs=[HOME],
         sections=[valaszto('aszf-vallalkozasoknak', 'ÁSZF vállalkozásoknak',
                            'magánszemélyként, a szakmáján és önálló foglalkozásán kívül eső '
                            'célból rendel.', NAP)]
                  + epit(FOGYASZTO)
                  + [sec_faq(GYIK_FOGYASZTO),
                     letoltes('okotechhome-aszf.pdf', 'ÁSZF fogyasztóknak')]),

    dict(file='aszf-vallalkozasoknak.html', url='aszf-vallalkozasoknak', img='dokumentumok',
         title='ÁSZF vállalkozásoknak | ÖkoTech Home',
         desc='A fogyasztónak nem minősülő vásárlókra — cégekre, intézményekre — vonatkozó '
              'szerződési feltételek: teljesítés, fizetés, felelősség és jótállás.',
         h1='ÁSZF vállalkozásoknak',
         alt='Céges dokumentumok és bélyegző egy íróasztalon',
         lead='Fogyasztónak nem minősülő vásárlók részére. Magánszemélyként a fogyasztói '
              'változat vonatkozik Önre.',
         crumbs=[HOME],
         sections=[valaszto('aszf', 'fogyasztóknak szóló ÁSZF',
                            'cégként, intézményként vagy egyéni vállalkozóként, a szakmája '
                            'körében rendel.', NAP)]
                  + epit(VALLALKOZAS)
                  + [sec_faq(GYIK_VALLALKOZAS),
                     letoltes('okotechhome-aszf-vallalkozasoknak.pdf', 'ÁSZF vállalkozásoknak')]),
]


def main():
    for o in OLDALAK:
        html = G.build(o)
        html = html.replace(G.HEADER, HEADER)
        html = re.sub(r'(href|src|imagesrcset|srcset)="\.\./', r'\1="', html)
        html = html.replace('../assets/', 'assets/')
        html = keret_szinkron(html)
        html = webpage_sema(html, o, NAP_ISO)
        out = WEB / o['file']
        out.write_text(html, encoding='utf-8')
        szo = len(re.sub(r'<[^>]+>', ' ', html).split())
        print(f"  {o['file']:32s} {out.stat().st_size // 1024:>3} KB · {szo} szó")


if __name__ == '__main__':
    main()
