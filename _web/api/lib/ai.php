<?php
/**
 * ai.php — közös Anthropic-hívó a konzultációs végpontokhoz.
 * ---------------------------------------------------------------------------
 * Miért külön fájl: két végpont hívja (kitöltéssegéd és a beküldés utáni
 * összefoglalók), és a kulcs, a modell, a hibanaplózás és a timeout-kezelés
 * mindkettőnél ugyanaz. Ha ez a három helyen külön élne, három helyen kellene
 * javítani, és a kulcs is háromszor jelenne meg.
 *
 * A hívás SOHA nem dob a látogató felé: ha az AI nem érhető el, a hívó dönti
 * el, mit tesz. A kitöltéssegédnél ez „töltse ki kézzel", a beküldésnél pedig
 * az, hogy a levél az AI-összefoglaló NÉLKÜL megy ki — a megkeresés attól még
 * megérkezett, és azt elveszíteni sokkal drágább, mint egy hiányzó bekezdést.
 */

declare(strict_types=1);

final class OthAi
{
    /**
     * Egy kérés az Anthropic Messages API-hoz.
     *
     * @param array $cfg      a $CFG['ai'] tömb (kulcs, modell, timeout)
     * @param string $system  a rendszerpromt
     * @param string $user    a felhasználói üzenet
     * @param array|null $eszkoz  ha megadjuk, kikényszerített tool-hívás lesz
     *                            belőle, és a tool bemenetét adjuk vissza
     * @param int $maxToken
     * @return array|string|null  tool esetén tömb, egyébként szöveg; hibánál null
     */
    public static function keres(array $cfg, string $system, string $user,
                                 ?array $eszkoz = null, int $maxToken = 1200)
    {
        $kulcs = (string) ($cfg['kulcs'] ?? '');
        if ($kulcs === '' || str_starts_with($kulcs, 'IDE_JON')) {
            error_log('OTH AI: nincs beállítva API-kulcs — a hívás kimarad.');
            return null;
        }

        $kereles = [
            'model'      => $cfg['modell'] ?? 'claude-sonnet-5',
            'max_tokens' => $maxToken,
            'system'     => $system,
            'messages'   => [['role' => 'user', 'content' => $user]],
        ];
        if ($eszkoz !== null) {
            $kereles['tools']       = [$eszkoz];
            $kereles['tool_choice'] = ['type' => 'tool', 'name' => $eszkoz['name']];
        }

        /* A PHP futásidő-korlátja alá kell menni, különben a szkript hal meg
           előbb, és a látogató üres választ kap hibaüzenet helyett. */
        $phpKorlat = (int) ini_get('max_execution_time');
        $korlat = (int) ($cfg['timeout'] ?? 60);
        if ($phpKorlat > 5) { $korlat = min($korlat, $phpKorlat - 3); }

        $ch = curl_init('https://api.anthropic.com/v1/messages');
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST           => true,
            CURLOPT_TIMEOUT        => max(10, $korlat),
            CURLOPT_HTTPHEADER     => [
                'content-type: application/json',
                'x-api-key: ' . $kulcs,
                'anthropic-version: 2023-06-01',
            ],
            CURLOPT_POSTFIELDS => json_encode($kereles, JSON_UNESCAPED_UNICODE),
        ]);
        $valasz = curl_exec($ch);
        $kod = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $curlHiba = curl_error($ch);
        curl_close($ch);

        if ($valasz === false || $kod !== 200) {
            /* A kérés tartalma NEM kerülhet a naplóba: benne van a látogató
               leírása, a fejlécben pedig a kulcs. */
            error_log('OTH AI: HTTP ' . $kod . ($curlHiba ? ' · ' . $curlHiba : ''));
            return null;
        }

        $adat = json_decode((string) $valasz, true);
        if (!is_array($adat) || empty($adat['content'])) {
            error_log('OTH AI: értelmezhetetlen válasz.');
            return null;
        }

        foreach ($adat['content'] as $blokk) {
            if ($eszkoz !== null && ($blokk['type'] ?? '') === 'tool_use') {
                return is_array($blokk['input'] ?? null) ? $blokk['input'] : null;
            }
            if ($eszkoz === null && ($blokk['type'] ?? '') === 'text') {
                return trim((string) $blokk['text']);
            }
        }
        return null;
    }
}
