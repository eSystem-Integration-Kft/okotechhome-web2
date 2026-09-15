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

  /* ===================== A SAJÁT GA4 — KONTÉNERTŐL FÜGGETLENÜL ============
     MIÉRT VAN MÉGIS KÖZVETLEN GA4, a fenti indoklás ellenére. A konténert
     2026-09-15 óta MÁS CÉG üzemelteti. Ami a konténerben van, azt ők
     bármikor átírhatják — és ha a GA4-címke kikerül belőle, a mérésünk velük
     együtt tűnik el, jelzés nélkül. Az ügyfél saját mérése nem függhet attól,
     hogy egy külső fél mit tesz egy olyan felületen, amihez nekünk nincs
     hozzáférésünk.

     EZÉRT KÜLÖN PROPERTY, NEM UGYANAZ. A `data-ga4-sajat` attribútum a MI
     property-nk azonosítóját hordozza, ami NEM egyezhet a konténerben állóval.
     Ha a kettő ugyanaz volna, minden lapmegtekintés kétszer számolódna, és a
     riportok használhatatlanná válnának. A `prod-epit.sh` ezért ellenőrzi is,
     hogy a két azonosító különbözik-e.

     A HOZZÁJÁRULÁST UGYANÚGY MEGVÁRJA. A Consent Mode v2 alapállapota fentebb
     mindent `denied`-re állít, és ez a címke is annak a hatálya alatt fut: süti
     csak akkor születik, ha a látogató a statisztikai kategóriát engedte.
     Enélkül a GA4 süti nélküli jelzést küld, ahogy a konténerbeli is. */
  const SAJAT = sajat && sajat.dataset ? (sajat.dataset.ga4Sajat || '').trim() : '';
  if (SAJAT && SAJAT !== AZON) {
    const g = document.createElement('script');
    g.async = true;
    g.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(SAJAT);
    document.head.append(g);

    /* `send_page_view` marad az alapértelmezésen (igen): ez a címke ÖNÁLLÓ
       mérés, nem a konténer kiegészítése — a lapmegtekintést neki magának kell
       rögzítenie. */
    gtag('config', SAJAT);
  }

  /* A DÖNTÉS KÖVETÉSE. A `suti.js` induláskor is hirdet (a mentett döntéssel),
     és minden mentésnél újra — így a visszavonás is ideér, nem csak a megadás. */
  /* ===================== META PIXEL ======================================
     A PIXEL NEM ÉRTI A CONSENT MODE-OT, ezért saját hozzájárulási API-ja van:
     `fbq('consent','revoke' | 'grant')`. A dokumentáció két dolgot köt ki —
     a `revoke` az `init` ELŐTT álljon, és MINDEN lapon lefusson.

     MIÉRT ITT ÉS NEM A KONTÉNERBEN. A Pixelt a GTM-konténer tölti be, a
     triggere ott „minden oldal”. A konténert nem tudjuk szerkeszteni, viszont
     ez a fájl a konténer ELŐTT fut (a `prod-epit.sh` 6/b. rétege garantálja a
     sorrendet) — így a `revoke` biztosan megelőzi a Pixel indulását.

     A CSONK A META SAJÁT SNIPPETJÉNEK A SORBAN ÁLLÓ RÉSZE. A Pixel betöltésekor
     a Meta kódja látja, hogy az `fbq` már létezik, és a sorban álló parancsokat
     — köztük a `revoke`-ot — feldolgozza. A szkriptet NEM töltjük be: azt a
     konténer teszi.

     EZ JAVÍT EGY VALÓDI HIBÁT: a korábbi megoldás a konténert BÁRMILYEN
     döntésre elindította, tehát aki csak a szükséges sütiket engedte, annál is
     elsült a Pixel. A marketing kategória külön jel, és mostantól az dönt. */
  if (!window.fbq) {
    const n = function () {
      n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    };
    window.fbq = n;
    if (!window._fbq) window._fbq = n;
    n.push = n; n.loaded = true; n.version = '2.0'; n.queue = [];
  }
  window.fbq('consent', 'revoke');

  document.addEventListener('oth:suti', (e) => {
    const d = e.detail || {};
    /* A Metának KÜLÖN kell szólni — a Consent Mode frissítése rá nem hat. */
    try { window.fbq('consent', d.marketing ? 'grant' : 'revoke'); } catch (_) {}
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
