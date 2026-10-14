#!/usr/bin/env python3
# Prototyp: przepuklinabrzuszna.pl w układzie i krojach pisma z angielskiej strony meshfreehernia
import os, json, shutil, glob, html
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
 "zan1": "HV_1.jpg", "zan2": "HV_2.jpg", "zan3": "HV_3.jpg", "zan4": "HV_4.jpg",
 "martwica": "HV-martwica-skory-e1654946972342.jpg",
 "przed1": "HV-przed-operacja.jpg", "przed2": "HV-przed-operacja2.jpg",
 "otylosc": "otylosc-i-przepuklina.jpg",
 "plast-przed": "otylosc-i-HV-229x300.jpg", "plast-po": "otylosc-i-HV-pooper-230x300.jpg",
 "otwarta": "otwary-brzuch-300x199.jpg", "siatka": "siatka-do-wszczepienia-300x191.jpg",
 "warstwy": "warstwy-gdzie-siatka-e1654947350302.jpg", "lapar": "HV-laaproskopia-300x224.jpg",
 "esk1": "esk4-1024x575-1.jpg", "esk2": "Eskulap-szpital.jpg",
 "e-budynek": "eskulap-budynek.jpg", "e-pokoj": "eskulap-pokoj.jpg", "e-recepcja": "eskulap-recepcja.jpg", "e-lazienka": "eskulap-lazienka.jpg", "e-obraz": "eskulap-pracownia-obrazowa.jpg",
 "e-zima": "eskulap-front.jpg", "e-lato": "eskulap-wejscie.jpg", "e-sala": "eskulap-sala-angio.jpg", "e-tomo": "eskulap-tomograf.jpg", "e-recep2": "eskulap-recepcja2.jpg", "e-mapa": "eskulap-wejscia-mapa.png",
 "prof": "SD_n_1-scaled.jpg",
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
 ("link", "/", "Start"), ("link", "/przepuklina-brzuszna-objawy-zdjecia/", "Objawy i zdjęcia"),
 ("dd", "Rodzaje przepuklin", [("/przepuklina-pooperacyjna/", "Pooperacyjna"), ("/przepuklina-kresy-bialej/", "Kresy białej"), ("/przepuklina-pepkowa/", "Pępkowa"), (None, "Lędźwiowa"), (None, "Wewnętrzne")]),
 ("dd", "Metody operacji", [("/operacja-przepukliny-brzusznej/", "Przegląd metod"), (None, "Klasyczne"), (None, "Laparoskopowe"), (None, "Hybrydowe")]),
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
<div class="wrap">
<header class="top">
  <a class="brand" href="/"><strong>Przepuklina brzuszna</strong><span>prof. Stanisław Dąbrowiecki, chirurg</span></a>
  <a class="toptel" href="tel:+48{TEL}">Tel. {TELF}</a>
</header>
<nav class="nav" aria-label="Główne">{nav}</nav>
{body}
<footer>
  <p><strong>Indywidualna Specjalistyczna Praktyka Lekarska Prof. Stanisław Dąbrowiecki</strong><br>
  Tel. <a href="tel:+48{TEL}">{TELF}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a> · WhatsApp <a href="https://wa.me/48{TEL}">{TELF}</a></p>
  <p>Informacje na stronie mają charakter ogólny i nie zastępują badania lekarskiego. Leczenie i jego koszt ustala lekarz po zbadaniu chorego. <a href="/koszt-operacji-przepukliny-brzusznej/#o-mnie">O mnie</a> · <a href="/cookies/">Polityka prywatności</a></p>
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
    return f'<div class="hero"><p class="eyebrow">{eyebrow}</p><h1>{h1}</h1><p class="lead">{lead}</p>{CTA}</div>'

def review(name):
    n, t = REV[name]
    return f'<blockquote class="rev"><p>{html.escape(t.replace("..........", " … "))}</p><footer>{n}</footer></blockquote>'

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

