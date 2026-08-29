/* ============================================================================
   ÖkoTech Home — ugy.js
   Az AI-modulok KÖZÖS ügykezelése: azonosító, mentés, átadás a modulok között.
   ----------------------------------------------------------------------------
   EGY AZONOSÍTÓ, TÖBB MODUL. A látogató a 6. szekcióban (megoldás-ajánló) kap
   egy `MA-XXXX-XXXX` kódot. A 8. szekció (ársávbecslő) UGYANEZT az ügyet
   egészíti ki, nem újat nyit — így a `/eredmeny?id=…` lapon a teljes út együtt
   látszik, a második modul nem kérdezi újra, amit az első már megtudott, és a
   CRM egyetlen rekordból dolgozhat.

   MIÉRT KÜLÖN FÁJL. Három helyről kell ugyanez: a 6. szekció modulja, a 8.
   szekció modulja és az `/eredmeny` lap. Ha mindhárom saját `fetch`-et írna, a
   végpont neve, a hibakezelés és a tárolókulcs három helyen csúszhatna szét.

   AMI A BÖNGÉSZŐBEN MARAD. A `sessionStorage` csak az AZONOSÍTÓT és a GÉPI
   VÁLASZKULCSOKAT tartja — annyit, amennyi a következő modul előkitöltéséhez
   kell. Fül bezárásakor eltűnik. Személyes adat itt sincs.
   ========================================================================== */
