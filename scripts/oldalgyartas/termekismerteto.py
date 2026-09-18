#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""termekismerteto.py — az A.B. Clear termékismertető, mai arculattal.

MIÉRT ÚJ. A kiszolgálón talált `A.B.Clear_termekismerteto.pdf` négy oldala jó
anyag, de a lába alatt a RÉGI cég áll: `+36 33 400 387`, `www.emeszto.hu`,
`www.ciszterna.hu` — a mai szám +36 33 200 211, és e-mail-cím egyáltalán nincs
benne. Ez a fájl minden ajánlatkérőnek automatikusan kimenne, tehát nem mehet ki
így. Négy adat is eltért a webhely mai szövegétől:

  · GARANCIA: „2 év" — a 2026-09-18-i ÁSZF szerint fogyasztónak 3 év,
    vállalkozásnak 1 év, a tartályra 15 év, feltétellel.
  · VITUKI-ÉRTÉKEK: a régi lapon 20 BOI5 / 10 NH4-N / 8 P; a webhely mai,
    jóváhagyott tájékoztatása 15 / 9 / 5. A webhelyé az irányadó.
  · MEGFELELŐSÉGI ÁLLÍTÁS: a régi lap kimondta, hogy a berendezések
    „megfelelnek a 28/2004. KvVM-rendelet 3. területi kategóriájának". A kánon
    ezt tiltja: a mért érték nem megfelelőségi ígéret, mert a kibocsátás a
    terheléstől és az üzemeltetéstől is függ.
  · ÁRAMFOGYASZTÁS: a régi lap „havi 14-16 kWh"-t írt, a webhely 1000–1500 Ft
    havi villamosenergia-költséget (36 Ft/kWh példaárral, ami 28–42 kWh).
    A kettő nem hozható össze. BELA DÖNTÉSE (2026-09-18): a webhely adata a
    mérvadó, a 14-16 kWh nem kerül vissza. A szám a webhelyen és ebben a
    dokumentumban is ugyanaz — ha változik, mindkét helyen javítani kell.

A MŰSZAKI TÁBLÁZAT a régi termékismertetőből jön: az a cég saját, közzétett
terméklapja. A méretek mellett ott a forrás kikötése is.

