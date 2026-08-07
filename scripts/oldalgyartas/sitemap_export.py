#!/usr/bin/env python3
"""Oldaltérkép-export a tényleges menüszerkezetből.

A fejlec.py MENU/KESZUL/MASODLAGOS adatait olvassa, minden csomópontnál
ellenőrzi, hogy a hozzá tartozó HTML létezik-e, és két kimenetet ír:

  _files/sitemap-menurendszer.md    — szöveges fa, továbbküldhető
  _files/sitemap-menurendszer.html  — vizuális oldaltérkép (önhordó)

A HTML a márka tokenjeit használja, a betűtípusok base64-ben beágyazva
(a fonts.css-t a build_fonts() állítja elő, ha még nincs meg).

Futtatás a repo gyökeréből:  python3 scripts/oldalgyartas/sitemap_export.py
"""
from __future__ import annotations

import html
import json
import pathlib
import sys

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / "_web"
KIMENET = GYOKER / "_files"
sys.path.insert(0, str(GYOKER / "scripts" / "oldalgyartas"))

import fejlec  # noqa: E402

DATUM = "2026. augusztus 7."
VERZIO = (GYOKER / "VERSION").read_text().strip()

# A rendszer- és jogi oldalak nem a főmenüből nyílnak, de a teljes
# oldaltérkép része, ezért itt soroljuk fel őket.
JOGI = [
    ("Kapcsolat", "kapcsolat"),
    ("Adatkezelési tájékoztató", "adatkezelesi-tajekoztato"),
    ("Cookie-tájékoztató", "cookie-tajekoztato"),
    ("Általános Szerződési Feltételek", "aszf"),
    ("Jogi nyilatkozat", "jogi-nyilatkozat"),
    ("Akadálymentességi nyilatkozat", "akadalymentessegi-nyilatkozat"),
    ("404 — nem található", "404"),
    ("403 — hozzáférés megtagadva", "403"),
]

# Eltérések az eredeti Site map.docx-től, amiket dokumentálni kell.
ELTERESEK = [
    ("Összevonás", "A.B.Clear termékcsalád › Termékcsalád áttekintése",
     "A hub első gyereke önmaga áttekintése volt. A tartalom felkerült a hubba, "
     "az aloldal megszűnt. Ugyanez az EPURECO-nál és a Nagyobb rendszereknél. "
     "Tartalom nem veszett el, egy kattintás igen."),
    ("Névváltozás", "Projekt-előkészítés",
     "Az eredeti sitemapben ez a csomópont a Megoldások alatt szerepelt. "
     "Önálló főmenüponttá vált, mert mindhárom hubja (telekalkalmasság, "
     "vízelhelyezés, terhelés) megoldástípustól függetlenül érvényes."),
    ("Kiegészítés", "Rendszer- és jogi oldalak",
     "Az eredeti sitemap nem tartalmazta. A láblécből érhetők el, "
     "a főmenüben szándékosan nem jelennek meg."),
]


def van(url: str | None) -> bool:
    if not url:
        return False
    rel = url.rstrip("/") + "/index.html" if url.endswith("/") else url + ".html"
    return (WEB / rel).exists()


def utvonal(url: str | None) -> str:
    return "/" + url if url else "—"


# --------------------------------------------------------------- 1. ADATFA
def fa() -> list[dict]:
    ki: list[dict] = []
    for kat, katurl, hubok in fejlec.MENU:
        ki.append({
            "nev": kat, "url": katurl, "kesz": van(katurl), "tipus": "fo",
            "hubok": [{
                "nev": cim, "url": hurl, "kesz": van(hurl),
                "csalad": cim.startswith("↳"),
                "alok": [{"nev": c, "url": u, "kesz": van(u)} for c, u in alok],
            } for _ikon, cim, hurl, alok in hubok],
        })
    for kat, tervek in fejlec.KESZUL:
        ki.append({
            "nev": kat, "url": None, "kesz": False, "tipus": "terv",
            "hubok": [{"nev": t, "url": None, "kesz": False,
                       "csalad": False, "alok": []} for t in tervek],
        })
    for cim, url in fejlec.MASODLAGOS:
        ki.append({"nev": cim, "url": url, "kesz": van(url),
                   "tipus": "terv", "hubok": []})
    ki.append({
        "nev": "Rendszer- és jogi oldalak", "url": None, "kesz": True,
        "tipus": "jogi",
        "hubok": [{"nev": c, "url": u, "kesz": van(u),
                   "csalad": False, "alok": []} for c, u in JOGI],
    })
    return ki


