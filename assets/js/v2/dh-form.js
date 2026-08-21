/* dh-form.js — Keşfet formlarının çalışan iskeleti
   Kullanan: kesfet.html#dadaya-sor · dada-dogrula.html#talep
   Yeni kütüphane yok, saf vanilla JS, ES5 sözdizimi.

   SÖZLEŞME:
     Form   : form[data-dh-form]           — data değeri gönderim etiketidir
     Alan   : .dh-kform__f içindeki input/select/textarea (required destekli)
     Hata   : alanın .dh-kform__f kabına .is-bad + aria-invalid
     Sonuç  : [data-dh-form-done] kutusu .is-on olur, odak oraya taşınır

   Backend YOK: prototipte gönderim yapılmaz, `submit` engellenir ve
   kullanıcıya ne olacağı yazılı olarak bildirilir. alert() KULLANILMAZ
   (R7'de sitedeki alert'ler bu yüzden temizlenmişti). Girilen veri hiçbir
   yere yazılmaz — localStorage dahil; KVKK kararı alınmadı.
*/
(function () {
  'use strict';

  var formlar = [].slice.call(document.querySelectorAll('[data-dh-form]'));
  if (!formlar.length) return;

  function kap(el) {
    return el.closest ? el.closest('.dh-kform__f') : null;
  }

  function temizle(el) {
    var k = kap(el);
    if (k) k.classList.remove('is-bad');
    el.removeAttribute('aria-invalid');
  }

  function isaretle(el) {
    var k = kap(el);
    if (k) k.classList.add('is-bad');
    el.setAttribute('aria-invalid', 'true');
  }

  for (var i = 0; i < formlar.length; i++) {
    (function (f) {
      var alanlar = [].slice.call(f.querySelectorAll('input, select, textarea'));
      var done = f.querySelector('[data-dh-form-done]');

      for (var j = 0; j < alanlar.length; j++) {
        (function (a) {
          a.addEventListener('input', function () { temizle(a); });
          a.addEventListener('change', function () { temizle(a); });
        }(alanlar[j]));
      }

      f.addEventListener('submit', function (e) {
        e.preventDefault();

        var ilkHata = null;
        for (var k = 0; k < alanlar.length; k++) {
          var a = alanlar[k];
          if (!a.required) { temizle(a); continue; }
          var bos = (a.type === 'checkbox') ? !a.checked : !String(a.value).trim();
          if (!bos && a.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(a.value)) bos = true;
          if (bos) { isaretle(a); if (!ilkHata) ilkHata = a; }
          else { temizle(a); }
        }

        if (ilkHata) {
          if (done) done.classList.remove('is-on');
          ilkHata.focus();
          return;
        }

        f.reset();
        if (done) {
          done.classList.add('is-on');
          done.setAttribute('tabindex', '-1');
          done.focus();
        }
      });
    }(formlar[i]));
  }
}());
