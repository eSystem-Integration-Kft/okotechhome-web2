/* =============================================================================
   ÖkoTech Home — Test2 · szippantas.js
   Szippantási díj kalkulátor + települési díjadatbázis
   -----------------------------------------------------------------------------
   Amit csinál:
     1. a látogató által megadott díjszabásból kiszámolja az alkalmankénti és az
        éves szippantási költséget, és megmutatja, MIBŐL áll össze;
     2. kirajzolja a megyei csempetérképet, amely azt mutatja, hol tartunk a
        települési díjadatbázis építésével;
     3. átmásolja a kalkulátor értékeit a díjbeküldő űrlapba.

   Amit szándékosan NEM csinál:
     - nem tartalmaz sem díjat, sem településnevet: minden adat a
       `assets/data/szippantas-konfig.js` fájlból jön (0.6 alapszabály —
       számérték nem a kódban él);
     - nem validál a szerver helyett: a beküldést a `urlap.js` viszi, a döntést
       az `api/szippantasi-dij` végpont hozza;
     - nem állít semmit a látogató településéről, amíg arról nincs ellenőrzött
       forrásunk. Az üres adatbázis üresnek is látszik.

   JS nélkül: a lapon ott a képlet szavakban és a telefonos út (`<noscript>`).
   ============================================================================= */

