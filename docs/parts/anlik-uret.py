# -*- coding: utf-8 -*-
"""Anlık bölümünün alt sayfalarını üretir — yedi sayfa tek elden.

Anlık başlangıçta tek sayfa (çapa) modelindeydi: anlik.html#canli, #dakika …
Kullanıcı her alt başlığın KENDİ SAYFASI olmasını istedi. Bu betik o yedi
sayfayı docs/parts/sayfa-sablon.html şablonundan üretir:

  canli-gundem.html · dakika-dakika.html · bugun-ne-oldu.html ·
  gundem-takvimi.html · guncellenen-haberler.html · afet-acil-durum.html ·
  trafik-ulasim.html

İçerik anlik.html'den TAŞINDI, kopyalanmadı: her bölümün gövdesi burada
GOVDE sözlüğünde durur, sayfaya oradan yazılır; anlik.html'de bölümün yerine
yeni sayfaya giden kompakt bir özet kartı (.dh-nwsum) kalır — onu da bu betik
yazar. Böylece iki taraf birbirinden sapmaz ve betik yeniden çalıştırılabilir
(idempotent).

Dokunulmayanlar:
  · son-dakika.html — zaten vardı, yalnız şeritte adı geçer.
  · "Canlı Yayın" → video.html#canli, "Hava Durumu" → hava-durumu.html.
    Başka bölümlerin sayfaları; şeritte adları geçer, sayfaları burada üretilmez.
  · anlik.html'in #son-dakika, #yayin, #hava bölümleri yerinde kalır —
    merkez sayfa boşalmasın.

Kural notları:
  · Her yol "./" ile başlar; şablondan gelen noindex satırı korunur.
  · Şeritte açıklama etiketi YOK, yalnız isimler (proje kuralı).
  · Sayfaya özgü CSS yalnız assets/css/theme/v2/h-anlik.css'e yazılır.

Çalıştır:  python3 docs/parts/anlik-uret.py
Menü metni değiştiyse önce: python3 docs/parts/uret.py
"""
import os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)
sys.path.insert(0, os.path.join(kok, "docs", "parts"))
import yay                                            # noqa: E402  (isle() için)

SABLON = "docs/parts/sayfa-sablon.html"
MERKEZ = "anlik.html"

# ---------------------------------------------------------------- alt başlıklar
# Sıra uret.py'deki MENU["anlik"] ile aynı. (anahtar, ad, hedef, ikon, açıklama)
ALT = [
    ("son-dakika",  "Son Dakika",           "son-dakika.html",          "fa-bolt",
     "Doğrulanır doğrulanmaz geçilen başlıklar."),
    ("canli",       "Canlı Gündem",         "canli-gundem.html",        "fa-signal-stream",
     "Takibi süren başlıklar ve gelişme sayıları."),
    ("yayin",       "Canlı Yayın",          "video.html#canli",         "fa-play",
     "Dada Haber ekranı ve günün yayın akışı."),
    ("dakika",      "Dakika Dakika",        "dakika-dakika.html",       "fa-clock",
     "Günün gelişmeleri tek akışta, en yeni en üstte."),
    ("bugun",       "Bugün Ne Oldu?",       "bugun-ne-oldu.html",       "fa-calendar-day",
     "Günün başlıkları numaralı özet hâlinde."),
    ("takvim",      "Gündem Takvimi",       "gundem-takvimi.html",      "fa-forward",
     "Bugünden ileriye beklenen gelişmeler."),
    ("guncellenen", "Güncellenen Haberler", "guncellenen-haberler.html", "fa-clock-rotate-left",
     "Yayımlandıktan sonra değişen haberlerin kaydı."),
    ("afet",        "Afet ve Acil Durum",   "afet-acil-durum.html",     "fa-cloud-showers-heavy",
     "Uyarı seviyeleri ve acil çağrı numaraları."),
    ("trafik",      "Trafik ve Ulaşım",     "trafik-ulasim.html",       "fa-car",
     "Yol, raylı sistem, deniz ve hava ulaşımı."),
    ("hava",        "Hava Durumu",          "hava-durumu.html",    "fa-cloud-sun",
     "Sekiz günlük tahmin ve uyarı haritası."),
]
AD = {k: a for k, a, h, i, d in ALT}
HEDEF = {k: h for k, a, h, i, d in ALT}
IKON = {k: i for k, a, h, i, d in ALT}
ACIK = {k: d for k, a, h, i, d in ALT}

# Bu betiğin ürettiği sayfalar (anlik.html'den taşınan yedi bölüm).
URETILEN = ["canli", "dakika", "bugun", "takvim", "guncellenen", "afet", "trafik"]

# ------------------------------------------------------------------- sayfa üstü
# lead   : bannerdaki tek satırlık tanım
# etiket : taşınan bölümün aria-labelledby id'si (şablondan gelmiyor, içerikte)
# sinif  : taşınan bölümün <section> sınıfları
# slayt  : banner slaytları (görsel, başlık, saat, görüntülenme)
SAYFA = {
    "canli": dict(
        lead="Takibi süren başlıklar, gelişme sayılarıyla",
        etiket="dh-nw-canli-t", sinif="section panel pt-5 lg:pt-6 pb-0",
        slayt=[("img-13.jpg", "Bütçe görüşmeleri: Genel Kurul'da ikinci gün", "09:42", 18420),
               ("img-12.jpg", "Faiz kararı sonrası piyasalarda ilk tepki", "09:47", 12730)]),
    "dakika": dict(
        lead="Günün gelişmeleri tek akışta, en yeni en üstte",
        etiket="dh-dakika-t", sinif="section dh-live pt-5 lg:pt-6 pb-0",
        slayt=[("img-12.jpg", "Faiz kararının ardından kur ve borsada ilk hareket", "09:47", 15310),
               ("img-04.jpg", "Bartın ve Kastamonu'da eğitime bir gün ara verildi", "09:30", 8920)]),
    "bugun": dict(
        lead="Günün buraya kadarki başlıkları, bir dakikada",
        etiket="dh-bugun-t", sinif="section panel pt-5 lg:pt-6 pb-0",
        slayt=[("img-17.jpg", "Politika faizi 150 baz puan indirildi", "09:47", 22140),
               ("img-14.jpg", "Brüksel'de iki günlük diplomasi trafiği", "08:58", 6480)]),
    "takvim": dict(
        lead="Bugünden ileriye: açıklanacak veriler, duruşmalar, maçlar",
        etiket="dh-takvim-t", sinif="section panel pt-5 lg:pt-6 pb-0",
        slayt=[("img-05.jpg", "Genel Kurul'da bütçe oylaması bu akşam yapılacak", "09:15", 7420),
               ("img-18.jpg", "Yaz transfer dönemi gece yarısı kapanıyor", "08:40", 9860)]),
    "guncellenen": dict(
        lead="Yayımlandıktan sonra değişen haberlerin kaydı",
        etiket="dh-guncellenen-t", sinif="section panel pt-5 lg:pt-6 pb-0",
        slayt=[("img-12.jpg", "Faiz kararı: karar metninin tam çevirisi eklendi", "09:51", 13380),
               ("img-04.jpg", "Sağanak uyarısı: tatil edilen iller listesi genişledi", "09:34", 10240)]),
    "afet": dict(
        lead="Uyarı seviyeleri, acil çağrı numaraları ve son durum",
        etiket="dh-afet-t", sinif="section panel pt-5 lg:pt-6 pb-0",
        slayt=[("img-11.jpg", "Batı Karadeniz'de altı il için turuncu kod", "09:40", 24110),
               ("img-09.jpg", "Akdeniz kıyı şeridinde orman yangını riski yüksek", "08:15", 9310)]),
    "trafik": dict(
        lead="Yol, raylı sistem, deniz ve hava ulaşımında son durum",
        etiket="dh-trafik-t", sinif="section panel pt-5 lg:pt-6 pb-0",
        slayt=[("img-06.jpg", "İstanbul trafiğinde sabah yoğunluğu %71'e çıktı", "09:45", 11240),
               ("img-20.jpg", "Kuzey Marmara Otoyolu'nda bakım: bir şerit kapalı", "09:10", 5170)]),
}

# anlik.html'de bölümün yerine kalan kompakt kartın üç satırlık önizlemesi
ONIZLEME = {
    "canli": ["Bütçe görüşmeleri: Genel Kurul'da ikinci gün",
              "Faiz kararı sonrası piyasalarda ilk tepki",
              "Transfer dönemi: son gün kapanışa saatler kaldı"],
    "dakika": ["09:47 · Faiz kararının ardından kur ve borsada ilk hareket",
               "09:30 · Bartın ve Kastamonu'da eğitime bir gün ara verildi",
               "08:36 · Marmaray seferleri normale döndü"],
    "bugun": ["Politika faizi 150 baz puan indirildi",
              "Bütçe görüşmelerinde ikinci gün başladı",
              "Altı il için turuncu kodlu sağanak uyarısı"],
    "takvim": ["Bugün 20:00 · Genel Kurul'da bütçe oylaması",
               "Yarın 10:00 · Süper Lig 3. hafta programı",
               "24 Ağustos 10:00 · TÜİK tüketici güven endeksi"],
    "guncellenen": ["09:51 · Faiz kararı metninin tam çevirisi eklendi",
                    "09:34 · Tatil edilen iller listesi genişledi",
                    "08:47 · Marmaray gecikme süresi düzeltildi"],
    "afet": ["Kuvvetli sağanak — Batı Karadeniz · TURUNCU KOD",
             "Orman yangını riski — Akdeniz kıyı şeridi · YÜKSEK RİSK",
             "Barajlar ve taşkın durumu · NORMAL"],
    "trafik": ["İstanbul trafik yoğunluğu · %71 YOĞUN",
               "Kuzey Marmara Otoyolu · ŞERİT KAPALI",
               "Raylı sistemler · NORMAL"],
}

# anlik.html'deki kompakt kartın başlık çubuğunda duran damga
DAMGA = {
    "canli": ('fa-signal-stream', '5 başlık takipte'),
    "dakika": ('fa-rotate', "Akış 09.47'de güncellendi"),
    "bugun": ('fa-calendar-day', '21 Ağustos 2026 Cuma'),
    "takvim": ('fa-forward', 'Bugünden ileriye'),
    "guncellenen": ('fa-clock-rotate-left', 'Son 24 saat'),
    "afet": ('fa-rotate', '09:40 güncellendi'),
    "trafik": ('fa-map-marker-alt', 'İstanbul · 09:45'),
}


