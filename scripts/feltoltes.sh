#!/usr/bin/env bash
#
# feltoltes.sh — a `_web/` fa feltöltése a kiszolgálóra.
# =============================================================================
# HASZNÁLAT
#     scripts/feltoltes.sh tst              # PRÓBA: megmutatja, mi változna
#     scripts/feltoltes.sh tst --eles       # tényleges feltöltés a TESZTRE
#     scripts/feltoltes.sh eles --eles      # tényleges feltöltés az ÉLESRE
#     scripts/feltoltes.sh tst --eles --torol   # + a szerveren fölöslegessé vált fájlok törlése
#
# A MUNKAMENET: fejlesztés → `tst` → megnézzük a tst.okoth.hu-n → ha jó, `eles`.
# Két webhely, KÉT KÜLÖN KISZOLGÁLÓN, két külön fiókkal; egymást nem érintik,
# az élesítés nem szünteti meg a tesztoldalt.
#
# KÉT FA, EGY FORRÁS:
#     _web/       →  tst.okoth.hu     (itt fejlesztünk)
#     _web_prod/  →  okotechhome.hu   (a `_web/`-ből GENERÁLVA)
# A `_web_prod/`-ot a `scripts/prod-epit.sh` állítja elő; kézzel nem szerkesztjük.
#
# ALAPÉRTELMEZÉSBEN NEM ÍR SEMMIT. A `--eles` kapcsoló nélkül csak felsorolja,
# mit tenne. Ez nem óvatoskodás: egy elgépelt útvonal vagy egy rossz irányba
# fordított tükrözés percek alatt tesz tönkre egy működő webhelyet, és az FTP-n
# nincs visszavonás.
#
# A JELSZÓ NEM EBBEN A FÁJLBAN VAN, és nem is környezeti változóban, ahol a
# `ps` kilistázná. A macOS kulcskarikájából jön:
#
#     security add-internet-password -s okoth.hu        -a <FTP-felhasználó> -T /usr/bin/security -U -w
#     security add-internet-password -s okotechhome.hu -a <FTP-felhasználó> -T /usr/bin/security -U -w
#
# KÉT BEJEGYZÉS, mert két külön tárhely: a teszt a Versanus gépén
# (`cullinan.versanus.eu`), az éles a Sybellén (`cpanel60.sybell.hu`). A
# felhasználónév és a jelszó a kettőn NEM ugyanaz.
#
# (A `-w` után a parancs bekéri a jelszót, és nem írja ki a képernyőre. Ezt
# EGYSZER kell megtenni; a szkript onnantól magától olvassa.)
# =============================================================================
set -euo pipefail

GYOKER="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# A FORRÁSFÁT A KÖRNYEZET VÁLASZTJA MEG (lásd a környezettáblát lentebb):
# a teszt a `_web/`-ből megy ki, az éles a `_web_prod/`-ból.
HELYI=""

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
#
# HÁROM KÖRNYEZET, KÉT KISZOLGÁLÓ, KÉT FORRÁSFA.
#
#   tst    a fejlesztés vitrinje — a `_web/` megy ki rá.
#   okoth  az okoth.hu gyökere, UGYANAZON a tárhelyen a teszt fölött. Ritkán
#          kell; korábban ez futott `eles` néven, és a név félrevezetett.
#   eles   az ÉLES webhely: okotechhome.hu, MÁSIK tárhelyen (Sybell), másik
#          fiókkal — és a `_web_prod/` megy ki rá, nem a `_web/`.
#
# AZ ÉLES KAPCSOLÓDÁSI NEVE `cpanel60.sybell.hu`, nem a webhelyé. Ugyanaz a
# megfontolás, mint a tesztnél: a tárhely FTPS-tanúsítványa a KISZOLGÁLÓ nevére
# szól (`*.sybell.hu`, RapidSSL), a webhely nevével a névegyezés bukna el — az
# `ssl:verify-certificate true` pedig nem alku tárgya. Mérve 2026-09-11-én:
# Pure-FTPd TLS-sel a 21-es porton, a lánc a rendszer CA-készletéből hitelesül.
case "$KORNYEZET" in
  tst)   CIMKE="tst.okoth.hu";   KULCS="okoth.hu";       KAPCS="cullinan.versanus.eu"; TAVOLI="/public_html/_tst"; HELYI="$GYOKER/_web";      CA="ftps-ca.pem" ;;
  okoth) CIMKE="okoth.hu";       KULCS="okoth.hu";       KAPCS="cullinan.versanus.eu"; TAVOLI="/public_html";      HELYI="$GYOKER/_web";      CA="ftps-ca.pem" ;;
  eles)  CIMKE="okotechhome.hu"; KULCS="okotechhome.hu"; KAPCS="cpanel60.sybell.hu";   TAVOLI="/public_html";      HELYI="$GYOKER/_web_prod"; CA="ftps-ca-eles.pem" ;;
  *) cat >&2 <<'SUGO'
Használat: scripts/feltoltes.sh <tst|okoth|eles> [--eles] [--torol]

  tst      a tesztoldal — tst.okoth.hu        (forrás: _web/)
  okoth    az okoth.hu gyökere ugyanott       (forrás: _web/)
  eles     az ÉLES webhely — okotechhome.hu   (forrás: _web_prod/)

  --eles   TÉNYLEGESEN feltölt. Enélkül csak megmutatja, mi változna.
  --torol  a szerveren lévő, helyben már nem létező fájlokat is törli.
           Óvatosan: külön nézd meg előbb próbamenetben, mit sorol fel.

