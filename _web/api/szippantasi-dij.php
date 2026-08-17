<?php
/**
 * szippantasi-dij.php — települési szippantási díj beküldése.
 * ---------------------------------------------------------------------------
 * A `/szippantasi-dij-kalkulator` oldal adatgyűjtő űrlapja. A beküldés célja a
 * települési díjadatbázis feltöltése: a látogató a SAJÁT számláján szereplő
 * díjakat küldi be, forrásmegjelöléssel.
 *
 * MIÉRT NEM ÍRJUK KÖZVETLENÜL A KONFIGBA. A beérkező sor addig nem adat, amíg
 * valaki meg nem nézte a forrását: e-mailben érkezik, és emberi jóváhagyás után
 * kerül be az `assets/data/szippantas-konfig.js` `dijak` tömbjébe. Az
 * automatikus felvétel egy elgépelt nullát azonnal az összes látogatónak
 * kiszolgálna.
 *
 * SZEMÉLYES ADAT. A díjszabás önmagában nem személyes adat. Az e-mail-cím igen,
 * ezért az CSAK hozzájárulással küldhető be, és a mező opcionális: e-mail nélkül
 * is teljes értékű a beküldés.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';

OthVedelem::sebessegkorlat('szippantasi-dij', (int) $CFG['vedelem']['limit'], (int) $CFG['vedelem']['ablak_perc']);

/**
 * Pénz- és mennyiségérték normalizálása.
 *
 * A látogató a számláról másol: „12 000", „12.000 Ft", „3 500,-" és „3,5" is
 * érkezhet. A tizedesjel a magyar írásmódban VESSZŐ, a pont viszont ezres
 * elválasztó — ezért a pontot nem tizedesjelként értelmezzük, hanem eldobjuk,
 * kivéve ha a vessző hiányzik és a pont mögött nem három számjegy áll.
 *
 * @return float|null null = a mező üres, tehát NEM TUDJUK (ez nem nulla forint)
 */
function szip_szam(array $be, string $kulcs, float $max): ?float
{
    $nyers = trim((string) ($be[$kulcs] ?? ''));
    if ($nyers === '') {
        return null;
    }
    $t = preg_replace('/[^0-9,.\-]/u', '', $nyers) ?? '';
    if (str_contains($t, ',')) {
        $t = str_replace('.', '', $t);
        $t = str_replace(',', '.', $t);
    } elseif (preg_match('/\.\d{3}(?:\D|$)/', $t)) {
        $t = str_replace('.', '', $t);
    }
    if ($t === '' || !is_numeric($t)) {
        return null;
    }
    $v = (float) $t;
    if ($v < 0 || $v > $max) {
        return null;
    }
    return $v;
}

/* A vármegyekódok zárt értékkészlete. A kliens listából választ, de a POST
   szabadon szerkeszthető — a szerver ezért újraellenőrzi. */
const SZIP_MEGYEK = [
    'BK' => 'Bács-Kiskun',            'BA' => 'Baranya',
    'BE' => 'Békés',                  'BZ' => 'Borsod-Abaúj-Zemplén',
    'BU' => 'Budapest',               'CS' => 'Csongrád-Csanád',
    'FE' => 'Fejér',                  'GS' => 'Győr-Moson-Sopron',
    'HB' => 'Hajdú-Bihar',            'HE' => 'Heves',
    'JN' => 'Jász-Nagykun-Szolnok',   'KE' => 'Komárom-Esztergom',
    'NO' => 'Nógrád',                 'PE' => 'Pest',
    'SO' => 'Somogy',                 'SZ' => 'Szabolcs-Szatmár-Bereg',
    'TO' => 'Tolna',                  'VA' => 'Vas',
    'VE' => 'Veszprém',               'ZA' => 'Zala',
];

const SZIP_FORRASOK = [
    'szamla'        => 'Saját számla',
    'artablazat'    => 'Szolgáltatói ártáblázat vagy weboldal',
    'rendelet'      => 'Önkormányzati rendelet',
    'telefon'       => 'Telefonos tájékoztatás a szolgáltatótól',
    'egyeb'         => 'Egyéb',
];

$megye      = OthVedelem::szoveg($BE, 'megye', 4);
$telepules  = OthVedelem::szoveg($BE, 'telepules', 120);
$szolgaltato= OthVedelem::szoveg($BE, 'szolgaltato', 160);
$ervenyes   = OthVedelem::szoveg($BE, 'ervenyes', 40);
$forras     = OthVedelem::szoveg($BE, 'forras', 40);
$megjegyzes = OthVedelem::szoveg($BE, 'megjegyzes', 1500);
$email      = OthVedelem::email($BE, 'email');
$hozzajarul = !empty($BE['hozzajarul']);

/* Felső korlátok: nem a valóságot írják le, hanem az elgépelést fogják meg.
   Egy 9 000 000 Ft-os kiszállási díj nem díjszabás, hanem hiba. */
$kiszallas  = szip_szam($BE, 'kiszallas',   1000000.0);
$uritesM3   = szip_szam($BE, 'uritesM3',     500000.0);
$minimumDij = szip_szam($BE, 'minimumDij',  2000000.0);
$minimumM3  = szip_szam($BE, 'minimumM3',        50.0);
$kocsiM3    = szip_szam($BE, 'kocsiM3',          50.0);
$kmDij      = szip_szam($BE, 'kmDij',         50000.0);

