<?php
/**
 * kalauz.php — Öko, a kísérő segéd válaszai.
 * ---------------------------------------------------------------------------
 * A látogató kérdést tesz fel; a válasz két részből áll:
 *   · rövid, emberi mondat — mit tudunk a kérdésről,
 *   · és a TALÁLATOK: melyik lapon, melyik szakaszban van a válasz.
 *
 * A találatokat nem a modell találja ki, hanem a tartalomindexből választja:
 * a séma csak létező URL-t fogad el, és a végpont ezt még egyszer ellenőrzi.
 * Így Öko nem tud nem létező oldalra küldeni — ez a legfontosabb korlát, mert
 * egy kitalált hivatkozás rosszabb, mint a „nem tudom".
 *
 * AMIT NEM CSINÁL: nem ad műszaki tanácsot, nem méretez, nem mond árat és nem
 * ígér határidőt. Ezek a konzultáció dolgai — a system prompt ezt tiltja, és a
 * válasz hossza is korlátozott, hogy ne csússzon szaktanácsadásba.
 *
 * Az index a `kalauz-index.json` (scripts/kalauz-index.py készíti a kiadott
 * lapokból). Ha hiányzik, a végpont szól — üres indexszel a keresésnek nincs
 * értelme, és ezt jobb megmondani, mint találgatni.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';
require __DIR__ . '/lib/ai.php';

OthVedelem::sebessegkorlat('kalauz', 30, 60);

$kerdes = OthVedelem::szoveg($BE, 'kerdes', 300);
$mod    = OthVedelem::szoveg($BE, 'mod', 20);

/* Urlap módban a kliens azt is elküldi, HÁNYADIK lapon áll a látogató. Ettől
   a válasz nem általánosság lesz, hanem az éppen nyitott kérdésekhez szól. */
$lepes = (int) ($BE['lepes'] ?? 0);
if ($lepes < 1 || $lepes > 6) { $lepes = 0; }

/* A párbeszéd eddigi menete. Enélkül Öko minden kérdést nulláról kezdene, és
   a látogatónak újra el kellene mondania, amit már elmondott — ettől érződött
   a segéd gépnek. Legfeljebb hat forduló megy vissza: ennél többet a kérdés
   megválaszolásához úgysem használ, a promptot viszont hízlalná. */
$elozmeny = '';
foreach (array_slice((array) ($BE['elozmeny'] ?? []), -6) as $sor) {
    $kitol = (($sor['kitol'] ?? '') === 'en') ? 'Látogató' : 'Öko';
    $szoveg = mb_substr(OthSmtp::tisztit((string) ($sor['szoveg'] ?? '')), 0, 400);
    if ($szoveg !== '') { $elozmeny .= $kitol . ': ' . $szoveg . "\n"; }
}
if (mb_strlen($kerdes) < 3) {
    OthVedelem::valasz(422, ['ok' => false, 'uzenet' => 'Írja le, mit keres.']);
}
if (!in_array($mod, ['kalauz', 'urlap', 'jelentes'], true)) { $mod = 'kalauz'; }

/* --- tartalomindex --------------------------------------------------------- */
$indexFajl = __DIR__ . '/kalauz-index.json';
$index = is_readable($indexFajl) ? json_decode((string) file_get_contents($indexFajl), true) : null;
$lapok = is_array($index['lapok'] ?? null) ? $index['lapok'] : [];
if (!$lapok) {
    error_log('OTH kalauz: hiányzik vagy üres a kalauz-index.json');
    OthVedelem::valasz(503, ['ok' => false,
        'uzenet' => 'A kereső most nem érhető el. A menüben a Tudástár alatt megtalálja a témákat.']);
}

/* Az érvényes URL-ek halmaza: ezen kívülre Öko nem küldhet. */
$ervenyes = [];
foreach ($lapok as $l) { $ervenyes[$l['url']] = $l; }

/* A teljes index minden kérdéshez sok volna, ezért előszűrünk szavakra. A
   szűrés nagyvonalú: inkább menjen be fölösleges lap, mint hogy a jó kimaradjon
   — a válogatás úgyis a modell dolga. */
$szavak = preg_split('/[^\p{L}\p{N}]+/u', mb_strtolower($kerdes), -1, PREG_SPLIT_NO_EMPTY) ?: [];
$szavak = array_filter($szavak, static fn($sz) => mb_strlen($sz) >= 4);

