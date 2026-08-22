# -*- coding: utf-8 -*-
"""nato.html — üye ülke seçici. Tıklanan ülkenin künyesi ve haberleri gelir.

Yeni JS YAZILMADI: dünya sayfasındaki bölge seçici (assets/js/v2/dh-bolge.js)
"N seçenekten birini seç, künyeyi ve listeyi değiştir" sözleşmesini taşıyor;
burada seçenekler ülke. Veri kaynağı yine <script type="application/json">.
Backend gelince yalnız o JSON bloğu değişir.
"""
import json, os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)
sys.path.insert(0, os.path.join(kok, "docs", "parts"))
from sayfa_basligi import basli
SABLON = "docs/parts/sayfa-sablon.html"
HEDEF = "nato.html"
G = "./assets/images/main/posts/img-%02d.jpg"

# (anahtar, ad, kod, katılım, başkent, özet, kapsam, [haberler])
ULKE = [
 ("turkiye", "Türkiye", "TR", 1952, "Ankara",
  "İkinci büyük ordu; güney kanadında karar alma ve tatbikat trafiğinin merkezinde.",
  "Ankara · İzmir müttefik karargâhı · Konya AWACS üssü",
  [("Türkiye'nin ev sahipliğindeki tatbikat için hazırlık başladı",
    "Kara ve hava unsurlarının katılacağı çok uluslu tatbikatın takvimi açıklandı.", "Ankara", "09:12", "TATBİKAT", 1),
   ("Müttefik hava savunma ağına yeni radar entegrasyonu",
    "Erken uyarı hattındaki güncellemenin yıl sonuna kadar tamamlanması bekleniyor.", "Konya", "08:40", "SAVUNMA SANAYİİ", 2),
   ("Savunma sanayii ihracatında müttefik ülkelerin payı arttı",
    "İhracatın üçte ikisinden fazlası ittifak üyesi ülkelere yapıldı.", "Ankara", "07:55", "İHRACAT", 3)]),
 ("abd", "Amerika Birleşik Devletleri", "US", 1949, "Washington",
  "İttifakın en büyük askerî ve mali katkısını yapan üye; nükleer şemsiyenin taşıyıcısı.",
  "Washington · Stuttgart Avrupa Komutanlığı · Ramstein",
  [("Savunma bütçesi tasarısı komisyondan geçti",
    "Tasarı, Avrupa'daki caydırıcılık kalemine ayrılan payı koruyor.", "Washington", "10:05", "BÜTÇE", 4),
   ("Avrupa'daki rotasyonel tugay görev süresi uzatıldı",
    "Karar, doğu kanadındaki mevcudun yıl boyu aynı seviyede tutulacağı anlamına geliyor.", "Washington", "09:20", "KONUŞLANMA", 5),
   ("Ortak tedarik programında ikinci aşama onaylandı",
    "Program kapsamında mühimmat üretim hattı üç ülkeye yayılıyor.", "Washington", "08:12", "TEDARİK", 6)]),
 ("almanya", "Almanya", "DE", 1955, "Berlin",
  "Avrupa kanadının lojistik omurgası; ittifakın en yoğun ulaştırma düğümlerine ev sahipliği yapıyor.",
  "Berlin · Ramstein · Brunssum bölge karargâhı",
  [("Savunma harcaması hedefi üçüncü yıl da tutturuldu",
    "Bütçe görüşmelerinde tedarik kalemine ayrılan pay öne çıktı.", "Berlin", "09:48", "BÜTÇE", 7),
   ("Lojistik koridoru tatbikatı doğu sınırında başladı",
    "Ağır ekipmanın demiryoluyla sevki denendi.", "Berlin", "08:30", "LOJİSTİK", 8),
   ("Hava savunma sistemleri için ortak alım anlaşması",
    "Beş ülkenin katıldığı alım, teslimat takvimini öne çekiyor.", "Berlin", "07:40", "TEDARİK", 9)]),
 ("fransa", "Fransa", "FR", 1949, "Paris",
  "Bağımsız nükleer caydırıcılığa sahip ikinci Avrupalı üye; Akdeniz ve Sahel hattında etkin.",
  "Paris · Toulon · Akdeniz görev gücü",
  [("Akdeniz'de deniz güvenliği devriyesi genişletildi",
    "Görev gücüne iki fırkateyn daha katıldı.", "Toulon", "09:35", "DENİZ", 10),
   ("Savunma sanayii ihracat kalemleri yeniden düzenlendi",
    "Düzenleme, müttefik ülkelere teslimat sürelerini kısaltıyor.", "Paris", "08:05", "SANAYİ", 1),
   ("Hava kuvvetleri müşterek tatbikata katılıyor",
    "Tatbikat üç ülkenin hava sahasında yapılacak.", "Paris", "07:20", "TATBİKAT", 2)]),
 ("ingiltere", "Birleşik Krallık", "GB", 1949, "Londra",
  "Kuzey Atlantik ve Baltık hattında deniz gücü ağırlıklı katkı sağlıyor.",
  "Londra · Northwood deniz karargâhı · Baltık devriyesi",
  [("Baltık'ta hava devriyesi görevi devralındı",
    "Dört aylık dönem için iki filo görevlendirildi.", "Londra", "09:58", "HAVA", 3),
   ("Denizaltı programında yeni kilometre taşı",
    "İlk tekne için basınç testi süreci tamamlandı.", "Londra", "08:44", "PROGRAM", 4),
   ("Siber savunma merkezine ek kaynak ayrıldı",
    "Merkez, müttefik ağlarının izlenmesinde koordinasyon görevi üstleniyor.", "Londra", "07:35", "SİBER", 5)]),
 ("polonya", "Polonya", "PL", 1999, "Varşova",
  "Doğu kanadının en yüksek savunma harcaması oranına sahip üyesi.",
  "Varşova · Szczecin çokuluslu kolordu · doğu sınır hattı",
  [("Doğu sınırında altyapı yatırımı hızlandırıldı",
    "Yol ve depolama tesisleri için ihale takvimi açıklandı.", "Varşova", "10:12", "ALTYAPI", 6),
   ("Zırhlı tugay tedariki için sözleşme imzalandı",
    "Teslimatın üç yıla yayılması planlanıyor.", "Varşova", "09:02", "TEDARİK", 7),
   ("Çokuluslu kolordu karargâhı kapasitesini artırıyor",
    "Personel sayısı kademeli olarak yükseltilecek.", "Szczecin", "08:15", "KARARGÂH", 8)]),
 ("italya", "İtalya", "IT", 1949, "Roma",
  "Akdeniz'in merkezinde konumlanan üye; deniz ve hava ulaştırmasında düğüm noktası.",
  "Roma · Napoli müttefik deniz karargâhı · Sigonella",
  [("Napoli karargâhında yıllık değerlendirme toplantısı",
    "Akdeniz'deki görev gücünün yıl planı ele alındı.", "Napoli", "09:25", "KARARGÂH", 9),
   ("Hava ulaştırma filosuna iki uçak daha katıldı",
    "Filo, ittifak içi sevkiyatlarda kullanılıyor.", "Roma", "08:36", "LOJİSTİK", 10),
   ("Sahil güvenlik iş birliği protokolü yenilendi",
    "Protokol arama kurtarma tatbikatlarını da kapsıyor.", "Roma", "07:48", "İŞ BİRLİĞİ", 1)]),
 ("ispanya", "İspanya", "ES", 1982, "Madrid",
  "Atlantik ve Akdeniz arasındaki geçiş hattında üs ve liman kapasitesi sunuyor.",
  "Madrid · Rota deniz üssü · Torrejón hava merkezi",
  [("Rota'daki destroyer sayısı artırılıyor",
    "Karar, Atlantik devriyelerinin sıklığını yükseltecek.", "Madrid", "09:40", "DENİZ", 2),
   ("Hava gözetleme merkezi yazılım güncellemesi aldı",
    "Güncelleme, veri paylaşımını hızlandırıyor.", "Madrid", "08:22", "TEKNOLOJİ", 3),
   ("Savunma bütçesinde araştırma payı yükseldi",
    "Pay, üç yıllık planın ilk hedefini aştı.", "Madrid", "07:30", "BÜTÇE", 4)]),
 ("hollanda", "Hollanda", "NL", 1949, "Amsterdam",
  "Brunssum bölge karargâhına ev sahipliği yapıyor; lojistik planlamada kilit rol üstleniyor.",
  "Lahey · Brunssum bölge karargâhı · Rotterdam limanı",
  [("Brunssum'da müşterek planlama tatbikatı yapıldı",
    "Senaryo, ağır ekipmanın hızlı sevkine odaklandı.", "Brunssum", "09:15", "PLANLAMA", 5),
   ("Rotterdam limanı müttefik sevkiyat kapasitesini artırıyor",
    "Yeni rıhtım düzenlemesi yıl sonunda devrede.", "Rotterdam", "08:28", "LOJİSTİK", 6),
   ("Hava savunma bataryası doğu kanadına konuşlandı",
    "Konuşlanma altı ay sürecek.", "Lahey", "07:52", "KONUŞLANMA", 7)]),
 ("norvec", "Norveç", "NO", 1949, "Oslo",
  "Kuzey kanadının kutup hattındaki üyesi; soğuk iklim tatbikatlarına ev sahipliği yapıyor.",
  "Oslo · Bodø hava üssü · Kuzey Kutbu hattı",
  [("Kuzey'de soğuk iklim tatbikatı tamamlandı",
    "Tatbikata on iki ülkeden birlik katıldı.", "Bodø", "09:30", "TATBİKAT", 8),
   ("Deniz gözetleme uçakları için yeni üs düzenlemesi",
    "Üs, kuzey rotalarının izlenmesinde kullanılacak.", "Oslo", "08:18", "GÖZETLEME", 9),
   ("Enerji altyapısı güvenliği için ortak protokol",
    "Protokol deniz altı hatlarını kapsıyor.", "Oslo", "07:25", "ALTYAPI", 10)]),
 ("kanada", "Kanada", "CA", 1949, "Ottawa",
  "Kuzey Amerika hava savunmasında ABD ile ortak; Baltık'ta muharebe grubu liderliği yapıyor.",
  "Ottawa · Baltık muharebe grubu · kuzey hava savunma hattı",
  [("Baltık'taki muharebe grubu görev süresi uzatıldı",
    "Grup, çok uluslu yapısını koruyor.", "Ottawa", "09:44", "KONUŞLANMA", 1),
   ("Kuzey hava savunma hattında modernizasyon başlıyor",
    "İlk etap radar yenilemesini içeriyor.", "Ottawa", "08:33", "MODERNİZASYON", 2),
   ("Savunma tedarikinde yerli sanayi payı artıyor",
    "Yeni kural, ortak üretimi teşvik ediyor.", "Ottawa", "07:41", "SANAYİ", 3)]),
 ("yunanistan", "Yunanistan", "GR", 1952, "Atina",
  "Ege ve Doğu Akdeniz hattında konuşlu; savunma harcaması oranı ittifak ortalamasının üzerinde.",
  "Atina · Larissa hava karargâhı · Girit Suda üssü",
  [("Suda üssünde bakım kapasitesi genişletiliyor",
    "Genişleme, deniz unsurlarının bakım süresini kısaltacak.", "Girit", "09:20", "ÜS", 4),
   ("Hava kuvvetleri filo modernizasyonunda ikinci aşama",
    "Aşama, aviyonik güncellemeyi kapsıyor.", "Atina", "08:26", "MODERNİZASYON", 5),
   ("Doğu Akdeniz'de arama kurtarma tatbikatı yapıldı",
    "Tatbikata üç ülke katıldı.", "Atina", "07:38", "TATBİKAT", 6)]),
]

