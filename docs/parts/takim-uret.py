# -*- coding: utf-8 -*-
"""takim.html — dal + lig süzgeçli, aramalı takım dizini.

Talep (22 Ağustos akşamı): "Takım sayfasında futbol, basketbol, voleybol
gibi güzel bir ayrıştırma var ama bu kadar az bir takım yok. Sadece Süper
Lig değil, alt lig takımları da var. Burada bir filtreleme yapısına
ihtiyacımız var. Detaylı bir şekilde takımları gösterecek liste sayfası."

ÖNCE: dört sabit bölüm (Futbol · Basketbol · Voleybol · Formula 1),
yalnız en üst lig, süzgeç yok.
SONRA: tek ızgara + iki kademeli süzgeç (dal → lig) + ad araması.
Lig listesi dala göre daralır; sayaçlar süzgeçle birlikte güncellenir.

Takım adları prototip verisidir; gerçek kadro/lig bilgisi değildir.
Sayfa bunu görünür biçimde yazar.

Yeniden üret:  python3 docs/parts/takim-uret.py
"""
import json, os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)
sys.path.insert(0, os.path.join(kok, "docs", "parts"))
from sayfa_basligi import basli

SABLON = "docs/parts/sayfa-sablon.html"
HEDEF = "takim.html"

DAL = [
    ("futbol", "Futbol", "fa-futbol"),
    ("basketbol", "Basketbol", "fa-basketball-ball"),
    ("voleybol", "Voleybol", "fa-volleyball-ball"),
    ("f1", "Formula 1", "fa-flag-checkered"),
]

# (dal, lig, [takımlar])  — sayfaya özel prototip verisi
VERI = [
 ("futbol", "Trendyol Süper Lig", [
   "Galatasaray", "Fenerbahçe", "Beşiktaş", "Trabzonspor", "Başakşehir",
   "Kasımpaşa", "Samsunspor", "Eyüpspor", "Rizespor", "Antalyaspor",
   "Konyaspor", "Alanyaspor", "Göztepe", "Gaziantep FK", "Sivasspor",
   "Kayserispor", "Hatayspor", "Adana Demirspor"]),
 ("futbol", "Trendyol 1. Lig", [
   "Bandırmaspor", "Kocaelispor", "Erzurumspor", "Boluspor", "Sakaryaspor",
   "Manisa FK", "Ümraniyespor", "Keçiörengücü", "Şanlıurfaspor", "Iğdır FK",
   "Amed Sportif", "Çorum FK", "Ahlatcı Çorum", "Adanaspor", "Pendikspor",
   "Fatih Karagümrük", "Yeni Malatyaspor", "Giresunspor"]),
 ("futbol", "2. Lig", [
   "Karacabey Belediyespor", "Isparta 32 Spor", "Zonguldak Kömürspor",
   "Kırklarelispor", "Nazilli Belediyespor", "Somaspor", "Bucaspor 1928",
   "Serik Belediyespor", "24Erzincanspor", "Van Spor FK", "Beyoğlu Yeni Çarşı",
   "Kastamonuspor", "Denizlispor", "Altınordu"]),
 ("futbol", "Kadın Süper Ligi", [
   "Galatasaray Kadın", "Fenerbahçe Kadın", "Beşiktaş Kadın",
   "Trabzonspor Kadın", "ABB Fomget", "Hakkarigücü", "Amed SK Kadın",
   "Ataşehir Belediyespor"]),
 ("basketbol", "Türkiye Sigorta Basketbol Süper Ligi", [
   "Anadolu Efes", "Fenerbahçe Beko", "Beşiktaş", "Galatasaray",
   "Türk Telekom", "Bahçeşehir Koleji", "Karşıyaka", "Merkezefendi",
   "Petkim Spor", "Manisa BBSK", "Bursaspor", "Tofaş",
   "Konyaspor Basketbol", "Samsunspor Basketbol", "Yukatel Merkezefendi",
   "Aliağa Petkim"]),
 ("basketbol", "TBL (1. Lig)", [
   "Sigortam.net İTÜ", "Kocaeli BŞB Kağıtspor", "Bornova Belediyesi",
   "Final Spor", "Sakarya Büyükşehir", "Mamak Belediyesi",
   "Balıkesir BŞB", "Antalyaspor Basketbol"]),
 ("basketbol", "Kadınlar Basketbol Süper Ligi", [
   "Fenerbahçe Opet", "Galatasaray Çağdaş", "Beşiktaş BOA",
   "ÇBK Mersin", "Emlak Konut", "Botaş", "Melikgazi Kayseri",
   "İzmit Belediyespor"]),
 ("voleybol", "Sultanlar Ligi", [
   "VakıfBank", "Fenerbahçe Opet", "Eczacıbaşı Dynavit", "Galatasaray Daikin",
   "Türk Hava Yolları", "Zeren Spor", "Beşiktaş Ayos", "Aydın BŞB",
   "Nilüfer Belediyespor", "Kuzeyboru", "Bahçelievler Belediyesi",
   "İlbank"]),
 ("voleybol", "Efeler Ligi", [
   "Ziraat Bankkart", "Halkbank", "Fenerbahçe Parolapara", "Arkas Spor",
   "Galatasaray HDI", "İstanbul BBSK", "Cizre Belediyespor",
   "Sorgun Belediyespor", "Altekma", "Develi Belediyespor"]),
 ("voleybol", "1. Lig", [
   "Beşiktaş Voleybol", "Afyon Belediye", "Bursa BŞB", "Solhan Spor",
   "Muratpaşa Belediyesi", "Gümüşhane Torul Gençlik"]),
 ("f1", "Formula 1", [
   "Red Bull Racing", "Mercedes-AMG", "Ferrari", "McLaren",
   "Aston Martin", "Alpine", "Williams", "RB", "Kick Sauber", "Haas"]),
]

