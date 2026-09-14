/* suti.js — süti-hozzájárulás: sáv, beállításkezelő, és a döntés kihirdetése.
   ---------------------------------------------------------------------------
   MIÉRT VAN EZ A FÁJL. A webhely Cookie-tájékoztatója NÉGY kategóriát ígér, és
   azt, hogy a nem szükséges sütik CSAK hozzájárulás után kerülnek elhelyezésre
   — a felület viszont eddig nem létezett. A tájékoztató ezt maga is jelezte
   („ADATHIÁNY: a süti-hozzájárulási felület … még nem került be"). Amíg nincs,
   a mérés és a beágyazott térkép nem kapcsolható be jogszerűen.

   EZ A MODUL NEM MÉR ÉS NEM ÁGYAZ BE SEMMIT. Egyetlen dolga: megkérdezni,
   eltárolni a választ, és KIHIRDETNI. Aki hozzájáruláshoz kötött dolgot akar
   csinálni (`meres.js`, a térkép), az erre a hirdetésre iratkozik fel. Így a
   hozzájárulás egy helyen dől el, és nem szóródik szét a modulok között.

        document.addEventListener('oth:suti', (e) => e.detail.statisztika && …);
        OthSuti.enged('terkep')      // pillanatnyi állapot lekérdezése
        OthSuti.nyit()               // a beállításkezelő megnyitása

   A DOM-OT IS EZ A FÁJL KÉSZÍTI, nem az oldalgyártó. Száznegyven lap sablonját
   nem akartuk megbontani egy olyan sávért, ami a lapok 99%-án egyszer látszik
   és eltűnik — és így az oldalgyártó szkriptek egyike sem tud véletlenül
   kimaradni belőle.

   TÁROLÁS: SÜTI, nem localStorage. A tájékoztató a „süti-beállítás megjegyzése"
   sort a MŰKÖDÉSHEZ SZÜKSÉGES kategóriába sorolja, 12 hónapos élettartammal —
   ezt a vállalást tartjuk. (A localStorage-nak nincs lejárata; a tizenkét
   hónapot csak a süti tudja magától betartani.)
*/
(() => {
  'use strict';

  const NEV     = 'oth-suti';
  /* A VERZIÓ EMELÉSE ÚJRA MEGKÉRDEZ MINDENKIT, és ez így helyes: a korábbi
     hozzájárulás a marketing célra nem terjed ki, tehát nem vihető át. */
  const VERZIO  = 2;
  const HONAP   = 12;
  /* MARKETING KATEGÓRIA — 2026-09-14. A Google Ads konverziómérés és a Meta
     Pixel EU-ban hozzájáruláshoz kötött, és ez NEM a statisztikai kategória:
     a látogató dönthet úgy, hogy a látogatottságmérést engedi, a hirdetési
     célú követést nem. A Consent Mode v2 is külön jelet vár rájuk
     (`ad_storage`, `ad_user_data`, `ad_personalization`). */
  const KATEGORIAK = ['beallitas', 'statisztika', 'marketing', 'terkep'];

  /* A kategóriák szövege EGY HELYEN. A tájékoztató táblázatával szó szerint
     egyeznie kell — ha ott változik a leírás, itt is változtatni kell. */
  const SZOVEG = {
    beallitas: {
      cim: 'Beállításokat megjegyző',
      mit: 'A választásai megjegyzése — például a világos vagy sötét megjelenítés.',
    },
    statisztika: {
      cim: 'Statisztikai',
      mit: 'A látogatottság mérése összesített formában: mely oldalak népszerűek, ' +
           'hol akadnak el a látogatók. Eszköz: Google Analytics 4.',
    },
    marketing: {
      cim: 'Hirdetési és remarketing',
      mit: 'A hirdetéseink eredményességének mérése, és hogy ne ugyanazt a ' +
           'hirdetést lássa újra és újra. Eszköz: Google Ads és Meta Pixel.',
    },
    terkep: {
      cim: 'Beágyazott térkép',
      mit: 'A Kapcsolat oldalon a Google Térkép beágyazása. A megjelenítéssel a ' +
           'Google sütiket helyezhet el és megkapja az Ön IP-címét.',
    },
  };

  /* ------------------------------------------------------------- tárolás */

  function olvas() {
    const m = document.cookie.match(new RegExp('(?:^|; )' + NEV + '=([^;]*)'));
    if (!m) return null;
    try {
      const a = JSON.parse(decodeURIComponent(m[1]));
      /* VERZIÓELLENŐRZÉS. Ha egyszer új kategória kerül a listába, a régi
         hozzájárulás nem terjedhet ki rá — akkor újra meg kell kérdezni. */
      if (!a || a.v !== VERZIO || typeof a.k !== 'object') return null;
      return a;
    } catch { return null; }
  }

  function ir(kapcsolok) {
    const a = { v: VERZIO, t: new Date().toISOString(), k: kapcsolok };
    const lejar = new Date();
    lejar.setMonth(lejar.getMonth() + HONAP);
    /* A `Secure` csak HTTPS-en érvényes; helyi fejlesztésen (http://localhost)
       a böngésző eldobná vele együtt az egész sütit. */
    const biztos = location.protocol === 'https:' ? '; Secure' : '';
    document.cookie = NEV + '=' + encodeURIComponent(JSON.stringify(a))
      + '; Path=/; Max-Age=' + (HONAP * 30 * 24 * 60 * 60)
      + '; Expires=' + lejar.toUTCString()
      + '; SameSite=Lax' + biztos;
    return a;
  }

  function allapot() {
    const a = olvas();
    const ki = { dontott: !!a, ideje: a ? a.t : null };
    for (const k of KATEGORIAK) ki[k] = !!(a && a.k[k]);
    return ki;
  }

  /* A KIHIRDETÉS. Minden érdeklődő modul ezt hallgatja — a `document`-en, mert
     az minden szkript számára elérhető, betöltési sorrendtől függetlenül. */
  function kihirdet() {
    const a = allapot();
    document.dispatchEvent(new CustomEvent('oth:suti', { detail: a }));
    /* A GTM NEM HALLGAT CustomEvent-re. A Meta Pixel a Consent Mode-ot nem
       kezeli, tehát a betöltését magának a triggernek kell a marketing
       hozzájáruláshoz kötnie — ahhoz viszont a dataLayerben kell látnia a
       döntést. Ezért ugyanaz az állapot ide is kimegy, esemény formájában. */
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'oth_suti_dontes',
      oth_suti_statisztika: a.statisztika ? 'granted' : 'denied',
      oth_suti_marketing:   a.marketing   ? 'granted' : 'denied',
      oth_suti_terkep:      a.terkep      ? 'granted' : 'denied',
    });
  }

  function ment(kapcsolok) {
    ir(kapcsolok);
    kihirdet();
    sav?.remove();
    sav = null;
  }

  /* ----------------------------------------------------------- segédek */

  function elem(tag, osztaly, szoveg) {
    const e = document.createElement(tag);
    if (osztaly) e.className = osztaly;
    if (szoveg != null) e.textContent = szoveg;
    return e;
  }

  const mind = (ertek) =>
    Object.fromEntries(KATEGORIAK.map((k) => [k, ertek]));

  /* -------------------------------------------------------------- a sáv */

  let sav = null;

  function savEpit() {
    if (sav) return;
    sav = elem('section', 'suti-sav');
    sav.setAttribute('role', 'region');
    sav.setAttribute('aria-label', 'Süti-hozzájárulás');

    const doboz = elem('div', 'suti-sav-doboz');
    /* A MÁRKAJEL. Dekoratív: a jelentést a mellette álló szöveg hordozza,
       ezért `aria-hidden` (designrendszer 8.). Saját flex-elem, nem háttér —
       vésetként a szöveg alá került és foltnak látszott. */
    const jel = elem('span', 'suti-jel');
    jel.setAttribute('aria-hidden', 'true');
    doboz.append(jel);
    const szov  = elem('div', 'suti-sav-szoveg');
    szov.append(elem('p', 'type-ui-body-strong', 'Sütiket használunk'));

    const p = elem('p', 'type-ui-body');
    /* RÖVIDEN, hogy két sor legyen és ne három. A sáv a lap alján ül, és
       minden sora takar valamit abból, amiért a látogató jött — a hosszú
       magyarázat itt nem udvariasság, hanem útban van. Ami jogilag kell, az
       benne maradt: mit teszünk hozzájárulás nélkül, mihez kérünk engedélyt,
       és hogy visszavonható. A „ugyanolyan egyszerűen" vállalást a
       Cookie-tájékoztató mondja ki, a láblécben lévő gomb pedig teljesíti. */
    p.append(document.createTextNode(
      'A működéshez szükségeseket mindig elhelyezzük; a méréshez és a beágyazott ' +
      'térképhez a hozzájárulását kérjük — bármikor visszavonhatja. Részletek a '));
    const hiv = elem('a', 'suti-sav-link', 'Cookie-tájékoztatóban');
    hiv.href = '/cookie-tajekoztato';
    p.append(hiv, document.createTextNode('.'));
    szov.append(p);

    const gombok = elem('div', 'suti-sav-gombok');

    const beallit = elem('button', 'btn btn-secondary type-ui-button', 'Beállítások');
    beallit.type = 'button';
    beallit.addEventListener('click', nyit);

    const csak = elem('button', 'btn btn-secondary type-ui-button', 'Csak a szükségeseket');
    csak.type = 'button';
    csak.addEventListener('click', () => ment(mind(false)));

    const mindet = elem('button', 'btn btn-primary type-ui-button', 'Elfogadom mindet');
    mindet.type = 'button';
    mindet.addEventListener('click', () => ment(mind(true)));

    /* A SORREND SZÁNDÉKOS: az elutasítás ugyanolyan elérhető, mint az
       elfogadás, és mindkettő EGY kattintás. A NAIH és az EDPB is ezt kéri —
       a „csak elfogadás egy gombbal" mintát kifogásolja. */
    gombok.append(beallit, csak, mindet);
    doboz.append(szov, gombok);
    sav.append(doboz);
    document.body.append(sav);
  }

  /* ------------------------------------------------- a beállításkezelő */

  let parbeszed = null;

  function parbeszedEpit() {
    if (parbeszed) return parbeszed;
    parbeszed = elem('dialog', 'suti-parbeszed');
    parbeszed.setAttribute('aria-labelledby', 'suti-parbeszed-cim');

    const urlap = elem('form', 'suti-parbeszed-urlap');
    urlap.method = 'dialog';

    const cim = elem('h2', 'suti-parbeszed-cim type-h4', 'Süti-beállítások');
    cim.id = 'suti-parbeszed-cim';
    /* Ugyanaz a jel, a címsor mellett. A bal alsó sarokban nem lehet: ott a
       gombsor áll, és az átlátszatlan. */
    const fej = elem('div', 'suti-parbeszed-fej');
    const jelP = elem('span', 'suti-jel');
    jelP.setAttribute('aria-hidden', 'true');
    fej.append(jelP, cim);
    urlap.append(fej);

    const bev = elem('p', 'type-ui-body',
      'Kategóriánként dönthet. A működéshez szükséges sütik nélkül a webhely nem ' +
      'használható, ezért azok nem kapcsolhatók ki.');
    urlap.append(bev);

    /* A szükséges kategória is LÁTSZIK, kikapcsolt jelölőnégyzettel — a
       tájékoztató felsorolja, tehát itt sem hallgathatjuk el. */
    const lista = elem('ul', 'suti-lista');
    lista.append(sorEpit('szukseges', {
      cim: 'Működéshez szükséges',
      mit: 'A webhely alapvető működése és a süti-beállítás megjegyzése. ' +
           'Ehhez nem kell hozzájárulás.',
    }, true, true));
    for (const k of KATEGORIAK) {
      lista.append(sorEpit(k, SZOVEG[k], false, false));
    }
    urlap.append(lista);

    const gombok = elem('div', 'suti-parbeszed-gombok');

    const elvet = elem('button', 'btn btn-secondary type-ui-button', 'Csak a szükségeseket');
    elvet.type = 'button';
    elvet.addEventListener('click', () => { ment(mind(false)); parbeszed.close(); });

    const osszes = elem('button', 'btn btn-secondary type-ui-button', 'Mindet elfogadom');
    osszes.type = 'button';
    osszes.addEventListener('click', () => { ment(mind(true)); parbeszed.close(); });

    const mentes = elem('button', 'btn btn-primary type-ui-button', 'Választásom mentése');
    mentes.type = 'button';
    mentes.addEventListener('click', () => {
      const k = {};
      for (const kat of KATEGORIAK) {
        k[kat] = parbeszed.querySelector('#suti-' + kat).checked;
      }
      ment(k);
      parbeszed.close();
    });

    gombok.append(elvet, osszes, mentes);
    urlap.append(gombok);
    parbeszed.append(urlap);
    document.body.append(parbeszed);
    return parbeszed;
  }

  function sorEpit(kulcs, szov, bekapcsolva, tiltva) {
    const li = elem('li', 'suti-sor');
    const cimke = elem('label', 'suti-sor-cimke');
    cimke.htmlFor = 'suti-' + kulcs;

    const jelolo = elem('input', 'suti-jelolo');
    jelolo.type = 'checkbox';
    jelolo.id = 'suti-' + kulcs;
    jelolo.checked = bekapcsolva;
    jelolo.disabled = tiltva;

    const szoveg = elem('span', 'suti-sor-szoveg');
    szoveg.append(elem('span', 'suti-sor-cim type-ui-body-strong', szov.cim));
    szoveg.append(elem('span', 'suti-sor-mit type-ui-caption', szov.mit));

    cimke.append(jelolo, szoveg);
    li.append(cimke);
    return li;
  }

  function nyit() {
    const d = parbeszedEpit();
    const a = allapot();
    for (const k of KATEGORIAK) {
      d.querySelector('#suti-' + k).checked = a[k];
    }
    if (typeof d.showModal === 'function') d.showModal();
    else d.setAttribute('open', '');           // ősrégi böngésző: legalább látszik
  }

  /* ------------------------------------------------------------- indítás */

  /* EGYETLEN KATEGÓRIA MEGADÁSA. A beágyazott térkép helyén álló gomb hívja:
     ott a látogató éppen azt a célt engedélyezi, amiért a gomb kiteszi magát,
     és ez a hozzájárulás ugyanúgy érvényes, mint a sávon adott. A többi
     kategóriát NEM piszkálja — aki a térképet kéri, azzal nem járult hozzá a
     méréshez is. A sáv ettől eltűnik: döntés született. */
  function megad(kulcs) {
    if (!KATEGORIAK.includes(kulcs)) return;
    const a = allapot();
    const k = {};
    for (const kat of KATEGORIAK) k[kat] = kat === kulcs ? true : a[kat];
    ment(k);
  }

  window.OthSuti = {
    allapot,
    enged: (k) => !!allapot()[k],
    megad,
    nyit,
  };

  function indul() {
    /* A tájékoztató lapján (és bárhol máshol) egy `data-suti` attribútummal
       ellátott gomb nyitja a beállításokat — ez a „visszavonás ugyanolyan
       egyszerű" vállalás gyakorlati megvalósítása. */
    document.addEventListener('click', (e) => {
      const g = e.target.closest('[data-suti]');
      if (!g) return;
      e.preventDefault();
      nyit();
    });

    /* A LÁBLÉC GOMBJA `hidden`-nel érkezik, és itt válik láthatóvá. Szkript
       nélkül a beállításkezelő sem létezik, tehát a gomb sem nyitna semmit —
       egy néma vezérlő pedig rosszabb, mint a hiánya. */
    for (const g of document.querySelectorAll('[data-suti][hidden]')) {
      g.hidden = false;
    }

    /* AKI MÁR DÖNTÖTT, annak nem tesszük ki újra. A hirdetés viszont ilyenkor
       is elmegy: a mérésnek és a térképnek tudnia kell, mit engedett korábban. */
    if (allapot().dontott) { kihirdet(); return; }
    savEpit();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', indul, { once: true });
  } else {
    indul();
  }
})();
