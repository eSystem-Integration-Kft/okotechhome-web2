# `_web/` — webkimenet

Ez a könyvtár a **deployolható statikus site** gyökere, egyben a repó tulajdonképpeni hatóköre.
Kizárólag ennek a tartalma kerül élesre — a repó gyökerében élő `README.md`, `CHANGELOG.md`,
`VERSIONING.md`, `VERSION`, `scripts/` és `.github/` **nem**, és az itteni `README.md`,
`COMPONENTS.md`, `serve.py` sem.

## ⚠️ TESZT ÜZEMMÓD — élesítési ellenőrzőlista

Az oldal jelenleg a **`https://tst.okoth.hu`** aldomainen fut, és **minden keresőmotor
elől el van zárva**. Az éles domain: **`https://okoth.hu`**.

A zárás **három rétegben** él — élesítéskor mindhármat fel kell oldani:

| # | Hol | Mit kell tenni élesítéskor |
|---|---|---|
| 1 | `.htaccess` → *TESZT ÜZEMMÓD* blokk | az `X-Robots-Tag` sort törölni vagy kikommentezni |
| 2 | `robots.txt` | a `Disallow: /` helyére az élesítési változat (a fájlban kommentben ott áll) |
| 3 | minden HTML `<head>` | a `<meta name="robots" content="noindex, …">` sort törölni |

**Külön, a keresőktől független megfelelőségi pont:** a Kapcsolat oldalon a Google
Térkép **alapértelmezésben** töltődik be. A beágyazás sütit tesz le és elküldi a
látogató IP-jét a Google-nek, ezért a **cookie-tájékoztatóban nevesíteni kell**
(harmadik féltől származó süti, cél, adatkezelő), és a cookie-hozzájárulásnak ki kell
terjednie rá. Amíg ezek nem élnek, ez nyitott pont — a beágyazás a
`kapcsolat.html` `.terkep` szekciójában van.

### Google-térkép — a Maps API-kulcs beállítása

A kapcsolat oldal térképe **két üzemmódot** ismer, és kulcs nélkül is működik.

| | kulcs nélkül (mai állapot) | kulccsal |
|---|---|---|
| térkép | beágyazott `iframe` | valódi Maps JavaScript API |
| logós jelölés | saját réteg a keret fölött; húzáskor eltűnik | **valódi térképjelölő**, a házon marad |
| színezés | CSS-szűrő + fátyol | a Google saját stílusrétege, a designtokenekből |
| külső forrás | `www.google.com` | + `maps.googleapis.com`, `maps.gstatic.com` |

**A kulcs beszerzése** (Google Cloud Console): új projekt → *APIs & Services* →
**Maps JavaScript API** engedélyezése → *Credentials* → **Create credentials → API key**.
A projekthez számlázási profil kell; egy kapcsolat oldal forgalmát a havi ingyenkeret
fedezi, de a profil nélkül a térkép „for development purposes only" vízjelet kap.

**A kulcsot korlátozni KELL.** Ez a kulcs a böngészőben fut, tehát bárki elolvashatja
az oldal forrásából — ez nem hiba, hanem a Maps JS API működése. Nem a titkosság védi,
hanem a korlátozás: *Application restrictions* → **Websites**, és vedd fel a
`https://okoth.hu/*` és `https://tst.okoth.hu/*` mintát. *API restrictions* → csak a
**Maps JavaScript API**. Korlátozás nélkül a kulccsal más webhelyről is lehet a te
számládra terhelni.

**Beállítás:** a kulcs a `kapcsolat.html` `<section class="terkep" …>` elemének
`data-terkep-kulcs` attribútumába kerül (és a `scripts/oldalgyartas/kapcsolat.py`
`terkep_kulcs` változójába, hogy az újragenerálás ne írja felül). Üresen hagyva minden
a mai módon működik — a kulcs hiánya nem tör el semmit.

**A `.htaccess` CSP-je** külön blokkban engedi a Maps forrásait, kizárólag a
`kapcsolat.html`-re. Ebben szerepel a `style-src 'unsafe-inline'` is, mert a Maps a
saját elemeit beágyazott stílussal formázza. **Élesítés után érdemes megpróbálni
nélküle:** ha a böngésző konzoljában nincs CSP-hiba és a térkép hibátlan, vedd ki —
a beágyazott stílus engedélyezése egy XSS-hez való támadási felület. A `serve.py`
ugyanezt a fejlécet küldi helyben, hogy az eltérés ne csak élesben derüljön ki.

**Második nyitott megfelelőségi pont: a hivatkozások aláhúzása.** A hivatkozások
alapállapotban aláhúzás nélkül állnak (`a{text-decoration:none}`), egérrel és
billentyűzet-fókuszban aláhúzottak. Ez a **különálló** hivatkozásoknál (telefon,
e-mail, menü, kártyacím) rendben van. A **folyószövegbe ágyazott** hivatkozásnál a
WCAG 2.2 1.4.1 nem-szín alapú megkülönböztetést vár: a linkszín (`--link`, `#2F6F82`)
és a törzsszöveg (`--text-primary`, `#133216`) kontrasztja **2,49:1**, ami a 3:1 alatt
van, tehát ott formailag hiányosság. Világos háttéren ez nem is oldható meg pusztán
színnel: a 3:1 a szöveghez és a 4,5:1 a háttérhez egyszerre nem teljesíthető.
Ha az EAA-megfelelés élesben követelmény, a folyószövegbe ágyazott linkeknél
vissza kell tenni egy vékony aláhúzást — egyetlen szabály az `app.css` `@layer base`
blokkjában: `p a,li a{text-decoration:underline;text-decoration-thickness:1px;
text-underline-offset:.18em}`.

**Miért három réteg.** Önmagában a `robots.txt` nem elég: az URL link alapján akkor is
indexelődhet, tartalom nélkül. Az `X-Robots-Tag` fejléc a valódi tiltás, a `<meta>` pedig
akkor is véd, ha a fájl olyan szerverre kerül, ahol a `.htaccess` nem érvényesül.

**A legerősebb védelem a jelszó.** A `.htaccess`-ben előkészítve, kommentben áll a HTTP
Basic Auth blokk — ha a teszt-aldomain nyilvános URL-en érhető el, érdemes bekapcsolni.

**Ellenőrzés élesítés után:**

```bash
curl -I https://okoth.hu/ | grep -i x-robots-tag   # semmit nem adhat vissza
curl -s https://okoth.hu/robots.txt                 # Allow: / kell benne legyen
```

> A `canonical` és az Open Graph URL-ek **már az éles domainre** (`okoth.hu`) mutatnak,
> így élesítéskor azokhoz nem kell hozzányúlni. A kapcsolati e-mail cím maradt
> `kapcsolat@okotechhome.hu` — ha az is változik, azt külön kell átvezetni.

## Backend — levélküldés

