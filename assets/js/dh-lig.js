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
      o.o = t.g + t.m;
      o.sor = t.sy ? t.sg / t.sy : t.sg;
    }
    return o;
  }

  function hucre(br, kol, t) {
    var v = t[kol.k];
    if (kol.k === 'av') return isaretli(v);
    if (kol.k === 'yz') return '%' + ond(v * 100, 1);
    if (kol.k === 'sor') return ond(v, 2);
    return String(v);
  }

  /* ---------- Puan durumu tablosu ---------- */
  function tablo(lig) {
    var br = lig.br, S = SUTUN[br] || SUTUN.futbol, h = [], i, j;

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

    for (i = 0; i < lig.tablo.length; i++) {
      var t = turet(br, lig.tablo[i]);
      var sinif = ['dh-stand__row'];
      if (t.z) sinif.push(t.z);
      if (t.fav) sinif.push('now');
      h.push('<tr class="' + sinif.join(' ') + '">');
      h.push('<th scope="row" class="dh-stand__c-rank"><span class="dh-rank">' + (i + 1) + '</span></th>');
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
      h.push('<p class="dh-note" data-branch="' + esc(br) + '"><i class="' + esc(lig.ikon || 'fas fa-futbol') +
        '" aria-hidden="true"></i><span>' + esc(lig.not) + '</span></p>');
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
    bolum: function (ad, lig) { return (BOLUM[ad] || tablo)(lig); },
    tablo: tablo,
    fikstur: fikstur,
    sonuclar: sonuclar,
    istatistik: istatistik
  };
}));
