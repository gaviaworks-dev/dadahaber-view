# Dada Haber v2 — Bilgi Mimarisi Sözleşmesi

Kaynak: `Dada_Haber_Nihai_Menu_Haritasi (1).docx` · Sürüm 1.0 · 19 Ağustos 2026.
Bu dosya v2'nin **tek doğruluk kaynağıdır.** Menü metni, sıra ve gruplama
burada yazandan sapmaz.

Marka söylemi: **"Gündemin net hâli."** — logonun altında/yanında durur.

---

## 0. v2 çalışma kuralları (v1'i bozmamak için)

v1, `main` içinde `/v1/` klasörüne **HTML kopyası** olarak konacak ve
`../assets/` üzerinden ortak varlık ağacını kullanacak. Bu yüzden:

| Kural | Neden |
|---|---|
| **`custom.min.css` DEĞİŞTİRİLMEZ.** Tüm v2 CSS'i `assets/css/theme/v2/<parça>.css` içine. | v1 kopyası aynı dosyayı yüklüyor; değişirse v1 donmuş olmaz. |
| **Mevcut `assets/js/dh-*.js` DEĞİŞTİRİLMEZ.** Yeni davranış `assets/js/v2/dh-<ad>.js`. | Aynı sebep. |
| **Mevcut görseller değiştirilmez/silinmez**, yalnız eklenir. | Aynı sebep. |
| Her yol `./` ile başlar. `../assets/` ve `/...` kök-mutlak **yasak.** | Pages `/dadahaber-view/` alt dizininden servis ediyor. |
| `demo-six.min.css` vendor, dokunulmaz. | R1'den beri geçerli. |
| `text-bg-primary` kullanılmaz (vendor'da bayat yeşil). | R1'den beri geçerli. |
| Yeni kütüphane eklenmez. Swiper + scroll-snap + vanilla JS. | R1'den beri geçerli. |
| Her sayfada `<meta name="robots" content="noindex, nofollow">`. | Prototip kapalı. |
| Site tamamen Türkçe. İngilizce yer tutucu bırakılmaz. | R1'den beri geçerli. |

**CSS parça dosyaları çakışmaz:** her ajan yalnız kendi parçasına yazar.
`v2.css` bunları `@import` ile toplar; yayından önce tek dosyaya düzleştirilir.

---

## 1. Üst bilgi bandı (siyah `.dh-shortcuts` bandının yerini alır)

Sol grup — hızlı erişim ve günlük servis:

| Etiket | Hedef |
|---|---|
| Son Dakika | `son-dakika.html` |
| Piyasalar | `finans.html` |
| Hava Durumu | `veri-harita.html#hava` |
| Şehrim | `hesabim.html#sehirlerim` |
| Bültenler | `hesabim.html#bultenler` |
| Podcast | `podcast.html` |
| Mobil Uygulama | `hesabim.html#uygulama` |

Sağ grup: sosyal hesaplar · karanlık mod · arama · **Giriş Yap / Hesabım**.

## 2. Ana header

Logo · global arama · bildirim merkezi · kaydedilenler · hesabım · mobil menü.
Logo altında **"Gündemin net hâli."**

## 3. Ana menü — 11 başlık, bu sırada

`Şimdi · Gündem · Dünya · Ekonomi · Teknoloji · Gelecek · Spor · Sağlık ·
Kültür & Yaşam · Video · Keşfet`

Masaüstü: mega menü. Mobil: aynı sıra, açılır akordiyon.

### Kategori kimlik renkleri (`.dh-lb[data-cat]` perdesi ve mega menü rayı)

| Kategori | data-cat | Renk |
|---|---|---|
| Şimdi | `simdi` | `#c8102e` |
| Gündem | `gundem` | `#1b2a4a` |
| Dünya | `dunya` | `#0d6b8a` |
| Ekonomi | `ekonomi` | `#2aa1a9` |
| Teknoloji | `teknoloji` | `#1c3df9` |
| Gelecek | `gelecek` | `#6a1bd1` |
| Spor | `spor` | `#19750a` |
| Sağlık | `saglik` | `#00c5e5` |
| Kültür & Yaşam | `kultur` | `#b3204d` |
| Video | `video` | `#0c1d49` |
| Keşfet | `kesfet` | kurumsal amber |

Eski `data-cat` değerleri (`kadin` `savunma` `oyun` `finans`) **durur**, o
sayfalar silinmez; yalnız menüde yeni ebeveynlerine bağlanır.

---

## 4. Mega menü içeriği (dokümandan birebir)

Her mega menü paneli şu iskeleti taşır:
`3px kimlik şeridi` + `kategori adı` + `dokümandaki tek cümlelik işlev` +
`gruplanmış bağlantı sütunları`.

### 4.1 Şimdi — "Günün anlık gelişmelerinin toplandığı canlı merkezdir."
Son Dakika `son-dakika.html` · Canlı Gündem `simdi.html#canli` ·
Canlı Yayın `video.html#canli` · Dakika Dakika `simdi.html#dakika` ·
Bugün Ne Oldu? `simdi.html#bugun` · Gündem Takvimi `simdi.html#takvim` ·
Güncellenen Haberler `simdi.html#guncellenen` · Afet ve Acil Durum `simdi.html#afet` ·
Trafik ve Ulaşım `simdi.html#trafik` · Hava Durumu `veri-harita.html#hava`

### 4.2 Gündem
**Temel kategoriler:** Siyaset · Türkiye · Toplum · Hukuk · Güvenlik · Eğitim · Çevre · Afet
**Yerel haberler:** Yerel Haberler · İstanbul · Ankara · İzmir · 81 İl
**Özgün içerikler:** Özel Haber · Araştırma · Gündem Analizi
Not: kullanıcı şehir seçebilmeli, seçim `Şehrim` alanına kaydedilebilmeli.

### 4.3 Dünya
**Bölgeler:** Avrupa · Orta Doğu · Amerika · Asya Pasifik · Afrika · Balkanlar · Kafkasya · Türk Dünyası
**Konular:** Diplomasi · Küresel Siyaset · Savaş ve Çatışmalar · Göç · Uluslararası Kuruluşlar · Dünya Analizi

### 4.4 Ekonomi
**Ekonomi ve finans:** Türkiye Ekonomisi · Dünya Ekonomisi · Piyasalar · Döviz · Altın · Borsa · Kripto Para · Bankacılık · Kişisel Finans
**Sektörler:** İş Dünyası · Şirketler · Girişimcilik · Çalışma Hayatı · Enerji · Tarım · Sanayi · Gayrimenkul · Otomotiv
**Derinlik:** Ekonomi Analizi
**Piyasalar Ekranı:** Döviz kurları · Altın fiyatları · Borsa endeksleri · Kripto paralar · Akaryakıt fiyatları · Faiz oranları · Ekonomik takvim · Günlük değişim grafikleri
Mevcut sayfa eşlemesi: Döviz `doviz.html` · Altın `altin.html` · Borsa `borsa.html` ·
Kripto `kripto.html` · Piyasalar Ekranı `finans.html` · detay `finans-detay.html`

### 4.5 Teknoloji
Yapay Zekâ · Bilim · Tüketici Teknolojileri · Mobil · İnternet · Sosyal Medya ·
Siber Güvenlik · Yazılım · Girişimler · Uzay · **Savunma Teknolojileri** `savunma.html` ·
**Oyun** `oyun.html` · E-Spor · Dijital Kültür · Teknoloji Rehberleri · Ürün İncelemeleri

### 4.6 Gelecek — genç kullanıcılar için temel farklılaştırıcı
**Eğitim ve kariyer:** Eğitim ve Sınavlar · Üniversiteler · Burslar · Staj İlanları · Kariyer · Meslekler · İş Fırsatları · Girişimcilik · Geleceğin Meslekleri · Yapay Zekâ ve Çalışma Hayatı
**Toplum ve gelecek:** İklim · Sürdürülebilirlik · Dijital Haklar · Gençlerin Gündemi · Barınma · Yurt ve Öğrenci Yaşamı
**Fırsatlar:** Değişim Programları · Proje ve Yarışmalar · Gönüllülük · Fırsatlar ve Başvurular

### 4.7 Spor
**Branşlar:** Futbol `futbol.html` · Süper Lig · Millî Takım · Avrupa Ligleri · Şampiyonlar Ligi · Basketbol `basketbol.html` · Voleybol `voleybol.html` · Motor Sporları `formula1.html` · Tenis · Atletizm · Olimpiyatlar · Geleneksel Sporlar · E-Spor
**Servisler:** Transfer · Puan Durumu `puan-durumu.html` · Fikstür `fikstur.html` · Canlı Skor
**İçerikler:** Spor Analizi · Spor Video
Not: hesapta takım seçimi → kişisel bildirim. `takim-*.html` sayfaları burada.

### 4.8 Sağlık
Sağlık Haberleri · Halk Sağlığı · Ruh Sağlığı · Beslenme · Sağlıklı Yaşam · Hastalıklar ·
**Anne ve Çocuk** `hamilelik.html` · **Kadın Sağlığı** `kadin.html` · Erkek Sağlığı ·
Spor Sağlığı · Tıp Teknolojileri · İlaç ve Tedaviler · Sağlık Politikaları ·
Uzman Görüşleri · Sağlık Rehberleri · Doğru Bilinen Yanlışlar
**Editoryal zorunluluk:** sağlık içeriklerinde uzmanlık, kaynak ve bilgilendirme uyarısı zorunlu.

### 4.9 Kültür & Yaşam
Kültür Sanat · Sinema · Dizi · Müzik · Kitap · Edebiyat · Tiyatro · Sergi · Etkinlik ·
Şehir Yaşamı · Seyahat · Gastronomi · Moda · Tasarım · Mimari · İnsan Hikâyeleri ·
Popüler Kültür · Sosyal Medya Gündemi · Hafta Sonu · Kültür Takvimi
Not: `astroloji.html` Popüler Kültür altında konumlanır (dokümanda ayrı madde yok, sayfa korunur).

### 4.10 Video
Dada 60 · Son Dakika Videoları · Açıklayıcı Videolar · Canlı Yayın · Röportajlar ·
Sokaktan · Haber Dosyaları · Belgeseller · Stüdyo Programları · Ekonomi Programları ·
Teknoloji Programları · Spor Programları · Kültür Programları · Video Serileri · Program Arşivi
Mevcut: `video-galeri.html` `video-kategori-detay.html` `video-detay.html`

### 4.11 Keşfet — Dada Haber'e özgü formatların merkezi
Dada Özet `dada-ozet.html` · Günün 5'i `kesfet.html#gunun5` · Dada Bağlam `dada-baglam.html` ·
Dada Doğrula `dada-dogrula.html` · Farklı Bakışlar `farkli-bakislar.html` ·
Bana Etkisi `kesfet.html#bana-etkisi` · Veri & Harita `veri-harita.html` ·
Grafik Haberler `infografik.html` · Dada'ya Sor `kesfet.html#dadaya-sor` ·
Sakin Akış `sakin-akis.html` · Podcast `podcast.html` · Haber Dosyaları `kesfet.html#dosyalar` ·
Röportajlar `kesfet.html#roportaj` · Yazarlar `yazar-liste.html` · Görüş `yazar-liste.html#gorus` ·
Editörün Seçimi `kesfet.html#editor` · Foto Galeri `foto-fokus.html` · Arşiv `arsiv.html`

---

## 5. Dada Haber özel modül sayfaları

### 5.1 `dada-ozet.html` — Dada Özet
Derinlik seçimi: **15 Saniyede · 1 Dakikada · Derinlemesine**
Koleksiyonlar: Günün Özetleri · Haftanın Özeti · Ekonomi Özeti · Spor Özeti · Teknoloji Özeti

### 5.2 `dada-dogrula.html` — Dada Doğrula
Şüpheli iddia, görsel ve videoların doğrulama merkezi.
Karar etiketleri: **Doğru · Yanlış · Kısmen Doğru · Bağlamdan Koparılmış · Manipülasyon · Yapay Zekâ İçeriği**
Bölümler: Güncel İddialar · Görsel Doğrulama · Video Doğrulama ·
Doğrulama Talebi Gönder (form) · Doğrulama Metodolojisi

### 5.3 `dada-baglam.html` — Dada Bağlam
Gündemdeki Konular · Zaman Çizelgeleri · Kim Kimdir? · Ne Anlama Geliyor? ·
Temel Kavramlar · Önceki Gelişmeler · Belge ve Kaynaklar · Soru ve Cevaplar

### 5.4 `farkli-bakislar.html` — Farklı Bakışlar
Türkiye Basını · Dünya Basını · **Ortaklaşan Gerçekler** · **Ayrışan Görüşler** ·
Uzman Yorumları · Kaynak Karşılaştırması

### 5.5 `veri-harita.html` — Veri & Harita
Seçim Haritaları · Ekonomi Grafikleri · Afet Haritaları · Hava Durumu · Şehir Verileri ·
Nüfus Verileri · Eğitim Verileri · Sağlık Verileri · Spor İstatistikleri · İnteraktif Dosyalar

### 5.6 `sakin-akis.html` — Sakin Akış
Günün En Önemli 5 Haberi · Olumlu Gelişmeler · Çözüm Odaklı Haberler ·
**Şiddet Görsellerini Gizle** (anahtar) · **Son Dakika Bildirimlerini Durdur** (anahtar) ·
Sabah Özeti · Akşam Özeti

### 5.7 `podcast.html` — mevcut sayfa, kategoriler güncellenir
Günlük Gündem · Haftanın Özeti · Ekonomi · Dünya · Teknoloji · Kültür Sanat · Spor ·
Röportaj · Podcast Serileri · Tüm Bölümler

---

## 6. Yazarlar ve Görüş (`yazar-liste.html`)
Tüm Yazarlar · Güncel Yazılar · Konuk Yazarlar · Uzman Görüşleri · Editoryal ·
Analiz · Perspektif · Dosya Yazıları · Yazar Arşivi
**Etiket standardı:** her görüş içeriğinde görünür **Görüş / Analiz / Yorum** etiketi.

---

## 7. Kullanıcı menüsü (`hesabim.html`)

**Hesabım:** Genel Bakış · Gündemim · Takip Ettiğim Konular · Takip Ettiğim Şehirler ·
Takımlarım · Takip Ettiğim Yazarlar · Kaydedilen Haberler · Okuma Geçmişi ·
İzleme Geçmişi · Podcast Listem · Bildirimler · Bültenler · Sakin Akış Ayarları ·
Görünüm Tercihleri · Karanlık Mod · Dil Tercihi · Profil Bilgileri · Güvenlik ·
Gizlilik ve Veriler · Oturumu Kapat

**Bildirim tercihleri:** Son Dakika · Gündem · Şehrim · Ekonomi · Teknoloji · Gelecek ·
Spor · Takım Bildirimleri · Sağlık · Kültür & Yaşam · Günün Özeti · **Sessiz Saatler**

---

## 8. Global arama (`arama.html`)
**Sonuç sekmeleri:** Tümü · Haberler · Videolar · Podcastler · Yazarlar · Konular ·
Şehirler · Doğrulamalar · Veri ve Haritalar
**Filtreler:** Tarih · Kategori · İçerik türü · Yazar · Şehir · Haber durumu · Okuma süresi

---

## 9. Haber detayı modülleri (`haber-detay.html`) — menüye girmez
15 Saniyede Özet · Neden Önemli? · Bana Etkisi · Bundan Sonra Ne Olacak? · Dada Bağlam ·
**Haber Karnesi** · Kaynaklar ve Belgeler · Sesli Dinle · Güncelleme Geçmişi ·
Düzeltme Notu · **Yapay Zekâ Kullanım Bilgisi** · Konuyu Takip Et · Editöre Sor ·
Eksik Bilgi Bildir · Doğrulama Talebi Gönder

---

## 10. Footer — 6 sütun

**Haberler:** Son Dakika · Gündem · Dünya · Ekonomi · Teknoloji · Gelecek · Spor · Sağlık · Kültür & Yaşam · Yerel Haberler
**Dada Formatları:** Dada 60 · Dada Özet · Günün 5'i · Dada Bağlam · Dada Doğrula · Farklı Bakışlar · Veri & Harita · Podcast · Sakin Akış
**Kurumsal:** Hakkımızda · Künye · Ekibimiz · Yayın İlkeleri · Editoryal Bağımsızlık · Şeffaflık Merkezi · Doğrulama Metodolojisi · Düzeltme Politikası · Yapay Zekâ Politikası · Reklam Politikası · Kariyer · İletişim
**Destek ve İletişim:** Bize Ulaşın · Haber İhbarı · Doğrulama Talebi · Hata Bildir · Öneri ve Şikâyet · İçerik Kaldırma Talebi · Reklam Ver · Sponsorluk · Basın İletişimi
**Yasal:** Kullanım Koşulları · Gizlilik Politikası · KVKK Aydınlatma Metni · Çerez Politikası · Telif Hakları · Topluluk Kuralları · Erişilebilirlik · Açık Rıza Yönetimi
**Dada Haber Kanalları:** Mobil Uygulamalar · Bültenler · WhatsApp Kanalı · YouTube · Instagram · X · Facebook · LinkedIn · TikTok · RSS

Mevcut kurumsal sayfa eşlemesi: Hakkımızda `hakkimizda.html` · Künye `kunye.html` ·
Yayın İlkeleri `yayin-ilkeleri.html` · Reklam `reklam.html` · İletişim `iletisim.html` ·
Kullanım Koşulları `kullanim-sartlari.html` · KVKK `kvkk.html` · Aydınlatma `aydinlatma-metni.html` ·
Çerezler `cerezler.html` · Resmî İlanlar `resmi-ilanlar.html`
Karşılığı olmayanlar `coming-soon.html`'e bağlanır — kırık bağlantı bırakılmaz.

---

## 11. Nihai kararlar (dokümanın 10. bölümü)
- **Gelecek** genç kullanıcının eğitim/kariyer/iklim/dijital yaşam ihtiyacını karşılar.
- **Keşfet** Dada'ya özgü anlatım formatlarını tek merkezde toplar.
- **Şimdi** canlı ve son dakika gündemini yönetir.
- **Kültür & Yaşam** yakın içerikleri birleştirerek ana menü kalabalığını azaltır.
- **Finans ayrı ana kategori değildir**, Ekonomi altındadır.
- **Yazarlar ve Görüş** haberden etiket ve sayfa yapısıyla ayrılır.
- **Neden Önemli / Bana Etkisi / Haber Karnesi** menü öğesi değil, haber detay modülüdür.
