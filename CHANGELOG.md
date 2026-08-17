<p align="center">
  <img src="./.github/banner.png" alt="ÖkoTech Home — otthoni biológiai szennyvíztisztítás" width="100%">
</p>

<h1 align="center">Változásnapló — okotechhome-web2 <em>(Test2)</em></h1>

<p align="center">
  <img src="https://img.shields.io/badge/verzi%C3%B3-0.05.00-36C5E6?style=flat-square" alt="verzió 0.05.00">
  <img src="https://img.shields.io/badge/Keep%20a%20Changelog-1.1.0-C9A24A?style=flat-square" alt="Keep a Changelog 1.1.0">
  <img src="https://img.shields.io/badge/SemVer-2.0.0%20(padded)-1572B6?style=flat-square" alt="SemVer 2.0.0 padded">
  <img src="https://img.shields.io/badge/kiad%C3%A1sok-5-6f42c1?style=flat-square" alt="5 kiadás">
</p>

---

A napló formátuma a [Keep a Changelog 1.1.0](https://keepachangelog.com/hu/1.1.0/) ajánlást követi,
a verziószámozás a [Szemantikus Verziózás 2.0.0](https://semver.org/lang/hu/) szabályait —
**feltöltött írásmóddal** (`MINOR` és `PATCH` két számjegyen). A projektre szabott értelmezést
lásd: [`VERSIONING.md`](./VERSIONING.md).

**Hatókör:** ez a napló az `okotechhome-web2` repó (Test2 munkaterület) teljes történetét fedi le
az inicializálástól kezdve, **tételesen, commitonként**. A Test1 (`okotechhome-web`) története
külön naplóban él, és a két verzió-idővonal **független**.

**Kategóriák:** `Hozzáadva` · `Módosítva` · `Javítva` · `Eltávolítva` · `Elavult` · `Biztonság`

**Jelölések:** `§` = a főoldal szekciója · `OFC` = AI ajánlat-összehasonlító (offer comparison) ·
`AIDT` = AI döntéstámogató · a `( )` zárójelben álló hét karakteres kód a commit rövid hash-e.

---

## [Nem kiadott]

**Szippantási díj kalkulátor** — új modul-oldal a `/szippantasi-dij-kalkulator`
útvonalon, a megrendelői brief (Anna) alapján. A brief három díjszabás-szerkezetet
ír le; a modul **egyetlen képlettel** kezeli mindhármat, és megmutatja azt a
tételt, amit a látogató kifizet, de nem szállítanak el érte semmit.

### Hozzáadva

- **`/szippantasi-dij-kalkulator` — modul-oldal.** Élő kalkulátor (vármegye,
  település, éves alkalomszám, m³/alkalom, kiszállási díj, ürítési díj,
  minimumdíj, a minimumdíjban foglalt m³, kocsi űrtartalma, távolságarányos díj,
  egyéb), animált költségsáv tételes jelmagyarázattal, tartálymérő ábra és
  vármegyei csempetérkép. Nyolc szekció, hat GYIK-tétel `FAQPage` jelöléssel.
  Generátor: `scripts/oldalgyartas/szippantasi_kalkulator.py`.
- **Egy képlet mind a három díjszabásra.** `elszámolt m³ = max(elszállított,
  foglalt)` · `alapdíj = max(minimumdíj, ürítési díj × elszámolt m³)` ·
  `alkalmi díj = kiszállás + alapdíj + távolság + egyéb`. Lefedi a „csak
  mennyiség szerint", a „minimumdíj alsó korlátként" és a „a minimumdíj X m³-t
  tartalmaz" esetet — beleértve azt, amikor a **teljes kocsit** ki kell fizetni
  egyetlen köbméterért. A látogatónak nem kell kategóriába sorolnia a számláját.
- **Minimum-felár mint önálló kimenet.** Az az összeg, amit a látogató kifizet,
  de nem visznek el érte semmit — alkalmanként és évesre vetítve is, azzal
  együtt, hogy teltebb tartállyal mennyi lenne a fajlagos díj.
- **Települési díjadatbázis — üresen indul.** `assets/data/szippantas-konfig.js`:
  a `dijak` tömb szándékosan üres, mert egyetlen település díjszabását sem
  ismerjük ellenőrzött forrásból. A `0` valódi érték (nincs kiszállási díj), a
  `null` azt jelenti, hogy nem tudjuk — a kettő nem cserélhető fel.
- **Csempetérkép — 19 vármegye + Budapest.** Nem földrajzi térkép: azonos méretű
  csempék a valós kelet–nyugati és észak–déli sorrendben, mert pontos
  határvonalhoz nincs hiteles térképi forrásunk. A rácshely a konfigban él.
  Görgetésvezérelt animációval épül fel északnyugatról délkelet felé
  (`animation-timeline: view()`).
- **`api/szippantasi-dij` — díjbeküldő végpont.** Zárt vármegye- és
  forrás-értékkészlet, elgépelés-szűrő felső korlátok, „12 000 Ft"-ként másolt
  értékek normalizálása. Az adat **e-mailben** érkezik, és emberi ellenőrzés után
  kerül a konfigba — az automatikus felvétel egy elgépelt nullát azonnal minden
  látogatónak kiszolgálna. Nevet nem kér; e-mail-címet csak hozzájárulással.
- **Rajzolt modul-hero (`.szip-hero`) — jelzett eltérés.** A lap nem fényképes
  fejlécet kap: a rendelkezésre álló szippantásos felvételen ott a
  designrendszer 4.4-ben leírt **függőleges varrat**, a lap pedig eszköz, nem
  tartalom. A fejlécben ugyanaz a tartályábra áll, amit a kalkulátor is használ.
  Következmény: nincs fejléckép, tehát nincs `preload` — az LCP-elem a főcím.

### Módosítva

- **`app.css`** két új komponensblokkal (5.21 kalkulátor, 5.22 modul-hero),
  saját komponens-tokenekkel, mind újradeklarálva a `[data-theme="dark"]`
  blokkban. Cache-busting: `app.css?v=136` mind a 120 lapon.
- **`oldomedence-szippantas-es-karbantartas`** „Következő lépés" panelje a
  kalkulátorra is hivatkozik — ez a lap egyetlen bejövő hivatkozása, mert a
  szlug nincs a sitemapban, és menüpontot nem találunk ki hozzá.
- **`api/config.example.php`**: új `cimzettek['szippantasi-dij']` kulcs. A
  végpontnak van tartaléka, tehát a beküldés akkor sem vész el, ha a kulcs
  lemarad az éles configból.

### Vizuális átdolgozás (megrendelői visszajelzés nyomán)

- **A járműrajz újraírva.** Vezetőfülke ferde szélvédővel és ajtóvonallal, alváz,
  tartálybölcsők, domború hátsó véglap, bordázat, búvónyílás és szellőzőszelep,
  vákuumpumpa-ház, küllős tömlődob, alsó ürítőcsonk, sárvédők, küllős kerekek,
  gradienses talajárnyék. Egyetlen `--rajz-kontraszt` tokenből kevert ötfokú tónuslépcső
  — a rajz így annyi mélységet kap, mint egy háromtónusú illusztráció, de a paletta
  egyetlen tokenből jön, és követi a témaváltást.
- **A méretválasztó, az ábra és az animáció egy blokk.** Külön állva a járműméret
  átállítása nem látszott a rajzon. Most a rajz **vízszintesen nyúlik** az űrtartalommal
  (a fülke, a hátsó szerelvény és a kerekek ellenskálázással tartják az arányukat), és a
  tartály tetején **köbméterenként egy vonalka** fut — nyolc osztás nyolc köbmétert jelent.
- **Új leolvasás: tartálykihasználás.** Ez az egyetlen szám, amit a járműméret önmagában
  mozgat; a blokk lábjegyzete kimondja, hogy a díjat a foglalt mennyiség és az ürítési díj
  adja, és megnevezi azt a két esetet, amikor a járműméret mégis számít.
- **A fejléc animációja öt fázisú:** behajtás forgó kerekekkel és sebességvonalakkal →
  a kiszámlázott mennyiség felfut → az elszállított mennyiség felfut → a zöld réteg
  csillapodva hármat lötyög → a jelölők lefutnak; ezután 7 másodpercenként fénypászma.
- **Mezőcsoport-cím pirulában:** a `fieldset` felirata félkörös végű pirula, és a keret a
  pirula tengelyvonalában fut bele a két oldalába. A natív `legend` keretkivágása ezt nem
  tudja — a felirat ezért abszolút pozíciójú, saját, átlátszatlan háttérrel.
- **A figyelmeztetés adatblokk lett:** négy szám egy tömött bekezdés helyett cím + négy
  adatcella.
- **A jelölővonal láthatóbb és beszédesebb:** két réteg (tömör alsó a felület színével +
  sötét szaggatott fölötte), lefelé mutató gombostűfej korong helyett, és a műszeren a
  saját értéke is ki van írva. Nulla foglalt mennyiségnél a jelölés eltűnik — ott a
  tartály bal szélén állt, magyarázat nélkül.
- **Javított rajzhibák** (nagyításban derültek ki): a sárvédő íve keresztbe vágta a
  tartályt · az alváz beleolvadt a burkolatba, ezért a jármű darabokra esett · a tartály
  alsó árnyéka éles vízszintes vonalat húzott, ami folyadékszintnek látszott · a
  búvónyílás a „KIFIZETI" felirat alá esett. A feliratok azóta halót viselnek
  (`paint-order: stroke fill`).

### Designrendszer

- **Új szemantikus token: `--text-on-dark-soft`** — a sötét felület hiányzó középső
  szövegfoka. Világos felületen három szövegszint van, sötét felületen eddig csak kettő
  volt, ezért minden hivatkozás és folyó szöveg a majdnem fehér Stardustra került. A
  láblécben ez öt hasábnyi, maximális kontrasztú szöveget jelentett, ami optikailag
  vastagabbnak és „izzónak" látszott (irradiáció). Az új fok 13,3:1-ről **10,2:1**-re
  viszi a kontrasztot — AAA-n belül marad. Alkalmazva: a lábléc hasáblistái.
  Címre és `:hover`-re marad a teljes világosság.
- **`-moz-osx-font-smoothing: grayscale`** a `body`-n, a meglévő WebKit-es párja mellé:
  enélkül ugyanaz a lap más betűvastagságot mutatott Firefoxban és Chrome-ban macOS alatt.
- **A lábléc hasáblistái `line-height: 1.55`-öt kapnak** — a kétsorosra törő tételek
  sötét alapon a szűkebb sorközzel vibrálni látszottak.
- Cache-busting: `app.css?v=137` mind a 120 lapon.

### Akadálymentesség

- **Egyetlen, késleltetett élő régió.** A látható számokon nincs `aria-live`:
  gépelés közben minden leütésnél újra felolvasnák magukat. Helyettük egy rejtett
  `role="status"` régió mondja el az eredményt, 900 ms-mal az utolsó változás
  után, egyetlen mondatban.
- A csempék `<button>`-ok `aria-pressed`-del (szűrők, nem navigáció), és a
  képernyőolvasó a **teljes** vármegyenevet kapja, nem a rövidítést.
- 640px alatt a csempetérkép vízszintesen görgethető; a mezősorok `subgrid`-del
  igazodnak, hogy a kétsoros címke ne lökje lépcsőbe a szomszéd oszlopot.

### Amire adat kell — kérni

- **Települési díjszabások** a `dijak` tömbhöz (számla, közszolgáltatói
  ártáblázat vagy önkormányzati rendelet alapján). Enélkül a térkép üres marad.
- **A példaértékek jóváhagyása** (`peldaDijak`): jelenleg a brief „Példa"
  oszlopa. A felület végig jelzi, hogy példa, de a nagyságrendet a cégnek meg
  kell erősítenie.

---

## [0.05.00] — 2026-08-11

Öko **a lapok tényleges mondataiból** válaszol: teljes szöveges keresés
(RAG) váltja fel a címindexet, és három kódszintű réteg zárja ki a
kitalálást. A **helyzetem** és a **megoldások** szakasz három csatolt
anyagból bővült — köztük a `147/2010. (IV. 29.) Korm. rendelet` ellenőrzött
jogi alapjával, amely egy publikálást blokkoló adathiányt oldott fel.

### Hozzáadva

- **Szövegindex — Öko a lapok mondataiból válaszol.** `kalauz-szoveg.json`
  (857 részlet, 512 ezer karakter): a `<h2 id>`-k mentén darabolt
  szakaszszöveg. Kérdésenként a nyolc legjobban illő részlet **teljes
  terjedelemben** kerül a promptba, azzal, hogy azon túl ne állítson semmit.
  Kimarad az SVG-k `path` adata, a képernyőolvasónak szánt felirat, a
  morzsamenü és a belső jegyzet. Mért költség: 1,8 ms betöltés, 8 ms
  pontozás, 4 MB memória, ~2 450 token kérésenként. (`879c362`)
- **A megrendelésig vezető hét lépés** a promptban: tájékozódás → telekadatok
  → terhelés → megoldástípus → konzultáció és felmérés → tervezés és vízjogi
  engedély → kivitelezés. Minden válasznak el kell helyeznie a látogatót az
  úton, jeleznie a **függőségeket** (nincs ár felmérés előtt, nincs engedély
  telekadat nélkül), és a felkínált kérdések közül legalább egynek előre kell
  vinnie. (`8861031`)
- **Öko szakmai tudása az új tartalmakhoz:** a jogi kapu két feltétele, a
  vízminőségi paraméterek jelentése, a bizonyítékok nem egyenértékűsége, a
  magas talajvíz mint telepítési kérdés, a „nem tudom" négy fokozata, a
  nyaraló három esete. Két új laptéma-csomag (`ab-clear`, közcsatorna).
  (`c32281d`)
- **Jogi alap a közcsatorna-lapon.** A rendelet két nevesített feltétele —
  a szennyvízelvezető mű **műszaki elérhetősége** és a **tisztítótelepi
  kapacitás** —, és a következmény: ha mindkettő fennáll, új berendezés nem
  telepíthető. Dátumozva (2026-08-09) és forrásra hivatkozva. Két új
  táblázat, a kétkapus sorrend, négy GYIK. (`cf1d1d1`)
- **A „nincs közcsatorna" fejezet hiányzó fele:** ötelemű fogalomtár, a hat
  döntés előtti kérdés, „még nem tudja → honnan derül ki → mi a lépés"
  tábla, a hat valódi költségelem, nyolc azonos vizsgálati szempont, a négy
  kimenet **irányként, nem terméknévként**, az adatbiztonság négy fokozata,
  az eszkalációs határ a projektindítón. (`cf1d1d1`)
- **A biológiai HUB bizonyítékai:** a folyamat öt lépésben, az eleveniszap
  mint élő közeg, „Mit bizonyítanak a műszaki vizsgálatok?" (EN 12566-3,
  akkreditált vizsgálat, VITUKI — értékek nélkül, indoklással), az „nem
  mindenkinek jó" pozicionálás, laikus fogalomtár a kibocsátási
  paraméterekhez, a szezonalitás három esete, négy GYIK. (`db9d4a8`)
- **A.B.Clear: bizonyíték-hierarchia és garancia-elv.** Öt bizonyítéktípus,
  mindegyik mást igazol; a piacvezetői állítás elvetése indoklással. A
  garancia négy kérdéssel megválaszolva évszám helyett, a feltételek az
  írásos ajánlatban. Négy GYIK. (`4986a7b`)
- **Nyúló munkatér a kalauzpanelben:** az első kérdéstől a panel szélesebb
  és magasabb, a lépéskísérő egysoros fejlécre csukódik, és a fejlécre
  kattintva újranyitható. (`7090b9f`)

### Biztonság

- **A tiltólista kódban is, nem csak a promptban.** Mintaillesztés méri a
  kész választ: ár, kW/kWh, m³/nap, mg/l, m², LE, százalék és garanciaidő nem
  hagyhatja el a végpontot. Találatkor **a találatok megmaradnak**, csak a
  mondat cserélődik őszintére. Átmegy a jogszabály- és szabványszám, a
  telefonszám, a lap- és lépésszám. 14 egységteszttel ellenőrizve. (`c5581b1`)

### Módosítva

- **A naptár dátumsora oszlopfejléc lett:** a napnév viszi a hangsúlyt, a
  dátum halványabb kísérő, vékony vonal zárja le. A beküldött címke
  változatlan — saját változóból épül, nem a DOM-ból olvasva. (`b1fc995`)
- **A tartalomindex csak a `<main>`-ből épül**, laponként 14 szakaszig: a
  lábléc hasábcímei tartalmi szakaszként kerültek be, és a nyolcas korlát a
  bővebb lapok végét levágta. 943 felhígított helyett 686 valódi szakasz.
  (`cf1d1d1`)

### Javítva

- **26 üres címsor 24 lapon.** `<h2 id="-cim"></h2>` — a cím a fölötte álló
  eyebrow-ba csúszott, minden előfordulás ugyanazt az id-t viselte, a
  dokumentumszerkezetben lyuk maradt, és Öko indexe nem látta ezeket a
  szakaszokat. Mind megkapta a valódi címét és egyedi horgonyát. (`db9d4a8`)
- **A varázsló mezősúgói nem jutottak el Ökóhoz.** A hatlépéses űrlap
  egyetlen `<h2>` szakasz, a szakaszok pedig 1800 karakternél **csonkultak**
  — a 16 súgó fele, a jogi szöveg és az utolsó lapok mezői ki sem kerültek az
  indexbe. Mondathatáron darabolunk: a lap 1 csonka részből 4 teljes lett,
  csonkolt szakasz sehol nem maradt (17 volt). (`5f2f494`)
- **Két magyar-specifikus keresési hiba.** Ékezet: a toldalékolás elviszi a
  hosszú magánhangzót („kút" → „kutat"), ezért a pontozás ott hasalt el, ahol
  a látogató máshogy fogalmaz — most ékezet nélkül fut mindkét oldalon.
  Rövid tövek: a hatbetűs csonkolás elromlik, ha a tő rövidebb a ragozott
  alaknál — a Kút és védőtávolság lap **egyáltalán nem jött elő**. Kettős tő
  (hosszú teljes, rövid 0,7 súllyal), a zajt az IDF fogja vissza. Top-8
  találat tíz kérdésen: 9/10 → **10/10**. (`5f2f494`)
- **A keresés a hosszú szakaszokat favorizálta** — „mit jelent a
  csúcsterhelés?" a főoldal *véleményeire* talált. Ritkasági súly (IDF) és
  hossznormalizálás; hat próbakérdés mind a helyes témalapra ér. (`879c362`)
- **A „megmutatom, hol keresd" némán kimaradhatott:** ha a modell az aktuális
  lapot horgony nélkül adta vissza, a kliensnek nem volt mit kiemelnie. A
  végpont ilyenkor a kérdéshez legjobban illő szakasz horgonyát pótolja. A
  rámutató kéz a görgetés **végét** várja meg (`scrollend`), nem félúton mér.
  (`8861031`)
- **Az üres visszajelzőmező zöld sávot festett** az űrlapok alá. `:empty`
  állapotban a dobozdíszek lekerülnek — nem `display:none`, mert az kivenné
  az `aria-live` régiót a fából. Mérve: 0 px üresen, 58 px szöveggel.
  (`ba96b34`)
- **Négy lap törött horgonyra mutatott** (`#dontestamogato`, miközben a
  főoldalon `#ai-dontestamogato` áll). (`cf1d1d1`)

---

## [0.04.00] — 2026-08-10

Öko **idegenvezetővé** lép elő: minden hero-s lapon magától nyílik, laptémák
szerint készül fel, láthatóan vonul a fülre, és a fül vissza is kérdez. A
konzultációkérő **hülyebiztos** lett: lebegő mezősúgók, mezőnél maradó magyar
hibaüzenetek, gazdagabb haladásjelző. Az AI-végpontok **webhelyszintű napi
keretet** kaptak a kreditégetés ellen.

### Hozzáadva

- **16 lebegő mezősúgó a varázslóban** — minden kényes mezőnél „?": mit írjon be,
  és miért kérdezzük. Tisztán CSS (hover + fókusz), JS nélkül is működik; szűk
  kijelzőn a sorban nyílik ki, nem lebeg. (`86a1318`)
- **Mezőnél maradó hibaüzenetek** a natív böngészőbuborék helyett: magyarul, a
  mező dobozán, magától tűnik el javításkor; a csoport egyet ráz, az első hibához
  görgetünk. Beküldés előtt a **teljes űrlap** újraellenőrzése — visszatöltött
  vázlatnál visszaugrik az első hiányos lapra. (`86a1318`)
- **Öko magától nyílik** — a főoldalon és minden hero-s lapon a fejléckép felének
  kigördülésekor, a konzultációkérőn betöltéskor, fókuszlopás nélkül. Aki nem
  görget, annál 20 mp után csak a figura jelenik meg. (`86a1318`, `1b735b9`)
- **Laptémák útvonal szerint** — a köszönés, a belépő kérdések és a fül kérdései
  a webhely szakaszához igazodnak (helyzetem / megoldások / előkészítés /
  eredmények / tudástár). (`1b735b9`)
- **A fül jelez és kérdez** — ~40 mp-enként előrelép-billen-pislant, az első két
  alkalommal a lap témájában kérdez a fül melletti buborékban; a buborékra
  kattintva nyílik a panel, az X a munkamenetre elnémítja. (`1b735b9`)
- **Laponkénti javasolt kérdések a kísérőben** — a varázsló mind a hat lapjához
  saját kérdés-chipek, lapváltáskor cserélődnek. (`86a1318`)
- **Öko mezőről mezőre ismeri az űrlapot** — a `kalauz.php` urlap-módú promptja
  a hat lap minden mezőjét, példaértékeit és kitöltési szabályait tartalmazza,
  a kliens a lépésszámot is küldi. (`86a1318`)
- **A végpont tudja, melyik lapon áll a látogató** — az aktuális lap bekerül a
  katalógusba, és ha a válasz ott van, első találatként, horgonnyal jön vissza,
  amit a felület helyben kiemel. (`1b735b9`)

### Biztonság

- **Webhelyszintű napi AI-keret** (`OthVedelem::napiKeret`, zárolt fájlalapú
  számláló): az IP-nkénti korlátot proxylistával meg lehet kerülni, a napi
  plafont nem. Kalauz + kitöltéssegéd + beküldési brief közösen 400 hívás/nap,
  az ajánlat-elemzés külön 60/nap (`ai.napi_keret`, `ai.napi_keret_elemzes`).
  Betelte után a kalauz elköszön a napra, a segéd kézi kitöltést ajánl, a
  konzultációkérés **AI nélkül is kimegy** — megkeresés nem vész el. (`f9ba97c`)
- **Prompt-injection őr** a kalauz promptjában: a látogató szövege adat, nem
  utasítás — szabálymódosító, utasítás-kicsalogató kérés visszaterelést kap. (`f9ba97c`)

### Módosítva

- **Zárva = fül, mindenhol**: az Escape, a fejléc X-e és a fül kattintása
  ugyanoda vezet — Öko a jobb szél közepén marad. A sarok csak az érkezés
  helye. (`8903c9c`)
- **A bezárás hatóköre egy lapnézet** — volt munkamenet-szintű, de élesben egy
  korai bezárás az egész látogatásra elnémította a kalauzt („Öko kikapcsolt").
  A következő lapon újra alapból aktív. (`8d01916`)
- **Látható kivonulás**: a panel a fül felé húz össze, a fül nyugtázza —
  előrelép, megbillen, pislant. Mobilon az alsó lap lefelé süllyed. (`1b735b9`)
- **Nagyobb kártyaikonok** a varázslóban (32/16 → 48/24, vékonyabb vonal), a
  kijelölt kártyán zöldre töltődnek. (`8d01916`)
- **Gazdagabb haladásjelző**: 40-es körök, gyűrűs-dobbanó aktív lépés, berajzolt
  pipa a készeken, vastagabb sín zölden végigfutó kitöltéssel. (`86a1318`, `8d01916`)
- A fejlesztő megnevezése egységesen **eSystem-Integration Kft. (eSI Kft.)**. (`61a45b1`)

### Javítva

- **A panel képileg soha nem csukódott be** — a `.oko-panel{display:flex}`
  felülírta a `hidden` attribútumot, a csukó gombok csak az állapotot állították.
  Egy sor zárja: `.oko-panel[hidden]{display:none}`. Ez volt a visszatérő „nem
  megy a becsukás" panasz valódi oka. (`8903c9c`)
- **Cache-beragadás élesben**: a `kalauz.js` a kitett `?v=25` után is változott,
  így a látogatók egy évig a régi JS-t kapták; a `jelentes.html` őskori
  `app.css?v=82`-t kért. Teljes verzióléptetés mind a 119 lapon. (`8903c9c`)
- A lépcső körei átütöttek a mezősúgó lebegő buborékán (halmozási kontextus a
  lépéselemeken), és egy `background:` shorthand némán kilőtte a sín kitöltési
  animációját. (`86a1318`, `8d01916`)
- **Sötét témás hibaszínek**: a világos témás mélyvörös szöveg és rózsaszín
  mezőháttér sötét alapon olvashatatlan volt — saját `--danger-*` tokenek. (`86a1318`)

---

## [0.03.00] — 2026-08-09

Az **Öko kalauz** (AI-alapú kísérő minden lapon), a **konzultációkérő varázsló**
AI-támogatással, a fejlécképek teljes újragenerálása témánként, és az élő
Google-térkép.

### Hozzáadva

- **Öko — AI-alapú kalauz minden lapon.** Kis figura a jobb alsó sarokban, aki
  megkeresi a kérdésre a választ a webhely tartalmában, megmondja melyik lapon és
  melyik szakaszban van, és **oda is viszi**: a lap többi része elhalványul és
  elmosódik egy fedőréteg alatt, a megtalált szakasz élesen marad, egy rajzolt kéz
  pedig rámutat. A kiemelés hét másodperc után, kattintásra vagy `Esc`-re elenged.
  A figura maga a termék: az A.B.Clear tartály sziluettje, szemekkel — bordázott
  test, kúpos tető, narancs csonkok. Pislog, a pupillái a kurzort követik (minden
  példány a saját középpontjából), és rákérdezéskor billeg. (`86a8d5e`, `8da69bc`,
  `ceb2726`, `1ddd7e0`, `b198053`)
- **Öko három üzemmódja.** Az üzemmódot a `<body data-kalauz-mod>` mondja meg.
  Alapértelmezésben tartalomban igazít el; a konzultációkérőn nem terel el, hanem a
  kitöltésnél segít; az ajánlat-összehasonlítási jelentésen a saját eredményét
  magyarázza. Minden módnak saját nyitó ajánlásai, súgószövege és példakérdései
  vannak. (`86a8d5e`, `e861c5a`)
- **Öko párbeszédvezetése.** Nyitáskor három kattintható belépőt kínál, mert a
  látogatók többsége nem tudja, mit kérdezzen egy segédtől. Minden válasz alatt
  két-három továbbkérdés jelenik meg a látogató saját hangján — ezt a séma
  **kötelezővé** teszi, mert az a segéd, amelyik válaszol és elhallgat, pont a
  megoldandó probléma. Hat forduló megy vissza a modellhez, így nem kell
  megismételni, amit a látogató már elmondott. (`e861c5a`)
- **Öko fül-üzemmódja.** A panel bezárása nem tünteti el a segédet: Öko a jobb
  képernyőszél közepére húzódik félig kilógó fülként, `position:fixed`, tehát
  görgetésre sem mozdul. Egy koppintás visszahozza. (`80f0335`, `d700350`,
  `b198053`)
- **Konzultációkérő varázsló — `/konzultacio`.** Hat lépés: ki keres megoldást
  (magánszemély, vállalkozás szegmenssel, önkormányzat, tervező), hol tart a projekt,
  az ingatlan és a terhelés, szabad szöveges leírás, a konzultáció módja
  időpont-preferenciákkal, végül az elérhetőség és a jogi hozzájárulások.
  JS nélkül is teljes értékű: minden lap egyszerre látszik, a natív ellenőrzés
  működik, és egyetlen POST megy a végpontra. (`049e76d`)
- **Időpont-preferencia, nem foglalás.** A látogató naptárrácsból legfeljebb három
  sávot jelöl, és egyet e-mailben igazolunk vissza. Nincs külső naptárfiók, nincs
  OAuth, és nem keletkezhet ütköző foglalás. A kijelölt sávok abba a szöveges mezőbe
  íródnak, amit a JS nélküli út is használ — egyetlen igazság megy a szerverre.
  (`049e76d`)
- **AI-kitöltéssegéd.** A szabad szöveges leírásból kényszerített eszközhívással
  kiolvassa az ingatlantípust, a létszámot, a projektszakaszt és a telekadatokat, és
  beírja őket — **kizárólag üres mezőkbe**, hogy a látogató válaszát soha ne írja
  felül a gép. A modell kimenete bemenetnek számít: az értékkészletet a szerver
  újraellenőrzi. (`049e76d`)
- **AI szakmai brief és személyre szabott visszaigazolás.** Beküldéskor két hívás
  fut: az egyik nekünk ír előminősítést, hiánylistát és kockázatokat, a másik a
  látogató visszaigazolásába fogalmazza meg, mit érdemes a konzultációig
  előkészítenie. Mindkettő elhagyható — ha az API nem érhető el, a levelek nélkülük
  mennek ki. (`049e76d`)
- **Lépéskísérő a varázslón.** Öko panelje zöld keretet kap, és a társalgás fölött
  egy blokk követi a lépéseket: mit várunk azon a lapon, egy konkrét példa, és mit
  tud automatikusan kitölteni. A varázsló eseménnyel szól a lapváltásról, így a két
  szkript egymás nélkül is működik. (`8da69bc`)
- **Tartalomindex a kiadott lapokból.** A `scripts/kalauz-index.py` 118 lapból és 943
  horgonyozott szakaszból épít katalógust. Öko **csak ebből választhat** találatot: a
  séma útvonalat fogad el, és a végpont a válasz URL-jét, címét és horgonyát még
  egyszer az indexhez méri. Kitalált hivatkozás így nem juthat ki. (`86a8d5e`)
- **Élő Google-térkép a kapcsolat oldalon.** A kulccsal a beágyazott keret helyére
  valódi Maps JavaScript API kerül, a logós jelölés valódi térképjelölővé válik, a
  színezés pedig a designrendszer tokenjeiből jön — és a lap témájával együtt vált.
  (`bae51a3`, `ed3e0ea`)
- **Kapcsolat menüpont a főmenüben.** A fejléc CTA a konzultációkérőre mutat; a
  kapcsolat ezért önálló menüpontot kapott. Aki csak kérdezni akar, annak is kell út.
  (`ed3e0ea`)

### Módosítva

- **Mind a 63 fejléckép újragenerálva, témánként.** Tizennyolc kép szolgált ki 116
  oldalt, ezért a legtöbb lapon nem a saját témája állt: az éttermek oldalán
  szippantóautó, a cookie-tájékoztatón naplementés falu. Most 63 kép / 116 oldal,
  átlag 1,8 oldal képenként, és 33 kép egyetlen oldalt szolgál. Minden kép a
  `alapkepek/` könyvtár referenciáival készült — modern házak, valódi A.B.Clear és
  Épureco egységek, kitalált műszaki tartalom nélkül. (`c4d4693`, `95a644c`)
- **Egy fejléckép — egy alt.** Ugyanaz a fotó korábban kilenc különböző leírást
  kapott, jórészt olyan képről, ami sosem volt ott. (`c4d4693`, `95a644c`)
- **Rövidebb megamenü-címkék.** Három címke három-négy sorba tört a 157 képpontos
  oszlopban. A menücímke navigáció, nem cím: a teljes mondat az oldal H1-ében, a
  morzsamenüben és a JSON-LD-ben maradt. Most 14 címke egy sor, 4 kettő. (`a91aa3a`)

### Javítva

- **A térkép nem üresedik ki.** Hitelesítési hiba (lejárt kulcs, kimerült kvóta,
  hiányzó domain a referrer-korlátozásból) nem betöltési hiba: a fájl megérkezik, a
  térkép felépül, csempe viszont nem jön. A `tilesloaded` az egyetlen megbízható jel;
  ha hat másodpercen belül nem érkezik, a beágyazott keret visszatér. (`bae51a3`)
- **A folyamatsáv vonala átütött a korongokon** sötét témában. Két oka volt: a
  rétegsorrend a színekre volt bízva, és a hátralévő lépések `opacity`-vel
  halványodtak — az pedig a hátteret is áttetszővé teszi. (`1b3a780`, `239e85e`)
- **Mondaton belüli hivatkozás.** A `.text-link` önálló hivatkozásnak készült (44
  képpontos érintőcél, saját betűméret); mondat közepén szétfeszítette a sorközt. Az
  új `.szoveg-link` örökli a méretet. (`ed3e0ea`)
- **Öko gombjai kattinthatók.** A kilógó fej rátakart a záró gombra és elnyelte az
  egeret; a kezelő pedig egy korábbi, csendben dobott hiba miatt nem is épült fel.
  (`ad38bab`, `5f3ec71`, `b198053`)

## [0.02.00] — 2026-08-08

A főoldal fejléce és 1–5. szekciója a designrendszer-implementációval, a háromszintű
megamenü, a témaváltó, a sitemap szerinti aloldalak (118 oldal), a jogi réteg, és az
ajánlat-összehasonlító teljes jelentés-kimenete.

**VISSZAÁLLÁSI PONT.** Ez a kiadás a következő designfeldolgozás előtti utolsó stabil
állapot. Ha a folytatás félresikerül, ide lehet visszaállni:
`git checkout v0.02.00` — a csomag pedig a `_files/` alatt van.

### Hozzáadva

- **Háromszintű megamenü, egyetlen forrásból.** A menü szerkezete
  `scripts/oldalgyartas/fejlec.py`-ban adatként él, és onnan kerül mind a 118 oldalba —
  eddig a `sablon.py` egy meglévő aloldalból emelte ki, ezért csak kézi szerkesztéssel
  volt módosítható. A panel a navigációs blokkhoz igazodik, nem az egyes menüponthoz:
  1280 képpontos ablakban a középső menüponthoz kötve se balra, se jobbra nem férne el.
  A nyitó gombon ülő csúcs mondja meg, melyikből nyílt. (`92e93fd`, `4f44d74`)
- **Világos/sötét témaváltó a fejlécben.** Csúszkakapcsoló, nap és hold jellel. A témát a
  `<html data-theme>` hordozza, amit a `tema.js` ír ki — ez az **egyetlen halasztás
  nélkül** töltődő szkript, különben minden oldalbetöltéskor felvillanna a világos oldal.
  Első látogatáskor a rendszerbeállítás, utána a látogató választása. JS nélkül az oldal
  világos marad, és a kapcsoló meg sem jelenik. (`27f6c46`)
- **Ajánlat-összehasonlítási jelentés — három kimenet, egy adatból.** Letölthető önhordó
  HTML, nyomtatható `/jelentes` oldal (PDF), és e-mailben küldhető változat. Mindhárom az
  élő táblából épül, tehát nem mondhat mást, mint amit a látogató lát. A nyomtatás valódi
  oldalon fut, nem `blob:` URL-en: az örökölné a lap CSP-jét, és `style-src 'self'` mellett
  a jelentés formázás nélkül nyomtatódna. (`e3bb12a`)
- **Siker-párbeszéd elmosott háttérrel.** A küldés a modul vége; ilyenkor kell megmondani,
  hova ment a levél (a címek kiírva) és mi a következő lépés. Natív `dialog` — a
  fókuszcsapdát és az Esc-kezelést a platform adja. (`2fca62d`)
- **Folyamatjelző az elemzéshez.** Három szakasz, eltelt idő, megszakítás. A feltöltés
  **mérhető**, ott valódi százalék áll; utána a sáv határozatlan, mert a szerver a
  válaszig néma — kitalált százalék nem kerül ki. Emiatt ennél az egy hívásnál
  `XMLHttpRequest` fut `fetch` helyett: a `fetch` nem ad feltöltési haladást. (`9c692d2`)
- **JPG-feltöltés az ajánlat-összehasonlítóban.** Fényképezett és szkennelt ajánlat gyakori.
  Végigvezetve a láncon: tallózó, kliensoldali ellenőrzés, szerveroldali kiterjesztés- és
  MIME-lista, és az elemző végpont, ami a JPEG-et ugyanúgy képként adja a modellnek, mint
  a PNG-t. (`e3bb12a`)
- **Öt jogi oldal** (adatkezelési tájékoztató, cookie-tájékoztató, ÁSZF, jogi nyilatkozat,
  akadálymentességi nyilatkozat), a régi webhely tartalmából és a hiányzó részek pótlásával,
  a láblécbe kötve. (`7bef207`)
- **Oldaltérkép-export** (`scripts/oldalgyartas/sitemap_export.py`): a tényleges menüadatból
  Markdown-fa és önhordó HTML. Minden csomópontnál ellenőrzi, létezik-e a HTML. (`05b86fe`)
- **Titkok fájlból** — `oth_titok()`: fájl → környezeti változó → beírt érték, az első
  találat nyer. Az AI-kulcs cseréjéhez így nem kell a `config.php`-t szerkeszteni. Az új
  `api/.htaccess` védi az `api/` alatti `.txt`, `.log`, `.json` és `config.php` fájlokat.
  (`e3bb12a`)

- **Előkészítés → Terhelés és kapacitás hub — nyolc aloldal.** Lakosegyenérték ·
  Személyszám és vízfogyasztás · Átlag- és csúcsterhelés · Szezonális használat ·
  Panziók és vendéglátás · Intézményi terhelés · Speciális vagy ipari szennyvíz ·
  Terhelési profil és kapacitás-előminősítő. A hub **javítja** a korábbi
  LE-meghatározást: az „1 lakosegyenérték = 135 liter/fő/nap" téves — az LE a
  biológiailag bontható szerves terhelés egysége (1 LE = napi 60 g BOI5), a
  135 l/fő/nap legfeljebb saját hidraulikai tervezési feltételezés. A két fogalom
  külön oszlopban, külön mértékegységgel szerepel.
- **Előkészítés → Tisztított víz elhelyezése hub — hat aloldal.** Elszivárogtatás ·
  Tisztítómező · Gyökérzónás elhelyezés · Magas talajvízi helyzetek · Szivárogtatási
  vizsgálat · Mikor szükséges szakértő. Az „elszivárogtatás" és a „tisztítómező"
  **nem szinonima**: aktív rendszer után a szikkasztó befogad, oldómedence után a
  talajban kialakított mező maga a tisztítás része. A „gyökérzónás öntözés"
  fogalommá és használati korlátokká alakítva — a szabályozott mezőgazdasági
  víz-újrahasználat (EU 2020/741) külön kategóriaként elkülönítve.
- **Előkészítés → Telekalkalmasság hub — a brief szerinti kilenc aloldal**, plusz a
  szakasz áttekintő oldala (`projekt-elokeszites/`). Áttekintés · Talaj és
  szivárgóképesség · Talajvíz · Kút és védőtávolság · Telekméret és szabad terület ·
  Lejtés és csőmélység · Járműterhelés és hozzáférés · Adatgyűjtés · Telek- és
  vízelhelyezési előszűrő. A hub három ponton **felülírja** a korábbi
  kommunikációt: az „elég, ha tudja a telek adatait" helyett adatminőségi feltétel
  (becsült / dokumentált / mért) áll; a tartály telepíthetősége és a víz
  elhelyezhetősége **külön** döntés, sőt a második maga is kettéválik műszaki és jogi
  kérdésre; az eredmény pedig nem igen-nem, hanem négy állapot — standard, feltételes,
  vizsgálandó, jelenleg nem igazolt.
- **`.compare-table-start` — adattábla-variáns.** Az alaptábla oszlopokat vet össze,
  ezért középre zár; ez a változat sorokat sorol fel (adat, forrás, minőség), ahol a
  középre zárás olvashatatlan. `.compare-group` a témakörönkénti csoportfejléc-sor.

- **Kapcsolat — elérhetőségi kártya a térkép fölött.** A korábbi két blokk (szöveges
  „Elérhetőség és megközelítés" szekció, alatta a térképsáv) egyetlen sávvá vonva:
  a Google Térkép a teljes szélességű háttér, az adatok egy lebegő kártyán ülnek
  fölötte a bal oldalon. A rétegezés griddel megy — mindkét réteg ugyanabba a cellába
  kerül —, ezért a sáv magassága a magasabbhoz igazodik: nagyobb betűméretnél a
  kártya nem lóg ki, a térkép nő vele. Mobilon nincs átfedés, a kettő egymás alá áll.
- **Saját térképjelölés a cég logójával** — csücskös doboz a Google gombostűje fölött.
  A helye kiszámított, nem szemre igazított: a beágyazás középpontja (`ll=`) 0,00279
  fokkal nyugatabbra van a jelölőnél (`q=`), így a gombostű a sáv közepétől jobbra
  áll, el a bal oldali kártyától — a jelölés CSS-eltolása ugyanezt a **mért** 122
  képpontot követi (a képlet 130-at adna; a keret nem a `z=16` névleges léptékén
  rajzol).
- **Élő térkép a Maps JavaScript API-val — kulcsra várva.** Ha a `.terkep` elem
  `data-terkep-kulcs` attribútuma ki van töltve, a beágyazott keret helyére valódi
  térkép kerül, és a logós jelölés **valódi térképjelölővé** válik: koordinátához
  kötve, `OverlayView`-n keresztül, a térképpel együtt mozogva — húzás és nagyítás
  közben is a házon marad. A színezést ilyenkor nem CSS-szűrő adja, hanem a Google
  saját stílusrétege, és az értékek a designtokenekből olvasódnak ki, így a térkép a
  világos/sötét témával együtt vált. **Üres kulcsnál minden a régi módon működik** —
  a kulcs hiánya, rossz kulcs és hálózati hiba egyaránt a beágyazott keretre esik
  vissza, üres folt nem keletkezik. A `.htaccess` a Maps forrásait külön blokkban,
  kizárólag a `kapcsolat.html`-re engedi. Beállítás és a kulcs korlátozása:
  `_web/README.md`.
- **`terkep.js` — a jelölés élettartama (kulcs nélküli módban).** A réteg csak addig mutat a cégre, amíg a
  térkép áll, mozgásáról viszont — másik eredet lévén — a lap semmit nem tud. Ezért
  nem követjük, hanem visszavonjuk: az egér alatt elhalványul (CSS, JS nélkül is), és
  ha a látogató tényleg a térképpel foglalkozott — 700 ms-nél tovább időzött fölötte,
  vagy a keret fókuszt kapott —, a szkript végleg elveszi. A pontos helyet onnantól a
  Google saját gombostűje jelöli, ami együtt mozog a térképpel. A tévedés ára
  aszimmetrikus: a fölöslegesen elvett jelölés csak egy hiányzó dísz, a bent maradó
  viszont rossz helyre mutatna.
- **`--shadow-3` — harmadik elevációs szint.** A lapról leváló, más tartalom fölött
  lebegő felületekhez. Egyetlen használati helye a térkép fölötti kártya és jelölés:
  ott a háttér nem egyszínű, hanem rajzos, és a `--shadow-2` finom pereme beleolvadt.

- **„Telekvásárlás vagy új építés" hub — öt aloldal.** Alkalmas lehet-e a telek? ·
  Talaj, talajvíz és vízelhelyezés · Milyen dokumentumokra lehet szükség? ·
  Telekadat-ellenőrzőlista · Helyszíni felmérés.
  **A brief három ponton kifejezetten felülír korábbi állításokat, és mindhármat
  átvezettem:** (1) a „nem feltétlenül szükséges helyszíni felmérés — elég, ha
  tudja a telek adatait" helyére döntési tábla került (mikor elég dokumentum és
  fotó, mikor indokolt a kiszállás, mikor kell más szakértő); (2) a tartály
  telepíthetősége és a kezelt víz elhelyezhetősége **két külön döntés** — a régi
  tartalom ezt egybemosta, pedig a magasabb talajvíznél rögzíthető tartályból nem
  következik, hogy a víz helyben szikkasztható; (3) a felmérés eredménye nem
  „személyre szabott ajánlat", hanem strukturált telekbrief.
  Szolgáltatási ár sehol nincs, a felmérésé sem. Az ellenőrzőlista **nem kér
  kapcsolati adatot** a használatához, és minden tételnél elfogadja a „nem tudom"
  választ. A dokumentumoldal szerepkör szerint oszt (építtető / tervező /
  ÖkoTech / hatóság), és kimondja, hogy univerzális dokumentumlista nincs.
- **„Nincs elérhető közcsatorna" hub — a sitemap szerinti négy aloldal.**
  Milyen megoldási lehetőségek vannak? · Közcsatorna vagy egyedi rendszer? ·
  Milyen adatokat kell először összegyűjteni? · Projektindító. A hub-oldal
  döntési útvonalként köti össze őket, mert a sorrend nem tetszőleges: a
  közcsatornahelyzet tisztázása megelőzi a technológiaválasztást.
  **A brief négy szabálya végig érvényes:** nincs konkrét ár (a régi oldal havi
  költség- és megtérülési számai NEM kerültek át); a **„nem tudom" érvényes
  válasz** — az adatlap minden tételénél szerepel, honnan tudható meg, becsülhető-e
  vagy mérni kell; **az ajánlatkérés nem minden oldal végpontja** (legitim
  eredmény a további adatgyűjtés, a telekellenőrzés vagy más megoldás); és a
  **„Közcsatorna vagy egyedi rendszer?" a hub leggyorsabban avuló oldala** —
  jogi jelöléssel és azzal a kiírt kikötéssel, hogy a saját ingatlanra vonatkozó
  választ a víziközmű-szolgáltatótól és az önkormányzattól kell megkérni.
- **Megoldások hub — a sitemap szerinti négy döntéstámogató aloldal.**
  Megoldástípusok összehasonlítása · Melyik megoldás mikor megfelelő? · Kizáró és
  korlátozó feltételek · Megoldástípus-előszűrő. Bekötve a megamenübe (a
  Megoldások panel most nyolc elemű, 4+4 elrendezésben).
  **Két szabály végig érvényes, a tartalmi brief előírása szerint:**
  nincs „jobb–rosszabb" minősítés — a technológiák feltételekkel és
  kompromisszumokkal írhatók le, mert a cél nem az A.B. Clear mindenáron való
  kiválasztása, hanem a rossz technológiaválasztás megelőzése; és **nincs
  kitalált adat** — ahol a brief belső ÖkoTech-adatot ír elő (karbantartási
  ciklus, kizárási mátrix, telekigény, ürítési intervallum, energiafogyasztás,
  a teljes döntési fa), ott `ADATHIÁNY` jelölés áll, nem becslés. A jogszabályra
  hivatkozó állítások `JOGI ELLENŐRZÉS` jelölést kaptak, mert a brief publikálás
  előtti friss ellenőrzést ír elő. Konkrét ár sehol nincs, csak költségkategória.
  Az előszűrő felülete szándékosan még nem él: a döntési szabályokat a cég
  szakmai vezetésének kell jóváhagynia, mielőtt bárkinek eredményt mutatunk.
- **§12 — Dokumentált projektek és használói tapasztalatok**, és a hozzá tartozó
  **négy esettanulmány-oldal** (`eredmenyek/csikvand`, `bakonypeterd`,
  `diosbereny`, `obudavar`). Kiemelt projekt + hármas rács, mindegyik saját
  légifelvétellel, projektadat-táblával és „miért így oldottuk meg" magyarázattal.
  A számok és évszámok a végleges szövegdokumentumból valók, kerekítés nélkül.
  A nyolc visszajelzés léptethető, de **JS nélkül mind látszik** — a `hidden`
  attribútumot a JS teszi rá, tehát a tartalom sosem vész el, és a keresők is
  megtalálják. Nincs automatikus léptetés: a mozgó szöveg olvasás közben zavaró,
  és a WCAG 2.2 külön kéri a megállíthatóságot.
- **Levélküldő backend — három végpont.** `api/kapcsolat`, `api/dontestamogato`
  és `api/ajanlat-atnezes` (ez utóbbi csatolmánnyal). Saját, függőség nélküli
  SMTP-kliens (implicit TLS 465 és STARTTLS 587); a `mail()` azért nem jó, mert
  hitelesítés nélkül adja át a levelet, és SPF/DKIM nélkül spambe kerül.
  **Márkás HTML levélsablon**: sötét fejlécsáv a logóval, táblázatos elrendezés
  (az e-mail-kliensek nem tudnak flexboxot), minden szabály `style` attribútumban
  (a Gmail a `<style>`-t kiszűrheti), és mindig megy sima szöveges változat is.
  A kép blokkolása esetén a fejléc olvasható marad.
  **Négy védelmi réteg**: origin-ellenőrzés, mézesbödön mező, kitöltési idő,
  IP-alapú sebességkorlát. Minden felhasználói érték CR/LF-szűrésen megy át —
  enélkül a `Bcc:` beszúrható lenne, és az űrlap spamtovábbítóvá válna.
  A csatolmány kiterjesztés ÉS tényleges tartalom szerint is ellenőrzött.
  **A jelszó nincs a repóban**: `api/config.php` gitignore-olt, a repóban csak
  a minta van; az `api/.htaccess` a kiszolgálását is tiltja.
- **Kapcsolat oldal — valódi űrlap.** A korábbi „még nem éles" panel helyett
  működő űrlap, amely **JS nélkül is beküld** (sima POST); az `urlap.js` csak a
  választ jeleníti meg helyben, és a hibás mezőre ugrik.
- **§11 — AI ajánlat-összehasonlító.** A Test1-beli modul átvéve: három feltöltő
  kártya (A/B/C) behúzással és tallózással, formátum- és méretellenőrzéssel,
  fájlchippel és visszaállítással; háromlépéses jelző; tízsoros összehasonlító
  tábla, amely üresen indul, és csak a ténylegesen feltöltött ajánlatok oszlopát
  tölti ki. Viselkedés és elrendezés változatlan, a megjelenés a Test2
  tokenkészletéből.
  **Két eltérés a forrástól, mindkettő szándékos:** a megszólítás magázóra
  váltott (a webhely többi része, a 8. szekció modulja is az), és a kitöltés
  után a modul kiírja, hogy **mintaadatot** mutat — a feltöltött fájlok
  kiolvasása backendet igényel, ami még nincs. Enélkül a felhasználó a saját
  ajánlatai elemzésének hinné a táblát. A JS-horgok `data-ofc-*` attribútumok,
  nem osztályok, mert az osztály stílust sugallna.
  Forrás: `assets/js/ofc.js`, `scripts/oldalgyartas/szekcio11.py`.
- **§10 — Tudástár.** Hét témakör-belépő: egy kiemelt (a leggyakoribb elakadási
  pont) és hat a hármas rácsban, mindegyik „Pl. …" ízelítővel a témakör
  hatóköréről. A címek aláhúzottak — ez a dokumentált kivétel a webhely
  aláhúzás-mentes hivatkozásai alól: a szekció szinte csupa link, és a szín
  önmagában nem különböztetné meg őket (WCAG 1.4.1).
- **§9 — Üzemeltetés és hosszú távú költség.** Három technológia éves üzemeltetési
  tételei egymás mellett (zárt tároló · oldómedence · A.B. Clear), saját metszeti
  fényképpel. A számok a végleges szövegdokumentumból valók, nem becslésből —
  a számítás feltevései (háromfős háztartás, napi 135 l/fő, piaci átlagdíjak)
  lábjegyzetben, vonallal elválasztva, mert nem a tartalom folytatása, hanem a
  fenti számok érvényességi köre. Két új variáns: `.situation-grid[data-cols="3"]`
  és `.situation-media` (teljes fénykép világos keretben — a `.card-media` ezzel
  szemben kivágott illusztrációt tart). Az „Epureco … a technológia aloldalán"
  mondat az oldómedencés oldalra hivatkozik.
- **„Helyzetem" kategória — 8 oldal.** A sitemap első főkategóriája megépült: áttekintő
  (`helyzetem/`) és hét helyzet-oldal (nincs közcsatorna · telekvásárlás és új építés ·
  emésztő kiváltása · nyaraló és szezonális · családi ház · vállalkozás és intézmény ·
  már van rendszerem). A szekciók a sitemap 3. szintjét követik, a szerkezet az
  `okotechhome-oldalgyartas` skill „Helyzet-oldal" sablonját. Minden oldalon saját,
  21:9 arányú generált fejléckép, morzsamenü, GYIK és `BreadcrumbList` + `FAQPage`
  strukturált adat.
- **Kapcsolat oldal (`kapcsolat.html`).** A webhely egyetemes CTA-célpontja; eddig
  minden szekció és aloldal nem létező URL-re mutatott. Négy megszólítás-útvonal a
  sitemap szerint (új érdeklődő · meglévő ügyfél · szakmai partner · sajtó), plusz
  elérhetőségek. A fejléc „Konzultációt kérek" gombja is ide mutat.
- **`.situation-grid[data-cols]` reszponzív felülírása.** Az attribútum-szelektor
  specifikusabb az osztályszelektornál, ezért a média-lekérdezésben lévő
  `.situation-grid{grid-template-columns:…}` nem írta volna felül: tableten és
  mobilon is három oszlop maradt volna, összenyomott képekkel. A töréspontok
  most külön nevesítik a variánst.
- **`.numbered-grid` négyelemű változata.** Pontosan négy kártyánál 2×2 rács
  (`:has(> :nth-child(4):last-child)`), mert a hármas osztás 3+1-re tört, és az árva
  kártya elrendezési hibának látszott.
- **Egyedi hibaoldalak — 404 · 403 · 401 · 500.** Egyetlen relatív útvonal sincs
  bennük (a logó beágyazott SVG), mert a böngésző a relatív útvonalakat a
  *kért* URL-hez oldja fel, nem a hibaoldal helyéhez — `/megoldasok/nincs-ilyen`
  kérésnél a `assets/css/app.css` `/megoldasok/assets/…`-ra mutatna, és szintén 404
  lenne. A stílus ezért a `/assets/css/hiba.css`-ben áll, gyökér-abszolút
  hivatkozással. A `.htaccess` mind a négyet bejegyzi, és `Options -Indexes`-szel
  kikapcsolja a könyvtárlistákat (a tiltás 403-at ad, amit a hibaoldal fog el).
  Forrás: `scripts/oldalgyartas/hibaoldalak.py`.
- **`serve.py` — a teljes biztonságifejléc-készlet.** A helyi kiszolgáló eddig három
  fejlécet küldött, CSP-t nem; így egy egész hibaosztály csak élesben derült ki.
  Mostantól a `.htaccess` CSP-jét, `X-Frame-Options`-át, `Permissions-Policy`-jét és
  a teszt üzemmód `X-Robots-Tag`-jét is küldi.
- **Teljes ikonkészlet.** Eddig **egyetlen favicon sem volt** — minden böngészőfülön
  üres lap-ikon állt. A jelrajzból (a logó Fern-zöld térkép-sziluettje) készült
  `favicon.svg`, `favicon-{16,32,48}.png`, gyökérbeli `favicon.ico`,
  `apple-touch-icon.png` (tömör háttérrel, mert az iOS nem kezeli az alfát),
  `icon-{192,512}.png`, maskable változat és `site.webmanifest`. Bekötve mind a
  15 oldalra, `theme-color`-ral együtt.
- **Oldalgenerátorok a repóban** (`scripts/oldalgyartas/`): `sablon.py` a szekció- és
  oldalváz-építőkkel, `helyzetem.py`, `kapcsolat.py`, `hibaoldalak.py`. A fejlécet a
  sablon egy meglévő aloldalból emeli ki, így a 15 példányban duplikált fejléc nem tud
  szétcsúszni, amíg nincs valódi build-lépés.

### Módosítva

- **A levél logója beágyazva megy** (`Content-ID`), nem távoli URL-ről: a kliensek
  többsége nem tölt le távoli képet, és a webhely még nem él a configban álló néven. Ehhez
  valódi `multipart/related` szint kellett — e nélkül a logó külön csatolmányként jelent
  volna meg, a fejléc meg törötten. (`d4c8f8d`)
- **Az összehasonlító tábla balra igazít**, és a három ajánlat azonos szélességet kap.
  A `.compare-table` középre zárása rövid, chipszerű értékekre készült; itt valódi, több
  soros mondatok állnak. (`09b0346`)
- **Az AI-asszisztens jele** vastagabb vonallal, tömör levéllel újrarajzolva, 22–30
  képpontra tervezve. A márka teljes jelrajza nem való ide: korong belsejében foltnak
  látszik, nem jelnek. (`09b0346`)
- **Nincs aláhúzás a hivatkozásokon** alapállapotban; hoverre és fókuszra jelenik meg.
  (`5b742a4`)

- **A hivatkozások alapállapotban nem aláhúzottak** (`a{text-decoration:none}`), egérrel
  és billentyűzet-fókuszban igen. A böngésző alapértelmezett aláhúzása vastag, a
  betűtalpakat elvágó vonal, ami a felületen — ahol a linkek jellemzően külön sorban
  álló adatok — zajnak látszott. A `:hover`/`:focus-visible` aláhúzás nem díszítés:
  ez az egyetlen nem-szín alapú jelzés, ami a hivatkozást hivatkozásként azonosítja.
  A **folyószövegbe ágyazott** linkeknél ez nyitott WCAG 1.4.1 pont — a linkszín és a
  törzsszöveg kontrasztja 2,49:1, a 3:1 alatt. Részletek és a visszakapcsolás egyetlen
  szabálya: `_web/README.md`.
- **A beágyazott térkép tompított és márkaszínű fátylat kapott** (`saturate(.72)` +
  a lap zöldjének 30%-os rétege), hogy háttér maradjon, és a fölötte lebegő kártya és
  logó elváljon tőle. A fátyol maszkja az alsó sávot kihagyja: ott fut a Google logója
  és a térképadat-jelzés, azokat sem fadelni, sem befátyolozni nem szabad.
- **A Google saját adatlapja eltűnt a térkép bal felső sarkából.** URL-paraméterrel nem
  kapcsolható ki, ezért a keret 120px-szel feljebb nyúlik és a sávból kivágódik. Az
  alsó él a helyén marad, így az attribúció végig látszik.

### Javítva

- **Az összegzősor („Hiányzó / tisztázandó tétel") sosem töltődött ki.** A sor a szerver
  szempontjaiból próbált feltöltődni, de hozzá nem tartozik szempont — mindhárom oszlopában
  „—" állt, miközben fölötte több sorban is „nincs adat" szerepelt. Ez **származtatott
  érték**: a kliens számolja, és meg is nevezi a hiányzó szempontokat. (`e22ef87`)
- **A táblasorok sorrend alapján párosultak a szerver szempontjaival** (`Math.floor(i / 3)`).
  Egyetlen beszúrt sor némán elcsúsztatta volna az összes cellát — az ár a technológia
  oszlopába került volna, szabályosan formázva és teljesen rosszul. A párosítás mostantól
  `data-ofc-sor` kulcs alapján megy, és a generátor minden futáskor összeveti a két listát.
  (`e22ef87`)
- **PDF/nyomtatás mindig az üres állapotot mutatta.** Két ok: a `sessionStorage` fülönként
  külön él, a `noopener`-rel nyitott lap üres tárolóval indul (`a770b62`); majd a
  `window.open(..., 'noopener')` **mindig `null`-t ad vissza**, ezért a „blokkolva" tartalék
  minden alkalommal lefutott, és az eredeti fül a már kiürített jelentésre navigált.
  (`9c692d2`)
- **A levéltörzs „nincs adat"-ot írt** két ajánlat mellé, miközben a mellékletben végig
  volt adat: az oszlopcímkét foglalta össze, ami gyakran „nincs adat". Mostantól a fájlnév
  és az első érdemi szempont (elsősorban az ár) megy ki, a hiány pedig hiánynak számít,
  nem értéknek. (`2fca62d`)
- **Több címzett vesszővel** nem működött, és „váratlan hibát" adott. A végpont egy címet
  váró ellenőrzőt használt; most vesszőre és pontosvesszőre bont, ötig, és megnevezi a
  hibás címet. Az SMTP-hibát külön kapjuk el, beszédes üzenettel. (`dc11c55`)
- **A lábléc a `<head>`-be került** új oldalon: a beszúrási pont az első `<script src=` volt,
  ami a témaváltó szkriptje óta a fejrészben áll. Most a `</main>`-hez igazodik. (`e3bb12a`)
- **A kapcsolat oldalról hiányzott a lábléc** — a beszúró minta nem illeszkedett, és a
  szkript némán sikert jelentett. (`ce85a46`)

- **A kapcsolat oldalról hiányzott a lábléc.** A `lablec.py` a `\n<script src=` minta
  elé szúrta be a láblécet; ezen az oldalon az utolsó elem egy beágyazott JSON-LD blokk,
  amiben nincs `src=`, így a beszúrás NÉMÁN elmaradt — a szkript mégis sikeresnek
  jelentette. Új tartalék a `</body>` elé, és aki így sem kap láblécet, arról a szkript
  most nevesítve szól.
- **A főoldal 3. szekciójának hivatkozásai** nem létező, a sitemap-en kívüli szlugokra
  mutattak (`uj-epitkezes`, `emeszto-kivaltasa`, `idoszakos-hasznalat`, `telekvasarlas`).
  Mind a négy a megfelelő `helyzetem/…` oldalra mutat. Az első oszlop
  („Építkezés csatorna nélküli telken") a közcsatorna-oldalra került, mert a
  telekvásárlásra a negyedik oszlop mutat.
- **`megoldasok/megoldasok-attekintese`** — a megamenü olyan szlugra hivatkozott, amely
  soha nem létezett; az áttekintő oldal maga a `megoldasok/`. Javítva 13 fájlban.
- **Sötét panelen a prózában álló hivatkozás** a `--link` kékjét kapta, ami a Forest
  háttéren nem éri el a 4,5:1-et. A `.panel-dark-text a` mostantól ugyanazt a
  `--panel-dark-link` színt használja, mint a `.text-link`.
- **Nyolc fejléckép függőleges varrattal.** A képgeneráló promptban a „bal harmad
  üresen marad a szövegnek" megfogalmazás miatt a modell a bal harmadot külön, lapos
  panelként rajzolta, éles illesztéssel — a legfeltűnőbb az *Oldómedencés rendszer*
  oldalon volt. Mind a nyolc újragenerálva egyetlen összefüggő jelenetként; a
  hibás promptszerkezet és a varrat gépi kimutatása a `okotechhome-oldalgyartas`
  skill `designrendszer.md` fájljában rögzítve, hogy ne ismétlődjön.
- **Logó SVG megtisztítva.** A CorelDRAW-export külső DTD-hivatkozást (egyes elemzők
  hálózatról töltenék be), fix `width="3576px"`/`height` attribútumot (CSS-hiba esetén
  ekkorán rajzolódna) és holt névtereket tartalmazott. 10 771 → 10 349 byte, `<title>`
  hozzáadva a közvetlen megnyitáshoz.
- **Teszt üzemmód — keresők teljes kizárása.** Az oldal a `tst.okoth.hu` aldomainre
  költözik; a zárás három rétegben él: `X-Robots-Tag` fejléc a `.htaccess`-ben,
  `Disallow: /` a `robots.txt`-ben, és `<meta name="robots" content="noindex, …">`
  minden oldalon. A HTTP Basic Auth blokk előkészítve, kommentben. Az élesítési
  ellenőrzőlista a `_web/README.md` elején.
- **Domain átállítás:** a `canonical` és az Open Graph URL-ek `okotechhome.hu` helyett
  már az éles **`okoth.hu`** domainre mutatnak, így élesítéskor nem kell hozzájuk nyúlni.
- **Hero videó erőforrás-kezelése.** A hurokban futó felvétel `IntersectionObserver`-rel
  és `visibilitychange`-dzsel megáll, amikor kigörög a képből vagy a lap háttérbe kerül —
  enélkül a folyamatos dekódolás hosszú munkamenetben lassuláshoz, végül a lap
  összeomlásához vezetett. A videó újrakódolva takarékosabbra: 1600→1280px,
  3026→1515 kbps, 2,5→1,27 MB.
- **`serve.py` — részleges letöltés (HTTP 206).** A beépített kiszolgáló minden kérésre a
  teljes fájlt küldte, ezért a hurokvideó újra és újra letöltődött. Élesben az Apache ezt
  magától megoldja; ez a helyi kiszolgálót hozza szintre.

- **Megamenü a fejlécben** — a sitemap 2. szintje (39 aloldal öt kategóriában) lenyíló
  panelekből érhető el. A nyitóelem `button` (`aria-expanded` + `aria-controls`), a panel
  `hidden`-nel zár, Esc és külső kattintás bezárja, a fókusz visszatér. A navigáció a
  sitemap nyolc főkategóriájára épült át: öt a fejlécben panellel, három a kontaktsávban.
- **`index.html` — oldalfejléc**: kontaktsáv (cím, e-mail, telefon · GYIK, Karrier) és fő
  navigációs sáv (logó, ötelemű menü, „Konzultációt kérek" CTA). A menü natív
  `details`/`summary`: a markupban nyitva áll, ezért JS nélkül is elérhető; ≤1024px-en
  lenyitható panellé válik.
- **`index.html` — 1. szekció (*Hero*)**: adatsor, kiemeléses főcím, bevezető, két gomb és
  egy chip-hivatkozás az ajánlat-összehasonlításhoz. **Borító-elrendezés**: a felvétel a
  teljes hero-felületet kitölti, a szöveg rajta ül. A magasság a képernyővel mozog —
  legalább `100svh − --header-h`, e fölött a médiablokk aránya vagy a szöveg magassága
  dönt. ≤1024px-en a borító megszűnik: szöveg, alatta a szűk kivágatú kép.
- **Lágy folt (veil) a hero szövege mögött** — radiális gradiens, amely minden irányban a
  nulláig fut ki, ezért sehol nincs éle vagy sávhatára. Középpontja a konténerhez kötött
  (`50% − --container-max/2 + --page-gutter + 26ch`), így a szövegoszlop fölött marad
  minden képernyőszélességen. Csak annyit emel a háttéren, hogy a felvétel kontúrjai ne
  fussanak bele a betűkbe; ≤1024px-en kikapcsolva.

  > ⚠️ A mozgókép változó háttere miatt a WCAG 2.2 AA szövegkontraszt **nem garantálható
  > minden pillanatban**. Jelezve a `COMPONENTS.md` 13. pontjában.
- **Tapadó (sticky) fejléc** finom árnyékkal (`--shadow-1`, sötét témában elmarad):
  a kontaktsáv görgetéskor kicsúszik, a fő sáv a viewport tetején marad. A `top` épp a
  kontaktsáv magasságával negatív — a fő sávot önmagában nem lehet tapasztani, mert a
  `sticky` a szülő dobozán belül mozog.
- **`.btn-inverse`** — a hero második gombja a legsötétebb felületen (Forest), ahogy a
  vizuális terv mutatja; sötét témában a felület-lépcső következő fokán.
- **`index.html` — 2. szekció (*Bizalmi sáv*)**: négy állítás (3 800+ rendszer ·
  EN 12566-3 / CE · Construma Nagydíj 2014 · ISO 9001 / esztergomi gyártás) függőleges
  elválasztókkal; a szabványjelölések mono betűvel, mert adatok.
- **Hero-média** — állókép **két kivágásban** (16:9 asztali, 3:2 szűk) WebP-ben, `picture`
  art directionnel, és a `hero-rendszer.{webm,mp4}` felvétel hang nélkül. A videót
  a `site.js` **csak asztali nézetben, mozgás engedélyezése mellett és adattakarékos mód
  nélkül** tölti be, a `load` esemény után; minden más esetben az állókép a végállapot.
- **`assets/js/site.js`** — az oldal első JS-e (~2 KB, `defer`): menüpanel szűk nézetben,
  feltételes hero videó. Mindkettő progressive enhancement.
- **`index.html` — 8. szekció (*AI-alapú döntéstámogató*)** és **`assets/js/ai-advisor.js`**:
  a Test1 §6 modulja átvéve. A JS (566 sor: kérdéssor, ársáv-logika, eredményképernyő)
  **változatlan**, a ~200 soros `.aidt-*` CSS teljes egészében a Test2 tokenjeire újraírva.
  Lásd `_web/COMPONENTS.md` 18.
- **`assets/data/aidt-konfig.js`** — a döntéstámogató **árértékei a kódon kívülre kerültek**,
  a cég által szerkeszthető konfigba (a modulban csak tartalék marad). Ugyanitt áll az
  adatküldés végpontja és az adatkezelési tájékoztató útvonala.
- **Valódi adatküldés a döntéstámogatóban** — beállított végponttal `POST`, sikeres válasz
  után visszaigazolás, hibánál `role="alert"` üzenet. Végpont nélkül a modul **nem állítja,
  hogy elküldte**, hanem jelzi, hogy a küldés még nincs élesítve. A hozzájárulás mellett
  megjelenik az adatkezelési tájékoztató hivatkozása.
- **`<noscript>` alternatíva a 8. szekcióban** — JS nélkül a szekció elmondja, mit kérdezne
  a modul, és felkínálja a telefonos, illetve e-mailes utat.
- **Hero-felvétel cserélve** az új anyagra (naplementés kert, feltárt munkagödör): WebM
  2,7 MB + MP4 2,8 MB, 1600px szélességben. Az állóképek is **ebből a felvételből** készültek
  (16:9 asztali és 3:2 szűk kivágat), hogy a mobil és az asztali nézet ne térjen el.
  A hero adatsora a másodlagos szövegszínt kapta: a napfényes égen a harmadlagos nem érte el
  a 4,5:1-et.
- **`assets/img/logo-okotechhome.svg`** — az ügyféltől kapott kétszínű logó (Fern jelrajz,
  Forest szóvédjegy), egyetlen kiegészítéssel: a szóvédjegy sötét rendszertémán Stardustra
  vált (`prefers-color-scheme`). A fejlécben `height: var(--space-48)`, `width: auto`.
- **`assets/icon/ui-{helyszin,email,telefon}.svg`** — az ügyféltől kapott kontaktikonok
  `currentColor`-ra állítva; `ui-dokumentum.svg` **ideiglenes saját pótlás**, a terv
  chipjének rajzolata után (álló lap behajtott sarokkal, három sorral, az első rövidebb).
- **`.chip-link`** — kiegészítő, chip megjelenésű hivatkozás. Nem gomb (a 7.1 szerint
  szekciónként egy elsődleges CTA áll) és nem `.card-tag` (az nem interaktív).
- **`.icon-inline` / `.icon-inline-lg`** — soron belüli ikonméret-szerep. Itt a befoglaló
  négyzet a helyes szabály, nem a blokk-ikonok magasság-normalizálása.
- **`--dur-media` (600ms)** — javasolt lassabb időtartam-szerep médiaváltáshoz; a rendszerben
  eddig csak a `--dur-fast` (150ms) élt.
- **`assets/css/app.css`** — a designrendszer (`OTH-design-system-Teszt.v2` v0.5)
  implementációja `@layer` architektúrában: `reset → tokens → base → typography →
  components → responsive → motion`. A tokenblokk szó szerint az élő HTML-referenciából,
  a `.type-*` szereposztályok, a `.btn` és a `.text-link` változatlanul.
- **`index.html` — 3. szekció (*Kiinduló helyzet*)**: négy helyzetoszlop kerek
  ikonjelvénnyel és felső elválasztó vonallal (nem kártya, a canvason), alattuk **sötét
  kiemelt panel** a nagyobb kapacitású (50 fő feletti) igényekhez. A szövegek a végleges
  főoldal-dokumentumból (`Okoteh-Home.fooldal.szoveg-vagleges.docx`).
- **`assets/icon/ui-{epitkezes,emeszto,nyaralo,telek}.svg`** — a helyzetoszlopok
  ikonjai; saját vonalas rajzolat a vizuális terv után, `currentColor`-ral.
- **A döntéstámogató haladás-sínje és ikonjai átdolgozva** — a sín halvány sávon telített
  kitöltés, gyűrű nélküli véggel (a korábbi világos gyűrű elvágta a sínt), a kitöltésnek
  alsó határa van, hogy induláskor is látszódjon. A bizalmi jelvények 32→40px, a rajzolatok
  16→24px: a korábbi méret olvashatatlanul apró volt.
- **`.situation` · `.icon-badge` · `.panel-dark` · `.link-label`** — új komponensek,
  kizárólag meglévő tokenekből. Indoklás: `_web/COMPONENTS.md` 13/b–13/c.
- **`index.html` — 4. szekció (*Technológiák*)**: három sorszámozott magyarázókártya,
  „Gyors összehasonlítás" táblázat ikonos oszlopfejlécekkel, és a saját berendezések
  (Epureco oldómedence, A.B. Clear) blokkja. A technológiai ikonok és a két termékrender
  az ügyfél új eszközeire cserélve (a biológiai ikon 107×41 → 58×41, az `aspect-ratio`
  ehhez igazítva; a termékfotók 1254×1254, alfacsatornás WebP).
- **`index.html` — 5. szekció (*Megoldásaink*)**: négy termékkártya besorolás-címkével
  (A.B. Clear · telepek · Epureco oldómedencék · iszapzsákos technológia).
- **`.card-tag`** — címke-chip a kártya besorolásához. Nem státusz és nem művelet, ezért
  nem `.alert` és nem gomb, hanem önálló, nem interaktív komponens.
- **`.card-media-product`** — médiakeret-variáns álló és négyzetes termékrenderhez;
  a 3:2-es alapkeretben ezek a képek a kártya szélességének alig felét töltenék ki.
- **`.section-lead-wide` + `.br-desktop`** — a bevezető bekezdés a terv szerinti
  sortöréssel, kizárólag asztali nézetben kényszerítve.
- **Új komponensek** — a designrendszer 10. fejezete szerint még definiálatlan elemek
  dokumentált osztályként, kizárólag meglévő tokenekből: szekció-sáv, kártya, médiakeret,
  kiemelt panel, sorszámjelvény, ikon, összehasonlító táblázat, termékkártya,
  kétoszlopos szekcióalj. Indoklás és javasolt szabályzatszöveg: **`_web/COMPONENTS.md`**.
- **`.htaccess`** — kiterjesztés nélküli (clean) URL-ek: `/valami.html` → 301 `/valami`,
  `/index.html` → 301 `/`, záró perjel eltávolítása; biztonsági fejlécek (CSP, nosniff,
  X-Frame-Options, Referrer-Policy, Permissions-Policy), tömörítés és cache. A cache-szabályok
  kiegészítve a `video/webm` és `video/mp4` típusokkal.
- **`serve.py`** — lokális preview szerver, amely a `.htaccess` clean-URL viselkedését
  emulálja. Enélkül a kiterjesztés nélküli linkek helyben 404-et adnának.
- **Médiaeszközök** — öt kivágott illusztráció és két termékfotó WebP-ben
  (`assets/img/`), három technológiai ikon (`assets/icon/`).

### Javítva

- **Médiakeret magassága** — a `.card-media` egyszerre flex-konténer és flex-elem, így az
  alapértelmezett `min-height:auto` a *kép* belső méretéből számolt, és felülírta az
  `aspect-ratio`-t. A hiba csak akkor jelentkezett, ha a kép saját aránya magasabb volt a
  szereptokenben megadottnál — ezért asztali nézetben rejtve maradt, és mobilon jött elő
  (460×306 a várt 460×259 helyett). Javítás: `min-height:0`.
- **Ikonok beégetett színe** — a kapott CorelDRAW-SVG-k `fill:#21432B` nyers hexet
  hordoztak, ami a 9. tiltólistába ütközik és sötét témában olvashatatlan lenne.
  A `fill` `currentColor`-ra cserélve, a színt CSS-maszk adja.
- **Táblázat túlcsordulása** — a négyoszlopos összehasonlító tábla 46px-szel kilógott a
  szekcióalj felén. A cellák vízszintes belső térköze `--space-16` → `--space-8`.
- **Fejléc-ikonok elcsúszása** — alsó cellaigazításnál a kétsoros oszlopfelirat
  („Biológiai szennyvíztisztító") feltolta a saját ikonját, és az ikonsor kiesett a vonalból.
  A fejléccellák `vertical-align: top`-ra állítva.
- **A táblázat harmadik felülete** — a vizuális terv három felületet használ (panel →
  halványabb zöld páratlan sor → fehér páros sor), az implementációban csak kettő volt.
  A középső árnyalatra nincs token, nyers hexet pedig a 0.8 és a 9. szabály tilt, ezért
  `color-mix(in srgb, var(--surface-muted) 60%, var(--surface))` állítja elő — így témaváltáskor
  együtt mozog a két forrásfelülettel.

### Dokumentáció

- **`_web/README.md`** újraírva: designrendszer-összefoglaló (betűcsaládok, paletta, térköz,
  töréspontok), a betartott kötelező szabályok, clean-URL viselkedéstábla, deploy-kizárások.
- **`README.md`** — Test1 ↔ Test2 összevetés kiegészítve a tényleges tipográfiával és
  palettával; a könyvtárfa a valós `_web/` tartalommal; helyi fejlesztés `serve.py`-ra állítva.
- **`VERSIONING.md`** — commit-hatókörök a projekt tényleges moduljaira igazítva,
  verzió-életút frissítve.
- **Jelezve:** a Test1 GSAP + Lenis animációs rétege ütközik a designrendszer **0.7**
  alapszabályával (*„Nincs framework"*), ezért nem emelhető át változtatás nélkül.

### Megjegyzés

- A kártyák **azonos magasságúak** (a rács `stretch` igazítása), a hivatkozás
  `margin-top:auto`-val mindig a kártya alján zár.
- A `_web/` linkjei már **kiterjesztés nélküliek**; a hivatkozott aloldalak
  (`uj-epitkezes`, `emeszto-kivaltasa`, …) még nem léteznek, így helyben 404-et adnak.
  A hero három modul-útvonala (`dontesi-utvonal`, `koltsegiranytu`,
  `ajanlat-osszehasonlitas`) **javasolt szlug**, a döntéstámogató modulok végleges
  elnevezésével együtt véglegesítendő.
- Döntést igénylő pontok a `COMPONENTS.md`-ben jelölve: a navigációs CTA gombként való
  megjelenítése (7.6 tábla), a szekció-sávok váltakozása (5.3 elv), a kontaktsáv
  hivatkozásainak típusa (`.topbar-link` vs `.text-link`), a nagybetűs navigáció
  szerepszintre emelése, az inverz gomb felvétele a 7.1-be, a réteg- (z-index-) skála
  hiánya, valamint a mozgókép rendszerszintű szabályozása.
- **A logó szóvédjegye a `prefers-color-scheme`-et követi**, nem a `[data-theme]`
  kapcsolót — a témaváltó UI megépítésekor inline SVG-re cserélendő. A vektoros mester
  (`okotech-logo-magyar-colorversions.ai`) egyszínű, szeriffes feliratú változatokat
  tartalmaz; a weben az ügyféltől külön kapott **kétszínű, groteszk feliratú** SVG él.
- A hero videója **8 másodperces, néma, hurokban futó** felvétel: WebM 1,4 MB,
  MP4 1,7 MB. Szűk nézetben egyik sem töltődik le.

---

## [0.01.01] — 2026-07-26

A **Test2** repó inicializálása: webkimenet-váz, verziókezelés és dokumentációs réteg.
**Weboldal-kód még nincs** — a `_web/` egyelőre üres váz.

A Test2 azonos márkát, motort, technológiát és logót visz, mint a Test1
(`okotechhome-web`, jelenleg `0.9.0`); az eltérés kizárólag a **designrendszerben** lesz.

### Hozzáadva

- **`_web/`** — a deployolható statikus webkimenet váza (`assets/{css,js,img}`), saját
  `README.md`-vel: célszerkezet, technológiai réteg, helyi kiszolgálás, minőségi kapuk.
- **`README.md`** — HTML-alapú (banner, badge-ek, táblázatok) projektútmutató:
  Test1 ↔ Test2 összevetés, repó-hatókör, verziózás, deploy, nyitott pontok.
- **`CHANGELOG.md`** — ez a napló, Keep a Changelog 1.1.0 formátumban.
- **`VERSIONING.md`** — verziózási szabályzat: a **feltöltött** (`X.YY.ZZ`) verziószám-formátum
  definíciója és indoklása, SemVer-értelmezés statikus marketing-oldalra, Conventional Commits →
  verzióemelés leképezés, ág- és tagkonvenciók, kiadási folyamat, deploy-korreláció,
  visszaállítási (rollback) recept, verzió-életút.
- **`VERSION`** — gépi olvasásra alkalmas, egysoros verzió-forrás (single source of truth): `0.01.01`.
- **`scripts/release.sh`** — kiadás-automatizálás: a feltöltött formátum validációja, numerikus
  (`10#` bázisú, oktális-biztos) verzió-összehasonlítás, `VERSION` frissítés, `CHANGELOG.md`
  szekció-ellenőrzés, annotált tag létrehozása, `--dry-run` móddal.
- **`.gitignore`** — a repó hatókörét kikényszerítő kizárások (lásd alább), valamint titkok,
  rendszerszemét és build-melléktermékek.
- **`.github/banner.png` · `.github/banner.svg`** — README-banner, a Test1 repóból átemelve
  (a márka azonos, a banner nem kerül élesre).

### Repó-hatókör

A távoli repóba **kizárólag a webkimenet és a verziókezelési réteg** kerül. A projekt körüli
belső munkaanyag **szándékosan helyben marad**, és nincs a git-történetben sem:

| Helyi könyvtár | Miért marad ki |
|---|---|
| `_memory/` | belső projektmemória, gépspecifikus — nem a leszállítandó része |
| `_work/` | munkapéldányok, jegyzetek, promptok, nagy médiamentések |
| `_files/` | ügyfél-dokumentumok (ajánlat, stratégia, jogi klauzula) |
| `_OTH_tesztfileok/` | teszt-ajánlatok az OFC modul kipróbálásához |
| `_kepek_videok/` | médiamesterek (434 MB); a git nem bináris-tár |

> Ezek mentése **nem git feladata** — külső meghajtó vagy felhő-tárhely szükséges hozzá.

### Git-történet

- **Friss, tiszta történet.** A könyvtár korábban a Test1 munkaterület másolt `.git`-jét hordozta
  (`de586e6` commit + `v1.0.0` tag, távoli nélkül), ami a Test2 `0.01.01`-es indulásával
  ellentmondásban állt. Az örökölt történet `git bundle`-ként mentve
  (`_work/_backup/okotechhome2-inherited-test1-history.bundle`, helyi), az eredeti pedig
  érintetlenül megvan a `_OkoTechHome/.git`-ben — egyedi adat nem veszett el.
- **Távoli repó bekötve:** `github.com/eSystem-Integration-Kft/okotechhome-web2` (privát),
  fő ág: `main`.
- **Annotált tag:** `v0.01.01`.

---

<p align="center">
  <sub>Ökotech-Home Kft. · fejlesztő: eSystem-Integration Kft. (eSI Kft.), Érd</sub>
</p>
