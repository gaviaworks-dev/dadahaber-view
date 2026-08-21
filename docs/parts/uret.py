# -*- coding: utf-8 -*-
"""Dada Haber v2 kabuğu — header/offcanvas/footer üretir.

V1–V2 birleştirme talimatı (21 Ağustos 2026) uygulandı:
  · üst servis bandı kaldırıldı (son dakika/piyasa/hava/şehir/bülten/sosyal)
  · yerine V1'deki gibi kompakt FORMAT BANDI geldi
  · ana menü 11 → 8 başlık; kalanlar "Diğer" perdeleme menüsüne taşındı
  · "Şimdi" → "Anlık" (dosya da anlik.html)
  · karanlık mod anahtarı kabuktan tamamen çıktı
  · sosyal hesaplar YALNIZ footer'da
Menü metni ve sırası elle yazılmaz ki sapma olmasın."""
import io, os

L = "haber-liste.html"   # gerçek sayfası olmayan alt kategoriler için liste şablonu

# --------------------------------------------------------------- format bandı
# V1'in üst şeridi: yayın formatlarını tanıtan kanal şeridi. Ana menü değildir.
FORMAT = [
    ("Haber Dinle", "haber-dinle.html", "fa-headphones"),
    ("Foto Fokus",  "foto-fokus.html",  "fa-camera"),
    ("Video Haber", "video.html",       "fa-play"),
    ("İnfografik",  "infografik.html",  "fa-chart-bar"),
    ("Podcast",     "podcast.html",     "fa-podcast"),
]

