#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""llms.txt — belépő az AI-keresőknek.

MI EZ. Egy gyökérben álló, Markdown formátumú fájl, amit az AI-keresők
(ChatGPT Search, Perplexity, Claude, Gemini) használnak arra, hogy egy
lapon átlássák, MIRŐL SZÓL a webhely, és HOL vannak a lényegi lapjai. A
`sitemap.xml` a gépnek sorolja fel az URL-eket; az `llms.txt` a modellnek
magyarázza el a szerkezetet.

FELTÖREKVŐ SZABVÁNY, nem kötelező. Olcsó viszont, és pontosan azt a hiányt
tölti be, amivel az AI-keresők küzdenek: a webhely 184 lapjából melyik ötven
mond valami újat, és milyen kérdésre.

MIÉRT GENERÁLT. Mert a lapok címe és bevezetője a HTML-ben él, és ha kézzel
másolnánk át, az első átfogalmazásnál elcsúszna. Itt a `<title>`-ből és a
`meta description`-ből dolgozunk — abból, amit a kereső amúgy is lát.

MIT SOROL FEL. A hat tartalmi szakasz MINDEN indexelhető lapját, egy soros
leírással, plusz az öt gyökérszintű belépőt — összesen 178 hivatkozást, ~55 KB.
Ez tudatosan több, mint amit az `llms.txt` bevett gyakorlata (rövid, válogatott
lista) javasol: a tartalom itt nem marketinganyag, hanem műszaki válaszgyűjtemény,
és egy AI-keresőnek épp az segít, ha látja, MELYIK lap melyik kérdésre felel.
A címeket és a leírásokat a lapok `<title>`-jéből és `meta description`-jéből
vesszük — abból, amit a kereső amúgy is lát —, tehát nem tud elcsúszni tőlük.

Ami KIMARAD: a hibaoldalak, a `noindex` lapok, az `api/`, az `assets/` és az
`oth-titkok/`.

