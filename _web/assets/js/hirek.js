/* ============================================================================
   Hírek — rovatszűrés a gyűjtőlapon
   ----------------------------------------------------------------------------
   A LISTA TELJES EGÉSZÉBEN A HTML-BEN VAN. Ez a modul nem épít listát, csak
   elrejti azt, ami nem tartozik a kiválasztott rovathoz. Ebből következik,
   hogy szkript nélkül minden hír látszik — a szűrés kényelmi funkció, nem a
   tartalom feltétele.

   A REJTÉST A NATÍV `hidden` VÉGZI, nem osztály: a képernyőolvasó és a
   keresőn belüli keresés (Ctrl+F) is ezt érti, és nincs olyan állapot, amiben
   az elem vizuálisan eltűnik, de a fókuszsorrendben benne marad.

   AZ ÁLLAPOTOT AZ `aria-pressed` HORDOZZA, szintén natív attribútum — a chip
   kinézetét a CSS ebből olvassa ki (`.hir-chip[aria-pressed="true"]`), tehát
   nincs két helyen nyilvántartott igazság.

   A VÁLASZTÁS BEKERÜL AZ URL-BE (`?rovat=…`, `history.replaceState`): így a
   megosztott hivatkozás ugyanazt a nézetet hozza vissza, és a részletlapról
   visszalépve nem esik szét a szűrés. Új előzménybejegyzést NEM írunk — a
   „vissza" gomb a lapról KIFELÉ vigyen, ne a szűrő korábbi állásaiba.
   ============================================================================ */
(function () {
  "use strict";

  var gyoker = document.querySelector("[data-hirek]");
  if (!gyoker) return;

  var chipek = Array.prototype.slice.call(gyoker.querySelectorAll(".hir-chip"));
  /* CSAK A KÁRTYÁK. A puszta `[data-rovat]` a szűrőgombokat is megtalálta —
     azokon ugyanez az adatjelző áll —, így a szűrés a saját vezérlőit is
     elrejtette volna, a találatszámba pedig beleszámolta a négy gombot. */
  var elemek = Array.prototype.slice.call(
    gyoker.querySelectorAll(".card-item[data-rovat]"));
  var talalat = gyoker.querySelector("[data-hir-talalat]");
  var ures = gyoker.querySelector("[data-hir-ures]");
  if (!chipek.length || !elemek.length) return;

  var SZOVEG = {
    hu: { egy: " hír", tobb: " hír", mind: "Összesen " },
    en: { egy: " item", tobb: " items", mind: "Total " }
  };
  var T = SZOVEG[(document.documentElement.lang || "hu").slice(0, 2)] || SZOVEG.hu;

  /* A találatszám csak most kerül a lapra: szkript nélkül nincs szűrés, tehát
     nincs mit visszajelezni — egy statikus „42 hír" felirat ilyenkor csak
     zaj volna. */
  if (talalat) {
    talalat.hidden = false;
    talalat.setAttribute("aria-live", "polite");
  }

  function ervenyes(rovat) {
    if (!rovat || rovat === "mind") return "mind";
    return chipek.some(function (c) { return c.dataset.rovat === rovat; })
      ? rovat : "mind";
  }

  function szur(rovat, urlbe) {
    var db = 0;
    elemek.forEach(function (el) {
      var latszik = rovat === "mind" || el.dataset.rovat === rovat;
      el.hidden = !latszik;
      if (latszik) db++;
    });
    chipek.forEach(function (c) {
      c.setAttribute("aria-pressed", String(c.dataset.rovat === rovat));
    });
    if (talalat) talalat.textContent = T.mind + db + (db === 1 ? T.egy : T.tobb);
    if (ures) ures.hidden = db !== 0;

    if (urlbe && window.history && window.history.replaceState) {
      var u = new URL(window.location.href);
      if (rovat === "mind") u.searchParams.delete("rovat");
      else u.searchParams.set("rovat", rovat);
      window.history.replaceState(null, "", u);
    }
  }

  chipek.forEach(function (c) {
    c.addEventListener("click", function () { szur(c.dataset.rovat, true); });
  });

  var indulo = "mind";
  try {
    indulo = ervenyes(new URL(window.location.href).searchParams.get("rovat"));
  } catch (e) { /* régi böngésző: marad a teljes lista */ }
  szur(indulo, false);
})();