Három végpont a `_web/api/` alatt, PHP-ben (a tárhely Apache + PHP):

| Végpont | Mit szolgál ki |
|---|---|
| `api/kapcsolat` | a Kapcsolat oldal űrlapja |
| `api/dontestamogato` | a 8. szekció összefoglalója (JSON) |
| `api/ajanlat-atnezes` | a 11. szekció szakértői átnézése, csatolmánnyal |
| `api/ajanlat-elemzes` | a feltöltött ajánlatok gépi kiolvasása (AI-proxy) |
| `api/ajanlat-jelentes` | az összehasonlítási jelentés elküldése e-mailben |

**A jelszó nincs a repóban.** A valódi értékek az `api/config.php`-ban élnek,
ami a `.gitignore`-ban van; a repóban csak az `api/config.example.php` minta.
Új szerverre telepítéskor:

```bash
cd api && cp config.example.php config.php && chmod 600 config.php
# majd beírni az SMTP-adatokat (vagy környezeti változóban megadni — az erősebb)
```

Az `api/.htaccess` letiltja a `config.php`, a `lib/`, a naplók és a `.txt` fájlok
kiszolgálását, blokkolja a rejtett fájlokat, és kikapcsolja a könyvtárlistázást.
Ez akkor is véd, ha a PHP kiesne és a szerver nyers szövegként adná ki a fájlt.

> ⚠️ **Ez a védelem Apache-specifikus.** Ha a tárhely nginx-et használ, a `.htaccess`
> nem érvényesül — ilyenkor a titkokat a webgyökér **fölé** kell tenni (lásd lent).

### Titkok fájlból — az API-kulcs cseréje szerkesztés nélkül

A `config.php` minden környezetben ugyanaz, egyetlen dolog kivételével: a titkok.
Ha a kulcs a fájlban áll, akkor a config nem másolható környezetek között, és minden
kulcscsere fájlszerkesztés — ami épp azért kockázatos, mert a titkot kézzel kell egy
kódfájlba illeszteni.

Ezért az `oth_titok()` **sorrendben** keresi az értéket, és az első találat nyer:

| Sorrend | Hely | Mikor használd |
|---|---|---|
| 1. | `../oth-titkok/ai-kulcs.txt` — a **webgyökér fölött** | ez az ajánlott: amit a szerver nem lát, azt nem is tudja kiszolgálni |
| 2. | `api/ai-kulcs.txt` | kényelmesebb, de **csak Apache alatt** biztonságos (az `api/.htaccess` védi) |
| 3. | `OTH_AI_KULCS` környezeti változó | ha a tárhely enged `SetEnv`-et vagy panelből állítható |
| 4. | a `config.php`-ba írt érték | végső tartalék |

A beolvasott érték **trimelve** kerül felhasználásra: a szerkesztő által odabiggyesztett
sorvég nem rontja el a kulcsot — ez a leggyakoribb „miért nem működik" ok.

```bash
mkdir -p ../oth-titkok && chmod 700 ../oth-titkok
printf '%s' 'sk-ant-…' > ../oth-titkok/ai-kulcs.txt
chmod 600 ../oth-titkok/ai-kulcs.txt
```

Az SMTP-jelszó ugyanezt a segédfüggvényt használhatja; egyelőre csak az AI-kulcs van
rákötve, mert azt kell rendszeresen cserélni.

### A logó a levélben — miért beágyazva

A levélsablon fejléce **nem hivatkozik távoli képre**. Két okból nem működne:

1. a levelezőkliensek többsége alapból **nem tölt le távoli képet**;
2. ha a webhely még nem él azon a néven, ami a configban áll, akkor **nincs is mit**
   letölteni — és a fejléc helyén törött kép marad.

A logó ezért a levél **részeként** utazik, `Content-ID`-vel; a sablon `cid:oth-logo`-ra
hivatkozik. Ehhez valódi `multipart/related` szint kell, mert a beágyazott kép a HTML
*belsejébe* tartozik, a melléklet pedig *mellé* — e nélkül a logó külön csatolmányként
jelenne meg a levél alján, a fejléc meg maradna törött. A szerkezet a levélhez igazodik:

```text
csak szöveg        multipart/alternative [ text/plain , text/html ]
+ beágyazott kép   multipart/related     [ alternative , kép(ek) ]
+ melléklet        multipart/mixed       [ related|alternative , fájlok ]
```

A csatolást az `oth_kuld()` végzi, **nem az egyes végpontok**: a fejléc a márkasablon
része, nem az üzeneteké, így egyetlen végpontról sem maradhat le. Ha a képfájl hiányzik,
a sablon visszaesik a configban álló URL-re.

A `<img>` magassága **rögzített** (69 px), nem `auto`: kép nélkül az `auto` az alt-szöveg
dobozát a 220 px-es szélességhez nyújtaná, és a fejléc helyén egy óriási üres négyzet
maradna. Rögzített magassággal a helyettesítő szöveg egy logónyi sávban ül.

**Négy védelmi réteg** minden végponton: origin-ellenőrzés (CSRF), mézesbödön
mező, kitöltési idő, és IP-alapú sebességkorlát. A fejléc-injekció ellen minden
felhasználói érték CR/LF-szűrésen megy át — enélkül az űrlap spamtovábbítóvá
válna.

**Az űrlapok JS nélkül is működnek:** sima POST megy a végpontra. Az
`assets/js/urlap.js` csak annyit tesz, hogy a választ helyben jeleníti meg.

## Ajánlat-összehasonlítási jelentés

A 11. szekció összehasonlítása korábban **csak a képernyőn létezett**: a lap bezárásával
elveszett. A jelentés ezt viszi el — három kimenetben, de **egyetlen adatból**, amit a
modul az élő táblából olvas ki. Ez a lényeg: a jelentés nem mondhat mást, mint amit a
látogató lát.

| Kimenet | Hogyan | Hol él |
|---|---|---|
| **HTML letöltése** | önhordó fájl, beépített stíluslappal és logóval | `assets/js/jelentes.js` |
| **PDF / nyomtatás** | valódi oldal (`/jelentes`), onnan `print()` | `jelentes.html` + `jelentes-oldal.js` |
| **Küldés e-mailben** | márkás levéltörzs + a teljes jelentés mellékletként | `api/ajanlat-jelentes` |

### Miért nem `blob:` URL a nyomtatás

Kézenfekvő volna a kész HTML-t `blob:` URL-en megnyitni és kinyomtatni. **Nem működik:**
a `blob:` dokumentum a létrehozó lap tartalombiztonsági szabályát (CSP) örökli, a
webhelyé pedig `style-src 'self'` — a beágyazott `<style>` blokkot a böngésző kiszűrné, és
a jelentés formázás nélkül, csupasz szövegként nyomtatódna ki.

