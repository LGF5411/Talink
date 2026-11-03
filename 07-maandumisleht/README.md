# Pane detsember pausile — maandumisleht (mitteametlik kontseptsioon)

Tallinki jõulukampaania kontseptuaalne maandumisleht portfoolio jaoks. **Ei ole Tallinki ametlik leht.** Hinnad, kuupäevad, graafikud ja paketid on näidised.

Autor: Andrii Shnayder · [LinkedIn](https://www.linkedin.com/in/andrii-shnayder-a15bb8440)

![Maandumisleht](preview-desktop.png)

## Mis siin on
- **Vali oma paus** — toote valik pausi pikkuse järgi (päev / kruiis / pikk paus). Valgusribade kõrgus = pausi pikkus.
- **Hinnakalender** — soodsamad ja populaarsed päevad, klaviatuuriga liigutav (nooled, Home/End).
- **Kajutid** — lihtsad kaardid; päevapausil kajutit ei pakuta.
- **Mis on hinnas**, **programm tund-tunnilt**, **KKK**, **lõpu-CTA**.
- **Mobiilis** kinnitatud „Broneeri" riba ja kokkuvõte enne broneerimisse suunamist.

## Tehniline
- Puhas HTML + CSS + vanilla JS, ilma ehitusetapita. Avaneb otse failist.
- Pildid `srcset`-iga (900 / 1600 / 2400 / 2880 px), laisk laadimine allpool voldi.
- Ligipääsetavus: WCAG AA kontrast, nähtav fookus, `radiogroup` noolenuppudega, kalendris üks Tab-peatus, `dialog` Esc-iga, puutealad ≥ 44 px, `prefers-reduced-motion` toetus.
- Kontrollitud laiustel 375 / 768 / 1280 / 1440 px — horisontaalset kerimist pole.

## Käivitamine
```
# avage index.html brauseris, või:
python3 -m http.server 8000
```

## GitHub Pages
1. Looge repo (nt `tallink-paus-concept`) ja laadige selle kausta sisu üles.
2. Settings → Pages → Branch: `main`, kaust `/ (root)`.
3. Leht avaneb aadressil `https://<kasutaja>.github.io/tallink-paus-concept/`.

Platvorm: Tallinki enda sait ei kasuta Shopifyd, seepärast on kampaanialeht tehtud eraldiseisva staatilise lehena, mida on lihtne mistahes CMS-i või kampaaniadomeeni alla tõsta.
