-- ============================================================================
-- ÖkoTech Home — webes beküldések fogadó táblája
-- ============================================================================
-- EZT A FÁJLT A CRM TULAJDONOSA FUTTATJA. A weboldal ebbe a táblába ír, a CRM
-- ebből olvas. Más kapcsolat a két rendszer között nincs.
--
-- FUTTATÁS:
--     mysql -u root -p <adatbazis> < crm-mysql-sema.sql
--
-- A tábla létrehozása önmagában biztonságos és megismételhető
-- (`CREATE TABLE IF NOT EXISTS`). A FELHASZNÁLÓ ÉS A JOGOSULTSÁGOK szakasz
-- viszont ki van kommentezve: azt előbb ki kell tölteni, mert jelszót és
-- adatbázisnevet tartalmaz.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- A weboldal öt csatornája (kapcsolat, konzultáció, ajánlat-összehasonlító,
-- ársávbecslő, megoldás-ajánló) EGYETLEN táblába ír. A CRM ebből olvas.
--
-- MIÉRT EGY TÁBLA ÉS NEM ÖT. A csatornák ugyanazt a borítékot használják
-- (`OthCrm::csomag()`): ügyazonosító, külső azonosító, kapcsolat, megkeresés,
-- GDPR. Ami eltér, az a `valaszok` tartalma — és pontosan az, aminek NEM szabad
-- oszlopokká válnia. Öt tábla ugyanazt a szerkezetet ismételné, a lekérdezések
-- pedig minden csatorna-bővítésnél átírásra szorulnának.
--
-- MIÉRT JSON A `valaszok`. A kulcsai az ŰRLAP KÉRDÉSEIT idézik, nem gépi
-- azonosítók: „Hány fő lakik az ingatlanban?”. Ha egy kérdést átfogalmazunk, a
-- kulcs is változik. Oszlopokra képezve minden szövegjavítás adatbázis-migrációt
-- jelentene — így viszont nem jelent semmit.
--
-- KÖVETELMÉNY: MySQL 5.7.8+ vagy MariaDB 10.2+ (JSON típus).
-- Régebbinél a `valaszok` legyen MEDIUMTEXT; a tartalom ugyanaz a JSON szöveg,
-- csak a szerver nem validálja és nem lehet rá `->>` operátorral szűrni.
-- ============================================================================

