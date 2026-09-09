## Mi változott

<!-- Egy-két mondat arról, MI a változás, és MIÉRT. A „hogyan" a diffben van. -->

## Érintett terület

- [ ] `_web/` — webkimenet (HTML / CSS / JS)
- [ ] `_web/api/` — PHP-végpontok
- [ ] `scripts/oldalgyartas/` — oldalgenerátorok
- [ ] Dokumentáció (`README`, `CHANGELOG`, `COMPONENTS`, `VERSIONING`)
- [ ] Kiadás / verziózás

## Ellenőrzés

- [ ] `bash scripts/ellenorzes.sh` hibátlanul lefut
- [ ] Helyben megnézve: `cd _web && python3 serve.py` → <http://localhost:8849>
- [ ] **Világos ÉS sötét témában** rendben van
- [ ] Billentyűzettel végigjárható, a fókusz látszik
- [ ] `prefers-reduced-motion` mellett sem mozog semmi fölöslegesen
- [ ] Ha stíluslap vagy modul változott: a `?v=NN` cache-buster megemelve
- [ ] Ha generátor változott: a generált lapok újragyártva és commitolva

## Ami NEM mehet bele

- [ ] Nincs titok a diffben (API-kulcs, SMTP-jelszó, `config.php`)
- [ ] Nincs `_memory/`, `_work/`, `_files/`, `_kepek_videok/` tartalom
