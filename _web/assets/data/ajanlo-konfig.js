/* =============================================================================
   ÖkoTech Home — AI megoldás-ajánló (6. szekció) · KONFIGURÁCIÓ
   -----------------------------------------------------------------------------
   Forrás: `OkoTech-Home_AI-modul_fejlesztoi_specifikacio.2.docx` (2026-08-24),
   ÁTDOLGOZVA az `okotech-megoldas-ajanlo-hibalista-es-javaslatok.docx` (eSystem
   Integration Kft., 2026-09-11) alapján.

   EZT A FÁJLT A CÉG SZERKESZTHETI, fejlesztő nélkül: a kérdések, a válaszok, a
   döntési szabályok és a kimeneti szövegek mind itt élnek. A modul logikája
   (`assets/js/ajanlo.js`) egyetlen szakmai állítást sem tartalmaz.

   Módosítás után elég a fájlt feltölteni és a hivatkozás verzióját emelni
   (`index.html`: `ajanlo-konfig.js?v=NN`).

   ═══ A LEGFONTOSABB SZABÁLY (hibalista 3.2.) ═════════════════════════════════
   A MODUL NEM VEZETHET OLYAN KIMENETRE ÍTÉLETKÉNT, AMIRE AZ ÖKOTECH-HOME NEM
   TUD AJÁNLATOT ADNI. Ezért lett a korábbi „zárt tároló" végkövetkeztetésből
   „a vízelhelyezés a szűk keresztmetszet": a zárt tároló a szótárban marad
   (`termekek.zarttarolo`), de a modul SOHA nem választja kimenetnek — felmérés
   utáni lehetséges irány, nem egy laikus szemmértékén alapuló ítélet.

   ═══ NÉGY KIMENETTÍPUS, NÉGY KÜLÖN ZÁRÓ KÉPERNYŐ (hibalista 3.1.) ════════════
   A záró képernyő korábban SABLON volt: minden kimenetnél ugyanazt a hármat
   csinálta (terméknév, kivitelezési feltételek, átvezetés az ársávbecslőre) —
   akkor is, ha a modul el sem jutott javaslatig. Innentől ELÁGAZÁS: a fejlécet,
   a blokkokat és a következő lépést a `kimenetek` alatti típus szabja meg.

   ⚠️ JÓVÁHAGYÁSRA VÁR (a specifikáció 8. pontja és a hibalista 9. fejezete):
     · a három használati kategória definíciója és a hozzájuk rendelt termékek,
     · a határesetek listájának teljessége,
     · a szabad terület sávhatárai (`teruletSavok`) — MUNKAHIPOTÉZISEK,
     · a befogadó-kérdés (árok, csapadékvíz-elvezetés, élővíz) — amíg nincs
       szakmai döntés, a modul csak TISZTÁZANDÓKÉNT említi, nem kérdez rá,
     · a tisztázandók `ido` mezője (mennyi idő) — szándékosan üres, lásd ott.
   ============================================================================= */
