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
