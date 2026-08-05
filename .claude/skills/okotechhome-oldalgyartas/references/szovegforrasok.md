# Szöveg- és adatforrások

**Alapszabály:** számot, jogszabályt, szabványt, terméktulajdonságot, árat **sosem írsz
emlékezetből**. Vagy az alábbi forrásokból jön, vagy jelölöd, hogy hiányzik.

## Ami megvan

| Forrás | Mit tartalmaz | Hol |
|---|---|---|
| **Főoldal-szöveg (végleges)** | mind a 15 főoldali szekció szövege | `/Users/mb/Desktop/Okoteh-Home.fooldal.szoveg-vagleges.docx` |
| **Sitemap** | a teljes oldalszerkezet, 402 elem | `/Users/mb/Desktop/Site map.docx` → `references/sitemap.md` |
| **Szakmai tudásbázis** | szabványok, HU jog, EU-keret, piac, glosszárium (HU/EN/DE), GEO/AIO | `otthoni-biologiai-szennyviztisztitas` skill |
| **Döntéstámogató modulok leírása** | a 4 AI-modul célja, kérdései, kimenetei | `_files/okotechhome-dontestamogato-modulok.docx` |
| **Stratégia** | pozicionálás, célközönség, üzenetek | `_files/okotechhome-strategia.html` |
| **Régi weboldal kivonata** | pozicionálás, működési leírás, előnyök | `_OkoTechHome/_cowork/work/_original/pages/` |
| **Médiaeszközök** | renderek, videók, logó | `_kepek_videok/` + `ASSET-MANIFEST.md` |

## Ami HIÁNYZIK — kérni kell

Ezek nélkül a termékoldalak (`A.B.Clear termékcsalád`, `EPURECO termékcsalád`) és a
műszaki aloldalak **nem építhetők meg hitelesen**:

| Hiányzó adat | Mire kell | Honnan jöhet |
|---|---|---|
| **A.B. Clear modellek**: típusjel, LE-kapacitás, névleges napi terhelés, tartályméret, tömeg, betáplálás mélysége | „Modellek és kapacitások", „Műszaki adatok" | gyártói adatlap |
| **A.B. Clear teljesítmény**: BOI5 / KOI / lebegőanyag kilépő értékek, hatásfok, energiafogyasztás | „Kibocsátási értékek", „Energiafogyasztási adatok" | EN 12566-3 vizsgálati jegyzőkönyv |
| **CE / DoP** | „Tanúsítványok és dokumentumok" | teljesítménynyilatkozat (PDF) |
| **EPURECO modellek**: típus, térfogat, LE, méretek | „Modellek és kapacitások" | gyártói/forgalmazói adatlap |
| **Szikkasztómező méretezése**: talajtípusonkénti fajlagos terhelés, területigény | „Tisztítómező és területigény" | méretezési táblázat |
| **Iszapzsák**: kapacitás, ürítési gyakoriság, szabadalmi szám(ok) | „Iszapzsákos technológia", „Szabadalmi dokumentumok" | szabadalmi okirat |
| **Alkatrészek, kopó elemek**: kompresszor típusa, membrán élettartama, árak | „Alkatrészre van szükségem", üzemeltetési költség | szerviz-lista |
| **Ársávok jóváhagyása** | 8. szekció modulja | `_web/assets/data/aidt-konfig.js` — jelenleg placeholder |
| **Referenciák**: helyszín, kapacitás, év, engedélyezési háttér | „Eredmények és bizonyítékok" | cégnyilvántartás |

> A régi weboldal maga is jelzi ezt a hiányt: *„(LE) · ár · a szikkasztó mező méretezési
> táblázata → gyártói/forgalmazói dokumentációból."*

## Hogyan jelöld a hiányt

Ha egy szekcióhoz nincs adat, **ne találj ki és ne kerekíts**. A HTML-be tedd be a
szekció vázát, és a forrásba egy jól kereshető jelölést:

```html
<!-- ADATHIÁNY: A.B. Clear modelltábla — gyártói adatlap kell (típusjel, LE, méret, tömeg).
     Addig ez a szekció nem publikálható. -->
```

Az összegyűjtött hiányokat vezesd a `_web/README.md` „Hiányzik" táblájába is.

## Szöveghangnem (a stratégiából)

- **Nem eladunk, hanem eligazítunk.** A látogató bizonytalan, nem terméket keres, hanem
  biztonságot a döntéshez.
- **Kimondjuk, ha nem a mi rendszerünk a jó.** Ez a cég ígérete — a „mikor nem megfelelő"
  szekció ezért kötelező.
- **Ár helyett tényezők.** Végleges árat csak helyszíni felmérés után adunk; a modulok
  nagyságrendet és költségmozgatókat mutatnak.
- **Magyar, magázó, tárgyszerű.** Nincs felkiáltójel, nincs marketingszuperlatívusz.
- Szám mellé mindig kontextus: *„háromfős háztartásnál, napi 135 l/fő fogyasztással"*.