/* ============================================================================
   Hírek — vízszintes idővonal: lassú sodrás és léptetőgombok
   ----------------------------------------------------------------------------
   A SÁV SZKRIPT NÉLKÜL IS MŰKÖDIK: `overflow-x` pálya, tehát ujjal húzható,
   trackpaddel görgethető, és a Tab-bal érkező fókusz magától begörgeti a
   következő pontot. Ez a modul két dolgot tesz hozzá — a lassú sodrást és a
   két léptetőgombot —, és MINDKETTŐT csak akkor, ha van értelme:

   · a sodrás el sem indul, ha a sor kifér, vagy ha a látogató kevesebb
     mozgást kért (`prefers-reduced-motion`);
   · a gombokat a szkript hozza létre, nem a HTML — így nem marad a lapon
     olyan vezérlő, amelyik nem csinál semmit.

   A SODRÁS MEGÁLL, amint valaki hozzáér: egér, fókusz, ujj, görgetés. Ez nem
   udvariasság, hanem a használhatóság feltétele — egy magától mozgó sávban
   nem lehet célba találni. Újraindul, ha a látogató elengedi, de csak egy
   rövid szünet után, hogy az olvasás közben ne kapkodjon.

   A végeken VISSZAFORDUL, nem ugrik vissza az elejére: a szakasznak van eleje
   és vége (2014 → ma), nem körkörös.
   ============================================================================ */
