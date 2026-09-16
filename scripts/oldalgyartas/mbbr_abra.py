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

# A KÉSLELTETÉS OSZTÁLLYAL, nem `style="--i:N"`-nel. Az éles CSP
# (`style-src 'self'`) a soron belüli stílust eldobja — mérve 2026-09-16-án
# élesben minden buborék 0 s késleltetéssel, egyszerre indult. Az `abra-iN`
# osztály az app.css-ben állítja a `--i` értékét.

SZEL = 680


def hordozo(cx, cy, r=7, oszt=''):
    """Egy biofilmhordozó elem. A klasszikus, bordázott hengeres hordozó
    felülnézete: kör, benne kereszt — ettől ismerhető fel, és ettől látszik,
    hogy a FELÜLET a lényeg, nem a test."""
    o = f' class="{oszt}"' if oszt else ''
    k = r * 0.62
    return (f'<g{o} transform="translate({cx:.1f},{cy:.1f})">'
            f'<circle r="{r}" fill="var(--abra-hordozo)" stroke="var(--abra-kiemeles)" stroke-width="1.4"/>'
            f'<path d="M{-k} 0 H{k} M0 {-k} V{k}" stroke="var(--abra-kiemeles)" '
            f'stroke-width="1.2" opacity=".75"/></g>')


def pehely(cx, cy, r=5, oszt=''):
    """Eleveniszap-pehely: szabálytalan folt, nem mértani alakzat — a
    különbség a hordozóhoz képest épp ez."""
    o = f' class="{oszt}"' if oszt else ''
    d = (f'M{-r} 0 Q{-r*0.8} {-r} 0 {-r*0.9} Q{r} {-r*0.9} {r*0.9} 0 '
         f'Q{r} {r*0.85} 0 {r} Q{-r*0.9} {r*0.9} {-r} 0 Z')
    return (f'<path{o} transform="translate({cx:.1f},{cy:.1f})" d="{d}" '
            f'fill="var(--abra-iszap)" stroke="var(--abra-keret)" stroke-width="1" opacity=".9"/>')


def buborek_sor(x, w, y_alj, db, kulcs):
    ki = []
    for i in range(db):
        cx = x + w * (i + 1) / (db + 1)
        ki.append(f'<circle class="abra-bub abra-i{i}" cx="{cx:.1f}" cy="{y_alj - 8}" r="{2.4 + (i % 3) * 0.6:.1f}" '
                  f'fill="var(--abra-kiemeles)"/>')
    return ''.join(ki)


