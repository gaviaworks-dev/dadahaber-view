/* R7-Y — YORUM ETKİLEŞİMLERİ: YANITLA + BİLDİR
   ------------------------------------------------------------------
   Kapsam
     1) "Yanıtla" — yorumun hemen altında satır içi yanıt yazma alanı.
        Aynı anda tek alan açık kalır; Esc kapatır; odak metin alanına
        gider, kapanınca düğmeye döner.
     2) "Bildir" — yorumdan kopmadan çalışan şikâyet modalı.
        role="dialog" + aria-modal, focus trap, Esc, odak iadesi,
        arka plan kaydırma kilidi.

   NEDEN AYRI SAYFA DEĞİL MODAL
     Bildirme, uzun bir haber metninin dibindeki tek bir yoruma ait
     mikro görev. Ayrı sayfa (yorum-bildir.html) üç şeyi bozardı:
     (a) okuma konumu kaybolur, geri dönünce yorum listesi en baştan
     açılır; (b) hangi yorumun bildirildiği bilgisi backend olmadan
     ancak sorgu dizesiyle taşınabilir — doğrulanamaz ve kırılgan;
     (c) vazgeçme maliyeti artar. Modal, bildirilen yorumu ekranda
     tutar, Esc ile geri alınabilir ve tek bir DOM kopyasıyla sekiz
     sayfaya yayılır.

   YAYILIM
     Markup üretimi tamamen çalışma anında. Bir sayfaya eklemek için
     tek satır yeter:
       <script defer src="./assets/js/dh-yorum.js"></script>
     .dh-rev__act--reply / --report düğmeleri DOM'dan bulunur, modal
     <body> sonuna sayfa başına BİR kez enjekte edilir.

   Kütüphane yok, vanilla. Backend yok: gönderim sahte yorum ÜRETMEZ,
   yalnız "incelemeye alındı" bilgisi verir.
   ================================================================== */
