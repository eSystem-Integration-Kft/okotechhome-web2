/* =============================================================================
   ÖkoTech Home — Test2 · kalauz.js
   „Öko" — a lapokon végigkísérő segéd
   -----------------------------------------------------------------------------
   MI EZ. Egy kis figura a jobb alsó sarokban, aki bejelentkezik, és segít
   megtalálni a tartalmat: keresésre megmutatja, MELYIK oldalon van a válasz,
   a talált szakaszt kiemeli a lapon, és tovább is viszi a látogatót.

   A FIGURA a termékből jön: az Épureco tartály sziluettje — bordázott test, két
   aknanyak — szemekkel. Nem rajzfilmfigura: a tekintet nyugodt, nincs vigyor és
   nincs pörgés. A cég komoly dolgot ad el, a segéd ehhez igazodik.

   HÁROM ÜZEMMÓD, mert nem minden lapon ugyanaz a dolga:
     · `kalauz`  — alapértelmezés: keresés és útbaigazítás a tartalomban.
     · `urlap`   — a konzultációkérőn: nem terel el, csak a kitöltésnél segít.
     · `jelentes`— az ajánlat-összehasonlítási jelentésen: ott a saját eredményét
                   magyarázza, nem a webhely tartalmát keresi.
   Az üzemmódot a `<body data-kalauz-mod>` mondja meg; ha hiányzik, `kalauz`.

   AMIT SZÁNDÉKOSAN NEM CSINÁL. Nem ugrik a látogató elé: első alkalommal
   megvárja, amíg a lap megnyugszik, és egyetlen buborékkal jelentkezik be.
   Aki bezárja, annak a munkamenet végéig nem szól újra. Csökkentett mozgás
   mellett minden animáció elmarad — a figura akkor egyszerűen ott van.
   ============================================================================= */

