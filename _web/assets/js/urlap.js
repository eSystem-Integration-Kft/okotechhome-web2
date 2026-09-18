/* =============================================================================
   ÖkoTech Home — Produktív · urlap.js
   Űrlapbeküldés oldalfrissítés nélkül — progressive enhancement
   -----------------------------------------------------------------------------
   Az űrlap JS NÉLKÜL is teljes értékű: sima POST megy a végpontra. Ez a fájl
   annyit tesz, hogy elfogja a beküldést, és a választ helyben jeleníti meg —
   így a látogató nem veszíti el a kitöltött oldalt, és a hibás mezőhöz vissza
   tud lépni.

   Amit szándékosan NEM csinál: nem validál a szerver helyett. A böngésző
   natív ellenőrzése (`required`, `type="email"`) segít, de a döntést a
   végpont hozza — a kliensoldali ellenőrzés megkerülhető.
   ============================================================================= */

(() => {
  'use strict';

  const urlapok = document.querySelectorAll('[data-urlap]');
  if (!urlapok.length) return;

  urlapok.forEach((urlap) => {
    /* A megnyitás időpontja: a végpont ebből látja, ha valaki 3 másodperc
       alatt „töltötte ki" az űrlapot. A mező JS nélkül üres marad, és a
       szerver akkor egyszerűen nem alkalmazza ezt a szűrőt. */
    const ido = urlap.querySelector('[data-urlap-ido]');
    if (ido) ido.value = String(Math.floor(Date.now() / 1000));

    /*
     * A KORÁBBI ÜGY AZONOSÍTÓJA — MINDEN ŰRLAPHOZ, EGY HELYEN.
     *
     * Ha a látogató korábban kitöltötte az ársávbecslőt vagy a
     * megoldás-ajánlót és el is mentette, ez a kód összeköti a mostani, NÉVVEL
     * érkező megkeresést a korábbi névtelen válaszaival. Az értékesítő így már
     * a hívás előtt tudja, mekkora házról, milyen jelenlegi megoldásról és
     * milyen ársávról van szó — anélkül, hogy a látogatónak bármit meg kellett
     * volna ismételnie.
     *
     * ITT, ÉS NEM ŰRLAPONKÉNT. Minden űrlap ezen a kezelőn megy át; ha
     * egyesével kellene beírni, a következő űrlapnál elmaradna — és a hiány
     * néma: a megkeresés attól még megérkezik, csak épp előzmény nélkül.
     *
     * Ha nincs mentett ügy, a mező nem jön létre: üres értéket küldeni
     * ugyanaz, mint nem küldeni, de a kérésben zajt jelentene.
     */
    try {
      const ugy = window.OthUgy && window.OthUgy.allapot ? window.OthUgy.allapot() : null;
      const azon = ugy && ugy.azonosito ? ugy.azonosito : '';

      if (azon && !urlap.querySelector('[name="ugy_azonosito"]')) {
        const rejtett = document.createElement('input');
        rejtett.type = 'hidden';
        rejtett.name = 'ugy_azonosito';
        rejtett.value = azon;
        urlap.appendChild(rejtett);
      }
    } catch (hiba) {
      /* Az ügytár hiánya nem akadályozhatja meg a beküldést: a megkeresés
         előzmény nélkül is teljes értékű. */
    }

    /* ================= KÖSZÖNŐABLAK =========================================
       MIÉRT ABLAK, ÉS NEM CSAK A ZÖLD SOR. A beküldés a látogató részéről
       befejezett munka — tizenöt mezőt töltött ki. Egy sor szöveg az űrlap
       alatt ezt nem zárja le: a lap ugyanúgy néz ki, mint előtte, a kiürült
       mezőkkel, és nem derül ki, mi következik. Az elmosott háttér kimondja,
       hogy ez a szakasz véget ért.

       A ZÖLD SOR MARAD. Ez a réteg rá ÉPÜL, nem helyette van: `<dialog>`
       nélküli böngészőben, vagy ha bármi elszáll a felépítés közben, a
       visszaigazolás akkor is ott áll az űrlap alatt. A megerősítés nem
       múlhat egy díszen.

       ŰRLAPONKÉNT MÁS A FOLYTATÁS. Aki ajánlatot kért, két munkanapig vár —
       neki az összehasonlítás és a referenciák valók. Aki megrendelt, annak a
       telepítés és az üzemeltetés. Általános „nézzen körül" helyett azt
       ajánljuk, ami az ő helyzetében következik.

       MINDEN HIVATKOZÁS ELLENŐRZÖTT: halott link nem kerülhet ide. */
    const KOSZONO = {
      oth_ajanlatkeres: {
        cim: 'Köszönjük az ajánlatkérését!',
        alcim: 'Átnézzük az adatokat, és két munkanapon belül küldjük a tételes '
             + 'ajánlatot. Ha valami hiányzik a méretezéshez, előbb rákérdezünk.',
        linkek: [
          ['megoldasok/megoldastipusok-osszehasonlitasa', 'Megoldások összehasonlítása',
           'Mi a különbség a három technológia között, és melyiknek mik a feltételei.'],
          ['eredmenyek/esettanulmanyok', 'Esettanulmányok',
           'Megvalósult rendszerek — telekadatokkal, terheléssel, tapasztalatokkal.'],
          ['tudastar/uzemeltetes-teendok-es-koltsegek', 'Üzemeltetés és költségek',
           'Mivel jár egy berendezés éves szinten. Érdemes az ajánlat mellé olvasni.'],
        ],
      },
      oth_megrendeles: {
        cim: 'Köszönjük a megrendelését!',
        alcim: 'Munkatársunk ellenőrzi, és külön levélben visszaigazolja — '
             + 'a szerződés ezzel jön létre.',
        linkek: [
          ['tudastar/telepites-lepesrol-lepesre', 'Telepítés lépésről lépésre',
           'Mi történik a helyszínen, és mire érdemes előre felkészülni.'],
          ['tudastar/uzemeltetes-teendok-es-koltsegek', 'Üzemeltetés és költségek',
           'A rendszeres teendők és a valós éves költség.'],
        ],
      },
      oth_konzultacio: {
        cim: 'Köszönjük a konzultációkérését!',
        alcim: 'Az időpontot külön visszaigazoljuk.',
        linkek: [
          ['helyzetem/', 'Kiindulópont', 'Válassza ki a helyzetét, és nézze meg, mi jöhet szóba.'],
          ['tudastar/', 'Tudástár', 'Technológia, engedélyezés, méretezés — érthetően.'],
        ],
      },
    };
    const KOSZONO_ALAP = {
      cim: 'Köszönjük a megkeresését!',
      alcim: 'Megkaptuk, és hamarosan jelentkezünk.',
      linkek: [
        ['tudastar/', 'Tudástár', 'Technológia, engedélyezés, méretezés — érthetően.'],
        ['eredmenyek/', 'Eredmények', 'Megvalósult rendszerek és tanúsítványok.'],
      ],
    };

    /** A gyökérhez képesti útvonal a lap MÉLYSÉGE szerint. Az űrlapok
        `action`-je is relatív (`api/ajanlat`), ebből olvassuk ki az előtagot —
        így a hírcikkek két szint mély lapjain is jó helyre mutat. */
    const eloTag = () => {
      const a = urlap.getAttribute('action') || '';
      const m = a.match(/^((?:\.\.\/)*)/);
      return m ? m[1] : '';
    };

    const koszonoAblak = (uzenet) => {
      if (typeof HTMLDialogElement === 'undefined') return;   // régi böngésző: marad a zöld sor
      const k = KOSZONO[urlap.dataset.meres] || KOSZONO_ALAP;
      const p = eloTag();

      const d = document.createElement('dialog');
      d.className = 'koszono';
      d.setAttribute('aria-labelledby', 'koszono-cim');

      const belso = document.createElement('div');
      belso.className = 'koszono-belso';

      const logo = document.createElement('img');
      logo.className = 'koszono-logo';
      logo.src = p + 'assets/img/logo-okotechhome.svg';
      logo.alt = 'ÖkoTech Home';
      /* A méret a jelölésben is ott van: kép nélküli pillanatban sem ugrik
         meg az elrendezés. */
      logo.width = 128; logo.height = 32;
      belso.append(logo);

      const cim = document.createElement('h2');
      cim.className = 'type-display-section-title koszono-cim';
      cim.id = 'koszono-cim';
      cim.textContent = k.cim;
      belso.append(cim);

      const alcim = document.createElement('p');
      alcim.className = 'type-ui-body koszono-szoveg';
      /* A SZERVER ÜZENETE NYER, ha van: az tartalmazhat olyat, amit csak a
         végpont tud — például a megrendelés azonosítóját. */
      alcim.textContent = uzenet || k.alcim;
      belso.append(alcim);

      if (k.linkek.length) {
        const cimke = document.createElement('p');
        cimke.className = 'type-data-eyebrow koszono-tovabb-cim';
        cimke.textContent = 'Amíg válaszolunk';
        belso.append(cimke);

        const lista = document.createElement('ul');
        lista.className = 'koszono-tovabb';
        lista.setAttribute('role', 'list');
        k.linkek.forEach(([ut, nev, leiras]) => {
          const li = document.createElement('li');
          const a = document.createElement('a');
          a.className = 'koszono-link';
          a.href = p + ut;
          const b = document.createElement('b');
          b.className = 'type-ui-body-strong';
          b.textContent = nev;
          const sp = document.createElement('span');
          sp.className = 'type-ui-caption';
          sp.textContent = leiras;
          a.append(b, sp);
          li.append(a);
          lista.append(li);
        });
        belso.append(lista);
      }

      const zar = document.createElement('button');
      zar.type = 'button';
      zar.className = 'btn btn-secondary koszono-zar';
      zar.textContent = 'Bezárom';
      zar.addEventListener('click', () => d.close());
      belso.append(zar);

      d.append(belso);
      document.body.append(d);
      d.showModal();
      /* A bezárt ablak nem marad a DOM-ban: egy második beküldés sajátot épít. */
      d.addEventListener('close', () => d.remove());
    };
    /* ======================================================================= */

    const valasz = urlap.querySelector('[data-urlap-valasz]');
    const gomb = urlap.querySelector('button[type="submit"]');

    const jelez = (szoveg, allapot) => {
      if (!valasz) return;
      valasz.textContent = szoveg;
      if (allapot === 'hiba') valasz.setAttribute('data-allapot', 'hiba');
      else valasz.removeAttribute('data-allapot');
      valasz.hidden = false;
      valasz.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
    };

    const mezoHibak = (mezok) => {
      urlap.querySelectorAll('[aria-invalid]').forEach((m) => m.removeAttribute('aria-invalid'));
      if (!mezok) return;
      let elso = null;
      Object.keys(mezok).forEach((nev) => {
        const m = urlap.querySelector('[name="' + nev + '"]');
        if (!m) return;
        m.setAttribute('aria-invalid', 'true');
        if (!elso) elso = m;
      });
      if (elso) elso.focus();
    };

    /* ================= MÉRÉS =================================================
       A KONVERZIÓ A dataLayerBE MEGY, nem közvetlen mérőkódba. A GTM-en kívül
       szándékosan nincs Google- vagy Meta-hívás: két helyről mérve ugyanaz az
       esemény kétszer számolódna.

       MIÉRT ITT ÉS NEM A KÖSZÖNŐOLDALON. A régi webhelyen a konverzió a
       `/koszonooldal-*` lap megtekintésére sült el. Itt nincs köszönőoldal: az
       űrlap AJAX-szal küld, a látogató a helyén marad. A sikeres beküldés
       pillanata az egyetlen megbízható jel, és az itt van.

       A BŐVÍTETT EGYEZTETÉS MEZŐI A RESET ELŐTT KELLENEK. Lentebb `urlap.reset()`
       fut; ha utána olvasnánk ki az e-mailt és a telefont, üres sztringet
       kapnánk, és az enhanced conversion némán érték nélkül maradna. */
    const MERT = new WeakSet();   // űrlaponként egyszer, lásd lentebb

    const mezo = (nev) => {
      const m = urlap.querySelector('[name="' + nev + '"]');
      return m && m.value ? String(m.value).trim() : '';
    };

    const konverzio = () => {
      /* EGYSZER SÜLHET EL. A gomb sikeres küldés után tiltva marad, de a
         garanciát nem arra bízzuk: egy visszalépés, egy kettős kattintás vagy
         egy böngészőkiegészítő újraküldhetné az űrlapot. */
      if (MERT.has(urlap)) return;
      MERT.add(urlap);

      const esemeny = urlap.dataset.meres;      // pl. oth_ajanlatkeres
      if (!esemeny) return;                     // amelyik űrlapnál nincs, az nem mér

      /* Egységes alak, hogy az egyeztetés illeszkedni tudjon: kisbetűs e-mail,
         a telefonból csak a számjegyek és a vezető +. */
      const email = mezo('email').toLowerCase();
      const tel = (mezo('telefon') || mezo('megrendelo_telefon') || mezo('kapcsolattarto_telefonszama'))
        .replace(/[^\d+]/g, '');

      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({
        event: esemeny,
        oth_urlap: urlap.getAttribute('action') || '',
        oth_email: email || undefined,
        oth_telefon: tel || undefined,
      });

      /* ÉS KÖZVETLENÜL A GA4-NEK IS, ha nincs konténer.
         ---------------------------------------------------------------
         A fenti `dataLayer.push` a GTM-nek szól. A konténer 2026-09-15-én
         kivezetésre került, tehát ma SENKI nem olvassa azt a sort — az
         esemény ott helyben elveszne.

         A `meres.js` a közvetlen ág bekapcsolásakor kiteszi a
         `window.OthGa4Kozvetlen`-t. Ha ez megvan, a GA4 itt kapja meg az
         eseményt. Ha a konténer valaha visszatér, a kapcsoló kikerül, ez az
         ág elnémul, és a `dataLayer` sor veszi át — ugyanaz az esemény nem
         mehet ki kétszer.

         A dataLayer-push AKKOR IS MARAD, amikor nincs konténer: olcsó, és
         ez a szerződés a mérőeszköz felé. Aki holnap bekapcsol egy
         konténert, készen találja.

         SZEMÉLYES ADAT NEM MEGY A GA4-BE. Az e-mail és a telefon a
         dataLayerben marad, mert azt a bővített egyeztetéshez a Google Ads
         és a Meta címkéje használja — a GA4 felhasználói adatot nem fogad,
         és a beküldésünk sem tenné oda. */
      const ga4 = window.OthGa4Kozvetlen;
      if (ga4 && typeof window.gtag === 'function') {
        window.gtag('event', esemeny, {
          oth_urlap: urlap.getAttribute('action') || '',
          send_to: ga4,
        });
      }
    };
    /* ======================================================================= */

    urlap.addEventListener('submit', async (e) => {
      /* Ha a böngésző natív ellenőrzése megbukik, hagyjuk őt dolgozni. */
      if (!urlap.checkValidity()) return;

      e.preventDefault();
      if (gomb) { gomb.disabled = true; gomb.setAttribute('aria-busy', 'true'); }

      try {
        const res = await fetch(urlap.action, {
          method: 'POST',
          headers: { 'Accept': 'application/json' },
          body: new FormData(urlap),
        });
        const adat = await res.json().catch(() => ({}));

        if (res.ok && adat.ok) {
          mezoHibak(null);
          jelez(adat.uzenet || 'Köszönjük, megkaptuk.', 'ok');
          konverzio();          /* A RESET ELŐTT — lásd a fenti indoklást. */

          /* AZ ŰRLAP KÉSZ — ezt a jelölőt az `urlap-ellenorzes.js` is nézi.
             Nélküle a lenti `reset()` kiüríti a kötelező jelölőnégyzetet, az
             ellenőrző modul újraszámol, és a SIKERES beküldés zöld
             visszaigazolása alá odaírja, hogy „a beküldéshez még hiányzik
             valami" — pontosan akkor, amikor semmi sem hiányzik. */
          urlap.dataset.bekuldve = '1';

          urlap.reset();
          if (ido) ido.value = String(Math.floor(Date.now() / 1000));

          /* A GOMB TILTVA MARAD, DE NEM PÖRÖG TOVÁBB.
             A tiltás szándékos: a kétszeri beküldés ugyanazt a levelet küldené
             el újra. Az `aria-busy` viszont azt jelenti, hogy DOLGOZIK — a
             munka pedig kész. Rajta hagyva a gomb örökké pörgő várakozásnak
             látszik, és a látogató azt hiszi, lefagyott — a zöld visszaigazolás
             ellenére is. (Mérve: pontosan ez történt.) */
          if (gomb) { gomb.removeAttribute('aria-busy'); }

          /* A KÖSZÖNŐABLAK A LEGUTOLSÓ LÉPÉS, és külön védve.
             A beküldés ekkor már megtörtént, a levél elment, a zöld sor ott
             áll — ha az ablak felépítése bármiért elszáll (régi böngésző, egy
             hiányzó ikon, egy kiegészítő), az NEM ronthatja el a
             visszaigazolást. A látogató megerősítése nem múlhat egy díszen. */
          try { koszonoAblak(adat.uzenet); } catch (_) { /* marad a zöld sor */ }
          return;
        }
        mezoHibak(adat.mezok);
        jelez(adat.uzenet || 'A küldés most nem sikerült. Kérjük, próbálja újra.', 'hiba');
      } catch (_) {
        jelez('A küldés most nem sikerült — lehet, hogy megszakadt a kapcsolat. '
            + 'Próbálja újra, vagy hívjon minket: +36 33 200 211.', 'hiba');
      } finally {
        if (gomb && !urlap.querySelector('[data-urlap-valasz]:not([data-allapot])')) {
          gomb.disabled = false;
          gomb.removeAttribute('aria-busy');
        }
      }
    });
  });
})();
