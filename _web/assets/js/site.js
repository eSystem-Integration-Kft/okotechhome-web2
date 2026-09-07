/* =============================================================================
   ÖkoTech Home — Test2 · site.js
   -----------------------------------------------------------------------------
   Designrendszer 0.7: „Nincs framework. Natív HTML-elem és vanilla JS.
   A viselkedést nem újraépítjük, hanem a platformtól kérjük."

   Két viselkedés, mindkettő progressive enhancement — JS nélkül az oldal teljes
   értékű marad:
     1) a navigációs panel szűk nézetben csukva indul (a markupban nyitva áll),
     2) a hero állóképe fölé asztali nézetben videó kerül.
   ============================================================================= */

(() => {
  'use strict';

  const wide = window.matchMedia('(min-width: 1025px)');

  /* ---------------------------------------------------------------- 1) Menü */
  /* A `details` a markupban NYITVA áll: JS nélkül a menü látható és használható.
     Itt csak annyi történik, hogy szűk nézetben becsukjuk — a nyitás-zárás
     magát a natív elem végzi. */
  const drawer = document.querySelector('.nav-drawer');

  if (drawer) {
    const syncDrawer = () => { drawer.open = wide.matches; };
    syncDrawer();
    wide.addEventListener('change', syncDrawer);

    document.addEventListener('click', (event) => {
      if (!wide.matches && drawer.open && !drawer.contains(event.target)) {
        drawer.open = false;
      }
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && !wide.matches && drawer.open) {
        drawer.open = false;
        const toggle = drawer.querySelector('summary');
        if (toggle) toggle.focus();
      }
    });
  }

  /* ------------------------------------------------------------ 2) Megamenü */
  /* A panelek `hidden` attribútummal zárnak — JS nélkül egyik sem marad nyitva.
     Egyszerre csak egy lehet nyitva; Esc és a panelen kívüli kattintás zár. */
  const triggers = Array.from(document.querySelectorAll('.nav-trigger'));

  if (triggers.length) {
    const panelOf = (t) => document.getElementById(t.getAttribute('aria-controls'));

    const closeAll = (except) => {
      triggers.forEach((t) => {
        if (t === except) return;
        t.setAttribute('aria-expanded', 'false');
        const p = panelOf(t);
        if (p) p.hidden = true;
      });
    };

    triggers.forEach((t) => {
      t.addEventListener('click', () => {
        const isOpen = t.getAttribute('aria-expanded') === 'true';
        closeAll(t);
        t.setAttribute('aria-expanded', String(!isOpen));
        const p = panelOf(t);
        if (p) p.hidden = isOpen;
      });
    });

    document.addEventListener('keydown', (event) => {
      if (event.key !== 'Escape') return;
      const open = triggers.find((t) => t.getAttribute('aria-expanded') === 'true');
      if (!open) return;
      closeAll();
      open.focus();
    });

    document.addEventListener('click', (event) => {
      if (!event.target.closest('.nav-item')) closeAll();
    });

    /* Nézetváltásnál (asztali ⇄ szűk) a nyitott panel bezár, mert a
       pozicionálása is más. */
    wide.addEventListener('change', () => closeAll());
  }

  /* ---------------------------------------------------------- 3) Hero videó */
  /* A videót a HTML nem tartalmazza, mert három esetben nem szabad letölteni:
     szűk nézetben (a mozgókép ott nem olvasható, és 1,4 MB mobilforgalom),
     `prefers-reduced-motion` mellett, és adattakarékos módban. Ilyenkor a
     hero állóképe marad — az a végállapot, nem helyőrző. */
  const media = document.querySelector('[data-hero-video]');
  if (!media) return;

  const motionOk = window.matchMedia('(prefers-reduced-motion: no-preference)').matches;
  const saveData = Boolean(navigator.connection && navigator.connection.saveData);
  if (!wide.matches || !motionOk || saveData) return;

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
