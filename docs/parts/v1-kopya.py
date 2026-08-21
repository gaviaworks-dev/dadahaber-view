# -*- coding: utf-8 -*-
"""v1'in donmuş kopyasını /v1/ klasörüne çıkarır.

Neden HTML-only: varlık ağacı 189 MB. v2 varlıklara yalnız EKLİYOR
(custom.min.css ve mevcut dh-*.js değiştirilmedi), bu yüzden v1 kopyası
../assets/ üzerinden aynı ağacı paylaşabilir ve yine de donmuş kalır.

Yol dönüşümü: "./assets/" -> "../assets/"
Sayfa bağlantıları göreli kalır (spor.html -> /v1/spor.html), yani kopya
kendi içinde tutarlı gezinir.
"""
import os, re, subprocess, sys

DAL = sys.argv[1] if len(sys.argv) > 1 else "v1"
HEDEF = "v1"

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)

dosyalar = subprocess.run(["git", "ls-tree", "-r", "--name-only", DAL],
                          capture_output=True, text=True, check=True).stdout.split()
htmls = [d for d in dosyalar if d.endswith(".html") and "/" not in d]
if not htmls:
    sys.exit("HATA: %s dalında kök HTML bulunamadı" % DAL)

os.makedirs(HEDEF, exist_ok=True)
n = 0
for d in htmls:
    s = subprocess.run(["git", "show", "%s:%s" % (DAL, d)],
                       capture_output=True, text=True, check=True).stdout
    s = s.replace('"./assets/', '"../assets/').replace("'./assets/", "'../assets/")
    s = s.replace('(./assets/', '(../assets/')
    s = s.replace(' ./assets/', ' ../assets/')   # srcset içindeki virgülden sonraki yollar
    # donmuş kopya olduğunu sayfada görünür kıl
    s = s.replace("</body>", """  <div style="position:fixed;left:0;right:0;bottom:0;z-index:99999;background:#111;color:#fff;
    font:500 12px/1.4 system-ui,sans-serif;padding:9px 14px;display:flex;gap:12px;align-items:center;
    justify-content:center;flex-wrap:wrap">
    <span><b style="color:#fcb623">v1 arşivi</b> — Dada Haber arayüz prototipinin R8 sonundaki donmuş hâli.</span>
    <a href="../index.html" style="color:#fcb623;font-weight:700">Güncel sürüme (v2) git &rarr;</a>
  </div>
</body>""", 1)
    open(os.path.join(HEDEF, d), "w", encoding="utf-8").write(s)
    n += 1

# arama motorlarına kapalı olduğu zaten her sayfada noindex ile duruyor
kirik = []
for d in os.listdir(HEDEF):
    s = open(os.path.join(HEDEF, d), encoding="utf-8").read()
    # dikkat: '../assets/' de './assets/' alt dizesini içerir — tırnakla ara
    for kalip in ('"./assets/', "'./assets/", '(./assets/'):
        if kalip in s:
            kirik.append(d)
            break
print("%s -> %s/ : %d sayfa" % (DAL, HEDEF, n))
if kirik:
    print("UYARI — hâlâ ./assets/ taşıyan sayfa: %s" % ", ".join(kirik[:5]))
else:
    print("yol dönüşümü temiz (./assets/ kalmadı)")
