#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Előkészítés → Tisztított víz elhelyezése — hub és a brief szerinti hat aloldal.

A brief NÉGY ponton pontosít a jelenlegi ÖkoTech-kommunikációhoz képest:

1. Az „elszivárogtatás" és a „tisztítómező" NEM szinonima. Aktív biológiai
   rendszer után a tisztítás már a berendezésben megtörtént, a szikkasztó a
   kilépő víz ELHELYEZÉSÉRE szolgál. Oldómedencénél viszont a talajban
   kialakított mező maga a technológia része — a 147/2010. is „tisztítómezővel
   ellátott oldómedencés létesítményről" beszél.

2. A „gyökérzónás öntözés" jelenlegi megfogalmazása műszakilag és jogilag
   pontosítandó. Külön kategória a felszín alatti elhelyezés, a dísznövényzet
   vízellátása és a szabályozott mezőgazdasági víz-újrahasználás; ez utóbbira
   az EU 2020/741 külön minőség- és kockázatkezelési rendszert állít.

3. A szikkasztó-méretezés lehet az ÖkoTech egyik legerősebb tudásterülete, de
   a jelenlegi cikkek konkrét számai (alagút-darabszám, dréncső-egyenérték)
   csak dokumentált input→méretezés→eredmény összefüggéssel publikálhatók.

4. A vízelhelyezés az ajánlatadás ELŐFELTÉTELE, nem utólagos kiegészítő.
   Ne lehessen ajánlatkész állapotba jutni úgy, hogy a látogató nem tudja,
   hová kerül a napi kifolyó vízmennyiség.

ÁR SEHOL nem szerepel; a kialakítások legfeljebb költségbefolyásoló
tényezőként különíthetők el.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import (sec_numbered, sec_split, sec_prose, sec_situations,
                    sec_cta, sec_faq)

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

JOGI = ('<!-- JOGI ELLENŐRZÉS PUBLIKÁLÁS ELŐTT. Érintett: 147/2010. Korm. rendelet 25–26. § ·\n'
        '     27/2004. KvVM rendelet érzékenységi besorolása (2026-ban módosult melléklet) ·\n'
        '     219/2004. Korm. rendelet · felszíni befogadónál vízjogi és kibocsátási\n'
        '     követelmények · víz-újrahasználásnál az EU 2020/741 hatálya. Dátumozott\n'
        '     felülvizsgálat kell hozzá. -->')


def hiany(mi, honnan):
    return (f'<!-- ADATHIÁNY: {mi}\n'
            f'     Forrás: {honnan}. Addig konkrét értékkel nem publikálható. -->')


HOME = ('Főoldal', '../')
ELO = ('Előkészítés', './')
CRUMB = [HOME, ELO]
HUB = [HOME, ELO, ('Tisztított víz elhelyezése', 'tisztitott-viz-elhelyezese')]