def szamok(t: list[dict]) -> dict:
    hubok = [h for k in t for h in k["hubok"]]
    alok = [a for h in hubok for a in h["alok"]]
    return {
        "fo": len([k for k in t if k["tipus"] != "jogi"]),
        "fo_kesz": len([k for k in t if k["tipus"] == "fo"]),
        "hub": len(hubok), "hub_kesz": len([h for h in hubok if h["kesz"]]),
        "alo": len(alok), "alo_kesz": len([a for a in alok if a["kesz"]]),
        "ossz": len(hubok) + len(alok),
        "ossz_kesz": len([h for h in hubok if h["kesz"]]) + len([a for a in alok if a["kesz"]]),
        "html": len(list(WEB.rglob("*.html"))),
    }


# ------------------------------------------------------------ 2. MARKDOWN
def markdown(t: list[dict], sz: dict) -> str:
    s = [f"# ÖkoTech Home — menürendszer és oldaltérkép",
         "",
         f"Állapot: {DATUM} · verzió {VERZIO}",
         "",
         f"- Főmenüpont: **{sz['fo']}** (ebből megépült: {sz['fo_kesz']})",
         f"- Hub: **{sz['hub']}** (megépült: {sz['hub_kesz']})",
         f"- Aloldal: **{sz['alo']}** (megépült: {sz['alo_kesz']})",
         f"- Menücsomópont összesen: **{sz['ossz']}**, ebből megépült: **{sz['ossz_kesz']}**",
         f"- Legenerált HTML-fájl a repóban: **{sz['html']}**",
         "",
         "Jelölés: `[+]` megépült oldal · `[ ]` tervezett, még nem létező oldal.",
         "A megamenü mindhárom szintet mutatja: főmenüpont › hub › aloldal.",
         "", "---", ""]

    for kat in t:
        jel = "[+]" if kat["kesz"] else "[ ]"
        s.append(f"## {jel} {kat['nev']}  `{utvonal(kat['url'])}`")
        s.append("")
        for i, h in enumerate(kat["hubok"]):
            utolso = i == len(kat["hubok"]) - 1
            hj = "[+]" if h["kesz"] else "[ ]"
            ag = "└── " if utolso else "├── "
            s.append(f"{ag}{hj} {h['nev']}  `{utvonal(h['url'])}`")
            szulo = "    " if utolso else "│   "
            for j, a in enumerate(h["alok"]):
                aj = "[+]" if a["kesz"] else "[ ]"
                aag = "└── " if j == len(h["alok"]) - 1 else "├── "
                s.append(f"{szulo}{aag}{aj} {a['nev']}  `{utvonal(a['url'])}`")
        s.append("")

    s += ["---", "", "## Eltérések az eredeti sitemaptől", ""]
    for tip, mit, miert in ELTERESEK:
        s.append(f"**{tip} — {mit}**")
        s.append("")
        s.append(miert)
        s.append("")
    return "\n".join(s) + "\n"


# ---------------------------------------------------------------- 3. HTML
def h(sz: str) -> str:
    return html.escape(sz, quote=False)


