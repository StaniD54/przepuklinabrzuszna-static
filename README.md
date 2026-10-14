# przepuklinabrzuszna.pl (wersja statyczna)

Strona prof. Stanisława Dąbrowieckiego o przepuklinach brzusznych. Statyczny HTML, docelowo Cloudflare Pages.

## Struktura strony (menu = kafelki na głównej, jedna lista `NAV_ITEMS` w `build/build_site.py`)
- Start
- Objawy i zdjęcia
- Rodzaje przepuklin ▾: pooperacyjna i kresy białej (zatwierdzone); pępkowa, lędźwiowa, rzadkie, wewnętrzne, rozworu przełykowego (szkice)
- Metody operacji ▾: przegląd metod, klasyczne, laparoskopowe, hybrydowe (szkice)
- Wyniki i przygotowanie: rokowanie, co pogarsza wyniki, jak się przygotować (szkic)
- Konsultacje i koszt: konsultacje online i osobiste (Bydgoszcz, Poznań), szpital Eskulap, O mnie, opinie, koszt
- Polityka prywatności (tylko w stopce)

## Pliki
- `site/` – **nowa strona** (katalog wyjściowy dla Cloudflare Pages: `site`, bez polecenia budowania). Wdrożenie WSTRZYMANE do decyzji autora.
- `build/` – źródła: `build_site.py` (generuje `site/`), `style.css`, `menu.js`, `reviews.json`, `fonts/`, `source-images/`.
- `archiwum/v1-poprawiona-stara-strona/` – poprzednia strona z poprawkami v1 (zapas; zawiera nieaktualne treści, np. Warszawa, rok 1979).

## Budowanie
```
python3 build/build_site.py     # wymaga: pip install pillow
```

## Decyzje autora
- Bez cennika: koszt „zostanie jednoznacznie określony po zbadaniu chorego”; dolna granica 6000 zł (prosta przepuklina, wrota 1–2 cm, zamykana szwami); raty możliwe. Czas pobytu: do ustalenia po badaniu.
- Profesor od 2012; kierował Kliniką 12 lat; prywatnie od 2020. Bez roku 1979. Strona tylko o przepuklinach (bez chirurgii otyłości).
- Konsultacje wyłącznie w Bydgoszczy i Poznaniu oraz online. Online: pacjenta z przepukliną brzuszną nie można zakwalifikować po rozmowie; badanie zawsze potrzebne, czasem tomografia.
- Każda zakwalifikowana osoba dostaje na piśmie zalecenia przed i po operacji (zamiast osobnej strony „po operacji”).
- Strona główna lakonicznie; szczegóły konsultacji, szpitala, życiorysu, opinii i kosztu na ostatniej stronie.
- Język prosty, dla zwykłych pacjentów.
- Przepukliny rozworu przełykowego autor NIE operuje: strona i sekcja w metodach tylko informacyjnie. Obserwacja przepuklin bezobjawowych: pomijamy (zostaje „jedyna rada to operacja”).
- Bez wzmianek o technice robotowej (autor jej nie stosuje). Bez przepukliny pachwinowej (osobne strony autora).
- Próg: laparoskopia do 5–8 cm, operacja otwarta od ok. 8–10 cm, hybrydowa 5–10 cm; ubytek 1–2 cm zamykany szwami, większy siatką. Spójność tych zasad między stronami jest obowiązkowa.
- Pytania i odpowiedzi dopasowane do tematu każdej podstrony (po 3), odpowiedzi szersze niż tekst strony.
- Nagłówek H1: maks. 70% szerokości okna, dłuższy zawija się.
- Fragmenty oznaczone „szkic do akceptacji” wymagają zatwierdzenia przed publikacją.

## Do ustalenia / zrobienia
- Link do profilu na ZnanymLekarzu (obecny jest profil bariatry z Warszawą, do podmiany).
- Zatwierdzenie szkiców: pępkowa, lędźwiowa, rzadkie, wewnętrzne, rozwór przełykowy, klasyczne, laparoskopowe, hybrydowe, wyniki i przygotowanie, sekcje Objawy/Ciekawostka/Metoda według rodzaju (po zatwierdzeniu usunąć plakietki „szkic").
- Ilustracje do nowych stron (kresa, pępkowa, lędźwiowa, rzadkie, wewnętrzne, rozwór, metody) – dostarczy autor lub własne schematy.
- Sprawdzić liczby w sekcjach medycznych (źródła).
- Google Tag Manager z banerem zgody (obecnie brak cookies).
- Wdrożenie na Cloudflare Pages, przekierowania ze starych adresów, przełączenie domeny.