# ------------------------------------------------------------------ ana menü
# 8 başlık. Kaldırılan hiçbir kategori silinmedi — hepsi "Diğer" altında.
MENU = [
 ("anlik", "Anlık", "anlik.html",
  "Günün anlık gelişmelerinin toplandığı canlı merkez.",
  # Alt başlıkların her biri kendi sayfası (docs/parts/anlik-uret.py üretir).
  # Canlı Yayın ve Hava Durumu başka bölümlerin sayfalarına gider.
  [(None, [("Son Dakika","son-dakika.html"),("Canlı Gündem","canli-gundem.html"),
           ("Canlı Yayın","video.html#canli"),("Dakika Dakika","dakika-dakika.html"),
           ("Bugün Ne Oldu?","bugun-ne-oldu.html")]),
   (None, [("Gündem Takvimi","gundem-takvimi.html"),("Güncellenen Haberler","guncellenen-haberler.html"),
           ("Afet ve Acil Durum","afet-acil-durum.html"),("Trafik ve Ulaşım","trafik-ulasim.html"),
           ("Hava Durumu","veri-harita.html#hava")])]),

 ("gundem", "Gündem", "gundem.html",
  "Türkiye, siyaset, toplum, hukuk ve yerel haberler.",
  [("Temel kategoriler", [("Siyaset",L),("Türkiye",L),("Toplum",L),("Hukuk",L),
                          ("Güvenlik",L),("Eğitim",L),("Çevre",L),("Afet",L)]),
   ("Yerel haberler", [("Yerel Haberler","gundem.html#yerel"),("İstanbul",L),("Ankara",L),
                       ("İzmir",L),("81 İl","gundem.html#iller")]),
   ("Özgün içerikler", [("Özel Haber",L),("Araştırma",L),("Gündem Analizi",L)])]),

 ("dunya", "Dünya", "dunya.html",
  "Bölgeler, diplomasi ve küresel gelişmeler.",
  [("Bölgeler", [("Avrupa",L),("Orta Doğu",L),("Amerika",L),("Asya Pasifik",L),
                 ("Afrika",L),("Balkanlar",L),("Kafkasya",L),("Türk Dünyası",L)]),
   ("Konular", [("Diplomasi",L),("Küresel Siyaset",L),("Savaş ve Çatışmalar",L),
                ("Göç",L),("Uluslararası Kuruluşlar",L),("Dünya Analizi",L)])]),

 ("ekonomi", "Finans", "ekonomi.html",
  "Piyasalar, kişisel finans, sektörler ve iş dünyası.",
  [("Piyasalar", [("Piyasa Ekranı","finans.html"),("Döviz","doviz.html"),("Altın","altin.html"),
                  ("Borsa","borsa.html"),("Kripto Para","kripto.html"),
                  ("Akaryakıt Fiyatları","finans.html#akaryakit"),
                  ("Faiz Oranları","finans.html#faiz"),
                  ("Ekonomik Takvim","finans.html#takvim")]),
   ("Ekonomi", [("Türkiye Ekonomisi",L),("Dünya Ekonomisi",L),("Bankacılık",L),
                ("Kişisel Finans",L),("Enflasyon",L),("Ekonomi Analizi",L)]),
   ("Sektörler", [("İş Dünyası",L),("Şirketler",L),("Girişimcilik",L),("Çalışma Hayatı",L),
                  ("Enerji",L),("Tarım",L),("Sanayi",L),("Gayrimenkul",L),("Otomotiv",L)])]),

 ("savunma", "Savunma", "savunma.html",
  "Savunma sanayii, millî projeler ve güvenlik gündemi.",
  [("Savunma sanayii", [("Savunma Sanayii","savunma.html"),("Millî Projeler","savunma.html"),
                        ("İHA ve SİHA",L),("Hava Platformları",L),("Deniz Platformları",L),
                        ("Kara Sistemleri",L),("Füze ve Roket Sistemleri",L)]),
   ("Güvenlik", [("Millî Güvenlik",L),("Askerî Operasyonlar",L),("Sınır Güvenliği",L),
                 ("Terörle Mücadele",L),("Uluslararası Güvenlik",L),("NATO",L)]),
   ("İçerikler", [("Savunma Teknolojileri","teknoloji.html"),("İhracat ve Anlaşmalar",L),
                  ("Savunma Analizi",L),("Uzman Görüşleri",L),("Savunma Videoları","video.html")])]),

 ("spor", "Spor", "spor.html",
  "Branşlar, canlı skorlar, puan durumu ve fikstür.",
  [("Branşlar", [("Futbol","futbol.html"),("Basketbol","basketbol.html"),
                 ("Voleybol","voleybol.html"),("Motor Sporları","formula1.html"),
                 ("Bisiklet","bisiklet.html"),("Tenis",L),("Atletizm",L),
                 ("Olimpiyatlar",L),("Geleneksel Sporlar",L),("E-Spor",L)]),
   ("Servisler", [("Canlı Skor","spor.html#canli"),("Puan Durumu","puan-durumu.html"),
                  ("Fikstür","fikstur.html"),("Takımlar","takim.html"),("Transfer",L),
                  ("Millî Takım",L)]),
   ("Takımlar", [("Galatasaray","takim-galatasaray.html"),("Fenerbahçe","takim-fenerbahce.html"),
                 ("Beşiktaş","takim-besiktas.html"),("Trabzonspor","takim-trabzonspor.html"),
                 ("Süper Lig","puan-durumu.html"),("Avrupa Ligleri","puan-durumu.html"),
                 ("Spor Analizi",L),("Spor Video","video.html#spor")])]),

 ("kadin", "Kadın", "kadin.html",
  "Kadın gündemi, sağlık, hak ve yaşam içerikleri.",
  [("Gündem", [("Kadın Gündemi","kadin.html"),("Kadın Hakları",L),("Toplumsal Cinsiyet",L),
               ("Kadın ve Hukuk",L),("Kadın ve Çalışma Hayatı",L),("Başarı Hikâyeleri",L)]),
   ("Sağlık", [("Kadın Sağlığı","kadin.html#saglik"),("Hamilelik","hamilelik.html"),
               ("Anne ve Çocuk","hamilelik.html"),("Beslenme",L),("Ruh Sağlığı",L)]),
   ("Yaşam", [("Moda",L),("Güzellik",L),("Ev ve Yaşam",L),("Astroloji","astroloji.html"),
              ("Kadın Yazarlar","yazar-liste.html")])]),

 ("diger", "Diğer", "diger.html",
  "Ana menüde yer almayan tüm kategoriler ve formatlar.",
  [("Teknoloji ve bilim", [("Teknoloji","teknoloji.html"),("Yapay Zekâ",L),("Bilim",L),
                           ("Uzay",L),("Siber Güvenlik",L),("Yazılım",L),
                           ("Oyun","oyun.html"),("E-Spor",L),("Ürün İncelemeleri",L)]),
   ("Sağlık ve yaşam", [("Sağlık","saglik.html"),("Halk Sağlığı",L),("Beslenme",L),
                        ("Ruh Sağlığı",L),("Hamilelik","hamilelik.html"),
                        ("Otomobil",L),("Seyahat",L),
                        ("Gastronomi","https://dadamutfak.com/")]),
   ("Kültür ve sanat", [("Kültür &amp; Yaşam","kultur-yasam.html"),("Sinema",L),("Dizi",L),
                        ("Müzik",L),("Kitap",L),("Edebiyat",L),("Tiyatro",L),("Sergi",L),
                        ("Astroloji","astroloji.html")]),
   ("Gelecek ve eğitim", [("Gelecek","gelecek.html"),("Eğitim ve Sınavlar",L),("Üniversiteler",L),
                          ("Burslar",L),("Kariyer",L),("İklim",L),("Çevre",L),
                          ("Sürdürülebilirlik",L),("Gençlerin Gündemi",L)]),
   ("Keşfet formatları", [("Keşfet","kesfet.html"),("Dada Özet","dada-ozet.html"),
                          ("Günün 5’i","kesfet.html#gunun5"),("Dada Bağlam","dada-baglam.html"),
                          ("Dada Doğrula","dada-dogrula.html"),
                          ("Farklı Bakışlar","farkli-bakislar.html"),
                          ("Veri &amp; Harita","veri-harita.html"),("Sakin Akış","sakin-akis.html")]),
   ("Medya ve arşiv", [("Video","video.html"),("Video Galeri","video-galeri.html"),
                       ("Foto Fokus","foto-fokus.html"),("İnfografik","infografik.html"),
                       ("Podcast","podcast.html"),("Haber Dinle","haber-dinle.html"),
                       ("Yazarlar","yazar-liste.html"),("Resmî İlanlar","resmi-ilanlar.html"),
                       ("Arşiv","arsiv.html")])]),
]

