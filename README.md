# Dadahaber — arayüz prototipi

Dadahaber haber sitesinin yeni görünümü. **Statik prototip:** build adımı yok,
paket yöneticisi yok, backend yok. Dosyaları bir statik sunucudan servis etmek yeterli.

> **Bu bir yayın değildir.** Sayfalardaki haber metinleri, isimler, rakamlar ve
> görseller yer tutucudur. Hukuki metinler (KVKK, çerezler, kullanım şartları,
> aydınlatma metni) hukuk onayından geçmemiştir. Site `noindex` ve `robots.txt`
> ile arama motorlarına kapalıdır.

## Yayın

GitHub Pages · `main` dalı · kök dizin

| | |
|---|---|
| **v2 (güncel)** | https://gaviaworks-dev.github.io/dadahaber-view/ |
| **v1 (donmuş arşiv)** | https://gaviaworks-dev.github.io/dadahaber-view/v1/ |

## Sürümler

| Dal / dizin | Ne |
|---|---|
| `main` | Yayımlanan sürüm. Pages buradan servis eder. |
| `v1` dalı + `v1-donmus` etiketi | R8 sonundaki hâlin donmuş kopyası. **Silinmez, üzerine commit atılmaz.** |
| `/v1/` klasörü (main içinde) | v1'in yayındaki kopyası. `docs/parts/v1-kopya.py` üretir. |
| `v2` dalı | Çalışma dalı. |

`v1`'i yerelde görmek için:

```bash
git checkout v1
python3 -m http.server 8765     # → http://localhost:8765/
```

**v1 nasıl donmuş kalıyor:** `/v1/` kopyası yalnız HTML taşır ve varlıkları
`../assets/` üzerinden paylaşır. Bu güvenli, çünkü **v2 varlık ağacına yalnız
ekleme yapar** — `custom.min.css` ve mevcut `assets/js/dh-*.js` v2'de
değiştirilmemiştir. Tüm v2 CSS'i `assets/css/theme/v2/` altındadır.

## v2 — bilgi mimarisi

v2, `Dada_Haber_Nihai_Menu_Haritasi` (Sürüm 1.0, 19 Ağustos 2026) dokümanına
göre kuruldu. **Sözleşme: `docs/V2-IA.md`** — menü metni, sıra ve gruplama
oradan sapmaz.

Ana menü (11 başlık):
`Şimdi · Gündem · Dünya · Ekonomi · Teknoloji · Gelecek · Spor · Sağlık ·
Kültür & Yaşam · Video · Keşfet`

Marka söylemi: **"Gündemin net hâli."**

### v2'de gelen sayfalar

| Grup | Sayfalar |
|---|---|
| Ana kategori merkezleri | `simdi` `gundem` `dunya` `ekonomi` `gelecek` `kultur-yasam` `video` `kesfet` |
| Dada formatları | `dada-ozet` `dada-dogrula` `dada-baglam` `farkli-bakislar` `veri-harita` `sakin-akis` |
| Kullanıcı alanı | `hesabim` |

Mevcut sayfalar silinmedi, yeni ebeveynlerine bağlandı:
`savunma` `oyun` → Teknoloji · `kadin` `hamilelik` → Sağlık ·
`astroloji` → Kültür & Yaşam · `doviz` `altin` `borsa` `kripto` `finans` → Ekonomi

### Kabuk tek kaynaktan yayılır

Header, mobil menü ve footer **elle düzenlenmez.** Veri `docs/parts/uret.py`
içindedir; parçalar üretilir ve `docs/parts/yay.py` ile tüm kök HTML sayfalarına
yayılır. Yayıcı idempotenttir.

```bash
python3 docs/parts/uret.py     # header/offcanvas/footer parçalarını üret
python3 docs/parts/yay.py      # tüm sayfalara yay
```

Aktif menü başlığı markup'a gömülmez; sayfa `<body data-dh-cat="spor">` yazar,
`assets/js/v2/dh-v2-nav.js` işaretler.

## Yerel çalıştırma

