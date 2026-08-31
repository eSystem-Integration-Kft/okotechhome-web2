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

**Főoldal szövegkönyv v2.1 átvezetve.** A `Főoldal szöveg — javított változat
(v2.1)` dokumentum alapján **69 módosítás 13 szekcióban**: a hero bevezetőjétől
a GYIK válaszaiig. A visszatérő motívum három: (1) az Epureco **forgalmazott**
ülepítő, nem saját gyártású szennyvíztisztító — ezt minden említésnél kimondjuk;
(2) a technológiaválasztást a **terhelés** dönti el, nem az áramellátás vagy az
ingatlantípus; (3) a helyszíni felmérés nem a mi minősítésünk, hanem **díj
ellenében szabadon kérhető szaktanácsadás**. Változáskivonat:
`_files/fooldal-szoveg-v21-atvezetes.html`.

**Ügyfélvélemények — két futó szalag.** Az `Ugyfeltapasztalatok.docx` hét új
visszajelzése átvezetve; a szekció egyesével léptethető idézetdoboz helyett
tizenöt véleményből álló, ellentétes irányban futó szalagpárrá alakult (110 s és
132 s). A kártya a lap **sablonkártyáját** követi — ugyanaz a felület, keret,
sarok, árnyék és belső tér —, és **minden kártya egyforma magas**, a két sor is
egymással: a `min-height` mért maximumból van szabva. Az idézet a szabad tér
közepén áll, így a rövid vélemények alatt nem gyűlik egyetlen lyukká a hely.
Szüneteltető gomb nincs, a szalag `:hover` és `:focus-within` mellett áll meg.

**Főoldal §6 — AI megoldás-ajánló.** A webhely első interaktív eleme: hat rövid
kérdésből megmutatja, melyik szennyvízkezelési megoldás jöhet szóba, és ahol a
helyzet egyértelmű, ott **terméket is nevez**. Ahol nem az, ott kimondja, hogy
vegyes a kép — felsorolva, mi miatt nem lehetett automatikusan dönteni.

**Főoldal §7 — Az A.B. Clear működése.** A metszetkép nem illusztráció a szöveg
mellett, hanem a szekció színpada: teljes szélességű sáv, rajta a tisztítási
folyamat és az iszapzsákos technológia kártyája, a berendezés helyét — és a
felszín fölötti házat — szabadon hagyva. A szekciót az öt működési tény és a telepíthetőség három állapota zárja
— köztük a **kizáró ok**, ugyanolyan súllyal, mint a másik kettő.

**Szippantási díj kalkulátor** — új modul-oldal a `/szippantasi-dij-kalkulator`
útvonalon, a megrendelői brief (Anna) alapján. A brief három díjszabás-szerkezetet
ír le; a modul **egyetlen képlettel** kezeli mindhármat, és megmutatja azt a
tételt, amit a látogató kifizet, de nem szállítanak el érte semmit.

### Hozzáadva

- **§6 — AI megoldás-ajánló (`index.html`).** Kétfelületes modul: bal oldalon
  az asszisztens (egy kérdés, azonnali magyarázat, a következő kérdés
  előnézete), jobb oldalon az élő állapotpanel (hat szakasz állapota, a
  kirajzolódó irány, a kivitelezési feltételek és a tisztázandók). Motor:
  `assets/js/ajanlo.js`, tartalom: `assets/data/ajanlo-konfig.js`.
- **Kétszintű döntési logika a specifikáció szerint.** A TECHNOLÓGIÁT a
  használat jellege és a terhelés dönti el (A.B. Clear · Epureco · szakértői
  egyeztetés), a MEGVALÓSÍTÁS FELTÉTELEIT a telek adottságai. A telek nem
  választ új technológiát — egyetlen kivétellel: a vízelhelyezéshez szükséges
  szabad terület kizáró is lehet.
- **A szabad terület kétlépcsős kiértékelése.** 1. lépcső: elég-e a terület az
  oldómedence szikkasztómezőjéhez (a biológiaiénak 2–3-szorosa)? Ha nem, az
  Epureco irány kiesik — de nem automatikus A.B. Clear ajánlás lesz belőle,
  hanem ellentmondás-jelzés. 2. lépcső: elég-e a biológiai rendszer
  szivárogtatójához? Ha nem, az már nem technológiaválasztás: a zárt tároló
  marad a járható irány. A modul **soha nem közöl méterszámot** arról, mekkora
  szivárogtató kell.
- **Epurecónál a kompromisszum kimondása kötelező** — a kimenet mindig
  tartalmazza, hogy a tisztítás nagy része a talajban történik, alacsonyabb
  tisztítási teljesítménnyel.
- **`.btn-halvany` — csendes gombváltozat.** A „Vissza" nem lehet hangosabb a
  főműveletnél; a meglévő három gomb mind kitöltött. Indoklás: COMPONENTS.md 23/a.
- **Eredmény mentése azonosítóval — `/eredmeny?id=MA-XXXX-XXXX`.** A záró
  képernyőn a látogató elmentheti az eredményt: kap egy **`MA-XXXX-XXXX`**
  kódot és egy címet, ahonnan bármikor előveheti, kinyomtathatja vagy PDF-be
  mentheti. Az azonosító készletéből hiányzik a `0`/`O` és az `1`/`I` — a kódot
  telefonban is be kell tudni mondani. Végpontok: `api/ajanlo-mentes` (mentés),
  `api/ajanlo-eredmeny` (visszaolvasás), tároló: `api/.eredmenyek/`.