ZL = "https://www.znanylekarz.pl/stanislaw-dabrowiecki/chirurg-bariatra/warszawa"
def opinions_block():
    return sec("Opinie", review("Robert Graczyk") + review("Adam") + review("Małgorzata K.") +
               f'<p><a href="{ZL}" rel="noopener" target="_blank">Więcej opinii pacjentów w serwisie ZnanyLekarz</a></p>', "opinie")

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
 ("/przepuklina-brzuszna-objawy-zdjecia/", "Przepuklina brzuszna: jak wygląda", "Zdjęcia i skutki odkładania operacji"),
 ("/przepuklina-pooperacyjna/", "Przepuklina pooperacyjna", "Przepuklina w bliźnie po operacji"),
 ("/operacja-przepukliny-brzusznej/", "Metody operacji", "Szwy, siatka, laparoskopia, plastyka brzucha"),
 ("/koszt-operacji-przepukliny-brzusznej/", "Konsultacje i koszt", "Gdzie przyjmuję i operuję, ile to kosztuje"),
]

# ============ STRONA GŁÓWNA ============
home = hero("Przepukliny brzuszne i pooperacyjne", "<span>Operuję przepukliny brzuszne.</span> <span>To moja specjalizacja.</span>",
            "Konsultacje w Bydgoszczy i Poznaniu oraz online. Operacje w prywatnym szpitalu Eskulap w Osielsku koło Bydgoszczy.")
home += """<div class="facts"><div><b>12 lat</b><span>kierowania Kliniką Chirurgii w Bydgoszczy</span></div><div><b>2012</b><span>od tego roku profesor chirurgii</span></div><div><b>od 6000 zł</b><span>dolna granica kosztu, ustalanego po badaniu</span></div></div>"""
home += sec("Leczenie", """<p>Gdy jama brzuszna jest otwierana cięciem chirurgicznym, jest <b>duże ryzyko powstania przepukliny pooperacyjnej</b>. Przepuklina w bliźnie może się pojawić od razu po operacji, po miesiącach, a nawet po wielu latach. Są też przepukliny po operacjach laparoskopowych. Bywają też takie, które powstają samoistnie.</p>
<p><b>Gdy przepuklina się pojawi, sama już nie zniknie. Jedyna rada to operacja.</b> Nigdy nie należy dopuszczać do zaawansowanego stanu choroby.</p>""", "leczenie")
DESC = {"/przepuklina-brzuszna-objawy-zdjecia/": "Jak wygląda, objawy, zdjęcia i skutki odkładania operacji",
        "/przepuklina-pooperacyjna/": "Przepuklina w bliźnie po operacji",
        "/operacja-przepukliny-brzusznej/": "Szwy, siatka, laparoskopia, plastyka brzucha",
        "/koszt-operacji-przepukliny-brzusznej/": "Gdzie przyjmuję i operuję, ile to kosztuje"}
def _tile(u, t):
    if u: return f'<li><a href="{u}"><b>{t}</b></a></li>'
    return f'<li class="soon" title="w przygotowaniu"><b>{t}</b></li>'
def _tiles_from_menu():
    out = ""
    for it in NAV_ITEMS[1:]:
        if it[0] == "link":
            out += f'<ul class="cards">{_tile(it[1], it[2])}</ul>'
        else:
            out += f'<h3 class="grp">{it[1]}</h3><ul class="cards">' + "".join(_tile(u, t) for u, t in it[2]) + '</ul>'
    return out
home += sec("Tematy", _tiles_from_menu(), "tematy", "wide")
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
b = hero("Przepuklina brzuszna", "Przepuklina brzuszna: jak wygląda, objawy, zdjęcia",
         "Zdjęcia przepuklin zaniedbanych oraz informacje, dlaczego nie wolno odkładać operacji.")
