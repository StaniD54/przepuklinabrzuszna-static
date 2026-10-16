#!/usr/bin/env python3
# Prototyp: przepuklinabrzuszna.pl w układzie i krojach pisma z angielskiej strony meshfreehernia
import re, os, json, shutil, glob, html
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/site"
UP = f"{ROOT}/build/source-images"
BASE = "https://przepuklinabrzuszna.pl"
TEL, TELF = "603751335", "603 751 335"
EMAIL = "s.dabrowiecki@outlook.com"

shutil.rmtree(OUT, ignore_errors=True)
for d in ("img", "fonts"): os.makedirs(f"{OUT}/{d}")

# ---- czcionki (hostowane lokalnie, bez Google Fonts) ----
for f in os.listdir(f"{ROOT}/build/fonts"):
    shutil.copy(f"{ROOT}/build/fonts/{f}", f"{OUT}/fonts/{f}")

# ---- obrazy: zmniejszone, WebP ----
IMGS = {
 "zan1": "HV_1.jpg", "zan2": "HV_2.jpg", "zan3": "HV_3.jpg", "zan4": "HV_4.jpg", "powikl1": "HV_powiklana_1.jpg", "powikl2": "HV-martwica-skory-e1654946972342.jpg",
 "po1": "HV_pooper_1.jpg", "po2": "HV_pooper_2.jpg", "po3": "HV_pooper_3.jpg", "przed1": "HV-przed-operacja.jpg", "przed2": "HV-przed-operacja2.jpg",
 "otylosc": "otylosc-i-przepuklina.jpg",
 "plast-przed": "otylosc-i-HV-229x300.jpg", "plast-po": "otylosc-i-HV-pooper-230x300.jpg",
 "otwarta": "otwary-brzuch-300x199.jpg", "siatka": "siatka-do-wszczepienia-300x191.jpg",
 "warstwy": "warstwy-gdzie-siatka-e1654947350302.jpg", "lapar": "HV-laaproskopia-300x224.jpg",
 "esk1": "esk4-1024x575-1.jpg", "esk2": "Eskulap-szpital.jpg",
 "e-budynek": "eskulap-budynek.jpg", "e-pokoj": "eskulap-pokoj.jpg", "e-recepcja": "eskulap-recepcja.jpg", "e-lazienka": "eskulap-lazienka.jpg", "e-obraz": "eskulap-pracownia-obrazowa.jpg",
 "e-zima": "eskulap-front.jpg", "e-lato": "eskulap-wejscie.jpg", "e-sala": "eskulap-sala-angio.jpg", "e-tomo": "eskulap-tomograf.jpg", "e-recep2": "eskulap-recepcja2.jpg", "e-mapa": "eskulap-wejscia-mapa.png",
 "prof": "SD_n_1-scaled.jpg",
 "pep1": "pepkowa-1.jpg", "pep2": "pepkowa-2.jpg", "pep3": "pepkowa-3.jpg",
}
SIZES = {}
from PIL import ImageSequence
_g = Image.open(f"{UP}/powieksza-sie.gif"); _fr = [f.convert("RGB").copy() for f in ImageSequence.Iterator(_g)]
_fr[0].save(f"{OUT}/img/powieksza-sie.webp", save_all=True, append_images=_fr[1:], duration=_g.info.get("duration", 120), loop=0, quality=65, method=6)
SIZES["powieksza-sie"] = _fr[0].size
_g2 = Image.open(f"{UP}/uwiezniecie.gif"); _f2 = []; _d2 = []
for _f in ImageSequence.Iterator(_g2): _f2.append(_f.convert("RGBA").copy()); _d2.append(_f.info.get("duration", 1000))
_f2[0].save(f"{OUT}/img/uwiezniecie.webp", save_all=True, append_images=_f2[1:], duration=_d2, loop=0, quality=80, method=6)
SIZES["uwiezniecie"] = _f2[0].size
for k, p in IMGS.items():
    im = Image.open(f"{UP}/{p}").convert("RGB")
    im.thumbnail((900, 1100))
    im.save(f"{OUT}/img/{k}.webp", quality=80, method=6)
    SIZES[k] = im.size

def img(k, alt, cap=None, cls=""):
    w, h = SIZES[k]
    c = f'<figcaption>{cap}</figcaption>' if cap else ""
    return f'<figure class="ph {cls}"><img src="/img/{k}.webp" width="{w}" height="{h}" alt="{alt}" loading="lazy">{c}</figure>'

REV = json.load(open(f"{ROOT}/build/reviews.json", encoding="utf-8"))
REV = {n.split(" (")[0]: (n, t) for n, t in REV}

# ---- CSS ----
CSS = open(f"{ROOT}/build/style.css", encoding="utf-8").read()
open(f"{OUT}/style.css", "w", encoding="utf-8").write(CSS)
shutil.copy(f"{ROOT}/build/menu.js", f"{OUT}/menu.js")

SOON = lambda t: f'<span class="soon" title="w przygotowaniu">{t} <small>wkrótce</small></span>'
NAV_ITEMS = [
 ("link", "/", "Start"), ("link", "/przepuklina-brzuszna-objawy-zdjecia/", "Wygląd, objawy"),
 ("dd", "Rodzaje przepuklin", [("/przepuklina-pooperacyjna/", "Pooperacyjna"), ("/przepuklina-kresy-bialej/", "Kresy białej"), ("/przepuklina-pepkowa/", "Pępkowa"), ("/przepuklina-ledzwiowa/", "Lędźwiowa"), ("/rzadkie-przepukliny-brzuszne/", "Rzadkie"), ("/przepukliny-wewnetrzne/", "Wewnętrzne"), ("/przepuklina-rozworu-przelykowego/", "Przełykowa")]),
 ("dd", "Metody operacji", [("/operacja-przepukliny-brzusznej/", "Przegląd metod"), ("/operacja-klasyczna-przepukliny-brzusznej/", "Klasyczne"), ("/operacja-laparoskopowa-przepukliny-brzusznej/", "Laparoskopowe"), ("/operacja-hybrydowa-przepukliny-brzusznej/", "Hybrydowe")]),
 ("link", "/wyniki-leczenia-przepukliny-brzusznej/", "Wyniki i przygotowanie"),
 ("link", "/koszt-operacji-przepukliny-brzusznej/", "Konsultacje i koszt"),
]

def build_nav(path):
    out = []
    for it in NAV_ITEMS:
        if it[0] == "link":
            out.append(f'<a href="{it[1]}"{" aria-current=page" if it[1] == path else ""}>{it[2]}</a>')
        else:
            cur = any(u == path for u, _ in it[2])
            subs = "".join(f'<a href="{u}"{" aria-current=page" if u == path else ""}>{t}</a>' if u else SOON(t) for u, t in it[2])
            out.append(f'<div class="dd{" cur" if cur else ""}"><button type="button" aria-expanded="false">{it[1]}</button><div class="sub">{subs}</div></div>')
    return "".join(out)

def _flat_nav():
    out = []
    for it in NAV_ITEMS:
        if it[0] == "link": out.append((it[1], it[2]))
        else: out.extend(it[2])
    return out

def pager(path):
    flat = _flat_nav(); urls = [u for u, _ in flat]
    if path not in urls: return ""
    i = urls.index(path)
    nu, nt = flat[i + 1] if i + 1 < len(flat) else flat[0]
    lab = nt
    return f'<div class="pager"><a class="up" href="#top" aria-label="Na górę strony" title="Na górę">↑</a><a class="next" href="{nu}">{lab} →</a></div>'

def page(path, title, desc, body, h1_schema=None):
    nav = build_nav(path)
    canon = BASE + path
    return f"""<!doctype html>
<html lang="pl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{canon}"><meta property="og:type" content="website"><meta property="og:locale" content="pl_PL">
<link rel="preload" href="/fonts/hanken-grotesk-latin-ext-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/source-serif-4-latin-ext-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/style.css">
</head>
<body>
<div class="wrap" id="top">
<header class="top">
  <a class="brand" href="/"><strong>Prof. Stanisław Dąbrowiecki</strong></a>
  <a class="toptel" href="tel:+48{TEL}">Tel. {TELF}</a>
</header>
<nav class="nav" aria-label="Główne">{nav}</nav>
{body}
{pager(path)}
<footer>
  <p><strong>Indywidualna Specjalistyczna Praktyka Lekarska Prof. Stanisław Dąbrowiecki</strong><br>
  Tel. <a href="tel:+48{TEL}">{TELF}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a> · WhatsApp <a href="https://wa.me/48{TEL}">{TELF}</a></p>
  <p><strong>Konsultacje i zabiegi odbywają się w ramach Indywidualnej Specjalistycznej Praktyki Lekarskiej. Prof. Dąbrowiecki nie ma umowy z NFZ; konsultacje i zabiegi są płatne.</strong></p>
  <p>Informacje na stronie mają charakter ogólny i nie zastępują badania lekarskiego. Leczenie i jego koszt ustala lekarz po zbadaniu chorego. <a href="/koszt-operacji-przepukliny-brzusznej/#o-mnie">O mnie</a> · <a href="/cookies/">Polityka prywatności</a><br>Zaktualizowano: 15.10.2026</p>
</footer>
</div>
<div class="bar" role="navigation" aria-label="Szybki kontakt">
  <a class="btn" href="tel:+48{TEL}">Zadzwoń</a><a class="btn ghost" href="sms:+48{TEL}?&body=BRZUCH">SMS: BRZUCH</a>
</div>
<script src="/menu.js" defer></script>
</body>
</html>"""

def sec(label, inner, id_=None, cls=""):
    i = f' id="{id_}"' if id_ else ""
    return f'<section{i}><h2>{label}</h2><div class="body {cls}">{inner}</div></section>'

DRAFT = '<span class="draft">szkic do akceptacji</span>'
CTA = (f'<div class="cta-row"><a class="btn" href="tel:+48{TEL}">Zadzwoń: {TELF}</a>'
       f'<a class="btn ghost" href="sms:+48{TEL}?&body=BRZUCH">Wyślij SMS: BRZUCH</a></div>')

def hero(eyebrow, h1, lead):
    if ": " in h1 and "<span>" not in h1:
        a, b_ = h1.split(": ", 1); h1 = f"<span>{a}:</span> <span>{b_}</span>"
    return f'<div class="hero">{f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ''}<h1>{h1}</h1><p class="lead">{lead}</p>{CTA}</div>'

def teaser(t, n=2, maxlen=300):
    t = t.replace("..........", " ").strip()
    parts = re.split(r"(?<=[.!?])\s+", t)
    out = " ".join(parts[:n])
    if len(out) > maxlen:
        out = out[:maxlen].rsplit(" ", 1)[0].rstrip(",;:")
    out = re.sub(r"\s+", " ", out)
    return out.rstrip(". ") + " …" if (len(parts) > n or len(out) < len(t.strip())) else out

def review(name):
    n, t = REV[name]
    return f'<blockquote class="rev"><p>{html.escape(teaser(t))}</p><footer>{n}</footer></blockquote>'

def consult_block():
    return sec("Konsultacje", f"""
<h3>Konsultacja online</h3>
<p>Pacjenta z przepukliną brzuszną nie można zakwalifikować do leczenia po konsultacji online. Podczas rozmowy mogę przekazać tylko ogólne informacje, ponieważ każdy przypadek jest inny i nie ma standardowego postępowania. W trakcie takiej rozmowy dopytam dokładnie o stan zdrowia pacjenta i opiszę wymagane przygotowanie do zabiegu. Omówię również organizację leczenia, długość pobytu i związane z tym koszty. Jednak do ostatecznej kwalifikacji niezbędne jest osobiste badanie chorego. W przypadku przepukliny brzusznej badanie jest wymagane za każdym razem, a czasami także tomografia komputerowa lub inne badania dodatkowe.</p>
<p>Rozmowy: Skype, WhatsApp, Messenger lub Zoom, praktycznie codziennie o godzinie 20.00. Termin ustalamy telefonicznie lub SMS-em: <a href="tel:+48{TEL}">{TELF}</a>.</p>
<h3>Kwalifikacja do leczenia</h3>
<p>Każda zakwalifikowana osoba otrzymuje szczegółowe informacje na piśmie dotyczące przygotowania do zabiegu i zachowania po operacji, tak aby leczenie i okres rekonwalescencji trwały jak najkrócej.</p>
<h3>Konsultacje osobiste</h3>
<p>Konsultuję obecnie wyłącznie w Bydgoszczy i w Poznaniu.</p>
<dl class="where">
 <dt>Bydgoszcz</dt><dd>ul. Mierosławskiego 9/3 · <a href="tel:+48{TEL}">{TELF}</a> · <a href="https://www.google.com/maps/search/?api=1&query=Mierosławskiego+9+Bydgoszcz">mapa</a></dd>
 <dt>Poznań</dt><dd>ul. Szafirowa 3/5, 62-070 Dąbrowa k. Poznania · <a href="tel:+48618550662">61 855 06 62</a> · <a href="https://www.google.com/maps/search/?api=1&query=Szafirowa+3/5+62-070+Dąbrowa">mapa</a></dd>
</dl>
<p class="note">Wyślij SMS o treści <b>BRZUCH</b> na nr {TELF}. Odeślę adresy i terminy konsultacji oraz podstawowe informacje o leczeniu przepuklin brzusznych.</p>""", "konsultacje")

ZL = "https://www.znanylekarz.pl/profil/stanislaw-dabrowiecki"
def opinions_block():
    return sec("Opinie", "".join(review(k) for k in REV) +
               f'<p>Pełne opinie pacjentów: <a href="{ZL}" rel="noopener" target="_blank">profil w serwisie ZnanyLekarz</a></p>', "opinie")

def about_block():
    return sec("O mnie", f"""<div class="about">{img('prof','Prof. Stanisław Dąbrowiecki')}<div>
    <p>Absolwent Wydziału Lekarskiego Akademii Medycznej w Gdańsku. Specjalista chirurgii ogólnej, doktor i doktor habilitowany nauk medycznych. Od 2012 roku profesor zwyczajny (nominacja z rąk Prezydenta RP).</p>
    <p>Od 2002 r. profesor nadzwyczajny Akademii Medycznej im. L. Rydygiera w Bydgoszczy, w latach 2002–2004 prorektor ds. klinicznych i kształcenia podyplomowego. Po połączeniu uczelni z Uniwersytetem Mikołaja Kopernika w Toruniu: profesor UMK i pełnomocnik Rektora UMK ds. klinicznych i kształcenia podyplomowego.</p>
    <p>W latach 2001–2012 kierownik Katedry i Kliniki Chirurgii Ogólnej i Endokrynologicznej Collegium Medicum UMK w Bydgoszczy. Za mojego kierownictwa powstał w niej wiodący w kraju ośrodek leczenia trudnych przypadków przepuklin.</p>
    <p>W latach 2009–2012 przewodniczący Rady Ordynatorów Szpitala Uniwersyteckiego w Bydgoszczy. Od 2020 roku praktykuję wyłącznie prywatnie.</p></div></div>""", "o-mnie")