(() => {
  'use strict';

  if (document.querySelector('.oko')) return;                 // kétszer ne
  const TAROLO = 'oth-oko-elrejtve';
  const csokkentett = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const mod = document.body.dataset.kalauzMod || 'kalauz';

  /* --------------------------------------------------------------- a figura */
  /* Egyetlen inline SVG, mert a szemek külön mozognak: a pupilla a kurzor felé
     fordul, a szemhéj pislog. Külső fájlból ezek nem volnának elérhetők. */
  const FIGURA = `
<svg class="oko-figura" viewBox="0 0 100 104" role="img" aria-hidden="true" focusable="false">
  <ellipse class="oko-arnyek" cx="50" cy="98" rx="30" ry="5"/>
  <g class="oko-test-csoport">
    <!-- aknanyakak: a tartály két búvónyílása, egyben a figura „füle" -->
    <rect class="oko-nyak" x="24" y="10" width="16" height="14" rx="4"/>
    <rect class="oko-nyak" x="60" y="10" width="16" height="14" rx="4"/>
    <rect class="oko-fedel" x="21" y="6" width="22" height="7" rx="3.5"/>
    <rect class="oko-fedel" x="57" y="6" width="22" height="7" rx="3.5"/>
    <!-- test: a bordázott tartály lekerekítve -->
    <rect class="oko-test" x="10" y="20" width="80" height="74" rx="24"/>
    <!-- bordák: a termék legjellegzetesebb jegye, halványan -->
    <g class="oko-bordak">
      <path d="M20 40v34M28 34v46M72 34v46M80 40v34"/>
    </g>
    <!-- szemek -->
    <g class="oko-szem" data-oko-szem>
      <ellipse class="oko-szemfeher" cx="38" cy="52" rx="11" ry="12"/>
      <circle class="oko-pupilla" data-oko-pupilla cx="38" cy="52" r="5.4"/>
      <circle class="oko-csillanas" cx="35.6" cy="49" r="1.9"/>
      <rect class="oko-hej" data-oko-hej x="26" y="38" width="24" height="0" rx="2"/>
    </g>
    <g class="oko-szem" data-oko-szem>
      <ellipse class="oko-szemfeher" cx="62" cy="52" rx="11" ry="12"/>
      <circle class="oko-pupilla" data-oko-pupilla cx="62" cy="52" r="5.4"/>
      <circle class="oko-csillanas" cx="59.6" cy="49" r="1.9"/>
      <rect class="oko-hej" data-oko-hej x="50" y="38" width="24" height="0" rx="2"/>
    </g>
    <!-- a be- és kimenő csonk: a tartály oldalán, apró jelzésként -->
    <rect class="oko-csonk" x="4" y="44" width="8" height="7" rx="3.5"/>
    <rect class="oko-csonk" x="88" y="44" width="8" height="7" rx="3.5"/>
  </g>
</svg>`;

  const SZOVEG = {
    kalauz: {
      koszon: 'Segítsek megtalálni, amit keres?',
      sug: 'Írja be, mi a kérdése — megmutatom, melyik oldalon van a válasz.',
      helyorzo: 'Például: mekkora telek kell hozzá?',
    },
    urlap: {
      koszon: 'Ha elakad a kitöltésben, szóljon.',
      sug: 'Kérdezzen bátran bármelyik mezőről — azt is megmondom, mit érdemes előkészíteni.',
      helyorzo: 'Például: mit írjak a csúcsterheléshez?',
    },
    jelentes: {
      koszon: 'Segítek értelmezni az összehasonlítást.',
      sug: 'Kérdezzen a jelentés bármelyik soráról — elmondom, mit jelent és mire érdemes figyelni.',
      helyorzo: 'Például: miért tér el a két ár?',
    },
  }[mod] || {};

  /* ------------------------------------------------------------ a felület */
  const gyoker = document.createElement('div');
  gyoker.className = 'oko';
  gyoker.dataset.okoMod = mod;
  gyoker.innerHTML = `
    <div class="oko-buborek" data-oko-buborek role="status" aria-live="polite" hidden>
      <p class="type-ui-caption oko-buborek-szoveg" data-oko-buborek-szoveg></p>
      <button type="button" class="oko-buborek-zar" data-oko-zar aria-label="Bezárás">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg>
      </button>
    </div>

    <button type="button" class="oko-gomb" data-oko-gomb
            aria-expanded="false" aria-controls="oko-panel">
      ${FIGURA}
      <span class="oko-rejtett">Öko — segéd megnyitása</span>
    </button>

    <div class="oko-panel" id="oko-panel" data-oko-panel role="dialog"
         aria-label="Öko — segéd" hidden>
      <div class="oko-panel-fej">
        <span class="oko-panel-jel" aria-hidden="true">${FIGURA}</span>
        <div class="oko-panel-cimek">
          <p class="type-ui-subtitle oko-panel-cim">Öko</p>
          <p class="type-ui-caption oko-panel-alcim" data-oko-alcim></p>
        </div>
        <button type="button" class="oko-panel-zar" data-oko-panel-zar aria-label="Bezárás">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg>
        </button>
      </div>
      <div class="oko-tarsalgas" data-oko-tarsalgas></div>
      <form class="oko-urlap" data-oko-urlap>
        <label class="oko-rejtett" for="oko-kerdes">Kérdés</label>
        <input class="oko-input" id="oko-kerdes" type="text" autocomplete="off"
               data-oko-input maxlength="300">
        <button class="oko-kuld" type="submit" aria-label="Küldés">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h14M13 6l6 6-6 6"/></svg>
        </button>
      </form>
    </div>`;
  document.body.appendChild(gyoker);

  const gomb = gyoker.querySelector('[data-oko-gomb]');
  const panel = gyoker.querySelector('[data-oko-panel]');
  const buborek = gyoker.querySelector('[data-oko-buborek]');
  const buborekSzoveg = gyoker.querySelector('[data-oko-buborek-szoveg]');
  const tarsalgas = gyoker.querySelector('[data-oko-tarsalgas]');
  const urlap = gyoker.querySelector('[data-oko-urlap]');
  const input = gyoker.querySelector('[data-oko-input]');
  gyoker.querySelector('[data-oko-alcim]').textContent = SZOVEG.sug || '';
  input.placeholder = SZOVEG.helyorzo || '';

  /* ------------------------------------------------------------- bejövetel */
  /* Nem az első pillanatban jelenik meg: a lap előbb nyugodjon meg, hogy a
     figura ne a betöltés zajába érkezzen. Aki egyszer elküldte, annak a
     munkamenet végéig nem jelentkezik újra. */
  const elrejtve = (() => { try { return sessionStorage.getItem(TAROLO) === '1'; } catch { return false; } })();
  if (!elrejtve) {
    setTimeout(() => {
      gyoker.classList.add('is-erkezik');
      if (SZOVEG.koszon && !panelNyitva()) {
        buborekSzoveg.textContent = SZOVEG.koszon;
        buborek.hidden = false;
        // A buborék magától elmegy: aki nem foglalkozik vele, ne kelljen bezárnia.
        setTimeout(() => { if (!panelNyitva()) buborek.hidden = true; }, 9000);
      }
    }, csokkentett ? 200 : 1600);
  } else {
    gyoker.classList.add('is-erkezik');
  }

  /* ------------------------------------------------------------ pislogás */
  const hejak = [...gyoker.querySelectorAll('[data-oko-hej]')];
  function pislog() {
    hejak.forEach((h) => h.classList.add('is-csukva'));
    setTimeout(() => hejak.forEach((h) => h.classList.remove('is-csukva')), 130);
  }
  if (!csokkentett) {
    /* Szabálytalan ütem: az egyenletes pislogás gépies. */
    (function utemez() {
      setTimeout(() => { pislog(); utemez(); }, 2600 + Math.random() * 4200);
    })();
  }

  /* ------------------------------------------------- a tekintet követése */
  /* A pupilla a kurzor felé fordul, de csak keveset: a nagy kilengés bandzsít.
     Érintőképernyőn nincs kurzor, ott a szem középen marad. */
  if (!csokkentett && matchMedia('(pointer: fine)').matches) {
    const pupillak = [...gyoker.querySelectorAll('[data-oko-pupilla]')];
    const alap = pupillak.map((p) => ({ x: +p.getAttribute('cx'), y: +p.getAttribute('cy') }));
    let varakozik = false;
    addEventListener('pointermove', (e) => {
      if (varakozik) return;
      varakozik = true;
      requestAnimationFrame(() => {
        varakozik = false;
        const d = gomb.getBoundingClientRect();
        const kx = d.left + d.width / 2;
        const ky = d.top + d.height / 2;
        const szog = Math.atan2(e.clientY - ky, e.clientX - kx);
        const tav = Math.min(2.6, Math.hypot(e.clientX - kx, e.clientY - ky) / 60);
        pupillak.forEach((p, i) => {
          p.setAttribute('cx', String(alap[i].x + Math.cos(szog) * tav));
          p.setAttribute('cy', String(alap[i].y + Math.sin(szog) * tav));
        });
      });
    }, { passive: true });
  }

  /* --------------------------------------------------------- nyit és zár */
  function panelNyitva() { return !panel.hidden; }
  function nyit() {
    buborek.hidden = true;
    panel.hidden = false;
    gomb.setAttribute('aria-expanded', 'true');
    gyoker.classList.add('is-nyitva');
    if (!tarsalgas.children.length) uzenet('oko', SZOVEG.sug || '');
    input.focus();
  }
  function zar() {
    panel.hidden = true;
    gomb.setAttribute('aria-expanded', 'false');
    gyoker.classList.remove('is-nyitva');
    gomb.focus();
  }
  gomb.addEventListener('click', () => (panelNyitva() ? zar() : nyit()));
  gyoker.querySelector('[data-oko-panel-zar]').addEventListener('click', zar);
  gyoker.querySelector('[data-oko-zar]').addEventListener('click', () => {
    buborek.hidden = true;
    try { sessionStorage.setItem(TAROLO, '1'); } catch { /* privát mód */ }
  });
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && panelNyitva()) zar(); });

  /* ------------------------------------------------------------- üzenetek */
  function uzenet(kitol, szoveg, talalatok) {
    const sor = document.createElement('div');
    sor.className = `oko-uzenet oko-uzenet-${kitol}`;
    const p = document.createElement('p');
    p.className = 'type-ui-caption oko-uzenet-szoveg';
    p.textContent = szoveg;
    sor.appendChild(p);

    if (talalatok && talalatok.length) {
      const lista = document.createElement('ul');
      lista.className = 'oko-talalatok';
      talalatok.slice(0, 4).forEach((t) => {
        const li = document.createElement('li');
        const a = document.createElement('a');
        a.className = 'oko-talalat';
        a.href = t.url;
        a.textContent = t.cim;
        if (t.reszlet) {
          const kis = document.createElement('span');
          kis.className = 'oko-talalat-reszlet';
          kis.textContent = t.reszlet;
          a.appendChild(kis);
        }
        /* Ha a találat EZEN a lapon van, nem navigálunk: odagörgetünk és
           kiemeljük. A látogató így látja, hogy hol volt a válasz. */
        if (t.horgony) {
          a.addEventListener('click', (e) => {
            const cel = document.querySelector(t.horgony);
            if (!cel) return;                       // más lapon van: menjen a link
            e.preventDefault();
            kiemel(cel);
          });
        }
        li.appendChild(a);
        lista.appendChild(li);
      });
      sor.appendChild(lista);
    }
    tarsalgas.appendChild(sor);
    tarsalgas.scrollTop = tarsalgas.scrollHeight;
    return sor;
  }

  /* --------------------------------------------------------- kiemelés */
  /* A megtalált szakaszt nem elég odagörgetni: a lapon meg is kell mutatni,
     különben a látogató a szöveg közepén találja magát és keresgél tovább. */
  let kiemeltElem = null;
  function kiemel(cel) {
    if (kiemeltElem) kiemeltElem.classList.remove('oko-kiemelt');
    cel.classList.add('oko-kiemelt');
    kiemeltElem = cel;
    cel.scrollIntoView({ behavior: csokkentett ? 'auto' : 'smooth', block: 'center' });
    setTimeout(() => cel.classList.remove('oko-kiemelt'), 4000);
  }

  /* --------------------------------------------------------------- kérdés */
  let dolgozik = false;
  urlap.addEventListener('submit', async (e) => {
    e.preventDefault();
    const kerdes = input.value.trim();
    if (!kerdes || dolgozik) return;
    uzenet('en', kerdes);
    input.value = '';
    dolgozik = true;
    gyoker.classList.add('is-gondolkodik');
    const varakozo = uzenet('oko', 'Megnézem…');

    try {
      const valasz = await fetch('api/kalauz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kerdes, mod, oldal: location.pathname }),
      });
      const eredmeny = await valasz.json();
      varakozo.remove();
      if (!valasz.ok || !eredmeny.ok) throw new Error(eredmeny.uzenet || '');
      uzenet('oko', eredmeny.valasz || '', eredmeny.talalatok);
    } catch {
      varakozo.remove();
      uzenet('oko', 'Most nem érem el a keresőt. A menü Tudástár pontja alatt megtalálja a témákat, vagy hívjon minket: +36 33 200 211.');
    } finally {
      dolgozik = false;
      gyoker.classList.remove('is-gondolkodik');
      input.focus();
    }
  });
})();
