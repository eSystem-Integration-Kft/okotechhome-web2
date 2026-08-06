/* =============================================================================
   ÖkoTech Home — Test2 · velemeny.js
   Visszajelzés-léptető — progressive enhancement
   -----------------------------------------------------------------------------
   A markupban MINDEN vélemény ott van, és JS nélkül mind látszik egymás alatt.
   Ez a fájl annyit tesz, hogy egyszerre egyet mutat, és léptethetővé teszi.
   Így a tartalom sosem vész el, és a keresők is mindet megtalálják.

   Nincs automatikus léptetés: a mozgó szöveg olvasás közben zavaró, és a
   WCAG 2.2 külön kéri, hogy az ötmásodpercnél hosszabb automatikus mozgás
   megállítható legyen. A léptetés itt csak felhasználói szándékra indul.
   ============================================================================= */

(() => {
  'use strict';

  document.querySelectorAll('[data-velemeny-doboz]').forEach((doboz) => {
    const elemek = Array.from(doboz.querySelectorAll('[data-velemeny]'));
    if (elemek.length < 2) return;

    const elozo = doboz.querySelector('[data-velemeny-elozo]');
    const kovetkezo = doboz.querySelector('[data-velemeny-kovetkezo]');
    const szamlalo = doboz.querySelector('[data-velemeny-szamlalo]');
    let mutat = 0;

    const rajzol = (fokusz) => {
      elemek.forEach((el, i) => {
        el.hidden = i !== mutat;
        el.toggleAttribute('data-aktiv', i === mutat);
      });
      if (szamlalo) szamlalo.textContent = (mutat + 1) + ' / ' + elemek.length;
      /* Léptetés után a megjelenő idézetre irányítjuk a fókuszt, különben a
         billentyűzetes és a képernyőolvasós felhasználó nem tudja, mi változott.
         Kattintásnál nem mozdítjuk, mert ott a szem követi. */
      if (fokusz) {
        const cel = elemek[mutat].querySelector('.velemeny-szoveg');
        if (cel) { cel.setAttribute('tabindex', '-1'); cel.focus({ preventScroll: true }); }
      }
    };

    const lep = (irany, fokusz) => {
      /* Körbeér: az utolsó után az első jön. Így egyik gomb sem válik
         használhatatlanná, és nem kell letiltott állapotot magyarázni. */
      mutat = (mutat + irany + elemek.length) % elemek.length;
      rajzol(fokusz);
    };

    if (elozo) elozo.addEventListener('click', () => lep(-1, false));
    if (kovetkezo) kovetkezo.addEventListener('click', () => lep(1, false));

    /* Billentyűzet: a nyilak csak akkor lépnek, ha a fókusz a dobozon belül
       van — különben elvennénk a lapozást az oldal más elemeitől. */
    doboz.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); lep(-1, true); }
      if (e.key === 'ArrowRight') { e.preventDefault(); lep(1, true); }
    });

    rajzol(false);
  });
})();
