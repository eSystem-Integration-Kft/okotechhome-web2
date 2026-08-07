#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Megoldások → Biológiai szennyvíztisztítás — hub, hét aloldal, és alatta az
A.B.Clear termékcsalád alhub a saját hét aloldalával.

A LEGFONTOSABB SZERKEZETI VÁLTOZÁS: a „biológiai szennyvíztisztítás" és az
„A.B.Clear" eddig ugyanazon az oldalon keveredett. Itt szétválik:
a biológiai oldal TECHNOLÓGIATÍPUS, az A.B.Clear TERMÉKCSALÁD. A látogató előbb
eldönti, hogy aktív biológiai technológia való-e neki, és csak utána azt, hogy
az ÖkoTech melyik terméke megfelelő.

A brief NÉGY állítást kifejezetten pontosít:

1. „Zéró szippantás" — a jelenlegi termékoldal abszolút módon fogalmaz. Az
   iszapzsák valós differenciáló előny, de normál üzemeltetési feltételekhez,
   zsákkezeléshez és iszapellenőrzéshez kötött. Feltételekkel együtt kimondva
   az állítás nem gyengül, hanem bizonyíthatóvá válik.

2. „Minimális karbantartás" — a használati utasítás ellenőrzési, naplózási,
   levegőztetési, iszap-, kompresszor- és karbantartási feladatokat ír elő.
   Ezért valós feladatmodellt mutatunk, nem ígéretet.

3. A dokumentumrendszer szétszórt: CE/EN 12566-3, VITUKI-vizsgálat, szabadalom
   és engedélypéldák külön-külön említve, verziózott bizonyítéktár nélkül.

4. A modell- és kapacitásarchitektúra nincs egységesítve: a GYIK A.B.Clear 6,
   8 és 10–50 csoportokat említ, a termékoldal „1–50 főig" kommunikál.

ÁR AZ EGÉSZ ÁGON NEM JELENIK MEG. A régi webhely 2014-es árai történeti
tartalmak, több mint egy évtizede elavultak — nem újrahasznosíthatók.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import (sec_numbered, sec_split, sec_prose, sec_situations,
                    sec_cta, sec_faq)

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

JOGI = ('<!-- JOGI ÉS MŰSZAKI ELLENŐRZÉS PUBLIKÁLÁS ELŐTT. Érintett: EN 12566-3 aktuális\n'
        '     változata · CE/teljesítménynyilatkozat · 28/2004. KvVM rendelet és a\n'
        '     kifolyóvízre vonatkozó vízminőségi előírások · 147/2010. Korm. rendelet.\n'
        '     A jogszabályi megfelelőségi kijelentés NEM időtlen terméktulajdonság:\n'
        '     mindig az aktuális rendeletszöveghez kell igazítani. -->')


def hiany(mi, honnan):
    return (f'<!-- ADATHIÁNY: {mi}\n'
            f'     Forrás: {honnan}. Addig konkrét értékkel nem publikálható. -->')


HOME = ('Főoldal', '../')
MEG = ('Megoldások', './')
CRUMB = [HOME, MEG]
HUB = [HOME, MEG, ('Biológiai szennyvíztisztítás', 'biologiai-szennyviztisztitas')]
ABC = HUB + [('A.B.Clear termékcsalád', 'ab-clear')]


