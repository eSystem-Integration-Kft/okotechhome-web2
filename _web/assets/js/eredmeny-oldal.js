/* ============================================================================
   ÖkoTech Home — eredmeny-oldal.js
   A megoldás-ajánló MENTETT eredményének megjelenítése azonosító alapján.
   ----------------------------------------------------------------------------
   A lap `/eredmeny?id=MA-XXXX-XXXX` alakban hívható. Az azonosítót a látogató
   a 6. szekció záró képernyőjén kapja, amikor elmenti az eredményt.

   MIÉRT NEM A CÍMSORBÓL RAJZOLUNK. A rekord a szerveren él, nem az URL-ben:
   így ugyanaz a link később is ugyanazt mutatja, telefonban bemondható, és a
   kinyomtatott/PDF példányon szereplő azonosítóval a kolléga is elő tudja
   venni pontosan azt, amit a látogató látott.

   IDEGEN ADAT — a szerver a saját tárolójából olvas, de a mezők eredetileg a
   kliensről érkeztek. Ezért minden mező `textContent`-tel kerül a lapra, soha
   `innerHTML`-lel: a tárolt szövegből nem lehet elem.
   ========================================================================== */
(() => {
  'use strict';

  const ALAK = /^MA-[A-Z2-9]{4}-[A-Z2-9]{4}$/;   /* az `ugy.js` ugyanezt ismeri */

  /* Az ellenőrzés az `ugy.js`-é. Ha az nem töltődött be, a régi alakvizsgálat
     marad — általános üzenettel, de nem töri el a lapot. */
  const ellenoriz = (nyers) => (window.OthUgy && window.OthUgy.ellenoriz)
    ? window.OthUgy.ellenoriz(nyers)
    : (ALAK.test(String(nyers || '').trim().toUpperCase())
      ? { ok: true, azon: String(nyers).trim().toUpperCase() }
      : { ok: false, uzenet: 'A helyes alak: MA-XXXX-XXXX — négy-négy betű vagy szám, kötőjellel elválasztva.' });

  const eszkoztar = document.querySelector('[data-er-eszkoztar]');
  const torzs     = document.querySelector('[data-er-torzs]');
  const uzenet    = document.querySelector('[data-er-uzenet]');
  const uzenetCim = document.querySelector('[data-er-uzenet-cim]');
  const uzenetSzo = document.querySelector('[data-er-uzenet-szoveg]');
  const kereso    = document.querySelector('[data-er-kereso]');
  const mezo      = document.getElementById('er-id');
  if (!torzs || !uzenet) return;

  const el = (tag, oszt, szoveg) => {
    const e = document.createElement(tag);
    if (oszt) e.className = oszt;
    if (szoveg != null) e.textContent = szoveg;
    return e;
  };

  const HONAP = ['január', 'február', 'március', 'április', 'május', 'június',
                 'július', 'augusztus', 'szeptember', 'október', 'november', 'december'];

  const datum = (iso) => {
    const d = new Date(iso);
    if (isNaN(d)) return '';
    return `${d.getFullYear()}. ${HONAP[d.getMonth()]} ${d.getDate()}.`;
  };

  /* -------------------------------------------------------------- ÜZENETEK */

  function allapot(cim, szoveg, keresoKell) {
    uzenetCim.textContent = cim;
    uzenetSzo.textContent = szoveg;
    if (kereso) kereso.hidden = !keresoKell;
    uzenet.hidden = false;
    torzs.hidden = true;
    if (eszkoztar) eszkoztar.hidden = true;
  }

  /* ------------------------------------------------------------ KIRAJZOLÁS */

  function blokk(cim) {
    const b = el('section', 'eredmeny-blokk');
    b.appendChild(el('h2', 'type-display-highlight-title eredmeny-blokk-cim', cim));
    return b;
  }

  function tetelLista(tetelek, leirassal) {
    const dl = el('dl', 'eredmeny-lista');
    tetelek.forEach((t) => {
      const sor = el('div', 'eredmeny-tetel');
      sor.appendChild(el('dt', 'type-ui-body-strong', t.cimke || ''));
      if (leirassal && t.szoveg) sor.appendChild(el('dd', 'type-ui-subtitle', t.szoveg));
      dl.appendChild(sor);
    });
    return dl;
  }

  /* A modulok megjelenítési neve. Zárt lista: ismeretlen kulcsot nem rajzolunk. */
  const MODUL_NEV = {
    ajanlo: 'Megoldás-ajánló',
    arsav: 'Előzetes ársáv'
  };
  const MODUL_SORREND = ['ajanlo', 'arsav'];

  function modulBlokk(kulcs, b) {
    const e = b.eredmeny || {};
    const szakasz = el('section', 'eredmeny-modul');

    const fej = el('header', 'eredmeny-modul-fej');
    fej.appendChild(el('p', 'type-data-eyebrow eredmeny-eyebrow', MODUL_NEV[kulcs]));
    fej.appendChild(el('h2', 'type-display-highlight-title eredmeny-blokk-cim',
      e.termekNev || e.cim || MODUL_NEV[kulcs]));
    if (b.mentve) fej.appendChild(el('p', 'type-ui-caption eredmeny-modul-datum', 'Mentve: ' + (datum(b.mentve) || '—')));
    szakasz.appendChild(fej);

    if (e.cim && e.termekNev) szakasz.appendChild(el('p', 'type-ui-body-strong eredmeny-modul-cim', e.cim));
    if (e.indoklas) szakasz.appendChild(el('p', 'type-ui-body', e.indoklas));
    if (e.kompromisszum) szakasz.appendChild(el('p', 'type-ui-body eredmeny-kompromisszum', e.kompromisszum));

    if (Array.isArray(e.okok) && e.okok.length) {
      /* A FEJLÉC A KIMENETTÍPUSTÓL FÜGG (hibalista H5) — a nyomtatott példány
         sem állíthat mást, mint a képernyő. A mentett rekord `okokCim` mezője
         hozza magával; régi rekordoknál marad a korábbi szöveg. */
      szakasz.appendChild(el('p', 'type-ui-body-strong eredmeny-okok-cim',
        e.okokCim || (kulcs === 'arsav'
          ? 'Tisztázandó pontok a válaszokból:'
          : 'Amit a válaszokból nem lehetett automatikusan eldönteni:')));
      const ul = el('ul', 'eredmeny-okok');
      e.okok.forEach((o) => ul.appendChild(el('li', 'type-ui-body', o.cimke || '')));
      szakasz.appendChild(ul);
    }

    const alszakasz = (cim, tetelek, leirassal) => {
      if (!Array.isArray(tetelek) || !tetelek.length) return;
      szakasz.appendChild(el('h3', 'type-ui-card-title eredmeny-alcim', cim));
      szakasz.appendChild(tetelLista(tetelek, leirassal));
    };
    alszakasz(kulcs === 'arsav' ? 'Mi mozgatja az árat' : 'Kivitelezési feltételek', e.feltetelek, true);
    alszakasz(kulcs === 'arsav' ? 'Amit érdemes előkészíteni' : 'Tisztázandók', e.tisztazandok, true);
    alszakasz('A megadott válaszok', b.valaszok, true);

    return szakasz;
  }

  function rajzol(ugy) {
    torzs.replaceChildren();
    const modulok = ugy.modulok || {};
    const megvan = MODUL_SORREND.filter((k) => modulok[k]);

    /* FEJLÉC — az azonosító és a teljes cím LÁTHATÓ szövegként is szerepel,
       nem csak hivatkozásként: a kinyomtatott vagy PDF-be mentett lapon a
       kattintható link semmit nem ér, a beírható cím viszont igen. */
    const fej = el('header', 'eredmeny-fej');
    fej.appendChild(el('p', 'type-data-eyebrow eredmeny-eyebrow', 'ÖkoTech Home · mentett eredmény'));
    fej.appendChild(el('h1', 'type-display-page-title eredmeny-cim',
      megvan.length > 1 ? 'A megadott helyzet és az előzetes ársáv'
                        : (MODUL_NEV[megvan[0]] || 'Mentett eredmény')));

    const meta = el('dl', 'eredmeny-meta');
    const metaSor = (cimke, ertek) => {
      const d = el('div', 'eredmeny-meta-sor');
      d.appendChild(el('dt', 'type-ui-caption', cimke));
      d.appendChild(el('dd', 'type-data-value', ertek));
      meta.appendChild(d);
    };
    metaSor('Azonosító', ugy.azonosito || '—');
    metaSor('Utoljára mentve', datum(ugy.frissitve || ugy.letrehozva) || '—');
    metaSor('Visszakereshető', location.origin + location.pathname + '?id=' + (ugy.azonosito || ''));
    fej.appendChild(meta);
    /* MI EZ AZ AZONOSÍTÓ. Aki hivatkozásra érkezik ide, nem tudja, miért van
       kódja — és a kód önmagában riasztó lehet. Egy mondat elveszi az élét. */
    fej.appendChild(el('p', 'type-ui-caption eredmeny-mi-ez',
      'Az azonosító nem regisztráció: nevet, e-mail-címet vagy telefonszámot nem kértünk hozzá, '
      + 'és nem tudjuk, ki Ön. Csak annyit tesz, hogy megjegyzi, mit adott meg — így bármikor '
      + 'előveheti, kinyomtathatja, és a további eszközeink nem kérdezik újra ugyanazt.'));

    /* Ha csak az egyik modul futott le, mondjuk ki — a hiányt nem elhallgatni
       kell, hanem felkínálni a folytatást. */
    if (megvan.length === 1) {
      const hianyzik = MODUL_SORREND.find((k) => !modulok[k]);
      const p2 = el('p', 'type-ui-body eredmeny-hiany');
      p2.appendChild(document.createTextNode(
        hianyzik === 'arsav'
          ? 'Ehhez az ügyhöz még nem tartozik ársávbecslés. '
          : 'Ehhez az ügyhöz még nem tartozik megoldás-ajánlás. '));
      const a = el('a', 'text-link');
      a.href = './#' + (hianyzik === 'arsav' ? 'ai-dontestamogato' : 'megoldas-ajanlo');
      const b = el('span', 'link-label', hianyzik === 'arsav' ? 'Ársávbecslő indítása' : 'Megoldás-ajánló indítása');
      b.appendChild(el('span', 'action-arrow-end', '→')).setAttribute('aria-hidden', 'true');
      a.appendChild(b);
      p2.appendChild(a);
      fej.appendChild(p2);
    }
    torzs.appendChild(fej);

    megvan.forEach((k) => torzs.appendChild(modulBlokk(k, modulok[k])));

    torzs.appendChild(el('p', 'type-ui-caption eredmeny-zaro',
      'Az eredmény tájékoztató jellegű, és nem helyettesíti a helyszíni felmérést. '
      + 'A mentett példány azt mutatja, amit a modulok a mentés pillanatában mondtak; '
      + 'a végleges megoldást és az árat szakértői egyeztetés után határozzuk meg.'));

    /* ELÉRHETŐSÉG (hibalista H10). A lap eddig azonosítót, dátumot, URL-t,
       javaslatot, tisztázandókat és a megadott válaszokat tartalmazta — de
       nem volt rajta telefonszám, e-mail és cégnév. Aki kinyomtatja vagy
       elküldi a párjának, annál pont ez hiányzik.

       Ez NEM sérti az adatgyűjtés-mentességet (spec 7.): itt MI adunk adatot,
       nem kérünk. A `tel:` és `mailto:` hivatkozás képernyőn működik, a
       nyomtatott lapon pedig a látható szöveg marad olvasható. */
    const lab = el('footer', 'eredmeny-elerhetoseg');
    lab.appendChild(el('span', 'type-ui-caption eredmeny-elerhetoseg-nev',
      'ÖkoTech-Home Kft. · 2509 Esztergom, Strázsa u. 12.'));
    const tel = el('a', 'type-ui-caption', '+36 33 200 211');
    tel.href = 'tel:+3633200211';
    lab.appendChild(tel);
    const lev = el('a', 'type-ui-caption', 'kapcsolat@okotechhome.hu');
    lev.href = 'mailto:kapcsolat@okotechhome.hu';
    lab.appendChild(lev);
    lab.appendChild(el('span', 'type-ui-caption', 'okotechhome.hu'));
    torzs.appendChild(lab);

    torzs.hidden = false;
    uzenet.hidden = true;
    if (eszkoztar) eszkoztar.hidden = false;
  }

  /* ------------------------------------------------------------- LEKÉRÉS */

  async function betolt(id) {
    allapot('Mentett eredmény betöltése…',
            'Egy pillanat, előkeressük a megadott azonosítóhoz tartozó eredményt.', false);
    if (!window.OthUgy) {
      allapot('A mentett eredményt most nem érjük el',
              'A lap egy összetevője nem töltődött be. Kérjük, frissítse az oldalt.', true);
      return;
    }
    const valasz = await window.OthUgy.olvas(id);
    if (!valasz.ok) {
      allapot('Ezt az azonosítót nem találjuk',
              valasz.uzenet
                || 'Lehet, hogy elgépelés történt, vagy a mentés megőrzési ideje lejárt. '
                   + 'Az ajánlót bármikor újra lefuttathatja.', true);
      if (mezo) mezo.value = id;
      return;
    }
    rajzol(valasz.ugy || {});
    /* A címsor kövesse, amit néz — így a lap megosztható és könyvjelzőzhető. */
    try { history.replaceState(null, '', '?id=' + encodeURIComponent(id)); } catch (_) { /* nincs mit tenni */ }
  }

  /* ---------------------------------------------------------------- INDÍTÁS */

  if (eszkoztar) {
    const ny = eszkoztar.querySelector('[data-er-nyomtat]');
    if (ny) ny.addEventListener('click', () => window.print());
  }

  if (kereso) {
    kereso.addEventListener('submit', (ev) => {
      ev.preventDefault();
      /* Az `ugy.js` NEVEZI MEG a hibát (tiltott jel, hiányzó jel) — a puszta
         „helyes alak: MA-XXXX-XXXX" nem mondta meg, mi rossz a beírtban. */
      const e = ellenoriz(mezo.value);
      if (!e.ok) {
        mezo.setAttribute('aria-invalid', 'true');
        allapot('Az azonosító nem megfelelő', e.uzenet, true);
        mezo.focus();
        return;
      }
      mezo.value = e.azon;
      mezo.removeAttribute('aria-invalid');
      betolt(e.azon);
    });
  }

  const id = new URLSearchParams(location.search).get('id');
  const idEll = id ? ellenoriz(id) : null;
  if (idEll && idEll.ok) {
    betolt(idEll.azon);
  } else if (idEll) {
    /* Hibás kód a címsorban (elgépelt vagy csonka link): a hibát mondjuk
       meg, ne egy általános „adja meg" felhívást. */
    allapot('Az azonosító nem megfelelő', idEll.uzenet, true);
    if (mezo) { mezo.value = id; mezo.setAttribute('aria-invalid', 'true'); }
  } else {
    allapot('Adja meg a mentett eredmény azonosítóját',
            'A megoldás-ajánló záró képernyőjén kapott kóddal bármikor előveheti '
            + 'azt, amit a modul mondott. A kód a mentett PDF-en is szerepel.', true);
    if (id) { if (mezo) mezo.value = id; }
  }
})();
