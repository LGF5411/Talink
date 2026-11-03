"""Internal campaign presentation: 6 slides 1920x1080 (ET) -> PNG + PDF."""
import pathlib
from PIL import Image
from render import page, shoot, IMG, OUT, ROOT

O = (ROOT / "out").as_uri()
W, H = 1920, 1080


def frame(n, body, dark=True):
    bg = "var(--navy-800)" if dark else "var(--paper)"
    fg = "var(--white)" if dark else "var(--ink)"
    sub = "var(--mist)" if dark else "#5B6B86"
    return page(W, H, f"""
<div class="layer" style="inset:0;background:{bg};color:{fg}">
 {body}
 <div class="layer" style="left:96px;right:96px;bottom:48px;display:flex;justify-content:space-between;font-size:16px;color:{sub}">
  <span><b style="letter-spacing:.16em;font-weight:700;color:{fg}">TALLINK</b>&nbsp;&nbsp;·&nbsp;&nbsp;Pane detsember pausile</span>
  <span>Mitteametlik kontseptsioon · {n}/6</span>
 </div>
</div>""")


EY = lambda t, c="var(--mist)": f'<p style="font-size:18px;letter-spacing:.1em;text-transform:uppercase;font-weight:600;color:{c}">{t}</p>'
H2 = lambda t, s=88: f'<h2 style="font-size:{s}px;line-height:1;font-weight:600;letter-spacing:-.025em">{t}</h2>'
P = lambda t, c="var(--mist)", s=26: f'<p style="font-size:{s}px;line-height:1.45;color:{c}">{t}</p>'


def s1():
    return frame(1, f"""
<div class="layer" style="right:0;top:0;bottom:0;width:52%;background:url({IMG}/kv-4x5.jpg) center 62%/cover"></div>
<div class="layer" style="right:0;top:0;bottom:0;width:52%;background:linear-gradient(90deg,var(--navy-800),rgba(8,30,64,0) 40%)"></div>
<div class="layer" style="left:96px;top:96px;width:44%">
  {EY('Jõuluhooaja kampaania · tutvustus tiimile')}
  <h1 style="margin-top:40px;font-size:148px;line-height:.95;font-weight:600;letter-spacing:-.03em">Pane detsember<br>pausile.</h1>
  <div style="margin-top:40px">{P('Üks emotsionaalne mõte, sama selge pakkumine ja kõik kanalid ühes visuaalses keeles: bännerid, trükk, uudiskiri, video ja maandumisleht.', s=28)}</div>
  <p style="margin-top:64px;font-size:20px;color:var(--mist)">Andrii Shnayder · november 2026</p>
</div>""")


def s2():
    card = lambda k, t, d: f'<div style="padding:40px;border-radius:24px;background:var(--navy-700)">{EY(k)}<p style="margin-top:18px;font-size:34px;font-weight:600;letter-spacing:-.02em;line-height:1.15">{t}</p><p style="margin-top:14px;font-size:22px;line-height:1.45;color:var(--mist)">{d}</p></div>'
    return frame(2, f"""
<div class="layer" style="left:96px;top:96px;right:96px">
  {EY('Lähtekoht')}
  <div style="margin-top:28px">{H2('Detsember on aasta kõige kiirem kuu.<br><span style="color:var(--mist)">Meri on selle ainus paus.</span>', 84)}</div>
</div>
<div class="layer" style="left:96px;right:96px;bottom:140px;display:grid;grid-template-columns:repeat(3,1fr);gap:28px">
  {card('Täna', 'Selge pakkumine', 'Kood, marsruut ja hind „alates“ — arusaadav ja müüv. Seda hoiame alles.')}
  {card('Kitsaskoht', 'Räägime allahindlusest', 'Hooajad näevad sarnased välja, visuaal on tihti stock-pilt seltskonnast tekil.')}
  {card('Võimalus', 'Üks tunne + sama pakkumine', 'Kampaania räägib sellest, mida reis annab: aega maha võtta. Hind jääb 2 sekundiga loetavaks.')}
</div>""")


def s3():
    return frame(3, f"""
<div class="layer" style="left:0;top:0;bottom:0;width:48%;background:url({IMG}/kv-4x5.jpg) 50% 78%/auto 210% no-repeat"></div>
<div class="layer" style="left:0;top:0;bottom:0;width:48%;background:linear-gradient(270deg,var(--navy-800),rgba(8,30,64,0) 35%)"></div>
<div class="layer" style="left:54%;right:96px;top:120px">
  {EY('Idee ja märk')}
  <div style="margin-top:28px">{H2('Laeva tuled vees<br>on pausimärk.', 84)}</div>
  <div style="margin-top:36px">{P('Kaks sooja valgusriba: akende peegeldus fotol, pausimärk CTA-nupul, üleminek videos, pausi pikkuse valik maandumislehel. Üks võte, mitte logo kõrval.')}</div>
  <div style="margin-top:56px;display:flex;gap:56px;align-items:flex-end">
    <div style="display:flex;gap:48px;align-items:flex-end">
      {''.join(f'<span class="pause" style="--pw:16px;gap:14px"><i style="height:{h}px;width:16px"></i><i style="height:{h}px;width:16px"></i></span>' for h in (52, 92, 140))}
    </div>
    {P('Riba kõrgus = pausi pikkus:<br><b style="color:var(--white)">päev · kruiis · nädalavahetus</b>', s=22)}
  </div>
  <p style="margin-top:56px;font-size:22px;color:var(--mist)">Lõpurida jääb Tallinki enda mõtteks: <b style="color:var(--white)">„Jõulud algavad pardal.“</b></p>
</div>""")


