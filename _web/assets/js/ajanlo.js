/* ============================================================================
   ÖkoTech-Home — AI megoldás-ajánló (6. szekció)
   ----------------------------------------------------------------------------
   Forrás: `OkoTech-Home_AI-modul_fejlesztoi_specifikacio.2.docx` (2026-08-24).
   ÁTDOLGOZVA: `okotech-megoldas-ajanlo-hibalista-es-javaslatok.docx`
   (eSystem Integration Kft., 2026-09-11) — a modul végigtesztelése alapján.

   TERVEZÉSI ELVEK — ezek a specifikációból következnek, nem stílusdöntések:

   1. SZAKMAI ÁLLÍTÁS NINCS A KÓDBAN. Kérdés, válasz, magyarázat, döntési
      szabály, terméknév és kimeneti szöveg mind az `assets/data/ajanlo-konfig.js`
      fájlban él, amit a cég fejlesztő nélkül szerkeszthet. Ez a fájl csak
      kiértékel és kirajzol.

   2. KÉT SZINT, VÉGIG SZÉTVÁLASZTVA (spec 2.):
        · a TECHNOLÓGIÁT a használat jellege és a terhelés dönti el,
        · a MEGVALÓSÍTÁS FELTÉTELEIT a telek adottságai és a vízelhelyezés.
      A telek adottságai tehát nem választanak új technológiát — egyetlen
      kivétellel: a szabad terület a vízelhelyezést kérdésessé teheti.

   3. A MODUL MEGNEVEZI A TERMÉKET, ahol a helyzet egyértelmű, és KIMONDJA a
      bizonytalanságot ott, ahol az fennáll. Határesetnél nem termékajánlás a
      kimenet, hanem az, hogy vegyes a kép — felsorolva, mi miatt.

   4. ADATOT NEM KÉRÜNK ÉS NEM KÜLDÜNK. A modul regisztráció és e-mail-cím
      nélkül indul, a válaszok a lapon maradnak. A záró képernyőn sincs
      kontaktadat-bekérés (spec 7.).

   ══ MI VÁLTOZOTT A HIBALISTA UTÁN ══════════════════════════════════════════

   A talált hibák többsége EGYETLEN közös gyökérre vezethető vissza: a záró
   képernyő SABLONKÉNT futott, nem elágazásként. Ugyanazt a három dolgot tette
   minden kimenetnél — terméknevet mutatott, kivitelezési feltételeket sorolt,
   és átküldött az ársávbecslőre —, függetlenül attól, hogy a modul eljutott-e
   egyáltalán javaslatig. Ebből következett H1, H2, H3 és H5.

   Innentől a `K.kimenetek` alatti TÍPUS szabja meg a fejlécet, a megjelenő
   blokkokat és a következő lépést. A `kimenet()` egyetlen helyen dönti el,
   melyik típusról van szó; minden rajzoló ebből dolgozik.

     H1 · Az egyeztetés-státuszt NEM írja felül a terület-szabály. Egy
          ellentmondást nem lehet egy további szűkítő feltétellel feloldani —
          a modul ettől nem lesz magabiztosabb, hanem két nyitott kérdése lesz.
     H2 · A zárt tároló nem automatikus ítélet többé. Nem forgalmazzuk, tehát
          a modul nem vezethet rá végkövetkeztetésként (konfig 3.2.).
     H3 · Az ársávbecslő CTA kimenettípus-függő: ahol nincs mit árazni, ott
          nem jelenik meg.
     H4 · A kivitelezési feltételek a VÉGEREDMÉNY típusához vannak kapuzva
          (`feltetelek[].csak`), nem csak a bemenő válaszokhoz.
     H5 · A fejléc kimenettípus-függő — nem állíthatja két sorral a
          „nem lehetett eldönteni" fölött, hogy „a javasolt megoldás".
     H6 · Az irány-kártya nem fagy meg: STÁTUSZ + INDOKLÁS, ami minden válasz
          után lép (`iranyAllapot()`).
     H8 · Az ellentmondás meg van nevezve — melyik két szempont ütközik.
     H11· Az azonosító magától keletkezik az eredmény megjelenésekor.
     H13· A buborékok háromrészesek, más nyitott kérdéssel zárnak — a konfig
          szövegeiben, nem itt.
     H14· A helyzetkép-panel szakaszai kattinthatók, és a visszalépés utáni
          módosítás mindent újraszámol.

   JS NÉLKÜL: a szekció `<noscript>` blokkja írja le, mit kérdezne a modul, és
   felkínálja a személyes utat — a kérdéssor nem épül fel.
   ========================================================================== */
