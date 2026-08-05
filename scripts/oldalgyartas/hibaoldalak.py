#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Egyedi hibaoldalak — 404 · 403 · 401 · 500.

MIÉRT ÖNHORDÓ EZ A NÉGY OLDAL
-----------------------------
Hibaoldalnál a böngésző a relatív útvonalakat a KÉRT URL-hez oldja fel, nem a
hibaoldal helyéhez. A `/megoldasok/nincs-ilyen` kérésre kiszolgált 404.html-ben
az `assets/css/app.css` így `/megoldasok/assets/css/app.css`-re mutatna — ami
szintén 404. Ezért ezen a négy oldalon MINDEN hivatkozás gyökér-abszolút, a logó
pedig beágyazott SVG — nincs egyetlen relatív útvonal sem.

MIÉRT NEM BEÁGYAZOTT A STÍLUS
-----------------------------
A relatív útvonal problémáját elvileg beágyazott `<style>` is megoldaná — DE a
`.htaccess` CSP-je `style-src 'self' https://fonts.googleapis.com`, `'unsafe-inline'`
NÉLKÜL. A böngésző ezért minden `<style>` blokkot eldob, és a hibaoldal
formázatlanul jelenik meg. Ugyanez vonatkozik a beágyazott logó SVG SAJÁT
`<style>` blokkjára is — attól rajzolódott feketén.

A megoldás: a stílus külön fájlban (`/assets/css/hiba.css`), GYÖKÉR-ABSZOLÚT
hivatkozással — az is független a kért URL mélységétől —, a logó színe pedig
`fill` prezentációs attribútummal, amit a CSP nem érint.

Ez a webhely EGYETLEN helye, ahol a stílus nem az app.css-ből jön. Ha a
tokenek változnak, a `hiba.css`-t kézzel utána kell húzni.

FIGYELEM: helyben ez a hiba NEM jön elő, mert a `serve.py` nem küld CSP-fejlécet.
A hibaoldalakat élesben (vagy CSP-t küldő kiszolgálón) kell ellenőrizni.