# ------------------------------------------------------- mobil alt gezinme
# Keşfet ORTADA ve kalıcı vurgulu: Dada Haber'i klasik haber sitesinden ayıran
# ana ürün orası. Dinle/Ara/Hesabım alt menüden çıktı — Dinle "Medya ve
# Formatlar"da, Ara ve Hesabım mobil header'da, karanlık mod menü içinde.
BNAV = [
    ("Anasayfa",   "index.html",       "fas fa-home-lg-alt",   ""),
    ("Son Dakika", "son-dakika.html",  "fas fa-bolt",          ""),
    ("Keşfet",     "kesfet.html",      "fas fa-compass",       "dh-bnav__item--kesfet"),
    ("Video",      "video.html",       "fas fa-play",          ""),
    ("Menü",       "#uc-menu-panel",   "fas fa-bars",          ""),
]

SOSYAL = [("Instagram","fa-instagram","#"),("YouTube","fa-youtube","#"),("X","fa-x-twitter","#"),
          ("Facebook","fa-facebook-f","#"),("LinkedIn","fa-linkedin-in","#"),("TikTok","fa-tiktok","#")]

# ------------------------------------------------------------------- footer
# Üç bağlantı sütunu + toplayıcı kurumsal şerit + yasal şerit.
# Kurumsal ve iletişim ayrı sütunlar değil; tek satırda ve daha az maddeyle.
FOOTER = [
 ("Kategoriler", [("Anlık","anlik.html"),("Gündem","gundem.html"),("Dünya","dunya.html"),
   ("Finans","ekonomi.html"),("Savunma","savunma.html"),("Spor","spor.html"),
   ("Kadın","kadin.html"),("Tüm Kategoriler","diger.html")]),
 ("Formatlar", [("Haber Dinle","haber-dinle.html"),("Foto Fokus","foto-fokus.html"),
   ("Video Haber","video.html"),("İnfografik","infografik.html"),("Podcast","podcast.html"),
   ("Video Galeri","video-galeri.html")]),
 ("Keşfet", [("Dada Özet","dada-ozet.html"),("Dada Bağlam","dada-baglam.html"),
   ("Dada Doğrula","dada-dogrula.html"),("Farklı Bakışlar","farkli-bakislar.html"),
   ("Veri &amp; Harita","veri-harita.html"),("Sakin Akış","sakin-akis.html")]),
]

# Toplayıcı kurumsal şerit — Hakkımızda ve İletişim tek satırda, az maddeyle.
KURUMSAL = [("Hakkımızda","hakkimizda.html"),("Künye","kunye.html"),
            ("Yayın İlkeleri","yayin-ilkeleri.html"),("İletişim","iletisim.html"),
            ("Yardım Merkezi","iletisim.html#yardim"),("Reklam","reklam.html"),
            ("İnsan Kaynakları","coming-soon.html"),("Resmî İlanlar","resmi-ilanlar.html")]

