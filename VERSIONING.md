<p align="center">
  <img src="./.github/banner.png" alt="ÖkoTech Home — otthoni biológiai szennyvíztisztítás" width="100%">
</p>

<h1 align="center">Verziózási szabályzat — ÖkoTech Home <em>Test2</em></h1>

<p align="center">
  <img src="https://img.shields.io/badge/verzi%C3%B3-0.01.01-36C5E6?style=flat-square" alt="verzió 0.01.01">
  <img src="https://img.shields.io/badge/SemVer-2.0.0%20(padded)-1572B6?style=flat-square" alt="SemVer 2.0.0 padded">
  <img src="https://img.shields.io/badge/Conventional%20Commits-1.0.0-FE5196?style=flat-square" alt="Conventional Commits 1.0.0">
  <img src="https://img.shields.io/badge/Keep%20a%20Changelog-1.1.0-C9A24A?style=flat-square" alt="Keep a Changelog">
</p>

Ez a dokumentum rögzíti, **hogyan kap verziószámot** az `okotechhome-web2` (Test2) munkaterület,
mikor kell emelni, ki emeli, és mi történik a kiadáskor. A tényleges változásokat a
[`CHANGELOG.md`](./CHANGELOG.md) tartalmazza.

> **Viszony a Test1-hez.** A Test1 (`okotechhome-web`, jelenleg `0.9.0`) és a Test2 azonos
> márkát, motort, technológiát és logót visz, **eltérő designrendszerrel**. A két repó
> verziószáma **független**: a Test2 saját, nulláról induló idővonalon halad `0.01.01`-től.

---

## 1. Az igazság forrásai

| Forrás | Szerep |
|---|---|
| `VERSION` | Az aktuális verzió gépi olvasásra, egyetlen sorban (`0.01.01`). **Ez az elsődleges forrás.** |
| `CHANGELOG.md` | Emberi olvasásra: mi változott, mikor, melyik commitban. |
| Git tag (`vX.YY.ZZ`) | A kiadás megváltoztathatatlan (immutable) horgonya a történetben. |

A háromnak **mindig egyeznie kell**. A [`scripts/release.sh`](./scripts/release.sh) ezt kikényszeríti.

---

## 2. Verziószám-formátum — nullákkal feltöltött SemVer

```
MAJOR . MINOR . PATCH
  X   .  YY   .  ZZ          →  0.01.01
  │      │       └── két számjegy, nullával feltöltve (01, 02, … 09, 10, 11 …)
  │      └────────── két számjegy, nullával feltöltve
  └───────────────── nincs feltöltés (0, 1, 2 …)
```

