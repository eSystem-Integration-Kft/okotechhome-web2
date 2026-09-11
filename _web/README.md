# `_web/` — webkimenet

Ez a könyvtár a **deployolható statikus site** gyökere, egyben a repó tulajdonképpeni hatóköre.
Kizárólag ennek a tartalma kerül élesre — a repó gyökerében élő `README.md`, `CHANGELOG.md`,
`VERSIONING.md`, `VERSION`, `scripts/` és `.github/` **nem**, és az itteni `README.md`,
`COMPONENTS.md`, `serve.py` sem.

## ⚠️ TESZT ÜZEMMÓD — élesítési ellenőrzőlista

Az oldal jelenleg a **`https://tst.okoth.hu`** aldomainen fut, és **minden keresőmotor
elől el van zárva**. Az éles domain: **`https://okotechhome.hu`** — a webhely a régi
WordPress helyére kerül, **ugyanarra a kiszolgálóra** (`79.172.249.246`), és az
`okoth.hu` DNS-e **nem** fordul át. Az `okoth.hu` marad az, ami: a `tst.` aldomain
gazdája.

A zárás **három rétegben** él. **Ezt a hármat NEM kézzel oldjuk fel**: a
`scripts/prod-epit.sh` teszi meg, az élesbe menő fa építésekor (lásd lentebb,
*Két fa, egy forrás*). A táblázat azért van itt, hogy tudni lehessen, mit csinál:

| # | Hol | Mit kell tenni élesítéskor |
|---|---|---|
| 1 | `.htaccess` → *TESZT ÜZEMMÓD* blokk | az `X-Robots-Tag` sort törölni vagy kikommentezni |
| 2 | `robots.txt` | a `Sitemap:` sor felvétele — **csak ha már van `sitemap.xml`**. (A fájlban NINCS általános `Disallow: /`: a letöltés szándékosan szabad, az indexelést a noindex tiltja. Az AI- és SEO-botok tiltása élesben is marad.) |
| 3 | minden HTML `<head>` | a `<meta name="robots" content="noindex, …">` → `index, follow` |
| 4 | `.htaccess` → *RÉGI WORDPRESS-URL-EK* blokk | **ELINTÉZVE 2026-09-11-én**: az Apache olvassa. Mérve élesben — a kiterjesztés nélküli URL-ek és mind a 301-es átirányítás (Ads + a régi blog 42 bejegyzése) működik |
| 5 | `api/config.php` a szerveren | **ELINTÉZVE**: a fájl már mindkét domainre írva (`origin` tartalmazza mindkettőt, az e-mail `url`/`logo` az élesre mutat), és fent van |
| 6 | **`/oth-titkok/*.txt` a szerveren** | **KÜLÖN LÉPÉS**, lásd lentebb — a `config.php` NEM elég: az AI-kulcs és a CRM-tokenek külön fájlokban élnek, a webgyökér FÖLÖTT |

### A titkok — három hely, egyik sincs a repóban

A webhely három forrásból vesz titkot:

| # | Hol | Mi van benne | Hogyan kerül a szerverre |
|---|---|---|---|
| 1 | `api/config.php` | SMTP-jelszó, címzettek, korlátok | a `feltoltes.sh` **szándékosan kihagyja** — egyszer, kézzel megy fel |
| 2 | **`/oth-titkok/*.txt`** | **AI-kulcs**, CRM-tokenek | `scripts/titkok-atvitel.sh` |
| 3 | környezeti változók | ugyanezek, ha valaki így adja meg | a tárhely beállításai |

**A 2. pont a fiók HOME könyvtárában van, nem a `public_html`-ben.** Szándékosan:
ami a webgyökéren kívül van, azt a kiszolgáló akkor sem tudja kiszolgálni, ha
egyszer elromlik a `.htaccess`.

> ⚠️ **Ez élesítéskor kimaradt, és Öko emiatt nem működött.** A `config.php`
> felkerült, és ebből az a benyomás támadt, hogy a titkok megvannak — pedig az
> **AI-kulcs külön fájl**. A napló egyértelmű volt:
> `OTH AI: nincs beállítva API-kulcs — a hívás kimarad.`

**A `crm-db.txt` nem vihető át.** Az a HELYI MySQL hozzáférése (`127.0.0.1`,
`okoth_web`); az éles kiszolgálón ilyen adatbázis nincs. Ott létre kell hozni
egyet, és a saját hozzáférését beírni. Amíg nincs, a **CRM-napló csendben
kimarad** — a beküldések ettől még kimennek e-mailben.

```bash
scripts/titkok-atvitel.sh          # PRÓBA: megmutatja, mit vinne át
scripts/titkok-atvitel.sh --eles   # tényleges átvitel
```

### Két fa, egy forrás — hogyan megy ki a teszt és az éles

