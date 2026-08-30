<?php
/**
 * indit.php — közös indítás minden végponthoz.
 * ---------------------------------------------------------------------------
 * Betölti a konfigurációt és a könyvtárakat, elvégzi a kérés- és
 * bot-ellenőrzést, és beállítja a hibakezelést.
 *
 * A hibák NEM jutnak ki a válaszba: egy PHP-figyelmeztetés útvonalat, verziót
 * vagy akár konfigurációs értéket árulhatna el. A látogató általános üzenetet
 * kap, a részlet a naplóba megy.
 */

declare(strict_types=1);

ini_set('display_errors', '0');
ini_set('log_errors', '1');
ini_set('error_log', __DIR__ . '/../hiba.log');
error_reporting(E_ALL);

require __DIR__ . '/smtp.php';
require __DIR__ . '/level.php';
require __DIR__ . '/vedelem.php';
/*
 * A CRM-ÁTADÁS MINDEN VÉGPONTON ELÉRHETŐ.
 *
 * Nem minden végpont használja, de a betöltése olcsó, és így nem fordulhat
 * elő, hogy egy új űrlapnál elmarad a `require` — a kitöltés pedig némán
 * kimaradna a CRM-ből.
 */
require __DIR__ . '/crm.php';

$configFajl = __DIR__ . '/../config.php';
if (!is_file($configFajl)) {
    error_log('OTH: hiányzik a config.php — másold le a config.example.php-ból.');
    OthVedelem::hiba(503, 'A küldés jelenleg nem elérhető. Kérjük, hívjon minket, vagy írjon e-mailt.');
}
/** @var array $CFG */
$CFG = require $configFajl;

set_exception_handler(function (Throwable $e): void {
    error_log('OTH kivétel: ' . $e->getMessage());
    OthVedelem::hiba(500, 'Váratlan hiba történt a küldés közben. Kérjük, próbálja újra, vagy hívjon minket.');
});

OthVedelem::keresEllenorzes($CFG['vedelem']['origin']);

/* A bemenet JSON vagy űrlap is lehet: a döntéstámogató JSON-t küld, az
   ajánlat-átnézés fájlokkal együtt multipart/form-data-t. */
$BE = $_POST;
$nyersTipus = $_SERVER['CONTENT_TYPE'] ?? '';
if (stripos($nyersTipus, 'application/json') !== false) {
    $nyers = file_get_contents('php://input') ?: '';
    if (strlen($nyers) > 200000) {
        OthVedelem::hiba(413, 'A beküldött adat túl nagy.');
    }
    $j = json_decode($nyers, true);
    $BE = is_array($j) ? $j : [];
}

OthVedelem::botEllenorzes($BE, (int) $CFG['vedelem']['min_kitoltes']);

/** Levélküldés a konfigurált SMTP-n. */
function oth_kuld(array $CFG, array $cimzettek, string $targy, string $szoveg,
                  string $html, array $csatolmanyok = [], string $valaszCim = '',
                  string $valaszNev = ''): void
{
    /* A LOGÓ MINDEN LEVÉLBE BEÁGYAZVA MEGY. Itt tesszük hozzá, nem a hívó
       végpontokban: a fejléc a márkasablon része, nem az egyes üzeneteké — így
       egyetlen végpontról sem maradhat le. Ha a képfájl hiányzik, a sablon
       visszaesik a configban álló URL-re, és ez a rész elmarad. */
    $logo = OthLevel::logoResz();
    if ($logo) {
        array_unshift($csatolmanyok, $logo);
    }

    [$torzs, $fejlecek] = OthLevel::mime($szoveg, $html, $csatolmanyok);

    if ($valaszCim !== '') {
        /* Reply-To: a válasz a látogatóhoz megy, de a FELADÓ a saját
           domainünk marad — különben az SPF elbukik és a levél spambe kerül. */
        $fejlecek[] = 'Reply-To: ' . OthSmtp::fejlecNev($valaszNev ?: $valaszCim) . " <{$valaszCim}>";
    }
    $fejlecek[] = 'X-Mailer: okoth.hu';
    $fejlecek[] = 'Auto-Submitted: auto-generated';

    (new OthSmtp($CFG['smtp']))->kuld(
        $CFG['from']['cim'],
        $CFG['from']['nev'],
        $cimzettek,
        $targy,
        $torzs,
        $fejlecek
    );
}