$hibak = [];
if (mb_strlen($telepules) < 2) {
    $hibak['telepules'] = 'Kérjük, adja meg a település nevét.';
}
if (!isset(SZIP_MEGYEK[$megye])) {
    $hibak['megye'] = 'Kérjük, válasszon vármegyét.';
}
if (!isset(SZIP_FORRASOK[$forras])) {
    $hibak['forras'] = 'Kérjük, jelölje meg, honnan származik az adat.';
}
/* Legalább egy díjtételnek lennie kell — különben a beküldés csak egy
   településnevet rögzítene, ami az adatbázisban semmit nem ér. */
if ($kiszallas === null && $uritesM3 === null && $minimumDij === null) {
    $hibak['uritesM3'] = 'Legalább egy díjtételt adjon meg (kiszállási, ürítési vagy minimumdíj).';
}
/* Az e-mail-cím személyes adat: hozzájárulás nélkül nem kérjük és nem
   kezeljük. Enélkül is teljes értékű a beküldés. */
if ($email !== '' && !$hozzajarul) {
    $hibak['hozzajarul'] = 'Az e-mail-cím megadásához az adatkezelési hozzájárulás szükséges.';
}
if ($hibak) {
    OthVedelem::valasz(422, ['ok' => false, 'uzenet' => 'Néhány mezőt pontosítani kell.', 'mezok' => $hibak]);
}

/** Megjelenítés: az üres mező „nem tudjuk", a nulla viszont valódi érték. */
$dij = static function (?float $v, string $egyseg): string {
    if ($v === null) {
        return 'nem adta meg';
    }
    return number_format($v, ($v == floor($v) ? 0 : 1), ',', "\u{00A0}") . "\u{00A0}" . $egyseg;
};

$adatok = [
    'Vármegye'            => OthVedelem::html(SZIP_MEGYEK[$megye]),
    'Település'           => OthVedelem::html($telepules),
    'Szolgáltató'         => $szolgaltato !== '' ? OthVedelem::html($szolgaltato) : '',
    'Kiszállási / alapdíj'=> OthVedelem::html($dij($kiszallas, 'Ft/alkalom')),
    'Ürítési díj'         => OthVedelem::html($dij($uritesM3, 'Ft/m³')),
    'Minimumdíj'          => OthVedelem::html($dij($minimumDij, 'Ft/alkalom')),
    'Ebben foglalt mennyiség' => OthVedelem::html($dij($minimumM3, 'm³')),
    'Szippantóautó űrtartalma' => OthVedelem::html($dij($kocsiM3, 'm³')),
    'Távolságarányos díj' => OthVedelem::html($dij($kmDij, 'Ft/km')),
    'Mikortól érvényes'   => $ervenyes !== '' ? OthVedelem::html($ervenyes) : '',
    'Forrás'              => OthVedelem::html(SZIP_FORRASOK[$forras]),
    'Megjegyzés'          => $megjegyzes !== '' ? OthVedelem::html($megjegyzes) : '',
    'Beküldő e-mail-címe' => $email !== '' ? OthVedelem::html($email) : 'nem adta meg',
];

$cim = $telepules . ' (' . SZIP_MEGYEK[$megye] . ') — szippantási díj';

$html = OthLevel::html(
    $CFG['webhely'],
    'Díjadat a kalkulátorból',
    $cim,
    'Egy látogató beküldte a településén érvényes szippantási díjakat. '
  . 'A sor CSAK ellenőrzés után kerülhet be a szippantas-konfig.js `dijak` tömbjébe — '
  . 'a forrást és a nagyságrendet nézze át, mielőtt felveszi.',
    $adatok,
    $email !== '' ? ['felirat' => 'Válasz a beküldőnek', 'url' => 'mailto:' . $email] : [],
    'Beérkezett: ' . date('Y. m. d. H:i')
      . ' · IP: ' . htmlspecialchars((string) ($_SERVER['REMOTE_ADDR'] ?? '—'), ENT_QUOTES, 'UTF-8')
);
$szoveg = OthLevel::szoveg($CFG['webhely'], $cim,
    'Egy látogató beküldte a településén érvényes szippantási díjakat. Ellenőrzés után vehető fel az adatbázisba.',
    $adatok, 'Beérkezett: ' . date('Y. m. d. H:i'));

/* Ha a configban nincs külön címzett, a kapcsolati postafiókba megy — a
   beküldés így akkor sem vész el, ha a config még nem lett kiegészítve. */
$cimzettek = $CFG['cimzettek']['szippantasi-dij'] ?? $CFG['cimzettek']['kapcsolat'];

oth_kuld($CFG, $cimzettek, '[Weboldal] Díjadat — ' . $cim, $szoveg, $html, [],
    $email, $telepules);

OthVedelem::valasz(200, [
    'ok' => true,
    'uzenet' => 'Köszönjük — megkaptuk. Az adatot a forrás ellenőrzése után vesszük fel '
              . 'az adatbázisba, ezért nem jelenik meg azonnal a térképen.',
]);
