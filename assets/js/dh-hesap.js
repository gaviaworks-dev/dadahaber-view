/* dh-hesap.js — Gebelik hesaplayıcıları (hamilelik.html)
   Saf vanilla JS, kütüphane yok. İki hesaplayıcı:
     1) Gebelik haftası + tahmini doğum tarihi  (#dh-hesap-hafta)
     2) Yumurtlama ve doğurgan dönem            (#dh-hesap-yumurta)

   Yöntem (yaygın Naegele kuralı, TAHMİNİDİR):
     · Son adet tarihinden (SAT): TDT = SAT + 280 gün + (döngü - 28)
     · Gebe kalma tarihinden    : SAT karşılığı = tarih - 14 gün
     · Yumurtlama               : SAT + döngü - 14
     · Doğurgan aralık          : yumurtlama - 5 ... yumurtlama + 1
   Sonuçların tamamı ekranda "tahmini" olarak etiketlenir; hata
   durumu renge TEK BAŞINA güvenmez (ikon + metin + aria-live). */
(function () {
  'use strict';

  var GUN = 86400000;
  var AY = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
    'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'];

  function bugun() { var d = new Date(); return new Date(d.getFullYear(), d.getMonth(), d.getDate()); }
  function parse(v) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(v || '');
    if (!m) return null;
    var d = new Date(+m[1], +m[2] - 1, +m[3]);
    return (d.getFullYear() === +m[1] && d.getMonth() === +m[2] - 1 && d.getDate() === +m[3]) ? d : null;
  }
  function ekle(d, n) { return new Date(d.getFullYear(), d.getMonth(), d.getDate() + n); }
  function fark(a, b) { return Math.round((b - a) / GUN); }
  function yaz(d) { return d.getDate() + ' ' + AY[d.getMonth()] + ' ' + d.getFullYear(); }

  /* --- Alan hatası: kutu + ikon + metin, renk tek gösterge değil --- */
  function hata(fld, mesaj) {
    if (!fld) return;
    fld.classList.add('dh-fld--err');
    var box = fld.querySelector('.dh-fld__err');
    var inp = fld.querySelector('.dh-input');
    if (box) {
      box.innerHTML = '<i class="fas fa-exclamation-circle" aria-hidden="true"></i><span></span>';
      box.querySelector('span').textContent = mesaj;
      box.hidden = false;
    }
    if (inp) { inp.setAttribute('aria-invalid', 'true'); }
  }
  function temizle(form) {
    var flds = form.querySelectorAll('.dh-fld');
    for (var i = 0; i < flds.length; i++) {
      flds[i].classList.remove('dh-fld--err');
      var box = flds[i].querySelector('.dh-fld__err');
      if (box) { box.hidden = true; box.textContent = ''; }
      var inp = flds[i].querySelector('.dh-input');
      if (inp) inp.removeAttribute('aria-invalid');
    }
  }
  function goster(host) { if (host) host.hidden = false; }

  /* =========== 1) Gebelik haftası + tahmini doğum tarihi =========== */
  var f1 = document.getElementById('dh-hesap-hafta');
  if (f1) {
    var modlar = f1.querySelectorAll('input[name="dh-mod"]');
    var satWrap = f1.querySelector('[data-dh-mod="sat"]');
    var gkWrap = f1.querySelector('[data-dh-mod="gk"]');

    function mod() {
      for (var i = 0; i < modlar.length; i++) if (modlar[i].checked) return modlar[i].value;
      return 'sat';
    }
    function modUygula() {
      var m = mod();
      if (satWrap) satWrap.hidden = (m !== 'sat');
      if (gkWrap) gkWrap.hidden = (m !== 'gk');
    }
    for (var i = 0; i < modlar.length; i++) modlar[i].addEventListener('change', modUygula);
    modUygula();

    f1.addEventListener('submit', function (e) {
      e.preventDefault();
      temizle(f1);
      var out = f1.querySelector('[data-dh-out]');
      var m = mod();
      var alanId = (m === 'sat') ? 'dh-sat' : 'dh-gk';
      var inp = f1.querySelector('#' + alanId);
      var fld = inp ? inp.closest('.dh-fld') : null;
      var d = parse(inp && inp.value);
      var t = bugun();

      if (!d) { hata(fld, 'Tarihi gün/ay/yıl olarak eksiksiz seçin.'); if (inp) inp.focus(); return; }
      if (d > t) { hata(fld, 'İleri bir tarih seçilemez. Geçmiş bir tarih girin.'); inp.focus(); return; }

      var dongu = 28;
      if (m === 'sat') {
        var sel = f1.querySelector('#dh-dongu');
        dongu = parseInt(sel && sel.value, 10);
        if (!dongu) { hata(sel.closest('.dh-fld'), 'Döngü uzunluğunu seçin.'); sel.focus(); return; }
      }

      // SAT karşılığı: gebe kalma tarihi verildiyse 14 gün geri al
      var sat = (m === 'sat') ? d : ekle(d, -14);
      var duzeltme = (m === 'sat') ? (dongu - 28) : 0;
      var gecen = fark(sat, t) - duzeltme;

      if (gecen < 0) { hata(fld, 'Bu tarih henüz bir gebelik haftası vermiyor. Tarihi kontrol edin.'); inp.focus(); return; }
      if (gecen > 300) { hata(fld, 'Tarih 300 günden eski. Gebelik takibi için son adet tarihinizi girin.'); inp.focus(); return; }

      var hafta = Math.floor(gecen / 7);
      var gun = gecen % 7;
      var tdt = ekle(sat, 280 + duzeltme);
      var kalan = fark(t, tdt);
      var tri = hafta <= 13 ? '1. Trimester' : (hafta <= 27 ? '2. Trimester' : '3. Trimester');
      var eksenHafta = Math.min(40, Math.max(1, hafta || 1));

      f1.querySelector('[data-dh-res="hafta"]').textContent = hafta + ' hafta ' + gun + ' gün';
      f1.querySelector('[data-dh-res="tri"]').textContent = tri;
      f1.querySelector('[data-dh-res="tdt"]').textContent = yaz(tdt);
      f1.querySelector('[data-dh-res="kalan"]').textContent =
        kalan > 0 ? (kalan + ' gün') : (kalan === 0 ? 'Bugün' : Math.abs(kalan) + ' gün geçti');
      var git = f1.querySelector('[data-dh-res-goto]');
      if (git) {
        git.hidden = false;
        git.textContent = eksenHafta + '. haftayı eksende aç';
        git.setAttribute('data-week', String(eksenHafta));
      }
      goster(out);
    });

    f1.addEventListener('reset', function () {
      temizle(f1);
      var out = f1.querySelector('[data-dh-out]');
      if (out) out.hidden = true;
      setTimeout(modUygula, 0);
    });

    f1.addEventListener('click', function (e) {
      var g = e.target.closest && e.target.closest('[data-dh-res-goto]');
      if (!g) return;
      e.preventDefault();
      document.dispatchEvent(new CustomEvent('dh-gebelik-goto',
        { detail: { week: parseInt(g.getAttribute('data-week'), 10) } }));
    });
  }

  /* =========== 2) Yumurtlama ve doğurgan dönem =========== */
  var f2 = document.getElementById('dh-hesap-yumurta');
  if (f2) {
    f2.addEventListener('submit', function (e) {
      e.preventDefault();
      temizle(f2);
      var inp = f2.querySelector('#dh-y-sat');
      var fld = inp.closest('.dh-fld');
      var sel = f2.querySelector('#dh-y-dongu');
      var d = parse(inp.value);
      var t = bugun();

      if (!d) { hata(fld, 'Son adet tarihini gün/ay/yıl olarak seçin.'); inp.focus(); return; }
      if (d > t) { hata(fld, 'İleri bir tarih seçilemez. Geçmiş bir tarih girin.'); inp.focus(); return; }
      if (fark(d, t) > 120) { hata(fld, 'Tarih 120 günden eski. Son döngünüzün ilk gününü girin.'); inp.focus(); return; }

      var dongu = parseInt(sel.value, 10);
      if (!dongu) { hata(sel.closest('.dh-fld'), 'Döngü uzunluğunu seçin.'); sel.focus(); return; }

      var yum = ekle(d, dongu - 14);
      var bas = ekle(yum, -5);
      var bit = ekle(yum, 1);
      var sonraki = ekle(d, dongu);

      f2.querySelector('[data-dh-res="yum"]').textContent = yaz(yum);
      f2.querySelector('[data-dh-res="aralik"]').textContent = yaz(bas) + ' – ' + yaz(bit);
      f2.querySelector('[data-dh-res="sonraki"]').textContent = yaz(sonraki);
      goster(f2.querySelector('[data-dh-out]'));
    });

    f2.addEventListener('reset', function () {
      temizle(f2);
      var out = f2.querySelector('[data-dh-out]');
      if (out) out.hidden = true;
    });
  }
})();