```text
_web/       →  tst.okoth.hu      (itt fejlesztünk, ezt nézzük meg)
_web_prod/  →  okotechhome.hu    (ez megy élesbe — a _web/-ből GENERÁLVA)
```

A `_web_prod/` **nem második forrás, hanem kimenet**. Ha a két fát kézzel
tartanánk karban, néhány héten belül elcsúsznának: minden javítást kétszer
kellene megcsinálni, és a „melyik az igazi?" kérdésre valamelyik mindig rossz
választ adna. Így a `_web/` az egyetlen igazság, a `_web_prod/` pedig bármikor
eldobható és újraépíthető. **Kézzel soha ne írj bele**; a `.gitignore` ezért is
zárja ki a verziókövetésből.

A kettő között **csak a teszt üzemmód három rétege** a különbség — a tartalom,
a stílus, a szkriptek és a képek bájtra azonosak. Mérve: 190 HTML + a
`.htaccess` tér el, más semmi.

**A munkamenet:**

```bash
# 1. fejlesztés után ki a tesztre, és megnézzük a tst.okoth.hu-n
scripts/feltoltes.sh tst --eles

# 2. ha jó, felépítjük az éles fát a _web/-ből
scripts/prod-epit.sh

# 3. próbamenet: mit írna felül? (nem ír semmit)
scripts/feltoltes.sh eles

# 4. és fel az élesre
scripts/feltoltes.sh eles --eles
```

**A 4. lépés előtt három kapu áll**, és egyik sem kerülhető meg véletlenül:

1. **Van-e mit feltölteni, és naprakész-e.** A `prod-epit.sh --ellenoriz` megnézi,
   változott-e a `_web/` az utolsó építés óta; ha igen, megmondja, mi.
2. **Teszt üzemmód nem mehet élesbe.** Egyetlen bennmaradt `noindex` elég ahhoz,
   hogy a Google kiejtse a lapot az indexből — és a visszaállítás után is hetekig
   tart, mire visszamászik.
3. **A megerősítés a domaint kéri**, nem egy „igen"-t. Az „igen" reflexből
   leüthető; a domain nevét kiírni már döntés.

**A két kiszolgáló két külön fiók**, két külön jelszóval a kulcskarikán:

| Környezet | Kapcsolódás | Távoli út | Kulcskarika-bejegyzés |
|---|---|---|---|
| `tst`, `okoth` | `cullinan.versanus.eu` | `/public_html/_tst`, `/public_html` | `okoth.hu` |
| `eles` | `cpanel60.sybell.hu` | `/public_html` | `okotechhome.hu` |

A kapcsolódási név mindkét helyen a **kiszolgálóé**, nem a webhelyé: az
FTPS-tanúsítvány arra szól (`*.sybell.hu`, RapidSSL), és az
`ssl:verify-certificate true` nem alku tárgya. Mérve 2026-09-11-én: az éles
gépen Pure-FTPd fut TLS-sel a 21-es porton, a lánc a rendszer CA-készletéből
hitelesül.

**Külön, a keresőktől független megfelelőségi pont:** a Kapcsolat oldalon a Google
Térkép **alapértelmezésben** töltődik be. A beágyazás sütit tesz le és elküldi a
látogató IP-jét a Google-nek, ezért a **cookie-tájékoztatóban nevesíteni kell**
(harmadik féltől származó süti, cél, adatkezelő), és a cookie-hozzájárulásnak ki kell
terjednie rá. Amíg ezek nem élnek, ez nyitott pont — a beágyazás a
`kapcsolat.html` `.terkep` szekciójában van.

### Google Ads céloldalak — a régi URL-ek átirányítása

A Google Ads hirdetésekbe a **régi webhely** URL-jei vannak beégetve
(`okotechhome.hu`). Élesítés után ezek 404-re futnának, a Google pedig a nem
működő céloldalú hirdetést **„Destination not working"** címen elutasítja — a
kampány leállhat. Ezért a `.htaccess` *RÉGI DOMAIN → ÚJ DOMAIN* blokkjának
**már az átállás pillanatában élnie kell**, nem utólag.

Mivel a webhely **ugyanarra a domainre** kerül, ahol a régi URL-ek éltek, ezek
**azonos domainen belüli útvonal-átirányítások** — nincs bennük domainváltás, és
nincs `HTTP_HOST` feltétel sem. A 13 régi útvonal **egyike sem ütközik** az új
webhely lapjaival; ellenőrizve.

A lekérdezőstringet (`?gclid=…`) az Apache alapból hozzáfűzi, tehát az Ads
kattintáskövetése nem sérül.

**A lista 13 útvonalat fed le** (2026-09-10-i átadás). Ami nincs benne, az két
lépcsőben dől el:

