# -*- coding: utf-8 -*-
"""trafik-ulasim.html — şehir seçimli trafik ve ulaşım sayfası.

Talep (22 Ağustos gecesi): "Burada sadece İstanbul oluşturulmuş, bu doğru
değil. Ankara'daki kişi bunu nasıl kullanacak? Kullanım için iyi değil,
bunu bir düzenleyelim; ek özellik ekleme durumu varsa ekleyelim."

ÖNCE: sayfa İstanbul'a gömülüydü — "İstanbul trafik yoğunluğu",
"Kuzey Marmara Otoyolu" gibi başlıklar sabit metindi.
SONRA: on şehir çipten seçiliyor; yoğunluk göstergesi, en sıkışık
güzergâh ve dört ulaşım satırı seçilen şehre göre yeniden yazılıyor.
EK ÖZELLİK: "şehrim yap" — seçim localStorage'a yazılıyor, sonraki
ziyarette o şehir açılıyor.

Sayısal değerler prototiptir; şehir indisinden deterministik üretilir.

Yeniden üret:  python3 docs/parts/trafik-uret.py
"""
import json, os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)
HEDEF = "trafik-ulasim.html"

# (anahtar, ad, bölge, nüfus, en sıkışık güzergâh, ana yol, raylı sistem, deniz, hava)
SEHIR = [
 ("istanbul", "İstanbul", "Marmara", "15,9 mn",
  "E-5 Bakırköy — Zeytinburnu",
  ("Kuzey Marmara Otoyolu", "Hafif yoğunluk; gişe çıkışlarında kısa kuyruk."),
  ("Marmaray · Metro", "Marmaray'da 4 dakikalık gecikme, metro hatları normal."),
  ("Şehir hatları", "Boğaz hattında lodos nedeniyle iki sefer iptal."),
  ("İstanbul · Sabiha Gökçen", "Ortalama gecikme 6 dakika. Kapanan pist yok.")),
 ("ankara", "Ankara", "İç Anadolu", "5,8 mn",
  "Eskişehir Yolu — Söğütözü kavşağı",
  ("Çevre yolu", "Konya Yolu bağlantısında bakım çalışması, tek şerit kapalı."),
  ("Ankaray · Metro", "M4 hattında sefer sıklığı artırıldı, aksama yok."),
  ("—", "Şehirde deniz ulaşımı bulunmuyor."),
  ("Esenboğa", "Ortalama gecikme 4 dakika. Sis uyarısı yok.")),
 ("izmir", "İzmir", "Ege", "4,5 mn",
  "Mustafa Kemal Sahil Bulvarı",
  ("İzmir Çevre Yolu", "Trafik akıcı; Gaziemir çıkışında kısa yavaşlama."),
  ("İZBAN · Metro", "İZBAN'da 6 dakikalık gecikme, metro normal."),
  ("Vapur hatları", "Karşıyaka — Konak seferleri normal."),
  ("Adnan Menderes", "Gecikme yok.")),
 ("bursa", "Bursa", "Marmara", "3,2 mn",
  "Ankara Yolu — Ovaakça",
  ("Bursa çevre yolu", "İnegöl yönünde yol çalışması sürüyor."),
  ("Bursaray", "Seferler normal."),
  ("Mudanya hattı", "Deniz otobüsü seferleri normal."),
  ("Yenişehir", "Gecikme yok.")),
 ("antalya", "Antalya", "Akdeniz", "2,7 mn",
  "Konyaaltı — Lara aksı",
  ("D-400 karayolu", "Turizm sezonu yoğunluğu; Kemer yönü sıkışık."),
  ("Antray", "Seferler normal."),
  ("Kaleiçi marina", "Tur tekneleri normal çalışıyor."),
  ("Antalya", "Yoğun tarifede ortalama 9 dakika gecikme.")),
 ("adana", "Adana", "Akdeniz", "2,3 mn",
  "Turhan Cemal Beriker Bulvarı",
  ("Tarsus — Adana — Gaziantep otoyolu", "Trafik akıcı; Pozantı bakımı tamamlandı."),
  ("Adana Metro", "Seferler normal."),
  ("—", "Şehirde deniz ulaşımı bulunmuyor."),
  ("Çukurova", "Gecikme yok.")),
 ("konya", "Konya", "İç Anadolu", "2,3 mn",
  "Yeni İstanbul Caddesi",
  ("Konya — Ankara yolu", "Yol çalışması yok, akış normal."),
  ("Tramvay", "Seferler normal."),
  ("—", "Şehirde deniz ulaşımı bulunmuyor."),
  ("Konya", "Gecikme yok.")),
 ("gaziantep", "Gaziantep", "Güneydoğu Anadolu", "2,1 mn",
  "Şehitkâmil — Karataş bağlantısı",
  ("Şanlıurfa yolu", "Ağır taşıt yoğunluğu; sağ şerit yavaş."),
  ("Gaziray", "Seferler normal."),
  ("—", "Şehirde deniz ulaşımı bulunmuyor."),
  ("Oğuzeli", "Gecikme yok.")),
 ("trabzon", "Trabzon", "Karadeniz", "0,8 mn",
  "Sahil yolu — Değirmendere",
  ("Karadeniz sahil yolu", "Sağanak nedeniyle iki noktada su birikintisi."),
  ("—", "Şehirde raylı sistem bulunmuyor."),
  ("Liman", "Yolcu seferleri normal."),
  ("Trabzon", "Rüzgâr nedeniyle ortalama 12 dakika gecikme.")),
 ("samsun", "Samsun", "Karadeniz", "1,4 mn",
  "Atatürk Bulvarı — sahil kesimi",
  ("Samsun — Ordu yolu", "Trafik akıcı."),
  ("Samulaş tramvay", "Seferler normal."),
  ("Liman", "Yük trafiği normal."),
  ("Çarşamba", "Gecikme yok.")),
]

