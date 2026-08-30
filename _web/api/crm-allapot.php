<?php

declare(strict_types=1);

/**
 * crm-allapot.php — A CRM-KAPCSOLAT ÁLLAPOTA, BÖNGÉSZŐBŐL.
 *
 * Használat:
 *     https://tst.okoth.hu/api/crm-allapot.php?kod=386d5c0d9c9f0a4e
 *
 * MIÉRT VAN EGYÁLTALÁN. Ha egy kitöltés nem ér el a CRM-be, a hiba HÁROM
 * helyen lehet: nincs `crm` blokk a configban, rossz a forrás-azonosító, vagy
 * hiányzik a titok. Kívülről egyik sem látszik — a látogató visszaigazolást
 * kap, a levél megérkezik, és csak napokkal később tűnik fel, hogy a CRM üres.
 * Ez a lap megmondja, MELYIK a három közül.
 *
 * ADATLÉTREHOZÁS NÉLKÜL DOLGOZIK. Szándékosan ROSSZ aláírással kérdez: a CRM az
 * aláírást csak azután nézi meg, hogy a forrást megtalálta, tehát a válaszkód
 * elárulja a beállítás állapotát, miközben semmi nem tárolódik.
 *
 *     404 → a slug rossz, ilyen forrás nincs a CRM-ben
 *     401 → a slug JÓ, a forrás megvan
 *
 * A TITOK SOHA NEM JELENIK MEG. Csak az, hogy be van-e állítva.
 *
 * HA VÉGEZTÉL, TÖRÖLD EZT A FÁJLT. Nem szivárogtat titkot, de a forrás-slugokat
 * megmutatja — az a támadónak félkész információ.
 */

const OTH_KOD = '386d5c0d9c9f0a4e';

if (!hash_equals(OTH_KOD, (string) ($_GET['kod'] ?? ''))) {
    http_response_code(404);
    exit;
}

header('Content-Type: text/plain; charset=utf-8');

$configFajl = __DIR__ . '/config.php';

if (!is_file($configFajl)) {
    exit("✗ Nincs config.php ebben a könyvtárban.\n");
}

$CFG   = require $configFajl;
$beall = $CFG['crm'] ?? null;

if (!is_array($beall)) {
    exit("✗ A config.php-ban NINCS 'crm' blokk.\n\n"
       . "  Ez a leggyakoribb ok: a küldő ilyenkor CSENDBEN visszatér, és\n"
       . "  egyetlen kitöltés sem indul el a CRM felé.\n\n"
       . "  Másold be a config.example.php 'crm' szakaszát.\n");
}

if (empty($beall['engedelyezve'])) {
    exit("✗ A CRM-átadás ki van kapcsolva (crm.engedelyezve = false).\n");
}

$alap = rtrim((string) ($beall['url'] ?? ''), '/');

echo "Kapu: {$alap}\n";
echo "Az api/ könyvtár: " . __DIR__ . "\n\n";

/*
 * HOL VAN A TITKOK KÖNYVTÁRA?
 *
 * A `config.php` fix útvonalakat próbál, és ha egyik sem talál, a titok
 * ÜRESEN marad — a küldő pedig csendben visszatér. Ilyenkor a kérdés nem az,
 * hogy „miért nem megy", hanem az, hogy „hova tetted a mappát".
 *
 * Ez a rész végigjárja a szóba jöhető helyeket, és megmondja, MELYIK létezik.
 * Csak azt írja ki, hogy a fájl ott van-e — a tartalmához nem nyúl.
 */
echo "A TITKOK KÖNYVTÁRÁNAK KERESÉSE\n";

$jeloltek = [
    __DIR__ . '/../../oth-titkok',        // a webgyökér FÖLÖTT — ezt várja a config
    __DIR__ . '/../oth-titkok',           // a teszt-oldal gyökerében
    __DIR__ . '/oth-titkok',              // az api/ alatt
    __DIR__ . '/../../../oth-titkok',     // két szinttel a gyökér fölött
    __DIR__ . '/../../public_html/oth-titkok',
    dirname(__DIR__, 2) . '/tst.okoth.hu/oth-titkok',
];

