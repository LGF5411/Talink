"""Portfolio case PDF (ET), 12 pages, 1920x1200 -> PNG -> PDF."""
import pathlib
from PIL import Image
from render import page, shoot, IMG, OUT, ROOT

O = (ROOT / "out").as_uri()
W, H = 1920, 1200
LINK_LANDING = "github.io link — lisan pärast avaldamist"
LINK_VIDEO = "video link — lisan pärast üleslaadimist"


def pg(n, body, dark=True):
    bg, fg, sub = ("var(--navy-800)", "var(--white)", "var(--mist)") if dark else ("var(--paper)", "var(--ink)", "#4A5A76")
    return page(W, H, f"""
<div class="layer" style="inset:0;background:{bg};color:{fg}">{body}
 <div class="layer" style="left:96px;right:96px;bottom:44px;display:flex;justify-content:space-between;font-size:15px;color:{sub}">
  <span>Pane detsember pausile · Andrii Shnayder</span><span>Mitteametlik kontseptsioon · {n:02d}/12</span></div>
</div>""")


EY = lambda t, c="var(--mist)": f'<p style="font-size:17px;letter-spacing:.1em;text-transform:uppercase;font-weight:600;color:{c}">{t}</p>'
H2 = lambda t, s=76: f'<h2 style="font-size:{s}px;line-height:1.02;font-weight:600;letter-spacing:-.025em">{t}</h2>'
P = lambda t, c="var(--mist)", s=22: f'<p style="font-size:{s}px;line-height:1.5;color:{c}">{t}</p>'
IMGBOX = lambda src, w, h, extra="": f'<div style="width:{w}px;height:{h}px;border-radius:14px;overflow:hidden;background:url({src}) center/cover;box-shadow:0 30px 70px -30px rgba(0,0,0,.65);{extra}"></div>'
CAP = lambda t: f'<p style="margin-top:12px;font-size:15px;color:var(--mist)">{t}</p>'


def p01():
    return pg(1, f"""
<div class="layer" style="inset:0;background:url({IMG}/../landing/assets/hero-wide-2880.jpg) 70% 50%/cover"></div>
<div class="layer" style="inset:0;background:linear-gradient(90deg,rgba(8,30,64,.92) 0%,rgba(8,30,64,.55) 45%,rgba(8,30,64,0) 70%)"></div>
<div class="layer" style="left:96px;top:96px;width:900px">
  {EY('Portfoolio kaasus · kandideerimine: Disainer, Tallink Grupp')}
  <h1 style="margin-top:44px;font-size:168px;line-height:.93;font-weight:600;letter-spacing:-.03em">Pane<br>detsember<br>pausile.</h1>
  <div style="margin-top:44px;max-width:620px">{P('Tallinki jõuluhooaja kampaania: üks idee, kõik kanalid — bännerid, trükk, uudiskiri, video ja maandumisleht. Lisaks UX-vaade praegusele lehele.', s=26)}</div>
  <p style="margin-top:56px;display:inline-block;padding:10px 18px;border-radius:999px;border:1px solid var(--navy-500);font-size:17px;color:var(--mist)">Mitteametlik kontseptsioon · Unofficial concept</p>
  <p style="margin-top:28px;font-size:22px">Andrii Shnayder</p>
</div>""")


