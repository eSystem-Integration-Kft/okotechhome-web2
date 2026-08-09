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
<svg class="oko-figura" viewBox="0 0 100 108" role="img" aria-hidden="true" focusable="false">
  <ellipse class="oko-arnyek" cx="50" cy="103" rx="30" ry="4.5"/>
  <g class="oko-test-csoport">
    <!-- narancs be- és kimenő csonk, ahogy a terméken -->
    <rect class="oko-csonk" x="6" y="52" width="16" height="9" rx="4.5"/>
    <rect class="oko-csonk" x="78" y="45" width="16" height="9" rx="4.5"/>
    <!-- kúpos felsőrész -->
    <path class="oko-kup" d="M35 16h30l9 25H26z"/>
    <!-- perem a kúp és a henger között -->
    <rect class="oko-perem" x="21" y="40" width="58" height="6" rx="3"/>
    <!-- hengeres test -->
    <path class="oko-test" d="M23 46h54v40a10 10 0 0 1-10 10H33a10 10 0 0 1-10-10z"/>
    <!-- a test bal oldali íve: ettől lesz henger, nem doboz -->
    <path class="oko-test-arny" d="M23 46h9v50h-1a8 8 0 0 1-8-8z"/>
    <!-- szemek -->
    <g class="oko-szem">
      <ellipse class="oko-szemfeher" cx="41" cy="62" rx="10.5" ry="11.5"/>
      <circle class="oko-pupilla" data-oko-pupilla cx="41" cy="62" r="5.2"/>
      <circle class="oko-csillanas" cx="38.8" cy="59.2" r="1.8"/>
      <rect class="oko-hej" data-oko-hej x="29.5" y="48" width="23" height="0" rx="2"/>
    </g>
    <g class="oko-szem">
      <ellipse class="oko-szemfeher" cx="62" cy="62" rx="10.5" ry="11.5"/>
      <circle class="oko-pupilla" data-oko-pupilla cx="62" cy="62" r="5.2"/>
      <circle class="oko-csillanas" cx="59.8" cy="59.2" r="1.8"/>
      <rect class="oko-hej" data-oko-hej x="50.5" y="48" width="23" height="0" rx="2"/>
    </g>
    <!-- száj: egy nyugodt ív, nem vigyor -->
    <path class="oko-szaj" d="M43 82q8 7 16 0"/>
  </g>
