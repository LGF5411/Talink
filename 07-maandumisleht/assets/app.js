/* Pane detsember pausile — landing v3 logic (unofficial concept, sample data) */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const go = (el, block = 'start') => el?.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block });
  const ic = (n) => `<svg aria-hidden="true"><use href="#i-${n}"/></svg>`;

  /* ---------- sample data (not Tallink's real prices or schedules) ---------- */
  const PAUSES = [
    { id: 'paev', name: 'Päevapaus', route: 'Tallinn ⇄ Helsingi', routeLong: 'Tallinn – Helsingi – Tallinn', len: '1 päev', from: 39, kind: 'day', img: 'assets/img/pk-paev.jpg',
      rib: [['ship', '2 h merel'], ['sun', 'Helsingi'], ['ship', '2 h merel']], sr: 'Kaks tundi merel, päev Helsingis, kaks tundi tagasi.',
      timeline: [['07:30', '', 'Väljumine Tallinnast', 'Hommikukohv ja vaade merele.', 'ship', 'tl-ship'],
                 ['09:30', '', 'Helsingi', 'Senaatori väljaku jõuluturg ja kesklinna tuled.', 'map-pin', 'tl-window'],
                 ['16:30', '', 'Tagasi pardale', 'Jõulubuffet õhtusöögiks.', 'utensils', 'tl-buffet'],
                 ['18:30', '', 'Tallinnas', 'Detsember jätkub — puhanuna.', 'house', 'tl-deck']] },
    { id: 'kruiis', name: 'Kruiisipaus', route: 'Tallinn ⇄ Stockholm', routeLong: 'Tallinn – Stockholm – Tallinn', len: '2 ööd', from: 79, kind: 'cabin', img: 'assets/img/pk-kruiis.jpg', tag: 'Kõige populaarsem',
      rib: [['moon', 'Öö merel'], ['sun', 'Stockholm'], ['moon', 'Öö merel']], sr: 'Öö merel, päev Stockholmis, öö merel tagasi.',
      timeline: [['17:30', 'Päev 1', 'Väljumine Tallinnast', 'Päev Tallinna jõuluturul, õhtu juba pardal.', 'ship', 'tl-ship'],
                 ['19:30', 'Päev 1', 'Jõulubuffet', 'Põhjamaised jõuluroad, aega on küllalt.', 'utensils', 'tl-buffet'],
                 ['22:00', 'Päev 1', 'Õhtune show', 'Elav muusika ja jõuluprogramm.', 'music', 'tl-deck'],
                 ['10:00', 'Päev 2', 'Stockholm', 'Gamla stani jõuluturg ja Skanseni tuled.', 'map-pin', 'tl-window'],
                 ['16:30', 'Päev 2', 'Tagasi pardale', 'Teine öö merel — saun või raamat.', 'bed-double', 'tl-cabin'],
                 ['10:30', 'Päev 3', 'Tallinnas', 'Puhkus, mis ei võtnud ühtegi tööpäeva rohkem kui vaja.', 'house', 'tl-ship']] },
    { id: 'pikk', name: 'Pikk paus', route: 'Tallinn ⇄ Stockholm + hotell', routeLong: 'Tallinn – Stockholm (hotell) – Tallinn', len: '3 ööd', from: 189, kind: 'cabin', img: 'assets/img/pk-pikk.jpg',
      rib: [['moon', 'Laev'], ['sun', 'Linn'], ['hotel', 'Hotell'], ['sun', 'Linn'], ['moon', 'Laev']], sr: 'Öö laeval, kaks päeva Stockholmis ja öö hotellis, öö laeval tagasi.',
      timeline: [['17:30', 'Päev 1', 'Väljumine Tallinnast', 'Jõulubuffet ja show pardal.', 'ship', 'tl-buffet'],
                 ['10:00', 'Päev 2', 'Stockholm', 'Hotelli registreerimine, terve päev linnas.', 'hotel', 'tl-window'],
                 ['—', 'Päev 3', 'Vaba päev', 'Jõuluturud, muuseumid, kohvikud.', 'map-pin', 'tl-deck'],
                 ['16:30', 'Päev 3', 'Tagasi pardale', 'Viimane õhtu merel.', 'bed-double', 'tl-cabin'],
                 ['10:30', 'Päev 4', 'Tallinnas', 'Detsembri teine pool — rahulikum.', 'house', 'tl-ship']] },
  ];
  const OPTS = {
    cabin: { title: 'Kus sa magad?', lead: 'Kõik kajutid on kahele kuni neljale. Lisatasu on inimese kohta (näidis).',
      list: [{ id: 'sise', name: 'Sisekajut', desc: 'Vaikne ja pime — kõige parem uni.', add: 0, img: 'assets/cabin-inside-800.jpg', icon: 'bed-double', alt: 'Hubane sisekajut, soe lugemislamp' },
             { id: 'meri', name: 'Merevaatega kajut', desc: 'Hommik algab merega aknas.', add: 30, img: 'assets/cabin-sea-800.jpg', icon: 'waves', alt: 'Kajut suure aknaga, väljas öine meri' },
             { id: 'prem', name: 'Premium-kajut', desc: 'Rohkem ruumi, hommikusöök kajutisse.', add: 90, img: 'assets/cabin-premium-800.jpg', icon: 'star', alt: 'Avar premium-kajut suure aknaga' }] },
    day: { title: 'Kus sa reisi ajal oled?', lead: 'Päevareisil ööbida pole vaja — vali, kui rahulikult tahad sõita (näidishinnad).',
      list: [{ id: 'istekoht', name: 'Istekoht salongis', desc: 'Pehme tool ja vaade merele.', add: 0, img: 'assets/img/opt-seat.jpg', icon: 'armchair', alt: 'Illuminaator ja hõõgvein aknalaual' },
             { id: 'comfort', name: 'Comfort-salong', desc: 'Vaiksem ala, kohv ja suupisted.', add: 15, img: 'assets/img/opt-lounge.jpg', icon: 'sofa', alt: 'Tugitool suure akna ees, väljas õhtune meri' },
             { id: 'kajut', name: 'Päevakajut', desc: 'Oma tuba kogu reisi ajaks.', add: 29, img: 'assets/img/opt-daycabin.jpg', icon: 'bed-double', alt: 'Väike hubane kajut' }] },
  };
  const YEAR = 2026, MONTH = 11;
  const MONTHS = ['jaanuar', 'veebruar', 'märts', 'aprill', 'mai', 'juuni', 'juuli', 'august', 'september', 'oktoober', 'november', 'detsember'];
  const DOW = ['P', 'E', 'T', 'K', 'N', 'R', 'L'];

  const st = { pause: 'kruiis', day: null, opt: { cabin: 'sise', day: 'istekoht' }, optTouched: false, pax: 2, club: false, promo: false };
  const P = () => PAUSES.find(p => p.id === st.pause);
  const O = () => OPTS[P().kind].list.find(o => o.id === st.opt[P().kind]);
  const k = () => (st.club ? .9 : 1) * (st.promo ? .8 : 1);
  const dayPrice = (p, d, disc = true) => {
    const dow = new Date(YEAR, MONTH, d).getDay();
    const f = 1 + ((dow === 5 || dow === 6) ? .25 : 0) + (d >= 18 && d <= 23 ? .2 : 0) + (dow === 0 || dow === 4 ? .1 : 0);
    return Math.round(p.from * f * (disc ? k() : 1));
  };
  const pp = () => (st.day ? dayPrice(P(), st.day) : Math.round(P().from * k())) + O().add;
  const total = () => pp() * st.pax;
  const fmtDate = (d) => `${DOW[new Date(YEAR, MONTH, d).getDay()]}, ${d}. ${MONTHS[MONTH]}`;
  const eur = (n) => `${n} €`;

  /* ---------- 1 · picker ---------- */
  const picker = $('[data-picker]');
  picker.innerHTML = PAUSES.map(p => `
    <button class="pk" type="button" role="radio" aria-checked="false" data-pause="${p.id}">
      <span class="pk__img"><img src="${p.img}" alt="" loading="lazy" width="1000" height="625"></span>
      ${p.tag ? `<span class="pk__tag">${p.tag}</span>` : ''}
      <span class="pk__check">${ic('check')}</span>
      <span class="pk__body">
        <span class="pk__name">${p.name}</span>
        <span class="pk__route">${ic('ship')}${p.route} · ${p.len}</span>
        <span class="rib" aria-hidden="true">${p.rib.map(([i, t]) => `<span class="rib__seg rib__seg--${i}"><span class="rib__ico">${ic(i)}</span><span class="rib__t">${t}</span></span>`).join('')}</span>
        <span class="sr-only">${p.sr}</span>
        <span class="pk__price"><span>alates</span><span><b data-pk-pp="${p.id}">${eur(p.from)}</b> / in</span></span>
      </span>
    </button>`).join('');
  picker.addEventListener('click', e => { const b = e.target.closest('[data-pause]'); if (b) setPause(b.dataset.pause); });
  picker.addEventListener('keydown', e => {
    const dir = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (!dir) return;
    e.preventDefault(); const i = PAUSES.findIndex(p => p.id === st.pause), j = (i + dir + PAUSES.length) % PAUSES.length;
    setPause(PAUSES[j].id); $(`[data-pause="${PAUSES[j].id}"]`).focus();
  });

  /* ---------- 2 · calendar ---------- */
  const grid = $('[data-cal-grid]'), cal = $('[data-cal]');
  function renderCal() {
    const p = P(), days = new Date(YEAR, MONTH + 1, 0).getDate(), lead = (new Date(YEAR, MONTH, 1).getDay() + 6) % 7;
    const prices = Array.from({ length: days }, (_, i) => dayPrice(p, i + 1));
    const lo = Math.min(...prices), hi = Math.max(...prices), focusDay = st.day || prices.indexOf(lo) + 1;
    grid.innerHTML = '<span class="day day--empty" aria-hidden="true"></span>'.repeat(lead) + prices.map((v, i) => {
      const d = i + 1, cls = v <= lo * 1.02 ? 'is-low' : v >= hi * .9 ? 'is-high' : '';
      return `<button class="day ${cls}" type="button" role="gridcell" tabindex="${d === focusDay ? 0 : -1}" aria-selected="${st.day === d}" data-day="${d}" aria-label="${fmtDate(d)}, alates ${v} eurot${cls === 'is-low' ? ', soodsam' : ''}"><span class="day__n">${d}</span><span class="day__p">${eur(v)}</span></button>`;
    }).join('');
    cal.classList.toggle('is-club', st.club || st.promo);
    $('[data-cal-hint]').textContent = [st.club && 'Club One', st.promo && 'kood PAUS20'].filter(Boolean).length ? `Soodushinnad (${[st.club && 'Club One', st.promo && 'PAUS20'].filter(Boolean).join(' + ')}) · inimese kohta · näidis` : 'Hinnad inimese kohta · näidis';
  }
  grid.addEventListener('click', e => { const b = e.target.closest('[data-day]'); if (b) setDay(+b.dataset.day, true); });
  grid.addEventListener('keydown', e => {
    const mv = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: 7, ArrowUp: -7, Home: -40, End: 40 }[e.key]; if (!mv) return;
    const cur = e.target.closest('[data-day]'); if (!cur) return; e.preventDefault();
    const days = $$('[data-day]', grid), n = Math.min(days.length, Math.max(1, +cur.dataset.day + mv)), nx = days[n - 1];
    days.forEach(x => x.tabIndex = x === nx ? 0 : -1); nx.focus();
  });

  /* ---------- 3 · seats / cabins ---------- */
  const optsWrap = $('[data-opts]');
  function renderOpts() {
    const kind = P().kind, cfg = OPTS[kind];
    $('[data-opt-title]').textContent = cfg.title; $('[data-opt-lead]').textContent = cfg.lead;
    optsWrap.innerHTML = cfg.list.map(o => `
      <button class="opt" type="button" role="radio" aria-checked="${st.opt[kind] === o.id}" tabindex="${st.opt[kind] === o.id ? 0 : -1}" data-opt="${o.id}">
        <span class="opt__img"><img src="${o.img}" alt="${o.alt}" loading="lazy" width="800" height="500"></span>
        <span class="opt__body"><span class="opt__name">${ic(o.icon)}${o.name}</span><span class="opt__desc">${o.desc}</span>
        <span class="opt__row"><span class="opt__add ${o.add ? '' : 'opt__add--in'}">${o.add ? `+ ${o.add} € / in` : 'Hinnas'}</span><span class="opt__radio" aria-hidden="true"></span></span></span>
      </button>`).join('');
  }
  optsWrap.addEventListener('click', e => { const b = e.target.closest('[data-opt]'); if (!b) return; setOpt(b.dataset.opt); });
  optsWrap.addEventListener('keydown', e => {
    const dir = { ArrowRight: 1, ArrowDown: 1, ArrowLeft: -1, ArrowUp: -1 }[e.key]; if (!dir) return; e.preventDefault();
    const list = OPTS[P().kind].list, i = list.findIndex(o => o.id === st.opt[P().kind]), n = list[(i + dir + list.length) % list.length];
    setOpt(n.id); $(`[data-opt="${n.id}"]`).focus();
  });

  /* ---------- timeline with sticky photo ---------- */
  const tlA = $('[data-tl-a]'), tlB = $('[data-tl-b]'), tlCap = $('[data-tl-cap]');
  let tlFront = tlA, tlIO;
  function showTl(src, cap) {
    if (tlCap) tlCap.textContent = cap;
    if (!tlA || tlFront.getAttribute('src') === src) return;
    const back = tlFront === tlA ? tlB : tlA;
    back.src = src; back.classList.remove('is-hidden'); tlFront.classList.add('is-hidden'); tlFront = back;
  }
  function renderTimeline() {
    const p = P();
    $('[data-prog-title]').textContent = `${p.name} tund-tunnilt`;
    const tl = $('[data-timeline]');
    tl.innerHTML = p.timeline.map(([t, d, h, txt, i, img]) => `
      <li data-img="assets/img/${img}.jpg" data-cap="${t} · ${h}"><span class="tl__ico">${ic(i)}</span>
        <div><p class="tl__t">${t}${d ? `<small>${d}</small>` : ''}</p><h4>${h}</h4><p>${txt}</p>
        <div class="tl__thumb"><img src="assets/img/${img}.jpg" alt="" loading="lazy"></div></div></li>`).join('');
    tlA.src = `assets/img/${p.timeline[0][5]}.jpg`; tlA.classList.remove('is-hidden'); tlB.classList.add('is-hidden'); tlFront = tlA;
    tlCap.textContent = `${p.timeline[0][0]} · ${p.timeline[0][2]}`;
    tlIO?.disconnect();
    tlIO = new IntersectionObserver(es => es.forEach(en => {
      if (!en.isIntersecting) return;
      $$('li', tl).forEach(li => li.classList.toggle('is-on', li === en.target));
      showTl(en.target.dataset.img, en.target.dataset.cap);
    }), { rootMargin: '-45% 0px -50% 0px' });
    $$('li', tl).forEach(li => tlIO.observe(li));
    $('li', tl).classList.add('is-on');
  }

  /* ---------- summary + steps + mobile bar ---------- */
  const sum = $('[data-summary]');
  function sync(pulse) {
    const p = P(), o = O();
    $('[data-sum-img]').src = p.img;
    $('[data-sum-len]').textContent = p.len;
    $('[data-sum-name]').textContent = p.name;
    $('[data-sum-route]').textContent = p.route;
    const sd = $('[data-sum-date]'); sd.textContent = st.day ? fmtDate(st.day) : 'Vali kalendrist'; sd.classList.toggle('is-empty', !st.day);
    $('[data-sum-opt]').textContent = o.name;
    $('[data-sum-pp]').textContent = eur(pp());
    $('[data-sum-total]').textContent = `Kokku ${eur(total())} · ${st.pax} ${st.pax === 1 ? 'reisija' : 'reisijat'}`;
    $('[data-sum-club]').hidden = !st.club;
    $('[data-sum-promo]').hidden = !st.promo;
    const tkp = $('.ticket__pp'); let em = $('em', tkp); if (st.promo && !em) { em = document.createElement('em'); tkp.append(em); } if (em) em.textContent = st.promo ? 'Sooduskood PAUS20 · −20%' : ''; if (em && !st.promo) em.remove();
    $('[data-promo-apply]').textContent = st.promo ? 'Kood lisatud ✓' : 'Kasuta koodi'; $('.offer--code').classList.toggle('is-applied', st.promo);
    const label = st.day ? 'Jätka broneerimist' : 'Vali kuupäev';
    $('[data-sum-cta]').textContent = label; $('[data-mbar-cta]').textContent = st.day ? 'Broneeri' : label;
    $('[data-mbar-name]').textContent = p.name;
    $('[data-mbar-meta]').textContent = `${st.day ? fmtDate(st.day) : 'Kuupäev valimata'} · ${eur(pp())} / in`;
    $$('[data-pax-out]').forEach(el => el.textContent = st.pax);
    $$('[data-pk-pp]').forEach(el => { const q = PAUSES.find(x => x.id === el.dataset.pkPp); el.textContent = eur(Math.round(q.from * k())); });
    $('[data-tk-pp]').textContent = eur(pp());
    // steps
    const done = [true, !!st.day, !!st.day && st.optTouched];
    const now = done.indexOf(false);
    $$('[data-step]').forEach((a, i) => { a.classList.toggle('is-done', done[i]); a.classList.toggle('is-now', i === now); a.setAttribute('aria-current', i === now ? 'step' : 'false'); });
    // club price block
    const reg = st.day ? dayPrice(p, st.day, false) : p.from;
    $('[data-save-reg]').textContent = eur(reg); $('[data-save-club]').textContent = eur(Math.round(reg * .9));
    $('[data-save-note]').textContent = `${p.name}${st.day ? ', ' + fmtDate(st.day) : ''} · inimese kohta · näidis −10%`;
    if (pulse) { sum.classList.remove('is-pulse'); void sum.offsetWidth; sum.classList.add('is-pulse'); }
    document.dispatchEvent(new CustomEvent('paus:change'));
  }
  function setPause(id) {
    st.pause = id;
    $$('[data-pause]').forEach(b => { const on = b.dataset.pause === id; b.setAttribute('aria-checked', on); b.tabIndex = on ? 0 : -1; });
    renderCal(); renderOpts(); renderTimeline(); sync(true);
  }
  function setDay(d, fromCal) {
    st.day = d;
    $$('[data-day]', grid).forEach(x => { const on = +x.dataset.day === d; x.setAttribute('aria-selected', on); x.tabIndex = on ? 0 : -1; });
    sync(true);
    if (fromCal && innerWidth > 1000 && !st.optTouched) { /* gentle guidance: show step 3 is next */ $('[data-step="3"]').classList.add('is-now'); }
  }
  function setOpt(id) { st.opt[P().kind] = id; st.optTouched = true; renderOpts(); sync(true); }
  function setPax(n) { st.pax = Math.max(1, Math.min(9, n)); sync(true); }
  document.addEventListener('click', e => { const b = e.target.closest('[data-pax]'); if (b) setPax(st.pax + +b.dataset.pax); });

  function needDate() {
    go($('#s2'), 'center');
    grid.classList.add('is-nudge'); setTimeout(() => grid.classList.remove('is-nudge'), 1200);
    setTimeout(() => $('[data-day][tabindex="0"]', grid)?.focus({ preventScroll: true }), reduce ? 0 : 600);
  }
  const dlg = $('[data-dlg]');
  function openDialog() {
    const p = P();
    $('[data-dlg-img]').src = p.img; $('[data-dlg-title]').textContent = p.name;
    $('[data-dlg-route]').textContent = p.routeLong; $('[data-dlg-date]').textContent = fmtDate(st.day);
    $('[data-dlg-opt]').textContent = O().name;
    $('[data-dlg-pax]').textContent = `${st.pax} ${st.pax === 1 ? 'reisija' : 'reisijat'}${st.club ? ' · Club One' : ''}`;
    $('[data-dlg-promo]').hidden = !st.promo;
    $('[data-dlg-total]').textContent = `${eur(total())} (näidis)`;
    dlg.showModal ? dlg.showModal() : dlg.setAttribute('open', '');
  }
  const book = () => (st.day ? openDialog() : needDate());
  $('[data-sum-cta]').addEventListener('click', book);
  $('[data-mbar-cta]').addEventListener('click', book);

  /* ---------- quick ticket ---------- */
  const tf = $('[data-book-form]'), from = $('[data-bk-from]'), to = $('[data-bk-to]'), date = $('[data-bk-date]'), msg = $('[data-bk-msg]');
  let syncing = false;
  const routePause = () => {
    const a = from.value, b = to.value;
    if (a === b) return { err: 'Vali erinev lähte- ja sihtsadam.' };
    if (a !== 'Tallinn') return { err: 'Kampaania pausid algavad Tallinnast — teised liinid leiad sõidugraafikust.' };
    return { id: b === 'Helsingi' ? 'paev' : (st.pause === 'pikk' ? 'pikk' : 'kruiis') };
  };
  function fromTicket() {
    if (syncing) return;
    const r = routePause(); msg.textContent = r.err || '';
    if (r.id && r.id !== st.pause) setPause(r.id);
    if (/^2026-12-\d\d$/.test(date.value)) setDay(+date.value.slice(8));
  }
  [from, to, date].forEach(el => el.addEventListener('change', fromTicket));
  const swap = $('[data-bk-swap]');
  swap.addEventListener('click', () => { [from.value, to.value] = [to.value, from.value]; swap.classList.toggle('is-spin'); fromTicket(); });
  document.addEventListener('paus:change', () => {
    syncing = true; from.value = 'Tallinn'; to.value = st.pause === 'paev' ? 'Helsingi' : 'Stockholm';
    date.value = st.day ? `2026-12-${String(st.day).padStart(2, '0')}` : ''; syncing = false;
  });
  tf.addEventListener('submit', e => {
    e.preventDefault();
    const r = routePause();
    if (r.err) { msg.textContent = r.err; (from.value !== 'Tallinn' ? from : to).focus(); return; }
    if (!/^2026-12-\d\d$/.test(date.value)) { msg.textContent = 'Vali väljumise kuupäev detsembris. Soodsamad päevad näed allpool kalendris.'; date.focus(); return; }
    msg.textContent = ''; setPause(r.id); setDay(+date.value.slice(8)); openDialog();
  });

  /* ---------- Club One ---------- */
  const clubT = $('[data-club-toggle]');
  clubT.addEventListener('change', () => {
    st.club = clubT.checked; renderCal(); sync(true);
    cal.classList.remove('is-flash'); void cal.offsetWidth; cal.classList.add('is-flash');
  });

  /* ---------- offers: promo code ---------- */
  const toastEl = $('[data-toast]'); let toastT;
  const toast = (t) => { toastEl.textContent = t; toastEl.classList.add('is-on'); clearTimeout(toastT); toastT = setTimeout(() => toastEl.classList.remove('is-on'), 2600); };
  function setPromo(on) { st.promo = on; renderCal(); sync(true); cal.classList.remove('is-flash'); void cal.offsetWidth; cal.classList.add('is-flash'); }
  $('[data-promo-apply]').addEventListener('click', () => { if (st.promo) { go($('#pausid')); return; } setPromo(true); toast('Sooduskood PAUS20 lisatud — hinnad on −20%'); });
  $('[data-promo-remove]').addEventListener('click', () => { setPromo(false); toast('Sooduskood eemaldatud'); });
  const codeBtn = $('[data-code-copy]');
  codeBtn.addEventListener('click', async () => {
    let okc = false; try { await navigator.clipboard.writeText('PAUS20'); okc = true; } catch { /* clipboard blocked */ }
    $('[data-code-state]').textContent = okc ? 'Kopeeritud' : 'PAUS20'; codeBtn.classList.toggle('is-copied', okc);
    toast(okc ? 'Kood kopeeritud' : 'Kopeeri kood käsitsi: PAUS20');
    setTimeout(() => { $('[data-code-state]').textContent = 'Kopeeri'; codeBtn.classList.remove('is-copied'); }, 2200);
  });

  /* ---------- compare slider ---------- */
  const cmp = $('[data-cmp]'), handle = $('[data-cmp-handle]');
  const setX = (v) => {
    v = Math.max(4, Math.min(96, v)); cmp.style.setProperty('--x', v + '%');
    handle.setAttribute('aria-valuenow', Math.round(v)); handle.setAttribute('aria-valuetext', `${Math.round(100 - v)}% linna, ${Math.round(v)}% merd`);
  };
  const fromPointer = (e) => { const r = cmp.getBoundingClientRect(); setX(((e.clientX - r.left) / r.width) * 100); };
  let drag = false;
  cmp.addEventListener('pointerdown', e => { drag = true; cmp.classList.add('is-used'); cmp.setPointerCapture(e.pointerId); fromPointer(e); });
  cmp.addEventListener('pointermove', e => { if (drag) fromPointer(e); });
  ['pointerup', 'pointercancel'].forEach(t => cmp.addEventListener(t, () => { drag = false; }));
  handle.addEventListener('keydown', e => {
    const cur = +handle.getAttribute('aria-valuenow');
    const v = { ArrowLeft: cur - 5, ArrowDown: cur - 5, ArrowRight: cur + 5, ArrowUp: cur + 5, Home: 4, End: 96 }[e.key];
    if (v === undefined) return; e.preventDefault(); cmp.classList.add('is-used'); setX(v);
  });
  // gentle hint: slide once when it comes into view
  if (!reduce) new IntersectionObserver(([en], o) => {
    if (!en.isIntersecting) return; o.disconnect();
    let t0; const anim = (t) => { t0 ??= t; const p = Math.min(1, (t - t0) / 1600); if (cmp.classList.contains('is-used')) return;
      setX(52 + Math.sin(p * Math.PI * 2) * 14); if (p < 1) requestAnimationFrame(anim); };
    setTimeout(() => requestAnimationFrame(anim), 500);
  }, { threshold: .5 }).observe(cmp);

  /* ---------- menu ---------- */
  const menu = $('[data-menu]'), menuBtn = $('.menubtn');
  let opener = null;
  const focusables = () => $$('a[href],button:not([hidden]),input', menu).filter(x => x.offsetParent !== null);
  function openMenu(mode, btn) {
    opener = btn; menu.hidden = false; document.body.classList.add('menu-on'); menuBtn.setAttribute('aria-expanded', 'true');
    requestAnimationFrame(() => requestAnimationFrame(() => menu.classList.add('is-open')));
    setTimeout(() => (mode === 'search' ? sIn : $('.qt', menu)).focus(), reduce ? 0 : 320);
  }
  function closeMenu(restore = true) {
    menu.classList.remove('is-open'); document.body.classList.remove('menu-on'); menuBtn.setAttribute('aria-expanded', 'false');
    sDrop.hidden = true; setTimeout(() => { menu.hidden = true; }, reduce ? 0 : 520);
    if (restore) (opener || menuBtn).focus();
  }
  $$('[data-menu-open]').forEach(b => b.addEventListener('click', () => openMenu(b.dataset.menuOpen, b)));
  $$('[data-menu-close]').forEach(b => b.addEventListener('click', () => closeMenu()));
  menu.addEventListener('keydown', e => {
    if (e.key === 'Escape') { if (!sDrop.hidden && document.activeElement === sIn && sIn.value) { sIn.value = ''; drawRes(''); return; } return closeMenu(); }
    if (e.key !== 'Tab') return;
    const f = focusables(), first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  menu.addEventListener('click', e => {
    const a = e.target.closest('a'); if (!a) return;
    if (a.dataset.gotoPause) setPause(a.dataset.gotoPause);
    if (a.dataset.jump) { e.preventDefault(); closeMenu(false); setTimeout(() => go($(a.dataset.jump)), 80); return; }
    if (a.hasAttribute('data-menu-link') || a.getAttribute('href').startsWith('#')) closeMenu(false);
  });
  document.addEventListener('keydown', e => { if (e.key === '/' && menu.hidden && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); openMenu('search', $('[data-menu-open="search"]')); } });

  /* search */
  const INDEX = [
    ['Vali oma paus', '#pausid', 'calendar-days', 'Sellel lehel'], ['Hinnakalender detsember', '#s2', 'calendar-days', 'Sellel lehel'], ['Kajutid ja istekohad', '#s3', 'bed-double', 'Sellel lehel'],
    ['Jõulubuffet ja mis on hinnas', '#hinnas', 'utensils', 'Sellel lehel'], ['Club One liikmehind', '#club-one', 'star', 'Sellel lehel'], ['Programm tund-tunnilt', '#programm', 'clock', 'Sellel lehel'],
    ['Pagas, lapsed, dokumendid (KKK)', '#kkk', 'circle-help', 'Sellel lehel'], ['Uudiskiri ja äpp', '#uudiskiri', 'mail', 'Sellel lehel'],
    ['Sõidugraafikud', 'https://www.tallink.com/ee-et/soidugraafikud', 'calendar-days', 'tallink.com'], ['Kruiisiprogramm ja artistid', 'https://www.tallink.com/ee-et/pardal/kruiisiprogramm', 'music', 'tallink.com'],
    ['Restoranid ja buffet', 'https://www.tallink.com/ee-et/pardal/buffet-restoranid-baarid', 'utensils', 'tallink.com'], ['Lastega reisimine, FriendSHIP', 'https://www.tallink.com/ee-et/laevareisid/kruiis/lastega-reisimine', 'baby', 'tallink.com'],
    ['Reisi muutmine ja tühistamine', 'https://www.tallink.com/ee-et/hea-teada/reisi-ostmine-muutmine-tuhistamine', 'refresh-ccw', 'tallink.com'], ['Terminalid ja sadamad', 'https://www.tallink.com/ee-et/hea-teada/terminalid-sadamad', 'map-pin', 'tallink.com'],
    ['Pagas ja reisitingimused', 'https://www.tallink.com/ee-et/hea-teada/reisitingimused', 'luggage', 'tallink.com'], ['Pakkumised ja sooduskoodid', 'https://www.tallink.com/ee-et/pakkumised-soodustused', 'tag', 'tallink.com'],
    ['Klienditeenindus', 'https://www.tallink.com/ee-et/hea-teada/kontaktid', 'headset', 'tallink.com'], ['Club One liitumine', 'https://clubone.tallink.com/et/liitumine', 'circle-user', 'clubone.tallink.com'],
  ];
  const sIn = $('[data-search-input]'), sRes = $('[data-search-res]'), sHint = $('[data-search-hint]'), sDrop = $('[data-search-drop]');
  const norm = t => t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  function drawRes(q) {
    const n = norm(q.trim()), hits = n ? INDEX.filter(([t]) => norm(t).includes(n)) : INDEX.slice(0, 6);
    sHint.textContent = n ? (hits.length ? `${hits.length} tulemust` : 'Ei leidnud — proovi „buffet“, „pagas“ või „kajut“') : 'Populaarne';
    sRes.innerHTML = hits.map(([t, h, i, w]) => `<li><a href="${h}"${h.startsWith('#') ? ` data-jump="${h}"` : ''}>${ic(i)}${t}<small>${w}</small></a></li>`).join('');
    sDrop.hidden = false;
  }
  sIn.addEventListener('focus', () => drawRes(sIn.value));
  sIn.addEventListener('input', () => drawRes(sIn.value));
  sIn.addEventListener('keydown', e => { if (e.key === 'ArrowDown') { e.preventDefault(); $('a', sRes)?.focus(); } });
  sRes.addEventListener('keydown', e => {
    const items = $$('a', sRes), i = items.indexOf(document.activeElement);
    if (e.key === 'ArrowDown') { e.preventDefault(); items[Math.min(items.length - 1, i + 1)]?.focus(); }
    if (e.key === 'ArrowUp') { e.preventDefault(); (i <= 0 ? sIn : items[i - 1]).focus(); }
  });
  menu.addEventListener('focusin', e => { if (!e.target.closest('.msearch')) sDrop.hidden = true; });

  /* ---------- newsletter (concept: nothing is sent) ---------- */
  const nf = $('[data-news]'), nm = $('[data-news-mail]'), nmsg = $('[data-news-msg]');
  nf.addEventListener('submit', e => {
    e.preventDefault();
    const ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(nm.value.trim());
    nm.setAttribute('aria-invalid', !ok);
    nmsg.className = 'news__msg ' + (ok ? 'is-ok' : 'is-err');
    nmsg.textContent = ok ? 'Aitäh! Kontseptsioonis kirja tegelikult ei saadeta.' : 'Kontrolli e-posti aadressi, nt nimi@email.ee';
    if (ok) nm.value = ''; else nm.focus();
  });

  /* ---------- header, progress, nav state, mobile bar, reveal ---------- */
  const hdr = $('[data-hdr]'), mbar = $('[data-mbar]'), hero = $('.hero');
  new IntersectionObserver(([en]) => { mbar.classList.toggle('is-on', !en.isIntersecting); }, { rootMargin: '-80px 0px 0px 0px' }).observe(hero);
  const solid = () => hdr.classList.toggle('is-solid', scrollY > 8); solid(); addEventListener('scroll', solid, { passive: true });
  let tick = false;
  addEventListener('scroll', () => { if (tick) return; tick = true; requestAnimationFrame(() => {
    const h = document.documentElement; hdr.style.setProperty('--p', (h.scrollTop / Math.max(1, h.scrollHeight - innerHeight)).toFixed(4)); tick = false; }); }, { passive: true });
  const navLinks = $$('.hdr__nav a');
  const navIO = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) navLinks.forEach(a => a.classList.toggle('is-on', a.getAttribute('href') === '#' + en.target.id)); }), { rootMargin: '-45% 0px -50% 0px' });
  navLinks.forEach(a => { const t = $(a.getAttribute('href')); if (t) navIO.observe(t); });
  const rio = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('is-in'); rio.unobserve(en.target); } }), { rootMargin: '0px 0px -8% 0px' });
  $$('.reveal').forEach((el, i) => { el.style.transitionDelay = `${(i % 4) * 70}ms`; rio.observe(el); });

  /* public API (used by tests and the case page) */
  window.PAUS = { state: () => ({ ...st }), setPause, setDay, setPax, setPromo, setClub: (on) => { clubT.checked = !!on; clubT.dispatchEvent(new Event('change')); } };
  setPause(st.pause);
})();

