"""Print files: A3 poster + A5 flyer (2 pp). HTML in mm -> Chromium PDF (RGB)
-> Ghostscript CMYK (FOGRA39) -> TrimBox/BleedBox. Usage: python3 print.py"""
import pathlib, subprocess, io, base64
import qrcode
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject, DictionaryObject, NameObject, ArrayObject, StreamObject, TextStringObject, NumberObject
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = (ROOT / "img").as_uri()
CSS = (ROOT / "src" / "tokens.css").read_text()
OUT = ROOT / "out" / "print"
ICC = "/usr/share/texlive/texmf-dist/tex/generic/colorprofiles/FOGRA39L_coated.icc"
BLEED = 3  # mm
BOOK_URL = "https://www.tallink.com/"   # sample destination


def qr_svg(url, color="#FFFFFF"):
    q = qrcode.QRCode(border=0, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url); q.make()
    m = q.get_matrix(); n = len(m)
    rects = "".join(f'<rect x="{x}" y="{y}" width="1.02" height="1.02"/>' for y, row in enumerate(m) for x, v in enumerate(row) if v)
    return f'<svg viewBox="0 0 {n} {n}" style="width:100%;height:100%;display:block" fill="{color}" shape-rendering="crispEdges">{rects}</svg>'


def bars(h_mm, w_mm=2.4, color="var(--amber)"):
    return (f'<span style="display:inline-flex;gap:{w_mm*.9}mm;align-items:flex-end;height:{max(h_mm, w_mm*3.2)}mm">'
            f'<i style="display:block;width:{w_mm}mm;height:{h_mm}mm;border-radius:{w_mm}mm;background:{color}"></i>'
            f'<i style="display:block;width:{w_mm}mm;height:{h_mm}mm;border-radius:{w_mm}mm;background:{color}"></i></span>')


def doc(w, h, pages):
    W, H = w + 2 * BLEED, h + 2 * BLEED
    pg = "".join(f'<section class="pg">{p}</section>' for p in pages)
    fd = (ROOT / "fonts").as_uri()
    ff = "".join(f"@font-face{{font-family:'PrintInter';src:url({fd}/InterDisplay-{n}.ttf) format('truetype');font-weight:{w}}}" for n, w in (("Regular", 400), ("SemiBold", 600), ("Bold", 700)))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{ff}{CSS}
:root{{--font:'PrintInter',sans-serif}}
@page{{size:{W}mm {H}mm;margin:0}}
html,body{{background:none}}
.pg{{position:relative;width:{W}mm;height:{H}mm;overflow:hidden;page-break-after:always;background:var(--navy-800)}}
.pg:last-child{{page-break-after:auto}}
.ab{{position:absolute}}
.paper{{background:var(--paper);color:var(--ink)}}
</style></head><body>{pg}</body></html>"""


def kv_front(w, h, scale, qr=True):
    """scale: 1.0 = A3. Safe area 12mm*scale inside trim."""
    b, s = BLEED, scale
    safe = b + 14 * s
    return f"""
<div class="ab" style="inset:0;background:url({IMG}/kv-4k.jpg) center 60%/cover"></div>
<div class="ab" style="inset:0;background:linear-gradient(180deg,rgba(8,30,64,.55) 0%,rgba(8,30,64,0) 36%,rgba(4,16,38,0) 60%,rgba(4,16,38,.9) 100%)"></div>
<div class="ab" style="top:{safe}mm;left:{safe}mm;right:{safe}mm;display:flex;justify-content:space-between;align-items:center">
  <span class="wordmark" style="--wm:{9*s}mm;font-size:{9*s}mm">TALLINK</span>
  <span class="tag-unofficial" style="font-size:{3.2*s}mm">Mitteametlik kontseptsioon</span>
</div>
<div class="ab" style="top:{safe + 26*s}mm;left:{safe}mm;right:{safe}mm">
  <h1 style="font-size:{37*s}mm;line-height:.97;font-weight:600;letter-spacing:-.025em">Pane detsember<br>pausile.</h1>
  <p style="margin-top:{7*s}mm;font-size:{8.5*s}mm;color:var(--mist);line-height:1.3">Päev, öö või terve nädalavahetus merel.</p>
</div>
<div class="ab" style="left:{safe}mm;right:{safe}mm;bottom:{safe}mm;display:flex;justify-content:space-between;align-items:flex-end;gap:{10*s}mm">
  <div>
    <p style="font-size:{8*s}mm;line-height:1.35">Jõulukruiis + jõulubuffet<br><b style="font-size:{15*s}mm;font-weight:600;color:var(--amber)">alates XX €</b>
      <span style="font-size:{4*s}mm;color:var(--mist)">&nbsp;näidishind</span></p>
    <p style="margin-top:{5*s}mm;font-size:{7*s}mm">Jõulud algavad pardal.</p>
  </div>
  {f'''<div style="text-align:center">
    <div style="width:{34*s}mm;height:{34*s}mm;padding:{3*s}mm;background:var(--white);border-radius:{4*s}mm">{qr_svg(BOOK_URL, "#041026")}</div>
    <p style="margin-top:{3*s}mm;font-size:{4.2*s}mm;color:var(--white)">Skanni ja vali oma paus</p></div>''' if qr else ''}
</div>"""


def flyer_back(w, h):
    b = BLEED; safe = b + 10
    opt = lambda name, hgt, text, accent=False: f"""
