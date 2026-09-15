<?php
/**
 * ajanlat.php — az Ajánlatkérés oldal űrlapja.
 * ---------------------------------------------------------------------------
 * Két levél megy ki: az ajánlatkérés nekünk (a látogató címével Reply-To-ban,
 * a csatolt helyszínrajzokkal együtt), és a visszaigazolás a látogatónak.
 *
 * MIÉRT KÜLÖN VÉGPONT, ÉS NEM A `kapcsolat.php` EGY MEZŐVEL. Az ajánlatkérés
 * más adatokat kér (ingatlantípus, létszám, jelenlegi megoldás, tervezett
 * kezdés), MELLÉKLETET fogad, és más postaládába megy. Egy közös végpont
 * mindhármat feltételes ágakkal oldaná meg — az ilyen elágazás az, ami később
 * némán elromlik.
 */

declare(strict_types=1);
require __DIR__ . '/lib/indit.php';

OthVedelem::sebessegkorlat('ajanlat', (int) $CFG['vedelem']['limit'], (int) $CFG['vedelem']['ablak_perc']);

/* --- bemenet ------------------------------------------------------------- */
$nev       = OthVedelem::szoveg($BE, 'nev', 120);
$email     = OthVedelem::email($BE, 'email');
$telefon   = OthVedelem::telefon($BE, 'telefon');
$cegnev    = OthVedelem::szoveg($BE, 'cegnev', 160);
$telepules = OthVedelem::szoveg($BE, 'telepules', 120);
$hrsz      = OthVedelem::szoveg($BE, 'hrsz', 60);
$letszam   = OthVedelem::szoveg($BE, 'letszam', 10);
$uzenet    = OthVedelem::szoveg($BE, 'uzenet', (int) $CFG['vedelem']['max_uzenet']);
$hozzajarul = !empty($BE['hozzajarul']);

/* A kapcsolattartó és a vízfogyasztás SZABAD SZÖVEG, ezért hosszkorlátos.
   A vízfogyasztás azért nem szám: a látogató a vízszámláról olvassa le, és az
   hol m³/hó, hol l/nap — egy `number` mező itt csak elutasítaná a helyes
   választ. A méretezést amúgy sem ez dönti el, hanem a mérnöki átnézés. */
$kapcsolattarto = OthVedelem::szoveg($BE, 'kapcsolattarto', 120);
$vizfogyasztas  = OthVedelem::szoveg($BE, 'vizfogyasztas', 60);

/* A HÍRLEVÉL KÜLÖN HOZZÁJÁRULÁS, nem az adatkezelési jelölő része. Az egyik
   az ajánlat elkészítéséhez kell, a másik marketingcélú megkeresés — a kettő
   összevonása a GDPR szerint érvénytelen hozzájárulás. A CRM külön mezőben
   várja, mert a leiratkozást is külön kell tudni kezelni. */
$hirlevel = !empty($BE['hirlevel']);

/* HONNAN ÉRKEZETT — a `kampany.js` tölti ki, rejtett mezőkből. A látogató
   sosem gépeli, tehát bármi jöhet: hosszkorlát és ugyanaz a szövegtisztítás,
   mint minden más mezőn. */
$kampanyTipus = OthVedelem::szoveg($BE, 'kampany_tipus', 120);
$kampanyAzon  = OthVedelem::szoveg($BE, 'kampany_azonosito', 120);
$partnerAzon  = OthVedelem::szoveg($BE, 'partner_azon', 120);

/* Zárt értékkészletű mezők: a kliens bármit küldhet, ezért a listán kívüli
   érték nem „egyéb" lesz, hanem eldobjuk — a levélben csak olyan felirat
   jelenhet meg, amit MI írtunk. */
