#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Előkészítés → Terhelés és kapacitás — hub és a brief szerinti nyolc aloldal.

A brief NÉGY ponton javít a jelenlegi ÖkoTech-kommunikáción:

1. „1 lakosegyenérték = 135 liter/fő/nap" — ez TÉVES definíció. Az LE a
   biológiailag bontható SZERVES terhelés egysége: 1 LE = napi 60 g BOI5.
   A 135 l/fő/nap legfeljebb saját HIDRAULIKAI tervezési feltételezés lehet,
   és a kettőt terminológiailag szét kell választani. Ez az egész tudástár
   egyik legfontosabb szakmai korrekciója.

2. A 30%-os tartós és a 150%-os 2–3 napos túlterhelési állítás két külön
   dolog, két külön idődimenzióban. Egyszerre is igazak lehetnek, de csak
   akkor publikálhatók, ha dokumentált, mire vonatkozik a százalék, mely
   modellekre, mennyi ideig és milyen kifolyóvíz-minőségi kritérium mellett.

3. Az 50–100 LE közötti útvonal rendezetlen: a lakossági oldal 1–50 főig
   kommunikál, majd 50 fő felett a nagytelepi oldalra küld, az viszont
   100 LE feletti rendszerekről szól. A közte lévő sáv nincs lefedve.

4. A „hány fő?" jó BELÉPŐ kérdés, de nem lehet minden projekt méretezési
   egysége. Panziónál a kihasználtság, intézménynél a jelenléti profil,
   üzemnél a technológiai és laboradat a mérvadó.