def html_doc(t: list[dict], sz: dict) -> str:
    fonts = (GYOKER / "scripts" / "oldalgyartas" / "_fonts.css")
    fontcss = fonts.read_text() if fonts.exists() else ""

    savok = []
    for kat in t:
        allap = "kesz" if kat["kesz"] else "terv"
        hk = len(kat["hubok"])
        ak = sum(len(x["alok"]) for x in kat["hubok"])
        meta = []
        if hk:
            meta.append(f"{hk} hub")
        if ak:
            meta.append(f"{ak} aloldal")
        oszlopok = []
        for hub in kat["hubok"]:
            nev = h(hub["nev"].lstrip("↳ "))
            csal = " oszlop-csalad" if hub["csalad"] else ""
            allo = "kesz" if hub["kesz"] else "terv"
            tetelek = "".join(
                f'<li class="tetel" data-allapot="{"kesz" if a["kesz"] else "terv"}">'
                f'<span class="tetel-cim">{h(a["nev"])}</span></li>'
                for a in hub["alok"])
            lista = f'<ul class="alista">{tetelek}</ul>' if tetelek else ""
            slug = (f'<code class="slug">{h(utvonal(hub["url"]))}</code>'
                    if hub["url"] else "")
            oszlopok.append(
                f'<div class="oszlop{csal}" data-allapot="{allo}">'
                f'<h3 class="oszlop-cim">{nev}</h3>{slug}{lista}</div>')
        kslug = (f'<code class="slug slug-fo">{h(utvonal(kat["url"]))}</code>'
                 if kat["url"] else "")
        savok.append(
            f'<section class="sav" data-allapot="{allap}">'
            f'<header class="sav-fej">'
            f'<h2 class="sav-cim">{h(kat["nev"])}</h2>{kslug}'
            f'<span class="sav-meta">{" · ".join(meta) or "tervezés alatt"}</span>'
            f'</header>'
            f'<div class="oszlopok">{"".join(oszlopok)}</div>'
            f'</section>')

    sorok = []
    for kat in t:
        for hub in kat["hubok"]:
            sorok.append((1, kat["nev"], hub["nev"].lstrip("↳ "), hub["url"], hub["kesz"]))
            for a in hub["alok"]:
                sorok.append((2, kat["nev"], a["nev"], a["url"], a["kesz"]))
    index = "".join(
        f'<tr data-allapot="{"kesz" if k else "terv"}" data-szint="{m}">'
        f'<td class="ix-kat">{h(katn)}</td>'
        f'<td class="ix-cim">{h(cim)}</td>'
        f'<td class="ix-url"><code>{h(utvonal(u))}</code></td>'
        f'<td class="ix-all">{"él" if k else "terv"}</td></tr>'
        for m, katn, cim, u, k in sorok)

    elter = "".join(
        f'<div class="elteres"><span class="elteres-tip">{h(tip)}</span>'
        f'<h3 class="elteres-cim">{h(mit)}</h3><p>{h(miert)}</p></div>'
        for tip, mit, miert in ELTERESEK)

    return TPL.format(
        fontcss=fontcss, datum=DATUM, verzio=VERZIO,
        fo=sz["fo"], fo_kesz=sz["fo_kesz"], hub=sz["hub"], hub_kesz=sz["hub_kesz"],
        alo=sz["alo"], alo_kesz=sz["alo_kesz"], ossz=sz["ossz"],
        ossz_kesz=sz["ossz_kesz"], szazalek=round(sz["ossz_kesz"] / sz["ossz"] * 100),
        savok="".join(savok), index=index, elteresek=elter)


