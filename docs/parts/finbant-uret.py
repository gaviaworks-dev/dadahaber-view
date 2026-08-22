# -*- coding: utf-8 -*-
"""Finans alt sayfalarının düz renk bandını GÖRSELLİ HABER BANDINA çevirir.

Talep (revize-2.docx, madde 2): "Döviz kurları sayfasındaki bant yapısı
kurumsala uygun değil; burayı diğer sayfalar gibi (finans sayfasındaki
görsel gibi) haber bant şeklinde yapalım. Bu tarz başka sayfa varsa
onları da düzelt."

TARAMA: `.dh-finhead` (düz teal degrade bant) yalnız dört sayfada —
altin, borsa, doviz, kripto. Hepsi bu üreteçten geçiyor.

NEDEN .dh-ph--photo: sitenin başlık standardı bu (27 sayfa) ve devir
notu "yeni sayfa yazarken bunu kullan" diyor. finans.html'in tam swiper
bandı (.dh-lb) dört sayfaya kopyalanmadı — dört ayrı kaydırıcı bakım
yükü olurdu ve o banner kategori sayfası içindir. Bunun yerine standart
görselli başlığa, finans'takiyle aynı bilgiyi taşıyan tek satırlık
ÖNE ÇIKAN HABER şeridi eklendi (.dh-ph__haber): kategori çipi, başlık,
yazar ve meta. Böylece hem kurumsal başlık dili korunuyor hem talebin
istediği "haber bandı" içeriği geliyor.

Yeniden üret:  python3 docs/parts/finbant-uret.py
"""
import os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)

# sayfa: (kicker, h1, lead, kırıntı adı, görsel, odak, öne çıkan haber)
SAYFA = {
 "doviz.html": (
   "FİNANS · DÖVİZ", "Döviz Kurları",
   "Serbest piyasa ve Merkez Bankası kurları, gün içi değişim ve çevirici tek sayfada.",
   "Döviz", "img-09.jpg", "50% 42%",
   ("DÖVİZ", "Dolar/TL güne yatay başladı, bant daraldı",
    "Selin Arıkan", "Ekonomi Editörü", "20.08.2026", "3 DK", "4,2B")),
 "altin.html": (
   "FİNANS · ALTIN", "Altın Fiyatları",
   "Gram, çeyrek, ons ve külçe fiyatları; Kapalıçarşı ile serbest piyasa farkı tek sayfada.",
   "Altın", "img-14.jpg", "50% 46%",
   ("ALTIN", "Ons altında 2.400 dolar eşiği yeniden test ediliyor",
    "Kerem Doğan", "Muhabir", "19.08.2026", "5 DK", "3,1B")),
 "borsa.html": (
   "FİNANS · BORSA", "Borsa ve Endeksler",
   "BIST 100, sektör endeksleri, yükselen ve düşenler ile KAP bildirimleri tek sayfada.",
   "Borsa", "img-05.jpg", "50% 40%",
   ("BORSA", "BIST 100 haftaya alıcılı başladı, işlem hacmi arttı",
    "Emre Yıldız", "Piyasa Muhabiri", "20.08.2026", "4 DK", "2,8B")),
 "kripto.html": (
   "FİNANS · KRİPTO", "Kripto Para",
   "Bitcoin, Ethereum ve altcoinlerde anlık fiyat, hacim ve piyasa değeri tek sayfada.",
   "Kripto", "img-18.jpg", "50% 44%",
   ("KRİPTO", "Ethereum ağ ücretleri üç ayın en düşük seviyesinde",
    "Kerem Doğan", "Muhabir", "19.08.2026", "5 DK", "3,1B")),
}


def bant(kicker, h1, lead, crumb, gorsel, poz, haber):
    kat, bas, yazar, unvan, tarih, sure, goruntu = haber
    o = []
    w = o.append
    w('    <header class="dh-ph dh-ph--photo dh-ph--haber" data-cat="finans">\n')
    w('      <span class="dh-vmedia" style="--dh-vpos: %s" aria-hidden="true">\n' % poz)
    w('        <img src="./assets/images/main/posts/%s" alt="" loading="eager" fetchpriority="high" decoding="async">\n' % gorsel)
    w('      </span>\n')
    w('      <div class="container max-w-xl">\n')
    w('        <nav class="dh-art-crumb dh-art-crumb--ink" aria-label="Sayfa yolu">\n')
    w('          <a href="index.html" aria-label="Anasayfa"><i class="fas fa-home-lg-alt" aria-hidden="true"></i></a>\n')
    w('          <i class="fas fa-chevron-right" aria-hidden="true"></i>\n')
    w('          <a href="finans.html">Finans</a>\n')
    w('          <i class="fas fa-chevron-right" aria-hidden="true"></i>\n')
    w('          <span aria-current="page">%s</span>\n' % crumb)
    w('        </nav>\n\n')
    w('        <span class="dh-ph__bar" aria-hidden="true"></span>\n')
    w('        <span class="dh-ph__eyebrow">%s</span>\n' % kicker)
    w('        <h1 class="dh-ph__title">%s</h1>\n' % h1)
    w('        <p class="dh-ph__sub">%s</p>\n\n' % lead)
    # öne çıkan haber şeridi — finans.html bandındaki bilgi düzeni
    w('        <div class="dh-ph__haber">\n')
    w('          <a class="dh-ph__hkat" href="finans.html">%s</a>\n' % kat)
    w('          <p class="dh-ph__ht"><a href="finans-detay.html">%s</a></p>\n' % bas)
    w('          <div class="dh-ph__hmeta">\n')
    w('            <span class="dh-ph__hyazar"><b>%s</b><small>%s</small></span>\n' % (yazar, unvan))
    w('            <span class="dh-ph__hstat">\n')
    w('              <span><i class="fas fa-calendar-day" aria-hidden="true"></i> %s</span>\n' % tarih)
    w('              <span><i class="fas fa-clock" aria-hidden="true"></i> %s</span>\n' % sure)
    w('              <span><i class="fas fa-eye" aria-hidden="true"></i> %s</span>\n' % goruntu)
    w('            </span>\n')
    w('          </div>\n')
    w('        </div>\n')
    w('      </div>\n    </header>\n')
    return "".join(o)


n = 0
for dosya, veri in SAYFA.items():
    s = open(dosya, encoding="utf-8").read()
    yeni = bant(*veri)

    # eski düz bant ya da önceki üretim
    m = re.search(r'[ \t]*<section class="dh-finhead"', s)
    if m:
        b = m.start()
        k = s.index("</section>", b) + len("</section>")
    else:
        m = re.search(r'[ \t]*<header class="dh-ph dh-ph--photo dh-ph--haber"', s)
        if not m:
            print("  ! %s — bant bulunamadı, atlandı" % dosya)
            continue
        b = m.start()
        k = s.index("</header>", b) + len("</header>")
    while k < len(s) and s[k] in " \t":
        k += 1
    if k < len(s) and s[k] == "\n":
        k += 1
    s = s[:b] + yeni + s[k:]
    open(dosya, "w", encoding="utf-8").write(s)
    print("  %s yazıldı" % dosya)
    n += 1

print("%d sayfa görselli haber bandına alındı" % n)
