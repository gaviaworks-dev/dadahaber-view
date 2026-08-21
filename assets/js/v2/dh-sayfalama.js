/* dh-sayfalama.js — liste sayfalarında ÇALIŞAN sayfalama ve "daha fazla yükle"
   Talimat madde 15: "Butonlar, sekmeler, açılır menüler ve sayfa bağlantıları
   yalnızca görsel olarak bulunmamalı; frontend seviyesinde çalışmalıdır."

   İki bileşen:
   1) .dh-pager — kendi bölümündeki kartları sayfalar. Sayfa sayısı işaretlemeden
      DEĞİL, gerçek kart sayısından hesaplanır; numaralar yeniden yazılır ki
      kullanıcıya yalan söylemesin.
   2) [data-dh-daha] — listeyi kademeli açar; biterken düğme kendini kapatır.

   Kart gizlenir, silinmez: JS kapalıysa liste tam görünür, veri kaybı olmaz.
   Yeni kütüphane yok, vanilla ES5. */
(function () {
  'use strict';

  /* Sayfa boyu sabit değil: liste kaç karttan oluşuyorsa 2–4 sayfa çıkacak
     şekilde hesaplanır. Sabit 8 verildiğinde 6 kartlık bölümlerde tek sayfa
     kalıp sayfalayıcı hiç kurulmuyordu (ölçümde yakalandı). */
  function sayfaBoyu(toplam) {
    var sayfa = Math.min(4, Math.max(2, Math.round(toplam / 6)));
    return Math.ceil(toplam / sayfa);
  }

  function dizi(n) { return Array.prototype.slice.call(n); }

  /* Sayfalayıcının yönettiği kart kümesini bul.
     Kartlar kabın DOĞRUDAN çocuğu olmak zorunda değil: ölçümde 6 makalenin
     altısı da tek bir sarmalayıcının içindeydi ve liste hiç kurulmuyordu.
     Bu yüzden her makale, "yalnız kendisini içeren" en dış ataya kadar
     yükseltilir; birden fazla makale barındıran seviyede durur. */
  function gizlenecek(makale, kap) {
    var n = makale;
    while (n.parentElement && n.parentElement !== kap &&
           n.parentElement.querySelectorAll('article').length === 1) {
      n = n.parentElement;
    }
    return n;
  }

  function listeBul(baslangic) {
    var k = baslangic;
    while (k && k.parentElement && k.parentElement !== document.body) {
      var kap = k.parentElement;
      var makaleler = dizi(kap.querySelectorAll('article'));
      if (makaleler.length >= 4) {
        var kartlar = [];
        for (var i = 0; i < makaleler.length; i++) {
          var h = gizlenecek(makaleler[i], kap);
          if (kartlar.indexOf(h) === -1) kartlar.push(h);
        }
        if (kartlar.length >= 4) return { kap: kap, kartlar: kartlar };
      }
      k = kap;
    }
    return null;
  }

  function pagerKur(pager) {
    var liste = listeBul(pager);
    if (!liste) return;
    var kartlar = liste.kartlar;
    var toplam = kartlar.length;
    if (toplam < 4) { pager.hidden = true; return; }
    var SAYFA_BOY = sayfaBoyu(toplam);
    var sayfa_adet = Math.ceil(toplam / SAYFA_BOY);
    if (sayfa_adet < 2) { pager.hidden = true; return; }

    var durum = document.createElement('p');
    durum.className = 'dh-pager__durum';
    durum.setAttribute('role', 'status');
    durum.setAttribute('aria-live', 'polite');
    pager.parentNode.insertBefore(durum, pager);

    function ciz(aktif) {
      /* kartlar */
      var bas = (aktif - 1) * SAYFA_BOY, son = Math.min(bas + SAYFA_BOY, toplam);
      for (var i = 0; i < toplam; i++) {
        kartlar[i].hidden = !(i >= bas && i < son);
      }
      durum.textContent = toplam + ' haberden ' + (bas + 1) + '–' + son + ' gösteriliyor · sayfa ' + aktif + '/' + sayfa_adet;

      /* sayfalayıcı yeniden yazılır */
      var h = [];
      var kenar = function (yon, etiket, kapali) {
        var ok = yon === 'geri' ? 'left' : 'right';
        var ic = '<i class="unicon-chevron-' + ok + '" aria-hidden="true"></i>';
        if (etiket.indexOf('İlk') === 0 || etiket.indexOf('Son') === 0) ic += ic;
        return kapali
          ? '<span class="dh-pager__nav is-off" aria-disabled="true" aria-label="' + etiket + '">' + ic + '</span>'
          : '<a class="dh-pager__nav" href="#" data-git="' + etiket + '" aria-label="' + etiket + '">' + ic + '</a>';
      };
      h.push(kenar('geri', 'İlk sayfa', aktif === 1));
      h.push(kenar('geri', 'Önceki sayfa', aktif === 1));
      for (var s = 1; s <= sayfa_adet; s++) {
        var yakin = Math.abs(s - aktif) <= 1 || s === 1 || s === sayfa_adet;
        if (!yakin) {
          if (h[h.length - 1].indexOf('dh-pager__gap') === -1) {
            h.push('<span class="dh-pager__gap" aria-hidden="true">…</span>');
          }
          continue;
        }
        h.push(s === aktif
          ? '<a class="dh-pager__pg is-on" href="#" aria-current="page" aria-label="Sayfa ' + s + '">' + s + '</a>'
          : '<a class="dh-pager__pg" href="#" data-sayfa="' + s + '" aria-label="Sayfa ' + s + '">' + s + '</a>');
      }
      h.push(kenar('ileri', 'Sonraki sayfa', aktif === sayfa_adet));
      h.push(kenar('ileri', 'Son sayfa', aktif === sayfa_adet));
      pager.innerHTML = h.join('\n');
      pager.setAttribute('data-aktif', String(aktif));
    }

    pager.addEventListener('click', function (e) {
      var t = e.target.closest ? e.target.closest('a') : null;
      if (!t || !pager.contains(t)) return;
      e.preventDefault();
      var aktif = parseInt(pager.getAttribute('data-aktif') || '1', 10);
      var hedef = aktif;
      if (t.hasAttribute('data-sayfa')) hedef = parseInt(t.getAttribute('data-sayfa'), 10);
      else {
        var g = t.getAttribute('data-git');
        if (g === 'İlk sayfa') hedef = 1;
        else if (g === 'Son sayfa') hedef = sayfa_adet;
        else if (g === 'Önceki sayfa') hedef = Math.max(1, aktif - 1);
        else if (g === 'Sonraki sayfa') hedef = Math.min(sayfa_adet, aktif + 1);
      }
      if (hedef === aktif) return;
      ciz(hedef);
      var ilk = kartlar[(hedef - 1) * SAYFA_BOY];
      if (ilk && ilk.scrollIntoView) ilk.scrollIntoView({ block: 'start', behavior: 'auto' });
      var odak = pager.querySelector('[aria-current="page"]');
      if (odak) odak.focus();
    });

    ciz(1);
  }

  /* --------------------------------------------------- daha fazla yükle */
  function dahaKur(dugme) {
    var liste = listeBul(dugme);
    if (!liste) return;
    var kartlar = liste.kartlar, toplam = kartlar.length;
    if (toplam < 6) return;
    /* ilk açılışta yarısı görünür, her tıkta üçte biri daha açılır */
    var ADIM = Math.max(3, Math.ceil(toplam / 3));
    var gorunur = Math.ceil(toplam / 2);

    function ciz() {
      for (var i = 0; i < toplam; i++) kartlar[i].hidden = i >= gorunur;
      var kalan = toplam - gorunur;
      var etiket = dugme.querySelector('span') || dugme;
      if (kalan <= 0) {
        etiket.textContent = 'Tüm haberler yüklendi';
        dugme.setAttribute('aria-disabled', 'true');
      } else {
        etiket.textContent = 'Daha fazla haber yükle (' + kalan + ')';
      }
    }
    dugme.addEventListener('click', function (e) {
      e.preventDefault();
      if (dugme.getAttribute('aria-disabled') === 'true') return;
      gorunur = Math.min(gorunur + ADIM, toplam);
      ciz();
    });
    ciz();
  }

  function kur() {
    dizi(document.querySelectorAll('.dh-pager')).forEach(pagerKur);
    dizi(document.querySelectorAll('[data-dh-daha]')).forEach(dahaKur);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', kur);
  else kur();
})();
