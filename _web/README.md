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

**A jelszó nincs a repóban.** A valódi értékek az `api/config.php`-ban élnek,
ami a `.gitignore`-ban van; a repóban csak az `api/config.example.php` minta.
Új szerverre telepítéskor:

```bash
cd api && cp config.example.php config.php && chmod 600 config.php
# majd beírni az SMTP-adatokat (vagy környezeti változóban megadni — az erősebb)
```

Az `api/.htaccess` letiltja a `config.php`, a `lib/` és a naplók kiszolgálását.
Ez akkor is véd, ha a PHP kiesne és a szerver nyers szövegként adná ki a fájlt.

**Négy védelmi réteg** minden végponton: origin-ellenőrzés (CSRF), mézesbödön
mező, kitöltési idő, és IP-alapú sebességkorlát. A fejléc-injekció ellen minden
felhasználói érték CR/LF-szűrésen megy át — enélkül az űrlap spamtovábbítóvá
válna.

**Az űrlapok JS nélkül is működnek:** sima POST megy a végpontra. Az
`assets/js/urlap.js` csak annyit tesz, hogy a választ helyben jeleníti meg.

## Jelenlegi állapot

| | |
|---|---|
| **Designrendszer** | `OTH-design-system-Teszt.v2` **v0.5** implementálva (`assets/css/app.css`) |
| **Kész szekciók** | fejléc · 1. — *Hero* · 2. — *Bizalmi sáv* · 3. — *Kiinduló helyzet* · 4. — *Technológiák* · 5. — *Megoldásaink* · 8. — *AI-alapú döntéstámogató* |
| **Kész aloldalak** | **Megoldások** (5) · **Helyzetem** (8) · **Kapcsolat** — összesen 14 aloldal |
| **Szövegforrás** | `Okoteh-Home.fooldal.szoveg-vagleges.docx` (főoldal) · `Site map.docx` + `okotechhome-oldalgyartas` skill (aloldalak) |
| **Hiányzik** | lábléc, a sitemap 5 további főkategóriája, `sitemap.xml`, főoldali 6–7. és 9–15. szekció |
| **URL-séma** | kiterjesztés nélküli (clean URL), `.htaccess` + `serve.py` |
| **JS** | `assets/js/site.js` (2 KB) — menüpanel, hero videó · `assets/js/ai-advisor.js` (566 sor) — a 8. szekció interaktív modulja, a Test1-ből átvéve. Minden más HTML + CSS. |

## Szerkezet

```text
_web/
├─ index.html                    # főoldal — fejléc + 1–5. és 8. szekció
├─ kapcsolat.html                # a webhely egyetemes CTA-célpontja
├─ megoldasok/                   # index + 4 technológia-oldal
├─ helyzetem/                    # index + 7 helyzet-oldal
├─ .htaccess                     # clean URL rewrite, 301-ek, biztonsági fejlécek, cache
├─ robots.txt                    # TESZT ÜZEMMÓD: Disallow: / — élesítéskor cserélni
├─ {401,403,404,500}.html        # egyedi hibaoldalak — külön stíluslappal (lásd lent)
├─ favicon.ico                   # a gyökérben kell: a böngészők kérés nélkül is kérik
├─ site.webmanifest              # PWA-ikonok és téma
├─ serve.py                      # lokális preview szerver (a .htaccess-t emulálja)
├─ COMPONENTS.md                 # ÚJ komponensek — javaslat a designrendszerhez
└─ assets/
   ├─ css/app.css                # a teljes designrendszer @layer architektúrában
   ├─ js/site.js                 # menüpanel + hero videó (progressive enhancement)
   ├─ js/ai-advisor.js           # 8. szekció — AI döntéstámogató (Test1-ből, változatlan)
   ├─ icon/                      # ikonok, currentColor-ra állítva (CSS-maszk)
   │  ├─ tech-{zart-tarolo,oldomedence,biologiai}.svg      # technológiák (ügyféleszköz)
   │  ├─ ui-{helyszin,email,telefon}.svg                   # kontaktsáv (ügyféleszköz)
   │  └─ ui-{dokumentum,epitkezes,emeszto,nyaralo,telek}.svg  # saját rajzolat
   ├─ video/                     # hero-felvétel, WebM (VP9) + MP4 (H.264), hang nélkül
   │  └─ hero-rendszer.{webm,mp4}
   └─ img/                       # WebP, alfacsatornás kivágatok
      ├─ logo-okotechhome.svg
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
