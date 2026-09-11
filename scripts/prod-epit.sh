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

# --------------------------------------- 2/b. réteg: sitemap.xml és llms.txt
# A TÉRKÉP ITT KÉSZÜL, nem a `_web/`-ben: ott minden lap `noindex`, tehát a
# térkép szükségszerűen üres lenne — és ha mégsem szűrnénk, olyan lapokat
# jelentene be, amiket ugyanaz a lap a metasorában letilt. A sorrend kötött:
# a noindex-réteg UTÁN, a robots.txt-réteg ELŐTT (az onnan tudja meg, hogy van
# már mit bejelenteni).
python3 "$GYOKER/scripts/oldalgyartas/sitemap.py" "$CEL" | sed 's/^/  /'
python3 "$GYOKER/scripts/oldalgyartas/llms.py" "$CEL" | sed 's/^/  /'

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

# ------------------------------------------- 4. réteg: a PHP-kezelő rögzítése
# MIÉRT KELL. A cPanel a MultiPHP-beállítást a `/public_html/.htaccess`-be
# írja (`AddHandler application/x-httpd-ea-phpXX`). A telepítés viszont ezt a
# fájlt FELÜLÍRJA a miénkkel — a kezelő eltűnik, és a könyvtár a fiók
# alapértelmezésére esik vissza. Élesben ez egyszer már megtörtént: az `api/`
# PHP 7.4-re esett, a kód pedig 8.0+ elemet használ (záró vessző a
# paraméterlistában), tehát MINDEN végpont 500-at adott.
#
# Ezért a kezelőt MI tesszük bele, és nem hagyjuk a szerencsére. A `_web/`-be
# NEM kerül: a teszt másik tárhelyen van, más csomagkészlettel — ott ez a sor
# éppen hogy elronthatná a PHP-feldolgozást.
#
# A CSOMAG NEVE a tárhelyé (EasyApache 4). Mérve 2026-09-11-én mind a négy
# telepítve van: ea-php82 (8.2.33) · ea-php83 (8.3.33) · ea-php84 (8.4.24) ·
# ea-php85 (8.5.9). Verzióváltáskor EZT a sort kell átírni — és utána
# ellenőrizni, hogy az `api/` végpontjai 422-t adnak üres POST-ra, nem 500-at.
PHP_CSOMAG="${OTH_PHP_CSOMAG:-ea-php82}"
python3 - "$CEL/.htaccess" "$PHP_CSOMAG" <<'PYPHP'
import sys, pathlib
p, csomag = pathlib.Path(sys.argv[1]), sys.argv[2]
t = p.read_text(encoding='utf-8')
if 'x-httpd-' in t:
    sys.exit(0)
t = t.rstrip('\n') + (
    '\n\n# --- PHP-KEZELŐ (élesben rögzítve) ------------------------------------------\n'
    '# A cPanel MultiPHP ide írná a maga sorát, de a telepítés felülírja ezt a\n'
    '# fájlt — ezért a `scripts/prod-epit.sh` teszi bele. A kód PHP 8.0+ elemeket\n'
    '# használ; e nélkül a könyvtár a fiók alapértelmezésére esne vissza, és az\n'
    '# `api/` egyszer már 7.4-re esett vissza emiatt (minden végpont 500).\n'
    '<IfModule mime_module>\n'
    f'  AddHandler application/x-httpd-{csomag} .php .php8 .phtml\n'
    '</IfModule>\n')
p.write_text(t, encoding='utf-8')
PYPHP

# ------------------------------------- 5. réteg: az AI-robotok beengedése
# DÖNTÉS (Bela, 2026-09-11): az ÉLES oldal MINDEN AI-robotot beenged — a
# válaszadókat (OAI-SearchBot, PerplexityBot, Claude-SearchBot…) és a
# modelltanítókat (GPTBot, ClaudeBot, CCBot, Google-Extended…) is. A cél az
# AI-keresési láthatóság: ami nem érhető el, azt egyetlen AI-kereső sem tudja
# idézni. Mérve élesítés előtt: mind a tizenkét próbált AI-ügynök 403-at kapott,
# tehát a GEO-láthatóság pontosan nulla volt.
#
# A TESZT ZÁRVA MARAD. A `tst.okoth.hu` `noindex`, nincs kihirdetve, és
# félkész szövegek vannak rajta — annak nincs helye sem modellben, sem AI-válaszban.
# Ezért él ez a réteg csak itt, és nem a `_web/`-ben.
#
# A SEO-ELEMZŐ BOTOK TILTVA MARADNAK (Ahrefs, Semrush, MJ12, DotBot…): azok nem
# hoznak látogatót és nem idéznek, csak a szerkezetet mérik fel harmadik fél
# eszközéhez.
python3 - "$CEL" <<'PYAI'
import re, sys, pathlib

