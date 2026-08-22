# -*- coding: utf-8 -*-
"""BURÇ ÇARKI bölümünü astroloji.html'e yazar (idempotent).

Talep (22 Ağustos): "astrolojide uygun yere bu yapıda bir yapı kuralım."
Referans: solda günlük/haftalık/aylık yorum girişleri, sağda 12 dilimli
burç çarkı.

ENTEGRASYON: çark kendi durumunu TUTMAZ. Her dilim `data-dh-card="<burç>"`
taşır; sayfadaki mevcut dh-astro.js bu niteliği zaten dinliyor — tıklayınca
burcu seçip #astroloji bölümüne kaydırıyor. Böylece tek doğruluk kaynağı
korunuyor, ikinci bir seçim durumu doğmuyor. dh-astro.js DEĞİŞTİRİLMEDİ
(denetim.py 7. kural: v1 ile paylaşılan dosya).

Yeniden üret:  python3 docs/parts/astro-cark-uret.py
"""
import math, os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)

HEDEF = "astroloji.html"
ISARET_BAS = "<!-- BURÇ ÇARKI — üretilmiş: docs/parts/astro-cark-uret.py -->"
ISARET_SON = "<!-- /BURÇ ÇARKI -->"

BURC = [
    ("koc",     "Koç",     "♈", "21 Mart – 19 Nisan",    "Ateş"),
    ("boga",    "Boğa",    "♉", "20 Nisan – 20 Mayıs",   "Toprak"),
    ("ikizler", "İkizler", "♊", "21 Mayıs – 20 Haziran", "Hava"),
    ("yengec",  "Yengeç",  "♋", "21 Haziran – 22 Temmuz","Su"),
    ("aslan",   "Aslan",   "♌", "23 Temmuz – 22 Ağustos","Ateş"),
    ("basak",   "Başak",   "♍", "23 Ağustos – 22 Eylül", "Toprak"),
    ("terazi",  "Terazi",  "♎", "23 Eylül – 22 Ekim",    "Hava"),
    ("akrep",   "Akrep",   "♏", "23 Ekim – 21 Kasım",    "Su"),
    ("yay",     "Yay",     "♐", "22 Kasım – 21 Aralık",  "Ateş"),
    ("oglak",   "Oğlak",   "♑", "22 Aralık – 19 Ocak",   "Toprak"),
    ("kova",    "Kova",    "♒", "20 Ocak – 18 Şubat",    "Hava"),
    ("balik",   "Balık",   "♓", "19 Şubat – 20 Mart",    "Su"),
]

CX = CY = 300.0
R_DIS = 290.0     # dış kenar
R_ORTA = 226.0    # ad bandı ile glif bandı sınırı
R_IC = 138.0      # glif bandının iç kenarı
R_GOBEK = 92.0    # göbek diski


def nokta(r, aci):
    a = math.radians(aci)
    return CX + r * math.cos(a), CY + r * math.sin(a)


def halka_dilim(r1, r2, a0, a1):
    """r1 iç, r2 dış yarıçaplı halka dilimi (a0 -> a1, derece)."""
    x1, y1 = nokta(r2, a0)
    x2, y2 = nokta(r2, a1)
    x3, y3 = nokta(r1, a1)
    x4, y4 = nokta(r1, a0)
    return ("M %.2f %.2f A %.2f %.2f 0 0 1 %.2f %.2f "
            "L %.2f %.2f A %.2f %.2f 0 0 0 %.2f %.2f Z"
            % (x1, y1, r2, r2, x2, y2, x3, y3, r1, r1, x4, y4))


def svg():
    p = []
    p.append('<svg class="dh-zc__svg" viewBox="0 0 600 600" role="img" '
             'aria-labelledby="dh-zc-svg-t dh-zc-svg-d">')
    p.append('  <title id="dh-zc-svg-t">Burç çarkı</title>')
    p.append('  <desc id="dh-zc-svg-d">On iki burç, çark üzerinde sırayla '
             'dizilmiştir. Bir dilime dokunduğunuzda o burcun günlük yorumu '
             'açılır. Çark bir gökyüzü haritası değildir; şematiktir.</desc>')
    p.append('  <circle class="dh-zc__ring" cx="300" cy="300" r="%.1f"/>' % R_DIS)
    p.append('  <circle class="dh-zc__ring" cx="300" cy="300" r="%.1f"/>' % R_ORTA)
    p.append('  <circle class="dh-zc__ring" cx="300" cy="300" r="%.1f"/>' % R_IC)

    for i, (anahtar, ad, glif, tarih, element) in enumerate(BURC):
        a0 = -105.0 + i * 30.0
        a1 = a0 + 30.0
        orta = a0 + 15.0

        gx, gy = nokta((R_IC + R_ORTA) / 2.0, orta)
        ax, ay = nokta((R_ORTA + R_DIS) / 2.0, orta)
        # Alt yarıda metni ters durmasın diye 180 derece çevir.
        donme = orta + 90.0
        if 0.0 < (orta % 360.0) < 180.0:
            donme = orta - 90.0

        p.append('  <a class="dh-zc__dilim" data-dh-card="%s" href="#astroloji" '
                 'role="link" tabindex="0" aria-label="%s — %s">' % (anahtar, ad, tarih))
        p.append('    <path class="dh-zc__alan" d="%s"/>' % halka_dilim(R_ORTA, R_DIS, a0, a1))
        p.append('    <path class="dh-zc__alan dh-zc__alan--ic" d="%s"/>' % halka_dilim(R_IC, R_ORTA, a0, a1))
        p.append('    <text class="dh-zc__ad" x="%.2f" y="%.2f" transform="rotate(%.2f %.2f %.2f)">%s</text>'
                 % (ax, ay, donme, ax, ay, ad))
        p.append('    <text class="dh-zc__glif" x="%.2f" y="%.2f">%s</text>' % (gx, gy, glif))
        p.append('  </a>')
        # ayraç çizgisi
        x1, y1 = nokta(R_IC, a0)
        x2, y2 = nokta(R_DIS, a0)
        p.append('  <line class="dh-zc__ayrac" x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"/>' % (x1, y1, x2, y2))

    p.append('  <circle class="dh-zc__gobek" cx="300" cy="300" r="%.1f"/>' % R_GOBEK)
    p.append('  <text class="dh-zc__gobekK" x="300" y="286">BURÇ</text>')
    p.append('  <text class="dh-zc__gobekK" x="300" y="316">ÇARKI</text>')
    p.append('</svg>')
    return "\n            ".join(p)


