/* =============================================================================
   ÖkoTech Home — Test2 · dokumentum.js
   Okirat-oldalak segédje: nyomtatás, keltezés, jogszabályi lábjegyzetek
   -----------------------------------------------------------------------------
   Három apró viselkedés, mindegyik progressive enhancement — JS nélkül az
   oldal teljes értékű marad:

     1) NYOMTATÁS. A gomb a böngésző saját nyomtatási párbeszédét nyitja meg
        (onnan PDF-be is menthető). JS nélkül a gomb elrejtve marad, mert a
        `Ctrl/⌘+P` amúgy is működik — hamis gombot nem mutatunk.

     2) KELTEZÉS. A „Kelt" dátuma a mai napra töltődik elő, de nem zárul le.

     3) JOGSZABÁLYI LÁBJEGYZETEK. A felső index szövege buborékban is olvasható,
        anélkül hogy a lap aljára kellene ugrani.

   A MELLÉKLETEK KÜLÖN MODULBAN élnek: `urlap-fajl.js` (ledobó felület,
   fájllista, korlátok).
   ============================================================================= */

(() => {
  'use strict';

  /* ------------------------------------------------------------- nyomtatás */
  document.querySelectorAll('[data-nyomtat]').forEach((gomb) => {
    gomb.hidden = false;
    gomb.addEventListener('click', () => window.print());
  });

  /* ----------------------------------------------------------- mai dátum */
  /* A „Kelt" dátuma az esetek túlnyomó részében a MAI nap — a legtöbb kitöltő
     ugyanaznap küldi be. Előtöltjük, de nem zárjuk le: aki visszamenőleg vagy
     előre keltez, felülírja. Csak ÜRES mezőt töltünk, hogy a böngésző által
     visszaállított értéket (frissítés után) ne írjuk felül. */
  document.querySelectorAll('input[type="date"][data-ma]').forEach((mezo) => {
    if (mezo.value) return;
    const ma = new Date();
    const p2 = (n) => String(n).padStart(2, '0');
    mezo.value = `${ma.getFullYear()}-${p2(ma.getMonth() + 1)}-${p2(ma.getDate())}`;
  });

  /* ------------------------------------------------- jogszabály-hivatkozások */
  /* A szövegben álló felső index (`[3]`) a lábjegyzetre mutat. Kattintásra oda
     is visz — ez JS nélkül is működik, mert sima horgony —, de a legtöbbször
     nem akar odaugrani senki: csak tudni akarja, mi az a [3].
     Ezért a lábjegyzet szövegét ÁTEMELJÜK egy buborékba, ami ráállásra
     megjelenik. A szöveg így EGY helyen él (a lábjegyzetlistában): nincs
     kétszer leírva, tehát nem is csúszhat el egymástól.

     A GÖRDÜLÉS is szelídebb: a `:target` villanás megmutatja, hova érkeztünk,
     különben a lap alján landolva a látogató keresné, mi változott. */
  const mozgasOk = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('a.dok-jog[href^="#"]').forEach((jel) => {
    const cel = document.getElementById(decodeURIComponent(jel.getAttribute('href').slice(1)));
    if (!cel) return;

    const buborek = document.createElement('span');
    buborek.className = 'sugo-buborek sugo-buborek-jog';
    /* A lábjegyzet szövege, a saját formázásával együtt (a jogszabály neve
       félkövér marad) — de hivatkozás nélkül: buborékban a link zsákutca. */
    buborek.innerHTML = cel.innerHTML.replace(/<a\b[^>]*>|<\/a>/g, '');
    buborek.setAttribute('aria-hidden', 'true');   // a horgony neve úgyis a szám
    jel.append(buborek);

    jel.addEventListener('click', (e) => {
      if (!mozgasOk) return;                       // hagyjuk a natív ugrást
      e.preventDefault();
      /* A `:target` állapot a hash-ből jön, ezért azt is beállítjuk — de a
         görgetést mi végezzük, simán. */
      history.replaceState(null, '', '#' + cel.id);
      cel.scrollIntoView({ behavior: 'smooth', block: 'center' });
      /* Az animáció újraindítása, ha ugyanarra a lábjegyzetre kattintanak
         kétszer: az osztály levétele-visszatétele nélkül a `:target` nem
         változna, és a villanás elmaradna. */
      cel.classList.remove('is-villan');
      void cel.offsetWidth;
      cel.classList.add('is-villan');
    });
  });

})();