FUTTATÁS:  a `prod-epit.sh` hívja, az éles fára.
"""
import html
import pathlib
import re
import sys

GYOKER = pathlib.Path(__file__).resolve().parents[2]
DOMAIN = 'https://okotechhome.hu'

# A felsorolt szakaszok, sorrendben. A cím a miénk (az `llms.txt` szerkezete
# a mi állításunk), a lapok listája a fájlrendszerből jön.
SZAKASZOK = [
    ('Kiindulópont — melyik helyzetben mit érdemes nézni', 'helyzetem'),
    ('Megoldások és technológiák', 'megoldasok'),
    ('Projekt-előkészítés — telek, terhelés, engedély', 'projekt-elokeszites'),
    ('Tudástár — szakmai válaszok', 'tudastar'),
    ('Eredmények — megvalósult projektek és tanúsítványok', 'eredmenyek'),
    ('A cégről és a hírek', 'okotech-home'),
]

# Ezek a lapok a gyökérben állnak, és önmagukban is belépési pontok.
GYOKER_LAPOK = ['kapcsolat', 'konzultacio', 'ajanlat', 'megrendeles',
                'szippantasi-dij-kalkulator']


def cim_es_leiras(f: pathlib.Path):
    t = f.read_text(encoding='utf-8', errors='replace')
    c = re.search(r'<title>(.*?)</title>', t, re.S)
    d = re.search(r'<meta name="description" content="(.*?)">', t, re.S)
    cim = html.unescape(c.group(1)).strip() if c else f.stem
    # A címből a márkanevet levágjuk: a fájl fejlécében úgyis ott áll, és
    # ötvenszer megismételve csak zaj.
    cim = re.sub(r'\s*[—|]\s*ÖkoTech[- ]Home\s*$', '', cim).strip()
    leiras = html.unescape(d.group(1)).strip() if d else ''
    return cim, re.sub(r'\s+', ' ', leiras)


def indexelheto(f: pathlib.Path) -> bool:
    t = f.read_text(encoding='utf-8', errors='replace')
    return not re.search(r'<meta name="robots"[^>]*content="[^"]*noindex', t)


def ut(f: pathlib.Path, web: pathlib.Path) -> str:
    rel = f.relative_to(web).with_suffix('')
    reszek = list(rel.parts)
    mappa = reszek[-1] == 'index'
    if mappa:
        reszek.pop()
    if not reszek:
        return '/'
    return '/' + '/'.join(reszek) + ('/' if mappa else '')


def epit(web: pathlib.Path) -> str:
    fo = web / 'index.html'
    _, fo_leiras = cim_es_leiras(fo)

    s = ['# ÖkoTech-Home Kft.',
         '',
         f'> {fo_leiras}',
         '',
         'Biológiai szennyvíztisztító berendezések gyártása, telepítése és',
         'szervize közcsatorna nélküli ingatlanokhoz. 2004 óta, Esztergomban,',
         'saját fejlesztéssel és gyártással, több mint 3800 telepítéssel.',
         '',
         '## Amit tudni érdemes rólunk',
         '',
         '- **Mivel foglalkozunk:** egyedi (decentralizált) szennyvízkezelés ott,',
         '  ahol nincs közcsatorna — családi háztól a településszintű telepig.',
         '- **Mit adunk egy kézben:** felmérés, méretezés, gyártás, telepítés,',
         '  üzemeltetés és szerviz.',
         '- **Hol:** 2509 Esztergom, Strázsa u. 12. · +36 33 200 211 ·',
         '  kapcsolat@okotechhome.hu · Magyarország egész területén dolgozunk.',
         '- **Amit nem csinálunk:** ha a helyzet nem a mi rendszerünket kívánja,',
         '  azt megmondjuk. A webhely több lapja külön tárgyalja, MIKOR NEM',
         '  megfelelő egy-egy megoldás.',
         '']

    for cim, mappa in SZAKASZOK:
        d = web / mappa
        if not d.is_dir():
            continue
        tetelek = []
        for f in sorted(d.rglob('*.html')):
            if not indexelheto(f):
                continue
            c, l = cim_es_leiras(f)
            tetelek.append(f'- [{c}]({DOMAIN}{ut(f, web)}): {l}' if l
                           else f'- [{c}]({DOMAIN}{ut(f, web)})')
        if tetelek:
            s += [f'## {cim}', ''] + tetelek + ['']

    tetelek = []
    for nev in GYOKER_LAPOK:
        f = web / f'{nev}.html'
        if f.exists() and indexelheto(f):
            c, l = cim_es_leiras(f)
            tetelek.append(f'- [{c}]({DOMAIN}{ut(f, web)}): {l}' if l
                           else f'- [{c}]({DOMAIN}{ut(f, web)})')
    if tetelek:
        s += ['## Megkeresés és eszközök', ''] + tetelek + ['']

    s += ['## Megjegyzés',
          '',
          'A webhely teljes URL-listája: ' + DOMAIN + '/sitemap.xml',
          'A szakmai állításokat forrás támasztja alá a lapokon (szabvány,',
          'jogszabály, mérés). Számot, határértéket és jogszabályi hivatkozást',
          'kérjük az adott lapról idézni, ne összevontan.',
          '']
    return '\n'.join(s)


if __name__ == '__main__':
    web = (pathlib.Path(sys.argv[1]) if len(sys.argv) > 1
           else GYOKER / '_web_prod').resolve()
    if not web.is_dir():
        sys.exit(f'Nincs meg a fa: {web} — előbb: scripts/prod-epit.sh')
    ki = web / 'llms.txt'
    szoveg = epit(web)
    ki.write_text(szoveg, encoding='utf-8')
    print(f'llms.txt: {len(szoveg.splitlines())} sor, '
          f'{szoveg.count("- [")} hivatkozás')