def consult_short():
    return sec("Konsultacje", f"""<p>Konsultuję w Bydgoszczy (ul. Mierosławskiego 9/3) i w Poznaniu (Dąbrowa k. Poznania) oraz online. Operuję w prywatnym szpitalu Eskulap w Osielsku koło Bydgoszczy.</p>
<p>Termin ustalamy telefonicznie lub SMS-em: <a href="tel:+48{TEL}">{TELF}</a>. <a href="/koszt-operacji-przepukliny-brzusznej/">Konsultacje, szpital i koszt: szczegóły</a></p>""", "konsultacje")

def hospital_block():
    return sec("Gdzie operuję", f"""
<p>Operuję w szpitalu Eskulap w Osielsku koło Bydgoszczy. Jest to prywatny, luksusowo wyposażony szpital z własnym parkingiem przy wejściu.</p>
<ul class="check"><li>jasne, klimatyzowane pokoje chorych, własne łazienki z prysznicem bez progu</li><li>dobrze wyposażona sala operacyjna, dostępna całą dobę, Intensywna Terapia przy sali operacyjnej</li><li>doświadczony zespół pielęgniarski, stale dostępny lekarz, również na dyżurze nocnym</li><li>pracownia RTG, nowoczesne obrazowanie Siemens na miejscu (w tym rezonans magnetyczny i pracownia angiografii cyfrowej) oraz laboratorium z możliwością wykonania nawet skomplikowanych badań</li></ul>
<div class="duo">{img('e-zima','Szpital Eskulap w Osielsku, widok z lotu ptaka')}{img('e-lato','Wejście główne do szpitala Eskulap, z parkingiem przy wejściu')}</div>
<div class="gal">{img('e-sala','Pracownia angiografii cyfrowej Siemens')}{img('e-tomo','Tomograf komputerowy Siemens SOMATOM')}{img('e-recep2','Recepcja i poczekalnia')}{img('e-pokoj','Jasny pokój chorych z regulowanym łóżkiem i klimatyzacją')}</div>
<h3>Dojazd i wejścia do budynku</h3>
<p>Na zabieg przyjeżdża się do szpitala po konsultacji w Bydgoszczy lub Poznaniu. Plan pokazuje wejścia do budynku: do izby przyjęć i na oddziały prowadzi wejście nr 1.</p>
<div class="map">{img('e-mapa','Plan terenu szpitala Eskulap: wejścia, parkingi P1–P4, wjazd od ulicy Tymiankowej')}</div>""", "szpital")

def faq_block(items):
    d = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)
    return sec("Pytania", d, "pytania", "faq")

def more_links(items):
    li = "".join(f'<li><a href="{u}"><b>{t}</b><span>{d}</span></a></li>' for u, t, d in items)
    return sec("Zobacz także", f'<ul class="cards">{li}</ul>', cls="wide")

FAQ_COMMON = [
 ("Czy przepuklina brzuszna może sama zniknąć?", "Nie. Gdy przepuklina się pojawi, sama już nie zniknie. Jedyną metodą leczenia jest operacja."),
 ("Ile kosztuje operacja?", "Koszt zostanie jednoznacznie określony po zbadaniu chorego. Dolna granica to 6000 zł (prosta przepuklina o średnicy wrót 1–2 cm, którą można zamknąć przez zeszycie szwami). <a href='/koszt-operacji-przepukliny-brzusznej/'>Szczegóły</a>."),
 ("Czy pacjent jest winny powstania przepukliny pooperacyjnej?", "Nie. Operowany pacjent nigdy nie jest winny powstania przepukliny."),
 ("Czy można odbyć konsultację online?", "Tak (Skype, WhatsApp, Messenger lub Zoom, praktycznie codziennie o 20.00). "+"Pacjenta z przepukliną brzuszną nie można zakwalifikować do leczenia po konsultacji online. Podczas rozmowy mogę przekazać tylko ogólne informacje, ponieważ każdy przypadek jest inny i nie ma standardowego postępowania. W trakcie takiej rozmowy dopytam dokładnie o stan zdrowia pacjenta i opiszę wymagane przygotowanie do zabiegu. Omówię również organizację leczenia, długość pobytu i związane z tym koszty. Jednak do ostatecznej kwalifikacji niezbędne jest osobiste badanie chorego. W przypadku przepukliny brzusznej badanie jest wymagane za każdym razem, a czasami także tomografia komputerowa lub inne badania dodatkowe."),
]

ALL = [
 ("/przepuklina-brzuszna-objawy-zdjecia/", "Wygląd, objawy", "Zdjęcia i skutki odkładania operacji"),
 ("/przepuklina-pooperacyjna/", "Przepuklina pooperacyjna", "Przepuklina w bliźnie po operacji"),
 ("/operacja-przepukliny-brzusznej/", "Metody operacji", "Szwy, siatka, laparoskopia, plastyka brzucha"),
 ("/koszt-operacji-przepukliny-brzusznej/", "Konsultacje i koszt", "Gdzie przyjmuję i operuję, ile to kosztuje"),
]

# ============ STRONA GŁÓWNA ============
home = hero("", "<span>Operuję przepukliny brzuszne.</span> <span>To moja specjalizacja.</span>",
            "Konsultacje w Bydgoszczy i Poznaniu oraz online. Operacje w prywatnym szpitalu Eskulap w Osielsku koło Bydgoszczy.")
home += """<div class="facts"><div><b>12 lat</b><span>kierownik uniwersyteckiej kliniki chirurgii w Bydgoszczy</span></div><div><b>od 2012</b><span>profesor chirurgii</span></div><div><b>od 6000 zł</b><span>koszt operacji prostej przepukliny; dokładny koszt ustalam po badaniu</span></div></div>"""
home += sec("Problem", """<p>Gdy jama brzuszna jest otwierana cięciem chirurgicznym, jest <b>duże ryzyko powstania przepukliny pooperacyjnej</b>. Przepuklina w bliźnie może się pojawić od razu po operacji, po miesiącach, a nawet po wielu latach. Są też przepukliny po operacjach laparoskopowych. Bywają też takie, które powstają samoistnie.</p>
<p><b>Gdy przepuklina się pojawi, sama już nie zniknie. Jedyna rada to operacja.</b> Nigdy nie należy dopuszczać do zaawansowanego stanu choroby.</p>""", "problem")
DESC = {"/przepuklina-brzuszna-objawy-zdjecia/": "Jak wygląda, objawy, zdjęcia i skutki odkładania operacji",
        "/przepuklina-pooperacyjna/": "Przepuklina w bliźnie po operacji",
        "/operacja-przepukliny-brzusznej/": "Szwy, siatka, laparoskopia, plastyka brzucha",
        "/koszt-operacji-przepukliny-brzusznej/": "Gdzie przyjmuję i operuję, ile to kosztuje"}
def _tile(u, t):
    if u: return f'<li><a href="{u}"><b>{t}</b></a></li>'
    return f'<li class="soon" title="w przygotowaniu"><b>{t}</b></li>'
def _tiles_from_menu():
    out = ""; seen_group = False; tail = ""
    for it in NAV_ITEMS[1:]:
        if it[0] == "link":
            if seen_group: tail += _tile(it[1], it[2])
            else: out += f'<ul class="cards">{_tile(it[1], it[2])}</ul>'
        else:
            seen_group = True
            out += f'<h3 class="grp">{it[1]}</h3><ul class="cards">' + "".join(_tile(u, t) for u, t in it[2]) + '</ul>'
    if tail: out += f'<h3 class="grp">Przygotowanie i konsultacje</h3><ul class="cards">{tail}</ul>'
    return out
home += sec("Dlaczego operować", f"""<div class="why"><div><p>Przepuklina to na początku defekt kosmetyczny, ale gdy się powiększa, zaczyna stopniowo coraz bardziej utrudniać życie. Nieleczona może doprowadzić do tego, że do worka przepuklinowego przemieszczą się wszystkie jelita. Może dojść do ich uwięźnięcia i zadzierzgnięcia, co jest ostrym problemem i wymaga pilnego leczenia szpitalnego. Nie lekceważ więc przepukliny.</p>
<p><a href="/przepuklina-brzuszna-objawy-zdjecia/">Objawy, objawy alarmowe i zdjęcia →</a></p></div>
<figure class="ph"><img src="/img/powieksza-sie.webp" width="{SIZES['powieksza-sie'][0]}" height="{SIZES['powieksza-sie'][1]}" alt="Przepuklina stopniowo się powiększa" loading="lazy"><figcaption>Przepuklina nie stoi w miejscu, powoli i stopniowo się powiększa.</figcaption></figure></div>
<div class="grid4">{img('zan1','Duża przepuklina brzuszna')}{img('zan2','Przepuklina brzuszna, widok z przodu')}{img('zan3','Przepuklina ze zmianami skóry')}{img('zan4','Duża przepuklina brzuszna, widok z boku')}</div>""", "dlaczego", "wide")
home += sec("Jakie przepukliny operuję", """<p>Zajmuję się przepuklinami ściany brzucha. Każda wymaga indywidualnego planu leczenia, ustalanego po zbadaniu chorego.</p>
<ul class="check"><li><a href="/przepuklina-pooperacyjna/"><b>Przepuklina pooperacyjna.</b></a> Powstaje w bliźnie po operacji jamy brzusznej, nawet po latach. Jest najczęstsza i najtrudniejsza w leczeniu, zwłaszcza gdy wraca po wcześniejszej naprawie.</li><li><a href="/przepuklina-kresy-bialej/"><b>Przepuklina kresy białej.</b></a> Wybrzuszenie w środku brzucha, nad pępkiem, bez wcześniejszej operacji.</li><li><a href="/przepuklina-pepkowa/"><b>Przepuklina pępkowa.</b></a> U dzieci często zamyka się sama, u dorosłych zwykle trzeba ją operować.</li><li><a href="/przepuklina-ledzwiowa/"><b>Przepuklina lędźwiowa.</b></a> W boku, najczęściej po operacji nerki.</li><li><a href="/rzadkie-przepukliny-brzuszne/"><b>Przepukliny rzadkie:</b></a> Spiegla, zasłonowa, kulszowa i kroczowa. Trudne do rozpoznania, najlepiej widać je w tomografii.</li><li><a href="/przepukliny-wewnetrzne/"><b>Przepukliny wewnętrzne.</b></a> Nie widać ich na brzuchu, mogą powstać po operacjach bariatrycznych.</li></ul>
<p class="note">Przepukliny rozworu przełykowego („przepukliny żołądka”) nie operuję. <a href="/przepuklina-rozworu-przelykowego/">Informacje o nich</a> podaję tylko jako wyjaśnienie.</p>""", "rodzaje")
home += sec("Jak operuję", """<p>Zasada jest prosta: naprawa <b>bez napięcia</b>, a jeśli się da, metodą małoinwazyjną. Niewielki ubytek (1–2 cm) zamykam samymi szwami. Większe przepukliny wzmacniam siatką, bo zmniejsza ona liczbę nawrotów.</p>
<ul class="check"><li><a href="/operacja-laparoskopowa-przepukliny-brzusznej/"><b>Laparoskopia</b></a> przy przepuklinach małych i średnich (do 5–8 cm): mniej zakażeń rany, krótszy pobyt.</li><li><a href="/operacja-hybrydowa-przepukliny-brzusznej/"><b>Metoda hybrydowa</b></a> przy średnich i dużych (5–10 cm) oraz przy gęstych zrostach.</li><li><a href="/operacja-klasyczna-przepukliny-brzusznej/"><b>Operacja „na otwarto”</b></a> przy dużych i złożonych przepuklinach. Gdy przepuklina jest rozległa, jednocześnie można wykonać plastykę brzucha.</li></ul>
<p><a href="/operacja-przepukliny-brzusznej/">Przegląd metod →</a></p>""", "metody")
home += sec("Wyniki i przygotowanie", """<p>Po jednej operacji z siatką trwałe wyleczenie uzyskuje się według danych światowych u większości chorych, zwykle u 85–98%. Najtrudniejsze są duże przepukliny pooperacyjne. Ryzyko nawrotu zwiększają otyłość, palenie papierosów i cukrzyca. Przed operacją warto przestać palić co najmniej 4 tygodnie, a przy otyłości zmniejszyć masę ciała. Każdy zakwalifikowany pacjent dostaje ode mnie szczegółowe zalecenia na piśmie, przed i po operacji.</p>
<p><a href="/wyniki-leczenia-przepukliny-brzusznej/">Wyniki leczenia i jak się przygotować →</a></p>""", "wyniki")
home += consult_short()
home += sec("Lekarz", f"""<div class="about">{img('prof','Prof. Stanisław Dąbrowiecki')}<div>
<p class="sig"><b>Profesor Stanisław Dąbrowiecki</b><br>chirurg</p>
<p><a href="/koszt-operacji-przepukliny-brzusznej/#o-mnie">Więcej o mnie</a></p></div></div>""", "o-mnie")
home += opinions_block()
home += faq_block([FAQ_COMMON[0], FAQ_COMMON[2], FAQ_COMMON[1]])
home += sec("Kontakt", f'<p>Telefon i WhatsApp: <a href="tel:+48{TEL}">{TELF}</a><br>E-mail: <a href="mailto:{EMAIL}">{EMAIL}</a></p>{CTA}', "kontakt")
open(f"{OUT}/index.html", "w", encoding="utf-8").write(page("/", "Przepuklina brzuszna: operacja, zdjęcia, koszty | Prof. Dąbrowiecki",
    "Jak wygląda przepuklina brzuszna i pooperacyjna, kiedy operować, ile kosztuje. Prof. Dąbrowiecki, chirurg: konsultacje Bydgoszcz, Poznań, online.", home))

def write(path, title, desc, body):
    d = f"{OUT}{path}"; os.makedirs(d, exist_ok=True)
    open(f"{d}index.html", "w", encoding="utf-8").write(page(path, title, desc, body))

# ============ OBJAWY I ZDJĘCIA ============
b = hero("Przepuklina brzuszna", "Przepuklina brzuszna. Wygląd, objawy",
         "Zdjęcia przepuklin zaniedbanych oraz informacje, dlaczego nie wolno odkładać operacji.")