A séma a [SemVer 2.0.0](https://semver.org/lang/hu/) **rendezési és jelentéstani szabályait**
követi, csak a `MINOR` és `PATCH` mezőt **két számjegyre feltöltve** írjuk. A cél, hogy a
kiadások neve fájlnévben, tag-listában és deploy-mappában is **lexikografikusan rendezett**
maradjon (`v0.01.01 < v0.02.00 < v0.10.00`), plain `sort` mellett is.

| Szabály | Részlet |
|---|---|
| **Kezdőverzió** | `0.01.01` — a Test2 munkaterület inicializálása |
| **Érvényes minta** | `^[0-9]+\.[0-9]{2}\.[0-9]{2}$` |
| **Tag** | `v` előtag + a verzió: `v0.01.01` |
| **Túlcsordulás** | ha a `MINOR` vagy `PATCH` eléri a `99`-et, a következő szint emelendő |
| **Összehasonlítás** | mezőnként **numerikusan** (`10#` bázissal, hogy a `08`/`09` ne oktálisan értelmeződjön) |
| **Előkiadás** | `0.02.00-rc.1` — megengedett, de a jelen fázisban nem használt |

> ⚠️ **Eszköz-kompatibilitás.** Szigorú SemVer-parserek (npm `semver`, `sort -V` régi BSD-változat)
> a `01`-et vezető nullás mezőként elutasíthatják vagy tévesen rendezhetik. Ezért a repó **nem**
> támaszkodik `package.json`-verzióra: az egyetlen forrás a `VERSION` fájl, az összehasonlítást
> pedig a `release.sh` végzi saját, numerikus logikával.

---

## 3. SemVer-értelmezés statikus marketing-oldalra

A klasszikus SemVer API-kra készült; itt a „nyilvános felület” nem függvényszignatúra,
hanem **URL-struktúra, oldal-inventár és a látogató által látott döntési tölcsér**.

### MAJOR — `X.00.00`

Törő változás a nyilvános felületen. Emelendő, ha:

- URL megszűnik vagy megváltozik átirányítás nélkül (SEO-törés),
- oldal kikerül az inventárból (a `sitemap.xml` szűkül),
- a döntési tölcsér szerkezete alapjaiban változik (szekciók sorrendje / logikája újraírva),
- a designrendszer tokenkészlete lecserélődik,
- a `.htaccess` rewrite- vagy CSP-politikája inkompatibilisen változik,
- a nyelvi hatókör bővül (pl. HU → HU/EN/DE többnyelvű útvonalak).

> **`0.yy.zz` fázis.** Amíg a `MAJOR` = `0`, a projekt átadás előtti állapotban van: a `MINOR`
> viselkedik törő-verzióként. Az **`1.00.00`-t az ügyfél általi éles átvétel (go-live elfogadás)**
> alkalmával kell kiadni.

### MINOR — `x.YY.00`

Visszafelé kompatibilis bővítés. Emelendő, ha:

- új oldal kerül a `_web/`-be,
- új főoldali szekció vagy modul jelenik meg,
- meglévő szekció érdemben újraépül vagy új képességet kap,
- új médiaeszköz-készlet (hero-videó csere, új illusztráció-sorozat) érkezik,
- új integráció vagy backend-végpont bekötése történik.

### PATCH — `x.yy.ZZ`

Hibajavítás és csiszolás, új képesség nélkül:

- vizuális hiba, tördelés, böngésző-inkompatibilitás javítása,
- szövegjavítás (elgépelés, megfogalmazás), meta-adat pontosítás,
- meglévő eszköz cseréje jobb változatra funkcióváltozás nélkül,
- teljesítmény-finomhangolás mérhető viselkedésváltozás nélkül.

### Amit **nem** kell verziózni

Dokumentáció-only változás (`README.md`, `CHANGELOG.md` elgépelés), lokális fejlesztői
eszköz módosítása — ezek a következő kiadással utaznak.

---

## 4. Conventional Commits → verzióemelés

A repó [Conventional Commits](https://www.conventionalcommits.org/) formátumot használ,
**angol commit-üzenettel** (a belső dokumentáció magyar).

```
<típus>(<hatókör>): <mit, jelen időben, kisbetűvel>
```

| Típus | Jelentés | Verzióhatás |
|---|---|---|
| `feat` | új képesség, oldal, szekció | **MINOR** |
| `fix` | hibajavítás | **PATCH** |
| `style` | vizuális csiszolás, viselkedésváltozás nélkül | **PATCH** |
| `refactor` | átszervezés kimeneti változás nélkül | **PATCH** |
| `perf` | teljesítmény | **PATCH** |
| `docs` | dokumentáció | — |
| `chore` | karbantartás, eszközök | — |
| `feat!` / `BREAKING CHANGE:` lábjegyzet | törő változás | **MAJOR** |

**Bevált hatókörök (scope):** `design` (tokenek, `app.css`), `web` (szekció- és oldalépítés),
`compare` (összehasonlító tábla), `hero`, `nav`, `form`, `seo`, `a11y`, `htaccess`, `assets`,
`icon`, `readme`, `release`.

Példák:

```
feat(design): introduce the Test2 token set and type scale      → MINOR
fix(hero): keep the scroll cue visible on 360 px viewports      → PATCH
style(nav): tighten the header spacing on tablet                → PATCH
docs(readme): document the repository scope and deploy flow     → nincs emelés
```

---

## 5. Ágak és tagek

| Elem | Konvenció | Példa |
|---|---|---|
| Fő ág | `main` — mindig telepíthető állapot | |
| Munkaág | `feat/<rövid-leírás>`, `fix/<rövid-leírás>` | `feat/design-tokens` |
| Hotfix | `hotfix/<rövid-leírás>` | `hotfix/csp-fonts` |
| Kiadási tag | **annotált** tag, `v` előtaggal | `v0.01.01` |

A tag **mindig annotált** (`git tag -a`), soha nem lightweight — így hordozza a kiadó nevét,
a dátumot és a kiadási megjegyzést, és a `git describe` is helyesen működik.

---

## 6. Kiadási folyamat

### Automatizáltan

```bash
./scripts/release.sh 0.02.00 --dry-run   # próba: mit csinálna
./scripts/release.sh 0.02.00             # éles kiadás
```

A szkript lépései:

1. ellenőrzi, hogy a munkakönyvtár tiszta és `main`-en állunk,
2. validálja a feltöltött verziószám formátumát, és hogy nagyobb-e a jelenleginél,
3. ellenőrzi, hogy a `CHANGELOG.md` tartalmaz-e szekciót az új verzióhoz,
4. frissíti a `VERSION` fájlt,
5. `chore(release): vX.YY.ZZ` committal rögzít,
6. annotált taget hoz létre a `CHANGELOG` szekció összefoglalójával,
7. kiírja a push-parancsot (**nem push-ol magától**).

### Kézzel

```bash
echo "0.02.00" > VERSION
# CHANGELOG.md: [Kiadatlan] → [0.02.00] — ÉÉÉÉ-HH-NN
git add VERSION CHANGELOG.md
git commit -m "chore(release): v0.02.00"
git tag -a v0.02.00 -m "v0.02.00 — <egymondatos összefoglaló>"
git push origin main --follow-tags
```

---

## 7. Kiadási ellenőrzőlista

Éles kiadás előtt:

- [ ] `CHANGELOG.md` `[Kiadatlan]` szekciója átnevezve, dátummal
- [ ] `VERSION` és a tag egyezik, a formátum feltöltött (`0.02.00`, nem `0.2.0`)
- [ ] Minden új / módosult oldal szerepel a `_web/sitemap.xml`-ben
- [ ] `_web/robots.txt` nem tiltja az új útvonalakat
- [ ] Navigáció és lábléc szinkron minden HTML fájlban
- [ ] Új külső forrás esetén a `_web/.htaccess` CSP kiegészítve
- [ ] Lokális ellenőrzés (clean URL viselkedés)
- [ ] `prefers-reduced-motion` alatt is működik minden új animáció
- [ ] Új médiaeszköz optimalizálva (WebP/AVIF kép, MP4 + WebM videó + poster)
- [ ] Billentyűzetes bejárás és látható fókusz az új interaktív elemeken (WCAG 2.2 AA)
- [ ] Core Web Vitals nem romlott (LCP < 2,5 s · INP < 200 ms · CLS < 0,1)

---

## 8. Deploy-korreláció

A telepítés Apache shared hostingra történik (FTP/rsync), tehát a szerveren nincs git.
Hogy egy éles hiba visszavezethető legyen egy verzióra:

1. minden deploy **tag-elt commitról** induljon,
2. a deploy után a tag üzenetébe vagy a kiadási jegyzetbe kerüljön a dátum és a környezet,
3. a `git tag --contains <commit>` megmondja, melyik kiadás óta él egy változás,
4. két kiadás különbsége bármikor visszanézhető:

```bash
git diff v0.01.01..v0.02.00 --stat        # mi változott két kiadás közt
git log v0.01.01..v0.02.00 --oneline      # milyen commitok
```

Csak a `_web/` tartalma kerül élesre — csomagolás tag-elt kiadásból:

```bash
git archive v0.02.00 --prefix=okotechhome2/ -o /tmp/okotechhome2-0.02.00.tar.gz _web
```

---

## 9. Visszaállítás (rollback)

```bash
# 1) mi az utolsó jó kiadás
git tag --sort=-v:refname | head -5

# 2) az adott kiadás fájljainak kinyerése egy külön könyvtárba, feltöltésre
git archive v0.01.01 --prefix=okotechhome2-0.01.01/ -o /tmp/okotechhome2-0.01.01.tar.gz

# 3) ha a main-t is vissza kell tekerni (a történet megőrzésével)
git revert --no-commit v0.01.01..HEAD && git commit -m "revert: back to v0.01.01 state"
```

A `git revert` előnyben részesítendő a `git reset --hard` helyett: megőrzi az auditálhatóságot,
ami a NIS2 szerinti változáskövetés miatt is elvárás.

---

## 10. Verzió-életút

| Fázis | Verziótartomány | Állapot |
|---|---|---|
| Munkaterület-inicializálás | `0.01.01` | kiadva |
| Designrendszer-implementáció + 3–4. szekció | `0.02.00` | **kiadásra kész** |
| További szekciók és aloldalak | `0.03.00` – `0.99.xx` | tervezett |
| Éles átvétel (go-live) | `1.00.00` | tervezett |
| Karbantartás, tartalom-bővítés | `1.xx.yy` | tervezett |
| Többnyelvűsítés (HU/EN/DE), CRM/AI backend | `2.00.00` | opció |

---

<p align="center">
  <sub>Ökotech-Home Kft. · fejlesztő: eSystem-Integration Kft. (eSI Kft.), Érd</sub>
</p>
