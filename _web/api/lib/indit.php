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

/*
 * AZ IDŐZÓNA A KÓDBÓL JÖN, NEM A KISZOLGÁLÓRÓL.
 *
 * A `date.timezone` az éles gépen `UTC`-n állt (mérve 2026-09-11-én), és ez a
 * webhely minden kiírt időpontját elcsúsztatta: nyáron két, télen egy órával.
 * Nem elméleti hiba — ezek látszanak is:
 *
 *   · „Beérkezett: …" az értesítő levelekben,
 *   · a jelentés keltezése,
 *   · a mentett ügyek és a feltöltött ajánlatok fájlneve (`YmdHis`),
 *   · a CRM-napló bejegyzései.
 *
 * A `crm-naplo.php` eddig egyetlen helyen, kézzel tette helyre
 * (`setTimezone(new DateTimeZone('Europe/Budapest'))`) — a többi huszonhat
 * dátumhívás viszont a kiszolgáló beállítását örökölte.
 *
 * ITT ÁLLÍTJUK BE, ugyanazzal a megfontolással, mint fölötte a hibakezelést:
 * ami a működés helyességéhez kell, azt ne a tárhely beállításaira bízzuk.
 * Így a teszt és az éles gép ugyanazt az időt írja, akkor is, ha a két cPanel
 * másképp van beállítva.
 */
date_default_timezone_set('Europe/Budapest');

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

/**
 * A BELSŐ ÉRTESÍTÉSEK MÁSOLATI CÍMEI. Külön függvény, hogy a hívás helyén
 * egyetlen szó legyen belőle, és hogy egy helyen lehessen kikapcsolni.
 *
 * CSAK A NEKÜNK SZÓLÓ LEVELEKRE való. A látogatónak küldött visszaigazolás
 * nem kaphat másolatot: az az ő levele, a mi belső címeinknek nincs helye
 * benne — se a fejlécben, se a postaládában.
 */
function oth_masolat(array $CFG): array
{
    return array_values(array_filter((array) ($CFG['cimzettek']['masolat'] ?? [])));
}

/** Levélküldés a konfigurált SMTP-n. */
function oth_kuld(array $CFG, array $cimzettek, string $targy, string $szoveg,
                  string $html, array $csatolmanyok = [], string $valaszCim = '',
                  string $valaszNev = '', array $masolat = []): void
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
    $fejlecek[] = 'X-Mailer: okotechhome.hu';
    $fejlecek[] = 'Auto-Submitted: auto-generated';

    (new OthSmtp($CFG['smtp']))->kuld(
        $CFG['from']['cim'],
        $CFG['from']['nev'],
        $cimzettek,
        $targy,
        $torzs,
        $fejlecek,
        $masolat
    );
}
