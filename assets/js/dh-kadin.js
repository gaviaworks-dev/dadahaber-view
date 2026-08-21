/* dh-kadin.js — Kadın sayfasının alt kategori sekmeleri (R7-K2 B)
   Yeni kütüphane yok, saf vanilla JS.
   dh-astro.js / dh-gebelik.js ile AYNI sözleşme:
     Veri kaynağı : <script type="application/json" id="dh-kadin-data">
     Sekmeler     : .dh-catbar__chip[data-dh-kcat] (role="tab")
     Paneller     : .dh-kmod__panel[data-dh-kpanel] (role="tabpanel")
     Yönlendirme  : data-dh-kpanel="go" paneli, metni JSON'dan gelir
   Backend gelince YALNIZ JSON bloğu değişir; işaretleme aynı kalır. */
(function () {
  'use strict';

  var node = document.getElementById('dh-kadin-data');
  if (!node) return;

  var DATA;
  try { DATA = JSON.parse(node.textContent); } catch (e) { return; }

  var CATS = DATA.kategoriler || {};
  var KEYS = Object.keys(CATS);
  if (!KEYS.length) return;

  var chips = [].slice.call(document.querySelectorAll('[data-dh-kcat]'));
  var panels = [].slice.call(document.querySelectorAll('[data-dh-kpanel]'));
  if (!chips.length || !panels.length) return;

  var goPanel = document.querySelector('[data-dh-kpanel="go"]');
  var goAd = document.querySelector('[data-dh-kgo-ad]');
  var goTxt = document.querySelector('[data-dh-kgo-txt]');
  var goLink = document.querySelector('[data-dh-kgo-link]');

  var current = null;

  /* Şerit bir Swiper; aktif çip görünür alanın dışında kalabiliyor.
     Swiper varsa onun slideTo'su, yoksa native kaydırma kullanılır. */
  function reveal(chip) {
    var slide = chip.parentElement;
    var swEl = chip.closest('.swiper');
    if (swEl && swEl.swiper && slide) {
      var i = [].indexOf.call(slide.parentElement.children, slide);
      if (i >= 0) swEl.swiper.slideTo(i);
      return;
    }
    var box = chip.closest('.dh-catbar__swiper, .dh-mbox__filter');
    if (!box || box.scrollWidth <= box.clientWidth) return;
    box.scrollLeft = chip.offsetLeft - (box.clientWidth - chip.offsetWidth) / 2;
  }

  function show(key, opts) {
    var cat = CATS[key];
    if (!cat) return;
    opts = opts || {};
    current = key;

    var hedef = cat.panel || 'go';

    for (var i = 0; i < panels.length; i++) {
      var ac = panels[i].getAttribute('data-dh-kpanel') === hedef;
      panels[i].hidden = !ac;
    }

    /* Modülü olmayan kategori: sahte panel yok, tek satır yönlendirme.
       Ya kendi bölümüne ya da sayfadaki haber listesine götürür. */
    if (hedef === 'go' && goPanel) {
      if (goAd) goAd.textContent = cat.ad;
      if (goTxt) goTxt.textContent = cat.not || 'Bu alt kategorinin haberleri aşağıdaki listede.';
      if (goLink) {
        goLink.setAttribute('href', cat.git || DATA.liste || '#');
        goLink.innerHTML = '';
        goLink.appendChild(document.createTextNode(cat.gitAd || 'Haberlere in '));
        var ic = document.createElement('i');
        ic.className = 'fas fa-arrow-right';
        ic.setAttribute('aria-hidden', 'true');
        goLink.appendChild(ic);
      }
      goPanel.setAttribute('aria-labelledby', 'dh-kchip-' + key);
    }

    for (var j = 0; j < chips.length; j++) {
      var on = chips[j].getAttribute('data-dh-kcat') === key;
      chips[j].classList.toggle('is-on', on);
      chips[j].setAttribute('aria-selected', on ? 'true' : 'false');
      chips[j].setAttribute('tabindex', on ? '0' : '-1');
      if (on) {
        reveal(chips[j]);
        if (opts.focus) chips[j].focus();
      }
    }
  }

  function step(delta) {
    var i = KEYS.indexOf(current);
    if (i < 0) i = 0;
    show(KEYS[(i + delta + KEYS.length) % KEYS.length], { focus: true });
  }

  document.addEventListener('click', function (e) {
    if (!e.target.closest) return;

    var chip = e.target.closest('[data-dh-kcat]');
    if (chip) {
      e.preventDefault();
      show(chip.getAttribute('data-dh-kcat'));
      return;
    }

    /* "Tümü" özetindeki hücreler ilgili sekmeye geçirir */
    var cell = e.target.closest('[data-dh-kgo]');
    if (cell) {
      e.preventDefault();
      show(cell.getAttribute('data-dh-kgo'));
      var bar = document.querySelector('.dh-catbar');
      if (bar && bar.scrollIntoView) bar.scrollIntoView({ behavior: 'smooth', block: 'start' });
      return;
    }

    /* Sağlık kontrol listesi: yalnız bu oturumda, kayıt yok */
    var chk = e.target.closest('.dh-chk__it');
    if (chk) {
      chk.setAttribute('aria-pressed', chk.getAttribute('aria-pressed') === 'true' ? 'false' : 'true');
    }
  });

  /* Klavye: şerit içinde sol/sağ/Home/End */
  document.addEventListener('keydown', function (e) {
    if (!e.target.closest || !e.target.closest('[data-dh-kcat]')) return;
    if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
    else if (e.key === 'Home') { e.preventDefault(); show(KEYS[0], { focus: true }); }
    else if (e.key === 'End') { e.preventDefault(); show(KEYS[KEYS.length - 1], { focus: true }); }
  });

  show(DATA.aktif && CATS[DATA.aktif] ? DATA.aktif : KEYS[0]);
})();
