/* dh-sehir.js — Gündem sayfası şehir seçici (v2 / A)
   Dokümandaki "YEREL DENEYİM" notunun karşılığı: kullanıcı şehir seçer,
   seçim "Şehrim" olarak saklanır ve yerel haber paneli o şehre döner.

   dh-astro.js / dh-kadin.js / dh-gebelik.js ile AYNI sözleşme:
     Veri kaynağı : <script type="application/json" id="dh-sehir-data">
     İşaretleme   : data-dh-sehir-* nitelikleri
   Backend gelince YALNIZ JSON bloğu değişir; işaretleme aynı kalır.

   Veri sözleşmesi:
     varsayilan : ilk açılışta gösterilecek il adı
     anahtar    : localStorage anahtarı (varsayılan "dh-sehir")
     iller      : [{ ad, plaka, bolge }]
     sablon     : [{ baslik, ozet, etiket, dk }] — "{il}" yer tutucusu geçer
     ozel       : { "<il adı>": [ {baslik, ozet, etiket, dk} ] } — şablonu ezer
     git        : haber listesine giden bağlantı (varsayılan haber-liste.html)

   İşaretleme:
     [data-dh-sehir]            kök
     [data-dh-sehir-ara]        arama kutusu (input)
     [data-dh-sehir-liste]      81 il düğmesinin yazılacağı kap
     [data-dh-sehir-bos]        sonuç yok satırı
     [data-dh-sehir-sayi]       görünen il sayısı
     [data-dh-sehir-sec="Ad"]   hızlı seçim düğmesi (sabit markup)
     [data-dh-sehir-ad]         seçili il adının yazılacağı yer (çoğul olabilir)
     [data-dh-sehir-bolge]      seçili ilin bölgesi
     [data-dh-sehir-plaka]      seçili ilin plakası
     [data-dh-sehir-durum]      "kayıtlı / kaydedilmedi" satırı
     [data-dh-sehir-haberler]   haber satırlarının yazılacağı kap
     [data-dh-sehir-git]        "tüm ... haberleri" bağlantısı
     [data-dh-sehir-sil]        kaydı silen düğme                              */
