/* ============================================================================
   Dada Haber v2 — Canlı skorlar: dal sekmeleri (spor.html #canli)

   Talep: "Burada bir tab menü oluşturabiliriz; futbolun canlısı,
   basketbolun canlısı, tenisin canlısı şeklinde. Sayfalandırma çok
   dağılmış durumda, bu şekilde gitmeyelim."

   Sekmeler MARKUP'A GÖMÜLMÜYOR: ray içindeki kartların `data-branch`
   değerleri okunup sekmeler ondan üretiliyor. Kart eklenince sekme de
   kendiliğinden geliyor, iki yerde güncelleme derdi olmuyor.

   SÖZLEŞME
     <div class="dh-canli" data-dh-canli>
       <div class="dh-canli__tabs" data-dh-canli-tabs></div>   ← üretilir
       <div class="dh-mcrail"> <article data-branch="futbol"> ... </div>
   ========================================================================== */
(function () {
  'use strict';

  var AD = {
    futbol: 'Futbol', basketbol: 'Basketbol', voleybol: 'Voleybol',
    tenis: 'Tenis', f1: 'Formula 1', bisiklet: 'Bisiklet',
    atletizm: 'Atletizm', motor: 'Motor Sporları'
  };
  var IKON = {
    futbol: 'fa-futbol', basketbol: 'fa-basketball-ball', voleybol: 'fa-volleyball-ball',
    tenis: 'fa-table-tennis', f1: 'fa-flag-checkered', bisiklet: 'fa-bicycle',
    atletizm: 'fa-person-running', motor: 'fa-motorcycle'
  };

  function kur(kok) {
    var ray = kok.querySelector('.dh-mcrail');
    var yuva = kok.querySelector('[data-dh-canli-tabs]');
    if (!ray || !yuva) return;

    var kart = [].slice.call(ray.children);
    var dallar = [];
    kart.forEach(function (k) {
      var b = k.getAttribute('data-branch');
      if (b && dallar.indexOf(b) < 0) dallar.push(b);
    });
    if (dallar.length < 2) return;         // tek dal varsa sekmeye gerek yok

    var secili = 'tumu';

    function say(dal) {
      return kart.filter(function (k) {
        return dal === 'tumu' || k.getAttribute('data-branch') === dal;
      }).length;
    }

    function ciz() {
      kart.forEach(function (k) {
        k.hidden = !(secili === 'tumu' || k.getAttribute('data-branch') === secili);
      });
      [].slice.call(yuva.children).forEach(function (b) {
        var on = b.getAttribute('data-dal') === secili;
        b.classList.toggle('is-on', on);
        b.setAttribute('aria-selected', on ? 'true' : 'false');
        b.setAttribute('tabindex', on ? '0' : '-1');
      });
    }

    function dugme(dal, ad, ikon) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'dh-canli__tab';
      b.setAttribute('role', 'tab');
      b.setAttribute('data-dal', dal);
      b.innerHTML = (ikon ? '<i class="fas ' + ikon + '" aria-hidden="true"></i>' : '')
        + '<span>' + ad + '</span><b>' + say(dal) + '</b>';
      b.addEventListener('click', function () { secili = dal; ciz(); });
      return b;
    }

    yuva.setAttribute('role', 'tablist');
    yuva.appendChild(dugme('tumu', 'Tümü', 'fa-bolt'));
    dallar.forEach(function (d) {
      yuva.appendChild(dugme(d, AD[d] || d, IKON[d]));
    });

    yuva.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      var t = [].slice.call(yuva.children);
      var i = t.indexOf(document.activeElement);
      if (i < 0) return;
      e.preventDefault();
      var j = (i + (e.key === 'ArrowRight' ? 1 : -1) + t.length) % t.length;
      t[j].focus();
      t[j].click();
    });

    ciz();
  }

  function init() {
    document.querySelectorAll('[data-dh-canli]').forEach(kur);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
