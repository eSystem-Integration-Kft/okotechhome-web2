<?php
/**
 * konzultacio.php — a konzultációkérő varázsló beküldése.
 * ---------------------------------------------------------------------------
 * Két levél megy ki:
 *   1. NEKÜNK: a teljes adatlap, és fölötte az AI szakmai briefje —
 *      előminősítés, a hiányzó adatok listája és a kockázatok. A brief a
 *      DÖNTÉST NEM HOZZA MEG, csak összeszedi, amit a látogató elmondott.
 *   2. A LÁTOGATÓNAK: visszaigazolás és személyre szabott következő lépés.
 *
 * Az AI mindkét helyen ELHAGYHATÓ: ha nem érhető el, a levelek nélküle mennek
 * ki. Egy megkeresés elvesztése összehasonlíthatatlanul drágább, mint egy
 * hiányzó bekezdés.
 *
 * A varázsló JS nélkül is ide POST-ol, ezért itt minden mező opcionális a
 * névre, e-mailre és a hozzájárulásra kivéve — a hiányzó adatokat a
 * konzultáción pótoljuk, nem az űrlapon kényszerítjük ki.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';
require __DIR__ . '/lib/ai.php';

OthVedelem::sebessegkorlat('konzultacio', (int) $CFG['vedelem']['limit'], (int) $CFG['vedelem']['ablak_perc']);

/* --- bemenet --------------------------------------------------------------- */
$nev        = OthVedelem::szoveg($BE, 'nev', 120);
$email      = OthVedelem::email($BE, 'email');
$telefon    = OthVedelem::telefon($BE, 'telefon');
$telepules  = OthVedelem::szoveg($BE, 'telepules', 120);
$leiras     = OthVedelem::szoveg($BE, 'leiras', (int) $CFG['vedelem']['max_uzenet']);
$idopont    = OthVedelem::szoveg($BE, 'idopont', 300);
$cegnev     = OthVedelem::szoveg($BE, 'cegnev', 160);
$hozzajarul = !empty($BE['hozzajarul']);
$hirlevel   = !empty($BE['hirlevel']);

/* Zárt értékkészletű mezők: a kliens bármit küldhet, ezért a listán kívüli
   érték egyszerűen üres marad. */
$LISTAK = [
    'ki'         => ['magan' => 'Magánszemély', 'ceg' => 'Vállalkozás vagy intézmény',
                     'onkormanyzat' => 'Önkormányzat vagy közösség', 'szakmai' => 'Tervező vagy kivitelező'],
    'szegmens'   => ['panzio' => 'Panzió, apartman, vendégház', 'etterem' => 'Étterem, nagykonyha',
                     'kemping' => 'Kemping, közösségi létesítmény', 'intezmeny' => 'Iskola, óvoda, intézmény',
                     'uzem' => 'Üzem, ipari vagy különleges szennyvíz', 'iroda' => 'Iroda, telephely',
                     'egyeb' => 'Egyéb'],
    'fazis'      => ['tajekozodas' => 'Még tájékozódik', 'telek' => 'Telekvásárlás előtt',
                     'tervezes' => 'Tervezés vagy engedélyeztetés', 'epitkezes' => 'Épül vagy hamarosan indul',
                     'csere' => 'Meglévőt váltana ki', 'problema' => 'Működő rendszerrel van gond'],
    'jelenlegi'  => ['nincs' => 'Nincs semmi (új építés, üres telek)', 'emeszto' => 'Zárt vagy szikkasztó emésztő',
                     'oldomedence' => 'Oldómedence tisztítómezővel', 'biologiai' => 'Biológiai tisztítóberendezés',
                     'kozcsatorna' => 'Közcsatorna, de gond van vele', 'nemtudom' => 'Nem tudja pontosan'],
    'hasznalat'  => ['allando' => 'Állandó, egész éves', 'szezonalis' => 'Szezonális',
                     'hetvegi' => 'Hétvégi, alkalmi', 'valtozo' => 'Változó'],
    'talajviz'   => ['nem' => 'Nem jellemző', 'idoszakos' => 'Időszakosan magas', 'igen' => 'Tartósan magas'],
    'kut'        => ['nincs' => 'Nincs', 'van' => 'Van a telken', 'szomszed' => 'A szomszédban van'],
    'mod'        => ['telefon' => 'Telefonos egyeztetés', 'online' => 'Online konzultáció',
                     'helyszini' => 'Helyszíni felmérés'],
    'surgosseg'  => ['azonnal' => 'Sürgős, napokon belül', 'honap' => 'Egy hónapon belül',
                     'negyedev' => 'Ebben a negyedévben', 'tajekozodas' => 'Nincs határidő'],
];
$V = [];
foreach ($LISTAK as $mezo => $lista) {
    $ertek = OthVedelem::szoveg($BE, $mezo, 40);
    $V[$mezo] = isset($lista[$ertek]) ? $ertek : '';
}

