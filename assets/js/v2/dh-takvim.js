/* dh-takvim.js — ekonomik takvim süzgeci
   Ülke ve etki düzeyine göre kayıtları gizler/gösterir. Kayıt SİLİNMEZ,
   yalnız hidden alır: JS kapalıysa takvimin tamamı görünür kalır.
   Semantik radiogroup (sekme değil): görünen bölümü değil, o bölümün
   VERİSİNİ süzüyor — dh-tabs.js'teki aynı ayrım.
   Vanilla, ES5, yeni kütüphane yok. */
(function () {
  'use strict';

  var kok = document.querySelector('[data-dh-takvim]');
  var liste = document.querySelector('[data-dh-tk-liste]');
  if (!kok || !liste) return;

  var kayitlar = [].slice.call(liste.children);
  var sayac = kok.querySelector('[data-dh-tk-say]');
  var ulke = '';
  var onem = '';

  function uygula() {
    var n = 0;
    for (var i = 0; i < kayitlar.length; i++) {
      var k = kayitlar[i];
      var uy = (!ulke || k.getAttribute('data-ulke') === ulke) &&
               (!onem || k.getAttribute('data-onem') === onem);
      k.hidden = !uy;
      if (uy) n++;
    }
    if (sayac) sayac.textContent = String(n);
    bos(n === 0);
  }

  var bosKutu = null;
  function bos(goster) {
    if (goster && !bosKutu) {
      bosKutu = document.createElement('p');
      bosKutu.className = 'dh-tkfilt__bos';
      bosKutu.setAttribute('role', 'status');
      bosKutu.textContent = 'Bu süzgeçle eşleşen kayıt yok. Başka bir ülke ya da etki düzeyi seçin.';
      liste.parentNode.insertBefore(bosKutu, liste.nextSibling);
    } else if (!goster && bosKutu) {
      bosKutu.parentNode.removeChild(bosKutu);
      bosKutu = null;
    }
  }

  function grupKur(nitelik, ata) {
    var dugmeler = [].slice.call(kok.querySelectorAll('[' + nitelik + ']'));
    if (!dugmeler.length) return;

    function sec(b) {
      for (var i = 0; i < dugmeler.length; i++) {
        var acik = dugmeler[i] === b;
        dugmeler[i].setAttribute('aria-checked', acik ? 'true' : 'false');
        dugmeler[i].classList.toggle('is-on', acik);
        dugmeler[i].tabIndex = acik ? 0 : -1;
      }
      ata(b.getAttribute(nitelik) || '');
      uygula();
    }

    for (var i = 0; i < dugmeler.length; i++) {
      (function (b) { b.addEventListener('click', function () { sec(b); }); }(dugmeler[i]));
    }
    /* ok tuşlarıyla gezinme — dolaşan tabindex */
    dugmeler[0].parentNode.addEventListener('keydown', function (e) {
      var yon = (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1
              : (e.key === 'ArrowLeft' || e.key === 'ArrowUp') ? -1 : 0;
      if (!yon) return;
      e.preventDefault();
      var i = dugmeler.indexOf(document.activeElement);
      if (i < 0) i = 0;
      var h = dugmeler[(i + yon + dugmeler.length) % dugmeler.length];
      sec(h);
      h.focus();
    });
    sec(dugmeler[0]);
  }

  grupKur('data-dh-tk-ulke', function (v) { ulke = v; });
  grupKur('data-dh-tk-onem', function (v) { onem = v; });
  uygula();
})();
