/* dh-etki.js — "Bana Etkisi" seçicisi (kesfet.html#bana-etkisi)
   Yeni kütüphane yok, saf vanilla JS, ES5 sözdizimi.

   ORTAK SÖZLEŞME (dh-astro.js / dh-gebelik.js / dh-kadin.js ile aynı):
     Veri      : <script type="application/json" id="dh-etki-data">
     Seçenek   : button[data-dh-etki] · role="radio" · aria-checked
     Yazım yeri: [data-dh-etki-out="<alan>"]
   Backend gelince YALNIZ JSON bloğu değişir; işaretleme aynı kalır.

   ROL SEÇİMİ: seçenekler görünen bölümü değiştirmiyor, TEK panelin
   VERİSİNİ değiştiriyor. R7'de yazılan üç desenden ikincisi bu:
   role="radiogroup" + role="radio" + aria-checked. Tablist yanlış olurdu.

   VERİ SÖZLEŞMESİ
     {
       "gundem":  { "konu": "...", "baslik": "...", "tarih": "21.08.2026",
                    "kaynak": 4, "link": "haber-detay.html" },
       "varsayilan": "ogrenci",
       "durumlar": {
         "<anahtar>": {
           "ad": "Öğrenci",
           "ozet": "tek paragraf",
           "satirlar": [ { "k": "AYLIK ETKİ", "v": "..." }, ... ],  // 3 adet
           "not": "isteğe bağlı tek cümle"
         }
       }
     }
*/
(function () {
  'use strict';

  var node = document.getElementById('dh-etki-data');
  if (!node) return;

  var DATA;
  try { DATA = JSON.parse(node.textContent); } catch (e) { return; }

  var DUR = DATA.durumlar || {};
  var KEYS = Object.keys(DUR);
  if (!KEYS.length) return;

  var opts = [].slice.call(document.querySelectorAll('[data-dh-etki]'));
  if (!opts.length) return;

  function out(ad) { return document.querySelector('[data-dh-etki-out="' + ad + '"]'); }

  var elOzet = out('ozet');
  var elRows = out('satirlar');
  var elNot = out('not');
  var elAd = out('ad');

  function yaz(el, metin) { if (el) el.textContent = metin || ''; }

  function ciz(key) {
    var d = DUR[key];
    if (!d) return;

    yaz(elAd, d.ad);
    yaz(elOzet, d.ozet);
    yaz(elNot, d.not);
    if (elNot) elNot.hidden = !d.not;

    if (elRows) {
      var satirlar = d.satirlar || [];
      elRows.innerHTML = '';
      for (var i = 0; i < satirlar.length; i++) {
        var box = document.createElement('div');
        box.className = 'dh-ketki__row';

        var k = document.createElement('span');
        k.className = 'dh-ketki__k dh-mono';
        k.textContent = satirlar[i].k;

        var v = document.createElement('span');
        v.className = 'dh-ketki__v';
        v.textContent = satirlar[i].v;

        box.appendChild(k);
        box.appendChild(v);
        elRows.appendChild(box);
      }
    }

    for (var j = 0; j < opts.length; j++) {
      var on = opts[j].getAttribute('data-dh-etki') === key;
      opts[j].classList.toggle('is-on', on);
      opts[j].setAttribute('aria-checked', on ? 'true' : 'false');
      opts[j].tabIndex = on ? 0 : -1;
    }
  }

  function sec(key, odak) {
    ciz(key);
    if (!odak) return;
    for (var i = 0; i < opts.length; i++) {
      if (opts[i].getAttribute('data-dh-etki') === key) { opts[i].focus(); return; }
    }
  }

  function aktif() {
    for (var i = 0; i < opts.length; i++) {
      if (opts[i].getAttribute('aria-checked') === 'true') return opts[i].getAttribute('data-dh-etki');
    }
    return KEYS[0];
  }

  for (var i = 0; i < opts.length; i++) {
    (function (b) {
      b.addEventListener('click', function () { sec(b.getAttribute('data-dh-etki')); });
    }(opts[i]));
  }

  /* Klavye: grup içinde dolaşan tabindex, ok tuşları anında seçer */
  var grup = opts[0].closest('[role="radiogroup"]') || opts[0].parentNode;
  grup.addEventListener('keydown', function (e) {
    var yon = (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1
            : (e.key === 'ArrowLeft' || e.key === 'ArrowUp') ? -1 : 0;
    var i = opts.indexOf(document.activeElement);
    if (i < 0) return;
    var hedef = null;
    if (yon) hedef = opts[(i + yon + opts.length) % opts.length];
    else if (e.key === 'Home') hedef = opts[0];
    else if (e.key === 'End') hedef = opts[opts.length - 1];
    else return;
    e.preventDefault();
    sec(hedef.getAttribute('data-dh-etki'), true);
  });

  var ilk = DATA.varsayilan && DUR[DATA.varsayilan] ? DATA.varsayilan : aktif();
  ciz(DUR[ilk] ? ilk : KEYS[0]);
}());