$SOKSZOROS = [
    'tunet'  => ['szag' => 'Szag', 'visszaduzzad' => 'Visszaduzzadás', 'megtelik' => 'Gyakran megtelik',
                 'leallt' => 'Leállt vagy hibát jelez', 'vizallas' => 'Pangó víz', 'hatosag' => 'Hatósági felszólítás'],
    'adatok' => ['helyszinrajz' => 'Helyszínrajz, tulajdoni lap', 'talajvizsgalat' => 'Talajvizsgálat',
                 'szivarogtatas' => 'Szivárogtatási vizsgálat', 'talajviz' => 'Talajvízszint-adat',
                 'terv' => 'Építési vagy vízjogi terv', 'ajanlat' => 'Másik ajánlat', 'semmi' => 'Egyelőre semmi'],
];
$T = [];
foreach ($SOKSZOROS as $mezo => $lista) {
    $be = $BE[$mezo] ?? ($BE[$mezo . '[]'] ?? []);
    $ki = [];
    foreach ((array) $be as $ertek) {
        if (isset($lista[$ertek]) && count($ki) < 12) { $ki[] = $lista[$ertek]; }
    }
    $T[$mezo] = $ki;
}

$szam = static function (string $kulcs, int $max) use ($BE): string {
    $ertek = (int) ($BE[$kulcs] ?? 0);
    return ($ertek > 0 && $ertek <= $max) ? (string) $ertek : '';
};
$letszam    = $szam('letszam', 2000);
$csucs      = $szam('csucs', 5000);
$telekmeret = $szam('telekmeret', 1000000);

/* --- ellenőrzés ------------------------------------------------------------ */
$hibak = [];
if (mb_strlen($nev) < 2) { $hibak['nev'] = 'Kérjük, adja meg a nevét.'; }
if ($email === '')       { $hibak['email'] = 'Kérjük, adjon meg érvényes e-mail-címet.'; }
if (!$hozzajarul)        { $hibak['hozzajarul'] = 'Az adatkezeléshez való hozzájárulás szükséges.'; }
if ($V['ki'] === '')     { $hibak['ki'] = 'Kérjük, jelölje meg, ki keres megoldást.'; }
if ($hibak) {
    OthVedelem::valasz(422, ['ok' => false, 'uzenet' => 'Néhány mezőt pontosítani kell.', 'mezok' => $hibak]);
}

/* --- adatlap --------------------------------------------------------------- */
$cimke = static fn(string $mezo): string => $LISTAK[$mezo][$V[$mezo]] ?? '';