YASAL = [("Kullanım Koşulları","kullanim-sartlari.html"),
         ("Gizlilik ve KVKK","kvkk.html"),
         ("Aydınlatma Metni","aydinlatma-metni.html"),
         ("Çerez Politikası","cerezler.html"),
         ("Açık Rıza Metni","cerezler.html#riza"),
         ("Telif Hakları","kullanim-sartlari.html#telif")]

TELIF = ("Dadahaber.com internet sitesinde yayımlanan haber, yazı, fotoğraf, video, "
         "grafik ve diğer içerikler, izin alınmadan kısmen veya tamamen kopyalanamaz, "
         "çoğaltılamaz ve yeniden yayımlanamaz. Kaynak gösterilerek yapılacak "
         "kullanımlarda ilgili içeriğe aktif bağlantı verilmesi zorunludur.")


def ext(h): return ' target="_blank" rel="noopener"' if h.startswith("http") else ""

# ----------------------------------------------------------------- header
def header():
    """İki satırlı kabuk:
      1) format bandı (siyah)  — yayın formatları kanal şeridi
      2) marka satırı          — logo · ANA MENÜ (sola yaslı) · ikonlar · giriş
    Ana menü ayrı satırda değil, logo hizasında. Arama alanı kaldırıldı;
    arama ikonu arama kipini açar. Perdeleme paneli marka satırına yaslanır."""
    o = io.StringIO(); w = o.write
    w('  <!-- Header start -->\n')
    w('  <header class="uc-header header-six uc-navbar-sticky-wrap z-999"\n')
    w('    data-uc-sticky="sel-target: .uc-navbar-container; cls-active: uc-navbar-sticky; cls-inactive: uc-navbar-transparent; end: !*;">\n')
    w('    <nav class="uc-navbar-container bg-white dark:bg-gray-900 fs-6 z-1">\n')

    # 1. format bandı
    w('\n      <!-- 1. Format bandı — yayın formatları kanal şeridi -->\n')
    w('      <div class="dh-v2-fmt panel z-3">\n        <div class="container max-w-xl">\n')
    w('          <div class="dh-v2-fmt__row">\n')
    w('            <nav class="dh-v2-fmt__track" aria-label="Yayın formatları">\n')
    for ad, h, ik in FORMAT:
        w('              <a href="%s"><i class="fas %s" aria-hidden="true"></i><span>%s</span></a>\n' % (h, ik, ad))
    w('            </nav>\n')
    # ikon seti + ayraç + giriş/üye ol — bandın sağ ucunda
    w('            <div class="dh-v2-brand__acts">\n')
    w('              <a class="dh-v2-act dh-v2-act--ara uc-search-trigger" href="#uc-search-modal" data-uc-toggle aria-label="Ara">\n')
    w('                <i class="fas fa-search fs-4" aria-hidden="true"></i><span class="dh-v2-act__label">Ara</span></a>\n')
    w('              <a class="dh-v2-act" href="hesabim.html#bildirimler" aria-label="Bildirim merkezi">\n')
    w('                <i class="fas fa-bell fs-4" aria-hidden="true"></i>\n')
    w('                <span class="dh-v2-act__badge">3</span><span class="dh-v2-act__label">Bildirim merkezi</span></a>\n')
    w('              <a class="dh-v2-act" href="hesabim.html#kaydedilenler" aria-label="Kaydedilenler">\n')
    w('                <i class="fas fa-bookmark fs-4" aria-hidden="true"></i><span class="dh-v2-act__label">Kaydedilenler</span></a>\n')
    w('              <div class="dh-v2-user" data-dh-user>\n')
    w('                <button class="dh-v2-act" type="button" aria-expanded="false" aria-controls="dh-user-menu" aria-label="Hesap">\n')
    w('                  <i class="fas fa-user-circle fs-4" aria-hidden="true"></i><span class="dh-v2-act__label">Hesap</span>\n')
    w('                </button>\n')
    w('                <div class="dh-v2-user__menu" id="dh-user-menu" hidden>\n')
    w('                  <a href="giris.html"><i class="fas fa-right-to-bracket" aria-hidden="true"></i>Giriş Yap</a>\n')
    w('                  <a href="uye-ol.html"><i class="fas fa-user-plus" aria-hidden="true"></i>Üye Ol</a>\n')
    w('                  <a href="hesabim.html"><i class="fas fa-user-circle" aria-hidden="true"></i>Hesabım</a>\n')
    w('                </div>\n')
    w('              </div>\n')
    w('              <span class="dh-v2-brand__sep" aria-hidden="true"></span>\n')
    w('              <a class="dh-v2-signin" href="giris.html">Giriş Yap</a>\n')
    w('              <a class="dh-v2-signup" href="uye-ol.html">Üye Ol</a>\n')
    w('            </div>\n')
    w('          </div>\n        </div>\n      </div>\n')

    # 2. marka satırı: logo + ana menü + ikonlar + giriş
    w('\n      <!-- 2. Marka satırı — logo · ana menü (sola yaslı) · ikonlar · giriş -->\n')
    w('      <div class="dh-v2-brand panel z-2">\n        <div class="container max-w-xl">\n')
    w('          <div class="dh-v2-brand__row dh-v2-nav__bar">\n')
    w('            <a class="uc-menu-trigger dh-v2-menu-trigger" href="#uc-menu-panel" data-uc-toggle\n')
    w('              aria-label="Menüyü aç" aria-expanded="false" aria-controls="uc-menu-panel"></a>\n')
    w('            <div class="dh-v2-brand__logo">\n')
    w('              <a href="index.html" aria-label="Dada Haber ana sayfa">\n')
    w('                <img class="d-block dark:d-none" src="./assets/images/logos/logo.png" alt="Dada Haber" srcset="./assets/images/logos/logo-300w.png 300w, ./assets/images/logos/logo-600w.png 600w, ./assets/images/logos/logo.png 1198w" sizes="180px">\n')
    w('                <img class="d-none dark:d-block" src="./assets/images/logos/logo-white.png" alt="Dada Haber" srcset="./assets/images/logos/logo-white-300w.png 300w, ./assets/images/logos/logo-white-600w.png 600w, ./assets/images/logos/logo-white.png 1198w" sizes="180px">\n')
    w('              </a>\n')
    w('            </div>\n')

    # ana menü — logo hizasında, sola yaslı
    w('            <nav class="dh-v2-nav" aria-label="Ana menü">\n')
    w('              <ul class="dh-v2-nav__list">\n')
    for slug, ad, hub, is_, gruplar in MENU:
        genis = ' dh-mega--genis' if slug == "diger" else ''
        w('                <li data-dh-menu>\n')
        w('                  <a href="%s" data-cat="%s" aria-expanded="false">%s <i class="fas fa-chevron-down" aria-hidden="true"></i></a>\n' % (hub, slug, ad))
        w('                  <div class="dh-mega%s" data-cat="%s">\n' % (genis, slug))
        w('                    <div class="dh-mega__inner">\n')
        w('                      <div class="dh-mega__head">\n')
        w('                        <span class="dh-mega__title">%s</span>\n' % ad)
        w('                        <p class="dh-mega__job">%s</p>\n' % is_)
        w('                        <a class="dh-mega__all" href="%s">Tümünü Gör</a>\n' % hub)
        w('                      </div>\n')
        w('                      <div class="dh-mega__cols">\n')
        for baslik, ogeler in gruplar:
            w('                        <div>\n')
            if baslik:
                w('                          <span class="dh-mega__grp">%s</span>\n' % baslik)
            w('                          <ul>\n')
            for t, h in ogeler:
                w('                            <li><a href="%s"%s>%s</a></li>\n' % (h, ext(h), t))
            w('                          </ul>\n')
            w('                        </div>\n')
        w('                      </div>\n')
        w('                    </div>\n')
        w('                  </div>\n')
        w('                </li>\n')
    w('              </ul>\n')
    w('            </nav>\n')

    w('          </div>\n        </div>\n      </div>\n')
    w('\n    </nav>\n  </header>\n')
    return o.getvalue()

