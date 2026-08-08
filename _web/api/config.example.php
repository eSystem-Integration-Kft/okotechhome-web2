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
    foreach ($utvonalak as $u) {
        if (is_file($u) && is_readable($u)) {
            $t = trim((string) @file_get_contents($u));
            if ($t !== '') {
                return $t;
            }
        }
    }
    return $envKulcs !== '' ? oth_env($envKulcs, $fallback) : $fallback;
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
            __DIR__ . '/../../oth-titkok/ai-kulcs.txt',   // a webgyökér FÖLÖTT — ez az ajánlott
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
    ],

    /* --- Feladó és címzettek --------------------------------------------- */
    // A feladónak a saját domainen kell lennie, különben az SPF/DKIM elbukik,
    // és a levél spambe kerül. A látogató címe a Reply-To fejlécbe megy.
    'from'      => ['cim' => 'nev@example.hu', 'nev' => 'ÖkoTech Home — weboldal'],
    'cimzettek' => [
        'kapcsolat'       => ['kapcsolat@example.hu'],
        'dontestamogato'  => ['kapcsolat@example.hu'],
        'ajanlat-atnezes' => ['kapcsolat@example.hu'],
    ],

    /* --- Visszaigazolás a látogatónak ------------------------------------ */
    'visszaigazolas' => true,

    /* --- Védelem ---------------------------------------------------------- */
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