$LISTAK = [
    'ingatlan' => [
        'csaladi-haz' => 'Családi ház, állandó lakhatás',
        'nyaralo'     => 'Nyaraló, időszakos használat',
        'vallalkozas' => 'Vállalkozás (panzió, étterem, üzem)',
        'intezmeny'   => 'Intézmény (iskola, óvoda, közösségi épület)',
        'kozossegi'   => 'Több ingatlan, közösségi rendszer',
    ],
    'jelenlegi' => [
        'nincs'        => 'Semmi — új építés vagy üres telek',
        'emeszto'      => 'Emésztő (szikkasztó akna)',
        'oldomedence'  => 'Oldómedence, szikkasztás',
        'biologiai'    => 'Biológiai tisztító berendezés',
        'egyeb'        => 'Egyéb vagy nem tudja',
    ],
    'irany' => [
        'nem-tudom' => 'Még nem tudja — javaslatot kér',
        'ab-clear'  => 'A.B.Clear biológiai tisztító',
        'epureco'   => 'EPURECO oldómedence',
        'nagyobb'   => 'Nagyobb vagy közösségi rendszer',
    ],
    'kezdes' => [
        '1-honap'      => 'Egy hónapon belül',
        '3-honap'      => 'Három hónapon belül',
        'fel-ev'       => 'Fél éven belül',
        'tajekozodas'  => 'Még csak tájékozódik',
    ],
    'talajviz' => [
        'nem'        => 'Nem, vagy nem tud róla',
        'igen'       => 'Igen, magas a talajvíz',
        'idoszakos'  => 'Időszakosan, tavasszal megáll a víz',
        'nem-tudom'  => 'Nem tudja',
    ],
    /* A KÖZCSATORNA A LEGFONTOSABB KIZÁRÓ FELTÉTEL. Ahol van kiépített
       közcsatorna, ott jellemzően rá kell kötni, és egyedi berendezés csak
       kivételesen engedélyezhető — a „van, és rá van kötve" válasz tehát nem
       adat, hanem figyelmeztetés az ajánlatot készítőnek. */
    'csatorna' => [
        'nincs'          => 'Nincs az utcában közcsatorna',
        'van-nem-kotott' => 'Van, de nincs rákötve',
        'rakotott'       => 'Van, és rá van kötve',
        'tervezett'      => 'Tervezik, de még nincs kiépítve',
        'nem-tudom'      => 'Nem tudja',
    ],
    'hol_tart' => [
        'valasztas-elott' => 'Még keresi az ingatlant vagy a telket',
        'megvasarolt'     => 'Megvásárolta, még nem építkezik',
        'epul'            => 'Épül vagy felújítás alatt áll',
        'lakott'          => 'Kész, lakott ingatlan',
    ],
    /* A MEGYE IS ZÁRT LISTA, pedig „csak" egy helynév. Az űrlapon legördülő,
       tehát a kliens úgysem gépeli — de a végpont HTTP-n bárkitől fogad
       adatot, és a CRM ebből szűr. Egy elgépelt vagy szándékosan hamis
       megyenév ott csendben rossz csoportba sorolná a megkeresést. */
    'megye' => [
        'Budapest'               => 'Budapest',
        'Bács-Kiskun'            => 'Bács-Kiskun',
        'Baranya'                => 'Baranya',
        'Békés'                  => 'Békés',
        'Borsod-Abaúj-Zemplén'   => 'Borsod-Abaúj-Zemplén',
        'Csongrád-Csanád'        => 'Csongrád-Csanád',
        'Fejér'                  => 'Fejér',
        'Győr-Moson-Sopron'      => 'Győr-Moson-Sopron',
        'Hajdú-Bihar'            => 'Hajdú-Bihar',
        'Heves'                  => 'Heves',
        'Jász-Nagykun-Szolnok'   => 'Jász-Nagykun-Szolnok',
        'Komárom-Esztergom'      => 'Komárom-Esztergom',
        'Nógrád'                 => 'Nógrád',
        'Pest'                   => 'Pest',
        'Somogy'                 => 'Somogy',
        'Szabolcs-Szatmár-Bereg' => 'Szabolcs-Szatmár-Bereg',
        'Tolna'                  => 'Tolna',
        'Vas'                    => 'Vas',
        'Veszprém'               => 'Veszprém',
        'Zala'                   => 'Zala',
        'kulfold'                => 'Külföld',
    ],
];
$valasztott = [];
foreach ($LISTAK as $mezo => $lista) {
    $ertek = OthVedelem::szoveg($BE, $mezo, 40);
    $valasztott[$mezo] = $lista[$ertek] ?? '';
}

