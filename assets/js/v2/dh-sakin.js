/* dh-sakin.js — Sakin Akış tercihleri (v2 / sakin-akis.html · hesabim.html)
   Yeni kütüphane yok, saf vanilla JS.

   SÖZLEŞME
     Anahtar   : <input type="checkbox" data-dh-pref="<anahtar>">
     Saklama   : localStorage["dh.pref.<anahtar>"] = "1" | "0"
     Yayın     : window CustomEvent "dh:pref" { detail:{ key, on } }
     Etki      : [data-dh-hassas]   -> şiddet perdesi (siddet-gizle)
                 [data-dh-sakin-alert] / [data-dh-sakin-quiet] -> bildirim şeridi
                 [data-dh-sakin-state] -> durum satırı

   Tercih sunucuya gönderilmez; yalnız bu tarayıcıda durur.
   Bu dosya `data-dh-pref` anahtarlarının TEK sahibidir — dh-hesap.js
   aynı anahtarlara ikinci kez bağlanmaz, yalnız "dh:pref" olayını dinler. */
(function () {
  'use strict';

  var NS = 'dh.pref.';

  function read(key) {
    try { return localStorage.getItem(NS + key) === '1'; } catch (e) { return false; }
  }
  function write(key, on) {
    try { localStorage.setItem(NS + key, on ? '1' : '0'); } catch (e) { /* özel mod */ }
  }

  /* ---------- şiddet perdesi ---------- */
  function applySiddet(on) {
    var figs = document.querySelectorAll('[data-dh-hassas]');
    for (var i = 0; i < figs.length; i++) {
      var f = figs[i];
      var veil = f.querySelector('.dh-sakin__veil');
      f.classList.toggle('is-hidden', on);
      if (!on) f.classList.remove('is-shown');
      if (veil) veil.hidden = !on;
    }
  }

  /* ---------- son dakika şeridi ---------- */
  function applyBildirim(on) {
    var alert = document.querySelector('[data-dh-sakin-alert]');
    var quiet = document.querySelector('[data-dh-sakin-quiet]');
    if (alert) alert.hidden = on;
    if (quiet) quiet.hidden = !on;
  }

  /* ---------- durum satırı ---------- */
  function applyState() {
    var box = document.querySelector('[data-dh-sakin-state]');
    if (!box) return;
    var s = read('siddet-gizle');
    var b = read('bildirim-dur');
    var txt;
    if (s && b) txt = 'Şiddet görselleri gizli · Son dakika bildirimleri durduruldu';
    else if (s) txt = 'Şiddet görselleri gizli · Bildirimler açık';
    else if (b) txt = 'Görseller açık · Son dakika bildirimleri durduruldu';
    else txt = 'Her iki anahtar da kapalı.';
    box.textContent = txt;
  }

  function apply(key, on) {
    if (key === 'siddet-gizle') applySiddet(on);
    if (key === 'bildirim-dur') applyBildirim(on);
    applyState();
  }

  /* ---------- anahtarları bağla ---------- */
  var boxes = document.querySelectorAll('input[type="checkbox"][data-dh-pref]');
  for (var i = 0; i < boxes.length; i++) {
    (function (box) {
      var key = box.getAttribute('data-dh-pref');
      box.checked = read(key);
      box.addEventListener('change', function () {
        write(key, box.checked);
        /* aynı anahtar birden çok yerde olabilir (sayfa + hesap paneli) */
        var twins = document.querySelectorAll('input[data-dh-pref="' + key + '"]');
        for (var j = 0; j < twins.length; j++) {
          if (twins[j] !== box) twins[j].checked = box.checked;
        }
        apply(key, box.checked);
        window.dispatchEvent(new CustomEvent('dh:pref', {
          detail: { key: key, on: box.checked }
        }));
      });
      apply(key, box.checked);
    })(boxes[i]);
  }

  /* ---------- perdeye dokunma: yalnız o görseli aç ---------- */
  document.addEventListener('click', function (e) {
    if (!e.target.closest) return;
    var v = e.target.closest('.dh-sakin__veil');
    if (!v) return;
    e.preventDefault();
    var fig = v.closest('[data-dh-hassas]');
    if (!fig) return;
    fig.classList.remove('is-hidden');
    fig.classList.add('is-shown');
    v.hidden = true;
  });

  applyState();
})();