LV = ["normal", "uyari", "kritik"]
ETIKET = {"normal": "NORMAL", "uyari": "DİKKAT", "kritik": "YOĞUN"}
IKON = ["fa-road", "fa-train-subway", "fa-ship", "fa-plane"]
BASLIK = ["Ana güzergâh", "Raylı sistem", "Deniz ulaşımı", "Hava ulaşımı"]

DATA = {"varsayilan": "istanbul", "sehirler": {}}
for i, (k, ad, bolge, nufus, sikisik, yol, ray, deniz, hava) in enumerate(SEHIR):
    yogunluk = 34 + (i * 17) % 55           # 34–88
    satirlar = []
    for j, (b, veri) in enumerate(zip(BASLIK, [yol, ray, deniz, hava])):
        lv = LV[(i + j) % 3] if veri[0] != "—" else "normal"
        satirlar.append({
            "ad": veri[0] if veri[0] != "—" else b + " · yok",
            "aciklama": veri[1],
            "lv": lv, "etiket": ETIKET[lv], "ikon": IKON[j],
        })
    DATA["sehirler"][k] = {
        "ad": ad, "bolge": bolge, "nufus": nufus + " nüfus",
        "saat": "%02d.%02d" % (8 + i % 10, (i * 13) % 60),
        "yogunluk": yogunluk, "sikisik": sikisik, "satirlar": satirlar,
    }

o = []
w = o.append
w('      <div class="container max-w-xl">\n')
w('        <div class="section-header panel dh-secbar">\n')
w('          <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-trafik-t">Trafik ve Ulaşım</h2>\n')
w('          <div class="dh-secbar__tools">\n')
w('            <span class="dh-nwstamp"><i class="fas fa-map-marker-alt" aria-hidden="true"></i> '
  '<span data-dh-trafik-kapsam></span></span>\n')
w('            <a href="veri-harita.html" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Şehir Verileri</a>\n')
w('          </div>\n')
w('        </div>\n')

w('        <div class="dh-trf" data-dh-trafik>\n')
w('          <div class="dh-trf__cips" role="radiogroup" aria-label="Şehir seçimi">\n')
for k, ad, *_ in SEHIR:
    w('            <button type="button" class="dh-trf__cip" role="radio" aria-checked="false" '
      'data-dh-trafik-sec="%s">%s</button>\n' % (k, ad))
w('          </div>\n')

w('          <div class="dh-trf__ust">\n')
w('            <div class="dh-trf__id">\n')
w('              <h3 class="dh-trf__ad" data-dh-trafik-ad>İstanbul</h3>\n')
w('              <button type="button" class="dh-trf__kaydet" data-dh-trafik-kaydet>Şehrim yap</button>\n')
w('            </div>\n')
w('            <div class="dh-trf__olcu">\n')
w('              <span class="dh-trf__lbl">Trafik yoğunluğu</span>\n')
w('              <div class="dh-trf__bar" data-lv="normal"><span data-dh-trafik-bar></span></div>\n')
w('              <b class="dh-trf__yuzde" data-dh-trafik-yogunluk>%0</b>\n')
w('            </div>\n')
w('            <p class="dh-trf__sik"><i class="fas fa-triangle-exclamation" aria-hidden="true"></i> '
  'En sıkışık güzergâh: <b data-dh-trafik-sikisik></b></p>\n')
w('          </div>\n')

w('          <div class="dh-nwstat dh-nwstat--trafik">\n')
w('            <ul class="dh-nwstat__rows" data-dh-trafik-satirlar aria-live="polite"></ul>\n')
w('          </div>\n')
w('          <p class="dh-trf__not"><i class="fas fa-circle-info" aria-hidden="true"></i> '
  'Değerler prototip için üretilmiştir; gerçek ölçüm değildir. Resmî bilgi için '
  'ilgili belediye ve karayolları duyurularını esas alın.</p>\n')
w('        </div>\n')
w('      </div>')
GOVDE = "".join(o)

# --- anlik-uret.py içindeki gövdeyi değiştir -------------------------------
p = "docs/parts/anlik-uret.py"
s = open(p, encoding="utf-8").read()
bas = s.index('GOVDE["trafik"] = """')
ic = bas + len('GOVDE["trafik"] = """')
son = s.index('"""', ic)
s = s[:ic] + GOVDE + s[son:]
# veri betiği + JS bağlantısı EK'e
if 'dh-trafik-data' not in s:
    ek = ('\n\n    <script type="application/json" id="dh-trafik-data">\n'
          + json.dumps(DATA, ensure_ascii=False, separators=(",", ":"))
          + '\n    </script>')
    i2 = s.index('EK["trafik"] = """')
    j2 = s.index('"""', i2 + len('EK["trafik"] = """'))
    s = s[:j2] + ek + s[j2:]
open(p, "w", encoding="utf-8").write(s)
print("anlik-uret.py güncellendi (%d şehir)" % len(SEHIR))
