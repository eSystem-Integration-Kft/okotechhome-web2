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
# A két lapfa gyökere. Alapértelmezésben a magyar repó elrendezése (`_web` és
# `_web/en`), így a szkriptek itt változatlanul futnak. Az angol webhely 2026.
# szeptemberében külön projektbe költözött (`_OkoTechHome2_EN/_webout`, ahol
# nincs `en/` szint), ezért mindkét gyökér felülírható:
#   OKOTH_HU_WEB=…/_OkoTechHome2/_web  OKOTH_EN_WEB=…/_OkoTechHome2_EN/_webout
HU_WEB = os.environ.get('OKOTH_HU_WEB') or os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', '..', '_web'))
EN_WEB = os.environ.get('OKOTH_EN_WEB') or os.path.join(HU_WEB, 'en')
SZOTAR_UT = os.path.join(ITT, 'szotar.json')
NEVEK_UT = os.path.join(ITT, 'nem_forditando.json')
MAGYAR_BETU = 'a-záéíóöőúüűA-ZÁÉÍÓÖŐÚÜŰ'


def szotar() -> dict:
    if os.path.exists(SZOTAR_UT):
        return json.load(open(SZOTAR_UT, encoding='utf-8'))
    return {}


def ment(d: dict) -> None:
    json.dump(d, open(SZOTAR_UT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)


NEVEK = set(json.load(open(NEVEK_UT, encoding='utf-8'))) if os.path.exists(NEVEK_UT) else set()


def csomok(fajl: str) -> list:
    """A lap fordítandó szövegcsomói és attribútumai, dokumentumsorrendben."""
    s = open(fajl, encoding='utf-8').read()
    t = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    t = re.sub(r'<script(?![^>]*ld\+json)[^>]*>.*?</script>', '', t, flags=re.S)
    ki = [x.strip() for x in re.findall(r'>([^<>]+)<', t)]
    ki += [m.group(2) for m in re.finditer(r'\b(alt|aria-label|title|placeholder)="([^"]+)"', t)]
    # a meta-leírás is látható szöveg — a keresőtalálatban és a megosztáskor.
    # A `content` attribútum viszont technikai értékeket is hordoz (charset,
    # viewport, robots), ezért csak a leíró meta-elemeket vesszük ide.
    ki += [m.group(1) for m in re.finditer(
        r'<meta[^>]*\b(?:name|property)="(?:description|og:(?:title|description)|twitter:(?:title|description))"[^>]*'
        r'content="([^"]+)"', t)]
    ki += [m.group(1) for m in re.finditer(
        r'<meta[^>]*content="([^"]+)"[^>]*\b(?:name|property)="(?:description|og:(?:title|description)|twitter:(?:title|description))"', t)]
    ki = [x for x in ki if x and re.search(r'[A-Za-zÁ-ű]{3,}', x)]
    return list(dict.fromkeys(ki))


def maradek(fajl: str, d: dict) -> list:
    """Ami a szótárból nem oldható meg — ezt kell még lefordítani.

    A mérce nem az „ékezetes-e", hanem hogy a csomó SZÓ SZERINT szerepel-e a
    magyar forráslapon: az ékezet nélküli magyar szavakat (`Folytatom`, `Nincs`)
    az ékezetszűrő átengedte, és bent maradtak a kész lapokon.
    """
    import nyelvek
    en_rel = os.path.relpath(fajl, EN_WEB)[:-5]
    hu_rel = {v: k for k, v in nyelvek.SZLUG.items()}.get(en_rel)
    hu_csomok = set(csomok(os.path.join(HU_WEB, hu_rel + '.html'))) if hu_rel else set()
    return [c for c in csomok(fajl)
            if c in hu_csomok and c not in d and not tulajdonnev(c)]


def tulajdonnev(c: str) -> bool:
    """Amin nincs mit fordítani: név, településnév, cím, entitás, szám.

    A mérce nem lehet a nagy kezdőbetű önmagában — `Nincs`, `Van`, `Vissza`
    valódi felirat, és pontosan ezek maradtak bent, amikor a szűrő ennél
    engedékenyebb volt. Ezért csak a TÖBB SZAVAS, végig nagybetűvel kezdődő
    csomót engedjük át magától; az egyszavú neveket névsor sorolja fel.
    """
    if c in NEVEK or '@' in c:
        return True
    if not re.search(r'[A-Za-zÁ-ű]', re.sub(r'&[a-z]+;', '', c)):
        return True                                   # entitás, szám, írásjel
    if re.match(r'^\d{4}\s+\S', c):
        return True                                   # magyar postai cím — nem fordul
    if re.match(r'^[A-Z0-9][A-Z0-9./-]*$', c):
        return True                                   # kód, azonosítóminta
    szavak = [w for w in re.findall(r"[A-Za-zÁ-ű.'-]+", c) if len(w) > 1]
    return len(szavak) > 1 and all(w[0].isupper() for w in szavak)


FORDITHATO_ATTR = ('alt', 'title', 'aria-label', 'placeholder', 'label', 'content')
URLSZERU = re.compile(r'^(?:[a-z]+:|[./#]|[\w./-]+\.(?:html|webp|png|svg|js|css|json)\b)')


def savok(s: str) -> list:
    """A fordítható tartományok a dokumentumban: [(kezd, veg), ...].

    Egy szótári pár csak akkor cserélhető, ha a találat EGÉSZE ilyen sávba esik.
    Ezen múlik, hogy az `href`-be, `id`-ba, osztálynévbe ne írjunk bele: a
    „vagy" → „or" pár egyszer már elrontotta a magyar szlugokat
    (`biologiai-rendszer-or-oldomedence`), és a hivatkozás némán eltört.
    """
    ki, mutato = [], 0
    tiltott = {}
    for m in re.finditer(r'<(script|style)\b[^>]*>', s, re.I):
        veg = s.lower().find('</' + m.group(1).lower(), m.end())
        tiltott[m.start()] = (veg if veg >= 0 else len(s), 'ld+json' in m.group(0))
    for m in re.finditer(r'<[^>]*>', s):
        if m.start() > mutato:
            ki.append((mutato, m.start()))              # szövegcsomó két tag között
        for a in re.finditer(r'\b([a-zA-Z-]+)="([^"]*)"', m.group(0)):
            if a.group(1).lower() in FORDITHATO_ATTR and not URLSZERU.match(a.group(2)):
                ki.append((m.start() + a.start(2), m.start() + a.end(2)))
        mutato = m.end()
    if mutato < len(s):
        ki.append((mutato, len(s)))
    # a script/style belseje kiesik — kivéve a ld+json, ahol a JSON értékei mennek
    for kezd, (veg, jsonld) in tiltott.items():
        ki = [(a, b) for a, b in ki if b <= kezd or a >= veg]
        if jsonld:
            for m in re.finditer(r':\s*"((?:[^"\\]|\\.)*)"', s[kezd:veg]):
                if not URLSZERU.match(m.group(1)):
                    ki.append((kezd + m.start(1), kezd + m.end(1)))
    return sorted(ki)


def alkalmaz(fajl: str, d: dict) -> int:
    """A szótári párok alkalmazása — SOHA nem mondat belsejébe.

    A cserét a fordítható sávok TELJES tartalmára illesztjük, nem részletre.
    A szótár minden kulcsa egy teljes szövegcsomóból származik (`csomok()`),
    tehát ez nem szűkítés, hanem a helyes illesztés. A részleges illesztés
    egyszer már mondatokat rontott el: a „nem" → „not" pár lefordítatlan magyar
    mondatokba is beleírt, a szóhatár hiánya miatt pedig a `hanem` szóból
    `hanot` lett. Egy csomó vagy lefordul egészében, vagy érintetlen marad és
    látszik a jelentésben.
    """
    s = open(fajl, encoding='utf-8').read()
    darabok, utolso, n = [], 0, 0
    for kezd, veg in savok(s):
        nyers = s[kezd:veg]
        mag = nyers.strip()
        if not mag or mag not in d:
            continue
        elol = nyers[:len(nyers) - len(nyers.lstrip())]
        hatul = nyers[len(nyers.rstrip()):]
        en = d[mag]
        if '\n' in mag:
            sorok = mag.split('\n')
            behuzas = re.match(r'\s*', sorok[1]).group(0) if len(sorok) > 1 else ''
            szel = max(len(l) for l in sorok)
            en = '\n'.join(textwrap.wrap(' '.join(en.split()), width=max(szel, 80),
                                          subsequent_indent=behuzas))
        darabok.append(s[utolso:kezd]); darabok.append(elol + en + hatul)
        utolso = veg; n += 1
    if n:
        darabok.append(s[utolso:])
        open(fajl, 'w', encoding='utf-8').write(''.join(darabok))
    return n


if __name__ == '__main__':
    sys.path.insert(0, ITT)
    parancs, lapok = sys.argv[1], sys.argv[2:]
    d = szotar()
    for lap in lapok:
        f = lap if lap.endswith('.html') else os.path.join(EN_WEB, lap + '.html')
        if parancs == 'alkalmaz':
            n = alkalmaz(f, d)
            m = maradek(f, d)
            print(f'{os.path.relpath(f, EN_WEB):48s} {n:4d} csere, {len(m):3d} maradt')
        elif parancs == 'marad':
            m = maradek(f, d)
            print(f'--- {os.path.relpath(f, EN_WEB)}  ({len(m)} csomó)')
            for x in m:
                print(json.dumps(x, ensure_ascii=False))