# ------------------------------------------------------- sayfaya özgü ek bölüm
# Alt başlık kendi sayfasına çıkınca merkez sayfadaki tek modül sayfayı
# doldurmuyor. Her sayfaya konusuyla devam eden ikinci bir bölüm eklendi;
# hepsi mevcut .dh-nwlist / .dh-nwstat bileşenlerini kullanır, yeni bileşen yok.
EK = {}

EK["canli"] = """    <section class="section panel pt-5 lg:pt-6 pb-0" id="kapanan" aria-labelledby="dh-nwek-canli-t">
      <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-nwek-canli-t">Canlı Takibi Kapanan Başlıklar</h2>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-clock-rotate-left" aria-hidden="true"></i> Son 24 saat</span>
            <a href="arsiv.html" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Arşiv</a>
          </div>
        </div>
        <p class="dh-nwintro">Takibi sona eren başlıklar. Akış kapandı, sayfa son hâliyle duruyor; yeni gelişme olursa başlık yeniden açılır.</p>
        <ul class="dh-nwlist dh-nwlist--upd">
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-21T07:40">07:40</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Gece açıklanan enflasyon revizyonu</a></h3>
              <span class="dh-nwlist__note">Takip kapandı · 62 gelişme · süre 5 sa 20 dk</span>
            </div>
            <span class="dh-nwlist__tag">EKONOMİ</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-21T06:10">06:10</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Marmaray sinyalizasyon arızası ve sefer düzeni</a></h3>
              <span class="dh-nwlist__note">Takip kapandı · 28 gelişme · süre 2 sa 05 dk</span>
            </div>
            <span class="dh-nwlist__tag">ULAŞIM</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-20T23:55">23:55</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Avrupa kupası rövanşı: maç sonu değerlendirmeleri</a></h3>
              <span class="dh-nwlist__note">Takip kapandı · 91 gelişme · süre 4 sa 40 dk</span>
            </div>
            <span class="dh-nwlist__tag">SPOR</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-20T21:30">21:30</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Yerli haberleşme uydusu entegrasyon süreci</a></h3>
              <span class="dh-nwlist__note">Takip kapandı · 19 gelişme · süre 3 sa 10 dk</span>
            </div>
            <span class="dh-nwlist__tag">TEKNOLOJİ</span>
          </li>
        </ul>
      </div>
    </section>
"""

EK["dakika"] = """    <section class="section panel pt-5 lg:pt-6 pb-0" id="cok-okunan" aria-labelledby="dh-nwek-dakika-t">
      <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-nwek-dakika-t">Akışta En Çok Okunanlar</h2>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-clock" aria-hidden="true"></i> Son 6 saat</span>
          </div>
        </div>
        <p class="dh-nwintro">Akıştaki maddelerin tıklanma sırası. Sıralama otomatik hesaplanır, editör müdahalesi yoktur.</p>
        <ol class="dh-nwlist dh-nwlist--ozet">
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">1</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Faiz kararının ardından kur ve borsada ilk hareket</a></h3>
              <p class="dh-nwlist__sum">Bankacılık endeksinin açılışta öne çıktığı görüldü.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-21T09:47">09:47</time> · EKONOMİ</span>
            </div>
          </li>
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">2</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Bartın ve Kastamonu'da eğitime bir gün ara verildi</a></h3>
              <p class="dh-nwlist__sum">Valilik kararının kuvvetli yağış beklentisiyle alındığı belirtildi.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-21T09:30">09:30</time> · AFET</span>
            </div>
          </li>
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">3</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Marmaray seferleri normale döndü</a></h3>
              <p class="dh-nwlist__sum">Sabah yoğunluğundaki 12 dakikalık gecikmenin telafi edildiği açıklandı.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-21T08:36">08:36</time> · ULAŞIM</span>
            </div>
          </li>
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">4</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Genel Kurul'da üç bakanlığın bütçesi görüşülüyor</a></h3>
              <p class="dh-nwlist__sum">Oturumun gün boyu süreceği, akşam oylamaya geçileceği bildirildi.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-21T09:42">09:42</time> · GÜNDEM</span>
            </div>
          </li>
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">5</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Ege'de arama kurtarma tatbikatı başladı</a></h3>
              <p class="dh-nwlist__sum">İki gün sürecek tatbikata deniz ve hava unsurları katılıyor.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-21T09:05">09:05</time> · DÜNYA</span>
            </div>
          </li>
        </ol>
      </div>
    </section>
"""

EK["bugun"] = """    <section class="section panel pt-5 lg:pt-6 pb-0" id="dun" aria-labelledby="dh-nwek-bugun-t">
      <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-nwek-bugun-t">Dün Ne Oldu?</h2>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-calendar-day" aria-hidden="true"></i> 20 Ağustos 2026 Perşembe</span>
            <a href="arsiv.html" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Arşiv</a>
          </div>
        </div>
        <p class="dh-nwintro">Bir önceki günün kapanış özeti. Gün bittiğinde liste dondurulur ve arşive alınır.</p>
        <ol class="dh-nwlist dh-nwlist--ozet">
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">1</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Bütçe görüşmeleri Genel Kurul'da başladı</a></h3>
              <p class="dh-nwlist__sum">İlk gün iki bakanlığın bütçesi görüşüldü, oturum gece yarısı kapandı.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-20T11:20">11:20</time> · GÜNDEM</span>
            </div>
          </li>
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">2</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Avrupa kupalarında temsilcimiz turu geçti</a></h3>
              <p class="dh-nwlist__sum">Rövanşın ardından kura çekiminin çarşamba günü yapılacağı bildirildi.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-20T22:15">22:15</time> · SPOR</span>
            </div>
          </li>
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">3</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Yerli haberleşme uydusunda entegrasyon tamamlandı</a></h3>
              <p class="dh-nwlist__sum">Fırlatma takviminin yıl sonunda açıklanacağı belirtildi.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-20T20:40">20:40</time> · TEKNOLOJİ</span>
            </div>
          </li>
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">4</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Tarım ürünlerinde ihracat rakamları açıklandı</a></h3>
              <p class="dh-nwlist__sum">Temmuz verisinde yaş meyve sebze kaleminin öne çıktığı görüldü.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-20T14:05">14:05</time> · EKONOMİ</span>
            </div>
          </li>
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">5</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Kültür yolu festivali programı duyuruldu</a></h3>
              <p class="dh-nwlist__sum">Eylül boyunca dört ilde 120 etkinlik yapılacağı açıklandı.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-20T12:30">12:30</time> · KÜLTÜR</span>
            </div>
          </li>
        </ol>
      </div>
    </section>
"""

EK["takvim"] = """    <section class="section panel pt-5 lg:pt-6 pb-0" id="ileri-takvim" aria-labelledby="dh-nwek-takvim-t">
      <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-nwek-takvim-t">Eylülde Öne Çıkanlar</h2>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-forward" aria-hidden="true"></i> Önümüzdeki ay</span>
          </div>
        </div>
        <p class="dh-nwintro">Tarihi kesinleşmiş, ay içine yayılan gelişmeler. Saati açıklanmamış maddelerde yalnız gün yazar.</p>
        <ol class="dh-nwlist dh-nwlist--cal">
          <li class="dh-nwlist__day"><span>1 Eylül Salı</span></li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-09-01T09:00">09:00</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">YKS ek yerleştirme başvuruları başlıyor</a></h3>
              <p class="dh-nwlist__sum">Başvurular on gün sürecek, sonuçlar ayın ortasında açıklanacak.</p>
            </div>
            <span class="dh-nwlist__tag">EĞİTİM</span>
          </li>
          <li class="dh-nwlist__day"><span>3 Eylül Perşembe</span></li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-09-03T10:00">10:00</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">TÜİK ağustos enflasyon verisi</a></h3>
              <p class="dh-nwlist__sum">Aylık ve yıllık tüketici fiyat endeksi açıklanacak.</p>
            </div>
            <span class="dh-nwlist__tag">EKONOMİ</span>
          </li>
          <li class="dh-nwlist__day"><span>7 Eylül Pazartesi</span></li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-09-07T08:30">08:30</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Yeni eğitim öğretim yılı başlıyor</a></h3>
              <p class="dh-nwlist__sum">Okul servis ücretleri ve ulaşım düzenlemeleri aynı gün yürürlüğe giriyor.</p>
            </div>
            <span class="dh-nwlist__tag">EĞİTİM</span>
          </li>
          <li class="dh-nwlist__day"><span>17 Eylül Perşembe</span></li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-09-17T14:00">14:00</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Para Politikası Kurulu toplantısı</a></h3>
              <p class="dh-nwlist__sum">Yılın yedinci faiz kararı açıklanacak.</p>
            </div>
            <span class="dh-nwlist__tag">EKONOMİ</span>
          </li>
        </ol>
      </div>
    </section>
"""

