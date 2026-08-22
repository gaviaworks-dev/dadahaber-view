# -*- coding: utf-8 -*-
"""Spor sayfalarında haber listesini TAM GENİŞLİĞE çıkarır.

Talep (revize-2.docx, madde 5): "Basket ve diğer spor sayfalarında 3'lü
şekilde liste sayfasını oluşturalım; formula1.html sayfası buna örnek."

ÖLÇÜM (1440px): basketbol/voleybol/futbol'de liste ZATEN üç sütun ama
`.dh-sprail` (1fr + 320px yan sütun) içinde kaldığı için ızgara 936px,
kart 312px. formula1.html'de aynı ızgara 1280px, kart 427px. Yani sorun
sütun sayısı değil, GENİŞLİK: kartlar %27 dar ve başlıklar sıkışıyor.
Üstelik sıralama başlığı (`En Yeni · En Eski ...`) zaten rayın DIŞINDA,
tam genişlikte duruyor — başlık geniş, liste dar kalıyordu.

DÜZEN: ray sökülüyor, sıra
    1) yan sütun panelleri (Puan Durumu · Maç Merkezi · Takımlar)
       yan yana üç kolon — `.dh-spor2__ust`
    2) altında tam genişlik üç sütunlu haber listesi
Böylece formula1 düzenine oturuyor ve revize-2 madde 3'ün "puan
durumunun altında ... daha sonra spor haberlerinin liste kısmı" sırası
da sağlanıyor.

Yeniden üret:  python3 docs/parts/spor-duzen-uret.py
"""
import os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)

SAYFALAR = ["basketbol.html", "voleybol.html", "futbol.html", "spor.html"]


def kapat(s, i, etiket):
    """i: '<etiket' başlangıcı. Dengeli kapanıştan SONRAKİ indisi döndürür."""
    ac = "<%s" % etiket
    kap = "</%s>" % etiket
    n, j = 0, i
    for m in re.finditer(r"<%s\b|</%s>" % (etiket, etiket), s[i:]):
        if m.group(0).startswith(kap):
            n -= 1
            if n == 0:
                return i + m.end()
        else:
            n += 1
    return -1


def satir_basi(s, i):
    j = s.rfind("\n", 0, i)
    return j + 1 if j != -1 else 0


n = 0
for dosya in SAYFALAR:
    s = open(dosya, encoding="utf-8").read()

    if '<div class="dh-spor2">' in s:
        print("  %s — zaten yeni düzende" % dosya)
        continue

    i = s.find('<div class="dh-sprail">')
    if i < 0:
        print("  ! %s — ray yok, atlandı" % dosya)
        continue
    b = satir_basi(s, i)
    e = kapat(s, i, "div")
    if e < 0:
        sys.exit("HATA: %s — ray kapanmıyor" % dosya)
    ray = s[i:e]

    # ana sütun: yalnız haber listesi var (ölçüldü)
    mi = ray.find('<div class="dh-sprail__main">')
    me = kapat(ray, mi, "div")
    ana = ray[ray.index(">", mi) + 1:me - len("</div>")].strip()

    # yan sütun panelleri
    yi = ray.find('<div class="dh-sprail__inner">')
    ye = kapat(ray, yi, "div")
    yan = ray[ray.index(">", yi) + 1:ye - len("</div>")].strip()

    # Sıralama başlığı (`En Yeni · En Eski ...`) rayın DIŞINDA, hemen
    # üstündeydi. Yeni düzende paneller araya girdiği için başlık listeden
    # kopuyordu — ölçüldü, ekranda panellerin üstünde kalıyordu.
    # Başlık listenin içine, ızgaranın hemen üstüne alınıyor.
    baslik = ""
    hm = None
    for hm in re.finditer(r'[ \t]*<header class="page-header[^"]*"[^>]*>', s[:b]):
        pass
    if hm and 'data-dh-pick' in s[hm.start():b]:
        hb = satir_basi(s, hm.start())
        he = kapat(s, hm.start(), "header")
        if he > 0 and he <= b:
            baslik = s[hb:he].rstrip("\n")
            # başlığı eski yerinden çıkar
            son = he
            while son < len(s) and s[son] in " \t":
                son += 1
            if son < len(s) and s[son] == "\n":
                son += 1
            s = s[:hb] + s[son:]
            kayma = son - hb
            b -= kayma
            e -= kayma

    # REVİZE 2 (22 Ağustos): alttaki üçlü panel (Puan Durumu · Maç Merkezi
    # · Takımlar) KALDIRILDI. Talep: "aşağı indiğimiz zaman ikinci bir puan
    # durumu var, ona gerek yok... kısayol takımlar kısmını kaldıralım...
    # maç merkezi yukarıda zaten var."
    # ÖLÇÜM: üçü de sayfanın üstündeki lig merkezinde (futbol/basketbol/
    # voleybol) ya da hub'da (spor.html) zaten duruyordu — birebir tekrar.
    # `yan` değişkeni artık kullanılmıyor; blok tamamen atılıyor.
    yeni = (
        '                    <div class="dh-spor2">\n'
        '                      <div class="dh-spor2__liste">\n'
        + (baslik + "\n" if baslik else "")
        + ana + "\n"
        '                      </div>\n'
        '                    </div>\n'
    )
    s = s[:b] + yeni + s[e:]
    open(dosya, "w", encoding="utf-8").write(s)
    print("  %s — ray söküldü, liste tam genişliğe çıktı" % dosya)
    n += 1

print("%d sayfa yeni düzende" % n)
