/* =============================================================================
   ÖkoTech Home — Test2 · urlap-ellenorzes.js
   Élő űrlapellenőrzés — progressive enhancement
   -----------------------------------------------------------------------------
   MIT CSINÁL. Kitöltés közben ellenőrzi a mezőket, a hibát PIROS BUBORÉKBAN
   mondja el a mező alatt, és a beküldő gombot addig „inaktívan" tartja, amíg
   valami hiányzik — a nyilatkozatokat is beleértve.

   MIT NEM CSINÁL. Nem helyettesíti a szerveroldali ellenőrzést: a kliens
   megkerülhető, a döntést a végpont hozza (api/*.php). Ez a réteg a KITÖLTŐNEK
   szól, nem a védelemnek.

   HÁROM DÖNTÉS, AMI NEM MAGÁTÓL ÉRTETŐDŐ:

   1. A GOMB NEM `disabled`, HANEM `aria-disabled`. A letiltott gomb néma
      zsákutca: nem fókuszálható, a képernyőolvasó átugorja, és a látogató nem
      tudja meg, mi hiányzik. Így viszont megnyomható — és a megnyomás
      MEGMUTATJA az összes hiányt, és odaugrik az elsőhöz.

   2. HIBÁT CSAK „ÉRINTETT" MEZŐN MUTATUNK. Az üres űrlap nem hibás, csak
      kitöltetlen: piros mezőkkel fogadni a látogatót ellenséges. A mező akkor
      válik érintetté, ha elhagyta (`blur`), vagy ha megnyomta a gombot.

   3. A HIBAÜZENET MAGYARUL, KONKRÉTAN. A böngésző saját üzenete („Please fill
      out this field") angol is lehet, és semmit nem mond arról, mit várunk.
   ============================================================================= */