```bash
python3 -m http.server 8765
# → http://localhost:8765/
```

`file://` ile açma — göreli yollar ve `fetch` çağrıları çalışmaz.

## Yapı

```
*.html                       kök sayfalar (referans üçlü: index · haber-liste · haber-detay)
v1/                          v1'in donmuş yayın kopyası (yalnız main'de)
assets/css/theme/
  demo-six.min.css           vendor tema — DOKUNULMAZ
  custom.min.css             v1'in CSS'i — v2'de DEĞİŞTİRİLMEZ (v1 kopyası paylaşıyor)
  v2.css                     v2 toplayıcı
  v2/kabuk.css               header · mega menü · footer
  v2/a-gundem.css            Şimdi · Gündem · Dünya
  v2/b-bolum.css             Ekonomi · Gelecek · Kültür & Yaşam
  v2/c-kesfet.css            Keşfet · Dada Özet · Doğrula · Bağlam
  v2/d-arac.css              Farklı Bakışlar · Veri & Harita · Sakin Akış · Hesabım
  v2/e-detay.css             Video · haber detay modülleri · arama · görüş etiketi
assets/js/dh-*.js            v1 bileşen scriptleri — DEĞİŞTİRİLMEZ
assets/js/v2/*.js            v2 scriptleri
assets/fonts/                self-host fontlar
docs/V2-IA.md                v2 bilgi mimarisi sözleşmesi
docs/HANDOFF.md              oturum devri notu — yeni oturumda ÖNCE bunu oku
docs/YAYILIM.md              sayfa yayılım fazı brifingi
docs/parts/                  kabuk üreteci + yayıcı + sayfa şablonu
```

## Değişmez kurallar

1. `demo-six.min.css` **vendor'dur, dokunulmaz.**
2. **`custom.min.css` v2'de değiştirilmez.** v1 kopyası onu paylaşıyor; değişirse
   v1 donmuş olmaz. Tüm v2 CSS'i `assets/css/theme/v2/` altına.
3. **Mevcut `assets/js/dh-*.js` değiştirilmez.** Yeni davranış `assets/js/v2/`.
4. `text-bg-primary` utility'si **kullanılmaz** — vendor'da bayat yeşil değerde.
5. **Yeni kütüphane eklenmez.** Swiper, native scroll-snap ve vanilla JS yeter.
6. Site tamamen **Türkçe**; İngilizce yer tutucu metin bırakılmaz.
7. **Her yol `./` ile başlar.** `../assets/` ve kök-mutlak `/...` canlıda kırılır
   (Pages `/dadahaber-view/` alt dizininden servis ediyor). Tek istisna: `/v1/`
   kopyası, ki o gerçekten alt dizindedir.
8. Karanlık mod sınıfı `<html>` üzerinde **`uc-dark`** — `dark` değil.
   URL ile tetiklemek için `?dark=1`.
9. Köşe imzası: yarıçap `8px 8px 8px 0` (sol-alt keskin).
10. **Değiştirmeden önce ölç.** Tahminle düzenleme yapılmaz.

## Bilinen açık konular

- **Gilroy ticari bir fonttur** (Radomir Tinkov / MyFonts) ve açık lisansı yoktur.
  Alan adı bazlı web font lisansının `dadahaber.com` için ayrı kapsam gerektirip
  gerektirmediği teyit edilmemiştir.
- Tema demo görselleri satın alınan temaya aittir.
- Kulüp armaları ve oyuncu adları kurgusaldır; gerçek marka kullanılmamıştır.
- Hamilelik bölümündeki değerler yer tutucudur, tıbbi onaydan geçmemiştir.
- Dada Doğrula'daki iddialar ve Farklı Bakışlar'daki yayın adları **kurgusaldır**;
  gerçek kişi veya yayın organına görüş/iddia atfedilmemiştir.
- Haber görsellerinde `srcset` yoktur — türev boyutlar üretilmemiştir (yalnız
  logo için üretildi). Gerçek içerik geldiğinde görsel hattıyla çözülmelidir.
