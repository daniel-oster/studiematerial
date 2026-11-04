# Projektanteckningar: Från röst till lag (Sveriges statsskick)

Det här syns inte på sidan. Det är en överlämning till den som bygger vidare.

Version 1, 2026-11-04.

## Vad det är

Studiesida inför provet om **Sveriges statsskick** (samhällskunskap), för Sarah. Samma utseende och samma Läs/Förhör-upplägg som plugghäftet för naturkunskap kapitel 2 (`sarah/ekologi/plugghafte/`): E-svar öppet, högre nivå utfällbart, minnesknep, trafikljus och förhörskort.

Sidan: `sarah/statsskick/studiematerial/index.html` (fristående HTML, `layout: null`). Provsidan med kortet: `sarah/statsskick/index.md`. PDF för utskrift: `fran-rost-till-lag.pdf` bredvid sidan.

## Underlag (finns inte i repot)

Repot är publikt, så originalfilerna ligger inte här. De var:

- Lärarens lista "inför provet": E-nivå (grundlagar, statschef, riksdag, utskott, opposition, regering, kommuner och regioner) och högre nivå (riksdag mot regering, ärendets väg, varför utskottens förslag blir lag, parlamentarism).
- Lärarens frågor 1–20 (1–15 E-nivå, 16–20 valfria för högre nivå).
- Lärarens bilder: Sveriges statsskick, Kommun, region och länsstyrelse, Från förslag till lag.
- Bokens kapitel 3, "Demokratiska statsskick – Sverige ett exempel", s. 49–81 (inskannat). Fotografier av boken, så sidhänvisningarna gäller den.

## Struktur

| Del | id | Innehåll | Kort |
|---|---|---|---|
| 1 Grundlagar och statschef | `#del1` | Lärarens fråga 1–5 | F1–F5 |
| 2 Riksdagen | `#del2` | Fråga 6–9, plus bonus om valsystemet | F6–F9, B1 |
| 3 Regeringen | `#del3` | Fråga 10–12, plus regeringstyper och statsförvaltningen | F10–F12, T1, T2 |
| 4 Kommun, region och du | `#del4` | Fråga 13–15, plus samma modell på tre nivåer och länsstyrelsen | F13–F15, T3, T4 |
| 5 Högre nivå | `#del5` | Fråga 16–20 med modellsvar | F16–F20 |
| 6 Begrepp | `#del6` | 44 ord från bokens ordlista och lärarens bilder | `b-<ord>` |
| Kvällen före | `#kvallen` | Alla minnesknep, makttrappan och siffror på en sida | – |

Kort-id:n följer lärarens frågenummer (F1–F20). Extrakort är märkta T (tillägg) och B (bonus, står inte på provlistan).

## Pedagogiska val

1. E-svaret står öppet med nyckelorden markerade, högre nivå är en numrerad orsakskedja som fälls ut.
2. Ett minnesknep på varje kort. De återkommande bilderna: Regera–Ärva–Trycka–Yttra (de fyra grundlagarna), Lagar–Pengar–Koll (riksdagens tre uppgifter), styrelsen och vd:n (riksdag och regering), lagkaptenen och maskoten (statsminister och statschef), doktorn och bussen (region), husregeln (lagens väg), smaka på soppan (utskotten), kassaskåp med två nycklar (grundlagsändring).
3. Högre nivå är dolt tills eleven trycker, för aktiv återkallning. Modellsvaren följer lärarens formuleringar i frågorna.
4. Del 4 pekar ut att kommun, region och stat har samma modell (fullmäktige, styrelse, nämnder), eftersom läraren själv jämför kommunfullmäktige med riksdagen.

## Källkonflikter och val

Principen: där lärarens bilder och boken säger olika står **båda uppgifterna** på sidan, i en ruta märkt "Källorna skiljer sig". Namn på ämbetsinnehavare står med år och källa.

- **Grundlagsändring (F3):** lärarens bild skriver "minst hälften", boken "fler än hälften". Båda står i rutan.
- **Bokens påstående om FN:s konventioner** (en grundlagsändring får inte strida mot dem) står med som "Boken säger också". Det finns inte på lärarens bilder, och det är tveksamt om det stämmer juridiskt, men det är bokens text och provet bygger på boken.
- **Landshövding i Dalarna (T4):** lärarens två bilder anger olika personer (Camilla Fagerberg Littorin respektive Helena Höij). Båda namnen står med källa.
- **Antal regioner (F14):** boken skriver 21 i texten (s. 76) och 20 i ordlistan (s. 80).
- **Regionskatt (F14):** lärarens bild ca 10 %, boken omkring 13 % (s. 74). Kommunalskatten är 19 % enligt boken.
- **Namn (F5, F11, F12, kvällen före):** kung Carl XVI Gustaf (boken, 2024), statsminister Ulf Kristersson (boken, sedan 2022), talman Andreas Norlén (lärarens bild). Riksdagsval hölls i september 2026, så uppgifterna kan ha ändrats.
- **Årtal:** regeringsformen 1974 (gäller 1975), YGL 1992 (lärarens bild, trädde i kraft då).
- Det som inte står på lärarens provlista (valsystem, partier, ideologier, domstolar, medborgerliga skyldigheter) är utelämnat, utom ett bonuskort om valsystemet (B1) eftersom spärregeln ingår i lärarens bild om riksdagen.

## Design och teknik

Samma CSS och skript som plugghäftet, kopierade in i den fristående filen. Skillnader: delarnas accenter (`#del1`–`#del6`), lagringsnyckeln `statsskick-lampor-v1` och urvalen i förhöret (`grund`, `riks`, `reg`, `lokal`, `hog`, `begrepp`).

- `article.item[data-card][data-group]` är ett kort. `[data-back]` markerar det som visas på kortets baksida i förhöret.
- Texterna finns bara i HTML-filen. Ändra där, bygg sedan om PDF:en.

## PDF

```
node _verktyg/sida-till-pdf/render.js sarah/statsskick/studiematerial/index.html sarah/statsskick/studiematerial/fran-rost-till-lag.pdf
```

Skriver ut sidan med webbläsarens utskriftsstil (lampor och knappar döljs, alla utfällbara svar öppnas). Kräver Node med Playwright. Typsnitten hämtas från Google Fonts vid utskriften.

## Sådant som kan bli inaktuellt

- Namn på ämbetsinnehavare (se ovan), särskilt statsminister och talman efter valet 2026.
- Antalet nationella folkomröstningar (sex, senast 2003 enligt boken).

## PDF: sidbrytningar

Utskriftsstilen (i `<style>` längst ner, `@media print`) ger: varje del på ny sida, rubriker som hålls ihop med det som följer, kort/rutor/tabeller som inte delas mitt i, vägkartan och källraden dolda, samt en tätare "Kvällen före" som ryms på en sida. Efter ändringar i texten: kontrollera att inget kort blivit så högt att det inte ryms på en sida (F16 är det högsta), och bygg om PDF:en.