TPL = """<meta charset="utf-8">
<title>ÖkoTech Home — menürendszer és oldaltérkép</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{fontcss}

:root {{
  --forest:#133216; --oliveleaf:#56642B; --fern:#80A640; --lime:#E5EBBB;
  --drizzle:#F3F2EC; --stardust:#FAFAFA; --seamist:#DEECEA; --amber:#C98A1D;

  --ground:var(--drizzle); --surface:var(--stardust); --sunken:#EBEAE1;
  --ink:var(--forest); --ink-2:var(--oliveleaf); --ink-3:#7C8560;
  --vonal:#DDDCCF; --vonal-halk:#E8E7DC;
  --el:var(--fern); --terv:var(--amber);
  --font-fej:'Zilla Slab',Georgia,serif;
  --font-torzs:'IBM Plex Sans',system-ui,sans-serif;
  --font-adat:'IBM Plex Mono',ui-monospace,monospace;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --ground:#0E2612; --surface:#16331A; --sunken:#1C3D20;
    --ink:#EDF2E2; --ink-2:#B9C99A; --ink-3:#8B9C6E;
    --vonal:#2A4A2C; --vonal-halk:#213C24;
    --el:#9CC258; --terv:#DFA742;
  }}
}}
:root[data-theme="dark"] {{
  --ground:#0E2612; --surface:#16331A; --sunken:#1C3D20;
  --ink:#EDF2E2; --ink-2:#B9C99A; --ink-3:#8B9C6E;
  --vonal:#2A4A2C; --vonal-halk:#213C24;
  --el:#9CC258; --terv:#DFA742;
}}
:root[data-theme="light"] {{
  --ground:#F3F2EC; --surface:#FAFAFA; --sunken:#EBEAE1;
  --ink:#133216; --ink-2:#56642B; --ink-3:#7C8560;
  --vonal:#DDDCCF; --vonal-halk:#E8E7DC;
  --el:#80A640; --terv:#C98A1D;
}}

* {{ box-sizing:border-box }}
body {{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:var(--font-torzs); font-size:15px; line-height:1.55;
  -webkit-font-smoothing:antialiased;
}}
.lap {{ max-width:1180px; margin:0 auto; padding:clamp(1.5rem,4vw,4rem) clamp(1rem,4vw,3rem) 6rem }}

/* --- fejléc --- */
.fej {{ border-bottom:2px solid var(--ink); padding-bottom:1.75rem }}
.eyebrow {{
  font-family:var(--font-adat); font-size:11px; letter-spacing:.16em;
  text-transform:uppercase; color:var(--ink-2); margin:0 0 1rem;
  display:flex; flex-wrap:wrap; gap:.5rem 1.25rem;
}}
h1 {{
  font-family:var(--font-fej); font-weight:600; font-size:clamp(2rem,5vw,3.25rem);
  line-height:1.05; letter-spacing:-.02em; margin:0; text-wrap:balance;
}}
.alcim {{ margin:.9rem 0 0; max-width:62ch; color:var(--ink-2); font-size:1.0625rem }}

/* --- mérőszámok --- */
.szamok {{
  display:grid; grid-template-columns:repeat(auto-fit,minmax(9rem,1fr));
  gap:1px; background:var(--vonal); border:1px solid var(--vonal);
  margin:2.5rem 0 0;
}}
.szam {{ background:var(--surface); padding:1rem 1.15rem }}
.szam-ertek {{
  font-family:var(--font-adat); font-size:1.875rem; font-weight:500;
  line-height:1.1; font-variant-numeric:tabular-nums; display:block;
}}
.szam-ertek small {{ font-size:.9rem; color:var(--ink-3) }}
.szam-cimke {{
  font-family:var(--font-adat); font-size:10.5px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--ink-3); margin-top:.4rem; display:block;
}}

/* --- jelmagyarázat --- */
.jelek {{
  display:flex; flex-wrap:wrap; gap:.5rem 2rem; margin:1.25rem 0 0;
  font-family:var(--font-adat); font-size:11.5px; color:var(--ink-2);
}}
.jel {{ display:flex; align-items:center; gap:.5rem }}
.pont {{ width:8px; height:8px; flex:none }}
.pont-el {{ background:var(--el) }}
.pont-terv {{ border:1.5px dashed var(--terv) }}

/* --- sávok --- */
.sav {{ margin-top:4rem }}
.sav-fej {{
  display:flex; align-items:baseline; flex-wrap:wrap; gap:.6rem 1rem;
  padding-bottom:.7rem; border-bottom:1px solid var(--ink);
}}
.sav-cim {{
  font-family:var(--font-fej); font-weight:500; font-size:1.6rem;
  letter-spacing:-.01em; margin:0; line-height:1.15;
}}
.sav[data-allapot="terv"] .sav-cim {{ color:var(--ink-2) }}
.sav[data-allapot="terv"] .sav-fej {{ border-bottom-color:var(--vonal) }}
.sav-meta {{
  margin-left:auto; font-family:var(--font-adat); font-size:11px;
  letter-spacing:.1em; text-transform:uppercase; color:var(--ink-3);
}}
.slug {{
  font-family:var(--font-adat); font-size:11.5px; color:var(--ink-3);
  overflow-wrap:anywhere;
}}
.slug-fo {{ color:var(--ink-2) }}

.oszlopok {{
  display:grid; grid-template-columns:repeat(auto-fill,minmax(14.5rem,1fr));
  gap:0;
}}
.oszlop {{
  padding:1.35rem 1.25rem 1.5rem; border-bottom:1px solid var(--vonal-halk);
  border-right:1px solid var(--vonal-halk);
}}
.oszlop-csalad {{ background:var(--sunken) }}
.oszlop-cim {{
  font-family:var(--font-torzs); font-weight:600; font-size:.95rem;
  line-height:1.3; margin:0 0 .3rem; text-wrap:balance;
}}
.oszlop-csalad .oszlop-cim::before {{
  content:'↳ '; color:var(--el); font-family:var(--font-adat);
}}
.oszlop[data-allapot="terv"] .oszlop-cim {{ color:var(--ink-2) }}
.oszlop[data-allapot="terv"] .oszlop-cim::after {{
  content:'terv'; font-family:var(--font-adat); font-size:9.5px;
  letter-spacing:.12em; text-transform:uppercase; color:var(--terv);
  border:1px solid var(--terv); padding:.1em .4em; margin-left:.5em;
  vertical-align:.15em; white-space:nowrap;
}}

.alista {{ list-style:none; margin:.85rem 0 0; padding:0 }}
.tetel {{
  position:relative; padding-left:1.5rem; font-size:.875rem;
  line-height:1.45; margin-bottom:.4rem; color:var(--ink-2);
}}
.tetel::before {{
  content:'├'; position:absolute; left:0; top:0;
  font-family:var(--font-adat); color:var(--vonal); font-size:.875rem;
}}
.tetel:last-child::before {{ content:'└' }}
.tetel::after {{
  content:''; position:absolute; left:.62rem; top:.62em;
  width:.55rem; height:1px; background:var(--vonal);
}}
/* A kész oldal az alapeset — jelöletlen. A kivételt jelöljük. */
.tetel[data-allapot="terv"] {{ color:var(--ink-3) }}
.tetel[data-allapot="terv"] .tetel-cim {{
  border-bottom:1px dashed var(--terv); padding-bottom:1px;
}}

/* --- eltérések --- */
.elteresek {{
  margin-top:4.5rem; border-top:2px solid var(--ink); padding-top:1.75rem;
}}
.elteres-racs {{
  display:grid; grid-template-columns:repeat(auto-fit,minmax(17rem,1fr));
  gap:1px; background:var(--vonal); border:1px solid var(--vonal); margin-top:1.5rem;
}}
.elteres {{ background:var(--surface); padding:1.25rem }}
.elteres-tip {{
  font-family:var(--font-adat); font-size:10px; letter-spacing:.14em;
  text-transform:uppercase; color:var(--el);
}}
.elteres-cim {{
  font-family:var(--font-fej); font-weight:500; font-size:1.0625rem;
  margin:.45rem 0 .5rem; line-height:1.25;
}}
.elteres p {{ margin:0; font-size:.875rem; color:var(--ink-2) }}

/* --- URL-index --- */
.index {{ margin-top:4.5rem; border-top:2px solid var(--ink); padding-top:1.75rem }}
h2.blokk-cim {{
  font-family:var(--font-fej); font-weight:600; font-size:1.5rem;
  margin:0; letter-spacing:-.01em;
}}
.blokk-alcim {{ margin:.5rem 0 0; color:var(--ink-2); font-size:.9375rem; max-width:60ch }}
.tabla-keret {{ overflow-x:auto; margin-top:1.5rem; border:1px solid var(--vonal) }}
table {{ border-collapse:collapse; width:100%; background:var(--surface); font-size:.8125rem }}
th {{
  font-family:var(--font-adat); font-size:10px; letter-spacing:.13em;
  text-transform:uppercase; text-align:left; color:var(--ink-3);
  padding:.6rem .8rem; border-bottom:1px solid var(--vonal); white-space:nowrap;
  position:sticky; top:0; background:var(--surface);
}}
td {{ padding:.42rem .8rem; border-bottom:1px solid var(--vonal-halk); vertical-align:top }}
tr:last-child td {{ border-bottom:0 }}
.ix-kat {{ color:var(--ink-3); white-space:nowrap; width:1%; padding-left:1rem }}
.ix-cim {{ font-weight:400; white-space:nowrap }}
tr[data-szint="1"] .ix-cim {{ font-weight:600 }}
tr[data-szint="2"] .ix-cim {{ padding-left:2.2rem }}
.ix-url code {{ font-family:var(--font-adat); font-size:11.5px; color:var(--ink-2) }}
.ix-all {{
  font-family:var(--font-adat); font-size:10.5px; letter-spacing:.1em;
  text-transform:uppercase; white-space:nowrap; width:4rem;
}}
tr[data-allapot="kesz"] .ix-all {{ color:var(--el) }}
tr[data-allapot="terv"] .ix-all {{ color:var(--terv) }}
tr[data-allapot="terv"] .ix-cim {{ color:var(--ink-3); font-weight:400 }}

.zaras {{
  margin-top:3.5rem; padding-top:1.25rem; border-top:1px solid var(--vonal);
  font-family:var(--font-adat); font-size:11px; color:var(--ink-3);
  display:flex; flex-wrap:wrap; gap:.4rem 1.5rem;
}}

@media (max-width:640px) {{
  .oszlop {{ border-right:0 }}
  .sav-meta {{ margin-left:0 }}
}}
@media print {{
  body {{ background:#fff; color:#000 }}
  .lap {{ max-width:none; padding:0 }}
  .sav {{ break-inside:avoid; margin-top:2rem }}
  .oszlop {{ break-inside:avoid }}
  th {{ position:static }}
}}
</style>

<div class="lap">
  <header class="fej">
    <p class="eyebrow"><span>ÖkoTech Home</span><span>Menürendszer</span>
      <span>{datum}</span><span>v{verzio}</span></p>
    <h1>Oldaltérkép a megépült navigációról</h1>
    <p class="alcim">A megamenü mindhárom szintje kinyomtatva: főmenüpont, hub, aloldal.
      Ez a dokumentum a tényleges menüadatból készült, nem kézzel — ami itt szerepel,
      az a fejlécben is szerepel, és fordítva.</p>

    <div class="szamok">
      <div class="szam"><span class="szam-ertek">{fo}<small> / {fo_kesz} él</small></span>
        <span class="szam-cimke">Főmenüpont</span></div>
      <div class="szam"><span class="szam-ertek">{hub}<small> / {hub_kesz} él</small></span>
        <span class="szam-cimke">Hub</span></div>
      <div class="szam"><span class="szam-ertek">{alo}<small> / {alo_kesz} él</small></span>
        <span class="szam-cimke">Aloldal</span></div>
      <div class="szam"><span class="szam-ertek">{ossz_kesz}<small> / {ossz}</small></span>
        <span class="szam-cimke">Megépült · {szazalek}%</span></div>
    </div>

    <p class="jelek">
      <span class="jel"><span class="pont pont-el"></span>jelöletlen oldal = megépült és elérhető</span>
      <span class="jel"><span class="pont pont-terv"></span>szaggatottal jelölve = tervezett, a menüben látszik, de nem kattintható</span>
      <span class="jel">↳ termékcsalád a fölötte lévő technológia alatt</span>
    </p>
  </header>

  {savok}

  <section class="elteresek">
    <h2 class="blokk-cim">Eltérés az eredeti sitemaptől</h2>
    <p class="blokk-alcim">Három ponton tér el a megépült szerkezet a leadott
      Site map dokumentumtól. Mindhárom szándékos, és mindhárom indoklással.</p>
    <div class="elteres-racs">{elteresek}</div>
  </section>

  <section class="index">
    <h2 class="blokk-cim">URL-index</h2>
    <p class="blokk-alcim">Minden menücsomópont útvonala egy helyen — átirányításokhoz,
      SEO-hoz és fejlesztői átadáshoz.</p>
    <div class="tabla-keret">
      <table>
        <thead><tr><th>Főmenüpont</th><th>Oldal</th><th>Útvonal</th><th>Állapot</th></tr></thead>
        <tbody>{index}</tbody>
      </table>
    </div>
  </section>

  <p class="zaras"><span>ÖkoTech Home · okotechhome.hu</span>
    <span>Generálva: scripts/oldalgyartas/sitemap_export.py</span>
    <span>Állapot: {datum}</span></p>
</div>
"""


def main() -> None:
    t = fa()
    sz = szamok(t)
    KIMENET.mkdir(exist_ok=True)
    (KIMENET / "sitemap-menurendszer.md").write_text(markdown(t, sz), encoding="utf-8")
    (KIMENET / "sitemap-menurendszer.html").write_text(html_doc(t, sz), encoding="utf-8")
    print(json.dumps(sz, ensure_ascii=False))
    print("→ _files/sitemap-menurendszer.md")
    print("→ _files/sitemap-menurendszer.html")


if __name__ == "__main__":
    main()
