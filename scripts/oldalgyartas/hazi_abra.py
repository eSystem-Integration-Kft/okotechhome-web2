# -*- coding: utf-8 -*-
"""A „Házi szennyvíztisztító" lap ábrája: négy helyzet, négy irány.

A lap állítása: a választás nem termékkérdéssel kezdődik, hanem azzal, hogyan
használják az ingatlant. Ezért négy HASZNÁLATI helyzet áll egymás mellett —
nem négy termék. A rajz mindegyiknél a használat ritmusát mutatja: az egész
évben lakott ház, a szezonálisan használt nyaraló, a kiváltandó régi akna és a
csúcsokkal terhelt intézmény.

A `hub-*` készlet szabályai szerint: SVG a téma színeivel, `aria-hidden`
(a jelentést a mellette álló HTML-szöveg hordozza), a mozgás az app.css
`motion` rétegében, `prefers-reduced-motion` mögött, a késleltetés osztályból
(`abra-iN`), mert az éles CSP a soron belüli stílust eldobja.
"""
import html as _html


def _svg(tartalom, cim):
    return (f'<!-- {_html.escape(cim, quote=True)} -->'
            f'<svg class="hub-lepes-rajz" viewBox="0 0 120 84" aria-hidden="true" focusable="false">'
            f'{tartalom}</svg>')


def _haz(x, y, sz=1.0, jel=''):
    """Egyszerű házforma: tető + test."""
    return (f'<g transform="translate({x},{y}) scale({sz})">'
            f'<path d="M0 22 L20 4 L40 22 V44 H0 Z" fill="none" stroke="var(--abra-keret)" '
            f'stroke-width="2.2" stroke-linejoin="round"/>'
            f'<rect x="14" y="30" width="12" height="14" rx="1.5" fill="none" '
            f'stroke="var(--abra-keret)" stroke-width="1.8"/>{jel}</g>')


def _pontsor(y, teli, ures, x0=14, koz=12):
    """Hónapritmus: teli és üres korongok sora."""
    ki = []
    for i in range(teli + ures):
        szin = 'var(--abra-kiemeles)' if i < teli else 'none'
        ki.append(f'<circle cx="{x0 + i * koz}" cy="{y}" r="3.4" fill="{szin}" '
                  f'stroke="var(--abra-kiemeles)" stroke-width="1.4"/>')
    return ''.join(ki)


def rajz_csaladi_haz():
    """Egész évben lakott ház: folyamatos, kiszámítható terhelés."""
    fust = ''.join(
        f'<circle class="abra-bub abra-i{i}" cx="{72 + i * 3}" cy="26" r="2.2" '
        f'fill="var(--abra-kiemeles)"/>' for i in range(3))
    return _svg(
        _haz(14, 8, 1.0) + fust +
        '<path d="M2 64 H118" stroke="var(--abra-jel)" stroke-width="1.2" stroke-dasharray="3 3"/>'
        + _pontsor(74, 8, 0, x0=12, koz=13),
        'Egész évben lakott ház: folyamatos terhelés')


def rajz_nyaralo():
    """Nyaraló: néhány hónap használat, közte hosszú szünet."""
    return _svg(
        _haz(14, 8, 1.0) +
        '<path d="M64 30 L74 20 L84 30 V44 H64 Z" fill="none" stroke="var(--abra-jel)" '
        'stroke-width="1.8" stroke-linejoin="round" opacity=".7"/>'
        '<path d="M2 64 H118" stroke="var(--abra-jel)" stroke-width="1.2" stroke-dasharray="3 3"/>'
        + _pontsor(74, 3, 5, x0=12, koz=13),
        'Nyaraló: néhány hónap használat, közte szünet')


