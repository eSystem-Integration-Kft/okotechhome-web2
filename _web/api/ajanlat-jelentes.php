<?php
/**
 * ajanlat-jelentes.php — az ajánlat-összehasonlítási jelentés elküldése.
 * ---------------------------------------------------------------------------
 * A látogató a saját e-mail-címére kéri el azt az összehasonlítást, amit a
 * böngészőjében látott. A levél KÉT részből áll:
 *
 *   * a törzsben a márkás, táblázatos összefoglaló (OthLevel sablon) — ez az,
 *     amit a postaládában megnyitva azonnal lát;
 *   * mellékletként a teljes jelentés önhordó HTML-fájlként — ez nyomtatható,
 *     archiválható, és böngészőben ugyanúgy néz ki, mint a webhelyen.
 *
 * A JELENTÉS A KLIENSTŐL JÖN, tehát IDEGEN ADAT. Semmit nem veszünk át belőle
 * HTML-ként: minden mező escape-elve kerül a levélbe és a mellékletbe is. A
 * szerkezetet (hány oszlop, milyen mezők) itt ellenőrizzük, nem bízunk benne.
 *
 * A levél KIZÁRÓLAG a megadott címre megy — másolat nem készül az irodának.
 * A látogató a saját összehasonlítását kérte el, nem megkeresést küldött; egy
 * néma másolat a háta mögött adatvédelmi meglepetés volna.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';

OthVedelem::sebessegkorlat('jelentes', 5, (int) $CFG['vedelem']['ablak_perc']);

/* TÖBB CÍMZETT. A jelentést jellemzően nem egyedül nézi meg az ember: a
   házastárs, a tervező vagy a kivitelező is megkapja. A mező ezért vesszővel
   (vagy pontosvesszővel) elválasztott listát fogad.

   Nem az `OthVedelem::email()`-t használjuk, mert az EGY címet vár, és a listát
   üresre értékelné — a látogató pedig azt látná, hogy a beírt címe „érvénytelen".
   Minden címet külön ellenőrzünk, az ismétlődéseket kiszűrjük, és ötnél
   megállunk: a végpont a saját jelentés elküldésére való, nem körlevélre. */
const MAX_CIMZETT = 5;

$cimzettek = [];
$rosszCimek = [];
foreach (preg_split('/[,;]+/', (string) ($BE['email'] ?? '')) as $nyers) {
    $c = trim($nyers);
    if ($c === '') { continue; }
    $ervenyes = filter_var($c, FILTER_VALIDATE_EMAIL);
    if ($ervenyes === false) {
        $rosszCimek[] = mb_substr($c, 0, 80);
    } elseif (!in_array($ervenyes, $cimzettek, true)) {
        $cimzettek[] = $ervenyes;
    }
}

$hozzajarul = !empty($BE['hozzajarul']);
$jelentes   = $BE['jelentes'] ?? null;

$hibak = [];
if ($rosszCimek) {
    /* A HIBÁS CÍMET VISSZAMONDJUK. „Érvénytelen e-mail-cím" önmagában
       használhatatlan öt cím közül: a látogató nem tudja, melyiket javítsa. */
    $hibak['email'] = 'Ezt a címet nem tudjuk értelmezni: '
        . implode(', ', array_map(fn($c) => '„' . $c . '”', $rosszCimek)) . '.';
} elseif (!$cimzettek) {
    $hibak['email'] = 'Kérjük, adjon meg érvényes e-mail-címet.';
} elseif (count($cimzettek) > MAX_CIMZETT) {
    $hibak['email'] = 'Egyszerre legfeljebb ' . MAX_CIMZETT . ' címre küldjük el a jelentést.';
}
if (!$hozzajarul)   { $hibak['hozzajarul'] = 'A küldéshez a hozzájárulás szükséges.'; }
if (!is_array($jelentes) || empty($jelentes['sorok']) || !is_array($jelentes['sorok'])) {
    $hibak['jelentes'] = 'Nincs mit elküldeni: futtassa le az összehasonlítást.';
}
if ($hibak) {
    OthVedelem::valasz(422, ['ok' => false, 'uzenet' => 'A beküldést pontosítani kell.', 'mezok' => $hibak]);
}