1. **ha ugyanaz az útvonal létezik az új webhelyen**, oda megy (nem a
   főoldalra) — ez akkor számít, amikor a régi domain már ezt a webhelyet
   szolgálja ki, és az `okotechhome.hu/megoldasok/ab-clear` egy **élő lap**
   címe;
2. minden más a **főoldalra** — jobb, mint a 404. A régi sitemap többi URL-jét
   külön fel kell mérni; addig ez a háló.

### A két domain ma két külön kiszolgálón van

Mérés, 2026-09-10:

| Domain | IP | Mi fut rajta |
|---|---|---|
| `okotechhome.hu`, `www.` | `79.172.249.246` | nginx (cPanel-proxy) + **WordPress** — ide kerül a webhely |
| `okoth.hu`, `tst.okoth.hu`, `cullinan.versanus.eu` | `81.0.107.145` | a **teszt** gazdája marad |

**A DNS nem mozdul.** A `tst.okoth.hu` tartalma kerül át a régi kiszolgálóra, a
WordPress helyére — ezért az átirányítások **azonos domainen belüli**
útvonal-átirányítások, nem domainváltás.

**Az `.htaccess` működni fog:** a `/cgi-sys/defaultwebpage.cgi` → `200` és a
`/whm-server-status` → `403` **cPanelt** jelez, ahol az nginx csak proxy az
Apache előtt. Ezt élesítéskor **két percben érdemes ellenőrizni** (tölts fel egy
próbaszabályt, és nézd meg, érvényesül-e), mert ha mégsem Apache szolgálná ki, a
kiterjesztés nélküli URL-ek **mind 404-eznének**.

### PHP-követelmények az új kiszolgálón

A `_web/api/` alatt **17 PHP-fájl** fut élesben (űrlapok, levélküldés, CRM,
Öko kalauz).

| Amit igényel | Miért |
|---|---|
| **PHP 8.0 minimum** | a kód `match()`, `str_contains()` és `str_starts_with()` hívásokat használ — ezek 8.0-tól léteznek |
| `curl` | AI-hívások és a CRM-átadás (4 fájl) |
| `mbstring` | ékezetes szövegkezelés — 16 fájlban |
| `openssl` | az SMTP `stream_socket_enable_crypto`-val TLS-re vált (`api/lib/smtp.php`) — enélkül **nem megy ki levél** |
| `PDO` + `pdo_mysql` | a CRM-napló (`api/lib/crm-mysql.php`) |
| **`fileinfo`** | a feltöltött melléklet valódi típusának ellenőrzése (`api/lib/vedelem.php`) — enélkül a **melléklet-ellenőrzés dől el**, nem a kiterjesztésre hagyatkozunk |
| **`zip`** | `ZipArchive` a dokumentumkezeléshez (`api/lib/office.php`) |
| `json`, `pcre`, `filter`, `hash` | a PHP magjában, külön bekapcsolni nem kell |
| kimenő kapcsolat az SMTP- és a HTTPS-portra | levélküldés és AI-hívás |

> A `fileinfo` és a `zip` **korábban hiányzott ebből a listából**. Nem elméleti
> kockázat: a kód `finfo_open()`-t és `ZipArchive`-ot hív, és mindkettő
> végzetes hiba, ha a bővítmény nincs fent. A lista most a kódból van
> visszafejtve, nem emlékezetből.

**MÉRVE AZ ÉLES KISZOLGÁLÓN (2026-09-11):** mind a hét jelen van, a
`PDO::getAvailableDrivers()` tartalmazza a `mysql`-t, és a kimenő kapcsolat is
nyitva van (`mail.okoth.hu:465` 80 ms, `api.anthropic.com:443` 39 ms).

**MÉRVE AZ ÉLES KISZOLGÁLÓN (2026-09-11): PHP 8.5.9, `cgi-fcgi`** — és mind az
öt igényelt bővítmény (`curl`, `json`, `mbstring`, `pdo_mysql`, `openssl`) jelen
van. A váltással tehát nincs teendő: a `crm-mysql.php` és a `crm.php`
megjegyzései épp 8.5-ös viselkedésre készültek fel.

> A `/public_html/.user.ini` `session.save_path`-ja `alt-php80`-ra mutat — az a
> fájl 2021-ből való, és **félrevezet**: a domain tényleges kezelője 8.5. A
> verziót ne ebből olvasd ki, hanem mérd meg.

### A `php.ini` mért állapota (2026-09-11, éles kiszolgáló)

