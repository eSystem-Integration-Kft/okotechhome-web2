---
name: okotechhome-oldalgyartas
description: >-
  Oldalgyártás az okotechhome.hu (Test2) statikus site-ra: a sitemap alapján új aloldalt vagy
  szekciót építeni, meglévőt átdolgozni, a Test2 designrendszer komponenskészletével és
  tokenjeivel. Tartalmazza a teljes sitemapot (402 elem), az URL-sémát, az oldaltípus-sablonokat
  (termék, helyzet, tudástár, modul, jogi), a komponenskészletet és a szövegforrásokat.
  HASZNÁLD MINDIG, amikor a `_web/` alatt HTML-t, CSS-t vagy JS-t írsz vagy módosítasz —
  új aloldalt hozol létre, szekciót építesz, komponenst választasz, útvonalat nevezel el,
  vagy a designrendszer betartását kell ellenőrizni. A szakmai (szennyvíztechnikai, jogi,
  szabvány-) tartalomhoz az `otthoni-biologiai-szennyviztisztitas` skillt is olvasd be.
---

# ÖkoTech Home — oldalgyártás (Test2)

Ez a skill azt írja le, **hogyan készül egy oldal ebben a repóban**. A *mit írjunk* kérdésre
a szakmai skill és a szövegforrások válaszolnak; ez a skill a **szerkezetet, a
komponenseket és a szabályokat** adja.

## Mikor használd

- új aloldal létrehozása a sitemap alapján,
- új szekció a főoldalon vagy aloldalon,
- meglévő szekció átdolgozása vizuális terv alapján,
- komponensválasztás („kártya vagy helyzetoszlop?"),
- útvonal (szlug) elnevezése,
- annak ellenőrzése, hogy egy változtatás betartja-e a designrendszert.

## Munkamenet — minden oldalnál ugyanaz

1. **Keresd meg az oldalt a sitemapban** → `references/sitemap.md`. Ha nincs benne, azt
   jelezd, ne találj ki új menüpontot.
2. **Válaszd ki az oldaltípust** → `references/oldaltipusok.md`. A típus megmondja, milyen
   szekciókból áll az oldal, és milyen sorrendben.
3. **Szedd össze a szöveget** → `references/szovegforrasok.md`. **Számot, jogszabályt,
   szabványt, terméktulajdonságot sosem írsz emlékezetből** — vagy forrásból jön, vagy
   jelölöd, hogy hiányzik.
4. **Építsd meg a meglévő komponensekből** → `references/designrendszer.md`. Ha nincs
   megfelelő komponens, **új osztályt hozol létre dokumentálva** (`_web/COMPONENTS.md`),
   nem improvizálsz egyedi értékekkel.
5. **Ellenőrizd** a kiadási kapukat (lentebb), és **frissítsd a dokumentációt**:
   `_web/COMPONENTS.md` (ha új komponens), `CHANGELOG.md`, `_web/README.md`.

## Vasszabályok

| Szabály | Miért |
|---|---|
| **Egyedi érték nincs.** Minden méret, szín, térköz tokenből vagy `.type-*` szereposztályból. | A designrendszer 0.8 / 9. tiltólistája |
| **Réteg-sorrend.** Komponens-szabály nem hivatkozhat primitívre (`--color-*`) vagy nyers hexre. | primitive → semantic → component |
| **Sötét téma.** Minden új témafüggő token újradeklarálva a `[data-theme="dark"]` blokkban. | a `var()` a deklaráció helyén oldódik fel |
| **Nincs framework.** Natív HTML-elem és vanilla JS; a viselkedést a platformtól kérjük. | designrendszer 0.7 |
| **Állapot natív attribútummal** (`disabled`, `aria-invalid`, `aria-busy`), nem osztállyal. | |
| **Kiterjesztés nélküli URL**, `.htaccess` + `serve.py` kezeli. | |
| **Cache-busting:** minden módosított eszközhöz `?v=NN` emelés az `index.html`-ben. | a `.htaccess` egy évet ad a statikus fájloknak |

## Kiadási kapuk (minden oldalnál)

- WCAG 2.2 AA · látható fókusz · `prefers-reduced-motion` · 44×44px érintőcélpont
- LCP < 2,5 s · INP < 200 ms · CLS < 0,1 (kép/videó `width`+`height`, `srcset`, `sizes`)
- egyetlen `<h1>`, hierarchikus címsorok, `aria-labelledby` minden szekción
- minden kép `alt`-ja **leíró** (mit ábrázol), a dekoratív elem `aria-hidden="true"`
- a hivatkozott, még nem létező útvonalak a `_web/README.md`-ben felsorolva

## Referenciák

| Fájl | Mikor olvasd |
|---|---|
| `references/sitemap.md` | mindig, az oldal helyének és szlugjának megállapításához |
| `references/oldaltipusok.md` | a szekciósorrend és a sablon kiválasztásához |
| `references/designrendszer.md` | komponens- és tokenválasztáshoz |
| `references/szovegforrasok.md` | mielőtt bármilyen szöveget vagy számot leírsz |

**Szakmai tartalomhoz** (technológia, jog, szabvány, határérték, terminológia) az
`otthoni-biologiai-szennyviztisztitas` skill referenciáit használd — az a tudásbázis, ez a
gyártási kézikönyv.
