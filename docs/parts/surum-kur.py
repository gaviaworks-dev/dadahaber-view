# -*- coding: utf-8 -*-
"""Yayın ağacını kurar: kök HTML'leri /<surum>/ altına taşır, köke yönlendirme koyar.

Yayındaki yapı:
    /            -> yönlendirme sayfası, /<surum>/ adresine gider
    /<surum>/    -> sitenin kendisi (tek gerçek kopya)
    /v1/         -> donmuş arşiv (v1-kopya.py üretir)
    /assets/     -> ortak varlık ağacı, sürümler ../assets/ ile paylaşır
    /404.html    -> Pages yalnız KÖK 404'ü kullanır, o yüzden kökte kalır

Yol dönüşümü: "./assets/" -> "../assets/" (srcset içindekiler dâhil).
Sayfa bağlantıları göreli kalır, kopya kendi içinde tutarlı gezinir.
"""
import os, re, shutil, subprocess, sys

SURUM = sys.argv[1] if len(sys.argv) > 1 else "v2"

kok = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True, check=True).stdout.strip()
os.chdir(kok)

htmls = sorted(f for f in os.listdir(".") if f.endswith(".html") and os.path.isfile(f))
if not htmls:
    sys.exit("HATA: kökte HTML yok — önce v2 içeriği alınmalı.")

os.makedirs(SURUM, exist_ok=True)
tasinan = 0
for d in htmls:
    s = open(d, encoding="utf-8").read()
    for a, b in (('"./assets/', '"../assets/'), ("'./assets/", "'../assets/"),
                 ('(./assets/', '(../assets/'), (' ./assets/', ' ../assets/')):
        s = s.replace(a, b)
    open(os.path.join(SURUM, d), "w", encoding="utf-8").write(s)
    tasinan += 1

# 404 kökte de kalsın: Pages proje sitelerinde YALNIZ kök 404.html'i kullanır.
# Kökteki kopya orijinal ./assets/ yollarını taşır.
kok404 = None
if "404.html" in htmls:
    kok404 = open("404.html", encoding="utf-8").read()

for d in htmls:
    os.remove(d)

if kok404 is not None:
    open("404.html", "w", encoding="utf-8").write(kok404)

# Köke yönlendirme. Üç katman: meta refresh · canonical · JS replace.
# JS replace history'ye kayıt bırakmaz — geri tuşu yönlendirme döngüsüne girmez.
# JS kapalıysa meta refresh, o da engelliyse görünür bağlantı çalışır.
open("index.html", "w", encoding="utf-8").write("""<!DOCTYPE html>
<html lang="tr" dir="ltr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="robots" content="noindex, nofollow">
  <title>Dada Haber</title>
  <link rel="icon" href="./assets/images/logos/logo-left.png">
  <meta http-equiv="refresh" content="0; url=./{s}/">
  <link rel="canonical" href="./{s}/">
  <script>location.replace("./{s}/" + location.search + location.hash);</script>
  <style>
    body {{ margin:0; min-height:100vh; display:grid; place-items:center;
           background:#fff; color:#121212;
           font:500 15px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif; }}
    .k {{ text-align:center; padding:24px; }}
    .k img {{ width:200px; height:auto; margin-bottom:18px; }}
    .k p {{ margin:0 0 16px; color:#5c5c5c; }}
    .k a {{ display:inline-block; padding:11px 20px; background:#fcb623; color:#121212;
            font-weight:700; text-decoration:none; border-radius:8px 8px 8px 0; }}
    .k small {{ display:block; margin-top:18px; color:#8a8a8a; font-size:12px; }}
    .k small a {{ background:none; padding:0; color:#8a8a8a; font-weight:500;
                  text-decoration:underline; }}
    @media (prefers-color-scheme: dark) {{
      body {{ background:#121212; color:#fff; }}
      .k p {{ color:#a8a8a8; }}
    }}
  </style>
</head>
<body>
  <div class="k">
    <img src="./assets/images/logos/logo.png" alt="Dada Haber">
    <p>Güncel sürüme yönlendiriliyorsunuz.</p>
    <a href="./{s}/">Devam et &rarr;</a>
    <small>Önceki sürüm: <a href="./v1/">v1 arşivi</a></small>
  </div>
</body>
</html>
""".format(s=SURUM))

print("kök -> %s/ : %d sayfa taşındı" % (SURUM, tasinan))
print("kökte kalan: index.html (yönlendirme)%s" % (", 404.html" if kok404 else ""))

# doğrulama
art = [d for d in os.listdir(SURUM)
       if d.endswith(".html") and re.search(r'["\'(] ?\./assets/', open(os.path.join(SURUM, d), encoding="utf-8").read())]
if art:
    sys.exit("HATA — %s/ altında hâlâ ./assets/ taşıyan sayfa: %s" % (SURUM, ", ".join(art[:5])))
print("yol dönüşümü temiz (./assets/ kalmadı)")
