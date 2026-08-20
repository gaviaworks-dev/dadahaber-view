/* R3-6 — GÜNLÜK PANEL
   Namaz vakitleri panelinde sıradaki vakti işaretler ve ona kalan süreyi
   yazar. Saatler markup'ta data-dh-prayer="HH:MM" olarak duruyor; backend
   bağlanınca aynı attribute doldurulacak, bu dosya değişmeyecek. */
(function () {
  var panel = document.querySelector('.dh-panel--prayer');
  if (!panel) return;

  var cells = [].slice.call(panel.querySelectorAll('[data-dh-prayer]'));
  var out = panel.querySelector('[data-dh-prayer-countdown]');
  if (!cells.length) return;

  function minutes(hhmm) {
    var m = /^(\d{1,2}):(\d{2})$/.exec((hhmm || '').trim());
    return m ? (+m[1]) * 60 + (+m[2]) : null;
  }

  function label(diff) {
    var h = Math.floor(diff / 60), m = diff % 60;
    if (h > 0) return h + ' sa ' + m + ' dk';
    return m + ' dk';
  }

  function tick() {
    var now = new Date();
    var cur = now.getHours() * 60 + now.getMinutes();

    var nextIndex = -1, nextDiff = Infinity;
    cells.forEach(function (c, i) {
      var t = minutes(c.dataset.dhPrayer);
      if (t === null) return;
      var diff = t - cur;
      if (diff < 0) diff += 24 * 60;          /* ertesi güne sar */
      if (diff < nextDiff) { nextDiff = diff; nextIndex = i; }
    });

    cells.forEach(function (c, i) { c.classList.toggle('is-now', i === nextIndex); });

    if (out && nextIndex > -1) {
      var name = cells[nextIndex].querySelector('.dh-cell__label').textContent.trim();
      out.textContent = name + "'ya " + label(nextDiff) + ' kaldı';
      /* Türkçe ek uyumu: kalın ünlüyle biten adlar 'a', ince olanlar 'e' */
      var last = name.slice(-1).toLowerCase();
      if ('aıouâ'.indexOf(last) > -1) out.textContent = name + "'ya " + label(nextDiff) + ' kaldı';
      else if ('eiöü'.indexOf(last) > -1) out.textContent = name + "'ye " + label(nextDiff) + ' kaldı';
      else out.textContent = name + ' vaktine ' + label(nextDiff) + ' kaldı';
    }
  }

  tick();
  window.setInterval(tick, 30000);
})();
