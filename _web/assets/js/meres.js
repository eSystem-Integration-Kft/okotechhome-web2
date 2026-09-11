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
  /* Az IP-anonimizálás a GA4-ben alapértelmezett és nem kapcsolható ki, ezért
     nem állítjuk külön. A `denied` állapotban küldött jelzés sütit nem használ. */
  gtag('config', AZON);

  const t = document.createElement('script');
  t.async = true;
  t.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(AZON);
  document.head.append(t);

  /* A DÖNTÉS KÖVETÉSE. A `suti.js` induláskor is hirdet (a mentett döntéssel),
     és minden mentésnél újra — így a visszavonás is ideér, nem csak a megadás. */
  document.addEventListener('oth:suti', (e) => {
    const eng = e.detail && e.detail.statisztika ? 'granted' : 'denied';
    gtag('consent', 'update', { analytics_storage: eng });
  });
})();
