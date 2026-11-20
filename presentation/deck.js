/* Minimal, dependency-free slide engine with fragments, step classes,
   speaker notes, presenter window, and hash navigation.

   Keys:  → / Space / PgDn / Enter : next step     ← / PgUp / Backspace : previous
          Shift+→ / Shift+← : next / previous slide (skip fragments)
          Home / End : first / last       <number> + Enter : go to slide
          F : fullscreen   N : notes overlay   S : presenter window   T : reset timer
          B / . : blank screen   O : slide index
*/
(function () {
  const W = 1600, H = 900;
  const deck = document.querySelector('.deck');
  const slides = Array.from(document.querySelectorAll('.slide'));
  const isPresenter = new URLSearchParams(location.search).has('presenter');
  const chan = ('BroadcastChannel' in window) ? new BroadcastChannel('msc-deck') : null;

  let cur = 0, step = 0, typed = '';
  const PT = (document.documentElement.lang || '').startsWith('pt');
  const L = PT ? { untitled: '(sem título)', end: '— fim —', step: 'passo', more: 'próximo: mais neste slide', nexts: 'próximo slide: ', notes: '(sem notas)', target: 'meta ≈ ', plan: 'tempo planejado ao fim deste slide ≈ ' }
               : { untitled: '(untitled)', end: '— end —', step: 'step', more: 'next: more on this slide', nexts: 'next slide: ', notes: '(no notes)', target: 'target ≈ ', plan: 'planned elapsed at end of this slide ≈ ' };
  let startTime = null;

  // ---- fragments ---------------------------------------------------------
  slides.forEach((s, i) => {
    s.dataset.index = i + 1;
    const frags = Array.from(s.querySelectorAll('.f'));
    // explicit order via data-f, otherwise DOM order; equal data-f = shown together
    let auto = 0;
    frags.forEach(f => {
      if (f.dataset.f === undefined) { auto += 1; f.dataset.f = auto; }
      else { auto = Math.max(auto, +f.dataset.f); }
    });
    s._frags = frags;
    s._steps = frags.reduce((m, f) => Math.max(m, +f.dataset.f), 0);
    const pn = document.createElement('div');
    pn.className = 'pagenum';
    pn.textContent = (i + 1);
    if (!s.classList.contains('nochrome')) s.appendChild(pn);
  });

  function sectionOf(i) {
    for (let k = i; k >= 0; k--) if (slides[k].dataset.section) return slides[k].dataset.section;
    return '';
  }

  // ---- scaling -----------------------------------------------------------
  function fit() {
    if (isPresenter) return;
    const sc = Math.min(window.innerWidth / W, window.innerHeight / H);
    deck.style.transform = `translate(-50%,-50%) scale(${sc})`;
  }
  window.addEventListener('resize', fit);

  // ---- render ------------------------------------------------------------
  const bar = document.querySelector('.progress > i');
  const sect = document.querySelector('.sectionlabel');
  if (sect) {
    const names = [];
    slides.forEach(s => { const n = s.dataset.section; if (n && !names.includes(n)) names.push(n); });
    sect.innerHTML = names.map(n => `<span>${n}</span>`).join('');
  }
  const notesBox = document.querySelector('.notes-overlay');

  function apply(dir) {
    slides.forEach((s, i) => {
      s.classList.toggle('active', i === cur);
      s.classList.toggle('past', i < cur);
      s.classList.toggle('future', i > cur);
    });
    const s = slides[cur];
    s._frags.forEach(f => f.classList.toggle('on', +f.dataset.f <= step));
    // step-N classes for transient highlights
    s.className = s.className.replace(/\bstep-\d+\b/g, '').trim();
    s.classList.add('step-' + step);
    if (s.dataset.anim && window.DeckAnims && window.DeckAnims[s.dataset.anim]) {
      window.DeckAnims[s.dataset.anim](s, step, dir);
    }
    if (bar) bar.style.width = (100 * cur / (slides.length - 1)) + '%';
    deck.classList.toggle('on-nochrome', s.classList.contains('nochrome'));
    if (sect) {
      const name = sectionOf(cur);
      sect.style.visibility = s.classList.contains('nochrome') ? 'hidden' : 'visible';
      sect.querySelectorAll('span').forEach(sp => sp.classList.toggle('cur', sp.textContent === name));
    }
    if (notesBox) {
      const n = s.querySelector('aside.notes');
      notesBox.innerHTML = n ? n.innerHTML : `<em>${L.notes}</em>`;
    }
    if (!isPresenter) history.replaceState(null, '', '#/' + (cur + 1) + (step ? '/' + step : ''));
    broadcast();
  }

  function go(i, st, dir) {
    i = Math.max(0, Math.min(slides.length - 1, i));
    const changed = i !== cur;
    cur = i;
    step = st === 'end' ? slides[i]._steps : (st || 0);
    if (changed) restartAnims(slides[cur]);
    apply(dir || 0);
  }
  function restartAnims(s) {
    // re-trigger CSS animations marked .replay when entering a slide
    s.querySelectorAll('.replay').forEach(el => {
      el.classList.remove('replay'); void el.offsetWidth; el.classList.add('replay');
    });
  }
  function next() {
    if (!startTime) startTime = Date.now();
    if (step < slides[cur]._steps) { step++; apply(1); }
    else if (cur < slides.length - 1) go(cur + 1, 0, 1);
  }
  function prev() {
    if (step > 0) { step--; apply(-1); }
    else if (cur > 0) go(cur - 1, 'end', -1);
  }

  // ---- presenter sync ------------------------------------------------------
  function broadcast() {
    if (!chan || isPresenter) return;
    chan.postMessage({ cur, step, startTime });
  }
  if (chan) chan.onmessage = (e) => {
    const d = e.data;
    if (d.cmd && !isPresenter) {
      if (d.cmd === 'next') next(); else if (d.cmd === 'prev') prev();
      else if (d.cmd === 'hello') broadcast();
      else if (d.cmd === 'reset') { startTime = Date.now(); broadcast(); }
      return;
    }
    if (isPresenter && d.cur !== undefined) { startTime = d.startTime; renderPresenter(d.cur, d.step); }
  };

  function renderPresenter(c, st) {
    const s = slides[c];
    const nx = slides[c + 1];
    const title = el => el ? (el.querySelector('h1,h2')?.textContent || L.untitled) : L.end;
    document.getElementById('p-cur').textContent = `${c + 1} / ${slides.length} — ${title(s)}`;
    document.getElementById('p-step').textContent = `${L.step} ${st} / ${s._steps}`;
    document.getElementById('p-next').textContent = st < s._steps ? L.more : L.nexts + title(nx);
    const n = s.querySelector('aside.notes');
    document.getElementById('p-notes').innerHTML = n ? n.innerHTML : `<em>${L.notes}</em>`;
    document.getElementById('p-target').textContent = s.dataset.time ? `${L.target}${s.dataset.time} s` : '';
    // cumulative planned time
    let planned = 0;
    for (let k = 0; k <= c; k++) planned += parseFloat(slides[k].dataset.time || 0);
    document.getElementById('p-plan').textContent = `${L.plan}${Math.floor(planned / 60)}:${String(Math.round(planned % 60)).padStart(2, '0')}`;
  }

  if (isPresenter) {
    document.body.classList.add('presenter');
    setInterval(() => {
      const el = document.getElementById('p-clock');
      if (!startTime) { el.textContent = '00:00'; return; }
      const t = Math.floor((Date.now() - startTime) / 1000);
      el.textContent = `${String(Math.floor(t / 60)).padStart(2, '0')}:${String(t % 60).padStart(2, '0')}`;
    }, 500);
    document.addEventListener('keydown', e => {
      if (['ArrowRight', ' ', 'PageDown', 'Enter'].includes(e.key)) chan.postMessage({ cmd: 'next' });
      if (['ArrowLeft', 'PageUp', 'Backspace'].includes(e.key)) chan.postMessage({ cmd: 'prev' });
      if (e.key === 't' || e.key === 'T') chan.postMessage({ cmd: 'reset' });
    });
    chan && chan.postMessage({ cmd: 'hello' });
    return;
  }

  // ---- index overlay ----------------------------------------------------
  const idx = document.querySelector('.index-overlay');
  if (idx) {
    idx.innerHTML = slides.map((s, i) => {
      const t = s.querySelector('h1,h2')?.textContent || '';
      const sec = s.dataset.section ? `<b>${s.dataset.section}</b>` : '';
      return `<a data-i="${i}">${sec}<span>${i + 1}. ${t}</span></a>`;
    }).join('');
    idx.addEventListener('click', e => {
      const a = e.target.closest('a'); if (!a) return;
      idx.classList.remove('show'); go(+a.dataset.i, 0);
    });
  }

  // ---- input -------------------------------------------------------------
  document.addEventListener('keydown', e => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key;
    if (/^\d$/.test(k)) { typed += k; return; }
    if (k === 'Enter' && typed) { go(parseInt(typed, 10) - 1, 0); typed = ''; return; }
    typed = '';
    if (e.shiftKey && k === 'ArrowRight') { go(cur + 1, 0, 1); return; }
    if (e.shiftKey && k === 'ArrowLeft') { go(cur - 1, 0, -1); return; }
    if (['ArrowRight', 'ArrowDown', ' ', 'PageDown', 'Enter'].includes(k)) { e.preventDefault(); next(); }
    else if (['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'].includes(k)) { e.preventDefault(); prev(); }
    else if (k === 'Home') go(0, 0);
    else if (k === 'End') go(slides.length - 1, 0);
    else if (k === 'f' || k === 'F') {
      if (!document.fullscreenElement) document.documentElement.requestFullscreen(); else document.exitFullscreen();
    }
    else if (k === 'n' || k === 'N') document.body.classList.toggle('show-notes');
    else if (k === 'b' || k === 'B' || k === '.') document.body.classList.toggle('blank');
    else if (k === 'o' || k === 'O' || k === 'Escape') idx && idx.classList.toggle('show', k !== 'Escape' ? undefined : false);
    else if (k === 's' || k === 'S') window.open(location.pathname + '?presenter', 'presenter', 'width=1100,height=750');
    else if (k === 't' || k === 'T') { startTime = Date.now(); broadcast(); }
  });
  document.addEventListener('click', e => {
    if (e.target.closest('a,button,.index-overlay')) return;
    if (e.clientX > window.innerWidth * 0.25) next(); else prev();
  });

  // ---- start -------------------------------------------------------------
  window.deckGo = (n, st) => go(n - 1, st === undefined ? 'end' : st);
  fit();
  const m = location.hash.match(/#\/(\d+)(?:\/(\d+))?/);
  go(m ? +m[1] - 1 : 0, m && m[2] ? +m[2] : 0);
  restartAnims(slides[cur]);
})();
