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

/* Az elemzés drága művelet: szigorúbb korlát, mint a leveleknél. */
OthVedelem::sebessegkorlat('elemzes', 5, 60);

$ai = $CFG['ai'] ?? [];
if (empty($ai['kulcs']) || $ai['kulcs'] === 'IDE_JON_AZ_API_KULCS') {
    error_log('OTH: hiányzik az AI API-kulcs a config.php-ból.');
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
        /* DOC/XLS: a bináris tartalmat nem küldjük el — a modell nem tudja
           megbízhatóan olvasni, és a félreolvasás rosszabb, mint a nemleges válasz. */
        $content[] = ['type' => 'text', 'text' =>
            "(Ez a fájl {$f['mime']} formátumú, amelyet nem tudunk megbízhatóan kiolvasni. "
          . "Minden szempontnál „nincs adat” szerepeljen, a megjegyzésben pedig az, hogy a "
          . "formátum miatt nem olvasható.)"];
    }
}

/* --- hívás ----------------------------------------------------------------- */
$kereles = [
    'model'      => $ai['modell'] ?? 'claude-sonnet-5',
    'max_tokens' => 4000,
    'system'     => $SYSTEM,
    'messages'   => [['role' => 'user', 'content' => $content]],
];

$ch = curl_init('https://api.anthropic.com/v1/messages');
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST           => true,
    CURLOPT_TIMEOUT        => (int) ($ai['timeout'] ?? 120),
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
    error_log('OTH AI: HTTP ' . $kod . ($curlHiba ? ' · ' . $curlHiba : ''));
    OthVedelem::valasz(502, ['ok' => false,
        'uzenet' => 'Az elemzés most nem sikerült. Próbálja újra, vagy küldje el nekünk az '
                  . 'ajánlatokat — szakértőnk átnézi őket.']);
}

$j = json_decode($valasz, true);
$szoveg = $j['content'][0]['text'] ?? '';
/* A modell kaphat kódblokkot a szöveg köré; leszedjük, mielőtt dekódolnánk. */
$szoveg = trim(preg_replace('/^```(?:json)?|```$/m', '', $szoveg));
$adat = json_decode($szoveg, true);

if (!is_array($adat) || empty($adat['ajanlatok'])) {
    error_log('OTH AI: értelmezhetetlen válasz.');
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