b += sec("Co to jest", f"""<p>Przepuklina brzuszna to wypuklenie zawartości jamy brzusznej przez osłabione miejsce w ścianie brzucha. Najczęściej powstaje w bliźnie po wcześniejszej operacji (przepuklina pooperacyjna), ale bywa też, że powstaje samoistnie.</p>
<p>Rozpoznanie ustalam podczas badania. Mogą być wymagane dodatkowe badania (USG, tomografia, rezonans magnetyczny).</p>""")
b += sec("Objawy", f"""<p>Przepuklina, którą da się wsunąć z powrotem do brzucha, daje takie objawy (od najczęstszych):</p>
<ol class="reasons"><li><b>Wybrzuszenie pod skórą.</b> To zwykle pierwszy objaw. Powiększa się przy kaszlu, staniu, wysiłku i parciu, a znika po położeniu się lub po wsunięciu ręką.</li><li><b>Uczucie ciężkości, ciągnięcia lub pełności</b> w tym miejscu.</li><li><b>Ból lub dyskomfort.</b> Nasila się przy kaszlu, wypróżnianiu, oddawaniu moczu, wysiłku i współżyciu. Zwykle jest najgorszy pod koniec dnia, a mija po położeniu się.</li><li><b>Ból piekący lub ostry</b> promieniujący w okolicę przepukliny.</li></ol>
<p>Zdarza się, że przepuklina nie boli i widać tylko wybrzuszenie. To nie znaczy, że można czekać: przepuklina sama nie zniknie i z czasem się powiększa.</p>""", "objawy")
b += sec("Objawy alarmowe", f"""<div class="two"><figure class="ph gifx"><img src="/img/uwiezniecie.webp" width="{SIZES['uwiezniecie'][0]}" height="{SIZES['uwiezniecie'][1]}" alt="Uwięźnięcie jelita w przepuklinie" loading="lazy"><figcaption>Uwięźnięcie jelita w przepuklinie.</figcaption></figure><div><p>Powikłanie rozwija się w dwóch krokach. Najpierw <b>uwięźnięcie</b>: przepuklinę nie da się już wsunąć. Potem <b>zadzierzgnięcie</b>: jelito traci dopływ krwi i obumiera.</p>
<p>Objawy, od wczesnych do późnych:</p>
<ol class="reasons"><li>wybrzuszenie, które wcześniej dawało się wsunąć, teraz „nie wchodzi” (może jeszcze nie boleć),</li><li>narastająca tkliwość i ból nad przepukliną,</li><li>nagły, bardzo silny ból,</li><li>kurczowy ból brzucha, nudności, wymioty, brak oddawania gazów i stolca, wzdęcie,</li><li>zaczerwienienie, obrzęk i ocieplenie skóry nad przepukliną,</li><li>późno: twarda, bardzo bolesna masa, gorączka, przyspieszone tętno, spadek ciśnienia, splątanie, krew w wymiocinach lub w stolcu.</li></ol></div></div>
<div class="callout"><p><b>Zgłoś się natychmiast do szpitala (lub wezwij pogotowie), gdy przepuklina przestanie się wsuwać albo pojawi się silny ból, wymioty lub brak oddawania gazów.</b> Nie czekaj do rana.</p></div>
<p>Groźniejsze są przepukliny o <b>małych wrotach</b>: im mniejszy otwór, tym większe ryzyko zadzierzgnięcia. Przepukliny o bardzo wąskich wrotach (zasłonowa, kulszowa) bywają rozpoznane dopiero wtedy, gdy wywołają niedrożność jelit.</p>""", "alarm", "wide")
b += sec("To tylko na SOR", f"""<p><b>Czy badania krwi pokażą, że jelito obumarło?</b> Częściowo. Ma to znaczenie głównie na szpitalnym oddziale ratunkowym (SOR), gdy chory trafia z podejrzeniem uwięźnięcia. W mojej praktyce, przy planowych operacjach, nie ma praktycznie zastosowania, bo o pilnej operacji decydują objawy i badanie chorego. Badania opisane w literaturze (głównie przy przepuklinach pachwinowych i udowych) wskazują, że martwicę jelita zapowiadają:</p>
<ul class="check"><li>objawy niedrożności jelit i długi czas od początku dolegliwości do operacji (np. powyżej 16–26 godzin),</li><li>podwyższone wskaźniki zapalenia: liczba białych krwinek, stosunek neutrofili do limfocytów (NLR), CRP,</li><li>wyższy mleczan, mocznik i bilirubina oraz niski sód.</li></ul>
<p>Żaden z tych wyników nie wyklucza martwicy, gdy jest prawidłowy. Dlatego decyzję podejmuje się na podstawie objawów, badania chorego i tomografii z kontrastem, a nie samych badań krwi.</p>""", "ciekawostka", "wide")
b += sec("Zdjęcia", f"""<p>Na zdjęciach skutki braku operacji. Przepukliny powiększały się przez lata. Lekceważono objawy, a operacja była stale odkładana na później; czasami przez pacjenta, bywa że przez lekarza.</p>
<div class="grid4 g3">{img('zan1','Duża przepuklina brzuszna')}{img('zan2','Przepuklina brzuszna, widok z przodu')}{img('zan4','Duża przepuklina brzuszna, widok z boku')}</div>
<h3>Przepuklina powikłana</h3>
<p>Worek przepuklinowy uciska skórę, która go pokrywa. Na skórze powstają zmiany wynikające z tego ucisku. Powodują one zmiany niedokrwienne, czyli skóra jest coraz gorzej ukrwiona. Gdy zmiany się nasilą, może dojść do pęknięcia skóry na worku przepuklinowym.</p>
<div class="grid4 g3 sq">{img('zan3','Przepuklina powikłana zmianami niedokrwiennymi skóry')}{img('powikl1','Przepuklina powikłana zmianami niedokrwiennymi skóry, widok z przodu')}{img('powikl2','Przepuklina powikłana zmianami skórnymi, widok z góry')}</div>
<p class="note">Na zdjęciach wyżej skóra nad przepukliną nie wytrzymuje napięcia i stopniowo ulega martwicy. Z czasem dojdzie do pęknięcia i wydostania się jelit na zewnątrz. To będzie już dramat: pęknięta przepuklina na brzuchu.</p>
<p><b>Każda z tych przepuklin zaczynała się jako niewielkie uwypuklenie na ścianie brzucha. W tym momencie była łatwa do zaopatrzenia chirurgicznego, a zabieg nie był obciążający dla pacjenta. Lekceważenie problemu lub złe porady powodowały odkładanie zabiegu na wiele lat.</b></p>
<p><b>Nigdy nie można dopuszczać do tak zaawansowanego stanu choroby.</b> Pacjent staje się inwalidą.</p>""", "zdjecia", "wide")
b += sec("Pacjent nie jest winny", """<p>Operowany pacjent <b>nigdy</b> nie jest winny powstania przepukliny. Bywa, że pacjent jest obwiniany: „za szybko wstał Pan z łóżka po operacji”. To nie jest prawda i to nie jest przyczyna przepukliny. Nie dajcie sobie tego wmówić.</p>""")
b += sec("Kto jest zagrożony", f"""<p>Niebezpieczeństwo wystąpienia przepukliny jest większe u osób z nadwagą lub otyłością oraz po pilnych operacjach. Również w takiej sytuacji można chorym pomóc. Gdy można przesunąć operację o kilka miesięcy, należy spróbować odchudzić pacjenta. U osoby otyłej należy jednocześnie wykonać plastykę brzucha: zlikwidować przepuklinę oraz usunąć nadmiar tłuszczu z brzucha.</p>
<div class="duo">{img('przed1','Przepuklina brzuszna u osoby otyłej, przed operacją')}{img('przed2','Przepuklina brzuszna, widok z boku, przed operacją')}</div>""")
b += more_links(ALL[1:])
b += faq_block([('Jak rozpoznać, że mam przepuklinę brzuszną?', 'Najczęściej jest to wybrzuszenie pod skórą, które powiększa się przy kaszlu, staniu lub wysiłku, a po położeniu się znika albo da się je wsunąć. Może towarzyszyć uczucie ciężkości lub ciągnięcia i ból, który narasta pod koniec dnia. Ostateczne rozpoznanie stawia lekarz po zbadaniu chorego, a w trudnych przypadkach pomaga USG lub tomografia.'), ('Kiedy przepuklina brzuszna wymaga pilnej pomocy?', 'Gdy wybrzuszenie przestaje się wsuwać, pojawia się silny ból, wymioty, wzdęcie brzucha albo brak oddawania gazów i stolca. To może być uwięźnięcie jelita, a potem jego zadzierzgnięcie, czyli obumarcie. Nie należy wtedy czekać do rana, tylko jechać do szpitala. Groźniejsze są przepukliny o małym otworze.'), ('Czy przepuklina, która nie boli, musi być operowana?', 'Brak bólu nie oznacza, że można czekać. Przepuklina sama nie zniknie, z czasem się powiększa, a duże przepukliny są trudniejsze do operacji i wymagają dłuższej rekonwalescencji. Jedyną metodą leczenia jest operacja, a im wcześniej, tym zwykle jest prostsza.')])
write("/przepuklina-brzuszna-objawy-zdjecia/", "Przepuklina brzuszna. Wygląd, objawy | Prof. Dąbrowiecki",
      "Jak wygląda przepuklina brzuszna? Zdjęcia, skutki odkładania operacji i kto jest zagrożony. Prof. Dąbrowiecki, konsultacje w Bydgoszczy i Poznaniu.", b)

# ============ POOPERACYJNA ============
b = hero("Przepuklina w bliźnie", "Przepuklina pooperacyjna: leczenie i operacja",
         "Przepuklina w bliźnie po operacji jamy brzusznej. Jak powstaje i jak ją leczę.")
b += sec("Zdjęcia", f"""<div class="grid4 g3">{img('po1','Duża przepuklina pooperacyjna w bliźnie pośrodku brzucha')}{img('po2','Przepuklina pooperacyjna w bliźnie pośrodku brzucha, widok z przodu')}{img('po3','Przepuklina pooperacyjna z bliznami po wielu operacjach, widok z przodu')}</div>
<p>Zaawansowane, duże przepukliny brzuszne, które powstały w bliźnie pooperacyjnej w wyniku nieprawidłowego gojenia rany operacyjnej.</p>""")
b += sec("Czym jest i jak często", f"""<p>Przepuklina w bliźnie to wypuklenie zawartości jamy brzusznej przez osłabione miejsce w ścianie brzucha, najczęściej tam, gdzie wcześniej była cięta skóra i mięśnie. Gdy się pojawi, sama już nie zniknie.</p>
<p>Po cięciu pośrodku brzucha przepuklina powstaje u około 10–20% chorych. U osób z grupy podwyższonego ryzyka nawet u 30–44%. Po operacjach laparoskopowych zdarza się rzadziej (około 1–3%), ale ryzyko rośnie u osób obciążonych chorobami.</p>
<p>Operowany pacjent <b>nigdy</b> nie jest winny powstania przepukliny. To, że „za szybko wstał z łóżka po operacji", nie jest jej przyczyną.</p>""")
b += sec("Po jakich operacjach", f"""<p>Przepuklina może powstać po każdym zabiegu, w którym otwierano jamę brzuszną. Najczęściej są to:</p>
<ul class="check"><li>operacje jelit, żołądka, trzustki, wątroby i pęcherzyka żółciowego,</li><li>operacje ginekologiczne i cięcie cesarskie,</li><li>operacje dużych naczyń w brzuchu (np. poszerzenia aorty),</li><li>operacje otyłości, jeżeli były wykonywane „na otwarto",</li><li>zamykanie sztucznego odbytu i miejsce, w którym go wyłoniono.</li></ul>
<p>Przepuklina może też powstać po operacjach laparoskopowych, najczęściej w miejscu, przez które wprowadzano grubsze narzędzia, zwykle przy pępku.</p>""")
b += sec("Kiedy się pojawia", f"""<p>Przepuklina zaczyna się najczęściej od nieprawidłowego gojenia ściany brzucha, często już w pierwszym miesiącu po operacji. Wybrzuszenie może jednak być widoczne dopiero po miesiącach, a nawet po latach. Po roku przepuklinę ma około 5% operowanych, a po dwóch latach około 10%.</p>""")
b += sec("Kto jest bardziej narażony", f"""<p>Przepuklina powstaje częściej, gdy:</p>
<ul class="check"><li>rana po operacji uległa zakażeniu (to najsilniejszy czynnik, który można ograniczyć),</li><li>pacjent jest otyły,</li><li>pacjent pali papierosy,</li><li>pacjent ma cukrzycę, zwłaszcza źle wyrównaną,</li><li>pacjent ma przewlekłą chorobę płuc i kaszle (kaszel podnosi ciśnienie w brzuchu),</li><li>pacjent jest w podeszłym wieku, niedożywiony, przyjmuje sterydy lub leki obniżające odporność,</li><li>pacjent ma chorobę tkanki łącznej albo poszerzenie aorty w brzuchu.</li></ul>
<p>Znaczenie ma też sposób operacji: cięcie pośrodku brzucha, technika zamknięcia rany, chemioterapia i przetoczenia krwi.</p>""")
b += sec("Objawy", f"""<p>Pierwszym objawem jest zazwyczaj wybrzuszenie w bliźnie, bardziej widoczne w pozycji stojącej, przy kaszlu lub wysiłku. Czasem znika w pozycji leżącej. Może się pojawić:</p>
<ul class="check"><li>ból lub uczucie ciągnięcia w okolicy blizny,</li><li>uczucie ciężkości i szybkie męczenie się,</li><li>wzdęcia, kłopoty z wypróżnianiem, nudności po jedzeniu,</li><li>ból pleców lub trudności w wykonywaniu codziennych czynności.</li></ul>
<p>Mała przepuklina może przez długi czas nie dawać żadnych dolegliwości, a mimo to wymaga leczenia.</p>""")
b += sec("Jak zmienia się w czasie", f"""<p>Przepuklina zwykle powiększa się z czasem. Otwór w ścianie brzucha stopniowo się poszerza, a do worka przepuklinowego wchodzi coraz więcej jelit. Wybrzuszenie rośnie, ściana brzucha cieńsieje, a dolegliwości narastają, czyli ból, dyskomfort, ograniczenie aktywności i problemy estetyczne.</p>
<p>Duże przepukliny są trudniejsze do operacji, wymagają rozleglejszego zabiegu i dłuższej rekonwalescencji. Dlatego nie warto czekać, aż przepuklina urośnie.</p>""")
b += sec("Powikłania", f"""<div class="two"><figure class="ph gifx"><img src="/img/uwiezniecie.webp" width="{SIZES['uwiezniecie'][0]}" height="{SIZES['uwiezniecie'][1]}" alt="Uwięźnięcie jelita w przepuklinie: jelito zostaje uwięzione w worku przepuklinowym i traci dopływ krwi" loading="lazy"><figcaption>Uwięźnięcie jelita w przepuklinie.</figcaption></figure><div><p>Najgroźniejsze powikłanie to <b>uwięźnięcie</b>: jelito zostaje uwięzione w przepuklinie i nie można go wsunąć z powrotem do brzucha. Może dojść do niedrożności jelit i do <b>zadzierzgnięcia</b>, czyli odcięcia dopływu krwi do jelita. Jelito obumiera i przestaje przepuszczać treść. Takie powikłania wymagają <b>pilnej operacji w szpitalu</b>.</p>
<p>Uwięźnięcie zdarza się w ciągu życia u około 6–15% chorych z przepukliną, a niedrożność jelit u 10–15%.</p>
<p>Operacja pilna jest obarczona większym ryzykiem powikłań niż zabieg planowy. Inne powikłania nieleczonej przepukliny to przewlekły ból, niedokrwienie i zmiany martwicze skóry nad workiem przepuklinowym. Zaawansowana przepuklina może prowadzić do trwałego kalectwa.</p></div></div>""")
b += sec("Kiedy pilnie do lekarza", f"""<div class="callout"><p><b>Zgłoś się natychmiast do szpitala, gdy pojawi się:</b> nagły ból, twarde i bolesne wybrzuszenie, którego nie da się wsunąć z powrotem, nudności lub wymioty, wzdęcie brzucha albo brak oddawania gazów i stolca. To objawy uwięźnięcia lub zadzierzgnięcia jelita.</p></div>""")
b += sec("Jak zmniejszyć ryzyko", f"""<p>Ryzyko przepukliny po operacji można zmniejszyć. Warto:</p>
<ul class="check"><li>przestać palić papierosy,</li><li>zmniejszyć masę ciała,</li><li>wyrównać cukrzycę,</li><li>unikać dźwigania i dużego wysiłku w czasie gojenia,</li><li>dbać o ranę i od razu zgłaszać oznaki zakażenia (zaczerwienienie, ropa, gorączka).</li></ul>
<p>Sama operacja naprawcza również niesie ryzyko nawrotu przepukliny i przewlekłego bólu, dlatego ważny jest wybór metody i doświadczenie operatora.</p>""")
b += sec("Plastyka brzucha", f"""<p>Przy rozległej przepuklinie, otyłości, ale też u osób masywnie odchudzonych, wykonuje się jednocześnie likwidację przepukliny oraz plastykę brzucha. Polega to na usunięciu rozciągniętej ściany brzucha. Najlepiej, gdy po operacji brzuch jest płaski. Operacja jest bardziej rozległa, ale efekt leczenia jest bardzo dobry.</p>
<div class="duo">{img('plast-przed','Przepuklina pooperacyjna u osoby otyłej, przed operacją','przed operacją')}{img('plast-po','Brzuch po operacji przepukliny z plastyką brzucha','po operacji')}</div>""")
b += sec("Przepuklina nawrotowa", """<p>Przepuklina brzuszna nawrotowa to przepuklina, która ponownie wystąpiła po wcześniejszym leczeniu. Podobnie jak przepuklina bardzo duża i lędźwiowa wymaga starannej oceny przed operacją. Operacja może być klasyczna lub laparoskopowa, a koszt jest ustalany po zbadaniu pacjenta.</p>""")
b += sec("Plan leczenia", """<p>W leczeniu przepuklin są ustalone schematy postępowania. Różnimy się jednak między sobą, dlatego u każdego chorego z przepukliną ustalam osobny plan leczenia oraz metodę operacyjną.</p>""")
b += more_links([ALL[0], ALL[2], ALL[3]])
b += faq_block([('Czy to ja jestem winny, że po operacji powstała przepuklina?', 'Nie. Operowany pacjent nigdy nie jest winny powstania przepukliny. To, że „za szybko wstał z łóżka”, nie jest jej przyczyną. Ryzyko zależy m.in. od zakażenia rany, otyłości, palenia, cukrzycy, techniki zamknięcia brzucha i tego, czy operacja była pilna.'), ('Po ilu miesiącach lub latach od operacji może pojawić się przepuklina w bliźnie?', 'Zaczyna się zwykle od nieprawidłowego gojenia ściany brzucha, często już w pierwszym miesiącu, ale wybrzuszenie bywa widoczne dopiero po miesiącach, a nawet po latach. Po roku przepuklinę ma około 5% operowanych, a po dwóch latach około 10%. Dlatego blizny warto obserwować także długo po operacji.'), ('Czy mała przepuklina w bliźnie też wymaga operacji?', 'Tak. Mała przepuklina może długo nie dawać dolegliwości, ale sama nie zniknie i z czasem rośnie. Otwór w ścianie brzucha się poszerza, a do worka wchodzi coraz więcej jelit. Dlatego nie warto czekać, aż urośnie, bo duże przepukliny są trudniejsze do operacji.')])
write("/przepuklina-pooperacyjna/", "Przepuklina pooperacyjna: leczenie, operacja | Prof. Dąbrowiecki",
      "Przepuklina pooperacyjna (w bliźnie): jak powstaje, jak ją operuję, także z plastyką brzucha. Konsultacje w Bydgoszczy i Poznaniu oraz online.", b)

