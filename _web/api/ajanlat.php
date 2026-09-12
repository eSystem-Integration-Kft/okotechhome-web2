<?php
/**
 * ajanlat.php — az Ajánlatkérés oldal űrlapja.
 * ---------------------------------------------------------------------------
 * Két levél megy ki: az ajánlatkérés nekünk (a látogató címével Reply-To-ban,
 * a csatolt helyszínrajzokkal együtt), és a visszaigazolás a látogatónak.
 *
 * MIÉRT KÜLÖN VÉGPONT, ÉS NEM A `kapcsolat.php` EGY MEZŐVEL. Az ajánlatkérés
 * más adatokat kér (ingatlantípus, létszám, jelenlegi megoldás, tervezett
 * kezdés), MELLÉKLETET fogad, és más postaládába megy. Egy közös végpont
 * mindhármat feltételes ágakkal oldaná meg — az ilyen elágazás az, ami később
 * némán elromlik.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';

OthVedelem::sebessegkorlat('ajanlat', (int) $CFG['vedelem']['limit'], (int) $CFG['vedelem']['ablak_perc']);

/* --- bemenet ------------------------------------------------------------- */
$nev       = OthVedelem::szoveg($BE, 'nev', 120);
$email     = OthVedelem::email($BE, 'email');
$telefon   = OthVedelem::telefon($BE, 'telefon');
$cegnev    = OthVedelem::szoveg($BE, 'cegnev', 160);
$telepules = OthVedelem::szoveg($BE, 'telepules', 120);
$hrsz      = OthVedelem::szoveg($BE, 'hrsz', 60);
$letszam   = OthVedelem::szoveg($BE, 'letszam', 10);
$uzenet    = OthVedelem::szoveg($BE, 'uzenet', (int) $CFG['vedelem']['max_uzenet']);
$hozzajarul = !empty($BE['hozzajarul']);

/* Zárt értékkészletű mezők: a kliens bármit küldhet, ezért a listán kívüli
   érték nem „egyéb" lesz, hanem eldobjuk — a levélben csak olyan felirat
   jelenhet meg, amit MI írtunk. */
$LISTAK = [
    'ingatlan' => [
        'csaladi-haz' => 'Családi ház, állandó lakhatás',
        'nyaralo'     => 'Nyaraló, időszakos használat',
        'vallalkozas' => 'Vállalkozás (panzió, étterem, üzem)',
        'intezmeny'   => 'Intézmény (iskola, óvoda, közösségi épület)',
        'kozossegi'   => 'Több ingatlan, közösségi rendszer',
    ],
    'jelenlegi' => [
        'nincs'        => 'Semmi — új építés vagy üres telek',
        'emeszto'      => 'Emésztő (szikkasztó akna)',
        'oldomedence'  => 'Oldómedence, szikkasztás',
        'biologiai'    => 'Biológiai tisztító berendezés',
        'egyeb'        => 'Egyéb vagy nem tudja',
    ],
    'irany' => [
        'nem-tudom' => 'Még nem tudja — javaslatot kér',
        'ab-clear'  => 'A.B.Clear biológiai tisztító',
        'epureco'   => 'EPURECO oldómedence',
        'nagyobb'   => 'Nagyobb vagy közösségi rendszer',
    ],
    'kezdes' => [
        '1-honap'      => 'Egy hónapon belül',
        '3-honap'      => 'Három hónapon belül',
        'fel-ev'       => 'Fél éven belül',
        'tajekozodas'  => 'Még csak tájékozódik',
    ],
];
$valasztott = [];
foreach ($LISTAK as $mezo => $lista) {
    $ertek = OthVedelem::szoveg($BE, $mezo, 40);
    $valasztott[$mezo] = $lista[$ertek] ?? '';
}

/* --- ellenőrzés ---------------------------------------------------------- */
$hibak = [];
if (mb_strlen($nev) < 2)       { $hibak['nev'] = 'Kérjük, adja meg a nevét.'; }
if ($email === '')             { $hibak['email'] = 'Kérjük, adjon meg érvényes e-mail-címet.'; }
if (mb_strlen($telepules) < 2) { $hibak['telepules'] = 'A település nélkül nem tudunk árat mondani.'; }
if (!$hozzajarul)              { $hibak['hozzajarul'] = 'Az adatkezeléshez való hozzájárulás szükséges.'; }

/* --- csatolmányok -------------------------------------------------------- */
$csatolmanyok = OthVedelem::fajlLista($_FILES['fajl'] ?? null, $CFG['csatolmany'], $fajlHiba);
if ($fajlHiba !== '') { $hibak['fajl'] = $fajlHiba; }

if ($hibak) {
    OthVedelem::valasz(422, ['ok' => false, 'uzenet' => 'Néhány mezőt pontosítani kell.', 'mezok' => $hibak]);
}

