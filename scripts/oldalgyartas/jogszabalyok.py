#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""jogszabalyok.py — `/tudastar/jogszabalyok`: mi változott 2012 óta.

MIÉRT EZ A LAP. A régi webhely 2012. májusi jogszabályi összefoglalója évi 344
organikus kattintást hozott — a lista legnagyobb egyedi tétele. A fájl
visszakerült az eredeti címére, tehát a kattintás landol; a TARTALMA viszont
tizennégy éves, és négy ponton ma mást mond a jogszabály.

Ez a lap nem cáfolja a régit, hanem MELLÉ ÁLL: megmutatja, mi változott, miért,
és mi következik ebből a tulajdonosnak. Aki a 2012-es PDF-et keresi, megkapja —
és megkapja hozzá azt is, amit azóta tudni kell.

FORRÁS. A hatályos állapot a szakmai tudásbázisból jön
(`.claude/skills/otthoni-biologiai-szennyviztisztitas/references/hu-jogszabalyok.md`,
állapot: 2025), a 2012-es állítások a visszaállított PDF-ből. Amit egyik forrás
sem támaszt alá, az NINCS a lapon.

JOGI TARTALOM — FELÜLVIZSGÁLAT AJÁNLOTT. A lap tájékoztat, nem jogi tanácsot ad;
ezt ki is mondja. A jogszabályhelyek ellenőrizhetők: minden tétel mellett ott a
szám és a tárgy.

