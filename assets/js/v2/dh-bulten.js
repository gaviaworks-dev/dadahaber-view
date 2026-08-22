/* ============================================================================
   Dada Haber v2 — Bülten açılır penceresi KAPALI

   Talep (22 Ağustos): "Bu kısım kalkacak."

   NEDEN JS: pencereyi vendor `app-head-bs.js` açıyor —
     const t = localStorage.getItem("newsletterModalShown");
     !t && setTimeout(() => UniCore.modal("#uc-newsletter-modal").show(), 1e4);
   O dosya v1 arşiviyle paylaşılıyor, DEĞİŞTİRİLEMEZ (denetim.py 7. kural).
   Bayrak burada, vendor'ın DOMContentLoaded dinleyicisi okumadan ÖNCE
   yazılıyor: `defer` betikler DOMContentLoaded'dan önce çalışır, bu yüzden
   sıra garanti.

   İşaretleme (`#uc-newsletter-modal`) sayfalardan ayrıca kaldırıldı
   (yay.py); bu dosya ikinci emniyet.
   ========================================================================== */
(function () {
  'use strict';
  try {
    localStorage.setItem('newsletterModalShown', 'true');
  } catch (e) {}
})();
