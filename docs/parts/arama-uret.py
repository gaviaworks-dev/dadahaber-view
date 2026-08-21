# -*- coding: utf-8 -*-
"""arama.html — Nihai Menü Haritası bölüm 7 'Global Arama'.
Sonuç sekmeleri (9) + süzgeçler (7). Mevcut haber ızgarası 'Haberler'
grubu olarak korunur; diğer sekmeler için tür başına ayrı sonuç bloğu."""
import io, re

SEKME = [("tumu","Tümü","128"),("haberler","Haberler","64"),("videolar","Videolar","18"),
         ("podcastler","Podcastler","9"),("yazarlar","Yazarlar","7"),("konular","Konular","12"),
         ("sehirler","Şehirler","5"),("dogrulamalar","Doğrulamalar","8"),("veri","Veri ve Haritalar","5")]

SUZGEC = [
 ("Tarih", ["Tüm zamanlar","Son 24 saat","Son 7 gün","Son 30 gün","Son 1 yıl"]),
 ("Kategori", ["Tüm kategoriler","Şimdi","Gündem","Dünya","Ekonomi","Teknoloji","Gelecek","Spor","Sağlık","Kültür & Yaşam","Video","Keşfet"]),
 ("İçerik türü", ["Tüm türler","Haber","Analiz","Görüş","Röportaj","Video","Podcast","İnfografik","Doğrulama"]),
 ("Yazar", ["Tüm yazarlar","Selin Aydın","Murat Erkan","Deniz Kara","Elif Şahin","Konuk yazarlar"]),
 ("Şehir", ["Tüm şehirler","İstanbul","Ankara","İzmir","Bursa","Antalya","Diğer iller"]),
 ("Haber durumu", ["Tüm haberler","Güncellenenler","Düzeltme notu olanlar","Doğrulanmış","Canlı"]),
 ("Okuma süresi", ["Fark etmez","1 dakikadan kısa","1–3 dakika","3–7 dakika","7 dakikadan uzun"]),
]

def sekmeler():
    o = io.StringIO(); w = o.write
    w('        <!-- v2 · Sonuç sekmeleri (doküman bölüm 7) -->\n')
    w('        <nav class="section panel dh-catbar" data-cat="" aria-label="Sonuç türleri">\n')
    w('          <div class="container max-w-xl">\n            <div class="dh-catbar__row">\n')
    w('              <span class="dh-catbar__root"><span class="dh-catbar__root-ad" aria-current="page">ARAMA</span><span class="dh-catbar__root-fn">sonuç türleri</span></span>\n')
    w('              <div class="dh-catbar__inner swiper-parent">\n')
    w('                <div class="swiper dh-catbar__swiper" data-uc-swiper="items: auto; gap: 8; free: true; grab-cursor: true; next: .dh-catbar__nav--next; prev: .dh-catbar__nav--prev; disable-class: is-off; watchOverflow: true;">\n')
    w('                  <div class="swiper-wrapper" role="tablist" aria-label="Sonuç türleri">\n')
    for n, (k, ad, adet) in enumerate(SEKME):
        on = " is-on" if n == 0 else ""
        w('                    <div class="swiper-slide"><button type="button" class="dh-catbar__chip%s" role="tab" aria-selected="%s" data-dh-ara-sekme="%s">%s <span class="dh-ara__n">%s</span></button></div>\n'
          % (on, "true" if n == 0 else "false", k, ad, adet))
    w('                  </div>\n                </div>\n')
    w('                <div class="dh-catbar__nav dh-catbar__nav--prev" role="button" aria-label="Önceki türler"><i class="unicon-chevron-left"></i></div>\n')
    w('                <div class="dh-catbar__nav dh-catbar__nav--next" role="button" aria-label="Sonraki türler"><i class="unicon-chevron-right"></i></div>\n')
    w('              </div>\n            </div>\n          </div>\n        </nav>\n')
    return o.getvalue()

