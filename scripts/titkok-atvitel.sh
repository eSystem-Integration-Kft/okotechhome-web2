#!/usr/bin/env bash
#
# titkok-atvitel.sh — a szervertitkok átvitele a tesztről az élesre.
# =============================================================================
# MI EZ ÉS MIÉRT KÜLÖN SZKRIPT
#
# A webhely három helyről vesz titkot, és EGYIK SINCS a verziókövetésben:
#
#   1. `api/config.php`          — SMTP-jelszó, címzettek, korlátok
#   2. `/oth-titkok/*.txt`       — AI-kulcs és CRM-tokenek, a WEBGYÖKÉR FÖLÖTT
#   3. környezeti változók       — ha valaki így adja meg (OTH_AI_KULCS stb.)
#
# A 2. pont a fiók HOME könyvtárában van, nem a `public_html`-ben — szándékosan:
# ami a webgyökéren kívül van, azt a kiszolgáló nem tudja kiszolgálni, akkor sem,
# ha egyszer elromlik a `.htaccess`.
#
# EZ A SZKRIPT A 2. PONTOT VISZI ÁT. A `config.php`-t nem: az már fent van.
#
# MIÉRT NEM A `feltoltes.sh` CSINÁLJA. Azt naponta futtatjuk; ez egyszeri,
# beállító lépés. Egy telepítőszkriptnek nem dolga titkot mozgatni — és ha
# mégis tenné, egy törlő tükrözés egyszer letörölné őket.
#
# ================================ FIGYELEM ==================================
# A `crm-db.txt` SZÁNDÉKOSAN KIMARAD. Az a HELYI MySQL hozzáférése
# (`127.0.0.1`, `okoth_web`) — az éles kiszolgálón ilyen adatbázis nincs, és
# ha átmásolnánk, az éles webhely egy nem létező (vagy ami rosszabb: a teszt)
# adatbázisra mutatna. Az éles CRM-naplóhoz ott kell adatbázist létrehozni, és
# a saját hozzáférését beírni. Amíg nincs, a CRM-napló csendben kimarad — a
# beküldések ettől még kimennek e-mailben.
# =============================================================================
#
# HASZNÁLAT
#     scripts/titkok-atvitel.sh                 # PRÓBA: megmutatja, mit vinne át
#     scripts/titkok-atvitel.sh --eles          # tényleges átvitel (terminálból)
#     scripts/titkok-atvitel.sh --eles --igen   # ha nincs billentyűzet (pl. `!` futtatás)
#
# A jelszavak a macOS kulcskarikájáról jönnek, ugyanonnan, ahonnan a
# `feltoltes.sh` veszi őket (`okoth.hu` és `okotechhome.hu` bejegyzés).
# =============================================================================
set -euo pipefail

GYOKER="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

piros() { printf '\033[31m%s\033[0m\n' "$*" >&2; }
zold()  { printf '\033[32m%s\033[0m\n' "$*"; }
sarga() { printf '\033[33m%s\033[0m\n' "$*"; }
halk()  { printf '\033[2m%s\033[0m\n' "$*"; }

ELES=0; IGEN=0
for k in "$@"; do
  case "$k" in
    --eles) ELES=1 ;;
    --igen) IGEN=1 ;;
    *) printf 'Ismeretlen kapcsoló: %s\n' "$k" >&2; exit 2 ;;
  esac
done

# A HORDOZHATÓ titkok. Az AI-kulcs ugyanaz az Anthropic-fiók, a CRM-tokenek
# ugyanahhoz a külső szolgáltatáshoz (dealkeeper.hu) tartoznak — mindkettő
# ugyanaz a két környezetben.
FAJLOK=(ai-kulcs crm-arsav crm-kapcsolat crm-konzultacio crm-megoldasajanlo crm-osszehasonlito)

command -v lftp >/dev/null || { piros "Nincs telepítve az lftp (brew install lftp)."; exit 1; }

