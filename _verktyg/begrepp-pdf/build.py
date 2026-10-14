"""Bygger utskriftshäftet (PDF) för Ekologins 44 begrepp.

Läser webbsidan sarah/ekologi/begrepp/index.html, så att texterna bara finns på ett ställe,
och lägger upp dem i samma stil som plugghäftet för kapitel 2 (Fraunces + Source Sans 3,
ett kort per begrepp, lampor, minnesknep i gul ruta, vik-kort och kvällen före provet).

Kör från repots rot:  python3 _verktyg/begrepp-pdf/build.py
Kräver: python3 med bs4 och pypdf, node med playwright (Chromium).
"""
import html
import os
import re
import subprocess
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
SRC = ROOT / "sarah/ekologi/begrepp/index.html"
OUT = ROOT / "sarah/ekologi/begrepp/ekologins-44-begrepp.pdf"
TMP = HERE / "_build"

# Korta minnesknep till vik-korten (det långa knepet står i kortet för varje begrepp).
SHORT_KNEP = {
    1: "Naturens hus", 2: "Bio = liv", 3: "A som i Aldrig levt", 4: "Abborrfolket",
    5: "Kocken", 6: "Gästen", 7: "Diskaren", 8: "Bygga med ljus",
    9: "Fotosyntesen baklänges", 10: "Pilen = ”blir mat åt”", 11: "Spindelnätet",
    12: "Våningar i ett hus", 13: "Tiondelsregeln", 14: "Enkelbiljett", 15: "Pantburkar",
    16: "Kortaste plankan", 17: "Maxskylten i hissen", 18: "Sista bullen",
    19: "Jägaren vinner", 20: "Win-win", 21: "Zooma ut: gen → art → ekosystem",
    22: "Ingen faktura", 23: "Skafferiet", 24: "Servicen", 25: "Spat",
    26: "Lämna lägerplatsen", 27: "Benet NATUR", 28: "Benet MÄNNISKOR", 29: "Benet PENGAR",
    30: "Plocka bären, inte riset", 31: "Ditt fotspår", 32: "Gräset reser sig",
    33: "Isen på tjärnen", 34: "Gammal karta mot ny", 35: "Algfest → syrebrist",
    36: "Ringar på vattnet",
}

# Del 1–5 handlar om naturen (grönt), del 6–8 om människan och hållbarhet (blått).
def theme(part):
    return "green" if part <= 5 else "blue"


def inner(el):
    return "".join(str(c) for c in el.contents).strip()


def lamps():
    return ('<div class="lamps"><span><i class="g"></i>kan</span>'
            '<span><i class="y"></i>osäker</span><span><i class="r"></i>kan inte</span></div>')


def render_tagline(p):
    """<p class="ex"><span class="tag">I tjärnen</span>text</p> -> etikett + text."""
    tag = p.find(class_="tag")
    label = tag.get_text(strip=True) if tag else ""
    if tag:
        tag.extract()
    cls = "ex nyans" if label.lower().startswith("nyansera") else "ex"
    return f'<p class="{cls}"><span class="lbl">{html.escape(label)}</span>{inner(p)}</p>'


def render_knep(p):
    m = p.find("mark")
    return f'<div class="knep"><span class="pill knep-pill">Minnesknep</span> {inner(m)}</div>'


def render_chain(ol):
    items = "".join(f"<li><b>{i}</b>{inner(li)}</li>" for i, li in enumerate(ol.find_all("li"), 1))
    return f'<ol class="steps">{items}</ol>'


def render_body_children(children):
    """Innehållet i ett kort (högerkolumnen)."""
    out = []
    for c in children:
        if not getattr(c, "name", None):
            continue
        cls = c.get("class", [])
        if c.name == "h3" or "eyebrow" in cls or "num" in cls:
            continue
        if "plain" in cls:
            out.append(f"<p class=\"plain\">{inner(c)}</p>")
        elif "knep" in cls:
            out.append(render_knep(c))
        elif "ex" in cls:
            out.append(render_tagline(c))
        elif "chain-h" in cls:
            out.append(f'<p class="chain-h">{inner(c)}</p>')
        elif c.name == "ol" and "chain" in cls:
            out.append(render_chain(c))
        elif "tbl-wrap" in cls:
            out.append(f'<div class="tbl">{inner(c)}</div>')
        else:
            out.append(str(c))
    return "".join(out)


