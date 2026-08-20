/* dh-tabs.js — Lig merkezi: sekmeler + iki kademeli lig seçici (R7-S)
   Yeni kütüphane yok, saf vanilla JS. ES5 sözdizimi.

   İKİ AYRI DESEN, İKİ AYRI ARIA ROLÜ — bilerek:
   · SEKMELER (.dh-sort[role=tablist]) hangi BÖLÜMÜN görüneceğini seçer:
     Puan Durumu · Fikstür · Sonuçlar · Kral/İstatistik. Klasik tab deseni:
     role=tab + aria-selected + aria-controls, ok tuşlarında otomatik etkinleşme.
   · LİG SEÇİCİ (.dh-lgpick) bir sekme değil SÜZGEÇTİR: görünen bölümü
     değiştirmez, o bölümün VERİSİNİ değiştirir. Doğru rol radiogroup/radio +
     aria-checked. İki tablist aynı paneli yönetirse ekran okuyucuda
     "hangi sekmedeyim" bilgisi bozulur; bu yüzden ayrıldı.

   Klavye (her iki desende de dolaşan tabindex / roving tabindex):
     ← ↑  önceki · → ↓  sonraki · Home ilk · End son — hepsi anında seçer.
     Grup dışına Tab ile çıkılır, grup içinde tek durak vardır.

   Veri: assets/js/dh-lig-veri.js -> window.DHLigVeri[<dal>]. Sayfaya gömmek
   yerine ortak dosya: aynı lig verisi dört sayfada kullanılıyor, gömülü olsa
   dört kez indirilirdi. İşaretlemeyi dh-lig.js üretir (build sırasında Node
   ile aynı modül — iki taraf ayrışmasın diye). */
