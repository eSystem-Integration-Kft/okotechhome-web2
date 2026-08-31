/* ============================================================================
   ÖkoTech-Home — AI-alapú döntéstámogató (Mitől függ az ár?) modul
   ----------------------------------------------------------------------------
   Beágyazott, chat-jellegű, 6-kérdéses előminősítő. Kimenet: nagyságrendi
   ársáv + személyre szabott, szöveges összefoglaló.

   FONTOS TERVEZÉSI ELV (spec 6. pont):
   - A SZÁMOT (ársávot) NEM az AI adja, hanem a lenti PRICE_TABLE logikai tábla.
     Ez élesben egy karbantartható konfig (admin-felület / DB-tábla) legyen,
     amit a cég (Anna) a fejlesztő nélkül is frissíthet. A lenti értékek
     PLACEHOLDEREK — éles indulás előtt Anna hagyja jóvá őket.
   - A SZÖVEGET (nyugtázás, magyarázat, összefoglaló) itt sablonok adják. Éles
     környezetben ide köthető egy szigorú rendszerprompttal futó AI-hívás, a
     cég tudásanyagára korlátozva (a modell csak fogalmaz, szakmai döntést nem hoz).
   - Adatkezelés: a folyamat elején SEMMILYEN személyes adatot nem kérünk.
     Email + visszahívás csak az eredményképernyőn, egymástól elkülönítve.
   ========================================================================== */
