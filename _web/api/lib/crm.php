<?php
/**
 * crm.php — a kitöltések átadása a DealKeeper CRM-nek.
 * ---------------------------------------------------------------------------
 * MINDEN KITÖLTÉST ÁTAD, AKKOR IS, HA NINCS E-MAIL-CÍM.
 *
 * A főoldali modulok (ársávbecslő, megoldás-ajánló) szándékosan nem kérnek
 * nevet: a látogató tájékozódik, nem kapcsolatba lép. Ezekből a CRM-ben nem
 * lesz érdeklődő — nincs kit felhívni —, de rögzülnek NÉVTELEN ügyrekordként:
 *
 *   * megmutatják, hányan jutnak el a weboldalig, és mire keresnek választ,
 *   * és ha ugyanaz a látogató KÉSŐBB nevet is ad, az ügyazonosító (`MA-…`)
 *     visszamenőleg összekapcsolja a két beküldést — az értékesítő így már
 *     tudja, mekkora házról és milyen jelenlegi megoldásról van szó.
 *
 * A KÜLDÉS SOSEM AKADÁLYOZHATJA MEG A LEVELET.
 *
 * Ha a CRM nem elérhető, lassú vagy hibázik, a látogató attól még megkapja a
 * visszaigazolást, és mi is az értesítést. Egy megkeresés elvesztése
 * összehasonlíthatatlanul drágább, mint egy késve érkező CRM-rekord — ezért
 * fut rövid időkorláttal, és ezért nyeli el a hibát a naplóba.
 *
 * AZ ALÁÍRÁS. A kapu a nyílt interneten ül, ezért minden kérés HMAC-aláírást
 * és időbélyeget visz. A titok forrásonként külön, a config.php-ban (gitignore).
 */
declare(strict_types=1);

final class OthCrm
{
    /** Rövid: a látogató nem várhat a CRM-re. */
    private const TIMEOUT = 4;

