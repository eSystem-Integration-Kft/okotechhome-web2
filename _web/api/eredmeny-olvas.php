<?php
/**
 * eredmeny-olvas.php — egy mentett ÜGY visszaolvasása azonosító alapján.
 * ---------------------------------------------------------------------------
 * Két helyről hívjuk:
 *   * az `/eredmeny?id=…` lapról — ott a teljes ügy megjelenik,
 *   * a 8. szekció modulja elejéről — ott csak a gépi válaszkulcsok kellenek,
 *     hogy ne kérdezze újra azt, amit a 6. szekció már megtudott.
 *
 * MIÉRT POST, ha egyszer olvasás. A közös indítás (`lib/indit.php`) minden
 * végpontnál origin-ellenőrzést végez, és ahhoz POST kell. Ez itt nem
 * kényelmetlenség, hanem védelem: a rekordot csak a saját lapunkról lehet
 * lekérni, nem ágyazható be idegen oldalba, és az azonosító nem kerül
 * böngésző-előzménybe vagy proxynaplóba.
 *
 * TALÁLGATÁS ELLEN. Nem létező azonosítóra UGYANAZ a 404 megy, mint lejártra:
 * a kettő megkülönböztetése önmagában is információ volna.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';

$beall = $CFG['eredmeny'] ?? [];
if (empty($beall['engedelyezve'])) {
    OthVedelem::hiba(503, 'A mentett eredmények lekérése jelenleg nem elérhető.');
}

OthVedelem::sebessegkorlat('eredmeny-olvas', 40, (int) $CFG['vedelem']['ablak_perc']);

$azonosito = strtoupper(OthVedelem::szoveg($BE, 'id', 20));

/* Szigorú alak-ellenőrzés a fájlnév összeállítása ELŐTT: a bemenet nem
   tartalmazhat útvonal-elemet, és nem mutathat a könyvtáron kívülre. */
if (!preg_match('/^MA-[A-Z2-9]{4}-[A-Z2-9]{4}$/', $azonosito)) {
    OthVedelem::hiba(422, 'Az azonosító alakja nem megfelelő. A helyes alak: MA-XXXX-XXXX.');
}

$utvonal = __DIR__ . '/.eredmenyek/' . $azonosito . '.json';
if (!is_file($utvonal)) {
    OthVedelem::hiba(404, 'Ezt az azonosítót nem találjuk. Lehet, hogy elgépelés történt, vagy a mentés megőrzési ideje lejárt.');
}

$ugy = json_decode((string) @file_get_contents($utvonal), true);
if (!is_array($ugy)) {
    error_log('OTH eredmeny-olvas: sérült rekord — ' . $azonosito);
    OthVedelem::hiba(500, 'A mentett eredményt nem sikerült beolvasni.');
}

OthVedelem::valasz(200, ['ok' => true, 'ugy' => $ugy]);
