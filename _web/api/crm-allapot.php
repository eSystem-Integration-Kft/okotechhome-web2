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

/* ===========================================================================
   A MYSQL-ÚT ÁLLAPOTA
   ---------------------------------------------------------------------------
   A fenti szakasz a HTTP-kaput vizsgálja. A `crm.mod` viszont 'mysql' vagy
   'mindketto' is lehet, és olyankor a beküldés EGY MÁSIK úton megy — amit a
   HTTP-próba egyáltalán nem érint.

   AMIT ITT KIDERÍTÜNK, sorrendben, mert egymásra épülnek: van-e beállítás, van-e
   jelszó, létrejön-e a kapcsolat, megvan-e a tábla, és van-e ÍRÁSJOG. Az utolsó
   a legfontosabb: kapcsolódni bárki tud, írni nem — és a különbség csak az első
   valódi beküldésnél derülne ki, amikor már kár lett belőle.

   NEM HAGY NYOMOT. A próbaírás tranzakcióban fut, és MINDIG visszagördül.
   =========================================================================== */
echo "\n\nA MYSQL-ÚT ÁLLAPOTA\n";

$mod = (string) ($beall['mod'] ?? 'http');
echo "  szállítás ........ {$mod}\n";

$my = $beall['mysql'] ?? [];
$hasznalja = $mod === 'mysql' || $mod === 'mindketto';

if (!$hasznalja) {
    echo "  A beküldések NEM ezen az úton mennek. A lenti ellenőrzés így is\n";
    echo "  lefut, hogy átkapcsolás ELŐTT lásd, működne-e.\n";
}

$hol = ($my['socket'] ?? '') !== ''
    ? 'socket: ' . $my['socket']
    : ($my['hoszt'] ?? '(nincs)') . ':' . ($my['port'] ?? 3306);
echo "  hol .............. {$hol}\n";
echo "  adatbázis ........ " . (($my['adatbazis'] ?? '') ?: '(NINCS MEGADVA)') . "\n";
echo "  felhasználó ...... " . (($my['felhasznalo'] ?? '') ?: '(NINCS MEGADVA)') . "\n";
echo "  tábla ............ " . (($my['tabla'] ?? 'web_bekuldes')) . "\n";
/* A JELSZÓT SOSEM ÍRJUK KI, csak azt, hogy van-e. */
echo "  jelszó ........... " . (($my['jelszo'] ?? '') !== '' ? '✓ beállítva' : '✗ ÜRES') . "\n\n";

if (($my['adatbazis'] ?? '') === '' || ($my['felhasznalo'] ?? '') === '') {
    echo "  ✗ Hiányos beállítás — a kapcsolatot meg sem próbálom.\n";
} elseif (($my['jelszo'] ?? '') === '') {
    echo "  ✗ Nincs jelszó. A config a titkot fájlból olvassa:\n";
    echo "      oth-titkok/crm-db.txt  (a public_html FÖLÖTT, chmod 600)\n";
} else {
    try {
        $dsn = ($my['socket'] ?? '') !== ''
            ? 'mysql:unix_socket=' . $my['socket'] . ';dbname=' . $my['adatbazis'] . ';charset=utf8mb4'
            : 'mysql:host=' . $my['hoszt'] . ';port=' . (int) ($my['port'] ?? 3306)
              . ';dbname=' . $my['adatbazis'] . ';charset=utf8mb4';

        $pdo = new PDO($dsn, (string) $my['felhasznalo'], (string) $my['jelszo'], [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_TIMEOUT            => 3,
            PDO::ATTR_EMULATE_PREPARES   => false,
        ]);
        echo "  ✓ kapcsolat létrejött\n";

        $tabla = preg_replace('/[^A-Za-z0-9_]/', '', (string) ($my['tabla'] ?? 'web_bekuldes'));
        $van = $pdo->query("SHOW TABLES LIKE " . $pdo->quote($tabla))->fetch();
        if (!$van) {
            echo "  ✗ NINCS MEG a(z) `{$tabla}` tábla ebben az adatbázisban.\n";
            echo "    Futtasd le: scripts/crm-mysql-sema.sql\n";
        } else {
            echo "  ✓ a(z) `{$tabla}` tábla megvan\n";

            /* ÍRÁSPRÓBA, VISSZAGÖRDÍTVE. A jogosultság a MySQL-ben oszloponként
               is adható, tehát a „tudok kapcsolódni" még semmit nem jelent. */
            try {
                $pdo->beginTransaction();
                $st = $pdo->prepare("INSERT INTO {$tabla} (external_id, csatorna, forras) VALUES (?, ?, ?)");
                $st->execute(['oth-proba-' . bin2hex(random_bytes(6)), 'proba', 'crm-allapot']);
                $pdo->rollBack();
                echo "  ✓ írásjog megvan (a próbasor visszagördült, nem maradt nyoma)\n";
            } catch (Throwable $e) {
                if ($pdo->inTransaction()) { $pdo->rollBack(); }
                echo "  ✗ NINCS ÍRÁSJOG vagy a tábla szerkezete más:\n";
                echo "    " . get_class($e) . ' — ' . mb_substr($e->getMessage(), 0, 160) . "\n";
            }
        }
    } catch (Throwable $e) {
        echo "  ✗ a kapcsolat NEM jött létre: " . get_class($e) . "\n";
        echo "    " . mb_substr($e->getMessage(), 0, 200) . "\n\n";
        if (stripos((string) ($my['hoszt'] ?? ''), 'localhost') !== false) {
            echo "    ⚠ A `hoszt` értéke `localhost`. A PHP ilyenkor FIGYELMEN KÍVÜL\n";
            echo "      HAGYJA a portot, és a pdo_mysql.default_socket socketjét\n";
            echo "      használja — ha az másik MySQL, félrevezető „Access denied\"\n";
            echo "      jön. Írj `127.0.0.1`-et: az tényleg TCP-t jelent.\n";
        }
    }
}

echo "\nHa végeztél, TÖRÖLD ezt a fájlt.\n";
