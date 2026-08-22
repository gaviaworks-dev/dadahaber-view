# -*- coding: utf-8 -*-
"""hava-durumu.html — 81 il · ilçe seçimli detaylı hava durumu sayfası.

Talep (revize-2.docx, madde 1): "Hava durumu sayfasını ayrı bir sayfada
gösterelim. Detaylı bir sayfalandırma oluşturabiliriz. Kurumsal yapımıza
uygun şekilde il ve ilçe seçerek gösterim yapabiliriz."
Örnek verilenler: ventusky.com ve mgm.gov.tr/tahmin/il-ve-ilceler.

ÖNCE: "Hava Durumu" bağlantısı veri-harita.html#hava çapasına gidiyordu —
bir veri sayfasının içindeki tek bölüm. Artık kendi sayfası var.

KALIP: il seçimi iller.html'deki şematik ızgaranın (.dh-tr81) aynısı;
yeni bir seçim dili icat edilmedi. İlçe seçimi çip şeridi (.dh-hv__ilce).
Sayfa başlığı .dh-ph--photo standardı (sayfa_basligi.basli).

PROTOTİP SINIRI: gerçek meteoroloji verisi yok. Sayılar il indisinden
deterministik üretiliyor; ilçe seçimi merkeze göre küçük bir sapma
uyguluyor (ayrı ilçe verisi tutulmuyor). Sayfa bunu görünür biçimde
yazıyor ve resmî kaynak olarak MGM'yi işaret ediyor.

Yeniden üret:  python3 docs/parts/hava-uret.py
"""
import json, os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)
sys.path.insert(0, os.path.join(kok, "docs", "parts"))
from sayfa_basligi import basli
from iller_veri import ILLER, IL_BOLGE, anahtar, kisalt   # tek kaynak

SABLON = "docs/parts/sayfa-sablon.html"
HEDEF = "hava-durumu.html"

DURUM = [
    ("Az bulutlu", "fa-cloud-sun"), ("Parçalı bulutlu", "fa-cloud-sun"),
    ("Açık", "fa-sun"), ("Çok bulutlu", "fa-cloud"),
    ("Sağanak yağışlı", "fa-cloud-showers-heavy"), ("Hafif yağmurlu", "fa-cloud-rain"),
    ("Puslu", "fa-smog"), ("Rüzgârlı", "fa-wind"),
]
GUN = ["Bugün", "Yarın", "Cumartesi", "Pazar", "Pazartesi", "Salı", "Çarşamba"]
TARIH = ["22 Ağu", "23 Ağu", "24 Ağu", "25 Ağu", "26 Ağu", "27 Ağu", "28 Ağu"]

# İlçe adları prototip yer tutucudur; her il için merkez + yedi ilçe.
ILCE_EK = ["Merkez", "Kuzey", "Güney", "Sahil", "Ova", "Yayla", "Sanayi", "Üniversite"]

UYARI = [
    None, None, None,
    {"seviye": "sari", "etiket": "SARI KOD",
     "metin": "Kuvvetli sağanak bekleniyor; ani su baskınlarına karşı dikkatli olun."},
    None, None,
    {"seviye": "turuncu", "etiket": "TURUNCU KOD",
     "metin": "Fırtına ve dolu riski var; açık alanda bulunmaktan kaçının."},
    None,
]