/* --- ellenőrzés ---------------------------------------------------------- */
$hibak = [];
if (mb_strlen($nev) < 2)       { $hibak['nev'] = 'Kérjük, adja meg a nevét.'; }
if ($email === '')             { $hibak['email'] = 'Kérjük, adjon meg érvényes e-mail-címet.'; }
if (mb_strlen($telepules) < 2) { $hibak['telepules'] = 'A település nélkül nem tudunk árat mondani.'; }
if (!$hozzajarul)              { $hibak['hozzajarul'] = 'Az adatkezeléshez való hozzájárulás szükséges.'; }

/* --- csatolmányok -------------------------------------------------------- */
$csatolmanyok = OthVedelem::fajlLista($_FILES['fajl'] ?? null, $CFG['csatolmany'], $fajlHiba);
if ($fajlHiba !== '') { $hibak['fajl'] = $fajlHiba; }

if ($hibak) {
    OthVedelem::valasz(422, ['ok' => false, 'uzenet' => 'Néhány mezőt pontosítani kell.', 'mezok' => $hibak]);
}

/* --- értesítés nekünk ---------------------------------------------------- */
$cimSor = 'Ajánlatkérés — ' . $nev . ' (' . $telepules . ')';
$adatok = [
    'Név'                => OthVedelem::html($nev),
    'E-mail'             => '<a href="mailto:' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '" style="color:#2F6F82;">' . htmlspecialchars($email, ENT_QUOTES, 'UTF-8') . '</a>',
    'Telefon'            => $telefon !== '' ? OthVedelem::html($telefon) : '',
    'Cég vagy intézmény' => $cegnev !== '' ? OthVedelem::html($cegnev) : '',
    'Kapcsolattartó'     => $kapcsolattarto !== '' ? OthVedelem::html($kapcsolattarto) : '',
    'Település'          => OthVedelem::html($telepules),
    'Megye'              => OthVedelem::html($valasztott['megye']),
    'Helyrajzi szám'     => $hrsz !== '' ? OthVedelem::html($hrsz) : '',
    'Ingatlan típusa'    => OthVedelem::html($valasztott['ingatlan']),
    'Hány fő használja'  => $letszam !== '' ? OthVedelem::html($letszam) : '',
    'Vízfogyasztás'      => $vizfogyasztas !== '' ? OthVedelem::html($vizfogyasztas) : '',
    'Talajvíz'           => OthVedelem::html($valasztott['talajviz']),
    'Jelenlegi megoldás' => OthVedelem::html($valasztott['jelenlegi']),
    'Közcsatorna'        => OthVedelem::html($valasztott['csatorna']),
    'Hol tart'           => OthVedelem::html($valasztott['hol_tart']),
    'Érdeklődés iránya'  => OthVedelem::html($valasztott['irany']),
    'Tervezett kezdés'   => OthVedelem::html($valasztott['kezdes']),
    'Megjegyzés'         => $uzenet !== '' ? OthVedelem::html($uzenet) : '',
    'Hírlevél'           => $hirlevel ? 'kért' : '',
    /* A KAMPÁNYJELÖLÉS IS BENNE VAN a belső levélben. Nem az értékesítőnek
       szól, hanem annak, aki egy konkrét megkeresésnél utólag kérdezi, honnan
       jött — a CRM-be is megy, de a levél az, ami archívumban marad. */
    'Kampány'            => $kampanyTipus !== '' || $kampanyAzon !== ''
        ? OthVedelem::html(trim($kampanyTipus . ' · ' . $kampanyAzon, ' ·')) : '',
    'Ajánló'             => $partnerAzon !== '' ? OthVedelem::html($partnerAzon) : '',
    'Mellékletek'        => $csatolmanyok
        ? OthVedelem::html(implode(', ', array_column($csatolmanyok, 'nev'))) : '',
];

$html = OthLevel::html(
    $CFG['webhely'],
    'Ajánlatkérés a weboldalról',
    $cimSor,
    'Az alábbi ajánlatkérés érkezett. A válasz gomb közvetlenül a kérőnek megy.',
    $adatok,
    ['felirat' => 'Ajánlat írása', 'url' => 'mailto:' . $email],
    'Beérkezett: ' . date('Y. m. d. H:i') . ' · IP: ' . htmlspecialchars((string) ($_SERVER['REMOTE_ADDR'] ?? '—'), ENT_QUOTES, 'UTF-8')
);
$szoveg = OthLevel::szoveg($CFG['webhely'], $cimSor,
    'Az alábbi ajánlatkérés érkezett a weboldalról.', $adatok,
    'Beérkezett: ' . date('Y. m. d. H:i'));