</svg>`;

  const SZOVEG = {
    kalauz: {
      koszon: 'Segítsek megtalálni, amit keres?',
      sug: 'Mondja el, hol tart — megmutatom, melyik oldalon van a válasz, és mi a következő lépés.',
      helyorzo: 'Például: mekkora telek kell hozzá?',
      /* Kiindulás kattintásra. A legtöbb látogató nem tudja, mit kérdezzen —
         ezért Öko kínálja fel a négy leggyakoribb belépőt. */
      inditok: [
        'Nincs közcsatorna nálunk — mik a lehetőségeim?',
        'Honnan induljak el? Még csak tájékozódom.',
        'Alkalmas-e a telkem egyedi rendszerre?',
        'Meglévő emésztőt szeretnék kiváltani.',
      ],
    },
    urlap: {
      koszon: 'Ha elakad a kitöltésben, szóljon.',
      sug: 'Kérdezzen bátran bármelyik mezőről — azt is megmondom, mit érdemes előkészíteni.',
      helyorzo: 'Például: mit írjak a csúcsterheléshez?',
      inditok: [
        'Mit írjak, ha nem tudom a telek méretét?',
        'Mit jelent a csúcsterhelés?',
        'Milyen adatokat készítsek elő a konzultációra?',
      ],
    },
    jelentes: {
      koszon: 'Segítek értelmezni az összehasonlítást.',
      sug: 'Kérdezzen a jelentés bármelyik soráról — elmondom, mit jelent és mire érdemes figyelni.',
      helyorzo: 'Például: miért tér el a két ár?',
      inditok: [
        'Mire figyeljek az ajánlatok összevetésénél?',
        'Mi az, ami gyakran kimarad egy ajánlatból?',
        'Mit jelent, ha nagyon eltér a két ár?',
      ],
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

    <!-- A FÜL. Nem a sarokban álló gomb utazik ide: az ottani helyzetét a
         böngésző semmilyen úton nem engedte átírni (inline !important sem
         mozdította), ezért a fül külön elem, saját fix pozícióval. Így semmit
         sem örököl, és a becsúszása egyetlen transform. -->
    <button type="button" class="oko-ful" data-oko-ful
            aria-expanded="false" aria-controls="oko-panel" hidden>
      ${FIGURA}
      <span class="oko-rejtett">Öko — segéd (félrehúzva, megnyitás)</span>
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
  /* Öko MINDIG ott van — a bezárás a köszönő buborékra vonatkozik, nem a
     figurára. Aki nem kér a szövegből, attól elvesszük a buborékot, de a
     segéd elérhető marad: ez a dolga. */
  const buborekElrejtve = (() => { try { return sessionStorage.getItem(TAROLO) === '1'; } catch { return false; } })();
  setTimeout(() => {
    gyoker.classList.add('is-erkezik');
    if (SZOVEG.koszon && !buborekElrejtve && !panelNyitva()) {
      buborekSzoveg.textContent = SZOVEG.koszon;
      buborek.hidden = false;
      setTimeout(() => { if (!panelNyitva()) buborek.hidden = true; }, 9000);
    }
  }, csokkentett ? 200 : 1600);

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
        /* Minden figura a SAJÁT középpontjából néz — eddig mindegyik a sarokban
           álló gombhoz igazodott, így a panel fejlécében ülő Öko folyton
           félrenézett. */
        pupillak.forEach((p, i) => {
          const svg = p.closest('svg');
          if (!svg) return;
          const d = svg.getBoundingClientRect();
          if (!d.width) return;
          const kx = d.left + d.width / 2;
          const ky = d.top + d.height / 2;
          const szog = Math.atan2(e.clientY - ky, e.clientX - kx);
          const tav = Math.min(2.6, Math.hypot(e.clientX - kx, e.clientY - ky) / 60);
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
    fulre(true);                       // előbb félrevonul, hogy legyen helye
    panel.hidden = false;
    gomb.setAttribute('aria-expanded', 'true');
    gyoker.classList.add('is-nyitva');
    if (!tarsalgas.children.length && SZOVEG.sug) {
      const sor = uzenet('oko', SZOVEG.sug);
      javaslatok(SZOVEG.inditok, sor);
    }
    input.focus();
  }
  function zar() {
    panel.hidden = true;
    gomb.setAttribute('aria-expanded', 'false');
    gyoker.classList.remove('is-nyitva');
    fulre(false);                      // visszasétál a sarokba
    reflektorLe();
    gomb.focus();
  }
  gomb.addEventListener('click', () => (panelNyitva() ? zar() : nyit()));

  /* A figura a sarokból a jobb szél közepére vonul, és fül lesz belőle. A
     sarok így felszabadul, Öko viszont látható marad — a szemei kilógnak. */
  /* A helyzetet innen állítjuk, nem osztályból: a stíluslapon a szabály a
     többi `.oko-gomb` deklarációval versenyzett és alulmaradt, a figura pedig
     a sarokban ragadt. Az elemre írt érték minden szabályt megelőz, a CSS
     `transition` viszont ugyanúgy animálja a két helyzet között. */
  /* A sarokban álló figura és a szélen ülő fül két KÜLÖN elem: egyszerre
     mindig csak az egyik látszik. A váltás így nem pozíció-animáció, hanem
     megjelenés — és az működik ott is, ahol a helyzet átírása nem. */
  const ful = gyoker.querySelector('[data-oko-ful]');
  function fulre(be) {
    gyoker.classList.toggle('is-ful', be);
    gomb.hidden = be;
    ful.hidden = !be;
  }
  ful.addEventListener('click', () => (panelNyitva() ? zar() : nyit()));
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

  /* Kattintható folytatás. A látogatónak nem kell kitalálnia, mit kérdezzen
     legközelebb — Öko megmutatja, merre érdemes tovább menni. */
  function javaslatok(lista, sor) {
    if (!lista || !lista.length) return;
    const doboz = document.createElement('div');
    doboz.className = 'oko-javaslatok';
    lista.slice(0, 3).forEach((szoveg) => {
      const gomb = document.createElement('button');
      gomb.type = 'button';
      gomb.className = 'oko-javaslat';
      gomb.textContent = szoveg;
      gomb.addEventListener('click', () => { doboz.remove(); kerdez(szoveg); });
      doboz.appendChild(gomb);
    });
    (sor || tarsalgas).appendChild(doboz);
    tarsalgas.scrollTop = tarsalgas.scrollHeight;
  }

  /* --------------------------------------------------------- kiemelés */
  /* A megtalált szakaszt nem elég odagörgetni: a lapon meg is kell mutatni,
     különben a látogató a szöveg közepén találja magát és keresgél tovább. */
  let fokuszElem = null;
  let fedo = null;
  let mutato = null;

  function reflektorLe() {
    if (fokuszElem) { fokuszElem.classList.remove('oko-fokusz'); fokuszElem = null; }
    if (fedo) { fedo.remove(); fedo = null; }
    if (mutato) { mutato.remove(); mutato = null; }
  }

  /* Nem elég odagörgetni: a lap többi részét visszavesszük, a megtalált
     szakaszt kiemeljük, és a kéz oda is mutat. A látogatónak egy pillanat
     alatt látnia kell, HOL a válasz. */
  function kiemel(cel) {
    reflektorLe();

    fedo = document.createElement('div');
    fedo.className = 'oko-reflektor';
    fedo.addEventListener('click', reflektorLe);
    document.body.appendChild(fedo);

    cel.classList.add('oko-fokusz');
    fokuszElem = cel;
    cel.scrollIntoView({ behavior: csokkentett ? 'auto' : 'smooth', block: 'center' });

    /* A kéz a görgetés UTÁN kerül a helyére: menet közben számolva mellétrafálna. */
    setTimeout(() => {
      if (!fokuszElem) return;
      const d = cel.getBoundingClientRect();
      mutato = document.createElement('div');
      mutato.className = 'oko-mutato is-koppint';
      mutato.innerHTML = '<svg viewBox="0 0 32 32" aria-hidden="true">'
        + '<path fill="#FBFBF7" stroke="#2C302C" stroke-width="1.6" stroke-linejoin="round"'
        + ' d="M11 5.5a2 2 0 0 1 4 0v8.2l1.2-2.1a2 2 0 0 1 3.5 2l-.6 1.1 1.6-.4a2 2 0 0 1 1 3.9l-1.2.3 1 .6a2 2 0 0 1-1.4 3.7l-4.4-1.1a7 7 0 0 1-4.6-4L11 14z"/>'
        + '</svg>';
      mutato.style.left = Math.max(8, Math.min(innerWidth - 46, d.right - 24)) + 'px';
      mutato.style.top = Math.max(8, d.top + Math.min(d.height / 2, 120)) + 'px';
      document.body.appendChild(mutato);
    }, csokkentett ? 0 : 480);

    /* Magától elenged: a reflektor nem maradhat a lapon. */
    setTimeout(reflektorLe, 7000);
  }

  addEventListener('keydown', (e) => { if (e.key === 'Escape') reflektorLe(); });

  /* ------------------------------------------------------------- kísérő */
  /* Az űrlapon Öko nem keres, hanem VÉGIGKÍSÉR: minden laphoz megmondja, mit
     várunk, mit tud belőle automatikusan kitölteni, és mutat rá példát. A
     szöveg a lapváltás eseményére frissül, és a váltás látszik is. */
  const KISERO = [
    null,
    { cim: 'Ki keres megoldást?',
      mit: 'Jelölje meg, magánszemélyként vagy szervezet nevében keres megoldást. Ettől függ minden további kérdés.',
      pelda: 'Vállalkozásnál a létesítmény típusa is kell — panzió, étterem, iskola, üzem.',
      auto: 'A leírásból ezt is felismerem, ha később szabad szöveggel írja le a helyzetet.' },
    { cim: 'Hol tart a projekt?',
      mit: 'A szakasz mondja meg, mi a következő lépés: tájékozódás, méretezés, engedélyeztetés vagy kivitelezés. A jelenlegi megoldást is kérdezzük.',
      pelda: 'Ha most vásárolna telket, a „Telekvásárlás előtt" a jó — akkor a telek alkalmassága a fő kérdés.',
      auto: 'Ha működő rendszerrel van gond, itt a tüneteket is bejelölheti.' },
    { cim: 'Az ingatlan és a terhelés',
      mit: 'A terhelés adja a méretet, a telek adottságai a típust. Amit nem tud, hagyja üresen — ez nem hiba.',
      pelda: 'Négyfős család állandó lakhatással: állandó létszám 4, csúcsterhelés üres, ha nincs vendégjárás.',
      auto: 'A talajvizet és a telekméretet a szabad szöveges leírásból is kitöltöm.' },
    { cim: 'Írja le a saját szavaival',
      mit: 'Néhány mondat elég. Ez az a pont, ahol a legtöbbet tudok segíteni.',
      pelda: '„Négyfős család, új ház Esztergom mellett, nincs közcsatorna, a telek 1200 m², tavasszal magas a talajvíz."',
      auto: 'Egy gombnyomásra kiolvasom belőle az ingatlantípust, a létszámot, a projektszakaszt és a telekadatokat, és kitöltöm az előző lapokat. Amit rosszul értek, Ön javítja.' },
    { cim: 'Konzultáció módja és időpontja',
      mit: 'Válassza ki, hogyan egyeztetne, és jelöljön több sávot, amikor elérhető. Ez még nem foglalás — egyet visszaigazolunk.',
      pelda: 'Három sáv a jó arány: abból szinte biztosan találunk közöset.',
      auto: 'A naptárból kiválasztott sávok automatikusan bekerülnek a szöveges mezőbe.' },
    { cim: 'Elérhetőség',
      mit: 'Név és e-mail kell a visszaigazoláshoz, a telefon gyorsítja az egyeztetést. Az adatkezelési hozzájárulás kötelező.',
      pelda: 'A település vagy irányítószám azért fontos, mert a helyszíni felmérés útját ebből tervezzük.',
      auto: 'A beküldés után szakmai összefoglalót kap arról, mit érdemes a konzultációig előkészítenie.' },
  ];

  if (mod === 'urlap') {
    gyoker.classList.add('is-kisero');
    const doboz = document.createElement('div');
    doboz.className = 'oko-kisero';
    doboz.hidden = true;
    panel.insertBefore(doboz, tarsalgas);

    document.addEventListener('konzv:lap', (e) => {
      const adat = KISERO[e.detail.lap];
      if (!adat) { doboz.hidden = true; return; }
      doboz.hidden = false;
      doboz.innerHTML = `
        <div class="oko-kisero-fej">
          <span class="oko-kisero-lepes">${e.detail.lap}/6</span>
          <p class="type-ui-subtitle oko-kisero-cim"></p>
        </div>
        <p class="type-ui-caption oko-kisero-mit"></p>
        <p class="type-ui-caption oko-kisero-pelda"></p>
        <p class="type-ui-caption oko-kisero-auto">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3.5 13.9 9l5.6 1.9-5.6 2L12 18.5l-1.9-5.6L4.5 11l5.6-2z"/></svg>
          <span></span>
        </p>`;
      doboz.querySelector('.oko-kisero-cim').textContent = adat.cim;
      doboz.querySelector('.oko-kisero-mit').textContent = adat.mit;
      doboz.querySelector('.oko-kisero-pelda').textContent = adat.pelda;
      doboz.querySelector('.oko-kisero-auto span').textContent = adat.auto;
      /* Az animációt újra kell indítani: osztály le, reflow, osztály fel. */
      doboz.classList.remove('is-valt');
      void doboz.offsetWidth;
      doboz.classList.add('is-valt');
    });
  }

  /* --------------------------------------------------------------- kérdés */
  let dolgozik = false;
  const naplo = [];                  // a párbeszéd, hogy Öko építeni tudjon rá

  urlap.addEventListener('submit', (e) => {
    e.preventDefault();
    kerdez(input.value.trim());
  });

  async function kerdez(kerdes) {
    if (!kerdes || dolgozik) return;
    uzenet('en', kerdes);
    naplo.push({ kitol: 'en', szoveg: kerdes });
    input.value = '';
    dolgozik = true;
    gyoker.classList.add('is-gondolkodik');
    const varakozo = uzenet('oko', 'Megnézem…');

    try {
      const valasz = await fetch('/api/kalauz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kerdes, mod, oldal: location.pathname, elozmeny: naplo.slice(-6) }),
      });
      const eredmeny = await valasz.json();
      varakozo.remove();
      if (!valasz.ok || !eredmeny.ok) throw new Error(eredmeny.uzenet || '');
      const sor = uzenet('oko', eredmeny.valasz || '', eredmeny.talalatok);
      naplo.push({ kitol: 'oko', szoveg: eredmeny.valasz || '' });
      javaslatok(eredmeny.javaslatok, sor);
    } catch {
      varakozo.remove();
      uzenet('oko', 'Most nem érem el a keresőt. A menü Tudástár pontja alatt megtalálja a témákat, vagy hívjon minket: +36 33 200 211.');
    } finally {
      dolgozik = false;
      gyoker.classList.remove('is-gondolkodik');
      input.focus();
    }
  }
})();