def rajz_emeszto_csere():
    """Emésztő kiváltása: a régi akna marad, új berendezés kerül mellé."""
    cseppek = ''.join(
        f'<circle class="hub-hullo abra-i{i}" cx="{88 + i * 8}" cy="56" r="1.6" fill="var(--abra-viz)"/>'
        for i in range(3))
    return _svg(
        '<rect x="2" y="24" width="116" height="58" rx="3" fill="var(--abra-iszap)" opacity=".35"/>'
        '<path d="M2 24 H118" stroke="var(--abra-kiemeles)" stroke-width="2.2"/>'
        # régi akna
        '<rect x="12" y="34" width="34" height="40" rx="4" fill="none" stroke="var(--abra-jel)" '
        'stroke-width="2" stroke-dasharray="5 4"/>'
        # nyíl
        '<path d="M52 54 H68 M62 48 L68 54 L62 60" fill="none" stroke="var(--abra-kiemeles)" '
        'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'
        # új berendezés
        '<rect x="74" y="34" width="34" height="40" rx="6" fill="none" stroke="var(--abra-keret)" stroke-width="2.2"/>'
        '<rect x="77" y="44" width="28" height="27" rx="3" fill="var(--abra-viz)"/>'
        + cseppek,
        'Emésztő kiváltása: a régi akna helyett új berendezés')


def rajz_intezmeny():
    """Intézmény: csúcsidőszakok, méretezett rendszer."""
    oszlopok = ''.join(
        f'<rect x="{62 + i * 13}" y="{74 - m}" width="8" height="{m}" rx="2" '
        f'fill="var(--abra-kiemeles)" opacity="{0.45 + 0.15 * (m > 20)}"/>'
        for i, m in enumerate((14, 30, 20, 38)))
    return _svg(
        # nagyobb épület
        '<rect x="10" y="20" width="40" height="54" rx="3" fill="none" stroke="var(--abra-keret)" stroke-width="2.2"/>'
        + ''.join(f'<rect x="{16 + c * 12}" y="{28 + s * 14}" width="8" height="9" rx="1.5" '
                  f'fill="var(--abra-viz)"/>' for s in range(3) for c in range(2))
        + '<path d="M2 74 H118" stroke="var(--abra-jel)" stroke-width="1.2"/>'
        + oszlopok,
        'Intézmény: csúcsidőszakokkal terhelt profil')


HELYZETEK = [
    (rajz_csaladi_haz, 'Egész évben lakott családi ház', 'Aktív biológiai tisztító',
     'A napi terhelés kiszámítható, a biológia folyamatosan tápanyagot kap.'),
    (rajz_nyaralo, 'Nyaraló, hétvégi ház', 'Biológiai vagy oldómedencés',
     'Egy 2–3 hetes kihagyás egyik technológiánál sem okoz gondot; erősen szezonális '
     'használatnál az oldómedencés rendszer is szóba jön.'),
    (rajz_emeszto_csere, 'Meglévő emésztő kiváltása', 'Aktív biológiai tisztító',
     'A régi akna kitisztítás és vízzáróvá tétel után például esővízgyűjtőként hasznosítható tovább.'),
    (rajz_intezmeny, 'Panzió, étterem, intézmény', 'Kapacitás szerint méretezve',
     'Itt a terhelési profil és a csúcsidőszakok döntenek, nem az épület funkciója.'),
]


def helyzet_abra(azon):
    lepesek = []
    for n, (rajz, cim, irany, szoveg) in enumerate(HELYZETEK, 1):
        lepesek.append(f'''          <li class="hub-lepes">
            {rajz()}
            <p class="type-data-eyebrow hub-lepes-szam">{n:02d}</p>
            <h3 class="type-ui-card-title hub-lepes-cim">{_html.escape(cim)}</h3>
            <p class="type-ui-body-strong hub-irany">{_html.escape(irany)}</p>
            <p class="type-ui-body hub-lepes-szoveg">{_html.escape(szoveg)}</p>
          </li>''')
    nl = chr(10)
    return f'''      <figure class="hub-folyamat" aria-labelledby="{azon}">
        <figcaption class="hub-folyamat-fej">
          <p class="type-data-eyebrow section-eyebrow">Infografika</p>
          <p class="type-display-highlight-title hub-folyamat-cim" id="{azon}">Négy helyzet, négy irány</p>
        </figcaption>
        <ol class="hub-lepesek" role="list">
{nl.join(lepesek)}
        </ol>
        <p class="type-ui-caption hub-folyamat-jegyzet">A választás nem termékkérdéssel kezdődik, hanem azzal, hogyan használják az ingatlant.</p>
      </figure>'''
