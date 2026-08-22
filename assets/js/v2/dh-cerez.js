/* ============================================================================
   Dada Haber v2 — Çerez rıza bandı + Gizlilik Tercih Merkezi

   VERİ SÖZLEŞMESİ — dh-riza.js ile AYNI kaydı paylaşır:
     localStorage["dh-riza"] = { s:1, islevsel:bool, analitik:bool,
                                 pazarlama:bool, t:"<ISO 8601>" }
   Böylece bandan verilen karar `cerezler.html#riza` sayfasında da görünür,
   oradan değiştirilen tercih bant tarafından yeniden sorulmaz.
   "s" sözleşme sürümü; artarsa eski kayıt yok sayılır ve yeniden sorulur.

   Vendor bandı (#uc-gdpr-notification) DOM'da kalır — app-head-bs.js ona
   koşulsuz `addEventListener` bağlıyor, kaldırılırsa hata atar ve o dosya
   v1 arşiviyle paylaşılıyor (değiştirilemez). Bu yüzden CSS ile gizlenir,
   ayrıca burada `gdprAccepted` yazılır ki vendor bir daha açmasın.

   Bu dosya PROTOTİPTİR: gerçek çerez yazmaz/silmez, yalnız tercihi saklar.
   ========================================================================== */
(function () {
  'use strict';

  var KOK = document.querySelector('[data-dh-cerez]');
  if (!KOK) return;

  var ANAHTAR = 'dh-riza';
  var SURUM = 1;
  var ALANLAR = ['islevsel', 'analitik', 'pazarlama'];

  var band = KOK.querySelector('.dh-cz__band');
  var perde = KOK.querySelector('[data-dh-cerez-perde]');
  var panel = KOK.querySelector('[data-dh-cerez-panel]');
  var kutular = {};
  ALANLAR.forEach(function (ad) {
    kutular[ad] = KOK.querySelector('[data-dh-cerez-alan="' + ad + '"]');
  });

  var sonOdak = null;

  function oku() {
    try {
      var ham = localStorage.getItem(ANAHTAR);
      if (!ham) return null;
      var v = JSON.parse(ham);
      if (!v || v.s !== SURUM) return null;
      return v;
    } catch (e) { return null; }
  }

  function yaz(deger) {
    var kayit = { s: SURUM, t: new Date().toISOString() };
    ALANLAR.forEach(function (ad) { kayit[ad] = !!deger[ad]; });
    try {
      localStorage.setItem(ANAHTAR, JSON.stringify(kayit));
      localStorage.setItem('gdprAccepted', 'true');   // vendor bandı susturulur
    } catch (e) {}
    return kayit;
  }

  function kutulariDoldur(v) {
    ALANLAR.forEach(function (ad) {
      if (kutular[ad]) kutular[ad].checked = !!(v && v[ad]);
    });
  }

  function bandiKapat() {
    KOK.hidden = true;
    document.documentElement.classList.remove('dh-cz-acik');
  }

  function panelAc() {
    sonOdak = document.activeElement;
    kutulariDoldur(oku() || {});
    perde.hidden = false;
    panel.hidden = false;
    document.documentElement.classList.add('dh-cz-kilit');
    var ilk = panel.querySelector('button, input');
    if (ilk) ilk.focus();
    document.addEventListener('keydown', tuS);
  }

  function panelKapat() {
    perde.hidden = true;
    panel.hidden = true;
    document.documentElement.classList.remove('dh-cz-kilit');
    document.removeEventListener('keydown', tuS);
    if (sonOdak && sonOdak.focus) sonOdak.focus();
  }

  function tuS(e) {
    if (e.key === 'Escape') { panelKapat(); return; }
    if (e.key !== 'Tab') return;
    var od = panel.querySelectorAll('button, input, a[href]');
    if (!od.length) return;
    var ilk = od[0], son = od[od.length - 1];
    if (e.shiftKey && document.activeElement === ilk) { e.preventDefault(); son.focus(); }
    else if (!e.shiftKey && document.activeElement === son) { e.preventDefault(); ilk.focus(); }
  }

  function karar(deger) {
    yaz(deger);
    panelKapat();
    bandiKapat();
    // Rıza kararı verildikten SONRA bildirim kartı sırasını alsın.
    document.dispatchEvent(new CustomEvent('dh:riza-verildi'));
  }

  KOK.querySelector('[data-dh-cerez-ac]').addEventListener('click', panelAc);
  KOK.querySelector('[data-dh-cerez-panel-kapat]').addEventListener('click', panelKapat);
  perde.addEventListener('click', panelKapat);

  KOK.querySelector('[data-dh-cerez-kabul]').addEventListener('click', function () {
    karar({ islevsel: true, analitik: true, pazarlama: true });
  });
  KOK.querySelector('[data-dh-cerez-red]').addEventListener('click', function () {
    karar({ islevsel: false, analitik: false, pazarlama: false });
  });
  KOK.querySelector('[data-dh-cerez-tumu]').addEventListener('click', function () {
    kutulariDoldur({ islevsel: true, analitik: true, pazarlama: true });
    karar({ islevsel: true, analitik: true, pazarlama: true });
  });
  KOK.querySelector('[data-dh-cerez-onay]').addEventListener('click', function () {
    var d = {};
    ALANLAR.forEach(function (ad) { d[ad] = kutular[ad] && kutular[ad].checked; });
    karar(d);
  });
  // Bandı X ile kapatmak KARAR DEĞİLDİR: hiçbir isteğe bağlı çerez açılmaz,
  // kayıt da yazılmaz — bir sonraki ziyarette yeniden sorulur.
  KOK.querySelector('[data-dh-cerez-kapat]').addEventListener('click', bandiKapat);

  // Kayıt varsa bant hiç açılmaz.
  var mevcut = oku();
  if (mevcut) {
    kutulariDoldur(mevcut);
    try { localStorage.setItem('gdprAccepted', 'true'); } catch (e) {}
    // Sayfadaki "tercihlerimi değiştir" bağlantıları paneli açabilsin.
  } else {
    KOK.hidden = false;
    document.documentElement.classList.add('dh-cz-acik');
  }

  // Her yerden çağrılabilir kanca: <a href="#" data-dh-cerez-tercih>
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target.closest('[data-dh-cerez-tercih]') : null;
    if (!t) return;
    e.preventDefault();
    panelAc();
  });
})();
