#!/usr/bin/env bash
#
# ellenorzes.sh — okotechhome-web2 (Test2) repository checks
#
# Usage:
#   ./scripts/ellenorzes.sh
#
# Runs the mechanical checks that a human reviewer would otherwise have to do by
# hand before every release. Each check is cheap, deterministic, and answers a
# question that has actually gone wrong at least once in this repository.
#
# Exit code 0 = everything passed. Anything else = at least one check failed.
#
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

HIBA=0
red()  { printf '\033[31m  ✕ %s\033[0m\n' "$*" >&2; HIBA=1; }
grn()  { printf '\033[32m  ✓ %s\033[0m\n' "$*"; }
ylw()  { printf '\033[33m  ! %s\033[0m\n' "$*"; }
cim()  { printf '\n\033[1m%s\033[0m\n' "$*"; }

# ── 1. Verzió ────────────────────────────────────────────────────────────────
# A `_web/VERSION` a KISZOLGÁLÓRA is felkerül: ebből lehet megállapítani, melyik
# kiadás fut élesben. Ha a gyökérhez képest elcsúszik, pont arra a kérdésre ad
# rossz választ, amiért létezik.
cim "1. Verzió"
GYOKER="$(tr -d '[:space:]' < VERSION 2>/dev/null)"
WEB="$(tr -d '[:space:]' < _web/VERSION 2>/dev/null)"

if [[ "$GYOKER" =~ ^[0-9]+\.[0-9]{2}\.[0-9]{2}$ ]]; then
  grn "VERSION formátuma feltöltött SemVer: $GYOKER"
else
  red "VERSION nem feltöltött SemVer: '$GYOKER' (elvárt: X.YY.ZZ)"
fi

if [[ "$GYOKER" == "$WEB" ]]; then
  grn "_web/VERSION megegyezik a gyökérrel"
else
  red "_web/VERSION ($WEB) ≠ VERSION ($GYOKER) — a kiszolgálón rossz verzió látszana"
fi

if grep -qE "^## \[$GYOKER\]" CHANGELOG.md; then
  grn "CHANGELOG.md tartalmaz [$GYOKER] szekciót"
else
  red "CHANGELOG.md nem tartalmaz '## [$GYOKER]' szekciót"
fi

# ── 2. Titkok ────────────────────────────────────────────────────────────────
# Egy kiszivárgott kulcs a git TÖRTÉNETÉBŐL is előbányászható: a visszavonás
# után is ott marad örökre. Ezért a kapu a commit előtt van, nem utána.
cim "2. Titkok"
TILTOTT=0
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  # A feltöltés tanúsítványlánca nyilvános adat (Let's Encrypt), és NÉLKÜLE a
  # feltoltes.sh nem tud kapcsolódni — ez a kivétel szándékos.
  [[ "$f" == "scripts/ftps-ca.pem" ]] && continue
  red "titkot tartalmazó fájl a repóban: $f"
  TILTOTT=1
done < <(git ls-files -- '*.env' '.env*' '*.key' '*.pem' '_web/api/config.php' 2>/dev/null)

# Az oth-titkok könyvtár SZERKEZETE a repóban van, a TARTALMA soha.
while IFS= read -r f; do
  [[ -z "$f" ]] && continue
  case "$f" in
    _web/oth-titkok/.htaccess|_web/oth-titkok/README.md) ;;
    *) red "az oth-titkok tartalma nem kerülhet a repóba: $f"; TILTOTT=1 ;;
  esac
done < <(git ls-files -- '_web/oth-titkok/*' 2>/dev/null)

[[ $TILTOTT -eq 0 ]] && grn "nincs titkot tartalmazó fájl a verziókövetésben"

# ── 3. Cache-busting ─────────────────────────────────────────────────────────
# A `?v=NN` a lapokon EGY érték kell legyen. Ha kettő van, a látogató fele a
# régi stíluslapot kapja, és a hiba csak nála jelentkezik — nálunk soha.
cim "3. Cache-busting"
# A `mapfile` a macOS-en szállított bash 3.2-ben nincs meg — sima szövegként
# tartjuk a listát, hogy a szkript a fejlesztőgépen is fusson, ne csak a CI-ben.
CSS_V="$(grep -rho 'app\.css?v=[0-9]\+' _web --include='*.html' 2>/dev/null | sort -u)"
CSS_DB="$(printf '%s\n' "$CSS_V" | grep -c . || true)"
if [[ "$CSS_DB" -eq 1 ]]; then
  grn "minden lap ugyanazt a stíluslapot kéri: $CSS_V"
