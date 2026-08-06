<?php
/**
 * ajanlat-elemzes.php — a 11. szekció ajánlat-összehasonlítója.
 * ---------------------------------------------------------------------------
 * A böngészőtől 2–3 feltöltött ajánlatot kap, a Claude API-val strukturált
 * mezőkre bontja, és JSON-ban adja vissza a táblázat celláit.
 *
 * AZ API-KULCS SOHA NEM KERÜL A BÖNGÉSZŐBE. Ez a fájl a proxy: a kulcs a
 * config.php-ban él (gitignore), a kliens csak ezt a végpontot látja.
 *
 * ÁLLÍTÁSFEGYELEM — ez a legfontosabb rész, nem a technika.
 * A modell ajánlatokról fog állításokat tenni, amelyek alapján a látogató
 * dönthet. Ezért a system prompt kötelezi arra, hogy:
 *   - CSAK azt írja le, ami a dokumentumban SZEREPEL,
 *   - a hiányt „nincs adat"-ként jelölje, ne értelmezéssel pótolja,
 *   - ne minősítsen („jobb", „ajánlott"), csak leírjon,
 *   - ne ígérjen árat, határidőt, engedélyezhetőséget.
 * A kiolvasás pontossága korlátos, különösen szkennelt vagy fotózott
 * dokumentumnál — ezt a felület is kiírja.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';
require __DIR__ . '/lib/office.php';

/* A dokumentumok kiolvasása hosszú művelet. Megosztott tárhelyen a
   max_execution_time gyakran 30–60 másodperc: a szerver a szkriptet VÁLASZ
   NÉLKÜL megöli, a böngésző pedig a végtelenségig vár. Ez volt az oka annak,
   hogy a gomb pörgött, de semmi nem történt.

   Ezért: felemeljük a futásidőt, ha a tárhely engedi, ÉS a curl időkorlátját
   ez alá állítjuk — így a hívás mindig előbb ér véget, mint a szkript, és
   marad idő értelmes hibaüzenetet visszaadni. */
@set_time_limit(180);
$phpKorlat = (int) ini_get('max_execution_time');
/* 0 = nincs korlát. Ha van, 10 másodperc tartalékot hagyunk a válasz
   összeállítására és elküldésére. */
$curlKorlat = $phpKorlat > 0 ? max(15, $phpKorlat - 10) : 150;

/* Az elemzés drága művelet: szigorúbb korlát, mint a leveleknél. */
OthVedelem::sebessegkorlat('elemzes', 5, 60);

$ai = $CFG['ai'] ?? [];
if (empty($ai['kulcs']) || $ai['kulcs'] === 'IDE_JON_AZ_API_KULCS') {
    /* A naplóba MEGKÜLÖNBÖZTETVE írjuk, mi hiányzik — a két eset más javítást
       kíván, és a kettő összemosása órákat vihet el a hibakeresésből.
       A kulcs ÉRTÉKE természetesen sosem kerül a naplóba. */
    if (!isset($CFG['ai'])) {
        error_log('OTH AI: a config.php-ban NINCS "ai" tömb. A kulcsot ebbe a szerkezetbe '
                . "kell tenni: 'ai' => ['kulcs' => '…', 'modell' => 'claude-sonnet-5'].");
    } elseif (empty($ai['kulcs'])) {
        error_log('OTH AI: az "ai" tömb megvan, de a "kulcs" mező üres.');
    } else {
        error_log('OTH AI: a "kulcs" mező még a helyőrzőt tartalmazza.');
    }
    OthVedelem::valasz(503, ['ok' => false,
        'uzenet' => 'Az automatikus elemzés jelenleg nem elérhető. Küldje el nekünk az '
                  . 'ajánlatokat, és szakértőnk átnézi őket.']);
}

/* --- a feltöltött ajánlatok ------------------------------------------------ */
$mezok = ['ajanlat_a' => 'A', 'ajanlat_b' => 'B', 'ajanlat_c' => 'C'];
$dokumentumok = [];
foreach ($mezok as $mezo => $jel) {
    if (!isset($_FILES[$mezo]) || ($_FILES[$mezo]['error'] ?? UPLOAD_ERR_NO_FILE) === UPLOAD_ERR_NO_FILE) {
        continue;
    }
    try {
        $f = OthVedelem::fajl($_FILES[$mezo], $CFG['csatolmany']);
    } catch (RuntimeException $e) {
        OthVedelem::valasz(422, ['ok' => false, 'uzenet' => "Ajánlat {$jel}: " . $e->getMessage()]);
    }
    /* A típus csak segédinformáció: NEM ez alapján állítunk semmit, a modell
       a dokumentumból olvas. */
    $tipus = OthVedelem::szoveg($BE, 'tipus_' . strtolower($jel), 60);
    $dokumentumok[$jel] = ['fajl' => $f, 'tipus' => $tipus];
}