$adatok = array_filter([
    'Név'                => OthVedelem::html($nev),
    'E-mail'             => '<a href="mailto:' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '" style="color:#2F6F82;">' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '</a>',
    'Telefon'            => $telefon !== '' ? OthVedelem::html($telefon) : '',
    'Település'          => $telepules !== '' ? OthVedelem::html($telepules) : '',
    'Megkereső'          => OthVedelem::html($cimke('ki')),
    'Létesítmény'        => OthVedelem::html($cimke('szegmens')),
    'Cég vagy intézmény' => $cegnev !== '' ? OthVedelem::html($cegnev) : '',
    'Projektszakasz'     => OthVedelem::html($cimke('fazis')),
    'Jelenlegi megoldás' => OthVedelem::html($cimke('jelenlegi')),
    'Tapasztalt tünetek' => $T['tunet'] ? OthVedelem::html(implode(', ', $T['tunet'])) : '',
    'Használat'          => OthVedelem::html($cimke('hasznalat')),
    'Állandó létszám'    => $letszam !== '' ? $letszam . ' fő' : '',
    'Csúcsterhelés'      => $csucs !== '' ? $csucs . ' fő' : '',
    'Telekméret'         => $telekmeret !== '' ? $telekmeret . ' m²' : '',
    'Talajvíz'           => OthVedelem::html($cimke('talajviz')),
    'Kút'                => OthVedelem::html($cimke('kut')),
    'Meglévő adatok'     => $T['adatok'] ? OthVedelem::html(implode(', ', $T['adatok'])) : '',
    'Konzultáció módja'  => OthVedelem::html($cimke('mod')),
    'Kért időpontok'     => $idopont !== '' ? OthVedelem::html($idopont) : '',
    'Sürgősség'          => OthVedelem::html($cimke('surgosseg')),
    'Hírlevél'           => $hirlevel ? 'Kért tájékoztatást' : '',
    'Saját leírás'       => $leiras !== '' ? OthVedelem::html($leiras) : '',
], static fn($v) => $v !== '');

/* --- AI: szakmai brief nekünk, és következő lépés a látogatónak ------------- */
$osszefoglalo = '';
$brief = '';
$aiBemenet = '';
foreach ($adatok as $k => $v) {
    if ($k === 'E-mail' || $k === 'Telefon') { continue; }   // a briefhez nem kell
    $aiBemenet .= $k . ': ' . strip_tags($v) . "\n";
}

/* A napi keret itt NEM állítja meg a beküldést: a levél AI-brief nélkül is
   kimegy. Egy elveszett megkeresés többe kerül, mint egy hiányzó bekezdés.
   Egy beküldés két AI-hívás, ezért kettőt foglalunk. */
$aiFer = OthVedelem::napiKeret('ai', (int) ($CFG['ai']['napi_keret'] ?? 400))
      && OthVedelem::napiKeret('ai', (int) ($CFG['ai']['napi_keret'] ?? 400));

if ($aiFer && $aiBemenet !== '' && !empty($CFG['ai']['kulcs'])) {
    $SYS_BRIEF = <<<'SYS'
Egy magyar szennyvíztisztítási cég belső munkatársának készítesz rövid briefet
egy beérkezett konzultációkérésről. A címzett szakember — neki tényekre és
hiányokra van szüksége, nem magyarázatra.

A brief szerkezete, magyarul, tömören:
1. Egy mondat: ki keres mit, milyen szakaszban.
2. Mire utalnak az adatok (terhelés, telek, talajvíz, jelenlegi megoldás).
3. Mi hiányzik a felelős méretezéshez — felsorolás.
4. Kockázat vagy figyelmeztetés, ha van (magas talajvíz, kút közelsége,
   szűk telek, ipari szennyvíz, hatósági ügy).

SZABÁLYOK
- Csak a megadott adatokból dolgozz. Amit nem tudsz, azt hiányként írd le.
- NE javasolj konkrét terméket, NE mondj árat, kapacitást vagy határidőt.
- Ne ismételd meg az adatlapot, azt a címzett látja alatta.
- Legfeljebb 180 szó. Sima szöveg, HTML nélkül.
SYS;
    $b = OthAi::keres($CFG['ai'], $SYS_BRIEF, $aiBemenet, null, 700);
    if (is_string($b) && $b !== '') { $brief = $b; }

    $SYS_VALASZ = <<<'SYS'
Egy magyar szennyvíztisztítási cég nevében írsz rövid, személyes hangú
bekezdést annak, aki most küldött be konzultációkérést. A címzett laikus.

Tartalma:
- Egy mondat arról, hogy értjük, hol tart.
- Mi az a 2-3 dolog, amit a konzultációig érdemes előkészítenie vagy
  megnéznie (pl. telek helyszínrajza, talajvíz tapasztalata, vízfogyasztás).

SZABÁLYOK
- NE ígérj árat, kapacitást, határidőt vagy konkrét megoldást — a javaslat a
  konzultáció dolga.
- Ne köszönj el, ne írj aláírást, ne ismételd meg az adatait.
- Legfeljebb 110 szó, magázódva, sima szöveg HTML nélkül.
SYS;
    $o = OthAi::keres($CFG['ai'], $SYS_VALASZ, $aiBemenet, null, 500);
    if (is_string($o) && $o !== '') { $osszefoglalo = $o; }
}

