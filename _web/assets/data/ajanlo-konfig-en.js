/* =============================================================================
   ÖkoTech Home — AI solution finder (section 6) · CONFIGURATION (English)
   -----------------------------------------------------------------------------
   The English counterpart of `ajanlo-konfig.js`. Same shape, same keys, same
   answer identifiers — only the wording differs. The identifiers MUST stay in
   Hungarian: the decision rules, the saved case records and the CRM handover
   all key on them, and a saved result must read the same whichever language
   produced it.

   TERMINOLOGY, fixed once and used consistently:
     oldómedence          → septic tank
     zárt tároló          → sealed holding tank
     szikkasztómező       → drainage field   (the septic tank's larger field)
     szivárogtató         → soakaway         (the treatment unit's smaller one)
     kiemelt szivárogtató → raised soakaway
     speciális rögzítés   → anti-flotation anchoring
     tisztázandók         → points to clarify

   The URLs point into the HUNGARIAN page tree with `../`, because those pages
   have no English versions yet. As English pages appear, the URLs move with
   them — one edit per line, in this file.
   ============================================================================= */
window.OTH_AJANLO = {

  verzio: "2026-08-28",

  mentes: {
    bevezeto: "Once you save, you get a reference. This is not registration: we ask for no name, "
            + "no email address and no telephone number, and we do not know who you are. "
            + "It does one thing: it remembers what you have already told us. With it you can "
            + "return to this result at any time, print it or save it as a PDF, and our other "
            + "tools (the price estimator further down the page, for instance) will not ask you "
            + "the same questions again. If you do not save it, nothing stays with us — your "
            + "answers remain in your browser.",
    azonositoMagyarazat: "What is this? A code that ties your answers together — with no personal data. "
                       + "It is not registration, and you do not have to memorise it: you can simply bookmark the page.",
    megorzesSzoveg: "The saved result is stored under a reference, with no personal data, for 180 days."
  },

  lepesek: [
    { id: "hasznalat", cim: "Pattern of use",
      uzenet: "Let us start with how the property is used: this decides which technology can be considered at all. Three short questions." },
    { id: "letszam", cim: "Occupancy / load",
      uzenet: "Thank you. Next comes the load the system will carry." },
    { id: "kihagyas", cim: "Length of gaps",
      uzenet: "One more question about use — the length of the gaps also bears on the choice of technology." },
    { id: "telek", cim: "The plot",
      uzenet: "On the basis of use, {irany} currently looks like the right direction. Now let us see what conditions the plot imposes on the build.",
      uzenetVegyes: "On the basis of use the picture is mixed — we will come back to that at the end. Now let us see what the plot says." },
    { id: "vizelhelyezes", cim: "Water disposal",
      uzenet: "The last question is about disposing of the treated water. This is the one factor that can rule a solution out on its own." },
    { id: "eredmeny", cim: "Result", zaro: true,
      uzenet: "We are done. This is the picture your answers give." }
  ],

  kerdesek: [
    {
      id: "hasznalat", lepes: "hasznalat",
      kerdes: "How regularly is the property used?",
      valaszok: [
        { id: "eletvitelszeru", cimke: "All year round, as a permanent home" },
        { id: "hetvegi",        cimke: "At weekends or occasionally" },
        { id: "szezonalis",     cimke: "Only in certain months" }
      ],
      magyarazat: {
        eletvitelszeru: "This is the single most important input to the choice of technology. Under a year-round, even load the bacterial culture is fed continuously, so active biological treatment can be sustained. A two- or three-week holiday does not on its own count as intermittent use.",
        hetvegi:        "Weekend or occasional use means an intermittent load. Continuous, active biological operation is harder to sustain then — the next two questions decide whether this really is an intermittent pattern.",
        szezonalis:     "A property lived in only during certain months has long idle spells. The next two questions look at how much load falls on the period of use — that is what separates intermittent use from strong seasonality."
      }
    },
    {
      id: "letszam", lepes: "letszam",
      kerdes: "How many people use it regularly?",
      valaszok: [
        { id: "1-2",  cimke: "1–2 people" },
        { id: "3-4",  cimke: "3–4 people" },
        { id: "5-6",  cimke: "5–6 people" },
        { id: "7-10", cimke: "7–10 people" },
        { id: "10+",  cimke: "More than 10" }
      ],
      magyarazat: {
        "1-2":  "With few occupants the daily volume of wastewater is low too. That is not a problem in itself, but combined with longer absences the load can become so uneven that the pattern already counts as a borderline case.",
        "3-4":  "This is the most common household size, and its load is easy to predict.",
        "5-6":  "With more occupants the peak load is higher too. Combined with intermittent use, the system carries a fluctuating load — and then the pattern cannot be classified automatically.",
        "7-10": "At this occupancy the sizing is a technical question in its own right, and handling the peak load also bears on the choice of technology.",
        "10+":  "Above ten people we are no longer talking about domestic scale: the system is built from several units, and the sizing calls for individual design."
      }
    },
    {
      id: "kihagyas", lepes: "kihagyas",
      kerdes: "Are there gaps of several weeks or months?",
      valaszok: [
        { id: "nincs",   cimke: "No, a holiday at most" },
        { id: "hetek",   cimke: "Yes, a few weeks" },
        { id: "honapok", cimke: "Yes, several months" }
      ],
      magyarazat: {
        nincs:   "Under a continuous load the bacterial culture can be sustained steadily — that is the basic condition for active biological treatment.",
        hetek:   "After a gap of a few weeks the culture restarts, but the pattern is no longer entirely even. Whether this rules out an active system emerges together with the pattern of use and the occupancy.",
        honapok: "Over an idle spell of several months the active biological culture breaks down. Restarting is manageable, but where it recurs regularly it becomes an operating question worth talking through in person."
      }
    },
    {
      id: "talajviz", lepes: "telek",
      kerdes: "Is there any sign that the groundwater may be high?",
      sugo: "A dug well, a damp cellar, experience from nearby properties.",
      valaszok: [
        { id: "igen",     cimke: "Yes" },
        { id: "nem",      cimke: "No" },
        { id: "nemtudom", cimke: "I do not know", nemtudom: true }
      ],
      magyarazat: {
        igen:     "This does not on its own rule out the proposed solution. For the build, though, it is worth allowing for a raised soakaway and anti-flotation anchoring, so that the groundwater cannot lift the tank.",
        nem:      "This allows the standard arrangement: the tank can be installed by gravity, without raising, and the treated water can be disposed of in the usual way.",
        nemtudom: "Not an obstacle: the groundwater level can be established unambiguously by an on-site survey. It goes on the list of points to clarify, and the process can continue."
      }
    },
    {
      id: "talaj", lepes: "telek",
      kerdes: "What is the soil like on the plot?",
      valaszok: [
        { id: "homokos",  cimke: "More sandy" },
        { id: "kotott",   cimke: "More heavy / clay" },
        { id: "nemtudom", cimke: "I do not know", nemtudom: true }
      ],
      magyarazat: {
        homokos:  "Free-draining soil makes disposing of the treated water simpler, and the soakaway can be smaller.",
        kotott:   "Poorly draining, clay soil is not an exclusion, but the treated water then has to be disposed of through a raised soakaway. That affects both the build and the cost.",
        nemtudom: "The soil's infiltration capacity can be established on site. It goes on the list of points to clarify, and the process can continue."
      }
    },
    {
      id: "terulet", lepes: "vizelhelyezes",
      kerdes: "How much continuous, undeveloped area is available on the plot?",
      sugo: "An approximate figure is enough — this is where the soakaway would go.",
      valaszok: [
        { id: "kicsi",    cimke: "Less than about 30 m²" },
        { id: "kozepes",  cimke: "About 30–60 m²" },
        { id: "nagy",     cimke: "More than about 60 m²" },
        { id: "nemtudom", cimke: "I do not know", nemtudom: true }
      ],
      magyarazat: {
        kicsi:    "From here on this is no longer a question of choosing a technology. If there is not enough area to dispose of the water, there is no treatment solution that “needs less space” — a sealed holding tank remains the workable direction, and a discussion is needed in any case.",
        kozepes:  "This size is generally enough for a biological system's soakaway. A septic tank's drainage field, however, is typically two to three times as large, so that direction cannot be built on an area this size.",
        nagy:     "This size permits water disposal for either direction. The exact size of soakaway required depends on the load, the soil structure and the groundwater level — the survey establishes that.",
        nemtudom: "This does not block the process: the available area goes on the list of points to clarify, and can be established unambiguously during the on-site survey."
      }
    }
  ],

  iranySzabalyok: [
    { ha: { hasznalat: ["eletvitelszeru"], kihagyas: ["honapok"] }, irany: "egyeztetes",
      ok: "permanent occupation, but with regular gaps of several months" },
    { ha: { hasznalat: ["eletvitelszeru"], letszam: ["1-2"], kihagyas: ["hetek"] }, irany: "egyeztetes",
      ok: "a permanently occupied property used by one or two people, with frequent longer absences" },
    { ha: { hasznalat: ["eletvitelszeru"] }, irany: "abclear" },
    { ha: { hasznalat: ["hetvegi"], letszam: ["5-6", "7-10", "10+"] }, irany: "egyeztetes",
      ok: "a property used almost every weekend, but by a large number of people" },
    { ha: { hasznalat: ["hetvegi"] }, irany: "epureco" },
    { ha: { hasznalat: ["szezonalis"], letszam: ["5-6", "7-10", "10+"] }, irany: "egyeztetes",
      ok: "strong seasonality: intensive use during the season, an empty property outside it" },
    { ha: { hasznalat: ["szezonalis"] }, irany: "epureco" }
  ],

  telekHatasok: [
    { ha: { talajviz: "igen" },
      feltetelek: ["kiemelt-szivarogtato", "specialis-rogzites"] },
    { ha: { talajviz: "nemtudom" }, tisztazandok: ["talajviz"] },
    { ha: { talaj: "kotott" }, feltetelek: ["kiemelt-szivarogtato"] },
    { ha: { talaj: "nemtudom" }, tisztazandok: ["talaj"] },
    { ha: { terulet: "nemtudom" }, tisztazandok: ["terulet"] }
  ],

  teruletSavok: {
    kicsi:   { biologiai: false, oldomedence: false },
    kozepes: { biologiai: true,  oldomedence: false },
    nagy:    { biologiai: true,  oldomedence: true  },
    nemtudom:{ biologiai: null,  oldomedence: null  }
  },

  feltetelek: {
    "kiemelt-szivarogtato": {
      cimke: "Raised soakaway", jel: "csepp",
      leiras: "The treated water is disposed of in a soakaway raised above ground level, so that poor drainage or a high water table does not impede infiltration."
    },
    "specialis-rogzites": {
      cimke: "Anti-flotation anchoring", jel: "horgony",
      leiras: "The tank is anchored to a concrete base so that high groundwater cannot lift it."
    },
    "gravitacios-megoldas": {
      cimke: "Separate technical solution for gravity", jel: "lejtes",
      leiras: "Where the depth of the outgoing pipe and the terrain mean a gravity arrangement will not work, a pumping station or an adjusted level arrangement is required."
    }
  },

  tisztazandok: {
    kut: {
      mindig: true, cimke: "Proximity of a well or the plot boundary",
      hogyan: "The exact protective distance cannot be given as a single figure in metres: local conditions and the permitting requirements determine it together. It can be settled by an on-site survey."
    },
    szivarogtato: {
      mindig: true, cimke: "The size of soakaway required",
      hogyan: "It depends on the expected load, the soil structure and the groundwater level. The survey establishes it, not a figure given in advance."
    },
    terep: {
      mindig: true, cimke: "The depth of the outgoing pipe and the fall of the ground",
      hogyan: "This decides whether a gravity arrangement will work. The existing pipe outlet can be inspected on site."
    },
    talajviz: {
      cimke: "Exact ground conditions",
      hogyan: "The groundwater level can be established unambiguously by an on-site survey."
    },
    talaj: {
      cimke: "The soil's infiltration capacity",
      hogyan: "The soil structure can be inspected on site; where it is in doubt, a percolation test settles it."
    },
    terulet: {
      cimke: "Free area for water disposal",
      hogyan: "The continuous, undeveloped area available on the plot can be established from the site plan or on site."
    }
  },

  termekek: {
    abclear: {
      nev: "A.B. Clear",
      rovid: "On the pattern of use this looks like the strongest direction, though the plot's conditions may still refine the recommendation.",
      indoklas: "Under a year-round, even load, active biological treatment can be sustained: the bacterial culture is fed continuously. Because of the sludge-bag arrangement the system needs no tanker emptying.",
      url: "../megoldasok/ab-clear"
    },
    epureco: {
      nev: "Epureco septic tank",
      rovid: "On the intermittent pattern of use this looks like the strongest direction, though the plot's conditions may still refine the recommendation.",
      indoklas: "A septic tank copes well with an intermittent, irregular load: it holds no active biological culture that has to be sustained, and it needs no electricity.",
      kompromisszum: "In treatment terms this is a compromise: in exchange for simpler operation that tolerates fluctuating load well, most of the treatment happens in the soil, at lower treatment performance than A.B. Clear's active biological treatment.",
      url: "../megoldasok/epureco"
    },
    zarttarolo: {
      nev: "Sealed holding tank",
      rovid: "With no means of disposing of the water, this remains the workable direction.",
      indoklas: "Where there is not enough area to dispose of the treated water, this is no longer a question of choosing a technology: without infiltration the wastewater produced has to be collected and taken away.",
      url: "../megoldasok/megoldastipusok-osszehasonlitasa"
    },
    egyeztetes: {
      nev: "Expert consultation",
      rovid: "The factors you have given contradict one another, so the module does not name a product.",
      indoklas: "The picture is mixed: the answers do not allow an automatic decision. The points below are why it is worth going through the situation in person.",
      url: "../konzultacio"
    }
  },

  tovabb: {
    elsodleges: { cimke: "See roughly what it would cost", url: "#ai-dontestamogato" },
    masodlagos: [
      { cimke: "Exclusions and limiting conditions", url: "../megoldasok/kizaro-es-korlatozo-feltetelek" },
      { cimke: "Infiltrating the treated water", url: "../megoldasok/biologiai-telek-es-terhelesi-feltetelek" },
      { cimke: "Expert consultation", url: "../konzultacio" }
    ]
  }
};
