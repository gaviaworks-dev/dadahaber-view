/* dh-firsat.js — Gelecek / Fırsatlar ve Başvurular süzgeci (v2 · B)
   Yeni kütüphane yok, saf vanilla JS.

   dh-astro.js / dh-kadin.js / dh-gebelik.js ile AYNI sözleşme:
     Veri kaynağı : <script type="application/json" id="dh-firsat-data">
     Süzgeç kabı  : [data-dh-firsat-grup="tur|kime|zaman"] (role="radiogroup")
     Liste        : [data-dh-firsat-liste]
     Sayaç        : [data-dh-firsat-sayi]  (aria-live="polite")
     Boş durum    : [data-dh-firsat-bos]
   Backend gelince YALNIZ JSON bloğu değişir; işaretleme aynı kalır.

   JSON şeması:
   {
     "bugun": "2026-08-21",          // referans gün (backend'de sunucu günü)
     "yakinGun": 10,                 // "son günler" eşiği
     "turler":  [{"k":"burs","ad":"Burs"}, ...],
     "kime":    [{"k":"universite","ad":"Üniversite öğrencisi"}, ...],
     "zaman":   [{"k":"tumu","ad":"Tümü"},{"k":"7","ad":"7 gün içinde"}, ...],
     "kayitlar":[{
        "ad":"...", "kurum":"...", "tur":"burs",
        "kime":["lise","universite"], "son":"2026-09-15",
        "yer":"Çevrim içi", "link":"haber-detay.html", "yeni":true
     }, ...]
   }

   Not: süzgeç çipleri SAYFA değil VERİ değiştiriyor; HANDOFF R7 kararına göre
   role="radiogroup" + role="radio" kullanılıyor (tablist/tab DEĞİL). */
