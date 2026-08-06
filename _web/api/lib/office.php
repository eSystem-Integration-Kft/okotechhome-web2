<?php
/**
 * office.php — szöveg kinyerése Office-dokumentumokból.
 * ---------------------------------------------------------------------------
 * A DOCX és az XLSX valójában ZIP-archívum XML-ekkel. A szöveg ezért
 * kibontható külső könyvtár nélkül, a beépített ZipArchive-val — és ha
 * szöveggé alakítottuk, a modell már ugyanúgy tudja olvasni, mint egy PDF-et.
 *
 * A RÉGI .xls (BIFF) NEM ZIP, hanem bináris formátum. Azt nem bontjuk ki:
 * a félig sikerült kiolvasás rosszabb, mint az őszinte „nem tudtuk elolvasni",
 * mert téves adatot vinne az összehasonlításba.
 */

declare(strict_types=1);

final class OthOffice
{
    /** @return string|null a kinyert szöveg, vagy null, ha nem megy */
    public static function szoveg(string $adat, string $mime): ?string
    {
        $zip = self::zipMegnyit($adat);
        if ($zip === null) {
            return null;                 // régi .xls/.doc — bináris, nem bontjuk
        }
        try {
            if (str_contains($mime, 'wordprocessingml')) {
                return self::docx($zip);
            }
            if (str_contains($mime, 'spreadsheetml')) {
                return self::xlsx($zip);
            }
            return null;
        } finally {
            $zip->close();
        }
    }

    private static function zipMegnyit(string $adat): ?ZipArchive
    {
        /* A ZipArchive fájlt vár, nem memóriapuffert. A tmp fájl a kérés végén
           törlődik; a webgyökérbe semmi nem kerül. */
        $tmp = tempnam(sys_get_temp_dir(), 'oth');
        if ($tmp === false || file_put_contents($tmp, $adat) === false) {
            return null;
        }
        $zip = new ZipArchive();
        $ok = $zip->open($tmp) === true;
        @unlink($tmp);                   // a nyitott leíró tovább él
        return $ok ? $zip : null;
    }

    /** Bekezdésenként új sor, hogy a szerkezet ne vesszen el. */
    private static function docx(ZipArchive $zip): ?string
    {
        $xml = $zip->getFromName('word/document.xml');
        if ($xml === false) {
            return null;
        }
        $xml = preg_replace('#</w:p>#', "\n", $xml);
        $xml = preg_replace('#<w:tab[^>]*/>#', "\t", $xml);
        return self::tisztit(strip_tags($xml));
    }

    /**
     * Az XLSX a cellák szövegét megosztott táblában tárolja; a munkalap csak
     * indexre hivatkozik. Ezért előbb a táblát olvassuk be, aztán a lapokat.
     */
    private static function xlsx(ZipArchive $zip): ?string
    {
        $kozos = [];
        $ss = $zip->getFromName('xl/sharedStrings.xml');
        if ($ss !== false && preg_match_all('#<si>(.*?)</si>#s', $ss, $m)) {
            foreach ($m[1] as $si) {
                $kozos[] = self::tisztit(strip_tags($si));
            }
        }

        $ki = [];
        for ($i = 0; $i < $zip->numFiles; $i++) {
            $nev = $zip->getNameIndex($i);
            if (!preg_match('#^xl/worksheets/sheet\d+\.xml$#', (string) $nev)) {
                continue;
            }
            $lap = $zip->getFromName($nev);
            if ($lap === false) { continue; }
            /* Soronként olvassuk, hogy a táblázat sorszerkezete megmaradjon —
               egy ajánlatnál ez hordozza a tétel–ár párosítást. */
            preg_match_all('#<row[^>]*>(.*?)</row>#s', $lap, $sorok);
            foreach ($sorok[1] as $sor) {
                $cellak = [];
                preg_match_all('#<c[^>]*?(?:\st="(\w+)")?[^>]*>(.*?)</c>#s', $sor, $cs, PREG_SET_ORDER);
                foreach ($cs as $c) {
                    $ertek = self::tisztit(strip_tags($c[2] ?? ''));
                    if (($c[1] ?? '') === 's' && $ertek !== '') {
                        $ertek = $kozos[(int) $ertek] ?? '';
                    }
                    if ($ertek !== '') { $cellak[] = $ertek; }
                }
                if ($cellak) { $ki[] = implode("\t", $cellak); }
            }
        }
        return $ki ? implode("\n", $ki) : null;
    }

    private static function tisztit(string $s): string
    {
        $s = html_entity_decode($s, ENT_QUOTES | ENT_XML1, 'UTF-8');
        return trim(preg_replace('/[ \t]+/', ' ', $s) ?? '');
    }
}
