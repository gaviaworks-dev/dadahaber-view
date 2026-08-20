# Dadahaber — Yayılım Fazı Brifingi (R6)

Ana sayfa (`index.html`), liste (`haber-liste.html`) ve detay (`haber-detay.html`)
tamamlandı ve `10197e2` ile commit edildi. **Bu üç sayfa referans kaynağıdır.**
Yayılım fazında kalan 52 sayfa aynı yapıya çekilir.

> Önce `docs/HANDOFF.md`'yi oku. Oradaki değişmez kurallar bu fazda da geçerli.

---

## 0. Değişmez kurallar (tekrar)

1. `assets/css/theme/demo-six.min.css` **vendor'dur, dokunulmaz.**
2. Tüm özel CSS `assets/css/theme/custom.min.css` içinde. **YALNIZCA
   `cat >> assets/css/theme/custom.min.css` ile dosyanın SONUNA ekle.**
   Write/Edit ile dosyanın tamamını yeniden YAZMA — bu fazda paralel
   çalışan başka ajanlar var, tam dosya yazımı onların bloklarını siler.
   (Bu hata iki kez yaşandı, iki blok kayboldu.)
3. **Yeni kütüphane eklenmez.** Swiper, native scroll-snap, vanilla JS yeter.
4. `text-bg-primary` utility'si KULLANILMAZ (bayat yeşil `RGBA(16,191,71)`).
5. Site tamamen **Türkçe**. İngilizce yer tutucu metin bırakma.
6. **Değiştirmeden önce ÖLÇ.** Tahminle düzenleme yok — Playwright ile canlı ölçüm.
7. Commit atma, push atma. Ana oturum commit'ler.

---

## 1. Ortak kabuk — her sayfada birebir aynı olacak

Kaynak: `index.html`. Kopyalanacak parçalar:

| Parça | Nerede | Not |
|---|---|---|
| Siyah üst bant | `<div class="uc-top-navbar dh-shortcuts ...">` | Beyaz tema bandının yerine geçer |
| Sağ sarı ray | `<span class="dh-rail" aria-hidden="true"></span>` | `#wrapper`'ın hemen ÖNÜNE |
| DADA filigranı | `<span class="dh-mark" aria-hidden="true">DADA</span>` | `#wrapper`'ın İLK çocuğu |
| Sarı footer | `<!-- Footer start -->` … `<!-- Footer end -->` | Tema footer'ının yerine |
| Yukarı çık + tema düğmesi | `.backtotop-wrap` | Zaten çoğu sayfada var |
| Scriptler | `footer-reveal.js`, `dh-panel.js`, `dh-reels.js` (video akışı varsa), `dh-track.js` (kayan ray varsa) | `app.js`'ten sonra |

**Tuzak:** `city-select.js` yalnız `#citySelectModal` olan sayfaya eklenir;
yoksa `null.addEventListener` hatası verir. Kontrol et.

Kırmızı **SON HABERLER** şeridi (`bg-danger` ticker) hangi sayfada varsa
**kaldırılır** — kullanıcı istemiyor.

---

## 2. Liste tipi sayfa kalıbı (`haber-liste.html` referans)

- Banner: `.dh-lb` + `data-cat="<kategori>"`
  - Sol üstte breadcrumb (`.dh-art-crumb` — detay sayfasıyla **aynı bileşen**,
    ev ikonu + chevron ayraç). **Liste sayfalarında breadcrumb altına ayraç
    KOYULMAZ**; detay sayfalarında olabilir.
  - Altında sayfa başlığı `.dh-lb__title`, onun altında uçlara doğru sönen
    yumuşak ayraç `.dh-lb__rule`.
  - Oklar (`.dh-lb__nav`) en sağda.
  - Perde: %30 koyu + kurumsal renk soldan ve sağ alt köşeden patlar.
    **Perde slaytın İÇİNDEKİ `.position-cover` katmanına verilir** —
    slider'ın kardeşi olursa Swiper'ın transform'u yüzünden metnin üstünü örter.
- Kategori şeridi: `.dh-catbar` + `.dh-catbar__chip` (aktif: `.is-on`)
- Sıralama: `.dh-sort` + `.dh-sort__tab` (açılır kutu DEĞİL, sekme)
- Kart ızgarası: `.dh-listgrid` — başlıklar **sola yaslı**

### Kategori rengi (`--dh-cat`, `data-cat` ile)
`kadin #4300ff` · `teknoloji #1c3df9` · `spor #19750a` · `finans #2aa1a9`
`savunma #e20000` · `saglik #00c5e5` · `oyun #0c1d49` · boş = kurumsal amber

---

## 3. Bileşen ailesi — yeni sayfada bunları kullan, yenisini uydurma

