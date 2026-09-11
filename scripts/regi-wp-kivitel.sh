#!/usr/bin/env bash
#
# regi-wp-kivitel.sh — a régi WordPress kivitele a webgyökér alól.
# =============================================================================
# MIÉRT KELL EZ
#
# Az élesítéskor a régi webhely a `/public_html/__old/` alá került. Ott viszont
# a WEBGYÖKÉR ALATT van, és mérve NEM volt elzárva, csak „nem látszott":
#
#     /__old/xmlrpc.php ................ 200   ← lefutott
#     /__old/wp-includes/version.php ... 200   ← lefutott
#     /__old/index.php ................. 500   ← lefutott, csak hibára
#     /__old/wp-config.php ............. 500   ← a PHP értelmezte
#
# Az 500 nem védelem: azt jelenti, hogy a PHP ELINDULT, és a régi WordPress
# csak a 8.2-t nem bírja. Egy PHP-verzió visszaállítás máris élő, évek óta nem
# frissített WordPresst adna vissza — nyilvános `wp-login.php`-val és
# `xmlrpc.php`-val, amit jelszótöréshez és pingback-erősítéshez tömegesen
# szondáznak. A fában ezen felül ott van:
#
#     wp-config.php ....... az adatbázis hozzáférése
#     mentesek/ ........... mentések
#     hirlevel/ ........... `drwxrwxrwx` — MINDENKI ÁLTAL ÍRHATÓ
#     get_azon.php · google-geolocation-save.php · update_erd_date.php
#
# A `_web/.htaccess` már 404-et ad mindenre, ami `/__old/` alá esik. Ez viszont
# NEM HÉZAGMENTES: amíg a könyvtár a webgyökér alatt van, az Apache beolvassa a
# SAJÁT `.htaccess`-ét, és ezt `.htaccess` szintjéről nem lehet megtiltani
# (`AllowOverride None` kellene a kiszolgálókonfigban). Mérhető jele is van: a
# `/__old/readme.html` 301-et ad, és a célban ott a kiszolgáló abszolút
# útvonala — vagyis abban a könyvtárban még dől el valami.
#
# AMIT EZ A SZKRIPT CSINÁL: EGYETLEN ÁTNEVEZÉS.
#
#     /public_html/__old  →  /__old-wordpress-archivum
#
# A cél a fiók HOME könyvtára, oda, ahol az `oth-titkok` is van — a webgyökéren
# KÍVÜL. Onnan a kiszolgáló nem tud kiszolgálni semmit, akkor sem, ha egyszer
# elromlik egy `.htaccess`. Semmi nem törlődik, minden fájl megmarad, FTP-n
# ugyanúgy elérhető.
#
# VISSZAFORDÍTÁS (ha mégis kell): ugyanez fordítva, FTP-kliensből vagy a cPanel
# Fájlkezelőjéből — nevezd vissza a `/__old-wordpress-archivum`-ot
# `/public_html/__old`-ra.
#
# HASZNÁLAT
#     scripts/regi-wp-kivitel.sh                # PRÓBA: megmutatja, mit tenne
#     scripts/regi-wp-kivitel.sh --eles         # tényleges mozgatás (terminálból)
#     scripts/regi-wp-kivitel.sh --eles --igen  # ha nincs billentyűzet (`!` futtatás)
# =============================================================================
set -euo pipefail

GYOKER="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

piros() { printf '\033[31m%s\033[0m\n' "$*" >&2; }
zold()  { printf '\033[32m%s\033[0m\n' "$*"; }
sarga() { printf '\033[33m%s\033[0m\n' "$*"; }
halk()  { printf '\033[2m%s\033[0m\n' "$*"; }

HONNAN="/public_html/__old"
HOVA="/__old-wordpress-archivum"

ELES=0; IGEN=0
for k in "$@"; do
  case "$k" in
    --eles) ELES=1 ;;
    --igen) IGEN=1 ;;
    *) piros "Ismeretlen kapcsoló: $k"; exit 2 ;;
  esac
done

command -v lftp >/dev/null || { piros "Nincs telepítve az lftp (brew install lftp)."; exit 1; }

U=$(security find-internet-password -s okotechhome.hu 2>/dev/null | awk -F\" '/"acct"<blob>/{print $4}' | head -1 || true)
[ -n "$U" ] || { piros "Nincs kulcskarika-bejegyzés az okotechhome.hu hoszthoz."; exit 1; }
P=$(security find-internet-password -s okotechhome.hu -a "$U" -w 2>/dev/null || true)
[ -n "$P" ] || { piros "A jelszó nem olvasható ki."; exit 1; }

echo
sarga "╭─ A RÉGI WORDPRESS KIVITELE A WEBGYÖKÉR ALÓL ────────────────╮"
printf '  kiszolgáló . cpanel60.sybell.hu   (%s)\n' "$U"
printf '  honnan ..... %s\n' "$HONNAN"
printf '  hova ....... %s   (a HOME-ban, a webgyökéren kívül)\n' "$HOVA"
printf '  művelet .... átnevezés — semmi nem törlődik\n'
echo  "╰─────────────────────────────────────────────────────────────╯"
echo

if [ "$ELES" = 0 ]; then
  halk "Tényleges mozgatás:  scripts/regi-wp-kivitel.sh --eles"
  exit 0
fi

# Megerősítés — billentyűzet nélkül a kapcsoló, lásd feltoltes.sh.
if [ -t 0 ]; then
  read -r -p "Biztosan mozgatod? Írd be: igen — " valasz
  [ "$valasz" = "igen" ] || { sarga "Megszakítva."; exit 0; }
elif [ "$IGEN" != 1 ]; then
  piros "Nem interaktív futtatás — a megerősítés így a kapcsoló:"
  echo   "    scripts/regi-wp-kivitel.sh --eles --igen" >&2
  exit 1
fi

{ printf 'set ftp:ssl-allow true\nset ftp:ssl-force true\nset ftp:ssl-protect-data true\n'
  printf 'set ssl:verify-certificate true\nset ssl:ca-file "%s/scripts/ftps-ca-eles.pem"\n' "$GYOKER"
  printf 'open -u "%s","%s" "ftp://cpanel60.sybell.hu"\n' "$U" "$P"
  printf 'mv %s %s\n' "$HONNAN" "$HOVA"
  printf 'echo "--- a HOME-ban (ide került) ---"\n'
  printf 'cls -l / | grep -i archivum\n'
  printf 'echo "--- a public_html alatt (üres sor = már nincs ott) ---"\n'
  printf 'cls -l /public_html | grep -i "__old" || true\n'
  printf 'bye\n'
} | lftp 2>&1 | sed -E 's#(ftps?://[^:/@]+):[^@]*@#\1:***@#g'

echo
zold "Kész. Ellenőrzés — mindegyiknek 404-nek kell lennie:"
for u in "__old/" "__old/wp-config.php" "__old/xmlrpc.php" "__old/readme.html" "__old/.htaccess"; do
  printf '  %-28s %s\n' "/$u" \
    "$(curl -s -o /dev/null -w '%{http_code}' -m 15 "https://okotechhome.hu/$u" || echo '—')"
done
echo
halk "És a webhely maga:"
printf '  %-28s %s\n' "/" "$(curl -s -o /dev/null -w '%{http_code}' -m 15 https://okotechhome.hu/ || echo '—')"
