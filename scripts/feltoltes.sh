#!/usr/bin/env bash
#
# feltoltes.sh — a `_web/` fa feltöltése a kiszolgálóra.
# =============================================================================
# HASZNÁLAT
#     scripts/feltoltes.sh tst              # PRÓBA: megmutatja, mi változna
#     scripts/feltoltes.sh tst --eles       # tényleges feltöltés a tesztre
#     scripts/feltoltes.sh eles --eles      # tényleges feltöltés az élesre
#     scripts/feltoltes.sh tst --eles --torol   # + a szerveren fölöslegessé vált fájlok törlése
#
# ALAPÉRTELMEZÉSBEN NEM ÍR SEMMIT. A `--eles` kapcsoló nélkül csak felsorolja,
# mit tenne. Ez nem óvatoskodás: egy elgépelt útvonal vagy egy rossz irányba
# fordított tükrözés percek alatt tesz tönkre egy működő webhelyet, és az FTP-n
# nincs visszavonás.
#
# A JELSZÓ NEM EBBEN A FÁJLBAN VAN, és nem is környezeti változóban, ahol a
# `ps` kilistázná. A macOS kulcskarikájából jön:
#
#     security add-internet-password -s tst.okoth.hu -a <FTP-felhasználó> -w
#
# (A `-w` után a parancs bekéri a jelszót, és nem írja ki a képernyőre. Ezt
# EGYSZER kell megtenni; a szkript onnantól magától olvassa.)
# =============================================================================
set -euo pipefail

GYOKER="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HELYI="$GYOKER/_web"

piros() { printf '\033[31m%s\033[0m\n' "$*" >&2; }
zold()  { printf '\033[32m%s\033[0m\n' "$*"; }
sarga() { printf '\033[33m%s\033[0m\n' "$*"; }
halk()  { printf '\033[2m%s\033[0m\n' "$*"; }

# ---------------------------------------------------------------- paraméterek
KORNYEZET="${1:-}"; shift || true
ELES=0; TOROL=0
for k in "$@"; do
  case "$k" in
    --eles)  ELES=1 ;;
    --torol) TOROL=1 ;;
    *) piros "Ismeretlen kapcsoló: $k"; exit 2 ;;
  esac
done

case "$KORNYEZET" in
  tst)  HOSZT="tst.okoth.hu"; TAVOLI="/" ;;
  eles) HOSZT="okoth.hu";     TAVOLI="/" ;;
  *) cat >&2 <<'SUGO'
Használat: scripts/feltoltes.sh <tst|eles> [--eles] [--torol]

  tst      a tesztkiszolgáló (tst.okoth.hu)
  eles     az éles webhely (okoth.hu)

  --eles   TÉNYLEGESEN feltölt. Enélkül csak megmutatja, mi változna.
  --torol  a szerveren lévő, helyben már nem létező fájlokat is törli.
           Óvatosan: külön nézd meg előbb próbamenetben, mit sorol fel.
SUGO
     exit 2 ;;
esac

# ------------------------------------------------------------------ ellenőrzés
command -v lftp >/dev/null || { piros "Nincs telepítve az lftp (brew install lftp)."; exit 1; }
[ -d "$HELYI" ] || { piros "Nincs meg a _web könyvtár: $HELYI"; exit 1; }

