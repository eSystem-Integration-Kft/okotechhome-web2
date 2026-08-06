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
  const ALLOWED_EXT = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png'];
  const MAX_SIZE = 10 * 1024 * 1024;

  const extOf = (file) => (file.name.split('.').pop() || '').toLowerCase();

  const rejectReason = (file) => {
    if (!ALLOWED_EXT.includes(extOf(file))) {
      return 'Nem támogatott formátum. Engedélyezett: PDF, DOC, DOCX, XLS, XLSX, PNG.';
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
  };

  emptyState();
  uzenet('', null);

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

    const adatok = new FormData();
    Array.from(document.querySelectorAll('[data-ofc-card]')).forEach((c, i) => {
      const input = c.querySelector('[data-ofc-input]');
      const sel = c.querySelector('.ofc-select');
      const jel = ['a', 'b', 'c'][i];
      if (input && input.files && input.files[0]) adatok.append('ajanlat_' + jel, input.files[0]);
      if (sel && sel.selectedIndex > 0) adatok.append('tipus_' + jel, sel.value);
    });

    fetch('api/ajanlat-elemzes', { method: 'POST', headers: { Accept: 'application/json' }, body: adatok })
      .then((r) => r.json().then((j) => ({ ok: r.ok, j })))
      .then(({ ok, j }) => {
        if (!ok || !j.ok) throw new Error(j.uzenet || 'Az elemzés nem sikerült.');
        fillState(j);
        compare.scrollIntoView({ block: 'start', behavior: 'smooth' });
      })
      .catch((e) => uzenet(e.message, 'hiba'))
      .finally(() => {
        cta.classList.remove('is-loading');
        cta.removeAttribute('aria-busy');
      });
  });
})();
