/* dh-bolge.js — Dünya sayfası bölge seçici (v2 / A)
   Sekiz bölge şeridi; seçime göre bölge künyesi ve haber listesi değişir.

   dh-astro.js / dh-kadin.js ile AYNI sözleşme:
     Veri kaynağı : <script type="application/json" id="dh-bolge-data">
     İşaretleme   : data-dh-bolge-* nitelikleri
   Backend gelince YALNIZ JSON bloğu değişir.

   Şerit VERİ değiştiriyor, sayfa değiştirmiyor: R7 kararına göre
   semantiği role="radiogroup" + role="radio" (tablist DEĞİL).

   Veri sözleşmesi:
     varsayilan : açılışta seçili bölge anahtarı
     bolgeler   : { "<anahtar>": {
                     ad, ozet, kapsam,
                     haberler: [{ baslik, ozet, yer, saat, etiket, gorsel }]
                   } }

   İşaretleme:
     [data-dh-bolge]             kök
     [data-dh-bolge-sec="<k>"]   şerit düğmesi (role="radio")
     [data-dh-bolge-ad]          seçili bölge adı (çoğul olabilir)
     [data-dh-bolge-ozet]        bölge tek cümlelik künyesi
     [data-dh-bolge-kapsam]      kapsanan ülke/başlık satırı
     [data-dh-bolge-sayi]        haber sayısı
     [data-dh-bolge-liste]       haber kartlarının yazılacağı kap            */
(function () {
  'use strict';

  var node = document.getElementById('dh-bolge-data');
  if (!node) return;

  var DATA;
  try { DATA = JSON.parse(node.textContent); } catch (e) { return; }

  var B = DATA.bolgeler || {};
  var KEYS = Object.keys(B);
  if (!KEYS.length) return;

  var kok = document.querySelector('[data-dh-bolge]');
  if (!kok) return;

  var liste = kok.querySelector('[data-dh-bolge-liste]');
  var ozetEl = kok.querySelector('[data-dh-bolge-ozet]');
  var kapsamEl = kok.querySelector('[data-dh-bolge-kapsam]');
  var sayiEl = kok.querySelector('[data-dh-bolge-sayi]');
  var dugmeler = [].slice.call(kok.querySelectorAll('[data-dh-bolge-sec]'));

  var current = null;

  /* Aktif düğme kayan şeridin dışında kalabiliyor; ortala. */
  function reveal(btn) {
    var box = btn.closest('.dh-bolge__rail');
    if (!box || box.scrollWidth <= box.clientWidth) return;
    box.scrollLeft = btn.offsetLeft - (box.clientWidth - btn.offsetWidth) / 2;
  }

  function kart(h) {
    var art = document.createElement('article');
    art.className = 'dh-dcard';

    var a = document.createElement('a');
    a.className = 'dh-dcard__link';
    a.setAttribute('href', 'haber-detay.html');

    var fig = document.createElement('span');
    fig.className = 'dh-dcard__fig';
    var img = document.createElement('img');
    img.className = 'dh-dcard__img';
    img.setAttribute('src', h.gorsel || './assets/images/410x410.png');
    img.setAttribute('alt', '');
    img.setAttribute('loading', 'lazy');
    img.setAttribute('decoding', 'async');
    var tag = document.createElement('span');
    tag.className = 'dh-dcard__tag';
    tag.textContent = h.etiket || 'DÜNYA';
    fig.appendChild(img);
    fig.appendChild(tag);

    var body = document.createElement('span');
    body.className = 'dh-dcard__body';

    var t = document.createElement('h3');
    t.className = 'dh-dcard__title';
    t.textContent = h.baslik || '';

    var p = document.createElement('span');
    p.className = 'dh-dcard__sum';
    p.textContent = h.ozet || '';

    var m = document.createElement('span');
    m.className = 'dh-dcard__meta';
    var yer = document.createElement('span');
    yer.className = 'dh-dcard__yer';
    yer.textContent = h.yer || '';
    var saat = document.createElement('time');
    saat.className = 'dh-dcard__saat';
    saat.textContent = h.saat || '';
    m.appendChild(yer);
    m.appendChild(saat);

    body.appendChild(t);
    body.appendChild(p);
    body.appendChild(m);

    a.appendChild(fig);
    a.appendChild(body);
    art.appendChild(a);
    return art;
  }

  function show(key, opts) {
    var b = B[key];
    if (!b) return;
    opts = opts || {};
    current = key;

    var adlar = kok.querySelectorAll('[data-dh-bolge-ad]');
    for (var i = 0; i < adlar.length; i++) adlar[i].textContent = b.ad;
    if (ozetEl) ozetEl.textContent = b.ozet || '';
    if (kapsamEl) kapsamEl.textContent = b.kapsam || '';

    var hs = b.haberler || [];
    if (sayiEl) sayiEl.textContent = hs.length;
    if (liste) {
      liste.textContent = '';
      for (var j = 0; j < hs.length; j++) liste.appendChild(kart(hs[j]));

      /* REVİZE (22 Ağustos akşamı): "ilin haberlerinin tamamını okuması
         için de renkli buton yapalım, ortalı şekilde."
         Düğme listeyle birlikte çiziliyor ki seçilen ilin adını taşısın.
         Hedef sayfa haber listesi; il adı sorgu dizesine değil, metne
         yazılıyor (prototipte süzgeç yok). */
      var cta = document.createElement('a');
      cta.className = 'dh-bolge__tumu';
      cta.href = 'haber-liste.html';
      cta.setAttribute('data-il', b.ad || '');
      cta.innerHTML = (b.ad || '') + ' haberlerinin tamamı'
        + '<i class="fas fa-arrow-right" aria-hidden="true"></i>';
      liste.appendChild(cta);
    }

    for (var k = 0; k < dugmeler.length; k++) {
      var on = dugmeler[k].getAttribute('data-dh-bolge-sec') === key;
      dugmeler[k].classList.toggle('is-on', on);
      dugmeler[k].setAttribute('aria-checked', on ? 'true' : 'false');
      dugmeler[k].setAttribute('tabindex', on ? '0' : '-1');
      if (on) {
        reveal(dugmeler[k]);
        if (opts.focus) dugmeler[k].focus();
      }
    }
  }

  function step(delta) {
    var i = KEYS.indexOf(current);
    if (i < 0) i = 0;
    show(KEYS[(i + delta + KEYS.length) % KEYS.length], { focus: true });
  }

  kok.addEventListener('click', function (e) {
    if (!e.target.closest) return;
    var b = e.target.closest('[data-dh-bolge-sec]');
    if (!b) return;
    e.preventDefault();
    show(b.getAttribute('data-dh-bolge-sec'));
  });

  /* Radyo grubu klavye sözleşmesi: ok tuşları seçimi taşır. */
  kok.addEventListener('keydown', function (e) {
    if (!e.target.closest || !e.target.closest('[data-dh-bolge-sec]')) return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); step(1); }
    else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); step(-1); }
    else if (e.key === 'Home') { e.preventDefault(); show(KEYS[0], { focus: true }); }
    else if (e.key === 'End') { e.preventDefault(); show(KEYS[KEYS.length - 1], { focus: true }); }
  });

  show(DATA.varsayilan && B[DATA.varsayilan] ? DATA.varsayilan : KEYS[0]);
})();
