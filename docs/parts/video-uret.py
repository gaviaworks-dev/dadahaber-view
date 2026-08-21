# -*- coding: utf-8 -*-
"""video.html — Nihai Menü Haritası 3.10 'Video' ana kategorisi.
Bölümler dokümandaki 15 başlığın birebir karşılığı. Bileşenler mevcut
video ailesinden yeniden kullanılıyor (.dh-lb .dh-secbar .dh-track .dh-vid
.dh-serie .dh-shorts .dh-zeb) — yeni bileşen icat edilmiyor."""
import io, re

POSTER = ["./assets/images/videos/posters/vid-01.jpg",
          "./assets/images/videos/posters/vid-03.jpg",
          "./assets/images/videos/posters/vid-04.jpg",
          "./assets/images/videos/posters/vid-05.jpg"]
IMG = ["./assets/images/demo-six/posts/img-%02d.jpg" % n for n in range(1, 23)]

def poster(i): return POSTER[i % len(POSTER)]
def img(i): return IMG[i % len(IMG)]

# (anchor, başlık, açıklama, "Tümünü Gör" hedefi, [(başlık, süre, tarih, izlenme)])
FORMAT = [
 ("sondakika", "Son Dakika Videoları", "Gelişme anında çekilen ham görüntü ve ilk aktarımlar.", "video-galeri.html",
  [("Kurul toplantısından ilk görüntüler", "01:12", "12.12.2025", "412B"),
   ("Merkezde yaya düzenlemesi başladı", "00:48", "12.12.2025", "268B"),
   ("Alt komisyon açıklaması", "02:05", "12.12.2025", "196B"),
   ("Trafik akışında ilk gün", "01:33", "12.12.2025", "154B"),
   ("Durak yerleri değişti: sahadan", "00:57", "11.12.2025", "121B"),
   ("Basın açıklaması tam metin", "04:20", "11.12.2025", "98B")]),
 ("aciklayici", "Açıklayıcı Videolar", "Karmaşık bir başlığı grafik ve haritayla adım adım anlatan formatlar.", "kesfet.html",
  [("Yaya önceliği ne demek? 90 saniyede", "01:30", "12.12.2025", "540B"),
   ("Bütçe üç yıla nasıl yayılıyor?", "02:14", "11.12.2025", "388B"),
   ("Enflasyon sepeti neden değişti?", "03:02", "10.12.2025", "612B"),
   ("Seçim barajı nasıl hesaplanır?", "02:40", "09.12.2025", "455B"),
   ("Deprem yönetmeliği neyi zorunlu kılıyor?", "03:18", "08.12.2025", "372B"),
   ("Faiz kararı cebe nasıl yansır?", "02:05", "08.12.2025", "701B")]),
 ("canli", "Canlı Yayın", "Kesintisiz yayın akışı, canlı bağlantılar ve özel yayınlar.", "video-galeri.html",
  [("Ana Haber — canlı yayın", "Canlı", "Şimdi", "12,4B"),
   ("Kurul toplantısı canlı bağlantı", "Canlı", "Şimdi", "3,1B"),
   ("Piyasa açılışı özel yayını", "01:02:40", "12.12.2025", "88B"),
   ("Seçim gecesi yayın arşivi", "05:12:00", "10.12.2025", "1,4Mn"),
   ("Meclis oturumu tam kayıt", "03:44:10", "09.12.2025", "216B"),
   ("Basın toplantısı tam kayıt", "00:52:18", "08.12.2025", "94B")]),
 ("roportaj", "Röportajlar", "Uzun soluklu, kesintisiz söyleşiler.", "kesfet.html#roportaj",
  [("Kent plancısıyla 40 dakika", "40:12", "12.12.2025", "231B"),
   ("Ekonomist: üç yıllık takvim gerçekçi mi?", "28:44", "11.12.2025", "310B"),
   ("Ulaşım mühendisi anlatıyor", "33:05", "10.12.2025", "185B"),
   ("Mahalle esnafı ne diyor?", "22:18", "09.12.2025", "142B"),
   ("Öğrenci temsilcisiyle söyleşi", "26:50", "08.12.2025", "119B"),
   ("Bir belediye başkanının günü", "45:30", "07.12.2025", "203B")]),
 ("sokaktan", "Sokaktan", "Vatandaşın kendi cümlesiyle: kısa saha röportajları.", "video-galeri.html",
  [("Merkeze araçla girenler ne diyor?", "03:12", "12.12.2025", "289B"),
   ("Durak değişikliği kimi etkiledi?", "02:48", "12.12.2025", "234B"),
   ("Öğrenciler barınmayı anlatıyor", "04:05", "11.12.2025", "467B"),
   ("Pazarda fiyat turu", "03:30", "10.12.2025", "521B"),
   ("Yeni yaya aksında ilk gün", "02:20", "10.12.2025", "198B"),
   ("Kiracılar ve ev sahipleri", "05:14", "09.12.2025", "612B")]),
]

