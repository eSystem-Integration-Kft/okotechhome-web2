# Oldaltípusok és sablonok

A sitemap 402 eleme **hat oldaltípusba** sorolható. A típus megmondja, milyen szekciókból
áll az oldal és milyen sorrendben. Az eltérést jelölni kell, nem csendben megtenni.

---

## 1. Belépő / áttekintő oldal

*(pl. „Megoldások áttekintése", „Projekt-előkészítési központ", „Támogatási központ")*

| # | Szekció | Komponens |
|---|---|---|
| 1 | oldalcím + bevezető | `.section-head-start`, `.type-display-page-title` |
| 2 | az alárendelt oldalak rácsa | `.situation-grid` (ikonos) vagy `.card-grid` |
| 3 | „mikor melyik" eligazító | `.compare-table` vagy `.numbered-grid` |
| 4 | továbblépés | `.panel-dark` egy CTA-val |

**Cél:** a látogató 10 másodpercen belül tudja, melyik alárendelt oldal az övé.

---

## 2. Technológia-oldal

*(pl. „Biológiai szennyvíztisztítás", „Oldómedencés rendszer")*

| # | Szekció | Megjegyzés |
|---|---|---|
| 1 | cím + egymondatos meghatározás | mit csinál a technológia |
| 2 | **Hogyan működik** | lépések: `.numbered-grid` |
| 3 | **Kinek megfelelő** / **Mikor nem** | két oszlop `.split`-ben — a „mikor nem" **kötelező** |
| 4 | telek- és terhelési feltételek | `.compare-table` vagy adatpár-lista |
| 5 | üzemeltetés, karbantartás | |
| 6 | költségtényezők | **konkrét szám csak forrásból** |
| 7 | termékcsalád-hivatkozás | `.panel` a saját termékre |
| 8 | kapcsolódó esettanulmányok | `.card-grid` |

> A „Mikor nem megfelelő" szekció a cég ígéretének része („megmondjuk, ha nem a mi
> rendszerünk a megoldás"). Ne hagyd ki, és ne írd körbe.

---

## 3. Termékcsalád-oldal és aloldalai

*(A.B.Clear, EPURECO — a sitemap szerint: áttekintés · modellek és kapacitások · műszaki
adatok · telepítési feltételek · dokumentumok · kapcsolódó referenciák)*

| # | Szekció | Komponens |
|---|---|---|
| 1 | terméknév + pozicionálás | `.type-display-page-title` |
| 2 | termékrender | alfás WebP, `.product-media` |
| 3 | kinek való / mikor | `.split` |
| 4 | **modellek és kapacitások** | `.compare-table` — **típusjel, LE, méret, tömeg** |
| 5 | **műszaki adatok** | adatpár-lista vagy tábla |
| 6 | telepítési feltételek | `.numbered-grid` |
| 7 | tanúsítványok, dokumentumok | letöltéslista |
| 8 | üzemeltetési költség | |
| 9 | CTA | `.panel-dark` |

> ⚠️ **A 4., 5. és 7. szekcióhoz gyártói adat kell.** Ezek a számok jelenleg **nincsenek meg**
> a repóban — lásd `szovegforrasok.md`. Amíg nincsenek, a szekció helyét jelöld, de
> **ne írj bele becsült értéket**.

---

## 4. Helyzet-oldal

*(pl. „Telekvásárlás vagy új építés előtt állok", „Meglévő emésztőt szeretnék kiváltani")*

| # | Szekció |
|---|---|
| 1 | a helyzet felismerése — „ez Ön?" |
| 2 | mit kell tisztázni (kérdéslista) |
| 3 | milyen megoldások jöhetnek szóba / mi esik ki |
| 4 | tipikus buktatók |
| 5 | milyen adatokat érdemes előkészíteni |
| 6 | a hozzá tartozó modul (telek-előszűrő, projektbrief) vagy konzultációs CTA |

---

## 5. Tudástár-cikk

| # | Szekció |
|---|---|
| 1 | cím + a kérdés egy mondatban |
| 2 | rövid válasz (2–3 mondat) — **AIO-idézhető** |
| 3 | részletes kifejtés |
| 4 | mikor kérj szakértőt |
| 5 | kapcsolódó cikkek |

Strukturált adat: `FAQPage` vagy `Article` JSON-LD. A rövid válasz legyen önmagában is
értelmes — az AI-keresők azt idézik.

---

## 6. Modul-oldal (interaktív)

*(telek-előszűrő, költségiránytű, ajánlat-összehasonlító, projektbrief)*

| # | Szekció |
|---|---|
| 1 | mit ad a modul, mit nem |
| 2 | mennyi idő, kell-e adatot megadni, elmenthető-e |
| 3 | a modul felülete (`<div id="…-root">`, JS tölti) |
| 4 | `<noscript>` alternatíva — **kötelező** |
| 5 | jogi kitétel: az eredmény tájékoztató jellegű |

A 8. szekció (`ai-advisor.js` + `assets/data/aidt-konfig.js`) a minta: **számérték soha a
kódban**, hanem szerkeszthető konfigban; küldés csak valódi végponttal, különben őszinte
jelzés.

---

## 7. Jogi / rendszeroldal

Egyszerű, egyoszlopos szövegoldal `.section-inner` + `.type-ui-body`. Kötelező oldalak a
sitemap szerint: adatkezelési tájékoztató, cookie-tájékoztató, jogi nyilatkozat, ÁSZF,
akadálymentességi nyilatkozat, 404.