kulcs() {  # $1 = kulcskarika-hoszt → "felhasznalo\njelszo"
  local h="$1" u p
  u=$(security find-internet-password -s "$h" 2>/dev/null | awk -F\" '/"acct"<blob>/{print $4}' | head -1 || true)
  [ -n "$u" ] || { piros "Nincs kulcskarika-bejegyzés a(z) $h hoszthoz."; exit 1; }
  p=$(security find-internet-password -s "$h" -a "$u" -w 2>/dev/null || true)
  [ -n "$p" ] || { piros "A jelszó nem olvasható ki ($h / $u)."; exit 1; }
  printf '%s\n%s\n' "$u" "$p"
}

{ read -r TU; read -r TP; } < <(kulcs okoth.hu)
{ read -r EU; read -r EP; } < <(kulcs okotechhome.hu)

echo
if [ "$ELES" = 1 ]; then
  sarga "╭─ TITKOK ÁTVITELE ───────────────────────────────────────────╮"
else
  zold  "╭─ PRÓBAMENET — semmi nem íródik ki ──────────────────────────╮"
fi
printf '  honnan ..... cullinan.versanus.eu:/oth-titkok   (%s)\n' "$TU"
printf '  hova ....... cpanel60.sybell.hu:/oth-titkok     (%s)\n' "$EU"
printf '  fájlok ..... %s\n' "${FAJLOK[*]}"
printf '  KIHAGYVA ... crm-db.txt (helyi MySQL — élesben saját hozzáférés kell)\n'
echo  "╰─────────────────────────────────────────────────────────────╯"
echo

if [ "$ELES" = 0 ]; then
  halk "Tényleges átvitel:  scripts/titkok-atvitel.sh --eles"
  exit 0
fi

# A MEGERŐSÍTÉS KÉTFÉLEKÉPPEN ADHATÓ MEG, mert a szkript nem mindig kap
# billentyűzetet. Terminálból kérdezünk; ha a bemenet nem terminál (a Claude
# Code `!` futtatása, cron, csővezeték), akkor a `--igen` kapcsoló a
# megerősítés. A `read` ilyenkor azonnal EOF-ot kapna, és `set -e` mellett
# csendben megölné a szkriptet — pontosan ez történt az első futtatáskor.
if [ -t 0 ]; then
  read -r -p "Biztosan átviszed? Írd be: igen — " valasz
  [ "$valasz" = "igen" ] || { sarga "Megszakítva."; exit 0; }
elif [ "$IGEN" != 1 ]; then
  piros "Nem interaktív futtatás — a megerősítés így a kapcsoló:"
  echo   "    scripts/titkok-atvitel.sh --eles --igen" >&2
  exit 1
fi

# A KÖZTES KÖNYVTÁR a felhasználó saját `mktemp`-je, 700-as jogosultsággal, és
# a szkript minden kilépési ágon törli — megszakításnál is.
TITOK="$(mktemp -d)"; chmod 700 "$TITOK"
trap 'rm -rf "$TITOK"' EXIT INT TERM

{ printf 'set ftp:ssl-allow true\nset ftp:ssl-force true\nset ftp:ssl-protect-data true\n'
  printf 'set ssl:verify-certificate true\nset ssl:ca-file "%s/scripts/ftps-ca.pem"\n' "$GYOKER"
  printf 'open -u "%s","%s" "ftp://cullinan.versanus.eu"\n' "$TU" "$TP"
  for f in "${FAJLOK[@]}"; do printf 'get /oth-titkok/%s.txt -o %s/%s.txt\n' "$f" "$TITOK" "$f"; done
  printf 'bye\n'
} | lftp 2>&1 | sed -E 's#(ftps?://[^:/@]+):[^@]*@#\1:***@#g'

echo "  letöltve:"
for f in "$TITOK"/*.txt; do
  printf '    %-26s %s bájt\n' "$(basename "$f")" "$(wc -c < "$f" | tr -d ' ')"
done

{ printf 'set ftp:ssl-allow true\nset ftp:ssl-force true\nset ftp:ssl-protect-data true\n'
  printf 'set ssl:verify-certificate true\nset ssl:ca-file "%s/scripts/ftps-ca-eles.pem"\n' "$GYOKER"
  printf 'open -u "%s","%s" "ftp://cpanel60.sybell.hu"\n' "$EU" "$EP"
  printf 'mkdir -p /oth-titkok\n'
  printf 'mput -O /oth-titkok %s/*.txt\n' "$TITOK"
  printf 'chmod 600 /oth-titkok/ai-kulcs.txt\n'
  printf 'chmod 700 /oth-titkok\n'
  printf 'cls -l /oth-titkok\n'
  printf 'bye\n'
} | lftp 2>&1 | sed -E 's#(ftps?://[^:/@]+):[^@]*@#\1:***@#g'

echo
zold "Kész. Ellenőrzés — az Ökónak válaszolnia kell:"
halk "  curl -s -X POST -H 'Content-Type: application/json' \\"
halk "    -H 'Origin: https://okotechhome.hu' \\"
halk "    --data '{\"kerdes\":\"Mikor nem megfelelő ez a rendszer?\"}' \\"
halk "    https://okotechhome.hu/api/kalauz.php"
halk "  → {\"ok\":true,…}   (ha {\"ok\":false,…}: api/hiba.log a szerveren)"
