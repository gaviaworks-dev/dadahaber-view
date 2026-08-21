/* dh-hesap.js — Hesabım: bölüm sekmeleri + çapa yönlendirme + Sessiz Saatler
   (v2 / hesabim.html).  DİKKAT: assets/js/dh-hesap.js BAŞKA bir dosyadır
   (DadaDiet hesaplayıcısı); bu dosya onunla ilgisizdir.

   Yeni kütüphane yok, saf vanilla JS.

   SÖZLEŞME
     Sekmeler : [role="tablist"] içinde .dh-hsp__tab[data-dh-tab="<id>"]
     Paneller : [role="tabpanel"] id="<id>"  ->  hesabim.html#<id> çalışır
                (#sehirlerim #kaydedilenler #bildirimler #bultenler #uygulama
                 kabuk tarafından kullanılıyor, id'ler sabittir)
     Saat     : <select data-dh-pref-time="<anahtar>">
                -> localStorage["dh.pref.<anahtar>"]

   `data-dh-pref` ANAHTARLARINA BU DOSYA BAĞLANMAZ — onların tek sahibi
   dh-sakin.js'tir. Buradan yalnız "dh:pref" olayı dinlenir. */
(function () {
  'use strict';

  var NS = 'dh.pref.';
  var list = document.querySelector('.dh-hsp__nav[role="tablist"]');
  if (!list) return;

  var tabs = [].slice.call(list.querySelectorAll('[data-dh-tab]'));
  if (!tabs.length) return;

  function panelOf(tab) {
    return document.getElementById(tab.getAttribute('data-dh-tab'));
  }

  function show(id, opts) {
    opts = opts || {};
    var found = false;
    for (var i = 0; i < tabs.length; i++) {
      var t = tabs[i];
      var p = panelOf(t);
      var on = t.getAttribute('data-dh-tab') === id;
      if (on) found = true;
      t.classList.toggle('is-on', on);
      t.setAttribute('aria-selected', on ? 'true' : 'false');
      t.setAttribute('tabindex', on ? '0' : '-1');
      if (p) p.hidden = !on;
      if (on && opts.focus) t.focus();
    }
    if (!found) return false;
    if (opts.hash !== false && window.history && window.history.replaceState) {
      try { window.history.replaceState(null, '', '#' + id); } catch (e) { /* file:// */ }
    }
    return true;
  }

  function step(delta) {
    /* Odak seritte ise ondan, degilse secili sekmeden ilerle. */
    var i = tabs.indexOf(document.activeElement);
    if (i < 0) {
      i = 0;
      for (var k = 0; k < tabs.length; k++) {
        if (tabs[k].getAttribute('aria-selected') === 'true') { i = k; break; }
      }
    }
    var n = tabs[(i + delta + tabs.length) % tabs.length];
    show(n.getAttribute('data-dh-tab'), { focus: true });
  }

  list.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-dh-tab]') : null;
    if (!t) return;
    e.preventDefault();
    show(t.getAttribute('data-dh-tab'));
  });

  list.addEventListener('keydown', function (e) {
    if (!e.target.closest || !e.target.closest('[data-dh-tab]')) return;
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') { e.preventDefault(); step(1); }
    else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') { e.preventDefault(); step(-1); }
    else if (e.key === 'Home') { e.preventDefault(); show(tabs[0].getAttribute('data-dh-tab'), { focus: true }); }
    else if (e.key === 'End') { e.preventDefault(); show(tabs[tabs.length - 1].getAttribute('data-dh-tab'), { focus: true }); }
  });

  /* Çapa yönlendirme: kabuk hesabim.html#bildirimler gibi bağlantılar veriyor.
     Panel gizliyken tarayıcı kaydıramaz; sekmeyi biz açıyoruz. */
  function fromHash(scroll) {
    var id = (location.hash || '').replace('#', '');
    if (!id) return false;
    var ok = show(id, { hash: false });
    if (ok && scroll) {
      var box = document.querySelector('.dh-hsp');
      if (box && box.scrollIntoView) box.scrollIntoView({ block: 'start' });
    }
    return ok;
  }

  window.addEventListener('hashchange', function () { fromHash(true); });

  /* --- Sessiz Saatler ---------------------------------------------------- */
  var times = [].slice.call(document.querySelectorAll('[data-dh-pref-time]'));
  var out = document.querySelector('[data-dh-sessiz-out]');

  function readT(key, fb) {
    try { return localStorage.getItem(NS + key) || fb; } catch (e) { return fb; }
  }

  function renderOut() {
    if (!out) return;
    var on = document.querySelector('input[data-dh-pref="bild-sessiz"]');
    var b = readT('sessiz-bas', '23:00');
    var s = readT('sessiz-bit', '07:00');
    out.textContent = (on && on.checked) ? (b + ' — ' + s + ' arası sessiz') : 'Kapalı';
  }

  for (var i = 0; i < times.length; i++) {
    (function (sel) {
      var key = sel.getAttribute('data-dh-pref-time');
      var v = readT(key, key === 'sessiz-bas' ? '23:00' : '07:00');
      sel.value = v;
      if (sel.value !== v) sel.value = v;  // seçenek yoksa geri düş
      sel.addEventListener('change', function () {
        try { localStorage.setItem(NS + key, sel.value); } catch (e) { /* özel mod */ }
        renderOut();
      });
    })(times[i]);
  }

  window.addEventListener('dh:pref', renderOut);
  renderOut();

  /* --- açılış ------------------------------------------------------------ */
  /* Derin bağlantıyla gelindiyse (hesabim.html#bildirimler) panele kaydır;
     bölüm mobilde sayfanın çok altında kalıyor. */
  if (!fromHash(true)) show(tabs[0].getAttribute('data-dh-tab'), { hash: false });
})();
