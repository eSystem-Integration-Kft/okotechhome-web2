#!/usr/bin/env bash
#
# prod-epit.sh — a `_web_prod/` előállítása a `_web/` fából.
# =============================================================================
# MI EZ ÉS MIÉRT VAN
#
# Két webhelyünk van, de EGY forrásunk:
#
#     _web/        →  tst.okoth.hu   — itt fejlesztünk, ezt nézzük meg
#     _web_prod/   →  okotechhome.hu — ez megy élesbe
#
# A `_web_prod/` NEM MÁSODIK FORRÁS, hanem a `_web/` KIMENETE. Ez a különbség
# a lényeg: ha a két fát kézzel tartanánk karban, néhány héten belül
# elcsúsznának egymástól — minden javítást kétszer kellene megcsinálni, és a
# „melyik az igazi?" kérdésre a kettő közül valamelyik mindig rossz választ
# adna. Így viszont a `_web/` az egyetlen igazság, a `_web_prod/` pedig
# bármikor eldobható és újraépíthető.
#
# EBBŐL KÖVETKEZIK: a `_web_prod/`-ba KÉZZEL SOHA NE ÍRJ. Ami ott van, azt a
# következő futtatás felülírja. A `.gitignore` ezért zárja ki a verziókövetésből.
#
# MI A KÜLÖNBSÉG A KETTŐ KÖZÖTT
#
# Mindössze annyi, amennyi a teszt és az éles között szükségszerű — a
# TESZT ÜZEMMÓD három rétege (lásd `_web/README.md`):
#
#   1. minden HTML `<head>`-jében a `noindex` meta → `index, follow`
#   2. a `.htaccess` `X-Robots-Tag: noindex` sora kikommentezve
#   3. a `robots.txt` megkapja a `Sitemap:` sort
#
# A tartalom, a stílus, a szkriptek, a képek BÁJTRA AZONOSAK. Ami az éles
# oldalon másképp néz ki, az hiba, nem szándék.
#
# AMI NEM ITT DŐL EL: az `api/config.php` (git-ignorált, csak a kiszolgálón
# él) `origin` listája és az e-mail `url`/`logo` értéke — azt az éles gépen
# kell átírni, egyszer. Lásd `_web/README.md` élesítési ellenőrzőlista.
#
# HASZNÁLAT
#     scripts/prod-epit.sh              # felépíti a _web_prod/-ot
#     scripts/prod-epit.sh --ellenoriz  # csak megnézi, naprakész-e
# =============================================================================
set -euo pipefail

GYOKER="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FORRAS="$GYOKER/_web"
CEL="$GYOKER/_web_prod"

piros() { printf '\033[31m%s\033[0m\n' "$*" >&2; }
zold()  { printf '\033[32m%s\033[0m\n' "$*"; }
sarga() { printf '\033[33m%s\033[0m\n' "$*"; }
halk()  { printf '\033[2m%s\033[0m\n' "$*"; }

CSAK_ELLENORZES=0
[[ "${1:-}" == "--ellenoriz" ]] && CSAK_ELLENORZES=1

[ -d "$FORRAS" ] || { piros "Nincs meg a forrás: $FORRAS"; exit 1; }

# ---------------------------------------------------------------- ellenőrzés
# NAPRAKÉSZ-E. A `_web/` legfrissebb módosítását hasonlítjuk a `_web_prod/`
# jelzőfájljához. Nem tartalom-hasonlítás: az a több ezer fájlon lassú volna,
# és úgyis csak arra a kérdésre kell válaszolni, hogy „építettünk-e a legutóbbi
# szerkesztés óta".
JELZO="$CEL/.epult"
if [ "$CSAK_ELLENORZES" = 1 ]; then
  if [ ! -f "$JELZO" ]; then
    piros "A _web_prod/ még nem épült fel. Futtasd: scripts/prod-epit.sh"
    exit 1
  fi
  UJABB="$(find "$FORRAS" -type f -newer "$JELZO" ! -path '*/.git/*' | head -5)"
  if [ -n "$UJABB" ]; then
    piros "A _web_prod/ ELAVULT — a _web/ azóta változott:"
    printf '%s\n' "$UJABB" | sed "s#$GYOKER/#      #"
    echo "  Futtasd újra: scripts/prod-epit.sh" >&2
    exit 1
  fi
  zold "A _web_prod/ naprakész (épült: $(cat "$JELZO"))."
  exit 0