def szoras(x, y, w, h, db, r, lenges=3):
    """Szórt elhelyezés a tartályON BELÜL, garantált fali hézaggal.

    KÉZZEL MEGADOTT KOORDINÁTÁKKAL INDULT, és a hordozók kilógtak a keretből:
    a sugár és a lebegés kilengése nem volt beszámítva, a legalsó sor pedig
    pontosan a tartály aljára esett. Rácsból számolva ez nem fordulhat elő —
    és egy jövőbeli darabszám-változás sem hozza vissza.

    A JITTER DETERMINISZTIKUS (a sorszámból, nem véletlenből): generált
    fájlban a véletlen minden futáskor más rajzot adna, és a git minden
    építéskor változást látna."""
    m = r + lenges + 6                      # fali biztonsági sáv
    bx, by = x + m, y + m
    bw, bh = w - 2 * m, h - 2 * m
    sorok = 3
    oszlopok = -(-db // sorok)               # felfelé kerekítve
    ki = []
    for i in range(db):
        s, o = divmod(i, oszlopok)
        # Fél cellányi eltolás minden második sorban — így nem áll rácsba.
        eltol = 0.5 if s % 2 else 0.0
        cx = bx + bw * ((o + 0.5 + eltol) / oszlopok)
        cy = by + bh * ((s + 0.5) / sorok)
        # ELHANGOLÁS a cellán belül. Nem kozmetika: ha a szórás rácsosnak
        # látszik, az MBBR rajza épp azt gyengíti, amit állít — hogy a
        # hordozók SZABADON mozognak. A Fixed Bed rendezett rácsa ezzel
        # szemben szándékos: ott a rendezettség maga az üzenet.
        # A kilengés a cella ~40%-a, a `min/max` pedig a sávban tartja.
        cx += (i * 7 % 5 - 2) * (bw / oszlopok) * 0.22
        cy += (i * 3 % 5 - 2) * (bh / sorok) * 0.22
        ki.append((min(max(cx, bx), bx + bw), min(max(cy, by), by + bh)))
    return ki


def harom_elv_svg():
    """Fixed Bed · MBBR · eleveniszap — hol él a biomassza?"""
    tw, res = 190, 35
    x0 = (SZEL - (3 * tw + 2 * res)) / 2       # 30
    ty, th = 56, 108
    alj = ty + th                               # 164

    def keret(x, cim, belul, jegyzet, azon):
        # A TARTALOM VÁGÓMASZKBAN. A helyes koordináták az elsődleges megoldás
        # (lásd `szoras()`), ez a garancia: a lebegő hordozók és a felszálló
        # buborékok így akkor sem tudnak kilépni a keretből, ha valaki később
        # több elemet kér vagy nagyobb kilengést állít be.
        return f'''
    <g>
      <defs><clipPath id="{azon}">
        <rect x="{x}" y="{ty}" width="{tw}" height="{th}" rx="7"/>
      </clipPath></defs>
      <rect x="{x}" y="{ty}" width="{tw}" height="{th}" rx="7" fill="var(--abra-viz)"/>
      <g clip-path="url(#{azon})">{belul}</g>
      <rect x="{x}" y="{ty}" width="{tw}" height="{th}" rx="7" fill="none"
            stroke="var(--abra-keret)" stroke-width="2.5"/>
      <text x="{x + tw / 2}" y="{ty - 22}" text-anchor="middle" class="abra-cimke abra-cimke-eros">{cim}</text>
      <text x="{x + tw / 2}" y="{alj + 24}" text-anchor="middle" class="abra-jegyzet">{jegyzet}</text>
    </g>'''

    # 1 · FIXED BED — a hordozó RÖGZÍTETT: egy helyben álló blokk, körülötte
    #     áramlik a víz. A rögzítést a tartófal jelzi.
    x = x0
    # A HORDOZÓBLOKK és a benne álló rács MÉRETBŐL SZÁMOLVA. Beégetett
    # lépésközzel indult, és a jobb szélső oszlop meg az alsó sor a BLOKK
    # keretére ült — ugyanaz a hiba, mint a tartályoknál, egy szinttel
    # beljebb. A rács itt SZABÁLYOS marad (szemben az MBBR szórásával): a
    # rögzített ágy rendezettsége maga az állítás.
    bx, by = x + 34, ty + 16
    bw, bh = tw - 68, th - 46
    hr, oszlopok, sorok = 6.5, 5, 3
    m = hr + 5                                 # a blokk fala és a hordozó közt
    rogz = [f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="4" '
            f'fill="var(--abra-hordozo)" stroke="var(--abra-kiemeles)" stroke-width="1.6" opacity=".9"/>']
    for sor in range(sorok):
        for osz in range(oszlopok):
            cx = bx + m + (bw - 2 * m) * (osz / (oszlopok - 1))
            cy = by + m + (bh - 2 * m) * (sor / (sorok - 1))
            rogz.append(hordozo(cx, cy, hr))
    # A TARTÓFAL: ettől látszik, hogy a blokk nem lebeg, hanem rögzítve van.
    rogz.append(f'<path d="M{bx} {ty + 9} H{bx + bw}" stroke="var(--abra-keret)" '
                f'stroke-width="2" stroke-linecap="round"/>'
                f'<path d="M{bx + bw / 2} {ty + 9} V{by}" stroke="var(--abra-keret)" '
                f'stroke-width="2" stroke-linecap="round"/>')
    rogz.append(buborek_sor(x, tw, alj, 5, 'fb'))
    ki = [keret(x, 'Fixed Bed', ''.join(rogz), 'a hordozó a helyén marad', 'abra-tart-fb')]

    # 2 · MBBR — a hordozók SZABADON MOZOGNAK a reaktortérben. A szórt
    #     elrendezés és a lebegés együtt mondja el, hogy nincsenek rögzítve.
    x = x0 + tw + res
    mozgo = [hordozo(cx, cy, 7, f'abra-lebeg abra-i{i}')
             for i, (cx, cy) in enumerate(szoras(x, ty, tw, th, 14, 7))]
    mozgo.append(buborek_sor(x, tw, alj, 6, 'mbbr'))
    ki.append(keret(x, 'MBBR', ''.join(mozgo), 'a hordozó a vízzel együtt mozog', 'abra-tart-mbbr'))

    # 3 · ELEVENISZAP — nincs mesterséges hordozófelület: a mikroorganizmusok
    #     jelentős része a vízben LEBEGŐ iszappelyhekben van jelen.
    x = x0 + 2 * (tw + res)
    lebego = [pehely(cx, cy, 5.4, f'abra-lebeg abra-i{i}')
              for i, (cx, cy) in enumerate(szoras(x, ty, tw, th, 14, 5.4))]
    lebego.append(buborek_sor(x, tw, alj, 6, 'ei'))
    ki.append(keret(x, 'Eleveniszap', ''.join(lebego), 'a biomassza a vízben lebeg', 'abra-tart-ei'))

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