# A felhasználónevet a kulcskarikán tárolt bejegyzés adja. Ha több is van a
# hoszthoz, a `-a` kapcsolóval kell megmondani, melyik kell.
# KÉT LÉPÉSBEN, nem egy behelyettesítésbe fészkelve. A macOS rendszer-bashe
# 3.2-es, és az a `${VAR:-$( … "…" … )}` alakot nem tudja értelmezni — a szkript
# néma szintaktikai hibával állt meg. A `|| true` szintén nem elhagyható: a
# `pipefail` mellett a „nincs ilyen bejegyzés” hibakódja megölné a szkriptet,
# MIELŐTT kiírná, hogyan kell beállítani.
FELHASZNALO="${OTH_FTP_USER:-}"
if [ -z "$FELHASZNALO" ]; then
  FELHASZNALO=$(security find-internet-password -s "$HOSZT" 2>/dev/null \
    | awk -F\" '/"acct"<blob>/{print $4}' | head -1 || true)
fi

if [ -z "$FELHASZNALO" ]; then
  piros "Nincs kulcskarika-bejegyzés a(z) $HOSZT hoszthoz."
  cat >&2 <<SUGO

  Egyszeri beállítás (a jelszót a parancs kéri be, nem írja ki):

      security add-internet-password -s $HOSZT -a <FTP-felhasználó> -w

SUGO
  exit 1
fi

JELSZO="$(security find-internet-password -s "$HOSZT" -a "$FELHASZNALO" -w 2>/dev/null || true)"
[ -n "$JELSZO" ] || { piros "A jelszó nem olvasható ki a kulcskarikából ($HOSZT / $FELHASZNALO)."; exit 1; }

# --------------------------------------------------------------------- kizárás
#
# AMIT SOHA NEM TÖLTÜNK FEL. Fejlesztői segédfájlok; a `.htaccess` a `.md`-t és
# a `.py`-t ugyan nem is szolgálná ki, de ami nincs ott, azt nem is kell védeni.
#
# AMIHEZ SOHA NEM NYÚLUNK A SZERVEREN. Ezek a fájlok NEM a repóban élnek, hanem
# ott keletkeznek: a `config.php` a titkokkal, a sebességkorlát állapota és a
# hibanapló. Törlő tükrözésnél egy hiányzó sor itt megsemmisítené a
# konfigurációt, és az egész API leállna.
#
KIZAR=(
  --exclude-glob 'README.md'
  --exclude-glob 'COMPONENTS.md'
  --exclude-glob '*.md'
  --exclude-glob 'serve.py'
  --exclude-glob '.router-dev.php'
  --exclude-glob '.DS_Store'
  --exclude-glob 'api/config.php'
  --exclude-glob 'api/hiba.log'
  --exclude      'api/\.ratelimit/'
  --exclude      'api/\.eredmenyek/'
)

TUKROZ_KAPCSOLOK=( --continue --parallel=4 --verbose=1 )
[ "$TOROL" = 1 ] && TUKROZ_KAPCSOLOK+=( --delete )
[ "$ELES"  = 0 ] && TUKROZ_KAPCSOLOK+=( --dry-run )

# ------------------------------------------------------------------- kiírás
echo
if [ "$ELES" = 1 ]; then
  sarga "╭─ ÉLES FELTÖLTÉS ────────────────────────────────────────────╮"
else
  zold  "╭─ PRÓBAMENET — semmi nem íródik ki ──────────────────────────╮"
fi
printf '  cél .............. %s%s\n' "$HOSZT" "$TAVOLI"
printf '  felhasználó ...... %s\n'   "$FELHASZNALO"
printf '  forrás ........... %s\n'   "$HELYI"
printf '  törlés ........... %s\n'   "$([ "$TOROL" = 1 ] && echo 'IGEN — a szerveren fölösleges fájlok eltűnnek' || echo 'nem')"
echo  "╰─────────────────────────────────────────────────────────────╯"
echo

if [ "$ELES" = 1 ]; then
  read -r -p "Biztosan feltöltöd? Írd be: igen — " valasz
  [ "$valasz" = "igen" ] || { sarga "Megszakítva."; exit 0; }
fi

# ------------------------------------------------------------------ feltöltés
#
# A jelszót a `set` paranccsal adjuk át az lftp-nek a saját szkriptjében, nem a
# parancssorban: a parancssor a `ps` kimenetében MINDENKI számára látszana a
# gépen. Az `-e` így is az lftp folyamatáé marad, de nem argumentumként.
#
lftp -u "$FELHASZNALO","$JELSZO" "ftp://$HOSZT" <<LFTP
set ftp:ssl-allow true
set ftp:ssl-force true
set ftp:ssl-protect-data true
set ssl:verify-certificate true
set net:max-retries 3
set net:timeout 20
set xfer:clobber on
mirror --reverse ${TUKROZ_KAPCSOLOK[@]} ${KIZAR[@]} "$HELYI" "$TAVOLI"
bye
LFTP

echo
if [ "$ELES" = 1 ]; then
  zold "Kész. A böngészőben CTRL+SHIFT+R a gyorsítótár megkerüléséhez."
else
  halk "Ez próbamenet volt. Tényleges feltöltés:  scripts/feltoltes.sh $KORNYEZET --eles"
fi
