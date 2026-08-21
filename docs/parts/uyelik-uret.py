# -*- coding: utf-8 -*-
"""giris.html · uye-ol.html · sifremi-unuttum.html üretir.

Üçü aynı iskeleti paylaşır (sol: neden hesap · sağ: form). Tek yerde durur ki
sayfalar birbirinden sapmasın. Form iskeleti .dh-kform'dan gelir, davranış
assets/js/v2/dh-giris.js'te. Backend yok: gönderim yapılmaz, veri yazılmaz.
"""
import os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)

SABLON = "docs/parts/sayfa-sablon.html"

FAYDA = [
    ("fa-bookmark", "Kaydet ve sonra oku",
     "Beğendiğin haberleri kaydet, okuma listeni her cihazdan sürdür."),
    ("fa-bell", "Yalnız istediğin bildirim",
     "Takip ettiğin kategori, şehir ve takımlar için bildirim al; gerisi sessiz."),
    ("fa-compass", "Keşfet sana göre",
     "Dada Özet, Bağlam ve Doğrula formatları ilgi alanına göre sıralanır."),
    ("fa-sliders-h", "Ayarların seninle gelir",
     "Şehrin, takımın ve görünüm tercihin hesabına bağlı kalır."),
]

PROTO = ('Bu bir arayüz prototipidir. Form gerçek bir kayıt veya giriş yapmaz; '
         'girdiğin bilgiler hiçbir yere gönderilmez ve tarayıcında saklanmaz.')


def sekme(aktif):
    o = ['              <nav class="dh-auth__tabs" aria-label="Hesap işlemleri">\n']
    for ad, h, k in (("Giriş Yap", "giris.html", "giris"), ("Üye Ol", "uye-ol.html", "uyeol")):
        ek = ' aria-current="page"' if k == aktif else ''
        o.append('                <a href="%s"%s>%s</a>\n' % (h, ek, ad))
    o.append('              </nav>\n')
    return "".join(o)


def alan(id_, etiket, tur, ph, **kw):
    zor = kw.get("zorunlu", True)
    ipucu = kw.get("ipucu")
    hata = kw.get("hata", "Bu alan zorunlu.")
    oto = kw.get("oto", "")
    minlen = kw.get("minlen")
    eslesir = kw.get("eslesir")
    o = ['                  <div class="dh-kform__f">\n']
    o.append('                    <label for="%s">%s%s</label>\n'
             % (id_, etiket, ' <span class="dh-kform__req" aria-hidden="true">*</span>' if zor else
                ' <span class="dh-kform__hint">(isteğe bağlı)</span>'))
    nitelik = ''
    if zor:
        nitelik += ' required'
    if oto:
        nitelik += ' autocomplete="%s"' % oto
    if minlen:
        nitelik += ' minlength="%d"' % minlen
    if eslesir:
        nitelik += ' data-dh-eslesir="%s"' % eslesir
    nitelik += ' data-dh-bos="%s"' % hata

    if tur == "password":
        o.append('                    <div class="dh-auth__pw">\n')
        o.append('                      <input class="dh-input" id="%s" name="%s" type="password" placeholder="%s"%s>\n'
                 % (id_, id_, ph, nitelik))
        o.append('                      <button class="dh-auth__eye" type="button" aria-label="Şifreyi göster" aria-pressed="false">')
        o.append('<i class="fas fa-eye" aria-hidden="true"></i></button>\n')
        o.append('                    </div>\n')
    else:
        o.append('                    <input class="dh-input" id="%s" name="%s" type="%s" placeholder="%s"%s>\n'
                 % (id_, id_, tur, ph, nitelik))
    o.append('                    <span class="dh-kform__err">%s</span>\n' % hata)
    if ipucu:
        o.append('                    <span class="dh-kform__hint">%s</span>\n' % ipucu)
    o.append('                  </div>\n')
    return "".join(o)


def onay(id_, metin, hata):
    return ('                  <div class="dh-kform__f">\n'
            '                    <label class="dh-kform__chk">\n'
            '                      <input type="checkbox" id="%s" name="%s" required data-dh-bos="%s">\n'
            '                      <span>%s</span>\n'
            '                    </label>\n'
            '                    <span class="dh-kform__err">%s</span>\n'
            '                  </div>\n' % (id_, id_, hata, metin, hata))


def bitti(metin):
    return ('                  <div class="dh-kform__done" data-dh-form-done role="status">\n'
            '                    <i class="fas fa-circle-check" aria-hidden="true"></i>\n'
            '                    <span>%s <b>Prototip sürümünde form gerçek bir gönderim yapmaz.</b></span>\n'
            '                  </div>\n' % metin)


def alternatif():
    return ('              <div class="dh-auth__or">veya</div>\n'
            '              <div class="dh-auth__alt">\n'
            '                <a href="#"><i class="fa-brands fa-google" aria-hidden="true"></i>Google ile devam et</a>\n'
            '                <a href="#"><i class="fa-brands fa-apple" aria-hidden="true"></i>Apple ile devam et</a>\n'
            '              </div>\n')