def p02():
    row = lambda k, t: f'<div style="display:grid;grid-template-columns:220px 1fr;gap:32px;padding:26px 0;border-top:1px solid rgba(255,255,255,.1)"><p style="font-size:18px;color:var(--amber);font-weight:600">{k}</p><p style="font-size:24px;line-height:1.45">{t}</p></div>'
    return pg(2, f"""
<div class="layer" style="left:96px;top:96px;width:760px">
  {EY('Ülesanne ja insight')}
  <div style="margin-top:28px">{H2('Detsember on aasta kõige kiirem kuu. Meri on selle ainus paus.', 72)}</div>
  <div style="margin-top:36px">{P('Eesmärk: jõulukampaania, mis räägib tundest, aga hoiab pakkumise sama selgena. Üks mõte, mis töötab ühtmoodi 160×600 bänneril, A3 plakatil ja 15-sekundilises videos.', s=24)}</div>
</div>
<div class="layer" style="right:96px;top:96px;width:860px">
  {row('Täna tugev', 'Selged pakkumised: marsruut, hind „alates“, palju jõulusisu (buffet, jõuluturud, jõuluvana).')}
  {row('Võimalus', 'Hooajad sarnanevad ja suhtlus räägib rohkem allahindlusest kui elamusest. Visuaal on sageli tüüpiline.')}
  {row('Lähenemine', 'Üks emotsionaalne mõte + sama selge pakkumine + puhtam ja tänapäevasem visuaalne tase.')}
  {row('Bränd', 'Töötan Tallinki brändi sees (Eesti publik, Tallinna liinid). Lõpurida „Jõulud algavad pardal“ on Tallinki enda mõte — arendan seda, ei asenda.')}
  {row('Piirid', 'Kõik hinnad ja graafikud on näidised. Broneerimissüsteemi ega kogu saidi ümberkujundust ei tee.')}
</div>""")


def p03():
    sc = [("Jõulud algavad pardal", "Laev öösel, aknad nagu jõuluehe.", "1·5·3·2", "Tallinki enda mõte — tugev bränd, aga uudsust pole."),
          ("Pane detsember pausile", "Kaks valgusriba = pausimärk. Kiire detsember → vaikne meri.", "4·4·5·5", "Värske inimlik insight ja üks graafiline võte, mis kannab kõiki kandjaid."),
          ("Üks reis. Kaks jõuluturgu.", "Graafiline marsruut, pileti esteetika.", "3·4·2·3", "Hea pakkumine, nõrk video. Helsingisse ööd pardal ei ole.")]
    cards = "".join(f'''<div style="padding:36px;border-radius:22px;background:{"var(--navy-600)" if i==1 else "var(--navy-700)"};border:1px solid {"var(--amber)" if i==1 else "transparent"};display:grid;gap:14px;align-content:start">
      <p style="font-size:16px;color:var(--mist)">Idee {i+1}</p><p style="font-size:34px;font-weight:600;letter-spacing:-.02em;line-height:1.1">{t}</p>
      <p style="font-size:19px;color:var(--mist);line-height:1.45">{d}</p>
      <p style="margin-top:8px;font-size:15px;color:var(--mist)">Värskus · Bränd · Kõik kandjad · Autor</p>
      <p style="font-size:30px;font-weight:600;color:{"var(--amber)" if i==1 else "var(--white)"};font-variant-numeric:tabular-nums">{s}</p>
      <p style="font-size:18px;line-height:1.45">{v}</p></div>''' for i, (t, d, s, v) in enumerate(sc))
    return pg(3, f"""
<div class="layer" style="left:96px;top:96px;right:96px">{EY('Kolm ideed → valik')}<div style="margin-top:24px">{H2('Valisin kõige värskema, mitte kõige turvalisema.', 68)}</div></div>
<div class="layer" style="left:96px;right:96px;top:360px;display:grid;grid-template-columns:repeat(3,1fr);gap:28px">{cards}</div>
<div class="layer" style="left:96px;right:96px;bottom:110px">{P('Lõpplahendus ühendab kolm: <b style="color:var(--white)">„Pane detsember pausile“</b> on põhimõte, <b style="color:var(--white)">„Jõulud algavad pardal“</b> lõpurida ja <b style="color:var(--white)">„Üks reis. Kaks jõuluturgu.“</b> elab kruiisipausi sees maandumislehel.', s=21)}</div>""")