- **A mentett rekordban nincs személyes adat.** Se név, se e-mail, se
  telefonszám, se IP: csak a hat válasz és a belőlük számított kimenet.
  A rekord **pillanatkép** — a konfiguráció verziójával együtt tárolva, tehát
  egy későbbi logikaváltozás nem írja át azt, amit a látogatónak mondtunk.
- **`/eredmeny` — új lap.** Azonosító alapján előkeresi a mentett eredményt;
  azonosító nélkül kereső űrlapot kínál. A „Nyomtatás / PDF" a böngésző saját
  PDF-mentését hívja (nincs PDF-könyvtár, ahogy a 11. szekció jelentésénél
  sem), és **az azonosító meg a teljes cím látható szövegként is szerepel** a
  lapon — papíron a kattintható link semmit nem ér.
- **Tartalék, ha a szerver nem elérhető.** Nincs `config.php`, ki van kapcsolva
  vagy hálózati hiba: a modul letölti a szöveges összefoglalót, és **kimondja**,
  hogy szerverre nem került, tehát azonosító sincs.
- **`api/config.php` → `ajanlo` szakasz.** `engedelyezve` és `megorzes_nap`
  (alapérték 180). A mentés végpontja alkalomszerűen takarít.
- **§7 — Az A.B. Clear működése (`index.html`).** Középre zárt szekciófejléc,
  teljes szélességű metszetjelenet két magyarázókártyával, öt működési tény
  sorszámozott rácsban, és a telepíthetőség három állapota kiemelt panelben,
  a kizáró és korlátozó feltételek lapjára mutató CTA-val.
- **Új komponensek: `.mukodes-*`.** `.mukodes-jelenet` (teljes szélességű
  jelenet, arányból számolt magassággal és felső korláttal),
  `.mukodes-jelenet-racs` (kártya · szabad sáv · kártya),
  `.mukodes-kartya`, `.mukodes-lepesek`, `.mukodes-zsak-kepek`,
  `.mukodes-lista`, `.mukodes-feltetelek`, valamint a
  `.situation-grid[data-cols="5"]` variáns. Indoklás: `COMPONENTS.md` 22.
- **Négy új kép.** `mukodes-metszet.webp` (1672×851, `srcset`-tel 1100px-es
  változattal) — a föld alatti metszet; `mukodes-tartaly-kosar-nelkul.webp` és
  `mukodes-tartaly-iszapzsakkal.webp` (480px) — ugyanaz a tartály felülnézetből,
  iszapkosár nélkül és a behelyezett kosárral. A két felvétel együtt mutatja meg,
  mi a kosár szerepe; külön-külön egyik sem mondaná el.
- **Három új ikon.** `ui-iszap-{kosar,zsak,komposzt}.svg` a „Kezelés 3 lépésben"
  sorokhoz, a meglévő készlet nyelvén (24×24, `stroke-width:1.8`,
  `currentColor`), mindhárom fájl fejlécében az **ideiglenes** jelöléssel.
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
- **`app.css?v=160`** és **`kalauz.js?v=39`** mind a 121 lapon (az új `/eredmeny` lappal együtt).

### Módosítva — az Öko kalauz

- **Helyszíni segítség: Öko megszólal, amikor a látogató odaér.** Bármely felület
  felveheti a `data-oko-pont` attribútumot; jelenleg az ügyazonosító mezője és a
  mentés magyarázata ilyen. Csukott panelnél buborék egy mondattal (kattintásra
  a teljes magyarázat és három kérdés), nyitott panelnél Öko egyszerűen
  megszólal a párbeszédben. Pontonként egyszer, és soha annak, aki bezárta.
- **A helyszíni segítség erősebb az általános köszönésnél.** A görgetés
  mindkettőt elindítja, és az események sorrendje nem garantált; a `megerkezik()`
  ezért nem írhatja felül a buborékot, ha már van benne pont-üzenet.
- **Görgetéspozíció, nem IntersectionObserver — és nem `requestAnimationFrame`.**
  Mindkettő a megjelenítés ütemezésétől függ: háttérfülön vagy visszafogott
  rendereléskor nem fut le, és vele a segítség is elmarad. A
  `getBoundingClientRect()` időalapú fékezéssel (150 ms) mindig megmondja, hol
  tart a látogató. Ugyanaz a megfontolás, mint a hero-figyelőnél.
- **Öko megtanulta az ügyazonosítót.** A rendszerprompt külön blokkot kapott:
  mi az, mi NEM (nem regisztráció, nem fiók, személyes adat nélkül), hol adható
  meg, mi történik, ha elvész (nem tudjuk visszakeresni — épp azért, mert nincs
  mellette személyes adat), és meddig él. A **megőrzési idő a konfigurációból**
  megy a promptba, nem beírt számként.

### Módosítva — az azonosítómező kerete

- **A mező a webhely saját űrlapmezője lett** (`.urlap-input`), csak a kód
  alakjához igazítva (mono betű, szűkebb szélesség). Így a mérete, a belső tere,
  a fókuszgyűrűje és a hibaállapota ugyanaz, mint a kapcsolati vagy a
  konzultációs űrlapon.
- **A nyugalmi keret Olive Leaf** (`--border-strong`) a szokásos halvány vonal
  helyett: ez az egyetlen beírható mező a szekcióban, és a sáv többi eleme
  elviszi róla a figyelmet — a márkaszínű keret mondja meg, hova kell írni.
  Ugyanaz a zöld, mint a mellette álló „Betöltés" gombé.