# ===========================================================================
# HUB
# ===========================================================================
def epit_hub():
    return [
        sec_prose('Miért külön téma', 'A berendezés kiválasztása nem zárja le a projektet', [
            'A biológiai szennyvíztisztító kiválasztásával a feladat fele van kész. A '
            'másik fele az, hogy <strong>hová és milyen módon kerül a berendezésből kilépő '
            'tisztított víz</strong> — és ezt már a tervezéskor meg kell határozni, nem a '
            'telepítés hetében.',
            'A napi kilépő vízmennyiség nagyjából annyi, amennyi szennyvíz beérkezik. Ez nem '
            'tűnik el: valahol el kell helyezni. Ezért a vízelhelyezés iránya az '
            'ajánlatadás <strong>előfeltétele</strong>, nem utólagos kiegészítő — ha ez '
            'nincs tisztázva, a projekt nem ajánlatkész.',
            'Ez a szakasz az elhelyezési irányokat és a hozzájuk tartozó feltételeket veszi '
            'végig. Nem ad univerzális javaslatot: a végeredmény egy <em>valószínű '
            'elhelyezési irány</em>, a hozzá szükséges telekadatokkal és az esetleg '
            'szükséges vizsgálatokkal együtt.',
        ]),

        sec_situations('Elhelyezési irányok', 'Hová kerülhet a tisztított víz?',
                       'Három fő irány, eltérő műszaki és szabályozási feltételekkel. '
                       'Nem egyenrangú alternatívák: az első a leggyakoribb, a harmadik '
                       'külön szakmai és jogi ág.',
                       [
                           ('nav-vizelvezetes', 'Elszivárogtatás',
                            'A leggyakoribb helyi megoldás: a már megtisztított víz '
                            'felszín alatti elhelyezése a talajban. A talaj mért '
                            'befogadóképességén, a talajvízen és a szabad területen múlik.',
                            'elszivarogtatas', 'Elszivárogtatás'),
                           ('oldomedence', 'Tisztítómező',
                            'Oldómedencés rendszernél a talajban kialakított mező nem '
                            'kiegészítő, hanem a tisztítás része. Ezért nagyobb a '
                            'területigénye, és nem helyezhető át szabadon.',
                            'tisztitomezo', 'Tisztítómező'),
                           ('nav-vizminoseg', 'Gyökérzónás elhelyezés',
                            'A telken belüli hasznosítás növényzeti területen. Pontos '
                            'műszaki definícióval és világos használati korlátokkal — '
                            'nem azonos a szabályozott mezőgazdasági öntözéssel.',
                            'gyokerzonas-elhelyezes', 'Gyökérzónás elhelyezés'),
                       ]),

        sec_split('A leggyakoribb félreértés', 'Elszivárogtatás vagy tisztítómező?',
                  'Aktív biológiai rendszer után — elszivárogtatás',
                  ['A tisztítás a BERENDEZÉSBEN történt meg',
                   'A szikkasztó a kilépő víz elhelyezésére szolgál',
                   'A helyigény jellemzően kisebb',
                   'A méretezés a napi vízmennyiség és a mért szivárgás függvénye',
                   'A hely — kellő körültekintéssel — megválasztható'],
                  'Oldómedence után — tisztítómező',
                  ['A medencében ANAEROB előkezelés történik',
                   'Az aerob folyamat jelentős része a MEZŐBEN zajlik',
                   'A mező a technológia része, nem elvezetés',
                   'A területigény ezért jellemzően nagyobb',
                   'A jogszabály is „tisztítómezővel ellátott" létesítményt nevez meg']),

        sec_numbered('Amitől függ', 'Mi dönti el, melyik irány jöhet szóba?',
                     'Ezek együtt hatnak. Egyetlen kedvezőtlen tényező is átírhatja az '
                     'irányt, de egyetlen kedvező sem elég önmagában.',
                     ['<strong>A talaj mért szivárgóképessége.</strong> Nem a talaj neve. '
                      'Ez határozza meg, befogadja-e a talaj a napi vízmennyiséget, és '
                      'mekkora felületen.',
                      '<strong>A talajvíz szezonális maximuma.</strong> Nem a mai vízállás. '
                      'A szikkasztó és a talajvíz viszonya a működés alapfeltétele.',
                      '<strong>A napi kifolyó vízmennyiség.</strong> A terhelésből adódik, '
                      'és a szikkasztó méretét közvetlenül meghatározza.',
                      '<strong>A rendelkezésre álló szabad terület.</strong> A szükséges '
                      'felületnek el is kell férnie — a ház, kút, behajtó és a tervezett '
                      'építmények után.',
                      '<strong>Kút és vízbázisvédelem.</strong> A tisztított víz talajba '
                      'jutásának pontja vízvédelmi szempontból önálló objektum.',
                      '<strong>Területi érzékenységi besorolás.</strong> Fokozottan érzékeny '
                      'területen a földtani közegbe történő bevezetésre külön feltételek '
                      'vonatkoznak.']),

        sec_prose('Amit ez a szakasz nem tesz', 'Nincs univerzális elhelyezési javaslat', [
            'Az elhelyezési irány telekspecifikus. Ugyanaz a berendezés két szomszédos '
            'telken más megoldást igényelhet — és van, ahol a helyi elhelyezés nem oldható '
            'meg. Ezért itt nem javaslatot adunk, hanem feltételeket és döntési útvonalat.',
            'A <strong>felszíni befogadóba vezetés</strong> ezért külön, szakmai és jogi ág: '
            'vízjogi engedélyt és kibocsátási feltételek teljesítését igényli, és nem '
            'kezelhető a helyi elhelyezés egyszerű alternatívájaként. Ha ez merül fel, '
            'jogosult tervező és hatósági egyeztetés következik.',
            'Konkrét árat sem közlünk. A különböző kialakítások költségszintje eltér — '
            'nagyobb szikkasztó, szivattyús vízvezetés, speciális kialakítás mind '
            'költségbefolyásoló tényező —, de ez a projekt egészében értelmezhető, nem '
            'önmagában.',
        ]),

        sec_cta('Következő lépés', 'Kezdje a leggyakoribb iránnyal',
                ['A legtöbb családi házas projektnél az elszivárogtatás az első vizsgálandó '
                 'irány. Ha a talaj és a talajvíz megengedi, ez a legegyszerűbb megoldás — '
                 'és rögtön kiderül, mit kell hozzá megmérni.'],
                'Elszivárogtatás', 'elszivarogtatas',
                alt=('Mikor szükséges szakértő?', 'mikor-szukseges-szakerto')),

        sec_faq([
            ('Mennyi víz jön ki naponta a berendezésből?',
             'Nagyjából annyi, amennyi szennyvíz beérkezik — a biológiai tisztítás a '
             'szennyezőanyagot bontja le, nem a vizet tünteti el. Ezért nem lehet a '
             'szikkasztót az udvaron maradt helyhez méretezni: a napi vízmennyiséghez kell.'),
            ('Ha jó a talaj, akkor rendben van a vízelhelyezés?',
             'Nem feltétlenül. Jó vízbefogadó talaj mellett is akadály lehet a magas '
             'szezonális talajvíz, a szűk szabad terület, a kút közelsége vagy a terület '
             'érzékenységi besorolása. A talaj az egyik feltétel, nem az egyetlen.'),
            ('Bevezethető a víz a patakba vagy az árokba?',
             'Ez külön szakmai és jogi kérdés: vízjogi engedélyt és kibocsátási '
             'követelmények teljesítését igényli, és nem minden helyszínen jöhet szóba. '
             'Nem kezelhető a helyi elszivárogtatás egyszerű alternatívájaként — jogosult '
             'tervezővel és a hatósággal kell egyeztetni.'),
            ('Locsolhatok a tisztított vízzel?',
             'A telken belüli hasznosításnak vannak műszaki és használati feltételei, és '
             'nem minden felhasználás megengedhető. Ezt külön oldalon tárgyaljuk, mert a '
             'kérdés érzékeny: más a dísznövényzet és más az élelmiszernövény, és a '
             'szabályozott mezőgazdasági újrahasználat megint külön jogi kategória.'),
            ('Mikor kell szakértő?',
             'Ha a talajvíz nem ismert, a szivárgóképesség nincs mérve, a telek kijelölt '
             'vízbázisvédelmi területet érinthet, felszíni befogadó merül fel, vagy nagyobb '
             'illetve nem kommunális projektről van szó. Ezeket külön oldal veszi végig.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 1) Elszivárogtatás
# ===========================================================================
def epit_elszivarogtatas():
    return [
        sec_prose('Mit jelent', 'A már megtisztított víz elhelyezése', [
            'Aktív biológiai rendszernél az elszivárogtatás <strong>nem a szennyvíztisztítás '
            'fő folyamata</strong>, hanem a már biológiailag megtisztított víz talajban '
            'történő elhelyezése. Ez a különbség fontos: a szikkasztó itt nem tisztít, hanem '
            'befogad.',
            'A kialakítás felszín alatti: a berendezésből kilépő víz elosztó rendszeren '
            'keresztül jut a talajba, jellemzően kavicságyba fektetett elemekkel. A felszínen '
            'ebből nem látszik semmi, és a terület — bizonyos korlátok között — használható '
            'marad.',
        ]),

        sec_prose('A méretezés a kritikus pont', 'Nem a maradék helyhez kell igazítani', [
            'A rendszer megfelelő méretezése kritikus. Alulméretezett szikkasztónál '
            '<strong>visszaduzzadás</strong> és a talaj <strong>eliszapolódása</strong> '
            'jelentkezhet, ami működési problémához és költséges helyreállításhoz vezet. '
            'Ez nem elméleti kockázat, hanem a leggyakoribb utólagos hiba ebben a '
            'rendszertípusban.',
            'A szükséges méret nem a berendezés típusából következik, hanem négy adatból: a '
            '<strong>napi vízmennyiségből</strong>, a talaj <strong>mért '
            'szivárgóképességéből</strong>, a <strong>talajvíz</strong> helyzetéből és a '
            'rendelkezésre álló <strong>területből</strong>. A beérkező szennyvíz mennyisége '
            'lényegében a rendszerből elhelyezendő vízmennyiségként jelenik meg.',
            'Ebből következik a legfontosabb gyakorlati szabály: a szikkasztót nem lehet az '
            'udvaron maradt helyhez méretezni. Ha a szükséges felület nem fér el, nem a '
            'szikkasztót kell kisebbre venni — más elhelyezési irányt kell keresni.',
        ]),

        sec_numbered('A feltételek', 'Mit kell tisztázni az elszivárogtatáshoz?', '',
                     ['<strong>Mért szivárgóképesség.</strong> A szikkasztó tervezett helyén '
                      'és mélységében, szivárogtatási vizsgálattal. Talajtípus-megnevezésből '
                      'nem vezethető le.',
                      '<strong>Szezonális legmagasabb talajvíz.</strong> Nem a mai vízállás. '
                      'A szikkasztó és a talajvíz közötti viszony a működés feltétele.',
                      '<strong>Napi elhelyezendő vízmennyiség.</strong> A háztartás '
                      'terheléséből adódik; nagyobb terhelés arányosan nagyobb felületet '
                      'igényel.',
                      '<strong>Elegendő szabad terület.</strong> A szükséges felület, '
                      'a szervizhozzáféréssel és a későbbi területhasználattal együtt.',
                      '<strong>Gravitációs vagy szivattyús vízvezetés.</strong> Ha a '
                      'szikkasztó a berendezés kifolyójánál magasabban van, szivattyú kell.',
                      '<strong>Kút, vízbázisvédelem, érzékenységi besorolás.</strong> '
                      'A tisztított víz talajba jutásának pontja vízvédelmi szempontból '
                      'önálló objektum.']),

        sec_split('Hosszú távon', 'Mi rontja el, és mi tartja működésben',
                  'Ezek okoznak problémát',
                  ['Alulméretezett felület — visszaduzzadás, eliszapolódás',
                   'A talajvíz szezonális megemelkedése a szikkasztó szintjéig',
                   'A terület tömörítése, burkolása, járműterhelés',
                   'Mély gyökérzetű növényzet a szikkasztó fölött',
                   'A berendezés elhanyagolt karbantartása — a kilépő víz minősége romlik',
                   'Csapadékvíz rávezetése a rendszerre'],
                  'Ezek tartják működésben',
                  ['Mért adaton alapuló méretezés, tartalékkal',
                   'A talajvíztől megfelelő távolságra tartott elhelyezési szint',
                   'A terület fölött gyep vagy sekély gyökérzetű növényzet',
                   'A berendezés rendszeres karbantartása',
                   'A csapadékvíz külön elvezetése',
                   'A terület jövőbeli használatának előre tisztázása']),

        hiany('a szikkasztó szükséges mérete adott napi vízmennyiséghez és mért szivárgási '
              'értékhez; a beépített alagútelem darabszáma; a dréncsöves kialakítással való '
              'egyenérték',
              'ÖkoTech belső méretezési algoritmus + az alkalmazott alagútmodell aktuális '
              'gyártói adatlapja. A jelenlegi cikk számaihoz nincs dokumentálva a mért '
              'szivárgási érték, a napi terhelés, a biztonsági tényező és a talajvízmélység, '
              'amire vonatkoznak'),

        sec_cta('Következő lépés', 'A méretezés mért adatot kér',
                ['Az elszivárogtatás megvalósíthatósága azon áll vagy bukik, hogy a talaj '
                 'ténylegesen mennyi vizet nyel el. Ezt mérni kell — a szivárogtatási '
                 'vizsgálat oldala megmutatja, hogyan és mikor.'],
                'Szivárogtatási vizsgálat', 'szivarogtatasi-vizsgalat',
                alt=('Tisztított víz elhelyezése', 'tisztitott-viz-elhelyezese')),

        sec_faq([
            ('Mekkora szikkasztó kell egy négyfős családhoz?',
             'Erre szándékosan nem adunk számot, mert a talaj mért szivárgóképessége nélkül '
             'nem lenne megalapozott. Ugyanaz a négyfős háztartás az egyik talajon jóval '
             'kisebb, a másikon többszörös felületet igényel. A létszám csak az egyik '
             'bemenet — a mérés a másik.'),
            ('Látszik valami a felszínen?',
             'Jellemzően nem. A kialakítás felszín alatti, fölötte gyep vagy sekély gyökerű '
             'növényzet lehet. Ami nem lehet: burkolat, tömörítés, járműforgalom és mély '
             'gyökérzetű fa.'),
            ('Mi történik, ha alulméretezett a szikkasztó?',
             'A víz nem távozik elég gyorsan, visszaduzzad, a talaj pórusai eliszapolódnak, '
             'és a rendszer fokozatosan romlik. A helyreállítás jellemzően a szikkasztó '
             'bontását és újraépítését jelenti — lényegesen drágábban, mint amennyibe az '
             'előzetes mérés került volna.'),
            ('Elszivárogtatható a víz agyagos talajon?',
             'Nehezebben, nagyobb felületen, és van, ahol egyáltalán nem. Ezt mérés dönti el, '
             'nem a talaj megnevezése. Ha a helyi elhelyezés nem oldható meg, más irányt kell '
             'vizsgálni — ilyenkor érdemes korán szakértőhöz fordulni.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 2) Tisztítómező
# ===========================================================================
def epit_tisztitomezo():
    return [
        sec_prose('A legfontosabb különbség', 'A mező nem elvezetés — tisztítás', [
            'Az oldómedencés rendszernél a talajban kialakított tisztítómező '
            '<strong>a technológia része</strong>, nem vízelvezető kiegészítő. Ezért nem '
            'azonos azzal a szikkasztóval, amit aktív biológiai rendszer után alkalmaznak.',
            'A folyamat kétlépcsős: az oldómedencében <strong>anaerob</strong> — oxigén '
            'nélküli — előkezelés történik, a további <strong>aerob</strong> folyamat '
            'jelentős része pedig a mezőben, a talaj felső, levegős rétegében zajlik. '
            'A tisztítás tehát nem fejeződik be a medencében.',
            'Ez a különbség magyarázza a nagyobb területigényt is, és azt, hogy a mező helye '
            'nem tekinthető szabadon áthelyezhető kiegészítőnek. A jogszabály sem véletlenül '
            'nevezi ezt „tisztítómezővel ellátott oldómedencés létesítménynek”.',
        ]),

        sec_numbered('A folyamat', 'Mi történik lépésenként?', '',
                     ['<strong>Oldómedence.</strong> A szennyvíz beérkezik, a szilárd rész '
                      'leülepszik, és anaerob bontás indul. A kilépő víz előkezelt, de még '
                      'nem tisztított.',
                      '<strong>Elosztás.</strong> Az előkezelt víz elosztó rendszeren '
                      'keresztül, egyenletesen jut a mezőbe. Az egyenletes terheléselosztás '
                      'a működés feltétele — ha egy szakasz kap mindent, az hamar telítődik.',
                      '<strong>Aerob kezelés a talajban.</strong> A mező felső, levegős '
                      'rétegében élő mikroorganizmusok bontják tovább a szerves anyagot. '
                      'Ehhez oxigén kell — ezért kritikus, hogy a réteg ne tömörödjön be, '
                      'és ne kerüljön víz alá.',
                      '<strong>Elhelyezés a talajban.</strong> A megtisztított víz a mélyebb '
                      'rétegekbe szivárog. Innentől ugyanazok a feltételek érvényesek, mint '
                      'bármely más talajba juttatásnál.']),

        sec_split('Két rendszer, két helyigény', 'Miért nagyobb a mező?',
                  'Aktív biológiai rendszer szikkasztója',
                  ['A víz már megtisztítva érkezik',
                   'A talaj feladata: befogadás',
                   'A méret a vízmennyiség és a szivárgás függvénye',
                   'Jellemzően kisebb felület',
                   'A hely — korlátok között — megválasztható'],
                  'Oldómedence tisztítómezője',
                  ['A víz előkezelve, de nem tisztítva érkezik',
                   'A talaj feladata: tisztítás ÉS befogadás',
                   'A méret a terheléstől és a talaj oxigénellátásától is függ',
                   'Jellemzően nagyobb felület',
                   'A helye technológiai adottság, nem elrendezési kérdés']),

        sec_numbered('Amit a mező fölött nem lehet', 'A terület használata utána',
                     'A mező működése a talaj levegőzésén múlik. Minden, ami ezt rontja, '
                     'a tisztítás hatásfokát rontja — nem csak a vízelvezetést.',
                     ['Burkolás, betonozás, tömörítés',
                      'Járműforgalom, parkolás, tárolás',
                      'Mély gyökérzetű fák és cserjék telepítése',
                      'Csapadékvíz rávezetése — a mező többletterhelést kap',
                      'Építmény elhelyezése a mező fölé vagy közvetlen mellé',
                      'A terület megbontása anélkül, hogy tudnánk, hol fut az elosztás']),

        hiany('az EPURECO tisztítómező aktuális méretezési szabályai, a talajterhelési '
              'küszöbök, a mező fölötti felszíni használat pontos korlátai, valamint a '
              'mezőtelítődés felismerése és helyreállítása',
              'ÖkoTech műszaki dokumentáció + gyártói adatlap + megvalósult EPURECO '
              'projektek többéves tapasztalata. A szippantási ciklusra vonatkozó jelenlegi '
              'univerzális állítás szintén projekt- és termékfeltételekkel validálandó'),

        sec_cta('Következő lépés', 'A mező is mért talajadatot igényel',
                ['A tisztítómező méretezéséhez ugyanúgy szükség van a talaj mért '
                 'befogadóképességére és a talajvíz helyzetére, mint az elszivárogtatásnál — '
                 'sőt, itt a talaj oxigénellátása is számít.'],
                'Szivárogtatási vizsgálat', 'szivarogtatasi-vizsgalat',
                alt=('Tisztított víz elhelyezése', 'tisztitott-viz-elhelyezese')),

        sec_faq([
            ('Miért kell nagyobb hely az oldómedencés rendszerhez?',
             'Mert ott a tisztítás jelentős része a talajban történik, nem a berendezésben. '
             'A mező nem elvezet, hanem tisztít — ehhez felület, levegős talajréteg és idő '
             'kell. Az aktív biológiai rendszernél a tisztítás már a berendezésben lezajlik, '
             'ezért a szikkasztó feladata kisebb.'),
            ('Áthelyezhető a tisztítómező, ha kell a hely?',
             'Nem szabadon. A mező helye és mérete technológiai adottság, az elosztó rendszer '
             'pedig hozzá tervezett. Áthelyezése lényegében új mező építése — ezért kell a '
             'helyét a projekt elején, a kerti tervekkel együtt eldönteni.'),
            ('Mi történik, ha a mező betelik?',
             'A tisztítási hatásfok romlik, a víz nehezebben szivárog el, és a felszínen is '
             'jelentkezhet nedvesedés. Az okok között tömörítés, túlterhelés, csapadékvíz '
             'rávezetése és elhanyagolt karbantartás egyaránt lehet. A helyreállítás '
             'jellemzően a mező részleges vagy teljes újraépítése.'),
            ('Lehet fölé kertet telepíteni?',
             'Gyep és sekély gyökérzetű növényzet jellemzően igen. Mély gyökérzetű fa, cserje, '
             'burkolat, tömörítés és járműforgalom nem. Ha kertépítést tervez, azt a rendszer '
             'tervezésekor érdemes jelezni.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 3) Gyökérzónás elhelyezés
# ===========================================================================
def epit_gyokerzona():
    return [
        sec_prose('Mit értünk alatta', 'Először a fogalmat kell tisztázni', [
            'A „gyökérzónás elhelyezés” kifejezés a magyar piacon többféle dolgot takar, '
            'ezért itt pontosan megmondjuk, mire használjuk: <strong>a biológiailag '
            'megtisztított víz felszín alatti elhelyezése növényzettel fedett '
            'területen</strong>, ahol a víz a növények gyökérzónájának mélységébe kerül.',
            'Ez tehát nem felszíni öntözés, nem locsolórendszer, és nem a víz tárolása '
            'későbbi felhasználásra. A felszín alatti kijuttatás lényege éppen az, hogy a '
            'vízzel nincs közvetlen érintkezés.',
        ]),

        sec_prose('Amit nem állítunk', 'Három külön kategória, amit nem szabad összemosni', [
            '<strong>Felszín alatti elhelyezés dísznövényzet területén.</strong> Ez az, '
            'amiről ez az oldal szól. Műszakilag az elszivárogtatás egy változata, azzal a '
            'többlettel, hogy a víz a növényzet számára is hasznosul.',
            '<strong>Beltéri újrahasználat.</strong> WC-öblítés vagy más háztartási '
            'felhasználás további kezelést igényel. A biológiailag tisztított víz erre '
            'önmagában nem alkalmas, és emberi fogyasztásra semmilyen körülmények között '
            'nem az.',
            '<strong>Szabályozott mezőgazdasági víz-újrahasználat.</strong> Ez külön jogi '
            'kategória: az EU 2020/741 rendelet a hatálya alá tartozó újrahasználatra külön '
            'vízminőségi, monitoring- és kockázatkezelési rendszert állít. Nem keverendő '
            'össze a házi kerti felszín alatti elhelyezéssel.',
        ]),

        sec_numbered('Használati korlátok', 'Mire kell figyelni?',
                     'Ezek nem óvatoskodás: a tisztított víz nem ivóvíz minőségű, és a '
                     'felhasználás módja határozza meg a kockázatot.',
                     ['<strong>Felszín alatti kijuttatás.</strong> A cél az, hogy a vízzel '
                      'ne legyen közvetlen érintkezés — sem emberi, sem állati. Felszíni '
                      'kilocsolás, permetezés vagy aeroszolképződés nem cél és nem javasolt.',
                      '<strong>Dísznövényzet, nem élelmiszernövény.</strong> Az ehető '
                      'növények öntözése lényegesen szigorúbb megítélés alá esik, és '
                      'külön szakértői állásfoglalás nélkül nem javasolt.',
                      '<strong>Gyermekek által használt kertrész.</strong> Játszóterület, '
                      'homokozó, medence környéke — itt az elhelyezési pontot érdemes '
                      'távolabb tervezni.',
                      '<strong>Nincs tárolás.</strong> A tisztított víz tárolása a '
                      'vízminőséget rontja és további kockázatot jelent; a rendszer '
                      'folyamatos elhelyezésre készül, nem gyűjtésre.',
                      '<strong>Télen ugyanúgy megy.</strong> A víz télen is keletkezik, '
                      'a növényzet vízigénye viszont nem. A rendszernek a téli időszakot '
                      'is kezelnie kell — ezért ez nem „öntözés”, hanem elhelyezés.',
                      '<strong>Telített talaj.</strong> Csapadékos időszakban a talaj '
                      'befogadóképessége csökken. A méretezésnek ezt is bírnia kell.']),

        hiany('az ÖkoTech gyökérzónás kialakításának pontos műszaki definíciója: '
              'telepítési rajz, keresztmetszet, a vállalt növényzeti felhasználás köre, '
              'a NEM javasolt felhasználások listája, valamint az A.B.Clear kifolyóvíz '
              'aktuális vízminőségi és mikrobiológiai eredményei',
              'ÖkoTech műszaki csapat + akkreditált laborvizsgálat + közegészségügyi '
              'szakértői állásfoglalás. Amíg ezek nincsenek meg, ez az oldal a fogalmat és '
              'a korlátokat írja le, konkrét felhasználási ígéret nélkül'),

        sec_split('Bizonyíték helyett ígéret nincs', 'Mi az, ami valóban meggyőző',
                  'Ez számít bizonyítéknak',
                  ['Megvalósult ÖkoTech-projekt fotóval és metszettel',
                   'A kifolyó víz akkreditált laboreredménye',
                   'A konkrét elhelyezési kialakítás műszaki rajza',
                   'Több éve működő rendszer tapasztalata',
                   'Világosan megfogalmazott használati korlátok'],
                  'Ez nem bizonyíték',
                  ['„Szebb lesz tőle a kert” típusú általános állítás',
                   'Vízminőségi adat nélküli „újrahasznosítható” megfogalmazás',
                   'Más gyártó kommunikációjára hivatkozás',
                   'A mezőgazdasági újrahasználat szabályainak átemelése házi kertre',
                   'Konkrét kialakítás nélküli „gyökérzónás öntözés” kifejezés']),

        sec_cta('Következő lépés', 'Telekspecifikus egyeztetés',
                ['A gyökérzónás kialakítás feltételei telkenként eltérnek: a talaj, a '
                 'talajvíz, a növényzet és a kert használata együtt dönt. Írja meg, mit '
                 'tervez a kertben, és megmondjuk, mi valósítható meg belőle.'],
                'Kapcsolatfelvétel', '../kapcsolat',
                alt=('Tisztított víz elhelyezése', 'tisztitott-viz-elhelyezese')),

        sec_faq([
            ('Iható a tisztított víz?',
             'Nem. Emberi fogyasztásra semmilyen körülmények között nem alkalmas, és erre '
             'kezeléssel sem készítjük elő. A biológiai tisztítás a szennyezőanyag-terhelést '
             'csökkenti, nem ivóvizet állít elő.'),
            ('Locsolhatok vele zöldséget vagy gyümölcsöt?',
             'Élelmiszernövény öntözését külön szakértői állásfoglalás nélkül nem javasoljuk. '
             'Ez lényegesen szigorúbb megítélés alá esik, mint a dísznövényzet, és a '
             'szabályozott mezőgazdasági víz-újrahasználat külön jogi kategória is.'),
            ('Használhatom WC-öblítésre?',
             'További kezelés nélkül nem. A beltéri újrahasználat önálló technológiai kérdés, '
             'saját berendezésekkel és feltételekkel — nem a szennyvíztisztító kimenetének '
             'egyszerű átvezetése.'),
            ('Mi történik télen?',
             'A szennyvíz télen is keletkezik, a növényzet vízigénye viszont minimális. Ezért '
             'a rendszer nem öntözésre, hanem folyamatos elhelyezésre készül: a téli '
             'időszakot is a talajnak kell befogadnia. A méretezésnek ezt is bírnia kell.'),
            ('Ez ugyanaz, mint a nádgyökérzónás tisztítás?',
             'Nem. A nádgyökérzónás rendszer egy önálló tisztítási technológia. Amiről itt szó '
             'van, az a már megtisztított víz elhelyezése növényzettel fedett területen — '
             'a hasonló elnevezés ellenére más funkció.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 4) Magas talajvízi helyzetek
# ===========================================================================
def epit_magas_talajviz():
    return [
        sec_prose('Két külön probléma', 'A tartály és a víz', [
            'Magas talajvíznél két dolgot kell külön megvizsgálni: a tartály biztonságos '
            'földbe helyezését, és a kifolyó tisztított víz elhelyezhetőségét. Ezek nem '
            'ugyanazok, és nem is következnek egymásból.',
            'A tartály kérdése <strong>szerkezeti</strong>: az ÖkoTech magas talajvíznél a '
            'műanyag tartály köré betonmedencés kialakítást alkalmaz, ami megakadályozza a '
            'felúszást. Bizonyos vízállásig ez tehát megoldható.',
            'A víz elhelyezése viszont <strong>befogadási és jogi</strong> kérdés. '
            'A 147/2010. Korm. rendelet magas talajvízállású területen külön feltételekhez '
            'köti az egyedi szennyvíztisztító létesítmény alkalmazását, fokozottan érzékeny '
            'területen pedig a vízbázisvédelmi szabályokhoz. Attól, hogy a tartály '
            'rögzíthető, a szikkasztás még nem lesz megfelelő.',
        ]),

        sec_prose('Melyik vízszint a mértékadó?', 'A szezonális maximum', [
            'A talajvízszint az év során méterekkel változhat. Egy nyár végi mérés a '
            'legkedvezőbb állapotot mutatja, miközben tavasszal vagy hosszabb csapadékos '
            'időszakban a víz jóval magasabban állhat. A döntéshez a <strong>szezonálisan '
            'előforduló legmagasabb jellemző vízállás</strong> a mértékadó.',
            'Ez azt jelenti, hogy egyetlen pillanatnyi mérés ritkán elegendő. Vagy hosszabb '
            'megfigyelés kell, vagy olyan dokumentum, amely a szezonális maximumot is '
            'tartalmazza, vagy szakértői értékelés a helyi rétegviszonyok alapján.',
        ]),

        sec_numbered('Előzetes jelek', 'Mi utalhat magas talajvízre?',
                     'Ezek jelzések, nem bizonyítékok — de mindegyik indokolja a '
                     'vizsgálatot. Érdemes dátummal és fotóval rögzíteni őket.',
                     ['Nedvesedő vagy beázó pince a házban vagy a szomszédban',
                      'Ásott kút alacsony vízszintje a terepszinttől számítva',
                      'Korábbi földmunkánál — alapásás, medence — vízbetörés a gödörbe',
                      'Tavaszi vagy csapadék utáni tartós vízállás a kertben',
                      'Nádas, sásos növényzet a telken vagy a közvetlen környéken',
                      'Környékbeli tapasztalat: kinél és milyen mélyen jött fel a víz']),

        sec_numbered('Az eredmény', 'Négy külön ág — nem automatikus elutasítás', '',
                     ['<strong>Tartályrögzítés szükséges.</strong> A telepítés '
                      'megvalósítható, de szerkezeti megoldással. Ez költség- és '
                      'kivitelezési következménnyel jár.',
                      '<strong>A vízelhelyezés külön vizsgálandó.</strong> A tartály '
                      'kérdése rendezhető, de a szikkasztás megfelelősége nem igazolt. '
                      'Szivárogtatási vizsgálat és a talajvízszint tisztázása következik.',
                      '<strong>Hatósági vagy hidrogeológiai ellenőrzés szükséges.</strong> '
                      'Fokozottan érzékeny terület, vízbázisvédelmi közelség vagy ismeretlen '
                      'rétegviszonyok esetén nem a berendezés szállítója dönt.',
                      '<strong>Más elhelyezési irány kell.</strong> Ha a helyi elhelyezés '
                      'nem támasztható alá, a projekt nem lezárul, hanem más irányt vesz — '
                      'ehhez viszont jogosult tervező kell.']),

        hiany('az ÖkoTech által vállalt maximális talajvízszint standard és betonmedencés '
              'kialakításnál, a betonmedence aktuális műszaki terve, és hogy milyen '
              'vízelhelyezési alternatívák valósultak meg magas talajvizes projekteknél',
              'ÖkoTech műszaki csapat + megvalósult magas talajvizes referenciák. Enélkül a '
              'látogató nem tudja megítélni, az ő esete melyik ágra esik'),

        sec_cta('Következő lépés', 'A vízszint önmagában nem elég',
                ['Magas talajvíznél is a talaj mért befogadóképessége dönti el, mi '
                 'valósítható meg — a kettőt együtt kell megnézni. Ha az adatok hiányoznak '
                 'vagy az eset határhelyzet, érdemes rögtön a szakértői ágat nézni.'],
                'Mikor szükséges szakértő?', 'mikor-szukseges-szakerto',
                alt=('Szivárogtatási vizsgálat', 'szivarogtatasi-vizsgalat')),

        sec_faq([
            ('Magas talajvíznél eleve nem telepíthető rendszer?',
             'Nem így van. A tartály telepítése bizonyos vízállásig szerkezeti megoldással '
             'kezelhető. Amit külön kell vizsgálni, az a tisztított víz elhelyezhetősége — '
             'és ez a nehezebb kérdés, mert a talaj befogadóképessége mellett a terület '
             'besorolása is számít.'),
            ('Felúszhat a tartály?',
             'Magas talajvíznél ez valós kockázat, különösen üres vagy részben töltött '
             'tartálynál. Éppen ezért alkalmazunk ilyenkor betonmedencés vagy más rögzített '
             'kialakítást. Ez tervezési kérdés, nem utólag megoldható.'),
            ('Elég, ha nyáron megnézzük a vízszintet?',
             'Nem. A nyár végi állapot jellemzően a legkedvezőbb, és a tavaszi maximumról '
             'semmit nem mond. Ha csak egy időpontban mérhető, azt dátummal együtt kell '
             'rögzíteni, és a szezonális maximumot más forrásból — dokumentumból, '
             'megfigyelésből vagy szakértőtől — kell megbecsülni.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 5) Szivárogtatási vizsgálat
# ===========================================================================
def epit_vizsgalat():
    return [
        sec_prose('Nem formalitás', 'Ez a méretezés legfontosabb bemenete', [
            'A szivárogtatási vizsgálat nem adminisztratív lépés, hanem a szikkasztó '
            'méretezésének <strong>legfontosabb telekspecifikus bemeneti adata</strong>. '
            'Ez méri közvetlenül azt, amit tudni kell: milyen sebességgel nyeli el a talaj a '
            'vizet a tervezett mélységben.',
            'A talaj megnevezése — homokos, agyagos, kötött — ezt nem helyettesíti. Két '
            'egymás melletti telek ugyanúgy nevezhető homokosnak, miközben a rétegződésük '
            'miatt egészen másképp viselkednek. A vizsgálat éppen ezt a különbséget méri.',
        ]),

        sec_numbered('A vizsgálat', 'Mit kell tudni róla?', '',
                     ['<strong>Hol.</strong> A szikkasztó <em>tervezett helyén</em>, nem a '
                      'telek egy tetszőleges pontján. Ha a hely még nem dőlt el, előbb az '
                      'elrendezést kell tisztázni.',
                      '<strong>Milyen mélységben.</strong> A tervezett elhelyezési '
                      'mélységben. Egy felszín közeli mérés mást mutathat, mint a másfél '
                      'méterrel lejjebb lévő réteg.',
                      '<strong>Mikor.</strong> Lehetőleg olyan időszakban, amikor a talaj '
                      'nem telített csapadéktól — vagy a mérés mellett rögzíteni kell az '
                      'előzményt, mert az eredményt befolyásolja.',
                      '<strong>A talajvízzel együtt.</strong> A szivárgási eredmény jó '
                      'talajvíz nélkül félrevezető: a szezonális maximum a szikkasztó '
                      'szintjéig felérhet, és akkor a mért érték nem érvényes.',
                      '<strong>Dokumentálva.</strong> Egy laikus által kiásott gödörben '
                      'végzett házi próba és egy szakmailag dokumentált mérés nem azonos '
                      'bizonyító erejű. A méretezéshez az utóbbi kell.']),

        sec_prose('Mi lesz az eredményből?', 'Nem osztályzat — bemeneti adat', [
            'A vizsgálat eredményét nem „jó” vagy „rossz” talajként érdemes értelmezni. '
            'Egy szám, amely a napi elhelyezendő vízmennyiséggel együtt megadja a szükséges '
            'szikkasztófelületet — vagy megmutatja, hogy a szükséges felület nem fér el, és '
            'más elhelyezési irányt kell keresni.',
            'Jó eredmény sem elegendő önmagában: a talajvíz, a rendelkezésre álló terület, a '
            'kút közelsége és a terület érzékenységi besorolása ugyanúgy feltétel. '
            'A vizsgálat egy kérdést zár le a több közül — de azt véglegesen.',
        ]),

        sec_split('Mikor érdemes elvégezni', 'Időzítés',
                  'Ekkor van értelme',
                  ['Ha a helyi elszivárogtatás a valószínű irány',
                   'Ha a szikkasztó tervezett helye már körvonalazódott',
                   'Telekvásárlás előtt, ha a szennyvízkezelés kockázati tényező',
                   'Ha korábbi talajadat régi, vagy más pontra vonatkozik',
                   'Mielőtt bárki konkrét szikkasztóméretet ígér'],
                  'Ekkor várjon vele',
                  ['Amíg nem tudni, hová kerül a ház és a berendezés',
                   'Ha a közcsatorna helyzete még nem tisztázott',
                   'Ha a telek vízbázisvédelmi helyzete bizonytalan — előbb az derüljön ki',
                   'Ha a projekt nagyságrendje miatt úgyis mérnöki tervezés következik',
                   'Ha friss, dokumentált mérés áll rendelkezésre ugyanarra a helyre']),

        hiany('az ÖkoTech által elfogadott vizsgálati módszer és protokoll: hány mérési '
              'pont, milyen mélységben, milyen mértékegységben, és milyen mért értékhez '
              'milyen szikkasztó-konfiguráció tartozik',
              'ÖkoTech műszaki csapat — hivatalos mérési és méretezési protokoll. Amíg ez '
              'nincs rögzítve, a látogatónak nem mondható meg, milyen vizsgálati eredményt '
              'fogadunk el, és ez az oldal a célt írja le, nem a módszert'),

        sec_cta('Következő lépés', 'Ha az eredmény nem elég jó',
                ['Gyenge szivárgási eredmény nem a projekt vége. Ilyenkor nagyobb felület, '
                 'más kialakítás vagy más elhelyezési irány jöhet szóba — de a döntéshez '
                 'jellemzően szakértő kell. A következő oldal megmutatja, melyik esetben ki.'],
                'Mikor szükséges szakértő?', 'mikor-szukseges-szakerto',
                alt=('Tisztított víz elhelyezése', 'tisztitott-viz-elhelyezese')),

        sec_faq([
            ('Elvégezhetem magam?',
             'Tájékozódásra végezhet egyszerű próbát — kiásott gödörbe vizet töltve, a '
             'süllyedést mérve —, és ez sokat elárul. A méretezéshez azonban dokumentált, '
             'szakmailag elvégzett mérés kell: a mélység, a víztelítettség, az előzmény és a '
             'mérési mód mind befolyásolja az eredményt.'),
            ('Mennyibe kerül?',
             'Konkrét árat itt nem adunk, mert szolgáltatás, és a helyszíntől és a '
             'vizsgálati mélységtől függ. Ami biztos: lényegesen kevesebb, mint egy '
             'alulméretezett szikkasztó utólagos újraépítése.'),
            ('Van már talajmechanikai szakvéleményem. Az elég?',
             'Sokszor jó kiindulás, de két dolgot ellenőrizni kell: a telek melyik pontjára '
             'és milyen mélységre vonatkozik, és tartalmaz-e vízbefogadó képességre '
             'vonatkozó adatot. Az alapozáshoz készült feltárás nem feltétlenül tartalmaz '
             'szivárgási értéket.'),
            ('Mi van, ha rossz az eredmény?',
             'Az azt jelenti, hogy a helyi elhelyezéshez nagyobb felület kell, vagy más '
             'kialakítás, esetleg más irány. Ez nem elutasítás, hanem információ — és jóval '
             'olcsóbb most megtudni, mint a szikkasztó megépítése után.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 6) Mikor szükséges szakértő?
# ===========================================================================
def epit_szakerto():
    return [
        sec_prose('Két hiba, egyforma áron', 'A fölösleges kör és az elmaradt vizsgálat', [
            'Egy szokásos családi házas teleknél több alapadat távolról is elegendő lehet az '
            'első műszaki irány meghatározásához — ilyenkor a szakértői kör fölösleges '
            'költség és időveszteség.',
            'Vannak viszont helyzetek, amelyekben az online előszűrés nem helyettesítheti a '
            'helyszíni vagy jogosult szakértői vizsgálatot. Ilyenkor a „megoldjuk magunk” '
            'hozzáállás drágább, mint a szakértő — mert a hibát a megépült rendszeren kell '
            'javítani.',
            'Ez az oldal a kettő között húz határt: mikor elég a saját adat, mikor kell '
            'helyszíni felmérés, és mikor olyan szakértő, akit nem mi biztosítunk.',
        ]),

        sec_split('A határ', 'Mikor elég az adat, és mikor nem',
                  'Jellemzően elegendő a távoli előszűrés',
                  ['Szokásos családi házas projekt, kommunális szennyvízzel',
                   'Ismert és dokumentált talaj- és talajvízadat',
                   'Nincs kút a közelben, vagy a helyzete tisztázott',
                   'Nem érzékeny vagy nem fokozottan érzékeny terület',
                   'Bőven elegendő szabad terület',
                   'A csőkilépési szint ismert vagy még tervezhető'],
                  'Itt szakértő kell',
                  ['Ismeretlen vagy csak becsült szezonális talajvízszint',
                   'Nincs mért szivárgási adat, és a helyi elhelyezés a cél',
                   'Kijelölt vízbázisvédelmi terület vagy bizonytalan kúthelyzet',
                   'Fokozottan érzékeny terület',
                   'Nagyon kis vagy erősen beépített telek',
                   'Felszíni befogadóba vezetés terve',
                   'Nagyobb kapacitású, intézményi vagy nem kommunális projekt']),

        sec_numbered('Kihez, mivel', 'Melyik kérdéshez melyik szakértő?',
                     'Nem ugyanaz a kompetencia. A rossz szakértőhöz fordulás ugyanúgy '
                     'időveszteség, mint a szakértő hiánya.',
                     ['<strong>ÖkoTech műszaki felmérő.</strong> Elhelyezés, szintek, '
                      'hozzáférés, a rendszer kialakítása, telekbrief. Azt zárja le, ami '
                      'a berendezés és a telepítés kérdése.',
                      '<strong>Geotechnikus.</strong> Talajmechanika, rétegződés, '
                      'teherbírás, szivárgási vizsgálat. Akkor kell, ha a talaj viselkedése '
                      'a kérdés.',
                      '<strong>Hidrogeológus.</strong> Felszín alatti vizek, áramlási '
                      'viszonyok, vízbázisvédelmi megítélés. Akkor kell, ha a víz útja a '
                      'kérdés — nem a talajé.',
                      '<strong>Jogosult gépész vagy vízépítési tervező.</strong> '
                      'Engedélyezési és kiviteli terv, felszíni befogadó, nagyobb projektek '
                      'méretezése. Ő nyilatkozik arról, ami tervezői felelősség.',
                      '<strong>Akkreditált labor.</strong> Vízminőségi vizsgálat. Nagyobb '
                      'vagy nem kommunális projektnél, illetve kibocsátási követelmény '
                      'esetén elengedhetetlen.',
                      '<strong>Hatóság.</strong> Engedélyezhetőség, vízjogi engedély, '
                      'területi besorolás. Erről senki más nem nyilatkozhat érvényesen.']),

        sec_prose('Amit az ÖkoTech felmérése nem dönt el', 'A saját hatáskör határai', [
            'A helyszíni felmérésünk műszaki szolgáltatás: rögzíti a szinteket, az '
            'elrendezést, a hozzáférést és a látható kockázatokat, és ebből strukturált '
            'telekbrief készül. Ez sok bizonytalanságot lezár.',
            'Amit viszont <strong>nem</strong> dönt el: az engedélyezhetőséget, a '
            'vízbázisvédelmi megítélést, a felszín alatti víz áramlási viszonyait és a '
            'jogosult tervezői felelősségbe tartozó méretezést. Ezekben nem a berendezés '
            'szállítója az illetékes — és aki mást ígér, az olyat vállal, amire nincs '
            'felhatalmazása.',
            'Ezt szándékosan mondjuk ki: a projekt akkor lesz biztonságos, ha mindenki a '
            'saját hatáskörében nyilatkozik.',
        ]),

        sec_numbered('Mit vigyen a szakértőnek?', 'Amivel gyorsabb és olcsóbb',
                     'A szakértői idő drága. Minél több áll rendelkezésre ezekből, annál '
                     'kevesebb kell belőle.',
                     ['Helyszínrajz a házzal, a kúttal, a behajtóval és a tervezett '
                      'rendszerhellyel',
                      'A szennyvízcső kilépési helye és folyásfenék-mélysége',
                      'Ami a talajról és a talajvízről tudható — dokumentummal, dátummal',
                      'Korábbi talajmechanikai szakvélemény, ha van',
                      'A kút adatlapja vagy dokumentációja',
                      'A háztartás létszáma és a tervezett használat módja',
                      'Fotók a telepítés tervezett helyéről és a behajtóról',
                      'A település neve és a helyrajzi szám — a besorolás ellenőrzéséhez']),

        hiany('az ÖkoTech belső eszkalációs szabályrendszere: mikor elég a távoli adat, '
              'mikor kötelező a kiszállás, mikor kérnek geotechnikai vagy hidrogeológiai '
              'vizsgálatot, milyen szakértői partnerekkel dolgoznak, és mit vállalnak az '
              'engedélyezésből',
              'ÖkoTech műszaki és értékesítési vezetés. A publikus tartalom nem előzheti '
              'meg a belső szabályt — enélkül a látogatónak adott ígéret nem tartható'),

        sec_cta('Következő lépés', 'Mondja el, hol tart',
                ['Ha nem világos, melyik ágra esik az Ön projektje, írja meg, amit tud — a '
                 'település nevét, a telek adottságait és a háztartás létszámát. Megmondjuk, '
                 'elég-e a távoli előszűrés, vagy melyik vizsgálat indokolt.'],
                'Kapcsolatfelvétel', '../kapcsolat',
                alt=('Tisztított víz elhelyezése', 'tisztitott-viz-elhelyezese')),

        sec_faq([
            ('Miért nem elég mindig a helyszíni felmérés?',
             'Mert a felmérés műszaki szolgáltatás, nem hatósági eljárás és nem tervezői '
             'nyilatkozat. A szinteket, az elrendezést és a hozzáférést lezárja, de a '
             'vízbázisvédelmi megítélésről vagy az engedélyezhetőségről nem nyilatkozhat.'),
            ('Ki fizeti a szakértői vizsgálatot?',
             'A geotechnikai, hidrogeológiai és tervezői munka önálló szolgáltatás, saját '
             'költséggel. Éppen ezért fontos előre eldönteni, hogy szükséges-e — sok '
             'projektnél nem az, és fölösleges kiadás lenne.'),
            ('Nagyobb projektnél mi változik?',
             'A kapacitás mellett az engedélyezési és üzemeltetési modell is relevánssá '
             'válik, és a vízminőség, a kibocsátási határérték és a laboradat is bekerül a '
             'képbe. Ilyenkor a projekt már tervezői és — befogadóba vezetésnél — vízjogi '
             'szakértelmet igényel.'),
        ]),
        JOGI,
    ]


# ===========================================================================
OLDALAK = [
    dict(file='projekt-elokeszites/tisztitott-viz-elhelyezese.html',
         url='projekt-elokeszites/tisztitott-viz-elhelyezese', img='oldomedence',
         title='Tisztított víz elhelyezése — hová kerül a kilépő vízmennyiség | ÖkoTech Home',
         desc='Elszivárogtatás, tisztítómező, gyökérzónás elhelyezés — mi a különbség, mitől '
              'függ, és miért az ajánlatadás előfeltétele, nem utólagos kiegészítő.',
         h1='Tisztított víz elhelyezése',
         alt='Kavicságyba fektetett szikkasztóelemek egy frissen kiásott árokban, mögötte '
             'zöld kert',
         lead='A berendezés kiválasztásával a feladat fele van kész. A napi kilépő '
              'vízmennyiség nem tűnik el: valahol el kell helyezni — és ez a nehezebb '
              'kérdés.',
         crumbs=CRUMB, sections=epit_hub()),

    dict(file='projekt-elokeszites/elszivarogtatas.html',
         url='projekt-elokeszites/elszivarogtatas', img='biologiai',
         title='Elszivárogtatás — a tisztított víz elhelyezése a talajban | ÖkoTech Home',
         desc='A leggyakoribb helyi megoldás. Mitől függ a szikkasztó mérete, mi okoz '
              'visszaduzzadást, és miért nem lehet a maradék helyhez méretezni.',
         h1='Elszivárogtatás',
         alt='Talajmetszet: a berendezésből kilépő cső elosztóhoz vezet, alatta kavicságyas '
             'szikkasztó réteg',
         lead='A biológiai tisztítás már megtörtént a berendezésben — a szikkasztó feladata '
              'a kilépő víz elhelyezése. A méretezés a napi vízmennyiségen és a talaj MÉRT '
              'befogadóképességén múlik.',
         crumbs=HUB, sections=epit_elszivarogtatas()),

    dict(file='projekt-elokeszites/tisztitomezo.html',
         url='projekt-elokeszites/tisztitomezo', img='nyaralo',
         title='Tisztítómező — miért a technológia része | ÖkoTech Home',
         desc='Oldómedencés rendszernél a talajban kialakított mező nem elvezetés, hanem '
              'tisztítás. Ezért nagyobb a területigénye, és nem helyezhető át szabadon.',
         h1='Tisztítómező',
         alt='Rétegzett talajmetszet oldómedencével és a mögötte húzódó, elosztócsövekkel '
             'ellátott tisztítómezővel',
         lead='A leggyakoribb félreértés: a tisztítómező nem ugyanaz, mint a biológiai '
              'rendszer utáni szikkasztó. Itt a talaj nemcsak befogad, hanem tisztít is.',
         crumbs=HUB, sections=epit_tisztitomezo()),

    dict(file='projekt-elokeszites/gyokerzonas-elhelyezes.html',
         url='projekt-elokeszites/gyokerzonas-elhelyezes', img='csaladi-haz',
         title='Gyökérzónás elhelyezés — mit jelent, és mit nem | ÖkoTech Home',
         desc='Felszín alatti elhelyezés növényzeti területen. Pontos fogalom, világos '
              'használati korlátok, és miért külön kategória a mezőgazdasági újrahasználat.',
         h1='Gyökérzónás elhelyezés',
         alt='Gondozott kert dísznövényekkel, a gyep alatt húzódó felszín alatti '
             'elhelyezőrendszer jelölt nyomvonalával',
         lead='A kifejezés a piacon többfélét takar, ezért itt pontosan megmondjuk, mire '
              'használjuk — és mire nem. A használati korlátok éppolyan fontosak, mint a '
              'lehetőség.',
         crumbs=HUB, sections=epit_gyokerzona()),

    dict(file='projekt-elokeszites/magas-talajvizi-helyzetek.html',
         url='projekt-elokeszites/magas-talajvizi-helyzetek', img='kozcsatorna',
         title='Magas talajvízi helyzetek — tartály és vízelhelyezés | ÖkoTech Home',
         desc='A tartály rögzíthető, a szikkasztás ettől még nem lesz megfelelő. Melyik '
              'vízszint a mértékadó, mik az előzetes jelek, és mikor kell szakértő.',
         h1='Magas talajvízi helyzetek',
         alt='Munkagödör magas talajvízzel: a gödör alján összegyűlt víz, körülötte nedves '
             'talajréteg',
         lead='Magas talajvíz nem automatikus elutasítás. Két külön kérdésre bomlik — és '
              'az egyikre jellemzően van szerkezeti megoldás, a másikra nem következik '
              'belőle semmi.',
         crumbs=HUB, sections=epit_magas_talajviz()),

    dict(file='projekt-elokeszites/szivarogtatasi-vizsgalat.html',
         url='projekt-elokeszites/szivarogtatasi-vizsgalat', img='telekvasarlas',
         title='Szivárogtatási vizsgálat — a méretezés bemeneti adata | ÖkoTech Home',
         desc='Mit mér, hol és milyen mélységben, mikor érdemes elvégezni, és mi következik '
              'gyenge eredményből. Nem formalitás — a szikkasztó mérete ezen múlik.',
         h1='Szivárogtatási vizsgálat',
         alt='Vizsgálati gödör a telken, benne mérőléc és vízszintjelölés a szivárgás '
             'méréséhez',
         lead='Ez méri közvetlenül azt, amit a méretezéshez tudni kell: milyen sebességgel '
              'nyeli el a talaj a vizet a tervezett mélységben. A talaj megnevezése ezt nem '
              'helyettesíti.',
         crumbs=HUB, sections=epit_vizsgalat()),

    dict(file='projekt-elokeszites/mikor-szukseges-szakerto.html',
         url='projekt-elokeszites/mikor-szukseges-szakerto', img='vallalkozas',
         title='Mikor szükséges szakértő? — a hatáskörök határai | ÖkoTech Home',
         desc='Mikor elég a saját adat, mikor kell helyszíni felmérés, és melyik kérdéshez '
              'melyik szakértő. Amit az ÖkoTech felmérése nem dönt el.',
         h1='Mikor szükséges szakértő?',
         alt='Két szakember műszaki rajz fölött egyeztet egy építési terület szélén',
         lead='Két hiba kerül ugyanannyiba: a fölösleges szakértői kör és az elmaradt '
              'vizsgálat. Ez az oldal a kettő között húz határt.',
         crumbs=HUB, sections=epit_szakerto()),
]

if __name__ == '__main__':
    (WEB / 'projekt-elokeszites').mkdir(exist_ok=True)
    for o in OLDALAK:
        out = WEB / o['file']
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:60s} {len(out.read_text(encoding='utf-8'))//1024} KB")
