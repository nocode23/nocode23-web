# Přehled změn webu

Tento soubor je rychlý orientační záznam změn hlavního repozitáře `nocode23/nocode23-web`. Detailní důvody a otevřené úkoly jsou v `docs/TODO.md`; pravidla struktury a publikování v `docs/STRUCTURE.md`.

## 8. září 2026

- `43b4b16` — sjednocená výška odkazových karet Lacto Tracker a Daily Routines & Habits. Delší název už kartu neroztahuje.
- `16a786c` — upravený náhled Knihy Primus: větší prostor pro screenshot celé homepage, odstraněné zbytečné vnitřní odsazení a čistší browser preview.
- `823ad3e` — nahrazené tři náhledy obálek jedním malým náhledem celého e-shopu Knihy Primus.

## 7. září 2026

- `f460a3d` — zapsané a ověřené produkční nasazení předchozí verze.
- `f0721c5` — hlavní auditní úprava webu: struktura homepage, texty a metadata projektů, dostupnost, responzivita, skutečné vizuály, kontrolní skripty a bezpečnější publikování submodulů.

## Jak změny publikovat

Hlavní repo obsahuje portfolio v `www/` a tři produktové weby jako git submoduly. Pro kontrolu použij `python3 scripts/verify.py`. Pro publikování přes GitHub použij `python3 scripts/publish.py --publish`; skript nejdřív publikuje submoduly a potom hlavní repo. Push hlavního repa spouští nasazení přes existující Cloudflare Pages propojení.

Po každém pushi ověř veřejnou stránku a stav Cloudflare Pages. GitHub historie je zdroj technických detailů; tento soubor je stručný lidský přehled, aby se při další práci nemuselo hledat v jednotlivých commitech.