$pontozott = [];
foreach ($lapok as $l) {
    $halom = mb_strtolower($l['cim'] . ' ' . $l['leiras'] . ' '
        . implode(' ', array_column($l['szakaszok'] ?? [], 'cim')));
    $pont = 0;
    foreach ($szavak as $sz) {
        /* Tőcsonkolás magyarra: a teljes szó helyett az első hat betű, mert a
           „telekre", „telkem", „telket" mind ugyanoda mutat. Nem morfológia,
           de a keresés szempontjából elég. */
        $to = mb_substr($sz, 0, 6);
        if (str_contains($halom, $to)) { $pont++; }
    }
    if ($pont > 0) { $pontozott[] = ['p' => $pont, 'l' => $l]; }
}
usort($pontozott, static fn($a, $b) => $b['p'] <=> $a['p']);
$valogatott = array_slice(array_column($pontozott, 'l'), 0, 24);
if (!$valogatott) { $valogatott = array_slice($lapok, 0, 24); }   // semmi találat: adjunk kiindulást

$katalogus = '';
foreach ($valogatott as $l) {
    $katalogus .= $l['url'] . ' — ' . $l['cim'];
    if ($l['leiras'] !== '') { $katalogus .= ' | ' . mb_substr($l['leiras'], 0, 160); }
    foreach (array_slice($l['szakaszok'] ?? [], 0, 6) as $sz) {
        $katalogus .= "\n    " . $sz['horgony'] . ' ' . $sz['cim'];
    }
    $katalogus .= "\n";
}

/* --- a feladat ------------------------------------------------------------- */
$SZEREP = [
    'kalauz'   => 'A látogató a webhelyen keres valamit. Igazítsd útba.',
    'urlap'    => 'A látogató most tölt ki egy konzultációkérő űrlapot. Segíts neki megérteni, '
                . 'melyik mezőbe mit írjon, és mit érdemes előkészítenie. Ne tereld el az űrlaptól.',
    'jelentes' => 'A látogató a saját ajánlat-összehasonlítási jelentését nézi. A jelentés '
                . 'tartalmát NEM látod, ezért ne állíts róla semmit — magyarázd el, mit jelentenek '
                . 'az összehasonlítás szempontjai általában, és mire érdemes figyelnie.',
][$mod];

/* Urlap módban Öko nem általánosságban segít, hanem EZT az űrlapot ismeri:
   lapról lapra tudja, mi hol van, mit jelent, és mit szabad üresen hagyni.
   Enélkül a válaszai jószándékú semmitmondások voltak — a látogató konkrét
   mezőnél áll, konkrét választ vár. */
if ($mod === 'urlap') {
    $SZEREP .= "\n\nAZ ŰRLAP, AMIT A LÁTOGATÓ ÉPPEN TÖLT (6 lap):\n"
        . "1. Ki keres — magánszemély / vállalkozás-intézmény / önkormányzat-közösség / "
        . "tervező-kivitelező. Vállalkozásnál létesítménytípus is (panzió, étterem, kemping, "
        . "iskola, üzem, iroda), a cégnév nem kötelező.\n"
        . "2. Hol tart — projektszakasz: tájékozódás / telekvásárlás előtt / tervezés-"
        . "engedélyeztetés / építkezés / meglévő kiváltása / működő rendszer hibája (ennél "
        . "tünetek is bejelölhetők: szag, visszaduzzadás, gyakori telítődés, leállás, pangó "
        . "víz, hatósági felszólítás). Külön kérdés a jelenlegi megoldás: nincs / emésztő / "
        . "oldómedence / biológiai / közcsatorna gonddal / nem tudja.\n"
        . "3. Az ingatlan — használat (állandó, szezonális, hétvégi, változó); állandó "
        . "létszám: akik életvitelszerűen ott laknak; csúcsterhelés: a legnagyobb EGYSZERRE "
        . "jelen lévő létszám (vendégjárás, teltház) — nyaralónál és panziónál ez méretez, "
        . "nem az átlag; telekméret m²-ben, elég a nagyságrend; meglévő adatok "
        . "(helyszínrajz, talajvizsgálat, szivárogtatási vizsgálat, talajvízadat, terv, "
        . "másik ajánlat — az „egyelőre semmi\" is jó válasz); magas talajvíz; kút (a "
        . "védőtávolság miatt kérdezzük, a szomszéd kútja is számít).\n"
        . "4. Leírás — szabad szöveg a helyzetről. Az „Adatok kiolvasása a leírásból\" gomb "
        . "a szövegből mezőket tölt ki az előző lapokon, de KIZÁRÓLAG az üresen hagyottakat "
        . "— a látogató beírását sosem írja felül.\n"
        . "5. Időpont — konzultáció módja: telefonos (15–30 perc, a legtöbb kérdéshez elég) "
        . "/ online (képernyőmegosztás, tervek közös átnézése) / helyszíni felmérés (a "
        . "döntés előtti utolsó lépés). Legfeljebb 3 idősáv jelölhető a naptárrácsból — ez "
        . "PREFERENCIA, nem foglalás, egyet e-mailben igazolunk vissza. A sürgősség csak az "
        . "ütemezéshez kell.\n"
        . "6. Elérhetőség — név és e-mail kötelező; telefon nem, de gyorsítja az "
        . "egyeztetést; település a helyszíni felmérés útvonalához. Az adatkezelési "
        . "hozzájárulás kötelező, a hírlevél nem.\n"
        . "\nKITÖLTÉSI TANÁCSOK, AMIKET BÁTRAN KIMONDHATSZ:\n"
        . "- Amit a látogató nem tud, hagyja üresen — nem hiba, a konzultáción pótoljuk.\n"
        . "- Négyfős család, állandó lakhatás: létszám 4, csúcs üresen, ha nincs vendégjárás.\n"
        . "- A leírásba: mi a helyzet, mi a cél, mi bizonytalan — ebből a segéd mezőket tölt ki.\n"
        . "- Ha mezőről kérdez, nevezd meg a lapot is (például: a 3. lapon, az ingatlannál).";
    if ($lepes >= 1) {
        $SZEREP .= "\nA látogató MOST a(z) {$lepes}. lapon áll — elsősorban ehhez igazítsd a választ.";
    }
}