def p04():
    return pg(4, f"""
<div class="layer" style="left:96px;top:96px;width:520px">
  {EY('Key visual ja mini-juhend')}
  <div style="margin-top:24px">{H2('Laeva tuled vees on pausimärk.', 64)}</div>
  <div style="margin-top:28px">{P('Kaks akende peegeldust vees moodustavad pausimärgi. Sama märk on CTA-nupul, video üleminekus ja pausi valikus. Üks võte, mitte logo kõrval.', s=21)}</div>
  <div style="margin-top:40px">{IMGBOX(f"{O}/banners/et/1080x1350.png", 420, 525)}</div>
</div>
<div class="layer" style="right:96px;top:96px">{IMGBOX(f"{O}/guide.png", 1136, 710)}{CAP('Mini-juhend: palett (üks soe aktsent), Inter Display kahe lõikega, pausimärgi konstruktsioon, KV kasutus „nii / mitte nii“, fotokeel.')}</div>""")


def p05():
    b = lambda n, w, h, cap: f'<figure>{IMGBOX(f"{O}/banners/et/{n}.png", w, h)}{CAP(cap)}</figure>'
    return pg(5, f"""
<div class="layer" style="left:96px;top:96px">{EY('Bännerid ja sotsiaalmeedia')}<div style="margin-top:24px">{H2('7 formaati × ET/EN', 64)}</div></div>
<div class="layer" style="left:96px;top:300px;display:flex;gap:28px;align-items:flex-end">
  {b('1080x1350', 360, 450, 'Feed 4:5')}{b('1080x1920', 253, 450, 'Stories — UI turvaalad')}{b('1080x1080', 380, 380, 'Feed 1:1')}
  {b('160x600', 120, 450, '160×600')}
  <div style="display:grid;gap:22px">{b('1200x628', 420, 220, 'Link-reklaam 1200×628')}{b('300x250', 240, 200, '300×250')}</div>
</div>
<div class="layer" style="left:96px;bottom:110px;width:1700px">{IMGBOX(f"{O}/banners/et/728x90.png", 728, 90)}{CAP('728×90. Väikestel formaatidel on oma paigutus, mitte vähendatud KV: tekst ei lange alla loetavuse piiri.')}</div>""")


def p06():
    return pg(6, f"""
<div class="layer" style="inset:0;background:var(--paper)"></div>
<div class="layer" style="left:96px;top:96px;width:520px;color:var(--ink)">
  {EY('Trükk ja uudiskiri', '#4A5A76')}
  <div style="margin-top:24px">{H2('Terminal, laev ja postkast.', 60)}</div>
  <div style="margin-top:26px">{P('A3 plakat ja kahepoolne A5 flaier on valmis trükikojale: CMYK FOGRA39, 3 mm üleulatus, TrimBox/BleedBox, fondid manustatud, KV ~276 ppi. QR viib otse pausi valikusse.', '#3A4A66', 20)}</div>
  <div style="margin-top:22px">{P('Flaieri tagakülg on soojal paberil: valgusribade kõrgus näitab pausi pikkust.', '#3A4A66', 20)}</div>
  <div style="margin-top:22px">{P('Uudiskiri 600 px, tabelpaigutus, mobiilis üks veerg. Teema: „Detsembri kõige rahulikum päev on merel“.', '#3A4A66', 20)}</div>
</div>
<div class="layer" style="left:680px;top:110px;transform:rotate(-1.5deg)">{IMGBOX(f"{O}/print/poster-A3-ET-p1.jpg", 470, 664, "box-shadow:0 40px 80px -30px rgba(10,26,51,.55)")}</div>
<div class="layer" style="left:1170px;top:180px;transform:rotate(2deg)">{IMGBOX(f"{O}/print/flyer-A5-ET-p1.jpg", 260, 368, "box-shadow:0 30px 60px -25px rgba(10,26,51,.5)")}</div>
<div class="layer" style="left:1230px;top:560px;transform:rotate(-2.5deg)">{IMGBOX(f"{O}/print/flyer-A5-ET-p2.jpg", 260, 368, "box-shadow:0 30px 60px -25px rgba(10,26,51,.5)")}</div>
<div class="layer" style="right:96px;top:110px">{IMGBOX(f"{O}/email/email-mobile.png", 260, 920, "background-position:top;background-size:100% auto;box-shadow:0 30px 60px -25px rgba(10,26,51,.5)")}</div>""", dark=False)