def haber(h):
    baslik, ozet, yer, saat, etiket, g = h
    return {"baslik": baslik, "ozet": ozet, "yer": yer, "saat": saat,
            "etiket": etiket, "gorsel": G % g}

DATA = {"varsayilan": ULKE[0][0], "bolgeler": {}}
for a, ad, kod, yil, bask, ozet, kapsam, hs in ULKE:
    DATA["bolgeler"][a] = {
        "ad": ad,
        "ozet": ozet,
        "kapsam": "%s · Üyelik %d · Başkent %s" % (kapsam, yil, bask),
        "haberler": [haber(h) for h in hs],
    }

g = []
w = g.append
w(basli("Savunma", "NATO",
        "İttifakın gündemi üye ülke üzerinden okunur: bir ülke seçin, o ülkenin ittifak "
        "içindeki konumu ve son gelişmeleri aşağıda görünsün.",
        [("Savunma", "savunma.html"), ("NATO", None)], "img-04.jpg", "50% 44%",
        ["Üye ülke: <b>%d</b>" % len(ULKE), "Veri: <b>prototip</b>"]))

w('        <section class="section panel" id="uyeler" aria-labelledby="dh-nato-t">\n')
w('          <div class="container max-w-xl">\n')
w('            <div class="section-header panel dh-secbar">\n')
w('              <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-nato-t">Üye Ülkeler</h2>\n')
w('              <div class="dh-secbar__tools">\n')
w('                <span class="dh-nwstamp"><i class="fas fa-shield-alt" aria-hidden="true"></i> %d ülke</span>\n' % len(ULKE))
w('                <a href="savunma.html" class="dh-secbar__all">Savunma gündemi</a>\n')
w('              </div>\n            </div>\n')
w('            <div class="dh-bolge dh-bolge--nato" data-dh-bolge>\n')
w('              <div class="dh-bolge__rail" role="radiogroup" aria-label="Üye ülke seçimi">\n')
for a, ad, kod, yil, *_ in ULKE:
    w('                <button type="button" class="dh-bolge__b" role="radio" aria-checked="false" tabindex="-1" '
      'data-dh-bolge-sec="%s"><span class="dh-nato__kod" aria-hidden="true">%s</span><span>%s</span></button>\n'
      % (a, kod, ad))
