/* ============================================================================
   ÖkoTech-Home — AI megoldás-ajánló (6. szekció)
   ----------------------------------------------------------------------------
   Forrás: `OkoTech-Home_AI-modul_fejlesztoi_specifikacio.2.docx` (2026-08-24).

   TERVEZÉSI ELVEK — ezek a specifikációból következnek, nem stílusdöntések:

   1. SZAKMAI ÁLLÍTÁS NINCS A KÓDBAN. Kérdés, válasz, magyarázat, döntési
      szabály, terméknév és kimeneti szöveg mind az `assets/data/ajanlo-konfig.js`
      fájlban él, amit a cég fejlesztő nélkül szerkeszthet. Ez a fájl csak
      kiértékel és kirajzol.

   2. KÉT SZINT, VÉGIG SZÉTVÁLASZTVA (spec 2.):
        · a TECHNOLÓGIÁT a használat jellege és a terhelés dönti el,
        · a MEGVALÓSÍTÁS FELTÉTELEIT a telek adottságai és a vízelhelyezés.
      A telek adottságai tehát nem választanak új technológiát — egyetlen
      kivétellel: a szabad terület a vízelhelyezés hiánya miatt kizáró lehet.

   3. A MODUL MEGNEVEZI A TERMÉKET, ahol a helyzet egyértelmű, és KIMONDJA a
      bizonytalanságot ott, ahol az fennáll. Határesetnél nem termékajánlás a
      kimenet, hanem az, hogy vegyes a kép — felsorolva, mi miatt.

   4. ADATOT NEM KÉRÜNK ÉS NEM KÜLDÜNK. A modul regisztráció és e-mail-cím
      nélkül indul, a válaszok a lapon maradnak. A záró képernyőn sincs
      kontaktadat-bekérés (spec 7.).

   JS NÉLKÜL: a szekció `<noscript>` blokkja írja le, mit kérdezne a modul, és
   felkínálja a személyes utat — a kérdéssor nem épül fel.
   ========================================================================== */