(() => {
  'use strict';

  const urlapok = document.querySelectorAll('[data-urlap]');
  if (!urlapok.length) return;

  /* --------------------------------------------------------- egyedi szabályok */
  /* A `data-ellenoriz` attribútum választ közülük. Mindegyik ÜRES értéknél
     rendben van: a kötelezőséget a `required` intézi, nem ez. */
  const SZABALYOK = {
    /* ADÓSZÁM — 8 számjegy + áfakód (1–5) + megyekód. Az ellenőrzőszám a NAV
       algoritmusa szerint: az első hét számjegy 9,7,3,1,9,7,3 súllyal, az
       összeg tízes kiegészítője a nyolcadik. Így az elgépelt szám már itt
       kiderül, nem a számlázásnál. */
    adoszam: (ertek) => {
      const t = ertek.replace(/[\s-]/g, '');
      if (!/^\d{11}$/.test(t)) {
        return 'Az adószám 11 számjegy: nyolc számjegy, az áfakód és a megyekód — például 12345678-2-11.';
      }
      const afa = Number(t[8]);
      if (afa < 1 || afa > 5) return 'Az adószám kilencedik jegye (áfakód) 1 és 5 közötti szám.';
      const sulyok = [9, 7, 3, 1, 9, 7, 3];
      let osszeg = 0;
      for (let i = 0; i < 7; i++) osszeg += Number(t[i]) * sulyok[i];
      const ellenorzo = (10 - (osszeg % 10)) % 10;
      if (ellenorzo !== Number(t[7])) {
        return 'Az adószám ellenőrzőszáma nem stimmel — kérjük, nézze meg újra a nyolcadik számjegyet.';
      }
      return '';
    },

    /* TELEFON — nem formátumot írunk elő (a +36, a 06 és a szóközös alak is
       helyes), csak azt nézzük, van-e benne elég számjegy ahhoz, hogy
       visszahívható legyen. */
    telefon: (ertek) => {
      const szamok = ertek.replace(/\D/g, '');
      if (szamok.length < 9) return 'A telefonszám túl rövidnek tűnik — például +36 30 123 4567.';
      if (szamok.length > 14) return 'A telefonszám túl hosszú — ellenőrizze, nem került-e bele fölösleges karakter.';
      return '';
    },

    /* IRÁNYÍTÓSZÁM — magyar: négy számjegy, nem kezdődhet nullával. */
    iranyitoszam: (ertek) => (/^[1-9]\d{3}$/.test(ertek.trim())
      ? '' : 'A magyar irányítószám négy számjegy, például 2500.'),
  };

  /* A böngésző saját hibáit magyarra fordítjuk, és megmondjuk, mit várunk. */
  /* A MEZŐ NEVE a hibaüzenetbe: a címke szövege, DE a csillag és a súgógomb
     nélkül. Szövegcserével ez nem megbízható (a súgó szövege is a címkében ül),
     ezért a címke másolatából kivesszük a nem odavaló elemeket, és úgy olvassuk
     ki — így nem kerül a mondatba se a `*`, se a „Súgó: …". */
  const cimkeSzoveg = (mezo) => {
    const cimke = mezo.labels && mezo.labels[0];
    if (!cimke) return 'A mező';
    const masolat = cimke.cloneNode(true);
    masolat.querySelectorAll('.sugo,[aria-hidden="true"],.visually-hidden').forEach((e) => e.remove());
    return masolat.textContent.replace(/\s+/g, ' ').trim() || 'A mező';
  };

  const uzenet = (mezo) => {
    const v = mezo.validity;
    const cimke = cimkeSzoveg(mezo);

    if (v.valueMissing) {
      if (mezo.type === 'checkbox') return 'Ehhez a nyilatkozathoz a jelölés szükséges.';
      if (mezo.type === 'radio')    return 'Kérjük, válasszon a lehetőségek közül.';
      if (mezo.type === 'file')     return 'Kérjük, válasszon fájlt.';
      return `A(z) „${cimke}" kitöltése kötelező.`;
    }
    if (v.typeMismatch && mezo.type === 'email') {
      return 'Ez nem tűnik érvényes e-mail-címnek — a @ jel és a domain is kell hozzá.';
    }
    if (v.rangeUnderflow) return `A legkisebb megadható érték ${mezo.min}.`;
    if (v.rangeOverflow)  return `A legnagyobb megadható érték ${mezo.max}.`;
    if (v.stepMismatch)   return 'Egész számot adjon meg.';
    if (v.tooShort)       return `Legalább ${mezo.minLength} karakter szükséges.`;
    if (v.tooLong)        return `Legfeljebb ${mezo.maxLength} karakter adható meg.`;
    if (v.badInput && mezo.type === 'number') return 'Itt számot várunk.';
    if (v.badInput && mezo.type === 'date')   return 'Kérjük, adjon meg érvényes dátumot.';
    if (v.patternMismatch || v.customError)   return mezo.validationMessage;
    return mezo.validationMessage || 'Ezt az értéket nem tudjuk elfogadni.';
  };

  urlapok.forEach((urlap) => {
    const gomb = urlap.querySelector('button[type="submit"]');
    if (!gomb) return;

    const mezok = () => Array.from(urlap.elements).filter((m) =>
      m.name && !m.disabled && m.type !== 'submit' && m.type !== 'button'
      && m.type !== 'hidden' && !m.closest('.urlap-csapda'));

    /* A rádiócsoportból csak az ELSŐ kap hibaüzenetet — különben ugyanaz a
       mondat háromszor jelenne meg egymás alatt. */
    const elsoACsoportban = (m) => m.type !== 'radio'
      || urlap.querySelectorAll(`[name="${CSS.escape(m.name)}"]`)[0] === m;

    const hibaHelye = (m) => {
      if (m.type === 'checkbox' || m.type === 'radio') {
        return m.closest('.urlap-jelolo') || m.closest('.dok-valasztek') || m.closest('.urlap-mezo');
      }
      return m.closest('.urlap-mezo') || m.parentElement;
    };

    const egyediHiba = (m) => {
      /* A FÁJLMEZŐ HIBÁJA MÁSHONNAN JÖN. A mellékletmodul (`urlap-fajl.js`)
         állapítja meg — darabszám, méret —, ez a réteg csak VISSZAÍRJA.
         Enélkül a következő billentyűleütés `setCustomValidity('')`-vel némán
         letörölné, a gomb kizöldülne, és a túl nagy melléklet elindulna. */
      if (m.type === 'file') return m.dataset.fajlHiba || '';
      const szabaly = SZABALYOK[m.dataset.ellenoriz];
      if (!szabaly || !m.value.trim()) return '';
      return szabaly(m.value);
    };

    const hibaMutat = (m, szoveg) => {
      const hely = hibaHelye(m);
      if (!hely) return;
      let doboz = hely.querySelector(':scope > .urlap-hiba');
      if (!szoveg) {
        if (doboz) doboz.remove();
        m.removeAttribute('aria-invalid');
        if (m.getAttribute('aria-describedby') === doboz?.id) m.removeAttribute('aria-describedby');
        hely.classList.remove('is-hibas');
        return;
      }
      if (!doboz) {
        doboz = document.createElement('span');
        doboz.className = 'urlap-hiba type-ui-caption';
        doboz.id = 'hiba-' + (m.id || m.name).replace(/[^\w-]/g, '') + '-' + Math.random().toString(36).slice(2, 6);
        doboz.setAttribute('role', 'alert');
        hely.append(doboz);
      }
      doboz.textContent = szoveg;
      m.setAttribute('aria-invalid', 'true');
      m.setAttribute('aria-describedby', doboz.id);
      hely.classList.add('is-hibas');
    };

    /* Egy mező kiértékelése. `mutat`: kiírjuk-e a hibát, vagy csak számolunk. */
    const ellenoriz = (m, mutat) => {
      const egyedi = egyediHiba(m);
      m.setCustomValidity(egyedi);
      const rendben = m.checkValidity();
      /* A fájlmező nem kap buborékot: a baj a MELLÉKLETLISTÁBAN áll, a fájl
         mellett, amelyikre vonatkozik — a buborék ugyanazt mondaná el
         másodszor, a lista fölött lebegve. */
      if (mutat && elsoACsoportban(m) && m.type !== 'file') hibaMutat(m, rendben ? '' : uzenet(m));
      return rendben;
    };

    const allapot = () => {
      const kesz = mezok().every((m) => ellenoriz(m, m.dataset.erintett === '1'));
      gomb.setAttribute('aria-disabled', kesz ? 'false' : 'true');
      if (jelzo) {
        jelzo.textContent = kesz
          ? 'Minden kötelező mező kész.'
          : 'A beküldéshez még hiányzik valami a jelölt mezőkből.';
        if (kesz) jelzo.setAttribute('data-kesz', ''); else jelzo.removeAttribute('data-kesz');
      }
      return kesz;
    };

    /* Állapotjelző a gomb mellé — a látogatónak tudnia kell, MIÉRT nem aktív. */
    const jelzo = document.createElement('span');
    jelzo.className = 'type-ui-caption urlap-hianyzik';
    jelzo.setAttribute('aria-live', 'polite');
    (urlap.querySelector('.urlap-akcio') || gomb.parentElement).append(jelzo);

    urlap.addEventListener('input', (e) => {
      const m = e.target;
      if (m.dataset.erintett === '1') ellenoriz(m, true);
      allapot();
    });

    urlap.addEventListener('change', (e) => {
      e.target.dataset.erintett = '1';
      ellenoriz(e.target, true);
      allapot();
    });

    urlap.addEventListener('focusout', (e) => {
      const m = e.target;
      if (!m.name || m.type === 'submit') return;
      m.dataset.erintett = '1';
      ellenoriz(m, true);
      allapot();
    });

    /* A gomb megnyomása hiányos űrlapon: MEGMUTATJA a hiányokat, és odaugrik az
       elsőhöz — nem történik „semmi", ami a leggyakoribb űrlapzsákutca. */
    gomb.addEventListener('click', (e) => {
      if (gomb.getAttribute('aria-disabled') !== 'true') return;
      e.preventDefault();
      mezok().forEach((m) => { m.dataset.erintett = '1'; });
      allapot();
      const elso = mezok().find((m) => !m.checkValidity());
      if (elso) {
        (hibaHelye(elso) || elso).scrollIntoView({ behavior: 'smooth', block: 'center' });
        elso.focus({ preventScroll: true });
      }
    });

    /* Sikeres beküldés után az űrlap kiürül: a hibák és a jelölések is. */
    urlap.addEventListener('reset', () => {
      window.setTimeout(() => {
        urlap.querySelectorAll('.urlap-hiba').forEach((d) => d.remove());
        urlap.querySelectorAll('[aria-invalid]').forEach((m) => m.removeAttribute('aria-invalid'));
        mezok().forEach((m) => { delete m.dataset.erintett; m.setCustomValidity(''); });
        allapot();
      }, 0);
    });

    allapot();
  });
})();