/* --- értesítés nekünk ---------------------------------------------------- */
$cimSor = 'Ajánlatkérés — ' . $nev . ' (' . $telepules . ')';
$adatok = [
    'Név'                => OthVedelem::html($nev),
    'E-mail'             => '<a href="mailto:' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '" style="color:#2F6F82;">' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '</a>',
    'Telefon'            => $telefon !== '' ? OthVedelem::html($telefon) : '',
    'Cég vagy intézmény' => $cegnev !== '' ? OthVedelem::html($cegnev) : '',
    'Település'          => OthVedelem::html($telepules),
    'Helyrajzi szám'     => $hrsz !== '' ? OthVedelem::html($hrsz) : '',
    'Ingatlan típusa'    => OthVedelem::html($valasztott['ingatlan']),
    'Hány fő használja'  => $letszam !== '' ? OthVedelem::html($letszam) : '',
    'Jelenlegi megoldás' => OthVedelem::html($valasztott['jelenlegi']),
    'Érdeklődés iránya'  => OthVedelem::html($valasztott['irany']),
    'Tervezett kezdés'   => OthVedelem::html($valasztott['kezdes']),
    'Megjegyzés'         => $uzenet !== '' ? OthVedelem::html($uzenet) : '',
    'Mellékletek'        => $csatolmanyok
        ? OthVedelem::html(implode(', ', array_column($csatolmanyok, 'nev'))) : '',
];

$html = OthLevel::html(
    $CFG['webhely'],
    'Ajánlatkérés a weboldalról',
    $cimSor,
    'Az alábbi ajánlatkérés érkezett. A válasz gomb közvetlenül a kérőnek megy.',
    $adatok,
    ['felirat' => 'Ajánlat írása', 'url' => 'mailto:' . $email],
    'Beérkezett: ' . date('Y. m. d. H:i') . ' · IP: ' . htmlspecialchars((string) ($_SERVER['REMOTE_ADDR'] ?? '—'), ENT_QUOTES, 'UTF-8')
);
$szoveg = OthLevel::szoveg($CFG['webhely'], $cimSor,
    'Az alábbi ajánlatkérés érkezett a weboldalról.', $adatok,
    'Beérkezett: ' . date('Y. m. d. H:i'));

$cimzett = $CFG['cimzettek']['ajanlat'] ?? $CFG['cimzettek']['kapcsolat'];
oth_kuld($CFG, $cimzett, '[Weboldal] ' . $cimSor, $szoveg, $html, $csatolmanyok, $email, $nev,
         oth_masolat($CFG));

/* --- visszaigazolás a látogatónak ---------------------------------------- */
if (!empty($CFG['visszaigazolas'])) {
    $vhtml = OthLevel::html(
        $CFG['webhely'],
        'Visszaigazolás',
        'Megkaptuk az ajánlatkérését',
        "Köszönjük. Az adatokat átnézzük, és két munkanapon belül küldjük a tételes ajánlatot.\n"
        . 'Ha valami hiányzik a méretezéshez, előbb rákérdezünk. Sürgős esetben: ' . $CFG['webhely']['tel'] . '.',
        [
            'Település'       => OthVedelem::html($telepules),
            'Ingatlan típusa' => OthVedelem::html($valasztott['ingatlan']),
            'Megjegyzése'     => $uzenet !== '' ? OthVedelem::html($uzenet) : '',
        ],
        ['felirat' => 'Vissza a weboldalra', 'url' => $CFG['webhely']['url']],
        'Erre a levélre nem szükséges válaszolnia — csak visszaigazolás.'
    );
    $vszoveg = OthLevel::szoveg($CFG['webhely'], 'Megkaptuk az ajánlatkérését',
        'Az adatokat átnézzük, és két munkanapon belül küldjük a tételes ajánlatot.',
        ['Település' => OthVedelem::html($telepules)]);

    /* A visszaigazolás elmaradása NEM hiba a látogató szempontjából: az
       ajánlatkérés már megérkezett hozzánk. */
    try {
        oth_kuld($CFG, [$email], 'Megkaptuk az ajánlatkérését — ' . $CFG['webhely']['nev'], $vszoveg, $vhtml);
    } catch (Throwable $e) {
        error_log('OTH: az ajánlatkérés visszaigazolása nem ment ki: ' . $e->getMessage());
    }
}

/* --- átadás a CRM-nek (a levelek UTÁN) ----------------------------------- */
OthCrm::kuld($CFG, 'ajanlat', OthCrm::csomag(
    OthVedelem::szoveg($BE, 'ugy_azonosito', 40) ?: null,
    'ajanlat-' . date('YmdHis') . '-' . substr(sha1($email), 0, 8),
    ['nev' => $nev, 'email' => $email, 'telefon' => $telefon, 'cegnev' => $cegnev],
    [
        'targy'    => 'Ajánlatkérés a weboldalról',
        'uzenet'   => $uzenet,
        'url'      => $CFG['webhely']['url'] ?? null,
        'valaszok' => array_filter([
            'település'          => $telepules,
            'helyrajzi szám'     => $hrsz,
            'ingatlan típusa'    => $valasztott['ingatlan'],
            'létszám'            => $letszam,
            'jelenlegi megoldás' => $valasztott['jelenlegi'],
            'érdeklődés iránya'  => $valasztott['irany'],
            'tervezett kezdés'   => $valasztott['kezdes'],
        ]),
    ],
    $hozzajarul,
));

OthVedelem::valasz(200, [
    'ok' => true,
    'uzenet' => 'Köszönjük, megkaptuk az ajánlatkérését. Két munkanapon belül küldjük a tételes ajánlatot.',
]);
