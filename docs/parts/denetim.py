# -*- coding: utf-8 -*-
"""Yayın öncesi statik denetim — tarayıcı gerektirmez, saniyeler sürer.
Playwright denetimi (audit.js) bunun yerine geçmez, tamamlar."""
import glob, os, re, sys, collections

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sayfalar = sorted(glob.glob("*.html"))
metin = {f: open(f, encoding="utf-8").read() for f in sayfalar}
idler = {f: re.findall(r'\bid="([^"]+)"', s) for f, s in metin.items()}
hata = []

# 1) kırık dosya hedefi
mevcut = set(sayfalar)
kirik = collections.defaultdict(set)
for f, s in metin.items():
    for h in re.findall(r'(?:href|src)="([^"]+)"', s):
        if h.startswith(("http", "mailto:", "#", "tel:", "data:", "javascript:")):
            continue
        yol = h.split("#")[0].split("?")[0]
        if not yol:
            continue
        if yol.startswith("./"):
            yol = yol[2:]
        if yol.startswith("../") or yol.startswith("/"):
            kirik["MUTLAK/ÜST YOL: " + h].add(f); continue
        if yol.endswith(".html"):
            if yol not in mevcut: kirik[yol].add(f)
        elif not os.path.exists(yol):
            kirik[yol].add(f)
if kirik:
    hata.append("kırık dosya hedefi: %d — %s" % (len(kirik), ", ".join(sorted(kirik)[:6])))

# 2) kırık çapa
eksik = set()
for f, s in metin.items():
    for h in re.findall(r'href="([^"]+#[^"]+)"', s):
        if h.startswith(("http", "mailto:")): continue
        yol, anc = h.split("#", 1)
        if yol.startswith("./"): yol = yol[2:]
        hedef = yol or f
        if hedef in idler and anc and anc not in idler[hedef]:
            eksik.add("%s#%s" % (hedef, anc))
if eksik:
    hata.append("kırık çapa: %d — %s" % (len(eksik), ", ".join(sorted(eksik)[:6])))

# 3) yinelenen id
for f, l in idler.items():
    yin = [k for k, n in collections.Counter(l).items() if n > 1 and k]
    if yin:
        hata.append("%s: yinelenen id — %s" % (f, ", ".join(yin[:4])))

# 4) noindex her sayfada
yok = [f for f, s in metin.items() if 'name="robots"' not in s or "noindex" not in s]
if yok:
    hata.append("noindex yok: %s" % ", ".join(yok))

# 5) lang="tr"
yok = [f for f, s in metin.items() if 'lang="tr"' not in s[:400]]
if yok:
    hata.append('lang="tr" yok: %s' % ", ".join(yok))

# 6) v2 kabuğu her sayfada (404/coming-soon footer taşımaz)
for f, s in metin.items():
    if "dh-v2-nav__list" not in s: hata.append("%s: v2 gezinti yok" % f)
    if "theme/v2.css" not in s: hata.append("%s: v2.css bağlantısı yok" % f)
    if f not in ("404.html", "coming-soon.html") and "dh-v2-foot" not in s:
        hata.append("%s: v2 footer yok" % f)

# 7) custom.min.css ve dh-*.js dokunulmamış mı (v1 kopyası paylaşıyor)
import subprocess
d = subprocess.run(["git", "diff", "--name-only", "v1", "--",
                    "assets/css/theme/custom.min.css", "assets/css/theme/demo-six.min.css",
                    "assets/js/dh-astro.js", "assets/js/dh-gal.js", "assets/js/dh-gebelik.js",
                    "assets/js/dh-hesap.js", "assets/js/dh-kadin.js", "assets/js/dh-lig.js",
                    "assets/js/dh-lig-veri.js", "assets/js/dh-listen.js", "assets/js/dh-panel.js",
                    "assets/js/dh-reels.js", "assets/js/dh-share.js", "assets/js/dh-tabs.js",
                    "assets/js/dh-toc.js", "assets/js/dh-track.js", "assets/js/dh-yorum.js"],
                   capture_output=True, text=True).stdout.split()
if d:
    hata.append("v1 PAYLAŞILAN DOSYA DEĞİŞMİŞ (v1 donmuş kalmalı): %s" % ", ".join(d))

print("%d sayfa denetlendi" % len(sayfalar))
if hata:
    print("\nHATA (%d):" % len(hata))
    for h in hata: print("  ✗", h)
    sys.exit(1)
print("TEMİZ")