# ============ METODY ============
b = hero("Operacja przepukliny brzusznej", "Operacja przepukliny brzusznej: metody",
         "Szwy, siatka, laparoskopia lub operacja „na otwarto”. Metodę wybieram po zbadaniu chorego.")
b += sec("Na czym polega", """<p>Operacja przepukliny brzusznej polega na przesunięciu tego, co jest poza brzuchem (w worku przepuklinowym), z powrotem na miejsce, do jamy brzusznej. Następnie zeszywa się otwór przepuklinowy oraz wzmacnia osłabione miejsce w ścianie brzucha, aby nie doszło do nawrotu przepukliny.</p>
<p>Naprawa jest najlepsza, gdy możliwe jest odtworzenie silnej ściany brzucha. <b>Niewielkie otwory przepuklinowe można jedynie zeszyć.</b> W innych przypadkach do wzmocnienia miejsca zeszycia stosuje się materiały sztuczne, czyli siatki. Jest to bezpieczne postępowanie, sprawdzone przez ostatnie 60 lat.</p>""")
b += sec("Laparoskopia", f"""<p>Przepukliny o niewielkich i średnich rozmiarach (do 5–8 cm) można operować laparoskopowo. Przy większych rozmiarach zaleca się operację „na otwarto”, poprzez cięcie ściany brzucha.</p>
<div class="grid3">{img('lapar','Laparoskopowa naprawa przepukliny powyżej pępka','laparoskopowa naprawa przepukliny powyżej pępka w linii pośrodkowej ciała')}{img('otwarta','Operacja na otwarto, wypreparowana ściana brzucha','wypreparowana ściana powłoki brzusznej, przygotowana do wszczepienia siatki')}{img('siatka','Siatka przygotowywana do wszczepienia','siatka przygotowywana do wszczepienia w ścianę brzucha')}</div>""", "metody", "wide")
b += sec("Siatka", f"""<p>W zależności od metody operacyjnej siatka może być wprowadzona do różnych warstw ściany brzucha (na rysunku oznaczone numerami 1–5).</p>{img('warstwy','Warstwy ściany brzucha, w które można wprowadzić siatkę')}""")
b += sec("Metoda według rodzaju", f"""<p>Metodę wybiera się według rodzaju i miejsca przepukliny, wielkości otworu i tego, czy operacja jest planowa, czy pilna. Zasada jest jedna: naprawa <b>bez napięcia</b>, z siatką, a jeśli się da, metodą małoinwazyjną (laparoskopia). Taka operacja mniej boli, pobyt w szpitalu jest krótszy, a powrót do aktywności szybszy, przy podobnej liczbie nawrotów.</p>
<h3 class="grp">Przepuklina pooperacyjna i większa w linii środkowej (powyżej 2 cm)</h3>
<ul class="check"><li><b>Siatka jest standardem.</b> Przy takich przepuklinach samo zeszycie szwami daje nawroty nawet do 54%, siatka tę liczbę wyraźnie zmniejsza.</li><li><b>Siatka za mięśniem prostym brzucha</b> (sublay) jest uznawana za najlepszą. Siatka nad powięzią (onlay) jest rzadziej wybierana. Siatkę „mostkującą” stosuje się tylko wtedy, gdy nie da się zbliżyć brzegów otworu.</li><li><b>Duży otwór (powyżej 10–12 cm):</b> stosuje się rozdzielenie warstw mięśni (separację komponentów), zwłaszcza tylną. Pozwala to zbliżyć brzegi bez napięcia i umieścić siatkę w dobrze ukrwionym miejscu.</li><li><b>Metody małoinwazyjne:</b> starsza laparoskopowa metoda z siatką wewnątrz jamy brzusznej może powodować zrosty. Nowsze metody laparoskopowe umieszczają siatkę poza jamą brzuszną.</li></ul>
<h3 class="grp">Przepuklina pępkowa</h3>
<ul class="check"><li>Ubytek o średnicy 1–2 cm zamykam szwami, bez siatki.</li><li>Przy większym ubytku zaleca się siatkę. Zmniejsza ona liczbę nawrotów, a nie zwiększa liczby zakażeń rany.</li></ul>
<h3 class="grp">Przepuklina rozworu przełykowego (informacyjnie, tych przepuklin nie operuję)</h3>
<ul class="check"><li>Standardem jest laparoskopia: mniej powikłań i niższa śmiertelność niż po operacji otwartej.</li><li>Zamyka się odnogi przepony, usuwa worek i zwykle dodaje fundoplikację. Siatkę stosuje się tylko wtedy, gdy nie da się zbliżyć odnóg szwami. Rutynowa siatka nie zmniejsza liczby nawrotów.</li></ul>
<h3 class="grp">Przepukliny rzadkie (Spiegla, lędźwiowa)</h3>
<ul class="check"><li>Naprawa z siatką, a samo zeszycie tylko przy małych ubytkach.</li><li>Przepuklinę Spiegla naprawia się także wtedy, gdy nie daje objawów, bo grozi uwięźnięciem. Zwykle robi się to metodą małoinwazyjną, a „na otwarto” przy dużych przepuklinach lub w trybie pilnym, gdy trzeba usunąć fragment jelita.</li></ul>""", "wedlug-rodzaju")
b += sec("Plastyka brzucha", """<p>Przy rozległej przepuklinie brzusznej, a także u osób masywnie odchudzonych, jednocześnie z likwidacją przepukliny wykonuje się plastykę brzucha. Operacja jest bardziej rozległa, ale efekt leczenia jest bardzo dobry. Zdjęcia przed i po operacji są na stronie o <a href="/przepuklina-pooperacyjna/">przepuklinie pooperacyjnej</a>.</p>""")
b += more_links([("/operacja-klasyczna-przepukliny-brzusznej/", "Operacja klasyczna", "Kiedy wybieram operację „na otwarto”"), ("/operacja-laparoskopowa-przepukliny-brzusznej/", "Operacja laparoskopowa", "Kiedy wybieram laparoskopię"), ("/operacja-hybrydowa-przepukliny-brzusznej/", "Operacja hybrydowa", "Połączenie cięcia i laparoskopii"), ALL[1], ("/wyniki-leczenia-przepukliny-brzusznej/", "Wyniki i przygotowanie", "Rokowanie, co pogarsza wyniki, jak się przygotować"), ALL[3]])
b += faq_block([('Czy można operować laparoskopowo?', "Przepukliny o niewielkich i średnich rozmiarach (do 5–8 cm) można operować laparoskopowo. Przy większych zaleca się operację „na otwarto”, a przy średnich i dużych bywa dobra metoda łączona. Metodę wybieram po zbadaniu chorego, bo każdy przypadek jest inny. <a href='/operacja-laparoskopowa-przepukliny-brzusznej/'>Więcej o laparoskopii</a>."), ('Czy każda przepuklina wymaga siatki?', 'Nie. Niewielkie otwory można tylko zeszyć, a ubytek o średnicy 1–2 cm zamykam szwami. Przy większych ubytkach siatka wzmacnia naprawę i zmniejsza liczbę nawrotów. Siatki są używane od około 60 lat i jest to postępowanie bezpieczne i sprawdzone.'), ('Czy przy dużej przepuklinie można jednocześnie zrobić plastykę brzucha?', 'Tak. Przy rozległej przepuklinie, a także u osób masywnie odchudzonych, jednocześnie z likwidacją przepukliny wykonuje się plastykę brzucha. Operacja jest bardziej rozległa, ale efekt leczenia jest bardzo dobry. Zdjęcia przed i po są na stronie o przepuklinie pooperacyjnej.')])
write("/operacja-przepukliny-brzusznej/", "Operacja przepukliny brzusznej: metody, siatka, laparoskopia | Prof. Dąbrowiecki",
      "Na czym polega operacja przepukliny brzusznej: szwy, siatka, laparoskopia, plastyka brzucha. Prof. Dąbrowiecki, szpital Eskulap, Osielsko.", b)

# ============ KRESA BIAŁA ============
b = hero("Przepuklina w linii pośrodkowej", "Przepuklina kresy białej: objawy i leczenie",
         "Wybrzuszenie w środku brzucha, nad pępkiem lub w jego okolicy, bez wcześniejszej operacji.")