def govde(baslik, kicker, lead, sag, faydalar=True):
    o = []
    w = o.append
    w('        <section class="section panel dh-auth">\n')
    w('          <div class="container max-w-xl">\n')
    w('            <nav class="dh-art-crumb" aria-label="Sayfa yolu">')
    w('<a href="index.html" aria-label="Anasayfa"><i class="fas fa-home-lg-alt" aria-hidden="true"></i></a>')
    w('<i class="fas fa-chevron-right" aria-hidden="true"></i>')
    w('<span aria-current="page">%s</span></nav>\n' % baslik)
    w('            <div class="dh-auth__grid">\n')
    w('              <aside class="dh-auth__side">\n')
    w('                <span class="dh-auth__kicker">%s</span>\n' % kicker)
    w('                <h1 class="dh-auth__t">%s</h1>\n' % baslik)
    w('                <p class="dh-auth__l">%s</p>\n' % lead)
    if faydalar:
        w('                <ul class="dh-auth__ben">\n')
        for ik, b, a in FAYDA:
            w('                  <li><i class="fas %s" aria-hidden="true"></i><span><b>%s</b>'
              '<span>%s</span></span></li>\n' % (ik, b, a))
        w('                </ul>\n')
    w('              </aside>\n')
    w('              <div class="dh-auth__main">\n')
    w(sag)
    w('                <div class="dh-auth__proto">\n')
    w('                  <i class="fas fa-shield-alt" aria-hidden="true"></i>\n')
    w('                  <span>%s</span>\n' % PROTO)
    w('                </div>\n')
    w('              </div>\n')
    w('            </div>\n          </div>\n        </section>\n')
    return "".join(o)


# ------------------------------------------------------------------- giriş
giris_form = (
    sekme("giris")
    + '              <form class="dh-kform dh-auth__form" data-dh-auth="giris" novalidate>\n'
    + alan("giris-eposta", "E-posta", "email", "ornek@eposta.com",
           oto="email", hata="E-posta adresinizi yazın.")
    + alan("giris-sifre", "Şifre", "password", "Şifreniz", oto="current-password",
           hata="Şifrenizi yazın.")
    + '                  <div class="dh-kform__f">\n'
    + '                    <div class="dh-auth__row">\n'
    + '                      <label class="dh-kform__chk"><input type="checkbox" id="giris-hatirla" name="hatirla">'
      '<span>Beni hatırla</span></label>\n'
    + '                      <a class="dh-auth__link" href="sifremi-unuttum.html">Şifremi unuttum</a>\n'
    + '                    </div>\n'
    + '                  </div>\n'
    + '                  <div class="dh-kform__act">\n'
    + '                    <button class="dh-btn" type="submit">Giriş yap '
      '<i class="fas fa-right-to-bracket" aria-hidden="true"></i></button>\n'
    + '                  </div>\n'
    + bitti('Giriş bilgileri alındı.')
    + '              </form>\n'
    + alternatif()
    + '              <p class="dh-auth__foot">Hesabın yok mu? <a href="uye-ol.html">Üye ol</a> — '
      'kaydetme, bildirim ve kişiselleştirme özellikleri açılsın.</p>\n'
)

# ------------------------------------------------------------------ üye ol
uyeol_form = (
    sekme("uyeol")
    + '              <form class="dh-kform dh-auth__form" data-dh-auth="uyeol" novalidate>\n'
    + alan("uye-ad", "Ad soyad", "text", "Adınız ve soyadınız", oto="name",
           hata="Ad ve soyadınızı yazın.")
    + alan("uye-eposta", "E-posta", "email", "ornek@eposta.com", oto="email",
           hata="E-posta adresinizi yazın.",
           ipucu="Doğrulama bağlantısı bu adrese gönderilir.")
    + alan("uye-sifre", "Şifre", "password", "En az 8 karakter", oto="new-password",
           minlen=8, hata="Şifre en az 8 karakter olmalı.")
    + '                  <div class="dh-kform__f">\n'
    + '                    <div class="dh-auth__pwm" data-dh-pwm="uye-sifre" data-guc="0">\n'
    + '                      <div class="dh-auth__pwbar" aria-hidden="true"><span></span><span></span>'
      '<span></span><span></span></div>\n'
    + '                      <span class="dh-auth__pwl" role="status">ŞİFRE GÜCÜ</span>\n'
    + '                    </div>\n'
    + '                  </div>\n'
    + alan("uye-sifre2", "Şifre tekrar", "password", "Şifreyi yeniden yazın",
           oto="new-password", eslesir="uye-sifre", hata="Şifreyi yeniden yazın.")
    + onay("uye-kosul",
           'Kullanım koşullarını ve <a href="kvkk.html">KVKK aydınlatma metnini</a> okudum, kabul ediyorum.',
           "Devam etmek için koşulları kabul edin.")
    + '                  <div class="dh-kform__f">\n'
    + '                    <label class="dh-kform__chk"><input type="checkbox" id="uye-bulten" name="bulten">'
      '<span>Günün özeti bültenine abone olmak istiyorum. İstediğin an bırakabilirsin.</span></label>\n'
    + '                  </div>\n'
    + '                  <div class="dh-kform__act">\n'
    + '                    <button class="dh-btn" type="submit">Üyeliği tamamla '
      '<i class="fas fa-user-plus" aria-hidden="true"></i></button>\n'
    + '                  </div>\n'
    + bitti('Üyelik bilgileri alındı. Gerçek sürümde e-postana bir doğrulama bağlantısı gönderilir.')
    + '              </form>\n'
    + alternatif()
    + '              <p class="dh-auth__foot">Zaten üye misin? <a href="giris.html">Giriş yap</a>.</p>\n'
)

