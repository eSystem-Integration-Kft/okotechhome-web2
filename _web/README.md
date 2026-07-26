# `_web/` — webkimenet

Ez a könyvtár a **deployolható statikus site** gyökere, egyben a repó tulajdonképpeni hatóköre.
Kizárólag ennek a tartalma kerül élesre — a repó gyökerében élő `README.md`, `CHANGELOG.md`,
`VERSIONING.md`, `VERSION`, `scripts/` és `.github/` **nem**, és az itteni `README.md`,
`COMPONENTS.md`, `serve.py` sem.

## Jelenlegi állapot

| | |
|---|---|
| **Designrendszer** | `OTH-design-system-Teszt.v2` **v0.5** implementálva (`assets/css/app.css`) |
| **Kész szekciók** | 3. — *Kiinduló helyzet* · 4. — *Technológiák* · 5. — *Megoldásaink* |
| **Hiányzik** | 1–2. szekció (hero, bizalmi sáv), aloldalak, `404.html`, `robots.txt`, `sitemap.xml` |
| **URL-séma** | kiterjesztés nélküli (clean URL), `.htaccess` + `serve.py` |
| **JS** | jelenleg **nincs** — mindhárom szekció teljes egészében HTML + CSS |

## Szerkezet

```text
_web/
├─ index.html                    # főoldal — jelenleg a 3., 4. és 5. szekció
├─ .htaccess                     # clean URL rewrite, 301-ek, biztonsági fejlécek, cache
├─ serve.py                      # lokális preview szerver (a .htaccess-t emulálja)
├─ COMPONENTS.md                 # ÚJ komponensek — javaslat a designrendszerhez
└─ assets/
   ├─ css/app.css                # a teljes designrendszer @layer architektúrában
   ├─ js/                        # (üres — még nincs szükség rá)
   ├─ icon/                      # technológiai ikonok, currentColor-ra állítva
   │  └─ tech-{zart-tarolo,oldomedence,biologiai}.svg
   └─ img/                       # WebP, alfacsatornás kivágatok
      ├─ helyzet-{uj-epitkezes,emeszto-kivaltasa,nyaralo,telekvasarlas}.webp
      ├─ nagyobb-kapacitas-panzio.webp
      ├─ termek-{epureco-oldomedence,ab-clear}.webp
      └─ megoldas-{ab-clear,telepek,iszapzsak}.webp
```

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
| **Interakció** | vanilla JS — jelenleg egyáltalán nincs betöltve |
| **Média** | WebP kivágatok (alfa), videónál WebM (VP9) + MP4 (H.264) + poster |
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

> A hivatkozott aloldalak (`uj-epitkezes`, `emeszto-kivaltasa`, `idoszakos-hasznalat`,
> `telekvasarlas`, `szervezeti-telepulesi-megoldasok`, tudástár) **még nem léteznek**,
> így helyben 404-et adnak. Ez várt állapot, nem hiba.

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
