/* ============================================================================
   Dada Haber v2 — Bildirim izni kartı (yumuşak soru)

   NEDEN YUMUŞAK SORU: tarayıcının kendi izin kutusu sayfa açılır açılmaz
   çıkarsa okur çoğunlukla "engelle" diyor ve karar KALICI oluyor — bir daha
   sorulamıyor. Önce site kendi kartıyla neden istediğini anlatır; okur
   "İzin Ver" derse tarayıcının kutusu ancak o zaman açılır.

   SIRA: çerez kararı önce gelir. dh-cerez.js karar anında
   `dh:riza-verildi` olayını yayar; kart onu bekler. Kayıt zaten varsa
   kısa bir gecikmeyle açılır.

   VERİ SÖZLEŞMESİ
     localStorage["dh-bildirim"] = { s:1, karar:"izin"|"sonra"|"kapatildi",
                                     t:"<ISO 8601>" }
   Karar yazıldıysa kart bir daha açılmaz.

   Bu dosya PROTOTİPTİR: bildirim ABONELİĞİ kurmaz (service worker / push
   yok). Yalnız tarayıcı iznini ister ve kararı saklar.
   ========================================================================== */
(function () {
  'use strict';

  var KOK = document.querySelector('[data-dh-bildirim]');
  if (!KOK) return;

  var ANAHTAR = 'dh-bildirim';
  var SURUM = 1;
  var GECIKME = 1600;   // çerez kararından sonra nefes payı

  function oku() {
    try {
      var v = JSON.parse(localStorage.getItem(ANAHTAR) || 'null');
      return (v && v.s === SURUM) ? v : null;
    } catch (e) { return null; }
  }

  function yaz(karar) {
    try {
      localStorage.setItem(ANAHTAR, JSON.stringify({
        s: SURUM, karar: karar, t: new Date().toISOString()
      }));
    } catch (e) {}
  }

  function kapat(karar) {
    if (karar) yaz(karar);
    KOK.hidden = true;
  }

  function ac() {
    if (oku()) return;
    // Tarayıcı zaten karar vermişse (izin verilmiş ya da engellenmiş)
    // okuru ikinci kez rahatsız etme.
    if (typeof Notification !== 'undefined' && Notification.permission !== 'default') {
      yaz(Notification.permission === 'granted' ? 'izin' : 'sonra');
      return;
    }
    KOK.hidden = false;
  }

  KOK.querySelector('[data-dh-bildirim-sonra]').addEventListener('click', function () {
    kapat('sonra');
  });
  KOK.querySelector('[data-dh-bildirim-kapat]').addEventListener('click', function () {
    kapat('kapatildi');
  });
  KOK.querySelector('[data-dh-bildirim-izin]').addEventListener('click', function () {
    kapat('izin');
    if (typeof Notification === 'undefined' || !Notification.requestPermission) return;
    try {
      var s = Notification.requestPermission();
      if (s && typeof s.then === 'function') { s.then(function () {}, function () {}); }
    } catch (e) {}
  });

  // Çerez kararı verilmeden sorma.
  var rizaVar = false;
  try { rizaVar = !!localStorage.getItem('dh-riza'); } catch (e) {}
  if (rizaVar) {
    setTimeout(ac, GECIKME);
  } else {
    document.addEventListener('dh:riza-verildi', function () { setTimeout(ac, GECIKME); });
  }
})();