# -------------------------------------------------------------- offcanvas
def offcanvas():
    o = io.StringIO(); w = o.write
    w('  <!--  Menu panel -->\n')
    w('  <div id="uc-menu-panel" role="dialog" aria-modal="true" aria-label="Ana menü" data-uc-offcanvas="overlay: true;">\n')
    w('    <div class="uc-offcanvas-bar bg-white text-dark dark:bg-gray-900 dark:text-white">\n')
    w('      <header class="uc-offcanvas-header hstack justify-between items-center pb-4 bg-white dark:bg-gray-900">\n')
    w('        <div class="uc-logo">\n')
    w('          <a href="index.html" class="h5 text-none text-gray-900 dark:text-white">\n')
    w('            <img class="w-48px" src="./assets/images/logos/logo-left.png" alt="Dada Haber" srcset="./assets/images/logos/logo-left-96w.png 96w, ./assets/images/logos/logo-left.png 286w" sizes="48px">\n')
    w('          </a>\n        </div>\n')
    w('        <button class="uc-offcanvas-close p-0 icon-3 btn border-0 dark:text-white dark:text-opacity-50 hover:text-primary duration-150 transition-all" type="button">\n')
    w('          <i class="unicon-close"></i>\n        </button>\n')
    w('      </header>\n')
    w('      <div class="panel">\n')
    w('        <p class="dh-v2-off__slogan">Gündemin net hâli.</p>\n')
    w('        <div class="dh-v2-off__user">\n')
    w('          <a class="dh-v2-signin" href="giris.html">Giriş Yap</a>\n')
    w('          <a class="dh-v2-signup" href="uye-ol.html">Üye Ol</a>\n')
    w('        </div>\n')
    w('        <ul class="dh-v2-off__list" data-uc-nav>\n')
    for slug, ad, hub, is_, gruplar in MENU:
        w('          <li class="uc-parent">\n')
        w('            <a href="%s" data-cat="%s">%s</a>\n' % (hub, slug, ad))
        w('            <ul class="uc-nav-sub" data-uc-nav>\n')
        for baslik, ogeler in gruplar:
            if baslik:
                w('              <li><span class="dh-v2-off__grp">%s</span></li>\n' % baslik)
            for t, h in ogeler:
                w('              <li><a href="%s"%s>%s</a></li>\n' % (h, ext(h), t))
        w('            </ul>\n          </li>\n')
    w('        </ul>\n')
    w('        <span class="dh-v2-off__grp dh-v2-off__grp--sec">Medya ve Formatlar</span>\n')
    w('        <div class="dh-v2-off__svc">\n')
    for ad, h, ik in FORMAT:
        w('          <a href="%s"><i class="fas %s" aria-hidden="true"></i>%s</a>\n' % (h, ik, ad))
    w('        </div>\n')
    # görünüm ayarları — karanlık mod alt menüden buraya taşındı
    w('        <span class="dh-v2-off__grp dh-v2-off__grp--sec">Görünüm</span>\n')
    w('        <div class="dh-v2-off__view">\n')
    w('          <span><i class="fas fa-moon" aria-hidden="true"></i>Karanlık mod</span>\n')
    w('          <div class="darkmode-trigger" data-darkmode-switch>\n')
    w('            <label class="switch"><span class="sr-only">Karanlık mod</span>')
    w('<input type="checkbox"><span class="slider fs-5"></span></label>\n')
    w('          </div>\n')
    w('        </div>\n')
    w('      </div>\n    </div>\n  </div>\n')
    return o.getvalue()

