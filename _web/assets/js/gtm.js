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

  /* A KONTÉNER MEGVÁRJA A DÖNTÉST — és ez átmeneti megoldás.
     ---------------------------------------------------------------------
     MÉRVE 2026-09-14-én, élesben: amint a konténer betöltött, vele betöltött a
     Meta Pixel is (`connect.facebook.net/signals/config/…` és `fbevents.js`) —
     MIELŐTT a látogató bármihez hozzájárult volna. A Meta Pixel ugyanis nem
     vesz részt a Consent Mode-ban: a Google címkéit a `denied` alapállapot
     visszafogja, a Pixelt nem. A konténerben a trigger „minden oldal”, tehát
     a hozzájárulás megkérdezése előtt sütizett.

     KÉT RÉTEG VÉDI, mert a kettő mást old meg:

     1. EZ A KÉSLELTETÉS — a konténer csak azután indul, hogy a látogató
        döntött. Amíg nem döntött, EGYETLEN kérés sem megy a Google-höz vagy a
        Metához; a puszta szkriptbetöltés is elárulná az IP-címét.

     2. A META SAJÁT HOZZÁJÁRULÁSI API-ja (`meres.js`): `fbq('consent',
        'revoke')` a konténer előtt, és csak `marketing === true` esetén
        `grant`. EZ JAVÍT EGY VALÓDI HIBÁT: önmagában ez a késleltetés
        BÁRMILYEN döntésre elindítja a konténert, tehát aki csak a szükséges
        sütiket engedte, annál is elsült volna a Pixel. A marketing kategória
        külön jel, és mostantól az dönt.

     AMI AZ 1. RÉTEGGEL ELVÉSZ: a Consent Mode süti nélküli jelzései annál, aki
     még nem döntött. Valós veszteség, de kisebb baj, mint döntés előtt
     megkeresni a Google-t és a Metát.

     A KONTÉNER-OLDALI VÉGLEGES MEGOLDÁS: a Meta Pixel címkéjének triggere
     várjon az `oth_suti_dontes` eseményre, `oth_suti_marketing === "granted"`
     feltétellel. Amint ez megvan, az 1. réteg (ez a késleltetés) elhagyható, és
     a Google mérése teljes értékűvé válik — a 2. réteg akkor is maradjon. */
  const S = window.OthSuti;
  if (S && S.allapot && S.allapot().dontott) {
    betolt();
  } else {
    document.addEventListener('oth:suti', betolt, { once: true });
  }
})();