- **A fókuszgyűrű marad a rendszer kékje** (`--border-focus`), és ez szándékos:
  a modul minden KIVÁLASZTOTT állapota zöld (válaszgomb, chip, jelvény). Ha a
  fókusz is zöld volna, a billentyűzettel érkező nem tudná megkülönböztetni, mi
  a kijelölt és mi a fókuszált. A gyűrű a webhely mind a 45 fókuszpontján
  ugyanez — itt sem térhet el. Egérrel kattintva a mező zöld kerettel áll ott;
  a kék csak fókuszban jelenik meg.

### Hozzáadva — a teljes angol fa váza és a nyelvi infrastruktúra

- **`scripts/oldalgyartas/nyelvek.py` — a szlugtérkép.** 121 magyar↔angol
  útvonalpár, ez a többnyelvűség egyetlen forrása: ebből épül az angol lapok
  helye, a `hreflang` páros, a nyelvváltó célja és a belső hivatkozások
  átírása. A szlugok angolul vannak, nem a magyar átirataként — ezért a
  párosítás nem számítható ki az útvonalból, kizárólag ez a tábla adja.
  Ellenőrizve: pontosan lefedi mind a 121 lapot, ütköző angol szlug nélkül.

- **`nyelvi_klon.py` — a lapvázak generálása.** Nyelv és gyökérjelölés,
  eszközútvonalak, a fejléc és a lábléc átemelése a kész angol nyitólapról, és
  a belső hivatkozások átirányítása: ahol már van angol változat, oda; ahol
  nincs, a magyar lapra `hreflang="hu"` jelöléssel. **Szöveget nem fordít** — a
  gépies és az ítéletet igénylő munka külön lépés. Meglévő lapot alapból nem ír
  felül: egy kész fordítás elvesztése sokkal drágább, mint egy kihagyott váz.

- **`nyelvi_parok.py` — a lappárok összekötése.** Kölcsönös `hreflang` mindkét
  lapon, és a nyelvváltó a lap SAJÁT párjára. Újrafuttatható.

  Három hibát kellett menet közben javítani, mind a relatív útvonalakból:
  · az `en/` fa maga is egy szinttel lejjebb van, ezért a nulla mélységű angol
    lapok `en/assets/…`-t kértek, ami nincs;
  · a magyar lapra mutató tartalék hivatkozást naivan toldalékoltam ahelyett,
    hogy kiszámoltam volna — 198 cím mutatott `en/`-en belülre;
  · az átemelt fejléc és lábléc hivatkozásai a NYITÓLAP mélységéhez készültek,
    egy alkönyvtárban máshova visznek — további 136 törött cím.

  Végállapot: **246 lap, 0 HTML-hiba, 0 saját törött hivatkozás, 0 nem
  kölcsönös `hreflang`.** A megmaradt 23 törött cél a magyar fán is törött —
  a sitemapban szereplő, még meg nem épített lapok.

  ⚠️ **A 119 új angol lap TARTALMA egyelőre magyar.** A váz kész és helyes; a
  fordítás (~71 000 szó) szakaszosan következik, klaszterenként commitolva.

### Hozzáadva — angol konzultációs lap és a nyelvi visszautak

- **`/en/consultation`** — a második angol lap, kb. 1000 szó. Azért ez jött
  másodikként: a fejléc CTA-ja ide mutat, és angol nyelvű látogatót egy teljesen
  magyar űrlapra dobni a konverziós út legrosszabb pontja. A fejlécet és a
  léblécet a már lefordított nyitólapból emeltem át, nem újrafordítva —
  így nem tud elcsúszni a kettő.

- **Javítva: 33 lefordítatlan felirat maradt bent, mert a keresésem ékezetre
  szűrt.** A „Folytatom", a „Nincs", a „Van", a „Vissza", a „Szempont", a
  „Weboldal" és társaik ékezet nélküliek — az ellenőrzőm pedig a magyar szöveget
  ékezetes betűk alapján ismerte fel, tehát ezeket rendre átengedte, és a lapot
  „0 magyar szó" eredménnyel jelentettem késznek.

  Az új ellenőrzés nem talál, hanem **összevet**: kigyűjti a lap szövegcsomóit és
  attribútumait, majd megnézi, melyik egyezik SZÓ SZERINT a magyar forráslapéval.
  Ami mindkettőben ugyanaz, az vagy tulajdonnév, vagy lefordítatlan maradék — és
  a kettő szétválasztható. Ez az ékezet nélküli szavakat is megfogja. Mindkét
  angol lap most 0 maradékkal zár.

- **Javítva: a lábléc helyére egy véleményszerző-blokk került.** Az angol
  konzultációs lap készítésekor a láblécet az `<footer` elem első előfordulására
  illesztve emeltem át a nyitólapról — a véleménykártyák szerzőblokkja viszont
  szintén `<footer`, így a lap aljára „Zoboki Dávid · Pilisszentlászló" került,
  valódi lábléc helyett. Osztályra illesztve (`<footer class="lablec">`) javítva.
  A fejléc kivágása nem volt érintett: az egyetlen eltérés a nyelvváltó címe,
  ami szándékos.

- **A nyelvváltó a lap SAJÁT párjára mutat**, nem a nyitólapra. Eddig a magyar
  konzultációs lapról az EN gomb az angol nyitólapra vitt, ami elveszíti a
  kontextust; most `konzultacio` ↔ `en/consultation`. A `hreflang` mindkét
  irányban ki van írva — az egyoldalú bejegyzést a Google figyelmen kívül
  hagyja.

- **Az angol lapok CTA-i az angol konzultációra mennek.** A nyitólapon két
  hivatkozás és a fejléc gombja is át lett irányítva.

