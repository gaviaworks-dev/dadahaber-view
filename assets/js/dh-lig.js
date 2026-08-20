/* dh-lig.js — Lig verisi işaretleme üreteci (R7-S)
   Yeni kütüphane yok, saf vanilla JS. ES5 sözdizimi.

   NEDEN AYRI DOSYA: aynı işaretlemeyi iki yer üretiyor —
   (1) build sırasında Node, sayfaya varsayılan ligin STATİK HTML'ini gömüyor
       (JS kapalıyken de tablo görünür, arama motoru da görür),
   (2) tarayıcıda lig değiştirildiğinde bu dosya yeniden üretiyor.
   Tek kaynak olmazsa iki taraf zamanla ayrışır. Bu yüzden tek modül,
   iki ortam: `module.exports` varsa Node, yoksa `window.DHLig`.

   İÇ TUTARLILIK: türetilen alanlar (O, P, AV, Y%, set oranı) burada
   HESAPLANIR, veriden okunmaz. Yer tutucu veri bile aritmetik olarak
   doğru kalır. Sayı biçimi Türkçe: ondalık ayracı virgül. */
(function (root, factory) {
  var api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.DHLig = api;
}(typeof window !== 'undefined' ? window : this, function () {
  'use strict';

  var EMBLEM = './assets/images/demo-six/emblems/logo-';

  /* Deterministik sözde-rastgele: aynı tohum -> aynı sayı dizisi.
     Geçmiş sezonları veriyi büyütmeden türetmek için. */
  function rng(seed) {
    var s = seed >>> 0 || 1;
    return function () {
      s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0;
      return s / 4294967296;
    };
  }
  function tohum(str) {
    var h = 2166136261, i;
    for (i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = (h * 16777619) >>> 0; }
    return h;
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  /* Türkçe sayı: ondalık ayracı virgül */
  function ond(n, basamak) {
    return Number(n).toFixed(basamak).replace('.', ',');
  }
  function isaretli(n) {
    return (n > 0 ? '+' : '') + n;
  }
  function crest(i) {
    var n = (i % 10) + 1;
    return EMBLEM + (n < 10 ? '0' + n : n) + '.svg';
  }

  /* ---- Sütun kümeleri: dala göre değişen tek şey budur.
     Lig değişimi sütunları DEĞİL veriyi değiştirir; dal değişimi sütunları. */
  var SUTUN = {
    futbol: {
      ad: 'Takım',
      kolon: [
        { k: 'o',  b: 'O',  t: 'Oynadığı maç' },
        { k: 'g',  b: 'G',  t: 'Galibiyet' },
        { k: 'b',  b: 'B',  t: 'Beraberlik' },
        { k: 'm',  b: 'M',  t: 'Mağlubiyet' },
        { k: 'a',  b: 'A',  t: 'Attığı gol', dim: true },
        { k: 'y',  b: 'Y',  t: 'Yediği gol', dim: true },
        { k: 'av', b: 'AV', t: 'Averaj' },
        { k: 'p',  b: 'P',  t: 'Puan', pts: true }
      ]
    },
    basketbol: {
      ad: 'Takım',
      kolon: [
        { k: 'o',  b: 'O',  t: 'Oynadığı maç' },
        { k: 'g',  b: 'G',  t: 'Galibiyet' },
        { k: 'm',  b: 'M',  t: 'Mağlubiyet' },
        { k: 'sa', b: 'SA', t: 'Attığı sayı', dim: true },
        { k: 'sy', b: 'SY', t: 'Yediği sayı', dim: true },
        { k: 'av', b: 'AV', t: 'Sayı averajı' },
        { k: 'yz', b: 'Y%', t: 'Galibiyet yüzdesi', pts: true }
      ]
    },
    voleybol: {
      ad: 'Takım',
      kolon: [
        { k: 'o',   b: 'O',    t: 'Oynadığı maç' },
        { k: 'g',   b: 'G',    t: 'Galibiyet' },
        { k: 'm',   b: 'M',    t: 'Mağlubiyet' },
        { k: 'sg',  b: 'SG',   t: 'Alınan set', dim: true },
        { k: 'sy',  b: 'SY',   t: 'Verilen set', dim: true },
        { k: 'sor', b: 'S.OR', t: 'Set oranı' },
        { k: 'p',   b: 'P',    t: 'Puan', pts: true }
      ]
    }
  };

  /* Türetilen alanlar burada hesaplanır — veriden okunmaz. */
  function turet(br, t) {
    var o = {};
    for (var k in t) o[k] = t[k];
    if (br === 'futbol') {
      o.o = t.g + t.b + t.m;
      o.p = t.g * 3 + t.b;
      o.av = t.a - t.y;
    } else if (br === 'basketbol') {
      o.o = t.g + t.m;
      o.av = t.sa - t.sy;
      o.yz = o.o ? t.g / o.o : 0;
    } else {
      /* Voleybol: set ve puan TÜRETİLİR, veriden okunmaz.
         Bir galibiyet 3 set alır, bir mağlubiyet 3 set verir.
         w2 = 3-2 kazanılan maç · l2 = 2-3 kaybedilen maç
         w1 = 3-1 kazanılan · l1 = 1-3 kaybedilen
         Alınan set  = 3G + 2*l2 + l1
         Verilen set = 3M + 2*w2 + w1
         Puan        = 3G - w2 + l2   (3-2 galibiyeti 2, 2-3 mağlubiyeti 1) */
      var w2 = t.w2 || 0, l2 = t.l2 || 0, w1 = t.w1 || 0, l1 = t.l1 || 0;
      o.o = t.g + t.m;
      o.sg = 3 * t.g + 2 * l2 + l1;
      o.sy = 3 * t.m + 2 * w2 + w1;
      o.sor = o.sy ? o.sg / o.sy : o.sg;
      o.p = 3 * t.g - w2 + l2;
    }
    return o;
  }

  /* ---- İç saha / deplasman ayrımı ----
     Kısıt: evO + depO = O ve her iki yarıda da G+B+M = o yarının O'su.
     Ev sahibi avantajı yer tutucu veride de gerçekçi olsun diye
     galibiyetlerin ~%60'ı, yenen gollerin ~%42'si iç sahaya düşer.
     Veriden okunmuyor, burada TÜRETİLİYOR: toplamla çelişmesi imkânsız. */
  function bol(toplam, yariO, oran) {
    var v = Math.round(toplam * oran);
    if (v > yariO) v = yariO;
    if (v > toplam) v = toplam;
    if (v < 0) v = 0;
    return v;
  }
  function yarim(br, t, ev) {
    var o = turet(br, t);
    var yariO = Math.ceil(o.o / 2);
    var digerO = o.o - yariO;
    var g = bol(o.g, yariO, 0.6);
    var b = br === 'futbol' ? bol(o.b, yariO - g, 0.55) : 0;
    var m = yariO - g - b;
    if (m < 0) { m = 0; }
    /* deplasman tarafı toplamın kalanı */
    var dg = o.g - g, db = (o.b || 0) - b, dm = (o.m) - m;
    /* kalan negatifse iç sahadan geri ver */
    while (dm < 0 && g > 0) { g--; dg++; m++; dm--; m--; dm++; break; }
    var y = { ad: t.ad, z: t.z, fav: t.fav };
    if (ev) {
      y.g = g; y.m = m; if (br === 'futbol') y.b = b;
      if (br === 'futbol') { y.a = bol(o.a, o.a, 0.58); y.y = bol(o.y, o.y, 0.42); }
      if (br === 'basketbol') { y.sa = Math.round(o.sa * 0.52); y.sy = Math.round(o.sy * 0.48); }
      if (br === 'voleybol') {
        y.w2 = bol(t.w2 || 0, g, 0.45); y.w1 = bol(t.w1 || 0, g - y.w2, 0.5);
        y.l2 = bol(t.l2 || 0, m, 0.4); y.l1 = bol(t.l1 || 0, m - y.l2, 0.5);
      }
    } else {
      y.g = dg < 0 ? 0 : dg; y.m = dm < 0 ? 0 : dm; if (br === 'futbol') y.b = db < 0 ? 0 : db;
      if (br === 'futbol') { y.a = o.a - bol(o.a, o.a, 0.58); y.y = o.y - bol(o.y, o.y, 0.42); }
      if (br === 'basketbol') { y.sa = o.sa - Math.round(o.sa * 0.52); y.sy = o.sy - Math.round(o.sy * 0.48); }
      if (br === 'voleybol') {
        y.w2 = Math.max(0, (t.w2 || 0) - bol(t.w2 || 0, o.g, 0.45));
        y.w1 = Math.max(0, (t.w1 || 0) - bol(t.w1 || 0, o.g, 0.5));
        y.l2 = Math.max(0, (t.l2 || 0) - bol(t.l2 || 0, o.m, 0.4));
        y.l1 = Math.max(0, (t.l1 || 0) - bol(t.l1 || 0, o.m, 0.5));
      }
    }
    /* yarıların toplamı tam O etsin */
    var top = y.g + y.m + (y.b || 0);
    var hedef = ev ? yariO : digerO;
    if (top !== hedef) y.m += hedef - top;
    if (y.m < 0) { y.g += y.m; y.m = 0; }
    if (br === 'voleybol') {
      if (y.w2 > y.g) y.w2 = y.g;
      if (y.w1 > y.g - y.w2) y.w1 = y.g - y.w2;
      if (y.l2 > y.m) y.l2 = y.m;
      if (y.l1 > y.m - y.l2) y.l1 = y.m - y.l2;
    }
    return y;
  }

  /* ---- Geçmiş sezon türetme ----
     Sezon başına ayrı veri taşımak yükü üçe katlardı (ölçüm: 82KB -> 246KB).
     Geçmiş sezonlar aynı kadrodan deterministik olarak türetiliyor:
     aynı lig + aynı sezon her zaman aynı tabloyu verir, aritmetik
     yine dh-lig.js'te hesaplandığı için iç tutarlılık bozulmaz.
     Backend bağlanınca bu fonksiyonun yerini sunucudan gelen sezon alır. */
  function sezonla(lig, sezon) {
    if (!sezon || sezon === lig.sezon) return lig;
    var r = rng(tohum(lig.ad + sezon));
    var kopya = {}, k;
    for (k in lig) kopya[k] = lig[k];
    kopya.sezon = sezon;
    kopya.kicker = lig.kicker + ' · ' + sezon;
    kopya.tablo = lig.tablo.map(function (t) {
      var o = {}, j;
      for (j in t) o[j] = t[j];
      var sap = function (v, pay) { return Math.max(0, Math.round(v + (r() - 0.5) * pay)); };
      var O = (t.g || 0) + (t.b || 0) + (t.m || 0);
      o.g = Math.min(O, sap(t.g, O * 0.28));
      o.b = t.b === undefined ? undefined : Math.min(O - o.g, sap(t.b, O * 0.22));
      o.m = O - o.g - (o.b || 0);
      if (t.a !== undefined) { o.a = sap(t.a, 14); o.y = sap(t.y, 14); }
      if (t.sa !== undefined) { o.sa = sap(t.sa, 90); o.sy = sap(t.sy, 90); }
      if (t.w2 !== undefined || t.l2 !== undefined) {
        o.w2 = Math.min(o.g, sap(t.w2 || 0, 3));
        o.w1 = Math.min(o.g - o.w2, sap(t.w1 || 0, 3));
        o.l2 = Math.min(o.m, sap(t.l2 || 0, 3));
        o.l1 = Math.min(o.m - o.l2, sap(t.l1 || 0, 3));
      }
      return o;
    });
    /* yeniden sırala ve bölge sınıflarını sıraya göre yeniden dağıt */
    var zonSira = lig.tablo.map(function (t) { return t.z || ''; });
    var fav = lig.tablo.filter(function (t) { return t.fav; })[0];
    kopya.tablo.sort(function (x, y) { return puan(lig.br, y) - puan(lig.br, x) || fark(lig.br, y) - fark(lig.br, x); });
    kopya.tablo = kopya.tablo.map(function (t, i) {
      var o = {}, j;
      for (j in t) o[j] = t[j];
      o.z = zonSira[i];
      o.fav = fav && t.ad === fav.ad ? 1 : 0;
      return o;
    });
    return kopya;
  }

  function puan(br, t) { var o = turet(br, t); return br === 'basketbol' ? o.yz * 1000 : o.p; }
  function fark(br, t) { var o = turet(br, t); return br === 'voleybol' ? o.sor * 100 : o.av; }

  /* ---- Paylaşılan sıra ----
     Lig kuralı: sıralama ölçütlerinin tamamında eşit olan takımlar
     aynı sırayı paylaşır, sonraki takım atlanan sıraları atlar
     (1, 2, 3, 4, 4, 6, 6, 8 ...). Referans ölçümünde de böyle. */
  function siralar(br, tablo) {
    var anahtar = tablo.map(function (t) {
      var o = turet(br, t);
      return br === 'futbol' ? [o.p, o.av, o.a].join('/')
        : br === 'basketbol' ? [o.yz.toFixed(4), o.av, o.sa].join('/')
        : [o.p, o.sor.toFixed(4), o.sg].join('/');
    });
    var out = [], son = null, sonSira = 0, i;
    for (i = 0; i < anahtar.length; i++) {
      if (anahtar[i] === son) out.push(sonSira);
      else { sonSira = i + 1; son = anahtar[i]; out.push(sonSira); }
    }
    return out;
  }

  function hucre(br, kol, t) {
    var v = t[kol.k];
    if (kol.k === 'av') return isaretli(v);
    if (kol.k === 'yz') return '%' + ond(v * 100, 1);
    if (kol.k === 'sor') return ond(v, 2);
    return String(v);
  }

  /* ---------- Puan durumu tablosu ----------
     gorunum: 'genel' | 'ev' | 'dep'  (referanstaki Genel / İç Saha / Deplasman) */
  function tablo(lig, gorunum) {
    var br = lig.br, S = SUTUN[br] || SUTUN.futbol, h = [], i, j;
    var kaynak = lig.tablo;
    if (gorunum === 'ev' || gorunum === 'dep') {
      kaynak = kaynak.map(function (t) { return yarim(br, t, gorunum === 'ev'); });
      kaynak = kaynak.slice().sort(function (x, y) {
        return puan(br, y) - puan(br, x) || fark(br, y) - fark(br, x);
      });
    }
    var sira = siralar(br, kaynak);

    h.push('<div class="dh-stand__wrap" tabindex="0" role="region" aria-label="' + esc(lig.ad) + ' puan durumu">');
    h.push('<table class="dh-stand" data-branch="' + esc(br) + '">');
    h.push('<caption class="dh-stand__cap">' + esc(lig.ad) + ' puan durumu</caption>');
    h.push('<thead><tr><th scope="col" class="dh-stand__c-rank"><abbr title="Sıra">#</abbr></th>');
    h.push('<th scope="col" class="dh-stand__c-name">' + esc(S.ad) + '</th>');
    for (j = 0; j < S.kolon.length; j++) {
      var kol = S.kolon[j];
      h.push('<th scope="col" class="' + (kol.dim ? 'is-dim' : (kol.pts ? 'dh-stand__pts' : '')) +
        '"><abbr title="' + esc(kol.t) + '">' + esc(kol.b) + '</abbr></th>');
    }
    h.push('</tr></thead><tbody>');

    for (i = 0; i < kaynak.length; i++) {
      var t = turet(br, kaynak[i]);
      var sinif = ['dh-stand__row'];
      if (t.z) sinif.push(t.z);
      if (t.fav) sinif.push('now');
      h.push('<tr class="' + sinif.join(' ') + '">');
      h.push('<th scope="row" class="dh-stand__c-rank"><span class="dh-rank' +
        (sira[i] === sira[i - 1] ? ' is-tie' : '') + '">' + sira[i] + '</span></th>');
      h.push('<td class="dh-stand__c-name"><span class="dh-stand__team">' +
        '<img class="dh-stand__crest" src="' + crest(i) + '" alt="" width="22" height="22" loading="lazy">' +
        '<span class="dh-stand__nm">' + esc(t.ad) + '</span></span></td>');
      for (j = 0; j < S.kolon.length; j++) {
        var k2 = S.kolon[j];
        h.push('<td class="' + (k2.dim ? 'is-dim' : (k2.pts ? 'dh-stand__pts' : '')) + '">' +
          esc(hucre(br, k2, t)) + '</td>');
      }
      h.push('</tr>');
    }
    h.push('</tbody></table></div>');

    /* Bölge şeridi lige göre değişir — açıklama da lige göre üretilir. */
    if (lig.zonlar && lig.zonlar.length) {
      h.push('<ul class="dh-legend">');
      for (i = 0; i < lig.zonlar.length; i++) {
        h.push('<li class="dh-legend__it ' + esc(lig.zonlar[i].k) + '">' +
          '<span class="dh-legend__key" aria-hidden="true"></span>' + esc(lig.zonlar[i].ad) + '</li>');
      }
      h.push('</ul>');
    }
    if (lig.not) {
      var ek = gorunum === 'ev' ? ' İç saha tablosu yalnız evinde oynanan maçları sayar.'
        : (gorunum === 'dep' ? ' Deplasman tablosu yalnız dışarıda oynanan maçları sayar.' : '');
      h.push('<p class="dh-note" data-branch="' + esc(br) + '"><i class="' + esc(lig.ikon || 'fas fa-futbol') +
        '" aria-hidden="true"></i><span>' + esc(lig.not + ek) + '</span></p>');
    }
    return h.join('');
  }

  /* ---------- Maç listesi (fikstür + sonuçlar ortak) ---------- */
  function macListesi(lig, mac, bitti) {
    var h = [], son = null, i;
    h.push('<div class="dh-fx">');
    h.push('<div class="dh-fx__cols" aria-hidden="true">' +
      '<span>Saat</span><span>Ev sahibi <i>–</i> Konuk</span><span>Nerede</span><span>' +
      (bitti ? 'Durum' : 'Yayın') + '</span></div>');
    for (i = 0; i < mac.length; i++) {
      var m = mac[i];
      if (m.gun !== son) {
        son = m.gun;
        h.push('<div class="dh-fx__day"><span class="dh-fx__daylbl">' +
          esc(lig.hafta) + ' · ' + esc(m.gun) + '</span></div>');
      }
      var sinif = ['dh-fx__row'];
      if (bitti) sinif.push('is-done');
      if (m.fav) sinif.push('is-fav');
      var evKazandi = bitti && m.es > m.ds, depKazandi = bitti && m.ds > m.es;
      h.push('<div class="' + sinif.join(' ') + '">');
      h.push('<span class="dh-fx__when">' + esc(m.saat) + '</span>');
      h.push('<span class="dh-fx__what">');
      h.push('<span class="dh-fx__side' + (evKazandi ? ' is-win' : '') + '">' + esc(m.ev) +
        (m.ha === 'EV' ? '<b class="dh-fx__ha">EV</b>' : '') + '</span>');
      h.push('<span class="dh-fx__vs">' + (bitti ? esc(m.es) + '&nbsp;–&nbsp;' + esc(m.ds) : '–') + '</span>');
      h.push('<span class="dh-fx__side dh-fx__side--away' + (depKazandi ? ' is-win' : '') + '">' +
        (m.ha === 'DEP' ? '<b class="dh-fx__ha">DEP</b>' : '') + esc(m.dep) + '</span>');
      h.push('</span>');
      h.push('<span class="dh-fx__meta"><i class="fas fa-map-marker-alt" aria-hidden="true"></i>' + esc(m.stat) + '</span>');
      h.push('<span class="dh-fx__state">' + esc(bitti ? m.durum : m.yayin) + '</span>');
      h.push('</div>');
    }
    h.push('</div>');
    return h.join('');
  }

  function fikstur(lig) { return macListesi(lig, lig.fikstur, false); }
  function sonuclar(lig) { return macListesi(lig, lig.sonuclar, true); }

  /* ---------- Kral / istatistik ---------- */
  function istatistik(lig) {
    var s = lig.istatistik, h = [], i, j;
    h.push('<div class="dh-stand__wrap" tabindex="0" role="region" aria-label="' + esc(lig.ad) + ' ' + esc(s.baslik) + '">');
    h.push('<table class="dh-stand dh-stand--stat" data-branch="' + esc(lig.br) + '">');
    h.push('<caption class="dh-stand__cap">' + esc(lig.ad) + ' ' + esc(s.baslik) + '</caption>');
    h.push('<thead><tr><th scope="col" class="dh-stand__c-rank"><abbr title="Sıra">#</abbr></th>' +
      '<th scope="col" class="dh-stand__c-name">Oyuncu</th>');
    for (j = 0; j < s.sut.length; j++) {
      h.push('<th scope="col" class="' + (j === s.sut.length - 1 && s.sut.length < 4 ? 'dh-stand__pts' : (j === 1 && s.sut.length >= 4 ? 'dh-stand__pts' : '')) +
        '">' + esc(s.sut[j]) + '</th>');
    }
    h.push('</tr></thead><tbody>');
    for (i = 0; i < s.satir.length; i++) {
      var r = s.satir[i];
      h.push('<tr class="dh-stand__row">');
      h.push('<th scope="row" class="dh-stand__c-rank"><span class="dh-rank">' + (i + 1) + '</span></th>');
      h.push('<td class="dh-stand__c-name"><span class="dh-stand__team">' +
        '<img class="dh-stand__crest" src="' + crest(i) + '" alt="" width="22" height="22" loading="lazy">' +
        '<span class="dh-stand__who"><span class="dh-stand__nm">' + esc(r.ad) + '</span>' +
        '<span class="dh-stand__club">' + esc(r.tk) + '</span></span></span></td>');
      for (j = 0; j < r.v.length; j++) {
        var pts = (r.v.length < 4 ? j === r.v.length - 1 : j === 1);
        h.push('<td class="' + (pts ? 'dh-stand__pts' : (j === 0 ? 'is-dim' : '')) + '">' + esc(r.v[j]) + '</td>');
      }
      h.push('</tr>');
    }
    h.push('</tbody></table></div>');
    return h.join('');
  }

  var BOLUM = { tablo: tablo, fikstur: fikstur, sonuclar: sonuclar, istatistik: istatistik };

  return {
    SUTUN: SUTUN,
    turet: turet,
    sezonla: sezonla,
    siralar: siralar,
    yarim: yarim,
    bolum: function (ad, lig, gorunum) { return (BOLUM[ad] || tablo)(lig, gorunum); },
    tablo: tablo,
    fikstur: fikstur,
    sonuclar: sonuclar,
    istatistik: istatistik
  };
}));
