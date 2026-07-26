<p align="center">
  <img src="./.github/banner.png" alt="ÖkoTech Home — otthoni biológiai szennyvíztisztítás" width="100%">
</p>

<h1 align="center">okotechhome-web2 — <em>Test2</em> munkaterület</h1>

<p align="center">
  <strong>Ugyanaz a márka, motor és technológia — új designrendszerrel.</strong><br>
  Az <a href="https://okotechhome.hu">Ökotech-Home Kft.</a> döntéstámogató weboldalának
  második, párhuzamos designváltozata.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/verzi%C3%B3-0.01.01-36C5E6?style=flat-square" alt="verzió 0.01.01">
  <img src="https://img.shields.io/badge/v%C3%A1ltozat-Test2-C9A24A?style=flat-square" alt="Test2">
  <img src="https://img.shields.io/badge/st%C3%A1tusz-inicializ%C3%A1lva-6f42c1?style=flat-square" alt="státusz: inicializálva">
  <img src="https://img.shields.io/badge/statikus-HTML%20%2F%20CSS%20%2F%20JS-19C37D?style=flat-square" alt="statikus">
  <img src="https://img.shields.io/badge/SEO%20%2B%20GEO-JSON--LD-6f42c1?style=flat-square" alt="SEO+GEO">
  <img src="https://img.shields.io/badge/A11y-WCAG%202.2%20AA-0A7?style=flat-square" alt="WCAG 2.2 AA">
  <img src="https://img.shields.io/badge/licenc-Proprietary-C9A24A?style=flat-square" alt="Proprietary">
</p>

<p align="center">
  <a href="./CHANGELOG.md">Változásnapló</a> ·
  <a href="./VERSIONING.md">Verziózási szabályzat</a> ·
  <a href="./VERSION">VERSION</a>
</p>

---

## ✨ Mi ez

Ez a repó az **ÖkoTech Home** weboldal **Test2** változatának forráskódja: a telepíthető
webkimenet (`_web/`) és a hozzá tartozó verziókezelési réteg, saját verziószámmal.

> A projekt körüli belső munkaanyag (memória, jegyzetek, ügyfél-dokumentumok, médiamesterek)
> **szándékosan nem része a repónak** — lásd a *Mi nincs git alatt* szakaszt.

<table>
  <tr><td><b>Ügyfél</b></td><td>Ökotech-Home Kft. · Esztergom · 2004 óta · 3800+ telepítés</td></tr>
  <tr><td><b>Fejlesztő</b></td><td>eSystem-Integration Kft. / IEM — Industrial Electric &amp; Mechanic Kft., Érd</td></tr>
  <tr><td><b>Távoli repó</b></td><td><code>github.com/eSystem-Integration-Kft/okotechhome-web2</code> (privát)</td></tr>
  <tr><td><b>Kezdőverzió</b></td><td><code>v0.01.01</code></td></tr>
  <tr><td><b>Nyelv</b></td><td><code>hu-HU</code></td></tr>
</table>

### 🔁 Test1 ↔ Test2

<table>
  <tr>
    <th></th>
    <th>Test1 — <code>okotechhome-web</code></th>
    <th>Test2 — <code>okotechhome-web2</code> <i>(ez)</i></th>
  </tr>
  <tr><td><b>Márka / logó</b></td><td colspan="2" align="center">🟰 <b>azonos</b> — ÖkoTech Home</td></tr>
  <tr><td><b>Motor / technológia</b></td><td colspan="2" align="center">🟰 <b>azonos</b> — statikus HTML/CSS/JS, GSAP + Lenis, Apache <code>.htaccess</code></td></tr>
  <tr><td><b>Tartalmi téma</b></td><td colspan="2" align="center">🟰 <b>azonos</b> — otthoni biológiai szennyvíztisztítás, döntéstámogató tölcsér</td></tr>
  <tr><td><b>Designrendszer</b></td><td>smaragd/aqua tokenkészlet, Sora + Inter</td><td>🆕 <b>új vizuális irány</b> — kidolgozás alatt</td></tr>
  <tr><td><b>Verziószám</b></td><td><code>0.9.0</code> (klasszikus SemVer)</td><td><code>0.01.01</code> (feltöltött SemVer)</td></tr>
  <tr><td><b>Verzió-idővonal</b></td><td colspan="2" align="center">↔️ <b>független</b> — a két repó verziója nem korrelál</td></tr>
</table>

---

## 📁 Könyvtárszerkezet

