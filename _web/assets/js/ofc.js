/* =============================================================================
   ÖkoTech Home — Test2 · ofc.js
   AI ajánlat-összehasonlító: fájlcsatolás és az összehasonlító tábla vezérlése
   -----------------------------------------------------------------------------
   A Test1-beli modul viselkedése változatlanul: három kártya (A/B/C), mindegyik
   dropzone-ra kattintva tallóz vagy behúzott fájlt fogad; csatolás után a fájl
   chipje látszik, a fejléc × visszaállítja az üres állapotot. A tábla üresen
   indul, és az „Ajánlatok összehasonlítása" gomb tölti ki — csak azoknak az
   ajánlatoknak az oszlopát, amelyekhez tényleg tartozik feltöltés.

   AZ ELEMZÉS VALÓDI. A gomb feltölti az ajánlatokat az api/ajanlat-elemzes
   végpontra, amely a dokumentumokból olvassa ki a cellák tartalmát. Az
   API-kulcs a szerveren marad, a böngésző sosem látja.

   AMIT A FELÜLET KÖTELEZŐEN KIÍR: az elemzés tájékoztató jellegű, és ahol
   „nincs adat" áll, ott a dokumentum nem tartalmazta az információt — ez NEM
   jelenti azt, hogy a szolgáltatás kimarad az ajánlatból. A különbségtétel a
   látogató szempontjából lényeges, ezért a szöveg a szerverről jön (egy helyen
   változik), és a tábla fölött mindig megjelenik.
   ============================================================================= */

