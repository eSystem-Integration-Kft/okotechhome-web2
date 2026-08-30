<?php
/**
 * eredmeny-mentes.php — ÜGY mentése: a főoldali AI-modulok közös tárolója.
 * ---------------------------------------------------------------------------
 * EGY AZONOSÍTÓ, TÖBB MODUL. A látogató a 6. szekcióban (megoldás-ajánló) kap
 * egy `MA-XXXX-XXXX` kódot; a 8. szekció (ársávbecslő) UGYANEZT az ügyet
 * egészíti ki, nem újat nyit. Így
 *
 *   * a `/eredmeny?id=…` lapon mindkét modul kimenete együtt látszik,
 *   * a második modul nem kérdezi újra azt, amit az első már megtudott,
 *   * a CRM egyetlen rekordból látja a teljes utat, nem két töredékből.
 *
 * MI KERÜL BE ÉS MI NEM. A rekordban NINCS személyes adat: se név, se e-mail,
 * se telefonszám, se cím, se IP. Csak a modulok kérdéseire adott válaszok és a
 * belőlük SZÁMÍTOTT kimenet — pontosan az, amit a látogató a képernyőn látott.
 * (A 8. szekció e-mailes összefoglalója KÜLÖN végponton megy, és az e-mail-cím
 * nem kerül ebbe a rekordba.)
 *
 * PILLANATKÉP, NEM ÉLŐ SZÁMÍTÁS. A kimenetet a kliens küldi, és úgy tesszük el,
 * ahogy megkapta — a modul konfigurációjának verziójával együtt. Ha később
 * változik a logika, a mentett példány akkor is azt mutatja, amit MONDTUNK.
 *
 * FELÜLÍRÁS. Meglévő ügyhöz csak az adott MODUL blokkja íródik felül (a
 * látogató újrafuttathatja az ársávbecslőt). A másik modul blokkja érintetlen
 * marad. Az azonosítót ismerni kell hozzá: ez a „kulcs”, ezért nem közlünk
 * belőle semmit olyannak, aki nem ismeri.
 *
 * IDEGEN ADAT. A törzs a kliensről jön: minden mező típusra, hosszra és
 * darabszámra korlátozva kerül a fájlba, escape-elve.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';

$beall = $CFG['eredmeny'] ?? [];
if (empty($beall['engedelyezve'])) {
    OthVedelem::hiba(503, 'A mentés jelenleg nem elérhető. Az eredményt letöltheti szövegfájlként is.');
}

OthVedelem::sebessegkorlat('eredmeny-mentes', 30, (int) $CFG['vedelem']['ablak_perc']);

/* Melyik modul ír. Zárt lista: ismeretlen kulcs nem hozhat létre blokkot. */
const OTH_MODULOK = ['ajanlo', 'arsav'];

$modul = strtolower(OthVedelem::szoveg($BE, 'modul', 20));
if (!in_array($modul, OTH_MODULOK, true)) {
    OthVedelem::hiba(422, 'Ismeretlen modul.');
}

$valaszok = is_array($BE['valaszok'] ?? null) ? $BE['valaszok'] : [];
$eredmeny = is_array($BE['eredmeny'] ?? null) ? $BE['eredmeny'] : [];
if (!$valaszok || !$eredmeny) {
    OthVedelem::hiba(422, 'Hiányos eredmény — a mentés nem indítható el.');
}

/** Rövid szöveggé alakít, hosszkorláttal. */
$sz = static function ($ertek, int $max = 400): string {
    if (is_array($ertek)) { $ertek = implode(', ', array_map('strval', $ertek)); }
    return mb_substr(OthSmtp::tisztit((string) $ertek), 0, $max);
};

/** Kulcs–érték lista, darabszám- és hosszkorláttal. */
$lista = static function ($nyers, int $maxDb, int $maxHossz) use ($sz): array {
    if (!is_array($nyers)) { return []; }
    $ki = [];
    foreach ($nyers as $e) {
        if (count($ki) >= $maxDb) { break; }
        if (is_array($e)) {
            $sor = [];
            foreach (['cimke', 'szoveg'] as $k) {
                if (isset($e[$k])) { $sor[$k] = $sz($e[$k], $maxHossz); }
            }
            if ($sor) { $ki[] = $sor; }
        } else {
            $v = $sz($e, $maxHossz);
            if ($v !== '') { $ki[] = ['cimke' => $v]; }
        }
    }
    return $ki;
};

