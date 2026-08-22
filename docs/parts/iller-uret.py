# -*- coding: utf-8 -*-
"""iller.html — 81 il, şematik Türkiye ızgarası üzerinden.

gundem.html#iller bir çapa bölümüydü; kendi sayfasına çıktı.
Izgara veri-harita.html'deki .dh-tr81 kalıbı: dokuza dokuz, plaka
sırasıyla. GERÇEK COĞRAFİ SINIR GÖSTERMEZ — sayfada da böyle yazıyor.

Seçici için yeni JS yazılmadı: assets/js/v2/dh-bolge.js sözleşmesi
(seç -> künye + liste değişsin) burada il için kullanılıyor.
"""
import json, os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)
sys.path.insert(0, os.path.join(kok, "docs", "parts"))
from sayfa_basligi import basli
SABLON = "docs/parts/sayfa-sablon.html"
HEDEF = "iller.html"

ILLER = """Adana Adıyaman Afyonkarahisar Ağrı Amasya Ankara Antalya Artvin Aydın Balıkesir
Bilecik Bingöl Bitlis Bolu Burdur Bursa Çanakkale Çankırı Çorum Denizli
Diyarbakır Edirne Elazığ Erzincan Erzurum Eskişehir Gaziantep Giresun Gümüşhane Hakkâri
Hatay Isparta Mersin İstanbul İzmir Kars Kastamonu Kayseri Kırklareli Kırşehir
Kocaeli Konya Kütahya Malatya Manisa Kahramanmaraş Mardin Muğla Muş Nevşehir
Niğde Ordu Rize Sakarya Samsun Siirt Sinop Sivas Tekirdağ Tokat
Trabzon Tunceli Şanlıurfa Uşak Van Yozgat Zonguldak Aksaray Bayburt Karaman
Kırıkkale Batman Şırnak Bartın Ardahan Iğdır Yalova Karabük Kilis Osmaniye
Düzce""".split()

BOLGE = {
 "Marmara": "İstanbul Bursa Kocaeli Tekirdağ Balıkesir Çanakkale Edirne Kırklareli Sakarya Bilecik Yalova".split(),
 "Ege": "İzmir Manisa Aydın Denizli Muğla Afyonkarahisar Kütahya Uşak".split(),
 "Akdeniz": "Antalya Adana Mersin Hatay Isparta Burdur Kahramanmaraş Osmaniye".split(),
 "İç Anadolu": "Ankara Konya Kayseri Eskişehir Sivas Yozgat Aksaray Karaman Kırıkkale Kırşehir Nevşehir Niğde Çankırı".split(),
 "Karadeniz": ("Samsun Trabzon Ordu Rize Giresun Zonguldak Bolu Düzce Karabük Bartın Kastamonu "
               "Sinop Çorum Amasya Tokat Artvin Gümüşhane Bayburt").split(),
 "Doğu Anadolu": "Erzurum Van Malatya Elazığ Ağrı Kars Erzincan Bingöl Bitlis Hakkâri Muş Tunceli Ardahan Iğdır".split(),
 "Güneydoğu Anadolu": "Gaziantep Şanlıurfa Diyarbakır Mardin Batman Adıyaman Siirt Şırnak Kilis".split(),
}
IL_BOLGE = {il: b for b, ler in BOLGE.items() for il in ler}

