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
        'kiterjesztes' => ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png'],
        'mime' => [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'image/png',
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
