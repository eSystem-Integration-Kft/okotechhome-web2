/* =============================================================================
   ÖkoTech Home — Test2 · konzultacio.js
   A konzultációkérő varázsló — progressive enhancement
   -----------------------------------------------------------------------------
   AMIT JS NÉLKÜL IS TUD az űrlap: minden lap egyszerre látszik, a natív
   `required` ellenőrzés működik, és egyetlen POST megy a végpontra. A beküldést
   az urlap.js fogja el (az is opcionális), a szerver pedig JS nélküli POST-ra
   is választ ad.

   AMIT EZ A FÁJL HOZZÁTESZ:
     1. lapozás + haladásjelző,
     2. feltételes blokkok (`data-konzv-ha`),
     3. időpont-sávok naptárrácsból — az érték a szöveges mezőbe íródik,
        tehát a szerver felé ugyanaz a mező megy JS-sel és anélkül,
     4. mentés localStorage-ba, hogy a félbehagyott kitöltés folytatható legyen,
     5. kitöltéssegéd: a szabad szöveges leírásból az api/konzultacio-kitoltes
        végpont strukturált mezőket ad vissza, és azokat beírjuk — CSAK az üres
        mezőkbe, hogy a látogató válaszát soha ne írja felül a gép.

   A NAPTÁR NEM FOGLALÁS. Csak preferenciát rögzít: a látogató sávokat jelöl, a
   visszaigazolás e-mailben jön. Ezért nem kell hozzá szabad időpontokat
   lekérdezni, és nem is keletkezhet ütköző foglalás.
   ============================================================================= */