MANSET = [
 ("Belediye meclisi {il}'de ulaşım tarifesini görüşüyor", "Komisyon raporu bu hafta oylanacak.", "YEREL YÖNETİM"),
 ("{il}'de okul servis ücretlerine düzenleme", "Yeni tarife eylülde yürürlüğe giriyor.", "EĞİTİM"),
 ("{il} çevre yolunda çalışma trafiği etkiliyor", "Alternatif güzergâh iki hafta kullanılacak.", "ULAŞIM"),
 ("{il}'de tarım destek başvuruları açıldı", "Başvurular ay sonuna kadar sürecek.", "TARIM"),
 ("{il} Valiliği hava durumu için uyarı yayımladı", "Sağanak beklentisi gece saatlerini kapsıyor.", "HAVA"),
 ("{il}'de konut kiralarında üç aylık gerileme", "Merkez ilçelerde ilan süresi kısaldı.", "KONUT"),
 ("{il} sanayi bölgesinde istihdam arttı", "Yeni tesis üç yüz kişilik kapasiteye ulaştı.", "EKONOMİ"),
 ("{il}'de kültür sezonu açılış programı belli oldu", "Program on gün sürecek.", "KÜLTÜR"),
 ("{il} hastanesinde yeni poliklinik hizmete girdi", "Randevular bu hafta açılıyor.", "SAĞLIK"),
]
G = "./assets/images/main/posts/img-%02d.jpg"

def kisalt(il):
    """Izgara kutusu 62px; sekiz karakterden uzun ad taşıyor.
    Tam ad her kutunun <title>'ında duruyor (fare ve ekran okuyucu görür)."""
    return il if len(il) <= 8 else il[:7] + "."

def anahtar(il):
    d = str.maketrans("çğıöşüÇĞİÖŞÜâ ", "cgiosucgiosua-")
    return il.translate(d).lower()

DATA = {"varsayilan": anahtar("İstanbul"), "bolgeler": {}}
for i, il in enumerate(ILLER):
    plaka = i + 1
    bol = IL_BOLGE.get(il, "—")
    haberler = []
    for j in range(3):
        b, o, e = MANSET[(i + j * 3) % len(MANSET)]
        haberler.append({
            "baslik": b.format(il=il), "ozet": o, "yer": il,
            "saat": "%02d:%02d" % (7 + (i + j) % 12, (i * 7 + j * 11) % 60),
            "etiket": e, "gorsel": G % (((i + j) % 10) + 1),
        })
    DATA["bolgeler"][anahtar(il)] = {
        "ad": il,
        "ozet": "%s bölgesinde yer alıyor. Plaka %02d. Yerel gündem, belediye kararları ve hava durumu bu sayfada." % (bol, plaka),
        "kapsam": "%s · Plaka %02d · %d haber" % (bol, plaka, 40 + (i * 13) % 220),
        "haberler": haberler,
    }

