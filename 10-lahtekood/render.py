"""Render campaign layouts (HTML -> PNG) with headless Chromium.
Usage: python3 render.py <job> ...   jobs: kv, banners
"""
import sys, pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = (ROOT / "img").as_uri()
CSS = (ROOT / "src" / "tokens.css").read_text()
OUT = ROOT / "out"

COPY = {
    "et": dict(head="Pane detsember<br>pausile.", end="Jõulud algavad pardal.",
               sub="Päev, öö või terve nädalavahetus merel.",
               offer="Jõulukruiis + jõulubuffet", price="alates XX €", note="näidishind",
               cta="Vali oma paus", cta_s="Vali paus", uf="Mitteametlik kontseptsioon"),
    "en": dict(head="Put December<br>on pause.", end="Christmas starts on board.",
               sub="A day, a night or a whole weekend at sea.",
               offer="Christmas cruise + buffet", price="from XX €", note="sample price",
               cta="Choose your pause", cta_s="Pick a pause", uf="Unofficial concept"),
}


def page(w, h, body, extra=""):
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}
html,body{{width:{w}px;height:{h}px;overflow:hidden}}
.art{{position:relative;width:{w}px;height:{h}px;overflow:hidden;background:var(--navy-800)}}
.bg{{position:absolute;inset:0;background-size:cover;background-position:center}}
.shade{{position:absolute;inset:0}}
.layer{{position:absolute}}
.cta{{display:inline-flex;align-items:center;gap:.7em;background:var(--white);color:var(--navy-900);
  font-weight:600;border-radius:999px;white-space:nowrap}}
.cta .pause{{--pw:.32em}}
.cta .pause i{{background:var(--navy-900);box-shadow:none}}
.price b{{color:var(--amber);font-weight:600}}
{extra}</style></head><body><div class="art">{body}</div></body></html>"""


def kv(w, h, lang="et", img="kv-4x5.jpg", pos="center"):
    """Master KV. Scales every size off the short side."""
    c = COPY[lang]
    s = min(w, h)
    pad = round(s * 0.07)
    vertical = h / w > 1.5
    head = round(s * (0.135 if vertical else 0.112))
    top = round(h * 0.12) if vertical else pad      # stories UI safe zone
    bot = round(h * 0.15) if vertical else pad
    return page(w, h, f"""
<div class="bg" style="background-image:url({IMG}/{img});background-position:{pos}"></div>
<div class="shade" style="background:linear-gradient(180deg,rgba(8,30,64,.55) 0%,rgba(8,30,64,0) 38%,rgba(4,16,38,0) 62%,rgba(4,16,38,.85) 100%)"></div>
<div class="layer" style="top:{top}px;left:{pad}px;right:{pad}px;display:flex;justify-content:space-between;align-items:center">
  <span class="wordmark" style="--wm:{round(s*.03)}px">TALLINK</span>
  <span class="tag-unofficial" style="--uf:{round(s*.017)}px">{c['uf']}</span>
</div>
<div class="layer" style="top:{top + round(s*0.1)}px;left:{pad}px;right:{pad}px">
  <h1 style="font-size:{head}px;line-height:.98;font-weight:600;letter-spacing:var(--tracking-head)">{c['head']}</h1>
  <p style="margin-top:{round(s*.03)}px;font-size:{round(s*.032)}px;color:var(--mist);line-height:1.3">{c['sub']}</p>
</div>
<div class="layer" style="left:{pad}px;right:{pad}px;bottom:{bot}px;display:flex;justify-content:space-between;align-items:flex-end;gap:{pad}px">
  <div>
    <p class="price" style="font-size:{round(s*.03)}px;line-height:1.35">{c['offer']}<br><b style="font-size:{round(s*.05)}px">{c['price']}</b>
      <span style="font-size:{round(s*.018)}px;color:var(--mist)">&nbsp;{c['note']}</span></p>
    <p style="margin-top:{round(s*.022)}px;font-size:{round(s*.026)}px;color:var(--white);opacity:.9">{c['end']}</p>
  </div>
  <span class="cta" style="font-size:{round(s*.03)}px;padding:{round(s*.022)}px {round(s*.034)}px"><span class="pause"><i></i><i></i></span>{c['cta']}</span>
