# -*- coding: utf-8 -*-
"""Az MBBR-cikk két ábrája.

1. HOL ÉL A BIOMASSZA — Fixed Bed, MBBR és eleveniszap egymás mellett. Ez a
   cikk központi állítása képben: mindhárom ugyanazt a biológiai lehetőséget
   használja, csak másképp biztosít helyet a mikroorganizmusoknak.

2. A BIOFILM METSZETE — a cikk legérdekesebb szakasza: a néhány milliméteres
   rétegen BELÜL is eltérő körülmények alakulnak ki, mert az oxigén a hordozó
   felé haladva fogy. Egy apró hordozóelem felületén összetett mikrobiológiai
   ökoszisztéma működik; ezt mondatban nehéz, rajzban könnyű elmondani.

A SZÍNEK TOKENBŐL JÖNNEK (`--abra-*`), ugyanúgy, mint az SBR-ábrákon — így a
rajz témát vált a lappal. A mozgás a stíluslapban él, `prefers-reduced-motion`
mögött: a lebegő hordozók és a felszálló buborékok azt mutatják, amit a rajz
állít, semmivel sem többet.
"""

SZEL = 680


def hordozo(cx, cy, r=7, oszt='', stilus=''):
    """Egy biofilmhordozó elem. A klasszikus, bordázott hengeres hordozó
    felülnézete: kör, benne kereszt — ettől ismerhető fel, és ettől látszik,
    hogy a FELÜLET a lényeg, nem a test."""
    o = f' class="{oszt}"' if oszt else ''
    s = f' style="{stilus}"' if stilus else ''
    k = r * 0.62
    return (f'<g{o}{s} transform="translate({cx:.1f},{cy:.1f})">'
            f'<circle r="{r}" fill="var(--abra-hordozo)" stroke="var(--abra-kiemeles)" stroke-width="1.4"/>'
            f'<path d="M{-k} 0 H{k} M0 {-k} V{k}" stroke="var(--abra-kiemeles)" '
            f'stroke-width="1.2" opacity=".75"/></g>')


def pehely(cx, cy, r=5, oszt='', stilus=''):
    """Eleveniszap-pehely: szabálytalan folt, nem mértani alakzat — a
    különbség a hordozóhoz képest épp ez."""
    o = f' class="{oszt}"' if oszt else ''
    s = f' style="{stilus}"' if stilus else ''
    d = (f'M{-r} 0 Q{-r*0.8} {-r} 0 {-r*0.9} Q{r} {-r*0.9} {r*0.9} 0 '
         f'Q{r} {r*0.85} 0 {r} Q{-r*0.9} {r*0.9} {-r} 0 Z')
    return (f'<path{o}{s} transform="translate({cx:.1f},{cy:.1f})" d="{d}" '
            f'fill="var(--abra-iszap)" stroke="var(--abra-keret)" stroke-width="1" opacity=".9"/>')


def buborek_sor(x, w, y_alj, db, kulcs):
    ki = []
    for i in range(db):
        cx = x + w * (i + 1) / (db + 1)
        ki.append(f'<circle class="abra-bub" cx="{cx:.1f}" cy="{y_alj - 8}" r="{2.4 + (i % 3) * 0.6:.1f}" '
                  f'fill="var(--abra-kiemeles)" style="--i:{i}"/>')
    return ''.join(ki)