PROGRAM = [
 ("dosya", "Haber Dosyaları", "Tek konuya odaklanan çok bölümlü dosyalar.", 16,
  "8 dosya · her ay yeni dosya · 2,1Mn izlenme",
  [("Kentin ulaşım planı — 1. bölüm", "18:40"), ("Kentin ulaşım planı — 2. bölüm", "21:05"),
   ("Barınma dosyası — 1. bölüm", "24:12"), ("Barınma dosyası — 2. bölüm", "19:55"),
   ("Enerji dosyası", "27:30"), ("Tarımda su dosyası", "23:18")]),
 ("belgesel", "Belgeseller", "Uzun metrajlı, saha çekimli belgesel yapımlar.", 18,
  "12 belgesel · 3,6Mn izlenme",
  [("Bir nehrin hikâyesi", "52:10"), ("Şehrin altındaki şehir", "48:22"),
   ("Mevsimlik yollar", "44:05"), ("Son atölyeler", "39:48"),
   ("Denizden dönenler", "57:30"), ("Yüksekteki köy", "41:12")]),
 ("studyo", "Stüdyo Programları", "Konuk ağırlıklı, düzenli yayınlanan stüdyo yapımları.", 20,
  "6 program · haftada 4 yayın · 4,4Mn izlenme",
  [("Gündem Masası", "58:20"), ("Açık Oturum", "1:02:14"),
   ("Haftanın Konuğu", "46:30"), ("Sorularla", "38:05"),
   ("Karşılıklı", "51:44"), ("Perde Arkası", "42:18")]),
]

TEMATIK = [
 ("ekonomi", "Ekonomi Programları", "Piyasa, sektör ve kişisel finans yayınları.", "ekonomi.html",
  [("Ekonomi Masası — faiz kararı", "42:10", "12.12.2025", "388B"),
   ("Piyasa Kapanışı", "18:05", "12.12.2025", "212B"),
   ("Sektör Raporu: enerji", "35:22", "11.12.2025", "156B"),
   ("Cepten Cebe: bütçe yönetimi", "26:40", "10.12.2025", "294B"),
   ("Girişim Hikâyeleri", "31:18", "09.12.2025", "178B"),
   ("Tarımda Fiyat", "28:55", "08.12.2025", "142B")]),
 ("teknoloji", "Teknoloji Programları", "Yapay zekâ, bilim ve ürün incelemeleri.", "teknoloji.html",
  [("Yapay Zekâ Notları", "38:12", "12.12.2025", "521B"),
   ("Ürün İnceleme: yeni nesil", "22:40", "11.12.2025", "467B"),
   ("Siber Güvenlik Dosyası", "44:05", "10.12.2025", "233B"),
   ("Uzaydan Haberler", "29:18", "09.12.2025", "312B"),
   ("Yazılımcı Odası", "51:30", "08.12.2025", "189B"),
   ("Oyun Masası", "36:22", "07.12.2025", "398B")]),
 ("spor", "Spor Programları", "Maç analizi, saha sonrası ve branş yayınları.", "spor.html",
  [("Sahanın Dili — derbi sonrası", "48:10", "12.12.2025", "812B"),
   ("Puan Durumu Masası", "32:24", "12.12.2025", "445B"),
   ("Transfer Gündemi", "27:05", "11.12.2025", "678B"),
   ("Basketbol Panorama", "38:40", "10.12.2025", "234B"),
   ("Voleybol Saati", "29:15", "09.12.2025", "156B"),
   ("Motor Sporları Bülteni", "24:50", "08.12.2025", "198B")]),
 ("kultur", "Kültür Programları", "Sinema, müzik, kitap ve şehir yaşamı yayınları.", "kultur-yasam.html",
  [("Perde: haftanın filmleri", "34:20", "12.12.2025", "267B"),
   ("Kitap Kulübü", "42:15", "11.12.2025", "189B"),
   ("Sahne Arkası", "38:05", "10.12.2025", "145B"),
   ("Şehir Rehberi", "26:44", "09.12.2025", "312B"),
   ("Mutfakta Bugün", "31:30", "08.12.2025", "423B"),
   ("Seyahat Notları", "35:12", "07.12.2025", "278B")]),
]