# ----------------------------------------------------------------- footer
def footer():
    """Kardeş marka DadaFit footer kalıbı:
       sol: marka + açıklama + sosyal ikonlar · orta: üç bağlantı sütunu ·
       sağ: uygulama indirme. Altında toplayıcı kurumsal şerit, yasal şerit
       ve en altta telif bilgilendirmesi. Sosyal hesaplar YALNIZ burada."""
    o = io.StringIO(); w = o.write
    w('  <footer id="uc-footer" class="uc-footer dh-v2-foot panel uc-light">\n')
    w('    <div class="container max-w-xl">\n')
    w('      <div class="dh-v2-foot__top">\n')

    # sol: marka
    w('        <div class="dh-v2-foot__brand">\n')
    w('          <img src="./assets/images/logos/logo-white.png" alt="Dada Haber" srcset="./assets/images/logos/logo-white-300w.png 300w, ./assets/images/logos/logo-white-600w.png 600w, ./assets/images/logos/logo-white.png 1198w" sizes="200px">\n')
    w('          <p class="dh-v2-foot__desc">Günün gelişmelerini bağlamıyla veren dijital haber platformu. '
      'Haberin ne olduğunu, neden önemli olduğunu ve neye dayandığını aynı sayfada gösteriyoruz.</p>\n')
    w('          <ul class="dh-v2-foot__soc">\n')
    for ad, ikon, h in SOSYAL:
        w('            <li><a href="%s" aria-label="%s"><i class="fa-brands %s" aria-hidden="true"></i></a></li>\n' % (h, ad, ikon))
    w('            <li><a href="#" aria-label="WhatsApp Kanalı"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i></a></li>\n')
    w('            <li><a href="#" aria-label="RSS"><i class="fas fa-rss" aria-hidden="true"></i></a></li>\n')
    w('          </ul>\n')
    w('        </div>\n')

    # orta: bağlantı sütunları
    w('        <div class="dh-v2-foot__cols">\n')
    for baslik, ogeler in FOOTER:
        w('          <div class="dh-v2-foot__grp">\n')
        w('            <h2>%s</h2>\n            <ul>\n' % baslik)
        for t, h in ogeler:
            w('              <li><a href="%s">%s</a></li>\n' % (h, t))
        w('            </ul>\n          </div>\n')
    w('        </div>\n')

    # sağ: uygulama
    w('        <div class="dh-v2-foot__app">\n')
    w('          <h2>Dada Haber&rsquo;i İndir</h2>\n')
    w('          <p>Gündemi cebinde taşı. Takip ettiğin başlıklar, kaydettiğin haberler ve '
      'bildirimler uygulamada da seninle.</p>\n')
    w('          <div class="dh-v2-foot__store">\n')
    w('            <a class="dh-store-badge" href="hesabim.html#uygulama"><i class="fa-brands fa-apple" aria-hidden="true"></i><span><small>İndir</small><b>App Store</b></span></a>\n')
    w('            <a class="dh-store-badge" href="hesabim.html#uygulama"><i class="fa-brands fa-google-play" aria-hidden="true"></i><span><small>İndir</small><b>Google Play</b></span></a>\n')
    w('          </div>\n')
    w('        </div>\n')
    w('      </div>\n')

    # toplayıcı kurumsal şerit
    w('      <nav class="dh-v2-foot__strip" aria-label="Kurumsal bağlantılar">\n')
    for t, h in KURUMSAL:
        w('        <a href="%s">%s</a>\n' % (h, t))
    w('      </nav>\n')

    # yasal şerit — etiketli
    w('      <nav class="dh-v2-foot__strip dh-v2-foot__strip--yasal" aria-label="Yasal bağlantılar">\n')
    w('        <span class="dh-v2-foot__striplbl">Yasal</span>\n')
    for t, h in YASAL:
        w('        <a href="%s">%s</a>\n' % (h, t))
    w('      </nav>\n')

    w('      <div class="dh-v2-foot__bottom">\n')
    w('        <p class="dh-v2-foot__rights">%s</p>\n' % TELIF)
    w('        <p class="dh-v2-foot__copy">Dada Haber &copy; 2026, Tüm Hakları Saklıdır. <span>Prototip · Bilgi mimarisi sürüm 2.1</span></p>\n')
    w('      </div>\n')
    w('    </div>\n  </footer>\n')
    return o.getvalue()


# ------------------------------------------------------ mobil alt gezinme
def bnav():
    o = io.StringIO(); w = o.write
    w('  <!-- Mobil alt gezinme — 991,98px altında görünür -->\n')
    w('  <nav class="dh-bnav" aria-label="Alt gezinme">\n')
    w('    <div class="dh-bnav__row">\n')
    for ad, h, ik, cls in BNAV:
        ek = ' data-uc-toggle aria-haspopup="dialog"' if h.startswith("#") else ''
        k = ("dh-bnav__item " + cls).strip()
        w('      <a class="%s" href="%s"%s>\n' % (k, h, ek))
        w('        <span class="dh-bnav__ic" aria-hidden="true"><i class="%s"></i></span>\n' % ik)
        w('        <span class="dh-bnav__label">%s</span>\n' % ad)
        w('      </a>\n')
    w('    </div>\n  </nav>\n')
    return o.getvalue()


if __name__ == "__main__":
    d = os.path.dirname(os.path.abspath(__file__))
    for ad, fn in (("header.html", header), ("offcanvas.html", offcanvas),
                   ("footer.html", footer), ("bnav.html", bnav)):
        open(os.path.join(d, ad), "w", encoding="utf-8").write(fn())
        print(ad, "yazıldı")
