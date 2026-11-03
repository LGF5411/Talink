"""Vector case PDF: re-render the 12 case pages via Chromium print (selectable text, clickable links)."""
import pathlib, re
from playwright.sync_api import sync_playwright
from pypdf import PdfWriter, PdfReader

R = pathlib.Path('/root/tallink'); H = R / 'out' / '_html' / 'case'; OUT = R / 'out' / 'case'
fd = (R / 'fonts').as_uri()
FONT = "".join(f"@font-face{{font-family:'CaseInter';src:url({fd}/InterDisplay-{n}.ttf) format('truetype');font-weight:{w}}}"
               for n, w in (("Regular", 400), ("SemiBold", 600), ("Bold", 700)))
LINKS = {
    'linkedin.com/in/andrii-shnayder-a15bb8440': 'https://www.linkedin.com/in/andrii-shnayder-a15bb8440',
    'tallink.com → Christmas cruises 2026': 'https://tallink.com/travelling/cruises/christmas-season',
}
parts = []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1920, 'height': 1200})
    for i in range(1, 13):
        html = (H / f'p{i:02d}.html').read_text()
        html = html.replace('<style>', f"<style>{FONT}\n@page{{size:1920px 1200px;margin:0}}\n", 1)
        html = html.replace('</style>', ":root{--font:'CaseInter',sans-serif}</style>", 1)
        for text, url in LINKS.items():
            html = html.replace(text, f'<a href="{url}" style="color:inherit;text-decoration:underline;text-underline-offset:3px">{text}</a>', 1)
        tmp = H / f'_v{i:02d}.html'; tmp.write_text(html)
        pg.goto(tmp.as_uri(), wait_until='networkidle')
        out = OUT / f'_v{i:02d}.pdf'
        pg.pdf(path=str(out), width='1920px', height='1200px', print_background=True, prefer_css_page_size=True)
        parts.append(out); tmp.unlink()
    b.close()
w = PdfWriter()
for f in parts:
    for page in PdfReader(str(f)).pages: w.add_page(page)
w.add_metadata({'/Title': 'Pane detsember pausile — Tallinki jõulukampaania (mitteametlik kontseptsioon)', '/Author': 'Andrii Shnayder'})
final = OUT / 'Pane-detsember-pausile-kaasus-ET.pdf'
with open(final, 'wb') as fh: w.write(fh)
for f in parts: f.unlink()
r = PdfReader(str(final))
txt = r.pages[1].extract_text()[:80].replace('\n', ' ')
links = sum(1 for pgx in r.pages for a in (pgx.get('/Annots') or []) if a.get_object().get('/A'))
print('pages', len(r.pages), '| text p2:', txt, '| link annotations:', links, '| size MB', round(final.stat().st_size / 1e6, 1))
