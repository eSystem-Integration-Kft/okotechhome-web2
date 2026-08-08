<?php
/**
 * level.php — HTML levélsablon és MIME-összeállítás.
 * ---------------------------------------------------------------------------
 * Az e-mail nem böngésző. Amit itt kerülni kell, és amiért a kód így néz ki:
 *
 *   * NINCS flexbox és grid — a Gmail, az Outlook és a legtöbb kliens nem
 *     támogatja. Az elrendezés `<table>`, ahogy 2005 óta.
 *   * NINCS külső vagy `<style>` blokkból örökölt formázás — a Gmail a
 *     `<style>`-t kiszűrheti, ezért MINDEN szabály `style=""` attribútumban áll.
 *     (A webhelyen ez tiltott minta; itt szükségszerű, és csak itt.)
 *   * NINCS webfont — a Zilla Slab nem tölthető be, ezért a címeknél Georgia,
 *     a törzsnél rendszerbetű a tartalék.
 *   * A KÉP BLOKKOLVA LEHET: a legtöbb kliens alapból nem tölt le képet, ezért
 *     a fejléc a logó nélkül is olvasható marad (alt-szöveg + szöveges név).
 *   * MINDIG megy sima szöveges változat is (multipart/alternative): enélkül a
 *     levél spampontot kap, és a szövegalapú kliensekben olvashatatlan.
 *
 * Márkaszínek (a designrendszerből): Forest #133216 · Fern #80A640 ·
 * Drizzle #F2F2EF · Stardust #FAFAFA · Slate #4A4F49.
 */

declare(strict_types=1);

final class OthLevel
{
    private const FOREST   = '#133216';
    private const FERN     = '#80A640';
    private const DRIZZLE  = '#F2F2EF';
    private const STARDUST = '#FAFAFA';
    private const SLATE    = '#4A4F49';
    private const VONAL    = '#DCDCD6';

    private const SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif";
    private const SERIF = "Georgia,'Times New Roman',serif";

    /** A beágyazott logó azonosítója; a HTML `cid:` hivatkozása erre mutat. */
    private const LOGO_CID = 'oth-logo';

    private static ?array $logoResz = null;
    private static bool $logoOlvasva = false;

    /**
     * A logó a levélbe ÁGYAZVA megy, nem távoli URL-ről.
     *
     * A `https://…/logo-email.png` hivatkozás két okból is elbukik: a levelezők
     * többsége alapból nem tölt le távoli képet, és ha a webhely még nem él
     * azon a néven, ami a configban áll, akkor a kép egyszerűen nincs meg — a
     * fejlécben törött kép és egy óriásira nyúlt alt-doboz marad.
     *
     * Beágyazva egyik sem fordulhat elő: a kép a levél része. Cserébe minden
     * levél ~12 kB-tal nagyobb, ami ezért bőven megéri.
     *
     * @return array{nev:string,mime:string,adat:string,cid:string}|null
     */
    public static function logoResz(): ?array
    {
        if (!self::$logoOlvasva) {
            self::$logoOlvasva = true;
            $ut = __DIR__ . '/../../assets/img/logo-email.png';
            $adat = is_file($ut) ? @file_get_contents($ut) : false;
            self::$logoResz = ($adat === false || $adat === '') ? null : [
                'nev'  => 'okotech-home.png',
                'mime' => 'image/png',
                'adat' => $adat,
                'cid'  => self::LOGO_CID,
            ];
        }
        return self::$logoResz;
    }

