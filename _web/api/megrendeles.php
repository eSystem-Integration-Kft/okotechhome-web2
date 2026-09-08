<?php
/**
 * megrendeles.php — a Megrendelőlap beküldése.
 * ---------------------------------------------------------------------------
 * A megrendelés JOGI NYILATKOZAT, nem érdeklődés. Ezért itt három dolog más,
 * mint a többi űrlapnál:
 *
 *   1. A KÖTELEZŐ NYILATKOZATOK a szerveren is kötelezők. A jelölőnégyzet a
 *      kliensen `required`, de az ellenőrzés megkerülhető — a feltételek
 *      elfogadása nélkül érkező beküldést itt utasítjuk vissza.
 *   2. A LEVÉL A BIZONYÍTÉK. A megrendelés minden adatát tételesen tartalmazza,
 *      időbélyeggel és IP-vel, mert ez az, ami a postaládában megmarad.
 *   3. A VISSZAIGAZOLÁS NEM SZERZŐDÉSKÖTÉS. A látogatónak küldött levél
 *      kimondja, hogy a szerződés az ÖkoTech-Home külön visszaigazolásával jön
 *      létre — különben a rendszerüzenet elfogadásnak látszana.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';

OthVedelem::sebessegkorlat('megrendeles', (int) $CFG['vedelem']['limit'], (int) $CFG['vedelem']['ablak_perc']);

/* --- bemenet ------------------------------------------------------------- */
$ajanlat   = OthVedelem::szoveg($BE, 'ajanlat_sorszam', 60);
$datum     = OthVedelem::szoveg($BE, 'datum', 20);
$keltHely  = OthVedelem::szoveg($BE, 'kelt_hely', 120);
$nev       = OthVedelem::szoveg($BE, 'megrendelo_neve', 160);
$telefon   = OthVedelem::telefon($BE, 'megrendelo_telefon');
$kNev      = OthVedelem::szoveg($BE, 'kapcsolattarto_neve', 160);
$kTel      = OthVedelem::telefon($BE, 'kapcsolattarto_telefonszama');
$email     = OthVedelem::email($BE, 'email');
$adoszam   = OthVedelem::szoveg($BE, 'adoszam', 40);
$lakhely   = OthVedelem::szoveg($BE, 'lakhely', 200);
$szlaNev   = OthVedelem::szoveg($BE, 'szamlazasi_nev', 160);
$szlaCim   = OthVedelem::szoveg($BE, 'szamlazasi_cim', 200);
$postacim  = OthVedelem::szoveg($BE, 'postacim', 200);
$helyszin  = OthVedelem::szoveg($BE, 'cim', 240);
$alairo    = OthVedelem::szoveg($BE, 'megrendelo_signo', 160);
$megjegyzes = OthVedelem::szoveg($BE, 'megjegyzes', 2000);

/* Zárt értékkészlet: a levélben csak olyan felirat jelenhet meg, amit MI
   írtunk — a kliens értéke csak kulcs. */
$VALASZTHATO = [
    'kivitelezes'    => ['szereléssel', 'szerelés nélkül'],
    'uzembehelyezes' => ['üzembe helyezéssel', 'üzembe helyezés nélkül'],
    'szallitas'      => ['ÖkoTech-Home általi szállítással', 'saját szállítóeszközzel'],
];
$valasztott = [];
foreach ($VALASZTHATO as $mezo => $ertekek) {
    $e = OthVedelem::szoveg($BE, $mezo, 60);
    $valasztott[$mezo] = in_array($e, $ertekek, true) ? $e : '';
}

$eszamla     = !empty($BE['eszamla']);
$feltetelek  = !empty($BE['feltetelek']);
$hozzajarul  = !empty($BE['hozzajarul']);
$karbantartas = !empty($BE['karbantartas']);
$hirlevel    = !empty($BE['hirlevel']);

