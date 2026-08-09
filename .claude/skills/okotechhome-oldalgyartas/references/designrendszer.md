# Test2 designrendszer — komponenskészlet és tokenek

**Igazságforrás:** `OTH-design-system-Teszt.v2` v0.5, implementálva: `_web/assets/css/app.css`.
Az új (a rendszerben még nem definiált) komponensek indoklása: `_web/COMPONENTS.md`.

## Rétegek

```
@layer reset, tokens, base, typography, components, responsive, motion;
```

Komponens-szabály **kizárólag szemantikus tokenre** hivatkozhat, primitívre (`--color-*`)
és nyers hexre soha.

## Tipográfiai szerepek

| Osztály | Méret (asztali) | Használat |
|---|---|---|
| `.type-display-hero` | 52px / 600 | csak a hero `h1` |
| `.type-display-page-title` | 38px / 500 | aloldal `h1` |
| `.type-display-section-title` | 28px / 500 | szekció `h2` |
| `.type-display-highlight-title` | 30px / 500 | kiemelt panel címe |
| `.type-ui-card-title` | 16px / 600 | kártya-, oszlopcím |
| `.type-ui-body` | 16px / 400 | törzsszöveg |
| `.type-ui-subtitle` | 14px / 400 | másodlagos szöveg, táblacella |
| `.type-ui-label` | 13px / 500 | címke, kontaktsáv |
| `.type-ui-button` | 15px / 600 | gomb, navigáció |
| `.type-ui-caption` | 12px / 400 | apró megjegyzés |
| `.type-data-eyebrow` | 11px mono, nagybetűs | szekció-eyebrow |
| `.type-data-value` | 12px mono | adat (nem nagybetűs) |

**Betűcsalád szerep szerint:** Zilla Slab = `type-display-*` · IBM Plex Sans = `type-ui-*` ·
IBM Plex Mono = `type-data-*`. Más kombináció nincs.

## Színek (szemantikus)

| Token | Mire |
|---|---|
| `--canvas` / `--surface` / `--surface-muted` / `--surface-inverse` | sáv · kártya · lime kiemelés · Forest |
| `--text-primary` / `--text-secondary` / `--text-tertiary` | cím · törzsszöveg · halványabb szöveg |
| `--text-on-dark` / `--text-on-dark-muted` | sötét felületen cím · törzsszöveg |
| `--primary` (Fern) / `--secondary` (Olive Leaf) | elsődleges · másodlagos akció |
| `--link` / `--link-hover` | hivatkozás világos felületen |
| `--border` / `--border-focus` | vonal · fókuszgyűrű |
| `--warning-*` / `--danger-*` | figyelmeztetés · hiba |

**Fern felületen mindig Forest szöveg.** Fern **szövegszínként** csak nagy méretben (≥28px),
mert világos háttéren épp a 3:1 határon van.

## Térköz és elrendezés

- skála: `--space-4 … --space-128`, **köztes érték nincs**; ami nem esik rá, az két érték
  összege (`calc(var(--space-64) + var(--space-16))`)
- konténer: `--container-max` (1180px) + `--page-gutter` (48 / 32 / 20px)
- szekcióhatár: `--space-section` (128 / 96 / 64px)
- töréspontok: **≤640 mobil · 641–1024 tablet · ≥1025 asztali**

## Komponenskészlet — mikor melyiket

| Igény | Komponens | Megjegyzés |
|---|---|---|
| szekció-sáv | `.section` + `.section-inner` + `.section-head` | `aria-labelledby` kötelező |
| balra zárt szekciófejléc | `.section-head-start` | |
| kártyarács képpel | `.card-grid` + `.card-item` + `.card-media` + `.card` | 4·2·1 oszlop |
| kártya besorolással | `.card` + `.card-tag` | a tag nem interaktív |
| **ikonos oszlop kártya nélkül** | `.situation-grid` + `.situation` + `.icon-badge` | felül vonal, 3. szekció mintája |
| sorszámozott magyarázókártya | `.numbered-grid` + `.card` + `.card-badge` | |
| világos kiemelt panel | `.panel` (+ `.panel-media`) | |
| **sötét kiemelt panel** | `.panel-dark` (+ `-head` / `-body` / `-eyebrow` / `-title` / `-text`) | link a panelen: `--panel-dark-link` |
| összehasonlító táblázat | `.compare-scroll` + `.compare-table` | `role="region"`, `tabindex="0"` |
| termékkártya | `.product-grid` + `.product` + `.product-media` | négyzetes médiakeret |
| kétoszlopos szekcióalj | `.split` + `.split-col` / `.split-panel` / `.split-card` | |
| bizalmi sáv | `.trust-grid` + `.trust-item` (+ `.trust-title-data` mono) | oszlopköz nincs, a vonal a cellahatáron |
| elsődleges gomb | `.btn.btn-primary` | szekciónként **egy** |
| másodlagos gomb | `.btn.btn-secondary` | Olive Leaf |
| sötét (inverz) gomb | `.btn.btn-inverse` | Forest felület |
| szöveges hivatkozás | `.text-link` (+ `.link-label` ha a nyíl hátul áll) | 44px érintőcélpont |
| chip-hivatkozás | `.chip-link` | kiegészítő belépési pont |
| ikon | `.icon` + méretosztály (`.icon-inline`, `.icon-inline-lg`, `.icon-badge-size`) + rajzolat-osztály | CSS-maszk, `currentColor` |

## Ikonok

- a rajzolatok `assets/icon/`-ban, `fill:currentColor`-ra állítva
- **blokk-ikon:** magasságra normalizálva, per-ikon `aspect-ratio`
- **soron belüli ikon:** befoglaló négyzet (`.icon-inline` 16px, `-lg` 24px, `.icon-badge-size` 36px)
- ügyféleszköz > saját rajzolat. Saját rajzolatnál a fájl fejlécében jelöld, hogy ideiglenes.

