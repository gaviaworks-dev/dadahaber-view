/*!
 * dh-toc.js — yapışkan içindekiler kolonu için aktif bölüm işareti.
 * Kütüphanesiz. IntersectionObserver ile okunmakta olan bölümü bulur,
 * ilgili .dh-toc__link öğesine .is-now sınıfını verir (aile imzası).
 *
 * rootMargin üst değeri -140px: sabit header 120px + 20px nefes.
 * Bir bölüm görünür alanın üst bandına girdiği anda "okunuyor" sayılır.
 */
(function () {
  'use strict';

  function init() {
    var nav = document.querySelector('[data-dh-toc]');
    if (!nav) return;

    var links = Array.prototype.slice.call(nav.querySelectorAll('.dh-toc__link'));
    if (!links.length) return;

    var map = {};
    var sections = [];
    links.forEach(function (a) {
      var id = (a.getAttribute('href') || '').replace('#', '');
      if (!id) return;
      var sec = document.getElementById(id);
      if (!sec) return;
      map[id] = a;
      sections.push(sec);
    });
    if (!sections.length) return;

    var current = null;
    function mark(el) {
      if (el === current) return;
      links.forEach(function (a) {
        a.classList.remove('is-now');
        a.removeAttribute('aria-current');
      });
      if (el) {
        el.classList.add('is-now');
        el.setAttribute('aria-current', 'true');
      }
      current = el;
    }

    // Görünürlük oranı yerine "üst banda en yakın görünür bölüm" kuralı:
    // uzun bölümlerde oran ölçümü yanıltıyor.
    var visible = {};
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        visible[e.target.id] = e.isIntersecting;
      });
      var hit = null;
      for (var i = 0; i < sections.length; i++) {
        if (visible[sections[i].id]) { hit = sections[i]; break; }
      }
      if (!hit) {
        // Hiçbiri bantta değil: son geçilen bölümü koru.
        var y = window.scrollY + 140;
        for (var j = 0; j < sections.length; j++) {
          if (sections[j].offsetTop <= y) hit = sections[j];
        }
      }
      mark(hit ? map[hit.id] : null);
    }, { rootMargin: '-140px 0px -60% 0px', threshold: 0 });

    sections.forEach(function (s) { io.observe(s); });

    // Bağlantıya tıklanınca hedef bölüm hemen işaretlensin
    nav.addEventListener('click', function (e) {
      var a = e.target.closest ? e.target.closest('.dh-toc__link') : null;
      if (a) mark(a);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
