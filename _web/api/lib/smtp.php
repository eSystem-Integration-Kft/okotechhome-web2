<?php
/**
 * smtp.php — minimális SMTP-kliens hitelesítéssel, függőség nélkül.
 * ---------------------------------------------------------------------------
 * Miért nem a beépített `mail()`: az a helyi MTA-nak adja át a levelet,
 * hitelesítés nélkül. Megosztott tárhelyen ez vagy nem működik, vagy a levél
 * SPF/DKIM nélkül megy ki, és spambe kerül. Az ügyfél saját postafiókjából,
 * hitelesítve küldeni a megbízható út — ahhoz viszont SMTP kell.
 *
 * Miért nem PHPMailer: composer nincs a tárhelyen, és a feladat ennyi —
 * kapcsolódás, EHLO, AUTH LOGIN, MAIL FROM / RCPT TO / DATA. A könyvtár
 * súlya és frissítési kötelezettsége nem áll arányban ezzel.
 *
 * Támogatott: implicit TLS (465, `ssl`) és STARTTLS (587, `tls`).
 */

declare(strict_types=1);

final class OthSmtpHiba extends RuntimeException {}

final class OthSmtp
{
    /** @var resource|null */
    private $sock = null;
    private array $cfg;

    public function __construct(array $cfg)
    {
        $this->cfg = $cfg;
    }

    /**
     * @param string   $fromCim   boríték-feladó (a hitelesített fiók)
     * @param string   $fromNev   megjelenített név
     * @param string[] $cimzettek
     * @param string   $targy
     * @param string   $torzs     kész MIME-törzs (fejlécek nélkül)
     * @param string[] $fejlecek  további fejlécek `Név: érték` alakban
     */
    public function kuld(
        string $fromCim,
        string $fromNev,
        array $cimzettek,
        string $targy,
        string $torzs,
        array $fejlecek = []
    ): void {
        $this->nyit();
        try {
            $this->parancs("MAIL FROM:<{$fromCim}>", [250]);
            foreach ($cimzettek as $c) {
                $this->parancs("RCPT TO:<{$c}>", [250, 251]);
            }
            $this->parancs('DATA', [354]);

            $fej = array_merge([
                'Date: ' . date('r'),
                'From: ' . self::fejlecNev($fromNev) . " <{$fromCim}>",
                'To: ' . implode(', ', $cimzettek),
                'Subject: ' . self::fejlecErtek($targy),
                'Message-ID: <' . bin2hex(random_bytes(12)) . '@' . $this->cfg['host'] . '>',
                'MIME-Version: 1.0',
            ], $fejlecek);

            /* A törzsben a sor eleji pontot duplázni kell, különben a
               `.` egyedül a levél végét jelentené (RFC 5321 4.5.2). */
            $adat = implode("\r\n", $fej) . "\r\n\r\n"
                  . preg_replace('/^\./m', '..', $torzs);

            $this->ir($adat . "\r\n.\r\n");
            $this->valasz([250]);
            $this->parancs('QUIT', [221]);
        } finally {
            $this->zar();
        }
    }

    /* ------------------------------------------------------------ kapcsolat */

    private function nyit(): void
    {
        $host = $this->cfg['host'];
        $port = (int) $this->cfg['port'];
        $mod  = $this->cfg['secure'] ?? 'ssl';

        /* A tanúsítvány ellenőrzése BE van kapcsolva. Kikapcsolva a hitelesítő
           adatok egy közbeékelődő félnek is átadhatók lennének. */
        $ctx = stream_context_create(['ssl' => [
            'verify_peer'       => true,
            'verify_peer_name'  => true,
            'allow_self_signed' => false,
            'SNI_enabled'       => true,
        ]]);

        $cim = ($mod === 'ssl' ? 'ssl://' : 'tcp://') . $host . ':' . $port;
        $sock = @stream_socket_client(
            $cim,
            $errno,
            $errstr,
            (int) ($this->cfg['timeout'] ?? 20),
            STREAM_CLIENT_CONNECT,
            $ctx
        );
        if (!$sock) {
            throw new OthSmtpHiba("Nem sikerült kapcsolódni ({$errno}).");
        }
        $this->sock = $sock;
        stream_set_timeout($this->sock, (int) ($this->cfg['timeout'] ?? 20));

        $this->valasz([220]);
        $ehlo = 'oth-' . preg_replace('/[^a-z0-9.\-]/i', '', $host);
        $this->parancs("EHLO {$ehlo}", [250]);

        if ($mod === 'tls') {
            $this->parancs('STARTTLS', [220]);
            if (!stream_socket_enable_crypto($this->sock, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)) {
                throw new OthSmtpHiba('A STARTTLS nem sikerült.');
            }
            $this->parancs("EHLO {$ehlo}", [250]);
        }

        $this->parancs('AUTH LOGIN', [334]);
        $this->parancs(base64_encode((string) $this->cfg['user']), [334]);
        $this->parancs(base64_encode((string) $this->cfg['pass']), [235]);
    }

    private function zar(): void
    {
        if (is_resource($this->sock)) {
            @fclose($this->sock);
        }
        $this->sock = null;
    }

    /* --------------------------------------------------------- protokoll I/O */

    private function ir(string $s): void
    {
        if (@fwrite($this->sock, $s) === false) {
            throw new OthSmtpHiba('Az írás megszakadt.');
        }
    }

    private function parancs(string $parancs, array $vart): string
    {
        $this->ir($parancs . "\r\n");
        return $this->valasz($vart);
    }

    private function valasz(array $vart): string
    {
        $sorok = '';
        while (true) {
            $sor = fgets($this->sock, 1024);
            if ($sor === false) {
                throw new OthSmtpHiba('A kiszolgáló nem válaszolt.');
            }
            $sorok .= $sor;
            /* Többsoros válasznál a kód után `-` áll; az utolsó sorban szóköz. */
            if (strlen($sor) >= 4 && $sor[3] === ' ') {
                break;
            }
        }
        $kod = (int) substr($sorok, 0, 3);
        if (!in_array($kod, $vart, true)) {
            /* A hibaüzenet NEM tartalmazhatja a parancsot: az AUTH sorban a
               jelszó base64-e állna, és bekerülne a naplóba. */
            throw new OthSmtpHiba("Váratlan SMTP-válasz: {$kod}.");
        }
        return $sorok;
    }

    /* ------------------------------------------------------------- fejlécek */

    /** Megjelenített név fejlécbe: RFC 2047 kódolás, ha nem ASCII. */
    public static function fejlecNev(string $s): string
    {
        $s = self::tisztit($s);
        if (preg_match('/^[\x20-\x7E]*$/', $s) && !preg_match('/["\\\\]/', $s)) {
            return '"' . $s . '"';
        }
        return '=?UTF-8?B?' . base64_encode($s) . '?=';
    }

    /** Fejléc-érték (tárgy stb.): kódolás + sortörés-védelem. */
    public static function fejlecErtek(string $s): string
    {
        $s = self::tisztit($s);
        return preg_match('/^[\x20-\x7E]*$/', $s)
            ? $s
            : '=?UTF-8?B?' . base64_encode($s) . '?=';
    }

    /**
     * FEJLÉC-INJEKCIÓ ELLEN. Ez a legfontosabb sor az egész fájlban: ha a
     * felhasználó által megadott érték CR/LF-et tartalmazhatna, tetszőleges
     * további fejlécet (pl. Bcc) fűzhetne a levélhez, és a űrlap
     * spam-továbbítóvá válna.
     */
    public static function tisztit(string $s): string
    {
        return trim(str_replace(["\r", "\n", "\0"], ' ', $s));
    }
}