<div style="display:grid;grid-template-columns:16mm 1fr;gap:5mm;align-items:end;padding:6mm 0;border-top:.3mm solid rgba(10,26,51,.18)">
  <div style="display:flex;align-items:flex-end;height:22mm">{bars(hgt, 2.6, "#94600F" if accent else "var(--ink)")}</div>
  <div><p style="font-size:6mm;font-weight:600;letter-spacing:-.02em">{name}</p>
  <p style="margin-top:1.5mm;font-size:3.6mm;line-height:1.4;color:#3A4A66">{text}</p></div>
</div>"""
    return f"""
<div class="ab paper" style="inset:0"></div>
<div class="ab" style="top:{safe}mm;left:{safe}mm;right:{safe}mm;color:var(--ink)">
  <p style="font-size:3mm;letter-spacing:.08em;text-transform:uppercase;color:#5B6B86">Tallink · Mitteametlik kontseptsioon</p>
  <h2 style="margin-top:8mm;font-size:13mm;line-height:1;font-weight:600;letter-spacing:-.025em">Kui pikk paus<br>sulle sobib?</h2>
  <div style="margin-top:9mm">
    {opt("Päevapaus", 7, "Helsingi päevareis. Hommikul laevale, õhtul tagasi.")}
    {opt("Kruiisipaus", 13, "Stockholm ja tagasi. Kaks ööd merel, päev jõuluturul. Üks reis, kaks jõuluturgu.", True)}
    {opt("Pikk paus", 20, "Kruiis + hotell Stockholmis. Detsember jääb sadamasse.")}
  </div>
</div>
<div class="ab" style="left:{safe}mm;right:{safe}mm;bottom:{safe}mm;display:flex;justify-content:space-between;align-items:flex-end;color:var(--ink)">
  <div>
    <p style="font-size:3.6mm;line-height:1.5">Hinnas: jõulubuffet · õhtune show · hommik uues linnas</p>
    <p style="margin-top:2mm;font-size:9mm;font-weight:600;color:#94600F">alates XX € <span style="font-size:3mm;font-weight:400;color:#5B6B86">näidishind</span></p>
  </div>
  <div style="text-align:center">
    <div style="width:24mm;height:24mm">{qr_svg(BOOK_URL, "#0A1A33")}</div>
    <p style="margin-top:2mm;font-size:3mm">Broneeri</p>
  </div>
</div>"""


def render_pdf(name, w, h, pages):
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = OUT / f"_{name}.html"; tmp.write_text(doc(w, h, pages))
    rgb = OUT / f"_{name}-rgb.pdf"
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page()
        pg.goto(tmp.as_uri(), wait_until="networkidle")
        pg.pdf(path=str(rgb), width=f"{w+2*BLEED}mm", height=f"{h+2*BLEED}mm", print_background=True, prefer_css_page_size=True)
        br.close()
    cmyk = OUT / f"_{name}-cmyk.pdf"
    subprocess.run(["gs", "-q", "-dBATCH", "-dNOPAUSE", "-dSAFER", "-sDEVICE=pdfwrite",
                    "-dCompatibilityLevel=1.6", "-sColorConversionStrategy=CMYK", "-sProcessColorModel=DeviceCMYK",
                    f"-sOutputICCProfile={ICC}", "-dOverrideICC=true", "-dPDFSETTINGS=/prepress",
                    "-dDownsampleColorImages=false", "-dAutoFilterColorImages=false", "-dColorImageFilter=/DCTEncode",
                    f"-sOutputFile={cmyk}", str(rgb)], check=True)
    # set Trim/Bleed boxes (pt)
    mm = 72 / 25.4
    r = PdfReader(str(cmyk)); wr = PdfWriter()
    for page in r.pages:
        W, H = float(page.mediabox.width), float(page.mediabox.height)
        page.bleedbox = RectangleObject([0, 0, W, H])
        page.trimbox = RectangleObject([BLEED * mm, BLEED * mm, W - BLEED * mm, H - BLEED * mm])
        wr.add_page(page)
    icc = StreamObject(); icc._data = open(ICC, 'rb').read()
    icc.update({NameObject('/N'): NumberObject(4)})
    oi = DictionaryObject({NameObject('/Type'): NameObject('/OutputIntent'), NameObject('/S'): NameObject('/GTS_PDFX'),
        NameObject('/OutputConditionIdentifier'): TextStringObject('FOGRA39'), NameObject('/Info'): TextStringObject('Coated FOGRA39 (ISO 12647-2:2004)'),
        NameObject('/RegistryName'): TextStringObject('http://www.color.org'), NameObject('/DestOutputProfile'): wr._add_object(icc)})
    wr._root_object[NameObject('/OutputIntents')] = ArrayObject([wr._add_object(oi)])
    wr.add_metadata({'/Title': name, '/Author': 'Andrii Shnayder', '/Subject': 'Mitteametlik kontseptsioon'})
    final = OUT / f"{name}.pdf"
    with open(final, "wb") as f: wr.write(f)
    for t in (tmp, rgb, cmyk): t.unlink()
    print("ok", final)


if __name__ == "__main__":
    render_pdf("poster-A3-ET", 297, 420, [kv_front(297, 420, 1.0)])
    render_pdf("flyer-A5-ET", 148, 210, [kv_front(148, 210, 0.5, qr=False), flyer_back(148, 210)])
