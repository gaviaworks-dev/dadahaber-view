/* dh-tabs.js — Lig merkezi: sekmeler + üç kademeli lig seçici (R7-S)
   Yeni kütüphane yok, saf vanilla JS. ES5 sözdizimi.

   ÜÇ AYRI DESEN, ÜÇ AYRI ARIA ROLÜ — bilerek:
   · SEKMELER (.dh-sort--tabs[role=tablist]) hangi BÖLÜMÜN görüneceğini seçer:
     Puan Durumu · Fikstür · Sonuçlar · Kral/İstatistik. Klasik tab deseni:
     role=tab + aria-selected + aria-controls, ok tuşlarında otomatik etkinleşme.
   · SEÇİCİLER (.dh-lgpick lig çipleri, .dh-sort--split Genel/İç Saha/Deplasman)
     sekme DEĞİL SÜZGEÇTİR: görünen bölümü değiştirmez, o bölümün VERİSİNİ
     değiştirir. Doğru rol radiogroup/radio + aria-checked. İki tablist aynı
     paneli yönetirse ekran okuyucuda "hangi sekmedeyim" bilgisi bozulur.
   · ÜLKE ve SEZON native <select>: seçenek sayısı büyük ve gezinilecek değil
     seçilecek listeler (referans sitede ülke listesi 77 seçenek).

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

  /* ---------------- Üç kademeli lig seçici ----------------
     ÜLKE (açılır kutu) -> LİG (çip) -> SEZON (açılır kutu)
     Kumanda tipi kararı ve ölçümü: custom.min.css R7-S/6. */
  function ligKur(root) {
    var pick = root.querySelector('[data-dh-lgpick]');
    var dal = root.getAttribute('data-dh-veri');
    if (!pick || !dal || !window.DHLig || !window.DHLigVeri) return;

    var LIGLER = window.DHLigVeri[dal];
    if (!LIGLER) return;

    var ulkeSel = pick.querySelector('[data-dh-ulke]');
    var sezonSel = pick.querySelector('[data-dh-sezon]');
    var ligler = dizi(pick.querySelectorAll('[data-lig]'));
    var kicker = root.querySelector('[data-dh-lig-kicker]');
    var bolumler = dizi(root.querySelectorAll('[data-dh-lg]'));
    var splitler = dizi(root.querySelectorAll('[data-dh-split] [role="radio"]'));
    var aktifLig = (pick.querySelector('[data-lig][aria-checked="true"]') || ligler[0]);
    var gorunumAd = 'genel';

    function veriyi() {
      var lig = LIGLER[aktifLig ? aktifLig.getAttribute('data-lig') : ''];
      if (!lig) return null;
      return sezonSel ? window.DHLig.sezonla(lig, sezonSel.value) : lig;
    }

    function ciz() {
      var lig = veriyi();
      if (!lig) return;
      for (var i = 0; i < bolumler.length; i++) {
        var ad = bolumler[i].getAttribute('data-dh-lg');
        bolumler[i].innerHTML = window.DHLig.bolum(ad, lig, ad === 'tablo' ? gorunumAd : null);
      }
      if (kicker) kicker.textContent = lig.kicker;
      root.setAttribute('data-lig', aktifLig.getAttribute('data-lig'));
      root.setAttribute('data-sezon', lig.sezon || '');
    }

    function ligSec(chip, cizme) {
      /* Ülke kutusu ile şerit ayrışmasın: seçilen lig başka bir ülkeye
         aitse (derin bağlantı, program ile seçim) kutu da o ülkeye
         çekilir ve görünen çip kümesi yenilenir. */
      var kod = chip.getAttribute('data-scope');
      if (ulkeSel && ulkeSel.value !== kod) {
        ulkeSel.value = kod;
        for (var k = 0; k < ligler.length; k++) {
          ligler[k].hidden = ligler[k].getAttribute('data-scope') !== kod;
        }
      }
      for (var i = 0; i < ligler.length; i++) {
        var acik = ligler[i] === chip;
        ligler[i].setAttribute('aria-checked', acik ? 'true' : 'false');
        ligler[i].classList.toggle('is-on', acik);
      }
      aktifLig = chip;
      odakSirasi(ligler.filter(gorunur), chip);
      if (cizme !== false) ciz();
    }

    function ulkeSec(kod, cizme) {
      var ilk = null;
      for (var j = 0; j < ligler.length; j++) {
        var uyar = ligler[j].getAttribute('data-scope') === kod;
        ligler[j].hidden = !uyar;
        if (uyar && !ilk) ilk = ligler[j];
      }
      if (ilk && (!aktifLig || aktifLig.getAttribute('data-scope') !== kod)) {
        ligSec(ilk, cizme);
      } else if (aktifLig) {
        odakSirasi(ligler.filter(gorunur), aktifLig);
        if (cizme !== false) ciz();
      }
      var sarici = pick.querySelector('[data-dh-leagues]');
      if (sarici) sarici.scrollLeft = 0;
    }

    function gorunumSec(btn) {
      for (var i = 0; i < splitler.length; i++) {
        var acik = splitler[i] === btn;
        splitler[i].setAttribute('aria-checked', acik ? 'true' : 'false');
        splitler[i].classList.toggle('is-on', acik);
      }
      odakSirasi(splitler, btn);
      gorunumAd = btn.getAttribute('data-gorunum') || 'genel';
      var lig = veriyi();
      var hedef = root.querySelector('[data-dh-lg="tablo"]');
      if (lig && hedef) hedef.innerHTML = window.DHLig.bolum('tablo', lig, gorunumAd);
    }

    for (var j = 0; j < ligler.length; j++) {
      (function (c) { c.addEventListener('click', function () { ligSec(c); }); }(ligler[j]));
    }
    for (var k = 0; k < splitler.length; k++) {
      (function (c) { c.addEventListener('click', function () { gorunumSec(c); }); }(splitler[k]));
    }
    if (ulkeSel) ulkeSel.addEventListener('change', function () { ulkeSec(ulkeSel.value); });
    if (sezonSel) sezonSel.addEventListener('change', function () { ciz(); });

    var ligKutu = pick.querySelector('[data-dh-leagues]');
    var splitKutu = root.querySelector('[data-dh-split]');
    if (ligKutu) ligKutu.addEventListener('keydown', klavye(function () { return ligler; }, function (c) { ligSec(c); }));
    if (splitKutu) splitKutu.addEventListener('keydown', klavye(function () { return splitler; }, function (c) { gorunumSec(c); }));

    /* İlk kurulum: varsayılan ligin statik HTML'i sayfada zaten var,
       yeniden çizme — yalnız görünürlük ve odak sırası kurulur. */
    if (ulkeSel) ulkeSec(ulkeSel.value, false);
  }

  /* ---------------- Basit süzgeç grupları ----------------
     Sıralama / hafta / dönem şeritleri. Eskiden role="tab" idi ama
     yönettikleri bir panel yoktu: ekran okuyucuya sekme diye tanıtılan
     ama hiçbir şey açmayan denetimlerdi. Artık role="group" +
     aria-pressed, ve tıklandığında gerçekten seçim değiştiriyorlar.
     Veriyi backend bağlanınca sunucu değiştirecek. */
  function pickKur() {
    var gruplar = dizi(document.querySelectorAll('[data-dh-pick]'));
    for (var i = 0; i < gruplar.length; i++) {
      (function (g) {
        var btns = dizi(g.querySelectorAll('button'));
        function sec(b) {
          for (var j = 0; j < btns.length; j++) {
            var acik = btns[j] === b;
            btns[j].setAttribute('aria-pressed', acik ? 'true' : 'false');
            btns[j].classList.toggle('is-on', acik);
          }
        }
        for (var k = 0; k < btns.length; k++) {
          (function (b) { b.addEventListener('click', function () { sec(b); }); }(btns[k]));
        }
      }(gruplar[i]));
    }
  }

  function kur() {
    pickKur();
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