(() => {
  "use strict";

  const K = window.OTH_AJANLO;
  const gyoker = document.getElementById("ajanlo-root");
  if (!K || !gyoker) return;

  /* ------------------------------------------------------------- ÁLLAPOT */
  const allapot = {
    valaszok: {},      /* kérdésazonosító → válaszazonosító */
    aktiv: 0,          /* az AKTUÁLIS kérdés indexe a K.kerdesek tömbben */
    kesz: false        /* igaz, ha a kimenet látszik */
  };

  const kerdesSzam = K.kerdesek.length;

  /* --------------------------------------------------------- SEGÉDFÜGGVÉNYEK */
  const el = (tag, oszt, szoveg) => {
    const e = document.createElement(tag);
    if (oszt) e.className = oszt;
    if (szoveg != null) e.textContent = szoveg;
    return e;
  };

  /* A rajzolatok dekoratívak: a jelentést mindig a mellettük álló szöveg
     hordozza (designrendszer 8.), ezért `aria-hidden`. */
  const JEL = {
    ora:      '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    lakat:    '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    borotek:  '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    pipa:     '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    kor:      '<circle cx="12" cy="12" r="9"/>',
    folyamat: '<circle cx="12" cy="12" r="9" stroke-dasharray="3 3"/>',
    csepp:    '<path d="M12 3c3.5 4.2 5.5 7 5.5 9.6A5.5 5.5 0 0 1 12 18a5.5 5.5 0 0 1-5.5-5.4C6.5 10 8.5 7.2 12 3Z"/>',
    horgony:  '<circle cx="12" cy="5" r="2.2"/><path d="M12 7.2V20"/><path d="M7.5 11h9"/><path d="M4.5 15.5A8 8 0 0 0 12 20a8 8 0 0 0 7.5-4.5"/>',
    lejtes:   '<path d="M3 19h18"/><path d="M4 16 20 6"/>',
    szikra:   '<path d="M12 3.5 13.6 9 19 10.5 13.6 12 12 17.5 10.4 12 5 10.5 10.4 9Z"/><path d="M18 15.5l.7 2.3 2.3.7-2.3.7-.7 2.3-.7-2.3-2.3-.7 2.3-.7Z"/>',
    info:     '<circle cx="12" cy="12" r="9"/><path d="M12 11v5"/><path d="M12 8h.01"/>',
    figyelem: '<path d="M12 4 2.8 19.5h18.4Z"/><path d="M12 10v4"/><path d="M12 17h.01"/>'
  };

  /* A készlet fele VONALAS rajzolat (kontúr), a másik fele KITÖLTÖTT. A kettőt
     nem lehet ugyanazzal a `fill`/`stroke` beállítással megjeleníteni: a vonalas
     rajzolat kitöltve fekete folttá válik. A besorolás itt van, nem a hívás
     helyén — így egy új rajzolat felvételekor egy helyen kell dönteni. */
  const VONALAS = new Set(["ora", "lakat", "borotek", "pipa", "kor", "folyamat",
                           "horgony", "lejtes", "info", "figyelem"]);

  const svg = (nev, oszt) => {
    const s = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    s.setAttribute("viewBox", "0 0 24 24");
    s.setAttribute("aria-hidden", "true");
    const osztalyok = (oszt ? oszt + " " : "") + (VONALAS.has(nev) ? "ajanlo-jel-vonal" : "");
    if (osztalyok.trim()) s.setAttribute("class", osztalyok.trim());
    s.innerHTML = JEL[nev] || "";
    return s;
  };

  const ido = () => {
    const d = new Date();
    /* 24 órás alak, a magyar konvenció szerint (HH:mm). */
    return String(d.getHours()).padStart(2, "0") + ":" + String(d.getMinutes()).padStart(2, "0");
  };

  const lepesIndex = (lepesId) => K.lepesek.findIndex((l) => l.id === lepesId);
  const kerdesekLepesben = (lepesId) => K.kerdesek.filter((q) => q.lepes === lepesId);

  /* ==========================================================================
     KIÉRTÉKELÉS
     ========================================================================== */

  /* Első szakasz: a használat jellege + terhelés → technológiairány.
     A szabályok SORRENDBEN értékelődnek, az első illeszkedő nyer (spec 3.).
     Ha bármelyik bemenet hiányzik, egyetlen szabály sem illeszkedik. */
  function elsoSzakasz() {
    for (const sz of K.iranySzabalyok) {
      let talalat = true;
      for (const kulcs of Object.keys(sz.ha)) {
        if (!sz.ha[kulcs].includes(allapot.valaszok[kulcs])) { talalat = false; break; }
      }
      if (talalat) return { irany: sz.irany, ok: sz.ok || null };
    }
    return null;
  }

  /* Második szakasz: a telek adottságai. Ezek NEM választanak technológiát —
     feltételt szabnak vagy ellentmondást jeleznek. A szabad terület a kivétel:
     a vízelhelyezés hiánya kizáró ok (spec 4–5.). */
  function masodikSzakasz(elso) {
    const feltetelek = [], tisztazandok = [];
    const hozzaad = (t, id) => { if (!t.includes(id)) t.push(id); };

    for (const h of K.telekHatasok) {
      const kulcs = Object.keys(h.ha)[0];
      if (allapot.valaszok[kulcs] !== h.ha[kulcs]) continue;
      (h.feltetelek || []).forEach((f) => hozzaad(feltetelek, f));
      (h.tisztazandok || []).forEach((t) => hozzaad(tisztazandok, t));
    }

    let irany = elso ? elso.irany : null;
    let ellentmondas = null;

    /* KÉTLÉPCSŐS TERÜLET-KIÉRTÉKELÉS (spec 5.).
       1. lépcső: elég-e a terület az oldómedence szikkasztómezőjéhez?
       2. lépcső: elég-e a biológiai rendszer szivárogtatójához?
       A sorrend fordítva számít: ha a 2. lépcső bukik, az 1. már lényegtelen. */
    const sav = K.teruletSavok[allapot.valaszok.terulet];
    if (sav) {
      if (sav.biologiai === false) {
        irany = "zarttarolo";
        ellentmondas = "A vízelhelyezéshez rendelkezésre álló terület a biológiai rendszer szivárogtatójához sem elegendő. Ilyenkor nincs „kisebb helyigényű” szennyvíztisztító megoldás: szivárogtatás nélkül a szennyvizet gyűjteni és elszállíttatni kell.";
      } else if (sav.oldomedence === false && elso && elso.irany === "epureco") {
        irany = "egyeztetes";
        ellentmondas = "A használat alapján az oldómedencés irány jött volna ki, a rendelkezésre álló terület viszont az oldómedence szikkasztómezőjét nem engedi — az jellemzően a biológiai rendszer szivárogtatójának két-háromszorosa.";
      }
    }

    /* A kötelező tisztázandók a válaszoktól függetlenül megjelennek (spec 6.). */
    Object.keys(K.tisztazandok).forEach((id) => {
      if (K.tisztazandok[id].mindig) hozzaad(tisztazandok, id);
    });
    /* Amíg a szabad területre nincs válasz, az is nyitott kérdés. */
    if (!allapot.valaszok.terulet) hozzaad(tisztazandok, "terulet");

    return { irany: irany, feltetelek: feltetelek, tisztazandok: tisztazandok, ellentmondas: ellentmondas };
  }

  const kep = () => {
    const elso = elsoSzakasz();
    return { elso: elso, masodik: masodikSzakasz(elso) };
  };

  /* ==========================================================================
     BAL OLDAL — AZ ASSZISZTENS
     ========================================================================== */

  function sinRajzol(aktivLepes) {
    /* A sín a jobb oldali állapotpanel vizuális párja, ezért képernyőolvasónak
       nem mondjuk el kétszer ugyanazt. */
    const sin = el("ol", "ajanlo-sin");
    sin.setAttribute("aria-hidden", "true");
    K.lepesek.forEach((l, i) => {
      const p = el("li", "ajanlo-sin-pont");
      p.dataset.allapot = i < aktivLepes ? "kesz" : (i === aktivLepes ? "aktiv" : "nyitott");
      p.appendChild(el("span", "ajanlo-sin-jel"));
      sin.appendChild(p);
    });
    return sin;
  }

  function valaszokRajzol(q, elonezet) {
    const csoport = el("div", "ajanlo-valaszok");
    q.valaszok.forEach((v) => {
      const cimke = el("label", "ajanlo-valasz");
      const be = document.createElement("input");
      be.type = "radio";
      be.name = "ajanlo-" + q.id;
      be.value = v.id;
      be.checked = allapot.valaszok[q.id] === v.id;
      if (elonezet) be.disabled = true;
      be.addEventListener("change", () => {
        allapot.valaszok[q.id] = v.id;
        rajzol();
      });
      cimke.appendChild(be);
      /* A kiválasztást nem csak a szín jelzi: a korongba pipa kerül. */
      const jel = el("span", "ajanlo-valasz-pipa");
      jel.setAttribute("aria-hidden", "true");
      cimke.appendChild(jel);
      cimke.appendChild(el("span", "type-ui-body", v.cimke));
      csoport.appendChild(cimke);
    });
    return csoport;
  }

  function kerdesRajzol(q, elonezet) {
    const doboz = el("fieldset", "ajanlo-kerdes");
    if (elonezet) { doboz.disabled = true; doboz.dataset.elonezet = "igen"; }
    const cim = el("legend", "type-ui-body-strong ajanlo-kerdes-cim", q.kerdes);
    doboz.appendChild(cim);
    if (q.sugo) doboz.appendChild(el("p", "type-ui-caption ajanlo-kerdes-sugo", q.sugo));
    doboz.appendChild(valaszokRajzol(q, elonezet));
    return doboz;
  }

  function uzenetRajzol(szoveg) {
    const b = el("div", "ajanlo-uzenet");
    b.appendChild(el("p", "type-ui-body ajanlo-uzenet-szoveg", szoveg));
    b.appendChild(el("p", "type-ui-caption ajanlo-uzenet-ido", ido()));
    return b;
  }

  function magyarazatRajzol(szoveg) {
    const m = el("div", "ajanlo-magyarazat");
    m.appendChild(svg("szikra", "ajanlo-magyarazat-jel"));
    m.appendChild(el("p", "type-ui-subtitle", szoveg));
    return m;
  }

  function lepesUzenete(lepes) {
    const elso = elsoSzakasz();
    if (lepes.uzenetVegyes && elso && elso.irany === "egyeztetes") return lepes.uzenetVegyes;
    if (!lepes.uzenet) return "";
    const nev = elso && K.termekek[elso.irany] ? "az " + K.termekek[elso.irany].nev : "a javasolt megoldás";
    return lepes.uzenet.replace("{irany}", nev);
  }

  function folyamRajzol() {
    const folyam = el("div", "ajanlo-folyam");
    const q = K.kerdesek[allapot.aktiv];
    const lepes = K.lepesek[lepesIndex(q.lepes)];

    /* Az asszisztens üzenete csak a szakasz ELSŐ kérdésénél jelenik meg. */
    const elsoAdottLepesben = kerdesekLepesben(q.lepes)[0].id === q.id;
    if (elsoAdottLepesben) folyam.appendChild(uzenetRajzol(lepesUzenete(lepes)));

    folyam.appendChild(kerdesRajzol(q, false));

    const valasz = allapot.valaszok[q.id];
    if (valasz && q.magyarazat && q.magyarazat[valasz]) {
      folyam.appendChild(magyarazatRajzol(q.magyarazat[valasz]));
    }

    /* A KÖVETKEZŐ kérdés halványan, letiltva — a látogató látja, mi jön, de
       nem tud előre ugrani. */
    const kov = K.kerdesek[allapot.aktiv + 1];
    if (valasz && kov) folyam.appendChild(kerdesRajzol(kov, true));

    return folyam;
  }

  function labRajzol() {
    const lab = el("div", "ajanlo-lab");

    const vissza = el("button", "btn btn-halvany ajanlo-vissza");
    vissza.type = "button";
    vissza.appendChild(el("span", "ajanlo-nyil-elol", "←"));
    vissza.appendChild(document.createTextNode("Vissza"));
    vissza.disabled = allapot.aktiv === 0 && !allapot.kesz;
    vissza.addEventListener("click", () => {
      if (allapot.kesz) { allapot.kesz = false; }
      else if (allapot.aktiv > 0) { allapot.aktiv -= 1; }
      rajzol();
    });

    /* A záró képernyőn nincs „előre": a továbblépés ott a kimenet saját
       gombjaira tartozik (ársávbecslő, mentés), nem a kérdéssor lábára. */
    if (allapot.kesz) {
      lab.appendChild(vissza);
      return lab;
    }

    const tovabb = el("button", "btn btn-primary ajanlo-tovabb");
    tovabb.type = "button";
    const utolso = allapot.aktiv === kerdesSzam - 1;
    tovabb.appendChild(document.createTextNode(utolso ? "Eredmény" : "Tovább"));
    tovabb.appendChild(el("span", "ajanlo-nyil", "→"));
    tovabb.disabled = !allapot.valaszok[K.kerdesek[allapot.aktiv].id];
    tovabb.addEventListener("click", () => {
      if (utolso) allapot.kesz = true;
      else allapot.aktiv += 1;
      rajzol();
    });

    lab.appendChild(vissza);
    lab.appendChild(tovabb);
    return lab;
  }

  /* ---------------------------------------------------- KIMENET (záró kép) */
  function eredmenyRajzol() {
    const k = kep();
    const irany = k.masodik.irany || (k.elso && k.elso.irany) || "egyeztetes";
    const termek = K.termekek[irany];
    const doboz = el("div", "ajanlo-eredmeny");

    doboz.appendChild(uzenetRajzol(K.lepesek[K.lepesek.length - 1].uzenet));

    /* 1 · A javasolt megoldás */
    const blokk1 = el("section", "ajanlo-blokk");
    blokk1.appendChild(el("h4", "type-ui-card-title ajanlo-blokk-cim",
      irany === "egyeztetes" ? "Vegyes a kép" : "A javasolt megoldás"));
    const fejlec = el("div", "ajanlo-termek");
    /* Terméknévhez csepp, egyeztetéshez info: a jelvény ne ígérjen terméket
       ott, ahol a modul szándékosan nem nevez meg egyet sem. */
    fejlec.appendChild(svg(irany === "egyeztetes" ? "info" : "csepp", "ajanlo-termek-jel"));
    const szov = el("div");
    szov.appendChild(el("p", "type-ui-body-strong ajanlo-termek-nev", termek.nev));
    szov.appendChild(el("p", "type-ui-subtitle ajanlo-termek-szoveg", termek.indoklas));
    fejlec.appendChild(szov);
    blokk1.appendChild(fejlec);

    /* Epurecónál a kompromisszum kimondása kötelező (spec 6.). */
    if (termek.kompromisszum) {
      blokk1.appendChild(el("p", "type-ui-subtitle ajanlo-kompromisszum", termek.kompromisszum));
    }

    /* Határesetnél és ellentmondásnál: MI MIATT nem lehetett dönteni. */
    const okok = [];
    if (k.elso && k.elso.ok) okok.push(k.elso.ok);
    if (k.masodik.ellentmondas) okok.push(k.masodik.ellentmondas);
    if (okok.length) {
      const ul = el("ul", "ajanlo-okok");
      okok.forEach((o) => ul.appendChild(el("li", "type-ui-subtitle", o)));
      blokk1.appendChild(el("p", "type-ui-subtitle ajanlo-okok-cim",
        "Amit a válaszaiból nem lehetett automatikusan eldönteni:"));
      blokk1.appendChild(ul);
    }
    doboz.appendChild(blokk1);

    /* 2 · Kivitelezési feltételek */
    if (k.masodik.feltetelek.length) {
      const blokk2 = el("section", "ajanlo-blokk");
      blokk2.appendChild(el("h4", "type-ui-card-title ajanlo-blokk-cim", "Kivitelezési feltételek"));
      const lista = el("ul", "ajanlo-feltetel-lista");
      k.masodik.feltetelek.forEach((id) => {
        const f = K.feltetelek[id]; if (!f) return;
        const li = el("li", "ajanlo-feltetel");
        li.appendChild(svg(f.jel, "ajanlo-feltetel-jel"));
        const t = el("div");
        t.appendChild(el("p", "type-ui-body-strong", f.cimke));
        t.appendChild(el("p", "type-ui-subtitle ajanlo-feltetel-szoveg", f.leiras));
        li.appendChild(t);
        lista.appendChild(li);
      });
      blokk2.appendChild(lista);
      doboz.appendChild(blokk2);
    }

    /* 3 · Tisztázandók — minden elem mellett, hogyan tisztázható (spec 6.). */
    const blokk3 = el("section", "ajanlo-blokk");
    blokk3.appendChild(el("h4", "type-ui-card-title ajanlo-blokk-cim", "Tisztázandók"));
    const dl = el("dl", "ajanlo-tisztazando-lista");
    k.masodik.tisztazandok.forEach((id) => {
      const t = K.tisztazandok[id]; if (!t) return;
      const sor = el("div", "ajanlo-tisztazando");
      sor.appendChild(el("dt", "type-ui-body-strong", t.cimke));
      sor.appendChild(el("dd", "type-ui-subtitle", t.hogyan));
      dl.appendChild(sor);
    });
    blokk3.appendChild(dl);
    doboz.appendChild(blokk3);

    /* Továbblépés — kontaktadat NÉLKÜL (spec 7.). */
    const cta = el("div", "ajanlo-cta");
    const fo = el("a", "btn btn-primary", K.tovabb.elsodleges.cimke);
    fo.href = K.tovabb.elsodleges.url;
    cta.appendChild(fo);
    /* A mentés MAGYARÁZATA a gomb elé kerül, nem utána: a látogatónak a
       kattintás ELŐTT kell tudnia, mit kap és mit nem kérünk cserébe. */
    if (K.mentes.bevezeto) {
      const bev = el("p", "type-ui-subtitle ajanlo-mentes-bevezeto", K.mentes.bevezeto);
      /* Öko itt is megszólal, amikor a látogató idegörget — lásd kalauz.js PONTOK. */
      bev.dataset.okoPont = "mentes";
      cta.appendChild(bev);
    }
    const ment = el("button", "btn btn-halvany", "Eredmény mentése");
    ment.type = "button";
    ment.addEventListener("click", () => mentes(ment, cta));
    cta.appendChild(ment);
    const linkek = el("ul", "ajanlo-linkek");
    K.tovabb.masodlagos.forEach((l) => {
      const li = el("li");
      const a = el("a", "text-link");
      a.href = l.url;
      const burok = el("span", "link-label", l.cimke);
      burok.appendChild(el("span", "action-arrow-end", "→")).setAttribute("aria-hidden", "true");
      a.appendChild(burok);
      li.appendChild(a);
      linkek.appendChild(li);
    });
    cta.appendChild(linkek);
    doboz.appendChild(cta);

    return doboz;
  }

  /* ==========================================================================
     MENTÉS — azonosítóval, visszakereshetően
     --------------------------------------------------------------------------
     A fejléc azt ígéri, hogy az eredmény elmenthető. Ez KÉT úton valósul meg,
     és a kettő nem egyenrangú:

       1. SZERVERRE, azonosítóval (`api/ajanlo-mentes`). A látogató kap egy
          `MA-XXXX-XXXX` kódot és egy címet (`/eredmeny?id=…`). Onnan a lap
          kinyomtatható vagy PDF-be menthető — és a PDF-en ott a kód és a cím
          is, tehát telefonban bemondható, kollégának továbbadható.
       2. HELYBEN, szövegfájlként. Ez a TARTALÉK: ha a végpont nem elérhető
          (nincs `config.php`, ki van kapcsolva, hálózati hiba), a modul nem
          hallgat el semmit — letölti a szöveges összefoglalót, és kimondja,
          hogy szerverre most nem került, tehát azonosító sincs.

     E-mail-címet egyik úton sem kérünk (spec 7.), és a rekordban sincs
     személyes adat: a válaszok és a belőlük számított kimenet megy el. */

  /** A mentendő csomag — pontosan az, amit a látogató a képernyőn lát. */
  function mentendo() {
    const k = kep();
    const irany = k.masodik.irany || (k.elso && k.elso.irany) || "egyeztetes";
    const t = K.termekek[irany] || {};
    const okok = [];
    if (k.elso && k.elso.ok) okok.push({ cimke: k.elso.ok });
    if (k.masodik.ellentmondas) okok.push({ cimke: k.masodik.ellentmondas });

    return {
      verzio: K.verzio || "",
      /* GÉPI VÁLASZKULCSOK a modulok közti átadáshoz: ebből tölti elő a 8.
         szekció azt, amit itt már megkérdeztünk. A `valaszok` mező ugyanez
         emberi olvasatban — a kettő szándékosan külön él, mert az egyiket gép
         használja, a másikat ember olvassa. */
      valaszKulcsok: Object.assign({}, allapot.valaszok),
      valaszok: K.kerdesek.reduce((ki, q) => {
        const v = allapot.valaszok[q.id];
        if (v) {
          const o = q.valaszok.find((x) => x.id === v);
          ki.push({ cimke: q.kerdes, szoveg: (o && o.cimke) || v });
        }
        return ki;
      }, []),
      eredmeny: {
        irany: irany,
        cim: irany === "egyeztetes" ? "Vegyes a kép" : "A javasolt megoldás",
        termekNev: t.nev || "",
        indoklas: t.indoklas || "",
        kompromisszum: t.kompromisszum || "",
        okok: okok,
        feltetelek: k.masodik.feltetelek.map((id) => {
          const f = K.feltetelek[id] || {};
          return { cimke: f.cimke || id, szoveg: f.leiras || "" };
        }),
        tisztazandok: k.masodik.tisztazandok.map((id) => {
          const x = K.tisztazandok[id] || {};
          return { cimke: x.cimke || id, szoveg: x.hogyan || "" };
        })
      }
    };
  }

  function osszefoglalo(azonosito) {
    const k = kep();
    const irany = k.masodik.irany || (k.elso && k.elso.irany) || "egyeztetes";
    const t = K.termekek[irany];
    const sorok = [];
    sorok.push("ÖkoTech Home — megoldás-ajánló, előzetes eredmény");
    sorok.push("Készült: " + new Date().toLocaleString("hu-HU"));
    if (azonosito) {
      sorok.push("Azonosító: " + azonosito);
      sorok.push("Visszakereshető: " + window.OthUgy.eredmenyUrl(azonosito));
    }
    sorok.push("");
    sorok.push("A VÁLASZAI");
    K.kerdesek.forEach((q) => {
      const v = allapot.valaszok[q.id];
      if (!v) return;
      const cimke = (q.valaszok.find((o) => o.id === v) || {}).cimke || v;
      sorok.push("- " + q.kerdes + " " + cimke);
    });
    sorok.push("");
    sorok.push(irany === "egyeztetes" ? "VEGYES A KÉP" : "A JAVASOLT MEGOLDÁS");
    sorok.push(t.nev);
    sorok.push(t.indoklas);
    if (t.kompromisszum) { sorok.push(""); sorok.push(t.kompromisszum); }
    if (k.elso && k.elso.ok) { sorok.push(""); sorok.push("Nem volt automatikusan eldönthető: " + k.elso.ok); }
    if (k.masodik.ellentmondas) { sorok.push(""); sorok.push(k.masodik.ellentmondas); }
    if (k.masodik.feltetelek.length) {
      sorok.push(""); sorok.push("KIVITELEZÉSI FELTÉTELEK");
      k.masodik.feltetelek.forEach((id) => {
        const f = K.feltetelek[id]; if (f) sorok.push("- " + f.cimke + ": " + f.leiras);
      });
    }
    sorok.push(""); sorok.push("TISZTÁZANDÓK");
    k.masodik.tisztazandok.forEach((id) => {
      const x = K.tisztazandok[id]; if (x) sorok.push("- " + x.cimke + ": " + x.hogyan);
    });
    sorok.push("");
    sorok.push("Az eredmény tájékoztató jellegű. A végleges megoldást helyszíni felmérés után határozzuk meg.");
    return sorok.join("\n");
  }

  function szovegLetolt(azonosito) {
    const blob = new Blob([osszefoglalo(azonosito)], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "okotechhome-megoldas-ajanlo" + (azonosito ? "-" + azonosito : "") + ".txt";
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  /** A mentés eredménye a CTA fölött jelenik meg, a gomb helyett. */
  function mentesDoboz(sikeres, adat, hibaSzoveg) {
    const d = el("div", "ajanlo-mentve");
    d.dataset.allapot = sikeres ? "kesz" : "tartalek";
    d.setAttribute("role", "status");
    d.appendChild(svg(sikeres ? "pipa" : "figyelem", "ajanlo-mentve-jel"));

    const sz = el("div", "ajanlo-mentve-szoveg");
    if (sikeres) {
      sz.appendChild(el("p", "type-ui-body-strong", "Elmentettük. Az eredmény azonosítója:"));
      sz.appendChild(el("p", "ajanlo-mentve-azonosito type-data-value", adat.azonosito));
      if (K.mentes.azonositoMagyarazat) {
        sz.appendChild(el("p", "type-ui-caption ajanlo-mentve-mi-ez", K.mentes.azonositoMagyarazat));
      }
      const cim = window.OthUgy.eredmenyUrl(adat.azonosito);
      const a = el("a", "text-link ajanlo-mentve-link");
      a.href = window.OthUgy.eredmenyHref(adat.azonosito);
      const b = el("span", "link-label", "Megnyitás, nyomtatás és PDF-be mentés");
      b.appendChild(el("span", "action-arrow-end", "→")).setAttribute("aria-hidden", "true");
      a.appendChild(b);
      sz.appendChild(a);
      /* A teljes cím LÁTHATÓ szövegként is: a kinyomtatott lapon a kattintható
         hivatkozás semmit nem ér, a beírható cím viszont igen. */
      sz.appendChild(el("p", "type-ui-caption ajanlo-mentve-cim", cim));
      sz.appendChild(el("p", "type-ui-caption ajanlo-mentve-megjegyzes",
        (K.mentes.megorzesSzoveg || "")
        + " Az azonosítót telefonon is bemondhatja. A lap alatti ársávbecslő innentől "
        + "tudja, mit adott már meg — azokat a kérdéseket nem teszi fel újra, és az "
        + "eredményét ugyanehhez az azonosítóhoz csatolja."));
    } else {
      sz.appendChild(el("p", "type-ui-body-strong", "Szerverre most nem sikerült elmenteni"));
      sz.appendChild(el("p", "type-ui-subtitle", (hibaSzoveg ? hibaSzoveg + " " : "")
        + "Az eredményt szövegfájlként letöltöttük a gépére, tehát nem veszett el — "
        + "azonosító viszont ehhez nem tartozik, és visszakeresni sem tudjuk."));
    }
    d.appendChild(sz);
    return d;
  }

  async function mentes(gomb, cta) {
    if (!window.OthUgy) { szovegLetolt(""); return; }
    gomb.disabled = true;
    gomb.setAttribute("aria-busy", "true");
    const valasz = await window.OthUgy.ment("ajanlo", mentendo());
    gomb.disabled = false;
    gomb.removeAttribute("aria-busy");

    if (valasz.ok) {
      gomb.replaceWith(mentesDoboz(true, valasz));
    } else {
      szovegLetolt("");
      cta.insertBefore(mentesDoboz(false, null, valasz.uzenet), gomb);
    }
  }

  function asszisztensRajzol() {
    const kartya = el("div", "ajanlo-asszisztens");
    const aktivLepes = lepesIndex(K.kerdesek[allapot.aktiv].lepes);
    /* A záró képernyőn MINDEN szakasz kész — a sín ilyenkor nem jelöl aktívat,
       különben ellentmondana a panelnek, ami már „Kész”-t ír a 6. szakaszra. */
    kartya.appendChild(sinRajzol(allapot.kesz ? K.lepesek.length : aktivLepes));

    const tartalom = el("div", "ajanlo-tartalom");

    const fej = el("div", "ajanlo-fej");
    const cimek = el("div");
    cimek.appendChild(el("p", "type-ui-card-title ajanlo-fej-cim", "ÖkoTechHome AI Asszisztens"));
    cimek.appendChild(el("p", "type-ui-subtitle ajanlo-fej-alcim",
      "Megoldás-ajánló · " + kerdesSzam + " rövid kérdés"));
    fej.appendChild(cimek);
    const szamlalo = el("p", "ajanlo-szamlalo");
    szamlalo.appendChild(el("span", "ajanlo-szamlalo-most",
      String(allapot.kesz ? K.lepesek.length : aktivLepes + 1)));
    szamlalo.appendChild(el("span", "ajanlo-szamlalo-ossz", " / " + K.lepesek.length));
    fej.appendChild(szamlalo);
    tartalom.appendChild(fej);

    /* A gépi válaszkulcsokat a munkamenetbe akkor is eltesszük, ha a látogató
       nem ment: a 8. szekció így is át tudja venni, amit itt megadott. Az
       azonosító csak mentéskor keletkezik — átvételhez nem kell. */
    if (allapot.kesz && window.OthUgy) {
      window.OthUgy.jegyez("ajanlo", Object.assign({}, allapot.valaszok), "");
      /* A teljes kimenet is a munkamenetbe kerül — de NEM megy sehova. Ha a
         látogató itt nem ment, de az ársávbecslőnél igen, ez a blokk ugyanabba
         az ügybe kerül fel: így nem lesz féloldalas a rekord. */
      window.OthUgy.fuggoben("ajanlo", mentendo());
    }
    tartalom.appendChild(allapot.kesz ? eredmenyRajzol() : folyamRajzol());
    tartalom.appendChild(labRajzol());

    kartya.appendChild(tartalom);
    return kartya;
  }

  /* ==========================================================================
     JOBB OLDAL — AZ ÁLLAPOTPANEL
     ========================================================================== */

  function lepesAllapot(l, i, aktivLepes) {
    if (l.zaro) return allapot.kesz ? "kesz" : (aktivLepes === i ? "aktiv" : "nyitott");
    const qs = kerdesekLepesben(l.id);
    const megvan = qs.length > 0 && qs.every((q) => allapot.valaszok[q.id]);
    if (megvan && i < aktivLepes) return "kesz";
    if (i === aktivLepes) return "aktiv";
    return megvan ? "kesz" : "nyitott";
  }

  const ALLAPOT_SZO = { kesz: "Kész", aktiv: "Folyamatban", nyitott: "Még nyitott" };
  const ALLAPOT_JEL = { kesz: "pipa", aktiv: "folyamat", nyitott: "kor" };

  function panelRajzol() {
    const panel = el("aside", "ajanlo-panel");
    panel.setAttribute("aria-labelledby", "ajanlo-panel-cim");
    panel.setAttribute("aria-live", "polite");

    const aktivLepes = allapot.kesz
      ? K.lepesek.length - 1
      : lepesIndex(K.kerdesek[allapot.aktiv].lepes);

    const pirula = el("p", "ajanlo-allapot");
    pirula.appendChild(svg("info", "ajanlo-allapot-jel"));
    pirula.appendChild(el("span", "type-ui-label",
      allapot.kesz ? "Jelenlegi állapot · kész" : "Jelenlegi állapot · folyamatban"));
    panel.appendChild(pirula);

    panel.appendChild(el("h3", "type-display-highlight-title ajanlo-panel-cim", "Az Ön helyzetképe"))
      .id = "ajanlo-panel-cim";
    const megvalaszolt = K.kerdesek.filter((q) => allapot.valaszok[q.id]).length;
    panel.appendChild(el("p", "type-ui-subtitle ajanlo-panel-alcim",
      megvalaszolt + " / " + kerdesSzam + " válasz megadva"));

    /* A hat szakasz állapota */
    const lista = el("ol", "ajanlo-lepeslista");
    K.lepesek.forEach((l, i) => {
      const a = lepesAllapot(l, i, aktivLepes);
      const li = el("li", "ajanlo-lepessor");
      li.dataset.allapot = a;
      li.appendChild(el("span", "ajanlo-lepesszam type-data-value",
        String(i + 1).padStart(2, "0")));
      li.appendChild(el("span", "type-ui-body ajanlo-lepescim", l.cim));
      const jelzo = el("span", "ajanlo-lepesjelzo");
      jelzo.appendChild(el("span", "type-ui-subtitle", ALLAPOT_SZO[a]));
      jelzo.appendChild(svg(ALLAPOT_JEL[a], "ajanlo-lepesjel"));
      li.appendChild(jelzo);
      lista.appendChild(li);
    });
    panel.appendChild(lista);

    const k = kep();

    /* Jelenlegi irány */
    panel.appendChild(el("p", "type-ui-label ajanlo-panel-felirat", "Jelenlegi irány"));
    const iranyId = k.masodik.irany || (k.elso && k.elso.irany);
    const iranyDoboz = el("div", "ajanlo-irany");
    if (iranyId) {
      const t = K.termekek[iranyId];
      iranyDoboz.appendChild(svg(iranyId === "egyeztetes" ? "info" : "csepp", "ajanlo-irany-jel"));
      const sz = el("div");
      sz.appendChild(el("p", "type-ui-body-strong ajanlo-irany-nev", t.nev));
      sz.appendChild(el("p", "type-ui-subtitle ajanlo-irany-szoveg",
        k.masodik.ellentmondas || t.rovid));
      iranyDoboz.appendChild(sz);
    } else {
      iranyDoboz.appendChild(svg("info", "ajanlo-irany-jel"));
      iranyDoboz.appendChild(el("p", "type-ui-subtitle ajanlo-irany-szoveg",
        "A használati szakasz három kérdése után jelenik meg az irány."));
    }
    panel.appendChild(iranyDoboz);

    /* Kivitelezési feltételek — chipként, ahogy már látszanak */
    if (k.masodik.feltetelek.length) {
      panel.appendChild(el("p", "type-ui-label ajanlo-panel-felirat",
        "Kivitelezési feltételek, amelyek már látszanak"));
      const chipek = el("ul", "ajanlo-chipek");
      k.masodik.feltetelek.forEach((id) => {
        const f = K.feltetelek[id]; if (!f) return;
        const li = el("li", "ajanlo-chip");
        li.appendChild(svg(f.jel, "ajanlo-chip-jel"));
        li.appendChild(el("span", "type-ui-subtitle", f.cimke));
        chipek.appendChild(li);
      });
      panel.appendChild(chipek);
    }

    /* Tisztázandók */
    if (k.masodik.tisztazandok.length) {
      panel.appendChild(el("p", "type-ui-label ajanlo-panel-felirat", "Tisztázandók"));
      const ul = el("ul", "ajanlo-tisztazando-rovid");
      k.masodik.tisztazandok.forEach((id) => {
        const t = K.tisztazandok[id]; if (!t) return;
        ul.appendChild(el("li", "type-ui-subtitle", t.cimke));
      });
      panel.appendChild(ul);
    }

    /* A záró figyelmeztetés csak amíg tart a folyamat: a kimenet után már nem
       „nem végleges”, hanem kész — ott a tisztázandók listája a helyén beszél. */
    if (!allapot.kesz) {
      const fig = el("p", "ajanlo-figyelem");
      fig.appendChild(svg("figyelem", "ajanlo-figyelem-jel"));
      const sz = el("span", "type-ui-subtitle");
      sz.appendChild(el("strong", null, "Fontos:"));
      sz.appendChild(document.createTextNode(
        " az ajánlás ebben a szakaszban még nem végleges, a telek adottságai módosíthatják a kimenetet."));
      fig.appendChild(sz);
      panel.appendChild(fig);
    }

    return panel;
  }

  /* ==========================================================================
     KIRAJZOLÁS
     ========================================================================== */
  function rajzol() {
    const test = el("div", "ajanlo-body");
    test.appendChild(asszisztensRajzol());
    test.appendChild(panelRajzol());
    gyoker.replaceChildren(test);
  }

  rajzol();
})();