def p07():
    return pg(7, f"""
<div class="layer" style="left:96px;top:96px;width:540px">
  {EY('Maandumisleht — keskne ekraan')}
  <div style="margin-top:24px">{H2('Vali oma paus.', 72)}</div>
  <div style="margin-top:26px">{P('Toote valik algab küsimusest „kui pikk paus?“. Valik muudab korraga hinnakalendri, kajutid ja programmi. Mobiilis on „Broneeri“ riba kinnitatud ja enne broneerimisse suunamist näeb kokkuvõtet.', s=21)}</div>
  <ul style="margin-top:30px;list-style:none;display:grid;gap:12px;font-size:19px;color:var(--mist)">
   <li>· WCAG AA kontrast, nähtav fookus, puutealad ≥ 44 px</li><li>· Kalender: üks Tab-peatus, nooled liigutavad</li>
   <li>· prefers-reduced-motion, srcset-pildid</li><li>· HTML/CSS/JS — Tallinki sait ei ole Shopifys, kampaanialeht on eraldiseisev</li></ul>
  <p style="margin-top:34px;font-size:19px;color:var(--amber)">{LINK_LANDING}</p>
</div>
<div class="layer" style="left:700px;top:96px;width:1124px;height:900px;border-radius:16px;overflow:hidden;background:url({O}/landing/desktop-1440-full.png) top/100% auto;box-shadow:0 40px 90px -30px rgba(0,0,0,.7)"></div>
<div class="layer" style="left:1560px;top:420px;width:270px;height:584px;border-radius:34px;overflow:hidden;border:7px solid #000;background:url({O}/landing/mobile-390-hero.png) top/cover;box-shadow:0 40px 90px -30px rgba(0,0,0,.8)"></div>""")


def p08():
    fr = [("1.6", "Kiire detsember"), ("4.4", "Paus."), ("5.6", "Ribad → peegeldused"), ("8.6", "Valgus."), ("10.2", "Jõulubuffet."), ("13.0", "Lõpukaart")]
    cells = "".join(f'<figure>{IMGBOX(f"{O}/video/frames/f-{t}.jpg", 262, 466)}{CAP(f"{t} s · {c}")}</figure>' for t, c in fr)
    return pg(8, f"""
<div class="layer" style="left:96px;top:96px;right:96px;display:flex;justify-content:space-between;align-items:flex-end">
  <div>{EY('Video 15 s · 6 s · 1:1')}<div style="margin-top:24px">{H2('Kõige meeldejäävam hetk: üleminek.', 64)}</div></div>
  <div style="width:560px">{P('Kaks pausiriba liiguvad täpselt laeva akende peegelduste peale — kaader on mõõdetud pildi pealt. Heli on originaalne ja genereeritud koodis (tiksumine → vaikus → soe pad ja meri), seega litsentsiküsimust pole.', s=19)}<p style="margin-top:14px;font-size:18px;color:var(--amber)">{LINK_VIDEO}</p></div>
</div>
<div class="layer" style="left:96px;right:96px;top:390px;display:flex;justify-content:space-between">{cells}</div>""")


