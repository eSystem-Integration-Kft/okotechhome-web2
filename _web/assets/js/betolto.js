/* betolto.js — a lap alatti widgetek szkriptjei az ELSŐ KIRAJZOLÁS UTÁN.
   ---------------------------------------------------------------------------
   MIÉRT. A `defer` szkript a HTML feldolgozása után, de az első kirajzolás
   ELŐTT futhat le: a böngésző a stíluslapra vár, és amikor megérkezik, előbb
   a várakozó szkripteket futtatja, csak utána rajzol. Lassú telefonon így a
   főoldal 11 widgetjének (~135 KB) kódja a hero címsora elé állt.
   Mérve 2026-09-16-án, PSI-hez hasonló lassú CPU-n (benchmark ~740): a
   szimulált LCP mediánja 3,49 mp-ről 3,27 mp-re csökkent, a widgetek ugyanúgy
   felépültek.

   HOGYAN. A késleltetett szkript helyőrzőként áll a lapon:
       <script type="text/plain" data-kesleltetett src="…"></script>
   A nem JavaScript típusú `<script>`-et a böngésző nem tölti le és nem
   futtatja, az útvonala viszont a helyén marad (a verzióemelés és az
   `ellenorzes.sh` ugyanúgy látja). Ez a fájl a kirajzolás után valódi
   `<script>`-re cseréli őket, `async = false`-szal — így a lapon álló
   SORRENDBEN futnak le (pl. az `ugy.js` az `ai-advisor.js` előtt).

   A „KIRAJZOLÁS UTÁN" a `requestAnimationFrame` + `setTimeout(0)`: a képkocka
   callbackje a festés előtt fut, a benne ütemezett feladat már utána.
   Háttérlapon nincs képkocka (a rAF nem fut) — ott azonnal indulunk. A 2 mp-es
   tartalék arra az esetre van, ha a képkocka valamiért elmaradna.

   Melyik szkript kerülhet ide, azt a `scripts/oldalgyartas/szkript_kesleltetes.py`
   dönti el (a lapon álló többi szkript függőségeivel együtt). */
(() => {
  'use strict';
  let elindult = false;

  const indit = () => {
    if (elindult) return;
    elindult = true;
    for (const helyorzo of document.querySelectorAll('script[data-kesleltetett]')) {
      const szkript = document.createElement('script');
      szkript.src = helyorzo.src;
      szkript.async = false;
      helyorzo.after(szkript);
    }
  };

  const kirajzolasUtan = () => {
    if (document.visibilityState === 'hidden') {
      indit();
      return;
    }
    requestAnimationFrame(() => setTimeout(indit, 0));
    setTimeout(indit, 2000);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', kirajzolasUtan, { once: true });
  } else {
    kirajzolasUtan();
  }
})();