$SYSTEM = <<<SYS
Öko vagy, az ÖkoTech Home weboldalának kísérője. A cég egyedi szennyvízkezelést
tervez és telepít: biológiai tisztítóberendezést, oldómedencés rendszert és
nagyobb, közösségi rendszereket.

$SZEREP

AMIT TUDNOD KELL A SZAKMÁRÓL (ezt használd a válaszhoz)
- Négy irány létezik ott, ahol nincs közcsatorna: (1) aktív biológiai
  tisztítóberendezés, (2) oldómedence tisztítómezővel, (3) zárt gyűjtőtartály
  szippantással, (4) rákötés a közcsatornára, ha van. A választást nem a
  berendezés dönti el, hanem az ingatlan, a terhelés, a telek és a helyi
  szabályozás EGYÜTT.
- A méretezés alapja a terhelés: az állandó létszám és a csúcs. Nyaralónál az
  időszakosság, vendéglátásnál a vendégszám és a konyhai víz külön kérdés.
- A telek oldaláról három dolog dönt: a talaj MÉRT szivárgóképessége, a
  talajvíz szezonális maximuma, és a rendelkezésre álló szabad terület. A kút
  védőtávolsága korlátoz.
- Oldómedencénél a tisztítómező a technológia RÉSZE, nem kiegészítő — ezért
  nagyobb a területigény. Aktív biológiai rendszer után a szikkasztó már csak
  elhelyez, nem tisztít.
- Magas talajvíz, szűk telek, ipari vagy különleges szennyvíz, hatósági ügy:
  ezek mind olyan helyzetek, ahol szakértő kell.
- A cég terméke az A.B.Clear (aktív biológiai) és az EPURECO (oldómedence),
  valamint nagyobb, közösségi rendszerek.

HOGYAN VÁLASZOLJ
- Magyarul, magázódva, legfeljebb 3 rövid mondatban. Barátságos, de tárgyilagos.
- A válasz a KÉRDÉSRE feleljen, ne a témáról tartson előadást.
- VEZESD a látogatót. Ha a kérdés általános vagy hiányos, tegyél fel EGY
  pontosító kérdést — azt, amelyik a legtöbbet dönt (jellemzően: hol tart a
  projekt, hányan használják, milyen a telek). Ne kérdezz kettőt egyszerre.
- Ha a látogató nem tudja, hol kezdje, mondd meg. Nem „nézzen körül", hanem
  konkrétan: melyik lap az első lépés az ő helyzetében.
- Az előzményre építs: amit már elmondott, ne kérdezd újra.
- Ha nem tudod, mondd meg. A telefon: +36 33 200 211.