b += sec("Co to jest", f"""<p>Przepuklina brzuszna to wypuklenie zawartości jamy brzusznej przez osłabione miejsce w ścianie brzucha. Najczęściej powstaje w bliźnie po wcześniejszej operacji (przepuklina pooperacyjna), ale bywa też, że powstaje samoistnie.</p>
<p>{DRAFT}Typowym objawem jest wybrzuszenie, które może się powiększać. Przepuklina czasem boli (bywa, że tak). Dokładne objawy i rozpoznanie ustalam podczas badania.</p>""")
b += sec("Zdjęcia", f"""<p>Na zdjęciach skutki braku operacji. Przepukliny powiększały się przez lata. Lekceważono objawy, a operacja była stale odkładana na później; czasami przez pacjenta, bywa że przez lekarza.</p>
<div class="grid4">{img('zan1','Duża przepuklina brzuszna')}{img('zan2','Przepuklina brzuszna, widok z przodu')}{img('zan3','Przepuklina z zmianami skóry')}{img('zan4','Duża przepuklina brzuszna, widok z boku')}</div>
<p class="note">Na zdjęciach z prawej skóra nad przepukliną nie wytrzymuje napięcia i stopniowo ulega martwicy. Z czasem dojdzie do pęknięcia i wydostania się jelit na zewnątrz. To będzie już dramat: pęknięta przepuklina na brzuchu.</p>
<div class="duo">{img('martwica','Martwica skóry nad przepukliną')}</div>
<p><b>Nigdy nie można dopuszczać do tak zaawansowanego stanu choroby.</b> Pacjent staje się inwalidą.</p>""", "zdjecia", "wide")
b += sec("To nie Pana wina", """<p>Operowany pacjent <b>nigdy</b> nie jest winny powstania przepukliny. Bywa, że pacjent jest obwiniany: „za szybko wstał Pan z łóżka po operacji”. To nie jest prawda i to nie jest przyczyna przepukliny. Nie dajcie sobie tego wmówić.</p>""")
b += sec("Kto jest zagrożony", f"""<p>Niebezpieczeństwo wystąpienia przepukliny jest większe u osób z nadwagą lub otyłością oraz po pilnych operacjach. Również w takiej sytuacji można chorym pomóc. Gdy można przesunąć operację o kilka miesięcy, należy spróbować odchudzić pacjenta. U osoby otyłej należy jednocześnie wykonać plastykę brzucha: zlikwidować przepuklinę oraz usunąć nadmiar tłuszczu z brzucha.</p>
<div class="duo">{img('przed1','Przepuklina brzuszna u osoby otyłej, przed operacją')}{img('przed2','Przepuklina brzuszna, widok z boku, przed operacją')}</div>""")
b += more_links(ALL[1:])
b += faq_block([FAQ_COMMON[0], FAQ_COMMON[2]])
write("/przepuklina-brzuszna-objawy-zdjecia/", "Przepuklina brzuszna: jak wygląda, objawy, zdjęcia | Prof. Dąbrowiecki",
      "Jak wygląda przepuklina brzuszna? Zdjęcia, skutki odkładania operacji i kto jest zagrożony. Prof. Dąbrowiecki, konsultacje w Bydgoszczy i Poznaniu.", b)

# ============ POOPERACYJNA ============
b = hero("Przepuklina w bliźnie", "Przepuklina pooperacyjna: leczenie i operacja",
         "Przepuklina w bliźnie po operacji jamy brzusznej. Jak powstaje i jak ją leczę.")
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
b += faq_block([FAQ_COMMON[0], FAQ_COMMON[2]])
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
b += sec("Plastyka brzucha", """<p>Przy rozległej przepuklinie brzusznej, a także u osób masywnie odchudzonych, jednocześnie z likwidacją przepukliny wykonuje się plastykę brzucha. Operacja jest bardziej rozległa, ale efekt leczenia jest bardzo dobry. Zdjęcia przed i po operacji są na stronie o <a href="/przepuklina-pooperacyjna/">przepuklinie pooperacyjnej</a>.</p>""")
b += more_links([ALL[0], ALL[1], ALL[3]])
b += faq_block([FAQ_COMMON[0], ("Czy można operować laparoskopowo?", "Przepukliny o niewielkich i średnich rozmiarach (do 5–8 cm) można operować laparoskopowo. Przy większych zaleca się operację „na otwarto”. Metodę wybieram po zbadaniu chorego.")])
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
b += sec("Leczenie", f"""<p>Przepuklinę kresy białej leczy się operacyjnie. Małe ubytki (do około 1,5 cm, bez dodatkowych czynników ryzyka) można zamknąć samymi szwami. Większe wzmacnia się siatką, żeby przepuklina nie wróciła. Nawrót jest najważniejszym powikłaniem odległym. Rodzaj operacji wybieram po zbadaniu chorego. <a href="/koszt-operacji-przepukliny-brzusznej/">Koszt i konsultacje</a></p>""")
b += more_links([ALL[0], ALL[1], ALL[2]])
b += faq_block([FAQ_COMMON[0], FAQ_COMMON[1]])
write("/przepuklina-kresy-bialej/", "Przepuklina kresy białej (nadbrzuszna): objawy, leczenie | Prof. Dąbrowiecki",
      "Przepuklina kresy białej: czym jest, objawy, powikłania, różnica od rozejścia mięśni prostych i leczenie. Prof. Dąbrowiecki, Bydgoszcz.", b)