| Beállítás | Érték | Ítélet |
|---|---|---|
| `display_errors` | Off | ✅ élesben kötelező |
| `log_errors` | On, `error_log` | ✅ |
| `max_execution_time`, `max_input_time` | 600 | ✅ bőven elég |
| `max_input_vars` | 10000 | ✅ |
| `memory_limit` | 1024M | ✅ |
| `zlib.output_compression` | **Off** | ✅ *(korábban On volt, és ütközött a `mod_deflate`-tel — azóta kikapcsolva)* |
| `allow_url_fopen` | Off | ✅ a kód curl-t használ, távoli `fopen`-t sehol |
| `post_max_size` | **800M** | ⚠️ túlméretezett |
| `upload_max_filesize` | **512M** | ⚠️ túlméretezett |
| `session.save_path` | `…/alt-php80` | ⚠️ elavult út (a gép 8.5-öt futtat) |
| `date.timezone` | `UTC` | a kód már nem függ tőle — lásd lentebb |

**A két méretkorlát.** A webhely saját korlátja **10 MB** melléklet
(`api/config.php` → `max_meret`). A jelenlegi beállítással a PHP előbb
*befogad* egy 800 MB-os POST-ot, és csak utána utasítja el az alkalmazás — ez
fölösleges támadási felület és fölösleges lemezforgalom.
**Javaslat: `post_max_size = 32M`, `upload_max_filesize = 16M`.**

**A `session.save_path`** a PHP 8.0 munkakönyvtárára mutat, miközben a gép
8.5-öt futtat. A webhely API-ja **nem használ munkamenetet**, tehát ma nincs
következménye — de ha egyszer lesz, csendben rossz helyre írna. Érdemes
kiüríteni a mezőt, hogy a cPanel a verzióhoz tartozót generálja.

**Az időzóna** `UTC`-n állt, és ez a kiírt időpontokat nyáron két órával
csúsztatta el: az értesítő levelek „Beérkezett" sorát, a jelentés keltezését, a
mentett ügyek fájlnevét és a CRM-naplót. **A kódban javítva** (v0.30.01): az
`api/lib/indit.php` maga állítja be az `Europe/Budapest` zónát, ugyanazzal a
megfontolással, mint fölötte a hibakezelést — ami a működés helyességéhez kell,
azt ne a tárhely beállításaira bízzuk. A kiszolgálón tehát **nincs teendő**;
ha mégis átállítod, az sem árt.

## Backend — levélküldés

Három végpont a `_web/api/` alatt, PHP-ben (a tárhely Apache + PHP):

| Végpont | Mit szolgál ki |
|---|---|
| `api/kapcsolat` | a Kapcsolat oldal űrlapja |
| `api/eredmeny-mentes` | ÜGY mentése: a 6. és a 8. szekció kimenete EGY azonosító alá |
| `api/eredmeny-olvas` | egy mentett ügy visszaolvasása azonosító alapján |
| `api/dontestamogato` | a 8. szekció összefoglalója (JSON) |
| `api/ajanlat-atnezes` | a 11. szekció szakértői átnézése, csatolmánnyal |
| `api/ajanlat-elemzes` | a feltöltött ajánlatok gépi kiolvasása (AI-proxy) |
| `api/ajanlat-jelentes` | az összehasonlítási jelentés elküldése e-mailben |
| `api/szippantasi-dij` | a szippantási díjkalkulátor adatbeküldései |

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

## Szippantási díj kalkulátor — `/szippantasi-dij-kalkulator`

Modul-oldal: a látogató a **saját** díjszabásából számol éves szippantási költséget, és
közben épül a **települési díjadatbázis**. A szippantás nem a cég szolgáltatása — a lap ezt
ki is mondja —, a kalkulátor mégis a cég kérdése: a szippantási igény technológiafüggő, és
a látogató itt látja meg, mekkora visszatérő tétel ez.

### Amit a modul megold

A megrendelői brief három díjszabás-szerkezetet ír le. A modul **egyetlen képlettel** kezeli
mindhármat, tehát a látogatónak nem kell besorolnia a számláját egy kategóriába:

```
elszámolt m³ = max(elszállított m³, a minimumdíjban foglalt m³)
alapdíj      = max(minimumdíj, ürítési díj × elszámolt m³)
alkalmi díj  = kiszállási díj + alapdíj + távolsági díj + egyéb
```

A modul legfontosabb kimenete a **minimum-felár**: az az összeg, amit a látogató kifizet, de
nem szállítanak el érte semmit. Ez a szám indokolja a ritkább, teltebb tartállyal végzett
szippantást — és ez az, amit egy sima „mennyibe kerül" kalkulátor elrejt.

### Az adatbázis üres, és ez látszik is

| | |
|---|---|
| **A `dijak` tömb** | `assets/data/szippantas-konfig.js` — induláskor **üres** |
| **Miért** | egyetlen település díjszabását sem ismerjük ellenőrzött forrásból, becsültet pedig nem írunk ki |
| **Mi kell egy sorhoz** | `megye`, `telepules`, `ervenyes`, `forras` — mind kötelező |
| **`null` vs `0`** | a `0` valódi érték (nincs kiszállási díj), a `null` azt jelenti, hogy nem tudjuk. A kettő nem cserélhető fel |
| **Hogyan töltődik** | a lap űrlapjáról → `api/szippantasi-dij` → e-mail → **emberi ellenőrzés** → a konfigba |

