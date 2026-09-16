# -*- coding: utf-8 -*-
"""A két technológiai elv ábrája. Két külön SVG, mert keskenyen egymás alá kell
kerülniük — egyetlen, széles rajz telefonon olvashatatlan volna.

A SZÍNEK TOKENBŐL JÖNNEK (`--abra-*`), nem beégetve: így a rajz témát vált a
lappal együtt. Az SVG-ben `currentColor` és `var()` keveredik; a `var()` az
SVG-ben is működik, ha a dokumentum CSS-e definiálja.

── MI VÁLTOZOTT AZ ELSŐ VÁLTOZATHOZ KÉPEST ────────────────────────────────────

Négy hiba volt benne, mind a rajz OLVASHATÓSÁGÁT rontotta:

  1. A be- és kilépő nyilak a tartály KERETÉRE estek, tehát félig eltűntek
     alatta. Most a tartályon KÍVÜL futnak, saját margóban — a rajzterület
     ezért lett szélesebb (440 → 480), nem azért, mert több fér bele.
  2. A negyedik fázis elvezető nyila a panel széléhez ért. Most 40 egység
     margó marad neki mindkét oldalon.
  3. A ciklusív a semmiből indult: nem kapcsolódott egyik tartályhoz sem.
     Most a 4. fázis alól indul, és NYÍLHEGGYEL ér vissza az 1. fázishoz —
     ettől látszik, hogy ugyanaz a tér kezdi elölről.
  4. A folyamatos átfolyású rajz NÉGY KÜLÖN TARTÁLYT mutatott. Az félrevezető:
     egyetlen tartály az, válaszfalakkal, és a víz átfolyó nyíláson megy
     kamráról kamrára. A vízszint ezért most VÉGIG AZONOS — közlekedőedények —,
     iszap pedig csak ott ül, ahol tényleg ülepszik.

Az ANIMÁCIÓ nem dísz: a levegőztetés buborékai, a ciklus futó szaggatása és az
átfolyó rajz haladó cseppje pontosan azt mutatják, amit a rajz állít. A
`prefers-reduced-motion` a stíluslapban kapuzza — lásd `app.css`, `.abra-*`.
"""

# A KÉSLELTETÉS OSZTÁLLYAL, nem `style="--i:N"`-nel. Az éles CSP
# (`style-src 'self'`) a soron belüli stílust eldobja — mérve 2026-09-16-án
# élesben minden buborék 0 s késleltetéssel, egyszerre indult. Az `abra-iN`
# osztály az app.css-ben állítja a `--i` értékét.

# A rajzterület. Minden koordináta ehhez képest értendő.
SZEL, MAG = 480, 262
TARTALY_Y, TARTALY_MAG = 52, 88
ALJ = TARTALY_Y + TARTALY_MAG          # 140
KOZEP_Y = TARTALY_Y + TARTALY_MAG / 2  # 96
MARGO = 40                             # a be- és kilépő nyilak helye