</div>""")


def cta(c, fs, py, px, short=False):
    return f'<span class="cta" style="font-size:{fs}px;padding:{py}px {px}px"><span class="pause"><i></i><i></i></span>{c["cta_s" if short else "cta"]}</span>'


def banner(w, h, lang="et"):
    """Fixed IAB / link-ad sizes with their own layouts."""
    c = COPY[lang]
    head1 = c["head"].replace("<br>", " ")
    photo = lambda pos, size="cover": f'<div class="bg" style="background:url({IMG}/kv-4x5.jpg) {pos}/{size} no-repeat"></div>'
    uf = lambda fs, css: f'<span class="tag-unofficial layer" style="--uf:{fs}px;{css}">{c["uf"]}</span>'
    if (w, h) == (1200, 628):
        return page(w, h, f"""
{photo('right -40px top 46%', 'auto 185%')}
<div class="shade" style="background:linear-gradient(90deg,var(--navy-800) 38%,rgba(8,30,64,.6) 52%,rgba(8,30,64,0) 70%)"></div>
<div class="layer" style="left:64px;top:56px;right:600px">
  <span class="wordmark" style="--wm:22px">TALLINK</span>
  <h1 style="margin-top:56px;font-size:76px;line-height:.98;font-weight:600;letter-spacing:var(--tracking-head)">{c['head']}</h1>
  <p style="margin-top:20px;font-size:22px;color:var(--mist);line-height:1.35">{c['sub']}</p>
</div>
<div class="layer" style="left:64px;bottom:56px;display:flex;align-items:center;gap:32px">
  {cta(c, 22, 16, 26)}
  <p class="price" style="font-size:18px;line-height:1.3">{c['offer']}<br><b style="font-size:28px">{c['price']}</b> <span style="font-size:13px;color:var(--mist)">{c['note']}</span></p>
</div>
{uf(12, 'right:40px;bottom:28px')}""")
    if (w, h) == (300, 250):
        return page(w, h, f"""
{photo('center 64%', 'auto 150%')}
<div class="shade" style="background:linear-gradient(180deg,rgba(8,30,64,.9) 0%,rgba(8,30,64,0) 48%,rgba(4,16,38,.0) 60%,rgba(4,16,38,.9) 100%)"></div>
<div class="layer" style="left:18px;top:16px;right:18px">
  <h1 style="font-size:27px;line-height:1;font-weight:600;letter-spacing:var(--tracking-head)">{c['head']}</h1>
</div>
<div class="layer" style="left:18px;right:18px;bottom:16px;display:flex;justify-content:space-between;align-items:flex-end">
  <p class="price" style="font-size:11px;line-height:1.25">{c['offer']}<br><b style="font-size:17px">{c['price']}</b></p>
  {cta(c, 12, 8, 11)}
</div>
{uf(8, 'right:18px;top:20px;writing-mode:vertical-rl;opacity:.6')}""")
    if (w, h) == (728, 90):
        return page(w, h, f"""
<div class="layer" style="left:0;top:0;bottom:0;width:150px;background:url({IMG}/kv-4x5.jpg) 50% 66%/auto 330% no-repeat"></div>
<div class="shade" style="left:0;width:150px;background:linear-gradient(90deg,rgba(8,30,64,0) 55%,var(--navy-800))"></div>
<div class="layer" style="left:164px;top:0;bottom:0;display:flex;align-items:center">
  <h1 style="font-size:24px;line-height:1;font-weight:600;letter-spacing:var(--tracking-head);white-space:nowrap">{head1}</h1>
</div>
<div class="layer" style="right:20px;top:0;bottom:0;display:flex;align-items:center;gap:16px">
  <p class="price" style="font-size:18px;white-space:nowrap"><b>{c['price']}</b></p>
  {cta(c, 13, 10, 14)}
</div>
{uf(7, 'left:164px;bottom:6px;opacity:.6')}""")
    if (w, h) == (160, 600):
        return page(w, h, f"""
{photo('center 70%', 'auto 100%')}
<div class="shade" style="background:linear-gradient(180deg,var(--navy-800) 30%,rgba(8,30,64,0) 50%,rgba(4,16,38,0) 70%,var(--navy-900) 90%)"></div>
<div class="layer" style="left:16px;right:12px;top:22px">
  <span class="wordmark" style="--wm:12px">TALLINK</span>
  <h1 style="margin-top:22px;font-size:25px;line-height:1;font-weight:600;letter-spacing:var(--tracking-head)">{c['head'].replace(' ', '<br>', 1) if lang=='et' else c['head']}</h1>
  <p style="margin-top:12px;font-size:12px;color:var(--mist);line-height:1.35">{c['sub']}</p>