EK["guncellenen"] = """    <section class="section dh-serit dh-serit--ak bg-white dark:bg-gray-900" id="duzeltme" aria-labelledby="dh-nwek-guncellenen-t">
      <div class="section-outer panel py-4 lg:py-8">
        <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-nwek-guncellenen-t">Düzeltme ve Yanıt Notları</h2>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-clock-rotate-left" aria-hidden="true"></i> Son 7 gün</span>
            <a href="yayin-ilkeleri.html" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Yayın İlkeleri</a>
          </div>
        </div>
        <p class="dh-nwintro">Bir haberde hata yapıldığında düzeltme metin içinde değil, ayrı bir not olarak eklenir ve burada listelenir. Notlar silinmez.</p>
        <ul class="dh-nwlist dh-nwlist--upd">
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-21T08:47">08:47</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Marmaray gecikme süresi 20 dakika değil 12 dakikadır</a></h3>
              <span class="dh-nwlist__note">Düzeltme · ilk yayım <time datetime="2026-08-21T06:22">06:22</time> · kaynak yeniden teyit edildi</span>
            </div>
            <span class="dh-nwlist__tag">DÜZELTME</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-20T21:10">21:10</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Uydu fırlatma takvimi &quot;yıl sonu&quot; olarak netleştirildi</a></h3>
              <span class="dh-nwlist__note">Düzeltme · ifade belirsizdi, kurum açıklamasıyla değiştirildi</span>
            </div>
            <span class="dh-nwlist__tag">DÜZELTME</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-19T16:40">16:40</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Belediye açıklaması habere yanıt olarak eklendi</a></h3>
              <span class="dh-nwlist__note">Yanıt hakkı · kurum metni kısaltılmadan yayımlandı</span>
            </div>
            <span class="dh-nwlist__tag">YANIT</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-18T11:05">11:05</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Fotoğraf altyazısındaki yer adı düzeltildi</a></h3>
              <span class="dh-nwlist__note">Düzeltme · görsel değişmedi, yalnız altyazı güncellendi</span>
            </div>
            <span class="dh-nwlist__tag">DÜZELTME</span>
          </li>
        </ul>
        </div>
      </div>
    </section>


    <section class="section panel" id="ilke" aria-labelledby="dh-ilke-t">
      <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-ilke-t">Bir Haber Neden Güncellenir?</h2>
          <div class="dh-secbar__tools">
            <a href="yayin-ilkeleri.html" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Yayın İlkeleri</a>
          </div>
        </div>
        <p class="dh-nwintro">Güncelleme haberin geçmişini silmez. Her değişiklik saatiyle kaydedilir; düzeltme gerektiren durumlarda ayrı bir not eklenir.</p>
        <ul class="dh-ilke">
          <li class="dh-ilke__it">
            <span class="dh-ilke__ic" aria-hidden="true"><i class="fas fa-plus"></i></span>
            <b class="dh-ilke__t">Yeni bilgi eklendi</b>
            <span class="dh-ilke__d">Gelişme sürüyor; doğrulanan her yeni ayrıntı habere işlenir. Başlık değişmez.</span>
          </li>
          <li class="dh-ilke__it">
            <span class="dh-ilke__ic" aria-hidden="true"><i class="fas fa-pen"></i></span>
            <b class="dh-ilke__t">İfade netleştirildi</b>
            <span class="dh-ilke__d">Anlam aynı kalır, cümle daha açık yazılır. Metin içinde iz bırakılmaz, kayıt burada tutulur.</span>
          </li>
          <li class="dh-ilke__it">
            <span class="dh-ilke__ic" aria-hidden="true"><i class="fas fa-triangle-exclamation"></i></span>
            <b class="dh-ilke__t">Düzeltme yapıldı</b>
            <span class="dh-ilke__d">Yanlış bir bilgi yayımlandıysa habere düzeltme notu eklenir ve not silinmez.</span>
          </li>
          <li class="dh-ilke__it">
            <span class="dh-ilke__ic" aria-hidden="true"><i class="fas fa-reply"></i></span>
            <b class="dh-ilke__t">Yanıt hakkı kullanıldı</b>
            <span class="dh-ilke__d">Haberde adı geçen kurum ya da kişinin yanıtı, kısaltılmadan habere eklenir.</span>
          </li>
        </ul>
      </div>
    </section>"""

EK["afet"] = """    <section class="section panel dh-serit bg-gray-10 dark:bg-gray-800" id="deprem" aria-labelledby="dh-nwek-afet-t">
      <div class="section-outer panel py-4 lg:py-8">
        <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-nwek-afet-t">Son 24 Saatte Hissedilen Depremler</h2>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-rotate" aria-hidden="true"></i> <time datetime="2026-08-21T09:40">09:40</time> itibarıyla</span>
            <a href="veri-harita.html#afet" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Afet Haritası</a>
          </div>
        </div>
        <p class="dh-nwintro">Büyüklüğü 3,0 ve üzeri olan, yerleşim yerlerinde hissedilen sarsıntılar. Resmî kayıt AFAD ve Kandilli listelerindedir.</p>
        <ul class="dh-nwlist dh-nwlist--upd">
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-21T06:12">06:12</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Ege Denizi açıkları — 3,8</a></h3>
              <span class="dh-nwlist__note">Derinlik 7,2 km · İzmir ve Muğla'da hissedildi · hasar ihbarı yok</span>
            </div>
            <span class="dh-nwlist__tag">3,8</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-21T02:48">02:48</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Simav — Kütahya — 3,4</a></h3>
              <span class="dh-nwlist__note">Derinlik 9,0 km · çevre ilçelerde hafif hissedildi</span>
            </div>
            <span class="dh-nwlist__tag">3,4</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-20T19:26">19:26</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Akdeniz — Antalya açıkları — 3,1</a></h3>
              <span class="dh-nwlist__note">Derinlik 24,6 km · kıyı şeridinde hissedilmedi</span>
            </div>
            <span class="dh-nwlist__tag">3,1</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-20T13:04">13:04</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Yedisu — Bingöl — 3,3</a></h3>
              <span class="dh-nwlist__note">Derinlik 6,8 km · merkez ilçede hissedildi · hasar ihbarı yok</span>
            </div>
            <span class="dh-nwlist__tag">3,3</span>
          </li>
        </ul>
        </div>
      </div>
    </section>


    <section class="section panel" id="hazirlik" aria-labelledby="dh-hazirlik-t">
      <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-hazirlik-t">Afet Öncesi Hazırlık</h2>
          <div class="dh-secbar__tools">
            <a href="https://www.afad.gov.tr/" rel="noopener noreferrer" target="_blank" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">AFAD</a>
          </div>
        </div>
        <p class="dh-nwintro">Bu sayfa resmî bir uyarı kanalı değildir. Aşağıdakiler hatırlatmadır; afet anında AFAD ve valilik duyurularını esas alın.</p>
        <ul class="dh-ilke">
          <li class="dh-ilke__it">
            <span class="dh-ilke__ic" aria-hidden="true"><i class="fas fa-box-open"></i></span>
            <b class="dh-ilke__t">Afet çantası hazır mı?</b>
            <span class="dh-ilke__d">Su, kuru gıda, ilk yardım seti, el feneri, düdük, powerbank ve kimlik fotokopisi. Yılda bir tazeleyin.</span>
          </li>
          <li class="dh-ilke__it">
            <span class="dh-ilke__ic" aria-hidden="true"><i class="fas fa-people-roof"></i></span>
            <b class="dh-ilke__t">Buluşma noktası belirleyin</b>
            <span class="dh-ilke__d">Ev içinde ve dışında iki ayrı nokta. Hane halkının tamamı ezbere bilsin.</span>
          </li>
          <li class="dh-ilke__it">
            <span class="dh-ilke__ic" aria-hidden="true"><i class="fas fa-couch"></i></span>
            <b class="dh-ilke__t">Devrilebilecekleri sabitleyin</b>
            <span class="dh-ilke__d">Dolap, kitaplık ve televizyon duvara sabitlenmeli; yatak başına ağır eşya konmamalı.</span>
          </li>
          <li class="dh-ilke__it">
            <span class="dh-ilke__ic" aria-hidden="true"><i class="fas fa-mobile-screen"></i></span>
            <b class="dh-ilke__t">Haberleşmeyi planlayın</b>
            <span class="dh-ilke__d">Şebeke yoğunsa arama yerine kısa mesaj. Şehir dışından bir kişiyi ortak irtibat seçin.</span>
          </li>
        </ul>
      </div>
    </section>"""

