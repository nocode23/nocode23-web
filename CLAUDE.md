# Práce na nocode23.com

Statické portfolio v `www/`, čisté HTML/CSS/JS. Existující hosting je Cloudflare Pages propojený s GitHubem `nocode23/nocode23-web`; zachovej jej. Aktuální struktura a publikování: `docs/STRUCTURE.md`.

- Tři podwebové repozitáře jsou git submoduly: Lacto Tracker, Daily Routines & Habits, Limits.
- Před změnami ověř `git status` v hlavním repu i dotčeném submodulu. Nezahrnuj cizí rozpracované změny.
- `www/data/apps.json` obsahuje metadata všech projektů. Označené projektové bloky a počty v homepage generuje `python3 scripts/sync-projects.py`. Po úpravách spusť `python3 scripts/verify.py`.
- Publikování: `python3 scripts/publish.py` nejprve provede kontrolu bez zápisu. Parametr `--publish` posílá commitnuté podprojekty před rodičem. Nepublikuj rodiče z pre-push hooku dítěte.
- Homepage: úvod → projekty → o projektu → technologie. Zachovej pojetí osobní laboratoře a existující vizuální identitu. Žádné nevyžádané kontaktní nebo agenturní sekce.
- Syne, Outfit, JetBrains Mono; tmavé pozadí, barevné akcenty. Každá aplikace má vlastní styl.
- Na `.card` nepřidávej `overflow: hidden` kvůli Safari/backdrop-filter. Dekorativní pseudo-elementy nesmí blokovat klikání.
- Obsah musí být čitelný bez JS. Respektuj `prefers-reduced-motion` a ovládání klávesnicí.
- V češtině používej jednotné tykání. Z českého portfolia odkazuj na české verze, pokud existují.
- Veřejný kontakt: `support@nocode23.com`. Nepřidávej osobní e-mail ani osobní jméno do marketingových textů.
- Claims o datech, účtech a mazání ověř proti aplikaci. EN/CS homepage, support a privacy musí být konzistentní.
- DJ Matty a Knihy Primus jsou externí projekty. Jejich živé weby se nepublikují z tohoto repa.
- `WEBSITE.md` je historický brief Limits; není zdrojem pravdy pro aktuální privacy ani distribuční informace.
