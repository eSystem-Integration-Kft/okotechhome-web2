/* =============================================================================
   ÖkoTech Home — AI megoldás-ajánló (6. szekció) · KONFIGURÁCIÓ
   -----------------------------------------------------------------------------
   Forrás: `OkoTech-Home_AI-modul_fejlesztoi_specifikacio.2.docx` (2026-08-24).

   EZT A FÁJLT A CÉG SZERKESZTHETI, fejlesztő nélkül: a kérdések, a válaszok, a
   döntési szabályok és a kimeneti szövegek mind itt élnek. A modul logikája
   (`assets/js/ajanlo.js`) egyetlen szakmai állítást sem tartalmaz.

   Módosítás után elég a fájlt feltölteni és a hivatkozás verzióját emelni
   (`index.html`: `ajanlo-konfig.js?v=NN`).

   ⚠️ JÓVÁHAGYÁSRA VÁR (a specifikáció 8. pontja):
     · a három használati kategória definíciója és a hozzájuk rendelt termékek,
     · a határesetek listájának teljessége,
     · az az elv, hogy a modul MEGNEVEZI a terméket, ahol egyértelmű,
     · a szabad terület sávhatárai (`teruletSavok`) — ezek jelenleg
       MUNKAHIPOTÉZISEK, nem méretezési adatok.
   ============================================================================= */
