# Podklad pro web appky Limits

Tohle je obsahový brief pro stavbu jednostránkového webu (landing page) pro
macOS appku **Limits** — ne hotová stránka, ale text a struktura, ze které
lze web postavit (statický HTML/Squarespace/Framer/cokoliv).

Screenshot appky (`website-preview.png`) sem do kořene repa ještě doplň
ručně — automatický screenshot se nepovedl kvůli chybějícímu oprávnění
Screen Recording pro terminál. Doporučené místo záběru: hlavní okno appky
(`ContentView`), ne jen menu bar dropdown — na webu působí lépe celé okno
s oběma providery.

## Doporučená struktura stránky

1. Hero (název, jedna věta, screenshot, tlačítko ke stažení)
2. Funkce (3–4 karty)
3. Jak to funguje (krátké technické vysvětlení + upozornění na křehkost)
4. Privacy (plný text níže)
5. Stažení / požadavky
6. Patička (verze, odkaz na GitHub pokud bude veřejný)

---

## 1. Hero

**Nadpis:** Limits

**Podnadpis:** Sleduj, jak blízko jsi limitu Claude a ChatGPT — přímo z menu
baru.

**Popisek (1–2 věty):** Limits je malá macOS appka pro menu bar, která
ukazuje, kolik ti zbývá z Claude (5hodinové a týdenní okno) a ChatGPT
(primární/sekundární rate-limit okno) — na jedno kliknutí, bez otevírání
prohlížeče.

**CTA tlačítko:** Stáhnout pro macOS (14+)

*[sem screenshot: website-preview.png]*

## 2. Funkce

- **Oba providery na jednom místě** — přepínání mezi Claude a ChatGPT přímo
  v menu baru, bez nutnosti mít otevřené dvě karty v prohlížeči.
- **Vlastní interval kontroly** — appka si sama v nastaveném intervalu
  obnovuje data (výchozí 5 minut), nastavitelné podle potřeby.
- **Notifikace při blížícím se limitu** — appka upozorní lokálně
  (bez serveru, bez push notifikací), když se blížíš prahu využití.
- **Vizuální styl "F1 telemetrie"** — tmavé téma s ciferníky, HUD a
  timing-tower řádky inspirované závodní telemetrií, ne další nudný
  systémový widget.

## 3. Jak to funguje

Claude ani ChatGPT nenabízí veřejné API pro data o využití účtu. Limits
proto pro každého providera otevře vlastní, izolovanou přihlašovací session
(přesně jako v prohlížeči) a využití si vyžádá stejným způsobem, jakým to
dělá samotná webová appka daného providera — z jeho vlastní přihlášené
session, ne přes zkopírovaná cookies.

Protože jde o nezdokumentované, interní endpointy, může se to kdykoliv beze
zmínky změnit. Pokud k tomu dojde, appka to nahlásí jako "data vypadají
jinak, než se čekalo" místo aby spadla.

## 4. Privacy Policy (návrh plného textu)

> **Poslední aktualizace:** [doplnit datum]
>
> Limits je macOS appka pro sledování využití limitů účtů Claude a ChatGPT.
> Tato stránka popisuje, jaká data appka zpracovává a kde se ukládají.
>
> **Co appka čte.** Limits čte procenta využití a časy resetu limitů z tvého
> Claude a/nebo ChatGPT účtu — pomocí stejné přihlášené session, jakou by
> použil tvůj prohlížeč. Appka nemá přístup k obsahu tvých konverzací, jen
> k údajům o využití limitů.
>
> **Co appka odesílá.** Nic a nikam mimo samotné claude.ai a chatgpt.com —
> žádná analytika, žádné sledování, žádný vlastní server. Appka nemá žádnou
> vlastní backendovou infrastrukturu. Notifikace o blížícím se limitu jsou
> čistě lokální (macOS `UserNotifications`), nejsou to push notifikace a
> nejde přes ně žádná data ven.
>
> **Kde se co ukládá.** Appka běží v macOS App Sandboxu. Přihlašovací
> session ke Claude a ChatGPT appka neukládá sama — necháváš to na
> systémovém WebKit úložišti, stejně jako by to dělal Safari, a Claude i
> ChatGPT mají každý svoje vlastní, oddělené úložiště (jeden provider nemá
> přístup k cookies druhého). Pokud v appce vypneš "remember sign-ins",
> přihlášení se drží jen v paměti a po zavření appky zmizí. Appka si sama
> ukládá jen nastavení zobrazení (interval kontroly, zvolený provider pro
> menu bar, vzhled) — žádná data o využití, tokeny ani identifikátory účtu.
>
> **Smazání dat.** Přetažením appky do koše ve Finderu se smaže i všechna
> data appky (nastavení i uložené přihlášení) — macOS to u sandboxovaných
> appek dělá automaticky.
>
> **Kontakt:** [doplnit e-mail/adresu pro dotazy k privacy]

## 5. Stažení / požadavky

- macOS 14 nebo novější
- Appka je podepsaná Developer ID a notarizovaná Apple (Direct
  Distribution) — po stažení se spustí bez varování Gatekeeperu
- Aktuální verze: [doplnit dle `MARKETING_VERSION` v `project.yml`]

## Poznámky k tónu webu

Appka je celá v angličtině (vědomé rozhodnutí — čeština byla z UI vyřazená),
takže i finální text webu by měl být spíš anglicky, i když tenhle brief je
česky. Při překladu do finální podoby zachovej přímočarost a technickou
upřímnost výše (žádné marketingové výplně typu "seamless" / "powerful" bez
obsahu) — odpovídá to stylu zbytku projektu (README, commit messages).