- Ellenőrizve: az angol fából **nulla törött hivatkozás**, és a nyitólapon
  hiányzó 23 cél pontosan ugyanaz a 23, ami a magyar nyitólapról is hiányzik —
  ezek a sitemapban szereplő, még meg nem épített lapok, nem a fordítás hibái.

### Hozzáadva — Öko kalauz angolul

- **A kalauz felülete nyelvenkénti szótárból dolgozik** (`kalauz.js`): köszönés,
  alcím, súgó, helyőrző, belépő kérdések és a félretett fül időnkénti kérdései,
  mindhárom módban (kalauz, űrlap, jelentés). A görgetésre megszólaló
  magyarázatok (`PONTOK` — ügyazonosító, mentés) szintén.

- **A laptémák (`TEMAK`) magyarok maradnak, szándékosan**: a mintáik magyar
  útvonalakra illeszkednek, és angol aloldal még nincs. Az angol lapon így az
  alap szövegek érvényesülnek — nem hibás állapot, hanem a jelenlegi lapkészlet
  következménye.

- **A szerver a látogató nyelvén válaszol.** A kliens elküldi a `<html lang>`
  értékét, a `kalauz.php` pedig **egyetlen nyelvi utasítást fűz a prompt
  végére** — nem külön angol promptot. A szakmai tudás, a tiltólista és a
  viselkedési szabályok így egy forráson maradnak: két párhuzamos prompt
  előbb-utóbb elcsúszna, és a hiba épp azon a nyelven jelentkezne, amit
  ritkábban nézünk.

- **A hibaüzenetek is a látogató nyelvén.** Aki az angol lapon kérdez, ne magyar
  mondattal találkozzon, amikor épp elakadunk — az a kettős kudarc. Mind a négy
  végponti üzenet (napi keret, üres kérdés, hiányzó index, elérhetetlen modell)
  nyelvfüggő.

- **A kalauz indexében már benne van az angol nyitólap** (`/en/`), tehát Öko
  hivatkozhat rá. A többi hivatkozott lap egyelőre magyar — a prompt utasítja
  Ökót, hogy ezt **mondja ki egyszer, tárgyilagosan**, ne hallgassa el és ne
  mentegetőzzön miatta.

### Hozzáadva — a két modul angolul

- **A megoldás-ajánló tartalma nyelvenkénti fájlba került.** Az
  `ajanlo-konfig-en.js` az `ajanlo-konfig.js` angol párja: azonos szerkezet,
  azonos kulcsok, **azonos válaszazonosítók** — csak a megfogalmazás más. Az
  azonosítók szándékosan magyarok maradnak: a döntési szabályok, a mentett
  ügyrekordok és a CRM-átadás mind ezekre kulcsolnak, és egy mentett eredménynek
  ugyanazt kell jelentenie, bármelyik nyelven készült. Géppel ellenőrizve: a
  kérdés- és válaszazonosítók, a szabályok, a területsávok, a termék-, feltétel-
  és tisztázandó-kulcsok mind egyeznek a két fájlban.

- **Az ársávbecslő kérdései ugyanígy** (`ai-advisor.js`, `KERDESEK` tábla): 35
  azonosító, mindkét nyelven azonos. Az árak továbbra is egyetlen helyen élnek
  (`aidt-konfig.js`) — az nyelvfüggetlen, mert számokat tartalmaz.

- **A felületi feliratok szótárba kerültek** mindkét motorban (`SZOVEG`, `T`),
  a `<html lang>` alapján választva. A tartalom nyelvenkénti konfigurációs
  fájlban él, a felület a motorban: az elsőt a cég szerkeszti, a másodikat nem.

- **Rögzített szakmai szótár** — hogy a további lapokon se csússzon el:
  oldómedence = *septic tank*, zárt tároló = *sealed holding tank*,
  szikkasztómező = *drainage field*, szivárogtató = *soakaway*,
  kiemelt szivárogtató = *raised soakaway*,
  speciális rögzítés = *anti-flotation anchoring*,
  tisztázandók = *points to clarify*.

- **Gyökér-előtag a nyelvi alkönyvtárakhoz** (`ugy.js`). A modulok a lap
  könyvtárához képest hívták az API-t, tehát az angol lapról `/en/api/...`-ra
  mutattak volna — ami nincs. A lap most a `<html data-gyoker="../">`
  attribútummal mondja meg, hol a gyökér; a gyökérben álló lapokon az attribútum
  hiányzik, és az előtag üres.

  ⚠️ Öko kalauz **még magyarul válaszol az angol lapon is**. Megrendelői döntés,
  hogy ez akkor kerül sorra, amikor a teljes angol lapkészlet megvan — a
  keresőindexe úgyis csak akkor tud angol lapokra hivatkozni.

### Hozzáadva — angol nyitólap (`/en/`)

- **A főoldal angol változata elkészült** (`_web/en/index.html`), mintaként: ezen
  hagyható jóvá a hangnem és a szakmai szótár, mielőtt a további 124 lap
  fordítása elindul. Kb. **7 000 szó**, a teljes szerkezettel — megamenü, mind a
  tizenhárom szekció, a 14 kérdéses GYIK, a lábléc, a `FAQPage` JSON-LD, és
  minden `alt`, `aria-label`, `title`, `placeholder`.

- **Angol szlugok**, a `/en/` alkönyvtárban. A magyar↔angol párosítást a lapok
  saját `hreflang` hivatkozásai tartják nyilván, mert a szlugok eltérnek, tehát a
  másik nyelv címe nem számítható ki az útvonalból.

