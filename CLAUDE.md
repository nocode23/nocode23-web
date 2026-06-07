# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Static website **nocode23.com** — osobní portfolio/laboratoř Petra Primuse experimentující s AI a vibe codingem. Čistý HTML/CSS/JS, žádný framework, žádný build step. Hostování: Wedos. Doména: nocode23.com.

## Struktura

```
nocode23.com/
  index.html              ← hlavní portfolio stránka
  sitemap.xml
  robots.txt
  lacto-tracker/          ← podstránka pro iOS aplikaci Lacto Tracker
    index.html            ← EN verze
    index-cs.html         ← CS verze
    privacy-policy.html
    privacy-policy-cs.html
    sitemap.xml
    assets/
      css/main.css        ← veškeré styly lacto-tracker sekce
      js/main.js          ← sticky showcase logika (IntersectionObserver)
      fonts/              ← self-hosted: Plus Jakarta Sans + JetBrains Mono (woff2)
      images/             ← screenshoty aplikace, App Store badge, app ikona
```

## Design systém — index.html

- **Pozadí:** `#07070e` (near-black)
- **Fonty:** Syne (display, Google Fonts) + Outfit (body) + JetBrains Mono
- **Akcenty:** `--blue: #4F8EF7`, `--violet: #9B59F5`, `--cyan: #22d3ee`
- **Blobové pozadí:** třídy `.bl1`–`.bl4` (pozor: `.b1`–`.b3` jsou bento karty — neplést!)
- **Bento grid:** 12 sloupců, karty `.b1` (span 5), `.b2` (span 7), `.b3` (span 12)
- **Hover glow:** `::after` pseudo-element musí mít `pointer-events: none` jinak blokuje klikání

## Design systém — lacto-tracker/

- **Fonty:** Plus Jakarta Sans (variable 200–800, self-hosted) + JetBrains Mono (self-hosted)
- **Akcent:** `--orange: #F5891F` (barva aplikace)
- **Sticky showcase:** JS v `assets/js/main.js` přepíná screenshoty telefonu při scrollu

## Projekty v bento gridu

### App · iOS (`.b1`)
- **Lacto Tracker** — sledování kojení, App Store ID `6760203009`
  - Stránka: `lacto-tracker/index.html`
  - App Store: `https://apps.apple.com/app/lacto-tracker/id6760203009`

### Web (`.b2`)
- **DJ Matty** — prezentační web pro profesionálního DJ
  - URL: `https://www.djmatty.cz/`

### Grafika (`.b3`)
- **Knihy Primus** — kompletní redesign rodinného e-shopu nakladatelství
  - URL: `https://www.knihyprimus.cz`

## Přidání nového projektu

Každý projekt v bento kartě je `<a href="..." class="feat-project">` blok obsahující:
- `.feat-logo` — 36×36px obrázek nebo div s emoji
- `.feat-name` — název projektu
- `.feat-sub` — jednořádkový popis
- Šipka `→` (interní) nebo `↗` (externí odkaz)

Před prvním projektem v kartě přidat `<div class="feat-divider">Spuštěno</div>`.

## Důležité technické poznámky

- `overflow: hidden` na `.card` **nesmí být** — způsobuje ořez obsahu v Safari při kombinaci s `backdrop-filter`
- `::after` glow efekt musí mít `pointer-events: none` — jinak blokuje klikání na odkazy
- Blob třídy jsou `.bl1`–`.bl4`, bento slot třídy jsou `.b1`–`.b3` — nikdy neplést
- Live server funguje — není třeba otvírat soubory přes `open` příkaz po každé editaci
- Uživatel mluví česky, odpovídej česky

## Nástroje v sekci Technologie

Claude AI, Claude Code, ChatGPT, Codex, Visual Studio Code, Swift/SwiftUI, Xcode, Raycast, TestFlight, App Store Connect, GitHub, GitHub Pages, Wedos Hosting — vše jako `<a class="t-tag">` s odkazem, `target="_blank" rel="noopener"`.
