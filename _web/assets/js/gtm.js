/* gtm.js — Google Tag Manager konténer, hozzájáruláshoz igazítva.
   ---------------------------------------------------------------------------
   MIÉRT NEM A GOOGLE BEILLESZTŐ KÓDJA VAN A LAPON. Ugyanaz az ok, ami a
   `meres.js`-nél: a CSP nem enged beágyazott szkriptet (`script-src 'self'`),
   a Google pedig beágyazott `<script>`-et ad. Beágyazott kód engedélyezéséhez
   `'unsafe-inline'` kellene — egyetlen mérőeszközért kinyitni az egész
   webhelyet XSS-re rossz üzlet. Külső fájlból ugyanaz a konténer tölt be, a
   CSP pedig szigorú marad.

   A KONTÉNERAZONOSÍTÓ NEM ITT VAN, hanem a beszúró `<script>` tag `data-gtm`
   attribútumában. Ezért maradhat ugyanez a fájl mindkét fában: a tag csak az
   ÉLES fába kerül bele (`prod-epit.sh`), a tesztoldal forgalma tehát nem
   szennyezi be az adatot. Azonosító nélkül a modul nem csinál semmit.

   A SORREND SZÁMÍT. Ez a fájl a `meres.js` UTÁN töltődik, és mindkettő
   `defer` — a `defer`-es szkriptek a dokumentum sorrendjében futnak le. Így a
   Consent Mode v2 alapállapota (minden `denied`) MÁR OTT VAN a dataLayerben,
   mielőtt a konténer betöltene. Ez nem stílus kérdése: a Consent Mode csak
   akkor tudja visszatartani a sütiket, ha a `default` parancs megelőzi a
   címkéket.

   AMIT EZ A FÁJL NEM CSINÁL: nem tölt be GA4-et, Google Ads-et vagy Meta
   Pixelt. Mindhárom a konténerben él. A webhelyen GTM-en kívül szándékosan
   nincs mérőkód — két helyről mérve ugyanaz az esemény kétszer számolódna.
*/
(() => {
  'use strict';

  const sajat = document.currentScript
    || document.querySelector('script[data-gtm]');
  const AZON = sajat && sajat.dataset ? (sajat.dataset.gtm || '').trim() : '';
  if (!AZON) return;                       // teszt üzemmód: nincs konténer

  function betolt() {
    /* A `dataLayer` MÁR LÉTEZIK: a `suti.js` a döntést, a `meres.js` a Consent
       Mode alapállapotát tolta bele. Nem felülírjuk, hanem folytatjuk. */
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ 'gtm.start': Date.now(), event: 'gtm.js' });

    const t = document.createElement('script');
    t.async = true;
    t.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(AZON);
    document.head.append(t);
  }

  /* A KONTÉNER AZONNAL INDUL. Ez a Consent Mode v2 feltétele.
     ---------------------------------------------------------------------
     VOLT ITT EGY KÉSLELTETÉS: a konténer megvárta a látogató döntését. Bela
     döntése alapján (2026-09-14) kikerült — „menjen, ne korlátozzuk”. A
     mérési előírás Consent Mode v2-t kér, és a késleltetés pont azt ütötte ki.

     MIÉRT VOLT OTT. A Meta Pixel nem vesz részt a Consent Mode-ban: a Google
     címkéit a `denied` alapállapot visszafogja, a Pixelt nem. A konténerben a
     Pixel triggere „minden oldal”, tehát mérve, élesben, a konténerrel együtt
     betöltött — döntés előtt.

     MI FOGJA VISSZA MOSTANTÓL. A Meta saját hozzájárulási API-ja, a
     `meres.js`-ben: `fbq('consent', 'revoke')` fut a konténer betöltése ELŐTT,
     és `grant` csak akkor megy, ha a látogató a MARKETING kategóriát fogadta
     el. A `revoke` állapotú Pixel nem sütizik és nem küld eseményt. Ez most
     EGYETLEN réteg, nem kettő — ezért a `meres.js` sorrendje (Consent Mode
     alapállapot → fbq stub → revoke) nem átrendezhető, és a `prod-epit.sh`
     beszúrási sorrendje sem.

     AMIT A KÉSLELTETÉS ELRONTOTT, és ezért került ki:
       · a Consent Mode v2 SÜTI NÉLKÜLI JELZÉSEI el sem indultak;
       · aki a sávra EGYÁLTALÁN NEM VÁLASZOLT, semmilyen mérésbe nem került
         bele, még modellezettbe sem.

     AMIT CSERÉBE VÁLLALTUNK: a konténer szkriptje döntés előtt is elindul,
     tehát a látogató IP-címe eljut a Google-höz és a Metához. A Consent Mode
     v2 így működik, és a mérési előírás ezt kéri.

     A VISSZAÚT EGY SOR, ha mégis kell: a `betolt()` helyett újra
     `document.addEventListener('oth:suti', betolt, { once: true })`. */
  betolt();
})();
