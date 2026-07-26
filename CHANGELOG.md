<p align="center">
  <img src="./.github/banner.png" alt="ÖkoTech Home — otthoni biológiai szennyvíztisztítás" width="100%">
</p>

<h1 align="center">Változásnapló — okotechhome-web2 <em>(Test2)</em></h1>

<p align="center">
  <img src="https://img.shields.io/badge/verzi%C3%B3-0.01.01-36C5E6?style=flat-square" alt="verzió 0.01.01">
  <img src="https://img.shields.io/badge/Keep%20a%20Changelog-1.1.0-C9A24A?style=flat-square" alt="Keep a Changelog 1.1.0">
  <img src="https://img.shields.io/badge/SemVer-2.0.0%20(padded)-1572B6?style=flat-square" alt="SemVer 2.0.0 padded">
  <img src="https://img.shields.io/badge/kiad%C3%A1sok-1-6f42c1?style=flat-square" alt="1 kiadás">
</p>

---

A napló formátuma a [Keep a Changelog 1.1.0](https://keepachangelog.com/hu/1.1.0/) ajánlást követi,
a verziószámozás a [Szemantikus Verziózás 2.0.0](https://semver.org/lang/hu/) szabályait —
**feltöltött írásmóddal** (`MINOR` és `PATCH` két számjegyen). A projektre szabott értelmezést
lásd: [`VERSIONING.md`](./VERSIONING.md).

**Hatókör:** ez a napló az `okotechhome-web2` repó (Test2 munkaterület) teljes történetét fedi le
az inicializálástól kezdve, **tételesen, commitonként**. A Test1 (`okotechhome-web`) története
külön naplóban él, és a két verzió-idővonal **független**.

**Kategóriák:** `Hozzáadva` · `Módosítva` · `Javítva` · `Eltávolítva` · `Elavult` · `Biztonság`

**Jelölések:** `§` = a főoldal szekciója · `OFC` = AI ajánlat-összehasonlító (offer comparison) ·
`AIDT` = AI döntéstámogató · a `( )` zárójelben álló hét karakteres kód a commit rövid hash-e.

---

## [Kiadatlan]

Az első két tartalmi szekció és a hozzájuk tartozó designrendszer-implementáció.
Kiadásra kész — `./scripts/release.sh 0.02.00` (előtte ezt a szekciót át kell nevezni
`## [0.02.00] — ÉÉÉÉ-HH-NN` alakra).

### Hozzáadva

- **`assets/css/app.css`** — a designrendszer (`OTH-design-system-Teszt.v2` v0.5)
  implementációja `@layer` architektúrában: `reset → tokens → base → typography →
  components → responsive → motion`. A tokenblokk szó szerint az élő HTML-referenciából,
  a `.type-*` szereposztályok, a `.btn` és a `.text-link` változatlanul.
- **`index.html` — 3. szekció (*Kiinduló helyzet*)**: négy helyzetkártya kivágott
  illusztrációval, alattuk kiemelt panel a nagyobb kapacitású (50 fő feletti) igényekhez,
  a szekció egyetlen elsődleges CTA-jával.
- **`index.html` — 4. szekció (*Technológiák*)**: három sorszámozott magyarázókártya,
  „Gyors összehasonlítás" táblázat ikonos oszlopfejlécekkel, és a saját berendezések
  (Epureco oldómedence, A.B. Clear) blokkja.
- **Új komponensek** — a designrendszer 10. fejezete szerint még definiálatlan elemek
  dokumentált osztályként, kizárólag meglévő tokenekből: szekció-sáv, kártya, médiakeret,
  kiemelt panel, sorszámjelvény, ikon, összehasonlító táblázat, termékkártya,
  kétoszlopos szekcióalj. Indoklás és javasolt szabályzatszöveg: **`_web/COMPONENTS.md`**.
- **`.htaccess`** — kiterjesztés nélküli (clean) URL-ek: `/valami.html` → 301 `/valami`,
  `/index.html` → 301 `/`, záró perjel eltávolítása; biztonsági fejlécek (CSP, nosniff,
  X-Frame-Options, Referrer-Policy, Permissions-Policy), tömörítés és cache.
- **`serve.py`** — lokális preview szerver, amely a `.htaccess` clean-URL viselkedését
  emulálja. Enélkül a kiterjesztés nélküli linkek helyben 404-et adnának.
- **Médiaeszközök** — öt kivágott illusztráció és két termékfotó WebP-ben
  (`assets/img/`), három technológiai ikon (`assets/icon/`).

### Javítva

- **Médiakeret magassága** — a `.card-media` egyszerre flex-konténer és flex-elem, így az
  alapértelmezett `min-height:auto` a *kép* belső méretéből számolt, és felülírta az
  `aspect-ratio`-t. A hiba csak akkor jelentkezett, ha a kép saját aránya magasabb volt a
  szereptokenben megadottnál — ezért asztali nézetben rejtve maradt, és mobilon jött elő
  (460×306 a várt 460×259 helyett). Javítás: `min-height:0`.
- **Ikonok beégetett színe** — a kapott CorelDRAW-SVG-k `fill:#21432B` nyers hexet
  hordoztak, ami a 9. tiltólistába ütközik és sötét témában olvashatatlan lenne.
  A `fill` `currentColor`-ra cserélve, a színt CSS-maszk adja.
- **Táblázat túlcsordulása** — a négyoszlopos összehasonlító tábla 46px-szel kilógott a
  szekcióalj felén. A cellák vízszintes belső térköze `--space-16` → `--space-8`.

### Megjegyzés

- A kártyák **azonos magasságúak** (a rács `stretch` igazítása), a hivatkozás
  `margin-top:auto`-val mindig a kártya alján zár.
- A `_web/` linkjei már **kiterjesztés nélküliek**; a hivatkozott aloldalak
  (`uj-epitkezes`, `emeszto-kivaltasa`, …) még nem léteznek, így helyben 404-et adnak.
- Két, döntést igénylő pont a `COMPONENTS.md`-ben van jelölve: a navigációs CTA
  gombként való megjelenítése (7.6 tábla), és a szekció-sávok váltakozása (5.3 elv).

---

## [0.01.01] — 2026-07-26

A **Test2** repó inicializálása: webkimenet-váz, verziókezelés és dokumentációs réteg.
**Weboldal-kód még nincs** — a `_web/` egyelőre üres váz.

A Test2 azonos márkát, motort, technológiát és logót visz, mint a Test1
(`okotechhome-web`, jelenleg `0.9.0`); az eltérés kizárólag a **designrendszerben** lesz.

### Hozzáadva

- **`_web/`** — a deployolható statikus webkimenet váza (`assets/{css,js,img}`), saját
  `README.md`-vel: célszerkezet, technológiai réteg, helyi kiszolgálás, minőségi kapuk.
- **`README.md`** — HTML-alapú (banner, badge-ek, táblázatok) projektútmutató:
  Test1 ↔ Test2 összevetés, repó-hatókör, verziózás, deploy, nyitott pontok.
- **`CHANGELOG.md`** — ez a napló, Keep a Changelog 1.1.0 formátumban.
- **`VERSIONING.md`** — verziózási szabályzat: a **feltöltött** (`X.YY.ZZ`) verziószám-formátum
  definíciója és indoklása, SemVer-értelmezés statikus marketing-oldalra, Conventional Commits →
  verzióemelés leképezés, ág- és tagkonvenciók, kiadási folyamat, deploy-korreláció,
  visszaállítási (rollback) recept, verzió-életút.
- **`VERSION`** — gépi olvasásra alkalmas, egysoros verzió-forrás (single source of truth): `0.01.01`.
- **`scripts/release.sh`** — kiadás-automatizálás: a feltöltött formátum validációja, numerikus
  (`10#` bázisú, oktális-biztos) verzió-összehasonlítás, `VERSION` frissítés, `CHANGELOG.md`
  szekció-ellenőrzés, annotált tag létrehozása, `--dry-run` móddal.
- **`.gitignore`** — a repó hatókörét kikényszerítő kizárások (lásd alább), valamint titkok,
  rendszerszemét és build-melléktermékek.
- **`.github/banner.png` · `.github/banner.svg`** — README-banner, a Test1 repóból átemelve
  (a márka azonos, a banner nem kerül élesre).

### Repó-hatókör

A távoli repóba **kizárólag a webkimenet és a verziókezelési réteg** kerül. A projekt körüli
belső munkaanyag **szándékosan helyben marad**, és nincs a git-történetben sem:

| Helyi könyvtár | Miért marad ki |
|---|---|
| `_memory/` | belső projektmemória, gépspecifikus — nem a leszállítandó része |
| `_work/` | munkapéldányok, jegyzetek, promptok, nagy médiamentések |
| `_files/` | ügyfél-dokumentumok (ajánlat, stratégia, jogi klauzula) |
| `_OTH_tesztfileok/` | teszt-ajánlatok az OFC modul kipróbálásához |
| `_kepek_videok/` | médiamesterek (434 MB); a git nem bináris-tár |

> Ezek mentése **nem git feladata** — külső meghajtó vagy felhő-tárhely szükséges hozzá.

### Git-történet

- **Friss, tiszta történet.** A könyvtár korábban a Test1 munkaterület másolt `.git`-jét hordozta
  (`de586e6` commit + `v1.0.0` tag, távoli nélkül), ami a Test2 `0.01.01`-es indulásával
  ellentmondásban állt. Az örökölt történet `git bundle`-ként mentve
  (`_work/_backup/okotechhome2-inherited-test1-history.bundle`, helyi), az eredeti pedig
  érintetlenül megvan a `_OkoTechHome/.git`-ben — egyedi adat nem veszett el.
- **Távoli repó bekötve:** `github.com/eSystem-Integration-Kft/okotechhome-web2` (privát),
  fő ág: `main`.
- **Annotált tag:** `v0.01.01`.

---

<p align="center">
  <sub>Ökotech-Home Kft. · fejlesztő: eSystem-Integration Kft. / IEM — Industrial Electric &amp; Mechanic Kft., Érd</sub>
</p>
