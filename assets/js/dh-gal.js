/* dh-gal.js — R6-M · Foto galeri görüntüleyici
   Kütüphane yok. Kalıp kaynağı: dadagastro.com/video-mutfagi seri
   gezinme davranışı; görüntüleyici tarafı foto muhabirliğinin kendi
   nesnesinden (kontak baskısı) türetildi.

   Markup sözleşmesi:
     <div class="dh-gal" id="X" data-dh-gal>
       <div class="dh-gal__stage">
         <img class="dh-gal__img is-on" src data-cap data-credit>
         ... N adet
         <span class="dh-gal__count"><b>01</b> / 24</span>
         <button class="dh-gal__arrow dh-gal__arrow--prev" data-dh-gal-prev>
         <button class="dh-gal__arrow dh-gal__arrow--next" data-dh-gal-next>
         <button class="dh-gal__tool" data-dh-gal-full>
       </div>
       <div class="dh-gal__cap">
         <span class="dh-gal__captxt" data-dh-gal-cap></span>
         <span class="dh-gal__credit" data-dh-gal-credit></span>
       </div>
       <div class="dh-gal__strip">
         <button class="dh-gal__thumb" data-dh-gal-go="0"> ... </button>
       </div>
     </div>

   Klavye: ← önceki · → sonraki · Home ilk · End son · Esc tam ekran çıkışı.
   Tam ekranda body kaydırması kilitlenir (html.dh-gal-lock). */
(function () {
  'use strict';

  function pad(n) { return (n < 10 ? '0' : '') + n; }

  function setup(root) {
    var stage = root.querySelector('.dh-gal__stage');
    if (!stage) return;
    var imgs = [].slice.call(stage.querySelectorAll('.dh-gal__img'));
    if (!imgs.length) return;

    var thumbs = [].slice.call(root.querySelectorAll('[data-dh-gal-go]'));
    var strip = root.querySelector('.dh-gal__strip');
    var prev = root.querySelector('[data-dh-gal-prev]');
    var next = root.querySelector('[data-dh-gal-next]');
    var full = root.querySelector('[data-dh-gal-full]');
    var countCur = root.querySelector('[data-dh-gal-cur]');
    var countAll = root.querySelector('[data-dh-gal-all]');
    var capEl = root.querySelector('[data-dh-gal-cap]');
    var credEl = root.querySelector('[data-dh-gal-credit]');
    var i = Math.max(0, imgs.findIndex(function (x) { return x.classList.contains('is-on'); }));
    if (i < 0) i = 0;

    if (countAll) countAll.textContent = pad(imgs.length);

    function show(n, scrollStrip) {
      n = (n + imgs.length) % imgs.length;
      i = n;
      imgs.forEach(function (im, k) { im.classList.toggle('is-on', k === n); });
      thumbs.forEach(function (t, k) {
        t.classList.toggle('is-on', k === n);
        t.setAttribute('aria-current', k === n ? 'true' : 'false');
      });
      var cur = imgs[n];
      if (countCur) countCur.textContent = pad(n + 1);
      if (capEl) capEl.textContent = cur.getAttribute('data-cap') || '';
      if (credEl) credEl.textContent = cur.getAttribute('data-credit') || '';
      /* Görsel yükünü öne çekmeden, yalnız komşuları hazırla. */
      [n - 1, n + 1].forEach(function (k) {
        var im = imgs[(k + imgs.length) % imgs.length];
        if (im && im.loading === 'lazy') im.loading = 'eager';
      });
      if (scrollStrip !== false && strip && thumbs[n]) {
        var tr = thumbs[n].getBoundingClientRect(), sr = strip.getBoundingClientRect();
        if (tr.left < sr.left + 8 || tr.right > sr.right - 8) {
          strip.scrollTo({ left: thumbs[n].offsetLeft - (strip.clientWidth - tr.width) / 2, behavior: 'smooth' });
        }
      }
    }

    if (prev) prev.addEventListener('click', function () { show(i - 1); });
    if (next) next.addEventListener('click', function () { show(i + 1); });
    thumbs.forEach(function (t, k) {
      t.addEventListener('click', function () { show(k); });
    });

    /* Sahneye tıklama: sağ yarı ileri, sol yarı geri. Tam ekranda da geçerli. */
    stage.addEventListener('click', function (e) {
      if (e.target.closest('button')) return;
      var r = stage.getBoundingClientRect();
      show(e.clientX - r.left > r.width / 2 ? i + 1 : i - 1);
    });

    /* Tam ekran, #wrapper'ın DIŞINA taşınarak açılır.
       Sebep (HANDOFF'ta kayıtlı tuzak): #wrapper position:relative + z-index
       alıyor, kendi stacking context'ini açıyor. İçindeki position:fixed
       öğe, z-index 1002 bile olsa sticky header'ın (z-999) ALTINDA kalıyor
       — ekran görüntüsüyle doğrulandı. .dh-reels da aynı sebeple markup'ta
       #wrapper dışında duruyor. Burada aynı çözüm JS ile uygulanıyor:
       açılışta düğüm body'ye taşınır, kapanışta yerine geri konur. */
    var anchor = document.createComment('dh-gal');

    function setFull(on) {
      if (on) {
        if (!anchor.parentNode) root.parentNode.insertBefore(anchor, root);
        document.body.appendChild(root);
      } else if (anchor.parentNode) {
        anchor.parentNode.insertBefore(root, anchor);
        anchor.parentNode.removeChild(anchor);
      }
      root.classList.toggle('is-full', on);
      document.documentElement.classList.toggle('dh-gal-lock', on);
      if (full) {
        full.setAttribute('aria-pressed', on ? 'true' : 'false');
        full.setAttribute('aria-label', on ? 'Tam ekrandan çık' : 'Tam ekran');
        var ic = full.querySelector('i');
        if (ic) ic.className = on ? 'fas fa-compress' : 'fas fa-expand';
      }
      show(i, true);
    }

    if (full) full.addEventListener('click', function () { setFull(!root.classList.contains('is-full')); });

    document.addEventListener('keydown', function (e) {
      var isFull = root.classList.contains('is-full');
      /* Tam ekran değilken yalnız galeri odaktayken klavyeyi dinle;
         sayfadaki diğer ok kullanımlarını çalmasın. */
      if (!isFull && !root.contains(document.activeElement)) return;
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(i - 1); }
      else if (e.key === 'ArrowRight') { e.preventDefault(); show(i + 1); }
      else if (e.key === 'Home') { e.preventDefault(); show(0); }
      else if (e.key === 'End') { e.preventDefault(); show(imgs.length - 1); }
      else if (e.key === 'Escape' && isFull) { e.preventDefault(); setFull(false); }
    });

    /* Dokunmatik kaydırma */
    var x0 = null;
    stage.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    stage.addEventListener('touchend', function (e) {
      if (x0 === null) return;
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 42) show(dx < 0 ? i + 1 : i - 1);
      x0 = null;
    }, { passive: true });

    show(i, false);
  }

  function init() { document.querySelectorAll('[data-dh-gal]').forEach(setup); }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