def harom_elv_svg():
    """Fixed Bed · MBBR · eleveniszap — hol él a biomassza?"""
    tw, res = 190, 35
    x0 = (SZEL - (3 * tw + 2 * res)) / 2       # 30
    ty, th = 56, 108
    alj = ty + th                               # 164

    def keret(x, cim, belul, jegyzet):
        return f'''
    <g>
      <rect x="{x}" y="{ty}" width="{tw}" height="{th}" rx="7" fill="var(--abra-viz)"/>
      {belul}
      <rect x="{x}" y="{ty}" width="{tw}" height="{th}" rx="7" fill="none"
            stroke="var(--abra-keret)" stroke-width="2.5"/>
      <text x="{x + tw / 2}" y="{ty - 22}" text-anchor="middle" class="abra-cimke abra-cimke-eros">{cim}</text>
      <text x="{x + tw / 2}" y="{alj + 24}" text-anchor="middle" class="abra-jegyzet">{jegyzet}</text>
    </g>'''

    # 1 · FIXED BED — a hordozó RÖGZÍTETT: egy helyben álló blokk, körülötte
    #     áramlik a víz. A rögzítést a tartófal jelzi.
    x = x0
    rogz = [f'<rect x="{x + 34}" y="{ty + 16}" width="{tw - 68}" height="{th - 46}" rx="4" '
            f'fill="var(--abra-hordozo)" stroke="var(--abra-kiemeles)" stroke-width="1.6" opacity=".9"/>']
    for sor in range(3):
        for osz in range(5):
            rogz.append(hordozo(x + 46 + osz * 28, ty + 28 + sor * 22, 6.5))
    rogz.append(f'<path d="M{x + 34} {ty + 10} H{x + tw - 34}" stroke="var(--abra-keret)" '
                f'stroke-width="2" stroke-linecap="round"/>')
    rogz.append(buborek_sor(x, tw, alj, 5, 'fb'))
    ki = [keret(x, 'Fixed Bed', ''.join(rogz), 'a hordozó a helyén marad')]

    # 2 · MBBR — a hordozók SZABADON MOZOGNAK a reaktortérben. A szórt
    #     elrendezés és a lebegés együtt mondja el, hogy nincsenek rögzítve.
    x = x0 + tw + res
    helyek = [(28, 24), (62, 42), (96, 20), (130, 46), (160, 28),
              (40, 66), (76, 78), (112, 62), (146, 80),
              (30, 94), (66, 100), (104, 92), (140, 102), (168, 70)]
    mozgo = [hordozo(x + hx, ty + hy, 7, 'abra-lebeg', f'--i:{i}')
             for i, (hx, hy) in enumerate(helyek)]
    mozgo.append(buborek_sor(x, tw, alj, 6, 'mbbr'))
    ki.append(keret(x, 'MBBR', ''.join(mozgo), 'a hordozó a vízzel együtt mozog'))

    # 3 · ELEVENISZAP — nincs mesterséges hordozófelület: a mikroorganizmusok
    #     jelentős része a vízben LEBEGŐ iszappelyhekben van jelen.
    x = x0 + 2 * (tw + res)
    pelyhek = [(32, 30), (64, 52), (98, 26), (128, 58), (158, 36),
               (44, 74), (80, 88), (116, 76), (150, 92),
               (26, 98), (68, 106), (104, 100), (140, 108), (170, 70)]
    lebego = [pehely(x + px, ty + py, 5.4, 'abra-lebeg', f'--i:{i}')
              for i, (px, py) in enumerate(pelyhek)]
    lebego.append(buborek_sor(x, tw, alj, 6, 'ei'))
    ki.append(keret(x, 'Eleveniszap', ''.join(lebego), 'a biomassza a vízben lebeg'))

    return f'''<svg class="abra-svg" viewBox="0 0 {SZEL} 210" role="img"
     aria-labelledby="abra-elvek-cim abra-elvek-leiras">
    <title id="abra-elvek-cim">Hol él a biomassza: Fixed Bed, MBBR és eleveniszap</title>
    <desc id="abra-elvek-leiras">Mindhárom megoldás ugyanazt a biológiai
    lehetőséget használja, csak másképp biztosít helyet a mikroorganizmusoknak.
    A Fixed Bed rögzített hordozón tartja a biofilmet; az MBBR-ben a
    hordozóelemek szabadon mozognak a reaktortérben; az eleveniszapos
    technológiában nincs mesterséges hordozófelület, a biomassza jelentős része
    a vízben lebegő iszappelyhekben van jelen. Mindhárom esetben levegőztetés
    biztosítja az oxigént.</desc>{''.join(ki)}
  </svg>'''


