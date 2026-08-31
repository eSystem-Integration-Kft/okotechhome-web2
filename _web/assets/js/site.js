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
  /* A FIÓK saját töréspontja — TÁGABB, mint a tableté, és EGYEZNIE KELL az
     app.css `@media (max-width:1240px)` blokkjával. Ha a kettő elcsúszik, a
     köztes szélességeken a `details` nyitva marad, miközben a CSS már panelként
     jeleníti meg: a menü tartalma kattintás nélkül kilóg a lapra. */
  const navSzeles = window.matchMedia('(min-width: 1241px)');

  /* ---------------------------------------------------------------- 1) Menü */
  /* A `details` a markupban NYITVA áll: JS nélkül a menü látható és használható.
     Itt csak annyi történik, hogy szűk nézetben becsukjuk — a nyitás-zárás
     magát a natív elem végzi. */
  const drawer = document.querySelector('.nav-drawer');

  if (drawer) {
    const syncDrawer = () => { drawer.open = navSzeles.matches; };
    syncDrawer();
    navSzeles.addEventListener('change', syncDrawer);

    document.addEventListener('click', (event) => {
      if (!navSzeles.matches && drawer.open && !drawer.contains(event.target)) {
        drawer.open = false;
      }
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && !navSzeles.matches && drawer.open) {
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
    navSzeles.addEventListener('change', () => closeAll());
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
  const guardPlayback = (video) => {
    let visibleInViewport = true;

    const update = () => {
      const shouldPlay = visibleInViewport && document.visibilityState === 'visible';
      if (shouldPlay && video.paused) video.play().catch(() => {});
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
    video.addEventListener('canplay', () => {
      video.play().then(
        () => { video.dataset.ready = ''; guardPlayback(video); },
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