(function () {
  'use strict';

  var ILERI = { ArrowRight: 1, ArrowDown: 1, Right: 1, Down: 1 };
  var GERI = { ArrowLeft: -1, ArrowUp: -1, Left: -1, Up: -1 };

  function dizi(nodeList) {
    return Array.prototype.slice.call(nodeList);
  }

  /* Dolaşan tabindex: grupta yalnız seçili öğe Tab durağıdır. */
  function odakSirasi(items, aktif) {
    for (var i = 0; i < items.length; i++) {
      items[i].tabIndex = items[i] === aktif ? 0 : -1;
    }
  }

  function gorunur(el) {
    return el.offsetParent !== null || el.getClientRects().length > 0;
  }

  /* Ok tuşu gezinmesi — gizli çipler atlanır. */
  function klavye(getItems, sec) {
    return function (e) {
      var yon = ILERI[e.key] ? 1 : (GERI[e.key] ? -1 : 0);
      var items = getItems().filter(gorunur);
      if (!items.length) return;
      var i = items.indexOf(document.activeElement);
      var hedef = null;
      if (yon) {
        if (i < 0) i = 0;
        hedef = items[(i + yon + items.length) % items.length];
      } else if (e.key === 'Home') {
        hedef = items[0];
      } else if (e.key === 'End') {
        hedef = items[items.length - 1];
      } else {
        return;
      }
      e.preventDefault();
      sec(hedef);
      hedef.focus();
    };
  }

  /* ---------------- Sekmeler ---------------- */
  function sekmeKur(root) {
    var liste = root.querySelector('[data-dh-tabs]');
    if (!liste) return null;
    var tablar = dizi(liste.querySelectorAll('[role="tab"]'));
    if (!tablar.length) return null;

    function panel(tab) {
      var id = tab.getAttribute('aria-controls');
      return id ? document.getElementById(id) : null;
    }

    function sec(tab) {
      for (var i = 0; i < tablar.length; i++) {
        var t = tablar[i], acik = t === tab, p = panel(t);
        t.setAttribute('aria-selected', acik ? 'true' : 'false');
        t.classList.toggle('is-on', acik);
        if (p) {
          p.hidden = !acik;
          p.classList.toggle('is-on', acik);
        }
      }
      odakSirasi(tablar, tab);
    }

    for (var i = 0; i < tablar.length; i++) {
      (function (t) {
        t.addEventListener('click', function () { sec(t); });
      }(tablar[i]));
    }
    liste.addEventListener('keydown', klavye(function () { return tablar; }, sec));

    var acik = liste.querySelector('[aria-selected="true"]') || tablar[0];
    sec(acik);
    return { tablar: tablar, sec: sec };
  }

  /* ---------------- Lig seçici ---------------- */
  function ligKur(root) {
    var pick = root.querySelector('[data-dh-lgpick]');
    var dal = root.getAttribute('data-dh-veri');
    if (!pick || !dal || !window.DHLig || !window.DHLigVeri) return;

    var LIGLER = window.DHLigVeri[dal];
    if (!LIGLER) return;

    var kapsamlar = dizi(pick.querySelectorAll('[data-scope][role="radio"]:not([data-lig])'));
    var ligler = dizi(pick.querySelectorAll('[data-lig]'));
    var kicker = root.querySelector('[data-dh-lig-kicker]');
    var bolumler = dizi(root.querySelectorAll('[data-dh-lg]'));
    var aktifLig = (pick.querySelector('[data-lig][aria-checked="true"]') || ligler[0]);

    function ciz(id) {
      var lig = LIGLER[id];
      if (!lig) return;
      for (var i = 0; i < bolumler.length; i++) {
        var ad = bolumler[i].getAttribute('data-dh-lg');
        bolumler[i].innerHTML = window.DHLig.bolum(ad, lig);
      }
      if (kicker) kicker.textContent = lig.kicker;
      root.setAttribute('data-lig', id);
    }

    function ligSec(chip, cizme) {
      for (var i = 0; i < ligler.length; i++) {
        var acik = ligler[i] === chip;
        ligler[i].setAttribute('aria-checked', acik ? 'true' : 'false');
        ligler[i].classList.toggle('is-on', acik);
      }
      aktifLig = chip;
      odakSirasi(ligler.filter(gorunur), chip);
      if (cizme !== false) ciz(chip.getAttribute('data-lig'));
    }

    function kapsamSec(chip, cizme) {
      var s = chip.getAttribute('data-scope');
      for (var i = 0; i < kapsamlar.length; i++) {
        var acik = kapsamlar[i] === chip;
        kapsamlar[i].setAttribute('aria-checked', acik ? 'true' : 'false');
        kapsamlar[i].classList.toggle('is-on', acik);
      }
      odakSirasi(kapsamlar, chip);

      var ilk = null;
      for (var j = 0; j < ligler.length; j++) {
        var uyar = ligler[j].getAttribute('data-scope') === s;
        ligler[j].hidden = !uyar;
        if (uyar && !ilk) ilk = ligler[j];
      }
      /* Seçili lig bu kapsamda değilse kapsamın ilk ligine geçilir. */
      if (ilk && (!aktifLig || aktifLig.getAttribute('data-scope') !== s)) {
        ligSec(ilk, cizme);
      } else if (aktifLig) {
        odakSirasi(ligler.filter(gorunur), aktifLig);
      }
      var sarici = pick.querySelector('[data-dh-leagues]');
      if (sarici) sarici.scrollLeft = 0;
    }

    for (var i = 0; i < kapsamlar.length; i++) {
      (function (c) { c.addEventListener('click', function () { kapsamSec(c); }); }(kapsamlar[i]));
    }
    for (var j = 0; j < ligler.length; j++) {
      (function (c) { c.addEventListener('click', function () { ligSec(c); }); }(ligler[j]));
    }

    var kapsamKutu = pick.querySelector('[data-dh-scopes]');
    var ligKutu = pick.querySelector('[data-dh-leagues]');
    if (kapsamKutu) kapsamKutu.addEventListener('keydown', klavye(function () { return kapsamlar; }, function (c) { kapsamSec(c); }));
    if (ligKutu) ligKutu.addEventListener('keydown', klavye(function () { return ligler; }, function (c) { ligSec(c); }));

    /* İlk kurulum: sayfada zaten varsayılan ligin statik HTML'i var,
       yeniden çizme — yalnız görünürlük ve odak sırası kurulur. */
    var acikKapsam = pick.querySelector('[data-scope][aria-checked="true"]:not([data-lig])') || kapsamlar[0];
    if (acikKapsam) kapsamSec(acikKapsam, false);
  }

  function kur() {
    var kokler = dizi(document.querySelectorAll('[data-dh-lig]'));
    for (var i = 0; i < kokler.length; i++) {
      sekmeKur(kokler[i]);
      ligKur(kokler[i]);
    }
    /* Lig seçicisi olmayan, yalnız sekmeli paneller */
    var yalnizSekme = dizi(document.querySelectorAll('[data-dh-tabs]'));
    for (var j = 0; j < yalnizSekme.length; j++) {
      var kok = yalnizSekme[j].closest ? yalnizSekme[j].closest('[data-dh-lig]') : null;
      if (!kok) sekmeKur(yalnizSekme[j].parentNode);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', kur);
  } else {
    kur();
  }
}());
