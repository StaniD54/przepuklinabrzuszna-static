#!/usr/bin/env python3
"""Buduje poprawioną wersję strony głównej przepuklinabrzuszna.pl z kopii orig-copy/index.html.
Idempotentne: zawsze startuje od oryginału. Wynik: przepuklinabrzuszna-live/index.html"""
import re, json, shutil, os
from bs4 import BeautifulSoup

BASE = "https://przepuklinabrzuszna.pl"
SRC = "/home/claude/brzuszna/orig-copy/index.html"
DST = "/home/claude/brzuszna/przepuklinabrzuszna-live/index.html"
TEL = "603751335"
TEL_FMT = "603 751 335"
EMAIL = "s.dabrowiecki@outlook.com"

TITLE = "Przepuklina brzuszna: operacja, zdjęcia, koszty | Prof. Dąbrowiecki"
DESC = ("Jak wygląda przepuklina brzuszna i pooperacyjna, kiedy operować, ile kosztuje. "
        "Prof. Dąbrowiecki, chirurg: konsultacje Bydgoszcz, Poznań, Warszawa, online.")

html = open(SRC, encoding="utf-8").read()

# ---------- 1. czyszczenie śladów Cloudflare / WordPressa ----------
html = re.sub(r'<script[^>]*email-decode[^>]*></script>', '', html)
html = re.sub(r"<script>\(function\(\)\{function c\(\)\{var b=a\.contentDocument.*?</script>", '', html, flags=re.S)
html = re.sub(r'<script[^>]*static\.cloudflareinsights\.com[^>]*></script>', '', html)
html = re.sub(r'<link rel="(?:alternate|EditURI|https://api\.w\.org/|alternate)"[^>]*(?:feed|xmlrpc|wp-json)[^>]*>', '', html)
html = re.sub(r'<link[^>]*href="/(?:wp-json|xmlrpc\.php|feed|comments/feed)[^"]*"[^>]*>', '', html)
html = re.sub(r'<link[^>]*rel="canonical"[^>]*>', '', html)
# ukryty e-mail Cloudflare -> prawdziwy adres
html = re.sub(r'<a[^>]*email-protection[^>]*>.*?</a>',
              f'<a href="mailto:{EMAIL}">{EMAIL}</a>', html, flags=re.S)
html = html.replace('href="/x.com/dabrowiecki_s"', 'href="https://x.com/dabrowiecki_s"')

# ---------- 2. title, description, canonical, OG ----------
html = re.sub(r'<title>.*?</title>', f'<title>{TITLE}</title>', html, flags=re.S)
html = re.sub(r'<meta name="description"[^>]*>', f'<meta name="description" content="{DESC}">', html)
html = re.sub(r'<meta property="og:title"[^>]*>', f'<meta property="og:title" content="{TITLE}">', html)
html = re.sub(r'<meta property="og:description"[^>]*>', f'<meta property="og:description" content="{DESC}">', html)
html = re.sub(r'<meta property="og:url"[^>]*>', f'<meta property="og:url" content="{BASE}/">', html)
canon = f'<link rel="canonical" href="{BASE}/">'

# ---------- 3. dane strukturalne ----------
faq = [
 ("Czy przepuklina brzuszna może sama zniknąć?",
  "Nie. Gdy przepuklina się pojawi, sama już nie zniknie. Jedyną metodą leczenia jest operacja, a odkładanie jej pozwala przepuklinie rosnąć."),
 ("Ile kosztuje operacja przepukliny brzusznej?",
  "Koszt zostanie jednoznacznie określony po zbadaniu chorego, w trakcie konsultacji. Zależy od stopnia skomplikowania operacji i utrudnień w zabiegu (nadwaga, otyłość, wielkość przepukliny) oraz planowanego pobytu w szpitalu. Dolna granica to 6000 zł: dotyczy prostej przepukliny brzusznej o średnicy wrót 1–2 cm, którą można zamknąć przez zeszycie szwami. Możliwe jest rozłożenie płatności na raty."),
 ("Czy mogę zapłacić w ratach?",
  "Tak, jest możliwość rozłożenia płatności na raty."),
 ("Ile dni trwa pobyt w szpitalu?",
  "Czas pobytu w szpitalu zostanie ustalony po zbadaniu chorego, w trakcie konsultacji. Zależy od wielkości przepukliny, rodzaju operacji i znieczulenia."),
 ("Czy operuje Pan przepuklinę razem z plastyką brzucha?",
  "Tak. Przy otyłości, ale też u osób masywnie odchudzonych, można jednocześnie zlikwidować przepuklinę oraz usunąć nadmiar skóry i tkanki tłuszczowej brzucha."),
 ("Czy pacjent jest winny powstania przepukliny pooperacyjnej?",
  "Nie. Operowany pacjent nigdy nie jest winny powstania przepukliny. Jest to znane powikłanie operacji, które może wystąpić zaraz po zabiegu, po miesiącach, a nawet po wielu latach."),
 ("Jak wygląda konsultacja i czy można ją odbyć online?",
  "Zawsze badam pacjenta, wyjaśniam przyczyny przepukliny, oceniam bezpieczeństwo operacji i omawiam możliwe metody. Konsultacje online (WhatsApp, Skype, Messenger) są możliwe praktycznie codziennie o godzinie 20.00. W ten sposób nie zbadam pacjenta, ale ogólnie ustalę stan zdrowia i badania wymagane do zabiegu."),
 ("Gdzie Pan operuje?",
  "Leczenie prowadzę w prywatnym szpitalu Eskulap w Osielsku koło Bydgoszczy. Konsultacje odbywają się w Bydgoszczy, Poznaniu i Warszawie."),
]
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q,
                          "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
