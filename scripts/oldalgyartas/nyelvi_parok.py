# -*- coding: utf-8 -*-
"""A magyar és angol lappárok összekötése: `hreflang` + nyelvváltó.

Mindkét lapra kiírja a KÖLCSÖNÖS `hreflang` hivatkozásokat, és a fejléc
nyelvváltóját a lap SAJÁT párjára állítja — nem a nyelv nyitólapjára. Egy
konzultációs lapról az EN gomb a konzultáció angol változatára visz, nem az
angol nyitólapra: a nyelvváltás ne veszítse el, hol tart a látogató.

Újrafuttatható: a meglévő blokkot lecseréli, nem duplikálja.
"""
import os, re, sys

WEB = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '_web'))
sys.path.insert(0, os.path.dirname(__file__))
from nyelvek import SZLUG

BLOKK = ('\n\n<!-- NYELVI VÁLTOZATOK — kölcsönös. Az `x-default` a magyar: az a teljes\n'
         '     lapkészlet. ÉLESÍTÉSKOR teljes (abszolút) címre cserélendő, a robots\n'
         '     sorral együtt — a webhely szándékosan domainfüggetlen. -->\n'
         '<link rel="alternate" hreflang="hu" href="{hu}">\n'
         '<link rel="alternate" hreflang="en" href="{en}">\n'
         '<link rel="alternate" hreflang="x-default" href="{hu}">')

# A kommentáros blokkot ÉS az árván maradt `alternate` sorokat is elviszi: egy
# korábbi, kézzel írt változat kommentárja más szövegű volt, a mintára nem
# illeszkedett, és a linksorok bent maradtak — így a lap két blokkot kapott.
REGI = re.compile(r'\n*<!-- NYELVI VÁLTOZATOK.*?-->|\n*<link rel="alternate" hreflang="[^"]*"[^>]*>', re.S)


def relut(honnan_dir: str, hova: str) -> str:
    """Relatív út — az `index` lapok KÖNYVTÁRALAKBAN.

    A `/megoldasok/index` és a `/megoldasok/` ugyanaz a lap, de a keresőnek két
    cím. Az utóbbi a kanonikus alak a webhelyen (a `.htaccess` is arra irányít),
    ezért a `hreflang` és a nyelvváltó is azt kapja.
    """
    u = os.path.relpath(hova, honnan_dir).replace(os.sep, '/')
    if u == 'index':
        return './'
    if u.endswith('/index'):
        return u[:-5]
    return u


def ir(fajl: str, hu_cim: str, en_cim: str, valto_cim: str, valto_nyelv: str) -> None:
    s = open(fajl, encoding='utf-8').read()
    s = REGI.sub('', s)
    horgony = [l for l in s.split('\n') if 'assets/css/app.css?v=' in l]
    if not horgony:
        return
    s = s.replace(horgony[0], horgony[0] + BLOKK.format(hu=hu_cim, en=en_cim), 1)

    # a nyelvváltó a lap saját párjára
    if valto_nyelv == 'en':      # magyar lapon állunk, az EN gomb a párra megy
        s = re.sub(r'(<a class="nyelvvalto-elem type-ui-nav" href=")[^"]*(" hreflang="en")',
                   lambda m: m.group(1) + valto_cim + m.group(2), s)
    else:                        # angol lapon állunk, a HU gomb a párra megy
        s = re.sub(r'(<a class="nyelvvalto-elem type-ui-nav" href=")[^"]*(" hreflang="hu" lang="hu")',
                   lambda m: m.group(1) + valto_cim + m.group(2), s)
    open(fajl, 'w', encoding='utf-8').write(s)


if __name__ == '__main__':
    n = 0
    for hu_ut, en_ut in sorted(SZLUG.items()):
        hu_f = os.path.join(WEB, hu_ut + '.html')
        en_f = os.path.join(WEB, 'en', en_ut + '.html')
        if not (os.path.exists(hu_f) and os.path.exists(en_f)):
            continue
        hu_dir = os.path.dirname(hu_ut) or '.'
        en_dir = os.path.join('en', os.path.dirname(en_ut)) if os.path.dirname(en_ut) else 'en'

        # magyar lap: önmaga + az angol párja
        ir(hu_f,
           hu_cim=relut(hu_dir, hu_ut),
           en_cim=relut(hu_dir, os.path.join('en', en_ut)),
           valto_cim=relut(hu_dir, os.path.join('en', en_ut)),
           valto_nyelv='en')
        # angol lap: a magyar párja + önmaga
        ir(en_f,
           hu_cim=relut(en_dir, hu_ut),
           en_cim=relut(en_dir, os.path.join('en', en_ut)),
           valto_cim=relut(en_dir, hu_ut),
           valto_nyelv='hu')
        n += 1
    print(f'{n} lappár összekötve')
