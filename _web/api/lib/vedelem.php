<?php
/**
 * vedelem.php — bemenetellenőrzés, spamszűrés, sebességkorlát, közös válaszok.
 * ---------------------------------------------------------------------------
 * Alapelv: a kliensoldali ellenőrzés NEM ellenőrzés. Minden érték itt is át
 * kell hogy essen a szűrésen, mert a végpont közvetlenül is hívható.
 *
 * Négy réteg véd a visszaéléstől:
 *   1. Origin-ellenőrzés     — más webhelyről indított beküldés (CSRF) kizárva
 *   2. Mézesbödön mező       — a robotok kitöltik, ember nem látja
 *   3. Kitöltési idő         — 3 másodperc alatt nem tölt ki űrlapot ember
 *   4. IP-alapú sebességkorlát — fájlalapú, adatbázis nélkül
 */

declare(strict_types=1);

final class OthVedelem
{
    /** JSON-válasz és kilépés. A státuszkód is beszédes, nem csak a törzs. */
    public static function valasz(int $kod, array $adat): void
    {
        http_response_code($kod);
        header('Content-Type: application/json; charset=utf-8');
        /* A végpont csak a saját oldalról hívható; a hibaválasz sem
           kereshető ki külső oldalról. */
        header('X-Content-Type-Options: nosniff');
        header('Cache-Control: no-store');
        echo json_encode($adat, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        exit;
    }

    public static function hiba(int $kod, string $uzenet): void
    {
        self::valasz($kod, ['ok' => false, 'uzenet' => $uzenet]);
    }

    /** Csak POST, és csak a saját origin-ünkről. */
    public static function keresEllenorzes(array $engedettOrigin): void
    {
        if (($_SERVER['REQUEST_METHOD'] ?? '') !== 'POST') {
            header('Allow: POST');
            self::hiba(405, 'Csak POST kérést fogadunk.');
        }

        $origin = $_SERVER['HTTP_ORIGIN'] ?? '';
        if ($origin === '' && !empty($_SERVER['HTTP_REFERER'])) {
            $p = parse_url($_SERVER['HTTP_REFERER']);
            if (!empty($p['scheme']) && !empty($p['host'])) {
                $origin = $p['scheme'] . '://' . $p['host']
                        . (empty($p['port']) ? '' : ':' . $p['port']);
            }
        }
        /* Üres origin: régi böngésző vagy szigorú adatvédelmi beállítás —
           ilyenkor átengedjük, mert a többi réteg még véd. Rossz origin
           viszont egyértelműen idegen oldalról indított kérés. */
        if ($origin !== '' && !in_array($origin, $engedettOrigin, true)) {
            self::hiba(403, 'A kérés nem a webhelyről érkezett.');
        }
    }

    /** Mézesbödön + kitöltési idő. Mindkettő csendes elutasítás. */
    public static function botEllenorzes(array $be, int $minMasodperc): void
    {
        /* A mezőt a CSS rejti el; ember sosem tölti ki, robot igen. */
        if (trim((string) ($be['weboldal'] ?? '')) !== '') {
            /* Sikeres válasz, hogy a robot ne próbálkozzon tovább — de
               levél nem megy ki. */
            self::valasz(200, ['ok' => true, 'uzenet' => 'Köszönjük, megkaptuk.']);
        }
        $nyitva = (int) ($be['nyitva'] ?? 0);
        if ($nyitva > 0 && (time() - $nyitva) < $minMasodperc) {
            self::hiba(429, 'Túl gyors beküldés. Próbálja meg újra néhány másodperc múlva.');
        }
    }

    /**
     * IP-alapú sebességkorlát. Fájlalapú, mert megosztott tárhelyen nincs
     * garantáltan adatbázis vagy APCu.
     */
    public static function sebessegkorlat(string $kulcs, int $limit, int $ablakPerc): void
    {
        $dir = __DIR__ . '/../.ratelimit';
        if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) {
            return; // ha nem tudunk írni, inkább átengedjük, mint hogy elszálljon
        }
        $ip = $_SERVER['REMOTE_ADDR'] ?? '0.0.0.0';
        $f  = $dir . '/' . hash('sha256', $kulcs . '|' . $ip) . '.json';

        $most  = time();
        $ablak = $ablakPerc * 60;
        $bejegyzesek = [];
        if (is_file($f)) {
            $r = json_decode((string) @file_get_contents($f), true);
            if (is_array($r)) {
                $bejegyzesek = array_values(array_filter($r, fn($t) => ($most - (int) $t) < $ablak));
            }
        }
        if (count($bejegyzesek) >= $limit) {
            self::hiba(429, 'Túl sok beküldés érkezett erről a gépről. Próbálja meg később, vagy hívjon minket.');
        }
        $bejegyzesek[] = $most;
        @file_put_contents($f, json_encode($bejegyzesek), LOCK_EX);

        /* Alkalmi takarítás, hogy a könyvtár ne nőjön korlátlanul. */
        if (random_int(1, 50) === 1) {
            foreach ((array) glob($dir . '/*.json') as $regi) {
                if (is_file($regi) && ($most - filemtime($regi)) > $ablak * 4) {
                    @unlink($regi);
                }
            }
        }
    }

