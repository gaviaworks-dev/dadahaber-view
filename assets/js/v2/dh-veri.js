/* dh-veri.js — Veri & Harita: hava durumu şehir seçici (v2 / veri-harita.html)
   Yeni kütüphane yok, saf vanilla JS. Grafik kütüphanesi de yok —
   sayfadaki bütün grafikler satır içi SVG'dir, bu dosya onlara dokunmaz.

   dh-astro.js / dh-kadin.js / dh-bakis.js ile AYNI sözleşme:
     Veri kaynağı : <script type="application/json" id="dh-hava-data">
     Seçici       : [data-dh-hava-picks] içine .dh-catbar__chip[data-dh-sehir]
                    üretilir; role="radio" (aynı sayfadaki veriyi değiştirir)
     Alanlar      : [data-dh-hava="<alan>"]
     Hücreler     : [data-dh-hava-cells]  -> .dh-panel / .dh-cell (mevcut bileşen)
     Tablo        : [data-dh-hava-rows]
   Backend gelince YALNIZ JSON bloğu değişir; işaretleme aynı kalır. */
(function () {
  'use strict';

  var node = document.getElementById('dh-hava-data');
  if (!node) return;

  var DATA;
  try { DATA = JSON.parse(node.textContent); } catch (e) { return; }

  var SEH = DATA.sehirler || {};
  var KEYS = Object.keys(SEH);
  if (!KEYS.length) return;

  var GUN = DATA.gunler || [];
  var IKON = DATA.ikon || {};

  var picks = document.querySelector('[data-dh-hava-picks]');
  var cells = document.querySelector('[data-dh-hava-cells]');
  var rows = document.querySelector('[data-dh-hava-rows]');
  var current = null;

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }

  function buildPicks() {
    if (!picks) return;
    picks.innerHTML = '';
    for (var i = 0; i < KEYS.length; i++) {
      var b = el('button', 'dh-catbar__chip', SEH[KEYS[i]].ad);
      b.type = 'button';
      b.setAttribute('role', 'radio');
      b.setAttribute('aria-checked', 'false');
      b.setAttribute('data-dh-sehir', KEYS[i]);
      b.setAttribute('tabindex', '-1');
      picks.appendChild(b);
    }
  }

  function render(key, opts) {
    var s = SEH[key];
    if (!s) return;
    opts = opts || {};
    current = key;

    var ad = document.querySelectorAll('[data-dh-hava="sehir"], [data-dh-hava="sehir2"]');
    for (var a = 0; a < ad.length; a++) ad[a].textContent = s.ad;

    /* --- .dh-panel hücreleri (sitenin mevcut günlük panel bileşeni) --- */
    if (cells) {
      cells.innerHTML = '';
      for (var i = 0; i < s.gunluk.length && i < GUN.length; i++) {
        var g = s.gunluk[i];
        var ik = IKON[g.d] || {};
        var c = el('div', 'dh-cell' + (i === 0 ? ' is-now' : ''));
        c.setAttribute('role', 'listitem');
        c.appendChild(el('span', 'dh-cell__label', GUN[i]));
        var ic = el('span', 'dh-cell__icon');
        var img = document.createElement('img');
        img.src = ik.src || './assets/images/weather.svg';
        img.alt = ik.ad || '';
        img.width = 30;
        img.loading = 'lazy';
        ic.appendChild(img);
        c.appendChild(ic);
        c.appendChild(el('span', 'dh-cell__value', g.yuksek + '°'));
        cells.appendChild(c);
      }
    }

    /* --- haftalık tablo --- */
    if (rows) {
      rows.innerHTML = '';
      for (var j = 0; j < s.gunluk.length && j < GUN.length; j++) {
        var d = s.gunluk[j];
        var ikon = IKON[d.d] || {};
        var tr = el('tr');
        var th = el('th', null, GUN[j]);
        th.setAttribute('scope', 'row');
        tr.appendChild(th);
        tr.appendChild(el('td', null, ikon.ad || '—'));
        tr.appendChild(el('td', 'dh-num', d.yuksek + '°C'));
        tr.appendChild(el('td', 'dh-num', d.dusuk + '°C'));
        tr.appendChild(el('td', 'dh-num', '%' + d.yagis));
        tr.appendChild(el('td', 'dh-num', d.ruzgar + ' km/sa'));
        rows.appendChild(tr);
      }
    }

    if (picks) {
      var chips = picks.querySelectorAll('[data-dh-sehir]');
      for (var k = 0; k < chips.length; k++) {
        var on = chips[k].getAttribute('data-dh-sehir') === key;
        chips[k].classList.toggle('is-on', on);
        chips[k].setAttribute('aria-checked', on ? 'true' : 'false');
        chips[k].setAttribute('tabindex', on ? '0' : '-1');
        if (on && opts.focus) chips[k].focus();
      }
    }
  }

  function step(delta) {
    var i = KEYS.indexOf(current);
    if (i < 0) i = 0;
    render(KEYS[(i + delta + KEYS.length) % KEYS.length], { focus: true });
  }

  document.addEventListener('click', function (e) {
    if (!e.target.closest) return;
    var chip = e.target.closest('[data-dh-sehir]');
    if (!chip) return;
    e.preventDefault();
    render(chip.getAttribute('data-dh-sehir'));
  });

  document.addEventListener('keydown', function (e) {
    if (!e.target.closest || !e.target.closest('[data-dh-sehir]')) return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); step(1); }
    else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); step(-1); }
    else if (e.key === 'Home') { e.preventDefault(); render(KEYS[0], { focus: true }); }
    else if (e.key === 'End') { e.preventDefault(); render(KEYS[KEYS.length - 1], { focus: true }); }
  });

  buildPicks();
  render(DATA.aktif && SEH[DATA.aktif] ? DATA.aktif : KEYS[0]);
})();
