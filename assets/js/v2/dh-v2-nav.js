/* v2 — aktif ana menü başlığı
   Sayfa <body data-dh-cat="spor"> yazar; kabuk her sayfada aynı olduğu için
   aktif işareti markup'a gömülmez, buradan verilir. Böylece kabuk tek
   kaynaktan (docs/parts/) yayılabilir ve sayfa başına sapma olmaz. */
(function () {
  var cat = document.body && document.body.getAttribute('data-dh-cat');
  if (!cat) return;
  var sec = ['.dh-v2-nav__list', '.dh-v2-off__list'];
  for (var i = 0; i < sec.length; i++) {
    var a = document.querySelector(sec[i] + ' > li > a[data-cat="' + cat + '"]');
    if (a) a.setAttribute('aria-current', 'page');
  }
})();
