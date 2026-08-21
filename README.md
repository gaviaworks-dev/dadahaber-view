# Dadahaber — arayüz prototipi

Dadahaber haber sitesinin yeni görünümü. **Statik prototip:** build adımı yok,
paket yöneticisi yok, backend yok. Dosyaları bir statik sunucudan servis etmek yeterli.

> **Bu bir yayın değildir.** Sayfalardaki haber metinleri, isimler, rakamlar ve
> görseller yer tutucudur. Hukuki metinler (KVKK, çerezler, kullanım şartları,
> aydınlatma metni) hukuk onayından geçmemiştir. Site `noindex` ve `robots.txt`
> ile arama motorlarına kapalıdır.

## Yayın

GitHub Pages · `main` dalı · kök dizin
→ https://gaviaworks-dev.github.io/dadahaber-view/

## Sürümler

| Dal | Ne |
|---|---|
| `main` | Yayımlanan sürüm. Pages buradan servis eder. |
| `v1` | R8 sonundaki hâlin donmuş kopyası. Silinmez. |
| `v2` | Üzerine inşa edilen çalışma dalı. Hazır olunca `main`'e birleştirilir. |

`v1`'i sonradan görüntülemek için:

```bash
git checkout v1
python3 -m http.server 8765     # → http://localhost:8765/
```

`v2` yayına geçtiğinde `v1`'in bir kopyası `main` içinde `/v1/` klasörüne
konulup `…/dadahaber-view/v1/` adresinden kalıcı olarak erişilebilir yapılabilir
(site göreli yol kullanır, kopya kendi içinde tutarlı çalışır).

## Yerel çalıştırma

```bash
python3 -m http.server 8765
# → http://localhost:8765/
```

`file://` ile açma — göreli yollar ve `fetch` çağrıları çalışmaz.

## Yapı

```
*.html                       67 sayfa (referans üçlü: index · haber-liste · haber-detay)
assets/css/theme/
  demo-six.min.css           vendor tema — DOKUNULMAZ
  custom.min.css             tüm özel CSS. YALNIZCA dosyanın SONUNA eklenir.
assets/js/dh-*.js            kendi yazdığımız vanilla JS bileşenleri
assets/fonts/                self-host fontlar
docs/HANDOFF.md              oturum devri notu — yeni oturumda ÖNCE bunu oku
docs/YAYILIM.md              sayfa yayılım fazı brifingi
```

## Değişmez kurallar

1. `demo-six.min.css` **vendor'dur, dokunulmaz.** Her şey `custom.min.css`'ten
   override edilir ve **yalnızca dosyanın sonuna eklenir.**
2. **Yeni kütüphane eklenmez.** Swiper, native scroll-snap ve vanilla JS yeter.
3. `text-bg-primary` utility'si **kullanılmaz** — vendor'da bayat yeşil değerde.
4. Site tamamen **Türkçe**; İngilizce yer tutucu metin bırakılmaz.
5. **Değiştirmeden önce ölç.** Tahminle düzenleme yapılmaz.

## Bilinen açık konular

- **Gilroy ticari bir fonttur** (Radomir Tinkov / MyFonts) ve açık lisansı yoktur.
  Alan adı bazlı web font lisansının `dadahaber.com` için ayrı kapsam gerektirip
  gerektirmediği teyit edilmemiştir.
- Tema demo görselleri satın alınan temaya aittir.
- Kulüp armaları ve oyuncu adları kurgusaldır; gerçek marka kullanılmamıştır.
- Hamilelik bölümündeki değerler yer tutucudur, tıbbi onaydan geçmemiştir.
- Haber görsellerinde `srcset` yoktur — türev boyutlar üretilmemiştir (yalnız
  logo için üretildi). Gerçek içerik geldiğinde görsel hattıyla çözülmelidir.