- **A `fejlec.py` mostantól kihagyja a nyelvi alkönyvtárakat.** A generátor
  magyar feliratokkal és magyar szlugokkal dolgozik: egy futtatás némán
  visszaírta volna a magyar fejlécet az angol lapra. A `MENU` nyelvenkénti
  táblává bontása akkor lesz esedékes, amikor az angol fa megnő.

- **Az angol lap belső hivatkozásai a magyar lapokra mutatnak**, `hreflang="hu"`
  jelöléssel — így a képernyőolvasó és a böngésző is tudja, hogy nyelvet vált.
  Ez a fokozatos bevezetés bevett gyakorlata; ahogy elkészülnek az angol lapok,
  a hivatkozások átállnak.

  ⚠️ **Amit az angol lap MÉG NEM tud.** A §6 megoldás-ajánló és a §8
  ársávbecslő tartalma közös JS-fájlokból jön (`assets/data/ajanlo-konfig.js`,
  `aidt-konfig.js`), Öko tudásbázisa pedig a `kalauz-*.json`-ból — ezek
  **magyarul jelennek meg az angol lapon is**. A `<noscript>` tartalék viszont
  már angol. Ez további kb. 12 000 szó, és nyelvi szétválasztást igényel a
  modulokban; a nyitólap jóváhagyása után érdemes nekifutni.

### Hozzáadva — nyelvváltó és a többnyelvűség szerkezete

- **Nyelvváltó a fejlécben** (`.nyelvvalto`), a témaváltó és a CTA között, mind a
  121 lapon. Az aktuális nyelv nem hivatkozás, hanem `span` `aria-current`-tel:
  önmagára mutató link zavaró, és a képernyőolvasónak sincs mit bejelentenie
  rajta.

- **A szerkezet: nyelvenként külön alkönyvtár** (`/en/`, később `/de/`), saját
  lapkészlettel. Ez a lényeg abban a kérdésben, hogy „mi lesz azzal, ami magyarul
  megvan, angolul viszont nem kell": **semmi** — az angol lapkészletnek nem kell
  tükröznie a magyart. Amiből nincs fordítás, arról egyszerűen nincs `hreflang`
  bejegyzés, és a váltó az adott nyelv nyitólapjára visz, nem 404-re.

  A cél címét szándékosan **nem az útvonalból számítjuk**: a szlugok nyelvenként
  mások (`megoldasok/ab-clear` ↔ `en/solutions/ab-clear`), tehát nincs mit
  kiszámolni. A leképezést minden lap a saját `hreflang` hivatkozásaiban hordozza
  — így a váltó laponként pontos, és a keresők is ugyanabból az egy forrásból
  kapják meg a párosítást. A `hreflang` kölcsönös kell legyen: az egyoldalú
  bejegyzést a Google figyelmen kívül hagyja.

### Javítva — a menüfiók

- **A menü tartalma kattintás nélkül kilógott a lapra** 1025 és 1240 pixel
  között. Az előző lépésben a CSS töréspontját 1240-re vittem, a fiókot becsukó
  JS viszont 1025-öt figyelt: a köztes szélességeken a `details` nyitva maradt,
  miközben a CSS már lebegő panelként jelenítette meg. A `site.js` mostantól
  saját, a CSS-sel **egyező** töréspontot használ (`min-width: 1241px`), és a
  megjegyzés kimondja, hogy a kettőnek együtt kell mozognia.

- **A panel a teljes fejléc alatt nyílik, saját görgetéssel.** Két korábbi
  próbálkozás bukott meg ezen: a fejléc jobb széléhez tapadva a gombtól
  elszakadva lebegett; a gombhoz kötve pedig — mivel `position:absolute`, tehát
  nem tolja lejjebb a lapot — a háromszintű menü **alja levágódott**, és nem
  lehetett hozzáférni. A „majd a lapot görgeti a látogató" feltevés abszolút
  pozicionálású panelnél nem áll: nincs mit görgetni.

  Most a viszonyítási pont a `.header-main`, a panel végigfut a fejléc
  szélességében, a magassága korlátos, és saját görgetést kap. Mérve 1150×583-as
  ablakban, kinyitott almenüvel: 1756 pixelnyi tartalom egy 408 pixeles panelben,
  a képernyő alá lógás nélkül, minden hivatkozás elérhető.

  A magasságkorlát **arány, nem kiszámolt pontos érték** (`min(70dvh, 100dvh − 9rem)`).
  A panel teteje a fejlécverem alján kezdődik, aminek a magassága a sticky sáv
  elgörgetésével változik — egy fix tokenből levont képlet ezért éppen a
  legszűkebb esetben téved. Az első kísérletem pontosan így lógott 45 pixellel
  a képernyő alá.

### Módosítva — levegő a menüben, és egy hajszálvonal

- **A menüpontok köze rugalmas**, ahogy a betűméret is: 1241 képpontnál 8px,
  1680-nál 24px. Széles képernyőn mérve 341 pixel maradt szabadon a fejlécben,
  és a menü ott zsúfoltnak látszott; a szűk végén viszont minden képpont
  számít, ezért ott marad a korábbi érték. A menüpontok belső terével együtt két
  felirat között 16-tól 32 képpontig terjed a távolság.

- **Hajszálvonal a menü és a két kapcsoló között.** A témaváltó és a nyelvváltó
  egy csoport — beállítások, nem navigáció —, és a vonal ezt mondja ki egy
  képpontnyi jellel, keret és háttér nélkül. A `.tema-doboz` első flex eleme,
  tehát a kapcsolókkal együtt tűnik el, ha a téma-szkript nem futott le.