FUTTATÁS:  python3 scripts/oldalgyartas/termekismerteto.py
"""
import base64
import pathlib
import re
import subprocess
import sys
import tempfile

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
CEL = WEB / 'assets' / 'dok' / 'okotechhome-termekismerteto.pdf'

CHROME_JELOLTEK = [
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
]


def chrome():
    for c in CHROME_JELOLTEK:
        if pathlib.Path(c).exists():
            return c
    sys.exit('HIBA: nem találom a Chrome-ot a PDF-nyomtatáshoz.')


def be(ut, mime):
    """Fájl beágyazva. A PDF ne függjön attól, hol áll a forrásfa."""
    adat = base64.b64encode((WEB / ut).read_bytes()).decode()
    return f'data:{mime};base64,{adat}'


MIME = {'.webp': 'image/webp', '.svg': 'image/svg+xml',
        '.png': 'image/png', '.jpg': 'image/jpeg'}


def kep(ut):
    return be(ut, MIME[pathlib.Path(ut).suffix])


def jelrajz(szin='#80A640'):
    """A jelrajz SVG-je beágyazva. Az `<img>` feketén rajzolná: a fájl maszknak
    készült, a kitöltése ott közömbös — itt viszont színt kell adni neki."""
    s = (WEB / 'assets/img/logo-jel.svg').read_text(encoding='utf-8')
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    # A path saját `fill="#000"`-ja erősebb a gyökéren megadottnál, ezért azt
    # írjuk át — különben a jelrajz feketén jelenik meg.
    s = s.replace('fill="#000"', f'fill="{szin}"')
    return s.replace('<svg ', '<svg class="jel" ', 1)


def kicsinyit(ut, max_szel):
    """Kép a NYOMTATÁSI mérethez igazítva, átlátszóság megtartásával.

    A Chrome a beágyazott képet pixelenként viszi a PDF-be: az 1672 pixel széles
    metszet egymaga 2 MB fölé vitte a fájlt, pedig a lapon 100 mm-en áll. A
    termékfotók KIVÁGOTTAK (alfa-csatorna), ezért nem lehet belőlük JPEG — PNG
    marad, csak kisebb felbontáson.
    """
    forras = WEB / ut
    cel = pathlib.Path(tempfile.gettempdir()) / (forras.stem + f'-{max_szel}.png')
    if not cel.exists():
        subprocess.run(['sips', '-s', 'format', 'png', '-Z', str(max_szel),
                        str(forras), '--out', str(cel)], check=True, capture_output=True)
    adat = base64.b64encode(cel.read_bytes()).decode()
    return f'data:image/png;base64,{adat}'


def betu(nev):
    return be(f'assets/fonts/{nev}', 'font/woff2')


# ---------------------------------------------------------------- tartalom
ELONYOK = [
    ('Nincs csatornadíj',
     'A szennyvíz a keletkezés helyén tisztul meg. Nincs csatornahasználati díj, és '
     'szippantás sem — az iszapzsákos technológia miatt a fölösiszap zsákban gyűlik.'),
    ('Alacsony üzemeltetési költség',
     'Az áramfogyasztás a berendezés méretétől függ; háztartási változatnál ez '
     'jellemzően 1000–1500 Ft havonta (36 Ft/kWh példaárral). A teljes éves '
     'üzemeltetés — árammal, iszapzsákokkal és évesített membráncserével — '
     'nagyjából 22 700–27 500 Ft.'),
    ('Nem igényel nagy földmunkát',
     'A polipropilén tartály könnyű: daru nélkül, kézi erővel is elhelyezhető. '
     'A befolyó- és a kifolyócső között mindössze 20 cm a szintkülönbség.'),
    ('Jól viseli az alul- és túlterhelést',
     'A hétvégi csúcs és a néhány hetes kihagyás sem borítja fel a biológiát. '
     'Nyaralónál is működik, ha a leállás nem húzódik hónapokra.'),
    ('Szagtalan és csendes',
     'Normál működés mellett nincs szennyvízszag a kertben, és hangszigetelésre '
     'sincs szükség — a kompresszor a berendezésben, a föld alatt dolgozik.'),
    ('Hosszú élettartam',
     'A tartály környezeti hatásokkal szemben ellenálló. A tartály stabilitására és '
     'vízzáróságára 15 év kiterjesztett jótállást vállalunk — feltétele, hogy a '
     'kiszállítást, a beszerelést és az éves karbantartást is mi végezzük.'),
]

MUKODES = [
    ('A szennyvíz beérkezik',
     'Az első, anaerob kamrába jutva egy kosárszűrőre kerül, amely felfogja a nagyobb '
     'szilárd szennyeződéseket. A vízben oldódó anyagok a vízmozgás miatt '
     'felaprózódnak, és a szennyvízzel együtt átjutnak a szűrőn.'),
    ('Anoxikus tér',
     'A kamrán átjutva anoxikus térbe kerül a víz. Itt zajlanak a szennyeződések '
     'levegő nélküli bontási folyamatai.'),
    ('Levegőztetett tér',
     'Ezt követi az aerob, mesterségesen levegőztetett tér. Itt egy mikrobuborékos '
     'levegőztető cső látja el a baktériumokat oxigénnel — ezeknek a folyamatoknak '
     'köszönhető, hogy a működés nem jár kellemetlen szaghatással.'),
    ('Utóülepítés',
     'Az utolsó lebontási folyamat után a szennyvíz az utóülepítő térbe jut. A tiszta '
     'víz és az iszap összeállt, megmaradt szennyeződések szétválnak, előbbi a '
     'felszínen marad, míg az iszap a kamra aljára lerakódik.'),
    ('A tisztított víz távozik',
     'A tiszta víz a kifolyócsövön keresztül távozik a berendezésből — '
     'elszivárogtatásra, vagy ciszternában tárolva későbbi újrahasznosításra.'),
]

VITUKI = [
    ('KOI(Cr)', '55 mg/l'), ('BOI₅', '15 mg/l'), ('Lebegőanyag', '18 mg/l'),
    ('Ammónium-nitrogén', '9 mg/l'), ('Összes nitrogén', '20 mg/l'),
    ('Összes foszfor', '5 mg/l'),
]

MUSZAKI = [
    ('Napi kapacitás (m³)', '0,78', '1', '1,3'),
    ('Átmérő (mm)', '1330', '1330', '1500'),
    ('Magasság (mm)', '1900', '2200', '2530'),
    ('Befolyócső magassága (mm)', '1380', '1680', '1715'),
    ('Kifolyócső magassága (mm)', '1220', '1520', '1555'),
    ('Be- és kifolyócső átmérője (mm)', '110/110', '110/110', '110/110'),
    ('Légbefúvó nyomása (Δpmbar)', '230', '230', '230'),
    ('Légbefúvó kapacitása (l/perc)', '30', '37', '52'),
    ('Levegőztető elem hossza (m)', '0,3', '0,36', '0,5'),
    ('Légbefúvó teljesítménye (W)', '60', '80', '80'),
]


def lap1():
    return f'''
<section class="lap cimlap">
  <div class="cimlap-szoveg">
    <img class="logo" src="{kep('assets/img/logo-okotechhome.svg')}" alt="">
    <p class="kicsi">Termékismertető</p>
    <h1>A.B. Clear<br>biológiai szennyvíztisztító</h1>
    <p class="alcim">Harmóniában a természettel — 6-tól 50 lakosegyenértékig,
       családi háztól panzión át intézményekig.</p>
    <ul class="tenyek">
      <li><strong>6–50 LE</strong><span>lakosegyenérték</span></li>
      <li><strong>EN 12566-3</strong><span>CE-tanúsítás</span></li>
      <li><strong>15 év</strong><span>tartálygarancia</span></li>
      <li><strong>Magyar</strong><span>fejlesztés és gyártás</span></li>
    </ul>
  </div>
  <figure class="cimlap-kep">
    <img src="{kicsinyit('assets/img/termek-ab-clear.webp', 1200)}" alt="">
  </figure>
  <p class="labjegyzet">ÖkoTech-Home Kft. · 2509 Esztergom, Strázsa u. 12. ·
     +36 33 200 211 · kapcsolat@okotechhome.hu · okotechhome.hu</p>
</section>'''


def lap2():
    tetelek = ''.join(f'''
      <li><h3>{c}</h3><p>{sz}</p></li>''' for c, sz in ELONYOK)
    return f'''
<section class="lap">
  <header class="fej">
    {jelrajz()}
    <p class="kicsi">Miért az A.B. Clear</p>
  </header>
  <h2>A közműves tisztítással egyenértékű megoldás — a saját telken</h2>
  <p class="bevezeto">Az A.B. Clear berendezések a kommunális szennyvíz megtisztítására
     alkalmasak: családi házak, nyaralók, irodák, panziók, vendéglők, tanyák, lovardák és
     intézmények szennyvizére, de településrészek, sőt teljes települések kommunális
     szennyvizének kezelésére is.</p>
  <ul class="elonyok">{tetelek}
  </ul>
  <div class="zaro-sav">
    <img src="{kicsinyit('assets/img/megoldas-iszapzsak.webp', 600)}" alt="">
    <div>
      <h3>Az iszapzsák — ettől marad el a szippantás</h3>
      <p>A keletkező fölösiszap a berendezésen belül, zsákban gyűlik és víztelenedik.
         A zsák a helyén cserélhető, az iszapmennyiség pedig állandó marad. A tisztított
         víz a kifolyócsövön át távozik — elszivárogtatásra vagy ciszternába.</p>
    </div>
  </div>
</section>'''


def lap3():
    lepesek = ''.join(f'''
      <li><span class="szam">{i:02d}</span><div><h3>{c}</h3><p>{sz}</p></div></li>'''
                      for i, (c, sz) in enumerate(MUKODES, 1))
    return f'''
<section class="lap">
  <header class="fej">
    {jelrajz()}
    <p class="kicsi">Hogyan működik</p>
  </header>
  <h2>Teljesoxidációs eleveniszapos tisztítás, iszapzsákkal</h2>
  <p class="bevezeto">A berendezések ugyanazon az elven működnek, mint a nagy, városi
     szennyvíztisztító telepek: az összes munkafolyamat egy tartályon belül zajlik, a
     különálló kamrák más és más tisztítási fázisnak felelnek meg. A bontást
     mikroorganizmusok végzik.</p>
  <div class="ket-hasab">
    <ol class="lepesek">{lepesek}
    </ol>
    <div>
      <figure class="metszet">
        <img src="{kicsinyit('assets/img/mukodes-metszet.webp', 1180)}" alt="">
      </figure>
      <div class="doboz">
        <h3>Az iszapzsák — egyedülálló technológiai újítás</h3>
        <p>Az A.B. Clear szennyvíztisztítók egyedüliként rendelkeznek iszapzsákkal,
           amelybe az iszap elektromos szivattyú közbeiktatása nélkül kerül. A
           keletkező fölösiszapot ez a részegység távolítja el a berendezésből,
           víztelenítve. Az iszap a helyén, könnyen kezelhető formában tárolódik,
           a zsákkal együtt eltávolítható. <strong>Ezzel fölöslegessé válik a
           szippantás</strong>, az iszapmennyiség pedig állandó marad.</p>
      </div>
      <div class="doboz">
        <h3>Elektromos részegységek</h3>
        <p><strong>Membrános levegőszivattyú</strong> — kis teljesítményű, csendes,
           230 V-os hálózati áramról üzemelő készülék; a membrán negyedévenkénti
           tisztítás és 50 000 üzemóránként csere mellett dolgozik.
           <strong>Váltómotor</strong> — a levegő útját a beállított időpontokban az
           iszapzsák felé irányítja. <strong>Mikroprocesszoros vezérlőegység</strong>
           (választható) — háromállású időkapcsolóként az üzemmódot igény szerint
           állítja be.</p>
      </div>
    </div>
  </div>
</section>'''


def lap4():
    vituki = ''.join(f'<tr><th>{n}</th><td>{e}</td></tr>' for n, e in VITUKI)
    muszaki = ''.join(
        f'<tr><th>{s[0]}</th><td>{s[1]}</td><td>{s[2]}</td><td>{s[3]}</td></tr>'
        for s in MUSZAKI)
    return f'''
<section class="lap">
  <header class="fej">
    {jelrajz()}
    <p class="kicsi">Műszaki adatok</p>
  </header>
  <h2>Mért értékek, méretek, jótállás</h2>
  <div class="ket-hasab">
    <div>
      <h3>Kifolyóvíz-jellemzők</h3>
      <table class="adat"><tbody>{vituki}</tbody></table>
      <p class="apro">VITUKI-vizsgálatra hivatkozó, jellemző értékek. <strong>Nem
         terméktulajdonságok</strong> abban az értelemben, hogy minden körülmények
         között garantáltak lennének: a tényleges kilépővíz-minőség a terheléstől, az
         üzemeltetéstől és a biológia állapotától is függ. Egy konkrét projekt
         kibocsátási megfelelőségét mindig az adott befogadó, az alkalmazandó
         határértékek és a hatósági előírások alapján kell megítélni.</p>
      <h3>Jótállás</h3>
      <p class="apro">A berendezésre és elektronikai részére fogyasztóként
         <strong>3 év</strong>, vállalkozásként <strong>1 év</strong>. A műanyag
         tartályra <strong>15 év</strong> kiterjesztett jótállás, ha a kiszállítást,
         a szakszerű beszerelést és az éves karbantartást is mi végezzük. Az
         ÁSZF-ben részletesen: okotechhome.hu/aszf</p>
    </div>
    <div>
      <h3>Technikai adatok</h3>
      <table class="adat muszaki">
        <thead><tr><th></th><th>A.B. Clear 6</th><th>A.B. Clear 8</th><th>A.B. Clear 10</th></tr></thead>
        <tbody>{muszaki}</tbody>
      </table>
      <p class="apro">A változtatás jogát fenntartjuk; telepítés előtt kérje az aktuális
         méreteket. Nagyobb kapacitásról — 50 lakosegyenérték felett, illetve
         településszintű rendszereknél — külön méretezés készül.</p>
      <h3>Engedélyezés</h3>
      <p class="apro">A szükséges hatósági eljárás attól függ, milyen berendezést
         telepítenek, hogyan történik a tisztított víz elhelyezése, és milyenek a
         helyszín adottságai. A CE-tanúsítással rendelkező szennyvízkezelő
         berendezésekre és a tisztított víz elszivárogtatására nem azonos szabályok
         vonatkoznak, ezért az alkalmazandó eljárást minden esetben az adott projekt
         alapján tisztázzuk.</p>
    </div>
  </div>
  <footer class="zaro">
    <div>
      <img class="logo-zaro" src="{kep('assets/img/logo-okotechhome.svg')}" alt="">
      <p class="apro">Fejlesztés, gyártás, telepítés és szerviz egy kézben.</p>
    </div>
    <p class="elerhetoseg">2509 Esztergom, Strázsa u. 12.<br>
       +36 33 200 211<br>kapcsolat@okotechhome.hu<br><strong>okotechhome.hu</strong></p>
  </footer>
</section>'''


def dokumentum():
    return f'''<!DOCTYPE html>
<html lang="hu"><head><meta charset="utf-8">
<title>A.B. Clear biológiai szennyvíztisztító — termékismertető</title>
<style>
@font-face {{ font-family:'Zilla Slab'; font-weight:600; src:url({betu('zilla-slab-600-latin-ext.woff2')}) format('woff2'); }}
@font-face {{ font-family:'Zilla Slab'; font-weight:400; src:url({betu('zilla-slab-400-latin-ext.woff2')}) format('woff2'); }}
@font-face {{ font-family:'IBM Plex Sans'; font-weight:400 600; src:url({betu('ibm-plex-sans-400-600-latin-ext.woff2')}) format('woff2'); }}
@font-face {{ font-family:'IBM Plex Mono'; font-weight:500; src:url({betu('ibm-plex-mono-500-latin-ext.woff2')}) format('woff2'); }}

:root {{
  --fern:#80A640; --forest:#133216; --olive:#56642B;
  --lime:#E5EBBB; --drizzle:#F3F2EC; --stardust:#FAFAFA;
}}
* {{ box-sizing:border-box; margin:0; padding:0; }}
@page {{ size:A4 landscape; margin:0; }}
html {{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }}
body {{ font-family:'IBM Plex Sans',sans-serif; color:var(--forest); font-size:10.2pt; line-height:1.5; }}

.lap {{
  width:297mm; height:210mm; padding:14mm 16mm; page-break-after:always;
  position:relative; overflow:hidden; background:var(--stardust);
  display:flex; flex-direction:column;
}}
.lap:last-child {{ page-break-after:auto; }}

h1 {{ font-family:'Zilla Slab',serif; font-weight:600; font-size:30pt; line-height:1.08; letter-spacing:-.01em; }}
h2 {{ font-family:'Zilla Slab',serif; font-weight:600; font-size:17pt; line-height:1.2; margin-bottom:3mm; }}
h3 {{ font-family:'IBM Plex Sans',sans-serif; font-weight:600; font-size:10.5pt; margin-bottom:1.2mm; }}
p {{ margin-bottom:2mm; }}
.kicsi {{ font-family:'IBM Plex Mono',monospace; font-weight:500; font-size:7.6pt;
  letter-spacing:.16em; text-transform:uppercase; color:var(--olive); margin-bottom:2mm; }}
.bevezeto {{ font-size:11pt; max-width:210mm; margin-bottom:5mm; color:var(--olive); }}
.apro {{ font-size:8.6pt; line-height:1.45; color:var(--olive); }}

/* --- címlap ------------------------------------------------------------ */
.cimlap {{ display:grid; grid-template-columns:1.05fr .95fr; gap:12mm; align-items:center;
  background:linear-gradient(180deg,var(--drizzle) 0%,var(--stardust) 62%); }}
.logo {{ width:52mm; margin-bottom:9mm; }}
.cimlap .alcim {{ font-size:12pt; color:var(--olive); margin:4mm 0 8mm; max-width:120mm; }}
.tenyek {{ display:grid; grid-template-columns:repeat(2,1fr); gap:3mm 5mm; list-style:none; max-width:120mm; }}
.tenyek li {{ background:var(--lime); border-radius:3mm; padding:3mm 4mm; }}
.tenyek strong {{ display:block; font-family:'Zilla Slab',serif; font-size:13pt; }}
.tenyek span {{ font-size:8.4pt; color:var(--olive); }}
.cimlap-kep img {{ width:100%; height:150mm; object-fit:cover; border-radius:4mm; }}
.labjegyzet {{ position:absolute; left:16mm; right:16mm; bottom:9mm; font-size:8.2pt;
  color:var(--olive); border-top:.4mm solid var(--lime); padding-top:2.5mm; }}

/* --- belső lapok -------------------------------------------------------- */
.fej {{ display:flex; align-items:center; gap:3mm; margin-bottom:5mm; }}
.jel {{ width:8mm; height:auto; flex:none; }}
.fej .kicsi {{ margin:0; }}
.elonyok {{ display:grid; grid-template-columns:repeat(3,1fr); gap:4mm; list-style:none; margin-bottom:5mm; }}
.elonyok li {{ background:var(--drizzle); border-radius:3mm; padding:4mm; }}
.elonyok p {{ font-size:9pt; color:var(--olive); margin:0; }}
.zaro-sav {{ margin-top:auto; display:grid; grid-template-columns:46mm 1fr; gap:6mm;
  align-items:center; background:var(--lime); border-radius:3mm; padding:4mm 5mm; }}
.zaro-sav img {{ width:100%; height:40mm; object-fit:contain; }}
.zaro-sav p {{ font-size:9pt; margin:0; }}

.ket-hasab {{ display:grid; grid-template-columns:1fr 1fr; gap:8mm; }}
.lepesek {{ list-style:none; }}
.lepesek li {{ display:flex; gap:3mm; margin-bottom:3.5mm; }}
.szam {{ font-family:'IBM Plex Mono',monospace; font-weight:500; font-size:8.4pt;
  color:var(--fern); padding-top:.6mm; }}
.lepesek p {{ font-size:9pt; color:var(--olive); margin:0; }}
.metszet img {{ width:100%; height:52mm; object-fit:contain; margin-bottom:4mm; }}
.doboz {{ background:var(--lime); border-radius:3mm; padding:4mm; margin-bottom:3mm; }}
.doboz p {{ font-size:8.8pt; margin:0; }}

/* --- táblázatok --------------------------------------------------------- */
.adat {{ width:100%; border-collapse:collapse; margin-bottom:3mm; font-size:9pt; }}
.adat th, .adat td {{ text-align:left; padding:1.5mm 2mm; border-bottom:.3mm solid var(--lime); }}
.adat th {{ font-weight:400; color:var(--olive); }}
.adat td {{ font-family:'IBM Plex Mono',monospace; font-weight:500; text-align:right; }}
.muszaki thead th {{ font-weight:600; color:var(--forest); text-align:right; font-size:8.6pt; }}
.muszaki thead th:first-child {{ text-align:left; }}
.adat h3 {{ margin-top:4mm; }}
.ket-hasab h3 {{ margin-top:4mm; margin-bottom:2mm; }}
.ket-hasab > div > h3:first-child {{ margin-top:0; }}

.zaro {{ margin-top:auto; display:flex; justify-content:space-between; align-items:flex-end;
  border-top:.4mm solid var(--lime); padding-top:3.5mm; }}
.logo-zaro {{ width:42mm; margin-bottom:1.5mm; }}
.elerhetoseg {{ font-size:9pt; text-align:right; color:var(--olive); margin:0; }}
</style></head><body>
{lap1()}{lap2()}{lap3()}{lap4()}
</body></html>'''


def main():
    with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(dokumentum())
        atmeneti = f.name
    CEL.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([chrome(), '--headless', '--disable-gpu', '--no-sandbox',
                    '--no-pdf-header-footer', f'--print-to-pdf={CEL}',
                    f'file://{atmeneti}'], check=True, capture_output=True, timeout=180)
    pathlib.Path(atmeneti).unlink(missing_ok=True)
    print(f'  {CEL.relative_to(GYOKER)}: {CEL.stat().st_size / 1024:.0f} KB')


if __name__ == '__main__':
    main()
