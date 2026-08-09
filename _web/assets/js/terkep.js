/* =============================================================================
 * terkep.js — a kapcsolat oldal térképe
 *
 * KÉT ÜZEMMÓD, ugyanazon a jelölésen.
 *
 * 1) KULCS NÉLKÜL (és JS nélkül) marad a beágyazott Google-keret. A logós
 *    jelölés ilyenkor a mi rétegünk a keret fölött, fix képpontra állítva —
 *    és pontosan addig igaz, amíg a térkép alatta áll. A keret másik eredetről
 *    jön, a benne történő mozgásról a lap semmit nem tud, követni tehát nem
 *    tudjuk. Ezért nem követjük, hanem visszavonjuk: az egér alatt elhalványul
 *    (ezt a CSS intézi), és ha a látogató tényleg a térképpel foglalkozott,
 *    innen végleg elvesszük. A helyet onnantól a Google saját gombostűje
 *    jelöli, ami viszont együtt mozog a térképpel.
 *
 * 2) API-KULCCSAL a keret helyére VALÓDI térkép kerül, és a logós jelölés
 *    valódi térképjelölővé válik: koordinátához kötve, a térképpel együtt
 *    mozogva. Nem tűnik el, nem csúszik el, húzás és nagyítás közben is a
 *    házon marad. Ez az 1) pont teljes körű megoldása — az ottani trükkökre
 *    ilyenkor nincs szükség.
 *
 * A KULCS a `.terkep` elem `data-terkep-kulcs` attribútumában áll. Üresen a
 * lap az 1) módban működik, tehát a kulcs hiánya nem tör el semmit.
 * A Maps JavaScript API kulcsa SZÁNDÉKOSAN publikus (a böngészőben fut) —
 * nem titok, hanem HTTP-referrer-korlátozással kell védeni a Google Cloud
 * konzolban. Lásd `_web/README.md`.
 *
 * A térkép színezését nem CSS-szűrő adja, hanem a Google saját stílusrétege,
 * és az értékeket a designrendszer tokenjeiből olvassuk ki — így a térkép
 * együtt vált a lap világos/sötét témájával, és nincs kettős igazság.
 * ========================================================================== */