DATA = {"varsayilan": anahtar("İstanbul"), "iller": {}}
for i, il in enumerate(ILLER):
    plaka = i + 1
    taban = 18 + (i * 7) % 16                     # 18–33 °C
    d, ikon = DURUM[i % len(DURUM)]

    saatlik = []
    for h in range(12):
        saat = (9 + h * 2) % 24
        dd, di = DURUM[(i + h) % len(DURUM)]
        saatlik.append({
            "saat": "%02d.00" % saat,
            "derece": taban + ((h * 3) % 7) - 3,
            "yagis": (i * 5 + h * 11) % 70,
            "ikon": di,
        })

    gunluk = []
    for g in range(7):
        gd, gi = DURUM[(i + g * 2) % len(DURUM)]
        gmax = taban + ((g * 5) % 8) - 2
        gunluk.append({
            "gun": GUN[g], "tarih": TARIH[g], "durum": gd, "ikon": gi,
            "yagis": (i * 3 + g * 17) % 80,
            "ruzgar": 8 + (i + g * 4) % 28,
            "max": gmax, "min": gmax - (6 + (i + g) % 5),
        })

    DATA["iller"][anahtar(il)] = {
        "ad": il,
        "bolge": IL_BOLGE.get(il, "—"),
        "plaka": "%02d" % plaka,
        "ilceler": [(il + " " + e if e != "Merkez" else il + " Merkez") for e in ILCE_EK],
        "simdi": {
            "derece": taban, "durum": d, "ikon": ikon,
            "hissedilen": taban + ((i % 5) - 2),
            "nem": 38 + (i * 3) % 50,
            "ruzgar": 6 + (i * 5) % 30, "yon": i % 8,
            "basinc": 1002 + (i % 22),
            "gorus": 6 + (i % 15),
            "yagis": (i * 7) % 75,
            "dogus": "0%d.%02d" % (6 + i % 2, (i * 3) % 60),
            "batis": "%d.%02d" % (19 + i % 2, (i * 7) % 60),
            "guncel": "22 Ağustos 2026, %02d.00 itibarıyla" % (6 + (i % 12)),
        },
        "saatlik": saatlik,
        "gunluk": gunluk,
        "uyari": UYARI[i % len(UYARI)],
    }

# --- şematik ızgara: iller.html ile aynı kalıp -----------------------------
KUTU, BOSLUK = 62, 6


