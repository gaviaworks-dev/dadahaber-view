/* dh-gebelik.js — Gebelik haftası ekseni (hamilelik.html)
   Yeni kütüphane yok, saf vanilla JS. dh-astro.js ile aynı sözleşme:
   Veri kaynağı  : <script type="application/json" id="dh-gebelik-data">
   Güncellenen   : [data-dh-gebe="<alan>"] taşıyan her düğüm
   Seçici        : .dh-catbar__chip kalıbının hafta varyantı ([data-dh-week])
   Dönem sekmesi : .dh-sort kalıbı ([data-dh-tri])
   Backend gelince YALNIZ JSON bloğu değişir; işaretleme aynı kalır. */
(function () {
  'use strict';

  var node = document.getElementById('dh-gebelik-data');
  if (!node) return;

  var DATA;
  try { DATA = JSON.parse(node.textContent); } catch (e) { return; }

  var W = DATA.haftalar || {};
  var TODAY = String(DATA.bugun || 1);
  var ORDER = Object.keys(W).sort(function (a, b) { return (+a) - (+b); });
  if (!ORDER.length) return;

  var strip = document.querySelector('[data-dh-week-strip]');
  var current = null;

  var TRI = {
    '1': { ad: '1. Trimester', ara: '1 – 13. hafta' },
    '2': { ad: '2. Trimester', ara: '14 – 27. hafta' },
    '3': { ad: '3. Trimester', ara: '28 – 40. hafta' }
  };

  function setText(key, value) {
    var list = document.querySelectorAll('[data-dh-gebe="' + key + '"]');
    for (var i = 0; i < list.length; i++) list[i].textContent = value;
  }

  function paras(host, arr) {
    if (!host) return;
    host.innerHTML = '';
    for (var i = 0; i < arr.length; i++) {
      var p = document.createElement('p');
      p.textContent = arr[i];
      host.appendChild(p);
    }
  }

  function scrollChipIntoView(chip) {
    if (!strip || strip.scrollWidth <= strip.clientWidth) return;
    var left = chip.offsetLeft - (strip.clientWidth - chip.offsetWidth) / 2;
    if (typeof strip.scrollTo === 'function') strip.scrollTo({ left: left, behavior: 'smooth' });
    else strip.scrollLeft = left;
  }

  function render(key, opts) {
    key = String(key);
    var h = W[key];
    if (!h) return;
    current = key;
    opts = opts || {};

    var t = String(h.t);
    setText('hafta', key);
    setText('kicker', key === TODAY ? 'BU HAFTADASINIZ' : 'SEÇİLİ HAFTA');
    setText('baslik', key + '. Hafta');
    setText('tri', TRI[t] ? TRI[t].ad + ' · ' + TRI[t].ara : '');
    setText('boy', h.boy);
    setText('agirlik', h.agirlik);
    setText('kiyas', h.kiyas);
    setText('kalan', (40 - (+key)) + ' hafta');
    setText('ozet', h.ozet);

    paras(document.querySelector('[data-dh-gebe="bebek"]'), h.bebek || []);
    paras(document.querySelector('[data-dh-gebe="anne"]'), h.anne || []);
    paras(document.querySelector('[data-dh-gebe="dikkat"]'), h.dikkat || []);

    if (strip) {
      var chips = strip.querySelectorAll('[data-dh-week]');
      for (var j = 0; j < chips.length; j++) {
        var on = chips[j].getAttribute('data-dh-week') === key;
        chips[j].classList.toggle('is-on', on);
        chips[j].setAttribute('aria-selected', on ? 'true' : 'false');
        chips[j].setAttribute('tabindex', on ? '0' : '-1');
        if (on && !opts.silent) scrollChipIntoView(chips[j]);
      }
    }

    if (!opts.silent && history.replaceState) {
      history.replaceState(null, '', '#hafta-' + key);
    }
  }

  var filterMode = 'hepsi';

  function markTabs() {
    var tabs = document.querySelectorAll('[data-dh-tri]');
    for (var k = 0; k < tabs.length; k++) {
      var sel = tabs[k].getAttribute('data-dh-tri') === filterMode;
      tabs[k].classList.toggle('is-on', sel);
      tabs[k].setAttribute('aria-selected', sel ? 'true' : 'false');
    }
  }

  function applyFilter(mode) {
    filterMode = mode;
    markTabs();
    if (!strip) return;
    var chips = strip.querySelectorAll('[data-dh-week]');
    for (var i = 0; i < chips.length; i++) {
      var t = chips[i].getAttribute('data-dh-week-tri');
      var show = (mode === 'hepsi') || (t === mode);
      chips[i].hidden = !show;
    }
    var bands = document.querySelectorAll('[data-dh-band]');
    for (var b = 0; b < bands.length; b++) {
      bands[b].hidden = !(mode === 'hepsi' || bands[b].getAttribute('data-dh-band') === mode);
    }
    var note = document.querySelector('[data-dh-gebe="filtre"]');
    if (note) {
      note.textContent = mode === 'hepsi'
        ? '40 haftanın tamamı gösteriliyor.'
        : (TRI[mode] ? TRI[mode].ad + ' gösteriliyor — ' + TRI[mode].ara + '.' : '');
    }
    // Seçili hafta filtrenin dışında kaldıysa dönemin ilk haftasına geç
    if (mode !== 'hepsi' && W[current] && String(W[current].t) !== mode) {
      for (var j = 0; j < ORDER.length; j++) {
        if (String(W[ORDER[j]].t) === mode) { render(ORDER[j]); return; }
      }
    }
    render(current, { silent: true });
  }

  function step(delta) {
    var i = ORDER.indexOf(current);
    if (i < 0) i = 0;
    var n = i;
    // filtre açıkken yalnız görünür haftalar arasında dolaş
    for (var guard = 0; guard < ORDER.length; guard++) {
      n = (n + delta + ORDER.length) % ORDER.length;
      if (filterMode === 'hepsi' || String(W[ORDER[n]].t) === filterMode) break;
    }
    render(ORDER[n]);
    var chip = strip && strip.querySelector('[data-dh-week="' + ORDER[n] + '"]');
    if (chip) chip.focus();
  }

  document.addEventListener('click', function (e) {
    if (!e.target.closest) return;
    var chip = e.target.closest('[data-dh-week]');
    if (chip) { e.preventDefault(); render(chip.getAttribute('data-dh-week')); return; }
    var tab = e.target.closest('[data-dh-tri]');
    if (tab) { e.preventDefault(); applyFilter(tab.getAttribute('data-dh-tri')); return; }
    if (e.target.closest('[data-dh-week-prev]')) { e.preventDefault(); step(-1); return; }
    if (e.target.closest('[data-dh-week-next]')) { e.preventDefault(); step(1); return; }
    if (e.target.closest('[data-dh-week-today]')) { e.preventDefault(); applyFilter('hepsi'); render(TODAY); }
  });

  if (strip) {
    strip.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); step(1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
      else if (e.key === 'Home') { e.preventDefault(); render(ORDER[0]); }
      else if (e.key === 'End') { e.preventDefault(); render(ORDER[ORDER.length - 1]); }
    });
  }

  // Hesaplayıcıdan gelen "bu haftayı eksende göster" isteği
  document.addEventListener('dh-gebelik-goto', function (e) {
    var n = e && e.detail && e.detail.week;
    if (!n || !W[String(n)]) return;
    applyFilter('hepsi');
    render(String(n));
    var top = document.getElementById('hafta');
    if (top) top.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  var fromHash = (location.hash.match(/^#hafta-(\d+)$/) || [])[1];
  render(fromHash && W[fromHash] ? fromHash : TODAY, { silent: true });
})();