</div>
<div class="layer" style="left:16px;right:16px;bottom:22px">
  <p class="price" style="font-size:11px;line-height:1.3">{c['offer']}<br><b style="font-size:19px">{c['price']}</b></p>
  <div style="margin-top:12px">{cta(c, 12, 9, 12, short=True)}</div>
  <p class="tag-unofficial" style="--uf:8.5px;margin-top:10px;opacity:1">{c['uf']}</p>
</div>""")
    return kv(w, h, lang)


BANNERS = [(1080, 1080), (1080, 1350), (1080, 1920), (1200, 628), (300, 250), (728, 90), (160, 600)]


def shoot(jobs):
    OUT.mkdir(exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, w, h, html in jobs:
            pg = b.new_page(viewport={"width": w, "height": h})
            tmp = OUT / "_html" / f"{name}.html"
            tmp.parent.mkdir(parents=True, exist_ok=True)
            (OUT / f"{name}.png").parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text(html)
            pg.goto(tmp.as_uri(), wait_until="load")
            pg.wait_for_timeout(150)
            pg.screenshot(path=str(OUT / f"{name}.png"))
            pg.close()
            print("ok", name, w, h)
        b.close()


def guide():
    w, h = 1600, 1000
    sw = lambda c, n, v, t="var(--white)": f'<div><div style="height:120px;border-radius:16px;background:{c};border:1px solid rgba(255,255,255,.12)"></div><p style="margin-top:12px;font-size:15px;font-weight:600">{n}</p><p style="font-size:13px;color:var(--mist)">{v}</p></div>'
    thumb = lambda inner, ok: f'<div><div style="position:relative;height:170px;border-radius:14px;overflow:hidden;background:var(--navy-900)">{inner}</div><p style="margin-top:10px;font-size:14px;color:{"var(--amber)" if ok else "#FF8A80"}">{"✓ Nii" if ok else "✕ Mitte nii"}</p></div>'
    kvimg = f'<div style="position:absolute;inset:0;background:url({IMG}/kv-4x5.jpg) center 62%/cover"></div>'
    body = f"""
