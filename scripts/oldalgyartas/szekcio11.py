#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""11. szekció — AI ajánlat-összehasonlító, a Test1-ből átvéve.

A markup nagy része ismétlődik (három azonos feltöltő kártya, tíz azonos
szerkezetű táblasor), ezért generáljuk: kézi másolással a három kártya
elkerülhetetlenül szétcsúszna.

MEGSZÓLÍTÁS: a Test1-beli modul tegező, a Test2 viszont végig magázó (a 8.
szekció is az). Egyetlen szekció eltérő hangneme feltűnő volna, ezért a
szövegeket magázóra vettük át — a tartalom és a felépítés változatlan.
"""
import pathlib, re

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

# --- ikonok (vonalrajzok, a modul közös méretezésével) ----------------------
I = {
    'chat':   '<path d="M21 15a2 2 0 0 1-2 2H8l-4 4V5a2 2 0 0 1 2-2h11a2 2 0 0 1 2 2z"/>',
    'scale':  '<path d="M12 3v18M7 7l-4 6h8zM17 7l4 6h-8zM3 13a4 4 0 0 0 8 0M13 13a4 4 0 0 0 8 0M8 21h8"/>',
    'check':  '<path d="M9 11l3 3 8-8"/><path d="M20 12v6a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h9"/>',
    'drop':   '<path d="M12 3s6 6.5 6 11a6 6 0 0 1-12 0c0-4.5 6-11 6-11z"/>',
    'quest':  '<path d="M9.1 9a3 3 0 0 1 5.8 1c0 2-3 3-3 3"/><path d="M12 17h.01"/><circle cx="12" cy="12" r="9"/>',
    'spark':  '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 15l.8 2.2L22 18l-2.2.8L19 21l-.8-2.2L16 18l2.2-.8z"/>',
    'arrow':  '<path d="M5 12h14M13 6l6 6-6 6"/>',
    'shield': '<path d="M12 3 4 6v6c0 5 3.4 7.7 8 9 4.6-1.3 8-4 8-9V6l-8-3Z"/>',
    'lock':   '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    'bulb':   '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 1 4 10.5c-.7.7-1 1.3-1 2.5H9c0-1.2-.3-1.8-1-2.5A6 6 0 0 1 12 3Z"/>',
    'upload': '<path d="M12 15V4m0 0-4 4m4-4 4 4"/><path d="M4 14v3a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-3"/>',
    'ok':     '<path d="m9 12 2 2 4-4"/><circle cx="12" cy="12" r="9"/>',
    'warn':   '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/><path d="M12 9v4M12 17h.01"/>',
    'info':   '<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 0 1 4 2c0 1.5-2 2-2 3M12 17h.01"/>',
    'ext':    '<path d="M7 17 17 7M8 7h9v9"/>',
    'leaf':   '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2.5 1 5.5.5 8-1 5-5.5 8-8.5 10z"/><path d="M2 22c3-3 5.5-4.5 9-6"/>',
    'cal':    '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    'tag':    '<path d="M20.6 13.4 12.6 21.4a2 2 0 0 1-2.8 0L3 14.6V4h10.6l7 7a2 2 0 0 1 0 2.4Z"/><circle cx="8" cy="8" r="1.3"/>',
    'funnel': '<path d="M3 4h18l-7 8v6l-4 2v-8L3 4Z"/>',
    'users':  '<path d="M16 21v-1.5a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4V21"/><circle cx="9.5" cy="7" r="3.5"/><path d="M21 21v-1.5a4 4 0 0 0-3-3.85"/>',
    'wrench': '<path d="M14.7 6.3a4 4 0 0 0-5.2 5.2l-6 6a2 2 0 0 0 2.8 2.8l6-6a4 4 0 0 0 5.2-5.2l-2.6 2.6-2-2z"/>',
    'doc':    '<path d="M9 4H6a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-3"/><path d="M9 3h6v3H9z"/><path d="M8 13h8M8 17h5"/>',
    'map':    '<path d="m9 4-6 2.5V21l6-2.5 6 2.5 6-2.5V4l-6 2.5L9 4Z"/><path d="M9 4v14.5M15 6.5V21"/>',
    'card':   '<rect x="2.5" y="6" width="19" height="12" rx="2"/><circle cx="12" cy="12" r="2.6"/><path d="M6 9.5v5M18 9.5v5"/>',
    'resp':   '<path d="M15 21v-1.5a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4V21"/><circle cx="9" cy="7" r="3.5"/><path d="m16 11 2 2 4-4"/>',
    'guard':  '<path d="M12 3 4 6v6c0 5 3.4 7.7 8 9 4.6-1.3 8-4 8-9V6l-8-3Z"/><path d="m9 12 2 2 4-4"/>',
    'tick':   '<path d="M20 6 9 17l-5-5"/>',
    'cross':  '<path d="M18 6 6 18M6 6l12 12"/>',
    'dashi':  '<path d="M7 12h10"/>',
    'unclear':'<path d="M9.5 9.2a2.6 2.6 0 0 1 4.2 2c0 1.6-2.2 2-2.2 3.2M12 18h.01"/>',
}
def svg(k):
    return f'<svg viewBox="0 0 24 24" aria-hidden="true">{I[k]}</svg>'


# --- bal oszlop: a modul négy ígérete ---------------------------------------
FEATURES = [
    ('scale', 'Ajánlatok egymás mellé rendezése',
     'Átlátható összehasonlítás a fontos szempontok alapján.'),
    ('check', 'Hiányzó tételek kiemelése',
     'Megmutatjuk, mi nem szerepel az ajánlatokban, de fontos lehet.'),
    ('drop', 'Fenntartási és szippantási szempontok',
     'Látja, milyen karbantartással és későbbi költségekkel kell számolnia.'),
    ('quest', 'Kérdések, amiket érdemes feltenni',
     'Személyre szabott kérdéseket kap a kivitelezőnek.'),
]

# --- a három feltöltő kártya ------------------------------------------------
# A régi, bináris .doc és .xls KIMARAD: azokat nem tudjuk megbízhatóan
# kiolvasni, és a félig sikerült kiolvasás téves adatot vinne az
# összehasonlításba. Jobb a tallózásnál elutasítani, mint utólag közölni.
ACCEPT = ('.pdf,.docx,.xlsx,.png,.jpg,.jpeg,application/pdf,'
          'application/vnd.openxmlformats-officedocument.wordprocessingml.document,'
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,'
          'image/png,image/jpeg')
TYPES = ['Válasszon típust', 'Zárt szennyvíztároló', 'Biológiai szennyvíztisztító',
         'Oldómedence', 'Egyéb']
CARDS = [('A', '', 'pl. Kivitelező 1', False),
         ('B', '', 'pl. Kivitelező 2', False),
         ('C', ' <span class="ofc-opt">(opcionális)</span>', 'pl. Kivitelező 3', True)]


def card(letter, extra, placeholder, muted):
    opts = '\n'.join(f'              <option>{t}</option>' for t in TYPES)
    badge = 'ofc-badge ofc-badge-muted' if muted else 'ofc-badge'
    return f'''          <div class="ofc-card" data-ofc-card>
            <p class="type-ui-card-title ofc-card-head">
              <span class="{badge}" aria-hidden="true">{letter}</span>
              <span class="ofc-card-name">Ajánlat {letter}{extra}</span>
              <button type="button" class="ofc-x" data-ofc-clear aria-label="Ajánlat {letter} törlése">&times;</button>
            </p>
            <div class="ofc-slot" data-ofc-slot>
              <button type="button" class="ofc-drop" data-ofc-drop>
                {svg('upload')}
                <b class="type-ui-subtitle ofc-drop-title">Húzza ide a fájlt, vagy kattintson a tallózáshoz</b>
                <small class="type-ui-caption ofc-drop-hint">PDF, DOCX, XLSX, JPG, PNG · legfeljebb 10&nbsp;MB</small>
              </button>
              <input type="file" data-ofc-input accept="{ACCEPT}"
                     aria-label="Ajánlat {letter} fájlja" hidden>
            </div>
            <label class="type-ui-caption ofc-label" for="ofc-tipus-{letter.lower()}">Megoldás típusa</label>
            <select class="ofc-select" id="ofc-tipus-{letter.lower()}">
{opts}
            </select>
            <label class="type-ui-caption ofc-label" for="ofc-megj-{letter.lower()}">Megjegyzés (opcionális)</label>
            <input class="ofc-note" type="text" id="ofc-megj-{letter.lower()}" placeholder="{placeholder}">
          </div>'''


# --- az összehasonlító tábla ------------------------------------------------
# (jelölés, szöveg, ikon-kulcs vagy None, alszöveg vagy None)
def st(kind, text, icon=None, sub=None):
    ic = ' ' + svg(icon) if icon else ''
    sm = f'<small>{sub}</small>' if sub else ''
    return f'<span class="ofc-st ofc-st-{kind}">{text}{ic}{sm}</span>'

NODATA = st('nodata', 'Nincs adat', 'dashi')

ROWS = [
    ('tag', 'Teljes ár (bruttó)',
     ['1&nbsp;250&nbsp;000&nbsp;Ft', '2&nbsp;890&nbsp;000&nbsp;Ft', '1&nbsp;690&nbsp;000&nbsp;Ft']),
    ('funnel', 'Milyen technológia?',
     [st('muted', 'Gyűjt', None, 'zárt tároló'),
      st('muted', 'Tisztít', None, 'biológiai'),
      st('muted', 'Ülepít', None, '+ elszivárogtat')]),
    ('users', 'Mire van méretezve?',
     [NODATA,
      st('yes', 'Méretezve', 'tick', '5 fő · állandó lakás'),
      st('warn', 'Feltételezett', None, 'kb. 4 fő')]),
    ('wrench', 'Telepítés tartalma',
     [st('no', 'Csak berendezés', 'cross'),
      st('yes', 'Teljes', 'tick', 'földmunka + bekötés + beüzemelés'),
      st('unclear', 'Részleges', 'unclear', 'földmunka nélkül')]),
    ('drop', 'Tisztított víz elvezetése',
     [st('muted', 'Nem releváns', None, 'gyűjtő rendszer'),
      st('unclear', 'Nincs megadva', 'unclear'),
      st('yes', 'Elszivárogtatás', 'tick', 'benne van')]),
    ('doc', 'Engedélyezéshez',
     [NODATA,
      st('yes', 'CE / EN 12566-3', 'tick', 'dokumentáció + helyszínrajz'),
      NODATA]),
    ('map', 'Telekadottságok',
     [st('warn', 'Nem vették figyelembe'),
      st('yes', 'Helyszíni felmérés', 'tick', 'talaj + talajvíz'),
      st('warn', 'Feltételezésekre épül')]),
    ('card', 'Éves üzemeltetési költség',
     [st('bad', 'Magas', None, 'rendszeres szippantás (4–6 hetente)'),
      st('yes', 'Alacsony', 'tick', 'áram + évi 1 szerviz'),
      st('warn', 'Közepes', None, 'időszakos szippantás')]),
    ('resp', 'Felelősség',
     [NODATA,
      st('yes', 'Egy felelős', 'tick', 'gyártó = kivitelező = szerviz'),
      st('warn', 'Több szereplő')]),
    ('guard', 'Garancia és szerviz',
     [NODATA,
      st('yes', 'Hazai szerviz', 'tick', 'alkatrész-háttérrel'),
      NODATA]),
]
TOTAL = ('warn', 'Hiányzó / tisztázandó tétel',
         [st('bad', '6 tétel'), st('warn', '1 tétel'), st('bad', '4 tétel')])

HEADS = [('Ajánlat A', 'Zárt tároló'), ('Ajánlat B', 'Biológiai tisztító'),
         ('Ajánlat C', 'Oldómedence')]

AI = [('ok', 'b', 'Az <b>Ajánlat&nbsp;B</b> a legteljesebb és a legmagasabb műszaki szintű '
       '(biológiai tisztítás), telepítéssel és engedélyezéssel együtt — de érdemes tisztázni '
       'a tisztított víz elvezetésének módját.'),
      ('warn', 'a', 'Az <b>Ajánlat&nbsp;A</b> a legolcsóbb, de csak <b>gyűjt</b> — nem tisztít: '
       'rendszeres szippantást igényel, és több kulcstétel hiányzik (méretezés, engedélyezés, '
       'garancia).'),
      ('info', 'c', 'Az <b>Ajánlat&nbsp;C</b> (oldómedence) részleges megoldás — az '
       'elszivárogtatás benne van, de a telepítés, a telekadottságok és a felelősségi háttér '
       'tisztázásra szorul.')]


def build():
    feats = '\n'.join(f'''          <li class="ofc-feature">
            <span class="ofc-feat-ico" aria-hidden="true">{svg(k)}</span>
            <div>
              <h3 class="type-ui-card-title ofc-feat-title">{t}</h3>
              <p class="type-ui-subtitle ofc-feat-text">{d}</p>
            </div>
          </li>''' for k, t, d in FEATURES)

    cards = '\n'.join(card(*c) for c in CARDS)

    ths = '\n'.join(f'                  <th scope="col">{a}<span class="type-ui-caption ofc-th-sub">{b}</span></th>'
                    for a, b in HEADS)

    def row(icon, label, cells, cls=''):
        tds = '\n'.join(f'                  <td class="type-ui-subtitle">{c}</td>' for c in cells)
        return f'''                <tr{cls}>
                  <th scope="row" class="type-ui-subtitle">
                    <span class="ofc-cell-label">{svg(icon)}{label}</span>
                  </th>
{tds}
                </tr>'''

    body = '\n'.join(row(i, l, c) for i, l, c in ROWS)
    body += '\n' + row(TOTAL[0], TOTAL[1], TOTAL[2], ' class="ofc-row-total"')

    ai = '\n'.join(f'''            <li class="type-ui-subtitle" data-ofc-for="{key}">
              <span class="ofc-ai-{kind}" aria-hidden="true">{svg(kind)}</span>
              <span>{txt}</span>
            </li>''' for kind, key, txt in AI)

    return f'''
  <!-- ==========================================================================
       11. SZEKCIÓ — AI AJÁNLAT-ÖSSZEHASONLÍTÓ
       A Test1-beli modul átvéve: viselkedés és elrendezés változatlan, a
       megjelenés a Test2 tokenkészletéből. A megszólítás magázóra váltott, mert
       a webhely többi része (a 8. szekció modulja is) magázó.

       ⚠️ A feltöltött fájlok kiolvasása backendet igényel — ma NEM történik
       elemzés. A tábla mintaadatot tartalmaz, és a kitöltés után a modul ezt
       jól láthatóan ki is írja (lásd ofc.js → showDemoNotice).
  =========================================================================== -->
  <section class="section" id="ajanlat-osszehasonlito" aria-labelledby="ofc-cim">
    <div class="section-inner">
      <div class="ofc">

        <div>
          <p class="type-data-eyebrow ofc-eyebrow">{svg('chat')}AI támogatás</p>
          <h2 class="type-display-section-title" id="ofc-cim">
            Hasonlítsa össze a kapott ajánlatokat <span class="ofc-accent">érthetően.</span>
          </h2>
          <p class="type-ui-body ofc-lead">
            Töltsön fel 2–3 ajánlatot, és megmutatjuk, miben térnek el: mit tartalmaznak, mi
            hiányzik belőlük, milyen későbbi költségekkel számolhat, és mire érdemes rákérdezni
            döntés előtt.
          </p>

          <ul class="ofc-features" role="list">
{feats}
          </ul>

          <p class="ofc-actions">
            <button type="button" class="btn btn-primary ofc-cta">
              <span class="ofc-cta-jel" aria-hidden="true">{svg('spark')}</span>
              <span data-ofc-felirat>Ajánlatok elemzése</span>
              <span class="action-arrow-end" aria-hidden="true">&rarr;</span>
            </button>
          </p>
          <p class="type-ui-caption ofc-disclaimer">
            {svg('shield')}Az elemzés tájékoztató jellegű, nem helyettesíti a helyszíni
            felmérést és a szakértői véleményt.
          </p>

          <aside class="ofc-ai" aria-labelledby="ofc-ai-cim">
            <h3 class="type-ui-card-title ofc-ai-title" id="ofc-ai-cim">Megjegyzések a dokumentumokról</h3>
            <ul class="ofc-ai-list" role="list">
{ai}
            </ul>
          </aside>
        </div>

        <div>

          <ol class="ofc-steps type-ui-label" role="list">
            <li class="ofc-step is-active"><span class="ofc-step-n" aria-hidden="true">1</span>Ajánlatok feltöltése</li>
            <li class="ofc-step-sep" aria-hidden="true"></li>
            <li class="ofc-step"><span class="ofc-step-n" aria-hidden="true">2</span>AI összehasonlítás</li>
            <li class="ofc-step-sep" aria-hidden="true"></li>
            <li class="ofc-step"><span class="ofc-step-n" aria-hidden="true">3</span>Eredmény és javaslatok</li>
          </ol>

          <div class="ofc-panel">
            <!-- AI-JEL. A panel sarkában jelzi, hogy itt gépi feldolgozás
                 történik — a mozgás finom és folyamatos, nem villog: a cél a
                 jelenlét jelzése, nem a figyelem elterelése. `aria-hidden`,
                 mert a mondanivalóját a mellette álló felirat hordozza. -->
            <p class="ofc-aijel" aria-hidden="true">
              <span class="ofc-aijel-gyuru"></span>
              <span class="ofc-aijel-mag">{svg('spark')}</span>
              <span class="ofc-aijel-felirat">AI</span>
            </p>
            <div class="ofc-uphead">
              <div>
                <h3 class="type-ui-card-title">Töltsön fel 2–3 ajánlatot
                  <span class="ofc-uphead-note">(PDF, kép vagy szöveg formátumban)</span>
                </h3>
                <p class="type-ui-caption ofc-secure">{svg('lock')}Az adatait bizalmasan kezeljük.</p>
              </div>
              <p class="type-ui-subtitle ofc-tip">
                {svg('bulb')}<span><b>Tipp:</b> nevezze el az ajánlatokat (pl. Kivitelező 1,
                Kivitelező 2), hogy könnyebb legyen azonosítani őket.</span>
              </p>
            </div>

            <div class="ofc-cards">
{cards}
            </div>
          </div>

          <div class="ofc-compare">
            <div class="ofc-compare-head">
              <h3 class="type-ui-card-title ofc-compare-title">{svg('spark')}AI összehasonlítás — előnézet</h3>
            </div>
            <div data-ofc-body>
              <div class="compare-scroll" role="region" aria-labelledby="ofc-cim" tabindex="0">
                <table class="compare-table" data-ofc-table>
                  <thead>
                    <tr>
                      <th scope="col">Szempont</th>
{ths}
                    </tr>
                  </thead>
                  <tbody>
{body}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- JELENTÉS. Az összehasonlítás magában a lapban él; ha a látogató
               bezárja, elveszik. Ez a blokk viszi el magával: letölthető
               HTML-fájlként, kinyomtatható PDF-be, vagy elküldhető e-mailben.
               A jelentés a képernyőn látható táblából épül, tehát nem mondhat
               mást, mint amit a látogató lát (assets/js/jelentes.js). -->
          <div class="ofc-export" data-ofc-export>
            <div class="ofc-export-fej">
              <h3 class="type-ui-card-title ofc-export-cim">{svg('doc')}Jelentés az összehasonlításról</h3>
              <p class="type-ui-caption ofc-export-alcim">Céges fejléccel, nyomtatásra rendezve.</p>
            </div>
            <p class="ofc-export-gombok">
              <button type="button" class="btn btn-secondary" data-ofc-letolt>HTML letöltése</button>
              <button type="button" class="btn btn-secondary" data-ofc-pdf>PDF / nyomtatás</button>
              <button type="button" class="btn btn-secondary" data-ofc-levelnyit
                      aria-expanded="false" aria-controls="ofc-lev">Küldés e-mailben</button>
            </p>

            <form class="ofc-lev" id="ofc-lev" data-ofc-lev hidden novalidate>
              <p class="urlap-mezo">
                <label class="type-ui-caption urlap-cimke" for="ofc-lev-email">E-mail-cím <span aria-hidden="true">*</span></label>
                <input class="urlap-input" type="email" id="ofc-lev-email" name="email" required
                       autocomplete="email" placeholder="pelda@email.hu">
              </p>
              <p class="urlap-jelolo">
                <input type="checkbox" id="ofc-lev-hozzajarul" name="hozzajarul" value="1" required>
                <label class="type-ui-subtitle" for="ofc-lev-hozzajarul">Hozzájárulok, hogy a megadott
                  e-mail-címemre elküldjék a jelentést.
                  <a href="adatkezelesi-tajekoztato">Adatkezelési tájékoztató</a> <span aria-hidden="true">*</span></label>
              </p>
              <!-- Mézesbödön: a robotok kitöltik, ember nem látja. A `nyitva` mező a
                   megnyitás időpontja — a túl gyors beküldés is robotra utal. -->
              <p class="urlap-csapda" aria-hidden="true">
                <label for="ofc-lev-weboldal">Weboldal</label>
                <input type="text" id="ofc-lev-weboldal" name="weboldal" tabindex="-1" autocomplete="off">
              </p>
              <input type="hidden" name="nyitva" value="" data-urlap-ido>
              <p class="urlap-akcio">
                <button class="btn btn-primary" type="submit">Jelentés küldése</button>
              </p>
              <p class="type-ui-caption ofc-lev-allapot" data-ofc-lev-allapot role="status"></p>
            </form>
          </div>

          <div class="ofc-expert">
            <p class="type-ui-body ofc-expert-text">{svg('leaf')}Bizonytalan? Szakértőnk átnézi az
              ajánlatokat, és személyre szabott tanácsot ad.</p>
            <a class="btn btn-secondary" href="kapcsolat">Szakértői átnézés kérése</a>
          </div>

        </div>
      </div>
    </div>
  </section>
'''


if __name__ == '__main__':
    p = WEB / 'index.html'
    s = p.read_text(encoding='utf-8')
    sec = build()
    if 'ajanlat-osszehasonlito' in s:
        s = re.sub(r'\n  <!-- =+\n       11\. SZEKCIÓ.*?\n  </section>\n', sec, s, flags=re.S)
    else:
        s = s.replace('\n</main>', sec + '\n</main>', 1)
    if 'js/ofc.js' not in s:
        s = s.replace('<script src="assets/js/ai-advisor.js?v=3" defer></script>',
                      '<script src="assets/js/ai-advisor.js?v=3" defer></script>\n'
                      '<script src="assets/js/ofc.js?v=1" defer></script>')
    # A jelentés motorja az ofc.js ELŐTT töltődik: az ofc.js a gombok
    # lenyomásakor a `window.OthJelentes`-t hívja. Mindkettő `defer`, tehát a
    # sorrendjük a dokumentumbeli sorrend.
    if '<script src="assets/js/jelentes.js' not in s:
        s = re.sub(r'(<script src="assets/js/ofc\.js[^"]*" defer></script>)',
                   '<script src="assets/js/jelentes.js?v=1" defer></script>\n\\1', s, count=1)
    p.write_text(s, encoding='utf-8')
    print('index.html — 11. szekció beírva')
