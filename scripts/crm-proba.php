<?php

declare(strict_types=1);

/**
 * crm-proba.php — a CRM-kapcsolat ellenőrzése, ADATLÉTREHOZÁS NÉLKÜL.
 *
 * Használat:  php scripts/crm-proba.php
 *
 * MIÉRT NEM KÜLD VALÓDI BEKÜLDÉST. Egy éles próbaküldés érdeklődőt és sales
 * feladatot hozna létre, amit utána kézzel kellene kitakarítani — és amíg ott
 * van, valaki fel is hívhatja. Ehelyett SZÁNDÉKOSAN ROSSZ ALÁÍRÁSSAL küldünk: a
 * CRM az aláírást csak azután nézi meg, hogy a forrást megtalálta, tehát a
 * válaszkód elárulja a beállítás állapotát, miközben semmi nem tárolódik.
 *
 *     404 → a slug rossz, ilyen forrás nincs a CRM-ben
 *     401 → a slug jó, a forrás megvan
 *
 * A titkot ez nem igazolja — ahhoz érvényes aláírás kellene, ami már valódi
 * beküldés lenne. Azt viszont megnézi, hogy a titok egyáltalán megvan-e.
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

    /* A MINTA-SZÖVEG BENNFELEJTÉSE a leggyakoribb hiba: a config
       szintaktikailag helyes, a rendszer elindul, és csak az első valódi
       kitöltéskor derülne ki, hogy nem megy sehova. */
    $titokHiba = $titok === '' || str_contains($titok, 'IDE_');

    if ($forras === '' || str_contains($forras, 'IDE_A')) {
        printf("  %-16s ✗ nincs beállítva a forrás-azonosító\n", $nev);
        $hiba++;
        continue;
    }

    /*
     * A SLUGOT AKKOR IS MEGNÉZZÜK, HA A TITOK HIÁNYZIK.
     *
     * A két hiba független, és a beállítás két külön lépésben történik: előbb a
     * forrás felvétele a CRM-ben, aztán a titok kimásolása. Ha a hiányzó titok
     * miatt kihagynánk a slug-ellenőrzést, csak a következő futáson derülne ki,
     * hogy az is rossz — vagyis kétszer kellene ugyanazt körbejárni.
     */
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

    if ($kod === 404) {
        printf("  %-16s ✗ NINCS ilyen forrás a CRM-ben: %s\n", $nev, $forras);
        $hiba++;
    } elseif ($kod !== 401) {
        printf("  %-16s ? HTTP %d — %s\n", $nev, $kod, mb_substr($valasz, 0, 80));
        $hiba++;
    } elseif ($titokHiba) {
        printf("  %-16s ⚠ a forrás MEGVAN, de hiányzik a titok: %s\n", $nev, $forras);
        $hiba++;
    } else {
        printf("  %-16s ✓ forrás megvan, titok beállítva: %s\n", $nev, $forras);
    }
}

echo "\n" . ($hiba === 0
    ? "Minden csatorna rendben. A titkot csak egy valódi beküldés igazolja.\n"
    : "{$hiba} csatorna nincs rendben — a fentiek szerint.\n");

exit($hiba === 0 ? 0 : 1);
