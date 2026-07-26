# `_web/` — webkimenet

Ez a könyvtár a **deployolható statikus site** gyökere, egyben a repó tulajdonképpeni hatóköre.
Kizárólag ennek a tartalma kerül élesre — a repó gyökerében élő `README.md`, `CHANGELOG.md`,
`VERSIONING.md`, `VERSION`, `scripts/` és `.github/` **nem**.

## Célszerkezet

```text
_web/
├─ index.html              # főoldal — döntési tölcsér
├─ …                       # döntési aloldalak, termékoldalak, jogi oldalak, 404.html
├─ assets/
│  ├─ css/                 # designrendszer: @layer + design-tokenek (custom properties)
│  ├─ js/                  # vanilla JS modulok
│  └─ img/                 # optimalizált képek (WebP/AVIF)
├─ .htaccess               # clean URL rewrite, 301-ek, biztonsági fejlécek, cache
├─ robots.txt              # hagyományos + AI/GEO crawlerek
└─ sitemap.xml             # oldal-inventár
```

> **Jelenlegi állapot (`v0.01.01`):** üres váz — `assets/{css,js,img}` létrehozva, oldal még nincs.
> A Test2 designrendszer meghatározása a `0.02.00` mérföldkő.

## Motor és technológia — azonos a Test1-gyel

| Réteg | Megoldás |
|---|---|
| **Markup** | szemantikus HTML5, oldalanként önálló fájl |
| **Stílus** | saját CSS `@layer` + custom properties (nincs Tailwind) |
| **Interakció** | vanilla JS modulok |
| **Animáció** | GSAP 3.12 + ScrollTrigger, Lenis smooth-scroll |
| **Média** | WebM (VP9) elsődleges + MP4 (H.264) fallback + JPG poster |
| **Szerver** | statikus, Apache `.htaccess` (clean URL, rewrite, fejlécek) |

Ami **eltér** a Test1-től: a designrendszer — tokenkészlet, tipográfia, motion-nyelv, layout-ritmus.

## Helyi kiszolgálás

```bash
cd _web
python3 -m http.server 8849      # http://localhost:8849
```

> Clean URL-ek bevezetésekor ide kell egy `serve.py` preview-szerver (a Test1 mintájára) —
> a sima `http.server` 404-et ad a kiterjesztés nélküli útvonalakra.

## Minőségi kapuk (kiadás előtt)

- WCAG 2.2 AA · látható fókusz · `prefers-reduced-motion`
- Core Web Vitals: LCP < 2,5 s · INP < 200 ms · CLS < 0,1
- CSP, HSTS, `X-Frame-Options: DENY`, `nosniff`, `Referrer-Policy`
- JSON-LD (`Organization`, `FAQPage`, `BreadcrumbList`), Open Graph, canonical

Teljes ellenőrzőlista: [`../VERSIONING.md`](../VERSIONING.md) → *Kiadási ellenőrzőlista*
