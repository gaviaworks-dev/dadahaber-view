/* v2 — "Konuyu Takip Et"
   Prototip: seçim localStorage'da tutulur, backend yok. Buton durumu
   metin + aria-pressed ile bildirilir; yalnız renkle bildirilmez. */
(function () {
  var ANAHTAR = 'dh-takip';
  function oku() {
    try { return JSON.parse(localStorage.getItem(ANAHTAR) || '[]'); } catch (e) { return []; }
  }
  function yaz(l) {
    try { localStorage.setItem(ANAHTAR, JSON.stringify(l)); } catch (e) {}
  }
  function ciz(b, takipte) {
    var t = b.querySelector('[data-dh-takip-t]');
    if (t) t.textContent = takipte ? 'Takip Ediliyor' : 'Konuyu Takip Et';
    b.classList.toggle('is-on', takipte);
    b.setAttribute('aria-pressed', takipte ? 'true' : 'false');
    var i = b.querySelector('i');
    if (i) i.className = takipte ? 'fas fa-bell-slash' : 'fas fa-bell';
  }
  var dugmeler = document.querySelectorAll('[data-dh-takip]');
  for (var n = 0; n < dugmeler.length; n++) {
    (function (b) {
      var konu = b.getAttribute('data-dh-takip');
      ciz(b, oku().indexOf(konu) !== -1);
      b.addEventListener('click', function () {
        var l = oku(), i = l.indexOf(konu);
        if (i === -1) l.push(konu); else l.splice(i, 1);
        yaz(l);
        ciz(b, i === -1);
      });
    })(dugmeler[n]);
  }
})();