fi

# ------------------------------------------------------------------- másolás
# TÜKRÖZÉS, nem hozzáfűzés: a `--delete` miatt ami a forrásból kikerült, az a
# kimenetből is eltűnik. E nélkül a törölt lapok élesben ottragadnának.
#
# A `.epult` jelzőfájlt a törlés alól KI KELL VENNI, különben a tükrözés
# letörli, mielőtt kiírnánk — és az `--ellenoriz` soha nem találná meg.
echo
sarga "╭─ _web_prod építése ─────────────────────────────────────────╮"
printf '  forrás ..... %s\n' "$FORRAS"
printf '  kimenet .... %s\n' "$CEL"
echo  "╰─────────────────────────────────────────────────────────────╯"

mkdir -p "$CEL"
rsync -a --delete --exclude '.epult' "$FORRAS"/ "$CEL"/

# --------------------------------------------------- 1. réteg: a noindex meta
# Minden lap fejlécében ugyanaz az egy sor áll; a `_web/` oldalain a fölötte
# lévő megjegyzés is kimondja, hogy élesítéskor ezt kell cserélni.
# EGYETLEN PYTHON-MENET, nem fájlonkénti indítás. Száznyolcvanhat lapra a
# `python3` elindítása önmagában tovább tart, mint maga a csere.
LAPOK=$(python3 - "$CEL" <<'PYMETA'
import sys, pathlib

CEL = pathlib.Path(sys.argv[1])

META_TESZT = ('<meta name="robots" content="noindex, nofollow, noarchive, '
              'nosnippet, noimageindex, notranslate, max-snippet:0, '
              'max-image-preview:none, max-video-preview:0, noai, noimageai">')
META_ELES = '<meta name="robots" content="index, follow">'

# A meta FOLOTT allo teszt-uzemmodi megjegyzes is megy: elesben felrevezetne,
# mert epp az ellenkezojet irja le annak, ami a sorban all.
MEGJEGYZES = """<!-- TESZT ÜZEMMÓD: a robot LETÖLTHETI a lapot (a robots.txt engedi), de nem
     indexelheti, nem archiválhatja és nem idézhet belőle — ugyanezt küldi a
     .htaccess X-Robots-Tag fejléce is. ÉLESÍTÉSKOR a lenti sor tartalmát
     "index, follow"-ra kell cserélni, minden oldalon. -->
"""

db = 0
for f in CEL.rglob('*.html'):
    t = f.read_text(encoding='utf-8')
    if META_TESZT not in t:
        continue
    t = t.replace(MEGJEGYZES, '').replace(META_TESZT, META_ELES)
    f.write_text(t, encoding='utf-8')
    db += 1
print(db)
PYMETA
)

# ------------------------------------------- 2. réteg: az X-Robots-Tag fejléc
# CSAK az A) blokk sorát kommentezzük ki. A B) blokk (AI- és SEO-botok
# kizárása) élesben is MARAD — az nem a teszt üzemmód része.
python3 - "$CEL/.htaccess" <<'PY'
import sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding='utf-8')
sor = '  Header always set X-Robots-Tag "noindex, nofollow, noarchive, nosnippet, noimageindex, notranslate, max-snippet:0, max-image-preview:none, max-video-preview:0, noai, noimageai"'
if sor not in t:
    sys.exit('HIBA: az X-Robots-Tag sor nem található a .htaccess-ben — a teszt üzemmód szerkezete megváltozott, a prod-epit.sh-t hozzá kell igazítani.')
t = t.replace(sor,
  '  # ÉLES ÜZEMMÓD — az indexelés tiltása kivéve. A sort a prod-epit.sh\n'
  '  # kommentezte ki; a `_web/`-ben változatlanul aktív, mert ott a teszt fut.\n'
  '  # ' + sor.strip())
p.write_text(t, encoding='utf-8')
PY

# ----------------------------------------------- 3. réteg: robots.txt sitemap
# CSAK AKKOR JELENTJÜK BE, HA VAN MIT. Egy 404-re mutató `Sitemap:` sor
# rosszabb, mint a hiánya: a kereső hibaként naplózza, és a Search Console-ban
# is az jelenik meg. A `sitemap.xml` ma még nincs meg (lásd `_web/README.md`
# „Hiányzik" pontját) — amint elkészül, ez a sor magától bekerül.
if [ -f "$CEL/sitemap.xml" ]; then
  python3 - "$CEL/robots.txt" <<'PYROBOTS'