def p09():
    ba = lambda a, b, t, d: f'''<div style="display:grid;gap:14px"><div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
      <figure>{IMGBOX(a, 230, 160)}{CAP("enne")}</figure><figure>{IMGBOX(b, 230, 160)}{CAP("pärast")}</figure></div>
      <p style="font-size:22px;font-weight:600">{t}</p><p style="font-size:17px;color:var(--mist);line-height:1.5">{d}</p></div>'''
    tool = lambda k, v: f'<div style="display:grid;grid-template-columns:200px 1fr;gap:20px;padding:16px 0;border-top:1px solid rgba(255,255,255,.1)"><p style="font-size:17px;color:var(--amber);font-weight:600">{k}</p><p style="font-size:19px;line-height:1.45">{v}</p></div>'
    return pg(9, f"""
<div class="layer" style="left:96px;top:96px;width:640px">
  {EY('Kuidas kasutasin AI-d')}
  <div style="margin-top:24px">{H2('AI teeb mustandi. Otsused teen mina.', 60)}</div>
  <div style="margin-top:30px">
   {tool('Pildid', 'Higgsfield · GPT Image: KV, kajutid, buffet, linn, tekk. Valisin kaadrid ja kirjutasin promptid kampaania fotokeele järgi.')}
   {tool('Suurendus', 'ByteDance upscale 4K: KV trükiks (~276 ppi A3) ja tekk lõpukaardiks.')}
   {tool('Tekstid', 'AI mustand ET/EN → toimetasin ise. Lõplik eesti keele korrektuur on minu.')}
   {tool('Kood', 'Bännerite süsteem, trükifailid (CMYK), maandumisleht ja video kaadrid on tehtud koodis — üks token-süsteem kõigile kandjatele.')}
   {tool('Käsitsi', 'Retušš, kärpimine, kompositsioon, faktikontroll, ligipääsetavus.')}
  </div>
</div>
<div class="layer" style="left:820px;right:96px;top:110px;display:grid;grid-template-columns:1fr 1fr;gap:44px 40px">
  {ba(f"{IMG}/kv-16x9.jpg", f"{IMG}/../landing/assets/hero-wide-1600.jpg", "Mäed välja", "AI pani laeva fjordi. Läänemerel mägesid pole — ehitasin laia kaadri KV-st ja laiendasin taevast.")}
  {ba(f"{IMG}/ai-before-funnel.jpg", f"{IMG}/ai-after-funnel.jpg", "Võõras märk eemaldatud", "4K suurendus „mõtles välja“ korstnale logolaadse märgi. Retušeerisin selle — kampaanias ei tohi olla võõraid brände.")}
  {ba(f"{IMG}/../landing/assets/cabin-sea-800.jpg", f"{IMG}/../landing/assets/cabin-inside-800.jpg", "Sisekajut ilma aknata", "Esimesel „sisekajutil“ oli aken. Sisekajutil akent pole — genereerisin uue ja kasutasin esimest merevaatega kajutina.")}
  {ba(f"{IMG}/buffet.jpg", f"{IMG}/buffet-table.jpg", "Aknad ja mäed välja", "Buffet-kaadri aknas olid lumised mäed. Kärpisin laua peale; vertikaalvideo jaoks tegin eraldi kaadri.")}
</div>""")


def wire_card(lines, accent=None, h=None):
    """tiny grey wireframe card; lines = list of (width%, height px, colour key)"""
    col = {"g": "#C9CED8", "d": "#8C95A6", "a": "#F2B45E", "b": "#0A1A33", "w": "#E9ECF1"}
    rows = "".join(f'<div style="width:{w}%;height:{hh}px;border-radius:{min(hh, 8)}px;background:{col[c]}"></div>' for w, hh, c in lines)
    return f'<div style="padding:12px;border-radius:10px;background:#fff;display:grid;gap:7px;align-content:start;{"outline:2px solid #F2B45E;" if accent else ""}{f"height:{h}px;" if h else ""}">{rows}</div>'


def opp(n, title, prob, sol, eff, before, after):
    return f'''<div style="display:grid;grid-template-columns:1fr 1fr;gap:28px;padding:30px 0;border-top:1px solid rgba(10,26,51,.14)">
  <div><p style="font-size:16px;color:#94600F;font-weight:700">Võimalus {n}</p>
    <p style="margin-top:6px;font-size:28px;font-weight:600;letter-spacing:-.02em">{title}</p>
    <p style="margin-top:12px;font-size:17px;line-height:1.5"><b>Täna:</b> {prob}</p>
    <p style="margin-top:8px;font-size:17px;line-height:1.5"><b>Ettepanek:</b> {sol}</p>
    <p style="margin-top:8px;font-size:17px;line-height:1.5;color:#3A4A66"><b style="color:#0A1A33">Mõju:</b> {eff}</p></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px">
    <div><p style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#4A5A76;margin-bottom:8px">Praegu (skeem)</p><div style="padding:14px;border-radius:12px;background:#E4E0D8">{before}</div></div>
    <div><p style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#94600F;margin-bottom:8px">Ettepanek</p><div style="padding:14px;border-radius:12px;background:#E4E0D8">{after}</div></div>
  </div></div>'''