    /**
     * Teljes HTML levél.
     *
     * @param array  $webhely  a config `webhely` tömbje
     * @param string $eyebrow  kis felső címke (pl. „Új megkeresés")
     * @param string $cim      a levél címe
     * @param string $bevezeto egy bekezdés a cím alatt (HTML-escape-elve érkezik)
     * @param array  $adatok   címke => érték párok; az érték már escape-elt
     * @param array  $gomb     ['felirat' => …, 'url' => …] vagy üres
     * @param string $labjegyzet
     */
    public static function html(
        array $webhely,
        string $eyebrow,
        string $cim,
        string $bevezeto,
        array $adatok,
        array $gomb = [],
        string $labjegyzet = ''
    ): string {
        $sorok = '';
        foreach ($adatok as $cimke => $ertek) {
            if ($ertek === '' || $ertek === null) {
                continue;
            }
            $sorok .= '
              <tr>
                <td style="padding:12px 0;border-bottom:1px solid ' . self::VONAL . ';vertical-align:top;width:38%;font-family:' . self::SANS . ';font-size:13px;line-height:1.5;color:' . self::SLATE . ';">'
                . htmlspecialchars((string) $cimke, ENT_QUOTES, 'UTF-8') . '</td>
                <td style="padding:12px 0 12px 16px;border-bottom:1px solid ' . self::VONAL . ';vertical-align:top;font-family:' . self::SANS . ';font-size:15px;line-height:1.6;color:' . self::FOREST . ';">'
                . $ertek . '</td>
              </tr>';
        }

        $gombHtml = '';
        if (!empty($gomb['url'])) {
            $gombHtml = '
              <tr><td style="padding:24px 0 0 0;">
                <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
                  <td style="background:' . self::FERN . ';border-radius:8px;">
                    <a href="' . htmlspecialchars($gomb['url'], ENT_QUOTES, 'UTF-8') . '"
                       style="display:inline-block;padding:13px 26px;font-family:' . self::SANS . ';font-size:15px;font-weight:600;color:' . self::FOREST . ';text-decoration:none;">'
                    . htmlspecialchars($gomb['felirat'], ENT_QUOTES, 'UTF-8') . '</a>
                  </td>
                </tr></table>
              </td></tr>';
        }

        $lab = $labjegyzet !== ''
            ? '<tr><td style="padding:24px 0 0 0;font-family:' . self::SANS . ';font-size:12px;line-height:1.6;color:' . self::SLATE . ';">' . $labjegyzet . '</td></tr>'
            : '';

        $nev  = htmlspecialchars($webhely['nev'], ENT_QUOTES, 'UTF-8');
        $url  = htmlspecialchars($webhely['url'], ENT_QUOTES, 'UTF-8');
        /* Beágyazott logó, ha a fájl megvan; különben marad a configban álló
           URL. A `cid:` hivatkozáshoz a küldő (oth_kuld) csatolja a képet. */
        $logo = self::logoResz()
            ? 'cid:' . self::LOGO_CID
            : htmlspecialchars((string) $webhely['logo'], ENT_QUOTES, 'UTF-8');

        return '<!DOCTYPE html>
<html lang="hu" xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="x-apple-disable-message-reformatting">
<title>' . htmlspecialchars($cim, ENT_QUOTES, 'UTF-8') . '</title>
</head>
<body style="margin:0;padding:0;background:' . self::DRIZZLE . ';">

<!-- Előnézeti szöveg: a postaláda listájában a tárgy mellett ez látszik.
     Utána szóköz-kitöltés, különben a kliens a levél elejét másolná be. -->
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">'
. htmlspecialchars($bevezeto, ENT_QUOTES, 'UTF-8') . str_repeat('&#847;&zwnj;&nbsp;', 40) . '</div>

<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:' . self::DRIZZLE . ';">
  <tr><td align="center" style="padding:32px 16px;">

    <table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:100%;">

      <!-- FEJLÉC: sötét márkasáv. A magasság RÖGZÍTETT, nem `auto`: ha a kép
           mégsem jelenne meg, az `auto` mellett a böngésző az alt-szöveg
           dobozát a szélességhez nyújtja, és a fejléc helyén egy óriási üres
           négyzet marad. Rögzített 69 képpont mellett a helyettesítő szöveg
           egy logónyi sávban ül, világosan a sötét háttéren. -->
      <tr><td style="background:' . self::FOREST . ';border-radius:14px 14px 0 0;padding:28px 32px;">
        <a href="' . $url . '" style="text-decoration:none;">
          <img src="' . $logo . '" width="220" height="69" alt="' . $nev . '"
               style="display:block;border:0;outline:none;width:220px;height:69px;line-height:69px;color:' . self::STARDUST . ';font-family:' . self::SANS . ';font-size:20px;font-weight:700;">
        </a>
      </td></tr>

      <!-- TÖRZS -->
      <tr><td style="background:' . self::STARDUST . ';padding:32px;">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">
          <tr><td style="font-family:' . self::SANS . ';font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:' . self::SLATE . ';padding-bottom:8px;">'
          . htmlspecialchars($eyebrow, ENT_QUOTES, 'UTF-8') . '</td></tr>
          <tr><td style="font-family:' . self::SERIF . ';font-size:24px;line-height:1.25;color:' . self::FOREST . ';padding-bottom:16px;">'
          . htmlspecialchars($cim, ENT_QUOTES, 'UTF-8') . '</td></tr>
          <tr><td style="font-family:' . self::SANS . ';font-size:15px;line-height:1.6;color:' . self::SLATE . ';padding-bottom:8px;">'
          . nl2br(htmlspecialchars($bevezeto, ENT_QUOTES, 'UTF-8')) . '</td></tr>

          <tr><td style="padding-top:16px;">
            <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">' . $sorok . '</table>
          </td></tr>
          ' . $gombHtml . $lab . '
        </table>
      </td></tr>

      <!-- LÁBLÉC -->
      <tr><td style="background:' . self::DRIZZLE . ';border:1px solid ' . self::VONAL . ';border-top:0;border-radius:0 0 14px 14px;padding:20px 32px;font-family:' . self::SANS . ';font-size:12px;line-height:1.7;color:' . self::SLATE . ';">
        <strong style="color:' . self::FOREST . ';">' . $nev . '</strong><br>'
        . htmlspecialchars($webhely['cim'], ENT_QUOTES, 'UTF-8') . '<br>
        <a href="tel:' . preg_replace('/[^0-9+]/', '', $webhely['tel']) . '" style="color:' . self::SLATE . ';">' . htmlspecialchars($webhely['tel'], ENT_QUOTES, 'UTF-8') . '</a> ·
        <a href="mailto:' . htmlspecialchars($webhely['email'], ENT_QUOTES, 'UTF-8') . '" style="color:' . self::SLATE . ';">' . htmlspecialchars($webhely['email'], ENT_QUOTES, 'UTF-8') . '</a> ·
        <a href="' . $url . '" style="color:' . self::SLATE . ';">' . preg_replace('#^https?://#', '', $url) . '</a>
      </td></tr>

    </table>
  </td></tr>
</table>
</body>
</html>';
    }

