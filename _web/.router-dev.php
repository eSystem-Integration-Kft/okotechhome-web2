<?php
/**
 * .router-dev.php — útválasztó a PHP beépített szerveréhez (fejlesztéshez).
 * ---------------------------------------------------------------------------
 *     php -S 127.0.0.1:8851 -t . .router-dev.php
 *
 * A `.htaccess` viselkedését utánozza: a kiterjesztés nélküli útvonalhoz
 * megkeresi a `.php` vagy `.html` párját. A HTML-t MAGA KÜLDI KI — a `return
 * false` csak akkor működne, ha a kért URI maga egy létező fájl volna; e
 * nélkül a beépített szerver a gyökér index.html-jét adja vissza minden
 * kiterjesztés nélküli címre, és a fejlesztő a főoldalt nézve hiszi, hogy a
 * lapja üres.
 *
 * ÉLESBEN NEM FUT: a feltöltésből kizárva (scripts/feltoltes.sh).
 */
$u = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$f = __DIR__ . $u;

if ($u !== '/' && file_exists($f) && !is_dir($f)) {
    return false;                       // valódi fájl: szolgálja ki a szerver
}

foreach ([$f . '.php', $f . '.html', rtrim($f, '/') . '/index.html'] as $p) {
    if (!file_exists($p) || is_dir($p)) {
        continue;
    }
    if (substr($p, -4) === '.php') {
        $_SERVER['SCRIPT_FILENAME'] = $p;
        require $p;
        return true;
    }
    header('Content-Type: text/html; charset=UTF-8');
    readfile($p);
    return true;
}
return false;