# --- şematik ızgara (9x9, plaka sırasıyla) ---
KUTU, BOSLUK = 62, 6
def izgara():
    o = ['              <svg class="dh-tr81 dh-tr81--sec" viewBox="0 0 606 606" role="group"\n'
         '                aria-labelledby="dhIller-t dhIller-d" preserveAspectRatio="xMidYMid meet">\n'
         '                <title id="dhIller-t">Şematik Türkiye ızgarası — 81 il</title>\n'
         '                <desc id="dhIller-d">81 il, dokuza dokuz şematik ızgarada plaka sırasıyla dizilmiştir. '
         'Gerçek coğrafi sınır göstermez. Bir kutuya tıklayın, o ilin gündemi aşağıda açılsın.</desc>\n']
    for i, il in enumerate(ILLER):
        r, c = divmod(i, 9)
        x, y = c * (KUTU + BOSLUK), r * (KUTU + BOSLUK)
        o.append('                <g class="dh-tr81__c" role="radio" aria-checked="false" tabindex="-1" '
                 'data-dh-bolge-sec="%s" data-bolge="%s"><title>%s (%02d)</title>'
                 '<rect x="%d" y="%d" width="%d" height="%d" rx="6" ry="6" class="dh-tr81__box"/>'
                 '<text class="dh-tr81__no" x="%d" y="%d" text-anchor="middle">%02d</text>'
                 '<text class="dh-tr81__lv" x="%d" y="%d" text-anchor="middle">%s</text></g>\n'
                 % (anahtar(il), IL_BOLGE.get(il, ""), il, i + 1,
                    x, y, KUTU, KUTU, x + KUTU // 2, y + 26, i + 1,
                    x + KUTU // 2, y + 46, kisalt(il)))
    o.append('              </svg>\n')
    return "".join(o)

g = []; w = g.append
w(basli("Gündem", "81 İl",
        "Bir il seçin: o ilin bölgesi, plakası ve son yerel gündemi aşağıda açılsın. "
        "Izgara plaka sırasına göre dizilidir, gerçek coğrafi sınır göstermez.",
        [("Gündem", "gundem.html"), ("81 İl", None)], "img-06.jpg", "50% 52%",
        ["<b>81</b> il", "<b>7</b> bölge"]))
w('        <section class="section panel" id="harita" aria-labelledby="dh-iller-t">\n')
w('          <div class="container max-w-xl">\n')
w('            <div class="section-header panel dh-secbar">\n')
w('              <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-iller-t">Şematik Türkiye Izgarası</h2>\n')
w('              <div class="dh-secbar__tools"><span class="dh-nwstamp">'
  '<i class="fas fa-map-location-dot" aria-hidden="true"></i> 81 il · 7 bölge</span>\n')
w('                <a href="gundem.html" class="dh-secbar__all">Gündeme dön</a></div>\n')
w('            </div>\n')
w('            <div class="dh-iller dh-bolge dh-bolge--iller" data-dh-bolge>\n')
w('              <div class="dh-iller__map" role="radiogroup" aria-label="İl seçimi">\n')
w(izgara())
w('              </div>\n')
w('              <div class="dh-iller__yan">\n')
w('                <div class="dh-bolge__id">\n')
w('                  <h3 class="dh-bolge__ad" data-dh-bolge-ad>İstanbul</h3>\n')
w('                  <p class="dh-bolge__ozet" data-dh-bolge-ozet></p>\n')
w('                  <span class="dh-bolge__kapsam" data-dh-bolge-kapsam></span>\n')
w('                </div>\n')
w('                <div class="dh-bolge__liste" data-dh-bolge-liste aria-live="polite"></div>\n')
w('              </div>\n')
w('            </div>\n')
w('            <p class="dh-nato__not"><i class="fas fa-circle-info" aria-hidden="true"></i> '
  'Izgara şematiktir; kutuların yeri plaka sırasına göredir, coğrafi konum değildir. '
  'Başlıklar ve sayılar prototip için üretilmiş yer tutuculardır.</p>\n')
w('          </div>\n        </section>\n\n')
w('    <script type="application/json" id="dh-bolge-data">\n')
w(json.dumps(DATA, ensure_ascii=False, separators=(",", ":")))
w('\n    </script>\n')
GOVDE = "".join(g)

s = open(SABLON, encoding="utf-8").read()
s = s.replace("<title>SAYFA BAŞLIĞI — Dada Haber</title>", "<title>81 İl — Dada Haber</title>")
if 'data-dh-cat=""' in s:
    s = s.replace('data-dh-cat=""', 'data-dh-cat="gundem"', 1)
m = re.search(r"[ \t]*<!-- ={10,} SAYFA GÖVDESİ BURAYA ={10,}.*?={10,} -->\n", s, re.S)
if not m: sys.exit("HATA: gövde yuvası yok")
s = s[:m.start()] + GOVDE + s[m.end():]
m2 = re.search(r'[ \t]*<script defer src="\./assets/js/app\.js"></script>[ \t]*\n', s)
s = s[:m2.end()] + '    <script defer src="./assets/js/v2/dh-bolge.js"></script>\n' + s[m2.end():]
open(HEDEF, "w", encoding="utf-8").write(s)
print("%s yazıldı (%d satır, %d il, JSON %.0f KB)"
      % (HEDEF, len(s.splitlines()), len(ILLER), len(json.dumps(DATA, ensure_ascii=False)) / 1024))