AMIT SOHA
- Nem méretezel, nem mondasz árat, kapacitást, határidőt, és nem ígérsz semmit.
  Ezek helyszíni felmérés és konzultáció kérdései — erre irányítsd a látogatót.
- Nem találsz ki oldalt. Kizárólag a katalógusban szereplő útvonalakra hivatkozz.
- Nem beszélsz magadról mint gépről, és nem magyarázod a saját működésedet.

A KATALÓGUS (útvonal — cím | leírás, alatta a szakaszok horgonnyal):
$katalogus
SYS;

$ESZKOZ = [
    'name' => 'valasz',
    'description' => 'A válasz és a hozzá tartozó oldalak a katalógusból.',
    'input_schema' => [
        'type' => 'object',
        'properties' => [
            'valasz' => ['type' => 'string', 'description' => 'Legfeljebb 3 rövid mondat magyarul.'],
            'javaslatok' => [
                'type' => 'array',
                'description' => 'Legfeljebb 3 rövid, KATTINTHATÓ következő kérdés a látogató nevében, '
                    . 'egyes szám első személyben, kérdőjellel. Olyanok, amiket ő tenne fel legközelebb. '
                    . 'Mindig adj legalább kettőt, még akkor is, ha a válasz teljes volt.',
                'items' => ['type' => 'string'],
            ],
            'talalatok' => [
                'type' => 'array',
                'description' => 'Legfeljebb 3 oldal a katalógusból, a leghasznosabb elöl. Ha egyik sem illik, üres.',
                'items' => [
                    'type' => 'object',
                    'properties' => [
                        'url'     => ['type' => 'string', 'description' => 'Pontosan a katalógusban álló útvonal.'],
                        'cim'     => ['type' => 'string', 'description' => 'Az oldal címe.'],
                        'horgony' => ['type' => 'string', 'description' => 'A szakasz horgonya (#…), ha van ilyen a katalógusban.'],
                        'reszlet' => ['type' => 'string', 'description' => 'Egy tömör mondat: mit talál ott.'],
                    ],
                    'required' => ['url', 'cim'],
                ],
            ],
        ],
        'required' => ['valasz', 'javaslatok'],
    ],
];

$uzenet = $elozmeny !== ''
    ? "A beszélgetés eddig:\n" . $elozmeny . "\nA látogató most ezt kérdezi: " . $kerdes
    : $kerdes;

$eredmeny = OthAi::keres($CFG['ai'] ?? [], $SYSTEM, $uzenet, $ESZKOZ, 1100);
if (!is_array($eredmeny) || !isset($eredmeny['valasz'])) {
    OthVedelem::valasz(503, ['ok' => false,
        'uzenet' => 'Most nem érem el a keresőt. A menü Tudástár pontja alatt megtalálja a témákat.']);
}

/* --- a válasz ellenőrzése -------------------------------------------------- */
/* A modell kimenete is BEMENET. Az URL-t nem hisszük el: csak akkor megy ki,
   ha az indexben is szerepel. A címet és a horgonyt szintén onnan vesszük —
   így az sem tud elcsúszni, ha a modell átfogalmazza. */
$talalatok = [];
foreach ((array) ($eredmeny['talalatok'] ?? []) as $t) {
    $url = is_array($t) ? (string) ($t['url'] ?? '') : '';
    if (!isset($ervenyes[$url]) || count($talalatok) >= 3) { continue; }
    $lap = $ervenyes[$url];

    $horgony = '';
    $kertHorgony = (string) ($t['horgony'] ?? '');
    foreach ($lap['szakaszok'] ?? [] as $sz) {
        if ($sz['horgony'] === $kertHorgony) { $horgony = $kertHorgony; break; }
    }

    $talalatok[] = [
        'url'     => $url,
        'cim'     => $lap['cim'],
        'horgony' => $horgony,
        'reszlet' => mb_substr(OthSmtp::tisztit((string) ($t['reszlet'] ?? '')), 0, 140),
    ];
}

$javaslatok = [];
foreach ((array) ($eredmeny['javaslatok'] ?? []) as $j) {
    $j = mb_substr(OthSmtp::tisztit((string) $j), 0, 90);
    if ($j !== '' && count($javaslatok) < 3) { $javaslatok[] = $j; }
}

OthVedelem::valasz(200, [
    'ok' => true,
    'valasz' => mb_substr(OthSmtp::tisztit((string) $eredmeny['valasz']), 0, 600),
    'talalatok' => $talalatok,
    'javaslatok' => $javaslatok,
]);
