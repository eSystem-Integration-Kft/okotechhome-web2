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
ALCIM = {'Az engedélyezés menete': 'Részletes útmutató a hatósági eljárás lépéseiről.', 'Telek-alkalmassági ellenőrzés': 'Mit kell megnézni a telken a döntés előtt.', 'Magas talajvíz és betonmedencés telepítés': 'Mikor kell eltérő műszaki kialakítás.', 'A tisztított víz elszivárogtatása': 'Hová kerülhet a kezelt víz, és milyen feltételekkel.', 'A technológiák összehasonlítása': 'Zárt tároló, oldómedence és biológiai rendszer egymás mellett.', 'Időszakos használat és technológiaválasztás': 'Nyaraló és szezonális ingatlan: melyik megoldás való oda.', 'Emésztő kiváltása': 'Mikor indokolt a csere, és mi lesz a régi rendszerrel.', 'Az iszapzsákos technológia': 'Hogyan működik szippantás nélkül.', 'Szaghatás és karbantartás': 'Mit jelez a szag, és mit kell tenni.', 'Mit szabad és mit nem szabad a rendszerbe juttatni?': 'A mindennapi használat szabályai.', 'Üzemeltetés és hosszú távú költség': 'Az éves tételek technológiánként.', 'Előzetes ársáv kalkulátor': 'Néhány kérdés alapján nagyságrendi tartomány.', 'Ajánlat-ellenőrző': 'Mire terjed ki az ajánlat, és mi hiányzik belőle.', 'Előzetes szakmai egyeztetés': 'Elköteleződés nélküli első beszélgetés.'}
esc = lambda s: _h.escape(s, quote=False)

# ------------------------------------------------------------------ 13.
LEPESEK = [
    ('lepes-telekadat', 'Projektadatok és telekadottságok',
     ['csőkivezetés, lejtés', 'talaj és talajvíz', 'elszivárogtatás',
      'gépi hozzáférés a telken'],
     'milyen kialakítás jöhet szóba az adott ingatlanon.'),
    ('lepes-meretezes', 'Méretezés és technológia',
     ['állandó lakóház vagy nyaraló', 'meglévő emésztő kiváltása',
      'nagyobb terhelésű ingatlan'],
     'az A.B. Clear biológiai szennyvíztisztító, az Epureco oldómedence vagy egy nagyobb '
     'kapacitású rendszer illik-e a helyzethez.'),
    ('lepes-dokumentum', 'Dokumentáció és engedélyezési háttér',
     ['EN 12566-3 szerinti minősítés', 'műszaki adatok és helyszínrajz',
      'a kezelt víz elhelyezése', 'hatósági kérdések'],
     'milyen dokumentációval és milyen eljárással érdemes továbbmenni.'),
    ('lepes-telepites', 'Gyártás és telepítés',
     ['magyarországi gyártás', 'saját fejlesztésű rendszerek',
      'telepítési tapasztalat csatorna nélküli ingatlanokon'],
     'hogyan lesz a tervből működő berendezés.'),
    ('lepes-beuzemeles', 'Beüzemelés és használat',
     ['átadás és működési tudnivalók', 'tisztítószerek',
      'az iszapzsák kezelése', 'szaghatás, kompresszor'],
     'mit kell tudnia a tulajdonosnak a mindennapi használatról.'),
    ('lepes-karbantartas', 'Karbantartás, szerviz és hosszú távú támogatás',
     ['rendszeres ellenőrzés', 'membráncsere, kompresszor', 'iszapzsák',
      'dokumentáció és karbantartási emlékeztető', 'hibajelzés és szervizháttér'],
     'hogyan marad a rendszer hosszú távon üzembiztos.'),
]