LOGO = "./assets/images/demo-six/emblems/logo-%02d.svg"
DETAY = {
    "Galatasaray": "takim-galatasaray.html",
    "Fenerbahçe": "takim-fenerbahce.html",
    "Beşiktaş": "takim-besiktas.html",
    "Trabzonspor": "takim-trabzonspor.html",
}


def anahtar(t):
    d = str.maketrans("çğıöşüÇĞİÖŞÜâ .", "cgiosucgiosua--")
    return re.sub(r"-+", "-", t.translate(d).lower()).strip("-")


takimlar = []
i = 0
for dal, lig, ler in VERI:
    for t in ler:
        i += 1
        takimlar.append({
            "ad": t, "dal": dal, "lig": lig,
            "href": DETAY.get(t, "spor-takim-detay.html"),
            "logo": LOGO % ((i % 10) + 1),
            "ara": anahtar(t),
        })

LIGLER = []
for dal, lig, _ in VERI:
    if (dal, lig) not in LIGLER:
        LIGLER.append((dal, lig))

DAL_AD = {k: a for k, a, _ in DAL}

g = []
w = g.append
w(basli("Spor", "Takımlar",
        "Dal ve lig seçerek takım arayın. Liste futbol, basketbol, voleybol ve "
        "Formula 1 takımlarını; üst liglerin yanı sıra alt ligleri de kapsar.",
        [("Spor", "spor.html"), ("Takımlar", None)], "img-02.jpg", "50% 42%",
        ["<b>%d</b> takım" % len(takimlar), "<b>%d</b> lig" % len(LIGLER)]))

w('        <section class="section panel dh-tkl" id="takimlar" aria-labelledby="dh-tkl-t" data-dh-takim>\n')
w('          <div class="container max-w-xl">\n')
w('            <div class="section-header panel dh-secbar">\n')
w('              <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-tkl-t">Takım Dizini</h2>\n')
w('              <div class="dh-secbar__tools"><span class="dh-nwstamp">'
  '<i class="fas fa-shield-halved" aria-hidden="true"></i> '
  '<b data-dh-takim-sayac>%d</b> takım listeleniyor</span></div>\n' % len(takimlar))
w('            </div>\n')