def render_extra(el):
    """Rutor som står efter ett kort: vanligt misstag, ordförklaring, fördjupning."""
    cls = el.get("class", [])
    if el.name == "div" and "box" in cls:
        kind = "warn" if "warn" in cls else "note"
        title = el.find("strong").get_text(strip=True)
        text = inner(el.find("p"))
        return f'<div class="box {kind}"><span class="pill">{html.escape(title)}</span> {text}</div>'
    if el.name == "details" and "deep" in cls:
        head = el.find(class_="deep-k")
        head.extract()
        title = el.find("summary").get_text(" ", strip=True)
        body = "".join(f"<p>{inner(p)}</p>" for p in el.find(class_="deep-body").find_all("p"))
        return (f'<div class="deep"><span class="pill deep-pill">Fördjupning</span>'
                f'<p class="deep-t">{html.escape(title)}</p>{body}</div>')
    return ""


def render_card(art, extras):
    num = art["data-num"]
    kind = art["data-kind"]
    title = inner(art.find("h3"))
    if kind == "challenge":
        details = art.find("details")
        details.find("summary").extract()
        body = render_body_children(details.children)
        left = (f'<div class="kicker">Utmaning</div><div class="code">{num}</div>'
                f'<h3 class="q long">{title}</h3>{lamps()}<div class="ref">Facit nr {num}</div>')
        right = f'<span class="pill lvl-pill">Svar · tänk själv först</span>{body}'
    else:
        body = render_body_children(art.find("h3").parent.children)
        left = (f'<div class="kicker">Begrepp</div><div class="code">{num}</div>'
                f'<h3 class="q">{title}</h3>{lamps()}<div class="ref">Facit nr {num}</div>')
        right = f'<span class="pill lvl-pill">Förklaring</span>{body}'
    right += "".join(extras)
    return (f'<section class="card {kind}"><div class="left">{left}</div>'
            f'<div class="right">{right}</div></section>')


def render_part(sec):
    part = int(sec["data-part"])
    head = sec.find(class_="part-head")
    q = head.find("h2").get_text(strip=True)
    sub = head.find(class_="sub").get_text(strip=True)
    facit = head.find(class_="facit").get_text(strip=True)
    intro = inner(sec.find(class_="intro"))
    gk = sec.find(class_="gk")
    gk_text = inner(gk.find("mark"))
    legend = gk.find(class_="legend")
    legend_html = f'<p class="legend">{inner(legend)}</p>' if legend else ""

    blocks = []
    pending = None  # (artikel, [extra rutor])
    for el in sec.children:
        if not getattr(el, "name", None) or el is head:
            continue
        cls = el.get("class", [])
        if el.name == "article" and "item" in cls:
            if pending:
                blocks.append(render_card(*pending))
            pending = (el, [])
        elif (el.name == "div" and "box" in cls) or (el.name == "details" and "deep" in cls):
            if pending:
                pending[1].append(render_extra(el))
            else:  # rutan står efter en figur: lägg den direkt under figuren
                blocks.append(f'<div class="after-fig">{render_extra(el)}</div>')
        elif el.name == "figure":
            if pending:
                blocks.append(render_card(*pending))
                pending = None
            blocks.append(f'<figure class="fig">{inner(el)}</figure>')
    if pending:
        blocks.append(render_card(*pending))

    return (f'<div class="part t-{theme(part)}" id="del{part}">'
            f'<header class="part-head"><span class="delpill">Del {part}</span><h2>{html.escape(q)}</h2>'
            f'<div class="part-meta">{html.escape(sub)}<br>{html.escape(facit)}</div></header>'
            f'<div class="part-intro"><p>{intro}</p><div class="gk"><span class="pill knep-pill">Knepet för hela delen</span> '
            f'<b>{gk_text}</b>{legend_html}</div></div>'
            + "".join(blocks) + "</div>"), part, q, gk_text, sub


