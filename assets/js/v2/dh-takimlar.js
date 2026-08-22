/* ============================================================================
   Dada Haber v2 — Takım dizini süzgeci (takim.html)

   Talep: "Sadece Süper Lig değil, alt lig takımları da var. Burada bir
   filtreleme yapısına ihtiyacımız var."

   İKİ KADEMELİ SÜZGEÇ: dal seçilince lig çipleri o dala daralır. Ad
   araması ikisinin üstüne biner. Süzgeç DOM'da: kart gizlenir/gösterilir,
   veri kopyası tutulmaz — tek doğruluk kaynağı işaretleme.
   ========================================================================== */
(function () {
  'use strict';

  var KOK = document.querySelector('[data-dh-takim]');
  if (!KOK) return;

  var grid = KOK.querySelector('[data-dh-takim-grid]');
  var kart = [].slice.call(grid.children);
  var dalCips = KOK.querySelector('[data-dh-takim-dal]');
  var ligCips = KOK.querySelector('[data-dh-takim-lig]');
  var ara = KOK.querySelector('[data-dh-takim-ara]');
  var sayac = KOK.querySelector('[data-dh-takim-sayac]');
  var bos = KOK.querySelector('[data-dh-takim-bos]');

  var dal = 'tumu', lig = 'tumu', q = '';

  function ciz() {
    var n = 0;
    kart.forEach(function (k) {
      var uy = (dal === 'tumu' || k.getAttribute('data-dal') === dal)
        && (lig === 'tumu' || k.getAttribute('data-lig') === lig)
        && (!q || k.getAttribute('data-ara').indexOf(q) >= 0);
      k.hidden = !uy;
      if (uy) n++;
    });
    if (sayac) sayac.textContent = n;
    if (bos) bos.hidden = n > 0;

    // Lig çipleri seçili dala daralır.
    [].slice.call(ligCips.children).forEach(function (b) {
      var bd = b.getAttribute('data-dal');
      b.hidden = !!(bd && dal !== 'tumu' && bd !== dal);
    });

    isaretle(dalCips, 'data-dal', dal);
    isaretle(ligCips, 'data-lig', lig);
  }

  function isaretle(kap, nitelik, deger) {
    [].slice.call(kap.children).forEach(function (b) {
      var on = b.getAttribute(nitelik) === deger;
      b.classList.toggle('is-on', on);
      b.setAttribute('aria-checked', on ? 'true' : 'false');
    });
  }

  dalCips.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-dal]') : null;
    if (!b) return;
    dal = b.getAttribute('data-dal');
    // Dal değişince lig seçimi geçersiz kalabilir; başa döner.
    lig = 'tumu';
    ciz();
  });

  ligCips.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('[data-lig]') : null;
    if (!b) return;
    lig = b.getAttribute('data-lig');
    ciz();
  });

  if (ara) ara.addEventListener('input', function () {
    q = ara.value.trim().toLowerCase()
      .replace(/[çğıöşü]/g, function (c) {
        return { 'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u' }[c];
      });
    ciz();
  });

  ciz();
})();