(function () {
  'use strict';

  var replyBtns = document.querySelectorAll('.dh-rev__act--reply');
  var reportBtns = document.querySelectorAll('.dh-rev__act--report');
  if (!replyBtns.length && !reportBtns.length) return;

  var MAX_REPLY = 600;
  var MAX_NOTE = 500;
  var uid = 0;

  /* Odaklanabilir öğe seçicisi — focus trap ve ilk odak için. */
  var FOCUSABLE = 'a[href], button:not([disabled]), input:not([disabled]),' +
    ' select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

  function focusables(root) {
    return Array.prototype.filter.call(
      root.querySelectorAll(FOCUSABLE),
      function (el) {
        return !el.hasAttribute('hidden') &&
          el.offsetWidth + el.offsetHeight > 0 &&
          !el.closest('[hidden]');
      }
    );
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  /* Bir aksiyon düğmesinden o yorumun kimliğini çıkar.
     İç içe yanıtta da doğru çalışır: en yakın .dh-rev__body kendi
     gövdesidir, ebeveyninki değil. */
  function commentOf(btn) {
    var body = btn.closest('.dh-rev__body');
    if (!body) return null;
    var nameEl = body.querySelector(':scope > .dh-rev__head .dh-rev__name');
    var whenEl = body.querySelector(':scope > .dh-rev__head .dh-rev__when');
    var textEl = body.querySelector(':scope > .dh-rev__text');
    return {
      body: body,
      name: nameEl ? nameEl.textContent.trim() : 'Okur',
      when: whenEl ? whenEl.textContent.trim() : '',
      text: textEl ? textEl.textContent.replace(/\s+/g, ' ').trim() : ''
    };
  }

  /* Metnin ilk satırı: cümle sonu ya da 140 karakter. */
  function firstLine(t) {
    if (!t) return '';
    var cut = t.search(/[.!?…](\s|$)/);
    if (cut > 24 && cut < 160) return t.slice(0, cut + 1);
    return t.length > 140 ? t.slice(0, 140).replace(/\s\S*$/, '') + '…' : t;
  }

  /* ================================================================
     1) YANITLA — satır içi yanıt alanı
     ================================================================ */
  var openForm = null;   // açık .dh-yn
  var openOwner = null;  // onu açan düğme

  function closeReply(returnFocus) {
    if (!openForm) return;
    var owner = openOwner;
    openForm.remove();
    openForm = null;
    openOwner = null;
    if (owner) {
      owner.setAttribute('aria-expanded', 'false');
      owner.removeAttribute('aria-controls');
      if (returnFocus) owner.focus();
    }
  }

  function buildReply(btn, info) {
    var n = ++uid;
    var ids = {
      form: 'dh-yn-' + n,
      area: 'dh-yn-a-' + n,
      cnt: 'dh-yn-c-' + n,
      err: 'dh-yn-e-' + n
    };

    var form = document.createElement('form');
    form.className = 'dh-yn';
    form.id = ids.form;
    form.setAttribute('novalidate', '');
    form.innerHTML =
      '<p class="dh-yn__to"><i class="fas fa-reply" aria-hidden="true"></i>' +
        '<span><b>@' + esc(info.name) + '</b>’a yanıt</span></p>' +
      '<label class="dh-yn__label" for="' + ids.area + '">Yanıtın</label>' +
      '<textarea class="dh-yn__area" id="' + ids.area + '" rows="3" maxlength="' + MAX_REPLY + '"' +
        ' aria-describedby="' + ids.cnt + '"' +
        ' placeholder="Yorumun hangi bölümüne yanıt veriyorsun?"></textarea>' +
      '<p class="dh-yn__err" id="' + ids.err + '" hidden>' +
        '<i class="fas fa-exclamation-circle" aria-hidden="true"></i>' +
        '<span>Yanıt metni boş olamaz. Yanıtını yazıp yeniden dene.</span></p>' +
      '<div class="dh-yn__foot">' +
        '<span class="dh-yn__count" id="' + ids.cnt + '">0 / ' + MAX_REPLY + ' karakter</span>' +
        '<span class="dh-yn__btns">' +
          '<button type="button" class="dh-yn__btn dh-yn__btn--ghost" data-yn-cancel>Vazgeç</button>' +
          '<button type="submit" class="dh-yn__btn dh-yn__btn--go">Yanıtla</button>' +
        '</span>' +
      '</div>';

    var area = form.querySelector('.dh-yn__area');
    var cnt = form.querySelector('.dh-yn__count');
    var err = form.querySelector('.dh-yn__err');

    area.addEventListener('input', function () {
      cnt.textContent = area.value.length + ' / ' + MAX_REPLY + ' karakter';
      cnt.classList.toggle('is-near', area.value.length > MAX_REPLY - 60);
      if (area.value.trim()) clearErr();
    });

    function clearErr() {
      err.hidden = true;
      err.removeAttribute('role');
      area.removeAttribute('aria-invalid');
      area.setAttribute('aria-describedby', ids.cnt);
    }

    function showErr() {
      err.hidden = false;
      err.setAttribute('role', 'alert');
      area.setAttribute('aria-invalid', 'true');
      area.setAttribute('aria-describedby', ids.err + ' ' + ids.cnt);
      area.focus();
    }

    form.querySelector('[data-yn-cancel]').addEventListener('click', function () {
      closeReply(true);
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!area.value.trim()) { showErr(); return; }
      var owner = openOwner;
      var host = info.body;
      closeReply(false);
      // Sahte yorum eklemiyoruz — backend yok, yanıltıcı olurdu.
      var ok = document.createElement('p');
      ok.className = 'dh-yn__ok';
      ok.setAttribute('role', 'status');
      ok.innerHTML = '<i class="fas fa-check-circle" aria-hidden="true"></i>' +
        '<span>Yanıtın alındı. İncelendikten sonra yayımlanacak.</span>';
      host.appendChild(ok);
      if (owner) owner.focus();
    });

    form.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' || e.key === 'Esc') {
        e.stopPropagation();
        closeReply(true);
      }
    });

    return form;
  }

  Array.prototype.forEach.call(replyBtns, function (btn) {
    btn.setAttribute('aria-expanded', 'false');
    btn.addEventListener('click', function () {
      if (openOwner === btn) { closeReply(true); return; }
      closeReply(false);                 // aynı anda tek alan
      var info = commentOf(btn);
      if (!info) return;
      var form = buildReply(btn, info);
      var stale = info.body.querySelector(':scope > .dh-yn__ok');
      if (stale) stale.remove();
      info.body.appendChild(form);       // .dh-rev__replies'in ardına, aynı rayda
      openForm = form;
      openOwner = btn;
      btn.setAttribute('aria-expanded', 'true');
      btn.setAttribute('aria-controls', form.id);
      form.querySelector('.dh-yn__area').focus();
    });
  });

  /* ================================================================
     2) BİLDİR — modal
     ================================================================ */
  if (!reportBtns.length) return;

  var REASONS = [
    ['hakaret', 'Hakaret veya nefret söylemi'],
    ['spam', 'Spam veya reklam'],
    ['yanlis', 'Yanlış bilgi'],
    ['kisisel', 'Kişisel veri paylaşımı'],
    ['mustehcen', 'Müstehcen içerik'],
    ['diger', 'Diğer']
  ];

  var modal = document.createElement('div');
  modal.className = 'dh-bil';
  modal.hidden = true;
  modal.innerHTML =
    '<div class="dh-bil__veil" data-bil-veil></div>' +
    '<div class="dh-bil__box" role="dialog" aria-modal="true"' +
      ' aria-labelledby="dh-bil-title" tabindex="-1">' +
      '<div class="dh-bil__head">' +
        '<h2 class="dh-bil__title" id="dh-bil-title">Yorumu bildir</h2>' +
        '<button type="button" class="dh-bil__x" data-bil-close aria-label="Bildirim penceresini kapat">' +
          '<i class="fas fa-times" aria-hidden="true"></i></button>' +
      '</div>' +
      '<form class="dh-bil__form" novalidate>' +
        '<div class="dh-bil__quote">' +
          '<span class="dh-bil__qwho"><b data-bil-name></b><span data-bil-when></span></span>' +
          '<p class="dh-bil__qtext" data-bil-text></p>' +
        '</div>' +
        '<fieldset class="dh-bil__set">' +
          '<legend class="dh-bil__legend">Bildirim sebebi</legend>' +
          '<p class="dh-bil__err" id="dh-bil-err-reason" hidden>' +
            '<i class="fas fa-exclamation-circle" aria-hidden="true"></i>' +
            '<span>Bir sebep seç, sonra gönder.</span></p>' +
          REASONS.map(function (r, i) {
            return '<label class="dh-bil__opt"><input type="radio" name="dh-bil-reason"' +
              ' value="' + r[0] + '" id="dh-bil-r' + i + '"' +
              (r[0] === 'diger' ? ' aria-controls="dh-bil-other"' : '') +
              '><span>' + r[1] + '</span></label>';
          }).join('') +
        '</fieldset>' +
        '<div class="dh-bil__cond" id="dh-bil-other" hidden>' +
          '<label class="dh-bil__label" for="dh-bil-other-in">Sebebini kısaca yaz</label>' +
          '<input type="text" class="dh-bil__in" id="dh-bil-other-in" maxlength="120"' +
            ' placeholder="Örn. başkasının adına yazılmış yorum">' +
          '<p class="dh-bil__err" id="dh-bil-err-other" hidden>' +
            '<i class="fas fa-exclamation-circle" aria-hidden="true"></i>' +
            '<span>"Diğer" seçtiğinde sebebini yazman gerekiyor.</span></p>' +
        '</div>' +
        '<div class="dh-bil__field">' +
          '<label class="dh-bil__label" for="dh-bil-note">Açıklama <span class="dh-bil__opt-tag">isteğe bağlı</span></label>' +
          '<textarea class="dh-bil__in dh-bil__area" id="dh-bil-note" rows="3" maxlength="' + MAX_NOTE + '"' +
            ' aria-describedby="dh-bil-note-c"' +
            ' placeholder="Editör ekibinin bilmesi gereken bir ayrıntı var mı?"></textarea>' +
          '<span class="dh-bil__count" id="dh-bil-note-c">0 / ' + MAX_NOTE + ' karakter</span>' +
        '</div>' +
        '<p class="dh-bil__kvkk"><i class="fas fa-lock" aria-hidden="true"></i>' +
          '<span>Bildirimin yalnızca editör incelemesi için işlenir, yorum sahibiyle paylaşılmaz. ' +
          '<a href="kvkk.html">KVKK Aydınlatma Metni</a></span></p>' +
        '<div class="dh-bil__foot">' +
          '<button type="button" class="dh-yn__btn dh-yn__btn--ghost" data-bil-close>Vazgeç</button>' +
          '<button type="submit" class="dh-yn__btn dh-yn__btn--go">Bildirimi gönder</button>' +
        '</div>' +
      '</form>' +
      '<div class="dh-bil__done" hidden>' +
        '<i class="fas fa-check-circle" aria-hidden="true"></i>' +
        '<h3>Bildirimin alındı</h3>' +
        '<p>Editör ekibi yorumu inceleyecek. Sonucu e-posta ile bildirmiyoruz; ' +
          'kural ihlali görülürse yorum yayından kaldırılır.</p>' +
        '<button type="button" class="dh-yn__btn dh-yn__btn--go" data-bil-close>Kapat</button>' +
      '</div>' +
    '</div>';
  document.body.appendChild(modal);

  var box = modal.querySelector('.dh-bil__box');
  var form = modal.querySelector('.dh-bil__form');
  var done = modal.querySelector('.dh-bil__done');
  var other = modal.querySelector('#dh-bil-other');
  var otherIn = modal.querySelector('#dh-bil-other-in');
  var note = modal.querySelector('#dh-bil-note');
  var noteC = modal.querySelector('#dh-bil-note-c');
  var errReason = modal.querySelector('#dh-bil-err-reason');
  var errOther = modal.querySelector('#dh-bil-err-other');
  var radios = modal.querySelectorAll('input[name="dh-bil-reason"]');
  var lastFocus = null;
  var padWas = '';

  note.addEventListener('input', function () {
    noteC.textContent = note.value.length + ' / ' + MAX_NOTE + ' karakter';
    noteC.classList.toggle('is-near', note.value.length > MAX_NOTE - 60);
  });

  Array.prototype.forEach.call(radios, function (r) {
    r.addEventListener('change', function () {
      // Görsel işaret + koşullu alan aynı yerde yönetilir.
      Array.prototype.forEach.call(radios, function (o) {
        o.closest('.dh-bil__opt').classList.toggle('is-on', o.checked);
      });
      var isOther = r.value === 'diger' && r.checked;
      other.hidden = !isOther;
      hideErr(errReason, null);
      if (isOther) otherIn.focus();
      else hideErr(errOther, otherIn);
    });
  });

  otherIn.addEventListener('input', function () {
    if (otherIn.value.trim()) hideErr(errOther, otherIn);
  });

  function showErr(el, field) {
    el.hidden = false;
    el.setAttribute('role', 'alert');
    if (field) {
      field.setAttribute('aria-invalid', 'true');
      field.setAttribute('aria-describedby', el.id);
      field.focus();
    }
  }

  function hideErr(el, field) {
    el.hidden = true;
    el.removeAttribute('role');
    if (field) {
      field.removeAttribute('aria-invalid');
      field.removeAttribute('aria-describedby');
    }
  }

  function resetForm() {
    form.reset();
    form.hidden = false;
    done.hidden = true;
    other.hidden = true;
    hideErr(errReason, null);
    hideErr(errOther, otherIn);
    noteC.textContent = '0 / ' + MAX_NOTE + ' karakter';
    noteC.classList.remove('is-near');
    Array.prototype.forEach.call(radios, function (r) {
      r.closest('.dh-bil__opt').classList.remove('is-on');
    });
  }

  function openModal(btn) {
    var info = commentOf(btn);
    if (!info) return;
    closeReply(false);
    lastFocus = btn;
    modal.querySelector('[data-bil-name]').textContent = info.name;
    modal.querySelector('[data-bil-when]').textContent = info.when ? ' · ' + info.when : '';
    modal.querySelector('[data-bil-text]').textContent = firstLine(info.text);
    resetForm();

    // Arka plan kaydırması dursun; kaydırma çubuğu payı telafi edilsin.
    var gap = window.innerWidth - document.documentElement.clientWidth;
    padWas = document.body.style.paddingRight;
    if (gap > 0) document.body.style.paddingRight = gap + 'px';
    document.documentElement.classList.add('dh-bil-lock');

    modal.hidden = false;
    box.focus();
  }

  function closeModal() {
    if (modal.hidden) return;
    modal.hidden = true;
    document.documentElement.classList.remove('dh-bil-lock');
    document.body.style.paddingRight = padWas;
    if (lastFocus && document.contains(lastFocus)) lastFocus.focus();
    lastFocus = null;
  }

  Array.prototype.forEach.call(modal.querySelectorAll('[data-bil-close]'), function (b) {
    b.addEventListener('click', closeModal);
  });
  modal.querySelector('[data-bil-veil]').addEventListener('click', closeModal);

  modal.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' || e.key === 'Esc') {
      e.stopPropagation();
      closeModal();
      return;
    }
    if (e.key !== 'Tab') return;
    var list = focusables(box);
    if (!list.length) { e.preventDefault(); box.focus(); return; }
    var first = list[0];
    var last = list[list.length - 1];
    var act = document.activeElement;
    if (e.shiftKey) {
      if (act === first || act === box || !box.contains(act)) {
        e.preventDefault();
        last.focus();
      }
    } else if (act === last) {
      e.preventDefault();
      first.focus();
    }
  });

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var picked = modal.querySelector('input[name="dh-bil-reason"]:checked');
    if (!picked) {
      showErr(errReason, null);
      radios[0].focus();
      return;
    }
    if (picked.value === 'diger' && !otherIn.value.trim()) {
      showErr(errOther, otherIn);
      return;
    }
    form.hidden = true;
    done.hidden = false;
    done.setAttribute('role', 'status');
    done.querySelector('[data-bil-close]').focus();
  });

  Array.prototype.forEach.call(reportBtns, function (btn) {
    btn.setAttribute('aria-haspopup', 'dialog');
    btn.addEventListener('click', function () { openModal(btn); });
  });
})();
