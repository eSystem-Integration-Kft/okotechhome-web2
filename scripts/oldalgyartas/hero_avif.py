#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hero_avif.py — a fejlécképek AVIF-változata és a keskeny 750 px-es méret.

MIÉRT. A Search Console (valós látogatói adat, 2026-09-16): mobilon 100 URL
LCP-je 4 mp fölött, a csoport p75-e 4,5 mp. Az aloldalakon az LCP-elem a
fejléckép KESKENY változata — és ezek átlagosan 104 KB-osak, a legnehezebbek
~300 KB-osak (az ügyfél fotói: fű, föld, kavics — a WebP-nek drága textúra).

MIT CSINÁL.
  1. Minden `assets/img/oldalak/hero-*.webp` mellé AVIF-et kódol mind a három
     méretben, a keskenyhez pedig egy 750 px széles WebP + AVIF párt is — a
     2x-es kijelzőjű telefonoknak (≈375 px × 2) az 1100 px-es fölösleges.
  2. Csoportonként eldönti, megéri-e az AVIF (lásd DÖNTÉS) — ahol nem, törli.
  3. A lapok `<picture>` blokkjába és előtöltésébe beírja a 750-es jelöltet
     és a nyerő AVIF-forrásokat. A `<img>` érintetlen: ami AVIF-et nem ismer,
     a WebP-t kapja.

A FORRÁS A KIADOTT WEBP, nem az `alapkepek/` JPG-je. 24 fejlécet később az
ügyfél fotóira cseréltünk; a JPG-k azoknál elavultak. A kiadott WebP-ből
kódolva a kivágás garantáltan ugyanaz — csak a formátum és a méret változik.

MÉRETKERET, NEM FIX MINŐSÉG. A renderek AVIF-ben töredékükre mennek, a fotók
alig. Ezért képenként a LEGJOBB minőséget keressük, ami a keretbe fér, de van
alsó határ (MIN_Q), és a torzítás (ImageMagick SSIM-eltérés) nem lépheti túl a
MAX_ELTERES-t. Ha a keret csak rosszabb képpel tartható, a minőség nyer.
Mérve 2026-09-16-án: q58 kétszeres nagyításban sem különböztethető meg.

A kicsinyítés Mitchell-szűrővel — lásd designrendszer.md, „Méretre vágás".

FUTTATÁS:  python3 scripts/oldalgyartas/hero_avif.py [--csak-html] [--ujra]
  --csak-html  csak a lapok jelölése, a mentett döntés alapján
  --ujra       a korábban vesztesnek mért AVIF-et is újrakódolja és újramérni
