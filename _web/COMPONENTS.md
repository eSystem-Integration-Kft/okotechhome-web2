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

## 12. Amire még nincs megoldás

- **Képaláírás** és `--media-tint` — a kép- és illusztrációs rendszer hiányzó része
- **Ikon-méretskála és vonalvastagság** — jelenleg egyetlen `--icon-size` szerep él
- **Sötét témájú `.alert`** — a státusz-tokenek nem témafüggők (designrendszer 10.)
- **Szekció-sáv váltakozás:** az 5.3 elv szerint a sávoknak váltakozniuk kell
  (`canvas → surface-muted → sötét`). A 3. és 4. szekció a vizuális terv szerint **egyaránt
  canvas** sávon ül. A `.section-alt` osztály készen áll; a ritmust a teljes oldal
  összeállásakor kell eldönteni.