(function () {
  "use strict";

  var idovonalak = document.querySelectorAll(".hir-idovonal");
  if (!idovonalak.length) return;

  var SZOVEG = {
    hu: { elore: "Előre az időben", vissza: "Vissza az időben" },
    en: { elore: "Forward in time", vissza: "Back in time" }
  };
  var T = SZOVEG[(document.documentElement.lang || "hu").slice(0, 2)] || SZOVEG.hu;

  var NYIL = {
    vissza: "M15 5 8 12l7 7",
    elore: "m9 5 7 7-7 7"
  };

  function gomb(irany, cimke) {
    var b = document.createElement("button");
    b.type = "button";
    b.className = "hir-idovonal-gomb";
    b.setAttribute("aria-label", cimke);
    b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" ' +
      'stroke-linecap="round" stroke-linejoin="round"><path d="' +
      NYIL[irany] + '"/></svg>';
    return b;
  }

  idovonalak.forEach(function (ido) {
    var palya = ido.querySelector(".hir-idovonal-palya");
    var vezerlok = ido.querySelector(".hir-idovonal-vezerlok");
    if (!palya) return;

    var lepes = function () {
      var elem = palya.querySelector(".hir-idovonal-elem");
      /* Három hasábnyi ugrás: elég nagy, hogy haladjon, elég kicsi, hogy a
         szem kövesse. */
      return (elem ? elem.getBoundingClientRect().width : 200) * 3;
    };

    function hatar() {
      return palya.scrollWidth - palya.clientWidth;
    }

    /* A simítást a MŰVELET kéri, nem a konténer (lásd az app.css jegyzetét).
       Kevesebb mozgást kérő látogatónál ugrik, nem gördül. */
    var halkabb = window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var MOD = halkabb ? "auto" : "smooth";

    /* ---- léptetőgombok ---- */
    var balra, jobbra;
    if (vezerlok) {
      balra = gomb("vissza", T.vissza);
      jobbra = gomb("elore", T.elore);
      vezerlok.appendChild(balra);
      vezerlok.appendChild(jobbra);
      balra.addEventListener("click", function () {
        keziSzunet(); palya.scrollBy({ left: -lepes(), behavior: MOD });
      });
      jobbra.addEventListener("click", function () {
        keziSzunet(); palya.scrollBy({ left: lepes(), behavior: MOD });
      });
    }

    var savKeret = ido.querySelector(".hir-idovonal-keret");

    function allapotFrissit() {
      /* Az 1px tűrés a tört képpontos görgetési pozíció miatt kell: a
         `scrollLeft` ritkán áll pontosan nullán vagy a határon. */
      var eleje = palya.scrollLeft <= 1;
      var vege = palya.scrollLeft >= hatar() - 1;
      if (balra) {
        /* A szélen álló gomb `disabled` — natív állapot, a képernyőolvasó is
           ezt mondja. */
        balra.disabled = eleje;
        jobbra.disabled = vege;
      }
      if (savKeret) {
        /* A széli elhalványítás csak arra az oldalra kerül, amerre van még
           sor. A CSS ebből a két jelzőből olvassa ki a maszkot. */
        savKeret.toggleAttribute("data-balra", !eleje);
        savKeret.toggleAttribute("data-vege", !vege);
      }
    }
    palya.addEventListener("scroll", allapotFrissit, { passive: true });
    window.addEventListener("resize", allapotFrissit);
    allapotFrissit();

    /* ---- sodrás: magától, és az egérrel a sáv szélén ---- */
    if (halkabb || hatar() < 8) {
      if (vezerlok && hatar() < 8) vezerlok.hidden = true;
      return;
    }

    /* KÉT ÜZEMMÓD, EGY HUROK.

       · MAGÁTÓL — amíg senki nem nyúl hozzá, a sáv nagyon lassan sodródik, és
         a végeken visszafordul. Ez csak annyit mond el, hogy a sor folytatódik.
       · AZ EGÉRREL — ha a mutató a sáv SZÉLE felé tart, arrafelé gördül, és
         annál gyorsabban, minél közelebb van a széléhez. A sáv közepén áll.
         Így a látogató a gombok nélkül is végigpásztázhatja a tizenkét évet,
         egyetlen mozdulattal, oda-vissza.

       A sebesség NÉGYZETESEN nő a zónában (`k * k`), nem egyenesen: a zóna
       belső határán így alig indul meg — nincs az a rántás, ami az egyenes
       arányosságnál a zónahatáron érződik —, a legszélén viszont gyors. */
    var AMBIENS = 28;       /* képpont / másodperc, magától */
    var EL_MAX = 520;       /* képpont / másodperc a sáv legszélén */
    var ZONA = 0.22;        /* a sáv szélességének hányada mindkét oldalon */
    var KEZI_MS = 1200;     /* gombnyomás után ennyi ideig nem sodrunk */

    var irany = 1, poz = palya.scrollLeft, utolso = 0, ido_id = 0;
    var hover = false, egerX = 0, huzas = false, fokusz = false, kezi_ig = 0;

    function zonaSzelesseg(r) {
      /* A zóna a sáv arányos része, de van alsó és felső korlátja: keskeny
         kijelzőn a 22% pár tíz képpont volna (véletlenül is beletévednénk),
         széles kijelzőn viszont a fél sávot elvinné. */
      return Math.max(72, Math.min(260, r.width * ZONA));
    }

    function elSebesseg() {
      var r = palya.getBoundingClientRect();
      var z = zonaSzelesseg(r);
      var balTav = egerX - r.left;
      var jobbTav = r.right - egerX;
      if (balTav < z) {
        var kb = (z - balTav) / z;
        return -EL_MAX * kb * kb;
      }
      if (jobbTav < z) {
        var kj = (z - jobbTav) / z;
        return EL_MAX * kj * kj;
      }
      return 0;
    }

    function sebesseg() {
      if (huzas || Date.now() < kezi_ig) return 0;
      if (hover) return elSebesseg();
      if (fokusz) return 0;      /* billentyűzetes olvasás közben álljon */
      return irany * AMBIENS;
    }

    /* A POZÍCIÓT SAJÁT SZÁMLÁLÓ TARTJA, nem a `scrollLeft` visszaolvasása:
       képkockánként fél képpont a lépés, a böngésző pedig a `scrollLeft`
       getterén kerekíthet — ilyenkor minden kör ugyanazt az értéket adná
       vissza, és a sáv soha nem mozdulna el. */
    function kocka(t) {
      if (!utolso) utolso = t;
      var dt = Math.min((t - utolso) / 1000, 0.05);  /* fülváltás után ne ugorjon */
      utolso = t;
      var h = hatar();
      if (h < 8) { ido_id = 0; return; }
      var v = sebesseg();
      if (v) {
        poz += v * dt;
        /* A végeken megáll. Magától visszafordul (a szakasznak van eleje és
           vége, nem körkörös); egérrel viszont csak nekiütközik a szélnek —
           ott a látogató dönti el, merre tovább. */
        if (poz >= h) { poz = h; if (!hover) irany = -1; }
        if (poz <= 0) { poz = 0; if (!hover) irany = 1; }
        palya.scrollLeft = poz;
      } else {
        poz = palya.scrollLeft;   /* álltunkban követjük a kézi görgetést */
      }
      ido_id = window.requestAnimationFrame(kocka);
    }

    /* A FUTÁS EGYETLEN IGAZSÁGA a képkocka-azonosító. Külön „áll" jelzőt
       tartani azért veszélyes, mert a két érték szétcsúszhat — ha a böngésző
       eldobja a képkockát (például háttérfülön), a jelző „fut" állásban
       ragad, és a sáv többé nem indul újra. */
    function indul() {
      if (ido_id || document.hidden) return;
      poz = palya.scrollLeft;
      utolso = 0;
      ido_id = window.requestAnimationFrame(kocka);
    }
    function allj() {
      if (ido_id) { window.cancelAnimationFrame(ido_id); ido_id = 0; }
    }
    function keziSzunet() { kezi_ig = Date.now() + KEZI_MS; }

    /* Az egérrel vezérelt sodrás CSAK EGÉRRE szól: ujjal a húzás a természetes
       mozdulat, és ott a „sáv széle" a képernyő széle is egyben. */
    palya.addEventListener("pointerenter", function (e) {
      if (e.pointerType === "touch") return;
      hover = true; egerX = e.clientX; jelolElt();
    });
    palya.addEventListener("pointermove", function (e) {
      if (e.pointerType === "touch") return;
      hover = true; egerX = e.clientX; jelolElt();
    });
    palya.addEventListener("pointerleave", function () {
      hover = false; jelolElt();
    });
    palya.addEventListener("pointerdown", function () { huzas = true; });
    /* A felengedést az ABLAKON figyeljük, és a megszakadt mutatóeseményt is:
       ha a látogató a sávon nyomja le és az ablakon kívül engedi el, a `huzas`
       „lenyomva" állásban ragadna, és a sodrás soha többé nem indulna el. */
    window.addEventListener("pointerup", function () { huzas = false; });
    window.addEventListener("pointercancel", function () { huzas = false; });
    window.addEventListener("blur", function () { huzas = false; });
    palya.addEventListener("wheel", keziSzunet, { passive: true });
    ido.addEventListener("focusin", function () { fokusz = true; });
    ido.addEventListener("focusout", function () { fokusz = false; });

    /* A mutató alakja megmondja, mi történik: a zónában oldalra mutató nyíl,
       a sáv közepén a szokásos. A CSS ebből a jelzőből dolgozik. */
    function jelolElt() {
      if (!savKeret) return;
      if (!hover) { savKeret.removeAttribute("data-el"); return; }
      var v = elSebesseg();
      if (v < 0) savKeret.setAttribute("data-el", "bal");
      else if (v > 0) savKeret.setAttribute("data-el", "jobb");
      else savKeret.removeAttribute("data-el");
    }

    /* Csak akkor fusson, ha látszik: háttérfülön és a képernyőn kívül
       fölösleges munka. */
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (bejegyzesek) {
        bejegyzesek.forEach(function (b) {
          if (b.isIntersecting) indul(); else allj();
        });
      }, { threshold: 0.2 }).observe(ido);
    } else {
      indul();
    }
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) allj(); else indul();
    });
  });
})();