def suzgecler():
    o = io.StringIO(); w = o.write
    w('\n        <!-- v2 · Arama süzgeçleri (doküman bölüm 7) -->\n')
    w('        <section class="section panel dh-filt" aria-labelledby="dh-filt-b">\n')
    w('          <div class="container max-w-xl">\n')
    w('            <div class="dh-filt__bar">\n')
    w('              <h2 class="dh-filt__t" id="dh-filt-b"><i class="fas fa-sliders" aria-hidden="true"></i> Süzgeçler</h2>\n')
    w('              <div class="dh-filt__grid">\n')
    for n, (ad, secenek) in enumerate(SUZGEC):
        sid = "dhFilt%d" % n
        w('                <label class="dh-filt__f">\n')
        w('                  <span class="dh-filt__lab" id="%s-l">%s</span>\n' % (sid, ad))
        w('                  <select class="dh-filt__sel" id="%s" aria-labelledby="%s-l">\n' % (sid, sid))
        for s_ in secenek:
            w('                    <option>%s</option>\n' % s_)
        w('                  </select>\n                </label>\n')
    w('              </div>\n')
    w('              <button type="button" class="dh-filt__clr" data-dh-filt-temizle>Süzgeçleri temizle</button>\n')
    w('            </div>\n          </div>\n        </section>\n')
    return o.getvalue()

# tür grupları — Haberler dışındakiler
def grup(k, baslik, tumu_h, satirlar, tur):
    o = io.StringIO(); w = o.write
    w('\n                    <section class="dh-arag" data-dh-ara-grup="%s" aria-labelledby="%s-b">\n' % (k, k))
    w('                      <header class="dh-arag__h">\n')
    w('                        <h2 class="dh-arag__t" id="%s-b">%s</h2>\n' % (k, baslik))
    w('                        <a class="dh-arag__all" href="%s">Bu türdeki tüm sonuçlar</a>\n' % tumu_h)
    w('                      </header>\n')
    w('                      <ul class="dh-arag__l dh-arag__l--%s">\n' % tur)
    for satir in satirlar:
        w('                        %s\n' % satir)
    w('                      </ul>\n                    </section>\n')
    return o.getvalue()

def sat(h, baslik, meta, ek=""):
    return ('<li><a href="%s"><b>%s</b><span class="dh-arag__m">%s</span>%s</a></li>' % (h, baslik, meta, ek))

