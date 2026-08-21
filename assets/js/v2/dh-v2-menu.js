/* v2 — perdeleme ana menü + kullanıcı menüsü
   Panelin kendisi CSS'te; burada yalnız AÇMA NİYETİ yönetilir:
   fareyle gecikmeli aç/kapa, dokunmada ilk dokunuş açar, klavyeyle gezinme,
   Escape ile kapanma ve sayfanın geri kalanını perdeleyen katman.
   Vendor'a dokunulmaz; bu dosya yalnız v2 kabuğunu bilir. */
(function () {
  'use strict';

  var bar = document.querySelector('.dh-v2-nav__bar');
  var scrim = null;
  var acik = null;
  var acZ = 0, kapatZ = 0;
  var AC_GECIKME = 90;    // fare geçerken panel çakmasın
  var KAPAT_GECIKME = 220; // panele inerken kaybolmasın

  function scrimKur() {
    if (scrim) return scrim;
    scrim = document.createElement('div');
    scrim.className = 'dh-v2-scrim';
    scrim.setAttribute('aria-hidden', 'true');
    scrim.addEventListener('mouseenter', function () { kapat(); });
    scrim.addEventListener('click', function () { kapat(); });
    document.body.appendChild(scrim);
    return scrim;
  }

  function ac(li) {
    if (acik === li) return;
    if (acik) kapatHemen();
    li.classList.add('is-open');
    var a = li.querySelector(':scope > a');
    if (a) a.setAttribute('aria-expanded', 'true');
    scrimKur().classList.add('is-on');
    acik = li;
  }

  function kapatHemen() {
    if (!acik) return;
    acik.classList.remove('is-open');
    var a = acik.querySelector(':scope > a');
    if (a) a.setAttribute('aria-expanded', 'false');
    acik = null;
    if (scrim) scrim.classList.remove('is-on');
  }

  function kapat() {
    clearTimeout(acZ);
    clearTimeout(kapatZ);
    kapatZ = setTimeout(kapatHemen, KAPAT_GECIKME);
  }

  if (bar) {
    var ogeler = bar.querySelectorAll('.dh-v2-nav__list > li');

    Array.prototype.forEach.call(ogeler, function (li) {
      var tetik = li.querySelector(':scope > a');
      if (!li.querySelector('.dh-mega')) return;

      li.addEventListener('mouseenter', function () {
        clearTimeout(kapatZ);
        clearTimeout(acZ);
        acZ = setTimeout(function () { ac(li); }, AC_GECIKME);
      });
      li.addEventListener('mouseleave', function () {
        clearTimeout(acZ);
        kapat();
      });

      /* Dokunmatikte ilk dokunuş paneli açar, ikincisi kategoriye gider.
         Farede tıklama her zaman gider — kullanıcı yolunu kesmeyiz. */
      if (tetik) {
        tetik.addEventListener('click', function (e) {
          var dokunma = e.pointerType === 'touch' || (!e.pointerType && !window.matchMedia('(hover: hover)').matches);
          if (dokunma && acik !== li) {
            e.preventDefault();
            ac(li);
          }
        });
        tetik.addEventListener('focus', function () {
          clearTimeout(kapatZ);
          ac(li);
        });
      }

      /* Klavyeyle panelden çıkıldığında kontrollü kapan */
      li.addEventListener('focusout', function (e) {
        if (!li.contains(e.relatedTarget)) kapat();
      });
    });

    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape' && e.key !== 'Esc') return;
      if (!acik) return;
      var tetik = acik.querySelector(':scope > a');
      kapatHemen();
      if (tetik) tetik.focus();
    });

    document.addEventListener('click', function (e) {
      if (acik && !acik.contains(e.target)) kapatHemen();
    });
  }

  /* ------------------------------------------------ kullanıcı menüsü */
  var sarmal = document.querySelector('[data-dh-user]');
  if (sarmal) {
    var dugme = sarmal.querySelector('button');
    var kutu = sarmal.querySelector('.dh-v2-user__menu');
    if (dugme && kutu) {
      var kullaniciKapat = function () {
        kutu.hidden = true;
        dugme.setAttribute('aria-expanded', 'false');
      };
      dugme.addEventListener('click', function (e) {
        e.stopPropagation();
        var acikMi = !kutu.hidden;
        kutu.hidden = acikMi;
        dugme.setAttribute('aria-expanded', String(!acikMi));
      });
      document.addEventListener('click', function (e) {
        if (!sarmal.contains(e.target)) kullaniciKapat();
      });
      document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' || e.key === 'Esc') {
          if (!kutu.hidden) { kullaniciKapat(); dugme.focus(); }
        }
      });
    }
  }
})();
