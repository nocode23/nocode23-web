# STRUCTURE.md

Živá dokumentace projektu nocode23.com.

## Adresářový strom

```
nocode23.com/
  www/                        ← web root (nasazuje se na Cloudflare Pages)
    index.html
    robots.txt
    sitemap.xml
    assets/
      css/main.css
      js/main.js
      images/
        logo-djmatty.png      ← lokálně stažené logo
        logo-knihyprimus.png  ← lokálně stažené logo
    data/
      apps.json               ← jediný zdroj pravdy o všech aplikacích
    lacto-tracker/            ← git submodule (github.com/nocode23/lacto-tracker-web)
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
  shared/                     ← sdílené assety (zatím prázdné)
  docs/
    STRUCTURE.md              ← tento soubor
  .vscode/
    settings.json             ← liveServer.settings.root = /www
  CLAUDE.md
```

## Hosting a deployment

- **Cloudflare Pages** — projekt `nocode23-web`, output: `www/`
- **GitHub** — `github.com/nocode23/nocode23-web` (public)
- **DNS** — na Cloudflare (přesunuto z czechia.cz)
- **Doména** — registrována na czechia.cz
- **Auto-deploy** — git push → Cloudflare Pages nasadí automaticky

## Aplikace

| ID            | Název         | Stav | GitHub repo            | App Store ID |
|---------------|---------------|------|------------------------|--------------|
| lacto-tracker | Lacto Tracker | live | nocode23/lacto-tracker-web (public) | 6760203009 |

## Changelog

| Datum      | Změna |
|------------|-------|
| 2026-06-07 | [www] Migrace — index.html a assets/ přesunuty do www/, vytvořena struktura www/data/apps.json, shared/, docs/ |
| 2026-06-07 | [www] lacto-tracker jako git submodule (github.com/nocode23/lacto-tracker-web) |
| 2026-06-07 | [www] Cloudflare Pages nasazen, DNS přesunuto na Cloudflare |
| 2026-06-07 | [www] Meta tagy, Lucide ikony v bento tagech, t-green barva pro hosting/infra |
| 2026-06-07 | [www] Loga DJ Matty a Knihy Primus stažena lokálně do assets/images/ |