(() => {
  'use strict';

  const gyoker = document.querySelector('[data-szip]');
  if (!gyoker) return;

  /* --------------------------------------------------------------- KONFIG */
  /* Ha a konfigfájl nem töltődött be, a modul nem tippel: kiírja, hogy az
     adat hiányzik, és a kalkulátor a látogató saját értékeivel dolgozik
     tovább (a példaértékek nélkül). A szekció nem törhet el emiatt. */
  const CFG = window.OTH_SZIPPANTAS || {};
  const PELDA = CFG.peldaDijak || {};
  const MEGYEK = Array.isArray(CFG.megyek) ? CFG.megyek : [];
  const DIJAK = Array.isArray(CFG.dijak) ? CFG.dijak : [];
  const KOCSI_SAVOK = Array.isArray(CFG.kocsiSavok) ? CFG.kocsiSavok : [];
  const KOCSI_MIN = Number(CFG.kocsiMin) || 1;
  const KOCSI_MAX = Number(CFG.kocsiMax) || 20;

  const halkMozgas = window.matchMedia('(prefers-reduced-motion: reduce)');

  /* ------------------------------------------------------------ FORMÁZÁS */
  /* Magyar számformátum: ezres csoportosítás nem törhető szóközzel
     (`1 234 567 Ft`), tizedesjel vessző. Az Intl adja, nem kézzel fűzzük. */
  const ft0 = new Intl.NumberFormat('hu-HU', { maximumFractionDigits: 0 });
  const szam1 = new Intl.NumberFormat('hu-HU', { maximumFractionDigits: 1 });
  const szazalek = new Intl.NumberFormat('hu-HU', { style: 'percent', maximumFractionDigits: 0 });

  const forint = (n) => ft0.format(Math.round(n)) + ' Ft';
  const kobmeter = (n) => szam1.format(n) + ' m³';

  /* ------------------------------------------------------------- SEGÉDEK */
  const el = (sel, hol) => (hol || gyoker).querySelector(sel);
  const mind = (sel, hol) => Array.from((hol || gyoker).querySelectorAll(sel));

  /** Mező értéke számként. Üres mező 0, negatív érték nincs. */
  const ertek = (nev, alap) => {
    const m = el('[name="' + nev + '"]');
    if (!m) return alap || 0;
    const v = parseFloat(String(m.value).replace(',', '.'));
    if (!isFinite(v)) return typeof alap === 'number' ? alap : 0;
    return Math.max(0, v);
  };

  const beir = (nev, v) => {
    const m = el('[name="' + nev + '"]');
    if (m && v !== null && v !== undefined) m.value = String(v);
  };

  /* Ékezetérzéketlen összehasonlítás a településnevekhez: a látogató
     „Csikvand"-ot is beírhat. */
  const kulcs = (s) => String(s || '')
    .toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '');

  /* ==========================================================================
     1. SZÁMÍTÁS
     --------------------------------------------------------------------------
     Egyetlen képlet fedi le mind a három gyakorlatban előforduló díjszabást:

       elszámolt m³ = max(elszállított m³, a minimumdíjban foglalt m³)
       alapdíj      = max(minimumdíj, ürítési díj × elszámolt m³)
       alkalmi díj  = kiszállási díj + alapdíj + távolsági díj + egyéb

     Miért ez az egy képlet elég:
       · nincs minimumdíj (0 Ft, 0 m³)  → alkalmi = kiszállás + ürítés × m³
       · a minimumdíj csak alsó korlát  → a max() emeli fel a kis mennyiséget
       · a minimumdíj X m³-t tartalmaz  → az elszámolt m³ sosem kevesebb X-nél
       · a teljes kocsit ki kell fizetni → X = a kocsi űrtartalma

     A „minimum-felár" az a rész, amit a látogató KIFIZET, de nem visz el:
     alapdíj − (ürítési díj × ténylegesen elszállított m³). Ez sosem negatív,
     mert az alapdíj definíció szerint nagyobb-egyenlő ennél.
     ========================================================================== */
  function szamol() {
    const alkalom = Math.max(0, ertek('alkalom'));
    const m3 = ertek('m3');
    const kocsiM3 = Math.min(KOCSI_MAX, Math.max(KOCSI_MIN, ertek('kocsiM3', KOCSI_MIN)));
    /* A foglalt mennyiség 0-tól a kocsi űrtartalmáig terjedhet — ennél többet
       egyetlen fuvarra nem lehet kiszámlázni. */
    const minimumM3 = Math.min(kocsiM3, ertek('minimumM3'));

    const kiszallas = ertek('kiszallas');
    const uritesM3 = ertek('uritesM3');
    const minimumDij = ertek('minimumDij');
    const km = ertek('kmDij') * ertek('tavolsagKm');
    const egyeb = ertek('egyeb');

    const elszamoltM3 = Math.max(m3, minimumM3);
    const uritesValos = uritesM3 * m3;
    const alapDij = Math.max(minimumDij, uritesM3 * elszamoltM3);
    const minimumFelar = Math.max(0, alapDij - uritesValos);

    const alkalmi = kiszallas + alapDij + km + egyeb;

    return {
      alkalom, m3, kocsiM3, minimumM3, elszamoltM3,
      kiszallas, uritesValos, minimumFelar, km, egyeb,
      alkalmi,
      eves: alkalmi * alkalom,
      /* Fajlagos díj arra, amit ténylegesen elvitetnek. Ez a szám mondja meg,
         megérte-e a kis adag: 1 m³-nél a kiszállás és a minimum ráterhelődik. */
      fajlagos: m3 > 0 ? alkalmi / m3 : null,
      /* Ugyanez akkor, ha a látogató a foglalt mennyiséget (vagy a kocsit)
         kihasználná — a kalkulátor ezzel mutatja meg a jobb utat. */
      fajlagosTeli: elszamoltM3 > 0
        ? (kiszallas + Math.max(minimumDij, uritesM3 * elszamoltM3) + km + egyeb) / elszamoltM3
        : null,
      /* Hány m³-t fizet ki úgy, hogy nem viszik el. */
      nemVittM3: Math.max(0, elszamoltM3 - m3),
      /* Tartálykihasználás: ez az egyetlen szám, amit a JÁRMŰMÉRET önmagában
         mozgat. A díjat nem a kocsi mérete adja, hanem a foglalt mennyiség és
         az ürítési díj — a kihasználás viszont megmutatja, mennyire éri meg
         kihívni ekkora autót. */
      kihasznalas: kocsiM3 > 0 ? Math.min(1, m3 / kocsiM3) : 0
    };
  }

  /* ==========================================================================
     2. KIÍRÁS
     ========================================================================== */

  /* Számláló-animáció. A végérték AZONNAL a DOM-ba kerül (`textContent`), és
     csak utána indul a visszaszámolás — így ha az animáció bármiért elmarad,
     a helyes érték áll ott, nem a kiindulási nulla. */
  const elozo = new WeakMap();
  function irSzam(cel, uj, formazo) {
    if (!cel) return;
    cel.textContent = formazo(uj);
    if (halkMozgas.matches) { elozo.set(cel, uj); return; }
    const regi = elozo.get(cel);
    elozo.set(cel, uj);
    if (regi === undefined || regi === uj || !isFinite(regi)) return;

    const kezdet = performance.now();
    const ido = 420;
    const lep = (most) => {
      const t = Math.min(1, (most - kezdet) / ido);
      /* ease-out: a szám gyorsan indul és lágyan áll be */
      const k = 1 - Math.pow(1 - t, 3);
      cel.textContent = formazo(regi + (uj - regi) * k);
      if (t < 1) requestAnimationFrame(lep);
    };
    requestAnimationFrame(lep);
  }

  const kiUgras = (nev) => el('[data-szip-ki="' + nev + '"]');

  function kiir(a) {
    irSzam(kiUgras('alkalom'), a.alkalmi, forint);
    irSzam(kiUgras('ev'), a.eves, forint);
    irSzam(kiUgras('elszamolt'), a.elszamoltM3, kobmeter);

    const fajl = kiUgras('fajlagos');
    if (fajl) {
      fajl.textContent = a.fajlagos === null ? '—' : forint(a.fajlagos) + '/m³';
      elozo.set(fajl, a.fajlagos || 0);
    }

    /* --- költségsáv: minden szelet a saját arányát kapja meg -------------- */
    const ossz = a.alkalmi > 0 ? a.alkalmi : 1;
    const reszek = {
      kiszallas: a.kiszallas,
      urites: a.uritesValos,
      minimum: a.minimumFelar,
      km: a.km,
      egyeb: a.egyeb
    };
    Object.keys(reszek).forEach((k) => {
      const szelet = el('[data-szip-sav-elem="' + k + '"]');
      if (szelet) {
        szelet.style.setProperty('--szip-arany', String(reszek[k] / ossz));
        /* Nulla forintos tétel nem kap sávot és nem kap sorszámot sem a
           képernyőolvasóban — de a jelmagyarázatban ott marad az értéke. */
        szelet.hidden = reszek[k] <= 0;
      }
      const cimke = el('[data-szip-tetel="' + k + '"]');
      if (cimke) cimke.textContent = forint(reszek[k]);
    });

    const savOssz = el('[data-szip-sav]');
    if (savOssz) {
      savOssz.setAttribute('aria-label',
        'Az alkalmankénti díj összetétele: ' +
        'kiszállási díj ' + forint(a.kiszallas) + ', ' +
        'ürítési díj az elszállított mennyiségre ' + forint(a.uritesValos) + ', ' +
        'minimumdíj-felár ' + forint(a.minimumFelar) + ', ' +
        'távolsági díj ' + forint(a.km) + ', ' +
        'egyéb ' + forint(a.egyeb) + '. Összesen ' + forint(a.alkalmi) + '.');
    }

    /* --- tartálymérő ------------------------------------------------------ */
    const tank = el('[data-szip-tank]');
    if (tank) {
      const kocsi = a.kocsiM3 > 0 ? a.kocsiM3 : 1;
      tank.style.setProperty('--szip-toltes', String(Math.min(1, a.m3 / kocsi)));
      tank.style.setProperty('--szip-fizetett', String(Math.min(1, a.elszamoltM3 / kocsi)));
      tank.style.setProperty('--szip-minimum', String(Math.min(1, a.minimumM3 / kocsi)));
      tank.setAttribute('aria-label',
        'Szippantóautó tartálya ' + kobmeter(a.kocsiM3) + '. Elszállított mennyiség ' +
        kobmeter(a.m3) + ', kiszámlázott mennyiség ' + kobmeter(a.elszamoltM3) + '.');
    }
    const cimkeSet = {
      m3: kobmeter(a.m3),
      fizetett: kobmeter(a.elszamoltM3),
      kocsi: kobmeter(a.kocsiM3),
      kihasznalas: szazalek.format(a.kihasznalas)
    };
    Object.keys(cimkeSet).forEach((k) => {
      const c = el('[data-szip-tank-cimke="' + k + '"]');
      if (c) c.textContent = cimkeSet[k];
    });

    /* --- figyelmeztetés: kifizetett, de el nem szállított mennyiség --------
       Négy külön adatcella, nem egyetlen mondat: négy szám egy bekezdésbe
       fűzve olvashatatlan volt. */
    const jelzes = el('[data-szip-jelzes]');
    if (jelzes) {
      const van = a.nemVittM3 > 0.01 && a.minimumFelar > 0;
      jelzes.hidden = !van;
      if (van) {
        const cellak = {
          nemVitt: kobmeter(a.nemVittM3),
          alkalom: forint(a.minimumFelar),
          ev: forint(a.minimumFelar * a.alkalom),
          teli: a.fajlagosTeli === null ? '—' : forint(a.fajlagosTeli) + '/m³'
        };
        Object.keys(cellak).forEach((k) => {
          const c = el('[data-szip-jelzes-ertek="' + k + '"]');
          if (c) c.textContent = cellak[k];
        });
      }
    }

    /* --- a rajz mérete és beosztása követi a járműméretet ------------------ */
    jarmuMeret(a.kocsiM3);
  }

  /* ==========================================================================
     2/b. A RAJZ MÉRETE ÉS KÖBMÉTER-BEOSZTÁSA
     --------------------------------------------------------------------------
     A járműméret választása addig csak a töltés ARÁNYÁT mozgatta, magán a
     rajzon nem látszott — jogos kifogás volt, hogy „csak a rajzon nem változik
     semmi". Két dolog teszi láthatóvá:

       1. a jármű vízszintesen nyúlik (0,94 … 1,06): egy 12 m³-es kocsi
          láthatóan hosszabb, mint egy 3 m³-es. A tartomány szándékosan szűk —
          nagyobb nyújtás a kerekeket ellipszissé lapítaná;
       2. a tartály tetején KÖBMÉTERENKÉNT egy vonalka fut. Ettől lesz a rajz
          mérőeszköz: nyolc osztás nyolc köbmétert jelent, tizenegy tizenegyet.
     ========================================================================== */
  const SVGNS = 'http://www.w3.org/2000/svg';
  /* A gyorsválasztók szélső értékei adják a rajz nyújtási tartományát. Ha a
     konfigban módosulnak a járműméretek, a rajz magától követi. */
  const SAV_MIN = KOCSI_SAVOK.length
    ? Math.min.apply(null, KOCSI_SAVOK.map((x) => Number(x.ertek))) : 3;
  const SAV_MAX = KOCSI_SAVOK.length
    ? Math.max.apply(null, KOCSI_SAVOK.map((x) => Number(x.ertek))) : 12;
  let utolsoKocsi = null;

  function jarmuMeret(kocsiM3) {
    if (kocsiM3 === utolsoKocsi) return;
    utolsoKocsi = kocsiM3;

    const svg = el('[data-szip-tank]');
    if (!svg) return;

    /* A nyújtás a GYAKORLATI járműtartományra van vetítve (a legkisebb és a
       legnagyobb konfigurált gyorsválasztó közé), nem a mező megengedett
       végleteire: 1 és 20 m³ közé vetítve a valóságban előforduló 4 és 11 m³
       között alig lett volna látható különbség. A tartományon kívüli értékek
       a két végponton megállnak. */
    const t = (kocsiM3 - SAV_MIN) / Math.max(1, SAV_MAX - SAV_MIN);
    svg.style.setProperty('--szip-kocsi-arany',
      (0.90 + Math.max(0, Math.min(1, t)) * 0.22).toFixed(3));

    const skala = el('[data-szip-skala]', svg);
    if (!skala) return;
    skala.textContent = '';
    const db = Math.round(kocsiM3);
    /* Húsz osztás fölött a vonalkák összeérnének; ilyenkor kettesével lépünk. */
    const lepes = db > 20 ? 2 : 1;
    for (let i = lepes; i < db; i += lepes) {
      const x = 150 + 300 * (i / kocsiM3);
      const v = document.createElementNS(SVGNS, 'line');
      /* Minden ötödik vonalka hosszabb — így a beosztás számolható. */
      const hosszu = i % 5 === 0;
      v.setAttribute('x1', x.toFixed(1));
      v.setAttribute('x2', x.toFixed(1));
      v.setAttribute('y1', '98');
      v.setAttribute('y2', hosszu ? '114' : '107');
      v.setAttribute('class', hosszu ? 'szip-rajz-osztas szip-rajz-osztas-fo'
                                     : 'szip-rajz-osztas');
      skala.append(v);
    }
  }

  /* Késleltetett összegzés a képernyőolvasónak. A látható számokon nincs
     `aria-live`; itt egyetlen mondat megy ki, és csak akkor, ha a látogató
     abbahagyta a gépelést. */
  let eloIdozito = 0;
  function eloBemond(a) {
    const cel = el('[data-szip-elo]');
    if (!cel) return;
    clearTimeout(eloIdozito);
    eloIdozito = setTimeout(() => {
      let mondat = 'Éves szippantási költség ' + forint(a.eves)
        + ', alkalmanként ' + forint(a.alkalmi) + '.';
      if (a.nemVittM3 > 0.01 && a.minimumFelar > 0) {
        mondat += ' Ebből ' + forint(a.minimumFelar)
          + ' olyan mennyiségre jut, amit nem szállítanak el.';
      }
      cel.textContent = mondat;
    }, 900);
  }

  /* ==========================================================================
     3. CSEMPETÉRKÉP — a díjadatbázis állapota
     --------------------------------------------------------------------------
     Nem földrajzi térkép: azonos méretű csempék, a valós kelet–nyugati és
     észak–déli sorrendben. Pontos határvonalat nem rajzolunk, mert arra
     nincs hiteles forrásunk — a csempe viszont nem is állít ilyet.
     ========================================================================== */
  function telepulesekMegyeben(kod) {
    return DIJAK.filter((d) => d && d.megye === kod);
  }

  function terkepEpit() {
    const doboz = el('[data-szip-terkep]');
    if (!doboz || !MEGYEK.length) return;

    const lista = document.createElement('ul');
    lista.className = 'szip-terkep-racs';
    lista.setAttribute('role', 'list');

    MEGYEK.forEach((m) => {
      const db = telepulesekMegyeben(m.kod).length;
      const li = document.createElement('li');
      li.className = 'szip-terkep-cella';
      li.style.setProperty('--szip-sor', String(m.sor));
      li.style.setProperty('--szip-oszlop', String(m.oszlop));
      /* Lépcsős megjelenés: a sorrend a rácshelyből jön, hogy a térkép
         északnyugatról délkelet felé „épüljön fel". Görgetésvezérelt
         animációnál nem késleltetés, hanem eltolt animációs TARTOMÁNY adja a
         lépcsőt — ezért sorszám megy át, nem ezredmásodperc. */
      li.style.setProperty('--szip-lepcso', String(m.sor + m.oszlop));

      const gomb = document.createElement('button');
      gomb.type = 'button';
      gomb.className = 'szip-csempe';
      gomb.dataset.kod = m.kod;
      gomb.dataset.allapot = db > 0 ? 'van' : 'nincs';
      gomb.setAttribute('aria-pressed', 'false');

      const nev = document.createElement('span');
      nev.className = 'type-ui-label szip-csempe-nev';
      nev.textContent = m.rovid;

      const db_ = document.createElement('span');
      db_.className = 'type-data-value szip-csempe-db';
      db_.textContent = db > 0 ? String(db) : '—';

      /* A képernyőolvasónak a teljes név és a valódi állapot kell, nem a
         rövidítés és a gondolatjel. */
      const rejtett = document.createElement('span');
      rejtett.className = 'visually-hidden';
      rejtett.textContent = m.nev + ' — '
        + (db > 0 ? db + ' településről van díjadatunk' : 'még nincs díjadatunk');

      gomb.append(nev, db_, rejtett);
      li.append(gomb);
      lista.append(li);

    });

    doboz.textContent = '';
    doboz.append(lista);

    doboz.addEventListener('click', (e) => {
      const gomb = e.target.closest('.szip-csempe');
      if (gomb) valasztMegye(gomb.dataset.kod, true);
    });
  }

  function terkepOsszeg() {
    const cel = el('[data-szip-terkep-osszeg]');
    if (!cel) return;
    const telepulesek = new Set(DIJAK.map((d) => d && d.megye + '|' + kulcs(d.telepules)));
    telepulesek.delete('undefined|');
    const megyekAdattal = new Set(DIJAK.map((d) => d && d.megye)).size;

    cel.textContent = telepulesek.size === 0
      ? 'Az adatbázis most indul: még egyetlen település díjszabása sincs benne megerősített forrásból.'
      : telepulesek.size + ' település díjszabása van benne, ' + megyekAdattal
        + ' vármegyéből. A hiányzó helyeket a beküldésekből töltjük fel.';
  }

  /* Megyeválasztás — a csempéről és a legördülőből is ugyanide fut be. */
  let aktivMegye = '';
  function valasztMegye(kod, gorgess) {
    aktivMegye = kod || '';
    mind('.szip-csempe').forEach((g) => {
      g.setAttribute('aria-pressed', g.dataset.kod === aktivMegye ? 'true' : 'false');
    });
    const valaszto = el('[name="megye"]');
    if (valaszto && valaszto.value !== aktivMegye) valaszto.value = aktivMegye;

    telepuleslistaFrissit();
    megyeReszlet();

    if (gorgess) {
      const cel = el('[data-szip-terkep-reszlet]');
      if (cel && !halkMozgas.matches) cel.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  function megyeReszlet() {
    const cel = el('[data-szip-terkep-reszlet]');
    if (!cel) return;
    if (!aktivMegye) {
      cel.textContent = 'Válasszon vármegyét a térképen, és megmutatjuk, mely településekről van már díjadatunk.';
      return;
    }
    const megye = MEGYEK.find((m) => m.kod === aktivMegye);
    const sorok = telepulesekMegyeben(aktivMegye);
    if (!megye) return;
    if (!sorok.length) {
      cel.textContent = megye.nev + ': innen még egyetlen település díjszabását sem ismerjük '
        + 'ellenőrzött forrásból. Ha ismeri a sajátját, az alábbi űrlapon beküldheti — '
        + 'a következő érdeklődő már azt fogja látni.';
      return;
    }
    cel.textContent = megye.nev + ': ' + sorok.length + ' településről van adatunk — '
      + sorok.map((s) => s.telepules).join(', ') + '.';
  }

  /* A településmező javaslatlistája: KIZÁRÓLAG azok a helyek, amelyekről
     tényleg van adatunk. Teljes magyar településlistát nem kínálunk fel —
     az azt sugallná, hogy mindegyikhez tartozik díjszabás. */
  function telepuleslistaFrissit() {
    const lista = document.getElementById('szip-telepulesek');
    if (!lista) return;
    lista.textContent = '';
    DIJAK
      .filter((d) => d && (!aktivMegye || d.megye === aktivMegye))
      .forEach((d) => {
        const o = document.createElement('option');
        o.value = d.telepules;
        lista.append(o);
      });
  }

  /* Ha a beírt településhez van adatunk, felkínáljuk a díjak betöltését.
     MAGÁTÓL NEM ÍRJUK FELÜL a látogató által beírt értéket — az ő számlája
     erősebb forrás, mint a mi adatbázisunk. */
  function telepulesTalalat() {
    const jel = el('[data-szip-talalat]');
    const gomb = el('[data-szip-betolt]');
    if (!jel) return;
    const nev = el('[name="telepules"]');
    const k = kulcs(nev && nev.value);
    const talalt = k
      ? DIJAK.find((d) => d && kulcs(d.telepules) === k && (!aktivMegye || d.megye === aktivMegye))
      : null;

    if (talalt) {
      jel.textContent = talalt.telepules + ': ismerjük a díjszabást'
        + (talalt.szolgaltato ? ' (' + talalt.szolgaltato + ')' : '')
        + (talalt.ervenyes ? ', ' + talalt.ervenyes + ' szerint' : '') + '.';
      jel.hidden = false;
      if (gomb) { gomb.hidden = false; gomb.dataset.kod = talalt.megye + '|' + kulcs(talalt.telepules); }
    } else {
      jel.textContent = k
        ? 'Erről a településről még nincs díjadatunk. Írja be a saját számláján szereplő díjakat — és ha megosztja velünk, felvesszük az adatbázisba.'
        : '';
      jel.hidden = !k;
      if (gomb) gomb.hidden = true;
    }
    return talalt;
  }

  function dijakBetolt() {
    const t = telepulesTalalat();
    if (!t) return;
    ['kiszallas', 'uritesM3', 'minimumDij', 'minimumM3', 'kocsiM3', 'kmDij'].forEach((k) => {
      if (t[k] !== null && t[k] !== undefined) beir(k, t[k]);
    });
    peldaJelzesLevesz();
    frissit();
  }

  /* ==========================================================================
     4. PÉLDAÉRTÉKEK
     --------------------------------------------------------------------------
     A kalkulátor működő számpéldával indul, mert üres mezőkkel nem mutat semmit.
     A felület viszont VÉGIG jelzi, hogy ezek példák — és amint a látogató
     hozzányúl egy mezőhöz, arról a mezőről lekerül a jelzés.
     ========================================================================== */
  const PELDA_MEZOK = ['alkalom', 'm3', 'kiszallas', 'uritesM3',
                       'minimumDij', 'minimumM3', 'kocsiM3'];

  function peldaBetolt() {
    Object.keys(PELDA).forEach((k) => beir(k, PELDA[k]));
    mind('[data-szip-pelda]').forEach((j) => { j.hidden = false; });
    const savJel = el('[data-szip-pelda-sav]');
    if (savJel) savJel.hidden = false;
    frissit();
  }

  function peldaJelzesLevesz(mezoNev) {
    if (mezoNev) {
      const j = el('[data-szip-pelda="' + mezoNev + '"]');
      if (j) j.hidden = true;
    } else {
      mind('[data-szip-pelda]').forEach((j) => { j.hidden = true; });
    }
    /* A sáv fölötti figyelmeztetés addig marad, amíg akár EGY mező is
       példaértéken áll — különben eltűnne, mielőtt igaz lenne. */
    const savJel = el('[data-szip-pelda-sav]');
    if (savJel) {
      savJel.hidden = !mind('[data-szip-pelda]').some((j) => !j.hidden);
    }
  }

  /* ==========================================================================
     5. ÉRTÉKEK ÁTMÁSOLÁSA A BEKÜLDŐ ŰRLAPBA
     ========================================================================== */
  function atmasol() {
    const urlap = document.querySelector('[data-szip-urlap]');
    if (!urlap) return;
    const parok = {
      megye: el('[name="megye"]') && el('[name="megye"]').value,
      telepules: el('[name="telepules"]') && el('[name="telepules"]').value,
      kiszallas: ertek('kiszallas'),
      uritesM3: ertek('uritesM3'),
      minimumDij: ertek('minimumDij'),
      minimumM3: ertek('minimumM3'),
      kocsiM3: ertek('kocsiM3'),
      kmDij: ertek('kmDij')
    };
    Object.keys(parok).forEach((k) => {
      const m = urlap.querySelector('[name="' + k + '"]');
      if (m && parok[k] !== undefined && parok[k] !== null && parok[k] !== '') {
        m.value = String(parok[k]);
      }
    });
    const vissza = urlap.querySelector('[data-szip-atmasolva]');
    if (vissza) {
      vissza.textContent = 'A kalkulátorban megadott értékeket átemeltük ide. '
        + 'Nézze át őket, és egészítse ki a forrással — csak igazolt adatot veszünk fel.';
      vissza.hidden = false;
    }
    const elso = urlap.querySelector('[name="telepules"]');
    if (elso) elso.focus();
  }

  /* ==========================================================================
     6. BEKÖTÉS
     ========================================================================== */
  function frissit() {
    const a = szamol();
    kiir(a);
    eloBemond(a);
  }

  /* Minden mezőváltozás újraszámol. `input` és nem `change`: a szám azonnal
     kövesse a gépelést — a modul lényege épp az, hogy látni lehessen, mi
     mozgatja a költséget. */
  gyoker.addEventListener('input', (e) => {
    const nev = e.target.name;
    if (nev && PELDA_MEZOK.indexOf(nev) !== -1) peldaJelzesLevesz(nev);
    if (nev === 'telepules') telepulesTalalat();
    if (nev === 'megye') valasztMegye(e.target.value, false);
    frissit();
  });

  gyoker.addEventListener('click', (e) => {
    const kocsiGomb = e.target.closest('[data-szip-kocsi]');
    if (kocsiGomb) {
      beir('kocsiM3', kocsiGomb.dataset.szipKocsi);
      peldaJelzesLevesz('kocsiM3');
      mind('[data-szip-kocsi]').forEach((g) => {
        g.setAttribute('aria-pressed', g === kocsiGomb ? 'true' : 'false');
      });
      frissit();
      return;
    }
    if (e.target.closest('[data-szip-pelda-gomb]')) { peldaBetolt(); return; }
    if (e.target.closest('[data-szip-betolt]')) { dijakBetolt(); return; }
    if (e.target.closest('[data-szip-atmasol]')) { atmasol(); }
  });

  /* Kocsi-gyorsválasztók feliratának feltöltése a konfigból — a HTML-ben csak
     a hely áll, hogy a méretek egyetlen forrásból jöjjenek. */
  function kocsiGombokEpit() {
    const doboz = el('[data-szip-kocsi-sor]');
    if (!doboz || !KOCSI_SAVOK.length) return;
    doboz.textContent = '';
    KOCSI_SAVOK.forEach((s) => {
      const g = document.createElement('button');
      g.type = 'button';
      g.className = 'szip-kocsi-gomb';
      g.dataset.szipKocsi = String(s.ertek);
      g.setAttribute('aria-pressed', 'false');
      const nev = document.createElement('span');
      nev.className = 'type-ui-button szip-kocsi-nev';
      nev.textContent = s.nev;
      const jelzo = document.createElement('span');
      jelzo.className = 'type-data-value szip-kocsi-jelzo';
      jelzo.textContent = s.jelzo;
      g.append(nev, jelzo);
      doboz.append(g);
    });
  }

  /* Megyeválasztó feltöltése — ugyanabból a listából, mint a térkép. */
  function megyeValasztoEpit() {
    const v = el('[name="megye"]');
    if (!v) return;
    MEGYEK.forEach((m) => {
      const o = document.createElement('option');
      o.value = m.kod;
      o.textContent = m.nev;
      v.append(o);
    });
    /* A beküldő űrlap ugyanezt a listát kapja. */
    const v2 = document.querySelector('[data-szip-urlap] [name="megye"]');
    if (v2) {
      MEGYEK.forEach((m) => {
        const o = document.createElement('option');
        o.value = m.kod;
        o.textContent = m.nev;
        v2.append(o);
      });
    }
  }

  megyeValasztoEpit();
  kocsiGombokEpit();
  terkepEpit();
  terkepOsszeg();
  telepuleslistaFrissit();
  megyeReszlet();
  peldaBetolt();

  /* A számoló felület csak most válik láthatóvá: JS nélkül a `<noscript>`
     szövege áll a helyén, és nem villan fel egy üres, működésképtelen mezősor.
     A beküldő űrlapon nincs ilyen jelölés — az JS nélkül is elmegy. */
  mind('[data-szip-vart]').forEach((e) => e.removeAttribute('data-szip-vart'));
})();
