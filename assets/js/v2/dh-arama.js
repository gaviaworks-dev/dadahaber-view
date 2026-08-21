/* v2 — Global arama sekmeleri (Nihai Menü Haritası bölüm 7)
   Sonuçlar içerik türüne göre gruplanmış; sekme seçimi grupları gösterir/gizler.
   Prototip: gerçek sorgu yok, süzme yalnız görünür grup üzerinde. */
(function () {
  var sekmeler = document.querySelectorAll('[data-dh-ara-sekme]');
  var gruplar = document.querySelectorAll('[data-dh-ara-grup]');
  if (!sekmeler.length || !gruplar.length) return;

  function goster(k) {
    for (var i = 0; i < gruplar.length; i++) {
      var g = gruplar[i];
      var uygun = (k === 'tumu') || (g.getAttribute('data-dh-ara-grup') === k);
      g.hidden = !uygun;
    }
    for (var j = 0; j < sekmeler.length; j++) {
      var s = sekmeler[j];
      var secili = s.getAttribute('data-dh-ara-sekme') === k;
      s.classList.toggle('is-on', secili);
      s.setAttribute('aria-selected', secili ? 'true' : 'false');
    }
    var b = document.querySelector('[data-dh-ara-sayi]');
    if (b) {
      var t = document.querySelector('[data-dh-ara-sekme="' + k + '"] .dh-ara__n');
      b.textContent = t ? t.textContent : '';
    }
  }

  for (var i = 0; i < sekmeler.length; i++) {
    sekmeler[i].addEventListener('click', function () {
      goster(this.getAttribute('data-dh-ara-sekme'));
    });
  }

  /* Süzgeçleri temizle — seçimleri ilk seçeneğe döndürür */
  var temizle = document.querySelector('[data-dh-filt-temizle]');
  if (temizle) {
    temizle.addEventListener('click', function () {
      var sel = document.querySelectorAll('.dh-filt__sel');
      for (var n = 0; n < sel.length; n++) sel[n].selectedIndex = 0;
    });
  }

  /* URL'deki ?t= sekmesini uygula */
  var t = new URLSearchParams(location.search).get('t');
  goster(t && document.querySelector('[data-dh-ara-sekme="' + t + '"]') ? t : 'tumu');
})();
