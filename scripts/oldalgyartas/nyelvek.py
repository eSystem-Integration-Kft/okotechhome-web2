# -*- coding: utf-8 -*-
"""Nyelvi szlugtérkép — magyar útvonal → angol útvonal.

EZ A TÖBBNYELVŰSÉG EGYETLEN FORRÁSA. Ebből épül:
  · az angol lapok helye a fájlrendszerben (`_web/en/<angol út>.html`),
  · a `hreflang` páros mindkét lapon,
  · a nyelvváltó célja laponként,
  · és a belső hivatkozások átírása, ahogy egy-egy lap elkészül angolul.

A szlugok ANGOLUL vannak, nem a magyar átirataként: az angol keresőt angol
szavak érdeklik, és a látogatónak is mond valamit az URL. A magyar↔angol
párosítás ezért NEM számítható ki az útvonalból — kizárólag ez a tábla adja.

A kulcs a `_web`-hez képesti magyar útvonal, kiterjesztés nélkül; az érték az
`_web/en`-hez képesti angol útvonal, ugyanúgy. A `helyzetem/index` → `situation/index`
alakú párokban az `index` mindkét oldalon megmarad.
"""

SZLUG = {
    # --- gyökérszintű lapok -------------------------------------------------
    'index':                          'index',
    'konzultacio':                    'consultation',
    'kapcsolat':                      'contact',
    'adatkezelesi-tajekoztato':       'privacy-notice',
    'aszf':                           'terms-and-conditions',
    'cookie-tajekoztato':             'cookie-notice',
    'jogi-nyilatkozat':               'legal-notice',
    'akadalymentessegi-nyilatkozat':  'accessibility-statement',
    'szippantasi-dij-kalkulator':     'emptying-cost-calculator',
    'eredmeny':                       'saved-result',
    'jelentes':                       'comparison-report',

    # --- Helyzetem / My situation -------------------------------------------
    'helyzetem/index':                                        'situation/index',
    'helyzetem/nincs-elerheto-kozcsatorna':                   'situation/no-mains-sewer',
    'helyzetem/milyen-megoldasi-lehetosegek-vannak':          'situation/what-options-are-there',
    'helyzetem/kozcsatorna-vagy-egyedi-rendszer':             'situation/mains-sewer-or-standalone',
    'helyzetem/milyen-adatokat-kell-osszegyujteni':           'situation/what-information-to-gather',
    'helyzetem/projektindito':                                'situation/project-starter',
    'helyzetem/telekvasarlas-vagy-uj-epites-elott-allok':     'situation/buying-a-plot-or-building',
    'helyzetem/alkalmas-lehet-e-a-telek':                     'situation/could-the-plot-be-suitable',
    'helyzetem/talaj-talajviz-es-vizelhelyezes':              'situation/soil-groundwater-and-disposal',
    'helyzetem/milyen-dokumentumokra-lehet-szukseg':          'situation/what-documents-you-may-need',
    'helyzetem/telekadat-ellenorzolista':                     'situation/plot-data-checklist',
    'helyzetem/helyszini-felmeres':                           'situation/on-site-survey',
    'helyzetem/meglevo-emesztot-szeretnek-kivaltani':         'situation/replacing-a-cesspit',
    'helyzetem/mikor-indokolt-a-csere':                       'situation/when-replacement-is-worthwhile',
    'helyzetem/emeszto-oldomedence-vagy-biologiai':           'situation/cesspit-septic-tank-or-biological',
    'helyzetem/teljes-koltseg-es-megterules':                 'situation/total-cost-and-payback',
    'helyzetem/meglevo-rendszer-felmerese':                   'situation/assessing-an-existing-system',
    'helyzetem/koltseg-es-projektbrief':                      'situation/cost-and-project-brief',
    'helyzetem/nyaralo-vagy-szezonalisan-hasznalt-ingatlan':  'situation/holiday-or-seasonal-property',
    'helyzetem/mit-jelent-az-idoszakos-terheles':             'situation/what-intermittent-load-means',
    'helyzetem/biologiai-rendszer-vagy-oldomedence':          'situation/biological-system-or-septic-tank',
    'helyzetem/hosszabb-tavollet-es-ujrainditas':             'situation/long-absences-and-restarting',
    'helyzetem/szezonalis-esettanulmanyok':                   'situation/seasonal-case-studies',
    'helyzetem/hasznalati-profil':                            'situation/building-a-usage-profile',
    'helyzetem/csaladi-hazhoz-keresek-rendszert':             'situation/a-system-for-a-family-home',
    'helyzetem/megoldastipus-kivalasztasa':                   'situation/choosing-a-solution-type',
    'helyzetem/telekalkalmassag':                             'situation/plot-suitability',
    'helyzetem/kapacitas-es-letszam':                         'situation/capacity-and-occupancy',
    'helyzetem/koltseg-es-telepites':                         'situation/cost-and-installation',
    'helyzetem/ajanlatkeresi-keszultseg':                     'situation/ready-to-request-a-quote',
    'helyzetem/vallalkozas-vagy-intezmeny-szamara-keresek-megoldast': 'situation/for-a-business-or-institution',
    'helyzetem/vallalkozas-panziok-es-szallashelyek':         'situation/guesthouses-and-accommodation',
    'helyzetem/vallalkozas-ettermek-es-nagykonyhak':          'situation/restaurants-and-commercial-kitchens',
    'helyzetem/vallalkozas-iskolak-es-intezmenyek':           'situation/schools-and-institutions',
    'helyzetem/vallalkozas-kempingek-es-kozossegi':           'situation/campsites-and-community-facilities',
    'helyzetem/vallalkozas-uzemek-es-specialis-terhelesek':   'situation/plants-and-special-loads',
    'helyzetem/vallalkozas-szakmai-projektbrief':             'situation/technical-project-brief',
    'helyzetem/mar-van-rendszerem-segitsegre-van-szuksegem':  'situation/i-already-have-a-system',

    # --- Megoldások / Solutions ---------------------------------------------
    'megoldasok/index':                                'solutions/index',
    'megoldasok/megoldastipusok-osszehasonlitasa':      'solutions/comparing-solution-types',
    'megoldasok/melyik-megoldas-mikor-megfelelo':       'solutions/which-solution-suits-which-case',
    'megoldasok/kizaro-es-korlatozo-feltetelek':        'solutions/exclusions-and-limiting-conditions',
    'megoldasok/megoldastipus-eloszuro':                'solutions/solution-type-pre-screener',
    'megoldasok/biologiai-szennyviztisztitas':          'solutions/biological-treatment',
    'megoldasok/biologiai-hogyan-mukodik':              'solutions/biological-how-it-works',
    'megoldasok/biologiai-kinek-megfelelo':             'solutions/biological-who-it-suits',
    'megoldasok/biologiai-mikor-nem-megfelelo':         'solutions/biological-when-it-is-not-suitable',
    'megoldasok/biologiai-telek-es-terhelesi-feltetelek':'solutions/biological-plot-and-load-conditions',
    'megoldasok/biologiai-uzemeltetes-es-karbantartas': 'solutions/biological-operation-and-maintenance',
    'megoldasok/biologiai-koltsegtenyezok':             'solutions/biological-cost-factors',
    'megoldasok/biologiai-esettanulmanyok':             'solutions/biological-case-studies',
    'megoldasok/ab-clear':                              'solutions/ab-clear',
    'megoldasok/ab-clear-modellek-es-kapacitasok':      'solutions/ab-clear-models-and-capacities',
    'megoldasok/ab-clear-muszaki-adatok':               'solutions/ab-clear-technical-data',
    'megoldasok/ab-clear-iszapzsakos-technologia':      'solutions/ab-clear-sludge-bag-technology',
    'megoldasok/ab-clear-telepitesi-feltetelek':        'solutions/ab-clear-installation-requirements',
    'megoldasok/ab-clear-dokumentumok':                 'solutions/ab-clear-documents',
    'megoldasok/ab-clear-referenciak':                  'solutions/ab-clear-references',
    'megoldasok/oldomedences-rendszer':                 'solutions/septic-tank-system',
    'megoldasok/oldomedence-hogyan-mukodik':            'solutions/septic-tank-how-it-works',
    'megoldasok/oldomedence-kinek-megfelelo':           'solutions/septic-tank-who-it-suits',
    'megoldasok/oldomedence-mikor-nem-megfelelo':       'solutions/septic-tank-when-it-is-not-suitable',
    'megoldasok/oldomedence-tisztitomezo':              'solutions/septic-tank-drainage-field',
    'megoldasok/oldomedence-szippantas-es-karbantartas':'solutions/septic-tank-emptying-and-maintenance',
    'megoldasok/oldomedence-esettanulmanyok':           'solutions/septic-tank-case-studies',
    'megoldasok/epureco':                               'solutions/epureco',
    'megoldasok/epureco-modellek-es-kapacitasok':       'solutions/epureco-models-and-capacities',
    'megoldasok/epureco-muszaki-adatok':                'solutions/epureco-technical-data',
    'megoldasok/epureco-telepitesi-feltetelek':         'solutions/epureco-installation-requirements',
    'megoldasok/epureco-dokumentumok':                  'solutions/epureco-documents',
    'megoldasok/nagyobb-es-kozossegi-rendszerek':       'solutions/larger-and-community-systems',
    'megoldasok/nagyobb-kapacitasi-kategoriak':         'solutions/larger-capacity-categories',
    'megoldasok/nagyobb-terhelesi-profil':              'solutions/larger-load-profile',
    'megoldasok/nagyobb-elokezeles-es-kiegeszitok':     'solutions/larger-pre-treatment-and-accessories',
    'megoldasok/nagyobb-monitoring-es-uzemeltetes':     'solutions/larger-monitoring-and-operation',
    'megoldasok/nagyobb-engedelyezes':                  'solutions/larger-permitting',
    'megoldasok/nagyobb-esettanulmanyok':               'solutions/larger-case-studies',
    'megoldasok/nagyobb-szakmai-konzultacio':           'solutions/larger-technical-consultation',
    'megoldasok/alternativak':                          'solutions/alternatives',

    # --- Projekt-előkészítés / Preparation -----------------------------------
    'projekt-elokeszites/index':                             'preparation/index',
    'projekt-elokeszites/telekalkalmassag':                  'preparation/plot-suitability',
    'projekt-elokeszites/telekalkalmassag-attekintese':      'preparation/plot-suitability-overview',
    'projekt-elokeszites/talaj-es-szivargokepesseg':         'preparation/soil-and-infiltration-capacity',
    'projekt-elokeszites/talajviz':                          'preparation/groundwater',
    'projekt-elokeszites/kut-es-vedotavolsag':               'preparation/wells-and-protective-distance',
    'projekt-elokeszites/telekmeret-es-szabad-terulet':      'preparation/plot-size-and-available-area',
    'projekt-elokeszites/lejtes-es-csomelyseg':              'preparation/gradient-and-pipe-depth',
    'projekt-elokeszites/jarmuterheles-es-hozzaferes':       'preparation/vehicle-loading-and-access',
    'projekt-elokeszites/telekadatok-osszegyujtese':         'preparation/how-to-gather-the-plot-data',
    'projekt-elokeszites/telek-es-vizelhelyezesi-eloszuro':  'preparation/plot-and-disposal-pre-screener',
    'projekt-elokeszites/tisztitott-viz-elhelyezese':        'preparation/treated-water-disposal',
    'projekt-elokeszites/elszivarogtatas':                   'preparation/soakaway-infiltration',
    'projekt-elokeszites/tisztitomezo':                      'preparation/drainage-field',
    'projekt-elokeszites/gyokerzonas-elhelyezes':            'preparation/reed-bed-disposal',
    'projekt-elokeszites/magas-talajvizi-helyzetek':         'preparation/high-groundwater-situations',
    'projekt-elokeszites/szivarogtatasi-vizsgalat':          'preparation/percolation-test',
    'projekt-elokeszites/mikor-szukseges-szakerto':          'preparation/when-you-need-an-expert',
    'projekt-elokeszites/terheles-es-kapacitas':             'preparation/load-and-capacity',
    'projekt-elokeszites/lakosegyenertek':                   'preparation/population-equivalent',
    'projekt-elokeszites/szemelyszam-es-vizfogyasztas':      'preparation/occupancy-and-water-use',
    'projekt-elokeszites/atlag-es-csucsterheles':            'preparation/average-and-peak-load',
    'projekt-elokeszites/szezonalis-hasznalat':              'preparation/seasonal-use',
    'projekt-elokeszites/panziok-es-vendeglatas':            'preparation/guesthouses-and-hospitality',
    'projekt-elokeszites/intezmenyi-terheles':               'preparation/institutional-load',
    'projekt-elokeszites/specialis-vagy-ipari-szennyviz':    'preparation/special-or-industrial-wastewater',
    'projekt-elokeszites/terhelesi-profil-eloszuro':         'preparation/load-profile-pre-qualifier',

    # --- Eredmények / Results ------------------------------------------------
    'eredmenyek/csikvand':      'results/csikvand',
    'eredmenyek/bakonypeterd':  'results/bakonypeterd',
    'eredmenyek/diosbereny':    'results/diosbereny',
    'eredmenyek/obudavar':      'results/obudavar',
}

# Visszafelé is kelleni fog: angol útvonal → magyar.
SZLUG_VISSZA = {v: k for k, v in SZLUG.items()}
assert len(SZLUG_VISSZA) == len(SZLUG), 'ütköző angol szlug a táblában'
