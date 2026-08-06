#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""13–15. szekció: Egy kézben · Szakértői továbblépés · Döntést támogató GYIK.

A szöveg a végleges szövegdokumentumból való, szó szerint.

JOGI JELÖLÉS: a dokumentum egyik GYIK-kérdésénél az ügyfél maga jelezte, hogy
„[Jogi ellenőrzés szükséges a végleges megfogalmazás előtt.]" — ez a rákötési
kötelezettségről és a talajterhelési díjról szóló kérdés. Az ilyen állítás
jogszabály-értelmezés; ha tévesen jelenik meg, az a látogatót téves döntéshez
vezetheti, a céget pedig felelősségre. Ezért a kérdés NEM kerül ki az oldalra,
csak a helye van megjelölve — a szöveg a generátorban megvan, egy sor
átbillentéssel publikálható, amint a jogi jóváhagyás megvan.
"""
import pathlib, re, sys, html as _h
sys.path.insert(0, str(pathlib.Path(__file__).parent))

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'
esc = lambda s: _h.escape(s, quote=False)

# ------------------------------------------------------------------ 13.
LEPESEK = [
    ('nav-felmeres', 'Projektadatok és telekadottságok',
     ['csőkivezetés, lejtés', 'talaj és talajvíz', 'elszivárogtatás',
      'gépi hozzáférés a telken'],
     'milyen kialakítás jöhet szóba az adott ingatlanon.'),
    ('nav-terheles', 'Méretezés és technológia',
     ['állandó lakóház vagy nyaraló', 'meglévő emésztő kiváltása',
      'nagyobb terhelésű ingatlan'],
     'az A.B. Clear biológiai szennyvíztisztító, az Epureco oldómedence vagy egy nagyobb '
     'kapacitású rendszer illik-e a helyzethez.'),
    ('nav-engedely', 'Dokumentáció és engedélyezési háttér',
     ['EN 12566-3 szerinti minősítés', 'műszaki adatok és helyszínrajz',
      'a kezelt víz elhelyezése', 'hatósági kérdések'],
     'milyen dokumentációval és milyen eljárással érdemes továbbmenni.'),
    ('nav-telepites', 'Gyártás és telepítés',
     ['magyarországi gyártás', 'saját fejlesztésű rendszerek',
      'telepítési tapasztalat csatorna nélküli ingatlanokon'],
     'hogyan lesz a tervből működő berendezés.'),
    ('nav-inditas', 'Beüzemelés és használat',
     ['átadás és működési tudnivalók', 'tisztítószerek',
      'az iszapzsák kezelése', 'szaghatás, kompresszor'],
     'mit kell tudnia a tulajdonosnak a mindennapi használatról.'),
    ('nav-szerviz', 'Karbantartás, szerviz és hosszú távú támogatás',
     ['rendszeres ellenőrzés', 'membráncsere, kompresszor', 'iszapzsák',
      'dokumentáció és karbantartási emlékeztető', 'hibajelzés és szervizháttér'],
     'hogyan marad a rendszer hosszú távon üzembiztos.'),
]

# ------------------------------------------------------------------ 14.
TISZTAZ = [
    ('Műszaki irány',
     'reális-e az adott helyzetben a biológiai szennyvíztisztító, az oldómedence vagy más '
     'kialakítás. Azt is megmondjuk, ha az Ön ingatlanán nem a mi rendszerünk a megfelelő '
     'megoldás.'),
    ('Tisztázandó pontok',
     'mely telekadatok, engedélyezési kérdések vagy helyszíni adottságok befolyásolják a döntést.'),
    ('Következő lépés',
     'elég-e további adatot bekérni, szükséges-e helyszíni felmérés, vagy már előkészíthető '
     'az ajánlat.'),
]
UTANA = [
    'Elküldi az alapadatokat: a telek, a használat, a meglévő rendszer és az elérhető '
    'dokumentumok adatait.',
    'Átnézzük, mi tisztázható előzetesen: a műszaki irányt, a hiányzó adatokat, az '
    'engedélyezési kérdéseket.',
    'Egyeztetünk a következő lépésről: további adatbekérés, helyszíni felmérés vagy '
    'ajánlat-előkészítés.',
    'Ajánlatot csak tisztázott adatok alapján készítünk. Automatikus értékesítési folyamat '
    'nem indul.',
]

# ------------------------------------------------------------------ 15.
# (csoport, kérdés, válasz, hivatkozás-felirat, hivatkozás-cél, jogi_jóváhagyás_kell)
GYIK = [
 ('Engedélyezés és telekalkalmasság', 'Kell engedély a házi szennyvíztisztító telepítéséhez?',
  'Az engedélyezés menete településenként eltérhet. Van, ahol egyszerűbb bejelentés elegendő, '
  'máshol részletesebb vízjogi vagy hatósági eljárás szükséges. Az első lépés mindig ugyanaz: '
  'tisztázni kell a helyi előírásokat, a kezelt víz elhelyezését és a telek adottságait.',
  'Az engedélyezés menete', 'tudastar/engedelyezes-es-megfeleloseg', False),
 ('Engedélyezés és telekalkalmasság', 'Mitől függ, hogy telepíthető-e szennyvíztisztító az adott telken?',
  'Elsősorban a kezelt víz elhelyezésétől, a talaj szikkasztóképességétől, a talajvízszinttől, '
  'a csőkivezetés mélységétől és a helyi előírásoktól. Nem elég azt tudni, van-e hely a '
  'tartálynak. Azt is látni kell, hová kerül a víz.',
  'Telek-alkalmassági ellenőrzés', 'projekt-elokeszites/telekalkalmassag', False),
 ('Engedélyezés és telekalkalmasság', 'Magas talajvíznél is telepíthető biológiai szennyvíztisztító?',
  'A magas talajvíz nem feltétlenül kizáró ok, de külön műszaki kialakítást igényelhet. Ilyenkor '
  'a tartály védelmét és a kezelt víz elhelyezését külön kell megtervezni.',
  'Magas talajvíz és betonmedencés telepítés', 'tudastar/telek-talaj-es-viz', False),
 ('Engedélyezés és telekalkalmasság', 'Hová kerül a tisztított víz?',
  'Jellemzően telken belüli elszivárogtatással vagy gyökérzónás hasznosítással kerül vissza a '
  'környezetbe. A feltételeket a talaj, a talajvíz, a helyi előírások és a választott technológia '
  'együtt határozzák meg.',
  'A tisztított víz elszivárogtatása', 'projekt-elokeszites/tisztitott-viz-elhelyezese', False),
 ('Engedélyezés és telekalkalmasság',
  'Van csatorna az utcánkban. Választhatok mégis egyedi szennyvízkezelést?',
  'A műszakilag elérhető közcsatornára főszabály szerint rákötési kötelezettség áll fenn. '
  'A jogszabály ismer kivételt hatályos vízjogi üzemeltetési engedéllyel üzemeltetett egyedi '
  'szennyvízkezelő létesítmény esetén, ilyenkor viszont talajterhelési díjjal is számolni kell. '
  'Ez egyedi mérlegelést kíván, ezért érdemes a helyi előírások tisztázásával kezdeni.',
  'Vonatkozó jogszabályok', 'tudastar/engedelyezes-es-megfeleloseg', True),

 ('Technológia és használat',
  'Mi a különbség a zárt tároló, az oldómedence és a biológiai szennyvíztisztító között?',
  'A zárt tároló gyűjti a szennyvizet, ezért rendszeres szippantást igényel. Az oldómedence '
  'ülepít és részlegesen kezel. A biológiai szennyvíztisztító ténylegesen biológiai tisztítást '
  'végez, amelynek végén tisztított víz távozik.',
  'A technológiák összehasonlítása', 'megoldasok/', False),
 ('Technológia és használat', 'Nyaralóhoz vagy időszakos használathoz jó a biológiai szennyvíztisztító?',
  'Nem minden esetben. A baktériumkultúra rendszeres terhelés mellett működik a legjobban. '
  'Időszakos használatnál külön kell vizsgálni, hogy a biológiai szennyvíztisztító, az '
  'oldómedence vagy más megoldás illik-e az ingatlanhoz.',
  'Időszakos használat és technológiaválasztás',
  'helyzetem/nyaralo-vagy-szezonalisan-hasznalt-ingatlan', False),
 ('Technológia és használat',
  'Mi történik a régi emésztővel, ha biológiai szennyvíztisztítóra váltunk?',
  'A meglévő emésztőt szakszerűen kell kezelni: kiürítés, megszüntetés, betömedékelés vagy más '
  'funkcióra alakítás merülhet fel. Ezt a telepítés előtt kell tisztázni, mert a régi rendszer '
  'helye és állapota a kivitelezést is befolyásolja.',
  'Emésztő kiváltása', 'helyzetem/meglevo-emesztot-szeretnek-kivaltani', False),

 ('Üzemeltetés', 'Kell szippantani az A.B. Clear biológiai szennyvíztisztítót?',
  'Nem. Az iszapzsákos technológia miatt a rendszer nem igényel rendszeres szippantást. '
  'A tisztítás során keletkező fölösiszap zsákban gyűlik, víztelenített formában kivehető, '
  'majd komposztálható.',
  'Az iszapzsákos technológia', 'megoldasok/biologiai-szennyviztisztitas', False),
 ('Üzemeltetés', 'Van szaga a biológiai szennyvíztisztítónak?',
  'Megfelelő működés mellett nincs szaghatás. A biológiai tisztítás levegőztetett folyamat, '
  'nem rothasztásra épül. Az erős szag jellemzően hibára, túlterhelésre vagy karbantartási '
  'problémára utal.',
  'Szaghatás és karbantartás', 'tudastar/uzemeltetes-es-hibamegelozes', False),
 ('Üzemeltetés', 'Kell baktériumot, tablettát vagy adalékanyagot adagolni?',
  'Az A.B. Clear rendszerben a baktériumkultúra önfenntartó, a beérkező szennyvíz táplálja. '
  'Normál használat mellett nincs szükség baktériumtablettára, porra vagy más adalékanyagra.',
  'Mit szabad és mit nem szabad a rendszerbe juttatni?',
  'tudastar/uzemeltetes-es-hibamegelozes', False),
 ('Üzemeltetés', 'Miből áll az éves üzemeltetési költség?',
  'A technológiától függ. Zárt tárolónál a fő tétel a szippantás. Biológiai rendszereknél '
  'áramfogyasztás, alkatrészcsere, karbantartás és iszapkezelés merülhet fel. Az A.B. Clear '
  'esetében nincs rendszeres szippantás és nincs adalékanyag, ezért az éves költség jobban '
  'tervezhető.',
  'Üzemeltetés és hosszú távú költség', '#uzemeltetes-cim', False),

 ('Ár és ajánlat', 'Miért nem adható pontos ár telefonon vagy néhány adat alapján?',
  'A végleges ár nem csak a berendezéstől függ. Számít a kapacitás, a földmunka, a telek '
  'hozzáférhetősége, a csőkivezetés mélysége, a talajvíz, a kezelt víz elhelyezése, és az is, '
  'ki végzi a telepítést. Pontos ajánlatot ezért csak az ingatlan adatainak ismeretében lehet adni.',
  'Előzetes ársáv kalkulátor', '#ai-dontestamogato', False),
 ('Ár és ajánlat', 'Mire érdemes figyelni, ha már van ajánlatom?',
  'Ellenőrizze, mire terjed ki az ajánlat: csak a berendezésre, vagy tartalmazza a telepítést, '
  'a földmunkát, a kezelt víz elhelyezését, az engedélyezési dokumentációt, a beüzemelést és a '
  'szervizhátteret is. A hiányzó tételek később külön költségként jelenhetnek meg.',
  'Ajánlat-ellenőrző', '#ajanlat-osszehasonlito', False),

 ('Következő lépés', 'Kell helyszíni felmérés az első egyeztetéshez?',
  'Nem feltétlenül. Sok esetben a telek alapadataiból, a használat módjából, a meglévő '
  'rendszerből és a rendelkezésre álló rajzokból már látszik, milyen irányba érdemes '
  'továbbmenni. Helyszíni felmérésre akkor van szükség, ha a műszaki vagy engedélyezési '
  'kérdések ezt indokolják.',
  'Előzetes szakmai egyeztetés', 'kapcsolat', False),
]


def epit():
    sin = '\n'.join(f'''          <li class="folyamat-lepes">
            <button type="button" class="folyamat-gomb" data-folyamat="{i}"
                    aria-expanded="{'true' if i == 1 else 'false'}" aria-controls="lepes-{i}">
              <span class="type-data-value folyamat-szam">{i:02d}</span>
              <span class="folyamat-korong" aria-hidden="true">
                <span class="icon icon-inline icon-badge-size icon-{ik}"></span>
              </span>
              <span class="type-ui-subtitle folyamat-cimke">{esc(cim)}</span>
            </button>
          </li>''' for i, (ik, cim, _, _) in enumerate(LEPESEK, 1))

    panelek = '\n'.join(f'''        <div class="folyamat-panel" id="lepes-{i}" data-folyamat-panel="{i}"{'' if i == 1 else ' hidden'}>
          <h3 class="type-display-highlight-title folyamat-cim">
            <span class="folyamat-cim-szam">{i:02d}</span> · {esc(cim)}
          </h3>
          <ul class="folyamat-lista" role="list">
{chr(10).join(f'            <li class="type-ui-body">{esc(x)}</li>' for x in tetelek)}
          </ul>
          <p class="folyamat-dol">
            <strong class="type-ui-card-title">Itt dől el:</strong>
            <span class="type-ui-body">{esc(dol)}</span>
          </p>
        </div>''' for i, (_, cim, tetelek, dol) in enumerate(LEPESEK, 1))

    tisztaz = '\n'.join(f'''          <li class="type-ui-body"><span class="fit-mark fit-yes" aria-hidden="true"></span>'''
                        f'''<span class="fit-text"><strong>{esc(c)}</strong> — {esc(t)}</span></li>'''
                        for c, t in TISZTAZ)

    utana = '\n'.join(f'''        <li class="card">
          <span class="card-badge type-data-value" aria-hidden="true">{i}</span>
          <p class="type-ui-body card-text">{esc(t)}</p>
        </li>''' for i, t in enumerate(UTANA, 1))

    # --- GYIK csoportonként ---
    csoportok, sorrend = {}, []
    for cs, k, v, cimke, cel, jogi in GYIK:
        if cs not in csoportok:
            csoportok[cs] = []; sorrend.append(cs)
        csoportok[cs].append((k, v, cimke, cel, jogi))

    gyik = ''
    for cs in sorrend:
        tetelek = ''
        for k, v, cimke, cel, jogi in csoportok[cs]:
            if jogi:
                tetelek += (f'\n        <!-- JOGI JÓVÁHAGYÁSRA VÁR — NEM PUBLIKÁLHATÓ:\n'
                            f'             „{k}"\n'
                            f'             A szövegforrás maga jelöli: „[Jogi ellenőrzés szükséges a\n'
                            f'             végleges megfogalmazás előtt.]" A válasz a rákötési\n'
                            f'             kötelezettséget és a talajterhelési díjat értelmezi —\n'
                            f'             jogszabály-értelmezés, téves megfogalmazás esetén a\n'
                            f'             látogatót téves döntéshez vezetheti. A kész szöveg a\n'
                            f'             scripts/oldalgyartas/szekcio13_15.py fájlban áll; a\n'
                            f'             GYIK-sorban a `True` `False`-ra váltásával publikálható,\n'
                            f'             amint a jogi jóváhagyás megvan. -->\n')
                continue
            tetelek += f'''        <details class="faq-item">
          <summary class="faq-q type-ui-card-title">{esc(k)}</summary>
          <div class="faq-a">
            <p class="type-ui-body">{esc(v)}</p>
            <p class="faq-tovabb"><a class="text-link" href="{cel}"><span class="link-label">{esc(cimke)}<span class="action-arrow-end" aria-hidden="true">&rarr;</span></span></a></p>
          </div>
        </details>
'''
        gyik += f'''
      <div class="gyik-csoport">
        <h3 class="type-ui-card-title gyik-csoport-cim">{esc(cs)}</h3>
        <div class="faq">
{tetelek}        </div>
      </div>
'''

    return f'''
  <!-- ==========================================================================
       13. SZEKCIÓ — EGY KÉZBEN
  =========================================================================== -->
  <section class="section" aria-labelledby="egykezben-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Szolgáltatási folyamat</p>
        <h2 class="type-display-section-title section-title" id="egykezben-cim">
          Felmérés. Dokumentáció. Telepítés. Karbantartás.
        </h2>
        <p class="type-ui-body section-lead">
          Nem csak berendezést szállítunk. A döntéshez szükséges telekadatokat, a műszaki
          dokumentációt, a gyártást, a telepítést és az üzemeltetési hátteret is ugyanahhoz
          a rendszerhez kapcsoljuk.
        </p>
      </header>
      <!-- A lépéssor JS NÉLKÜL is teljes: a `hidden` attribútumot a szkript
           teszi a panelekre, tehát mind a hat lépés olvasható marad. -->
      <div class="folyamat" data-folyamat-doboz>
        <ol class="folyamat-sin" role="list">
{sin}
        </ol>
        <div class="folyamat-panelek">
{panelek}
        </div>
      </div>
    </div>
  </section>

  <!-- ==========================================================================
       14. SZEKCIÓ — SZAKÉRTŐI TOVÁBBLÉPÉS
  =========================================================================== -->
  <section class="section" aria-labelledby="konzultacio-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Előzetes konzultáció</p>
        <h2 class="type-display-section-title section-title" id="konzultacio-cim">
          Az első egyeztetés elköteleződés nélkül zajlik — a célja, hogy Ön tisztábban lásson
        </h2>
        <p class="type-ui-body section-lead">
          Az első beszélgetés nem értékesítés és nem helyszíni felmérés. Az induló irányt
          tisztázzuk. A végére három dolognak kell látszania:
        </p>
      </header>

      <div class="split">
        <div class="split-col">
          <ul class="fit-list" role="list">
{tisztaz}
          </ul>

          <p class="konz-akcio">
            <a class="btn btn-primary" href="kapcsolat">Előzetes egyeztetést kérek</a>
          </p>
          <p class="type-ui-subtitle konz-tel">
            <a href="tel:+3633200211">+36 33 200 211</a> — 2004 óta ugyanezen a számon.
          </p>
          <p class="type-ui-caption konz-keznel">
            <strong>Hasznos, ha kéznél van:</strong> helyrajzi szám, helyszínrajz vagy tervrajz,
            a meglévő emésztő adatai, fotók a telekről, korábbi ajánlatok.
          </p>
        </div>

        <aside class="split-card konz-bemutat" aria-labelledby="konz-nev">
          <p class="type-ui-card-title konz-nev" id="konz-nev">Krasznói Anna</p>
          <p class="type-ui-subtitle konz-titulus">ügyvezető, társalapító · ÖkoTech-Home Kft.</p>
          <p class="type-ui-body konz-bio">
            Közgazdász, korábban banki kockázatkezelési vezető. A szennyvíztisztítást azóta is
            így nézi: beruházási, engedélyezési és üzemeltetési döntésként, nem csak műszaki
            kérdésként. A cég első berendezése a saját telkükre épült, ahová a szippantóautó
            sem jutott fel.
          </p>
          <!-- ADATHIÁNY: portréfotó Krasznói Annáról — ügyféltől kérendő. -->
        </aside>
      </div>

      <div class="konz-utana">
        <h3 class="type-ui-card-title konz-utana-cim">Mi történik a jelentkezés után?</h3>
        <ul class="numbered-grid" role="list">
{utana}
        </ul>
      </div>
    </div>
  </section>

  <!-- ==========================================================================
       15. SZEKCIÓ — DÖNTÉST TÁMOGATÓ GYIK
       A kérdések a végleges szövegdokumentumból valók. EGY kérdés jogi
       jóváhagyásra vár, azt a markup csak megjelöli — lásd lent.
  =========================================================================== -->
  <section class="section" aria-labelledby="gyik-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Gyakori kérdések</p>
        <h2 class="type-display-section-title section-title" id="gyik-cim">
          Gyakori kérdések egyedi szennyvízkezelésről, emésztő kiváltásáról és engedélyezésről
        </h2>
        <p class="type-ui-body section-lead">
          Rövid válaszok a döntés előtt leggyakrabban felmerülő kérdésekre. A részletes műszaki,
          engedélyezési és üzemeltetési háttér a kapcsolódó tudástáranyagokban érhető el.
        </p>
      </header>
{gyik}
    </div>
  </section>
'''


if __name__ == '__main__':
    import json
    p = WEB / 'index.html'
    s = p.read_text(encoding='utf-8')
    uj = epit()
    if 'egykezben-cim' in s:
        s = re.sub(r'\n  <!-- =+\n       13\. SZEKCIÓ.*?\n  </section>\n(?=\n</main>)', uj, s, flags=re.S)
    else:
        s = s.replace('\n</main>', uj + '\n</main>', 1)

    # FAQPage strukturált adat a MEGJELENÍTETT kérdésekből
    tetelek = [{"@type": "Question", "name": k,
                "acceptedAnswer": {"@type": "Answer", "text": v}}
               for _, k, v, _, _, jogi in GYIK if not jogi]
    ld = ('<script type="application/ld+json">\n'
          + json.dumps({"@context": "https://schema.org", "@type": "FAQPage",
                        "mainEntity": tetelek}, ensure_ascii=False, indent=2)
          + '\n</script>\n')
    s = re.sub(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>\n', '', s, flags=re.S)
    s = s.replace('</body>', ld + '</body>', 1)

    p.write_text(s, encoding='utf-8')
    print(f'index.html — 13–15. szekció beírva ({len(tetelek)} publikált GYIK, '
          f'{sum(1 for g in GYIK if g[5])} jogi jóváhagyásra vár)')
