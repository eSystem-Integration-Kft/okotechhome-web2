/* =============================================================================
   ÖkoTech Home — jelentes-oldal.js
   A /jelentes oldal vezérlése
   -----------------------------------------------------------------------------
   Az adatot a 11. szekció adja át `sessionStorage`-ban (jelentes.js). Ha nincs
   adat, az oldal nem üres táblát mutat, hanem megmondja, miért üres, és
   visszairányít — a csupa „—" tábla azt sugallná, hogy az elemzés lefutott és
   nem talált semmit.

   `?nyomtat=1` esetén a lap magától megnyitja a nyomtatási párbeszédet. Előbb
   megvárjuk a logót és a betűket: a nyomtatási kép abban a pillanatban készül,
   amikor a párbeszéd megnyílik, egy félig betöltött lapot nyomtatna ki.
   ============================================================================= */

(() => {
  'use strict';

  const J = window.OthJelentes;
  const torzs = document.querySelector('[data-jelentes-torzs]');
  const ures = document.querySelector('[data-jelentes-ures]');
  const eszkoztar = document.querySelector('[data-jelentes-eszkoztar]');
  if (!J || !torzs || !ures || !eszkoztar) return;

  const adat = J.olvas();

  if (!adat || !adat.sorok || !adat.sorok.length) {
    ures.hidden = false;
    return;
  }

  torzs.innerHTML = J.markup(adat);
  torzs.hidden = false;
  eszkoztar.hidden = false;

  const logoKesz = J.logotBeilleszt(torzs, '');

  const nyomtat = document.querySelector('[data-jelentes-nyomtat]');
  if (nyomtat) nyomtat.addEventListener('click', () => window.print());

  const letolt = document.querySelector('[data-jelentes-letolt]');
  if (letolt) {
    letolt.addEventListener('click', () => {
      letolt.disabled = true;
      J.letoltes(adat, '')
        .catch(() => { window.alert('A jelentés összeállítása nem sikerült. Kérjük, próbálja újra.'); })
        .finally(() => { letolt.disabled = false; });
    });
  }

  if (new URLSearchParams(location.search).get('nyomtat') === '1') {
    const betuk = document.fonts && document.fonts.ready
      ? document.fonts.ready : Promise.resolve();
    Promise.all([logoKesz, betuk]).then(() => setTimeout(() => window.print(), 120));
  }
})();