doctor_ld = {
    "@context": "https://schema.org", "@type": "Physician",
    "name": "Stanisław Dąbrowiecki", "honorificPrefix": "prof. dr hab. n. med.",
    "url": BASE + "/", "telephone": "+48" + TEL, "email": EMAIL,
    "medicalSpecialty": "Surgical",
    "description": "Chirurg, profesor chirurgii. Operacje przepuklin brzusznych i pooperacyjnych, także z plastyką brzucha.",
    "address": {"@type": "PostalAddress", "addressLocality": "Bydgoszcz", "addressCountry": "PL"},
    "sameAs": ["https://www.facebook.com/prof.dabrowiecki", "https://x.com/dabrowiecki_s",
               "https://pl.pinterest.com/sdbrowiecki/",
               "https://www.youtube.com/channel/UCYtx7soG1is2ertlI8MeVPQ"],
}
website_ld = {"@context": "https://schema.org", "@type": "WebSite", "name": "Przepuklina brzuszna",
              "url": BASE + "/", "inLanguage": "pl-PL"}
ld = "".join(f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>'
             for o in (website_ld, doctor_ld, faq_ld))
# usuń stare bloki ld+json (puste url, błędny adres Twittera)
html = re.sub(r'<script[^>]*application/ld\+json[^>]*>.*?</script>', '', html, flags=re.S)

