<?php
/**
 * dontestamogato.php — a 8. szekció (AI döntéstámogató) eredményének küldése.
 * ---------------------------------------------------------------------------
 * A modul JSON-t küld: { email, visszahivas, valaszok{}, arsav{}, idobelyeg }.
 * Két levél megy: az összefoglaló a látogatónak, és egy értesítés nekünk —
 * ez utóbbi az érdeklődés miatt fontos, különösen visszahívás-kérésnél.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';

OthVedelem::sebessegkorlat('dontestamogato', (int) $CFG['vedelem']['limit'], (int) $CFG['vedelem']['ablak_perc']);

$email       = OthVedelem::email($BE, 'email');
$visszahivas = !empty($BE['visszahivas']);
$valaszok    = is_array($BE['valaszok'] ?? null) ? $BE['valaszok'] : [];
$arsav       = is_array($BE['arsav'] ?? null) ? $BE['arsav'] : [];

if ($email === '') {
    OthVedelem::valasz(422, ['ok' => false, 'uzenet' => 'Kérjük, adjon meg érvényes e-mail-címet.',
                             'mezok' => ['email' => 'Érvénytelen e-mail-cím.']]);
}

/* A válaszok a kliensről jönnek, tehát NEM megbízhatóak: minden kulcsot és
   értéket szövegként kezelünk, escape-elve, hosszkorláttal. Nem használjuk
   őket vezérlésre, csak megjelenítjük. */
$sorok = [];
$i = 0;
foreach ($valaszok as $kulcs => $ertek) {
    if (++$i > 40) { break; }
    $k = mb_substr(OthSmtp::tisztit((string) $kulcs), 0, 120);
    $v = is_array($ertek) ? implode(', ', array_map('strval', $ertek)) : (string) $ertek;
    $v = mb_substr(OthSmtp::tisztit($v), 0, 400);
    if ($k === '' || $v === '') { continue; }
    $sorok[$k] = OthVedelem::html($v);
}

$sav = '';
if (!empty($arsav['min']) && !empty($arsav['max'])) {
    $sav = number_format((float) $arsav['min'], 0, ',', "\u{00A0}") . "\u{00A0}–\u{00A0}"
         . number_format((float) $arsav['max'], 0, ',', "\u{00A0}") . "\u{00A0}Ft";
} elseif (!empty($arsav['szoveg'])) {
    $sav = mb_substr(OthSmtp::tisztit((string) $arsav['szoveg']), 0, 200);
}

$LABJEGYZET = 'A megadott tartomány <strong>tájékoztató jellegű</strong>: a végleges árat a '
    . 'telepítési körülmények — földmunka, a bekötés mélysége és a kezelt víz elhelyezésének '
    . 'módja — mozgatják leginkább, ezeket pedig helyszíni felmérés nélkül nem lehet '
    . 'felelősen megmondani.';

/* ------------------------------------------------ összefoglaló a látogatónak */
$adatok = $sorok;
if ($sav !== '') {
    $adatok = ['Becsült költségtartomány' => '<strong>' . htmlspecialchars($sav, ENT_QUOTES, 'UTF-8') . '</strong>'] + $adatok;
}

$html = OthLevel::html(
    $CFG['webhely'],
    'Döntéstámogató — összefoglaló',
    'Az Ön válaszai és a becsült költségtartomány',
    "Köszönjük, hogy kitöltötte a döntéstámogatót. Az alábbiakban összefoglaltuk, mit adott meg,\n"
    . 'és milyen nagyságrenddel érdemes számolnia.',
    $adatok,
    ['felirat' => 'Felmérés kérése', 'url' => $CFG['webhely']['url'] . '/kapcsolat'],
    $LABJEGYZET
);
$szoveg = OthLevel::szoveg($CFG['webhely'], 'Az Ön válaszai és a becsült költségtartomány',
    'Köszönjük, hogy kitöltötte a döntéstámogatót.', $adatok, strip_tags($LABJEGYZET));

oth_kuld($CFG, [$email], 'Döntéstámogató — összefoglaló · ' . $CFG['webhely']['nev'], $szoveg, $html);

/* ------------------------------------------------------- értesítés nekünk */
$belso = ['E-mail' => htmlspecialchars($email, ENT_QUOTES, 'UTF-8')]
       + ($visszahivas ? ['Visszahívást kért' => '<strong>Igen</strong>'] : [])
       + ($sav !== '' ? ['Becsült tartomány' => htmlspecialchars($sav, ENT_QUOTES, 'UTF-8')] : [])
       + $sorok;

$bhtml = OthLevel::html(
    $CFG['webhely'],
    $visszahivas ? 'Visszahívást kértek' : 'Döntéstámogató kitöltve',
    ($visszahivas ? 'Visszahívási kérés — ' : 'Új kitöltés — ') . $email,
    $visszahivas
        ? 'A látogató kitöltötte a döntéstámogatót, és visszahívást kért.'
        : 'A látogató kitöltötte a döntéstámogatót, és kérte az összefoglalót.',
    $belso,
    ['felirat' => 'Válasz írása', 'url' => 'mailto:' . $email],
    'Beérkezett: ' . date('Y. m. d. H:i')
);
$bszoveg = OthLevel::szoveg($CFG['webhely'], 'Döntéstámogató kitöltve', '', $belso);

try {
    oth_kuld($CFG, $CFG['cimzettek']['dontestamogato'],
        ($visszahivas ? '[Weboldal] VISSZAHÍVÁS — ' : '[Weboldal] Döntéstámogató — ') . $email,
        $bszoveg, $bhtml, [], $email);
} catch (Throwable $e) {
    /* A látogató már megkapta az összefoglalót — a belső értesítés hiánya
       nem az ő hibája, és nem is az ő problémája. */
    error_log('OTH: a belső értesítés nem ment ki: ' . $e->getMessage());
}

/*
 * ÁTADÁS A CRM-NEK.
 *
 * A döntéstámogatót kitöltő látogató TÁJÉKOZÓDIK: nála a döntés hetek múlva
 * születik meg, és a türelmetlen hívás ront a helyzeten. Ezért megy külön
 * forrásba — a CRM ebből tudja, hogy nem kell azonnal telefonálni, de azt is,
 * hogy mit válaszolt a látogató, ha később mégis megkeres minket.
 */
OthCrm::kuld($CFG, 'arsav', OthCrm::csomag(
    OthVedelem::szoveg($BE, 'ugy_azonosito', 40) ?: null,
    'arsav-' . date('YmdHis') . '-' . substr(sha1($email), 0, 8),
    ['email' => $email],
    [
        'targy'    => $visszahivas ? 'Ársávbecslő — VISSZAHÍVÁST kért' : 'Ársávbecslő kitöltése',
        'url'      => $CFG['webhely']['url'] ?? null,
        'valaszok' => array_merge(
            array_map(static fn ($v): string => is_array($v) ? implode(', ', array_map('strval', $v)) : (string) $v, $valaszok),
            $arsav === [] ? [] : ['becsült ársáv' => implode(' – ', array_map('strval', $arsav))],
        ),
    ],
    /* HOZZÁJÁRULÁS: csak a visszahívás-kérés az. Az e-mail-cím megadása az
       összefoglaló KÉRÉSE, nem marketing-engedély — ezt a különbséget a CRM-nek
       is látnia kell, mert onnantól az ő felelőssége, kit szólít meg. */
    $visszahivas,
));

OthVedelem::valasz(200, ['ok' => true, 'uzenet' => 'Elküldtük az összefoglalót.']);