Az automatikus felvétel szándékosan nincs: egy elgépelt nulla azonnal minden látogatónak
kiszolgálódna. A felület ezt meg is mondja — a beküldés után kiírja, hogy az adat nem
jelenik meg azonnal a térképen.

### Ami HIÁNYZIK — kérni kell

| Hiányzó adat | Mire kell | Honnan jöhet |
|---|---|---|
| **Települési díjszabások** (kiszállási, ürítési, minimumdíj, foglalt m³, kocsi űrtartalom, érvényesség, forrás) | a `dijak` tömb — a térkép és az előtöltés enélkül üres | ügyfélszámlák, közszolgáltatói ártáblázatok, önkormányzati rendeletek |
| **A példaértékek jóváhagyása** | a kalkulátor kiinduló értékei (`peldaDijak`) | jelenleg a megrendelői brief „Példa" oszlopa — a cégnek meg kell erősítenie, hogy nagyságrendileg vállalható |

### Navigáció — nyitott pont

A lap **nincs benne a sitemapban** ezen a szlugon. A sitemap a *Költségek és ajánlatok*
kategória alatt „Szippantási költség" tételt ismer; ez a lap ennél több (interaktív modul +
adatbázis), és a megrendelő a gyökérbeli `/szippantasi-dij-kalkulator` útvonalat kérte.
Ezért a lap **nem kapott megamenü-pontot** (a menü szerkezete a `fejlec.py`-ban adatként él,
és onnan kerül mind a 147 lapra). Egyetlen bejövő hivatkozása van:
`megoldasok/oldomedence-szippantas-es-karbantartas` → „Következő lépés" panel.

Ha a lap a menübe kerül, a `fejlec.py` *Előkészítés › Költségek és ajánlatok* hasábja a
helye — de azt a kategóriát előbb létre kell hozni.

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
  `eredmenyek/`, `tudastar/`) — útvonal szerint, mert 147 lapra kézi lista
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

`scripts/kalauz-index.py` → `api/kalauz-index.json` (142 lap, 931 szakasz).

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

## Hírek — a régi WordPress-blog átemelése

A régi webhely blogja **42 bejegyzést** tartott 2014 és 2026 között, és az
élesítéskor a WordPress helyére ez a webhely kerül — a tartalom tehát elveszne.
Az anyag ezért átkerült a **`/okotech-home/hirek/`** szakaszba: gyűjtőlap +
42 hírrészlet, képekkel, dokumentumokkal és a beágyazott videókkal együtt.

### Mi került át és hogyan

| | |
|---|---|
| **Hírek** | 42 — a blog teljes anyaga, egy bejegyzés sem veszett el |
| **Képek** | 127 WebP az `assets/img/hirek/` alatt. Borítóból **három** méret: `-borito` 1200×800 és `-borito-600` 600×400 a kártyarácsnak (egységes 3:2), `-borito-teljes` pedig a hírrészletnek — ott a kép a tartalom, nem vághatjuk meg. A cikkbeli képek az eredeti arányukban, max. 1100px szélesen |
| **Dokumentumok** | 5 PDF `assets/dok/` alatt (D&B- és ISO-tanúsítványok, IPARJOG-sajtóközlemények) — a régi oldalon `wp-content/uploads/` alatt éltek |
| **Videó** | 2 YouTube-beágyazás, `youtube-nocookie.com`-ra irányítva |
| **Rovatok** | 3, a sitemap szerint: Vállalati hírek (28) · Pályázatok és fejlesztések (8) · Kiállítások és események (6) |
| **Forrás** | `scripts/oldalgyartas/hirek-forras.json` — ez a hírek EGYETLEN forrása |
| **Generátor** | `scripts/oldalgyartas/hirek.py` |

### Egy hír törlése

A blog anyaga **változtatás nélkül** került át; a rostálás külön menet. Egy hír
eltávolítása három lépés:

1. vedd ki a bejegyzését a `hirek-forras.json` `hirek` tömbjéből,
2. futtasd újra: `python3 scripts/oldalgyartas/hirek.py`,
3. töröld a hozzá tartozó `_web/okotech-home/hirek/<szlug>.html`-t, a képeit
   (`assets/img/hirek/<szlug>-*.webp`) és a `.htaccess` átirányító sorát.

A generátor **nem takarít maga után** — ez szándékos: egy elgépelt szlug így
nem törölne le fájlokat.

### Amit a régi URL-ekkel tettünk

