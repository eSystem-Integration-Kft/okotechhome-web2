<?php
/**
 * crm-naplo.php — átadási napló: mit adtunk át, mikor, és megérkezett-e.
 * ---------------------------------------------------------------------------
 * MIÉRT KELL. A CRM-átadás SZÁNDÉKOSAN néma: ha a túloldal nem veszi át a
 * kitöltést, a látogató attól még megkapja a visszaigazolást, és mi is az
 * értesítő levelet. Ez helyes — egy megkeresés elvesztése drágább egy késve
 * érkező CRM-rekordnál —, de van egy ára: kívülről semmi nem látszik. A CRM
 * napokig üres maradhat úgy, hogy közben minden működőnek tűnik.
 *
 * Ez a napló az a hely, ahol mégis látszik.
 *
 * AMI A NAPLÓBA KERÜL: időbélyeg, csatorna, a beküldés külső azonosítója, a
 * szállítás módja, az eredmény és a hiba rövid kódja.
 *
 * AMI NEM: a beküldés TARTALMA. Se név, se e-mail, se telefonszám, se üzenet.
 * A napló üzemeltetési eszköz, nem másodpéldány — egy fájl, ami hónapokig gyűlik
 * a kiszolgálón, ne legyen személyesadat-tár. A `külső azonosító` benne van, de
 * az álnév: dátumból és az e-mail-cím csonkolt lenyomatából áll.
 *
 * HAVI FÁJL, SORONKÉNT EGY JSON. Így a fájl bármikor átvágható a hónap
 * fordulóján, a régi hónap egyben archiválható vagy törölhető, és minden sor
 * önmagában értelmes — egy félbeszakadt írás nem teszi olvashatatlanná a többit.
 */
declare(strict_types=1);

final class OthCrmNaplo
{
    /** Meddig őrizzük. A régebbi havi fájlokat írás közben takarítjuk. */
    private const MEGORZES_HONAP = 12;

    /**
     * Egy átadási kísérlet rögzítése.
     *
     * @param  string  $csatorna    belső csatornanév
     * @param  string  $kulsoAzon   a beküldés külső azonosítója
     * @param  string  $mod         'http' | 'mysql'
     * @param  bool    $siker       megérkezett-e a túloldalon
     * @param  string  $reszlet     HTTP-kód, SQLSTATE vagy rövid hibaok
     * @param  float   $mp          mennyi ideig tartott
     */
    public static function ir(
        string $csatorna,
        string $kulsoAzon,
        string $mod,
        bool $siker,
        string $reszlet = '',
        float $mp = 0.0,
    ): void {
        try {
            $dir = __DIR__ . '/../.crm-naplo';

            /* 0700: a fájlokat csak a webszerver felhasználója olvashatja. Az
               `api/.htaccess` ezen felül a `.`-kal kezdődő útvonalakat és a
               `.log` kiterjesztést is tiltja — a kettő együtt véd. */
            if (!is_dir($dir) && !@mkdir($dir, 0700, true) && !is_dir($dir)) {
                return;
            }

            $sor = json_encode([
                'ido'      => gmdate('c'),
                'csatorna' => $csatorna,
                'azonosito'=> $kulsoAzon,
                'mod'      => $mod,
                'eredmeny' => $siker ? 'ok' : 'hiba',
                'reszlet'  => mb_substr($reszlet, 0, 120),
                'mp'       => round($mp, 3),
            ], JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);

            /* `FILE_APPEND | LOCK_EX`: párhuzamos beküldéseknél a sorok nem
               csúsznak egymásba. Enélkül két egyidejű írás egyetlen kevert,
               olvashatatlan sort adna — és pont forgalmi csúcsban. */
            @file_put_contents(
                $dir . '/' . gmdate('Y-m') . '.log',
                $sor . "\n",
                FILE_APPEND | LOCK_EX,
            );

            self::takarit($dir);
        } catch (Throwable $e) {
            /* A NAPLÓZÁS SOHA NEM BUKTATHATJA EL A BEKÜLDÉST. Ha ide nem tudunk
               írni, az kellemetlen, de a látogató kitöltése ettől még rendben
               van — némán elnyeljük. */
        }
    }

    /** A megőrzési időn túli havi fájlok törlése. Olcsó, mert ritkán talál. */
    private static function takarit(string $dir): void
    {
        $hatar = gmdate('Y-m', strtotime('-' . self::MEGORZES_HONAP . ' months'));
        foreach ((array) @glob($dir . '/*.log') as $f) {
            if (basename($f, '.log') < $hatar) {
                @unlink($f);
            }
        }
    }

    /** A napló beolvasása megjelenítéshez. Legfrissebb elöl. */
    public static function olvas(string $honap, int $max = 500): array
    {
        $f = __DIR__ . '/../.crm-naplo/' . preg_replace('/[^0-9-]/', '', $honap) . '.log';
        if (!is_file($f)) {
            return [];
        }

        $sorok = array_reverse(array_filter(explode("\n", (string) @file_get_contents($f))));
        $ki = [];
        foreach ($sorok as $s) {
            if (count($ki) >= $max) {
                break;
            }
            $d = json_decode($s, true);
            if (is_array($d)) {
                $ki[] = $d;
            }
        }

        return $ki;
    }

    /** Mely hónapokról van napló. */
    public static function honapok(): array
    {
        $ki = [];
        foreach ((array) @glob(__DIR__ . '/../.crm-naplo/*.log') as $f) {
            $ki[] = basename($f, '.log');
        }
        rsort($ki);

        return $ki;
    }
}
