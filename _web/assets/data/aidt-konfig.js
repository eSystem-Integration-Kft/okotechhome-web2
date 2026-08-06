/* =============================================================================
   ÖkoTech Home — AI döntéstámogató · KONFIGURÁCIÓ
   -----------------------------------------------------------------------------
   EZT A FÁJLT A CÉG SZERKESZTHETI, fejlesztő nélkül. A modul logikája
   (`assets/js/ai-advisor.js`) nem tartalmaz árakat — azok kizárólag itt élnek.

   Módosítás után elég a fájlt feltölteni és a hivatkozás verzióját emelni
   (`index.html`: `aidt-konfig.js?v=NN`), hogy a látogatók a frisset kapják.

   ⚠️ Az alábbi értékek MÉG NINCSENEK JÓVÁHAGYVA — éles indulás előtt a cég
   szakmai vezetésének kell megerősítenie őket.
   ============================================================================= */
window.OTH_AIDT = {

  /* --------------------------------------------------------------- ÁRSÁVOK */
  /* Minden érték FORINTBAN, [alsó, felső] párként. `null` = nem adunk sávot
     (egyedi méretezés). A kulcsok a kérdéssor válaszazonosítói. */
  arsav: {
    /* alapsáv a háztartás mérete szerint */
    base: {
      "1-2":  [1600000, 2200000],
      "3-4":  [1900000, 2600000],
      "5-6":  [2400000, 3200000],
      "7-10": [3000000, 4200000],
      "10+":  null,                 /* 50 fő feletti kapacitás: egyedi tervezés */
      "x":    [1600000, 3200000]    /* ismeretlen kapacitás — széles tartalék */
    },

    /* felárak FORINTBAN — a telek adottságai és a kivitelezés körülményei.
       A modul ezeket a felső véghez nagyobb súllyal adja hozzá. */
    modifiers: {
      talajviz:   350000,   /* magas talajvíz — betonmedencés kialakítás */
      keveshely:  250000,   /* szűk telek, nehéz gépi hozzáférés */
      lejtes:     150000,   /* lejtős terep */
      hozzaferes: 300000,   /* korlátozott munkagépes megközelítés */
      emeszto:    250000,   /* meglévő emésztő bontása, kiürítése */
      csere:      150000    /* meglévő rendszer cseréje */
    }
  },

  /* ----------------------------------------------------------- ADATKÜLDÉS */
  /* Ide kerül az összefoglaló-küldés végpontja, amint elkészül a backend.
     Üresen hagyva a modul NEM küld adatot sehova, és ezt őszintén jelzi is
     a látogatónak. Külső (nem saját domainre mutató) végpontnál a
     `.htaccess` CSP-jét ki kell egészíteni: `connect-src 'self' <domain>`. */
  endpoint: "api/dontestamogato",

  /* Az adatkezelési tájékoztató útvonala — a hozzájárulás mellett jelenik meg. */
  adatkezelesUrl: "adatkezelesi-tajekoztato"
};
