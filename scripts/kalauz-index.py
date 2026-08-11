#!/usr/bin/env python3
"""Tartalomindex Ökónak — a webhely lapjaiból, a lapokból magukból.

MIÉRT A LAPOKBÓL. Külön karbantartott témalista elavulna: a sitemap már ma sem
egyezik minden ponton a valósággal. Az index a KIADOTT HTML-ből készül, tehát
azt tükrözi, ami tényleg fent van — ha egy lap megszűnik, kiesik innen is.

MI KERÜL BE. Lapon: az útvonal, a cím, a leíró meta, és a szakaszcímek a
horgonyaikkal. A szakaszcím a lényeg: Öko nem csak azt tudja megmondani, MELYIK
lapon van a válasz, hanem azt is, hogy a lap MELYIK részében — és a horgonnyal
oda is tud görgetni.

KÉT KIMENET, KÉT CÉLRA:
  · kalauz-index.json — a NAVIGÁCIÓ indexe: melyik lapon melyik szakasz van.
    Kicsi, minden kéréssel betöltődik, ebből ellenőrizzük az URL-eket.
  · kalauz-szoveg.json — a SZAKASZOK SZÖVEGE. Ebből tud Öko a lap tényleges
    mondataiból válaszolni, nem a modell általános tudásából. Enélkül a
    végpont meg tudta mondani, HOL a válasz, de a témáról csak a promptba
    írt tudásból beszélt — egy szakmailag hihető, de forrás nélküli mondat
    ott bármikor keletkezhetett.

FUTTATÁS:  python3 scripts/kalauz-index.py
KIMENET:   _web/api/kalauz-index.json + _web/api/kalauz-szoveg.json
"""
import html
import json
import pathlib
import re

GYOKER = pathlib.Path(__file__).resolve().parent.parent / '_web'
KIMENET = GYOKER / 'api' / 'kalauz-index.json'
KIMENET_SZOVEG = GYOKER / 'api' / 'kalauz-szoveg.json'

# Szakaszonkénti felső hossz. Az átlag 626 karakter, tehát ez a plafon csak a
# leghosszabb szakaszokat érinti — ott viszont kell, mert egy 4000 karakteres
# szakasz egymaga elvinné a prompt idézhető keretét.
HOSSZ = 1800

# A szakaszszövegek ide gyűlnek, miközben a lapindex épül: ugyanazt a HTML-t
# kétszer beolvasni fölösleges.
szoveg_tetelek = []

# Ezekre nem irányítunk: jogi szövegek, hibaoldalak, eszközlapok.
KIHAGY = {
    '404.html', '401.html', '403.html', '500.html',
    'jelentes.html',            # csak saját eredménnyel értelmes
}

cim_re   = re.compile(r'<h1[^>]*>(.*?)</h1>', re.S)
desc_re  = re.compile(r'<meta name="description" content="([^"]*)"')
# Szakaszcím a horgonyával: a lapokon a <section> hordozza az id-t.
szakasz_re = re.compile(
    r'<section[^>]*\bid="([^"]+)"[^>]*>.*?<h2[^>]*>(.*?)</h2>', re.S)
# Ahol a section-nek nincs id-je, az aria-labelledby mutat a címre.
h2_re = re.compile(r'<h2[^>]*\bid="([^"]+)"[^>]*>(.*?)</h2>', re.S)