def izgara():
    o = ['              <svg class="dh-tr81 dh-tr81--sec" viewBox="0 0 606 606" role="radiogroup"\n'
         '                aria-labelledby="dhHava-t dhHava-d" preserveAspectRatio="xMidYMid meet">\n'
         '                <title id="dhHava-t">Şematik Türkiye ızgarası — 81 il</title>\n'
         '                <desc id="dhHava-d">81 il, dokuza dokuz şematik ızgarada plaka sırasıyla '
         'dizilmiştir. Gerçek coğrafi sınır göstermez. Bir kutuya tıklayın, o ilin hava durumu '
         'yanda açılsın.</desc>\n']
    for i, il in enumerate(ILLER):
        r, c = divmod(i, 9)
        x, y = c * (KUTU + BOSLUK), r * (KUTU + BOSLUK)
        o.append('                <g class="dh-tr81__c" role="radio" aria-checked="false" tabindex="-1" '
                 'data-dh-hava-sec="%s" data-ad="%s" data-plaka="%d"><title>%s (%02d)</title>'
                 '<rect x="%d" y="%d" width="%d" height="%d" rx="6" ry="6" class="dh-tr81__box"/>'
                 '<text class="dh-tr81__no" x="%d" y="%d" text-anchor="middle">%02d</text>'
                 '<text class="dh-tr81__lv" x="%d" y="%d" text-anchor="middle">%s</text></g>\n'
                 % (anahtar(il), il.lower(), i + 1, il, i + 1,
                    x, y, KUTU, KUTU, x + KUTU // 2, y + 26, i + 1,
                    x + KUTU // 2, y + 46, kisalt(il)))
    o.append('              </svg>\n')
    return "".join(o)


HUCRE = [
    ("hissedilen", "Hissedilen", "fa-temperature-half"),
    ("nem", "Nem", "fa-droplet"),
    ("ruzgar", "Rüzgâr", "fa-wind"),
    ("yagis", "Yağış ihtimali", "fa-umbrella"),
    ("basinc", "Basınç", "fa-gauge-high"),
    ("gorus", "Görüş", "fa-eye"),
    ("dogus", "Gün doğumu", "fa-sun"),
    ("batis", "Gün batımı", "fa-moon"),
]

g = []
w = g.append
w(basli("Anlık", "Hava Durumu",
        "İl ve ilçe seçin: o noktanın anlık değerleri, saatlik seyri ve yedi günlük "
        "tahmini aşağıda açılsın. Resmî uyarılar için Meteoroloji Genel Müdürlüğü esastır.",
        [("Anlık", "anlik.html"), ("Hava Durumu", None)], "img-11.jpg", "50% 44%",
        ["<b>81</b> il", "<b>7</b> günlük tahmin"]))

w('        <section class="section panel dh-hv" id="hava" aria-labelledby="dh-hava-t" data-dh-hava>\n')
w('          <div class="container max-w-xl">\n')
w('            <div class="section-header panel dh-secbar">\n')
w('              <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-hava-t">İl ve İlçe Seçimi</h2>\n')
w('              <div class="dh-secbar__tools">\n')
w('                <span class="dh-nwstamp"><i class="fas fa-cloud-sun" aria-hidden="true"></i> '
  '<span data-dh-hava-sayac>81</span> il listeleniyor</span>\n')
w('                <a href="veri-harita.html#hava" class="dh-secbar__all">Veri &amp; Harita</a>\n')
w('              </div>\n')
w('            </div>\n')

w('            <div class="dh-hv__grid">\n')
# --- sol: ızgara + arama ---
w('              <div class="dh-hv__map">\n')
w('                <label class="dh-hv__ara">\n')
w('                  <span class="sr-only">İl ara</span>\n')
w('                  <i class="fas fa-magnifying-glass" aria-hidden="true"></i>\n')
w('                  <input type="search" placeholder="İl adı ya da plaka yaz — örn. Trabzon, 61" '
  'data-dh-hava-ara autocomplete="off">\n')
w('                </label>\n')
w(izgara())
w('                <p class="dh-hv__not"><i class="fas fa-circle-info" aria-hidden="true"></i> '
  'Izgara şematiktir; kutuların yeri plaka sırasına göredir, coğrafi konum değildir.</p>\n')
w('              </div>\n')

# --- sağ: seçili il paneli ---
w('              <div class="dh-hv__yan">\n')
w('                <div class="dh-hv__ust">\n')
w('                  <span class="dh-hv__kapsam" data-dh-hava-kapsam></span>\n')
w('                  <h3 class="dh-hv__ad" data-dh-hava-ad>İstanbul</h3>\n')
w('                  <span class="dh-hv__ilceAd" data-dh-hava-ilcead></span>\n')
w('                </div>\n')

w('                <div class="dh-hv__ilceler" role="radiogroup" aria-label="İlçe seçimi" '
  'data-dh-hava-ilceler></div>\n')

w('                <div class="dh-hv__uyari" data-dh-hava-uyari hidden>\n')
w('                  <span class="dh-hv__ulv" data-dh-hava-uyari-lv></span>\n')
w('                  <p class="dh-hv__utx" data-dh-hava-uyari-tx></p>\n')
w('                </div>\n')

w('                <div class="dh-hv__simdi">\n')
w('                  <div class="dh-hv__derece"><b data-dh-hava-derece>24°</b>'
  '<span data-dh-hava-durum>Az bulutlu</span></div>\n')
w('                  <dl class="dh-hv__cells">\n')
for anah, ad, ik in HUCRE:
    w('                    <div class="dh-hv__cell"><dt><i class="fas %s" aria-hidden="true"></i> %s</dt>'
      '<dd data-dh-hava-%s>—</dd></div>\n' % (ik, ad, anah))
w('                  </dl>\n')
w('                  <span class="dh-hv__guncel"><i class="fas fa-rotate" aria-hidden="true"></i> '
  '<span data-dh-hava-guncel></span></span>\n')
w('                </div>\n')
w('              </div>\n')
w('            </div>\n')
w('          </div>\n        </section>\n\n')

# --- saatlik ---
# REVİZE (22 Ağustos akşamı): "başlangıç sayfası beyaz, sonra şeffaf
# şeklinde devam edecek bir zebra modu ile yapalım."
# Şerit kalıbı bırakıldı — kendi zeminini dayattığı için zebra sırasına
# giremiyordu. Artık düz bölüm: §16 sırayla beyaz/şeffaf veriyor.
w('        <section class="section panel dh-hv__saatsec" id="saatlik" '
  'aria-labelledby="dh-hvs-t">\n')
w('          <div class="section-outer panel">\n')
w('            <div class="container max-w-xl">\n')
w('              <div class="section-header panel dh-secbar">\n')
w('                <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-hvs-t">'
  '<span data-dh-hava-ad2>İstanbul</span> · Saatlik Seyir</h2>\n')
w('                <div class="dh-secbar__tools"><span class="dh-nwstamp">'
  '<i class="fas fa-clock" aria-hidden="true"></i> '
  '<span data-dh-hava-ilcead2></span> · 24 saat</span></div>\n')
w('              </div>\n')
w('              <p class="dh-nwintro">Seçtiğiniz nokta için sıcaklık ve yağış ihtimalinin gün içi seyri. '
  'Şerit yatay kaydırılabilir.</p>\n')
w('              <ul class="dh-hv__saatlik" data-dh-hava-saatlik></ul>\n')
w('            </div>\n')
w('          </div>\n        </section>\n\n')

# --- 7 gün ---
w('        <section class="section panel" id="gunluk" aria-labelledby="dh-hvg-t">\n')
w('          <div class="container max-w-xl">\n')
w('            <div class="section-header panel dh-secbar">\n')
w('              <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-hvg-t">'
  '<span data-dh-hava-ad3>İstanbul</span> · Yedi Günlük Tahmin</h2>\n')
w('              <div class="dh-secbar__tools"><a href="anlik.html" class="dh-secbar__all">Anlık Merkezi</a></div>\n')
w('            </div>\n')
w('            <div class="dh-hv__tablo" tabindex="0" role="region" aria-label="Yedi günlük tahmin tablosu">\n')
w('              <table class="dh-hv__t">\n')
w('                <caption class="sr-only">Seçili nokta için yedi günlük hava tahmini</caption>\n')
w('                <thead><tr><th scope="col">Gün</th><th scope="col">Durum</th>'
  '<th scope="col">Yağış</th><th scope="col">Rüzgâr</th>'
  '<th scope="col">En yüksek</th><th scope="col">En düşük</th></tr></thead>\n')
w('                <tbody data-dh-hava-gunluk></tbody>\n')
w('              </table>\n')
w('            </div>\n')
w('            <p class="dh-hv__kaynak"><i class="fas fa-triangle-exclamation" aria-hidden="true"></i> '
  '<b>Prototip verisi.</b> Bu sayfadaki sayılar arayüz denemesi için üretilmiştir; gerçek ölçüm '
  'değildir. Resmî tahmin ve uyarılar için '
  '<a href="https://www.mgm.gov.tr/" rel="noopener noreferrer" target="_blank">Meteoroloji Genel '
  'Müdürlüğü</a> esastır.</p>\n')
w('          </div>\n        </section>\n\n')

w('    <script type="application/json" id="dh-hava-data">\n')
w(json.dumps(DATA, ensure_ascii=False, separators=(",", ":")))
w('\n    </script>\n')
GOVDE = "".join(g)

s = open(SABLON, encoding="utf-8").read()
s = s.replace("<title>SAYFA BAŞLIĞI — Dada Haber</title>", "<title>Hava Durumu — Dada Haber</title>")
if 'data-dh-cat=""' in s:
    s = s.replace('data-dh-cat=""', 'data-dh-cat="anlik"', 1)
m = re.search(r"[ \t]*<!-- ={10,} SAYFA GÖVDESİ BURAYA ={10,}.*?={10,} -->\n", s, re.S)
if not m:
    sys.exit("HATA: gövde yuvası yok")
s = s[:m.start()] + GOVDE + s[m.end():]
m2 = re.search(r'[ \t]*<script defer src="\./assets/js/app\.js"></script>[ \t]*\n', s)
s = s[:m2.end()] + '    <script defer src="./assets/js/v2/dh-hava.js"></script>\n' + s[m2.end():]
open(HEDEF, "w", encoding="utf-8").write(s)
print("%s yazıldı (%d satır, %d il, JSON %.0f KB)"
      % (HEDEF, len(s.splitlines()), len(ILLER), len(json.dumps(DATA, ensure_ascii=False)) / 1024))
