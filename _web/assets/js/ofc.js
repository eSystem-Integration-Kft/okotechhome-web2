/* =============================================================================
   ÖkoTech Home — Test2 · ofc.js
   AI ajánlat-összehasonlító: fájlcsatolás és az összehasonlító tábla vezérlése
   -----------------------------------------------------------------------------
   A Test1-beli modul viselkedése változatlanul: három kártya (A/B/C), mindegyik
   dropzone-ra kattintva tallóz vagy behúzott fájlt fogad; csatolás után a fájl
   chipje látszik, a fejléc × visszaállítja az üres állapotot. A tábla üresen
   indul, és az „Ajánlatok összehasonlítása" gomb tölti ki — csak azoknak az
   ajánlatoknak az oszlopát, amelyekhez tényleg tartozik feltöltés.

   ⚠️ AMIT A MODUL MA NEM TUD
   A feltöltött fájlok kiolvasása backendet igényel: ma NEM történik elemzés.
   A táblában és az AI-összegzésben MINTAADAT jelenik meg, hogy a felület
   kipróbálható legyen. Ezért a kitöltés után egy jól látható figyelmeztetés is
   megjelenik — enélkül a felhasználó azt hinné, a saját ajánlatait látja
   feldolgozva. (Ugyanaz az elv, mint a 8. szekció e-mail-küldésénél: inkább
   mondjuk meg, hogy még nem éles, mint hogy úgy tegyünk, mintha az lenne.)

   Élesítéskor: a `fillState()` a backend válaszából töltse a cellákat, és a
   `showDemoNotice()` hívása törlendő.
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

  const valueCells = Array.from(compare.querySelectorAll('[data-ofc-table] tbody td'))
    .filter((td) => td.cellIndex > 0);
  const headSubs = Array.from(compare.querySelectorAll('[data-ofc-table] thead .ofc-th-sub'));
  const aiList = document.querySelector('.ofc-ai-list');
  const steps = document.querySelectorAll('.ofc-step');

  /* A markupban álló mintatartalmat eltesszük, mert az üres állapot felülírja. */
  const cellStore = valueCells.map((td) => td.innerHTML);
  const headStore = headSubs.map((s) => s.innerHTML);
  const aiStore = aiList ? aiList.innerHTML : '';

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

  /* A mintaadat-figyelmeztetés. Amíg nincs backend, a tábla NEM a feltöltött
     fájlokból készül — ezt ki kell mondani, nem elrejteni. */
  const showDemoNotice = () => {
    if (compare.querySelector('.ofc-demo')) return;
    const p = document.createElement('p');
    p.className = 'ofc-demo type-ui-body';
    p.setAttribute('role', 'status');
    p.innerHTML =
      '<strong>Ez egy bemutató kitöltés.</strong> A feltöltött fájlok kiolvasása még nem ' +
      'él, ezért az alábbi tábla mintaadatot mutat, nem az Ön ajánlatait. Ha most szeretne ' +
      'érdemi véleményt, küldje el nekünk az ajánlatokat — átnézzük.';
    compare.insertBefore(p, compare.querySelector('[data-ofc-body]'));
  };

  const fillState = () => {
    const up = uploaded();
    valueCells.forEach((td, i) => {
      const offer = td.cellIndex - 1;              // 0 = A, 1 = B, 2 = C
      td.innerHTML = up[offer] ? cellStore[i] : '<span class="ofc-dash">—</span>';
    });
    headSubs.forEach((s, i) => { s.innerHTML = up[i] ? headStore[i] : '—'; });

    if (aiList) {
      aiList.innerHTML = aiStore;
      Array.from(aiList.querySelectorAll('li')).forEach((li) => {
        const key = li.getAttribute('data-ofc-for');
        if (key && !up[OFFER_INDEX[key]]) li.hidden = true;
      });
    }
    if (steps[0]) { steps[0].classList.remove('is-active'); steps[0].classList.add('is-done'); }
    if (steps[1]) steps[1].classList.add('is-active');
    showDemoNotice();
  };

  emptyState();

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
    setTimeout(() => {
      cta.classList.remove('is-loading');
      cta.removeAttribute('aria-busy');
      fillState();
      compare.scrollIntoView({ block: 'start', behavior: 'smooth' });
    }, 900);
  });
})();