(() => {
  'use strict';

  /* A végpontok útvonala. Nem szakmai adat, ezért nem a cég szerkesztette
     konfigban él, hanem itt — egy helyen, mindhárom hívó számára. */
  const VEGPONT_MENTES = 'api/eredmeny-mentes';
  const VEGPONT_OLVAS  = 'api/eredmeny-olvas';
  const EREDMENY_LAP   = 'eredmeny';
  const TAR_KULCS      = 'oth-ugy';
  const ALAK           = /^MA-[A-Z2-9]{4}-[A-Z2-9]{4}$/;

  /** A lap gyökeréhez képest abszolút cím — aloldalról is helyes marad. */
  const alap = () => location.origin + location.pathname.replace(/[^/]*$/, '');

  /* ------------------------------------------------------- BÖNGÉSZŐTÁROLÓ */
  /* A `sessionStorage` privát ablakban és letiltott sütiknél dobhat. Az ügy
     nem működés-kritikus: ha nem tudjuk eltenni, a modul egyszerűen újra
     megkérdezi, amit kell. */
  function olvasTar() {
    try {
      const n = sessionStorage.getItem(TAR_KULCS);
      const o = n ? JSON.parse(n) : null;
      return (o && typeof o === 'object') ? o : null;
    } catch (_) { return null; }
  }

  function irTar(o) {
    try { sessionStorage.setItem(TAR_KULCS, JSON.stringify(o)); } catch (_) { /* nem baj */ }
    /* A két modul EGY lapon él, egymás alatt. A 8. szekció átvételi sávja a
       lap betöltésekor épül fel — akkor még nincs mit átvenni. Ez az esemény
       szól neki, amikor a 6. szekció végzett; így a látogatónak nem kell
       frissítenie a lapot ahhoz, hogy a felajánlás megjelenjen. */
    try { window.dispatchEvent(new CustomEvent('oth-ugy-valtozott', { detail: o })); } catch (_) { /* régi böngésző */ }
  }

  /** A modul válaszkulcsainak és az azonosítónak az eltétele a következő modulnak. */
  function jegyez(modul, valaszKulcsok, azonosito) {
    const o = olvasTar() || { modulok: {} };
    if (!o.modulok) o.modulok = {};
    if (azonosito && ALAK.test(azonosito)) o.azonosito = azonosito;
    if (modul && valaszKulcsok) o.modulok[modul] = valaszKulcsok;
    irTar(o);
    return o;
  }

  /**
   * FÜGGŐBEN lévő modul-kimenet: lefutott, de a látogató (még) nem mentette el.
   *
   * MIÉRT KELL. A látogató végigmehet a megoldás-ajánlón mentés nélkül, aztán
   * az ársávbecslőn — és OTT nyomhat mentést. Ilyenkor a két modul kimenete
   * egy ügybe tartozik, csak a sorrend fordított. Enélkül az ügy féloldalas
   * volna: benne az ársáv, nélküle az, ami odáig vezetett.
   *
   * A munkamenetben él, tehát a fül bezárásával eltűnik. Semmit nem küld el
   * magától: csak akkor kerül szerverre, ha a látogató MENT.
   */
  function fuggoben(modul, csomag) {
    const o = olvasTar() || { modulok: {} };
    if (!o.fuggoben) o.fuggoben = {};
    o.fuggoben[modul] = csomag;
    irTar(o);
  }

  /** Van-e olyan lefutott modul, ami mentéskor magától az ügybe kerülne? */
  function fuggoModulok(kiveve) {
    const o = olvasTar();
    if (!o || !o.fuggoben || o.azonosito) return [];
    return Object.keys(o.fuggoben).filter((m) => m !== kiveve);
  }

  /* --------------------------------------------------------------- HÁLÓZAT */

  /** Egységes válaszolvasás: a nem-JSON válasz is kezelt eset. */
  async function hivas(vegpont, csomag) {
    let v;
    try {
      v = await fetch(vegpont, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(csomag)
      });
    } catch (_) {
      return { ok: false, uzenet: '' };
    }
    let adat = null;
    /* Helyi előnézetben (statikus kiszolgáló) a PHP nem fut le: nyers forrás
       vagy hibalap érkezik, nem JSON. Ez nem kivétel, hanem várt eset. */
    try { adat = await v.json(); } catch (_) { adat = null; }
    if (!v.ok || !adat || !adat.ok) {
      return { ok: false, uzenet: (adat && adat.uzenet) ? adat.uzenet : '' };
    }
    return adat;
  }

  /**
   * Modul kimenetének mentése. Ha a munkamenetben már van azonosító, azt az
   * ÜGYET egészíti ki; különben újat nyit.
   * @returns {Promise<{ok:boolean, azonosito?:string, uj?:boolean, uzenet?:string}>}
   */
  async function ment(modul, csomag) {
    let tar = olvasTar() || {};

    /* ELŐBB A FÜGGŐBEN LÉVŐ MODULOK. Ha a látogató végigment az egyik modulon
       mentés nélkül, és a másikat menti el, mindkettő EGY ügybe kerül — az
       elsőt itt küldjük fel, és a keletkező azonosítót adjuk tovább. */
    if (!tar.azonosito && tar.fuggoben) {
      const varok = Object.keys(tar.fuggoben).filter((m) => m !== modul);
      for (let i = 0; i < varok.length; i++) {
        const m = varok[i];
        const v = await hivas(VEGPONT_MENTES, Object.assign(
          { modul: m, azonosito: (olvasTar() || {}).azonosito || '' }, tar.fuggoben[m]));
        if (v.ok) { jegyez(m, tar.fuggoben[m].valaszKulcsok, v.azonosito); }
      }
      tar = olvasTar() || {};
    }

    const valasz = await hivas(VEGPONT_MENTES, Object.assign({
      modul: modul,
      azonosito: tar.azonosito || ''
    }, csomag));
    if (valasz.ok) {
      jegyez(modul, csomag.valaszKulcsok, valasz.azonosito);
      /* A felküldött függőben lévők már az ügyben vannak. */
      const o = olvasTar() || {};
      delete o.fuggoben;
      irTar(o);
    }
    return valasz;
  }

  /** Mentett ügy visszaolvasása azonosító alapján. */
  async function olvas(id) {
    const azon = String(id || '').trim().toUpperCase();
    if (!ALAK.test(azon)) return { ok: false, uzenet: 'Az azonosító alakja nem megfelelő. A helyes alak: MA-XXXX-XXXX.' };
    const valasz = await hivas(VEGPONT_OLVAS, { id: azon });
    if (valasz.ok && valasz.ugy) {
      /* A visszaolvasott ügy válaszkulcsai innentől a munkamenetben is
         elérhetők — a másik modul ebből tölt elő. */
      const o = { azonosito: valasz.ugy.azonosito, modulok: {} };
      Object.keys(valasz.ugy.modulok || {}).forEach((m) => {
        const b = valasz.ugy.modulok[m];
        if (b && b.valaszKulcsok) o.modulok[m] = b.valaszKulcsok;
      });
      irTar(o);
    }
    return valasz;
  }

  window.OthUgy = {
    ALAK: ALAK,
    eredmenyUrl: (azon) => alap() + EREDMENY_LAP + '?id=' + encodeURIComponent(azon),
    eredmenyHref: (azon) => EREDMENY_LAP + '?id=' + encodeURIComponent(azon),
    allapot: olvasTar,
    /** Egy korábbi modul gépi válaszkulcsai, ha vannak. */
    valaszkulcsok: (modul) => {
      const o = olvasTar();
      return (o && o.modulok && o.modulok[modul]) ? o.modulok[modul] : null;
    },
    jegyez: jegyez,
    fuggoben: fuggoben,
    fuggoModulok: fuggoModulok,
    ment: ment,
    olvas: olvas
  };
})();
