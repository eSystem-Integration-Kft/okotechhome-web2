/* meres.js — Google Analytics 4, hozzájáruláshoz kötve.
   ---------------------------------------------------------------------------
   MIÉRT NEM A GOOGLE BEILLESZTŐ KÓDJA VAN ITT. Két okból:

   1. A CSP nem enged beágyazott szkriptet (`script-src 'self'`), a Google
      pedig beágyazott `<script>`-et ad. Beágyazott kód engedélyezéséhez
      `'unsafe-inline'` kellene — egyetlen mérőeszközért kinyitni az egész
      webhelyet XSS-re rossz üzlet. Külső fájlból ugyanez a kód fut, a CSP
      pedig szigorú marad.

   2. A MÉRÉS HOZZÁJÁRULÁSHOZ KÖTÖTT (GDPR 6. cikk (1) a), ePrivacy). A Google
      kódja alapból mér; itt alapból NEM. A `consent default` minden tárolást
      `denied`-re állít, MÉG AZELŐTT, hogy a `gtag.js` betöltene — a Consent
      Mode v2 csak így tudja visszatartani a sütiket. Utána a `suti.js`
      hirdetésére frissítünk. Ha a látogató nem járul hozzá, a GA4 sütit nem
      helyez el; legfeljebb süti nélküli, azonosítatlan jelzést küld.

   A MÉRŐAZONOSÍTÓ NEM EBBEN A FÁJLBAN VAN, hanem a beszúró `<script>` tag
   `data-ga4` attribútumában. Ezért maradhat ugyanez a fájl mindkét fában: a
   tag csak az ÉLES fába kerül bele (`prod-epit.sh`), a tesztoldal forgalma
   tehát nem szennyezi be az adatot. Azonosító nélkül a modul nem csinál semmit.
*/
(() => {
  'use strict';

  const sajat = document.currentScript
    || document.querySelector('script[data-ga4]');
  const AZON = sajat && sajat.dataset ? (sajat.dataset.ga4 || '').trim() : '';
  if (!AZON) return;                       // teszt üzemmód: nincs mérés

  window.dataLayer = window.dataLayer || [];
  function gtag() { window.dataLayer.push(arguments); }
  window.gtag = window.gtag || gtag;

  /* ALAPÁLLAPOT: MINDEN TILTVA. A `wait_for_update` ad fél másodpercet a
     `suti.js`-nek arra, hogy a korábban elmentett döntést kihirdesse — enélkül
     a visszatérő, hozzájáruló látogató első lapmegtekintése elveszne. */
  gtag('consent', 'default', {
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    functionality_storage: 'granted',
    security_storage: 'granted',
    wait_for_update: 500,
  });

  gtag('js', new Date());

  /* A GA4-ET NEM EZ A FÁJL TÖLTI BE — 2026-09-14 óta.
     ---------------------------------------------------------------------
     Korábban itt állt a `gtag('config', AZON)` és a `gtag/js` betöltése. A
     mérés azóta a GTM-konténeren (`gtm.js`) keresztül fut, és a konténer
     UGYANEZT a GA4 property-t tölti. Ha mindkettő futna, minden lapmegtekintés
     KÉTSZER számolódna — a PPC-brief ezért is köti ki, hogy GTM-en kívül ne
     kerüljön be Google-kód.

     AMI ITT MARAD, AZ A LÉNYEG: a Consent Mode v2 alapállapota. A `gtag()`
     ilyenkor is a `dataLayer`-be ír, a konténer pedig onnan olvassa — a
     `default` parancs tehát eléri a címkéket, csak épp a GTM-en át. A sorrendet
     a `prod-epit.sh` 6/b. rétege garantálja: a `meres.js` tag a `gtm.js` ELŐTT
     áll, és mindkettő `defer`.

     AZ AZONOSÍTÓ MARAD a `data-ga4` attribútumban: ez a kapcsoló, ami
     megmondja, hogy éles fában vagyunk-e, és dokumentálja, melyik property-be
     mérünk. Enélkül ez a modul nem csinál semmit. */

  /* A DÖNTÉS KÖVETÉSE. A `suti.js` induláskor is hirdet (a mentett döntéssel),
     és minden mentésnél újra — így a visszavonás is ideér, nem csak a megadás. */
  document.addEventListener('oth:suti', (e) => {
    const d = e.detail || {};
    const stat = d.statisztika ? 'granted' : 'denied';
    const mark = d.marketing   ? 'granted' : 'denied';
    /* MIND A NÉGY JEL, nem csak az analitika. A Consent Mode v2-ben a
       hirdetési célnak HÁROM külön jele van, és a Google Ads konverziómérés
       mindhármat nézi — ha csak az `analytics_storage`-ot frissítjük, a
       hirdetési jelek örökre `denied`-en maradnak, és a konverzió EU-ban
       mérhetetlen. A `terkep` nem tartozik ide: az a beágyazott Google Térkép
       megjelenítéséről szól, nem tárolásról. */
    gtag('consent', 'update', {
      analytics_storage:  stat,
      ad_storage:         mark,
      ad_user_data:       mark,
      ad_personalization: mark,
    });
  });
})();
