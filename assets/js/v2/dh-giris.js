/* dh-giris.js — giriş · üye ol · şifremi unuttum formlarının çalışan iskeleti
   Görsel sözleşme dh-form.js ile aynı (.dh-kform__f.is-bad, .dh-kform__err,
   [data-dh-form-done].is-on) ama doğrulama kuralları farklı olduğu için ayrı
   dosya: şifre uzunluğu, şifre tekrarı ve onay kutuları burada denetlenir.

   Backend YOK. Prototipte gönderim yapılmaz, hiçbir veri hiçbir yere yazılmaz
   — localStorage dahil. alert() kullanılmaz. */
(function () {
  'use strict';

  var formlar = [].slice.call(document.querySelectorAll('[data-dh-auth]'));

  function kap(el) { return el.closest ? el.closest('.dh-kform__f') : null; }
  function temizle(el) {
    var k = kap(el);
    if (k) k.classList.remove('is-bad');
    el.removeAttribute('aria-invalid');
  }
  function isaretle(el, mesaj) {
    var k = kap(el);
    if (k) {
      k.classList.add('is-bad');
      if (mesaj) {
        var e = k.querySelector('.dh-kform__err');
        if (e) e.textContent = mesaj;
      }
    }
    el.setAttribute('aria-invalid', 'true');
  }
  var EPOSTA = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  /* --------------------------------------------------- şifre göster/gizle */
  var gozler = document.querySelectorAll('.dh-auth__eye');
  Array.prototype.forEach.call(gozler, function (d) {
    d.addEventListener('click', function () {
      var alan = d.parentNode.querySelector('input');
      if (!alan) return;
      var gizli = alan.type === 'password';
      alan.type = gizli ? 'text' : 'password';
      d.setAttribute('aria-label', gizli ? 'Şifreyi gizle' : 'Şifreyi göster');
      d.setAttribute('aria-pressed', String(gizli));
      var ik = d.querySelector('i');
      if (ik) ik.className = gizli ? 'fas fa-eye-slash' : 'fas fa-eye';
    });
  });

  /* ------------------------------------------------------- şifre gücü */
  function guc(s) {
    var p = 0;
    if (s.length >= 8) p++;
    if (s.length >= 12) p++;
    if (/[a-zçğıöşü]/.test(s) && /[A-ZÇĞİÖŞÜ]/.test(s)) p++;
    if (/\d/.test(s) && /[^\wçğıöşüÇĞİÖŞÜ]/.test(s)) p++;
    return Math.min(p, 4);
  }
  var ETIKET = ['ŞİFRE GÜCÜ', 'ZAYIF', 'ORTA', 'İYİ', 'GÜÇLÜ'];
  var olcerler = document.querySelectorAll('[data-dh-pwm]');
  Array.prototype.forEach.call(olcerler, function (m) {
    var alan = document.getElementById(m.getAttribute('data-dh-pwm'));
    var etiket = m.querySelector('.dh-auth__pwl');
    if (!alan) return;
    alan.addEventListener('input', function () {
      var g = alan.value ? Math.max(1, guc(alan.value)) : 0;
      m.setAttribute('data-guc', String(g));
      if (etiket) etiket.textContent = ETIKET[g];
    });
  });

  /* ------------------------------------------------------------ doğrulama */
  Array.prototype.forEach.call(formlar, function (f) {
    var alanlar = [].slice.call(f.querySelectorAll('input, select'));
    var done = f.querySelector('[data-dh-form-done]');

    alanlar.forEach(function (a) {
      a.addEventListener('input', function () { temizle(a); });
      a.addEventListener('change', function () { temizle(a); });
    });

    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var ilk = null;

      alanlar.forEach(function (a) {
        if (a.getAttribute('type') === 'hidden') return;
        var hata = null;

        if (a.required) {
          var bos = (a.type === 'checkbox') ? !a.checked : !String(a.value).trim();
          if (bos) hata = a.getAttribute('data-dh-bos') || 'Bu alan zorunlu.';
        }
        if (!hata && a.type === 'email' && a.value && !EPOSTA.test(a.value)) {
          hata = 'Geçerli bir e-posta adresi yazın.';
        }
        if (!hata && a.type === 'password' && a.value && !a.hasAttribute('data-dh-eslesir')) {
          var min = parseInt(a.getAttribute('minlength') || '0', 10);
          if (min && a.value.length < min) hata = 'Şifre en az ' + min + ' karakter olmalı.';
        }
        if (!hata && a.hasAttribute('data-dh-eslesir')) {
          var kaynak = document.getElementById(a.getAttribute('data-dh-eslesir'));
          if (kaynak && a.value !== kaynak.value) hata = 'Şifreler aynı değil.';
        }

        if (hata) { isaretle(a, hata); if (!ilk) ilk = a; }
        else { temizle(a); }
      });

      if (ilk) {
        if (done) done.classList.remove('is-on');
        ilk.focus();
        return;
      }

      f.reset();
      var m = f.querySelector('[data-dh-pwm]');
      if (m) {
        m.setAttribute('data-guc', '0');
        var l = m.querySelector('.dh-auth__pwl');
        if (l) l.textContent = ETIKET[0];
      }
      if (done) {
        done.classList.add('is-on');
        done.setAttribute('tabindex', '-1');
        done.focus();
      }
    });
  });
})();
