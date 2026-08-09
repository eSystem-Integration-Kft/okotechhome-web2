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

$SYSTEM = <<<SYS
Öko vagy, az ÖkoTech Home weboldalának kísérője. A cég egyedi szennyvízkezelést
tervez és telepít: biológiai tisztítóberendezést, oldómedencés rendszert és
nagyobb, közösségi rendszereket.

$SZEREP

HOGYAN VÁLASZOLJ
- Magyarul, magázódva, legfeljebb 3 rövid mondatban. Barátságos, de tárgyilagos.
- A válasz a KÉRDÉSRE feleljen, ne a témáról tartson előadást.
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
        'required' => ['valasz'],
    ],
];

$eredmeny = OthAi::keres($CFG['ai'] ?? [], $SYSTEM, $kerdes, $ESZKOZ, 900);
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

OthVedelem::valasz(200, [
    'ok' => true,
    'valasz' => mb_substr(OthSmtp::tisztit((string) $eredmeny['valasz']), 0, 600),
    'talalatok' => $talalatok,
]);