ÁR SEHOL nem szerepel. Kapacitásváltozás legfeljebb később validált
ársávot befolyásoló tényezőként említhető.
"""
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import sablon as G
from sablon import (sec_numbered, sec_split, sec_prose, sec_situations,
                    sec_cta, sec_faq)

WEB = pathlib.Path(__file__).resolve().parents[2] / '_web'

JOGI = ('<!-- JOGI ELLENŐRZÉS PUBLIKÁLÁS ELŐTT. Érintett: 147/2010. Korm. rendelet\n'
        '     (egyedi szennyvíztisztítás 1–50 LE) · 26/2002. Korm. rendelet\n'
        '     (LE-számítás BOI5 alapján) · 220/2004. és 28/2004. rendelet (termelési és\n'
        '     szolgáltatási szennyvíz) · a 2024/3019/EU átdolgozott települési\n'
        '     szennyvíz-irányelv magyar átültetése. Dátumozott felülvizsgálat kell. -->')


def hiany(mi, honnan):
    return (f'<!-- ADATHIÁNY: {mi}\n'
            f'     Forrás: {honnan}. Addig konkrét értékkel nem publikálható. -->')


HOME = ('Főoldal', '../')
ELO = ('Előkészítés', './')
CRUMB = [HOME, ELO]
HUB = [HOME, ELO, ('Terhelés és kapacitás', 'terheles-es-kapacitas')]


# ===========================================================================
# HUB
# ===========================================================================
def epit_hub():
    return [
        sec_prose('A kiinduló kérdés', 'A „hány fő?” csak az első kérdés', [
            'A szennyvíztisztító szükséges kapacitása nem pusztán az ingatlant használó '
            'személyek számából következik. A keletkező <strong>vízmennyiség</strong>, a '
            '<strong>szervesanyag-terhelés</strong>, a használat <strong>időbeli '
            'eloszlása</strong> és a rövid vagy tartós <strong>csúcsok</strong> együtt '
            'határozzák meg.',
            'Családi háznál a létszám jó közelítés lehet, és nyugodtan azzal érdemes '
            'kezdeni. Panziónál, iskolánál, étteremnél vagy üzemnél viszont ugyanannyi „fő” '
            'egészen más vízmennyiséget és szennyezőanyag-terhelést jelenthet — ott a '
            'létszám önmagában félrevezető.',
            'Ez a szakasz ezért nem „X főhöz Y berendezés” táblázatot ad, hanem elvezet egy '
            '<strong>terhelési profilig</strong>: átlag, csúcs, a csúcs időtartama és '
            'gyakorisága, valamint a bizonytalanságok. Ebből már megalapozottan '
            'meghatározható a kapacitástartomány.',
        ]),

        sec_split('Két külön terhelés', 'Amit külön kell mérni és külön kell méretezni',
                  'Hidraulikai terhelés — mennyi VÍZ érkezik',
                  ['Napi átlagos vízmennyiség, m³/nap vagy liter/nap',
                   'Rövid idő alatt beérkező csúcs — reggeli zuhanyzás, mosógép',
                   'A vízszámlából vagy mérőóráról leolvasható',
                   'Új építésnél becsülni kell',
                   'Ez határozza meg a berendezés átfolyási kapacitását',
                   'És ez adja a naponta ELHELYEZENDŐ vízmennyiséget is'],
                  'Szerves terhelés — mennyi ANYAGOT kell lebontani',
                  ['A biológiailag bontható szennyezőanyag mennyisége',
                   'Mértékegysége a lakosegyenérték (LE): 1 LE = napi 60 g BOI5',
                   'Nem olvasható le a vízórán',
                   'Laboratóriumi vizsgálattal mérhető',
                   'Ez határozza meg a biológiai fokozat méretét',
                   'Nagy vízfogyasztás nem jelent arányosan nagy szerves terhelést']),

        sec_situations('A szakasz oldalai', 'Melyik helyzet áll a legközelebb?',
                       'A fogalmakkal érdemes kezdeni, utána a saját projekttípusnál '
                       'folytatni. A csúcsterhelés mindegyikre vonatkozik.',
                       [
                           ('nav-terheles', 'Lakosegyenérték',
                            'Mit jelent az LE, miért nem azonos a napi vízfogyasztással, '
                            'és mikor elég helyette a személyszám.',
                            'lakosegyenertek', 'Lakosegyenérték'),
                           ('epitkezes', 'Személyszám és vízfogyasztás',
                            'Családi háznál a létszám jó kiindulás — de a vízszámla '
                            'pontosabb. Hogyan lesz a kettőből használható adat.',
                            'szemelyszam-es-vizfogyasztas', 'Létszám és fogyasztás'),
                           ('nav-mukodes', 'Átlag- és csúcsterhelés',
                            'A rövid vendégcsúcs és a tartós túlterhelés nem ugyanaz. '
                            'És az alulterhelés is külön üzemállapot.',
                            'atlag-es-csucsterheles', 'Átlag és csúcs'),
                           ('nyaralo', 'Szezonális használat',
                            'Hosszú nulla terhelés és hirtelen visszatérő csúcs. Ez nemcsak '
                            'kapacitási, hanem technológiaválasztási kérdés is.',
                            'szezonalis-hasznalat', 'Szezonális használat'),
                           ('nav-vallalkozas', 'Panziók és vendéglátás',
                            'A férőhely nem terhelés. Kihasználtság, konyha, mosoda, '
                            'rendezvény — és a zsíros konyhai víz külön kérdés.',
                            'panziok-es-vendeglatas', 'Panzió, vendéglátás'),
                           ('nav-kozossegi', 'Intézményi terhelés',
                            'A „300 fős” iskola nem 300 LE. Jelenléti idő, szünetek, '
                            'nagykonyha és a napi terhelési ritmus.',
                            'intezmenyi-terheles', 'Intézmény'),
                           ('nav-adatbazis', 'Speciális vagy ipari szennyvíz',
                            'Az üzemben dolgozó 50 ember és az 50 fős üzem technológiai '
                            'szennyvize nem ugyanaz a feladat.',
                            'specialis-vagy-ipari-szennyviz', 'Ipari szennyvíz'),
                       ]),

        sec_numbered('Amit el kell kerülni', 'Négy tipikus méretezési hiba',
                     'Mindegyik ugyanabból ered: egyetlen számból méreteznek.',
                     ['<strong>A maximumra méretezés.</strong> Ha az évi néhány nagy '
                      'családi összejövetel határozza meg a berendezés méretét, a rendszer '
                      'az év többi napján tartósan alulterhelt lesz — és az önálló '
                      'üzemeltetési probléma.',
                      '<strong>A rendszeres csúcs figyelmen kívül hagyása.</strong> Az évi '
                      'két alkalom más, mint a minden hétvégén érkező vendégek. '
                      'A gyakoriság és az időtartam legalább annyira számít, mint a csúcs '
                      'nagysága.',
                      '<strong>A vízmennyiség és a szerves terhelés összekeverése.</strong> '
                      'Nagy vízfogyasztás nem jelent arányosan nagy szennyezőanyag-terhelést '
                      '— és fordítva. Étteremnél éppen az utóbbi a szűk keresztmetszet.',
                      '<strong>A bővítés kihagyása.</strong> Ha tudható, hogy két éven belül '
                      'bővül a család vagy a szálláshely, azt a tervezéskor kell figyelembe '
                      'venni. Utólag berendezést cserélni lényegesen drágább.']),

        hiany('a jelenlegi 50–100 LE közötti kapacitási sáv: a lakossági oldal 1–50 főig '
              'kommunikál, majd 50 fő felett a nagytelepi oldalra irányít — az viszont '
              '100 LE feletti rendszerekről szól. A közte lévő sáv nincs lefedve',
              'ÖkoTech belső műszaki workshop: mi a standard A.B.Clear felső névleges '
              'LE-határa, mi a 10–50-es termékcsalád valós kapacitása, mi történik 50–100 LE '
              'között, és honnan indul a konténeres/tartályos nagytelep'),

        sec_cta('Következő lépés', 'Kezdje a fogalommal',
                ['A lakosegyenérték a leggyakrabban félreértett fogalom ezen a területen — '
                 'és a félreértés konkrét méretezési hibához vezet. Néhány perc, és utána '
                 'minden további oldal érthetőbb lesz.'],
                'Lakosegyenérték', 'lakosegyenertek',
                alt=('Személyszám és vízfogyasztás', 'szemelyszam-es-vizfogyasztas')),

        sec_faq([
            ('Nem elég megmondani, hányan lakunk a házban?',
             'Családi háznál ez jó kiindulás, és sokszor elegendő is az első irányhoz. '
             'Pontosabb lesz viszont, ha a tényleges vízfogyasztást is megnézzük a '
             'vízszámláról, és megmondja, van-e rendszeres vendégcsúcs vagy tervezett '
             'létszámváltozás.'),
            ('Miért nem méretezünk a maximális létszámra?',
             'Mert az aktív biológiai rendszer baktériumközössége megfelelő '
             'tápanyagterhelést igényel. A tartósan alulterhelt rendszer önálló üzemeltetési '
             'probléma — nem „biztonságos tartalék”. A helyes megközelítés az átlag és a '
             'reálisan rendszeres csúcs együtt.'),
            ('Mi az a BOI5?',
             'A biokémiai oxigénigény öt napra vetítve: az a mennyiségű oxigén, amit a '
             'szennyvízben lévő mikroorganizmusok öt nap alatt felhasználnak a szerves anyag '
             'lebontásához. Ez a szerves terhelés mérőszáma — és ezen alapul a '
             'lakosegyenérték definíciója is.'),
            ('50 fő fölött mi változik?',
             'A 147/2010. Korm. rendelet szerinti egyedi szennyvíztisztítás kategóriája '
             '1–50 LE terhelésig terjed. E fölött a projekt más szabályozási és '
             'engedélyezési úton halad, és a tervezés is mérnöki feladattá válik.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 1) Lakosegyenérték
# ===========================================================================
def epit_le():
    return [
        sec_prose('A definíció', 'Az LE nem egy ember, és nem is liter', [
            'A lakosegyenérték (LE) a szennyvíz biológiailag lebontható szerves terhelésének '
            'szabványosított mértékegysége. A hivatalos európai meghatározás szerint '
            '<strong>1 LE olyan szerves, biológiailag bontható terhelés, amelynek ötnapos '
            'biokémiai oxigénigénye — a BOI5 — napi 60 gramm oxigénnek felel meg.</strong>',
            'Ebből két dolog következik. Az egyik: az LE nem személy, hanem terhelés. '
            'A másik: az LE nem vízmennyiség — nem liter, nem köbméter.',
            'A magyar szabályozásban az egyedi szennyvíztisztítás fogalma legalább 1, '
            'legfeljebb 50 LE terhelésig terjed, ezért az LE nem pusztán műszaki adat: '
            'a projekt szabályozási kategóriáját is meghatározza.',
        ]),

        sec_prose('Egy korrekció', 'Az „1 LE = 135 liter/fő/nap” állítás téves', [
            'A jelenlegi ÖkoTech-tartalom egy helyen úgy fogalmaz, hogy „1 lakosegyenérték '
            'napi 135 liter/fő/nap vízfogyasztást jelent”. Ezt pontosítjuk: '
            'ez <strong>nem az LE definíciója</strong>.',
            'A 135 liter/fő/nap érték használható lehet saját <strong>hidraulikai '
            'tervezési feltételezésként</strong> — vagyis feltevésként arról, mennyi víz '
            'keletkezik naponta fejenként —, de a lakosegyenérték attól függetlenül a '
            'szerves terhelés egysége marad.',
            'A kettő szétválasztása nem szőrszálhasogatás. Egy étterem napi vízfogyasztása '
            'és szerves terhelése egészen máshogy arányulnak egymáshoz, mint egy családi '
            'házé — ha a kettőt ugyanannak vesszük, a méretezés hibás lesz.',
        ]),

        sec_split('A két fogalom', 'Mikor melyiket használjuk',
                  'LE — szerves terhelés',
                  ['Mértékegysége: napi 60 g BOI5 = 1 LE',
                   'A biológiai fokozat méretezésének alapja',
                   'Laborvizsgálattal mérhető',
                   'A jogi kategóriát is ez határozza meg (1–50 LE)',
                   'Intézménynél és üzemnél ez a mérvadó',
                   'Mérési adatból: napi BOI5-terhelés osztva 60 g/nap értékkel'],
                  'l/fő/nap — hidraulikai feltételezés',
                  ['Mértékegysége: liter naponta, személyenként',
                   'A vízmennyiség tervezésének alapja',
                   'A vízszámláról közelíthető',
                   'Tervezési feltevés, nem jogi kategória',
                   'Családi háznál praktikus kiindulás',
                   'A naponta elhelyezendő vízmennyiséget is ez adja']),

        sec_numbered('Mikor elég a személyszám?', 'És mikor nem',
                     'A közelítés annál pontosabb, minél inkább „szokásos háztartási” a '
                     'vízhasználat.',
                     ['<strong>Családi ház, állandó lakhatás.</strong> Itt 1 fő ≈ 1 LE '
                      'ésszerű közelítés, mert a háztartási szennyvíz összetétele nagyjából '
                      'egységes. A létszámmal érdemes kezdeni.',
                      '<strong>Nyaraló, szezonális ingatlan.</strong> A létszám még jó '
                      'kiindulás, de a használat időbeli eloszlása legalább annyira számít.',
                      '<strong>Panzió, szálláshely.</strong> A férőhely nem azonos a '
                      'terheléssel: a kihasználtság, a mosoda és a konyha külön tételek. '
                      'A létszám itt már csak belépő adat.',
                      '<strong>Iskola, iroda, intézmény.</strong> A névleges létszám nem '
                      'egész napos jelenlétet jelent. A jelenléti idő és az éves üzemnapok '
                      'nélkül a szám félrevezető.',
                      '<strong>Étterem, üzem, technológiai szennyvíz.</strong> Itt a '
                      'személyszám érdemben nem használható: a szerves terhelés a '
                      'tevékenységből ered, és laboradat kell hozzá.']),

        hiany('honnan származik az ÖkoTech által használt 135 l/fő/nap tervezési érték, '
              'mely termékadatlapok és ajánlati kalkulációk használják, és hogyan '
              'kapcsolódik a hidraulikai feltételezés a BOI5-alapú méretezéshez',
              'ÖkoTech műszaki csapat. Amíg ez nincs dokumentálva, a 135 l/fő/nap nem '
              'közölhető sem tényként, sem az LE definíciójaként'),

        sec_cta('Következő lépés', 'A gyakorlatban a vízszámlával kezdünk',
                ['A fogalom tisztázása után jön a konkrét adat. Meglévő háznál a vízszámla '
                 'a legmegbízhatóbb kiindulás, új építésnél becslés — a következő oldal '
                 'megmutatja, hogyan lesz belőlük használható terhelési adat.'],
                'Személyszám és vízfogyasztás', 'szemelyszam-es-vizfogyasztas',
                alt=('Terhelés és kapacitás', 'terheles-es-kapacitas')),

        sec_faq([
            ('Nekem is tudnom kell, mi az az LE?',
             'Családi házas projektnél nem feltétlenül — ott a létszám és a vízfogyasztás '
             'elegendő. Akkor válik fontossá, ha panzióról, intézményről vagy nagyobb '
             'projektről van szó, mert ott a személyszám már nem írja le a valós terhelést, '
             'és a jogi kategória is az LE-től függ.'),
            ('Hogyan számítható ki az LE mérésből?',
             'Ha van laboratóriumi vizsgálat, a napi BOI5-terhelést kell elosztani '
             '60 g/nap értékkel. Ehhez ismerni kell a napi szennyvízmennyiséget és a mért '
             'BOI5-koncentrációt. Mérés nélkül becsülni lehet, de az becslés marad.'),
            ('Miért fontos az 50 LE-s határ?',
             'Mert az egyedi szennyvíztisztítás jogi kategóriája eddig terjed. E fölött a '
             'projekt más szabályozási úton halad, más engedélyezési és üzemeltetési '
             'követelményekkel — és a tervezés is jogosult tervező feladata lesz.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 2) Személyszám és vízfogyasztás
# ===========================================================================
def epit_szemelyszam():
    return [
        sec_prose('A gyakorlati kiindulás', 'A létszám jó — a vízszámla jobb', [
            'Családi háznál a lakók száma jó első közelítés a szükséges kapacitáshoz. '
            'A pontosabb döntést viszont a <strong>tényleges vízhasználat</strong> segíti, '
            'mert ugyanaz a négyfős háztartás jelentősen eltérő vízmennyiséget termelhet.',
            'Meglévő háznál ezért érdemes a vízszámlából vagy a mérőóráról származó valós '
            'havi vagy éves fogyasztást használni. Ez nem becslés, hanem mért adat — és '
            'jellemzően már rendelkezésre áll.',
            'Új építésnél nincs mit leolvasni, ott a létszám, a várható életmód és a '
            'vízhasználó berendezések alapján becslés szükséges. Ezt később, az első év '
            'fogyasztási adatai alapján lehet pontosítani.',
        ]),

        sec_numbered('A vízszámla használata', 'Hogyan lesz belőle napi átlag?',
                     'Néhány perc, és lényegesen pontosabb adat lesz belőle, mint a puszta '
                     'létszámból.',
                     ['<strong>Vegyen egy teljes évet.</strong> Legalább négy negyedéves '
                      'vagy tizenkét havi számlát. Egyetlen hónap félrevezető: a nyári és a '
                      'téli fogyasztás jelentősen eltér.',
                      '<strong>Ossza el 365-tel.</strong> Az éves köbméter osztva 365-tel '
                      'adja a napi átlagos vízfogyasztást m³-ben; ezerrel szorozva literben.',
                      '<strong>Vonja le, ami nem lesz szennyvíz.</strong> A kerti öntözés, a '
                      'medencefeltöltés és az állatitatás nem terheli a rendszert. Ha külön '
                      'mérőóra van rá, egyszerű; ha nincs, a nyári többletfogyasztásból '
                      'nagyjából becsülhető.',
                      '<strong>Nézzen rá a szélsőségekre.</strong> Ha egy időszak kiugróan '
                      'magas, annak lehet oka: csőtörés, szivárgás, vagy egyszeri '
                      'feltöltés. Az ilyen érték nem a tényleges használatot mutatja, '
                      'ezért ki kell venni.',
                      '<strong>Rögzítse a létszámot is.</strong> A napi átlagot elosztva a '
                      'létszámmal megkapja a fajlagos fogyasztást — ez mutatja meg, hogy a '
                      'háztartás a szokásos sávban van-e, vagy attól eltér.']),

        sec_split('Ki számít, és hogyan', 'Négyféle létszám, ne keverje őket',
                  'Ezt kell megadni',
                  ['Állandó lakók száma — akik nap mint nap ott laknak',
                   'Jellemző napi használói létszám, ha ez ettől eltér',
                   'Maximális alkalmi létszám, a gyakoriságával együtt',
                   'Tervezett tartós létszámváltozás — gyerek, beköltöző szülő',
                   'Éves vízfogyasztás m³-ben, számláról'],
                  'Ezt külön jelezze',
                  ['Kerti öntözés vagy medence — ez nem lesz szennyvíz',
                   'Nagy vízfogyasztású berendezés — jacuzzi, több mosógép',
                   'Otthonról dolgozók: több napközbeni vízhasználat',
                   'Rendszeres hétvégi vendégek, nem alkalmi',
                   'Korábbi csőtörés vagy szivárgás a számlázott időszakban']),

        hiany('az ÖkoTech saját lakossági vízfogyasztási projektadatai, az új építésnél '
              'alkalmazott tervezési fajlagos érték, és hogy mekkora eltérésnél írja felül '
              'a mért vízfogyasztás a puszta személyszámot',
              'ÖkoTech műszaki csapat + megvalósult projektek fogyasztási adatai. Amíg ez '
              'nincs meg, konkrét liter/fő/nap érték nem publikálható tervezési szabályként'),

        sec_prose('Amit a víz nem mutat meg', 'A vízmennyiség és a szennyezés két külön adat', [
            'Nagy vízfogyasztás nem jelent automatikusan arányosan nagy '
            'szervesanyag-terhelést. Aki sokat zuhanyzik és sokat mos, sok vizet használ, de '
            'a szennyezőanyag-mennyisége ettől nem lesz arányosan nagyobb — a szennyvize '
            'hígabb lesz.',
            'Fordítva is igaz: viszonylag kevés vízzel is érkezhet nagy szerves terhelés — '
            'jellemzően ott, ahol konyhai vagy technológiai szennyvíz is van a rendszerben.',
            'Ezért kérdezünk rá a szokatlan vízhasználatra külön. Szokásos háztartásnál a '
            'kettő együtt mozog, és a vízfogyasztásból jól közelíthető a terhelés — de '
            'rendhagyó használatnál a két adatot külön kell kezelni.',
        ]),

        sec_cta('Következő lépés', 'Az átlag még nem a teljes kép',
                ['Az átlagos napi terhelés mellett az is számít, hogy mikor és mennyivel tér '
                 'el ettől a valóság. A vendégcsúcs, a hosszabb távollét és a tartós '
                 'túlterhelés más-más kockázatot jelent.'],
                'Átlag- és csúcsterhelés', 'atlag-es-csucsterheles',
                alt=('Terhelés és kapacitás', 'terheles-es-kapacitas')),

        sec_faq([
            ('Nincs meg a vízszámlám. Mit tegyek?',
             'A szolgáltatói ügyfélportálon jellemzően visszanézhető a fogyasztási előzmény. '
             'Ha ez sem elérhető, a létszám és a használati szokások alapján becslés '
             'készíthető — csak jelezze, hogy becslésről van szó, mert a méretezésben ez '
             'számít.'),
            ('Új házat építünk, még nincs fogyasztásunk.',
             'Ilyenkor a létszámból és a tervezett életmódból indulunk ki: hány fő, hány '
             'fürdőszoba, van-e otthon dolgozó, terveznek-e medencét vagy jelentős kerti '
             'vízhasználatot. Ez becslés, ezért a bővítési tartalékot is érdemes átgondolni.'),
            ('Beleszámít a kerti öntözés?',
             'A szennyvízterhelésbe nem: az a víz nem jut a rendszerbe. A vízszámlában '
             'viszont benne van, ezért ki kell venni belőle. Ha nincs külön mérőóra, a nyári '
             'és a téli fogyasztás különbségéből nagyjából becsülhető.'),
            ('Havonta változik a létszámunk. Mit írjak?',
             'Adja meg az állandó lakók számát, és külön a jellemző maximumot a '
             'gyakoriságával együtt — például „négyen lakunk, minden második hétvégén '
             'hatan”. A méretezésnél éppen ez a két adat együtt számít.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 3) Átlag- és csúcsterhelés
# ===========================================================================
def epit_csucs():
    return [
        sec_prose('A helyes kérdés', 'Nem a maximum, hanem a rendszeres',
                  [
            'A berendezést nem érdemes automatikusan az ingatlan valaha előforduló legnagyobb '
            'személyszámára méretezni. Az évi egy-két nagy összejövetel miatt választott '
            'nagyobb rendszer az év többi napján tartósan alulterhelt lesz — és az önálló '
            'üzemeltetési probléma, nem biztonsági tartalék.',
            'A <strong>rendszeresen vagy tartósan</strong> jelentkező csúcsterhelést viszont '
            'nem szabad figyelmen kívül hagyni. A minden hétvégén érkező vendégek egészen '
            'mást jelentenek, mint az évi kétszeri családi ünnep.',
            'A méretezéshez ezért négy adat kell, nem egy: az <strong>átlag</strong>, a '
            '<strong>csúcs nagysága</strong>, a csúcs <strong>időtartama</strong> és a '
            '<strong>gyakorisága</strong>.',
        ]),

        sec_split('Két külön csúcs', 'Amit nem szabad összevonni',
                  'Hidraulikai csúcs — egyszerre sok víz',
                  ['Reggeli zuhanyzás, mosógép és mosogatógép egyszerre',
                   'Rövid idő alatt nagy mennyiség érkezik',
                   'Kockázat: a víz gyorsabban halad át, mint kellene',
                   'A berendezés átfolyási kapacitása a korlát',
                   'Napon belül jelentkezik, akár óránként változóan'],
                  'Szerves csúcs — sok bontandó anyag',
                  ['Vendégek, nagyobb főzés, ünnepi hétvége',
                   'A szennyezőanyag-mennyiség nő, nem feltétlenül a vízé',
                   'Kockázat: a biológiai fokozat nem győzi lebontani',
                   'A baktériumközösség alkalmazkodása időbe telik',
                   'Napokban mérhető, nem órákban']),

        sec_numbered('Négy tipikus helyzet', 'Melyik vonatkozik Önre?', '',
                     ['<strong>Alkalmi vendég.</strong> Évi néhány alkalommal többen vannak. '
                      'Ez jellemzően nem indokol nagyobb berendezést — a rendszerek rövid '
                      'ideig többletterhelést is kezelnek.',
                      '<strong>Rendszeres hétvégi többlet.</strong> Minden vagy majdnem '
                      'minden hétvégén nagyobb a létszám. Ez már méretezési tényező, mert '
                      'nem alkalmi kiugrás, hanem a használat része.',
                      '<strong>Tartós létszámnövekedés.</strong> Beköltöző családtag, '
                      'megszülető gyermek, hazaköltöző szülő. Ez az átlagot emeli meg, '
                      'ezért az átlagba kell beszámítani, nem a csúcsba.',
                      '<strong>Tartós alulterhelés.</strong> A rendszer a névlegesnél '
                      'lényegesen kevesebbet kap — hosszabb távollét, elköltöző családtagok. '
                      'Az aktív biológiai rendszer baktériumközössége tápanyagot igényel, '
                      'ezért ez is külön üzemállapot, nem „kevesebb gond”.']),

        hiany('a jelenlegi két túlterhelési állítás összehangolása és validálása: a GYIK '
              '2–3 napos 150%-os terhelése és a szakmai cikk tartós 30%-os túlterhelése. '
              'Dokumentálni kell, mire vonatkozik a százalék (személyszám, vízmennyiség vagy '
              'szerves terhelés), mely modellekre, mennyi ideig, milyen hőmérsékleten és '
              'milyen kifolyóvíz-minőségi kritérium mellett',
              'ÖkoTech műszaki csapat + EN 12566-3 vizsgálati dokumentáció + '
              'laboreredmények. A két szám akár egyszerre is igaz lehet, de forrás és '
              'alkalmazási tartomány nélkül félreérthető — így nem publikálható'),

        sec_prose('A túlméretezés is hiba', 'Miért nem jó a „biztos, ami biztos”', [
            'Az aktív biológiai rendszer élő baktériumközösséggel dolgozik, amely megfelelő '
            'tápanyagterhelést igényel. Ha a rendszer tartósan a névlegesnél lényegesen '
            'kevesebbet kap, az nem kíméli — hanem külön üzemállapotot jelent, amit kezelni '
            'kell.',
            'Ezért nem javasoljuk a „vegyünk inkább nagyobbat” logikát. A helyes méret az, '
            'amely az <strong>átlagos</strong> terhelést jól szolgálja ki, és a '
            '<strong>rendszeres</strong> csúcsokat is kezeli — nem az, amely az évi '
            'legnagyobb napra van kitalálva.',
            'Ha valóban nagy a szórás — például szezonális használatnál —, az nem '
            'méretezéssel, hanem üzemmódválasztással és technológiaválasztással kezelendő.',
        ]),

        sec_cta('Következő lépés', 'Ha hosszú szünetek is vannak',
                ['A szezonális használat külön eset: nem egyszerűen kevesebb szennyvíz, '
                 'hanem hosszabb nulla terhelés és hirtelen visszatérő csúcs. Ez nemcsak '
                 'kapacitási, hanem technológiaválasztási kérdés is.'],
                'Szezonális használat', 'szezonalis-hasznalat',
                alt=('Terhelés és kapacitás', 'terheles-es-kapacitas')),

        sec_faq([
            ('Hatan leszünk karácsonykor, egyébként négyen. Nagyobb kell?',
             'Jellemzően nem. Az évi néhány alkalommal jelentkező, néhány napos többlet '
             'rövid csúcsnak számít. Ha viszont havonta többször, rendszeresen fordul elő, '
             'az már a használat része, és a méretezésnél figyelembe kell venni.'),
            ('Mennyi többletterhelést bír a rendszer?',
             'Erre szándékosan nem adunk most számot. A jelenlegi anyagainkban két különböző '
             'érték szerepel, két különböző idődimenzióban, és nincs dokumentálva, mire '
             'vonatkoznak pontosan — személyszámra, vízmennyiségre vagy szerves terhelésre, '
             'mely modellekre és milyen kifolyóvíz-minőség mellett. Amíg ez nincs rendezve, '
             'egy szám közlése félrevezető lenne.'),
            ('Mi történik tartós túlterhelésnél?',
             'A biológiai fokozat nem győzi lebontani a beérkező szerves anyagot, a kilépő '
             'víz minősége romlik, és a szikkasztó is nagyobb terhelést kap — ami annak az '
             'élettartamát is rontja. Ez nem hirtelen meghibásodás, hanem fokozatos romlás, '
             'ezért gyakran későn derül ki.'),
            ('Bővítést tervezünk. Mikor kell szólni?',
             'A tervezéskor. Ha tudható, hogy két-három éven belül bővül a család vagy a '
             'szálláshely, azt a kapacitás megválasztásánál figyelembe vesszük. Utólag '
             'berendezést cserélni lényegesen drágább, mint eleve a bővítéssel számolni.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 4) Szezonális használat
# ===========================================================================
def epit_szezonalis():
    return [
        sec_prose('Nem egyszerűen kevesebb', 'Hosszú szünet, hirtelen csúcs', [
            'A szezonális terhelés nem azt jelenti, hogy „kevesebb szennyvíz”. Azt jelenti, '
            'hogy hosszabb <strong>alacsony vagy nulla</strong> terhelési időszakok '
            'váltakoznak <strong>hirtelen visszatérő csúcsokkal</strong> — és ez a kettő '
            'együtt más feladat, mint a folyamatos, kiegyensúlyozott használat.',
            'Az aktív biológiai rendszer élő baktériumközösséggel dolgozik, amely folyamatos '
            'szervesanyag-utánpótlást igényel. Hosszú szünet után ez a közösség lecsökken, '
            'és a visszatérő terhelést nem azonnal képes kezelni.',
            'Ezért a szezonális használat nemcsak <em>kapacitási</em>, hanem '
            '<em>technológiaválasztási</em> kérdés is: bizonyos használati profiloknál a '
            'passzív, oldómedencés rendszer relevánsabb lehet.',
        ]),

        sec_numbered('A terhelési profil', 'Mit kell rögzíteni?',
                     'Éves átlaglétszámot itt nem érdemes számolni — az elfedi éppen azt, '
                     'ami számít.',
                     ['<strong>Használati hónapok.</strong> Mely hónapokban használják '
                      'egyáltalán az ingatlant.',
                      '<strong>A használat mintája.</strong> Minden hétvégén, csak a '
                      'nyári szezonban, vagy szórványosan.',
                      '<strong>Csúcsszezon hossza és létszáma.</strong> Hány hétig és '
                      'hány fővel.',
                      '<strong>A leghosszabb nulla terhelés.</strong> Ez a legfontosabb '
                      'egyetlen adat ezen az oldalon — ettől függ, milyen üzemmód vagy '
                      'leállítási eljárás szükséges.',
                      '<strong>A visszatérési csúcs.</strong> A szünet után rögtön teljes '
                      'terhelés érkezik, vagy fokozatosan indul a használat.',
                      '<strong>Áramellátás távollét alatt.</strong> Marad-e áram a '
                      'berendezésen, amikor senki nincs ott.']),

        sec_split('Két üzemállapot', 'Rövid és hosszú távollét — nem ugyanaz',
                  'Rövidebb szünet — hétvégi ház jellegű használat',
                  ['A berendezés üzemben marad',
                   'Alulterheléses üzemmód, ahol a vezérlés ezt támogatja',
                   'A baktériumközösség fennmarad',
                   'A visszatérés nem igényel külön beavatkozást',
                   'Az áramellátásnak folyamatosnak kell lennie'],
                  'Hosszú, több hónapos kihagyás',
                  ['A berendezés leállítása jöhet szóba',
                   'Kiürítés és tiszta vízzel való feltöltés',
                   'Tavasszal újbóli beüzemelés szükséges',
                   'A biológia újraindulása időt vesz igénybe',
                   'Ez tervezett eljárás, nem „csak kikapcsoljuk”']),

        hiany('az A.B.Clear jóváhagyott távolléti időtartományai: meddig maradhat a rendszer '
              'alulterheléses üzemben, mikortól kell leállítani, mi a pontos leállítási és '
              'újraindítási eljárás, és mit tud az aktuális vezérlőprogram',
              'ÖkoTech műszaki csapat + aktuális használati útmutató és vezérlőverzió. '
              'A jelenlegi webes tartalom és a GYIK eltérő időtávokról beszél; ezt egységes, '
              'szakmailag jóváhagyott szabályrendszerré kell alakítani, mielőtt a látogató '
              'konkrét hónapszámot lát'),

        sec_prose('Technológiaválasztás', 'Amikor a használati mód dönt, nem a méret', [
            'Ha a használat erősen szakaszos — például kizárólag nyári nyaraló, hosszú téli '
            'kihagyással —, akkor a kérdés már nem az, hogy „hány fős rendszer kell”, hanem '
            'hogy melyik technológia bírja jól ezt a mintát.',
            'Az aktív biológiai rendszer folyamatos működésre készül, és a hosszú szünetet '
            'külön eljárással kezeli. A passzív, oldómedencés rendszer ebből a szempontból '
            'toleránsabb, mert nem élő, aktív iszapközösség folyamatos fenntartásán alapul.',
            'Ez nem azt jelenti, hogy nyaralóba nem való aktív rendszer — hanem azt, hogy a '
            'választásnál a használati profilt is meg kell nézni, nem csak a létszámot.',
        ]),

        sec_cta('Következő lépés', 'Ha vendégeket is fogad',
                ['Ha az ingatlant nem csak a család használja, hanem szálláshelyként is '
                 'működik, a terhelés más logika szerint áll össze: a férőhely, a '
                 'kihasználtság és az esetleges vendéglátás együtt.'],
                'Panziók és vendéglátás', 'panziok-es-vendeglatas',
                alt=('Terhelés és kapacitás', 'terheles-es-kapacitas')),

        sec_faq([
            ('Télen nem használjuk a nyaralót. Mi lesz a rendszerrel?',
             'Több hónapos kihagyásnál tervezett eljárás szükséges — jellemzően leállítás, '
             'kiürítés, tiszta vízzel való feltöltés, majd tavasszal újbóli beüzemelés. '
             'A pontos időhatárokat és a lépéseket a berendezés aktuális használati '
             'útmutatója rögzíti, ezért ezt mindig a konkrét modellre kell egyeztetni.'),
            ('Hétvégi házhoz jó az aktív biológiai rendszer?',
             'Rendszeres hétvégi használatnál igen, ha a vezérlés támogatja az '
             'alulterheléses üzemmódot és marad áram a berendezésen. Ha a használat ennél '
             'szakaszosabb — hosszú, több hónapos szünetekkel —, érdemes a passzív '
             'rendszert is megvizsgálni.'),
            ('Kell áram, amikor nem vagyunk ott?',
             'Az aktív biológiai rendszernél igen: a levegőztetés a baktériumközösség '
             'fenntartásához kell, és ez a távollét alatt is fut, csökkentett üzemben. '
             'Ha az ingatlanon a téli időszakban nincs áram, azt a technológiaválasztásnál '
             'előre jelezni kell.'),
            ('Mennyi idő, míg a rendszer újraindul tavasszal?',
             'A biológia újraindulása időt vesz igénybe — a kilépő víz minősége nem az első '
             'naptól éri el a szokásos szintet. Konkrét időtartamot itt nem közlünk, mert az '
             'a modelltől, a hőmérséklettől és a terheléstől függ; ezt a beüzemelés '
             'dokumentációja rögzíti.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 5) Panziók és vendéglátás
# ===========================================================================
def epit_panzio():
    return [
        sec_prose('A férőhely nem terhelés', 'Amiből valóban összeáll', [
            'Panzió vagy vendéglátóhely méretezésénél a névleges férőhelyszám nem azonos a '
            'szennyvíztisztító tényleges terhelésével. Egy húszférőhelyes panzió éves '
            'átlagban működhet nyolc vendéggel és három csúcshétvégén húsz fővel — a kettő '
            'egészen más rendszert kíván.',
            'A terhelési profilhoz ezért a férőhely mellett szükséges az éves '
            '<strong>kihasználtság</strong>, a <strong>csúcsidőszakok</strong>, a '
            '<strong>nyitvatartás</strong>, a <strong>személyzet</strong>, valamint a '
            'mosoda, a wellness és az esetleges vendéglátás vízhasználata.',
        ]),

        sec_split('Két külön szennyvízáram', 'Amit nem szabad egybevenni',
                  'Kommunális — a vendégek szennyvize',
                  ['Fürdőszoba, WC, kézmosó',
                   'Összetétele a háztartásihoz hasonló',
                   'A kihasználtsággal arányosan változik',
                   'Reggeli és esti hidraulikai csúcsokkal',
                   'Ez a szokásos biológiai tisztítás feladata'],
                  'Konyhai — a vendéglátás használt vize',
                  ['Mosogatás, előkészítés, takarítás',
                   'Magasabb szerves-, zsír- és olajterhelés',
                   'Nem a vendégszámmal, hanem az étkezésszámmal arányos',
                   'Rövid, intenzív csúcsokkal a konyha üzemideje szerint',
                   'ELŐKEZELÉST igényelhet — zsírleválasztást']),

        sec_numbered('Amit meg kell adni', 'A szálláshelyi terhelési profil', '',
                     ['<strong>Férőhely és átlagos éves kihasználtság.</strong> A kettő '
                      'együtt adja a reális átlagot; a férőhely önmagában a maximumot mutatja.',
                      '<strong>Csúcsidőszakok.</strong> Mikor telt ház, mennyi ideig, és '
                      'évente hányszor. Balatoni panziónál ez néhány hét, városiban '
                      'rendezvényekhez kötött.',
                      '<strong>Nyitvatartási napok.</strong> Egész évben vagy szezonálisan '
                      'üzemel. Ha szezonálisan, a szezonális használat oldala is releváns.',
                      '<strong>Személyzet létszáma.</strong> Ők is terhelést jelentenek, '
                      'jellemzően a nyitvatartás teljes idejében.',
                      '<strong>Étkeztetés.</strong> Csak reggeli, vagy teljes étterem. '
                      'A napi étkezésszám és a konyha üzemideje.',
                      '<strong>Mosoda.</strong> Helyben mosnak, vagy külső szolgáltató. '
                      'A saját mosoda jelentős, koncentrált vízhasználat.',
                      '<strong>Wellness.</strong> Medence, jacuzzi, szauna. A '
                      'medencevíz-csere külön, nagy egyszeri vízmennyiség.',
                      '<strong>Rendezvények.</strong> Esküvő, konferencia — rövid, nagyon '
                      'nagy csúcs, amely nem a szállásvendégekből ered.']),

        sec_prose('A konyha külön kérdés', 'Nem oldható meg „vendégszám × liter” módszerrel', [
            'A vendéglátásból származó szennyvíz zsír- és olajterhelése eltér a háztartásitól, '
            'és ez a biológiai fokozat működését közvetlenül befolyásolja. Nagyobb konyhai '
            'terhelésnél a technológia zsírfogó kamrával egészíthető ki — de hogy ez mikor '
            'szükséges, azt a konkrét üzemből kell levezetni.',
            'A 220/2004. Korm. rendelet a termelési és szolgáltatási tevékenységből származó '
            'szennyvíznél technológiai és üzemelési adatokat is releváns bemenetként kezel. '
            'Ez a gyakorlatban azt jelenti, hogy a nagykonyhás projekt nem méretezhető '
            'egyszerű „vendégszám × liter/fő” módszerrel.',
            'Ahol a konyhai terhelés jelentős, ott a laboradat és az előkezelés kérdése '
            'korán belép — érdemes ezzel számolni, nem a projekt végén szembesülni vele.',
        ]),

        hiany('panziók tényleges férőhely–vízfogyasztás adatai, szezonális kihasználtsági '
              'profilok, éttermes és étterem nélküli szálláshelyek terhelési különbsége, '
              'az alkalmazott konyhai előkezelő konfigurációk, valamint hogy mekkora '
              'konyhai terheléstől kötelező a zsírleválasztás',
              'ÖkoTech megvalósult panzió- és vendéglátóipari projektek + kifolyóvíz '
              'laboreredmények. Amíg ez nincs meg, konkrét kapacitási küszöb nem közölhető'),

        sec_cta('Következő lépés', 'Intézménynél megint más a logika',
                ['Ha iskoláról, óvodáról, irodáról vagy más közösségi intézményről van szó, '
                 'a névleges létszám mellett a jelenléti idő és az éves üzemnapok a '
                 'meghatározók.'],
                'Intézményi terhelés', 'intezmenyi-terheles',
                alt=('Terhelés és kapacitás', 'terheles-es-kapacitas')),

        sec_faq([
            ('Húsz férőhelyes a panzióm. Húsz fős rendszer kell?',
             'Nem feltétlenül — valószínűleg nem. A férőhely a maximumot mutatja, a '
             'méretezés viszont az átlagos kihasználtságból és a rendszeres csúcsokból '
             'indul. Adja meg az éves kihasználtságot és a csúcshétvégék számát, és abból '
             'lényegesen pontosabb kép áll össze.'),
            ('Van éttermünk is. Az mit változtat?',
             'Sokat. A konyhai szennyvíz zsír- és szervesanyag-terhelése eltér a '
             'háztartásitól, és előkezelést — jellemzően zsírleválasztást — igényelhet. '
             'A méretezéshez a napi étkezésszám és a konyha üzemideje kell, nem a '
             'vendégéjszaka.'),
            ('Rendezvényeket is tartunk. Erre méretezzünk?',
             'A rendezvény rövid, nagyon nagy csúcs, amit jellemzően nem érdemes a '
             'berendezés méretével kezelni — az az év többi napján túlméretezést jelentene. '
             'Adja meg a gyakoriságot és a nagyságrendet, és megnézzük, mi a helyes '
             'megközelítés az adott esetben.'),
            ('Kell laborvizsgálat?',
             'Szálláshelynél a kommunális jellegű terhelés jellemzően jól becsülhető. Ahol '
             'jelentős konyhai vagy egyéb technológiai terhelés is van, ott a laboradat '
             'gyakran elkerülhetetlen — enélkül a méretezés feltételezésen alapulna.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 6) Intézményi terhelés
# ===========================================================================
def epit_intezmeny():
    return [
        sec_prose('A névleges létszám félrevezető', 'A „300 fős” iskola nem 300 LE', [
            'Egy intézmény „300 fős” megnevezése önmagában nem elegendő a méretezéshez, mert '
            'a 300 fő nem feltétlenül egyszerre, nem egész nap és nem egész évben használja '
            'a létesítményt.',
            'Egy iskolánál a hétköznapi reggel–délután terhelés, a hétvégi minimális '
            'használat, a tanítási szünetek és a nagykonyha egészen különböző hidraulikai és '
            'biológiai állapotokat eredményeznek. Az éves átlag ezt elfedi, a névleges '
            'létszám pedig eltúlozza.',
            'A méretezéshez ezért a létszám mellett a <strong>jelenléti idő</strong>, a '
            '<strong>nyitvatartás</strong>, a tényleges <strong>vízfogyasztás</strong>, az '
            '<strong>étkeztetés</strong> és a <strong>szezonális zárás</strong> is kell.',
        ]),

        sec_numbered('A működési profil', 'Amit meg kell adni', '',
                     ['<strong>Intézménytípus.</strong> Iskola, óvoda, iroda, szociális '
                      'intézmény, sportlétesítmény — a napi ritmusuk alapvetően eltér.',
                      '<strong>Névleges és tényleges létszám.</strong> Hányan vannak '
                      'nyilvántartva, és jellemzően hányan vannak jelen.',
                      '<strong>Jelenléti idő.</strong> Hány órát töltenek bent. A négy órát '
                      'bent töltő óvodás nem ugyanaz a terhelés, mint egy bentlakó.',
                      '<strong>Hétköznap és hétvége.</strong> Van-e hétvégi használat, és '
                      'milyen mértékű.',
                      '<strong>Éves üzemnapok és szünetek.</strong> Nyári zárás, téli '
                      'szünet — ezek hosszú alulterhelési időszakok.',
                      '<strong>Tényleges vízfogyasztás.</strong> Meglévő intézménynél ez '
                      'megvan, és lényegesen pontosabb minden becslésnél.',
                      '<strong>Nagykonyha.</strong> Van-e főzőkonyha, hány adag, milyen '
                      'üzemidőben.',
                      '<strong>Sport, rendezvény, bentlakás.</strong> Tornaterem zuhanyzóval, '
                      'esti rendezvények, kollégium — mind külön terhelési ablak.']),

        sec_split('Két különböző napi ritmus', 'Példa a különbségre',
                  'Iskola nagykonyha nélkül',
                  ['Terhelés hétköznap reggel 8 és délután 4 között',
                   'Hétvégén és szünetben közel nulla',
                   'Jellemzően kommunális összetételű szennyvíz',
                   'A csúcs a szünetekhez igazodik — óránként ismétlődő hullámok',
                   'Éves szinten jelentős alulterhelési időszakokkal'],
                  'Iskola főzőkonyhával',
                  ['Ugyanaz a kommunális terhelés, plusz konyhai',
                   'A konyhai csúcs 10 és 14 óra között koncentrálódik',
                   'Magasabb zsír- és szervesanyag-terhelés',
                   'Előkezelés — zsírleválasztás — válhat szükségessé',
                   'A konyha a szünetekben is működhet, ha van napközi vagy tábor']),

        sec_prose('Az 50 LE feletti sáv', 'Ahol a kérdés már nem csak kapacitás', [
            'Az 50 LE feletti tartományban a projekt már nem a 147/2010. Korm. rendelet '
            'szerinti egyszerű egyedi szennyvíztisztítás kategóriája. Ezért a kapacitás '
            'mellett az <strong>engedélyezési</strong> és <strong>üzemeltetési modell</strong> '
            'is korán relevánssá válik.',
            'Ilyenkor a méretezés jogosult tervező feladata, a kibocsátási követelmények és '
            'a monitoring kérdése belép, és az üzemeltetői felelősség is más — nem a '
            'tulajdonos alkalmi figyelme, hanem rendszeres, dokumentált üzemeltetés.',
            'Ez nem bonyolultabbá teszi a projektet, hanem más útra állítja. Érdemes ezt '
            'korán tisztázni, mert a tervezési és engedélyezési átfutás is más.',
        ]),

        hiany('iskolai és intézményi ÖkoTech-referenciák: névleges létszám és valós '
              'vízfogyasztás összevetése, szüneti működési tapasztalat, konyhás intézményi '
              'rendszerek konfigurációja, monitoring- és laboradat, hosszú távú szervizadat',
              'ÖkoTech megvalósult intézményi projektek. Ezek nélkül a látogató nem tud '
              'viszonyítani, és a méretezés is feltételezésen alapul'),

        sec_cta('Következő lépés', 'Ha technológiai szennyvíz is keletkezik',
                ['Ha az intézményben vagy a telephelyen nem csak kommunális jellegű '
                 'szennyvíz keletkezik, a méretezés más logikát követ: ott a gyártási '
                 'technológia és a laboradat a kiindulás.'],
                'Speciális vagy ipari szennyvíz', 'specialis-vagy-ipari-szennyviz',
                alt=('Terhelés és kapacitás', 'terheles-es-kapacitas')),

        sec_faq([
            ('Az iskola 300 fős. Milyen rendszer kell?',
             'Ebből az egy adatból nem megállapítható. Kell hozzá a tényleges napi jelenlét, '
             'a bent töltött idő, az éves üzemnapok, a szünetek és az, hogy van-e '
             'főzőkonyha. Meglévő intézménynél a vízfogyasztás mindezt jól közelíti — azzal '
             'érdemes kezdeni.'),
            ('Mi történik a nyári szünetben?',
             'Hosszú alulterhelési időszak keletkezik, amit kezelni kell. Ez üzemmód- és '
             'technológiaválasztási kérdés, és a méretezésnél is számít: nem lehet csak a '
             'tanítási időszak terhelésére tervezni, a szüneti állapotot is bírnia kell a '
             'rendszernek.'),
            ('A nagykonyha beleszámít a létszámba?',
             'Nem így kell kezelni. A konyhai terhelés nem olvasztható be egyszerűen '
             'személyegyenértékbe: eltérő az összetétele, más az időbeli eloszlása, és '
             'előkezelést igényelhet. Külön adatként kell megadni: napi adagszám és a konyha '
             'üzemideje.'),
            ('Ki üzemelteti majd a rendszert?',
             'Intézményi méretben ez önálló kérdés, nem melléktevékenység. Nagyobb '
             'kapacitásnál rendszeres, dokumentált üzemeltetés és jellemzően monitoring is '
             'szükséges. Érdemes már a tervezéskor eldönteni, hogy ez saját '
             'munkatárssal vagy szolgáltatóval oldható meg.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 7) Speciális vagy ipari szennyvíz
# ===========================================================================
def epit_ipari():
    return [
        sec_prose('Az alapkérdés', 'Ötven ember vagy ötven fős üzem?', [
            'Egy üzemben dolgozó ötven ember kommunális szennyvize és egy ötven fős üzem '
            'termeléséből származó technológiai szennyvíz <strong>nem ugyanaz a méretezési '
            'feladat</strong> — még akkor sem, ha a létszám azonos.',
            'A kommunális szennyvíz összetétele nagyjából kiszámítható. A technológiai '
            'szennyvíz összetételét viszont a gyártási folyamat határozza meg: egy borászat, '
            'egy tejüzem és egy vágóhíd szennyvize egymástól is gyökeresen eltér.',
            'Ezért az „ipari szennyvíz” nem egyetlen egységes kategória, és nem méretezhető '
            'személyszám alapján. Itt a kiindulás a technológia és a laboradat.',
        ]),

        sec_numbered('Amit tudni kell', 'A technológiai adatok', '',
                     ['<strong>A két szennyvízáram szétválasztása.</strong> Mennyi a '
                      'szociális (kommunális) és mennyi a technológiai eredetű. Sok esetben '
                      'ezek külön is kezelhetők — és ez a legolcsóbb megoldás.',
                      '<strong>A gyártástechnológia.</strong> Mi készül, milyen '
                      'folyamatokkal, milyen alap- és segédanyagokból.',
                      '<strong>Munkarend.</strong> Hány műszak, heti hány nap, éves hány '
                      'üzemnap.',
                      '<strong>Idényjelleg.</strong> A borászat szüret idején egészen mást '
                      'termel, mint télen. Az idényjelleg a csúcsterhelést határozza meg.',
                      '<strong>Vízhozam.</strong> Átlagos és maximális m³/nap, valamint az '
                      'órás vagy műszakonkénti csúcs.',
                      '<strong>Laborparaméterek.</strong> BOI5, KOI, lebegőanyag, és '
                      'iparágtól függően zsír/olaj, nitrogén, foszfor, pH, hőmérséklet. '
                      'A pontos listát mindig a technológia határozza meg.',
                      '<strong>Meglévő előkezelés.</strong> Van-e már zsírfogó, rács, '
                      'ülepítő, kiegyenlítő medence.']),

        sec_split('A két út', 'Mi következik az adatokból',
                  'Kommunális jellegű ág',
                  ['A szennyvíz összetétele háztartásihoz hasonló',
                   'A technológiai áram elkülöníthető vagy elhanyagolható',
                   'A szokásos biológiai tisztítás alkalmazható',
                   'A méretezés a létszámból és a vízfogyasztásból indul',
                   'Laborvizsgálat jellemzően nem előfeltétel'],
                  'Technológiai ág',
                  ['A gyártásból eredő terhelés meghatározó',
                   'Mintavétel és laborvizsgálat szükséges',
                   'Előkezelés és kiegyenlítés vizsgálandó',
                   'Iparág-specifikus kibocsátási határértékek élnek',
                   'Egyedi mérnöki tervezés, nem katalógusméret']),

        sec_prose('Amit nem vállalunk sablonból', 'Miért nincs itt kapacitástáblázat', [
            'A jelenlegi ÖkoTech-tartalom vágóhídi, tejüzemi és borászati szennyvíz '
            'biológiai tisztítását is megoldhatóként említi. Ez a szakmai képesség létezhet, '
            'de a weboldalon nem lehet belőle automatikus méretezés — mert a bemeneti '
            'vízminőség és a szükséges előkezelés projektenként más.',
            'Ezért ezen az oldalon nincs kapacitástáblázat és nincs modellajánlás. Ami van: '
            'a szükséges adatok listája, és a megvalósíthatósági vizsgálat útja. Ha '
            'laboradat nincs, az első lépés a mintavétel — nem az ajánlat.',
            'Ez nem óvatoskodás. Egy rosszul méretezett ipari rendszer nem a beruházó '
            'pénzét pazarolja el először, hanem a kibocsátási követelmények teljesítését '
            'teszi lehetetlenné — és azt utólag lényegesen nehezebb korrigálni.',
        ]),

        hiany('az ÖkoTech tényleges ipari referenciái: vágóhídi, tejüzemi és borászati '
              'projektek befolyó és kifolyó laboreredményekkel, az alkalmazott előkezelés, '
              'a névleges és csúcsterhelés, a működési időtáv — és külön: mit NEM vállal '
              'az ÖkoTech',
              'ÖkoTech mérnöki csapat. Az iparági hitelesség kizárólag megvalósult '
              'projekten és laboradaton alapulhat; enélkül ez az oldal a folyamatot írja '
              'le, nem a képességet'),

        sec_cta('Következő lépés', 'Kezdjük a technológiával',
                ['Írja meg, mi a tevékenység, hány műszakban, milyen éves ritmusban, és '
                 'hogy van-e már laboreredmény. Ebből meg tudjuk mondani, elegendő-e a '
                 'meglévő adat a megvalósíthatósági vizsgálathoz, vagy mintavétellel kell '
                 'kezdeni.'],
                'Kapcsolatfelvétel', '../kapcsolat',
                alt=('Mikor szükséges szakértő?', 'mikor-szukseges-szakerto')),

        sec_faq([
            ('Nincs laboreredményünk. Így is lehet ajánlatot kérni?',
             'Ajánlatot felelősen nem, megvalósíthatósági egyeztetést viszont igen. '
             'A technológia, a munkarend és a vízhozam alapján meg tudjuk mondani, milyen '
             'vizsgálat szükséges és milyen nagyságrendről van szó. A méretezéshez viszont '
             'a laboradat elkerülhetetlen.'),
            ('Szétválasztható a szociális és a technológiai szennyvíz?',
             'Sok üzemben igen, és gyakran ez a legolcsóbb megoldás: a kommunális ág a '
             'szokásos módon kezelhető, a technológiai pedig külön előkezelést kap. '
             'Érdemes ezt már a tervezéskor megvizsgálni.'),
            ('Milyen laborparaméterek kellenek?',
             'A minimum jellemzően BOI5, KOI és lebegőanyag; ezen felül iparágtól függően '
             'zsír és olaj, nitrogén, foszfor, pH és hőmérséklet. A pontos listát a '
             'technológia határozza meg — ezért kérdezünk rá először a gyártási folyamatra.'),
            ('Van olyan, amit nem vállalnak?',
             'Igen, és ezt előre megmondjuk. Vannak technológiai szennyvizek, amelyek '
             'biológiai úton nem vagy csak jelentős előkezeléssel kezelhetők. Ha ez a '
             'helyzet, azt a megvalósíthatósági vizsgálat során jelezzük — nem az ajánlat '
             'után.'),
        ]),
        JOGI,
    ]


# ===========================================================================
# 8) Terhelési profil és kapacitás-előminősítő
# ===========================================================================
def epit_eloszuro():
    return [
        sec_prose('Mi ez, és mi nem', 'Terhelési profil, nem árkalkulátor', [
            'Ez a modul a megadott használati adatokból strukturált <strong>terhelési '
            'profilt</strong> állít össze, és eldönti, hogy standard kapacitási tartomány '
            'becsülhető-e, vagy további mérés, laborvizsgálat, illetve szakértő szükséges.',
            'Amit <strong>nem</strong> ad: konkrét árat, garantált kapacitást hiányos '
            'adatokból, automatikus ipari méretezést és jogi engedélyezhetőségi ígéretet.',
            'A kemény termék- és méretezési szabályok jóváhagyott adatbázisból származnak. '
            'Generatív modell legfeljebb a szabad szöveg, a számlaadatok vagy a feltöltött '
            'dokumentum strukturálásában segít — a szükséges kapacitást nem ő találja ki.',
        ]),

        sec_numbered('A menet', 'Először a projekt típusa',
                     'Mert családi háznál, nyaralónál, panziónál, intézménynél és ipari '
                     'projektnél más kérdésekből áll össze a használható profil.',
                     ['<strong>Lakossági.</strong> Állandó létszám, vízfogyasztás, '
                      'vendégcsúcs, távollét, tervezett bővítés.',
                      '<strong>Szezonális.</strong> Ugyanez, plusz a használati hónapok, a '
                      'leghosszabb nulla terhelés és a visszatérési csúcs.',
                      '<strong>Panzió, vendéglátás.</strong> Férőhely, kihasználtság, '
                      'szezon, étkeztetés, mosoda, wellness, rendezvények.',
                      '<strong>Intézmény.</strong> Névleges és tényleges jelenlét, '
                      'jelenléti idő, nyitvatartás, szünetek, konyha, vízfogyasztás.',
                      '<strong>Ipari vagy speciális.</strong> Technológia, munkarend, '
                      'm³/nap, laboradat, meglévő előkezelés — itt a modul nem méretez, '
                      'hanem szakértői ágra irányít.']),

        sec_split('A kimenet', 'Amit külön jelöl',
                  'Terhelési adatok',
                  ['Hidraulikai átlag — napi vízmennyiség',
                   'Hidraulikai csúcs — rövid idő alatt beérkező mennyiség',
                   'Szerves terhelés, ahol megalapozottan becsülhető',
                   'Rövid túlterhelés: nagysága, időtartama, gyakorisága',
                   'Tartós túlterhelés, ha van',
                   'Alulterhelési időszakok hossza'],
                  'Következtetés',
                  ['Becsült kapacitási tartomány, ahol megalapozott',
                   'LE-kategória, ahol az adat ezt megengedi',
                   'A hiányzó adatok listája',
                   'Szakértői eszkaláció, ha indokolt',
                   '50 LE feletti ág, ha a terhelés ezt jelzi',
                   'Laborigény, ha a szennyvíz nem kommunális jellegű']),

        sec_numbered('A lehetséges eredmények', 'Négy kimenet, négy különböző út', '',
                     ['<strong>Standard lakossági kapacitástartomány.</strong> Az adatok '
                      'elegendők, a terhelés a szokásos sávban van. A tervezés folytatható.',
                      '<strong>Határhelyzet — szakértői ellenőrzés.</strong> A terhelés a '
                      'kategóriahatár közelében van, vagy a szórás szokatlanul nagy. Emberi '
                      'ellenőrzés következik.',
                      '<strong>50 LE feletti ág.</strong> A projekt kikerül az egyedi '
                      'szennyvíztisztítás kategóriájából; más tervezési és engedélyezési '
                      'úton halad.',
                      '<strong>Speciális szennyvíz — labor és mérnöki vizsgálat.</strong> '
                      'A terhelés nem kommunális jellegű. Mintavétel és megvalósíthatósági '
                      'vizsgálat következik, nem kapacitásbecslés.']),

        hiany('maga a szabálymotor: a teljes modell–terhelés adatbázis, a hidraulikai és '
              'BOI5 névleges értékek modellenként, a rövid és tartós túlterhelési szabályok, '
              'az alulterhelési szabályok, az 50–100 LE közötti projektút, a panzió- és '
              'intézményi méretezési szabály, valamint az ipari eszkaláció feltételei',
              'ÖkoTech műszaki workshop, majd legalább 100–200 korábbi projekt '
              'visszatesztelése — külön vizsgálva, hol tért el az ajánlott és a végül '
              'telepített modell. A modul addig nem kapcsolható élesre'),

        sec_cta('Addig is', 'Vegyük végig együtt',
                ['Amíg az előminősítő nem üzemel, ugyanezt élőben végigvesszük. Írja meg a '
                 'projekt típusát, a létszámot vagy a férőhelyet, a használat módját és — ha '
                 'van — az éves vízfogyasztást.',
                 'Ha van vízszámlája, laboreredménye vagy korábbi terv, csatolja: azokkal '
                 'lényegesen gyorsabban jutunk kapacitási irányig.'],
                'Kapcsolatfelvétel', '../kapcsolat',
                alt=('Terhelés és kapacitás', 'terheles-es-kapacitas')),

        sec_faq([
            ('Kapok konkrét berendezésmodellt a végén?',
             'Kapacitási tartományt igen, konkrét modellt nem. A végleges modellválasztás a '
             'telek adottságait, a vízelhelyezést és a telepítési körülményeket is figyelembe '
             'veszi — ezek nem ebből a modulból jönnek.'),
            ('Miért nem ad árat?',
             'Mert a beruházási költséget nem csak a kapacitás határozza meg: a telepítési '
             'körülmények, a szükséges kiegészítők, a vízelhelyezés kialakítása és a '
             'földmunka is befolyásolja. Kapacitásból árat becsülni félrevezető lenne.'),
            ('Elmenthető az eredmény?',
             'Igen, a kimenet menthető terhelési brief: a profil, a becsült kapacitási '
             'tartomány, a hiányzó adatok és a javasolt következő lépés. Ez közvetlenül '
             'felhasználható a telekalkalmassági és a műszaki egyeztetéshez.'),
        ]),
        JOGI,
    ]


# ===========================================================================
OLDALAK = [
    dict(file='projekt-elokeszites/terheles-es-kapacitas.html',
         url='projekt-elokeszites/terheles-es-kapacitas', img='vallalkozas',
         title='Terhelés és kapacitás — mekkora rendszer kell valójában | ÖkoTech Home',
         desc='A „hány fő?” csak az első kérdés. Vízmennyiség, szerves terhelés, csúcsok és '
              'időbeli eloszlás — ebből áll össze a terhelési profil.',
         h1='Terhelés és kapacitás',
         alt='Vízóra és számlálókerék közelről, mögötte elmosódott gépészeti szerelvények',
         lead='A szükséges kapacitás nem a létszámból következik. A vízmennyiség, a szerves '
              'terhelés és a használat időbeli eloszlása együtt dönt — a létszám csak a '
              'belépő kérdés.',
         crumbs=CRUMB, sections=epit_hub()),

    dict(file='projekt-elokeszites/lakosegyenertek.html',
         url='projekt-elokeszites/lakosegyenertek', img='attekintes',
         title='Lakosegyenérték (LE) — mit jelent, és mit nem | ÖkoTech Home',
         desc='1 LE = napi 60 g BOI5 szerves terhelés — nem személy és nem liter. Miért '
              'fontos a különbség, és mikor elég helyette a személyszám.',
         h1='Lakosegyenérték',
         alt='Laboratóriumi lombikok és mérőhenger egy világos asztalon, mellett jegyzetlap '
             'számításokkal',
         lead='A leggyakrabban félreértett fogalom ezen a területen — és a félreértés '
              'konkrét méretezési hibához vezet. Az LE nem egy ember, és nem is liter.',
         crumbs=HUB, sections=epit_le()),

    dict(file='projekt-elokeszites/szemelyszam-es-vizfogyasztas.html',
         url='projekt-elokeszites/szemelyszam-es-vizfogyasztas', img='csaladi-haz',
         title='Személyszám és vízfogyasztás — hogyan lesz belőle adat | ÖkoTech Home',
         desc='A létszám jó kiindulás, a vízszámla pontosabb. Hogyan számoljon napi átlagot, '
              'mit vonjon le belőle, és mit jelezzen külön.',
         h1='Személyszám és vízfogyasztás',
         alt='Vízszámla és számológép egy konyhaasztalon, mellette toll és jegyzetfüzet',
         lead='Családi háznál a lakók száma jó első közelítés — de a tényleges vízhasználat '
              'pontosabb, és jellemzően már rendelkezésre áll.',
         crumbs=HUB, sections=epit_szemelyszam()),

    dict(file='projekt-elokeszites/atlag-es-csucsterheles.html',
         url='projekt-elokeszites/atlag-es-csucsterheles', img='biologiai',
         title='Átlag- és csúcsterhelés — mire méretezzünk | ÖkoTech Home',
         desc='A rövid vendégcsúcs és a tartós túlterhelés nem ugyanaz, és az alulterhelés '
              'is külön üzemállapot. Négy adat kell, nem egy.',
         h1='Átlag- és csúcsterhelés',
         alt='Levegőztetett biológiai medence felszíne közelről, buborékokkal és örvénylő '
             'vízfelülettel',
         lead='Nem a maximumra méretezünk, de a rendszeres csúcsot nem hagyjuk figyelmen '
              'kívül. A méretezéshez négy adat kell: átlag, csúcs, időtartam és gyakoriság.',
         crumbs=HUB, sections=epit_csucs()),

    dict(file='projekt-elokeszites/szezonalis-hasznalat.html',
         url='projekt-elokeszites/szezonalis-hasznalat', img='nyaralo',
         title='Szezonális használat — hosszú szünet, hirtelen csúcs | ÖkoTech Home',
         desc='Nem egyszerűen kevesebb szennyvíz. Használati hónapok, leghosszabb nulla '
              'terhelés, visszatérési csúcs — és mikor számít a technológiaválasztás.',
         h1='Szezonális használat',
         alt='Zárt nyaraló télen, behavazott kert és leengedett redőnyök',
         lead='A szezonális terhelés nem kevesebb szennyvizet jelent, hanem hosszú szüneteket '
              'és hirtelen visszatérő csúcsokat. Ez nemcsak kapacitási kérdés.',
         crumbs=HUB, sections=epit_szezonalis()),

    dict(file='projekt-elokeszites/panziok-es-vendeglatas.html',
         url='projekt-elokeszites/panziok-es-vendeglatas', img='telepek',
         title='Panziók és vendéglátás — a férőhely nem terhelés | ÖkoTech Home',
         desc='Kihasználtság, szezon, konyha, mosoda, rendezvények. Miért nem méretezhető a '
              'vendéglátás „vendégszám × liter” módszerrel.',
         h1='Panziók és vendéglátás',
         alt='Panzió reggeliző terasza megterített asztalokkal, háttérben a szálláshely '
             'épülete',
         lead='Egy húszférőhelyes panzió éves átlagban működhet nyolc vendéggel és három '
              'csúcshétvégén húsz fővel. A két szám más rendszert kíván.',
         crumbs=HUB, sections=epit_panzio()),

    dict(file='projekt-elokeszites/intezmenyi-terheles.html',
         url='projekt-elokeszites/intezmenyi-terheles', img='kozcsatorna',
         title='Intézményi terhelés — a „300 fős” iskola nem 300 LE | ÖkoTech Home',
         desc='Jelenléti idő, nyitvatartás, szünetek és nagykonyha. Miért félrevezető a '
              'névleges létszám, és mi változik 50 LE fölött.',
         h1='Intézményi terhelés',
         alt='Iskolai folyosó szünetben, mosdóhelyiség bejáratával és nyitott ablakokkal',
         lead='A 300 fő nem egyszerre, nem egész nap és nem egész évben használja a '
              'létesítményt. A névleges létszám a méretezéshez önmagában félrevezető.',
         crumbs=HUB, sections=epit_intezmeny()),

    dict(file='projekt-elokeszites/specialis-vagy-ipari-szennyviz.html',
         url='projekt-elokeszites/specialis-vagy-ipari-szennyviz', img='alternativak',
         title='Speciális vagy ipari szennyvíz — technológia és laboradat | ÖkoTech Home',
         desc='Az üzemben dolgozó 50 ember és az 50 fős üzem technológiai szennyvize nem '
              'ugyanaz a feladat. Milyen adat kell, és miért nincs itt kapacitástáblázat.',
         h1='Speciális vagy ipari szennyvíz',
         alt='Ipari csarnok gépészeti vezetékekkel és rozsdamentes tartályokkal',
         lead='Az „ipari szennyvíz” nem egyetlen kategória, és nem méretezhető '
              'személyszámból. Itt a gyártástechnológia és a laboradat a kiindulás.',
         crumbs=HUB, sections=epit_ipari()),

    dict(file='projekt-elokeszites/terhelesi-profil-eloszuro.html',
         url='projekt-elokeszites/terhelesi-profil-eloszuro', img='mar-van-rendszerem',
         title='Terhelési profil és kapacitás-előminősítő | ÖkoTech Home',
         desc='Strukturált terhelési profil a használati adatokból: átlag, csúcs, '
              'bizonytalanságok, és hogy becsülhető-e standard kapacitástartomány.',
         h1='Terhelési profil és kapacitás-előminősítő',
         alt='Táblagép a kezekben, képernyőjén használati adatokat bekérő űrlappal',
         lead='Terhelési profilt állít össze, nem árat számol. Megmondja, becsülhető-e '
              'standard kapacitástartomány, vagy mérés, labor, illetve szakértő szükséges.',
         crumbs=HUB, sections=epit_eloszuro()),
]

if __name__ == '__main__':
    (WEB / 'projekt-elokeszites').mkdir(exist_ok=True)
    for o in OLDALAK:
        out = WEB / o['file']
        out.write_text(G.build(o), encoding='utf-8')
        print(f"  {o['file']:60s} {len(out.read_text(encoding='utf-8'))//1024} KB")