FIGYELEM: a gyökér-abszolút hivatkozások (és a .htaccess ErrorDocument sorai)
aldomainen/gyökérben jók, ALKÖNYVTÁRAS telepítésnél viszont át kell írni őket.
"""
import pathlib, re

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'
LOGO = (WEB / 'assets' / 'img' / 'logo-okotechhome.svg').read_text(encoding='utf-8')

# A beágyazott logóból kivesszük az XML-fejlécet, és a méretet CSS adja.
LOGO_INLINE = re.sub(r'^\s*<\?xml[^>]*\?>\s*', '', LOGO).strip()
# A CSP miatt az SVG saját <style> blokkja nem érvényesülne — a színt
# prezentációs attribútum adja, a témaváltást a hiba.css.
LOGO_INLINE = re.sub(r'<style.*?</style>', '', LOGO_INLINE, flags=re.S)
LOGO_INLINE = LOGO_INLINE.replace('<path class="fil0"', '<path class="fil0" fill="#80A640"')
LOGO_INLINE = LOGO_INLINE.replace('<path class="fil1"', '<path class="fil1" fill="#133216"')
LOGO_INLINE = LOGO_INLINE.replace('<svg ', '<svg class="hiba-logo-svg" role="img" aria-label="ÖkoTech Home" ', 1)

FEJLEC_CSS = '''/* =============================================================================
   hiba.css — a 401/403/404/500 oldalak stílusa
   -----------------------------------------------------------------------------
   GENERÁLT FÁJL — a forrás: scripts/oldalgyartas/hibaoldalak.py. Kézzel ne írd.

   Miért külön fájl, és miért nem az app.css:
     * a hibaoldalt a kiszolgáló tetszőleges mélységű URL-re adja vissza, a
       böngésző pedig a relatív útvonalakat a KÉRT URL-hez oldja fel — ezért
       a hivatkozás gyökér-abszolút (/assets/css/hiba.css);
     * beágyazott <style> nem jöhet szóba: a .htaccess CSP-je 'unsafe-inline'
       nélküli style-src-t ad, ami eldobná;
     * az app.css teljes egészében fölösleges volna egy hibaoldalhoz.

   A tokenek az app.css-ből másolt értékek. Ha ott változnak, ITT is át kell írni.
   ============================================================================= */
'''

CSS = '''
  /* A designrendszer szükséges részhalmaza — lásd a fájl fejlécében az okot. */
  :root{
    --color-forest:#133216; --color-fern:#80A640; --color-olive:#5B7B2E;
    --color-stardust:#FAFAFA; --color-drizzle:#F2F2EF; --color-slate:#4A4F49;
    --canvas:var(--color-drizzle); --surface:var(--color-stardust);
    --text-primary:var(--color-forest); --text-secondary:var(--color-slate);
    --primary:var(--color-fern); --border:#DCDCD6;
    --space-8:.5rem; --space-16:1rem; --space-24:1.5rem; --space-32:2rem;
    --space-48:3rem; --space-64:4rem; --space-96:6rem;
    --radius:.5rem;
  }
  @media (prefers-color-scheme:dark){
    :root{
      --canvas:#0E1A10; --surface:#16241A; --text-primary:var(--color-stardust);
      --text-secondary:#B9C2B8; --border:#2A3B2D;
    }
  }
  *,*::before,*::after{box-sizing:border-box}
  html{-webkit-text-size-adjust:100%}
  body{
    margin:0; min-height:100svh; display:flex; flex-direction:column;
    background:var(--canvas); color:var(--text-primary);
    font-family:"IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;
    font-size:1rem; line-height:1.6;
  }
  /* A hibaoldal egyetlen, középre zárt oszlop — ezért a logó és a lábléc is
     középen áll, nem balra zárva, mint a webhely többi részén. */
  .hiba-fej{
    padding:var(--space-24) clamp(1.25rem,5vw,3rem);
    border-bottom:1px solid var(--border); background:var(--surface);
    text-align:center;
  }
  .hiba-logo{display:inline-flex; text-decoration:none}
  .hiba-logo-svg{height:var(--space-48); width:auto; display:block}
  /* A logó színét `fill` prezentációs attribútum adja (a CSP miatt az SVG saját
     <style> blokkja nem érvényesülne). A prezentációs attribútum a leggyengébb
     forrás, ezért a sötét témát innen felül tudjuk írni: a szóvédjegy Forestje
     sötét háttéren olvashatatlan lenne. A jelrajz Fernje mindkét témán él. */
  @media (prefers-color-scheme:dark){
    .hiba-logo-svg .fil0{fill:var(--color-fern)}      /* a jelrajz sötéten is Fern */
    .hiba-logo-svg .fil1{fill:var(--color-stardust)}  /* a szóvédjegy világosra vált */
  }
  .hiba-fo{
    flex:1; display:flex; align-items:center;
    padding:var(--space-96) clamp(1.25rem,5vw,3rem);
  }
  .hiba-torzs{max-width:44rem; margin-inline:auto}
  .hiba-kod{
    font-family:"IBM Plex Mono",ui-monospace,monospace;
    font-size:.6875rem; letter-spacing:.12em; text-transform:uppercase;
    color:var(--text-secondary); margin:0 0 var(--space-16);
  }
  .hiba-cim{
    font-family:"Zilla Slab",Georgia,serif; font-weight:500;
    font-size:clamp(1.75rem,4vw,2.375rem); line-height:1.2;
    margin:0 0 var(--space-24); text-wrap:balance;
  }
  .hiba-szoveg{color:var(--text-secondary); margin:0 0 var(--space-16); max-width:38rem}
  .hiba-lista{
    list-style:none; margin:var(--space-32) 0 0; padding:0;
    display:grid; gap:var(--space-8);
  }
  .hiba-lista a{color:var(--text-primary); text-decoration:none; font-weight:500}
  .hiba-lista a:hover{color:var(--color-olive)}
  .hiba-lista a::before{content:"→"; margin-right:var(--space-8); color:var(--primary)}
  .hiba-gomb{
    display:inline-flex; align-items:center; gap:var(--space-8);
    margin-top:var(--space-32); padding:.75rem var(--space-24);
    min-height:2.75rem;                     /* 44px érintőcélpont */
    background:var(--primary); color:var(--color-forest);
    border-radius:var(--radius); text-decoration:none; font-weight:600;
  }
  .hiba-gomb:hover{background:var(--color-olive); color:var(--color-stardust)}
  a:focus-visible,.hiba-logo:focus-visible{
    outline:2px solid var(--primary); outline-offset:3px; border-radius:2px;
  }
  .hiba-lab{
    padding:var(--space-24) clamp(1.25rem,5vw,3rem);
    border-top:1px solid var(--border); color:var(--text-secondary);
    font-size:.875rem; text-align:center;
  }
  .hiba-lab p{margin:0}
  .hiba-lab a{color:inherit}
'''

LINKEK = [
    ('/', 'Főoldal'),
    ('/helyzetem/', 'Miben keres megoldást?'),
    ('/megoldasok/', 'Megoldások áttekintése'),
    ('/kapcsolat', 'Kapcsolat'),
]

OLDALAK = [
    dict(kod=404, fajl='404.html',
         cim='Ez az oldal nincs meg',
         bekezdesek=[
             'A kért cím nem létezik, vagy időközben megváltozott. Ha hivatkozásból '
             'érkezett, a hivatkozás elavult; ha kézzel írta be a címet, érdemes '
             'ellenőrizni az elgépelést.',
             'Alább a leggyakoribb belépési pontok — innen néhány kattintással '
             'megtalálja, amit keresett.'],
         gomb=('/', 'Vissza a főoldalra')),
    dict(kod=403, fajl='403.html',
         cim='Ehhez a tartalomhoz nincs hozzáférés',
         bekezdesek=[
             'A cím létezik, de a megtekintéséhez nincs jogosultsága. Ez rendszerint '
             'védett könyvtárat vagy olyan fájlt jelent, amelyet a kiszolgáló nem ad ki.',
             'Ha úgy gondolja, hogy hozzáférésre jogosult, írjon nekünk, és megnézzük.'],
         gomb=('/kapcsolat', 'Kapcsolatfelvétel')),
    dict(kod=401, fajl='401.html',
         cim='Belépés szükséges',
         bekezdesek=[
             'Ez a terület jelszóval védett. A webhely jelenleg fejlesztés alatt áll, '
             'ezért a tesztváltozat csak belépéssel érhető el.',
             'Ha kapott hozzáférést, töltse újra az oldalt, és adja meg a kapott '
             'felhasználónevet és jelszót.'],
         gomb=('/kapcsolat', 'Hozzáférés kérése')),
    dict(kod=500, fajl='500.html',
         cim='Váratlan hiba történt a kiszolgálón',
         bekezdesek=[
             'A kérést nem sikerült feldolgozni. A hiba a mi oldalunkon keletkezett, '
             'nem az Ön böngészőjében — az újratöltés gyakran segít.',
             'Ha a hiba ismétlődik, kérjük jelezze, és megírjuk, mikorra várható '
             'a javítás.'],
         gomb=('/', 'Vissza a főoldalra')),
]

SABLON = '''<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<!-- Hibaoldal: keresőben soha nincs helye, a teszt üzemmódtól függetlenül sem. -->
<meta name="robots" content="noindex, nofollow">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{cim} — ÖkoTech Home</title>
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<meta name="theme-color" content="#133216">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400&display=swap">
<link rel="stylesheet" href="/assets/css/hiba.css?v=2">
</head>
<body>

<header class="hiba-fej">
  <a class="hiba-logo" href="/" aria-label="ÖkoTech Home — főoldal">
{logo}
  </a>
</header>

<main class="hiba-fo">
  <div class="hiba-torzs">
    <p class="hiba-kod">Hiba {kod}</p>
    <h1 class="hiba-cim">{cim}</h1>
{bekezdesek}
    <a class="hiba-gomb" href="{gomb_href}">{gomb_cimke}</a>
    <ul class="hiba-lista">
{linkek}
    </ul>
  </div>
</main>

<footer class="hiba-lab">
  <p>ÖkoTech Home — 2509 Esztergom, Strázsa u. 12. ·
     <a href="tel:+3633200211">+36 33 200 211</a> ·
     <a href="mailto:kapcsolat@okotechhome.hu">kapcsolat@okotechhome.hu</a></p>
</footer>

</body>
</html>
'''


def build(o):
    bek = '\n'.join(f'    <p class="hiba-szoveg">{p}</p>' for p in o['bekezdesek'])
    lnk = '\n'.join(f'      <li><a href="{h}">{t}</a></li>' for h, t in LINKEK)
    logo = '\n'.join('    ' + ln for ln in LOGO_INLINE.splitlines())
    return SABLON.format(logo=logo, kod=o['kod'], cim=o['cim'],
                         bekezdesek=bek, linkek=lnk,
                         gomb_href=o['gomb'][0], gomb_cimke=o['gomb'][1])


if __name__ == '__main__':
    css_out = WEB / 'assets' / 'css' / 'hiba.css'
    css_out.write_text(FEJLEC_CSS + CSS, encoding='utf-8')
    print(f"assets/css/hiba.css  {len(CSS)//1024} KB")
    for o in OLDALAK:
        p = WEB / o['fajl']
        p.write_text(build(o), encoding='utf-8')
        print(f"{o['fajl']:10s} {len(p.read_text(encoding='utf-8'))//1024} KB")