$megvan = null;

foreach ($jeloltek as $ut) {
    $valos = realpath($ut);
    $letezik = $valos !== false && is_dir($valos);
    $proba   = $letezik && is_file($valos . '/crm-kapcsolat.txt');

    printf("  %-3s %s%s\n",
        $proba ? '✓' : ($letezik ? '·' : ' '),
        $valos !== false ? $valos : $ut,
        $proba ? '   ← ITT VANNAK A FÁJLOK' : ($letezik ? '   (a könyvtár létezik, de nincs benne crm-kapcsolat.txt)' : '   (nincs ilyen könyvtár)')
    );

    if ($proba && $megvan === null) {
        $megvan = $valos;
    }
}

if ($megvan === null) {
    echo "\n  ✗ Egyik helyen sem találom a crm-kapcsolat.txt-t.\n";
    echo "    Írd meg, pontosan hova tetted a mappát — a fenti api/ könyvtárhoz képest.\n";
} else {
    echo "\n  A config elsőként ezt nézi: " . realpath(__DIR__ . '/../..') . "/oth-titkok\n";

    if ($megvan !== realpath(__DIR__ . '/../../oth-titkok')) {
        echo "  ⚠ NEM EGYEZIK a megtalált hellyel — ezért látja üresnek a titkokat.\n";
        echo "    Vagy a mappát kell ide tenni, vagy a config útvonalát átírni.\n";
    } else {
        echo "  ✓ Egyezik. Ha mégis hiányzik a titok, a FÁJL üres vagy olvashatatlan\n";
        echo "    (jogosultság: a webszerver felhasználója tudja olvasni?).\n";
    }
}

echo "\nCSATORNÁK\n";

$csatornak = $beall['csatornak'] ?? null;

if (!is_array($csatornak)) {
    echo "⚠ RÉGI ALAKÚ CONFIG.\n\n";
    echo "  A 'crm' blokkban 'titkok' van, nem 'csatornak'. A mostani lib/crm.php\n";
    echo "  csatorna-táblát vár — ilyenkor minden küldés a „nincs beállítva ez a\n";
    echo "  csatorna\" ágon áll meg, és a naplóba ír.\n\n";
    echo "  Vagy a config.php-t kell átírni a config.example.php szerint,\n";
    echo "  vagy a lib/crm.php nem a legfrissebb a szerveren.\n";
    exit(1);
}

$hiba = 0;

foreach ($csatornak as $nev => $csat) {
    $forras = (string) ($csat['forras'] ?? '');
    $titok  = (string) ($csat['titok'] ?? '');

    $titokHiba = $titok === '' || str_contains($titok, 'IDE_');

    if ($forras === '' || str_contains($forras, 'IDE_A')) {
        printf("  %-16s ✗ nincs beállítva a forrás-azonosító\n", $nev);
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
    $curlHiba = curl_error($ch);

    if ($kod === 404) {
        printf("  %-16s ✗ NINCS ilyen forrás a CRM-ben: %s\n", $nev, $forras);
        $hiba++;
    } elseif ($kod === 401) {
        if ($titokHiba) {
            printf("  %-16s ⚠ a forrás MEGVAN, de hiányzik a titok: %s\n", $nev, $forras);
            $hiba++;
        } else {
            printf("  %-16s ✓ forrás megvan, titok beállítva: %s\n", $nev, $forras);
        }
    } elseif ($kod === 0) {
        printf("  %-16s ✗ a CRM nem érhető el innen: %s\n", $nev, $curlHiba);
        $hiba++;
    } else {
        printf("  %-16s ? HTTP %d — %s\n", $nev, $kod, mb_substr($valasz, 0, 90));
        $hiba++;
    }
}

echo "\n" . ($hiba === 0
    ? "Minden csatorna rendben. A titok helyességét csak egy valódi kitöltés igazolja.\n"
    : "{$hiba} csatorna nincs rendben — a fentiek szerint.\n");

echo "\nHa végeztél, TÖRÖLD ezt a fájlt.\n";