b += sec("Czym jest", f"""<p>Kresa biała to pas mocnej tkanki w środku brzucha, łączący z obu stron mięśnie proste. Przepuklina kresy białej powstaje samoistnie, bez związku z wcześniejszą operacją. W tkance powstaje ubytek, a przez niego wypycha się zawartość jamy brzusznej: tłuszcz lub fragment jelita.</p>
<p>Najczęściej występuje nad pępkiem (przepuklina nadbrzuszna) albo w okolicy pępka. Tworzy się prawdziwy worek przepuklinowy, a ciągłość kresy białej jest przerwana.</p>""")
b += sec("Objawy", f"""<p>Przepuklina bywa bez objawów. Zwykle widać lub wyczuwa się guzek w linii środkowej brzucha. Może on być większy przy kaszlu, parciu i wysiłku. Czasem pojawia się dyskomfort lub ból.</p>""")
b += sec("Powikłania", f"""<p>Jak każda przepuklina, może się uwięznąć i zadzierzgnąć, czyli jelito lub tłuszcz zostaną uwięzione w otworze i stracą dopływ krwi. To wymaga pilnej operacji. Zgłoś się natychmiast do szpitala przy nagłym bólu, twardym i bolesnym guzku, którego nie da się wsunąć, wymiotach lub braku oddawania gazów i stolca.</p>""")
b += sec("Czym różni się od rozejścia mięśni prostych", f"""<p>Rozejście mięśni prostych to coś innego. Kresa biała jest wtedy rozciągnięta i cieńsza, a mięśnie są odsunięte od siebie, ale nie ma ubytku ani worka przepuklinowego. Najczęściej zdarza się po ciąży, przy otyłości i w starszym wieku. Daje wałeczkowate wybrzuszenie przy napięciu brzucha i nie grozi uwięźnięciem.</p>
<ul class="check"><li><b>Przepuklina:</b> prawdziwy ubytek i worek, ryzyko uwięźnięcia, leczenie operacyjne.</li><li><b>Rozejście mięśni:</b> brak ubytku i worka, bez ryzyka uwięźnięcia, najpierw leczenie zachowawcze (ćwiczenia), czasem operacja.</li></ul>
<p>Oba stany mogą występować jednocześnie, zwłaszcza przy małej przepuklinie. Rozpoznaję je po zbadaniu chorego, a w trudnych przypadkach po USG lub tomografii.</p>""")
b += more_links([ALL[0], ALL[1], ALL[2]])
b += faq_block([('Czym przepuklina kresy białej różni się od rozejścia mięśni prostych?', 'W przepuklinie jest prawdziwy ubytek w powięzi i worek, więc grozi uwięźnięciem. W rozejściu mięśni kresa biała jest tylko rozciągnięta i cieńsza, bez ubytku i bez worka, i nie grozi uwięźnięciem. Oba stany mogą występować razem. Różnicę ustalam po zbadaniu chorego, a w wątpliwych przypadkach po USG lub tomografii.'), ('Czy przepuklina nad pępkiem może nie dawać żadnych objawów?', 'Tak, bywa bezobjawowa. Zwykle widać lub wyczuwa się guzek w linii środkowej brzucha, który powiększa się przy kaszlu i parciu. Brak bólu nie oznacza jednak, że przepuklina jest niegroźna, bo może się uwięznąć i zadzierzgnąć.'), ('Jak leczy się przepuklinę kresy białej?', "Leczenie jest operacyjne. Ubytek o średnicy 1–2 cm zamykam szwami, a przy większym zaleca się siatkę, która zmniejsza ryzyko nawrotu. Szczegóły opisuję na stronie o metodach operacji. <a href='/operacja-przepukliny-brzusznej/'>Metody operacji</a>.")])
write("/przepuklina-kresy-bialej/", "Przepuklina kresy białej (nadbrzuszna): objawy, leczenie | Prof. Dąbrowiecki",
      "Przepuklina kresy białej: czym jest, objawy, powikłania, różnica od rozejścia mięśni prostych i leczenie. Prof. Dąbrowiecki, Bydgoszcz.", b)

# ============ PĘPKOWA ============
b = hero("Przepuklina przy pępku", "Przepuklina pępkowa: objawy i leczenie",
         "Wybrzuszenie w pępku lub tuż przy nim. Czym jest, kiedy jest groźna i jak ją leczę.")
b += sec("Czym jest i jak częsta", f"""<p>Przepuklina pępkowa to wypuklenie zawartości jamy brzusznej (tłuszczu lub jelita) przez osłabione miejsce w ścianie brzucha przy pępku, czyli w miejscu po pępowinie. Za przepuklinę pępkową uznaje się ubytek w linii środkowej brzucha od 3 cm powyżej do 3 cm poniżej pępka.</p>
<p>Występuje u około 2–4% dorosłych i stanowi 6–14% wszystkich przepuklin ściany brzucha.</p>""")
b += sec("U dzieci i u dorosłych", f"""<p>U dzieci przepuklina pępkowa wynika z niepełnego zamknięcia pierścienia pępkowego i w około 90% przypadków zamyka się sama do wieku przedszkolnego.</p>
<p>U dorosłych jest zwykle nabyta: powstaje przy wzroście ciśnienia w brzuchu i rzadko cofa się sama. Częściej wymaga operacji.</p>""")
b += sec("Jak wygląda", f"""<p>Przepuklina pępkowa u dorosłych może wyglądać bardzo różnie, od niewielkiego wybrzuszenia w pępku po dużą przepuklinę wysuwającą się ponad skórę.</p>
<div class="grid3">{img('pep2','Mała przepuklina pępkowa u kobiety','mała przepuklina pępkowa: wybrzuszenie w pępku')}{img('pep3','Duża przepuklina pępkowa u mężczyzny','duża przepuklina pępkowa u osoby z otyłością')}{img('pep1','Duża przepuklina pępkowa z przebarwieniem skóry','duża przepuklina z przebarwieniem skóry nad nią')}</div>
<p class="note">Na ostatnim zdjęciu skóra nad przepukliną jest przebarwiona. Zmiany skóry nad przepukliną (zaczerwienienie, sine lub ciemne zabarwienie) to sygnał, że jest zagrożony dopływ krwi. Z takim objawem trzeba pilnie zgłosić się do lekarza.</p>""", "zdjecia", "wide")
b += sec("Kto jest bardziej narażony", f"""<p>U dorosłych przepuklina pępkowa powstaje częściej przy:</p>
<ul class="check"><li>otyłości,</li><li>wielu ciążach i porodach (rozciągnięcie pierścienia pępkowego),</li><li>wodobrzuszu przy marskości wątroby,</li><li>przewlekłym kaszlu, zaparciach lub dużym guzie w brzuchu (stale podwyższone ciśnienie w brzuchu),</li><li>paleniu papierosów, chorobach tkanki łącznej i niedoczynności tarczycy. Częściej chorują mężczyźni w wieku 41–80 lat.</li></ul>""")
b += sec("Objawy", f"""<p>Przepuklina często nie boli. Widać lub wyczuwa się wybrzuszenie przy pępku, które jest większe przy kaszlu i parciu. Może pojawić się dyskomfort lub ból. Dla wielu osób problemem jest też wygląd, czyli „wystający pępek".</p>""")
b += sec("Powikłania", f"""<p>Najgroźniejsze jest <b>uwięźnięcie</b> i <b>zadzierzgnięcie</b>: jelito lub sieć zostają uwięzione w przepuklinie i tracą dopływ krwi. Wymaga to pilnej operacji.</p>
<div class="callout"><p><b>Zgłoś się natychmiast do lekarza lub szpitala, gdy pojawi się:</b> twarde, bolesne wybrzuszenie, którego nie da się wsunąć, nudności lub wymioty, wzdęcie brzucha albo brak oddawania gazów i stolca.</p></div>""")
b += more_links([ALL[0], ALL[1], ALL[2]])
b += faq_block([('Czy przepuklina pępkowa u dziecka zniknie sama?', 'U dzieci przepuklina pępkowa w około 90% przypadków zamyka się sama do wieku przedszkolnego, więc zwykle się czeka i obserwuje. Gdy się nie zamknie, to o dalszym postępowaniu decyduje lekarz. U dorosłych jest inaczej: przepuklina pępkowa rzadko cofa się sama.'), ('Skąd się bierze przepuklina pępkowa u dorosłych?', 'Powstaje, gdy ciśnienie w brzuchu jest podwyższone. Sprzyjają temu otyłość, wiele ciąż i porodów, wodobrzusze, przewlekły kaszel, zaparcia, palenie papierosów oraz choroby tkanki łącznej. Częściej chorują mężczyźni w wieku 41–80 lat.'), ('Czy przepuklina pępkowa jest groźna?', 'Najgroźniejsze jest uwięźnięcie i zadzierzgnięcie, czyli utrata dopływu krwi do jelita lub sieci. Alarmem są twarde, bolesne wybrzuszenie, którego nie da się wsunąć, nudności lub wymioty, wzdęcie i brak oddawania gazów. Wtedy trzeba natychmiast jechać do szpitala. Nawet bezbolesną przepuklinę warto zoperować, zanim do tego dojdzie.')])
write("/przepuklina-pepkowa/", "Przepuklina pępkowa: objawy, leczenie, operacja | Prof. Dąbrowiecki",
      "Przepuklina pępkowa u dorosłych: przyczyny, objawy, powikłania i leczenie. Małe ubytki szwami, większe z siatką. Prof. Dąbrowiecki, Bydgoszcz.", b)

# ============ LĘDŹWIOWA ============
b = hero("Przepuklina w boku brzucha", "Przepuklina lędźwiowa: objawy i rozpoznanie",
         "Wybrzuszenie w boku, w okolicy lędźwi, najczęściej po operacji nerki.")
b += sec("Czym jest", f"""<p>Przepuklina lędźwiowa to wypuklenie zawartości jamy brzusznej przez ubytek w tylnej i bocznej ścianie brzucha, w okolicy lędźwi: między ostatnim żebrem, kością biodrową i mięśniami przykręgosłupowymi. Najczęściej powstaje po operacji nerki wykonanej przez cięcie w boku.</p>
<p>W worku przepuklinowym może znaleźć się jelito grube lub cienkie, tłuszcz, a rzadko nawet nerka, śledziona czy żołądek. Dlatego grozi uwięźnięciem i zadzierzgnięciem.</p>""")
b += sec("Jak często po operacji nerki", f"""<p>Po klasycznym, otwartym cięciu w boku przepuklina powstaje u około 20–30% chorych, a w niektórych badaniach nawet u 35%. Po planowym dostępie za otrzewną ryzyko spada do około 7%. Operacje małoinwazyjne ryzyko jeszcze zmniejszają: po laparoskopii około 11%.</p>""")
b += sec("Dlaczego powstaje", f"""<p>Cięcie w boku może uszkodzić nerwy, które pobudzają mięśnie ściany brzucha. Mięśnie wtedy stopniowo zanikają, ściana brzucha cieńsieje i słabnie. To sprzyja przepuklinie, a bok brzucha może się charakterystycznie wybrzuszać.</p>""")
b += sec("Kto jest bardziej narażony", f"""<p>Przepuklina lędźwiowa powstaje częściej przy:</p>
<ul class="check"><li>otyłości (to najsilniejszy czynnik),</li><li>paleniu papierosów,</li><li>cukrzycy i nadciśnieniu,</li><li>przewlekłej chorobie płuc i chorobie wieńcowej,</li><li>ciężkiej niewydolności nerek,</li><li>dużym guzie nerki i rozległym cięciu.</li></ul>""")
b += sec("Objawy", f"""<p>Przepuklina często nie daje objawów. W boku widać miękkie wybrzuszenie, które da się wsunąć i które powiększa się przy kaszlu i parciu. Może boleć okolica lędźwi, czasem występują zmiany w oddawaniu moczu lub stolca. Objawy bywają różne i niecharakterystyczne, więc łatwo je przeoczyć.</p>""")
b += sec("Przepuklina czy wybrzuszenie boku", f"""<p>Po operacji w boku mogą wystąpić dwie różne rzeczy:</p>
<ul class="check"><li><b>Prawdziwa przepuklina:</b> jest ubytek w ścianie brzucha i worek przepuklinowy. Grozi uwięźnięciem i zadzierzgnięciem.</li><li><b>Wybrzuszenie boku (pseudoprzepuklina):</b> mięśnie są wiotkie po uszkodzeniu nerwów, ale nie ma ubytku w ścianie. Nie grozi uwięźnięciem.</li></ul>
<p>Obie te sytuacje bywają nie do odróżnienia samym badaniem, a czasem nawet badania obrazowe nie rozstrzygają. Dlatego ocena wymaga doświadczenia.</p>""")
b += sec("Rozpoznanie", f"""<p>Podstawą jest dokładne badanie chorego. Najlepszym badaniem dodatkowym jest tomografia komputerowa: pokazuje wielkość ubytku, zawartość worka i zanik mięśni oraz odróżnia przepuklinę od wybrzuszenia i od tłuszczaka. USG wykonane przez mało doświadczonego lekarza może pomylić przepuklinę z tłuszczakiem.</p>""")
b += sec("Powikłania", f"""<p>Przy przepuklinach bocznych uwięźnięcie opisuje się nawet w co czwartym przypadku, a zadzierzgnięcie u kilku do kilkunastu procent chorych.</p>
<div class="callout"><p><b>Zgłoś się natychmiast do szpitala, gdy pojawi się:</b> twarde, bolesne wybrzuszenie, którego nie da się wsunąć, nudności lub wymioty, wzdęcie brzucha albo brak oddawania gazów i stolca.</p></div>""")
b += more_links([ALL[0], ALL[1], ALL[2]])
b += faq_block([('Dlaczego po operacji nerki może powstać przepuklina w boku?', 'Rozległe cięcie w boku i uszkodzenie nerwów zasilających mięśnie osłabiają ścianę brzucha. Ryzyko zwiększają otyłość, palenie, cukrzyca, duży guz nerki i choroby płuc. Operowany pacjent nigdy nie jest winny przepukliny.'), ('Jak odróżnić przepuklinę od wybrzuszenia boku?', 'Przy prawdziwej przepuklinie jest ubytek w ścianie i worek, więc grozi uwięźnięciem. Przy wybrzuszeniu boku (pseudoprzepuklinie) mięśnie są wiotkie po uszkodzeniu nerwów, ale ubytku nie ma i nie ma ryzyka uwięźnięcia. Samo badanie nie zawsze to rozstrzyga, dlatego pomaga tomografia komputerowa.'), ('Czy do rozpoznania przepukliny lędźwiowej potrzebna jest tomografia?', 'Najlepszym badaniem dodatkowym jest tomografia: pokazuje wielkość ubytku, zawartość worka i zanik mięśni oraz odróżnia przepuklinę od tłuszczaka. USG wykonane przez mało doświadczonego lekarza może pomylić przepuklinę z tłuszczakiem. O badaniach decyduję po zbadaniu chorego.')])
write("/przepuklina-ledzwiowa/", "Przepuklina lędźwiowa po operacji nerki: objawy, rozpoznanie | Prof. Dąbrowiecki",
      "Przepuklina lędźwiowa: gdzie powstaje, jak często po operacji nerki, objawy, różnica od wybrzuszenia boku, rozpoznanie. Prof. Dąbrowiecki, Bydgoszcz.", b)

# ============ RZADKIE ============
b = hero("Rzadkie przepukliny", "Rzadkie przepukliny ściany brzucha",
         "Przepukliny w nietypowych miejscach: trudne do zbadania i łatwo je przeoczyć. Najlepiej pokazuje je tomografia.")
