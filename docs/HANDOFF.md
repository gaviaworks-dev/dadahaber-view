# Dadahaber — Devir Notu

Bu dosya oturum devri içindir. Yeni bir oturuma başlarken önce bunu oku.

---

## Proje

Dadahaber haber sitesinin yeni görünümü. Hazır bir haber teması (`demo-six`) devralındı,
üzerine bölüm bölüm revizyon uygulanıyor. Site tamamen **Türkçe**, deploy **GitHub Pages**.

- Çalışma dizini: `~/Developer/Backend Projects/dadahaber-view`
- **67 HTML sayfa** (R6'da 4 yeni: `basketbol` `formula1` `bisiklet` `astroloji`;
  R7'de 7 yeni: `voleybol` `hamilelik` `hamilelik-detay` ve dört büyük takım sayfası;
  R8'de 1 yeni: `arama.html`).
  Referans üçlü: `index.html` · `haber-liste.html` · `haber-detay.html`
- Yerel sunucu: `python3 -m http.server 8765` → http://localhost:8765/

### Depo ve yayın (R8 sonunda kuruldu)

| | |
|---|---|
| Repo | https://github.com/gaviaworks-dev/dadahaber-view · **public** |
| Yayın | https://gaviaworks-dev.github.io/dadahaber-view/ |
| Pages kaynağı | `main` dalı, kök dizin (`/`) |
| Hesap | `gaviaworks-dev` (gh CLI ile giriş yapılmış) |

**Dal yapısı:**

| Dal | Rol |
|---|---|
| `main` | Yayımlanan sürüm. Pages buradan servis eder. |
| `v1` | R8 sonundaki hâlin **donmuş kopyası — SİLİNMEZ, üzerine commit atılmaz.** |
| `v2` | **Çalışma dalı. Yeni iş buraya yapılır.** Hazır olunca `main`'e birleştirilir. |

Üçü de şu an aynı commit'te (`c60abc4`). **Yeni oturumda önce `git checkout v2`.**

`v1`'i sonradan görüntülemek için: `git checkout v1` + yerel sunucu.
v2 yayına geçtiğinde v1'in bir kopyası `main` içinde `/v1/` klasörüne konulup
`…/dadahaber-view/v1/` adresinden kalıcı erişilebilir yapılabilir (site göreli
yol kullanır, kopya kendi içinde tutarlı çalışır).

### Yayın tuzağı — bir kez yaşandı, tekrar etmesin

Site Pages'te **`/dadahaber-view/` alt dizininden** servis ediliyor, yerelde ise
kökten. Bu yüzden:

- `"../assets/..."` yolları yerelde çalışır, **canlıda 404 verir** (tarayıcı `..`'yı
  alan adı köküne çözer). R8'de 3 sayfada 123 referans bu yüzden kırıldı, hepsi
  `"./assets/..."` yapıldı.
- `href="/..."` kök-mutlak yol da aynı sebeple kırılır. Şu an repoda **yok**, eklenmemeli.
- **Kural: her yol `./` ile başlar.** Push öncesi kontrol:
  `grep -l '"\.\./assets/\|href="/[^/]' *.html`

---

## Değişmez kurallar

1. **Renk, marka ve tema token'ı dış kaynaktan kopyalanmaz.** Dış sitelerden yalnız
   UI iskeleti, kompozisyon ve komponent davranışı alınır. Palet Dadahaber kurumsalına sadık kalır.
   *Tek istisna:* partner tanıtım bantlarının içi (DadaGastro `#E14827`, DadaDiet `#3BB77E`) —
   kullanıcı açıkça istedi, kapsam o bandın içiyle sınırlı.
2. **`demo-six.min.css` vendor'dur, dokunulmaz.** Her şey `custom.min.css`'ten override edilir.
   Tek istisna: `:root` bloğundaki token değerleri (İŞ 1'de font `@import` ve aile token'ları,
   R3-16'da hiçbir şey). Başka yeri değiştirilmedi.
3. **`text-bg-primary` utility'si KULLANILMAZ** — `demo-six.min.css`'te hâlâ bayat yeşil
   `RGBA(16,191,71)` değerinde. `bg-primary` amber ama `text-bg-primary` yeşil çıkar.
4. **Yeni kütüphane eklenmez.** Mevcutlarla çözülür (Swiper, native scroll-snap, vanilla JS).
5. **Değiştirmeden önce ÖLÇ.** Tahminle düzenleme yapılmaz — Playwright ile canlı ölçüm.
6. Her revizyon ayrı commit, ölçülen değerler commit mesajında.
   **GÜNCELLENDİ (R8 sonu):** `origin` tanımlı, push serbest. İş `v2` dalına
   yapılır; `main` yalnız birleştirmeyle güncellenir, `v1`'e dokunulmaz.
7. **Her sayfada `<meta name="robots" content="noindex, nofollow">` durur** ve
   kökte `robots.txt` `Disallow: /` verir. Prototip arama motorlarına kapalıdır;
   yeni sayfa eklerken noindex satırı unutulmamalı.
8. Temanın kullanılmayan demo CSS varyantları (`demo-two…demo-ten`, `main.css` —
   97 MB) `.gitignore`'da. Yerel diskte duruyorlar, repoya girmiyorlar.
   Site yalnız `demo-six.min.css` + `custom.min.css` yükler.

---

## Tasarım sistemi

### Kurumsal renk
- Tema token'ı: `--color-primary: #fcb623` (`demo-six.min.css` `:root`)
- **Logo varlığı `#ffac1e` ölçüyor** — 2,7° ton farkı var. **Karar verilmedi, değiştirilmedi.**
  Değiştirmek gerekirse `custom.min.css`'teki tek satır: `--dh-brand: var(--color-primary)`.
- Beyaz zeminde AA geçen ton: `--dh-menu-ink: var(--color-primary-700)` = `#7a5f01` (6,06:1)
- Sarı zeminde metin: `--dh-on-brand: #fff` (1,77:1 — **AA geçmiyor**, kullanıcı bilerek istedi)

### Tipografi — Gilroy (DadaGastro'dan)
- Self-host `@font-face`, `assets/fonts/gilroy/` (Light 300 / Medium 500 / ExtraBold 700-800)
- Gövde 500 / `line-height` 1.55 · Başlık 700 / 1.12 / `letter-spacing` -0.02em
- **Gilroy ticari font** (Radomir Tinkov / MyFonts), açık lisansı yok. Web font lisansları
  genelde alan adı başına verilir — `dadahaber.com` için ayrı kapsam gerekip gerekmediği
  **teyit edilmedi**.
- Başlıklarda `text-transform: uppercase` kaldırıldı (DadaGastro çevirmiyor + `lang="zxx"`
  yüzünden Türkçe `i → İ` bozuluyordu). 54 sayfada `lang="tr"` yapıldı.
- Kullanılmayan `assets/fonts/archivo/` ve `assets/fonts/noto-sans/` duruyor (İŞ 1 kalıntısı).

### Kurumsal köşe imzası
Logo rozeti piksel ölçümü: sol-üst ~20px · sağ-üst ~22px · sağ-alt ~20px yuvarlak,
**sol-alt 0px keskin**. Bu geometri tüm haber görsellerine ve kart çerçevelerine uygulandı.
Yeni bir kart/görsel eklerken `border-bottom-left-radius: 0` unutulmamalı.

### Bileşen ailesi (hepsi `custom.min.css`'te, `.dh-` önekli)

| Bileşen | Ne |
|---|---|
| `.dh-card` + `--row` + `--wide` | Haber kartı. Dikey ızgara, yatay liste, geniş akış. Tek bileşen. |
| `.dh-cards` + `--list` + `--feed` | Kart kapsayıcıları |
| `.dh-panel` + `.dh-cell` | Günlük panel ailesi (hava durumu, namaz vakitleri). İmza: `.is-now` |
| `.dh-teams` | Takım şeridi. Takip edilen takımda aynı `.is-now` işareti |
| `.dh-akis` / `.dh-shorts` / `.dh-short` / `.dh-reels` / `.dh-reel` | Video akışı + reels katmanı |
| `.dh-band` + `--gastro` + `--diet` | Partner tanıtım bantları (sabit arka plan/parallax) |
| `.dh-rcard` | DadaGastro yatay tarif kartı · `.dh-calc` DadaDiet hesaplayıcı |
| `.dh-breaking` | Son dakika şeridi (Swiper ticker) |
| `.dh-shortcuts` | Siyah üst bant |
| `.dh-art-*` | Haber detay banner/breadcrumb/meta/lead |
| `.dh-share` · `.dh-rev` · `.dh-watch` | Paylaş bileşeni · yorumlar · video izle butonu |
| `.dh-footer-brand` · `.dh-foot-soc` · `.dh-store-badge` | Sarı footer |
| `.dh-mark` · `.dh-rail` | DADA filigranı · sağ kenar şeridi |

### Kendi JS dosyalarımız
- `assets/js/footer-reveal.js` — footer perdesi (992px+), güvenlik freni var
- `assets/js/dh-reels.js` — video akışı + reels overlay (scroll-snap, ESC, klavye)
- `assets/js/dh-panel.js` — namaz vakti geri sayımı (`data-dh-prayer="HH:MM"` okur)
- `assets/js/dh-share.js` — paylaşım URL'leri, kopyala, `navigator.share`

### Vendor'da yapılan tek düzeltme
`assets/js/app-head-bs.js` — bülten pop-up koşulu `(!t||e>=4)` → `!t`.
Eskisi her 4 sayfa yüklemesinde tekrar açıyordu.

---

## Doğrulama yöntemi

Playwright kurulu: `/private/tmp/claude-501/.../scratchpad/pw` (npm paketi + chromium).
Hazır scriptler orada: `shot.js`, `shot2.js`, `shotd.js`, `shotfull.js` ve ölçüm scriptleri.

Tipik akış:
1. Referans siteyi Playwright ile aç, DOM/CSS'i **canlı ölç** (gerekirse tıkla, hover'la)
2. Bizim tarafı aynı şekilde ölç, farkı çıkar
3. Uygula
4. Tekrar ölçerek doğrula + ekran görüntüsü al
5. Ölçülen değerlerle birlikte commit

Not: `dadagourmet.com`'da konum modal'ı pointer olaylarını engelliyor — hover davranışını
`document.styleSheets` üzerinden `cssRules` okuyarak ölçmek gerekti.
`dadagastro.com/media/...` görselleri imzalı URL, doğrudan indirilince 403 — detay
sayfasından taze imzayla alınmalı.

---

## Referans siteler

- `dadagastro.com` — tipografi, tarif kartı, Dada Akış/reels, yorum bileşeni, footer sosyal, mağaza rozetleri
- `dadadiet.com` — kurumsal yeşil, hesaplayıcılar
- `dadagourmet.com/gurme-lezzetler` — haber kartı kalıbı, üst bant geometrisi
- `dadagourmet.com/gurme-lezzetler/nohut-nasil-pisirilir` — haber detay yapısı
- `trthaber.com` — header/son dakika şeridi yapısı (İŞ 2)
- `webrazzi.com` — arka plan wordmark fikri
- `haberler.com` — haber detayda video butonu konumu

---

## Bilinen açıklar

1. **Kurumsal renk kararı verilmedi** — logo `#ffac1e` vs tema `#fcb623`.
2. **Gilroy lisans kapsamı teyit edilmedi** (alan adı başına lisans sorusu).
3. **Sarı zeminde beyaz metin AA geçmiyor** (1,77:1). Kullanıcı bilerek seçti.
   Koyu mürekkebe dönmek tek satır: `--dh-on-brand: var(--color-gray-900)` (10,58:1).
4. ~~Beğen/beğenme ikonlarında outline ayrımı kayboldu.~~ **KAPANDI (R4).**
   Oy verilmemiş durum `far` (outline), verilmiş durum `fas` (dolu).
5. ~~Siyah üst bant yalnız iki sayfada.~~ **KAPANDI (R6 yayılımı).** Ortak kabuk
   59 sayfanın tamamında: siyah `dh-shortcuts`, sağ sarı ray, DADA filigranı,
   sarı footer, yukarı çık. Kırmızı SON HABERLER şeridi hiçbir sayfada yok.
6. **Detay sayfası metni 1008px'te ~115 karakter/satır** — klasik 65-75 bandının üstünde.
   Yanlara reklam rayı girince daralacağı varsayımıyla yapıldı.
7. **Video posterleri yatay 16:9 çekimden 9:16'ya kırpıldı** — gerçek dikey içerik gelince
   `ffmpeg` ile yeniden üretilmeli (komut R3-4 commit mesajında).
8. **Reels'te gerçek video oynatma tarayıcıda doğrulanmalı** — headless'ta autoplay
   politikası `play()`'i sessizce reddedebiliyor.
9. **İçerik tamamen yer tutucu.** Backend bağlanınca doldurulacak; namaz saatleri
   `data-dh-prayer` attribute'unda hazır bekliyor.

---

## Repo düzeni

```
index.html                       ana sayfa
haber-detay.html                 haber detay
assets/css/theme/custom.min.css  TÜM özel CSS burada (5.544 satır, bölüm başlıklarıyla)
assets/css/theme/demo-six.min.css  vendor tema — DOKUNMA
assets/js/dh-*.js                kendi bileşen scriptlerimiz
assets/fonts/gilroy/             aktif font
assets/images/partners/          partner bant görselleri + tarifler
assets/images/videos/posters/    ffmpeg ile çıkarılmış video posterleri
docs/HANDOFF.md                  bu dosya
```

`custom.min.css` bölüm başlıklarıyla ayrılmış (`R1 —`, `R2-2 —`, `R3-14 —` gibi);
her bölümün başında **ölçülen değerler ve neden o değer seçildiği** yorum olarak yazılı.


---

## R4–R6 (yayılım fazı) — bu oturumda ne değişti

Ayrıntılı brifing ve kurallar: **`docs/YAYILIM.md`** (kabuk reçetesi, bileşen
ailesi, geometri kararları, doğrulama protokolü). Yeni sayfa yazarken önce onu oku.

### Kesinleşen tasarım kararları
- **Çip / sekme / düğme yarıçapı `8px 8px 8px 0`.** Tam hap (999px) kullanılmaz.
  Tek istisna: görsel üstündeki kategori ETİKETLERİ hap olabilir.
- **Kenar yumuşatma (mask-image ile solma) YASAK.** Denendi, kullanıcı istemedi.
  Kayan rayın sağ kenarı net biter; "devamı var" bilgisini oklar verir.
- **Bölüm başlığı bağlantısı "Tümünü Gör"**, yanında chevron yok. Sol/sağ oklar kalır.
- Bölüm başlığı ile kart rayı arası ~26px. Kart araları masaüstü 16px, mobil 10px.
- Sticky kenar sütunlarında `offset: 136` (header 120px + 16 nefes).
- **Kategori rengi sayfa geneline uygulanmaz.** Sayfa `<head>`'lerindeki
  `:root{--color-primary: <renk> !important}` blokları KALDIRILDI. Kimlik yalnız
  `.dh-lb[data-cat]` banner perdesinden gelir:
  `kadin #4300ff · teknoloji #1c3df9 · spor #19750a · finans #2aa1a9 ·
  savunma #e20000 · saglik #00c5e5 · oyun #0c1d49` · boş = kurumsal amber.
  `--dh-brand-corp` bir SAVUNMA ŞİMİ olarak duruyor (bilerek literal).

### Yeni bileşenler (hepsi `custom.min.css`, `.dh-` önekli)
| Önek | Ne |
|---|---|
| `.dh-lb*` | Liste sayfası bannerı (breadcrumb + başlık + ayraç + oklar + perde) |
| `.dh-catbar*` · `.dh-sort*` | Kategori çipleri · sıralama sekmeleri |
| `.dh-feat*` | Bölümün büyük öne çıkan kartı (slider + noktalar) |
| `.dh-authors` / `.dh-author` · `.dh-wcard` / `.dh-prof` / `.dh-op` | Köşe yazıları modülü · yazar sayfaları |
| `.dh-pop-widget` / `.dh-pop` | Popüler haberler (numaralı) |
| `.dh-secbar` · `.dh-track` · `.dh-foto` · `.dh-pod` · `.dh-info` | Bölüm başlık çubuğu + ray + üç kart ailesi |
| `.dh-fin*` | Finans veri gösterimi (ticker, tablo, vitrin, çevirici, künye) |
| `.dh-sport` · `.dh-stand[data-branch]` · `.dh-mc` · `.dh-podium` · `.dh-stage` · `.dh-rank` | Spor: branş kimliği yapıyla verilir |
| `.dh-serie` · `.dh-gal` · `.dh-eps` · `.dh-player` · `.dh-vstage` · `.dh-arch` | Medya: seri rayı, galeri görüntüleyici, bölüm listesi, oynatıcı, arşiv |
| `.dh-panel--astro` · `.dh-zod` · `.dh-live` | Astroloji modülü · burç ızgarası · dakika dakika akış |
| `.dh-ph` · `.dh-mast` · `.dh-ilan` · `.dh-rate` · `.dh-minifoot` | Belge başlığı · künye · resmî ilan · reklam tablosu · sade footer |

### Yeni JS (hepsi vanilla, kütüphane yok)
`dh-track.js` (kayan ray) · `dh-gal.js` (galeri görüntüleyici) ·
`dh-astro.js` (burç değiştirici) · `dh-toc.js` (yapışkan içindekiler)

### Bu fazda ölçerek yakalanan gerçek hatalar
1. Hero nokta navigasyonu meta satırının üstüne düşüyordu (48px).
2. Yan sütun dikey slider'ında `h-100` döngüsü yüksekliği **33.554.414px**'e patlatıyordu.
3. `.dh-lb` perdesi tema slaytındaki bir div'e bağlıydı; o div olmayan sayfalarda
   banner başlığı **1,28:1** kontrastla okunmuyordu. Perde artık `article::after`.
4. R3-13 meta hizalama kuralı `.hstack` sarmalayıcısını kaçırıyordu → tarih sola yapışıktı.
5. Yukarı çık düğmesi amber üstü beyazdı (1,77:1).
6. `cnnturk`'ün artış/azalış renkleri AA'yı geçmiyordu (2,67 / 3,88) → yeniden seçildi.
7. Koyu temada header logosu `logo.png`'yi gösteriyordu (siyah wordmark, görünmez)
   → `logo-white.png` çifti 59 sayfada kuruldu.
8. `.dh-cell__label` / `.dh-panel__kicker` 4,17:1 → gray-500 (5,74:1).
9. Footer yasal listesinde kapanmayan `<li>` + "AYDINALTMA" yazım hatası (57 sayfa).

### ⚠ Paralel ajan tuzağı — iki kez yaşandı
`custom.min.css`'e **yalnız `cat >>` ile SONA ekle.** Write/Edit ile tüm dosyayı
yeniden yazan bir ajan, başka ajanların bloklarını siler. R4-D1 ve bir R4-* bloğu
bu yüzden kayboldu, yeniden yazıldı. Blok bütünlüğünü `grep -c` ile doğrula.

### Doğrulama protokolü (zorunlu)
Playwright ile **ölçümlü** denetim: yatay taşma (`scrollWidth - clientWidth > 2`),
`console` + `pageerror` = 0, 4xx = 0, kapsayıcı taşması, kardeş çakışması,
koyu görsel üstü metin için **piksel bazlı kontrast** (metni `visibility:hidden`
yapıp zemini ölç). **1440 / 1000 / 390 + dark** — dördü de temiz olmadan bitirme.

Son tam tarama: **59 sayfa × 4 konfigürasyon = 236 koşu, hepsi temiz.**

### Açık kalan kararlar
- `assets/images/logos/` altındaki **kategori logoları** (`spor-logo.png`,
  `kadin-logo.png`, `finans-logo.png` …) kullanılmıyor; kabuk her sayfada aynı
  ortak logoyu taşıyor. Bölüm logosu istenirse marka kararı olarak alınmalı.
- Yasal metinler mevzuata uygun iskelet; **hukuk onayından geçmedi**.
- Yapışkan içindekiler yalnız sayfanın en dibinde (1000px yükseklikte) header'ın
  arkasına giriyor; 1440px'te olmuyor. Standart sticky davranışı.


---

## R7 — İkinci yayılım turu

Bu tur, R6 yayılımının üstüne kullanıcı geri bildirimleriyle ilerledi. Altı ajan
çalıştı (liste hero'su · yorum akışları · finans düzeni · kurumsal görsel kimlik ·
hamilelik bölümü · spor mimarisi + kategori mimarisi), aralarına ana oturumun
site geneli düzeltmeleri girdi.

### Yeni sayfalar
`voleybol.html` · `hamilelik.html` · `hamilelik-detay.html` ·
`takim-galatasaray.html` · `takim-fenerbahce.html` · `takim-besiktas.html` ·
`takim-trabzonspor.html`

### Kesinleşen yeni kararlar (R6'nın üstüne)
- **Liste bannerı `.dh-lb` 420px.** Tek sürekli perde, kimlik şeridi CSS grid'de,
  hizalama sapması 0. Perde slaytın `article::after`'ında — kardeş katman
  yaparsan Swiper'ın transform'u metnin üstünü örter (bu hata iki kez yaşandı).
- **Tek sayfalama bileşeni `.dh-pager`.** Site iki ayrı kalıp taşıyordu, ikisi de
  biçimlenmemişti. Çizgiye üstten 48px alttan 40px nefes.
- **Sayfalamada çift katman yasak.** Son içerik yüzeyi ile footer arasında farklı
  renkte şerit kalmayacak (`R7-Z2`).
- **Zeminli bantta nefes payı**: üst 56px / alt 60px (mobil 36/40) — `R7-N`.
- **Alt kategori şeridinin kökü** (`.dh-catbar__row` + `.dh-catbar__root`):
  kategori renginde 3px şerit + üst kategori adı + "alt kategorileri" (spor'da
  "dalları"). **Chevron kullanılmaz** — chevron breadcrumb'ın işareti, kök ise
  kapsam etiketi; ikisi ayrışsın diye. Kök sayfanın kendisiyse
  `<span aria-current="page">`, gerçekten bir üst kademe varsa `<a>` +
  `.dh-catbar__root--link` (44px dokunma hedefi bunun için).
- **Şeridin semantiği üç ayrı durum:** modül değiştiriyorsa `role="tablist"`
  (kadin.html), başka sayfaya gezindiriyorsa `<nav>` + bağlantı, veri
  değiştiriyorsa `role="radiogroup"` (lig çipleri). Karıştırma.
- **Yazar adının altında unvan satırı** (`.dh-byline`). Beyaz mürekkep yalnız koyu
  bağlamda (`.uc-dark` / `.dh-lb` / `.dh-feat` / `.dh-hero`); açık zeminde gray-900.
- **Öne çıkan kart zikzak**: ardışık bölümlerde büyük kart sağ-sol-sağ (`R7-A`).
- **Kategori/takım rengi sayfa geneline uygulanmaz.** `<head>`'e `--color-primary`
  override'ı **eklenmez**. Kimlik yalnız `.dh-lb[data-cat]` / `[data-team]`
  perdesinden gelir; ortak kabuk kurumsal amber kalır.

### Yeni bileşenler (R6 tablosuna ek)
| Önek | Ne |
|---|---|
| `.dh-pager` | Tek sayfalama bileşeni (20+ sayfa) |
| `.dh-zeb` / `--w` | Medya sayfalarında zebra bant |
| `.dh-catbar__row` / `__root` | Alt kategori şeridinin kökü |
| `.dh-byline` | Yazar adı + unvan |
| `.dh-yn` · `.dh-bil` | Yorum yanıt alanı · bildir modalı |
| `.dh-finsum` · `.dh-finnews` | Finans piyasa özeti · haber omurgası |
| `.dh-hub` · `.dh-son5` · `.dh-mcrail--sik` | Spor bandı · maç formu · sıkı skor şeridi |
| `.dh-ph--photo` / `--doc` / `--prof` | Kurumsal · belge damgası · yazar profili başlığı |
| `.dh-about` · `.dh-strip` · `.dh-mastgrid` · `.dh-tlgrid` | Hakkımızda ızgarası · fotoğraf paneli · künye · kilometre taşları |
| `.dh-kmod` · `.dh-chk` · `.dh-cell--go` | Kadın modül alanı · kontrol listesi · tıklanabilir hücre |
| `.dh-panel--gebe` · `.dh-tri` · `.dh-hesap` · `.dh-medinfo` | Gebelik haftası · trimester · hesaplayıcı · sağlık uyarısı |
| `.dh-stand[data-branch]` · `.dh-lgpick` · `.dh-sort--tabs` | Lig tablosu · üç kademeli seçici · lig merkezi sekmeleri |

### Yeni JS (hepsi vanilla, kütüphane yok)
`dh-track.js` · `dh-gal.js` · `dh-astro.js` · `dh-toc.js` · `dh-listen.js` ·
`dh-yorum.js` · `dh-gebelik.js` · `dh-hesap.js` · `dh-lig.js` · `dh-lig-veri.js` ·
`dh-tabs.js` · `dh-kadin.js`

**Ortak sözleşme:** veri sayfadaki `<script type="application/json">` bloğunda,
işaretleme `data-dh-*` niteliklerinde. Backend gelince yalnız JSON bloğu değişir.
`dh-astro.js` · `dh-gebelik.js` · `dh-kadin.js` bu deseni birebir paylaşıyor.

### R7'de ölçerek yakalanan gerçek hatalar
1. Yan sütun slider'ında `h-100` döngüsü yüksekliği **33.554.414px**'e patlatıyordu.
2. `.dh-lb` perdesi tema markup'ına bağlıydı; o div'i olmayan sayfalarda banner
   başlığı **1,28:1** kontrastla okunmuyordu.
3. Hero kartı için yazılmış `color:#fff !important` bağlamdan bağımsızdı; açık
   zeminli kartlarda yazar adı **1,1:1** çıkıyordu.
4. Evrensel radyo sıfırlaması radyoyu kare yapıp **teal** boyuyordu (renk finans
   kategorisinden sızmış).
5. Ölü eski script 7 sayfada `alert()` kullanıyordu.
6. `hamilelik.html`'de `#wrapper` hiç kapanmıyordu; footer wrapper içinde kalıyor,
   `app.js` null hatası veriyordu.
7. `404.html` / `coming-soon.html`'de **fontawesome hiç yüklenmiyordu**.
8. Footer yasal listesinde kapanmayan `<li>` + "AYDINALTMA" yazım hatası (57 sayfa).
9. Koyu temada header logosu siyah wordmark'ı gösteriyordu.
10. Takım çipinde arma 9px alttan taşıp kırpılıyordu.
11. 390px'te spor hub sütunları **22px**'e çöküyordu (kaskad sırası hatası).
12. Takım sayfası banner alt satırı **2,77:1** — `<p>` bloklaşıp fotoğrafın açık
    bölgesini kapsıyordu; kutusu 1132 → 268px'e indirilince düzeldi.

### Bir ölçüm hatası da kayda geçti
`R7-C15`: breadcrumb kontrastı "3,45:1" diye raporlanmıştı; `<nav>` blok
seviyesinde olduğu için ölçüm kutusu bandın sağ yarısını da kapsıyordu. Metni
taşıyan çocuk ölçülünce 14,40–20,87. **Yanlış alarm silinmedi, not edildi.**

### R7 sonu açık kalanlar
- **Gerçek kulüp armaları yok** ve indirilmedi — tescilli marka, kullanım hakkı
  müşteri kararı. Takım renkleri de kulüp marka kılavuzundan alınmadı, kontrast
  için renk ailesinden seçildi.
- **Oyuncu adları kurgusal** (yanlış atıf / kişisel veri riski).
- **Hamilelik içeriği tıbbi onaydan geçmedi.** 40 haftanın boy/ağırlık değerleri
  yer tutucu ortalamalar; yayına çıkmadan hekim/sağlık editörü doğrulamalı.
  Hesaplayıcı sonucu `localStorage`'a **yazılmıyor** — gebelik verisi hassas
  kişisel veri, saklama kararı KVKK kapsamında ayrıca alınmalı.
- **Yasal metinler hukuk onayından geçmedi.**
- `.dh-fx__cols` / `.dh-fx__row` ızgara şablonları site genelinde birbirini
  tutmuyor; yalnız `.dh-hub__main` kapsamında düzeltildi.
- `.dh-lgpick__scope` ve `R7-C7`'deki eski `.dh-field*` kalıntıları ölü kod.
- Kadın'da modülsüz 6 kategoride haber listesi süzülmüyor (gerçek süzme backend işi).

---

## R8 — Sayfalandırma, responsive denetim, mobil alt menü

Doğrulama: Playwright/Chromium, **67 sayfa × 10 genişlik** (320·360·390·414·768·
820·1024·1280·1440·1920). Her bulgu ölçülerek bulundu ve ölçülerek doğrulandı.

### Yeni sayfa
- **`arama.html`** — arama sonuçları. Sitede her sayfada arama kutusu vardı ama
  `action="?"` ile hiçbir yere gitmiyordu. `haber-liste.html` şablon alındı,
  manşet slider'ının yerine `.dh-ph--photo` fotoğraflı başlık bandı kondu.
  67 sayfadaki form buraya bağlandı.

### Sayfalandırma (`.dh-pager`) — 38 sayfa, tek markup imzası
R7-P'deki bileşen tamamlandı: **ilk/son uçları**, **devre dışı durum**
(`<span aria-disabled>`, `<a>` değil), 44×44 hedef, ≤400px'te daralma.
Sitede üç ayrı kalıp vardı (`.dh-pager` 26 · `.dh-chip` nav 3 · yok 7) — hepsi
tek bileşene çekildi. `son-dakika`'da "daha eski yükle" düğmesinin yerine geçti.

**Ölçülen kusurlar:** sarmalayıcı + bileşen iki ayrı yatay çizgi çiziyordu
(1280px'te 73px arayla) · uç düğmesinde iki chevron `inline-grid` yüzünden alt
alta düşüyordu · tema `.nav-pagination a` (0,1,1) daralma kuralını yiyordu.

### Kritik responsive bulgular
1. **`overflow-hidden-x` hiçbir CSS'te tanımlı değildi.** 67 sayfanın hepsinde
   `#wrapper`'da duruyor, `.dh-zeb` tam genişlik bandı buna güveniyordu.
   1279–1296px arasında 19 sayfada 16px gerçek yatay kaydırma. `overflow-x: clip`
   verildi (`hidden` değil — sticky yan sütunu bozardı).
2. **Tablette `.dh-card--row` ikiye bölünüyordu** (768–991,98, 13 sayfa, kart
   154–185px, başlıklar kırpık). Sebep kaskad sırası: `.dh-cards--list{1fr}`
   3448. satırda, `.dh-cards{repeat(2,…)}` medya sorgusunda daha sonra, ikisi de
   (0,1,0). İki sınıflı seçiciyle geri alındı.
3. **11 form alanı 16px altındaydı** (iOS zorla yakınlaştırma) → ≤991,98px'te 16px.

### Orta
- **Dokunma hedefleri**: header arama 24×24, hamburger 32×40, tema anahtarı
  24×24, çerez kapat 14×14, sıralama sekmesi 45×24, kategori çipi 49×36, şerit
  okları 32×32 … Görsel boyut korunarak görünmez `::before` ile büyütüldü;
  **kaydırılan şeritlerde bu çalışmıyor** (kap taşmayı kırpıyor), orada gerçek
  yükseklik verildi. Ölçüm yöntemi: `elementFromPoint` ile 44×44 kutunun dört köşesi.
- **Mobilde 12px tabanı**: 58 bileşen etiketi 9,5–11px'teydi. Yalnız taban,
  11,5px üstüne dokunulmadı.
- **Logo CLS**: `.w-48px` ve `.logo-w-lg` oransızdı → `aspect-ratio` (134 → 0).
- **`100vh` → `dvh`** (yorum bildir modalı).
- **Media query eşikleri** Bootstrap `.98` kuralına çekildi (26 blok).

### Haber detay okuma genişliği
Range ile gerçek karakter sayımı: **1280px'te 141 karakter** (WCAG sınırı 80).
R3'te max-width kaldırılmıştı; gerekçesi "paylaş/önceki-sonraki blokları 1008px
olunca metin sıkışık duruyordu" idi — o hizalama şikâyeti haklı olduğu için
metin tek başına değil **okuma kolonunun tamamı** 612px'e çekildi (metin 580px).
Kapak görseli kabın dışında, tam genişlikte. Kolon daralınca float'lı görsellerin
yanındaki metin ~40 karaktere düşüp yaslamada boşluk açtığı için bu kapsamda
float kapatıldı. **Sonuç: 141 → ortalama 70 karakter.**

### Mobil alt gezinme (`.dh-bnav`) — kullanıcı isteği
Anasayfa · Son Dakika · Menü · Dinle · Ara. ≤991,98px'te görünür.
"Menü" mevcut offcanvas panelini açar. **z-index 999** — offcanvas 1000, rail
1000, "Görüş Bildir" 1000 ölçüldüğü için; menü açılınca panel çubuğun üstünde
kalır. Rail, tema anahtarı ve FAB çubuğun üstüne çekildi. `env(safe-area-inset-bottom)`.

### Diğer
- `haber-detay.html`'deki İngilizce yer tutucu metin Türkçeleştirildi. Yan fayda:
  tema `hyphens:auto` açıktı ama `lang="tr"` + İngilizce metin yüzünden hiç
  tireleme yapamıyordu; artık yaslı gövde düzgün tireleniyor.
- **Logo `srcset`**: 140px'lik yere 1198×244 / 95 KB PNG iniyordu. `sips` ile
  300w/600w/96w türevleri üretildi → 390px @1x'te logo yükü **161 KB → 44 KB**.
  Haber görsellerine dokunulmadı (hepsi yer tutucu, türev üretmek build işi).
- 352 yazar avatarına `loading="lazy"`.
- Slider noktaları: merkezler arası 15px ölçüldü, alan **15×40** yapıldı
  (komşuya binmeden WCAG 2.5.8'in 24×24 eşiğinin üstü).

### Kasten düzeltilmeyenler
- **Paragraf içi / kart başlığı bağlantıları** — WCAG 2.5.5 "inline" istisnası.
- **Kart görseli üstündeki kategori etiketi (44×19)** — büyütmek kapak
  bağlantısının alanını çalar, habere gitmek isteyeni kategoriye götürürdü.
- **Haber görsellerinde `srcset`** — türev boyut yok, buildless kalacak.

### Yayın (R8 sonu)
GitHub Pages reposu bu turda kuruldu: `gaviaworks-dev/dadahaber-view`, public,
Pages `main` kökünden. `v1` donmuş kopya, `v2` çalışma dalı.
Temanın kullanılmayan demo CSS varyantları (demo-two…demo-ten, main.css — 97 MB)
`.gitignore`'a alındı; site yalnız `demo-six.min.css` yükler. Tüm sayfalara
`noindex` + `robots.txt` eklendi.

---

## R8 sonu — durum ve v2'de bekleyenler

### Doğrulanmış durum (67 sayfa × 10 genişlik, canlı ölçüm)

| Kontrol | Sonuç |
|---|---|
| Yatay taşma | **0 / 67** |
| Sayfalama markup imzası | **38 sayfa / tek imza** |
| Mobil alt gezinme | **0 sorunlu sayfa** |
| 16px altı form alanı | **yok** |
| Görselde CLS riski | **0** |
| Tablette daralan kart | **0** |
| Konsol / JS hatası | **yok** |
| Canlı (Pages) 404 | **0** |

### v2'de ele alınacaklar — öncelik sırasıyla

1. **Haber görsellerinde `srcset` yok** (2344 görsel). 390px'te 1000px'lik dosya
   iniyor. Türev boyut üretmek gerekiyor — görseller yer tutucu olduğu için
   R8'de bilinçli ertelendi. Gerçek içerik/CMS geldiğinde görsel hattıyla çözülmeli.
   Logo için türevler üretildi (`logo-300w/600w`, `*-96w`), kalıp orada.
2. **İçerik hâlâ yer tutucu.** `haber-detay.html` R8'de Türkçeleştirildi ama
   diğer detay sayfalarında ve kartlarda yer tutucu metin/görsel sürüyor.
3. **Hukuki metinler onaydan geçmedi** (KVKK, çerezler, kullanım şartları,
   aydınlatma, yayın ilkeleri, künye). Yayına çıkmadan hukuk okumalı.
4. **Gilroy ticari font**, açık lisansı yok — public repoda yayımlanıyor
   (kullanıcı bilerek onayladı). `dadahaber.com` için alan adı lisansı teyit edilmeli.
5. **Hamilelik bölümü tıbbi onaydan geçmedi**; 40 haftanın değerleri yer tutucu.
6. **Kulüp armaları yok**, oyuncu adları kurgusal — tescilli marka kullanımı
   müşteri kararı.
7. Kadın'da modülsüz 6 kategoride haber listesi süzülmüyor (gerçek süzme backend işi).
8. `.dh-fx__cols` / `.dh-fx__row` ızgara şablonları site genelinde birbirini
   tutmuyor; yalnız `.dh-hub__main` kapsamında düzeltildi.
9. Ölü kod: `.dh-live__more` / `.dh-live__morebtn` CSS'i (markup'ı kalmadı),
   `.dh-lgpick__scope`, eski `.dh-field*` kalıntıları.

### R8'de kasten düzeltilmeyenler (tekrar açılmasın)

- **Paragraf içi ve kart başlığı bağlantıları 44px altında** — WCAG 2.5.5'in
  "inline" istisnası. Büyütmek tipografiyi ve kart düzenini bozar.
- **Kart görseli üstündeki kategori etiketi 44×19** — büyütmek kapak
  bağlantısının alanını çalar; habere gitmek isteyen kategoriye giderdi.
- **Slider noktaları 8×8** — alan 15×40 yapıldı (merkezler 15px arayla, daha
  fazlası komşuya biner). WCAG 2.5.8 (24×24) sağlanıyor.

### Ölçüm ortamı

Playwright + Chromium, kendi scratchpad'inde kuruldu (`npm i playwright` +
`npx playwright install chromium`, `PLAYWRIGHT_BROWSERS_PATH` ile yerel klasöre).
Kullanılan ölçüm scriptleri: taşma taraması, `elementFromPoint` ile etkin dokunma
alanı, `Range` ile gerçek karakter/satır sayımı, alt dizin taklidi (`page.route`
ile `/dadahaber-view/` öneki), CDP `CSS.getMatchedStylesForNode` ile hangi kuralın
kazandığı. **Kaskad çakışmalarını tahminle değil CDP ile çöz** — R8'de dört ayrı
"kural uygulanmıyor" vakası bu şekilde bulundu.

---

# v2 — Nihai Menü Haritası bilgi mimarisi

**Yeni oturumda önce `docs/V2-IA.md` oku.** Menü metni, sıra ve gruplama orada;
o dosyadan sapılmaz. Kaynak: `Dada_Haber_Nihai_Menu_Haritasi (1).docx`
(Sürüm 1.0, 19 Ağustos 2026).

## v2'nin taşıyıcı kararı: v1 donmuş kalmalı

`main` içinde `/v1/` klasörü v1'in yayındaki kopyasıdır ve varlıkları
`../assets/` üzerinden **paylaşır**. Bu ancak v2 varlık ağacına yalnız
EKLEME yaparsa güvenlidir. Bu yüzden v2'de:

| Dosya | Kural |
|---|---|
| `assets/css/theme/custom.min.css` | **DEĞİŞTİRİLMEZ.** Tüm v2 CSS'i `assets/css/theme/v2/` altına. |
| `assets/js/dh-*.js` | **DEĞİŞTİRİLMEZ.** Yeni davranış `assets/js/v2/`. |
| `assets/images/**` | Yalnız eklenir, mevcut dosya değiştirilmez/silinmez. |
| `assets/css/theme/demo-six.min.css` | Vendor, dokunulmaz (v1'den beri). |

`/v1/` kopyasını üreten betik: `docs/parts/v1-kopya.py` (yayın anında çalışır).
Donmuş kopyanın etiketi: `v1` dalı + `v1-donmus` git etiketi.

## Kabuk tek kaynaktan yayılır — elle düzenlenmez

```bash
python3 docs/parts/uret.py     # header.html · offcanvas.html · footer.html üretir
python3 docs/parts/yay.py      # tüm kök *.html sayfalarına yayar (idempotent)
```

`uret.py` içindeki `MENU` / `BANT` / `SOSYAL` / `FOOTER` yapıları dokümandan
birebir kopyalanmıştır. Menü değişecekse **orayı** değiştir, sayfaları değil.

`yay.py` her sayfada dört şeyi yapar: offcanvas bloğunu, `<!-- Header start -->`
… `</header>` aralığını ve `<footer id="uc-footer">` … `</footer>` aralığını
değiştirir; eksikse `v2.css` ve `dh-v2-nav.js` bağlantılarını ekler.
`404.html` ve `coming-soon.html` bilerek footer almaz (`.dh-minifoot` taşırlar).

Aktif menü başlığı markup'a gömülmez: sayfa `<body data-dh-cat="spor">` yazar,
`assets/js/v2/dh-v2-nav.js` işaretler. Böylece kabuk yeniden yayıldığında
aktif işaret kaybolmaz.

Yeni sayfa `docs/parts/sayfa-sablon.html`'den türetilir.

## Kabuk ölçüleri

| Katman | Yükseklik |
|---|---|
| Üst servis bandı | 40px (yapışkanda gizlenir) |
| Marka satırı | 84px (yapışkanda 56px) |
| Ana gezinti | 48px |
| **Toplam** | **172px · yapışkanda 104px** |

Yapışkan kenar sütunu ofseti bu yüzden `136` → `120` yapıldı.

## v2'de eklenen tasarım dili

- **Veri ve doğrulama sesi:** sayısal/zaman/künye/doğrulama bilgisi
  `var(--dh-mono)` (sistem monospace), 10–11px, `letter-spacing: .08em`,
  versal. Yeni font İNDİRİLMEDİ. Bu ses "bu bir kayıt/ölçüm" demek —
  Haber Karnesi, Dada Doğrula kararları, güncelleme saatleri, arama meta'sı.
- **11 kategori kimlik rengi** `v2/kabuk.css` `:root`'unda: `--dh-c-simdi`
  `--dh-c-gundem` `--dh-c-dunya` `--dh-c-ekonomi` `--dh-c-teknoloji`
  `--dh-c-gelecek` `--dh-c-spor` `--dh-c-saglik` `--dh-c-kultur` `--dh-c-video`
  `--dh-c-kesfet`. Kimlik yalnız banner perdesi ve şeritlerde; sayfa geneline
  `--color-primary` override'ı EKLENMEZ (v1'den beri geçerli).
- **Karar/tür etiketleri renkle ayrışmaz, metinle ayrışır.** Renk körlüğü ve
  gri baskı için etiketin kendisi kararın adını taşır (Doğru / Yanlış /
  Kısmen Doğru / Bağlamdan Koparılmış / Manipülasyon / Yapay Zekâ İçeriği ·
  Görüş / Analiz / Yorum).

## v2'de ölçerek yakalanan gerçek hatalar

1. **Vendor `uc-drop` mega paneli 250px'e kilitliyordu.** `stretch: x` inline
   `width: 1248px` yazıyor ama kullanılan genişlik 250px kalıyordu
   (`min-width: 250px` + drop'un kendi konumlandırması). Panel saf CSS'e
   taşındı: `.dh-v2-nav__bar { position: relative }` + `.dh-mega { position:
   absolute; inset-inline: 0 }` + `:hover` / `:focus-within`. Ölçülen genişlik
   artık 1248px = container.
2. **Karanlık mod sınıfı `uc-dark`, `dark` DEĞİL.** İlk yazılan 18 `html.dark`
   seçicisi hiç uygulanmıyordu. URL ile tetikleme: `?dark=1`.
   `localStorage.setItem('darkMode','true')` çalışmaz.
3. **Footer perdesi 671px'lik yeni footer'la kırılıyordu.** `footer-reveal.js`
   güvenlik freni `yükseklik + 80 > innerHeight` koşuluna bakıyor; 800px
   viewport'ta 671+80 = 751 < 800 olduğu için perde açık kalıyor ve footer'ın
   üst sütunları ekranın tepesine düşüyordu. Script 67 sayfadan kaldırıldı.
   6 sütunlu footer bir bilgi yüzeyi, perde değil.
4. **Sayfa şablonunda `#page-url` eksikti.** `assets/js/app.js` her sayfada
   `document.getElementById('page-url').value` yazıyor; GÖRÜŞ BİLDİR bloğu
   olmayan sayfa `pageerror` veriyor. Blok şablona geri kondu.
5. **992–1279 arasında gezintiyi yatay kaydırmak mega paneli kırpıyordu.**
   Kaydırma kaldırıldı; 11 başlık 12.5px yazı + 8px iç boşlukla sığıyor
   (992px'te liste 960px kutuda 807px'te bitiyor, ölçüldü).
6. **Tema kalıntısı kırık bağlantılar:** `blog-category.html`
   `blog-details.html` `page-author.html` `infografik-detay.html`
   `href="to_top"` — 82 sayfada düzeltildi. Site genelinde kırık iç bağlantı
   sayısı artık **0**.

## v2 açık kalanlar

- `v2.css` parçaları `@import` ile toplanıyor. Prototip için yeterli; gerçek
  yayında tek dosyaya düzleştirilmeli (paralel indirmeyi engelliyor).
- Alt kategorilerin çoğu gerçek sayfa değil, `haber-liste.html`'e bağlanıyor.
  Backend gelince kategori yönlendirmesi kurulmalı.
- Dada Doğrula iddiaları ve Farklı Bakışlar kaynak adları **kurgusaldır**;
  gerçek kişi/yayın organına iddia veya görüş atfedilmemiştir. Gerçek içerik
  gelince editoryal onay şart.
- Hesabım sayfası prototiptir; gerçek kişisel veri toplamaz, tercihler
  yalnız `localStorage`'da. KVKK kapsamı ayrıca ele alınmalı.
- v1'den devreden açıklar (Gilroy lisansı, sarı zeminde beyaz metin AA,
  hukuk onayı, kulüp armaları, hamilelik tıbbi onayı) **aynen duruyor.**