EK["trafik"] = """    <section class="section panel dh-serit bg-gray-10 dark:bg-gray-800" id="yol" aria-labelledby="dh-nwek-trafik-t">
      <div class="section-outer panel py-4 lg:py-8">
        <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-nwek-trafik-t">Şehirlerarası Yol Durumu</h2>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-rotate" aria-hidden="true"></i> <time datetime="2026-08-21T09:45">09:45</time> itibarıyla</span>
          </div>
        </div>
        <p class="dh-nwintro">Ana güzergâhlarda yol çalışması, hava koşulu ve kapanma bilgisi. Kar ve buzlanma dönemlerinde liste saatlik yenilenir.</p>
        <div class="dh-nwstat dh-nwstat--trafik">
          <ul class="dh-nwstat__rows">
            <li class="dh-nwstat__row" data-lv="uyari">
              <span class="dh-nwstat__ic" aria-hidden="true"><i class="fas fa-road"></i></span>
              <span class="dh-nwstat__body">
                <b class="dh-nwstat__name">Bolu Dağı geçişi — Ankara yönü</b>
                <span class="dh-nwstat__desc">Yağış nedeniyle görüş mesafesi düşük. Ekipler güzergâhta, hız sınırı 70 km/s.</span>
              </span>
              <span class="dh-nwstat__lv">DİKKATLİ GEÇİŞ</span>
            </li>
            <li class="dh-nwstat__row" data-lv="ok">
              <span class="dh-nwstat__ic" aria-hidden="true"><i class="fas fa-road"></i></span>
              <span class="dh-nwstat__body">
                <b class="dh-nwstat__name">Tarsus — Adana — Gaziantep otoyolu</b>
                <span class="dh-nwstat__desc">Trafik akıcı. Pozantı bakım çalışması dün tamamlandı.</span>
              </span>
              <span class="dh-nwstat__lv">AKICI</span>
            </li>
            <li class="dh-nwstat__row" data-lv="dikkat">
              <span class="dh-nwstat__ic" aria-hidden="true"><i class="fas fa-bus"></i></span>
              <span class="dh-nwstat__body">
                <b class="dh-nwstat__name">Karadeniz sahil yolu — Bartın kesimi</b>
                <span class="dh-nwstat__desc">Sağanak nedeniyle iki noktada su birikintisi. Otobüs seferlerinde 25 dakikaya varan gecikme.</span>
              </span>
              <span class="dh-nwstat__lv">GECİKMELİ</span>
            </li>
            <li class="dh-nwstat__row" data-lv="ok">
              <span class="dh-nwstat__ic" aria-hidden="true"><i class="fas fa-train-subway"></i></span>
              <span class="dh-nwstat__body">
                <b class="dh-nwstat__name">Yüksek hızlı tren hatları</b>
                <span class="dh-nwstat__desc">Ankara — İstanbul ve Ankara — Konya hatlarında sefer aksaması yok.</span>
              </span>
              <span class="dh-nwstat__lv">NORMAL</span>
            </li>
          </ul>
        </div>
        </div>
      </div>
    </section>


    <script type="application/json" id="dh-trafik-data">
{"varsayilan":"istanbul","sehirler":{"istanbul":{"ad":"İstanbul","bolge":"Marmara","nufus":"15,9 mn nüfus","saat":"08.00","yogunluk":34,"sikisik":"E-5 Bakırköy — Zeytinburnu","satirlar":[{"ad":"Kuzey Marmara Otoyolu","aciklama":"Hafif yoğunluk; gişe çıkışlarında kısa kuyruk.","lv":"normal","etiket":"NORMAL","ikon":"fa-road"},{"ad":"Marmaray · Metro","aciklama":"Marmaray'da 4 dakikalık gecikme, metro hatları normal.","lv":"uyari","etiket":"DİKKAT","ikon":"fa-train-subway"},{"ad":"Şehir hatları","aciklama":"Boğaz hattında lodos nedeniyle iki sefer iptal.","lv":"kritik","etiket":"YOĞUN","ikon":"fa-ship"},{"ad":"İstanbul · Sabiha Gökçen","aciklama":"Ortalama gecikme 6 dakika. Kapanan pist yok.","lv":"normal","etiket":"NORMAL","ikon":"fa-plane"}]},"ankara":{"ad":"Ankara","bolge":"İç Anadolu","nufus":"5,8 mn nüfus","saat":"09.13","yogunluk":51,"sikisik":"Eskişehir Yolu — Söğütözü kavşağı","satirlar":[{"ad":"Çevre yolu","aciklama":"Konya Yolu bağlantısında bakım çalışması, tek şerit kapalı.","lv":"uyari","etiket":"DİKKAT","ikon":"fa-road"},{"ad":"Ankaray · Metro","aciklama":"M4 hattında sefer sıklığı artırıldı, aksama yok.","lv":"kritik","etiket":"YOĞUN","ikon":"fa-train-subway"},{"ad":"Deniz ulaşımı · yok","aciklama":"Şehirde deniz ulaşımı bulunmuyor.","lv":"normal","etiket":"NORMAL","ikon":"fa-ship"},{"ad":"Esenboğa","aciklama":"Ortalama gecikme 4 dakika. Sis uyarısı yok.","lv":"uyari","etiket":"DİKKAT","ikon":"fa-plane"}]},"izmir":{"ad":"İzmir","bolge":"Ege","nufus":"4,5 mn nüfus","saat":"10.26","yogunluk":68,"sikisik":"Mustafa Kemal Sahil Bulvarı","satirlar":[{"ad":"İzmir Çevre Yolu","aciklama":"Trafik akıcı; Gaziemir çıkışında kısa yavaşlama.","lv":"kritik","etiket":"YOĞUN","ikon":"fa-road"},{"ad":"İZBAN · Metro","aciklama":"İZBAN'da 6 dakikalık gecikme, metro normal.","lv":"normal","etiket":"NORMAL","ikon":"fa-train-subway"},{"ad":"Vapur hatları","aciklama":"Karşıyaka — Konak seferleri normal.","lv":"uyari","etiket":"DİKKAT","ikon":"fa-ship"},{"ad":"Adnan Menderes","aciklama":"Gecikme yok.","lv":"kritik","etiket":"YOĞUN","ikon":"fa-plane"}]},"bursa":{"ad":"Bursa","bolge":"Marmara","nufus":"3,2 mn nüfus","saat":"11.39","yogunluk":85,"sikisik":"Ankara Yolu — Ovaakça","satirlar":[{"ad":"Bursa çevre yolu","aciklama":"İnegöl yönünde yol çalışması sürüyor.","lv":"normal","etiket":"NORMAL","ikon":"fa-road"},{"ad":"Bursaray","aciklama":"Seferler normal.","lv":"uyari","etiket":"DİKKAT","ikon":"fa-train-subway"},{"ad":"Mudanya hattı","aciklama":"Deniz otobüsü seferleri normal.","lv":"kritik","etiket":"YOĞUN","ikon":"fa-ship"},{"ad":"Yenişehir","aciklama":"Gecikme yok.","lv":"normal","etiket":"NORMAL","ikon":"fa-plane"}]},"antalya":{"ad":"Antalya","bolge":"Akdeniz","nufus":"2,7 mn nüfus","saat":"12.52","yogunluk":47,"sikisik":"Konyaaltı — Lara aksı","satirlar":[{"ad":"D-400 karayolu","aciklama":"Turizm sezonu yoğunluğu; Kemer yönü sıkışık.","lv":"uyari","etiket":"DİKKAT","ikon":"fa-road"},{"ad":"Antray","aciklama":"Seferler normal.","lv":"kritik","etiket":"YOĞUN","ikon":"fa-train-subway"},{"ad":"Kaleiçi marina","aciklama":"Tur tekneleri normal çalışıyor.","lv":"normal","etiket":"NORMAL","ikon":"fa-ship"},{"ad":"Antalya","aciklama":"Yoğun tarifede ortalama 9 dakika gecikme.","lv":"uyari","etiket":"DİKKAT","ikon":"fa-plane"}]},"adana":{"ad":"Adana","bolge":"Akdeniz","nufus":"2,3 mn nüfus","saat":"13.05","yogunluk":64,"sikisik":"Turhan Cemal Beriker Bulvarı","satirlar":[{"ad":"Tarsus — Adana — Gaziantep otoyolu","aciklama":"Trafik akıcı; Pozantı bakımı tamamlandı.","lv":"kritik","etiket":"YOĞUN","ikon":"fa-road"},{"ad":"Adana Metro","aciklama":"Seferler normal.","lv":"normal","etiket":"NORMAL","ikon":"fa-train-subway"},{"ad":"Deniz ulaşımı · yok","aciklama":"Şehirde deniz ulaşımı bulunmuyor.","lv":"normal","etiket":"NORMAL","ikon":"fa-ship"},{"ad":"Çukurova","aciklama":"Gecikme yok.","lv":"kritik","etiket":"YOĞUN","ikon":"fa-plane"}]},"konya":{"ad":"Konya","bolge":"İç Anadolu","nufus":"2,3 mn nüfus","saat":"14.18","yogunluk":81,"sikisik":"Yeni İstanbul Caddesi","satirlar":[{"ad":"Konya — Ankara yolu","aciklama":"Yol çalışması yok, akış normal.","lv":"normal","etiket":"NORMAL","ikon":"fa-road"},{"ad":"Tramvay","aciklama":"Seferler normal.","lv":"uyari","etiket":"DİKKAT","ikon":"fa-train-subway"},{"ad":"Deniz ulaşımı · yok","aciklama":"Şehirde deniz ulaşımı bulunmuyor.","lv":"normal","etiket":"NORMAL","ikon":"fa-ship"},{"ad":"Konya","aciklama":"Gecikme yok.","lv":"normal","etiket":"NORMAL","ikon":"fa-plane"}]},"gaziantep":{"ad":"Gaziantep","bolge":"Güneydoğu Anadolu","nufus":"2,1 mn nüfus","saat":"15.31","yogunluk":43,"sikisik":"Şehitkâmil — Karataş bağlantısı","satirlar":[{"ad":"Şanlıurfa yolu","aciklama":"Ağır taşıt yoğunluğu; sağ şerit yavaş.","lv":"uyari","etiket":"DİKKAT","ikon":"fa-road"},{"ad":"Gaziray","aciklama":"Seferler normal.","lv":"kritik","etiket":"YOĞUN","ikon":"fa-train-subway"},{"ad":"Deniz ulaşımı · yok","aciklama":"Şehirde deniz ulaşımı bulunmuyor.","lv":"normal","etiket":"NORMAL","ikon":"fa-ship"},{"ad":"Oğuzeli","aciklama":"Gecikme yok.","lv":"uyari","etiket":"DİKKAT","ikon":"fa-plane"}]},"trabzon":{"ad":"Trabzon","bolge":"Karadeniz","nufus":"0,8 mn nüfus","saat":"16.44","yogunluk":60,"sikisik":"Sahil yolu — Değirmendere","satirlar":[{"ad":"Karadeniz sahil yolu","aciklama":"Sağanak nedeniyle iki noktada su birikintisi.","lv":"kritik","etiket":"YOĞUN","ikon":"fa-road"},{"ad":"Raylı sistem · yok","aciklama":"Şehirde raylı sistem bulunmuyor.","lv":"normal","etiket":"NORMAL","ikon":"fa-train-subway"},{"ad":"Liman","aciklama":"Yolcu seferleri normal.","lv":"uyari","etiket":"DİKKAT","ikon":"fa-ship"},{"ad":"Trabzon","aciklama":"Rüzgâr nedeniyle ortalama 12 dakika gecikme.","lv":"kritik","etiket":"YOĞUN","ikon":"fa-plane"}]},"samsun":{"ad":"Samsun","bolge":"Karadeniz","nufus":"1,4 mn nüfus","saat":"17.57","yogunluk":77,"sikisik":"Atatürk Bulvarı — sahil kesimi","satirlar":[{"ad":"Samsun — Ordu yolu","aciklama":"Trafik akıcı.","lv":"normal","etiket":"NORMAL","ikon":"fa-road"},{"ad":"Samulaş tramvay","aciklama":"Seferler normal.","lv":"uyari","etiket":"DİKKAT","ikon":"fa-train-subway"},{"ad":"Liman","aciklama":"Yük trafiği normal.","lv":"kritik","etiket":"YOĞUN","ikon":"fa-ship"},{"ad":"Çarşamba","aciklama":"Gecikme yok.","lv":"normal","etiket":"NORMAL","ikon":"fa-plane"}]}}}
    </script>

    <script defer src="./assets/js/v2/dh-trafik.js"></script>"""


