/* Site layer v2 — menu, search, quick booking, Club One, newsletter (unofficial concept) */
(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const go = el => el?.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth' });

  /* ---------- full-screen menu (pause bars turn into a close mark) ---------- */
  const menu = $('[data-menu]'), hdrBtn = $('.hdr [data-menu-open="nav"]');
  let lastOpener = null;
  const focusables = () => $$('a[href],button,input', menu).filter(x => x.offsetParent !== null);
  function openMenu(mode, opener) {
    lastOpener = opener;
    const r = (opener || hdrBtn).getBoundingClientRect();
    menu.style.setProperty('--ox', `${r.left + r.width / 2}px`); menu.style.setProperty('--oy', `${r.top + r.height / 2}px`);
    menu.hidden = false; document.body.classList.add('menu-on');
    hdrBtn.setAttribute('aria-expanded', 'true'); hdrBtn.classList.add('is-x');
    requestAnimationFrame(() => requestAnimationFrame(() => menu.classList.add('is-open')));
    drawRes('');
    setTimeout(() => (mode === 'search' ? $('[data-search-input]') : focusables()[1])?.focus(), reduce ? 0 : 260);
  }
  function closeMenu(restore = true) {
    menu.classList.remove('is-open'); hdrBtn.classList.remove('is-x'); hdrBtn.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('menu-on');
    setTimeout(() => { menu.hidden = true; }, reduce ? 0 : 420);
    if (restore) (lastOpener || hdrBtn).focus();
  }
  $$('[data-menu-open]').forEach(b => b.addEventListener('click', () => openMenu(b.dataset.menuOpen, b)));
  $('[data-menu-close]').addEventListener('click', () => closeMenu());
  menu.addEventListener('keydown', e => {
    if (e.key === 'Escape') return closeMenu();
    if (e.key !== 'Tab') return;
    const f = focusables(), first = f[0], last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  menu.addEventListener('click', e => {
    const a = e.target.closest('a'); if (!a) return;
    if (a.dataset.jump) { e.preventDefault(); closeMenu(false); setTimeout(() => go($(a.dataset.jump)), 60); return; }
    if (a.getAttribute('href').startsWith('#')) { closeMenu(false); }
  });
  document.addEventListener('keydown', e => { if (e.key === '/' && menu.hidden && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); openMenu('search', $('.hdr [data-menu-open="search"]')); } });

  /* ---------- search: this page + real tallink.com sections ---------- */
  const INDEX = [
    ['Vali oma paus', '#pausid', 'Sellel lehel'], ['Hinnakalender detsember', '#pausid', 'Sellel lehel'], ['Kajutid', '[data-cabins-sec]', 'Sellel lehel'],
    ['Jõulubuffet — mis on hinnas', '#hinnas', 'Sellel lehel'], ['Club One liikmehinnad', '#club-one', 'Sellel lehel'], ['Programm tund-tunnilt', '#programm', 'Sellel lehel'],
    ['Pagas, lapsed, dokumendid — KKK', '#kkk', 'Sellel lehel'], ['Uudiskiri', '#uudiskiri', 'Sellel lehel'],
    ['Sõidugraafikud', 'https://www.tallink.com/ee-et/soidugraafikud', 'tallink.com'], ['Kruiisiprogramm ja artistid', 'https://www.tallink.com/ee-et/pardal/kruiisiprogramm', 'tallink.com'],
    ['Restoranid ja buffet', 'https://www.tallink.com/ee-et/pardal/buffet-restoranid-baarid', 'tallink.com'], ['Lastega reisimine, FriendSHIP', 'https://www.tallink.com/ee-et/laevareisid/kruiis/lastega-reisimine', 'tallink.com'],
    ['Reisi muutmine ja tühistamine', 'https://www.tallink.com/ee-et/hea-teada/reisi-ostmine-muutmine-tuhistamine', 'tallink.com'], ['Terminalid ja sadamad', 'https://www.tallink.com/ee-et/hea-teada/terminalid-sadamad', 'tallink.com'],
    ['Reisitingimused', 'https://www.tallink.com/ee-et/hea-teada/reisitingimused', 'tallink.com'], ['Pakkumised ja sooduskoodid', 'https://www.tallink.com/ee-et/pakkumised-soodustused', 'tallink.com'],
    ['Klienditeenindus', 'https://www.tallink.com/ee-et/hea-teada/kontaktid', 'tallink.com'], ['Club One liitumine', 'https://clubone.tallink.com/et/liitumine', 'clubone.tallink.com'],
  ];
  const sIn = $('[data-search-input]'), sRes = $('[data-search-res]'), sHint = $('[data-search-hint]');
  const norm = t => t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
  function drawRes(q) {
    const n = norm(q.trim());
    const hits = n ? INDEX.filter(([t]) => norm(t).includes(n)) : INDEX.slice(0, 5);
    sHint.textContent = n ? (hits.length ? `${hits.length} tulemust` : 'Ei leidnud — proovi „buffet“, „pagas“ või „kajut“') : 'Populaarne';
    sRes.innerHTML = hits.map(([t, h, w]) => `<li><a href="${h.startsWith('[') ? '#' : h}"${h.startsWith('[') ? ` data-jump="${h}"` : ''}>${t}<small>${w}</small></a></li>`).join('');
  }
  sIn.addEventListener('input', () => drawRes(sIn.value));

  /* links that choose a pause */
  document.addEventListener('click', e => { const a = e.target.closest('[data-goto-pause]'); if (a && window.PAUS) window.PAUS.setPause(a.dataset.gotoPause); });

  /* ---------- quick booking <-> picker / calendar ---------- */
  const f = $('[data-book-form]'), from = $('[data-bk-from]'), to = $('[data-bk-to]'), date = $('[data-bk-date]'), paxOut = $('[data-bk-pax]'), msg = $('[data-bk-msg]');
  let syncing = false;
  const routePause = () => {
    const a = from.value, b = to.value, pair = [a, b].sort().join('-');
    if (a === b) return { err: 'Vali erinev lähte- ja sihtsadam.' };
    if (a !== 'Tallinn') return { err: 'Kampaania pausid algavad Tallinnast — teised liinid leiad sõidugraafikust.' };
    return { id: pair === 'Helsingi-Tallinn' ? 'paev' : (window.PAUS?.state().pause === 'pikk' ? 'pikk' : 'kruiis') };
  };
  function fromWidget() {
    if (syncing || !window.PAUS) return;
    const r = routePause(); msg.textContent = r.err || '';
    if (r.id && r.id !== window.PAUS.state().pause) window.PAUS.setPause(r.id);
    if (/^2026-12-\d\d$/.test(date.value)) window.PAUS.setDay(+date.value.slice(8));
  }
  [from, to, date].forEach(el => el.addEventListener('change', fromWidget));
  const swap = $('[data-bk-swap]');
  swap.addEventListener('click', () => { [from.value, to.value] = [to.value, from.value]; swap.classList.toggle('is-spin'); fromWidget(); });
  $$('[data-pax]').forEach(b => b.addEventListener('click', () => { const n = Math.max(1, Math.min(9, +paxOut.textContent + +b.dataset.pax)); paxOut.textContent = n; window.PAUS?.setPax(n); }));
  document.addEventListener('paus:change', ({ detail: d }) => {
    syncing = true;
    from.value = 'Tallinn'; to.value = d.pause === 'paev' ? 'Helsingi' : 'Stockholm';
    if (d.day) date.value = `2026-12-${String(d.day).padStart(2, '0')}`;
    syncing = false;
  });
  f.addEventListener('submit', e => {
    e.preventDefault();
    const r = routePause();
    if (r.err) { msg.textContent = r.err; (from.value !== 'Tallinn' ? from : to).focus(); return; }
    if (!/^2026-12-\d\d$/.test(date.value)) { msg.textContent = 'Vali väljumise kuupäev detsembris — soodsamad päevad näed kalendrist allpool.'; date.focus(); return; }
    msg.textContent = '';
    window.PAUS.setPause(r.id); window.PAUS.setDay(+date.value.slice(8));
    $('.bar [data-book]').click(); // shared summary dialog
  });

  /* ---------- Club One ---------- */
  const club = $('[data-club-toggle]'), cal = $('[data-cal]');
  club?.addEventListener('change', () => {
    window.PAUS?.setClub(club.checked); cal.classList.toggle('is-club', club.checked);
    cal.classList.remove('is-flash'); void cal.offsetWidth; cal.classList.add('is-flash');
  });

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

  /* ---------- scroll progress + current section ---------- */
  const hdr = $('[data-hdr]');
  let tick = false;
  addEventListener('scroll', () => { if (tick) return; tick = true; requestAnimationFrame(() => {
    const h = document.documentElement; hdr.style.setProperty('--p', (h.scrollTop / Math.max(1, h.scrollHeight - innerHeight)).toFixed(4)); tick = false; }); }, { passive: true });
  const links = $$('.hdr__nav a');
  const io = new IntersectionObserver(es => es.forEach(en => { if (en.isIntersecting) links.forEach(a => a.classList.toggle('is-on', a.getAttribute('href') === '#' + en.target.id)); }), { rootMargin: '-45% 0px -50% 0px' });
  links.forEach(a => { const t = $(a.getAttribute('href')); if (t) io.observe(t); });
})();
