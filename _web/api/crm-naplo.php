<?php

declare(strict_types=1);

/**
 * crm-naplo.php — AZ ÁTADÁSI NAPLÓ, BÖNGÉSZŐBŐL.
 *
 * Használat:
 *     https://tst.okoth.hu/api/crm-naplo.php?kod=<a lenti kód>
 *     …&honap=2026-09
 *
 * MIÉRT VAN. A CRM-átadás szándékosan néma: ha a túloldal nem veszi át a
 * kitöltést, a látogató attól még megkapja a visszaigazolást, és a levél is
 * kimegy. Kívülről tehát semmi nem látszik — a CRM napokig üres maradhat úgy,
 * hogy minden működőnek tűnik. Ez a lap az a hely, ahol mégis látszik.
 *
 * AMI ITT LÁTHATÓ: időpont, csatorna, a beküldés külső azonosítója, a szállítás
 * módja, az eredmény és a hiba rövid kódja. A beküldés TARTALMA nem — se név,
 * se e-mail, se üzenet. A napló üzemeltetési eszköz, nem másodpéldány.
 *
 * A KÓD NEM JELSZÓ, csak annyi, hogy a cím ne legyen kitalálható. A lap nem ad
 * hozzáférést semmihez, de a beküldések ütemét és a csatornaneveket megmutatja.
 * ÉLESÍTÉS UTÁN TÖRÖLD, vagy tedd jelszóval védett könyvtárba.
 */

const OTH_NAPLO_KOD = 'a7f3c1e95b2d4806';

if (!hash_equals(OTH_NAPLO_KOD, (string) ($_GET['kod'] ?? ''))) {
    http_response_code(404);
    exit;
}

require __DIR__ . '/lib/crm-naplo.php';

$honapok = OthCrmNaplo::honapok();
$honap   = (string) ($_GET['honap'] ?? ($honapok[0] ?? gmdate('Y-m')));
$sorok   = OthCrmNaplo::olvas($honap, 800);

/* Összesítés csatornánként — ez mondja meg egy pillantásra, hol áll el a lánc. */
$ossz = [];
foreach ($sorok as $s) {
    $k = ($s['csatorna'] ?? '?') . ' · ' . ($s['mod'] ?? '?');
    $ossz[$k] ??= ['ok' => 0, 'hiba' => 0, 'utolso' => ''];
    $ossz[$k][$s['eredmeny'] === 'ok' ? 'ok' : 'hiba']++;
    $ossz[$k]['utolso'] = $ossz[$k]['utolso'] ?: (string) ($s['ido'] ?? '');
}
ksort($ossz);

function h(?string $s): string
{
    return htmlspecialchars((string) $s, ENT_QUOTES, 'UTF-8');
}

/** Az UTC-időbélyeg olvasható, helyi alakban. */
function ido(?string $iso): string
{
    if (!$iso) {
        return '—';
    }
    try {
        $d = new DateTimeImmutable($iso);

        return $d->setTimezone(new DateTimeZone('Europe/Budapest'))->format('m. d. H:i:s');
    } catch (Throwable $e) {
        return h($iso);
    }
}

header('Content-Type: text/html; charset=utf-8');
header('X-Robots-Tag: noindex, nofollow');
?>
<!DOCTYPE html>
<html lang="hu">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>CRM átadási napló — <?= h($honap) ?></title>
<style>
  :root{
    --papir:#f2f5f1; --lap:#fff; --tinta:#141b16; --halk:#6e7c74; --vonal:#d3dad1;
    --ok:#2f6b3a; --ok-h:#e4efe4; --baj:#8c2f2f; --baj-h:#f7e7e5;
  }
  @media (prefers-color-scheme:dark){
    :root{--papir:#0f1512;--lap:#161e19;--tinta:#e8efe8;--halk:#7e8d84;--vonal:#2a362f;
          --ok:#7bc48a;--ok-h:#1b2c20;--baj:#e08c86;--baj-h:#2e1a19}
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--papir);color:var(--tinta);
    font:14px/1.55 ui-sans-serif,-apple-system,"Segoe UI",sans-serif;padding:24px}
  h1{font-size:20px;margin:0 0 4px}
  .halk{color:var(--halk);font-size:13px}
  .sav{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0}
  .sav a{padding:5px 11px;border:1px solid var(--vonal);border-radius:7px;
    background:var(--lap);color:var(--tinta);text-decoration:none;font-size:13px}
  .sav a[aria-current]{border-color:var(--ok);color:var(--ok);font-weight:600}
  table{border-collapse:collapse;width:100%;background:var(--lap);
    border:1px solid var(--vonal);border-radius:9px;overflow:hidden;margin:0 0 26px}
  th,td{text-align:left;padding:8px 11px;border-bottom:1px solid var(--vonal);
    font-variant-numeric:tabular-nums}
  th{background:color-mix(in srgb,var(--vonal) 40%,transparent);font-size:12px;
    text-transform:uppercase;letter-spacing:.05em;color:var(--halk)}
  tr:last-child td{border-bottom:0}
  code{font:12.5px ui-monospace,Menlo,monospace;word-break:break-all}
  .b-ok{background:var(--ok-h);color:var(--ok);padding:2px 8px;border-radius:5px;
    font-size:12px;font-weight:600}
  .b-baj{background:var(--baj-h);color:var(--baj);padding:2px 8px;border-radius:5px;
    font-size:12px;font-weight:600}
  .ures{padding:26px;text-align:center;color:var(--halk);background:var(--lap);
    border:1px dashed var(--vonal);border-radius:9px}
  .gorgo{overflow-x:auto}
