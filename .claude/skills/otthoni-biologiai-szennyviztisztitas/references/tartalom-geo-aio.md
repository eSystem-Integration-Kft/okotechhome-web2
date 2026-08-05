# Tartalmi stratégia: GEO / AIO / SEO (szennyvíztisztítás)

Referencia a meta-szövegekhez, GYIK-hez, blogtervhez és strukturált adathoz. Cél: a látogatók informálása +
leadgenerálás, és hogy az **AI-keresők (ChatGPT / Perplexity / Gemini)** idézzék az oldalt.

## Top vásárlói kérdések (HU) — magas vásárlási szándék
1. Melyik a legjobb házi szennyvíztisztító kisberendezés családi házhoz?
2. Mennyibe kerül egy biológiai szennyvíztisztító telepítéssel együtt? (ár, adott év)
3. Szennyvíztisztító vs. zárt emésztő — melyik éri meg jobban?
4. Kell-e szippantani a biológiai szennyvíztisztítót?
5. Milyen engedély kell? (vízjogi / jegyzői, 500 m³/év határ)
6. Megtérül-e, és mennyi idő alatt?
7. Mennyi áramot fogyaszt / mennyi a havi költség?
8. SBR vagy MBBR vagy eleveniszapos — mi a különbség?
9. Hová lehet vezetni a tisztított vizet? (elszivárogtatás, öntözés)
10. Működik-e nyaralóhoz, idényhasználatra?
11. Milyen tisztítószert szabad használni? (klórmentes, biológiailag lebomló)
12. Milyen karbantartást igényel? (membrán-, kompresszorcsere)
13. Mekkora hely / milyen talaj kell hozzá?
14. Van-e rá állami támogatás? (otthonfelújítás / KAP — ellenőrizni)
15. Mennyi a tisztítási hatásfok / megfelel-e a határértékeknek?

## Kulcsszó-klaszterek
- **HU:** házi/egyedi szennyvíztisztító, biológiai szennyvíztisztító kisberendezés, szennyvíztisztító ár,
  emésztő kiváltása, csatornázatlan terület, szennyvíz öntözés, szippantásmentes, vízjogi engedély,
  eleveniszapos / SBR / MBBR szennyvíztisztító.
- **EN:** domestic / small sewage treatment plant, off-mains drainage, septic tank replacement, SBR vs septic,
  sewage treatment plant cost, EN 12566-3.
- **DE:** Kleinkläranlage Preis, SBR Kläranlage, Abwasser ohne Kanalanschluss, Hauskläranlage, EN 12566-3 Zulassung.

## Hogyan idéznek az AI-keresők — és mit jutalmaznak
Az AI-motorok a témát **technológiatípus + LE-tartomány + szabványmegfelelés (EN 12566-3, CE)** mentén foglalják
össze, és **tárgyilagos, összehasonlító** választ adnak. Idézést az alábbi tartalom nyer:
- **Strukturált GYIK** — Q→A párok, `schema.org/FAQPage` jelöléssel.
- **Konkrét műszaki specifikáció táblázatban** (LE, teljesítmény W, iszap m³/év, hatásfok %), nem marketing.
- **Szabvány- és engedélyhivatkozás** (EN 12566-3, CE; vízjogi/jegyzői eljárás, 500 m³/év).
- **Költség/megtérülés** valós számokkal (beruházás, éves fenntartás, megtérülési idő).
- **Tárgyilagos összehasonlító táblák** (oldómedence vs. biológiai; SBR vs. MBBR vs. fixágyas).
- **E-E-A-T jelek:** gyártói státusz, díjak (Construma 2014), CE/ISO, telephely (Esztergom), referenciák, 20+ év.

## Ajánlott oldalankénti tartalmi recept
1. **H1** a fő keresési szándékkal (pl. „Biológiai szennyvíztisztító kisberendezés 1–50 főig").
2. Rövid, **közvetlen válasz-bekezdés** a fő kérdésre (AI-snippet-barát, 40–60 szó).
3. **Specifikációs tábla** (LE, W, iszap m³/év, hatásfok %, méret, anyag).
4. **Előnyök** tárgyilagosan + **mire NEM jó** (őszinteség → bizalom + idézhetőség).
5. **Összehasonlító tábla** versenytechnológiával.
6. **Engedély/jog** rövid blokk (vízjogi/jegyzői, 500 m³/év, talajterhelési díj mentesség).
7. **GYIK** (5–8 kérdés) `FAQPage` schema-val.
8. **CTA**: ajánlatkérés (telek adatai), telefon, e-mail — több ponton.

## Strukturált adat (schema.org) minták
Minden oldalon javasolt: `Organization`/`LocalBusiness`, terméknél `Product` (+ ha van valós értékelés:
`AggregateRating` — csak hiteles, igazolható adattal!), GYIK-nél `FAQPage`, telepítési útmutatónál `HowTo`.

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Kell-e szippantani a biológiai szennyvíztisztítót?",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "A biológiai szennyvíztisztító jóval ritkábban igényel ürítést, mint a zárt emésztő. Az Ökotech-Home szabadalmaztatott iszapzsákos technológiájával gyakorlatilag szippantásmentes: a fölösiszap a zsákban gyűlik, kivehető és komposztálható."
    }
  }]
}
```

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Ökotech-Home Kft.",
  "image": "https://okotechhome.hu/.../logo-oko-245x90-normal-2.png",
  "telephone": "+36 33 200 211",
  "email": "kapcsolat@okotechhome.hu",
  "address": {"@type": "PostalAddress","streetAddress": "Strázsa utca 12.","addressLocality": "Esztergom","postalCode": "2509","addressCountry": "HU"},
  "areaServed": "HU",
  "award": "Construma Nagydíj 2014"
}
```

## Többnyelvű (GEO nemzetközi)
- `hreflang` minden nyelvi változatra (`hu`, `en`, `de`, + `x-default`).
- Nyelvenként **lokalizált kulcsszó** (ne tükörfordítás) — lásd `glosszarium-tobbnyelvu.md`.
- DE piacon emeld ki: EN 12566-3 + (ahol releváns) DIBt; AT-nál ÖNORM B 2502. Lásd `eu-nemzetkozi.md`.

## llms.txt / AIO technikai
- Tegyél `llms.txt`-t a gyökérbe a fő oldalak + 1 soros leírásukkal, hogy az LLM-ek könnyen feltérképezzék.
- Tartsd a fő tényeket (LE, hatásfok, szabvány, engedély, elérhetőség) **gépi olvasásra is** tisztán,
  táblázatban és FAQ-ban — ez növeli az AI-idézés esélyét.

## Pontosság = idézhetőség
Az AI-keresők a megbízható, ellenőrizhető tartalmat idézik. Tartsd be a `SKILL.md` „Pontossági korlátok"
szakaszát (VITUKI nem aktuális; EN 12566-3 nincs egységes határérték; N/P csak célzott eljárással; 30/2008 a
helyes műszaki rendelet; tisztított víz korlátai). A téves állítás idézhetetlen — vagy ami rosszabb, rossz
fényt vet a cégre.