A munkamenet: fejlesztés → tst → megnézzük a tst.okoth.hu-n → ha jó:
    scripts/prod-epit.sh              # _web_prod/ felépítése a _web/-ből
    scripts/feltoltes.sh eles --eles  # és fel az élesre
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

# A TESZTOLDAL AZ okoth.hu ALATT LAKIK (`/public_html/_tst`). Helyben nincs
# `_tst` könyvtár, tehát egy törlő tükrözés első dolga volna letörölni a
# szerverről az egész tesztoldalt. Az ÉLES tárhelyen ilyen könyvtár nincs, ott
# ez a kizárás tárgytalan — de ártani sem árt, ha egyszer mégis lenne.
[ "$KORNYEZET" = okoth ] && KIZAR+=( --exclude '^_tst/' )
[ "$KORNYEZET" = eles ]  && KIZAR+=( --exclude '^_tst/' )

# A GENERÁLÁS NYOMAI nem mennek ki a kiszolgálóra: a `.epult` jelzőfájl és az
# olvass-el csak nekünk szól.
KIZAR+=( --exclude-glob '.epult' --exclude-glob 'OLVASSEL.txt' )

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
printf '  kapcsolat ........ ftps://%s — tanúsítvány ellenőrizve (%s)\n' "$KAPCS" "$CA"
printf '  felhasználó ...... %s\n'   "$FELHASZNALO"
printf '  forrás ........... %s\n'   "$HELYI"
printf '  törlés ........... %s\n'   "$([ "$TOROL" = 1 ] && echo 'IGEN — a szerveren fölösleges fájlok eltűnnek' || echo 'nem')"
echo  "╰─────────────────────────────────────────────────────────────╯"
echo

# --------------------------------------------------------- kapuk az éleshez
#
# AZ ÉLES FELTÖLTÉS A CÉG MŰKÖDŐ WEBHELYÉT ÍRJA FELÜL. A tesztnél egy elrontott
# menet bosszúság; itt az ügyfél nyilvános arca. Ezért három kapu áll előtte, és
# egyik sem kerülhető meg véletlenül.
if [ "$KORNYEZET" = eles ]; then
  # 1) VAN-E MIT FELTÖLTENI, és a `_web/`-ből épült-e a mostani állapot.
  #    A `prod-epit.sh --ellenoriz` mondja meg; ha elavult, ő maga írja ki, mi
  #    változott azóta.
  [ -d "$HELYI" ] || { piros "Nincs meg a _web_prod/ — futtasd: scripts/prod-epit.sh"; exit 1; }
  bash "$GYOKER/scripts/prod-epit.sh" --ellenoriz || exit 1

  # 2) TESZT ÜZEMMÓD NEM MEHET ÉLESBE. Egyetlen bennmaradt `noindex` elég
  #    ahhoz, hogy a Google kiejtse a lapot az indexből — és az visszaállítás
  #    után is hetekig tart, mire visszamászik. Ez a kapu olcsó, a hiba nem.
  # A `|| true` itt sem elhagyható: `pipefail` mellett a találat nélküli `grep`
  # bukottá tenné a csővezetéket, és a `set -e` megállítaná a szkriptet —
  # pontosan a jó esetben.
  MARADT=$( { grep -rlF 'content="noindex' "$HELYI" --include='*.html' 2>/dev/null || true; } | wc -l | tr -d ' ')
  FEJLEC=$(grep -c '^  Header always set X-Robots-Tag' "$HELYI/.htaccess" 2>/dev/null || true)
  if [ "$MARADT" != 0 ] || [ "${FEJLEC:-0}" != 0 ]; then
    piros "TESZT ÜZEMMÓD AKTÍV a _web_prod/-ban — az élesítés leállt."
    printf '  noindex meta ....... %s lapon\n' "$MARADT" >&2
    printf '  X-Robots-Tag sor ... %s\n' "${FEJLEC:-0}" >&2
    echo   "  Építsd újra: scripts/prod-epit.sh" >&2
    exit 1
  fi
fi

if [ "$ELES" = 1 ]; then
  if [ "$KORNYEZET" = eles ]; then
    # 3) A MEGERŐSÍTÉS A DOMAINT KÉRI, nem egy „igen"-t. Az „igen" reflexből
    #    leüthető; a domain nevét kiírni már döntés.
    piros "FIGYELEM: ez a CÉG ÉLES WEBHELYÉT írja felül ($CIMKE)."
    read -r -p "Erősítsd meg a domain nevével — " valasz
    [ "$valasz" = "$CIMKE" ] || { sarga "Megszakítva."; exit 0; }
  else
    read -r -p "Biztosan feltöltöd? Írd be: igen — " valasz
    [ "$valasz" = "igen" ] || { sarga "Megszakítva."; exit 0; }
  fi
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
# A BIZALMI HORGONY KÖRNYEZETENKÉNT MÁS, mert a két tárhely tanúsítványa két
# külön hitelesítőtől jön: a teszté Let's Encrypt, az élesé DigiCert. Egy közös
# fájllal az éles kapcsolat jogosan bukna el („unable to get local issuer
# certificate") — és a kettőt szándékosan nem olvasztjuk egybe, hogy mindkét
# kapcsolaton pontosan egy lánc legyen elfogadható.
# Részletek és újragenerálás: a két .pem fájl fejlécében.
set ssl:ca-file "$GYOKER/scripts/$CA"
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