b += sec("Dlaczego są trudne", f"""<p>Rzadkie przepukliny występują w nietypowych miejscach, dają niewyraźne objawy i często nie da się ich wyczuć w badaniu. Rozpoznanie samym badaniem bywa niepewne, a nawet niemożliwe. Badaniem z wyboru jest <b>tomografia komputerowa</b>.</p>
<p>Opisuję tu przepukliny Spiegla, zasłonową, kulszową i kroczową. <a href="/przepuklina-ledzwiowa/">Przepuklina lędźwiowa</a> ma osobną stronę.</p>""")
b += sec("Przepuklina Spiegla", f"""<p>Powstaje z boku od mięśnia prostego brzucha, zwykle poniżej pępka. To tylko 0,12–2,12% wszystkich przepuklin ściany brzucha. Często leży w głębi ściany, pod mięśniami, więc bywa niewyczuwalna i rozpoznaje się ją w tomografii lub USG.</p>
<p>Ma wąską szyję, więc ryzyko uwięźnięcia i zadzierzgnięcia jest wysokie (15–24%). Dlatego zaleca się operację u każdego chorego, u którego ją rozpoznano.</p>""")
b += sec("Przepuklina zasłonowa", f"""<p>Rzadka (0,07–1% przepuklin), ale groźna. Zawartość brzucha przechodzi przez kanał w kości miednicy. Dotyczy najczęściej szczupłych, wyniszczonych, starszych kobiet, które rodziły.</p>
<p>Zwykle objawia się niedrożnością jelita cienkiego. Charakterystyczny, ale obecny tylko u 25–50% chorych, jest ból po wewnętrznej stronie uda przy ruchu biodrem. Rozpoznanie jest trudne, a w nawet połowie przypadków stawia się je dopiero w czasie operacji. Śmiertelność jest wysoka (11–50%). Tomografia miednicy ma ponad 95% czułości. Konieczna jest pilna operacja.</p>""")
b += sec("Przepuklina kulszowa", f"""<p>Jedna z najrzadszych przepuklin. U większości chorych (81%) nie wyczuwa się guza w pośladku, co opóźnia rozpoznanie. Może uciskać moczowód. Rozpoznaje się ją w tomografii. Leczenie jest operacyjne, a u chorych wysokiego ryzyka można założyć stent do moczowodu.</p>""")
b += sec("Przepuklina kroczowa", f"""<p>To przepuklina dna miednicy, przez ubytek między mięśniami przy odbycie. Pierwotna jest rzadka. Częściej jest wtórna, czyli powstaje w bliźnie po rozległych operacjach nowotworów miednicy (usunięcie odbytnicy, wytrzewienie miednicy, usunięcie pęcherza). Po usunięciu odbytnicy zdarza się u 1–27% operowanych.</p>""")
b += sec("Kiedy pilnie do lekarza", f"""<div class="callout"><p><b>Zgłoś się natychmiast do szpitala, gdy pojawi się:</b> silny ból brzucha lub miednicy, wymioty, wzdęcie brzucha, brak oddawania gazów i stolca, ból promieniujący do uda albo twarde i bolesne wybrzuszenie.</p></div>""")
b += more_links([ALL[0], ALL[1], ALL[2]])
b += faq_block([('Dlaczego rzadkie przepukliny tak trudno rozpoznać?', 'Występują w nietypowych miejscach, dają niewyraźne objawy i często nie da się ich wyczuć w badaniu. Czasem są pod mięśniami, a niektóre ujawniają się dopiero jako niedrożność jelit. Badaniem z wyboru jest tomografia komputerowa.'), ('Czy przepuklinę Spiegla trzeba operować, gdy nie boli?', 'Zaleca się operację u każdego chorego, u którego ją rozpoznano. Przepuklina ma wąską szyję, więc ryzyko uwięźnięcia i zadzierzgnięcia jest wysokie (15–24%). Zwykle operuje się ją małoinwazyjnie z siatką, a „na otwarto” przy dużych przepuklinach lub w trybie pilnym.'), ('Co to jest przepuklina zasłonowa i kogo dotyczy?', 'To rzadka, ale groźna przepuklina, w której zawartość brzucha przechodzi przez kanał w kości miednicy. Dotyczy najczęściej szczupłych, starszych kobiet, które rodziły. Często objawia się niedrożnością jelita, a ból po wewnętrznej stronie uda przy ruchu biodrem jest charakterystyczny, ale nie zawsze występuje. Wymaga pilnej operacji.')])
write("/rzadkie-przepukliny-brzuszne/", "Rzadkie przepukliny brzucha: Spiegla, zasłonowa, kulszowa, kroczowa | Prof. Dąbrowiecki",
      "Rzadkie przepukliny ściany brzucha: przepuklina Spiegla, zasłonowa, kulszowa i kroczowa. Objawy, rozpoznanie w tomografii, ryzyko uwięźnięcia.", b)

# ============ WEWNĘTRZNE ============
b = hero("Przepukliny w środku brzucha", "Przepukliny wewnętrzne",
         "Jelito wciśnięte w otwór wewnątrz brzucha. Nie widać ich na zewnątrz, a mogą być groźne.")
b += sec("Czym są", f"""<p>Przepuklina wewnętrzna to przemieszczenie jelita (najczęściej cienkiego) przez otwór wewnątrz jamy brzusznej, w błonie mocującej jelita (krezce), w otrzewnej lub w sieci. Nie widać jej na brzuchu, bo wszystko dzieje się w środku.</p>
<p>Odpowiada za około 0,6–5,8% niedrożności jelita cienkiego. Gdy dojdzie do uwięźnięcia i zadzierzgnięcia, śmiertelność przekracza 50%.</p>""")
b += sec("Skąd się biorą", f"""<p>Otwór może być wrodzony (wada rozwojowa krezki lub otrzewnej) albo nabyty. Najczęściej nabyty powstaje po operacjach, zwłaszcza po obejściu żołądka (Roux-en-Y) i po usunięciu części jelita grubego, a także po urazach.</p>""")
b += sec("Rodzaje", f"""<p>Wyróżnia się je według miejsca:</p>
<ul class="check"><li><b>Przy dwunastnicy i okrężnicy (przydwunastnicza):</b> najczęstsza. Lewostronna jest trzy razy częstsza niż prawostronna. Do połowy chorych ma niedrożność, śmiertelność przekracza 20%, dlatego zaleca się operację także bez objawów.</li><li><b>Przez otwór Winslowa</b> (do torby sieciowej).</li><li><b>Przez ubytek w krezce (przezkrezkowa):</b> częsta po operacjach, wysokie ryzyko skrętu jelita i niedokrwienia.</li><li><b>Przy kątnicy, w pobliżu esicy lub w więzadle szerokim macicy.</b></li></ul>""")
b += sec("Po obejściu żołądka", f"""<p>Szczególnie ważna po operacji otyłości z obejściem żołądka (Roux-en-Y). Występuje u około 3–14% operowanych. Powstaje w szczelinach, które zostają po operacji: w przestrzeni Petersena, przy połączeniu jelito-jelito (Brolina) i w krezce okrężnicy poprzecznej. Rutynowe zamykanie tych szczelin w czasie operacji zmniejsza ryzyko o około 70%.</p>""")
b += sec("Objawy", f"""<p>Często są to przewlekłe, nawracające bóle kolkowe brzucha po jedzeniu z nudnościami. Może też wystąpić nagła niedrożność lub niedokrwienie jelita, które wymagają pilnej operacji.</p>
<div class="callout"><p><b>Zgłoś się natychmiast do szpitala, gdy pojawi się:</b> silny ból brzucha, wymioty, brak oddawania gazów i stolca.</p></div>""")
b += sec("Rozpoznanie", f"""<p>Samo badanie lekarskie zwykle nie wystarcza. Badaniem z wyboru jest tomografia komputerowa z kontrastem.</p>""")
b += more_links([ALL[0], ALL[1], ALL[2]])
b += faq_block([('Czy przepuklinę wewnętrzną można zauważyć na brzuchu?', 'Nie. Wszystko dzieje się w środku, więc nie widać żadnego wybrzuszenia. Objawy to najczęściej nawracające kolkowe bóle brzucha po jedzeniu z nudnościami, a czasem nagła niedrożność jelita. Rozpoznanie zwykle wymaga tomografii z kontrastem.'), ('Czy po operacji otyłości z obejściem żołądka mogą powstać przepukliny wewnętrzne?', 'Tak, występują u około 3–14% operowanych. Powstają w szczelinach, które zostają po operacji, w przestrzeni Petersena, przy połączeniu jelito-jelito i w krezce okrężnicy poprzecznej. Rutynowe zamykanie tych szczelin w czasie operacji zmniejsza ryzyko o około 70%.'), ('Kiedy ból brzucha po takiej operacji jest alarmem?', 'Silny ból brzucha, wymioty i brak oddawania gazów i stolca to powód, żeby natychmiast jechać do szpitala. Uwięźnięcie i zadzierzgnięcie jelita w przepuklinie wewnętrznej może prowadzić do niedokrwienia jelita i wymaga pilnej operacji.')])
write("/przepukliny-wewnetrzne/", "Przepukliny wewnętrzne: objawy, po obejściu żołądka, rozpoznanie | Prof. Dąbrowiecki",
      "Przepukliny wewnętrzne: czym są, skąd się biorą, po operacji Roux-en-Y, objawy, tomografia z kontrastem. Prof. Dąbrowiecki, Bydgoszcz.", b)

# ============ ROZWÓR PRZEŁYKOWY ============
b = hero("Przepuklina żołądka", "Przepuklina rozworu przełykowego przepony",
         "Gdy usłyszysz „przepuklina żołądka”, zwykle chodzi o to: żołądek przesuwa się przez otwór w przeponie do klatki piersiowej.")
b += sec("Uwaga", """<div class="callout"><p><b>Nie operuję przepuklin rozworu przełykowego.</b> Informacje na tej stronie podaję wyłącznie w celach informacyjnych, ponieważ pacjenci często przychodzą z rozpoznaniem „przepuklina żołądka”. Leczenie takiej przepukliny wymaga konsultacji u chirurga, który się tym zajmuje.</p></div>""", "uwaga")
b += sec("Co to jest", f"""<p>Pacjenci często przychodzą z rozpoznaniem „przepuklina żołądka”. W rzeczywistości jest to <b>przepuklina rozworu przełykowego przepony</b>. Przepona oddziela klatkę piersiową od brzucha, a przełyk przechodzi przez nią otworem, który nazywa się rozworem. Gdy ten otwór się poszerzy, a jego otoczenie osłabnie, przez otwór przesuwa się do klatki piersiowej żołądek (jego część lub cały), a czasem inne narządy jamy brzusznej.</p>
<p>To nie jest przepuklina ściany brzucha, ale tak samo polega na wpuklaniu się narządów przez osłabione miejsce. Jest bardzo częsta: dotyczy około 10–50% dorosłych. Wielu chorych nie ma objawów, a przepuklinę znajduje się przypadkiem.</p>""")
b += sec("Rodzaje", f"""<p>Są cztery typy, a od typu zależy leczenie:</p>
<ul class="check"><li><b>Typ I, wślizgowa:</b> najczęstsza (około 90–95%). Połączenie przełyku z żołądkiem przesuwa się nad przeponę. Daje głównie objawy refluksu.</li><li><b>Typ II, okołoprzełykowa:</b> połączenie przełyku z żołądkiem jest na swoim miejscu, ale dno żołądka przeciska się obok przełyku.</li><li><b>Typ III, mieszana:</b> nad przeponą jest i połączenie, i dno żołądka.</li><li><b>Typ IV:</b> oprócz żołądka przesuwa się inny narząd, najczęściej okrężnica, a czasem śledziona lub trzustka.</li></ul>
<p>Typy II–IV to razem <b>przepukliny okołoprzełykowe</b>. Jest ich około 5%, ale to one grożą groźnymi powikłaniami.</p>""")
b += sec("Objawy", f"""<p>Przepuklina wślizgowa daje najczęściej zgagę i cofanie się treści do przełyku. Mogą też być objawy poza przełykiem: przewlekły kaszel, chrypka, ból w klatce piersiowej, który nie pochodzi z serca.</p>
<p>Większe przepukliny mogą powodować trudności w połykaniu, ból w klatce piersiowej i szybkie uczucie sytości. Czasem w żołądku powstają nadżerki, które powoli krwawią i prowadzą do niedokrwistości z niedoboru żelaza. Długotrwały refluks może prowadzić do przełyku Barretta, a z niego do raka przełyku.</p>
<div class="callout"><p><b>Wezwij pogotowie (112), gdy pojawi się:</b> nagły, silny ból w klatce piersiowej lub w nadbrzuszu, wymioty albo próby wymiotów bez efektu, niemożność połknięcia. To może być uwięźnięcie lub skręt żołądka. Wymaga natychmiastowej operacji, bo martwica żołądka kończy się śmiercią w co najmniej 30% przypadków.</p></div>""")
b += sec("Rozpoznanie", f"""<p>Przepuklinę zwykle znajduje się przy badaniach z powodu refluksu, trudności w połykaniu albo niedokrwistości. Podstawowe badania to <b>pasaż przełyku z kontrastem</b> i <b>gastroskopia</b>. Przed planową operacją wykonuje się też <b>manometrię przełyku</b> i czasem pH-metrię. Dużą przepuklinę okołoprzełykową widać czasem na zwykłym zdjęciu rentgenowskim klatki piersiowej jako zacienienie za sercem.</p>""")
b += sec("Leczenie", f"""<p>Leczenie zależy od typu przepukliny:</p>
<ul class="check"><li><b>Wślizgowa z refluksem:</b> najpierw leki zmniejszające kwas w żołądku i zmiana stylu życia (zmniejszenie masy ciała, brak jedzenia przed snem, uniesione wezgłowie łóżka). Operacja, gdy objawy nie ustępują albo chory nie toleruje leków.</li><li><b>Okołoprzełykowa z objawami:</b> operacja. Przy typie IV operacja jest zawsze potrzebna.</li></ul>
<p>Standardem jest operacja laparoskopowa. Chirurg wprowadza żołądek z powrotem do brzucha, usuwa worek przepuklinowy, zbliża do siebie odnogi przepony i zwykle wykonuje <b>fundoplikację</b>, czyli owija dno żołądka wokół przełyku, żeby zapobiec refluksowi i nawrotowi. Operacja laparoskopowa daje mniejszą utratę krwi, krótszy pobyt w szpitalu i mniej powikłań niż operacja otwarta.</p>
<p>Po fundoplikacji mogą wystąpić trudności w połykaniu oraz wzdęcia z trudnością w odbijaniu. Nawroty są częste: zależnie od wyjściowej wielkości przepukliny do około 50%.</p>""")
b += more_links([ALL[0], ALL[1], ALL[2]])
b += faq_block([('Czy Pan operuje przepukliny rozworu przełykowego?', 'Nie. Podaję te informacje wyłącznie w celach informacyjnych, bo pacjenci często przychodzą z takim rozpoznaniem. Leczenie wymaga konsultacji u chirurga, który zajmuje się tymi przepuklinami. Ja zajmuję się przepuklinami ściany brzucha.'), ('Czy „przepuklina żołądka” to to samo co przepuklina brzuszna?', 'Nie. Przepuklina brzuszna powstaje w ścianie brzucha. „Przepuklina żołądka” to najczęściej przepuklina rozworu przełykowego przepony: żołądek przesuwa się przez otwór w przeponie do klatki piersiowej. Dlatego objawy to zwykle zgaga i cofanie się treści, a nie guz na brzuchu.'), ('Kiedy trzeba wzywać pogotowie przy przepuklinie rozworu przełykowego?', 'Przy nagłym, silnym bólu w klatce piersiowej lub nadbrzuszu, wymiotach albo próbach wymiotów bez efektu i niemożności połknięcia. To może być uwięźnięcie lub skręt żołądka, który wymaga natychmiastowej operacji.')])
write("/przepuklina-rozworu-przelykowego/", "Przepuklina żołądka (rozworu przełykowego przepony): objawy, leczenie | Prof. Dąbrowiecki",
      "Przepuklina żołądka to przepuklina rozworu przełykowego przepony. Rodzaje, objawy (zgaga, trudności w połykaniu), objawy alarmowe, rozpoznanie i leczenie.", b)

