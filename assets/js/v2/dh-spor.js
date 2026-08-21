/* dh-spor.js — v2 spor bölümü davranışları (S-1 … S-4)
   Saf vanilla JS, ES5 sözdizimi, yeni kütüphane YOK.

   NEDEN AYRI DOSYA: `assets/js/dh-lig.js` · `dh-tabs.js` v1 ile paylaşılan
   dosyalardır ve DEĞİŞTİRİLEMEZ (v1 arşivi onları paylaşıyor). Bu dosya
   onların ÜSTÜNE davranış ekler; ürettikleri işaretlemeye dokunmaz, yalnız
   DOM'a yerleştirildikten sonra zenginleştirir.

   Dört iş:
   1) TAKIM BAĞLANTISI — puan durumu tablolarında arma + takım adı tek
      bağlantıya sarılır. Statik HTML'de bağlantılar zaten gömülü; bu kod
      yalnız dh-tabs.js lig/görünüm değiştirdiğinde YENİDEN üretilen
      tablolar için çalışır (idempotent: zaten <a> varsa dokunmaz).
   2) TABLO KIRPMA — 8'den fazla satırı olan puan durumu tablosu ilk 8
      satırda kırpılır, altına "Tümünü Gör" düğmesi konur.
   3) KOMPAKT LİG SEÇİCİ — ülke/lig/sezon tek satırda toplanır. Lig çipleri
      yerine bir <select> üretilir; çipler DOM'da KALIR (dh-tabs.js onlara
      bağlı) ve CSS ile gizlenir. JS kapalıysa eski çip şeridi çalışır.
   4) FİKSTÜR HAFTA GEÇİŞİ — kompakt önceki/mevcut/sonraki hafta. Hafta
      kaydırma ±7 günlük tarih aritmetiği + deplasman eşleşmelerinin
      dönüşümlü kaydırılması ile türetilir (dh-lig.js'in geçmiş sezon
      türetme yaklaşımının aynısı; veri yer tutucudur).

   Yeniden çizim: dh-tabs.js `[data-dh-lg]` kaplarının innerHTML'ini
   değiştiriyor. MutationObserver ile yakalanıp 1-2-4 yeniden uygulanır.
   Özyineleme kilidi (`kilit`) kendi eklediğimiz düğümlerin gözlemciyi
   tekrar tetiklemesini engeller. */