A WordPress a bejegyzéseket a **gyökérben** szolgálta ki (`/elkeszult-sajat-csarnokunk/`),
nem `/blog/` alatt, és ezek az URL-ek élnek a Google találati listájában meg a
megosztásokban. Mind a 42 régi útvonalhoz **301-es átirányítás** került a
`.htaccess`-be az új helyére, a `/blog/` gyűjtőlap és a lapozója pedig a Hírek
lapra megy. A régi szlugok egyike sem ütközik az új webhely lapjaival —
ellenőrizve.

Az `oldomedence-kontra-biologiai-szennyviztisztito` **kivétel**: arra már volt
szabály, a `tudastar/oldomedence-vagy-biologiai-szennyviztisztito` cikkre. Az
maradt; a hír a Hírek szakaszban is ott van, de a régi URL továbbra is a
tudástári cikkre visz.

### Eldöntendő élesítés előtt

- **Tartalmi átfedés.** Három blogbejegyzés ugyanazt mondja el, mint egy-egy
  tudástári cikk (oldómedence kontra biológiai; a szennyvíztisztító
  kiválasztásának szempontjai; kezelés koronavírus idején). Most mindkét helyen
  megvan. Élesítés előtt el kell dönteni, melyik marad — két közel azonos lap
  egymás ellen dolgozik a keresőben.
- **Hosszú címek.** Négy hír címe 110 karakternél hosszabb (a leghosszabb 145),
  mert a WordPressben bekezdésnyi cím volt. A szövegük **nem** lett
  megváltoztatva, csak a három csupa nagybetűs cím került mondatkezdő
  írásmódra. A rövidítés tartalmi döntés — az ügyfélé.
- **Régi ajánlatok.** Néhány hír lejárt akciót hirdet (karácsonyi kedvezmény
  2022, Otthonfelújítási program). Archívumban ez rendben van, de érdemes
  átgondolni, kell-e melléjük jelölés.

## Jelenlegi állapot

| | |
|---|---|
| **Designrendszer** | `OTH-design-system-Teszt.v2` **v0.5** implementálva (`assets/css/app.css`) |
| **Kész szekciók** | fejléc · 1. — *Hero* · 2. — *Bizalmi sáv* · 3. — *Kiinduló helyzet* · 4. — *Technológiák* · 5. — *Megoldásaink* · **6. — *AI megoldás-ajánló*** · **7. — *Az A.B. Clear működése*** · 8. — *AI-alapú döntéstámogató* · 9. — *Üzemeltetés* · 10. — *Tudástár* · 11. — *AI ajánlat-összehasonlító* · 12. — *Dokumentált projektek* · 13. — *Egy kézben* · 14. — *Szakértői továbblépés* · 15. — *GYIK* |
| **Kész aloldalak** | **Megoldások** (41) · **Kiindulópont** (38) · **Projekt-előkészítés** (27) · **Eredmények** (8) · **Tudástár** (12) · **Rólunk** (4) · megkeresés és jogi lapok — a főoldallal együtt **147 lap**. Minden szekció saját hub-lappal |
| **Szippantási kalkulátor** | `/szippantasi-dij-kalkulator` — egy képlet mind a három díjszabás-szerkezetre, csempetérkép a díjadatbázis állásáról, díjbeküldő űrlap. A díjadatbázis **üres**, a beküldés emberi ellenőrzés után kerül be |
| **Szövegforrás** | `Okoteh-Home.fooldal.szoveg-vagleges.docx` (főoldal) · `Site map.docx` + `okotechhome-oldalgyartas` skill (aloldalak) |
| **Hiányzik** | `sitemap.xml`; a szippantási díjadatbázis tartalma; a termékoldalak gyártói adatai |
| **Eldöntendő** | **Két különböző éves üzemeltetési költség él a webhelyen** ugyanarra a berendezésre: a főoldal 9. szekciója és a `tudastar/uzemeltetes-teendok-es-koltsegek` **35 700 Ft/év**-et közöl (áram 24 000 Ft), a `tudastar/oldomedence-vagy-biologiai-szennyviztisztito` tízéves táblája **22 700–27 500 Ft/év**-et (áram 11 000–15 800 Ft). Az iszapzsák és a membrán a két helyen azonos — **kizárólag az áramfeltételezés tér el**. Mindkét lapon HTML-megjegyzés jelöli |
| **URL-séma** | kiterjesztés nélküli (clean URL), `.htaccess` + `serve.py` |
| **JS** | 19 modul, összesen ~7770 sor. A legnagyobbak: `ai-advisor.js` (8. szekció), `ofc.js` (11. szekció), `jelentes.js` (jelentés), `terkep.js` (kapcsolati térkép). Mindegyik `defer`, **egyetlen kivétellel**: a `tema.js` a `<head>`-ben, halasztás nélkül fut, különben minden oldalbetöltéskor felvillanna a világos téma. |
| **Téma** | világos/sötét, csúszkakapcsolóval a fejlécben. Első látogatáskor a rendszerbeállítás, utána a látogató választása (`localStorage`). JS nélkül világos marad, és a kapcsoló meg sem jelenik. |
| **Megamenü** | háromszintű (főmenüpont › hub › aloldal), a szerkezete a `scripts/oldalgyartas/fejlec.py`-ban adatként él |
| **Öko kalauz** | AI-alapú kísérő minden lapon, három üzemmódban, a megrendelésig vezető hét lépés ismeretében. Navigációs index: **142 lap, 931 szakasz**. **Szövegindex: 1123 részlet** — a válasz a lapok tényleges mondataiból jön. Három kódszintű védelem a kitalálás ellen. Végpont: `api/kalauz.php` **Helyszíni segítség:** a `data-oko-pont` attribútummal jelölt felületeknél (ügyazonosító, mentés) magától megszólal, amikor a látogató odagörget. |
| **Konzultációkérő** | hatlépéses varázsló `/konzultacio` alatt, három AI-hívással (kitöltéssegéd, belső brief, személyre szabott visszaigazolás) |
| **Fejlécképek** | 63 kép / 139 oldal, témánként; mind a `alapkepek/` referenciáival generálva. **Egy kivétel:** a szippantási kalkulátor rajzolt fejlécet kap (COMPONENTS.md 21.) |

