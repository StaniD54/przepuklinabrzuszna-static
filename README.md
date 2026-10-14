# przepuklinabrzuszna.pl (wersja statyczna)

Strona prof. Stanisława Dąbrowieckiego o przepuklinach brzusznych. Statyczny HTML, docelowo Cloudflare Pages.

## Struktura strony (menu = kafelki na głównej, jedna lista `NAV_ITEMS` w `build/build_site.py`)
- Start
- Objawy i zdjęcia
- Rodzaje przepuklin ▾: pooperacyjna (gotowa), kresy białej, pępkowa, lędźwiowa, wewnętrzne (wkrótce)
- Metody operacji ▾: przegląd metod (jest), klasyczne, laparoskopowe, hybrydowe (wkrótce)
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
- Fragmenty oznaczone „szkic do akceptacji” wymagają zatwierdzenia przed publikacją.

## Do ustalenia / zrobienia
- Link do profilu na ZnanymLekarzu (obecny jest profil bariatry z Warszawą, do podmiany).
- Strony: kresy białej, pępkowa, lędźwiowa, wewnętrzne, klasyczne, laparoskopowe, hybrydowe.
- Przekaz o przepuklinach bez objawów (obserwacja czy zawsze operacja) – decyzja autora.
- Sprawdzić liczby w sekcjach medycznych (źródła).
- Google Tag Manager z banerem zgody (obecnie brak cookies).
- Wdrożenie na Cloudflare Pages, przekierowania ze starych adresów, przełączenie domeny.
