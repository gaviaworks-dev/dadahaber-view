/* R2-2 — VİDEO AKIŞI (reels)
   Kalıp kaynağı: dadagastro.com/video-mutfagi "Dada Akış" (#dakis)
   Playwright ile ölçülen davranış:
     overlay  : position:fixed; inset:0; z-index:120; overflow-y:auto;
                scroll-snap-type: y mandatory
     slayt    : her biri viewport yüksekliğinde, scroll-snap-align:center
     kapatma  : kapat butonu + ESC; açılışta body kaydırma kilitlenir
     sayaç    : "1 / 6" biçiminde, kaydırdıkça güncellenir
     segment  : üstte ilerleme çubukları, aktif olan dolu
   Kütüphane yok, native scroll-snap. */
(function () {
  var track = document.getElementById('dhShorts');
  var reels = document.getElementById('dhReels');
  if (!track || !reels) return;

  var scroller = document.getElementById('dhReelsScroll');
  var closeBtn = document.getElementById('dhReelsClose');
  var counter = document.getElementById('dhReelsCount');
  var cards = [].slice.call(track.querySelectorAll('[data-dh-short]'));
  var lastFocus = null;
  var built = false;

  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function build() {
    if (built) return;
    scroller.innerHTML = cards.map(function (c, i) {
      var segs = cards.map(function (_, j) { return '<i' + (j === i ? ' class="on"' : '') + '></i>'; }).join('');
      return '' +
        '<section class="dh-reel" data-index="' + i + '">' +
        '  <div class="dh-reel__stage">' +
        '    <div class="dh-reel__media" style="background-image:url(' + esc(c.dataset.poster) + ')"></div>' +
        '    <video class="dh-reel__video" loop muted playsinline preload="none" poster="' + esc(c.dataset.poster) + '">' +
        '      <source data-src="' + esc(c.dataset.video) + '" type="video/webm">' +
        '    </video>' +
        '    <div class="dh-reel__shade"></div>' +
        '    <div class="dh-reel__segs">' + segs + '</div>' +
        '    <span class="dh-reel__cat">' + esc(c.dataset.cat) + '</span>' +
        '    <button class="dh-reel__playbtn" type="button" aria-label="Oynat / Duraklat"><i class="fas fa-play" aria-hidden="true"></i></button>' +
        '    <div class="dh-reel__info">' +
        '      <h3>' + esc(c.dataset.title) + '</h3>' +
        '      <span class="dh-reel__views"><i class="fas fa-eye" aria-hidden="true"></i> ' + esc(c.dataset.views) + '</span>' +
        '    </div>' +
        '  </div>' +
        '  <div class="dh-reel__actions">' +
        '    <button class="dh-reel__act" type="button" aria-label="Beğen"><span class="ic"><i class="fas fa-heart" aria-hidden="true"></i></span></button>' +
        '    <button class="dh-reel__act" type="button" aria-label="Kaydet"><span class="ic"><i class="far fa-bookmark" aria-hidden="true"></i></span></button>' +
        '    <button class="dh-reel__act" type="button" aria-label="Paylaş"><span class="ic"><i class="fas fa-share-alt" aria-hidden="true"></i></span></button>' +
        '  </div>' +
        '</section>';
    }).join('');
    built = true;

    scroller.addEventListener('click', function (e) {
      var btn = e.target.closest('.dh-reel__playbtn');
      if (!btn) return;
      var v = btn.closest('.dh-reel').querySelector('video');
      if (!v) return;
      if (v.paused) { play(v); btn.classList.add('is-playing'); }
      else { v.pause(); btn.classList.remove('is-playing'); }
    });

    scroller.addEventListener('scroll', onScroll, { passive: true });
  }

  function play(v) {
    var s = v.querySelector('source[data-src]');
    if (s && !s.src) { s.src = s.dataset.src; v.load(); }
    var pr = v.play();
    if (pr && pr.catch) pr.catch(function () {});
  }

  function current() {
    var mid = scroller.scrollTop + scroller.clientHeight / 2;
    var reelsEls = scroller.children, best = 0, bestD = Infinity;
    for (var i = 0; i < reelsEls.length; i++) {
      var el = reelsEls[i], c = el.offsetTop + el.offsetHeight / 2, d = Math.abs(c - mid);
      if (d < bestD) { bestD = d; best = i; }
    }
    return best;
  }

  function onScroll() {
    var i = current();
    counter.textContent = (i + 1) + ' / ' + cards.length;
    [].forEach.call(scroller.children, function (el, j) {
      var v = el.querySelector('video');
      if (j === i) { el.classList.add('is-active'); }
      else { el.classList.remove('is-active'); if (v && !v.paused) v.pause(); }
      [].forEach.call(el.querySelectorAll('.dh-reel__segs i'), function (s, k) {
        s.classList.toggle('on', k === i);
      });
    });
  }

  function open(index) {
    build();
    lastFocus = document.activeElement;
    reels.hidden = false;
    document.documentElement.style.overflow = 'hidden';
    document.body.style.overflow = 'hidden';
    requestAnimationFrame(function () {
      reels.classList.add('is-open');
      var el = scroller.children[index];
      if (el) scroller.scrollTop = el.offsetTop;
      onScroll();
      closeBtn.focus();
    });
  }

  function close() {
    reels.classList.remove('is-open');
    [].forEach.call(scroller.querySelectorAll('video'), function (v) { v.pause(); });
    document.documentElement.style.overflow = '';
    document.body.style.overflow = '';
    window.setTimeout(function () { reels.hidden = true; }, 220);
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  cards.forEach(function (c, i) {
    c.addEventListener('click', function () { open(i); });
  });

  /* Ray oklarıyla yatay gezinme + uçlarda butonu pasifleştirme */
  var prev = document.querySelector('[data-dh-shorts-prev]');
  var next = document.querySelector('[data-dh-shorts-next]');
  function step(dir) {
    var card = cards[0];
    if (!card) return;
    var w = card.getBoundingClientRect().width + 18;
    track.scrollBy({ left: dir * w * 2, behavior: 'smooth' });
  }
  function syncNav() {
    if (!prev || !next) return;
    var max = track.scrollWidth - track.clientWidth;
    prev.disabled = track.scrollLeft <= 2;
    next.disabled = track.scrollLeft >= max - 2;
  }
  if (prev) prev.addEventListener('click', function () { step(-1); });
  if (next) next.addEventListener('click', function () { step(1); });
  track.addEventListener('scroll', syncNav, { passive: true });
  window.addEventListener('resize', syncNav);
  syncNav();

  closeBtn.addEventListener('click', close);

  reels.addEventListener('click', function (e) {
    if (e.target === reels || e.target === scroller) close();
  });

  document.addEventListener('keydown', function (e) {
    if (reels.hidden) return;
    if (e.key === 'Escape') { close(); return; }
    if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      var i = current() + (e.key === 'ArrowDown' ? 1 : -1);
      var el = scroller.children[Math.max(0, Math.min(cards.length - 1, i))];
      if (el) scroller.scrollTo({ top: el.offsetTop, behavior: 'smooth' });
    }
  });
})();
