# -*- coding: utf-8 -*-
"""v2.css'in @import parçalarını tek dosyaya düzleştirir (yayın öncesi).

Neden: @import zincirlenmiş indirme yapar — tarayıcı v2.css'i indirip
ayrıştırmadan parçaları görmez. Altı parça = altı seri gidiş-dönüş.
Geliştirmede parçalar ayrı kalır (paralel ajan çakışmasını önler),
yayında tek dosyaya düzleşir.

Kullanım:  python3 docs/parts/duzlestir.py
Çıktı:     assets/css/theme/v2.css (parçalar assets/css/theme/v2/ altında kalır)
"""
import os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)

HEDEF = "assets/css/theme/v2.css"
KAYNAK = "docs/parts/v2.css.src"

# İlk çalıştırmada @import'lu hâli kaynak olarak sakla
if not os.path.exists(KAYNAK):
    if "@import" not in open(HEDEF, encoding="utf-8").read():
        sys.exit("HATA: %s zaten düzleşmiş ve kaynak yok." % HEDEF)
    os.makedirs(os.path.dirname(KAYNAK), exist_ok=True)
    open(KAYNAK, "w", encoding="utf-8").write(open(HEDEF, encoding="utf-8").read())
    print("kaynak saklandı: %s" % KAYNAK)

src = open(KAYNAK, encoding="utf-8").read()
parcalar = re.findall(r'@import\s+url\("\./(v2/[^"]+)"\);', src)
if not parcalar:
    sys.exit("HATA: %s içinde @import bulunamadı." % KAYNAK)

out = ['/* ============================================================================\n',
       '   Dada Haber v2 — DÜZLEŞTİRİLMİŞ ÇIKTI. ELLE DÜZENLEME.\n',
       '   Kaynak parçalar: assets/css/theme/v2/*.css\n',
       '   Yeniden üret:    python3 docs/parts/duzlestir.py\n',
       '   ========================================================================== */\n']
top = 0
for p in parcalar:
    yol = os.path.join("assets/css/theme", p)
    if not os.path.exists(yol):
        sys.exit("HATA: parça yok — %s" % yol)
    icerik = open(yol, encoding="utf-8").read()
    n = len(icerik.splitlines())
    top += n
    out.append("\n/* ==== %s (%d satır) ==== */\n" % (p, n))
    out.append(icerik)
    if not icerik.endswith("\n"):
        out.append("\n")

open(HEDEF, "w", encoding="utf-8").write("".join(out))
print("%d parça -> %s (%d satır, %.0f KB)"
      % (len(parcalar), HEDEF, top, os.path.getsize(HEDEF) / 1024))
