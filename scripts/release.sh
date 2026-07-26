#!/usr/bin/env bash
#
# release.sh — okotechhome-web2 (Test2) release helper
#
# Usage:
#   ./scripts/release.sh <X.YY.ZZ> [--dry-run]
#
# Version format: padded SemVer — MINOR and PATCH are always two digits.
#   valid:   0.01.01   0.02.00   0.10.03   1.00.00
#   invalid: 0.1.1     0.2.0     v0.02.00
#
# Steps:
#   1. validate the version string (padded format) and that it is greater than the current one
#   2. verify clean worktree on main
#   3. verify CHANGELOG.md has a section for the new version
#   4. write VERSION, commit as chore(release), create an annotated tag
#   5. print the push command (never pushes on its own)
#
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

VERSION_FILE="VERSION"
CHANGELOG_FILE="CHANGELOG.md"
MAIN_BRANCH="main"

red()  { printf '\033[31m%s\033[0m\n' "$*" >&2; }
grn()  { printf '\033[32m%s\033[0m\n' "$*"; }
ylw()  { printf '\033[33m%s\033[0m\n' "$*"; }
die()  { red "HIBA: $*"; exit 1; }

NEW_VERSION="${1:-}"
DRY_RUN=0
[[ "${2:-}" == "--dry-run" ]] && DRY_RUN=1

[[ -n "$NEW_VERSION" ]] || die "Add meg a verziót. Példa: ./scripts/release.sh 0.02.00 [--dry-run]"

# --- 1. version format (padded SemVer) --------------------------------------
[[ "$NEW_VERSION" =~ ^[0-9]+\.[0-9]{2}\.[0-9]{2}$ ]] \
  || die "Érvénytelen formátum: '$NEW_VERSION' (elvárt: X.YY.ZZ — a MINOR és PATCH két számjegy, pl. 0.02.00)"

CURRENT_VERSION="$(tr -d '[:space:]' < "$VERSION_FILE" 2>/dev/null || echo "0.00.00")"
[[ "$CURRENT_VERSION" =~ ^[0-9]+\.[0-9]{2}\.[0-9]{2}$ ]] \
  || die "A $VERSION_FILE tartalma nem feltöltött formátumú: '$CURRENT_VERSION'"

# Numeric comparison, field by field.
# The 10# base prefix is mandatory: without it bash reads 08/09 as invalid octal.
ver_key() {
  local IFS='.'
  read -r maj min pat <<< "$1"
  printf '%d %d %d' "$((10#$maj))" "$((10#$min))" "$((10#$pat))"
}
read -r CUR_MAJ CUR_MIN CUR_PAT <<< "$(ver_key "$CURRENT_VERSION")"
read -r NEW_MAJ NEW_MIN NEW_PAT <<< "$(ver_key "$NEW_VERSION")"

if (( NEW_MAJ < CUR_MAJ )) \
  || (( NEW_MAJ == CUR_MAJ && NEW_MIN < CUR_MIN )) \
  || (( NEW_MAJ == CUR_MAJ && NEW_MIN == CUR_MIN && NEW_PAT <= CUR_PAT )); then
  die "A megadott verzió ($NEW_VERSION) nem nagyobb a jelenleginél ($CURRENT_VERSION)."
fi

# --- 2. git preconditions ---------------------------------------------------
git rev-parse --is-inside-work-tree >/dev/null 2>&1 || die "Nem git repóban vagyunk."

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$BRANCH" != "$MAIN_BRANCH" ]]; then
  ylw "FIGYELEM: nem a(z) '$MAIN_BRANCH' ágon vagy, hanem '$BRANCH'."
  [[ $DRY_RUN -eq 1 ]] || die "Kiadás csak '$MAIN_BRANCH' ágról indítható."
fi

if [[ -n "$(git status --porcelain)" ]]; then
  git status --short >&2
  die "A munkakönyvtár nem tiszta. Commitold vagy stash-eld a változásokat."
fi

if git rev-parse "v$NEW_VERSION" >/dev/null 2>&1; then
  die "A 'v$NEW_VERSION' tag már létezik."
fi

# --- 3. changelog section ---------------------------------------------------
grep -qE "^## \[$NEW_VERSION\]" "$CHANGELOG_FILE" \
  || die "A $CHANGELOG_FILE nem tartalmaz '## [$NEW_VERSION]' szekciót. Írd meg előbb a naplót."

# one-line summary = first non-empty, non-heading line under the version heading
SUMMARY="$(awk -v ver="## \\[$NEW_VERSION\\]" '
  $0 ~ ver {found=1; next}
  found && /^## \[/ {exit}
  found && NF && $0 !~ /^#/ && $0 !~ /^>/ {print; exit}
' "$CHANGELOG_FILE" | sed 's/[*_`]//g' | cut -c1-100)"
[[ -n "$SUMMARY" ]] || SUMMARY="kiadás"

# --- 4. summary -------------------------------------------------------------
cat <<EOF

  Repó        : $REPO_ROOT
  Ág          : $BRANCH
  Jelenlegi   : $CURRENT_VERSION
  Új verzió   : $NEW_VERSION
  Tag         : v$NEW_VERSION
  Összefoglaló: $SUMMARY

EOF

if [[ $DRY_RUN -eq 1 ]]; then
  ylw "DRY RUN — semmi nem történt. Éles futtatáshoz hagyd el a --dry-run kapcsolót."
  exit 0
fi

# --- 5. execute -------------------------------------------------------------
echo "$NEW_VERSION" > "$VERSION_FILE"
git add "$VERSION_FILE" "$CHANGELOG_FILE"
git commit -m "chore(release): v$NEW_VERSION"
git tag -a "v$NEW_VERSION" -m "v$NEW_VERSION — $SUMMARY"

grn "Kész: v$NEW_VERSION létrehozva."
cat <<EOF

Következő lépés (kézzel, ellenőrzés után):

  git push origin $MAIN_BRANCH --follow-tags

EOF