(function () {
  'use strict';

  var node = document.getElementById('dh-firsat-data');
  if (!node) return;

  var DATA;
  try { DATA = JSON.parse(node.textContent); } catch (e) { return; }

  var liste = document.querySelector('[data-dh-firsat-liste]');
  if (!liste) return;

  var sayiEl = document.querySelector('[data-dh-firsat-sayi]');
  var bosEl = document.querySelector('[data-dh-firsat-bos]');

  var AY = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara'];
  var GUN_MS = 86400000;
  var YAKIN = typeof DATA.yakinGun === 'number' ? DATA.yakinGun : 10;

  /* Tarihler UTC olarak çözülüyor; yaz saati kaymasıyla bir gün oynamasın. */
  function gun(s) {
    var p = String(s || '').split('-');
    return Date.UTC(+p[0], (+p[1] || 1) - 1, +p[2] || 1);
  }

  var BUGUN = gun(DATA.bugun || new Date().toISOString().slice(0, 10));

  var SECIM = { tur: 'tumu', kime: 'tumu', zaman: 'tumu' };

  /* ---------------------------------------------------------------- çipler */
  function chip(grup, k, ad, secili) {
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'dh-firsat__chip';
    b.setAttribute('role', 'radio');
    b.setAttribute('aria-checked', secili ? 'true' : 'false');
    b.setAttribute('tabindex', secili ? '0' : '-1');
    b.setAttribute('data-dh-firsat-deger', k);
    b.textContent = ad;
    b.addEventListener('click', function () { sec(grup, k); });
    return b;
  }

  function kurGrup(grup, ogeler) {
    var kap = document.querySelector('[data-dh-firsat-grup="' + grup + '"]');
    if (!kap) return null;
    var liste = [{ k: 'tumu', ad: 'Tümü' }].concat(ogeler || []);
    for (var i = 0; i < liste.length; i++) {
      kap.appendChild(chip(grup, liste[i].k, liste[i].ad, liste[i].k === SECIM[grup]));
    }
    kap.addEventListener('keydown', function (e) {
      var d = e.key === 'ArrowRight' || e.key === 'ArrowDown' ? 1
            : e.key === 'ArrowLeft' || e.key === 'ArrowUp' ? -1 : 0;
      if (!d && e.key !== 'Home' && e.key !== 'End') return;
      e.preventDefault();
      var ch = [].slice.call(kap.querySelectorAll('[data-dh-firsat-deger]'));
      var i = ch.indexOf(document.activeElement);
      if (i < 0) i = 0;
      var h = e.key === 'Home' ? 0
            : e.key === 'End' ? ch.length - 1
            : (i + d + ch.length) % ch.length;
      sec(grup, ch[h].getAttribute('data-dh-firsat-deger'));
      ch[h].focus();
    });
    return kap;
  }

  function sec(grup, k) {
    SECIM[grup] = k;
    var kap = document.querySelector('[data-dh-firsat-grup="' + grup + '"]');
    if (kap) {
      var ch = kap.querySelectorAll('[data-dh-firsat-deger]');
      for (var i = 0; i < ch.length; i++) {
        var on = ch[i].getAttribute('data-dh-firsat-deger') === k;
        ch[i].setAttribute('aria-checked', on ? 'true' : 'false');
        ch[i].setAttribute('tabindex', on ? '0' : '-1');
      }
    }
    ciz();
  }

  /* --------------------------------------------------------------- yardımcı */
  function ad(dizi, k) {
    for (var i = 0; i < (dizi || []).length; i++) if (dizi[i].k === k) return dizi[i].ad;
    return k;
  }

  function kimeMetni(ks) {
    var o = [];
    for (var i = 0; i < (ks || []).length; i++) o.push(ad(DATA.kime, ks[i]));
    return o.join(', ');
  }

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }

  function ikon(cls) {
    var i = document.createElement('i');
    i.className = cls;
    i.setAttribute('aria-hidden', 'true');
    return i;
  }

  /* ----------------------------------------------------------------- çizim */
  function ciz() {
    var kayitlar = (DATA.kayitlar || []).slice().sort(function (a, b) {
      return gun(a.son) - gun(b.son);
    });

    liste.innerHTML = '';
    var n = 0;

    for (var i = 0; i < kayitlar.length; i++) {
      var r = kayitlar[i];
      if (SECIM.tur !== 'tumu' && r.tur !== SECIM.tur) continue;
      if (SECIM.kime !== 'tumu' && (r.kime || []).indexOf(SECIM.kime) < 0) continue;

      var kalan = Math.round((gun(r.son) - BUGUN) / GUN_MS);
      if (SECIM.zaman !== 'tumu' && kalan > +SECIM.zaman) continue;

      n++;

      var it = el('li', 'dh-firsat__it');
      var yakin = kalan <= YAKIN;
      if (yakin) it.className += ' is-yakin';
      else if (r.yeni) it.className += ' is-yeni';
      /* "yeni eklendi" bilgisi renkle DEĞİL metinle veriliyor (bkz. B10) */

      /* tarih bloğu */
      var d = new Date(gun(r.son));
      var tar = el('span', 'dh-firsat__tarih');
      tar.appendChild(el('b', 'dh-firsat__gun', String(d.getUTCDate())));
      tar.appendChild(el('span', 'dh-firsat__ay', AY[d.getUTCMonth()]));
      it.appendChild(tar);

      /* başlık */
      var h = el('h4', 'dh-firsat__ad');
      var a = el('a', null, r.ad);
      a.setAttribute('href', r.link || 'haber-detay.html');
      h.appendChild(a);
      it.appendChild(h);

      /* meta: tür + kurum + kime uygun + yer */
      var m = el('span', 'dh-firsat__meta');
      m.appendChild(el('span', 'dh-firsat__tur', ad(DATA.turler, r.tur)));
      if (r.kurum) m.appendChild(el('span', null, r.kurum));
      var kime = el('span', 'dh-firsat__kime');
      kime.appendChild(ikon('fas fa-user-graduate'));
      kime.appendChild(el('span', null, kimeMetni(r.kime)));
      m.appendChild(kime);
      if (r.yer) {
        var yer = el('span', 'dh-firsat__kime');
        yer.appendChild(ikon('fas fa-location-dot'));
        yer.appendChild(el('span', null, r.yer));
        m.appendChild(yer);
      }
      if (r.yeni && !yakin) {
        var yn = el('span', 'dh-firsat__yeni');
        yn.appendChild(ikon('fas fa-circle-plus'));
        yn.appendChild(el('span', null, 'Yeni eklendi'));
        m.appendChild(yn);
      }
      it.appendChild(m);

      /* kalan gün — renk tek başına bilgi taşımıyor, metin de söylüyor */
      var kal = el('span', 'dh-firsat__kal');
      kal.appendChild(ikon(yakin ? 'fas fa-hourglass-end' : 'fas fa-hourglass-half'));
      kal.appendChild(el('span', null,
        kalan < 0 ? 'Başvuru kapandı'
          : kalan === 0 ? 'Bugün son gün'
          : kalan === 1 ? 'Son 1 gün'
          : yakin ? 'Son ' + kalan + ' gün'
          : kalan + ' gün kaldı'));
      it.appendChild(kal);

      liste.appendChild(it);
    }

    if (sayiEl) {
      sayiEl.innerHTML = '';
      sayiEl.appendChild(el('b', null, String(n)));
      sayiEl.appendChild(document.createTextNode(
        ' fırsat listeleniyor · ' + (DATA.kayitlar || []).length + ' kayıt içinde'));
    }
    if (bosEl) bosEl.hidden = n > 0;
  }

  kurGrup('tur', DATA.turler);
  kurGrup('kime', DATA.kime);
  kurGrup('zaman', DATA.zaman);
  ciz();
})();
