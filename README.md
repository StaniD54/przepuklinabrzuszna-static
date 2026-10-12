# przepuklinabrzuszna.pl (wersja statyczna)

Strona prof. Stanisława Dąbrowieckiego o przepuklinach brzusznych. Statyczny HTML, docelowo Cloudflare Pages.

## Struktura
- `site/` – **nowa strona** (gotowa do wdrożenia; katalog wyjściowy dla Cloudflare Pages: `site`, bez polecenia budowania).
- `build/` – źródła: `build_site.py` (generuje `site/`), `style.css`, `reviews.json`, `fonts/` (Source Serif 4, Hanken Grotesk, hostowane lokalnie), `source-images/`.
- `archiwum/v1-poprawiona-stara-strona/` – dotychczasowa strona (eksport z WordPressa/OptimizePress) z poprawkami v1 (title/meta, przyciski kontaktu, FAQ, bez tabeli cen). Zapas, gdyby trzeba było wrócić.

## Budowanie
```
python3 build/build_site.py     # wymaga: pip install pillow
```
Skrypt przeładowuje obrazy do WebP i zapisuje `site/`.

## Decyzje
- Bez cennika: koszt „zostanie jednoznacznie określony po zbadaniu chorego”; dolna granica 6000 zł (prosta przepuklina o średnicy wrót 1–2 cm, zamykana szwami); raty możliwe.
- Czas pobytu w szpitalu: do ustalenia po badaniu chorego.
- Profesor od 2012. E-mail: s.dabrowiecki@outlook.com.
- Układ i kroje pisma jak na stronie meshfreehernia.
- Fragmenty oznaczone „szkic do akceptacji” wymagają zatwierdzenia przez autora przed publikacją.

## Do zrobienia
- Strony: przepuklina pępkowa i białej kreski, po operacji, plastyka brzucha jako osobna.
- `/o-mnie/`, `/cookies/`, Google Tag Manager z banerem zgody.
- Wdrożenie na Cloudflare Pages, przekierowania ze starych adresów, przełączenie domeny.