if (count($dokumentumok) < 2) {
    OthVedelem::valasz(422, ['ok' => false,
        'uzenet' => 'Legalább két ajánlatot csatoljon — egyet nincs mihez hasonlítani.']);
}

/* --- a modellnek küldött tartalom ------------------------------------------ */
$SZEMPONTOK = [
    'teljes_ar'      => 'Teljes ár (bruttó)',
    'technologia'    => 'Milyen technológia',
    'meretezes'      => 'Mire van méretezve',
    'telepites'      => 'Telepítés tartalma',
    'vizelvezetes'   => 'Tisztított víz elvezetése',
    'engedelyezes'   => 'Engedélyezéshez szükséges dokumentáció',
    'telekadottsag'  => 'Telekadottságok figyelembevétele',
    'uzemeltetes'    => 'Éves üzemeltetési költség',
    'felelosseg'     => 'Felelősség',
    'garancia'       => 'Garancia és szerviz',
];

$SYSTEM = <<<'PROMPT'
Magyar szennyvízkezelési ajánlatokat olvasol ki és hasonlítasz össze egy weboldal
számára. A kimeneted alapján a látogató beruházási döntést hozhat, ezért a
pontosság fontosabb, mint a teljesség.

KÖTELEZŐ SZABÁLYOK
1. Csak azt írd le, ami a dokumentumban TÉNYLEGESEN szerepel. Ne következtess,
   ne egészíts ki iparági általánossággal, ne pótold a hiányt logikával.
2. Ha egy szempontról nincs adat, az érték pontosan "nincs adat" legyen.
   A hiány önmagában értékes információ a látogatónak — ne rejtsd el.
3. NE minősíts. Ne írd, hogy valami "jobb", "kedvezőbb", "ajánlott" vagy
   "hiányos". Írd le, mi szerepel, és mi nem.
4. Ne állíts semmit engedélyezhetőségről, megtérülésről, határidőről vagy
   műszaki alkalmasságról — ezeket dokumentumból nem lehet megállapítani.
5. Ha a dokumentum rosszul olvasható (szkennelt, fotózott, részleges), azt a
   "megjegyzes" mezőben jelezd. Inkább mondd, hogy bizonytalan, mint hogy tippelj.
6. Az árat pontosan úgy add vissza, ahogy a dokumentumban áll, a pénznemmel
   együtt. Ne számolj, ne kerekíts, ne váltsd át.

KIMENET
Kizárólag JSON, magyarázat és kódblokk nélkül. Szerkezet:
{"ajanlatok":{"A":{"cimke":"rövid technológiamegnevezés vagy 'nincs adat'",
"szempontok":{"kulcs":{"ertek":"…","reszlet":"…vagy null"}},
"megjegyzes":"olvashatósági észrevétel vagy null"}}}
A "reszlet" egy rövid pontosítás, ha a dokumentum tartalmaz ilyet; különben null.
PROMPT;

$szempontLista = '';
foreach ($SZEMPONTOK as $k => $nev) {
    $szempontLista .= "- {$k}: {$nev}\n";
}

$content = [[
    'type' => 'text',
    'text' => "Az alábbi ajánlatokat kell kiolvasnod. Minden ajánlathoz add meg az összes "
            . "szempontot; amelyikről nincs adat, oda pontosan „nincs adat” kerüljön.\n\n"
            . "Szempontok:\n{$szempontLista}",
]];

