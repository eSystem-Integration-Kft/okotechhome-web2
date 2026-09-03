# -*- coding: utf-8 -*-
"""Magyar szómaradvány keresése az idegen nyelvű fában.

A fordítási jelentés (`nyelvi_szoveg.py marad`) CSOMÓRA dolgozik: egy szövegcsomó
akkor jelenik meg, ha SZÓ SZERINT szerepel a magyar forráslapon. Ez két esetet
nem lát meg:

  · a részlegesen lefordított csomót — a mondat angol, de egy szó bent maradt
    („retention period: 8 év”);
  · a három betűnél rövidebb szót, amit a csomószűrő eleve kidobott („8 év”).

Ez a szűrő ezért SZÓRA dolgozik: a látható szöveget tokenekre bontja, és
magyarnak jelöl mindent, ami ékezetes vagy szerepel a magyar szótövek között.
"""
import json, os, re, sys, collections

ITT = os.path.dirname(__file__)
# A két lapfa gyökere. Alapértelmezésben a magyar repó elrendezése (`_web` és
# `_web/en`), így a szkriptek itt változatlanul futnak. Az angol webhely 2026.
# szeptemberében külön projektbe költözött (`_OkoTechHome2_EN/_webout`, ahol
# nincs `en/` szint), ezért mindkét gyökér felülírható:
#   OKOTH_HU_WEB=…/_OkoTechHome2/_web  OKOTH_EN_WEB=…/_OkoTechHome2_EN/_webout
HU_WEB = os.environ.get('OKOTH_HU_WEB') or os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', '..', '_web'))
EN_WEB = os.environ.get('OKOTH_EN_WEB') or os.path.join(HU_WEB, 'en')
EKEZET = 'áéíóöőúüűÁÉÍÓÖŐÚÜŰ'

# ékezet nélküli, de egyértelműen magyar szavak. Ami angolul is szó — `mind`,
# `sor`, `part` — nem kerülhet ide: téves találatot adna a kész angol szövegen. — a ragozott alakokat a
# szótő-illesztés fogja meg (`nap`, `napja`, `napig`)
MAGYAR_TOVEK = """
 ev evek evet evig evre honap honapok het hetek nap napok napig ora orak perc
 fo fok db darab forint ezer millio szaz tobb kevesebb legalabb legfeljebb
 van nincs vannak nincsenek volt lesz lehet kell kellett szukseges
 igen nem talan vagy es de ha akkor mert hogy amely amelyek ami amit
 ez az ezek azok itt ott ilyen olyan minden csak meg mar
 elso masodik harmadik negyedik otodik
 vissza tovabb kovetkezo elozo bezar megse rendben mentes torles
 szempont weboldal alacsony magas teljes reszleges folytatom
 telek talaj viz haz rendszer berendezes tartaly szennyviz kut mezo
 """.split()

NEVEK_UT = os.path.join(ITT, 'nem_forditando.json')
NEVEK = {n.lower() for n in json.load(open(NEVEK_UT, encoding='utf-8'))} if os.path.exists(NEVEK_UT) else set()
# angolban is helyes, vagy tulajdonnév része — ezekre nem jelzünk
KIVETEL = {
    'okotech', 'okotechhome', 'epureco', 'graf', 'vituki', 'construma', 'ce', 'en',
    'clear', 'hu', 'magyar', 'esztergom', 'strazsa', 'komarom', 'budapest',
    'csikvand', 'diosbereny', 'obudavar', 'bakonypeterd', 'kesztolc', 'alsonemedi',
    'laktanya', 'arpad', 'mikszath', 'gls', 'europa', 'kapcsolat', 'okotech-home',
}


def ekezettelen(sz: str) -> str:
    tab = str.maketrans('áéíóöőúüűÁÉÍÓÖŐÚÜŰ', 'aeiooouuuAEIOOOUUU')
    return sz.translate(tab)


def latszo_szoveg(fajl: str) -> list:
    """(szöveg, sor) párok: a lapon ténylegesen megjelenő szöveg."""
    s = open(fajl, encoding='utf-8').read()
    s = re.sub(r'<!--.*?-->', lambda m: '\n' * m.group(0).count('\n'), s, flags=re.S)
    s = re.sub(r'<(script|style)\b[^>]*>.*?</\1>',
               lambda m: '\n' * m.group(0).count('\n'), s, flags=re.S | re.I)
    ki = []
    for m in re.finditer(r'>([^<>]+)<', s):
        ki.append((m.group(1), s.count('\n', 0, m.start()) + 1))
    for m in re.finditer(r'\b(alt|aria-label|title|placeholder|content)="([^"]+)"', s):
        ki.append((m.group(2), s.count('\n', 0, m.start()) + 1))
    return ki


def magyar_szavak(fajl: str) -> list:
    talalat = []
    for szoveg, sor in latszo_szoveg(fajl):
        for m in re.finditer(r"[A-Za-z" + EKEZET + r"][A-Za-z" + EKEZET + r"'-]*", szoveg):
            sz = m.group(0)
            kicsi = sz.lower()
            if kicsi in KIVETEL or kicsi in NEVEK:
                continue
            if any(c in EKEZET for c in sz):
                talalat.append((sor, sz, szoveg.strip()[:90]))
            elif ekezettelen(kicsi) in MAGYAR_TOVEK and len(sz) > 1:
                talalat.append((sor, sz, szoveg.strip()[:90]))
    return talalat


if __name__ == '__main__':
    minta = sys.argv[1] if len(sys.argv) > 1 else ''
    import glob
    ossz = collections.Counter()
    lapok = 0
    for f in sorted(glob.glob(os.path.join(EN_WEB, minta, '**', '*.html'), recursive=True)):
        t = magyar_szavak(f)
        if not t:
            continue
        lapok += 1
        print(f'--- {os.path.relpath(f, EN_WEB)}  ({len(t)} találat)')
        for sor, sz, kontextus in t[:12]:
            print(f'   {sor:5d}  {sz:22s} {kontextus}')
        if len(t) > 12:
            print(f'   … és további {len(t) - 12}')
        ossz.update(sz for _, sz, _ in t)
    print(f'\n{lapok} lapon {sum(ossz.values())} magyar szómaradvány, {len(ossz)} féle')
    for sz, n in ossz.most_common(30):
        print(f'   {n:5d}× {sz}')
