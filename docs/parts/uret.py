# -*- coding: utf-8 -*-
"""Dada Haber v2 kabuğu — Nihai Menü Haritası'ndan header/offcanvas/footer üretir.
Menü metni ve sırası dokümandan birebir; elle yazılmaz ki sapma olmasın."""
import io, os

L = "haber-liste.html"   # gerçek sayfası olmayan alt kategoriler için liste şablonu

MENU = [
 ("simdi", "Şimdi", "simdi.html",
  "Günün anlık gelişmelerinin toplandığı canlı merkez.",
  [(None, [("Son Dakika","son-dakika.html"),("Canlı Gündem","simdi.html#canli"),
           ("Canlı Yayın","video.html#canli"),("Dakika Dakika","simdi.html#dakika"),
           ("Bugün Ne Oldu?","simdi.html#bugun")]),
   (None, [("Gündem Takvimi","simdi.html#takvim"),("Güncellenen Haberler","simdi.html#guncellenen"),
           ("Afet ve Acil Durum","simdi.html#afet"),("Trafik ve Ulaşım","simdi.html#trafik"),
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

 ("ekonomi", "Ekonomi", "ekonomi.html",
  "Piyasalar, kişisel finans ve iş dünyası.",
  [("Ekonomi ve finans", [("Türkiye Ekonomisi",L),("Dünya Ekonomisi",L),("Piyasalar","finans.html"),
                          ("Döviz","doviz.html"),("Altın","altin.html"),("Borsa","borsa.html"),
                          ("Kripto Para","kripto.html"),("Bankacılık",L),("Kişisel Finans",L)]),
   ("Sektörler", [("İş Dünyası",L),("Şirketler",L),("Girişimcilik",L),("Çalışma Hayatı",L),
                  ("Enerji",L),("Tarım",L),("Sanayi",L),("Gayrimenkul",L),("Otomotiv",L)]),
   ("Piyasalar ekranı", [("Akaryakıt Fiyatları","finans.html#akaryakit"),
                         ("Faiz Oranları","finans.html#faiz"),
                         ("Ekonomik Takvim","finans.html#takvim"),
                         ("Günlük Değişim Grafikleri","finans.html#grafik"),
                         ("Ekonomi Analizi",L)])]),

 ("teknoloji", "Teknoloji", "teknoloji.html",
  "Yapay zekâ, bilim ve dijital kültür.",
  [(None, [("Yapay Zekâ",L),("Bilim",L),("Tüketici Teknolojileri",L),
           ("Mobil",L),("İnternet",L),("Sosyal Medya",L)]),
   (None, [("Siber Güvenlik",L),("Yazılım",L),("Girişimler",L),
           ("Uzay",L),("Savunma Teknolojileri","savunma.html"),("Oyun","oyun.html")]),
   (None, [("E-Spor",L),("Dijital Kültür",L),("Teknoloji Rehberleri",L),
           ("Ürün İncelemeleri",L)])]),

 ("gelecek", "Gelecek", "gelecek.html",
  "Eğitim, kariyer, iklim ve gençlerin gündemi.",
  [("Eğitim ve kariyer", [("Eğitim ve Sınavlar",L),("Üniversiteler",L),("Burslar",L),
                          ("Staj İlanları",L),("Kariyer",L),("Meslekler",L),("İş Fırsatları",L),
                          ("Girişimcilik",L),("Geleceğin Meslekleri",L),
                          ("Yapay Zekâ ve Çalışma Hayatı",L)]),
   ("Toplum ve gelecek", [("İklim",L),("Sürdürülebilirlik",L),("Dijital Haklar",L),
                          ("Gençlerin Gündemi",L),("Barınma",L),("Yurt ve Öğrenci Yaşamı",L)]),
   ("Fırsatlar", [("Değişim Programları",L),("Proje ve Yarışmalar",L),
                  ("Gönüllülük",L),("Fırsatlar ve Başvurular","gelecek.html#firsatlar")])]),

 ("spor", "Spor", "spor.html",
  "Branşlar, skorlar, fikstür ve analiz.",
  [("Branşlar", [("Futbol","futbol.html"),("Süper Lig","puan-durumu.html"),("Millî Takım",L),
                 ("Avrupa Ligleri","puan-durumu.html"),("Şampiyonlar Ligi","puan-durumu.html"),
                 ("Basketbol","basketbol.html"),("Voleybol","voleybol.html"),
                 ("Motor Sporları","formula1.html"),("Bisiklet","bisiklet.html"),
                 ("Tenis",L),("Atletizm",L),("Olimpiyatlar",L),("Geleneksel Sporlar",L),("E-Spor",L)]),
   ("Servisler", [("Transfer",L),("Puan Durumu","puan-durumu.html"),
                  ("Fikstür","fikstur.html"),("Canlı Skor","fikstur.html#canli"),
                  ("Takımlar","takim.html")]),
   ("İçerikler", [("Spor Analizi",L),("Spor Video","video.html#spor")])]),

 ("saglik", "Sağlık", "saglik.html",
  "Halk sağlığı, yaşam ve uzman içerikleri.",
  [(None, [("Sağlık Haberleri","saglik.html"),("Halk Sağlığı",L),("Ruh Sağlığı",L),
           ("Beslenme",L),("Sağlıklı Yaşam",L),("Hastalıklar",L)]),
   (None, [("Anne ve Çocuk","hamilelik.html"),("Kadın Sağlığı","kadin.html"),("Erkek Sağlığı",L),
           ("Spor Sağlığı",L),("Tıp Teknolojileri",L),("İlaç ve Tedaviler",L)]),
   (None, [("Sağlık Politikaları",L),("Uzman Görüşleri",L),("Sağlık Rehberleri",L),
           ("Doğru Bilinen Yanlışlar","dada-dogrula.html#saglik")])]),

 ("kultur", "Kültür &amp; Yaşam", "kultur-yasam.html",
  "Kültür sanat, şehir, seyahat ve popüler kültür.",
  [("Kültür sanat", [("Kültür Sanat","kultur-yasam.html"),("Sinema",L),("Dizi",L),("Müzik",L),
                     ("Kitap",L),("Edebiyat",L),("Tiyatro",L),("Sergi",L),("Etkinlik",L)]),
   ("Yaşam", [("Şehir Yaşamı",L),("Seyahat",L),("Gastronomi","https://dadamutfak.com/"),
              ("Moda",L),("Tasarım",L),("Mimari",L),("İnsan Hikâyeleri",L)]),
   ("Popüler kültür", [("Popüler Kültür",L),("Sosyal Medya Gündemi",L),("Hafta Sonu",L),
                       ("Kültür Takvimi","kultur-yasam.html#takvim"),("Astroloji","astroloji.html")])]),

 ("video", "Video", "video.html",
  "Dikey video, program, canlı yayın ve belgesel.",
  [("Formatlar", [("Dada 60","video.html#dada60"),("Son Dakika Videoları","video.html#sondakika"),
                  ("Açıklayıcı Videolar","video.html#aciklayici"),("Canlı Yayın","video.html#canli"),
                  ("Röportajlar","video.html#roportaj"),("Sokaktan","video.html#sokaktan")]),
   ("Programlar", [("Haber Dosyaları","video.html#dosya"),("Belgeseller","video.html#belgesel"),
                   ("Stüdyo Programları","video.html#studyo"),("Ekonomi Programları","video.html#ekonomi"),
                   ("Teknoloji Programları","video.html#teknoloji"),("Spor Programları","video.html#spor"),
                   ("Kültür Programları","video.html#kultur")]),
   ("Arşiv", [("Video Serileri","video-kategori-detay.html"),("Program Arşivi","video-galeri.html"),
              ("Foto Fokus","foto-fokus.html")])]),

 ("kesfet", "Keşfet", "kesfet.html",
  "Dada Haber’e özgü açıklayıcı ve güven odaklı formatlar.",
  [("Dada formatları", [("Dada Özet","dada-ozet.html"),("Günün 5’i","kesfet.html#gunun5"),
                        ("Dada Bağlam","dada-baglam.html"),("Dada Doğrula","dada-dogrula.html"),
                        ("Farklı Bakışlar","farkli-bakislar.html"),("Bana Etkisi","kesfet.html#bana-etkisi")]),
   ("Veri ve anlatım", [("Veri &amp; Harita","veri-harita.html"),("Grafik Haberler","infografik.html"),
                        ("Dada’ya Sor","kesfet.html#dadaya-sor"),("Sakin Akış","sakin-akis.html"),
                        ("Podcast","podcast.html"),("Haber Dinle","haber-dinle.html")]),
   ("Dosya ve arşiv", [("Haber Dosyaları","kesfet.html#dosyalar"),("Röportajlar","kesfet.html#roportaj"),
                       ("Yazarlar","yazar-liste.html"),("Görüş","yazar-liste.html#gorus"),
                       ("Editörün Seçimi","kesfet.html#editor"),("Foto Galeri","foto-fokus.html"),
                       ("Arşiv","arsiv.html")])]),
]

BANT = [("Son Dakika","son-dakika.html","is-live"),("Piyasalar","finans.html",""),
        ("Hava Durumu","veri-harita.html#hava",""),("Şehrim","hesabim.html#sehirlerim",""),
        ("Bültenler","hesabim.html#bultenler",""),("Podcast","podcast.html",""),
        ("Mobil Uygulama","hesabim.html#uygulama","")]

SOSYAL = [("Instagram","fa-instagram","#"),("YouTube","fa-youtube","#"),("X","fa-x-twitter","#"),
          ("Facebook","fa-facebook-f","#"),("LinkedIn","fa-linkedin-in","#"),("TikTok","fa-tiktok","#")]

FOOTER = [
 ("Haberler", [("Son Dakika","son-dakika.html"),("Gündem","gundem.html"),("Dünya","dunya.html"),
   ("Ekonomi","ekonomi.html"),("Teknoloji","teknoloji.html"),("Gelecek","gelecek.html"),
   ("Spor","spor.html"),("Sağlık","saglik.html"),("Kültür &amp; Yaşam","kultur-yasam.html"),
   ("Yerel Haberler","gundem.html#yerel")]),
 ("Dada Formatları", [("Dada 60","video.html#dada60"),("Dada Özet","dada-ozet.html"),
   ("Günün 5’i","kesfet.html#gunun5"),("Dada Bağlam","dada-baglam.html"),
   ("Dada Doğrula","dada-dogrula.html"),("Farklı Bakışlar","farkli-bakislar.html"),
   ("Veri &amp; Harita","veri-harita.html"),("Podcast","podcast.html"),("Sakin Akış","sakin-akis.html")]),
 ("Kurumsal", [("Hakkımızda","hakkimizda.html"),("Künye","kunye.html"),("Ekibimiz","kunye.html#ekip"),
   ("Yayın İlkeleri","yayin-ilkeleri.html"),("Editoryal Bağımsızlık","yayin-ilkeleri.html#bagimsizlik"),
   ("Şeffaflık Merkezi","yayin-ilkeleri.html#seffaflik"),("Doğrulama Metodolojisi","dada-dogrula.html#metodoloji"),
   ("Düzeltme Politikası","yayin-ilkeleri.html#duzeltme"),("Yapay Zekâ Politikası","yayin-ilkeleri.html#yapay-zeka"),
   ("Reklam Politikası","reklam.html"),("Kariyer","coming-soon.html"),("İletişim","iletisim.html")]),
 ("Destek ve İletişim", [("Bize Ulaşın","iletisim.html"),("Haber İhbarı","iletisim.html#ihbar"),
   ("Doğrulama Talebi","dada-dogrula.html#talep"),("Hata Bildir","iletisim.html#hata"),
   ("Öneri ve Şikâyet","iletisim.html#oneri"),("İçerik Kaldırma Talebi","iletisim.html#kaldirma"),
   ("Reklam Ver","reklam.html"),("Sponsorluk","reklam.html#sponsorluk"),
   ("Basın İletişimi","iletisim.html#basin"),("Resmî İlanlar","resmi-ilanlar.html")]),
 ("Yasal", [("Kullanım Koşulları","kullanim-sartlari.html"),("Gizlilik Politikası","kvkk.html"),
   ("KVKK Aydınlatma Metni","aydinlatma-metni.html"),("Çerez Politikası","cerezler.html"),
   ("Telif Hakları","kullanim-sartlari.html#telif"),("Topluluk Kuralları","kullanim-sartlari.html#topluluk"),
   ("Erişilebilirlik","kullanim-sartlari.html#erisilebilirlik"),("Açık Rıza Yönetimi","cerezler.html#riza")]),
]

def ext(h): return ' target="_blank" rel="noopener"' if h.startswith("http") else ""

# ----------------------------------------------------------------- header
def header():
    o = io.StringIO(); w = o.write
    w('  <!-- Header start -->\n')
    w('  <header class="uc-header header-six uc-navbar-sticky-wrap z-999"\n')
    w('    data-uc-sticky="sel-target: .uc-navbar-container; cls-active: uc-navbar-sticky; cls-inactive: uc-navbar-transparent; end: !*;">\n')
    w('    <nav class="uc-navbar-container bg-white dark:bg-gray-900 fs-6 z-1">\n')

    # 1. üst servis bandı
    w('\n      <!-- 1. Üst bilgi bandı -->\n')
    w('      <div class="dh-v2-band panel z-3">\n        <div class="container max-w-xl">\n')
    w('          <div class="dh-v2-band__row">\n')
    w('            <span class="dh-v2-band__now">\n')
    w('              <i class="fas fa-calendar-day" aria-hidden="true"></i>\n')
    w('              <span class="datetime">12 Kasım 2025</span>\n')
    w('              <img src="./assets/images/cloudy.png" alt="" aria-hidden="true">\n')
    w('              <span>24,4 °C Ankara</span>\n')
    w('            </span>\n')
    w('            <nav class="dh-v2-band__links" aria-label="Hızlı erişim">\n')
    for ad, h, cls in BANT:
        w('              <a class="%s" href="%s">%s</a>\n' % (cls, h, ad))
    w('            </nav>\n')
    w('            <div class="dh-v2-band__end">\n')
    w('              <ul class="dh-v2-band__soc">\n')
    for ad, ikon, h in SOSYAL:
        w('                <li><a href="%s" aria-label="%s"><i class="fa-brands %s" aria-hidden="true"></i></a></li>\n' % (h, ad, ikon))
    w('              </ul>\n')
    w('              <span class="dh-v2-sep" aria-hidden="true"></span>\n')
    w('              <div class="darkmode-trigger" data-darkmode-switch>\n')
    w('                <label class="switch"><span class="sr-only">Karanlık mod</span>')
    w('<input type="checkbox"><span class="slider fs-5"></span></label>\n')
    w('              </div>\n')
    w('              <a class="dh-v2-login" href="hesabim.html">\n')
    w('                <i class="fas fa-user" aria-hidden="true"></i> Giriş Yap\n')
    w('              </a>\n')
    w('            </div>\n')
    w('          </div>\n        </div>\n      </div>\n')

    # 2. marka satırı
    w('\n      <!-- 2. Ana header -->\n')
    w('      <div class="dh-v2-brand panel z-2">\n        <div class="container max-w-xl">\n')
    w('          <div class="dh-v2-brand__row">\n')
    w('            <a class="uc-menu-trigger dh-v2-menu-trigger" href="#uc-menu-panel" data-uc-toggle aria-label="Menüyü aç"></a>\n')
    w('            <div class="dh-v2-brand__logo">\n')
    w('              <a href="index.html" aria-label="Dada Haber ana sayfa">\n')
    w('                <img class="d-block dark:d-none" src="./assets/images/logos/logo.png" alt="Dada Haber" srcset="./assets/images/logos/logo-300w.png 300w, ./assets/images/logos/logo-600w.png 600w, ./assets/images/logos/logo.png 1198w" sizes="220px">\n')
    w('                <img class="d-none dark:d-block" src="./assets/images/logos/logo-white.png" alt="Dada Haber" srcset="./assets/images/logos/logo-white-300w.png 300w, ./assets/images/logos/logo-white-600w.png 600w, ./assets/images/logos/logo-white.png 1198w" sizes="220px">\n')
    w('              </a>\n')
    w('              <span class="dh-v2-slogan">Gündemin net hâli.</span>\n')
    w('            </div>\n')
    w('            <div class="dh-v2-brand__search">\n')
    w('              <form action="arama.html" method="get" role="search">\n')
    w('                <i class="fas fa-search" aria-hidden="true"></i>\n')
    w('                <input type="search" name="q" placeholder="Haber, yazar, konu veya şehir ara" aria-label="Sitede ara">\n')
    w('              </form>\n')
    w('            </div>\n')
    w('            <div class="dh-v2-brand__acts">\n')
    w('              <a class="dh-v2-act uc-search-trigger d-lg-none" href="#uc-search-modal" data-uc-toggle>\n')
    w('                <i class="fas fa-search fs-4" aria-hidden="true"></i><span class="dh-v2-act__label">Ara</span></a>\n')
    w('              <a class="dh-v2-act" href="hesabim.html#bildirimler">\n')
    w('                <i class="fas fa-bell fs-4" aria-hidden="true"></i>\n')
    w('                <span class="dh-v2-act__badge">3</span><span class="dh-v2-act__label">Bildirim merkezi</span></a>\n')
    w('              <a class="dh-v2-act" href="hesabim.html#kaydedilenler">\n')
    w('                <i class="fas fa-bookmark fs-4" aria-hidden="true"></i><span class="dh-v2-act__label">Kaydedilenler</span></a>\n')
    w('              <a class="dh-v2-act" href="hesabim.html">\n')
    w('                <i class="fas fa-user-circle fs-4" aria-hidden="true"></i><span class="dh-v2-act__label">Hesabım</span></a>\n')
    w('            </div>\n')
    w('          </div>\n        </div>\n      </div>\n')

    # 3. ana gezinti
    w('\n      <!-- 3. Ana menü — 11 başlık -->\n')
    w('      <div class="dh-v2-nav panel z-2">\n        <div class="container max-w-xl">\n')
    w('          <div class="dh-v2-nav__bar">\n')
    w('            <nav aria-label="Ana menü">\n')
    w('              <ul class="dh-v2-nav__list">\n')
    for slug, ad, hub, is_, gruplar in MENU:
        w('                <li>\n')
        w('                  <a href="%s" data-cat="%s">%s <i class="fas fa-chevron-down" aria-hidden="true"></i></a>\n' % (hub, slug, ad))
        w('                  <div class="dh-mega" data-cat="%s">\n' % slug)
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
    w('            </nav>\n          </div>\n        </div>\n      </div>\n')
    w('\n    </nav>\n  </header>\n')
    return o.getvalue()

# -------------------------------------------------------------- offcanvas
def offcanvas():
    o = io.StringIO(); w = o.write
    w('  <!--  Menu panel -->\n')
    w('  <div id="uc-menu-panel" data-uc-offcanvas="overlay: true;">\n')
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
    w('        <div class="dh-v2-off__svc">\n')
    for ad, h, _ in BANT:
        ik = {"Son Dakika":"fa-bolt","Piyasalar":"fa-chart-line","Hava Durumu":"fa-cloud-sun",
              "Şehrim":"fa-location-dot","Bültenler":"fa-envelope","Podcast":"fa-podcast",
              "Mobil Uygulama":"fa-mobile-screen"}[ad]
        w('          <a href="%s"><i class="fas %s" aria-hidden="true"></i>%s</a>\n' % (h, ik, ad))
    w('          <a href="haber-dinle.html"><i class="fa-solid fa-ear-muffs" aria-hidden="true"></i>Haber Dinle</a>\n')
    w('        </div>\n')
    w('        <div class="dh-v2-off__svc" style="grid-template-columns:1fr">\n')
    w('          <a href="hesabim.html"><i class="fas fa-user-circle" aria-hidden="true"></i>Giriş Yap / Hesabım</a>\n')
    w('        </div>\n')
    w('      </div>\n    </div>\n  </div>\n')
    return o.getvalue()

# ----------------------------------------------------------------- footer
def footer():
    o = io.StringIO(); w = o.write
    w('  <footer id="uc-footer" class="uc-footer dh-v2-foot panel uc-light">\n')
    w('    <div class="container max-w-xl">\n')
    w('      <div class="dh-v2-foot__top">\n')
    w('        <div class="dh-v2-foot__brand">\n')
    w('          <img src="./assets/images/logos/logo-white.png" alt="Dada Haber" srcset="./assets/images/logos/logo-white-300w.png 300w, ./assets/images/logos/logo-white-600w.png 600w, ./assets/images/logos/logo-white.png 1198w" sizes="240px">\n')
    w('          <p class="dh-v2-foot__slogan">Gündemin net hâli.</p>\n')
    w('          <p class="dh-v2-foot__rights">dadahaber.com internet sitesinde yayınlanan yazı, haber, video ve fotoğrafların her türlü hakkı Dada İst Ajans Hiz. Tic. Ltd. Şti.’ye aittir. İzin alınmadan, kaynak gösterilerek dahi iktibas edilemez.</p>\n')
    w('        </div>\n')
    w('        <div class="dh-v2-foot__cols">\n')
    for baslik, ogeler in FOOTER:
        w('          <div>\n            <h3>%s</h3>\n            <ul>\n' % baslik)
        for t, h in ogeler:
            w('              <li><a href="%s">%s</a></li>\n' % (h, t))
        w('            </ul>\n          </div>\n')
    w('        </div>\n      </div>\n')
    w('      <div class="dh-v2-foot__chan">\n')
    w('        <div><h3>Dada Haber Kanalları</h3>\n')
    w('          <p class="dh-v2-foot__rights">Gündemi kaçırmayın: bültenlere abone olun, kanallardan takip edin.</p>\n')
    w('        </div>\n')
    w('        <div>\n          <div class="dh-v2-foot__soc">\n')
    w('            <a href="hesabim.html#uygulama"><i class="fas fa-mobile-screen" aria-hidden="true"></i>Mobil Uygulamalar</a>\n')
    w('            <a href="hesabim.html#bultenler"><i class="fas fa-envelope" aria-hidden="true"></i>Bültenler</a>\n')
    w('            <a href="#"><i class="fa-brands fa-whatsapp" aria-hidden="true"></i>WhatsApp Kanalı</a>\n')
    for ad, ikon, h in SOSYAL:
        w('            <a href="%s"><i class="fa-brands %s" aria-hidden="true"></i>%s</a>\n' % (h, ikon, ad))
    w('            <a href="#"><i class="fas fa-rss" aria-hidden="true"></i>RSS</a>\n')
    w('          </div>\n')
    w('          <div class="dh-v2-foot__store">\n')
    w('            <a class="dh-store-badge" href="hesabim.html#uygulama"><i class="fa-brands fa-apple" aria-hidden="true"></i><span><small>İndir</small><b>App Store</b></span></a>\n')
    w('            <a class="dh-store-badge" href="hesabim.html#uygulama"><i class="fa-brands fa-google-play" aria-hidden="true"></i><span><small>İndir</small><b>Google Play</b></span></a>\n')
    w('          </div>\n')
    w('        </div>\n      </div>\n')
    w('      <div class="dh-v2-foot__bottom">\n')
    w('        <p>Dada Haber &copy; 2026, Tüm Hakları Saklıdır.</p>\n')
    w('        <p class="dh-v2-foot__note">Prototip · Bilgi mimarisi sürüm 2.0</p>\n')
    w('      </div>\n')
    w('    </div>\n  </footer>\n')
    return o.getvalue()

d = os.path.dirname(os.path.abspath(__file__))
for ad, fn in (("header.html", header), ("offcanvas.html", offcanvas), ("footer.html", footer)):
    open(os.path.join(d, ad), "w", encoding="utf-8").write(fn())
    print(ad, "yazıldı")