# --- süzgeçler ---
w('            <div class="dh-tkl__filtre">\n')
w('              <div class="dh-tkl__satir">\n')
w('                <span class="dh-tkl__lbl">Dal</span>\n')
w('                <div class="dh-tkl__cips" role="radiogroup" aria-label="Dal seçimi" data-dh-takim-dal>\n')
w('                  <button type="button" class="dh-tkl__cip is-on" role="radio" aria-checked="true" data-dal="tumu">Tümü</button>\n')
for k, ad, ik in DAL:
    w('                  <button type="button" class="dh-tkl__cip" role="radio" aria-checked="false" data-dal="%s">'
      '<i class="fas %s" aria-hidden="true"></i>%s</button>\n' % (k, ik, ad))
w('                </div>\n')
w('              </div>\n')
w('              <div class="dh-tkl__satir">\n')
w('                <span class="dh-tkl__lbl">Lig</span>\n')
w('                <div class="dh-tkl__cips" role="radiogroup" aria-label="Lig seçimi" data-dh-takim-lig>\n')
w('                  <button type="button" class="dh-tkl__cip is-on" role="radio" aria-checked="true" data-lig="tumu">Tümü</button>\n')
for dal, lig in LIGLER:
    w('                  <button type="button" class="dh-tkl__cip" role="radio" aria-checked="false" '
      'data-lig="%s" data-dal="%s">%s</button>\n' % (anahtar(lig), dal, lig))
w('                </div>\n')
w('              </div>\n')
w('              <label class="dh-tkl__ara">\n')
w('                <span class="sr-only">Takım ara</span>\n')
w('                <i class="fas fa-magnifying-glass" aria-hidden="true"></i>\n')
w('                <input type="search" placeholder="Takım adı yaz — örn. Trabzon" data-dh-takim-ara autocomplete="off">\n')
w('              </label>\n')
w('            </div>\n')

# --- ızgara ---
w('            <div class="dh-tkl__grid" data-dh-takim-grid>\n')
for t in takimlar:
    w('              <a class="dh-tcard" href="%s" data-dal="%s" data-lig="%s" data-ara="%s">\n'
      % (t["href"], t["dal"], anahtar(t["lig"]), t["ara"]))
    w('                <span class="dh-tcard__crest"><img src="%s" alt="" width="44" height="44" loading="lazy"></span>\n' % t["logo"])
    w('                <span class="dh-tcard__nm">%s</span>\n' % t["ad"])
    w('                <span class="dh-tcard__meta">%s</span>\n' % t["lig"])
    w('              </a>\n')
w('            </div>\n')
w('            <p class="dh-tkl__bos" data-dh-takim-bos hidden>Bu süzgeçle eşleşen takım yok. '
  'Süzgeci genişletin ya da aramayı temizleyin.</p>\n')
w('            <p class="dh-tkl__not"><i class="fas fa-circle-info" aria-hidden="true"></i> '
  'Takım adları ve lig dağılımı prototip için hazırlanmış yer tutuculardır; güncel kadro ya da '
  'resmî lig kaydı değildir.</p>\n')
w('          </div>\n        </section>\n')
GOVDE = "".join(g)

s = open(SABLON, encoding="utf-8").read()
s = s.replace("<title>SAYFA BAŞLIĞI — Dada Haber</title>", "<title>Takımlar — Dada Haber</title>")
if 'data-dh-cat=""' in s:
    s = s.replace('data-dh-cat=""', 'data-dh-cat="spor"', 1)
m = re.search(r"[ \t]*<!-- ={10,} SAYFA GÖVDESİ BURAYA ={10,}.*?={10,} -->\n", s, re.S)
if not m:
    sys.exit("HATA: gövde yuvası yok")
s = s[:m.start()] + GOVDE + s[m.end():]
m2 = re.search(r'[ \t]*<script defer src="\./assets/js/app\.js"></script>[ \t]*\n', s)
s = s[:m2.end()] + '    <script defer src="./assets/js/v2/dh-takimlar.js"></script>\n' + s[m2.end():]
open(HEDEF, "w", encoding="utf-8").write(s)
print("%s yazıldı — %d takım, %d lig, %d dal" % (HEDEF, len(takimlar), len(LIGLER), len(DAL)))