/* --- a beérkezett szerkezet megtisztítása -------------------------------- */
/** Egyetlen szövegmező: típus kikényszerítve, hossz vágva. */
$sz = static fn($v, int $max = 300): string => mb_substr(trim((string) (is_scalar($v) ? $v : '')), 0, $max);

$keszult = $sz($jelentes['keszult'] ?? '', 40);
if ($keszult === '') { $keszult = date('Y. m. d.'); }

$ajanlatok = [];
foreach (array_slice((array) ($jelentes['ajanlatok'] ?? []), 0, 3) as $a) {
    if (!is_array($a)) { continue; }
    $ajanlatok[] = [
        'jel'   => $sz($a['jel'] ?? '', 4),
        'cim'   => $sz($a['cim'] ?? '', 80),
        'cimke' => $sz($a['cimke'] ?? '', 80),
        'fajl'  => $sz($a['fajl'] ?? '', 160),
        'tipus' => $sz($a['tipus'] ?? '', 80),
    ];
}
$oszlopSzam = max(1, count($ajanlatok));

$sorok = [];
foreach (array_slice((array) $jelentes['sorok'], 0, 40) as $s) {
    if (!is_array($s)) { continue; }
    $ertekek = [];
    foreach (array_slice((array) ($s['ertekek'] ?? []), 0, $oszlopSzam) as $c) {
        $ertekek[] = is_array($c)
            ? ['ertek' => $sz($c['ertek'] ?? '', 200), 'reszlet' => $sz($c['reszlet'] ?? '', 200)]
            : ['ertek' => $sz($c, 200), 'reszlet' => ''];
    }
    $sorok[] = [
        'cimke'   => $sz($s['cimke'] ?? '', 120),
        'osszeg'  => !empty($s['osszeg']),
        'ertekek' => $ertekek,
    ];
}
if (!$sorok) {
    OthVedelem::valasz(422, ['ok' => false, 'uzenet' => 'Nincs mit elküldeni: futtassa le az összehasonlítást.']);
}

$megjegyzesek = [];
foreach (array_slice((array) ($jelentes['megjegyzesek'] ?? []), 0, 10) as $m) {
    $t = $sz($m, 600);
    if ($t !== '') { $megjegyzesek[] = $t; }
}

/* --- melléklet: önhordó HTML -------------------------------------------- */
$h = static fn(string $s): string => htmlspecialchars($s, ENT_QUOTES, 'UTF-8');

$css = @file_get_contents(__DIR__ . '/../assets/css/jelentes.css') ?: '';
$logo = @file_get_contents(__DIR__ . '/../assets/img/logo-jelentes.svg') ?: '';
if ($logo !== '' && ($p = strpos($logo, '<svg')) !== false) {
    $logo = substr($logo, $p);
} else {
    $logo = 'ÖkoTech Home';
}

$kartyak = '';
foreach ($ajanlatok as $a) {
    $reszek = '';
    if ($a['cimke'] !== '') { $reszek .= '<p class="jel-ajanlat-cimke">' . $h($a['cimke']) . '</p>'; }
    if ($a['fajl'] !== '')  { $reszek .= '<p class="jel-ajanlat-fajl">' . $h($a['fajl']) . '</p>'; }
    if ($a['tipus'] !== '') { $reszek .= '<p class="jel-ajanlat-fajl">Megadott típus: ' . $h($a['tipus']) . '</p>'; }
    $kartyak .= '<div class="jel-ajanlat"><div class="jel-ajanlat-fej">'
        . '<span class="jel-jel" aria-hidden="true">' . $h($a['jel']) . '</span>'
        . '<p class="jel-ajanlat-nev">' . $h($a['cim']) . '</p></div>' . $reszek . '</div>';
}