DADA60 = [("Yaya aksında ilk gün — 60 saniye", "00:58", "GÜNDEM", "524B"),
          ("Derbi özeti — 60 saniye", "00:60", "SPOR", "812B"),
          ("Faiz kararı — 60 saniye", "00:52", "EKONOMİ", "467B"),
          ("Yapay zekâ haftası — 60 saniye", "00:55", "TEKNOLOJİ", "389B"),
          ("Burslar açıldı — 60 saniye", "00:47", "GELECEK", "298B"),
          ("Grip sezonu — 60 saniye", "00:59", "SAĞLIK", "212B"),
          ("Festival takvimi — 60 saniye", "00:44", "KÜLTÜR", "176B"),
          ("Dünya gündemi — 60 saniye", "00:57", "DÜNYA", "334B")]

CIP = [("Dada 60","#dada60"),("Son Dakika Videoları","#sondakika"),("Açıklayıcı Videolar","#aciklayici"),
       ("Canlı Yayın","#canli"),("Röportajlar","#roportaj"),("Sokaktan","#sokaktan"),
       ("Haber Dosyaları","#dosya"),("Belgeseller","#belgesel"),("Stüdyo Programları","#studyo"),
       ("Ekonomi Programları","#ekonomi"),("Teknoloji Programları","#teknoloji"),
       ("Spor Programları","#spor"),("Kültür Programları","#kultur"),
       ("Video Serileri","#seriler"),("Program Arşivi","#arsiv")]

o = io.StringIO(); w = o.write
sayac = [0]

def ray(anchor, baslik, aciklama, tum, ogeler, zebra=False):
    tid = "dhVid" + anchor.capitalize()
    w('        <section class="section panel%s" id="%s" aria-labelledby="%s-b">\n'
      % (" dh-zeb" if zebra else "", anchor, anchor))
    w('          <div class="container max-w-xl">\n')
    w('            <div class="section-header panel dh-secbar">\n')
    w('              <div>\n')
    w('                <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="%s-b">%s</h2>\n' % (anchor, baslik))
    w('                <p class="dh-vsec__lead">%s</p>\n' % aciklama)
    w('              </div>\n')
    w('              <div class="dh-secbar__tools">\n')
    w('                <a href="%s" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Tümünü Gör</a>\n' % tum)
    w('                <div class="dh-secbar__nav">\n')
    w('                  <button type="button" data-dh-track-prev="%s" aria-label="%s — önceki"><i class="fas fa-chevron-left" aria-hidden="true"></i></button>\n' % (tid, baslik))
    w('                  <button type="button" data-dh-track-next="%s" aria-label="%s — sonraki"><i class="fas fa-chevron-right" aria-hidden="true"></i></button>\n' % (tid, baslik))
    w('                </div>\n              </div>\n            </div>\n')
    w('            <div class="dh-track" id="%s">\n' % tid)
    for t, sure, tarih, izl in ogeler:
        sayac[0] += 1
        w('              <a class="dh-vid" href="video-detay.html">\n')
        w('                <span class="dh-vid__fig">\n')
        w('                  <img class="dh-vid__img" src="%s" alt="%s" loading="lazy" decoding="async">\n' % (poster(sayac[0]), t))
        w('                  <span class="dh-vid__dur"><i class="fas fa-play" aria-hidden="true"></i>%s</span>\n' % sure)
        w('                  <span class="dh-vid__play" aria-hidden="true"><i class="fas fa-play"></i></span>\n')
        w('                </span>\n')
        w('                <b class="dh-vid__title">%s</b>\n' % t)
        w('                <span class="dh-vid__meta">\n')
        w('                  <span><i class="fas fa-calendar-day" aria-hidden="true"></i>%s</span>\n' % tarih)
        w('                  <span><i class="fas fa-eye" aria-hidden="true"></i>%s</span>\n' % izl)
        w('                </span>\n              </a>\n')
    w('            </div>\n          </div>\n        </section>\n\n')