def build_html(pages):
    soup = BeautifulSoup(SRC.read_text(encoding="utf-8"), "html.parser")
    lead = inner(soup.find(class_="hero").find(class_="lead"))
    parts_html, toc, gks = [], [], []
    for sec in soup.select("section.part"):
        h, part, q, gk, sub = render_part(sec)
        parts_html.append(h)
        toc.append((part, q, sub))
        gks.append((part, q, gk))

    # Vik-kort: alla begrepp i facits ordning.
    terms = sorted(soup.select('article[data-kind="term"]'), key=lambda a: int(a["data-num"]))
    fold = "".join(
        f'<div class="fold"><div class="f-front"><div class="f-term">{inner(a.find("h3"))}</div>'
        f'<div class="f-k">Begrepp · nr {a["data-num"]}</div></div>'
        f'<div class="f-back"><p>{inner(a.find(class_="plain"))}</p>'
        f'<p class="f-knep">Knep: {html.escape(SHORT_KNEP[int(a["data-num"])])}</p></div></div>'
        for a in terms)

    whole = "".join(f"<li>{inner(li)}</li>" for li in soup.select("#helheten ol li"))
    mistakes = "".join(
        f'<div class="mini warnmini"><b>{i}</b>{inner(b.find("p"))}</div>'
        for i, b in enumerate(soup.select("div.box.warn"), 1))

    def pg(key):
        return pages.get(key, "")

    toc_rows = "".join(
        f'<li><i class="dot t-{theme(p)}"></i><span><b>Del {p} · {html.escape(q)}</b><small>{html.escape(sub)}</small></span><em>s. {pg(f"del{p}")}</em></li>'
        for p, q, sub in toc)
    toc_rows += (f'<li><i class="dot t-slate"></i><span><b>Vik-kort med begrepp</b><small>Klipp, vik, förhör dig själv</small></span><em>s. {pg("vik")}</em></li>'
                 f'<li><i class="dot t-gold"></i><span><b>Kvällen före provet</b><small>Allt på en sida</small></span><em>s. {pg("kvall")}</em></li>')

    gk_boxes = "".join(
        f'<div class="mini t-{theme(p)}"><b>Del {p} · {html.escape(q)}</b>{g}</div>' for p, q, g in gks)

    css = (HERE / "style.css").read_text(encoding="utf-8")
    return f"""<!doctype html><html lang="sv"><head><meta charset="utf-8">
<title>Ekologins 44 begrepp</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700;9..144,900&family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400&display=swap">
<style>{css}</style></head><body>

<section class="cover">
  <div class="hero">
    <div>
      <p class="hero-k">Ekologi och hållbar utveckling · Begrepp och utmaningar</p>
      <h1>Ekologins<br><span>44 begrepp</span></h1>
      <p class="hero-lead">{lead}</p>
    </div>
    <svg class="hero-ic" viewBox="0 0 120 120" aria-hidden="true">
      <circle cx="60" cy="60" r="54" fill="none" stroke="#F2C94C" stroke-width="2" stroke-dasharray="4 6"/>
      <ellipse cx="60" cy="66" rx="40" ry="20" fill="#7FB3BA"/>
      <ellipse cx="60" cy="66" rx="27" ry="12" fill="none" stroke="#E8F2EA" stroke-width="2" opacity=".8"/>
      <ellipse cx="60" cy="66" rx="13" ry="5.5" fill="none" stroke="#E8F2EA" stroke-width="2" opacity=".8"/>
      <path d="M30 48 l8 -22 l8 22 z M44 50 l9 -26 l9 26 z M76 48 l8 -20 l8 20 z" fill="#8FC79A"/>
    </svg>
  </div>

  <div class="legend3">
    <div class="lg green"><span class="pill lvl-pill">Förklaring</span><p>Begreppet med enkla ord, och ett exempel från skogstjärnen.</p></div>
    <div class="lg purple"><span class="pill deep-pill">Fördjupning</span><p>Gymnasienivå. Hjälper dig att <b>resonera nyanserat</b> för högre betyg.</p></div>
    <div class="lg yellow"><span class="pill knep-pill">Minnesknep</span><p>En bild eller liknelse som får det att fastna.</p></div>
  </div>

  <div class="two">
    <div class="col">
    <div class="panel">
      <h3>Så använder du häftet</h3>
      <ol class="howto">
        <li><span><b>Färglägg lamporna</b> vid varje begrepp: <b>grön</b> = kan, <b>gul</b> = osäker, <b>röd</b> = kan inte än.</span></li>
        <li><span><b>Täck högersidan</b> med ett papper. Säg förklaringen <b>högt</b> med egna ord. Kolla sedan.</span></li>
        <li><span><b>Plugga rött först</b>, sedan gult. Testa igen nästa dag.</span></li>
        <li><span>Utmaningarna: <b>tänk själv först</b>, svara i flera led, läs sedan svaret.</span></li>
      </ol>
    </div>
    <div class="panel plan">
    <h3>Lite varje dag slår allt på en gång</h3>
    <table>
      <tr><th>Dag 1</th><td>Del 1–2. Färglägg lamporna, täck och svara.</td></tr>
      <tr><th>Dag 2</th><td>Del 3–4. Gör om de röda från dag 1.</td></tr>
      <tr><th>Dag 3</th><td>Del 5–6. Skriv egna svar på utmaningarna innan du läser svaren.</td></tr>
      <tr><th>Dag 4</th><td>Del 7–8. Klipp ut vik-korten och förhör dig, gärna med någon.</td></tr>
      <tr><th>Dag 5</th><td>Bara gula och röda kort + ”Kvällen före provet”. Sov ordentligt.</td></tr>
    </table>
    </div>
    </div>
    <div class="panel">
      <h3>Innehåll</h3>
      <ul class="toc">{toc_rows}</ul>
    </div>
  </div>


  <div class="tip"><b>Numren är samma som i facit,</b> så du kan gå tillbaka till ditt papper. Du behöver inte använda exakt samma ord som facit. Det räcker att förklara med egna ord.</div>
</section>

{''.join(parts_html)}

<section class="vik" id="vik">
  <header class="part-head t-slate"><span class="delpill">Vik-kort</span><h2>Alla 36 begrepp</h2>
    <div class="part-meta">Begreppen i facits ordning.</div></header>
  <div class="vik-how">
    <div><b>1. Vik</b> längs den prickade mittlinjen, med texten utåt.</div>
    <div><b>2. Klipp</b> längs de streckade linjerna.</div>
    <div><b>3. Förhör dig:</b> läs begreppet, förklara högt, vänd och kolla. Sortera i högar: kan / kan inte.</div>
  </div>
  <div class="folds">{fold}</div>
</section>

<section class="kvall" id="kvall">
  <h2 class="big">Kvällen före provet – allt på en sida</h2>
  <p class="muted">Kan du förklara varje ruta högt på 20 sekunder? Då är du redo.</p>
  <div class="grid3">{gk_boxes}
    <div class="mini t-gold"><b>Energi mot ämnen</b>Energi = enkelbiljett. Ämnen = pantburk.</div>
  </div>
  <h3 class="sec">Hela tjärnen i åtta meningar</h3>
  <ol class="eight">{whole}</ol>
  <h3 class="sec">Vanliga misstag</h3>
  <div class="grid2">{mistakes}</div>
  <h3 class="sec">Siffror som är bra att kunna</h3>
  <div class="nums">
    <div><b>≈ 10 %</b>av energin går vidare till nästa trofinivå</div>
    <div><b>1 000 → 1 kg</b>alger blir till ungefär så mycket gädda</div>
    <div><b>78 %</b>av luften är kväve, men växterna kan inte använda det direkt</div>
    <div><b>1987</b>Brundtlandrapporten definierar hållbar utveckling</div>
    <div><b>17 mål</b>i Agenda 2030</div>
    <div><b>9 gränser</b>planetens gränser, framtagna 2009 (Rockström)</div>
    <div><b>7 av 9</b>gränser passerade enligt genomgången 2026</div>
    <div><b>3 nivåer</b>av biologisk mångfald: gener, arter, ekosystem</div>
  </div>
  <p class="good-luck">Lycka till! Du har gjort jobbet. Nu är det bara att plocka fram det.</p>
</section>
</body></html>"""