### Javítva — Öko magyarul válaszolt az angol lapon

- **A nyelvi utasítás egy hosszú magyar prompt végén állt, és alulmaradt.**
  Mérve: az angol URL-ekhez tartozó 883 szövegrészből **761 még magyar**, mert
  121 lapból 26 van lefordítva. A kalauz ezekből a részletekből olvas, és
  átvette a nyelvüket.

  Az utasítás mostantól a prompt **elején is** ott áll egy sorban, a végén pedig
  megerősítve: kimondja, hogy a forrás nagyrészt magyar, hogy ez a forrás
  tulajdonsága és nem utasítás, és hogy éppen ez a legvalószínűbb hiba itt.

  ⚠️ Ez a tünetet kezeli, nem az okát. A kalauz adatbázisa **csak a fordítás
  befejezése után lesz teljes**, és az eredménykártyák részletei addig magyarul
  jelennek meg, mert azok az indexből jönnek, nem a modelltől. A teljes
  ellenőrzés a fordítás lezárása utánra marad.

### Módosítva — a fejléc egy sorban marad

- **A navigáció betűmérete rugalmas**: `clamp(11px, 0.68vw + 2.6px, 14px)`.
  1680 pixelen 14px, 1240-en 11px, lineárisan közte. Nem a szerkezet törik meg,
  hanem a betű enged — mérve mindkét nyelven, 1241-től 1680-ig **egyetlen sor**,
  túlcsordulás nélkül.

- **A fejléc szélesebb, mint a törzstartalom** (`--header-container:1680px` a
  tartalom 1440-e helyett, `--header-gutter:32px` a 48 helyett). A törzsszöveg
  azért áll meg 1440-nél, mert hosszabb sort kényelmetlen olvasni; a fejlécben
  viszont nincs olvasandó sor, csak hat menüpont, két kapcsoló és egy gomb —
  ezeknek a hely kell, nem a mértéktartás.

- **A menüpontok belső tere 8-ról 4 pixelre szűkült**, így két felirat között
  16px marad (4 + 8 oszlopköz + 4).

- **A fejléc navigációja saját, tágabb töréspontot kapott (1240px)**, nem a
  tabletét (1024px). A hat nagybetűs menüpont 1240 alatt akkor sem fér el egy
  sorban, ha a betű a legkisebb megengedett fokán áll — a feliratok egyszerűen
  hosszabbak ennél. Tördelt, kétsoros fejléc helyett ott már a lenyitható panel
  jön.

- **A lenyitott panelben a betű visszakapja a 14 pixelt.** A rugalmas méret a
  fejlécsor szűkösségét oldja meg; a panelben nincs vízszintes szorítás, egy
  11px-es érintőmenü pedig csak rossz volna. A panel szélessége `70vw`-ről
  `min(92vw, 420px)`-re nőtt: a háromszintű menü behúzásai mellett a hosszabb
  aloldalcímek korábban négy sorba törtek.

### Módosítva — a fejléc tipográfiája

- **A főnavigáció saját tipográfiai szerepet kapott** (`.type-ui-nav`, 14px), egy
  fokkal a gombszöveg (15px) alatt — hogy a nyelvváltó elférjen. Nem a
  gombtokent írtuk át: a gombokon a 15px maradt.

  Egy buktató: a `.nav-trigger` a komponensrétegben **újra kimondja** a
  betűméretet, mert a `button` nem örökli a betűt — és mivel a komponensréteg a
  tipográfiai fölött áll, az osztálycsere önmagában nem ért volna el idáig. Ezt
  is át kellett állítani, különben a lenyíló menüpontok 15px-en maradtak volna,
  a többi 14-en.

- **A menüpontok köze 16-ról 8 pixelre szűkült.** A menüpontoknak saját 8px
  belső terük is van, tehát két felirat között így is 24px marad. A betűméret és
  a köz együtt annyi helyet szabadított fel, amennyit a nyelvváltó elfoglal: a
  fejléc nem lett szélesebb, mint előtte volt.

### Módosítva — a hero felvétele

- **Új hero-videó és -állókép, teljes 1080p-ben.** A korábbi felvétel 1280×722-es
  volt; az új a forrás teljes felbontásán, **1920×1080** (pontos 16:9) fut.
  A jelenet ugyanaz — családi ház naplementében, feltárt munkagödörben az
  A.B. Clear és a szikkasztóalagút —, ezért az `alt` szöveg érvényes maradt.

  | fájl | régi | új |
  |---|---|---|
  | `hero-rendszer.webm` (VP9) | 1,3 MB · 1280×722 | 2,6 MB · 1920×1080 |
  | `hero-rendszer.mp4` (H.264) | 1,2 MB · 1280×722 | 2,7 MB · 1920×1080 |
  | `hero-rendszer-allokep.webp` | 157 KB · 1600×893 | 200 KB · 1600×900 |

  A tömörítés nem a legmagasabb fokon áll: VP9 CRF 32 mellett a fájl 5,8 MB
  lett volna, CRF 44 mellett viszont a talaj textúrája és a kavics már láthatóan
  elkenődött. **CRF 40** az a pont, ahol a részlet még megvan. A videó csak
  széles nézetben, `prefers-reduced-motion` nélkül és `saveData` nélkül tölt be,
  és az állókép után — az LCP-elem az állókép, nem a felvétel.