w('              </div>\n')
w('              <div class="dh-bolge__id">\n')
w('                <h3 class="dh-bolge__ad" data-dh-bolge-ad>%s</h3>\n' % ULKE[0][1])
w('                <p class="dh-bolge__ozet" data-dh-bolge-ozet></p>\n')
w('                <span class="dh-bolge__kapsam" data-dh-bolge-kapsam></span>\n')
w('              </div>\n')
w('              <div class="dh-bolge__liste" data-dh-bolge-liste aria-live="polite"></div>\n')
w('            </div>\n')
w('            <p class="dh-nato__not"><i class="fas fa-circle-info" aria-hidden="true"></i> ')
w('Sayfadaki başlıklar, tarihler ve sayılar prototip için üretilmiş yer tutuculardır; ')
w('gerçek bir kuruma ya da açıklamaya dayanmaz.</p>\n')
w('          </div>\n        </section>\n\n')
w('    <script type="application/json" id="dh-bolge-data">\n')
w(json.dumps(DATA, ensure_ascii=False, indent=2))
w('\n    </script>\n')
GOVDE = "".join(g)

s = open(SABLON, encoding="utf-8").read()
s = s.replace("<title>SAYFA BAŞLIĞI — Dada Haber</title>", "<title>NATO — Dada Haber</title>")
if 'data-dh-cat=""' in s:
    s = s.replace('data-dh-cat=""', 'data-dh-cat="savunma"', 1)
m = re.search(r"[ \t]*<!-- ={10,} SAYFA GÖVDESİ BURAYA ={10,}.*?={10,} -->\n", s, re.S)
if not m:
    sys.exit("HATA: gövde yuvası yok")
s = s[:m.start()] + GOVDE + s[m.end():]
m2 = re.search(r'[ \t]*<script defer src="\./assets/js/app\.js"></script>[ \t]*\n', s)
s = s[:m2.end()] + '    <script defer src="./assets/js/v2/dh-bolge.js"></script>\n' + s[m2.end():]
open(HEDEF, "w", encoding="utf-8").write(s)
print("%s yazıldı (%d satır, %d ülke)" % (HEDEF, len(s.splitlines()), len(ULKE)))
