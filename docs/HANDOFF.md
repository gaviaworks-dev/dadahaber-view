# Dadahaber — Devir Notu

Bu dosya oturum devri içindir. Yeni bir oturuma başlarken önce bunu oku.

---

## Proje

Dadahaber haber sitesinin yeni görünümü. Hazır bir haber teması (`demo-six`) devralındı,
üzerine bölüm bölüm revizyon uygulanıyor. Site tamamen **Türkçe**, deploy **GitHub Pages**.

- Çalışma dizini: `~/Developer/Backend Projects/dadahaber-view`
- 55 HTML sayfa. Ağırlıklı çalışılan: `index.html` (5.049 satır), `haber-detay.html` (1.340 satır)
- Yerel sunucu: `python3 -m http.server 8765` → http://localhost:8765/

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
6. Commit atılır, **push atılmaz**. Her revizyon ayrı commit, ölçülen değerler commit mesajında.

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
4. **Beğen/beğenme ikonlarında outline "oy vermedin" durumunu kodluyordu** — hepsi
   dolduruldu, o ayrım kayboldu.
5. **Siyah üst bant + yeni bileşenler yalnız `index.html` ve `haber-detay.html`'de.**
   Diğer 53 sayfa hâlâ tema markup'ında.
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
