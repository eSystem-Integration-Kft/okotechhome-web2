/* =============================================================================
   ÖkoTech Home — Test2 · folyamat.js
   Szolgáltatási folyamat — lépéssor
   -----------------------------------------------------------------------------
   A markupban mind a hat lépés panelje ott van, és JS NÉLKÜL mind látszik
   egymás alatt: a `hidden` attribútumot ez a szkript teszi rájuk. A tartalom
   így sosem vész el, és a keresők is megtalálják mind a hat leírást.

   A gombok `aria-expanded`-del jelzik az állapotot, tehát a kiválasztást nem
   csak a szín hordozza — képernyőolvasóval és színlátászavarral is követhető.
   ============================================================================= */
(() => {
  'use strict';
  document.querySelectorAll('[data-folyamat-doboz]').forEach((doboz) => {
    const gombok = Array.from(doboz.querySelectorAll('[data-folyamat]'));
    const panelek = Array.from(doboz.querySelectorAll('[data-folyamat-panel]'));
    if (gombok.length < 2 || !panelek.length) return;

    const sin = doboz.querySelector('.folyamat-sin');

    const valt = (kulcs) => {
      const hol = gombok.findIndex((g) => g.dataset.folyamat === kulcs);

      gombok.forEach((g, i) => {
        g.setAttribute('aria-expanded', String(i === hol));
        /* Három állapot: megtett · jelenlegi · hátralévő. Attribútumban, nem
           osztályban — az állapot adat, és a CSS ebből következik. */
        const lepes = g.closest('.folyamat-lepes');
        if (lepes) {
          lepes.dataset.allapot = i < hol ? 'kesz' : (i === hol ? 'itt' : 'hatra');
        }
      });
      panelek.forEach((p) => { p.hidden = p.dataset.folyamatPanel !== kulcs; });

      /* A kitöltött sáv a lépés KÖZEPÉIG ér: a korongok a rács celláinak
         közepén ülnek, tehát az arány (index + 0,5) / lépésszám. */
      if (sin && gombok.length > 1) {
        const arany = (hol + 0.5) / gombok.length;
        sin.style.setProperty('--folyamat-halad', String(Math.max(0, Math.min(1, arany))));
      }
    };

    gombok.forEach((g) => g.addEventListener('click', () => valt(g.dataset.folyamat)));

    /* Nyilakkal is lépkedhető, ahogy a natív tab-listáknál megszokott. */
    doboz.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      const i = gombok.indexOf(document.activeElement);
      if (i < 0) return;
      e.preventDefault();
      const uj = gombok[(i + (e.key === 'ArrowRight' ? 1 : -1) + gombok.length) % gombok.length];
      uj.focus(); valt(uj.dataset.folyamat);
    });

    valt(gombok[0].dataset.folyamat);
  });
})();