foreach ($dokumentumok as $jel => $d) {
    $f = $d['fajl'];
    $content[] = ['type' => 'text', 'text' => "\n--- Ajánlat {$jel} ---"];
    if ($f['mime'] === 'application/pdf') {
        $content[] = ['type' => 'document', 'source' => [
            'type' => 'base64', 'media_type' => 'application/pdf',
            'data' => base64_encode($f['adat'])]];
    } elseif ($f['mime'] === 'image/png') {
        $content[] = ['type' => 'image', 'source' => [
            'type' => 'base64', 'media_type' => 'image/png',
            'data' => base64_encode($f['adat'])]];
    } else {
        /* A DOCX és az XLSX ZIP-archívum: a szöveget kibontjuk, és úgy küldjük.
           A régi, bináris .doc/.xls nem bontható — ott marad az őszinte
           „nem olvasható", mert a félig sikerült kiolvasás téves adatot vinne
           az összehasonlításba. */
        $kibontott = OthOffice::szoveg($f['adat'], $f['mime']);
        if ($kibontott !== null && $kibontott !== '') {
            $content[] = ['type' => 'text', 'text' =>
                "(A dokumentum szöveges tartalma, táblázatból kibontva. A tördelés "
              . "elveszhetett, az értékek nem.)\n\n" . mb_substr($kibontott, 0, 60000)];
        } else {
            $content[] = ['type' => 'text', 'text' =>
                "(Ez a fájl {$f['mime']} formátumú — régi, bináris Office-formátum, "
              . "amelyet nem tudunk megbízhatóan kiolvasni. Minden szempontnál "
              . "„nincs adat” szerepeljen, a megjegyzésben pedig az, hogy a formátum "
              . "miatt nem olvasható; javasold a PDF-be mentést.)"];
        }
    }
}

/* --- hívás ----------------------------------------------------------------- */
$kereles = [
    'model'      => $ai['modell'] ?? 'claude-sonnet-5',
    'max_tokens' => 8000,   // 10 szempont × 3 ajánlat, részletekkel
    'system'     => $SYSTEM,
    'messages'   => [['role' => 'user', 'content' => $content]],
];

$ch = curl_init('https://api.anthropic.com/v1/messages');
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST           => true,
    CURLOPT_TIMEOUT        => min((int) ($ai['timeout'] ?? 120), $curlKorlat),
    CURLOPT_HTTPHEADER     => [
        'content-type: application/json',
        'x-api-key: ' . $ai['kulcs'],
        'anthropic-version: 2023-06-01',
    ],
    CURLOPT_POSTFIELDS => json_encode($kereles, JSON_UNESCAPED_UNICODE),
]);
$valasz = curl_exec($ch);
$kod = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
$curlHiba = curl_error($ch);
curl_close($ch);

if ($valasz === false || $kod !== 200) {
    /* A hibaüzenet NEM tartalmazhatja a kérést: abban a dokumentum és a kulcs
       fejléce is szerepelne. */
    error_log('OTH AI: HTTP ' . $kod . ($curlHiba ? ' · ' . $curlHiba : '')
        . ' · php_limit=' . $phpKorlat . ' curl_limit=' . $curlKorlat);
    /* Az időtúllépés MÁS üzenetet kap: azon a felhasználó tud segíteni
       (kevesebb vagy kisebb fájl), a többi hibán nem. */
    $ido = ($kod === 0 && stripos($curlHiba, 'timed out') !== false);

    /* Az API hibatípusát a naplóba írjuk. Az elgépelt modellnév és a lejárt
       kulcs a leggyakoribb beüzemelési hiba, és mindkettő ÜZEMELTETŐI javítást
       kíván — a látogatónak nincs vele dolga, ezért ő általános üzenetet kap,
       az üzemeltető viszont pontosat. */
    $hj = json_decode((string) $valasz, true);
    $apiTipus = $hj['error']['type'] ?? '';
    $apiUzenet = $hj['error']['message'] ?? '';
    if ($kod === 404 || str_contains($apiUzenet, 'model')) {
        error_log('OTH AI: a modellnév valószínűleg érvénytelen — beállítva: "'
            . ($ai['modell'] ?? '?') . '". Az érvényes azonosítót az Anthropic konzol '
            . 'modell-listája adja. API-üzenet: ' . $apiUzenet);
    } elseif ($kod === 401 || $apiTipus === 'authentication_error') {
        error_log('OTH AI: a kulcsot az API visszautasította (401). Lejárt vagy '
            . 'visszavont kulcs? A config.php ai.kulcs mezőjét kell frissíteni.');
    } elseif ($kod === 429) {
        error_log('OTH AI: az API sebességkorlátja lépett életbe (429).');
    } elseif ($apiUzenet !== '') {
        error_log('OTH AI: API-hiba (' . $kod . ') ' . $apiTipus . ': ' . $apiUzenet);
    }

    OthVedelem::valasz(502, ['ok' => false,
        'uzenet' => $ido
            ? 'A kiolvasás nem fejeződött be időben. Próbálja kevesebb vagy kisebb '
            . 'fájllal — vagy küldje el nekünk az ajánlatokat, és szakértőnk átnézi őket.'
            : 'Az elemzés most nem sikerült. Próbálja újra, vagy küldje el nekünk az '
            . 'ajánlatokat — szakértőnk átnézi őket.']);
}