| Bileşen | Ne için |
|---|---|
| `.dh-card` / `--row` / `--wide` + `.dh-cards` | Haber kartı (dikey, yatay liste, geniş akış) |
| `.dh-card__excerpt` | Kart altında 1-2 cümlelik özet |
| `.dh-tag` / `.dh-tag--lg` | Görsel üstü kategori etiketi (hap değil, köşe imzalı) |
| `.dh-feat` + `.dh-feat__dots` | Bölümün büyük öne çıkan kartı (slider) |
| `.dh-secbar` + `.dh-track` | Bölüm başlık çubuğu + yatay kayan kart rayı |
| `.dh-foto` · `.dh-pod` · `.dh-info` | Foto Fokus · Podcast · İnfografik kartları |
| `.dh-authors` / `.dh-author` | Köşe yazıları modülü |
| `.dh-pop-widget` / `.dh-pop` | Popüler haberler (numaralı) |
| `.dh-panel` + `.dh-cell` | Günlük veri paneli (hava, namaz) — **veri gösterimi için taban** |
| `.dh-teams` | Takım şeridi |
| `.dh-akis` / `.dh-shorts` / `.dh-short` / `.dh-reels` | Video akışı + reels |
| `.dh-band` + `--gastro` / `--diet` | Partner tanıtım bantları |
| `.dh-rev` | Yorum / değerlendirme |
| `.dh-share` | Paylaş |
| `.dh-catbar` · `.dh-sort` · `.dh-lb` | Liste sayfası bileşenleri |

---

## 4. Geometri ve tipografi kararları

- **Kurumsal köşe imzası:** görsellerde ve kart çerçevelerinde
  `border-bottom-left-radius: 0`. Kart yarıçapı 16px.
- **Çipler / sekmeler / düğmeler:** `8px 8px 8px 0` (sert köşe, sol alt keskin).
  **Tam hap (999px) kullanılmaz** — kullanıcı açıkça istemedi.
  Tek istisna: görsel üstündeki kategori ETİKETLERİ hap olabilir.
- **Kenar yumuşatma (mask-image ile solma) YASAK** — denendi, kullanıcı
  "böyle soft istemedim, sil" dedi. Kayan rayın sağ kenarı NET biter;
  "devamı var" bilgisini yarım görünen kart ve oklar verir.
- **Bölüm başlığı ile kart rayı arası ~26px.** Daha dar olmayacak.
- Kart araları: masaüstü 16px, mobil 10px.
- Bölüm başlığı sağındaki bağlantı: **"Tümünü Gör"**, yanında chevron YOK.
  Sol/sağ ok düğmeleri kalır.
- Font: **Gilroy** (`custom.min.css` `:root`'tan geliyor, sayfa başına iş yok).
- Amber zeminde mürekkep **koyu** (`--color-gray-900`, 10,58:1). Amber üstü
  beyaz metin kullanma (1,77:1).
- Sticky kenar sütunlarında `offset: 136` (header 120px + 16px nefes).

---

## 5. Doğrulama — pazarlığa kapalı

Kullanıcı: *"bu hataları ben yakalamayayım"*. Her sayfa için Playwright ile
**ölçümlü** denetim çalıştır; göz kararı yetmez:

- `document.documentElement.scrollWidth - clientWidth > 2` -> yatay taşma, FAIL.
- `page.on('console')` + `page.on('pageerror')` -> 0 olmalı.
- `page.on('response')` -> 4xx sayısı 0 olmalı (kırık görsel/CSS/JS).
- Her taşınan elemanın `getBoundingClientRect()`'i kapsayıcısının içinde mi?
- Üst üste binmemesi gereken elemanlar için çakışma testi (`a.bottom > b.top`).
- Swiper kurulmuş mu: `el.swiper` var mı, slayt yükseklikleri makul mü.
- Kontrast: koyu görsel üstü beyaz metin için zemin parlaklığını piksel
  bazında ölç (metni `visibility:hidden` yapıp ekran görüntüsü al), en açık
  pikselde bile >= 4,5:1 olmalı.
- **1440 / 1000 / 390 + dark** — dördünde de TEMİZ almadan bitirme.
- Sonra ekran görüntülerini **Read ile aç ve BAK.**

Playwright: `/private/tmp/claude-501/-Users-gaviaworks-Developer-Backend-Projects-dadahaber-view/ce22754e-e380-4563-8b9b-222b67e994ab/scratchpad/pw`
(`node_modules` orada; `my-*.js` dosyaları hazır örnek scriptler.)
Yerel sunucu açık: http://localhost:8765/

---

## 6. Çalışma biçimi

- `frontend-design:frontend-design` skill'ini **yükle ve uygula**.
- **2-3 tur:** uygula -> ölç -> kendini eleştir -> revize et -> tekrar ölç.
- White space'e dikkat: ritim tutarlı olsun, bölümler arası aynı nefes.
- Yeni bir kalıp uydurmadan önce mevcut bileşen ailesinde karşılığı var mı bak.