import re, sys, pathlib
p = pathlib.Path(sys.argv[1])
t = p.read_text(encoding='utf-8')
# SORELEJI direktívát keresünk, nem a puszta szót: a fájl fejlécében
# megjegyzésben is szerepel a „Sitemap:", és arra ráfutva sosem írnánk ki a
# valódi sort.
if not re.search(r'^Sitemap:', t, re.M):
    t = t.rstrip('\n') + (
        '\n\n\n# --- 4) Webhelytérkép ----------------------------------------------------\n'
        '# Élesben ez mondja meg a keresőnek, hol kezdje. A `_web/` tesztfájljában\n'
        '# nincs benne: ott nincs mit bejelenteni.\n'
        'Sitemap: https://okotechhome.hu/sitemap.xml\n')
    p.write_text(t, encoding='utf-8')
PYROBOTS
  SITEMAP_VAN=1
else
  SITEMAP_VAN=0
fi

# ------------------------------------------------------------------- jelölés
cat > "$CEL/.epult" <<EOF
$(date '+%Y-%m-%d %H:%M:%S')
EOF
cat > "$CEL/OLVASSEL.txt" <<'EOF'
EZ A KÖNYVTÁR GENERÁLT — KÉZZEL NE SZERKESZD.

Forrása a `_web/`, előállítója a `scripts/prod-epit.sh`. Ami itt van, azt a
következő futtatás felülírja, és a verziókövetés sem tartja számon.

  _web/       → tst.okoth.hu    (itt fejlesztünk)
  _web_prod/  → okotechhome.hu  (ez megy élesbe)

A kettő között csak a teszt üzemmód három rétege a különbség: a noindex meta,
az X-Robots-Tag fejléc és a robots.txt Sitemap-sora. A tartalom azonos.
EOF

# ---------------------------------------------------------------- ellenőrzés
# A `|| true` NEM ELHAGYHATÓ. A `set -o pipefail` mellett a találat nélküli
# `grep` (kilépés 1) az EGÉSZ csővezetéket bukottá teszi, a `set -e` pedig
# megállítja a szkriptet — épp akkor, amikor a helyes eredményt találta meg.
MARADT_META=$( { grep -rlF 'content="noindex' "$CEL" --include='*.html' 2>/dev/null || true; } | wc -l | tr -d ' ')
MARADT_FEJLEC=$(grep -c '^  Header always set X-Robots-Tag' "$CEL/.htaccess" 2>/dev/null || true)
SITEMAP=$( { grep -c '^Sitemap:' "$CEL/robots.txt" 2>/dev/null || true; } | head -1)

echo
printf '  noindex meta cserélve ....... %s lapon\n' "$LAPOK"
printf '  maradt noindex meta ......... %s  %s\n' "$MARADT_META" "$([ "$MARADT_META" = 0 ] && echo '✓' || echo '✕ HIBA')"
printf '  aktív X-Robots-Tag sor ...... %s  %s\n' "${MARADT_FEJLEC:-0}" "$([ "${MARADT_FEJLEC:-0}" = 0 ] && echo '✓' || echo '✕ HIBA')"
if [ "$SITEMAP_VAN" = 1 ]; then
  printf '  robots.txt Sitemap sor ...... %s  %s\n' "${SITEMAP:-0}" "$([ "${SITEMAP:-0}" = 1 ] && echo '✓' || echo '✕ HIBA')"
else
  printf '  robots.txt Sitemap sor ...... –  (nincs sitemap.xml, ezért nem is jelentjük be)\n'
fi
echo

if [ "$MARADT_META" != 0 ] || [ "${MARADT_FEJLEC:-0}" != 0 ] \
   || { [ "$SITEMAP_VAN" = 1 ] && [ "${SITEMAP:-0}" != 1 ]; }; then
  piros "A _web_prod/ NEM élesíthető — a fenti ellenőrzés bukott."
  exit 1
fi

zold "Kész. Feltöltés élesbe:  scripts/feltoltes.sh eles --eles"
halk "(Előtte érdemes: scripts/feltoltes.sh eles — próbamenet, nem ír semmit.)"
