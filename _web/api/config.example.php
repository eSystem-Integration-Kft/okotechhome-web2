<?php
/**
 * config.example.php — MINTA. Másolat készítendő `config.php` néven.
 * ---------------------------------------------------------------------------
 * A `config.php` a .gitignore-ban van: valódi jelszó SOHA nem kerülhet a repóba.
 *
 * Telepítés a szerveren:
 *     cp config.example.php config.php
 *     # majd a config.php-ba beírni a valódi értékeket
 *     chmod 600 config.php
 *
 * Ha a tárhely enged környezeti változót (pl. .htaccess SetEnv, panel), az
 * ERŐSEBB megoldás: akkor a config.php értékei üresen hagyhatók, mert az
 * alábbi `env()` hívások elsőbbséget adnak a környezeti változónak.
 */

declare(strict_types=1);

/** Környezeti változó, ha van; különben a megadott alapérték. */
function oth_env(string $key, string $fallback = ''): string
{
    $v = getenv($key);
    return ($v === false || $v === '') ? $fallback : $v;
}

/**
 * Titok beolvasása FÁJLBÓL — hogy a kulcsot ne kelljen a config.php-ba írni.
 *
 * Sorrend: az első LÉTEZŐ és nem üres fájl nyer, utána a környezeti változó,
 * végül a megadott alapérték. A fájl tartalmát trimeljük, tehát a szerkesztő
 * által odabiggyesztett sorvég nem rontja el a kulcsot.
 *
 * HOVA TEDD A FÁJLT. Elsődlegesen a webgyökér FÖLÉ (`oth-titkok/`): ami nincs
 * a dokumentumgyökérben, azt a webszerver ki sem tudja szolgálni, tehát nem
 * kell védeni. A második hely az `api/` könyvtár — ez kényelmesebb, de csak
 * azért biztonságos, mert az api/.htaccess tiltja a .txt fájlok letöltését.
 * Ha a tárhelyed nem olvassa a .htaccess-t (nginx), CSAK az első helyet hasznld.
 *
 * Jogosultság: chmod 600, a tulajdonos a webszerver felhasználója.
 */
function oth_titok(array $utvonalak, string $envKulcs = '', string $fallback = ''): string
{
    $probalt = [];
    $olvas = static function (string $u) {
        if (is_file($u) && is_readable($u)) {
            $t = trim((string) @file_get_contents($u));
            if ($t !== '') {
                return $t;
            }
        }
        return null;
    };

    foreach ($utvonalak as $u) {
        $probalt[] = $u;
        if (($t = $olvas($u)) !== null) {
            return $t;
        }
    }

    /* FELFELÉ IS KERESÜNK. Az `oth-titkok/` a tárhely gyökerében áll, a
       webgyökér viszont tárhelyenként más mélységben: a `tst.okoth.hu/api/`
       két szintre van tőle, a `public_html/tst/api/` háromra. Fix `../../`
       csak az egyik elrendezésben talál, ezért korlátozott (5 szint) sétával
       keressük ugyanazt a fájlnevet minden fölöttes szint `oth-titkok/`
       könyvtárában. */
    $nev = basename((string) ($utvonalak[0] ?? ''));
    if ($nev !== '') {
        $dir = __DIR__;
        for ($i = 0; $i < 5; $i++) {
            $szulo = dirname($dir);
            if ($szulo === $dir) {
                break;
            }
            $dir = $szulo;
            $u = $dir . '/oth-titkok/' . $nev;
            $probalt[] = $u;
            if (($t = $olvas($u)) !== null) {
                return $t;
            }
        }
    }

    $ertek = $envKulcs !== '' ? oth_env($envKulcs, $fallback) : $fallback;

    /* Ha a helyőrzővel térünk vissza, a naplóba beírjuk, HOL kerestük — enélkül
       a hiba néma, és a keresés órákat visz el. A titok ÉRTÉKE sosem kerül a
       naplóba, csak útvonalak. Az `open_basedir` külön szerepel: megosztott
       tárhelyen ez a leggyakoribb ok, amiért a webgyökér FÖLÖTTI fájl nem
       olvasható — ilyenkor a titkot az `api/` könyvtárba kell tenni (a
       .htaccess védi), vagy környezeti változóból átadni. */
    if ($ertek === $fallback && $nev !== '') {
        $ob = ini_get('open_basedir');
        error_log('OTH titok: "' . $nev . '" egyik helyen sem olvasható. Keresve: '
                . implode(' | ', $probalt)
                . ($ob ? ' — FIGYELEM, open_basedir aktív: ' . $ob : ''));
    }
    return $ertek;
}

