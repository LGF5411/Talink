/* Pane detsember pausile — landing logic (unofficial concept, sample data) */
(() => {
  const root = document.documentElement;
  const base = (document.querySelector('[data-asset-base]') || {}).dataset?.assetBase || 'assets/';
  const img = (n) => base + n;

  // Sample data only — not Tallink's real prices or schedules.
  const PAUSES = [
    { id: 'paev', name: 'Päevapaus', h: [26, 26], meta: 'Tallinn ⇄ Helsingi · 1 päev',
      desc: 'Hommikul laevale, päev Helsingi jõuluturul, õhtul kodus.', from: 39, route: 'Tallinn – Helsingi – Tallinn', cabins: false,
      timeline: [
        ['07:30', 'Väljumine Tallinnast', 'Hommikukohv ja vaade merele.'],
        ['09:30', 'Helsingi', 'Senaatori väljaku jõuluturg ja kesklinna tuled.'],
        ['16:30', 'Tagasi pardale', 'Jõulubuffet õhtusöögiks.'],
        ['18:30', 'Tallinnas', 'Detsember jätkub — puhanuna.'] ] },
    { id: 'kruiis', name: 'Kruiisipaus', h: [44, 44], meta: 'Tallinn ⇄ Stockholm · 2 ööd', tag: 'Kõige populaarsem',
      desc: 'Kaks ööd merel ja päev Stockholmis. Üks reis, kaks jõuluturgu.', from: 79, route: 'Tallinn – Stockholm – Tallinn', cabins: true,
      timeline: [
        ['17:30', 'Väljumine Tallinnast', 'Päev Tallinna jõuluturul, õhtu juba pardal.', 'Päev 1'],
        ['19:30', 'Jõulubuffet', 'Põhjamaised jõuluroad, aega on küllalt.', 'Päev 1'],
        ['22:00', 'Õhtune show', 'Elav muusika ja jõuluprogramm.', 'Päev 1'],
        ['10:00', 'Stockholm', 'Gamla stani jõuluturg ja Skanseni tuled.', 'Päev 2'],
        ['16:30', 'Tagasi pardale', 'Teine öö merel, saun või raamat.', 'Päev 2'],
        ['10:30', 'Tallinnas', 'Puhkus, mis ei võtnud ühtegi tööpäeva rohkem kui vaja.', 'Päev 3'] ] },
    { id: 'pikk', name: 'Pikk paus', h: [68, 68], meta: 'Kruiis + hotell Stockholmis · 3 päeva',
      desc: 'Laev, hotell ja kaks päeva Stockholmis. Detsember jääb sadamasse.', from: 189, route: 'Tallinn – Stockholm (hotell) – Tallinn', cabins: true,
      timeline: [
        ['17:30', 'Väljumine Tallinnast', 'Jõulubuffet ja show pardal.', 'Päev 1'],
        ['10:00', 'Stockholm', 'Hotelli registreerimine, terve päev linnas.', 'Päev 2'],
        ['—', 'Vaba päev', 'Jõuluturud, muuseumid, kohvikud.', 'Päev 3'],
        ['16:30', 'Tagasi pardale', 'Viimane õhtu merel.', 'Päev 3'],
        ['10:30', 'Tallinnas', 'Detsembri teine pool — rahulikum.', 'Päev 4'] ] },
  ];
  const CABINS = [
    { id: 'sise', name: 'Sisekajut', desc: 'Vaikne ja pime. Kõige parem uni.', add: 0, img: 'cabin-inside-800.jpg', alt: 'Hämar ja hubane sisekajut, soe lugemislamp' },
    { id: 'meri', name: 'Merevaatega kajut', desc: 'Hommik algab merega aknas.', add: 30, img: 'cabin-sea-800.jpg', alt: 'Kajut suure aknaga, väljas öine meri ja kalda tuled' },
    { id: 'prem', name: 'Premium-kajut', desc: 'Rohkem ruumi, hommikusöök kajutisse.', add: 90, img: 'cabin-premium-800.jpg', alt: 'Avar premium-kajut suure akna ja pehme valgusega' },
  ];
  const YEAR = 2026, MONTH = 11; // December (0-based)
  const MONTHS = ['jaanuar','veebruar','märts','aprill','mai','juuni','juuli','august','september','oktoober','november','detsember'];
  const DOW = ['P','E','T','K','N','R','L'];

  const st = { pause: 'kruiis', day: null, cabin: 'sise' };
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const P = () => PAUSES.find(p => p.id === st.pause);
  const price = (p, d) => { // sample price curve: weekends and pre-Christmas cost more
    const dow = new Date(YEAR, MONTH, d).getDay();
    let k = 1 + ((dow === 5 || dow === 6) ? .25 : 0) + (d >= 18 && d <= 23 ? .2 : 0) + (dow === 0 || dow === 4 ? .1 : 0); // never below 'alates'
    return Math.round(p.from * k);
  };
  const fmtDate = (d) => `${DOW[new Date(YEAR, MONTH, d).getDay()]}, ${d}. ${MONTHS[MONTH]}`;

  // picker
  const picker = $('[data-picker]');
  picker.innerHTML = PAUSES.map(p => `
    <button class="pk reveal" role="radio" aria-checked="false" data-pause="${p.id}">
      ${p.tag ? `<span class="pk__tag">${p.tag}</span>` : ''}
      <span class="pk__bars" aria-hidden="true"><i style="--h:${p.h[0]}px"></i><i style="--h:${p.h[1]}px"></i></span>
      <span class="pk__name">${p.name}</span>
      <span class="pk__meta">${p.meta}</span>
      <span class="pk__desc">${p.desc}</span>
      <span class="pk__price">Näidishind<span>alates <b>${p.from} €</b></span></span>
    </button>`).join('');
  picker.addEventListener('click', e => { const b = e.target.closest('[data-pause]'); if (b) setPause(b.dataset.pause); });
  picker.addEventListener('keydown', e => { // radiogroup arrow keys
    if (!['ArrowRight','ArrowDown','ArrowLeft','ArrowUp'].includes(e.key)) return;
    e.preventDefault();
    const i = PAUSES.findIndex(p => p.id === st.pause), n = PAUSES.length;
    const j = (i + (e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1 : -1) + n) % n;
    setPause(PAUSES[j].id); $(`[data-pause="${PAUSES[j].id}"]`).focus();
  });

  // calendar
  const grid = $('[data-cal-grid]');
  function renderCal() {
    const p = P(), days = new Date(YEAR, MONTH + 1, 0).getDate();
    const lead = (new Date(YEAR, MONTH, 1).getDay() + 6) % 7; // Monday first
    const prices = Array.from({ length: days }, (_, i) => price(p, i + 1));
    const lo = Math.min(...prices), hi = Math.max(...prices);
    let html = '<span class="day day--empty"></span>'.repeat(lead);
    for (let d = 1; d <= days; d++) {
      const v = prices[d - 1], cls = v <= lo * 1.02 ? 'is-low' : v >= hi * .9 ? 'is-high' : '';
      const focusDay = st.day || prices.indexOf(lo) + 1;
      html += `<button class="day ${cls}" role="gridcell" tabindex="${d === focusDay ? 0 : -1}" aria-selected="${st.day === d}" data-day="${d}" aria-label="${fmtDate(d)}, alates ${v} eurot">
        <span class="day__n">${d}</span><span class="day__p">${v} €</span></button>`;
    }
    grid.innerHTML = html;
  }
  grid.addEventListener('click', e => { const b = e.target.closest('[data-day]'); if (!b) return; st.day = +b.dataset.day; $$('[data-day]', grid).forEach(x => { x.setAttribute('aria-selected', x === b); x.tabIndex = x === b ? 0 : -1; }); sync(); });
  grid.addEventListener('keydown', e => { // roving focus: one Tab stop, arrows move by day / week
    const mv = { ArrowRight: 1, ArrowLeft: -1, ArrowDown: 7, ArrowUp: -7, Home: -40, End: 40 }[e.key]; if (!mv) return;
    const cur = e.target.closest('[data-day]'); if (!cur) return; e.preventDefault();
    const days = $$('[data-day]', grid), n = Math.min(days.length, Math.max(1, +cur.dataset.day + mv));
    const nx = days[n - 1]; days.forEach(x => x.tabIndex = x === nx ? 0 : -1); nx.focus();
  });

  // cabins
  const cabWrap = $('[data-cabins]');
  function renderCabins() {
    const p = P();
    $('[data-cab-lead]').textContent = p.cabins ? 'Kõik kajutid on kahele kuni neljale. Kajuti hind lisandub pausi hinnale (näidishinnad).' : 'Päevareisil kajutit vaja pole — salongis on istekohad ja vaade merele.';
    cabWrap.innerHTML = p.cabins ? CABINS.map(c => `
      <button class="cab" aria-pressed="${st.cabin === c.id}" data-cabin="${c.id}">
        <span class="cab__img"><img src="${img(c.img)}" alt="${c.alt}" loading="lazy" width="800" height="500"></span>
        <span class="cab__body"><span class="cab__name">${c.name}</span><span class="cab__desc">${c.desc}</span>
        <span class="cab__row"><span>${c.add ? `+ <b>${c.add} €</b> / kajut` : '<b>Hinnas</b>'}</span><span class="cab__check" aria-hidden="true"></span></span></span>
      </button>`).join('') : `<div class="seats"><span class="pause pause--glow" aria-hidden="true" style="font-size:30px"><i></i><i></i></span><p>Valisid päevapausi: istekoht salongis on hinnas. Soovi korral saab lisada päevakajuti puhkamiseks.</p></div>`;
  }
  cabWrap.addEventListener('click', e => { const b = e.target.closest('[data-cabin]'); if (!b) return; st.cabin = b.dataset.cabin; $$('[data-cabin]').forEach(x => x.setAttribute('aria-pressed', x === b)); sync(); });

  // timeline
  function renderTimeline() {
    const p = P();
    $('[data-prog-title]').textContent = `${p.name} tund-tunnilt`;
    $('[data-timeline]').innerHTML = p.timeline.map(([t, h, d, day]) => `
      <li class="reveal is-in"><span class="tl__t">${t}${day ? `<span class="tl__d">${day}</span>` : ''}</span><div><h4>${h}</h4><p>${d}</p></div></li>`).join('');
  }

  function total() {
    const p = P(); const c = CABINS.find(x => x.id === st.cabin);
    const base = st.day ? price(p, st.day) : p.from;
    return base + (p.cabins && c ? c.add : 0);
  }
  function sync() {
    const p = P();
    $('[data-bar-pause]').textContent = p.name;
    $('[data-bar-meta]').textContent = (st.day ? fmtDate(st.day) : 'Vali kuupäev') + ` · alates ${total()} €`;
  }
  function setPause(id) {
    st.pause = id;
    $$('[data-pause]').forEach(b => { const on = b.dataset.pause === id; b.setAttribute('aria-checked', on); b.tabIndex = on ? 0 : -1; });
    renderCal(); renderCabins(); renderTimeline(); sync();
  }

  // booking dialog
  const dlg = $('[data-dlg]');
  document.addEventListener('click', e => {
    const b = e.target.closest('[data-book]'); if (!b) return;
    if (!st.day) { // nudge: choose a date first
      e.preventDefault(); $('#pausid').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
      grid.classList.add('is-nudge'); setTimeout(() => grid.classList.remove('is-nudge'), 1200);
      setTimeout(() => (grid.querySelector('.day.is-low') || grid.querySelector('.day:not(.day--empty)'))?.focus({ preventScroll: true }), 600);
      return;
    }
    e.preventDefault();
    const p = P(), c = CABINS.find(x => x.id === st.cabin);
    $('[data-dlg-title]').textContent = p.name;
    $('[data-dlg-route]').textContent = p.route;
    $('[data-dlg-date]').textContent = fmtDate(st.day);
    $('[data-dlg-cabin]').textContent = p.cabins ? c.name : 'Istekoht salongis';
    $('[data-dlg-price]').textContent = `${total()} € (näidis)`;
    dlg.showModal ? dlg.showModal() : dlg.setAttribute('open', '');
  });

  // header + sticky bar visibility
  const hdr = $('[data-hdr]'), bar = $('[data-bar]'), hero = $('.hero');
  new IntersectionObserver(([en]) => { hdr.classList.toggle('is-solid', !en.isIntersecting); bar.classList.toggle('is-on', !en.isIntersecting); }, { rootMargin: '-80px 0px 0px 0px' }).observe(hero);

  // reveal on scroll
  const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) { en.target.classList.add('is-in'); io.unobserve(en.target); } }), { rootMargin: '0px 0px -8% 0px' });
  const observe = () => $$('.reveal:not(.is-in)').forEach((el, i) => { el.style.transitionDelay = `${(i % 4) * 70}ms`; io.observe(el); });

  setPause(st.pause); observe();
})();