$cimzett = $CFG['cimzettek']['ajanlat'] ?? $CFG['cimzettek']['kapcsolat'];
oth_kuld($CFG, $cimzett, '[Weboldal] ' . $cimSor, $szoveg, $html, $csatolmanyok, $email, $nev,
         oth_masolat($CFG));

/* --- visszaigazolás a látogatónak ---------------------------------------- */

/* A VISSZAIGAZOLÁS A TELJES BEKÜLDÉST MUTATJA, nem három kiragadott mezőt. Két
   okból: a látogató ebből látja, MIT ÉRTETTÜNK MEG — egy elgépelt létszám vagy
   rossz település itt derül ki, nem az ajánlat megérkezésekor —, és mert ez az
   ő példánya arról, amit elküldött.

   KÉT MEZŐ VISZONT NEM MEGY VISSZA. A „Kampány" és az „Ajánló" belső adat: a
   `kampany.js` írta rejtett mezőből, a látogató nem gépelte és nem is látta.
   Visszatükrözni egyrészt értelmetlen, másrészt kellemetlen — szembesítené
   vele, hogy tudjuk, melyik hirdetésről jött. A CRM-be és a nekünk szóló
   levélbe természetesen bekerül.

   A `Mellékletek` sor is kimarad: a saját fájljait csatolva kapja vissza,
   felsorolni fölösleges. */
$vadatok = array_diff_key($adatok, array_flip(['Kampány', 'Ajánló', 'Mellékletek']));

if (!empty($CFG['visszaigazolas'])) {
    $vhtml = OthLevel::html(
        $CFG['webhely'],
        'Visszaigazolás',
        'Megkaptuk az ajánlatkérését',
        "Köszönjük. Az adatokat átnézzük, és két munkanapon belül küldjük a tételes ajánlatot.\n"
        . 'Ha valami hiányzik a méretezéshez, előbb rákérdezünk. Sürgős esetben: ' . $CFG['webhely']['tel'] . '.',
        $vadatok,
        ['felirat' => 'Vissza a weboldalra', 'url' => $CFG['webhely']['url']],
        'Erre a levélre nem szükséges válaszolnia — csak visszaigazolás.'
    );
    $vszoveg = OthLevel::szoveg($CFG['webhely'], 'Megkaptuk az ajánlatkérését',
        'Az adatokat átnézzük, és két munkanapon belül küldjük a tételes ajánlatot.',
        ['Település' => OthVedelem::html($telepules)]);

    /* MELLÉKLETEK A LÁTOGATÓNAK — sorrendben, mert a keret véges.
       ------------------------------------------------------------------
       1. A JOGI DOKUMENTUMOK ELÖL. Csatolva, nem hivatkozva: a weboldal
          szövege változhat, a levél nem. Ha valaki évekkel később vitatja,
          mit fogadott el, ez mutatja meg, mi állt ott a beküldés
          pillanatában.
       2. A SAJÁT FELTÖLTÉSEI hátul. Neki amúgy is megvannak — ez
          kényelem, nem bizonyíték —, ezért ez esik ki előbb, ha nem fér
          bele. Három 10 MB-os helyszínrajzzal a levelet a fogadó
          kiszolgálók visszautasítanák, és akkor VISSZAIGAZOLÁS SEM menne
          ki. Csonka levél jobb, mint elutasított. */
    $vcsatolmanyok = oth_csatolmany_keret(array_merge(
        oth_dokumentumok([
            'okotechhome-adatkezelesi-tajekoztato.pdf',
            'okotechhome-aszf.pdf',
            'okotechhome-termekismerteto.pdf',   // ha egyszer bekerül, magától megy
        ]),
        $csatolmanyok,
    ));

    /* A visszaigazolás elmaradása NEM hiba a látogató szempontjából: az
       ajánlatkérés már megérkezett hozzánk. */
    try {
        oth_kuld($CFG, [$email], 'Megkaptuk az ajánlatkérését — ' . $CFG['webhely']['nev'],
                 $vszoveg, $vhtml, $vcsatolmanyok);
    } catch (Throwable $e) {
        error_log('OTH: az ajánlatkérés visszaigazolása nem ment ki: ' . $e->getMessage());
    }
}

