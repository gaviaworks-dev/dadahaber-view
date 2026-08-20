/* Haber Dinle — kategori süzgeci + bülten seçimi.
   Kütüphane yok. Backend bağlanınca yalnız veri kaynağı değişir;
   süzgeç mantığı DOM üzerindeki data-* niteliklerinden okuyor. */
(function () {
  'use strict';

  var liste = document.getElementById('dinleListe');
  if (!liste) return;

  var baslik = document.getElementById('dinleBaslik');
  var sayac = document.getElementById('dinleSayac');
  var satirlar = [].slice.call(liste.querySelectorAll('[data-dinle-cat]'));
  var cipler = [].slice.call(document.querySelectorAll('[data-dinle-cat][class*="dh-catbar__chip"]'));
  var bultenler = [].slice.call(document.querySelectorAll('.dh-ep--btn[data-dinle-bulten]'));

  var BULTEN_AD = {};
  bultenler.forEach(function (b) {
    var t = b.querySelector('.dh-ep__title');
    BULTEN_AD[b.getAttribute('data-dinle-bulten')] = t ? t.textContent.trim() : '';
  });

  var secilenKat = '';      // '' = tümü
  var secilenBulten = '';   // '' = tümü

  function dakika(sn) { return Math.round(sn / 60); }

  function uygula() {
    var gorunen = 0, toplamSn = 0;

    satirlar.forEach(function (satir) {
      var kat = satir.getAttribute('data-dinle-cat') || '';
      var bul = satir.getAttribute('data-dinle-bulten') || '';
      var uyar = (!secilenKat || kat === secilenKat) &&
                 (!secilenBulten || bul === secilenBulten);
      satir.hidden = !uyar;
      if (uyar) {
        gorunen++;
        toplamSn += parseInt(satir.getAttribute('data-dinle-sn'), 10) || 0;
      }
    });

    /* Numaralar görünen sıraya göre yeniden yazılıyor —
       gizli satırlar listede boşluk bırakmasın. */
    var n = 0;
    satirlar.forEach(function (satir) {
      if (satir.hidden) return;
      n++;
      var num = satir.querySelector('.dh-ep__num');
      if (num) num.textContent = n;
    });

    if (baslik) {
      if (secilenBulten) baslik.textContent = BULTEN_AD[secilenBulten] || 'Sesli haberler';
      else if (secilenKat) {
        var cip = cipler.filter(function (c) { return c.getAttribute('data-dinle-cat') === secilenKat; })[0];
        baslik.textContent = (cip ? cip.textContent.trim() : '') + ' — sesli haberler';
      } else baslik.textContent = 'Bugünün sesli haberleri';
    }

    if (sayac) {
      sayac.textContent = gorunen
        ? gorunen + ' kayıt · ' + dakika(toplamSn) + ' dk'
        : 'Bu seçimde kayıt yok';
    }

    cipler.forEach(function (c) {
      var on = (c.getAttribute('data-dinle-cat') || '') === secilenKat;
      c.classList.toggle('is-on', on);
      if (on) c.setAttribute('aria-current', 'true');
      else c.removeAttribute('aria-current');
    });

    bultenler.forEach(function (b) {
      var on = b.getAttribute('data-dinle-bulten') === secilenBulten;
      b.classList.toggle('is-now', on);
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  }

  cipler.forEach(function (c) {
    c.addEventListener('click', function (e) {
      e.preventDefault();
      secilenKat = c.getAttribute('data-dinle-cat') || '';
      uygula();
    });
  });

  bultenler.forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.getAttribute('data-dinle-bulten');
      /* Aynı bültene tekrar basmak seçimi kaldırır. */
      secilenBulten = (secilenBulten === v) ? '' : v;
      uygula();
    });
  });

  uygula();
})();