/* A GÉPI VÁLASZKULCSOK a modulok közti átadáshoz kellenek (a 8. szekció ebből
   tölti ki előre azt, amit a 6. már megkérdezett). Szigorú szűrés: csak
   azonosító-alakú kulcs és érték maradhat — ezek vezérlésre is használhatók,
   tehát nem lehet bennük semmi más. */
$kulcsSzuro = static function ($nyers): array {
    if (!is_array($nyers)) { return []; }
    $ki = [];
    foreach ($nyers as $k => $v) {
        if (count($ki) >= 20) { break; }
        $kulcs = strtolower((string) $k);
        if (!preg_match('/^[a-z0-9_-]{1,40}$/', $kulcs)) { continue; }
        $ertekek = is_array($v) ? $v : [$v];
        $tiszta = [];
        foreach ($ertekek as $e) {
            $e = strtolower((string) $e);
            if (preg_match('/^[a-z0-9_+-]{1,40}$/', $e)) { $tiszta[] = $e; }
            if (count($tiszta) >= 10) { break; }
        }
        if ($tiszta) { $ki[$kulcs] = is_array($v) ? $tiszta : $tiszta[0]; }
    }
    return $ki;
};

$blokk = [
    'mentve'        => gmdate('c'),
    'verzio'        => OthVedelem::szoveg($BE, 'verzio', 40),
    'valaszKulcsok' => $kulcsSzuro($BE['valaszKulcsok'] ?? null),
    'valaszok'      => $lista($valaszok, 20, 300),
    'eredmeny'      => [
        'irany'         => $sz($eredmeny['irany'] ?? '', 40),
        'cim'           => $sz($eredmeny['cim'] ?? '', 120),
        'termekNev'     => $sz($eredmeny['termekNev'] ?? '', 120),
        'indoklas'      => $sz($eredmeny['indoklas'] ?? '', 900),
        'kompromisszum' => $sz($eredmeny['kompromisszum'] ?? '', 900),
        'okok'          => $lista($eredmeny['okok'] ?? [], 6, 600),
        'feltetelek'    => $lista($eredmeny['feltetelek'] ?? [], 8, 600),
        'tisztazandok'  => $lista($eredmeny['tisztazandok'] ?? [], 12, 600),
    ],
];

/* ------------------------------------------------------------- AZONOSÍTÓ */

/* A készletből hiányzik a 0/O és az 1/I: az azonosítót telefonban is be kell
   tudni mondani, és papírról is le kell tudni olvasni. 32 jel, 8 karakter —
   ~1,1 ezermilliárd lehetőség; a lekérdező végpont ezen felül sebességkorlátos. */
const OTH_JELKESZLET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const OTH_AZON_ALAK  = '/^MA-[A-Z2-9]{4}-[A-Z2-9]{4}$/';

function oth_uj_azonosito(): string
{
    $h = strlen(OTH_JELKESZLET);
    $ki = '';
    for ($i = 0; $i < 8; $i++) {
        if ($i === 4) { $ki .= '-'; }
        $ki .= OTH_JELKESZLET[random_int(0, $h - 1)];
    }
    return 'MA-' . $ki;
}

$dir = __DIR__ . '/.eredmenyek';
if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) {
    OthVedelem::hiba(503, 'A mentés jelenleg nem elérhető. Az eredményt letöltheti szövegfájlként is.');
}

$keresett = strtoupper(OthVedelem::szoveg($BE, 'azonosito', 20));
$uj = true;
$azonosito = '';

/* MEGLÉVŐ ÜGY KIEGÉSZÍTÉSE. Az alak-ellenőrzés a fájlnév összeállítása ELŐTT
   fut, tehát a bemenet nem tartalmazhat útvonal-elemet. */
