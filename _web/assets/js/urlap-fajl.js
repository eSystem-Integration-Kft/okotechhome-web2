/* =============================================================================
   ÖkoTech Home — Test2 · urlap-fajl.js
   Mellékletek: ledobó felület a natív fájlmező helyett
   -----------------------------------------------------------------------------
   MIÉRT. A natív `<input type="file">` két dolgot tud rosszul. Nem lehet
   RÁHÚZNI a fájlt — csak tallózni —, a kiválasztott fájlokról pedig annyit
   közöl, hogy „3 fájl": a nevüket nem, a méretüket nem, és egyet közülük nem
   lehet levenni, csak az egészet elölről kezdeni.

   MIT CSINÁL. A mezőt MEGTARTJA — a beküldés és a JS nélküli működés is ezen
   áll —, de elrejti a szem elől, és egy LEDOBÓ FELÜLETET tesz a helyére: ide
   húzható a fájl, ide kattintva nyílik a tallózó, alatta pedig ott a csatolt
   fájlok listája, névvel, mérettel, egyenkénti törléssel.

   NÉGY DÖNTÉS, AMI NEM MAGÁTÓL ÉRTETŐDŐ:

   1. A MEZŐ MARAD, CSAK NEM LÁTSZIK. A `visually-hidden` elrejtés
      FÓKUSZÁLHATÓ mezőt hagy maga után: a billentyűzetes látogató ugyanúgy
      odajut, a címke `for` kapcsolata ép marad, és a képernyőolvasó a valódi
      fájlmezőt jelenti be a saját címkéjével. `display:none` esetén mindez
      elveszne, és a ledobó felületre kellene ARIA-val ráhazudni, hogy ő a
      fájlmező. A fókuszkeretet a felület veszi át (`:focus-visible + .ledob`).

   2. A FÁJLLISTA HALMOZÓDIK. A tallózó minden megnyitása FELÜLÍRJA az input
      listáját, a látogató viszont azt várja, hogy a második behúzás HOZZÁAD.
      Ezért a lista itt él tömbként, és minden változás után visszaírjuk az
      inputba — így a beküldés pontosan azt küldi, amit a látogató lát.
      Az azonos fájl kétszer nem kerül be (név + méret + időbélyeg alapján).

   3. A VISSZAÍRÁSHOZ `DataTransfer` KELL. Ahol a böngésző nem ismeri (régi
      Safari), ott a behúzott lista EGYSZERŰEN felülírja a korábbit, a törlés
      pedig az egészet üríti — nem hamis felületet mutatunk, hanem szűkebb
      képességet. Ez a különbség sehol nem látszik hibaüzenetként.

   4. A KORLÁTOK A SZERVERREL EGYEZNEK (`api/lib/vedelem.php` → `fajl`), de ez
      a réteg csak KÖZÖL. A döntést a végpont hozza; a kliens megkerülhető.
   ============================================================================= */