return [
    /* --- SMTP ------------------------------------------------------------ */
    'smtp' => [
        'host'   => oth_env('OTH_SMTP_HOST', 'mail.example.hu'),
        'port'   => (int) oth_env('OTH_SMTP_PORT', '465'),
        // 'ssl' = implicit TLS (465), 'tls' = STARTTLS (587)
        'secure' => oth_env('OTH_SMTP_SECURE', 'ssl'),
        'user'   => oth_env('OTH_SMTP_USER', 'nev@example.hu'),
        'pass'   => oth_env('OTH_SMTP_PASS', 'IDE_JON_A_JELSZO'),
        'timeout' => 20,
    ],


    /* --- AI-elemzés (11. szekció ajánlat-összehasonlító) ------------------ */
    // Az API-kulcs SOHA nem kerül a böngészőbe: az api/ajanlat-elemzes.php a
    // proxy, a kliens csak azt a végpontot látja.
    'ai' => [
        // A kulcs FÁJLBÓL is jöhet, hogy ne kelljen ebbe az állományba írni —
        // így a config.php szerkesztés nélkül másolható, és a kulcs cseréjéhez
        // elég egy szövegfájlt felülírni. A sorrend: fájl → környezeti változó →
        // az itteni alapérték.
        'kulcs'   => oth_titok([
            // Ugyanaz a három mélység, mint a CRM-titkoknál: a webgyökér nem
            // mindenhol ül ugyanolyan mélyen. (Az `oth_titok()` ezen felül
            // felfelé is keres, ez a lista csak a gyors, egyértelmű eset.)
            __DIR__ . '/../../../oth-titkok/ai-kulcs.txt',
            __DIR__ . '/../../oth-titkok/ai-kulcs.txt',
            __DIR__ . '/../oth-titkok/ai-kulcs.txt',
            __DIR__ . '/ai-kulcs.txt',                    // az api/ könyvtárban — az api/.htaccess védi
        ], 'OTH_AI_KULCS', 'IDE_JON_AZ_API_KULCS'),
        // A modellazonosítót az Anthropic konzol modell-listája adja. Dokumentum-
        // kiolvasáshoz a pontosság a fontos: egy félreolvasott ár többe kerül,
        // mint amit egy kisebb modellel megspórol. Ha mégis vált, ugyanazokkal a
        // fájlokkal vesse össze — ha a „nincs adat” cellák száma nő, a modell
        // kevesebbet TALÁL MEG, nem az ajánlatból hiányzik.
        // Elgépelt modellnév esetén a hiba a api/hiba.log-ban nevesítve jelenik meg.
        'modell'  => oth_env('OTH_AI_MODELL', 'claude-sonnet-5'),
        'timeout' => 120,
        // WEBHELYSZINTŰ napi keretek — nem IP-nkénti: az IP-korlátot
        // proxylistával meg lehet kerülni, ezt nem. Betelte után a kalauz és a
        // kitöltéssegéd udvariasan elköszön, a konzultációkérés AI-összefoglaló
        // nélkül is kimegy. 0 = nincs keret.
        'napi_keret'         => 400,  // kalauz + kitöltéssegéd + beküldési brief
        'napi_keret_elemzes' => 60,   // ajánlat-elemzés (a legdrágább hívás)
    ],

    /* --- Feladó és címzettek --------------------------------------------- */
    // A feladónak a saját domainen kell lennie, különben az SPF/DKIM elbukik,
    // és a levél spambe kerül. A látogató címe a Reply-To fejlécbe megy.
    'from'      => ['cim' => 'nev@example.hu', 'nev' => 'ÖkoTech Home — weboldal'],
    'cimzettek' => [
        'kapcsolat'       => ['kapcsolat@example.hu'],
        'konzultacio'     => ['kapcsolat@example.hu'],
        'dontestamogato'  => ['kapcsolat@example.hu'],
        'ajanlat-atnezes' => ['kapcsolat@example.hu'],
        // A szippantási díjkalkulátor adatbeküldései. Kihagyva a 'kapcsolat'
        // postafiókba mennek — a végpontnak van tartaléka, tehát a beküldés
        // akkor sem vész el, ha ez a sor lemarad.
        'szippantasi-dij' => ['kapcsolat@example.hu'],
    ],

    /* --- Visszaigazolás a látogatónak ------------------------------------ */
    'visszaigazolas' => true,

    /* --- Védelem ---------------------------------------------------------- */
    /*
    | DealKeeper CRM — a kitöltések átadása.
    |
    | MINDEN kitöltés átmegy, akkor is, ha nincs e-mail-cím: a névtelen
    | modul-kitöltésekből a CRM-ben nem lesz érdeklődő, de rögzülnek
    | ügyrekordként — megmutatják, hányan tájékozódnak és mire keresnek
    | választ, és ha a látogató később nevet is ad, az ügyazonosító
    | visszamenőleg összekapcsolja a két beküldést.
    |
    | A küldés SOSEM akadályozza meg a levelet: rövid időkorláttal fut, és
    | hiba esetén csak a naplóba ír.
    */
    'crm' => [
        'engedelyezve' => (bool) oth_env('OTH_CRM_BE', false),

        // A beérkező kapu alapcíme — a forrás azonosítója a végére kerül.
        'url' => oth_env('OTH_CRM_URL', 'https://dealkeeper.hu/api/v1/beerkezo'),

        /*
        | CSATORNA → CRM-FORRÁS + TITOK.
        |
        | A bal oldali kulcs a MI belső nevünk, ezt hívja a kód. A `forras` az,
        | amit a CRM-ben a forrás felvételekor kapott — a CRM-ben UTÓLAG NEM
        | ÁTNEVEZHETŐ (egy átnevezés csendben elnémítaná a weboldalt), tehát
        | adottság, amihez itt igazodunk. Ha a CRM-ben más néven vetted fel,
        | CSAK EZT A SORT írd át; a végpontokhoz nem kell hozzányúlni.
        |
        | FORRÁSONKÉNT KÜLÖN TITOK. Egy közös titokkal egyetlen kiszivárgás
        | mind a négy csatornát megnyitná; külön titokkal a sérült forrás
        | önmagában visszavonható.
        |
        | A TITOK NE ITT ÁLLJON, hanem külön fájlban, a webgyökér FÖLÖTT.
        | Egy fájl = EGY titok, semmi más: az `oth_titok()` a fájl teljes
        | tartalmát olvassa be, tehát egy odabiggyesztett második sor mindkét
        | kulcsot használhatatlanná teszi.
        */
        'csatornak' => [
            'kapcsolat' => [
                'forras' => oth_env('OTH_CRM_FORRAS_KAPCSOLAT', 'okotechhome-kapcsolat'),
                'titok'  => oth_titok([
                /*
                 * TÖBB ÚTVONAL, MERT A WEBGYÖKÉR HELYE HÁZANKÉNT MÁS.
                 *
                 * Az `oth_titok()` az ELSŐ létező és nem üres fájlt veszi. A
                 * tárhelyek egy része `<domain>/`, más része
                 * `<domain>/public_html/` alá teszi a dokumentumgyökeret — és
                 * FTP-kliensből nézve nem derül ki, melyik. Ha csak egy
                 * útvonalat próbálnánk, egy szintnyi eltérés némán elnyelné a
                 * titkot: a küldő üresnek látja, csendben visszatér, és a
                 * kitöltés nyomtalanul elvész.
                 *
                 * A könyvtárban lévő `.htaccess` gondoskodik arról, hogy ha
                 * mégis webgyökérbe kerülne, ne legyen letölthető.
                 */
                    __DIR__ . '/../../../oth-titkok/crm-kapcsolat.txt',
                    __DIR__ . '/../../oth-titkok/crm-kapcsolat.txt',
                    __DIR__ . '/../oth-titkok/crm-kapcsolat.txt',
                    __DIR__ . '/crm-kapcsolat.txt',
                ], 'OTH_CRM_TITOK_KAPCSOLAT'),
            ],
            'arsav' => [
                'forras' => oth_env('OTH_CRM_FORRAS_ARSAV', 'okotechhome-arsav'),
                'titok'  => oth_titok([
                    __DIR__ . '/../../../oth-titkok/crm-arsav.txt',
                    __DIR__ . '/../../oth-titkok/crm-arsav.txt',
                    __DIR__ . '/../oth-titkok/crm-arsav.txt',
                    __DIR__ . '/crm-arsav.txt',
                ], 'OTH_CRM_TITOK_ARSAV'),
            ],
            /* Megoldás-ajánló — a MÁSIK főoldali modul, szintén névtelen.
               Nem az ársávbecslő testvércsatornája véletlenül: külön mérve
               látszik, hogy aki MINDKETTŐT kitöltötte, messzebb jár. */
            'ajanlo' => [
                'forras' => oth_env('OTH_CRM_FORRAS_AJANLO', 'okotechhome-ajanlo'),
                'titok'  => oth_titok([
                    __DIR__ . '/../../../oth-titkok/crm-megoldasajanlo.txt',
                    __DIR__ . '/../../../oth-titkok/crm-ajanlo.txt',
                    __DIR__ . '/../../oth-titkok/crm-megoldasajanlo.txt',
                    __DIR__ . '/../../oth-titkok/crm-ajanlo.txt',
                    __DIR__ . '/../oth-titkok/crm-megoldasajanlo.txt',
                    __DIR__ . '/../oth-titkok/crm-ajanlo.txt',
                    __DIR__ . '/crm-megoldasajanlo.txt',
                    __DIR__ . '/crm-ajanlo.txt',
                ], 'OTH_CRM_TITOK_AJANLO'),
            ],

            'osszehasonlito' => [
                'forras' => oth_env('OTH_CRM_FORRAS_OSSZEHASONLITO', 'okotechhome-osszehasonlito'),
                'titok'  => oth_titok([
                    __DIR__ . '/../../../oth-titkok/crm-osszehasonlito.txt',
                    __DIR__ . '/../../oth-titkok/crm-osszehasonlito.txt',
                    __DIR__ . '/../oth-titkok/crm-osszehasonlito.txt',
                    __DIR__ . '/crm-osszehasonlito.txt',
                ], 'OTH_CRM_TITOK_OSSZEHASONLITO'),
            ],
            'konzultacio' => [
                'forras' => oth_env('OTH_CRM_FORRAS_KONZULTACIO', 'okotechhome-konzultacio'),
                'titok'  => oth_titok([
                    __DIR__ . '/../../../oth-titkok/crm-konzultacio.txt',
                    __DIR__ . '/../../oth-titkok/crm-konzultacio.txt',
                    __DIR__ . '/../oth-titkok/crm-konzultacio.txt',
                    __DIR__ . '/crm-konzultacio.txt',
                ], 'OTH_CRM_TITOK_KONZULTACIO'),
            ],
        ],
    ],

    'vedelem' => [
        // Ugyanarról az IP-ről hány beküldés engedett az ablakon belül.
        'limit'        => 5,
        'ablak_perc'   => 60,
        // Ennél gyorsabb kitöltés robotra utal (másodperc).
        'min_kitoltes' => 3,
        'max_uzenet'   => 5000,
        // Csak ezekről az origin-ekről fogadunk beküldést (CSRF-védelem).
        'origin'       => ['https://okoth.hu', 'https://tst.okoth.hu'],
    ],

    /* --- Csatolmányok (ajánlat-átnézés) ----------------------------------- */
    'csatolmany' => [
        'max_meret'  => 10 * 1024 * 1024,
        'max_darab'  => 3,
        // A régi, bináris .doc és .xls kimarad — nem olvasható ki megbízhatóan.
        'kiterjesztes' => ['pdf', 'docx', 'xlsx', 'png', 'jpg', 'jpeg'],
        'mime' => [
            'application/pdf',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'image/png',
            'image/jpeg',
        ],
    ],

    /* --- Mentett eredmények (ÜGYTÁR) --------------------------------------
       A főoldali AI-modulok KÖZÖS tárolója. A látogató a 6. szekcióban kap egy
       `MA-XXXX-XXXX` azonosítót; a 8. szekció ugyanezt az ügyet egészíti ki,
       nem újat nyit. A `/eredmeny?id=…` lap mindkét modul kimenetét mutatja.

       A rekordban NINCS személyes adat: csak a modulok kérdéseire adott
       válaszok és a belőlük számított kimenet. Nevet, e-mail-címet, IP-t nem
       tárolunk mellé. (A 8. szekció e-mailes összefoglalója külön végponton
       megy, és a cím nem kerül az ügyrekordba.)

       ⚠️ A `megorzes_nap` értékének EGYEZNIE KELL az adatkezelési
       tájékoztatóban közölt megőrzési idővel. Ha itt átírod, ott is át kell.
       `engedelyezve => false` esetén a modulok nem hívnak szervert: az eredményt
       a látogató szövegfájlként töltheti le, és ezt a felület ki is mondja. */
    'eredmeny' => [
        'engedelyezve' => true,
        'megorzes_nap' => 180,
    ],

    /* --- Megjelenés a levélben -------------------------------------------- */
    'webhely' => [
        'nev'   => 'ÖkoTech Home',
        'url'   => 'https://okoth.hu',
        'logo'  => 'https://okoth.hu/assets/img/logo-email.png',
        'cim'   => '2509 Esztergom, Strázsa u. 12.',
        'tel'   => '+36 33 200 211',
        'email' => 'kapcsolat@okotechhome.hu',
    ],
];
