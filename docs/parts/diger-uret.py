# -*- coding: utf-8 -*-
"""diger.html — "Diğer" perdeleme menüsünün sayfa karşılığı.

Ana menü 11'den 8'e indi; menüden çıkan hiçbir kategori silinmedi. Bu sayfa
tam dizini taşır, böylece "Diğer" başlığının gerçek bir hedefi olur ve hiçbir
kategori bağlantısı kaybolmaz. Menü verisi uret.py'den okunur — iki yerde
elle tutulan liste olmaz.
"""
import os, re, subprocess, sys

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)
sys.path.insert(0, os.path.join(kok, "docs", "parts"))
from sayfa_basligi import basli
sys.path.insert(0, os.path.join(kok, "docs", "parts"))
from uret import MENU, FORMAT, ext          # noqa: E402

SABLON = "docs/parts/sayfa-sablon.html"
HEDEF = "diger.html"

ana = [m for m in MENU if m[0] != "diger"]
diger = [m for m in MENU if m[0] == "diger"][0]

g = []
w = g.append
w(basli("Dada Haber", "Tüm Kategoriler",
        "Ana menüde yer alan başlıklar ve menüden çıkan tüm kategoriler, formatlar "
        "ve servisler bu dizinde.",
        [("Tüm Kategoriler", None)], "img-11.jpg", "50% 48%"))

w('        <section class="section panel">\n')
w('          <div class="container max-w-xl">\n')
w('            <div class="dh-dizin">\n')

# --- ana kategoriler
w('              <div>\n')
w('                <div class="section-header panel dh-secbar">\n')
w('                  <h2 class="h5 xl:h4 m-0 text-black dark:text-white">Ana Kategoriler</h2>\n')
w('                  <div class="dh-secbar__tools">\n')
w('                    <span class="dh-nwstamp"><i class="fas fa-bars" aria-hidden="true"></i> %d başlık</span>\n' % len(ana))
w('                  </div>\n                </div>\n')
w('                <div class="dh-dizin__main">\n')
for slug, ad, hub, is_, _ in ana:
    w('                  <a class="dh-dizin__cat" data-cat="%s" href="%s"><span><b>%s</b><span>%s</span></span></a>\n'
      % (slug, hub, ad, is_))
w('                </div>\n              </div>\n\n')

# --- Diğer altındaki gruplar
w('              <div>\n')
w('                <div class="section-header panel dh-secbar">\n')
w('                  <h2 class="h5 xl:h4 m-0 text-black dark:text-white">Diğer Kategoriler</h2>\n')
w('                  <div class="dh-secbar__tools">\n')
w('                    <span class="dh-nwstamp"><i class="fas fa-list" aria-hidden="true"></i> %d grup</span>\n'
  % len(diger[4]))
w('                  </div>\n                </div>\n')
w('                <div class="dh-dizin__cols">\n')
for baslik, ogeler in diger[4]:
    w('                  <div class="dh-dizin__grp">\n')
    w('                    <h3>%s</h3>\n                    <ul>\n' % baslik)
    for t, h in ogeler:
        w('                      <li><a href="%s"%s>%s</a></li>\n' % (h, ext(h), t))
    w('                    </ul>\n                  </div>\n')
w('                </div>\n              </div>\n\n')

# --- yayın formatları
w('              <div>\n')
w('                <div class="section-header panel dh-secbar">\n')
w('                  <h2 class="h5 xl:h4 m-0 text-black dark:text-white">Yayın Formatları</h2>\n')
w('                </div>\n')
w('                <div class="dh-dizin__main">\n')
for ad, h, ik in FORMAT:
    w('                  <a class="dh-dizin__cat" data-cat="diger" href="%s"><span><b>%s</b></span></a>\n' % (h, ad))
w('                </div>\n              </div>\n')

w('            </div>\n          </div>\n        </section>\n')
GOVDE = "".join(g)

s = open(SABLON, encoding="utf-8").read()
s = s.replace("<title>SAYFA BAŞLIĞI — Dada Haber</title>",
              "<title>Tüm Kategoriler — Dada Haber</title>")
if 'data-dh-cat=""' in s:
    s = s.replace('data-dh-cat=""', 'data-dh-cat="diger"', 1)
else:
    s = re.sub(r'<body\s', '<body data-dh-cat="diger" ', s, count=1)

m = re.search(r"[ \t]*<!-- ={10,} SAYFA GÖVDESİ BURAYA ={10,}.*?={10,} -->\n", s, re.S)
if not m:
    sys.exit("HATA: şablonda gövde yuvası bulunamadı")
s = s[:m.start()] + GOVDE + s[m.end():]

open(HEDEF, "w", encoding="utf-8").write(s)
print("%s yazıldı (%d satır)" % (HEDEF, len(s.splitlines())))
