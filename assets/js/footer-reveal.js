/* İŞ 3 — FOOTER PERDESİ
   Footer'ın yüksekliğini ölçüp içerik sarmalayıcısının altına o kadar boşluk
   yazar; böylece sayfa sonunda içerik kalkar ve sabit duran footer ortaya çıkar.
   Kırılım temanın lg eşiği (992px). Altında footer statik akışta kalır.
   Güvenlik freni: footer viewport'a sığmıyorsa perde tamamen devre dışı. */
(function () {
  var MQ = '(min-width: 992px)';
  var SAFETY = 80; /* footer + bu pay viewport'u aşarsa perde kapanır */

  var wrap = document.getElementById('wrapper');
  var foot = document.getElementById('uc-footer');
  if (!wrap || !foot) return;

  var body = document.body;

  function fit() {
    var wide = window.matchMedia(MQ).matches;

    if (!wide) {
      body.classList.remove('dh-footer-reveal');
      wrap.style.marginBottom = '';
      return;
    }

    /* Ölçüm için perdeyi geçici olarak kapat: footer akışta iken
       gerçek yüksekliği okunur (fixed hâlde de aynı, ama tema
       değişimlerinde güvenli taraf bu). */
    body.classList.add('dh-footer-reveal');
    var h = foot.offsetHeight;

    if (h + SAFETY > window.innerHeight) {
      /* Footer ekrana sığmıyor — sabitlense üst kısmı hiç görünmezdi. */
      body.classList.remove('dh-footer-reveal');
      wrap.style.marginBottom = '';
      return;
    }

    wrap.style.marginBottom = h + 'px';
  }

  fit();
  window.addEventListener('resize', fit);
  window.addEventListener('load', fit);
  window.addEventListener('darkmode', fit); /* tema değişince yükseklik oynayabilir */
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
})();
