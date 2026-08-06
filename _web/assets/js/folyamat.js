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

    const valt = (kulcs) => {
      gombok.forEach((g) => g.setAttribute('aria-expanded',
        String(g.dataset.folyamat === kulcs)));
      panelek.forEach((p) => { p.hidden = p.dataset.folyamatPanel !== kulcs; });
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