def three(cards, cols=3):
    return f'<div style="display:grid;grid-template-columns:repeat({cols},1fr);gap:8px">{"".join(cards)}</div>'


CARD = [(100, 54, "g"), (80, 9, "d"), (60, 7, "g"), (40, 10, "d"), (100, 18, "w"), (100, 18, "b")]


def p10():
    chips = '<div style="display:flex;gap:5px;margin-bottom:8px">' + "".join(f'<span style="padding:4px 8px;border-radius:99px;font-size:10px;background:{"#0A1A33" if i==0 else "#fff"};color:{"#fff" if i==0 else "#0A1A33"}">{t}</span>' for i, t in enumerate(["Tallinn", "Helsingi", "Turu", "Stockholm"])) + '</div>'
    cal = '<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:3px;margin-top:6px">' + "".join(f'<span style="height:13px;border-radius:3px;background:{"#F2B45E" if i in (3,10) else ("#0A1A33" if i==5 else "#fff")}"></span>' for i in range(14)) + '</div>'
    o1 = opp(1, "Alusta sealt, kus klient on",
             "jõululehe põhitooted algavad Soomest (Stockholm–Helsingi, Helsingi–Tallinn, Turu–Stockholm). Eesti külastaja peab ise otsima Tallinnast lähtuvat reisi.",
             "lähtelinna valik kaartide kohal (Tallinn / Helsingi / Turu / Stockholm), kaardid filtreeruvad; vaikimisi valik keele või asukoha järgi.",
             "asjakohasem esimene ekraan, vähem kerimist ja tagasipõrkeid.",
             three([wire_card(CARD)] * 3), chips + three([wire_card(CARD, accent=True)] + [wire_card(CARD)] * 2))
    o2 = opp(2, "Kuupäev enne broneerimist",
             "kõik „Book now“ nupud avavad broneerimise ühe ja sama eeltäidetud kuupäevaga. Kasutaja näeb hinda alles süsteemis.",
             "kaardil mini-hinnakalender või vahekiht „vali kuupäev“ — broneerimine avaneb juba õige kuupäevaga.",
             "vähem üllatusi broneerimissüsteemis, kõrgem jätkamise määr.",
             three([wire_card(CARD)] * 3), wire_card([(100, 54, "g"), (80, 9, "d"), (60, 7, "g")], accent=True) + cal)
    return pg(10, f"""
<div class="layer" style="inset:0;background:var(--paper);color:var(--ink)"></div>
<div class="layer" style="left:96px;top:84px;right:96px;color:var(--ink)">
  <div style="display:flex;justify-content:space-between;align-items:flex-end">
    <div>{EY('Lisaväärtus: UX-vaade · 1/2', '#4A5A76')}<div style="margin-top:20px">{H2('Võimalused praegusel jõululehel', 56)}</div></div>
    <p style="width:560px;font-size:16px;line-height:1.5;color:#4A5A76">Leht: tallink.com → Christmas cruises 2026, vaadatud 3.11.2026. Lehe tugevused jäävad alles: selged hinnad, rikkalik jõulusisu, eeltäidetud broneerimislingid.</p>
  </div>
  <div style="margin-top:28px">{o1}{o2}</div>
</div>""", dark=False)