window.OTH_AJANLO = {

  /* A DÖNTÉSI LOGIKA VERZIÓJA. A mentett eredmény mellé is elmegy, hogy egy
     későbbi visszakeresésnél tudni lehessen, milyen szabályok szerint készült.
     Emeld, valahányszor a kérdéseken, a szabályokon vagy a sávhatárokon
     változtatsz. */
  verzio: "2026-08-28",

  /* ---------------------------------------------------------- MENTÉS ------
     A záró képernyőn a látogató elmentheti az eredményt. A mentés AZONOSÍTÓT
     kap, és a szerveren is eltároljuk, hogy visszakereshető és továbbvihető
     legyen. A rekordban NINCS személyes adat: csak a válaszok és a belőlük
     számított kimenet.

     Az azonosító alá a 8. szekció (ársávbecslő) kimenete is bekerül — EGY ügy,
     két modul. A végpontok az `assets/js/ugy.js`-ben élnek, mert ugyanazt
     három hívó használja (a két modul és az `/eredmeny` lap).

     ⚠️ A `megorzesSzoveg`-nek egyeznie kell az adatkezelési tájékoztatóval és
     az `api/config.php` `eredmeny.megorzes_nap` értékével.
     Ha a végpont nem elérhető (nincs `config.php`, ki van kapcsolva, hálózati
     hiba), a modul NEM hallgat: szövegfájlként felkínálja a letöltést, és
     kimondja, hogy szerverre most nem került. */
  mentes: {
    /* MIÉRT ÉRDEMES ELMENTENI — a mentés gombja fölött, MÉG a kattintás előtt.
       A látogató enélkül nem tudja, mit nyer vele: azt hiheti, adatot kérünk
       tőle, pedig épp az ellenkezője történik. */
    bevezeto: "Mentés után kap egy azonosítót. Ez nem regisztráció: nevet, "
            + "e-mail-címet vagy telefonszámot nem kérünk hozzá, és nem is tudjuk, ki Ön. "
            + "Egyetlen dolgot csinál: megjegyzi, mit adott már meg. Ezzel bármikor "
            + "előveheti ezt az eredményt, kinyomtathatja vagy PDF-be mentheti, a további "
            + "eszközeink (például a lap alatti ársávbecslő) pedig nem kérdezik újra "
            + "ugyanazt. Ha nem menti el, semmi nem marad meg nálunk — a válaszai a "
            + "böngészőjében maradnak.",
    /* Rövid, ismétlődő magyarázat mindenhol, ahol az azonosító MEGJELENIK. */
    azonositoMagyarazat: "Mi ez? Egy kód, ami a válaszait köti össze — személyes adat nélkül. "
                       + "Nem regisztráció, és nem kell megjegyeznie: a lapot elmentheti könyvjelzőbe is.",
    megorzesSzoveg: "A mentett eredményt azonosítóval, személyes adat nélkül tároljuk, 180 napig."
  },

  /* ------------------------------------------------------------- SZAKASZOK */
  /* A jobb oldali állapotpanel és a bal oldali sín ezekből épül. Az utolsó
     szakasz nem kérdés, hanem a kimenet. */
  /* `uzenet`: az asszisztens szövege a szakasz elején. A `{irany}` helyére a
     addigi termékirány neve kerül. `uzenetVegyes`: ugyanez arra az esetre,
     amikor a használati szakasz határesetet adott, tehát nincs mit megnevezni. */
  lepesek: [
    { id: "hasznalat", cim: "Használati jelleg",
      uzenet: "Kezdjük a használattal: ez dönti el, melyik technológia jöhet szóba egyáltalán. Három rövid kérdés lesz." },
    { id: "letszam", cim: "Létszám / terhelés",
      uzenet: "Köszönöm. Most az következik, mekkora terhelés jut a rendszerre." },
    { id: "kihagyas", cim: "Kihagyások gyakorisága",
      uzenet: "Már csak egy kérdés a használatról — a kihagyások hossza a technológiaválasztás szempontjából is számít." },
    { id: "telek", cim: "Telek adottságai",
      uzenet: "A használat alapján jelenleg {irany} tűnik megfelelő iránynak. Most megnézzük, hogy a telek adottságai milyen kivitelezési feltételeket szabnak.",
      uzenetVegyes: "A használat alapján vegyes a kép — erre a végén visszatérünk. Most nézzük meg, mit mondanak a telek adottságai." },
    { id: "vizelhelyezes", cim: "Vízelhelyezés lehetősége",
      uzenet: "Az utolsó kérdés a kezelt víz elhelyezéséről szól. Ez az egyetlen szempont, ami önmagában is kizáró lehet." },
    { id: "eredmeny", cim: "Eredmény", zaro: true,
      uzenet: "Készen vagyunk. Ez a kép rajzolódik ki a válaszaiból." }
  ],

  /* -------------------------------------------------------------- KÉRDÉSEK */
  /* `lepes`: melyik szakaszhoz tartozik. Egy szakaszban több kérdés is lehet.
     `magyarazat`: a válasz UTÁN megjelenő doboz szövege, válaszazonosító szerint.
     A specifikáció 2. pontja szerint minden válasz után azonnal meg kell
     magyarázni, mit jelent az adott válasz, és miért számít. */
  kerdesek: [
    {
      id: "hasznalat", lepes: "hasznalat",
      kerdes: "Milyen rendszeresen használják az ingatlant?",
      valaszok: [
        { id: "eletvitelszeru", cimke: "Egész évben, életvitelszerűen" },
        { id: "hetvegi",        cimke: "Hétvégente vagy alkalmanként" },
        { id: "szezonalis",     cimke: "Csak bizonyos hónapokban" }
      ],
      magyarazat: {
        eletvitelszeru: "Ez a technológiaválasztás legfontosabb bemenete. Egész éves, egyenletes terhelésnél a baktériumkultúra folyamatosan táplálékhoz jut, tehát aktív biológiai tisztítás is fenntartható. A 2–3 hetes szabadság önmagában nem minősül időszakos használatnak.",
        hetvegi:        "A hétvégi vagy alkalmi használat szakaszos terhelést jelent. Ilyenkor a folyamatos, aktív biológiai működés nehezebben tartható fenn — a következő két kérdés dönti el, hogy ez tényleg időszakos mintázat-e.",
        szezonalis:     "A csak bizonyos hónapokban lakott ingatlan hosszú üresjáratokkal jár. A következő két kérdés azt vizsgálja, mekkora terhelés jut a használt időszakra — ez különbözteti meg az időszakos használatot az erős szezonalitástól."
      }
    },
    {
      /* A SÁVOK SZÁNDÉKOSAN AZONOSAK a 8. szekció (ársávbecslő) kapacitás-
         kérdésének sávjaival. Enélkül a két modul között nem lehetne átvinni a
         választ: a „2–3 fő" sem az „1–2", sem a „3–4" sávba nem esik
         egyértelműen, tehát vagy újra kellene kérdezni, vagy tippelnénk.
         ⚠️ A specifikáció példája „magas létszám (4–5 fő)" — ez a 3–4 és az
         5–6 sáv határán fekszik. A jelenlegi értelmezés: MAGAS = 5 főtől.
         Ez a határ jóváhagyásra vár. */
      id: "letszam", lepes: "letszam",
      kerdes: "Hányan használják rendszeresen?",
      valaszok: [
        { id: "1-2",  cimke: "1–2 fő" },
        { id: "3-4",  cimke: "3–4 fő" },
        { id: "5-6",  cimke: "5–6 fő" },
        { id: "7-10", cimke: "7–10 fő" },
        { id: "10+",  cimke: "10 fő felett" }
      ],
      magyarazat: {
        "1-2":  "Alacsony létszámnál a napi szennyvízmennyiség is alacsony. Ez önmagában nem probléma, de ha hosszabb távollétekkel párosul, a terhelés annyira egyenetlenné válhat, hogy a mintázat már határesetnek számít.",
        "3-4":  "Ez a leggyakoribb háztartásméret, és a terhelés szempontjából jól kiszámítható.",
        "5-6":  "Magasabb létszámnál a csúcsterhelés is magasabb. Ha ez időszakos használattal párosul, a rendszerre hullámzó terhelés jut — ilyenkor a mintázat nem sorolható be automatikusan.",
        "7-10": "Ekkora létszámnál a méretezés önmagában is szakmai kérdés, és a csúcsterhelés kezelése a technológiaválasztást is befolyásolja.",
        "10+":  "Tíz fő felett már nem háztartási méretről beszélünk: a rendszer több egységből épül, és a méretezés egyedi tervezést igényel."
      }
    },
    {
      id: "kihagyas", lepes: "kihagyas",
      kerdes: "Előfordul-e több hetes vagy hónapos kihagyás?",
      valaszok: [
        { id: "nincs",   cimke: "Nem, legfeljebb szabadság" },
        { id: "hetek",   cimke: "Igen, néhány hetes" },
        { id: "honapok", cimke: "Igen, több hónapos" }
      ],
      magyarazat: {
        nincs:   "Folyamatos terhelés mellett a baktériumkultúra stabilan fenntartható — ez az aktív biológiai tisztítás alapfeltétele.",
        hetek:   "A néhány hetes kihagyás után a kultúra újraindul, de a mintázat már nem teljesen egyenletes. Hogy ez kizárja-e az aktív rendszert, a használat jellegével és a létszámmal együtt derül ki.",
        honapok: "A több hónapos üresjárat alatt az aktív biológiai kultúra leépül. Az újraindítás megoldható, de rendszeres ismétlődés mellett ez üzemeltetési kérdéssé válik, amit érdemes személyesen átbeszélni."
      }
    },
    {
      id: "talajviz", lepes: "telek",
      kerdes: "Van arra utaló jel, hogy magasan lehet a talajvíz?",
      sugo: "Ásott kút, vizes pince, környékbeli tapasztalat.",
      valaszok: [
        { id: "igen",     cimke: "Igen" },
        { id: "nem",      cimke: "Nem" },
        { id: "nemtudom", cimke: "Nem tudom", nemtudom: true }
      ],
      magyarazat: {
        igen:     "Ez önmagában nem zárja ki a javasolt megoldást. A kivitelezésnél viszont kiemelt szivárogtatóval és speciális rögzítéssel érdemes számolni, hogy a talajvíz ne emelje ki a tartályt.",
        nem:      "Ez a szokásos kialakítást teszi lehetővé: a tartály gravitációsan, kiemelés nélkül telepíthető, és a tisztított víz elhelyezése is a bevett módon oldható meg.",
        nemtudom: "Ez nem akadály: a talajvízszint helyszíni felméréssel egyértelműen tisztázható. A tisztázandók közé kerül, a folyamat mehet tovább."
      }
    },
    {
      id: "talaj", lepes: "telek",
      kerdes: "Milyen a talaj a telken?",
      valaszok: [
        { id: "homokos",  cimke: "Inkább homokos" },
        { id: "kotott",   cimke: "Inkább kötött / agyagos" },
        { id: "nemtudom", cimke: "Nem tudom", nemtudom: true }
      ],
      magyarazat: {
        homokos:  "A jól szivárgó talaj a tisztított víz elhelyezését egyszerűbbé teszi, és a szivárogtató is kisebb lehet.",
        kotott:   "A rosszul szivárgó, agyagos talaj nem kizáró ok, de a tisztított víz elhelyezése kiemelt szivárogtatóval oldható meg. Ez a kivitelezést és a költséget is befolyásolja.",
        nemtudom: "A talaj szivárgóképessége helyszínen megállapítható. A tisztázandók közé kerül, a folyamat mehet tovább."
      }
    },
    {
      id: "terulet", lepes: "vizelhelyezes",
      kerdes: "Mekkora összefüggő, beépítetlen terület áll rendelkezésre a telken?",
      sugo: "Hozzávetőleges érték is elég — ide kerülhet a szivárogtató.",
      valaszok: [
        { id: "kicsi",    cimke: "Kevesebb mint kb. 30 m²" },
        { id: "kozepes",  cimke: "Kb. 30–60 m²" },
        { id: "nagy",     cimke: "Kb. 60 m² felett" },
        { id: "nemtudom", cimke: "Nem tudom", nemtudom: true }
      ],
      magyarazat: {
        kicsi:    "Ez a kérdés innentől nem technológiaválasztás. Ha a vízelhelyezéshez nincs elegendő terület, nincs „kisebb helyigényű” szennyvíztisztító megoldás — ilyenkor a zárt tároló marad a járható irány, és mindenképpen egyeztetés szükséges.",
        kozepes:  "Ez a méret a biológiai rendszer szivárogtatójához jellemzően elegendő. Az oldómedence szikkasztómezője viszont ennek jellemzően a két-háromszorosa, tehát az az irány ekkora területen nem alakítható ki.",
        nagy:     "Ez a méret mindkét irány vízelhelyezését megengedi. A szükséges szivárogtató pontos mérete a terheléstől, a talajszerkezettől és a talajvízszinttől függ — ezt a felmérés adja meg.",
        nemtudom: "Ez nem blokkolja a folyamatot: a szabad terület a tisztázandók közé kerül, és a helyszíni felmérésen egyértelműen megállapítható."
      }
    }
  ],

  /* --------------------------------------------------- ELSŐ SZAKASZ — IRÁNY */
  /* A specifikáció 3. pontja. A szabályok SORRENDBEN értékelődnek ki, az első
     illeszkedő nyer. `ha`: a válaszazonosítók, `bármelyik` értelemben tömbben.
     `irany`: abclear | epureco | egyeztetes.
     `ok`: határesetnél ez kerül a kimenetbe („mi miatt nem lehetett dönteni”). */
  iranySzabalyok: [
    { ha: { hasznalat: ["eletvitelszeru"], kihagyas: ["honapok"] }, irany: "egyeztetes",
      ok: "életvitelszerű használat, de rendszeres, több hónapos kihagyásokkal" },
    { ha: { hasznalat: ["eletvitelszeru"], letszam: ["1-2"], kihagyas: ["hetek"] }, irany: "egyeztetes",
      ok: "életvitelszerűen lakott ingatlan, amit egy-két fő használ, gyakori hosszabb távollétekkel" },
    { ha: { hasznalat: ["eletvitelszeru"] }, irany: "abclear" },
    { ha: { hasznalat: ["hetvegi"], letszam: ["5-6", "7-10", "10+"] }, irany: "egyeztetes",
      ok: "szinte minden hétvégén, de magas létszámmal használt ingatlan" },
    { ha: { hasznalat: ["hetvegi"] }, irany: "epureco" },
    { ha: { hasznalat: ["szezonalis"], letszam: ["5-6", "7-10", "10+"] }, irany: "egyeztetes",
      ok: "erős szezonalitás: az idény alatt intenzív használat, azon kívül üres ingatlan" },
    { ha: { hasznalat: ["szezonalis"] }, irany: "epureco" }
  ],

  /* ------------------------------------ MÁSODIK SZAKASZ — A TELEK HATÁSAI */
  /* Ezek NEM technológiát választanak, hanem az első szakasz eredményére
     reagálnak (specifikáció 4. pont). A `terulet` a kivétel: kizáró is lehet. */
  telekHatasok: [
    { ha: { talajviz: "igen" },
      feltetelek: ["kiemelt-szivarogtato", "specialis-rogzites"] },
    { ha: { talajviz: "nemtudom" }, tisztazandok: ["talajviz"] },
    { ha: { talaj: "kotott" }, feltetelek: ["kiemelt-szivarogtato"] },
    { ha: { talaj: "nemtudom" }, tisztazandok: ["talaj"] },
    { ha: { terulet: "nemtudom" }, tisztazandok: ["terulet"] }
  ],

  /* ⚠️ MUNKAHIPOTÉZIS, JÓVÁHAGYÁSRA VÁR. A specifikáció 5. pontjának kétlépcsős
     kiértékelése. A modul SOHA nem közöl konkrét méterszámot arról, mekkora
     szivárogtató kell — csak azt, hogy a rendelkezésre álló terület melyik
     lépcsőt engedi. A `kicsi` sáv a 2. lépcsőt is bukja, a `kozepes` csak az
     1. lépcsőt (az oldómedence szikkasztómezője a biológiaiénak 2–3-szorosa). */
  teruletSavok: {
    kicsi:   { biologiai: false, oldomedence: false },
    kozepes: { biologiai: true,  oldomedence: false },
    nagy:    { biologiai: true,  oldomedence: true  },
    nemtudom:{ biologiai: null,  oldomedence: null  }
  },

  /* ------------------------------------------------ KIVITELEZÉSI FELTÉTELEK */
  feltetelek: {
    "kiemelt-szivarogtato": {
      cimke: "Kiemelt szivárogtató", jel: "csepp",
      leiras: "A tisztított vizet a talajszint fölé emelt szivárogtatóban helyezzük el, hogy a rossz szivárgás vagy a magas talajvíz ne akadályozza a beszivárgást."
    },
    "specialis-rogzites": {
      cimke: "Speciális rögzítés", jel: "horgony",
      leiras: "A tartályt a betonalaphoz rögzítjük, hogy a magas talajvíz ne emelhesse ki."
    },
    "gravitacios-megoldas": {
      cimke: "Külön műszaki megoldás a gravitációra", jel: "lejtes",
      leiras: "Ha a csőkivezetés mélysége és a terep miatt a gravitációs kialakítás nem működik, átemelés vagy módosított magassági kialakítás szükséges."
    }
  },

  /* -------------------------------------------------------- TISZTÁZANDÓK */
  /* `mindig: true` — a specifikáció 6. pontja szerint ezek KÖTELEZŐEN
     megjelennek, függetlenül a válaszoktól. */
  tisztazandok: {
    kut: {
      mindig: true, cimke: "Kút / telekhatár közelsége",
      hogyan: "A pontos védőtávolság nem adható meg egyetlen méterszámmal: a helyi adottságok és az engedélyezési feltételek együtt határozzák meg. Helyszíni felmérésen tisztázható."
    },
    szivarogtato: {
      mindig: true, cimke: "A szükséges szivárogtató mérete",
      hogyan: "A várható terheléstől, a talajszerkezettől és a talajvízszinttől függ. Ezért a felmérés adja meg, nem előre megadott méterszám."
    },
    terep: {
      mindig: true, cimke: "A csőkivezetés mélysége és a terep lejtése",
      hogyan: "Ez dönti el, működik-e a gravitációs kialakítás. A meglévő csőkivezetés helyszínen megnézhető."
    },
    talajviz: {
      cimke: "Pontos talajviszonyok",
      hogyan: "A talajvízszint helyszíni felméréssel egyértelműen megállapítható."
    },
    talaj: {
      cimke: "A talaj szivárgóképessége",
      hogyan: "A talajszerkezet a helyszínen megnézhető; kétséges esetben szivárgási próba adja meg."
    },
    terulet: {
      cimke: "Szabad terület a vízelhelyezéshez",
      hogyan: "A telken rendelkezésre álló összefüggő, beépítetlen terület a helyszínrajzról vagy a helyszínen megállapítható."
    }
  },

  /* -------------------------------------------------------------- TERMÉKEK */
  termekek: {
    abclear: {
      nev: "A.B. Clear",
      rovid: "A használati mintázat alapján ez tűnik a legerősebb iránynak, de a telek adottságai még pontosíthatják az ajánlást.",
      indoklas: "Az egész éves, egyenletes terhelés mellett az aktív biológiai tisztítás fenntartható: a baktériumkultúra folyamatosan táplálékhoz jut. Az iszapzsákos kialakítás miatt a rendszer szippantásmentes.",
      url: "megoldasok/ab-clear"
    },
    epureco: {
      nev: "Epureco oldómedence",
      rovid: "A használat időszakos mintázata alapján ez tűnik a legerősebb iránynak, de a telek adottságai még pontosíthatják az ajánlást.",
      indoklas: "Az időszakos, szakaszos terhelést az oldómedence jól tűri: nincs benne aktív biológiai kultúra, amit fenn kellene tartani, és áramellátást sem igényel.",
      /* A specifikáció 6. pontja: Epureco esetén a kompromisszumot MINDIG ki
         kell mondani. Ez nem opcionális kiegészítés. */
      kompromisszum: "Ez tisztítási szempontból kompromisszum: az egyszerűbb, terhelésingadozást jól tűrő működésért cserébe a tisztítás nagy része a talajban történik, alacsonyabb tisztítási teljesítménnyel, mint az A.B. Clear aktív biológiai tisztítása.",
      url: "megoldasok/epureco"
    },
    zarttarolo: {
      nev: "Zárt tároló",
      rovid: "A vízelhelyezés hiánya miatt ez marad a járható irány.",
      indoklas: "Ha a tisztított víz elhelyezésére nincs elegendő terület, az már nem technológiaválasztási kérdés: szivárogtatás nélkül a keletkező szennyvizet gyűjteni és elszállíttatni kell.",
      url: "megoldasok/megoldastipusok-osszehasonlitasa"
    },
    egyeztetes: {
      nev: "Szakértői egyeztetés",
      rovid: "A megadott szempontok ellentmondanak egymásnak, ezért a modul nem nevez meg terméket.",
      indoklas: "Vegyes a kép: a válaszok alapján nem lehet automatikusan dönteni. Az alábbi pontok miatt érdemes személyesen átnézni a helyzetet.",
      url: "konzultacio"
    }
  },

  /* ----------------------------------------------------------- TOVÁBBLÉPÉS */
  /* A specifikáció 7. pontja: a záró képernyőn NEM kérünk kontaktadatot. */
  tovabb: {
    elsodleges: { cimke: "Nézze meg, nagyságrendileg mibe kerülne", url: "#ai-dontestamogato" },
    masodlagos: [
      { cimke: "Kizáró és korlátozó feltételek", url: "megoldasok/kizaro-es-korlatozo-feltetelek" },
      { cimke: "A tisztított víz elszivárogtatása", url: "megoldasok/biologiai-telek-es-terhelesi-feltetelek" },
      { cimke: "Szakértői konzultáció", url: "konzultacio" }
    ]
  }
};
