# -*- coding: utf-8 -*-
"""A Megoldások hub ábrái.

A LAP KÖZPONTI ÁLLÍTÁSA KÉPBEN: a szennyvíztisztító rendszer nem egy
berendezés, hanem három, egymásra épülő rész — kezelés, vízelhelyezés,
üzemeltetés. „Aki csak a berendezést választja ki, az a rendszernek
egyharmadát tervezte meg." Ezért három egyenrangú kártya, nyíllal összekötve,
nem egy nagy rajz a berendezésről.

A rajzok a `hub-*` készlet szabályai szerint: SVG (a téma színeivel, élesen
nagyítva is), `aria-hidden` — a jelentést a mellette álló HTML-szöveg hordozza.
A mozgás az app.css `motion` rétegében, `prefers-reduced-motion` mögött.
A késleltetés osztályból jön (`abra-iN`), mert az éles CSP a soron belüli
stílust eldobja.
"""
import html as _html


def _svg(tartalom, cim):
    return (f'<!-- {_html.escape(cim, quote=True)} -->'
            f'<svg class="hub-lepes-rajz" viewBox="0 0 120 84" aria-hidden="true" focusable="false">'
            f'{tartalom}</svg>')


def _talaj(y=24):
    return (f'<rect x="2" y="{y}" width="116" height="{82 - y}" rx="3" fill="var(--abra-iszap)" opacity=".4"/>'
            f'<path d="M2 {y} H118" stroke="var(--abra-kiemeles)" stroke-width="2.2"/>')


def rajz_kezeles():
    """A műtárgy: a ház szennyvize a tartályba érkezik."""
    buborek = ''.join(
        f'<circle class="abra-bub abra-i{i}" cx="{cx}" cy="64" r="2.2" fill="var(--abra-kiemeles)"/>'
        for i, cx in enumerate((72, 84, 96)))
    return _svg(
        '<path d="M8 40 L26 24 L44 40 V56 H8 Z" fill="none" stroke="var(--abra-keret)" '
        'stroke-width="2.2" stroke-linejoin="round"/>'
        + _talaj(44) +
        # bekötőcső a tartályig
        '<path d="M44 52 H60 Q66 52 66 58" fill="none" stroke="var(--abra-keret)" stroke-width="5" stroke-linecap="round"/>'
        '<path class="abra-ciklus" d="M44 52 H60 Q66 52 66 58" fill="none" stroke="var(--abra-viz)" '
        'stroke-width="2.4" stroke-dasharray="6 4" stroke-linecap="round"/>'
        # műtárgy
        '<rect x="56" y="54" width="54" height="26" rx="5" fill="none" stroke="var(--abra-keret)" stroke-width="2.2"/>'
        '<rect x="58" y="60" width="50" height="18" rx="3" fill="var(--abra-viz)"/>'
        '<path d="M84 54 V80" stroke="var(--abra-keret)" stroke-width="1.4" stroke-dasharray="3 3"/>'
        + buborek,
        'A ház szennyvize a műtárgyba érkezik')


def rajz_vizelhelyezes():
    """A tisztítómező: a kezelt víz a talajba szivárog."""
    cseppek = ''.join(
        f'<circle class="hub-hullo abra-i{i}" cx="{x}" cy="52" r="1.7" fill="var(--abra-viz)"/>'
        for i, x in enumerate((26, 44, 62, 80, 98)))
    fu = ''.join(f'<path d="M{x} 24 V16 M{x} 20 Q{x - 5} 16 {x - 7} 12 M{x} 19 Q{x + 5} 15 {x + 7} 11" '
                 f'fill="none" stroke="var(--abra-kiemeles)" stroke-width="1.6" stroke-linecap="round"/>'
                 for x in (20, 60, 100))
    return _svg(
        _talaj(24) + fu +
        # kavicságy és perforált cső
        '<rect x="10" y="38" width="100" height="14" rx="4" fill="var(--surface)" '
        'stroke="var(--abra-keret)" stroke-width="1.6"/>'
        + ''.join(f'<circle cx="{x}" cy="45" r="1.4" fill="var(--abra-jel)" opacity=".7"/>' for x in range(18, 106, 9))
        + '<rect x="16" y="41" width="88" height="8" rx="4" fill="none" stroke="var(--abra-kiemeles)" stroke-width="1.6"/>'
        + cseppek,
        'A kezelt víz a tisztítómezőn át a talajba szivárog')


