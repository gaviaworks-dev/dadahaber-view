/* dh-bakis.js — Farklı Bakışlar gelişme seçici (v2 / farkli-bakislar.html)
   Yeni kütüphane yok, saf vanilla JS.
   dh-astro.js / dh-kadin.js ile AYNI sözleşme:
     Veri kaynağı : <script type="application/json" id="dh-bakis-data">
     Seçici       : [data-dh-bakis-picks] içine .dh-catbar__chip[data-dh-gelisme]
                    üretilir; role="radio" (veri değiştiriyor, sayfa değiştirmiyor)
     Alanlar      : [data-dh-bakis="<alan>"] metin olarak doldurulur
     Listeler     : [data-dh-bakis-ortak|-ayrisan|-tr|-dunya|-uzman|-cmp]
   Backend gelince YALNIZ JSON bloğu değişir; işaretleme aynı kalır. */
(function () {
  'use strict';

  var node = document.getElementById('dh-bakis-data');
  if (!node) return;

  var DATA;
  try { DATA = JSON.parse(node.textContent); } catch (e) { return; }

  var G = DATA.gelismeler || {};
  var KEYS = Object.keys(G);
  if (!KEYS.length) return;

  var picks = document.querySelector('[data-dh-bakis-picks]');
  var current = null;

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt != null) n.textContent = txt;
    return n;
  }

  function setText(key, value) {
    var list = document.querySelectorAll('[data-dh-bakis="' + key + '"]');
    for (var i = 0; i < list.length; i++) list[i].textContent = value;
  }

  function fill(host, items, render) {
    if (!host) return;
    host.innerHTML = '';
    for (var i = 0; i < items.length; i++) host.appendChild(render(items[i], i));
  }

  /* --- seçici çipleri --------------------------------------------------- */
  function buildPicks() {
    if (!picks) return;
    picks.innerHTML = '';
    for (var i = 0; i < KEYS.length; i++) {
      var k = KEYS[i];
      var b = el('button', 'dh-catbar__chip', G[k].ad);
      b.type = 'button';
      b.setAttribute('role', 'radio');
      b.setAttribute('aria-checked', 'false');
      b.setAttribute('data-dh-gelisme', k);
      b.setAttribute('tabindex', '-1');
      picks.appendChild(b);
    }
  }

  /* --- satır kalıpları --------------------------------------------------- */
  function ortakRow(o) {
    var li = el('li', 'dh-bakis__ortak');
    li.appendChild(el('span', 'dh-bakis__ortakic'));
    li.appendChild(el('p', 'dh-bakis__ortaktxt', o.metin));
    li.appendChild(el('span', 'dh-num dh-bakis__ortakkac', o.kac));
    return li;
  }

  function ayriRow(a) {
    var li = el('li', 'dh-bakis__ayri');
    var head = el('div', 'dh-bakis__ayrihead');
    head.appendChild(el('b', 'dh-bakis__ayrisrc', a.kaynak));
    head.appendChild(el('span', 'dh-num dh-bakis__ayritur', a.tur));
    li.appendChild(head);
    li.appendChild(el('span', 'dh-bakis__ayritutum', a.tutum));
    li.appendChild(el('p', 'dh-bakis__ayritxt', a.metin));
    return li;
  }

  function srcRow(s) {
    var li = el('li', 'dh-bakis__src');
    li.appendChild(el('b', 'dh-bakis__srcad', s.kaynak));
    li.appendChild(el('span', 'dh-bakis__srcbas', s.baslik));
    li.appendChild(el('span', 'dh-num dh-bakis__srcaci', s.aci));
    return li;
  }

  function expCard(u) {
    var a = el('article', 'dh-bakis__exp');
    var h = el('header', 'dh-bakis__exphead');
    h.appendChild(el('span', 'dh-num dh-bakis__expetiket', u.etiket));
    a.appendChild(h);
    a.appendChild(el('blockquote', 'dh-bakis__expq', u.gorus));
    var f = el('footer', 'dh-bakis__expfoot');
    f.appendChild(el('b', 'dh-bakis__expad', u.ad));
    f.appendChild(el('span', 'dh-bakis__expunvan', u.unvan));
    a.appendChild(f);
    return a;
  }

  function cmpRow(c) {
    var tr = el('tr');
    var th = el('th', 'dh-bakis__cmpsrc', c.kaynak);
    th.setAttribute('scope', 'row');
    tr.appendChild(th);
    var tur = el('td');
    tur.appendChild(el('span', 'dh-num dh-bakis__cmptur', c.tur));
    tr.appendChild(tur);
    tr.appendChild(el('td', 'dh-bakis__cmpbas', '“' + c.baslik + '”'));
    var v = el('td');
    v.appendChild(el('span', 'dh-num dh-bakis__cmpvurgu', c.vurgu));
    tr.appendChild(v);
    return tr;
  }

  /* --- ana çizim --------------------------------------------------------- */
  function render(key, opts) {
    var g = G[key];
    if (!g) return;
    opts = opts || {};
    current = key;

    setText('etiket', g.etiket);
    setText('baslik', g.baslik);
    setText('ozet', g.ozet);
    setText('kaynak', g.kaynak);
    setText('ulke', g.ulke);
    setText('ilk', g.ilk);
    setText('uzlasma', g.uzlasma);
    setText('sayi-gelisme', String(KEYS.length));
    setText('sayi-kaynak', g.kaynak);
    setText('guncelleme', DATA.guncelleme || '—');

    setText('ortak-adet', g.ortak.length + ' madde');
    setText('ayri-adet', g.ayrisan.length + ' kaynak');
    setText('tr-adet', g.tr.length + ' yayın');
    setText('dunya-adet', g.dunya.length + ' yayın');

    fill(document.querySelector('[data-dh-bakis-ortak]'), g.ortak, ortakRow);
    fill(document.querySelector('[data-dh-bakis-ayrisan]'), g.ayrisan, ayriRow);
    fill(document.querySelector('[data-dh-bakis-tr]'), g.tr, srcRow);
    fill(document.querySelector('[data-dh-bakis-dunya]'), g.dunya, srcRow);
    fill(document.querySelector('[data-dh-bakis-uzman]'), g.uzman, expCard);
    fill(document.querySelector('[data-dh-bakis-cmp]'), g.karsilastirma, cmpRow);

    if (picks) {
      var chips = picks.querySelectorAll('[data-dh-gelisme]');
      for (var i = 0; i < chips.length; i++) {
        var on = chips[i].getAttribute('data-dh-gelisme') === key;
        chips[i].classList.toggle('is-on', on);
        chips[i].setAttribute('aria-checked', on ? 'true' : 'false');
        chips[i].setAttribute('tabindex', on ? '0' : '-1');
        if (on && opts.focus) chips[i].focus();
      }
    }
  }

  function step(delta) {
    var i = KEYS.indexOf(current);
    if (i < 0) i = 0;
    render(KEYS[(i + delta + KEYS.length) % KEYS.length], { focus: true });
  }

  document.addEventListener('click', function (e) {
    if (!e.target.closest) return;
    var chip = e.target.closest('[data-dh-gelisme]');
    if (!chip) return;
    e.preventDefault();
    render(chip.getAttribute('data-dh-gelisme'));
  });

  /* Klavye: radiogroup semantiği — ok tuşları seçimi taşır */
  document.addEventListener('keydown', function (e) {
    if (!e.target.closest || !e.target.closest('[data-dh-gelisme]')) return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { e.preventDefault(); step(1); }
    else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); step(-1); }
    else if (e.key === 'Home') { e.preventDefault(); render(KEYS[0], { focus: true }); }
    else if (e.key === 'End') { e.preventDefault(); render(KEYS[KEYS.length - 1], { focus: true }); }
  });

  buildPicks();
  render(DATA.aktif && G[DATA.aktif] ? DATA.aktif : KEYS[0]);
})();
