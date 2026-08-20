/* dh-astro.js — Günlük burç modülü (kadin.html · astroloji.html)
   Yeni kütüphane yok, saf vanilla JS.
   Veri kaynağı: <script type="application/json" id="dh-astro-data">
   Sözleşme: [data-dh-astro="<alan>"] taşıyan her düğüm seçili burca göre
   güncellenir. Çipler .dh-catbar__chip kalıbını kullanır; .is-on = okunan
   burç, .is-now = bugün sezonda olan burç (dh-cell ailesindeki aynı imza). */
(function () {
  'use strict';

  var node = document.getElementById('dh-astro-data');
  if (!node) return;

  var DATA;
  try {
    DATA = JSON.parse(node.textContent);
  } catch (e) {
    return;
  }
  var SIGNS = DATA.signs || {};
  var SEASON = DATA.season;
  var ORDER = Object.keys(SIGNS);
  var VS = '︎';

  var strip = document.querySelector('[data-dh-astro-signs]');
  var period = 'gunluk';
  var current = null;

  function setText(key, value) {
    var list = document.querySelectorAll('[data-dh-astro="' + key + '"]');
    for (var i = 0; i < list.length; i++) list[i].textContent = value;
  }

  function render(key) {
    var s = SIGNS[key];
    if (!s) return;
    current = key;

    setText('kicker', key === SEASON ? 'BUGÜNÜN BURCU' : 'GÜNÜN YORUMU');
    setText('glyph', s.g + VS);
    setText('ad', s.ad);
    setText('tarih', s.tarih + ' · ' + s.element + ' · ' + s.yonetici);
    setText('ask', s.ask);
    setText('kariyer', s.kariyer);
    setText('saglik', s.saglik);
    setText('sayi', s.sayi);
    setText('renk', s.renk);
    setText('uyum', s.uyum);
    setText('ozet', s.ozet);
    setText('f-ask', s.facets[0]);
    setText('f-kariyer', s.facets[1]);
    setText('f-saglik', s.facets[2]);

    var body = document.querySelector('[data-dh-astro="metin"]');
    if (body) {
      var paras = s[period] || s.gunluk || [];
      body.innerHTML = '';
      for (var i = 0; i < paras.length; i++) {
        var p = document.createElement('p');
        p.textContent = paras[i];
        body.appendChild(p);
      }
    }

    if (strip) {
      var chips = strip.querySelectorAll('[data-dh-sign]');
      for (var j = 0; j < chips.length; j++) {
        var on = chips[j].getAttribute('data-dh-sign') === key;
        chips[j].classList.toggle('is-on', on);
        chips[j].setAttribute('aria-selected', on ? 'true' : 'false');
        if (on) scrollChipIntoView(chips[j]);
      }
    }

    // Sayfadaki burç kartlarında da aynı seçim işaretlensin (astroloji.html)
    var cards = document.querySelectorAll('[data-dh-card]');
    for (var k = 0; k < cards.length; k++) {
      cards[k].classList.toggle('is-on', cards[k].getAttribute('data-dh-card') === key);
    }
  }

  function scrollChipIntoView(chip) {
    if (!strip || strip.scrollWidth <= strip.clientWidth) return;
    var left = chip.offsetLeft - (strip.clientWidth - chip.offsetWidth) / 2;
    if (typeof strip.scrollTo === 'function') {
      strip.scrollTo({ left: left, behavior: 'smooth' });
    } else {
      strip.scrollLeft = left;
    }
  }

  function step(delta) {
    var i = ORDER.indexOf(current);
    if (i < 0) i = 0;
    render(ORDER[(i + delta + ORDER.length) % ORDER.length]);
  }

  document.addEventListener('click', function (e) {
    var chip = e.target.closest ? e.target.closest('[data-dh-sign]') : null;
    if (chip) {
      e.preventDefault();
      render(chip.getAttribute('data-dh-sign'));
      return;
    }
    var card = e.target.closest ? e.target.closest('[data-dh-card]') : null;
    if (card) {
      e.preventDefault();
      render(card.getAttribute('data-dh-card'));
      var top = document.getElementById('astroloji');
      if (top) top.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }
    var tab = e.target.closest ? e.target.closest('[data-dh-period]') : null;
    if (tab) {
      period = tab.getAttribute('data-dh-period');
      render(current);
      return;
    }
    if (e.target.closest && e.target.closest('[data-dh-astro-prev]')) { step(-1); return; }
    if (e.target.closest && e.target.closest('[data-dh-astro-next]')) { step(1); }
  });

  // Klavye: şeritte sol/sağ ok ile burçlar arasında gezinme
  if (strip) {
    strip.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
    });
  }

  var start = (strip && strip.querySelector('.is-on'))
    ? strip.querySelector('.is-on').getAttribute('data-dh-sign')
    : ORDER[0];
  render(start);
})();