Ezért a nyomtatás **azonos eredetű, valódi oldalon** fut, külső stíluslappal. A letöltött
fájlra viszont ez nem vonatkozik: azt a látogató `file://` alatt nyitja meg, ahol nincs
CSP — oda tehát beépíthető a stíluslap és a logó.

### Egy stíluslap, két felhasználás

Az `assets/css/jelentes.css` **kétféleképpen él**: a `/jelentes` oldalon `<link>`-kel, a
letöltött fájlba pedig beépítve. Így a kettő nem tud elcsúszni egymástól. A márkaszínek
itt nyers értékkel állnak (a fájl elején, egy helyen deklarálva) — a tokenkészletet nem
lehet „magával vinni" egy különálló dokumentumba.

### A logó harmadik változata

A `logo-jelentes.svg` a teljes logó, de a színek **`fill` attribútumban**, nem `<style>`
blokkban. A jelentés a rajzot a lapba illeszti, a CSP pedig a beágyazott stílusblokkot
kiszűrné — a logó szín nélkül, feketén jelenne meg. (Ugyanez az oka, amiért a hibaoldalak
logója is `fill`-lel dolgozik.)

Így **három logóváltozat** él a repóban, mindegyiknek külön oka van:

| Fájl | Mire |
|---|---|
| `logo-okotechhome.svg` | fejléc, világos téma |
| `logo-okotechhome-sotet.svg` | fejléc, sötét téma — `img`-ként betöltve az SVG nem látja a lap `data-theme`-jét |
| `logo-jelentes.svg` | beágyazásra (jelentés, hibaoldalak) — `<style>` nélkül |
| `logo-email.png` | levélfejléc, `Content-ID`-vel beágyazva |

### Az adat nem kerül a szerverre

A jelentés tartalmát a 11. szekció a böngésző tárolóján keresztül adja át a `/jelentes`
oldalnak. Szándékos: az ajánlatok a látogató dokumentumaiból származnak, tehát a
nyomtatáshoz és a letöltéshez **semmi nem megy a szerverre**. Közvetlenül megnyitva a
`/jelentes` ezért üres — az oldal ezt meg is mondja, és visszairányít, ahelyett hogy
csupa „—" táblát mutatna.

> **Miért `localStorage`, ha egyszer semmit nem akarunk tárolni.** A jelentés ÚJ FÜLÖN
> nyílik meg, a `sessionStorage` viszont fülönként külön él: a `noopener`-rel nyitott lap
> **üres tárolóval indul**, és a jelentés helyén az „ehhez a nézethez még nincs
> összehasonlítás" üzenet jelent meg. A `localStorage` fülök között közös — az adat mégsem
> marad ott, mert a fogadó oldal az **olvasás pillanatában törli**. Így csak a kattintás és
> a lap betöltése közötti másodpercig létezik. (`sessionStorage`-ba is írunk, tartalékként:
> ha a `localStorage` tiltott — privát mód, sütikorlát —, az azonos fülön történő
> megnyitás így is működik.)

E-mailnél az adat természetesen felmegy: ott a szerver **idegen adatként** kezeli —
minden mező hosszra vágva és escape-elve kerül a levéltörzsbe és a mellékletbe is.

### Mi kerül a levéltörzsbe, és mi a mellékletbe

600 képpont szélességben egy négyoszlopos összehasonlítás olvashatatlan, ezért a
levéltörzs **összefoglaló**, a teljes tábla a mellékletben van. Ajánlatonként a fájlnév és
az **első érdemi szempont** (elsősorban az ár) megy ki.

> **Amit ez javít:** korábban a törzsben az oszlopcímke állt. Az viszont gyakran
> „nincs adat", mert az elemzés nem mindig tudja megnevezni a technológiát a
> dokumentumból — így a levélben három ajánlatból kettő mellett „nincs adat" jelent meg,
> holott a mellékelt táblában végig volt adat. A `nincs adat` mostantól **hiánynak
> számít, nem értéknek**: nem kerül összefoglalóba, és a csupa hiányból álló összegzősor
> is kimarad.

### Az összegzősor számított — és miért fontos ez

A „Hiányzó / tisztázandó tétel" sor **nem a szervertől jön**: a kliens számolja a fölötte
lévő sorokból, hány szempontról nincs adat az adott ajánlatban, és ki is írja, **melyekről**.

> **Amit ez javított.** A sor korábban ugyanúgy a szerver szempontjaiból próbált
> feltöltődni, mint a többi — csakhogy hozzá nem tartozik szempont, így mindhárom
> oszlopában „—" állt, miközben fölötte több sorban is „nincs adat" szerepelt. A modul
> legfontosabb állítása maradt üresen.

### A sorok kulcs szerint párosulnak, nem sorrend szerint

Minden táblasor `data-ofc-sor="<kulcs>"` attribútumot visel, és a kliens ez alapján keresi
meg a szerver válaszában a hozzá tartozó szempontot. Korábban a párosítás **sorrend**
alapján ment (`Math.floor(i / 3)`): egyetlen beszúrt sor némán elcsúsztatta az összes
cellát — az ár a technológia oszlopába került volna, hibaüzenet nélkül.

A két lista — a markup `ROWS` és az `api/ajanlat-elemzes.php` `$SZEMPONTOK` — **egymástól
függetlenül szerkeszthető**, ezért a generátor minden futáskor összeveti őket, és eltérés
esetén megáll:

```
! A táblasorok kulcsai nem egyeznek a szerver szempontjaival.
  szerver: [... 'meretezes', 'extra_uj', 'telepites' ...]
  markup:  [... 'meretezes', 'telepites' ...]
```

Ha új szempont kell, **mindkét helyen** fel kell venni — és a generátor ezt kikényszeríti.

### Több címzett

A mező vesszővel (vagy pontosvesszővel) elválasztott listát fogad, **legfeljebb ötöt** —
ez a saját jelentés elküldésére való, nem körlevélre. Minden címet külön ellenőrzünk, és
ha egy nem értelmezhető, **megnevezzük, melyik**: öt cím közül az „érvénytelen e-mail-cím"
használhatatlan visszajelzés.

A levél **kizárólag a megadott címekre** megy — néma másolat nem készül az irodának. A
látogató a saját összehasonlítását kéri el, nem megkeresést küld.

### Visszaigazolás — párbeszédben