(() => {
  "use strict";

  /* ---------------------------------------------------------------- KÉRDÉSEK */
  /* A pontos szövegek külön dokumentumban véglegesednek — ez a szerkezet. */
  /* A NYELVET a `<html lang>` adja meg. A kérdések, a válaszcímkék és a
     magyarázatok nyelvenként külön táblában állnak — a VÁLASZAZONOSÍTÓK
     viszont mindkettőben azonosak, mert az ársávtábla, a mentett ügyrekord és
     a megoldás-ajánlóból való átvétel mind ezekre kulcsol. */
  const NYELV = (document.documentElement.lang || 'hu').slice(0, 2) === 'en' ? 'en' : 'hu';


  /* ------------------------------------------------------- FELÜLETI SZÖVEG ---
     A kérdések nyelvenkénti tábláját fent a `KERDESEK` adja; ide a felület
     állandó feliratai kerülnek. Azért egy fájlban a motorral, mert ezek a
     modul szerkezetéhez tartoznak, nem a cég szerkeszti őket. */
  const T = {
    hu: {
      udvozles: "Üdvözlöm! Hat rövid kérdésen vezetem végig, hogy lássa, milyen tényezők befolyásolják az előzetes ársávot.",
      koszonom: "Köszönöm.",
      milliFt: "millió Ft",
      egyediMeretezes: "Egyedi méretezés",
      dKapacitas: (c) => `<b>Kapacitás (${c}):</b> ez adja a rendszer alap-méretezését, ez a legnagyobb tétel.`,
      dTalajviz: "<b>Magas talajvíz:</b> a tartály körüli betonozás / kiegészítő megoldás feljebb tolja a költséget.",
      dKevesHely: "<b>Kevés hely:</b> szűk telken a beépítés és a gépi munka igényesebb.",
      dHozzaferes: "<b>Nehéz gépi hozzáférés:</b> a kivitelezés több munkát és időt kíván.",
      dEmeszto: "<b>Emésztő kiváltása:</b> a régi akna bontása és a többletmunka növeli a beruházást.",
      dCsere: "<b>Rendszercsere:</b> a meglévő elemek kezelése többletmunkát jelent.",
      dIdoszakos: "<b>Időszakos használat:</b> más technológia is szóba jöhet, ez a méretezést és a költséget is befolyásolja.",
      pTelek: "A telek méretei és egy egyszerű helyszínrajz (akár kézzel).",
      pHasznalat: "A tervezett használat (állandó / időszakos) és a várható létszám.",
      pTalajviz: "Amit a talajvízszintről / talajviszonyokról tud.",
      pMeglevo: "A meglévő rendszer adatai (típus, kor, elhelyezkedés).",
      pElvezetes: "Az elvezetéshez elképzelt irány (szikkasztás / öntözés / élővíz).",
      tovabb: "Tovább",
      kivalasztva: "kiválasztva",
      valasszonTobbet: "Válasszon egyet vagy többet",
      ajanlobol: "A megoldás-ajánlóból",
      tobbValaszthato: "Több is választható",
      miertSzamit: "Miért számít ez?",
      megNyitott: "Még nyitott",
      atveve: "átvéve",
      otPerc: "Kb. 5 perc az egész",
      helyzetkep: "Az Ön helyzetképe",
      valaszMegadva: "válasz megadva",
      elozetesArsav: "Előzetes ársáv",
      megKell: (n) => `Még ${n} válasz szükséges`,
      keszNezze: "Kész — nézze meg az összefoglalót",
      pontosodik: "A becslés a válaszokkal pontosodik.",
      fontosTajekoztato: "<b>Fontos:</b> az eredmény tájékoztató jellegű, nem végleges árajánlat.",
      tajBecsles: "Tájékozódási becslés · nem árajánlat",
      egyediSzoveg: "Ekkora kapacitásnál (10 fő felett) telep-kategóriás, egyedileg méretezett megoldásról beszélünk — a sávot felmérés után adjuk meg pontosan.",
      tajSav: "Tájékozódási sáv · nem árajánlat",
      savSzoveg: "Ez egy nagyságrendi tájékozódási sáv az Ön válaszai alapján. A pontos árat mindig helyszíni, szakértői konzultáció után adjuk meg.",
      osszefoglaloEyebrow: "Az Ön előzetes összefoglalója",
      osszefoglaloCim: "Íme, amit a válaszaiból látunk",
      mozgatjak: "Önnél ezek mozgatják leginkább a költséget",
      erdemesTisztazni: "Ezt érdemes még tisztázni",
      nincsNyitott: "Nincs nyitott kérdés",
      mindenMegadva: "Minden lényeges pontot megadott — a konzultáción a részleteket finomítjuk.",
      elokesziteni: "Mit érdemes előkészíteni a konzultációra",
      elkuldomMagamnak: "Elküldöm magamnak az összefoglalót",
      egyszeriEmail: "Egyszeri email az összefoglalóval. Ez önmagában nem jelent megkeresési hozzájárulást.",
      emailCim: "E-mail-cím",
      elkuldom: "Elküldöm",
      keressenMeg: "Kérem, hogy a cég szakértője nézze át a helyzetemet és keressen meg.",
      adatFelhasznalas: "Az adatait kizárólag az összefoglaló elküldésére és — külön jelölés esetén — a kapcsolatfelvételre használjuk. Részletek:",
      adatkezeles: "Adatkezelési tájékoztató",
      konzultaciotKerek: "Konzultációt kérek",
      ujrakezdem: "Újrakezdem a kérdéseket",
      jogiKitetel: "Az ársáv tájékoztató jellegű, nem végleges árajánlat. A számokat a cég szakmai vezetése hagyja jóvá; a pontos ajánlat helyszíni felmérés után készül.",
      nincsElesitve: "A küldés még nincs élesítve",
      nincsElesitveSzoveg: "Az összefoglaló e-mailes küldése hamarosan indul. Addig az eredményt a böngészőből kinyomtathatja, vagy hívjon minket:",
      elkuldtuk: "Elküldtük az összefoglalót",
      nezzeMeg: "nézze meg a beérkezők között.",
      hamarosanJelentkezik: "Szakértőnk hamarosan jelentkezik.",
      kuldesNemSikerult: "A küldés most nem sikerült. Próbálja újra, vagy hívjon minket: +36 33 200 211.",
      asszisztens: "ÖkoTechHome AI Asszisztens",
      fejAlcim: "Előzetes ársáv · 6 rövid kérdés",
      helyzetkepRovid: "Az Ön helyzetképe ·",
      reszben: "(részben)",
      atvettuk: "Átvettük a megoldás-ajánlóból:",
      ugyazonosito: "Ügyazonosító:",
      atirhatja: "Bármelyiket átírhatja a helyzetkép-panelen.",
      megsem: "Mégsem, üresen kezdem",
      atTudjukVenni: "Az adatait át tudjuk venni a megoldás-ajánlóból.",
      nemKerdezzukUjra: "Amit ott már megadott, azt itt nem kérdezzük újra.",
      adatAtvetel: "Adatok átvétele",
      vanMentett: "Van mentett azonosítója a megoldás-ajánlóból?",
      irjaBe: "Írja be, és amit ott megadott, azt itt nem kérdezzük újra.",
      betoltes: "Betöltés",
      nincsMitAtvenni: "Ezekből a válaszokból itt nem tudtunk mit átvenni.",
      nincsIlyenAzon: "Ezt az azonosítót nem találjuk.",
      nincsHasznalhato: "Ehhez az azonosítóhoz nincs olyan válasz, amit itt fel tudnánk használni.",
      mentsEl: "Mentse el az ársávot is az ügyéhez",
      mentesLeiras: "Azonosítót kap hozzá, amivel bármikor előveheti és PDF-be mentheti. Ez nem regisztráció: nevet, e-mail-címet nem kérünk hozzá.",
      ajanloIsIde: "A megoldás-ajánló eredménye ugyanide kerül.",
      eredmenyMentese: "Eredmény mentése",
      elmentettuk: "Elmentettük. Az ügy azonosítója:",
      mikodEz: "Mi ez? Egy kód, ami a válaszait köti össze — személyes adat nélkül.",
      megnyitas: "Megnyitás, nyomtatás és PDF-be mentés",
      nemSikerultMenteni: "Most nem sikerült elmenteni",
      probaljaUjra: "Kérjük, próbálja újra néhány perc múlva.",
      arsavTermek: "Előzetes ársáv",
      arsavIndoklas: "A megadott válaszok alapján számított, tájékoztató ársáv. "
    },
    en: {
      udvozles: "Welcome. I will take you through six short questions so you can see which factors shape the indicative price range.",
      koszonom: "Thank you.",
      milliFt: "million HUF",
      egyediMeretezes: "Individual sizing",
      dKapacitas: (c) => `<b>Capacity (${c}):</b> this sets the basic sizing of the system, and it is the largest single item.`,
      dTalajviz: "<b>High groundwater:</b> concreting around the tank or an additional solution pushes the cost up.",
      dKevesHely: "<b>Little space:</b> on a tight plot the installation and the machine work are more demanding.",
      dHozzaferes: "<b>Difficult machine access:</b> the build takes more work and more time.",
      dEmeszto: "<b>Cesspit replacement:</b> demolishing the old chamber and the extra work raise the investment.",
      dCsere: "<b>System replacement:</b> dealing with the existing components means extra work.",
      dIdoszakos: "<b>Intermittent use:</b> another technology may come into play, and this affects both the sizing and the cost.",
      pTelek: "The plot's dimensions and a simple site plan (a hand sketch will do).",
      pHasznalat: "The intended use (permanent / intermittent) and the expected number of people.",
      pTalajviz: "Whatever you know about the groundwater level and ground conditions.",
      pMeglevo: "Details of the existing system (type, age, location).",
      pElvezetes: "The intended means of disposal (infiltration / irrigation / watercourse).",
      tovabb: "Next",
      kivalasztva: "selected",
      valasszonTobbet: "Choose one or more",
      ajanlobol: "From the solution finder",
      tobbValaszthato: "More than one can be chosen",
      miertSzamit: "Why does this matter?",
      megNyitott: "Still open",
      atveve: "carried over",
      otPerc: "About 5 minutes in all",
      helyzetkep: "Your situation so far",
      valaszMegadva: "answers given",
      elozetesArsav: "Indicative price range",
      megKell: (n) => `${n} more answer${n === 1 ? "" : "s"} needed`,
      keszNezze: "Done — take a look at the summary",
      pontosodik: "The estimate sharpens with each answer.",
      fontosTajekoztato: "<b>Important:</b> the result is indicative, not a final quotation.",
      tajBecsles: "Indicative estimate · not a quotation",
      egyediSzoveg: "At this capacity (more than 10 people) we are talking about a plant-scale, individually sized solution — we give the range precisely after a survey.",
      tajSav: "Indicative range · not a quotation",
      savSzoveg: "This is an order-of-magnitude indicative range based on your answers. We always give the exact price after an on-site expert consultation.",
      osszefoglaloEyebrow: "Your preliminary summary",
      osszefoglaloCim: "Here is what your answers show",
      mozgatjak: "In your case these drive the cost most",
      erdemesTisztazni: "These are still worth clarifying",
      nincsNyitott: "No open questions",
      mindenMegadva: "You have given every material point — we will refine the details at the consultation.",
      elokesziteni: "What is worth preparing for the consultation",
      elkuldomMagamnak: "Send the summary to myself",
      egyszeriEmail: "A single email with the summary. On its own this is not consent to be contacted.",
      emailCim: "Email address",
      elkuldom: "Send",
      keressenMeg: "Please have your specialist review my situation and get in touch.",
      adatFelhasznalas: "We use your details solely to send the summary and — where you tick the box — to make contact. Details:",
      adatkezeles: "Privacy notice",
      konzultaciotKerek: "Request a consultation",
      ujrakezdem: "Start the questions again",
      jogiKitetel: "The price range is indicative, not a final quotation. The figures are approved by the company's technical management; the exact quote follows an on-site survey.",
      nincsElesitve: "Sending is not live yet",
      nincsElesitveSzoveg: "Emailing the summary goes live shortly. Until then you can print the result from your browser, or call us:",
      elkuldtuk: "The summary has been sent",
      nezzeMeg: "check your inbox.",
      hamarosanJelentkezik: "Our specialist will be in touch shortly.",
      kuldesNemSikerult: "Sending failed just now. Please try again, or call us: +36 33 200 211.",
      asszisztens: "ÖkoTechHome AI Assistant",
      fejAlcim: "Indicative price range · 6 short questions",
      helyzetkepRovid: "Your situation so far ·",
      reszben: "(in part)",
      atvettuk: "Carried over from the solution finder:",
      ugyazonosito: "Case reference:",
      atirhatja: "You can change any of them in the situation panel.",
      megsem: "No thanks, start from scratch",
      atTudjukVenni: "We can carry your details over from the solution finder.",
      nemKerdezzukUjra: "What you gave there, we will not ask again here.",
      adatAtvetel: "Carry the data over",
      vanMentett: "Do you have a saved reference from the solution finder?",
      irjaBe: "Type it in, and what you gave there we will not ask again here.",
      betoltes: "Load",
      nincsMitAtvenni: "There was nothing in those answers we could use here.",
      nincsIlyenAzon: "We cannot find that reference.",
      nincsHasznalhato: "That reference holds no answer we could use here.",
      mentsEl: "Save the price range to your case too",
      mentesLeiras: "You get a reference for it, so you can return to it at any time and save it as a PDF. This is not registration: we ask for no name and no email address.",
      ajanloIsIde: "The solution finder's result lands in the same place.",
      eredmenyMentese: "Save the result",
      elmentettuk: "Saved. The case reference:",
      mikodEz: "What is this? A code that ties your answers together — with no personal data.",
      megnyitas: "Open, print or save as PDF",
      nemSikerultMenteni: "Could not be saved just now",
      probaljaUjra: "Please try again in a few minutes.",
      arsavTermek: "Indicative price range",
      arsavIndoklas: "An indicative price range calculated from the answers given. "
    }
  }[NYELV];

  const KERDESEK = {
  hu: [
    {
      id: "kapacitas", step: "Kapacitás",
      q: "Hány fő használja majd rendszeresen a rendszert?",
      why: "A használók száma meghatározza, mekkora kapacitásra kell méretezni a rendszert. Ez azért fontos, mert érdemes elkerülni mind az alulméretezést, mind a túlméretezést: az egyik működési problémákhoz vezethet, a másik indokolatlanul növelheti a beruházási költséget.",
      multi: false,
      options: [
        { id: "1-2", label: "1–2 fő", chip: "1–2 fő" },
        { id: "3-4", label: "3–4 fő", chip: "3–4 fő" },
        { id: "5-6", label: "5–6 fő", chip: "5–6 fő" },
        { id: "7-10", label: "7–10 fő", chip: "7–10 fő" },
        { id: "10+", label: "10 fő felett", chip: "10 fő felett" },
        { id: "x", label: "Nem tudom pontosan", chip: "Kapacitás tisztázandó", unknown: true }
      ]
    },
    {
      id: "hasznalat", step: "Használati jelleg",
      q: "Milyen jellegű lesz a használat?",
      why: "Az állandó és az időszakos használat más terhelést jelent a rendszernek — ez befolyásolja, milyen technológia a legmegfelelőbb, és hogyan érdemes méretezni.",
      multi: false,
      options: [
        { id: "allando", label: "Állandó (állandó lakás)", chip: "Állandó használat" },
        { id: "idoszakos", label: "Időszakos (pl. hétvégi ház)", chip: "Időszakos használat" },
        { id: "szezonalis", label: "Szezonális (pl. nyaraló)", chip: "Szezonális használat" },
        { id: "x", label: "Nem tudom pontosan", chip: "Használat tisztázandó", unknown: true }
      ]
    },
    {
      id: "telek", step: "Telek adottságai",
      q: "Van olyan helyszíni adottság, ami nehezítheti a telepítést?",
      why: "Bizonyos adottságok — magas talajvíz, kevés hely, nehéz gépi hozzáférés — plusz munkát vagy kiegészítő megoldást igényelnek, ezért feljebb tolhatják a költséget. Ezért kérdezzük rá előre.",
      multi: true,
      options: [
        { id: "talajviz", label: "Magas talajvíz", chip: "Magas talajvíz" },
        { id: "keveshely", label: "Kevés hely / kis telek", chip: "Kevés hely" },
        { id: "lejtes", label: "Lejtős terep", chip: "Lejtős terep" },
        { id: "hozzaferes", label: "Nehéz gépi hozzáférés", chip: "Nehéz hozzáférés" },
        { id: "elovíz", label: "Közeli élővíz vagy kút", chip: "Közeli élővíz/kút" },
        { id: "nincs", label: "Nincs ilyen, tudtommal", chip: "Nincs nehezítő adottság", exclusive: true },
        { id: "x", label: "Nem tudom", chip: "Adottságok tisztázandó", unknown: true, exclusive: true }
      ]
    },
    {
      id: "elvezetes", step: "Elvezetés módja",
      q: "Hova kerülhet a megtisztított víz?",
      why: "A tisztított víz elhelyezése — elszikkasztás, gyökérzónás öntözés vagy élővízbe vezetés — a telek és az engedélyezési környezet függvénye, és hatással van a kivitelezésre.",
      multi: false,
      options: [
        { id: "szikkaszt", label: "Elszikkasztás a telken", chip: "Elszikkasztás" },
        { id: "gyoker", label: "Gyökérzónás öntözés", chip: "Gyökérzónás öntözés" },
        { id: "elovíz", label: "Élővízbe vezetés", chip: "Élővízbe vezetés" },
        { id: "x", label: "Nem tudom / most derül ki", chip: "Elvezetés tisztázandó", unknown: true }
      ]
    },
    {
      id: "meglevo", step: "Meglévő rendszer",
      q: "Van jelenleg valamilyen szennyvízkezelő megoldás a telken?",
      why: "Egy régi emésztő vagy akna kiváltása bontással és többletmunkával jár, ezért másképp alakul a költség, mint egy teljesen új telepítésnél.",
      multi: false,
      options: [
        { id: "uj", label: "Nincs, teljesen új telepítés", chip: "Új telepítés" },
        { id: "emeszto", label: "Régi emésztő / akna kiváltása", chip: "Emésztő kiváltása" },
        { id: "csere", label: "Meglévő rendszer cseréje / bővítése", chip: "Rendszercsere" },
        { id: "x", label: "Nem tudom pontosan", chip: "Meglévő rendszer tisztázandó", unknown: true }
      ]
    },
    {
      id: "fazis", step: "Konzultációs igény",
      q: "Mennyire aktuális most a döntés?",
      why: "Ez segít nekünk eldönteni, hogyan tudunk a leghasznosabbak lenni: tájékozódáshoz háttéranyaggal, konkrét projekthez helyszíni felméréssel.",
      multi: false,
      options: [
        { id: "tajekozodas", label: "Most tájékozódom", chip: "Tájékozódás" },
        { id: "felev", label: "Fél éven belül tervezem", chip: "Fél éven belül" },
        { id: "kesz", label: "Konkrét, kész projekt", chip: "Kész projekt" },
        { id: "x", label: "Nem tudom még", chip: "Ütemezés tisztázandó", unknown: true }
      ]
    }
  ],
  en: [
    {
      id: "kapacitas", step: "Capacity",
      q: "How many people will use the system regularly?",
      why: "The number of users determines the capacity the system has to be sized for. This matters because both under-sizing and over-sizing are worth avoiding: the first can lead to operating problems, the second raises the capital cost without reason.",
      multi: false,
      options: [
        { id: "1-2", label: "1–2 people", chip: "1–2 people" },
        { id: "3-4", label: "3–4 people", chip: "3–4 people" },
        { id: "5-6", label: "5–6 people", chip: "5–6 people" },
        { id: "7-10", label: "7–10 people", chip: "7–10 people" },
        { id: "10+", label: "More than 10", chip: "More than 10" },
        { id: "x", label: "I am not sure", chip: "Capacity to clarify", unknown: true }
      ]
    },
    {
      id: "hasznalat", step: "Pattern of use",
      q: "What kind of use will it be?",
      why: "Permanent and intermittent use place different loads on the system — that bears on which technology suits best, and on how it should be sized.",
      multi: false,
      options: [
        { id: "allando", label: "Permanent (a permanent home)", chip: "Permanent use" },
        { id: "idoszakos", label: "Intermittent (e.g. a weekend house)", chip: "Intermittent use" },
        { id: "szezonalis", label: "Seasonal (e.g. a holiday home)", chip: "Seasonal use" },
        { id: "x", label: "I am not sure", chip: "Use to clarify", unknown: true }
      ]
    },
    {
      id: "telek", step: "The plot",
      q: "Is there anything on site that could make installation harder?",
      why: "Certain conditions — high groundwater, little space, difficult machine access — call for extra work or an additional solution, and can therefore push the cost up. That is why we ask in advance.",
      multi: true,
      options: [
        { id: "talajviz", label: "High groundwater", chip: "High groundwater" },
        { id: "keveshely", label: "Little space / small plot", chip: "Little space" },
        { id: "lejtes", label: "Sloping ground", chip: "Sloping ground" },
        { id: "hozzaferes", label: "Difficult machine access", chip: "Difficult access" },
        { id: "elovíz", label: "A watercourse or well nearby", chip: "Watercourse/well nearby" },
        { id: "nincs", label: "None that I know of", chip: "No complicating conditions", exclusive: true },
        { id: "x", label: "I do not know", chip: "Conditions to clarify", unknown: true, exclusive: true }
      ]
    },
    {
      id: "elvezetes", step: "Means of disposal",
      q: "Where can the treated water go?",
      why: "Disposing of the treated water — infiltration, reed-bed irrigation or discharge to a watercourse — depends on the plot and on the permitting environment, and it affects the build.",
      multi: false,
      options: [
        { id: "szikkaszt", label: "Infiltration on the plot", chip: "Infiltration" },
        { id: "gyoker", label: "Reed-bed irrigation", chip: "Reed-bed irrigation" },
        { id: "elovíz", label: "Discharge to a watercourse", chip: "Discharge to watercourse" },
        { id: "x", label: "I do not know / still to be settled", chip: "Disposal to clarify", unknown: true }
      ]
    },
    {
      id: "meglevo", step: "Existing system",
      q: "Is there any wastewater solution on the plot at present?",
      why: "Replacing an old cesspit or chamber involves demolition and extra work, so the cost works out differently than for an entirely new installation.",
      multi: false,
      options: [
        { id: "uj", label: "No, an entirely new installation", chip: "New installation" },
        { id: "emeszto", label: "Replacing an old cesspit / chamber", chip: "Cesspit replacement" },
        { id: "csere", label: "Replacing / extending an existing system", chip: "System replacement" },
        { id: "x", label: "I am not sure", chip: "Existing system to clarify", unknown: true }
      ]
    },
    {
      id: "fazis", step: "Consultation need",
      q: "How immediate is the decision?",
      why: "This helps us decide how we can be most useful: background material if you are still looking into it, an on-site survey for a concrete project.",
      multi: false,
      options: [
        { id: "tajekozodas", label: "I am just looking into it", chip: "Looking into it" },
        { id: "felev", label: "Planned within six months", chip: "Within six months" },
        { id: "kesz", label: "A concrete, ready project", chip: "Ready project" },
        { id: "x", label: "I do not know yet", chip: "Timing to clarify", unknown: true }
      ]
    }
  ]
  };
  const QUESTIONS = KERDESEK[NYELV];

  /* ------------------------------------------------- ÁRSÁV LOGIKAI TÁBLA ----
     PLACEHOLDER értékek — éles indulás előtt Anna hagyja jóvá / állítja be.
     Élesben ez egy szerkeszthető konfig (admin/DB) legyen, ne kódban.
     base: kapacitás -> [alsó, felső] Ft.  modifiers: adottság/kiváltás -> +Ft.  */
  /* A konfigurációt külön, a cég által szerkeszthető fájl adja
     (`assets/data/aidt-konfig.js`). Ha az hiányzik, a lenti tartalék lép életbe. */
  const CFG = (typeof window !== "undefined" && window.OTH_AIDT) || {};
  const PRICE_TABLE = CFG.arsav || {
    base: {
      "1-2": [1600000, 2200000],
      "3-4": [1900000, 2600000],
      "5-6": [2400000, 3200000],
      "7-10": [3000000, 4200000],
      "10+": null,                 // egyedi méretezés (telep-kategória) — sávot nem adunk
      "x":   [1600000, 3200000]    // széles tartalék, ha a kapacitás ismeretlen
    },
    modifiers: {
      talajviz:   350000,
      keveshely:  250000,
      lejtes:     150000,
      hozzaferes: 300000,
      emeszto:    250000,          // kiváltás: bontás + többletmunka
      csere:      150000
    }
  };

  /* Sáv számítása a válaszokból. A modifierek a felső véget jobban emelik. */
  function computeBand(a) {
    const base = PRICE_TABLE.base[a.kapacitas];
    if (a.kapacitas === "10+") return { special: "telep" };
    if (!base) return null;
    let lo = base[0], hi = base[1], mod = 0;
    const add = (id) => { if (PRICE_TABLE.modifiers[id]) mod += PRICE_TABLE.modifiers[id]; };
    if (Array.isArray(a.telek)) a.telek.forEach(add);
    if (a.meglevo) add(a.meglevo);
    lo += Math.round(mod * 0.4);
    hi += mod;
    const round = (n) => Math.round(n / 100000) * 100000;
    return { lo: round(lo), hi: round(hi), mod };
  }

  const fmtM = (n) => (n / 1000000).toLocaleString("hu-HU", { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  function bandText(band) {
    if (!band) return "—";
    if (band.special) return T.egyediMeretezes;
    return `${fmtM(band.lo)}–${fmtM(band.hi)} ${T.milliFt}`;
  }

  /* -------------------------------------------------- SZÖVEG-GENERÁTOR ------
     Sablon-alapú (AI-stand-in). Éles: szigorúan promptolt AI-hívás ide köthető. */
  const NARRATION = {
    greeting: T.udvozles,
    ack: (qi, opt) => {
      const q = QUESTIONS[qi];
      return `${T.koszonom} ${q.why}`;
    }
  };

  /* Az eredmény személyre szabott „ármozgató tényezők" szövege. */
  function driversList(a) {
    const out = [];
    const capLabel = optChip(0, a.kapacitas);
    if (capLabel) out.push(T.dKapacitas(capLabel));
    const telek = Array.isArray(a.telek) ? a.telek : [];
    if (telek.includes("talajviz")) out.push(T.dTalajviz);
    if (telek.includes("keveshely")) out.push(T.dKevesHely);
    if (telek.includes("hozzaferes")) out.push(T.dHozzaferes);
    if (a.meglevo === "emeszto") out.push(T.dEmeszto);
    if (a.meglevo === "csere") out.push(T.dCsere);
    if (a.hasznalat === "idoszakos" || a.hasznalat === "szezonalis") out.push(T.dIdoszakos);
    return out.slice(0, 4);
  }

  /* A „tisztázandó pontok" a „nem tudom" válaszokból. */
  function clarifyList(a) {
    const out = [];
    QUESTIONS.forEach((q) => {
      const val = a[q.id];
      const isUnknown = q.multi
        ? Array.isArray(val) && val.includes("x")
        : val === "x";
      if (isUnknown) {
        const opt = q.options.find((o) => o.unknown);
        out.push(opt ? opt.chip : q.step);
      }
    });
    return out;
  }

  /* Konzultációra előkészítendők — a válaszokra kicsit szabva. */
  function prepList(a) {
    const out = [
      T.pTelek,
      T.pHasznalat
    ];
    const telek = Array.isArray(a.telek) ? a.telek : [];
    if (telek.includes("talajviz") || telek.includes("x")) out.push(T.pTalajviz);
    if (a.meglevo === "emeszto" || a.meglevo === "csere") out.push(T.pMeglevo);
    out.push(T.pElvezetes);
    return out;
  }

  /* ----------------------------------------------------------- SEGÉDLETEK */
  function optChip(qi, valId) {
    const o = QUESTIONS[qi].options.find((x) => x.id === valId);
    return o ? o.chip : null;
  }
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  function svg(paths, extra) {
    return `<svg viewBox="0 0 24 24" aria-hidden="true" ${extra || ""}>${paths}</svg>`;
  }
  /* Az asszisztens avatarja a MÁRKA JELRAJZÁT viseli, nem egy általános
     házikó-vonalrajzot: az utóbbi 1,8 képpontos vonalakból állt, és 24
     képpontra zsugorítva alig látszott. A jelrajzot CSS-maszkkal rajzoljuk
     (app.css `.aidt-jel`), mert tömör forma — kis méretben is olvasható —, és
     a színét a tokenkészlet adja. */
  const ICON = {
    check: '<path d="M20 6 9 17l-5-5"/>',
    info: '<circle cx="12" cy="12" r="9"/><path d="M12 16v-4M12 8h.01"/>',
    warn: '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4M12 17h.01"/>',
    mail: '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>',
    phone: '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
    multi: '<path d="M11 6h9M11 12h9M11 18h9"/><path d="m3 6 1.4 1.4L7 4.2"/><path d="m3 12 1.4 1.4L7 10.2"/><path d="m3 18 1.4 1.4L7 16.2"/>'
  };

  /* ------------------------------------------------------------- ÁLLAPOT */
  const state = {
    step: 0, answers: {}, draft: [],   // draft: multi-select ideiglenes
    atvett: new Set(),                 // a 6. szekcióból ÁTVETT kérdések azonosítói
    elojelolt: {},                     // részlegesen átvett multi-kérdések előjelölése
    ugy: null                          // a mentett ügy azonosítója, ha van
  };

  /* ==========================================================================
     ÁTVÉTEL A 6. SZEKCIÓBÓL (megoldás-ajánló)
     --------------------------------------------------------------------------
     A látogató két modulon megy végig, és a kettő részben UGYANAZT kérdezi.
     Kétszer megkérdezni ugyanazt nem csak kényelmetlen — azt is jelzi, hogy
     nem figyeltünk oda. Ezért amit a 6. szekció már megtudott, azt ide
     átvesszük, és a kérdést nem tesszük fel újra.

     KÉT SZINT, és a különbség fontos:
       · `zar: true`  — a 6. szekció válasza EGYÉRTELMŰEN megfelel az itteni
         kérdésnek, tehát kitöltöttnek jelöljük, és nem kérdezzük újra.
         (A látogató a helyzetkép-panelről bármikor átírhatja.)
       · `zar: false` — a 6. szekció csak RÉSZBEN válaszolta meg: itt csak
         előjelölünk, a kérdés aktív marad, és a látogató egészíti ki.

     A LÉTSZÁM SÁVJAI SZÁNDÉKOSAN AZONOSAK a két modulban. Enélkül nem volna
     átvihető: egy „2–3 fő" válasz sem az „1–2", sem a „3–4" sávba nem esne
     egyértelműen, tehát vagy újra kellene kérdezni, vagy tippelnénk. */
  const ATVETEL = [
    { ide: "kapacitas", zar: true, ebbol: (a) => a.letszam || null },
    { ide: "hasznalat", zar: true, ebbol: (a) => ({
        eletvitelszeru: "allando", hetvegi: "idoszakos", szezonalis: "szezonalis"
      })[a.hasznalat] || null },
    /* A telek-kérdés több adottságot sorol; a 6. szekció ezek közül kettőről
       tud. A többit (lejtés, gépi hozzáférés, közeli élővíz) itt kell
       megkérdezni, ezért a kérdés aktív marad. */
    { ide: "telek", zar: false, ebbol: (a) => {
        const ki = [];
        if (a.talajviz === "igen") { ki.push("talajviz"); }
        if (a.terulet === "kicsi") { ki.push("keveshely"); }
        return ki.length ? ki : null;
      } }
  ];

  /** Egy kérdés címkéje az átvételi visszajelzéshez. */
  const kerdesCimke = (id) => { const q = QUESTIONS.find((x) => x.id === id); return q ? q.step : id; };

  /**
   * A 6. szekció gépi válaszkulcsaiból kitölti, amit lehet.
   * @returns {string[]} a ténylegesen átvett kérdések címkéi
   */
  function atvesz(kulcsok) {
    if (!kulcsok) return [];
    const felvett = [];
    ATVETEL.forEach((m) => {
      const q = QUESTIONS.find((x) => x.id === m.ide);
      if (!q) return;
      const ertek = m.ebbol(kulcsok);
      if (ertek == null) return;
      const ervenyes = (v) => q.options.some((o) => o.id === v);
      if (q.multi) {
        const lista = (Array.isArray(ertek) ? ertek : [ertek]).filter(ervenyes);
        if (!lista.length) return;
        state.elojelolt[q.id] = lista;
        felvett.push(q.step);
      } else {
        if (!ervenyes(ertek)) return;
        state.answers[q.id] = ertek;
        state.atvett.add(q.id);
        felvett.push(q.step);
      }
    });

    /* CSAK ÖSSZEFÜGGŐ ELŐTAG vehető át. A beszélgetés-nézet a `step` előtti
       kérdéseket rajzolja megválaszoltként; egy „lyuk" (megválaszolt kérdés a
       még nem elért kérdések között) itt hibás állapot volna. Ami kilóg, azt
       inkább újra megkérdezzük. */
    let i = 0;
    while (i < QUESTIONS.length && state.atvett.has(QUESTIONS[i].id)) i++;
    QUESTIONS.slice(i).forEach((q) => {
      if (state.atvett.has(q.id)) { state.atvett.delete(q.id); delete state.answers[q.id]; }
    });
    state.step = i;
    const q = QUESTIONS[i];
    state.draft = (q && q.multi && state.elojelolt[q.id]) ? state.elojelolt[q.id].slice() : [];
    return felvett;
  }

  /* --------------------------------------------------------------- RENDER */
  let root, chatEl, panelEl, bodyEl;

  function render() {
    if (state.step >= QUESTIONS.length) { renderResult(); return; }
    renderChat();
    renderPanel();
  }

  function renderChat() {
    const parts = [];
    parts.push(bubble("bot", `<p>${esc(NARRATION.greeting)}</p>`, "10:30"));

    for (let i = 0; i < state.step; i++) {
      parts.push(questionBubble(i, false));   // válaszolt kérdés: opciók láthatók, a választott kiemelve
      if (i === state.step - 1 && state.typing) parts.push(typingRow());   // az utolsó válasz után a rendszer „gépel"
      else parts.push(bubble("bot ack", ackHtml(i), null));
    }
    if (!state.typing && state.step < QUESTIONS.length) {
      parts.push(questionBubble(state.step, true));
    }
    chatEl.innerHTML = parts.join("");
    if (state._animate) {                        // belépő animáció csak az új aktív kérdésre
      const aq = chatEl.querySelector(".is-active-q");
      if (aq) aq.classList.add("aidt-in");
      state._animate = false;
    }
    wireOptions();
    updateRail();
    if (state.step > 0) chatEl.scrollTop = chatEl.scrollHeight;
  }

  function typingRow() {
    return `<div class="aidt-row is-bot no-av"><div class="aidt-bubble bot aidt-typing"><span></span><span></span><span></span></div></div>`;
  }
  function updateRail() {
    const fill = bodyEl.querySelector(".aidt-rail-fill");
    if (fill) fill.style.height = Math.min(100, (state.step / QUESTIONS.length) * 100) + "%";
  }

  /* üdvözlő / nyugtázó buborék — a mockup szerint avatar NÉLKÜL, behúzva igazítva */
  function bubble(cls, inner, time) {
    const bot = cls.includes("bot");
    return `<div class="aidt-row ${bot ? "is-bot no-av" : "is-user"}">
      <div class="aidt-bubble ${cls}">${inner}${time ? `<span class="aidt-time">${time}</span>` : ""}</div>
    </div>`;
  }

  function questionBubble(qi, active) {
    const q = QUESTIONS[qi];
    const val = state.answers[q.id];
    const selected = active
      ? (q.multi ? state.draft : [])
      : (q.multi ? (Array.isArray(val) ? val : []) : (val != null ? [val] : []));
    let opts = `<div class="aidt-opts${q.multi ? " is-multi" : ""}" role="group" aria-label="${esc(q.q)}">`;
    q.options.forEach((o) => {
      const sel = selected.includes(o.id);
      const dis = active ? "" : " disabled";
      const unk = o.unknown ? ' data-unknown="1"' : "";
      if (q.multi) {   // checkbox-stílus: a négyzet jelzi, hogy több is választható
        opts += `<button type="button" class="aidt-opt aidt-opt--cb${sel ? " is-sel" : ""}" data-opt="${o.id}"${unk}${dis} aria-pressed="${sel}">
          <span class="aidt-cbx">${svg(ICON.check)}</span><span>${esc(o.label)}</span></button>`;
      } else {
        opts += `<button type="button" class="aidt-opt${sel ? " is-sel" : ""}" data-opt="${o.id}"${unk}${dis}>
          <span>${esc(o.label)}</span>${sel ? `<span class="aidt-opt-ck">${svg(ICON.check)}</span>` : ""}</button>`;
      }
    });
    opts += `</div>`;
    if (active && q.multi) {
      opts += `<div class="aidt-multi-foot">
        <button type="button" class="aidt-next" data-next="1"${state.draft.length ? "" : " disabled"}>${T.tovabb} <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></button>
        <span class="aidt-multi-hint">${state.draft.length ? esc(state.draft.length + " " + T.kivalasztva) : T.valasszonTobbet}</span>
      </div>`;
    }
    /* Az ÁTVETT kérdés nem „megválaszolt" a szokásos értelemben: a látogató itt
       nem kattintott. Ezt ki kell írni, különben úgy tűnne, mintha ő adta
       volna meg — és nem tudná, miért nem kérdeztük meg. */
    const atvettJel = (!active && state.atvett.has(q.id))
      ? ` <span class="aidt-atvett-badge">${svg(ICON.check)}${T.ajanlobol}</span>` : "";
    return `<div class="aidt-row is-bot${active ? " is-active-q" : ""}${!active && state.atvett.has(q.id) ? " is-atvett" : ""}">
      <span class="aidt-av-sm"><span class="aidt-jel" aria-hidden="true"></span></span>
      <div class="aidt-bubble bot aidt-qwrap">
        <p class="aidt-q">${esc(q.q)}${q.multi ? ` <span class="aidt-multi-badge">${svg(ICON.multi)}${T.tobbValaszthato}</span>` : ""}${atvettJel}</p>
        ${opts}
      </div>
    </div>`;
  }

  function ackHtml(qi) {
    return `<p>${esc(NARRATION.ack(qi))}</p>
      <span class="aidt-why">${svg(ICON.info)} ${T.miertSzamit}</span>`;
  }

  /* jobb panel — haladás + helyzetkép + ársáv-teaser */
  function renderPanel() {
    const answered = state.step;
    const remaining = QUESTIONS.length - answered;
    let steps = "";
    QUESTIONS.forEach((q, i) => {
      const done = i < state.step;
      const active = i === state.step;
      const val = state.answers[q.id];
      let valHtml = `<span class="aidt-sv open">${T.megNyitott}</span>`;
      if (done) {
        if (q.multi) {
          const ids = Array.isArray(val) ? val : [];
          const first = ids.length ? optChipById(q, ids[0]) : "—";
          const extra = ids.length > 1 ? ` +${ids.length - 1}` : "";
          valHtml = `<span class="aidt-sv chip">${esc(first)}${extra}</span>`;
        } else {
          valHtml = `<span class="aidt-sv chip">${esc(optChipById(q, val) || "—")}</span>`;
        }
      }
      const atv = state.atvett.has(q.id);
      steps += `<button type="button" class="aidt-step${done ? " is-done" : ""}${active ? " is-active" : ""}${atv ? " is-atvett" : ""}"${done || active ? ` data-edit="${i}"` : " disabled"}>
        <span class="aidt-step-n">${done ? svg(ICON.check) : String(i + 1).padStart(2, "0")}</span>
        <span class="aidt-step-label">${esc(q.step)}${atv ? ` <span class="aidt-step-atvett">${T.atveve}</span>` : ""}</span>
        ${valHtml}
      </button>`;
    });

    const dots = QUESTIONS.map((_, i) => `<span class="aidt-dot${i < state.step ? " on" : ""}"></span>`).join("");

    panelEl.innerHTML = `
      <div class="aidt-time-pill">${svg(ICON.info)} ${T.otPerc}</div>
      <h3 class="aidt-panel-h">${T.helyzetkep}</h3>
      <p class="aidt-panel-sub">${answered} / ${QUESTIONS.length} ${T.valaszMegadva}</p>
      <div class="aidt-steps">${steps}</div>
      <div class="aidt-band-box">
        <h4>${T.elozetesArsav}</h4>
        <p class="aidt-band-sub">${remaining > 0 ? T.megKell(remaining) : T.keszNezze}</p>
        <div class="aidt-band-row"><div class="aidt-dots">${dots}</div><span class="aidt-band-val">--- Ft</span></div>
        <p class="aidt-band-note">${T.pontosodik}</p>
      </div>
      <div class="aidt-warn">${svg(ICON.warn)}<p>${T.fontosTajekoztato}</p></div>`;
    wirePanel();
    syncMobile();
  }
  function optChipById(q, id) { const o = q.options.find((x) => x.id === id); return o ? o.chip : null; }

  /* ----------------------------------------------------------- EREDMÉNY */
  function renderResult() {
    const a = state.answers;
    const band = computeBand(a);
    const drivers = driversList(a);
    const clarify = clarifyList(a);
    const prep = prepList(a);

    let bandBlock;
    if (band && band.special) {
      bandBlock = `<div class="aidt-res-band special">
        <span class="aidt-res-tag">${T.tajBecsles}</span>
        <strong>${T.egyediMeretezes}</strong>
        <p>${T.egyediSzoveg}</p>
      </div>`;
    } else {
      bandBlock = `<div class="aidt-res-band">
        <span class="aidt-res-tag">${T.tajSav}</span>
        <strong>${bandText(band)}</strong>
        <p>${T.savSzoveg}</p>
      </div>`;
    }

    bodyEl.innerHTML = `
      <div class="aidt-result">
        <div class="aidt-res-head">
          <span class="aidt-av-lg"><span class="aidt-jel" aria-hidden="true"></span></span>
          <div>
            <p class="aidt-eyebrow small">${T.osszefoglaloEyebrow}</p>
            <h3>${T.osszefoglaloCim}</h3>
          </div>
        </div>

        ${bandBlock}

        <div class="aidt-res-cols">
          <section class="aidt-res-card">
            <h4>${T.mozgatjak}</h4>
            <ul class="aidt-drivers">${drivers.map((d) => `<li>${d}</li>`).join("")}</ul>
          </section>
          <section class="aidt-res-card">
            <h4>${clarify.length ? T.erdemesTisztazni : T.nincsNyitott}</h4>
            ${clarify.length
              ? `<ul class="aidt-clarify">${clarify.map((c) => `<li>${esc(c)}</li>`).join("")}</ul>`
              : `<p class="aidt-muted">${T.mindenMegadva}</p>`}
          </section>
        </div>

        <section class="aidt-res-card">
          <h4>${T.elokesziteni}</h4>
          <ul class="aidt-prep">${prep.map((p) => `<li>${svg(ICON.check)} ${esc(p)}</li>`).join("")}</ul>
        </section>

        <div class="aidt-res-actions">
          <div class="aidt-act">
            <span class="aidt-act-ico">${svg(ICON.mail)}</span>
            <div class="aidt-act-body">
              <h5>${T.elkuldomMagamnak}</h5>
              <p>${T.egyszeriEmail}</p>
              <form class="aidt-mailform" novalidate>
                <input type="email" name="email" inputmode="email" autocomplete="email" placeholder="az.on.email@pelda.hu" aria-label="${T.emailCim}" required />
                <button type="submit" class="btn btn-primary">${T.elkuldom}</button>
              </form>
              <label class="aidt-consent"><input type="checkbox" name="callback" /> <span>${T.keressenMeg}</span></label>
              <p class="aidt-privacy">${T.adatFelhasznalas} <a href="${esc(CFG.adatkezelesUrl || "adatkezelesi-tajekoztato")}">${T.adatkezeles}</a>.</p>
            </div>
          </div>
          <div class="aidt-act-cta">
            <a href="ajanlatkeres" class="btn btn-primary">${T.konzultaciotKerek} <svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>
            <button type="button" class="btn btn-secondary" data-restart="1">${T.ujrakezdem}</button>
          </div>
        </div>

        <p class="aidt-res-foot">${svg(ICON.warn)} ${T.jogiKitetel}</p>
      </div>`;

    // jobb panel „kész" állapot
    renderPanel();
    wireResult();

    /* A mentés blokkja a záró megjegyzés ELÉ kerül: az utolsó szó a
       „tájékoztató jellegű" figyelmeztetésé maradjon. */
    const foot = bodyEl.querySelector(".aidt-res-foot");
    if (foot && window.OthUgy) foot.parentNode.insertBefore(mentesBlokk(), foot);
  }

  /* --------------------------------------------------------------- EVENTEK */
  function wireOptions() {
    const scope = chatEl.querySelector(".is-active-q");
    if (!scope) return;
    scope.querySelectorAll(".aidt-opt").forEach((btn) => {
      btn.addEventListener("click", () => {
        const q = QUESTIONS[state.step];
        const id = btn.getAttribute("data-opt");
        if (q.multi) {
          const opt = q.options.find((o) => o.id === id);
          if (opt.exclusive) { state.draft = [id]; }
          else {
            state.draft = state.draft.filter((x) => { const o = q.options.find((y) => y.id === x); return o && !o.exclusive; });
            const at = state.draft.indexOf(id);
            if (at >= 0) state.draft.splice(at, 1); else state.draft.push(id);
          }
          renderChat();
        } else {
          commitAnswer(q, id);
        }
      });
    });
    const nextBtn = scope.querySelector(".aidt-next");
    if (nextBtn) nextBtn.addEventListener("click", () => {
      if (!state.draft.length) return;
      commitAnswer(QUESTIONS[state.step], state.draft.slice());
    });
  }
  function wirePanel() {
    panelEl.querySelectorAll(".aidt-step[data-edit]").forEach((b) => {
      b.addEventListener("click", () => jumpTo(parseInt(b.getAttribute("data-edit"), 10)));
    });
  }
  function wireResult() {
    bodyEl.querySelectorAll("[data-edit]").forEach((b) => b.addEventListener("click", () => jumpTo(parseInt(b.getAttribute("data-edit"), 10))));
    const restart = bodyEl.querySelector("[data-restart]");
    if (restart) restart.addEventListener("click", () => {
      state.step = 0; state.answers = {}; state.draft = [];
      state.atvett = new Set(); state.elojelolt = {};
      rebuildBody();
      if (typeof atvetelSavFrissit === "function") atvetelSavFrissit();
    });
    const form = bodyEl.querySelector(".aidt-mailform");
    if (form) form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = form.email.value.trim();
      const ok = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email);
      form.email.setAttribute("aria-invalid", ok ? "false" : "true");
      if (!ok) { form.email.focus(); form.email.classList.add("err"); return; }
      form.email.classList.remove("err");
      const callback = bodyEl.querySelector('input[name="callback"]').checked;
      const body = form.closest(".aidt-act-body");

      /*
       * AZ ÜGYAZONOSÍTÓ ELŐBB, MINT A LEVÉL.
       *
       * A két küldés eddig egymástól függetlenül futott: a levélben ott volt az
       * e-mail-cím ügyazonosító nélkül, a mentett ügyben ott volt az azonosító
       * e-mail-cím nélkül. A kettő SOHA nem találkozott — a CRM-ben így egy
       * névtelen kitöltés és egy gazdátlan e-mail-cím keletkezett, és az
       * értékesítő nem tudta meg, hogy ugyanarról az emberről van szó.
       *
       * Ezért ha a látogató még nem mentett, MOST mentünk: az ügy tartalma
       * ugyanaz, amit a levél is visz, tehát semmi újat nem tárolunk — csak
       * megszületik a kód, ami a kettőt összeköti. A CRM ebből visszamenőleg
       * az érdeklődőhöz csatolja a korábbi névtelen válaszokat.
       *
       * A MENTÉS BUKÁSA NEM ÁLLÍTHATJA MEG A LEVELET. Az azonosító hasznos,
       * de a levél a fontosabb: azt a látogató kérte.
       */
      let ugyAzonosito = "";

      try {
        const allapot = window.OthUgy && window.OthUgy.allapot ? window.OthUgy.allapot() : null;
        ugyAzonosito = (allapot && allapot.azonosito) || "";

        if (!ugyAzonosito && window.OthUgy) {
          const mentes = await window.OthUgy.ment("arsav", mentendo());
          if (mentes && mentes.ok) ugyAzonosito = mentes.azonosito || "";
        }
      } catch (hiba) {
        /* Szándékosan némán: lásd fent. */
      }

      /* A strukturált profil: ugyanaz megy a backendnek, amit a látogató lát. */
      const payload = {
        email: email,
        visszahivas: callback,
        valaszok: state.answers,
        arsav: computeBand(state.answers),
        ugy_azonosito: ugyAzonosito,
        idobelyeg: new Date().toISOString()
      };

      /* Végpont nélkül NEM állítjuk, hogy elküldtük — ez félrevezetés lenne. */
      if (!CFG.endpoint) {
        body.innerHTML =
          `<div class="aidt-sent">${svg(ICON.warn)}<div><h5>${T.nincsElesitve}</h5>
          <p>${T.nincsElesitveSzoveg} <a href="tel:+3633200211">+36 33 200 211</a>.</p></div></div>`;
        return;
      }

      const btn = form.querySelector("button");
      btn.disabled = true; btn.setAttribute("aria-busy", "true");
      try {
        const res = await fetch(CFG.endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error(String(res.status));
        body.innerHTML =
          `<div class="aidt-sent">${svg(ICON.check)}<div><h5>${T.elkuldtuk}</h5>
          <p>${esc(email)} — ${T.nezzeMeg}${callback ? " " + T.hamarosanJelentkezik : ""}</p></div></div>`;
      } catch (err) {
        btn.disabled = false; btn.removeAttribute("aria-busy");
        let note = body.querySelector(".aidt-senderr");
        if (!note) {
          note = document.createElement("p");
          note.className = "aidt-senderr";
          note.setAttribute("role", "alert");
          form.after(note);
        }
        note.textContent = T.kuldesNemSikerult;
      }
    });
  }

  function commitAnswer(q, value) {
    state.answers[q.id] = value;
    state.step += 1;
    state.draft = [];
    if (state.step >= QUESTIONS.length) { rebuildBody(); return; }
    state.typing = true;
    render();                                  // a sín előre lép + „gépel" jelző látszik
    clearTimeout(state._tt);
    state._tt = setTimeout(() => { state.typing = false; state._animate = true; render(); }, 650);
  }
  function jumpTo(i) {
    if (i < 0 || i >= QUESTIONS.length) return;
    clearTimeout(state._tt);
    state.typing = false;
    // az i. kérdéstől újra — a későbbi válaszokat töröljük (előre újra kérdezünk)
    for (let k = i; k < QUESTIONS.length; k++) {
      delete state.answers[QUESTIONS[k].id];
      /* Ha a látogató átírja, az már NEM átvett válasz: a jelölés is elmegy. */
      state.atvett.delete(QUESTIONS[k].id);
    }
    state.step = i;
    const q = QUESTIONS[i];
    state.draft = (q.multi && Array.isArray(state.answers[q.id])) ? state.answers[q.id].slice() : [];
    rebuildBody();
  }

  /* Body váltás: kérdés-nézet <-> eredmény-nézet (a .aidt-body szerkezete változik) */
  function rebuildBody() {
    if (state.step >= QUESTIONS.length) {
      bodyEl.classList.add("is-result");
      renderResult();
    } else {
      bodyEl.classList.remove("is-result");
      bodyEl.innerHTML = `
        <div class="aidt-chat">
          <span class="aidt-rail" aria-hidden="true"><span class="aidt-rail-fill"></span></span>
          <div class="aidt-chat-head">
            <span class="aidt-av"><span class="aidt-jel" aria-hidden="true"></span></span>
            <div class="aidt-chat-id"><b>${T.asszisztens}</b><span>${T.fejAlcim}</span></div>
            <span class="aidt-count"><b>${Math.min(state.step + 1, QUESTIONS.length)}</b> / ${QUESTIONS.length}</span>
          </div>
          <div class="aidt-msgs"></div>
        </div>
        <aside class="aidt-panel-wrap">
          <button type="button" class="aidt-mtoggle" aria-expanded="false">${T.helyzetkepRovid} <b><span class="aidt-mstep">${state.step}</span>/${QUESTIONS.length}</b><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button>
          <div class="aidt-panel"></div>
        </aside>`;
      chatEl = bodyEl.querySelector(".aidt-msgs");
      panelEl = bodyEl.querySelector(".aidt-panel");
      wireMobileToggle();
      state._animate = true;
      render();
    }
  }

  /* mobil: helyzetkép összecsukható sáv */
  function wireMobileToggle() {
    const t = bodyEl.querySelector(".aidt-mtoggle");
    if (t) t.addEventListener("click", () => {
      const open = bodyEl.classList.toggle("panel-open");
      t.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }
  function syncMobile() {
    const ms = bodyEl.querySelector(".aidt-mstep");
    if (ms) ms.textContent = String(state.step);
    const c = bodyEl.querySelector(".aidt-count b");
    if (c) c.textContent = String(Math.min(state.step + 1, QUESTIONS.length));
  }

  /* ==========================================================================
     ÁTVÉTELI SÁV — a modul FÖLÖTT
     --------------------------------------------------------------------------
     Három állapota van, és mindig azt mutatja, ami épp igaz:
       · van a munkamenetben 6. szekciós adat  → felajánljuk az átvételt,
       · nincs, de lehet mentett azonosító     → beírható mező,
       · megtörtént az átvétel                 → megmondjuk, MIT vettünk át.
     A sáv sosem tölt be magától: az átvétel a látogató döntése. */
  let savEl = null;

  function atvetelSavFrissit() {
    if (!savEl) return;
    const ugy = window.OthUgy || null;
    const kulcsok = ugy ? ugy.valaszkulcsok("ajanlo") : null;
    const allapot = ugy ? ugy.allapot() : null;
    const azon = allapot && allapot.azonosito ? allapot.azonosito : "";

    if (state.atvett.size || Object.keys(state.elojelolt).length) {
      const cimkek = [];
      state.atvett.forEach((id) => cimkek.push(kerdesCimke(id)));
      Object.keys(state.elojelolt).forEach((id) => cimkek.push(kerdesCimke(id) + " " + T.reszben));
      savEl.className = "aidt-atvetel is-kesz";
      savEl.innerHTML = `${svg(ICON.check)}
        <div><p><b>${T.atvettuk}</b> ${esc(cimkek.join(", "))}.
        ${azon ? T.ugyazonosito + " <b>" + esc(azon) + "</b>." : ""}</p>
        <p class="aidt-atvetel-sub">${T.atirhatja}</p></div>
        <button type="button" class="btn btn-halvany" data-atv-vissza>${T.megsem}</button>`;
      savEl.hidden = false;
    } else if (kulcsok) {
      savEl.className = "aidt-atvetel";
      savEl.innerHTML = `${svg(ICON.info)}
        <div><p><b>${T.atTudjukVenni}</b>
        ${azon ? T.ugyazonosito + " <b>" + esc(azon) + "</b>." : ""}</p>
        <p class="aidt-atvetel-sub">${T.nemKerdezzukUjra}</p></div>
        <button type="button" class="btn btn-primary" data-atv-betolt>${T.adatAtvetel}</button>`;
      savEl.hidden = false;
    } else {
      savEl.className = "aidt-atvetel is-kereso";
      savEl.innerHTML = `${svg(ICON.info)}
        <div><p><b>${T.vanMentett}</b></p>
        <p class="aidt-atvetel-sub">${T.irjaBe}</p></div>
        <form class="aidt-atvetel-form" novalidate>
          <input class="urlap-input aidt-azon-mezo" type="text" name="id" inputmode="text"
                 autocomplete="off" spellcheck="false" placeholder="MA-XXXX-XXXX"
                 maxlength="12" aria-label="${T.ugyazonosito}" />
          <button type="submit" class="btn btn-halvany">${T.betoltes}</button>
        </form>
        <p class="aidt-atvetel-hiba" role="alert" hidden></p>`;
      savEl.hidden = false;
    }
    savWire();
  }

  function savWire() {
    const be = savEl.querySelector("[data-atv-betolt]");
    if (be) be.addEventListener("click", () => {
      const felvett = atvesz(window.OthUgy.valaszkulcsok("ajanlo"));
      if (!felvett.length) { atvetelSavHiba(T.nincsMitAtvenni); return; }
      rebuildBody();
      atvetelSavFrissit();
    });

    const vissza = savEl.querySelector("[data-atv-vissza]");
    if (vissza) vissza.addEventListener("click", () => {
      state.step = 0; state.answers = {}; state.draft = [];
      state.atvett = new Set(); state.elojelolt = {};
      rebuildBody();
      atvetelSavFrissit();
    });

    const form = savEl.querySelector(".aidt-atvetel-form");
    if (form) form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const mezo = form.querySelector("input");
      const btn = form.querySelector("button");
      const id = (mezo.value || "").trim().toUpperCase();
      if (!window.OthUgy || !window.OthUgy.ALAK.test(id)) {
        mezo.setAttribute("aria-invalid", "true");
        atvetelSavHiba("A helyes alak: MA-XXXX-XXXX.");
        return;
      }
      mezo.removeAttribute("aria-invalid");
      btn.disabled = true; btn.setAttribute("aria-busy", "true");
      const valasz = await window.OthUgy.olvas(id);
      btn.disabled = false; btn.removeAttribute("aria-busy");
      if (!valasz.ok) { atvetelSavHiba(valasz.uzenet || T.nincsIlyenAzon); return; }
      const felvett = atvesz(window.OthUgy.valaszkulcsok("ajanlo"));
      if (!felvett.length) { atvetelSavHiba(T.nincsHasznalhato); return; }
      rebuildBody();
      atvetelSavFrissit();
    });
  }

  function atvetelSavHiba(szoveg) {
    const h = savEl.querySelector(".aidt-atvetel-hiba");
    if (h) { h.textContent = szoveg; h.hidden = false; }
  }

  /* ==========================================================================
     MENTÉS — UGYANABBA az ügybe, amit a 6. szekció nyitott
     --------------------------------------------------------------------------
     Nem új azonosítót ad: ha a munkamenetben már van ügy, azt egészíti ki.
     Így a `/eredmeny?id=…` lapon a két modul kimenete együtt látszik, és a
     CRM egyetlen rekordból látja a teljes utat. */
  function mentendo() {
    const a = state.answers;
    const band = computeBand(a);
    const cimkek = QUESTIONS.map((q) => {
      const val = a[q.id];
      if (val == null) return null;
      const ids = Array.isArray(val) ? val : [val];
      const sz = ids.map((id) => optChipById(q, id)).filter(Boolean).join(", ");
      return sz ? { cimke: q.q, szoveg: sz } : null;
    }).filter(Boolean);

    const tisztit = (h) => String(h).replace(/<[^>]*>/g, "");

    return {
      verzio: CFG.verzio || "",
      valaszKulcsok: Object.assign({}, a),
      valaszok: cimkek,
      eredmeny: {
        irany: "arsav",
        cim: T.arsavTermek,
        termekNev: bandText(band),
        indoklas: T.arsavIndoklas
                + "Nem árajánlat: a pontos árat helyszíni felmérés után adjuk meg.",
        okok: clarifyList(a).map((c) => ({ cimke: c })),
        feltetelek: driversList(a).map((d) => ({ cimke: tisztit(d) })),
        tisztazandok: prepList(a).map((t) => ({ cimke: t }))
      }
    };
  }

  function mentesBlokk() {
    const doboz = document.createElement("div");
    doboz.className = "aidt-mentes";
    doboz.dataset.okoPont = "mentes";
    /* Ha a megoldás-ajánló is lefutott, de a látogató ott nem mentett, az a
       kimenet is felkerül ugyanabba az ügybe. Ezt KIMONDJUK: nem érheti
       meglepetés, hogy mit mentett el. */
    const fuggo = window.OthUgy.fuggoModulok("arsav").indexOf("ajanlo") >= 0;
    doboz.innerHTML = `${svg(ICON.info)}
      <div><p><b>${T.mentsEl}</b></p>
      <p class="aidt-mentes-sub">${T.mentesLeiras}${fuggo ? " " + T.ajanloIsIde : ""}</p></div>
      <button type="button" class="btn btn-halvany" data-aidt-ment>${T.eredmenyMentese}</button>`;
    const gomb = doboz.querySelector("[data-aidt-ment]");
    gomb.addEventListener("click", async () => {
      if (!window.OthUgy) return;
      gomb.disabled = true; gomb.setAttribute("aria-busy", "true");
      const valasz = await window.OthUgy.ment("arsav", mentendo());
      gomb.disabled = false; gomb.removeAttribute("aria-busy");
      if (valasz.ok) {
        const cim = window.OthUgy.eredmenyUrl(valasz.azonosito);
        doboz.className = "aidt-mentes is-kesz";
        doboz.innerHTML = `${svg(ICON.check)}
          <div><p><b>${T.elmentettuk}</b></p>
          <p class="aidt-mentes-azon">${esc(valasz.azonosito)}</p>
          <p class="aidt-mentes-sub">${T.mikodEz}</p>
          <p><a class="aidt-mentes-link" href="${esc(window.OthUgy.eredmenyHref(valasz.azonosito))}">${T.megnyitas}</a></p>
          <p class="aidt-mentes-cim">${esc(cim)}</p></div>`;
      } else {
        doboz.className = "aidt-mentes is-hiba";
        doboz.innerHTML = `${svg(ICON.warn)}
          <div><p><b>${T.nemSikerultMenteni}</b></p>
          <p class="aidt-mentes-sub">${esc(valasz.uzenet || T.probaljaUjra)}</p></div>`;
      }
    });
    return doboz;
  }

  /* ------------------------------------------------------------- INDÍTÁS */
  function init() {
    root = document.getElementById("aidt-root");
    if (!root) return;
    savEl = document.createElement("div");
    savEl.hidden = true;
    /* Öko itt magától megszólal, amikor a látogató idegörget: egy azonosító-
       mező a semmiből úgy néz ki, mint egy regisztráció. Lásd kalauz.js PONTOK. */
    savEl.dataset.okoPont = "ugyazonosito";
    root.appendChild(savEl);
    bodyEl = document.createElement("div");
    bodyEl.className = "aidt-body";
    root.appendChild(bodyEl);
    rebuildBody();
    atvetelSavFrissit();
    /* A 6. szekció ugyanezen a lapon él, a modul FÖLÖTT: amikor ott végez a
       látogató, a sáv magától átvált a felajánlásra — nem kell frissítenie. */
    window.addEventListener("oth-ugy-valtozott", () => {
      if (!state.atvett.size && !Object.keys(state.elojelolt).length && state.step === 0) atvetelSavFrissit();
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