(function () {
  'use strict';

  /* ---------- ortak ---------- */

  var LIMIT = 8;                       /* ilk görünümde gösterilen satır */
  var HAFTA_MENZIL = 4;                /* ± kaç hafta gezilebilir */

  var BUYUK = {
    galatasaray: 'takim-galatasaray.html',
    fenerbahce: 'takim-fenerbahce.html',
    besiktas: 'takim-besiktas.html',
    trabzonspor: 'takim-trabzonspor.html'
  };
  var DETAY = 'spor-takim-detay.html';

  var AY = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
    'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık'];

  var sayac = 0;
  var kilit = false;

  function dizi(n) { return Array.prototype.slice.call(n); }

  /* Türkçe'ye duyarlı sadeleştirme: "Beşiktaş" -> "besiktas".
     toLowerCase() tek başına yetmez ('I' -> 'i' olur, 'ı' beklenirken). */
  function sade(s) {
    var ust = { 'İ': 'i', 'I': 'ı', 'Ş': 'ş', 'Ğ': 'ğ', 'Ü': 'ü', 'Ö': 'ö', 'Ç': 'ç' };
    var o = '', i, c;
    s = String(s == null ? '' : s);
    for (i = 0; i < s.length; i++) { c = s.charAt(i); o += (ust[c] || c); }
    o = o.toLowerCase()
      .replace(/ı/g, 'i').replace(/ş/g, 's').replace(/ğ/g, 'g')
      .replace(/ü/g, 'u').replace(/ö/g, 'o').replace(/ç/g, 'c');
    return o.replace(/[^a-z0-9]+/g, '');
  }

  /* Dört büyük futbol takımının kendi sayfası var; başka her takım —
     ve BÜTÜN basketbol/voleybol takımları — ortak takım detayına gider.
     "Fenerbahçe Beko" futbol sayfasına GİTMEZ: sade() tam eşleşme arar. */
  function hedef(dal, ad) {
    if (dal === 'futbol') {
      var s = sade(ad);
      if (BUYUK[s]) return BUYUK[s];
    }
    return DETAY;
  }

  /* Takım tablosu mu? Oyuncu/sporcu tabloları (gol krallığı, tenis, atletizm,
     F1, bisiklet) DIŞARIDA kalır — onların satırı bir takım değil bir KİŞİdir,
     takım sayfasına bağlanamaz. Ölçüm: puan-durumu.html'de branşı "f1" olan
     tablo .dh-stand__team kalıbını kullanıyor ama arması yok; ilk sürüm onu
     yanlışlıkla bağlamıştı. İki koşul birden aranıyor: branş + arma. */
  var TAKIM_DALI = { futbol: 1, basketbol: 1, voleybol: 1 };

  function siralamaTablosuMu(t) {
    var c = ' ' + t.className + ' ';
    return c.indexOf(' dh-stand--stat ') < 0 && c.indexOf(' dh-squad ') < 0;
  }

  function puanTablosuMu(t) {
    return siralamaTablosuMu(t) && !!TAKIM_DALI[t.getAttribute('data-branch') || ''];
  }

  function cocuk(el, sinif) {
    var i, c = el.childNodes;
    for (i = 0; i < c.length; i++) {
      if (c[i].nodeType === 1 && c[i].className && (' ' + c[i].className + ' ').indexOf(' ' + sinif + ' ') >= 0) return c[i];
    }
    return null;
  }

  /* ---------- 1) Takım bağlantısı ---------- */

  function baglantila(kok) {
    var tablo = dizi((kok || document).querySelectorAll('table.dh-stand')), i, j;
    for (i = 0; i < tablo.length; i++) {
      var t = tablo[i];
      if (!puanTablosuMu(t)) continue;
      var dal = t.getAttribute('data-branch') || '';
      var hucre = dizi(t.querySelectorAll('.dh-stand__team'));
      for (j = 0; j < hucre.length; j++) {
        var h = hucre[j];
        if (h.querySelector('a')) continue;              /* zaten bağlı */
        var ad = cocuk(h, 'dh-stand__nm');
        if (!ad) continue;                               /* oyuncu satırı */
        var arma = cocuk(h, 'dh-stand__crest');
        if (!arma) continue;                             /* armasız satır = kişi */
        var a = document.createElement('a');
        a.className = 'dh-stand__link';
        a.href = hedef(dal, ad.textContent);
        h.insertBefore(a, arma);
        a.appendChild(arma);
        a.appendChild(ad);
      }
    }
  }

  /* ---------- 2) Tablo kırpma + "Tümünü Gör" ---------- */

  function kirp(kok) {
    var tablo = dizi((kok || document).querySelectorAll('table.dh-stand')), i, j;
    for (i = 0; i < tablo.length; i++) {
      var t = tablo[i];
      if (!siralamaTablosuMu(t)) continue;
      if (t.getAttribute('data-dh-kirp') === 'yok') continue;
      if (t.getAttribute('data-dh-kirpildi')) continue;
      var satir = dizi(t.querySelectorAll('tbody > tr'));
      if (satir.length <= LIMIT) continue;

      t.setAttribute('data-dh-kirpildi', '1');
      t.className += ' dh-stand--kirpik';
      for (j = LIMIT; j < satir.length; j++) satir[j].className += ' dh-stand__gizli';

      var sar = t.parentNode;                            /* .dh-stand__wrap */
      var kap = sar && sar.parentNode ? sar.parentNode : null;
      if (!kap) continue;

      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'dh-standmore';
      btn.setAttribute('aria-expanded', 'false');
      var id = t.id || ('dh-stand-' + (++sayac));
      t.id = id;
      btn.setAttribute('aria-controls', id);
      btn.innerHTML = '<span class="dh-standmore__txt">Tümünü Gör</span>' +
        '<span class="dh-standmore__say">' + satir.length + ' sıra</span>' +
        '<i class="fas fa-chevron-down dh-standmore__ok" aria-hidden="true"></i>';
      kap.insertBefore(btn, sar.nextSibling);

      (function (tablo2, dugme, satirlar) {
        dugme.addEventListener('click', function () {
          var acik = dugme.getAttribute('aria-expanded') === 'true';
          var k;
          for (k = LIMIT; k < satirlar.length; k++) {
            satirlar[k].className = acik
              ? satirlar[k].className + ' dh-stand__gizli'
              : satirlar[k].className.replace(/\s*dh-stand__gizli/g, '');
          }
          dugme.setAttribute('aria-expanded', acik ? 'false' : 'true');
          dugme.className = acik ? 'dh-standmore' : 'dh-standmore is-open';
          tablo2.className = acik
            ? tablo2.className + ' dh-stand--kirpik'
            : tablo2.className.replace(/\s*dh-stand--kirpik/g, '');
          var yazi = dugme.querySelector('.dh-standmore__txt');
          if (yazi) yazi.textContent = acik ? 'Tümünü Gör' : 'Daha Az Göster';
        });
      }(t, btn, satir));
    }
  }

  /* ---------- 3) Kompakt lig seçici ---------- */

  function ligSecKur(kok) {
    var pick = kok.querySelector('[data-dh-lgpick]');
    if (!pick || pick.getAttribute('data-dh-kompakt')) return;
    var kutu = pick.querySelector('[data-dh-leagues]');
    var satir = pick.querySelector('.dh-lgpick__line--sel');
    if (!kutu || !satir) return;

    var sezon = satir.querySelector('[data-dh-sezon]');
    var sezonKap = sezon ? sezon.parentNode : null;

    var etiket = document.createElement('label');
    etiket.className = 'dh-pick dh-pick--lig';
    var yazi = document.createElement('span');
    yazi.className = 'dh-pick__lbl';
    yazi.appendChild(document.createTextNode('Lig'));
    var sel = document.createElement('select');
    sel.className = 'dh-pick__sel dh-pick__sel--lig';
    sel.setAttribute('aria-label', 'Lig');
    etiket.appendChild(yazi);
    etiket.appendChild(sel);

    if (sezonKap && sezonKap.parentNode === satir) satir.insertBefore(etiket, sezonKap);
    else satir.appendChild(etiket);

    function tazele() {
      var cip = dizi(kutu.querySelectorAll('[data-lig]')).filter(function (c) { return !c.hidden; });
      var i;
      sel.innerHTML = '';
      for (i = 0; i < cip.length; i++) {
        var o = document.createElement('option');
        o.value = cip[i].getAttribute('data-lig');
        o.appendChild(document.createTextNode((cip[i].textContent || '').replace(/^\s+|\s+$/g, '')));
        if (cip[i].getAttribute('aria-checked') === 'true') o.selected = true;
        sel.appendChild(o);
      }
      sel.disabled = !cip.length;
    }

    sel.addEventListener('change', function () {
      var c = kutu.querySelector('[data-lig="' + sel.value + '"]');
      if (c) c.click();
    });
    /* Çip ya da ülke kutusu değiştiğinde dh-tabs.js önce çalışsın diye
       kuyruğun sonuna atılır (script sırası: dh-tabs.js ÖNCE bağlanır). */
    kutu.addEventListener('click', function () { setTimeout(tazele, 0); });
    var ulke = pick.querySelector('[data-dh-ulke]');
    if (ulke) ulke.addEventListener('change', function () { setTimeout(tazele, 0); });

    tazele();
    pick.className += ' dh-lgpick--kompakt';
    pick.setAttribute('data-dh-kompakt', '1');
  }

  /* ---------- 4) Fikstür hafta geçişi ---------- */

  function adOku(el) {
    var i, c = el.childNodes;
    for (i = c.length - 1; i >= 0; i--) {
      if (c[i].nodeType === 3 && /\S/.test(c[i].nodeValue)) return c[i].nodeValue.replace(/^\s+|\s+$/g, '');
    }
    return (el.textContent || '').replace(/^\s+|\s+$/g, '');
  }
  function adYaz(el, ad) {
    var i, c = el.childNodes;
    for (i = c.length - 1; i >= 0; i--) {
      if (c[i].nodeType === 3 && /\S/.test(c[i].nodeValue)) { c[i].nodeValue = ad; return; }
    }
    el.appendChild(document.createTextNode(ad));
  }

  /* "35. Hafta · Cumartesi, 17 Mayıs" -> {hafta:35, gun:'Cumartesi', t:17, ay:4} */
  function gunCoz(metin) {
    var m = /^\s*(\d+)\.\s*Hafta\s*[··]\s*([^,]+),\s*(\d+)\s+(\S+)\s*$/.exec(metin || '');
    if (!m) return null;
    var ay = AY.indexOf(m[4]);
    if (ay < 0) return null;
    return { hafta: parseInt(m[1], 10), gun: m[2].replace(/^\s+|\s+$/g, ''), t: parseInt(m[3], 10), ay: ay };
  }

  function fiksturKur(kok) {
    var kaplar = dizi((kok || document).querySelectorAll('[data-dh-lg="fikstur"]')), i;
    for (i = 0; i < kaplar.length; i++) tekFikstur(kaplar[i]);
  }

  function tekFikstur(kap) {
    if (kap.getAttribute('data-dh-hafta-kuruldu')) return;
    var fx = kap.querySelector('.dh-fx');
    if (!fx) return;

    /* Gün grupları ve maç satırları sırayla okunur. */
    var gruplar = [], satirlar = [], son = null, i;
    var cocuklar = dizi(fx.children);
    for (i = 0; i < cocuklar.length; i++) {
      var el = cocuklar[i];
      var s = ' ' + el.className + ' ';
      if (s.indexOf(' dh-fx__day ') >= 0) {
        var lbl = el.querySelector('.dh-fx__daylbl');
        var coz = lbl ? gunCoz(lbl.textContent) : null;
        if (!coz) return;                                  /* tanımadığımız biçim: dokunma */
        son = { lbl: lbl, coz: coz };
        gruplar.push(son);
      } else if (s.indexOf(' dh-fx__row ') >= 0) {
        var yanlar = el.querySelectorAll('.dh-fx__side');
        if (yanlar.length < 2) continue;
        satirlar.push({ ev: adOku(yanlar[0]), depEl: yanlar[1], dep: adOku(yanlar[1]) });
      }
    }
    if (!gruplar.length || satirlar.length < 3) return;

    var taban = gruplar[0].coz.hafta;

    var nav = document.createElement('div');
    nav.className = 'dh-wknav';
    nav.setAttribute('role', 'group');
    nav.setAttribute('aria-label', 'Hafta seçimi');
    nav.innerHTML =
      '<button type="button" class="dh-wknav__btn" data-dh-wk="-1" aria-label="Önceki hafta">' +
      '<i class="fas fa-chevron-left" aria-hidden="true"></i></button>' +
      '<span class="dh-wknav__lbl" data-dh-wklbl aria-live="polite">' + taban + '. Hafta</span>' +
      '<button type="button" class="dh-wknav__btn" data-dh-wk="1" aria-label="Sonraki hafta">' +
      '<i class="fas fa-chevron-right" aria-hidden="true"></i></button>';
    kap.insertBefore(nav, fx);

    var etiketEl = nav.querySelector('[data-dh-wklbl]');
    var dugmeler = dizi(nav.querySelectorAll('[data-dh-wk]'));
    var kayma = 0;

    function uygula(d) {
      var n = satirlar.length, j, k;
      var alt = Math.max(1, taban - HAFTA_MENZIL) - taban;
      var ust = taban + HAFTA_MENZIL - taban;
      if (d < alt) d = alt;
      if (d > ust) d = ust;
      kayma = d;

      /* gün etiketleri: ±7 gün. Hafta günü adı 7'nin katında değişmez,
         bu yüzden gün adı KORUNUR, yalnız gün/ay yeniden hesaplanır. */
      for (j = 0; j < gruplar.length; j++) {
        var c = gruplar[j].coz;
        var t = new Date(2026, c.ay, c.t);
        t.setDate(t.getDate() + 7 * d);
        gruplar[j].lbl.textContent = (taban + d) + '. Hafta · ' + c.gun + ', ' +
          t.getDate() + ' ' + AY[t.getMonth()];
      }

      /* eşleşmeler: deplasman listesi d kadar dönüşümlü kaydırılır */
      var yeni = [];
      for (j = 0; j < n; j++) yeni.push(satirlar[((j + d) % n + n) % n].dep);
      for (j = 0; j < n; j++) {
        if (yeni[j] === satirlar[j].ev) {                /* takım kendisiyle eşleşemez */
          k = (j + 1) % n;
          var g = yeni[j]; yeni[j] = yeni[k]; yeni[k] = g;
        }
      }
      for (j = 0; j < n; j++) adYaz(satirlar[j].depEl, yeni[j]);

      etiketEl.textContent = (taban + d) + '. Hafta';
      for (j = 0; j < dugmeler.length; j++) {
        var yon = parseInt(dugmeler[j].getAttribute('data-dh-wk'), 10);
        dugmeler[j].disabled = (yon < 0 && d <= alt) || (yon > 0 && d >= ust);
      }
      kap.setAttribute('data-dh-hafta', String(taban + d));
    }

    for (i = 0; i < dugmeler.length; i++) {
      (function (b) {
        b.addEventListener('click', function () {
          uygula(kayma + parseInt(b.getAttribute('data-dh-wk'), 10));
        });
      }(dugmeler[i]));
    }

    kap.setAttribute('data-dh-hafta-kuruldu', '1');
    uygula(0);
  }

  /* ---------- yeniden çizimi izle ---------- */

  function izle() {
    if (!window.MutationObserver) return;
    var hedefler = dizi(document.querySelectorAll('[data-dh-lg]')), i;
    if (!hedefler.length) return;
    var gozcu = new MutationObserver(function (kayitlar) {
      if (kilit) return;
      kilit = true;
      try {
        var gorulen = [], j;
        for (j = 0; j < kayitlar.length; j++) {
          var h = kayitlar[j].target;
          if (gorulen.indexOf(h) < 0) gorulen.push(h);
        }
        for (j = 0; j < gorulen.length; j++) {
          gorulen[j].removeAttribute('data-dh-hafta-kuruldu');
          baglantila(gorulen[j]);
          kirp(gorulen[j]);
          if (gorulen[j].getAttribute('data-dh-lg') === 'fikstur') tekFikstur(gorulen[j]);
        }
      } finally {
        setTimeout(function () { kilit = false; }, 0);
      }
    });
    for (i = 0; i < hedefler.length; i++) gozcu.observe(hedefler[i], { childList: true });
  }

  /* ---------- kurulum ---------- */

  function kur() {
    baglantila(document);
    kirp(document);
    var lig = dizi(document.querySelectorAll('[data-dh-lig]')), i;
    for (i = 0; i < lig.length; i++) ligSecKur(lig[i]);
    fiksturKur(document);
    izle();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', kur);
  } else {
    kur();
  }
}());