def nyil(x1, y, x2, oszt=''):
    """Vízszintes nyíl nyílheggyel. A hegy a VÉGÉN van, a haladás irányában."""
    h = 6 if x2 > x1 else -6
    o = f' class="{oszt}"' if oszt else ''
    return (f'<path{o} d="M{x1} {y} L{x2} {y} M{x2-h} {y-6} L{x2} {y} L{x2-h} {y+6}" '
            f'fill="none" stroke="var(--abra-jel)" stroke-width="2.5" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def viz(x, w, felso, also=ALJ):
    return (f'<rect x="{x}" y="{felso}" width="{w}" height="{also-felso}" '
            f'fill="var(--abra-viz)"/>')


def iszap(x, w, felso, also=ALJ):
    return (f'<rect x="{x}" y="{felso}" width="{w}" height="{also-felso}" '
            f'fill="var(--abra-iszap)"/>')


def buborekok(x, w, db=5, kulcs=''):
    """Felszálló buborékok. A késleltetés a sorszámból jön, nem véletlenből:
    generált fájlban a véletlen minden futáskor más rajzot adna."""
    ki = []
    for i in range(db):
        cx = x + w * (i + 1) / (db + 1)
        r = 2.6 + (i % 3) * 0.7
        ki.append(f'<circle class="abra-bub abra-i{i}" cx="{cx:.1f}" cy="{ALJ - 12}" r="{r:.1f}" '
                  f'fill="var(--abra-kiemeles)"/>')
    return ''.join(ki)


def badge(cx, szam):
    """Fázisszám korongban — a puszta szám a keret mellett elveszett."""
    return (f'<circle cx="{cx}" cy="28" r="13" fill="var(--abra-badge)" '
            f'stroke="var(--abra-kiemeles)" stroke-width="1.5"/>'
            f'<text x="{cx}" y="33" text-anchor="middle" class="abra-szam">{szam}</text>')


def sbr_svg():
    """SBR — UGYANAZ A TÉR, négy fázis IDŐBEN egymás után."""
    tw, res = 76, 32                       # tartályszélesség és köz
    x0 = MARGO                             # 40 … 440
    fazisok = []

    # 1 · FELTÖLTÉS — alacsony vízszint, a beérkező víz tölti
    x = x0
    fazisok.append((x, 'Feltöltés', viz(x + 3, tw - 6, ALJ - 30), ''))

    # 2 · LEVEGŐZTETÉS — tele, buborékokkal
    x = x0 + (tw + res)
    fazisok.append((x, 'Levegőztetés', viz(x + 3, tw - 6, TARTALY_Y + 14),
                    buborekok(x + 3, tw - 6)))

    # 3 · ÜLEPÍTÉS — az iszap leül, fölötte tisztul a víz
    x = x0 + 2 * (tw + res)
    fazisok.append((x, 'Ülepítés',
                    viz(x + 3, tw - 6, TARTALY_Y + 14, ALJ - 26) + iszap(x + 3, tw - 6, ALJ - 26),
                    f'<path d="M{x+14} {ALJ-34} L{x+tw-14} {ALJ-34}" stroke="var(--abra-jel)" '
                    f'stroke-width="1.5" stroke-dasharray="4 4" opacity=".7"/>'))

    # 4 · ELVEZETÉS — a tisztított víz fölülről megy el, az iszap marad
    x = x0 + 3 * (tw + res)
    fazisok.append((x, 'Elvezetés',
                    viz(x + 3, tw - 6, TARTALY_Y + 34, ALJ - 26) + iszap(x + 3, tw - 6, ALJ - 26), ''))

    ki = []
    for i, (x, cimke, kitoltes, extra) in enumerate(fazisok):
        ki.append(f'''
    <g>
      {badge(x + tw / 2, i + 1)}
      {kitoltes}
      <rect x="{x}" y="{TARTALY_Y}" width="{tw}" height="{TARTALY_MAG}" rx="6"
            fill="none" stroke="var(--abra-keret)" stroke-width="2.5"/>
      {extra}
      <text x="{x + tw / 2}" y="{ALJ + 24}" text-anchor="middle" class="abra-cimke">{cimke}</text>
    </g>''')

    # A BE- ÉS KILÉPŐ NYÍL A TARTÁLYON KÍVÜL — hat egység hézaggal, hogy a
    # keret ne takarja el. Ez volt az eredeti rajz legláthatóbb hibája.
    ki.append('\n    ' + nyil(12, KOZEP_Y, x0 - 8))
    utolso_jobb = x0 + 3 * (tw + res) + tw
    ki.append('\n    ' + nyil(utolso_jobb + 8, KOZEP_Y, SZEL - 12))

    # A CIKLUS visszazáró íve: a 4. fázis alól indul, és NYÍLHEGGYEL ér vissza
    # az 1.-hez. Így látszik, hogy ugyanaz a tér kezdi elölről.
    bal = x0 + tw / 2
    jobb = x0 + 3 * (tw + res) + tw / 2
    ki.append(f'''
    <path class="abra-ciklus" d="M{jobb} {ALJ + 34} L{jobb} {ALJ + 50}
             Q{jobb} {ALJ + 60} {jobb - 10} {ALJ + 60}
             L{bal + 10} {ALJ + 60} Q{bal} {ALJ + 60} {bal} {ALJ + 50} L{bal} {ALJ + 36}"
          fill="none" stroke="var(--abra-jel)" stroke-width="2" stroke-dasharray="6 5"/>
    <path d="M{bal - 6} {ALJ + 42} L{bal} {ALJ + 34} L{bal + 6} {ALJ + 42}" fill="none"
          stroke="var(--abra-jel)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="{SZEL / 2}" y="{MAG - 8}" text-anchor="middle" class="abra-jegyzet">a ciklus újraindul</text>''')

    return f'''<svg class="abra-svg" viewBox="0 0 {SZEL} {MAG}" role="img"
     aria-labelledby="abra-sbr-cim abra-sbr-leiras">
    <title id="abra-sbr-cim">SBR: egy reaktortér, négy fázis egymás után</title>
    <desc id="abra-sbr-leiras">Ugyanabban a tartályban zajlik a feltöltés, a
    levegőztetés, az ülepítés és a tisztított víz elvezetése — egymás után,
    időben elválasztva. Az ülepítés után a leülepedett iszap a tartály alján
    marad, a fölötte kitisztult vizet vezetik el. A ciklus végén minden
    kezdődik elölről.</desc>{''.join(ki)}
  </svg>'''


def atfolyo_svg():
    """Folyamatos átfolyás — UGYANAZ AZ IDŐ, a fázisok TÉRBEN elválasztva.

    EGY TARTÁLY, válaszfalakkal. Az első változat négy különálló dobozt
    rajzolt, ami félrevezető: a kamrák közlekedőedények, tehát a vízszint
    végig azonos, és a víz átfolyó nyíláson megy tovább."""
    kamrak = ['Fogadás', 'Levegőztetés', 'Ülepítés', 'Elvezetés']
    x0, tw = MARGO, SZEL - 2 * MARGO       # 40 … 440
    kw = tw / len(kamrak)                  # 100
    vizszint = TARTALY_Y + 16              # KÖZLEKEDŐEDÉNYEK: végig azonos
    nyilas_y = TARTALY_Y + 44              # az átfolyó nyílás közepe

    ki = ['\n    ' + viz(x0 + 2, tw - 4, vizszint)]

    # Iszap csak ott, ahol tényleg ülepszik: a fogadó- és az ülepítőkamrában.
    for i in (0, 2):
        ki.append(iszap(x0 + i * kw + 3, kw - 6, ALJ - 24))

    # A tartály EGY keret, a válaszfalak belül — mindegyiken egy nyílással.
    ki.append(f'''
    <rect x="{x0}" y="{TARTALY_Y}" width="{tw}" height="{TARTALY_MAG}" rx="6"
          fill="none" stroke="var(--abra-keret)" stroke-width="2.5"/>''')
    for i in range(1, len(kamrak)):
        fx = x0 + i * kw
        ki.append(f'''
    <path d="M{fx} {TARTALY_Y + 4} L{fx} {nyilas_y - 11} M{fx} {nyilas_y + 11} L{fx} {ALJ - 4}"
          stroke="var(--abra-keret)" stroke-width="2.5" stroke-linecap="round"/>''')

    ki.append(buborekok(x0 + kw + 3, kw - 6, 4))

    # A VÍZ ÚTJA: a nyílásokon át, kamráról kamrára. A haladó csepp ezen fut.
    ut = f'M{x0 - 8} {KOZEP_Y}'
    for i in range(1, len(kamrak)):
        fx = x0 + i * kw
        ut += f' L{fx - 22} {KOZEP_Y} L{fx} {nyilas_y} L{fx + 22} {KOZEP_Y}'
    ut += f' L{x0 + tw + 8} {KOZEP_Y}'
    ki.append(f'''
    <path id="abra-utvonal" class="abra-ut" d="{ut}" fill="none"
          stroke="var(--abra-jel)" stroke-width="1.5" stroke-dasharray="5 5" opacity=".55"/>
    <circle class="abra-csepp" cx="{x0 - 8}" cy="{KOZEP_Y}" r="4" fill="var(--abra-kiemeles)">
      <animateMotion dur="9s" repeatCount="indefinite" calcMode="linear">
        <mpath href="#abra-utvonal" xlink:href="#abra-utvonal"/>
      </animateMotion>
    </circle>''')

    for i, nev in enumerate(kamrak):
        ki.append(f'''
    <text x="{x0 + i * kw + kw / 2}" y="{ALJ + 24}" text-anchor="middle" class="abra-cimke">{nev}</text>''')

    ki.append('\n    ' + nyil(12, KOZEP_Y, x0 - 8))
    ki.append('\n    ' + nyil(x0 + tw + 8, KOZEP_Y, SZEL - 12))
    ki.append(f'''
    <text x="{SZEL / 2}" y="{MAG - 8}" text-anchor="middle" class="abra-jegyzet">a szennyvíz végighalad a kamrákon</text>''')

    return f'''<svg class="abra-svg" viewBox="0 0 {SZEL} {MAG}" role="img"
     xmlns:xlink="http://www.w3.org/1999/xlink"
     aria-labelledby="abra-atfolyo-cim abra-atfolyo-leiras">
    <title id="abra-atfolyo-cim">Folyamatos átfolyás: egy tartály, a fázisok térben</title>
    <desc id="abra-atfolyo-leiras">A szennyvíz egyetlen tartályon halad
    keresztül, amit válaszfalak osztanak egymást követő, különböző funkciójú
    kamrákra. A válaszfalakon átfolyó nyílás van, a vízszint ezért minden
    kamrában azonos. A fázisok elkülönítését a tartály kialakítása biztosítja,
    nem az időzítés.</desc>{''.join(ki)}
  </svg>'''
