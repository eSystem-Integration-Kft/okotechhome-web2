/* =============================================================================
   ÖkoTech Home — Test2 · urlap.js
   Űrlapbeküldés oldalfrissítés nélkül — progressive enhancement
   -----------------------------------------------------------------------------
   Az űrlap JS NÉLKÜL is teljes értékű: sima POST megy a végpontra. Ez a fájl
   annyit tesz, hogy elfogja a beküldést, és a választ helyben jeleníti meg —
   így a látogató nem veszíti el a kitöltött oldalt, és a hibás mezőhöz vissza
   tud lépni.

   Amit szándékosan NEM csinál: nem validál a szerver helyett. A böngésző
   natív ellenőrzése (`required`, `type="email"`) segít, de a döntést a
   végpont hozza — a kliensoldali ellenőrzés megkerülhető.
   ============================================================================= */

(() => {
  'use strict';

  const urlapok = document.querySelectorAll('[data-urlap]');
  if (!urlapok.length) return;

  urlapok.forEach((urlap) => {
    /* A megnyitás időpontja: a végpont ebből látja, ha valaki 3 másodperc
       alatt „töltötte ki" az űrlapot. A mező JS nélkül üres marad, és a
       szerver akkor egyszerűen nem alkalmazza ezt a szűrőt. */
    const ido = urlap.querySelector('[data-urlap-ido]');
    if (ido) ido.value = String(Math.floor(Date.now() / 1000));

    /*
     * A KORÁBBI ÜGY AZONOSÍTÓJA — MINDEN ŰRLAPHOZ, EGY HELYEN.
     *
     * Ha a látogató korábban kitöltötte az ársávbecslőt vagy a
     * megoldás-ajánlót és el is mentette, ez a kód összeköti a mostani, NÉVVEL
     * érkező megkeresést a korábbi névtelen válaszaival. Az értékesítő így már
     * a hívás előtt tudja, mekkora házról, milyen jelenlegi megoldásról és
     * milyen ársávról van szó — anélkül, hogy a látogatónak bármit meg kellett
     * volna ismételnie.
     *
     * ITT, ÉS NEM ŰRLAPONKÉNT. Minden űrlap ezen a kezelőn megy át; ha
     * egyesével kellene beírni, a következő űrlapnál elmaradna — és a hiány
     * néma: a megkeresés attól még megérkezik, csak épp előzmény nélkül.
     *
     * Ha nincs mentett ügy, a mező nem jön létre: üres értéket küldeni
     * ugyanaz, mint nem küldeni, de a kérésben zajt jelentene.
     */
    try {
      const ugy = window.OthUgy && window.OthUgy.allapot ? window.OthUgy.allapot() : null;
      const azon = ugy && ugy.azonosito ? ugy.azonosito : '';

      if (azon && !urlap.querySelector('[name="ugy_azonosito"]')) {
        const rejtett = document.createElement('input');
        rejtett.type = 'hidden';
        rejtett.name = 'ugy_azonosito';
        rejtett.value = azon;
        urlap.appendChild(rejtett);
      }
    } catch (hiba) {
      /* Az ügytár hiánya nem akadályozhatja meg a beküldést: a megkeresés
         előzmény nélkül is teljes értékű. */
    }

    const valasz = urlap.querySelector('[data-urlap-valasz]');
    const gomb = urlap.querySelector('button[type="submit"]');

    const jelez = (szoveg, allapot) => {
      if (!valasz) return;
      valasz.textContent = szoveg;
      if (allapot === 'hiba') valasz.setAttribute('data-allapot', 'hiba');
      else valasz.removeAttribute('data-allapot');
      valasz.hidden = false;
      valasz.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    };

    const mezoHibak = (mezok) => {
      urlap.querySelectorAll('[aria-invalid]').forEach((m) => m.removeAttribute('aria-invalid'));
      if (!mezok) return;
      let elso = null;
      Object.keys(mezok).forEach((nev) => {
        const m = urlap.querySelector('[name="' + nev + '"]');
        if (!m) return;
        m.setAttribute('aria-invalid', 'true');
        if (!elso) elso = m;
      });
      if (elso) elso.focus();
    };

    urlap.addEventListener('submit', async (e) => {
      /* Ha a böngésző natív ellenőrzése megbukik, hagyjuk őt dolgozni. */
      if (!urlap.checkValidity()) return;

      e.preventDefault();
      if (gomb) { gomb.disabled = true; gomb.setAttribute('aria-busy', 'true'); }

      try {
        const res = await fetch(urlap.action, {
          method: 'POST',
          headers: { 'Accept': 'application/json' },
          body: new FormData(urlap),
        });
        const adat = await res.json().catch(() => ({}));

        if (res.ok && adat.ok) {
          mezoHibak(null);
          jelez(adat.uzenet || 'Köszönjük, megkaptuk.', 'ok');
          urlap.reset();
          if (ido) ido.value = String(Math.floor(Date.now() / 1000));
          /* Sikeres küldés után a gomb tiltva marad: a kétszeri beküldés
             ugyanazt a levelet küldené el újra. */
          return;
        }
        mezoHibak(adat.mezok);
        jelez(adat.uzenet || 'A küldés most nem sikerült. Kérjük, próbálja újra.', 'hiba');
      } catch (_) {
        jelez('A küldés most nem sikerült — lehet, hogy megszakadt a kapcsolat. '
            + 'Próbálja újra, vagy hívjon minket: +36 33 200 211.', 'hiba');
      } finally {
        if (gomb && !urlap.querySelector('[data-urlap-valasz]:not([data-allapot])')) {
          gomb.disabled = false;
          gomb.removeAttribute('aria-busy');
        }
      }
    });
  });
})();
