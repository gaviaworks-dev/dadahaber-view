# -*- coding: utf-8 -*-
"""spor.html üst düzeni — revize-2.docx madde 3.

Talep, kelimesi kelimesine:
  · "Sol taraftaki Formula 1 yapısını direktman kaldıralım."
  · "Futbol, basketbol, voleybol yapısı sistemde durabilir. Lakin onu
     sağ tarafa koyalım."
  · "Diğer yan tarafında, sol tarafında iki tane haber sayfalandırması,
     yani liste şeklinde aşağı doğru kayabilir."
  · "Aşağı indiğimizde bu yeni, eski, çok okunan kısımlar... buradaki
     kısmı bir nevi yukarı almış olacağız."
  · "Sonra puan durumunun altında tenis ve atletizmle alakalı kısmı
     ikinci bir yapı olarak gösterebilir. Daha sonra spor haberlerinin
     liste kısmı gibi kayması lazım."
  · "Canlı maç muhabbetleri, tüm dallarla alakalı kısım kalsın."

ÖNCE:  .dh-hub = [side: Formula 1] [main: Puan Durumu] [news: Spor Gündemi]
       ...sonra spor haberleri listesi, sonra tenis/atletizm
SONRA: .dh-hub = [news: Spor Gündemi — SOL, geniş] [main: Puan Durumu — SAĞ]
       ...sonra tenis/atletizm, sonra spor haberleri listesi

Canlı skor şeridi (.dh-hub__tape) ve "Canlı Maçlar ve Son Skorlar"
bölümü DOKUNULMADI — talep açıkça kalsın diyor.

Yeniden üret:  python3 docs/parts/spor-hub-uret.py
"""
import os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)
HEDEF = "spor.html"


def kapat(s, i, etiket):
    n = 0
    for m in re.finditer(r"<%s\b|</%s>" % (etiket, etiket), s[i:]):
        if m.group(0).startswith("</"):
            n -= 1
            if n == 0:
                return i + m.end()
        else:
            n += 1
    return -1


def satir_basi(s, i):
    j = s.rfind("\n", 0, i)
    return j + 1 if j != -1 else 0


def kes(s, i, etiket):
    """Bloğu satır başından kapanışın sonrasına kadar keser, (blok, kalan)."""
    b = satir_basi(s, i)
    e = kapat(s, i, etiket)
    if e < 0:
        sys.exit("HATA: %s kapanmıyor (%d)" % (etiket, i))
    while e < len(s) and s[e] in " \t":
        e += 1
    if e < len(s) and s[e] == "\n":
        e += 1
    return s[b:e], s[:b] + s[e:]


s = open(HEDEF, encoding="utf-8").read()
degisti = []

# 1) Formula 1 sütunu kaldırılıyor
i = s.find('<div class="dh-hub__side">')
if i >= 0:
    blok, s = kes(s, i, "div")
    if 'data-branch="f1"' not in blok:
        sys.exit("HATA: dh-hub__side içinde F1 yok — yanlış blok kesilecekti")
    degisti.append("Formula 1 sütunu kaldırıldı (%d karakter)" % len(blok))

# 2) hub iki sütuna işaretleniyor (sıra CSS'te: news sol, main sağ)
if '<div class="dh-hub">' in s:
    s = s.replace('<div class="dh-hub">', '<div class="dh-hub dh-hub--ikili">', 1)
    degisti.append("hub .dh-hub--ikili oldu")

# 3) tenis + atletizm satırı, haber listesinin ÖNÜNE alınıyor
ti = s.find('<div class="section pt-0 pb-4 lg:pb-6">')
if ti >= 0 and 'id="tenis"' in s[ti:ti + 12000]:
    blok, s = kes(s, ti, "div")
    hedef = s.find('<div class="section py-4 lg:py-8" id="spor-haberleri">')
    if hedef < 0:
        sys.exit("HATA: spor-haberleri kabı bulunamadı")
    hb = satir_basi(s, hedef)
    s = s[:hb] + blok + s[hb:]
    degisti.append("tenis+atletizm haber listesinin üstüne alındı")

open(HEDEF, "w", encoding="utf-8").write(s)
for d in degisti:
    print("  " + d)
print("%s yazıldı" % HEDEF)
