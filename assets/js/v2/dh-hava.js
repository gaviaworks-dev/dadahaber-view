/* ============================================================================
   Dada Haber v2 — Hava Durumu (hava-durumu.html)

   VERİ SÖZLEŞMESİ
     <script type="application/json" id="dh-hava-data"> içinde:
     { varsayilan:"istanbul",
       iller:{ <anahtar>: { ad, bolge, plaka, ilceler:[ad,...],
                            simdi:{...}, saatlik:[...], gunluk:[...],
                            uyari:{...}|null } } }

   Sayfada tek durum var: seçili il + seçili ilçe. İlçe değişince yalnız
   sapma uygulanır (ilçe indisine bağlı deterministik kayma) — prototip
   olduğu için ayrı ilçe verisi tutulmuyor, bu dosyada da öyle yazıyor.

   Bileşen sözleşmesi iller.html'deki dh-bolge.js ile aynı desende:
   kökte data-dh-hava, hedefler data-dh-hava-* nitelikleriyle bulunur.
   ========================================================================== */
(function () {
  'use strict';

  var KOK = document.querySelector('[data-dh-hava]');
  if (!KOK) return;

  var ham = document.getElementById('dh-hava-data');
  if (!ham) return;
  var VERI;
  try { VERI = JSON.parse(ham.textContent); } catch (e) { return; }

  var iller = VERI.iller || {};
  var secili = VERI.varsayilan;
  var ilce = 0;

  var YON = ['K', 'KD', 'D', 'GD', 'G', 'GB', 'B', 'KB'];

  /* Saatlik şerit ve yedi günlük tablo AYRI <section>'larda; kökün
     dışındalar. Ölçüldü: KOK.querySelector ikisini de bulamıyordu,
     iki blok boş kalıyordu. Önce kök içinde, bulamazsa belgede aranır. */
  function el(sel) { return KOK.querySelector(sel) || document.querySelector(sel); }
  function hepsi(sel) {
    var i = KOK.querySelectorAll(sel);
    return i.length ? i : document.querySelectorAll(sel);
  }

  /* İlçe sapması: prototipte ayrı ilçe verisi yok. Merkeze göre
     deterministik ve küçük bir kayma uygulanır ki seçim görünür olsun
     ama veri gerçekmiş gibi durmasın. */
  function sapma(i) { return i === 0 ? 0 : ((i % 5) - 2); }

  function yaz(hedef, deger) {
    var d = el('[data-dh-hava-' + hedef + ']');
    if (d) d.textContent = deger;
  }

  function ciz() {
    var v = iller[secili];
    if (!v) return;
    var s = sapma(ilce);
    var ilceAd = v.ilceler[ilce] || v.ilceler[0];

    /* REVİZE (22 Ağustos gecesi): "il seçtikten sonra detayları
       verebilecek şekilde işlem yapabilir." Alt bölümler (Saatlik Seyir,
       Yedi Günlük Tahmin) artık seçili ilin adını taşıyor — okur
       aşağı indiğinde hangi ilin verisine baktığını kaybetmiyor. */
    yaz('ad', v.ad);
    yaz('ad2', v.ad);
    yaz('ad3', v.ad);
    yaz('ilcead', ilceAd);
    yaz('ilcead2', ilceAd);
    yaz('kapsam', v.bolge + ' · Plaka ' + v.plaka + ' · ' + v.ilceler.length + ' ilçe');

    var n = v.simdi;
    yaz('derece', (n.derece + s) + '°');
    yaz('durum', n.durum);
    yaz('hissedilen', (n.hissedilen + s) + '°');
    yaz('nem', '%' + n.nem);
    yaz('ruzgar', n.ruzgar + ' km/s ' + YON[n.yon % 8]);
    yaz('basinc', n.basinc + ' hPa');
    yaz('gorus', n.gorus + ' km');
    yaz('yagis', '%' + n.yagis);
    yaz('dogus', n.dogus);
    yaz('batis', n.batis);
    yaz('guncel', n.guncel);

    // saatlik şerit
    var sr = el('[data-dh-hava-saatlik]');
    if (sr) {
      sr.innerHTML = v.saatlik.map(function (h) {
        return '<li class="dh-hv__sa">'
          + '<span class="dh-hv__saat">' + h.saat + '</span>'
          + '<span class="dh-hv__ikon" aria-hidden="true"><i class="fas ' + h.ikon + '"></i></span>'
          + '<span class="dh-hv__sd">' + (h.derece + s) + '°</span>'
          + '<span class="dh-hv__sy">%' + h.yagis + '</span></li>';
      }).join('');
    }

    // günlük tablo
    var gv = el('[data-dh-hava-gunluk]');
    if (gv) {
      gv.innerHTML = v.gunluk.map(function (g) {
        return '<tr><th scope="row" class="dh-hv__gun"><b>' + g.gun + '</b><small>' + g.tarih + '</small></th>'
          + '<td class="dh-hv__gd"><i class="fas ' + g.ikon + '" aria-hidden="true"></i> ' + g.durum + '</td>'
          + '<td class="dh-hv__gy">%' + g.yagis + '</td>'
          + '<td class="dh-hv__gr">' + g.ruzgar + ' km/s</td>'
          + '<td class="dh-hv__gmax"><b>' + (g.max + s) + '°</b></td>'
          + '<td class="dh-hv__gmin">' + (g.min + s) + '°</td></tr>';
      }).join('');
    }

    // uyarı
    var uy = el('[data-dh-hava-uyari]');
    if (uy) {
      if (v.uyari) {
        uy.hidden = false;
        uy.setAttribute('data-lv', v.uyari.seviye);
        uy.querySelector('[data-dh-hava-uyari-lv]').textContent = v.uyari.etiket;
        uy.querySelector('[data-dh-hava-uyari-tx]').textContent = v.uyari.metin;
      } else {
        uy.hidden = true;
      }
    }

    // ilçe çipleri
    var ic = el('[data-dh-hava-ilceler]');
    if (ic) {
      ic.innerHTML = v.ilceler.map(function (ad, i) {
        return '<button type="button" class="dh-hv__ilce' + (i === ilce ? ' is-on' : '')
          + '" role="radio" aria-checked="' + (i === ilce) + '" data-dh-hava-ilce="' + i + '">'
          + ad + '</button>';
      }).join('');
    }

    // ızgara seçili durumu
    hepsi('[data-dh-hava-sec]').forEach(function (g) {
      var on = g.getAttribute('data-dh-hava-sec') === secili;
      g.classList.toggle('is-on', on);
      g.setAttribute('aria-checked', on ? 'true' : 'false');
      g.setAttribute('tabindex', on ? '0' : '-1');
    });

    // arama alanı
    var ar = el('[data-dh-hava-ara]');
    if (ar && document.activeElement !== ar) ar.value = '';
  }

  KOK.addEventListener('click', function (e) {
    var g = e.target.closest ? e.target.closest('[data-dh-hava-sec]') : null;
    if (g) {
      secili = g.getAttribute('data-dh-hava-sec');
      ilce = 0;
      ciz();
      return;
    }
    var b = e.target.closest ? e.target.closest('[data-dh-hava-ilce]') : null;
    if (b) {
      ilce = +b.getAttribute('data-dh-hava-ilce') || 0;
      ciz();
    }
  });

  KOK.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    var g = e.target.closest ? e.target.closest('[data-dh-hava-sec]') : null;
    if (!g) return;
    e.preventDefault();
    secili = g.getAttribute('data-dh-hava-sec');
    ilce = 0;
    ciz();
  });

  // il arama
  var ara = el('[data-dh-hava-ara]');
  if (ara) {
    ara.addEventListener('input', function () {
      var q = ara.value.trim().toLowerCase();
      var sayac = 0;
      hepsi('[data-dh-hava-sec]').forEach(function (g) {
        var ad = (g.getAttribute('data-ad') || '').toLowerCase();
        var pl = g.getAttribute('data-plaka') || '';
        var uyar = !q || ad.indexOf(q) === 0 || pl === q;
        g.style.opacity = uyar ? '' : '.22';
        g.style.pointerEvents = uyar ? '' : 'none';
        if (uyar) sayac++;
      });
      var sn = el('[data-dh-hava-sayac]');
      if (sn) sn.textContent = sayac;
    });
    ara.addEventListener('keydown', function (e) {
      if (e.key !== 'Enter') return;
      e.preventDefault();
      var ilk = [].slice.call(hepsi('[data-dh-hava-sec]')).filter(function (g) {
        return g.style.pointerEvents !== 'none';
      })[0];
      if (ilk) { secili = ilk.getAttribute('data-dh-hava-sec'); ilce = 0; ciz(); }
    });
  }

  ciz();
})();
