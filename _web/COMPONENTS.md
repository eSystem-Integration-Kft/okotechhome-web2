# Új komponensek — javaslat a designrendszerhez

**Állapot:** javaslat, jóváhagyásra vár
**Épít:** `OTH-design-system-Teszt.v2.html` / `.md` (v0.5)
**Implementáció:** `assets/css/app.css` → `@layer components`
**Első felhasználás:** 3. szekció — *Kiinduló helyzet* (`index.html`)

---

## Miért létezik ez a dokumentum

A designrendszer **10. fejezete** (*Ami még nincs definiálva*) kimondja, hogy az alábbiakra
hivatkozni tilos, mert nincs mögöttük implementáció — és ha a feladat ilyet igényel, azt
**jelezni kell, nem improvizálni**:

- Kártya (az e1 emelés komponense), médiakeret, adatpár-lista
- **Szekció-sáv** komponens
- **Kép- és illusztrációs rendszer** — arányok, `--media-tint`, képaláírás
- Táblázat, harmonika, idővonal, lépcsős folyamat
- Ikonrendszer

A 3. szekció megépítéséhez ezek közül **négyre** volt szükség: szekció-sáv, kártya, médiakeret
és kiemelt panel. Ezt ezennel jelezzük. A hiány áthidalása a **4. alapszabály** szerint történt —
*„Új variáns csak új, dokumentált osztállyal jöhet létre"* —, azaz:

- minden érték **meglévő tokenből** származik; egyedi px, hex és köztes térköz nincs,
- a réteg-sorrend (primitive → semantic → component) sértetlen: az új komponens-tokenek
  kizárólag **szemantikus** tokenre hivatkoznak, primitívre soha,
- minden témafüggő új komponens-token **újra van deklarálva** a `[data-theme="dark"]` blokkban
  (2.4 szabály).

Amint a designrendszer hivatalosan definiálja ezeket, az itteni osztályok a hivatalos
implementációra cserélendők.

---

## 1. Új komponens-tokenek

| Token | Érték | Témafüggő | Sötétben újradeklarálva |
|---|---|---|:--:|
| `--section-bg` | `var(--canvas)` | igen | ✅ |
| `--section-alt-bg` | `var(--surface-muted)` | igen | ✅ |
| `--card-bg` | `var(--surface)` | igen | ✅ |
| `--card-border` | `var(--border)` | igen | ✅ |
| `--card-shadow` | `var(--shadow-1)` → sötétben `none` | igen | ✅ |
| `--card-radius` | `var(--r-lg)` | nem | — |
| `--card-padding` | `var(--space-24)` | nem | — |
| `--panel-bg` | `var(--surface-muted)` | igen | ✅ |
| `--panel-border` | `var(--border)` | igen | ✅ |
| `--panel-radius` | `var(--r-xl)` | nem | — |
| `--panel-padding` | `var(--space-48)` / `32` / `24` töréspontonként | nem | — |
| `--media-ratio-card` | `3 / 2` → mobilon `16 / 9` | nem | — |
| `--media-ratio-panel` | `16 / 9` | nem | — |
| `--container-max` | `1180px` | nem | — |

**`--card-shadow` sötétben `none`.** Nem hibajavítás, hanem a 3. fejezet szabályának
végrehajtása: *„Sötét témában a mélységet a felület-lépcső viszi, nem az árnyék."*

**`--container-max`** nem új döntés: az 5.2 fejezet rögzíti az 1180px-es konténerszélességet.
Tokenné emelve, hogy ne szórt literálként éljen a kódban.

---

## 2. Szekció-sáv — `.section`

```html
<section class="section" aria-labelledby="szekcio-cim">
  <div class="section-inner">
    <header class="section-head">
      <p class="type-data-eyebrow section-eyebrow">Kiinduló helyzet</p>
      <h2 class="type-display-section-title section-title" id="szekcio-cim">…</h2>
    </header>
    …
  </div>
</section>
```