def s4():
    th = lambda src, w, h, cap: f'<figure style="display:grid;gap:12px;align-content:end"><div style="width:{w}px;height:{h}px;border-radius:10px;overflow:hidden;box-shadow:0 20px 50px -20px rgba(0,0,0,.6);background:url({src}) center/cover"></div><figcaption style="font-size:16px;color:var(--mist)">{cap}</figcaption></figure>'
    return frame(4, f"""
<div class="layer" style="left:96px;top:96px">{EY('Kandjad')}<div style="margin-top:24px">{H2('Üks mõte, kõik kanalid.', 72)}</div></div>
<div class="layer" style="left:96px;right:96px;top:300px;display:flex;gap:28px;align-items:flex-end">
  {th(f'{O}/banners/et/1080x1350.png', 336, 420, 'Feed 4:5')}
  {th(f'{O}/banners/et/1080x1920.png', 236, 420, 'Stories 9:16')}
  {th(f'{O}/print/poster-A3-ET-p1.jpg', 297, 420, 'Plakat A3 · terminal')}
  {th(f'{O}/print/flyer-A5-ET-p2.jpg', 296, 420, 'Flaier A5 · tagakülg')}
  <div style="display:grid;gap:28px">
    {th(f'{O}/banners/et/1200x628.png', 420, 220, 'Link-reklaam 1200×628')}
    {th(f'{O}/banners/et/728x90.png', 420, 52, 'Leaderboard 728×90')}
  </div>
</div>
<div class="layer" style="left:96px;bottom:110px">{P('Lisaks: 300×250, 160×600, 1080×1080, uudiskiri 600 px, 15 s video. Kõik ET + EN.', s=22)}</div>""")


def s5():
    return frame(5, f"""
<div class="layer" style="left:96px;top:96px;width:36%">
  {EY('Maandumisleht')}
  <div style="margin-top:24px">{H2('Vali oma paus.', 80)}</div>
  <div style="margin-top:32px">{P('Toote valik algab küsimusest, mitte tabelist: kui pikk paus sulle sobib? Valik muudab kalendri hinnad, kajutid ja programmi korraga.')}</div>
  <ul style="margin-top:36px;list-style:none;display:grid;gap:14px;font-size:22px;color:var(--mist)">
    <li>· Kalender näitab soodsamaid päevi</li><li>· Mobiilis kinnitatud „Broneeri“ riba</li><li>· Kokkuvõte enne broneerimisse suunamist</li></ul>
</div>
<div class="layer" style="right:96px;top:110px;width:840px;height:525px;border-radius:16px;overflow:hidden;box-shadow:0 40px 90px -30px rgba(0,0,0,.7);background:url({O}/landing/desktop-1440-hero.png) top/cover"></div>
<div class="layer" style="right:140px;top:400px;width:250px;height:541px;border-radius:30px;overflow:hidden;border:6px solid #000;box-shadow:0 40px 90px -30px rgba(0,0,0,.8);background:url({O}/landing/mobile-390-hero.png) top/cover"></div>""")


def s6():
    step = lambda when, what, d: f'<div style="padding-top:28px;border-top:2px solid var(--amber)"><p style="font-size:18px;color:var(--amber);font-weight:600">{when}</p><p style="margin-top:12px;font-size:30px;font-weight:600;letter-spacing:-.02em">{what}</p><p style="margin-top:10px;font-size:20px;line-height:1.45;color:var(--mist)">{d}</p></div>'
    kpi = lambda k, d: f'<div style="padding:28px;border-radius:20px;background:var(--navy-700)"><p style="font-size:24px;font-weight:600">{k}</p><p style="margin-top:8px;font-size:18px;color:var(--mist);line-height:1.4">{d}</p></div>'
    return frame(6, f"""
<div class="layer" style="left:96px;top:96px">{EY('Käivitus ja mõõtmine')}<div style="margin-top:24px">{H2('Kuidas see jookseb.', 72)}</div></div>
<div class="layer" style="left:96px;right:96px;top:330px;display:grid;grid-template-columns:repeat(4,1fr);gap:36px">
  {step('Nov, 2. pool', 'Teaser', 'Stories ja feed: „Detsember tuleb. Paus on olemas.“ Uudiskiri püsiklientidele.')}
  {step('Jõulubuffeti start', 'Põhikampaania', 'Kõik kandjad, maandumisleht, video 15 s ja 6 s.')}
  {step('Detsember', 'Terminal ja laev', 'A3 plakatid ja A5 flaierid QR-koodiga otse pausi valikusse.')}
  {step('Enne jõule', 'Viimane paus', 'Sama KV, uus pealkiri: „Viimane paus enne jõule.“')}
</div>
<div class="layer" style="left:96px;right:96px;bottom:130px;display:grid;grid-template-columns:repeat(4,1fr);gap:20px">
  {kpi('Bännerite CTR', 'vs eelmise hooaja jõulukampaania')}
  {kpi('Pausi valiku kasutus', 'mitu % maandumislehe külastajatest valib pausi')}
  {kpi('Broneerimise konversioon', 'valik → broneeringu algus')}
  {kpi('Uudiskirja avamised', 'teema A/B: „paus“ vs hinnapõhine')}
</div>""")


if __name__ == "__main__":
    jobs = [(f"slides/slide-{i}", W, H, f()) for i, f in enumerate((s1, s2, s3, s4, s5, s6), 1)]
    shoot(jobs)
    ims = [Image.open(OUT / f"slides/slide-{i}.png").convert("RGB") for i in range(1, 7)]
    ims[0].save(OUT / "slides/Pane-detsember-pausile-esitlus-ET.pdf", save_all=True, append_images=ims[1:], resolution=144)
    print("pdf ok")