/* --- átadás a CRM-nek (a levelek UTÁN) ----------------------------------- */
OthCrm::kuld($CFG, 'ajanlat', OthCrm::csomag(
    OthVedelem::szoveg($BE, 'ugy_azonosito', 40) ?: null,
    'ajanlat-' . date('YmdHis') . '-' . substr(sha1($email), 0, 8),
    ['nev' => $nev, 'email' => $email, 'telefon' => $telefon, 'cegnev' => $cegnev],
    [
        'targy'    => 'Ajánlatkérés a weboldalról',
        'uzenet'   => $uzenet,
        'url'      => $CFG['webhely']['url'] ?? null,
        /*
         * A KULCSOK A CRM MEZŐNEVEI, nem a kérdések szövege — ebben az egy
         * csatornában. A `web_bekuldes` tábla `valaszok` JSON-ját a fogadó
         * oldal bontja szét az `ajanlatkeres` és az `ugyfelek` táblába, és
         * ehhez gépi néven kell hivatkoznia rájuk. Egy átfogalmazott kérdés
         * így nem töri el a szétbontást.
         *
         * A LÁTHATÓ FELIRAT ETTŐL FÜGGETLEN: a belső levél `$adatok` tömbje
         * viszi a magyar címkéket, és az változhat szabadon.
         */
        'valaszok' => array_filter([
            'letesitmeny_tipusa'  => $valasztott['ingatlan'],
            /* A `letesitmeny_egyeb` ÉS a `megjegyzes` UGYANAZT AZ ÉRTÉKET kapja,
               és ez szándékos. A CRM mezőlistája mindkettőt „szabad szavas
               megjegyzés"-ként írja le, a régi rendszerben viszont két külön
               beviteli mező volt. Itt egy van — a lap alján a „Megjegyzés" —,
               és nem találunk ki mesterséges különbséget oda, ahol a látogató
               egy dobozba írt. A szétbontó így mindkét néven megtalálja.
               A `web_bekuldes.uzenet` oszlopban is ott van, harmadszor. */
            'letesitmeny_egyeb'   => $uzenet,
            'megjegyzes'          => $uzenet,
            'szemelyek_szama'     => $letszam,
            'vizfogyasztas'       => $vizfogyasztas,
            'talajviz'            => $valasztott['talajviz'],
            'telepites_helyszine' => $telepules,
            'megye'               => $valasztott['megye'],
            'varos'               => $telepules,
            'helyrajzi_szam'      => $hrsz,
            'kapcsolattarto'      => $kapcsolattarto,
            'szennyvizkezeles'    => $valasztott['jelenlegi'],
            'csatorna_lehetoseg'  => $valasztott['csatorna'],
            'hol_tart_a_lakas'    => $valasztott['hol_tart'],
            'erdeklodes_iranya'   => $valasztott['irany'],
            'tervezett_kezdes'    => $valasztott['kezdes'],
            /* A `hirlevel` és az `adatkezeles` SOSEM eshet ki az `array_filter`
               rostáján, mert a „nem" éppolyan érdemi válasz, mint az „igen" —
               ezért sztring, nem logikai érték. Az `adatkezeles` a
               `gdpr_hozzajarulas` oszlopban is ott van; itt azért ismételjük,
               hogy a szétbontó egyetlen JSON-ból dolgozhasson. */
            'hirlevel'            => $hirlevel ? 'igen' : 'nem',
            'adatkezeles'         => $hozzajarul ? 'igen' : 'nem',
            'partner_azon'        => $partnerAzon,
            'kampany_tipus'       => $kampanyTipus,
            'kampany_azonosito'   => $kampanyAzon,
        ]),
    ],
    $hozzajarul,
));

OthVedelem::valasz(200, [
    'ok' => true,
    'uzenet' => 'Köszönjük, megkaptuk az ajánlatkérését. Két munkanapon belül küldjük a tételes ajánlatot.',
]);