/* ============================================================================
   Hírek — nagyított képnézet
   ----------------------------------------------------------------------------
   A cikkbeli képek visszafogott méretben állnak; aki közelebbről akarja látni
   valamelyiket, rákattint, és a kép előtérbe jön, a lap mögötte elmosódik.

   A DOBOZT A PLATFORM ADJA: natív `<dialog>` + `showModal()`. Ebből magától
   jön a fókuszcsapda, az Esc, a háttér inertté tétele, a visszatérő fókusz és
   a `::backdrop` — mindaz, amit egy kézzel épített „modal" el szokott rontani.
   Ha a böngésző nem ismeri a `showModal`-t, a modul NEM csinál semmit: a képek
   maradnak képnek, és nem ül a lapon nem működő gomb.

   EGYETLEN DOBOZ szolgálja ki az összes képet — negyvenkét cikkben több száz
   `<dialog>` fölösleges DOM volna.

   A NAGYÍTÓGOMBOT IS EZ A MODUL TESZI a képek köré, nem a HTML: szkript nélkül
   a kép nem kattintható, tehát nem is szabad úgy kinéznie.
   ============================================================================ */
(function () {
  "use strict";

  var kepek = document.querySelectorAll(".hir-figura img");
  if (!kepek.length) return;
  if (typeof HTMLDialogElement === "undefined" ||
      !HTMLDialogElement.prototype.showModal) return;

  var SZOVEG = {
    hu: { nyit: "Kép megnyitása nagyban", bezar: "Bezárás", cimke: "Nagyított kép" },
    en: { nyit: "Open image larger", bezar: "Close", cimke: "Enlarged image" }
  };
  var T = SZOVEG[(document.documentElement.lang || "hu").slice(0, 2)] || SZOVEG.hu;

  /* ---- a közös doboz ---- */
  var doboz = document.createElement("dialog");
  doboz.className = "hir-nagykep";
  doboz.setAttribute("aria-label", T.cimke);

  var nagykep = document.createElement("img");
  nagykep.className = "hir-nagykep-kep";
  nagykep.decoding = "async";

  var felirat = document.createElement("p");
  felirat.className = "type-ui-caption hir-nagykep-felirat";

  var bezar = document.createElement("button");
  bezar.type = "button";
  bezar.className = "hir-nagykep-bezar";
  bezar.setAttribute("aria-label", T.bezar);
  bezar.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true" ' +
    'stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>';

  doboz.appendChild(bezar);
  doboz.appendChild(nagykep);
  doboz.appendChild(felirat);
  document.body.appendChild(doboz);

  bezar.addEventListener("click", function () { doboz.close(); });

  /* A HÁTTÉRRE KATTINTVA IS ZÁR. A `::backdrop` nem külön elem: a rá érkező
     kattintás a `<dialog>`-on jelenik meg. Ezért csak akkor zárunk, ha a
     célpont MAGA a doboz — a képre vagy a feliratra kattintás nem zárhat. */
  doboz.addEventListener("click", function (e) {
    if (e.target === doboz) doboz.close();
  });

  /* ---- a képek köré tett gomb ---- */
  Array.prototype.forEach.call(kepek, function (kep) {
    var gomb = document.createElement("button");
    gomb.type = "button";
    gomb.className = "hir-nagyit";
    gomb.setAttribute("aria-label", T.nyit);
    kep.parentNode.insertBefore(gomb, kep);
    gomb.appendChild(kep);

    gomb.addEventListener("click", function () {
      /* A FORRÁST NYITÁS ELŐTT ÍRJUK ÁT, nem záráskor takarítunk. A `close`
         eseményre bízni a tisztítást csábító volna, de az `allow-discrete`
         záróátmenettel futó dobozon nem megbízhatóan tüzel — mérve: nem jött
         meg másfél másodperc alatt sem. Így viszont a doboz mindig a helyes
         képpel nyílik, esemény nélkül is.

         A `srcset`-es képnél a böngésző által TÉNYLEGESEN kiválasztott
         változatot vesszük át (`currentSrc`), nem a `src`-t: különben a
         kártyaméretű fájl nagyítódna fel. */
      nagykep.removeAttribute("width");
      nagykep.removeAttribute("height");
      nagykep.src = kep.currentSrc || kep.src;
      nagykep.alt = kep.alt;
      if (kep.naturalWidth) {
        nagykep.width = kep.naturalWidth;
        nagykep.height = kep.naturalHeight;
      }
      felirat.textContent = kep.alt;
      felirat.hidden = !kep.alt;
      doboz.showModal();
    });
  });
})();