/* --- ellenőrzés ---------------------------------------------------------- */
$hibak = [];
if ($ajanlat === '')            { $hibak['ajanlat_sorszam'] = 'A megrendelőlap csak érvényes árajánlat sorszámával együtt érvényes.'; }
if ($datum === '')              { $hibak['datum'] = 'Kérjük, adja meg a keltezés dátumát.'; }
if (mb_strlen($keltHely) < 2)   { $hibak['kelt_hely'] = 'Kérjük, adja meg, hol kelt a megrendelés.'; }
if (mb_strlen($nev) < 2)        { $hibak['megrendelo_neve'] = 'Kérjük, adja meg a megrendelő nevét.'; }
if ($telefon === '')            { $hibak['megrendelo_telefon'] = 'Kérjük, adjon meg telefonszámot.'; }
if ($email === '')              { $hibak['email'] = 'Kérjük, adjon meg érvényes e-mail-címet.'; }
if (mb_strlen($lakhely) < 5)    { $hibak['lakhely'] = 'Kérjük, adja meg az állandó lakhelyet vagy székhelyet.'; }
if (mb_strlen($szlaNev) < 2)    { $hibak['szamlazasi_nev'] = 'Kérjük, adja meg a számlázási nevet.'; }
if (mb_strlen($szlaCim) < 5)    { $hibak['szamlazasi_cim'] = 'Kérjük, adja meg a számlázási címet.'; }
if (mb_strlen($helyszin) < 5)   { $hibak['cim'] = 'A telepítés helyszíne és helyrajzi száma nélkül nem visszaigazolható a megrendelés.'; }
if (mb_strlen($alairo) < 2)     { $hibak['megrendelo_signo'] = 'Kérjük, adja meg az aláíró nevét.'; }
foreach ($valasztott as $mezo => $ertek) {
    if ($ertek === '') { $hibak[$mezo] = 'Kérjük, válasszon a lehetőségek közül.'; }
}
if (!$eszamla)    { $hibak['eszamla'] = 'Az elektronikus számla elfogadása szükséges.'; }
if (!$feltetelek) { $hibak['feltetelek'] = 'A megrendelési feltételek elfogadása nélkül a megrendelés nem küldhető be.'; }
if (!$hozzajarul) { $hibak['hozzajarul'] = 'Az adatkezeléshez való hozzájárulás szükséges.'; }

$csatolmanyok = OthVedelem::fajlLista($_FILES['fajl'] ?? null, $CFG['csatolmany'], $fajlHiba);
if ($fajlHiba !== '') { $hibak['fajl'] = $fajlHiba; }

if ($hibak) {
    OthVedelem::valasz(422, ['ok' => false, 'uzenet' => 'A megrendelés néhány pontját ki kell egészíteni.', 'mezok' => $hibak]);
}

/* --- a megrendelés adatlapja --------------------------------------------- */
$azonosito = 'MR-' . date('Ymd-His') . '-' . strtoupper(substr(sha1($email . $ajanlat), 0, 4));
$cimSor = 'Megrendelés — ' . $nev . ' (ajánlat: ' . $ajanlat . ')';

$adatok = [
    'Megrendelés azonosítója' => OthVedelem::html($azonosito),
    'Hivatkozott árajánlat'   => OthVedelem::html($ajanlat),
    'Kelt'                    => OthVedelem::html(($keltHely !== '' ? $keltHely . ', ' : '') . $datum),
    'Megrendelő neve'         => OthVedelem::html($nev),
    'Megrendelő telefonja'    => OthVedelem::html($telefon),
    'Kapcsolattartó'          => $kNev !== '' ? OthVedelem::html($kNev . ($kTel !== '' ? ' · ' . $kTel : '')) : '',
    'E-mail'                  => '<a href="mailto:' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '" style="color:#2F6F82;">' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '</a>',
    'Állandó lakhely / székhely' => OthVedelem::html($lakhely),
    'Számlázási név'          => OthVedelem::html($szlaNev),
    'Számlázási cím'          => OthVedelem::html($szlaCim),
    'Postacím'                => $postacim !== '' ? OthVedelem::html($postacim) : '',
    'Adószám'                 => $adoszam !== '' ? OthVedelem::html($adoszam) : '',
    'Telepítés helyszíne'     => OthVedelem::html($helyszin),
    'Kivitelezés'             => OthVedelem::html($valasztott['kivitelezes']),
    'Üzembe helyezés'         => OthVedelem::html($valasztott['uzembehelyezes']),
    'Szállítás'               => OthVedelem::html($valasztott['szallitas']),
    'Megjegyzés'              => $megjegyzes !== '' ? OthVedelem::html($megjegyzes) : '',
    'Mellékletek'             => $csatolmanyok ? OthVedelem::html(implode(', ', array_column($csatolmanyok, 'nev'))) : '',
    'Aláíró neve'             => OthVedelem::html($alairo),
    'Nyilatkozatok'           => OthVedelem::html(implode(' · ', array_filter([
        $feltetelek   ? 'Megrendelési feltételek elfogadva' : '',
        $eszamla      ? 'Elektronikus számla elfogadva' : '',
        $karbantartas ? 'Karbantartási tájékoztatás kérve' : '',
        $hirlevel     ? 'Hírlevélre feliratkozott' : '',
        $hozzajarul   ? 'Adatkezelési hozzájárulás megadva' : '',
    ]))),
];