    /**
     * Egy kitöltés átadása.
     *
     * @param  string  $csatorna  a BELSŐ csatornanév ('kapcsolat', 'arsav',
     *                            'osszehasonlito', 'konzultacio') — NEM a CRM
     *                            forrás-azonosítója. Az, hogy melyik csatorna
     *                            melyik CRM-forrásba megy, a config dolga.
     * @param  array   $adat    a beküldés a CRM szerződése szerint
     *
     * @return bool sikerült-e — a VÉGPONTOK NE ÁGAZZANAK EL rajta. A látogató
     *              beküldése akkor is sikeres, ha a CRM éppen nem elérhető: a
     *              levél már elment. A visszatérési érték a próbáé és a
     *              naplóé, nem a válaszé.
     */
    public static function kuld(array $CFG, string $csatorna, array $adat): bool
    {
        $beall = $CFG['crm'] ?? [];

        if (empty($beall['engedelyezve']) || empty($beall['url'])) {
            return false;
        }

        /*
         * A CSATORNA → FORRÁS LEKÉPEZÉS A CONFIGBAN ÁLL, NEM A KÓDBAN.
         *
         * A CRM forrás-azonosítója (slug) ott dől el, ahol a forrást felveszik,
         * és UTÓLAG NEM ÁTNEVEZHETŐ — ez a CRM-ben tudatos döntés, mert egy
         * átnevezés csendben elnémítaná a weboldalt. A slug tehát adottság,
         * amihez nekünk kell igazodni.
         *
         * Ha a végpontokba drótoznánk be, minden CRM-oldali elnevezés hét fájl
         * módosítását és új feltöltést jelentene — és amíg az meg nem történik,
         * a kitöltések 404-gyel némán elvesznek. Így viszont egyetlen
         * config-sor átírása elég, kódmódosítás nélkül.
         */
        $csat = $beall['csatornak'][$csatorna] ?? null;

        if (!is_array($csat)) {
            error_log("OTH CRM: nincs beállítva ez a csatorna: {$csatorna}");

            return false;
        }

        $forras = (string) ($csat['forras'] ?? '');
        $titok  = (string) ($csat['titok'] ?? '');

        if ($forras === '' || $titok === '') {
            error_log("OTH CRM: hiányos csatorna-beállítás: {$csatorna}");

            return false;
        }

        $torzs     = json_encode($adat, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
        $idobelyeg = (string) time();

        /*
         * AZ ALÁÍRÁS AZ IDŐBÉLYEGET IS TARTALMAZZA.
         *
         * Enélkül egy egyszer elcsípett kérés korlátlanul újrajátszható lenne:
         * ugyanaz az aláírás holnap is érvényes maradna, és bárki
         * megkereséseket gyárthatna a nevünkben.
         */
        /*
         * AZ `sha256=` ELŐTAG A SZERZŐDÉS RÉSZE, nem díszítés. A CRM a
         * teljes, előtagos szöveget hasonlítja össze `hash_equals`-szal —
         * csupasz hexet küldve minden kérés 401-gyel pattan vissza, és a
         * kitöltés némán elveszik. Ez a sor volt az egyetlen eltérés a két
         * oldal között, és csak végpontok közötti próbán derült ki.
         */
        $alairas = 'sha256=' . hash_hmac('sha256', $idobelyeg . '.' . $torzs, $titok);

        $url = rtrim((string) $beall['url'], '/') . '/' . rawurlencode($forras);

        $ch = curl_init($url);

        curl_setopt_array($ch, [
            CURLOPT_POST           => true,
            CURLOPT_POSTFIELDS     => $torzs,
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT        => self::TIMEOUT,
            CURLOPT_CONNECTTIMEOUT => 2,
            CURLOPT_HTTPHEADER     => [
                'Content-Type: application/json',
                'X-Dk-Timestamp: ' . $idobelyeg,
                'X-Dk-Signature: ' . $alairas,
            ],
        ]);

        $valasz = curl_exec($ch);
        $kod    = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        $hiba   = curl_error($ch);

        /* PHP 8.0 óta a lezárás automatikus; 8.5-től a hívás E_DEPRECATED-et ír
           a naplóba — a látogatói forgalom minden beküldésnél telefirkálná. */
        unset($ch);

        /*
         * A HIBA A NAPLÓBA MEGY, nem a válaszba.
         *
         * A látogató nem tud mit kezdeni azzal, hogy a CRM nem vette át a
         * kitöltését — a levele attól még megérkezett hozzánk. A napló
         * viszont megmondja, ha a kapu napok óta nem működik.
         */
        if ($kod < 200 || $kod >= 300) {
            error_log("OTH CRM: {$forras} → HTTP {$kod} " . ($hiba !== '' ? $hiba : (string) $valasz));

            return false;
        }

        return true;
    }

    /**
     * A KÖZÖS BEKÜLDÉSI ALAK.
     *
     * A CRM magyar kulcsokat vár, mert ezt az űrlapot is magyar mezőnevekkel
     * írjuk — a fordítás a CRM oldalán, EGY helyen történik.
     *
     * @param  array  $kapcsolat  nev, email, telefon (bármelyik elhagyható)
     * @param  array  $megkereses targy, uzenet, becsult_ertek, valaszok
     */
    public static function csomag(
        ?string $ugyAzonosito,
        ?string $kulsoAzonosito,
        array $kapcsolat,
        array $megkereses,
        bool $hozzajarulas = false,
    ): array {
        $csomag = [];

        if ($ugyAzonosito !== null && $ugyAzonosito !== '') {
            /*
             * AZ ÜGYAZONOSÍTÓ A LEGFONTOSABB MEZŐ.
             *
             * Ez fűzi össze ugyanannak a látogatónak a több kitöltését — a
             * névtelen ársávbecslőt a később megadott névvel. Enélkül egy
             * ember három megkeresésként jelenne meg a CRM-ben, és három
             * kolléga hívná fel ugyanazzal a kérdéssel.
             */
            $csomag['ugy_azonosito'] = $ugyAzonosito;
        }

        if ($kulsoAzonosito !== null && $kulsoAzonosito !== '') {
            // Ismételt kézbesítésnél ebből tudja a CRM, hogy ugyanaz a beküldés.
            $csomag['external_id'] = $kulsoAzonosito;
        }

        $kapcsolat = array_filter($kapcsolat, static fn ($v): bool => $v !== null && $v !== '');

        if ($kapcsolat !== []) {
            $csomag['kapcsolat'] = $kapcsolat;
        }

        $csomag['megkereses'] = array_filter(
            $megkereses,
            static fn ($v): bool => $v !== null && $v !== '' && $v !== [],
        );

        $csomag['gdpr'] = ['hozzajarulas' => $hozzajarulas];

        return $csomag;
    }
}