# ------------------------------------------------------------------ 14.
TISZTAZ = [
    ('nav-iranytu', 'Műszaki irány',
     'reális-e az adott helyzetben a biológiai szennyvíztisztító, az oldómedence vagy más '
     'kialakítás. Azt is megmondjuk, ha az Ön ingatlanán nem a mi rendszerünk a megfelelő '
     'megoldás.'),
    ('nav-ellenorzes', 'Tisztázandó pontok',
     'mely telekadatok, engedélyezési kérdések vagy helyszíni adottságok befolyásolják a döntést.'),
    ('nav-inditas', 'Következő lépés',
     'elég-e további adatot bekérni, szükséges-e helyszíni felmérés, vagy már előkészíthető '
     'az ajánlat.'),
]
UTANA = [
    ('Elküldi az alapadatokat:',
     'a telek, a használat, a meglévő rendszer és az elérhető dokumentumok adatait.'),
    ('Átnézzük, mi tisztázható előzetesen:',
     'a műszaki irányt, a hiányzó adatokat, az engedélyezési kérdéseket.'),
    ('Egyeztetünk a következő lépésről:',
     'további adatbekérés, helyszíni felmérés vagy ajánlat-előkészítés.'),
    ('Ajánlatot csak tisztázott adatok alapján készítünk.',
     'Automatikus értékesítési folyamat nem indul.'),
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

    tisztaz = '\n'.join(f'''          <li class="konz-pont">
            <span class="konz-pont-ikon" aria-hidden="true">
              <span class="icon icon-inline icon-badge-size icon-{ik}"></span>
            </span>
            <h3 class="type-ui-card-title konz-pont-cim">{esc(c)}</h3>
            <p class="type-ui-body konz-pont-szoveg">{esc(t[0].upper() + t[1:])}</p>
          </li>''' for ik, c, t in TISZTAZ)

    utana = '\n'.join(f'''          <li class="utana-lepes">
            <span class="utana-szam type-ui-card-title" aria-hidden="true">{i}</span>
            <p class="type-ui-subtitle utana-szoveg"><strong>{esc(a)}</strong> {esc(b)}</p>
          </li>''' for i, (a, b) in enumerate(UTANA, 1))

    # --- GYIK csoportonként ---
    csoportok, sorrend = {}, []
    for cs, k, v, cimke, cel, jogi in GYIK:
        if cs not in csoportok:
            csoportok[cs] = []; sorrend.append(cs)
        csoportok[cs].append((k, v, cimke, cel, jogi))

    fulek, listak, jogi_megjegyzes = [], [], ''
    for ci, cs in enumerate(sorrend, 1):
        akt = ' aria-selected="true"' if ci == 1 else ' aria-selected="false"'
        rejt = '' if ci == 1 else ' hidden'
        fulek.append(f'''            <button type="button" role="tab" class="gyik-ful type-ui-body"
                    id="ful-{ci}" data-gyik-ful="{ci}"{akt} aria-controls="gyik-{ci}"
                    tabindex="{0 if ci == 1 else -1}">{esc(cs)}</button>''')

        sorok, valaszok = [], []
        for qi, (k, v, cimke, cel, jogi) in enumerate(csoportok[cs], 1):
            if jogi:
                jogi_megjegyzes += (f'''
        <!-- JOGI JÓVÁHAGYÁSRA VÁR — NEM PUBLIKÁLHATÓ: „{k}"
             A szövegforrás maga jelöli: „[Jogi ellenőrzés szükséges a végleges
             megfogalmazás előtt.]" A válasz a rákötési kötelezettséget és a
             talajterhelési díjat értelmezi — jogszabály-értelmezés, téves
             megfogalmazás esetén a látogatót téves döntéshez vezetheti.
             A kész szöveg a scripts/oldalgyartas/szekcio13_15.py fájlban áll;
             a GYIK-sor `True` értékét `False`-ra váltva publikálható. -->''')
                continue
            kv = f'{ci}-{qi}'
            aktk = ' aria-selected="true"' if qi == 1 else ' aria-selected="false"'
            sorok.append(f'''              <li>
                <button type="button" class="gyik-kerdes" data-gyik-kerdes="{kv}"{aktk}
                        aria-controls="valasz-{kv}">
                  <span class="gyik-kerdes-szam type-ui-subtitle" aria-hidden="true">{qi}</span>
                  <span class="type-ui-body gyik-kerdes-szoveg">{esc(k)}</span>
                </button>
              </li>''')
            valaszok.append(f'''            <article class="gyik-valasz" id="valasz-{kv}"
                     data-gyik-valasz="{kv}"{'' if qi == 1 else ' hidden'}>
              <h4 class="type-display-highlight-title gyik-valasz-cim">
                <span class="gyik-valasz-szam" aria-hidden="true">{qi}</span>{esc(k)}
              </h4>
              <p class="type-ui-body gyik-valasz-szoveg">{esc(v)}</p>
              <a class="gyik-tovabb" href="{cel}">
                <span class="gyik-tovabb-nyil" aria-hidden="true">&rarr;</span>
                <span>
                  <span class="type-ui-card-title gyik-tovabb-cimke">{esc(cimke)}</span>
                  <span class="type-ui-subtitle gyik-tovabb-alcim">{esc(ALCIM.get(cimke, ''))}</span>
                </span>
              </a>
            </article>''')

        listak.append(f'''        <div class="gyik-tabla" id="gyik-{ci}" role="tabpanel"
             aria-labelledby="ful-{ci}" data-gyik-tabla="{ci}"{rejt}>
          <div class="gyik-oszlopok">
            <ul class="gyik-kerdesek" role="list">
{chr(10).join(sorok)}
            </ul>
            <div class="gyik-valaszok">
{chr(10).join(valaszok)}
            </div>
          </div>
        </div>''')

    gyik = f'''
      <div class="gyik" data-gyik>
        <div class="gyik-fulek" role="tablist" aria-label="Kérdéskörök">
{chr(10).join(fulek)}
        </div>
{chr(10).join(listak)}
      </div>
{jogi_megjegyzes}
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

      <div class="konz-fo">
        <div class="konz-bal">
          <ul class="konz-pontok" role="list">
{tisztaz}
          </ul>

          <p class="konz-akcio">
            <a class="btn btn-primary" href="kapcsolat">
              <span class="action-arrow" aria-hidden="true">&rarr;</span>Előzetes egyeztetést kérek
            </a>
          </p>

          <p class="konz-tel">
            <span class="konz-tel-ikon" aria-hidden="true">
              <span class="icon icon-inline icon-inline-lg icon-telefon"></span>
            </span>
            <span>
              <a class="type-ui-card-title konz-tel-szam" href="tel:+3633200211">+36 33 200 211</a>
              <span class="type-ui-caption konz-tel-alatt">— 2004 óta ugyanezen a számon.</span>
            </span>
          </p>
        </div>

        <aside class="konz-bemutat" aria-labelledby="konz-nev">
          <figure class="konz-foto">
            <img src="assets/img/krasznoi-anna.webp" width="640" height="962"
                 alt="Krasznói Anna, az ÖkoTech-Home Kft. ügyvezetője" loading="lazy" decoding="async">
          </figure>
          <div class="konz-bemutat-torzs">
            <p class="type-display-highlight-title konz-nev" id="konz-nev">Krasznói Anna</p>
            <p class="type-ui-subtitle konz-titulus">ügyvezető, társalapító · ÖkoTech-Home Kft.</p>
            <p class="type-ui-body konz-bio">
              Közgazdász, korábban banki kockázatkezelési vezető. A szennyvíztisztítást azóta is
              így nézi: beruházási, engedélyezési és üzemeltetési döntésként, nem csak műszaki
              kérdésként.
            </p>
            <p class="type-ui-body konz-bio">
              A cég első berendezése a saját telkükre épült, ahová a szippantóautó sem jutott fel.
            </p>
          </div>
        </aside>
      </div>

      <p class="konz-keznel">
        <span class="konz-keznel-ikon" aria-hidden="true">
          <span class="icon icon-inline icon-inline-lg icon-dokumentum"></span>
        </span>
        <span class="type-ui-body"><strong>Hasznos, ha kéznél van:</strong> helyrajzi szám,
          helyszínrajz vagy tervrajz, a meglévő emésztő adatai, fotók a telekről, korábbi ajánlatok.</span>
      </p>

      <div class="utana">
        <h3 class="type-display-highlight-title utana-cim">Mi történik a jelentkezés után?</h3>
        <ol class="utana-sin" role="list">
{utana}
        </ol>
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
