<?php
/**
 * ajanlat-atnezes.php — a 11. szekció (ajánlat-összehasonlító) szakértői átnézése.
 * ---------------------------------------------------------------------------
 * Ez a végpont FÁJLOKAT is fogad: a látogató 2–3 ajánlatot csatol, mi pedig
 * átnézzük őket. Amíg az automatikus kiolvasás nincs kész, ez a modul valódi,
 * működő kimenete — ezért fontos, hogy a csatolmány tényleg megérkezzen.
 *
 * A fájlok NEM kerülnek a webgyökérbe: közvetlenül a levélbe ágyazódnak, és a
 * kérés végén eltűnnek. Így nincs feltöltött-fájl-könyvtár, amit védeni kell.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';

/* Fájlfeltöltésnél szigorúbb korlát: ez a művelet drágább. */
OthVedelem::sebessegkorlat('ajanlat', 3, (int) $CFG['vedelem']['ablak_perc']);

$nev     = OthVedelem::szoveg($BE, 'nev', 120);
$email   = OthVedelem::email($BE, 'email');
$telefon = OthVedelem::telefon($BE, 'telefon');
$uzenet  = OthVedelem::szoveg($BE, 'uzenet', 3000);
$hozzajarul = !empty($BE['hozzajarul']);

$hibak = [];
if (mb_strlen($nev) < 2) { $hibak['nev'] = 'Kérjük, adja meg a nevét.'; }
if ($email === '')       { $hibak['email'] = 'Kérjük, adjon meg érvényes e-mail-címet.'; }
if (!$hozzajarul)        { $hibak['hozzajarul'] = 'Az adatkezeléshez való hozzájárulás szükséges.'; }

/* --- csatolmányok ------------------------------------------------------- */
$csatolmanyok = [];
$fajlHibak = [];
$mezok = ['ajanlat_a' => 'Ajánlat A', 'ajanlat_b' => 'Ajánlat B', 'ajanlat_c' => 'Ajánlat C'];

foreach ($mezok as $mezo => $cimke) {
    if (!isset($_FILES[$mezo]) || ($_FILES[$mezo]['error'] ?? UPLOAD_ERR_NO_FILE) === UPLOAD_ERR_NO_FILE) {
        continue;
    }
    if (count($csatolmanyok) >= (int) $CFG['csatolmany']['max_darab']) {
        break;
    }
    try {
        $f = OthVedelem::fajl($_FILES[$mezo], $CFG['csatolmany']);
        /* A címke a fájlnév elé kerül, hogy a postaládában is látszódjon,
           melyik ajánlat melyik. */
        $f['nev'] = $cimke . ' — ' . $f['nev'];
        $csatolmanyok[] = $f;
    } catch (RuntimeException $e) {
        $fajlHibak[$mezo] = $cimke . ': ' . $e->getMessage();
    }
}

if ($fajlHibak) {
    $hibak = array_merge($hibak, $fajlHibak);
}
if (!$csatolmanyok && !$fajlHibak) {
    $hibak['ajanlat_a'] = 'Csatoljon legalább egy ajánlatot.';
}
if ($hibak) {
    OthVedelem::valasz(422, ['ok' => false, 'uzenet' => 'A beküldést pontosítani kell.', 'mezok' => $hibak]);
}

/* Összméret: a levélszerverek jellemzően 20–25 MB fölött visszautasítanak,
   és a base64 még ~33%-kal növel. 15 MB nyers a biztonságos felső határ. */
$ossz = array_sum(array_map(fn($f) => strlen($f['adat']), $csatolmanyok));
if ($ossz > 15 * 1024 * 1024) {
    OthVedelem::valasz(413, ['ok' => false,
        'uzenet' => 'A csatolt fájlok együtt túl nagyok. Küldje kevesebbet, vagy írjon nekünk e-mailben.']);
}

/* --- levél nekünk -------------------------------------------------------- */
$lista = implode('<br>', array_map(
    fn($f) => htmlspecialchars($f['nev'], ENT_QUOTES, 'UTF-8')
        . ' <span style="color:#4A4F49;">(' . round(strlen($f['adat']) / 1024) . ' KB)</span>',
    $csatolmanyok
));

$adatok = [
    'Név'      => OthVedelem::html($nev),
    'E-mail'   => '<a href="mailto:' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '" style="color:#2F6F82;">' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '</a>',
    'Telefon'  => $telefon !== '' ? OthVedelem::html($telefon) : '',
    'Megjegyzés' => $uzenet !== '' ? OthVedelem::html($uzenet) : '',
    'Csatolt ajánlatok' => $lista,
];

$html = OthLevel::html(
    $CFG['webhely'],
    'Szakértői átnézés kérése',
    'Ajánlat-átnézés — ' . $nev,
    'A látogató ajánlatokat küldött be átnézésre. A fájlok a levél mellékleteként érkeztek.',
    $adatok,
    ['felirat' => 'Válasz írása', 'url' => 'mailto:' . $email],
    'Beérkezett: ' . date('Y. m. d. H:i')
);
$szoveg = OthLevel::szoveg($CFG['webhely'], 'Ajánlat-átnézés — ' . $nev,
    'A látogató ajánlatokat küldött be átnézésre.', $adatok);

oth_kuld($CFG, $CFG['cimzettek']['ajanlat-atnezes'],
    '[Weboldal] Ajánlat-átnézés — ' . $nev, $szoveg, $html, $csatolmanyok, $email, $nev);

/* --- visszaigazolás a látogatónak (csatolmány NÉLKÜL) -------------------- */
if (!empty($CFG['visszaigazolas'])) {
    $vhtml = OthLevel::html(
        $CFG['webhely'],
        'Visszaigazolás',
        'Megkaptuk az ajánlatait',
        "Köszönjük. Szakértőnk átnézi a beküldött ajánlatokat, és jelentkezik a tapasztalatokkal.\n"
        . 'Ha közben kérdése van, hívjon minket: ' . $CFG['webhely']['tel'] . '.',
        ['Beküldött fájlok' => $lista],
        [],
        'Az átnézés tájékoztató jellegű, nem helyettesíti a helyszíni felmérést.'
    );
    $vszoveg = OthLevel::szoveg($CFG['webhely'], 'Megkaptuk az ajánlatait',
        'Szakértőnk átnézi a beküldött ajánlatokat, és jelentkezik.', ['Beküldött fájlok' => $lista]);
    try {
        oth_kuld($CFG, [$email], 'Megkaptuk az ajánlatait — ' . $CFG['webhely']['nev'], $vszoveg, $vhtml);
    } catch (Throwable $e) {
        error_log('OTH: a visszaigazolás nem ment ki: ' . $e->getMessage());
    }
}

OthVedelem::valasz(200, [
    'ok' => true,
    'uzenet' => 'Köszönjük, megkaptuk az ajánlatokat. Szakértőnk átnézi őket, és jelentkezik.',
]);