elif [[ "$CSS_DB" -eq 0 ]]; then
  ylw "nem található app.css hivatkozás — átugorva"
else
  red "TÖBBFÉLE app.css verzió van a lapokon: $(printf '%s ' $CSS_V)"
fi

# ── 4. Hivatkozott eszközök léteznek ─────────────────────────────────────────
# Egy elgépelt szkriptnév néma: a lap betölt, csak épp egy modul nem fut le.
cim "4. Hivatkozott eszközök"
# CSAK az attribútumból: a prózában és a kommentekben is szerepelnek
# fájlnevek („a tartalom az assets/data/ajanlo-konfig.js-ben él"), azok viszont
# nem hivatkozások, és mondat közepén levágva sosem léteznének.
HIANY=0
while IFS= read -r sor; do
  lap="${sor%%:*}"
  ertek="${sor#*\"}"          # (src|href)=" utáni rész
  ertek="${ertek%\"}"         # a záró idézőjel le
  cel="_web/${ertek%%\?*}"    # a ?v=NN cache-buster le
  [[ -f "$cel" ]] && continue
  red "hiányzó eszköz: $cel (hivatkozza: ${lap#_web/})"
  HIANY=1
done < <(grep -rhoE --include='*.html' -H '(src|href)="assets/[A-Za-z0-9/_.-]+\.(js|css)(\?v=[0-9]+)?"' _web 2>/dev/null | sort -u)
[[ $HIANY -eq 0 ]] && grn "minden hivatkozott JS/CSS eszköz létezik"

# ── 5. JS szintaxis ──────────────────────────────────────────────────────────
cim "5. JS szintaxis"
if command -v node >/dev/null 2>&1; then
  JSHIBA=0
  while IFS= read -r f; do
    node --check "$f" >/dev/null 2>&1 || { red "szintaktikai hiba: $f"; JSHIBA=1; }
  done < <(git ls-files '_web/assets/js/*.js')
  [[ $JSHIBA -eq 0 ]] && grn "minden JS modul szintaktikailag ép"
else
  ylw "node nincs telepítve — a JS-ellenőrzés kimarad"
fi

# ── 6. Python szintaxis ──────────────────────────────────────────────────────
cim "6. Python szintaxis"
if command -v python3 >/dev/null 2>&1; then
  if git ls-files '*.py' | xargs -r python3 -m py_compile 2>/dev/null; then
    grn "minden Python-generátor szintaktikailag ép"
  else
    red "legalább egy Python-fájl nem fordul"
  fi
  find . -name '__pycache__' -type d -prune -exec rm -rf {} + 2>/dev/null
else
  ylw "python3 nincs telepítve — a Python-ellenőrzés kimarad"
fi

# ── 7. Teszt üzemmód ─────────────────────────────────────────────────────────
# NEM hiba, csak emlékeztető: a `Disallow: /` szándékos, amíg a webhely a
# tesztaldomainen fut. Élesítéskor viszont HÁROM helyen kell feloldani.
cim "7. Teszt üzemmód"
if grep -qE '^\s*Disallow:\s*/\s*$' _web/robots.txt 2>/dev/null; then
  ylw "TESZT ÜZEMMÓD aktív: robots.txt tiltja az indexelést (élesítéskor 3 réteget kell oldani — lásd _web/README.md)"
else
  grn "a robots.txt nem zárja el a webhelyet"
fi

# ── Összegzés ────────────────────────────────────────────────────────────────
if [[ $HIBA -eq 0 ]]; then
  printf '\n\033[32mMinden ellenőrzés rendben.\033[0m\n'
else
  printf '\n\033[31mLegalább egy ellenőrzés elbukott.\033[0m\n'
fi
exit $HIBA