$fejek = '';
foreach ($ajanlatok as $a) {
    $fejek .= '<th scope="col">' . $h($a['cim'])
        . ($a['cimke'] !== '' ? '<span>' . $h($a['cimke']) . '</span>' : '') . '</th>';
}

$testSorok = '';
foreach ($sorok as $s) {
    $cellak = '';
    foreach ($s['ertekek'] as $c) {
        $cellak .= '<td><span class="jel-ertek">' . $h($c['ertek']) . '</span>'
            . ($c['reszlet'] !== '' ? '<span class="jel-reszlet">' . $h($c['reszlet']) . '</span>' : '')
            . '</td>';
    }
    $testSorok .= '<tr' . ($s['osszeg'] ? ' class="jel-osszeg"' : '') . '>'
        . '<th scope="row">' . $h($s['cimke']) . '</th>' . $cellak . '</tr>';
}

$megjBlokk = '';
if ($megjegyzesek) {
    $li = '';
    foreach ($megjegyzesek as $m) { $li .= '<li>' . $h($m) . '</li>'; }
    $megjBlokk = '<section class="jel-blokk"><h2 class="jel-blokk-cim">Megjegyzések a dokumentumokról</h2>'
        . '<ul class="jel-lista">' . $li . '</ul></section>';
}

$melleklet = '<!DOCTYPE html>
<html lang="hu"><head><meta charset="utf-8">
<title>Ajánlat-összehasonlítás — ÖkoTech Home (' . $h($keszult) . ')</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{margin:0;padding:24px;background:#F3F2EC}
' . $css . '</style></head><body>
<article class="jel">
  <header class="jel-fejlec">
    <span class="jel-logo">' . $logo . '</span>
    <p class="jel-ceg">ÖkoTech-Home Kft.<br>okotechhome.hu · ' . $h((string) $CFG['webhely']['tel']) . '<br>'
      . $h((string) ($CFG['webhely']['email'] ?? 'kapcsolat@okotechhome.hu')) . '</p>
  </header>
  <div class="jel-cimsor">
    <p class="jel-eyebrow">Ajánlat-összehasonlítás</p>
    <h1 class="jel-cim">A beküldött ajánlatok egymás mellett</h1>
    <p class="jel-datum">Készült: ' . $h($keszult) . '</p>
  </div>
  <section class="jel-blokk"><h2 class="jel-blokk-cim">Az összehasonlított ajánlatok</h2>
    <div class="jel-ajanlatok">' . $kartyak . '</div></section>
  <section class="jel-blokk"><h2 class="jel-blokk-cim">Összehasonlítás szempontok szerint</h2>
    <div class="jel-tabla-keret"><table class="jel-tabla">
      <thead><tr><th scope="col">Szempont</th>' . $fejek . '</tr></thead>
      <tbody>' . $testSorok . '</tbody>
    </table></div></section>
  ' . $megjBlokk . '
  <p class="jel-zaro"><strong>Tájékoztató jellegű összeállítás.</strong> A jelentés a beküldött
    dokumentumokból készült, és nem helyettesíti a helyszíni felmérést és a szakértői véleményt.
    Ahol „nincs adat” szerepel, ott a dokumentum nem tartalmazta az információt — ez nem jelenti
    azt, hogy a szolgáltatás kimarad az ajánlatból.</p>
  <footer class="jel-lab"><span>ÖkoTech-Home Kft. · 2509 Esztergom, Strázsa u. 12.</span>
    <span>okotechhome.hu</span><span>Készült: ' . $h($keszult) . '</span></footer>
</article></body></html>';

/* --- levél a látogatónak ------------------------------------------------- */
/* A törzs ÖSSZEFOGLALÓ, nem másolat: 600 képpont szélességben egy
   négyoszlopos összehasonlítás olvashatatlan. A teljes tábla a mellékletben van.
 *
 * MIT MUTATUNK AJÁNLATONKÉNT. A fájlnevet — erről ismerhető fel a postaládában,
 * melyik ajánlatról van szó —, és az első ÉRDEMI szempontot, elsősorban az árat.
 *
 * Korábban itt az oszlopcímke (`cimke`) állt. Az viszont gyakran „nincs adat",
 * mert az elemzés nem mindig tudja megnevezni a technológiát a dokumentumból —
 * és akkor a levélben három ajánlatból kettő mellett „nincs adat" állt, holott
 * a mellékelt táblában végig volt adat. A levél nem hazudott, csak a
 * legrosszabb mezőt választotta összefoglalónak. */

/** „nincs adat" NEM érték: hiány. Összefoglalóba nem való. */
$ures = static fn(string $v): bool =>
    $v === '' || $v === '—' || preg_match('/^\s*nincs\s+adat\s*$/iu', $v) === 1;

/** Az ajánlathoz tartozó első érdemi szempont — az árat előnyben részesítve. */
$elsoErdemi = static function (int $oszlop) use ($sorok, $ures): ?array {
    $tartalek = null;
    foreach ($sorok as $s) {
        $c = $s['ertekek'][$oszlop] ?? null;
        if (!$c || $ures((string) $c['ertek'])) { continue; }
        if (preg_match('/\bár\b|\bára\b|költség|díj/iu', $s['cimke']) === 1) {
            return ['cimke' => $s['cimke'], 'ertek' => $c['ertek']];
        }
        $tartalek ??= ['cimke' => $s['cimke'], 'ertek' => $c['ertek']];
    }
    return $tartalek;
};

$adatok = [];
foreach ($ajanlatok as $i => $a) {
    $reszek = [];
    if ($a['fajl'] !== '') {
        $reszek[] = '<span style="color:#4A4F49;font-size:13px;">' . $h($a['fajl']) . '</span>';
    }
    $fo = $elsoErdemi($i);
    if ($fo) {
        $reszek[] = $h($fo['cimke']) . ': <strong>' . $h($fo['ertek']) . '</strong>';
    }
    /* A technológiacímke csak akkor kerül ki, ha az elemzés tényleg megnevezte. */
    if (!$ures($a['cimke'])) {
        $reszek[] = '<span style="color:#4A4F49;font-size:13px;">' . $h($a['cimke']) . '</span>';
    }
    if (!$reszek) {
        $reszek[] = '<span style="color:#4A4F49;font-size:13px;">a részletek a mellékletben</span>';
    }
    $adatok[$a['cim'] !== '' ? $a['cim'] : ('Ajánlat ' . $a['jel'])] = implode('<br>', $reszek);
}

/* Az összegzősor csak akkor kerül a levélbe, ha legalább egy oszlopában van
   érték — egy csupa „—" sor semmit nem mond, csak zajt visz a levélbe. */
foreach ($sorok as $s) {
    if (!$s['osszeg']) { continue; }
    $reszek = [];
    $vanErtek = false;
    foreach ($s['ertekek'] as $i => $c) {
        $jel = $ajanlatok[$i]['jel'] ?? (string) ($i + 1);
        $ertek = (string) $c['ertek'];
        if (!$ures($ertek)) { $vanErtek = true; }
        $reszek[] = $h($jel) . ': ' . $h($ertek);
    }
    if ($vanErtek) {
        $adatok[$s['cimke']] = implode(' &nbsp;·&nbsp; ', $reszek);
    }
}

$html = OthLevel::html(
    $CFG['webhely'],
    'Ajánlat-összehasonlítás',
    'A jelentése elkészült',
    'Mellékeltük a teljes összehasonlítást HTML-fájlként — böngészőben megnyitva ugyanúgy '
    . 'néz ki, mint a webhelyen, és onnan nyomtatható vagy menthető PDF-be.',
    $adatok,
    ['felirat' => 'Szakértői átnézés kérése',
     'url' => rtrim((string) $CFG['webhely']['url'], '/') . '/kapcsolat'],
    'Az összehasonlítás tájékoztató jellegű, nem helyettesíti a helyszíni felmérést és a '
    . 'szakértői véleményt. Készült: ' . $keszult . '.'
);
$szoveg = OthLevel::szoveg($CFG['webhely'], 'A jelentése elkészült',
    'Mellékeltük a teljes ajánlat-összehasonlítást HTML-fájlként.', $adatok);

/* A KÜLDÉST KÜLÖN KAPJUK EL. Enélkül az indit.php általános kivételkezelője
   „Váratlan hiba történt" üzenetet ad, ami a látogatónak semmit nem mond, és
   nekünk sem: nem derül ki, hogy a jelentés összeállításával volt-e baj, vagy
   a levélszerverrel. A részlet a naplóba megy, a látogató pedig megtudja,
   hogy nem ő rontott el valamit. */
try {
    oth_kuld(
        $CFG,
        $cimzettek,
        'Ajánlat-összehasonlítás — ' . $CFG['webhely']['nev'],
        $szoveg,
        $html,
        [[
            'nev'  => 'okotech-ajanlat-osszehasonlitas.html',
            'mime' => 'text/html',
            'adat' => $melleklet,
        ]]
    );
} catch (Throwable $e) {
    error_log('OTH jelentés: a levélküldés nem sikerült — ' . $e->getMessage());
    OthVedelem::valasz(502, ['ok' => false,
        'uzenet' => 'A jelentés elkészült, de a levélszerver nem vette át. Töltse le HTML-ben, '
                  . 'vagy próbálja újra néhány perc múlva — ha továbbra sem megy, jelezze nekünk.']);
}

/*
 * ÁTADÁS A CRM-NEK — a levél UTÁN.
 *
 * Itt a látogató SAJÁT MAGÁNAK kéri el az összehasonlítást. Ez gyengébb jelzés
 * az átnézésnél — még nem kért tőlünk semmit —, de az e-mail-cím megvan, és a
 * beküldött ajánlatok száma elárulja, hol tart a döntésben.
 *
 * Több címzett is lehet (a látogató elküldheti a házastársának is). A CRM-be
 * az ELSŐ cím megy: az az övé, a többi továbbküldés. Mindet felvenni azt
 * jelentené, hogy olyan embereknek nyitunk kartont, akik sosem jártak nálunk.
 */
OthCrm::kuld($CFG, 'okotechhome-osszehasonlito', OthCrm::csomag(
    OthVedelem::szoveg($BE, 'ugy_azonosito', 40) ?: null,
    'jelentes-' . date('YmdHis') . '-' . substr(sha1((string) ($cimzettek[0] ?? '')), 0, 8),
    ['email' => (string) ($cimzettek[0] ?? '')],
    [
        'targy'    => 'Ajánlat-összehasonlítás elkérve — ' . count($ajanlatok) . ' ajánlat',
        'url'      => $CFG['webhely']['url'] ?? null,
        'valaszok' => array_filter([
            'összehasonlított ajánlatok' => (string) count($ajanlatok),
            'megnevezett technológiák'   => implode(', ', array_filter(array_column($ajanlatok, 'cimke'))),
            'továbbküldve'               => count($cimzettek) > 1 ? (count($cimzettek) - 1) . ' további címre' : '',
        ]),
    ],
    $hozzajarul,
));

$db = count($cimzettek);
OthVedelem::valasz(200, ['ok' => true,
    'uzenet' => $db === 1
        ? 'Elküldtük a jelentést a megadott címre. Ha pár percen belül nem érkezik meg, '
        . 'nézze meg a levélszemét mappát is.'
        : 'Elküldtük a jelentést mind a ' . $db . ' címre. Ha pár percen belül nem érkezik meg, '
        . 'nézzék meg a levélszemét mappát is.']);
