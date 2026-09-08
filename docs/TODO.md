# Audit webu — stav úprav

8. září 2026. Poslední verze `43b4b16` byla nasazena přes GitHub na nocode23.com. Cloudflare Pages potvrdilo úspěch; ověřeno všech 14 veřejných HTML stránek. Stručný changelog je v `docs/CHANGELOG.md`.

## Hotovo v této verzi

- [x] P0: Archivovaný známý chybný lokální pre-push hook Daily Routines. Nový verzovaný publikační skript posílá podprojekty před hlavním repem, při chybě se zastaví a odmítá cizí staged změny.
- [x] P0: Opraveno osm App Store odkazů v EN/CS support a privacy Daily Routines.
- [x] P0: Sjednocená synchronizace a mazání dat v EN/CS homepage, support a privacy Daily Routines. Ověřeno proti místní implementaci CloudKit a popisu releasu 1.4.
- [x] P0: Opravená tvrzení Limits o koši, WebKit úložišti, autentizaci a rozsahu čtených dat podle zdrojového kódu. Text doporučuje Disconnect a neslibuje vymazání všech dat odinstalací.
- [x] P1: Projekty před sekcí O projektu; kratší úvod a popisy konkrétního přínosu všech pěti projektů. Knihy Primus zařazeny jako e-shop.
- [x] P1: Názvy, odkazy, ikony, popisy a počty mají společný zdroj v apps.json. Generátor ukládá přímo HTML, není nutné čekat na JS/fetch.
- [x] P1: Náhled DJ Matty nahrazen existujícím čitelným projektovým vizuálem; Knihy Primus používají skutečný malý náhled celé homepage e-shopu místo obálek knih.
- [x] P1: Aktualizovaná hlavní dokumentace a označený historický brief Limits.
- [x] P1: Kontrolní skript pro všechny stránky a připravená šablona GitHub Actions workflow.
- [x] P2: Daily Routines zahrnuté do sitemap, absolutní canonical/hreflang. České portfolio vede na české produktové weby; český App Store badge.
- [x] P2: Ikona Daily Routines z přibližně 1 MB na 23,4 kB pro webové použití.
- [x] P2: Nativní dialog galerie, české názvy tlačítek, Escape, fokus a návrat na původní ovládací prvek. Mobilní menu správně aktualizuje svůj stav.
- [x] P2: Viditelnost obsahu bez JS, preference omezení pohybu, FAQ přístupné bez JS a při spuštěném JS odpovědi svázané s tlačítky.
- [x] P2: Limits nabízí skutečný screenshot panelu, přímé stažení ZIP a instalační postup; verze odkazuje na aktuální release.
- [x] P2: Daily Routines doplněno o skutečný screenshot iPadu ve světlé i tmavé variantě.
- [x] P2: Opravené přetékání velkého loga a zalamování navigace homepage na mobilu.
- [x] P2: Sjednocená výška ohraničených karet Lacto Tracker a Daily Routines & Habits.

## Ověření

- `python3 scripts/verify.py`: 14 HTML stránek; lokální soubory, kotvy, download CTA, metadata, sitemap a 5 projektů.
- `node --check`: všechny čtyři hlavní JS soubory.
- Pět integračních testů publikování s dočasnými lokálními Git remotes: správné pořadí, odmítnutí pushnutí dítěte, ochrana staged změn, dry run a odmítnutí starého hooku.
- `git diff --check` v rodiči i všech třech submodulech.
- Safari: desktopové projektové karty, česká galerie včetně přesunu fokusu a Escape; mobilní šířka 390 px — homepage, Daily Routines a Limits; otevření mobilního menu Daily Routines.
- Přímý odkaz Limits.zip vrací po přesměrování HTTP 200.

## Zbývající práce

- [ ] P1: Aktivovat šablonu GitHub Actions po zajištění oprávnění `workflow`; lokální kontrolní a publikační skript fungují již nyní.

- [x] P1: Publikovat připravenou verzi a ověřit nasazení na Cloudflare — dokončeno 7. září 2026 (`f0721c5`). GitHub workflow zatím není aktivní; OAuth přihlášení nemá scope `workflow`. Šablona zůstává v `docs/workflows/verify.yml`.
- [ ] P1: Nastavit v Cloudflare build command pro blokování chybného nasazení (viz STRUCTURE.md). Lokální skript a GitHub workflow toto nastavení samy nemění.
- [ ] P2: Nové české screenshoty Daily Routines a screenshot widgetu. Dostupná sada je anglická; nepřekreslovat rozhraní uměle.
- [ ] P2: Doplnit skutečnou krátkou ukázku menu baru a Docku Limits bez osobních údajů.
- [ ] P2: Podrobnější případové studie s vlastními zkušenostmi autora a doloženými výsledky; současná verze používá pouze ověřitelné popisy realizací.
- [ ] P2: Rozšířená kontrola na skutečném iPhonu/iPadu, při 200% textu a se čtečkou obrazovky. Kontrola Safari Responsive Design není test na fyzickém zařízení.
- [ ] Samostatný projekt: redakční úpravy živého e-shopu Knihy Primus (tvary počtů titulů, úvodní texty, důraz na katalog). Změny v tomto repu upravují jeho portfolio prezentaci, nikoli WordPress e-shop.

## Zdroje nových obrazových podkladů

- DJ Matty: existující `djmatty/images/og-image.jpg`, kopie jako `www/assets/images/preview-djmatty.jpg`.
- Knihy Primus: existující screenshot homepage `www/assets/images/shot-knihyprimus.jpg`.
- iPad: existující `Again/apple_connect/screenshots/ipad/02_dashboard.png` a tmavá varianta; optimalizováno pro web.
- Limits: již existující `assets/images/screenshot-panel.png`.