- **Az állókép a 4,2. másodperc kockája, nem az első.** Ott már folyik a
  tisztított víz a szikkasztóalagútból, és a tartály is tele van — ez az a kép,
  ami magában is elmondja, mit csinál a rendszer. A kezdőkocka ehhez képest
  üresnek látszik. A videó átúszik az állóképre, tehát a kis kompozíciós
  eltérés nem látszik; mobilon, csökkentett mozgás mellett és adattakarékos
  módban pedig **ez az állókép marad az egyetlen kép** — annak kell a legjobbnak
  lennie, nem a videó első pillanatának.

- **A `height` 902-ről 900-ra javítva.** A jelölésben megadott magasság eddig
  nem egyezett a fájléval (893 px), ami elrendezés-ugrást okozhatott. Az új
  képek pontosan 16:9-esek, és a `<head>` `preload` sorai is az új verziót
  töltik elő — enélkül a böngésző a régit szedte volna le.

### Módosítva — záró kitételek

- **A 8. szekció záró jogi kitétele középre került**, felső elválasztó vonallal:
  a modul utolsó szava ne olvadjon bele a fölötte lévő blokkokba.
- **A 6. szekció záró megjegyzése ugyanígy** (`.section-note-kozep`): ott nem
  egyetlen számhoz tartozó lábjegyzet áll, hanem az egész szekcióra vonatkozó
  kitétel — a bal élhez tapadva árválkodott.

### Eltávolítva

- **A hero magyarázó bekezdése parkolóra került** (megrendelői kérés). Nem
  törölve: a jelölésben kommentben, szó szerint megmarad, és a `.hero-jegyzet`
  stílusa is a helyén maradt — a visszatétel egyetlen lépés.

- **Az ügyfélvélemények megállító gombja és a `assets/js/velemeny.js`.**
  Megrendelői döntés: a hover úgyis megállítja a szalagot, a gomb pedig idegen
  elem volt a vélemények alatt. A szkriptnek ezzel nem maradt feladata — a
  mozgást, a megállítást és a rendezést is a CSS viszi.

  ⚠️ **Vállalt eltérés:** a szekció így nem teljesíti a WCAG 2.2 SC 2.2.2
  pontját. Érintőképernyőn nincs hover, a fókusz sem feltétlenül jut a szalagra,
  és a `prefers-reduced-motion` nem számít teljesítési módnak. Ha az
  EAA-megfelelés előkerül, a javítás nem a gomb visszatétele, hanem egy
  **lapszintű „mozgás csökkentése" kapcsoló** a fejlécben — az egy helyen, a lap
  összes animációjára megoldja.
- **A kártyák nagy, halvány Zilla Slab idézőjele.** A megadott fokon és
  áttetszőségben nem jelnek látszott, hanem elgépelésnek. Helyette valódi magyar
  idézőjelpár áll az idézet körül, a szöveg fokán.

### Javítva

- **Öko elnyelte a kiszolgáló saját üzenetét.** A `kalauz.js` gondosan
  továbbvitte a végpont indoklását (`throw new Error(eredmeny.uzenet)`), a
  `catch` viszont **kötés nélkül** állt — eldobta, és helyette mindig ugyanazt
  az általános mondatot mutatta. Így a napi keret betelését jelző üzenet
  sosem jutott el a látogatóig, és minden hiba egyformán nézett ki:
  hiányzó kulcs, lejárt keret, rossz origin, hálózati hiba. A dobott hiba most
  meg van jelölve (`othUzenet`), és a `catch` a kiszolgáló szavát mutatja —
  a böngésző angol, technikai üzenetét továbbra sem. A `kalauz.php` két
  hibaüzenete megkapta a telefonszámot, ami eddig csak a kliens általános
  mondatában szerepelt: ha Öko nem tud segíteni, a telefon a következő lépés.

- **Az ajánlat-elemzés nem találta az API-kulcsot, a CRM-titkok viszont igen.**
  Nem a CRM-átadás vitte el: pontosan fordítva. A CRM-titkok útvonallistája
  három mélységet sorol (`../`, `../../`, `../../../`), az AI-kulcsé viszont
  csak egyet (`../../`) — a tesztoldal gyökere pedig eggyel mélyebben ül, mint
  amit ez a fix útvonal elér. Így a CRM megtalálta a magáét, az AI-kulcs nem, és
  az `ajanlat-elemzes.php` a „nem elérhető" ágra futott.

  Az `oth_titok()` most **felfelé is keres**: a megadott útvonalak után korlátos
  (5 szint) sétával végignézi minden fölöttes szint `oth-titkok/` könyvtárát
  ugyanarra a fájlnévre. Így a titkok megtalálása nem függ attól, milyen mélyen
  ül a webgyökér — se itt, se a CRM-nél.

  Ha mégsem talál, a hiba nem néma többé: a naplóba bekerül **minden kipróbált
  útvonal**, és külön az `open_basedir` értéke, ha aktív — megosztott tárhelyen
  ez a leggyakoribb ok, amiért a webgyökér fölötti fájl olvashatatlan. A titok
  ÉRTÉKE természetesen sosem kerül a naplóba.

  ⚠️ A `config.php` nincs a repóban (nem is lehet), ezért a javítás a szerveren
  csak akkor él, ha az ottani `config.php` `oth_titok()` függvénye is frissül.

- **A jeleneten álló két felvétel közül a jobb oldali kisebbnek látszott.** Az
  elválasztó vonal a második kép `border-left`-je volt: a globális
  `box-sizing:border-box` miatt a keret és a belső térköz a `width:100%`-on
  belülre esett, és 17px-kel szűkítette a kép tartalmát. A vonal átkerült a rács
  `::before` pszeudoelemére. A képaláírások elmaradtak (a terven sincsenek): a
  hosszabb felirat két sorba tört, és `align-items:end` mellett a saját képét
  feljebb tolta.
