/* ============================================================================
   Galéria — a megbízói helyszíni felvételek léptetése
   ----------------------------------------------------------------------------
   A léptetést a BÖNGÉSZŐ végzi: a sáv `scroll-snap` pálya, tehát az ujjal
   húzás, a trackpad és a vízszintes görgetés magától működik. Ez a modul csak
   ráépül — számlálót ír, a bélyegeket összehangolja, a nyílbillentyűket és a
   léptetőgombokat bekapcsolja.

   EBBŐL KÖVETKEZIK, HOGY HA A SZKRIPT NEM FUT LE, A GALÉRIA AKKOR IS MŰKÖDIK:
   végiggörgethető, minden kép és felirat a HTML-ben van. A gombokat és a
   számlálót ezért NEM a HTML hozza, hanem ez a modul teszi hozzá — így nem
   marad a lapon olyan vezérlő, ami nem csinál semmit.

   Az aktív képet `IntersectionObserver` állapítja meg, nem a görgetési pozíció
   számolása: a snap-pálya a nagyítás, a rugalmas görgetés és a szélső elemek
   miatt nem ad megbízható koordinátát, a láthatóság viszont igen.
   ============================================================================ */
(function () {
  "use strict";

  var galeriak = document.querySelectorAll(".galeria");
  if (!galeriak.length) return;

  var SZOVEG = {
    hu: { elozo: "Előző kép", kovetkezo: "Következő kép", kepre: "Ugrás erre a képre: ",
          kozul: " / ", pálya: "Képek — nyílbillentyűkkel léptethető" },
    en: { elozo: "Previous image", kovetkezo: "Next image", kepre: "Go to image: ",
          kozul: " / ", pálya: "Images — use the arrow keys to move" }
  };
  var NY = (document.documentElement.lang || "hu").slice(0, 2);
  var T = SZOVEG[NY] || SZOVEG.hu;

  galeriak.forEach(function (galeria) {
    var sav = galeria.querySelector(".galeria-sav");
    var elemek = Array.prototype.slice.call(galeria.querySelectorAll(".galeria-elem"));
    if (!sav || elemek.length < 2) return;

    var aktiv = 0;

    /* ---- a vezérlősor: csak most jön létre, mert csak most van értelme ---- */
    var vezerlo = document.createElement("div");
    vezerlo.className = "galeria-vezerlo";

    var elozo = lepteto("-1", T.elozo, "M15 18l-6-6 6-6");
    var kovetkezo = lepteto("1", T.kovetkezo, "M9 6l6 6-6 6");

    var belyegek = document.createElement("ul");
    belyegek.className = "galeria-belyegek";
    belyegek.setAttribute("role", "list");

    elemek.forEach(function (elem, i) {
      var kep = elem.querySelector("img");
      var li = document.createElement("li");
      var gomb = document.createElement("button");
      gomb.type = "button";
      gomb.className = "galeria-belyeg";
      /* A bélyeg neve a képé: a felirat mondja meg, hova ugrunk — nem a sorszám. */
      gomb.setAttribute("aria-label", T.kepre + (kep ? kep.alt : String(i + 1)));
      var bkep = document.createElement("img");
      /* A bélyeghez SAJÁT, apró fájl tartozik (`data-belyeg`). A nagy kép
         újrahasznosítása 80 képpontos helyre több száz kilobájtot töltetne le
         azokért a felvételekért, amelyeket a látogató talán meg sem néz. */
      bkep.src = kep ? (kep.getAttribute("data-belyeg") || kep.currentSrc || kep.src) : "";
      bkep.alt = "";
      bkep.loading = "lazy";
      bkep.decoding = "async";
      gomb.appendChild(bkep);
      gomb.addEventListener("click", function () { ugrik(i); });
      li.appendChild(gomb);
      belyegek.appendChild(li);
    });

    var szamlalo = galeria.querySelector(".galeria-szamlalo");
    if (szamlalo) {
      /* `polite`, nem `assertive`: a léptetés a látogató saját műveletének
         visszajelzése, nem közbevágó hír. */
      szamlalo.setAttribute("aria-live", "polite");
      szamlalo.setAttribute("aria-atomic", "true");
    }

    vezerlo.appendChild(elozo);
    vezerlo.appendChild(belyegek);
    vezerlo.appendChild(kovetkezo);
    galeria.appendChild(vezerlo);

    /* ---- a pálya billentyűzetről is járható ---- */
    /* Innentől a szkript vezérli: a CSS ettől kezdve rejtheti el a nem aktív
       feliratokat, mert van, ami visszahozza őket. */
    galeria.setAttribute("data-vezerelt", "");

    sav.setAttribute("tabindex", "0");
    sav.setAttribute("role", "group");
    sav.setAttribute("aria-label", T.pálya);
    sav.addEventListener("keydown", function (e) {
      if (e.key === "ArrowRight") { e.preventDefault(); ugrik(aktiv + 1); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); ugrik(aktiv - 1); }
      else if (e.key === "Home") { e.preventDefault(); ugrik(0); }
      else if (e.key === "End") { e.preventDefault(); ugrik(elemek.length - 1); }
    });

    /* ---- melyik kép az aktív: a láthatóság dönti el, nem a koordináta ---- */
    var figyelo = new IntersectionObserver(function (bejegyzesek) {
      bejegyzesek.forEach(function (b) {
        if (!b.isIntersecting) return;
        var i = elemek.indexOf(b.target);
        if (i >= 0 && i !== aktiv) { aktiv = i; frissit(); }
      });
    }, { root: sav, threshold: 0.6 });
    elemek.forEach(function (el) { figyelo.observe(el); });

    frissit();

    /* ---- a galéria belépése, ha a szekcióhoz érünk ----
       A belépő jelölést a SZKRIPT teszi rá, és a megjelenéskor veszi le. Ha ez
       a modul nem fut le, a galéria alapból látható marad — a láthatóság sosem
       függhet attól, hogy egy szkript lefutott-e. */
    if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      galeria.setAttribute("data-belep", "");
      var belepo = new IntersectionObserver(function (b) {
        if (b[0].isIntersecting) { galeria.removeAttribute("data-belep"); belepo.disconnect(); }
      }, { threshold: 0.15 });
      belepo.observe(galeria);
      /* Biztonsági háló: ha a figyelő bármiért nem szólal meg (nulla magasságú
         szülő, régi görgetéstároló), a jelölés akkor is lekerül. */
      setTimeout(function () { galeria.removeAttribute("data-belep"); }, 2500);
    }

    function lepteto(irany, cimke, ut) {
      var g = document.createElement("button");
      g.type = "button";
      g.className = "galeria-lep";
      g.setAttribute("aria-label", cimke);
      g.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" ' +
        'stroke="currentColor" stroke-width="1.8" stroke-linecap="round" ' +
        'stroke-linejoin="round" aria-hidden="true"><path d="' + ut + '"/></svg>';
      g.addEventListener("click", function () { ugrik(aktiv + Number(irany)); });
      return g;
    }

    function ugrik(i) {
      i = Math.max(0, Math.min(elemek.length - 1, i));
      /* `scrollIntoView` helyett a sáv saját görgetése: az előbbi a LAPOT is
         megmozgatná, és a galéria kiugrana a képernyő közepére lapozás közben. */
      sav.scrollTo({ left: elemek[i].offsetLeft - sav.offsetLeft, behavior: mozog() });
      aktiv = i;
      frissit();
    }

    function mozog() {
      return window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth";
    }

    function frissit() {
      elemek.forEach(function (el, i) {
        if (i === aktiv) el.setAttribute("data-aktiv", "");
        else el.removeAttribute("data-aktiv");
      });
      var gombok = belyegek.querySelectorAll(".galeria-belyeg");
      gombok.forEach(function (g, i) {
        if (i === aktiv) g.setAttribute("aria-current", "true");
        else g.removeAttribute("aria-current");
      });
      if (gombok[aktiv]) {
        var g = gombok[aktiv];
        belyegek.scrollTo({
          left: g.offsetLeft - belyegek.offsetLeft - (belyegek.clientWidth - g.clientWidth) / 2,
          behavior: mozog()
        });
      }
      elozo.disabled = aktiv === 0;
      kovetkezo.disabled = aktiv === elemek.length - 1;
      if (szamlalo) szamlalo.textContent = (aktiv + 1) + T.kozul + elemek.length;
    }
  });
})();