# ============ WYNIKI I PRZYGOTOWANIE ============
b = hero("Wyniki i przygotowanie", "Wyniki leczenia przepukliny i przygotowanie do operacji",
         "Jak często przepuklina wraca, co pogarsza wyniki i co możesz zrobić przed operacją.")
b += sec("Wyniki leczenia", f"""<p>Według danych światowych po jednej operacji z siatką trwałe wyleczenie uzyskuje się u większości chorych, zwykle u 85–98%, zależnie od rodzaju i wielkości przepukliny oraz techniki. Niepowodzeniem jest <b>nawrót</b>. Najtrudniejsze są duże przepukliny pooperacyjne, lędźwiowe i okołoprzełykowe.</p>
<ul class="check"><li><b>Przepuklina pępkowa:</b> rokowanie dobre. Nawrót zdarza się rzadko, a ryzyko zwiększają otyłość i wodobrzusze.</li><li><b>Przepuklina w linii środkowej i pooperacyjna:</b> rokowanie jest najmniej korzystne z częstych przepuklin. Około 14% chorych wymaga ponownej operacji z powodu nawrotu w ciągu 5 lat, a w ciągu 10 lat około 16%. Najważniejsza jest wielkość ubytku. Gorzej rokują otyłość, zakażenie rany i przepuklina nawrotowa. Siatka, metoda małoinwazyjna i separacja komponentów zmniejszają ryzyko nawrotu.</li><li><b>Przepuklina rozworu przełykowego:</b> objawy ustępują u większości chorych, ale nawrót w badaniu bywa częsty (około 27%, a przy dużych przepuklinach do 48%). Większość nawrotów nie daje objawów i nie wymaga ponownej operacji.</li><li><b>Przepuklina Spiegla:</b> rokowanie bardzo dobre, nawroty około 3,4%.</li><li><b>Przepuklina lędźwiowa:</b> gorsze przy dużych ubytkach (powyżej 15 cm) i otyłości. Szew zawodzi, potrzebna jest siatka.</li><li><b>Przepuklina zasłonowa:</b> siatka wyraźnie zmniejsza nawroty. Ryzykiem jest późne rozpoznanie i wysoka śmiertelność.</li></ul>
<p class="note">Podane liczby to głównie nawroty mierzone ponowną operacją. Zaniża to rzeczywistą częstość nawrotów, w przepuklinach brzusznych nawet około pięciokrotnie, bo wielu chorych z małym nawrotem nie zgłasza się do operacji.</p>""", "wyniki")
b += sec("Co pogarsza wyniki", f"""<p>Nawrót zależy od przepukliny i od chorego. Czego nie da się zmienić: duży ubytek, przepuklina, która już wracała, operacja w trybie pilnym, płeć żeńska i starszy wiek. To, na co masz wpływ:</p>
<ul class="check"><li><b>Otyłość.</b> To najsilniejszy czynnik, na który chory może wpłynąć. Ryzyko nawrotu rośnie razem z BMI. Przy BMI od około 35 jest prawie trzykrotnie większe.</li><li><b>Palenie papierosów.</b> Zwiększa ryzyko zakażenia rany, a ono samo ponad dwukrotnie zwiększa ryzyko nawrotu. Przy przepuklinie pooperacyjnej ryzyko nawrotu u palaczy jest kilka razy większe.</li><li><b>Cukrzyca</b> ze źle kontrolowanym cukrem: gorsze gojenie rany i większe ryzyko nawrotu.</li><li>Wodobrzusze i marskość wątroby, leki osłabiające odporność, przewlekły kaszel (choroby płuc), zaparcia, alkohol i niedożywienie.</li></ul>
<p>Przy operacji małoinwazyjnej (laparoskopowej) wpływ otyłości i palenia na powikłania jest mniejszy niż przy operacji „na otwarto”.</p>""", "pogarsza")
b += sec("Jak się przygotować", f"""<p>Przygotowanie przed operacją zmniejsza ryzyko powikłań, zwłaszcza ran. Co zrobić:</p>
<ol class="reasons"><li><b>Przestań palić co najmniej 4 tygodnie przed operacją</b>, najlepiej 4–8 tygodni. Po takim czasie gojenie rany jest prawie takie jak u osób niepalących. Samo zalecenie lekarza zwykle nie wystarcza, pomaga zorganizowany program rzucania palenia. Unikaj też e-papierosów.</li><li><b>Zmniejsz masę ciała.</b> Pomaga utrata 5–10% masy. Przy BMI około 50 i więcej planową dużą rekonstrukcję odkłada się do czasu schudnięcia. Przy BMI 35–50 postępowanie ustala się indywidualnie.</li><li><b>Wyrównaj cukier</b>, jeśli masz cukrzycę.</li><li><b>Ogranicz alkohol.</b> Więcej niż dwa drinki dziennie zwiększa ryzyko powikłań o około połowę, dlatego warto nie pić 4–8 tygodni przed zabiegiem.</li><li><b>Zadbaj o odżywianie i ruch.</b> Pomaga ćwiczenie ogólne i oddechowe.</li></ol>
<div class="callout"><p><b>Nie odkładaj operacji w nieskończoność.</b> Przepuklina sama nie zniknie, a czekanie na odchudzanie bywa ryzykowne, bo grozi operacją w trybie pilnym, która ma gorsze wyniki. Dla jednych chorych potrzebne jest przygotowanie, dla innych lepiej operować szybko. Decyduję o tym po zbadaniu chorego.</p></div>
<p>Każdy zakwalifikowany pacjent dostaje ode mnie szczegółowe zalecenia na piśmie, przed i po operacji.</p>""", "przygotowanie")
b += more_links([ALL[0], ALL[2], ALL[3]])
b += faq_block([('Jak długo przed operacją nie wolno palić?', 'Co najmniej 4 tygodnie, najlepiej 4–8 tygodni. Po takim czasie gojenie rany jest prawie takie jak u niepalących. Pomaga zorganizowany program rzucania palenia. Unikać trzeba też e-papierosów.'), ('Czy muszę schudnąć przed operacją przepukliny?', 'Nie zawsze. Pomaga utrata 5–10% masy ciała, a przy BMI około 50 i więcej planową dużą rekonstrukcję odkłada się. Przy BMI 35–50 postępowanie ustala się indywidualnie. Czekanie na odchudzanie bywa też ryzykowne, bo grozi operacją w trybie pilnym, która ma gorsze wyniki.'), ('Czy przepuklina może wrócić po operacji?', 'Tak, nawrót jest głównym niepowodzeniem. Zależy od rodzaju przepukliny, wielkości ubytku, techniki i od chorego. Ryzyko zwiększają otyłość, palenie, cukrzyca i zakażenie rany. Przepukliny pooperacyjne wracają częściej niż pępkowe.')])
write("/wyniki-leczenia-przepukliny-brzusznej/", "Wyniki leczenia przepukliny brzusznej i przygotowanie do operacji | Prof. Dąbrowiecki",
      "Ile przepuklin wraca po operacji, co pogarsza wyniki (otyłość, palenie, cukrzyca) i jak się przygotować do operacji przepukliny brzusznej.", b)

# ============ KLASYCZNE ============
b = hero("Metody operacji", "Klasyczna operacja przepukliny („na otwarto”)",
         "Cięcie przez ścianę brzucha. Wybieram ją, gdy przepuklina jest duża lub trudna, albo gdy jest bardzo mała.")
b += sec("Kiedy wybieram", f"""<p>Dla większości przepuklin brzusznych operacja laparoskopowa daje mniej zakażeń rany i krótszy pobyt w szpitalu, przy podobnej trwałości. Dlatego klasyczną operację wybieram w sytuacjach, w których jest lepsza:</p>
<ul class="check"><li><b>Duża lub złożona przepuklina</b> (ubytek powyżej około 8–10 cm), zwłaszcza gdy część jelit leży na stałe poza jamą brzuszną.</li><li><b>Szczupły chory z dużym ubytkiem.</b> W badaniach operacja otwarta dawała u takich chorych mniej powikłań i lepszą jakość życia. Laparoskopię częściej wybiera się u osób otyłych i przy przepuklinach nawrotowych, bo grozi wtedy mniej zakażeń.</li><li><b>Pole skażone lub zakażone</b> (np. przetoka jelitowo-skórna). Używa się wtedy mniej siatki syntetycznej, a czasem siatki wchłanialnej.</li><li><b>Operacja pilna</b> (uwięźnięcie, zadzierzgnięcie). Im cięższy stan chorego, tym prostsza powinna być naprawa. Dobrze odżywiony, stabilny chory bez zakażenia może mieć od razu wykonaną pełną rekonstrukcję.</li><li><b>Rozejście mięśni prostych z nadmiarem skóry</b> albo kilka ubytków naraz. Wykonuje się wtedy operację otwartą z zeszyciem rozejścia, a czasem z plastyką brzucha.</li><li><b>Bardzo mały ubytek</b> (np. przepuklina nadbrzusza o średnicy 1 cm), który zamykam szwami bez siatki.</li></ul>""", "kiedy")
b += sec("Duże przepukliny: uwolnienie mięśni", f"""<p>W dużej przepuklinie trzeba zbliżyć do siebie mięśnie proste i zamknąć powięź bez napięcia, a następnie wzmocnić ją siatką. Do tego służy <b>separacja komponentów</b>, czyli uwolnienie mięśni bocznych brzucha, żeby dały się przesunąć do środka.</p>
<ul class="check"><li><b>Separacja tylna</b> (z uwolnieniem mięśnia poprzecznego brzucha, TAR) jest dziś preferowana w wielu złożonych przepuklinach. Siatka leży za mięśniami, w dobrze ukrwionym miejscu, a powikłań ran i zakażeń jest mniej.</li><li><b>Separacja przednia</b> wymaga szerokiego odwarstwienia skóry i tkanki podskórnej, co zwiększa liczbę powikłań ran. Są jednak metody, które to ograniczają (m.in. endoskopowe).</li></ul>
<p>Tylna separacja jest szczególnie przydatna przy ubytkach z boku brzucha i wtedy, gdy siatka musi sięgać daleko poza brzegi ubytku.</p>""", "separacja")
b += sec("Co pomaga przy dużych przepuklinach", f"""<p>Przed operacją i w jej trakcie stosuje się pomocnicze metody:</p>
<ul class="check"><li><b>Toksyna botulinowa</b> wstrzyknięta w mięśnie boczne brzucha około 4 tygodnie przed operacją. Rozluźnia je i wydłuża, więc łatwiej zamknąć powięź bez napięcia.</li><li><b>Stopniowe wytwarzanie odmy w jamie brzusznej.</b> Pomaga przy dużej utracie miejsca w jamie brzusznej, ale ma więcej powikłań i jest kosztowna, więc stosuje się ją ostrożnie.</li><li><b>Nacięcie tylnej blaszki pochewki mięśnia prostego.</b> Zmniejsza napięcie powięzi. W małych i średnich przepuklinach może pozwolić na trwałą naprawę bez siatki.</li><li><b>Szew z małymi kęsami</b> (small bite), który poprawia trwałość zamknięcia linii środkowej.</li><li><b>Zamknięcie warstwowe</b> przy współistniejącym rozejściu mięśni, w małych przepuklinach nadbrzusza i pępka.</li></ul>""", "pomoce")
b += sec("Siatka czy szew", f"""<p>Siatka zmniejsza liczbę nawrotów przy wszystkich ubytkach poza najmniejszymi. Ma jednak własne ryzyko, np. zakażenie lub przewlekły ból, dlatego przy najmniejszych ubytkach wystarczy zeszycie szwami. Decyzję podejmuję po zbadaniu chorego, ważąc ryzyko nawrotu i ryzyko związane z siatką.</p>
<p>Wyniki i czynniki, które je pogarszają, opisuję na stronie <a href="/wyniki-leczenia-przepukliny-brzusznej/">Wyniki i przygotowanie</a>.</p>""", "siatka-szew")
b += more_links([ALL[0], ALL[2], ("/wyniki-leczenia-przepukliny-brzusznej/", "Wyniki i przygotowanie", "Rokowanie, co pogarsza wyniki, jak się przygotować")])
b += faq_block([('Czy operacja „na otwarto” jest gorsza niż laparoskopia?', 'Nie. Dla większości przepuklin laparoskopia daje mniej zakażeń rany i krótszy pobyt, ale operacja otwarta jest lepsza przy dużych i złożonych przepuklinach, w zakażonym polu, w operacjach pilnych i u szczupłych chorych z dużym ubytkiem. Chodzi o dobór metody do chorego.'), ('Co to jest separacja komponentów?', 'To uwolnienie mięśni bocznych brzucha, żeby można je było przesunąć do środka i zamknąć powięź bez napięcia przy dużej przepuklinie. Najczęściej stosuje się dziś separację tylną, która daje mniej powikłań ran niż przednia.'), ('Po co wstrzykuje się toksynę botulinową przed operacją?', 'Rozluźnia i wydłuża mięśnie boczne brzucha. Podaje się ją około 4 tygodnie przed operacją przy dużych przepuklinach, żeby łatwiej było zamknąć powięź bez napięcia.')])
write("/operacja-klasyczna-przepukliny-brzusznej/", "Klasyczna (otwarta) operacja przepukliny brzusznej | Prof. Dąbrowiecki",
      "Kiedy wybiera się klasyczną operację przepukliny „na otwarto”: duże przepukliny, separacja komponentów, toksyna botulinowa, siatka lub szew.", b)

# ============ LAPAROSKOPOWE ============
b = hero("Metody operacji", "Operacja laparoskopowa przepukliny",
         "Kilka małych cięć zamiast jednego dużego. Mniej zakażeń rany i krótszy pobyt w szpitalu.")