- **A vonal és a sorszámkorong nem volt egy tengelyen.** A `.situation` vonala a
  hasáb tetején állt, a korong 33px-rel lejjebb — két külön jel, üres sávval. A
  korong fél magasságnyival feljebb került, így a vonal a közepén fut át.
- **Árva szó a szekcióbevezető végén.** A `.section-lead` `text-wrap:pretty`-t
  kapott: az utolsó sorra nem maradhat egyetlen szó.
- **A középre zárt szekciófejléc bevezetője balra csúszott.** A `.section-lead`
  62ch-s korlátja keskenyebb a konténernél, `margin-inline:auto` nélkül a blokk
  a bal élhez tapadt, és a benne középre zárt szöveg optikailag elcsúszott a cím
  alatt. A `.section-head-start` alatti visszaállítás eddig is a stíluslapban
  állt — a párja hiányzott. A §9 (*Üzemeltetés és hosszú távú költség*) fejléce
  is ettől volt ferde.

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

### Biztonság

**Robotpolitika — „letöltés igen, hasznosítás nem".** A `tst.okoth.hu` és az
`okoth.hu` eddig `Disallow: /`-val zárta ki a robotokat. Ez visszafelé sült el:
amit a `robots.txt` kizár, azt a robot **le sem tölti**, így a `noindex` fejlécet
sem látja — és a máshonnan mutató linkek alapján az URL címként mégis bekerülhet
az indexbe. Az új felállás megfordítja a rétegeket:

- **`_web/robots.txt`** — az általános botoknak a letöltés szabad (`Allow: /`),
  egyedül az `/api/` marad kizárva. Az `assets/` szándékosan nyitva van: enélkül
  a kereső hiányosan rajzolná ki a lapot.
- **Név szerinti tiltás** ugyanott, két csoportban: AI-tanító és AI-kereső (GEO)
  ügynökök — GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Applebot-Extended,
  Bytespider, CCBot, meta-externalagent és társaik —, valamint SEO-elemző és
  backlink-figyelő botok: AhrefsBot, SemrushBot, MJ12bot, DotBot, BLEXBot,
  DataForSeoBot, Screaming Frog és a többi.
- **`_web/.htaccess` A) réteg** — az `X-Robots-Tag` kibővült a kivonat- és
  előnézet-korlátokkal (`max-snippet:0`, `max-image-preview:none`,
  `max-video-preview:0`) és a `noai`/`noimageai` jelzéssel. Ez a GEO ellen való:
  amiből nem idézhető részlet, azt az AI-válaszgeneráló sem építheti be.
- **`_web/.htaccess` B) réteg** — a `robots.txt` csak kérés, ezért ugyanaz a
  névsor `SetEnvIfNoCase` User-Agent-szűrővel **403-at** is kap: a tanítóadat-
  gyűjtő le sem tölti a lapot. A `robots.txt` és a `403.html` szándékos kivétel —
  ha a tiltott bot a `robots.txt`-re 403-at kapna, azt az RFC 9309 szerint
  „nincs korlátozás"-ként értelmezhetné.
- **Mind a 124 oldal** `<meta name="robots">` sora ugyanazt mondja, mint a
  fejléc; a négy oldalgyártó sablon (`sablon.py`, `jelentes_oldal.py`,
  `szippantasi_kalkulator.py`, `hibaoldalak.py`) is frissült, hogy az újragenerálás
  ne írja vissza a régit.

Ellenőrizve helyi Apache 2.4-gyel: böngésző, Googlebot és Bingbot 200-at kap
`X-Robots-Tag: noindex`-szel, a GPTBot / ClaudeBot / PerplexityBot /
Google-Extended / CCBot / Bytespider / AhrefsBot / SemrushBot / Screaming Frog /
MJ12bot 403-at, a `robots.txt` viszont mindenkinek kimegy.

**Az Öko kalauz érintetlen.** Ellenőrizve: a `/api/kalauz` POST a látogató
böngészőjéből 200-at kap, a `kalauz.js`, az `ai-advisor.js` és az
`assets/data/` konfigfájlok is elérhetők; a `kalauz-index.json` és a
`config.php` továbbra is zárva (ezt az `api/.htaccess` intézi, változatlanul).
A kalauz kifelé hív (`api.anthropic.com`), az indexét pedig helyi fájlokból
építi (`scripts/kalauz-index.py` az `_web/` HTML-jeit olvassa), ezért sem a
`robots.txt`, sem az UA-szűrő nem áll az útjába. Botként ugyanez a végpont
403 — az AI-hívásnak ára van, és nem a tanítóadat-gyűjtőké.

### Amire adat kell — kérni

- **Az adatkezelési tájékoztató kiegészítése.** A megoldás-ajánló mentett
  eredménye a szerveren tárolódik (azonosítóval, személyes adat nélkül, 180
  napig). A tájékoztató ezt jelenleg **nem említi** — élesítés előtt be kell
  írni, és a megőrzési időnek egyeznie kell a `config.php`
  `ajanlo.megorzes_nap` értékével.
- **A megoldás-ajánló döntési logikájának jóváhagyása** (a specifikáció 8.
  pontja): a három használati kategória definíciója és a hozzájuk rendelt
  termékek, a határesetek listájának teljessége, a terméknevesítés elve, és a
  szabad területre vonatkozó kérdés m²-sávjai. A sávhatárok jelenleg
  **munkahipotézisek** az `ajanlo-konfig.js`-ben, nem méretezési adatok.
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