# ---------------------------------------------------------- taşınan gövdeler
# anlik.html'den TAŞINDI (kopya değil). Bölümün <section> sarmalayıcısı
# SAYFA[k]["sinif"] ile yeniden kurulur; burada yalnız kap içi durur.
GOVDE = {}
GOVDE["canli"] = """      <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <div class="dh-live__heading">
            <span class="dh-live__badge"><span class="dh-live__pulse" aria-hidden="true"></span> CANLI</span>
            <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-nw-canli-t">Canlı Gündem</h2>
          </div>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-signal-stream" aria-hidden="true"></i> 5 başlık takipte</span>
            <div class="dh-secbar__nav">
              <button type="button" data-dh-track-prev="dhCanliTrack" aria-label="Önceki başlıklar"><i class="fas fa-chevron-left" aria-hidden="true"></i></button>
              <button type="button" data-dh-track-next="dhCanliTrack" aria-label="Sonraki başlıklar"><i class="fas fa-chevron-right" aria-hidden="true"></i></button>
            </div>
          </div>
        </div>
        <div class="dh-track" id="dhCanliTrack">
          <a class="dh-nwtopic" href="haber-detay.html">
            <span class="dh-nwtopic__fig">
              <img class="dh-nwtopic__img" src="./assets/images/main/posts/img-13.jpg" alt="" loading="lazy" decoding="async">
              <span class="dh-nwtopic__badge"><span class="dh-live__pulse" aria-hidden="true"></span> CANLI</span>
            </span>
            <b class="dh-nwtopic__title">Bütçe görüşmeleri: Genel Kurul'da ikinci gün</b>
            <span class="dh-nwtopic__meta">
              <span class="dh-nwtopic__cnt">34 gelişme</span>
              <time datetime="2026-08-21T09:42">09:42</time>
            </span>
          </a>
          <a class="dh-nwtopic" href="haber-detay.html">
            <span class="dh-nwtopic__fig">
              <img class="dh-nwtopic__img" src="./assets/images/main/posts/img-12.jpg" alt="" loading="lazy" decoding="async">
              <span class="dh-nwtopic__badge"><span class="dh-live__pulse" aria-hidden="true"></span> CANLI</span>
            </span>
            <b class="dh-nwtopic__title">Faiz kararı sonrası piyasalarda ilk tepki</b>
            <span class="dh-nwtopic__meta">
              <span class="dh-nwtopic__cnt">21 gelişme</span>
              <time datetime="2026-08-21T09:47">09:47</time>
            </span>
          </a>
          <a class="dh-nwtopic" href="haber-detay.html">
            <span class="dh-nwtopic__fig">
              <img class="dh-nwtopic__img" src="./assets/images/main/posts/img-04.jpg" alt="" loading="lazy" decoding="async">
              <span class="dh-nwtopic__badge"><span class="dh-live__pulse" aria-hidden="true"></span> CANLI</span>
            </span>
            <b class="dh-nwtopic__title">Batı Karadeniz'de sağanak: yol ve okul durumu</b>
            <span class="dh-nwtopic__meta">
              <span class="dh-nwtopic__cnt">17 gelişme</span>
              <time datetime="2026-08-21T09:30">09:30</time>
            </span>
          </a>
          <a class="dh-nwtopic" href="haber-detay.html">
            <span class="dh-nwtopic__fig">
              <img class="dh-nwtopic__img" src="./assets/images/main/posts/img-14.jpg" alt="" loading="lazy" decoding="async">
              <span class="dh-nwtopic__badge"><span class="dh-live__pulse" aria-hidden="true"></span> CANLI</span>
            </span>
            <b class="dh-nwtopic__title">Brüksel temasları: gümrük birliği masada</b>
            <span class="dh-nwtopic__meta">
              <span class="dh-nwtopic__cnt">9 gelişme</span>
              <time datetime="2026-08-21T08:58">08:58</time>
            </span>
          </a>
          <a class="dh-nwtopic" href="haber-detay.html">
            <span class="dh-nwtopic__fig">
              <img class="dh-nwtopic__img" src="./assets/images/demo-six/posts/img-17.jpg" alt="" loading="lazy" decoding="async">
              <span class="dh-nwtopic__badge"><span class="dh-live__pulse" aria-hidden="true"></span> CANLI</span>
            </span>
            <b class="dh-nwtopic__title">Transfer dönemi: son gün kapanışa saatler kaldı</b>
            <span class="dh-nwtopic__meta">
              <span class="dh-nwtopic__cnt">48 gelişme</span>
              <time datetime="2026-08-21T09:20">09:20</time>
            </span>
          </a>
        </div>
      </div>"""

GOVDE["dakika"] = """      <div class="container max-w-xl">
        <header class="dh-secbar dh-live__bar">
          <div class="dh-live__heading">
            <span class="dh-live__badge"><span class="dh-live__pulse" aria-hidden="true"></span> CANLI</span>
            <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-dakika-t">Dakika Dakika</h2>
          </div>
          <div class="dh-secbar__tools">
            <span class="dh-astro__stamp"><i class="fas fa-rotate" aria-hidden="true"></i> Akış 09.47'de güncellendi</span>
          </div>
        </header>

        <div class="dh-live__periods">
          <div class="dh-sort" role="tablist" aria-label="Akış aralığı">
            <button type="button" class="dh-sort__tab is-on" role="tab" aria-selected="true">Tümü</button>
            <button type="button" class="dh-sort__tab" role="tab" aria-selected="false">Son 1 Saat</button>
            <button type="button" class="dh-sort__tab" role="tab" aria-selected="false">Bugün</button>
            <button type="button" class="dh-sort__tab" role="tab" aria-selected="false">Dün</button>
          </div>
          <span class="dh-astro__stamp"><i class="fas fa-clock" aria-hidden="true"></i> En yeni en üstte</span>
        </div>

        <ol class="dh-live__feed">
          <li class="dh-live__day"><span>Bugün · 21 Ağustos 2026</span></li>
          <li class="dh-live__item is-now">
            <time class="dh-live__time" datetime="2026-08-21T09:47">09:47</time>
            <div class="dh-live__body">
              <div class="dh-live__meta">
                <span class="dh-live__cat">EKONOMİ</span>
                <span class="dh-live__now"><span class="dh-live__pulse" aria-hidden="true"></span> Şu an</span>
              </div>
              <h3 class="dh-live__title"><a href="haber-detay.html">Faiz kararının ardından kur ve borsada ilk hareket</a></h3>
              <p class="dh-live__sum">Endeksin açılışta yükselişe geçtiği, bankacılık hisselerinin öne çıktığı görüldü.</p>
            </div>
          </li>
          <li class="dh-live__item">
            <time class="dh-live__time" datetime="2026-08-21T09:42">09:42</time>
            <div class="dh-live__body">
              <div class="dh-live__meta"><span class="dh-live__cat">GÜNDEM</span></div>
              <h3 class="dh-live__title"><a href="haber-detay.html">Genel Kurul'da üç bakanlığın bütçesi görüşülüyor</a></h3>
              <p class="dh-live__sum">Oturumun gün boyu süreceği, akşam saatlerinde oylamaya geçileceği bildirildi.</p>
            </div>
          </li>
          <li class="dh-live__item">
            <time class="dh-live__time" datetime="2026-08-21T09:30">09:30</time>
            <div class="dh-live__body">
              <div class="dh-live__meta"><span class="dh-live__cat">AFET</span></div>
              <h3 class="dh-live__title"><a href="haber-detay.html">Bartın ve Kastamonu'da eğitime bir gün ara verildi</a></h3>
              <p class="dh-live__sum">Valilik açıklamasında kararın kuvvetli yağış beklentisiyle alındığı belirtildi.</p>
            </div>
          </li>
          <li class="dh-live__item">
            <time class="dh-live__time" datetime="2026-08-21T09:05">09:05</time>
            <div class="dh-live__body">
              <div class="dh-live__meta"><span class="dh-live__cat">DÜNYA</span></div>
              <h3 class="dh-live__title"><a href="haber-detay.html">Ege'de arama kurtarma tatbikatı başladı</a></h3>
              <p class="dh-live__sum">İki gün sürecek tatbikata deniz ve hava unsurlarının katıldığı belirtildi.</p>
            </div>
          </li>
          <li class="dh-live__item">
            <time class="dh-live__time" datetime="2026-08-21T08:36">08:36</time>
            <div class="dh-live__body">
              <div class="dh-live__meta"><span class="dh-live__cat">ULAŞIM</span></div>
              <h3 class="dh-live__title"><a href="haber-detay.html">Marmaray seferleri normale döndü</a></h3>
              <p class="dh-live__sum">Sabah yoğunluğunda yaşanan 12 dakikalık gecikmenin telafi edildiği açıklandı.</p>
            </div>
          </li>
          <li class="dh-live__day"><span>Dün · 20 Ağustos 2026</span></li>
          <li class="dh-live__item">
            <time class="dh-live__time" datetime="2026-08-20T22:15">22:15</time>
            <div class="dh-live__body">
              <div class="dh-live__meta"><span class="dh-live__cat">SPOR</span></div>
              <h3 class="dh-live__title"><a href="haber-detay.html">Avrupa kupalarında temsilcimiz turu geçti</a></h3>
              <p class="dh-live__sum">Rövanşta alınan sonucun ardından kura çekimi cuma günü yapılacak.</p>
            </div>
          </li>
          <li class="dh-live__item">
            <time class="dh-live__time" datetime="2026-08-20T20:40">20:40</time>
            <div class="dh-live__body">
              <div class="dh-live__meta"><span class="dh-live__cat">TEKNOLOJİ</span></div>
              <h3 class="dh-live__title"><a href="haber-detay.html">Yerli haberleşme uydusunda entegrasyon tamamlandı</a></h3>
              <p class="dh-live__sum">Fırlatma takviminin yıl sonunda açıklanacağı bildirildi.</p>
            </div>
          </li>
        </ol>

        <div class="dh-nwmore">
          <a class="dh-nwmore__btn" href="son-dakika.html">Akışın tamamını aç <i class="fas fa-arrow-right" aria-hidden="true"></i></a>
        </div>
      </div>"""

GOVDE["bugun"] = """      <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-bugun-t">Bugün Ne Oldu?</h2>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-calendar-day" aria-hidden="true"></i> 21 Ağustos 2026 Cuma</span>
            <a href="dada-ozet.html" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Tümünü Gör</a>
          </div>
        </div>
        <p class="dh-nwintro">Günün buraya kadarki beş başlığı. Her madde bir dakikadan kısa okunur; ayrıntı için başlığa gidin.</p>
        <ol class="dh-nwlist dh-nwlist--ozet">
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">1</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Politika faizi 150 baz puan indirildi</a></h3>
              <p class="dh-nwlist__sum">Karar beklentilerin bir miktar üzerinde geldi; metinde sıkı duruşun süreceği vurgulandı.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-21T09:47">09:47</time> · EKONOMİ</span>
            </div>
          </li>
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">2</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Bütçe görüşmelerinde ikinci gün başladı</a></h3>
              <p class="dh-nwlist__sum">Üç bakanlığın bütçesi ele alınıyor; oylamanın akşam yapılması bekleniyor.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-21T09:42">09:42</time> · GÜNDEM</span>
            </div>
          </li>
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">3</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Altı il için turuncu kodlu sağanak uyarısı</a></h3>
              <p class="dh-nwlist__sum">İki ilde okullar tatil edildi; kara yollarında ekipler teyakkuza geçirildi.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-21T09:30">09:30</time> · AFET</span>
            </div>
          </li>
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">4</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Brüksel'de iki günlük diplomasi trafiği</a></h3>
              <p class="dh-nwlist__sum">Gümrük birliğinin güncellenmesi ve vize başlıkları masada.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-21T08:58">08:58</time> · DÜNYA</span>
            </div>
          </li>
          <li class="dh-nwlist__item">
            <span class="dh-nwlist__num">5</span>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">YKS ek yerleştirme takvimi açıklandı</a></h3>
              <p class="dh-nwlist__sum">Başvurular 1 Eylül'de başlıyor, sonuçlar ayın ortasında ilan edilecek.</p>
              <span class="dh-nwlist__note"><time datetime="2026-08-21T07:14">07:14</time> · EĞİTİM</span>
            </div>
          </li>
        </ol>
      </div>"""