CEL = pathlib.Path(sys.argv[1])

# --- robots.txt: a 2) szakasz (AI-botok) kivétele ---
r = CEL / 'robots.txt'
t = r.read_text(encoding='utf-8')
kezd = t.find('# --- 2) AI-tanító')
veg = t.find('# --- 3) SEO-elemző')
if kezd == -1 or veg == -1 or veg < kezd:
    sys.exit('HIBA: a robots.txt szakaszhatárai nem találhatók — '
             'a szerkezet megváltozott, a prod-epit.sh-t hozzá kell igazítani.')
t = t[:kezd] + (
    '# --- 2) AI-tanító és AI-kereső (GEO) botok — ÉLESBEN ENGEDVE ---------------\n'
    '# A tiltólistát a `prod-epit.sh` vette ki. Az éles oldal célja az\n'
    '# AI-keresési láthatóság: amit a robot nem tud letölteni, azt egyetlen\n'
    '# AI-kereső sem tudja idézni. A TESZT oldalon (`_web/`) a tiltás megmarad.\n'
    '# A felsorolás ott van, ha egyszer vissza kell kapcsolni.\n\n\n'
) + t[veg:]
r.write_text(t, encoding='utf-8')

# --- .htaccess: az AI-ügynökök SetEnvIf sorainak kivétele ---
# A SEO-botok sora (Ahrefs, Semrush…) MARAD. A kettőt a tartalmuk különíti el,
# nem a sorszámuk: a sorszám az első átrendezésnél elcsúszna.
h = CEL / '.htaccess'
t = h.read_text(encoding='utf-8')
AI_JEL = ('GPTBot', 'meta-externalagent', 'CCBot')     # a három AI-sor kezdő mintája
SEO_JEL = ('AhrefsBot',)
uj_sorok, kivett = [], 0
for sor in t.split('\n'):
    ai = sor.lstrip().startswith('SetEnvIfNoCase User-Agent') and any(j in sor for j in AI_JEL)
    if ai and not any(j in sor for j in SEO_JEL):
        uj_sorok.append('  # ÉLESBEN ENGEDVE (prod-epit.sh) — AI-robotok: ' + sor.strip()[:60] + '…')
        kivett += 1
        continue
    uj_sorok.append(sor)
if kivett != 3:
    sys.exit(f'HIBA: {kivett} AI-sort találtam a .htaccess-ben 3 helyett — '
             'a szerkezet megváltozott, a prod-epit.sh-t hozzá kell igazítani.')
h.write_text('\n'.join(uj_sorok), encoding='utf-8')
print(f'AI-robotok beengedve: robots.txt 2) szakasz + {kivett} .htaccess-sor')
PYAI

# ------------------------------------- 6. réteg: a mérés (GA4) bekapcsolása
#
# A MÉRÉS CSAK AZ ÉLES OLDALON FUT. Ha a `_web/`-be tennénk, a saját
# fejlesztői forgalmunk és minden tesztbeküldés bekerülne a GA4-be — a
# kiindulási adat pedig pont annyira ér, amennyire tiszta. Ezért a mérés is
# réteg, ugyanúgy, mint a noindex eltávolítása.
#
# A MÉRŐAZONOSÍTÓ ITT ÁLL, egy helyen. A `meres.js` maga nem tartalmazza: a
# beszúrt tag `data-ga4` attribútumából olvassa ki, és azonosító híján nem
# csinál semmit. Így ugyanaz a fájl mehet mindkét fába.
#
# A HOZZÁJÁRULÁST NEM EZ A RÉTEG KEZELI. A `meres.js` alapból MINDENT tilt
# (Consent Mode v2 `denied`), és csak akkor enged, ha a `suti.js` — ami
# mindkét fában ott van — azt hirdeti, hogy a látogató a statisztikai
# kategóriát engedélyezte. A mérés bekapcsolása tehát nem kerüli meg a
# hozzájárulást, csak elérhetővé teszi.
GA4="G-EN120W3K2Q"
python3 - "$CEL" "$GA4" <<'PYGA'
import pathlib, re, sys
cel, ga4 = pathlib.Path(sys.argv[1]), sys.argv[2]
sor = ('<!-- Mérés (GA4). Hozzájárulásig minden tárolás tiltva — lásd\n'
       '     assets/js/meres.js és assets/js/suti.js. -->\n'
       f'<script src="/assets/js/meres.js?v=1" data-ga4="{ga4}" defer></script>\n')
