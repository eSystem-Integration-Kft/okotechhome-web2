/* =============================================================================
   ÖkoTech Home — Test2 · gyik.js
   Kétszintű GYIK: kategóriafülek + kérdéslista + válaszpanel
   -----------------------------------------------------------------------------
   JS NÉLKÜL minden kategória és minden válasz látszik egymás alatt — a `hidden`
   attribútumot ez a szkript teszi rájuk. A tizennégy kérdés-válasz így a
   keresők számára is teljes egészében elérhető marad.

   Az állapotot `aria-selected` hordozza, nem osztály: a képernyőolvasó ebből
   tudja, melyik fül és melyik kérdés aktív, és a stílus is ebből következik.
   ============================================================================= */
(() => {
  'use strict';
  document.querySelectorAll('[data-gyik]').forEach((doboz) => {
    const fulek = Array.from(doboz.querySelectorAll('[data-gyik-ful]'));
    const tablak = Array.from(doboz.querySelectorAll('[data-gyik-tabla]'));
    if (!fulek.length) return;

    const kerdesValt = (tabla, kulcs) => {
      tabla.querySelectorAll('[data-gyik-kerdes]').forEach((k) =>
        k.setAttribute('aria-selected', String(k.dataset.gyikKerdes === kulcs)));
      tabla.querySelectorAll('[data-gyik-valasz]').forEach((v) => {
        v.hidden = v.dataset.gyikValasz !== kulcs;
      });
    };

    const fulValt = (kulcs, fokusz) => {
      fulek.forEach((f) => {
        const akt = f.dataset.gyikFul === kulcs;
        f.setAttribute('aria-selected', String(akt));
        /* Roving tabindex: a fülsoron egyetlen Tab-megálló van, a többi
           nyíllal érhető el — ez a WAI-ARIA tabs mintája. */
        f.tabIndex = akt ? 0 : -1;
        if (akt && fokusz) f.focus();
      });
      tablak.forEach((t) => { t.hidden = t.dataset.gyikTabla !== kulcs; });
    };

    fulek.forEach((f) => f.addEventListener('click', () => fulValt(f.dataset.gyikFul, false)));

    doboz.querySelectorAll('[data-gyik-tabla]').forEach((tabla) => {
      tabla.querySelectorAll('[data-gyik-kerdes]').forEach((k) =>
        k.addEventListener('click', () => kerdesValt(tabla, k.dataset.gyikKerdes)));
      const elso = tabla.querySelector('[data-gyik-kerdes]');
      if (elso) kerdesValt(tabla, elso.dataset.gyikKerdes);
    });

    doboz.querySelector('[role="tablist"]').addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
      const i = fulek.indexOf(document.activeElement);
      if (i < 0) return;
      e.preventDefault();
      const uj = fulek[(i + (e.key === 'ArrowRight' ? 1 : -1) + fulek.length) % fulek.length];
      fulValt(uj.dataset.gyikFul, true);
    });

    fulValt(fulek[0].dataset.gyikFul, false);
  });
})();