GOVDE["takvim"] = """      <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-takvim-t">Gündem Takvimi</h2>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-forward" aria-hidden="true"></i> Bugünden ileriye</span>
            <a href="hesabim.html#bildirimler" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Hatırlat</a>
          </div>
        </div>
        <p class="dh-nwintro">Takvimde beklenen gelişmeler var: açıklanacak veriler, başlayacak duruşmalar, oynanacak maçlar. Saatler yerel saattir.</p>
        <ol class="dh-nwlist dh-nwlist--cal">
          <li class="dh-nwlist__day"><span>Bugün · 21 Ağustos Cuma</span></li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-21T14:00">14:00</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Hazine iç borçlanma ihalesi sonuçları</a></h3>
              <p class="dh-nwlist__sum">İki ihalenin ortalama bileşik faizi açıklanacak.</p>
            </div>
            <span class="dh-nwlist__tag">EKONOMİ</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-21T20:00">20:00</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Genel Kurul'da bütçe oylaması</a></h3>
              <p class="dh-nwlist__sum">Üç bakanlık bütçesinin oylanması bekleniyor.</p>
            </div>
            <span class="dh-nwlist__tag">GÜNDEM</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-21T23:59">23:59</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Yaz transfer dönemi kapanıyor</a></h3>
              <p class="dh-nwlist__sum">Tescil işlemleri için son saat; kulüplerin listeleri gece yayımlanacak.</p>
            </div>
            <span class="dh-nwlist__tag">SPOR</span>
          </li>
          <li class="dh-nwlist__day"><span>Yarın · 22 Ağustos Cumartesi</span></li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-22T10:00">10:00</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Süper Lig 3. hafta programı başlıyor</a></h3>
              <p class="dh-nwlist__sum">Hafta sonu dokuz maç oynanacak; canlı skor sayfası açık olacak.</p>
            </div>
            <span class="dh-nwlist__tag">SPOR</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-22T15:00">15:00</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">İstanbul'da toplu ulaşım zam toplantısı</a></h3>
              <p class="dh-nwlist__sum">Ulaşım koordinasyon merkezinin gündeminde tarife maddesi var.</p>
            </div>
            <span class="dh-nwlist__tag">YEREL</span>
          </li>
          <li class="dh-nwlist__day"><span>24 Ağustos Pazartesi</span></li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-24T10:00">10:00</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">TÜİK tüketici güven endeksi</a></h3>
              <p class="dh-nwlist__sum">Ağustos ayı verisi açıklanacak.</p>
            </div>
            <span class="dh-nwlist__tag">EKONOMİ</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-24T14:00">14:00</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Yeni eğitim yılı hazırlık toplantısı</a></h3>
              <p class="dh-nwlist__sum">Bakanlık il müdürleriyle takvim ve kayıt sürecini görüşecek.</p>
            </div>
            <span class="dh-nwlist__tag">EĞİTİM</span>
          </li>
          <li class="dh-nwlist__day"><span>26 Ağustos Çarşamba</span></li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-26T11:00">11:00</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Avrupa kupalarında kura çekimi</a></h3>
              <p class="dh-nwlist__sum">Grup aşaması eşleşmeleri belli olacak.</p>
            </div>
            <span class="dh-nwlist__tag">SPOR</span>
          </li>
          <li class="dh-nwlist__day"><span>30 Ağustos Pazar</span></li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-30T09:00">09:00</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">30 Ağustos Zafer Bayramı törenleri</a></h3>
              <p class="dh-nwlist__sum">Ankara ve Afyonkarahisar'daki törenler canlı yayımlanacak.</p>
            </div>
            <span class="dh-nwlist__tag">GÜNDEM</span>
          </li>
        </ol>
      </div>"""

GOVDE["guncellenen"] = """      <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-guncellenen-t">Güncellenen Haberler</h2>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-clock-rotate-left" aria-hidden="true"></i> Son 24 saat</span>
            <a href="arsiv.html" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Tümünü Gör</a>
          </div>
        </div>
        <p class="dh-nwintro">Yayımlandıktan sonra yeni bilgiyle güncellenen haberler. Her satırda son güncelleme saati ve kaçıncı güncelleme olduğu yazar.</p>
        <ul class="dh-nwlist dh-nwlist--upd">
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-21T09:51">09:51</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Faiz kararı: karar metninin tam çevirisi eklendi</a></h3>
              <span class="dh-nwlist__note">Son güncelleme <time datetime="2026-08-21T09:51">09:51</time> · 4. güncelleme · yayım <time datetime="2026-08-21T09:47">09:47</time></span>
            </div>
            <span class="dh-nwlist__tag">EKONOMİ</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-21T09:34">09:34</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Sağanak uyarısı: tatil edilen iller listesi genişledi</a></h3>
              <span class="dh-nwlist__note">Son güncelleme <time datetime="2026-08-21T09:34">09:34</time> · 3. güncelleme · yayım <time datetime="2026-08-21T08:20">08:20</time></span>
            </div>
            <span class="dh-nwlist__tag">AFET</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-21T08:47">08:47</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Marmaray arızası: sefer sayıları ve gecikme süresi düzeltildi</a></h3>
              <span class="dh-nwlist__note">Son güncelleme <time datetime="2026-08-21T08:47">08:47</time> · 2. güncelleme · düzeltme notu var</span>
            </div>
            <span class="dh-nwlist__tag">ULAŞIM</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-21T08:05">08:05</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Brüksel temasları: görüşme başlıkları teyit edildi</a></h3>
              <span class="dh-nwlist__note">Son güncelleme <time datetime="2026-08-21T08:05">08:05</time> · 1. güncelleme · yayım <time datetime="2026-08-21T07:58">07:58</time></span>
            </div>
            <span class="dh-nwlist__tag">DÜNYA</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-20T23:20">23:20</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Avrupa kupası maçı: maç sonu açıklamaları eklendi</a></h3>
              <span class="dh-nwlist__note">Son güncelleme <time datetime="2026-08-20T23:20">23:20</time> · 5. güncelleme · yayım <time datetime="2026-08-20T20:00">20:00</time></span>
            </div>
            <span class="dh-nwlist__tag">SPOR</span>
          </li>
          <li class="dh-nwlist__item">
            <time class="dh-nwlist__time" datetime="2026-08-20T21:10">21:10</time>
            <div class="dh-nwlist__body">
              <h3 class="dh-nwlist__title"><a href="haber-detay.html">Uydu projesi: fırlatma takvimi ifadesi netleştirildi</a></h3>
              <span class="dh-nwlist__note">Son güncelleme <time datetime="2026-08-20T21:10">21:10</time> · 2. güncelleme · düzeltme notu var</span>
            </div>
            <span class="dh-nwlist__tag">TEKNOLOJİ</span>
          </li>
        </ul>
      </div>"""

GOVDE["afet"] = """      <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-afet-t">Afet ve Acil Durum</h2>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-rotate" aria-hidden="true"></i> <time datetime="2026-08-21T09:40">09:40</time> güncellendi</span>
            <a href="veri-harita.html#afet" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Afet Haritası</a>
          </div>
        </div>
        <div class="dh-nwstat">
          <ul class="dh-nwstat__rows">
            <li class="dh-nwstat__row" data-lv="kritik">
              <span class="dh-nwstat__ic" aria-hidden="true"><i class="fas fa-cloud-showers-heavy"></i></span>
              <span class="dh-nwstat__body">
                <b class="dh-nwstat__name">Kuvvetli sağanak — Batı Karadeniz</b>
                <span class="dh-nwstat__desc">Bartın, Kastamonu, Sinop, Zonguldak, Karabük, Düzce. Öğleden sonra şiddetlenmesi bekleniyor.</span>
              </span>
              <span class="dh-nwstat__lv">TURUNCU KOD</span>
            </li>
            <li class="dh-nwstat__row" data-lv="uyari">
              <span class="dh-nwstat__ic" aria-hidden="true"><i class="fas fa-fire"></i></span>
              <span class="dh-nwstat__body">
                <b class="dh-nwstat__name">Orman yangını riski — Akdeniz kıyı şeridi</b>
                <span class="dh-nwstat__desc">Antalya ve Muğla'da rüzgâr hızı 45 km/s. Ormanlık alanlara giriş sınırlı.</span>
              </span>
              <span class="dh-nwstat__lv">YÜKSEK RİSK</span>
            </li>
            <li class="dh-nwstat__row" data-lv="dikkat">
              <span class="dh-nwstat__ic" aria-hidden="true"><i class="fas fa-wave-square"></i></span>
              <span class="dh-nwstat__body">
                <b class="dh-nwstat__name">Son 24 saatte hissedilen deprem</b>
                <span class="dh-nwstat__desc">En büyüğü 3,8 — Ege Denizi açıkları, 06:12. Hasar ihbarı bulunmuyor.</span>
              </span>
              <span class="dh-nwstat__lv">İZLENİYOR</span>
            </li>
            <li class="dh-nwstat__row" data-lv="ok">
              <span class="dh-nwstat__ic" aria-hidden="true"><i class="fas fa-water"></i></span>
              <span class="dh-nwstat__body">
                <b class="dh-nwstat__name">Barajlar ve taşkın durumu</b>
                <span class="dh-nwstat__desc">Taşkın uyarısı verilen havza yok. Doluluk oranları mevsim normalinde.</span>
              </span>
              <span class="dh-nwstat__lv">NORMAL</span>
            </li>
          </ul>
          <div class="dh-nwacil">
            <span class="dh-nwacil__head">Acil çağrı</span>
            <ul class="dh-nwacil__list">
              <li class="dh-nwacil__it"><b class="dh-nwacil__num">112</b><span class="dh-nwacil__ad">Acil Çağrı Merkezi</span></li>
              <li class="dh-nwacil__it"><b class="dh-nwacil__num">122</b><span class="dh-nwacil__ad">AFAD</span></li>
              <li class="dh-nwacil__it"><b class="dh-nwacil__num">177</b><span class="dh-nwacil__ad">Orman Yangını İhbar</span></li>
              <li class="dh-nwacil__it"><b class="dh-nwacil__num">168</b><span class="dh-nwacil__ad">Alo Kaymakam</span></li>
            </ul>
            <p class="dh-nwacil__note">Bu sayfa resmî bir uyarı kanalı değildir. Afet anında AFAD ve valilik duyurularını esas alın.</p>
          </div>
        </div>
      </div>"""

