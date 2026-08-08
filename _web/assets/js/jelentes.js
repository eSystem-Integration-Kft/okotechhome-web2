/* =============================================================================
   ÖkoTech Home — jelentes.js
   Az ajánlat-összehasonlítási jelentés: adatgyűjtés, megjelenítés, letöltés
   -----------------------------------------------------------------------------
   Egy adat, három kimenet — és mindhárom UGYANEBBŐL a kódból épül, hogy ne
   tudjanak eltérni egymástól:

     1. a /jelentes oldal képernyős nézete,
     2. a letöltött, önhordó HTML-fájl,
     3. az e-mailben elküldött változat (a szerver ugyanezt az adatot kapja).

   MIÉRT NEM ELÉG EGY BLOB-ABLAK A NYOMTATÁSHOZ. Kézenfekvő volna a kész HTML-t
   `blob:` URL-en megnyitni és kinyomtatni. A `blob:` dokumentum viszont a
   létrehozó lap tartalombiztonsági szabályát (CSP) örökli, a webhelyé pedig
   `style-src 'self'` — beágyazott `<style>` blokk nélkül a jelentés formázás
   nélkül, csupasz szövegként jelenne meg. Ezért a nyomtatás egy VALÓDI,
   azonos eredetű oldalon (jelentes.html) történik, külső stíluslappal.

   A LETÖLTÖTT fájlra ez nem vonatkozik: azt a látogató `file://` alatt nyitja
   meg, ahol nincs CSP — oda tehát beépíthetjük a stíluslapot és a logót.
   ============================================================================= */