# ============ PĘPKOWA ============
b = hero("Przepuklina przy pępku", "Przepuklina pępkowa: objawy i leczenie",
         "Wybrzuszenie w pępku lub tuż przy nim. Czym jest, kiedy jest groźna i jak ją leczę.")
b += sec("Czym jest i jak częsta", f"""<p>{DRAFT}Przepuklina pępkowa to wypuklenie zawartości jamy brzusznej (tłuszczu lub jelita) przez osłabione miejsce w ścianie brzucha przy pępku, czyli w miejscu po pępowinie. Za przepuklinę pępkową uznaje się ubytek w linii środkowej brzucha od 3 cm powyżej do 3 cm poniżej pępka.</p>
<p>Występuje u około 2–4% dorosłych i stanowi 6–14% wszystkich przepuklin ściany brzucha.</p>""")
b += sec("U dzieci i u dorosłych", f"""<p>{DRAFT}U dzieci przepuklina pępkowa wynika z niepełnego zamknięcia pierścienia pępkowego i w około 90% przypadków zamyka się sama do wieku przedszkolnego.</p>
<p>U dorosłych jest zwykle nabyta: powstaje przy wzroście ciśnienia w brzuchu i rzadko cofa się sama. Częściej wymaga operacji.</p>""")
b += sec("Kto jest bardziej narażony", f"""<p>{DRAFT}U dorosłych przepuklina pępkowa powstaje częściej przy:</p>
<ul class="check"><li>otyłości,</li><li>wielu ciążach i porodach (rozciągnięcie pierścienia pępkowego),</li><li>wodobrzuszu przy marskości wątroby,</li><li>przewlekłym kaszlu, zaparciach lub dużym guzie w brzuchu (stale podwyższone ciśnienie w brzuchu),</li><li>paleniu papierosów, chorobach tkanki łącznej i niedoczynności tarczycy. Częściej chorują mężczyźni w wieku 41–80 lat.</li></ul>""")
b += sec("Objawy", f"""<p>{DRAFT}Przepuklina często nie boli. Widać lub wyczuwa się wybrzuszenie przy pępku, które jest większe przy kaszlu i parciu. Może pojawić się dyskomfort lub ból. Dla wielu osób problemem jest też wygląd, czyli „wystający pępek".</p>""")
b += sec("Powikłania", f"""<p>{DRAFT}Najgroźniejsze jest <b>uwięźnięcie</b> i <b>zadzierzgnięcie</b>: jelito lub sieć zostają uwięzione w przepuklinie i tracą dopływ krwi. Wymaga to pilnej operacji.</p>
<div class="callout"><p><b>Zgłoś się natychmiast do lekarza lub szpitala, gdy pojawi się:</b> twarde, bolesne wybrzuszenie, którego nie da się wsunąć, nudności lub wymioty, wzdęcie brzucha albo brak oddawania gazów i stolca.</p></div>""")
b += sec("Leczenie", f"""<p>{DRAFT}Operację zaleca się przy przepuklinach, które dają dolegliwości, powiększają się, uległy uwięźnięciu albo bardzo przeszkadzają z powodów estetycznych. U kobiet zabieg zwykle odracza się do czasu zakończenia planów rodzicielskich, bo ciąża rozciąga pierścień pępkowy.</p>
<p>Małe ubytki (1–2 cm) mogę zamknąć samymi szwami. Większe wzmacniam siatką, żeby przepuklina nie wróciła. Metodę wybieram po zbadaniu chorego. <a href="/koszt-operacji-przepukliny-brzusznej/">Koszt i konsultacje</a></p>""")
b += more_links([ALL[0], ALL[1], ALL[2]])
b += faq_block([FAQ_COMMON[0], FAQ_COMMON[1]])
write("/przepuklina-pepkowa/", "Przepuklina pępkowa: objawy, leczenie, operacja | Prof. Dąbrowiecki",
      "Przepuklina pępkowa u dorosłych: przyczyny, objawy, powikłania i leczenie. Małe ubytki szwami, większe z siatką. Prof. Dąbrowiecki, Bydgoszcz.", b)

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
open(f"{OUT}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
urls = ["/"] + [u for u, _, _ in ALL] + ["/przepuklina-kresy-bialej/", "/przepuklina-pepkowa/", "/cookies/"]
open(f"{OUT}/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
print("OK", len(urls), "stron")