$j = json_decode($valasz, true);

/* A content tömb ELSŐ eleme nem feltétlenül szöveg: a modell adhat előtte más
   típusú blokkot is. Ezért a típus alapján keressük meg, nem index szerint. */
$szoveg = '';
foreach (($j['content'] ?? []) as $blokk) {
    if (($blokk['type'] ?? '') === 'text') {
        $szoveg .= $blokk['text'] ?? '';
    }
}

/* A modell kaphat kódblokkot vagy bevezető mondatot a JSON köré. Előbb a
   kódblokk-jelöléseket szedjük le, majd — ha még mindig nem áll össze — a
   legkülső kapcsos zárójelpárt vágjuk ki. */
$szoveg = trim(preg_replace('/^```(?:json)?\s*|\s*```$/m', '', $szoveg));
$adat = json_decode($szoveg, true);
if (!is_array($adat)) {
    $eleje = strpos($szoveg, '{');
    $vege  = strrpos($szoveg, '}');
    if ($eleje !== false && $vege !== false && $vege > $eleje) {
        $adat = json_decode(substr($szoveg, $eleje, $vege - $eleje + 1), true);
    }
}

if (!is_array($adat) || empty($adat['ajanlatok'])) {
    /* A naplóba a HIBA OKA kerül és a válasz eleje — enélkül nem lehet
       megmondani, a modell írt-e prózát, kifutott-e a tokenkeretből, vagy
       más szerkezetet adott. A dokumentum tartalma nem kerül a naplóba. */
    error_log('OTH AI: értelmezhetetlen válasz.'
        . ' stop=' . ($j['stop_reason'] ?? '?')
        . ' hossz=' . strlen($szoveg)
        . ' eleje=' . substr(preg_replace('/\s+/', ' ', $szoveg), 0, 200));
    OthVedelem::valasz(502, ['ok' => false,
        'uzenet' => 'Az elemzés eredményét nem sikerült feldolgozni. Küldje el nekünk az '
                  . 'ajánlatokat, és átnézzük.']);
}

/* --- tisztítás a kimenet előtt --------------------------------------------- */
$ki = [];
foreach ($dokumentumok as $jel => $d) {
    $a = $adat['ajanlatok'][$jel] ?? [];
    $sz = [];
    foreach (array_keys($SZEMPONTOK) as $k) {
        $e = $a['szempontok'][$k] ?? [];
        $sz[$k] = [
            'ertek'   => mb_substr(OthSmtp::tisztit((string) ($e['ertek'] ?? 'nincs adat')), 0, 160),
            'reszlet' => isset($e['reszlet']) && $e['reszlet'] !== null
                ? mb_substr(OthSmtp::tisztit((string) $e['reszlet']), 0, 160) : null,
        ];
    }
    $ki[$jel] = [
        'cimke'      => mb_substr(OthSmtp::tisztit((string) ($a['cimke'] ?? 'nincs adat')), 0, 60),
        'fajlnev'    => $d['fajl']['nev'],
        'szempontok' => $sz,
        'megjegyzes' => isset($a['megjegyzes']) && $a['megjegyzes'] !== null
            ? mb_substr(OthSmtp::tisztit((string) $a['megjegyzes']), 0, 300) : null,
    ];
}

OthVedelem::valasz(200, [
    'ok'         => true,
    'ajanlatok'  => $ki,
    'szempontok' => $SZEMPONTOK,
    /* A kliens ezt írja ki a tábla fölé. A szöveg itt van, nem a JS-ben, hogy
       az elemzés jellege és a kiírt figyelmeztetés egy helyen változzon. */
    'tajekoztato' => 'Az elemzés a feltöltött dokumentumokból készült, és '
        . 'tájékoztató jellegű: nem helyettesíti a helyszíni felmérést és a szakértői '
        . 'véleményt. Ahol „nincs adat" szerepel, ott a dokumentum nem tartalmazta az '
        . 'információt — ez nem jelenti azt, hogy a szolgáltatás kimarad az ajánlatból. '
        . 'Szkennelt vagy fotózott dokumentumnál a kiolvasás pontossága korlátos.',
]);