(() => {
  "use strict";


  /* ------------------------------------------------------------- FELÜLET ---
     A modul TARTALMA nyelvenkénti konfigurációs fájlban él (`ajanlo-konfig.js`,
     `ajanlo-konfig-en.js`); ide csak a felület állandó feliratai kerülnek —
     gombok, panelcímek, állapotszövegek. Azért itt, és nem a konfigurációban,
     mert ezeket nem a cég szerkeszti, hanem a modul szerkezetéhez tartoznak.

     A nyelvet a `<html lang>` adja meg. Ismeretlen nyelvnél a magyar marad. */
  const NYELV = (document.documentElement.lang || 'hu').slice(0, 2) === 'en' ? 'en' : 'hu';
  const SZOVEG = {
    hu: {
      feltetelek: "Kivitelezési feltételek",
      tisztazandok: "Tisztázandók",
      allapotSzo: { kesz: "Kész", aktiv: "Folyamatban", nyitott: "Még nyitott" },
      eredmenyGomb: "Eredmény",
      tovabbGomb: "Tovább",
      visszaGomb: "Vissza",
      /* A mentés MÁR MEGTÖRTÉNT, mire ez látszik (H11) — a gomb innentől
         csak megosztásra való. */
      linkMasolas: "Link másolása",
      linkMasolva: "A link a vágólapon",
      linkNemSikerult: "A másolás nem ment — a fenti cím kijelölhető",
      elmentve: "Elmentettük. Az eredmény azonosítója:",
      megnyitas: "Megnyitás, nyomtatás és PDF-be mentés",
      mentes: "Eredmény mentése",
      nemSikerult: "Szerverre most nem sikerült elmenteni",
      asszisztens: "ÖkoTechHome AI Asszisztens",
      ajanloCim: "Megoldás-ajánló · ",
      rovidKerdes: " rövid kérdés",
      allapotKesz: "Jelenlegi állapot · kész",
      allapotFolyamatban: "Jelenlegi állapot · folyamatban",
      helyzetkep: "Az Ön helyzetképe",
      valaszMegadva: " válasz megadva",
      jelenlegiIrany: "Jelenlegi irány",
      iranyKesobb: "A használati szakasz kérdései után jelenik meg az irány.",
      feltetelekLatszanak: "Kivitelezési feltételek, amelyek már látszanak",
      /* A 4.2. FELHALMOZÓDÓ LISTA címe. A magyarázatok a bal oldalon
         buborékban jelennek meg, és elgörögnek; a jobb oldali panel pont
         arra való, hogy megmaradjanak. */
      eldoltCim: "Ami eddig eldőlt",
      /* A tisztázandók három mezője közül a másik kettő felirata. */
      tisztazandoKi: "Ki tudja megmondani:",
      tisztazandoIdo: "Mennyi idő:",
      lepesreUgras: "Ugrás ehhez a szakaszhoz: ",
      nemVegleges: " az ajánlás ebben a szakaszban még nem végleges, a telek adottságai módosíthatják a kimenetet.",
      egyKerdes: "Egy kérdés",
      ketKerdes: "Két kérdés"
    },
    en: {
      feltetelek: "Conditions for the build",
      tisztazandok: "Points to clarify",
      allapotSzo: { kesz: "Done", aktiv: "In progress", nyitott: "Still open" },
      eredmenyGomb: "Result",
      tovabbGomb: "Next",
      visszaGomb: "Back",
      linkMasolas: "Copy the link",
      linkMasolva: "Link copied",
      linkNemSikerult: "Copying failed — the address above can be selected",
      elmentve: "Saved. The result's reference:",
      megnyitas: "Open, print or save as PDF",
      mentes: "Save the result",
      nemSikerult: "Could not be saved to the server just now",
      asszisztens: "ÖkoTechHome AI Assistant",
      ajanloCim: "Solution finder · ",
      rovidKerdes: " short questions",
      allapotKesz: "Current state · complete",
      allapotFolyamatban: "Current state · in progress",
      helyzetkep: "Your situation so far",
      valaszMegadva: " answers given",
      jelenlegiIrany: "Current direction",
      iranyKesobb: "The direction appears after the questions on use.",
      feltetelekLatszanak: "Conditions for the build that are already apparent",
      eldoltCim: "What has been settled",
      tisztazandoKi: "Who can tell:",
      tisztazandoIdo: "How long:",
      lepesreUgras: "Jump to this stage: ",
      nemVegleges: " the recommendation is not final at this stage; the plot's conditions may still change the outcome.",
      egyKerdes: "One question",
      ketKerdes: "Two questions"
    }
  }[NYELV];

  const K = window.OTH_AJANLO;
  const gyoker = document.getElementById("ajanlo-root");
  if (!K || !gyoker) return;

  /* ------------------------------------------------------------- ÁLLAPOT */
  const allapot = {
    valaszok: {},      /* kérdésazonosító → válaszazonosító */
    aktiv: 0,          /* az AKTUÁLIS kérdés indexe a K.kerdesek tömbben */
    kesz: false,       /* igaz, ha a kimenet látszik */
    /* A LEGTÁVOLABBI PONT, ameddig a látogató eljutott. Ebből tudjuk, melyik
       szakaszra lehet visszaugrani a panelről (H14), és azt is, hogy egy
       módosítás után vissza kell-e vinni az eredményhez. */
    legtavolabb: 0,
    vegigert: false
  };

  const kerdesSzam = K.kerdesek.length;
  /* A HASZNÁLATI SZAKASZ kérdései — ezek döntik el a technológiát. Az
     irány-kártya bizonyossági fokához kell tudni, hány van még hátra. */
  const HASZNALATI = K.kerdesek.filter((q) => ["hasznalat", "letszam", "kihagyas"].indexOf(q.lepes) >= 0);

  /* --------------------------------------------------------- SEGÉDFÜGGVÉNYEK */
  const el = (tag, oszt, szoveg) => {
    const e = document.createElement(tag);
    if (oszt) e.className = oszt;
    if (szoveg != null) e.textContent = szoveg;
    return e;
  };

  /* ------------------------------------------------------------ MÉRÉS ------
     A hibalista 6.1. és 6.6. pontja. A specifikáció szerint a modul „a weboldal
     első interaktív eleme, amivel a látogató találkozik" — közben a főoldal 6.
     szekciójában fut. A két állítás nem fér össze, és amíg nem tudjuk, hányan
     jutnak el idáig, a modul belső konverziójának javítása egy ismeretlen szám
     töredékén dolgozik. Ez az egyetlen pont, ahol a MÉRÉS ELŐZZE MEG a
     fejlesztést.

     A `gtag` csak az éles fán létezik (a `prod-epit.sh` 6. rétege teszi be), és
     ott is csak sütihozzájárulás szerint mér — a `meres.js` Consent Mode v2-vel
     kapuzza. Itt ezért mindent némán elnyelünk: a mérés SOHA nem törheti el a
     modult. */
  function mer(esemeny, adat) {
    if (typeof window.gtag !== "function") return;
    try { window.gtag("event", esemeny, adat || {}); } catch (e) { /* néma */ }
  }

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
    figyelem: '<path d="M12 4 2.8 19.5h18.4Z"/><path d="M12 10v4"/><path d="M12 17h.01"/>',
    /* A „ki tudja megmondani" sorhoz — a tisztázandók napirendté keretezése. */
    kez:      '<path d="M12 21a8 8 0 0 0 8-8v-3.2a1.8 1.8 0 0 0-3.6 0V8a1.8 1.8 0 0 0-3.6 0V4.8a1.8 1.8 0 0 0-3.6 0V13"/><path d="M9.2 13V7.4a1.8 1.8 0 0 0-3.6 0v7.2"/>',
    /* A „link másolása" gombhoz. */
    lanc:     '<path d="M10 13.5a3.5 3.5 0 0 0 5 0l2.5-2.5a3.5 3.5 0 0 0-5-5L11 7.5"/><path d="M14 10.5a3.5 3.5 0 0 0-5 0L6.5 13a3.5 3.5 0 0 0 5 5l1.5-1.5"/>'
  };

  /* A készlet fele VONALAS rajzolat (kontúr), a másik fele KITÖLTÖTT. A kettőt
     nem lehet ugyanazzal a `fill`/`stroke` beállítással megjeleníteni: a vonalas
     rajzolat kitöltve fekete folttá válik. A besorolás itt van, nem a hívás
     helyén — így egy új rajzolat felvételekor egy helyen kell dönteni. */
  const VONALAS = new Set(["ora", "lakat", "borotek", "pipa", "kor", "folyamat",
                           "horgony", "lejtes", "info", "figyelem", "kez", "lanc"]);

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
  const valaszCimke = (kerdesId) => {
    const q = K.kerdesek.find((x) => x.id === kerdesId);
    const v = q && allapot.valaszok[q.id];
    const o = v && q.valaszok.find((x) => x.id === v);
    return o ? o.cimke : "";
  };

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

  /* ══════════════════════════════════════════════════════ A KIMENET ═════════
     EGY HELYEN dől el, milyen típusú a kimenet — ez a hibalista központi
     javaslata (3.1.). Korábban a záró képernyő és a panel külön-külön
     következtetett ugyanabból az adatból, és nem ugyanarra jutottak.

     PRIORITÁSI SORREND, és ez a H1 javítása:

       1. ELLENTMONDÁS (`egyeztetes`) — ez a legerősebb. Ha a használati
          válaszok két irányba húznak, azt egy további szűkítő feltétel
          (mondjuk a szűk terület) NEM oldja fel. A modul ettől nem lesz
          magabiztosabb, hanem két nyitott kérdése lesz.
       2. VÍZELHELYEZÉS KÉRDÉSES (`vizelhelyezes`) — a terület a kezelt víz
          elhelyezését teszi kérdésessé. NEM ítélet, és NEM zárt tároló (H2):
          a felmérés dönt.
       3. KONKRÉT TERMÉK (`termek`).

     A `tipus` `null`, amíg egyetlen szabály sem illeszkedik — ilyenkor még
     nincs irány, a panel ezt írja ki. */
  function kimenet() {
    const elso = elsoSzakasz();
    const feltetelek = [], tisztazandok = [], utkozesek = [];
    const hozzaad = (t, id) => { if (t.indexOf(id) < 0) t.push(id); };

    for (const h of K.telekHatasok) {
      const kulcs = Object.keys(h.ha)[0];
      if (allapot.valaszok[kulcs] !== h.ha[kulcs]) continue;
      (h.feltetelek || []).forEach((f) => hozzaad(feltetelek, f));
      (h.tisztazandok || []).forEach((t) => hozzaad(tisztazandok, t));
    }

    let tipus = elso ? (elso.irany === "egyeztetes" ? "egyeztetes" : "termek") : null;
    let irany = elso ? elso.irany : null;
    if (elso && elso.ok) utkozesek.push(elso.ok);

    /* KÉTLÉPCSŐS TERÜLET-KIÉRTÉKELÉS (spec 5.).
       1. lépcső: elég-e a terület az oldómedence szikkasztómezőjéhez?
       2. lépcső: elég-e a biológiai rendszer szivárogtatójához?
       A sorrend fordítva számít: ha a 2. lépcső bukik, az 1. már lényegtelen. */
    const sav = K.teruletSavok[allapot.valaszok.terulet];
    const SZ = K.teruletSzabalyok || {};
    if (sav) {
      if (sav.biologiai === false) {
        hozzaad(tisztazandok, "terulet");
        hozzaad(tisztazandok, "befogado");
        if (tipus === "egyeztetes") {
          /* H1 · AZ ELLENTMONDÁS MARAD. Két külön nyitott kérdés — az
             egyeztetés-státuszt a terület-szabály nem írja felül. */
          if (SZ.ellentmondasEsSzuk) utkozesek.push(SZ.ellentmondasEsSzuk);
        } else {
          /* H2 · NEM ZÁRT TÁROLÓ, hanem „a vízelhelyezés a szűk keresztmetszet".
             Amit nem forgalmazunk, arra a modul nem vezethet ítéletként. */
          tipus = "vizelhelyezes";
          irany = null;
        }
      } else if (sav.oldomedence === false && elso && elso.irany === "epureco") {
        tipus = "egyeztetes";
        irany = "egyeztetes";
        if (SZ.oldomedenceNemFer) utkozesek.push(SZ.oldomedenceNemFer);
      }
    }

    /* H4 · A KIVITELEZÉSI FELTÉTELEK KÉT KAPUN MENNEK ÁT.

       1. `csak`    — a VÉGEREDMÉNY TÍPUSA. Korábban a szabályok csak a bemenő
          válaszokhoz voltak kötve, ezért jelent meg a „kiemelt szivárogtató"
          olyan kimeneten is, ahol egyáltalán nincs szivárogtató.
       2. `igenyel` — a feltételezett TÉNY. Ahol a kezelt víz elhelyezése maga
          a nyitott kérdés, ott a szivárogtatóra épülő feltételt nem állítjuk —
          akkor sem, ha a kimenet egyébként határeset (④ ág). Egy feltétel,
          ami egy még el nem dőlt dolgot feltételez, ugyanaz a hiba, mint a
          zárt tároló ítéletként: olyat állít, ami mögé nem tudunk állni. */
    const vizNyitott = !!(sav && sav.biologiai === false);
    const szurtFeltetelek = feltetelek.filter((id) => {
      const f = K.feltetelek[id];
      if (!f) return false;
      if (f.csak && f.csak.indexOf(tipus) < 0) return false;
      if (f.igenyel === "szivarogtato" && vizNyitott) return false;
      return true;
    });

    /* A kötelező tisztázandók a válaszoktól függetlenül megjelennek (spec 6.). */
    Object.keys(K.tisztazandok).forEach((id) => {
      if (K.tisztazandok[id].mindig) hozzaad(tisztazandok, id);
    });
    /* AMIRE NINCS VÁLASZ, AZ NYITOTT KÉRDÉS. A részleges eredménynél (6.5.) ez
       a lényeg: aki a negyediknél abbahagyja, ne kapjon féloldalas képet —
       lássa, mi az, amit még nem tudunk róla. */
    ["talajviz", "talaj", "terulet"].forEach((id) => {
      if (!allapot.valaszok[id]) hozzaad(tisztazandok, id);
    });

    const hasznalatKesz = HASZNALATI.every((q) => allapot.valaszok[q.id]);
    return {
      tipus: tipus,
      irany: irany,
      utkozesek: utkozesek,
      feltetelek: szurtFeltetelek,
      tisztazandok: tisztazandok,
      hasznalatKesz: hasznalatKesz,
      hasznalatHatra: HASZNALATI.filter((q) => !allapot.valaszok[q.id]).length,
      mindMegvan: K.kerdesek.every((q) => allapot.valaszok[q.id])
    };
  }

  /* ══════════════════════════════ AZ IRÁNY-KÁRTYA ÁLLAPOTA (H6, 4.1.) ═══════
     A kártya alatti szöveg korábban a 2/6-tól a 6/6-ig SZÓ SZERINT AZONOS volt:
     „…de a telek adottságai még pontosíthatják az ajánlást." A végén ez
     pontatlan — a telek adottságai már pontosították.

     Helyette a bizonyosság FOKA van kiírva, és az minden válasz után lép. Ez
     egy specifikációs ellentmondást is rendez (S5): a spec szerint az irány a
     használati szakasz három kérdése után jelenik meg, a valóságban viszont
     már az első válasz után ott a terméknév. Ha őszintén ki van írva, hogy ez
     még csak előzetes, megjelenhet korán. */
  function iranyAllapot(k) {
    const A = K.iranyAllapotok || {};
    if (k.tipus === "vizelhelyezes") return A.vizelhelyezes;
    if (k.tipus === "egyeztetes") {
      return { cimke: (A.ellentmondas || {}).cimke, szoveg: k.utkozesek[0] || "" };
    }
    if (!k.hasznalatKesz) {
      const a = A.elozetes || {};
      const szo = k.hasznalatHatra === 1 ? SZOVEG.egyKerdes : SZOVEG.ketKerdes;
      return { cimke: a.cimke, szoveg: (a.szoveg || "").replace("{hatra}", szo) };
    }
    if (k.feltetelek.length) return A.feltetellel;
    if (k.mindMegvan) return A.megerositve;
    return A.eldolt;
  }

  /* A 4.2. FELHALMOZÓDÓ LISTA. A buborékok elgörögnek; ez megmarad. */
  function levezetesek() {
    const ki = [];
    K.kerdesek.forEach((q) => {
      const v = allapot.valaszok[q.id];
      if (v && q.levezetes && q.levezetes[v]) ki.push(q.levezetes[v]);
    });
    return ki;
  }

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

  /* A VÁLASZ MAGA A LÉPTETÉS — egyválasztós kérdésnél nincs „Tovább" gomb, mint
     az ársávbecslőnél sem. Egy kattintás, egy döntés: a külön megerősítés ott
     üres mozdulat, ahol úgyis csak egy válasz adható.

     A BILLENTYŰZET viszont másképp működik. Rádiócsoportban a nyilak nemcsak
     mozgatják a fókuszt, hanem VÁLASZTANAK is: aki a második lehetőségre akar
     eljutni, az elsőt menet közben kijelöli. Azonnali léptetéssel ott ragadna,
     ahol csak áthaladt. Ezért a nyíllal érkező választás késleltetve lép — a
     következő nyílütés törli a függőben lévő lépést —, a mutatóval érkező
     azonnal. Így egyik használati mód sem szenved a másiktól. */
  let nyilNavigacio = false;
  let fuggoLepes = 0;
  addEventListener("pointerdown", () => { nyilNavigacio = false; }, true);

  function leptet(q, fokuszal) {
    clearTimeout(fuggoLepes);
    const lep = () => {
      /* H14 · VISSZALÉPÉS UTÁNI MÓDOSÍTÁS. Aki már látta az eredményt, majd
         visszament egy korábbi kérdéshez és átírta a válaszát, ne kelljen
         újra végigkattintania a maradékot: ha minden kérdésre van válasz, a
         módosítás azonnal az ÚJRASZÁMOLT eredményhez visz vissza. */
      const mind = K.kerdesek.every((x) => allapot.valaszok[x.id]);
      if (allapot.vegigert && mind) allapot.kesz = true;
      else if (allapot.aktiv === kerdesSzam - 1) allapot.kesz = true;
      else allapot.aktiv += 1;
      rajzol();
      /* A rajzolás CSERÉLI a DOM-ot, tehát a fókusz a törzsre esne vissza. Aki
         billentyűvel érkezett, ott ragadna: vissza kellene tabolnia a most
         megjelent kérdésig. Ezért a nyíllal léptető látogatót a következő
         kérdés első válaszára tesszük. Mutatóval érkezőnél ezt nem tesszük —
         ott a fókuszgyűrű váratlanul jelenne meg. */
      if (fokuszal) {
        const elso = gyoker.querySelector(".ajanlo-kerdes:not([data-elonezet]) input");
        if (elso) elso.focus();
      }
    };
    if (nyilNavigacio) fuggoLepes = setTimeout(lep, 900);
    else lep();
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
      be.addEventListener("keydown", (e) => {
        if (e.key.indexOf("Arrow") === 0) { nyilNavigacio = true; clearTimeout(fuggoLepes); }
      });
      be.addEventListener("change", () => {
        allapot.valaszok[q.id] = v.id;
        /* 6.6. · A „nem tudom" aránya kérdésenként TERMÉKMINŐSÉGI mutató, nem
           forgalmi: ha a szabad területnél magas, akkor nem a látogatóval van
           baj, hanem a kérdéssel. Ez mutatja meg, sikerült-e a m²-sávos
           átfogalmazás (6.7. A/B-jelölt). */
        mer("ajanlo_valasz", { kerdes: q.id, valasz: v.id, nem_tudom: v.nemtudom ? 1 : 0 });
        /* Többválasztósnál a gomb lép — itt csak a kijelölés frissül. */
        if (q.tobbes) { rajzol(); return; }
        /* Nyilazás közben SZÁNDÉKOSAN nem rajzolunk: a csere elvinné a fókuszt
           a csoportból, és a látogató nem tudna továbblépni a válaszok között.
           A kijelölést a böngésző maga mutatja, a stílus a `:checked`-re épül. */
        leptet(q, nyilNavigacio);
      });
      /* Az ismételt kattintás a MÁR kijelölt válaszra nem vált `change`
         eseményt, léptetnie viszont kell: az eredményről visszalépő látogató
         másképp nem tudna újra előre jutni, ha nincs „Tovább" gomb. */
      be.addEventListener("click", () => {
        if (q.tobbes || nyilNavigacio) return;
        if (allapot.valaszok[q.id] === v.id) leptet(q, false);
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

  /* A buborék szövege. A `magyarazatFugg` egy KORÁBBI válasz függvényében ad
     pontosabb szöveget — a kihagyás-kérdésnél a mondat csak akkor igaz, ha
     tudjuk, milyen használat mellett hangzik el (a folyamat legfontosabb
     pillanata, hibalista 5.). Ha nincs ilyen, marad az általános. */
  function magyarazatSzoveg(q, valasz) {
    let sz = q.magyarazat && q.magyarazat[valasz];
    const f = q.magyarazatFugg;
    if (f && f.terkep) {
      const fuggo = allapot.valaszok[f.kulcs];
      const ag = fuggo && f.terkep[fuggo];
      if (ag && ag[valasz]) sz = ag[valasz];
    }
    if (!sz) return "";
    return sz.replace("{letszam}", valaszCimke("letszam").toLowerCase());
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

    const valasz = allapot.valaszok[q.id];

    /* AZ ELŐZŐ VÁLASZ MAGYARÁZATA. Mind a hat kérdéshez tartozik egy — ez a
       modul tartalmi hozadéka, nem díszítés. Amíg „Tovább" gomb volt, a
       magyarázat a válasz alatt jelent meg, és a látogató elolvashatta,
       mielőtt továbblépett. Az automatikus léptetéssel az a képernyő eltűnik,
       ezért a magyarázat ide költözik: a KÖVETKEZŐ kérdés fölé, reakcióként
       arra, amit az imént válaszolt. Csak akkor, ha ez a kérdés még
       megválaszolatlan — visszalépéskor a saját magyarázata áll lentebb, és a
       kettő együtt ismétlés volna. */
    const elozo = allapot.aktiv > 0 ? K.kerdesek[allapot.aktiv - 1] : null;
    const elozoValasz = elozo ? allapot.valaszok[elozo.id] : null;
    if (!valasz && elozo && elozoValasz) {
      const sz = magyarazatSzoveg(elozo, elozoValasz);
      if (sz) folyam.appendChild(magyarazatRajzol(sz));
    }

    /* Az asszisztens üzenete csak a szakasz ELSŐ kérdésénél jelenik meg. */
    const elsoAdottLepesben = kerdesekLepesben(q.lepes)[0].id === q.id;
    if (elsoAdottLepesben) folyam.appendChild(uzenetRajzol(lepesUzenete(lepes)));

    folyam.appendChild(kerdesRajzol(q, false));

    if (valasz) {
      const sz = magyarazatSzoveg(q, valasz);
      if (sz) folyam.appendChild(magyarazatRajzol(sz));
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
    vissza.appendChild(document.createTextNode(SZOVEG.visszaGomb));
    vissza.disabled = allapot.aktiv === 0 && !allapot.kesz;
    vissza.addEventListener("click", () => {
      if (allapot.kesz) { allapot.kesz = false; }
      else if (allapot.aktiv > 0) { allapot.aktiv -= 1; }
      rajzol();
    });

    /* A záró képernyőn nincs „előre": a továbblépés ott a kimenet saját
       gombjaira tartozik, nem a kérdéssor lábára. */
    if (allapot.kesz) {
      lab.appendChild(vissza);
      return lab;
    }

    lab.appendChild(vissza);

    /* RÉSZLEGES EREDMÉNY (hibalista 6.5.). A modul a harmadik kérdés után már
       megmutatja az irányt — onnantól minden pillanatban van értelmezhető
       eredmény. Aki a negyediknél abbahagyja, eddig SEMMIT nem kapott; innentől
       lezárhatja azzal, ami megvan. Amit nem adott meg, az automatikusan a
       tisztázandók közé kerül (lásd `kimenet()`), tehát a kép nem féloldalas,
       hanem őszintén részleges. */
    const k = kimenet();
    const aktiv = K.kerdesek[allapot.aktiv];
    if (K.reszleges && k.hasznalatKesz && !k.mindMegvan && allapot.aktiv >= HASZNALATI.length) {
      const most = el("button", "btn btn-halvany ajanlo-reszleges", K.reszleges.gomb);
      most.type = "button";
      most.addEventListener("click", () => {
        mer("ajanlo_reszleges", { megvalaszolt: K.kerdesek.filter((x) => allapot.valaszok[x.id]).length });
        allapot.kesz = true;
        rajzol();
      });
      lab.appendChild(most);
    }

    /* „TOVÁBB" CSAK TÖBBVÁLASZTÓS KÉRDÉSNÉL. Ahol egyetlen válasz adható, ott a
       válasz maga a döntés, és a megerősítő gomb üres mozdulat — az
       ársávbecslő is így működik. Ahol többet is meg lehet jelölni, ott
       viszont kell: a látogatónak kell jeleznie, hogy készen van. */
    if (!aktiv.tobbes) return lab;

    const tovabb = el("button", "btn btn-primary ajanlo-tovabb");
    tovabb.type = "button";
    const utolso = allapot.aktiv === kerdesSzam - 1;
    tovabb.appendChild(document.createTextNode(utolso ? SZOVEG.eredmenyGomb : SZOVEG.tovabbGomb));
    tovabb.appendChild(el("span", "ajanlo-nyil", "→"));
    tovabb.disabled = !allapot.valaszok[aktiv.id];
    tovabb.addEventListener("click", () => {
      if (utolso) allapot.kesz = true;
      else allapot.aktiv += 1;
      rajzol();
    });
    lab.appendChild(tovabb);
    return lab;
  }

  /* ══════════════════════════════════════ KIMENET — NÉGY KÜLÖN ZÁRÓ KÉP ═════
     A hibalista 3.1. táblázata. Korábban EGYETLEN sablon futott: terméknév,
     kivitelezési feltételek, ársávbecslő — minden kimenetnél ugyanaz, akkor is,
     ha a modul el sem jutott javaslatig.

     Innentől a `K.kimenetek[tipus].blokkok` sorolja fel, MI jelenjen meg, és
     mindegyik blokk külön feltétellel — nem alapértelmezésben. */

  function blokkFej(cim) {
    const b = el("section", "ajanlo-blokk");
    b.appendChild(el("h4", "type-ui-card-title ajanlo-blokk-cim", cim));
    return b;
  }

  /* 1–2 · KONKRÉT TERMÉK. Az Epurecónál a kompromisszum kimondása kötelező
     (spec 6.) — és a hibalista 10. pontja szerint nemcsak itt, hanem már az
     irány-kártyán is, amint az irány megjelenik. */
  function termekBlokk(k, kim) {
    const b = blokkFej(kim.fejlec);
    const termek = K.termekek[k.irany];
    if (!termek) return b;
    const fejlec = el("div", "ajanlo-termek");
    fejlec.appendChild(svg(kim.jel, "ajanlo-termek-jel"));
    const szov = el("div");
    szov.appendChild(el("p", "type-ui-body-strong ajanlo-termek-nev", termek.nev));
    szov.appendChild(el("p", "type-ui-subtitle ajanlo-termek-szoveg", termek.indoklas));
    fejlec.appendChild(szov);
    b.appendChild(fejlec);
    if (termek.kompromisszum) {
      b.appendChild(el("p", "type-ui-subtitle ajanlo-kompromisszum", termek.kompromisszum));
    }
    return b;
  }

  /* 3 · HATÁRESET / ELLENTMONDÁS (H5, H8, 4.3.).
     A régi blokk ÖNELLENTMONDÓ volt: „A javasolt megoldás" fejléc alatt két
     sorral lejjebb az állt, hogy „Amit a válaszaiból nem lehetett automatikusan
     eldönteni". Ugyanaz a blokk egyszerre állította, hogy megvan és hogy nincs
     meg. Most a fejléc kimondja, hogy nem dönthető el — és MEGNEVEZZÜK, melyik
     két szempont ütközik. */
  function utkozesBlokk(k, kim) {
    const b = blokkFej(kim.fejlec);
    const t = K.termekek.egyeztetes || {};

    if (k.utkozesek.length) {
      const ul = el("ul", "ajanlo-okok");
      k.utkozesek.forEach((o) => ul.appendChild(el("li", "type-ui-subtitle", o)));
      b.appendChild(ul);
    }
    if (t.indoklas) b.appendChild(el("p", "type-ui-subtitle ajanlo-termek-szoveg", t.indoklas));

    /* A HATÁRESET-ÁG LEGFONTOSABB MONDATA. Megelőzi azt, hogy a látogató azt
       higgye, ŐERRE válaszolt rosszul, és visszamenjen „javítani". */
    if (t.megnyugtatas) {
      b.appendChild(el("p", "type-ui-subtitle ajanlo-megnyugtatas", t.megnyugtatas));
    }

    /* A TELEK-VÁLASZOK ITT SEM VESZNEK KÁRBA: kivitelezési feltételeket
       szabnak, amik MINDKÉT lehetséges irányra érvényesek. */
    const nyitva = el("div", "ajanlo-nyitva");
    if (t.nyitvaCim) nyitva.appendChild(el("p", "type-ui-body-strong", t.nyitvaCim));
    if (k.feltetelek.length && t.nyitvaFeltetellel) {
      const cimkek = k.feltetelek
        .map((id) => (K.feltetelek[id] || {}).cimke)
        .filter(Boolean).join(", ");
      nyitva.appendChild(el("p", "type-ui-subtitle",
        t.nyitvaFeltetellel + " " + cimkek.toLowerCase() + "."));
    }
    if (t.nyitvaZaro) nyitva.appendChild(el("p", "type-ui-subtitle", t.nyitvaZaro));
    if (nyitva.childElementCount) b.appendChild(nyitva);
    return b;
  }

  /* 4 · VÍZELHELYEZÉS KÉRDÉSES (H2, 3.3.).
     A kártya itt MEGFORDUL, nem lesz magabiztosabb. A szöveg a konfigból jön,
     szó szerint a hibalista 3.3. pontja szerint — a végkicsengés nem az, hogy
     „ezt nem mi csináljuk", hanem hogy „idáig elkísérünk, és megmondjuk, hova
     tovább". A modul eddig sem hazudott, és most sem szabad. */
  function vizelhelyezesBlokk(k, kim) {
    const b = blokkFej(kim.fejlec);
    if (kim.bevezeto) b.appendChild(el("p", "type-ui-subtitle ajanlo-termek-szoveg", kim.bevezeto));
    if (Array.isArray(kim.tisztazni) && kim.tisztazni.length) {
      if (kim.tisztazniCim) {
        b.appendChild(el("p", "type-ui-body-strong ajanlo-okok-cim", kim.tisztazniCim));
      }
      const ul = el("ul", "ajanlo-okok");
      kim.tisztazni.forEach((s) => ul.appendChild(el("li", "type-ui-subtitle", s)));
      b.appendChild(ul);
    }
    return b;
  }

  function feltetelBlokk(k) {
    const b = blokkFej(SZOVEG.feltetelek);
    const lista = el("ul", "ajanlo-feltetel-lista");
    k.feltetelek.forEach((id) => {
      const f = K.feltetelek[id]; if (!f) return;
      const li = el("li", "ajanlo-feltetel");
      li.appendChild(svg(f.jel, "ajanlo-feltetel-jel"));
      const t = el("div");
      t.appendChild(el("p", "type-ui-body-strong", f.cimke));
      t.appendChild(el("p", "type-ui-subtitle ajanlo-feltetel-szoveg", f.leiras));
      li.appendChild(t);
      lista.appendChild(li);
    });
    b.appendChild(lista);
    return b;
  }

  /* TISZTÁZANDÓK — NAPIREND, NEM HIÁNYLISTA (hibalista 6.3.).
     Egy nyitott kérdésekből álló lista olvasható úgy is, hogy „még nem tudsz
     dönteni" — és úgy is, hogy „itt a kész napirended a beszélgetéshez". A
     második teszi a konzultációt természetes következő lépéssé. Ehhez
     elemenként három dolog kell: mit jelent, KI tudja megmondani, és nagyjából
     mennyi idő. Az üres mezőket kihagyjuk — az `ido` szándékosan üres, amíg a
     cég nem hagy jóvá értéket. */
  function tisztazandoBlokk(k) {
    const b = blokkFej(SZOVEG.tisztazandok);
    if (K.tisztazandokBevezeto) {
      b.appendChild(el("p", "type-ui-subtitle ajanlo-tisztazando-bevezeto", K.tisztazandokBevezeto));
    }
    const dl = el("dl", "ajanlo-tisztazando-lista");
    k.tisztazandok.forEach((id) => {
      const t = K.tisztazandok[id]; if (!t) return;
      const sor = el("div", "ajanlo-tisztazando");
      sor.appendChild(el("dt", "type-ui-body-strong", t.cimke));
      const dd = el("dd", "type-ui-subtitle");
      dd.appendChild(el("p", null, t.hogyan));
      if (t.ki) {
        const p = el("p", "type-ui-caption ajanlo-tisztazando-ki");
        p.appendChild(svg("kez", "ajanlo-tisztazando-jel"));
        p.appendChild(el("span", null, t.ki));
        dd.appendChild(p);
      }
      if (t.ido) {
        const p = el("p", "type-ui-caption ajanlo-tisztazando-ki");
        p.appendChild(svg("ora", "ajanlo-tisztazando-jel"));
        p.appendChild(el("span", null, t.ido));
        dd.appendChild(p);
      }
      sor.appendChild(dd);
      dl.appendChild(sor);
    });
    b.appendChild(dl);
    return b;
  }

  /* TOVÁBBLÉPÉS — kontaktadat NÉLKÜL (spec 7.), és KIMENETTÍPUS-FÜGGŐEN (H3).
     Korábban minden kimenet az ársávbecslőre küldött tovább — a zárt tároló és
     a határeset ágon is. Az vagy nem működött, vagy működött, és akkor olyasmi
     árát mutatta, ami nincs a kínálatban. */
  function ctaRajzol(k, kim) {
    const cta = el("div", "ajanlo-cta");

    const els = kim.elsodleges || {};
    if (els.url) {
      const fo = el("a", "btn btn-primary", els.cimke);
      fo.href = els.url;
      fo.addEventListener("click", () => mer("ajanlo_tovabb", { tipus: k.tipus, cel: els.url }));
      cta.appendChild(fo);
    }

    /* A „vízelhelyezés kérdéses" ág záró mondata a GOMB UTÁN áll: előbb a
       következő lépés, utána az őszinte kitekintés arra, mi lesz, ha a
       felmérés mégis a zárt tároló felé mutat. */
    if (kim.zaro) cta.appendChild(el("p", "type-ui-subtitle ajanlo-zaro", kim.zaro));

    /* Az ársávbecslő MÁSODLAGOSAN, ahol a nagyságrend még értelmes kérdés —
       és SEHOGY, ahol nincs mit árazni. */
    if (kim.arsav === "masodlagos" && K.tovabb && K.tovabb.arsav) {
      const a = el("a", "text-link ajanlo-arsav-masodlagos");
      a.href = K.tovabb.arsav.url;
      const burok = el("span", "link-label", kim.arsavCimke || K.tovabb.arsav.cimke);
      burok.appendChild(el("span", "action-arrow-end", "→")).setAttribute("aria-hidden", "true");
      a.appendChild(burok);
      a.addEventListener("click", () => mer("ajanlo_tovabb", { tipus: k.tipus, cel: "arsav" }));
      cta.appendChild(a);
    }

    cta.appendChild(mentesRajzol());

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
    return cta;
  }

  function eredmenyRajzol() {
    const k = kimenet();
    const kim = K.kimenetek[k.tipus] || K.kimenetek.termek;
    const doboz = el("div", "ajanlo-eredmeny");
    /* A kimenettípus a DOM-ban is látszik — a stílus és a mérés is ebből
       dolgozik, nem a fejléc szövegéből. */
    doboz.dataset.kimenet = k.tipus || "termek";

    doboz.appendChild(uzenetRajzol(K.lepesek[K.lepesek.length - 1].uzenet));

    (kim.blokkok || []).forEach((nev) => {
      if (nev === "termek" && k.irany) doboz.appendChild(termekBlokk(k, kim));
      else if (nev === "utkozes") doboz.appendChild(utkozesBlokk(k, kim));
      else if (nev === "vizelhelyezes") doboz.appendChild(vizelhelyezesBlokk(k, kim));
      else if (nev === "feltetelek" && k.feltetelek.length) doboz.appendChild(feltetelBlokk(k));
      else if (nev === "tisztazandok" && k.tisztazandok.length) doboz.appendChild(tisztazandoBlokk(k));
    });

    doboz.appendChild(ctaRajzol(k, kim));
    return doboz;
  }

  /* ==========================================================================
     MENTÉS — az azonosító MAGÁTÓL keletkezik (H11, 6.2.)
     --------------------------------------------------------------------------
     KORÁBBAN: zöld elsődleges gomb (ársávbecslő) → öt sor magyarázat →
     „Eredmény mentése" másodlagos gombként. Aki nem olvasta végig, nem mentett
     — és elvesztette a megoszthatóságot és a visszakereshetőséget. Senki ne
     veszítse el a munkáját azzal, hogy nem olvasott el egy bekezdést.

     MOSTANTÓL: az eredmény megjelenésekor a modul elmenti, és az azonosító ott
     van a képernyőn. A gomb már csak MEGOSZTÁSRA való — egy családi ház
     szennyvízkezeléséről ritkán dönt egy ember, és a link a második
     döntéshozót éri el.

     ADATOT EHHEZ SEM KÉRÜNK. A rekordban nincs személyes adat: a válaszok és a
     belőlük számított kimenet megy el, semmi más (spec 7.). Ezért nincs jogi
     akadálya annak, hogy magától keletkezzen.

     HA A VÉGPONT NEM ELÉRHETŐ (nincs `config.php`, ki van kapcsolva, hálózati
     hiba), a modul NEM hallgat el semmit: visszaáll a kézi mentésre, letölti a
     szöveges összefoglalót, és kimondja, hogy szerverre most nem került, tehát
     azonosító sincs. */

  let mentesFut = false;
  let mentesValasz = null;      /* {ok:true, azonosito} | {ok:false, uzenet} */
  let mentettUjjlenyomat = "";  /* a mentett VÁLASZOK lenyomata */

  /** A mentendő csomag — pontosan az, amit a látogató a képernyőn lát. */
  function mentendo() {
    const k = kimenet();
    const kim = K.kimenetek[k.tipus] || K.kimenetek.termek;
    const t = (k.irany && K.termekek[k.irany]) || {};
    const eg = K.termekek.egyeztetes || {};

    /* AMI A MENTETT LAPRA KERÜL, ugyanaz a négy kimenettípus szerint (H5): a
       nyomtatott példány sem állíthatja, hogy „a javasolt megoldás", ha a modul
       épp azt mondta ki, hogy nem tudja eldönteni. */
    let okok = k.utkozesek.map((o) => ({ cimke: o }));
    let okokCim = "";
    let indoklas = t.indoklas || "";
    if (k.tipus === "egyeztetes") {
      okokCim = "Melyik két szempont ütközik";
      indoklas = [eg.indoklas, eg.megnyugtatas].filter(Boolean).join(" ");
    } else if (k.tipus === "vizelhelyezes") {
      okokCim = kim.tisztazniCim || "";
      okok = (kim.tisztazni || []).map((s) => ({ cimke: s }));
      indoklas = [kim.bevezeto, kim.zaro].filter(Boolean).join(" ");
    }

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
        tipus: k.tipus || "",
        irany: k.irany || "",
        cim: kim.fejlec,
        termekNev: t.nev || "",
        indoklas: indoklas,
        kompromisszum: t.kompromisszum || "",
        okokCim: okokCim,
        okok: okok,
        feltetelek: k.feltetelek.map((id) => {
          const f = K.feltetelek[id] || {};
          return { cimke: f.cimke || id, szoveg: f.leiras || "" };
        }),
        tisztazandok: k.tisztazandok.map((id) => {
          const x = K.tisztazandok[id] || {};
          return { cimke: x.cimke || id, szoveg: [x.hogyan, x.ki, x.ido].filter(Boolean).join(" ") };
        })
      }
    };
  }

  function osszefoglalo(azonosito) {
    const k = kimenet();
    const kim = K.kimenetek[k.tipus] || K.kimenetek.termek;
    const t = (k.irany && K.termekek[k.irany]) || null;
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
    sorok.push(kim.fejlec.toUpperCase());
    if (t) { sorok.push(t.nev); sorok.push(t.indoklas); }
    if (t && t.kompromisszum) { sorok.push(""); sorok.push(t.kompromisszum); }
    if (k.tipus === "egyeztetes") {
      const eg = K.termekek.egyeztetes || {};
      if (eg.indoklas) sorok.push(eg.indoklas);
      if (eg.megnyugtatas) { sorok.push(""); sorok.push(eg.megnyugtatas); }
    }
    if (k.tipus === "vizelhelyezes" && kim.bevezeto) sorok.push(kim.bevezeto);
    if (k.utkozesek.length) {
      sorok.push("");
      k.utkozesek.forEach((o) => sorok.push("- " + o));
    }
    if (k.tipus === "vizelhelyezes" && Array.isArray(kim.tisztazni)) {
      sorok.push(""); sorok.push(kim.tisztazniCim || "");
      kim.tisztazni.forEach((s) => sorok.push("- " + s));
      if (kim.zaro) { sorok.push(""); sorok.push(kim.zaro); }
    }
    if (k.feltetelek.length) {
      sorok.push(""); sorok.push("KIVITELEZÉSI FELTÉTELEK");
      k.feltetelek.forEach((id) => {
        const f = K.feltetelek[id]; if (f) sorok.push("- " + f.cimke + ": " + f.leiras);
      });
    }
    sorok.push(""); sorok.push("TISZTÁZANDÓK");
    k.tisztazandok.forEach((id) => {
      const x = K.tisztazandok[id];
      if (x) sorok.push("- " + x.cimke + ": " + [x.hogyan, x.ki].filter(Boolean).join(" "));
    });
    sorok.push("");
    sorok.push("ÖkoTech-Home Kft. · 2509 Esztergom, Strázsa u. 12.");
    sorok.push("+36 33 200 211 · kapcsolat@okotechhome.hu · okotechhome.hu");
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

  /* AZ AUTOMATIKUS MENTÉS. Az eredmény megjelenésekor indul, és pontosan
     egyszer fut le VÁLASZ-ÁLLÁSONKÉNT: az ujjlenyomat miatt a újrarajzolás
     nem indít új kérést, egy visszalépés utáni MÓDOSÍTÁS viszont igen — hiszen
     akkor a mentett rekord elavult. A már meglévő azonosítót az `ugy.js` viszi
     tovább, tehát a frissítés ugyanabba az ügybe kerül. */
  function automentes() {
    if (!window.OthUgy || mentesFut) return;
    const ujj = JSON.stringify(allapot.valaszok);
    if (ujj === mentettUjjlenyomat) return;
    mentesFut = true;
    mentettUjjlenyomat = ujj;
    window.OthUgy.ment("ajanlo", mentendo()).then((v) => {
      mentesFut = false;
      mentesValasz = v;
      /* Ha közben visszalépett, ne rántsuk vissza az eredményhez — csak akkor
         rajzolunk újra, ha még mindig azt nézi. */
      if (allapot.kesz) rajzol();
    }, () => {
      mentesFut = false;
      mentesValasz = { ok: false, uzenet: "" };
      if (allapot.kesz) rajzol();
    });
  }

  /** Az azonosító és a megosztás — vagy a tartalék, ha a mentés nem sikerült. */
  function mentesRajzol() {
    const d = el("div", "ajanlo-mentve");

    /* Amíg a kérés fut, nem ígérünk semmit: a doboz üresen marad, és a
       `role="status"` majd felolvassa, ha megjött. */
    if (!mentesValasz) {
      d.dataset.allapot = "fut";
      d.setAttribute("role", "status");
      d.setAttribute("aria-busy", "true");
      return d;
    }

    if (!mentesValasz.ok) {
      /* TARTALÉK: kézi mentés, ahogy eddig. A látogató nem veszít semmit, de
         megmondjuk, hogy azonosító most nem keletkezett. */
      d.dataset.allapot = "tartalek";
      d.setAttribute("role", "status");
      d.appendChild(svg("figyelem", "ajanlo-mentve-jel"));
      const sz = el("div", "ajanlo-mentve-szoveg");
      sz.appendChild(el("p", "type-ui-body-strong", SZOVEG.nemSikerult));
      sz.appendChild(el("p", "type-ui-subtitle", (mentesValasz.uzenet ? mentesValasz.uzenet + " " : "")
        + "Az eredményt szövegfájlként letöltheti, tehát nem vész el — "
        + "azonosító viszont ehhez nem tartozik, és visszakeresni sem tudjuk."));
      const g = el("button", "btn btn-halvany", SZOVEG.mentes);
      g.type = "button";
      g.addEventListener("click", () => szovegLetolt(""));
      sz.appendChild(g);
      d.appendChild(sz);
      return d;
    }

    d.dataset.allapot = "kesz";
    d.setAttribute("role", "status");
    d.appendChild(svg("pipa", "ajanlo-mentve-jel"));

    const azon = mentesValasz.azonosito;
    const cim = window.OthUgy.eredmenyUrl(azon);
    const sz = el("div", "ajanlo-mentve-szoveg");
    sz.appendChild(el("p", "type-ui-body-strong", SZOVEG.elmentve));
    sz.appendChild(el("p", "ajanlo-mentve-azonosito type-data-value", azon));
    if (K.mentes.azonositoMagyarazat) {
      sz.appendChild(el("p", "type-ui-caption ajanlo-mentve-mi-ez", K.mentes.azonositoMagyarazat));
    }
    const a = el("a", "text-link ajanlo-mentve-link");
    a.href = window.OthUgy.eredmenyHref(azon);
    const b = el("span", "link-label", SZOVEG.megnyitas);
    b.appendChild(el("span", "action-arrow-end", "→")).setAttribute("aria-hidden", "true");
    a.appendChild(b);
    sz.appendChild(a);
    /* A teljes cím LÁTHATÓ szövegként is: a kinyomtatott lapon a kattintható
       hivatkozás semmit nem ér, a beírható cím viszont igen — és ha a vágólap
       nem érhető el, ez marad a kijelölhető tartalék. */
    sz.appendChild(el("p", "type-ui-caption ajanlo-mentve-cim", cim));

    if (K.mentes.linkBevezeto) {
      const bev = el("p", "type-ui-subtitle ajanlo-mentes-bevezeto", K.mentes.linkBevezeto);
      /* Öko itt is megszólal, amikor a látogató idegörget — lásd kalauz.js PONTOK. */
      bev.dataset.okoPont = "mentes";
      sz.appendChild(bev);
    }

    /* LINK MÁSOLÁSA. A `navigator.clipboard` csak biztonságos eredetben és
       felhasználói mozdulatra működik; ha nem megy, nem hallgatunk, hanem
       odamutatunk a fenti, kijelölhető címre. */
    const gomb = el("button", "btn btn-halvany ajanlo-masol");
    gomb.type = "button";
    gomb.appendChild(svg("lanc", "ajanlo-masol-jel"));
    const felirat = el("span", null, SZOVEG.linkMasolas);
    gomb.appendChild(felirat);
    const visszajelzes = el("p", "type-ui-caption ajanlo-masolva");
    visszajelzes.setAttribute("role", "status");
    gomb.addEventListener("click", () => {
      const kesz = (siker) => {
        visszajelzes.textContent = siker ? SZOVEG.linkMasolva : SZOVEG.linkNemSikerult;
        mer("ajanlo_link_masolas", { siker: siker ? 1 : 0 });
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(cim).then(() => kesz(true), () => kesz(false));
      } else { kesz(false); }
    });
    sz.appendChild(gomb);
    sz.appendChild(visszajelzes);

    if (K.mentes.bevezeto) {
      sz.appendChild(el("p", "type-ui-caption ajanlo-mentve-megjegyzes",
        K.mentes.bevezeto + " " + (K.mentes.megorzesSzoveg || "")));
    }
    d.appendChild(sz);
    return d;
  }

  function asszisztensRajzol() {
    const kartya = el("div", "ajanlo-asszisztens");
    const aktivLepes = lepesIndex(K.kerdesek[allapot.aktiv].lepes);
    /* A záró képernyőn MINDEN szakasz kész — a sín ilyenkor nem jelöl aktívat,
       különben ellentmondana a panelnek, ami már „Kész"-t ír a 6. szakaszra. */
    kartya.appendChild(sinRajzol(allapot.kesz ? K.lepesek.length : aktivLepes));

    const tartalom = el("div", "ajanlo-tartalom");

    const fej = el("div", "ajanlo-fej");
    const cimek = el("div");
    cimek.appendChild(el("p", "type-ui-card-title ajanlo-fej-cim", SZOVEG.asszisztens));
    cimek.appendChild(el("p", "type-ui-subtitle ajanlo-fej-alcim",
      SZOVEG.ajanloCim + kerdesSzam + SZOVEG.rovidKerdes));
    fej.appendChild(cimek);
    const szamlalo = el("p", "ajanlo-szamlalo");
    szamlalo.appendChild(el("span", "ajanlo-szamlalo-most",
      String(allapot.kesz ? K.lepesek.length : aktivLepes + 1)));
    szamlalo.appendChild(el("span", "ajanlo-szamlalo-ossz", " / " + K.lepesek.length));
    fej.appendChild(szamlalo);
    tartalom.appendChild(fej);

    /* A gépi válaszkulcsokat a munkamenetbe akkor is eltesszük, ha a mentés nem
       sikerül: a 8. szekció így is át tudja venni, amit itt megadott. */
    if (allapot.kesz && window.OthUgy) {
      window.OthUgy.jegyez("ajanlo", Object.assign({}, allapot.valaszok), "");
      /* A teljes kimenet is a munkamenetbe kerül. Ha a szerveres mentés
         elakad, de a látogató az ársávbecslőnél ment, ez a blokk ugyanabba az
         ügybe kerül fel: így nem lesz féloldalas a rekord. */
      window.OthUgy.fuggoben("ajanlo", mentendo());
      automentes();
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

  const ALLAPOT_SZO = SZOVEG.allapotSzo;
  const ALLAPOT_JEL = { kesz: "pipa", aktiv: "folyamat", nyitott: "kor" };

  /* A SZAKASZOK KATTINTHATÓK (H14). A „Kész ✓" jelölés eddig kattinthatónak
     LÁTSZOTT, de nem volt az. Most az, ahova a látogató már eljutott, oda
     vissza is ugorhat — előre nem: az előreugrás átugrott kérdéseket hagyna,
     és a modul pont azért kérdez sorban, mert az egyik válasz a másikat
     értelmezi. */
  function lepesreUgras(i) {
    const l = K.lepesek[i];
    if (l.zaro) { allapot.kesz = true; rajzol(); return; }
    const elso = kerdesekLepesben(l.id)[0];
    if (!elso) return;
    allapot.kesz = false;
    allapot.aktiv = K.kerdesek.indexOf(elso);
    rajzol();
    const be = gyoker.querySelector(".ajanlo-kerdes:not([data-elonezet]) input");
    if (be) be.focus();
  }

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
      allapot.kesz ? SZOVEG.allapotKesz : SZOVEG.allapotFolyamatban));
    panel.appendChild(pirula);

    panel.appendChild(el("h3", "type-display-highlight-title ajanlo-panel-cim", SZOVEG.helyzetkep))
      .id = "ajanlo-panel-cim";
    const megvalaszolt = K.kerdesek.filter((q) => allapot.valaszok[q.id]).length;
    panel.appendChild(el("p", "type-ui-subtitle ajanlo-panel-alcim",
      megvalaszolt + " / " + kerdesSzam + SZOVEG.valaszMegadva));

    /* A hat szakasz állapota */
    const lista = el("ol", "ajanlo-lepeslista");
    const elertLepes = Math.max(aktivLepes, lepesIndex(K.kerdesek[allapot.legtavolabb].lepes),
                                allapot.vegigert ? K.lepesek.length - 1 : 0);
    K.lepesek.forEach((l, i) => {
      const a = lepesAllapot(l, i, aktivLepes);
      const li = el("li", "ajanlo-lepessor");
      li.dataset.allapot = a;
      /* Oda ugorhat vissza, ahol már járt — és a záró szakaszra csak akkor, ha
         egyszer már látta az eredményt. */
      const ugorhat = i <= elertLepes && !(l.zaro && !allapot.vegigert)
                      && !(i === aktivLepes && !allapot.kesz);
      const test = el(ugorhat ? "button" : "div", "ajanlo-lepestest");
      if (ugorhat) {
        test.type = "button";
        test.setAttribute("aria-label", SZOVEG.lepesreUgras + l.cim);
        test.addEventListener("click", () => lepesreUgras(i));
      }
      test.appendChild(el("span", "ajanlo-lepesszam type-data-value",
        String(i + 1).padStart(2, "0")));
      test.appendChild(el("span", "type-ui-body ajanlo-lepescim", l.cim));
      const jelzo = el("span", "ajanlo-lepesjelzo");
      jelzo.appendChild(el("span", "type-ui-subtitle", ALLAPOT_SZO[a]));
      jelzo.appendChild(svg(ALLAPOT_JEL[a], "ajanlo-lepesjel"));
      test.appendChild(jelzo);
      li.appendChild(test);
      lista.appendChild(li);
    });
    panel.appendChild(lista);

    const k = kimenet();

    /* ── JELENLEGI IRÁNY — STÁTUSZ + INDOKLÁS (H6, 4.1.) ────────────────────
       A kártya nem fagy meg: az indoklás minden válasz után lép, és a
       bizonyosság FOKA ki van írva. Ellentmondásnál és szűk területnél a
       kártya MEGFORDUL — nem lesz magabiztosabb. */
    panel.appendChild(el("p", "type-ui-label ajanlo-panel-felirat", SZOVEG.jelenlegiIrany));
    const all = iranyAllapot(k);
    const iranyDoboz = el("div", "ajanlo-irany");
    iranyDoboz.dataset.kimenet = k.tipus || "nyitott";

    if (!k.tipus) {
      iranyDoboz.appendChild(svg("info", "ajanlo-irany-jel"));
      iranyDoboz.appendChild(el("p", "type-ui-subtitle ajanlo-irany-szoveg", SZOVEG.iranyKesobb));
    } else {
      const kim = K.kimenetek[k.tipus] || K.kimenetek.termek;
      const termek = k.irany && K.termekek[k.irany];
      iranyDoboz.appendChild(svg(kim.jel, "ajanlo-irany-jel"));
      const sz = el("div");
      /* A NÉV VAGY A STÁTUSZ áll elöl, alatta az indoklás. Terméknél a
         terméknév a név, alatta a bizonyosság; ellentmondásnál és szűk
         területnél maga a státusz. */
      sz.appendChild(el("p", "type-ui-body-strong ajanlo-irany-nev",
        termek ? termek.nev : (all && all.cimke) || ""));
      if (termek && all && all.cimke) {
        sz.appendChild(el("p", "type-ui-label ajanlo-irany-statusz", all.cimke));
      }
      if (all && all.szoveg) {
        sz.appendChild(el("p", "type-ui-subtitle ajanlo-irany-szoveg", all.szoveg));
      }
      /* AZ EPURECO-KOMPROMISSZUM MÁR ITT (hibalista 10.). Ha valaki három
         kérdésen át egy terméknevet lát, majd a végén kap egy fenntartást, az
         csalódás; ha a kompromisszum az első pillanattól ott van, az
         őszinteség. */
      if (termek && termek.kompromisszumRovid) {
        sz.appendChild(el("p", "type-ui-caption ajanlo-irany-fenntartas", termek.kompromisszumRovid));
      }
      iranyDoboz.appendChild(sz);
    }
    panel.appendChild(iranyDoboz);

    /* ── AMI EDDIG ELDŐLT (4.2.) ────────────────────────────────────────────
       A magyarázatok a bal oldalon buborékban jelennek meg, és elgörögnek. A
       jobb oldali panel pont arra való, hogy megmaradjanak: a tartalom kész
       volt, csak nem ott volt, ahol marad. */
    const lev = levezetesek();
    if (lev.length) {
      panel.appendChild(el("p", "type-ui-label ajanlo-panel-felirat", SZOVEG.eldoltCim));
      const ul = el("ul", "ajanlo-eldolt");
      lev.forEach((x) => {
        const li = el("li", "ajanlo-eldolt-sor");
        li.appendChild(el("span", "type-ui-subtitle ajanlo-eldolt-bal", x.bal));
        li.appendChild(el("span", "ajanlo-eldolt-nyil", "→")).setAttribute("aria-hidden", "true");
        li.appendChild(el("span", "type-ui-subtitle ajanlo-eldolt-jobb", x.jobb));
        ul.appendChild(li);
      });
      panel.appendChild(ul);
    }

    /* Kivitelezési feltételek — chipként, ahogy már látszanak */
    if (k.feltetelek.length) {
      panel.appendChild(el("p", "type-ui-label ajanlo-panel-felirat",
        SZOVEG.feltetelekLatszanak));
      const chipek = el("ul", "ajanlo-chipek");
      k.feltetelek.forEach((id) => {
        const f = K.feltetelek[id]; if (!f) return;
        const li = el("li", "ajanlo-chip");
        li.appendChild(svg(f.jel, "ajanlo-chip-jel"));
        li.appendChild(el("span", "type-ui-subtitle", f.cimke));
        chipek.appendChild(li);
      });
      panel.appendChild(chipek);
    }

    /* Tisztázandók */
    if (k.tisztazandok.length) {
      panel.appendChild(el("p", "type-ui-label ajanlo-panel-felirat", SZOVEG.tisztazandok));
      const ul = el("ul", "ajanlo-tisztazando-rovid");
      k.tisztazandok.forEach((id) => {
        const t = K.tisztazandok[id]; if (!t) return;
        ul.appendChild(el("li", "type-ui-subtitle", t.cimke));
      });
      panel.appendChild(ul);
    }

    /* A záró figyelmeztetés csak amíg tart a folyamat: a kimenet után már nem
       „nem végleges", hanem kész — ott a tisztázandók listája a helyén beszél. */
    if (!allapot.kesz) {
      const fig = el("p", "ajanlo-figyelem");
      fig.appendChild(svg("figyelem", "ajanlo-figyelem-jel"));
      const sz = el("span", "type-ui-subtitle");
      sz.appendChild(el("strong", null, "Fontos:"));
      sz.appendChild(document.createTextNode(SZOVEG.nemVegleges));
      fig.appendChild(sz);
      panel.appendChild(fig);
    }

    return panel;
  }

  /* ==========================================================================
     KIRAJZOLÁS
     ========================================================================== */
  let mertKimenet = "";

  function rajzol() {
    /* A LEGTÁVOLABBI PONT nyilvántartása — ebből tudja a panel, melyik
       szakaszra lehet visszaugrani (H14). */
    if (allapot.aktiv > allapot.legtavolabb) allapot.legtavolabb = allapot.aktiv;
    if (allapot.kesz) allapot.vegigert = true;

    /* 6.6. · A KIMENETTÍPUSOK ELOSZLÁSA. Ha az egyeztetés aránya nagyon magas,
       a döntési fa túl óvatos; ha nagyon alacsony, túl magabiztos. Egy
       látogatónál kimenettípusonként egyszer mérünk. */
    if (allapot.kesz) {
      const k = kimenet();
      const kulcs = (k.tipus || "") + "|" + (k.irany || "");
      if (kulcs !== mertKimenet) {
        mertKimenet = kulcs;
        mer("ajanlo_kimenet", { tipus: k.tipus || "", irany: k.irany || "",
                                teljes: k.mindMegvan ? 1 : 0 });
      }
    }

    const test = el("div", "ajanlo-body");
    test.appendChild(asszisztensRajzol());
    test.appendChild(panelRajzol());
    gyoker.replaceChildren(test);
  }

  /* 6.1. · HÁNYAN JUTNAK EL A MODULIG. A specifikáció szerint ez „a weboldal
     első interaktív eleme, amivel a látogató találkozik" — közben a főoldal 6.
     szekciójában fut. A két állítás nem fér össze, és amíg nem tudjuk, hányan
     görgetnek le idáig, a modul belső konverziójának javítása egy ismeretlen
     szám töredékén dolgozik. Ez az egyetlen pont, ahol a mérés előzze meg a
     fejlesztést — az eredménye megváltoztathatja a többi prioritását. */
  if (typeof IntersectionObserver === "function") {
    const figyelo = new IntersectionObserver((bejegyzesek) => {
      bejegyzesek.forEach((b) => {
        if (!b.isIntersecting) return;
        mer("ajanlo_lathato", {});
        figyelo.disconnect();
      });
    }, { threshold: 0.25 });
    figyelo.observe(gyoker);
  }

  rajzol();
})();