def seri(anchor, baslik, aciklama, kapak, gercek, bolumler):
    tid = "dhVid" + anchor.capitalize()
    w('        <section class="section panel dh-zeb" id="%s" aria-labelledby="%s-b">\n' % (anchor, anchor))
    w('          <div class="container max-w-xl">\n')
    w('            <div class="dh-serie">\n              <div class="dh-serie__head">\n')
    w('                <span class="dh-serie__cover"><img src="%s" alt="" loading="lazy" decoding="async"></span>\n' % img(kapak))
    w('                <span class="dh-serie__info">\n')
    w('                  <b class="dh-serie__name" id="%s-b"><i class="fas fa-layer-group" aria-hidden="true"></i>%s</b>\n' % (anchor, baslik))
    w('                  <span class="dh-serie__facts">%s</span>\n' % gercek)
    w('                  <span class="dh-vsec__lead">%s</span>\n' % aciklama)
    w('                </span>\n')
    w('                <span class="dh-serie__tools">\n')
    w('                  <a class="dh-serie__open" href="video-kategori-detay.html">Tümünü Aç <i class="fas fa-arrow-right" aria-hidden="true"></i></a>\n')
    w('                  <span class="dh-secbar__nav">\n')
    w('                    <button type="button" data-dh-track-prev="%s" aria-label="%s — önceki"><i class="fas fa-chevron-left" aria-hidden="true"></i></button>\n' % (tid, baslik))
    w('                    <button type="button" data-dh-track-next="%s" aria-label="%s — sonraki"><i class="fas fa-chevron-right" aria-hidden="true"></i></button>\n' % (tid, baslik))
    w('                  </span>\n                </span>\n              </div>\n')
    w('              <div class="dh-track" id="%s">\n' % tid)
    for n, (t, sure) in enumerate(bolumler, 1):
        sayac[0] += 1
        w('                <a class="dh-vid" href="video-detay.html">\n')
        w('                  <span class="dh-vid__fig">\n')
        w('                    <img class="dh-vid__img" src="%s" alt="%s" loading="lazy" decoding="async">\n' % (poster(sayac[0]), t))
        w('                    <span class="dh-vid__ep">%d. Bölüm</span>\n' % n)
        w('                    <span class="dh-vid__dur"><i class="fas fa-play" aria-hidden="true"></i>%s</span>\n' % sure)
        w('                    <span class="dh-vid__play" aria-hidden="true"><i class="fas fa-play"></i></span>\n')
        w('                  </span>\n')
        w('                  <b class="dh-vid__title">%s</b>\n' % t)
        w('                </a>\n')
    w('              </div>\n            </div>\n          </div>\n        </section>\n\n')

# ---------------------------------------------------------------- gövde
w('        <!-- Format çipleri — dokümandaki 15 Video başlığı -->\n')
w('        <nav class="section panel dh-catbar" data-cat="video" aria-label="Video formatları">\n')
w('          <div class="container max-w-xl">\n            <div class="dh-catbar__row">\n')
w('              <span class="dh-catbar__root"><span class="dh-catbar__root-ad" aria-current="page">VİDEO</span><span class="dh-catbar__root-fn">formatları</span></span>\n')
w('              <div class="dh-catbar__inner swiper-parent">\n')
w('                <div class="swiper dh-catbar__swiper" data-uc-swiper="items: auto; gap: 8; free: true; grab-cursor: true; next: .dh-catbar__nav--next; prev: .dh-catbar__nav--prev; disable-class: is-off; watchOverflow: true;">\n')
w('                  <div class="swiper-wrapper">\n')
for ad, h in CIP:
    w('                    <div class="swiper-slide"><a class="dh-catbar__chip" href="%s">%s</a></div>\n' % (h, ad))
w('                  </div>\n                </div>\n')
w('                <button class="dh-catbar__nav dh-catbar__nav--prev" type="button" aria-label="Önceki"><i class="fas fa-chevron-left" aria-hidden="true"></i></button>\n')
w('                <button class="dh-catbar__nav dh-catbar__nav--next" type="button" aria-label="Sonraki"><i class="fas fa-chevron-right" aria-hidden="true"></i></button>\n')
w('              </div>\n            </div>\n          </div>\n        </nav>\n\n')

