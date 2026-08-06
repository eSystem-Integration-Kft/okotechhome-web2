/* =============================================================================
 * terkep.js — a logós térképjelölés élettartama
 *
 * A jelölés egy SAJÁT réteg a beágyazott Google Térkép fölött. A helye fix
 * képpontban van megadva (lásd app.css `.terkep-jeloles`), és pontosan addig
 * mutat a cégre, amíg a térkép alatta áll. Ha a látogató elhúzza vagy
 * átnagyítja a térképet, a réteg a helyén marad — onnantól rossz helyre mutat.
 *
 * Ezt nem lehet megelőzni: a keret másik eredetről jön, a benne történő
 * mozgásról a lap semmit nem tud. Ezért nem követjük, hanem VISSZAVONJUK: ha
 * a látogató valóban a térképpel foglalkozott, a jelölést végleg elvesszük.
 * A pontos helyet ilyenkor a Google saját gombostűje jelöli, ami viszont
 * együtt mozog a térképpel.
 *
 * A halványítást (egér a térkép fölött) a CSS intézi, JS nélkül is működik.
 * Ez a fájl csak a VÉGLEGES eltávolítást adja hozzá.
 *
 * Két jelet fogadunk el „tényleg hozzányúlt"-nak:
 *   · az egér legalább 700 ms-ig a térkép fölött volt — a fölötte elhaladó
 *     kurzor ennél rövidebb;
 *   · a keret fókuszt kapott — ez kattintásnál és húzásnál mindig megtörténik.
 *
 * A tévedés ára aszimmetrikus: fölöslegesen elvett jelölés csak egy hiányzó
 * dísz, a bent maradó viszont rossz helyre mutat. Ezért a szigorúbb irányba
 * tévedünk.
 * ========================================================================== */
(function () {
  'use strict';

  var vaszon = document.querySelector('.terkep-vaszon');
  if (!vaszon) return;

  var jeloles = vaszon.querySelector('.terkep-jeloles');
  var keret = vaszon.querySelector('.terkep-beagyazott');
  if (!jeloles || !keret) return;

  var ido = 0;

  function elvesz() {
    window.clearTimeout(ido);
    vaszon.removeEventListener('pointerenter', belep);
    vaszon.removeEventListener('pointerleave', kilep);
    window.removeEventListener('blur', fokuszra);
    jeloles.remove();
  }

  function belep() {
    ido = window.setTimeout(elvesz, 700);
  }

  function kilep() {
    window.clearTimeout(ido);
  }

  // A keretbe kattintás elveszi a lap fókuszát; az `activeElement` ilyenkor
  // maga a keret. Ez az egyetlen jel, amit egy másik eredetű iframe-ről
  // biztosan megkapunk.
  function fokuszra() {
    if (document.activeElement === keret) elvesz();
  }

  vaszon.addEventListener('pointerenter', belep);
  vaszon.addEventListener('pointerleave', kilep);
  window.addEventListener('blur', fokuszra);
})();