GOVDE["trafik"] = """      <div class="container max-w-xl">
        <div class="section-header panel dh-secbar">
          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-trafik-t">Trafik ve Ulaşım</h2>
          <div class="dh-secbar__tools">
            <span class="dh-nwstamp"><i class="fas fa-map-marker-alt" aria-hidden="true"></i> <span data-dh-trafik-kapsam></span></span>
            <a href="veri-harita.html" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Şehir Verileri</a>
          </div>
        </div>
        <div class="dh-trf" data-dh-trafik>
          <div class="dh-trf__cips" role="radiogroup" aria-label="Şehir seçimi">
            <button type="button" class="dh-trf__cip" role="radio" aria-checked="false" data-dh-trafik-sec="istanbul">İstanbul</button>
            <button type="button" class="dh-trf__cip" role="radio" aria-checked="false" data-dh-trafik-sec="ankara">Ankara</button>
            <button type="button" class="dh-trf__cip" role="radio" aria-checked="false" data-dh-trafik-sec="izmir">İzmir</button>
            <button type="button" class="dh-trf__cip" role="radio" aria-checked="false" data-dh-trafik-sec="bursa">Bursa</button>
            <button type="button" class="dh-trf__cip" role="radio" aria-checked="false" data-dh-trafik-sec="antalya">Antalya</button>
            <button type="button" class="dh-trf__cip" role="radio" aria-checked="false" data-dh-trafik-sec="adana">Adana</button>
            <button type="button" class="dh-trf__cip" role="radio" aria-checked="false" data-dh-trafik-sec="konya">Konya</button>
            <button type="button" class="dh-trf__cip" role="radio" aria-checked="false" data-dh-trafik-sec="gaziantep">Gaziantep</button>
            <button type="button" class="dh-trf__cip" role="radio" aria-checked="false" data-dh-trafik-sec="trabzon">Trabzon</button>
            <button type="button" class="dh-trf__cip" role="radio" aria-checked="false" data-dh-trafik-sec="samsun">Samsun</button>
          </div>
          <div class="dh-trf__ust">
            <div class="dh-trf__id">
              <h3 class="dh-trf__ad" data-dh-trafik-ad>İstanbul</h3>
              <button type="button" class="dh-trf__kaydet" data-dh-trafik-kaydet>Şehrim yap</button>
            </div>
            <div class="dh-trf__olcu">
              <span class="dh-trf__lbl">Trafik yoğunluğu</span>
              <div class="dh-trf__bar" data-lv="normal"><span data-dh-trafik-bar></span></div>
              <b class="dh-trf__yuzde" data-dh-trafik-yogunluk>%0</b>
            </div>
            <p class="dh-trf__sik"><i class="fas fa-triangle-exclamation" aria-hidden="true"></i> En sıkışık güzergâh: <b data-dh-trafik-sikisik></b></p>
          </div>
          <div class="dh-nwstat dh-nwstat--trafik">
            <ul class="dh-nwstat__rows" data-dh-trafik-satirlar aria-live="polite"></ul>
          </div>
          <p class="dh-trf__not"><i class="fas fa-circle-info" aria-hidden="true"></i> Değerler prototip için üretilmiştir; gerçek ölçüm değildir. Resmî bilgi için ilgili belediye ve karayolları duyurularını esas alın.</p>
        </div>
      </div>"""



# ------------------------------------------------------ sayfa <head> açıklaması
ACIKLAMA = {
    "canli": "Takibi süren başlıklar ve gelişme sayılarıyla Dada Haber canlı gündem sayfası.",
    "dakika": "Günün gelişmeleri dakika dakika tek akışta; en yeni madde en üstte.",
    "bugun": "Günün buraya kadarki başlıkları numaralı özet hâlinde.",
    "takvim": "Bugünden ileriye beklenen gelişmeler: veriler, duruşmalar, maçlar, törenler.",
    "guncellenen": "Yayımlandıktan sonra yeni bilgiyle güncellenen haberler ve düzeltme notları.",
    "afet": "Afet ve acil durum uyarı seviyeleri, son depremler ve acil çağrı numaraları.",
    "trafik": "İstanbul ve şehirlerarası yol, raylı sistem, deniz ve hava ulaşımında son durum.",
}


# ------------------------------------------------------------------- yardımcı
def govde_yuvasi(s):
    m = re.search(r"[ \t]*<!-- ={10,} SAYFA GÖVDESİ BURAYA ={10,}.*?={10,} -->\n", s, re.S)
    if not m:
        sys.exit("HATA: şablonda gövde yuvası bulunamadı")
    return m


def dengeli(s, i, etiket):
    """i: açılış etiketinin başlangıcı. Dengeli kapanıştan SONRAKİ indisi verir."""
    n = 0
    for m in re.finditer(r"<%s\b|</%s>" % (etiket, etiket), s[i:]):
        if m.group(0).startswith("</"):
            n -= 1
            if n == 0:
                return i + m.end()
        else:
            n += 1
    sys.exit("HATA: <%s> kapanmıyor" % etiket)


def satir_basi(s, i):
    j = s.rfind("\n", 0, i)
    return j + 1 if j != -1 else 0


# ------------------------------------------------------------------- banner
def banner(k):
    """anlik.html'deki .dh-lb bloğunun kalıbı. Değişen: breadcrumb, lead, h1
    ve slaytlar. Perde slaytın kendi katmanında (article::after) — kardeş
    katman yapılırsa Swiper transform'u metnin üstünü örter (iki kez yaşandı)."""
    ad, d = AD[k], SAYFA[k]
    o = []
    w = o.append
    w('    <!-- Sayfa başlığı bandı -->\n')
    w('    <div class="block-slider block-slider-miniposts panel swiper-parent uc-dark dh-lb dh-lb--v2" data-cat="anlik">\n')
    w('      <div class="dh-lb__veil" aria-hidden="true"></div>\n')
    w('      <div class="swiper-main swiper"\n')
    w('        data-uc-swiper="items: 1; autoplay: 6000; active: 1; gap: 0; disable-class: opacity-30; '
      'effect: fade; fade: true; next: .dh-lb__nav .swiper-next; prev: .dh-lb__nav .swiper-prev;">\n')
    w('        <div class="swiper-wrapper">\n')
    for gorsel, baslik, saat, sayi in d["slayt"]:
        w('          <div class="swiper-slide">\n')
        w('            <article class="post type-post">\n')
        w('              <div class="featured-image bg-gray-25 dark:bg-gray-800">\n')
        w('                <canvas class="min-h-300px lg:min-h-500px"></canvas>\n')
        w('                <img class="media-cover image" src="./assets/images/common/img-fallback.png"\n')
        w('                  data-src="./assets/images/main/posts/%s" alt="%s" data-uc-img="loading: lazy">\n'
          % (gorsel, baslik))
        w('              </div>\n')
        w('              <div class="d-block position-cover z-1" aria-hidden="true"></div>\n')
        w('              <div class="panel max-w-xl mx-auto px-2 z-3">\n')
        w('                <div class="post-header panel position-absolute bottom-0 vstack justify-between '
          'gap-2 xl:gap-4 max-w-600px mb-4 xl:mb-8">\n')
        w('                  <div class="post-top hstack gap-narrow">\n')
        w('                    <div class="post-category hstack gap-narrow fs-7 fw-bold h-24px px-1 '
          'rounded-1 shadow-xs bg-primary text-gray-900">\n')
        w('                      <a class="text-none text-gray-900" href="%s">%s</a>\n' % (HEDEF[k], ad))
        w('                    </div>\n')
        w('                  </div>\n')
        w('                  <h3 class="post-title h4 lg:h3 xl:h2 m-0 text-truncate-2" data-swiper-parallax="-48">\n')
        w('                    <a class="text-none" href="haber-detay.html">%s</a>\n' % baslik)
        w('                  </h3>\n')
        w('                  <div class="post-meta panel justify-content-start align-items-start gap-1 fs-7 '
          'ft-tertiary fw-medium text-uppercase text-white text-opacity-60 d-flex z-1">\n')
        w('                    <span class="text-gray-50"><i class="fas fa-bolt"></i> %s güncellendi</span>\n' % saat)
        w('                    <div class="sep text-white">·</div>\n')
        w('                    <span class="text-gray-50"><i class="fas fa-eye"></i> '
          '<span class="minimizeNumber">%d</span></span>\n' % sayi)
        w('                  </div>\n')
        w('                </div>\n')
        w('              </div>\n')
        w('            </article>\n')
        w('          </div>\n')
    w('        </div>\n')
    w('        <div class="dh-lb__top">\n')
    w('          <div class="container max-w-xl dh-lb__topinner">\n')
    w('            <nav class="dh-art-crumb dh-lb__crumb" aria-label="Sayfa yolu">'
      '<a href="index.html" aria-label="Anasayfa"><i class="fas fa-home-lg-alt" aria-hidden="true"></i></a>'
      '<i class="fas fa-chevron-right" aria-hidden="true"></i>'
      '<a href="anlik.html">Anlık</a>'
      '<i class="fas fa-chevron-right" aria-hidden="true"></i>'
      '<span aria-current="page">%s</span></nav>\n' % ad)
    w('            <p class="dh-lb__lead">%s</p>\n' % d["lead"])
    w('            <h1 class="dh-lb__title">%s</h1>\n' % ad)
    w('            <span class="dh-lb__rule" aria-hidden="true"></span>\n')
    w('            <div class="dh-lb__nav">\n')
    w('              <div class="swiper-nav swiper-prev" role="button" aria-label="Önceki">'
      '<i class="unicon-chevron-left icon-1"></i></div>\n')
    w('              <div class="swiper-nav swiper-next" role="button" aria-label="Sonraki">'
      '<i class="unicon-chevron-right icon-1"></i></div>\n')
    w('            </div>\n')
    w('          </div>\n')
    w('        </div>\n')
    w('      </div>\n')
    w('    </div>\n')
    return "".join(o)


