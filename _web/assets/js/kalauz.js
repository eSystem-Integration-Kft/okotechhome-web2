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

   MIKOR SZÓLAL MEG. Hero-s lapon a fejléckép felének kigördülése után magától
   kinyílik (fókuszt nem vesz el), a konzultációkérőn nyitva érkezik. A bezárás
   egy lapnézetre szól: ott fülre húzódik, a következő lapon újra aktív. A fül
   időnként jelez, és kétszer kérdez is. Csökkentett mozgás mellett minden
   animáció elmarad — a figura akkor egyszerűen ott van.
   ============================================================================= */

(() => {
  'use strict';

  if (document.querySelector('.oko')) return;                 // kétszer ne
  const TAROLO = 'oth-oko-elrejtve';
  const csokkentett = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const mod = document.body.dataset.kalauzMod || 'kalauz';

  /* A bezárás hatóköre EGYETLEN lapnézet. Volt munkamenet-szintű is
     (sessionStorage-zászlóval), de az félrevezetett: aki egyszer becsukta,
     annál minden további lapon némán, fülként indult — élesben úgy tűnt,
     Öko „kikapcsolt". Alapból mindig aktív; aki ezen a lapon csukta be,
     azt ezen a lapon nem zargatjuk újra. */
  let lezarta = false;

  /* --------------------------------------------------------------- a figura */
  /* Egyetlen inline SVG, mert a szemek külön mozognak: a pupilla a kurzor felé
     fordul, a szemhéj pislog. Külső fájlból ezek nem volnának elérhetők. */
  const FIGURA = `
<svg class="oko-figura" viewBox="0 0 100 108" role="img" aria-hidden="true" focusable="false">
  <ellipse class="oko-arnyek" cx="50" cy="102" rx="29" ry="4.5"/>
  <g class="oko-test-csoport">
    <!-- narancs csonkok: a jobb oldali magasabban, ahogy a terméken -->
    <rect class="oko-csonk-arny" x="6" y="53.5" width="16" height="8" rx="4"/>
    <rect class="oko-csonk" x="6" y="52" width="16" height="8" rx="4"/>
    <rect class="oko-csonk-arny" x="78" y="46.5" width="16" height="8" rx="4"/>
    <rect class="oko-csonk" x="78" y="45" width="16" height="8" rx="4"/>

    <!-- kúpos felsőrész, lekerekített felső élekkel -->
    <path class="oko-kup" d="M37.5 15h25a4 4 0 0 1 3.7 2.5L74 39H26l7.8-21.5A4 4 0 0 1 37.5 15z"/>
    <!-- a kúp bal oldalán fény, jobb oldalán árnyék: ettől lesz kúp, nem háromszög -->
    <path class="oko-kup-feny" d="M37.5 15h7l-6 24H26l7.8-21.5A4 4 0 0 1 37.5 15z"/>
    <path class="oko-kup-arny" d="M62.5 15h-6l6 24H74l-7.8-21.5A4 4 0 0 0 62.5 15z"/>

    <!-- perem a kúp és a henger között -->
    <rect class="oko-perem" x="20" y="38.5" width="60" height="7" rx="3.5"/>
    <rect class="oko-perem-vonal" x="20" y="44.5" width="60" height="1.6" rx=".8"/>

    <!-- hengeres test, enyhén domború oldalakkal -->
    <path class="oko-test"
          d="M23.5 45.5c-.8 14-.9 27.5 0 40.5.4 6 4.6 10 10.5 10h32c5.9 0 10.1-4 10.5-10 .9-13 .8-26.5 0-40.5z"/>
    <!-- fény a bal oldalon, árnyék a jobb szélen -->
    <path class="oko-test-feny" d="M23.5 45.5c-.8 14-.9 27.5 0 40.5.2 3.2 1.5 5.8 3.5 7.6-1.6-16-1.7-32.1-.5-48.1z"/>
    <path class="oko-test-arny" d="M76.5 45.5c.8 14 .9 27.5 0 40.5-.3 4.3-2.5 7.5-5.8 9.1 2.3-16.4 2.6-33 1.3-49.6z"/>

    <!-- szemek -->
    <g class="oko-szem">
      <ellipse class="oko-szemfeher" cx="40.5" cy="66" rx="11.5" ry="12.5"/>
      <circle class="oko-pupilla" data-oko-pupilla cx="40.5" cy="66" r="5.6"/>
      <circle class="oko-csillanas" cx="38" cy="63" r="2"/>
      <rect class="oko-hej" data-oko-hej x="28.5" y="51" width="25" height="0" rx="2"/>
    </g>
    <g class="oko-szem">
      <ellipse class="oko-szemfeher" cx="62.5" cy="66" rx="11.5" ry="12.5"/>
      <circle class="oko-pupilla" data-oko-pupilla cx="62.5" cy="66" r="5.6"/>
      <circle class="oko-csillanas" cx="60" cy="63" r="2"/>
      <rect class="oko-hej" data-oko-hej x="50.5" y="51" width="25" height="0" rx="2"/>
    </g>

    <!-- KONTÚR. A fény- és árnyékrétegek FÖLÉ kerül, különben azok kitakarnák
         a széleket. Enélkül a törtfehér test beleolvad a világos zöld fejlécbe
         és a lap halvány felületeibe. -->
    <g class="oko-kontur">
      <path d="M37.5 15h25a4 4 0 0 1 3.7 2.5L74 39H26l7.8-21.5A4 4 0 0 1 37.5 15z"/>
      <rect x="20" y="38.5" width="60" height="7" rx="3.5"/>
      <path d="M23.5 45.5c-.8 14-.9 27.5 0 40.5.4 6 4.6 10 10.5 10h32c5.9 0 10.1-4 10.5-10 .9-13 .8-26.5 0-40.5z"/>
    </g>
  </g>
</svg>`;

  const SZOVEG = {
    kalauz: {
      koszon: 'Segítsek megtalálni, amit keres?',
      alcim: 'Megmutatom, hol a válasz.',
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
      /* A félretett fül időnkénti kérdései. */
      jelzes: [
        'Segítsek megtalálni, amit keres?',
        'Kérdezhet — megmutatom, hol a válasz.',
      ],
    },
    urlap: {
      koszon: 'Ha elakad a kitöltésben, szóljon.',
      alcim: 'Segítek a kitöltésben.',
      sug: 'Kérdezzen bátran bármelyik mezőről — azt is megmondom, mit érdemes előkészíteni.',
      helyorzo: 'Például: mit írjak a csúcsterheléshez?',
      inditok: [
        'Mit írjak, ha nem tudom a telek méretét?',
        'Mit jelent a csúcsterhelés?',
        'Milyen adatokat készítsek elő a konzultációra?',
      ],
      jelzes: [
        'Elakadt a kitöltésben? Segítek.',
        'Kérdezzen — megmondom, mit hová írjon.',
      ],
    },
    jelentes: {
      koszon: 'Segítek értelmezni az összehasonlítást.',
      alcim: 'Elmagyarázom az összehasonlítást.',
      sug: 'Kérdezzen a jelentés bármelyik soráról — elmondom, mit jelent és mire érdemes figyelni.',
      helyorzo: 'Például: miért tér el a két ár?',
      inditok: [
        'Mire figyeljek az ajánlatok összevetésénél?',
        'Mi az, ami gyakran kimarad egy ajánlatból?',
        'Mit jelent, ha nagyon eltér a két ár?',
      ],
      jelzes: [
        'Kérdése van az összehasonlítás valamelyik sorához?',
      ],
    },
  }[mod] || {};

  /* LAPTÉMÁK. Öko nem ugyanazt mondja a megoldások között, mint a referenciák
     vagy az előkészítés lapjain: a köszönés, a belépő kérdések és a fül
     időnkénti kérdései a webhely szakaszához igazodnak. Az útvonal dönt —
     laponkénti kézi lista 119 oldalra nem volna karbantartható. */
  if (mod === 'kalauz') {
    const TEMAK = [
      [/^\/helyzetem/, {
        koszon: 'Segítek eldönteni, mi legyen a következő lépés.',
        inditok: [
          'Mi a következő lépés az én helyzetemben?',
          'Milyen adatokat gyűjtsek össze?',
          'Melyik megoldástípus való nekem?',
        ],
        jelzes: [
          'Melyik lépésnél tart most?',
          'Segítsek megtalálni a helyzetéhez illő utat?',
        ],
      }],
      [/^\/megoldasok/, {
        koszon: 'Kérdezzen bátran erről a megoldásról.',
        inditok: [
          'Kinek való ez a megoldás?',
          'Mikor nem megfelelő ez a rendszer?',
          'Miben tér el a többi megoldástól?',
        ],
        jelzes: [
          'Segítsek eldönteni, ez való-e az Ön telkére?',
          'Kíváncsi, mennyi helyet kér ez a rendszer?',
        ],
      }],
      [/^\/projekt-elokeszites/, {
        koszon: 'Segítek az előkészítésben eligazodni.',
        inditok: [
          'Milyen vizsgálatok kellenek a telkemhez?',
          'Mit tudok előre elintézni?',
          'Mikor kell szakértőt bevonni?',
        ],
        jelzes: [
          'Tudja már, milyen a talaj a telkén?',
          'Segítsek összeállítani a teendőlistát?',
        ],
      }],
      [/^\/eredmenyek/, {
        koszon: 'Referenciák között jár — segítek keresni.',
        inditok: [
          'Van hasonló projekt az én helyzetemhez?',
          'Mit mutatnak a mérési eredmények?',
          'Hol működik ilyen rendszer a környékemen?',
        ],
        jelzes: [
          'Keressek az Önéhez hasonló projektet?',
        ],
      }],
      [/^\/tudastar/, {
        koszon: 'A tudástárban segítek eligazodni.',
        jelzes: [
          'Nem találja, amit keres? Segítek.',
        ],
      }],
    ];
    const tema = TEMAK.find(([minta]) => minta.test(location.pathname));
    if (tema) Object.assign(SZOVEG, tema[1]);
  }

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
        <button type="button" class="oko-panel-zar" data-oko-panel-zar
                aria-label="Bezárás — Öko a lap szélén marad" title="Becsukom">
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
  gyoker.querySelector('[data-oko-alcim]').textContent = SZOVEG.alcim || '';
  input.placeholder = SZOVEG.helyorzo || '';

  /* ------------------------------------------------------------- bejövetel */
  /* Nem az első pillanatban jelenik meg: a lap előbb nyugodjon meg, hogy a
     figura ne a betöltés zajába érkezzen. Aki egyszer elküldte, annak a
     munkamenet végéig nem jelentkezik újra. */
  /* Öko MINDIG ott van — a bezárás a köszönő buborékra vonatkozik, nem a
     figurára. Aki nem kér a szövegből, attól elvesszük a buborékot, de a
     segéd elérhető marad: ez a dolga. */
  /* Aki a buborékot bezárta, annak a munkamenetben nem szólunk többet — sem
     köszönéssel, sem a fül időnkénti kérdéseivel. Futásidőben is billen, mert
     a döntés az X-szel bármikor megszülethet. */
  let buborekTiltva = (() => { try { return sessionStorage.getItem(TAROLO) === '1'; } catch { return false; } })();

  function megerkezik() {
    if (gyoker.classList.contains('is-erkezik')) return;
    gyoker.classList.add('is-erkezik');
    /* Ha fülként indul (konzultációkérő), a becsúszás animációja már az
       érkezés ELŐTT, láthatatlanul lefutott — a gyökér addig visibility:hidden.
       Itt újraindítjuk, hogy a belépés látsszon is. */
    if (gyoker.classList.contains('is-ful') && !csokkentett) {
      ful.style.animation = 'none';
      void ful.offsetWidth;                        // reflow: az animáció újraindul
      ful.style.animation = '';
    }
    if (SZOVEG.koszon && !buborekTiltva && !lezarta && !panelNyitva()) {
      buborekSzoveg.textContent = SZOVEG.koszon;
      buborek.hidden = false;
      setTimeout(() => { if (!panelNyitva()) buborek.hidden = true; }, 9000);
    }
  }

  /* A FŐOLDALON megvárjuk a hero-t. Ott a nagy fejléckép viszi a figyelmet, és
     egy sarokban feltűnő segéd elvenne belőle — ezért Öko csak akkor lép elő,
     amikor a hero java már kigördült felfelé. A `.hero` a főoldalé; az
     aloldalak fejléce `.page-hero` is, azokon marad az azonnali megjelenés. */

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
  /* `fokuszal:false` az automatikus nyitásé: amikor Öko magától szólal meg
     (főoldal, konzultációkérő), nem veheti el a fókuszt — a látogató éppen
     görget vagy űrlapot tölt, és a billentyűzete az övé. */
  function nyit(fokuszal = true) {
    buborek.hidden = true;
    fulre(true);                       // előbb félrevonul, hogy legyen helye
    panel.hidden = false;
    bezarasBekotes();
    gomb.setAttribute('aria-expanded', 'true');
    ful.setAttribute('aria-expanded', 'true');
    gyoker.classList.add('is-nyitva');
    if (!tarsalgas.children.length && SZOVEG.sug) {
      const sor = uzenet('oko', SZOVEG.sug);
      javaslatok(SZOVEG.inditok, sor);
    }
    if (fokuszal) input.focus();
  }
  function zar() {
    if (panel.hidden || panel.classList.contains('is-zarul')) return;
    gomb.setAttribute('aria-expanded', 'false');
    ful.setAttribute('aria-expanded', 'false');
    gyoker.classList.remove('is-nyitva');
    /* Bezárás után Öko NEM megy vissza a sarokba: a lap szélén marad, fülként.
       A sarok az érkezés helye — akinek a panel most nem kell, annak a fül a
       nyugalmi állapot. A döntés erre a lapnézetre szól: itt nem nyitunk rá
       újra automatikusan — a következő lapon Öko megint alapból aktív. */
    lezarta = true;
    reflektorLe();
    const lezar = () => {
      panel.classList.remove('is-zarul');
      panel.hidden = true;
      ful.focus();
    };
    if (csokkentett) { lezar(); return; }
    /* LÁTHATÓ kivonulás: a panel a fül felé húz össze — látszik, HOVÁ ment —,
       a fül pedig nyugtázza: előrelép és pislant. Enélkül a panel egyszerűen
       eltűnt, és a látogató nem tudta, hol keresse. */
    panel.classList.add('is-zarul');
    setTimeout(() => {
      lezar();
      ful.classList.add('is-int');
      pislog();
      setTimeout(() => ful.classList.remove('is-int'), 1200);
    }, 230);
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

  /* A KONZULTÁCIÓKÉRŐN Öko eleve a lap szélén ül, fülként — ott az űrlap a
     főszereplő, a sarokban álló figura a Tovább gomb útjában állna. A fül a
     jobb szél közepén jelzi, hogy itt van, és egy koppintásra kinyílik. */
  if (mod === 'urlap') fulre(true);
  /* ESEMÉNYDELEGÁLÁS a gyökéren. Az egyes gombokra kötött kezelők közül a
     kicsinyítőé néma maradt — a gomb ott volt, a kattintás rá is ment, kezelő
     viszont nem tartozott hozzá. Egyetlen figyelő a gyökéren ezt a hibaosztályt
     megszünteti: nem számít, mikor és hányszor épül újra a panel belseje. */
  /* A bezárás FÜLRE CSUK: a panel eltűnik, Öko viszont a lap szélén marad,
     egy koppintásra elérhetően.

     A kezelő a NYITÁSKOR kerül a gombra, nem a modul betöltésekor: a
     gyökérre kötött delegálás és a betöltéskori közvetlen kötés is némán
     kimaradt, a gomb tehát halott volt. Így viszont akkor kötjük, amikor a
     gomb bizonyítottan a DOM-ban van, és az `onclick` egyetlen kezelőt tart —
     ismételt nyitásnál sem halmozódik. */
  function bezarasBekotes() {
    const x = panel.querySelector('[data-oko-panel-zar]');
    if (!x) return;
    /* Ugyanaz a `zar()`, mint az Escape-é és a fülé: a bezárásnak EGY útja
       van, és mindegyik a fülön hagyja Ökót. */
    x.onclick = zar;
  }

  gyoker.querySelector('[data-oko-zar]').addEventListener('click', () => {
    buborek.hidden = true;
    buborekTiltva = true;
    try { sessionStorage.setItem(TAROLO, '1'); } catch { /* privát mód */ }
  });
  /* A buborék maga is meghívás: rákattintva a panel nyílik. Az X kivétel —
     az a „köszönöm, nem" útja. */
  buborek.addEventListener('click', (e) => {
    if (e.target.closest('[data-oko-zar]')) return;
    if (!panelNyitva()) nyit();
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
    /* A tartalomindex horgonyai a CÍMEKEN ülnek, mert a lapokon az `id` ott
       van. Egy kiemelt címsor viszont semmit nem mond — a válasz a szakaszban
       áll, tehát a legközelebbi szakaszt emeljük ki, ha van. */
    cel = cel.closest('section') || cel;
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
      auto: 'A leírásból ezt is felismerem, ha később szabad szöveggel írja le a helyzetet.',
      kerdesek: ['Nyaralóra keresek megoldást — magánszemély vagyok?',
        'Mi számít vállalkozási létesítménynek?'] },
    { cim: 'Hol tart a projekt?',
      mit: 'A szakasz mondja meg, mi a következő lépés: tájékozódás, méretezés, engedélyeztetés vagy kivitelezés. A jelenlegi megoldást is kérdezzük.',
      pelda: 'Ha most vásárolna telket, a „Telekvásárlás előtt" a jó — akkor a telek alkalmassága a fő kérdés.',
      auto: 'Ha működő rendszerrel van gond, itt a tüneteket is bejelölheti.',
      kerdesek: ['Emésztőm van — melyik szakaszt jelöljem?',
        'Nem tudom, mi van most a telken. Mit válasszak?'] },
    { cim: 'Az ingatlan és a terhelés',
      mit: 'A terhelés adja a méretet, a telek adottságai a típust. Amit nem tud, hagyja üresen — ez nem hiba.',
      pelda: 'Négyfős család állandó lakhatással: állandó létszám 4, csúcsterhelés üres, ha nincs vendégjárás.',
      auto: 'A talajvizet és a telekméretet a szabad szöveges leírásból is kitöltöm.',
      kerdesek: ['Mit írjak a csúcsterheléshez?',
        'Honnan tudom, magas-e a talajvíz?',
        'Nem tudom a telek méretét — baj?'] },
    { cim: 'Írja le a saját szavaival',
      mit: 'Néhány mondat elég. Ez az a pont, ahol a legtöbbet tudok segíteni.',
      pelda: '„Négyfős család, új ház Esztergom mellett, nincs közcsatorna, a telek 1200 m², tavasszal magas a talajvíz."',
      auto: 'Egy gombnyomásra kiolvasom belőle az ingatlantípust, a létszámot, a projektszakaszt és a telekadatokat, és kitöltöm az előző lapokat. Amit rosszul értek, Ön javítja.',
      kerdesek: ['Mit érdemes beleírnom a leírásba?',
        'Mi történik a leírásommal beküldés után?'] },
    { cim: 'Konzultáció módja és időpontja',
      mit: 'Válassza ki, hogyan egyeztetne, és jelöljön több sávot, amikor elérhető. Ez még nem foglalás — egyet visszaigazolunk.',
      pelda: 'Három sáv a jó arány: abból szinte biztosan találunk közöset.',
      auto: 'A naptárból kiválasztott sávok automatikusan bekerülnek a szöveges mezőbe.',
      kerdesek: ['Melyik konzultációs formát válasszam?',
        'Mi történik, ha egyik időpontom sem jó Önöknek?'] },
    { cim: 'Elérhetőség',
      mit: 'Név és e-mail kell a visszaigazoláshoz, a telefon gyorsítja az egyeztetést. Az adatkezelési hozzájárulás kötelező.',
      pelda: 'A település vagy irányítószám azért fontos, mert a helyszíni felmérés útját ebből tervezzük.',
      auto: 'A beküldés után szakmai összefoglalót kap arról, mit érdemes a konzultációig előkészítenie.',
      kerdesek: ['Miért kérik a települést?',
        'Mi történik az adataimmal a beküldés után?'] },
  ];

  if (mod === 'urlap') {
    gyoker.classList.add('is-kisero');
    const doboz = document.createElement('div');
    doboz.className = 'oko-kisero';
    doboz.hidden = true;
    panel.insertBefore(doboz, tarsalgas);

    document.addEventListener('konzv:lap', (e) => {
      aktualisLepes = e.detail.lap;                 // Öko válaszaihoz: hol áll épp
      const adat = KISERO[e.detail.lap];
      if (!adat) { doboz.hidden = true; return; }
      doboz.hidden = false;
      doboz.innerHTML = `
        <button type="button" class="oko-kisero-fej" data-oko-kisero-valt
                aria-expanded="true" title="A lépés súgójának nyitása-csukása">
          <span class="oko-kisero-lepes">${e.detail.lap}/6</span>
          <span class="type-ui-subtitle oko-kisero-cim"></span>
          <svg class="oko-kisero-nyil" viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>
        </button>
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
      /* Laponkénti javasolt kérdések: a látogatónak nem kell kitalálnia, mit
         kérdezhet — Öko az AKTUÁLIS lap buktatóit kínálja fel. */
      (adat.kerdesek || []).length && (() => {
        const sor = document.createElement('div');
        sor.className = 'oko-kisero-kerdesek';
        adat.kerdesek.forEach((k) => {
          const g = document.createElement('button');
          g.type = 'button';
          g.className = 'oko-javaslat';
          g.textContent = k;
          g.addEventListener('click', () => kerdez(k));
          sor.appendChild(g);
        });
        doboz.appendChild(sor);
      })();
      /* Párbeszéd közben a kísérő csukva frissül — a fejléce nyitja. Az
         aria-expanded a LÁTHATÓ állapotot mondja: párbeszéd nélkül minden
         részlet látszik, tehát nyitott. */
      doboz.classList.remove('is-nyitott');
      const valt = doboz.querySelector('[data-oko-kisero-valt]');
      const ariaFrissit = () => valt.setAttribute('aria-expanded',
        String(!(gyoker.classList.contains('is-tarsalog') && !doboz.classList.contains('is-nyitott'))));
      valt.onclick = () => { doboz.classList.toggle('is-nyitott'); ariaFrissit(); };
      ariaFrissit();
      /* Az animációt újra kell indítani: osztály le, reflow, osztály fel. */
      doboz.classList.remove('is-valt');
      void doboz.offsetWidth;
      doboz.classList.add('is-valt');
    });
  }

  /* --------------------------------------------------------------- kérdés */
  let dolgozik = false;
  let aktualisLepes = 0;             // urlap módban: melyik lapon áll a látogató
  const naplo = [];                  // a párbeszéd, hogy Öko építeni tudjon rá

  urlap.addEventListener('submit', (e) => {
    e.preventDefault();
    kerdez(input.value.trim());
  });

  async function kerdez(kerdes) {
    if (!kerdes || dolgozik) return;
    /* A MUNKATÉR MEGNYÚLIK: az első kérdéstől a panel nagyobb, a kísérő pedig
       fejlécre csukódik — a hely az olvasásé. A CSS intézi, itt csak a jel. */
    gyoker.classList.add('is-tarsalog');
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
        body: JSON.stringify({ kerdes, mod, oldal: location.pathname, lepes: aktualisLepes, elozmeny: naplo.slice(-6) }),
      });
      const eredmeny = await valasz.json();
      varakozo.remove();
      if (!valasz.ok || !eredmeny.ok) throw new Error(eredmeny.uzenet || '');
      const sor = uzenet('oko', eredmeny.valasz || '', eredmeny.talalatok);
      naplo.push({ kitol: 'oko', szoveg: eredmeny.valasz || '' });
      javaslatok(eredmeny.javaslatok, sor);

      /* MEGMUTATJA MAGÁTÓL. Ha az első találat ezen a lapon van, nem várunk
         kattintásra: odagörgetünk, a lap többi részét visszavesszük, és a kéz
         rámutat. „Itt van" — ez a segéd dolga, nem egy újabb hivatkozás. */
      const elso = (eredmeny.talalatok || [])[0];
      if (elso && elso.horgony) {
        const most = location.pathname.replace(/\/$/, '') || '/';
        const oda = (elso.url || '').replace(/\/$/, '') || '/';
        const cel = most === oda ? document.querySelector(elso.horgony) : null;
        if (cel) setTimeout(() => kiemel(cel), 420);
      }
    } catch {
      varakozo.remove();
      uzenet('oko', 'Most nem érem el a keresőt. A menü Tudástár pontja alatt megtalálja a témákat, vagy hívjon minket: +36 33 200 211.');
    } finally {
      dolgozik = false;
      gyoker.classList.remove('is-gondolkodik');
      input.focus();
    }
  }

  /* ---------------------------------------------------- mikor lépjen elő */
  /* A FŐOLDALON megvárjuk a hero-t: ott a nagy fejléckép viszi a figyelmet, és
     egy sarokban feltűnő segéd elvenne belőle. Öko akkor jön elő, amikor a
     hero fele már kigördült felfelé. Az aloldalakon (`.page-hero`) marad az
     azonnali megjelenés.

     A GÖRGETÉS POZÍCIÓJÁT nézzük, nem IntersectionObservert: a hero magasabb a
     nézetablaknál, ezért a látható aránya betöltéskor is 0.5 alatt van, és a
     figyelő rögtön az első hívásán megszólalt.

     EZ A BLOKK A FÁJL VÉGÉN ÁLL, szándékosan: korábban a felület konstansai
     (`panel`, `ful`) még nem léteztek, a `megerkezik()` viszont hivatkozott
     rájuk — a dobott hiba pedig csendben megállította a szkript hátralévő
     részét, és a gombok kezelői sem épültek fel. */
  const hero = document.querySelector('.hero');
  if (mod === 'urlap') {
    /* A KONZULTÁCIÓKÉRŐN Öko nem várat magára: nyitva érkezik, a kísérővel és
       a lap kérdéseivel — itt ő a másodpilóta, nem díszlet. Fókuszt nem vesz
       el: a látogató az űrlapot tölti. */
    setTimeout(() => {
      megerkezik();
      if (!lezarta) nyit(false);
    }, csokkentett ? 200 : 900);
  } else if (hero) {
    /* MINDEN HERO-S LAPON idegenvezetőként dolgozik: amikor a fejléckép fele
       kigördült — tehát a látogató elindult lefelé, olvasni kezdett —,
       magától kinyílik a lap témájához igazított belépő kérdésekkel. Az
       aloldalak fejléce alacsonyabb, ott ez hamarabb jön el — pont jókor:
       aki görget, az keres valamit. Aki egyszer becsukta, annál csak a
       figura érkezik meg. */
    const gorgetesre = () => {
      if (scrollY > hero.offsetHeight * 0.5) {
        removeEventListener('scroll', gorgetesre);
        clearTimeout(vegso);
        megerkezik();
        if (!lezarta) nyit(false);
      }
    };
    /* Ha a látogató nem görget, húsz másodperc után akkor is előlép — de csak
       a figura: aki áll, annak nem ugrunk az arcába egy nyitott panellel. */
    const vegso = setTimeout(megerkezik, 20000);
    addEventListener('scroll', gorgetesre, { passive: true });
    gorgetesre();                    // horgonnyal érkezőnek már görgetve van
  } else {
    setTimeout(megerkezik, csokkentett ? 200 : 1600);
  }

  /* ------------------------------------------------------- a fül jelzése */
  /* A félrehúzott fül nem hallgat el végleg: időnként előrébb lép, megbillen
     és pislant — az első két alkalommal pedig KÉRDEZ is egyet, a lap
     témájában, a fül melletti buborékban. Kétszer és nem többször: a segéd
     jelen van, nem követelőzik. Aki a buborékot X-szel bezárta, annak csak a
     néma jelzés marad. Csökkentett mozgás mellett semmi. */
  let jelzesDb = 0;
  if (!csokkentett) {
    setInterval(() => {
      if (ful.hidden || panelNyitva() || !gyoker.classList.contains('is-erkezik')) return;
      ful.classList.add('is-int');
      pislog();
      setTimeout(() => ful.classList.remove('is-int'), 1400);
      const kerdesek = SZOVEG.jelzes || [];
      if (!buborekTiltva && kerdesek.length && jelzesDb < 2) {
        buborekSzoveg.textContent = kerdesek[jelzesDb % kerdesek.length];
        jelzesDb++;
        buborek.hidden = false;
        setTimeout(() => { if (!panelNyitva()) buborek.hidden = true; }, 8000);
      }
    }, 38000);
  }
})();