    /** Sima szöveges változat ugyanabból az adatból. */
    public static function szoveg(
        array $webhely,
        string $cim,
        string $bevezeto,
        array $adatok,
        string $labjegyzet = ''
    ): string {
        $s = $cim . "\n" . str_repeat('=', mb_strlen($cim)) . "\n\n" . $bevezeto . "\n\n";
        foreach ($adatok as $cimke => $ertek) {
            if ($ertek === '' || $ertek === null) {
                continue;
            }
            $tiszta = trim(html_entity_decode(strip_tags(str_replace(['<br>', '<br/>', '<br />'], "\n", (string) $ertek)), ENT_QUOTES, 'UTF-8'));
            $s .= $cimke . ":\n" . $tiszta . "\n\n";
        }
        if ($labjegyzet !== '') {
            $s .= trim(strip_tags($labjegyzet)) . "\n\n";
        }
        $s .= str_repeat('-', 48) . "\n"
            . $webhely['nev'] . "\n" . $webhely['cim'] . "\n"
            . $webhely['tel'] . ' · ' . $webhely['email'] . ' · ' . $webhely['url'] . "\n";
        return $s;
    }

    /** Fájlnév MIME-fejléchez: CR/LF kiszűrve, nem ASCII név kódolva. */
    private static function fejlecFajlnev(string $nev): string
    {
        $nev = str_replace('"', '', OthSmtp::tisztit($nev));
        return preg_match('/^[\x20-\x7E]*$/', $nev)
            ? '"' . $nev . '"'
            : '=?UTF-8?B?' . base64_encode($nev) . '?=';
    }

