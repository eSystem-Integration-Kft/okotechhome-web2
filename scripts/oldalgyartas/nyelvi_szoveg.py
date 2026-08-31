# -*- coding: utf-8 -*-
"""Fordítás alkalmazása és a hátralévő szöveg kigyűjtése.

A webhelyen sok mondat ISMÉTLŐDIK a lapok között — szekciócímek, gombfeliratok,
visszatérő magyarázatok. Ezért a fordítások egy halmozódó szótárban gyűlnek
(`szotar.json`), és minden új lapra előbb az addig ismert párokat alkalmazzuk;
csak az marad kézi munka, ami tényleg új.

  alkalmaz <lap...>   a szótárból amit lehet, lecserél; kiírja, mi maradt
  marad <lap...>      csak jelentés: mi van még hátra, fordítás nélkül

A csere SZÓHATÁRRA fut: a magyar toldalékol, és egy rövid szó (`Ülepít`) egy
hosszabb belsejében is előfordul (`Ülepítő`) — a nyers csere ilyenkor csonka
képződményt gyárt. A párokat hosszúság szerint csökkenő sorrendben alkalmazzuk.
"""
import json, os, re, sys, textwrap

ITT = os.path.dirname(__file__)
WEB = os.path.normpath(os.path.join(ITT, '..', '..', '_web'))
SZOTAR_UT = os.path.join(ITT, 'szotar.json')
MAGYAR_BETU = 'a-záéíóöőúüűA-ZÁÉÍÓÖŐÚÜŰ'


def szotar() -> dict:
    if os.path.exists(SZOTAR_UT):
        return json.load(open(SZOTAR_UT, encoding='utf-8'))
    return {}


def ment(d: dict) -> None:
    json.dump(d, open(SZOTAR_UT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)


def csomok(fajl: str) -> list:
    """A lap fordítandó szövegcsomói és attribútumai, dokumentumsorrendben."""
    s = open(fajl, encoding='utf-8').read()
    t = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    t = re.sub(r'<script(?![^>]*ld\+json)[^>]*>.*?</script>', '', t, flags=re.S)
    ki = [x.strip() for x in re.findall(r'>([^<>]+)<', t)]
    ki += [m.group(2) for m in re.finditer(r'\b(alt|aria-label|title|placeholder)="([^"]+)"', t)]
    ki = [x for x in ki if x and re.search(r'[A-Za-zÁ-ű]{3,}', x)]
    return list(dict.fromkeys(ki))


def maradek(fajl: str, d: dict) -> list:
    """Ami a szótárból nem oldható meg — ezt kell még lefordítani.

    A mérce nem az „ékezetes-e", hanem hogy a csomó SZÓ SZERINT szerepel-e a
    magyar forráslapon: az ékezet nélküli magyar szavakat (`Folytatom`, `Nincs`)
    az ékezetszűrő átengedte, és bent maradtak a kész lapokon.
    """
    import nyelvek
    en_rel = os.path.relpath(fajl, os.path.join(WEB, 'en'))[:-5]
    hu_rel = {v: k for k, v in nyelvek.SZLUG.items()}.get(en_rel)
    hu_csomok = set(csomok(os.path.join(WEB, hu_rel + '.html'))) if hu_rel else set()
    return [c for c in csomok(fajl) if c in hu_csomok and c not in d]


def alkalmaz(fajl: str, d: dict) -> int:
    s = open(fajl, encoding='utf-8').read()
    n = 0
    for hu in sorted(d, key=len, reverse=True):
        if hu not in s:
            continue
        en = d[hu]
        if '\n' in hu:
            sorok = hu.split('\n')
            behuzas = re.match(r'\s*', sorok[1]).group(0) if len(sorok) > 1 else ''
            szel = max(len(l) for l in sorok)
            en = '\n'.join(textwrap.wrap(' '.join(en.split()), width=max(szel, 80),
                                         subsequent_indent=behuzas))
        uj, db = re.subn(re.escape(hu) + f'(?![{MAGYAR_BETU}])', lambda _: en, s)
        if db:
            s = uj; n += db
    open(fajl, 'w', encoding='utf-8').write(s)
    return n


if __name__ == '__main__':
    sys.path.insert(0, ITT)
    parancs, lapok = sys.argv[1], sys.argv[2:]
    d = szotar()
    for lap in lapok:
        f = lap if lap.endswith('.html') else os.path.join(WEB, 'en', lap + '.html')
        if parancs == 'alkalmaz':
            n = alkalmaz(f, d)
            m = maradek(f, d)
            print(f'{os.path.relpath(f, WEB):48s} {n:4d} csere, {len(m):3d} maradt')
        elif parancs == 'marad':
            m = maradek(f, d)
            print(f'--- {os.path.relpath(f, WEB)}  ({len(m)} csomó)')
            for x in m:
                print(json.dumps(x, ensure_ascii=False))
