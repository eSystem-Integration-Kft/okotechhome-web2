#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Helyzetem kategória oldalgenerátor — Test2 designrendszer.

A fejléc (kontaktsáv + megamenü) ma minden oldalon duplikálódik. Amíg nincs
build-lépés, ez a szkript az egyetlen forrás: a fejlécet egy meglévő aloldalból
emeli ki, így nem tud szétcsúszni.
"""
import re, pathlib, html as _html

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'
SRC = (WEB / 'megoldasok' / 'alternativak.html').read_text(encoding='utf-8')

# A fejléc a skip-linktől a </header>-ig tart; a Helyzetem oldalak ugyanolyan
# mélyen vannak, mint a Megoldások, ezért a ../ hivatkozások változatlanul jók.
m = re.search(r'(<a class="skip-link".*?</header>)', SRC, re.S)
HEADER = m.group(1)


def esc(s):
    return _html.escape(s, quote=False)


def slug_id(s):
    """Szekció-azonosító: ékezet nélkül, kisbetűvel — az aria-labelledby-hoz."""
    t = s.lower()
    for a, b in zip('áéíóöőúüű', 'aeiooouuu'):
        t = t.replace(a, b)
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')


# --- szekció-építők -------------------------------------------------------

def sec_numbered(eyebrow, title, lead, items):
    sid = slug_id(title) + '-cim'
    lis = '\n'.join(
        f'        <li class="card">\n'
        f'          <span class="card-badge type-data-value" aria-hidden="true">{i:02d}</span>\n'
        f'          <p class="type-ui-body card-text">{t}</p>\n'
        f'        </li>'
        for i, t in enumerate(items, 1))
    leadp = f'\n        <p class="type-ui-body section-lead">{lead}</p>' if lead else ''
    return f'''
  <section class="section" aria-labelledby="{sid}">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">{eyebrow}</p>
        <h2 class="type-display-section-title section-title" id="{sid}">{title}</h2>{leadp}
      </header>
      <ul class="numbered-grid" role="list">
{lis}
      </ul>
    </div>
  </section>
'''


def sec_split(eyebrow, title, yes_title, yes, no_title, no):
    sid = slug_id(title) + '-cim'
    def rows(items, mark):
        return '\n'.join(
            f'            <li class="type-ui-body"><span class="fit-mark fit-{mark}" aria-hidden="true"></span>'
            f'<span class="fit-text">{t}</span></li>' for t in items)
    return f'''
  <section class="section" aria-labelledby="{sid}">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">{eyebrow}</p>
        <h2 class="type-display-section-title section-title" id="{sid}">{title}</h2>
      </header>
      <div class="split">
        <div class="split-card">
          <h3 class="type-ui-card-title split-title">{yes_title}</h3>
          <ul class="fit-list" role="list">
{rows(yes, 'yes')}
          </ul>
        </div>
        <div class="split-card">
          <h3 class="type-ui-card-title split-title">{no_title}</h3>
          <ul class="fit-list" role="list">
{rows(no, 'no')}
          </ul>
        </div>
      </div>
    </div>
  </section>
'''


def sec_prose(eyebrow, title, paras):
    sid = slug_id(title) + '-cim'
    body = '\n'.join(f'      <p class="type-ui-body section-lead">{p}</p>' for p in paras)
    return f'''
  <section class="section" aria-labelledby="{sid}">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">{eyebrow}</p>
        <h2 class="type-display-section-title section-title" id="{sid}">{title}</h2>
      </header>
{body}
    </div>
  </section>
'''


def sec_situations(eyebrow, title, lead, items):
    """Ikonos oszlopok — a főoldal 3. szekciójának komponense."""
    sid = slug_id(title) + '-cim'
    lis = []
    for icon, h, txt, href, label in items:
        lis.append(f'''        <li class="situation">
          <span class="icon-badge" aria-hidden="true">
            <span class="icon icon-inline icon-badge-size icon-{icon}"></span>
          </span>
          <h3 class="type-ui-card-title situation-title">{h}</h3>
          <p class="type-ui-body situation-text">{txt}</p>
          <a class="text-link situation-action" href="{href}"><span class="link-label">{label}<span class="action-arrow-end" aria-hidden="true">&rarr;</span></span></a>
        </li>''')
    leadp = f'\n        <p class="type-ui-body section-lead">{lead}</p>' if lead else ''
    return f'''
  <section class="section" aria-labelledby="{sid}">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">{eyebrow}</p>
        <h2 class="type-display-section-title section-title" id="{sid}">{title}</h2>{leadp}
      </header>
      <ul class="situation-grid" role="list">
{chr(10).join(lis)}
      </ul>
    </div>
  </section>
'''


def sec_cta(eyebrow, title, paras, btn_label, btn_href, alt=None):
    sid = slug_id(title) + '-cim'
    body = '\n'.join(f'          <p class="type-ui-body panel-dark-text">{p}</p>' for p in paras)
    altl = ''
    if alt:
        altl = (f'\n          <p class="type-ui-body panel-dark-text">'
                f'<a href="{alt[1]}">{alt[0]}</a></p>')
    return f'''
  <section class="section" aria-labelledby="{sid}">
    <div class="section-inner">
      <aside class="panel-dark" aria-labelledby="{sid}">
        <div class="panel-dark-head">
          <p class="type-data-eyebrow panel-dark-eyebrow">{eyebrow}</p>
          <h2 class="type-display-highlight-title panel-dark-title" id="{sid}">{title}</h2>
        </div>
        <div class="panel-dark-body">
{body}{altl}
          <p class="panel-dark-actions"><a class="btn btn-inverse" href="{btn_href}">{btn_label}</a></p>
        </div>
      </aside>
    </div>
  </section>
'''


def sec_faq(faq):
    items = '\n'.join(f'''        <details class="faq-item">
          <summary class="faq-q type-ui-card-title">{q}</summary>
          <div class="faq-a"><p class="type-ui-body">{a}</p></div>
        </details>''' for q, a in faq)
    return f'''
  <section class="section" aria-labelledby="gyik-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Gyakori kérdések</p>
        <h2 class="type-display-section-title section-title" id="gyik-cim">Amit a leggyakrabban kérdeznek</h2>
      </header>
      <div class="faq">
{items}
      </div>
    </div>
  </section>
'''


# --- oldalváz -------------------------------------------------------------

def build(p):
    img = p['img']
    body = ''.join(p['sections'])
    crumb = ''.join(
        f'            <li><a href="{h}">{t}</a></li>\n' for t, h in p['crumbs'])
    # A FAQPage jelölést a MEGJELENÍTETT kérdésekből olvassuk ki, nem külön
    # listából: így a strukturált adat nem tud eltérni a látható tartalomtól —
    # az eltérés a Google szerint önmagában is szabálysértés.
    pairs = re.findall(
        r'<summary class="faq-q[^"]*">(.*?)</summary>.*?<div class="faq-a">(.*?)</div>',
        body, re.S)
    faq_ld = ',\n'.join(
        '      {"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}'
        % (_json(strip_tags(q)), _json(strip_tags(a))) for q, a in pairs)
    crumb_ld = ',\n'.join(
        '      {"@type":"ListItem","position":%d,"name":%s,"item":"https://okoth.hu/%s"}'
        % (i, _json(t), h.replace('../', '').lstrip('./'))
        for i, (t, h) in enumerate(p['crumbs'], 1))
    crumb_ld += ',\n      {"@type":"ListItem","position":%d,"name":%s,"item":"https://okoth.hu/%s"}' % (
        len(p['crumbs']) + 1, _json(p['h1']), p['url'])

    return f'''<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<!-- TESZT ÜZEMMÓD: az oldal fejlesztés alatt áll. ÉLESÍTÉSKOR ezt a sort
     minden oldalról törölni kell (a .htaccess X-Robots-Tag blokkjával együtt). -->
<meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{p['title']}</title>
<meta name="description" content="{esc(p['desc'])}">
<link rel="canonical" href="https://okoth.hu/{p['url']}">
<meta property="og:type" content="article">
<meta property="og:title" content="{esc(p['h1'])}">
<meta property="og:description" content="{esc(p['desc'])}">
<meta property="og:image" content="https://okoth.hu/assets/img/oldalak/hero-{img}.webp">
<meta property="og:locale" content="hu_HU">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Zilla+Slab:wght@400;500;600;700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="../assets/css/app.css?v=59">
<link rel="preload" as="image" href="../assets/img/oldalak/hero-{img}.webp"
      imagesrcset="../assets/img/oldalak/hero-{img}-1024.webp 1100w, ../assets/img/oldalak/hero-{img}.webp 1800w"
      imagesizes="100vw">
</head>
<body>

{HEADER}

<main id="fotartalom">

  <section class="hero page-hero" aria-labelledby="oldal-cim">
    <div class="hero-inner">
      <div class="hero-copy">
        <nav class="breadcrumb" aria-label="Morzsamenü">
          <ol class="breadcrumb-list type-ui-caption" role="list">
{crumb}            <li aria-current="page">{p['h1']}</li>
          </ol>
        </nav>
        <h1 class="type-display-page-title hero-title" id="oldal-cim">{p['h1']}</h1>
        <p class="type-ui-body-strong hero-lead">{p['lead']}</p>
      </div>
    </div>
    <figure class="hero-media page-hero-media">
      <picture>
        <source media="(max-width: 1024px)" srcset="../assets/img/oldalak/hero-{img}-szuk.webp 1100w" sizes="100vw" width="1100" height="471">
        <img src="../assets/img/oldalak/hero-{img}.webp"
             srcset="../assets/img/oldalak/hero-{img}-1024.webp 1100w, ../assets/img/oldalak/hero-{img}.webp 1800w"
             sizes="100vw" width="1800" height="771" alt="{esc(p['alt'])}" fetchpriority="high" decoding="async">
      </picture>
    </figure>
  </section>
{body}
</main>

<script src="../assets/js/site.js?v=3" defer></script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@graph": [
    {{
      "@type": "BreadcrumbList",
      "itemListElement": [
{crumb_ld}
      ]
    }},
    {{
      "@type": "FAQPage",
      "mainEntity": [
{faq_ld}
      ]
    }}
  ]
}}
</script>

</body>
</html>
'''


import json as _j
def _json(s):
    return _j.dumps(s, ensure_ascii=False)


def strip_tags(s):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', s)).strip()
