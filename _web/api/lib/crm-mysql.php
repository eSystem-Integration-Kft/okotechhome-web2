<?php
/**
 * crm-mysql.php — a kitöltések átadása KÖZVETLENÜL egy CRM MySQL-táblájába.
 * ---------------------------------------------------------------------------
 * UGYANAZT A BORÍTÉKOT KAPJA, mint a HTTP-kapu. A végpontok az `OthCrm::kuld()`-ot
 * hívják, az pedig a beállítás szerint dönti el, melyik úton megy az adat — a
 * hat hívási helyhez ezért nem kell hozzányúlni.
 *
 * MIKOR JOBB EZ, MINT A HTTP-KAPU. Ha a CRM UGYANAZON A KISZOLGÁLÓN fut, mint a
 * weboldal: nincs hálózat, nincs aláírás-egyeztetés, nincs időkorlát-kockázat, és
 * a beküldés tranzakcióban ér földet.
 *
 * MIKOR ROSSZABB. Ha a CRM MÁSIK gépen van. Egy nyílt interneten átmenő MySQL
 * kapcsolat gyengébb, mint egy aláírt HTTPS-kérés: a jelszó hosszú életű, a port
 * támadható, és TLS nélkül a teljes forgalom olvasható. Távoli CRM-nél MARADJON
 * A HTTP-KAPU — ez a fájl a localhost esetére való.
 *
 * A HIBA SOHA NEM AKADÁLYOZHATJA MEG A LEVELET. Ugyanaz a szabály, mint a
 * HTTP-kapunál: rövid időkorlát, a hiba a naplóba megy, a látogató beküldése
 * ettől függetlenül sikeres — a levél már elment.
 */
declare(strict_types=1);

final class OthCrmMysql
{
    /** A látogató nem várhat az adatbázisra. */
    private const KAPCSOLAT_TIMEOUT = 3;

    /** @var PDO|null Kérésenként egy kapcsolat; a végpont amúgy is egyszer ír. */
    private static $pdo = null;

    /** Az utolsó írás jellege — az átadási napló ezt jegyzi föl. */
    public static $utolsoMuvelet = '';