(() => {
  'use strict';

  const urlap = document.querySelector('[data-konzv]');
  if (!urlap) return;

  const TAROLO = 'oth-konzultacio-v1';
  const lapok = [...urlap.querySelectorAll('[data-konzv-lap]')];
  const lepcso = urlap.querySelector('[data-konzv-lepcso]');
  const jelzok = [...urlap.querySelectorAll('[data-konzv-jelzo]')];
  const vissza = urlap.querySelector('[data-konzv-vissza]');
  const tovabb = urlap.querySelector('[data-konzv-tovabb]');
  const kuldes = urlap.querySelector('.urlap-kuldes');
  const osszegzes = urlap.querySelector('[data-konzv-osszegzes]');
  const osszLista = urlap.querySelector('[data-konzv-osszegzes-lista]');
  if (!lapok.length) return;

  let aktiv = 0;

  /* ---------------------------------------------------------------- lapozás */
  urlap.classList.add('is-lapozo');
  if (lepcso) lepcso.hidden = false;
  if (tovabb) tovabb.hidden = false;

  function mutat(i, fokusz = true) {
    /* Az irány vezérli a belépő animációt: előre jobbról, vissza balról.
       Enélkül a lapok ugranak, és nem érződik, hogy egy folyamatban haladunk. */
    urlap.classList.toggle('is-vissza', i < aktiv);
    aktiv = Math.max(0, Math.min(i, lapok.length - 1));
    lapok.forEach((l, n) => { l.hidden = n !== aktiv; });
    jelzok.forEach((j, n) => {
      j.classList.toggle('is-aktiv', n === aktiv);
      j.classList.toggle('is-kesz', n < aktiv);
    });
    const utolso = aktiv === lapok.length - 1;
    if (vissza) vissza.hidden = aktiv === 0;
    if (tovabb) tovabb.hidden = utolso;
    if (kuldes) kuldes.hidden = !utolso;
    if (osszegzes) {
      osszegzes.hidden = !utolso;
      if (utolso) osszegzesFrissit();
    }
    /* A kísérő (kalauz.js) ebből tudja, melyik lapon állunk. Esemény, nem
       közvetlen hívás: a két szkript egymás nélkül is működik. */
    document.dispatchEvent(new CustomEvent('konzv:lap', {
      detail: { lap: aktiv + 1, utolso: aktiv === lapok.length - 1 }
    }));
    if (fokusz) {
      const cim = lapok[aktiv].querySelector('.konzv-lap-cim');
      if (cim) { cim.setAttribute('tabindex', '-1'); cim.focus({ preventScroll: true }); }
      lapok[aktiv].scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    }
  }

  /* --------------------------------------------------------- hibaüzenetek */
  /* NEM a böngésző natív buborékja: az pár másodperc után eltűnik, a szövege
     böngészőnként más, és rejtett lapon meg sem jelenik. A saját üzenet a
     mező ALATT áll, magyarul, és addig marad, amíg a hibát nem javítják. */
  function hibaSzoveg(m) {
    const v = m.validity;
    if (v.valueMissing) {
      if (m.type === 'radio') return 'Kérjük, válasszon egyet a lehetőségek közül.';
      if (m.type === 'checkbox') return 'A folytatáshoz ezt be kell jelölni.';
      if (m.tagName === 'SELECT') return 'Kérjük, válasszon a listából.';
      if (m.type === 'email') return 'Kérjük, adja meg az e-mail-címét.';
      return 'Ez a mező kötelező.';
    }
    if (v.typeMismatch && m.type === 'email') return 'Kérjük, érvényes e-mail-címet adjon meg — például nev@pelda.hu.';
    if (v.rangeUnderflow || v.rangeOverflow) return `${m.min}–${m.max} közötti szám lehet.`;
    if (v.badInput) return 'Kérjük, számot írjon ide.';
    return m.validationMessage || 'Kérjük, ellenőrizze a mezőt.';
  }

  /* A hiba nem a mezőn ül, hanem a mező DOBOZÁN: rádióknál a kártyacsoporton,
     jelölőnél a soron — a látogató a csoportot látja egynek, nem az inputot. */
  function hibaDoboz(m) {
    return m.closest('.urlap-mezo') || m.closest('.konzv-valasztok')
        || m.closest('.urlap-jelolo') || m.parentElement;
  }

  function hibaJelez(m) {
    const doboz = hibaDoboz(m);
    if (!doboz) return;
    /* LABEL-be nem teszünk üzenetet: a szövegére kattintás átbillentené magát
       a jelölőt — a hozzájárulást nem pipálhatja ki egy félrement kattintás.
       Ott az üzenet a label UTÁN áll, testvérként. */
    const cimkeE = doboz.tagName === 'LABEL';
    let p = cimkeE
      ? (doboz.nextElementSibling?.classList.contains('mezo-hiba') ? doboz.nextElementSibling : null)
      : doboz.querySelector('.mezo-hiba');
    if (!p) {
      p = document.createElement('p');
      p.className = 'type-ui-caption mezo-hiba';
      if (cimkeE) doboz.after(p); else doboz.appendChild(p);
    }
    p.textContent = hibaSzoveg(m);
    doboz.classList.add('is-hibas', 'is-raz');
    setTimeout(() => doboz.classList.remove('is-raz'), 420);
    m.setAttribute('aria-invalid', 'true');
  }

  function hibaTorol(kor) {
    kor.querySelectorAll('.mezo-hiba').forEach((p) => p.remove());
    kor.querySelectorAll('.is-hibas').forEach((d) => d.classList.remove('is-hibas', 'is-raz'));
    kor.querySelectorAll('[aria-invalid]').forEach((m) => m.removeAttribute('aria-invalid'));
  }

  /* Javításkor a hiba magától tűnik el — nem kell hozzá újra a Tovább. */
  urlap.addEventListener('input', hibaFigyel);
  urlap.addEventListener('change', hibaFigyel);
  function hibaFigyel(e) {
    const m = e.target;
    if (!(m instanceof Element)) return;
    const doboz = m.closest('.is-hibas');
    if (doboz && (typeof m.checkValidity !== 'function' || m.checkValidity())) {
      doboz.classList.remove('is-hibas', 'is-raz');
      doboz.querySelector('.mezo-hiba')?.remove();
      if (doboz.nextElementSibling?.classList.contains('mezo-hiba')) doboz.nextElementSibling.remove();
      doboz.querySelectorAll('[aria-invalid]').forEach((x) => x.removeAttribute('aria-invalid'));
    }
  }

  /* A rejtettség vizsgálatában a LAP a határ: teljes-űrlap ellenőrzéskor a lap
     maga is `hidden`, de a benne álló mezők attól még számítanak — csak a
     feltételes (ki nem nyitott) blokkok mezői nem. */
  function rosszMezok(lap) {
    return [...lap.querySelectorAll('input,select,textarea')].filter((m) => {
      const rejtett = m.closest('[hidden]');
      if (m.disabled || (rejtett && rejtett !== lap)) return false;
      return !m.checkValidity();
    });
  }

  function lapErvenyes(lap) {
    hibaTorol(lap);
    const rossz = rosszMezok(lap);
    if (!rossz.length) return true;
    rossz.forEach(hibaJelez);
    const elso = rossz[0];
    (hibaDoboz(elso) || elso).scrollIntoView({ block: 'center', behavior: 'smooth' });
    elso.focus({ preventScroll: true });
    return false;
  }

  tovabb?.addEventListener('click', () => {
    if (!lapErvenyes(lapok[aktiv])) return;
    mutat(aktiv + 1);
    ment();
  });
  vissza?.addEventListener('click', () => mutat(aktiv - 1));

  /* BEKÜLDÉS ELŐTT a teljes űrlapot végignézzük, nem csak az utolsó lapot: a
     vázlat-visszatöltés úgy is állhat a 6. lapon, hogy egy korábbi lap üres.
     Az első hibás laphoz visszaugrunk, és ott mutatjuk meg, mi hiányzik —
     a natív ellenőrzés egy rejtett lapon némán elakadna. */
  kuldes?.addEventListener('click', (e) => {
    for (let i = 0; i < lapok.length; i++) {
      if (!rosszMezok(lapok[i]).length) continue;
      e.preventDefault();
      if (i !== aktiv) mutat(i, false);
      lapErvenyes(lapok[i]);
      return;
    }
  });

  jelzok.forEach((j, n) => {
    j.addEventListener('click', () => { if (n < aktiv) mutat(n); });
  });

  /* ------------------------------------------------------- feltételes blokk */
  const felteteles = [...urlap.querySelectorAll('[data-konzv-ha]')];
  function feltetelekFrissit() {
    felteteles.forEach((blokk) => {
      const [nev, ertek] = blokk.dataset.konzvHa.split('=');
      const be = urlap.querySelector(`[name="${nev}"]:checked`);
      const kell = be && be.value === ertek;
      blokk.hidden = !kell;
      /* A rejtett blokk mezőit ki is kapcsoljuk: így nem küldünk olyan értéket,
         ami a látogató számára nem is látszott. */
      blokk.querySelectorAll('input,select,textarea').forEach((m) => { m.disabled = !kell; });
    });
  }
  urlap.addEventListener('change', () => { feltetelekFrissit(); ment(); });
  feltetelekFrissit();

  /* -------------------------------------------------------------- naptárrács */
  const racs = urlap.querySelector('[data-konzv-naptar-racs]');
  const idopontMezo = urlap.querySelector('[data-konzv-idopont]');
  const SAVOK = [['de', 'de. 9–12'], ['du', 'du. 13–16'], ['ke', 'késő 16–18']];
  const NAPNEV = ['vas', 'hét', 'ked', 'sze', 'csü', 'pén', 'szo'];
  const MAX_SAV = 3;
  const valasztott = new Set();

  if (racs && idopontMezo) {
    racs.hidden = false;
    const ma = new Date();
    let nap = new Date(ma.getFullYear(), ma.getMonth(), ma.getDate() + 1);
    let db = 0;
    while (db < 5) {
      const d = nap.getDay();
      if (d !== 0 && d !== 6) {                       // hétvégén nem egyeztetünk
        const oszlop = document.createElement('div');
        oszlop.className = 'konzv-nap';
        const fej = document.createElement('p');
        fej.className = 'konzv-nap-fej';
        /* A napnév és a dátum KÉT elem: a fejléc így oszlopcímkeként olvasható,
           nem a sávgombok negyedik soraként. A szöveges címke (a mezőbe és a
           levélbe kerülő alak) változatlan marad. */
        const napNev = NAPNEV[d];
        const napDatum = `${nap.getMonth() + 1}.${nap.getDate()}.`;
        const fejCimke = `${napNev} ${napDatum}`;
        const nevElem = document.createElement('span');
        nevElem.className = 'konzv-nap-nev';
        nevElem.textContent = napNev;
        const datumElem = document.createElement('span');
        datumElem.className = 'konzv-nap-datum';
        datumElem.textContent = napDatum;
        fej.append(nevElem, datumElem);
        oszlop.appendChild(fej);
        const datum = `${nap.getFullYear()}-${String(nap.getMonth() + 1).padStart(2, '0')}-${String(nap.getDate()).padStart(2, '0')}`;
        SAVOK.forEach(([kulcs, cimke]) => {
          const gomb = document.createElement('button');
          gomb.type = 'button';
          gomb.className = 'konzv-sav';
          gomb.textContent = cimke;
          gomb.setAttribute('aria-pressed', 'false');
          gomb.dataset.sav = `${datum}|${kulcs}`;
          gomb.dataset.cimke = `${fejCimke} ${cimke}`;
          gomb.addEventListener('click', () => savValt(gomb));
          oszlop.appendChild(gomb);
        });
        racs.appendChild(oszlop);
        db++;
      }
      nap = new Date(nap.getFullYear(), nap.getMonth(), nap.getDate() + 1);
    }
  }

  function savValt(gomb) {
    const kulcs = gomb.dataset.sav;
    if (valasztott.has(kulcs)) valasztott.delete(kulcs);
    else if (valasztott.size < MAX_SAV) valasztott.add(kulcs);
    else return;                                       // a negyediket nem vesszük fel
    gomb.setAttribute('aria-pressed', String(valasztott.has(kulcs)));
    savokIrasa();
    ment();
  }

  /* A kijelölt sávok a SZÖVEGES mezőbe íródnak. Egyetlen igazság megy a
     szerverre, és a látogató kézzel is hozzáírhat. */
  function savokIrasa() {
    if (!idopontMezo) return;
    const cimkek = [...racs.querySelectorAll('[aria-pressed="true"]')].map((g) => g.dataset.cimke);
    idopontMezo.value = cimkek.join(' · ');
    racs.querySelectorAll('.konzv-sav').forEach((g) => {
      g.disabled = valasztott.size >= MAX_SAV && g.getAttribute('aria-pressed') !== 'true';
    });
  }

  /* ------------------------------------------------------------- összegzés */
  function osszegzesFrissit() {
    if (!osszLista) return;
    osszLista.innerHTML = '';
    const adat = new FormData(urlap);
    const CIMKE = {
      ki: 'Megkereső', szegmens: 'Létesítmény', cegnev: 'Cég',
      fazis: 'Projektszakasz', jelenlegi: 'Jelenlegi megoldás',
      hasznalat: 'Használat', letszam: 'Létszám', csucs: 'Csúcsterhelés',
      telekmeret: 'Telekméret', talajviz: 'Talajvíz', kut: 'Kút',
      mod: 'Konzultáció módja', idopont: 'Időpontok', surgosseg: 'Sürgősség',
      nev: 'Név', email: 'E-mail', telefon: 'Telefon', telepules: 'Település',
    };
    const SZOVEG = {};
    urlap.querySelectorAll('option').forEach((o) => { if (o.value) SZOVEG[o.value] = o.textContent.trim(); });
    urlap.querySelectorAll('.konzv-valaszto input').forEach((r) => {
      const cim = r.parentElement.querySelector('.konzv-valaszto-cim');
      if (cim) SZOVEG[r.value] = cim.textContent.trim();
    });
    Object.entries(CIMKE).forEach(([nev, cimke]) => {
      const ertek = (adat.get(nev) || '').toString().trim();
      if (!ertek) return;
      const dt = document.createElement('dt'); dt.textContent = cimke;
      const dd = document.createElement('dd'); dd.textContent = SZOVEG[ertek] || ertek;
      osszLista.append(dt, dd);
    });
  }

  /* ------------------------------------------------- mentés és folytatás */
  const folytatas = urlap.querySelector('[data-konzv-folytatas]');
  let mentesIdozito = 0;

  function ment() {
    clearTimeout(mentesIdozito);
    mentesIdozito = setTimeout(() => {
      try {
        const adat = {};
        new FormData(urlap).forEach((ertek, kulcs) => {
          if (kulcs === 'weboldal' || kulcs === 'nyitva') return;
          if (adat[kulcs] === undefined) adat[kulcs] = ertek;
          else adat[kulcs] = [].concat(adat[kulcs], ertek);
        });
        /* Üres vázlatot nem mentünk: különben a puszta megnyitás után a
           következő látogatáskor „félbehagyott kitöltést" ajánlanánk fel,
           amiben nincs semmi. */
        const vanTartalom = Object.values(adat).some((e) => String(e).trim() !== '');
        if (!vanTartalom && !valasztott.size) { localStorage.removeItem(TAROLO); return; }
        localStorage.setItem(TAROLO, JSON.stringify({ adat, savok: [...valasztott], lap: aktiv, ido: Date.now() }));
      } catch { /* privát mód: a mentés kimarad, a kitöltés működik */ }
    }, 400);
  }

  function betolt(mentett) {
    Object.entries(mentett.adat || {}).forEach(([nev, ertek]) => {
      const ertekek = [].concat(ertek);
      urlap.querySelectorAll(`[name="${nev}"],[name="${nev}[]"]`).forEach((m) => {
        if (m.type === 'checkbox' || m.type === 'radio') {
          if (ertekek.includes(m.value)) m.checked = true;
        } else if (ertekek[0] !== undefined) {
          m.value = ertekek[0];
        }
      });
    });
    (mentett.savok || []).forEach((k) => {
      const gomb = racs?.querySelector(`[data-sav="${k}"]`);
      if (gomb) { valasztott.add(k); gomb.setAttribute('aria-pressed', 'true'); }
    });
    savokIrasa();
    feltetelekFrissit();
    mutat(Math.min(mentett.lap || 0, lapok.length - 1), false);
  }

  try {
    const nyers = localStorage.getItem(TAROLO);
    if (nyers && folytatas) {
      const mentett = JSON.parse(nyers);
      /* Két hétnél régebbi vázlatot nem ajánlunk fel: addigra a helyzet
         megváltozott, és a félig kitöltött régi adat többet árt, mint használ. */
      if (Date.now() - (mentett.ido || 0) < 14 * 24 * 3600e3) {
        folytatas.hidden = false;
        folytatas.querySelector('[data-konzv-folytat]').addEventListener('click', () => {
          betolt(mentett); folytatas.hidden = true;
        });
        folytatas.querySelector('[data-konzv-elvet]').addEventListener('click', () => {
          localStorage.removeItem(TAROLO); folytatas.hidden = true;
        });
      } else {
        localStorage.removeItem(TAROLO);
      }
    }
  } catch { /* sérült vázlat: figyelmen kívül */ }

  urlap.addEventListener('input', ment);
  urlap.addEventListener('submit', () => {
    try { localStorage.removeItem(TAROLO); } catch { /* nem baj */ }
  });

  /* ------------------------------------------------------- kitöltéssegéd */
  const leiras = urlap.querySelector('[data-konzv-leiras]');
  const aiGomb = urlap.querySelector('[data-konzv-ai-gomb]');
  const aiAllapot = urlap.querySelector('[data-konzv-ai-allapot]');

  function aiGombAllapot() {
    if (!aiGomb || !leiras) return;
    aiGomb.disabled = leiras.value.trim().length < 30;
  }
  leiras?.addEventListener('input', aiGombAllapot);
  aiGombAllapot();

  aiGomb?.addEventListener('click', async () => {
    if (!leiras) return;
    aiGomb.disabled = true;
    aiGomb.setAttribute('aria-busy', 'true');
    aiAllapot.className = 'type-ui-caption konzv-ai-allapot';
    aiAllapot.textContent = 'Olvasom a leírást…';
    try {
      const valasz = await fetch('api/konzultacio-kitoltes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ leiras: leiras.value.slice(0, 4000) }),
      });
      const eredmeny = await valasz.json();
      if (!valasz.ok || !eredmeny.ok) throw new Error(eredmeny.uzenet || 'Nem sikerült.');
      const betoltve = mezokBeirasa(eredmeny.mezok || {});
      aiAllapot.className = 'type-ui-caption konzv-ai-allapot is-kesz';
      aiAllapot.textContent = betoltve
        ? `${betoltve} mezőt kitöltöttem az előző lapokon — kérjük, nézze át őket.`
        : 'Nem találtam olyan adatot, amit be tudnék írni. Töltse ki a mezőket kézzel.';
    } catch (hiba) {
      aiAllapot.className = 'type-ui-caption konzv-ai-allapot is-hiba';
      aiAllapot.textContent = 'A segéd most nem érhető el — a mezőket kézzel is kitöltheti.';
    } finally {
      aiGomb.removeAttribute('aria-busy');
      aiGombAllapot();
    }
  });

  /* CSAK ÜRES mezőbe írunk. A gép javaslata soha nem írja felül azt, amit a
     látogató maga adott meg — az ő válasza az erősebb. */
  function mezokBeirasa(mezok) {
    let db = 0;
    Object.entries(mezok).forEach(([nev, ertek]) => {
      if (ertek === '' || ertek === null || ertek === undefined) return;
      const radiok = urlap.querySelectorAll(`input[type="radio"][name="${nev}"]`);
      if (radiok.length) {
        if ([...radiok].some((r) => r.checked)) return;
        const talalat = [...radiok].find((r) => r.value === String(ertek));
        if (talalat) { talalat.checked = true; db++; }
        return;
      }
      const mezo = urlap.querySelector(`[name="${nev}"]`);
      if (!mezo || mezo.value.trim() !== '') return;
      if (mezo.tagName === 'SELECT') {
        if (![...mezo.options].some((o) => o.value === String(ertek))) return;
      }
      mezo.value = String(ertek);
      db++;
    });
    if (db) { feltetelekFrissit(); ment(); }
    return db;
  }

  /* Induláskor az első lap látszik. */
  mutat(0, false);
})();