CREATE TABLE IF NOT EXISTS `web_bekuldes` (
  `id`                BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,

  -- --- honnan jött -------------------------------------------------------
  -- A `csatorna` a MI belső nevünk, a `forras` az, amit a CRM-ben a forrás
  -- kapott. Mindkettő eltárolva: az első a kódunkhoz köt, a második a CRM
  -- riportjaihoz, és a kettő szétválhat anélkül, hogy adat veszne.
  `csatorna`          VARCHAR(32)     NOT NULL
                      COMMENT 'kapcsolat | konzultacio | osszehasonlito | arsav | ajanlo',
  `forras`            VARCHAR(64)     NOT NULL
                      COMMENT 'a CRM-oldali forrás azonosítója',

  -- --- azonosítók --------------------------------------------------------
  -- Az `external_id` EGYEDI: ez teszi a beküldést ismételhetővé. A névtelen
  -- moduloknál szándékosan állandó (`ugy-<azonosító>-<modul>`), mert a látogató
  -- újrafuttathatja a modult — olyankor FRISSÍTÉS a helyes, nem új sor.
  `external_id`       VARCHAR(96)     NOT NULL,

  -- A `MA-XXXX-XXXX` alakú ügyazonosító fűzi össze ugyanannak a látogatónak a
  -- több kitöltését — a névtelen modulokat a később megadott névvel. Ez a
  -- legfontosabb mező, ezért van rajta index.
  `ugy_azonosito`     CHAR(12)                 DEFAULT NULL,

  -- --- kapcsolat ----------------------------------------------------------
  -- Névtelen csatornáknál (arsav, ajanlo) MINDEGYIK NULL. Ez nem hiányosság:
  -- a modulok szándékosan nem kérnek nevet, és amit nem kérünk, azt nem is
  -- tároljuk.
  `nev`               VARCHAR(160)             DEFAULT NULL,
  `email`             VARCHAR(190)             DEFAULT NULL,
  `telefon`           VARCHAR(40)              DEFAULT NULL,
  `ceg`               VARCHAR(160)             DEFAULT NULL,

  -- --- a megkeresés -------------------------------------------------------
  `targy`             VARCHAR(255)             DEFAULT NULL,
  `uzenet`            MEDIUMTEXT               DEFAULT NULL,
  `url`               VARCHAR(255)             DEFAULT NULL,
  `valaszok`          JSON                     DEFAULT NULL
                      COMMENT 'kulcs-érték, a kulcsok az űrlap kérdései — NE képezd oszlopokra',

  -- --- GDPR ---------------------------------------------------------------
  -- Nem azt jelenti, hogy „beküldött egy űrlapot”, hanem hogy KIFEJEZETTEN
  -- hozzájárult a megkereséshez. Ahol 0, ott a rekord marketing céllal nem
  -- kereshető meg. Az ársávbecslőnél csak a visszahívás-kérés számít annak.
  `gdpr_hozzajarulas` TINYINT(1)      NOT NULL DEFAULT 0,

  -- --- állapot ------------------------------------------------------------
  `beerkezett`        DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modositva`         DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP
                                               ON UPDATE CURRENT_TIMESTAMP,
  -- A CRM állítja 1-re, amikor egy ügyintéző megnyitotta. A weboldal SOHA nem
  -- írja — ez a mező a CRM-é.
  `feldolgozva`       TINYINT(1)      NOT NULL DEFAULT 0,

  PRIMARY KEY (`id`),

  -- Az ismétlődő kézbesítés ezen bukik el, nem duplikálódik.
  UNIQUE KEY `uk_external_id` (`external_id`),

  KEY `ix_ugy_azonosito` (`ugy_azonosito`),
  KEY `ix_csatorna_ido`  (`csatorna`, `beerkezett`),
  KEY `ix_feldolgozva`   (`feldolgozva`, `beerkezett`),
  KEY `ix_email`         (`email`)
)
ENGINE = InnoDB
DEFAULT CHARSET = utf8mb4
COLLATE = utf8mb4_hungarian_ci
COMMENT = 'okoth.hu — webes űrlapbeküldések';

-- ============================================================================
-- A WEBOLDAL FELHASZNÁLÓJA CSAK ANNYIT KAP, AMENNYI KELL
-- ----------------------------------------------------------------------------
-- A weboldal ÍR, de nem olvas és nem töröl. Ha a webszervert feltörik, a
-- támadó ezzel a felhasználóval nem tudja kilistázni a korábbi megkereséseket
-- — ez a különbség egy kellemetlenség és egy adatvédelmi incidens között.
--
-- A `feldolgozva` mezőt szándékosan nem tudja állítani: az a CRM dolga.
-- ============================================================================

-- A `SELECT (external_id)` NEM ELHAGYHATÓ, de ennél több NEM IS KELL: a
-- weboldal ismételt kézbesítéskor `UPDATE … WHERE external_id = ?` utasítást ad,
-- és a MySQL a WHERE-hez olvasási jogot kér — erre az EGY oszlopra.
--
-- Kézenfekvő volna `INSERT … ON DUPLICATE KEY UPDATE`-et használni, de a MySQL
-- ahhoz SELECT-jogot kér az ÖSSZES érintett oszlopra: a webes felhasználó akkor
-- ki tudná listázni a korábbi megkeresések nevét és e-mail-címét. (A 8.0.20-as
-- sorálias alak sem segít — próbán ugyanígy 1143-mal elszáll.) Ezért ír a kód
-- INSERT-et, és csak ütközéskor UPDATE-et.

-- CREATE USER 'okoth_web'@'localhost' IDENTIFIED BY '<erős jelszó>';
-- GRANT INSERT,
--       SELECT (`external_id`),
--       UPDATE (`csatorna`, `forras`, `ugy_azonosito`, `nev`, `email`, `telefon`,
--               `ceg`, `targy`, `uzenet`, `url`, `valaszok`, `gdpr_hozzajarulas`)
--   ON `<adatbazis>`.`web_bekuldes` TO 'okoth_web'@'localhost';
-- FLUSH PRIVILEGES;
--
-- Ellenőrzés (mindkettőnek HIBÁT kell adnia):
--   SELECT nev FROM web_bekuldes;     -- 1142: SELECT denied
--   DELETE FROM web_bekuldes;         -- 1142: DELETE denied

-- ============================================================================
-- MEGŐRZÉS
-- ----------------------------------------------------------------------------
-- A névtelen modul-kitöltéseket a weboldal 180 nap után törli a saját
-- tárolójából, és ez az érték az adatkezelési tájékoztatóban is szerepel. Ha a
-- CRM-ben más a megőrzési rend, azt a tájékoztatóban is fel kell tüntetni.
--
-- Példa a névtelen rekordok tisztítására (a CRM ütemezőjéből, nem a weboldalról):
--
-- DELETE FROM `web_bekuldes`
--  WHERE `csatorna` IN ('arsav','ajanlo')
--    AND `nev` IS NULL AND `email` IS NULL
--    AND `beerkezett` < (NOW() - INTERVAL 180 DAY);
-- ============================================================================

-- ============================================================================
-- AMIT A CRM OLVAS
-- ----------------------------------------------------------------------------
-- Az öt csatorna EGY táblába ír. Amit a CRM-nek tennie kell: figyelni az új
-- sorokat, és `feldolgozva = 1`-re állítani, amit egy ügyintéző megnyitott.
-- ============================================================================

-- Új, még senki által meg nem nyitott beküldések:
--
--   SELECT id, beerkezett, csatorna, nev, email, telefon, targy
--     FROM web_bekuldes
--    WHERE feldolgozva = 0
--    ORDER BY beerkezett DESC;

-- Egy beküldés teljes tartalma, a válaszokkal együtt:
--
--   SELECT * FROM web_bekuldes WHERE id = ?;

-- Megnyitás után:
--
--   UPDATE web_bekuldes SET feldolgozva = 1 WHERE id = ?;

-- EGY ÜGYFÉL TELJES ÚTJA. Ez az ügyazonosító értelme: ugyanaz a látogató
-- előbb névtelenül kitölti a modulokat, később nevet is ad. A CRM így
-- visszamenőleg összekapcsolja őket, és az értékesítő már a hívás előtt tudja,
-- mekkora házról van szó.
--
--   SELECT csatorna, beerkezett, nev, targy, valaszok
--     FROM web_bekuldes
--    WHERE ugy_azonosito = 'MA-XXXX-XXXX'
--    ORDER BY beerkezett;

-- KERESÉS A VÁLASZOK KÖZÖTT. A `valaszok` JSON, tehát kulcs szerint szűrhető —
-- de a kulcsok az űrlap kérdéseit idézik, és egy átfogalmazott kérdéssel
-- változnak. Riportot ne erre építs, csak eseti keresést.
--
--   SELECT id, valaszok->>'$."Létesítmény"' AS letesitmeny
--     FROM web_bekuldes
--    WHERE csatorna = 'konzultacio';

-- MARKETING CÉLÚ MEGKERESÉS. Csak ahol a látogató kifejezetten hozzájárult.
-- A `gdpr_hozzajarulas = 0` NEM azt jelenti, hogy elfelejtette bejelölni:
-- azt, hogy nem is kértük tőle — például egy névtelen modul-kitöltésnél.
--
--   SELECT * FROM web_bekuldes WHERE gdpr_hozzajarulas = 1;

-- ============================================================================
-- AMIT A CRM NEM KAP MEG
-- ----------------------------------------------------------------------------
--   · IP-cím, süti- vagy eszközazonosító — nincs a beküldésben
--   · a feltöltött ajánlatfájlok — csak a fájlnevek; a fájlok e-mailben mennek
--   · az AI-elemzés kimenete — azt a látogató kapja meg
-- ============================================================================