$html = OthLevel::html(
    $CFG['webhely'],
    'Megrendelés a weboldalról',
    $cimSor,
    'Az alábbi megrendelés érkezett a megrendelőlapon. A szerződés az ÖkoTech-Home '
    . 'visszaigazolásával jön létre — kérjük, ellenőrizze az ajánlat sorszámát és a tételeket.',
    $adatok,
    ['felirat' => 'Válasz a megrendelőnek', 'url' => 'mailto:' . $email],
    'Beérkezett: ' . date('Y. m. d. H:i') . ' · IP: ' . htmlspecialchars((string) ($_SERVER['REMOTE_ADDR'] ?? '—'), ENT_QUOTES, 'UTF-8')
);
$szoveg = OthLevel::szoveg($CFG['webhely'], $cimSor,
    'Az alábbi megrendelés érkezett a megrendelőlapon.', $adatok,
    'Beérkezett: ' . date('Y. m. d. H:i'));

$cimzett = $CFG['cimzettek']['megrendeles'] ?? $CFG['cimzettek']['kapcsolat'];
oth_kuld($CFG, $cimzett, '[MEGRENDELÉS] ' . $cimSor, $szoveg, $html, $csatolmanyok, $email, $nev);

/* --- visszaigazolás a megrendelőnek -------------------------------------- */
if (!empty($CFG['visszaigazolas'])) {
    $vhtml = OthLevel::html(
        $CFG['webhely'],
        'Visszaigazolás',
        'Megkaptuk a megrendelését',
        "Köszönjük. A megrendelést munkatársunk ellenőrzi, és külön levélben visszaigazolja — "
        . "a szerződés ezzel a visszaigazolással jön létre.\n"
        . 'Kérdés esetén: ' . $CFG['webhely']['tel'] . '.',
        [
            'Megrendelés azonosítója' => OthVedelem::html($azonosito),
            'Hivatkozott árajánlat'   => OthVedelem::html($ajanlat),
            'Telepítés helyszíne'     => OthVedelem::html($helyszin),
            'Kivitelezés'             => OthVedelem::html($valasztott['kivitelezes']),
            'Üzembe helyezés'         => OthVedelem::html($valasztott['uzembehelyezes']),
            'Szállítás'               => OthVedelem::html($valasztott['szallitas']),
        ],
        ['felirat' => 'Vissza a weboldalra', 'url' => $CFG['webhely']['url']],
        'Ez a levél a beküldés visszaigazolása, nem a megrendelés elfogadása.'
    );
    $vszoveg = OthLevel::szoveg($CFG['webhely'], 'Megkaptuk a megrendelését',
        'A megrendelést munkatársunk ellenőrzi, és külön levélben visszaigazolja — a szerződés ezzel jön létre.',
        ['Megrendelés azonosítója' => OthVedelem::html($azonosito),
         'Hivatkozott árajánlat'   => OthVedelem::html($ajanlat)]);

    try {
        oth_kuld($CFG, [$email], 'Megkaptuk a megrendelését — ' . $CFG['webhely']['nev'], $vszoveg, $vhtml);
    } catch (Throwable $e) {
        error_log('OTH: a megrendelés visszaigazolása nem ment ki: ' . $e->getMessage());
    }
}

/* --- átadás a CRM-nek (a levelek UTÁN) ----------------------------------- */
OthCrm::kuld($CFG, 'megrendeles', OthCrm::csomag(
    OthVedelem::szoveg($BE, 'ugy_azonosito', 40) ?: null,
    $azonosito,
    ['nev' => $nev, 'email' => $email, 'telefon' => $telefon, 'cegnev' => $szlaNev],
    [
        'targy'    => 'Megrendelés — ' . $ajanlat,
        'uzenet'   => $megjegyzes,
        'url'      => $CFG['webhely']['url'] ?? null,
        'valaszok' => array_filter([
            'árajánlat sorszáma'  => $ajanlat,
            'telepítés helyszíne' => $helyszin,
            'kivitelezés'         => $valasztott['kivitelezes'],
            'üzembe helyezés'     => $valasztott['uzembehelyezes'],
            'szállítás'           => $valasztott['szallitas'],
            'számlázási név'      => $szlaNev,
            'számlázási cím'      => $szlaCim,
            'adószám'             => $adoszam,
            'hírlevél'            => $hirlevel ? 'igen' : 'nem',
        ]),
    ],
    $hozzajarul,
));

OthVedelem::valasz(200, [
    'ok' => true,
    'uzenet' => 'Köszönjük, megkaptuk a megrendelését (' . $azonosito . '). '
              . 'Munkatársunk ellenőrzi, és külön levélben visszaigazolja — a szerződés ezzel jön létre.',
]);
