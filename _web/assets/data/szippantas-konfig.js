/* =============================================================================
   ÖkoTech Home — Szippantási díj kalkulátor · KONFIGURÁCIÓ
   -----------------------------------------------------------------------------
   EZT A FÁJLT A CÉG SZERKESZTHETI, fejlesztő nélkül. A modul logikája
   (`assets/js/szippantas.js`) nem tartalmaz sem díjat, sem településnevet —
   azok kizárólag itt élnek.

   Módosítás után elég a fájlt feltölteni és a hivatkozás verzióját emelni
   (`szippantasi-dij-kalkulator.html`: `szippantas-konfig.js?v=NN`), mert a
   `.htaccess` egy évig cache-eli a JS-t.

   ⚠️ EZ A FÁJL NEM ÁRLISTA. A `dijak` tömb induláskor ÜRES: jelenleg egyetlen
   település díjszabását sem ismerjük ellenőrzött forrásból. Ide KIZÁRÓLAG
   olyan sor kerülhet, amelyet számla, szolgáltatói ártáblázat vagy önkormányzati
   rendelet igazol — a `forras` és az `ervenyes` mező kitöltése ezért kötelező.
   Becsült, „hallottam", „kb." érték ebbe a fájlba nem írható.
   ============================================================================= */

window.OTH_SZIPPANTAS = {

  /* ------------------------------------------------------------ PÉLDAÉRTÉKEK */
  /* A kalkulátor ezekkel indul, hogy a látogató lásson működő számpéldát.
     A felület KIÍRJA, hogy ezek példák, és minden mező mellett ott a jelzés,
     amíg a látogató felül nem írja.

     FORRÁS: megrendelői brief (Anna, 2026. 08.) — a briefben is „Példa"
     oszlopcímmel szerepelnek. NEM egy konkrét település díjszabása. */
  peldaDijak: {
    /* Kiinduló HASZNÁLATI értékek. Nem állítás arról, hogy egy háztartás
       ennyiszer vagy ennyit szippantat — azért állnak itt, hogy a kalkulátor
       ne nullát mutasson az első pillanatban. A felület jelzi, hogy példa. */
    alkalom:        2,   /* alkalom / év                                      */
    m3:             4,   /* m³ / alkalom                                      */

    kiszallas:  12000,   /* Ft / alkalom — lehet 0 is                          */
    uritesM3:    3500,   /* Ft / m³                                            */
    minimumDij: 25000,   /* Ft / alkalom — lehet 0 (nincs minimumdíj)          */
    minimumM3:      5,   /* a minimumdíjban FOGLALT m³ (0 … kocsi űrtartalma)  */
    kocsiM3:        8,   /* a szippantóautó űrtartalma m³-ben                  */
    kmDij:          0,   /* Ft / km — távolságarányos díj, ha a szolgáltató kér */
    tavolsagKm:     0,   /* megteendő távolság km-ben (oda-vissza, ha úgy számol) */
    egyeb:          0    /* Ft / alkalom — egyéb tétel (pl. tömlőhossz-felár)  */
  },

  /* -------------------------------------------------------- KOCSI-ŰRTARTALOM */
  /* A gyakorlatban előforduló járműméretek. Ezek a sávok adják a kalkulátor
     gyorsválasztóit; a látogató kézzel is beírhat értéket.
     FORRÁS: megrendelői brief (Anna, 2026. 08.). */
  kocsiSavok: [
    { kulcs: 'kicsi',   nev: 'Kisebb autó',  jelzo: '3–5 m³',   ertek: 4  },
    { kulcs: 'atlagos', nev: 'Átlagos méret', jelzo: '6–8 m³',   ertek: 7  },
    { kulcs: 'nagy',    nev: 'Nagyobb autó', jelzo: '10–12 m³', ertek: 11 }
  ],
  /* A kocsi-űrtartalom mező megengedett tartománya. */
  kocsiMin: 1,
  kocsiMax: 20,

  /* ------------------------------------------------------------------ MEGYÉK */
  /* Magyarország 19 vármegyéje + Budapest. A `sor` / `oszlop` a CSEMPETÉRKÉP
     rácshelye (6 oszlop × 5 sor). Ez NEM földrajzi térkép, hanem csempe-
     kartogram: minden egység azonos méretű csempe, a helyük a valós kelet–
     nyugati és észak–déli sorrendet követi. Így nem állítunk pontos
     határvonalat ott, ahol nincs hiteles térképi forrásunk.

     `kod`: a KSH/rendszám szerinti kétbetűs rövidítés — ez a `dijak` tömb
     kulcsa is, tehát átnevezni csak együtt szabad. */
  megyek: [
    { kod: 'GS', nev: 'Győr-Moson-Sopron',        rovid: 'Győr-M-S',  sor: 1, oszlop: 2 },
    { kod: 'KE', nev: 'Komárom-Esztergom',        rovid: 'Kom-Eszt',  sor: 1, oszlop: 3 },
    { kod: 'NO', nev: 'Nógrád',                   rovid: 'Nógrád',    sor: 1, oszlop: 4 },
    { kod: 'BZ', nev: 'Borsod-Abaúj-Zemplén',     rovid: 'Borsod',    sor: 1, oszlop: 5 },
    { kod: 'SZ', nev: 'Szabolcs-Szatmár-Bereg',   rovid: 'Szabolcs',  sor: 1, oszlop: 6 },

    { kod: 'VA', nev: 'Vas',                      rovid: 'Vas',       sor: 2, oszlop: 1 },
    { kod: 'VE', nev: 'Veszprém',                 rovid: 'Veszprém',  sor: 2, oszlop: 2 },
    { kod: 'BU', nev: 'Budapest',                 rovid: 'Budapest',  sor: 2, oszlop: 3 },
    { kod: 'PE', nev: 'Pest',                     rovid: 'Pest',      sor: 2, oszlop: 4 },
    { kod: 'HE', nev: 'Heves',                    rovid: 'Heves',     sor: 2, oszlop: 5 },
    { kod: 'HB', nev: 'Hajdú-Bihar',              rovid: 'Hajdú-B',   sor: 2, oszlop: 6 },

    { kod: 'ZA', nev: 'Zala',                     rovid: 'Zala',      sor: 3, oszlop: 1 },
    { kod: 'SO', nev: 'Somogy',                   rovid: 'Somogy',    sor: 3, oszlop: 2 },
    { kod: 'FE', nev: 'Fejér',                    rovid: 'Fejér',     sor: 3, oszlop: 3 },
    { kod: 'BK', nev: 'Bács-Kiskun',              rovid: 'Bács-K',    sor: 3, oszlop: 4 },
    { kod: 'JN', nev: 'Jász-Nagykun-Szolnok',     rovid: 'Jász-N-Sz', sor: 3, oszlop: 5 },
    { kod: 'BE', nev: 'Békés',                    rovid: 'Békés',     sor: 3, oszlop: 6 },

    { kod: 'TO', nev: 'Tolna',                    rovid: 'Tolna',     sor: 4, oszlop: 3 },
    { kod: 'CS', nev: 'Csongrád-Csanád',          rovid: 'Csongrád',  sor: 4, oszlop: 5 },

    { kod: 'BA', nev: 'Baranya',                  rovid: 'Baranya',   sor: 5, oszlop: 3 }
  ],

  /* --------------------------------------------------- TELEPÜLÉSI ADATBÁZIS */
  /* ⚠️ SZÁNDÉKOSAN ÜRES. Egyetlen település díjszabását sem ismerjük ellenőrzött
     forrásból, és becsült értéket ide nem írunk — a látogató a saját számláját
     nézve pontosabbat tud, mint amit mi tippelnénk.

     Egy sor felvételéhez KÖTELEZŐ: `megye`, `telepules`, `ervenyes`, `forras`.
     A díjmezők közül ami nem ismert, az maradjon `null` — a 0 azt jelenti,
     hogy a tétel LÉTEZIK, de nulla forint (pl. nincs kiszállási díj), a `null`
     pedig azt, hogy nem tudjuk. A kettő nem cserélhető fel.

     Minta (kommentben, hogy ne látszódjon adatnak):

     { megye: 'PE', telepules: 'Példafalu', szolgaltato: 'Példa Kft.',
       kiszallas: 12000, uritesM3: 3500, minimumDij: 25000, minimumM3: 5,
       kocsiM3: 8, kmDij: null, ervenyes: '2026-01',
       forras: 'szolgáltatói ártáblázat' }
  */
  dijak: [],

  /* ----------------------------------------------------------- ADATBEKÜLDÉS */
  /* A díjbeküldő űrlap végpontja. Üresen hagyva a modul NEM állítja, hogy
     elküldte az adatot — kiírja, hogy a beküldés még nincs élesítve, és
     felkínálja az e-mailes utat. Félrevezető visszaigazolás nincs. */
  vegpont: 'api/szippantasi-dij',

  /* Ide megy a beküldés, ha a végpont nem érhető el. */
  tartalekEmail: 'kapcsolat@okotechhome.hu',

  /* Az adatkezelési tájékoztató útvonala — a hozzájárulás mellett jelenik meg. */
  adatkezelesUrl: 'adatkezelesi-tajekoztato'
};
