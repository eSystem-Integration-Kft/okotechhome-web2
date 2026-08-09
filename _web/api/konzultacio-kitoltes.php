<?php
/**
 * konzultacio-kitoltes.php — kitöltéssegéd a konzultációkérő varázslóhoz.
 * ---------------------------------------------------------------------------
 * A látogató a saját szavaival leírja a helyzetét; ez a végpont abból a
 * varázsló mezőire képezett STRUKTURÁLT választ ad vissza. A kliens csak az
 * ÜRES mezőkbe írja be — a látogató saját válaszát soha nem írja felül.
 *
 * Miért tool-hívás és nem szabad szöveg: így a modell a séma szerinti
 * értékkészletből választ, és a kliensnek nem kell szöveget elemeznie. Ami
 * nem szerepel a leírásban, az üres marad — a találgatás itt kifejezetten
 * káros lenne, mert a látogató a saját adatának hinné.
 *
 * A kulcs SOHA nem kerül a böngészőbe: a kliens ezt a végpontot látja, a
 * végpont pedig a fájlból olvasott kulccsal hívja az API-t.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';
require __DIR__ . '/lib/ai.php';

OthVedelem::sebessegkorlat('konzultacio-kitoltes', 20, 60);

$leiras = OthVedelem::szoveg($BE, 'leiras', 4000);
if (mb_strlen($leiras) < 30) {
    OthVedelem::valasz(422, ['ok' => false, 'uzenet' => 'Írjon néhány mondatot a helyzetről.']);
}

$SYSTEM = <<<'SYS'
Egy magyar szennyvíztisztítási cég konzultációkérő űrlapjának kitöltését segíted.
A látogató szabad szöveggel leírta a helyzetét. A feladatod, hogy a leírásból
KIOLVASD az űrlap mezőinek értékét.

SZABÁLYOK
- Csak azt töltsd ki, ami a leírásból következik. Amit a szöveg nem mond ki és
  nem is következik belőle egyértelműen, azt hagyd üresen. NE TALÁLGASS: a
  látogató a saját adatának fogja hinni, amit beírsz.
- A felsorolt értékkészletből válassz; oda nem illő értéket ne adj vissza.
- A számokat egész számként add vissza, mértékegység nélkül.
- Nem adsz tanácsot, nem ígérsz árat, határidőt vagy műszaki megoldást.
  A te dolgod kizárólag az adatkiolvasás.
SYS;

$ESZKOZ = [
    'name' => 'urlap_kitoltes',
    'description' => 'Az űrlapmezők értéke a leírásból. A nem szereplő mezőket hagyd ki.',
    'input_schema' => [
        'type' => 'object',
        'properties' => [
            'ki' => ['type' => 'string', 'enum' => ['magan', 'ceg', 'onkormanyzat', 'szakmai'],
                     'description' => 'Ki keres megoldást.'],
            'szegmens' => ['type' => 'string',
                           'enum' => ['panzio', 'etterem', 'kemping', 'intezmeny', 'uzem', 'iroda', 'egyeb'],
                           'description' => 'Csak ha ki=ceg.'],
            'fazis' => ['type' => 'string',
                        'enum' => ['tajekozodas', 'telek', 'tervezes', 'epitkezes', 'csere', 'problema'],
                        'description' => 'A projekt szakasza.'],
            'jelenlegi' => ['type' => 'string',
                            'enum' => ['nincs', 'emeszto', 'oldomedence', 'biologiai', 'kozcsatorna', 'nemtudom'],
                            'description' => 'A jelenlegi megoldás az ingatlanon.'],
            'hasznalat' => ['type' => 'string',
                            'enum' => ['allando', 'szezonalis', 'hetvegi', 'valtozo']],
            'letszam'    => ['type' => 'integer', 'description' => 'Állandó létszám, fő.'],
            'csucs'      => ['type' => 'integer', 'description' => 'Csúcsterhelés, fő.'],
            'telekmeret' => ['type' => 'integer', 'description' => 'Telekméret, m2.'],
            'talajviz'   => ['type' => 'string', 'enum' => ['nem', 'idoszakos', 'igen']],
            'kut'        => ['type' => 'string', 'enum' => ['nincs', 'van', 'szomszed']],
            'surgosseg'  => ['type' => 'string', 'enum' => ['azonnal', 'honap', 'negyedev', 'tajekozodas']],
            'telepules'  => ['type' => 'string', 'description' => 'Település vagy irányítószám, ha említi.'],
        ],
        'required' => [],
    ],
];

$mezok = OthAi::keres($CFG['ai'] ?? [], $SYSTEM, $leiras, $ESZKOZ, 700);

if (!is_array($mezok)) {
    OthVedelem::valasz(503, ['ok' => false,
        'uzenet' => 'A segéd most nem érhető el. A mezőket kézzel is kitöltheti.']);
}

/* A modell válasza is BEMENET: a séma betartását nem feltételezzük, hanem
   ellenőrizzük. Csak ismert kulcs, csak megengedett érték megy vissza. */
$ENGEDETT = [];
foreach ($ESZKOZ['input_schema']['properties'] as $nev => $sema) {
    $ENGEDETT[$nev] = $sema['enum'] ?? ($sema['type'] === 'integer' ? 'int' : 'szoveg');
}

$tiszta = [];
foreach ($mezok as $nev => $ertek) {
    if (!isset($ENGEDETT[$nev]) || $ertek === null || $ertek === '') { continue; }
    $szabaly = $ENGEDETT[$nev];
    if ($szabaly === 'int') {
        $szam = (int) $ertek;
        if ($szam > 0 && $szam < 1000000) { $tiszta[$nev] = $szam; }
    } elseif ($szabaly === 'szoveg') {
        $tiszta[$nev] = mb_substr(OthSmtp::tisztit((string) $ertek), 0, 120);
    } elseif (is_array($szabaly) && in_array($ertek, $szabaly, true)) {
        $tiszta[$nev] = $ertek;
    }
}

OthVedelem::valasz(200, ['ok' => true, 'mezok' => $tiszta]);
