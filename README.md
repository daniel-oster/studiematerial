# Studiematerial

Studiematerial för Sarah och Annabelle, publicerat med GitHub Pages:
**https://daniel-oster.github.io/studiematerial/**

## Struktur

```
index.html              Startsida – välj barn
sarah/index.html        Sarahs sida – listar hennes material automatiskt
annabelle/index.html    Annabelles sida
sarah/<prov>/index.md   Ett material (t.ex. ett prov); kan vara en samling
sarah/<prov>/<del>.md   Underliggande delar (begrepp, PDF:er ...)
_mallar/material.md     Mall med alla fält som går att använda
_anteckningar/          Projektanteckningar per material (publiceras inte på sidan)
```

Varje materialsida är en Markdown-fil med samma format (se `_mallar/material.md`):

- `child` – vilket barn materialet hör till
- `id` – unikt id
- `parent` – id på samlingen ovanför; tomt betyder att sidan visas direkt på barnets sida
- `terms` – begreppslista (har en "förhör mig"-knapp som döljer förklaringarna)
- `pdfs` – PDF:er som öppnas i ny flik för utskrift (lägg filerna i samma mapp)

Sidor som har `parent` satt till en sidas `id` listas automatiskt längst ner på den sidan.

### Egna HTML-sidor

Ett material kan också vara en färdig, fristående HTML-sida (t.ex. en Claude-artefakt).
Lägg den som `index.html` i en egen mapp och sätt `layout: null` i front matter, så
används sidans egen design men den listas ändå på rätt ställe. Exempel:
`sarah/ekologi/begrepp/index.html`.

**Obs:** repot och sidan är publika. Lägg inte upp lärarens facit eller annat material
som inte får spridas.