def render(pages):
    TMP.mkdir(exist_ok=True)
    src = TMP / "haefte.html"
    pdf = TMP / "haefte.pdf"
    src.write_text(build_html(pages), encoding="utf-8")
    env = dict(os.environ)
    npm_root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    env["NODE_PATH"] = npm_root + os.pathsep + env.get("NODE_PATH", "")
    subprocess.run(["node", str(HERE / "render.js"), str(src), str(pdf)], check=True, env=env)
    return pdf


def find_pages(pdf, soup_titles):
    """Sidnummer för varje del, vik-korten och kvällen före provet (för innehållsförteckningen)."""
    texts = [re.sub(r"\s+", " ", p.extract_text() or "") for p in PdfReader(str(pdf)).pages]
    found = {}
    for key, needle in soup_titles:
        for i, t in enumerate(texts[1:], 2):
            if needle in t:
                found[key] = i
                break
    return found


def main():
    soup = BeautifulSoup(SRC.read_text(encoding="utf-8"), "html.parser")
    titles = [(f'del{s["data-part"]}', s.find("h2").get_text(strip=True)) for s in soup.select("section.part")]
    titles += [("vik", "Alla 36 begrepp"), ("kvall", "Kvällen före provet – allt på en sida")]
    pdf = render({})
    pages = find_pages(pdf, titles)
    missing = [k for k, _ in titles if k not in pages]
    if missing:
        sys.exit(f"Hittade inte sidnummer för: {missing}")
    pdf = render(pages)
    if find_pages(pdf, titles) != pages:
        sys.exit("Sidnumren flyttade sig mellan körningarna")
    OUT.write_bytes(pdf.read_bytes())
    print(f"Skrev {OUT.relative_to(ROOT)} ({len(PdfReader(str(OUT)).pages)} sidor), sidor: {pages}")


if __name__ == "__main__":
    main()
