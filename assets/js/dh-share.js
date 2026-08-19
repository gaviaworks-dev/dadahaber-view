/* R2-4 — PAYLAŞ BİLEŞENİ
   Referans: dadagourmet.com .ptr-share (buton + açılır menü).
   UX yükseltmeleri:
     - Web Share API varsa native paylaşım butonu görünür (mobil)
     - Bağlantı kopyalama + görünür ve okuyucuya duyurulan geri bildirim
     - Paylaşım URL'leri çalışma anında doldurulur (kopyala-yapıştır hatası olmaz)
     - Tüm hedefler en az 44x44px (WCAG 2.5.5 dokunma hedefi) */
(function () {
  var box = document.querySelector('[data-dh-share]');
  if (!box) return;

  var url = location.href;
  var title = (document.querySelector('h1') || {}).textContent || document.title;
  title = title.replace(/\s+/g, ' ').trim();

  box.querySelectorAll('[data-dh-share-url]').forEach(function (a) {
    a.href = a.dataset.dhShareUrl
      .replace(/\{url\}/g, encodeURIComponent(url))
      .replace(/\{title\}/g, encodeURIComponent(title));
  });

  var toast = box.querySelector('[data-dh-share-toast]');
  var timer;
  function say(msg, ok) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.toggle('is-error', !ok);
    toast.classList.add('is-on');
    window.clearTimeout(timer);
    timer = window.setTimeout(function () { toast.classList.remove('is-on'); }, 2600);
  }

  var nativeBtn = box.querySelector('[data-dh-share-native]');
  if (nativeBtn && navigator.share) {
    nativeBtn.hidden = false;
    nativeBtn.addEventListener('click', function () {
      navigator.share({ title: title, url: url }).catch(function () {});
    });
  }

  var copyBtn = box.querySelector('[data-dh-share-copy]');
  if (copyBtn) {
    copyBtn.addEventListener('click', function () {
      function done() { say('Bağlantı kopyalandı', true); }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(url).then(done, fallback);
      } else { fallback(); }
      function fallback() {
        var t = document.createElement('textarea');
        t.value = url; t.setAttribute('readonly', ''); t.style.position = 'fixed'; t.style.opacity = '0';
        document.body.appendChild(t); t.select();
        var ok = false;
        try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
        document.body.removeChild(t);
        ok ? done() : say('Kopyalanamadı — bağlantıyı elle seçin', false);
      }
    });
  }
})();
