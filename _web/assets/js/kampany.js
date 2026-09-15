/* kampany.js — honnan érkezett a látogató, az űrlap rejtett mezőibe.
   ---------------------------------------------------------------------------
   MIT OLD MEG. A CRM-nek tudnia kell, melyik hirdetés vagy melyik ajánló hozta
   a megkeresést. A hirdetés az érkezési URL-ben adja meg magát (`utm_*`), az
   ajánló egy saját paraméterben — de a látogató ritkán ott kér ajánlatot, ahol
   belépett: olvas két-három lapot, és csak utána tölti ki az űrlapot. Addigra
   az eredeti URL-paraméterek eltűntek a címsorból.

   EZÉRT TÁROLJUK. Az ELSŐ érkezés paraméterei kerülnek el a munkamenet
   tárolójába, és onnan másolódnak be az űrlap rejtett mezőibe, bármelyik lapon
   küldi is el. Aki egy hirdetésre kattintott, ugyanahhoz a hirdetéshez tartozik
   három lappal később is.

   MIÉRT NEM A `document.referrer`-BŐL. A második kattintás után a referrer már
   a SAJÁT lapunk — a hirdetés nyoma elveszne. Az `utm_*` viszont a belépéskor
   egyszer, biztosan ott van.

   MIÉRT `sessionStorage` ÉS NEM `localStorage`. A munkamenet végén magától
   elmúlik. Nem tartós azonosító, nem követi a látogatót napokon át, és nem
   alkalmas profilalkotásra — csak addig él, amíg az a látogatás tart. Ami
   benne van, azt a látogató maga hozta magával az URL-ben; új információt nem
   gyűjtünk róla. A tartós, hónapokig élő attribúció ennél jóval többet
   állítana a látogatóról, és külön hozzájárulást kívánna.

   AMI NEM KERÜL BELE: semmilyen személyes adat. Csak a hirdetési címkék
   (`utm_source`, `utm_campaign`, …) és az ajánló azonosítója — olyan értékek,
   amelyeket mi magunk tettünk a hivatkozásba.
*/
(() => {
  'use strict';

  const KULCS = 'oth-kampany';

  /* Az ajánlói azonosító TÖBB NÉVEN érkezhet. A hirdetéskezelők és a partnerek
     nem ugyanazt a paramétert használják, és egy elgépelt paraméternév néma
     adatvesztés — a beküldés átmegy, csak épp nem tudni, ki hozta. */
  const AJANLO_NEVEK = ['ref', 'partner', 'ajanlo', 'partner_azon'];

  /** A munkamenet tárolója privát ablakban és letiltott tárolásnál dobhat. A
      kampányjelölés nem kritikus: hiba esetén üresen megy az űrlap. */
  const olvas = () => {
    try {
      return JSON.parse(sessionStorage.getItem(KULCS) || 'null');
    } catch {
      return null;
    }
  };

  const ir = (ertek) => {
    try {
      sessionStorage.setItem(KULCS, JSON.stringify(ertek));
    } catch {
      /* nem tároljuk — ezen a lapon még így is működik */
    }
  };

  /**
   * Az AKTUÁLIS URL paramétereiből épít jelölést, vagy `null`-t ad, ha egy sincs.
   *
   * A `kampany_azonosito` a kampány neve, de ha az hiányzik, a `utm_medium` és
   * a `utm_content` is használható — jobb egy részleges jelölés, mint semmi.
   */
  const urlbol = () => {
    const p = new URLSearchParams(window.location.search);
    const utm = (n) => (p.get('utm_' + n) || '').trim().slice(0, 120);

    const tipus = utm('source');
    const azonosito = utm('campaign') || utm('medium') || utm('content');

    let partner = '';
    for (const n of AJANLO_NEVEK) {
      const v = (p.get(n) || '').trim().slice(0, 120);
      if (v) { partner = v; break; }
    }

    if (!tipus && !azonosito && !partner) return null;

    return { tipus, azonosito, partner };
  };

  /* AZ ELSŐ JELÖLÉS NYER, nem az utolsó. Ha a látogató a munkamenet közben
     még egyszer rákattint egy másik hirdetésre, az elsőt nem írjuk felül: azt
     az utat kezdte el, amelyik idehozta. Ez az „első érintés" attribúció —
     egyértelmű szabály, és nem függ attól, hányszor navigál oda-vissza. */
  let jeloles = olvas();
  if (!jeloles) {
    jeloles = urlbol();
    if (jeloles) ir(jeloles);
  }

  if (!jeloles) return;

  /* A rejtett mezők a `data-kampany` attribútumról ismerhetők fel, nem a
     `name`-ről: a CRM mezőnevei változhatnak, a jelölés szerepe nem. */
  const tolt = () => {
    document.querySelectorAll('input[data-kampany]').forEach((mezo) => {
      const szerep = mezo.dataset.kampany;
      if (szerep in jeloles && jeloles[szerep]) {
        mezo.value = jeloles[szerep];
      }
    });
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', tolt, { once: true });
  } else {
    tolt();
  }
})();