### Hivatkozott, de még meg nem épített útvonalak

A lábléc a **sitemap szerkezetét** viszi, nem a kész lapok listáját — a sitemap
pedig több lapot ismer, mint amennyi elkészült. Ezért a lábléc tizenegy olyan
útvonalra mutat, ami ma **404**. Ez tudatos állapot, de nyilván kell tartani:
egy *elgépelt* szlug pontosan úgy néz ki, mint egy még meg nem épített lap.

A `scripts/ellenorzes.sh` **7. kapuja** minden futáskor felsorolja őket. Ha a
lista ennél a tizenegynél hosszabb, az **hiba**: vagy elgépelés került be, vagy
a listát kell itt frissíteni.

| Útvonal | Mi lenne | Honnan hivatkozzuk |
|---|---|---|
| `tudastar/telek-talaj-es-viz` | Tudástár-hub: talajtípusok, talajvíz, szikkasztás, vízbefogadó, kút és védőtávolság | lábléc |
| `tudastar/terheles-es-meretezes` | Tudástár-hub: lakosegyenérték, vízfogyasztás, hidraulikai és szervesanyag-terhelés, csúcs- és alulterhelés | lábléc |
| `tudastar/engedelyezes-es-megfeleloseg` | Tudástár-hub: jogi fogalmak, engedélyezési folyamat, CE és szabványok, mintavétel | lábléc |
| `tudastar/uzemeltetes-es-hibamegelozes` | Tudástár-hub: üzemeltetés, hibamegelőzés | lábléc |
| `tudastar/koltseg-es-megvalositas` | Tudástár-hub: teljes projektköltség, megvalósítás | lábléc |
| `tudastar/fogalomtar` | Fogalomtár | lábléc |
| `projekt-elokeszites/engedelyezes-es-dokumentumok` | Előkészítés-hub — a szekció másik három hubja (`telekalkalmassag`, `terheles-es-kapacitas`, `tisztitott-viz-elhelyezese`) már megvan | lábléc |
| `projekt-elokeszites/helyszini-felmeres` | Előkészítés-hub. **Vigyázat:** a `helyzetem/helyszini-felmeres` létezik, de az más lap — nem átirányítási cél | lábléc |
| `projekt-elokeszites/koltsegek-es-ajanlatok` | Előkészítés-hub | lábléc · a szippantási kalkulátor ide kerülne be a menübe (lásd fentebb) |
| `ugyfeltamogatas/` | Ügyféltámogatás szekció (hibajelenségek, karbantartás, alkatrészek) — a `helyzetem.py` is hivatkozza | lábléc · Kiindulópont-lapok |
| `partnereknek/` | Partneri szekció | lábléc |

Az `ugyfeltamogatas/` a sitemap **ÜGYFÉLSZOLGÁLAT** ágának nyilvános fele; a
belépés mögötti ügyfélzóna külön, megtervezett, de el nem indított projekt.

### Miért kell minden szekciómappába `index.html`

Amíg a `tudastar/`, `eredmenyek/` és `okotech-home/` mappában nem volt
`index.html`, mind a három **403-at adott** — miközben a megamenü és a lábléc
hasábcíme minden lapon odamutatott. 2026-09-10-én megépült mindhárom hub-lap,
így ma mind `200`.

