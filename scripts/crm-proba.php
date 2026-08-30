<?php

declare(strict_types=1);

/**
 * crm-proba.php — a CRM-kapcsolat ellenőrzése, ADATLÉTREHOZÁS NÉLKÜL.
 *
 * Használat a szerveren vagy helyben:
 *     php scripts/crm-proba.php
 *
 * MIÉRT NEM KÜLD VALÓDI BEKÜLDÉST. Egy éles próbaküldés érdeklődőt és sales
 * feladatot hozna létre, amit utána kézzel kellene kitakarítani — és amíg ott
 * van, valaki fel is hívhatja. Ehelyett SZÁNDÉKOSAN ROSSZ ALÁÍRÁSSAL küldünk:
 * a CRM az aláírást csak azután nézi meg, hogy a forrást megtalálta, tehát a
 * válaszkód elárulja, hol tart a beállítás — miközben semmi nem tárolódik.
 *
 *     404  → a `forras` NEM létezik a CRM-ben — rossz slug
 *     401  → a slug JÓ, a forrás megvan (az aláírás szándékosan rossz volt)
 *     egyéb → a kapu nem érhető el, vagy más a baj
 *
 * A titkot ez a próba NEM tudja ellenőrizni: ahhoz érvényes aláírás kellene,
 * ami már valódi beküldés lenne. Amit viszont ellenőriz: hogy a titok egyáltalán
 * MEGVAN-E, és nem maradt-e benne a minta-szöveg.
 */

$configFajl = __DIR__ . '/../_web/api/config.php';

if (! is_file($configFajl)) {
    fwrite(STDERR, "Nincs config.php: {$configFajl}\n");
    exit(1);
}

$CFG   = require $configFajl;
$beall = $CFG['crm'] ?? [];

if (empty($beall['engedelyezve'])) {
    echo "A CRM-átadás KI VAN KAPCSOLVA (crm.engedelyezve = false).\n";
    exit(1);
}

$alap = rtrim((string) ($beall['url'] ?? ''), '/');

echo "Kapu: {$alap}\n\n";

$hiba = 0;

foreach (($beall['csatornak'] ?? []) as $nev => $csat) {
    $forras = (string) ($csat['forras'] ?? '');
    $titok  = (string) ($csat['titok'] ?? '');

    /* A minta-szöveg bennfelejtése a leggyakoribb hiba: a config szintaktikailag
       helyes, a rendszer elindul, és csak a beküldéskor derül ki, hogy nem megy. */
    if ($forras === '' || str_contains($forras, 'IDE_A')) {
        printf("  %-16s ✗ nincs beállítva a forrás-azonosító\n", $nev);
        $hiba++;
        continue;
    }

    if ($titok === '' || str_contains($titok, 'IDE_')) {
        printf("  %-16s ✗ hiányzik a titok (%s)\n", $nev, $forras);
        $hiba++;
        continue;
    }

    $ch = curl_init($alap . '/' . rawurlencode($forras));

    curl_setopt_array($ch, [
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => '{}',
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_TIMEOUT        => 8,
        CURLOPT_HTTPHEADER     => [
            'Content-Type: application/json',
            'X-Dk-Timestamp: ' . time(),
            'X-Dk-Signature: sha256=szandekosan-rossz',
        ],
    ]);

    $valasz = (string) curl_exec($ch);
    $kod    = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);

    if ($kod === 401) {
        printf("  %-16s ✓ a forrás létezik: %s\n", $nev, $forras);
    } elseif ($kod === 404) {
        printf("  %-16s ✗ NINCS ilyen forrás a CRM-ben: %s\n", $nev, $forras);
        $hiba++;
    } else {
        printf("  %-16s ? HTTP %d — %s\n", $nev, $kod, mb_substr($valasz, 0, 80));
        $hiba++;
    }
}

echo "\n" . ($hiba === 0
    ? "Mind a négy forrás megvan. A titkot csak egy valódi beküldés igazolja.\n"
    : "{$hiba} csatorna nincs rendben — a fentiek szerint.\n");

exit($hiba === 0 ? 0 : 1);