/* --- értesítés nekünk ------------------------------------------------------ */
$modNev = $cimke('mod') !== '' ? $cimke('mod') : 'konzultáció';
$bevezeto = "Új konzultációkérés érkezett a weboldalról.\n"
    . 'Kért forma: ' . $modNev . ($idopont !== '' ? ' · időpontok: ' . $idopont : '') . "\n";
if ($brief !== '') {
    $bevezeto .= "\nSZAKMAI BRIEF (gépi összefoglaló, ellenőrizendő):\n" . $brief . "\n";
}

$html = OthLevel::html(
    $CFG['webhely'],
    'Konzultációkérés',
    'Új konzultációkérés',
    $bevezeto,
    $adatok,
    ['felirat' => 'Válasz a megkeresőnek', 'url' => 'mailto:' . $email],
    'A megkereső címe a Reply-To fejlécben — a válasz gomb közvetlenül neki megy.'
);
$szoveg = OthLevel::szoveg($CFG['webhely'], 'Új konzultációkérés', $bevezeto, $adatok);

$cimzettek = $CFG['cimzettek']['konzultacio'] ?? ($CFG['cimzettek']['kapcsolat'] ?? []);
/* A 6. paraméter a CSATOLMÁNYOK tömbje — a válaszcím csak utána jön. */
oth_kuld($CFG, $cimzettek, 'Konzultációkérés — ' . $nev . ($telepules !== '' ? ' · ' . $telepules : ''),
    $szoveg, $html, [], $email, $nev);

/* --- visszaigazolás a látogatónak ------------------------------------------ */
if (!empty($CFG['visszaigazolas'])) {
    $vbevezeto = "Köszönjük, megkaptuk a konzultációkérését.\n"
        . 'Két munkanapon belül visszaigazoljuk az időpontot, vagy újat ajánlunk, '
        . "ha egyik megadott sáv sem fér a naptárba.\n";
    if ($osszefoglalo !== '') {
        $vbevezeto .= "\n" . $osszefoglalo . "\n";
    }
    $vbevezeto .= "\nHa sürgős, a telefon a gyorsabb út: " . $CFG['webhely']['tel'] . '.';

    /* A látogatónak a saját válaszait küldjük vissza — de az elérhetőségét nem,
       azt ő maga tudja, és a levél így rövidebb. */
    $sajat = $adatok;
    unset($sajat['Név'], $sajat['E-mail'], $sajat['Telefon'], $sajat['Település'], $sajat['Hírlevél']);

    $vhtml = OthLevel::html(
        $CFG['webhely'], 'Visszaigazolás', 'Megkaptuk a konzultációkérését',
        $vbevezeto, $sajat,
        ['felirat' => 'Vissza a weboldalra', 'url' => $CFG['webhely']['url']],
        'Erre a levélre nem szükséges válaszolnia — az időpontot külön visszaigazoljuk.'
    );
    $vszoveg = OthLevel::szoveg($CFG['webhely'], 'Megkaptuk a konzultációkérését', $vbevezeto, $sajat);

    try {
        oth_kuld($CFG, [$email], 'Megkaptuk a konzultációkérését — ' . $CFG['webhely']['nev'],
            $vszoveg, $vhtml);
    } catch (Throwable $e) {
        error_log('OTH: a konzultációs visszaigazolás nem ment ki: ' . $e->getMessage());
    }
}

OthVedelem::valasz(200, [
    'ok' => true,
    'uzenet' => 'Köszönjük, megkaptuk a konzultációkérését. Két munkanapon belül visszaigazoljuk az időpontot.',
]);