Miért 403 volt, és miért nem 404: a `.htaccess` `Options -Indexes`-t állít és
`DirectoryIndex index.html`-t vár, a kiterjesztés nélküli URL-t `.html`-re
átíró szabály pedig **csak nem-könyvtárra** fut le. A kérés így eljutott a
könyvtárig, ott nem volt index, a listázás tiltott → `ErrorDocument 403`.

**Ezért: új szekciómappa nyitásakor az `index.html` nem opcionális.** A
`scripts/ellenorzes.sh` 7. kapuja a mappahivatkozáshoz megköveteli — a puszta
„létezik a mappa" vizsgálat ezt elengedte, és pont ezért maradt sokáig észre
nem véve.

## Szerkezet

```text
_web/
├─ index.html                    # főoldal — fejléc + mind a 15 szekció
├─ kapcsolat.html                # a webhely egyetemes CTA-célpontja
├─ jelentes.html                 # az ajánlat-összehasonlítási jelentés nyomtatható nézete
├─ eredmeny.html                 # a MENTETT ÜGY lapja — a 6. és a 8. szekció kimenete együtt
├─ szippantasi-dij-kalkulator.html  # díjkalkulátor + települési díjadatbázis (modul-oldal)
├─ megoldasok/                   # index + 40 technológia- és termékoldal
├─ helyzetem/                    # index + 37 helyzet-oldal
├─ projekt-elokeszites/          # index + 26 előkészítés-oldal
├─ eredmenyek/                   # esettanulmányok, tanúsítványok, ügyféltapasztalatok
├─ tudastar/                     # 5 szakmai cikk — EN 12566, telepítés, oldómedence vs. biológiai, szagok, CE-vizsgálat
├─ okotech-home/                 # cégbemutatás: cégünkről, történetünk, pályázatok
│  └─ hirek/                     # HÍREK — gyűjtőlap (index) + 42 hírrészlet, a régi WordPress-blog anyaga
├─ ajanlat.html                  # ajánlatkérő — élő űrlapellenőrzés, melléklet ráhúzással
├─ megrendeles.html              # megrendelőlap — okirat, feltételekkel és aláírással
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
   ├─ js/hirek.js                # HÍREK: rovatszűrő + a vízszintes idővonal lassú sodrása
   ├─ js/tema.js                 # világos/sötét téma — `<head>`-ben, HALASZTÁS NÉLKÜL fut
   ├─ js/urlap.js                # űrlapbeküldés oldalfrissítés nélkül
   ├─ js/urlap-ellenorzes.js     # élő űrlapellenőrzés — piros csillag, buborékos hiba
   ├─ js/urlap-fajl.js           # MELLÉKLET: ledobó felület, fájllista, korlátok
   ├─ js/ajanlo.js               # 6. szekció — AI megoldás-ajánló (motor; a tartalom konfigban)
   ├─ js/ugy.js                  # KÖZÖS: ügyazonosító, mentés, átadás a modulok között
   ├─ js/eredmeny-oldal.js       # a mentett ügy lapja — azonosító alapján olvas
   ├─ js/ai-advisor.js           # 8. szekció — AI döntéstámogató (Test1-ből, változatlan)
   ├─ js/ofc.js                  # 11. szekció — feltöltés, elemzés, jelentés-kivitel
   ├─ js/jelentes.js             # a jelentés motorja: adatgyűjtés, kirajzolás, önhordó fájl
   ├─ js/jelentes-oldal.js       # a /jelentes oldal vezérlése (nyomtatás, letöltés)
   ├─ js/szippantas.js           # szippantási díjkalkulátor + csempetérkép
   ├─ data/ajanlo-konfig.js      # 6. szekció — kérdések, döntési szabályok, szövegek — a CÉG szerkeszti
   ├─ data/szippantas-konfig.js  # díjak, vármegyék, példaértékek — a CÉG szerkeszti
   ├─ icon/                      # ikonok, currentColor-ra állítva (CSS-maszk)
   │  ├─ tech-{zart-tarolo,oldomedence,biologiai}.svg      # technológiák (ügyféleszköz)
   │  ├─ ui-{helyszin,email,telefon}.svg                   # kontaktsáv (ügyféleszköz)
   │  ├─ ui-{dokumentum,epitkezes,emeszto,nyaralo,telek}.svg  # saját rajzolat
   │  └─ ui-iszap-{kosar,zsak,komposzt}.svg                 # §7 „Kezelés 3 lépésben" (ideiglenes)
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
      ├─ megoldas-{ab-clear,telepek,iszapzsak}.webp
      ├─ mukodes-metszet{,-1100}.webp                # §7 — a föld alatti metszet, teljes szélességű sávhoz
      └─ mukodes-tartaly-{kosar-nelkul,iszapzsakkal}.webp  # §7 — ugyanaz a tartály felülnézetből
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