(() => {
  'use strict';

  const TAR_KULCS = 'oth-ajanlat-jelentes';

  /* A tábla celláin ez a hét állapotosztály fordulhat elő; a jelentés saját
     `jel-a-*` osztályaira képezzük le őket, hogy a stíluslap ne függjön a
     webhely osztályneveitől. */
  const ALLAPOTOK = ['yes', 'no', 'bad', 'warn', 'unclear', 'nodata', 'muted'];

  const HONAP = ['január', 'február', 'március', 'április', 'május', 'június',
                 'július', 'augusztus', 'szeptember', 'október', 'november', 'december'];

  const datum = (d) => `${d.getFullYear()}. ${HONAP[d.getMonth()]} ${d.getDate()}.`;

  const esc = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');

  /* ------------------------------------------------------------- adatgyűjtés */

  /** Egy tábla-cella tartalmát bontja értékre, részletre és állapotra. */
  const cella = (td) => {
    const jelolt = td.querySelector('.ofc-st');
    const forras = jelolt || td;
    const reszlet = forras.querySelector('small');
    const masolat = forras.cloneNode(true);
    masolat.querySelectorAll('svg, small').forEach((e) => e.remove());
    const allapot = ALLAPOTOK.find((a) => forras.classList.contains('ofc-st-' + a)) || '';
    return {
      ertek: masolat.textContent.replace(/\s+/g, ' ').trim() || '—',
      reszlet: reszlet ? reszlet.textContent.replace(/\s+/g, ' ').trim() : '',
      allapot,
    };
  };

  /**
   * A 11. szekció élő állapotát adattá alakítja. Azt olvassa, ami a képernyőn
   * van — így a jelentés sosem mondhat mást, mint amit a látogató lát.
   */
  const gyujt = () => {
    const tabla = document.querySelector('[data-ofc-table]');
    if (!tabla) return null;

    const fejek = Array.from(tabla.querySelectorAll('thead th')).slice(1);
    const ajanlatok = fejek.map((th, i) => {
      const kartya = document.querySelectorAll('[data-ofc-card]')[i];
      const fajl = kartya && kartya.querySelector('.ofc-file-name');
      const tipus = kartya && kartya.querySelector('.ofc-select');
      const megj = kartya && kartya.querySelector('.ofc-note');
      const sub = th.querySelector('.ofc-th-sub');
      const cim = th.cloneNode(true);
      cim.querySelectorAll('.ofc-th-sub').forEach((e) => e.remove());
      return {
        jel: ['A', 'B', 'C'][i] || String(i + 1),
        cim: cim.textContent.trim(),
        cimke: sub ? sub.textContent.replace(/\s+/g, ' ').trim() : '',
        fajl: fajl ? fajl.textContent.trim() : '',
        tipus: tipus && tipus.selectedIndex > 0 ? tipus.value : '',
        megjegyzes: megj ? megj.value.trim() : '',
      };
    });

    const sorok = Array.from(tabla.querySelectorAll('tbody tr')).map((tr) => {
      const cimke = tr.querySelector('th .ofc-cell-label') || tr.querySelector('th');
      const masolat = cimke.cloneNode(true);
      masolat.querySelectorAll('svg').forEach((e) => e.remove());
      return {
        cimke: masolat.textContent.replace(/\s+/g, ' ').trim(),
        osszeg: tr.classList.contains('ofc-row-total'),
        ertekek: Array.from(tr.querySelectorAll('td')).map(cella),
      };
    });

    const lista = document.querySelector('.ofc-ai-list');
    const megjegyzesek = lista
      ? Array.from(lista.querySelectorAll('li'))
          .filter((li) => !li.classList.contains('ofc-ai-wait'))
          .map((li) => li.textContent.replace(/\s+/g, ' ').trim())
          .filter(Boolean)
      : [];

    const sav = document.querySelector('.ofc-uzenet');

    return {
      keszult: datum(new Date()),
      ajanlatok,
      sorok,
      megjegyzesek,
      tajekoztato: sav ? sav.textContent.replace(/\s+/g, ' ').trim() : '',
    };
  };

  /* -------------------------------------------------------------- kirajzolás */

  const ajanlatKartya = (a) => {
    const sorok = [];
    if (a.cimke) sorok.push(`<p class="jel-ajanlat-cimke">${esc(a.cimke)}</p>`);
    if (a.fajl) sorok.push(`<p class="jel-ajanlat-fajl">${esc(a.fajl)}</p>`);
    if (a.tipus) sorok.push(`<p class="jel-ajanlat-fajl">Megadott típus: ${esc(a.tipus)}</p>`);
    if (a.megjegyzes) sorok.push(`<p class="jel-ajanlat-fajl">Megjegyzés: ${esc(a.megjegyzes)}</p>`);
    return `<div class="jel-ajanlat">
      <div class="jel-ajanlat-fej">
        <span class="jel-jel" aria-hidden="true">${esc(a.jel)}</span>
        <p class="jel-ajanlat-nev">${esc(a.cim)}</p>
      </div>
      ${sorok.join('\n      ')}
    </div>`;
  };

  const ertekCella = (c) => {
    const oszt = 'jel-ertek' + (c.allapot ? ' jel-a-' + c.allapot : '');
    const reszlet = c.reszlet ? `<span class="jel-reszlet">${esc(c.reszlet)}</span>` : '';
    return `<td><span class="${oszt}">${esc(c.ertek)}</span>${reszlet}</td>`;
  };

  /** A jelentés törzse — ugyanaz a weboldalon és a letöltött fájlban. */
  const markup = (adat) => {
    const fejek = adat.ajanlatok.map((a) =>
      `<th scope="col">${esc(a.cim)}${a.cimke ? `<span>${esc(a.cimke)}</span>` : ''}</th>`).join('\n            ');

    const sorok = adat.sorok.map((s) =>
      `<tr${s.osszeg ? ' class="jel-osszeg"' : ''}>
            <th scope="row">${esc(s.cimke)}</th>
            ${s.ertekek.map(ertekCella).join('\n            ')}
          </tr>`).join('\n          ');

    const megjegyzesek = adat.megjegyzesek.length
      ? `<section class="jel-blokk">
      <h2 class="jel-blokk-cim">Megjegyzések a dokumentumokról</h2>
      <ul class="jel-lista">
        ${adat.megjegyzesek.map((m) => `<li>${esc(m)}</li>`).join('\n        ')}
      </ul>
    </section>`
      : '';

    const tajekoztato = adat.tajekoztato
      ? `<p class="jel-zaro">${esc(adat.tajekoztato)}</p>` : '';

    return `<header class="jel-fejlec">
      <span class="jel-logo" data-jel-logo></span>
      <p class="jel-ceg">ÖkoTech-Home Kft.<br>okotechhome.hu · +36 33 200 211<br>kapcsolat@okotechhome.hu</p>
    </header>

    <div class="jel-cimsor">
      <p class="jel-eyebrow">Ajánlat-összehasonlítás</p>
      <h1 class="jel-cim">A beküldött ajánlatok egymás mellett</h1>
      <p class="jel-datum">Készült: ${esc(adat.keszult)}</p>
    </div>

    <section class="jel-blokk">
      <h2 class="jel-blokk-cim">Az összehasonlított ajánlatok</h2>
      <div class="jel-ajanlatok">
        ${adat.ajanlatok.map(ajanlatKartya).join('\n        ')}
      </div>
    </section>

    <section class="jel-blokk">
      <h2 class="jel-blokk-cim">Összehasonlítás szempontok szerint</h2>
      <div class="jel-tabla-keret">
        <table class="jel-tabla">
          <thead>
            <tr>
            <th scope="col">Szempont</th>
            ${fejek}
            </tr>
          </thead>
          <tbody>
          ${sorok}
          </tbody>
        </table>
      </div>
    </section>

    ${megjegyzesek}
    ${tajekoztato}

    <p class="jel-zaro"><strong>Tájékoztató jellegű összeállítás.</strong> A jelentés a
      beküldött dokumentumokból készült, és nem helyettesíti a helyszíni felmérést és a
      szakértői véleményt. Ahol „nincs adat” szerepel, ott a dokumentum nem tartalmazta az
      információt — ez nem jelenti azt, hogy a szolgáltatás kimarad az ajánlatból.</p>

    <footer class="jel-lab">
      <span>ÖkoTech-Home Kft. · 2509 Esztergom, Strázsa u. 12.</span>
      <span>okotechhome.hu</span>
      <span>Készült: ${esc(adat.keszult)}</span>
    </footer>`;
  };

  /* ------------------------------------------------------------ önhordó fájl */

  /**
   * Teljes, magában megálló HTML-fájl: a stíluslap és a logó beépítve, hogy a
   * letöltött dokumentum internet és webhely nélkül is ugyanígy nézzen ki.
   * A betűket viszont a Google Fontsról hivatkozzuk — beágyazva ~270 kB-tal
   * hizlalnák a fájlt. Hálózat nélkül a tartalék Georgia / rendszerbetű lép be,
   * a szedés kicsit más lesz, a tartalom változatlan.
   */
  const dokumentum = (adat, css, logo) => `<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="utf-8">
<title>Ajánlat-összehasonlítás — ÖkoTech Home (${esc(adat.keszult)})</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
body{margin:0;padding:clamp(1rem,4vw,2.5rem);background:#F3F2EC}
${css}
</style>
</head>
<body>
<article class="jel">
    ${markup(adat).replace('<span class="jel-logo" data-jel-logo></span>',
                           `<span class="jel-logo">${logo}</span>`)}
</article>
</body>
</html>
`;

  /* ------------------------------------------------------------- segédletek */

  const szoveg = (url) => fetch(url, { credentials: 'same-origin' })
    .then((r) => { if (!r.ok) throw new Error(url + ' — ' + r.status); return r.text(); });

  /** A logó SVG-jét a `<svg …>` kezdettől vesszük: az XML-fejlécet a HTML nem kéri. */
  const logoTisztit = (s) => s.slice(Math.max(0, s.indexOf('<svg')));

  const letolt = (nev, tartalom, tipus) => {
    const blob = new Blob([tartalom], { type: tipus });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = nev;
    document.body.append(a);
    a.click();
    a.remove();
    /* Az objektum-URL-t nem bontjuk azonnal: a letöltés a kattintás után
       aszinkron indul, és egyes böngészőkben a korai felszabadítás megszakítja. */
    setTimeout(() => URL.revokeObjectURL(url), 60000);
  };

  const fajlnev = (adat) =>
    'okotech-ajanlat-osszehasonlitas-'
    + adat.keszult.replace(/[^0-9]+/g, '-').replace(/^-|-$/g, '') + '.html';

  window.OthJelentes = {
    TAR_KULCS,
    gyujt,
    markup,
    datum,

    /** Elmenti az adatot, hogy a /jelentes oldal fel tudja venni. */
    tarol(adat) {
      try {
        sessionStorage.setItem(TAR_KULCS, JSON.stringify(adat));
        return true;
      } catch (_) {
        return false;
      }
    },

    olvas() {
      try {
        const s = sessionStorage.getItem(TAR_KULCS);
        return s ? JSON.parse(s) : null;
      } catch (_) {
        return null;
      }
    },

    /** A logót a kész törzsbe illeszti (a webhelyen és a letöltött fájlban is). */
    logotBeilleszt(gyoker, elotag) {
      const hely = gyoker.querySelector('[data-jel-logo]');
      if (!hely) return Promise.resolve();
      return szoveg(elotag + 'assets/img/logo-jelentes.svg')
        .then((svg) => { hely.innerHTML = logoTisztit(svg); })
        .catch(() => { hely.textContent = 'ÖkoTech Home'; });
    },

    /** Önhordó HTML-fájl összeállítása és letöltése. */
    letoltes(adat, elotag) {
      return Promise.all([
        szoveg(elotag + 'assets/css/jelentes.css'),
        szoveg(elotag + 'assets/img/logo-jelentes.svg').then(logoTisztit).catch(() => 'ÖkoTech Home'),
      ]).then(([css, logo]) => {
        letolt(fajlnev(adat), dokumentum(adat, css, logo), 'text/html;charset=utf-8');
      });
    },
  };
})();