(() => {
  'use strict';

  const mezok = document.querySelectorAll('[data-urlap-fajl]');
  if (!mezok.length) return;

  const MAX_DARAB = 3;
  const MAX_MERET = 10 * 1024 * 1024;

  /* A `DataTransfer` konstruktor a fájllista visszaírásának egyetlen módja.
     Egyszer kérdezzük meg, mert a hiánya nem változik futás közben. */
  const ATIRHATO = (() => {
    try { return !!new DataTransfer(); } catch (_) { return false; }
  })();

  const meret = (b) => (b < 1024 ? b + ' B'
    : b < 1048576 ? Math.round(b / 1024) + ' KB'
    : (b / 1048576).toFixed(1).replace('.', ',') + ' MB');

  /* --------------------------------------------------------------- ikonok */
  /* A típusjel a KITERJESZTÉSBŐL jön, nem a MIME-típusból: behúzáskor a
     `type` gyakran üres string, a fájlnév viszont mindig megvan. */
  const IRAT = '<path d="M14 3v5a1 1 0 0 0 1 1h5"/><path d="M20 9v10a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h8Z"/>';
  const IKON = {
    irat: IRAT + '<path d="M8 13h8M8 17h5"/>',
    kep:  IRAT + '<circle cx="9.5" cy="13" r="1.2"/><path d="M7 19l3.5-4 2.5 2.6 2-1.9L18 19"/>',
    tabla: IRAT + '<path d="M7 13h10M7 17h10M12 11v8"/>',
  };
  const TIPUSOK = [
    { minta: /\.(png|jpe?g|webp|gif|heic|avif)$/i, ikon: 'kep' },
    { minta: /\.(xlsx?|csv|ods)$/i,                ikon: 'tabla' },
  ];
  const ikonja = (nev) => (TIPUSOK.find((t) => t.minta.test(nev)) || { ikon: 'irat' }).ikon;

  const svg = (tartalom, osztaly) =>
    '<svg class="' + osztaly + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    + 'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
    + 'aria-hidden="true" focusable="false">' + tartalom + '</svg>';

  /* A ledobó felület jele: tálca, fölötte emelkedő nyíl. Behúzás közben a
     nyíl ismétlődően megemelkedik — ez az EGYETLEN önjáró mozgás a felületen,
     és pontosan addig tart, amíg a fájl a kurzoron lóg. */
  const LEDOB_JEL =
    '<svg class="urlap-ledob-abra" viewBox="0 0 48 40" fill="none" stroke="currentColor" '
    + 'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'
    + '<path class="urlap-ledob-talca" d="M7 25v6a4 4 0 0 0 4 4h26a4 4 0 0 0 4-4v-6"/>'
    + '<g class="urlap-ledob-nyil"><path d="M24 27V6"/><path d="M15.5 14.5 24 6l8.5 8.5"/></g>'
    + '</svg>';

  mezok.forEach((mezo) => {
    const hely = mezo.closest('.urlap-mezo') || mezo.parentElement;
    if (!hely) return;

    /* ------------------------------------------------------------ felület */
    const ledob = document.createElement('div');
    ledob.className = 'urlap-ledob';
    ledob.innerHTML =
      /* A keret SVG, nem `border`: így tud a szaggatás behúzáskor KÖRBEFUTNI.
         Nincs `viewBox` — a rajzegység így képpont, a lekerekítés nem torzul. */
      '<svg class="urlap-ledob-keret" aria-hidden="true" focusable="false">'
      + '<rect width="100%" height="100%" rx="10" ry="10"/></svg>'
      + '<span class="urlap-ledob-jel">' + LEDOB_JEL + '</span>'
      + '<span class="type-ui-subtitle urlap-ledob-cim">Húzza ide a fájlokat</span>'
      + '<span class="type-ui-caption urlap-ledob-alcim">vagy kattintson a tallózáshoz</span>'
      + '<span class="type-ui-caption urlap-ledob-korlat">PDF · JPG · PNG · DOCX · XLSX'
      + ' — legfeljebb ' + MAX_DARAB + ' fájl, egyenként 10 MB</span>';

    const lista = document.createElement('ul');
    lista.className = 'urlap-fajl-lista';
    /* ÉLŐ RÉGIÓ: a képernyőolvasó felolvassa, mi került be és mi a baj vele —
       enélkül a nem látó felhasználó csak a beküldéskor tudná meg. */
    lista.setAttribute('aria-live', 'polite');

    /* A sorrend: mező (rejtve) → felület → lista → a meglévő súgószöveg. */
    mezo.insertAdjacentElement('afterend', lista);
    mezo.insertAdjacentElement('afterend', ledob);
    mezo.classList.add('urlap-fajl-rejtve');

    /* A korlátok JS NÉLKÜL a súgószövegben állnak — ez az egyetlen hely, ahol
       akkor egyáltalán olvashatók. A felület viszont kiírja őket, ezért a
       súgóból itt kivesszük: kétszer ugyanaz a mondat zajt csinál. */
    hely.querySelectorAll('[data-fajl-korlat]').forEach((e) => e.remove());

    /* ---------------------------------------------------------- fájllista */
    let fajlok = Array.from(mezo.files || []);

    const kulcs = (f) => f.name + '|' + f.size + '|' + (f.lastModified || 0);

    /* Melyik fájl jelent már meg? A lista minden változásra ÚJRAÉPÜL, és
       animáció nélkül a beúszás minden korábbi soron újra lefutna: egy fájl
       csatolásakor az egész lista villanna. Csak az valóban új mozdul. */
    const latott = new Set();

    const visszair = () => {
      if (!ATIRHATO) return;
      const dt = new DataTransfer();
      fajlok.forEach((f) => dt.items.add(f));
      mezo.files = dt.files;
    };

    const hozzaad = (ujak) => {
      if (!ATIRHATO) { fajlok = Array.from(ujak); rajzol(); return; }
      const meglevo = new Set(fajlok.map(kulcs));
      Array.from(ujak).forEach((f) => {
        if (meglevo.has(kulcs(f))) return;
        meglevo.add(kulcs(f));
        fajlok.push(f);
      });
      visszair();
      rajzol();
    };

    const torol = (index) => {
      if (!ATIRHATO) { fajlok = []; mezo.value = ''; rajzol(); return; }
      fajlok.splice(index, 1);
      visszair();
      rajzol();
      /* A fókusz nem tűnhet el a törölt gombbal együtt: a felületre megy. */
      ledob.setAttribute('tabindex', '-1');
      ledob.focus({ preventScroll: true });
      ledob.removeAttribute('tabindex');
    };

    const rajzol = () => {
      lista.textContent = '';
      let hiba = '';

      if (fajlok.length > MAX_DARAB) {
        hiba = 'Legfeljebb ' + MAX_DARAB + ' fájl csatolható — most '
             + fajlok.length + ' van kiválasztva.';
      }

      /* A már nem szereplő fájlok kulcsa kikerül: ha ugyanazt később újra
         csatolják, az megint ÚJ — mert a látogató szemében az. */
      const mostani = new Set(fajlok.map(kulcs));
      latott.forEach((k) => { if (!mostani.has(k)) latott.delete(k); });

      fajlok.forEach((f, i) => {
        const li = document.createElement('li');
        li.className = 'urlap-fajl-tetel';
        if (!latott.has(kulcs(f))) { li.classList.add('is-uj'); latott.add(kulcs(f)); }
        const nagy = f.size > MAX_MERET;
        if (nagy) {
          li.classList.add('urlap-fajl-hibas');
          hiba = hiba || 'Egy fájl legfeljebb 10 MB lehet.';
        }
        li.innerHTML =
          '<span class="urlap-fajl-ikon">' + svg(IKON[ikonja(f.name)], 'urlap-fajl-tipus') + '</span>'
          + '<span class="urlap-fajl-adat">'
          + '<span class="type-ui-caption urlap-fajl-nev"></span>'
          + '<span class="type-ui-caption urlap-fajl-meret"></span></span>'
          + (nagy
            ? '<span class="urlap-fajl-jel urlap-fajl-jel-hiba">'
              + svg('<path d="M12 8v5"/><path d="M12 16.5h.01"/>'
                  + '<path d="M10.3 3.9 2.6 17.2A2 2 0 0 0 4.3 20h15.4a2 2 0 0 0 1.7-2.8L13.7 3.9a2 2 0 0 0-3.4 0Z"/>',
                'urlap-fajl-jel-abra') + '</span>'
            : '<span class="urlap-fajl-jel urlap-fajl-jel-ok">'
              + svg('<path d="m5 12.5 4.5 4.5L19 7.5"/>', 'urlap-fajl-jel-abra') + '</span>');

        /* A nevet és a méretet SZÖVEGKÉNT tesszük be: a fájlnév a látogatótól
           jön, és `innerHTML`-lel markup is lehetne belőle. */
        li.querySelector('.urlap-fajl-nev').textContent = f.name;
        li.querySelector('.urlap-fajl-meret').textContent =
          meret(f.size) + (nagy ? ' — túl nagy' : '');

        const gomb = document.createElement('button');
        gomb.type = 'button';
        gomb.className = 'urlap-fajl-torol';
        gomb.setAttribute('aria-label', f.name + ' eltávolítása');
        gomb.innerHTML = svg('<path d="M6 6l12 12M18 6 6 18"/>', 'urlap-fajl-torol-abra');
        gomb.addEventListener('click', () => torol(i));
        li.append(gomb);

        lista.append(li);
      });

      if (hiba) {
        const li = document.createElement('li');
        li.className = 'type-ui-caption urlap-fajl-uzenet';
        li.textContent = hiba;
        lista.append(li);
      }

      /* A natív ellenőrzés így a beküldést is megállítja. A `dataset` azért
         kell, mert az élő űrlapellenőrzés (urlap-ellenorzes.js) minden
         billentyűleütésnél újraszámolja a `customValidity`-t — onnan ezt a
         szöveget olvassa vissza, különben némán letörölné. */
      mezo.dataset.fajlHiba = hiba;
      mezo.setCustomValidity(hiba);
      ledob.classList.toggle('is-hibas', !!hiba);
      ledob.classList.toggle('is-telt', fajlok.length >= MAX_DARAB && !hiba);
    };

    /* ------------------------------------------------------------ kezelők */
    ledob.addEventListener('click', () => mezo.click());

    mezo.addEventListener('change', () => {
      hozzaad(mezo.files || []);
    });

    /* A behúzás számlálóval: a felület GYERMEKEI fölött a `dragleave` akkor is
       elsül, ha a kurzor a felületen belül maradt. A gyerekek `pointer-events`
       nélküliek, de a beágyazott SVG-k egyes böngészőkben mégis kapnak
       eseményt — a számláló ettől független. */
    let melyseg = 0;
    const jelolBe = () => { ledob.classList.add('is-huzas'); };
    const jelolKi = () => { melyseg = 0; ledob.classList.remove('is-huzas'); };

    ledob.addEventListener('dragenter', (e) => { e.preventDefault(); melyseg++; jelolBe(); });
    ledob.addEventListener('dragover', (e) => {
      e.preventDefault();
      /* A másolás-kurzor jelzi, hogy IDE le lehet tenni — enélkül a böngésző
         „tiltott" jelet mutat, és a látogató el sem engedi a fájlt. */
      if (e.dataTransfer) e.dataTransfer.dropEffect = 'copy';
      jelolBe();
    });
    ledob.addEventListener('dragleave', () => { if (--melyseg <= 0) jelolKi(); });
    ledob.addEventListener('dragend', jelolKi);

    ledob.addEventListener('drop', (e) => {
      e.preventDefault();
      jelolKi();
      const ujak = e.dataTransfer && e.dataTransfer.files;
      if (!ujak || !ujak.length) return;
      /* A mezőt „érintettnek" jelöljük, mert a behúzás nem fókuszál semmit, és
         az élő ellenőrzés csak érintett mezőn mutat hibát. */
      mezo.dataset.erintett = '1';
      hozzaad(ujak);
      /* `input`, NEM `change`. A `change` a saját kezelőnket is újraindítaná:
         a lista másodszor is újraépülne, és a beúszó animáció még azelőtt
         eltűnne, hogy bárki látta volna. Az élő ellenőrzés (urlap-ellenorzes.js)
         mindkettőre újraszámol, tehát a gomb állapota így is helyes. */
      mezo.dispatchEvent(new Event('input', { bubbles: true }));
    });

    /* A LAP FÖLÖTTI BEHÚZÁS. A böngésző alapértelmezése az, hogy a lap HELYETT
       nyitja meg a behúzott fájlt — ha a látogató elvéti a felületet, egy
       rossz mozdulattal elveszti a kitöltött űrlapot. Ezt megakadályozzuk, és
       közben halványan megmutatjuk, hol a felület helye.

       CSAK FÁJLRA. A `types` vizsgálata nem formaság: enélkül a szövegbehúzás
       is ide esne, és a megjegyzés-mezőbe nem lehetne szöveget húzni. */
    const fajltHuz = (e) => !!e.dataTransfer
      && Array.prototype.indexOf.call(e.dataTransfer.types || [], 'Files') >= 0;

    ['dragover', 'drop'].forEach((ev) =>
      document.addEventListener(ev, (e) => {
        if (ledob.contains(e.target) || !fajltHuz(e)) return;
        e.preventDefault();
        if (ev === 'drop') { jelolKi(); ledob.classList.remove('is-keszen'); }
      }));
    document.addEventListener('dragenter', (e) => {
      if (fajltHuz(e)) ledob.classList.add('is-keszen');
    });
    ['dragleave', 'dragend'].forEach((ev) =>
      document.addEventListener(ev, (e) => {
        /* Csak akkor engedjük el, ha a kurzor tényleg elhagyta az ablakot:
           a belső elemhatárokon átlépve a `relatedTarget` nem üres. */
        if (ev === 'dragleave' && e.relatedTarget) return;
        ledob.classList.remove('is-keszen');
      }));

    /* Sikeres beküldés után az űrlap kiürül — a lista is. */
    const urlap = mezo.form;
    if (urlap) {
      urlap.addEventListener('reset', () => {
        window.setTimeout(() => { fajlok = []; visszair(); rajzol(); }, 0);
      });
    }

    rajzol();
  });
})();