FUTTATÁS:  python3 scripts/oldalgyartas/jogszabalyok.py
"""
import html as H
import pathlib
import re
import sys
import urllib.parse

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from jogi_oldalak import sec_jogi, sec_tabla
from sablon import sec_faq

GYOKER = pathlib.Path(__file__).resolve().parents[2]
WEB = GYOKER / '_web'
MINTA_LAP = WEB / 'tudastar' / 'elszivarogtatas.html'
REGI_PDF = 'wp-content/uploads/2017/04/jogszabalyok-okotehhome-hu-2012-majus.pdf'

# (jelvény, új-e, cím, 2012-ben, ma, mit jelent Önnek)
VALTOZASOK = [
    ('Változott', False, 'A műszaki alaprendelet ma már ismeri az egyedi megoldásokat',
     'A 30/2008. (XII. 31.) KvVM rendeletről azt írtuk: „a törvényhozó megfeledkezett az '
     'egyedi szennyvíztisztítási megoldásokról, csak a központi szennyvízelvezetéssel '
     'foglalkozik”.',
     'Ez a rendelet a vizek hasznosítását szolgáló létesítmények <strong>műszaki '
     'szabályait</strong> adja, és a <strong>4. melléklete</strong> tartalmazza az egyedi '
     'szennyvíztisztítókra vonatkozó határértékeket.',
     'A kifolyó vízre vonatkozó követelményt itt kell keresni. A 28/2004. a felszíni vízbe '
     '(élővízbe) vezetés határértékeit adja — az más eset.'),

    ('Változott', False, 'Háromévente, nem ötévente',
     'Az összefoglaló szerint a felülvizsgálatok gyakoriságát az engedélyt kiadó szerv '
     'állapítja meg, „mely általában 5 év”.',
     'CE-jelölt lakossági kisberendezésnél a teljes engedélyezés helyett <strong>kötelező '
     'önellenőrzés</strong> terheli a tulajdonost: mintavétel és analitika a létesítéskor, '
     'majd <strong>háromévente</strong>, az eredmény a jegyzőnek 15 napon belül '
     '(147/2010. Korm. r.).',
     'Ez a <strong>tulajdonos</strong> kötelezettsége, nem a gyártóé. Érdemes naptárba tenni: '
     'a hároméves ciklus attól a naptól indul, amikor a berendezés üzembe állt.'),

    ('Változott', False, 'Más a hatóság neve — és néha más a hatóság is',
     'A másodfok az „Országos Környezet- és Vízügyi Főfelügyelőség”, a szikkasztási '
     'határértéket a „Vízügyi Felügyelőségek” írták elő.',
     'A <strong>jegyző</strong> marad, ha mindhárom teljesül: legfeljebb 500 m³/év '
     'kibocsátás, kizárólag háztartási szennyvíz, és a tisztított víz elszikkasztása. '
     'Minden más esetben a <strong>megyei katasztrófavédelmi igazgatóság</strong> jár el '
     'vízügyi hatóságként.',
     'Ha élővízbe vezetne, vagy 500 m³/év fölött van a kibocsátás, nem a jegyzőhöz kell '
     'fordulni. Rossz hatóságnál indított eljárás hónapokat vesz el.'),

    ('Új szabály', True, 'Megvan, mit kell benyújtani',
     'A kérelem tartalmát nem egyetlen jogszabály sorolta fel; a 2012-es összefoglalóban '
     'nem is szerepel ilyen lista.',
     'A <strong>41/2017. (XII. 29.) BM rendelet</strong> 3. melléklete tételesen megadja a '
     'vízjogi engedélyezési dokumentáció tartalmát. A szakhatóságok kijelölése az '
     '531/2017. Korm. rendeletben áll.',
     'A tervezőnek ehhez kell igazodnia. Az eljárás <strong>illetékmentes</strong>, a '
     'határidő <strong>60 nap</strong>; a dokumentációt vízilétesítmény-tervezésre jogosult '
     'szakember készíti.'),

    ('Változott', False, 'A kibocsátási határértékek rendeletét módosították',
     'A 28/2004. (XII. 25.) KvVM rendelet 2. számú mellékletére hivatkoztunk, a 2012-es '
     'szöveggel.',
     'A rendelet hatályos, de <strong>a 7/2023. (III. 13.) BM rendelet módosította</strong>, '
     '2023. június 26-i hatállyal.',
     'Ha egy régi tervben vagy ajánlatban a 28/2004. valamelyik értéke szerepel, érdemes '
     'megnézni, a mai szöveg szerint áll-e ott.'),

    ('Amire figyeljen', False, 'A talajterhelési díjnak ma kiírható a mértéke',
     'Az összefoglaló a mentesülés feltételét ismertette, összeget nem közölt.',
     'Az egységdíj <strong>1 200 Ft/m³</strong>, ezt szorozza a terület '
     'érzékenységi szorzója (a legérzékenyebb területen háromszoros). A bevallás '
     'önadózással, <strong>március 31-ig</strong> történik.',
     'Aki egyedi szennyvíztisztító kisberendezést használ és évente igazolja a '
     'határérték-tartást, <strong>mentesülhet vagy kedvezményt kaphat</strong> — de a '
     'konkrét kedvezményt a <strong>helyi önkormányzati rendelet</strong> adja, ezért azt a '
     'telepítés szerinti településen kell ellenőrizni.'),
]

HATALYOS = [
    ('1995. évi LVII. tv.', 'A vízgazdálkodásról (Vgtv.)',
     'A keret: vízilétesítmény létesítéséhez, üzemeltetéséhez, fennmaradásához és '
     'megszüntetéséhez vízjogi engedély kell.'),
    ('72/1996. (V. 22.) Korm. r.', 'Vízgazdálkodási hatósági jogkör',
     'Ez választja szét a jegyzői és a vízügyi hatáskört; itt áll az 500 m³/év küszöb.'),
    ('147/2010. (IV. 29.) Korm. r.', 'A vizek hasznosítása és védelme — általános szabályok',
     'Az egyedi tisztító telepítési feltételei, és a háromévenkénti önellenőrzés.'),
    ('30/2008. (XII. 31.) KvVM r.', 'Ugyanezek műszaki szabályai',
     'A 4. melléklet adja az egyedi tisztítók határértékeit. Érzékeny vagy magas '
     'talajvizű területen csak denitrifikációval működő berendezés telepíthető.'),
    ('41/2017. (XII. 29.) BM r.', 'A vízjogi engedélyezési dokumentáció tartalma',
     'A 3. melléklet sorolja fel, mit kell benyújtani.'),
    ('28/2004. (XII. 25.) KvVM r.', 'Vízszennyező anyagok kibocsátási határértékei',
     'A felszíni vízbe és a csatornába vezetés határértékei. Módosítva: 7/2023. (III. 13.) BM.'),
    ('27/2004. (XII. 25.) KvVM r.', 'Érzékeny települések besorolása',
     'A felszín alatti víz szempontjából érzékeny területeken szigorúbb az elhelyezés.'),
    ('219/2004. (VII. 21.) Korm. r.', 'A felszín alatti vizek védelme',
     'A szikkasztás alapvédelme.'),
    ('220/2004. (VII. 21.) Korm. r.', 'A felszíni vizek minőségvédelme',
     'Az élővízbe vezetés alapja.'),
    ('253/1997. (XII. 20.) Korm. r. (OTÉK)', 'Településrendezési és építési követelmények',
     'A közműpótló a központi közmű hiányában alkalmazható; a zárt szennyvíztároló '
     'végső megoldás.'),
    ('2003. évi LXXXIX. tv.', 'Környezetterhelési díj — ebből a talajterhelési díj',
     'Kit terhel, mi az alapja, és mikor lehet mentesülni.'),
    ('531/2017. (XII. 29.) Korm. r.', 'Szakhatóságok kijelölése',
     'Melyik szakhatóságot kell bevonni az eljárásba.'),
]

GYIK = [
    ('Használható még a 2012-es összefoglalójuk?',
     'Tájékozódásra igen, és épp ezért hagytuk elérhetően — de négy ponton ma mást mond a '
     'jogszabály, mint akkor. Ezeket fent tételesen összeszedtük. Ha a régi anyagból dolgozik, '
     'a hatóság megnevezését, a felülvizsgálati ciklust és a műszaki rendelet szerepét '
     'mindenképpen a mai állapot szerint nézze.'),
    ('Kell-e vízjogi engedély egy házi szennyvíztisztítóhoz?',
     'A vízilétesítmény főszabály szerint engedélyköteles. CE-jelölt, gyári lakossági '
     'kisberendezésnél viszont könnyített rezsim él: a teljes engedélyezés helyett a '
     'tulajdonost kötelező önellenőrzés terheli. Hogy egy konkrét projektben melyik út '
     'járható, azt a kapacitás, a szennyvíz eredete és a tisztított víz elhelyezése dönti el.'),
    ('Ki engedélyezi — a jegyző vagy a vízügyi hatóság?',
     'A jegyző, ha mindhárom teljesül: legfeljebb 500 m³/év kibocsátás, kizárólag háztartási '
     'szennyvíz, és a tisztított víz elszikkasztása. Ha bármelyik hiányzik — nagyobb '
     'mennyiség, nem háztartási szennyvíz, vagy élővízbe vezetés —, a megyei '
     'katasztrófavédelmi igazgatóság jár el vízügyi hatóságként.'),
    ('Mennyibe kerül az eljárás, és mennyi ideig tart?',
     'A vízjogi engedélyezés illetékmentes, az ügyintézési határidő 60 nap. A költség a '
     'tervezői munkáé: a dokumentációt vízilétesítmény-tervezésre jogosult szakember '
     'készíti. Szakhatóságként a járási hivatal népegészségügyi feladatköre, védett '
     'területen a természetvédelmi hatóság működik közre.'),
    ('Mentesülök a talajterhelési díj alól, ha tisztítót telepítek?',
     'Ez a lehetőség megvan: aki egyedi szennyvíztisztító kisberendezést alkalmaz és évente '
     'igazolja, hogy a vizsgált komponensek egyike sem haladja meg 20%-kal az alapállapotot, '
     'mentesülhet vagy kedvezményt kaphat. A konkrét kedvezményt viszont a helyi '
     'önkormányzati rendelet adja meg, ezért azt a telepítés szerinti településen kell '
     'ellenőrizni.'),
]


def valtozas_kartyak():
    ki = []
    for jel, uj, cim, regen, ma, kov in VALTOZASOK:
        ki.append(f'''        <li class="valtozas">
          <p class="type-ui-caption valtozas-jel{' valtozas-jel-uj' if uj else ''}">{jel}</p>
          <h3 class="type-ui-card-title valtozas-cim">{H.escape(cim)}</h3>
          <dl class="valtozas-sor">
            <dt>2012-ben</dt><dd class="type-ui-body">{regen}</dd>
            <dt>Ma</dt><dd class="type-ui-body valtozas-ma">{ma}</dd>
          </dl>
          <p class="type-ui-body valtozas-kovetkezmeny"><strong>Mit jelent Önnek:</strong> {kov}</p>
        </li>''')
    nl = chr(10)
    return f'''
  <section class="section" aria-labelledby="valtozasok-cim">
    <div class="section-inner">
      <header class="section-head section-head-start">
        <p class="type-data-eyebrow section-eyebrow">Ami változott</p>
        <h2 class="type-display-section-title section-title" id="valtozasok-cim">Hat pont, ahol ma mást mond a jogszabály</h2>
        <p class="type-ui-body section-lead">Nem elírásról van szó: 2012-ben ez volt a
          helyzet. Azóta viszont módosultak a rendeletek, és átalakult a hatósági
          szervezet — ezeket szedtük össze.</p>
      </header>
      <ul class="valtozas-racs" role="list">
{nl.join(ki)}
      </ul>
    </div>
  </section>
'''


def letoltes_szakasz():
    href = '../' + urllib.parse.quote(REGI_PDF)
    meret = (WEB / REGI_PDF).stat().st_size
    return sec_jogi('A régi összefoglaló', 'A 2012-es anyag — elérhető maradt', [
        ('p', 'Sokan a saját könyvjelzőjükből érik el, és hivatkoznak rá. Nem vettük le: '
              'ott van az eredeti címén, ahol eddig is volt. Azt viszont fontosnak tartjuk '
              'kimondani, hogy <strong>2012. májusi állapotot</strong> tükröz.'),
        ('p', f'<a class="text-link" href="{href}"><span class="link-label">'
              f'Jogszabályi összefoglaló — 2012. május'
              f'<span class="action-arrow-end" aria-hidden="true">&darr;</span></span></a> '
              f'<span class="type-ui-caption">PDF, {(meret + 512) // 1024} KB</span>'),
        ('kiemelt', 'Ha a régi anyagból dolgozik, három dolgot nézzen meg a mai állapot '
                    'szerint: <strong>ki a hatóság</strong>, <strong>milyen ritmusban kell '
                    'mintát venni</strong>, és <strong>melyik rendeletben</strong> keresse a '
                    'kifolyó vízre vonatkozó határértéket.'),
    ])


def keret_szinkron(html):
    """A keretet egy KIADOTT lapról vesszük, nem a sablonból — az elavult."""
    minta = MINTA_LAP.read_text(encoding='utf-8')
    fej = minta[:minta.index('</head>')]
    minta_re = re.compile(
        r'<link rel="preload" as="font"[^>]*>'
        r'|<script>\(\(\)=>\{try\{var t=localStorage.*?</script>'
        r'|<script src="[^"]*(?:tema|suti|kampany)\.js[^"]*"[^>]*></script>', re.S)
    for m in minta_re.finditer(fej):
        if m.group(0) not in html:
            html = html.replace('</head>', m.group(0) + '\n</head>', 1)
    veg = minta[minta.rindex('</footer>') + len('</footer>'):]
    sorok = re.findall(r'<script[^>]*src="[^"]*"[^>]*></script>', veg)
    regi = re.search(r'<script[^>]*src="[^"]*site\.js[^"]*"[^>]*></script>', html)
    if regi and sorok:
        html = html[:regi.start()] + '\n'.join(sorok) + html[regi.end():]
    return html


OLDAL = dict(
    file='tudastar/jogszabalyok.html', url='tudastar/jogszabalyok', img='engedelyezes',
    title='Szennyvíz jogszabályok — mi változott 2012 óta?',
    desc='A házi szennyvíztisztítóra vonatkozó hatályos jogszabályok, és hat pont, '
         'ahol ma mást mond a szabály, mint a 2012-es összefoglalónkban.',
    h1='Jogszabályi áttekintés',
    alt='Hatósági dokumentumok és pecsét egy íróasztalon',
    lead='A 2012-es összefoglalónkat ma is sokan használják. Nem vettük le — de mellé '
         'tettük, mi változott azóta.',
    crumbs=[('Főoldal', '../'), ('Tudástár', './')],
    sections=[
        sec_jogi('Miért ez a lap', 'Tizennégy év alatt sok minden változott', [
            ('p', 'A házi szennyvíztisztítók engedélyezése nem egyetlen jogszabályban áll: '
                  'a keretet a vízgazdálkodási törvény adja, a hatáskört egy kormányrendelet '
                  'osztja szét, a műszaki követelményt egy miniszteri rendelet, a '
                  'határértéket egy másik, a talajterhelési díjat pedig egy törvény és a '
                  'helyi önkormányzati rendelet együtt.'),
            ('p', 'Ebből következik, hogy egy összefoglaló <strong>gyorsan elavul</strong>. '
                  'A miénk 2012-ben készült, és azóta négy ponton módosultak a szabályok, '
                  'két helyen pedig olyan rendelet lépett be, ami akkor még nem létezett. '
                  'Ez a lap ezt vezeti át — nem a régi helyett, hanem mellé.'),
            ('kiemelt', 'Ez a lap <strong>tájékoztat, nem jogi tanácsot ad</strong>. A '
                        'hivatkozott jogszabályt minden esetben érdemes elolvasni, a konkrét '
                        'projektet pedig az adott helyszín és a hatóság alapján megítélni.'),
        ]),
        valtozas_kartyak(),
        sec_jogi('Gyakori tévedés', 'A 78/2008. nem a szennyvízről szól', [
            ('p', 'Műszaki leírásokban és fórumokon vissza-visszatér a <strong>78/2008. '
                  '(IV. 3.) Korm. rendelet</strong> mint a szennyvíz műszaki rendelete. '
                  'Ez a rendelet a <strong>természetes fürdővizekről</strong> szól.'),
            ('kiemelt', 'A helyes hivatkozás a <strong>30/2008. (XII. 31.) KvVM '
                        'rendelet</strong> — a vizek hasznosítását, védelmét és kártételeinek '
                        'elhárítását szolgáló tevékenységekre és létesítményekre vonatkozó '
                        'műszaki szabályokról.'),
        ]),
        sec_tabla('Hatályos jogszabályok', 'Mi vonatkozik egy házi szennyvíztisztítóra',
                  'Szám, tárgy, és hogy az adott jogszabályban mit kell keresni.',
                  ['Jogszabály', 'Tárgy', 'Amit ad'],
                  [(f'<span class="jogi-cikk">{sz}</span>', H.escape(t), l)
                   for sz, t, l in HATALYOS]),
        sec_jogi('Ami jön', 'Egy uniós irányelv, ami még nincs átültetve', [
            ('p', 'A települési szennyvíz kezeléséről szóló irányelv átdolgozása '
                  '— <strong>(EU) 2024/3019</strong> — 2024-ben megszületett. Az egyedi '
                  'rendszereket úgy érinti, hogy ha egy tagállam a 2000 lakosegyenérték '
                  'feletti agglomerációk terhelésének több mint 2%-át kezeli egyedi '
                  'rendszerrel, azt <strong>indokolnia kell</strong>.'),
            ('p', 'Az átültetés határideje <strong>2027. július 31.</strong> A magyar '
                  'átültető jogszabály még nem ismert, ezért ma nem lehet megmondani, '
                  'pontosan mit jelent majd egy családi ház szintjén. Amint kihirdetik, '
                  'ezt a lapot frissítjük.'),
            ('p', 'Ugyanígy frissül a vízgyűjtő-gazdálkodási terv, és vele az érzékeny '
                  'területek listája — ez közvetve az elhelyezés feltételeire hat.'),
        ]),
        letoltes_szakasz(),
        sec_faq(GYIK),
    ],
)


def main():
    html = G.build(OLDAL)
    html = keret_szinkron(html)
    ki = WEB / OLDAL['file']
    ki.write_text(html, encoding='utf-8')
    szo = len(re.sub(r'<[^>]+>', ' ', html).split())
    print(f"  {OLDAL['file']}: {ki.stat().st_size // 1024} KB · {szo} szó")


if __name__ == '__main__':
    main()
