# -*- coding: utf-8 -*-
"""A két technológiai elv ábrája. Két külön SVG, mert keskenyen egymás alá kell
kerülniük — egyetlen, széles rajz telefonon olvashatatlan volna.

A SZÍNEK TOKENBŐL JÖNNEK (`--abra-*`), nem beégetve: így a rajz témát vált a
lappal együtt. Az SVG-ben `currentColor` és `var()` keveredik; a `var()` az
SVG-ben is működik, ha a dokumentum CSS-e definiálja.
"""

def tartaly(x, y, w, h, viz_felso=None, iszap=0, extra=''):
    """Egy tartály: keret + vízszint + (opcionálisan) leülepedett iszap."""
    r = []
    if viz_felso is not None:
        vy = y + viz_felso
        vh = h - viz_felso - iszap
        if vh > 0:
            r.append(f'<rect x="{x+3}" y="{vy}" width="{w-6}" height="{vh}" '
                     f'fill="var(--abra-viz)" rx="2"/>')
    if iszap:
        r.append(f'<rect x="{x+3}" y="{y+h-iszap}" width="{w-6}" height="{iszap-3}" '
                 f'fill="var(--abra-iszap)" rx="2"/>')
    r.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="none" '
             f'stroke="var(--abra-keret)" stroke-width="2.5"/>')
    return '\n      '.join(r) + ('\n      ' + extra if extra else '')


def sbr_svg():
    """SBR — ugyanaz a tér, négy fázis IDŐBEN."""
    fazisok = [
        ('1', 'Feltöltés', 62, 0,
         '<path d="M18 26 L18 44 M12 38 L18 45 L24 38" stroke="var(--abra-jel)" '
         'stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'),
        ('2', 'Levegőztetés', 18, 0,
         ''.join(f'<circle cx="{28+i*13}" cy="{92-((i*17)%38)}" r="{3.2-(i%3)*0.6:.1f}" '
                 f'fill="var(--abra-kiemeles)"/>' for i in range(5))),
        ('3', 'Ülepítés', 18, 26, ''),
        ('4', 'Elvezetés', 18, 26,
         '<path d="M92 44 L112 44 M106 38 L113 44 L106 50" stroke="var(--abra-jel)" '
         'stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'),
    ]
    ki = []
    for i, (szam, cimke, vf, isz, extra) in enumerate(fazisok):
        x = 14 + i * 106
        ki.append(f'''<g transform="translate({x},0)">
      <text x="43" y="22" text-anchor="middle" class="abra-szam">{szam}</text>
      {tartaly(8, 32, 70, 92, vf, isz, extra)}
      <text x="43" y="146" text-anchor="middle" class="abra-cimke">{cimke}</text>
    </g>''')
    # A ciklus visszazáró íve: ettől látszik, hogy ismétlődő folyamat.
    ki.append('''<path d="M57 172 L57 186 Q57 196 67 196 L375 196 Q385 196 385 186 L385 172"
      fill="none" stroke="var(--abra-jel)" stroke-width="2" stroke-dasharray="5 4"/>
    <path d="M51 178 L57 170 L63 178" fill="none" stroke="var(--abra-jel)"
      stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <text x="221" y="214" text-anchor="middle" class="abra-jegyzet">a ciklus újraindul</text>''')
    return f'''<svg class="abra-svg" viewBox="0 0 440 228" role="img"
     aria-labelledby="abra-sbr-cim abra-sbr-leiras">
    <title id="abra-sbr-cim">SBR: egy reaktortér, négy fázis egymás után</title>
    <desc id="abra-sbr-leiras">Ugyanabban a tartályban zajlik a feltöltés, a
    levegőztetés, az ülepítés és a tisztított víz elvezetése — egymás után,
    időben elválasztva. A ciklus végén minden kezdődik elölről.</desc>
    {''.join(ki)}
  </svg>'''


def atfolyo_svg():
    """Folyamatos átfolyás — ugyanaz az idő, a fázisok TÉRBEN elválasztva."""
    kamrak = ['Fogadás', 'Levegőztetés', 'Ülepítés', 'Elvezetés']
    w, x0, y0, h = 96, 24, 40, 92
    ki = []
    for i, nev in enumerate(kamrak):
        x = x0 + i * w
        viz = 18 if i else 34
        isz = 26 if i >= 2 else 0
        buborek = (''.join(f'<circle cx="{x+22+j*16}" cy="{100-((j*19)%40)}" r="3" '
                           f'fill="var(--abra-kiemeles)"/>' for j in range(4))
                   if i == 1 else '')
        ki.append(f'''<g>
      {tartaly(x, y0, w, h, viz, isz, buborek)}
      <text x="{x+w/2}" y="{y0+h+22}" text-anchor="middle" class="abra-cimke">{nev}</text>
    </g>''')
        if i < len(kamrak) - 1:
            # A válaszfal ÁTFOLYÓ nyílással: a víz megy tovább, az iszap marad.
            ki.append(f'<path d="M{x+w} {y0+14} L{x+w} {y0+h-14}" '
                      f'stroke="var(--abra-keret)" stroke-width="2.5" stroke-linecap="round"/>')
    ki.append(f'''<path d="M6 {y0+40} L20 {y0+40} M14 {y0+34} L21 {y0+40} L14 {y0+46}"
      stroke="var(--abra-jel)" stroke-width="2.5" fill="none"
      stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M{x0+4*w} {y0+40} L{x0+4*w+14} {y0+40} M{x0+4*w+8} {y0+34} L{x0+4*w+15} {y0+40} L{x0+4*w+8} {y0+46}"
      stroke="var(--abra-jel)" stroke-width="2.5" fill="none"
      stroke-linecap="round" stroke-linejoin="round"/>
    <text x="220" y="214" text-anchor="middle" class="abra-jegyzet">a szennyvíz végighalad a kamrákon</text>''')
    return f'''<svg class="abra-svg" viewBox="0 0 440 228" role="img"
     aria-labelledby="abra-atfolyo-cim abra-atfolyo-leiras">
    <title id="abra-atfolyo-cim">Folyamatos átfolyás: több kamra, a fázisok térben</title>
    <desc id="abra-atfolyo-leiras">A szennyvíz egymást követő, különböző funkciójú
    tereken halad keresztül. A fázisok elkülönítését a tartály kialakítása
    biztosítja, nem az időzítés.</desc>
    {''.join(ki)}
  </svg>'''