</style>
</head>
<body>

<h1>CRM átadási napló</h1>
<p class="halk">Mit adtunk át, mikor, és megérkezett-e a túloldalon.
   A beküldés tartalma szándékosan nincs benne — csak azonosító és eredmény.</p>

<?php if ($honapok): ?>
<nav class="sav" aria-label="Hónapok">
  <?php foreach ($honapok as $h): ?>
    <a href="?kod=<?= h(OTH_NAPLO_KOD) ?>&amp;honap=<?= h($h) ?>"
       <?= $h === $honap ? 'aria-current="page"' : '' ?>><?= h($h) ?></a>
  <?php endforeach; ?>
</nav>
<?php endif; ?>

<?php if (!$sorok): ?>
  <p class="ures">Ebben a hónapban nincs bejegyzés.<br>
     <span class="halk">Ha épp most küldtél be egy űrlapot és ez üres, a CRM-átadás
     ki van kapcsolva (<code>crm.engedelyezve</code>).</span></p>
<?php else: ?>

  <h2 style="font-size:15px;margin:0 0 8px">Összesítés — <?= h($honap) ?></h2>
  <div class="gorgo"><table>
    <thead><tr><th>Csatorna · mód</th><th>Sikeres</th><th>Hibás</th><th>Utolsó</th></tr></thead>
    <tbody>
    <?php foreach ($ossz as $k => $v): ?>
      <tr>
        <td><code><?= h((string) $k) ?></code></td>
        <td><?= (int) $v['ok'] ?></td>
        <td><?= $v['hiba'] ? '<span class="b-baj">' . (int) $v['hiba'] . '</span>' : '0' ?></td>
        <td><?= h(ido($v['utolso'])) ?></td>
      </tr>
    <?php endforeach; ?>
    </tbody>
  </table></div>

  <h2 style="font-size:15px;margin:0 0 8px">Tételek <span class="halk">(legfrissebb elöl,
     legfeljebb 800)</span></h2>
  <div class="gorgo"><table>
    <thead><tr><th>Időpont</th><th>Csatorna</th><th>Mód</th><th>Eredmény</th>
      <th>Részlet</th><th>mp</th><th>Azonosító</th></tr></thead>
    <tbody>
    <?php foreach ($sorok as $s): ?>
      <tr>
        <td><?= h(ido($s['ido'] ?? null)) ?></td>
        <td><?= h($s['csatorna'] ?? '') ?></td>
        <td><code><?= h($s['mod'] ?? '') ?></code></td>
        <td><?= ($s['eredmeny'] ?? '') === 'ok'
                ? '<span class="b-ok">megérkezett</span>'
                : '<span class="b-baj">nem érkezett meg</span>' ?></td>
        <td class="halk"><?= h($s['reszlet'] ?? '') ?></td>
        <td><?= h((string) ($s['mp'] ?? '')) ?></td>
        <td><code><?= h($s['azonosito'] ?? '') ?></code></td>
      </tr>
    <?php endforeach; ?>
    </tbody>
  </table></div>
<?php endif; ?>

<p class="halk">A napló <?= 12 ?> hónapig áll rendelkezésre; a régebbi havi fájlokat
   a rendszer magától törli. <strong>Élesítés után ezt a lapot töröld</strong>,
   vagy tedd jelszóval védett könyvtárba.</p>

</body>
</html>