# ---------- 4. CSS ----------
css = r"""
<style id="hx-css">
:root{--hx-accent:#1c7c4a;--hx-accent-d:#14613a;--hx-ink:#1f2a3a}
html{scroll-behavior:smooth}
.hx-btn{display:inline-flex;align-items:center;justify-content:center;gap:.5em;padding:.85em 1.4em;border-radius:10px;
  font:600 18px/1.2 Poppins,Arial,sans-serif;text-decoration:none!important;color:#fff!important;background:var(--hx-accent);
  border:2px solid var(--hx-accent);transition:background .15s}
.hx-btn:hover{background:var(--hx-accent-d);border-color:var(--hx-accent-d)}
.hx-btn.hx-alt{background:#fff;color:var(--hx-accent)!important}
.hx-btn.hx-alt:hover{background:#eef7f1}
.hx-cta{max-width:900px;margin:0 auto;padding:8px 20px 28px;text-align:center;font-family:Poppins,Arial,sans-serif;color:var(--hx-ink)}
.hx-lead{font-size:20px;line-height:1.5;margin:0 0 18px}
.hx-note{font-size:15px;line-height:1.5;margin:12px 0 0;color:#4a566b}
.hx-actions{display:flex;flex-wrap:wrap;gap:12px;justify-content:center}
.hx-trust{list-style:none;margin:22px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px}
.hx-trust li{background:#f3f6fb;border-radius:10px;padding:12px 14px;font-size:16px;line-height:1.35}
.hx-trust b{display:block;font-size:17px;color:#1b1bbf}
#op3-element-XYWZxx1O p,#op3-element-XYWZxx1O span{font-size:17px!important;line-height:1.6!important}
/* FAQ */
.hx-faq{max-width:900px;margin:0 auto;padding:10px 20px 40px;font-family:Poppins,Arial,sans-serif;color:var(--hx-ink)}
.hx-faq h2{font-size:30px;text-align:center;color:#1b1bbf;margin:10px 0 22px}
.hx-faq details{border:1px solid #d9e0ec;border-radius:10px;margin:0 0 12px;background:#fff}
.hx-faq summary{cursor:pointer;padding:16px 18px;font-weight:600;font-size:18px;line-height:1.4;list-style:none}
.hx-faq summary::-webkit-details-marker{display:none}
.hx-faq summary::after{content:"+";float:right;font-size:24px;line-height:1;color:var(--hx-accent)}
.hx-faq details[open] summary::after{content:"–"}
.hx-faq details p{margin:0;padding:0 18px 18px;font-size:17px;line-height:1.65}
/* nagłówek: telefon */
.hx-headtel{position:absolute;right:120px;top:50%;transform:translateY(-50%);font:600 17px Poppins,Arial,sans-serif;
  color:var(--hx-accent)!important;text-decoration:none!important;white-space:nowrap}
.navbar-brand h1{font:700 22px/1.2 Poppins,Arial,sans-serif!important;color:#1b1bbf!important;margin:0!important}
.op-navbar .op-container{position:relative}
/* pasek kontaktu na telefonie */
.hx-bar{display:none}
@media (max-width:767px){
  .hx-headtel{display:none}
  #op3-element-jJAXavn2 *{font-size:30px!important;line-height:1.25!important}
  #op3-element-hQTqH5zO [data-op3-element-type=image] img{max-height:260px;width:auto!important}
  #op3-element-2zdnMSpb{display:none!important}
  #op3-element-77FZGP3B,#op3-element-9MD1cBfo{margin-top:0!important;padding-top:0!important}
  .hx-cta{padding:4px 16px 22px}.hx-lead{font-size:18px}
  .hx-btn{width:100%}
  .hx-bar{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:99998;gap:8px;padding:8px 10px calc(8px + env(safe-area-inset-bottom));
    background:#fff;box-shadow:0 -2px 12px rgba(0,0,0,.18)}
  .hx-bar a{flex:1;padding:.8em .4em;font-size:17px}
  body{padding-bottom:76px}
  .hx-faq h2{font-size:25px}
}
</style>
"""

# ---------- 5. wstawki HTML ----------
hero_cta = f"""
<section class="hx-cta" aria-label="Kontakt i najważniejsze informacje">
  <p class="hx-lead">Operacje przepuklin brzusznych i pooperacyjnych, także z plastyką brzucha.
  Konsultacje w Bydgoszczy, Poznaniu, Warszawie i online.</p>
  <div class="hx-actions">
    <a class="hx-btn" href="tel:+48{TEL}">Zadzwoń: {TEL_FMT}</a>
    <a class="hx-btn hx-alt" href="sms:+48{TEL}?&body=BRZUCH">Wyślij SMS: BRZUCH</a>
  </div>
  <p class="hx-note">SMS o treści BRZUCH: odeślę adresy i terminy konsultacji oraz podstawowe informacje o leczeniu.</p>
  <ul class="hx-trust">
    <li><b>Chirurg od 1979 r.</b>profesor chirurgii, specjalizacja: przepukliny</li>
    <li><b>12 lat na czele Kliniki</b>Chirurgii Ogólnej w Bydgoszczy</li>
    <li><b>Koszt po badaniu</b><a href="#op3-element-nEVTqxgM">od 6000 zł</a> za prostą przepuklinę, możliwe raty</li>
    <li><b>Szpital Eskulap</b>Osielsko koło Bydgoszczy</li>
  </ul>
</section>
"""
faq_html = '<section class="hx-faq" id="faq"><h2>Najczęstsze pytania</h2>' + "".join(
    f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in faq) + '</section>'
bar_html = (f'<div class="hx-bar" role="navigation" aria-label="Szybki kontakt">'
            f'<a class="hx-btn" href="tel:+48{TEL}">Zadzwoń</a>'
            f'<a class="hx-btn hx-alt" href="sms:+48{TEL}?&body=BRZUCH">SMS: BRZUCH</a></div>')

# ---------- 6. operacje na DOM ----------
soup = BeautifulSoup(html, "html.parser")
root = soup.select_one('#op3-designer-element > div[data-op3-children]')
kids = root.find_all(recursive=False)
assert len(kids) == 24, len(kids)
hero, costs_band, reviews_band, reviews, contact_band = kids[0], kids[11], kids[18], kids[19], kids[20]
methods_last = kids[10]