if ($keresett !== '' && preg_match(OTH_AZON_ALAK, $keresett) && is_file($dir . '/' . $keresett . '.json')) {
    $utvonal = $dir . '/' . $keresett . '.json';
    $ugy = json_decode((string) @file_get_contents($utvonal), true);
    if (is_array($ugy)) {
        $ugy['frissitve'] = gmdate('c');
        $ugy['modulok'][$modul] = $blokk;
        if (@file_put_contents($utvonal, json_encode($ugy, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES), LOCK_EX) !== false) {
            $azonosito = $keresett;
            $uj = false;
        }
    }
}

/* ÚJ ÜGY. Ütközésre újrapróbálunk: az `x` mód csak akkor hoz létre fájlt, ha
   még nincs — így két egyidejű kérés nem írhat egymásra. */
if ($azonosito === '') {
    for ($proba = 0; $proba < 5; $proba++) {
        $jelolt = oth_uj_azonosito();
        $utvonal = $dir . '/' . $jelolt . '.json';
        $fp = @fopen($utvonal, 'x');
        if ($fp === false) { continue; }
        $ugy = [
            'azonosito'  => $jelolt,
            'letrehozva' => gmdate('c'),
            'frissitve'  => gmdate('c'),
            'modulok'    => [$modul => $blokk],
        ];
        fwrite($fp, json_encode($ugy, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));
        fclose($fp);
        @chmod($utvonal, 0600);
        $azonosito = $jelolt;
        break;
    }
}

if ($azonosito === '') {
    OthVedelem::hiba(503, 'A mentés most nem sikerült. Kérjük, próbálja újra.');
}

/* ---------------------------------------------------------- TAKARÍTÁS */

/* A megőrzési idő KONFIGURÁCIÓS kérdés, nem kódolt érték: az adatkezelési
   tájékoztatóban közölt idővel kell egyeznie. A `frissitve` számít, nem a
   létrehozás: egy folytatott ügy nem évül el a közepén. */
$megorzesNap = (int) ($beall['megorzes_nap'] ?? 180);
if ($megorzesNap > 0 && random_int(1, 25) === 1) {
    $hatar = time() - $megorzesNap * 86400;
    foreach ((array) glob($dir . '/MA-*.json') as $regi) {
        if (is_file($regi) && filemtime($regi) < $hatar) { @unlink($regi); }
    }
}

/*
 * ÁTADÁS A CRM-NEK — SZEMÉLYES ADAT NÉLKÜL.
 *
 * EZ A NÉVTELEN ÁG. A látogató itt nem adott nevet és e-mail-címet — a modul
 * nem is kér —, tehát a CRM-ben nem lesz belőle érdeklődő: nincs kit
 * felhívni. Két dolog miatt megy mégis át:
 *
 *   1. STATISZTIKA. Ebből derül ki, hányan jutnak el a weboldalig, mire
 *      keresnek választ, és hányan hallgatnak el a megszólalás előtt. Enélkül
 *      egy jól működő, de tájékozódásra használt modul halottnak látszana.
 *   2. AZ ÜGYAZONOSÍTÓ. Ha ugyanez a látogató KÉSŐBB megadja a nevét egy
 *      másik űrlapon, a CRM ugyanezzel a kóddal visszamenőleg összekapcsolja
 *      a két beküldést — és az értékesítő már a hívás előtt tudja, mekkora
 *      házról és milyen jelenlegi megoldásról van szó.
 *
 * A `kapcsolat` blokk SZÁNDÉKOSAN üres. Ami itt nincs benne, azt a CRM sem
 * kaphatja meg — a rekord ott is névtelen marad.
 */
OthCrm::kuld($CFG, 'okotechhome-arsav', OthCrm::csomag(
    $azonosito,
    'ugy-' . $azonosito . '-' . $modul,
    [],
    [
        'targy'    => 'Névtelen modul-kitöltés: ' . $modul,
        'valaszok' => array_map(
            static fn ($v): string => is_array($v) ? implode(', ', array_map('strval', $v)) : (string) $v,
            $valaszok,
        ),
    ],
));

OthVedelem::valasz(200, [
    'ok'           => true,
    'azonosito'    => $azonosito,
    'uj'           => $uj,
    'utvonal'      => 'eredmeny?id=' . rawurlencode($azonosito),
    'megorzes_nap' => $megorzesNap,
]);
