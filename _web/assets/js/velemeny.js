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

    /* ------------------------------------------------ automata léptetés
       A vélemények maguktól továbblépnek, hogy a látogató többet lásson
       egynél anélkül, hogy kattintania kellene.

       ÁLL, amikor a látogató épp foglalkozik vele: egér a dobozon, fókusz
       benne (billentyűzet), vagy a lap háttérbe kerül. Enélkül olvasás közben
       kicsúszna a szöveg a szeme elől, és a nyilakkal is versenyezne.

       Saját kattintás után újraindul az időzítő, nem a maradékkal folytatja —
       különben közvetlenül a kézi lépés után azonnal továbbugorhatna. */
    const LEPESKOZ = 7000;
    let ora = null;
    let allitva = false;

    const indit = () => {
      if (ora || allitva || elemek.length < 2) return;
      ora = setInterval(() => lep(1, false), LEPESKOZ);
    };
    const megall = () => { clearInterval(ora); ora = null; };
    const ujraindit = () => { megall(); indit(); };

    /* Csökkentett mozgásigénynél nincs automata léptetés: a magától mozgó
       tartalom pont az, amit a beállítás ki akar kapcsolni. */
    const nyugodt = window.matchMedia('(prefers-reduced-motion: reduce)');

    const allapot = (all) => { allitva = all; if (all) megall(); else indit(); };

    doboz.addEventListener('mouseenter', () => allapot(true));
    doboz.addEventListener('mouseleave', () => allapot(false));
    doboz.addEventListener('focusin', () => allapot(true));
    doboz.addEventListener('focusout', (e) => {
      if (!doboz.contains(e.relatedTarget)) allapot(false);
    });
    /* Háttérbe került lap: a böngésző úgyis ritkítja az időzítőt, de így a
       visszatérő látogató nem egy tíz lépéssel arrébb ugrott listát talál. */
    document.addEventListener('visibilitychange', () => {
      if (document.hidden) megall(); else indit();
    });

    if (!nyugodt.matches) indit();
    nyugodt.addEventListener('change', (e) => { if (e.matches) megall(); else indit(); });

    if (elozo) elozo.addEventListener('click', () => lep(-1, false));
    if (kovetkezo) kovetkezo.addEventListener('click', () => lep(1, false));
    [elozo, kovetkezo].forEach((g) => g && g.addEventListener('click', ujraindit));

    /* Billentyűzet: a nyilak csak akkor lépnek, ha a fókusz a dobozon belül
       van — különben elvennénk a lapozást az oldal más elemeitől. */
    doboz.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft') { e.preventDefault(); lep(-1, true); }
      if (e.key === 'ArrowRight') { e.preventDefault(); lep(1, true); }
    });

    rajzol(false);
  });
})();
