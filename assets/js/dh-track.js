/* dh-track.js — yatay kayan ray gezinme (R4)
   Kullanım:
     <div class="dh-track" id="fotoTrack"> ... kartlar ... </div>
     <button data-dh-track-prev="fotoTrack"> / <button data-dh-track-next="fotoTrack">
   Kütüphane yok; native scroll + scroll-snap üstüne ince bir katman.
   Bir adım = ekranda tam görünen kart sayısı kadar kart adımı. */
(function () {
  'use strict';

  function pitch(track) {
    var first = track.firstElementChild;
    if (!first) return track.clientWidth;
    var cs = getComputedStyle(track);
    var gap = parseFloat(cs.columnGap || cs.gap) || 0;
    return first.getBoundingClientRect().width + gap;
  }

  function step(track) {
    var p = pitch(track);
    if (!p) return track.clientWidth;
    var visible = Math.max(1, Math.floor(track.clientWidth / p));
    return p * visible;
  }

  function sync(track, prev, next) {
    /* Tolerans 3px: rayın 2px yatay padding'i yüzünden snap, teorik en büyük
       scrollLeft'in 2px gerisinde duruyor (390px ölçümü: scrollLeft 1984 /
       max 1986). 1px toleransla ileri oku sonda pasifleşmiyordu. */
    var max = track.scrollWidth - track.clientWidth - 3;
    if (prev) prev.disabled = track.scrollLeft <= 3;
    if (next) next.disabled = track.scrollLeft >= max;
    if (max <= 3) {
      if (prev) prev.disabled = true;
      if (next) next.disabled = true;
    }
  }

  /* Kenar yumuşatma durumu: .dh-edge-fade taşıyan HER ray için çalışır,
     prev/next düğmesi olsun olmasın (ör. .dh-shorts kendi scriptiyle geziniyor). */
  function fade(el) {
    var max = el.scrollWidth - el.clientWidth;
    el.classList.toggle('is-static', max <= 2);
    el.classList.toggle('is-start', el.scrollLeft <= 2);
    el.classList.toggle('is-end', el.scrollLeft >= max - 2);
  }

  function wireFade(el) {
    var raf = 0;
    var update = function () {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(function () { fade(el); });
    };
    el.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    if (window.ResizeObserver) new ResizeObserver(update).observe(el);
    update();
    setTimeout(update, 400);
    setTimeout(update, 1600);
  }

  function wire(track) {
    var id = track.id;
    if (!id) return;
    var prev = document.querySelector('[data-dh-track-prev="' + id + '"]');
    var next = document.querySelector('[data-dh-track-next="' + id + '"]');
    if (prev) prev.addEventListener('click', function () {
      track.scrollBy({ left: -step(track), behavior: 'smooth' });
    });
    if (next) next.addEventListener('click', function () {
      track.scrollBy({ left: step(track), behavior: 'smooth' });
    });

    var raf = 0;
    var update = function () {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(function () { sync(track, prev, next); });
    };
    track.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    if (window.ResizeObserver) new ResizeObserver(update).observe(track);
    // Görseller yüklendikçe genişlik değişiyor; ilk senkron birkaç kez tekrarlanır.
    update();
    setTimeout(update, 400);
    setTimeout(update, 1600);
  }

  function init() {
    document.querySelectorAll('.dh-track[id]').forEach(wire);
    document.querySelectorAll('.dh-edge-fade').forEach(wireFade);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