Új fejlécképnél vagy a sablonból újragyártott lapnál futtasd le újra.
"""
import concurrent.futures as cf
import json
import pathlib
import re
import subprocess
import sys
import tempfile

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
OLDALAK = WEB / 'assets' / 'img' / 'oldalak'

MIN_Q = 44                 # ez alatt a fotók textúrája már láthatóan elkenődik
MAX_Q = 62
MAX_ELTERES = 0.035        # SSIM-eltérés (0 = azonos); q58 ≈ 0,018–0,021
KERET = {                  # bájt — a mobil LCP szempontjából ami számít
    'szuk-750': 70_000,
    'szuk': 120_000,
    '1024': 110_000,
    '': 200_000,
}


def fut(*parancs):
    return subprocess.run(parancs, capture_output=True, text=True, check=True).stdout


def elteres(eredeti: pathlib.Path, uj: pathlib.Path) -> float:
    k = subprocess.run(['magick', 'compare', '-metric', 'SSIM', str(eredeti), str(uj), 'null:'],
                       capture_output=True, text=True)
    m = re.search(r'\(([\d.eE+-]+)\)', k.stderr + k.stdout)
    return float(m.group(1)) if m else 1.0


def avif_kerettel(png: pathlib.Path, cel: pathlib.Path, keret: int) -> str:
    """A legjobb minőség, ami a keretbe fér — a minőségi korlátok között."""
    utolso = None
    for q in range(MAX_Q, MIN_Q - 1, -4):
        tmp = cel.with_name(f'{cel.stem}.q{q}.tmp.avif')   # lépcsőnként külön: az előzőt csak a siker után dobjuk
        subprocess.run(['avifenc', '-q', str(q), '-s', '4', '-j', '2', str(png), str(tmp)],
                       capture_output=True, check=True)
        e = elteres(png, tmp)
        if e > MAX_ELTERES:
            # Ennél rosszabb képet nem adunk ki: marad az előző (jobb) lépcső.
            tmp.unlink()
            break
        if utolso:
            utolso[0].unlink(missing_ok=True)
        utolso = (tmp, q, e)
        if tmp.stat().st_size <= keret:
            break
    if not utolso:
        raise RuntimeError(f'{cel.name}: már a q{MAX_Q} is túl nagy eltérést ad')
    utolso[0].rename(cel)
    return f'q{utolso[1]} {cel.stat().st_size // 1024} KB (eltérés {utolso[2]:.3f})'


def kepet_kodol(alap: str) -> list[str]:
    """Egy fejléckép összes változata. Kihagyja, ami frissebb a forrásánál, és
    az AVIF-et ott, ahol egy korábbi mérés szerint nem nyer (lásd DÖNTÉS)."""
    naplo = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        feladat = [('', f'{alap}.webp', None), ('1024', f'{alap}-1024.webp', None),
                   ('szuk', f'{alap}-szuk.webp', None), ('szuk-750', f'{alap}-szuk.webp', 750)]
        for kulcs, forras_nev, szel in feladat:
            forras = OLDALAK / forras_nev
            if not forras.exists():
                continue
            nev = f'{alap}-{kulcs}' if kulcs else alap
            cel_avif = OLDALAK / f'{nev}.avif'
            cel_webp = OLDALAK / f'{nev}.webp' if szel else None
            csoport = 'mobil' if kulcs.startswith('szuk') else 'asztali'
            kell_avif = UJRA or DONTES_MOST.get(alap, {}).get(csoport) is not False
            kesz = not kell_avif or (cel_avif.exists() and cel_avif.stat().st_mtime >= forras.stat().st_mtime)
            if kesz and (cel_webp is None or cel_webp.exists()):
                continue
            png = tmp / f'{nev}.png'
            if szel:
                fut('magick', str(forras), '-filter', 'Mitchell', '-resize', f'{szel}x', str(png))
                # A 750-es WebP ugyanabból a kicsinyítésből, a meglévőkkel egyező
                # beállítással — ami AVIF-et nem ismer, ezt kapja.
                fut('cwebp', '-q', '78', '-m', '6', '-quiet', str(png), '-o', str(cel_webp))
            else:
                fut('magick', str(forras), str(png))
            if kell_avif:
                naplo.append(f'{nev}.avif: ' + avif_kerettel(png, cel_avif, KERET[kulcs]))
    return naplo


# ------------------------------------------------------------ DÖNTÉS
# AZ AVIF NEM MINDENHOL NYER. Mérve 2026-09-16-án, azonos SSIM-eltérésnél: a
# renderek AVIF-ben 20–35%-kal kisebbek, a fű-föld-kavics fotók viszont
# NAGYOBBAK, mint a WebP (pl. hero-oldomedence 750 px: WebP 98 KB, AVIF 125 KB;
# a 4:2:0 mintavétel sem segít). Az átlag mobilon csak −7% lett volna, néhány
# lapon pedig több adat ment volna ki. Ezért csoportonként döntünk: az AVIF
# csak akkor kerül ki, ha a csoport MINDKÉT fájlja legalább 15%-kal kisebb a
# WebP-párjánál. A két csoport a `<picture>` két AVIF-forrása: a keskeny
# (750 + 1100 px) és a széles (1100 + 1800 px) — egymástól függetlenek.
# A vesztes AVIF-et töröljük, hogy ne menjen ki; a döntést a DONTES fájl őrzi,
# így újrafuttatáskor nem kódoljuk újra (`--ujra` felülírja).
KUSZOB = 0.85
CSOPORT = {'mobil': ('szuk-750', 'szuk'), 'asztali': ('1024', '')}
DONTES = pathlib.Path(__file__).with_name('hero_avif_dontes.json')


def fajl(alap: str, kulcs: str, kit: str) -> pathlib.Path:
    return OLDALAK / f'{alap}-{kulcs}.{kit}' if kulcs else OLDALAK / f'{alap}.{kit}'


def dontest_hoz(alapok: list[str]) -> dict:
    dontes = {}
    for alap in alapok:
        dontes[alap] = {}
        for cs, kulcsok in CSOPORT.items():
            parok = [(fajl(alap, k, 'webp'), fajl(alap, k, 'avif')) for k in kulcsok]
            nyer = all(w.exists() and a.exists() and a.stat().st_size <= KUSZOB * w.stat().st_size
                       for w, a in parok)
            if not nyer:
                for _, a in parok:
                    a.unlink(missing_ok=True)
            dontes[alap][cs] = nyer
    DONTES.write_text(json.dumps(dontes, ensure_ascii=False, indent=1, sort_keys=True) + '\n', encoding='utf-8')
    return dontes


def dontes_olvas() -> dict:
    return json.loads(DONTES.read_text(encoding='utf-8')) if DONTES.exists() else {}


# ---------------------------------------------------------------- HTML
# A lapok jelölését MINDIG ÚJRAÉPÍTJÜK a fájlokból, bármilyen korábbi alakból
# (a sablon egyszerű WebP-s alakjából, a régi egyforrásos alakból, vagy egy
# korábbi futás kimenetéből). Így a döntés változása és az újrafuttatás is
# ugyanazt adja, és a lap csak létező fájlra hivatkozhat — egy hiányzó
# `srcset`-jelölt törött képet ad, mert a böngésző nem lép tovább a WebP-re.
KEPBLOKK = re.compile(
    r'(?P<beh>[ \t]*)(?P<forrasok>(?:<source [^\n]*?assets/img/oldalak/hero-[a-z0-9-]+?-(?:szuk|1024)[^\n]*>\n[ \t]*)+)'
    r'<img src="(?P<p>(?:\.\./)*)assets/img/oldalak/(?P<k>hero-[a-z0-9-]+?)\.webp(?P<v>\?v=\d+)?"')

ELOTOLTES = re.compile(
    r'<link rel="preload" as="image"(?: fetchpriority="high")?(?: type="image/avif")?(?: media="\((?P<m>max-width: 1024px|min-width: 1025px)\)")? '
    r'href="(?P<p>(?:\.\./)*)assets/img/oldalak/(?P<k>hero-[a-z0-9-]+?)(?:-szuk)?\.(?:webp|avif)(?P<v>\?v=\d+)?"\n'
    r'(?P<beh>[ \t]*)imagesrcset="[^"\n]*"\n'
    r'[ \t]*imagesizes="100vw">')


def jeloltek(alap: str, cs: str, ut: str, v: str, kit: str = '') -> tuple[str, str, str]:
    """(kiterjesztés, srcset, alapértelmezett href) — a csoport létező fájljaiból.
    Kiterjesztés nélkül a döntés szerint: AVIF, ha a csoportban nyert."""
    kit = kit or ('avif' if DONTES_MOST.get(alap, {}).get(cs) else 'webp')
    if cs == 'mobil':
        sz = [(f'{ut}-szuk.{kit}{v}', '1100w')]
        if fajl(alap, 'szuk-750', kit).exists():
            sz.insert(0, (f'{ut}-szuk-750.{kit}{v}', '750w'))
        return kit, ', '.join(f'{a} {b}' for a, b in sz), f'{ut}-szuk.{kit}{v}'
    return kit, f'{ut}-1024.{kit}{v} 1100w, {ut}.{kit}{v} 1800w', f'{ut}.{kit}{v}'


def kepblokk(m: re.Match) -> str:
    b, p, k, v = m['beh'], m['p'], m['k'], m['v'] or ''
    if set(re.findall(r'oldalak/(hero-[a-z0-9-]+?)(?:-szuk-750|-szuk|-1024)?\.(?:webp|avif)', m['forrasok'])) != {k}:
        return m[0]                                   # idegen kép a forrásokban: nem nyúlunk hozzá
    h = re.search(r'height="(\d+)"', m['forrasok'])[1]
    ut = f'{p}assets/img/oldalak/{k}'
    _, mobil_webp, _ = jeloltek(k, 'mobil', ut, v, 'webp')
    sorok = []
    # A SORREND DÖNT: a böngésző az első illeszkedő `<source>`-ot veszi. Keskeny
    # AVIF, keskeny WebP, széles AVIF — a széles WebP maga az `<img>`.
    if DONTES_MOST.get(k, {}).get('mobil'):
        _, sz, _ = jeloltek(k, 'mobil', ut, v)
        sorok.append(f'<source media="(max-width: 1024px)" type="image/avif" srcset="{sz}" sizes="100vw" width="1100" height="{h}">')
    sorok.append(f'<source media="(max-width: 1024px)" srcset="{mobil_webp}" sizes="100vw" width="1100" height="{h}">')
    if DONTES_MOST.get(k, {}).get('asztali'):
        _, sz, _ = jeloltek(k, 'asztali', ut, v)
        # Méret nélkül: így az `<img>` saját width/height-ját örökli.
        sorok.append(f'<source type="image/avif" srcset="{sz}" sizes="100vw">')
    return ''.join(f'{b}{s}\n' for s in sorok) + f'{b}<img src="{ut}.webp{v}"'


def elotoltes(m: re.Match) -> str:
    # AZ ELŐTÖLTÉS IS. A lapok feje korábban média-feltétel nélkül előtöltötte
    # a SZÉLES WebP-t — mobilon is, ahol a `<picture>` a keskenyet rajzolja ki.
    # A telefon így letöltött egy soha nem mutatott képet is (átlag 71 KB) —
    # alacsony prioritással, de ugyanazon a mobilkapcsolaton osztozva.
    # Mérve 2026-09-16-án, mind a 139 aloldalon. Helyette két, szélességhez
    # kötött előtöltés: mindegyik eszköz csak azt tölti, amit ki is rajzol. Az
    # AVIF-es előtöltés `type`-ot kap: az AVIF-et nem ismerő böngésző kihagyja
    # (a `<picture>` WebP-je attól még jön). WebP-előtöltés nem kerülhet mellé,
    # mert az AVIF-es böngésző azt is letöltené.
    # A `fetchpriority="high"` KÖTELEZŐ: a képelőtöltés alapból alacsony
    # prioritású, és mivel most már ugyanazt a fájlt kéri, mint az `<img>`, a
    # kép ezt a kérést örökli — a Chrome a stíluslap megérkezéséig vissza is
    # tartja. Mérve 2026-09-16-án: a 750-es kép „Low" prioritással indult.
    p, k, v, b = m['p'], m['k'], m['v'] or '', m['beh']
    ut = f'{p}assets/img/oldalak/{k}'
    csoportok = {'max-width: 1024px': ['mobil'], 'min-width: 1025px': ['asztali'], None: ['mobil', 'asztali']}[m['m']]
    ki = []
    for cs in csoportok:
        kit, sz, href = jeloltek(k, cs, ut, v)
        tipus = ' type="image/avif"' if kit == 'avif' else ''
        media = '(max-width: 1024px)' if cs == 'mobil' else '(min-width: 1025px)'
        ki.append(f'<link rel="preload" as="image" fetchpriority="high"{tipus} media="{media}" href="{href}"\n'
                  f'{b}imagesrcset="{sz}"\n'
                  f'{b}imagesizes="100vw">')
    return '\n'.join(ki)


DONTES_MOST: dict = {}


def lapokat_atir() -> int:
    db = 0
    for f in sorted(WEB.rglob('*.html')):
        t = f.read_text(encoding='utf-8')
        u, n = KEPBLOKK.subn(kepblokk, t)
        u, n2 = ELOTOLTES.subn(elotoltes, u)
        if u == t:
            continue
        hianyzo = [x for x in re.findall(r'(?:\.\./)*assets/img/oldalak/(hero-[a-z0-9-]+\.(?:avif|webp))', u)
                   if not (OLDALAK / x).exists()]
        if hianyzo:
            print(f'  ! kihagyva, hiányzó kép: {f.relative_to(WEB)} → {sorted(set(hianyzo))[:3]}')
            continue
        f.write_text(u, encoding='utf-8')
        db += 1
    return db


UJRA = '--ujra' in sys.argv


def main() -> int:
    DONTES_MOST.update(dontes_olvas())
    if '--csak-html' not in sys.argv:
        alapok = sorted({re.sub(r'-(1024|szuk|szuk-750)$', '', p.stem) for p in OLDALAK.glob('hero-*.webp')})
        print(f'{len(alapok)} fejléckép kódolása…')
        with cf.ThreadPoolExecutor(max_workers=6) as ex:
            for sorok in ex.map(kepet_kodol, alapok):
                for s in sorok:
                    print('  ' + s)
        DONTES_MOST.clear()
        DONTES_MOST.update(dontest_hoz(alapok))
        for cs in CSOPORT:
            nyer = sorted(a for a, d in DONTES_MOST.items() if d[cs])
            print(f'AVIF {cs}: {len(nyer)}/{len(alapok)} fejlécnél nyer ({", ".join(a[5:] for a in nyer)})')
    print(f'átírt lap: {lapokat_atir()}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
