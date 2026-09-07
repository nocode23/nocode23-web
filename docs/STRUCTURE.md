# Struktura nocode23.com

Aktualizováno 7. září 2026. Statické HTML/CSS/JS bez frameworku a bez povinného buildu.

## Repozitáře a hosting

- Hlavní repo: `nocode23/nocode23-web`, větev `main`.
- Cloudflare Pages: projekt `nocode23-web`, veřejný adresář `www/`.
- Push hlavního repozitáře spouští nasazení podle stávajícího propojení Cloudflare Pages.
- Přesné nastavení a výsledek nasazení ověř v Cloudflare; úspěšný Git push sám nepotvrzuje úspěšný deploy.
- Tři produktové weby jsou připnuté git submoduly. Jejich vlastní push neposune odkaz hlavního repozitáře.
- DJ Matty a Knihy Primus jsou externí weby; tento repozitář spravuje pouze jejich prezentaci v portfoliu.

| Adresář | Repo | Obsah |
| --- | --- | --- |
| `www/` | nocode23-web | České portfolio, společná sitemap a robots.txt |
| `www/lacto-tracker/` | lacto-tracker-web | EN `index.html`, CS `index-cs.html`, obě privacy |
| `www/daily-routines-and-habits/` | daily-routines-habits-web | Routing dle jazyka, `cs/` a `en/`: index, privacy, support |
| `www/limits/` | limits-web | EN produktová stránka a privacy; aplikace samotná v `nocode23/limits` |

Lacto Tracker: App Store `6760203009`. Daily Routines & Habits: App Store `6775655422`. Obě aplikace jsou zveřejněné. Limits se distribuuje přes GitHub Releases.

## Soubory a obsah

- `www/data/apps.json`: metadata všech pěti projektů (pole `projects`).
- `scripts/sync-projects.py`: přenese názvy, odkazy, ikony, popisy a počty do označených bloků `www/index.html`; stránka nepotřebuje JS pro načtení projektů.
- `scripts/verify.py`: kontrola 14 HTML stránek, lokálních souborů a kotev, App Store CTA, canonical/hreflang, sitemap a shody s přehledem projektů.
- `scripts/publish.py`: publikování commitnutých podprojektů před hlavním repozitářem; bez `--publish` pouze kontroluje stav.
- `scripts/retire-legacy-hook.py`: jednorázově archivuje přesně známý chybný lokální pre-push hook. Jiného hooku se nedotkne.
- `www/assets/`: styl, skripty, fonty a portfolio obrázky.
- Produktové weby mají samostatné `assets/` a zachovávají vlastní vizuální styl.
- `WEBSITE.md`: historický brief Limits, nikoli aktuální popis produktu. Aktuální text je v `www/limits/`.

## Automatické kontroly

Šablona `docs/workflows/verify.yml` je připravená pro kontrolu hlavní větve a pull requestů včetně rekurzivního checkoutu submodulů. Zatím není aktivní: současné GitHub OAuth přihlášení nemá scope `workflow` a server odmítl přidání do `.github/workflows/`. Po doplnění oprávnění přesuň šablonu do `.github/workflows/verify.yml` a pushni ji. Workflow samo nemění nastavení Cloudflare a není automatickou bránou přímého Pages nasazení. Před publikováním proto probíhá lokální ověření; pro blokování chybného deploye nastav v Cloudflare build command `python3 scripts/verify.py` při root directory repozitáře a output directory `www`. Toto nastavení zatím nebylo změněno.

## Úpravy a kontrola

```sh
python3 scripts/sync-projects.py
python3 scripts/verify.py
python3 -m unittest discover -s tests
python3 -m http.server 8765 --bind 127.0.0.1 --directory www
```

Nový projekt: přidej metadata a jeden pár komentářů `project:ID:start` / `project:ID:end` do portfolia, potom spusť synchronizaci. Vizuál a umístění karty se upravují v HTML/CSS. Přidání nové aplikace znamená také doplnění submodulu a seznamu `MODULES` v publish skriptu.

## Publikování

1. Uprav a zkontroluj web. Commitni změny v každém upraveném podprojektu; poté commitni soubory hlavního repozitáře. Do commitu ber jen změny určené k vydání.
2. Jednorázově spusť `python3 scripts/retire-legacy-hook.py`, pokud tato kopie ještě obsahuje starý hook Daily Routines.
3. Spusť `python3 scripts/publish.py` pro kontrolu. Vyžaduje čisté pracovní stromy, větev `main` a prázdný index hlavního repozitáře; připouští pouze změněné odkazy submodulů.
4. `python3 scripts/publish.py --publish` pushne postupně všechny tři podprojekty a ověří jejich zveřejněné SHA. Teprve poté commitne změněné odkazy a pushne hlavní repo. Při neúspěchu se zastaví. Neprovádí force push ani automatické slučování.
5. Ověř výsledek Cloudflare Pages a živé stránky včetně obou jazyků, podpory a tlačítek ke stažení.

Skript nepřebírá jiné staged změny, nespouští starý cross-repo hook a neobchází neznámé hooky. Současné publikování ze dvou pracovních kopií není podporované; git odmítnutí řeš před dalším spuštěním.

## Obsahová kontrola při změně aplikace

Funkce, kompatibilita, data a mazání se musí shodovat s vydanou aplikací. Při změně iCloudu nebo účtů projdi homepage, support a privacy v EN i CS. Screenshoty mají být skutečné a bez osobních dat. Nevytvářej smyšlené reference ani výsledky projektu.
