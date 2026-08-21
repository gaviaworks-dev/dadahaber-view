/* dh-ozet.js — Dada Özet derinlik seçimi (dada-ozet.html)
   15 Saniyede · 1 Dakikada · Derinlemesine — AYNI haberin üç okuması.
   Yeni kütüphane yok, saf vanilla JS, ES5 sözdizimi.

   ORTAK SÖZLEŞME:
     Veri     : <script type="application/json" id="dh-ozet-data">
     Şerit    : [data-dh-ozet-tabs] · role="tablist"
     Sekme    : button[data-dh-ozet] · role="tab" · aria-controls
     Panel    : [data-dh-ozet-panel] · role="tabpanel"
     Yazım    : [data-dh-ozet-out="<alan>"]  (govde · sure · kelime · kaynak)

   ROL SEÇİMİ: üç derinlik üç ayrı, bağımsız okunabilir METİN. Görünen
   panel gerçekten değişiyor -> role="tablist" doğru desen (R7'deki üç
   desenden birincisi). Klavye: ok tuşları anında seçer, Home/End uçlar.

   VERİ SÖZLEŞMESİ
     {
       "haber": { "kicker": "...", "baslik": "...", "tarih": "21.08.2026",
                  "guncelleme": "09:40", "link": "haber-detay.html" },
       "varsayilan": "15sn",
       "derinlikler": {
         "<anahtar>": {
           "ad": "15 Saniyede",
           "sure": "15 SN",
           "kelime": 38,
           "kaynak": 3,
           "blok": [ {"tip":"p","metin":"..."},
                     {"tip":"h","metin":"..."},
                     {"tip":"ul","maddeler":["...","..."]} ]
         }
       }
     }
   Yalnız üç blok tipi tanınır (p · h · ul); tanınmayan blok atlanır.
*/
(function () {
  'use strict';

  var node = document.getElementById('dh-ozet-data');
  if (!node) return;

  var DATA;
  try { DATA = JSON.parse(node.textContent); } catch (e) { return; }

  var DER = DATA.derinlikler || {};
  var tabs = [].slice.call(document.querySelectorAll('[data-dh-ozet]'));
  var panel = document.querySelector('[data-dh-ozet-panel]');
  if (!tabs.length || !panel) return;

  function out(ad) { return document.querySelector('[data-dh-ozet-out="' + ad + '"]'); }
  var elGovde = out('govde');
  var elSure = out('sure');
  var elKelime = out('kelime');
  var elKaynak = out('kaynak');

  function govdeCiz(blok) {
    elGovde.innerHTML = '';
    for (var i = 0; i < blok.length; i++) {
      var b = blok[i], el;
      if (b.tip === 'p') {
        el = document.createElement('p');
        el.textContent = b.metin;
      } else if (b.tip === 'h') {
        el = document.createElement('h3');
        el.textContent = b.metin;
      } else if (b.tip === 'ul') {
        el = document.createElement('ul');
        for (var j = 0; j < (b.maddeler || []).length; j++) {
          var li = document.createElement('li');
          li.textContent = b.maddeler[j];
          el.appendChild(li);
        }
      } else {
        continue;
      }
      elGovde.appendChild(el);
    }
  }

  function sec(tab, odak) {
    var key = tab.getAttribute('data-dh-ozet');
    var d = DER[key];
    if (!d) return;

    for (var i = 0; i < tabs.length; i++) {
      var on = tabs[i] === tab;
      tabs[i].setAttribute('aria-selected', on ? 'true' : 'false');
      tabs[i].tabIndex = on ? 0 : -1;
    }

    panel.setAttribute('aria-labelledby', tab.id || '');
    if (elGovde) govdeCiz(d.blok || []);
    if (elSure) elSure.textContent = d.sure || '';
    if (elKelime) elKelime.textContent = String(d.kelime || '');
    if (elKaynak) elKaynak.textContent = String(d.kaynak || '');

    if (odak) tab.focus();
  }

  for (var i = 0; i < tabs.length; i++) {
    (function (t) { t.addEventListener('click', function () { sec(t); }); }(tabs[i]));
  }

  var liste = document.querySelector('[data-dh-ozet-tabs]') || tabs[0].parentNode;
  liste.addEventListener('keydown', function (e) {
    var yon = (e.key === 'ArrowRight' || e.key === 'ArrowDown') ? 1
            : (e.key === 'ArrowLeft' || e.key === 'ArrowUp') ? -1 : 0;
    var i = tabs.indexOf(document.activeElement);
    if (i < 0) return;
    var hedef = null;
    if (yon) hedef = tabs[(i + yon + tabs.length) % tabs.length];
    else if (e.key === 'Home') hedef = tabs[0];
    else if (e.key === 'End') hedef = tabs[tabs.length - 1];
    else return;
    e.preventDefault();
    sec(hedef, true);
  });

  var ilk = null;
  for (var k = 0; k < tabs.length; k++) {
    if (tabs[k].getAttribute('data-dh-ozet') === DATA.varsayilan) { ilk = tabs[k]; break; }
  }
  sec(ilk || tabs[0]);
}());