b += sec("Na czym polega", f"""<p>Operację wykonuje się przez kilka małych nacięć, przez które wprowadza się kamerę i cienkie narzędzia. Siatkę umieszcza się od środka, pod ścianą brzucha. Główne zalety to wyraźnie <b>mniejsze ryzyko zakażenia rany</b>, krótszy pobyt w szpitalu i mniej powikłań ran, przy podobnej trwałości naprawy jak po operacji otwartej.</p>
<p>Operacja wymaga znieczulenia ogólnego i doświadczenia operatora.</p>""", "na-czym")
b += sec("Kiedy wybieram laparoskopię", f"""<p>Laparoskopia jest najlepsza w takich sytuacjach:</p>
<ul class="check"><li><b>Przepuklina małych i średnich rozmiarów</b>, do około 5–8 cm. W literaturze akceptuje się ją do około 10 cm, ale powyżej tej wielkości zaleca się ostrożność. Bardzo małe ubytki zamykam szwami bez siatki.</li><li><b>Otyłość.</b> To silne zalecenie towarzystw przepuklinowych: u osób otyłych laparoskopia zmniejsza liczbę zakażeń i powikłań rany. Czasem potrzebne są dodatkowe kroki techniczne, np. większe zakładanie siatki na brzegi ubytku i mocniejsze jej zamocowanie.</li><li><b>Przepuklina nawrotowa.</b> Omija się bliznę i dawne pole operacyjne, a ryzyko zakażenia jest mniejsze.</li><li><b>Starszy wiek.</b> Sam wiek nie jest przeciwwskazaniem, u starszych chorych też zmniejsza się ryzyko zakażenia.</li><li><b>Wybrane przepukliny boczne</b> i w okolicy nadłonowej, po dostosowaniu techniki do miejsca.</li><li><b>Wybrane operacje pilne:</b> uwięźnięcie w niezakażonym polu, gdy można ostrożnie odprowadzić zawartość.</li></ul>
<p>Podczas operacji zamykam ubytek w powięzi szwami, a nie tylko zakrywam go siatką. Zmniejsza to liczbę złych wyników w miejscu przepukliny.</p>""", "kiedy")
b += sec("Kiedy lepsza jest operacja otwarta", f"""<p>Zamiast laparoskopii wybieram operację <a href="/operacja-klasyczna-przepukliny-brzusznej/">klasyczną</a>, gdy:</p>
<ul class="check"><li>przepuklina jest bardzo duża lub złożona i część narządów leży na stałe poza jamą brzuszną,</li><li>pole jest zakażone lub jest czynna przetoka jelitowo-skórna,</li><li>trzeba usunąć wcześniej założoną siatkę,</li><li>spodziewane są rozległe zrosty (po wielu operacjach jamy brzusznej lub po „otwartym brzuchu”),</li><li>chory nie toleruje znieczulenia ogólnego,</li><li>chory jest szczupły i ma duży ubytek: w badaniach miał wtedy mniej powikłań po operacji otwartej.</li></ul>""", "otwarta")
b += more_links([ALL[0], ALL[2], ("/operacja-klasyczna-przepukliny-brzusznej/", "Operacja klasyczna", "Kiedy wybieram operację „na otwarto”")])
b += faq_block([('Czy po laparoskopii rany goją się lepiej?', 'Tak, ryzyko zakażenia rany jest wyraźnie mniejsze, a pobyt w szpitalu krótszy, przy podobnej trwałości naprawy jak po operacji otwartej. Jest to szczególnie ważne u osób otyłych.'), ('Czy laparoskopię można zastosować przy przepuklinie nawrotowej i u starszych osób?', 'Tak. Przy przepuklinie nawrotowej omija się bliznę i dawne pole operacyjne, a ryzyko zakażenia jest mniejsze. Sam wiek nie jest przeciwwskazaniem. Operacja wymaga znieczulenia ogólnego i doświadczenia operatora.'), ('Kiedy lepsza jest operacja otwarta niż laparoskopia?', 'Przy bardzo dużej lub złożonej przepuklinie, w zakażonym polu, gdy trzeba usunąć wcześniejszą siatkę, przy spodziewanych rozległych zrostach, gdy chory nie toleruje znieczulenia ogólnego i u szczupłych chorych z dużym ubytkiem.')])
write("/operacja-laparoskopowa-przepukliny-brzusznej/", "Laparoskopowa operacja przepukliny brzusznej | Prof. Dąbrowiecki",
      "Kiedy wybiera się laparoskopową operację przepukliny brzusznej: wielkość ubytku, otyłość, przepuklina nawrotowa. Kiedy lepsza jest operacja otwarta.", b)

# ============ HYBRYDOWE ============
b = hero("Metody operacji", "Hybrydowa operacja przepukliny",
         "Połączenie operacji „na otwarto” i laparoskopii. Metoda pośrednia dla przepuklin średnich i dużych.")
b += sec("Na czym polega", f"""<p>Operacja ma dwie części:</p>
<ul class="check"><li><b>Część otwarta:</b> nacinam skórę bezpośrednio nad przepukliną, rozdzielam zrosty, wycinam worek przepuklinowy i zamykam ubytek w powięzi szwami.</li><li><b>Część laparoskopowa:</b> przez małe nacięcia wprowadzam kamerę, oceniam jamę brzuszną i szeroko rozkładam siatkę od środka, z odpowiednim zakładem na brzegi ubytku.</li></ul>
<p>Chodzi o połączenie zalet obu metod. Otwarte zamknięcie ubytku i wycięcie worka zmniejszają ryzyko płynu pod skórą (seromu) i wybrzuszenia, a przy gęstych zrostach pozwalają je bezpiecznie rozdzielić. Laparoskopia zapewnia szerokie pokrycie siatką, mniej zakażeń rany i krótszy pobyt w szpitalu.</p>""", "na-czym")
b += sec("Kiedy rozważam", f"""<p>Technikę hybrydową rozważam, gdy:</p>
<ul class="check"><li><b>Ubytek jest średni lub duży</b> (około 5–10 cm): za duży na wygodną operację wyłącznie laparoskopową, ale nie wymaga pełnej rekonstrukcji „na otwarto”.</li><li><b>Spodziewane są gęste zrosty</b> albo chory miał wiele operacji brzucha. Otwarte rozdzielenie zrostów zmniejsza ryzyko uszkodzenia jelita, które jest najczęstszym powikłaniem rozdzielania zrostów laparoskopowo. Jest też bezpieczniejsze przy odprowadzaniu uwięźniętej zawartości.</li><li><b>Trzeba wyciąć worek przepuklinowy, nadmiar skóry lub poprawić bliznę.</b></li><li><b>Chory jest otyły</b> i ma ubytek do około 6 cm: w badaniach metoda była bezpieczna i nie zwiększała powikłań ran.</li><li><b>Zrosty okażą się trudniejsze, niż sądzono.</b> Wczesne przejście na technikę łączoną jest lepsze niż późna, ratunkowa zmiana metody. W jednej serii dużych przepuklin skróciło to operację, w ogóle nie było uszkodzeń jelita (wobec 29%) i chorzy wcześniej wychodzili ze szpitala.</li></ul>""", "kiedy")
b += sec("Co mówią badania", f"""<p>W badaniach porównawczych po operacji metodą hybrydową mniej było zbiorników płynu w gojących się ranach niż po laparoskopii. Po roku liczba nawrotów po metodzie hybrydowej i laparoskopii była taka sama. Po 5–10 latach nawroty i jakość życia były podobne w obu grupach. Badania zbiorcze wskazują na tendencję do mniejszej liczby powikłań, ale bez pewności statystycznej.</p>
<p>Czyli główna korzyść to <b>mniej płynu pod skórą i powikłań ran</b>, a nie trwalsza naprawa. Nie ma jednoznacznych dowodów na to, że wyniki po operacjach metodą hybrydową różnią się od tych po laparoskopii.</p>""", "badania")
b += sec("Ograniczenia", f"""<p>Część otwarta zmniejsza największą zaletę laparoskopii, czyli małą inwazyjność. Dlatego metodę hybrydową wybieram tylko wtedy, gdy sama laparoskopia byłaby trudna lub ryzykowna.</p>""", "ograniczenia")
b += more_links([ALL[0], ALL[2], ("/operacja-laparoskopowa-przepukliny-brzusznej/", "Operacja laparoskopowa", "Kiedy wybieram laparoskopię"), ("/operacja-klasyczna-przepukliny-brzusznej/", "Operacja klasyczna", "Kiedy wybieram operację „na otwarto”")])
b += faq_block([('Na czym polega operacja hybrydowa?', 'To połączenie dwóch metod: najpierw otwieram ścianę nad przepukliną, rozdzielam zrosty, wycinam worek i zamykam ubytek w powięzi szwami, a potem przez małe nacięcia rozkładam siatkę od środka. Łączy zalety obu metod.'), ('Czy operacja hybrydowa zmniejsza ryzyko nawrotu?', 'Dowodów wysokiej jakości na rzadsze nawroty nie ma. Główna korzyść to mniej płynu pod skórą (seromów) i mniej powikłań ran. Po 5–10 latach nawroty i jakość życia były podobne jak po samej laparoskopii.'), ('Dla kogo jest metoda hybrydowa?', 'Dla chorych ze średnią lub dużą przepukliną (około 5–10 cm), z gęstymi zrostami po wielu operacjach, gdy trzeba wyciąć worek lub poprawić bliznę. Rozważam ją też wtedy, gdy zrosty podczas laparoskopii okażą się trudniejsze, niż sądzono.')])
write("/operacja-hybrydowa-przepukliny-brzusznej/", "Hybrydowa operacja przepukliny brzusznej | Prof. Dąbrowiecki",
      "Hybrydowa operacja przepukliny: połączenie operacji otwartej i laparoskopii. Kiedy ją wybieram, co mówią badania, jakie są ograniczenia.", b)

# ============ KOSZT ============
b = hero("Konsultacje, szpital, koszt", "Konsultacje i koszt operacji przepukliny brzusznej",
         "Gdzie przyjmuję, gdzie operuję i od czego zależy koszt. Koszt zostanie jednoznacznie określony po zbadaniu chorego.")
b += consult_block()
b += hospital_block()
b += about_block()
b += opinions_block()
b += sec("Koszt operacji", f"""<p><b>Koszt leczenia zostanie jednoznacznie określony po zbadaniu chorego</b>, w trakcie konsultacji.</p>
<div class="callout"><p><b>Dolna granica kosztów to 6000 zł.</b> Dotyczy prostej przepukliny brzusznej o średnicy wrót 1–2 cm, którą można zamknąć przez zeszycie szwami.</p></div>
<p>Jest możliwość rozłożenia płatności na raty.</p>""")
b += sec("Od czego zależy", """<p>Koszt zależy od stopnia skomplikowania operacji, utrudnień w zabiegu (nadwaga, otyłość, wielkość przepukliny; trudne do operacji są duże przepukliny) oraz planowanego pobytu w szpitalu.</p>
<p>Przepukliny wielkie, nawrotowe i lędźwiowe wymagają indywidualnej oceny po zbadaniu pacjenta.</p>""")
b += sec("Dlaczego prywatnie", f"""<p>Operuję prywatnie i odpłatnie. Wiem, że można się leczyć na koszt NFZ, w wielu publicznych szpitalach wykonuje się operacje przepuklin. Dla nich jest to fragment działalności. Dlaczego pacjenci wybierają leczenie u mnie? Główne powody:</p>
<ol class="reasons"><li>zapewniam indywidualną, troskliwą opiekę,</li><li>pacjent wie, kto będzie go operować,</li><li>zabieg zostanie wykonany tak samo jak w najlepszych szpitalach świata,</li><li>nie będzie operować osoba, która się dopiero tego uczy,</li><li>pacjent zna i ufa osobie, która odpowiada za wynik leczenia.</li></ol>
<p>Pacjent wie też, kto zadba o dokumentację, recepty i zwolnienie, kto odpowie na pytania dotyczące leczenia i że dostanie pełną informację dotyczącą okresu przed- i pooperacyjnego.</p>""")
b += more_links(ALL[:3])
b += faq_block([FAQ_COMMON[1], FAQ_COMMON[3], ("Czy mogę zapłacić w ratach?", "Tak, jest możliwość rozłożenia płatności na raty."),
                ("Ile potrwa pobyt w szpitalu?", "Czas pobytu w szpitalu zostanie ustalony po zbadaniu chorego, w trakcie konsultacji.")])
write("/koszt-operacji-przepukliny-brzusznej/", "Konsultacje i koszt operacji przepukliny brzusznej | Prof. Dąbrowiecki",
      "Konsultacje w Bydgoszczy, Poznaniu i online, szpital Eskulap w Osielsku. Koszt operacji przepukliny brzusznej ustalam po zbadaniu chorego, dolna granica 6000 zł, możliwe raty.", b)


# ============ POLITYKA PRYWATNOŚCI ============
b = hero("Prywatność", "Polityka prywatności", "Jakie dane zbiera ta strona i jak się ze mną skontaktować w sprawie danych.")
b += sec("Zasady", f"""<p>Ta strona nie wymaga logowania i nie zawiera formularzy. <b>Nie ustawia plików cookies ani nie śledzi odwiedzających.</b> Strona jest udostępniana przez Cloudflare, który może w standardowy sposób przetwarzać adres IP odwiedzającego w celu dostarczenia i zabezpieczenia strony.</p>
<p>Gdy dzwonisz, piszesz SMS, e-mail lub przez WhatsApp, podane przez Ciebie dane (numer telefonu, treść wiadomości) wykorzystuję wyłącznie do kontaktu w sprawie konsultacji i leczenia.</p>
<p>Administrator danych: Indywidualna Specjalistyczna Praktyka Lekarska Prof. Stanisław Dąbrowiecki, ul. Mierosławskiego 9/3, 85-654 Bydgoszcz. E-mail: <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<p>Zgodnie z RODO możesz żądać dostępu do swoich danych, ich sprostowania, usunięcia lub ograniczenia przetwarzania oraz wnieść sprzeciw. Napisz na powyższy adres e-mail.</p>
<p class="note">Jeśli w przyszłości na stronie pojawi się analityka lub inne cookies, ta polityka zostanie uzupełniona, a odwiedzający zostanie poproszony o zgodę.</p>""")
write("/cookies/", "Polityka prywatności | Przepuklina brzuszna", "Polityka prywatności strony przepuklinabrzuszna.pl: brak cookies, kontakt w sprawie danych.", b)

# robots, sitemap
# WERSJA ROBOCZA: zablokuj indeksowanie. W dniu przełączenia domeny ustaw STAGING = False.
STAGING = True
if STAGING:
    open(f"{OUT}/robots.txt", "w").write("User-agent: *\nDisallow: /\n")
    open(f"{OUT}/_headers", "w").write("/*\n  X-Robots-Tag: noindex, nofollow\n")
else:
    open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
urls = ["/"] + [u for u, _, _ in ALL] + ["/przepuklina-kresy-bialej/", "/przepuklina-pepkowa/", "/przepuklina-ledzwiowa/", "/rzadkie-przepukliny-brzuszne/", "/przepukliny-wewnetrzne/", "/przepuklina-rozworu-przelykowego/", "/wyniki-leczenia-przepukliny-brzusznej/", "/operacja-klasyczna-przepukliny-brzusznej/", "/operacja-laparoskopowa-przepukliny-brzusznej/", "/operacja-hybrydowa-przepukliny-brzusznej/", "/cookies/"]
open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
print("OK", len(urls), "stron")