## Média

| Eset | Megoldás |
|---|---|
| illusztráció, alfás kivágat | WebP, `.card-media` / `.product-media` keret, `object-fit: contain` |
| hero-felvétel | `<picture>` art directionnel: 16:9 asztali, 3:2 szűk kivágat |
| videó | WebM (VP9) + MP4 (H.264), **hang nélkül**, JS tölti be feltételesen |
| videó feltételei | ≥1025px **és** `prefers-reduced-motion: no-preference` **és** nincs `saveData` |

Minden `<img>` kap `width`/`height` attribútumot (CLS), `loading="lazy"` a hajtás alattiakra,
`fetchpriority="high"` az LCP-elemre.

### Fejlécképek generálása — a diptichon-csapda

Az aloldali fejlécképeknél a szöveg a kép bal harmadán áll, ezért a bal harmadnak
nyugodtnak kell lennie. **Nem szabad viszont így megfogalmazni a promptot:**

> ~~„The left third is calm empty sky, uncluttered, **reserved for text**"~~

Ettől a modell a bal harmadot **külön panelként** rajzolja meg: lapos, textúra nélküli
felületet tesz oda, és a két rész között éles függőleges varrat marad. Tizennégy képből
nyolc így készült el, mind újragenerálásra szorult.

**Ami működik** — egyetlen jelenetként kell leírni, és a bal oldalt valódi tájelemmel
megtölteni:

```
ONE single continuous seamless scene …
The left third of the frame is unbroken meadow grass running to a low
treeline under a soft sky, quiet and free of objects; the subject sits in
the right two-thirds, and the ground/horizon line runs continuously across
the entire frame.
… Single uninterrupted photograph, no collage, no vertical seams,
no split screen, no flat panels, no text, no lettering, no people.
```

Három elem kell hozzá: (1) *ONE single continuous seamless scene* az elején,
(2) a horizont/talajvonal **átfut a teljes képen**, (3) a tiltólistán a
*collage · vertical seams · split screen · flat panels*.

**Ellenőrzés generálás után** — a varrat gépi úton kimutatható: oszloponkénti átlagos
abszolút szürkeérték-különbség; ahol ez az átlag hatszorosa fölé ugrik, ott varrat van.
A `scripts/oldalgyartas/` szkriptjei mellett ez néhány sor; szemre nem mindig látszik,
1440px-en viszont igen. Kiugrás **50% körül** szinte biztosan varrat; épületél és jármű
is adhat 4–5× jelet, azt szemre kell eldönteni.

Két további tiltás ugyanebből a családból: a *„soft-focus"* a bal oldalra életlen sávot
eredményez éles határral, a *„several situations side by side"* pedig filmszalagot.

### A fejlécképek is forráskép-szabály alá esnek

A 11.1 forráskép-szabály nem csak a főoldali fejlécképre vonatkozik: **minden** aloldali
fejlécképnél az `assets/img/alapkepek/` megfelelő darabja megy be referenciának, és a
prompt csak a környezetet, a fényt és a kameraállást írja le. Ami ebből következik:

- **Kitalált műszaki tartalom nincs.** A képen csak olyan berendezés szerepelhet, amelyik
  a könyvtárban is megvan. A tiltólistára külön ki kell írni, mit ne találjon ki:
  `no invented equipment or pipework, no perforated drainage pipes, no gravel trench
  drainfield, no soakaway pit`. Enélkül a modell a tartály mellé odarajzol egy
  kavicságyas, perforált csöves szikkasztómezőt — az elvezetés valódi eleme a
  könyvtárban a fekete szikkasztóblokk.
- **A felirat marad.** Referenciával a termék saját `A.B.CLEAR` felirata hibátlanul
  átjön, még 1800px-es kivágatban is olvashatóan. A „no lettering" tiltás helyett
  `no added text, captions or labels, no logos other than the product's own printed
  marking` kell — a régi, általános tiltás letörölné a termékről a feliratot.
- **Belső nézetnél mondd ki a kameraállást.** A könyvtár metszetrajzai felülnézetiek;
  ha a prompt nem mondja meg, hogy a kamera lefelé néz a nyitott aknába, a modell a
  berendezést oldalára fektetve a gyepre teszi. Kell hozzá: a kamera szöge, hogy a
  perem *a fűvel egy szintben* van, és hogy `nothing protrudes above the lawn`.
- **Régi épület csak ott, ahol a téma az.** Az emésztő kiváltásánál a repedt betongyűrű
  a tartalom lényege — a ház viszont ott is mai és felújított.

**Méretre vágás.** A mester 16:9-ben, 4K-ban készül; ebből jön a három méret
(`1800×764` · `1100×467` · `1100×718`). A széles kivágat az égboltból vesz el többet
(≈480px fentről az 5504×3072-es mesteren), a szűk `gravity east`, hogy a jobb
kétharmadban álló megoldás egészben megmaradjon. A lekicsinyítés **Mitchell**
újramintavételezéssel — az alapértelmezett Lanczos annyi fűtextúrát tart meg, hogy a
WebP ~25%-kal nehezebb lesz látható nyereség nélkül, és a fejléckép az LCP-elem.

## Amit tilos

- Tailwind vagy bármilyen CSS-keretrendszer
- inline `style` attribútum
- `!important` (kivéve dokumentált ütközésfeloldás)
- nyers hex, nyers px betűméret, köztes térköz
- `<div>`-gomb, `<button>` navigációra (navigáció mindig `<a>`)
- kép `alt` nélkül, dekoratív elem `aria-hidden` nélkül