def p11():
    card2 = [(100, 54, "g"), (80, 9, "d"), (60, 7, "g"), (100, 16, "w"), (100, 16, "b")]
    card1 = [(100, 54, "g"), (80, 9, "d"), (30, 8, "a"), (30, 8, "a"), (100, 18, "b")]
    price = lambda txts: '<div style="display:grid;gap:6px">' + "".join(f'<div style="padding:8px 10px;border-radius:8px;background:#fff;font-size:12px;display:flex;justify-content:space-between"><span>{a}</span><b>{b}</b></div>' for a, b in txts) + '</div>'
    o3 = opp(3, "Üks kaart — üks tegevus",
             "igal tootekaardil on kaks tegevust („Read more“ ja „Book now“) ning buffet ja jõuluturud on pikad tekstiplokid ilma tegevuseta.",
             "üks peamine CTA kaardil ja „Mis on hinnas“ märgid (buffet, ööd laeval, kestus) — lisainfo avaneb kaardi sees.",
             "kiirem otsus, vähem pilgu hüppamist, selgem esmane tegevus.",
             three([wire_card(card2)] * 3), three([wire_card(card1, accent=True)] + [wire_card(card1)] * 2))
    o4 = opp(4, "Hinnad ja sildid ühes keeles",
             "hinnavormingud erinevad (28,80 € · 100 € · 323 € / adult), „roundtrip“ plokis on ka ühesuunaline reis ja üks viide („top tips“) on ilma lingita.",
             "ühtne vorming „alates 28,80 € / in“, reisi tüübi silt (edasi-tagasi / ühesuunaline), puuduv link lisada; lisaks lühike KKK (lapsed, pagas, dokumendid).",
             "usaldus ja võrreldavus — klient ei pea hindu peas teisendama.",
             price([("Helsinki–Tallinn", "28,80 €"), ("Stockholm", "100 €"), ("Roundtrip*", "323 € / adult")]),
             price([("Päevareis · Helsingi", "alates 28,80 € / in"), ("Kruiis · Stockholm", "alates 100,00 € / in"), ("Ühesuunaline · Turu", "alates 323,00 € / in")]))
    return pg(11, f"""
<div class="layer" style="inset:0;background:var(--paper);color:var(--ink)"></div>
<div class="layer" style="left:96px;top:84px;right:96px;color:var(--ink)">
  <div>{EY('Lisaväärtus: UX-vaade · 2/2', '#4A5A76')}<div style="margin-top:20px">{H2('Väikesed muudatused, suur selgus', 56)}</div></div>
  <div style="margin-top:28px">{o3}{o4}</div>
  <p style="margin-top:18px;font-size:16px;color:#4A5A76">Skeemid on tehtud lehe struktuuri põhjal. Kõik ettepanekud sobivad praeguse broneerimissüsteemiga — muutub ainult kampaanialeht.</p>
</div>""", dark=False)


def p12():
    return pg(12, f"""
<div class="layer" style="inset:0;background:url({IMG}/../landing/assets/deck-1800.jpg) center 55%/cover"></div>
<div class="layer" style="inset:0;background:radial-gradient(ellipse at 30% 50%,rgba(4,16,38,.55),rgba(4,16,38,.92))"></div>
<div class="layer" style="left:96px;top:50%;transform:translateY(-50%);width:900px">
  <span class="pause" style="--pw:16px"><i></i><i></i></span>
  <div style="margin-top:36px">{H2('Aitäh, et vaatasite.<br>Seilame koos?', 92)}</div>
  <div style="margin-top:32px">{P('Valmis tööks Tallinki loovtiimis esimesest päevast: turundusdisain kõigis kanalites ja UX/UI lisaväärtusena.', s=24)}</div>
  <div style="margin-top:44px;display:grid;gap:10px;font-size:24px">
    <p><b>Andrii Shnayder</b></p>
    <p style="color:var(--mist)">linkedin.com/in/andrii-shnayder-a15bb8440</p>
  </div>
</div>""")


if __name__ == "__main__":
    fns = (p01, p02, p03, p04, p05, p06, p07, p08, p09, p10, p11, p12)
    shoot([(f"case/p{i:02d}", W, H, f()) for i, f in enumerate(fns, 1)])
    ims = [Image.open(OUT / f"case/p{i:02d}.png").convert("RGB") for i in range(1, 13)]
    ims[0].save(OUT / "case/Pane-detsember-pausile-kaasus-ET.pdf", save_all=True, append_images=ims[1:], resolution=150)
    print("pdf ok")