n = 0
for f in sorted(cel.rglob('*.html')):
    t = f.read_text(encoding='utf-8')
    if 'assets/js/meres.js' in t or '</head>' not in t:
        continue
    f.write_text(t.replace('</head>', sor + '</head>', 1), encoding='utf-8')
    n += 1
print(f'mérés beszúrva: {n} lapon ({ga4})')
PYGA

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
MERES=$( { grep -rl 'assets/js/meres.js' "$CEL" --include='*.html' 2>/dev/null || true; } | wc -l | tr -d ' ')
SUTI=$( { grep -rl 'assets/js/suti.js' "$CEL" --include='*.html' 2>/dev/null || true; } | wc -l | tr -d ' ')
MARADT_META=$( { grep -rlF 'content="noindex' "$CEL" --include='*.html' 2>/dev/null || true; } | wc -l | tr -d ' ')
MARADT_FEJLEC=$(grep -c '^  Header always set X-Robots-Tag' "$CEL/.htaccess" 2>/dev/null || true)
SITEMAP=$( { grep -c '^Sitemap:' "$CEL/robots.txt" 2>/dev/null || true; } | head -1)

echo
printf '  noindex meta cserélve ....... %s lapon\n' "$LAPOK"
printf '  maradt noindex meta ......... %s  %s\n' "$MARADT_META" "$([ "$MARADT_META" = 0 ] && echo '✓' || echo '✕ HIBA')"
printf '  aktív X-Robots-Tag sor ...... %s  %s\n' "${MARADT_FEJLEC:-0}" "$([ "${MARADT_FEJLEC:-0}" = 0 ] && echo '✓' || echo '✕ HIBA')"
PHPKEZ=$( { grep -c 'x-httpd-' "$CEL/.htaccess" 2>/dev/null || true; } | head -1)
printf '  PHP-kezelő rögzítve ......... %s  %s\n' "$PHP_CSOMAG" "$([ "${PHPKEZ:-0}" = 1 ] && echo '✓' || echo '✕ HIBA')"
if [ "$SITEMAP_VAN" = 1 ]; then
  printf '  robots.txt Sitemap sor ...... %s  %s\n' "${SITEMAP:-0}" "$([ "${SITEMAP:-0}" = 1 ] && echo '✓' || echo '✕ HIBA')"
else
  printf '  robots.txt Sitemap sor ...... –  (nincs sitemap.xml, ezért nem is jelentjük be)\n'
fi
printf '  mérés (GA4) a lapokon ....... %s  %s\n' "$MERES" "$([ "${MERES:-0}" -gt 0 ] && echo '✓' || echo '✕ HIBA')"
# A SORREND ITT ÁLLÍTÁS: hozzájárulási felület nélkül mérés nem mehet ki. Ha a
# `suti.js` valamiért kevesebb lapon van, mint a `meres.js`, az különbség némán
# jogsértő lapokat jelentene — ezért ez is kapu, nem tájékoztatás.
printf '  süti-hozzájárulás a lapokon . %s  %s\n' "$SUTI" "$([ "${SUTI:-0}" -ge "${MERES:-0}" ] && [ "${SUTI:-0}" -gt 0 ] && echo '✓' || echo '✕ HIBA — mérés hozzájárulás nélkül')"

echo

# A MÉRÉS KAPUJA IS ITT VAN. Mérés hozzájárulási felület nélkül nem kerülhet
# ki: ha a `suti.js` kevesebb lapon van, mint a `meres.js`, akkor a különbségen
# a GA4 a látogató beleegyezése nélkül futna. Ez nem figyelmeztetés, hanem
# leállás — az ilyen hiba némán keletkezik, és utólag nem javítható ki.
if [ "$MARADT_META" != 0 ] || [ "${MARADT_FEJLEC:-0}" != 0 ] || [ "${PHPKEZ:-0}" != 1 ] \
   || [ "${MERES:-0}" -eq 0 ] || [ "${SUTI:-0}" -lt "${MERES:-0}" ] \
   || { [ "$SITEMAP_VAN" = 1 ] && [ "${SITEMAP:-0}" != 1 ]; }; then
  piros "A _web_prod/ NEM élesíthető — a fenti ellenőrzés bukott."
  exit 1
fi

zold "Kész. Feltöltés élesbe:  scripts/feltoltes.sh eles --eles"
halk "(Előtte érdemes: scripts/feltoltes.sh eles — próbamenet, nem ír semmit.)"