    /**
     * NAPI KERET — webhelyszintű, nem IP-nkénti. Az IP-korlátot elosztott
     * támadás (botnet, proxylista) megkerüli: 30 hívás/óra szorozva ezer
     * címmel már számla. Ez a számláló a NAPOT nézi, címtől függetlenül —
     * a legrosszabb nap költsége így fix plafon alatt marad.
     *
     * NEM lép ki: igaz/hamis a válasza, mert a hívók nem egyformán reagálnak.
     * A kalauz udvarias 503-at ad, a konzultációkérő viszont AI nélkül is
     * kiküldi a levelet — a megkeresés elvesztése drágább minden keretnél.
     */
    public static function napiKeret(string $kulcs, int $limit): bool
    {
        if ($limit <= 0) { return true; }              // 0 vagy negatív: nincs keret
        $dir = __DIR__ . '/../.ratelimit';
        if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) {
            return true;                               // írásképtelen tárhely: átengedjük
        }
        $f = $dir . '/keret-' . preg_replace('/[^a-z0-9_-]/', '', $kulcs)
           . '-' . gmdate('Y-m-d') . '.txt';

        /* Zárolt olvasás-írás: két egyidejű kérés ne számolhasson ugyanarra a
           sorszámra. A c+ mód létrehozza a fájlt, ha még nincs. */
        $h = @fopen($f, 'c+');
        if ($h === false) { return true; }
        flock($h, LOCK_EX);
        $db = (int) stream_get_contents($h);
        $enged = $db < $limit;
        if ($enged) {
            rewind($h);
            ftruncate($h, 0);
            fwrite($h, (string) ($db + 1));
        }
        flock($h, LOCK_UN);
        fclose($h);

        /* Egyszer naplózunk, a keret betelésekor — nem minden elutasításnál,
           különben a napló maga válna a támadás felületévé. */
        if ($enged && $db + 1 === $limit) {
            error_log("OTH keret: a(z) „{$kulcs}\" napi keret ({$limit}) betelt.");
        }
        /* A tegnapi számlálófájlokat az alkalmi takarítás viszi el. */
        if (random_int(1, 100) === 1) {
            foreach ((array) glob($dir . '/keret-*.txt') as $regi) {
                if (is_file($regi) && (time() - filemtime($regi)) > 3 * 86400) {
                    @unlink($regi);
                }
            }
        }
        return $enged;
    }

    /* ------------------------------------------------------- mezőellenőrzés */

    public static function szoveg(array $be, string $kulcs, int $max = 200): string
    {
        $v = (string) ($be[$kulcs] ?? '');
        $v = trim(preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F]/u', '', $v) ?? '');
        return mb_substr($v, 0, $max);
    }

    public static function email(array $be, string $kulcs): string
    {
        $v = self::szoveg($be, $kulcs, 254);
        return filter_var($v, FILTER_VALIDATE_EMAIL) ? $v : '';
    }

    /** Telefon: csak a valóban telefonszám-szerű karakterek maradnak. */
    public static function telefon(array $be, string $kulcs): string
    {
        $v = self::szoveg($be, $kulcs, 40);
        $v = preg_replace('/[^0-9+()\/ \-]/', '', $v) ?? '';
        return trim($v);
    }

    /** Escape-elt, sortöréseket megőrző HTML-részlet. */
    public static function html(string $s): string
    {
        return nl2br(htmlspecialchars($s, ENT_QUOTES, 'UTF-8'));
    }

    /**
     * Feltöltött fájl ellenőrzése. A kiterjesztés ÉS a tényleges tartalom
     * alapján is — a kliens által küldött MIME-típus hamisítható.
     *
     * @return array{nev:string,mime:string,adat:string}
     */
    public static function fajl(array $f, array $cfg): array
    {
        if (($f['error'] ?? UPLOAD_ERR_NO_FILE) !== UPLOAD_ERR_OK) {
            throw new RuntimeException('A fájl feltöltése nem sikerült.');
        }
        if (($f['size'] ?? 0) > $cfg['max_meret']) {
            throw new RuntimeException('A fájl túl nagy (legfeljebb 10 MB).');
        }
        if (!is_uploaded_file($f['tmp_name'])) {
            throw new RuntimeException('Érvénytelen feltöltés.');
        }

        $nev = basename((string) ($f['name'] ?? 'fajl'));
        $ext = strtolower((string) pathinfo($nev, PATHINFO_EXTENSION));
        if (!in_array($ext, $cfg['kiterjesztes'], true)) {
            throw new RuntimeException('Nem támogatott formátum.');
        }

        $valodi = (new finfo(FILEINFO_MIME_TYPE))->file($f['tmp_name']) ?: '';
        if (!in_array($valodi, $cfg['mime'], true)) {
            throw new RuntimeException('A fájl tartalma nem egyezik a kiterjesztéssel.');
        }

        $adat = (string) file_get_contents($f['tmp_name']);
        /* A nevet megtisztítjuk: a fejlécbe kerül, és a címzett gépén fájlnév
           lesz belőle. Útvonal-elemet és vezérlőkaraktert nem engedünk. */
        $nev = preg_replace('/[^\p{L}\p{N}._\- ]+/u', '_', $nev) ?? 'fajl.' . $ext;
        return ['nev' => mb_substr($nev, 0, 120), 'mime' => $valodi, 'adat' => $adat];
    }
}