window.OTH_AJANLO = {

  /* A DÖNTÉSI LOGIKA VERZIÓJA. A mentett eredmény mellé is elmegy, hogy egy
     későbbi visszakeresésnél tudni lehessen, milyen szabályok szerint készült.
     Emeld, valahányszor a kérdéseken, a szabályokon vagy a sávhatárokon
     változtatsz. */
  verzio: "2026-09-13",

  /* ---------------------------------------------------------- MENTÉS ------
     A záró képernyőn a látogató elmentheti az eredményt. A mentés AZONOSÍTÓT
     kap, és a szerveren is eltároljuk, hogy visszakereshető és továbbvihető
     legyen. A rekordban NINCS személyes adat: csak a válaszok és a belőlük
     számított kimenet.

     AZ AZONOSÍTÓ MAGÁTÓL KELETKEZIK (hibalista H11 és 6.2.). Korábban a mentés
     egy másodlagos gomb volt öt sor magyarázat alatt, a zöld elsődleges gomb
     után: aki nem olvasta végig, nem mentett, és elvesztette a megoszthatóságot
     és a visszakereshetőséget. Most az eredmény megjelenésekor megszületik az
     azonosító, és a gomb már csak annyit csinál, hogy VÁGÓLAPRA teszi a linket.
     Adatot ehhez sem kérünk, tehát nincs jogi akadálya.

     ⚠️ A `megorzesSzoveg`-nek egyeznie kell az adatkezelési tájékoztatóval és
     az `api/config.php` `eredmeny.megorzes_nap` értékével.
     Ha a végpont nem elérhető (nincs `config.php`, ki van kapcsolva, hálózati
     hiba), a modul NEM hallgat: szövegfájlként felkínálja a letöltést, és
     kimondja, hogy szerverre most nem került. */
  mentes: {
    /* MIT KAPOTT — az automatikusan létrejött azonosító MELLETT. A látogató
       enélkül nem tudja, miért van kódja, és a kód önmagában riasztó lehet. */
    bevezeto: "Ez nem regisztráció: nevet, e-mail-címet vagy telefonszámot nem kértünk "
            + "hozzá, és nem tudjuk, ki Ön. Egyetlen dolgot csinál: megjegyzi, mit adott "
            + "meg. Ezzel bármikor előveheti ezt az eredményt, kinyomtathatja vagy PDF-be "
            + "mentheti, a további eszközeink (például a lap alatti ársávbecslő) pedig nem "
            + "kérdezik újra ugyanazt.",
    /* MIÉRT ÉRDEMES TOVÁBBADNI. Egy családi ház szennyvízkezeléséről szinte soha
       nem egy ember dönt — a megosztható link a második döntéshozót éri el. */
    linkBevezeto: "Egy családi ház szennyvízkezeléséről ritkán dönt egy ember. Ezt a "
                + "linket elküldheti annak, akivel együtt dönt — ugyanezt fogja látni.",
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
     magyarázni, mit jelent az adott válasz, és miért számít.

     A BUBORÉKOK HÁROMRÉSZESEK (hibalista 5.): mit jelent → mi változott ettől →
     mi maradt nyitva. Az utolsó rész köti össze a következő kérdéssel, és
     önmagában megszünteti azt az ismétlést, ami a régi szövegekben volt (H13).
     A buborék akkor jó, ha elolvasása után a látogató be tudja fejezni ezt a
     mondatot: „tehát nálam…".

     `magyarazatFugg`: ugyanez, de egy KORÁBBI válasz függvényében. Egyetlen
     helyen kell, a kihagyás-kérdésnél: ott a mondat csak akkor igaz, ha tudjuk,
     milyen használat mellett hangzik el. A `{letszam}` a megadott létszámsáv
     címkéjére cserélődik.

     `levezetes`: egy soros, felhalmozódó állítás a jobb oldali panelre
     (hibalista 4.2.) — „ami eddig eldőlt". A buborékok elgörögnek, ez megmarad. */
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
        eletvitelszeru: "Ez a technológiaválasztás legfontosabb bemenete: egész éves, egyenletes terhelésnél a baktériumkultúra folyamatosan táplálékhoz jut, tehát aktív biológiai tisztítás is fenntartható. A 2–3 hetes szabadság ezen nem változtat. Ami még nyitott: mekkora terhelés jut a rendszerre, és van-e ennél hosszabb kihagyás.",
        hetvegi:        "A hétvégi vagy alkalmi használat szakaszos terhelést jelent, tehát a folyamatos, aktív biológiai működés nehezebben tartható fenn. Időszakos használatnál ez fordítva van, mint az életvitelszerűnél: a baktériumkultúra a kihagyások alatt éhezne, ezért ott egyszerűbb, terhelésingadozást jobban tűrő megoldás való. Ami még nyitott: hányan használják, és milyen hosszúak a kihagyások.",
        szezonalis:     "A csak bizonyos hónapokban lakott ingatlan hosszú üresjáratokkal jár, tehát az aktív biológiai kultúra folyamatos fenntartása nem reális elvárás. Ami még nyitott: mekkora terhelés jut a használt időszakra — ez különbözteti meg az időszakos használatot az erős szezonalitástól."
      },
      levezetes: {
        eletvitelszeru: { bal: "Egész éves, egyenletes terhelés", jobb: "aktív biológiai tisztítás fenntartható" },
        hetvegi:        { bal: "Hétvégi, alkalmi használat",      jobb: "szakaszos terhelés" },
        szezonalis:     { bal: "Szezonális használat",            jobb: "hosszú üresjáratok" }
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
        "1-2":  "Alacsony létszámnál a napi szennyvízmennyiség is alacsony — ez a méretezés alsó sávja, és önmagában nem korlátoz. Ami még nyitott: ha ez hosszabb távollétekkel párosul, a terhelés annyira egyenetlenné válhat, hogy a mintázat már határesetnek számít.",
        "3-4":  "3–4 fő napi terhelése stabil, jól tervezhető mennyiség — erre a sávra készül a rendszerek alapmérete, tehát a létszám önmagában nem korlátoz. Ami még nyitott: hogy ez a terhelés egész évben megvan-e.",
        "5-6":  "Magasabb létszámnál a csúcsterhelés is magasabb, a méretezés viszont erre is bevett. Ami még nyitott: ha ez időszakos használattal párosul, hullámzó terhelés jut a rendszerre — azt a mintázatot már nem soroljuk be automatikusan.",
        "7-10": "Ekkora létszámnál a méretezés önmagában is szakmai kérdés: a csúcsterhelés kezelése a technológiaválasztást is befolyásolja. Ami még nyitott: a napi csúcsok eloszlása — ezt a felmérésen vesszük fel.",
        "10+":  "Tíz fő felett már nem háztartási méretről beszélünk: a rendszer több egységből épül, és a méretezés egyedi tervezést igényel. Ami még nyitott: gyakorlatilag minden méretezési részlet — ezt tervezői szinten kell átnézni."
      },
      levezetes: {
        "1-2":  { bal: "1–2 fő",        jobb: "alacsony terhelés, a méretezés alsó sávja" },
        "3-4":  { bal: "3–4 fő",        jobb: "szokásos méretezés, nem korlátoz" },
        "5-6":  { bal: "5–6 fő",        jobb: "magasabb csúcsterhelés, méretezéssel kezelhető" },
        "7-10": { bal: "7–10 fő",       jobb: "a méretezés önmagában szakmai kérdés" },
        "10+":  { bal: "10 fő felett",  jobb: "több egység, egyedi tervezés" }
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
        nincs:   "Ezzel a használati kép teljes. A specifikáció két szintje itt válik el egymástól: innentől a telek adottságai már nem azt befolyásolják, MELYIK megoldás jöjjön szóba, hanem azt, MILYEN FELTÉTELEKKEL valósítható meg.",
        hetek:   "A néhány hetes kihagyás után a baktériumkultúra újraindul, de a mintázat már nem teljesen egyenletes. Ami még nyitott: hogy ez kizárja-e az aktív rendszert — a használat jellegével és a létszámmal együtt derül ki, és lehet, hogy nem lesz automatikusan eldönthető.",
        honapok: "A több hónapos üresjárat alatt az aktív biológiai kultúra leépül. Az újraindítás megoldható, de rendszeres ismétlődés mellett ez üzemeltetési kérdéssé válik. Ami még nyitott: milyen gyakran és milyen hosszan — ezt érdemes személyesen átbeszélni."
      },
      /* A FOLYAMAT LEGFONTOSABB PILLANATA (hibalista 5.). Itt dől el a
         technológia, és itt van a határvonal a két szint között — ezt a
         specifikáció logikája tartalmazza, de a látogatónak eddig sehol nem
         mondtuk ki. Ez a mondat ingyen van. */
      magyarazatFugg: {
        kulcs: "hasznalat",
        terkep: {
          eletvitelszeru: {
            nincs: "Ezzel a használati kép teljes: egész évben, egyenletesen, {letszam}. Ez az a mintázat, ami mellett az aktív biológiai tisztítás megbízhatóan működik — a technológia kérdése ezzel eldőlt. Innentől a telek adottságai már nem azt befolyásolják, melyik megoldás jöjjön szóba, hanem azt, milyen feltételekkel valósítható meg."
          },
          hetvegi: {
            nincs: "Ezzel a használati kép teljes: hétvégi, alkalmi használat, hosszú kihagyás nélkül, {letszam}. A terhelés szakaszos, de kiszámítható — ez a mintázat az egyszerűbb, terhelésingadozást jól tűrő megoldás felé mutat, és a technológia kérdése ezzel eldőlt. Innentől a telek adottságai már nem azt befolyásolják, melyik megoldás jöjjön szóba, hanem azt, milyen feltételekkel valósítható meg."
          },
          szezonalis: {
            nincs: "Ezzel a használati kép teljes: idényben használt ingatlan, azon belül hosszú kihagyás nélkül, {letszam}. Az idényen kívüli üresjárat miatt itt nem az aktív biológiai kultúra fenntartása a cél, hanem a terhelésingadozás jó tűrése — a technológia kérdése ezzel eldőlt. Innentől a telek adottságai a kivitelezés feltételeit szabják, nem a megoldást."
          }
        }
      },
      levezetes: {
        nincs:   { bal: "Nincs hosszú kihagyás",     jobb: "a technológia eldőlt" },
        hetek:   { bal: "Néhány hetes kihagyás",     jobb: "a mintázat nem teljesen egyenletes" },
        honapok: { bal: "Több hónapos kihagyás",     jobb: "az aktív kultúra leépül" }
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
        igen:     "Ez önmagában nem zárja ki a javasolt megoldást — a kivitelezés feltételeit szabja meg. Ettől kiemelt szivárogtatóval és a tartály speciális rögzítésével számolunk, hogy a talajvíz ne emelhesse ki az üres tartályt. Ami még nyitott: a talaj szivárgóképessége, ami a szivárogtató méretét is befolyásolja.",
        nem:      "Ez a szokásos kialakítást teszi lehetővé: a tartály gravitációsan, kiemelés nélkül telepíthető. Tehát nem lesz szükség kiemelt szivárogtatóra, és a tartály speciális rögzítése sem merül fel. Ami még nyitott: a talaj szivárgóképessége — a szivárogtató méretét az adja meg.",
        nemtudom: "Ez nem akadály: a talajvízszint helyszíni felméréssel egyértelműen tisztázható, és a tisztázandók közé kerül. Ami még nyitott: amíg nincs meg, azzal kell számolni, hogy kiemelt szivárogtató és speciális rögzítés is szükségessé válhat."
      },
      levezetes: {
        igen:     { bal: "Magas talajvíz",        jobb: "kiemelt szivárogtató és speciális rögzítés" },
        nem:      { bal: "Nincs magas talajvíz",  jobb: "gravitációs telepítés" },
        nemtudom: { bal: "Talajvíz nem ismert",   jobb: "a felmérésen tisztázzuk" }
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
        homokos:  "A jól szivárgó talaj a tisztított víz elhelyezését egyszerűbbé teszi: kisebb szivárogtató is elég, és ez a kivitelezés költségén is látszik. Ami még nyitott: mekkora összefüggő terület áll rendelkezésre — a szivárogtató ugyanis helyet kér.",
        kotott:   "A rosszul szivárgó, agyagos talaj nem kizáró ok, de a kivitelezés feltételeit megszabja: a tisztított víz elhelyezése kiemelt szivárogtatóval oldható meg, ami a költséget is befolyásolja. Ami még nyitott: a rendelkezésre álló terület — kötött talajnál a szivárogtató jellemzően nagyobb.",
        nemtudom: "A talaj szivárgóképessége a helyszínen megállapítható, kétséges esetben szivárgási próbával — a tisztázandók közé kerül. Ami még nyitott: amíg nincs meg, a szivárogtató méretét sem lehet pontosítani."
      },
      levezetes: {
        homokos:  { bal: "Homokos talaj",        jobb: "kisebb szivárogtató elég" },
        kotott:   { bal: "Kötött, agyagos talaj", jobb: "kiemelt szivárogtató szükséges" },
        nemtudom: { bal: "Talaj nem ismert",     jobb: "helyszínen megnézhető" }
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
      /* A SÁVOK ÉRTELMEZÉSE (hibalista 5.). A specifikáció jó okkal tiltja a
         konkrét méterszámot — a válasz utáni magyarázat viszont megmondhatja,
         mit jelent ez az adott esetben. A „kicsi" ágon ez KÖTELEZŐ: ott ki kell
         mondani, hogy komoly korlát lehet — de ítélet nélkül (H2). */
      magyarazat: {
        kicsi:    "Ez komoly korlát lehet, és innentől nem is technológiaválasztás a kérdés. Nincs „kisebb helyigényű” szennyvíztisztító megoldás, mert a helyigény nagy részét nem a tartály adja, hanem a szivárogtató. Ami még nyitott: a ténylegesen felhasználható terület — a becsült és a felmérésen mért érték gyakran eltér —, és hogy van-e befogadó a közelben. Ezt felmérés nélkül nem döntjük el.",
        kozepes:  "Ez a méret a biológiai rendszer szivárogtatójához jellemzően elegendő, tehát a technológián nem változtat. Az oldómedence szikkasztómezője viszont ennek jellemzően a két-háromszorosa, tehát az az irány ekkora területen nem alakítható ki. Ami még nyitott: a pontos méret, amit a felmérés ad meg.",
        nagy:     "A rendelkezésre álló terület a szivárogtató kialakítását nem korlátozza. A pontos méretet a felmérés adja meg, de nagyságrendileg van hely rá.",
        nemtudom: "Ez nem blokkolja a folyamatot: a szabad terület a tisztázandók közé kerül, és a helyszíni felmérésen egyértelműen megállapítható. Ami még nyitott: amíg nincs meg, a vízelhelyezés módját sem lehet véglegesíteni."
      },
      levezetes: {
        kicsi:    { bal: "Kevesebb mint kb. 30 m²", jobb: "a vízelhelyezés a nyitott kérdés" },
        kozepes:  { bal: "Kb. 30–60 m²",            jobb: "a biológiai szivárogtatóhoz elég" },
        nagy:     { bal: "Kb. 60 m² felett",        jobb: "a terület nem korlátoz" },
        nemtudom: { bal: "Terület nem ismert",      jobb: "helyszínrajzról megállapítható" }
      }
    }
  ],

  /* --------------------------------------------------- ELSŐ SZAKASZ — IRÁNY */
  /* A specifikáció 3. pontja. A szabályok SORRENDBEN értékelődnek ki, az első
     illeszkedő nyer. `ha`: a válaszazonosítók, `bármelyik` értelemben tömbben.
     `irany`: abclear | epureco | egyeztetes.

     `ok`: határesetnél ez kerül a kimenetbe. AZ ELLENTMONDÁST MEG KELL NEVEZNI
     (hibalista H8 és 4.3.): a régi „a megadott szempontok ellentmondanak
     egymásnak" igaz volt, de nem mondta meg, MI mond ellent MINEK — a látogató
     ebből azt hihette, hogy ő rontott el valamit, és visszament „javítani". */
  iranySzabalyok: [
    { ha: { hasznalat: ["eletvitelszeru"], kihagyas: ["honapok"] }, irany: "egyeztetes",
      ok: "Két szempont húz ellentétes irányba: a rendszeres, egész éves használat az aktív biológiai tisztítás felé, a több hónapos üresjárat viszont ellene." },
    { ha: { hasznalat: ["eletvitelszeru"], letszam: ["1-2"], kihagyas: ["hetek"] }, irany: "egyeztetes",
      ok: "Két szempont húz ellentétes irányba: az ingatlan életvitelszerűen lakott, a terhelés viszont — egy-két fő, gyakori hosszabb távollétekkel — a szakaszos mintázat felé mutat." },
    { ha: { hasznalat: ["eletvitelszeru"] }, irany: "abclear" },
    { ha: { hasznalat: ["hetvegi"], letszam: ["5-6", "7-10", "10+"] }, irany: "egyeztetes",
      ok: "Két szempont húz ellentétes irányba: a hétvégi, alkalmi használat az egyszerűbb, terhelésingadozást tűrő megoldás felé, a magas létszám csúcsterhelése viszont az aktív biológiai tisztítás felé." },
    { ha: { hasznalat: ["hetvegi"] }, irany: "epureco" },
    { ha: { hasznalat: ["szezonalis"], letszam: ["5-6", "7-10", "10+"] }, irany: "egyeztetes",
      ok: "Két szempont húz ellentétes irányba: az idény alatti intenzív, magas létszámú használat az aktív biológiai tisztítás felé, az idényen kívüli hosszú üresjárat viszont ellene." },
    { ha: { hasznalat: ["szezonalis"] }, irany: "epureco" }
  ],

  /* ------------------------------------ MÁSODIK SZAKASZ — A TELEK HATÁSAI */
  /* Ezek NEM technológiát választanak, hanem az első szakasz eredményére
     reagálnak (specifikáció 4. pont). A `terulet` a kivétel: a vízelhelyezést
     önmagában kérdésessé teheti. */
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
     1. lépcsőt (az oldómedence szikkasztómezője a biológiaiénak 2–3-szorosa).

     ⚠️ FELOLDANDÓ SPECIFIKÁCIÓS ELLENTMONDÁS (hibalista S2). Ha a szükséges
     szivárogtató mérete a terheléstől, a talajszerkezettől és a talajvízszinttől
     függ — és ezért a modul nem ad méterszámot —, akkor a „nincs elég hely"
     ÍTÉLET sem hozható meg belőle. A `kicsi` sáv ezért nem ítéletre vezet,
     hanem a „vízelhelyezés kérdéses" kimenetre: ott a felmérés dönt. */
  teruletSavok: {
    kicsi:   { biologiai: false, oldomedence: false },
    kozepes: { biologiai: true,  oldomedence: false },
    nagy:    { biologiai: true,  oldomedence: true  },
    nemtudom:{ biologiai: null,  oldomedence: null  }
  },

  /* A terület-szabály SZÖVEGEI. Külön a döntéstől, mert ezeket a cég
     szerkesztheti — és mert az `ellentmondasEsSzuk` a hibalista H1 pontjának
     javítása: az egyeztetés-státuszt NEM írja felül a terület-szabály.
     Egy ellentmondást nem lehet egy további szűkítő feltétellel feloldani; a
     modul ettől nem lesz magabiztosabb, hanem két nyitott kérdése lesz. */
  teruletSzabalyok: {
    ellentmondasEsSzuk: "Ehhez egy MÁSODIK szűk keresztmetszet is jön: a megadott terület a kezelt víz elhelyezését is kérdésessé teszi. Ez az ellentmondást nem oldja fel — két külön nyitott kérdés, és mindkettőt a helyszíni felmérés zárja le.",
    oldomedenceNemFer: "Két szempont húz ellentétes irányba: a használat az oldómedencés irány felé mutat, a rendelkezésre álló terület viszont az oldómedence szikkasztómezőjét nem engedi — az jellemzően a biológiai rendszer szivárogtatójának két-háromszorosa."
  },

  /* ------------------------------------------------ KIVITELEZÉSI FELTÉTELEK */
  /* `csak`: MELYIK KIMENETTÍPUSNÁL érvényes a feltétel (hibalista H4). A
     szabályok korábban csak a BEMENŐ válaszokhoz voltak kötve, a végeredmény
     típusához nem — ezért jelent meg a „kiemelt szivárogtató" olyan kimenetnél
     is, ahol egyáltalán nincs szivárogtató. Hiányzó `csak` = mindenhol
     érvényes. */
  feltetelek: {
    "kiemelt-szivarogtato": {
      cimke: "Kiemelt szivárogtató", jel: "csepp",
      /* KÉT KAPU, két külön állítás — mindkettő kell.

         `csak`   — melyik KIMENETTÍPUSNÁL jelenhet meg (a hibalista H4 kérése).
         `igenyel`— milyen TÉNYT feltételez. A „kiemelt szivárogtató" azt
                    feltételezi, hogy egyáltalán LESZ szivárogtató. Ahol a
                    kezelt víz elhelyezése maga a nyitott kérdés (szűk
                    terület), ott ezt nem állíthatjuk — akkor sem, ha a
                    kimenet egyébként határeset. Ez ugyanaz az elv, mint a
                    3.2.: nem állítunk olyat, ami mögé nem tudunk állni. */
      csak: ["termek", "egyeztetes"],
      igenyel: "szivarogtato",
      leiras: "A tisztított vizet a talajszint fölé emelt szivárogtatóban helyezzük el, hogy a rossz szivárgás vagy a magas talajvíz ne akadályozza a beszivárgást."
    },
    "specialis-rogzites": {
      cimke: "Speciális rögzítés", jel: "horgony",
      /* Ez MINDEN földbe kerülő tartályra érvényes — az üres tartályt a magas
         talajvíz kiemelheti, függetlenül attól, mi van benne. */
      leiras: "A tartályt a betonalaphoz rögzítjük, hogy a magas talajvíz ne emelhesse ki."
    },
    "gravitacios-megoldas": {
      cimke: "Külön műszaki megoldás a gravitációra", jel: "lejtes",
      leiras: "Ha a csőkivezetés mélysége és a terep miatt a gravitációs kialakítás nem működik, átemelés vagy módosított magassági kialakítás szükséges."
    }
  },

  /* -------------------------------------------------------- TISZTÁZANDÓK */
  /* `mindig: true` — a specifikáció 6. pontja szerint ezek KÖTELEZŐEN
     megjelennek, függetlenül a válaszoktól.

     HÁROM MEZŐ, NEM EGY (hibalista 6.3.). Egy nyitott kérdésekből álló lista
     olvasható úgy is, hogy „még nem tudsz dönteni" — és úgy is, hogy „itt a
     kész napirended a szakértői beszélgetéshez". A második változat teszi a
     konzultációt természetes következő lépéssé. Ehhez elemenként három dolog
     kell: MIT JELENT (`hogyan`), KI TUDJA MEGMONDANI (`ki`), és NAGYJÁBÓL
     MENNYI IDŐ (`ido`).

     ⚠️ Az `ido` mezők SZÁNDÉKOSAN ÜRESEK. Időtartamot a saját folyamatunkról
     csak a cég állíthat; amíg nincs jóváhagyott érték, a modul inkább nem mond
     semmit, mint hogy tippeljen. A felület az üres mezőt kihagyja — töltsd ki,
     és magától megjelenik. */
  /* A LISTA KERETEZÉSE (hibalista 6.3.). Egy nyitott kérdésekből álló lista
     olvasható úgy is, hogy „még nem tudsz dönteni". Ez az egy mondat teszi
     napirenddé — és a konzultációt természetes következő lépéssé. */
  tisztazandokBevezeto: "Ez nem hiánylista, hanem napirend: ezeket a pontokat a helyszíni felmérésen közösen tisztázzuk — döntenie egyikről sem most kell.",

  tisztazandok: {
    kut: {
      mindig: true, cimke: "Kút / telekhatár közelsége",
      hogyan: "A pontos védőtávolság nem adható meg egyetlen méterszámmal: a helyi adottságok és az engedélyezési feltételek együtt határozzák meg. Helyszíni felmérésen tisztázható.",
      ki: "A helyszíni felmérésen, a telek és a kút tényleges helyzete alapján.",
      ido: ""
    },
    szivarogtato: {
      mindig: true, cimke: "A szükséges szivárogtató mérete",
      hogyan: "A várható terheléstől, a talajszerkezettől és a talajvízszinttől függ. Ezért a felmérés adja meg, nem előre megadott méterszám.",
      ki: "A felmérés adatai alapján mi méretezzük — ez a tervezés része, nem Önre hárul.",
      ido: ""
    },
    terep: {
      mindig: true, cimke: "A csőkivezetés mélysége és a terep lejtése",
      hogyan: "Ez dönti el, működik-e a gravitációs kialakítás. A meglévő csőkivezetés helyszínen megnézhető.",
      ki: "Helyszínen, a meglévő csőkivezetésnél — együtt megnézzük.",
      ido: ""
    },
    talajviz: {
      cimke: "Pontos talajviszonyok",
      hogyan: "A talajvízszint helyszíni felméréssel egyértelműen megállapítható.",
      ki: "A helyszíni felmérésen.",
      ido: ""
    },
    talaj: {
      cimke: "A talaj szivárgóképessége",
      hogyan: "A talajszerkezet a helyszínen megnézhető; kétséges esetben szivárgási próba adja meg.",
      ki: "Helyszínen megnézhető; kétséges esetben szivárgási próbával.",
      ido: ""
    },
    terulet: {
      cimke: "Szabad terület a vízelhelyezéshez",
      hogyan: "A telken rendelkezésre álló összefüggő, beépítetlen terület a helyszínrajzról vagy a helyszínen megállapítható.",
      ki: "Helyszínrajzról vagy a helyszínen, közösen felmérve.",
      ido: ""
    },
    /* ⚠️ SZAKMAI DÖNTÉSRE VÁR (hibalista 3.4. és 9.). Hogy mi számít
       befogadónak (árok, csapadékvíz-elvezetés, élővíz), milyen engedélyezési
       feltételekkel, és mit lehet erről felelősséggel állítani a weboldalon —
       ez nincs eldöntve. Amíg nincs, a modul NEM KÉRDEZ rá: csak ott említi
       tisztázandóként, ahol a vízelhelyezés amúgy is a nyitott kérdés. */
    befogado: {
      cimke: "Van-e befogadó a közelben",
      hogyan: "Ha a kezelt víz helyben nem szivárogtatható el, a következő kérdés az, hogy van-e a közelben olyan befogadó, ahova elvezethető. Ennek feltételeit a helyi adottságok és az engedélyezés együtt határozzák meg.",
      ki: "A helyszíni felmérésen, a szomszédos vízelvezetés megnézésével.",
      ido: ""
    }
  },

  /* -------------------------------------------------------------- TERMÉKEK */
  termekek: {
    abclear: {
      nev: "A.B. Clear",
      rovid: "A használati mintázat alapján ez tűnik a legerősebb iránynak.",
      indoklas: "Az egész éves, egyenletes terhelés mellett az aktív biológiai tisztítás fenntartható: a baktériumkultúra folyamatosan táplálékhoz jut. Az iszapzsákos kialakítás miatt a rendszer szippantásmentes.",
      url: "megoldasok/ab-clear"
    },
    epureco: {
      nev: "Epureco oldómedence",
      rovid: "A használat időszakos mintázata alapján ez tűnik a legerősebb iránynak.",
      indoklas: "Az időszakos, szakaszos terhelést az oldómedence jól tűri: nincs benne aktív biológiai kultúra, amit fenn kellene tartani, és áramellátást sem igényel.",
      /* A specifikáció 6. pontja: Epureco esetén a kompromisszumot MINDIG ki
         kell mondani. Ez nem opcionális kiegészítés — és a hibalista 10. pontja
         szerint nem csak a kimenetben: már a KÁRTYÁN is, amint az irány
         megjelenik. Ha valaki három kérdésen át egy terméknevet lát, majd a
         végén kap egy fenntartást, az csalódás; ha a kompromisszum az első
         pillanattól ott van, az őszinteség. */
      kompromisszum: "Ez tisztítási szempontból kompromisszum: az egyszerűbb, terhelésingadozást jól tűrő működésért cserébe a tisztítás nagy része a talajban történik, alacsonyabb tisztítási teljesítménnyel, mint az A.B. Clear aktív biológiai tisztítása.",
      kompromisszumRovid: "Kompromisszummal: a tisztítás nagy része a talajban történik.",
      url: "megoldasok/epureco"
    },
    /* ⚠️ A SZÓTÁRBAN MARAD, DE A MODUL SOHA NEM VÁLASZTJA (hibalista H2, 3.2.).
       Zárt tárolót nem forgalmazunk, tehát nem lehet automatikus végkövetkeztetés
       — pláne nem egy laikus szemmértékén alapuló területbecslésből. Felmérés
       utáni lehetséges irányként a „vízelhelyezés kérdéses" kimenet záró
       mondata említi, őszintén. */
    zarttarolo: {
      nev: "Zárt tároló",
      rovid: "Felmérés utáni lehetséges irány, nem automatikus ítélet.",
      indoklas: "Ha a tisztított víz elhelyezésére sem helyben, sem befogadóba nincs mód, a keletkező szennyvizet gyűjteni és elszállíttatni kell. Ezt nem forgalmazzuk — de ha a felmérés ide vezet, megmondjuk, és megmondjuk azt is, mi a következő lépés.",
      url: "megoldasok/megoldastipusok-osszehasonlitasa"
    },
    egyeztetes: {
      nev: "Szakértői egyeztetés",
      rovid: "A válaszok két irányba húznak, ezért a modul nem nevez meg terméket.",
      indoklas: "Terméket ezért nem nevezünk meg.",
      /* A HATÁRESET-ÁG LEGFONTOSABB MONDATA (hibalista 4.3.). Megelőzi azt,
         hogy a látogató azt higgye, ő válaszolt rosszul, és visszamenjen
         „javítani". */
      megnyugtatas: "A helyzete összetettebb az átlagosnál — ez a leggyakoribb oka annak, hogy valaki rossz rendszert kap. Épp ezért nem tippelünk.",
      /* A telek-válaszok a határeset-ágon SEM vesznek kárba: kivitelezési
         feltételeket szabnak, amik mindkét lehetséges irányra érvényesek. */
      nyitvaCim: "Két irány maradt nyitva",
      nyitvaFeltetellel: "Amit a telek adottságairól tudunk, mindkettőre érvényes:",
      nyitvaZaro: "A nyitott kérdés az üzemeltetés — ezt kell személyesen átbeszélni.",
      url: "konzultacio"
    }
  },

  /* ══════════════════════════════════════════════════ KIMENETTÍPUSOK ═══════
     A HIBALISTA KÖZPONTI JAVASLATA (3.1.). A záró képernyő korábban egyetlen
     sablon volt; négy, egymástól érdemben eltérő kimenettípus van, és
     mindegyik MÁS fejlécet, MÁS blokkokat és MÁS következő lépést kíván.

     A blokkok (terméknév, kivitelezési feltételek, tisztázandók, ársáv-CTA)
     mindegyike KÜLÖN FELTÉTELLEL jelenik meg, nem alapértelmezésben.

       `fejlec`     — a záró képernyő és a mentett lap címe (H5: a fejléc nem
                      mondhatja, hogy „a javasolt megoldás", két sorral a
                      „nem lehetett eldönteni" fölött)
       `jel`        — a jelvény ne ígérjen terméket ott, ahol nincs
       `elsodleges` — a következő lépés gombja
       `arsav`      — `elsodleges` | `masodlagos` | `nincs` (H3: nem vezetünk
                      ársávbecslőre olyan megoldásnál, ami nem létezik)
       `blokkok`    — melyik tartalmi blokk jelenjen meg */
  kimenetek: {
    /* 1–2. KONKRÉT TERMÉK (A.B. Clear vagy Epureco). Az Epurecónál a
       kompromisszum kimondása kötelező — azt a `termekek` szintje adja. */
    termek: {
      fejlec: "A javasolt megoldás",
      jel: "csepp",
      elsodleges: { cimke: "Nézze meg, nagyságrendileg mibe kerülne", url: "#ai-dontestamogato" },
      arsav: "elsodleges",
      blokkok: ["termek", "feltetelek", "tisztazandok"]
    },
    /* 3. HATÁRESET / ELLENTMONDÁS. A modul kimondja, hogy nem tud dönteni —
       ez a hitelesség alapja, és a hibalista 10. pontja szerint meg kell
       őrizni. Az ársávbecslő itt MÁSODLAGOS: „mindkét irány nagyságrendje". */
    egyeztetes: {
      fejlec: "Nem dönthető el automatikusan",
      jel: "info",
      elsodleges: { cimke: "Kérek szakértői egyeztetést", url: "konzultacio#urlap" },
      arsav: "masodlagos",
      arsavCimke: "Mindkét irány nagyságrendje",
      blokkok: ["utkozes", "feltetelek", "tisztazandok"]
    },
    /* 4. VÍZELHELYEZÉS KÉRDÉSES. A kártya itt MEGFORDUL, nem magabiztosabb
       lesz. Ársávbecslő NEM jelenik meg: nincs mit árazni, amíg nem tudjuk,
       hova kerül a kezelt víz. A konverzió ezen az ágon a felmérés-kérés. */
    vizelhelyezes: {
      fejlec: "A vízelhelyezés a szűk keresztmetszet",
      jel: "figyelem",
      elsodleges: { cimke: "Kérek helyszíni felmérést", url: "konzultacio?mod=helyszini#urlap" },
      arsav: "nincs",
      blokkok: ["vizelhelyezes", "tisztazandok"],

      /* A 3.3. FEJEZET SZÖVEGE, szó szerint. A végkicsengés nem az, hogy „ezt
         nem mi csináljuk", hanem hogy „idáig elkísérünk, és megmondjuk, hova
         tovább". A modul eddig sem hazudott, és most sem szabad. */
      bevezeto: "A megadott terület alapján a szivárogtató elhelyezése kérdéses. Ez nem azt jelenti, hogy nincs megoldás — azt jelenti, hogy itt nem a technológia a döntő kérdés, hanem az, hova kerül a kezelt víz.",
      tisztazniCim: "Amit ezen a ponton tisztázni kell:",
      tisztazni: [
        "a ténylegesen felhasználható terület — a becsült és a felmérésen mért érték gyakran eltér",
        "van-e befogadó a közelben",
        "a talajszerkezet, ami a szükséges méretet meghatározza"
      ],
      zaro: "A felmérés adja meg, hogy van-e járható út a helyben történő elhelyezésre. Ha nincs, arról is őszintén beszélünk — zárt tárolót nem forgalmazunk, de megmondjuk, mi a következő lépés."
    }
  },

  /* ═══════════════════════════════════ AZ IRÁNY-KÁRTYA ÁLLAPOTAI (4.1.) ════
     A kártya korábban MEGFAGYOTT: a terméknév alatti mondat a 2/6-tól a 6/6-ig
     szó szerint azonos volt („…de a telek adottságai még pontosíthatják az
     ajánlást"). A végén ez pontatlan — a telek adottságai már pontosították.

     Helyette KÉTRÉSZES a kártya: STÁTUSZ + INDOKLÁS, és az indoklás minden
     válasz után lép. Mellékhaszon: ez egy specifikációs ellentmondást is rendez
     (S5). A specifikáció szerint az irány a használati szakasz három kérdése
     után jelenik meg, a valóságban viszont már az első válasz után ott a
     terméknév. Ha a BIZONYOSSÁG FOKA őszintén ki van írva, megjelenhet korán. */
  iranyAllapotok: {
    elozetes:     { cimke: "Előzetes irány",
                    szoveg: "A használat jellege ebbe mutat. {hatra} még pontosítja." },
    eldolt:       { cimke: "A technológia eldőlt",
                    szoveg: "A telek adottságai innentől a kivitelezés feltételeit szabják, nem a megoldást." },
    megerositve:  { cimke: "Megerősítve",
                    szoveg: "A telek nem szabott extra kivitelezési feltételt." },
    feltetellel:  { cimke: "Megerősítve, feltétellel",
                    szoveg: "A telek adottságai kivitelezési feltételt szabnak — lentebb látszik, melyiket." },
    ellentmondas: { cimke: "Nem dönthető el automatikusan", szoveg: "" },
    vizelhelyezes:{ cimke: "A vízelhelyezés kérdéses",
                    szoveg: "Itt nem a technológia a döntő kérdés, hanem az, hova kerül a kezelt víz." }
  },

  /* ----------------------------------------------------------- TOVÁBBLÉPÉS */
  /* A specifikáció 7. pontja: a záró képernyőn NEM kérünk kontaktadatot.
     Az ELSŐDLEGES lépés kimenettípusonként változik (lásd `kimenetek`); ezek a
     másodlagos hivatkozások mindenhol ott vannak. */
  tovabb: {
    arsav: { cimke: "Nézze meg, nagyságrendileg mibe kerülne", url: "#ai-dontestamogato" },
    masodlagos: [
      { cimke: "Kizáró és korlátozó feltételek", url: "megoldasok/kizaro-es-korlatozo-feltetelek" },
      { cimke: "A tisztított víz elszivárogtatása", url: "megoldasok/biologiai-telek-es-terhelesi-feltetelek" },
      { cimke: "Szakértői konzultáció", url: "konzultacio" }
    ]
  },

  /* ------------------------------------------------- RÉSZLEGES EREDMÉNY ---
     A hibalista 6.5. pontja. A modul már a harmadik kérdés után megmutatja az
     irányt — onnantól minden pillanatban van értelmezhető eredmény. Aki a
     negyediknél abbahagyja, eddig SEMMIT nem kapott. Ez a gomb a negyedik
     kérdéstől jelenik meg: lezárja a folyamatot azzal, ami eddig megvan, és a
     megválaszolatlan kérdések automatikusan a tisztázandók közé kerülnek. */
  reszleges: {
    gomb: "Elég ennyi — lássuk az eredményt",
    magyarazat: "A telek adottságai a megoldáson már nem változtatnak, csak kivitelezési feltételeket szabhatnak hozzá. Amit nem adott meg, az a tisztázandók közé kerül."
  }
};
