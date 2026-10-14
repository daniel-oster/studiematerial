---
# MALL – kopiera till t.ex. sarah/<prov>/index.md eller sarah/<prov>/<del>.md
title: Rubrik på materialet
id: sarah-exempel            # unikt id (används av "parent" på underliggande sidor)
child: sarah                 # sarah eller annabelle
parent:                      # id på samlingssidan ovanför (tomt = visas på barnets sida)
subject: Ämne                # valfritt
test_date: 2026-11-05        # valfritt, provdatum
order: 1                     # sorteringsordning
description: Kort beskrivning som syns i listan.
kind: Begrepp                # valfritt – etikett på kortet i provet (t.ex. Begrepp, Studiematerial)
pdf: haefte.pdf              # valfritt – ger knappen "PDF att skriva ut" på kortet
open_label: Läs och förhör   # valfritt – text på knappen som öppnar sidan
pdfs:                        # valfritt – lägg PDF-filerna i samma mapp
  - title: Arbetsblad
    file: arbetsblad.pdf
terms:                       # valfritt – begreppslista
  - term: Begrepp
    definition: Förklaring av begreppet.
    knep: Minnesknep (valfritt).
---

Fri text i Markdown här (sammanfattningar, frågor, bilder ...).