/* day / night switch — remembers the choice, animates with a circular reveal where supported */
(() => {
  const root = document.documentElement, btn = document.querySelector('[data-theme-toggle]');
  if (!btn) return;
  const meta = document.querySelector('meta[name=theme-color]'), lbl = btn.querySelector('[data-theme-label]');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const sync = () => {
    const day = root.dataset.theme === 'day', t = day ? 'Öine vaade' : 'Päevane vaade';
    btn.setAttribute('aria-pressed', String(day)); btn.setAttribute('aria-label', t); btn.title = t;
    if (lbl) lbl.textContent = day ? 'Öö' : 'Päev';
    if (meta) meta.content = day ? '#F6F3EE' : '#081E40';
  };
  const apply = (day) => {
    if (day) root.dataset.theme = 'day'; else delete root.dataset.theme;
    try { localStorage.setItem('paus-theme', day ? 'day' : 'night'); } catch (e) {}
    sync();
  };
  btn.addEventListener('click', () => {
    const day = root.dataset.theme !== 'day';
    if (reduce || !document.startViewTransition) return apply(day);
    const r = btn.getBoundingClientRect(), x = r.left + r.width / 2, y = r.top + r.height / 2;
    const end = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    document.startViewTransition(() => apply(day)).ready.then(() => {
      root.animate({ clipPath: [`circle(0 at ${x}px ${y}px)`, `circle(${end}px at ${x}px ${y}px)`] },
        { duration: 700, easing: 'cubic-bezier(.16,1,.3,1)', pseudoElement: '::view-transition-new(root)' });
    });
  });
  sync();
})();
