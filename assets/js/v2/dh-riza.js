/* ============================================================================
   Dada Haber v2 — Açık Rıza Yönetimi (`cerezler.html#riza`)

   VERİ SÖZLEŞMESİ
   ---------------
   Depo      : localStorage
   Anahtar   : "dh-riza"
   Değer     : JSON — { "s": 1, "islevsel": bool, "analitik": bool,
                        "pazarlama": bool, "t": "<ISO 8601>" }
               "s"  → sözleşme sürümü. Sürüm artarsa eski kayıt yok sayılır
                      ve okura yeniden sorulur.
               "t"  → tercihin kaydedildiği an.
   Zorunlu çerezler kayda YAZILMAZ: kapatılamadıkları için saklanacak bir
   tercih yoktur. Arayüzde `disabled` + `checked` gösterilir.

   Bu dosya PROTOTİPTİR: gerçek bir çerez yazmaz/siler, yalnız tercihi saklar.
   Mevcut `assets/js/*.js` dosyalarına dokunulmadı (v1 donmuş kalmalı).
   ========================================================================== */
(function () {
  'use strict';

  var KOK = document.querySelector('[data-dh-riza]');
  if (!KOK) return;                       // bileşen yoksa hiçbir şey yapma

  var ANAHTAR = 'dh-riza';
  var SURUM = 1;
  var ALANLAR = ['islevsel', 'analitik', 'pazarlama'];

  var kutular = {};
  ALANLAR.forEach(function (ad) {
    kutular[ad] = KOK.querySelector('input[data-dh-riza-alan="' + ad + '"]');
  });
  var durum = KOK.querySelector('[data-dh-riza-durum]');
  var damga = KOK.querySelector('[data-dh-riza-damga]');

  function oku() {
    try {
      var ham = localStorage.getItem(ANAHTAR);
      if (!ham) return null;
      var v = JSON.parse(ham);
      if (!v || v.s !== SURUM) return null;
      return v;
    } catch (e) { return null; }
  }

  function yaz(v) {
    try { localStorage.setItem(ANAHTAR, JSON.stringify(v)); return true; }
    catch (e) { return false; }
  }

  function tarihMetni(iso) {
    var d = new Date(iso);
    if (isNaN(d)) return '';
    function ik(n) { return (n < 10 ? '0' : '') + n; }
    var ay = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
              'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'];
    return d.getDate() + ' ' + ay[d.getMonth()] + ' ' + d.getFullYear() +
           ', ' + ik(d.getHours()) + '.' + ik(d.getMinutes());
  }

  // --- arayüzü tazele ------------------------------------------------------
  function tazele(kayit) {
    var acik = ALANLAR.filter(function (ad) {
      return kutular[ad] && kutular[ad].checked;
    });
    var metin;
    if (!kayit) {
      metin = 'Henüz bir tercih kaydetmediniz. Zorunlu çerezler dışında hiçbir çerez çalışmıyor.';
    } else if (!acik.length) {
      metin = 'Yalnız zorunlu çerezler açık.';
    } else {
      var adlar = { islevsel: 'işlevsel', analitik: 'analitik', pazarlama: 'pazarlama' };
      metin = 'Zorunlu çerezlere ek olarak açık olanlar: ' +
              acik.map(function (a) { return adlar[a]; }).join(' · ') + '.';
    }
    if (durum) durum.textContent = metin;
    if (damga) {
      damga.textContent = kayit && kayit.t
        ? 'Son kayıt: ' + tarihMetni(kayit.t)
        : 'Kayıt yok';
    }
  }

  function uygula(kayit) {
    ALANLAR.forEach(function (ad) {
      if (kutular[ad]) kutular[ad].checked = !!(kayit && kayit[ad]);
    });
    tazele(kayit);
  }

  function kaydet() {
    var kayit = { s: SURUM, t: new Date().toISOString() };
    ALANLAR.forEach(function (ad) {
      kayit[ad] = !!(kutular[ad] && kutular[ad].checked);
    });
    if (!yaz(kayit)) {
      if (durum) durum.textContent =
        'Tercih kaydedilemedi: tarayıcınız bu site için yerel depolamayı engelliyor.';
      return;
    }
    tazele(kayit);
  }

  // --- olaylar -------------------------------------------------------------
  KOK.addEventListener('change', function (e) {
    if (e.target && e.target.hasAttribute('data-dh-riza-alan')) tazele(oku());
  });

  KOK.addEventListener('click', function (e) {
    var d = e.target.closest ? e.target.closest('[data-dh-riza-eylem]') : null;
    if (!d) return;
    var eylem = d.getAttribute('data-dh-riza-eylem');
    if (eylem === 'tumu') {
      ALANLAR.forEach(function (ad) { if (kutular[ad]) kutular[ad].checked = true; });
      kaydet();
    } else if (eylem === 'zorunlu') {
      ALANLAR.forEach(function (ad) { if (kutular[ad]) kutular[ad].checked = false; });
      kaydet();
    } else if (eylem === 'kaydet') {
      kaydet();
    } else if (eylem === 'sil') {
      try { localStorage.removeItem(ANAHTAR); } catch (err) {}
      uygula(null);
    }
  });

  uygula(oku());
})();