| Osztály | Szerep |
|---|---|
| `.section` | sáv: `--section-bg` háttér + `padding-block: var(--space-section)` |
| `.section-alt` | váltakozó sáv `--section-alt-bg` háttérrel (5.3: *„Szekció-sávok váltakoznak"*) |
| `.section-inner` | konténer: `max-width: var(--container-max)`, középre, `padding-inline: var(--page-gutter)` |
| `.section-head` | eyebrow + cím blokk, alatta `--space-48` |
| `.section-lead` | bevezető bekezdés a cím alatt, `max-width: 62ch` (olvashatósági korlát) |
| `.section-lead-wide` | variáns: a bevezető a teljes konténerszélességet használhatja |

**`.section-lead-wide` + `.br-desktop`.** Ahol a terv a bevezetőt fix sortöréssel mutatja
(5. szekció: két mondat, két sor), a 62ch korlát három sorra tördelne. A variáns feloldja a
korlátot, a törést pedig egy `<br class="br-desktop">` adja, amely **csak ≥1025px felett
látszik** — szűkebb képernyőn a szöveg természetesen tördel, ott a kényszerített törés csonka
sort hagyna.

- Asztali és tablet nézetben a fejléc **középre zárt**, mobilon **balra** — egy oszlopban a
  középre zárt, több soros cím olvasási horgony nélkül marad.
- A szekció **kötelezően** `aria-labelledby`-vel hivatkozik a saját `h2`-jére.

---

## 3. Kártyarács és kártya — `.card-grid`, `.card`

```html
<ul class="card-grid" role="list">
  <li class="card-item">
    <figure class="card-media">…</figure>
    <article class="card">
      <h3 class="type-ui-card-title card-title">…</h3>
      <p class="type-ui-body card-text">…</p>
      <a class="text-link card-action" href="…">
        <span class="action-arrow" aria-hidden="true">→</span>Hivatkozás szövege
      </a>
    </article>
  </li>
</ul>
```

**Emelés:** e1 — `--card-bg` + `--card-border` + `--card-shadow` (6. fejezet emelés-létra).

**Rács:** 4 oszlop asztali · 2 oszlop tablet · 1 oszlop mobil. `align-items: start`, tehát a
kártyák **nem nyúlnak egyforma magasra** — a kártya magasságát a saját tartalma adja.

**`.card-action { margin-top: auto }`** — a hivatkozás akkor is a kártya aljára kerül, ha a
szövegek eltérő hosszúak, így a linkek vízszintesen közel egy vonalba esnek.

**A kártya egésze nem kattintható.** Csak a benne lévő `.text-link` az. Ez tudatos: a teljes
felületű kattintás elrejtené a link célját a billentyűzetes és képernyőolvasós használat elől,
és ütközne a 7.2 *„navigációhoz `a`"* szabállyal.

**`.action-arrow`** dekoratív, `aria-hidden="true"`. A link szövege a nyíl nélkül is teljes
értelmű mondat — a 8. fejezet *„szín önmagában nem hordozhat jelentést"* elvének megfelelően
a nyíl sem hordoz információt.

### `.card-tag` — címke-chip

A kártya besorolását adja („Állandó használatra", „Nagy kapacitásra"). Az 5. szekcióban él.

```html
<span class="card-tag type-ui-label">Állandó használatra</span>
```

| Token | Érték |
|---|---|
| `--tag-bg` | `var(--surface-muted)` |
| `--tag-text` | `var(--text-primary)` |
| `--tag-radius` | `var(--r-md)` |

**Nem `.alert` és nem gomb.** A chip *besorolás*, nem státusz és nem művelet: nem interaktív,
nincs állapota, és nem hordoz olyan jelentést, amit a kártya címe és szövege ne mondana el.
Ezért önálló, semleges komponens.

### A kártyán belüli médiakeret

Az 5. szekcióban a kép a **kártyán belül** áll (a 3. szekcióban a kártya *fölött*, a canvason).
A térközt ilyenkor a kártya saját `gap`-je adja, ezért a keret alsó margója elmarad:

```css
.card > .card-media{margin-bottom:0}
```

---

## 4. Médiakeret — `.card-media`, `.panel-media`

A kivágott (alfacsatornás) illusztrációk befoglaló kerete. `object-fit: contain`, tehát a kép
sosem torzul és sosem vágódik le; a keret adja az egységes ritmust az eltérő méretarányú
képek mellett is.

```css
.card-media{
  display:flex; align-items:flex-end; justify-content:center;
  aspect-ratio:var(--media-ratio-card);
  min-height:0;
  margin-bottom:var(--space-16);
}
.card-media img{width:100%;height:100%;object-fit:contain;object-position:center bottom}
```

### `min-height: 0` — miért kötelező

A keret egyszerre **flex-konténer** (a képnek) és **flex-elem** (a `.card-item` oszlopában).
Flex-elemként az alapértelmezett `min-height: auto` a *tartalom* belső méretéből számol:
egy 800×533-as kép 460px szélességnél 306px magasságot követel, ami **felülírja az
`aspect-ratio`-t**. A hiba csak akkor látszik, ha a kép saját aránya **magasabb** a
szereptokenben megadottnál — ezért asztali nézetben rejtve maradt, és csak mobilon jött elő.
A `min-height: 0` adja vissza az irányítást a tokennek.

> Ha a designrendszer hivatalos médiakeretet definiál, ez a sor **nem hagyható el**.

### Reszponzív arány

Mobilon (≤640px) a kártya teljes szélességű, így a 3:2-es keret a viewport közel felét
elvinné, és négy egymást követő illusztráció a szöveget a hajtás alá tolná. Ezért a token
mobilon `16 / 9`-re vált — ugyanazzal a mintával, ahogy a rendszer a `--space-section` és a
display-méretek töréspontos váltását kezeli.

| Töréspont | `--media-ratio-card` | Keret magassága a viewporthoz |
|---|---|---|
| asztali / tablet | `3 / 2` | — |
| mobil ≤640px | `16 / 9` | 46% → 39% |

### `.card-media-product` — variáns álló/négyzetes renderhez

A 3:2-es alapkeret a **fekvő** helyzet-illusztrációkra van szabva. Az 5. szekció
termékrenderei álló (1086×1448) vagy négyzetes (1254×1254) arányúak; `contain` mellett ezek a
fekvő keretben eltörpülnének — a kártya szélességének alig felét töltenék ki. A variáns
négyzetes keretet ad (`--media-ratio-product: 1 / 1`), és középre igazít:

```css
.card-media-product{aspect-ratio:var(--media-ratio-product);align-items:center}
.card-media-product img{object-position:center}
```

---

## 5. Kiemelt panel — `.panel`

Kétoszlopos kiemelt blokk (szöveg + illusztráció), `--panel-bg` felületen, `--r-xl` sarokkal.
Tableten és mobilon egy oszlopra vált, és a **kép a szöveg elé kerül** (`order: -1`), hogy a
vizuális horgony vezesse be a blokkot.

A panel tartalmazza a szekció **egyetlen elsődleges CTA-ját** — a 7.1 szabály szerint
szekciónként egy `.btn-primary` engedett.

---

## 6. ⚠️ Jelzett eltérés — navigációs CTA gombként

A designrendszer **7.6 komponensválasztó táblája** determinisztikus:

| Szükséglet | Megoldás |
|---|---|
| Navigáció | `.text-link` |

A vizuális terv viszont a panel fő CTA-ját **kitöltött zöld gombként** mutatja, nem aláhúzott
szöveges linkként. Az implementáció:

```html
<a class="btn btn-primary panel-action" href="szervezeti-telepulesi-megoldasok">…</a>
```

- Az **elemtípus helyes**: navigáció → `<a>` (7.2 *„Döntési szabály: művelethez `button`,
  navigációhoz `a`. Nincs kivétel."*). A tiltólista is csak a `button`-t tiltja navigációra.
- Az **eltérés a megjelenésben van**: `a` elem `.btn-primary` stílussal.

**Kért döntés:** kerüljön-e a 7.6 táblába egy sor —
*„Szekció fő navigációs CTA-ja → `a.btn-primary`"* —, vagy a panel CTA-ja váltson
`.text-link`-re, a vizuális tervtől eltérve. Addig a jelenlegi megoldás él, jelölve.

---

## 7. Sorszámozott kártya — `.numbered-grid`, `.card-badge`

A 4. szekció három magyarázókártyája. A kártya maga a már definiált `.card`; új elem csak a
jelvény.

```html
<li class="card">
  <span class="card-badge type-data-value" aria-hidden="true">01</span>
  <p class="type-ui-body card-text"><strong>A zárt tároló gyűjt.</strong> …</p>
</li>
```

- A jelvény átmérője `--badge-size` = `var(--space-48)`, felülete `--badge-bg`
  (`--surface-muted`), a szám `.type-data-value` (mono, 12px).
- **`aria-hidden="true"`**: a sorszám vizuális rendezőelem, nem tartalom. A bekezdés első,
  félkövér mondata önmagában is azonosítja a technológiát.

---

## 8. Ikon — `.icon`

A designrendszer 10. fejezete szerint az **ikonrendszer definiálatlan** (méretskála,
vonalvastagság, `currentColor`-szabály). Ideiglenes megoldás egyetlen méretszereppel:

```css
.icon{
  display:block; width:var(--icon-size); height:var(--icon-size);
  background-color:currentColor;
  mask-image:url("../icon/tech-zart-tarolo.svg"); mask-size:contain; …
}
```

**Miért maszk, és nem `<img>`.** Az ügyféltől érkezett SVG-k CorelDRAW-exportok, beégetett
`fill:#21432B` értékkel — ez nyers hex a felületen, ami a 9. tiltólistába ütközik, és sötét
témában olvashatatlan lenne. A fájlokban a `fill` **`currentColor`-ra** cserélve
(`assets/icon/`), a színt pedig CSS-maszkkal a `currentColor` adja. `<img>`-ként betöltve a
`currentColor` nem oldódna fel a befoglaló dokumentum kontextusában.

Az ikonok **dekoratívak** (`aria-hidden="true"`): a jelentést mindig a mellettük álló
oszlopfejléc-szöveg hordozza (8. fejezet — *„szín önmagában nem hordozhat jelentést"*).

| Token | Érték |
|---|---|
| `--icon-size` | `var(--space-32)` — a **magasságot** rögzíti, nem a szélességet |

### Méretszabály: magasságra normalizálva, nem négyzetben

Az `--icon-size` az ikon **magassága**; a szélességet a rajzolat saját aránya adja
(`aspect-ratio` osztályonként).

| Osztály | Rajzolat | Arány | Megjelenítve |
|---|---|---|---|
| `.icon-zart-tarolo` | 52×41 | `52 / 41` | 41×32 |
| `.icon-oldomedence` | 67×41 | `67 / 41` | 52×32 |
| `.icon-biologiai` | 107×41 | `107 / 41` | 84×32 |

**Miért nem négyzetes doboz.** Négyzetes `32×32` kereten a `mask-size: contain` a
*szélességre* skáláz, tehát a legszélesebb rajzolat lesz a legalacsonyabb: a 107×41-es
ikon alig 12px magasan jelent meg, olvashatatlanul, míg az 52×41-es 25px-en. Az ikonsor
optikai súlya csak akkor egyenletes, ha a **magasság** a rögzített méret.

> Ha az ikonrendszer hivatalosan definiálódik, ez a szabály (magasság-normalizálás +
> per-ikon `aspect-ratio`) átemelendő, különben minden nem négyzetes ikon eltörpül.

---

## 9. Összehasonlító táblázat — `.compare-table`

A 10. fejezet szerint a **táblázat definiálatlan**. Az implementáció natív `<table>`-re épül,
teljes szemantikával:

- `<caption>` viszi a blokk címét (`.type-ui-card-title`) — nem külön `<h3>`, mert a cím
  a táblázathoz tartozik, és így a képernyőolvasó is a táblához köti,
- `<th scope="col">` az oszlopfejléceknél, `<th scope="row">` a sorfejléceknél,
- a csíkozás `tbody tr:nth-child(even)` alapon, `--table-row-alt-bg` felülettel,
- a `.compare-scroll` konténer `overflow-x:auto`, `role="region"`, `tabindex="0"` és
  `aria-labelledby` — így a táblázat **billentyűzetről is görgethető**, ha nem fér ki.

| Token | Érték |
|---|---|
| `--table-row-bg` | `color-mix(in srgb, var(--surface-muted) 60%, var(--surface))` |
| `--table-row-alt-bg` | `var(--surface)` |
| `--table-border` | `var(--border)` |
| `--table-cell-padding-block` | `var(--space-16)` |
| `--table-cell-padding-inline` | `var(--space-8)` |

### Három felület, nem kettő

A vizuális terven a tábla **három** felületet használ, nem kettőt:

| Réteg | Felület | Érték |
|---|---|---|
| panel | `--panel-bg` | `#E5EBBB` (Lime) |
| páratlan sor (1·3·5) | `--table-row-bg` | `#EDF1D4` — a panelnél halványabb zöld |
| páros sor (2·4) | `--table-row-alt-bg` | `#FAFAFA` (Stardust) |

A középső árnyalatra **nincs token**, és nyers hexet a 0.8 és a 9. szabály tilt. Ezért a
`--surface-muted` és a `--surface` **`color-mix`-e** adja — a rendszer maga is él ezzel
(`--topbar-bg`, `.btn-secondary:active`). Így az árnyalat témaváltáskor is együtt mozog a
két forrásfelülettel, ahelyett hogy beégetett érték lenne.

> Ha a designrendszer egyszer felvesz egy `--surface-muted-soft` szintet a felület-lépcsőbe,
> ez a `color-mix` arra cserélendő.

### Fejléc-igazítás

A fejléccellák `vertical-align: top`. Alsó igazításnál a kétsoros oszlopfelirat
(„Biológiai szennyvíztisztító") **feltolná a saját ikonját**, és az ikonsor elcsúszna.
Felülre igazítva mindhárom ikon egy vonalban áll, a hosszabb felirat pedig lefelé nő.

**A vízszintes belső térköz `--space-8`, nem `--space-16`.** A tábla a kétoszlopos szekcióalj
felén él: 1180px-es konténernél ~432px jut neki, és 16px-es cellatérköznél a negyedik oszlop
46px-szel kilógott. A `--space-8` pontosan a rendelkezésre álló szélességre hozza (432/432).
Ha a tábla egyszer teljes szélességű blokkba kerül, a `--space-16` visszaállítható.

Mobilon (≤640px) a tábla `min-width: 36rem` mellett görgethető marad — négyoszlopos
összehasonlítást 360px-en nem lehet torzításmentesen tördelni.

---

## 10. Termékkártya és kétoszlopos szekcióalj — `.product`, `.split`

- `.split` — `1fr 1fr` rács, tableten és mobilon egy oszlop.
- `.split-panel` — `--panel-bg` felület (az összehasonlító tábla kerete).
- `.split-card` — `--card-bg` felület, e1 emeléssel (a saját berendezések kerete).
- `.product-media` — négyzetes médiakeret (`--media-ratio-product: 1 / 1`), `object-fit: contain`,
  `min-height: 0` (lásd 4. pont).

---

## 11. `<strong>` súlya

A böngésző alapértelmezett `700`-as `<strong>` súlya kívül esik a rendszeren (4.4:
*„Nincs választható súlytartomány"*). A `base` réteg a `body-strong` szerep súlyára állítja:

```css
strong,b{font-weight:var(--type-ui-body-strong-weight)}   /* 600 */
```

---

## 12. Oldalfejléc — `.site-header`

A fejléc **két sávból** áll: fölül a kontaktsáv (`--topbar-bg` = `--canvas`), alatta a fő
navigációs sáv (`--header-bg` = `--surface`). A kettő felületkülönbsége adja a tagolást,
nem árnyék.

```html
<header class="site-header">
  <div class="topbar"><div class="topbar-inner">…</div></div>
  <div class="header-inner">
    <a class="site-logo" href="/">…</a>
    <details class="nav-drawer" open>
      <summary class="nav-toggle type-ui-button">Menü</summary>
      <nav class="site-nav" aria-label="Fő navigáció"><ul class="nav-list">…</ul></nav>
    </details>
    <a class="btn btn-primary header-cta" href="konzultacio">…</a>
  </div>
</header>
```

| Token | Érték | Sötétben újradeklarálva |
|---|---|:--:|
| `--topbar-bg` | `var(--canvas)` | ✅ |
| `--topbar-border` | `var(--border)` | ✅ |
| `--topbar-text` | `var(--text-primary)` | ✅ |
| `--topbar-icon` | `var(--primary)` | — (a Fern mindkét témán él) |
| `--header-bg` | `var(--surface)` | ✅ |
| `--header-border` | `var(--border)` | ✅ |
| `--header-shadow` | `var(--shadow-1)` → sötétben `none` | ✅ |
| `--header-h` | `calc(48 + 48 + 32)` = 128px, csak skálaértékekből | — |
| `--nav-text` | `var(--text-primary)` | ✅ |

**A kontaktsáv magasságát nem külön token adja**, hanem a benne álló hivatkozások
érintőcélpontja (`min-height: var(--space-48)`). Így a sáv és a kattintható felület nem
csúszhat szét, és nem keletkezik `--topbar-h`-tól független második magasságérték.
A fő sáv `min-height: var(--topbar-h)` (60px), a tényleges magasságát a 48px-es logó és a
`--space-16` belső térköz adja (80px).

### Tapadó (sticky) fejléc — miért az egész, és miért negatív `top`

```css
.site-header{position:sticky;top:calc(-1 * var(--space-48));z-index:30}
.header-main{border-bottom:1px solid var(--header-border);box-shadow:var(--header-shadow)}
```

A kívánt viselkedés: a kontaktsáv görgetéskor kicsússzon, a fő sáv maradjon a viewport
tetején. A kézenfekvő megoldás — `position: sticky` magán a fő sávon — **nem működik**:
a tapadó elem a *szülő* dobozán belül mozog, a fejléc pedig pontosan olyan magas, mint a
tartalma, így nincs hova tapadnia. Ezért a **teljes fejléc** tapad, `top`-ja pedig épp a
kontaktsáv magasságával negatív: a sáv kicsúszik, a fő sáv megáll a tetején.

Az árnyék (`--header-shadow` = `--shadow-1`) a **legfinomabb emelés**; sötét témában
elmarad, a 3. fejezet szabálya szerint (*ott a mélységet a felület-lépcső viszi*).

> ⚠️ **Nyitott:** a fejléc `z-index: 30`. A rendszerben nincs réteg- (z-index-) skála;
> a jelenlegi értékek: fejléc 30 · menüpanel 20 · skip-link 30 · hero szöveg 1.
> Ha a designrendszer felvesz egy réteg-skálát, ezek arra cserélendők.

### ⚠️ Jelzett eltérés — a kontaktsáv hivatkozásai nem `.text-link`

A 7.6 tábla szerint a navigáció `.text-link`, ami aláhúzott, `--link` színű és 44px magas.
A kontaktsáv három adata (cím, e-mail, telefon) így három kék, aláhúzott blokk lenne egy
13px-es utility sávban. Az implementáció `.topbar-link`: `--text-primary` szín, aláhúzás
csak hoverkor, de **teljes értékű fókuszgyűrű és 48px-es érintőcélpont**.

**Kért döntés:** kapjon-e a 7.6 tábla egy sort — *„utility sáv hivatkozása → `.topbar-link`"* —,
vagy a sáv váltson `.text-link`-re a vizuális tervtől eltérve.

### ⚠️ Jelzett eltérés — a navigáció nagybetűs

A `.nav-link` `text-transform: uppercase`-t kap. A rendszerben ilyet eddig csak a
`.type-data-eyebrow` szerep tett; a `type-ui-button` szerepnek nincs nagybetűs variánsa.
A vizuális terv viszont nagybetűs menüt mutat. Ha ez marad, érdemes szerepszinten
rögzíteni (pl. `--type-ui-nav-*`), hogy ne komponensszabály hordozza.

### Lenyitható menü natív elemmel

A 0.7 alapszabály (*„a viselkedést nem újraépítjük, hanem a platformtól kérjük"*) miatt a
menü `<details>`/`<summary>`, nem JS-vezérelt panel. A markupban **nyitva** áll, ezért
JS nélkül is elérhető; a `site.js` mindössze annyit tesz, hogy ≤1024px-en becsukja, és
kezeli az Esc-et meg a panelen kívüli kattintást.

A GYIK és a Karrier ≤640px-en a kontaktsávból a menübe költözik (`.nav-item-secondary`) —
szűk sávban a hat elem tördelése két sorra tolná a fejlécet.

### Megamenü — `.nav-trigger` + `.mega`

A sitemap **2. szintje** a fejlécből érhető el. Öt főkategória kap panelt (Helyzetem ·
Megoldások · Előkészítés · Tudástár · Eredmények), a maradék három (Ügyféltámogatás ·
Partnereknek · ÖkoTech-Home) a kontaktsávban áll — nyolc nagybetűs menüpont nem fér el a
logó és a CTA mellett.

```html
<li class="nav-item">
  <button type="button" class="nav-link nav-trigger type-ui-button"
          aria-expanded="false" aria-controls="mega-megoldasok">
    Megoldások<span class="nav-caret" aria-hidden="true"></span>
  </button>
  <div class="mega" id="mega-megoldasok" hidden>
    <div class="mega-inner">…<ul class="mega-list">…</ul>…</div>
  </div>
</li>
```

- A nyitóelem **`button`**, nem `a`: művelet, nem navigáció (7.2). A cél-oldalra a panel
  alján álló „Áttekintés: …" hivatkozás visz.
- A panel **`hidden` attribútummal** zár, ezért JS nélkül sem marad nyitva lógva.
- Egyszerre egy panel nyitott; **Esc** és a panelen kívüli kattintás zár, a fókusz
  visszatér a nyitó gombra. Nézetváltásnál (`matchMedia`) automatikusan zár, mert a
  pozicionálás is más.
- Asztali nézetben a panel a **fejléc teljes szélességén** ül (`.header-main` a
  pozicionálási kontextus), szűk nézetben a menüpont alatt, a folyamban nyílik.
- A menücímke rövidíthető (`Projekt-előkészítés` → `Előkészítés`); a panel fejléce és a
  cél-hivatkozás a **teljes** kategórianevet viszi.

> A `.nav-list` oszlopköze `--space-16` (nem 24): öt nagybetűs menüpont a lenyíló
> nyilakkal 24px-es közzel két sorba tördelt 1440px-en.

---

## 13. Hero — `.hero`

```html
<section class="hero" aria-labelledby="hero-cim">
  <div class="hero-inner"><div class="hero-copy">…</div></div>
  <figure class="hero-media" data-hero-video data-video-webm="…" data-video-mp4="…">
    <picture>…</picture>
  </figure>
</section>
```

| Token | Érték |
|---|---|
| `--hero-media-ratio` | `16 / 9` → ≤1024px `3 / 2` |
| `--hero-min-h` | `calc(100svh - var(--header-h))` |
| `--dur-media` | `600ms` |

### Borító-elrendezés

```css
.hero{
  display:grid;
  grid-template-columns:minmax(0,1fr);
  min-height:var(--hero-min-h);
}
.hero > .hero-inner,.hero > .hero-media{grid-column:1;grid-row:1}
.hero-inner{position:relative;z-index:1;align-self:start}
```

A szöveg és a médiablokk **ugyanabban a rácscellában** ül, a szöveg `z-index: 1`-gyel fest
fölötte. Így a felvétel a **teljes hero-felületet** kitölti, a szöveg pedig rajta.

A magasságot három tényező közül a **legnagyobb** adja:

| Forrás | Mikor dominál |
|---|---|
| `--hero-min-h` (`100svh − --header-h`) | alacsony ablakban — a hero mindig kitölti a képernyőt |
| `--hero-media-ratio` (16:9) | széles ablakban — a felvétel torzítatlanul elfér |
| a szövegoszlop magassága | keskeny asztali ablakban |

Ezért mozog a hero **a képernyővel együtt**: átméretezéskor folyamatosan a fenti három
közül a nagyobb érvényesül, a `cover` pedig a felvételt igazítja hozzá. A rács oszlopa
`minmax(0,1fr)` — `auto` mellett a rács a tartalom szélességére húzódna, és a médiablokk
aránya nem számolna magasságot.

≤1024px-en **nincs borító**: a hero blokk-elrendezésre vált (szöveg, alatta a szűk
kivágatú kép), mert egy oszlopban a mozgókép fölé szedett szöveg nem tartható olvashatóan.

### Lágy folt (veil) a szöveg mögött

```css
.hero-media::after{
  background:radial-gradient(ellipse 50ch 34ch at var(--hero-veil-x) 46%,
    var(--hero-veil) 0%,
    var(--hero-veil-soft) 52%,
    transparent 100%);
}
```

| Token | Érték | Sötétben újradeklarálva |
|---|---|:--:|
| `--hero-veil` | `color-mix(in srgb, var(--canvas) 90%, transparent)` | ✅ |
| `--hero-veil-soft` | `color-mix(in srgb, var(--canvas) 64%, transparent)` | ✅ |
| `--hero-veil-x` | `calc(50% − var(--container-max)/2 + var(--page-gutter) + 26ch)` | — |

- **Ellipszis, nem sáv.** A folt minden irányban a nulláig fut ki, ezért **sehol nincs
  éle, határa vagy vágása**. Korábbi iterációk lineáris gradienssel dolgoztak; az
  bármilyen finomra hangolva látható átmenetet („fade-t") hagyott a szöveg mellett.
- **A közepe a konténerhez kötött** (`--hero-veil-x`), nem viewport-százalékhoz — így a
  szövegoszlop fölött marad minden képernyőszélességen.
- **Csak annyit emel**, hogy a felvétel kontúrjai ne fussanak bele a betűkbe; a kép a
  szövegtől jobbra és lefelé végig tisztán látszik.
- Az **állóképnél gyakorlatilag láthatatlan**: ott a felső régió alfás, a folt a canvasra
  fest canvast.
- ≤1024px-en kikapcsolva (`display: none`): egy oszlopban a szöveg nem a felvételen áll.

> ⚠️ **Kontraszt.** A folt a leggyakoribb kockákon 4,5:1 fölé emeli a szöveget, de a
> mozgókép változó háttere miatt a WCAG 2.2 AA **nem garantálható minden pillanatban**.
> A rendszer mozgókép-szabályának megszületésekor ez felülvizsgálandó.

> Ez a `--media-tint` szereptoken első tényleges felhasználása lenne, ha a designrendszer
> definiálná (10. fejezet: a kép- és illusztrációs rendszer hiányzó része).

### ⚠️ Új időtartam-szerep — `--dur-media`

A rendszerben egyetlen időtartam él, a `--dur-fast` (150ms). Az állókép→videó átúszás
azon a hosszon ugrásnak látszik. A `--dur-media: 600ms` javaslat egy **lassabb,
médiaváltásra való** szerepre.

### Kép: art direction, nem csak méretezés

A `<picture>` ≤1024px-en **más kivágást** tölt (`…-szuk.webp`, 3:2), nem csak kisebb
fájlt. Indok: a széles változat felső harmada alfás égbolt, amit asztali nézetben a fölé
csúszó szöveg tölt ki — egy oszlopban ugyanaz a sáv üresen maradna.

| Nézet | Fájl | Méret |
|---|---|---|
| ≥1025px | `hero-rendszer-allokep.webp` (1024w / 1672w) | 16:9, teljes jelenet |
| ≤1024px | `hero-rendszer-allokep-szuk.webp` (800w / 1300w) | 3:2, szűk kivágat |

### Videó — feltételes, JS-ből

A hero videója **nincs benne a HTML-ben**. A `site.js` csak akkor hozza létre és tölti be,
ha mindhárom feltétel teljesül: `min-width: 1025px`, `prefers-reduced-motion: no-preference`,
és nincs `navigator.connection.saveData`. Egyébként az állókép marad — **az a végállapot,
nem helyőrző**.

- A videó a `load` esemény után indul, hogy ne versenyezzen az LCP-elemmel (az állóképpel).
- Csak akkor úszik be (`[data-ready]`), ha a `play()` ténylegesen elindult.
- `aria-hidden="true"`, `tabindex="-1"`: a jelentést az állókép `alt`-ja hordozza.
- Formátumok: WebM (VP9) elsőként, MP4 (H.264) tartalékként.

**Égbolt-átmenet.** A felvétel égboltja Stardust-fehér, a szekciósáv Drizzle — a videó
felső éle e nélkül látható vízszintes törés lenne. A `.hero-media[data-video-ready]::before`
egy `--space-96` magas átmenetet fest közvetlenül a médiablokk fölé, `--canvas`-ból
`--surface`-be. Csak akkor él, amikor a videó tényleg megy: az állókép égboltja alfás,
ott nincs mit elfedni.

---

## 13/a. Inverz gomb — `.btn-inverse`

A hero második gombja („Mennyibe kerül?"). A vizuális terv a **legsötétebb felületen**
mutatja (közel Forest), nem az Olive Leaf másodlagos színen.

| Token | Érték | Sötétben |
|---|---|---|
| `--button-inverse-bg` | `var(--surface-inverse)` (Forest) | `var(--surface-muted)` |
| `--button-inverse-text` | `var(--text-on-dark)` | `var(--text-primary)` |

**Miért nem `.btn-secondary`.** A 7.1 két gombváltozatot definiál; a `.btn-secondary`
felülete az Olive Leaf (`#56642B`), a terven viszont ennél jóval sötétebb gomb áll. A
`.btn-inverse` nem harmadik hierarchia-szint: ugyanaz a *másodlagos* szerep, más felületen.

**Sötét témában nem maradhat Forest**, mert az ott maga a sáv színe — a felület-lépcső
következő foka (`--surface-muted`) adja a kontrasztot.

> **Kért döntés:** a 7.1 vegye-e fel harmadik gombváltozatként, vagy a `.btn-secondary`
> felülete változzon a terv szerint.

---

## 13/b. Helyzetoszlop és ikonjelvény — `.situation`, `.icon-badge`

A 3. szekció négy kiinduló helyzete. **Nem kártya:** a canvason ülnek, felül vékony
elválasztó vonallal és kerek ikonjelvénnyel — a vizuális terv szerint.

```html
<li class="situation">
  <span class="icon-badge" aria-hidden="true">
    <span class="icon icon-inline icon-inline-lg icon-epitkezes"></span>
  </span>
  <h3 class="type-ui-card-title situation-title">…</h3>
  <p class="type-ui-body situation-text">…</p>
  <a class="text-link situation-action" href="…">
    <span class="link-label">Építkezés előtt állok<span class="action-arrow-end" aria-hidden="true">→</span></span>
  </a>
</li>
```

| Token | Érték |
|---|---|
| `--badge-lg-size` | `calc(var(--space-64) + var(--space-16))` = 80px — az ikonjelvény átmérője |
| `--icon-size-badge` | `calc(var(--space-32) + var(--space-4))` = 36px — a rajzolat a jelvényben |
| `--badge-bg` / `--badge-text` | a sorszámjelvényével közös (Lime felület, Forest rajzolat) |

**A méretek a tervről mérve**, nem becsülve: a kör 80px, benne a rajzolat 36px (45%).
Mindkettő skálaértékek összege — köztes egyedi méret nincs. Az ikonok vonalvastagsága
`1.8` a 24-es viewBoxban, ami 36px-en 2,7px — ez adja a terv optikai súlyát.

### Szövegszínek — a tervről mérve

| Elem | Token | Mért érték a terven |
|---|---|---|
| szekció- és oszlopcím | `--text-primary` | ≈ `#0f1c0f` (Forest) |
| törzsszöveg | `--text-tertiary` | `#697542` — **nem** a másodlagos (Olive Leaf) |
| hivatkozás | `--link` | `#1c6278` |
| panel eyebrow | `--panel-dark-muted` | `#849274` |
| panel cím | `--panel-dark-text` | `#ffffff` |
| panel törzsszöveg | `--panel-dark-muted` | `#849b7f` — **nem** a tiszta világos |
| panel hivatkozás | `--panel-dark-link` | `#c4eaf5` — világoskék, nem fehér |

- A rács 4 · 2 · 1 oszlop (asztali · tablet · mobil).
- A felső vonal `border-top: 1px solid var(--border)` + `padding-top: var(--space-32)`.
- `.situation-action { margin-top: auto }` — a hivatkozás akkor is az oszlop alján zár,
  ha a szövegek eltérő hosszúak.

### `.link-label` — miért kell a burok

A nyíl a felirat **után** áll, nem előtte (a 3. szekció terve így mutatja; a korábbi
szekciókban `.action-arrow` előre került). A `.text-link` viszont `inline-flex`, így a
nyíl külön flex-elemként a **sor végére** csúszna, nem a szó után. A `.link-label`
(`display: inline`) egy elembe fogja a feliratot és a nyilat.

> **Kért döntés:** a 7.2 rögzítse-e a nyíl helyét (elöl vagy hátul), vagy maradjon
> szekciónként a vizuális tervre bízva. Jelenleg mindkét minta él az oldalon.

---

## 13/c. Sötét kiemelt panel — `.panel-dark`

A 3. szekció záró blokkja: a legsötétebb felületen, kétoszlopos (cím | szöveg + link).

| Token | Érték | Sötétben |
|---|---|---|
| `--panel-dark-bg` | `var(--surface-inverse)` (Forest) | `var(--surface-muted)` |
| `--panel-dark-text` | `var(--text-on-dark)` | `var(--text-primary)` |
| `--panel-dark-muted` | `var(--text-on-dark-muted)` | `var(--text-secondary)` |

- Az emelést itt **nem árnyék adja, hanem a felület-váltás** — a 6. fejezet
  emelés-létrájának szellemében.
- A hivatkozás a panelen a **szövegszínt** veszi fel: a `--link` kékje (`#2F6F82`) Forest
  felületen nem éri el a 4,5:1-et.
- Sötét témában a Forest maga a sáv színe, ezért a panel a felület-lépcső következő fokára
  ül (`--surface-muted`), a szöveg pedig a normál szövegszínt kapja.

---

## 14. Chip-hivatkozás — `.chip-link`

A hero harmadik, kiegészítő belépési pontja („Már van ajánlata? Hasonlítsa össze").

| Token | Érték | Sötétben újradeklarálva |
|---|---|:--:|
| `--chip-bg` | `var(--surface-muted)` | ✅ |
| `--chip-text` | `var(--text-primary)` | ✅ |
| `--chip-radius` | `var(--r-md)` | — |

A gombsorral közös csoportban áll (`.hero-cta`, `flex-direction: column`,
`align-items: flex-start`), így a térköz egységes, a chip szélességét viszont **a saját
tartalma** adja — nem nyúlik a fölötte álló két gomb szélességére.

**Miért nem gomb és miért nem `.card-tag`.** A 7.1 szerint szekciónként **egy**
`.btn-primary` áll; a hero fő CTA-ja már az. Harmadik gombként ez a hivatkozás
azonos súllyal versenyezne a másik kettővel. A `.card-tag` viszont nem interaktív,
nincs fókuszállapota és nincs hover-emelése. A `.chip-link` a kettő között áll: chip
megjelenés, hivatkozás-viselkedés, 44px érintőcélpont, látható fókusz.

---

## 15. Bizalmi sáv — `.trust-grid`

Négy állítás középre zárva, függőleges elválasztókkal.

| Token | Érték | Sötétben újradeklarálva |
|---|---|:--:|
| `--trust-divider` | `var(--border)` | ✅ |

- **Oszlopköz szándékosan nincs.** Az elválasztó a cellahatáron fut (`border-left`),
  a levegőt a cellák belső tere adja (`padding-inline: var(--space-24)`). Oszlopközzel a
  vonal a hézag szélére kerülne, nem a közepére.
- 4 oszlop asztali · 2 oszlop tablet · 1 oszlop mobil; egy oszlopban az elválasztó
  vízszintesre vált (`border-top`).
- A cím `.type-ui-card-title`, a magyarázat `.type-ui-subtitle`.

### `.trust-title-data` — mono variáns

A szabvány- és tanúsítványjelölés (`EN 12566-3`, `ISO 9001`) **adat**, nem cím, ezért mono
betűvel áll — a 4.2 szerepkiosztás szellemében (`--font-mono` = adat). Méretszerepet nem
vált: a `.type-ui-card-title` 16px-e marad, csak a betűcsalád más. Külön `type-data-*`
szerep nem használható, mert azok 11–12px-esek, és a sáv címei nem apró adatcímkék.

---

## 16. Soron belüli ikonok — `.icon-inline`

| Token | Érték |
|---|---|
| `--icon-size-inline` | `var(--space-16)` — kontaktsáv |
| `--icon-size-inline-lg` | `var(--space-24)` — chip |

A 8. pont a **magasság-normalizálást** rögzítette a blokk-ikonokra (52×41 … 107×41).
A soron belüli ikonoknál viszont a **befoglaló négyzet** a helyes szabály: ezek a
rajzolatok közel négyzetesek (18×11, 13×18, 14×15, 24×24), így `mask-size: contain`
mellett az optikai súlyuk egyforma marad, és a szövegsorban egy vonalban ülnek.
Magasságra normalizálva a 18×11-es boríték kétszer olyan széles lenne, mint a 13×18-as
helyszín-ikon.

Az ikonok forrása az ügyféltől érkezett CorelDRAW-export, a `fill` `currentColor`-ra
cserélve (`assets/icon/ui-{helyszin,email,telefon}.svg`) — ugyanaz az eljárás, mint a
technológiai ikonoknál.

> ⚠️ **`ui-dokumentum.svg` ideiglenes.** A chip „ajánlat" ikonjához nem érkezett
> ügyféleszköz; a jelenlegi rajzolat saját, vonalas pótlás. Ügyféleszköz érkezésekor
> cserélendő.

---

## 17. Logó — `assets/img/logo-okotechhome.svg`

Az **ügyféltől kapott kétszínű SVG** (CorelDRAW-export, 928,41 × 289,93 viewBox), két
path, két osztály:

| Osztály | Rajzolat | Szín |
|---|---|---|
| `.fil0` | jelrajz (ház + fa) | `#80A640` — a márkapaletta Fern színe |
| `.fil1` | szóvédjegy („ÖkoTechHome") | `#133216` (Forest), sötét rendszertémán `#FAFAFA` (Stardust) |

Az eszközön egyetlen módosítás történt: a `.fil1` kapott egy
`@media (prefers-color-scheme:dark)` szabályt. Ezt az SVG saját `<style>`-ja viszi, mert a
logó `<img>`-ként töltődik be — ott a külső dokumentum `currentColor`-ja nem oldódna fel.

A méretezés a fejlécben: `height: var(--space-48)`, `width: auto` — a **magasság** a
rögzített méret, a szélességet a rajzolat aránya adja (ugyanaz a szabály, mint a
blokk-ikonoknál, 8. pont). A `width`/`height` attribútum a natív viewBox-méret, hogy a
böngésző a betöltés előtt is ismerje az arányt (CLS).

> ⚠️ **Két nyitott pont.** (1) A nyers hex a márkaeszköz saját színe, nem felületszín —
> a 0.8/9. tiltás CSS-re vonatkozik; ha a rendszer felvesz `--brand-*` tokeneket, ide is
> azok jönnek. (2) A `prefers-color-scheme` a **rendszertémát** követi, a `[data-theme]`
> kapcsolót nem. Amikor a témaváltó UI megépül, a logót inline SVG-re kell cserélni
> `currentColor`-os szóvédjeggyel.

---

## 18. AI-alapú döntéstámogató — `.aidt-*`

A 8. szekció (*„Mitől függ az ár?"*) a Test1 (`okotechhome-web`) §6 moduljából került át.
**A funkció és az elrendezés változatlan; a megjelenés teljes egészében a Test2
designrendszerére van átültetve.**

| Réteg | Mi történt vele |
|---|---|
| `assets/js/ai-advisor.js` (566 sor) | **változatlanul átvéve** — kérdéssor, állapotkezelés, ársáv-logika, eredményképernyő |
| `.aidt-*` CSS (~200 sor) | **újraírva**: minden érték a Test2 tokenjeiből |
| szekció-váz (HTML) | a Test2 `.section` / `.section-inner` szerkezetébe illesztve |

### Token-megfeleltetés (Test1 → Test2)

| Test1 | Test2 |
|---|---|
| `--paper`, `--paper-2` | `--canvas` |
| `--ink-text` / `--muted` | `--text-primary` / `--text-secondary` |
| `--line-light`, `--ag-line` | `--border` |
| `--emerald` / `--emerald-d` | `--primary` / `--secondary` |
| `--foam`, `--mint` | `--surface-muted` |
| `--ink`, `--ink-3` (gradiens) | `--surface-inverse` (sík felület) |
| `--gold` | `--warning-border` / `--warning-text` |
| `--shadow-sm` | `--card-shadow` |
| `clamp()` méretek | fix skálaértékek (`--space-*`) |
| pill (`100px`) sarkok | `--r-md` — a Test2 gombformája |
| nyers `px` betűméretek | `--type-*` szereptokenek |

**Miért a CSS hordozza a betűméretet.** A modul DOM-ját JS generálja, a markupban nincs
`.type-*` szereposztály. A komponens-CSS ezért közvetlenül a **szereptokenekre** hivatkozik
(`font-size: var(--type-ui-body-size)`), nem nyers px-re — a réteg-sorrend így sértetlen.

### Az ársáv a kódon kívül él — `assets/data/aidt-konfig.js`

A modul **nem tartalmaz árakat**. Az összes érték a fenti konfigfájlban áll, amit a cég
fejlesztő nélkül szerkeszthet; a modul `window.OTH_AIDT.arsav`-ból olvassa (ha a fájl
hiányzik, a JS-ben álló tartalék lép életbe, hogy a szekció ne törjön el).

```js
window.OTH_AIDT = {
  arsav:   { base: { "1-2": [1600000, 2200000], … }, modifiers: { talajviz: 350000, … } },
  endpoint: "",                                  // az összefoglaló-küldés végpontja
  adatkezelesUrl: "adatkezelesi-tajekoztato"
};
```

Szerkesztés után a hivatkozás verzióját is emelni kell (`aidt-konfig.js?v=NN`), mert a
`.htaccess` egy évig cache-eli a JS-t.

> ⚠️ Az értékek **még nincsenek jóváhagyva** — éles indulás előtt a cég szakmai
> vezetésének kell megerősítenie őket.

### Adatküldés és adatkezelés

- **Van végpont** (`endpoint` kitöltve): az űrlap `POST`-tal küldi a strukturált profilt
  (e-mail, visszahívás-jelölés, válaszok, számított ársáv, időbélyeg), és csak a sikeres
  válasz után írja ki, hogy elküldte. Hiba esetén `role="alert"` üzenet és telefonszám.
- **Nincs végpont** (jelenlegi állapot): a modul **nem állítja, hogy elküldte** — kiírja,
  hogy a küldés még nincs élesítve, és felkínálja a telefonos utat. Félrevezető
  visszaigazolás nincs.
- A hozzájárulás alatt megjelenik az **adatkezelési tájékoztató** hivatkozása
  (`adatkezelesUrl`).

> **CSP:** saját domainre mutató végpontot a jelenlegi `default-src 'self'` enged. Külső
> (CRM-)végpontnál a `.htaccess`-ben `connect-src 'self' <domain>` kiegészítés kell.

### JS nélkül — `<noscript>`

A szekció `<noscript>` blokkja elmondja, mit kérdezne a modul (a hat témát), és felkínálja
a telefonos, illetve e-mailes utat — így JS nélkül sem zsákutca a szekció.

---

## 18/a. Sötét felület — a hiányzó középső szövegfok, `--text-on-dark-soft`

**Világos** felületen három szövegszint él: `--text-primary` / `--text-secondary` /
`--text-tertiary`. **Sötét** felületen eddig csak kettő: a majdnem fehér
`--text-on-dark` (Stardust) és a jóval halványabb `--text-on-dark-muted`. A kettő között
akkora a lépés, hogy minden folyó szöveg és minden hivatkozás a legvilágosabb fokra
került — a láblécben ez öt hasábnyi, csupa maximális kontrasztú szöveget jelentett.

**Amit ez okoz.** Világos szöveg sötét alapon optikailag vastagabbnak és „izzónak"
látszik: a fényes felület a szemben túlnyúlik a betű határán (irradiáció), és a kijelző
gammája ezt még fel is erősíti. Nem betűsimítási hiba — a `-webkit-font-smoothing:
antialiased` a `body`-n eleve be van kapcsolva, tehát a WebKit már szürkeárnyalatosan
rajzol. A jelenséget a KONTRASZT MÉRTÉKE okozza, nem a rajzolás módja.

```
--text-on-dark-soft: color-mix(in srgb, var(--color-stardust) 86%, var(--color-forest));
```

| | kontraszt Forest alapon |
|---|---|
| `--text-on-dark` (Stardust) | **13,3:1** |
| `--text-on-dark-soft` | **10,2:1** — AAA-n belül (7:1) |
| `--text-on-dark-muted` | 5,5:1 — AA |

Mire való: **folyó szöveg és hivatkozáslista sötét felületen**. Címre, kiemelt értékre és
`:hover`-re marad a teljes `--text-on-dark` — a visszakapott világosság maga is jelzés.

Két kísérő beállítás ugyanitt:

- **`-moz-osx-font-smoothing: grayscale`** a `body`-n, a meglévő WebKit-es párja mellé.
  Enélkül ugyanaz a lap más betűvastagságot mutat Firefoxban és Chrome-ban macOS alatt.
- **`line-height: 1.55`** a lábléc hasáblistáin. A tételek kétsorosra törnek
  („Nincs elérhető / közcsatorna"); sötét alapon a szűk sorköz vibrálni látszik.

> **Ami még hátravan:** a `--panel-dark-text` (a sötét kiemelt panelek törzsszövege) még
> a teljes `--text-on-dark` fokon áll. Ott a szöveg rövid — két-három mondat —, tehát a
> jelenség sokkal kevésbé zavaró; ha egységesíteni akarjuk, ez a token cserélendő.

---

## 19. Amire még nincs megoldás

- **Képaláírás** és `--media-tint` — a kép- és illusztrációs rendszer hiányzó része
- **Ikon-méretskála és vonalvastagság** — jelenleg három méretszerep él
  (`--icon-size`, `--icon-size-inline`, `--icon-size-inline-lg`), skála és
  vonalvastagság-szabály nélkül
- **Sötét témájú `.alert`** — a státusz-tokenek nem témafüggők (designrendszer 10.)
- **Szekció-sáv váltakozás:** az 5.3 elv szerint a sávoknak váltakozniuk kell
  (`canvas → surface-muted → sötét`). A hero, a bizalmi sáv, a 3. és a 4. szekció a
  vizuális terv szerint **egyaránt canvas** sávon ül. A `.section-alt` osztály készen áll;
  a ritmust a teljes oldal összeállásakor kell eldönteni.
- **Fejléc viselkedése görgetéskor** — a terv statikus fejlécet mutat, a rendszerben
  viszont van `--topbar-h` token, ami tapadó (sticky) fejlécre utal. Amíg a designrendszer
  nem mondja ki, a fejléc statikus marad.
- **Videó a designrendszerben** — mozgókép, `poster`, autoplay-szabály és
  `prefers-reduced-motion`-viselkedés nincs definiálva. A hero videója a 8. fejezet
  akadálymentességi elvei szerint készült (dekoratív, feltételes betöltés), de ez
  jelenleg **komponensdöntés, nem rendszerszabály**.
- **Betűtípus-önhosztolás** — a Google Fonts külső kérés; a CSP `style-src`/`font-src`
  emiatt engedi a `fonts.googleapis.com`/`fonts.gstatic.com` hosztot. Önhosztolt woff2
  esetén mindkettő szűkíthető `'self'`-re.

---

## 20. Szippantási díj kalkulátor — `.szip-*`

A `/szippantasi-dij-kalkulator` modul-oldal felülete. Modul-oldal (oldaltípus 6.), tehát a
**számérték nem a kódban él**, hanem szerkeszthető konfigban:
`assets/data/szippantas-konfig.js`.

| Réteg | Hol |
|---|---|
| felület (`.szip-*`, ~330 sor) | `assets/css/app.css` 5.21 |
| logika | `assets/js/szippantas.js` |
| adat és példaértékek | `assets/data/szippantas-konfig.js` |
| beküldés | `api/szippantasi-dij.php` |
| oldalgenerátor | `scripts/oldalgyartas/szippantasi_kalkulator.py` |

### Egy képlet mind a három díjszabásra

```
elszámolt m³ = max(elszállított m³, a minimumdíjban foglalt m³)
alapdíj      = max(minimumdíj, ürítési díj × elszámolt m³)
alkalmi díj  = kiszállási díj + alapdíj + távolsági díj + egyéb
```

A megrendelői brief három szerkezetet ír le; ez az egy képlet mindhármat lefedi, ezért a
felületen nincs „díjszabás-típus" választó — a látogatónak nem kell besorolnia a saját
számláját egy kategóriába:

| eset | mit ír be | mit ad a képlet |
|---|---|---|
| nincs minimumdíj | 0 Ft, 0 m³ | kiszállás + ürítés × m³ |
| minimumdíj alsó korlát | minimumdíj, 0 m³ | a `max()` felemeli a kis mennyiséget |
| a minimumdíj X m³-t tartalmaz | minimumdíj, X m³ | az elszámolt m³ sosem kevesebb X-nél |
| a teljes kocsit ki kell fizetni | X = a kocsi űrtartalma | mindig a teljes kocsi |

A **minimum-felár** (`alapdíj − ürítési díj × ténylegesen elszállított m³`) a modul
legfontosabb kimenete: ezt fizeti ki a látogató úgy, hogy nem viszik el. Definíció szerint
sosem negatív, mert az alapdíj nagyobb-egyenlő nála.

### Az adatbázis üres — és ez látszik is

A `dijak` tömb **szándékosan üres**: egyetlen település díjszabását sem ismerjük ellenőrzött
forrásból. A csempetérkép ezért induláskor minden vármegyén „még nincs adat" állapotot mutat,
szaggatott kerettel — az üres hely így szándékosnak látszik, nem hibának.

Egy sor felvételéhez `megye`, `telepules`, `ervenyes` és `forras` kötelező. A díjmezőkben a
**`null` és a `0` nem cserélhető fel**: a `0` valódi érték (nincs kiszállási díj), a `null`
azt jelenti, hogy nem tudjuk. A felület és a levélsablon is külön kezeli a kettőt.

A beküldés **nem ír közvetlenül a konfigba**: e-mailben érkezik, és emberi ellenőrzés után
kerül be. Az automatikus felvétel egy elgépelt nullát azonnal minden látogatónak
kiszolgálna.

### Csempetérkép, nem földrajzi térkép — `.szip-terkep-racs`

19 vármegye + Budapest, 6 oszlop × 5 sor rácsban. Minden egység **azonos méretű csempe**, a
helyük a valós kelet–nyugati és észak–déli sorrendet követi. Pontos határvonalat
szándékosan nem rajzolunk: arra nincs hiteles térképi forrásunk, a csempe viszont nem is
állít ilyet. A rácshely a konfigban él (`sor`, `oszlop`), tehát átrendezhető kód nélkül.

640px alatt a rács vízszintesen görgethető (`.szip-terkep-gorgo`), mert hatoszlopos rácsban
360px-en a vármegyenév olvashatatlan lenne. A csempék `<button>`-ok (szűrők, nem
navigáció), az állapotuk `aria-pressed`, és a képernyőolvasó a **teljes** vármegyenevet és a
valódi állapotot kapja, nem a rövidítést és a gondolatjelet.

### A járműrajz — egy geometria, két felület

A jármű geometriája egyetlen helyen áll (`rajz()` a generátorban), és két helyen jelenik
meg: a **fejlécben** illusztrációként (sötét felület, betöltéskor behajtó jármű), a
**kalkulátorban** élőben (világos kártya, a mezőkhöz kötve). A megjelenést a
`.szip-rajz-hero` / `.szip-rajz-muszer` változatosztály állítja; az osztálynevek és a
koordináták azonosak. Két külön osztálykészlet esetén a két ábra idővel elcsúszott volna
egymástól — pedig épp az a lényeg, hogy a látogató a fejlécben látott ábrát ismerje fel a
kalkulátorban.

**Tónuslépcső egy színből.** A változat egyetlen `--rajz-kontraszt` tokent állít, és a
`.szip-rajz` ebből kever öt tónust (`--rajz-vonal` 55% … `--rajz-halvany` 7%). A rajz így
annyi mélységet kap, mint egy háromtónusú illusztráció, de a paletta egyetlen tokenből
származik, és a témaváltást automatikusan követi. A gradiensek (talajárnyék, talajvonal,
fénypászma, a tartály mélységi árnyéka) `stop-color` CSS-tulajdonságon keresztül kapják a
színüket — ezért ezek is témafüggők.

**A töltésréteg CSS `transform: scaleX()`**, nem SVG `width`: az SVG geometriai
tulajdonságok CSS-ből való állítása nem egyformán támogatott, a `transform` viszont
mindenhol animálódik. A `transform-origin` a tartály bal belső éle (x=150).

**Ellenskálázás.** A járműméret a TARTÁLYRÓL szól, ezért a műszer-változatban a jármű
vízszintesen nyúlik (0,90…1,12 a konfigurált legkisebb és legnagyobb járműméret között), a
**fülke, a hátsó szerelvény és a kerekek viszont visszaskálázzák magukat** a saját
középpontjuk körül. Enélkül a kerék ellipszissé lapult volna. A helyük viszont a szülő
skálázásával mozdul, tehát a hátsó tengely valóban hátrébb kerül a hosszabb kocsin.

**Szintbeosztás.** A tartály tetején köbméterenként egy vonalka fut. A műszer-változatban
ezt a JS rajzolja, mert a számuk a megadott űrtartalomtól függ (egy 4 m³-es kocsin négy
osztás, egy 11 m³-esen tizenegy); a fejléc ábráján állandó, nyolcosztásos skála áll, mert
ott illusztráció, nem mérés. Ettől lesz a rajz mérőeszköz — és ettől látszik a
járműméret-választás is, ami korábban jogos kifogás volt: „csak a rajzon nem változik
semmi."

**A jelölővonal két rétegű.** Egyetlen szaggatott vonal az egyik oldalon mindig elveszett:
sötéten az arany töltésen, világosan a halvány üres részen. Most alul tömör vonal fut a
felület színével, fölötte a sötét szaggatott — a szaggatás réseiben így a felület villan ki,
és a jelölés mindkét zónában olvasható. A korong helyett **lefelé mutató gombostűfej** áll a
vonal tetején: az megmondja, melyik pontra vonatkozik a felirat. A műszer jelölője a saját
értékét is kiírja (`5 m³`), és **eltűnik, ha a foglalt mennyiség nulla** — ott a vonal a
tartály bal szélén állna, és nem jelölne semmit.

**Amit a rajz megtanult menet közben.** Négy hiba, ami nagyításban derült ki:
a sárvédő íve a tartály alsó éle FÖLÉ nyúlt és keresztbe vágta (a csúcs 187 → 204); az
alváz a burkolat tónusát viselte, ezért a jármű különálló darabokra esett (saját,
erősebb `--rajz-arny` tónus); a tartály alsó árnyéka tömör sáv volt, és éles vízszintes
vonalat húzott a tartály közepén, ami folyadékszintnek látszott (gradiens lett belőle);
a búvónyílás középen állt, és pont a „KIFIZETI" felirat alá esett (a tartály elejére
került). A feliratok azóta `paint-order: stroke fill` halót viselnek a felület színével,
tehát bármi fölé kerülhetnek.

A doboz felülete `--szip-panel-bg`, a tartály ürege `--surface-sunken`. Ha a kettő ugyanaz
volna, a tartály üres része beleolvadna a háttérbe, és az ábra fő állítása — a „meddig van
tele" — eltűnne.

### A jármű blokkja — a választó és az ábra egy egység

A járműméret-választó és a rajz **egy `fieldset`-ben** él, teljes szélességben a
mezőrács alatt. Külön állva a kettő nem beszélt egymással: a látogató átállította a
méretet, és nem látta, mit csinál. A blokk bal oldalán a rajz, jobb oldalán az űrtartalom
mezője, a gyorsválasztók és a három leolvasás (elszállított · kiszámlázott ·
tartálykihasználás).

**A tartálykihasználás** azért került ide, mert ez az egyetlen szám, amit a járműméret
önmagában mozgat — a díjat a foglalt mennyiség és az ürítési díj adja. A blokk lábjegyzete
ezt ki is mondja: a járműméret két helyen számít, a „teljes kocsit számláznak" esetben és a
fajlagos díjon keresztül.

### Mezőcsoport-cím pirulában — `.szip-csoport-cim`

A `fieldset` felirata pirula: a két vége félkör, és a doboz kerete a pirula
**tengelyvonalában** fut bele a két oldalába. A natív `legend` keretkivágása ezt nem tudja:
a böngésző a felirat teljes dobozának szélességében szedi ki a vonalat, a vonal vége pedig
a doboz TETEJÉNÉL marad — ott, ahol a pirula íve még nem is kezdődik, tehát a keret nem a
körívbe futna bele, hanem a semmibe. A felirat ezért abszolút pozíciójú, a keretre középre
igazítva (`translateY(-50%)`), és a saját, átlátszatlan háttere takarja el mögötte a
vonalat. A `fieldset` címkézését ez nem érinti: a hozzáférhetőségi fa az első `legend`
gyereket veszi, a pozicionálástól függetlenül.

### A fejléc animációja — öt fázis, egy rajzból

| idő | mi történik |
|---|---|
| 0 ms | a jármű balról behúz; a kerekek és a tömlődob forognak, mögötte sebességvonalak húznak el |
| 620 ms | a **kiszámlázott** mennyiség felfut (arany) |
| 800 ms | az **elszállított** mennyiség felfut (zöld) — a két érték külön ütemben indul, hogy a különbségük külön is látszódjon |
| 1900 ms | a zöld réteg hármat **lötyög**, csillapodva: ettől lesz folyadék, nem sáv |
| 1500 ms | a két jelölő vonala lefut, majd a felirat megjelenik |
| 2200 ms-től | 7 másodpercenként fénypászma fut végig a tartályon — a hurok 18%-ában, a többi szünet |

A lötyögés és a feltöltés **ugyanazon a tulajdonságon** két animáció; a második akkor
indul, amikor az első befejeződött (`animation-fill-mode: both`). Csökkentett mozgás
mellett mindegyik elmarad, és a rajz a végállapotában áll — a `@keyframes` végállapota
ezért pontosan a statikus `transform` értéke.

### `@property --szip-arany` — miért kell regisztrálni

A költségsáv szeletei `flex-grow: var(--szip-arany)`. Regisztráció nélkül a böngésző a
custom property változását ugrásként dolgozza fel, és a szeletek átpattannak az új arányra
ahelyett, hogy átúsznának. A `@property` deklaráció `<number>` szintaxissal ezt oldja meg.

### A figyelmeztetés adatblokk, nem bekezdés

A modul legfontosabb állítása („fizet olyan mennyiségért, amit nem visznek el") korábban
egyetlen bekezdés volt **négy számmal** a mondat belsejében — olvashatatlan. Most cím +
négy adatcella: ki nem szállított mennyiség · alkalmankénti · éves · fajlagos díj teltebb
tartállyal. A számok így ránézésre összevethetők.

### Egyetlen, késleltetett élő régió

A látható számokon **nincs `aria-live`**. Gépelés közben minden leütésnél újra felolvasnák
magukat, és a felület használhatatlan lenne képernyőolvasóval. Helyettük egy
képernyőolvasónak szánt rejtett `role="status"` régió mondja el az eredményt, **900 ms-mal
az utolsó változás után**, egyetlen mondatban.

### `[hidden]` és `.btn`

A `.btn` `display:inline-flex`-e erősebb, mint a `[hidden]` alapértelmezett `display:none`-ja.
A modulon belül ezért külön szabály kell (`.szip-modul .btn[hidden]{display:none}`) —
enélkül a rejtett „Az ismert díjak betöltése" gomb látszott.

### `subgrid` a mezősorokban

A kétsoros címke lelökte a szomszéd oszlop mezőjét egy sorral, és a mezősor lépcsőzött.
A `.szip-mezosor` ezért három sorra (címke · mező · súgó) van osztva, és a mezők
`grid-template-rows: subgrid`-del ülnek rá. Ahol nincs támogatás, a régi — lépcsős, de
működő — elrendezés marad (`@supports`).

---

## 21. ⚠️ Jelzett eltérés — rajzolt modul-hero, `.szip-hero`

A webhely 116 aloldala **fényképes** fejlécet visel (`.page-hero`). A szippantási
kalkulátor nem. Két oka van, és mindkettő a designrendszerből következik:

1. **A rendelkezésre álló felvétel hibás.** A `hero-szippantas.webp` a 4.4-ben leírt
   **függőleges varrattal** készült: a bal harmad határán fókusz- és expozícióváltás
   látszik. 1440px-en ez szembeszökő.
2. **A lap eszköz, nem tartalom.** A fejléc feladata itt nem a hangulat, hanem az, hogy a
   látogató a görgetés előtt megértse a lap gondolatmenetét: van egy tartály, van amennyit
   elvisznek, és van amennyit kiszámláznak.

A fejléc ezért sötét felület (`--surface-inverse`), rajta ugyanaz a tartályábra, amit a
kalkulátor is használ, plusz a három díjtétel chipként. Az `og:image` **marad** a
felvétel — a megosztási kártyához kell egy fotó, és ott a kivágás miatt a varrat nem
látszik.

Következmény a teljesítményre: **nincs fejléckép, tehát nincs mit előre tölteni**. Az
LCP-elem a főcím, a `<link rel="preload" as="image">` ezért lekerült a lapról.

A sötét felület miatt a szöveg a sötét felületre szánt szerepszíneket kapja
(`--text-on-dark`, `--panel-dark-link`), a Fern eyebrow kontrasztja Forest alapon
**4,9:1** — normál szövegre is megfelel.

**Ha később készül varratmentes felvétel erre a témára**, a döntés újranyitható: a
`.szip-hero` cserélhető `.page-hero`-ra a generátorban, de akkor a fejléc elveszíti a
magyarázó szerepét. A kettő együtt is elképzelhető (fotó + alatta az ábra).

---

## 22. Teljes szélességű jelenet magyarázókártyákkal — `.mukodes-jelenet`

A főoldal 7. szekciója (*Az A.B. Clear működése*) egy olyan elrendezést kért, ami a
rendszerben nem szerepelt: a metszetkép nem illusztráció a szöveg mellett, hanem a
szekció **színpada** — a kártyák rajta állnak.

### Miért nem `.panel-media` vagy `.card-media`

Mindkét meglévő médiakeret a konténeren BELÜL él, és `object-fit: contain`-nel a képet
egy megadott arányú dobozba illeszti. A metszet viszont a föld alatti térről szól: ha
körülötte keret van, a talaj véget ér a keretnél, és a kép ábrává degradálódik. A
jelenet ezért az egyetlen blokk a lapon, amelyik kilóg a `--container-max`-ból, és a
képernyő két széléig ér.

### A kártyák nem abszolút pozíciójúak

Kézenfekvő volna `position:absolute`-tal a képre tenni őket, de akkor a kártya
magassága nem hat vissza a sávra: hosszabb szövegnél a kártya a berendezésre csúszna,
vagy kilógna a képből. Helyette a jeleneten **három oszlopos rács** ül
(kártya · szabad sáv · kártya), és a berendezés helyét a KÖZÉPSŐ oszlop tartja fenn:

```css
grid-template-columns:minmax(0,1fr) 30vw minmax(0,1fr);
```

A középső sáv **`vw`-ben van, nem `rem`-ben**. A metszet a KÉPERNYŐ szélességével
skálázódik (teljes szélességű sáv), a konténer viszont 1440px-nél megáll — rögzített
rem-mel a tartály 1440 fölött kinőtt volna a szabad sávból, és a kártyák belelógtak
volna a csövekbe.

A 30vw nem becslés. A metszeten mérve (canvas-olvasás az 1672px-es képen, soronként
a fény–sötét váltás keresésével):

| Mit | A kép szélességének |
|---|---|
| a tartály teste | 17,7% |
| a csővezetésekkel | 21,9% |
| a betonalappal — a legszélesebb pont | 26,1% |

A 30vw tehát a legszélesebb pont mellett is hagy ~2vw levegőt, és minden maradékot a
kártyáknak ad. A rács `--container-wide` (1440px) szélességű, nem `--container-max`
(1280px): a 160px-es különbség mind a kártyáké.

### A kártya törzsszövege 14px, és ez nem esztétikai döntés

A kártya magasságának **korlátja van**: ha magasabb, mint a sáv, kitakarja a
metszet fölső harmadát — ott áll a ház és a fűvonal, ami a jelenetet értelmezi
(*ez a föld alatt van, az meg fölötte*). Ugyanaz a négy lépés:

| Fok | A bal kártya a sáv %-ában | Mi látszik |
|---|---|---|
| `.type-ui-body` 16px | 87% | a ház teljesen takarva |
| `.type-ui-subtitle` 14px | ~60% | ház és fűvonal szabadon |
| `.type-ui-caption` 12px | ~50% | szabadon, de a szöveg apró |

A 12px olvashatatlanul kicsi volt, ezért a helyet **nem a betűméret adja, hanem a
kártya szélessége** (a szabad sáv 30vw-re szűkült). A kártyacím és a
„Kezelés 3 lépésben" felirat marad 16px, tehát a hierarchia megvan.

A negyedik forrás ugyanehhez: **a lépések között nincs térköz** (`gap:0`). A négy
lépés egyetlen összefüggő leírás, a tagolást a félkövér lépéscím adja, nem az üres
sáv — így a kártya további ~48px-kel alacsonyabb, és a sáv 63%-ánál nem nagyobb.

### A sáv magassága — arány alulról, korlát fölülről

```css
--jelenet-min-h:min(
  calc(100vw * var(--jelenet-arany-h) / var(--jelenet-arany-w)),
  var(--jelenet-max-h)
);
```

`min-height`, nem `aspect-ratio`: az arány csak az ALSÓ határt adja. Ha a kártyák
magasabbak (kisebb asztali szélesség, hosszabb szöveg), a sáv nő velük. Az
`aspect-ratio` ezt nem tudja: ott a tartalom kilógna a sávból.

### A kép NEM `object-fit: cover`

Ez a rész két menetben állt be, és az első megoldás rossz volt. `cover`-rel a sáv
növekedésekor a kép **oldalt vág** — és pont ott két dolog van, ami nem nélkülözhető:

1. a **ház** a bal szélen: ő mondja meg, hogy a metszet a felszín ALATT van;
2. a **berendezés**, ami a vágással együtt nagyobbra is skálázódik, tehát belelóg
   a kártyák sávjába — épp azt a szabad középső oszlopot töri el, amit a rács
   fenntart neki.

Helyette a kép mindig teljes szélességben, a saját arányában áll, a sáv aljához
horgonyozva:

```css
.mukodes-jelenet-kep{position:absolute;left:0;right:0;bottom:0;width:100%;height:auto}
```

Ami fölötte marad, az a lap alapszíne — és a kép teteje amúgy is **átlátszó égbolt**,
tehát a kettő varrat nélkül folytatódik. A sáv `overflow:hidden`-t kap: a felső
korlátnál (8 × `--space-128` = 1024px) a kép a TETEJÉBŐL veszít, ahol égbolt van.

### Fénykép fölött árnyék marad sötét témában is

A designrendszer 3. pontja szerint sötét témában a mélységet a felület-lépcső viszi, nem
az árnyék — ezért `--card-shadow: none` a sötét blokkban. **Fotó fölött viszont nincs
felület-lépcső**, amihez a kártya viszonyulhatna: a `--jelenet-kartya-shadow` ezért
mindkét témában `--shadow-2`. Ez az egyetlen helye.

### 1024px alatt a fedés megszűnik

Tableten és mobilon a kártya eltakarná a tartályt, ezért a kép statikus lesz (teljes
szélességű sáv, saját arányában), a kártyák pedig ALÁ kerülnek, normál rácsban. A két
iszapzsákos felvétel viszont **mobilon is egymás mellett marad**: egymás alá téve
hasábszélességűre nőnének, és a kártya tényállításai a képek alá görögnének.

### A két felvétel elválasztó vonala nem a képen van

Első nekifutásra a vonal a második kép `border-left`-je volt, `padding-left`-tel.
A globális `box-sizing:border-box` miatt viszont a `width:100%` a keretet és a
belső térközt is magába foglalta: a jobb oldali kép TARTALMA 17px-kel keskenyebb
lett, és láthatóan kisebbnek tűnt a bal oldalinál — pedig a két render azonos
léptékű (mindkettőn 942px a legnagyobb átmérő a 960px-es vásznon). A vonal ezért
a rács `::before` pszeudoeleme, `left:50%`-on: nem vesz el a képek szélességéből.

Feliratot a két kép **nem kap**. Egyrészt a vizuális terven sincs, másrészt a
hosszabb felirat két sorba tört, és `align-items:end` mellett a saját képét
feljebb tolta — ez volt a másik oka annak, hogy a két kép nem tűnt egyformának.

---

## 22/a. Öt oszlopos helyzetrács — `.situation-grid[data-cols="5"]`

Az „Amit a működésről érdemes tudni" öt tétele a 3. szekció helyzetoszlopainak rácsán ül
(`.situation` — felül vonal, jelvény, cím, szöveg), csak a jelvény itt nem ikon, hanem
sorszám (`.card-badge` + `.type-data-value`), ahogy a `.numbered-grid`-ben.

Az öt oszlop hasábja ~210px: **rövid, pásztázható tényekre való, folyó szövegre nem.**
Tableten 3 oszlop (3+2), mert a közös `[data-cols]` szabály kettesére törése itt
2+2+1-et adna, és az ötödik tétel árván maradna.

### A sorszám a vonalon ül, nem alatta

A `.situation` alapból vonalat húz a hasáb fölé, majd `--space-32` térközzel kezdi a
tartalmat. Így a vonal és a korong **két külön jelnek** látszott, közöttük üres sávval.
A korongot a fél magasságával feljebb húzva (`margin-top:calc(var(--badge-size) / -2)`,
mellette `padding-top:0`) a vonal a korong KÖZEPÉN fut át, és mivel a korong felülete
átlátszatlan, a vonal első 48px-e eltűnik mögötte: a vonal a korongból indul ki.

Ebből két további szabály következik:

- a rács `margin-top:var(--space-24)`-et kap, mert a korong fele a rács fölé lóg —
  enélkül a szekciófejléc alatti köz a felére csökkent volna;
- a `row-gap` `--space-64`, nem `--space-32`: többsoros nézetben a második sor korongja
  ugyanígy a sorközbe lóg.

A sorszám mérete `--type-ui-body-size` (16px): a `.type-data-value` 12px-e a 48px-es
korongon elveszett. A mono rajzolatot és a súlyt továbbra is a `.type-data-value` adja.

---

## 22/b. Három állapotú feltétel-lista — `.mukodes-feltetel`

A telepíthetőség nem igen/nem kérdés, hanem három állapot: *telepíthető* ·
*telepíthető plusz műszaki megoldással* · *kizáró ok lehet*. A `.fit-list`
(`.fit-yes` / `.fit-no`) ezért nem elég — az kettőt ismer.

Mindhárom állapot bal oldali 2px-es vonalat kap, a szemantikus státuszszínekből
(`--primary` · `--warning-border` · `--danger-border`), saját komponens-tokenen
keresztül, a sötét témában újradeklarálva (a `--danger-border` ott más érték). **A szín
nem hordoz önálló jelentést**: mindhárom tételnek van kimondott címe.

A lista `<dl>`, mert az állapot és a magyarázata név–érték pár. A `.panel` alap
`align-items:center`-e itt `start`-ra vált (`.panel:has(> .mukodes-feltetelek)`):
a jobb hasáb jóval magasabb a bal oldalinál, és a középre igazítás a felső vonalat
rontotta el.


---

## 22/c. „Kezelés 3 lépésben" — ikonos sorok, `.mukodes-kezeles`

Ikon + egy mondat, három sorban. Az ikon **dekoratív** (`aria-hidden`): a jelentést a
mellette álló mondat hordozza, ahogy a designrendszer 8. fejezete előírja.

A jelvény **lekerekített négyzet**, nem kör. Ezen a lapon a lime korong már foglalt: az
a SORSZÁMOT jelenti (`.card-badge`, 01–05 és a lépéssor számai). Két jel nem jelentheti
ugyanazt a felületen.

### Három új rajzolat, ideiglenes jelöléssel

`ui-iszap-kosar.svg` (nyitott, perforált láda a peremén fogantyúval) ·
`ui-iszap-zsak.svg` (összekötött nyakú, öblös zsák) ·
`ui-iszap-komposzt.svg` (talajvonalból kihajtó levélpár).

Mindhárom a meglévő ikonkészlet nyelvén beszél (24×24 viewBox, `stroke-width:1.8`,
kerek végződés, `currentColor`), és mindhárom fájl fejlécében ott a jelölés, hogy
**ügyféleszköz érkezésekor cserélendő** — ahogy a designrendszer az ikonoknál előírja.

---

## 23. AI megoldás-ajánló — `.ajanlo-*`

A főoldal 6. szekciója, a webhely **első interaktív eleme**. Forrás:
`OkoTech-Home_AI-modul_fejlesztoi_specifikacio.2.docx` (2026-08-24).

### Két felület, két szerep

| Oldal | Mit csinál |
|---|---|
| **bal — asszisztens** (`.ajanlo-asszisztens`) | egyszerre EGY kérdés, alatta a válasz azonnali magyarázata, és halványan a következő kérdés |
| **jobb — állapotpanel** (`.ajanlo-panel`) | ugyanaz a folyamat összegezve: a hat szakasz állapota, az addig kirajzolódó irány, a kivitelezési feltételek és a tisztázandók |

A panel az `aria-live="polite"` régió, nem a kérdéssor. A kérdéssorban a fókusz
amúgy is mozog, tehát a képernyőolvasó felolvassa — ha a panel is „élne”
ugyanarra, minden válasz kétszer hangzana el.

### A sín — miért nem százalék

A haladást hat korong mutatja, a köztük futó vonal a jelenlegi szakaszig zöld.
Kézenfekvő volna JS-ből egy `--halad: 62%` értéket beállítani, csakhogy az
**inline `style` attribútumot** hozna létre, amit a designrendszer tilt.

Helyette minden szakasz egy `flex` sáv: a korong a tetején, alatta a vonal
(`::after`), és a vonal színe a korong `data-allapot` értékéből jön. A zöld így
pontosan az aktuális korongig ér, számolás nélkül.

`align-self:start`: a sín a saját magasságát veszi fel, nem a kártyáét — nyújtva
a hat korong a záró képernyőn (ami jóval magasabb) szétesett volna.

### Válaszgombok — natív rádiógombok

A válaszok `<fieldset>`/`<legend>` és rejtett `<input type="radio">` +
`<label>` párok, nem `<button>`-ök `aria-pressed`-del. Ezzel a nyíllal
léptetés, a csoportosítás és a felolvasás a platformtól jön, nem ARIA-toldásból.
A kiválasztást `:has(input:checked)` festi, és a jelzés nem csak szín: a
korongba pipa kerül (ugyanaz a két elforgatott keret, mint a `.fit-yes`-nél).

### 23/a. Csendes gomb — `.btn-halvany`

A „Vissza” nem lehet hangosabb a főműveletnél. A rendszerben eddig három
gombváltozat élt (`primary` · `secondary` · `inverse`), és mindhárom KITÖLTÖTT
— a `.btn-inverse` (Forest) világos kártyán vizuálisan erősebb, mint a Fern
elsődleges gomb, tehát megfordítja a hierarchiát. A `.btn-halvany` felülete
`--surface`, kerete `--border-strong`, szövege `--text-primary`.

> A `konzultacio` varázsló „Vissza” gombja jelenleg `.btn-inverse`. Ugyanez a
> megfontolás ott is áll — cserélhető, de az külön változtatás.

### 23/b. Kiemelő szín — miért nem `--secondary`

A cím kiemelt szava, a „Kész” jelzés és a jelvények színe egyetlen tokenből
jön (`--ajanlo-kiemel`), mert a két témán MÁS szín kell:

| Téma | Sáv | Olive Leaf | Fern | Használt |
|---|---|---|---|---|
| világos | Drizzle | **5,6:1** | 2,6:1 | Olive Leaf |
| sötét | Forest | 2,2:1 | **4,9:1** | Fern |

Közvetlen `var(--secondary)` hivatkozással a sötét téma 2,2:1-en állt volna —
az AA alatt. A `--secondary` a sötét blokkban nincs újradeklarálva, tehát a
komponensnek kell saját tokent hoznia.

### 23/c. Rajzolatok — vonalas és kitöltött

A modul inline SVG-vel dolgozik (mint a 18. fejezet AIDT-modulja), nem
CSS-maszkkal: a felületet JS építi, és a maszkhoz minden rajzolatnak külön
fájl és külön osztály kellene. A készlet fele **kontúros**, fele **kitöltött**;
a kettő nem jeleníthető meg ugyanazzal a `fill`/`stroke` beállítással — a
kontúros rajzolat kitöltve fekete folttá válik.

A besorolás egy helyen él (`VONALAS` halmaz az `ajanlo.js`-ben), és a
`svg()` segédfüggvény teszi rá a `.ajanlo-jel-vonal` osztályt. A CSS-ben ez
`svg.ajanlo-jel-vonal` (elem + osztály), hogy a jelvények egyosztályos
`fill:currentColor` szabályait felülírja.

### A szakmai tartalom nincs a kódban

Kérdés, válasz, magyarázat, döntési szabály, terméknév, kimeneti szöveg — mind
az `assets/data/ajanlo-konfig.js`-ben él, amit a cég fejlesztő nélkül
szerkeszthet. Az `ajanlo.js` csak kiértékel és kirajzol. A konfig fejlécében ott
van, mi vár még jóváhagyásra (a specifikáció 8. pontja).

---

## 23/d. Az ÜGYAZONOSÍTÓ — egy kód, két modul, nulla személyes adat

A látogató két AI-modulon mehet végig a főoldalon: a 6. szekció megoldás-ajánlóján
és a 8. szekció ársávbecslőjén. A kettő részben **ugyanazt kérdezi**. Kétszer
megkérdezni ugyanazt nem csak kényelmetlen — azt is jelzi, hogy nem figyeltünk
oda.

Ezt egyetlen dolog oldja meg: **egy ügyazonosító** (`MA-XXXX-XXXX`), ami alatt
mindkét modul kimenete együtt él.

### Amit az azonosító NEM

Nem regisztráció, nem fiók, nem sütialapú követés. Nevet, e-mail-címet,
telefonszámot nem kérünk hozzá, IP-t nem tárolunk mellé — a rekordból nem derül
ki, ki a látogató. **Ezt minden felületen ki is mondjuk**, ahol az azonosító
megjelenik: a 6. szekció mentés-gombja fölött (még kattintás előtt), a mentés
visszajelzésében, a 8. szekció mentés-dobozában és az `/eredmeny` lap fejlécében.
Egy kód önmagában riasztó; egy mondat elveszi az élét.

### A készlet, amiből az azonosító áll

`ABCDEFGHJKLMNPQRSTUVWXYZ23456789` — hiányzik belőle a `0`/`O` és az `1`/`I`.
A kódot **telefonban is be kell tudni mondani**, és papírról leolvasni. 8 karakter,
32 jel: ~1,1e12 lehetőség; a lekérdező végpont ezen felül sebességkorlátos.

### Az átvétel a 8. szekcióban — `ATVETEL`

A modul fölött álló sáv (`.aidt-atvetel`) három állapotot ismer: van munkamenetbeli
adat → felajánlja; nincs → beírható azonosítómező; megtörtént → megmondja, **mit**
vett át. **Sosem tölt be magától**: az átvétel a látogató döntése.

A leképezés két szintet ismer, és a különbség fontos:

| | Mit tesz | Mikor |
|---|---|---|
| `zar: true` | kitöltöttnek jelöli, nem kérdezi újra | a 6. szekció válasza EGYÉRTELMŰEN megfelel az itteni kérdésnek |
| `zar: false` | csak előjelöl, a kérdés aktív marad | a 6. szekció csak RÉSZBEN válaszolta meg |

Jelenleg: **kapacitás** és **használat jellege** zárt átvétel, a **telek adottságai**
csak előjelölés (a 6. szekció a magas talajvízről és a kevés helyről tud, a
lejtésről, a gépi hozzáférésről és a közeli élővízről nem).

**Csak összefüggő előtag vehető át.** A beszélgetés-nézet a `step` előtti kérdéseket
rajzolja megválaszoltként; egy „lyuk" (megválaszolt kérdés a még el nem ért kérdések
között) hibás állapot volna. Ami kilóg, azt inkább újra megkérdezzük.

### A létszám sávjai szándékosan azonosak

A két modul létszám-kérdése ugyanazokat a sávokat használja (1–2 / 3–4 / 5–6 /
7–10 / 10 felett). Enélkül a válasz nem volna átvihető: egy „2–3 fő" sem az „1–2",
sem a „3–4" sávba nem esik egyértelműen, tehát vagy újra kellene kérdezni, vagy
tippelnénk.

> ⚠️ A specifikáció példája „magas létszám (4–5 fő)" — ez a 3–4 és az 5–6 sáv
> határán fekszik. A jelenlegi értelmezés: **magas = 5 főtől**. Ez a határ
> jóváhagyásra vár.

### „Átvéve" jelölés — mert a látogató itt nem kattintott

Az átvett kérdés úgy néz ki, mint egy megválaszolt kérdés. Ezért külön jelölést kap
a beszélgetésben (`.aidt-atvett-badge`) ÉS a helyzetkép-panelen
(`.aidt-step-atvett`): enélkül a látogató nem tudná, miért nem kérdeztük meg, és nem
jutna eszébe, hogy át is írhatja. A panelről szerkesztve az átvétel megszűnik.

### Függőben lévő modul — hogy ne legyen féloldalas az ügy

A látogató végigmehet a megoldás-ajánlón **mentés nélkül**, aztán az ársávbecslőn —
és ott nyomhat mentést. Ilyenkor a 6. szekció kimenete is felkerül ugyanabba az
ügybe (`OthUgy.fuggoben`). A munkamenetben él, tehát a fül bezárásával eltűnik, és
**semmit nem küld el magától**: csak akkor kerül szerverre, ha a látogató ment. A
8. szekció mentés-doboza ilyenkor ki is mondja, hogy a másik eredmény is felkerül.

### A PDF: a nyomtatási nézet MAGA a PDF

Nincs PDF-könyvtár. Az `/eredmeny` lap „Nyomtatás / PDF" gombja a böngésző saját
`window.print()`-jét hívja, a látogató a párbeszédben a „Mentés PDF-ként" célt
választja. Ugyanaz az elv, mint a 11. szekció jelentésénél — és ugyanazért.
Ezért kerül **az azonosító és a teljes cím látható szövegként** a lapra: papíron
és PDF-ben a kattintható link semmit nem ér, a beírható cím viszont igen.

### A rétegek

| Fájl | Mit csinál |
|---|---|
| `assets/js/ugy.js` | KÖZÖS réteg: azonosító, mentés, olvasás, munkamenet-tároló, `oth-ugy-valtozott` esemény |
| `api/eredmeny-mentes.php` | modul-blokk mentése — új ügyet nyit, vagy meglévőt egészít ki |
| `api/eredmeny-olvas.php` | ügy visszaolvasása azonosító alapján |
| `eredmeny.html` + `assets/js/eredmeny-oldal.js` | a mentett ügy lapja, nyomtatható |

Miért külön `ugy.js`: ugyanezt három hívó használja (a két modul és az `/eredmeny`
lap). Ha mindhárom saját `fetch`-et írna, a végpont neve, a hibakezelés és a
tárolókulcs három helyen csúszhatna szét.

**Miért POST a lekérés is:** a közös indítás (`api/lib/indit.php`) minden végpontnál
origin-ellenőrzést végez, ahhoz pedig POST kell. Így a rekordot csak a saját
lapunkról lehet lekérni, és az azonosító nem kerül böngésző-előzménybe vagy
proxynaplóba. Nem létező azonosítóra **ugyanaz a 404** megy, mint lejártra.

### Megőrzés és a CRM

`api/config.php` → `eredmeny.megorzes_nap` (alapérték: 180). A mentés végpontja
alkalomszerűen takarít; a `frissitve` számít, nem a létrehozás — egy folytatott ügy
nem évül el a közepén.

A tároló egy könyvtárnyi JSON-fájl (`api/.eredmenyek/MA-*.json`), ügyenként egy.
A szerkezete (azonosító, létrehozás, frissítés, modulonként verzió + válaszkulcsok
+ emberi olvasat + kimenet) **CRM-be közvetlenül betölthető**. Export-végpont
szándékosan NINCS: az hitelesítést igényelne, és azt külön kell megtervezni.

> ⚠️ **A megőrzési idő három helyen szerepel, és egyeznie kell:** a `config.php`-ban,
> az `ajanlo-konfig.js` `mentes.megorzesSzoveg` mezőjében, és az adatkezelési
> tájékoztatóban. Az utóbbi kiegészítése **élesítés előtti feladat**.

---

## 23/e. Öko helyszíni segítsége — `data-oko-pont`

Egy azonosítómező a semmiből **regisztrációnak néz ki**, pedig épp az ellenkezője.
A statikus magyarázószöveg segít, de csak akkor, ha elolvassák. Öko ezért
**magától megszólal** — nem a lap tetején, hanem akkor, amikor a látogató odaér.

### Hogyan opt-inol egy felület

Bármely elem felveheti a `data-oko-pont="<kulcs>"` attribútumot; a kulcshoz
tartozó szöveg a `kalauz.js` `PONTOK` táblájában él. Jelenleg két pont van:

| Kulcs | Hol | Mit mond |
|---|---|---|
| `ugyazonosito` | a 8. szekció átvételi sávja | „Ez a kód nem regisztráció — segítsek?" |
| `mentes` | a 6. szekció mentés-magyarázata, a 8. szekció mentés-doboza | „Elmagyarázzam, mit ad a mentés?" |

Minden pont **egyszer** szólal meg lapmegtekintésenként, és soha nem szólal meg
annak, aki Ökót bezárta.

### Két viselkedés, a panel állapota szerint

- **Csukott panel** → buborék egy mondattal. Rákattintva megnyílik a panel a
  TELJES magyarázattal és a ponthoz tartozó három kérdéssel.
- **Nyitott panel** (a főoldalon ez a gyakoribb: Öko a hero után magától kinyílik)
  → Öko egyszerűen megszólal a párbeszédben, a magyarázattal és a kérdésekkel.
  Kattintás nélkül, de nem tolakodva: a párbeszédhez hozzáfűz, nem szakít félbe.

### A helyszíni segítség erősebb az általános köszönésnél

A görgetés **mindkettőt** elindítja (a hero-figyelőt és a pont-figyelőt), és az
események sorrendje nem garantált. Ezért a `megerkezik()` nem írhatja felül a
buborékot, ha már van benne pont-üzenet: a konkrét segítség többet ér a
„Segítsek?"-nél. A pont a kulcsát az érkezés ELŐTT teszi ki, hogy ez eldőljön.

### Görgetéspozíció, nem IntersectionObserver — és nem `requestAnimationFrame`

Ugyanaz a megfontolás, mint a hero-nál (13. fejezet): az IO a lap
életciklusától és a megjelenítés ütemezésétől függ. Háttérfülön vagy
visszafogott rendereléskor **sem az IO, sem a `requestAnimationFrame` nem fut le**
— és vele a segítség is elmarad. A `getBoundingClientRect()` viszont mindig
megmondja, hol tart a látogató; időalapú fékezéssel (150 ms) másodpercenként
néhány mérés, ami olcsó.

A modulok felülete JS-ből épül, tehát a pontok később kerülnek a lapra: egy
`MutationObserver` is meghívja az ellenőrzést, nem csak a görgetés.

### Amit az AI is tud

A rendszerprompt (`api/kalauz.php`) külön blokkot kapott az ügyazonosítóról:
mi az, mi NEM, hol adható meg, mi történik, ha elvész, és meddig él. A megőrzési
idő **a konfigurációból** megy a promptba (`$MEGORZES`), nem beírt számként — így
a látogató ugyanazt hallja Ökótól, mint amit a felületen olvas, és egy
átállítás nem hagy hátra elavult számot a prompt közepén.

---

## 24. Ügyfélvélemények — két futó szalag, `.vel-*`

Egy vélemény anekdota. Tizenöt, folyamatosan mozgó vélemény a tapasztalat
**mennyiségét** is mutatja — ezt egy egyesével léptethető idézetdoboz (a korábbi
megoldás) nem tudja, mert egyszerre mindig csak egy állítást enged látni.

### Két szalag, ellentétes irányban

A felső sor balra, az alsó jobbra fut, eltérő időtartammal (110 s és 132 s). Az
ellentétes irány azt oldja meg, hogy a szem ne kapaszkodjon bele egyetlen
sodrásba; az eltérő idő azt, hogy a két sor kártyái ne álljanak össze ismétlődő
mintázattá.

### A varrat: `-50%` nem elég

A lista meg van kettőzve, a második példány `aria-hidden="true"` — képernyőolvasónak
**minden vélemény egyszer hangzik el**. A visszacsatolás akkor észrevehetetlen, ha a
szalag pontosan a második példány elejéig tolódik el. Ez **nem** `-50%`: a fél
szalagszélesség a két példány KÖZÉ eső térköz felénél megáll, és minden körnél
fél térköznyit ugrik a sor. Ezért `calc(-50% - var(--space-24) / 2)`, tokenben
`--vel-varrat`. Mérve mindkét soron 0 px eltérés.

### A kártya a sablonkártyát követi

Ugyanaz a felület, keret, sarok, árnyék és belső tér (`--card-bg`, `--card-border`,
`--card-radius`, `--card-shadow`, `--card-padding`), csak rögzített szélességgel,
mert szalagban áll. Felül a **témacímke** akcentusszínnel — ez mondja meg, mire
vonatkozik a vélemény, enélkül tizenöt dicséret egyetlen masszává olvad. Az idézet
körül valódi magyar idézőjelpár, a szöveg fokán: a korábbi nagy, halvány Zilla
Slab jel elgépelésnek látszott. Legalul hajszálvonal fölött a név és a település.

### Minden kártya egyforma magas

`min-height: var(--vel-kartya-mag)` — és ez nem csak a soron belüli kártyákat
egyenlíti ki (azt a flex `stretch` amúgy is megtenné), hanem **a két sort is egy
magasságra hozza**. Mért maximumok a leghosszabb idézettel: 23rem
kártyaszélességnél 330px, keskeny nézetben 18rem-nél 402px; a token ennél
bőkezűbb (22rem / 26rem). `min-height` és nem `height`: ha a betűtípus betöltése
mégis túlcsordítaná, a sor egyenletesen nő, szöveg nem vágódik le.

Az idézet a **szabad tér közepén áll** (`margin-block:auto`), az aláírás a kártya
alján marad. Enélkül a rövid vélemények alatt tenyérnyi folt gyűlt össze egyetlen
lyukként — így a hely a szöveg fölött és alatt oszlik el, és belső térköznek
látszik, nem hiánynak.

> Kipróbálva és **elvetve**: a rövid idézetek display betűs, 28px-es
> kiemelt-idézet változata. Papíron szerkesztőségi ritmust ad; a szalagban a
> 16px-es szomszédok mellett hangoskodásnak látszott, nem szándéknak.

### A kártyák sorrendje kézzel áll

Két szomszédos kártya nem viselheti ugyanazt a témacímkét — **a varraton át sem**
(utolsó ↔ első). A forrásdokumentum sorrendjében három „A cég ott volt utána is"
állt egymás mellett. A sorrend a HTML-ben rögzített, a másolt példányé azonos.

### Megállítás — és amit vállalunk

`:hover` és `:focus-within`, a `.vel-fal` egészén: aki az egyik sorba beleolvas,
annak a másik se szaladjon el alatta. Szüneteltető **gomb nincs** — megrendelői
döntés.

> ⚠️ Ezzel a szekció **nem teljesíti a WCAG 2.2 SC 2.2.2** pontját. Az öt
> másodpercnél hosszabban magától mozgó tartalmat meg kell tudni állítani, és
> érintőképernyőn nincs hover, a fókusz sem feltétlenül jut a szalagra. A
> `prefers-reduced-motion` sem számít teljesítési módnak. Ha az EAA-megfelelés
> előkerül, a legolcsóbb javítás nem a gomb visszatétele, hanem egy lapszintű
> „mozgás csökkentése" kapcsoló a fejlécben — az egy helyen, a lap minden
> animációjára megoldja.

`prefers-reduced-motion` mellett a szalag nem fut, hanem **tördelt ráccsá válik**
— ugyanaz a tartalom, mozgás nélkül. Nem vízszintes görgetéssé: azt egérrel
nehéz kezelni. A megkettőzött példány itt elrejtve.

### Nincs hozzá szkript

A mozgást, a megállítást, a rendezést és a széli elhalványulást (`mask-image`) is
a CSS viszi. A korábbi `velemeny.js` a gombbal együtt törölve.
