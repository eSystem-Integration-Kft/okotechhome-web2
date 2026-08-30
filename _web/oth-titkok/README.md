# oth-titkok

Ide kerülnek az API-kulcsok és a CRM-titkok — **egy fájl, egy titok**, semmi más,
még üres sor sem: az `oth_titok()` a fájl teljes tartalmát olvassa be, tehát egy
odabiggyesztett második sor mindkét kulcsot használhatatlanná teszi.

## Hova tedd

**A WEBGYÖKÉR FÖLÉ.** Nem a `public_html`-be és nem a `tst.okoth.hu`-ba, hanem
melléjük:

```
okoth.hu/
├── oth-titkok/        ← IDE
├── public_html/       ← az okoth.hu gyökere
└── tst.okoth.hu/      ← a teszt-oldal gyökere
    └── api/           ← innen keresi a kód: ../../oth-titkok/
```

Ami nincs a dokumentumgyökérben, azt a webszerver ki sem tudja szolgálni — nem
`.htaccess`-re bízzuk. A könyvtárban lévő `.htaccess` csak védőháló arra az
esetre, ha a mappa mégis a gyökérben marad; nginx alatt le sem fut.

## Fájlok

| fájl | mire való |
|---|---|
| `ai-kulcs.txt` | Anthropic API-kulcs az ajánlat-elemzéshez |
| `crm-kapcsolat.txt` | a kapcsolati űrlap CRM-titka |
| `crm-arsav.txt` | az ársávbecslő és a névtelen ügyrekordok titka |
| `crm-ajanlo.txt` | a megoldás-ajánló titka |
| `crm-osszehasonlito.txt` | az ajánlat-összehasonlító titka |
| `crm-konzultacio.txt` | a konzultációkérő titka |

Jogosultság: `chmod 600`, a tulajdonos a webszerver felhasználója.

## Ha kiszivárgott

A titok cseréje egy lépés: a CRM-ben **Beállítások → Beérkező űrlapok → Új
titok**. A régi AZONNAL érvénytelen lesz — nincs átfedési idő, mert aki cserél,
azért teszi, mert a régi kikerült valahova.

Az AI-kulcsot az Anthropic Console-ban kell visszavonni és újragenerálni.