<div style="padding:64px 72px;height:100%;display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto 1fr;column-gap:56px;row-gap:44px">
 <div style="display:flex;flex-direction:column;gap:40px">
  <div><p class="tag-unofficial" style="--uf:13px">Kampaania mini-juhend · Mitteametlik kontseptsioon</p>
   <h1 style="margin-top:14px;font-size:60px;line-height:1;font-weight:600;letter-spacing:var(--tracking-head)">Pane detsember pausile.</h1>
   <p style="margin-top:14px;font-size:18px;color:var(--mist);max-width:560px;line-height:1.45">Üks võte kõigil kandjatel: kaks sooja valgusriba. Laeva akende peegeldus vees, pausimärk nupul, üleminek videos.</p></div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px">
   {sw('var(--navy-800)','Öine meri','#081E40 · taust')}{sw('var(--navy-900)','Sügav meri','#041026 · varjud')}{sw('var(--white)','Valge','#FFFFFF · tekst, CTA')}{sw('var(--amber)','Akna valgus','#F2B45E · ainus aktsent')}
  </div>
  <div style="display:flex;gap:40px;align-items:flex-end">
   <div><p style="font-size:13px;color:var(--mist);margin-bottom:8px">Pealkiri · Inter Display 600 · −2,5%</p><p style="font-size:46px;font-weight:600;letter-spacing:-.025em;line-height:1">Aa Õõ Ää</p></div>
   <div><p style="font-size:13px;color:var(--mist);margin-bottom:8px">Tekst · Inter 400</p><p style="font-size:20px;line-height:1.4">Päev, öö või terve<br>nädalavahetus merel.</p></div>
  </div>
  <div style="display:flex;gap:32px;align-items:center">
   <span class="pause" style="--pw:26px"><i></i><i></i></span>
   <p style="font-size:15px;color:var(--mist);line-height:1.5;max-width:420px">Pausimärk: riba laius = vahe, kõrgus 3,2× laius, täisümar. Alati soe valgus või laevafoto osa, mitte lame ikoon.</p>
  </div>
 </div>
 <div style="display:flex;flex-direction:column;gap:22px">
  <p style="font-size:15px;font-weight:600">Key visuali kasutamine</p>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:18px">
   {thumb(kvimg+'<p style="position:absolute;left:14px;top:14px;font-size:20px;font-weight:600;line-height:1">Pane detsember<br>pausile.</p>',True)}
   {thumb(kvimg+'<span class="cta" style="position:absolute;right:12px;bottom:12px;font-size:11px;padding:7px 11px"><span class="pause"><i></i><i></i></span>Vali oma paus</span>',True)}
   {thumb('<div style="position:absolute;inset:0;background:var(--navy-800)"></div><p style="position:absolute;left:14px;top:14px;font-size:20px;font-weight:600;line-height:1">Üks mõte<br>kandja kohta.</p><span class="pause" style="--pw:9px;position:absolute;left:16px;bottom:18px"><i></i><i></i></span>',True)}
   {thumb(kvimg+'<p style="position:absolute;left:0;right:0;top:62%;text-align:center;font-size:20px;font-weight:600">Pane detsember pausile.</p>',False)}
   {thumb('<div style="position:absolute;inset:0;background:linear-gradient(135deg,#B3122E,#0E6B3A)"></div><p style="position:absolute;left:14px;top:14px;font-size:20px;font-weight:600">❄ Jõulupakkumine! ❄</p>',False)}
   {thumb('<div style="position:absolute;inset:0;background:linear-gradient(135deg,#1E3A8A,#7C3AED)"></div><div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);font-size:64px;color:#fff;opacity:.9">⏸</div>',False)}
  </div>
  <ul style="list-style:none;display:grid;gap:10px;font-size:15px;line-height:1.45;color:var(--mist);margin-top:6px">
   <li><b style="color:var(--white);font-weight:600">Tekst taevasse, mitte vette.</b> Peegeldused on märk — neid ei kata.</li>
   <li><b style="color:var(--white);font-weight:600">Hind ja CTA alla, alati koos.</b> Loetav 2 sekundiga, üks tegevus: broneerimine.</li>
   <li><b style="color:var(--white);font-weight:600">Ainult üks soe toon.</b> Ei punast-rohelist, ei lumehelbe-clipart'i, ei gradiente.</li>
   <li><b style="color:var(--white);font-weight:600">Puhas vorm, soe tunne.</b> Öö ja valgus, mitte "tech". Pausimärk ei ilmu kunagi lameda UI-ikoonina.</li>
  </ul>
 </div>
 <div style="grid-column:1/-1;display:grid;grid-template-columns:1.2fr 1fr 1fr 1fr 1fr;gap:18px;align-items:end">
  <div><p style="font-size:15px;font-weight:600">Fotokeel</p><p style="margin-top:8px;font-size:15px;line-height:1.5;color:var(--mist)">Öö, meri, soe valgus, detailid. Kinematograafiline ja vaikne. Ei stock-naeratusi tekil.</p></div>
  <div style="height:190px;border-radius:14px;background:url({IMG}/kv-4x5.jpg) center 58%/cover"></div><div style="height:190px;border-radius:14px;background:url({IMG}/window.jpg) center 55%/cover"></div><div style="height:190px;border-radius:14px;background:url({IMG}/buffet-table.jpg) center/cover"></div><div style="height:190px;border-radius:14px;background:url({IMG}/deck-9x16.jpg) center 60%/cover"></div>
 </div>
</div>"""
    return page(w, h, body)


if __name__ == "__main__":
    jobs = []
    if "kv" in sys.argv:
        for lang in ("et", "en"):
            jobs += [
                (f"kv-1080x1350-{lang}", 1080, 1350, kv(1080, 1350, lang)),
                (f"kv-1080x1920-{lang}", 1080, 1920, kv(1080, 1920, lang)),
            ]
    if "banners" in sys.argv:
        for lang in ("et", "en"):
            jobs += [(f"banners/{lang}/{w}x{h}", w, h, banner(w, h, lang)) for w, h in BANNERS]
    if "guide" in sys.argv:
        jobs.append(("guide", 1600, 1000, guide()))
    shoot(jobs)

