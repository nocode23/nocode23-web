# STRUCTURE.md

Živá dokumentace projektu nocode23.com.

## Adresářový strom

```
nocode23.com/
  www/                        ← web root (vše co se nasazuje na server)
    index.html
    assets/
      css/main.css
      js/main.js
    data/
      apps.json               ← jediný zdroj pravdy o všech aplikacích
    lacto-tracker/            ← micro-site aplikace (scope: lacto-tracker)
      index.html              ← EN verze
      index-cs.html           ← CS verze
      privacy-policy.html
      privacy-policy-cs.html
      sitemap.xml
      assets/
        css/main.css
        js/main.js
        fonts/
        images/
  shared/                     ← sdílené CSS a assety (zatím prázdné)
  docs/
    STRUCTURE.md              ← tento soubor
  .vscode/
    settings.json             ← liveServer.settings.root = /www
  CLAUDE.md
  robots.txt
  sitemap.xml
```

## Aplikace

| ID              | Název          | Stav | App Store ID |
|-----------------|----------------|------|--------------|
| lacto-tracker   | Lacto Tracker  | live | 6760203009   |

## Changelog

| Datum      | Změna |
|------------|-------|
| 2026-06-07 | [www] Migrace — index.html a assets/ přesunuty do www/, vytvořena struktura www/data/apps.json, shared/, docs/ |
| 2026-06-07 | [www] lacto-tracker/ přesunuto do www/, cesty opraveny, .vscode/settings.json přidán pro Live Server |
| 2026-06-07 | [lacto-tracker] integrován do hlavního repo (odstraněn vlastní .git), nasazen na nocode23.com/lacto-tracker/ |