def rajz_uzemeltetes():
    """Az üzemeltetés: rendszeres ellenőrzés és karbantartás."""
    return _svg(
        # naptárlap
        '<rect x="12" y="18" width="52" height="48" rx="5" fill="var(--surface)" '
        'stroke="var(--abra-keret)" stroke-width="2.2"/>'
        '<path d="M12 30 H64" stroke="var(--abra-keret)" stroke-width="1.8"/>'
        '<path d="M24 18 V12 M52 18 V12" stroke="var(--abra-keret)" stroke-width="2.2" stroke-linecap="round"/>'
        + ''.join(f'<circle cx="{x}" cy="{y}" r="2.2" fill="var(--abra-jel)" opacity=".55"/>'
                  for y in (40, 52) for x in (24, 38, 52))
        + '<circle class="abra-bub abra-i2" cx="38" cy="40" r="4" fill="var(--abra-kiemeles)"/>'
        # pipa a naptáron kívül: az elvégzett teendő
        '<circle cx="90" cy="46" r="20" fill="var(--abra-badge)" stroke="var(--abra-kiemeles)" stroke-width="2"/>'
        '<path class="hub-pipa" d="M80 46 L87 53 L101 39" fill="none" stroke="var(--abra-kiemeles)" '
        'stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"/>',
        'Rendszeres ellenőrzés és karbantartás')


LEPESEK = [
    (rajz_kezeles, 'A kezelés',
     'A műtárgy, amely a szennyvizet fogadja: zárt tároló, oldómedence vagy aktív biológiai '
     'szennyvíztisztító. Ebben dől el, milyen minőségű víz megy tovább.'),
    (rajz_vizelhelyezes, 'A vízelhelyezés',
     'A tisztított víznek el kell tudnia távozni — jellemzően szivárogtatómezőn keresztül, a '
     'talajba. Ez a rész igényli a legtöbb szabad területet, és itt akad el a legtöbb terv.'),
    (rajz_uzemeltetes, 'Az üzemeltetés',
     'Rendszeres ellenőrzés, karbantartás, és a rendszer típusától függően szippantás vagy '
     'iszapzsákcsere.'),
]


def rendszer_abra(azon):
    lepesek = []
    for n, (rajz, cim, szoveg) in enumerate(LEPESEK, 1):
        lepesek.append(f'''          <li class="hub-lepes">
            {rajz()}
            <p class="type-data-eyebrow hub-lepes-szam"><span class="visually-hidden">Rész </span>{n}</p>
            <h3 class="type-ui-card-title hub-lepes-cim">{_html.escape(cim)}</h3>
            <p class="type-ui-body hub-lepes-szoveg">{_html.escape(szoveg)}</p>
          </li>''')
    nl = chr(10)
    return f'''      <figure class="hub-folyamat" aria-labelledby="{azon}">
        <figcaption class="hub-folyamat-fej">
          <p class="type-data-eyebrow section-eyebrow">Infografika</p>
          <p class="type-display-highlight-title hub-folyamat-cim" id="{azon}">Három rész, egy rendszer</p>
        </figcaption>
        <ol class="hub-lepesek hub-lepesek-3" role="list">
{nl.join(lepesek)}
        </ol>
        <p class="type-ui-caption hub-folyamat-jegyzet">Aki csak a berendezést választja ki, az a rendszernek egyharmadát tervezte meg.</p>
      </figure>'''
