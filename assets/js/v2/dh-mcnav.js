/* ============================================================================
   Dada Haber v2 — Maç rayı: önceki / sonraki maç gezinmesi

   NEDEN KAYDIRMA DEĞİL: talep "scrollbar şeklinde gitmesin" idi. Önce
   mevcut dh-track.js ile yatay kaydırma denendi; ray programlı kaydırmayı
   KABUL ETMEDİ (ölçüldü: scrollWidth 1214 / clientWidth 394 olmasına
   rağmen `scrollLeft = 400` ataması 0'da kalıyor; snap kapatıldıktan
   sonra da değişmedi). Kaydırmayla uğraşmak yerine kartlar tek tek
   GÖSTERİLİYOR: bir anda bir maç görünür, düğmeler indisi değiştirir.
   Böylece kaydırma çubuğu da, snap çakışması da ortadan kalkıyor.

   SÖZLEŞME
     <div class="dh-mcnav">
       <button data-dh-mcnav-prev="<rayId>">  <button data-dh-mcnav-next="<rayId>">
     <div class="dh-mcrail" id="<rayId>"> <article> ... </article> </div>
   ========================================================================== */
(function () {
  'use strict';

  function kur(ray) {
    var id = ray.id;
    if (!id) return;
    var prev = document.querySelector('[data-dh-mcnav-prev="' + id + '"]');
    var next = document.querySelector('[data-dh-mcnav-next="' + id + '"]');
    var kart = [].slice.call(ray.children);
    if (kart.length < 2) {
      if (prev) prev.hidden = true;
      if (next) next.hidden = true;
      return;
    }

    var i = 0;
    var sayac = document.querySelector('[data-dh-mcnav-sayac="' + id + '"]');

    function ciz() {
      kart.forEach(function (k, j) {
        k.hidden = j !== i;
      });
      if (prev) prev.disabled = i === 0;
      if (next) next.disabled = i === kart.length - 1;
      if (sayac) sayac.textContent = (i + 1) + ' / ' + kart.length;
    }

    if (prev) prev.addEventListener('click', function () {
      if (i > 0) { i--; ciz(); }
    });
    if (next) next.addEventListener('click', function () {
      if (i < kart.length - 1) { i++; ciz(); }
    });

    ray.classList.add('dh-mcrail--tek');
    ciz();
  }

  function init() {
    document.querySelectorAll('.dh-mcrail[data-dh-mcnav]').forEach(kur);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
