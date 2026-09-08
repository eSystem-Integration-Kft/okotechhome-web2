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
#     security add-internet-password -s okoth.hu -a <FTP-felhasználó> -T /usr/bin/security -U -w
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

# HÁROM NÉV, három szerep — és ez nem szőrszálhasogatás, mert mind a három más:
#
#   CIMKE  a webhely neve, ahogy a böngészőben látszik. Csak kiírjuk.
#   KULCS  ezen a néven áll a kulcskarikán az FTP-hozzáférés. A teszt és az éles
#          UGYANAZON a tárhelyen, ugyanazzal a hozzáféréssel él, ezért mindkettő
#          `okoth.hu` — egy jelszó, egy bejegyzés.
#   KAPCS  amire ténylegesen csatlakozunk. A tárhely FTPS-tanúsítványa a
#          KISZOLGÁLÓ saját nevére szól (`cullinan.versanus.eu`), nem a
#          webhelyére; a webhely nevével a névegyezés bukna el. Az
#          `ssl:verify-certificate true` pedig nem alku tárgya: nélküle a
#          kapcsolat közbeékelhető, az FTP-jelszóval együtt.
#
# AZ FTP-GYÖKÉR NEM A WEBHELY GYÖKERE. A bejelentkezés a cPanel-fiók HOME
# könyvtárába érkezik (`.bashrc`, `mail/`, `logs/`, `etc/`…); a kiszolgált
# tartalom a `public_html` alatt van. A tesztoldal pedig ennek alkönyvtára:
# tst.okoth.hu = okoth.hu/_tst = `/public_html/_tst`. Egy `/`-re állított
# tükrözés a fiók home-jába szórná szét a webhelyet.
#
# Az éles tükrözés ezért is ZÁRJA KI a `_tst` könyvtárat: helyben nem létezik,
# tehát egy törlő menet első dolga volna letörölni az egész tesztoldalt.
#
# Új kiszolgálóra költözéskor a KAPCS és a TAVOLI írandó át (a cPanel/Plesk
# elrendezése más lehet) — egyszeri használatra ott az `OTH_FTP_KAPCS`.
case "$KORNYEZET" in
  tst)  CIMKE="tst.okoth.hu"; KULCS="okoth.hu"; KAPCS="cullinan.versanus.eu"; TAVOLI="/public_html/_tst" ;;
  eles) CIMKE="okoth.hu";     KULCS="okoth.hu"; KAPCS="cullinan.versanus.eu"; TAVOLI="/public_html" ;;
  *) cat >&2 <<'SUGO'
Használat: scripts/feltoltes.sh <tst|eles> [--eles] [--torol]

  tst      a tesztoldal (tst.okoth.hu = okoth.hu/_tst)
  eles     az éles webhely (okoth.hu gyökere)

  --eles   TÉNYLEGESEN feltölt. Enélkül csak megmutatja, mi változna.
  --torol  a szerveren lévő, helyben már nem létező fájlokat is törli.
           Óvatosan: külön nézd meg előbb próbamenetben, mit sorol fel.
SUGO
     exit 2 ;;
esac

# ------------------------------------------------------------------ ellenőrzés
KAPCS="${OTH_FTP_KAPCS:-$KAPCS}"

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
  FELHASZNALO=$(security find-internet-password -s "$KULCS" 2>/dev/null \
    | awk -F\" '/"acct"<blob>/{print $4}' | head -1 || true)
fi

if [ -z "$FELHASZNALO" ]; then
  piros "Nincs kulcskarika-bejegyzés a(z) $KULCS hoszthoz."
  cat >&2 <<SUGO

  Egyszeri beállítás (a jelszót a parancs kéri be, nem írja ki):

      security add-internet-password -s $KULCS -a <FTP-felhasználó> -T /usr/bin/security -U -w

SUGO
  exit 1
fi

JELSZO="$(security find-internet-password -s "$KULCS" -a "$FELHASZNALO" -w 2>/dev/null || true)"
[ -n "$JELSZO" ] || { piros "A jelszó nem olvasható ki a kulcskarikából ($KULCS / $FELHASZNALO)."; exit 1; }

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
  # A TÁRHELY SAJÁT FÁJLJAI a webkönyvtárban. Nem a repóból származnak, a
  # cPanel teszi és tartja karban őket; törlő tükrözésnél viszont „fölösleges"
  # fájlnak látszanának. A `.well-known` a tanúsítvány-megújítás munkaterülete:
  # ha eltűnik, a Let's Encrypt-megújítás bukik.
  --exclude-glob '.user.ini'
  --exclude-glob 'php.ini'
  --exclude      '^cgi-bin/'
  --exclude      '^\.well-known/'
  # Csak a szerveren élő tartalom: a régi sitemap és a képtár. Amíg nem kerül
  # be a repóba, a tükrözés nem takaríthatja el.
  --exclude-glob 'sitemap.html'
  --exclude      '^_pic/'
)

# A TESZTOLDAL AZ ÉLES ALATT LAKIK. Helyben nincs `_tst` könyvtár, tehát egy
# törlő tükrözés első dolga volna letörölni a szerverről az egész tesztoldalt.
[ "$KORNYEZET" = eles ] && KIZAR+=( --exclude '^_tst/' )

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
printf '  cél .............. %s  (%s%s)\n' "$CIMKE" "$KAPCS" "$TAVOLI"
printf '  kapcsolat ........ ftps://%s — tanúsítvány ellenőrizve\n' "$KAPCS"
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
# A jelszót az `open -u` kapja meg az lftp SAJÁT szkriptjében (a here-docból),
# nem a parancssorban: a parancssori argumentum a `ps` kimenetében a gép minden
# felhasználója számára látszana.
#
# A KIMENETET KITAKARJUK. Az lftp a műveleteket teljes URL-lel írja ki, és abban
# benne van a `felhasznalo:jelszo@` rész is — próbamenetben minden sorban. Ami a
# képernyőre kerül, az naplóba, képernyőképre és beillesztett hibajelentésbe is
# kerül; a jelszó egyikbe se való.
lftp <<LFTP 2>&1 | sed -E 's#(ftps?://[^:/@]+):[^@]*@#\1:***@#g'
set ftp:ssl-allow true
set ftp:ssl-force true
set ftp:ssl-protect-data true
set ssl:verify-certificate true
# A kiszolgáló csak a saját tanúsítványát küldi, a köztes elemeket nem — azok
# innen jönnek. Részletek és újragenerálás: scripts/ftps-ca.pem fejléce.
set ssl:ca-file "$GYOKER/scripts/ftps-ca.pem"
set net:max-retries 3
set net:timeout 20
set xfer:clobber on
# A `pwd` és a bőbeszédű állapotkiírás a JELSZÓT IS kiírná (lftp az URL-t
# felhasználó:jelszó alakban mutatja) — ezért nincs itt egyik sem.
open -u "$FELHASZNALO","$JELSZO" "ftp://$KAPCS"
mirror --reverse ${TUKROZ_KAPCSOLOK[@]} ${KIZAR[@]} "$HELYI" "$TAVOLI"
bye
LFTP


echo
if [ "$ELES" = 1 ]; then
  zold "Kész. A böngészőben CTRL+SHIFT+R a gyorsítótár megkerüléséhez."
else
  halk "Ez próbamenet volt. Tényleges feltöltés:  scripts/feltoltes.sh $KORNYEZET --eles"
fi