def tiszta(s: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()


# A szakaszszöveghez a jelölésnél többet kell eltávolítani: az inline SVG-k
# `path` koordinátái karakterszám szerint a törzsszöveg jelentős részét
# kitennék, és értelmes szót egyet sem tartalmaznak.
svg_re = re.compile(r'<svg\b.*?</svg>', re.S | re.I)
script_re = re.compile(r'<(script|style)\b.*?</\1>', re.S | re.I)
# A képernyőolvasónak szánt, vizuálisan rejtett feliratok duplikálnák a
# szöveget (a gombok „Bezárás", „Megnyitás" címkéi).
rejtett_re = re.compile(
    r'<span class="(visually-hidden|konzv-rejtett|oko-rejtett)"[^>]*>.*?</span>', re.S)


def szoveggé(reszlet: str) -> str:
    """HTML-részletből olvasható folyószöveg — ez megy a modellnek."""
    s = svg_re.sub(' ', reszlet)
    s = script_re.sub(' ', s)
    s = rejtett_re.sub(' ', s)
    # A morzsamenü a lap ELEJÉN áll, tehát a bevezető szövegrész elejére
    # kerülne — csupa navigációs szó, ami a kulcsszavas pontozást is rontja.
    s = re.sub(r'<nav class="breadcrumb".*?</nav>', ' ', s, flags=re.S)
    s = re.sub(r'<!--.*?-->', ' ', s, flags=re.S)      # a belső jegyzetek nem publikusak
    # A blokkzárók helyére szóköz kell, különben az „…kell.Ez…" alakok
    # összeragadnak, és a modell egy szónak látja a két mondat végét.
    s = re.sub(r'</(p|li|h[1-6]|div|td|th|dd|dt|section)>', ' ', s, flags=re.I)
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def darabol(s: str) -> list:
    """Hosszú szakaszt MONDATHATÁRON több részre — nem levágva.

    A csonkolás némán vitte el a leghosszabb szakaszok végét: a
    konzultációkérőnél például az egész űrlap egyetlen szakasz, tehát a
    mezősúgók fele, a jogi szöveg és az utolsó lapok mezői ki sem kerültek az
    indexbe. Ami nincs az indexben, arról Öko nem tud válaszolni.
    """
    if len(s) <= HOSSZ:
        return [s]
    reszek = []
    while s:
        if len(s) <= HOSSZ:
            reszek.append(s)
            break
        vag = max(s.rfind('. ', 0, HOSSZ), s.rfind('! ', 0, HOSSZ), s.rfind('? ', 0, HOSSZ))
        if vag < HOSSZ // 2:          # nincs mondathatár a plafon közelében
            vag = s.rfind(' ', 0, HOSSZ)
        if vag <= 0:
            vag = HOSSZ
        reszek.append(s[:vag + 1].strip())
        s = s[vag + 1:].strip()
    return [r for r in reszek if r]


def lapok():
    for p in sorted(GYOKER.rglob('*.html')):
        rel = p.relative_to(GYOKER)
        if rel.name in KIHAGY or str(rel).startswith('assets/'):
            continue
        t = p.read_text(encoding='utf-8')
        if 'noindex' in t and rel.name in ('adatkezelesi-tajekoztato.html',):
            pass  # a jogi lapokat bevesszük: gyakori kérdés, hol van
        cim = cim_re.search(t)
        if not cim:
            continue

        # A kiterjesztés nélküli útvonal a valódi URL (lásd .htaccess).
        url = str(rel).removesuffix('.html')
        if url.endswith('/index'):
            url = url.removesuffix('index')
        elif url == 'index':
            url = ''

        # CSAK A FŐTARTALOMBÓL. A lábléc hasábcímei is `<h2 id>`-k („Helyzetem",
        # „Megoldások"…), és bekerülve úgy néztek ki, mint tartalmi szakaszok —
        # Öko a láblécbe irányított volna. A `<main>` a határ.
        fo = re.search(r'<main\b.*?</main>', t, re.S)
        torzs = fo.group(0) if fo else t

        # A laponkénti felső korlát a prompt méretét fogja vissza, nem elvi
        # határ. Nyolcnál a bővebb lapok VÉGE esett ki — épp a fogalomtár, a
        # GYIK és a továbbvezető szakaszok, amikre a leggyakrabban kérdeznek rá.
        szakaszok = []
        for hid, h2 in h2_re.findall(torzs):
            szoveg = tiszta(h2)
            if szoveg and len(szakaszok) < 14:
                szakaszok.append({'cim': szoveg, 'horgony': '#' + hid})

        d = desc_re.search(t)
        lap_url = '/' + url if url else '/'
        lap_cim = tiszta(cim.group(1))

        # SZAKASZSZÖVEG. A vágópontok a `<h2 id>`-k: a címtől a következő
        # címig tartó rész egy szakasz. Ez megbízhatóbb, mint a `<section>`
        # párosítása regexszel, és pontosan azzal a horgonnyal áll párban,
        # amit a felület ki tud emelni.
        darabok = re.split(r'(<h2[^>]*\bid="([^"]+)"[^>]*>)', torzs)
        # darabok[0] a legelső cím ELŐTTI rész: a hero és a bevezető.
        bevezeto = szoveggé(darabok[0])
        if len(bevezeto) > 60:
            for n, resz in enumerate(darabol(bevezeto)):
                szoveg_tetelek.append({
                    'url': lap_url, 'lap': lap_cim,
                    'cim': 'Bevezető' + (f' ({n + 1}.)' if n else ''),
                    'horgony': '', 'szoveg': resz,
                })
        for i in range(1, len(darabok), 3):
            hid = darabok[i + 1]
            test = szoveggé(darabok[i + 2]) if i + 2 < len(darabok) else ''
            # A címet a szöveg elé fűzzük: a kulcsszavas pontozásnak és a
            # modellnek is kell a kontextus, hogy miről szól a részlet.
            szakasz_cim = tiszta(re.sub(r'<[^>]+>', '', darabok[i + 2].split('</h2>')[0])) \
                if '</h2>' in darabok[i + 2] else ''
            if len(test) > 60:
                for n, resz in enumerate(darabol(test)):
                    szoveg_tetelek.append({
                        'url': lap_url, 'lap': lap_cim,
                        'cim': szakasz_cim + (f' ({n + 1}. rész)' if n else ''),
                        'horgony': '#' + hid, 'szoveg': resz,
                    })

        yield {
            'url': lap_url,
            'cim': lap_cim,
            'leiras': tiszta(d.group(1)) if d else '',
            'szakaszok': szakaszok,
        }


def main() -> None:
    adat = list(lapok())                       # menet közben tölti a szoveg_tetelek-et
    KIMENET.write_text(
        json.dumps({'lapok': adat}, ensure_ascii=False, separators=(',', ':')),
        encoding='utf-8')
    KIMENET_SZOVEG.write_text(
        json.dumps({'reszek': szoveg_tetelek}, ensure_ascii=False, separators=(',', ':')),
        encoding='utf-8')

    szakasz = sum(len(l['szakaszok']) for l in adat)
    karakter = sum(len(r['szoveg']) for r in szoveg_tetelek)
    print(f'{len(adat)} lap, {szakasz} szakasz — {KIMENET.name} '
          f'{KIMENET.stat().st_size // 1024} KB')
    print(f'{len(szoveg_tetelek)} szövegrész, {karakter // 1000} ezer karakter — '
          f'{KIMENET_SZOVEG.name} {KIMENET_SZOVEG.stat().st_size // 1024} KB')


if __name__ == '__main__':
    main()