    /**
     * MIME-törzs összeállítása.
     *
     * A szerkezet attól függ, mi van a levélben. A `cid` kulcsú részek a HTML
     * BELSEJÉBE tartoznak (a logó), a többi rendes melléklet — a kettőt a
     * levelezők eltérően kezelik, ezért nem állhatnak ugyanabban a szintben:
     *
     *   csak szöveg:        multipart/alternative [ szöveg , HTML ]
     *   + beágyazott kép:   multipart/related     [ alternative , kép ]
     *   + melléklet:        multipart/mixed       [ related|alternative , fájlok ]
     *
     * A `related` szint nélkül a logó külön csatolmányként jelenne meg a levél
     * alján, a fejlécben pedig törött kép maradna.
     *
     * @param array $csatolmanyok  [['nev'=>…, 'mime'=>…, 'adat'=>bináris, 'cid'=>…?], …]
     * @return array{0:string,1:string[]}  [törzs, fejlécek]
     */
    public static function mime(string $szoveg, string $html, array $csatolmanyok = []): array
    {
        $beagyazott = [];
        $mellekletek = [];
        foreach ($csatolmanyok as $f) {
            if (!empty($f['cid'])) { $beagyazott[] = $f; } else { $mellekletek[] = $f; }
        }

        $altHatar = 'alt_' . bin2hex(random_bytes(8));
        $alt = "--{$altHatar}\r\n"
             . "Content-Type: text/plain; charset=UTF-8\r\n"
             . "Content-Transfer-Encoding: base64\r\n\r\n"
             . chunk_split(base64_encode($szoveg)) . "\r\n"
             . "--{$altHatar}\r\n"
             . "Content-Type: text/html; charset=UTF-8\r\n"
             . "Content-Transfer-Encoding: base64\r\n\r\n"
             . chunk_split(base64_encode($html)) . "\r\n"
             . "--{$altHatar}--\r\n";

        $torzs = $alt;
        $tipus = 'multipart/alternative; boundary="' . $altHatar . '"';

        if ($beagyazott) {
            $relHatar = 'rel_' . bin2hex(random_bytes(8));
            $torzs = "--{$relHatar}\r\n"
                   . "Content-Type: multipart/alternative; boundary=\"{$altHatar}\"\r\n\r\n"
                   . $alt . "\r\n";
            foreach ($beagyazott as $f) {
                $nev = self::fejlecFajlnev((string) $f['nev']);
                $cid = OthSmtp::tisztit((string) $f['cid']);
                $torzs .= "--{$relHatar}\r\n"
                        . 'Content-Type: ' . $f['mime'] . "; name={$nev}\r\n"
                        . "Content-Transfer-Encoding: base64\r\n"
                        . "Content-ID: <{$cid}>\r\n"
                        . "Content-Disposition: inline; filename={$nev}\r\n\r\n"
                        . chunk_split(base64_encode($f['adat'])) . "\r\n";
            }
            $torzs .= "--{$relHatar}--\r\n";
            /* `type="text/html"`: megmondja a kliensnek, melyik rész hivatkozik
               a beágyazott képekre. Enélkül egyes kliensek külön csatolmányként
               is kilistázzák a logót. */
            $tipus = 'multipart/related; type="text/html"; boundary="' . $relHatar . '"';
        }

        if (!$mellekletek) {
            return [$torzs, ['Content-Type: ' . $tipus]];
        }

        $mixHatar = 'mix_' . bin2hex(random_bytes(8));
        $kulso = "--{$mixHatar}\r\n"
               . 'Content-Type: ' . $tipus . "\r\n\r\n"
               . $torzs . "\r\n";

        foreach ($mellekletek as $f) {
            $nev = self::fejlecFajlnev((string) $f['nev']);
            $kulso .= "--{$mixHatar}\r\n"
                    . 'Content-Type: ' . $f['mime'] . "; name={$nev}\r\n"
                    . "Content-Transfer-Encoding: base64\r\n"
                    . "Content-Disposition: attachment; filename={$nev}\r\n\r\n"
                    . chunk_split(base64_encode($f['adat'])) . "\r\n";
        }
        $kulso .= "--{$mixHatar}--\r\n";

        return [$kulso, ['Content-Type: multipart/mixed; boundary="' . $mixHatar . '"']];
    }
}