(function () {
  'use strict';

  var node = document.getElementById('dh-sehir-data');
  if (!node) return;

  var DATA;
  try { DATA = JSON.parse(node.textContent); } catch (e) { return; }

  var ILLER = DATA.iller || [];
  if (!ILLER.length) return;

  var ANAHTAR = DATA.anahtar || 'dh-sehir';
  var SABLON = DATA.sablon || [];
  var OZEL = DATA.ozel || {};
  var GIT = DATA.git || 'haber-liste.html';

  var kok = document.querySelector('[data-dh-sehir]');
  if (!kok) return;

  var ara = kok.querySelector('[data-dh-sehir-ara]');
  var liste = kok.querySelector('[data-dh-sehir-liste]');
  var bos = kok.querySelector('[data-dh-sehir-bos]');
  var sayi = kok.querySelector('[data-dh-sehir-sayi]');
  var bolgeEl = kok.querySelector('[data-dh-sehir-bolge]');
  var plakaEl = kok.querySelector('[data-dh-sehir-plaka]');
  var durum = kok.querySelector('[data-dh-sehir-durum]');
  var haberler = kok.querySelector('[data-dh-sehir-haberler]');
  var gitEl = kok.querySelector('[data-dh-sehir-git]');
  var silEl = kok.querySelector('[data-dh-sehir-sil]');

  var secili = null;
  var kayitli = false;

  /* Türkçe duyarlı normalleştirme: "İ/ı" ve şapkalı harfler eşleşsin. */
  function norm(s) {
    return String(s || '')
      .replace(/İ/g, 'i').replace(/I/g, 'i').replace(/ı/g, 'i')
      .toLowerCase()
      .replace(/ğ/g, 'g').replace(/ş/g, 's').replace(/ç/g, 'c')
      .replace(/ö/g, 'o').replace(/ü/g, 'u')
      .replace(/â/g, 'a').replace(/î/g, 'i').replace(/û/g, 'u');
  }

  function bul(ad) {
    for (var i = 0; i < ILLER.length; i++) if (ILLER[i].ad === ad) return ILLER[i];
    return null;
  }

  /* localStorage gizlilik kipinde patlayabiliyor; sessizce yut. */
  function oku() {
    try { return window.localStorage.getItem(ANAHTAR); } catch (e) { return null; }
  }
  function yaz(v) {
    try { window.localStorage.setItem(ANAHTAR, v); return true; } catch (e) { return false; }
  }
  function sil() {
    try { window.localStorage.removeItem(ANAHTAR); } catch (e) {}
  }

  function haberVer(il) {
    if (OZEL[il.ad] && OZEL[il.ad].length) return OZEL[il.ad];
    var out = [];
    for (var i = 0; i < SABLON.length; i++) {
      var s = SABLON[i];
      out.push({
        baslik: String(s.baslik || '').replace(/\{il\}/g, il.ad),
        ozet: String(s.ozet || '').replace(/\{il\}/g, il.ad),
        etiket: s.etiket || 'YEREL',
        dk: s.dk || 3
      });
    }
    return out;
  }

  function haberYaz(il) {
    if (!haberler) return;
    var hs = haberVer(il);
    haberler.textContent = '';
    for (var i = 0; i < hs.length; i++) {
      var h = hs[i];

      var li = document.createElement('li');
      li.className = 'dh-yerel__it';

      var tag = document.createElement('span');
      tag.className = 'dh-yerel__tag';
      tag.textContent = h.etiket;

      var body = document.createElement('div');
      body.className = 'dh-yerel__body';

      var t = document.createElement('h4');
      t.className = 'dh-yerel__title';
      var a = document.createElement('a');
      a.setAttribute('href', 'haber-detay.html');
      a.textContent = h.baslik;
      t.appendChild(a);

      var p = document.createElement('p');
      p.className = 'dh-yerel__sum';
      p.textContent = h.ozet;

      var m = document.createElement('span');
      m.className = 'dh-yerel__meta';
      m.textContent = il.ad + ' · ' + h.dk + ' dk okuma';

      body.appendChild(t);
      body.appendChild(p);
      body.appendChild(m);

      li.appendChild(tag);
      li.appendChild(body);
      haberler.appendChild(li);
    }
  }

  function isaretle() {
    var dugmeler = kok.querySelectorAll('[data-dh-sehir-il]');
    for (var i = 0; i < dugmeler.length; i++) {
      var on = dugmeler[i].getAttribute('data-dh-sehir-il') === secili.ad;
      dugmeler[i].classList.toggle('is-on', on);
      dugmeler[i].setAttribute('aria-pressed', on ? 'true' : 'false');
    }
    var hizli = kok.querySelectorAll('[data-dh-sehir-sec]');
    for (var j = 0; j < hizli.length; j++) {
      var k = hizli[j].getAttribute('data-dh-sehir-sec') === secili.ad;
      hizli[j].classList.toggle('is-on', k);
      hizli[j].setAttribute('aria-pressed', k ? 'true' : 'false');
    }
  }

  function goster(il, kaydet) {
    secili = il;
    if (kaydet) kayitli = yaz(il.ad);

    var adlar = document.querySelectorAll('[data-dh-sehir-ad]');
    for (var i = 0; i < adlar.length; i++) adlar[i].textContent = il.ad;

    if (bolgeEl) bolgeEl.textContent = il.bolge;
    if (plakaEl) plakaEl.textContent = ('0' + il.plaka).slice(-2);
    if (durum) {
      durum.textContent = kayitli
        ? 'Bu cihazda “Şehrim” olarak kayıtlı.'
        : 'Henüz kaydedilmedi — bir il seçtiğinizde bu cihaza kaydedilir.';
      durum.classList.toggle('is-on', !!kayitli);
    }
    if (silEl) silEl.hidden = !kayitli;
    if (gitEl) {
      gitEl.setAttribute('href', GIT);
      gitEl.textContent = il.ad + ' haberlerinin tamamı';
    }
    haberYaz(il);
    isaretle();
  }

  function listeYaz(q) {
    if (!liste) return;
    var n = norm(q);
    liste.textContent = '';
    var gorunen = 0;
    for (var i = 0; i < ILLER.length; i++) {
      var il = ILLER[i];
      /* Ad içinde geçiyorsa ya da plaka numarası ile başlıyorsa eşleşir. */
      if (n && norm(il.ad).indexOf(n) < 0 && String(il.plaka).indexOf(n) !== 0) continue;
      gorunen++;
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'dh-sehir__il';
      b.setAttribute('data-dh-sehir-il', il.ad);
      b.setAttribute('aria-pressed', secili && secili.ad === il.ad ? 'true' : 'false');
      if (secili && secili.ad === il.ad) b.classList.add('is-on');

      var pl = document.createElement('span');
      pl.className = 'dh-sehir__plaka';
      pl.textContent = ('0' + il.plaka).slice(-2);

      var ad = document.createElement('span');
      ad.className = 'dh-sehir__ad';
      ad.textContent = il.ad;

      b.appendChild(pl);
      b.appendChild(ad);
      liste.appendChild(b);
    }
    if (bos) bos.hidden = gorunen > 0;
    if (sayi) sayi.textContent = gorunen;
  }

  kok.addEventListener('click', function (e) {
    if (!e.target.closest) return;

    var b = e.target.closest('[data-dh-sehir-il]');
    if (b) {
      var il = bul(b.getAttribute('data-dh-sehir-il'));
      if (il) goster(il, true);
      return;
    }

    var h = e.target.closest('[data-dh-sehir-sec]');
    if (h) {
      e.preventDefault();
      var il2 = bul(h.getAttribute('data-dh-sehir-sec'));
      if (il2) goster(il2, true);
      return;
    }

    if (e.target.closest('[data-dh-sehir-sil]')) {
      sil();
      kayitli = false;
      goster(bul(DATA.varsayilan) || ILLER[0], false);
    }
  });

  if (ara) {
    ara.addEventListener('input', function () { listeYaz(ara.value); });
    /* Arama kutusunda Enter formu göndermesin (kabukta form yok ama
       ileride sarmalanırsa sayfa yenilenmesin). */
    ara.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') e.preventDefault();
    });
  }

  var kayit = oku();
  var baslangic = (kayit && bul(kayit)) || bul(DATA.varsayilan) || ILLER[0];
  kayitli = !!(kayit && bul(kayit));
  listeYaz('');
  goster(baslangic, false);
})();