def biofilm_metszet_svg():
    """A biofilm metszete — miért nem homogén néhány milliméteren belül sem.

    A SZÍNÁTMENET AZ ÁLLÍTÁS, nem díszítés: az oxigén a víz felől a hordozó
    felé haladva fogy, és a rajz pontosan ezt mutatja. Az első változat két
    KÜLÖN téglalapra tette ugyanazt az átmenetet — mindkettő végigjátszotta,
    tehát a két réteg egyformának látszott, és épp az veszett el, amit a rajz
    mond. Egy réteg, egy átmenet, `userSpaceOnUse` egységben: így a szín a
    valódi távolsághoz igazodik, nem az elem saját dobozához."""
    y, h = 62, 92
    alj = y + h
    hx, hw = 76, 78                  # hordozó
    bx = hx + hw                     # a biofilm kezdete
    vx = bx + 200                    # a víz kezdete — a biofilm 200 egység
    kx = bx + 100                    # a belső/külső réteg jelképes határa
    vw = SZEL - 76 - vx

    # A BIOFILM „SZŐRÖS" FELSZÍNE a víz felé — ettől nem mértani sávnak
    # látszik, hanem élő rétegnek. Nagyobb kilengéssel, mint az első
    # változatban: ott alig lehetett észrevenni.
    fodor = f'M{vx} {y}'
    for i in range(6):
        yy = y + (i + 1) * h / 6
        ir = 7 if i % 2 == 0 else -6
        fodor += f' Q{vx + ir} {yy - h / 12:.1f} {vx} {yy:.1f}'

    def cimke(cx, szoveg, alcim):
        return (f'{chr(10)}    <text x="{cx:.0f}" y="{y - 30}" text-anchor="middle" '
                f'class="abra-cimke abra-cimke-eros">{szoveg}</text>'
                f'<text x="{cx:.0f}" y="{y - 15}" text-anchor="middle" '
                f'class="abra-jegyzet">{alcim}</text>')

    tengely_y = alj + 26
    return f'''<svg class="abra-svg" viewBox="0 0 {SZEL} 210" role="img"
     aria-labelledby="abra-biofilm-cim abra-biofilm-leiras">
    <title id="abra-biofilm-cim">A biofilm metszete: néhány milliméter, többféle környezet</title>
    <desc id="abra-biofilm-leiras">A hordozó felületén kialakuló biofilm nem
    homogén. A szennyvízzel érintkező külső réteg oxigénben gazdag, a hordozóhoz
    közelebbi belső területeken viszont az oxigén fogy — ezért ugyanazon a
    néhány milliméteres biológiai rétegen belül különböző mikrobiológiai
    folyamatok számára kedvező környezet jöhet létre. Az ábrán a biofilm
    színének erősödése a víz felé az oxigén növekvő mennyiségét jelöli.</desc>
    <defs>
      <linearGradient id="abra-biofilm" gradientUnits="userSpaceOnUse"
                      x1="{bx}" y1="0" x2="{vx}" y2="0">
        <stop offset="0" stop-color="var(--abra-biofilm-belso)"/>
        <stop offset="1" stop-color="var(--abra-biofilm-kulso)"/>
      </linearGradient>
    </defs>{cimke(hx + hw / 2, 'Hordozó', 'felületet ad')}{cimke(bx + 50, 'Belső réteg', 'kevés oxigén')}{cimke(kx + 50, 'Külső réteg', 'oxigéndús')}{cimke(vx + vw / 2, 'Szennyvíz', 'áramlik mellette')}
    <rect x="{hx}" y="{y}" width="{hw}" height="{h}" rx="4"
          fill="var(--abra-hordozo)" stroke="var(--abra-kiemeles)" stroke-width="1.6"/>
    <rect x="{bx}" y="{y}" width="{vx - bx}" height="{h}" fill="url(#abra-biofilm)"/>
    <rect x="{vx}" y="{y}" width="{vw}" height="{h}" rx="4" fill="var(--abra-viz)"/>
    <path d="M{kx} {y + 6} V{alj - 6}" stroke="var(--abra-keret)" stroke-width="1.2"
          stroke-dasharray="4 4" opacity=".6"/>
    <path d="{fodor}" fill="none" stroke="var(--abra-kiemeles)" stroke-width="2" opacity=".8"/>
    <rect x="{hx}" y="{y}" width="{vx + vw - hx}" height="{h}" rx="4" fill="none"
          stroke="var(--abra-keret)" stroke-width="2"/>

    <path class="abra-o2" d="M{vx - 6} {tengely_y} H{bx + 8}" fill="none"
          stroke="var(--abra-kiemeles)" stroke-width="2" stroke-linecap="round"/>
    <path d="M{bx + 14} {tengely_y - 5} L{bx + 8} {tengely_y} L{bx + 14} {tengely_y + 5}"
          fill="none" stroke="var(--abra-kiemeles)" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round"/>
    <text x="{(bx + vx) / 2:.0f}" y="{tengely_y + 22}" text-anchor="middle"
          class="abra-jegyzet">az oxigén befelé haladva fogy</text>
  </svg>'''
