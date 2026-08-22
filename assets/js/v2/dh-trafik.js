/* ============================================================================
   Dada Haber v2 — Trafik ve Ulaşım: şehir seçici (trafik-ulasim.html)

   Talep: "Burada sadece İstanbul oluşturulmuş, bu doğru değil. Ankara'daki
   kişi bunu nasıl kullanacak? Kullanım için iyi değil, bunu bir
   düzenleyelim; ek özellik ekleme durumu varsa ekleyelim."

   ÖNCE: sayfa İstanbul'a gömülüydü — başlıklar ("İstanbul trafik
   yoğunluğu", "Kuzey Marmara Otoyolu") sabit metindi.
   SONRA: on şehir arasından seçim; her satır seçilen şehre göre yeniden
   yazılıyor. EK ÖZELLİK: şehir kartında yoğunluk yüzdesi ve en sıkışık
   güzergâh; ayrıca "şehrim" olarak kaydetme (localStorage) — sonraki
   ziyarette o şehir açılıyor.

   Veri prototiptir; sayısal değerler şehir indisinden deterministik
   üretilir, gerçek ölçüm değildir. Sayfa bunu görünür biçimde yazar.
   ========================================================================== */
(function () {
  'use strict';

  var KOK = document.querySelector('[data-dh-trafik]');
  if (!KOK) return;

  var ham = document.getElementById('dh-trafik-data');
  if (!ham) return;
  var VERI;
  try { VERI = JSON.parse(ham.textContent); } catch (e) { return; }

  var ANAHTAR = 'dh-trafik-sehir';
  var secili = VERI.varsayilan;
  try {
    var kayit = localStorage.getItem(ANAHTAR);
    if (kayit && VERI.sehirler[kayit]) secili = kayit;
  } catch (e) {}

  function el(sel) { return KOK.querySelector(sel) || document.querySelector(sel); }

  function ciz() {
    var v = VERI.sehirler[secili];
    if (!v) return;

    var ad = el('[data-dh-trafik-ad]');
    if (ad) ad.textContent = v.ad;
    var kaps = el('[data-dh-trafik-kapsam]');
    if (kaps) kaps.textContent = v.bolge + ' · ' + v.nufus + ' · ' + v.saat + ' itibarıyla';

    var yog = el('[data-dh-trafik-yogunluk]');
    if (yog) yog.textContent = '%' + v.yogunluk;
    var bar = el('[data-dh-trafik-bar]');
    if (bar) {
      bar.style.width = v.yogunluk + '%';
      bar.parentElement.setAttribute('data-lv', v.yogunluk >= 70 ? 'kritik'
        : v.yogunluk >= 45 ? 'uyari' : 'normal');
    }
    var sik = el('[data-dh-trafik-sikisik]');
    if (sik) sik.textContent = v.sikisik;

    var rows = el('[data-dh-trafik-satirlar]');
    if (rows) {
      rows.innerHTML = v.satirlar.map(function (r) {
        return '<li class="dh-nwstat__row" data-lv="' + r.lv + '">'
          + '<span class="dh-nwstat__ic" aria-hidden="true"><i class="fas ' + r.ikon + '"></i></span>'
          + '<span class="dh-nwstat__body"><b class="dh-nwstat__name">' + r.ad + '</b>'
          + '<span class="dh-nwstat__desc">' + r.aciklama + '</span></span>'
          + '<span class="dh-nwstat__lv">' + r.etiket + '</span></li>';
      }).join('');
    }

    KOK.querySelectorAll('[data-dh-trafik-sec]').forEach(function (b) {
      var on = b.getAttribute('data-dh-trafik-sec') === secili;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-checked', on ? 'true' : 'false');
    });

    var kaydet = el('[data-dh-trafik-kaydet]');
    if (kaydet) {
      var kayitli = false;
      try { kayitli = localStorage.getItem(ANAHTAR) === secili; } catch (e) {}
      kaydet.textContent = kayitli ? 'Şehrim olarak kayıtlı' : 'Şehrim yap';
      kaydet.classList.toggle('is-on', kayitli);
    }
  }

  KOK.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-dh-trafik-sec]') : null;
    if (b) { secili = b.getAttribute('data-dh-trafik-sec'); ciz(); return; }
    var k = e.target.closest ? e.target.closest('[data-dh-trafik-kaydet]') : null;
    if (k) {
      try {
        if (localStorage.getItem(ANAHTAR) === secili) localStorage.removeItem(ANAHTAR);
        else localStorage.setItem(ANAHTAR, secili);
      } catch (er) {}
      ciz();
    }
  });

  ciz();
})();