GIRIS = [
    ("gunluk",   "Günlük Burç Yorumu",
     "Günlük burç yorumları: 22 Ağustos Cumartesi",
     "22 Ağustos 2026 Cumartesi günü on iki burcu neyin beklediği; aşk, "
     "kariyer ve para başlıklarında gün içi vurguları.",
     "Her sabah 06.00"),
    ("haftalik", "Haftalık Burç Yorumu",
     "Haftalık burç yorumları: 17 – 23 Ağustos",
     "Haftanın gökyüzü hareketleri ve bunların on iki burca etkisi; "
     "haftanın güçlü ve dikkat isteyen günleri.",
     "Pazartesi 07.00"),
    ("aylik",    "Aylık Burç Yorumu",
     "Aylık burç yorumları: Ağustos 2026",
     "Ay boyunca gerçekleşecek astrolojik olaylar, geri hareketler ve "
     "dolunay–yeniay takvimi; burç burç değerlendirme.",
     "Ayın ilk günü"),
]


def blok():
    o = []
    o.append('        ' + ISARET_BAS)
    o.append('        <section class="section dh-serit dh-zc bg-gray-10 dark:bg-gray-800" id="burc-carki" aria-labelledby="dh-zc-t">')
    o.append('          <div class="section-outer panel py-4 lg:py-8">')
    o.append('            <div class="container max-w-xl">')
    o.append('              <div class="section-header panel dh-secbar">')
    o.append('                <h2 class="h5 xl:h4 m-0 text-black dark:text-white" id="dh-zc-t">Burç Çarkı</h2>')
    o.append('                <div class="dh-secbar__tools">')
    o.append('                  <span class="dh-nwstamp"><i class="fas fa-star" aria-hidden="true"></i> 12 burç · şematik</span>')
    o.append('                  <a href="#burclar" class="dh-secbar__all fs-5 text-underline-none text-black dark:text-white">Tüm Burçlar</a>')
    o.append('                </div>')
    o.append('              </div>')
    o.append('              <p class="dh-nwintro">Çarktan bir burç seçin; o burcun günlük yorumu sayfanın başında açılır. '
             'Yorumlar eğlence amaçlıdır, kişisel danışmanlık yerine geçmez.</p>')
    o.append('              <div class="dh-zc__grid">')
    o.append('                <div class="dh-zc__kol">')
    o.append('                  <ul class="dh-zc__list">')
    for anahtar, kicker, baslik, ozet, sik in GIRIS:
        o.append('                    <li class="dh-zc__it" data-dh-donem="%s">' % anahtar)
        o.append('                      <span class="dh-zc__k">%s</span>' % kicker)
        o.append('                      <h3 class="dh-zc__t"><a href="astroloji.html#astroloji">%s</a></h3>' % baslik)
        o.append('                      <p class="dh-zc__s">%s</p>' % ozet)
        o.append('                      <span class="dh-zc__meta"><i class="fas fa-rotate" aria-hidden="true"></i> %s güncellenir</span>' % sik)
        o.append('                    </li>')
    o.append('                  </ul>')
    o.append('                  <a class="dh-zc__cta" href="#burclar">Tüm Burçlar <i class="fas fa-chevron-right" aria-hidden="true"></i></a>')
    o.append('                </div>')
    o.append('                <div class="dh-zc__cark">')
    o.append('            ' + svg())
    o.append('                </div>')
    o.append('              </div>')
    o.append('            </div>')
    o.append('          </div>')
    o.append('        </section>')
    o.append('        ' + ISARET_SON)
    return "\n".join(o) + "\n"


s = open(HEDEF, encoding="utf-8").read()
yeni = blok()

if ISARET_BAS in s:
    b = s.index(ISARET_BAS)
    b = s.rfind("\n", 0, b) + 1
    e = s.index(ISARET_SON) + len(ISARET_SON)
    while e < len(s) and s[e] in " \t":
        e += 1
    if e < len(s) and s[e] == "\n":
        e += 1
    s = s[:b] + yeni + s[e:]
    print("blok güncellendi")
else:
    # "Burçlar ve Tarih Aralıkları" bölümünün ÖNÜNE koy
    m = re.search(r'[ \t]*<section class="section dh-zodwrap', s)
    if not m:
        sys.exit("HATA: #burclar bölümü bulunamadı")
    b = m.start()
    s = s[:b] + yeni + s[b:]
    print("blok eklendi")

open(HEDEF, "w", encoding="utf-8").write(s)
print("%s yazıldı" % HEDEF)
