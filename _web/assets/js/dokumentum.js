/* =============================================================================
   ÖkoTech Home — Test2 · dokumentum.js
   Okirat-oldalak segédje: nyomtatás és mellékletek
   -----------------------------------------------------------------------------
   Két apró viselkedés, mindkettő progressive enhancement — JS nélkül az oldal
   teljes értékű marad:

     1) NYOMTATÁS. A gomb a böngésző saját nyomtatási párbeszédét nyitja meg
        (onnan PDF-be is menthető). JS nélkül a gomb elrejtve marad, mert a
        `Ctrl/⌘+P` amúgy is működik — hamis gombot nem mutatunk.

     2) MELLÉKLETEK. A natív fájlválasztó csak annyit ír ki, hogy „3 fájl".
        Itt kiírjuk a NEVÜKET és a MÉRETÜKET, és azonnal szólunk, ha valami
        túllépi a korlátot — nem a beküldés után, a szerver válaszából.
        A korlátok a szerverrel egyeznek (api/lib/vedelem.php `fajl`).
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

  /* ------------------------------------------------------------ mellékletek */
  const MAX_DARAB = 3;
  const MAX_MERET = 10 * 1024 * 1024;

  const meret = (b) => (b < 1024 ? b + ' B'
    : b < 1048576 ? Math.round(b / 1024) + ' KB'
    : (b / 1048576).toFixed(1).replace('.', ',') + ' MB');

  document.querySelectorAll('[data-urlap-fajl]').forEach((mezo) => {
    const lista = document.createElement('ul');
    lista.className = 'urlap-fajl-lista';
    /* A lista ÉLŐ régió: a képernyőolvasó felolvassa, mi került be és mi a baj
       vele — enélkül a nem látó felhasználó csak a beküldéskor tudná meg. */
    lista.setAttribute('aria-live', 'polite');
    mezo.insertAdjacentElement('afterend', lista);

    const rajzol = () => {
      lista.textContent = '';
      const fajlok = Array.from(mezo.files || []);
      let hiba = '';

      if (fajlok.length > MAX_DARAB) {
        hiba = `Legfeljebb ${MAX_DARAB} fájl csatolható — most ${fajlok.length} van kiválasztva.`;
      }

      fajlok.forEach((f) => {
        const li = document.createElement('li');
        const nev = document.createElement('span');
        nev.className = 'type-ui-caption';
        nev.textContent = f.name;
        const m = document.createElement('span');
        m.className = 'type-ui-caption urlap-fajl-meret';
        m.textContent = meret(f.size);
        if (f.size > MAX_MERET) {
          li.classList.add('urlap-fajl-hiba');
          m.textContent += ' — túl nagy';
          hiba = hiba || 'Egy fájl legfeljebb 10 MB lehet.';
        }
        li.append(nev, m);
        lista.append(li);
      });

      if (hiba) {
        const li = document.createElement('li');
        li.className = 'type-ui-caption urlap-fajl-hiba';
        li.textContent = hiba;
        lista.append(li);
        /* A natív ellenőrzés így a beküldést is megállítja — nem kell külön
           kezelő az űrlapra, és JS nélkül a szerver mondja ugyanezt. */
        mezo.setCustomValidity(hiba);
      } else {
        mezo.setCustomValidity('');
      }
    };

    mezo.addEventListener('change', rajzol);
  });
})();