(() => {
  'use strict';

  const cards = document.querySelectorAll('[data-ofc-card]');
  if (!cards.length) return;

  /* Csak ezek a formátumok mehetnek be — tallózásnál ÉS behúzásnál is.
     A szerveroldali ellenőrzést ez nem váltja ki, csak a felhasználót segíti. */
  const ALLOWED_EXT = ['pdf', 'docx', 'xlsx', 'png', 'jpg', 'jpeg'];
  const MAX_SIZE = 10 * 1024 * 1024;

  const extOf = (file) => (file.name.split('.').pop() || '').toLowerCase();

  const rejectReason = (file) => {
    if (!ALLOWED_EXT.includes(extOf(file))) {
      return 'Ezt a formátumot nem tudjuk kiolvasni. Engedélyezett: PDF, DOCX, XLSX, JPG, PNG. '
           + 'Régi .doc vagy .xls fájlt mentsen el PDF-ként, és úgy töltse fel.';
    }
    if (file.size > MAX_SIZE) return 'A fájl túl nagy (legfeljebb 10 MB).';
    return null;
  };

  const fmtSize = (b) => {
    if (b < 1024) return b + ' B';
    if (b < 1048576) return Math.round(b / 1024) + ' KB';
    return (b / 1048576).toFixed(1).replace('.', ',') + ' MB';
  };

  const CHECK = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>';

  /* ------------------------------------------------------------ fájl chipje */
  const makeChip = (file) => {
    const chip = document.createElement('div');
    chip.className = 'ofc-file';

    const ic = document.createElement('span');
    ic.className = 'ofc-file-ic';
    ic.textContent = (extOf(file) || 'fájl').toUpperCase().slice(0, 4);

    const meta = document.createElement('div');
    meta.className = 'ofc-file-meta';
    const name = document.createElement('b');
    name.className = 'ofc-file-name type-ui-subtitle';
    name.textContent = file.name;
    const size = document.createElement('span');
    size.className = 'ofc-file-size type-ui-caption';
    size.textContent = fmtSize(file.size);
    meta.append(name, size);

    const ok = document.createElement('span');
    ok.className = 'ofc-file-ok';
    ok.innerHTML = CHECK;

    chip.append(ic, meta, ok);
    return chip;
  };

  const showFile = (card, file) => {
    const slot = card.querySelector('[data-ofc-slot]');
    const drop = slot.querySelector('[data-ofc-drop]');
    const existing = slot.querySelector('.ofc-file');
    if (existing) existing.remove();
    drop.hidden = true;
    slot.insertBefore(makeChip(file), drop);
  };

  const showError = (card, msg) => {
    const slot = card.querySelector('[data-ofc-slot]');
    const drop = slot.querySelector('[data-ofc-drop]');
    let err = slot.querySelector('.ofc-error');
    if (!err) {
      err = document.createElement('p');
      err.className = 'ofc-error type-ui-caption';
      /* role="alert": a képernyőolvasó azonnal felolvassa, különben a
         visszautasításról a nem látó felhasználó nem értesülne. */
      err.setAttribute('role', 'alert');
      slot.append(err);
    }
    err.textContent = msg;
    if (drop) {
      drop.classList.add('is-error');
      setTimeout(() => drop.classList.remove('is-error'), 1600);
    }
  };

  const clearError = (card) => {
    const err = card.querySelector('.ofc-error');
    if (err) err.remove();
  };

  const clearCard = (card) => {
    const slot = card.querySelector('[data-ofc-slot]');
    const drop = slot.querySelector('[data-ofc-drop]');
    const input = slot.querySelector('[data-ofc-input]');
    const chip = slot.querySelector('.ofc-file');
    if (chip) chip.remove();
    clearError(card);
    input.value = '';
    drop.hidden = false;
    const sel = card.querySelector('.ofc-select');
    if (sel) sel.selectedIndex = 0;
    const note = card.querySelector('.ofc-note');
    if (note) note.value = '';
  };

  /* ------------------------------------------------------- kártyák bekötése */
  cards.forEach((card) => {
    const slot = card.querySelector('[data-ofc-slot]');
    const drop = slot && slot.querySelector('[data-ofc-drop]');
    const input = slot && slot.querySelector('[data-ofc-input]');
    if (!slot || !drop || !input) return;

    drop.addEventListener('click', () => input.click());

    input.addEventListener('change', () => {
      const file = input.files && input.files[0];
      if (!file) return;
      const reason = rejectReason(file);
      if (reason) { input.value = ''; showError(card, reason); return; }
      clearError(card);
      showFile(card, file);
    });

    ['dragenter', 'dragover'].forEach((ev) =>
      slot.addEventListener(ev, (e) => { e.preventDefault(); slot.classList.add('is-drag'); }));
    ['dragleave', 'dragend'].forEach((ev) =>
      slot.addEventListener(ev, (e) => {
        if (!slot.contains(e.relatedTarget)) slot.classList.remove('is-drag');
      }));

    slot.addEventListener('drop', (e) => {
      e.preventDefault();
      slot.classList.remove('is-drag');
      const file = e.dataTransfer && e.dataTransfer.files && e.dataTransfer.files[0];
      if (!file) return;
      const reason = rejectReason(file);
      if (reason) { showError(card, reason); return; }
      clearError(card);
      /* A behúzott fájlt az inputba is bemásoljuk, hogy egy későbbi űrlapküldés
         ugyanazt a fájlt találja, amit a felhasználó lát. */
      try {
        const dt = new DataTransfer();
        dt.items.add(file);
        input.files = dt.files;
      } catch (_) { /* régebbi böngésző: a chip akkor is látszik */ }
      showFile(card, file);
    });

    const clearBtn = card.querySelector('[data-ofc-clear]');
    if (clearBtn) clearBtn.addEventListener('click', () => clearCard(card));
  });

  /* ------------------------------------------- összehasonlító tábla és lépések */
  const compare = document.querySelector('.ofc-compare');
  if (!compare) return;
  const torzs = compare.querySelector('[data-ofc-body]');

  /* A tábla és az üzenet KIZÁRJA egymást. Hibánál egy csupa „—" tábla nemcsak
     csúnya: azt sugallja, hogy az elemzés lefutott és nem talált semmit —
     pedig el sem indult. */
  const uzenet = (szoveg, allapot) => {
    let sav = compare.querySelector('.ofc-uzenet');
    if (!szoveg) {
      if (sav) sav.remove();
      if (torzs) torzs.hidden = false;
      return;
    }
    if (!sav) {
      sav = document.createElement('p');
      sav.className = 'ofc-uzenet type-ui-body';
      compare.insertBefore(sav, torzs);
    }
    sav.className = 'ofc-uzenet type-ui-body' + (allapot === 'hiba' ? ' ofc-uzenet-hiba' : '');
    sav.setAttribute('role', allapot === 'hiba' ? 'alert' : 'status');
    sav.textContent = szoveg;
    if (torzs) torzs.hidden = (allapot === 'hiba');
  };

  const valueCells = Array.from(compare.querySelectorAll('[data-ofc-table] tbody td'))
    .filter((td) => td.cellIndex > 0);
  const headSubs = Array.from(compare.querySelectorAll('[data-ofc-table] thead .ofc-th-sub'));
  const aiList = document.querySelector('.ofc-ai-list');
  const steps = document.querySelectorAll('.ofc-step');


  const OFFER_INDEX = { a: 0, b: 1, c: 2 };

  const uploaded = () =>
    Array.from(document.querySelectorAll('[data-ofc-card] [data-ofc-input]'))
      .map((i) => Boolean(i.files && i.files[0]));

  const emptyState = () => {
    valueCells.forEach((td) => { td.innerHTML = '<span class="ofc-wait">—</span>'; });
    headSubs.forEach((s) => { s.innerHTML = '<span class="ofc-wait">—</span>'; });
    if (aiList) {
      aiList.innerHTML =
        '<li class="ofc-ai-wait type-ui-body"><span>Töltse fel az ajánlatokat — a feldolgozás után ' +
        'itt jelenik meg az összehasonlítás és a rövid összegzés.</span></li>';
    }
    steps.forEach((li, i) => {
      li.classList.toggle('is-active', i === 0);
      li.classList.remove('is-done');
    });
  };

  /* A cella tartalmát a szerver adja. Escape-elve írjuk ki: a modell
     kimenete idegen szöveg, HTML-ként értelmezve beszúrás lenne. */
  const cella = (mezo) => {
    if (!mezo) return '<span class="ofc-dash">—</span>';
    const ertek = document.createElement('span');
    const nincs = /^nincs adat$/i.test(mezo.ertek || '');
    ertek.className = 'ofc-st ' + (nincs ? 'ofc-st-nodata' : 'ofc-st-muted');
    ertek.textContent = mezo.ertek || 'nincs adat';
    if (mezo.reszlet) {
      const kis = document.createElement('small');
      kis.textContent = mezo.reszlet;
      ertek.append(kis);
    }
    return ertek.outerHTML;
  };

  const fillState = (adat) => {
    const kulcsok = Object.keys(adat.szempontok || {});
    const jelek = ['A', 'B', 'C'];

    valueCells.forEach((td, i) => {
      const jel = jelek[td.cellIndex - 1];
      const sor = kulcsok[Math.floor(i / 3)];
      const a = adat.ajanlatok[jel];
      td.innerHTML = a ? cella(a.szempontok[sor]) : '<span class="ofc-dash">—</span>';
    });
    headSubs.forEach((s, i) => {
      const a = adat.ajanlatok[jelek[i]];
      s.textContent = a ? a.cimke : '—';
    });

    if (aiList) {
      aiList.innerHTML = '';
      jelek.forEach((jel) => {
        const a = adat.ajanlatok[jel];
        if (!a || !a.megjegyzes) return;
        const li = document.createElement('li');
        li.className = 'type-ui-subtitle';
        li.textContent = 'Ajánlat ' + jel + ': ' + a.megjegyzes;
        aiList.append(li);
      });
      if (!aiList.children.length) {
        const li = document.createElement('li');
        li.className = 'type-ui-subtitle';
        li.textContent = 'A dokumentumok olvashatók voltak, külön észrevétel nincs.';
        aiList.append(li);
      }
    }

    if (steps[0]) { steps[0].classList.remove('is-active'); steps[0].classList.add('is-done'); }
    if (steps[1]) { steps[1].classList.remove('is-active'); steps[1].classList.add('is-done'); }
    if (steps[2]) steps[2].classList.add('is-active');

    /* A tájékoztató szöveg a szerverről jön, hogy egy helyen legyen karbantartva. */
    uzenet(adat.tajekoztato || '', 'ok');

    /* Innentől van mit jelenteni. Előtte a gombok rejtve vannak: üres tábláról
       készült jelentés azt sugallná, hogy az elemzés lefutott és nem talált
       semmit — pedig el sem indult. */
    const ex = document.querySelector('[data-ofc-export]');
    if (ex) ex.hidden = false;
  };

  emptyState();
  uzenet('', null);

  /* ------------------------------------------------------------- jelentés */
  /* Az összehasonlítás a lapon él: ha a látogató bezárja, elveszik. Ez a rész
     viszi el magával — letöltve, kinyomtatva vagy e-mailben.

     A gombok addig REJTVE maradnak, amíg nincs mit jelenteni: üres tábláról
     készült „jelentés" félrevezető lenne, mert azt sugallná, hogy az elemzés
     lefutott és nem talált semmit. A `fillState` kapcsolja be őket. */
  const exportBlokk = document.querySelector('[data-ofc-export]');
  const levUrlap = document.querySelector('[data-ofc-lev]');

  const jelentesAdat = () => (window.OthJelentes ? window.OthJelentes.gyujt() : null);

  const jelentesHiba = (gomb, eredeti) => {
    gomb.disabled = false;
    gomb.textContent = eredeti;
    uzenet('A jelentés összeállítása nem sikerült. Kérjük, próbálja újra.', 'hiba');
  };

  if (exportBlokk) {
    exportBlokk.hidden = true;

    const letolt = exportBlokk.querySelector('[data-ofc-letolt]');
    if (letolt) {
      letolt.addEventListener('click', () => {
        const adat = jelentesAdat();
        if (!adat) return;
        const eredeti = letolt.textContent;
        letolt.disabled = true;
        letolt.textContent = 'Összeállítás…';
        window.OthJelentes.letoltes(adat, '')
          .then(() => { letolt.disabled = false; letolt.textContent = eredeti; })
          .catch(() => jelentesHiba(letolt, eredeti));
      });
    }

    /* A nyomtatás VALÓDI, azonos eredetű oldalon fut. Egy `blob:` URL-en
       megnyitott dokumentum a lap CSP-jét örökli (`style-src 'self'`), ami
       kiszűrné a beágyazott stílusblokkot — a jelentés formázás nélkül
       jelenne meg. Lásd assets/js/jelentes.js. */
    const pdf = exportBlokk.querySelector('[data-ofc-pdf]');
    if (pdf) {
      pdf.addEventListener('click', () => {
        const adat = jelentesAdat();
        if (!adat || !window.OthJelentes.tarol(adat)) {
          uzenet('A böngésző nem engedi a jelentés átadását (privát mód?). '
               + 'Töltse le HTML-ben, és onnan nyomtassa ki.', 'hiba');
          return;
        }
        window.open('jelentes?nyomtat=1', '_blank', 'noopener');
      });
    }

    const levelNyit = exportBlokk.querySelector('[data-ofc-levelnyit]');
    if (levelNyit && levUrlap) {
      levelNyit.addEventListener('click', () => {
        const nyit = levUrlap.hidden;
        levUrlap.hidden = !nyit;
        levelNyit.setAttribute('aria-expanded', String(nyit));
        if (nyit) {
          const ido = levUrlap.querySelector('[data-urlap-ido]');
          if (ido) ido.value = String(Math.floor(Date.now() / 1000));
          const mezo = levUrlap.querySelector('input[type="email"]');
          if (mezo) mezo.focus();
        }
      });
    }

    if (levUrlap) {
      const allapot = levUrlap.querySelector('[data-ofc-lev-allapot]');
      const kiir = (szoveg, hiba) => {
        if (!allapot) return;
        allapot.textContent = szoveg;
        allapot.classList.toggle('ofc-lev-hiba', Boolean(hiba));
      };

      levUrlap.addEventListener('submit', (e) => {
        e.preventDefault();
        const adat = jelentesAdat();
        if (!adat) return;

        const email = levUrlap.querySelector('input[name="email"]');
        const hozzajarul = levUrlap.querySelector('input[name="hozzajarul"]');
        if (!email.value.trim() || !email.checkValidity()) {
          kiir('Kérjük, adjon meg érvényes e-mail-címet.', true);
          email.focus();
          return;
        }
        if (!hozzajarul.checked) {
          kiir('A jelentés küldéséhez a hozzájárulás szükséges.', true);
          hozzajarul.focus();
          return;
        }

        const kuldes = levUrlap.querySelector('button[type="submit"]');
        kuldes.disabled = true;
        kuldes.setAttribute('aria-busy', 'true');
        kiir('Küldés folyamatban…', false);

        fetch('api/ajanlat-jelentes', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({
            email: email.value.trim(),
            hozzajarul: 1,
            weboldal: levUrlap.querySelector('input[name="weboldal"]').value,
            nyitva: Number(levUrlap.querySelector('[data-urlap-ido]').value) || 0,
            jelentes: adat,
          }),
        })
          .then((r) => r.text().then((t) => {
            let j = {};
            try { j = JSON.parse(t); } catch (_) {
              throw new Error('A kiszolgáló nem értelmezhető választ adott'
                + (r.status ? ' (' + r.status + ')' : '') + '.');
            }
            if (!r.ok || !j.ok) throw new Error(j.uzenet || 'A küldés nem sikerült.');
            return j;
          }))
          .then((j) => {
            kiir(j.uzenet || 'Elküldtük a jelentést a megadott címre.', false);
            levUrlap.reset();
          })
          .catch((err) => kiir(err.message, true))
          .finally(() => {
            kuldes.disabled = false;
            kuldes.removeAttribute('aria-busy');
          });
      });
    }
  }

  const cta = document.querySelector('.ofc-cta');
  if (!cta) return;

  cta.addEventListener('click', () => {
    const up = uploaded();
    if (up.filter(Boolean).length < 2) {
      /* Kevesebb mint két ajánlatot nincs mihez hasonlítani: odagörgetünk az
         első üres kártyához, és megvillantjuk. */
      const firstEmpty = Array.from(document.querySelectorAll('[data-ofc-card]'))
        .find((c) => {
          const i = c.querySelector('[data-ofc-input]');
          return !(i.files && i.files[0]);
        });
      if (firstEmpty) {
        const drop = firstEmpty.querySelector('[data-ofc-drop]');
        firstEmpty.scrollIntoView({ block: 'center', behavior: 'smooth' });
        if (drop) {
          drop.classList.add('ofc-nudge');
          setTimeout(() => drop.classList.remove('ofc-nudge'), 1400);
        }
      }
      return;
    }

    cta.classList.add('is-loading');
    cta.setAttribute('aria-busy', 'true');
    /* A felirat is változik: a mozgó ikon önmagában nem mondja meg, mi tart —
       a dokumentumok kiolvasása fél percig is eltarthat. */
    const felirat = cta.querySelector('[data-ofc-felirat]');
    const eredetiFelirat = felirat ? felirat.textContent : '';
    if (felirat) felirat.textContent = 'Dokumentumok kiolvasása…';

    const adatok = new FormData();
    Array.from(document.querySelectorAll('[data-ofc-card]')).forEach((c, i) => {
      const input = c.querySelector('[data-ofc-input]');
      const sel = c.querySelector('.ofc-select');
      const jel = ['a', 'b', 'c'][i];
      if (input && input.files && input.files[0]) adatok.append('ajanlat_' + jel, input.files[0]);
      if (sel && sel.selectedIndex > 0) adatok.append('tipus_' + jel, sel.value);
    });

    /* Kliensoldali időkorlát. Enélkül a gomb a végtelenségig pörög, ha a
       szerver válasz nélkül elesik — márpedig megosztott tárhelyen ez a
       leggyakoribb kimenet. A határ bővebb, mint a szerveré, hogy annak
       saját hibaüzenete elsőbbséget élvezzen. */
    const megszakito = new AbortController();
    const ora = setTimeout(() => megszakito.abort(), 180000);

    fetch('api/ajanlat-elemzes', {
      method: 'POST', headers: { Accept: 'application/json' },
      body: adatok, signal: megszakito.signal,
    })
      /* A válasz nem biztos, hogy JSON: ha a szerver hibaoldalt vagy üres
         törzset ad, a json() elszállna egy értelmetlen üzenettel. */
      .then((r) => r.text().then((t) => {
        let j = {};
        try { j = JSON.parse(t); } catch (_) {
          throw new Error('A kiszolgáló nem értelmezhető választ adott'
            + (r.status ? ' (' + r.status + ')' : '') + '. Kérjük, próbálja újra.');
        }
        return { ok: r.ok, j };
      }))
      .then(({ ok, j }) => {
        if (!ok || !j.ok) throw new Error(j.uzenet || 'Az elemzés nem sikerült.');
        fillState(j);
        compare.scrollIntoView({ block: 'start', behavior: 'smooth' });
      })
      .catch((e) => uzenet(
        e.name === 'AbortError'
          ? 'A kiolvasás túl sokáig tartott, ezért megszakítottuk. Próbálja kevesebb '
            + 'vagy kisebb fájllal, vagy küldje el nekünk az ajánlatokat.'
          : e.message, 'hiba'))
      .finally(() => {
        clearTimeout(ora);
        cta.classList.remove('is-loading');
        cta.removeAttribute('aria-busy');
        if (felirat) felirat.textContent = eredetiFelirat;
      });
  });
})();
