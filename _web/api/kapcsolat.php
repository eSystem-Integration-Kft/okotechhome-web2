<?php
/**
 * kapcsolat.php — a Kapcsolat oldal űrlapja.
 * ---------------------------------------------------------------------------
 * Két levél megy ki: az értesítés nekünk (a látogató címével Reply-To-ban),
 * és a visszaigazolás a látogatónak, hogy tudja, megérkezett.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';

OthVedelem::sebessegkorlat('kapcsolat', (int) $CFG['vedelem']['limit'], (int) $CFG['vedelem']['ablak_perc']);

$nev     = OthVedelem::szoveg($BE, 'nev', 120);
$email   = OthVedelem::email($BE, 'email');
$telefon = OthVedelem::telefon($BE, 'telefon');
$telepules = OthVedelem::szoveg($BE, 'telepules', 120);
$tema    = OthVedelem::szoveg($BE, 'tema', 60);
$uzenet  = OthVedelem::szoveg($BE, 'uzenet', (int) $CFG['vedelem']['max_uzenet']);
$hozzajarul = !empty($BE['hozzajarul']);

$hibak = [];
if (mb_strlen($nev) < 2)      { $hibak['nev'] = 'Kérjük, adja meg a nevét.'; }
if ($email === '')            { $hibak['email'] = 'Kérjük, adjon meg érvényes e-mail-címet.'; }
if (mb_strlen($uzenet) < 10)  { $hibak['uzenet'] = 'Írjon néhány mondatot arról, miben segíthetünk.'; }
if (!$hozzajarul)             { $hibak['hozzajarul'] = 'Az adatkezeléshez való hozzájárulás szükséges.'; }
if ($hibak) {
    OthVedelem::valasz(422, ['ok' => false, 'uzenet' => 'Néhány mezőt pontosítani kell.', 'mezok' => $hibak]);
}

$TEMAK = [
    'uj'      => 'Új érdeklődő',
    'ugyfel'  => 'Meglévő ügyfél',
    'partner' => 'Szakmai partner',
    'sajto'   => 'Sajtó vagy egyéb megkeresés',
];
$temaNev = $TEMAK[$tema] ?? 'Megkeresés';

/* ---------------------------------------------------------- értesítés nekünk */
$adatok = [
    'Név'          => OthVedelem::html($nev),
    'E-mail'       => '<a href="mailto:' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '" style="color:#2F6F82;">' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '</a>',
    'Telefon'      => $telefon !== '' ? OthVedelem::html($telefon) : '',
    'Település'    => $telepules !== '' ? OthVedelem::html($telepules) : '',
    'Megkeresés típusa' => OthVedelem::html($temaNev),
    'Üzenet'       => OthVedelem::html($uzenet),
];

$html = OthLevel::html(
    $CFG['webhely'],
    'Új megkeresés a weboldalról',
    $temaNev . ' — ' . $nev,
    'Az alábbi megkeresés érkezett a kapcsolati űrlapon. A válasz gomb közvetlenül a feladónak megy.',
    $adatok,
    ['felirat' => 'Válasz írása', 'url' => 'mailto:' . $email],
    'Beérkezett: ' . date('Y. m. d. H:i') . ' · IP: ' . htmlspecialchars((string) ($_SERVER['REMOTE_ADDR'] ?? '—'), ENT_QUOTES, 'UTF-8')
);
$szoveg = OthLevel::szoveg($CFG['webhely'], $temaNev . ' — ' . $nev,
    'Az alábbi megkeresés érkezett a kapcsolati űrlapon.', $adatok,
    'Beérkezett: ' . date('Y. m. d. H:i'));

oth_kuld($CFG, $CFG['cimzettek']['kapcsolat'],
    '[Weboldal] ' . $temaNev . ' — ' . $nev,
    $szoveg, $html, [], $email, $nev);

/* ------------------------------------------- visszaigazolás a látogatónak */
if (!empty($CFG['visszaigazolas'])) {
    $vhtml = OthLevel::html(
        $CFG['webhely'],
        'Visszaigazolás',
        'Megkaptuk a megkeresését',
        "Köszönjük, hogy írt nekünk. Munkanapokon egy munkanapon belül igyekszünk válaszolni.\n"
        . 'Ha sürgős, a telefon a gyorsabb út: ' . $CFG['webhely']['tel'] . '.',
        ['Az Ön üzenete' => OthVedelem::html($uzenet)],
        ['felirat' => 'Vissza a weboldalra', 'url' => $CFG['webhely']['url']],
        'Erre a levélre nem szükséges válaszolnia — csak visszaigazolás.'
    );
    $vszoveg = OthLevel::szoveg($CFG['webhely'], 'Megkaptuk a megkeresését',
        'Köszönjük, hogy írt nekünk. Munkanapokon egy munkanapon belül igyekszünk válaszolni.',
        ['Az Ön üzenete' => OthVedelem::html($uzenet)]);

    /* A visszaigazolás elmaradása NEM hiba a látogató szempontjából: a
       megkeresés már megérkezett hozzánk. Ezért külön try-catch. */
    try {
        oth_kuld($CFG, [$email], 'Megkaptuk a megkeresését — ' . $CFG['webhely']['nev'],
            $vszoveg, $vhtml);
    } catch (Throwable $e) {
        error_log('OTH: a visszaigazolás nem ment ki: ' . $e->getMessage());
    }
}

/*
 * ÁTADÁS A CRM-NEK — a levelek UTÁN.
 *
 * A sorrend nem mindegy: a levél a fontos, a CRM-rekord a hasznos. Előbb
 * küldve egy lassú CRM a visszaigazolást késleltetné, egy hibázó pedig — ha
 * valaha kivételt dobna — meg is akadályozhatná.
 */
OthCrm::kuld($CFG, 'okotechhome-kapcsolat', OthCrm::csomag(
    OthVedelem::szoveg($BE, 'ugy_azonosito', 40) ?: null,
    'kapcsolat-' . date('YmdHis') . '-' . substr(sha1($email), 0, 8),
    ['nev' => $nev, 'email' => $email, 'telefon' => $telefon],
    [
        'targy'   => $tema !== '' ? $tema : 'Kapcsolatfelvétel a weboldalról',
        'uzenet'  => $uzenet,
        'url'     => $CFG['webhely']['url'] ?? null,
        'valaszok' => array_filter(['település' => $telepules]),
    ],
    $hozzajarul,
));

OthVedelem::valasz(200, [
    'ok' => true,
    'uzenet' => 'Köszönjük, megkaptuk a megkeresését. Munkanapokon egy munkanapon belül válaszolunk.',
]);