A sikeres küldés natív `<dialog>`-ban jelenik meg, elmosott háttérrel: a küldés a modul
**vége**, és ilyenkor kell megmondani, **hova** ment a levél (a címek kiírva — az
„elküldtük" önmagában nem ellenőrizhető állítás), és **mi a következő lépés**. A
fókuszcsapdát, az Esc-kezelést és a háttér inaktiválását a platform adja (0.7. alapszabály).

Ha a böngésző nem ismeri a `dialog`-ot, marad a gomb alatti szöveges visszajelzés.

### Amit tudni kell róla

- A **letöltött fájl** a betűket a Google Fontsról hivatkozza — beágyazva ~270 kB-tal
  hizlalná. Hálózat nélkül a tartalék Georgia / rendszerbetű lép be: a szedés kicsit más,
  a tartalom változatlan.
- A gombok addig **rejtve** vannak, amíg nincs mit jelenteni. Üres tábláról készült
  „jelentés" azt sugallná, hogy az elemzés lefutott és nem talált semmit.
- A `/jelentes` `noindex` — nem tartalomoldal, és üresen semmit nem mond.

## Öko — a kísérő kalauz

Kis figura a jobb alsó sarokban minden lapon. Nem chatbot: a dolga az, hogy a
látogató **megtalálja, amit keres**, és oda is jusson.

### Mit csinál

1. **Válaszol** — legfeljebb három rövid mondatban, magázódva. Ha a kérdés
   általános, **egy** pontosítót tesz fel: azt, amelyik a legtöbbet dönti el
   (hol tart a projekt, hányan használják, milyen a telek). Sosem kettőt.
2. **Megmondja, hol a válasz** — nem csak azt, melyik lapon, hanem melyik
   szakaszban is.
3. **Oda is viszi.** Ha a találat az aktuális lapon van, magától odagörget: a lap
   többi része elhalványul és elmosódik egy fedőréteg alatt, a szakasz élesen
   marad, egy rajzolt kéz pedig rámutat. Hét másodperc után, kattintásra vagy
   `Esc`-re elenged.
4. **Tovább is vezet** — minden válasz alatt két-három kattintható továbbkérdés áll
   a látogató saját hangján. Ezt a séma kötelezővé teszi: az a segéd, amelyik
   válaszol és elhallgat, épp a megoldandó problémát reprodukálja.

### A megrendelésig vezető út

A promptban nem csak a szakma áll, hanem az **út** is — enélkül Öko témákra
válaszolt, de senkit nem vitt előre. A hét lépés:

| # | Lépés | Hol |
|---|---|---|
| 1 | Tájékozódás — mi a helyzet, mi a négy irány | `helyzetem/` |
| 2 | **Telekadatok** — helyszínrajz, mért talajvizsgálat, talajvíz-maximum, szabad terület, kút | `projekt-elokeszites/telekalkalmassag` |
| 3 | **Terhelés** — állandó létszám, csúcs, használat jellege | `projekt-elokeszites/terheles-es-kapacitas` |
| 4 | Megoldástípus — a 2–3. adatai döntik el | `megoldasok/` |
| 5 | **Konzultáció és helyszíni felmérés** | `/konzultacio` |
| 6 | Tervezés és vízjogi engedély | `projekt-elokeszites/engedelyezes-es-dokumentumok` |
| 7 | Kivitelezés, majd üzemeltetés | — |

Minden válasznak **el kell helyeznie a látogatót ezen az úton**, és ki kell
mondania a következő lépést. A **függőségeket** is jeleznie kell: árat felmérés
előtt, engedélyt telekadat nélkül, típusválasztást terhelés nélkül nem lehet
— ilyenkor megmondja, mi kell előbb, és melyik lapon tájékozódhat róla. A séma
kötelezővé teszi, hogy a felkínált továbbkérdések közül **legalább egy a
tölcsérben előre vigyen**.

### Mikor szólal meg

- **Minden hero-s lapon magától kinyílik**, amint a fejléckép fele kigördült — aki
  görget, az olvasni kezdett, tehát keres valamit. Fókuszt ilyenkor nem vesz el.
  Aki nem görget, annál 20 másodperc után csak a figura jelenik meg, panel nélkül.
- **A konzultációkérőn nyitva érkezik** a lépésenkénti kísérővel.
- **A bezárás EGY lapnézetre szól**: Öko a fülre húzódik, és azon a lapon nem nyit
  rá újra — a következő lapon viszont megint alapból aktív. (Volt munkamenet-szintű
  változat is; élesben az egyetlen korai bezárás az egész látogatásra elnémította,
  ezért visszavettük.)
- **Laptémák:** a köszönés, a belépő kérdések és a fül kérdései a webhely
  szakaszához igazodnak (`helyzetem/`, `megoldasok/`, `projekt-elokeszites/`,
  `eredmenyek/`, `tudastar/`) — útvonal szerint, mert 119 lapra kézi lista
  karbantarthatatlan volna.

### Három üzemmód

A `<body data-kalauz-mod>` mondja meg; hiányában `kalauz`.

| mód | hol | mit csinál |
|---|---|---|
| `kalauz` | minden lapon | keresés és útbaigazítás a tartalomban |
| `urlap` | `/konzultacio` | nem terel el; a mezők kitöltésében segít, és lépésenként elmondja, mit várunk |
| `jelentes` | `/jelentes` | a saját eredményét magyarázza, nem a webhely tartalmát keresi |

Minden módnak saját belépői, súgószövege és példakérdései vannak.

### Három réteg a kitalálás ellen — mind kódban

A „ne találj ki semmit" utasítás önmagában egy valószínűségi modellre bízza a
szabályt. Ezért mindhárom védelem a végpontban fut, nem a promptban:

| Réteg | Mit zár ki | Hogyan |
|---|---|---|
| **Navigáció** | nem létező oldal, elcsúszott cím | az URL-t, a címet és a horgonyt a végpont **az indexből olvassa vissza**; ami nincs benne, kiesik |
| **Tartalom** | forrás nélküli állítás a témáról | a kérdéshez legjobban illő **nyolc valódi szövegrész** megy a promptba, azzal, hogy azon túl ne állítson semmit |
| **Számok** | kitalált ár, kapacitás, fogyasztás, garanciaidő | mintaillesztés a kész válaszon: ár, kW, m³/nap, mg/l, m², LE, %, garanciaév |

A számőrnél a **találatok megmaradnak**, csak a mondat cserélődik — a látogató
így nem üres kézzel marad, hanem a helyes forrásnál köt ki. Átmegy viszont a
jogszabály- és szabványszám (147/2010, EN 12566-3), a telefonszám, a lap- és
lépésszám: azok hivatkozások, nem műszaki ígéretek.

**Ami ezek után is megmarad:** a részletekre támaszkodó, de szabadon fogalmazott
mondat. A séma és a szűrők a hivatkozást, a számot és a forrást kötik meg — a
stílust nem.

### Amit soha nem tesz

- **Nem talál ki oldalt.** A találatokat a tartalomindexből választja, a séma csak
  útvonalat fogad el, és a végpont a válasz URL-jét, címét és horgonyát még egyszer
  az indexhez méri. Kitalált hivatkozás rosszabb, mint a „nem tudom".
- **Nem méretez, nem mond árat, kapacitást vagy határidőt.** Ezek helyszíni felmérés
  és konzultáció kérdései — oda irányít.
- **Nem beszél magáról mint gépről**, és nem magyarázza a saját működését.

### Amit a webhely szándékosan nem közöl — és Öko sem adhat ki

A lapokon több adat **azért nincs kiírva, mert még nincs ellenőrzött forrásból
megerősítve** (lásd az `ADATHIÁNY` jegyzeteket a HTML-ben). Ha ezeket a
rendszerprompt nem sorolná fel tételesen, a modell a saját általános tudásából
pótolná őket — és a látogató a cég állításának hinné. A tiltólista ezért a
prompt része:

| Nem adható ki | Amit helyette mond |
|---|---|
| Modellenkénti fogyasztás, kapacitás, méret, befolyási szint | mi dönti el, és hol kapja meg |
| Garanciaidő | az elv: nem az évszám, hanem a terjedelem, a kizárások és az üzembe helyezés feltételei; a konkrét szöveg az ajánlatban |
| Karbantartási és ürítési gyakoriságok, alkatrész-élettartam | hogy ezek dokumentumfüggők |
| Telepítésszám, piacvezetőség | melyik bizonyíték mit igazol |
| Mért kibocsátási értékek (KOI, BOI₅…) | mit *jelentenek* a paraméterek |
| Ár, ársáv, határidő | a felmérés mint előfeltétel |

A szabály nem tiltás-lista, hanem viselkedés: **nem kitérés és nem találgatás**
— Öko megmondja, *mi dönti el* az értéket, és hol jut hozzá a látogató.

Ugyanide tartozik a **jogi kapu**: a 147/2010. Korm. rendelet két feltétele
(műszaki elérhetőség + tisztítótelepi kapacitás) a promptban is szerepel, mert
ez a technológiaválasztás *előtti* kérdés — ha mindkettő teljesül, Ökónak a
rákötést kell mondania, akkor is, ha az nem vezet vásárláshoz.

### A tartalomindex

`scripts/kalauz-index.py` → `api/kalauz-index.json` (118 lap, 717 szakasz).

A **kiadott HTML-ből** épül, nem külön karbantartott listából: ha egy lap
megszűnik, kiesik innen is. Lapon: útvonal, cím, meta-leírás, és a szakaszcímek a
horgonyaikkal. A horgonyok a **címeken** ülnek, mert a lapok ott hordozzák az
`id`-t — a kiemelés ezért a legközelebbi `<section>`-re emelkedik, ahol a válasz
valójában van.

### A szövegindex — amiből Öko válaszol

`kalauz-szoveg.json` (835 szövegrész, 495 ezer karakter, 681 KB). Ugyanaz a
script írja, ugyanabból a HTML-ből, egyetlen olvasással.

Amíg csak a címindex létezett, Öko megmondta, **hol** a válasz, de a témáról a
rendszerpromptba írt tudásból beszélt — így forrás nélküli, mégis hihető mondat
bármikor keletkezhetett. Ez a fájl adja hozzá a **lapok tényleges szövegét**:
kérdésenként a nyolc legjobban illő szakasz teljes szövege bekerül a promptba,
azzal az utasítással, hogy elsősorban abból válaszoljon, és amit a részletek nem
mondanak ki, arról ne állítson semmit.

**A darabolás a `<h2 id>`-k mentén megy** — ugyanaz a határ, amit a felület ki
tud emelni, tehát az idézett részlethez mindig tartozik horgony. Az inline SVG-k
`path` adatai, a képernyőolvasónak szánt rejtett feliratok, a morzsamenü és a
belső HTML-jegyzetek kimaradnak: mind rontanák a keresést, tartalmat pedig nem
hordoznak.

**A keresés súlyozott**, mert a nyers előfordulásszám a hosszú szakaszokat
favorizálta — „mit jelent a csúcsterhelés?" a főoldal *véleményekre* talált rá.
Két javítás kellett: **ritkasági súly** (a minden lapon előforduló „szennyvíz"
keveset ér, a „csúcsterhelés" sokat) és **hossznormalizálás** (a találatszámot a
szöveghossz gyöke osztja). Az aktuális lap részletei 1,35× szorzót kapnak.

| Költség | Mért érték |
|---|---|
| a szövegindex betöltése | 1,8 ms |
| pontozás 835 részleten | 8,0 ms |
| csúcsmemória | 4 MB |
| a promptba kerülő részletek | ~7 400 karakter (~2 450 token) |

A `.json` kiszolgálását az `api/.htaccess` tiltja, tehát a fájl a böngészőből
nem tölthető le — a végpont olvassa, nem a kliens.

### A figura

Az A.B.Clear tartály sziluettje szemekkel: bordázott test, kúpos tető, narancs
csonkok. Inline SVG (nem képfájl), mert a pupillák a kurzort követik és a szemhéj
pislog — szabálytalan ütemben, mert az egyenletes pislogás gépiesnek hat. Minden
példány (sarokgomb, fül, panelfej) a **saját középpontjából** néz.

Csökkentett mozgás mellett minden animáció elmarad: a figura egyszerűen ott van.

### Fül-üzemmód

A panel bezárása nem tünteti el: Öko **láthatóan a fül felé húz össze** — látszik,
hová vonult —, a fül pedig nyugtázza: előrelép, megbillen, pislant. A jobb
képernyőszél közepén ül félig kilógva, a teste kicsúszik, a szemek bent maradnak.
`position:fixed`, tehát görgetésre sem mozdul. Egy koppintás visszahozza.

A fül **nem hallgat el végleg**: ~40 másodpercenként előrelép-billen-pislant, az
első két alkalommal a lap témájában kérdez is egyet a fül melletti buborékban.
Kétszer és nem többször. A buborékra kattintva a panel nyílik; az X a munkamenet
végéig elnémítja a kérdéseket.

A sarokban álló gomb és a fül **két külön elem**, egyszerre csak az egyik látszik.
Egyetlen elem mozgatásával nem volt megoldható: az elem helyzete inline
`!important` beállítással sem változott, és a stíluslapban semmi nem magyarázta.

### Végpont

`api/kalauz.php` — sebességkorlát 30/óra IP-nként, és **webhelyszintű napi keret**
(`ai.napi_keret`, alapból 400 hívás/nap az összes AI-végponttal közösen): az
IP-korlátot proxylistával meg lehet kerülni, ezt nem. A kérés a kérdést, az
üzemmódot, az **aktuális lap útvonalát**, urlap módban a **lépésszámot** és a
párbeszéd utolsó hat fordulóját viszi. A végpont az aktuális lapot betolja a
katalógusba, és kimondja: ha a válasz ezen a lapon van, az legyen az első találat
horgonnyal — a felület helyben emeli ki. A prompt a szakmai alapokat is tartalmazza
(a négy irány, a méretezés alapja, a telek három döntő tényezője, mikor kell
szakértő), urlap módban pedig **mezőről mezőre az űrlapot**. A látogató szövege a
prompt szerint adat, nem utasítás — a szabálymódosító kérés visszaterelést kap.

## Konzultációkérő varázsló — `/konzultacio`

A kapcsolati űrlap név, e-mail és szabad szöveg volt. Projektmegkereséshez ez kevés:
a méretezés a terheléstől, a telektől, a talajvíztől és a projekt szakaszától függ.

### Hat lépés

1. **Ki keres** — magánszemély · vállalkozás (létesítménytípussal) · önkormányzat ·
   tervező/kivitelező
2. **Hol tart** — projektszakasz és a jelenlegi megoldás; működési gondnál tünetlista
3. **Az ingatlan** — használat, állandó létszám, csúcs, telekméret, talajvíz, kút,
   meglévő adatok
4. **Leírás** — szabad szöveg, mellette a kitöltéssegéd
5. **Időpont** — telefonos, online vagy helyszíni; naptárból legfeljebb három sáv
6. **Elérhetőség** — név, e-mail, telefon, település, GDPR és ÁSZF

### Működési jellemzők

- **JS nélkül teljes értékű.** Minden lap egyszerre látszik, a natív `required`
  ellenőrzés működik, és egyetlen POST megy a végpontra. A JS teszi lapozóssá, adja
  a haladásjelzőt, a feltételes blokkokat és az összegzést.
- **A naptár preferenciát gyűjt, nem foglal.** Nincs külső naptárfiók, nincs OAuth,
  nincs tokenkezelés — és nem keletkezhet ütköző foglalás. A kijelölt sávok abba a
  szöveges mezőbe íródnak, amit a JS nélküli út is használ: egyetlen igazság megy a
  szerverre.
- **Vázlat a gépen.** A félbehagyott kitöltés `localStorage`-ban marad, és a
  folytatás ott veszi fel a fonalat. Üres vázlatot nem mentünk, két hétnél régebbit
  nem ajánlunk fel.
- **A rejtett feltételes mezők ki is kapcsolódnak**, hogy ne küldjünk olyan értéket,
  amit a látogató nem is látott.

### Az AI három feladata

| hol | mit csinál | ha nem érhető el |
|---|---|---|
| `api/konzultacio-kitoltes.php` | a szabad szöveges leírásból kiolvassa a mezőket | a látogató kézzel tölti ki |
| `api/konzultacio.php` (brief) | nekünk ír előminősítést, hiánylistát, kockázatokat | a levél nélküle megy ki |
| `api/konzultacio.php` (válasz) | a visszaigazolásba írja, mit érdemes előkészíteni | a levél nélküle megy ki |

**A kitöltéssegéd csak ÜRES mezőbe ír.** A gép javaslata soha nem írja felül azt,
amit a látogató maga adott meg — az ő válasza az erősebb. A modell kimenete
bemenetnek számít: az értékkészletet a szerver újraellenőrzi, és a listán kívüli
érték egyszerűen kimarad.

**Egy megkeresés elvesztése drágább, mint egy hiányzó bekezdés** — ezért mindhárom
AI-hívás elhagyható, és a levelek nélkülük is kimennek.

### Kulcs és korlátok

Az AI-kulcs a fájlból jön (`../oth-titkok/ai-kulcs.txt`, lásd fentebb), és **soha nem
kerül a böngészőbe**: a kliens csak a saját végpontjainkat látja. Sebességkorlát a
kitöltéssegédre 20/óra, a beküldésre a `config.php` általános korlátja.

Az IP-nkénti korlátok fölött **webhelyszintű napi keret** is él (`ai.napi_keret`,
alapból 400 AI-hívás/nap; az ajánlat-elemzésnek külön `napi_keret_elemzes`, 60/nap):
elosztott, IP-váltogató próbálkozás ellen a napi plafon véd, nem az IP-korlát.
Betelte után a kitöltéssegéd kézi kitöltést ajánl, a beküldés viszont **AI-brief
nélkül is kimegy** — megkeresést keret miatt nem veszítünk.

## Jelenlegi állapot

| | |
|---|---|
| **Designrendszer** | `OTH-design-system-Teszt.v2` **v0.5** implementálva (`assets/css/app.css`) |
| **Kész szekciók** | fejléc · 1. — *Hero* · 2. — *Bizalmi sáv* · 3. — *Kiinduló helyzet* · 4. — *Technológiák* · 5. — *Megoldásaink* · 8. — *AI-alapú döntéstámogató* |
| **Kész aloldalak** | **Megoldások** (5) · **Helyzetem** (8) · **Kapcsolat** — összesen 14 aloldal |
| **Szövegforrás** | `Okoteh-Home.fooldal.szoveg-vagleges.docx` (főoldal) · `Site map.docx` + `okotechhome-oldalgyartas` skill (aloldalak) |
| **Hiányzik** | lábléc, a sitemap 5 további főkategóriája, `sitemap.xml`, főoldali 6–7. és 9–15. szekció |
| **URL-séma** | kiterjesztés nélküli (clean URL), `.htaccess` + `serve.py` |
| **JS** | 13 modul, összesen ~3200 sor. A legnagyobbak: `ai-advisor.js` (8. szekció), `ofc.js` (11. szekció), `jelentes.js` (jelentés), `terkep.js` (kapcsolati térkép). Mindegyik `defer`, **egyetlen kivétellel**: a `tema.js` a `<head>`-ben, halasztás nélkül fut, különben minden oldalbetöltéskor felvillanna a világos téma. |
| **Téma** | világos/sötét, csúszkakapcsolóval a fejlécben. Első látogatáskor a rendszerbeállítás, utána a látogató választása (`localStorage`). JS nélkül világos marad, és a kapcsoló meg sem jelenik. |
| **Megamenü** | háromszintű (főmenüpont › hub › aloldal), a szerkezete a `scripts/oldalgyartas/fejlec.py`-ban adatként él |
| **Öko kalauz** | AI-alapú kísérő minden lapon, három üzemmódban, a megrendelésig vezető hét lépés ismeretében. Navigációs index: 118 lap, 717 szakasz. **Szövegindex: 857 részlet** — a válasz a lapok tényleges mondataiból jön. Három kódszintű védelem a kitalálás ellen. Végpont: `api/kalauz.php` |
| **Konzultációkérő** | hatlépéses varázsló `/konzultacio` alatt, három AI-hívással (kitöltéssegéd, belső brief, személyre szabott visszaigazolás) |
| **Fejlécképek** | 63 kép / 116 oldal, témánként; mind a `alapkepek/` referenciáival generálva |

## Szerkezet

```text
_web/
├─ index.html                    # főoldal — fejléc + 1–5., 8. és 11. szekció
├─ kapcsolat.html                # a webhely egyetemes CTA-célpontja
├─ jelentes.html                 # az ajánlat-összehasonlítási jelentés nyomtatható nézete
├─ megoldasok/                   # index + 4 technológia-oldal
├─ helyzetem/                    # index + 7 helyzet-oldal
├─ .htaccess                     # clean URL rewrite, 301-ek, biztonsági fejlécek, cache
├─ robots.txt                    # TESZT ÜZEMMÓD: Disallow: / — élesítéskor cserélni
├─ {401,403,404,500}.html        # egyedi hibaoldalak — külön stíluslappal (lásd lent)
├─ favicon.ico                   # a gyökérben kell: a böngészők kérés nélkül is kérik
├─ site.webmanifest              # PWA-ikonok és téma
├─ serve.py                      # lokális preview szerver (a .htaccess-t emulálja)
├─ api/                          # PHP-végpontok (levélküldés, AI-proxy) + .htaccess
├─ COMPONENTS.md                 # ÚJ komponensek — javaslat a designrendszerhez
└─ assets/
   ├─ css/app.css                # a teljes designrendszer @layer architektúrában
   ├─ css/jelentes.css           # a jelentés stíluslapja — a letöltött fájlba is BEÉPÜL
   ├─ js/site.js                 # menüpanel + hero videó (progressive enhancement)
   ├─ js/tema.js                 # világos/sötét téma — `<head>`-ben, HALASZTÁS NÉLKÜL fut
   ├─ js/ai-advisor.js           # 8. szekció — AI döntéstámogató (Test1-ből, változatlan)
   ├─ js/ofc.js                  # 11. szekció — feltöltés, elemzés, jelentés-kivitel
   ├─ js/jelentes.js             # a jelentés motorja: adatgyűjtés, kirajzolás, önhordó fájl
   ├─ js/jelentes-oldal.js       # a /jelentes oldal vezérlése (nyomtatás, letöltés)
   ├─ icon/                      # ikonok, currentColor-ra állítva (CSS-maszk)
   │  ├─ tech-{zart-tarolo,oldomedence,biologiai}.svg      # technológiák (ügyféleszköz)
   │  ├─ ui-{helyszin,email,telefon}.svg                   # kontaktsáv (ügyféleszköz)
   │  └─ ui-{dokumentum,epitkezes,emeszto,nyaralo,telek}.svg  # saját rajzolat
   ├─ video/                     # hero-felvétel, WebM (VP9) + MP4 (H.264), hang nélkül
   │  └─ hero-rendszer.{webm,mp4}
   └─ img/                       # WebP, alfacsatornás kivágatok
      ├─ logo-okotechhome{,-sotet}.svg             # fejléc — világos és sötét téma
      ├─ logo-jelentes.svg                         # beágyazható (fill-lel, <style> nélkül)
      ├─ logo-email.png                            # levélfejléc, Content-ID-vel beágyazva
      ├─ hero-rendszer-allokep{,-1024}.webp        # 16:9 — asztali
      ├─ hero-rendszer-allokep-szuk{,-800}.webp    # 3:2  — tablet és mobil kivágat
      ├─ helyzet-{uj-epitkezes,emeszto-kivaltasa,nyaralo,telekvasarlas}.webp
      ├─ nagyobb-kapacitas-panzio.webp
      ├─ termek-{epureco-oldomedence,ab-clear}.webp
      └─ megoldas-{ab-clear,telepek,iszapzsak}.webp
```

### Hibaoldalak — miért külön stíluslap

A `401/403/404/500.html` az **egyetlen négy oldal**, ahol a stílus nem az `app.css`-ből
jön. Ennek oka nem esztétikai:

> A böngésző a relatív útvonalakat a **kért URL-hez** oldja fel, nem a hibaoldal
> helyéhez. A `/megoldasok/nincs-ilyen` kérésre kiszolgált `404.html`-ben az
> `assets/css/app.css` hivatkozás `/megoldasok/assets/css/app.css`-re mutatna — ami
> szintén 404. A hibaoldal stílus nélkül jelenne meg.

Ezért a stílus a `/assets/css/hiba.css`-ben van, **gyökér-abszolút** hivatkozással, a
logó pedig beágyazott SVG — egyetlen relatív útvonal sincs az oldalon.

**Beágyazott `<style>` nem jöhet szóba**, mert a CSP `style-src`-je nem tartalmaz
`'unsafe-inline'`-t: a böngésző eldobná, és a hibaoldal formázatlanul jelenne meg.
Ugyanezért kapja a beágyazott logó a színét `fill` prezentációs attribútumból, nem az
SVG saját `<style>` blokkjából.

> A `serve.py` **ugyanazt a CSP-t küldi**, mint a `.htaccess` — enélkül ez a hibaosztály
> csak élesben derülne ki. Ha a `.htaccess` CSP-je változik, a `serve.py`-t is át kell írni.

Ha a designrendszer tokenjei változnak, a `hiba.css`-t kézzel utána kell húzni —
a forrás: `scripts/oldalgyartas/hibaoldalak.py`.

> ⚠️ **Alkönyvtáras telepítésnél** (pl. `pelda.hu/oko22/`) a `.htaccess`
> `ErrorDocument` sorait *és* a hibaoldalak gyökér-abszolút hivatkozásait is át kell
> írni az alkönyvtárra.

### Hero — média-döntési fa

| Feltétel | Mit lát a felhasználó |
|---|---|
| ≥1025px, mozgás engedve, nincs adattakarékos mód | állókép → **videó** a médiasávban (a `load` után, csak ha lejátszható) |
| ≤1024px | **szűk kivágatú állókép** (3:2) a szöveg alatt — videó nem töltődik le |
| `prefers-reduced-motion: reduce` | állókép |
| `navigator.connection.saveData` | állókép |
| JS nélkül | állókép |

Asztali nézetben a hero **borító-elrendezésű**: a felvétel a teljes hero-felületet
kitölti, a szöveg rajta ül. A hero magassága a képernyővel mozog: legalább
`100svh − fejléc`, e fölött a médiablokk 16:9-es aránya vagy a szövegoszlop magassága dönt.
A szöveg mögött **lágy folt** (radiális gradiens) fut, amely minden irányban a nulláig hal
el — nincs éle vagy sávhatára; ≤1024px-en kikapcsolva.

> ⚠️ A mozgókép változó háttere miatt a WCAG 2.2 AA szövegkontraszt nem garantálható
> minden pillanatban. Részletek: [`COMPONENTS.md`](./COMPONENTS.md) 13. pont.

Az állókép **végállapot, nem helyőrző**: minden nem asztali nézetben az marad.
Részletek és indoklás: [`COMPONENTS.md`](./COMPONENTS.md) 13. pont.

## Designrendszer

**Igazságforrás:** `OTH-design-system-Teszt.v2.html` (élő referencia) + `.md` (gépi kivonat), v0.5.
Ha a kettő eltér, **a HTML nyer**.

Az `app.css` `@layer` sorrendje rögzíti a rétegarchitektúrát:

```
reset → tokens → base → typography → components → responsive → motion
```

| Réteg | Test2 |
|---|---|
| **Display betű** | Zilla Slab (`--font-heading`) — kizárólag `type-display-*` |
| **Törzs betű** | IBM Plex Sans (`--font-body`) — kizárólag `type-ui-*` |
| **Adat betű** | IBM Plex Mono (`--font-mono`) — kizárólag `type-data-*` |
| **Paletta** | Stardust · Drizzle · Lime · Fern · Sea Mist · Sky Blue · Olive Leaf · Forest |
| **Elsődleges** | Fern `#80A640`, rajta **mindig Forest (sötét) szöveg** |
| **Térköz** | fix skála 4–128px, köztes érték nincs; szekcióhatár `--space-section` |
| **Konténer** | max. 1180px, oldalsó margó `--page-gutter` (20 / 32 / 48px) |
| **Töréspontok** | ≤640 mobil · 641–1024 tablet · ≥1025 asztali |

### Kötelező szabályok, amiket a kód betart

- **Egyedi érték nincs.** Nincs saját `font-size`, `padding`, `color`, `radius` — mindig token
  vagy `.type-*` szereposztály.
- **Réteg-sorrend.** Komponens-szabály nem használ primitívet (`--color-*`) vagy nyers hexet.
- **Sötét téma.** Minden témafüggő komponens-token újra van deklarálva a `[data-theme="dark"]`
  blokkban — a `var()` a *deklaráció* helyén oldódik fel, nem a használatén.
- **Állapot natív attribútummal:** `disabled`, `aria-invalid`, `aria-busy` — nem osztállyal.
- **`prefers-reduced-motion`** minden átmenetet lekapcsol.

> ⚠️ **Új komponensek.** A designrendszer 10. fejezete szerint a kártya, szekció-sáv, táblázat,
> médiakeret és ikonrendszer **még nincs definiálva**. Ezeket dokumentált osztályként vezettük be,
> kizárólag meglévő tokenekből — az indoklás és a javasolt szabályzatszöveg:
> [`COMPONENTS.md`](./COMPONENTS.md). Két pont ott **döntésre vár**.

## Motor és technológia

A **márka, a téma és a logó azonos** a Test1-gyel; az eltérés a designrendszerben van.

| Réteg | Megoldás |
|---|---|
| **Markup** | szemantikus HTML5, oldalanként önálló fájl |
| **Stílus** | saját CSS `@layer` + design-tokenek (nincs Tailwind) |
| **Interakció** | vanilla JS, `assets/js/site.js` (defer, ~2 KB) — natív `details` menü, feltételes hero videó |
| **Média** | WebP kivágatok (alfa), videónál WebM (VP9) + MP4 (H.264), hang nélkül |
| **Szerver** | statikus, Apache `.htaccess` |

> **Eltérés a Test1-től, amit tudni kell:** a Test1 GSAP 3.12 + ScrollTrigger + Lenis
> smooth-scroll stacket használ. A Test2 designrendszer **0.7 alapszabálya** viszont kimondja:
> *„Nincs framework. Natív HTML-elem és vanilla JS. A viselkedést nem újraépítjük, hanem a
> platformtól kérjük."* Ezért a GSAP/Lenis réteg **nem emelhető át változtatás nélkül** —
> ha a Test2-ben is kell scroll-animáció, vagy natív CSS scroll-driven animationnel kell
> megoldani, vagy a designrendszernek kell felmentést adnia. Ez nyitott kérdés.

## Helyi kiszolgálás

Az oldal **kiterjesztés nélküli** útvonalakat használ (`/uj-epitkezes`), amit élesben a
`.htaccess` rewrite old meg. A sima `python3 -m http.server` ezekre 404-et adna, ezért:

```bash
cd _web
python3 serve.py            # http://localhost:8849
python3 serve.py 9000       # egyedi port
```

A `serve.py` a `.htaccess` viselkedését emulálja:

| Kérés | Eredmény |
|---|---|
| `/uj-epitkezes` | `uj-epitkezes.html` kiszolgálva |
| `/uj-epitkezes.html` | 301 → `/uj-epitkezes` |
| `/index.html` | 301 → `/` |
| `/uj-epitkezes/` | 301 → `/uj-epitkezes` |
| nem létező útvonal | `404.html`, 404-es státusszal |

> A hivatkozott aloldalak **még nem léteznek**, így helyben 404-et adnak. Ez várt állapot,
> nem hiba. Jelenleg hivatkozott útvonalak:
>
> | Honnan | Útvonal |
> |---|---|
> | fejléc, navigáció | `megoldasok` · `megoldasaink` · `referenciak` · `tudastar` · `kapcsolat` · `gyik` · `karrier` |
> | fejléc CTA | `konzultacio` |
> | hero | `dontesi-utvonal` (döntési útvonal) · `koltsegiranytu` (költségiránytű) · `ajanlat-osszehasonlitas` |
> | 3–5. szekció | `uj-epitkezes` · `emeszto-kivaltasa` · `idoszakos-hasznalat` · `telekvasarlas` · `szervezeti-telepulesi-megoldasok` · `biologiai-szennyviztisztito-1-50` · `telepek` · `oldomedencek` · `iszapzsak` · `tudastar/technologiak-osszehasonlitasa` |
>
> A hero három útvonala a *döntéstámogató modulokhoz* tartozik
> (`_files/okotechhome-dontestamogato-modulok.docx`): a szlugok **javaslatok**, a modulok
> végleges elnevezésével együtt véglegesítendők.

## Deploy (Apache shared hosting)

1. A `_web/` tartalma megy fel — **a `.htaccess`-szel együtt**. Rejtett dotfile, az
   FTP-kliensek és ZIP-csomagolók alapból kihagyják; ha élesben minden link 404-el,
   jellemzően ez maradt le.
2. **Ne kerüljön ki:** `README.md`, `COMPONENTS.md`, `serve.py`.
3. HSTS csak éles, HTTPS-en kiszolgált domainen kapcsolandó be (a `.htaccess`-ben
   kommentben vár).

```bash
git archive v0.02.00 --prefix=okotechhome2/ -o /tmp/okotechhome2.tar.gz _web
```

## Minőségi kapuk (kiadás előtt)

- WCAG 2.2 AA · látható fókusz · `prefers-reduced-motion` · 44×44px érintőcélpont
- Core Web Vitals: LCP < 2,5 s · INP < 200 ms · CLS < 0,1
- CSP, HSTS, `X-Frame-Options: DENY`, `nosniff`, `Referrer-Policy`, `Permissions-Policy`
- JSON-LD (`Organization`, `FAQPage`, `BreadcrumbList`), Open Graph, canonical
- Cache-busting a statikus eszközökön (`app.css?v=NN`)

Teljes ellenőrzőlista: [`../VERSIONING.md`](../VERSIONING.md) → *Kiadási ellenőrzőlista*