A repó hatóköre **szándékosan szűk**: a távoli repóba a **webkimenet** és a hozzá tartozó
**dokumentációs / verziókezelési réteg** kerül. A munkakönyvtárak helyben maradnak.

```text
_OkoTechHome2/
│
│  ┌─ ✅ VERZIÓZOTT — github.com/eSystem-Integration-Kft/okotechhome-web2 ─────┐
├─ README.md                  # ez a fájl
├─ CHANGELOG.md               # tételes változásnapló (Keep a Changelog)
├─ VERSIONING.md              # verziózási szabályzat + kiadási folyamat
├─ VERSION                    # 0.01.01 — gépi olvasásra, single source of truth
├─ .gitignore                 # mi marad ki a verziózásból és miért
├─ scripts/release.sh         # kiadás-automatizálás (bump + annotált tag)
├─ .github/banner.*           # README-banner (nem kerül élesre)
├─ _web/                      # 🌐 WEBKIMENET — ez megy élesre
│  ├─ README.md
│  └─ assets/{css,js,img}/
│  └───────────────────────────────────────────────────────────────────────────┘
│
│  ┌─ ❌ HELYI — nem kerül a távoli repóba ────────────────────────────────────┐
├─ _memory/                   # 🧠 projektmemória (MEMORY.md index + tényfájlok)
├─ _work/                     # 🛠️ munkapéldányok, jegyzetek, promptok, kutatás
├─ _files/                    # ügyfél-leszállítandók (ajánlat, stratégia, jogi)
├─ _OTH_tesztfileok/          # teszt-ajánlatok az OFC modul kipróbálásához
└─ _kepek_videok/             # médiamesterek (434 MB) + ASSET-MANIFEST.md
   └──────────────────────────────────────────────────────────────────────────┘
```

### A munkakönyvtárak szerepe

| Könyvtár | Mi kerül bele | Git |
|---|---|---|
| **`_web/`** | a **deployolható** statikus site: HTML, `assets/`, `.htaccess`, `robots.txt`, `sitemap.xml` | ✅ **verziózott** |
| **`_memory/`** | projektmemória: `MEMORY.md` index + fájlonként egy tény (`user` · `feedback` · `project` · `reference`) | ❌ helyi |
| **`_work/`** | munkapéldányok, stratégia-jegyzetek, AI-promptok, kutatás, vázlatok, backupok | ❌ helyi |

---

## 🚫 Mi nincs git alatt (és miért)

| Útvonal | Méret | Ok |
|---|---|---|
| `_memory/` | — | belső projektmemória, gépspecifikus — nem a leszállítandó része |
| `_work/` | 6,2 MB | munkaanyag és nagy médiamentések; a kiforrott eredmény a `_web/`-be kerül |
| `_files/` | 268 KB | ügyfél-dokumentumok (ajánlat, stratégia, jogi klauzula) |
| `_OTH_tesztfileok/` | 996 KB | teszt-ajánlatok az OFC modul kipróbálásához |
| `_kepek_videok/` | 434 MB | videó-/kép-mesterek; a git nem bináris-tár |
| `.DS_Store`, `.env*`, `*.key` | — | rendszerszemét, titkok |

> ⚠️ **Ezek mentése nem git feladata.** Külső meghajtó vagy felhő-tárhely (időbélyeges mappa)
> javasolt — a `_memory/`, `_work/`, `_files/` és `_kepek_videok/` tartalma **csak ezen a gépen
> létezik**. A médiamesterek tételes leltára: `_kepek_videok/ASSET-MANIFEST.md`; ha mégis
> verziózni kell őket, a Git LFS-recept a manifest végén található.

---

## 🏷️ Verziózás