# ------------------------------------------------------- şifremi unuttum
sifre_form = (
    '              <ol class="dh-auth__steps">\n'
    '                <li class="is-on" data-n="1">E-posta</li>\n'
    '                <li data-n="2">Bağlantı</li>\n'
    '                <li data-n="3">Yeni şifre</li>\n'
    '              </ol>\n'
    + '              <form class="dh-kform dh-auth__form" data-dh-auth="sifre" novalidate>\n'
    + alan("sifre-eposta", "Hesabının e-posta adresi", "email", "ornek@eposta.com",
           oto="email", hata="E-posta adresinizi yazın.",
           ipucu="Kayıtlı bir adres yazdıysan sıfırlama bağlantısı gönderilir. "
                 "Güvenlik gereği adresin kayıtlı olup olmadığı belirtilmez.")
    + '                  <div class="dh-kform__act">\n'
    + '                    <button class="dh-btn" type="submit">Sıfırlama bağlantısı gönder '
      '<i class="fas fa-paper-plane" aria-hidden="true"></i></button>\n'
    + '                  </div>\n'
    + bitti('Sıfırlama bağlantısı gönderildi. Gelen kutunu ve gereksiz posta klasörünü kontrol et; '
            'bağlantı 60 dakika geçerlidir.')
    + '              </form>\n'
    + '              <p class="dh-auth__foot"><a href="giris.html">'
      '<i class="fas fa-arrow-left" aria-hidden="true"></i> Giriş ekranına dön</a> · '
      'Hesabın yok mu? <a href="uye-ol.html">Üye ol</a></p>\n'
)

SAYFALAR = [
    ("giris.html", "Giriş Yap", "Dada Haber Hesabı",
     "Kaydettiğin haberler, bildirimlerin ve tercihlerin hesabına bağlı. "
     "Giriş yap, kaldığın yerden devam et.", giris_form, True),
    ("uye-ol.html", "Üye Ol", "Ücretsiz Hesap",
     "Dakikalar içinde hesabını aç; gündemi kendi ilgi alanına göre kur. "
     "Üyelik ücretsiz, istediğin an silebilirsin.", uyeol_form, True),
    ("sifremi-unuttum.html", "Şifremi Unuttum", "Şifre Sıfırlama",
     "E-posta adresini yaz, sıfırlama bağlantısını gönderelim. "
     "Bağlantı 60 dakika geçerlidir ve yalnız bir kez kullanılır.", sifre_form, False),
]

sablon = open(SABLON, encoding="utf-8").read()
yuva = re.compile(r"[ \t]*<!-- ={10,} SAYFA GÖVDESİ BURAYA ={10,}.*?={10,} -->\n", re.S)

for dosya, baslik, kicker, lead, form, fayda in SAYFALAR:
    s = sablon
    s = s.replace("<title>SAYFA BAŞLIĞI — Dada Haber</title>",
                  "<title>%s — Dada Haber</title>" % baslik)
    if 'data-dh-cat=""' in s:
        s = s.replace('data-dh-cat=""', 'data-dh-cat="uyelik"', 1)
    else:
        s = re.sub(r'<body\s', '<body data-dh-cat="uyelik" ', s, count=1)
    m = yuva.search(s)
    if not m:
        sys.exit("HATA: şablonda gövde yuvası yok")
    s = s[:m.start()] + govde(baslik, kicker, lead, form, fayda) + s[m.end():]
    # davranış betiği
    s = s.replace('    <script defer src="./assets/js/app.js"></script>',
                  '    <script defer src="./assets/js/app.js"></script>\n'
                  '    <script defer src="./assets/js/v2/dh-giris.js"></script>', 1)
    open(dosya, "w", encoding="utf-8").write(s)
    print("%s yazıldı (%d satır)" % (dosya, len(s.splitlines())))