GRUPLAR = ""
GRUPLAR += grup("videolar", "Videolar", "video.html", [
  sat("video-detay.html","Depremde ilk 72 saat: sahadan aktarım","VİDEO · 12:48 · 12.12.2025"),
  sat("video-detay.html","Deprem yönetmeliği neyi zorunlu kılıyor?","AÇIKLAYICI · 03:18 · 11.12.2025"),
  sat("video-detay.html","Toplanma alanları nerede? Şematik harita","VERİ · 05:24 · 10.12.2025"),
  sat("video-detay.html","Bir arama kurtarma ekibinin günü","BELGESEL · 44:05 · 09.12.2025"),
], "vid")
GRUPLAR += grup("podcastler", "Podcastler", "podcast.html", [
  sat("podcast-detay.html","Günlük Gündem — deprem hazırlığı özel bölümü","GÜNLÜK GÜNDEM · 28:14 · 12.12.2025"),
  sat("podcast-detay.html","Haftanın Özeti — afet yönetimi","HAFTANIN ÖZETİ · 41:02 · 11.12.2025"),
  sat("podcast-detay.html","Röportaj: bir jeoloji mühendisiyle","RÖPORTAJ · 52:30 · 08.12.2025"),
], "pod")
GRUPLAR += grup("yazarlar", "Yazarlar", "yazar-liste.html", [
  sat("yazar-detay.html","Selin Aydın","EKONOMİ · 142 yazı · 3 yazı bu konuda"),
  sat("yazar-detay.html","Murat Erkan","DIŞ POLİTİKA · 98 yazı · 2 yazı bu konuda"),
  sat("yazar-detay.html","Deniz Kara","KENT VE YAŞAM · 76 yazı · 4 yazı bu konuda"),
], "yaz")
GRUPLAR += grup("konular", "Konular", "kesfet.html#dosyalar", [
  sat("dada-baglam.html","Deprem hazırlığı","KONU DOSYASI · 42 içerik · sürekli güncelleniyor"),
  sat("dada-baglam.html","Yapı denetimi","KONU DOSYASI · 18 içerik"),
  sat("dada-baglam.html","Afet yönetimi","KONU DOSYASI · 27 içerik"),
  sat("dada-baglam.html","Kentsel dönüşüm","KONU DOSYASI · 31 içerik"),
], "kon")
GRUPLAR += grup("sehirler", "Şehirler", "gundem.html#yerel", [
  sat("gundem.html#yerel","İstanbul","YEREL · 214 içerik · 6 içerik bu konuda"),
  sat("gundem.html#yerel","Ankara","YEREL · 168 içerik · 3 içerik bu konuda"),
  sat("gundem.html#yerel","İzmir","YEREL · 141 içerik · 5 içerik bu konuda"),
], "seh")
GRUPLAR += grup("dogrulamalar", "Doğrulamalar", "dada-dogrula.html", [
  sat("dada-dogrula.html","“Bu görüntü dünkü depremden” iddiası","DADA DOĞRULA · 12.12.2025", '<span class="dh-arag__v dh-arag__v--yanlis">Yanlış</span>'),
  sat("dada-dogrula.html","“Toplanma alanları kaldırıldı” iddiası","DADA DOĞRULA · 11.12.2025", '<span class="dh-arag__v dh-arag__v--kismen">Kısmen Doğru</span>'),
  sat("dada-dogrula.html","Zincir mesajdaki uyarı metni","DADA DOĞRULA · 10.12.2025", '<span class="dh-arag__v dh-arag__v--baglam">Bağlamdan Koparılmış</span>'),
  sat("dada-dogrula.html","Yapay zekâ ile üretilmiş enkaz görseli","DADA DOĞRULA · 09.12.2025", '<span class="dh-arag__v dh-arag__v--yz">Yapay Zekâ İçeriği</span>'),
], "dog")
GRUPLAR += grup("veri", "Veri ve Haritalar", "veri-harita.html", [
  sat("veri-harita.html#afet","Afet haritası — şematik il görünümü","VERİ & HARİTA · 81 il · güncel"),
  sat("veri-harita.html","Yapı stoku yaş dağılımı","EKONOMİ GRAFİĞİ · 2015–2025"),
  sat("veri-harita.html","Toplanma alanı yoğunluğu","ŞEHİR VERİSİ · ilçe bazlı"),
], "ver")

s = open("arama.html", encoding="utf-8").read()

# 1) sekme şeridi: mevcut dh-catbar bloğunu değiştir
i = s.index('        <nav class="section panel dh-catbar" data-cat="" aria-label="İçerik türleri">')
j = s.index('        </nav>\n', i) + len('        </nav>\n')
s = s[:i] + sekmeler() + suzgecler() + s[j:]

# 2) haber ızgarasını grup olarak işaretle
eski = '''                        <div class="col">
                            <div class="panel dh-listgrid">'''
yeni = '''                        <div class="col">
                            <div class="panel dh-listgrid dh-arag" data-dh-ara-grup="haberler">'''
assert eski in s
s = s.replace(eski, yeni, 1)

# 3) diğer tür gruplarını ızgaranın önüne koy
anch = '                    <div class="row g-4 xl:g-8">\n'
k = s.index(anch) + len(anch)
s = s[:k] + '                    <div class="dh-aragrup">' + GRUPLAR + '\n                    </div>\n' + s[k:]

# 4) betik
if "v2/dh-arama.js" not in s:
    m = re.search(r'[ \t]*<script defer src="\./assets/js/v2/dh-v2-nav\.js"></script>[ \t]*\n', s)
    s = s[:m.end()] + '    <script defer src="./assets/js/v2/dh-arama.js"></script>\n' + s[m.end():]

open("arama.html", "w", encoding="utf-8").write(s)
print("arama.html güncellendi:", len(s.splitlines()), "satır")