(function () {
  'use strict';

  var szekcio = document.querySelector('.terkep');
  if (!szekcio) return;

  var vaszon = szekcio.querySelector('.terkep-vaszon');
  var jeloles = szekcio.querySelector('.terkep-jeloles');
  var keret = szekcio.querySelector('.terkep-beagyazott');
  var elo = szekcio.querySelector('.terkep-elo');
  if (!vaszon || !jeloles || !keret) return;

  var kulcs = (szekcio.getAttribute('data-terkep-kulcs') || '').trim();
  var szel = parseFloat(szekcio.getAttribute('data-terkep-szelesseg'));
  var hossz = parseFloat(szekcio.getAttribute('data-terkep-hosszusag'));
  var nagyitas = parseInt(szekcio.getAttribute('data-terkep-nagyitas'), 10) || 16;

  if (kulcs && elo && isFinite(szel) && isFinite(hossz)) {
    eloTerkep();
  } else {
    beagyazottJeloles();
  }

  /* ---------------------------------------------------------------------
   * 1) BEÁGYAZOTT KERET — a jelölés élettartama
   *
   * Két jelet fogadunk el „tényleg hozzányúlt"-nak:
   *   · az egér legalább 700 ms-ig a térkép fölött volt — a fölötte elhaladó
   *     kurzor ennél rövidebb;
   *   · a keret fókuszt kapott — ez kattintásnál és húzásnál mindig megtörténik.
   *
   * A tévedés ára aszimmetrikus: a fölöslegesen elvett jelölés csak egy
   * hiányzó dísz, a bent maradó viszont rossz helyre mutat. Ezért a szigorúbb
   * irányba tévedünk.
   * ------------------------------------------------------------------- */
  function beagyazottJeloles() {
    var ido = 0;

    function elvesz() {
      window.clearTimeout(ido);
      vaszon.removeEventListener('pointerenter', belep);
      vaszon.removeEventListener('pointerleave', kilep);
      window.removeEventListener('blur', fokuszra);
      jeloles.remove();
    }
    function belep() { ido = window.setTimeout(elvesz, 700); }
    function kilep() { window.clearTimeout(ido); }
    function fokuszra() { if (document.activeElement === keret) elvesz(); }

    vaszon.addEventListener('pointerenter', belep);
    vaszon.addEventListener('pointerleave', kilep);
    window.addEventListener('blur', fokuszra);
  }

  /* ---------------------------------------------------------------------
   * 2) ÉLŐ TÉRKÉP — Maps JavaScript API
   * ------------------------------------------------------------------- */
  function eloTerkep() {
    // A `callback` globális nevet vár; egyedi névvel, hogy ne ütközzön.
    var nev = 'okotechTerkepKesz';
    window[nev] = epit;

    /* A Maps HITELESÍTÉSI hibát nem a script betöltésekor jelez, hanem ezen a
       globális függvényen: a fájl rendben letöltődik, a callback lefut, a
       térkép meg is épül — csak csempe nem érkezik hozzá. Ilyenkor a
       `s.onerror` nem szólal meg, tehát enélkül a látogató üres foltot kapna.
       Ez a leggyakoribb éles hiba: lejárt kulcs, kimerült kvóta, vagy a
       domain hiányzik a HTTP-referrer korlátozásból. */
    window.gm_authFailure = visszaKeretre;

    var s = document.createElement('script');
    s.src = 'https://maps.googleapis.com/maps/api/js'
          + '?key=' + encodeURIComponent(kulcs)
          + '&callback=' + nev + '&language=hu&region=HU&v=weekly&loading=async';
    s.async = true;
    // Ha maga a betöltés hasal el (hálózati hiba, letiltott API), a beágyazott
    // keret a helyén marad, és a jelölés visszakapja az 1) módot.
    s.onerror = beagyazottJeloles;
    document.head.appendChild(s);
  }

  /* Visszaállás a beágyazott keretre, ha az élő térkép nem tud megjelenni.
     A keretet ezért NEM töröljük, csak elrejtjük — amíg nem láttunk egyetlen
     kirajzolt csempét sem, addig szükség lehet rá. */
  function visszaKeretre() {
    szekcio.classList.remove('terkep-el');
    elo.hidden = true;
    elo.innerHTML = '';
    keret.hidden = false;
    beagyazottJeloles();
  }

  function epit() {
    if (!window.google || !window.google.maps) { beagyazottJeloles(); return; }
    jelolesProto();

    // A tároló ELŐBB kapja meg a méretét, mint ahogy a térkép megépül: egy
    // 0 magas dobozon a Maps 0×0-s nézetet számol, és utólag nem rajzol újra.
    szekcio.classList.add('terkep-el');
    elo.hidden = false;

    var terkep = new google.maps.Map(elo, {
      center: { lat: szel, lng: hossz },
      zoom: nagyitas,
      styles: stilus(),
      mapTypeControl: false,
      streetViewControl: false,
      fullscreenControl: false,
      // A görgetés a LAPOT görgesse; a térkép csak Ctrl/⌘ lenyomva nagyít.
      // Enélkül a lapon lefelé haladó látogató beleragad a térképbe.
      gestureHandling: 'cooperative',
      keyboardShortcuts: true
    });

    /* A keretet EGYELŐRE csak elrejtjük. Törölni csak akkor szabad, ha az élő
       térkép bizonyítottan kirajzolt — addig ez a tartalék. A `tilesloaded`
       az első olyan esemény, ami ezt igazolja: hitelesítési hiba esetén soha
       nem következik be, és akkor a gm_authFailure hozza vissza a keretet. */
    keret.hidden = true;

    /* A `tilesloaded` az EGYETLEN megbízható jel arra, hogy az élő térkép
       tényleg megjelent. A `gm_authFailure` nem elég: a Maps a
       RefererNotAllowedMapError esetén nem mindig hívja meg — a hibaüzenet
       kimegy a konzolra, a beépülő DOM felépül, csempe viszont nem érkezik,
       és a látogató üres foltot lát. Ezért határidőt is szabunk: ha ennyi idő
       alatt egyetlen csempe sem jött meg, visszaállunk a beágyazott keretre.
       Így a szekció akkor sem üresedik ki, ha a kulcs lejár, a kvóta elfogy,
       vagy a domain kimarad a referrer-korlátozásból. */
    var hatarido = setTimeout(visszaKeretre, 6000);
    google.maps.event.addListenerOnce(terkep, 'tilesloaded', function () {
      clearTimeout(hatarido);
      keret.remove();
    });

    /* TÉMAVÁLTÁS. A stílust a designrendszer tokenjeiből olvassuk ki, DE csak
       egyszer, a térkép építésekor — így sötétre váltás után a lap sötét lett,
       a térkép viszont világos maradt. Ez a legfeltűnőbb hiba a váltásnál,
       mert a térkép a lap legnagyobb egybefüggő felülete.
       A `data-theme` attribútumot figyeljük a gyökéren: a tema.js azt írja át,
       és a tokenek is ahhoz kötődnek. Nem eseményre hallgatunk, mert a
       témaváltó nem küld sajátot — az attribútum viszont mindig megváltozik. */
    new MutationObserver(function () {
      terkep.setOptions({ styles: stilus() });
    }).observe(document.documentElement, {
      attributes: true, attributeFilter: ['data-theme']
    });

    new Jeloles(terkep, new google.maps.LatLng(szel, hossz), jeloles);
  }

  /* A logós doboz mint valódi térképjelölő. Az `OverlayView` az egyetlen
     eszköz, amivel tetszőleges HTML köthető koordinátához úgy, hogy a
     térképpel együtt mozogjon — a `Marker` csak képet fogad el. */
  function Jeloles(terkep, pont, elem) {
    this.pont = pont;
    this.elem = elem;
    this.setMap(terkep);
  }

  function jelolesProto() {
    if (Jeloles.prototype instanceof google.maps.OverlayView) return;
    Jeloles.prototype = new google.maps.OverlayView();

    Jeloles.prototype.onAdd = function () {
      // `floatPane`: a jelölések rétege, a térképfeliratok fölött.
      this.getPanes().floatPane.appendChild(this.elem);
    };

    Jeloles.prototype.draw = function () {
      var p = this.getProjection().fromLatLngToDivPixel(this.pont);
      if (!p) return;
      // Képpont-pozíció, ezért JS-ből írjuk. Az igazítás (a doboz a pont fölé
      // emelkedik, csücsökkel lefelé) a CSS `transform`-jában marad.
      this.elem.style.left = p.x + 'px';
      this.elem.style.top = p.y + 'px';
    };

    Jeloles.prototype.onRemove = function () {
      if (this.elem.parentNode) this.elem.parentNode.removeChild(this.elem);
    };
  }

  /* A stílus a designrendszer tokenjeiből épül, nem beégetett hexákból: így a
     térkép a lap világos/sötét témájával együtt vált, és egy helyen — a
     tokeneknél — módosul. */
  function stilus() {
    var cs = getComputedStyle(document.documentElement);
    function t(nev, tartalek) {
      var v = cs.getPropertyValue(nev).trim();
      return v || tartalek;
    }
    var zold = t('--surface-muted', '#E5EBBB');
    var viz = t('--surface-sunken', '#DEECEA');
    var lap = t('--canvas', '#F3F2EC');
    var betu = t('--text-secondary', '#56642B');

    return [
      // A telített POI-ikonok és a nem odavaló feliratok elviszik a tekintetet
      // a jelölésről; a térkép itt HÁTTÉR, nem böngészendő adat.
      { featureType: 'poi', elementType: 'labels.icon', stylers: [{ visibility: 'off' }] },
      { featureType: 'poi.business', stylers: [{ visibility: 'off' }] },
      { featureType: 'transit', stylers: [{ visibility: 'off' }] },
      { elementType: 'labels.text.fill', stylers: [{ color: betu }] },
      { elementType: 'labels.text.stroke', stylers: [{ color: lap }, { weight: 3 }] },
      { featureType: 'landscape', elementType: 'geometry', stylers: [{ color: lap }] },
      { featureType: 'poi.park', elementType: 'geometry', stylers: [{ color: zold }] },
      { featureType: 'water', elementType: 'geometry', stylers: [{ color: viz }] },
      { featureType: 'road', elementType: 'geometry.fill', stylers: [{ color: '#FFFFFF' }] },
      { featureType: 'road', elementType: 'geometry.stroke', stylers: [{ visibility: 'off' }] },
      { featureType: 'road.highway', elementType: 'geometry.fill', stylers: [{ color: zold }] }
    ];
  }
})();