# banner
w('        <!-- Bölüm bannerı -->\n')
w('        <div class="block-slider block-slider-miniposts panel swiper-parent uc-dark dh-lb" data-cat="video">\n')
w('          <div class="dh-lb__veil" aria-hidden="true"></div>\n')
w('          <div class="swiper-main swiper" data-uc-swiper="items: 1; autoplay: 6000; gap: 0; effect: fade; fade: true;">\n')
w('            <div class="swiper-wrapper">\n')
for n, (t, sure, tarih, izl) in enumerate([("Kentin ulaşım planı — belgesel dosya","18:40","12.12.2025","412B"),
                                            ("Ekonomi Masası: faiz kararı sonrası","42:10","12.12.2025","388B"),
                                            ("Sahanın Dili: derbi sonrası","48:10","12.12.2025","812B")]):
    w('              <div class="swiper-slide">\n                <article class="post type-post">\n')
    w('                  <div class="featured-image bg-gray-25 dark:bg-gray-800">\n')
    w('                    <canvas class="min-h-300px lg:min-h-420px"></canvas>\n')
    w('                    <img class="media-cover image" src="%s" alt="%s" data-uc-scrollspy="cls: uc-animation-kenburns; repeat: true">\n' % (poster(n), t))
    w('                  </div>\n')
    w('                  <div class="panel max-w-xl mx-auto px-2 z-3">\n')
    w('                    <div class="post-header panel vstack justify-end items-start gap-2 lg:gap-3 min-h-300px lg:min-h-420px py-4 lg:py-6">\n')
    w('                      <nav class="dh-lb__crumb" aria-label="Sayfa yolu"><a href="index.html">Ana Sayfa</a> <span aria-hidden="true">/</span> <span aria-current="page">Video</span></nav>\n')
    w('                      <div class="post-category hstack gap-1 fs-7 fw-bold"><span class="dh-tag dh-tag--lg">%s</span></div>\n' % sure)
    w('                      <h1 class="post-title h4 lg:h3 xl:h2 m-0 text-truncate-2">%s</h1>\n' % t)
    w('                      <div class="post-meta panel hstack gap-2 fs-7 fw-medium">\n')
    w('                        <div class="post-date hstack gap-narrow"><i class="fas fa-calendar-day" aria-hidden="true"></i><span class="minimizeDate">%s</span></div>\n' % tarih)
    w('                        <div class="post-date hstack gap-narrow"><i class="fas fa-eye" aria-hidden="true"></i><span>%s</span></div>\n' % izl)
    w('                      </div>\n                    </div>\n                  </div>\n                </article>\n              </div>\n')
w('            </div>\n          </div>\n        </div>\n\n')

# Dada 60
w('        <!-- Dada 60 — dikey kısa video formatı -->\n')
w('        <section class="section panel" id="dada60" aria-labelledby="dada60-b">\n')
w('          <div class="container max-w-xl">\n')
w('            <div class="section-header panel dh-secbar">\n              <div>\n')
w('                <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dada60-b">Dada 60</h2>\n')
w('                <p class="dh-vsec__lead">Bir haber, altmış saniye. Dikey akış için üretilen kısa video formatı.</p>\n')
w('              </div>\n')
w('              <div class="dh-secbar__tools">\n')
w('                <a href="video-galeri.html" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Tümünü Gör</a>\n')
w('                <div class="dh-secbar__nav">\n')
w('                  <button type="button" data-dh-track-prev="dhVid60" aria-label="Dada 60 — önceki"><i class="fas fa-chevron-left" aria-hidden="true"></i></button>\n')
w('                  <button type="button" data-dh-track-next="dhVid60" aria-label="Dada 60 — sonraki"><i class="fas fa-chevron-right" aria-hidden="true"></i></button>\n')
w('                </div>\n              </div>\n            </div>\n')
w('            <div class="dh-track dh-shorts" id="dhVid60">\n')
for n, (t, sure, kat, izl) in enumerate(DADA60):
    w('              <a class="dh-short" href="video-detay.html">\n')
    w('                <img class="dh-short__img" src="%s" alt="%s" loading="lazy" decoding="async">\n' % (poster(n), t))
    w('                <span class="dh-short__dur"><i class="fas fa-play" aria-hidden="true"></i> %s</span>\n' % sure)
    w('                <span class="dh-short__play"><i class="fas fa-play" aria-hidden="true"></i></span>\n')
    w('                <span class="dh-short__body">\n')
    w('                  <b class="dh-short__title">%s</b>\n' % t)
    w('                  <span class="dh-short__views"><i class="fas fa-eye" aria-hidden="true"></i> %s</span>\n' % izl)
    w('                </span>\n              </a>\n')
w('            </div>\n          </div>\n        </section>\n\n')

for n, (a, b_, c, t, og) in enumerate(FORMAT):
    ray(a, b_, c, t, og, zebra=(n % 2 == 1))

