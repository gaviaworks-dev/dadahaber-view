/* dh-dogrula.js — Güncel İddialar karar süzgeci (dada-dogrula.html)
   Yeni kütüphane yok, saf vanilla JS, ES5 sözdizimi.

   ORTAK SÖZLEŞME:
     Süzgeç : [data-dh-vdfilter] · role="radiogroup"
     Düğme  : button[data-dh-vd="<karar|tumu>"] · role="radio" · aria-checked
     Sayaç  : düğme içinde [data-dh-vd-count] — DOM'dan sayılır, elle yazılmaz
     Kart   : [data-dh-vd-card="<karar>"]
     Boş    : [data-dh-vd-empty]
     Toplam : [data-dh-vd-total]

   İddia kartları SAYFADA statik duruyor (JS kapalıysa hepsi görünür ve
   okunur; süzgeç yalnız bir daraltma kolaylığı). Bu yüzden veri JSON'dan
   üretilmiyor — kararlar kartın kendi data niteliğinde. Sayaçlar DOM'dan
   sayıldığı için içerik değişince elle güncelleme gerekmez.
*/
(function () {
  'use strict';

  var grup = document.querySelector('[data-dh-vdfilter]');
  if (!grup) return;

  var btns = [].slice.call(grup.querySelectorAll('[data-dh-vd]'));
  var kartlar = [].slice.call(document.querySelectorAll('[data-dh-vd-card]'));
  var bos = document.querySelector('[data-dh-vd-empty]');
  var toplam = document.querySelector('[data-dh-vd-total]');
  if (!btns.length || !kartlar.length) return;

  /* Sayaçlar DOM'dan */
  var sayim = {};
  for (var i = 0; i < kartlar.length; i++) {
    var k = kartlar[i].getAttribute('data-dh-vd-card');
    sayim[k] = (sayim[k] || 0) + 1;
  }
  for (var j = 0; j < btns.length; j++) {
    var ad = btns[j].getAttribute('data-dh-vd');
    var c = btns[j].querySelector('[data-dh-vd-count]');
    if (c) c.textContent = String(ad === 'tumu' ? kartlar.length : (sayim[ad] || 0));
  }

  function suz(ad, odak) {
    var gorunen = 0;
    for (var i = 0; i < kartlar.length; i++) {
      var uy = (ad === 'tumu') || kartlar[i].getAttribute('data-dh-vd-card') === ad;
      kartlar[i].hidden = !uy;
      if (uy) gorunen++;
    }
    for (var j = 0; j < btns.length; j++) {
      var on = btns[j].getAttribute('data-dh-vd') === ad;
      btns[j].setAttribute('aria-checked', on ? 'true' : 'false');
      btns[j].tabIndex = on ? 0 : -1;
      if (on && odak) btns[j].focus();
    }
    if (bos) bos.classList.toggle('is-on', gorunen === 0);
    if (toplam) toplam.textContent = String(gorunen);
  }

  for (var m = 0; m < btns.length; m++) {
    (function (b) {
      b.addEventListener('click', function () { suz(b.getAttribute('data-dh-vd')); });
    }(btns[m]));
  }

  grup.addEventListener('keydown', function (e) {
    var yon = (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1
            : (e.key === 'ArrowLeft' || e.key === 'ArrowUp') ? -1 : 0;
    var i = btns.indexOf(document.activeElement);
    if (i < 0) return;
    var hedef = null;
    if (yon) hedef = btns[(i + yon + btns.length) % btns.length];
    else if (e.key === 'Home') hedef = btns[0];
    else if (e.key === 'End') hedef = btns[btns.length - 1];
    else return;
    e.preventDefault();
    suz(hedef.getAttribute('data-dh-vd'), true);
  });

  var acik = grup.querySelector('[aria-checked="true"]');
  suz(acik ? acik.getAttribute('data-dh-vd') : 'tumu');
}());
