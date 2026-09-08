/* =============================================================================
   ÖkoTech Home — Test2 · site.js
   -----------------------------------------------------------------------------
   Designrendszer 0.7: „Nincs framework. Natív HTML-elem és vanilla JS.
   A viselkedést nem újraépítjük, hanem a platformtól kérjük."

   Három viselkedés, mind progressive enhancement — JS nélkül az oldal teljes
   értékű marad (a fejléc olyankor a médialekérdezésre támaszkodik):
     1) a menüsor sűrűségét MÉRÉS választja: elfér-e egy sorban, és ha igen,
        milyen fokozattal — ha sehogy sem, lenyitható fiók lesz belőle,
     2) a megamenü egérrel ráállásra nyílik (szándék-küszöbbel), kattintásra és
        billentyűvel változatlanul,
     3) a hero állóképe fölé asztali nézetben videó kerül.
   ============================================================================= */

(() => {
  'use strict';

  const gyoker = document.documentElement;

  /* ---------------------------------------------------------------- 1) Menü */
  /* A `details` a markupban NYITVA áll: JS nélkül a menü látható és használható.
     Két dolog történik itt:
       · MÉRÉS — elfér-e a menüsor egyetlen sorban, és ha igen, milyen
         sűrűséggel (app.css: „A menüsor sűrűségi fokozatai");
       · a fiók nyitás-zárását magát a natív `details` végzi. */
  const drawer = document.querySelector('.nav-drawer');
  const navLista = document.querySelector('.nav-list');
  const fejlecSor = document.querySelector('.header-inner');

  /* A fokozatok a legtágabbtól a legszűkebbig. A negyedik állapot — a fiók —
     nem fokozat: ott már nincs sor. */
  const FOKOZATOK = ['tag', 'tomor', 'suru'];
  const fiokMod = () => gyoker.dataset.nav === 'fiok';

  /* MÉRÉS, NEM TÖRÉSPONT. Egy fix képpontérték a MAI menüre igaz; a következő
     menüpont után már nem az. Ezért a szkript sorra felveszi a fokozatokat, és
     mindegyiknél MEGKÉRDEZI a böngészőt, elfér-e a sor — az elsőt tartja meg,
     amelyik igen. Ha egyik sem, jön a fiók.

     A próbálgatás egyetlen feladaton belül fut, festés nélkül: a látogató nem
     lát belőle semmit, csak a végeredményt. */
  const ferElASor = () => {
    const st = getComputedStyle(fejlecSor);
    const belso = fejlecSor.clientWidth
      - parseFloat(st.paddingLeft) - parseFloat(st.paddingRight);
    const res = parseFloat(st.columnGap) || 0;
    let masok = 0;
    for (const gyerek of fejlecSor.children) {
      if (gyerek !== drawer) masok += gyerek.getBoundingClientRect().width;
    }
    const szabad = belso - masok - res * (fejlecSor.children.length - 1);
    /* A menüsor NEM tud összenyomódni (`nowrap` + `min-width:auto`), ezért a
       kirajzolt szélessége egyben a szükséges szélesség is. A `scrollWidth`
       csak biztosíték arra az esetre, ha egyszer mégis zsugorodna. */
    const kell = Math.max(navLista.scrollWidth,
                          navLista.getBoundingClientRect().width);
    return kell <= szabad + 0.5;
  };

  const fokozatValaszt = () => {
    if (!drawer || !navLista || !fejlecSor) return;
    const elozoFiok = fiokMod();
    const nyitvaVolt = drawer.open;

    /* Csukott `details` tartalma nem mérhető — a mérés idejére kinyitjuk. */
    drawer.open = true;
    let talalt = null;
    for (const fokozat of FOKOZATOK) {
      gyoker.dataset.nav = fokozat;
      if (ferElASor()) { talalt = fokozat; break; }
    }
    gyoker.dataset.nav = talalt || 'fiok';

    /* A fiók csukva indul; ha már fiók módban voltunk, a látogató döntése
       marad érvényben (átméretezés közben ne csukódjon be a nyitott menü). */
    drawer.open = talalt ? true : (elozoFiok ? nyitvaVolt : false);
    if (!talalt !== elozoFiok) zarMind();
  };

  if (drawer) {
    /* Az átméretezés összevonva — a mérés három kényszerített újratördelés,
       ezt nem érdemes minden eseményre lefuttatni. Időzítő, nem `rAF`: a
       képkocka-hívás háttérfülben és nem festett kereten egyszerűen nem szólal
       meg, és a fejléc a rossz fokozatban ragadna, amíg vissza nem térnek. */
    let utemezve = 0;
    const ujramer = () => {
      clearTimeout(utemezve);
      utemezve = setTimeout(fokozatValaszt, 90);
    };
    window.addEventListener('resize', ujramer);
    /* A BETŰ SZÉLESSÉGE DÖNT, a webfont pedig később érkezik, mint a mérés:
       a tartalék betűvel mért sor akár 5-8%-kal is más. Ezért a font
       betöltése után újramérünk. */
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(ujramer).catch(() => {});
    }

    document.addEventListener('click', (event) => {
      if (fiokMod() && drawer.open && !drawer.contains(event.target)) {
        drawer.open = false;
      }
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && fiokMod() && drawer.open) {
        drawer.open = false;
        const toggle = drawer.querySelector('summary');
        if (toggle) toggle.focus();
      }
    });
  }

  /* ------------------------------------------------------------ 2) Megamenü */
  /* A panelek `hidden` attribútummal zárnak — JS nélkül egyik sem marad nyitva.
     Egyszerre csak egy lehet nyitva; Esc és a panelen kívüli kattintás zár.

     NYITÁS EGÉRREL: ráállásra. Ez az elvárt viselkedés egy megamenütől, és a
     nyilak elhagyása után ez az egyetlen mód, hogy a panel kérés nélkül
     megmutatkozzon. Három részlet választja el a használhatót a bosszantótól:

       · SZÁNDÉK-KÜSZÖB — a menüsor fölött ÁTHALADÓ egér ne nyisson panelt.
         Ezért a nyitás 120 ms késleltetéssel indul, és a menüpont elhagyása
         törli.
       · TÜRELEM ZÁRÁSKOR — a menüpont és a panel között 16 képpontnyi rés van;
         amíg az egér ezt átszeli, egyik elem fölött sincs. 260 ms türelem
         nélkül a panel az orra előtt csukódna be.
       · AZONNALI VÁLTÁS — ha már nyitva van egy panel, a szomszéd menüpontra
         érve nincs mit „szándékozni": a panel azonnal vált, csak átúszik.

     Érintésre és billentyűvel mindez nem működik és nem is kell: ott a
     kattintás (Enter/Space) nyit. A `pointerenter` szűri a nem-egér eszközöket,
     a médialekérdezés pedig a hover nélküli környezeteket. */
  const triggers = Array.from(document.querySelectorAll('.nav-trigger'));
  const panelOf = (t) => document.getElementById(t.getAttribute('aria-controls'));

  const zarMind = (kiveve) => {
    triggers.forEach((t) => {
      if (t === kiveve) return;
      t.setAttribute('aria-expanded', 'false');
      const p = panelOf(t);
      if (p) p.hidden = true;
    });
  };

  if (triggers.length) {
    const NYITAS_KESLELTETES = 120;
    const ZARAS_TURELEM = 260;
    const VALTAS_JELOLES = 280;

    const finomMutato = window.matchMedia('(hover:hover) and (pointer:fine)');
    let nyitoIdozito = 0;
    let zaroIdozito = 0;
    let valtoIdozito = 0;
    /* Kattintással zárt panel ne nyíljon vissza rögtön a hoverre: az egér még
       a menüponton áll. A tiltás a menüpont elhagyásáig él. */
    let hoverTiltas = null;

    const nyitva = () => triggers.find((t) => t.getAttribute('aria-expanded') === 'true');

    const nyit = (t) => {
      const elozo = nyitva();
      if (elozo === t) return;
      /* Váltásnál a panel nem csúszik le újra, csak átúszik (app.css). */
      if (elozo) {
        gyoker.dataset.navValt = '';
        clearTimeout(valtoIdozito);
        valtoIdozito = setTimeout(() => { delete gyoker.dataset.navValt; }, VALTAS_JELOLES);
      }
      zarMind(t);
      t.setAttribute('aria-expanded', 'true');
      const p = panelOf(t);
      if (p) p.hidden = false;
    };

    const zar = () => zarMind();

    const idozitokTorlese = () => {
      clearTimeout(nyitoIdozito);
      clearTimeout(zaroIdozito);
    };

    triggers.forEach((t) => {
      const elem = t.closest('.nav-item');

      t.addEventListener('click', () => {
        idozitokTorlese();
        if (t.getAttribute('aria-expanded') === 'true') { zar(); hoverTiltas = t; }
        else nyit(t);
      });

      if (!elem) return;

      /* A panel a `.nav-item` GYEREKE, ezért a fölötte álló egér is „a
         menüponton belül" van — a `pointerleave` csak akkor szólal meg, ha a
         mutató mindkettőt elhagyta. */
      elem.addEventListener('pointerenter', (event) => {
        if (event.pointerType !== 'mouse' || !finomMutato.matches || fiokMod()) return;
        idozitokTorlese();
        if (hoverTiltas === t) return;
        if (nyitva()) nyit(t);
        else nyitoIdozito = setTimeout(() => nyit(t), NYITAS_KESLELTETES);
      });

      elem.addEventListener('pointerleave', (event) => {
        if (event.pointerType !== 'mouse' || !finomMutato.matches || fiokMod()) return;
        if (hoverTiltas === t) hoverTiltas = null;
        idozitokTorlese();
        zaroIdozito = setTimeout(zar, ZARAS_TURELEM);
      });

      /* Billentyűzet: ha a fókusz elhagyja a menüpontot (és vele a panelt), a
         panel bezár — különben a látogató „mögötte" tabolna tovább a lapon. */
      elem.addEventListener('focusout', (event) => {
        if (elem.contains(event.relatedTarget)) return;
        if (t.getAttribute('aria-expanded') === 'true') zar();
      });
    });

    document.addEventListener('keydown', (event) => {
      if (event.key !== 'Escape') return;
      const open = nyitva();
      if (!open) return;
      idozitokTorlese();
      zar();
      open.focus();
    });

    document.addEventListener('click', (event) => {
      if (!event.target.closest('.nav-item')) zar();
    });
  }

  /* A mérés csak azután futhat, hogy a megamenü zárófüggvénye (`zarMind`)
     létezik: módváltáskor azt hívja. */
  fokozatValaszt();

  /* ---------------------------------------------------------- 3) Hero videó */
  /* A videót a HTML nem tartalmazza, mert három esetben nem szabad letölteni:
     szűk nézetben (a mozgókép ott nem olvasható, és 1,4 MB mobilforgalom),
     `prefers-reduced-motion` mellett, és adattakarékos módban. Ilyenkor a
     hero állóképe marad — az a végállapot, nem helyőrző. */
  const media = document.querySelector('[data-hero-video]');
  if (!media) return;

  const motionOk = window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
  const saveData = Boolean(navigator.connection && navigator.connection.saveData);
  /* A videó KÉPERNYŐMÉRET kérdése, nem a menüé: a saját, változatlan
     töréspontját használja (1025px), nem a menüsor mért fokozatát. */
  const nagyKepernyo = window.matchMedia('(min-width: 1025px)');
  if (!nagyKepernyo.matches || !motionOk || saveData) return;

  /* A hurokban futó felvétel csak akkor játsszon, amikor tényleg látszik.
     Enélkül a böngésző a háttérben és görgetés után is dekódolja a képkockákat
     — hosszú munkamenetben ez memóriát és GPU-időt visz, és lassuláshoz,
     szélsőséges esetben a lap összeomlásához vezet. */
  /* LEJÁTSZÁSI SEBESSÉG. A felvétel eredeti tempója sietősebb, mint amit a
     hero nyugalma megkíván — lassítva a mozgás háttérré válik, nem vonja el a
     figyelmet a címsorról. Az érték a MARKUPBÓL jön (`data-video-sebesseg`),
     hogy hangoláshoz ne kelljen szkriptet nyitni.

     A korlátok nem önkényesek: 0,5 alatt a böngésző ugyanazt a képkockát
     tartja ki hosszan, és a folyamatos mozgás akadozásba vált át. */
  const SEBESSEG = Math.min(1.5, Math.max(0.5,
    parseFloat(media.dataset.videoSebesseg) || 0.75));

  /* A `playbackRate` nem ragad meg egyszer s mindenkorra: a forrás betöltése és
     egyes böngészők a lejátszás újraindításakor visszaállítják 1-re. Ezért nem
     elég egyszer beállítani — minden érintett ponton újra rátesszük. */
  const setSebesseg = (video) => { if (video.playbackRate !== SEBESSEG) video.playbackRate = SEBESSEG; };

  const guardPlayback = (video) => {
    let visibleInViewport = true;

    const update = () => {
      const shouldPlay = visibleInViewport && document.visibilityState === 'visible';
      if (shouldPlay && video.paused) { setSebesseg(video); video.play().catch(() => {}); }
      else if (!shouldPlay && !video.paused) video.pause();
    };

    if ('IntersectionObserver' in window) {
      new IntersectionObserver((entries) => {
        visibleInViewport = entries[0].isIntersecting;
        update();
      }, { threshold: 0.1 }).observe(video);
    }

    document.addEventListener('visibilitychange', update);
  };

  const startVideo = () => {
    const video = document.createElement('video');
    video.className = 'hero-video';
    video.muted = true;
    video.loop = true;
    video.playsInline = true;
    video.preload = 'auto';
    /* Attribútumként is: a Safari az autoplay-feltételt a MARKUPBÓL olvassa. */
    video.setAttribute('muted', '');
    video.setAttribute('playsinline', '');
    /* A felvétel dekoratív: ugyanazt mutatja, amit az állókép alt-szövege leír. */
    video.setAttribute('aria-hidden', 'true');
    video.tabIndex = -1;

    const addSource = (src, type) => {
      if (!src) return;
      const source = document.createElement('source');
      source.src = src;
      source.type = type;
      video.append(source);
    };
    addSource(media.dataset.videoWebm, 'video/webm');
    addSource(media.dataset.videoMp4, 'video/mp4');

    /* Csak akkor úszik be, ha tényleg elindult — különben az állókép marad. */
    /* A `loadedmetadata` az első pont, ahol a sebesség egyáltalán beállítható —
       előtte a médiaelem még nem tudja, mit játszik le. */
    video.addEventListener('loadedmetadata', () => setSebesseg(video));

    video.addEventListener('canplay', () => {
      setSebesseg(video);
      video.play().then(
        () => { video.dataset.ready = ''; setSebesseg(video); guardPlayback(video); },
        () => { video.remove(); }
      );
    }, { once: true });

    video.addEventListener('error', () => { video.remove(); }, { once: true });

    media.append(video);
  };

  /* A hero állóképe a LCP-elem: a videó csak utána kezd tölteni. */
  if (document.readyState === 'complete') startVideo();
  else window.addEventListener('load', startVideo, { once: true });
})();