    /**
     * Egy beküldés eltárolása.
     *
     * @param  array  $csat  a csatorna beállítása (`forras` kell belőle)
     * @param  array  $adat  az `OthCrm::csomag()` kimenete
     *
     * @return bool sikerült-e — a VÉGPONTOK NE ÁGAZZANAK EL rajta.
     */
    public static function ir(array $CFG, string $csatorna, array $csat, array $adat): bool
    {
        $beall = $CFG['crm']['mysql'] ?? [];

        if (empty($beall['adatbazis']) || empty($beall['felhasznalo'])) {
            error_log('OTH CRM/MySQL: hiányos beállítás (adatbazis vagy felhasznalo).');

            return false;
        }

        try {
            $pdo = self::kapcsolat($beall);

            $kapcs = $adat['kapcsolat'] ?? [];
            $megk  = $adat['megkereses'] ?? [];

            /*
             * A `valaszok` JSON-ként megy be, nem oszlopokra bontva. A kulcsai az
             * űrlap KÉRDÉSEIT idézik, nem gépi azonosítók — egy átfogalmazott
             * kérdés így nem igényel adatbázis-migrációt.
             */
            $valaszok = $megk['valaszok'] ?? null;
            $valaszokJson = ($valaszok === null || $valaszok === [])
                ? null
                : json_encode($valaszok, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);

            $tabla = self::tablanev($beall['tabla'] ?? 'web_bekuldes');

            $mezok = [
                'csatorna'          => $csatorna,
                'forras'            => (string) ($csat['forras'] ?? $csatorna),
                'ugy_azonosito'     => self::ures($adat['ugy_azonosito'] ?? null),
                'nev'               => self::ures($kapcs['nev'] ?? null),
                'email'             => self::ures($kapcs['email'] ?? null),
                'telefon'           => self::ures($kapcs['telefon'] ?? null),
                'ceg'               => self::ures($kapcs['ceg'] ?? null),
                'targy'             => self::ures($megk['targy'] ?? null),
                'uzenet'            => self::ures($megk['uzenet'] ?? null),
                'url'               => self::ures($megk['url'] ?? null),
                'valaszok'          => $valaszokJson,
                'gdpr_hozzajarulas' => !empty($adat['gdpr']['hozzajarulas']) ? 1 : 0,
            ];
            $kulsoAzon = (string) ($adat['external_id'] ?? '');

            /*
             * BESZÚRÁS, ÉS CSAK ÜTKÖZÉSKOR FRISSÍTÉS — nem `ON DUPLICATE KEY UPDATE`.
             *
             * Az ODKU kényelmesebb volna, de a MySQL a `VALUES(oszlop)`
             * kiolvasásához SELECT-jogot kér az ÖSSZES érintett oszlopra. A
             * weboldal felhasználója így ki tudná listázni a korábbi
             * megkeresések nevét és e-mail-címét — pontosan azt, amitől a szűk
             * jogosultság védeni hivatott. (A MySQL 8.0.20 sorálias alakja sem
             * segít: próbán ugyanígy 1143-mal elszállt.)
             *
             * Így viszont a webes felhasználónak elég:
             *     INSERT, UPDATE(oszlopok), SELECT(external_id)
             * — egyetlen oszlopot lát, és az is álnév.
             */
            try {
                $nevek = implode(', ', array_keys($mezok));
                $helyek = implode(', ', array_fill(0, count($mezok), '?'));
                $st = $pdo->prepare("INSERT INTO {$tabla} (external_id, {$nevek}) VALUES (?, {$helyek})");
                $st->execute(array_merge([$kulsoAzon], array_values($mezok)));

                self::$utolsoMuvelet = 'beszúrva';
            } catch (PDOException $e) {
                /* 1062 = egyedi kulcs ütközése: ez ISMÉTELT kézbesítés, nem hiba.
                   A két névtelen modul azonosítója szándékosan állandó, mert a
                   látogató újrafuttathatja őket — olyankor a legutolsó beküldés
                   az érvényes. Minden más hibát továbbdobunk. */
                if (($e->errorInfo[1] ?? 0) !== 1062) {
                    throw $e;
                }

                $ertekadas = implode(' = ?, ', array_keys($mezok)) . ' = ?';
                $st = $pdo->prepare("UPDATE {$tabla} SET {$ertekadas} WHERE external_id = ?");
                $st->execute(array_merge(array_values($mezok), [$kulsoAzon]));

                self::$utolsoMuvelet = 'frissítve';
            }

            return true;
        } catch (Throwable $e) {
            /*
             * A KIVÉTEL SZÖVEGE MEHET A NAPLÓBA, A BEKÜLDÉS TARTALMA NEM.
             * Egy PDO-hiba üzenete tartalmazhatja a paramétereket — köztük a
             * látogató nevét és e-mail-címét —, ezért csak a típust és a
             * csatornát írjuk ki, a teljes üzenetet nem.
             */
            error_log('OTH CRM/MySQL: ' . $csatorna . ' → ' . get_class($e)
                    . ' (' . self::rovidHiba($e) . ')');

            return false;
        }
    }

    /** Kapcsolat rövid időkorláttal, kivételekkel, natív prepared statementtel. */
    private static function kapcsolat(array $beall): PDO
    {
        if (self::$pdo instanceof PDO) {
            return self::$pdo;
        }

        /*
         * `ATTR_EMULATE_PREPARES = false`: valódi, szerveroldali előkészített
         * utasítás. Emulációval a PDO maga fűzi össze a lekérdezést — az
         * idézőjelezés helyes, de a JSON és a többbájtos karakterek kezelése
         * kiszámíthatatlanabb, és a típusok elvesznek.
         *
         * PERZISZTENS KAPCSOLAT NINCS. Megosztott tárhelyen a `PDO::ATTR_PERSISTENT`
         * elfogyasztja a kapcsolatkeretet, és a hiba akkor jelentkezik, amikor a
         * legrosszabb: forgalmi csúcsban.
         */
        self::$pdo = new PDO(
            self::dsn($beall),
            (string) $beall['felhasznalo'],
            (string) ($beall['jelszo'] ?? ''),
            self::pdoBeallitasok($beall),
        );

        return self::$pdo;
    }