# kontakt: klikalne numery i czytelniejsza czcionka
contact = kids[21]
for node in list(contact.find_all(string=re.compile('603751335'))):
    t = str(node)
    if '(603751335)' in t:
        t = t.replace('(603751335)', '(<a href="https://wa.me/48603751335">603751335</a>)')
    else:
        t = t.replace('603751335', '<a href="tel:+48603751335">603751335</a>')
    node.replace_with(BeautifulSoup(t, "html.parser"))
# koszty: bez tabeli cen, tekst o ustalaniu kosztu po badaniu
costs_txt = kids[12].select_one('#op3-element-t2Nw5RkG h2')
costs_txt.clear()
costs_txt.append(BeautifulSoup(
    '<b>Koszt leczenia zostanie jednoznacznie określony po zbadaniu chorego</b>, w trakcie konsultacji. '
    'Zależy on od stopnia skomplikowania operacji, utrudnień w zabiegu (nadwaga, otyłość, wielkość przepukliny '
    '– trudne do operacji są duże przepukliny, itd.) oraz planowanego pobytu w szpitalu. '
    '<b>Dolna granica kosztów to 6000 zł</b>: dotyczy prostej przepukliny brzusznej o średnicy wrót 1–2 cm, '
    'którą można zamknąć przez zeszycie szwami. '
    'Jest możliwość rozłożenia płatności na raty.', "html.parser"))
kids[12].select_one('#op3-element-GXKNekah').decompose()
bio = kids[23]
for n in bio.find_all(string=re.compile('2013 – profesor zwyczajny')):
    n.replace_with(str(n).replace('2013 – profesor zwyczajny','2012 – profesor zwyczajny'))
# opinie przed kosztami
reviews_band.extract(); reviews.extract()
costs_band.insert_before(reviews_band); costs_band.insert_before(reviews)
# CTA pod hero
soup.select_one('#op3-element-t2QOSUMX').insert_after(BeautifulSoup(hero_cta, "html.parser"))
# FAQ przed kontaktem
contact_band.insert_before(BeautifulSoup(faq_html, "html.parser"))
# tabela kosztów: opakowanie przewijane
# (tabela kosztów ma własny responsywny układ motywu – zostawiona bez zmian)
# telefon w nagłówku
cont = soup.select_one('.op-navbar .op-container')
if cont:
    cont.append(BeautifulSoup(f'<a class="hx-headtel" href="tel:+48{TEL}">Tel. {TEL_FMT}</a>', "html.parser"))
# pasek na dole
soup.body.append(BeautifulSoup(bar_html, "html.parser"))
# head
soup.head.append(BeautifulSoup(canon + ld + css, "html.parser"))

out = str(soup)
open(DST, "w", encoding="utf-8").write(out)
print("OK", len(out))

# ---------- 7. podstrony: o-mnie, cookies (tylko czyszczenie) ----------
def clean_sub(path, canon_url):
    h = open(path, encoding="utf-8").read()
    h = re.sub(r'<script[^>]*email-decode[^>]*></script>', '', h)
    h = re.sub(r"<script>\(function\(\)\{function c\(\)\{var b=a\.contentDocument.*?</script>", '', h, flags=re.S)
    h = re.sub(r'<script[^>]*static\.cloudflareinsights\.com[^>]*></script>', '', h)
    h = re.sub(r'<link[^>]*href="/(?:wp-json|xmlrpc\.php|feed|comments/feed)[^"]*"[^>]*>', '', h)
    h = re.sub(r'<link[^>]*rel="canonical"[^>]*>', f'<link rel="canonical" href="{canon_url}">', h)
    h = re.sub(r'<a[^>]*email-protection[^>]*>.*?</a>', f'<a href="mailto:{EMAIL}">{EMAIL}</a>', h, flags=re.S)
    h = re.sub(r'<meta property="og:url"[^>]*>', f'<meta property="og:url" content="{canon_url}">', h)
    open(path, "w", encoding="utf-8").write(h)
for sub in ("o-mnie", "cookies"):
    src = f"/home/claude/brzuszna/orig-copy/{sub}/index.html"
    dst = f"/home/claude/brzuszna/przepuklinabrzuszna-live/{sub}/index.html"
    shutil.copyfile(src, dst)
    clean_sub(dst, f"{BASE}/{sub}/")

# ---------- 8. robots.txt, sitemap.xml ----------
root_dir = "/home/claude/brzuszna/przepuklinabrzuszna-live"
open(f"{root_dir}/robots.txt", "w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
open(f"{root_dir}/sitemap.xml", "w").write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{BASE}/{p}</loc></url>\n" for p in ("", "o-mnie/"))
    + "</urlset>\n")
print("podstrony, robots, sitemap OK")