/* ============================================================================
   FOLYAMATJELZŐ — a „Mi történik a jelentkezés után?" lépéssor
   ----------------------------------------------------------------------------
   A vonal balról jobbra kirajzolódik, a korongok sorban gyúlnak ki. A mozgás
   azt mondja el, hogy ez EGYMÁS UTÁN következő folyamat, nem négy párhuzamos
   tétel — ezért érdemes egyáltalán mozgatni.

   A JELÖLÉST EZ A MODUL TESZI RÁ, ÉS A MEGJELENÉSKOR VESZI LE. Enélkül —
   szkript nélkül, csökkentett mozgásnál, vagy ha az animációs óra áll — a
   lépéssor egyszerűen teljesen látszik. A láthatóság sosem függhet attól, hogy
   egy szkript lefutott-e.
   ========================================================================== */
(() => {
  'use strict';

  /* Ugyanaz a minta két helyen: a lépéssor és az üzemidő-sávok is a
     megjelenéskor rajzolódnak ki. A jelölést a SZKRIPT teszi rá és a
     megjelenéskor veszi le — így szkript nélkül, csökkentett mozgásnál és
     háttérfülben is minden a végállapotában látszik.

     HÁTTÉRFÜLBEN NEM REJTÜNK EL SEMMIT. Ha a lap betöltéskor nem látható —
     háttérfül, előrenderelés, képernyőkép-szolgáltató —, a böngésző nem
     kézbesíti a figyelő hívásait és nem is fest: a jelölés fent maradna, és a
     tartalom láthatatlan lenne egy olyan pillanatképen, amit senki nem tud
     „felébreszteni".

     IDŐZÍTETT BIZTONSÁGI HÁLÓ NINCS, és ez szándékos. Egy „néhány másodperc
     múlva mindenképp mutasd meg" időzítő KIOLTJA magát az animációt: a látogató
     addig még feljebb olvas. A figyelő pedig nem tud néma maradni — a callback
     minden megfigyelt elemre lefut egyszer, rögtön a megfigyelés után. */
  const belepteto = (elem, jeloles, kuszob) => {
    if (!elem || !('IntersectionObserver' in window)) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    if (document.visibilityState !== 'visible') return;

    elem.setAttribute(jeloles, '');
    const figyelo = new IntersectionObserver((b) => {
      if (b[0].isIntersecting) { elem.removeAttribute(jeloles); figyelo.disconnect(); }
    }, { threshold: kuszob });
    figyelo.observe(elem);
  };

  document.querySelectorAll('.uzemido').forEach((u) => belepteto(u, 'data-belep', 0.2));

  belepteto(document.querySelector('.utana-sin'), 'data-folyamat', 0.35);
})();