    /**
     * A DSN MEZŐKBŐL épül, nem kész sztringből. Egy elgépelt DSN néma
     * kapcsolódási hibát ad; a külön mezők viszont egyesével ellenőrizhetők, és
     * a beállítást nem kell a PDO szintaxisának ismeretével írni.
     *
     * SOCKET VAGY HOSZT. Ha a CRM ugyanazon a gépen fut, a UNIX socket a
     * gyorsabb és a biztonságosabb: a forgalom el sem hagyja a gépet, tehát
     * tűzfalon nem kell portot nyitni. IP-címnél a port is kell — és onnantól
     * TLS nélkül a teljes forgalom, a jelszóval együtt, olvasható a hálózaton.
     */
    private static function dsn(array $b): string
    {
        /* A DSN nem előkészíthető utasítás: az adatbázisnevet itt szűrjük. */
        $db = preg_replace('/[^A-Za-z0-9_$-]/', '', (string) $b['adatbazis']);

        if (!empty($b['socket'])) {
            return 'mysql:unix_socket=' . $b['socket'] . ';dbname=' . $db . ';charset=utf8mb4';
        }

        return 'mysql:host=' . (string) ($b['hoszt'] ?? 'localhost')
             . ';port=' . (int) ($b['port'] ?? 3306)
             . ';dbname=' . $db . ';charset=utf8mb4';
    }

    /**
     * TLS CSAK TÁVOLI KAPCSOLATNÁL kell, de ott NEM ELHAGYHATÓ. A MySQL a
     * jelszót a kézfogás során küldi; titkosítatlan vonalon ez a jelszó és
     * minden beküldött személyes adat olvasható bárkinek, aki a forgalmat
     * látja. Ha távoli hoszt van megadva TLS nélkül, azt a naplóba írjuk —
     * jobb egy hangos figyelmeztetés, mint egy csendes szivárgás.
     */
    private static function pdoBeallitasok(array $b): array
    {
        $ki = [
            PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES   => false,
            PDO::ATTR_TIMEOUT            => self::KAPCSOLAT_TIMEOUT,
        ];

        $tavoli = empty($b['socket'])
            && !in_array((string) ($b['hoszt'] ?? 'localhost'), ['localhost', '127.0.0.1', '::1'], true);

        if (!empty($b['tls_ca'])) {
            $ki[PDO::MYSQL_ATTR_SSL_CA] = (string) $b['tls_ca'];
            /* A tanúsítvány ELLENŐRZÉSE külön kapcsoló a PHP-ban, és
               alapértelmezésben BE van kapcsolva. Csak akkor vedd ki, ha a
               kiszolgáló saját aláírású tanúsítványt használ — és akkor is
               inkább a CA-t add meg. */
            $ki[PDO::MYSQL_ATTR_SSL_VERIFY_SERVER_CERT] = !empty($b['tls_ellenoriz']);
        } elseif ($tavoli) {
            error_log('OTH CRM/MySQL: TÁVOLI adatbázis TLS nélkül (' . (string) $b['hoszt']
                    . ') — a jelszó és a beküldött adatok titkosítatlanul utaznak.');
        }

        return $ki;
    }

    /**
     * A táblanév NEM lehet paraméter az előkészített utasításban, ezért itt
     * szűrjük: csak azonosító-alakú név mehet át. A beállításból jön, tehát nem
     * a látogatótól — de egy elgépelt konfigurációs sor így hibát ad, nem
     * érvényes SQL-t valahol máshol.
     */
    private static function tablanev(string $nev): string
    {
        if (!preg_match('/^[A-Za-z_][A-Za-z0-9_]{0,63}$/', $nev)) {
            throw new RuntimeException('Érvénytelen táblanév a beállításban.');
        }

        return '`' . $nev . '`';
    }

    /** Üres szöveg helyett NULL — a hiányzó adat ne üres sztringként landoljon. */
    private static function ures($ertek): ?string
    {
        $ertek = is_array($ertek) ? implode(', ', array_map('strval', $ertek)) : $ertek;
        $ertek = $ertek === null ? null : trim((string) $ertek);

        return ($ertek === null || $ertek === '') ? null : $ertek;
    }

    /** A hibaüzenet első, ártalmatlan része — SQLSTATE és a driver kódja. */
    private static function rovidHiba(Throwable $e): string
    {
        $uzenet = $e->getMessage();
        if (preg_match('/^SQLSTATE\[[A-Z0-9]+\](\s*\[\d+\])?/', $uzenet, $m)) {
            return $m[0];
        }

        return substr($uzenet, 0, 60);
    }
}