# --------------------------------------------------------- alt kategori şeridi
def serit(aktif):
    """Anlık'ın alt sayfaları çip olarak. aktif=None → anlik.html'in kendisi.

    Şeritte AÇIKLAMA ETİKETİ YOK ("alt kategorileri" gibi) — yalnız isimler.
    Kök, bulunulan sayfa Anlık ise aria-current, değilse anlik.html bağlantısı."""
    o = []
    w = o.append
    w('    <!-- Alt kategori şeridi: Anlık bölümleri -->\n')
    w('    <nav class="section panel dh-catbar" data-cat="anlik" aria-label="Anlık bölümleri">\n')
    w('      <div class="container max-w-xl">\n')
    w('        <div class="dh-catbar__row">\n')
    if aktif is None:
        w('          <span class="dh-catbar__root">'
          '<span class="dh-catbar__root-ad" aria-current="page">ANLIK</span></span>\n')
    else:
        w('          <span class="dh-catbar__root dh-catbar__root--link">'
          '<a class="dh-catbar__root-ad" href="anlik.html">ANLIK</a></span>\n')
    w('          <div class="dh-catbar__inner swiper-parent">\n')
    w('            <div class="swiper dh-catbar__swiper"\n')
    w('              data-uc-swiper="items: auto; gap: 8; free: true; grab-cursor: true; '
      'next: .dh-catbar__nav--next; prev: .dh-catbar__nav--prev; disable-class: is-off; watchOverflow: true;">\n')
    w('              <div class="swiper-wrapper">\n')
    for k, ad, hedef, ikon, aciklama in ALT:
        ek = ' is-on' if k == aktif else ''
        cur = ' aria-current="page"' if k == aktif else ''
        w('                <div class="swiper-slide"><a class="dh-catbar__chip%s" href="%s"%s>%s</a></div>\n'
          % (ek, hedef, cur, ad))
    w('              </div>\n')
    w('            </div>\n')
    w('            <div class="dh-catbar__nav dh-catbar__nav--prev" role="button" aria-label="Önceki bölümler">'
      '<i class="unicon-chevron-left"></i></div>\n')
    w('            <div class="dh-catbar__nav dh-catbar__nav--next" role="button" aria-label="Sonraki bölümler">'
      '<i class="unicon-chevron-right"></i></div>\n')
    w('          </div>\n')
    w('        </div>\n')
    w('      </div>\n')
    w('    </nav>\n')
    return "".join(o)


# ------------------------------------------------- sayfa sonu: kardeş sayfalar
def digerleri(aktif):
    """Sayfanın sonunda Anlık'ın diğer bölümlerine giden ızgara. Şerit yukarıda
    yatay ve kayan; burada tam liste tek bakışta görünür."""
    o = []
    w = o.append
    w('    <section class="section panel pt-5 lg:pt-6 pb-5 lg:pb-7" aria-labelledby="dh-nwgo-t">\n')
    w('      <div class="container max-w-xl">\n')
    w('        <div class="section-header panel dh-secbar">\n')
    w('          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-nwgo-t">'
      'Anlık&#39;ın Diğer Bölümleri</h2>\n')
    w('          <div class="dh-secbar__tools">\n')
    w('            <a href="anlik.html" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">'
      'Anlık Merkezi</a>\n')
    w('          </div>\n')
    w('        </div>\n')
    w('        <div class="dh-nwgo">\n')
    for k, ad, hedef, ikon, aciklama in ALT:
        if k == aktif:
            continue
        w('          <a class="dh-nwgo__it" href="%s">\n' % hedef)
        w('            <span class="dh-nwgo__ic" aria-hidden="true"><i class="fas %s"></i></span>\n' % ikon)
        w('            <span class="dh-nwgo__body"><b class="dh-nwgo__t">%s</b>'
          '<span class="dh-nwgo__d">%s</span></span>\n' % (ad, aciklama))
        w('            <i class="fas fa-arrow-right dh-nwgo__go" aria-hidden="true"></i>\n')
        w('          </a>\n')
    w('        </div>\n')
    w('      </div>\n')
    w('    </section>\n')
    return "".join(o)


# ------------------------------------------ anlik.html'de kalan kompakt özet
def ozet(k):
    """Taşınan bölümün merkez sayfadaki yerine geçen kart. İçerik yeni sayfada;
    burada başlık, üç satırlık önizleme ve 'Tümünü Gör' kalır."""
    ad = AD[k]
    ikon, damga = DAMGA[k]
    o = []
    w = o.append
    w('    <section class="section panel pt-5 lg:pt-6 pb-0" id="%s" aria-labelledby="%s">\n'
      % (k, SAYFA[k]["etiket"]))
    w('      <div class="container max-w-xl">\n')
    w('        <div class="section-header panel dh-secbar">\n')
    w('          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="%s">%s</h2>\n'
      % (SAYFA[k]["etiket"], ad))
    w('          <div class="dh-secbar__tools">\n')
    w('            <span class="dh-nwstamp"><i class="fas %s" aria-hidden="true"></i> %s</span>\n'
      % (ikon, damga))
    w('            <a href="%s" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">'
      'Tümünü Gör</a>\n' % HEDEF[k])
    w('          </div>\n')
    w('        </div>\n')
    w('        <a class="dh-nwsum" href="%s">\n' % HEDEF[k])
    w('          <span class="dh-nwsum__ic" aria-hidden="true"><i class="fas %s"></i></span>\n' % IKON[k])
    w('          <span class="dh-nwsum__body">\n')
    # Başlık zaten bölüm çubuğunda (h2); kartta tekrarlanmaz.
    w('            <span class="dh-nwsum__d">%s</span>\n' % ACIK[k])
    w('            <span class="dh-nwsum__peek">\n')
    for satir in ONIZLEME[k]:
        w('              <span>%s</span>\n' % satir)
    w('            </span>\n')
    w('          </span>\n')
    w('          <span class="dh-nwsum__go">Tümünü Gör <i class="fas fa-arrow-right" aria-hidden="true"></i></span>\n')
    w('        </a>\n')
    w('      </div>\n')
    w('    </section>\n')
    return "".join(o)


# ------------------------------------------------------------------ üretim
sablon = open(SABLON, encoding="utf-8").read()
yazilan = []

for k in URETILEN:
    ad, dosya = AD[k], HEDEF[k]
    s = sablon
    s = s.replace("<title>SAYFA BAŞLIĞI — Dada Haber</title>",
                  "<title>%s — Dada Haber</title>" % ad, 1)
    s = s.replace('<meta name="description" content="">',
                  '<meta name="description" content="%s">' % ACIKLAMA[k], 1)
    if 'data-dh-cat=""' in s:
        s = s.replace('data-dh-cat=""', 'data-dh-cat="anlik"', 1)
    else:
        s = re.sub(r"<body\s", '<body data-dh-cat="anlik" ', s, count=1)

    govde = (banner(k) + "\n" + serit(aktif=k) + "\n"
             + '    <section class="%s" id="%s" aria-labelledby="%s">\n' % (SAYFA[k]["sinif"], k, SAYFA[k]["etiket"])
             + GOVDE[k] + "\n    </section>\n\n"
             + EK[k] + "\n" + digerleri(aktif=k))

    m = govde_yuvasi(s)
    s = s[:m.start()] + govde + s[m.end():]

    # kayan ray yalnız Canlı Gündem sayfasında var
    if 'data-dh-track-' in govde and "js/dh-track.js" not in s:
        s = s.replace('    <script defer src="./assets/js/v2/dh-v2-nav.js"></script>',
                      '    <script defer src="./assets/js/v2/dh-v2-nav.js"></script>\n'
                      '    <script defer src="./assets/js/dh-track.js"></script>', 1)

    open(dosya, "w", encoding="utf-8").write(s)
    yazilan.append(dosya)

# Şablon eski kabuğu taşıyor; kabuğu yay.py'nin kendi yerleştiricisiyle güncelle.
# Yalnız bu betiğin ürettiği sayfalara dokunulur, site geneline değil.
for dosya in yazilan:
    r, hata = yay.isle(dosya)
    if hata:
        sys.exit("HATA: %s — %s" % (dosya, hata))
    print("%s yazıldı (kabuk: %s)" % (dosya, ",".join(r) or "-"))


# ------------------------------------------------- merkez sayfa: anlik.html
a = open(MERKEZ, encoding="utf-8").read()

# 1) şerit — çapalar yerine yeni sayfalara
i = a.find('<nav class="section panel dh-catbar"')
if i == -1:
    sys.exit("HATA: anlik.html'de .dh-catbar yok")
b = satir_basi(a, i)
e = dengeli(a, i, "nav")
while e < len(a) and a[e] in " \t":
    e += 1
if e < len(a) and a[e] == "\n":
    e += 1
# şeridin hemen üstündeki yorum satırı varsa o da değişsin
onceki = satir_basi(a, b - 1)
if a[onceki:b].lstrip().startswith("<!--"):
    b = onceki
a = a[:b] + serit(aktif=None) + a[e:]

# 2) taşınan yedi bölüm → kompakt özet
for k in URETILEN:
    i = a.find('id="%s"' % k)
    if i == -1:
        sys.exit("HATA: anlik.html'de id=%s bölümü yok" % k)
    b = a.rfind("<section", 0, i)
    e = dengeli(a, b, "section")
    b = satir_basi(a, b)
    while e < len(a) and a[e] in " \t":
        e += 1
    if e < len(a) and a[e] == "\n":
        e += 1
    a = a[:b] + ozet(k) + a[e:]

open(MERKEZ, "w", encoding="utf-8").write(a)
print("%s güncellendi (%d bölüm özete indi)" % (MERKEZ, len(URETILEN)))
