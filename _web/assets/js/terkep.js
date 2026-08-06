/* =============================================================================
   ÖkoTech Home — Test2 · terkep.js
   Google Térkép betöltése KATTINTÁSRA
   -----------------------------------------------------------------------------
   Az oldal alapból saját, innen kiszolgált állóképet mutat: a betöltés így nem
   küld adatot harmadik félnek. A Google Térkép beágyazása viszont sütit tesz le
   és elküldi a látogató IP-jét a Google-nek — ez hozzájárulás nélkül nem
   jogszerű, ezért csak akkor töltjük be, ha a látogató RÁKATTINT.

   A gomb megnyomása maga a hozzájárulás: a szöveg megmondja, mi történik, és a
   kattintás előtt semmilyen kérés nem indul a Google felé.
   ============================================================================= */
(() => {
  'use strict';

  document.querySelectorAll('[data-terkep]').forEach((doboz) => {
    const gomb = doboz.querySelector('[data-terkep-betolt]');
    if (!gomb) return;

    gomb.addEventListener('click', () => {
      const keret = document.createElement('iframe');
      keret.className = 'terkep-beagyazott';
      keret.title = 'ÖkoTech Home — 2509 Esztergom, Strázsa u. 12. a Google Térképen';
      keret.loading = 'lazy';
      /* referrerpolicy: a Google ne kapja meg, melyik aloldalról érkezett. */
      keret.referrerPolicy = 'no-referrer-when-downgrade';
      keret.allowFullscreen = true;
      keret.src = 'https://www.google.com/maps?q=' +
        encodeURIComponent('2509 Esztergom, Strázsa u. 12.') + '&z=15&output=embed';

      doboz.dataset.terkepAllapot = 'beagyazott';
      doboz.append(keret);
      /* A gomb eltűnik: a betöltés nem visszavonható, és a kétszeri
         kattintás két iframe-et hozna létre. */
      gomb.remove();
    });
  });
})();