| | |
|---|---|
| **Aktuális verzió** | `0.01.01` — lásd a [`VERSION`](./VERSION) fájlt |
| **Formátum** | `MAJOR.MINOR.PATCH`, a `MINOR` és `PATCH` **két számjegyre feltöltve** (`0.01.01`, `0.02.00`, `0.10.00`) |
| **Változásnapló** | [`CHANGELOG.md`](./CHANGELOG.md) — Keep a Changelog 1.1.0 |
| **Szabályzat** | [`VERSIONING.md`](./VERSIONING.md) — SemVer-értelmezés, kiadási folyamat, rollback |
| **Séma** | [SemVer 2.0.0](https://semver.org/lang/hu/) (feltöltött írásmód) + [Conventional Commits](https://www.conventionalcommits.org/) |

```bash
git tag --sort=-v:refname             # kiadások időrendben
git log v0.01.01..HEAD --oneline      # mi történt az utolsó kiadás óta
git diff v0.01.01..HEAD --stat        # mely fájlok változtak

./scripts/release.sh 0.02.00 --dry-run   # kiadás próbája
./scripts/release.sh 0.02.00             # éles kiadás (VERSION + commit + tag)
```

> `MAJOR` = `0`, amíg az oldal ügyfél-átvétel előtt van. Az **`1.00.00` a go-live elfogadásakor** jön.

---

## 🖥️ Helyi fejlesztés

A webkimenet a `_web/` alatt épül. Amíg nincs saját preview-szerver, egyszerű kiszolgálás:

```bash
cd _web
python3 -m http.server 8849      # http://localhost:8849
```

> Clean URL-ek (`/uj-epitkezes`) bevezetésekor a Test1 `serve.py` mintájára kell preview-szervert
> tenni a `_web/` gyökerébe — a sima `http.server` 404-et adna a kiterjesztés nélküli linkekre.

---

## 🌐 Deploy

Csak a **`_web/` tartalma** kerül élesre. A `README.md`, `CHANGELOG.md`, `VERSIONING.md`,
`VERSION`, `scripts/` és `.github/` **nem** — a többi könyvtár pedig eleve nincs a repóban.

```bash
git archive v0.01.01 --prefix=okotechhome2/ -o /tmp/okotechhome2-0.01.01.tar.gz _web
```

| Környezet | Cím | Megjegyzés |
|---|---|---|
| **Éles** | *(még nincs kijelölve)* | a Test1/Test2 közötti választás után |
| **Staging** | `https://esysint.hu/_work/oko3/` *(javasolt)* | jelszavas (Basic Auth), keresők nem indexelik |

> ⚠️ A `.htaccess` rejtett dotfile — az FTP-kliensek és ZIP-ek alapból kihagyják. Ha élesben
> minden link 404-el, jellemzően ez az ok.

---

## 🏛️ Tulajdonjog és forráskód-folytonosság

A weboldalt az **eSystem-Integration Kft.** (IEM) fejleszti az **Ökotech-Home Kft.** részére.
A forráskód **vagyonijog-átruházás + ügyfél-tulajdonú privát repó** („A” konstrukció) alapú
**forráskód-folytonossági (escrow)** megállapodás szerint kerül átadásra, hogy a fejlesztés
a szolgáltató kiesése esetén is folytatható legyen (Szjt. 1999. évi LXXVI. tv.; Ptk. 6:238. §).

> **Licenc:** Proprietary — minden jog fenntartva. Külső felhasználás, sokszorosítás és terjesztés
> a jogtulajdonos írásos engedélye nélkül tilos.

---

## 📌 Nyitott pontok

**Designrendszer-döntést igényel** (részletek: [`_web/COMPONENTS.md`](./_web/COMPONENTS.md))

- [ ] Navigációs fő CTA gombként — kerüljön-e a 7.6 komponensválasztó táblába
      az `a.btn-primary` sor, vagy a panel CTA-ja váltson `.text-link`-re
- [ ] Szekció-sávok váltakozása (5.3 elv) — a 3. és 4. szekció jelenleg egyaránt
      canvas sávon ül, a vizuális terv szerint
- [ ] Az új komponensek (kártya, szekció-sáv, táblázat, médiakeret, ikon) átemelése
      a hivatalos designrendszerbe

**Építés**

- [x] 3. szekció — *Kiinduló helyzet*
- [x] 4. szekció — *Technológiák*
- [x] Clean URL (`.htaccess` + `serve.py`)
- [ ] 1–2. szekció (hero, bizalmi sáv)
- [ ] A hivatkozott aloldalak (`uj-epitkezes`, `emeszto-kivaltasa`, `idoszakos-hasznalat`,
      `telekvasarlas`, `szervezeti-telepulesi-megoldasok`, tudástár)
- [ ] `_web/404.html`, `_web/robots.txt`, `_web/sitemap.xml`
- [ ] Staging URL kijelölése és Basic Auth beállítása
- [ ] AI backend az `AIDT` és `OFC` modulok mögé (Test1-ben kliensoldali szimuláció)
- [ ] Test1 vs. Test2 ügyfél-döntés → a nyertes ág megy `1.00.00`-ra

---

<p align="center">
  <sub>Belső dokumentum · Ökotech-Home Kft. · 2509 Esztergom, Strázsa utca 12.<br>
  Fejlesztés: eSystem-Integration Kft. (IEM — Industrial Electric &amp; Mechanic Kft.), Érd</sub>
</p>