# ===========================================================================
# HUB — Biológiai szennyvíztisztítás
# ===========================================================================
def epit_hub():
    return [
        sec_prose('Mit jelent', 'Élő folyamat, nem szűrés', [
            'Az aktív biológiai szennyvíztisztítás lényege, hogy a háztartási szennyvíz '
            'szerves szennyezőanyagait <strong>mikroorganizmusok bontják le</strong> — '
            'ugyanaz a folyamat, ami a nagy szennyvíztisztító telepeken zajlik, csak egyetlen '
            'ingatlan léptékében. Ehhez a baktériumoknak oxigénre van szükségük, amit '
            'levegőztetéssel juttatunk a rendszerbe.',
            'Ez alapvetően más, mint a zárt tároló, amely csak gyűjt, és más, mint az '
            'oldómedence, ahol a tisztítás jelentős része a talajban folytatódik. Itt a '
            'tisztítás túlnyomó része <strong>a berendezésen belül</strong> megtörténik.',
            'A rendszernek két kimenete van: a tisztított víz, amelyet el kell helyezni, és '
            'a fölösiszap, amelyet kezelni kell. A második az, amiről a legkevesebb szó '
            'esik — pedig a hosszú távú működés ezen is múlik.',
        ]),

        sec_prose('Amit ez az oldal nem állít', 'Nem minden csatorna nélküli ingatlanhoz való', [
            'A biológiai rendszer sok helyzetben jó választás, de nem automatikusan '
            'megfelelő minden közcsatorna nélküli ingatlanhoz. Számít a használat '
            'rendszeressége, a terhelés, a telek, a talajvíz, a tisztított víz '
            'elhelyezhetősége — és az is, hogy a tulajdonos vállalja-e az előírt '
            'ellenőrzési feladatokat.',
            'Ez utóbbi a leggyakrabban elhallgatott feltétel. A berendezés önműködő, de nem '
            'felügyelet nélküli: rendszeres ellenőrzést, karbantartást és iszappróbát '
            'igényel. Ha ez nem vállalható, a technológia nem fog jól működni — függetlenül '
            'attól, hogy fizikailag elfér-e a telken.',
            'Ezért ezen az oldalon nemcsak azt mutatjuk meg, kinek való, hanem azt is, '
            'kinek nem.',
        ]),

        sec_situations('A szakasz oldalai', 'Mit érdemes megnézni?',
                       'A sorrend a döntés logikáját követi: előbb a technológia megértése, '
                       'aztán az alkalmasság, végül a hosszú távú vállalhatóság és a '
                       'bizonyíték.',
                       [
                           ('nav-mukodes', 'Hogyan működik?',
                            'Lépésről lépésre: mi történik a szennyvízzel a befolyástól a '
                            'tisztított víz kifolyásáig, és mi az az eleveniszap.',
                            'biologiai-hogyan-mukodik', 'Működés'),
                           ('nav-biologiai', 'Kinek megfelelő?',
                            'Nem épülettípus, hanem használati és műszaki helyzet szerint — '
                            'mikor működik jól egy aktív biológiai rendszer.',
                            'biologiai-kinek-megfelelo', 'Kinek megfelelő'),
                           ('nav-alternativak', 'Mikor nem megfelelő?',
                            'Feltételes és abszolút kizárás. Ahol más technológia '
                            'célszerűbb — és ezt előre jobb tudni.',
                            'biologiai-mikor-nem-megfelelo', 'Mikor nem'),
                           ('nav-talaj', 'Telek- és terhelési feltételek',
                            'A technológiai alkalmasságból projektalkalmasság: terhelés, '
                            'telek, csőszint, vízelhelyezés, villamos előkészítés.',
                            'biologiai-telek-es-terhelesi-feltetelek', 'Feltételek'),
                           ('nav-szerviz', 'Üzemeltetés és karbantartás',
                            'Mit ellenőriz a tulajdonos, milyen gyakran, és mi tartozik '
                            'szervizhez. Valós feladatlista, nem ígéret.',
                            'biologiai-uzemeltetes-es-karbantartas', 'Üzemeltetés'),
                           ('nav-koltseg', 'Költségtényezők',
                            'Mi határozza meg a teljes projekt és a többéves működés '
                            'költségét. Konkrét ár nincs — tényezők vannak.',
                            'biologiai-koltsegtenyezok', 'Költségtényezők'),
                           ('nav-esettanulmany', 'Kapcsolódó esettanulmányok',
                            'Működő példák helyzet szerint: családi ház, emésztőkiváltás, '
                            'nehezebb telek, közösségi projekt.',
                            'biologiai-esettanulmanyok', 'Esettanulmányok'),
                       ]),

        sec_split('Három megoldástípus', 'Miben más a biológiai rendszer',
                  'Aktív biológiai rendszer',
                  ['A tisztítás túlnyomó része a BERENDEZÉSBEN történik',
                   'Levegőztetés, tehát villamos energia kell hozzá',
                   'Folyamatos vagy rendszeres használatot igényel',
                   'A kilépő víz minősége mérhető és dokumentálható',
                   'Rendszeres ellenőrzés és iszapkezelés tartozik hozzá',
                   'A tisztított vizet ezután el kell helyezni'],
                  'Zárt tároló és oldómedence',
                  ['Zárt tároló: csak gyűjt, nem tisztít — rendszeres szippantás',
                   'Oldómedence: anaerob előkezelés, a tisztítás a TALAJBAN folytatódik',
                   'Oldómedencéhez nem kell villamos energia',
                   'Oldómedence nagyobb területet igényel a tisztítómező miatt',
                   'Hosszú kihagyást jobban tűr — szezonális ingatlanhoz releváns',
                   'A kilépő víz minősége nehezebben dokumentálható']),

        sec_numbered('Amit a rendszer nem tűr', 'Mit nem szabad beleengedni?',
                     'Az eleveniszap élő baktériumtömeg. Ami elpusztítja vagy megbénítja, '
                     'az a tisztítást állítja le — és a helyreállítás hetekbe telhet.',
                     ['<strong>Baktériumölő és erős vegyszerek.</strong> Fertőtlenítők, '
                      'klóros szerek, savas lefolyótisztítók nagyobb mennyiségben.',
                      '<strong>Gyógyszermaradék nagyobb mennyiségben.</strong> '
                      'Különösen antibiotikum — ez a rendeltetése szerint is baktériumölő.',
                      '<strong>Zsír és olaj nagy mennyiségben.</strong> Sütőolaj a '
                      'lefolyóba: a felszínen filmréteget képez, és rontja az oxigénbevitelt.',
                      '<strong>Nem lebomló szilárd anyag.</strong> Nedves törlőkendő, '
                      'higiéniai termék, macskaalom — ezek nem bomlanak le, hanem '
                      'felhalmozódnak.',
                      '<strong>Festék, oldószer, üzemanyag.</strong> Ezek nem háztartási '
                      'szennyvizek, és a biológiát tartósan károsítják.',
                      '<strong>Csapadékvíz.</strong> Nem mérgező, de felhígítja a '
                      'szennyvizet és hidraulikusan túlterheli a rendszert.']),

        sec_cta('Következő lépés', 'Először értsük meg, mi történik',
                ['A működés megértése után minden további kérdés — a karbantartás, a '
                 'vegyszerérzékenység, az alul- és túlterhelés — magától értetődővé válik. '
                 'Néhány perc, és utána a döntés is könnyebb.'],
                'Hogyan működik?', 'biologiai-hogyan-mukodik',
                alt=('A.B.Clear termékcsalád', 'ab-clear')),

        sec_faq([
            ('Mennyivel jobb ez, mint az oldómedence?',
             'Nem „jobb”, hanem más. Az aktív biológiai rendszer kisebb helyen, mérhetően '
             'jobb kilépővíz-minőséget ad, cserébe villamos energiát és rendszeres '
             'ellenőrzést igényel, és a folyamatos használatot szereti. Az oldómedence '
             'ezekben elnézőbb, de nagyobb területet kér. A választás a használati '
             'profilon múlik.'),
            ('Szagol?',
             'Rendeltetésszerű működésnél nem. A szag jellemzően valamilyen üzemzavar '
             'jelzése: elégtelen levegőztetés, túlterhelés vagy a biológia sérülése. '
             'Éppen ezért fontos a rendszeres ellenőrzés — a szag nem elviselendő '
             'velejáró, hanem tünet.'),
            ('Mennyi áramot fogyaszt?',
             'Konkrét fogyasztási adatot itt nem közlünk, mert modellenként eltér, és a '
             'nyilvános anyagainkban nincs egységesen dokumentálva. A levegőztetés '
             'folyamatos működést igényel, tehát ez az energiafogyasztás állandó tétel — '
             'a költségtényezők oldal ezt kezeli.'),
            ('Mi történik áramkimaradáskor?',
             'Rövid kimaradást a rendszer átvészel: a baktériumközösség nem pusztul el '
             'azonnal. Tartós áramhiánynál a levegőztetés hiánya miatt a biológia romlik. '
             'Ha az ingatlanon az áramellátás bizonytalan, azt a technológiaválasztásnál '
             'előre kell jelezni.'),
            ('Kell hozzá engedély?',
             'Ez projekt- és helyszínfüggő, és az eljárási szabályok időről időre '
             'változnak. Ezért itt nem adunk általános választ — a projekt-előkészítés '
             'szakasz foglalkozik vele, mindig aktuális forrásra hivatkozva.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 1) Hogyan működik?
# ===========================================================================
def epit_mukodes():
    return [
        sec_numbered('A folyamat', 'Mi történik a szennyvízzel?',
                     'A házból érkező szennyvíz útja a befolyástól a kifolyásig. '
                     'A pontos kamraszám és elrendezés modellenként eltérhet.',
                     ['<strong>Beérkezés és mechanikai előkezelés.</strong> A szennyvíz '
                      'gravitációsan érkezik. Az első térben a durvább szilárd rész '
                      'leülepszik, és megkezdődik a bontás.',
                      '<strong>Levegőztetett tér — itt történik a tisztítás.</strong> '
                      'Membrános légbefúvó finom buborékokat juttat a vízbe. Az oxigénhez '
                      'jutó baktériumok — az eleveniszap — lebontják a szerves anyagot.',
                      '<strong>Ülepítés.</strong> A levegőztetés után a víz megnyugszik, és '
                      'az iszap leülepszik. A tetején tiszta víz marad, alul a sűrűbb '
                      'iszapréteg.',
                      '<strong>Iszapvisszavezetés.</strong> Az ülepedett iszap egy része '
                      'visszakerül a levegőztetett térbe: ez tartja fenn a '
                      'baktériumközösséget.',
                      '<strong>Fölösiszap elvezetése.</strong> A baktériumok szaporodnak, '
                      'tehát folyamatosan keletkezik többlet. Ha ezt nem vezetjük el, a '
                      'rendszer eliszaposodik. Ez a kezelés az A.B.Clear egyik '
                      'megkülönböztető eleme.',
                      '<strong>Tisztított víz kifolyása.</strong> A megtisztított víz '
                      'elhagyja a berendezést — és innentől a vízelhelyezés kérdése '
                      'következik, ami önálló téma.']),

        sec_prose('Az eleveniszap', 'Amiből minden más következik', [
            'Az „eleveniszap” nem szennyeződés, hanem <strong>élő baktériumtömeg</strong> — '
            'ez végzi a tisztítást. Ha ezt az egy fogalmat megérti, minden más magától '
            'adódik.',
            'Miért kell <strong>levegőztetés</strong>? Mert ezek a baktériumok oxigénnel '
            'dolgoznak. Miért <strong>vegyszerérzékeny</strong> a rendszer? Mert a '
            'fertőtlenítőszer megöli őket. Miért baj a <strong>tartós alulterhelés</strong>? '
            'Mert éheznek. Miért baj a <strong>túlterhelés</strong>? Mert nem győzik. '
            'És miért kell az <strong>iszapkezelés</strong>? Mert szaporodnak, és a '
            'többletet el kell vezetni.',
            'Az eleveniszap állapota ezért nem műszaki kuriózum, hanem a rendszer '
            'egészségének mérőszáma — ezt méri az ülepedési (iszap-) próba, amit az '
            'üzemeltetés részeként rendszeresen el kell végezni.',
        ]),

        sec_split('Két kimenet', 'Amit sokan nem tudnak',
                  'Tisztított víz',
                  ['Nagyjából annyi, amennyi szennyvíz beérkezett',
                   'Minősége mérhető: KOI, BOI5, lebegőanyag, nitrogén, foszfor',
                   'Nem ivóvíz, és további kezelés nélkül nem is lesz az',
                   'El kell helyezni — ez önálló tervezési feladat',
                   'A vízelhelyezés a projekt előfeltétele, nem kiegészítője'],
                  'Fölösiszap',
                  ['A baktériumok szaporodásából keletkezik, folyamatosan',
                   'Ha nem vezetjük el, a rendszer eliszaposodik',
                   'Hagyományosan ezt szippantással távolítják el',
                   'Az A.B.Clear iszapzsákos megoldást használ erre',
                   'Ez nem szünteti meg a feladatot — más modellt ad rá']),

        sec_prose('Automatika nem egyenlő felügyelet nélküli működés', '', [
            'A berendezés vezérlése önműködő: a levegőztetési ciklusokat, az iszap '
            'visszavezetését és a fázisváltásokat automatika kezeli. Ettől viszont a '
            'rendszer még nem működik magától a végtelenségig.',
            'A használati utasítás rendszeres feladatokat ír elő: a levegőztetés '
            'ellenőrzését, az eleveniszap állapotának vizsgálatát, a kompresszor '
            'ellenőrzését, üzemeltetési napló vezetését és időszakos karbantartást. '
            'Ezek nem opcionálisak, és nem szerviz-feladatok — jelentős részük a '
            'tulajdonosé.',
            'Ezt vásárlás előtt érdemes tudni, nem utána. Az üzemeltetés oldalán tételesen '
            'végigvesszük, mi az, ami valóban a tulajdonos dolga.',
        ]),

        hiany('az aktualizált technológiai metszet és folyamatábra, a kamratérfogatok, a '
              'levegőztetési ciklusok, a termékmodellek közötti folyamatkülönbségek és az '
              'aktuális vezérlőlogika',
              'ÖkoTech műszaki dokumentáció. A nyilvános használati utasítás V4_2019.02.27. '
              'verziójú — publikálás előtt ellenőrizni kell, van-e újabb, és hogy minden '
              'értékesített modellre az vonatkozik-e'),

        sec_cta('Következő lépés', 'Illik ez az Ön használatához?',
                ['A technológia megértése után a következő kérdés az, hogy a saját '
                 'használati helyzete illeszkedik-e hozzá. Ez nem épülettípus kérdése, '
                 'hanem a használat rendszerességéé és a szennyvíz jellegéé.'],
                'Kinek megfelelő?', 'biologiai-kinek-megfelelo',
                alt=('A.B.Clear műszaki adatok', 'ab-clear-muszaki-adatok')),

        sec_faq([
            ('Mennyi idő, míg beindul a tisztítás?',
             'A baktériumközösség kialakulása időt vesz igénybe — a beüzemelés után nem az '
             'első naptól éri el a rendszer a szokásos kilépővíz-minőséget. A pontos '
             'időtartam a terheléstől és a hőmérséklettől függ, ezért ezt a beüzemelési '
             'dokumentáció rögzíti.'),
            ('Mi az az iszappróba?',
             'Egy egyszerű ülepedési vizsgálat: mérőhengerbe vett mintában megnézzük, '
             'mennyi idő alatt és milyen arányban ülepszik le az iszap. Ez mutatja meg az '
             'eleveniszap állapotát — tulajdonosi feladat, és néhány perc.'),
            ('Télen is működik?',
             'Igen. A berendezés a talajban van, ami hőmérsékleti szempontból kedvező, és '
             'a biológiai folyamat hőt is termel. A hidegebb időszakban a folyamat lassul, '
             'de nem áll le — feltéve, hogy a terhelés folyamatos.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 2) Kinek megfelelő?
# ===========================================================================
def epit_kinek():
    return [
        sec_prose('Nem épülettípus', 'A használati helyzet dönt', [
            'A biológiai rendszer alkalmassága nem abból következik, hogy családi házról, '
            'tanyáról vagy panzióról van szó, hanem abból, <em>hogyan használják</em> az '
            'ingatlant. Ugyanaz az épülettípus lehet ideális és lehet rossz választás is.',
            'Az alaphelyzet: <strong>folyamatosan vagy rendszeresen használt ingatlan, '
            'döntően kommunális jellegű szennyvízzel</strong>, ahol rendelkezésre áll '
            'villamos energia, megoldható a tisztított víz elhelyezése, és a tulajdonos '
            'vállalja az előírt ellenőrzési feladatokat.',
            'Ez négy feltétel, és mind a négynek teljesülnie kell.',
        ]),

        sec_numbered('A négy feltétel', 'Mikor működik jól?', '',
                     ['<strong>Rendszeres használat.</strong> A baktériumközösség '
                      'folyamatos tápanyagutánpótlást igényel. Az állandó lakhatás ideális; '
                      'a rendszeres hétvégi használat kezelhető; a több hónapos kihagyás '
                      'külön eljárást igényel.',
                      '<strong>Kommunális jellegű szennyvíz.</strong> Konyha, fürdőszoba, '
                      'WC, mosás. Ha technológiai, ipari vagy nagykonyhai szennyvíz is '
                      'érkezik, az külön vizsgálatot igényel — nem automatikusan kizárás, '
                      'de nem is automatikusan rendben.',
                      '<strong>Villamos energia.</strong> A levegőztetés folyamatos '
                      'működést igényel. Ha az ingatlanon nincs tartósan biztosítható '
                      'áramellátás, az aktív rendszer nem jó kiindulópont.',
                      '<strong>Megoldható vízelhelyezés.</strong> A napi kilépő '
                      'vízmennyiségnek helye kell legyen. Ez a telek és a talajviszonyok '
                      'kérdése — és gyakran ez a szűk keresztmetszet, nem a berendezés.']),

        sec_split('Tipikus helyzetek', 'Hol működik jól, és hol kell külön megnézni',
                  'Jellemzően jó választás',
                  ['Állandóan lakott családi ház közcsatorna nélkül',
                   'Tanya, ahol van villamos energia és megoldható a vízelhelyezés',
                   'Meglévő emésztő kiváltása állandó lakhatás mellett',
                   'Egész évben üzemelő panzió vagy kisebb szálláshely',
                   'Iroda, üzem szociális blokkja — kommunális szennyvízzel',
                   'Rendszeresen, minden hétvégén használt hétvégi ház'],
                  'Itt külön vizsgálat kell',
                  ['Csak nyáron használt nyaraló, hosszú téli kihagyással',
                   'Étterem vagy nagykonyha — a konyhai terhelés külön kérdés',
                   'Bizonytalan vagy időszakos áramellátás',
                   'Nem megoldott tisztítottvíz-elhelyezés',
                   'Erősen ingadozó, kiszámíthatatlan terhelés',
                   'Nem kommunális, technológiai eredetű szennyvíz']),

        sec_prose('A szezonális használat nem igen-nem kérdés', '', [
            'A nyaraló nem egyszerűen „alkalmas” vagy „nem alkalmas” kategória. A rövidebb '
            'vagy rendszeres távollét kezelhető — a vezérlés alulterheléses üzemmódot '
            'támogathat, és a baktériumközösség fennmarad.',
            'A több hónapos, teljes kihagyás viszont már külön üzemeltetési vagy leállítási '
            'eljárást igényel. Ez tervezett folyamat, nem „kikapcsoljuk és jövőre '
            'visszajövünk”.',
            'Ha a használat erősen szakaszos, a kérdés már nem a kapacitás, hanem a '
            'technológiaválasztás: ilyenkor a passzív, oldómedencés rendszer relevánsabb '
            'lehet. Ezt a szezonális használat oldalán részletesen végigvesszük.',
        ]),

        hiany('ügyfélszegmensenkénti telepítési szám, alkalmazási és kizárási mátrix, a '
              'szezonális használat pontos szabályai, valamint hol húzódik a B2B-standard '
              'és a mérnöki projekt közötti határ',
              'ÖkoTech értékesítés és műszaki csapat. A jelenlegi „kiknek ajánljuk" '
              'felsorolás széles — családi ház, tanya, panzió, motel, iroda, társasház —, '
              'de ezek nem azonos mélységű műszaki feltételekkel kezelhetők'),

        sec_cta('Következő lépés', 'Nézzük meg a másik oldalról is',
                ['Ha idáig minden illett, érdemes megnézni a kizárásokat is. Az őszinte '
                 '„ez nem Önnek való” több pénzt takarít meg, mint a rosszul megválasztott '
                 'rendszer bármilyen kedvezménye.'],
                'Mikor nem megfelelő?', 'biologiai-mikor-nem-megfelelo',
                alt=('Telek- és terhelési feltételek',
                     'biologiai-telek-es-terhelesi-feltetelek')),

        sec_faq([
            ('Hétvégi házba jó?',
             'Rendszeres hétvégi használatnál igen, ha van tartós áramellátás és a vezérlés '
             'támogatja az alulterheléses üzemet. Ha a használat ennél szakaszosabb — '
             'hosszú, több hónapos szünetekkel —, érdemes a passzív rendszert is '
             'megvizsgálni.'),
            ('Panzióhoz megfelelő?',
             'Egész évben üzemelő szálláshelyhez jellemzően igen. A méretezés viszont nem a '
             'férőhelyből indul, hanem a kihasználtságból, és ha van saját étterem, a '
             'konyhai terhelés külön kérdés — előkezelést igényelhet.'),
            ('Mi van, ha ritkán vagyunk otthon?',
             'Az alkalmi néhány napos távollét nem probléma. A rendszeres, hosszabb '
             'távollét már üzemmódkérdés, a több hónapos pedig külön leállítási eljárást '
             'igényel. Adja meg a leghosszabb várható távollétet — abból derül ki, mi a '
             'teendő.'),
            ('Két háztartás közösen használhatja?',
             'Műszakilag megoldható, de tisztázni kell a terhelést, a bekötés kialakítását '
             'és azt, hogy ki felel az üzemeltetésért. A közös használat nem műszaki, hanem '
             'jellemzően felelősségi kérdésen szokott elakadni.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 3) Mikor nem megfelelő?
# ===========================================================================
def epit_mikor_nem():
    return [
        sec_prose('Miért van ez az oldal', 'A nem is válasz', [
            'A rosszul megválasztott rendszer nem olcsóbb — csak később derül ki, mennyibe '
            'kerül. Ezért itt összeszedjük azokat a helyzeteket, amelyekben az aktív '
            'biológiai rendszer nem jó kiindulópont, vagy csak külön feltételekkel az.',
            'Két kategóriát külön kezelünk: ami a <strong>technológia</strong> általános '
            'korlátja, és ami az <strong>A.B.Clear</strong> konkrét termékhatára. A kettő '
            'nem ugyanaz, és a következmény sem.',
        ]),

        sec_split('Két súlyosság', 'Nem minden kizárás végleges',
                  'Abszolút — más technológia kell',
                  ['Nincs tartósan biztosítható villamos energia',
                   'Hosszú, több hónapos teljes kihagyás megfelelő eljárás nélkül',
                   'Nem kommunális jellegű szennyvíz előzetes vizsgálat nélkül',
                   'Az ingatlanon rendszeresen erős vegyszerterhelés éri a rendszert',
                   'A tulajdonos nem vállalja a rendszeres ellenőrzést'],
                  'Feltételes — vizsgálat vagy külön kialakítás',
                  ['Nem megoldott tisztítottvíz-elhelyezés — a telek dönt, nem a technológia',
                   'Magas talajvíz — szerkezeti megoldással kezelhető lehet',
                   'Nagykonyhai vagy jelentős zsírterhelés — előkezelés kell',
                   'Erősen ingadozó terhelés — üzemmód és méretezés kérdése',
                   'Kicsi vagy nehezen megközelíthető telek — elrendezés kérdése']),

        sec_numbered('A leggyakoribb okok', 'Mi buktatja el a projektet?',
                     'Tapasztalatunk szerint ezek okozzák a legtöbb utólagos csalódást — '
                     'és mindegyik előre kideríthető lett volna.',
                     ['<strong>Nem megoldott vízelhelyezés.</strong> Ez nem a technológiát '
                      'zárja ki, hanem a projektet állítja meg. A tartály elfér — a napi '
                      'kilépő vízmennyiségnek viszont nincs hová mennie.',
                      '<strong>Rosszul meghatározott kapacitás.</strong> A rendszer nem lesz '
                      'megfelelő attól, hogy fizikailag elfér. Tartós túlterhelésnél a '
                      'kilépő víz minősége romlik, tartós alulterhelésnél a biológia '
                      'gyengül.',
                      '<strong>Vegyszerterhelés.</strong> Ahol rendszeresen erős '
                      'fertőtlenítőt vagy klóros szert használnak — például bizonyos '
                      'üzemi vagy egészségügyi környezetben —, ott a biológia nem tud '
                      'stabilan működni.',
                      '<strong>Nem vállalt üzemeltetés.</strong> Ha a rendszeres ellenőrzés '
                      'és az iszapkezelés nem történik meg, a rendszer fokozatosan romlik. '
                      'Ez nem azonnali meghibásodás, ezért gyakran későn derül ki.',
                      '<strong>Áramellátás hiánya vagy bizonytalansága.</strong> '
                      'A levegőztetés folyamatos működést igényel. Tartós áramhiány esetén '
                      'a biológia leépül.',
                      '<strong>Jogi vagy területi korlátozás.</strong> Nem a berendezés a '
                      'kérdés, hanem az, hogy az adott helyen a tisztított víz elhelyezése '
                      'megengedett-e. Ez hatósági kérdés.']),

        sec_prose('Mikor mit érdemes megnézni helyette', '', [
            'Ha a probléma a <strong>hosszú kihagyás</strong> vagy a hiányzó áramellátás, '
            'az oldómedencés rendszer jöhet szóba: passzív működésű, nem igényel '
            'villamos energiát, és a szakaszos használatot jobban tűri. Cserébe nagyobb '
            'területet kér, mert a tisztítás jelentős része a talajban folyik.',
            'Ha a probléma a <strong>vízelhelyezés</strong>, akkor a technológiaváltás '
            'önmagában nem segít — az oldómedence még nagyobb felületet igényel. Ilyenkor '
            'a zárt tároló vagy más elhelyezési irány vizsgálata következik.',
            'Ha a szennyvíz <strong>nem kommunális jellegű</strong>, akkor nem termékválasztás, '
            'hanem mérnöki feladat következik: mintavétel, laborvizsgálat és '
            'megvalósíthatósági vizsgálat.',
        ]),

        hiany('a tényleges elutasítási okok, a műszaki hard-stop lista, az ügyfélszolgálati '
              'hibák leggyakoribb okai, valamint a nem megfelelő használatból eredő '
              'garanciális és szervizesetek',
              'ÖkoTech szerviz és értékesítés. Ez az oldal akkor lesz igazán hiteles, ha a '
              'valós elutasítási okok is szerepelnek benne — nem csak az elméletiek'),

        sec_cta('Következő lépés', 'Ha nem ez az irány',
                ['A megoldástípusok összevetése oldalon egymás mellett látja a három '
                 'lehetőséget, ugyanazon szempontok szerint. Ha bizonytalan, ott érdemes '
                 'folytatni.'],
                'Megoldástípusok összehasonlítása', 'megoldastipusok-osszehasonlitasa',
                alt=('Kizáró és korlátozó feltételek', 'kizaro-es-korlatozo-feltetelek')),

        sec_faq([
            ('Nyaralóba tényleg nem való?',
             'Nem ilyen egyszerű. A rendszeresen — például minden hétvégén — használt '
             'ingatlan kezelhető. A csak nyáron használt, télen több hónapra elhagyott '
             'ingatlan viszont külön leállítási eljárást igényel, és ott érdemes a passzív '
             'rendszert is megvizsgálni.'),
            ('Használhatok egyáltalán tisztítószert?',
             'Igen, a szokásos háztartási mennyiségben. Amit kerülni kell: a nagy '
             'mennyiségű klóros és erősen fertőtlenítő szer, a savas lefolyótisztító és a '
             'sütőolaj lefolyóba öntése. Ez nem szigorúbb, mint amit a legtöbb háztartás '
             'egyébként is meg tud tenni.'),
            ('Ha most nem megfelelő, később lehet az?',
             'Igen, több feltételes eset megoldható. A vízelhelyezés kialakítható, az '
             'áramellátás kiépíthető, a nagykonyhai terhelés előkezeléssel kezelhető. '
             'Ezért különítjük el a feltételes és az abszolút kizárást — a kettő nem '
             'ugyanaz.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 4) Telek- és terhelési feltételek
# ===========================================================================
def epit_feltetelek():
    return [
        sec_prose('Két kérdés, egy oldal', 'Technológiai alkalmasságból projektalkalmasság', [
            'Az előző oldalak arról szóltak, hogy a technológia illik-e a használatához. '
            'Ez az oldal arról, hogy a <strong>konkrét projektje</strong> megvalósítható-e: '
            'megfelelő-e a terhelés, és telepíthető-e a rendszer az adott telken.',
            'A kettő nem választható szét, mert egymásra hatnak: nagyobb terhelés nagyobb '
            'berendezést és nagyobb szikkasztófelületet igényel, a szűk telek pedig éppen '
            'ezt korlátozza.',
        ]),

        sec_numbered('Terhelési oldal', 'Mit kell tudni a használatról?', '',
                     ['<strong>Állandó létszám.</strong> Hányan laknak vagy tartózkodnak '
                      'rendszeresen az ingatlanban.',
                      '<strong>Tényleges vízfogyasztás.</strong> Meglévő ingatlannál a '
                      'vízszámláról — ez pontosabb, mint a létszám.',
                      '<strong>Csúcsterhelés.</strong> Mekkora, milyen hosszú és milyen '
                      'gyakori. A rendszeres hétvégi többlet más, mint az évi kétszeri '
                      'ünnep.',
                      '<strong>Távollét.</strong> A leghosszabb várható időszak, amikor a '
                      'rendszer nem kap terhelést.',
                      '<strong>Tervezett bővítés.</strong> Ha két-három éven belül nő a '
                      'létszám, azt most kell figyelembe venni.']),

        sec_numbered('Telepítési oldal', 'Mit kell tudni a telekről?',
                     'A tartály helye és a tisztított víz elhelyezése KÉT külön kérdés — '
                     'nem kezelhető egyetlen „elfér-e?” kérdéssel.',
                     ['<strong>Talaj és mért szivárgóképesség.</strong> Ez határozza meg, '
                      'hogy a tisztított víz helyben elhelyezhető-e, és mekkora felületen.',
                      '<strong>Talajvíz.</strong> A szezonális maximum. Hat a tartály '
                      'rögzítésére és külön a szikkasztásra.',
                      '<strong>Szabad terület.</strong> Ami a ház, a kút, a behajtó és a '
                      'közművek után marad — a szervizhozzáféréssel együtt.',
                      '<strong>A szennyvízcső kilépési mélysége.</strong> Ez határozza meg, '
                      'milyen szintre kerülhet a berendezés befolyója, és hogy kell-e '
                      'magasító vagy átemelő.',
                      '<strong>Villamos előkészítés.</strong> A berendezéshez kiépített, '
                      'megfelelően védett elektromos csatlakozás kell.',
                      '<strong>Járműterhelés és hozzáférés.</strong> A tartály fölött '
                      'külön kialakítás nélkül nem vezethető gépjárműforgalom, és a '
                      'rendszernek később is hozzáférhetőnek kell maradnia.']),

        hiany('az A.B.Clear modellek aktuális befolyási szintjei és a megengedett '
              'magasítás. A jelenlegi nyilvános anyagok ELTÉRŐ értékeket tartalmaznak: a '
              'GYIK az A.B.Clear 6 és 8 modellnél 51 cm befolyási szintet, magasítás '
              'nélkül legfeljebb 46 cm vezetékmélységet és legfeljebb 35 cm magasítóelemet '
              'ír le, a megrendelőlap viszont 30 cm feletti magasítást nevez meg '
              'működésképtelennek. A 10–50-es modellekről nincs nyilvános adat',
              'ÖkoTech műszaki csapat — modellenkénti adatlap. Amíg a két érték nincs '
              'összehangolva, egyik sem publikálható tervezési szabályként'),

        sec_split('Mi módosít, és mi állít meg', 'Nem minden akadály egyforma',
                  'Csak a kialakítást módosítja',
                  ['Magas talajvíz — rögzített vagy betonmedencés kialakítás',
                   'Mély csőkilépés — magasító vagy átemelő akna',
                   'Járműterhelés — külön méretezett betonakna',
                   'Gyengébb szivárgás — nagyobb szikkasztófelület',
                   'Ezek költséget és kivitelezési időt jelentenek, nem kizárást'],
                  'Megállíthatja a projektet',
                  ['A szükséges szikkasztófelület nem fér el a szabad területen',
                   'A terület besorolása nem engedi a talajba juttatást',
                   'Kijelölt vízbázisvédelmi terület érintettsége',
                   'Nem biztosítható villamos energia',
                   'Ezekben nem a berendezés szállítója dönt']),

        sec_cta('Következő lépés', 'A telket külön is végigvesszük',
                ['A projekt-előkészítés szakasz részletesen foglalkozik a telekadottságokkal '
                 'és a terheléssel — ott találja az előszűrőket és az adatgyűjtési '
                 'útmutatókat is.'],
                'Telekalkalmasság', '../projekt-elokeszites/telekalkalmassag',
                alt=('Terhelés és kapacitás', '../projekt-elokeszites/terheles-es-kapacitas')),

        sec_faq([
            ('Milyen mélyen kell lennie a szennyvízcsőnek?',
             'Erre most nem adunk számot, mert a nyilvános anyagainkban két különböző érték '
             'szerepel a megengedett magasításra, és a nagyobb modellekről nincs publikus '
             'adat. Amíg ez nincs összehangolva, a konkrét projektnél egyeztetve mondjuk '
             'meg — így nem téved, aki a weboldalra hagyatkozik.'),
            ('Mi van, ha túl mély a cső?',
             'Ilyenkor magasító elem vagy átemelő akna jöhet szóba. Mindkettő megoldás, de '
             'költség- és üzemeltetési következménnyel: az átemelő beruházási költséget, '
             'áramfogyasztást és egy további karbantartandó gépészeti elemet jelent.'),
            ('Kell hozzá külön elektromos kiépítés?',
             'Igen, a berendezéshez megfelelően védett elektromos csatlakozás szükséges. '
             'Ennek kiépítése jellemzően a kivitelezés része — érdemes a projekt elején '
             'tisztázni, ki végzi.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 5) Üzemeltetés és karbantartás
# ===========================================================================
def epit_uzemeltetes():
    return [
        sec_prose('Amit vásárlás előtt tudni kell', '„Minimális karbantartás” — mit jelent?', [
            'A biológiai rendszerről gyakran hangzik el, hogy „minimális karbantartást” '
            'igényel. Ez igaz abban az értelemben, hogy a napi működés önműködő — de nem '
            'jelenti azt, hogy nincs teendő.',
            'A használati és karbantartási utasítás konkrét, rendszeres feladatokat ír elő: '
            'ellenőrzést, üzemeltetési napló vezetését, a levegőztetés és az eleveniszap '
            'állapotának vizsgálatát, a kompresszor ellenőrzését és időszakos '
            'karbantartást. Ezek jelentős része <strong>tulajdonosi feladat</strong>.',
            'Ezt vásárlás előtt érdemes átgondolni. Nem sok idő — de rendszeresség kell '
            'hozzá, és aki ezt nem vállalja, annak a technológia nem fog jól működni.',
        ]),

        sec_split('Ki mit csinál', 'Felelősségi megosztás',
                  'A tulajdonos feladata',
                  ['Rendszeres szemrevételezés — működik-e a levegőztetés',
                   'Az eleveniszap ülepedési vizsgálata',
                   'Az iszapzsák állapotának ellenőrzése és kezelése',
                   'Üzemeltetési napló vezetése',
                   'A megengedett és kerülendő anyagok betartása',
                   'Hibajelzés esetén a szerviz értesítése'],
                  'A szerviz feladata',
                  ['Időszakos szakszerviz és átvizsgálás',
                   'Kompresszor és membrán karbantartása, cseréje',
                   'Vezérlés ellenőrzése, beállítása',
                   'A tulajdonos által el nem hárítható hibák javítása',
                   'Beüzemelés, újraindítás hosszú leállás után',
                   'Alkatrészcsere']),

        sec_numbered('Amit a tulajdonos ellenőriz', 'A rendszeres feladatok',
                     'A gyakoriságokat szándékosan nem számszerűsítjük itt — lásd alább, '
                     'miért. A konkrét ütemezést a berendezés aktuális használati '
                     'utasítása rögzíti.',
                     ['<strong>Levegőztetés.</strong> Működik-e a kompresszor, van-e '
                      'buborékolás a levegőztetett térben. Ez a legfontosabb egyetlen jel: '
                      'ha nincs levegőztetés, a biológia leáll.',
                      '<strong>Eleveniszap-állapot.</strong> Ülepedési vizsgálat '
                      'mérőhengerrel: mennyi idő alatt és milyen arányban ülepszik az '
                      'iszap. Ez mutatja a rendszer egészségét.',
                      '<strong>Iszapzsák.</strong> Állapot, telítettség, kezelés. Ez az '
                      'A.B.Clear iszapkezelési modelljének tulajdonosi része.',
                      '<strong>Általános állapot.</strong> Szag, a fedlap zárása, a '
                      'víztükör felszíne, szokatlan hang a kompresszor felől.',
                      '<strong>Üzemeltetési napló.</strong> Mikor mit ellenőrzött, mit '
                      'tapasztalt. Nem bürokrácia: hiba esetén ebből derül ki, mióta '
                      'tart a jelenség.']),

        hiany('a rendszeres feladatok PONTOS gyakorisága. A jelenlegi összehasonlító oldal '
              'heti ránézést és nagyjából háromhavonta ülepedési vizsgálatot említ, de ezt '
              'a legfrissebb használati utasítással kell összehangolni — a nyilvános '
              'változat V4_2019.02.27. verziójú',
              'ÖkoTech műszaki csapat: aktuális használati utasítás + szervizjegyek '
              'alapján a valós alkatrészcsere-gyakoriság, a tipikus tulajdonosi hibák és '
              'az éves karbantartási időráfordítás'),

        sec_split('Anyagok', 'Mi mehet a lefolyóba, és mi nem',
                  'Szokásos háztartási mennyiségben rendben',
                  ['Mosogatószer, mosószer, öblítő',
                   'Szappan, tusfürdő, sampon',
                   'WC-papír',
                   'Konyhai ételmaradék kis mennyiségben',
                   'Szokásos tisztítószerek mértékkel'],
                  'Kerülendő vagy tiltott',
                  ['Klóros és erősen fertőtlenítő szerek nagyobb mennyiségben',
                   'Savas lefolyótisztító',
                   'Sütőolaj és nagy mennyiségű zsír',
                   'Nedves törlőkendő, higiéniai termék, macskaalom',
                   'Festék, oldószer, üzemanyag, vegyszer',
                   'Gyógyszermaradék nagyobb mennyiségben — különösen antibiotikum',
                   'Csapadékvíz rávezetése']),

        sec_prose('Rendkívüli helyzetek', 'Áramkimaradás, távollét, hibajelzés', [
            '<strong>Áramkimaradás.</strong> Rövid kimaradást a rendszer átvészel. Tartós '
            'áramhiánynál a levegőztetés hiánya miatt a biológia romlik — hosszabb '
            'kimaradás után érdemes megfigyelni a rendszer viselkedését.',
            '<strong>Távollét.</strong> Rövidebb távollét esetén a rendszer üzemben marad. '
            'Több hónapos kihagyásnál külön eljárás szükséges. A pontos időhatárokat a '
            'berendezés aktuális dokumentációja rögzíti.',
            '<strong>Hibajelzés.</strong> Ha a vezérlés hibát jelez, vagy szokatlan szag, '
            'hang vagy víztükör-változás észlelhető, az szervizhívást indokol. Ezek nem '
            'tulajdonosi javítási feladatok.',
        ]),

        sec_cta('Következő lépés', 'És mibe kerül mindez?',
                ['Az üzemeltetésnek költségvonzata is van: energia, alkatrész, szerviz, '
                 'fogyóeszköz. A költségtényezők oldal ezeket veszi végig — konkrét ár '
                 'nélkül, de tételesen.'],
                'Költségtényezők', 'biologiai-koltsegtenyezok',
                alt=('Iszapzsákos technológia', 'ab-clear-iszapzsakos-technologia')),

        sec_faq([
            ('Mennyi időt vesz igénybe havonta?',
             'A rendszeres szemrevételezés néhány perc, az ülepedési vizsgálat is rövid. '
             'Konkrét éves időráfordítást most nem közlünk, mert nincs egységesen '
             'dokumentálva — de a nagyságrend a rendszeres, nem az időigényes kategóriába '
             'esik. Ami számít, az a rendszeresség.'),
            ('Mi történik, ha elmulasztom az ellenőrzést?',
             'Nem azonnal romlik el semmi — és éppen ez a veszélye. A biológia állapota '
             'fokozatosan romlik, a kilépő víz minősége csökken, és mire látható jel '
             'jelentkezik, a helyreállítás már hosszabb folyamat. Ezért fontos az '
             'üzemeltetési napló.'),
            ('Kell hozzá szerződéses karbantartás?',
             'A rendszeres szakszerviz erősen javasolt, és a garanciális feltételek is '
             'kapcsolódhatnak hozzá. A pontos feltételeket a konkrét vásárláskor '
             'egyeztetjük, mert ezek termék- és szerződésfüggők.'),
            ('Tényleg nem kell szippantani?',
             'Az iszapzsákos megoldás normál üzemeltetés mellett kiváltja a rendszeres '
             'szippantást — de ez nem azt jelenti, hogy nincs teendő az iszappal. '
             'A zsák kezelése tulajdonosi feladat, és rendkívüli helyzetben lehet szükség '
             'egyéb beavatkozásra. Az iszapzsákos oldal ezt részletesen leírja.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 6) Költségtényezők
# ===========================================================================
def epit_koltseg():
    return [
        sec_prose('Amit ez az oldal ad', 'Tényezők, nem ár', [
            'Konkrét árat ezen az oldalon nem talál — és ez szándékos. A projekt költségét '
            'nem a berendezés listaára határozza meg, hanem a telepített rendszer egésze és '
            'a többéves működés. Ugyanaz a berendezés két telken jelentősen eltérő '
            'összköltséggel valósul meg.',
            'Amit adunk helyette: a <strong>költségstruktúra</strong>. Ha tudja, mely '
            'tételekből áll össze egy projekt, két ajánlatot is össze tud hasonlítani — '
            'és látni fogja, ha valamelyikből hiányzik egy tétel.',
            'Ez utóbbi a gyakoribb probléma: nem a magas ár, hanem a hiányos ajánlat.',
        ]),

        sec_numbered('Beruházási költség', 'Miből áll össze a telepített rendszer?',
                     'Ezek nem mind szerepelnek minden ajánlatban — érdemes tételesen '
                     'végigkérdezni.',
                     ['<strong>A berendezés.</strong> Maga a tartály a gépészettel és a '
                      'vezérléssel.',
                      '<strong>Szállítás.</strong> Külön tétel lehet, vagy a megrendelő '
                      'saját szállítással is megoldhatja.',
                      '<strong>Földmunka.</strong> A munkagödör kiemelése, a föld '
                      'elhelyezése vagy elszállítása, visszatöltés. Talajtól és mélységtől '
                      'függően jelentősen eltér.',
                      '<strong>Csővezeték.</strong> A háztól a berendezésig, majd a '
                      'berendezéstől a vízelhelyezésig.',
                      '<strong>Magasító vagy átemelő.</strong> Ha a csőkilépés mélysége '
                      'indokolja. Az átemelő üzemeltetési költséget is jelent.',
                      '<strong>Tisztítottvíz-elhelyezés.</strong> A szikkasztó vagy más '
                      'kialakítás — mérete a talaj mért szivárgóképességétől függ. '
                      'Ez gyakran a legnagyobb egyedi szórású tétel.',
                      '<strong>Villamos kiállás.</strong> A védett elektromos csatlakozás '
                      'kiépítése.',
                      '<strong>Szerelés és üzembe helyezés.</strong> Külön szolgáltatási '
                      'elem lehet — saját kivitelezővel vagy az ÖkoTech kivitelezésében.']),

        sec_numbered('Működési költség', 'Mi jelentkezik évről évre?', '',
                     ['<strong>Villamos energia.</strong> A levegőztetés folyamatos '
                      'működést igényel, tehát ez állandó tétel.',
                      '<strong>Karbantartás és szerviz.</strong> Időszakos szakszerviz, '
                      'átvizsgálás.',
                      '<strong>Fogyóeszköz.</strong> Iszapzsák és egyéb cserélendő elem.',
                      '<strong>Kopóalkatrész.</strong> Kompresszormembrán és más, idővel '
                      'cserélendő alkatrész.',
                      '<strong>Eseti javítás.</strong> Ami a rendszeres karbantartáson '
                      'kívül merül fel.']),

        sec_prose('Amit érdemes összevetni', 'Beruházás és életciklus', [
            'A legolcsóbb beruházás nem feltétlenül a legolcsóbb megoldás tíz év alatt. '
            'A zárt tároló beruházási költsége alacsonyabb, de a rendszeres szippantás '
            'folyamatos, jelentős kiadás. A biológiai rendszer beruházása magasabb, de az '
            'üzemeltetése más szerkezetű.',
            'Ezért érdemes a két számot külön nézni: mennyibe kerül megvalósítani, és '
            'mennyibe kerül működtetni. A megtérülés kérdésére csak konkrét adatokkal '
            'lehet felelősen válaszolni — a jelenlegi szippantási gyakorisággal és '
            'költséggel, a helyi árakkal.',
            'A „zéró szippantás” előny valós, de akkor válik pénzügyi érvvé, ha mellé tesszük '
            'a megmaradó tulajdonosi feladatokat és a fogyóeszköz-költséget is.',
        ]),

        hiany('a jelenlegi projektajánlatok tipikus tételszerkezete, a valós '
              'energiafogyasztás modellenként, a karbantartási költség nagyságrendje, az '
              'alkatrészcsere-gyakoriság és az iszapzsák tényleges cseregyakorisága',
              'ÖkoTech értékesítés és szerviz. Minden költséginput GYORSAN AVUL — legalább '
              'negyedéves belső frissítési rend javasolt, mielőtt bármilyen ársáv '
              'nyilvánosságra kerül'),

        sec_prose('A régi árakról', 'Amit nem használunk fel', [
            'A korábbi webhelyen szerepeltek konkrét A.B.Clear árak. Ezek <strong>2014-es '
            'akciós adatok</strong>, több mint egy évtizede elavultak, és semmilyen formában '
            'nem vihetők át erre a webhelyre.',
            'Az ÖkoTech jelenlegi döntése szerint konkrét termékár nem kerül publikálásra. '
            'Az ajánlat a konkrét projekt adataiból áll össze — modell, telek, csőmélység, '
            'vízelhelyezés, kivitelezési terjedelem és kiegészítők —, és ezek nélkül egy '
            'közölt szám inkább félrevezetne.',
        ]),

        sec_cta('Következő lépés', 'Ajánlatkérési készültség',
                ['Ha a telek és a terhelés kérdései tisztázottak, az ajánlat is '
                 'megalapozott lesz. Ha még nem, előbb azokat érdemes végigvenni — így nem '
                 'kap olyan ajánlatot, amit később módosítani kell.'],
                'Telek- és terhelési feltételek', 'biologiai-telek-es-terhelesi-feltetelek',
                alt=('Terhelés és kapacitás',
                     '../projekt-elokeszites/terheles-es-kapacitas')),

        sec_faq([
            ('Miért nem írják ki az árat?',
             'Mert a berendezés ára a projekt egészének csak egy része, és önmagában '
             'félrevezető lenne. A földmunka, a vízelhelyezés kialakítása és a kivitelezési '
             'terjedelem telkenként jelentősen eltér — két azonos berendezésű projekt '
             'összköltsége is különbözhet.'),
            ('Mennyi idő alatt térül meg az emésztőhöz képest?',
             'Ez a jelenlegi szippantási gyakoriságtól, a helyi szippantási díjaktól és a '
             'projekt költségétől függ. Általános megtérülési időt felelősen nem lehet '
             'mondani — a konkrét adataival viszont kiszámolható.'),
            ('Mit érdemes megkérdezni egy ajánlatnál?',
             'Hogy melyik tétel szerepel benne a fenti listából, és melyik nem. '
             'A leggyakoribb eltérés a földmunka, a tisztítottvíz-elhelyezés és az '
             'üzembe helyezés körül van — ha ezek hiányoznak, az ajánlat nem '
             'összehasonlítható.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 7) Kapcsolódó esettanulmányok
# ===========================================================================
def epit_esettanulmanyok():
    return [
        sec_prose('Mit bizonyít egy referencia', 'És mit nem', [
            'Egy telepítéskori fotó azt bizonyítja, hogy a berendezés a földbe került. '
            'A hosszú távú működést nem. Ezért az esettanulmányoknál azt keressük, ami '
            'ténylegesen bizonyít: <strong>működési idő, karbantartási történet, '
            'iszapkezelési tapasztalat és — ahol van — laboreredmény</strong>.',
            'A referencia akkor hasznos, ha a saját helyzetéhez hasonló. Egy 128 berendezéses '
            'községi projekt más problémát old meg, mint egy magas talajvizű telken álló '
            'családi ház. Ezért érdemes helyzet szerint keresni, nem méret szerint.',
        ]),

        sec_situations('Működő projektek', 'Hasonló helyzetek',
                       'Az ÖkoTech dokumentált projektjei közül azok, amelyek a biológiai '
                       'technológia alkalmazhatóságát mutatják eltérő helyzetekben.',
                       [
                           ('nav-kozossegi', 'Csikvánd — 128 berendezés',
                            'Egész községet lefedő, egyedi berendezésekre épülő megoldás. '
                            'Azt mutatja, hogy a technológia nemcsak egyedi ingatlanon '
                            'működik.',
                            '../eredmenyek/csikvand', 'Csikvánd'),
                           ('nav-kozossegi', 'Diósberény — 90 berendezés',
                            'Hasonló léptékű települési projekt. A telepítések számánál '
                            'fontosabb, hogy évek óta üzemelnek.',
                            '../eredmenyek/diosbereny', 'Diósberény'),
                           ('nav-kozossegi', 'Bakonypéterd — központi telep',
                            'Négy összekapcsolt 50 fős berendezésből kialakított központi '
                            'telep. Azt mutatja, hol van a határ egyedi és telepi megoldás '
                            'között.',
                            '../eredmenyek/bakonypeterd', 'Bakonypéterd'),
                           ('nav-esettanulmany', 'Óbudavár — a kezdet',
                            'A legrégebbi dokumentált projektek egyike. Az évek óta tartó '
                            'működés önmagában is bizonyíték.',
                            '../eredmenyek/obudavar', 'Óbudavár'),
                       ]),

        sec_numbered('Amit minden esethez tudni érdemes', 'A hasznos esettanulmány adatai',
                     'Ezek nélkül a referencia illusztráció, nem bizonyíték. Ahol az adat '
                     'nálunk sincs meg, ott ezt jelezzük.',
                     ['Kiinduló probléma — mit kellett megoldani',
                      'A használat jellege és a terhelés',
                      'A telek adottságai: talaj, talajvíz, szabad terület',
                      'A választott rendszer és — ahol releváns — a modell',
                      'Hogyan oldották meg a tisztított víz elhelyezését',
                      'A telepítés éve és az azóta eltelt működési idő',
                      'Karbantartási és szerviztörténet',
                      'Rendelkezésre álló laboreredmény vagy mérés',
                      'Mit bizonyít az eset — és mit nem']),

        hiany('a strukturált esetlapok adattartalma: CRM- és projektarchívum, telepítési és '
              'beüzemelési jegyzőkönyvek, laboreredmények, szerviztörténet, '
              'ügyfélhozzájárulások és fotók',
              'ÖkoTech projektarchívum. A jelenlegi referenciák erősek, de a döntéshez '
              'szükséges műszaki adatok — terhelés, telek, vízelhelyezés, működési idő — '
              'nincsenek mellettük'),

        sec_prose('Amit a díj és a telepítésszám bizonyít', '', [
            'A Construma Nagydíj és az összesített telepítésszám vállalati bizalmi elem: azt '
            'mutatják, hogy a cég régóta és széles körben jelen van a piacon.',
            'Amit <strong>nem</strong> bizonyítanak: hogy az Ön helyzetében is működni fog. '
            'Ahhoz azonos helyzetű projekt kell — hasonló terheléssel, hasonló telekkel és '
            'hasonló vízelhelyezéssel. Ezért nem díjakkal érvelünk, hanem projektekkel.',
        ]),

        sec_cta('Következő lépés', 'Ha a technológia rendben van',
                ['Ha idáig minden illett a helyzetére, a következő kérdés az, hogy az '
                 'ÖkoTech saját megoldása miben más — és melyik modell tartozik az Ön '
                 'projektjéhez.'],
                'A.B.Clear termékcsalád', 'ab-clear',
                alt=('Bakonypéterd — központi telep', '../eredmenyek/bakonypeterd')),

        sec_faq([
            ('Van a saját helyzetemhez hasonló referencia?',
             'Írja meg, mi a helyzete — állandó lakhatás, emésztőkiváltás, nehezebb telek, '
             'szálláshely —, és megnézzük, van-e dokumentált, hasonló projektünk. Ha nincs, '
             'azt is megmondjuk.'),
            ('Beszélhetek egy meglévő ügyféllel?',
             'Ez az ügyfél hozzájárulásán múlik, de több esetben megoldható. Kérdezze meg — '
             'a működő rendszer tulajdonosa jellemzően többet tud mondani a mindennapokról, '
             'mint bármelyik adatlap.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# ALHUB — A.B.Clear termékcsalád
# ===========================================================================
def epit_abc_hub():
    return [
        sec_prose('Itt már a termékről van szó', 'Technológia és termék', [
            'Az eddigi oldalak arról szóltak, mi az aktív biológiai szennyvíztisztítás, és '
            'kinek való. Ez az oldal arról szól, hogy az <strong>ÖkoTech saját '
            'megoldása</strong> miben áll, és mely projekthez mely modell tartozik.',
            'A megkülönböztetés azért fontos, mert a két döntés különböző. Előbb el kell '
            'dönteni, hogy aktív biológiai technológia való-e Önnek — és csak utána azt, '
            'hogy melyik gyártó melyik terméke.',
        ]),

        sec_numbered('Miben más az A.B.Clear', 'Három állítás, három bizonyíték',
                     'Mindegyik mellé odatesszük, mi támasztja alá — és hol hiányzik még '
                     'a dokumentáció.',
                     ['<strong>Iszapzsákos iszapkezelés.</strong> Ez a legerősebb '
                      'termékspecifikus különbség: saját fejlesztés, szabadalmi oltalommal '
                      'és 2014-es Construma Nagydíjjal. Nem „karbantartás nélküli” '
                      'megoldás, hanem <em>eltérő iszapkezelési modell</em> — a részleteket '
                      'külön oldalon írjuk le.',
                      '<strong>CE-jelölés és EN 12566-3 megfelelőség.</strong> A berendezések '
                      'megfelelnek a vonatkozó szabványnak, akkreditált vizsgálat alapján. '
                      'A dokumentumok elérhetőségén dolgozunk — a cél, hogy minden állítás '
                      'mellett ott legyen az eredeti irat.',
                      '<strong>Magyar fejlesztés és gyártás.</strong> Ez a szerviz és az '
                      'alkatrészellátás szempontjából számít a leginkább: a pótalkatrész '
                      'nem külföldi szállítmányra vár.']),

        sec_situations('A termékcsalád oldalai', 'Mit szeretne megnézni?', '',
                       [
                           ('nav-attekintes', 'Termékcsalád áttekintése',
                            'Hogyan tagolódik a család kapacitás és alkalmazási helyzet '
                            'szerint, és hol vannak a határok.',
                            'ab-clear-termekcsalad-attekintese', 'Áttekintés'),
                           ('nav-terheles', 'Modellek és kapacitások',
                            'Névleges LE, hidraulikai kapacitás, alkalmazási tartomány — '
                            'egységes adatstruktúrában.',
                            'ab-clear-modellek-es-kapacitasok', 'Modellek'),
                           ('nav-biologiai', 'Műszaki adatok',
                            'A termékcsalád egyetlen hivatalos webes műszaki forráspontja. '
                            'Kifolyóvíz-jellemzők a vizsgálati háttérrel együtt.',
                            'ab-clear-muszaki-adatok', 'Műszaki adatok'),
                           ('nav-mukodes', 'Iszapzsákos technológia',
                            'Mi a fölösiszap, hogyan kezeli az iszapzsák, mi marad '
                            'tulajdonosi feladatnak — és mit jelent pontosan a „zéró '
                            'szippantás”.',
                            'ab-clear-iszapzsakos-technologia', 'Iszapzsák'),
                           ('nav-telepites', 'Telepítési feltételek',
                            'Csőszintek, talajvíz, rögzítés, villamos előkészítés, '
                            'hozzáférés — és hogy melyik munkát ki végzi.',
                            'ab-clear-telepitesi-feltetelek', 'Telepítés'),
                           ('nav-tanusitvany', 'Dokumentumok és tanúsítványok',
                            'Teljesítménynyilatkozat, használati utasítás, vizsgálati '
                            'jegyzőkönyv, szabadalom — verzióval és dátummal.',
                            'ab-clear-dokumentumok', 'Dokumentumok'),
                           ('nav-bizonyitek', 'Kapcsolódó referenciák',
                            'Kizárólag A.B.Clear berendezéssel működő projektek — modellel, '
                            'kapacitással és működési idővel.',
                            'ab-clear-referenciak', 'Referenciák'),
                       ]),

        hiany('a piacvezetői állítás alátámasztása. A webhely több különböző történeti '
              'telepítésszámot tartalmaz, és a „legtöbb telepítés Magyarországon" típusú '
              'állításhoz aktuális szám és összehasonlítási alap kell',
              'ÖkoTech értékesítés — aktuális, dátumozott telepítésszám. Enélkül ez az '
              'állítás nem kerülhet a webhelyre'),

        sec_cta('Következő lépés', 'Melyik modell tartozik Önhöz?',
                ['A modellválasztás nem pusztán személyszám kérdése: a valós fogyasztás, a '
                 'csúcsterhelés és a telekadatok is részei a döntésnek. Az áttekintés '
                 'megmutatja a család felépítését.'],
                'Termékcsalád áttekintése', 'ab-clear-termekcsalad-attekintese',
                alt=('Vissza: Biológiai szennyvíztisztítás', 'biologiai-szennyviztisztitas')),

        sec_faq([
            ('Mennyibe kerül egy A.B.Clear?',
             'Konkrét termékárat nem publikálunk. Az ajánlat a projekt adataiból áll össze — '
             'modell, telek, csőmélység, vízelhelyezés, kivitelezési terjedelem és '
             'kiegészítők —, és ezek nélkül egy közölt szám félrevezetne. A '
             'költségtényezők oldal megmutatja, miből áll össze.'),
            ('Tényleg nem kell szippantani?',
             'Az iszapzsákos megoldás normál üzemeltetés mellett kiváltja a rendszeres '
             'szippantást. Ez nem azt jelenti, hogy nincs teendő az iszappal: a zsák '
             'kezelése tulajdonosi feladat. Az iszapzsákos oldal pontosan leírja, mi a '
             'feltétele és mi marad a tulajdonosnál.'),
            ('Kapok hozzá dokumentációt?',
             'Igen: teljesítménynyilatkozat, használati és karbantartási utasítás, '
             'telepítési útmutató és műszaki adatlap tartozik a termékhez. Ezek '
             'elérhetőségén dolgozunk a webhelyen is, hogy vásárlás előtt is '
             'megnézhetők legyenek.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# A.B.Clear 1) Termékcsalád áttekintése
# ===========================================================================
def epit_abc_attekintes():
    return [
        sec_prose('A család felépítése', 'Nem egyetlen termék', [
            'Az A.B.Clear nem egyetlen berendezés, hanem termékcsalád. A jelenlegi '
            'kommunikáció „1–50 főig” egységes kategóriaként kezeli, a részletes '
            'tájékoztatás viszont külön beszél az A.B.Clear 6 és 8 modellekről, illetve a '
            '10–50-es berendezésekről — utóbbiak eltérő kialakításúak.',
            'Ez a különbség lényeges: nem csak méretben térnek el, hanem a telepítési '
            'feltételekben is. Ezért itt kapacitás és alkalmazási helyzet szerint mutatjuk '
            'be a családot, nem egyetlen sávként.',
        ]),

        sec_numbered('A tagolás logikája', 'Három tartomány', '',
                     ['<strong>Kisebb lakossági modellek.</strong> Jellemzően családi ház, '
                      'egy háztartás. Ide tartoznak azok a modellek, amelyekhez a nyilvános '
                      'tájékoztatásban is szerepelnek csőcsatlakozási adatok.',
                      '<strong>Nagyobb lakossági és kisebb közületi modellek.</strong> '
                      'Nagyobb háztartás, több háztartás, kisebb szálláshely, iroda. '
                      'Eltérő kialakítás, más telepítési feltételekkel.',
                      '<strong>50 LE fölött.</strong> Itt a projekt kikerül az egyedi '
                      'szennyvíztisztítás jogi kategóriájából, és más tervezési, '
                      'engedélyezési és üzemeltetési úton halad. Ez már nem '
                      'katalógusválasztás, hanem mérnöki feladat.']),

        hiany('a teljes, aktuális modelllista minden modell műszaki adatlapjával: névleges '
              'LE, maximális napi hidraulikai kapacitás (m³/nap), alapvető méret, befolyási '
              'szint, tipikus alkalmazás és a sajátos telepítési feltétel. Külön jelölendők '
              'a megszűnt modellek és a gyártási verziók',
              'ÖkoTech ár nélküli termékkatalógus. Ez az oldal addig a család SZERKEZETÉT '
              'írja le, nem a konkrét modelleket — mert a nyilvános anyagokban jelenleg '
              'nincs egységes modell → LE → m³/nap → alkalmazási tartomány mátrix'),

        sec_prose('Egy dokumentált adat, példaként', 'Így néz ki egy használható modelladat', [
            'Egy 2020-as vízjogi engedélyben az A.B.Clear 6 modellhez <strong>6 LE</strong> '
            'névleges terhelés és <strong>legfeljebb 0,78 m³/nap</strong> hidraulikai '
            'kapacitás szerepel. Ez jó példa arra, milyen adatpárra van szükség: a „fő” '
            'mellé mindig kell a tényleges napi vízmennyiség is.',
            'Ezt az értéket a modell hivatalos, aktuális adatlapjával <strong>újra kell '
            'ellenőrizni</strong>, mielőtt termékadatként megjelenik — egy négy évvel '
            'ezelőtti engedélypélda nem termékadatlap. Ezért szerepel itt példaként, nem '
            'specifikációként.',
        ]),

        sec_prose('Amit ne várjon ettől az oldaltól', 'A modellválasztás nem önkiszolgáló', [
            'Nem kérjük, hogy pusztán a személyszám alapján válassza ki a pontos modellt. '
            'A valós vízfogyasztás, a csúcsterhelés, a szezonalitás és a telekadatok '
            'ugyanúgy részei a döntésnek.',
            'A célunk az, hogy értse a család felépítését és a saját projektje '
            'nagyságrendjét — a végleges modellt közösen határozzuk meg, a terhelési '
            'profil és a telekadatok alapján.',
        ]),

        sec_cta('Következő lépés', 'Terhelési profil először',
                ['A modellválasztás bemenete a terhelési profil: átlag, csúcs, időtartam, '
                 'gyakoriság. Ha ez megvan, a modell kérdése lényegesen egyszerűbb.'],
                'Terhelés és kapacitás', '../projekt-elokeszites/terheles-es-kapacitas',
                alt=('Modellek és kapacitások', 'ab-clear-modellek-es-kapacitasok')),

        sec_faq([
            ('Négyen lakunk. Melyik modell kell?',
             'A létszám jó kiindulás, de önmagában nem elég a modellválasztáshoz. Kell hozzá '
             'a tényleges vízfogyasztás, a rendszeres csúcsterhelés és a tervezett bővítés '
             'is. Ezekkel együtt viszont gyorsan megvan a válasz.'),
            ('Mi a különbség a kisebb és a nagyobb modellek között?',
             'Nem csak a kapacitás: a nagyobb berendezések eltérő kialakításúak, és a '
             'telepítési feltételeik is mások. A pontos különbségeket a modellek és '
             'kapacitások oldalon gyűjtjük össze, amint az egységes adatlap rendelkezésre '
             'áll.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# A.B.Clear 2) Modellek és kapacitások
# ===========================================================================
def epit_abc_modellek():
    return [
        sec_prose('Mire jó ez az oldal', 'Kapacitás-átláthatóság', [
            'Ez az oldal a teljes modellcsaládot egységes adatstruktúrában mutatja be, hogy '
            'tervező és kivitelező is dolgozni tudjon vele: névleges lakosegyenérték, '
            'hidraulikai kapacitás, alkalmazási tartomány, tartályméret és minden olyan '
            'műszaki paraméter, amely a modellválasztást ténylegesen befolyásolja.',
            'Amit nem ad: automatikus modellválasztást. A kapacitás átláthatósága nem '
            'azonos azzal, hogy a látogató egyedül, egyetlen adatból kiválasztja a '
            'megfelelő berendezést.',
        ]),

        sec_numbered('Milyen adatokra van szükség', 'Modellenként ezek kellenek',
                     'Ez a lista egyben a hiányzó adatok listája is — lásd a megjegyzést '
                     'alább.',
                     ['<strong>Névleges lakosegyenérték (LE).</strong> A szerves terhelési '
                      'kapacitás.',
                      '<strong>Maximális napi hidraulikai kapacitás (m³/nap).</strong> '
                      'A „fő” mellé mindig kell ez is.',
                      '<strong>Befolyási és kifolyási szintek.</strong> Ezek határozzák meg, '
                      'milyen csőmélységgel telepíthető magasítás nélkül.',
                      '<strong>Méret és tömeg.</strong> A munkagödör és a beemelés '
                      'tervezéséhez.',
                      '<strong>Névleges és csúcsterhelési képesség.</strong> Csak igazolt, '
                      'dokumentált adattal — lásd alább.',
                      '<strong>Alulterhelési tartomány.</strong> Meddig működik stabilan a '
                      'névleges alatt.',
                      '<strong>Verzió és dátum.</strong> Melyik gyártási változatra '
                      'vonatkozik az adat.']),

        hiany('a teljes aktuális modellmátrix: modellenkénti névleges LE, m³/nap, '
              'befolyási és kifolyási szint, méret, tömeg, CE/teljesítménynyilatkozat, '
              'valamint az alul- és túlterhelési tartomány',
              'ÖkoTech műszaki csapat. A jelenlegi nyilvános anyagokban csak az A.B.Clear 6 '
              'és 8 csőcsatlakozási adatai szerepelnek; a 10–50-es modellekről annyi derül '
              'ki, hogy eltérő kialakításúak — ez tervezési döntéshez nem elegendő'),

        sec_prose('A túlterhelési számokról', 'Miért nem szerepelnek a táblázatban', [
            'A jelenlegi anyagainkban két különböző túlterhelési állítás szerepel: az egyik '
            'szerint a berendezés <em>tartósan</em> 30% túlterhelést bír, a másik szerint '
            '<em>2–3 napig</em> akár 150%-ot is kezel.',
            'Ez a két állítás akár egyszerre is igaz lehet — más idődimenzióról szólnak. '
            'Kapacitástáblázatba viszont csak akkor kerülhetnek, ha dokumentált, hogy a '
            'százalék <strong>mire vonatkozik</strong> (személyszám, vízmennyiség vagy '
            'szerves terhelés), <strong>mely modellekre</strong>, <strong>mennyi '
            'ideig</strong>, <strong>milyen hőmérsékleten</strong> és <strong>milyen '
            'kifolyóvíz-minőségi kritérium mellett</strong>.',
            'Enélkül a százalék túl könnyen félreérthető — és a méretezésben pont az ilyen '
            'szám okoz utólagos problémát. Ezért inkább nem közlünk számot, mint '
            'olyat, amit nem tudunk minősíteni.',
        ]),

        sec_split('Amikor kilép a standard sávból', 'Két határ',
                  'Standard modellválasztás',
                  ['Kommunális jellegű szennyvíz',
                   'A terhelés a névleges tartományon belül',
                   'A csúcsok kiszámíthatók és rendszeresek',
                   'A telek adottságai ismertek',
                   'Katalógusmodell és szokásos kialakítás'],
                  'Mérnöki, egyedi ág',
                  ['50 LE feletti terhelés',
                   'Nem kommunális vagy technológiai szennyvíz',
                   'Erősen kiszámíthatatlan terhelési profil',
                   'Több ingatlan vagy településrészi megoldás',
                   'Egyedi tervezés, más engedélyezési út']),

        sec_cta('Következő lépés', 'A profil a bemenet',
                ['A modellválasztás nem az első lépés, hanem a terhelési profil '
                 'eredménye. Ha ez megvan, a modell kérdése egyértelműbb — és nem kell '
                 'a maximumra méretezni.'],
                'Terhelési profil és kapacitás-előminősítő',
                '../projekt-elokeszites/terhelesi-profil-eloszuro',
                alt=('Műszaki adatok', 'ab-clear-muszaki-adatok')),

        sec_faq([
            ('Miért nincs itt kapacitástáblázat?',
             'Mert a nyilvános anyagainkban jelenleg nincs egységes, minden modellre '
             'kiterjedő adatlap. Inkább megmondjuk, mi hiányzik, mint hogy hiányos vagy '
             'egymásnak ellentmondó adatokat tegyünk ki. A konkrét projektnél a műszaki '
             'kollégáink pontos adatot adnak.'),
            ('A maximális vendégszámra méretezzünk?',
             'Nem. Az évi néhány alkalommal jelentkező csúcs miatt választott nagyobb '
             'rendszer az év többi napján tartósan alulterhelt lenne — és az önálló '
             'üzemeltetési probléma. Az átlag és a rendszeres csúcs együtt a helyes '
             'kiindulás.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# A.B.Clear 3) Műszaki adatok
# ===========================================================================
def epit_abc_muszaki():
    return [
        sec_prose('Egyetlen forráspont', 'Miért van szükség erre az oldalra', [
            'Ez az oldal az A.B.Clear termékcsalád <strong>egyetlen hivatalos webes műszaki '
            'forráspontja</strong>. A cél az, hogy ugyanaz az adat ne jelenjen meg eltérő '
            'változatokban a gyakori kérdésekben, a szakmai cikkekben és a '
            'engedélypéldákban.',
            'Ahol az adat még nincs egységesítve, azt itt jelezzük — nem hallgatjuk el, és '
            'nem választunk önkényesen a változatok közül.',
        ]),

        sec_prose('Kifolyóvíz-jellemzők', 'A mért értékek és ami mögöttük van', [
            'A jelenlegi műszaki tájékoztatásunk a kifolyó vízre az alábbi jellemző '
            'értékeket közli VITUKI-vizsgálatra hivatkozva: <strong>55 mg/l KOI(Cr), '
            '15 mg/l BOI5, 18 mg/l lebegőanyag, 9 mg/l ammónium-nitrogén, 20 mg/l összes '
            'nitrogén, 5 mg/l összes foszfor</strong>.',
            'Ezek használható, erős adatok — de csak a hozzájuk tartozó kontextussal együtt '
            'értelmezhetők: <em>melyik modellen</em>, <em>milyen tesztkörülmények között</em>, '
            '<em>mikor</em> mérték, és <em>milyen alkalmazhatósági határok</em> mellett '
            'érvényesek. Ezt a teljes vizsgálati jegyzőkönyvvel kell összekapcsolni.',
            'A vízminőségi értékek nem terméktulajdonságok abban az értelemben, hogy minden '
            'körülmények között garantáltak lennének: a tényleges kilépővíz-minőség a '
            'terheléstől, az üzemeltetéstől és a biológia állapotától is függ.',
        ]),

        sec_numbered('Amit ennek az oldalnak tartalmaznia kell', 'A teljes specifikáció',
                     'A lista egyben a dokumentumaudit feladatlistája is.',
                     ['Modell, névleges LE, m³/nap',
                      'Méretek, kamratérfogatok, tömeg',
                      'A tartály anyaga és szerkezete',
                      'Befolyó és kifolyó szintek',
                      'Kompresszor típusa és teljesítménye',
                      'Villamosenergia-igény',
                      'Vezérlés és üzemmódok',
                      'Levegőztetési rendszer',
                      'Kifolyóvíz-jellemzők a vizsgálati háttérrel',
                      'EN 12566-3 és CE dokumentáció',
                      'Telepítési hőmérsékleti és terhelési korlátok',
                      'Dokumentumverzió és utolsó frissítés dátuma']),

        hiany('a teljes VITUKI vizsgálati jegyzőkönyv (vizsgált modell, tesztkörülmények, '
              'dátum), a CE/teljesítménynyilatkozat modellenként, a termék- és villamos '
              'rajzok, a kamratérfogatok, a kompresszoradatok és a modellenkénti '
              'energiafogyasztás',
              'ÖkoTech műszaki dokumentáció. A kifolyóvíz-értékek addig „jellemző mért '
              'értékként" szerepelnek forrásmegjelöléssel — nem garantált '
              'terméktulajdonságként'),

        sec_prose('A jogszabályi megfelelőségről', 'Nem időtlen terméktulajdonság', [
            'A jelenlegi műszaki tartalmunk „megfelel a 28/2004. rendeletnek” típusú '
            'kijelentést tartalmaz. Az ilyen megfelelőségi állítást mindig az '
            '<strong>aktuális rendeletszöveghez</strong> kell igazítani, és nem kezelhető '
            'úgy, mintha a termék állandó tulajdonsága lenne.',
            'A jogszabályok és a szabványok időről időre módosulnak. Ezért ezen az oldalon '
            'minden megfelelőségi hivatkozás mellett szerepelnie kell annak, hogy melyik '
            'változatra vonatkozik, és mikor ellenőriztük utoljára.',
        ]),

        sec_cta('Következő lépés', 'A dokumentumok külön oldalon',
                ['A teljesítménynyilatkozat, a használati utasítás, a telepítési útmutató és '
                 'a vizsgálati jegyzőkönyv a dokumentumtárba kerül — verzióval, dátummal és '
                 'érvényességi állapottal.'],
                'Dokumentumok és tanúsítványok', 'ab-clear-dokumentumok',
                alt=('Iszapzsákos technológia', 'ab-clear-iszapzsakos-technologia')),

        sec_faq([
            ('Milyen minőségű vizet ad ki a berendezés?',
             'A rendelkezésre álló mérési eredmények szerint a kifolyó víz KOI, BOI5, '
             'lebegőanyag és tápanyagtartalom szempontjából jelentősen tisztított. '
             'A konkrét értékeket fent közöljük, a forrás megjelölésével — de ezek '
             'vizsgálati eredmények, nem minden körülmények között garantált értékek.'),
            ('Megfelel a szabványnak?',
             'A berendezések az EN 12566-3 szabvány szerinti megfelelőség alapján viselik a '
             'CE-jelölést, akkreditált vizsgálat alapján. A dokumentumok közvetlen '
             'elérhetőségén dolgozunk, hogy ez ne állítás, hanem ellenőrizhető irat legyen.'),
            ('Iható a tisztított víz?',
             'Nem, és nem is arra készül. Emberi fogyasztásra semmilyen körülmények között '
             'nem alkalmas. A tisztított víz elhelyezése önálló tervezési feladat.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# A.B.Clear 4) Iszapzsákos technológia
# ===========================================================================
def epit_abc_iszapzsak():
    return [
        sec_prose('A probléma', 'Miért kell egyáltalán iszapot kezelni?', [
            'Az aktív biológiai tisztítás közben <strong>fölösiszap keletkezik</strong> — a '
            'baktériumok szaporodnak, és a többletet el kell vezetni. Ha ez nem történik '
            'meg, a rendszer eliszaposodik, a tisztítás hatásfoka romlik.',
            'A hagyományos megoldás a rendszeres szippantás: időnként jön a szippantóautó, '
            'és elszállítja a felhalmozódott iszapot. Ez működik, de rendszeres költség és '
            'szervezési feladat — és pontosan az, amitől sokan a rendszert választanák.',
            'A nagy szennyvíztisztító telepeken viszont nem így megy: ott az iszapszint '
            'kezelése folyamatos, egyenletes folyamat. Az ÖkoTech saját fejlesztése ezt a '
            'logikát vitte át háztartási méretbe.',
        ]),

        sec_numbered('Hogyan működik', 'Az iszapzsákos megoldás', '',
                     ['<strong>Iszapsűrítő tér.</strong> A fölösiszap egy elkülönített '
                      'térbe kerül, ahol besűrűsödik — a víztartalom nagy része '
                      'visszaválik.',
                      '<strong>Vízvisszavezetés.</strong> A kivált víz visszakerül a '
                      'folyamatba. Így nem víz távozik, hanem a tényleges iszapmennyiség '
                      'marad.',
                      '<strong>Az iszapzsák.</strong> A besűrűsödött iszap zsákba kerül, '
                      'ahol tovább víztelenedik. A zsák visszatartja a szilárd részt.',
                      '<strong>A zsák kezelése.</strong> Amikor megtelt, kezelni kell. '
                      'Ez <strong>tulajdonosi feladat</strong>, és a folyamat része — nem '
                      'kivétel, hanem a modell lényege.']),

        sec_prose('A „zéró szippantás” pontosan', 'Mit jelent, és mit nem', [
            'Az iszapzsákos megoldás <strong>normál üzemeltetési feltételek mellett '
            'kiváltja a rendszeres szippantást</strong>. Ez valós, dokumentálható előny, '
            'és jelentős különbség a hagyományos megoldásokhoz képest.',
            'Amit <strong>nem</strong> jelent: hogy nincs teendő az iszappal. Az iszapszint '
            'ellenőrzése és beállítása tényleges üzemeltetési feladat, és a zsák kezelése '
            'is a tulajdonosé. Az iszapzsák tehát nem „karbantartás nélküli” megoldás, '
            'hanem <strong>eltérő iszapkezelési modell</strong>.',
            'Emellett lehetnek rendkívüli helyzetek — üzemzavar, tartós túlterhelés, a '
            'biológia sérülése —, amikor mégis szükség lehet egyéb beavatkozásra. Ezt '
            'jobb előre tudni, mint utólag csalódni.',
            'Így megfogalmazva az előny nem gyengül. Éppen ellenkezőleg: ellenőrizhetővé '
            'válik, és nem kelt olyan várakozást, amit a valóság nem tud teljesíteni.',
        ]),

        sec_split('Két iszapkezelési modell', 'Az összevetés',
                  'Hagyományos: rendszeres szippantás',
                  ['Az iszap a berendezésben halmozódik fel',
                   'Időnként szippantóautó szükséges',
                   'Rendszeres, visszatérő költség',
                   'Szervezési feladat: időpont, hozzáférés',
                   'A tulajdonosnak nincs napi teendője az iszappal'],
                  'A.B.Clear: iszapzsákos kezelés',
                  ['A fölösiszap folyamatosan a sűrítő térbe kerül',
                   'A víz visszaválik a folyamatba',
                   'Normál üzemben nincs rendszeres szippantás',
                   'A zsák kezelése tulajdonosi feladat',
                   'Fogyóeszköz-költség jelentkezik helyette']),

        hiany('a szabadalmi azonosítók és aktuális státuszuk országonként (magyar, EP, '
              'EAPO, vietnámi), az iszapzsák cseréjének VALÓS gyakorisága többéves '
              'ügyféladatok alapján, a szippantást mégis igénylő kivételes esetek, valamint '
              'a zsák kezelésének higiéniai és további kezelési protokollja',
              'ÖkoTech műszaki csapat és szerviz. A legerősebb bizonyíték itt a többéves '
              'üzemeltetési adat lenne: milyen gyakran kezelik a zsákot, mennyi iszap '
              'keletkezik, és valóban hány esetben vált szükségtelenné a szippantás'),

        sec_prose('Elismerés és oltalom', 'Amit a díj és a szabadalom jelent', [
            'A megoldás <strong>2014-ben Construma Nagydíjat</strong> kapott, és szabadalmi '
            'oltalom alatt áll. Ez azt mutatja, hogy a fejlesztés szakmai elismerést kapott, '
            'és hogy nem másolt megoldásról van szó.',
            'Amit ez <strong>nem</strong> bizonyít: a hosszú távú működést. Ahhoz üzemeltetési '
            'adat kell — hány éve működik, milyen gyakorisággal kezelik a zsákot, milyen '
            'szervizbeavatkozások fordultak elő. Ezen dolgozunk, és amint rendelkezésre '
            'áll, ide kerül.',
        ]),

        sec_cta('Következő lépés', 'Mi jár még az üzemeltetéssel?',
                ['Az iszapkezelés csak az egyik tulajdonosi feladat. Az üzemeltetés oldalán '
                 'tételesen végigvesszük, mi az, amit a tulajdonos ellenőriz, és mi tartozik '
                 'szervizhez.'],
                'Üzemeltetés és karbantartás', 'biologiai-uzemeltetes-es-karbantartas',
                alt=('Műszaki adatok', 'ab-clear-muszaki-adatok')),

        sec_faq([
            ('Milyen gyakran kell kezelni az iszapzsákot?',
             'A pontos gyakoriságot most nem tudjuk általánosan megmondani, mert a terheléstől '
             'és az üzemeltetéstől függ, és a valós, többéves adatokat még gyűjtjük. '
             'A konkrét berendezéshez tartozó dokumentáció ad rá iránymutatást — és a '
             'rendszeres iszapellenőrzésből úgyis látszik, mikor esedékes.'),
            ('Mit kell csinálni a megtelt zsákkal?',
             'A kezelés módját a berendezés használati utasítása írja le. Ez tulajdonosi '
             'feladat, és higiéniai szabályok tartoznak hozzá. A pontos protokollt a '
             'beüzemeléskor átadjuk és bemutatjuk.'),
            ('Előfordulhat, hogy mégis kell szippantás?',
             'Igen, rendkívüli helyzetben. Üzemzavar, tartós túlterhelés vagy a biológia '
             'sérülése esetén szükség lehet egyéb beavatkozásra. Normál üzemben ez nem '
             'jellemző — de nem mondjuk azt, hogy soha.'),
            ('Ez tényleg egyedi megoldás?',
             'Szabadalmi oltalom alatt álló saját fejlesztés, amely 2014-ben Construma '
             'Nagydíjat kapott. A szabadalmi azonosítókat és az országonkénti státuszt a '
             'dokumentumtárban tesszük elérhetővé.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# A.B.Clear 5) Telepítési feltételek
# ===========================================================================
def epit_abc_telepites():
    return [
        sec_prose('Miért van külön oldala', 'Ne az apróbetűben derüljön ki', [
            'A telepítési előfeltételek eddig szétszórtan szerepeltek: némelyik a gyakori '
            'kérdések között, némelyik a megrendelőlap apróbetűs részében. Ez az oldal '
            'egy helyre gyűjti őket — mert ezek nem részletkérdések, hanem a kivitelezés '
            'előfeltételei.',
            'A cél az, hogy a projekt ne helyszíni meglepetésekkel induljon. Amit itt előre '
            'tisztázunk, az nem kerül többletköltségbe a gödör szélén.',
        ]),

        sec_numbered('A helyszín előkészítése', 'Mit kell biztosítani?', '',
                     ['<strong>A tartály helye.</strong> Megfelelő távolságra az épülettől, '
                      'a kúttól és a telekhatártól, a szervizhozzáféréssel együtt tervezve.',
                      '<strong>A befolyó cső szintje.</strong> Ez határozza meg, kell-e '
                      'magasító elem vagy átemelő akna. A modellenkénti pontos értékek '
                      'egyeztetést igényelnek — lásd az alábbi megjegyzést.',
                      '<strong>Talajvíz és tartályrögzítés.</strong> Magas talajvíznél '
                      'betonmedencés vagy más rögzített kialakítás szükséges a felúszás '
                      'ellen.',
                      '<strong>A tisztított víz útja.</strong> A szikkasztó vagy más '
                      'elhelyezés helye és kialakítása — ez a projekt előfeltétele, nem '
                      'utólagos kiegészítő.',
                      '<strong>Villamos kiállás.</strong> Megfelelően védett elektromos '
                      'csatlakozás a berendezéshez.',
                      '<strong>Járműterhelés.</strong> A tartály fölött külön méretezett '
                      'betonakna nélkül nem vezethető gépjárműforgalom.',
                      '<strong>Munkagép hozzáférése.</strong> Behajtási szélesség, belógó '
                      'akadályok, a beemelés útvonala, a kitermelt föld helye.',
                      '<strong>Szervizhozzáférés.</strong> A fedlap tartósan nyitható és '
                      'megközelíthető kell maradjon.']),

        hiany('a modellenkénti pontos befolyási szintek és a megengedett magasítás. '
              'A nyilvános anyagokban ELTÉRŐ értékek szerepelnek: a gyakori kérdések az '
              'A.B.Clear 6 és 8 modellnél 51 cm befolyási szintet, magasítás nélkül '
              'legfeljebb 46 cm vezetékmélységet és legfeljebb 35 cm magasítóelemet '
              'említenek, a megrendelőlap viszont 30 cm feletti magasítást nevez meg '
              'működésképtelennek. A 10–50-es modellekről nincs nyilvános adat',
              'ÖkoTech műszaki csapat — aktuális telepítési kézikönyv és modellenkénti '
              'adatlap. Ez a legfontosabb nyitott pont ezen az oldalon: a látogató jelenleg '
              'nem tudja eldönteni, kell-e magasító vagy átemelő'),

        sec_split('Ki végzi', 'Felelősségi megosztás',
                  'Lehet a megrendelő vagy saját kivitelezője',
                  ['Földmunka, munkagödör kiemelése',
                   'Csővezeték fektetése a háztól',
                   'Villamos kiállás kiépítése',
                   'A tisztított víz elhelyezésének kivitelezése',
                   'Visszatöltés és terep rendezése',
                   'Szállítás — saját szállítással is megoldható'],
                  'ÖkoTech-szolgáltatásként kérhető',
                  ['Szállítás a helyszínre',
                   'Szerelés',
                   'Üzembe helyezés és beüzemelés',
                   'Átadás és a tulajdonos betanítása',
                   'Ezek külön szolgáltatási elemek, nem automatikusan része a '
                   'berendezés megrendelésének']),

        sec_prose('Átadás és betanítás', 'Ami a kivitelezés végén történik', [
            'A beüzemelés nem a berendezés bekapcsolása. Része a rendszer működésének '
            'ellenőrzése, a vezérlés beállítása, és — ami a leggyakrabban elmarad — a '
            'tulajdonos <strong>betanítása</strong>.',
            'A betanításon derül ki, hogyan kell elvégezni az ülepedési vizsgálatot, hogyan '
            'kell kezelni az iszapzsákot, mit jelent a vezérlés jelzése, és mit kell '
            'ellenőrizni rendszeresen. Ezt érdemes komolyan venni — a rendszer hosszú távú '
            'működése ezen múlik.',
            'Az átadás dokumentálva történik, és a berendezéshez tartozó iratok — használati '
            'utasítás, teljesítménynyilatkozat, jótállás — ekkor kerülnek át.',
        ]),

        sec_cta('Következő lépés', 'Előbb a telekadatok',
                ['A telepítési feltételek nagy része telekadat. Ha ezek megvannak, a '
                 'kivitelezés tervezhető — ha nem, a helyszíni felmérés zárja le a '
                 'nyitott kérdéseket.'],
                'Telekalkalmasság', '../projekt-elokeszites/telekalkalmassag',
                alt=('Dokumentumok és tanúsítványok', 'ab-clear-dokumentumok')),

        sec_faq([
            ('Saját kivitelezővel is telepíthető?',
             'A földmunka, a csövezés és a villamos kiállás jellemzően végezhető saját '
             'kivitelezővel. A szerelés és az üzembe helyezés külön szolgáltatási elem — '
             'ennek feltételeit a konkrét megrendelésnél egyeztetjük, mert a jótállás '
             'is kapcsolódhat hozzá.'),
            ('Mennyi ideig tart a telepítés?',
             'A földmunkától és a helyszíni körülményektől függ. A berendezés elhelyezése '
             'önmagában rövid folyamat; a teljes kivitelezés — a vízelhelyezés '
             'kialakításával együtt — jellemzően több nap. Pontos ütemezést a konkrét '
             'projektnél tudunk mondani.'),
            ('Kell hozzá engedély?',
             'Ez projekt- és helyszínfüggő, és az eljárási szabályok időről időre '
             'változnak. A korábbi engedélypéldáink 2020-asak, ezért mai eljárási '
             'szabályként nem használhatók. A projekt-előkészítés szakasz foglalkozik '
             'ezzel, aktuális forrásokkal.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# A.B.Clear 6) Dokumentumok és tanúsítványok
# ===========================================================================
def epit_abc_dokumentumok():
    return [
        sec_prose('Mi lesz ez az oldal', 'Egyetlen, verziózott bizonyítéktár', [
            'A cél az, hogy ez az oldal legyen az A.B.Clear termékek műszaki és '
            'megfelelőségi iratainak egyetlen hiteles, naprakész gyűjtőhelye — modell és '
            'dokumentumtípus szerint kereshetően.',
            'Ma ez a bizonyítékrendszer szétszórt: a CE- és EN 12566-3 megfelelőség, az '
            'akkreditált vizsgálat, a szabadalom és a korábbi engedélypéldák külön-külön '
            'szerepelnek a webhelyen, de nem állnak össze verziózott dokumentumtárrá.',
            'Ez az A.B.Clear szakmai hitelességének egyik legnagyobb kihasználatlan '
            'lehetősége — és őszintén szólva a legkönnyebben orvosolható is.',
        ]),

        sec_numbered('Milyen dokumentumok tartoznak ide', 'A dokumentumtár szerkezete',
                     'Minden irat mellett szerepelnie kell: modell, verzió, kiadás dátuma, '
                     'érvényességi állapot és dokumentumtulajdonos.',
                     ['<strong>Teljesítménynyilatkozat és CE-dokumentum.</strong> '
                      'Modellenként, az EN 12566-3 kapcsolódás megjelölésével.',
                      '<strong>Vizsgálati jegyzőkönyv.</strong> A teljes akkreditált '
                      'vizsgálati dokumentum, amelyre a kifolyóvíz-értékek hivatkoznak.',
                      '<strong>Használati és karbantartási utasítás.</strong> Modellenként, '
                      'az aktuális verzióval.',
                      '<strong>Telepítési útmutató.</strong> A kivitelezőnek és a '
                      'megrendelőnek egyaránt.',
                      '<strong>Műszaki adatlap és termékrajz.</strong> Méretek, szintek, '
                      'csatlakozások.',
                      '<strong>Garancia és jótállás.</strong> A feltételekkel együtt.',
                      '<strong>Szabadalmi dokumentum.</strong> Az iszapzsákos megoldáshoz, '
                      'országonkénti státusszal.',
                      '<strong>Korábbi engedélypéldák.</strong> Kizárólag „példa, '
                      'történeti dokumentum" minősítéssel — ezek NEM bizonyítják a mai '
                      'automatikus engedélyezhetőséget.']),

        hiany('maga a dokumentumtár. Kötelező dokumentumaudit szükséges: minden aktuális '
              'CE/teljesítménynyilatkozat, a teljes vizsgálati jegyzőkönyv, az aktuális '
              'használati és telepítési utasítás, a szabadalmi iratok, a garanciafeltételek '
              'és a modellváltozások nyilvántartása',
              'ÖkoTech műszaki és minőségügyi felelős. KÜLÖN ELLENŐRZENDŐ: a nyilvánosan '
              'elérhető használati és karbantartási utasítás V4_2019.02.27. verziójú — '
              'meg kell vizsgálni, ez-e még minden értékesített modell aktuális kezelési '
              'dokumentuma'),

        sec_split('Miért számít a verziózás', 'Két külön igény',
                  'Új értékesítés',
                  ['Az aktuális modellek aktuális dokumentumai kellenek',
                   'A megfelelőségi hivatkozásnak a hatályos szabványra kell mutatnia',
                   'A tervezőnek a mai adatlap kell, nem a tavalyi',
                   'A hatósági eljáráshoz érvényes irat szükséges'],
                  'Régi termékek támogatása',
                  ['Egy tíz éve telepített berendezéshez az AKKORI utasítás tartozik',
                   'Az alkatrészellátáshoz a gyártási verzió ismerete kell',
                   'A régi dokumentumnak elérhetőnek kell maradnia — archív státusszal',
                   'A kettőt nem szabad összekeverni: aki régi rendszert üzemeltet, '
                   'ne a mai adatlapot kapja']),

        sec_prose('A bizonyítéki lánc', 'Állítás → dokumentum → forrás', [
            'Minden műszaki állításnak vezetnie kell egy dokumentumhoz, és minden '
            'dokumentumnak azonosíthatónak kell lennie. Ha azt írjuk, hogy a berendezés '
            'megfelel egy szabványnak, akkor a megfelelőségi irat legyen egy kattintásra.',
            'Ez nem formalitás. A tervező, a kivitelező és a hatósági szereplő számára '
            'pontosan ez a különbség a marketingállítás és a használható műszaki '
            'információ között — és ez az, amit a versenytársak jellemzően nem tesznek meg.',
        ]),

        sec_cta('Addig is', 'Kérje el, amire szüksége van',
                ['Amíg a dokumentumtár nem áll össze, a szükséges iratokat közvetlenül '
                 'megküldjük. Írja meg, melyik modellről és milyen dokumentumról van szó — '
                 'és hogy milyen célra kell, mert attól függ, melyik verzió a helyes.'],
                'Kapcsolatfelvétel', '../kapcsolat',
                alt=('Műszaki adatok', 'ab-clear-muszaki-adatok')),

        sec_faq([
            ('Megkaphatom a teljesítménynyilatkozatot vásárlás előtt?',
             'Igen. Írja meg, melyik modell érdekli, és megküldjük. Tervezéshez és '
             'engedélyezési eljáráshoz ez gyakran szükséges is.'),
            ('A régi berendezésemhez hol találok dokumentációt?',
             'Adja meg a berendezés típusát és a telepítés hozzávetőleges évét — a hozzá '
             'tartozó, akkori dokumentációt keressük ki. A mai adatlap egy tíz éve '
             'telepített rendszerhez nem feltétlenül érvényes.'),
            ('A régi engedélypéldák bizonyítják, hogy engedélyezhető lesz?',
             'Nem. Azok konkrét projektekhez tartozó, 2020-as dokumentumok, és nem '
             'jelentenek automatikus mai engedélyezhetőséget. Példaként hasznosak — '
             'megmutatják, milyen adatokat tartalmazott egy ilyen eljárás —, de a mai '
             'szabályokat mindig aktuális forrásból kell ellenőrizni.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# A.B.Clear 7) Kapcsolódó referenciák
# ===========================================================================
def epit_abc_referenciak():
    return [
        sec_prose('Csak A.B.Clear', 'Miért szűkebb, mint az általános referencialista', [
            'Ez az oldal kizárólag olyan projekteket mutat, ahol ténylegesen A.B.Clear '
            'berendezés működik. Nem keveredik össze az ÖkoTech más technológiájú vagy '
            'általános vállalati projektjeivel — mert ha a terméket értékeli, akkor a '
            'termékről szóló bizonyíték számít.',
            'Minden esethez a döntés szempontjából releváns adatok tartoznak: modell, '
            'kapacitás, telepítés éve, használati helyzet, telek- és vízelhelyezési '
            'kialakítás, és a rendelkezésre álló működési eredmény.',
        ]),

        sec_situations('A.B.Clear projektek', 'Dokumentált telepítések',
                       'A jelenlegi referenciáink közül azok, ahol A.B.Clear berendezések '
                       'működnek.',
                       [
                           ('nav-kozossegi', 'Csikvánd — 128 berendezés',
                            'Egyedi berendezésekre épülő községi megoldás. A lépték itt a '
                            'bizonyíték: nem egyetlen telepítés sikere, hanem 128 '
                            'rendszeré egyszerre.',
                            '../eredmenyek/csikvand', 'Csikvánd'),
                           ('nav-kozossegi', 'Diósberény — 90 berendezés',
                            'Hasonló léptékű települési projekt, évek óta üzemelő '
                            'rendszerekkel.',
                            '../eredmenyek/diosbereny', 'Diósberény'),
                           ('nav-kozossegi', 'Bakonypéterd — négy 50 fős berendezés',
                            'Négy berendezésből kialakított központi telep. Azt mutatja, '
                            'hogyan skálázható a termékcsalád az egyedi telepítésen túl.',
                            '../eredmenyek/bakonypeterd', 'Bakonypéterd'),
                           ('nav-esettanulmany', 'Óbudavár — a kezdet',
                            'A legkorábbi dokumentált projektek egyike. A hosszú működési '
                            'idő önmagában is bizonyíték.',
                            '../eredmenyek/obudavar', 'Óbudavár'),
                       ]),

        sec_numbered('Amit egy termékreferenciának tartalmaznia kell',
                     'A hasznos esetlap adatai', '',
                     ['A.B.Clear modell és névleges kapacitás',
                      'A projekt típusa és a használati profil',
                      'A telepítés éve és az azóta eltelt működési idő',
                      'A telek adottságai — különösen a talajvíz',
                      'Hogyan oldották meg a tisztított víz elhelyezését',
                      'Kivitelezési sajátosság, ha volt',
                      'Üzemeltetési és karbantartási tapasztalat',
                      'Alkatrészcsere és szerviztörténet',
                      'Rendelkezésre álló laboreredmény',
                      'Ügyfél-visszajelzés, ahol van hozzájárulás']),

        hiany('a teljes A.B.Clear telepítési adatbázis: modell, év, helyszín, CRM-adat, '
              'szerviztörténet, laboreredmények és tulajdonosi hozzájárulások. Külön '
              'értékes lenne 5, 10 vagy régebb óta működő berendezések bemutatása '
              'karbantartási, alkatrész- és iszapkezelési tapasztalattal',
              'ÖkoTech projektarchívum és CRM. A hosszú működési idő közvetlenebbül '
              'bizonyítja a hosszú távú értékajánlatot, mint bármelyik telepítéskori fotó'),

        sec_prose('A telepítésszámról', 'Miért nem ezzel érvelünk', [
            'A webhelyünk több helyen említ összesített telepítésszámot, és ezek a számok '
            'nem egységesek — különböző időpontokban készült tartalmakból származnak.',
            'Ezért a „legtöbb telepítés Magyarországon” típusú piacvezetői állítást itt nem '
            'használjuk. Amíg nincs aktuális, dátumozott szám és összehasonlítási alap, '
            'az ilyen állítás nem ellenőrizhető — és ami nem ellenőrizhető, az nem '
            'bizonyíték.',
            'Helyette projektekkel érvelünk. Egy hasonló helyzetben évek óta működő rendszer '
            'többet mond, mint bármelyik összesítés.',
        ]),

        sec_cta('Következő lépés', 'Keressünk hasonlót az Ön helyzetéhez',
                ['Írja meg, mi a helyzete — létszám, használat, telek, a jelenlegi megoldás —, '
                 'és megnézzük, van-e dokumentált, hasonló A.B.Clear projektünk. Ha nincs, '
                 'azt is megmondjuk.'],
                'Kapcsolatfelvétel', '../kapcsolat',
                alt=('Bakonypéterd — központi telep', '../eredmenyek/bakonypeterd')),

        sec_faq([
            ('Van tíz éve működő A.B.Clear?',
             'Igen, a legkorábbi telepítéseink jóval régebbiek. A hozzájuk tartozó '
             'üzemeltetési és szerviztörténet összegyűjtésén dolgozunk, mert éppen ez a '
             'legerősebb bizonyíték — erősebb, mint bármelyik telepítéskori fotó.'),
            ('Meglátogatható egy működő rendszer?',
             'Ez az ügyfél hozzájárulásán múlik. Több esetben megoldható — kérdezze meg, és '
             'megnézzük, van-e a közelében olyan projekt, ahol ez elképzelhető.'),
        ]),
        JOGI,
    ]


# ===========================================================================
OLDALAK = [
    dict(file='megoldasok/biologiai-szennyviztisztitas.html',
         url='megoldasok/biologiai-szennyviztisztitas', img='biologiai',
         title='Biológiai szennyvíztisztítás — hogyan működik, kinek való | ÖkoTech Home',
         desc='Aktív biológiai szennyvíztisztítás: mit jelent, kinek megfelelő, mikor nem, '
              'milyen telek- és terhelési feltételei vannak, és mit igényel az üzemeltetés.',
         h1='Biológiai szennyvíztisztítás',
         alt='Talajmetszet egy családi ház kertje alatt: hengeres biológiai tisztítótartály '
             'belső terekkel és aknafedlapokkal',
         lead='A szennyvíz szerves szennyezőanyagait mikroorganizmusok bontják le — ugyanaz '
              'a folyamat, ami a nagy telepeken zajlik, egyetlen ingatlan léptékében. '
              'De nem minden csatorna nélküli ingatlanhoz való.',
         crumbs=CRUMB, sections=epit_hub()),

    dict(file='megoldasok/biologiai-hogyan-mukodik.html',
         url='megoldasok/biologiai-hogyan-mukodik', img='oldomedence',
         title='Hogyan működik a biológiai szennyvíztisztító? | ÖkoTech Home',
         desc='Lépésről lépésre a befolyástól a kifolyásig: kamrák, levegőztetés, '
              'eleveniszap, ülepítés és a fölösiszap kezelése.',
         h1='Hogyan működik?',
         alt='Levegőztetett biológiai medence felszíne közelről, finom buborékokkal',
         lead='Ha egyetlen fogalmat megért — az eleveniszapot —, minden más magától adódik: '
              'a levegőztetés, a vegyszerérzékenység, a terhelési korlátok és az '
              'iszapkezelés is.',
         crumbs=HUB, sections=epit_mukodes()),

    dict(file='megoldasok/biologiai-kinek-megfelelo.html',
         url='megoldasok/biologiai-kinek-megfelelo', img='csaladi-haz',
         title='Kinek megfelelő a biológiai rendszer? | ÖkoTech Home',
         desc='Nem épülettípus, hanem használati helyzet. Négy feltétel, amelynek '
              'teljesülnie kell — és a helyzetek, ahol külön vizsgálat szükséges.',
         h1='Kinek megfelelő?',
         alt='Modern földszintes családi ház gondozott kerttel, a gyepben két diszkrét '
             'aknafedlap',
         lead='Az alkalmasság nem abból következik, hogy családi házról vagy panzióról van '
              'szó, hanem abból, hogyan használják az ingatlant.',
         crumbs=HUB, sections=epit_kinek()),

    dict(file='megoldasok/biologiai-mikor-nem-megfelelo.html',
         url='megoldasok/biologiai-mikor-nem-megfelelo', img='alternativak',
         title='Mikor nem megfelelő a biológiai rendszer? | ÖkoTech Home',
         desc='Feltételes és abszolút kizárás. A leggyakoribb okok, amiért egy projekt '
              'elbukik — és mit érdemes megnézni helyette.',
         h1='Mikor nem megfelelő?',
         alt='Elhagyott, télre lezárt épület behavazott kerttel',
         lead='A rosszul megválasztott rendszer nem olcsóbb — csak később derül ki, mennyibe '
              'kerül. Az őszinte „ez nem Önnek való” többet ér bármilyen kedvezménynél.',
         crumbs=HUB, sections=epit_mikor_nem()),

    dict(file='megoldasok/biologiai-telek-es-terhelesi-feltetelek.html',
         url='megoldasok/biologiai-telek-es-terhelesi-feltetelek', img='telekvasarlas',
         title='Telek- és terhelési feltételek — biológiai rendszer | ÖkoTech Home',
         desc='Technológiai alkalmasságból projektalkalmasság: terhelés, talaj, talajvíz, '
              'szabad terület, csőszint, villamos előkészítés és hozzáférés.',
         h1='Telek- és terhelési feltételek',
         alt='Beépítetlen telek felmérés közben: kitűzőkarók, mérőszalag és talajminta-gödör',
         lead='A technológia illik a használatához — de a konkrét projekt megvalósítható-e? '
              'A tartály helye és a víz elhelyezése két külön kérdés.',
         crumbs=HUB, sections=epit_feltetelek()),

    dict(file='megoldasok/biologiai-uzemeltetes-es-karbantartas.html',
         url='megoldasok/biologiai-uzemeltetes-es-karbantartas', img='mar-van-rendszerem',
         title='Üzemeltetés és karbantartás — valós feladatok | ÖkoTech Home',
         desc='Mit ellenőriz a tulajdonos, mi tartozik szervizhez, mi mehet a lefolyóba. '
              'A „minimális karbantartás” lefordítva valós feladatokra.',
         h1='Üzemeltetés és karbantartás',
         alt='Mérőhenger iszapmintával és jegyzetfüzet egy aknafedlap mellett',
         lead='A napi működés önműködő — de nem felügyelet nélküli. Aki nem vállalja a '
              'rendszeres ellenőrzést, annál a technológia nem fog jól működni.',
         crumbs=HUB, sections=epit_uzemeltetes()),

    dict(file='megoldasok/biologiai-koltsegtenyezok.html',
         url='megoldasok/biologiai-koltsegtenyezok', img='attekintes',
         title='Költségtényezők — miből áll össze a projekt | ÖkoTech Home',
         desc='Beruházás és működés tételesen. Konkrét ár nincs — de a költségstruktúrával '
              'két ajánlatot is össze tud hasonlítani.',
         h1='Költségtényezők',
         alt='Kiterített árajánlat és számológép egy asztalon, mellette műszaki rajz',
         lead='Nem a magas ár a gyakori probléma, hanem a hiányos ajánlat. Ha tudja, mely '
              'tételekből áll össze egy projekt, látni fogja, ha valamelyik hiányzik.',
         crumbs=HUB, sections=epit_koltseg()),

    dict(file='megoldasok/biologiai-esettanulmanyok.html',
         url='megoldasok/biologiai-esettanulmanyok', img='csikvand',
         title='Kapcsolódó esettanulmányok — biológiai rendszer | ÖkoTech Home',
         desc='Működő projektek helyzet szerint. Mit bizonyít egy referencia, és mit nem — '
              'és milyen adatok teszik használhatóvá.',
         h1='Kapcsolódó esettanulmányok',
         alt='Falusi utcakép működő rendszerekkel: gondozott előkertek, a gyepben '
             'aknafedlapok',
         lead='Egy telepítéskori fotó azt bizonyítja, hogy a berendezés a földbe került. '
              'A hosszú távú működést nem. Ezért a működési időt és a szerviztörténetet '
              'keressük.',
         crumbs=HUB, sections=epit_esettanulmanyok()),

    # --- A.B.Clear alhub ---------------------------------------------------
    dict(file='megoldasok/ab-clear.html',
         url='megoldasok/ab-clear', img='biologiai',
         title='A.B.Clear termékcsalád — az ÖkoTech saját megoldása | ÖkoTech Home',
         desc='Iszapzsákos iszapkezelés, CE/EN 12566-3 megfelelőség, magyar fejlesztés. '
              'Modellek, műszaki adatok, telepítés és dokumentumok.',
         h1='A.B.Clear termékcsalád',
         alt='A.B.Clear tisztítóberendezés tartálya a telepítés előtt, mellette a fedlap '
             'és a gépészeti egység',
         lead='Az előző oldalak arról szóltak, mi az aktív biológiai szennyvíztisztítás. '
              'Ez arról, hogy az ÖkoTech saját megoldása miben áll — és melyik modell '
              'tartozik az Ön projektjéhez.',
         crumbs=HUB, sections=epit_abc_hub()),

    dict(file='megoldasok/ab-clear-termekcsalad-attekintese.html',
         url='megoldasok/ab-clear-termekcsalad-attekintese', img='attekintes',
         title='A.B.Clear termékcsalád áttekintése | ÖkoTech Home',
         desc='Hogyan tagolódik a család kapacitás és alkalmazási helyzet szerint, és hol '
              'húzódnak a határok — 50 LE fölött már mérnöki feladat.',
         h1='Termékcsalád áttekintése',
         alt='Több méretű tisztítóberendezés-tartály egymás mellett egy telephelyen',
         lead='Az A.B.Clear nem egyetlen berendezés, hanem termékcsalád — és a modellek nem '
              'csak méretben térnek el, hanem a telepítési feltételekben is.',
         crumbs=ABC, sections=epit_abc_attekintes()),

    dict(file='megoldasok/ab-clear-modellek-es-kapacitasok.html',
         url='megoldasok/ab-clear-modellek-es-kapacitasok', img='vallalkozas',
         title='A.B.Clear modellek és kapacitások | ÖkoTech Home',
         desc='Névleges LE, hidraulikai kapacitás, befolyási szintek — milyen adatokra van '
              'szükség a modellválasztáshoz, és miért nem önkiszolgáló a döntés.',
         h1='Modellek és kapacitások',
         alt='Műszaki adatlapok és mérőszalag egy asztalon, háttérben berendezés-tartály',
         lead='Kapacitás-átláthatóság — de nem automatikus modellválasztás. A valós '
              'fogyasztás, a csúcsterhelés és a telekadatok ugyanúgy részei a döntésnek.',
         crumbs=ABC, sections=epit_abc_modellek()),

    dict(file='megoldasok/ab-clear-muszaki-adatok.html',
         url='megoldasok/ab-clear-muszaki-adatok', img='kozcsatorna',
         title='A.B.Clear műszaki adatok — a hivatalos forráspont | ÖkoTech Home',
         desc='Kifolyóvíz-jellemzők a vizsgálati háttérrel, szabvány- és CE-megfelelőség, '
              'telepítési korlátok. Egyetlen hely, ahol az adat egységes.',
         h1='Műszaki adatok',
         alt='Laboratóriumi vízminta-üvegek sorban, mögöttük mérési jegyzőkönyv',
         lead='A termékcsalád egyetlen hivatalos webes műszaki forráspontja — hogy ugyanaz '
              'az adat ne jelenjen meg eltérő változatokban máshol.',
         crumbs=ABC, sections=epit_abc_muszaki()),

    dict(file='megoldasok/ab-clear-iszapzsakos-technologia.html',
         url='megoldasok/ab-clear-iszapzsakos-technologia', img='emeszto-csere',
         title='Iszapzsákos technológia — mit jelent a „zéró szippantás” | ÖkoTech Home',
         desc='Hogyan kezeli az iszapzsák a fölösiszapot, mi marad tulajdonosi feladatnak, '
              'és milyen feltételek mellett igaz, hogy nincs szükség szippantásra.',
         h1='Iszapzsákos technológia',
         alt='Iszapsűrítő tér és iszapzsák egy nyitott berendezés belsejében',
         lead='Az ÖkoTech legerősebb termékspecifikus különbsége. Nem „karbantartás '
              'nélküli” megoldás — eltérő iszapkezelési modell, világos feltételekkel.',
         crumbs=ABC, sections=epit_abc_iszapzsak()),

    dict(file='megoldasok/ab-clear-telepitesi-feltetelek.html',
         url='megoldasok/ab-clear-telepitesi-feltetelek', img='kapcsolat',
         title='A.B.Clear telepítési feltételek | ÖkoTech Home',
         desc='Csőszintek, talajvíz, rögzítés, villamos előkészítés, járműterhelés és '
              'hozzáférés — és hogy melyik munkát ki végzi.',
         h1='Telepítési feltételek',
         alt='Munkagödör a telepítés előtt, mellette a berendezés tartálya emelésre készen',
         lead='Ezek nem részletkérdések, hanem a kivitelezés előfeltételei. Amit előre '
              'tisztázunk, az nem kerül többletköltségbe a gödör szélén.',
         crumbs=ABC, sections=epit_abc_telepites()),

    dict(file='megoldasok/ab-clear-dokumentumok.html',
         url='megoldasok/ab-clear-dokumentumok', img='helyzetem',
         title='A.B.Clear dokumentumok és tanúsítványok | ÖkoTech Home',
         desc='Teljesítménynyilatkozat, vizsgálati jegyzőkönyv, használati utasítás, '
              'szabadalom — verzióval, dátummal és érvényességi állapottal.',
         h1='Dokumentumok és tanúsítványok',
         alt='Iratrendezőben sorakozó műszaki dokumentumok és tanúsítványok',
         lead='Minden műszaki állításnak vezetnie kell egy dokumentumhoz. Ez a különbség a '
              'marketingállítás és a használható műszaki információ között.',
         crumbs=ABC, sections=epit_abc_dokumentumok()),

    dict(file='megoldasok/ab-clear-referenciak.html',
         url='megoldasok/ab-clear-referenciak', img='diosbereny',
         title='A.B.Clear kapcsolódó referenciák | ÖkoTech Home',
         desc='Kizárólag A.B.Clear berendezéssel működő projektek — modellel, kapacitással, '
              'telepítési évvel és működési idővel.',
         h1='Kapcsolódó referenciák',
         alt='Községi utcakép, ahol több ingatlanon egyedi tisztítóberendezés működik',
         lead='Ha a terméket értékeli, akkor a termékről szóló bizonyíték számít — ezért '
              'ez a lista szűkebb, mint az általános referenciáké.',
         crumbs=ABC, sections=epit_abc_referenciak()),
]

if __name__ == '__main__':
    for o in OLDALAK:
        out = WEB / o['file']
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:56s} {len(out.read_text(encoding='utf-8'))//1024} KB")