w('        <!-- Programlar -->\n')
for a, b_, c, k, g, bl in PROGRAM:
    seri(a, b_, c, k, g, bl)

for n, (a, b_, c, t, og) in enumerate(TEMATIK):
    ray(a, b_, c, t, og, zebra=(n % 2 == 0))

# Seriler + Arşiv
w('        <!-- Video Serileri -->\n')
w('        <section class="section panel dh-zeb" id="seriler" aria-labelledby="seriler-b">\n')
w('          <div class="container max-w-xl">\n')
w('            <div class="section-header panel dh-secbar">\n              <div>\n')
w('                <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="seriler-b">Video Serileri</h2>\n')
w('                <p class="dh-vsec__lead">Düzenli yayınlanan tüm seriler tek listede.</p>\n')
w('              </div>\n')
w('              <div class="dh-secbar__tools"><a href="video-kategori-detay.html" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Tümünü Gör</a></div>\n')
w('            </div>\n')
w('            <div class="dh-vgrid">\n')
SERI = [("Ekonomi Masası","24 bölüm","Her Perşembe"),("Sahanın Dili","16 bölüm","Maç sonu"),
        ("Beş Dakikada Dünya","48 bölüm","Her sabah 07.00"),("Yapay Zekâ Notları","12 bölüm","İki haftada bir"),
        ("Kitap Kulübü","30 bölüm","Her Pazar"),("Şehir Rehberi","18 bölüm","Her Cuma")]
for n, (ad, bol, tempo) in enumerate(SERI):
    w('              <a class="dh-vgrid__c" href="video-kategori-detay.html">\n')
    w('                <span class="dh-vgrid__fig"><img src="%s" alt="" loading="lazy" decoding="async"></span>\n' % img(n + 16))
    w('                <span class="dh-vgrid__bd">\n')
    w('                  <b class="dh-vgrid__t">%s</b>\n' % ad)
    w('                  <span class="dh-vgrid__m">%s · %s</span>\n' % (bol, tempo))
    w('                </span>\n              </a>\n')
w('            </div>\n          </div>\n        </section>\n\n')

w('        <!-- Program Arşivi -->\n')
w('        <section class="section panel" id="arsiv" aria-labelledby="arsiv-b">\n')
w('          <div class="container max-w-xl">\n')
w('            <div class="section-header panel dh-secbar">\n              <div>\n')
w('                <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="arsiv-b">Program Arşivi</h2>\n')
w('                <p class="dh-vsec__lead">Yayından kalkmış programlar ve geçmiş sezonlar.</p>\n')
w('              </div>\n')
w('              <div class="dh-secbar__tools"><a href="arsiv.html" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Arşive Git</a></div>\n')
w('            </div>\n')
w('            <ul class="dh-varch">\n')
ARSIV = [("Gündem Masası","2019–2024","5 sezon · 412 bölüm"),("Açık Oturum","2017–2023","6 sezon · 288 bölüm"),
         ("Perde Arkası","2020–2024","4 sezon · 156 bölüm"),("Sorularla","2021–2025","4 sezon · 198 bölüm"),
         ("Karşılıklı","2018–2022","5 sezon · 240 bölüm"),("Haftanın Konuğu","2016–2021","6 sezon · 312 bölüm")]
for ad, yil, bilgi in ARSIV:
    w('              <li><a href="video-kategori-detay.html"><b>%s</b><time>%s</time><span>%s</span></a></li>\n' % (ad, yil, bilgi))
w('            </ul>\n          </div>\n        </section>\n')

govde = o.getvalue()

# --------------------------------------------------- şablona yerleştir
s = open("docs/parts/sayfa-sablon.html", encoding="utf-8").read()
s = s.replace('<body data-dh-cat=""', '<body data-dh-cat="video"', 1)
s = re.sub(r'<title>.*?</title>', '<title>Video — Dada Haber</title>', s, count=1)
m = re.search(r'[ \t]*<!-- ={5,} SAYFA GÖVDESİ BURAYA ={5,}.*?={5,} -->\n', s, re.S)
s = s[:m.start()] + govde + s[m.end():]
if "dh-track.js" not in s:
    k = re.search(r'[ \t]*<script defer src="\./assets/js/dh-panel\.js"></script>[ \t]*\n', s)
    s = s[:k.end()] + '    <script defer src="./assets/js/dh-track.js"></script>\n' + s[k.end():]
open("video.html", "w", encoding="utf-8").write(s)
print("video.html:", len(s.splitlines()), "satır ·", sayac[0], "video kartı")
