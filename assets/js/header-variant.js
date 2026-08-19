/* GEÇİCİ — header varyant önizlemesi.
   index.html?v=a  -> ana bar kurumsal renk zeminli
   index.html?v=b  -> ana bar beyaz (varsayılan)
   Varyant seçildikten sonra bu dosya ve index.html'deki <script> satırı silinecek. */
(function () {
  var v = new URLSearchParams(location.search).get('v');
  if (v !== 'a' && v !== 'b') return;
  var b = document.body || document.documentElement;
  b.classList.remove('dh-header-a', 'dh-header-b');
  b.classList.add('dh-header-' + v);
})();
